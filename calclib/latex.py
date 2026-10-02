"""Topic -> LaTeX for the four printed documents, student copy and key."""
import os
import shutil
import subprocess
import sys

from . import (FRQ, MCQ, BigIdea, Check, Definition, Example, Figure, Formula,
               Item, Meanings, form, n_forms, Section, Table, Text, Topic, Video, Desmos, FigureRow)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXBIN = os.path.expanduser("~/opt/texlive/bin/x86_64-linux")

THEMES = {
    # name: (main font, heading font, math font)
    "classic": ("Libertinus Serif", "Libertinus Sans", "Libertinus Math"),
    "modern": ("Fira Sans Book", "Fira Sans", "Fira Math"),
    "textbook": ("NewComputerModern10 Book", "NewComputerModernSans10", "NewComputerModernMath Book"),
}
FONT_FILES = {
    "Libertinus Serif": ("LibertinusSerif-Regular.otf", "LibertinusSerif-Bold.otf",
                         "LibertinusSerif-Italic.otf", "LibertinusSerif-BoldItalic.otf"),
    "Libertinus Sans": ("LibertinusSans-Regular.otf", "LibertinusSans-Bold.otf",
                        "LibertinusSans-Italic.otf", "LibertinusSans-Bold.otf"),
    "Libertinus Math": ("LibertinusMath-Regular.otf",),
    "Fira Sans Book": ("FiraSans-Book.otf", "FiraSans-SemiBold.otf",
                       "FiraSans-BookItalic.otf", "FiraSans-SemiBoldItalic.otf"),
    "Fira Sans": ("FiraSans-Regular.otf", "FiraSans-SemiBold.otf",
                  "FiraSans-Italic.otf", "FiraSans-SemiBoldItalic.otf"),
    "Fira Math": ("FiraMath-Regular.otf",),
    "NewComputerModern10 Book": ("NewCM10-Book.otf", "NewCM10-Bold.otf",
                                 "NewCM10-BookItalic.otf", "NewCM10-BoldItalic.otf"),
    "NewComputerModernSans10": ("NewCMSans10-Book.otf", "NewCMSans10-Bold.otf",
                                "NewCMSans10-BookOblique.otf", "NewCMSans10-BoldOblique.otf"),
    "NewComputerModernMath Book": ("NewCMMath-Book.otf",),
}


def _fontdecl(cmd, name, extra=""):
    f = FONT_FILES[name]
    if len(f) == 1:
        return f"\\{cmd}{{{f[0]}}}"
    return (f"\\{cmd}{{{f[0]}}}[BoldFont={f[1]}, ItalicFont={f[2]}, BoldItalicFont={f[3]}{extra}]")


def preamble(theme, key, docline):
    main, head, math = THEMES[theme]
    return "\n".join([
        r"\documentclass[11pt]{article}",
        r"\usepackage{calc}",
        _fontdecl("setmainfont", main, ", Numbers=Lining"),
        _fontdecl("newfontfamily\\headingfont", head, ", Numbers=Lining"),
        _fontdecl("setmathfont", math),
        r"\renewcommand{\hfont}{\headingfont}",
        r"\keytrue" if key else r"\keyfalse",
        rf"\renewcommand{{\docline}}{{{docline}}}",
        r"\begin{document}",
    ])


# ------------------------------------------------------------------ notes
def notes_tex(t: Topic, key, theme):
    out = [preamble(theme, key, f"Topic {t.number}"),
           rf"\topictitle{{{t.number}}}{{{t.title}}}{{{t.unit}}}{{Guided Notes}}",
           rf"\objectives{{{t.goals}}}"]
    for b in t.notes:
        if not isinstance(b, Text):
            out.append(r"\blockbreak")
        out.append(_block(b))
    out.append(r"\end{document}")
    return "\n\n".join(out)


