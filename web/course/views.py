import json
import re

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max, Q, Sum
from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from . import payments
from accounts.models import Classroom, Enrollment, Profile, can_open, can_save, class_for, has_full_access, is_free, unit_of
from accounts.permissions import forbidden, is_teacher, teacher_required
from accounts.ratelimit import ratelimit
from . import content, grading
from . import assess, exams, packets, slides
from .context import THEMES
from .site_pages import course_facts
from .models import Draft, ExamAttempt, FRQScore, IssuedPacket, QuizAttempt, Release, Response, StepDone

AREAS = ("notes", "practice", "quiz", "testprep")
AREA_KIND = {"notes": "notes", "practice": "practice", "quiz": "quiz", "testprep": "testprep"}
FREE_PRACTICE = 4          # practice problems anyone can try without an account


def _free_ids(pub):
    return {it["id"] for it in pub["practice"][:FREE_PRACTICE]}


def _preview(pub):
    """What a visitor without full access receives: the video(s) and the first few practice problems. Nothing else
    leaves the server, so the paywall can't be bypassed from the page source."""
    videos = [b for st in pub["steps"] for b in st["blocks"] if b["type"] == "video"]
    return {**pub, "steps": [{"title": "Video", "blocks": videos}] if videos else [],
            "practice": pub["practice"][:FREE_PRACTICE], "quiz": [], "mcq": [], "frq": [], "preview": True}


def _class_course(user):
    """ "AB" or "BC" for a student in a class (the class's course), else None: it picks which version of a two-version
    topic or unit test their Next links lead to (docs/ab-bc-versions.md)."""
    c = class_for(user)
    return c.course if c is not None else None


def _twin(num):
    """For a topic taught in two versions (6.14 AB and 6.14 BC), the other version, for a link in the lesson head."""
    meta = content.topic_meta(num)[1]
    if not meta or not meta["twin"] or meta["twin"] not in content.available():
        return None
    other = content.topic_meta(meta["twin"])[1]
    return {"n": other["n"], "label": other["label"], "course": other["tag"], "mine": meta["tag"]}


def _lesson(num, course=None):
    pub = content.public(num)
    if not pub:
        raise Http404("That lesson isn't written yet.")
    unit, meta = content.topic_meta(num)
    prev, nxt = content.neighbours(num, course)
    return pub, unit, prev, nxt


def home(request):
    """Teachers land on their dashboard and signed-in students on the course map. Everyone else gets the landing page,
    which sorts them into the student and teacher pages."""
    if is_teacher(request.user):
        return redirect("teacher")
    if request.user.is_authenticated:
        return redirect("student_dashboard")
    free = _free_summary()
    return render(request, "site/landing.html", {
        "free": free, "facts": course_facts(),
        "trig": next((f for f in free if f["module"] and f["first"]), None),
        "start": next((f["first"] for f in free if not f["module"] and f["first"]), None)})


def _free_summary():
    """The free lessons, for the landing and student pages: the free modules, then Units 1-3."""
    out = []
    for u in content.syllabus():
        if u["free"]:
            ready = [t for t in u["topics"] if t["n"] in content.available()]
            out.append({"name": u["short"] if u["module"] else f"Unit {u['n']}", "title": u["title"], "module": u["module"],
                        "count": len(ready), "first": ready[0]["n"] if ready else None})
    return out


def for_students(request):
    return render(request, "site/students.html", {"free": _free_summary(), "plan": payments.PLANS["student"]})


def for_teachers(request):
    return render(request, "site/teachers.html",
                  {"plans": [dict(p, key=k) for k, p in payments.PLANS.items() if p["who"] == "teacher"]})


def membership(request):
    return render(request, "site/membership.html", {
        "plans": [dict(p, key=k) for k, p in payments.PLANS.items()], "enabled": payments.payments_enabled()})


def checkout(request, plan):
    """PLACEHOLDER for Stripe Checkout (course/payments.py). Until payments are on, this says checkout opens soon."""
    if plan not in payments.PLANS:
        raise Http404
    url = payments.checkout_url(request, plan)
    if url:
        return redirect(url)
    return render(request, "site/checkout_soon.html", {"plan": payments.PLANS[plan]})


def course_map(request, module=False):
    have = content.available()
    done, best = {}, {}
    if request.user.is_authenticated:
        for row in StepDone.objects.filter(user=request.user).values("topic").annotate(n=Count("id")):
            done[row["topic"]] = row["n"]
        best = {r["topic"]: r for r in QuizAttempt.objects.filter(user=request.user)
                .values("topic").annotate(best=Max("score"), total=Max("total"))}
    units = []
    for u in content.syllabus():
        topics = []
        for t in u["topics"]:
            c = content.counts(t["n"]) if t["n"] in have else {}
            topics.append({**t, "ready": t["n"] in have,
                           "steps": c.get("steps", 0), "done": done.get(t["n"], 0),
                           "quiz": best.get(t["n"])})
        # a unit's test, or its AB and BC tests (Units 6-8), each with the student's best multiple-choice score
        tests = [{**v, "label": content.test_label(v["num"]), "best": best.get(v["num"])} for v in content.test_versions(u["n"])]
        units.append({**u, "topics": topics, "tests": tests})
    full = has_full_access(request.user)
    for u in units:
        u["locked"] = not u["free"] and not full          # paid units are tagged; free ones carry no tag
    if module:
        page = {"page_title": "Trig Course", "page_intro": "A refresher on everything from trigonometry that calculus "
                "uses, from right triangles to inverse trig functions. Each lesson has a video, notes, practice and a quiz."}
    else:
        page = {"page_title": "AP Calc Course", "page_intro": "One lesson per topic in the College Board course "
                "description, AB and BC. Lessons that are ready are highlighted."}
    groups = [{"modules": module, "units": [u for u in units if u["module"] == module]}]
    return render(request, "course/map.html", {**page, "groups": groups,
                                               "current_unit": _current_unit(request.user),
                                               "exams": [] if module else exams.available()})


def trig_course(request):
    return course_map(request, module=True)


