"""Topic 5.7: Using the Second Derivative Test to determine extrema.

CED: FUN-4.A (FUN-4.A.7, FUN-4.A.8): at c with f'(c) = 0, f''(c) < 0 gives a relative max and f''(c) > 0 a relative min;
f''(c) = 0 is inconclusive. If a continuous f has exactly one critical point on an interval and it is a relative extremum,
it is the absolute extremum there. Worked examples: x^3 - 3x^2 + 4, x^4 (inconclusive), x + 4/x on (0, inf).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Text, Topic, Variants, Video, num,
                     same, selfcheck)

x = sp.symbols("x", real=True)


def sdt(f, lo=-sp.oo, hi=sp.oo):
    """{c: 'max' | 'min' | 'inconclusive'} for each c with f'(c) = 0 in (lo, hi), by the sign of f''(c)."""
    f1, f2 = sp.diff(f, x), sp.diff(f, x, 2)
    out = {}
    for c in sorted(sp.solveset(f1, x, sp.Interval.open(lo, hi))):
        v = f2.subs(x, c)
        out[c] = "max" if v < 0 else "min" if v > 0 else "inconclusive"
    return out


assert sdt(x**3 - 3 * x**2 + 4) == {0: "max", 2: "min"}
assert sdt(x**4) == {0: "inconclusive"}
assert sdt(x + 4 / x, 0) == {2: "min"}

NOTES = [
    Video("s5_7.py::Lesson", "The second derivative test", 4),

    Section("The test"),
    Text(r"At a horizontal tangent, the bend of the graph tells the story. A hill with a flat top is a peak; a bowl with a flat bottom is a valley."),
    Formula("The Second Derivative Test", (
        r"Suppose $f'(c) = 0$. \par If $f''(c) < 0$ (concave \blank{down}), $f$ has a relative \blank{maximum} at $c$. \par "
        r"If $f''(c) > 0$ (concave \blank{up}), $f$ has a relative \blank{minimum} at $c$. \par "
        r"If $f''(c) = 0$, the test is \blank{inconclusive}: use the First Derivative Test instead.")),
    Text(r"\textbf{Inconclusive means inconclusive.} $x^4$, $-x^4$ and $x^3$ all have $f'(0) = 0$ and $f''(0) = 0$. The first has a minimum, the second a maximum, the third neither."),
    Text(r"\textbf{Justify:} ``$f$ has a relative maximum at $x = 0$ because $f'(0) = 0$ and $f''(0) < 0$.'' Both facts are needed."),

    Section("Which test?"),
    Text(r"Both tests are correct when they work; choosing one is a judgment call. The \textbf{second} derivative test is quick: plug $c$ into $f''$, no number line. "
         r"But it only applies where $f'(c) = 0$, and it says nothing when $f''(c) = 0$. The \textbf{first} derivative test always gives an answer, works where $f'$ is "
         r"undefined (corners, cusps), and gives the increasing/decreasing intervals too, but needs a sign chart. A good habit: if $f''$ is easy to find, try the "
         r"\blank{second} derivative test; if $f''(c) = 0$ or $f'(c)$ is undefined, use the \blank{first}."),

    Section("One critical point means absolute"),
    Text(r"If a continuous function has \blank{only one} critical point on an interval, and it's a relative minimum, then it is the \blank{absolute} minimum on that interval "
         r"(the graph can't come back down without making another critical point). The same goes for a maximum. This is how to justify optimization answers on open intervals."),
    VideoExample('Using the test', work="2.6cm"),
    BigIdea(r"At a horizontal tangent: $f'' < 0$ is a max, $f'' > 0$ is a min, $f'' = 0$ tells you nothing. A lone critical point that's a relative extremum is an absolute one."),
    Check(r"$f'(3) = 0$ and $f''(3) = -5$. What does $f$ have at $x = 3$?", selfcheck(r"\text{a relative maximum}"), r"Concave down at a horizontal tangent: a relative maximum."),
]

