import json
import re

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max, Q, Sum
from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse, HttpResponseForbidden, JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.models import Classroom, class_for, has_full_access
from . import content, grading
from . import assess, packets
from .models import Draft, FRQScore, IssuedPacket, QuizAttempt, Release, Response, StepDone

AREAS = ("notes", "practice", "quiz", "testprep")
FREE_PRACTICE = 4          # practice problems anyone can try without an account


def _free_ids(pub):
    return {it["id"] for it in pub["practice"][:FREE_PRACTICE]}


def _preview(pub):
    """What a visitor without full access receives: the video(s) and the first few practice problems. Nothing else
    leaves the server, so the paywall can't be bypassed from the page source."""
    videos = [b for st in pub["steps"] for b in st["blocks"] if b["type"] == "video"]
    return {**pub, "steps": [{"title": "Video", "blocks": videos}] if videos else [],
            "practice": pub["practice"][:FREE_PRACTICE], "quiz": [], "mcq": [], "frq": [], "preview": True}


def _lesson(num):
    pub = content.public(num)
    if not pub:
        raise Http404("That lesson isn't written yet.")
    unit, meta = content.topic_meta(num)
    prev, nxt = content.neighbours(num)
    return pub, unit, prev, nxt


def home(request):
    if request.user.is_authenticated and request.user.profile.is_teacher:
        return redirect("teacher")
    return course_map(request)


def course_map(request):
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
        tests = content.unit_tests()
        best_u = best.get(f"U{u['n']}")
        units.append({**u, "topics": topics, "test": u["n"] in tests, "test_num": f"U{u['n']}", "test_best": best_u})
    return render(request, "course/map.html", {"units": units, "current_unit": _current_unit(request.user)})


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
    try:
        return int(topic.lstrip("U").split(".")[0])
    except ValueError:
        return 1


def unit_test(request, num):
    if not has_full_access(request.user):
        return render(request, "course/locked.html", {"what": "Unit tests"})
    pub = content.public(num)
    if not pub:
        raise Http404("That unit test isn't written yet.")
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
    return render(request, "course/unittest.html", {"L": pub, "num": num, "lesson_json": pub, "state_json": state})


def lesson(request, num, area="notes"):
    if area not in AREAS:
        raise Http404
    pub, unit, prev, nxt = _lesson(num)
    pub = assess.strip(pub)
    full = has_full_access(request.user)
    if not full:
        pub = _preview(pub)
        state = {"steps_done": [], "correct": [], "frq": {}, "quiz": [], "full": False}
        return render(request, f"course/{area}.html", {
            "L": pub, "unit": unit, "num": num, "area": area, "prev": prev, "next": nxt,
            "lesson_json": pub, "state_json": state, "packet": False})
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
    return render(request, f"course/{area}.html", {
        "L": pub, "unit": unit, "num": num, "area": area, "prev": prev, "next": nxt,
        "lesson_json": pub, "state_json": state, "packet": packets.available(num),
    })


# ------------------------------------------------------------------ JSON API
def _body(request):
    try:
        return json.loads(request.body or b"{}")
    except ValueError:
        return {}


@require_POST
def api_check(request, num):
    """Check one answer. Returns correctness plus the solution once it has been tried.
    Visitors without full access may check only the free practice problems, and nothing is saved for them."""
    d = _body(request)
    priv = content.private(num)
    if not priv:
        raise Http404
    item, given, area = d.get("item", ""), (d.get("given") or "")[:300], d.get("area", "notes")
    if not has_full_access(request.user):
        pub = content.public(num)
        if num.startswith("U") or item not in _free_ids(pub):
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
        if "why_not" in spec and given in spec["why_not"]:
            out["why_not"] = spec["why_not"][given]
        if "rubric" in spec:
            out["rubric"] = spec["rubric"]
    return JsonResponse(out)


def _drafts(user, num):
    return {d.item: {"v": d.value, "r": d.revealed, "t": int(d.updated.timestamp() * 1000)}
            for d in Draft.objects.filter(user=user, topic=num)}


@login_required
@require_POST
def api_draft(request, num):
    """Save what is in one answer box (typed text, a picked choice, a shown answer) as the student works."""
    if not has_full_access(request.user):
        return JsonResponse({"error": "members only"}, status=403)
    d = _body(request)
    item = str(d.get("item", ""))[:40]
    if not item or not content.public(num):
        return JsonResponse({"error": "bad item"}, status=400)
    if not Draft.objects.filter(user=request.user, topic=num, item=item).exists() and \
            Draft.objects.filter(user=request.user, topic=num).count() >= 400:
        return JsonResponse({"error": "too many"}, status=400)
    defaults = {"value": str(d.get("value", ""))[:2000]}
    if d.get("revealed"):
        defaults["revealed"] = True
    Draft.objects.update_or_create(user=request.user, topic=num, item=item, defaults=defaults)
    return JsonResponse({"ok": True})


