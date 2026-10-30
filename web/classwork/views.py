"""The teacher's class pages: setup, calendar, progress, students, quizzes and tests, gradebook."""
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from accounts.models import Classroom
from accounts.permissions import teacher_required

from . import setup as S
from .models import Setup


def own_class(request, pk):
    return get_object_or_404(Classroom, pk=pk, teacher=request.user)


def _row(kind, values):
    """One row of the setup table: each column's choices, with the current value marked."""
    cols = {}
    for field in ("where", "opens", "dates", "record", "results"):
        opts = S.CHOICES[kind].get(field)
        cur = values.get(field)
        if opts is None:
            cols[field] = {"fixed": dict(_FIXED_LABELS).get((kind, field), "")}
        else:
            cols[field] = {"name": f"{kind}.{field}", "options": [{"v": v, "label": l, "on": v == cur} for v, l in opts]}
    details = [{"label": S.DETAIL_LABELS[f], "name": f"{kind}.{f}",
                "options": [{"v": v, "label": l, "on": v == values.get(f)} for v, l in S.CHOICES[kind][f]]}
               for f in S.DETAIL.get(kind, [])]
    return {"kind": kind, "name": S.NAMES[kind], "blurb": S.BLURBS[kind], "off": values.get("where") == "off",
            "cols": [cols[f] for f in ("where", "opens", "dates", "record", "results")], "details": details}


_FIXED_LABELS = [(("practice", "record"), "Done or not, never right or wrong"), (("testprep", "dates"), "None"),
                 (("testprep", "results"), "Right away"), (("notes", "results"), "–")]

SHOW_LABELS = [("grade", "Their grade in the course, with your weights"), ("due_dates", "Due dates, on their course page"),
               ("unopened", "Lessons that haven't opened yet (titles only)"), ("behind", 'A "behind" note when they miss a due date')]
WATCH_LABELS = [("missing", "Missing and late work"), ("hard_questions", "Quiz questions half the class or more missed"),
                ("sliding", "Students whose last two quizzes are under 60%")]


@never_cache
@teacher_required
def setup_page(request, pk):
    c = own_class(request, pk)
    s = S.class_setup(c)
    if request.method == "POST":
        s = Setup.objects.filter(classroom=c).first() or Setup(classroom=c)
        tpl = request.POST.get("apply_template")
        if tpl in S.TEMPLATES:
            s.kinds, s.template = S.template_kinds(tpl), tpl
        else:
            s.kinds = {k: S.clean(k, {f.split(".", 1)[1]: v for f, v in request.POST.items() if f.startswith(k + ".")})
                       for k in S.KINDS}
            s.show = {k: f"show.{k}" in request.POST for k, _ in SHOW_LABELS}
            days = request.POST.get("watch.inactive_days", "").strip()
            s.watch = {**{k: f"watch.{k}" in request.POST for k, _ in WATCH_LABELS},
                       "inactive_days": int(days) if days.isdigit() and "watch.inactive" in request.POST else 0}
            s.template = ""
        s.save()
        return redirect("cw_setup", pk=c.pk)
    current = {k: S.settings_for(c, k) for k in S.KINDS}
    show, watch = S.show(c), S.watch(c)
    return render(request, "classwork/setup.html", {
        "c": c, "tab": "setup", "rows": [_row(k, current[k]) for k in S.KINDS],
        "templates": [(k, v[0]) for k, v in S.TEMPLATES.items()], "template": s.template,
        "show": [{"k": k, "label": l, "on": show[k]} for k, l in SHOW_LABELS],
        "watch": [{"k": k, "label": l, "on": watch[k]} for k, l in WATCH_LABELS],
        "inactive_days": watch["inactive_days"],
        "units_apart": sorted(s.units) if s.pk else [],
    })


# ------------------------------------------------------------------ calendar
import datetime as dt  # noqa: E402

from django.contrib import messages  # noqa: E402

from course import content  # noqa: E402

from . import calendar as cal  # noqa: E402
from .models import Dated, NoSchool, StudentException  # noqa: E402


def _date(v):
    try:
        return dt.date.fromisoformat((v or "").strip())
    except ValueError:
        return None


def _local(c, v):
    """An aware datetime from a datetime-local input in the class's time zone, or None."""
    try:
        return dt.datetime.fromisoformat((v or "").strip()).replace(tzinfo=cal.zone(c))
    except ValueError:
        return None


def _field(c, moment):
    return moment.astimezone(cal.zone(c)).strftime("%Y-%m-%dT%H:%M") if moment else ""


def _students(c):
    return sorted((e.student for e in c.enrollments.select_related("student__profile")),
                  key=lambda u: u.profile.display_name.lower())


def _refs(c):
    """Everything this class could put on its calendar, for the "add a date" menu."""
    out = []
    for u in content.syllabus():
        for num in cal.unit_topics(u["n"], c.course):
            out.append((num, content.label(num)))
    tests = [(t["num"], content.test_label(t["num"])) for n in sorted(content.unit_tests())
             for t in [content.pick_test(n, c.course)] if t]
    return out, tests


@never_cache
@teacher_required
def calendar_page(request, pk):
    c = own_class(request, pk)
    if request.method == "POST":
        return _calendar_post(request, c)
    today = cal.local_day(c, dt.datetime.now(dt.timezone.utc))
    start = _date(request.GET.get("start")) or today
    start -= dt.timedelta(days=start.weekday())
    weeks = 3
    last = start + dt.timedelta(days=7 * weeks - 1)
    ev = cal.events(c, start, last)
    skips = {n.day: n for n in NoSchool.objects.filter(classroom=c, day__range=(start, last))}
    days = cal.class_days(c)
    cols = sorted(set(days) | {d.weekday() for d in ev})
    grid = []
    for w in range(weeks):
        monday = start + dt.timedelta(days=7 * w)
        grid.append({"monday": monday, "days": [
            {"day": monday + dt.timedelta(days=i), "events": ev.get(monday + dt.timedelta(days=i), []),
             "today": monday + dt.timedelta(days=i) == today, "skip": skips.get(monday + dt.timedelta(days=i)),
             "meets": i in days} for i in cols]})
    edit = None
    key = request.GET.get("edit", "")
    if ":" in key:
        kind, ref = key.split(":", 1)
        d = Dated.objects.filter(classroom=c, kind=kind, ref=ref).first()
        if d is not None:
            s = S.settings_for(c, kind, ref, d)
            edit = {"d": d, "label": cal.label(kind, ref), "opens": _field(c, d.opens), "due": _field(c, d.due),
                    "late_until": _field(c, d.late_until),
                    "results": [{"v": v, "label": l, "on": v == s.get("results")} for v, l in S.CHOICES[kind].get("results", [])],
                    "exceptions": [{"e": e, "name": e.student.profile.display_name, "due": e.due and e.due.astimezone(cal.zone(c))}
                                   for e in d.exceptions.select_related("student__profile")]}
    lessons, tests = _refs(c)
    units = [u for u in content.syllabus() if cal.unit_topics(u["n"], c.course)]
    others = Classroom.objects.filter(teacher=request.user).exclude(pk=c.pk)
    planned = {cal.unit_of(r) for r in Dated.objects.filter(classroom=c).values_list("ref", flat=True)} - {None}
    next_unit = next((u["n"] for u in units if u["n"] > max(planned, default=-1)), units[0]["n"] if units else None)
    return render(request, "classwork/calendar.html", {"next_unit": next_unit,
        "c": c, "tab": "calendar", "grid": grid, "cols": [cal.WEEKDAYS[i] for i in cols], "start": start,
        "prev": start - dt.timedelta(days=7 * weeks), "next": start + dt.timedelta(days=7 * weeks), "last": last,
        "edit": edit, "students": _students(c), "lessons": lessons, "tests": tests, "units": units, "others": others,
        "weekdays": [{"i": i, "name": n, "on": i in days} for i, n in enumerate(cal.WEEKDAYS)],
        "tz": S.class_setup(c).tz, "no_school": NoSchool.objects.filter(classroom=c, day__gte=today).order_by("day")[:12],
        "today": today, "kinds": [(k, S.NAMES[k]) for k in ("notes", "practice", "quiz", "unittest")], "tzs": TIMEZONES,
    })


