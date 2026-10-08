"""Topic -> JSON for the web app, plus SVG figures.

The page never receives answers. lesson.json is split in two:
  public:  everything the browser renders (text, prompts, choices, blank ids)
  private: answers, solutions and rubrics, looked up by id when the server grades
"""
from calclib import glue_punct
import json
from html import escape as html_escape
import os
import re
import shutil
import subprocess

from . import (FRQ, MCQ, UnitTest, slots, BigIdea, Check, Definition, Example, Figure, Formula, Item,
               Meanings, Section, Table, Text, Topic, Video, Desmos, FigureRow)
from .latex import ROOT, TEXBIN

# ------------------------------------------------------------------ LaTeX-light -> HTML
# an escaped \$ is a literal dollar sign, never a math delimiter
_MATH = re.compile(r"((?<!\\)\$\$.+?(?<!\\)\$\$|\\\[.+?\\\]|(?<!\\)\$.+?(?<!\\)\$)", re.S)


def _braced(s, i):
    """s[i] == '{'. Return (content, index after the matching '}')."""
    depth, j = 0, i
    while j < len(s):
        if s[j] == "{" and (j == 0 or s[j - 1] != "\\"):
            depth += 1
        elif s[j] == "}" and s[j - 1] != "\\":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    raise ValueError("unbalanced braces: " + s[i:i + 60])


class Blanks:
    """Collects \\blank{answer} occurrences so the page gets ids and the server gets answers."""

    def __init__(self, prefix):
        self.prefix, self.items = prefix, []

    def add(self, answer):
        bid = f"{self.prefix}-b{len(self.items) + 1}"
        self.items.append((bid, answer))
        return bid


DNE_WORDS = ("does not exist", "dne")


def _pick_html(bid, opts):
    """A check-box blank: the page shows one box per option; the answer stays on the server."""
    return f'<span class="blank pick" data-blank="{bid}" data-kind="pick" data-options="{html_escape(json.dumps(opts))}"></span>'


def _blank_html(bid, answer):
    kind = "math" if answer.strip().startswith("$") else "text"
    width = max(4, min(28, len(re.sub(r"[${}\\]", "", answer)) + 2))
    if answer.strip().lower() in DNE_WORDS:
        width = 6                      # "does not exist" gets a number-sized blank: its length mustn't give it away
    return f'<span class="blank" data-blank="{bid}" data-kind="{kind}" style="--w:{width}ch"></span>'


def _top_level_gaps(body):
    """Positions (start, end) of the \\quad/\\qquad gaps at the top level of a display (not inside braces,
    \\begin...\\end or \\left...\\right), where it can wrap. A \\quad right before \\text is a label's gap
    ("f(x) = L \\quad\\text{(left-hand limit)}") and stays put."""
    out, depth, env, lr, i = [], 0, 0, 0, 0
    while i < len(body):
        if body.startswith(r"\begin", i): env += 1
        elif body.startswith(r"\end", i): env -= 1
        elif body.startswith(r"\left", i): lr += 1
        elif body.startswith(r"\right", i): lr -= 1
        elif body[i] == "{" and (i == 0 or body[i - 1] != "\\"): depth += 1
        elif body[i] == "}" and body[i - 1] != "\\": depth -= 1
        m = re.match(r"(\s*\\q?quad\b\s*)+", body[i:]) if body[i] == "\\" or body[i].isspace() else None
        if m and depth == 0 and env == 0 and lr == 0:
            j = i + m.end()
            gap = m.group(0)
            if r"\qquad" in gap or not body.startswith(r"\text", j):
                out.append((i, j))
            i = j
            continue
        i += 1
    return out


def _display_wrap(s):
    """A display holding several formulas side by side (gapped by \\qquad or \\quad) is split into pieces that
    sit on one line when there is room and wrap onto the next when there isn't, instead of scrolling sideways
    (Adder, 2026-10-02: 1.3's one-sided limits box in a narrow window)."""
    def line(m):
        body = m.group(1)
        if r"\mblank" in body or r"\blank" in body:
            return m.group(0)                       # blanks: _display_blank_lines lays those out
        gaps = _top_level_gaps(body)
        if not gaps:
            return m.group(0)
        pieces, k = [], 0
        for a, b in gaps:
            pieces.append(body[k:a]); k = b
        pieces.append(body[k:])
        pieces = [p.strip() for p in pieces if p.strip()]
        if len(pieces) < 2:
            return m.group(0)
        return "\x02" + "".join(f"<span class='dpiece'>$\\displaystyle {p}$</span>" for p in pieces) + "\x03"
    return re.sub(r"\\\[(.+?)\\\]", line, s, flags=re.S)


