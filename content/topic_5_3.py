"""Topic 5.3: Determining intervals on which a function is increasing or decreasing.

CED: FUN-4.A (FUN-4.A.1): f' > 0 on an interval means f increases there; f' < 0 means f decreases. Method: find where f' is
0 or undefined, then test the sign of f' between those points (a sign chart). Worked examples: x^3 - 12x + 1, x e^(-x),
and a given f'(x) = (x + 1)(x - 3)^2 (a sign that doesn't change at 3).
"""
import sympy as sp

from calclib.figs import graph
from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Text, Topic, Variants, Video, num,
                     same, selfcheck)

x = sp.symbols("x", real=True)


def incdec(fp, lo=-sp.oo, hi=sp.oo):
    """(increasing, decreasing) as sets, from the sign of f'."""
    return (sp.solve_univariate_inequality(fp > 0, x, relational=False).intersect(sp.Interval(lo, hi)),
            sp.solve_univariate_inequality(fp < 0, x, relational=False).intersect(sp.Interval(lo, hi)))


def seteq(label, got, want):
    """same() for sets of x: compares interval unions exactly."""
    same(label, [int(g == w) for g, w in zip(got, want)], [1] * len(want))


seteq("ex1", list(incdec(sp.diff(x**3 - 12 * x + 1, x))), [sp.Union(sp.Interval.open(-sp.oo, -2), sp.Interval.open(2, sp.oo)), sp.Interval.open(-2, 2)])
seteq("ex2", list(incdec(sp.diff(x * sp.exp(-x), x))), [sp.Interval.open(-sp.oo, 1), sp.Interval.open(1, sp.oo)])
seteq("ex3", list(incdec((x + 1) * (x - 3)**2)), [sp.Union(sp.Interval.open(-1, 3), sp.Interval.open(3, sp.oo)), sp.Interval.open(-sp.oo, -1)])

FIG_FP = graph("t5_3_fp", [("-x-2", -4, -2), ("-sqrt(abs(4-x^2))", -2, 2), ("x-2", 2, 4), ("2+0*x", 4, 6)], xr=(-4, 6), yr=(-3, 3),
               ylabel="f'(x)", caption="The graph of $f'$ (not $f$): two segments, a semicircle, and a flat segment.")
FIG_PQ = graph("t5_3_pq", [("sqrt(abs(4-(x+1)^2))", -3, 1), ("-(x-1)", 1, 3), ("2*(x-3)-2", 3, 5)], xr=(-3, 5), yr=(-3, 3),
               ylabel="f'(x)", caption="The graph of $f'$: a semicircle and two line segments.")
FIG_F = graph("t5_3_f", [("(x^3-6*x^2+9*x)/2+1", 0, 4)], xr=(0, 4), yr=(0, 4), ylabel="f(x)", caption="The graph of $f$ (not $f'$).")

