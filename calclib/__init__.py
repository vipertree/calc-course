"""Single source of truth for every lesson.

A topic file (content/topic_X_Y.py) builds a Topic out of the blocks below.
The same Topic feeds:
  * the printed guided notes (student copy with blanks + teacher key),
  * the practice set, mini-quiz and test-prep PDFs (each with a key),
  * lesson.json for the web app.
Every answer that can be checked is checked with sympy when the topic loads;
build scripts refuse to run while FAILS is non-empty.

Text uses a small LaTeX subset so it can also be turned into HTML:
  $math$, \\textbf{}, \\emph{}, \\blank{answer}, \\mblank{answer} (inside math).
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import sympy as sp

FAILS = []


# ------------------------------------------------------------------ checks
def check(label, ok, detail=""):
    if not ok:
        FAILS.append(f"{label}: {detail}")
    return ok


def same(label, got, want):
    if isinstance(got, (list, tuple)):
        ok = len(got) == len(want)
        return all([same(f"{label}[{i}]", g, w) for i, (g, w) in enumerate(zip(got, want))]) and \
            check(label, ok, "length mismatch")
    got, want = sp.sympify(got), sp.sympify(want)
    if got.is_infinite or want.is_infinite:
        return check(label, got == want, f"{got} != {want}")
    d = sp.simplify(got - want)
    return check(label, d == 0, f"{got} != {want} (diff {d})")


def close(label, got, want, tol=1e-9):
    return check(label, abs(float(got) - float(want)) <= tol, f"got {got}, want {want}")


# ------------------------------------------------------------------ notes blocks
@dataclass
class Section:
    title: str


@dataclass
class Text:
    body: str


@dataclass
class Formula:
    title: str
    body: str


@dataclass
class Definition:
    title: str
    body: str


@dataclass
class BigIdea:
    body: str


@dataclass
class Meanings:
    keys: tuple            # any of "da","dg","ia","ig","inv"
    caption: str = ""


@dataclass
class Figure:
    tikz: str              # a complete tikzpicture
    name: str              # file stem for the web SVG
    caption: str = ""


@dataclass
class FigureRow:
    """Several small figures side by side."""
    figures: list


@dataclass
class Table:
    latex: str             # tabular body (LaTeX), may contain \blank{}
    spec: str
    header: str = ""


@dataclass
class Video:
    scene: str             # anim/<file>.py::<Scene>
    title: str
    minutes: float


@dataclass
class Desmos:
    """Interactive graph, web only (the PDF prints a pointer to it)."""
    title: str
    prompt: str
    expressions: list      # [{"latex": ..., "color": ..., "id": ...}, ...]
    bounds: dict           # {"left":..,"right":..,"bottom":..,"top":..}


@dataclass
class Example:
    title: str
    body: str
    solution: str
    work: str = "4cm"
    beat: str = ""         # the transcript beat that solves this example on screen, when the video teaches it as a lesson beat


@dataclass
class VideoExample:
    """An example in the notes that the video solves inside the lesson body: the scene's
    self.example("<title>", problem, steps) call is the single source, so notes and video can't disagree."""
    title: str
    work: str = "3cm"


@dataclass
class Check:
    prompt: str
    answer: "Answer"
    solution: str = ""
    work: str = "2.5cm"


# ------------------------------------------------------------------ answers
@dataclass
class Answer:
    """What the web app checks. kind: expr | number | choice | self."""
    kind: str
    value: Any = None      # sympy-parsable string, number, or "B"
    var: str = "x"
    tol: float = 0.0       # numeric answers: allowed absolute error (0 = exact)
    display: str = ""      # LaTeX shown in keys

    def tex(self):
        if self.display:
            return self.display
        if self.kind == "choice":
            return f"({self.value})"
        if self.kind in ("expr", "number"):
            if self.value == "DNE":
                return r"\text{does not exist}"
            return sp.latex(sp.sympify(self.value))
        return ""


def limchain(c, steps, value, var="x", side=""):
    r"""Limit notation on every line, as Adder requires:
    limchain(3, [r"\frac{x^2-9}{x-3}", r"(x+3)"], 6) ->
    $\displaystyle\lim_{x\to 3} \frac{x^2-9}{x-3} = \lim_{x\to 3} (x+3) = 6$"""
    lim = r"\lim_{" + var + r"\to " + str(c) + side + "}"
    chain = " = ".join(lim + " " + st for st in steps)
    return r"$\displaystyle " + chain + " = " + str(value) + "$"