def _display_blank_lines(s):
    """A display \\[ ... \\] holding blanks can't stay one KaTeX display (an input box can't live inside it). Turn it into a
    centered line of display-style pieces with the blanks between them: \\x02 $\\displaystyle A$ \\blank{$X$} $\\displaystyle B$ \\x03."""
    def line(m):
        body = m.group(1)
        if r"\mblank" not in body:
            return m.group(0)
        out, i = [], 0
        while True:
            j = body.find(r"\mblank", i)
            seg = body[i:] if j < 0 else body[i:j]
            if seg.strip():
                out.append("$\\displaystyle " + seg.strip() + "$")
            if j < 0:
                break
            k = j + len(r"\mblank")
            if body[k] == "[":
                k = body.index("]", k) + 1
            inner, i = _braced(body, k)
            out.append(f"\\blank{{${inner}$}}")
        return "\x02" + " ".join(out) + "\x03"
    return re.sub(r"\\\[(.+?)\\\]", line, s, flags=re.S)


def _blanks_in_math_to_mblank(s):
    """A text \\blank{$X$} written inside math (an easy slip: "$\\mblank{a} \\le f \\le \\blank{$b$}$") would split the
    formula and leak raw LaTeX onto the page. Inside math, treat it as \\mblank{X}."""
    out, i, mode = [], 0, None
    while i < len(s):
        if s.startswith(r"\blank", i):
            j = i + len(r"\blank")
            opt = ""
            if j < len(s) and s[j] == "[":
                e = s.index("]", j) + 1
                opt, j = s[j:e], e
            if j < len(s) and s[j] == "{":
                arg, k = _braced(s, j)
                if mode is None:
                    out.append(s[i:k])              # a text blank: copy it whole, its $...$ doesn't change mode
                else:
                    a = arg.strip()
                    if len(a) > 1 and a[0] == "$" and a[-1] == "$":
                        a = a[1:-1]
                    out.append(rf"\mblank{opt}{{{a}}}")
                i = k
                continue
        if s.startswith(r"\[", i) and mode is None:
            mode = "["; out.append(r"\["); i += 2; continue
        if s.startswith(r"\]", i) and mode == "[":
            mode = None; out.append(r"\]"); i += 2; continue
        if s[i] == "$" and (i == 0 or s[i - 1] != "\\") and mode in (None, "$"):
            mode = None if mode == "$" else "$"
        out.append(s[i]); i += 1
    return "".join(out)


def _blank_fracs_inline(s):
    """An input box can't sit inside a typeset fraction, so on the web \\frac{1}{\\mblank{X}} is written 1 / [box]
    (the PDF keeps the stacked fraction). A part that is more than one blank or token gets parentheses."""
    def part(a):
        a = a.strip()
        simple = re.fullmatch(r"\\mblank(\[[^\]]*\])?\{.*\}|[A-Za-z0-9.]+", a, re.S)
        if simple and (not a.startswith(r"\mblank") or _braced(a, a.index("{"))[1] == len(a)):
            return a
        return "(" + a + ")"
    out, pos = [], 0
    for m in re.finditer(r"\\[dt]?frac(?=\s*\{)", s):
        if m.start() < pos:
            continue
        num, k = _braced(s, s.index("{", m.end()))
        if k >= len(s) or s[k] != "{":
            continue
        den, k2 = _braced(s, k)
        if r"\mblank" not in num + den:
            continue
        out.append(s[pos:m.start()] + part(_blank_fracs_inline(num)) + r" \,/\, " + part(_blank_fracs_inline(den)))
        pos = k2
    return "".join(out) + s[pos:]