NOTES = [
    Video("s5_3.py::Lesson", "Uphill and downhill", 4),

    Section("The sign of the derivative"),
    Formula("Increasing and decreasing", (
        r"If $f'(x) > 0$ on an interval, $f$ is \blank{increasing} on that interval. \par "
        r"If $f'(x) < 0$ on an interval, $f$ is \blank{decreasing} on that interval.")),
    Text(r"Positive slope means the graph goes uphill as you read it left to right. The sign of $f'$ is what matters, not its size."),

    Section("Graphs of $f$ and $f'$"),
    Text(r"Stack the graph of $f'$ under the graph of $f$. Where $f$ climbs, the graph of $f'$ is \blank{above} the axis. Where $f$ falls, it is "
         r"\blank{below}. At a peak or valley of $f$, the graph of $f'$ crosses \blank{zero}."),
    Text(r"\textbf{Height is not slope.} $f$ can be positive while $f'$ is negative: the graph is above the axis but heading downhill. "
         r"The sign of $f$ says where the graph \emph{is}. The sign of $f'$ says which way it's \emph{going}."),
    Section("A sign chart"),
    Formula("Finding where $f$ increases and decreases", (
        r"\textbf{1.} Find $f'(x)$. \par \textbf{2.} Find where $f'(x) = 0$ or is undefined: the \blank{critical points}. \par "
        r"\textbf{3.} Mark them on a number line. Between them, $f'$ can't change sign, so test \blank{one} value in each piece. \par "
        r"\textbf{4.} Read off the answer: $+$ means increasing, $-$ means decreasing.")),
    VideoExample('Increasing from a sign chart', work="3cm"),
    Section("Reading the graph of $f'$"),
    Text(r"Given the graph of $f'$, you don't need a formula. Read its sign: \blank{above} the axis means $f$ is increasing, below means "
         r"$f$ is decreasing. Where the graph of $f'$ crosses from above to below, $f$ switches from increasing to decreasing. "
         r"Careful: if the graph of $f'$ is heading down but still above the axis, $f$ is still \blank{increasing}."),
    VideoExample('From the graph of f prime', work="3cm"),
    Text(r"\textbf{Justify with $f'$.} On the AP exam, say why: ``$f$ is increasing on $(2, \infty)$ because $f'(x) > 0$ there.'' "
         r"A sentence about the graph of $f$ alone doesn't earn the point."),
    BigIdea(r"The sign of $f'$ tells the direction of $f$. Critical points split the line into pieces, and $f'$ keeps one sign on each piece."),
    Check(r"On what interval is $f(x) = x^2 - 8x$ decreasing?", selfcheck(r"(-\infty, 4)"), r"$f'(x) = 2x - 8 < 0$ for $x < 4$."),
]

# ---------------------------------------------------------------- practice
P = [
    (x**2 - 6 * x + 1, "decreasing", "right", 3),
    (x**3 - 27 * x, "decreasing", "right", 3),
    (2 * x**3 + 3 * x**2 - 12 * x, "decreasing", "left", -2),
    (x**4 - 8 * x**2, "increasing", "left", -2),
    (x * sp.exp(x), "increasing", "left", -1),
    (sp.log(x) / x, "increasing", "right", sp.E),
    (x + 4 / x, "decreasing", "right", 2),
]
PRACTICE = []
for f, word, end, ans in P:
    pos = f.has(sp.log) or f == x + 4 / x
    fp = sp.factor(sp.together(sp.diff(f, x)))
    inc, dec = incdec(sp.diff(f, x), *((0, sp.oo) if pos else (-sp.oo, sp.oo)))
    first = (inc if word == "increasing" else dec)
    first = first.args[0] if isinstance(first, sp.Union) else first
    assert (first.left if end == "left" else first.right) == ans, (f, first)
    PRACTICE.append(Item(rf"$f(x) = {sp.latex(f)}$" + (r" for $x > 0$" if pos else "")
                         + rf". On what interval(s) is $f$ {word}? Enter the {end} endpoint of the first one.", num(ans),
                         rf"$f'(x) = {sp.latex(fp)}$. Increasing on ${sp.latex(inc)}$; decreasing on ${sp.latex(dec)}$.", work="2.6cm"))
