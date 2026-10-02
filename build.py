"""Build printed materials (and later web JSON) for one or more topics.

    python3 build.py 2.1                    # all four documents, student + key, classic theme
    python3 build.py 2.1 --theme modern     # another theme
    python3 build.py 2.1 --docs notes       # just the guided notes
    python3 build.py 2.1 --preview          # also write PNG previews to the scratch dir

The packet (lesson + practice + AP test prep in one PDF) is the base the web app stamps with each
student's name and packet ID on download; build/pdf/fonts/ gets the font that stamp is set in.
"""
import argparse
import importlib
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

import calclib  # noqa: E402
from calclib import latex  # noqa: E402

PREVIEW_DIR = os.environ.get("CALC_PREVIEW", os.path.join(ROOT, "build", "preview"))


def load(num):
    if num.upper().startswith("U"):
        return importlib.import_module("content.unit_" + num[1:]).TEST
    mod = importlib.import_module("content.topic_" + num.replace(".", "_"))
    return mod.TOPIC


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("topics", nargs="+")
    ap.add_argument("--theme", default="classic", choices=sorted(latex.THEMES))
    ap.add_argument("--docs", default="notes,practice,quiz,testprep,packet")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--web", action="store_true", help="also export lesson JSON + SVG figures for the site")
    ap.add_argument("--no-pdf", action="store_true")
    a = ap.parse_args()

    topics = [load(n) for n in a.topics]
    for t in topics:
        (calclib.validate_test if isinstance(t, calclib.UnitTest) else calclib.validate)(t)
    calclib.fail_if_needed()

    if a.web:
        from calclib import web
        for t in topics:
            fn = web.export_test if isinstance(t, calclib.UnitTest) else web.export
            p = fn(t, os.path.join(ROOT, "web", "course", "content"),
                   os.path.join(ROOT, "web", "static", "figures"))
            print("  " + os.path.relpath(p, ROOT))
    if a.no_pdf:
        return
    stamp_font()
    for t in topics:
        outdir = os.path.join(ROOT, "build", "pdf", t.number)
        docs = ["unittest"] if isinstance(t, calclib.UnitTest) else a.docs.split(",")
        for doc in docs:
            # quizzes and tests come in forms A, B, C... when their slots have variants
            nf = 1
            if doc == "quiz":
                nf = calclib.n_forms(t.quiz)
            elif doc == "unittest":
                nf = calclib.n_forms(t.mcq_a, t.mcq_b, t.frq)
            if nf > 1:          # forms replace the single-version files; drop stale ones
                for key in ("", "-key"):
                    old = os.path.join(outdir, f"{t.number}-{doc}{key}-{a.theme}.pdf")
                    if os.path.exists(old):
                        os.remove(old)
            for k in range(nf):
                for key in (False, True):
                    tag = f"-form{'ABCDEF'[k]}" if nf > 1 else ""
                    name = f"{t.number}-{doc}{tag}{'-key' if key else ''}-{a.theme}"
                    src = latex.DOCS[doc](t, key, a.theme, k) if doc in ("quiz", "unittest") else latex.DOCS[doc](t, key, a.theme)
                    pdf = latex.compile_tex(src, name, outdir)
                    import fitz
                    print(f"  {os.path.relpath(pdf, ROOT)}: {len(fitz.open(pdf))} pages")
                    if a.preview:
                        latex.preview(pdf, PREVIEW_DIR)


def stamp_font():
    """The web app stamps packets in the heading font; it reads it from here so the server needs no TeX."""
    import shutil
    import subprocess
    dest = os.path.join(ROOT, "build", "pdf", "fonts", "LibertinusSans-Regular.otf")
    if os.path.exists(dest):
        return
    env = dict(os.environ, PATH=latex.TEXBIN + ":" + os.environ["PATH"])
    src = subprocess.run(["kpsewhich", "LibertinusSans-Regular.otf"], capture_output=True, text=True, env=env).stdout.strip()
    if src:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy(src, dest)


if __name__ == "__main__":
    main()
