"""Loads lesson JSON written by ../build.py --web. Public half goes to the page; private half stays here."""
import json
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent


@lru_cache(maxsize=None)
def syllabus():
    return json.loads((HERE / "syllabus.json").read_text())


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
    flat = [{"n": t["n"], "title": t["title"]} for u in syllabus() for t in u["topics"] if t["n"] in have or t["n"] == num]
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