# ---------------------------------------------------------------- practice
P = [(x**3 - 12 * x + 1, "maximum"), (x**3 - 6 * x**2 + 9 * x, "minimum"), (x**4 - 8 * x**2, "maximum"), (x * sp.exp(-x), "maximum"),
     (x**2 * sp.log(x), "minimum"), (x - 2 * sp.sin(x), "minimum")]
PRACTICE = []
for f, ask in P:
    lo, hi = (0, sp.oo) if f.has(sp.log) else (0, 2 * sp.pi) if f.has(sp.sin) else (-sp.oo, sp.oo)
    cls = sdt(f, lo, hi)
    c = [k for k, v in cls.items() if v == ask[:3]]
    assert len(c) == 1, (f, cls)
    dom = r" for $x > 0$" if lo == 0 and hi == sp.oo else r" on $(0, 2\pi)$" if hi == 2 * sp.pi else ""
    PRACTICE.append(Item(rf"Use the Second Derivative Test to find the relative {ask} of $f(x) = {sp.latex(f)}${dom}. Enter its $x$-value.", num(c[0]),
                         rf"$f'(x) = {sp.latex(sp.simplify(sp.diff(f, x)))}$, $f''(x) = {sp.latex(sp.simplify(sp.diff(f, x, 2)))}$. " + "; ".join(
                             rf"$f''\left({sp.latex(k)}\right) {'<' if v == 'max' else '>'} 0$: relative {v}imum" for k, v in cls.items()) + ".",
                         work="2.6cm"))
same("p", [list(sdt(f, *((0, sp.oo) if f.has(sp.log) else (0, 2 * sp.pi) if f.has(sp.sin) else (-sp.oo, sp.oo))).keys()) for f, _ in P],
     [[-2, 2], [1, 3], [-2, 0, 2], [1], [sp.exp(-sp.Rational(1, 2))], [sp.pi / 3, 5 * sp.pi / 3]])
PRACTICE += [
    Item(r"$f'(2) = 0$ and $f''(2) = 0$. What can you conclude about $f$ at $x = 2$?", selfcheck(r"\text{nothing yet}"),
         r"The Second Derivative Test is inconclusive. Check the sign of $f'$ on each side (First Derivative Test).", work="1.4cm"),
    Item(r"$f(x) = x^4 - 4x^3$. The Second Derivative Test is inconclusive at one critical point. Which one, and what is happening there?", num(0),
         r"$f'(x) = 4x^2(x - 3)$, $f''(x) = 12x^2 - 24x$. $f''(0) = 0$: inconclusive. $f'$ is negative on both sides of $0$, so no extremum there.", work="2.4cm"),
    Item(r"$g(x) = x^2 + \dfrac{16}{x}$ for $x > 0$ has one critical point. Find the absolute minimum value of $g$ on $(0, \infty)$, and justify that it is absolute.", num(12),
         r"$g'(x) = 2x - \frac{16}{x^2} = 0$ at $x = 2$. $g''(x) = 2 + \frac{32}{x^3} > 0$, so a relative minimum; it is the only critical point, so it is the absolute minimum: $g(2) = 12$.", work="2.8cm"),
    Item(r"$f'(c) = 0$ and $f''(c) > 0$. Is the graph of $f$ concave up or down at $c$, and what does $f$ have there?", selfcheck(r"\text{concave up, relative minimum}"),
         r"Concave up with a horizontal tangent: a relative minimum.", work="1.4cm"),
]
assert sdt(x**2 + 16 / x, 0) == {2: "min"} and (x**2 + 16 / x).subs(x, 2) == 12

# ---------------------------------------------------------------- quiz
def q_item(f, ask):
    cls = sdt(f)
    c = [k for k, v in cls.items() if v == ask][0]
    word = {"max": "maximum", "min": "minimum"}[ask]
    return Item(rf"Use the Second Derivative Test to find the $x$-value of the relative {word} of $f(x) = {sp.latex(f)}$.", num(c),
                rf"$f'(x) = {sp.latex(sp.factor(sp.diff(f, x)))}$; $f''(x) = {sp.latex(sp.diff(f, x, 2))}$, and $f''({sp.latex(c)}) = {sp.latex(sp.diff(f, x, 2).subs(x, c))}$.", work="2.2cm")


