"""The AP FRQ Archive pages (/frq/). Free for everyone, no account. Data: course/frq.py."""
import re

from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import render

from . import content, frq

_FILE = re.compile(r"(?:[qs]\d{1,2}\.webp|\d{4}-(?:ab|bc)-\d\.pdf)")
_TYPES = {".webp": "image/webp", ".pdf": "application/pdf"}


def _year(v):
    try:
        y = int(v)
    except (TypeError, ValueError):
        return None
    return y if 1990 <= y <= 2100 else None


def _filters(request):
    g = request.GET
    exam = g.get("exam", "").upper()
    f = {"exam": exam if exam in ("AB", "BC") else "", "year_from": _year(g.get("from")),
         "year_to": _year(g.get("to")), "text": g.get("q", "").strip()[:80]}
    if f["year_from"] and f["year_to"] and f["year_from"] > f["year_to"]:
        f["year_from"], f["year_to"] = f["year_to"], f["year_from"]
    return f


def index(request, cat=None):
    if not settings.FRQ_ARCHIVE:
        raise Http404
    if cat and cat not in frq.BY_SLUG:
        raise Http404("There's no question type by that name.")
    f = _filters(request)
    active = any(f.values())
    everything = frq.filtered(**f)
    cats = [{"slug": c[0], "name": c[2], "blurb": c[3], "on": c[0] == cat,
             "count": sum(q["cat"] == c[0] for q in everything)} for c in frq.CATEGORIES]
    shown = [q for q in everything if not cat or q["cat"] == cat]
    rows = [{**q,  # a copy: the cached dicts stay untouched
             "snippet": frq.snippet(q, f["text"])} for q in shown]
    groups = []
    if cat:
        groups = [{"slug": cat, "name": frq.BY_SLUG[cat][2], "rows": rows}]
    else:
        for c in frq.CATEGORIES:
            r = [q for q in rows if q["cat"] == c[0]]
            if r:
                groups.append({"slug": c[0], "name": c[2], "rows": r})
        loose = [q for q in rows if not q["cat"]]
        if loose:
            groups.append({"slug": "", "name": "Not sorted yet", "rows": loose})
    query = request.GET.urlencode()
    return render(request, "course/frq.html", {
        "cats": cats, "cat": cat and frq.BY_SLUG[cat], "groups": groups, "count": len(rows),
        "matching": len(everything), "built": bool(frq.questions()), "f": f, "active": active, "years": frq.years(), "total": len(frq.questions()), "query": query,
        "page_title": frq.BY_SLUG[cat][2] if cat else "AP FRQ Archive"})


def question(request, qid):
    if not settings.FRQ_ARCHIVE:
        raise Http404
    q = frq.get(qid)
    if not q:
        raise Http404("That question isn't in the archive.")
    have = content.available()
    lessons = []
    for n in frq.lessons_for(q, have):
        _, t = content.topic_meta(n)
        if t:
            lessons.append({"n": n, "label": t["label"], "title": t["title"]})
    same = [x for x in frq.questions() if x["cat"] == q["cat"]]     # newest first
    i = [x["id"] for x in same].index(q["id"])
    newer = same[i - 1] if i > 0 else None
    older = same[i + 1] if i + 1 < len(same) else None
    # Part A (calculator) was questions 1-3 through 2010 and 1-2 from 2011; the section headers in the PDFs agree
    calc = "Part A: graphing calculator required" if q["number"] <= (3 if q["year"] <= 2010 else 2) else "Part B: no calculator"
    return render(request, "course/frq_question.html", {
        "q": q, "cat": q["cat"] and frq.BY_SLUG[q["cat"]], "lessons": lessons, "newer": newer, "older": older,
        "calc": calc, "pdf_kb": round(q["pdf_size"] / 1024)})


def file(request, qid, name):
    if not settings.FRQ_ARCHIVE:
        raise Http404
    """A page image or the original PDF. Public, cacheable; nginx serves the same tree in production."""
    if not _FILE.fullmatch(name) or not frq.get(qid):
        raise Http404
    base = settings.FRQ_DIR.resolve()
    path = (base / "files" / qid / name).resolve()
    if base not in path.parents or not path.is_file() or (name.endswith(".pdf") and name != f"{qid}.pdf"):
        raise Http404
    ext = path.suffix
    resp = FileResponse(open(path, "rb"), content_type=_TYPES[ext])
    if ext == ".pdf":
        resp["Content-Disposition"] = f'inline; filename="AP-Calculus-{qid}.pdf"'
    resp["Cache-Control"] = "public, max-age=604800"
    resp["X-Content-Type-Options"] = "nosniff"
    return resp