def videos(request):
    """Every lesson video in one place (Adder 2026-10-12): pick one and it plays here, without the lesson's notes.
    The trig module first, then Units 1-10; only lessons whose video is published are listed."""
    have = {p.name for p in settings.VIDEO_DIR.glob("*.mp4")} if settings.VIDEO_DIR.exists() else set()
    groups = []
    for u in sorted(content.syllabus(), key=lambda u: (not u["module"], u["n"])):
        items = [{"n": t["n"], "label": t["label"], "title": t["title"], "slug": content.slug(t["n"]),
                  "captions": (settings.VIDEO_DIR / f"{content.slug(t['n'])}.vtt").exists()}
                 for t in u["topics"] if f"{content.slug(t['n'])}.mp4" in have]
        if items:
            groups.append({"name": u["heading"], "n": u["n"], "items": items})
    return render(request, "course/videos.html", {"groups": groups})


@login_required
def student_dashboard(request):
    """A student's own page: where they left off, progress by unit, recent quiz and exam scores, their class."""
    if is_teacher(request.user):
        return redirect("teacher")
    steps = dict(StepDone.objects.filter(user=request.user).values("topic").annotate(n=Count("id")).values_list("topic", "n"))
    have = content.available()
    units = []
    for u in sorted(content.syllabus(), key=lambda u: (not u["module"], u["n"])):
        total = done = 0
        for t in u["topics"]:
            if t["n"] in have:
                c = content.counts(t["n"])
                total += c.get("steps", 0)
                done += min(steps.get(t["n"], 0), c.get("steps", 0))
        if total:
            units.append({"name": u["heading"], "n": u["n"], "module": u["module"], "done": done, "total": total,
                          "pct": round(100 * done / total), "open": can_open(request.user, f"{u['n']}.1"),
                          "url": reverse("trig") if u["module"] else f"{reverse('map')}#unit-{u['n']}"})
    last = (StepDone.objects.filter(user=request.user).order_by("-id").values_list("topic", flat=True).first()
            or Response.objects.filter(user=request.user).order_by("-id").values_list("topic", flat=True).first())
    resume = None
    if last and last in have and not last.startswith("U"):
        meta = content.topic_meta(last)[1]
        resume = {"n": last, "label": content.label(last), "title": meta["title"] if meta else last}
    quizzes = [{"n": a.topic, "label": content.label(a.topic) if not a.topic.startswith("U") else content.test_label(a.topic),
                "score": a.score, "total": a.total, "at": a.at}
               for a in QuizAttempt.objects.filter(user=request.user).order_by("-at")[:8]]
    tries = ExamAttempt.objects.filter(user=request.user).order_by("-id")[:5]
    klass = class_for(request.user)
    extra = {}
    if klass is not None:
        from classwork.student import extras
        extra = extras(request.user, klass)
        quizzes = [{"n": x["a"].topic, "label": content.label(x["a"].topic) if not x["a"].topic.startswith("U") else content.test_label(x["a"].topic),
                    "score": x["score"], "total": x["total"], "at": x["a"].at, "waiting": x["waiting"]} for x in extra.pop("quizzes")]
    return render(request, "course/student_dashboard.html", {
        "units": units, "resume": resume, "quizzes": quizzes, "exam_attempts": tries,
        "klass": klass, "full": has_full_access(request.user), **extra})


def trig_formulas(request):
    return formulas(request, module=True)


def formulas(request, module=False):
    """Key ideas and formulas (the course formula sheet): every formula box and definition from every lesson, filled in, by unit, each
    tagged with its topic. A student sees it all, with the topics past the furthest one they've reached grayed."""
    order = [t["n"] for u in content.syllabus() for t in u["topics"]]
    reached = None
    if request.user.is_authenticated:
        touched = set(StepDone.objects.filter(user=request.user).values_list("topic", flat=True))
        touched |= set(Response.objects.filter(user=request.user).values_list("topic", flat=True))
        touched |= set(Draft.objects.filter(user=request.user).values_list("topic", flat=True))
        idx = [order.index(t) for t in touched if t in order]
        reached = max(idx) if idx else -1
    units = []
    for u in content.syllabus():
        if u["module"] != module:
            continue
        rows = []
        for t in u["topics"]:
            pub = content.public(t["n"]) if t["n"] in content.available() else None
            if not pub or not pub.get("formulas"):
                continue
            ahead = reached is not None and order.index(t["n"]) > reached
            rows.append({"n": t["n"], "label": t["label"], "title": t["title"], "ahead": ahead, "items": pub["formulas"]})
        if rows:
            units.append({"n": u["n"], "title": u["title"], "heading": u["heading"], "rows": rows})
    title = "Trig Formulas" if module else "Calc Formula Sheet"
    return render(request, "course/formulas.html", {"units": units, "graying": reached is not None, "page_title": title})


def _current_unit(user):
    """The unit a student is working in: the one holding their most recent activity (a step finished, an answer
    checked or typed). Unit 1 for visitors and newcomers. The course map opens that unit and folds the rest."""
    if not user.is_authenticated:
        return 1
    latest = []
    for qs, field in ((StepDone.objects.filter(user=user), "at"), (Response.objects.filter(user=user), "at"),
                      (Draft.objects.filter(user=user), "updated")):
        row = qs.order_by("-" + field).values("topic", field).first()
        if row:
            latest.append((row[field], row["topic"]))
    if not latest:
        return 1
    topic = max(latest)[1]
    return unit_of(topic) or 1


def _gate(request, kind, num):
    """The class gate for this student and this work (classwork.access), with times shown in the class's zone."""
    from classwork import access, calendar as cal, setup as cs
    g = access.gate(request.user, kind, num)
    c = g["classroom"]
    if c is not None:
        show = cs.show(c)
        fmt = lambda m: m.astimezone(cal.zone(c)).strftime("%a %b %-d, %-I:%M %p").replace(":00 ", " ") if m else ""
        g.update(opens_text=fmt(g["opens"]), due_text=fmt(g["due"]) if show["due_dates"] else "")
    return g


GATE_WORDS = {"quiz": "quiz", "unittest": "unit test", "notes": "lesson", "practice": "practice set", "testprep": "test prep"}