def _lift_mblanks(s):
    """\\mblank{X} lives inside math. Close the math before it and reopen after, turning it into \\blank{$X$},
    so the page shows an input box instead of handing KaTeX an unknown command."""
    s = _display_blank_lines(_blank_fracs_inline(_blanks_in_math_to_mblank(s)))
    out, i, mode = [], 0, None          # mode: None, "$", or "["
    while i < len(s):
        if s.startswith(r"\mblank", i):
            j = i + len(r"\mblank")
            if s[j] == "[":
                j = s.index("]", j) + 1
            inner, k = _braced(s, j)
            close, reopen = {"$": ("\x04", "\x04"), "[": (r"\]", r"\["), None: ("", "")}[mode]   # \x04: a $ we added
            out.append(f"{close}\\blank{{${inner}$}}{reopen}")
            i = k
            continue
        if s.startswith(r"\[", i) and mode is None:
            mode = "["; out.append(r"\["); i += 2; continue
        if s.startswith(r"\]", i) and mode == "[":
            mode = None; out.append(r"\]"); i += 2; continue
        if s[i] == "$" and (i == 0 or s[i - 1] != "\\") and mode in (None, "$"):
            mode = None if mode == "$" else "$"
        out.append(s[i]); i += 1
    r = "".join(out)
    # drop only the empty math our own close/reopen made ("$" + added close, added reopen + "$"); two separate
    # formulas the author wrote side by side ("$H(t)$ $^\circ$C") must stay separate
    r = re.sub(r"(?<!\\)\$\s*\x04|\x04\s*\$", "", r).replace("\x04", "$")
    return re.sub(r"\\\[\s*\\\]", "", r)


def _wrap(s, cmd, open_, close):
    """Replace cmd{arg} with open_ arg close, matching braces properly (arg may hold math or nested braces)."""
    out, pos = [], 0
    while True:
        i = s.find(cmd, pos)
        if i < 0:
            return "".join(out) + s[pos:]
        j = i + len(cmd)
        while j < len(s) and s[j] == " ":
            j += 1
        if j >= len(s) or s[j] != "{" or (j < len(s) and s[i + len(cmd):i + len(cmd) + 1].isalpha()):
            out.append(s[pos:j]); pos = j
            continue
        arg, k = _braced(s, j)
        out.append(s[pos:i] + open_ + arg + close)
        pos = k


def html(s, blanks=None):
    """Convert the course's LaTeX subset to HTML. Math stays in $...$ for KaTeX."""
    if s is None:
        return ""
    s = _lift_mblanks(_display_wrap(glue_punct(s)))
    out, pos = [], 0
    # check-box blanks: \pick{a|b}{answer}
    def _pick(m):
        opts = [o.strip() for o in m.group(1).split("|")]
        if blanks is None:
            return m.group(2)
        return "\x00" + _pick_html(blanks.add("pick:" + m.group(2).strip()), opts) + "\x00"
    s = re.sub(r"\\pick\{([^{}]*)\}\{([^{}]*)\}", _pick, s)
    # pull \blank{} out first, since its argument may itself contain math
    while True:
        i = s.find(r"\blank", pos)
        if i < 0:
            out.append(s[pos:])
            break
        out.append(s[pos:i])
        j = i + len(r"\blank")
        if s[j] == "[":
            j = s.index("]", j) + 1
        ans, k = _braced(s, j)
        if blanks is None:
            out.append(ans)
        else:
            out.append("\x00" + _blank_html(blanks.add(ans), ans) + "\x00")
        pos = k
    s = "".join(out)
    s = re.sub(r"\\renewcommand\{\\arraystretch\}\{[^{}]*\}", "", s)
    s = _wrap(s, r"\textbf", "<strong>", "</strong>")      # brace-aware: the argument may contain $math$
    s = _wrap(s, r"\emph", "<em>", "</em>")
    s = _wrap(s, r"\hfill", "<span class='attrib'>", "</span>")
    s = _tabulars(s)
    # text-mode commands, outside math only
    parts = _MATH.split(s)
    for n, p in enumerate(parts):
        if n % 2 == 1:
            continue
        p = re.sub(r"\\textbf\{([^{}]*)\}", r"<strong>\1</strong>", p)
        p = re.sub(r"\\emph\{([^{}]*)\}", r"<em>\1</em>", p)
        p = re.sub(r"\\(?:small|footnotesize|normalsize|large)\b\s*", "", p)
        p = re.sub(r"\\hfill\s*\{([^{}]*)\}", r"<span class='attrib'>\1</span>", p)   # right-aligned attribution
        p = p.replace(r"\hfill", "")
        p = re.sub(r"\\centerline\{", "<div class='center'>", p)
        p = p.replace(r"\par", "<span class='pb'></span>").replace(r"\smallskip", "").replace(r"\medskip", "")
        p = p.replace(r"\quad", "&emsp;").replace(r"\qquad", "&emsp;&emsp;").replace("~", "&nbsp;")
        p = p.replace(r"\enspace", "&ensp;").replace(r"\,", "&thinsp;")
        p = p.replace("``", "&ldquo;").replace("''", "&rdquo;")
        # a literal dollar sign: KaTeX's auto-render reads one text node at a time, so a $ alone in its own
        # element can't pair with another and start math
        p = p.replace(r"\$", "<span class='usd'>$</span>")
        parts[n] = p
    s = "".join(parts)
    # close any <div class='center'> opened by \centerline{...}: its closing brace is the next lone }
    while "<div class='center'>" in s and s.count("<div class='center'>") > s.count("</div>"):
        i = s.rfind("<div class='center'>")
        j = s.find("}", i)
        s = s[:j] + "</div>" + s[j + 1:]
    # a blank never wraps away from the short formula it completes ("lim f(u) = [blank]"), nor from the
    # punctuation after it (Adder, 2026-10-02, 1.9)
    s = re.sub(r'(?<!\\)\$([^$]{1,80}?)\$\s*\x00(<span class="blank"[^\x00]*)\x00([.,;:!?)]?)',
               lambda m: f"<span class='nobr'>${m.group(1)}${m.group(2)}{m.group(3)}</span>", s)
    s = re.sub(r'\x00(<span class="blank"[^\x00]*)\x00([.,;:!?)])', r"<span class='nobr'>\1\2</span>", s)
    s = s.replace("\x00", "").replace("\x02", "<span class='dline'>").replace("\x03", "</span>")
    left = [m for n, part in enumerate(_MATH.split(s)) if n % 2 == 0
            for m in re.findall(r"\\[A-Za-z]+", re.sub(r"<[^>]*>", "", part))]
    if left:
        LEFTOVER.update(left)
    return s