def _block(b):
    if isinstance(b, Section):
        return rf"\sect{{{b.title}}}"
    if isinstance(b, Text):
        return b.body
    if isinstance(b, Formula):
        return rf"\begin{{formula}}[{b.title}]" + "\n" + b.body + "\n" + r"\end{formula}"
    if isinstance(b, Definition):
        return rf"\begin{{definition}}[{b.title}]" + "\n" + b.body + "\n" + r"\end{definition}"
    if isinstance(b, BigIdea):
        return r"\begin{bigidea}" + b.body + r"\end{bigidea}"
    if isinstance(b, Meanings):
        cap = rf"\par\centering\small\itshape {b.caption}\par" if b.caption else ""
        return r"{\meanings{" + ",".join(b.keys) + "}" + cap + "}"
    if isinstance(b, Figure):
        cap = rf"\par{{\small\itshape {b.caption}}}" if b.caption else ""
        return r"\begin{center}" + b.tikz + cap + r"\end{center}"
    if isinstance(b, FigureRow):
        w = 0.98 / len(b.figures)
        cells = [rf"\begin{{minipage}}[b]{{{w:.3f}\linewidth}}\centering " + f.tikz
                 + (rf"\par{{\small\itshape {f.caption}}}" if f.caption else "") + r"\end{minipage}" for f in b.figures]
        return r"\begin{center}" + r"\hfill".join(cells) + r"\end{center}"
    if isinstance(b, Table):
        head = rf"{b.header} \\ \midrule " if b.header else ""
        return (r"\begin{center}\renewcommand{\arraystretch}{1.35}\begin{tabular}{" + b.spec + r"}\toprule "
                + head + b.latex + r" \\ \bottomrule\end{tabular}\end{center}")
    if isinstance(b, Video):
        return (r"{\small\hfont\color{soft}\textbf{Video}\enspace " + b.title
                + rf" ({b.minutes:g} min, in the online lesson)" + r"}\par")
    if isinstance(b, Desmos):
        return (r"{\small\hfont\color{soft}\textbf{Explore}\enspace " + b.title
                + r" (interactive graph in the online lesson)}\par")
    if isinstance(b, Example):
        return (rf"\begin{{example}}[{b.title}]" + "\n" + b.body + "\n"
                + rf"\work{{{b.work}}}{{{b.solution}}}" + "\n" + r"\end{example}")
    if isinstance(b, Check):
        return (r"\begin{checkbox}" + "\n" + b.prompt + "\n"
                + rf"\work{{{b.work}}}{{{b.solution}}}" + "\n"
                + rf"\answerline{{${b.answer.tex()}$}}" + r"\end{checkbox}")
    raise TypeError(b)


# ------------------------------------------------------------------ item sets
def _fig(f):
    if f is None:
        return ""
    cap = rf"\par{{\small\itshape {f.caption}}}" if f.caption else ""
    return r"\par\nopagebreak\begin{center}" + f.tikz + cap + r"\end{center}" + "\n"


def _item(i, it: Item, key):
    calc = r"\enspace{\small\hfont[calculator]}" if it.calc else ""
    s = rf"\item {it.stem}{calc}" + "\n" + _fig(it.figure)
    s += rf"\work{{{it.work}}}{{{it.solution}}}" + "\n"
    if it.answer.kind != "self":
        s += rf"\answerline{{${it.answer.tex()}$}}"
    return s


def _mcq(q: MCQ, key):
    calc = r"\enspace{\small\hfont[calculator]}" if q.calc else ""
    s = (r"\needspace{9\baselineskip}" + rf"\item {q.stem}{calc}" + "\n" + _fig(q.figure)
         + r"\begin{choices}" + "\n")
    for i, c in enumerate(q.choices):
        letter = "ABCD"[i]
        mark = r"\textbf{" + c + r"}\enspace\correctmark" if (key and letter == q.correct) else c
        s += rf"\item {mark}" + "\n"
    s += r"\end{choices}" + "\n"
    if key:
        s += r"{\small " + q.solution
        if q.why_not:
            s += r"\par\smallskip{\color{soft}\hfont Common wrong answers:} " + "; ".join(
                f"({k}) {v}" for k, v in sorted(q.why_not.items()))
        s += "}\n"
    return s


def _frq(f: FRQ, key):
    calc = "Calculator allowed" if f.calc else "No calculator"
    s = (r"\needspace{10\baselineskip}{\hfont\bfseries " + f.title + r"}\hfill{\small\hfont " + calc
         + rf"\enspace\textperiodcentered\enspace {f.points} points}}\par" + "\n" + f.intro + "\n" + _fig(f.figure))
    s += r"\begin{enumerate}[label=(\alph*), leftmargin=2em]" + "\n"
    for p in f.parts:
        s += rf"\item {p.prompt}" + "\n" + rf"\work{{{p.work}}}{{{p.solution}}}" + "\n"
        if key:
            s += r"\par{\small\hfont\color{soft} Scoring}\par{\small\begin{tabular}{@{}p{1.1cm}p{13cm}@{}}"
            s += r" \\ ".join(rf"{pts} pt & {desc}" for pts, desc in p.rubric) + r"\end{tabular}}" + "\n"
    s += r"\end{enumerate}" + "\n"
    return s


def practice_tex(t, key, theme):
    out = [preamble(theme, key, f"Topic {t.number} Practice"),
           rf"\topictitle{{{t.number}}}{{{t.title}}}{{{t.unit}}}{{Practice}}",
           r"Give exact answers unless a problem says to round.",
           r"\begin{enumerate}"]
    out += [_item(i, it, key) for i, it in enumerate(t.practice)]
    out += [r"\end{enumerate}", r"\end{document}"]
    return "\n".join(out)