def _calendar_post(request, c):
    P = request.POST
    act = P.get("action")
    back = P.get("back") or ""
    if not back.startswith("?"):
        back = ""
    if act == "plan":
        start, unit = _date(P.get("start")), P.get("unit", "")
        if start and unit.isdigit():
            rows = cal.plan_unit(c, int(unit), start, pace=2 if P.get("pace") == "2" else 1, review=P.get("then") != "test")
            messages.success(request, f"Planned {len(rows)} dates for Unit {unit}." if rows else
                             "Nothing to plan: Setup doesn't put that unit's work on a schedule.")
            back = f"?start={start.isoformat()}"
    elif act == "shift":
        since, n = _date(P.get("since")), P.get("n", "1")
        if since and n.lstrip("-").isdigit():
            moved = cal.shift(c, since, int(n))
            messages.success(request, f"Moved {moved} item{'s' if moved != 1 else ''} by {n} class day{'s' if abs(int(n)) != 1 else ''}.")
    elif act == "noschool":
        day = _date(P.get("day"))
        if day:
            NoSchool.objects.get_or_create(classroom=c, day=day, defaults={"note": (P.get("note") or "")[:60]})
    elif act == "noschool_remove":
        NoSchool.objects.filter(classroom=c, day=_date(P.get("day"))).delete()
    elif act == "days":
        s = Setup.objects.filter(classroom=c).first() or Setup(classroom=c)
        s.days = sorted({int(x) for x in P.getlist("day") if x.isdigit() and int(x) < 7}) or [0, 1, 2, 3, 4]
        tz = P.get("tz", "")
        if tz in TIMEZONES:
            s.tz = tz
        s.save()
    elif act == "copy":
        src = Classroom.objects.filter(teacher=request.user, pk=P.get("source")).exclude(pk=c.pk).first()
        if src:
            n = cal.copy_from(c, src)
            messages.success(request, f"Copied {src.name}'s setup and {n} dates.")
    elif act == "add":
        kind, ref = P.get("kind"), P.get("ref", "")
        lessons, tests = _refs(c)
        ok = {n for n, _ in tests} if kind == "unittest" else {n for n, _ in lessons}
        if kind in ("notes", "practice", "quiz", "unittest") and ref in ok:
            d, _ = Dated.objects.get_or_create(classroom=c, kind=kind, ref=ref)
            back = f"?edit={kind}:{ref}&start={P.get('start', '')}"
    elif act in ("item", "item_delete", "exc_add", "exc_remove"):
        d = Dated.objects.filter(classroom=c, pk=P.get("dated")).first()
        if d is not None:
            if act == "item":
                d.opens, d.due, d.late_until = _local(c, P.get("opens")), _local(c, P.get("due")), _local(c, P.get("late_until"))
                res = P.get("results")
                own = dict(d.settings or {})
                if res in {v for v, _ in S.CHOICES[d.kind].get("results", [])} and res != S.settings_for(c, d.kind, d.ref).get("results"):
                    own["results"] = res
                elif res:
                    own.pop("results", None)
                d.settings = own
                d.save()
                messages.success(request, f"Saved {cal.label(d.kind, d.ref)}.")
            elif act == "item_delete":
                d.delete()
                back = f"?start={P.get('start', '')}"
            elif act == "exc_add":
                st = next((u for u in _students(c) if str(u.pk) == P.get("student")), None)
                if st:
                    tf = P.get("time_factor", "1")
                    StudentException.objects.update_or_create(dated=d, student=st, defaults={
                        "due": _local(c, P.get("due")), "excused": bool(P.get("excused")),
                        "time_factor": float(tf) if tf in ("1", "1.25", "1.5", "2") else 1.0})
            elif act == "exc_remove":
                StudentException.objects.filter(dated=d, pk=P.get("exc")).delete()
    return redirect(reverse("cw_calendar", args=[c.pk]) + back)


TIMEZONES = ["America/New_York", "America/Chicago", "America/Denver", "America/Phoenix", "America/Los_Angeles",
             "America/Anchorage", "Pacific/Honolulu", "Europe/London", "Europe/Berlin", "Asia/Tokyo", "Australia/Sydney"]


# ------------------------------------------------------------------ progress map
from .progress import ClassData  # noqa: E402

SORTS = [("behind", "Most behind first"), ("name", "Name"), ("quiz", "Lowest quiz average"), ("active", "Last active")]


def _cell(cell, label, tip):
    """One square on the progress map (see the legend in progress.html)."""
    q = cell.get("quiz")
    pct = cell["progress"]
    out = {"tip": tip, "late": cell["late"], "txt": "", "low": False, "cls": ""}
    if not cell.get("tracked", True) and pct is None and q is None:
        out["cls"] = "untracked"
        return out
    if cell["done"]:
        out["cls"] = "full"
    out["fill"] = 0 if cell["done"] or pct is None else round(100 * pct)
    if q:
        out["txt"] = f"{q[0]:g}"
        out["low"] = q[1] and q[0] / q[1] <= 0.4
        out["tip"] += f" · quiz {q[0]:g}/{q[1]}"
    if pct is not None:
        out["tip"] += f" · {round(100 * pct)}% of notes and practice"
    return out


