#!/usr/bin/env python3
"""Build the AP FRQ Archive (/frq/) from the PDFs tools/fetch_frq_archive.py mirrored into build/frq/raw/.

Run in the `calc` env (needs pymupdf and Pillow):

    ~/opt/mamba/envs/calc/bin/python tools/build_frq_archive.py

Writes, under build/frq/ (gitignored, rsynced to the server like build/pdf/):

    manifest.json        one record per question: category, year, exam(s), number, source files with size and
                         sha256, which PDF pages are the question and which the scoring guidelines, page images,
                         and the question text for search
    files/<id>/q1.webp   the question pages, rendered
    files/<id>/s1.webp   the scoring guideline pages, rendered
    files/<id>/<id>.pdf  the original PDF (question and scoring guidelines), for download

files/ is the only public part: the site serves it at /frq/file/ (nginx straight off disk in production).

Every source PDF is the College Board question followed by its scoring guidelines. A page is a scoring guideline
page when its header says "Scoring Guidelines" (every year 2002-2025 does). Anything that doesn't parse is listed
at the end and in manifest["problems"].
"""
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

import pymupdf
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
FRQ = REPO / "build" / "frq"
RAW = FRQ / "raw"
SCALE = 2.0             # 612pt wide page -> 1224px image: sharp on a phone, crisp at 1280 wide
CATEGORIES = ["TABLE", "RATE-ACCUMULATION", "PARTICLE-MOTION", "GRAPH-ANALYSIS",
              "DIFFERENTIAL-EQUATION", "MISCELLANEOUS", "BC-ONLY"]

CAT_FILE = re.compile(r"(?P<cat>[A-Z-]+)/(?P<year>\d{4})-(?P<exam>AB|BC)-Q(?P<n>\d)\.pdf")
SET_FILE = re.compile(r"_(?P<exam>AB|BC)/(?P<year>\d{4})/Q(?P<n>\d)\.pdf")
SG_HEAD = re.compile(r"scoring\s+guidelines?", re.I)
# "AP CALCULUS AB/CALCULUS BC 2017 SCORING GUIDELINES", "AP Calculus AB/BC 2025 Scoring Guidelines"
SHARED = re.compile(r"calculus\s+ab\s*/\s*(calculus\s+)?bc", re.I)
PART = re.compile(r"Part\s+[AB]\s*\((AB or BC|AB|BC)\)")
FORM_B = re.compile(r"\(Form\s*B\)", re.I)
BOILER = re.compile(r"(©|Copyright).*?$|Visit (the )?College Board on the (W|w)eb.*?$|GO ON TO THE NEXT PAGE\.?|"
                    r"Available (to AP professionals )?at .*?$|.*FREE-RESPONSE QUESTIONS.*?$|"
                    r"AP®? CALCULUS (AB|BC).*?$|-\d+-|\bWRITE ALL WORK IN THE (EXAM|PINK) BOOKLET\.?", re.M | re.I)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def clean_text(t):
    t = BOILER.sub(" ", t)
    t = re.sub(r"[ \t ]+", " ", t)
    t = re.sub(r"\s*\n\s*", "\n", t).strip()
    return t


def render(page, dest):
    pix = page.get_pixmap(matrix=pymupdf.Matrix(SCALE, SCALE), alpha=False)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    img.save(dest, "WEBP", quality=82, method=6)
    return {"file": dest.name, "w": pix.width, "h": pix.height}


def reuse(path):
    with Image.open(path) as img:
        return {"file": path.name, "w": img.width, "h": img.height}


def exams_for(exam, sg_text):
    """Which exams a question was on. From 2021 one combined AB/BC scoring document labels each question
    "Part A (AB or BC)", "Part B (AB)" or "Part A (BC)". 2017-2019 headed a shared question "AP CALCULUS AB/CALCULUS
    BC". Before that each exam had its own scoring document, so a shared question can't be told apart: exam only."""
    parts = PART.findall(sg_text)
    if parts:
        return ["AB", "BC"] if "AB or BC" in parts else [parts[0]]
    return ["AB", "BC"] if SHARED.search(sg_text) else [exam]