def num(v, tol=0.0, display=""):
    return Answer("number", v, tol=tol, display=display)


def dne():
    """The limit does not exist (and is not infinite)."""
    return Answer("number", "DNE", display=r"\text{Does not exist}")


def infinite(sign=1):
    return Answer("number", "oo" if sign > 0 else "-oo", display=r"\infty" if sign > 0 else r"-\infty")


def expr(v, var="x", display=""):
    return Answer("expr", v, var=var, display=display)


def choice(letter):
    return Answer("choice", letter)


def selfcheck(display):
    return Answer("self", display=display)


# ------------------------------------------------------------------ items
@dataclass
class Item:
    stem: str
    answer: Answer
    solution: str
    work: str = "3cm"
    calc: bool = False     # calculator allowed
    skill: str = ""        # CED skill / FRQ type tag
    figure: "Figure" = None  # drawn after the stem, before the answer space


@dataclass
class MCQ:
    stem: str
    choices: list
    correct: str           # "A".."D"
    solution: str
    why_not: dict = field(default_factory=dict)   # letter -> what that mistake was
    calc: bool = False
    skill: str = ""
    figure: "Figure" = None

    @property
    def answer(self):
        return choice(self.correct)


@dataclass
class Part:
    label: str
    prompt: str
    answer: Answer
    solution: str
    rubric: list           # list of (points, description)
    work: str = "4cm"


@dataclass
class FRQ:
    title: str
    intro: str
    parts: list
    calc: bool = False
    frq_type: str = ""     # e.g. "Table / rates", see docs
    figure: "Figure" = None

    @property
    def points(self):
        return sum(p for part in self.parts for p, _ in part.rubric)


# ------------------------------------------------------------------ variants
class Variants:
    """One quiz/test question slot with interchangeable versions. The web draws one per slot for each attempt;
    paper forms A, B, C... take version 0, 1, 2... (cycling when a slot has fewer)."""

    def __init__(self, *items):
        assert items, "a slot needs at least one version"
        self.items = list(items)


def slots(lst):
    """Question list -> list of slots, each a list of versions."""
    return [x.items if isinstance(x, Variants) else [x] for x in lst]


def form(lst, k=0):
    """Version k of every slot (paper form A is k = 0)."""
    return [s[k % len(s)] for s in slots(lst)]


def every(lst):
    """Every version of every slot, for validation."""
    return [v for s in slots(lst) for v in s]


def n_forms(*lists):
    return max([len(s) for lst in lists for s in slots(lst)] or [1])


# ------------------------------------------------------------------ topic
@dataclass
class Topic:
    number: str            # "2.1"
    title: str
    unit: str              # "Unit 2: Differentiation, Definition and Fundamental Properties"
    ced: list              # learning objective / EK codes
    goals: str             # one sentence, student-facing
    notes: list
    practice: list
    quiz: list
    mcq: list
    frq: list
    bc_only: bool = False

    def __post_init__(self):
        # every example in the notes is solved in the video (Adder, 2026-10-01). Lesson-body examples come in through
        # VideoExample placeholders; the worked examples close the notes. See videx.py.
        from .videx import problem_tex, solution_tex, video_examples
        from .figs import graph
        slug = self.number.replace('.', '_')
        body = {t: (p, st, g) for t, p, st, g in video_examples(self.number, lesson=True)}
        notes = []
        for k, b in enumerate(self.notes):
            if isinstance(b, VideoExample):
                if b.title not in body:
                    raise ValueError(f"{self.number}: VideoExample {b.title!r} has no self.example({b.title!r}, ...) in anim/s{slug}.py")
                problem, steps, spec = body[b.title]
                if spec:
                    notes.append(graph(f"t{slug}_bex{k}", **spec))
                notes.append(Example(b.title, problem_tex(problem), solution_tex(steps), work=b.work))
            else:
                notes.append(b)
        # examples typed straight into the notes are a backlog: they still need a video version (tools/example_audit.py)
        tpath = Path(__file__).resolve().parent.parent / "transcripts" / f"{slug}.md"
        heads = {l[3:].strip() for l in tpath.read_text().splitlines() if l.startswith("## ")} if tpath.exists() else set()
        for b in notes:
            if isinstance(b, Example) and b.beat and b.beat not in heads:
                raise ValueError(f"{self.number}: notes example {b.title!r} says the video solves it in beat {b.beat!r}, but the transcript has no such beat")
        self.notes_only_examples = [b.title for b in notes if isinstance(b, Example) and not b.beat
                                    and not any(isinstance(o, VideoExample) and o.title == b.title for o in self.notes)]
        vids = video_examples(self.number)
        if vids:
            notes.append(Section("Worked examples"))
            for k, (title, problem, steps, spec) in enumerate(vids, 1):
                if spec:
                    notes.append(graph(f"t{slug}_vex{k}", **spec))
                notes.append(Example(title.split(":", 1)[1].strip() if ":" in title else title, problem_tex(problem), solution_tex(steps), work="3.5cm"))
        self.notes = notes


