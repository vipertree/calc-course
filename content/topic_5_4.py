"""Topic 5.4: Using the First Derivative Test to determine relative (local) extrema.

CED: FUN-4.A (FUN-4.A.2): at a critical point, f' changing from + to - gives a relative max, - to + a relative min, no
change gives neither. AP justification: "because f' changes from positive to negative at x = c."
Worked examples: x^4 - 4x^3 (a critical point that is not an extremum), x + 2 sin x on (0, 2 pi), and a given
f'(x) = (x - 1)(x + 2)e^x.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Text, Topic, Variants, Video, num,
                     same, selfcheck, check, expr)

x = sp.symbols("x", real=True)


def fdt(fp, lo=-sp.oo, hi=sp.oo):
    """Classify each critical point (zeros of fp) in (lo, hi) by the sign of fp on either side: {c: 'max' | 'min' | 'neither'}."""
    cs = sorted(c for c in sp.solveset(fp, x, sp.Interval.open(lo, hi)))
    out = {}
    for c in cs:
        l, r = fp.subs(x, c - sp.Rational(1, 1000)), fp.subs(x, c + sp.Rational(1, 1000))
        out[c] = "max" if l > 0 > r else "min" if l < 0 < r else "neither"
    return out


assert fdt(sp.diff(x**4 - 4 * x**3, x)) == {0: "neither", 3: "min"}
assert fdt(1 + 2 * sp.cos(x), 0, 2 * sp.pi) == {2 * sp.pi / 3: "max", 4 * sp.pi / 3: "min"}
assert fdt((x - 1) * (x + 2) * sp.exp(x)) == {-2: "max", 1: "min"}

NOTES = [
    Video("s5_4.py::Lesson", "The first derivative test", 4),

    Section("Reading the sign change"),
    Formula("The First Derivative Test", (
        r"Let $c$ be a critical point of a continuous function $f$. \par "
        r"If $f'$ changes from \blank{positive} to \blank{negative} at $c$, $f$ has a relative \blank{maximum} at $c$. \par "
        r"If $f'$ changes from negative to positive at $c$, $f$ has a relative \blank{minimum} at $c$. \par "
        r"If $f'$ does not change sign at $c$, $f$ has \blank{no} relative extremum at $c$.")),
    Text(r"Uphill then downhill is a peak. Downhill then uphill is a valley. Uphill, flat for an instant, then uphill again is neither."),

    Section("Writing the justification"),
    Text(r"On the AP exam, a correct answer without a reason earns no credit. The reason names $f'$ and its sign change: "
         r"``$f$ has a relative maximum at $x = 2$ \blank{because} $f'$ changes from positive to negative there.''"),
    Text(r"\textbf{Not enough:} ``because $f'(2) = 0$'' (that only makes $2$ a critical point) or ``because the graph goes up then down'' (that describes $f$, not $f'$)."),
    VideoExample('From a sign chart', work="3cm"),
    BigIdea(r"A relative extremum is a sign change of $f'$: $+$ to $-$ is a max, $-$ to $+$ is a min, no change is neither. Always justify with $f'$."),
    Check(r"$f'$ changes from negative to positive at $x = -1$. What does $f$ have there?", selfcheck(r"\text{a relative minimum}"), r"A relative minimum."),
]

# ---------------------------------------------------------------- practice
P = [
    (x**3 - 3 * x**2 - 9 * x, "relative maximum"),
    (x**3 - 12 * x, "relative minimum"),
    (x**4 - 2 * x**2, "relative maximum"),
    (2 * x**3 - 9 * x**2 + 12 * x, "relative minimum"),
    (x * sp.exp(-x), "relative maximum"),
    (x**2 * sp.exp(x), "relative maximum"),
    (x - 2 * sp.log(x), "relative minimum"),
]
PRACTICE = []
for f, ask in P:
    pos = f.has(sp.log)
    fp = sp.diff(f, x)
    cls = fdt(fp, 0 if pos else -sp.oo)
    want = [c for c, k in cls.items() if k == ask.split()[1][:3]]
    assert len(want) == 1, (f, cls)
    PRACTICE.append(Item(rf"Find the $x$-value of the {ask} of $f(x) = {sp.latex(f)}$" + (r" for $x > 0$" if pos else "") + ". Justify your answer.", num(want[0]),
                         rf"$f'(x) = {sp.latex(sp.factor(sp.together(fp)))}$. " + "; ".join(
                             rf"at $x = {sp.latex(c)}$: " + {"max": r"$f'$ changes from $+$ to $-$, a relative maximum", "min": r"$f'$ changes from $-$ to $+$, a relative minimum",
                                                             "neither": r"no sign change, no extremum"}[k] for c, k in cls.items()) + ".", work="2.6cm"))
PRACTICE += [
    Item(r"$f'(x) = (x - 2)^2(x + 1)$. Classify each critical point of $f$. How many relative extrema does $f$ have?", num(1),
         r"At $-1$: $f'$ changes $-$ to $+$, a relative minimum. At $2$: no sign change. So one extremum.", work="2.2cm"),
    Item(r"$f'(x) = \dfrac{x - 3}{x^2 + 1}$. Does $f$ have a relative maximum or minimum at $x = 3$? Justify.", selfcheck(r"\text{minimum}"),
         r"The denominator is positive, so $f'$ has the sign of $x - 3$: negative then positive. A relative minimum, because $f'$ changes from negative to positive.", work="2cm"),
    Item(r"$g'(x) = x^{1/3}(x - 5)$. Where does $g$ have a relative maximum?", num(0),
         r"Critical points $0$ ($g'$ zero there) and $5$. Signs: $+$ on $(-\infty, 0)$ (negative times negative), $-$ on $(0, 5)$, $+$ after. Relative max at $0$.", work="2.4cm"),
    Item(r"The graph of $f'$ crosses the $x$-axis from above to below at $x = 4$, and touches the axis without crossing at $x = 1$. Where does $f$ have a relative maximum?",
         num(4), r"At $x = 4$, $f'$ changes from positive to negative. At $x = 1$ it doesn't change sign.", work="1.6cm"),
    Item(r"Kai writes: ``$f$ has a relative minimum at $x = 2$ because $f'(2) = 0$.'' What is missing?", selfcheck(r"\text{the sign change of } f'"),
         r"$f'(2) = 0$ only makes $2$ a critical point. The justification needs $f'$ to change from negative to positive at $2$.", work="1.6cm"),
]
assert fdt((x - 2)**2 * (x + 1)) == {-1: "min", 2: "neither"}

# ---------------------------------------------------------------- quiz
def q_item(f, ask):
    cls = fdt(sp.diff(f, x))
    c = [c for c, k in cls.items() if k == ask][0]
    word = {"max": "maximum", "min": "minimum"}[ask]
    return Item(rf"Find the $x$-value of the relative {word} of $f(x) = {sp.latex(f)}$, and justify it.", num(c),
                rf"$f'(x) = {sp.latex(sp.factor(sp.diff(f, x)))}$ changes from {'$+$ to $-$' if ask == 'max' else '$-$ to $+$'} at $x = {sp.latex(c)}$.", work="2.2cm")


QUIZ = [
    Variants(q_item(x**3 - 3 * x, "max"), q_item(x**3 - 27 * x, "max"), q_item(x**3 + 3 * x**2, "max")),
    Variants(q_item(x**3 - 6 * x**2, "min"), q_item(x**3 - 3 * x**2 - 24 * x, "min"), q_item(x**4 - 4 * x**3, "min")),
    Variants(
        MCQ(r"$f'(x) = (x + 3)(x - 1)^2$. At $x = 1$, $f$ has", [r"a relative maximum", r"a relative minimum", r"neither", r"a point where $f$ is undefined"], "C",
            r"$(x - 1)^2 \ge 0$, so $f'$ keeps the sign of $x + 3$ (positive) on both sides of $1$."),
        MCQ(r"$f'(x) = x^2(x - 2)$. At $x = 0$, $f$ has", [r"neither", r"a relative maximum", r"a relative minimum", r"a point where $f$ is undefined"], "A",
            r"$f'$ is negative on both sides of $0$."),
        MCQ(r"$f'(x) = (x - 4)^2(x + 2)$. At $x = 4$, $f$ has", [r"a relative maximum", r"a relative minimum", r"a point where $f$ is undefined", r"neither"], "D",
            r"$f'$ is positive on both sides of $4$."),
    ),
    Variants(
        MCQ(r"Which justifies that $f$ has a relative maximum at $x = 3$?", [r"$f'(3) = 0$", r"$f'$ changes from positive to negative at $x = 3$",
            r"$f(3)$ is the largest value of $f$", r"$f'$ changes from negative to positive at $x = 3$"], "B", r"The First Derivative Test.", why_not={"A": "only makes $3$ a critical point"}),
        MCQ(r"Which justifies that $f$ has a relative minimum at $x = -1$?", [r"$f'(-1) = 0$", r"$f'$ changes from positive to negative at $x = -1$",
            r"$f'$ changes from negative to positive at $x = -1$", r"$f(-1) < 0$"], "C", r"The First Derivative Test.", why_not={"A": "only makes $-1$ a critical point"}),
        MCQ(r"Which justifies that $f$ has no relative extremum at $x = 2$, a critical point?", [r"$f'$ does not change sign at $x = 2$", r"$f'(2) = 0$",
            r"$f(2) = 0$", r"$f'$ changes from negative to positive at $x = 2$"], "A", r"No sign change, no extremum."),
    ),
    Variants(
        Item(r"$f'(x) = (x - 1)(x - 5)$. Find the $x$-value of the relative maximum of $f$.", num(1), r"$f'$: $+$, $-$, $+$. Max at $1$.", work="1.4cm"),
        Item(r"$f'(x) = (2 - x)(x + 4)$. Find the $x$-value of the relative maximum of $f$.", num(2), r"$f'$: $-$, $+$, $-$. Max at $2$.", work="1.4cm"),
        Item(r"$f'(x) = x(x + 6)$. Find the $x$-value of the relative minimum of $f$.", num(0), r"$f'$: $+$, $-$, $+$. Min at $0$.", work="1.4cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$f(x) = x^4 - 8x^2$ has relative minima at", [r"$x = 0$ only", r"$x = -2$ and $x = 2$", r"$x = -2, 0, 2$", r"$x = 2$ only"], "B",
        r"$f'(x) = 4x(x - 2)(x + 2)$: signs $-, +, -, +$. Minima at $\pm 2$; maximum at $0$."),
    MCQ(r"$f'(x) = (x - 1)(x - 2)^2(x - 3)^3$. How many relative extrema does $f$ have?", [r"$1$", r"$3$", r"$0$", r"$2$"], "D",
        r"$f'$ changes sign at $1$ and at $3$ (odd powers), not at $2$."),
    MCQ(r"$f'(x) = e^{x}\sin x$ on $(0, 2\pi)$. $f$ has a relative maximum at", [r"$x = \pi$", r"$x = \frac\pi2$", r"$x = \frac{3\pi}{2}$", r"none"], "A",
        r"$e^x > 0$; $\sin x$ changes from $+$ to $-$ at $\pi$."),
    MCQ(r"$f'(x) = x^3 - 4x - 1$. At approximately what $x$ does $f$ have a relative maximum?", [r"$-1.861$", r"$2.115$", r"$-0.254$", r"$0.254$"], "C",
        r"The roots of $f'$ are about $-1.861$, $-0.254$ and $2.115$; $f'$ goes $-, +, -, +$, so the maximum is at $-0.254$.", calc=True),
]
rts = sorted(sp.nroots(x**3 - 4 * x - 1))
same("m4", [round(float(r), 3) for r in rts], [-1.861, -0.254, 2.115])

FRQS = [
    FRQ("Extrema from a derivative", (
        r"Let $f$ be a twice-differentiable function with $f(0) = 3$ and $f'(x) = (x - 1)(x + 2)e^{x}$ for all real numbers $x$. "
        r"It can be shown that $f''(x) = (x^2 + 3x - 1)e^{x}$."), [
        Part("a", r"Find the $x$-coordinate of each relative extremum of $f$, and classify each as a relative minimum or a relative "
                  r"maximum. Justify your answers.",
             selfcheck(r"\text{relative maximum at } x = -2;\ \text{relative minimum at } x = 1"),
             r"$f'(x) = 0$ at $x = -2$ and $x = 1$. $f'$ changes from positive to negative at $x = -2$, so $f$ has a relative maximum "
             r"there. $f'$ changes from negative to positive at $x = 1$, so $f$ has a relative minimum there.",
             [(1, "relative maximum at $x = -2$ with justification"), (1, "relative minimum at $x = 1$ with justification")],
             work="3cm"),
        Part("b", r"Write an equation for the line tangent to the graph of $f$ at $x = 0$.", expr("3 - 2*x"),
             r"$f'(0) = (-1)(2)(1) = -2$ and $f(0) = 3$, so the tangent line is $y = 3 - 2x$.",
             [(1, "$f'(0) = -2$"), (1, "tangent line equation")], work="2cm"),
        Part("c", r"Use the tangent line from part (b) to approximate $f(0.1)$. Is this approximation an overestimate or an "
                  r"underestimate of $f(0.1)$? Give a reason for your answer.", num(sp.Rational(14, 5)),
             r"$f(0.1) \approx 3 - 2(0.1) = 2.8$. For $0 \le x \le 0.1$, $x^2 + 3x - 1 < 0$, so $f''(x) < 0$ and the graph of $f$ is "
             r"concave down, lying below its tangent line. The approximation is an overestimate.",
             [(1, "approximation $2.8$"), (1, "overestimate, because $f'' < 0$ on $0 \\le x \\le 0.1$")], work="2.6cm"),
    ], frq_type="Function analysis"),
]
fp4 = (x - 1) * (x + 2) * sp.exp(x)
same("frq a", sorted(sp.solve(fp4, x)), [-2, 1])
check("frq a signs", fp4.subs(x, -3) > 0 and fp4.subs(x, 0) < 0 and fp4.subs(x, 2) > 0)
same("frq f''", sp.simplify(sp.diff(fp4, x) - (x**2 + 3 * x - 1) * sp.exp(x)), 0)
same("frq b", fp4.subs(x, 0), -2)
same("frq c", 3 - 2 * sp.Rational(1, 10), sp.Rational(14, 5))
check("frq c sign", all((v**2 + 3 * v - 1) < 0 for v in (0, sp.Rational(1, 20), sp.Rational(1, 10))))

TOPIC = Topic(
    number="5.4", title="Using the First Derivative Test to Determine Relative (Local) Extrema",
    unit="Unit 5: Analytical Applications of Differentiation", ced=["FUN-4.A", "FUN-4.A.2"],
    goals=r"Classify critical points as relative maxima, minima or neither from the sign change of $f'$, and justify the answer.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