@login_required
@require_POST
def api_step(request, num):
    if not has_full_access(request.user):
        return JsonResponse({'error': 'members only'}, status=403)
    d = _body(request)
    pub = content.public(num)
    step = int(d.get("step", -1))
    if not pub or not (0 <= step < len(pub["steps"])):
        return JsonResponse({"error": "bad step"}, status=400)
    StepDone.objects.get_or_create(user=request.user, topic=num, step=step)
    return JsonResponse({"ok": True})


@login_required
@require_POST
def api_quiz(request, num):
    if not has_full_access(request.user):
        return JsonResponse({'error': 'members only'}, status=403)
    d = _body(request)
    pub, priv = content.public(num), content.private(num)
    if not pub:
        raise Http404
    served_pub, info = assess.draw(request, num, pub)
    served = [it["id"] for it in served_pub["quiz"]]          # grade only what this taker was given
    cls = info["classroom"]
    if cls is not None and QuizAttempt.objects.filter(user=request.user, topic=num, classroom=cls).exists():
        return JsonResponse({"error": "already submitted", "submitted": True}, status=409)
    answers = d.get("answers", {})
    detail, score = {}, 0
    for iid in served:
        spec = priv["items"][iid]
        given = (answers.get(iid) or "")[:300]
        ok = bool(grading.check(given, spec["answer"])) if given else False
        score += ok
        detail[iid] = {"given": given, "correct": ok, "solution": spec["solution"],
                       "display": spec["answer"].get("display", "")}
    a = QuizAttempt.objects.create(user=request.user, topic=num, score=score, total=len(served), served=served,
                                   classroom=cls, form=info["form"],
                                   detail={k: {"given": v["given"], "correct": v["correct"]} for k, v in detail.items()})
    if cls is not None:
        if assess.released(cls, num):
            return JsonResponse({"submitted": True, "released": True, **assess.result_payload(a, priv)})
        return JsonResponse({"submitted": True, "released": False})
    assess.new_draw(request, num)                             # the next attempt gets a fresh draw
    return JsonResponse({"score": score, "total": len(served), "detail": detail})


@login_required
@require_POST
def api_frq_score(request, num):
    if not has_full_access(request.user):
        return JsonResponse({'error': 'members only'}, status=403)
    if num.startswith("U") and assess.withheld(request, num):
        return JsonResponse({"error": "results not released yet"}, status=403)
    d = _body(request)
    priv = content.private(num)
    spec = priv and priv["items"].get(d.get("part", ""))
    if not spec or "rubric" not in spec:
        raise Http404
    possible = sum(r["points"] for r in spec["rubric"])
    earned = max(0, min(possible, int(d.get("earned", 0))))
    FRQScore.objects.update_or_create(user=request.user, part=d["part"],
                                      defaults={"topic": num, "earned": earned, "possible": possible})
    return JsonResponse({"earned": earned, "possible": possible})


# ------------------------------------------------------------------ teacher
@login_required
def teacher(request):
    if not request.user.profile.is_teacher:
        return HttpResponseForbidden("Teachers only.")
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
            rows.append({"name": s.profile.display_name, "cells": cells})
        assessments = []
        for n in have + [f"U{u}" for u in sorted(content.unit_tests())]:
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
    return render(request, "teacher/dashboard.html", {"rosters": rosters, "topics": have})


@login_required
@require_POST
def new_class(request):
    if not request.user.profile.is_teacher:
        return HttpResponseForbidden()
    name = (request.POST.get("name") or "").strip()[:80]
    if name:
        Classroom.objects.create(name=name, teacher=request.user, course=request.POST.get("course", "AB")[:2])
    return redirect("teacher")


@login_required
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
    resp.set_cookie("theme", theme, max_age=365 * 24 * 3600, samesite="Lax")
    return resp


def set_design(request, design):
    from django.utils.http import url_has_allowed_host_and_scheme
    from .context import DESIGNS
    nxt = request.GET.get("next") or ""
    if not url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()}):
        nxt = "home"
    resp = redirect(nxt)
    if design in dict(DESIGNS):
        resp.set_cookie("design", design, max_age=365 * 24 * 3600, samesite="Lax")
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


@login_required
def transcripts(request):
    if not request.user.profile.is_teacher:
        return HttpResponseForbidden("Teachers only.")
    items = _transcripts()
    pick = request.GET.get("t")
    cur = next((t for t in items if t["num"] == pick), None)
    return render(request, "teacher/transcripts.html", {"items": items, "cur": cur,
                                                        "total": round(sum(t["minutes"] for t in items))})