@never_cache
@teacher_required
def progress_page(request, pk):
    c = own_class(request, pk)
    data = ClassData(c)
    units = [u for u in content.syllabus() if cal.unit_topics(u["n"], c.course)]
    focus = request.GET.get("unit", "")
    focus = int(focus) if focus.isdigit() else data.current_unit()
    only_due = request.GET.get("due") == "1"
    now = data.now
    columns = []
    for u in units:
        if u["n"] != focus:
            columns.append({"kind": "unit", "unit": u["n"], "label": u["short"].replace("Unit ", "U") if not u["module"] else "Trig",
                            "title": u["heading"], "href": f"?unit={u['n']}"})
            continue
        for num in cal.unit_topics(u["n"], c.course):
            d = data.dated.get(("notes", num))
            opens = d.opens if d and data.sets["notes"]["opens"] == "schedule" else None
            first_due = min([x.due for k in ("notes", "practice", "quiz") for x in [data.dated.get((k, num))] if x and x.due] or [None],
                            key=lambda m: m or now)
            if only_due and (first_due is None or first_due > now):
                continue
            columns.append({"kind": "topic", "num": num, "label": content.label(num).split(" ")[0], "focus": True,
                            "locked": opens and opens > now and cal.local_day(c, opens), "title": content.label(num)})
        t = content.pick_test(u["n"], c.course)
        if t:
            td = data.dated.get(("unittest", t["num"]))
            columns.append({"kind": "test", "num": t["num"], "label": "Test", "focus": True, "title": content.test_label(t["num"]),
                            "locked": td and td.opens and td.opens > now and cal.local_day(c, td.opens)})
    rows = []
    for s in data.students:
        cells = []
        for col in columns:
            if col["kind"] == "unit":
                summ = data.unit_summary(s.id, col["unit"])
                cell = {"progress": summ["progress"], "done": summ["done"], "late": summ["late"], "tracked": True, "quiz": None}
                out = _cell(cell, col["label"], f"{col['title']}: {round(100 * summ['progress'])}% of lessons done")
                out.update(txt=str(summ["avg"]) if summ["avg"] is not None else "", low=summ["avg"] is not None and summ["avg"] < 70, unit=True)
            elif col["locked"]:
                out = {"cls": "locked", "txt": col["locked"].strftime("%-m/%-d"), "tip": f"{col['title']} opens later"}
            elif col["kind"] == "test":
                q = data.quiz(s.id, col["num"])
                out = {"cls": "full" if q else "", "txt": f"{round(100 * q[0] / q[1])}" if q and q[1] else "", "fill": 0,
                       "low": bool(q and q[1] and q[0] / q[1] < 0.6), "tip": col["title"],
                       "late": bool(data.due("unittest", col["num"], s.id) and now > data.due("unittest", col["num"], s.id) and not q)}
            else:
                out = _cell(data.lesson(s.id, col["num"]), col["label"], col["title"])
            cells.append(out)
        done, total = data.due_work(s.id)
        avg = data.quiz_average(s.id)
        rows.append({"s": s, "name": s.profile.display_name, "cells": cells, "done": done, "total": total,
                     "share": done / total if total else 1.0, "avg": avg, "last": data.last_active.get(s.id)})
    sort = request.GET.get("sort", "behind")
    keyf = {"name": lambda r: r["name"].lower(), "quiz": lambda r: (r["avg"] is None, r["avg"] or 0),
            "active": lambda r: (r["last"] is not None, r["last"] or now)}.get(sort, lambda r: (r["share"], r["avg"] or 0))
    rows.sort(key=keyf)
    class_row = []
    for i, col in enumerate(columns):
        vals = [r["cells"][i] for r in rows if r["cells"][i].get("cls") not in ("locked", "untracked")]
        class_row.append(f"{round(100 * sum(1 for v in vals if v.get('cls') == 'full') / len(vals))}%" if vals else "")
    show_all = request.GET.get("all") == "1"
    return render(request, "classwork/progress.html", {
        "c": c, "tab": "progress", "columns": columns, "rows": rows if show_all or len(rows) <= 30 else rows[:30],
        "more": max(0, len(rows) - 30) if not show_all else 0, "class_row": class_row, "focus": focus, "units": units,
        "sorts": SORTS, "sort": sort, "only_due": only_due, "n": len(rows),
    })


# ------------------------------------------------------------------ class home
from collections import Counter  # noqa: E402

from course.models import QuizAttempt, Release, Response, StepDone  # noqa: E402


def _quiz_refs(data):
    return sorted({ref for (_, ref) in data.attempts} | {k[1] for k in data.dated if k[0] in ("quiz", "unittest")},
                  key=lambda r: (r.startswith("U"), [int(x) if x.isdigit() else 0 for x in r.lstrip("U").replace("BC", "").split(".")]))


def item_stats(data, ref):
    """Per question: how many answered it right (teacher fixes count) and the most common wrong answer."""
    right, seen, wrong = Counter(), Counter(), {}
    for (uid, r), tries in data.attempts.items():
        if r != ref or not tries:
            continue
        a = tries[0]
        for iid in a.served or list(a.detail):
            d = a.detail.get(iid, {})
            seen[iid] += 1
            if d.get("correct") or data.fixes.get((uid, ref, iid), 0) >= 1:
                right[iid] += 1
            elif d.get("given"):
                wrong.setdefault(iid, Counter())[d["given"].strip()] += 1
    return {iid: {"seen": seen[iid], "right": right[iid], "wrong": wrong.get(iid, Counter()).most_common(1)} for iid in seen}


