"""The AP FRQ Archive (/frq/): College Board released free-response questions, sorted by question type.

The files come from Adder's old archive at adderoaks.com/calcfrq/. tools/fetch_frq_archive.py mirrors it and
tools/build_frq_archive.py writes build/frq/manifest.json, the page images and the PDFs. This module only reads that
manifest; nothing here is in git or in the database. With no manifest the archive shows as empty, not broken.
"""
import json
import re
from functools import lru_cache

from django.conf import settings

# slug, folder name in the old archive, display name, short blurb, lesson topics where the match is clear
CATEGORIES = [
    ("table", "TABLE", "Table",
     "A table of values: estimate a derivative, a Riemann or trapezoidal sum, use the MVT or IVT.",
     ["2.3", "6.2", "5.1", "1.16", "8.1"]),
    ("rate-accumulation", "RATE-ACCUMULATION", "Rate and Accumulation",
     "A rate in and a rate out: how much has built up, and when there is the most.",
     ["6.1", "6.4", "6.7", "8.3"]),
    ("particle-motion", "PARTICLE-MOTION", "Particle Motion",
     "A particle on a line: when it speeds up, how far it travels and where it ends.",
     ["4.2", "8.2"]),
    ("graph-analysis", "GRAPH-ANALYSIS", "Graph Analysis",
     "A graph of f′ and the function built from it: where that function peaks and how it bends.",
     ["5.3", "5.4", "5.6", "6.5"]),
    ("differential-equations", "DIFFERENTIAL-EQUATION", "Differential Equations",
     "A slope field, then a particular solution by separating variables.",
     ["7.3", "7.4", "4.6", "7.7"]),
    ("miscellaneous", "MISCELLANEOUS", "Miscellaneous",
     "Everything else, from areas and volumes to implicit differentiation and related rates.",
     []),
    ("bc-only", "BC-ONLY", "BC Only",
     "Parametric, polar and series questions, on the BC exam only.",
     []),
]
BY_SLUG = {c[0]: c for c in CATEGORIES}
BY_FOLDER = {c[1]: c for c in CATEGORIES}

# BC-only questions point at Unit 9 or Unit 10 by what the question is about
BC_TOPICS = [
    (re.compile(r"\bpolar\b|r\s*=\s*f\s*\(\s*θ|\bθ\b", re.I), ["9.7", "9.8", "9.9"]),
    (re.compile(r"\bTaylor|Maclaurin|\bseries\b|radius of convergence|interval of convergence", re.I),
     ["10.11", "10.13", "10.14"]),
    (re.compile(r"\bparametric|x\s*\(\s*t\s*\)|position vector|velocity vector|\bxy-plane\b", re.I), ["9.1", "9.6"]),
]
BC_EXTRA = [(re.compile(r"Euler", re.I), ["7.5"]), (re.compile(r"logistic", re.I), ["7.9"]),
            (re.compile(r"integration by parts", re.I), ["6.11"]), (re.compile(r"improper", re.I), ["6.13"])]


def frq_dir():
    return settings.FRQ_DIR


def _manifest_path():
    return frq_dir() / "manifest.json"


def questions():
    p = _manifest_path()
    if not p.is_file():
        return []
    return _load(str(p), p.stat().st_mtime)


@lru_cache(maxsize=2)
def _load(path, mtime):
    data = json.loads(open(path, encoding="utf-8").read())
    out = []
    for q in data["questions"]:
        q = {**q, "text": _tidy(q["text"])}
        cats = [BY_FOLDER[c] for c in q["categories"] if c in BY_FOLDER]
        cat = cats[0] if cats else None
        out.append({
            "id": q["id"], "year": q["year"], "exam": q["exam"], "number": q["number"], "exams": q["exams"],
            "cat": cat and cat[0], "cat_name": cat[2] if cat else "Not sorted yet",
            "label": f"{q['exam']} Question {q['number']}" + (" (Form B)" if q.get("form") else ""),
            "form": q.get("form", ""),
            "also": _also(q),
            "text": q["text"], "search": _fold(q["text"]),
            "question_pages": q["question_pages"], "guideline_pages": q["guideline_pages"],
            "pdf": q["pdf"], "pdf_size": q["pdf_size"],
        })
    return out


