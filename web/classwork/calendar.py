"""The class calendar: which days the class meets, planning a whole unit onto those days, shifting dates around a
snow day, and laying the dated work out by day for the calendar page.

Every time is stored aware (UTC in the database) but decided in the class's own time zone: work opens at 7:00 am
and is due at 11:59 pm on a class day, there.
"""
import datetime as dt
from zoneinfo import ZoneInfo

from accounts.models import unit_of
from course import content

from . import setup as S
from .models import Dated, NoSchool

OPEN_AT = dt.time(7, 0)
DUE_AT = dt.time(23, 59)
WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def zone(classroom):
    try:
        return ZoneInfo(S.class_setup(classroom).tz or "America/New_York")
    except Exception:
        return ZoneInfo("America/New_York")


def class_days(classroom):
    return sorted(set(S.class_setup(classroom).days or [0, 1, 2, 3, 4]))


def at(classroom, day, time):
    return dt.datetime.combine(day, time, tzinfo=zone(classroom))


def local_day(classroom, moment):
    return moment.astimezone(zone(classroom)).date()


def _skips(classroom):
    return set(NoSchool.objects.filter(classroom=classroom).values_list("day", flat=True))


def class_day_on_or_after(classroom, day, skips=None):
    days, skips = class_days(classroom), _skips(classroom) if skips is None else skips
    for _ in range(400):
        if day.weekday() in days and day not in skips:
            return day
        day += dt.timedelta(days=1)
    return day


def add_class_days(classroom, day, n, skips=None):
    """The class day n class days after (n > 0) or before (n < 0) day."""
    days, skips = class_days(classroom), _skips(classroom) if skips is None else skips
    step = 1 if n >= 0 else -1
    left = abs(n)
    while left:
        day += dt.timedelta(days=step)
        if day.weekday() in days and day not in skips:
            left -= 1
    return day


def unit_topics(unit, course):
    """The lessons of a unit this course teaches, in order: AB leaves out BC-only topics, and a topic taught in two
    versions (6.14) contributes the one for this course."""
    u = next((u for u in content.syllabus() if u["n"] == unit), None)
    if u is None:
        return []
    have = content.available()
    out = []
    for t in u["topics"]:
        if t["n"] not in have:
            continue
        if course == "AB" and t["bc"] and not (t["twin"] and t["ab"]):
            continue
        if course == "BC" and t["twin"] and t["ab"]:
            continue
        out.append(t["n"])
    return out


def plan_unit(classroom, unit, start, pace=1, review=True):
    """Lay a unit onto the calendar from its first class day: one lesson every `pace` class days. Only the work the
    class setup puts on a schedule gets a date: a lesson opens on its day when notes open on a schedule; practice is
    due two class days later and the quiz the next class day, when they have due dates. Then a review day (or not)
    and the unit test. Re-planning a unit replaces its dates. Returns the Dated rows written."""
    skips = _skips(classroom)
    day = class_day_on_or_after(classroom, start, skips)
    rows = []

    def put(kind, ref, opens=None, due=None):
        d, _ = Dated.objects.update_or_create(classroom=classroom, kind=kind, ref=ref,
                                              defaults={"opens": opens, "due": due})
        rows.append(d)

    sets = {k: S.settings_for(classroom, k) for k in S.KINDS}
    topics = unit_topics(unit, classroom.course)
    for i, num in enumerate(topics):
        if i:
            day = add_class_days(classroom, day, pace, skips)
        if sets["notes"]["where"] != "off" and sets["notes"]["opens"] == "schedule":
            put("notes", num, opens=at(classroom, day, OPEN_AT),
                due=at(classroom, add_class_days(classroom, day, 1, skips), DUE_AT) if sets["notes"]["dates"] == "dated" else None)
        if sets["practice"]["where"] != "off" and (sets["practice"]["dates"] == "dated" or sets["practice"]["opens"] == "schedule"):
            put("practice", num, opens=at(classroom, day, OPEN_AT) if sets["practice"]["opens"] == "schedule" else None,
                due=at(classroom, add_class_days(classroom, day, 2, skips), DUE_AT) if sets["practice"]["dates"] == "dated" else None)
        if sets["quiz"]["where"] != "off" and (sets["quiz"]["dates"] == "dated" or sets["quiz"]["opens"] == "schedule"):
            qday = add_class_days(classroom, day, 1, skips)
            put("quiz", num, opens=at(classroom, day, OPEN_AT) if sets["quiz"]["opens"] == "schedule" else None,
                due=at(classroom, qday, DUE_AT) if sets["quiz"]["dates"] == "dated" else None)
    test = content.pick_test(unit, classroom.course)
    ut = sets["unittest"]
    if test and topics and ut["where"] != "off" and (ut["opens"] == "schedule" or ut["dates"] == "dated"):
        tday = add_class_days(classroom, day, 2 if review else 1, skips)
        put("unittest", test["num"], opens=at(classroom, tday, OPEN_AT) if sets["unittest"]["opens"] == "schedule" else None,
            due=at(classroom, tday, DUE_AT) if sets["unittest"]["dates"] == "dated" else None)
    return rows