def needs_you(data):
    """The class home's to-do list, newest and most pressing first."""
    c, out, now = data.c, [], data.now
    watch = S.watch(c)
    names = {s.id: s.profile.display_name for s in data.students}
    for ref in _quiz_refs(data):
        kind = "unittest" if ref.startswith("U") else "quiz"
        label = cal.label(kind, ref)
        took = [u for u in data.ids if data.attempts.get((u, ref))]
        d = data.dated.get((kind, ref))
        st = S.settings_for(c, kind, ref, d)
        if took and st.get("results") == "release" and not Release.objects.filter(classroom=c, topic=ref).exists():
            closed = d is not None and d.due is not None and d.due < now
            out.append({"tag": "Release", "warn": True, "at": d.due if d and d.due else now,
                        "text": f"{label}{' closed' if closed else ''}: {len(took)} of {len(data.ids)} took it. Results are waiting for you.",
                        "href": reverse("cw_quiz", args=[c.pk, ref]), "action": "Review"})
        if watch["missing"] and d is not None and d.due and d.due < now and st["where"] == "site":
            missing = [names[u] for u in data.ids if not data.attempts.get((u, ref)) and data.due(kind, ref, u) and data.due(kind, ref, u) < now]
            if missing:
                out.append({"tag": "Missing", "warn": True, "at": d.due,
                            "text": f"{len(missing)} didn't take {label}: {', '.join(missing[:6])}{'…' if len(missing) > 6 else ''}.",
                            "href": reverse("cw_quiz", args=[c.pk, ref]), "action": "See who"})
        if watch["hard_questions"] and len(took) >= 4:
            for i, (iid, s) in enumerate(item_stats(data, ref).items(), 1):
                if s["seen"] >= 4 and s["right"] * 2 < s["seen"]:
                    w = s["wrong"][0] if s["wrong"] else None
                    out.append({"tag": "Question", "at": d.due if d and d.due else now,
                                "text": f"{label}, question {i}: {s['seen'] - s['right']} of {s['seen']} missed it"
                                        + (f", and {w[1]} answered {w[0]}." if w and w[1] > 1 else "."),
                                "href": reverse("cw_quiz", args=[c.pk, ref]) + f"#q{i}", "action": "See it"})
    if watch["sliding"]:
        for s in data.students:
            recent = sorted(((tries[0].at, ref) for (u, ref), tries in data.attempts.items() if u == s.id and not ref.startswith("U")), reverse=True)[:2]
            scores = [data.quiz(s.id, ref) for _, ref in recent]
            if len(scores) == 2 and all(q and q[1] and q[0] / q[1] < 0.6 for q in scores):
                out.append({"tag": "Scores", "at": recent[0][0], "text": f"{names[s.id]} scored under 60% on {cal.label('quiz', recent[1][1])} and {cal.label('quiz', recent[0][1])}.",
                            "href": reverse("cw_student", args=[c.pk, s.id]), "action": "Open"})
    unit = data.current_unit()
    sched = data.scheduled_index(unit)
    topics = cal.unit_topics(unit, c.course)
    for s in data.students:
        far = data.furthest(s.id, unit)
        last = data.last_active.get(s.id)
        if sched >= 0 and sched - far >= 3:
            out.append({"tag": "Behind", "at": now - dt.timedelta(minutes=1),
                        "text": f"{names[s.id]} is {sched - far} lessons behind the schedule"
                                + (f" (last active {(now - last).days} days ago)." if last and (now - last).days >= 2 else "."),
                        "href": reverse("cw_student", args=[c.pk, s.id]), "action": "Open"})
        elif watch["inactive_days"] and (last is None or (now - last).days >= watch["inactive_days"]):
            out.append({"tag": "Quiet", "at": now - dt.timedelta(minutes=2),
                        "text": f"{names[s.id]} hasn't worked on the site {'yet' if last is None else f'in {(now - last).days} days'}.",
                        "href": reverse("cw_student", args=[c.pk, s.id]), "action": "Open"})
        joined = data.joined.get(s.id)
        if joined and (now - joined).days < 7:
            out.append({"tag": "New", "at": joined, "text": f"{names[s.id]} joined {joined.astimezone(cal.zone(c)).strftime('%A')}.",
                        "href": reverse("cw_student", args=[c.pk, s.id]), "action": "Open"})
    order = {"Release": 0, "Missing": 1, "Question": 2, "Scores": 3, "Behind": 4, "Quiet": 5, "New": 6}
    out.sort(key=lambda x: (order[x["tag"]], -(x["at"].timestamp())))
    return group_needs(out, c)


SUMMARY = {"Release": "{n} quizzes and tests have results waiting for you.", "Missing": "{n} quizzes have students who didn't take them.",
           "Question": "{n} questions were missed by half the class or more.", "Scores": "{n} students scored under 60% on their last two quizzes.",
           "Behind": "{n} students are 3 or more lessons behind the schedule.", "Quiet": "{n} students haven't worked on the site lately.",
           "New": "{n} students joined this week."}


def group_needs(items, c):
    """One row per kind of thing: a single item shows as is; several fold under a one-line summary."""
    groups = []
    for it in items:
        if groups and groups[-1]["tag"] == it["tag"]:
            groups[-1]["items"].append(it)
        else:
            groups.append({"tag": it["tag"], "warn": it.get("warn"), "items": [it]})
    for g in groups:
        if len(g["items"]) > 1:
            g["summary"] = SUMMARY[g["tag"]].format(n=len(g["items"]))
            if g["tag"] in ("Release", "Missing"):
                g["href"], g["action"] = reverse("cw_quizzes", args=[c.pk]), "Quizzes"
            elif g["tag"] in ("Behind", "Quiet", "New", "Scores"):
                g["href"], g["action"] = reverse("cw_progress", args=[c.pk]), "Progress"
    return groups


@never_cache
@teacher_required
def class_home(request, pk):
    c = own_class(request, pk)
    data = ClassData(c)
    now = data.now
    today = cal.local_day(c, now)
    monday = today - dt.timedelta(days=today.weekday())
    sunday = monday + dt.timedelta(days=6)
    due_week = []
    for (kind, ref), d in sorted(data.dated.items(), key=lambda kv: kv[1].due or now):
        if not d.due or kind not in ("notes", "practice", "quiz", "unittest"):
            continue
        day = cal.local_day(c, d.due)
        if not (monday <= day <= sunday):
            continue
        if kind in ("quiz", "unittest"):
            done = sum(1 for u in data.ids if data.quiz(u, ref) is not None)
        else:
            done = sum(1 for u in data.ids if data.lesson(u, ref)["done"])
        due_week.append({"label": cal.label(kind, ref), "day": day.strftime("%a"), "done": done, "of": len(data.ids),
                         "pct": round(100 * done / len(data.ids)) if data.ids else 0, "past": d.due < now})
    nxt = sorted((d for (k, _), d in data.dated.items() if k == "unittest" and (d.opens or d.due) and (d.opens or d.due) > now),
                 key=lambda d: d.opens or d.due)
    unit = data.current_unit()
    topics = cal.unit_topics(unit, c.course)
    sched = data.scheduled_index(unit)
    dots, stack = [], Counter()
    for s in data.students:
        i = data.furthest(s.id, unit)
        stack[i] += 1
        dots.append({"name": s.profile.display_name, "left": round(100 * (i + 0.5) / len(topics)) if topics and i >= 0 else 0,
                     "bottom": 4 + 14 * (stack[i] - 1), "none": i < 0, "href": reverse("cw_student", args=[c.pk, s.id])})
    ahead = sum(1 for s in data.students if sched >= 0 and data.furthest(s.id, unit) > sched)
    behind = sum(1 for s in data.students if sched >= 0 and sched - data.furthest(s.id, unit) >= 2)
    return render(request, "classwork/home.html", {
        "c": c, "tab": "home", "needs": needs_you(data), "due_week": due_week,
        "next_test": nxt[0] if nxt else None, "next_label": nxt and cal.label("unittest", nxt[0].ref),
        "next_when": nxt and (nxt[0].opens or nxt[0].due).astimezone(cal.zone(c)),
        "unit": next((u for u in content.syllabus() if u["n"] == unit), None), "topics": [content.label(t).split(" ")[0] for t in topics],
        "dots": dots, "sched_left": round(100 * (sched + 0.5) / len(topics)) if topics and sched >= 0 else None,
        "sched_label": topics[sched] if 0 <= sched < len(topics) else "", "sched_right": topics and sched >= 0 and (sched + 0.5) / len(topics) > 0.7, "ahead": ahead, "behind": behind,
        "on_pace": len(data.students) - ahead - behind, "setup_line": _setup_line(c), "stack_h": 14 * max(stack.values() or [1]) + 18,
    })


def _setup_line(c):
    bits = []
    for k in ("notes", "practice", "quiz", "unittest"):
        s = S.settings_for(c, k)
        where = {"site": "online", "paper": "on paper", "off": "not used"}[s["where"]]
        bits.append(f"{S.NAMES[k].lower()} {where}")
    return " · ".join(bits).capitalize()


# ------------------------------------------------------------------ one quiz or test
import re as _re  # noqa: E402