PRACTICE += [
    Item(r"$f'(x) = (x - 2)(x + 5)$. On what interval is $f$ decreasing?", selfcheck(r"(-5, 2)"), r"$f' < 0$ between the roots: $(-5, 2)$.", work="1.8cm"),
    Item(r"$f'(x) = x^2(x - 4)$. Is $f$ increasing or decreasing on $(0, 4)$?", selfcheck(r"\text{decreasing}"), r"For $0 < x < 4$, $x^2 > 0$ and $x - 4 < 0$, so $f' < 0$.", work="1.6cm"),
    Item(r"$f'(x) = e^{x}(x - 1)^2$. Where is $f$ decreasing?", selfcheck(r"\text{nowhere}"),
         r"$e^x > 0$ and $(x - 1)^2 \ge 0$, so $f' \ge 0$ everywhere: $f$ is never decreasing.", work="1.6cm"),
    Item(r"The graph of $f'$ is above the $x$-axis on $(-3, 1)$ and below it elsewhere. Where is $f$ increasing? Enter the left endpoint.", num(-3),
         r"$f' > 0$ on $(-3, 1)$, so $f$ increases there.", work="1.4cm"),
    Item(r"$f(x) = \sin x + \cos x$ on $(0, 2\pi)$. On what interval is $f$ decreasing? Enter the left endpoint.", num(sp.pi / 4),
         r"$f'(x) = \cos x - \sin x < 0$ on $\left(\frac\pi4, \frac{5\pi}{4}\right)$.", work="2.4cm"),
]
PRACTICE += [
    Item(r"The graph of $f'$ is shown. On what open intervals is $f$ increasing?", selfcheck(r"(-3, 1) \text{ and } (4, 5)"),
         r"$f' > 0$ where its graph is above the axis: on $(-3, 1)$ (the semicircle) and on $(4, 5)$.", work="1.6cm", figure=FIG_PQ),
    Item(r"The graph of $f'$ is shown. At what value of $x$ does $f$ switch from increasing to decreasing?", num(1),
         r"The graph of $f'$ crosses from above the axis to below at $x = 1$.", work="1.4cm", figure=FIG_PQ),
    Item(r"The graph of $f'$ is shown. The graph of $f'$ is decreasing on $(-1, 1)$. Is $f$ increasing or decreasing on $(-1, 1)$? Explain.",
         selfcheck(r"\text{increasing}"), r"Increasing: $f'$ is still positive on $(-1, 1)$ (above the axis), even though it's heading down.",
         work="1.6cm", figure=FIG_PQ),
    Item(r"The graph of $f$ is shown. On what open interval is $f'(x) < 0$?", selfcheck(r"(1, 3)"),
         r"$f$ is decreasing from its peak at $x = 1$ to its valley at $x = 3$, so $f' < 0$ on $(1, 3)$.", work="1.4cm", figure=FIG_F),
    Item(r"The graph of $f$ is shown. Is $f(2)$ positive or negative? Is $f'(2)$ positive or negative?", selfcheck(r"f(2) > 0,\ f'(2) < 0"),
         r"The graph is above the axis at $x = 2$ but heading downhill: $f(2) = 2 > 0$ and $f'(2) < 0$.", work="1.4cm", figure=FIG_F),
]
seteq("p", [incdec(sp.cos(x) - sp.sin(x), 0, 2 * sp.pi)[1], incdec((x - 2) * (x + 5))[1]], [sp.Interval.open(sp.pi / 4, 5 * sp.pi / 4), sp.Interval.open(-5, 2)])
seteq("p2", [incdec(sp.diff(sp.log(x) / x, x), 0, sp.oo)[0], incdec(sp.diff(x + 4 / x, x), 0, sp.oo)[1], incdec(sp.diff(x * sp.exp(x), x))[0]],
     [sp.Interval.open(0, sp.E), sp.Interval.open(0, 2), sp.Interval.open(-1, sp.oo)])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(*[Item(rf"On what interval is $f(x) = {sp.latex(f)}$ decreasing?", selfcheck(sp.latex(incdec(sp.diff(f, x))[1])),
                    rf"$f'(x) = {sp.latex(sp.factor(sp.diff(f, x)))} < 0$ on ${sp.latex(incdec(sp.diff(f, x))[1])}$.", work="2cm")
               for f in (x**3 - 3 * x, x**3 - 6 * x**2, x**3 - 12 * x + 5)]),
    Variants(
        Item(r"$f'(x) = (x + 2)(x - 6)$. On what interval is $f$ decreasing?", selfcheck(r"(-2, 6)"), r"$f' < 0$ between the roots.", work="1.4cm"),
        Item(r"$f'(x) = (3 - x)(x + 1)$. On what interval is $f$ increasing?", selfcheck(r"(-1, 3)"), r"$f' > 0$ between the roots (the parabola opens down).", work="1.4cm"),
        Item(r"$f'(x) = x(x - 5)$. On what interval is $f$ decreasing?", selfcheck(r"(0, 5)"), r"$f' < 0$ between the roots.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"$f'(x) = (x - 1)^2(x + 3)$. On which interval is $f$ increasing?", [r"$(-3, 1)$ only", r"$(1, \infty)$ only", r"$(-3, \infty)$", r"$(-\infty, -3)$"], "C",
            r"$(x - 1)^2 \ge 0$, so the sign of $f'$ is the sign of $x + 3$."),
        MCQ(r"$f'(x) = x^2(2 - x)$. On which interval is $f$ decreasing?", [r"$(2, \infty)$", r"$(0, 2)$", r"$(-\infty, 0)$", r"$(-\infty, 2)$"], "A",
            r"$x^2 \ge 0$, so the sign of $f'$ is the sign of $2 - x$."),
        MCQ(r"$f'(x) = (x + 2)^2(x - 4)$. On which interval is $f$ decreasing?", [r"$(-2, 4)$ only", r"$(4, \infty)$", r"$(-\infty, -2)$ only", r"$(-\infty, 4)$"], "D",
            r"$(x + 2)^2 \ge 0$, so the sign of $f'$ is the sign of $x - 4$."),
    ),
    Variants(
        Item(r"Where is $f(x) = xe^{-2x}$ increasing? Enter the right endpoint.", num(sp.Rational(1, 2)), r"$f'(x) = (1 - 2x)e^{-2x} > 0$ for $x < \frac12$.", work="1.8cm"),
        Item(r"Where is $f(x) = x^2e^{x}$ decreasing? Enter the left endpoint.", num(-2), r"$f'(x) = x(x + 2)e^{x} < 0$ on $(-2, 0)$.", work="1.8cm"),
        Item(r"Where is $f(x) = x - \ln x$ increasing? Enter the left endpoint.", num(1), r"$f'(x) = 1 - \frac1x > 0$ for $x > 1$.", work="1.8cm"),
    ),
    Variants(
        MCQ(r"Which is a correct justification that $f$ is increasing on $(2, 5)$?", [r"$f(x) > 0$ on $(2, 5)$", r"$f'(x) > 0$ on $(2, 5)$", r"$f''(x) > 0$ on $(2, 5)$", r"$f(5) > f(2)$"], "B",
            r"The sign of $f'$ decides it.", why_not={"D": "$f$ could dip in between"}),
        MCQ(r"Which is a correct justification that $g$ is decreasing on $(0, 3)$?", [r"$g(x) < 0$ on $(0, 3)$", r"$g(3) < g(0)$", r"$g'(x) < 0$ on $(0, 3)$", r"$g''(x) < 0$ on $(0, 3)$"], "C",
            r"The sign of $g'$ decides it.", why_not={"B": "$g$ could rise in between"}),
        MCQ(r"Which is a correct justification that $h$ is increasing on $(-1, 1)$?", [r"$h'(x) > 0$ on $(-1, 1)$", r"$h(x) > 0$ on $(-1, 1)$", r"$h(1) > h(-1)$", r"$h''(x) > 0$ on $(-1, 1)$"], "A",
            r"The sign of $h'$ decides it."),
    ),
]
seteq("q", [incdec(sp.diff(x * sp.exp(-2 * x), x))[0], incdec(sp.diff(x**2 * sp.exp(x), x))[1], incdec(sp.diff(x - sp.log(x), x), 0, sp.oo)[0]],
     [sp.Interval.open(-sp.oo, sp.Rational(1, 2)), sp.Interval.open(-2, 0), sp.Interval.open(1, sp.oo)])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"On which interval is $f(x) = x^4 - 4x^3$ decreasing?", [r"$(0, 3)$ only", r"$(3, \infty)$", r"$(-\infty, 0)$ only", r"$(-\infty, 3)$"], "D",
        r"$f'(x) = 4x^2(x - 3) \le 0$ for $x < 3$ (zero only at $x = 0$)."),
    MCQ(r"$f'(x) = \dfrac{x - 4}{x^2 + 1}$. On which interval is $f$ increasing?", [r"$(4, \infty)$", r"$(-1, 4)$", r"$(-\infty, 4)$", r"$(-1, 1)$"], "A",
        r"The denominator is always positive; $f' > 0$ when $x > 4$."),
    MCQ(r"$g(x) = \ln\left(x^2 + 4\right)$ is decreasing on", [r"$(0, \infty)$", r"$(-\infty, 0)$", r"$(-2, 2)$", r"nowhere"], "B",
        r"$g'(x) = \frac{2x}{x^2 + 4} < 0$ for $x < 0$."),
    MCQ(r"$f'(x) = \cos\left(x^2\right)$. On $[0, 2]$, $f$ is increasing on", [r"$[0, 2]$", r"$\left[\sqrt{\pi/2}, 2\right]$", r"$\left[0, \sqrt{\pi/2}\right]$", r"$[0, 1]$ only"], "C",
        r"$\cos\left(x^2\right) > 0$ while $x^2 < \frac\pi2$.", calc=True),
]
seteq("m", [incdec(sp.diff(x**4 - 4 * x**3, x))[1], incdec((x - 4) / (x**2 + 1))[0], incdec(sp.diff(sp.log(x**2 + 4), x))[1]],
     [sp.Union(sp.Interval.open(-sp.oo, 0), sp.Interval.open(0, 3)), sp.Interval.open(4, sp.oo), sp.Interval.open(-sp.oo, 0)])