LEFTOVER = set()     # TeX commands that reached the web as text; export() fails the build on any


def _tabulars(p):
    """\\begin{tabular}{spec} a & b \\\\ c & d \\end{tabular} -> <table>."""
    while r"\begin{tabular}" in p:
        i = p.index(r"\begin{tabular}")
        spec, j = _braced(p, i + len(r"\begin{tabular}"))
        k = p.index(r"\end{tabular}", j)
        body = p[j:k]
        rows = [r for r in re.split(r"\\\\", body) if r.strip()]
        trs = []
        for r in rows:
            hline = r"\hline" in r
            r = r.replace(r"\hline", "").replace(r"\toprule", "").replace(r"\midrule", "").replace(r"\bottomrule", "")
            if not r.strip():
                continue
            cells = [c.strip() for c in r.split("&")]
            trs.append(("<tr class='rule'>" if hline else "<tr>") + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
        vbar = " vbar" if "|" in spec else ""
        p = p[:i] + f"<table class='data{vbar}'>" + "".join(trs) + "</table>" + p[k + len(r"\end{tabular}"):]
    return p


def para(s, blanks=None):
    return "<div class='prose'>" + html(s, blanks) + "</div>"


# ------------------------------------------------------------------ figures
def figure_svg(fig: Figure, outdir):
    """Compile a pgfplots figure to SVG with dvisvgm; black ink becomes currentColor for dark mode."""
    os.makedirs(outdir, exist_ok=True)
    build = os.path.join(ROOT, "build", "svg")
    os.makedirs(build, exist_ok=True)
    shutil.copy(os.path.join(ROOT, "pdf", "calc.sty"), build)
    tex = (r"\documentclass[dvisvgm]{standalone}" "\n" r"\def\pgfsysdriver{pgfsys-dvisvgm.def}"
           "\n" r"\usepackage{calc}\pagestyle{empty}\setmainfont{LibertinusSans-Regular.otf}\setmathfont{LibertinusMath-Regular.otf}"
           "\n" r"\begin{document}" + fig.tikz + r"\end{document}")
    name = fig.name
    with open(os.path.join(build, name + ".tex"), "w") as f:
        f.write(tex)
    env = dict(os.environ, PATH=TEXBIN + ":" + os.environ["PATH"])
    r = subprocess.run(["xelatex", "-no-pdf", "-interaction=nonstopmode", name + ".tex"], cwd=build,
                       capture_output=True, text=True, env=env)
    if r.returncode != 0:
        raise SystemExit(r.stdout[-3000:])
    r = subprocess.run(["dvisvgm", "--no-fonts", "--exact-bbox", "-o", name + ".svg", name + ".xdv"], cwd=build,
                       capture_output=True, text=True, env=env)
    if r.returncode != 0:
        raise SystemExit(r.stderr[-3000:])
    svg = open(os.path.join(build, name + ".svg")).read()
    svg = re.sub(r"(fill|stroke)='#000'", r"\1='currentColor'", svg)
    svg = re.sub(r'(fill|stroke)="#000"', r'\1="currentColor"', svg)
    svg = re.sub(r"(fill|stroke)='#000000'", r"\1='currentColor'", svg)
    # open dots and label backgrounds are white on paper; on screen they must match the page
    svg = re.sub(r"fill='#fff(fff)?'", "style='fill:var(--bg)'", svg)
    svg = re.sub(r'fill="#fff(fff)?"', 'style="fill:var(--bg)"', svg)
    # paths with no fill attribute default to black: make the root inherit currentColor
    svg = svg.replace("<svg ", "<svg fill='currentColor' ", 1)
    with open(os.path.join(outdir, name + ".svg"), "w") as f:
        f.write(svg)
    return name + ".svg"


# ------------------------------------------------------------------ export
def _answer(a):
    return {"kind": a.kind, "value": None if a.value is None else str(a.value), "var": a.var,
            "tol": a.tol, "display": a.tex()}


def _units(a):
    """The unit part of a number answer's display (LaTeX), shown beside the web input so no one has to type it."""
    if a.kind != "number" or not a.display:
        return None
    d = a.display
    idx = [d.find(k) for k in (r"\ \text", r"\text", r"\ ^\circ", r"^\circ") if d.find(k) >= 0]
    if not idx:
        return None
    u = d[min(idx):]
    return u[2:].strip() if u.startswith("\\ ") else u.strip()


def fill_blanks(s):
    """The source with every blank written as its answer, for reference pages (the formula sheet): \\mblank{X} -> X
    (still inside its math), \\blank{X} -> X, \\pick{a|b}{X} -> X."""
    s = re.sub(r"\\pick\{[^{}]*\}\{([^{}]*)\}", r"\1", s)
    for cmd in (r"\mblank", r"\blank"):
        out, pos = [], 0
        while True:
            i = s.find(cmd, pos)
            if i < 0:
                out.append(s[pos:])
                break
            j = i + len(cmd)
            if j < len(s) and s[j] == "[":
                j = s.index("]", j) + 1
            if j >= len(s) or s[j] != "{":
                out.append(s[pos:j]); pos = j
                continue
            arg, k = _braced(s, j)
            out.append(s[pos:i] + arg)
            pos = k
        s = "".join(out)
    return s


def export(t: Topic, outdir, figdir):
    LEFTOVER.clear()
    pub, priv = {"number": t.number, "label": t.label, "title": t.title, "unit": t.unit, "goals": html(t.goals),
                 "ced": t.ced, "bc_only": t.bc_only}, {"blanks": {}, "items": {}}
    slug = t.number.replace(".", "_")

    # notes: grouped into steps, a new step at each Section
    steps, cur, n_ex, n_chk = [], None, 0, 0
    sheet = []          # every formula box and definition, filled in, for the course formula sheet
    blanks = Blanks(f"n{slug}")
    for b in t.notes:
        if isinstance(b, Section):
            # blocks before the first Section (normally just the video) join that first section: no "Start here" step
            lead = cur["blocks"] if cur is not None and not steps else []
            cur = {"title": html(b.title), "blocks": lead}
            steps.append(cur)
            continue
        if cur is None:
            cur = {"title": "", "blocks": []}
        if isinstance(b, Text):
            cur["blocks"].append({"type": "text", "html": para(b.body, blanks)})
        elif isinstance(b, Formula):
            cur["blocks"].append({"type": "formula", "title": html(b.title), "html": para(b.body, blanks)})
            sheet.append({"type": "formula", "title": html(b.title), "html": para(fill_blanks(b.body))})
        elif isinstance(b, Definition):
            cur["blocks"].append({"type": "definition", "title": html(b.title), "html": para(b.body, blanks)})
            sheet.append({"type": "definition", "title": html(b.title), "html": para(fill_blanks(b.body))})
        elif isinstance(b, BigIdea):
            cur["blocks"].append({"type": "bigidea", "html": html(b.body)})
        elif isinstance(b, Meanings):
            cur["blocks"].append({"type": "meanings", "keys": list(b.keys), "caption": html(b.caption)})
        elif isinstance(b, Figure):
            cur["blocks"].append({"type": "figure", "src": figure_svg(b, figdir), "caption": html(b.caption)})
        elif isinstance(b, FigureRow):
            cur["blocks"].append({"type": "figrow", "figures": [
                {"src": figure_svg(f, figdir), "caption": html(f.caption)} for f in b.figures]})
        elif isinstance(b, Table):
            head = "<tr>" + "".join(f"<th>{html(c.strip())}</th>" for c in b.header.split("&")) + "</tr>" if b.header else ""
            rows = [re.sub(r"^\s*\[[^\]]*\]", "", r).replace(r"\hline", "") for r in b.latex.split(r"\\")]    # drop print-only row spacing (\\[5pt]) and rules
            rows = [r for r in rows if r.strip()]
            body = "".join("<tr>" + "".join(f"<td>{html(c.strip(), blanks)}</td>" for c in r.split("&")) + "</tr>"
                           for r in rows)
            cur["blocks"].append({"type": "table", "html": f"<table class='data'>{head}{body}</table>"})
        elif isinstance(b, Video):
            cur["blocks"].append({"type": "video", "title": b.title, "minutes": b.minutes,
                                  "src": f"video/{slug}.mp4", "captions": f"video/{slug}.vtt"})
        elif isinstance(b, Desmos):
            cur["blocks"].append({"type": "desmos", "title": b.title, "html": html(b.prompt),
                                  "expressions": b.expressions, "bounds": b.bounds})
        elif isinstance(b, Example):
            n_ex += 1
            iid = f"n{slug}-ex{n_ex}"
            cur["blocks"].append({"type": "example", "id": iid, "n": n_ex, "title": html(b.title),
                                  "html": para(b.body)})
            priv["items"][iid] = {"solution": html(b.solution)}
        elif isinstance(b, Check):
            n_chk += 1
            iid = f"n{slug}-chk{n_chk}"
            cur["blocks"].append({"type": "check", "id": iid, "html": para(b.prompt),
                                  "answer_kind": b.answer.kind, "units": _units(b.answer)})
            priv["items"][iid] = {"answer": _answer(b.answer), "solution": html(b.solution)}
        else:
            raise TypeError(b)
    if not steps:
        raise ValueError(f"{t.number}: notes need at least one Section")
    pub["steps"] = steps
    for bid, ans in blanks.items:
        priv["blanks"][bid] = ans

    def figpub(f):
        return {"src": figure_svg(f, figdir), "caption": html(f.caption)} if f is not None else None

    def item_pub(prefix, i, it, v=0):
        iid = f"{prefix}{slug}-{i + 1}" + (f"v{v + 1}" if v else "")
        if isinstance(it, MCQ):
            d = {"id": iid, "type": "mcq", "html": para(it.stem), "calc": it.calc,
                 "choices": [html(c) for c in it.choices], "figure": figpub(it.figure)}
            priv["items"][iid] = {"answer": _answer(it.answer), "solution": html(it.solution),
                                  "why_not": {k: html(v) for k, v in it.why_not.items()}}
        else:
            stem = it.stem
            if _units(it.answer):   # the box shows the units, so the web prompt doesn't ask for them
                stem = re.sub(r"\s*Include units\.", "", stem)
            d = {"id": iid, "type": "item", "html": para(stem), "calc": it.calc,
                 "answer_kind": it.answer.kind, "units": _units(it.answer), "figure": figpub(it.figure)}
            priv["items"][iid] = {"answer": _answer(it.answer), "solution": html(it.solution)}
        return d

    pub["practice"] = [item_pub("p", i, it) for i, it in enumerate(t.practice)]
    # every version of every quiz slot; the server draws one per slot and never sends the rest to the page
    pub["quiz_variants"] = [[item_pub("q", i, it, v) for v, it in enumerate(vs)] for i, vs in enumerate(slots(t.quiz))]
    pub["quiz"] = [vs[0] for vs in pub["quiz_variants"]]
    pub["mcq"] = [item_pub("m", i, it) for i, it in enumerate(t.mcq)]
    frqs = []
    for i, f in enumerate(t.frq):
        fid = f"f{slug}-{i + 1}"
        parts = []
        for p in f.parts:
            pid = f"{fid}{p.label}"
            parts.append({"id": pid, "label": p.label, "html": para(p.prompt), "answer_kind": p.answer.kind, "units": _units(p.answer),
                          "points": sum(x for x, _ in p.rubric)})
            priv["items"][pid] = {"answer": _answer(p.answer), "solution": html(p.solution),
                                  "rubric": [{"points": x, "html": html(d)} for x, d in p.rubric]}
        frqs.append({"id": fid, "title": f"Question {len(frqs) + 1}", "html": para(f.intro), "calc": f.calc, "figure": figpub(f.figure),
                     "type": f.frq_type, "points": f.points, "parts": parts})
    pub["frq"] = frqs

    os.makedirs(outdir, exist_ok=True)
    pub["formulas"] = sheet
    with open(os.path.join(outdir, f"{slug}.json"), "w") as fh:
        _no_leftover(pub.get("number") or pub.get("title"))
        json.dump({"public": pub, "private": priv}, fh, indent=1)
    return os.path.join(outdir, f"{slug}.json")


def _no_leftover(name):
    if LEFTOVER:
        raise SystemExit(f"{name}: raw TeX would show on the web: {sorted(LEFTOVER)}")


def export_test(u: UnitTest, outdir, figdir):
    """Unit test -> U<n>.json. MCQs go in public["quiz"] so the quiz grader handles them."""
    priv = {"blanks": {}, "items": {}}
    qv = []
    na = len(u.mcq_a)
    for i, vs in enumerate(slots(u.mcq_a) + slots(u.mcq_b)):
        row = []
        for v, q in enumerate(vs):
            iid = f"u{u.unit}-{i + 1}" + (f"v{v + 1}" if v else "")
            row.append({"id": iid, "type": "mcq", "html": para(q.stem), "calc": q.calc,
                        "choices": [html(c) for c in q.choices],
                        "figure": {"src": figure_svg(q.figure, figdir), "caption": html(q.figure.caption)} if q.figure else None,
                        "part": "A" if i < na else "B"})
            priv["items"][iid] = {"answer": {"kind": "choice", "value": q.correct, "display": f"({q.correct})"},
                                  "solution": html(q.solution), "why_not": {k: html(w) for k, w in q.why_not.items()}}
        qv.append(row)
    qs = [row[0] for row in qv]
    frq_rows = []
    for i, vs in enumerate(slots(u.frq)):
      frqs = []
      for v, f in enumerate(vs):
        fid = f"u{u.unit}f{i + 1}" + (f"v{v + 1}" if v else "")
        parts = []
        for p in f.parts:
            pid = f"{fid}{p.label}"
            parts.append({"id": pid, "label": p.label, "html": para(p.prompt), "answer_kind": p.answer.kind, "units": _units(p.answer),
                          "points": sum(x for x, _ in p.rubric)})
            priv["items"][pid] = {"answer": _answer(p.answer), "solution": html(p.solution),
                                  "rubric": [{"points": x, "html": html(d)} for x, d in p.rubric]}
        # the student sees "Question n" only: a title or FRQ type would hint at the method
        frqs.append({"id": fid, "title": f"Question {i + 1}", "html": para(f.intro), "calc": f.calc,
                     "points": f.points, "parts": parts,
                     "figure": {"src": figure_svg(f.figure, figdir), "caption": html(f.figure.caption)} if f.figure else None})
      frq_rows.append(frqs)
    pub = {"number": f"U{u.unit}", "unit": u.unit, "title": u.title, "minutes": u.minutes, "quiz": qs,
           "frq": [row[0] for row in frq_rows], "quiz_variants": qv, "frq_variants": frq_rows,
           "steps": [], "practice": [], "mcq": []}
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, f"U{u.unit}.json")
    with open(path, "w") as fh:
        _no_leftover(pub.get("number") or pub.get("title"))
        json.dump({"public": pub, "private": priv}, fh, indent=1)
    return path