def _gate_page(request, g, kind, ctx):
    what = GATE_WORDS.get(kind, "work")
    msg = {"not_yet": f"This {what} opens {g.get('opens_text')}. Your teacher put it on the class schedule.",
           "off": f"Your class doesn't use this {what} on the site.",
           "paper": f"Your teacher gives this {what} on paper, in class.",
           "closed": f"This {what} closed {g.get('due_text') or 'on its due date'}. If you need more time, ask your teacher."}[g["state"]]
    return render(request, "course/gate.html", {**ctx, "gate": g, "gate_message": msg}, status=200)


def unit_test(request, num):
    if not can_open(request.user, num):
        return render(request, "course/locked.html", {"what": "Unit tests"})
    if not request.user.is_authenticated:
        # free unit tests are open, but a test is something you take and get scored on: that needs a (free) account
        return redirect(f"{reverse('signup')}?next={request.path}")
    pub = content.public(num)
    if not pub:
        raise Http404("That unit test isn't written yet.")
    g = _gate(request, "unittest", num)
    if g["state"] in ("not_yet", "off", "paper") or (g["state"] == "closed" and not QuizAttempt.objects.filter(
            user=request.user, topic=num, classroom=g["classroom"]).exists()):
        return _gate_page(request, g, "unittest", {"L": {"title": content.test_label(num), "label": num}, "num": num, "test_page": True})
    pub, info = assess.draw(request, num, pub)
    state = {"correct": [], "steps_done": [], "drafts": _drafts(request.user, num),
             "frq": {s.part: s.earned for s in FRQScore.objects.filter(user=request.user, topic=num)},
             "quiz": [{"score": a.score, "total": a.total, "at": a.at.isoformat()}
                      for a in QuizAttempt.objects.filter(user=request.user, topic=num)[:5]],
             "assess": assess.state(request, num, info, content.private(num))}
    if state["assess"]["mode"] == "class":
        state["quiz"] = []          # class students don't see scores until release
    else:
        state["print"] = {"forms": [{"form": f, "test": reverse("test_pdf", args=[num, f, "test"]),
                                     "key": reverse("test_pdf", args=[num, f, "key"])} for f in _paper_forms(num)]}
    # Units 6-8 come in an AB and a BC version: the page names this one and links the other (docs/ab-bc-versions.md)
    unit = content.unit_of_test(num)
    course, mine = content.test_course(num), _class_course(request.user)
    versions = [{**v, "label": content.test_label(v["num"]), "on": v["num"] == num, "url": reverse("unit_test", args=[v["num"]])}
                for v in content.test_versions(unit)] if course else []
    return render(request, "course/unittest.html", {"L": pub, "num": num, "lesson_json": pub, "state_json": state, "gate": g,
                                                    "test_label": content.test_label(num), "course": course,
                                                    "versions": versions, "class_course": mine if course else None})


def lesson(request, num, area="notes"):
    if area not in AREAS:
        raise Http404
    pub, unit, prev, nxt = _lesson(num, _class_course(request.user))
    pub = assess.strip(pub)
    if not can_open(request.user, num):
        pub = _preview(pub)
        state = {"steps_done": [], "correct": [], "frq": {}, "quiz": [], "full": False}
        return render(request, f"course/{area}.html", {
            "L": pub, "unit": unit, "num": num, "area": area, "prev": prev, "next": nxt,
            "lesson_json": pub, "state_json": state, "packet": False, "OPEN": False, "twin": _twin(num)})
    if not request.user.is_authenticated:
        # a free lesson for a visitor: everything to read and check, nothing saved (answers stay in this browser)
        state = {"full": True, "visitor": True, "steps_done": [], "correct": [], "frq": {}, "quiz": []}
        return render(request, f"course/{area}.html", {
            "L": pub, "unit": unit, "num": num, "area": area, "prev": prev, "next": nxt,
            "lesson_json": pub, "state_json": state, "packet": False, "OPEN": True, "twin": _twin(num)})
    kind = AREA_KIND[area]
    g = _gate(request, kind, num)
    ctx = {"L": pub, "unit": unit, "num": num, "area": area, "prev": prev, "next": nxt, "OPEN": True, "twin": _twin(num)}
    if g["state"] == "not_yet" or (kind == "quiz" and g["state"] in ("off", "paper")):
        return _gate_page(request, g, kind, ctx)
    if kind == "quiz" and g["state"] == "closed" and not QuizAttempt.objects.filter(
            user=request.user, topic=num, classroom=g["classroom"]).exists():
        return _gate_page(request, g, kind, ctx)
    info = None
    if area == "quiz":
        pub, info = assess.draw(request, num, _lesson(num)[0])
    drafts = _drafts(request.user, num)
    state = {"full": True, "drafts": drafts,
        "steps_done": list(StepDone.objects.filter(user=request.user, topic=num).values_list("step", flat=True)),
        "correct": list(Response.objects.filter(user=request.user, topic=num, correct=True)
                        .values_list("item", flat=True).distinct()),
        "frq": {s.part: s.earned for s in FRQScore.objects.filter(user=request.user, topic=num)},
        "quiz": [{"score": a.score, "total": a.total, "at": a.at.isoformat()}
                 for a in QuizAttempt.objects.filter(user=request.user, topic=num)[:5]],
    }
    # notes blanks already answered right (or shown on request) come back filled in from the answer key
    blanks = (content.private(num) or {}).get("blanks", {})
    state["shown"] = {b: blanks[b] for b in set(state["correct"]) | {k for k, d in drafts.items() if d["r"]} if b in blanks}
    if info is not None:
        state["assess"] = assess.state(request, num, info, content.private(num))
        if state["assess"]["mode"] == "class":
            state["quiz"] = []
    if g["state"] == "closed":
        state["closed"] = True
    return render(request, f"course/{area}.html", {
        "L": pub, "unit": unit, "num": num, "area": area, "prev": prev, "next": nxt,
        "lesson_json": pub, "state_json": state, "packet": packets.available(num), "OPEN": True, "gate": g,
        "slides": _is_teacher(request.user) and slides.manifest(num) is not None, "twin": _twin(num),
    })


# ------------------------------------------------------------------ JSON API
def _body(request):
    """The JSON object a page posted, or {} for anything else (a list, a number, broken JSON)."""
    try:
        d = json.loads(request.body or b"{}")
    except ValueError:
        return {}
    return d if isinstance(d, dict) else {}