def main():
    if not RAW.is_dir():
        sys.exit(f"{RAW} is missing: run tools/fetch_frq_archive.py first")
    problems = []
    pdfs = sorted(p.relative_to(RAW).as_posix() for p in RAW.rglob("*.pdf"))
    # 1. parse every file name; group the files that are the same question (a category copy and an exam-set copy)
    qs = {}
    for rel in pdfs:
        m = CAT_FILE.fullmatch(rel) or SET_FILE.fullmatch(rel)
        if not m or (m.re is CAT_FILE and m["cat"] not in CATEGORIES):
            problems.append(f"{rel}: name doesn't match either scheme")
            continue
        qid = f"{m['year']}-{m['exam'].lower()}-{m['n']}"
        q = qs.setdefault(qid, {"id": qid, "year": int(m["year"]), "exam": m["exam"], "number": int(m["n"]),
                                "categories": [], "sources": []})
        path = RAW / rel
        q["sources"].append({"path": rel, "size": path.stat().st_size, "sha256": sha256(path)})
        if m.re is CAT_FILE:
            q["categories"].append(m["cat"])
    # 2. split each question's PDF into question pages and scoring-guideline pages, render, extract text
    out_pages = FRQ / "files"
    out_pages.mkdir(parents=True, exist_ok=True)
    for stale in {p.name for p in out_pages.iterdir()} - set(qs):
        shutil.rmtree(out_pages / stale)
    for qid, q in sorted(qs.items()):
        shas = {s["sha256"] for s in q["sources"]}
        if len(shas) > 1:
            problems.append(f"{qid}: copies differ ({', '.join(s['path'] for s in q['sources'])}); using the first")
        if len(q["categories"]) > 1:
            problems.append(f"{qid}: in more than one category ({', '.join(q['categories'])})")
        if not q["categories"]:
            problems.append(f"{qid}: in no category folder (exam set only)")
        src = RAW / q["sources"][0]["path"]
        doc = pymupdf.open(src)
        kinds = []
        for page in doc:
            head = page.get_text()[:400]
            kinds.append("s" if SG_HEAD.search(head) else "q")
        if "s" not in kinds:
            problems.append(f"{qid}: no scoring guidelines in the file ({len(kinds)} page(s), the question only)")
        if kinds[0] != "q":
            problems.append(f"{qid}: first page isn't the question")
        # a "q" page after the guidelines start would be odd: report it, keep it with the guidelines
        first_s = kinds.index("s") if "s" in kinds else len(kinds)
        if "q" in kinds[first_s:]:
            problems.append(f"{qid}: a question page after the scoring guidelines (pages {kinds})")
        d = out_pages / qid
        d.mkdir(exist_ok=True)
        # pages are only re-rendered when the source PDF changed (rendering all of them takes several minutes)
        stamp = d / ".source-sha256"
        fresh = stamp.is_file() and stamp.read_text() == q["sources"][0]["sha256"]
        if not fresh:
            for old in d.iterdir():
                old.unlink()
        names = [f"q{i + 1}.webp" for i in range(first_s)] + [f"s{i - first_s + 1}.webp" for i in range(first_s, len(kinds))]
        pages = [reuse(d / n) if fresh and (d / n).is_file() else render(doc[i], d / n) for i, n in enumerate(names)]
        q["question_pages"], q["guideline_pages"] = pages[:first_s], pages[first_s:]
        stamp.write_text(q["sources"][0]["sha256"])
        text = "\n".join(doc[i].get_text() for i in range(first_s))
        sg_text = " ".join(doc[i].get_text()[:400] for i in range(first_s, len(kinds)))
        q["exams"] = exams_for(q["exam"], sg_text)
        q["form"] = "B" if FORM_B.search(text[:600]) else ""
        q["text"] = clean_text(text)
        if len(q["text"]) < 80:
            problems.append(f"{qid}: little or no question text ({len(q['text'])} characters), search won't find it")
        q["pdf"] = f"{qid}.pdf"
        shutil.copyfile(src, d / q["pdf"])
        q["pdf_size"] = src.stat().st_size
        doc.close()
        print(f"  {qid:12} {','.join(q['categories']) or '-':22} {''.join(kinds)}  {'/'.join(q['exams'])}")
    manifest = {"source": "https://adderoaks.com/calcfrq/", "categories": CATEGORIES,
                "questions": sorted(qs.values(), key=lambda q: (-q["year"], q["exam"], q["number"])),
                "problems": problems}
    (FRQ / "manifest.json").write_text(json.dumps(manifest, indent=1))
    n_q = len(qs)
    print(f"\n{n_q} questions from {len(pdfs)} files -> {FRQ / 'manifest.json'}")
    for c in CATEGORIES:
        print(f"  {c:22} {sum(c in q['categories'] for q in qs.values())}")
    if problems:
        print(f"\n{len(problems)} notes:")
        print("\n".join("  " + p for p in problems))


if __name__ == "__main__":
    main()
