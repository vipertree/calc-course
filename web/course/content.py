"""Loads lesson JSON written by ../build.py --web. Public half goes to the page; private half stays here."""
import json
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent


@lru_cache(maxsize=None)
def syllabus():
    """Units and their topics, each with its display names. A unit marked "module" (the trig review) is a standalone
    free module: it is never called a unit, and its lessons show as T1, T2, ... (Adder, 2026-10-08)."""
    out = json.loads((HERE / "syllabus.json").read_text())
    for u in out:
        u["module"] = u.get("module", False)
        u["short"] = u["title"] if u["module"] else f"Unit {u['n']}"
        u["heading"] = u["title"] if u["module"] else f"Unit {u['n']}. {u['title']}"
        u["line"] = f"{u['title']} · free module" if u["module"] else f"Unit {u['n']} · {u['title']}"
        for t in u["topics"]:
            t["label"] = f"{u['title'][0]}{t['n'].split('.')[1]}" if u["module"] else t["n"]
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


def unit_tests():
    return {int(p.stem[1:]) for p in (HERE / "content").glob("U*.json")}


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


def neighbours(num):
    """The previous and next *written* lessons, as {"n", "title"} dicts (or None)."""
    have = available()
    unit, _ = topic_meta(num)
    # a module stands alone: its lessons link to each other, and the course's lessons skip over it
    flat = [{"n": t["n"], "title": t["title"], "label": t["label"]} for u in syllabus() for t in u["topics"]
            if (t["n"] in have or t["n"] == num) and (u["module"] == (unit or {}).get("module", False))
            and (not u["module"] or u["n"] == unit["n"])]
    i = [t["n"] for t in flat].index(num)
    return (flat[i - 1] if i > 0 else None), (flat[i + 1] if i + 1 < len(flat) else None)


def counts(num):
    """How many gradable things each area has, for progress bars."""
    p = public(num)
    if p and num.startswith("U"):
        return {"quiz": len(p["quiz"]), "frq_points": sum(f["points"] for f in p["frq"])}
    if not p:
        return {}
    return {"steps": len(p["steps"]), "practice": len(p["practice"]), "quiz": len(p["quiz"]),
            "mcq": len(p["mcq"]), "frq_points": sum(f["points"] for f in p["frq"])}