def _str(v, n):
    """A posted value as a string of at most n characters; anything that isn't a string or number is ''."""
    if isinstance(v, bool) or not isinstance(v, (str, int, float)):
        return ""
    return str(v)[:n]


def _int(v, default=-1):
    try:
        return int(v)
    except (TypeError, ValueError, OverflowError):
        return default


@require_POST
@ratelimit("api-check", "user", 300, 60, json=True)
def api_check(request, num):
    """Check one answer. Returns correctness plus the solution once it has been tried.
    Visitors without full access may check only the free practice problems, and nothing is saved for them."""
    d = _body(request)
    priv = content.private(num)
    if not priv:
        raise Http404
    item, given, area = _str(d.get("item"), 40), _str(d.get("given"), 300), _str(d.get("area"), 10) or "notes"
    if not can_save(request.user, num):
        # not recorded: a visitor on a free lesson (any item), or anyone on a paid lesson's free practice problems
        if item in priv["blanks"] and is_free(num) and not num.startswith("U"):
            ok = grading.check_blank(given, priv["blanks"][item])
            out = {"correct": ok}
            if ok or d.get("reveal"):
                out["answer"] = priv["blanks"][item]
            return JsonResponse(out)
        pub = content.public(num)
        free_item = is_free(num) or item in _free_ids(pub)
        if num.startswith("U") or not free_item or item not in priv["items"]:
            return JsonResponse({"error": "members only"}, status=403)
        spec = priv["items"][item]
        out = {}
        if given and "answer" in spec:
            out["correct"] = grading.check(given, spec["answer"])
        if given or d.get("reveal"):
            out["solution"], out["display"] = spec.get("solution", ""), spec.get("answer", {}).get("display", "")
        return JsonResponse(out)
    if area not in ("notes", "practice", "testprep", "frq"):
        return JsonResponse({"error": "bad area"}, status=400)
    if not num.startswith("U"):
        from classwork.access import gate
        st = gate(request.user, "notes" if item in priv["blanks"] else AREA_KIND.get(area, "testprep"), num)["state"]
        if st == "not_yet":
            return JsonResponse({"error": "not open yet"}, status=403)
        if st == "closed" and area == "practice":
            return JsonResponse({"error": "closed"}, status=403)
    if item in priv["blanks"]:
        ok = grading.check_blank(given, priv["blanks"][item])
        if ok or not d.get("live"):         # live checks while typing only record a hit, never a miss
            Response.objects.create(user=request.user, topic=num, item=item, area="notes", given=given, correct=ok)
        out = {"correct": ok}
        if ok or d.get("reveal"):
            out["answer"] = priv["blanks"][item]
        return JsonResponse(out)
    spec = priv["items"].get(item)
    if spec is None:
        raise Http404
    if num.startswith("U") and area == "frq" and assess.withheld(request, num):
        if given:
            Response.objects.create(user=request.user, topic=num, item=item, area=area, given=given,
                                    correct=bool(grading.check(given, spec["answer"])) if "answer" in spec else False)
            return JsonResponse({"saved": True})
        return JsonResponse({"error": "results not released yet"}, status=403)
    out = {}
    if given and "answer" in spec:
        ok = grading.check(given, spec["answer"])
        if ok is not None:
            Response.objects.create(user=request.user, topic=num, item=item, area=area, given=given, correct=ok)
        out["correct"] = ok
    if given or d.get("reveal"):
        out["solution"] = spec.get("solution", "")
        out["display"] = spec.get("answer", {}).get("display", "")
        if "rubric" in spec:
            out["rubric"] = spec["rubric"]
    return JsonResponse(out)


def _drafts(user, num):
    return {d.item: {"v": d.value, "r": d.revealed, "t": int(d.updated.timestamp() * 1000)}
            for d in Draft.objects.filter(user=user, topic=num)}


@login_required
@require_POST
@ratelimit("api-draft", "user", 300, 60, json=True)
def api_draft(request, num):
    """Save what is in one answer box (typed text, a picked choice, a shown answer) as the student works."""
    if not can_save(request.user, num):
        return JsonResponse({"error": "members only"}, status=403)
    d = _body(request)
    item = _str(d.get("item"), 40)
    if not item or not content.public(num):
        return JsonResponse({"error": "bad item"}, status=400)
    if not Draft.objects.filter(user=request.user, topic=num, item=item).exists() and \
            Draft.objects.filter(user=request.user, topic=num).count() >= 400:
        return JsonResponse({"error": "too many"}, status=400)
    defaults = {"value": _str(d.get("value"), 2000)}
    if d.get("revealed"):
        defaults["revealed"] = True
    Draft.objects.update_or_create(user=request.user, topic=num, item=item, defaults=defaults)
    return JsonResponse({"ok": True})


@login_required
@require_POST
@ratelimit("api-step", "user", 120, 60, json=True)
def api_step(request, num):
    if not can_save(request.user, num):
        return JsonResponse({'error': 'members only'}, status=403)
    d = _body(request)
    pub = content.public(num)
    step = _int(d.get("step"))
    if not pub or not (0 <= step < len(pub["steps"])):
        return JsonResponse({"error": "bad step"}, status=400)
    StepDone.objects.get_or_create(user=request.user, topic=num, step=step)
    return JsonResponse({"ok": True})


