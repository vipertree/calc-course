"""Topic -> LaTeX for the four printed documents, student copy and key."""
import os
import shutil
import subprocess
import sys

from . import (glue_punct, unit_label, topic_name, expand_for_print, FRQ, MCQ, BigIdea, Check, Definition, Example, Figure, Formula,
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
    return "\n\n".join([preamble(theme, key, f"{topic_name(t.number)}"), _notes_body(t), r"\end{document}"])


def _notes_body(t: Topic):
    out = [rf"\topictitle{{{t.label}}}{{{t.title}}}{{{t.unit}}}{{Guided Notes}}",
           rf"\objectives{{{t.goals}}}"]
    blocks = list(t.notes)
    for k, b in enumerate(blocks):
        if isinstance(b, Example) and k and isinstance(blocks[k - 1], Figure):
            continue                       # drawn with the figure before it
        if not isinstance(b, Text):
            out.append(r"\blockbreak")
        nxt = blocks[k + 1] if k + 1 < len(blocks) else None
        if isinstance(b, Figure) and isinstance(nxt, Example):
            # an example's graph and the example itself stay on one page
            out.append(r"\begin{keep}" + _block(b) + "\n" + _block(nxt) + r"\end{keep}")
        else:
            out.append(_block(b))
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
    # \fitwidth: a figure wider than its column (two-column packet) is scaled down to fit
    return r"\par\nopagebreak\begin{center}\fitwidth{" + f.tikz + r"}" + cap + r"\end{center}" + "\n"


def _item(i, it: Item, key):
    calc = r"\enspace{\small\hfont[calculator]}" if it.calc else ""
    s = rf"\item\begin{{keepitem}}{it.stem}{calc}" + "\n" + _fig(it.figure)
    s += rf"\work{{{it.work}}}{{{it.solution}}}" + "\n"
    if it.answer.kind != "self":
        s += rf"\answerline{{${it.answer.tex()}$}}"     # keys only: the final answer, flush left
    return s + r"\end{keepitem}" + "\n"


def _mcq(q: MCQ, key):
    calc = r"\enspace{\small\hfont[calculator]}" if q.calc else ""
    s = (rf"\item\begin{{keepitem}}{q.stem}{calc}" + "\n" + _fig(q.figure)
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
        s += r"\par}" + "\n"
    return s + r"\end{keepitem}" + "\n"


def _frq(f: FRQ, key, n):
    """A free-response question, headed "Question n" only: no title anywhere, on student copies or keys,
    since a title hints at the method (Adder, 2026-10-02).
    The whole question stays on one page (frqwhole shrinks the student work space if it must); a key too tall
    for a page breaks between parts, keeping the heading, intro, figure and part (a) together."""
    calc = "Calculator allowed" if f.calc else "No calculator"
    head = f"Question {n}"
    lead = (r"{\hfont\bfseries " + head + r"}\hfill{\small\hfont " + calc
            + rf"\enspace\textperiodcentered\enspace {f.points} points}}\par" + "\n" + f.intro + "\n" + _fig(f.figure))
    parts = []
    for p in f.parts:
        s = rf"\begin{{frqpart}}{{{p.label}}}{p.prompt}" + "\n" + rf"\work{{{p.work}}}{{{p.solution}}}" + "\n"
        if key:
            s += r"\par{\small\hfont\color{soft} Scoring}\par{\small\begin{tabular}{@{}p{1.1cm}p{13cm}@{}}"
            s += r" \\ ".join(rf"{pts} pt & {desc}" for pts, desc in p.rubric) + r"\end{tabular}}" + "\n"
        parts.append(s + r"\end{frqpart}" + "\n")
    return (r"\begin{frqwhole}\begin{keep}" + lead + parts[0] + r"\end{keep}" + "\n" + "".join(parts[1:])
            + r"\end{frqwhole}\medskip" + "\n")


def _list(items, compact):
    """Numbered questions. The compact packet sets them two to a row, numbered left to right, each cell its own
    one-item list starting at the right number."""
    if not compact:
        return [r"\begin{enumerate}"] + items + [r"\end{enumerate}"]
    cell = lambda k: rf"\begin{{enumerate}}[start={k + 1}, topsep=0pt]" + items[k] + r"\end{enumerate}" if k < len(items) else ""
    return [r"\begin{pairs}"] + [rf"\pairrow{{{cell(k)}}}{{{cell(k + 1)}}}" for k in range(0, len(items), 2)] + [r"\end{pairs}"]


def _practice_body(t, key, compact=False):
    return "\n".join([rf"\topictitle{{{t.label}}}{{{t.title}}}{{{t.unit}}}{{Practice}}",
                      r"Give exact answers unless a problem says to round."]
                     + _list([(_mcq(it, key) if isinstance(it, MCQ) else _item(i, it, key)) for i, it in enumerate(t.practice)], compact))


def practice_tex(t, key, theme):
    return "\n".join([preamble(theme, key, f"{topic_name(t.number)} Practice"), _practice_body(t, key), r"\end{document}"])


def quiz_tex(t, key, theme, k=0):
    name = "Quiz" + (f", Form {'ABCDEF'[k]}" if n_forms(t.quiz) > 1 else "")
    out = [preamble(theme, key, f"{topic_name(t.number)} {name}"),
           rf"\topictitle{{{t.label}}}{{{t.title}}}{{{t.unit}}}{{{name}}}",
           r"No calculator unless a question is marked [calculator]. Show your work.",
           r"\begin{enumerate}"]
    for it in form(t.quiz, k):
        out.append(_mcq(it, key) if isinstance(it, MCQ) else _item(0, it, key))
    out += [r"\end{enumerate}", r"\end{document}"]
    return "\n".join(out)


def _testprep_body(t, key, compact=False):
    out = [rf"\topictitle{{{t.label}}}{{{t.title}}}{{{t.unit}}}{{AP Test Prep}}",
           r"\sect{Multiple choice}"]
    out += _list([_mcq(q, key) for q in t.mcq], compact)
    out += ([r"\sect{Free response}"] if t.frq else [])   # some topics have no AP-style FRQ
    out += [_frq(f, key, i + 1) for i, f in enumerate(t.frq)]
    return "\n".join(out)


def testprep_tex(t, key, theme):
    return "\n".join([preamble(theme, key, f"{topic_name(t.number)} Test Prep"), _testprep_body(t, key), r"\end{document}"])


def packet_tex(t, key, theme, compact=False):
    """Lesson, practice and AP test prep in one printable packet. Page numbers run through the whole packet;
    the web app stamps each student's copy with their name and a packet ID in the footer.
    Practice starts on a new page; test prep follows straight on from it (Adder, 2026-10-02). The compact
    packet (a paper-saving trial) also runs practice on from the lesson and sets practice and multiple choice
    in two columns."""
    parts = [("Lesson", _notes_body(t)), ("Practice", _practice_body(t, key, compact)),
             ("AP Test Prep", _testprep_body(t, key, compact))]
    out = [preamble(theme, key, f"{topic_name(t.number)} Packet")]
    for k, (name, body) in enumerate(parts):
        if k == 1 and not compact:
            out.append(r"\clearpage")
        elif k:
            out.append(r"\blockbreak\bigskip")   # a good place to break, like the gap between lesson blocks
        out += [rf"\renewcommand{{\docline}}{{Topic {t.number} Packet\enspace\textperiodcentered\enspace {name}}}",
                r"\setcounter{calcsec}{0}\setcounter{calcex}{0}", body]
    out.append(r"\end{document}")
    return "\n\n".join(out)


def unittest_tex(u, key, theme, k=0):
    title = f"{unit_label(u.unit)} Test" + (f", Form {'ABCDEF'[k]}" if n_forms(u.mcq_a, u.mcq_b, u.frq) > 1 else "")
    mcq_a, mcq_b, frqs = form(u.mcq_a, k), form(u.mcq_b, k), form(u.frq, k)
    na, nb, fpts = len(mcq_a), len(mcq_b), sum(f.points for f in frqs)
    out = [preamble(theme, key, title),
           rf"\topictitle{{U{u.unit}}}{{{u.title}}}{{{unit_label(u.unit)} Test\enspace\textperiodcentered\enspace {u.minutes}}}{{AP format}}",
           # the scoring, up front: every multiple-choice question is 1 point; each FRQ shows its own points
           r"{\small\hfont\textbf{Scoring}\enspace "
           + rf"Part A: {_count(na, 'question')}, 1 point each ({_count(na, 'point')}).\enspace "
           + rf"Part B: {_count(nb, 'question')}, 1 point each ({_count(nb, 'point')}).\enspace "
           + rf"Part C: {_count(len(frqs), 'question')} ({_count(fpts, 'point')}).\enspace "
           + rf"\textbf{{Total: {na + nb + fpts} points.}}}}\par"]
    if key:
        letters = [q.correct for q in mcq_a + mcq_b]
        out.append(r"{\small\hfont Answer key:\enspace " + ", ".join(f"{i + 1}{l}" for i, l in enumerate(letters)) + r"}\par")
    part = lambda n, pts: rf"{{\small\hfont {_count(n, 'question')}, 1 point each\enspace\textperiodcentered\enspace {_count(pts, 'point')}}}\par"
    out += [r"\sect{Part A: multiple choice, no calculator}", part(na, na),
            r"\begin{enumerate}"] + [_mcq(q, key) for q in mcq_a] + [r"\end{enumerate}",
            r"\sect{Part B: multiple choice, calculator allowed}", part(nb, nb),
            rf"\begin{{enumerate}}\setcounter{{enumi}}{{{na}}}"] + [_mcq(q, key) for q in mcq_b] + [r"\end{enumerate}",
            r"\sect{Part C: free response}",
            rf"{{\small\hfont {_count(len(frqs), 'question')}\enspace\textperiodcentered\enspace {_count(fpts, 'point')}}}\par",
            r"Show your work. Justify answers where asked."]
    out += [_frq(f, key, n) for n, f in enumerate(frqs, 1)]
    out.append(r"\end{document}")
    return "\n".join(out)


def _count(n, word):
    return f"{n}~{word}{'' if n == 1 else 's'}"         # ~: the number never ends a line


DOCS = {"notes": notes_tex, "practice": practice_tex, "quiz": quiz_tex, "testprep": testprep_tex,
        "packet": packet_tex, "packetcompact": lambda t, key, theme: packet_tex(t, key, theme, compact=True),
        "unittest": unittest_tex}


# ------------------------------------------------------------------ compile
def compile_tex(tex, name, outdir):
    tex = expand_for_print(glue_punct(tex))          # a sentence's period stays on the formula's line
    # a text \blank written inside math can't typeset (calc.sty's \blank measures its argument in text mode); the web
    # export already treats it as \mblank, so print does the same
    from .web import _blanks_in_math_to_mblank
    tex = _blanks_in_math_to_mblank(tex)
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