from .models import Adjustment, AnswerFix, GraderMiss  # noqa: E402


def _plain(html, n=90):
    t = _re.sub(r"<[^>]+>", " ", html or "")
    t = " ".join(t.split())
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "…"


def _same(a, b):
    return " ".join((a or "").split()).lower() == " ".join((b or "").split()).lower()


@never_cache
@teacher_required
def quiz_page(request, pk, ref):
    c = own_class(request, pk)
    kind = "unittest" if ref.startswith("U") else "quiz"
    pub, priv = content.public(ref), content.private(ref)
    if not pub:
        raise Http404
    if request.method == "POST":
        return _quiz_post(request, c, ref, kind, priv)
    data = ClassData(c)
    d = data.dated.get((kind, ref))
    names = {s.id: s.profile.display_name for s in data.students}
    first = next((t[0] for (u, r), t in data.attempts.items() if r == ref and t), None)
    order = (first.served if first else []) or [it["id"] for it in pub.get("quiz", [])]
    items = {v["id"]: v for row in (pub.get("quiz_variants") or [[q] for q in pub.get("quiz", [])]) for v in row}
    stats = item_stats(data, ref)
    dropped = data.dropped.get(ref, set())
    questions = []
    for i, iid in enumerate(order, 1):
        s = stats.get(iid, {"seen": 0, "right": 0, "wrong": []})
        w = s["wrong"][0] if s["wrong"] else None
        questions.append({"i": i, "id": iid, "text": _plain(items.get(iid, {}).get("html", "")), "seen": s["seen"], "right": s["right"],
                          "pct": round(100 * s["right"] / s["seen"]) if s["seen"] else 0, "low": s["seen"] and s["right"] * 2 < s["seen"],
                          "wrong": w and w[0], "wrong_n": w and w[1], "dropped": iid in dropped,
                          "key": (priv["items"].get(iid, {}).get("answer", {}) or {}).get("display", "")})
    rows, hist = [], Counter()
    for s in data.students:
        tries = data.attempts.get((s.id, ref))
        q = data.quiz(s.id, ref)
        due = data.due(kind, ref, s.id)
        if tries:
            a = tries[0]
            marks = []
            for iid in order:
                det = a.detail.get(iid, {})
                fix = data.fixes.get((s.id, ref, iid))
                marks.append("–" if iid in dropped else "✓" if det.get("correct") or (fix or 0) >= 1 else "½" if fix else "✗")
            hist[round(q[0]) if q else 0] += 1
            rows.append({"s": s, "name": names[s.id], "score": q, "marks": "".join(marks), "at": a.at.astimezone(cal.zone(c)),
                         "late": bool(due and a.at > due), "tries": len(tries), "pct": q[0] / q[1] if q and q[1] else 0})
        else:
            exc = data.exceptions.get((d.pk, s.id)) if d else None
            rows.append({"s": s, "name": names[s.id], "score": None, "missing": bool(due and due < data.now),
                         "exc": exc, "pct": -1})
    rows.sort(key=lambda r: (r["score"] is not None, r["pct"]))
    total = len(order) - len(dropped & set(order))
    took = [r for r in rows if r["score"] is not None]
    avg = sum(r["score"][0] for r in took) / len(took) if took else None
    peak = max(hist.values() or [1])
    return render(request, "classwork/quiz.html", {
        "c": c, "tab": "quizzes", "ref": ref, "kind": kind, "label": cal.label(kind, ref), "questions": questions, "rows": rows,
        "took": len(took), "n": len(data.students), "avg": avg, "total": total,
        "hist": [{"score": k, "n": hist[k], "h": round(100 * hist[k] / peak)} for k in range(total + 1)],
        "released": Release.objects.filter(classroom=c, topic=ref).exists(),
        "results": S.settings_for(c, kind, ref, d).get("results"), "dated": d,
        "due_text": d and d.due and d.due.astimezone(cal.zone(c)).strftime("%a %b %-d"), "closed": d and d.due and d.due < data.now,
        "form": first.form if first else "",
    })


def _quiz_post(request, c, ref, kind, priv):
    P = request.POST
    act = P.get("action")
    back = reverse("cw_quiz", args=[c.pk, ref])
    students = {s.id: s for s in _students(c)}
    if act == "release":
        r = Release.objects.filter(classroom=c, topic=ref)
        r.delete() if r.exists() else Release.objects.create(classroom=c, topic=ref)
    elif act == "drop":
        iid = P.get("item", "")
        if iid in priv["items"]:
            a = Adjustment.objects.filter(classroom=c, kind="drop_question", params__ref=ref, params__item=iid)
            a.delete() if a.exists() else Adjustment.objects.create(classroom=c, kind="drop_question", params={"ref": ref, "item": iid},
                                                                    note=f"{cal.label(kind, ref)}: one question dropped")
    elif act == "accept":
        iid, given = P.get("item", ""), P.get("given", "")
        if iid in priv["items"] and given:
            n = _accept(request, c, ref, iid, given, students)
            messages.success(request, f"Marked {n} answer{'s' if n != 1 else ''} right.")
    elif act in ("reopen", "excuse"):
        st = students.get(int(P.get("student", "0") or 0))
        if st:
            d, _ = Dated.objects.get_or_create(classroom=c, kind=kind, ref=ref)
            e, _ = StudentException.objects.get_or_create(dated=d, student=st)
            if act == "reopen":
                e.reopened, e.due = True, dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=2)
            else:
                e.excused = not e.excused
            e.save()
    return redirect(back)


def _accept(request, c, ref, iid, given, students):
    """Mark one answer right for every student in the class who gave it (the grader missed it), and report it."""
    n = 0
    for a in QuizAttempt.objects.filter(classroom=c, topic=ref, user__in=list(students)):
        det = a.detail.get(iid)
        if det and not det.get("correct") and _same(det.get("given"), given):
            AnswerFix.objects.update_or_create(classroom=c, student_id=a.user_id, topic=ref, item=iid,
                                               defaults={"credit": 1.0, "by": request.user})
            n += 1
    if n:
        GraderMiss.objects.get_or_create(topic=ref, item=iid, given=given[:300], defaults={"reported_by": request.user})
    return n


@never_cache
@teacher_required
def quizzes_page(request, pk):
    c = own_class(request, pk)
    data = ClassData(c)
    rows = []
    for ref in _quiz_refs(data):
        kind = "unittest" if ref.startswith("U") else "quiz"
        d = data.dated.get((kind, ref))
        scores = [q for u in data.ids for q in [data.quiz(u, ref)] if q]
        res = S.settings_for(c, kind, ref, d).get("results")
        rel = Release.objects.filter(classroom=c, topic=ref).exists()
        rows.append({"ref": ref, "label": cal.label(kind, ref), "took": len(scores), "n": len(data.ids),
                     "avg": round(100 * sum(p for p, _ in scores) / sum(t for _, t in scores)) if scores and sum(t for _, t in scores) else None,
                     "due": d and d.due and d.due.astimezone(cal.zone(c)),
                     "status": "Released" if rel else {"now": "Shown right away", "due": "Shown at the due date"}.get(res, "Waiting for you"),
                     "waiting": res == "release" and not rel and scores})
    return render(request, "classwork/quizzes.html", {"c": c, "tab": "quizzes", "rows": rows})