@login_required
@require_POST
@ratelimit("api-quiz", "user", 20, 60, json=True)
def api_quiz(request, num):
    if not can_save(request.user, num):
        return JsonResponse({'error': 'members only'}, status=403)
    d = _body(request)
    pub, priv = content.public(num), content.private(num)
    if not pub:
        raise Http404
    served_pub, info = assess.draw(request, num, pub)
    served = [it["id"] for it in served_pub["quiz"]]          # grade only what this taker was given
    cls = info["classroom"]
    from classwork.access import gate
    g = gate(request.user, "unittest" if num.startswith("U") else "quiz", num)
    if g["state"] in ("not_yet", "off", "paper"):
        return JsonResponse({"error": "not open"}, status=403)
    if g["state"] == "closed":
        return JsonResponse({"error": "closed"}, status=409)
    if cls is not None and g["attempts"] != "best" and QuizAttempt.objects.filter(user=request.user, topic=num, classroom=cls).exists():
        return JsonResponse({"error": "already submitted", "submitted": True}, status=409)
    answers = d.get("answers")
    if not isinstance(answers, dict):
        answers = {}
    detail, score = {}, 0
    for iid in served:
        spec = priv["items"][iid]
        given = _str(answers.get(iid), 300)
        ok = bool(grading.check(given, spec["answer"])) if given else False
        score += ok
        detail[iid] = {"given": given, "correct": ok, "solution": spec["solution"],
                       "display": spec["answer"].get("display", "")}
    a = QuizAttempt.objects.create(user=request.user, topic=num, score=score, total=len(served), served=served,
                                   classroom=cls, form=info["form"],
                                   detail={k: {"given": v["given"], "correct": v["correct"]} for k, v in detail.items()})
    if cls is not None:
        if assess.visible(request, num):
            return JsonResponse({"submitted": True, "released": True, **assess.result_payload(a, priv)})
        return JsonResponse({"submitted": True, "released": False})
    assess.new_draw(request, num)                             # the next attempt gets a fresh draw
    return JsonResponse({"score": score, "total": len(served), "detail": detail})


@login_required
@require_POST
@ratelimit("api-frq", "user", 120, 60, json=True)
def api_frq_score(request, num):
    if not can_save(request.user, num):
        return JsonResponse({'error': 'members only'}, status=403)
    if num.startswith("U") and assess.withheld(request, num):
        return JsonResponse({"error": "results not released yet"}, status=403)
    d = _body(request)
    priv = content.private(num)
    part = _str(d.get("part"), 40)
    spec = priv and priv["items"].get(part)
    if not spec or "rubric" not in spec:
        raise Http404
    possible = sum(r["points"] for r in spec["rubric"])
    earned = max(0, min(possible, _int(d.get("earned"), 0)))
    FRQScore.objects.update_or_create(user=request.user, part=part,
                                      defaults={"topic": num, "earned": earned, "possible": possible})
    return JsonResponse({"earned": earned, "possible": possible})


# ------------------------------------------------------------------ teacher
@never_cache
@teacher_required
def teacher(request):
    classes = Classroom.objects.filter(teacher=request.user).prefetch_related("enrollments__student__profile")
    have = sorted(content.available(), key=lambda n: [int(x) for x in n.split(".")])
    counts = {n: content.counts(n) for n in have}
    rosters = []
    for c in classes:
        students = [e.student for e in c.enrollments.all()]
        ids = [s.id for s in students]
        steps = {(r["user"], r["topic"]): r["n"] for r in
                 StepDone.objects.filter(user__in=ids).values("user", "topic").annotate(n=Count("id"))}
        prac = {(r["user"], r["topic"]): r["n"] for r in
                Response.objects.filter(user__in=ids, area="practice", correct=True)
                .values("user", "topic").annotate(n=Count("item", distinct=True))}
        quiz = {(r["user"], r["topic"]): r["best"] for r in
                QuizAttempt.objects.filter(user__in=ids).values("user", "topic").annotate(best=Max("score"))}
        frq = {(r["user"], r["topic"]): (r["e"], r["p"]) for r in
               FRQScore.objects.filter(user__in=ids).values("user", "topic").annotate(e=Sum("earned"), p=Sum("possible"))}
        rows = []
        for s in sorted(students, key=lambda s: s.profile.display_name.lower()):
            cells = []
            for n in have:
                k = (s.id, n)
                cells.append({"steps": steps.get(k, 0), "steps_total": counts[n]["steps"],
                              "practice": prac.get(k, 0), "practice_total": counts[n]["practice"],
                              "quiz": quiz.get(k), "quiz_total": counts[n]["quiz"],
                              "frq": frq.get(k)})
            rows.append({"id": s.id, "name": s.profile.display_name, "username": s.username, "cells": cells})
        assessments = []
        for n in have + [v["num"] for u in sorted(content.unit_tests()) for v in content.test_versions(u)]:
            got = QuizAttempt.objects.filter(classroom=c, topic=n)
            k = got.count()
            if not k:
                continue
            pub = content.public(n)
            nf = assess.n_forms(pub)
            assessments.append({"num": n, "submitted": got.values("user").distinct().count(), "of": len(students),
                                "form": assess.LETTERS[assess.class_form(c, n, nf)] if nf > 1 else "",
                                "released": assess.released(c, n)})
        rosters.append({"c": c, "rows": rows, "assessments": assessments})
    return render(request, "teacher/dashboard.html", {"rosters": rosters, "topics": have,
                                                      "temp_password": request.session.pop("temp_password", None)})


@teacher_required
@require_POST
def new_class(request):
    name = " ".join((request.POST.get("name") or "").split())[:80]
    course = request.POST.get("course", "AB")
    if name:
        Classroom.objects.create(name=name, teacher=request.user, course=course if course in ("AB", "BC") else "AB")
    return redirect("teacher")


@teacher_required
@require_POST
def toggle_class(request, pk):
    c = get_object_or_404(Classroom, pk=pk, teacher=request.user)
    c.open = not c.open
    c.save(update_fields=["open"])
    return redirect("teacher")


def set_theme(request, theme):
    from django.utils.http import url_has_allowed_host_and_scheme
    from .context import THEMES
    nxt = request.GET.get("next") or ""
    if not url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()}):
        nxt = "home"
    resp = redirect(nxt)
    if theme not in dict(THEMES):
        return resp
    resp.set_cookie("theme", theme, max_age=365 * 24 * 3600, samesite="Lax", path=settings.COOKIE_PATH,
                    secure=settings.SESSION_COOKIE_SECURE)
    return resp




# ------------------------------------------------------------------ transcripts (review before rendering)
def _transcripts():
    import glob, os, sys
    root = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    sys.path.insert(0, os.path.join(root, "tools"))
    from transcripts import PAUSE, WPM, parse, pause_seconds
    out = []
    files = glob.glob(os.path.join(root, "transcripts", "[0-9]*_*.md"))
    for f in sorted(files, key=lambda p: [int(x) for x in os.path.basename(p)[:-3].split("_")]):
        title, beats = parse(f)
        words = sum(len(PAUSE.sub("", " ".join(b["say"])).split()) for b in beats)
        out.append({"num": os.path.basename(f)[:-3].replace("_", "."), "title": title, "beats": beats,
                    "minutes": round(words / WPM + (2.5 * len(beats) + pause_seconds(beats)) / 60, 1)})
    return out