# older PDFs set math in the Symbol font, which extracts as Latin-1 look-alikes: £ is <=, ³ is >=, ¢ is a prime
_SYMBOL = str.maketrans({"\u00a3": "\u2264", "\u00b3": "\u2265", "\u00a2": "\u2032", "\u2014": "-"})


def _tidy(text):
    """Search and list text: the PDF's em dashes (section headers) become hyphens, Symbol-font stand-ins their symbols."""
    return text.translate(_SYMBOL)


def _also(q):
    """'Also on the BC exam' for a question that was on both exams (from 2017, when the scoring guidelines say so)."""
    if len(q["exams"]) < 2:
        return ""
    other = "BC" if q["exam"] == "AB" else "AB"
    return f"Also on the {other} exam"


def _fold(s):
    return re.sub(r"\s+", " ", s).lower()


def get(qid):
    return next((q for q in questions() if q["id"] == qid), None)


def years():
    ys = sorted({q["year"] for q in questions()})
    return ys


def lessons_for(q, available):
    """Course lessons that teach what this question asks, as topic numbers that exist on the site."""
    nums = []
    if q["cat"]:
        nums = list(BY_SLUG[q["cat"]][4])
    if q["cat"] == "bc-only" or "BC" in q["exams"] and not nums:
        for rx, ns in BC_TOPICS:
            if rx.search(q["text"]):
                nums += ns
                break
    if q["cat"] in ("bc-only", "differential-equations"):
        for rx, ns in BC_EXTRA:
            if rx.search(q["text"]):
                nums += ns
    seen = []
    for n in nums:
        if n in available and n not in seen:
            seen.append(n)
    return seen


def filtered(cat=None, exam="", year_from=None, year_to=None, text=""):
    out = []
    words = [w for w in _fold(text).split() if w]
    for q in questions():
        if cat and q["cat"] != cat:
            continue
        if exam and exam not in q["exams"]:
            continue
        if year_from and q["year"] < year_from:
            continue
        if year_to and q["year"] > year_to:
            continue
        if words and not all(w in q["search"] for w in words):
            continue
        out.append(q)
    return out


def snippet(q, text="", width=170):
    """A line of the question for the list: the opening of its stem, or the part around the first search word."""
    flat = re.sub(r"\s+", " ", q["text"]).strip()
    # the stem starts at "3. A student ..."; table cells and section headers often come out of the PDF first
    m = re.search(rf"(?<![\d.]){q['number']}\.\s+(?=[A-Z])", flat)
    if m:
        flat = flat[m.end():]
    words = [w for w in _fold(text).split() if w]
    if words:
        i = flat.lower().find(words[0])
        if i > 60:
            start = flat.rfind(" ", 0, i - 50) + 1
            piece = flat[start:start + width]
            return "…" + piece.rsplit(" ", 1)[0] + "…"
    if len(flat) <= width:
        return flat
    return flat[:width].rsplit(" ", 1)[0] + "…"


def categories_for_topic(num):
    """The question types a lesson prepares for, for the link on its AP test prep tab: the clear matches above,
    plus all of Unit 7 for differential equations and Units 9 and 10 for the BC-only questions."""
    unit = num.split(".")[0]
    slugs = [c[0] for c in CATEGORIES if num in c[4]]
    if unit == "7" and "differential-equations" not in slugs:
        slugs.append("differential-equations")
    if unit in ("9", "10"):
        slugs.append("bc-only")
    counts = {}
    for q in questions():
        counts[q["cat"]] = counts.get(q["cat"], 0) + 1
    return [{"slug": s, "name": BY_SLUG[s][2], "count": counts.get(s, 0)} for s in slugs if counts.get(s)]