@never_cache
@teacher_required
def students_page(request, pk):
    c = own_class(request, pk)
    data = ClassData(c)
    rows = []
    for s in data.students:
        done, total = data.due_work(s.id)
        rows.append({"s": s, "name": s.profile.display_name, "done": done, "total": total, "avg": data.quiz_average(s.id),
                     "last": data.last_active.get(s.id)})
    return render(request, "classwork/students.html", {"c": c, "tab": "students", "rows": rows,
                                                       "temp_password": request.session.pop("temp_password", None)})


from .models import Accommodation, TeacherNote  # noqa: E402


@never_cache
@teacher_required
def student_page(request, pk, uid):
    c = own_class(request, pk)
    e = get_object_or_404(c.enrollments.select_related("student__profile"), student_id=uid)
    st = e.student
    if request.method == "POST":
        return _student_post(request, c, st)
    data = ClassData(c)
    unit = request.GET.get("unit", "")
    unit = int(unit) if unit.isdigit() else data.current_unit()
    tz = cal.zone(c)
    lessons = []
    for num in cal.unit_topics(unit, c.course):
        n = data.counts(num)
        cell = data.lesson(st.id, num)
        q = data.quiz(st.id, num)
        due = [x for x in (data.due(k, num, st.id) for k in ("notes", "practice", "quiz")) if x]
        lessons.append({"num": num, "title": content.label(num), "steps": data.steps.get((st.id, num), 0), "steps_total": n.get("steps", 0),
                        "tried": data.tried.get((st.id, num), 0), "practice_total": n.get("practice", 0), "quiz": q,
                        "low": q and q[1] and q[0] / q[1] <= 0.4, "late": cell["late"], "done": cell["done"],
                        "due": min(due).astimezone(tz) if due else None,
                        "notes_mark": data.marks.get((st.id, "notes", num, "")), "practice_mark": data.marks.get((st.id, "practice", num, ""))})
    # one quiz, answer by answer
    taken = sorted(((t[0].at, ref) for (u, ref), t in data.attempts.items() if u == st.id and t), reverse=True)
    pick = request.GET.get("quiz") or (taken[0][1] if taken else None)
    answers, pick_label = [], ""
    if pick and data.attempts.get((st.id, pick)):
        a = data.attempts[(st.id, pick)][0]
        pub, priv = content.public(pick), content.private(pick)
        items = {v["id"]: v for row in (pub.get("quiz_variants") or [[q] for q in pub.get("quiz", [])]) for v in row}
        others = [t[0] for (u, r), t in data.attempts.items() if r == pick and u != st.id and t]
        for i, iid in enumerate(a.served or list(a.detail), 1):
            det = a.detail.get(iid, {})
            fix = data.fixes.get((st.id, pick, iid))
            same = sum(1 for o in others if not o.detail.get(iid, {}).get("correct") and _same(o.detail.get(iid, {}).get("given"), det.get("given"))
                       and data.fixes.get((o.user_id, pick, iid), 0) < 1) if det.get("given") and not det.get("correct") else 0
            answers.append({"i": i, "id": iid, "text": _plain(items.get(iid, {}).get("html", ""), 120), "given": det.get("given", ""),
                            "correct": det.get("correct"), "fix": fix, "dropped": iid in data.dropped.get(pick, set()),
                            "key": (priv["items"].get(iid, {}).get("answer", {}) or {}).get("display", ""), "same": same})
        pick_label = cal.label("unittest" if pick.startswith("U") else "quiz", pick)
    units = []
    for u in content.syllabus():
        if not cal.unit_topics(u["n"], c.course):
            continue
        summ = data.unit_summary(st.id, u["n"])
        units.append({"u": u, "pct": round(100 * summ["progress"]), "avg": summ["avg"], "on": u["n"] == unit})
    missing = []
    for (kind, ref), d in data.dated.items():
        due = data.due(kind, ref, st.id)
        if not due or due > data.now or kind not in ("notes", "practice", "quiz", "unittest"):
            continue
        done = data.quiz(st.id, ref) is not None if kind in ("quiz", "unittest") else data.lesson(st.id, ref)["done"]
        if not done:
            missing.append({"d": d, "label": cal.label(kind, ref), "due": due.astimezone(tz)})
    missing.sort(key=lambda m: m["due"])
    # activity by day, last three weeks
    today = cal.local_day(c, data.now)
    start = today - dt.timedelta(days=today.weekday() + 14)
    per_day = Counter()
    for qs, f in ((StepDone.objects, "at"), (Response.objects, "at")):
        for t in qs.filter(user=st, **{f + "__gte": dt.datetime.combine(start, dt.time(), tzinfo=tz)}).values_list(f, flat=True):
            per_day[t.astimezone(tz).date()] += 1
    peak = max(per_day.values() or [1])
    days = [{"day": start + dt.timedelta(days=i), "lv": 0 if not per_day[start + dt.timedelta(days=i)] else
             1 + min(2, int(3 * per_day[start + dt.timedelta(days=i)] / (peak + 1))), "n": per_day[start + dt.timedelta(days=i)]} for i in range(21)]
    ids = data.ids
    i = ids.index(st.id)
    note = TeacherNote.objects.filter(classroom=c, student=st).first()
    acc = Accommodation.objects.filter(classroom=c, student=st).first()
    far, sched = data.furthest(st.id, unit), data.scheduled_index(unit)
    topics = cal.unit_topics(unit, c.course)
    return render(request, "classwork/student.html", {
        "c": c, "tab": "students", "st": st, "name": st.profile.display_name, "lessons": lessons, "unit": unit,
        "answers": answers, "pick": pick, "pick_label": pick_label,
        "taken": [{"ref": r, "label": cal.label("unittest" if r.startswith("U") else "quiz", r)} for _, r in taken],
        "units": units, "missing": missing, "days": days, "note": note.text if note else "", "acc": acc,
        "avg": data.quiz_average(st.id), "last": data.last_active.get(st.id), "joined": e.joined,
        "prev": ids[i - 1] if i > 0 else None, "next": ids[i + 1] if i + 1 < len(ids) else None,
        "pace": (f"{sched - far} lessons behind" if sched - far >= 2 else "ahead" if far > sched >= 0 else "on pace") if sched >= 0 else "",
        "at": content.label(topics[far]).split(" ")[0] if 0 <= far < len(topics) else "",
    })