@teacher_required
def transcripts(request):
    items = _transcripts()
    pick = request.GET.get("t")
    cur = next((t for t in items if t["num"] == pick), None)
    return render(request, "teacher/transcripts.html", {"items": items, "cur": cur,
                                                        "total": round(sum(t["minutes"] for t in items))})


@teacher_required
@require_POST
def release(request, pk, num):
    """Release (or take back) a quiz or unit test's scores and solutions for one class."""
    c = get_object_or_404(Classroom, pk=pk, teacher=request.user)
    r = Release.objects.filter(classroom=c, topic=num)
    if r.exists():
        r.delete()
    else:
        Release.objects.create(classroom=c, topic=num)
    return redirect("teacher")


def _back_to_class(request, pk):
    """After a roster action: back to the class page it came from (classwork's Students tab), else the dashboard."""
    nxt = request.POST.get("next", "")
    return nxt if nxt.startswith(f"/teacher/class/{pk}/") or nxt.startswith(f"{request.META.get('SCRIPT_NAME', '')}/teacher/class/{pk}/") else "teacher"


def _class_student(request, pk, uid):
    """A student enrolled in one of this teacher's classes, or 404. Never another teacher or an admin."""
    c = get_object_or_404(Classroom, pk=pk, teacher=request.user)
    e = get_object_or_404(Enrollment.objects.select_related("student__profile"), classroom=c, student_id=uid)
    s = e.student
    if s.is_staff or s.is_superuser or is_teacher(s):
        raise Http404
    return c, e, s


TEMP_ALPHABET = "abcdefghjkmnpqrstuvwxyz23456789"


@teacher_required
@require_POST
@ratelimit("teacher-reset", "user", 60, 3600)
def reset_student_password(request, pk, uid):
    """For a student who forgot their password and has no confirmed email. The new password is shown to the
    teacher once; the student signs in with it and can change it in Account settings."""
    import secrets
    c, e, s = _class_student(request, pk, uid)
    pw = "-".join("".join(secrets.choice(TEMP_ALPHABET) for _ in range(4)) for _ in range(3))
    s.set_password(pw)
    s.save(update_fields=["password"])
    request.session["temp_password"] = {"name": s.profile.display_name, "username": s.username, "password": pw}
    return redirect(_back_to_class(request, pk))


@teacher_required
@require_POST
def remove_student(request, pk, uid):
    """Take a student out of a class. Their account and their own work stay theirs."""
    c, e, s = _class_student(request, pk, uid)
    e.delete()
    messages.success(request, f"{s.profile.display_name} is no longer in {c.name}.")
    return redirect(_back_to_class(request, pk))


# ------------------------------------------------------------------ video with HTTP Range (seeking)
_RANGE = re.compile(r"bytes=(\d*)-(\d*)")
_VIDEO_TYPES = {".mp4": "video/mp4", ".vtt": "text/vtt"}


def video(request, name):
    """Serve a lesson video or caption file with Range support. Django's static view ignores Range, and without
    206 responses browsers (Brave, Chrome) can't seek: the scrubber snaps back to where playback was."""
    path = (settings.VIDEO_DIR / name).resolve()
    ext = path.suffix
    if ext not in _VIDEO_TYPES or path.parent != settings.VIDEO_DIR.resolve() or not path.is_file():
        raise Http404
    resp = _ranged(request, path, _VIDEO_TYPES[ext])
    resp["Cache-Control"] = "public, max-age=86400"       # lesson videos are public (the free preview)
    return resp


def _ranged(request, path, content_type):
    """A file answered with HTTP Range support (206 partial content), so a <video> can seek."""
    size = path.stat().st_size
    m = _RANGE.fullmatch(request.headers.get("Range", "").strip())
    if not m or (not m[1] and not m[2]):
        resp = FileResponse(open(path, "rb"), content_type=content_type)
        resp["Accept-Ranges"] = "bytes"
        resp["Content-Length"] = str(size)
        return resp
    if m[1]:
        start, end = int(m[1]), min(int(m[2]) if m[2] else size - 1, size - 1)
    else:                                   # suffix range: last N bytes
        start, end = max(size - int(m[2]), 0), size - 1
    if start > end or start >= size:
        resp = HttpResponse(status=416)
        resp["Content-Range"] = f"bytes */{size}"
        return resp
    with open(path, "rb") as f:
        f.seek(start)
        data = f.read(end - start + 1)
    resp = HttpResponse(data, status=206, content_type=content_type)
    resp["Content-Range"] = f"bytes {start}-{end}/{size}"
    resp["Accept-Ranges"] = "bytes"
    resp["Content-Length"] = str(len(data))
    return resp


# ------------------------------------------------------------------ printable unit tests (solo students)
PDF_DIR = settings.PDF_DIR


def _paper_forms(num):
    return sorted(p.name.split("-form")[1][0] for p in (PDF_DIR / num).glob(f"{num}-unittest-form?-classic.pdf"))


def test_pdf(request, num, form, kind):
    """A paper form of a unit test, or its solutions manual. Class students never get the manual from here:
    their teacher decides when solutions come out."""
    if not (request.user.is_authenticated and can_open(request.user, num)):
        return forbidden(request, "Printable copies are free for Units 1 to 3 with a free account, and for members everywhere.")
    if kind == "key" and class_for(request.user) is not None:
        return forbidden(request, "Your teacher releases the solutions for your class.")
    name = f"{num}-unittest-form{form}{'-key' if kind == 'key' else ''}-classic.pdf"
    path = PDF_DIR / num / name
    if not path.is_file():
        raise Http404
    return FileResponse(open(path, "rb"), content_type="application/pdf", filename=name)


# ------------------------------------------------------------------ teacher handouts: every printable PDF in one place
_KINDS = [("packet", "Packet"), ("packetcompact", "Compact packet (trial)"), ("notes", "Guided notes"), ("practice", "Practice"), ("quiz-formA", "Quiz A"),
          ("quiz-formB", "Quiz B"), ("quiz-formC", "Quiz C"), ("testprep", "AP test prep"), ("unittest-formA", "Unit test A"), ("unittest-formB", "Unit test B"),
          ("unittest-formC", "Unit test C")]


