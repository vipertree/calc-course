"""Topic 6.2: Approximating areas with Riemann sums.

CED: LIM-5.A (LIM-5.A.1-LIM-5.A.4): left, right, midpoint and trapezoidal sums, with uniform or nonuniform partitions,
from graphs, tables and formulas; whether a sum over- or underestimates, from where f increases/decreases (left/right)
and its concavity (trapezoid). Worked examples: right sum for 1/x on [1, 3]; trapezoids from an uneven table; ordering
L, T, A, R for an increasing, concave-down f.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, num, same,
                     selfcheck)
from calclib.figs import graph

x = sp.symbols("x", real=True)


def rsum(f, edges, kind):
    """Riemann or trapezoidal sum of f (a sympy expression or a dict of table values) on the partition `edges`."""
    val = (lambda s: f[s]) if isinstance(f, dict) else (lambda s: f.subs(x, s))
    tot = 0
    for a, b in zip(edges, edges[1:]):
        w = b - a
        tot += w * {"left": val(a), "right": val(b), "mid": val((a + b) / sp.Integer(2)) if not isinstance(f, dict) else None,
                    "trap": (val(a) + val(b)) / sp.Integer(2)}[kind]
    return sp.nsimplify(tot)


F = x**2 / 4 + 1
E4 = [0, 1, 2, 3, 4]
same("lesson sums", [rsum(F, E4, k) for k in ("left", "right", "mid", "trap")], [sp.Rational(15, 2), sp.Rational(23, 2), sp.Rational(37, 4), sp.Rational(19, 2)])
TAB = {0: 4, 2: 6, 5: 7, 9: 5, 10: 3}
same("uneven", [rsum(TAB, [0, 2, 5, 9, 10], "left")], [59])
same("ex1", [rsum(1 / x, [1, sp.Rational(3, 2), 2, sp.Rational(5, 2), 3], "right")], [sp.Rational(19, 20)])
same("ex2", [rsum({0: 2, 1: 5, 3: 7, 4: 4}, [0, 1, 3, 4], "trap")], [21])

FIG_G = graph("t6_2_g", [("4-0.25*x^2", 0, 4)], xr=(0, 4), yr=(0, 5), ylabel="g(x)", caption="The graph of $g(x) = 4 - \\frac14x^2$.")

NOTES = [
    Video("s6_2.py::Lesson", "Riemann sums", 6),

    Section("Rectangles and trapezoids"),
    Text(r"To approximate the area under a curve, split the interval into pieces, put a simple shape on each piece, and add up their areas. "
         r"The width of a piece is $\Delta x$; with $n$ equal pieces of $[a, b]$, $\Delta x = \frac{b - a}{n}$."),
    Formula("Riemann sums", (
        r"\textbf{Left} sum: each height is $f$ at the \blank{left} end of its piece. \par "
        r"\textbf{Right} sum: each height is $f$ at the right end. \par "
        r"\textbf{Midpoint} sum: each height is $f$ at the \blank{middle} of its piece. \par "
        r"\textbf{Trapezoidal} sum: each piece is a trapezoid, area $= (\text{width}) \cdot \frac{\text{left height} + \text{right height}}{2}$. "
        r"With equal widths, $T = \frac{L + R}{2}$.")),
    Text(r"\textbf{Uneven widths.} With a table, the pieces often have different widths. Give each shape its own width: $\sum (\text{height})(\text{width})$."),
    VideoExample('Uneven widths', work="2.6cm"),

    Section("Over or under?"),
    Formula("Over- and underestimates", (
        r"$f$ increasing: left sum \blank{under}estimates, right sum overestimates. \par "
        r"$f$ decreasing: left sum overestimates, right sum underestimates. \par "
        r"$f$ concave up (a bowl): trapezoidal sum \blank{over}estimates. \par "
        r"$f$ concave down (a hill): trapezoidal sum underestimates.")),
    Text(r"For $f(x) = \frac14x^2 + 1$ on $[0, 4]$ with four pieces: $L = 7.5$, $R = 11.5$, $M = 9.25$, $T = 9.5$; the true area is $\frac{28}{3} \approx 9.33$."),
    BigIdea(r"A Riemann sum adds heights times widths. Left, right and midpoint say where each height comes from; trapezoids average the two sides. "
            r"Increasing/decreasing decides left and right over or under; concavity decides trapezoids."),
    Check(r"Find the left sum for $f(x) = x^2$ on $[0, 2]$ with $2$ equal pieces.", num(1), r"$\Delta x = 1$: $1 \cdot f(0) + 1 \cdot f(1) = 0 + 1 = 1$."),
]

# ---------------------------------------------------------------- practice
P = [(x**2, 0, 4, 4, "right"), (x**2, 0, 4, 4, "left"), (x**3, 0, 2, 4, "mid"), (sp.sqrt(x), 0, 4, 4, "trap"), (1 / x, 1, 2, 2, "trap"), (4 - x**2 / 4, 0, 4, 4, "left")]
NAME = {"left": "left Riemann sum", "right": "right Riemann sum", "mid": "midpoint sum", "trap": "trapezoidal sum"}
PRACTICE = []
for f, a, b, n, k in P:
    edges = [a + sp.Rational(b - a, n) * i for i in range(n + 1)]
    v = rsum(f, edges, k)
    PRACTICE.append(Item(rf"Use a {NAME[k]} with ${n}$ equal subintervals to approximate the area under $f(x) = {sp.latex(f)}$ on $[{a}, {b}]$.", num(v),
                         rf"$\Delta x = {sp.latex(sp.Rational(b - a, n))}$; the {NAME[k]} is ${sp.latex(v)}$.", work="2.4cm"))
PRACTICE += [
    Item(r"The table gives $r(t)$: $t = 0, 3, 4, 8$ hours; $r(t) = 10, 14, 12, 6$ gallons per hour. Use a right Riemann sum with the subintervals in the table to approximate "
         r"the total gallons from $t = 0$ to $t = 8$.", num(78), r"Widths $3, 1, 4$: $3(14) + 1(12) + 4(6) = 42 + 12 + 24 = 78$ gallons.", work="1.8cm"),
    Item(r"Using the same table, find the trapezoidal approximation of the total gallons from $t = 0$ to $t = 8$.", num(85),
         r"$3 \cdot \frac{10 + 14}{2} + 1 \cdot \frac{14 + 12}{2} + 4 \cdot \frac{12 + 6}{2} = 36 + 13 + 36 = 85$ gallons.", work="1.8cm"),
    Item(r"$f$ is decreasing on $[0, 5]$. Is a left Riemann sum for the area under $f$ an overestimate or an underestimate?", selfcheck(r"\text{overestimate}"),
         r"Decreasing: each left end is the high point of its piece, so the left sum is too big.", work="1.2cm"),
    Item(r"The graph of $g$ is shown. Is a trapezoidal sum for the area under $g$ on $[0, 4]$ an overestimate or an underestimate?", selfcheck(r"\text{underestimate}"),
         r"$g$ is concave down (a hill), so the trapezoid tops sit below the curve: an underestimate.", work="1.2cm", figure=FIG_G),
    Item(r"$f$ is increasing and concave up on $[a, b]$. Which is larger: the trapezoidal sum or the right sum, with the same partition?", selfcheck(r"\text{the right sum}"),
         r"$T = \frac{L + R}{2}$ and $L < R$, so $T < R$.", work="1.2cm"),
]
same("p tab", [rsum({0: 10, 3: 14, 4: 12, 8: 6}, [0, 3, 4, 8], "right"), rsum({0: 10, 3: 14, 4: 12, 8: 6}, [0, 3, 4, 8], "trap")], [78, 85])

# ---------------------------------------------------------------- quiz
def q(f, a, b, n, k):
    edges = [a + sp.Rational(b - a, n) * i for i in range(n + 1)]
    v = rsum(f, edges, k)
    return Item(rf"Use a {NAME[k]} with ${n}$ equal subintervals to approximate the area under $f(x) = {sp.latex(f)}$ on $[{a}, {b}]$.", num(v),
                rf"$\Delta x = {sp.latex(sp.Rational(b - a, n))}$: ${sp.latex(v)}$.", work="2cm")


QUIZ = [
    Variants(q(x**2 + 1, 0, 3, 3, "left"), q(x**2 + 1, 0, 3, 3, "right"), q(2 * x + 1, 0, 4, 4, "left")),
    Variants(q(x**2, 0, 4, 2, "mid"), q(x**2, 1, 5, 2, "mid"), q(x**3, 0, 4, 2, "mid")),
    Variants(q(x**2, 0, 4, 4, "trap"), q(x**2, 0, 2, 2, "trap"), q(x**3, 0, 2, 2, "trap")),
    Variants(*[Item(rf"Table: $x = {', '.join(map(str, xs))}$; $f(x) = {', '.join(map(str, ys))}$. Find the {NAME[k]} with the subintervals in the table.",
                    num(rsum(dict(zip(xs, ys)), xs, k)), rf"Widths ${', '.join(str(b - a) for a, b in zip(xs, xs[1:]))}$: the sum is ${rsum(dict(zip(xs, ys)), xs, k)}$.",
                    work="1.4cm")
               for xs, ys, k in (([0, 2, 3, 6], [1, 4, 5, 2], "left"), ([0, 2, 3, 6], [1, 4, 5, 2], "right"), ([0, 1, 4, 5], [3, 5, 1, 2], "trap"))]),
    Variants(
        MCQ(r"$f$ is increasing on $[0, 4]$. Which must be true about the left sum $L$, the right sum $R$ and the area $A$ under $f$?", [r"$L < A < R$", r"$R < A < L$",
            r"$A < L < R$", r"$L < R < A$"], "A", r"Increasing: left ends are low points, right ends are high points."),
        MCQ(r"$f$ is decreasing on $[0, 4]$. Which must be true about the left sum $L$, the right sum $R$ and the area $A$ under $f$?", [r"$L < A < R$", r"$R < A < L$",
            r"$A < L < R$", r"$L < R < A$"], "B", r"Decreasing: left ends are high points, right ends are low points."),
        MCQ(r"The graph of $f$ is concave up on $[0, 4]$. The trapezoidal sum $T$ and the area $A$ under $f$ satisfy", [r"$T < A$", r"$T = A$", r"$T > A$",
            r"it depends on whether $f$ is increasing"], "C", r"Concave up: the trapezoid tops sit above the curve."),
    ),
]
same("q4", [rsum({0: 1, 2: 4, 3: 5, 6: 2}, [0, 2, 3, 6], "left"), rsum({0: 1, 2: 4, 3: 5, 6: 2}, [0, 2, 3, 6], "right"), rsum({0: 3, 1: 5, 4: 1, 5: 2}, [0, 1, 4, 5], "trap")],
     [21, 19, sp.Rational(29, 2)])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"The trapezoidal sum with $2$ equal subintervals for the area under $f(x) = x^2$ on $[0, 4]$ is", [r"$16$", r"$20$", r"$24$", r"$32$"], "C",
        r"$\Delta x = 2$: $2 \cdot \frac{0 + 4}{2} + 2 \cdot \frac{4 + 16}{2} = 4 + 20 = 24$.", why_not={"A": "the left sum", "D": "the right sum"}),
    MCQ(r"Table: $t = 0, 1, 3, 6$; $v(t) = 2, 3, 5, 4$. The right Riemann sum with the subintervals in the table is", [r"$14$", r"$25$", r"$12$", r"$32$"], "B",
        r"Widths $1, 2, 3$: $1(3) + 2(5) + 3(4) = 3 + 10 + 12 = 25$.", why_not={"C": "the heights added without widths"}),
    MCQ(r"$f$ is positive, decreasing and concave up on $[a, b]$. Which approximation of the area under $f$ is an underestimate?", [r"the left sum",
        r"the trapezoidal sum", r"both the left and right sums", r"the right sum"], "D", r"Decreasing: the right sum is too small. Concave up: the trapezoidal sum is too big."),
    MCQ(r"The midpoint sum with $2$ equal subintervals for the area under $f(x) = x^3$ on $[0, 2]$ is", [r"$1$", r"$\frac72$", r"$4$", r"$5$"], "B",
        r"$\Delta x = 1$, midpoints $0.5$ and $1.5$: $1(0.125) + 1(3.375) = 3.5$.", why_not={"C": "the exact area", "D": "the trapezoidal sum"}),
]
same("m", [rsum(x**2, [0, 2, 4], "trap"), rsum({0: 2, 1: 3, 3: 5, 6: 4}, [0, 1, 3, 6], "right"), rsum(x**3, [0, 1, 2], "mid"), rsum(x**3, [0, 1, 2], "trap"),
           sp.integrate(x**3, (x, 0, 2))], [24, 25, sp.Rational(7, 2), 5, 4])

FRQS = [
    FRQ("Water into a tank", (
        r"Water flows into a tank at a rate modeled by a twice-differentiable, increasing function $R$, where $R(t)$ is measured in gallons per minute and $t$ is "
        r"measured in minutes. Selected values of $R(t)$ are given in the table."
        r"\par\smallskip\centerline{\begin{tabular}{c|ccccc} $t$ (minutes) & 0 & 2 & 5 & 9 & 10 \\ \hline "
        r"$R(t)$ (gallons per minute) & 4 & 6 & 7 & 9 & 12\end{tabular}}"), [
        Part("a", r"Use the data in the table to approximate $R'(7)$. Show the work that leads to your answer. Indicate units of measure.",
             num(sp.Rational(1, 2), display=r"0.5\ \text{gallons per minute per minute}"),
             r"$R'(7) \approx \dfrac{R(9) - R(5)}{9 - 5} = \dfrac{9 - 7}{4} = 0.5$ gallons per minute per minute.", [(1, "difference quotient and answer"), (1, "units")], work="2.2cm"),
        Part("b", r"Use a left Riemann sum with the four subintervals indicated by the table to approximate the amount of water that flows into the tank from $t = 0$ "
                  r"to $t = 10$. Show the computations that lead to your answer.", num(rsum({0: 4, 2: 6, 5: 7, 9: 9, 10: 12}, [0, 2, 5, 9, 10], "left"), display=r"63\ \text{gallons}"),
             r"$2(4) + 3(6) + 4(7) + 1(9) = 8 + 18 + 28 + 9 = 63$ gallons.", [(1, "left Riemann sum setup"), (1, "answer")], work="2.4cm"),
        Part("c", r"Is the approximation in part (b) an overestimate or an underestimate of the amount of water that flows into the tank? Give a reason for your answer.",
             selfcheck(r"\text{underestimate}"), r"$R$ is increasing, so on each subinterval the left endpoint gives the smallest value of $R$. The left Riemann sum is an underestimate.",
             [(1, "underestimate with reason")], work="1.8cm"),
    ], frq_type="Table"),
]
same("frq", [sp.Rational(9 - 7, 4), rsum({0: 4, 2: 6, 5: 7, 9: 9, 10: 12}, [0, 2, 5, 9, 10], "left")], [sp.Rational(1, 2), 63])

TOPIC = Topic(
    number="6.2", title="Approximating Areas with Riemann Sums",
    unit="Unit 6: Integration and Accumulation of Change", ced=["LIM-5.A", "LIM-5.A.1", "LIM-5.A.2", "LIM-5.A.3", "LIM-5.A.4"],
    goals=r"Approximate the area under a curve with left, right, midpoint and trapezoidal sums from graphs, tables and formulas, and decide whether each is an over- or underestimate.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
