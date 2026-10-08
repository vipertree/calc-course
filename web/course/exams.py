"""Full-length practice exams: loading, access, the server-side clock, grading and the score report.

An exam's JSON (build.py exam-<slug> --web) has four parts: Section I Part A/B (multiple choice) and Section II
Part A/B (free response). A sitting (ExamAttempt) walks them in order and never back:

    waiting on part k  --begin-->  part k running  --submit, or the deadline passes-->  waiting on part k + 1
    ... after the last part the attempt is finished and the multiple choice is graded.

The deadline is part_started + the part's minutes, on the server's clock. The browser's countdown is only a display
of the remaining seconds the server sent; a late answer is refused here whatever the page shows. sync() closes an
expired part the next time anything touches the attempt, so a closed laptop can't hold a part open.

While a sitting is in progress the page receives the current part's questions only: no later part (so the FRQs can't
be read during multiple choice) and no earlier one (it is closed). Answers, solutions, rubrics and topics stay on the
server until the attempt is finished.
"""
import json
from datetime import timedelta
from functools import lru_cache
from pathlib import Path

from django.utils import timezone

from accounts.models import has_full_access

from . import content

HERE = Path(__file__).resolve().parent
DIR = HERE / "content" / "exams"
GRACE = timedelta(seconds=10)       # network slack for an answer sent in the last second


# ------------------------------------------------------------------ loading
def _path(slug):
    return DIR / f"{slug}.json"


def load(slug):
    p = _path(slug)
    if not slug.isalnum() or not p.exists():
        return None
    return _read(p, p.stat().st_mtime)


@lru_cache(maxsize=16)
def _read(path, mtime):
    return json.loads(path.read_text())


def available():
    return sorted(p.stem for p in DIR.glob("*.json")) if DIR.exists() else []


def public(slug):
    d = load(slug)
    return d and d["public"]


def private(slug):
    d = load(slug)
    return d and d["private"]


def can_take(user, pub):
    """The free exam is for anyone signed in; members_only exams need full access (a class, a teacher, or a grant)."""
    if not user.is_authenticated:
        return False
    return not pub.get("members_only") or has_full_access(user)


# ------------------------------------------------------------------ the clock
def parts(pub):
    return pub["parts"]


def done(att, pub):
    return att.part >= len(parts(pub))


def deadline(att, pub):
    if att.part_started is None or done(att, pub):
        return None
    return att.part_started + timedelta(minutes=parts(pub)[att.part]["minutes"])


def remaining(att, pub, now=None):
    d = deadline(att, pub)
    if d is None:
        return None
    return max(0.0, (d - (now or timezone.now())).total_seconds())


def _close(att, pub, now, timed_out):
    """End the running part (or skip a waiting one) and move to the next; finish after the last."""
    key = parts(pub)[att.part]["key"]
    rec = att.timing.get(key, {})
    rec.update({"end": now.isoformat(), "timed_out": timed_out})
    att.timing[key] = rec
    att.part += 1
    att.part_started = None
    if done(att, pub):
        finish(att, pub, now)


def sync(att, pub, now=None):
    """Close the running part if its time is up. Saves when anything changed. Returns the attempt."""
    now = now or timezone.now()
    d = deadline(att, pub)
    if d is not None and now > d:
        att.timing.setdefault(parts(pub)[att.part]["key"], {})
        _close(att, pub, d, True)       # the part ended at its deadline, not when we noticed
        att.save()
    return att


def begin(att, pub, now=None):
    """Start the waiting part. A part already running stays as it is: a reload never restarts the clock."""
    now = now or timezone.now()
    sync(att, pub, now)
    if done(att, pub) or att.part_started is not None:
        return False
    att.part_started = now
    att.timing[parts(pub)[att.part]["key"]] = {"start": now.isoformat()}
    att.save()
    return True