def _handout_rows(num, title, course=""):
    d = PDF_DIR / num
    docs = []
    for kind, label in _KINDS:
        student, key = f"{num}-{kind}-classic.pdf", f"{num}-{kind}-key-classic.pdf"
        if (d / student).is_file():
            docs.append({"label": label, "student": reverse("handout_pdf", args=[num, student]),
                         "key": reverse("handout_pdf", args=[num, key]) if (d / key).is_file() else None})
    deck = reverse("slides", args=[num]) if not num.startswith("U") and slides.manifest(num) else None
    return {"num": num, "title": title, "docs": docs, "slides": deck, "course": course}


@teacher_required
def handouts(request):
    units = []
    tests = content.unit_tests()
    for u in content.syllabus():
        rows = [_handout_rows(t["n"], t["title"]) for t in u["topics"]]
        rows = [r for r in rows if r["docs"] or r["slides"]]
        # the unit test, or both versions of it for Units 6-8 (AB without the BC-only topics, BC the whole unit)
        test_rows = [_handout_rows(v["num"], f"Unit test, {v['course']} version" if v["course"] else "Unit test", v["course"])
                     for v in content.test_versions(u["n"])] if u["n"] in tests else []
        test_rows = [r for r in test_rows if r["docs"]]
        if rows or test_rows:
            units.append({"n": u["n"], "title": u["title"], "heading": u["heading"], "rows": rows, "tests": test_rows})
    lookup = None
    if request.GET.get("packet"):
        lookup = {"code": request.GET["packet"].strip()[:20], "found": _find_packet(request.user, request.GET["packet"])}
    return render(request, "teacher/handouts.html", {"units": units, "lookup": lookup})


def _find_packet(teacher, raw):
    """A packet a student in one of this teacher's classes (or the teacher) printed, by its ID, or None."""
    code = re.sub(r"[^A-Z0-9]", "", raw.upper())
    if len(code) != 8:
        return None
    p = IssuedPacket.objects.select_related("user__profile").filter(code=f"{code[:4]}-{code[4:]}").first()
    if p is None:
        return None
    if p.user != teacher and not p.user.enrollments.filter(classroom__teacher=teacher).exists():
        return None
    return {"code": p.code, "topic": p.topic, "created": p.created, "username": p.user.get_username(),
            "name": packets.holder_name(p.user)}


@teacher_required
def handout_pdf(request, num, name):
    path = (PDF_DIR / num / name).resolve()
    if path.parent != (PDF_DIR / num).resolve() or path.suffix != ".pdf" or not path.is_file():
        raise Http404
    # a teacher's copy says who printed it too (Adder, 2026-10-02); the Name line stays for the student
    p = packets.issue(request.user, num)
    data = packets.stamp(path, packets.holder_name(request.user), p.code, what="")
    resp = HttpResponse(data, content_type="application/pdf")
    resp["Content-Disposition"] = f'inline; filename="{name[:-4]}-{p.code}.pdf"'
    return resp


# ------------------------------------------------------------------ personalized packets
@login_required
@require_POST
def packet(request, num):
    """The topic's lesson, practice and AP test prep as one PDF, stamped on every page with who it was printed for
    and a packet ID that is recorded, so a leaked copy can be traced. Teachers print from Handouts, stamped with
    their own name."""
    if not (request.user.is_authenticated and can_open(request.user, num)):
        return forbidden(request, "Printable copies are free for Units 1 to 3 with a free account, and for members everywhere.")
    if not packets.available(num):
        raise Http404
    p = packets.issue(request.user, num)
    data = packets.stamp(packets.base_path(num), packets.holder_name(request.user), p.code)
    resp = HttpResponse(data, content_type="application/pdf")
    resp["Content-Disposition"] = f'attachment; filename="{num}-packet-{p.code}.pdf"'
    return resp


# ------------------------------------------------------------------ full-length practice exams
def _exam_or_404(slug):
    pub = exams.public(slug)
    if not pub:
        raise Http404("That exam isn't available.")
    return pub


def exam_list(request):
    rows = []
    for slug in exams.available():
        pub = exams.public(slug)
        rows.append({"slug": slug, "title": pub["title"], "course": pub["course"], "members_only": pub["members_only"], "outline": exams.outline(pub),
                     "open": exams.can_take(request.user, pub) if request.user.is_authenticated else not pub["members_only"]})
    free = sorted({r["course"] for r in rows if not r["members_only"]})
    note = (f"The {' and '.join(free)} exam{'s are' if len(free) > 1 else ' is'} open to any account." if free else "")
    return render(request, "course/exams.html", {"exams": rows, "free_note": note})


def exam_home(request, slug):
    """An exam's front page: what it is, start or resume, earlier sittings, and the print copies."""
    pub = _exam_or_404(slug)
    if not request.user.is_authenticated:
        return redirect(f"{reverse('login')}?next={request.path}")
    if not exams.can_take(request.user, pub):
        return render(request, "course/locked.html", {"what": "More practice exams"})
    attempts = list(ExamAttempt.objects.filter(user=request.user, exam=slug))
    for a in attempts:
        exams.sync(a, pub)
    past = [{"id": a.pk, "started": a.started, "summary": exams.summary(a, pub)} for a in attempts if a.finished]
    live = next((a for a in attempts if not a.finished), None)
    return render(request, "course/exam_home.html", {
        "E": pub, "slug": slug, "live": live, "past": past, "outline": exams.outline(pub),
        "live_part": live and exams.parts(pub)[live.part],
        "print_ready": {k: (PDF_DIR / f"exam-{slug}" / f"exam-{slug}-exam{'-key' if k == 'key' else ''}-classic.pdf").is_file() for k in ("exam", "key")}})


@login_required
@require_POST
@ratelimit("exam-start", "user", 30, 3600)
def exam_start(request, slug):
    pub = _exam_or_404(slug)
    if not exams.can_take(request.user, pub):
        return forbidden(request, "This is for members: students in a class, teachers, and anyone with full access.")
    live = next((a for a in ExamAttempt.objects.filter(user=request.user, exam=slug, finished__isnull=True)
                 if not exams.sync(a, pub).finished), None)
    if live is None:
        live = ExamAttempt.objects.create(user=request.user, exam=slug)
    return redirect("exam_attempt", slug=slug, pk=live.pk)


