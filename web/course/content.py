"""Loads lesson JSON written by ../build.py --web. Public half goes to the page; private half stays here."""
import json
import re
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent


from accounts.models import FREE_UNITS  # noqa: E402


@lru_cache(maxsize=None)
def syllabus():
    """Units and their topics, each with its display names. A unit marked "module" (the trig review) is a standalone
    free module: it is never called a unit, and its lessons show as T1, T2, ... (Adder, 2026-10-08)."""
    out = json.loads((HERE / "syllabus.json").read_text())
    for u in out:
        u["module"] = u.get("module", False)
        u["free"] = u["n"] in FREE_UNITS
        u["short"] = u["title"] if u["module"] else f"Unit {u['n']}"
        u["heading"] = u["title"] if u["module"] else f"Unit {u['n']}. {u['title']}"
        u["line"] = f"{u['title']} · free module" if u["module"] else f"Unit {u['n']} · {u['title']}"
        for t in u["topics"]:
            t["label"] = f"{u['title'][0]}{t['n'].split('.')[1]}" if u["module"] else t.get("label", t["n"])
            # a topic taught in two versions (6.14 AB and 6.14 BC; docs/ab-bc-versions.md): "short" is the number the
            # course map and the menu show beside an AB or BC tag; elsewhere the full label says which version it is
            t["ab"] = t.get("ab", False)
            t["twin"] = t.get("twin")
            t["short"] = t["label"].split(" ")[0]
            t["tag"] = ("AB" if t["ab"] else "BC") if t["twin"] else ("BC" if t["bc"] and not u["bc"] else "")
    return out


def label(num):
    """The number a student sees for a lesson: "2.1", or "T3" for a module lesson."""
    for u in syllabus():
        for t in u["topics"]:
            if t["n"] == num:
                return t["label"]
    return num


def slug(num):
    return num.replace(".", "_")


def _load(num):
    p = HERE / "content" / f"{slug(num)}.json"
    if not p.exists():
        return None
    return _read(p, p.stat().st_mtime)     # keyed by mtime so a rebuilt lesson shows up without a restart


@lru_cache(maxsize=256)
def _read(path, mtime):
    return json.loads(path.read_text())


def available():
    return {p.stem.replace("_", ".") for p in (HERE / "content").glob("*.json") if not p.stem.startswith("U")}


_TEST = re.compile(r"U(\d{1,2})(BC)?")


def test_nums():
    """Every built unit test: "U1" ... "U10", and "U6BC", "U7BC", "U8BC" for units tested in two versions."""
    return {p.stem for p in (HERE / "content").glob("U*.json") if _TEST.fullmatch(p.stem)}


def unit_tests():
    """The units that have a unit test (in one version or two)."""
    return {int(_TEST.fullmatch(n)[1]) for n in test_nums()}


def test_versions(unit):
    """A unit's tests, AB first: [{"num": "U6", "course": "AB"}, {"num": "U6BC", "course": "BC"}] for Units 6-8, where
    the AB test leaves out the BC-only topics and the BC test covers the whole unit; [{"num": "U4", "course": ""}] for
    a unit with one test (Units 9-10 are BC-only units, but their one test needs no tag)."""
    have = test_nums()
    out = [{"num": f"U{unit}", "course": ""}] if f"U{unit}" in have else []
    if f"U{unit}BC" in have:
        for t in out:
            t["course"] = "AB"
        out.append({"num": f"U{unit}BC", "course": "BC"})
    return out


def unit_of_test(num):
    m = _TEST.fullmatch(num)
    return int(m[1]) if m else None


def test_course(num):
    """ "AB" or "BC" for a test of a unit tested in two versions, else ""."""
    m = _TEST.fullmatch(num)
    if not m:
        return ""
    return next((v["course"] for v in test_versions(int(m[1])) if v["num"] == num), "")


def test_label(num):
    """What a unit test is called: "Unit 4 test", "Unit 6 AB test", "Unit 6 BC test", "Trig Review test"."""
    m = _TEST.fullmatch(num)
    if not m:
        return num
    unit = next((u for u in syllabus() if u["n"] == int(m[1])), None)
    course = test_course(num)
    return f"{unit['short'] if unit else 'Unit ' + m[1]}{' ' + course if course else ''} test"


def pick_test(unit, course):
    """The unit test a student should land on: the version for their course ("AB" or "BC"), else the first."""
    vs = test_versions(unit)
    return next((v for v in vs if v["course"] == course), vs[0] if vs else None)


def public(num):
    d = _load(num)
    return d and d["public"]


def private(num):
    d = _load(num)
    return d and d["private"]


def topic_meta(num):
    for u in syllabus():
        for t in u["topics"]:
            if t["n"] == num:
                return u, t
    return None, None


def neighbours(num, course=None):
    """The previous and next *written* lessons, as {"n", "title", "label"} dicts (or None).

    A topic taught in two versions (6.14 AB, 6.14 BC) is one stop on the way: arriving, a BC lesson leads to the BC
    version and any other lesson to the AB one, and leaving either version skips its twin. course ("AB" or "BC", a
    class's course) overrides the current lesson's own tag in both choices, and in which unit test the last lesson
    of a unit leads to."""
    have = available()
    unit, meta = topic_meta(num)
    mine = course or ("BC" if meta and meta["bc"] else "AB")
    # a module stands alone: its lessons link to each other, and the course's lessons skip over it
    flat = [{"n": t["n"], "title": t["title"], "label": t["label"], "twin": t["twin"], "ab": t["ab"]}
            for u in syllabus() for t in u["topics"]
            if (t["n"] in have or t["n"] == num) and (u["module"] == (unit or {}).get("module", False))
            and (not u["module"] or u["n"] == unit["n"])]
    names = [t["n"] for t in flat]
    i = names.index(num)
    twin = meta and meta["twin"]
    before = [t for t in flat[:i] if t["n"] != twin]
    after = [t for t in flat[i + 1:] if t["n"] != twin]
    if after and after[0]["twin"] in names:         # arriving at a two-version topic: the version for this course
        pair = [after[0], next(t for t in after if t["n"] == after[0]["twin"])]
        after = [next(t for t in pair if t["ab"] == (mine != "BC"))] + [t for t in after if t not in pair]
    prev, nxt = (before[-1] if before else None), (after[0] if after else None)
    if prev and prev["twin"] in names:              # coming back to one: the version for this course
        prev = next((t for t in flat if t["n"] in (prev["n"], prev["twin"]) and t["ab"] == (mine != "BC")), prev)
    # the last lesson of a unit leads to that unit's test, not into the next unit (Adder 2026-10-14)
    if unit and (nxt is None or nxt["n"].split(".")[0] != num.split(".")[0]) and unit["n"] in unit_tests():
        t = pick_test(unit["n"], mine)
        nxt = {"n": t["num"], "title": test_label(t["num"]), "label": "Test", "test": True}
    return prev, nxt


def counts(num):
    """How many gradable things each area has, for progress bars."""
    p = public(num)
    if p and num.startswith("U"):
        return {"quiz": len(p["quiz"]), "frq_points": sum(f["points"] for f in p["frq"])}
    if not p:
        return {}
    return {"steps": len(p["steps"]), "practice": len(p["practice"]), "quiz": len(p["quiz"]),
            "mcq": len(p["mcq"]), "frq_points": sum(f["points"] for f in p["frq"])}