def _student_post(request, c, st):
    P = request.POST
    act = P.get("action")
    back = reverse("cw_student", args=[c.pk, st.id]) + (f"?quiz={P.get('ref')}" if P.get("ref") else "")
    if act in ("fix", "half", "unfix"):
        ref, iid = P.get("ref", ""), P.get("item", "")
        priv = content.private(ref) if ref else None
        if priv and iid in priv["items"]:
            if act == "unfix":
                AnswerFix.objects.filter(classroom=c, student=st, topic=ref, item=iid).delete()
            else:
                AnswerFix.objects.update_or_create(classroom=c, student=st, topic=ref, item=iid,
                                                   defaults={"credit": 1.0 if act == "fix" else 0.5, "by": request.user})
                if act == "fix":
                    a = QuizAttempt.objects.filter(user=st, topic=ref, classroom=c).order_by("at").first()
                    given = a and a.detail.get(iid, {}).get("given")
                    if given:
                        GraderMiss.objects.get_or_create(topic=ref, item=iid, given=given[:300], defaults={"reported_by": request.user})
    elif act == "accept_all":
        ref, iid, given = P.get("ref", ""), P.get("item", ""), P.get("given", "")
        priv = content.private(ref) if ref else None
        if priv and iid in priv["items"] and given:
            n = _accept(request, c, ref, iid, given, {s.id: s for s in _students(c)})
            messages.success(request, f"Marked {n} answer{'s' if n != 1 else ''} right.")
    elif act == "note":
        TeacherNote.objects.update_or_create(classroom=c, student=st, defaults={"text": P.get("text", "")[:4000]})
        messages.success(request, "Note saved.")
    elif act == "excuse":
        d = Dated.objects.filter(classroom=c, pk=P.get("dated")).first()
        if d:
            e, _ = StudentException.objects.get_or_create(dated=d, student=st)
            e.excused = True
            e.save()
    elif act == "accommodation":
        tf = P.get("time_factor", "1")
        Accommodation.objects.update_or_create(classroom=c, student=st, defaults={
            "time_factor": float(tf) if tf in ("1", "1.25", "1.5", "2") else 1.0, "note": P.get("note", "")[:120]})
    return redirect(back)


# ------------------------------------------------------------------ gradebook
import csv  # noqa: E402

from django.http import HttpResponse  # noqa: E402

from . import grades as G  # noqa: E402
from .models import Category, Curve, Mark, TeacherItem  # noqa: E402

SOURCES = [("unittest", "Unit tests"), ("quiz", "Quizzes"), ("practice", "Practice (done or not)"), ("notes", "Lesson notes (done or not)"),
           ("exam", "Practice exams"), ("own", "Your own items")]