@login_required
@require_POST
def exam_discard(request, slug, pk):
    """Throw away an unfinished sitting, so the next one starts from Part A."""
    ExamAttempt.objects.filter(user=request.user, exam=slug, pk=pk, finished__isnull=True).delete()
    return redirect("exam_home", slug=slug)


def _attempt(request, slug, pk):
    pub = _exam_or_404(slug)
    att = get_object_or_404(ExamAttempt, pk=pk, exam=slug, user=request.user)
    return pub, exams.sync(att, pub)


@login_required
def exam_attempt(request, slug, pk):
    pub, att = _attempt(request, slug, pk)
    data = exams.report(att, pub) if att.finished else exams.live_state(att, pub)
    return render(request, "course/exam.html", {"E": pub, "slug": slug, "att": att, "data": data,
                                                "meta": {k: pub[k] for k in ("slug", "title", "course")}})


@login_required
@require_POST
@ratelimit("api-exam", "user", 300, 60, json=True)
def api_exam(request, slug, pk, action):
    """The sitting's actions. Every reply carries the fresh state, so the page follows the server, never its own clock."""
    pub, att = _attempt(request, slug, pk)
    d = _body(request)
    ok, status, extra = True, 200, {}
    if action == "begin":
        exams.begin(att, pub)
    elif action == "submit":
        ok = exams.submit_part(att, pub, _str(d.get("part"), 40))
    elif action == "answer":
        ok, why = exams.answer(att, pub, _str(d.get("item"), 40), _str(d.get("value"), 300))
        extra["reason"] = why
    elif action == "flag":
        ok = exams.flag(att, pub, _str(d.get("item"), 40), bool(d.get("on")))
    elif action == "frq":
        ok = exams.set_frq(att, pub, _str(d.get("part"), 40), d.get("checks"))
        if ok:
            extra.update({"summary": exams.summary(att, pub), "units": exams.by_unit(att, pub)})
    elif action != "state":
        raise Http404
    if not ok:
        status = 409
    if action != "frq":
        extra["state"] = {"finished": True} if att.finished else exams.live_state(att, pub)
    return JsonResponse({"ok": ok, **extra}, status=status)


def exam_pdf(request, slug, kind):
    """The printable exam, or its key with every solution and scoring guide. Same access as the exam itself."""
    pub = _exam_or_404(slug)
    if not request.user.is_authenticated:
        return redirect(f"{reverse('login')}?next={request.path}")
    if not exams.can_take(request.user, pub):
        return forbidden(request, "This is for members: students in a class, teachers, and anyone with full access.")
    name = f"exam-{slug}-exam{'-key' if kind == 'key' else ''}-classic.pdf"
    path = PDF_DIR / f"exam-{slug}" / name
    if not path.is_file():
        raise Http404
    return FileResponse(open(path, "rb"), content_type="application/pdf", filename=name)


# ------------------------------------------------------------------ teacher slide decks (tools/build_slides.py)
def _is_teacher(user):
    p = getattr(user, "profile", None) if user.is_authenticated else None
    return bool(p and p.is_teacher)


def _csp_ready(page, nonce):
    """Built decks carry an inline <script> and an onload= attribute, which the site's Content-Security-Policy
    blocks. Give inline scripts this response's nonce, and run the typeset hook on DOMContentLoaded instead (deferred
    scripts, KaTeX included, have all run by then). Done here so decks built before the policy work unchanged."""
    page = page.replace("<script>", f'<script nonce="{nonce}">')
    if ' onload="window.deckTypeset()"' in page:
        page = page.replace(' onload="window.deckTypeset()"', "")
        hook = (f'<script nonce="{nonce}">document.addEventListener("DOMContentLoaded", () => '
                '{ if (window.deckTypeset) window.deckTypeset(); });</script>\n')
        page = page.replace("</body>", hook + "</body>", 1)
    return page


def slides_page(request, num):
    """A topic's slide decks: present either version in the browser, or download it for PowerPoint."""
    if not _is_teacher(request.user):
        return forbidden(request)
    m = slides.manifest(num)
    if m is None:
        raise Http404("This topic has no slides yet.")
    unit, meta = content.topic_meta(num)
    versions = []
    for key, label in slides.VERSIONS:
        v = m["versions"].get(key)
        if not v:
            continue
        versions.append({"key": key, "label": label, "slides": v["slides"],
                         "html": reverse("slides_file", args=[num, v["html"]]),
                         "pptx": reverse("slides_file", args=[num, v["pptx"]]) if v.get("pptx") else None})
    return render(request, "teacher/slides.html", {"num": num, "title": (meta or {}).get("title") or m.get("title", ""),
                                                   "versions": versions})


def slides_file(request, num, name):
    """A deck, its PowerPoint file, or one of its stills. Teachers only, whatever the file."""
    if not _is_teacher(request.user):
        return forbidden(request)
    path = slides.path_for(num, name)
    if path is None:
        raise Http404
    ext = path.suffix
    if ext == ".html":
        # the deck opens in the look the teacher picked on the site
        page = path.read_text()
        theme = request.COOKIES.get("theme", "")
        if theme in dict(THEMES):
            page = page.replace('<html lang="en">', f'<html lang="en" data-theme="{theme}">', 1)
        page = _csp_ready(page, getattr(request, "csp_nonce", ""))
        resp = HttpResponse(page, content_type=slides.TYPES[ext])
        resp["Cache-Control"] = "private, no-cache"
        return resp
    if settings.SLIDES_ACCEL:
        resp = HttpResponse(content_type=slides.TYPES[ext])
        resp["X-Accel-Redirect"] = f"{settings.SLIDES_ACCEL.rstrip('/')}/{num}/{name}"
    else:
        resp = FileResponse(open(path, "rb"), content_type=slides.TYPES[ext])
    if ext == ".pptx":
        resp["Content-Disposition"] = f'attachment; filename="{path.name}"'
    resp["Cache-Control"] = "private, max-age=3600"
    return resp
