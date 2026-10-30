"""What a class's setup and calendar mean for one student and one piece of work, right now.

gate(user, kind, ref) answers: may they open it, is it closed, is it done on paper or not used in their class, when
is it due for them (their own exception first), is it late, and may they see results. Students outside a class, and
teachers, always get an open gate: their use of the site is unchanged.
"""
import datetime as dt

from accounts.models import class_for

from . import setup as S
from .models import Dated, StudentException

OPEN = {"state": "open", "classroom": None, "due": None, "opens": None, "late": False, "excused": False,
        "results": "now", "attempts": "best", "where": "site", "record": "", "late_rule": "marked"}


def _dated(classroom, kind, ref):
    return Dated.objects.filter(classroom=classroom, kind=kind, ref=ref).first()


def gate(user, kind, ref, now=None):
    c = class_for(user)
    if c is None:
        return dict(OPEN)
    now = now or dt.datetime.now(dt.timezone.utc)
    d = _dated(c, kind, ref)
    st = S.settings_for(c, kind, ref, d)
    exc = StudentException.objects.filter(dated=d, student=user).first() if d else None
    out = {"classroom": c, "results": st.get("results", "now"), "attempts": st.get("attempts", "one"),
           "where": st["where"], "record": st.get("record", ""), "late_rule": st.get("late", "marked"),
           "excused": bool(exc and exc.excused), "time_factor": exc.time_factor if exc else 1.0, "dated": d}

    # when it opens
    opens = None
    if st.get("opens") == "schedule" and d is not None:
        opens = d.opens
    elif st.get("opens") == "lesson":
        notes = _dated(c, "notes", ref)
        if notes is not None and S.settings_for(c, "notes", ref, notes).get("opens") == "schedule":
            opens = notes.opens
    # when it's due, for this student
    due = (exc.due if exc and exc.due else d.due) if d is not None and st.get("dates") == "dated" else None
    late_until = (exc.late_until if exc and exc.late_until else d.late_until) if d is not None else None
    out.update(opens=opens, due=due, late_until=late_until)

    if st["where"] == "off":
        out["state"] = "off"
    elif st["where"] == "paper" and kind in ("quiz", "unittest", "exam"):
        out["state"] = "paper"
    elif opens is not None and now < opens and not (exc and exc.reopened):
        out["state"] = "not_yet"
    elif due is not None and now > due and not (exc and exc.reopened):
        locked = st.get("late") == "lock" or (late_until is not None and now > late_until)
        out["state"] = "closed" if locked else "open"
        out["late"] = not locked
    else:
        out["state"] = "open"
    return out


def results_visible(user, kind, num, g=None):
    """May this class student see scores and solutions for their quiz or unit test? Individual users always may."""
    g = g or gate(user, kind, num)
    c = g["classroom"]
    if c is None:
        return True
    if g["results"] == "now":
        return True
    if g["results"] == "due":
        return g["due"] is not None and dt.datetime.now(dt.timezone.utc) > g["due"]
    from course.models import Release
    return Release.objects.filter(classroom=c, topic=num).exists()


def kind_for(num, area):
    if str(num).startswith("U"):
        return "unittest"
    return {"notes": "notes", "practice": "practice", "quiz": "quiz", "testprep": "testprep", "frq": "testprep"}.get(area, "notes")