@dataclass
class UnitTest:
    """End-of-unit test in AP format: Part A MCQ (no calculator), Part B MCQ (calculator), free response."""
    unit: int
    title: str
    mcq_a: list
    mcq_b: list
    frq: list
    minutes: str = "90 minutes"

    @property
    def number(self):
        return f"U{self.unit}"


def validate_test(u: UnitTest):
    qs = every(u.mcq_a) + every(u.mcq_b)
    for q in qs:
        check(f"U{u.unit} MCQ letters", q.correct in "ABCD", q.stem[:40])
    for q in every(u.mcq_b):
        check(f"U{u.unit} Part B marked calc", q.calc, q.stem[:40])
    for q in every(u.mcq_a):
        check(f"U{u.unit} Part A not calc", not q.calc, q.stem[:40])
    from collections import Counter
    for k in range(n_forms(u.mcq_a, u.mcq_b)):
        fq = form(u.mcq_a, k) + form(u.mcq_b, k)
        counts = Counter(q.correct for q in fq)
        check(f"U{u.unit} form {'ABCDEF'[k]} answer balance", max(counts.values()) <= len(fq) // 2, str(dict(counts)))
    import re
    for q in qs:
        for blk in [q.stem, q.solution] + list(q.choices) + list(q.why_not.values()):
            check(f"U{u.unit} no em dashes", "\u2014" not in blk, blk[:50])


def validate(t: Topic):
    import re
    check(f"{t.number} quiz length", 4 <= len(t.quiz) <= 6, f"{len(t.quiz)} questions")
    for q in t.mcq:
        check(f"{t.number} MCQ letters", q.correct in "ABCD"[: len(q.choices)], q.stem[:40])
        check(f"{t.number} MCQ has 4 choices", len(q.choices) == 4, q.stem[:40])
    for b in t.notes:
        if isinstance(b, (Example, Check)):
            check(f"{t.number} no blanks in example/check prompts (web would show the answers)",
                  "\\blank" not in (b.body if isinstance(b, Example) else b.prompt), getattr(b, "title", "check"))
    # slots are drawn independently, so a quiz question can't lean on another one
    for it in every(t.quiz):
        check(f"{t.number} quiz question stands alone", not re.search(r"(Question|Problem) \d", it.stem), it.stem[:60])
    letters = [q.correct for q in t.mcq]
    if len(letters) >= 4:
        check(f"{t.number} MCQ answer spread", len(set(letters)) >= 3, str(letters))
    import re
    dash = re.compile("—")
    glued = re.compile(r"\\(par|quad|qquad|smallskip|medskip)[A-Za-z]")
    for blk in _all_text(t):
        check(f"{t.number} no em dashes", not dash.search(blk), blk[:60])
        m = glued.search(blk)
        check(f"{t.number} command glued to next word", not m, m and blk[max(0, m.start() - 30):m.end() + 10])


def _all_text(t):
    out = []
    for b in t.notes:
        for v in vars(b).values():
            if isinstance(v, str):
                out.append(v)
    for it in t.practice + every(t.quiz) + t.mcq:
        out += [it.stem, it.solution] + list(getattr(it, "choices", []))
    for f in t.frq:
        out += [f.intro] + [p.prompt for p in f.parts] + [p.solution for p in f.parts]
        out += [d for p in f.parts for _, d in p.rubric]
    for q in t.mcq + [q for q in every(t.quiz) if isinstance(q, MCQ)]:
        out += list(q.why_not.values())
    return out


def fail_if_needed():
    if FAILS:
        print("\nCHECKS FAILED:")
        for f in FAILS:
            print("  -", f)
        raise SystemExit(1)