def shift(classroom, since, n):
    """Move every open and due date on or after `since` by n class days (a snow day: n = 1). Returns how many rows moved."""
    skips = _skips(classroom)
    moved = 0
    for d in Dated.objects.filter(classroom=classroom):
        changed = False
        for f in ("opens", "due", "late_until"):
            v = getattr(d, f)
            if v is None:
                continue
            local = v.astimezone(zone(classroom))
            if local.date() >= since:
                new_day = add_class_days(classroom, class_day_on_or_after(classroom, local.date(), skips), n, skips)
                setattr(d, f, local.replace(year=new_day.year, month=new_day.month, day=new_day.day))
                changed = True
        if changed:
            d.save()
            moved += 1
    return moved


def copy_from(target, source):
    """Copy another class's setup and calendar (dates only; no student exceptions). Returns rows copied."""
    from .models import Setup
    s = S.class_setup(source)
    if s.pk:
        Setup.objects.update_or_create(classroom=target, defaults={"kinds": s.kinds, "units": s.units, "show": s.show,
                                                                    "watch": s.watch, "days": s.days, "tz": s.tz})
    n = 0
    for d in Dated.objects.filter(classroom=source):
        Dated.objects.update_or_create(classroom=target, kind=d.kind, ref=d.ref,
                                       defaults={"opens": d.opens, "due": d.due, "late_until": d.late_until, "settings": d.settings})
        n += 1
    for ns in NoSchool.objects.filter(classroom=source):
        NoSchool.objects.get_or_create(classroom=target, day=ns.day, defaults={"note": ns.note})
    target.__dict__.pop("_setup_cache", None)
    return n


def label(kind, ref):
    if kind == "unittest":
        return content.test_label(ref)
    if kind == "exam":
        return f"Practice exam {ref.upper()}"
    name = content.label(ref) if ref[:1].isdigit() else ref
    return {"notes": f"{name} notes", "practice": f"{name} practice", "quiz": f"Quiz {name}",
            "testprep": f"{name} test prep"}.get(kind, name)


def events(classroom, first, last):
    """{date: [event]} for the days first..last: each open and due on the calendar, in the class's time zone."""
    out = {}
    tz = zone(classroom)
    for d in Dated.objects.filter(classroom=classroom).prefetch_related("exceptions"):
        for what, moment in (("opens", d.opens), ("due", d.due)):
            if moment is None:
                continue
            day = moment.astimezone(tz).date()
            if first <= day <= last:
                if what == "opens" and d.kind in ("practice", "quiz") and d.due is not None:
                    continue            # a quiz or practice that opens with its lesson shows once, on its due day
                if what == "opens" and d.kind in ("unittest", "exam") and d.due is not None and d.due.astimezone(tz).date() == day:
                    continue            # a test that opens and closes the same day shows once
                out.setdefault(day, []).append({"d": d, "what": what, "kind": d.kind, "ref": d.ref,
                                                "text": label(d.kind, d.ref) + (" opens" if what == "opens" and d.kind == "notes" else
                                                                                 " due" if what == "due" and d.kind != "unittest" else ""),
                                                "exceptions": d.exceptions.count()})
    order = {"unittest": 0, "notes": 1, "quiz": 2, "practice": 3, "exam": 4, "testprep": 5}
    for v in out.values():
        v.sort(key=lambda e: (order.get(e["kind"], 9), e["ref"]))
    return out