QUIZ = [
    Variants(q_item(x**3 - 3 * x, "min"), q_item(x**3 - 27 * x, "min"), q_item(x**3 - 3 * x**2, "min")),
    Variants(q_item(x**3 - 3 * x, "max"), q_item(-x**3 + 12 * x, "max"), q_item(x**3 + 3 * x**2 - 9 * x, "max")),
    Variants(
        MCQ(r"$f'(4) = 0$ and $f''(4) = 0$. Which is true?", [r"$f$ has a relative maximum at $4$", r"$f$ has a relative minimum at $4$", r"$f$ has an inflection point at $4$",
            r"The Second Derivative Test gives no conclusion"], "D", r"$f''(c) = 0$ is inconclusive."),
        MCQ(r"$f'(1) = 0$ and $f''(1) = 3$. Which is true?", [r"$f$ has a relative minimum at $1$", r"$f$ has a relative maximum at $1$", r"$f$ is decreasing at $1$", r"No conclusion"], "A",
            r"$f'' > 0$: concave up at a horizontal tangent."),
        MCQ(r"$f'(-2) = 0$ and $f''(-2) = -1$. Which is true?", [r"$f$ has a relative minimum at $-2$", r"$f$ has a relative maximum at $-2$", r"$f$ has an inflection point at $-2$", r"No conclusion"], "B",
            r"$f'' < 0$: concave down at a horizontal tangent."),
    ),
    Variants(
        MCQ(r"Which justifies that $f$ has a relative minimum at $x = 5$?", [r"$f''(5) > 0$", r"$f'(5) = 0$", r"$f'(5) = 0$ and $f''(5) > 0$", r"$f'(5) = 0$ and $f''(5) < 0$"], "C", r"Both facts are needed."),
        MCQ(r"Which justifies that $f$ has a relative maximum at $x = 1$?", [r"$f'(1) = 0$ and $f''(1) < 0$", r"$f''(1) < 0$", r"$f'(1) = 0$", r"$f'(1) = 0$ and $f''(1) > 0$"], "A", r"Both facts are needed."),
        MCQ(r"Which justifies that $f$ has a relative minimum at $x = -3$?", [r"$f'(-3) = 0$", r"$f''(-3) > 0$", r"$f'(-3) = 0$ and $f''(-3) < 0$", r"$f'(-3) = 0$ and $f''(-3) > 0$"], "D", r"Both facts are needed."),
    ),
    Variants(
        Item(r"$f(x) = x + \dfrac{9}{x}$ for $x > 0$. Find the absolute minimum value of $f$.", num(6), r"$f'(x) = 1 - \frac{9}{x^2} = 0$ at $3$; $f''(3) > 0$; only critical point, so $f(3) = 6$ is absolute.", work="2.2cm"),
        Item(r"$f(x) = 4x + \dfrac{1}{x}$ for $x > 0$. Find the absolute minimum value of $f$.", num(4), r"$f'(x) = 4 - \frac{1}{x^2} = 0$ at $\frac12$; $f'' > 0$; only critical point, so $f\left(\frac12\right) = 4$ is absolute.", work="2.2cm"),
        Item(r"$f(x) = x + \dfrac{25}{x}$ for $x > 0$. Find the absolute minimum value of $f$.", num(10), r"$f'(x) = 1 - \frac{25}{x^2} = 0$ at $5$; $f'' > 0$; only critical point, so $f(5) = 10$ is absolute.", work="2.2cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$f(x) = x^3 - 6x^2 + 9x + 1$. At $x = 1$, $f$ has", [r"a relative minimum, because $f''(1) > 0$", r"a relative maximum, because $f''(1) < 0$",
        r"an inflection point, because $f''(1) = 0$", r"no critical point"], "B", r"$f'(1) = 0$ and $f''(1) = 6 - 12 = -6 < 0$."),
    MCQ(r"$f'(x) = x^2 - 2x - 8$. Which describes $f$ at $x = 4$?", [r"relative maximum", r"inflection point", r"neither", r"relative minimum"], "D",
        r"$f'(4) = 0$ and $f''(x) = 2x - 2$, so $f''(4) = 6 > 0$."),
    MCQ(r"A continuous $g$ on $(0, \infty)$ has one critical point, $x = 3$, with $g''(3) < 0$. Then", [r"$g(3)$ is the absolute maximum of $g$ on $(0, \infty)$",
        r"$g(3)$ is the absolute minimum", r"$g$ has no absolute maximum", r"$g$ has an inflection point at $3$"], "A", r"A lone critical point that is a relative max is the absolute max."),
    MCQ(r"$f'(x) = e^{x}(x^2 - 3x)$. At $x = 3$, $f''(3)$ is about", [r"$0$", r"$20.086$", r"$60.257$", r"$-20.086$"], "C",
        r"$f''(x) = e^x(x^2 - x - 3)$, so $f''(3) = 3e^3 \approx 60.257 > 0$: a relative minimum.", calc=True),
]
same("m", [sp.diff(sp.exp(x) * (x**2 - 3 * x), x).subs(x, 3)], [3 * sp.exp(3)])

FRQS = [
    FRQ("A function with one turn", (
        r"Let $f$ be the function defined by $f(x) = \dfrac{\ln x}{x}$ for $x > 0$. It can be shown that "
        r"$f''(x) = \dfrac{2\ln x - 3}{x^3}$."), [
        Part("a", r"Find $f'(x)$. Find the $x$-coordinate of the critical point of $f$.", num(sp.E, tol=0.001, display=r"e"),
             r"$f'(x) = \dfrac{\frac1x\cdot x - \ln x}{x^2} = \dfrac{1 - \ln x}{x^2}$. $f'(x) = 0$ when $\ln x = 1$, so $x = e$.",
             [(1, "$f'(x)$"), (1, "$x = e$")], work="2.4cm"),
        Part("b", r"Use the Second Derivative Test to determine whether $f$ has a relative minimum or a relative maximum at the "
                  r"critical point. Justify your answer.", selfcheck(r"\text{Relative maximum}"),
             r"$f'(e) = 0$ and $f''(e) = \dfrac{2 - 3}{e^3} = -\dfrac{1}{e^3} < 0$, so $f$ has a relative maximum at $x = e$.",
             [(1, "$f''(e) < 0$"), (1, "relative maximum, with $f'(e) = 0$")], work="2.2cm"),
        Part("c", r"Find the absolute maximum value of $f$ for $x > 0$. Justify your answer.",
             num(sp.exp(-1), tol=0.001, display=r"\tfrac1e"),
             r"$x = e$ is the only critical point of $f$ on $x > 0$, and $f$ has a relative maximum there, so the relative maximum is "
             r"the absolute maximum. (Also, $f' > 0$ for $0 < x < e$ and $f' < 0$ for $x > e$.) The absolute maximum value is "
             r"$f(e) = \dfrac1e$.",
             [(1, "answer $\\frac1e$"), (1, "justification: only critical point, or the sign of $f'$")], work="2.6cm"),
    ], frq_type="Function analysis"),
]
assert sp.simplify(sp.diff(sp.log(x) / x, x, 2) - (2 * sp.log(x) - 3) / x**3) == 0 and sdt(sp.log(x) / x, 0) == {sp.E: "max"}
same("frq c", (sp.log(x) / x).subs(x, sp.E), sp.exp(-1))

TOPIC = Topic(
    number="5.7", title="Using the Second Derivative Test to Determine Extrema",
    unit="Unit 5: Analytical Applications of Differentiation", ced=["FUN-4.A", "FUN-4.A.7", "FUN-4.A.8"],
    goals=r"Classify critical points with the sign of $f''$, know when the test is inconclusive, and recognize when a relative extremum is absolute.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