@login_required
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


# ------------------------------------------------------------------ video with HTTP Range (seeking)
_RANGE = re.compile(r"bytes=(\d*)-(\d*)")
_VIDEO_TYPES = {".mp4": "video/mp4", ".vtt": "text/vtt"}


def video(request, name):
    """Serve a lesson video or caption file with Range support. Django's static view ignores Range, and without
    206 responses browsers (Brave, Chrome) can't seek: the scrubber snaps back to where playback was."""
    path = (settings.BASE_DIR / "static" / "video" / name).resolve()
    ext = path.suffix
    if ext not in _VIDEO_TYPES or path.parent != (settings.BASE_DIR / "static" / "video").resolve() or not path.is_file():
        raise Http404
    size = path.stat().st_size
    m = _RANGE.fullmatch(request.headers.get("Range", "").strip())
    if not m or (not m[1] and not m[2]):
        resp = FileResponse(open(path, "rb"), content_type=_VIDEO_TYPES[ext])
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
    resp = HttpResponse(data, status=206, content_type=_VIDEO_TYPES[ext])
    resp["Content-Range"] = f"bytes {start}-{end}/{size}"
    resp["Accept-Ranges"] = "bytes"
    resp["Content-Length"] = str(len(data))
    return resp


# ------------------------------------------------------------------ printable unit tests (solo students)
PDF_DIR = settings.BASE_DIR.parent / "build" / "pdf"


def _paper_forms(num):
    return sorted(p.name.split("-form")[1][0] for p in (PDF_DIR / num).glob(f"{num}-unittest-form?-classic.pdf"))


def test_pdf(request, num, form, kind):
    """A paper form of a unit test, or its solutions manual. Class students never get the manual from here:
    their teacher decides when solutions come out."""
    if not has_full_access(request.user):
        return HttpResponseForbidden("Members only.")
    if kind == "key" and class_for(request.user) is not None:
        return HttpResponseForbidden("Your teacher releases the solutions for your class.")
    name = f"{num}-unittest-form{form}{'-key' if kind == 'key' else ''}-classic.pdf"
    path = PDF_DIR / num / name
    if not path.is_file():
        raise Http404
    return FileResponse(open(path, "rb"), content_type="application/pdf", filename=name)


# ------------------------------------------------------------------ teacher handouts: every printable PDF in one place
_KINDS = [("packet", "Packet"), ("packetcompact", "Compact packet (trial)"), ("notes", "Guided notes"), ("practice", "Practice"), ("quiz-formA", "Quiz A"),
          ("quiz-formB", "Quiz B"), ("quiz-formC", "Quiz C"), ("testprep", "AP test prep"), ("unittest-formA", "Unit test A"), ("unittest-formB", "Unit test B"),
          ("unittest-formC", "Unit test C")]


def _handout_rows(num, title):
    d = PDF_DIR / num
    docs = []
    for kind, label in _KINDS:
        student, key = f"{num}-{kind}-classic.pdf", f"{num}-{kind}-key-classic.pdf"
        if (d / student).is_file():
            docs.append({"label": label, "student": reverse("handout_pdf", args=[num, student]),
                         "key": reverse("handout_pdf", args=[num, key]) if (d / key).is_file() else None})
    return {"num": num, "title": title, "docs": docs}


def handouts(request):
    if not (request.user.is_authenticated and request.user.profile.is_teacher):
        return HttpResponseForbidden("Teachers only.")
    units = []
    tests = content.unit_tests()
    for u in content.syllabus():
        rows = [_handout_rows(t["n"], t["title"]) for t in u["topics"]]
        rows = [r for r in rows if r["docs"]]
        test = _handout_rows(f"U{u['n']}", "Unit test") if u["n"] in tests else None
        if rows or (test and test["docs"]):
            units.append({"n": u["n"], "title": u["title"], "rows": rows, "test": test})
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


def handout_pdf(request, num, name):
    if not (request.user.is_authenticated and request.user.profile.is_teacher):
        return HttpResponseForbidden("Teachers only.")
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
    if not has_full_access(request.user):
        return HttpResponseForbidden("Members only.")
    if not packets.available(num):
        raise Http404
    p = packets.issue(request.user, num)
    data = packets.stamp(packets.base_path(num), packets.holder_name(request.user), p.code)
    resp = HttpResponse(data, content_type="application/pdf")
    resp["Content-Disposition"] = f'attachment; filename="{num}-packet-{p.code}.pdf"'
    return resp