def submit_part(att, pub, part_key, now=None):
    """The student ends the running part early. part_key must name the current part, so a stale page (or a second tab)
    can't end the part after it."""
    now = now or timezone.now()
    sync(att, pub, now)
    if done(att, pub) or att.part_started is None or parts(pub)[att.part]["key"] != part_key:
        return False
    _close(att, pub, now, False)
    att.save()
    return True


def _item_part(pub, item):
    for k, p in enumerate(parts(pub)):
        if any(it["id"] == item for it in p["items"]):
            return k
    return None


def answer(att, pub, item, value, now=None):
    """Record one multiple-choice answer ("" clears it). Refused unless the item is in the running part and the part's
    deadline (plus a few seconds of network slack) hasn't passed. -> (ok, reason)."""
    now = now or timezone.now()
    k = _item_part(pub, item)
    if k is None or parts(pub)[k]["kind"] != "mcq":
        return False, "unknown question"
    if value not in ("", "A", "B", "C", "D"):
        return False, "bad answer"
    d = deadline(att, pub)
    if done(att, pub) or att.part != k or d is None:
        sync(att, pub, now)
        return False, "that part is closed"
    if now > d + GRACE:
        sync(att, pub, now)
        return False, "time is up for this part"
    if value:
        att.answers[item] = value
    else:
        att.answers.pop(item, None)
    att.save(update_fields=["answers"])
    return True, ""


def flag(att, pub, item, on, now=None):
    """Mark a question in the running part for review (or unmark it)."""
    k = _item_part(pub, item)
    sync(att, pub, now)
    if k is None or done(att, pub) or att.part != k or att.part_started is None:
        return False
    fl = [f for f in att.flags if f != item] + ([item] if on else [])
    att.flags = fl
    att.save(update_fields=["flags"])
    return True


# ------------------------------------------------------------------ grading and scoring
def mc_items(pub):
    return [it for p in parts(pub) if p["kind"] == "mcq" for it in p["items"]]


def frq_parts(pub):
    return [pt for p in parts(pub) if p["kind"] == "frq" for q in p["items"] for pt in q["parts"]]


def finish(att, pub, now=None):
    priv = private(att.exam)
    att.mc_score = sum(1 for it in mc_items(pub) if att.answers.get(it["id"]) == priv["items"][it["id"]]["answer"])
    att.finished = now or timezone.now()


def set_frq(att, pub, part_id, checks):
    """The student's own rubric marks for one FRQ part: one bool per scoring line. Only after the exam is over."""
    priv = private(att.exam)
    spec = priv["items"].get(part_id)
    if att.finished is None or not spec or "rubric" not in spec:
        return False
    if not isinstance(checks, list) or len(checks) != len(spec["rubric"]):
        return False
    att.frq[part_id] = [bool(c) for c in checks]
    att.save(update_fields=["frq"])
    return True


def frq_points(att, priv, part_id):
    marks = att.frq.get(part_id)
    if marks is None:
        return None
    return sum(r["points"] for r, m in zip(priv["items"][part_id]["rubric"], marks) if m)


def ap_estimate(composite, cutoffs):
    for score, lo in cutoffs:
        if composite >= lo:
            return score
    return 1


def summary(att, pub):
    """MC raw, FRQ raw, composite and the estimated AP score. Unscored FRQ parts count 0 until the student scores them;
    the page says so."""
    priv = private(att.exam)
    fps = frq_parts(pub)
    scored = [p for p in fps if p["id"] in att.frq]
    frq_raw = sum(frq_points(att, priv, p["id"]) for p in scored)
    mc = att.mc_score or 0
    composite = round(mc * pub["mc_weight"] + frq_raw, 1)
    return {"mc": mc, "mc_total": pub["mc_total"], "frq": frq_raw, "frq_total": pub["frq_total"],
            "frq_parts_scored": len(scored), "frq_parts": len(fps),
            "composite": composite, "composite_total": round(pub["mc_total"] * pub["mc_weight"] + pub["frq_total"]),
            "ap": ap_estimate(composite, pub["cutoffs"]), "cutoffs": pub["cutoffs"]}