FRQS = [
    FRQ("Reading the sign of a derivative", (
        r"Let $f$ be a twice-differentiable function whose derivative is given by $f'(x) = (x^2 - 4)e^{-x}$ for all real numbers $x$."), [
        Part("a", r"On what open intervals is $f$ increasing? Justify your answer.",
             selfcheck(r"(-\infty, -2) \text{ and } (2, \infty)"),
             r"$e^{-x} > 0$, so $f'(x)$ has the sign of $x^2 - 4$. $f'(x) > 0$ for $x < -2$ and for $x > 2$, so $f$ is increasing on "
             r"$(-\infty, -2)$ and $(2, \infty)$.",
             [(1, "intervals"), (1, "reason: $f'(x) > 0$ there")], work="2.6cm"),
        Part("b", r"Which is greater, $f(0)$ or $f(1)$? Give a reason for your answer.", selfcheck(r"f(0)"),
             r"$f'(x) < 0$ for $-2 < x < 2$, so $f$ is decreasing on $0 \le x \le 1$. Therefore $f(0) > f(1)$.",
             [(1, "$f(0)$, because $f$ is decreasing on $0 \\le x \\le 1$")], work="2cm"),
        Part("c", r"Find $f''(0)$. Is $f'$ increasing or decreasing at $x = 0$? Give a reason for your answer.", num(4),
             r"$f''(x) = 2xe^{-x} - (x^2 - 4)e^{-x}$, so $f''(0) = 0 + 4 = 4$. Since $f''(0) > 0$, $f'$ is increasing at $x = 0$.",
             [(1, "$f''(0) = 4$"), (1, "increasing, because $f''(0) > 0$")], work="2.4cm"),
    ], frq_type="Function analysis"),
]
seteq("frq", list(incdec((x**2 - 4) * sp.exp(-x))), [sp.Union(sp.Interval.open(-sp.oo, -2), sp.Interval.open(2, sp.oo)), sp.Interval.open(-2, 2)])
same("frq c", sp.diff((x**2 - 4) * sp.exp(-x), x).subs(x, 0), 4)

TOPIC = Topic(
    number="5.3", title="Determining Intervals on Which a Function Is Increasing or Decreasing",
    unit="Unit 5: Analytical Applications of Differentiation", ced=["FUN-4.A", "FUN-4.A.1"],
    goals=r"Use the sign of $f'$ to find where $f$ increases and decreases, with a sign chart and a justification.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