def _f(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


@never_cache
@teacher_required
def gradebook_page(request, pk):
    c = own_class(request, pk)
    if request.method == "POST":
        return _gradebook_post(request, c)
    book = G.Book(c)
    rows = book.rows()
    detail = next((cat for cat in book.cats if str(cat.pk) == request.GET.get("detail")), None)
    items = book.items(detail) if detail else []
    if detail:
        for r in rows:
            r["items"] = [None if v is None else round(100 * v) for v in (book.score(detail, r["s"].id, k) for k, _ in items)]
    sort = request.GET.get("sort", "name")
    if sort == "grade":
        rows.sort(key=lambda r: (r["final"] is None, r["final"] or 0))
    weights = sum(cat.weight for cat in book.cats)
    gradeable = []
    for cat in book.cats:
        if cat.source in ("quiz", "unittest", "exam"):
            for k, label in book.items(cat):
                cv = book.curves.get((cat.source, k))
                raws = [v for v in (book.raw(cat, u, k) for u in book.data.ids) if v is not None]
                cur = [v for v in (book.score(cat, u, k) for u in book.data.ids) if v is not None]
                gradeable.append({"key": f"{cat.source}:{k}", "label": label, "curve": cv,
                                  "before": round(100 * sum(raws) / len(raws)) if raws else None,
                                  "after": round(100 * sum(cur) / len(cur)) if cur else None})
    return render(request, "classwork/gradebook.html", {
        "c": c, "tab": "gradebook", "cats": book.cats, "rows": rows, "detail": detail, "items": items, "weights": weights,
        "rules": {cat.pk: [{"key": key, "label": label, "options": [{"v": v, "label": l, "on": cat.rules.get(key, opts[0][0]) == v}
                                                                     for v, l in opts]} for key, label, opts in G.RULES.get(cat.source, [])]
                  for cat in book.cats},
        "sources": SOURCES, "gradeable": gradeable, "methods": Curve.METHODS[:4],
        "bonuses": Adjustment.objects.filter(classroom=c, kind="bonus"), "scale": book.scale, "sort": sort,
        "own_cats": [cat for cat in book.cats if cat.source == "own"],
        "entry": _entry_choices(c, book),
    })


def _entry_choices(c, book):
    """What can be entered by hand: paper quizzes and tests, notes and practice marked done, the teacher's own items."""
    out = []
    lessons = [n for u in content.syllabus() for n in cal.unit_topics(u["n"], c.course)]
    sets = book.data.sets
    if sets["unittest"]["where"] != "off":
        out += [(f"unittest:{t['num']}", content.test_label(t["num"])) for n in sorted(content.unit_tests())
                for t in [content.pick_test(n, c.course)] if t]
    if sets["quiz"]["where"] != "off":
        out += [(f"quiz:{n}", f"Quiz {content.label(n)}") for n in lessons]
    if sets["notes"]["where"] == "paper" or sets["notes"]["record"] == "mark":
        out += [(f"notes:{n}", f"{content.label(n)} notes, done") for n in lessons]
    if sets["practice"]["where"] == "paper":
        out += [(f"practice:{n}", f"{content.label(n)} practice, done") for n in lessons]
    out += [(f"own:{i.pk}", f"{i.name} ({cat.name})") for cat in book.cats if cat.source == "own" for i in cat.items.all()]
    return out


def _gradebook_post(request, c):
    P = request.POST
    act = P.get("action")
    back = reverse("cw_gradebook", args=[c.pk])
    cats = {str(cat.pk): cat for cat in G.categories(c)}
    if act == "weights":
        for k, cat in cats.items():
            cat.weight = max(0.0, _f(P.get(f"w{k}"), cat.weight))
            for key, _, opts in G.RULES.get(cat.source, []):
                v = P.get(f"r{k}.{key}")
                match = next((o for o, _ in opts if str(o) == v), None)
                if v is not None and (match is not None or v == str(match)):
                    cat.rules = {**cat.rules, key: match}
            cat.save()
        messages.success(request, "Weights saved.")
    elif act == "add_category":
        name = " ".join((P.get("name") or "").split())[:60]
        src = P.get("source")
        if name and src in dict(SOURCES):
            Category.objects.create(classroom=c, name=name, source=src, weight=max(0.0, _f(P.get("weight"), 10)), order=len(cats))
    elif act == "delete_category" and P.get("cat") in cats:
        cats[P.get("cat")].delete()
    elif act == "add_item" and P.get("cat") in cats and cats[P.get("cat")].source == "own":
        name = " ".join((P.get("name") or "").split())[:80]
        if name:
            it = TeacherItem.objects.create(category=cats[P.get("cat")], name=name, points=max(1.0, _f(P.get("points"), 10)),
                                            day=_date(P.get("day")), done_only=bool(P.get("done_only")))
            return redirect(back + f"enter/?item=own:{it.pk}")
    elif act == "curve":
        kind, _, ref = (P.get("item") or "").partition(":")
        method = P.get("method")
        if kind in ("quiz", "unittest", "exam") and ref and method in dict(Curve.METHODS):
            Curve.objects.update_or_create(classroom=c, kind=kind, ref=ref, defaults={
                "method": method, "params": {"target": _f(P.get("target"), 80), "points": _f(P.get("points"), 5)},
                "allow_over": bool(P.get("allow_over"))})
    elif act == "uncurve":
        kind, _, ref = (P.get("item") or "").partition(":")
        Curve.objects.filter(classroom=c, kind=kind, ref=ref).delete()
    elif act == "bonus":
        pts = _f(P.get("points"), 0)
        if pts:
            Adjustment.objects.create(classroom=c, kind="bonus", params={"points": pts}, note=(P.get("note") or "")[:120])
    elif act == "unbonus":
        Adjustment.objects.filter(classroom=c, kind="bonus", pk=P.get("adj")).delete()
    elif act == "scale":
        sc = []
        for name in ("A", "B", "C", "D"):
            v = _f(P.get(f"s{name}"), None)
            if v is not None:
                sc.append([name, v])
        s = Setup.objects.filter(classroom=c).first() or Setup(classroom=c)
        s.grading = {**(s.grading or {}), "scale": sorted(sc, key=lambda x: -x[1])}
        s.save()
    return redirect(back)


@never_cache
@teacher_required
def enter_page(request, pk):
    """Type in scores for one item: a paper quiz or unit test (by part), notes or practice done on paper, an own item."""
    c = own_class(request, pk)
    key = request.GET.get("item") or request.POST.get("item") or ""
    kind, _, ref = key.partition(":")
    students = _students(c)
    book = G.Book(c)
    if (key, ) not in [(k,) for k, _ in _entry_choices(c, book)]:
        return redirect("cw_gradebook", pk=c.pk)
    own = TeacherItem.objects.filter(category__classroom=c, pk=ref).first() if kind == "own" else None
    parts = G.test_parts(ref) if kind == "unittest" else [("", "Score", (book.data.counts(ref).get("quiz") or 5))] if kind == "quiz" else []
    if request.method == "POST":
        for s in students:
            if kind == "own":
                G.save_own_score(own, s, request.POST.get(f"v{s.pk}", ""))
                continue
            flags = {"excused": request.POST.get(f"x{s.pk}") == "ex", "absent": request.POST.get(f"x{s.pk}") == "ab"}
            if kind in ("notes", "practice"):
                done = bool(request.POST.get(f"d{s.pk}"))
                if done or any(flags.values()):
                    Mark.objects.update_or_create(classroom=c, student=s, kind=kind, ref=ref, part="",
                                                  defaults={"done": done, **flags, "by": request.user})
                else:
                    Mark.objects.filter(classroom=c, student=s, kind=kind, ref=ref, part="").delete()
                continue
            for part, _, possible in parts:
                v = request.POST.get(f"p{s.pk}.{part}", "").strip()
                if v == "" or any(flags.values()):
                    Mark.objects.filter(classroom=c, student=s, kind=kind, ref=ref, part=part).delete()
                else:
                    Mark.objects.update_or_create(classroom=c, student=s, kind=kind, ref=ref, part=part,
                                                  defaults={"points": max(0.0, min(_f(v), float(possible))), "possible": possible,
                                                            "excused": False, "absent": False, "by": request.user})
            if any(flags.values()):
                Mark.objects.update_or_create(classroom=c, student=s, kind=kind, ref=ref, part="",
                                              defaults={**flags, "points": None, "by": request.user})
            elif kind == "unittest":
                Mark.objects.filter(classroom=c, student=s, kind=kind, ref=ref, part="", points__isnull=True).delete()
        messages.success(request, "Scores saved.")
        return redirect(reverse("cw_enter", args=[c.pk]) + f"?item={key}")
    marks = {(m.student_id, m.part): m for m in Mark.objects.filter(classroom=c, kind=kind, ref=ref)} if kind != "own" else {}
    scores = {sc.student_id: sc for sc in own.scores.all()} if own else {}
    rows = []
    for s in students:
        flag = marks.get((s.pk, ""))
        rows.append({"s": s, "name": s.profile.display_name,
                     "parts": [{"part": p, "v": "" if marks.get((s.pk, p)) is None or marks[(s.pk, p)].points is None else f"{marks[(s.pk, p)].points:g}"}
                               for p, _, _ in parts],
                     "done": bool(marks.get((s.pk, "")) and marks[(s.pk, "")].done),
                     "flag": "ex" if flag and flag.excused else "ab" if flag and flag.absent else "",
                     "own": "ex" if scores.get(s.pk) and scores[s.pk].excused else ("" if not scores.get(s.pk) or scores[s.pk].points is None else f"{scores[s.pk].points:g}"),
                     "site": book.data.quiz(s.pk, ref) if kind in ("quiz", "unittest") and not any(marks.get((s.pk, p)) for p, _, _ in parts) else None})
    return render(request, "classwork/enter.html", {"c": c, "tab": "gradebook", "key": key, "kind": kind, "ref": ref, "own": own,
                                                    "parts": parts, "rows": rows, "label": dict(_entry_choices(c, book)).get(key, key),
                                                    "choices": _entry_choices(c, book)})


@teacher_required
def export(request, pk, fmt):
    c = own_class(request, pk)
    book = G.Book(c)
    rows = book.rows()
    resp = HttpResponse(content_type="text/csv; charset=utf-8")
    name = "".join(ch if ch.isalnum() else "-" for ch in c.name).strip("-") or "class"
    resp["Content-Disposition"] = f'attachment; filename="{name}-{fmt}.csv"'
    w = csv.writer(resp)
    if fmt == "powerschool":
        # PowerSchool's score import: one row per student, an identifier column and the score (percent)
        w.writerow(["Student", "Username", "Score", "Letter"])
        for r in rows:
            w.writerow([r["name"], r["s"].username, "" if r["final"] is None else r["final"], r["letter"]])
        return resp
    if fmt == "items":
        cols = [(cat, k, label) for cat in book.cats for k, label in book.items(cat)]
        w.writerow(["Student", "Username"] + [f"{cat.name}: {label}" for cat, _, label in cols] + ["Grade", "Letter"])
        for r in rows:
            vals = [book.score(cat, r["s"].id, k) for cat, k, _ in cols]
            w.writerow([r["name"], r["s"].username] + ["" if v is None else round(100 * v, 1) for v in vals] +
                       ["" if r["final"] is None else r["final"], r["letter"]])
        return resp
    w.writerow(["Student", "Username"] + [f"{cat.name} ({cat.weight:g}%)" for cat in book.cats] + ["Grade", "Letter"])
    for r in rows:
        w.writerow([r["name"], r["s"].username] + ["" if v is None else v for v in r["cats"]] +
                   ["" if r["final"] is None else r["final"], r["letter"]])
    return resp