def quiz_tex(t, key, theme, k=0):
    name = "Quiz" + (f", Form {'ABCDEF'[k]}" if n_forms(t.quiz) > 1 else "")
    out = [preamble(theme, key, f"Topic {t.number} {name}"),
           rf"\topictitle{{{t.number}}}{{{t.title}}}{{{t.unit}}}{{{name}}}",
           r"No calculator unless a question is marked [calculator]. Show your work.",
           r"\begin{enumerate}"]
    for it in form(t.quiz, k):
        out.append(_mcq(it, key) if isinstance(it, MCQ) else _item(0, it, key))
    out += [r"\end{enumerate}", r"\end{document}"]
    return "\n".join(out)


def testprep_tex(t, key, theme):
    out = [preamble(theme, key, f"Topic {t.number} Test Prep"),
           rf"\topictitle{{{t.number}}}{{{t.title}}}{{{t.unit}}}{{AP Test Prep}}",
           r"\sect{Multiple choice}",
           r"\begin{enumerate}"]
    out += [_mcq(q, key) for q in t.mcq]
    out += [r"\end{enumerate}", r"\sect{Free response}"]
    out += [_frq(f, key) for f in t.frq]
    out.append(r"\end{document}")
    return "\n".join(out)


def unittest_tex(u, key, theme, k=0):
    title = f"Unit {u.unit} Test" + (f", Form {'ABCDEF'[k]}" if n_forms(u.mcq_a, u.mcq_b, u.frq) > 1 else "")
    mcq_a, mcq_b, frqs = form(u.mcq_a, k), form(u.mcq_b, k), form(u.frq, k)
    out = [preamble(theme, key, title),
           rf"\topictitle{{U{u.unit}}}{{{u.title}}}{{Unit {u.unit} Test\enspace\textperiodcentered\enspace {u.minutes}}}{{AP format}}"]
    if key:
        letters = [q.correct for q in mcq_a + mcq_b]
        cells = " & ".join(f"{i + 1}\,{l}" for i, l in enumerate(letters))
        out.append(r"{\small\hfont Answer key:\enspace " + ", ".join(f"{i + 1}{l}" for i, l in enumerate(letters)) + r"}\par")
    n = len(mcq_a)
    out += [rf"\sect{{Part A: multiple choice, no calculator}}",
            r"\begin{enumerate}"] + [_mcq(q, key) for q in mcq_a] + [r"\end{enumerate}",
            rf"\sect{{Part B: multiple choice, calculator allowed}}",
            rf"\begin{{enumerate}}\setcounter{{enumi}}{{{n}}}"] + [_mcq(q, key) for q in mcq_b] + [r"\end{enumerate}",
            r"\sect{Part C: free response}", r"Show your work. Justify answers where asked."]
    out += [_frq(f, key) for f in frqs]
    out.append(r"\end{document}")
    return "\n".join(out)


DOCS = {"notes": notes_tex, "practice": practice_tex, "quiz": quiz_tex, "testprep": testprep_tex, "unittest": unittest_tex}


# ------------------------------------------------------------------ compile
def compile_tex(tex, name, outdir):
    os.makedirs(outdir, exist_ok=True)
    build = os.path.join(outdir, "_build")
    os.makedirs(build, exist_ok=True)
    shutil.copy(os.path.join(ROOT, "pdf", "calc.sty"), build)
    with open(os.path.join(build, name + ".tex"), "w") as f:
        f.write(tex)
    env = dict(os.environ, PATH=TEXBIN + ":" + os.environ["PATH"])
    for _ in range(2):   # tikz remember picture needs two passes
        r = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", name + ".tex"],
                           cwd=build, capture_output=True, text=True, env=env)
        if r.returncode != 0:
            print(r.stdout[-4000:])
            sys.exit(f"LaTeX failed on {name}")
    for line in r.stdout.splitlines():
        if line.startswith("Overfull \\hbox") and float(line.split("(")[1].split("pt")[0]) > 2:
            print("  ", name, line.strip())
    pdf = os.path.join(outdir, name + ".pdf")
    shutil.copy(os.path.join(build, name + ".pdf"), pdf)
    return pdf


def preview(pdf, pngdir, zoom=1.4):
    import fitz
    os.makedirs(pngdir, exist_ok=True)
    d = fitz.open(pdf)
    paths = []
    for i, page in enumerate(d):
        p = os.path.join(pngdir, f"{os.path.basename(pdf)[:-4]}-p{i + 1}.png")
        page.get_pixmap(matrix=fitz.Matrix(zoom, zoom)).save(p)
        paths.append(p)
    return paths