def _topic_index():
    out = {}
    for u in content.syllabus():
        for t in u["topics"]:
            out[t["n"]] = (u["n"], u["title"], t["title"])
    return out


def by_unit(att, pub):
    """Per-unit breakdown for the score report: multiple choice right / asked, FRQ points earned / possible (scored
    parts only), and the lessons behind what was missed, each linked when the lesson is written."""
    priv = private(att.exam)
    idx, have = _topic_index(), content.available()
    units = {}

    def unit(topic):
        un, ut, _ = idx[topic]
        return units.setdefault(un, {"n": un, "title": ut, "mc": 0, "mc_total": 0, "frq": 0, "frq_total": 0, "review": {}})

    def miss(u, topic):
        u["review"].setdefault(topic, {"n": topic, "title": idx[topic][2], "ready": topic in have, "missed": 0})["missed"] += 1

    for it in mc_items(pub):
        spec = priv["items"][it["id"]]
        u = unit(spec["topic"])
        u["mc_total"] += 1
        if att.answers.get(it["id"]) == spec["answer"]:
            u["mc"] += 1
        else:
            miss(u, spec["topic"])
    for p in frq_parts(pub):
        got = frq_points(att, priv, p["id"])
        if got is None:
            continue
        spec = priv["items"][p["id"]]
        u = unit(spec["topic"])
        u["frq"] += got
        u["frq_total"] += spec["points"]
        if got < spec["points"]:
            miss(u, spec["topic"])
    out = []
    for un in sorted(units):
        u = units[un]
        u["review"] = sorted(u["review"].values(), key=lambda r: [int(x) for x in r["n"].split(".")])
        out.append(u)
    return out


# ------------------------------------------------------------------ what the page gets
def live_state(att, pub, now=None):
    """The in-progress page's data: where the sitting is, the seconds left on the server's clock, and the current
    part's questions with this student's answers and flags. Nothing from any other part."""
    now = now or timezone.now()
    sync(att, pub, now)
    ps = parts(pub)
    out = {"id": att.pk, "finished": done(att, pub),
           "outline": [{k: p[k] for k in ("key", "section", "name", "kind", "calc", "minutes")} | {"count": len(p["items"])} for p in ps],
           "part": att.part, "running": att.part_started is not None and not done(att, pub)}
    if out["finished"]:
        return out
    cur = ps[att.part]
    out["remaining"] = remaining(att, pub, now)
    if out["running"]:
        ids = {it["id"] for it in cur["items"]}
        out["items"] = cur["items"]
        out["answers"] = {k: v for k, v in att.answers.items() if k in ids}
        out["flags"] = [f for f in att.flags if f in ids]
    return out


def report(att, pub):
    """Everything the finished page shows: each MC with the student's answer, the key and the solution; each FRQ
    with its solutions and rubric and the student's marks; the summary and the per-unit breakdown."""
    priv = private(att.exam)
    idx = _topic_index()
    mcs = []
    for it in mc_items(pub):
        spec = priv["items"][it["id"]]
        given = att.answers.get(it["id"], "")
        mcs.append({**it, "given": given, "key": spec["answer"], "ok": given == spec["answer"], "solution": spec["solution"],
                    "why": spec["why_not"].get(given, ""), "topic": spec["topic"], "topic_title": idx[spec["topic"]][2]})
    frqs = []
    for p in parts(pub):
        if p["kind"] != "frq":
            continue
        for q in p["items"]:
            frqs.append({**q, "parts": [{**pt, "solution": priv["items"][pt["id"]]["solution"], "rubric": priv["items"][pt["id"]]["rubric"],
                                         "marks": att.frq.get(pt["id"]), "topic": priv["items"][pt["id"]]["topic"]} for pt in q["parts"]]})
    return {"id": att.pk, "finished": True, "mc": mcs, "frq": frqs, "summary": summary(att, pub), "units": by_unit(att, pub),
            "timing": att.timing, "outline": [{k: p[k] for k in ("key", "section", "name", "minutes")} for p in parts(pub)]}
