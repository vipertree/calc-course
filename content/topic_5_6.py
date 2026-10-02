"""Topic 5.6: Determining concavity of functions over their domains.

CED: FUN-4.A (FUN-4.A.4-4.A.6): f'' > 0 means f' increasing and the graph concave up; f'' < 0 concave down; an inflection
point is where concavity changes (f'' changes sign, or equivalently f' changes from increasing to decreasing).
Callback to 4.6: concave up = the graph lies above its tangent lines. Worked examples: x^3 - 6x^2 + 5, x^4 - 4x^3,
x e^x.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Text, Topic, Variants, Video, num,
                     same, selfcheck)

x = sp.symbols("x", real=True)


def inflections(f, lo=-sp.oo, hi=sp.oo):
    """x-values where f'' changes sign."""
    f2 = sp.diff(f, x, 2)
    out = []
    for c in sorted(sp.solveset(f2, x, sp.Interval.open(lo, hi))):
        l, r = f2.subs(x, c - sp.Rational(1, 1000)), f2.subs(x, c + sp.Rational(1, 1000))
        if l * r < 0:
            out.append(c)
    return out


same("ex1", inflections(x**3 - 6 * x**2 + 5), [2])
same("ex2", inflections(x**4 - 4 * x**3), [0, 2])
same("ex3", inflections(x * sp.exp(x)), [-2])

NOTES = [
    Video("s5_6.py::Lesson", "Which way the graph bends", 4),

    Section("Concave up, concave down"),
    Text(r"A graph is \blank{concave up} where it bends upward like a cup, and \blank{concave down} where it bends downward like a cap. "
         r"Concave up means the graph lies \blank{above} its tangent lines (Topic 4.6); concave down means it lies below them."),
    Formula("Concavity from derivatives", (
        r"$f$ is concave up on an interval where $f'$ is \blank{increasing}, that is, where \[ f''(x) > 0. \] "
        r"$f$ is concave down where $f'$ is decreasing, that is, where \[ f''(x) < 0. \]")),
    Text(r"Why: as you move right along a cup, the tangent slopes keep growing. Along a cap they keep shrinking."),

    Section("Points of inflection"),
    Formula("Point of inflection", (
        r"A point of inflection is a point on the graph where the \blank{concavity changes}: $f''$ changes sign there "
        r"(equivalently, $f'$ changes from increasing to decreasing or the reverse).")),
    Text(r"\textbf{Careful:} $f''(c) = 0$ alone is not enough. $f(x) = x^4$ has $f''(0) = 0$, but $f'' = 12x^2 \ge 0$ on both sides: no inflection point."),
    VideoExample('Concavity of a cubic', work="2.6cm"),
    Text(r"\textbf{Justify with $f''$} (or with $f'$ increasing/decreasing): ``$f$ has a point of inflection at $x = -1$ because $f''$ changes sign there.''"),
    BigIdea(r"The sign of $f''$ tells which way the graph bends. A point of inflection is where $f''$ changes sign."),
    Check(r"$f''(x) = x - 3$. Where is $f$ concave down?", selfcheck(r"(-\infty, 3)"), r"$f'' < 0$ for $x < 3$."),
]

# ---------------------------------------------------------------- practice
P = [x**3 - 9 * x**2, x**3 + 6 * x**2 - x, x**4 - 6 * x**2, 2 * x**3 - 3 * x**2 - 12 * x, x * sp.exp(-x), x**4 + 4 * x**3, sp.exp(-x**2 / 2)]
PRACTICE = []
for f in P:
    inf = inflections(f)
    f2 = sp.factor(sp.diff(f, x, 2))
    PRACTICE.append(Item(rf"Find the $x$-coordinate{'s' if len(inf) > 1 else ''} of every point of inflection of $f(x) = {sp.latex(f)}$." + (" Enter the largest." if len(inf) > 1 else ""),
                         num(inf[-1]), rf"$f''(x) = {sp.latex(f2)}$ changes sign at $x = {', '.join(sp.latex(c) for c in inf)}$.", work="2.4cm"))
same("p", [inflections(f) for f in P], [[3], [-2], [-1, 1], [sp.Rational(1, 2)], [2], [-2, 0], [-1, 1]])
PRACTICE += [
    Item(r"Does $f(x) = x^4 + x$ have a point of inflection at $x = 0$? Explain.", selfcheck(r"\text{no}"),
         r"$f''(x) = 12x^2$ is $0$ at $x = 0$ but positive on both sides, so the concavity doesn't change. No inflection point.", work="1.8cm"),
    Item(r"$f'(x) = x^2 - 4x$. On what interval is the graph of $f$ concave down?", selfcheck(r"(-\infty, 2)"), r"$f''(x) = 2x - 4 < 0$ for $x < 2$.", work="1.6cm"),
    Item(r"The graph of $f'$ is increasing on $(-\infty, 1)$ and decreasing on $(1, \infty)$. Where does $f$ have a point of inflection?", num(1),
         r"$f'$ changes from increasing to decreasing at $x = 1$, so $f$ changes from concave up to concave down there.", work="1.4cm"),
    Item(r"$f(x) = \ln\left(x^2 + 1\right)$. Where is $f$ concave up?", selfcheck(r"(-1, 1)"),
         r"$f''(x) = \dfrac{2(1 - x^2)}{(x^2 + 1)^2} > 0$ for $-1 < x < 1$.", work="2.4cm"),
    Item(r"Is the graph of $f(x) = \sqrt{x}$ concave up or concave down for $x > 0$?", selfcheck(r"\text{concave down}"),
         r"$f''(x) = -\frac{1}{4}x^{-3/2} < 0$ for $x > 0$: concave down.", work="1.6cm"),
]
same("p2", [sp.simplify(sp.diff(sp.log(x**2 + 1), x, 2) - 2 * (1 - x**2) / (x**2 + 1)**2)], [0])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(*[Item(rf"Find the $x$-coordinate of the point of inflection of $f(x) = {sp.latex(f)}$.", num(inflections(f)[0]),
                    rf"$f''(x) = {sp.latex(sp.diff(f, x, 2))}$ changes sign at $x = {sp.latex(inflections(f)[0])}$.", work="1.8cm")
               for f in (x**3 - 3 * x**2 + 4, x**3 + 9 * x**2 - 2 * x, 2 * x**3 - 12 * x**2 + x)]),
    Variants(
        Item(r"$f''(x) = (x - 2)(x + 3)$. On what interval is $f$ concave down?", selfcheck(r"(-3, 2)"), r"$f'' < 0$ between the roots.", work="1.4cm"),
        Item(r"$f''(x) = x(x - 5)$. On what interval is $f$ concave down?", selfcheck(r"(0, 5)"), r"$f'' < 0$ between the roots.", work="1.4cm"),
        Item(r"$f''(x) = (4 - x)(x + 1)$. On what interval is $f$ concave up?", selfcheck(r"(-1, 4)"), r"$f'' > 0$ between the roots.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"$f''(x) = (x - 1)^2(x + 2)$. How many points of inflection does $f$ have?", [r"$0$", r"$1$", r"$2$", r"$3$"], "B", r"$f''$ changes sign only at $-2$."),
        MCQ(r"$f''(x) = x^2(x - 3)$. How many points of inflection does $f$ have?", [r"$2$", r"$0$", r"$1$", r"$3$"], "C", r"$f''$ changes sign only at $3$."),
        MCQ(r"$f''(x) = (x + 1)(x - 1)(x - 4)^2$. How many points of inflection does $f$ have?", [r"$1$", r"$3$", r"$0$", r"$2$"], "D", r"$f''$ changes sign at $-1$ and $1$, not at $4$."),
    ),
    Variants(
        MCQ(r"On an interval where the graph of $f$ is concave up,", [r"$f'$ is increasing", r"$f$ is increasing", r"$f'$ is positive", r"$f$ is positive"], "A",
            r"Concave up means $f'' > 0$, so $f'$ is increasing."),
        MCQ(r"On an interval where the graph of $f$ is concave down,", [r"$f$ is decreasing", r"$f'$ is decreasing", r"$f'$ is negative", r"$f$ is negative"], "B",
            r"Concave down means $f'' < 0$, so $f'$ is decreasing."),
        MCQ(r"If $f'$ is increasing on an interval, then on that interval the graph of $f$ is", [r"increasing", r"decreasing", r"concave down", r"concave up"], "D",
            r"$f'$ increasing means $f'' > 0$: concave up."),
    ),
    Variants(
        Item(r"Where is $f(x) = xe^{x}$ concave down? Enter the right endpoint of the interval.", num(-2), r"$f''(x) = (x + 2)e^x < 0$ for $x < -2$.", work="1.8cm"),
        Item(r"Where is $f(x) = xe^{-x}$ concave down? Enter the right endpoint of the interval.", num(2), r"$f''(x) = (x - 2)e^{-x} < 0$ for $x < 2$.", work="1.8cm"),
        Item(r"Where is $f(x) = x^2e^{x}$ concave down? Enter the right endpoint of the interval.", num(-2 + sp.sqrt(2)),
             r"$f''(x) = (x^2 + 4x + 2)e^x < 0$ between $-2 - \sqrt2$ and $-2 + \sqrt2$.", work="2cm"),
    ),
]
same("q", [inflections(x**2 * sp.exp(x))], [[-2 - sp.sqrt(2), -2 + sp.sqrt(2)]])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"The graph of $f(x) = x^4 - 4x^3 + 10$ is concave down on", [r"$(0, 2)$", r"$(-\infty, 0)$", r"$(2, \infty)$", r"$(0, 3)$"], "A", r"$f''(x) = 12x(x - 2) < 0$ on $(0, 2)$."),
    MCQ(r"At which point is $f(x) = x^3 - 3x^2 + 1$ changing concavity?", [r"$(0, 1)$", r"$(2, -3)$", r"$(1, -1)$", r"$(3, 1)$"], "C", r"$f''(x) = 6x - 6$ changes sign at $1$; $f(1) = -1$."),
    MCQ(r"$f'(x) = x^3 - 3x$. The graph of $f$ has points of inflection at", [r"$x = 0$ only", r"$x = \pm\sqrt3$", r"$x = \pm 1$ and $0$", r"$x = \pm 1$"], "D",
        r"$f''(x) = 3x^2 - 3$ changes sign at $\pm 1$.", why_not={"B": "those are the zeros of $f'$"}),
    MCQ(r"$f''(x) = \cos\left(x^2\right) - 0.2$. How many points of inflection does $f$ have on $(0, 3)$?", [r"$2$", r"$3$", r"$4$", r"$1$"], "B",
        r"$\cos\left(x^2\right) = 0.2$ where $x^2 \approx 1.369, 4.914, 7.652$: three sign changes in $(0, 3)$.", calc=True),
]
cands = [sp.sqrt(sp.acos(sp.Rational(1, 5))), sp.sqrt(2 * sp.pi - sp.acos(sp.Rational(1, 5))), sp.sqrt(2 * sp.pi + sp.acos(sp.Rational(1, 5)))]
same("m4", [int(all(0 < float(c) < 3 for c in cands)), int(float(sp.sqrt(4 * sp.pi - sp.acos(sp.Rational(1, 5)))) > 3)], [1, 1])

FRQS = [
    FRQ("Concavity and inflection", (r"Let $f(x) = x^4 - 6x^3 + 12x^2$."), [
        Part("a", r"Find $f''(x)$.", selfcheck(r"12x^2 - 36x + 24"), r"$f'(x) = 4x^3 - 18x^2 + 24x$, so $f''(x) = 12x^2 - 36x + 24 = 12(x - 1)(x - 2)$.", [(1, "$f''$")], work="1.8cm"),
        Part("b", r"On what interval is the graph of $f$ concave down? Justify.", selfcheck(r"(1, 2)"),
             r"$f''(x) = 12(x - 1)(x - 2) < 0$ on $(1, 2)$, so the graph is concave down there.", [(1, "interval"), (1, "reason using $f''$")], work="2cm"),
        Part("c", r"Find the $x$-coordinates of the points of inflection of $f$. Justify. Enter the larger one.", num(2),
             r"$f''$ changes sign at $x = 1$ (from $+$ to $-$) and at $x = 2$ (from $-$ to $+$), so both are points of inflection.", [(1, "both $x$-values"), (1, "sign-change reason")], work="2cm"),
    ], frq_type="Analyzing a function"),
]
same("frq", [inflections(x**4 - 6 * x**3 + 12 * x**2)], [[1, 2]])

TOPIC = Topic(
    number="5.6", title="Determining Concavity of Functions over Their Domains",
    unit="Unit 5: Analytical Applications of Differentiation", ced=["FUN-4.A", "FUN-4.A.4", "FUN-4.A.5", "FUN-4.A.6"],
    goals=r"Use the sign of $f''$ to find where a graph is concave up or down, and find points of inflection.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
