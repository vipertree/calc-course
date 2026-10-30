"""The teacher's class pages: setup, calendar, progress, students, quizzes and tests, gradebook."""
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
