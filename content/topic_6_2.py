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


def _l(v):
    """A sample point or value as LaTeX: decimals stay decimals (0.5, 1.25), fractions stay fractions."""
    v = sp.nsimplify(v)
    if v.is_Rational and not v.is_Integer:
        q = int(v.q)
        for p in (2, 5):
            while q % p == 0:
                q //= p
        if q == 1:
            return str(float(v)).rstrip("0").rstrip(".")
    return sp.latex(v)


def sum_work(f, edges, kind, name="f", letter=None, dec=False, unit=""):
    """The written work for a Riemann or trapezoidal sum, the way Adder wants it on every solution: first the sum with the
    function evaluated at its sample points (Delta x [f(1) + f(2) + ...], or width times f(...) for each piece when the widths
    differ), then the same with the values put in, then the total. f: a sympy expression in x, or a dict of table values.
    Returns LaTeX (a display, ending in a period). dec: show values as decimals where they terminate. unit: words after the total."""
    val = (lambda s: f[s]) if isinstance(f, dict) else (lambda s: f.subs(x, s))
    shown = (lambda v: _l(v)) if dec else (lambda v: sp.latex(sp.nsimplify(v)))
    letter = letter or {"left": "L", "right": "R", "mid": "M", "trap": "T"}[kind]
    rel = "="
    if letter.endswith(r"\approx"):                      # an integral being approximated: "integral of R dt ~ ..."
        letter, rel = letter[:-len(r"\approx")].rstrip(), r"\approx"
    pieces = list(zip(edges, edges[1:]))
    widths = [b - a for a, b in pieces]
    equal = len(set(widths)) == 1
    total = rsum(f, edges, kind)
    if kind == "trap":
        if equal:
            w = widths[0]
            coef = [1] + [2] * (len(edges) - 2) + [1]
            ev = " + ".join(("" if c == 1 else "2") + rf"{name}({_l(s)})" for c, s in zip(coef, edges))
            nv = " + ".join(("" if c == 1 else "2") + (rf"({shown(val(s))})" if c != 1 else shown(val(s))) for c, s in zip(coef, edges))
            lead = rf"\frac{{{_l(w)}}}{{2}}"
            lines = [rf"{letter} &{rel} {lead}\left[{ev}\right]", rf"&= {lead}\left[{nv}\right]", rf"&= {shown(total)}"]
        else:
            ev = " + ".join(rf"{_l(b - a)} \cdot \frac{{{name}({_l(a)}) + {name}({_l(b)})}}{{2}}" for a, b in pieces)
            nv = " + ".join(rf"{_l(b - a)} \cdot \frac{{{shown(val(a))} + {shown(val(b))}}}{{2}}" for a, b in pieces)
            each = " + ".join(shown((b - a) * (val(a) + val(b)) / sp.Integer(2)) for a, b in pieces)
            lines = [rf"{letter} &{rel} {ev}", rf"&= {nv}", rf"&= {each}", rf"&= {shown(total)}"]
    else:
        pick = {"left": lambda a, b: a, "right": lambda a, b: b, "mid": lambda a, b: (a + b) / sp.Integer(2)}[kind]
        ss = [pick(a, b) for a, b in pieces]
        if equal:
            w = widths[0]
            ev = " + ".join(rf"{name}({_l(s)})" for s in ss)
            nv = " + ".join(shown(val(s)) for s in ss)
            inner = sum(val(s) for s in ss)
            lines = [rf"{letter} &{rel} {_l(w)}\left[{ev}\right]", rf"&= {_l(w)}\left[{nv}\right]", rf"&= {_l(w)}\left({shown(inner)}\right) = {shown(total)}"]
        else:
            ev = " + ".join(rf"{_l(w)} \cdot {name}({_l(s)})" for w, s in zip(widths, ss))
            nv = " + ".join(rf"{_l(w)}({shown(val(s))})" for w, s in zip(widths, ss))
            each = " + ".join(shown(w * val(s)) for w, s in zip(widths, ss))
            lines = [rf"{letter} &{rel} {ev}", rf"&= {nv}", rf"&= {each}", rf"&= {shown(total)}"]
    lines[-1] += (rf"\ \text{{{unit}}}" if unit else "") + "."
    return r"\[ \begin{aligned} " + r" \\ ".join(lines) + r" \end{aligned} \]"


F = x**2 / 10 + 1
E8 = [0, 2, 4, 6, 8]
same("lesson sums", [rsum(F, E8, k) for k in ("left", "right", "mid", "trap")], [sp.Rational(96, 5), 32, sp.Rational(124, 5), sp.Rational(128, 5)])
same("lesson area", [sp.integrate(F, (x, 0, 8))], [sp.Rational(376, 15)])
TAB = {0: 4, 2: 6, 5: 7, 9: 5, 10: 3}
same("uneven", [rsum(TAB, [0, 2, 5, 9, 10], "left")], [59])
same("ex1", [rsum(1 / x, [1, sp.Rational(3, 2), 2, sp.Rational(5, 2), 3], "right")], [sp.Rational(19, 20)])
same("ex2", [rsum({0: 2, 1: 5, 3: 7, 4: 4}, [0, 1, 3, 4], "trap")], [21])


def sums_fig(name, kind, caption):
    """f(x) = 0.1x^2 + 1 on [0, 8] with the four rectangles of a left, right or midpoint sum, and a dot on the curve at
    each rectangle's height point."""
    f = lambda s: s * s / 10 + 1
    fill, dots = [], []
    for a in (0, 2, 4, 6):
        s = {"left": a, "right": a + 2, "mid": a + 1}[kind]
        fill.append(rf"\fill[ink!14] (axis cs:{a},0) rectangle (axis cs:{a + 2},{f(s)}); \draw (axis cs:{a},0) rectangle (axis cs:{a + 2},{f(s)});")
        dots.append((s, f(s)))
    return graph(name, [("0.1*x^2+1", 0, 8.4)], xr=(0, 9), yr=(0, 8), ystep=2, xstep=2, closed=dots, under="".join(fill), caption=caption)


FIG_L = sums_fig("t6_2_left", "left", r"Left Riemann sum: each height is $f$ where its piece starts.")
FIG_R = sums_fig("t6_2_right", "right", r"Right Riemann sum: each height is $f$ where its piece ends.")
FIG_M = sums_fig("t6_2_mid", "mid", r"Midpoint Riemann sum: each height is $f$ at the middle of its piece.")
FIG_G = graph("t6_2_g", [("4-0.25*x^2", 0, 4)], xr=(0, 4), yr=(0, 5), ylabel="g(x)", caption="The graph of $g(x) = 4 - \\frac14x^2$.")

NOTES = [
    Video("s6_2.py::Lesson", "Riemann sums", 10.5),

    Section("Left, right and midpoint Riemann sums"),
    Text(r"To approximate the area under a curve, split the interval into pieces, put a rectangle on each piece, and add up the rectangles' areas. "
         r"The width of a piece is $\Delta x$; with $n$ equal pieces of $[a, b]$, $\Delta x = \frac{b - a}{n}$."),
    Text(r"\textbf{Left Riemann sum.} Take $f(x) = 0.1x^2 + 1$ on $[0, 8]$ with four pieces, so $\Delta x = 2$. Build a rectangle on the first piece, "
         r"from $0$ to $2$. Its height is the function value where the piece \blank{starts}: $f(0) = 1$. Its area is width times height, "
         r"$2 \cdot f(0) = 2 \cdot 1 = 2$."),
    FIG_L,
    Text(r"The other three: $2 \cdot f(2) = 2 \cdot 1.4 = 2.8$, then $2 \cdot f(4) = 2 \cdot 2.6 = 5.2$, then $2 \cdot f(6) = 2 \cdot 4.6 = 9.2$. "
         r"Add the four areas: $L = 2 + 2.8 + 5.2 + 9.2 = 19.2$."),
    Text(r"\textbf{Factoring out the width.} Every rectangle has the same width, so it factors out: "
         r"\[ \begin{aligned} L &= 2\left[f(0) + f(2) + f(4) + f(6)\right] \\ &= 2\left[1 + 1.4 + 2.6 + 4.6\right] \\ &= 2(9.6) = 19.2. \end{aligned} \] "
         r"That's the usual way to write it. But you can always get it by thinking about the rectangles one at a time: each one is its width times its height."),
    Text(r"\textbf{Right Riemann sum.} We could draw the rectangles differently: make each height the function value at the \blank{right} side of its piece. "
         r"\[ \begin{aligned} R &= 2\left[f(2) + f(4) + f(6) + f(8)\right] \\ &= 2\left[1.4 + 2.6 + 4.6 + 7.4\right] \\ &= 2(16) = 32. \end{aligned} \]"),
    FIG_R,
    Text(r"\textbf{Midpoint Riemann sum.} Or use the \blank{middle} of each piece: $1$, $3$, $5$ and $7$. Go straight up from each middle to the curve for the height. "
         r"\[ \begin{aligned} M &= 2\left[f(1) + f(3) + f(5) + f(7)\right] \\ &= 2\left[1.1 + 1.9 + 3.5 + 5.9\right] \\ &= 2(12.4) = 24.8. \end{aligned} \]"),
    FIG_M,
    Formula("Riemann sums", (
        r"With $n$ equal pieces, $\Delta x = \frac{b - a}{n}$, and each sum is \[ \Delta x\left[\,\text{the } n \text{ heights added up}\,\right]. \] "
        r"\textbf{Left Riemann sum}: each height is $f$ at the left end of its piece. \par "
        r"\textbf{Right Riemann sum}: each height is $f$ at the right end. \par "
        r"\textbf{Midpoint Riemann sum}: each height is $f$ at the middle of its piece. \par "
        r"Always write the heights as values of the function first, $\Delta x\left[f(x_1) + f(x_2) + \cdots\right]$, then put in the numbers.")),

    Section("Trapezoidal sums"),
    Text(r"A \textbf{trapezoidal sum} replaces the flat tops with slanted ones that connect the points on the curve. Each trapezoid's area is its width times "
         r"the average of its two sides. Every inside height is used twice, once by each trapezoid next to it: "
         r"\[ \begin{aligned} T &= \frac{2}{2}\left[f(0) + 2f(2) + 2f(4) + 2f(6) + f(8)\right] \\ &= 1\left[1 + 2.8 + 5.2 + 9.2 + 7.4\right] = 25.6. \end{aligned} \] "
         r"With equal widths, $T = \frac{L + R}{2} = \frac{19.2 + 32}{2} = 25.6$. The true area is $\frac{376}{15} \approx 25.07$: the midpoint and "
         r"trapezoidal sums are much closer than the left and right sums."),
    Text(r"\textbf{Uneven widths.} With a table, the pieces often have different widths, so the width can't be factored out. Give each rectangle its own width "
         r"and add up (width)(height), with each height written as a function value first."),
    VideoExample('Uneven widths', work="2.6cm"),

    Section("Over or under?"),
    Text(r"\textbf{$f$ is increasing, and we use a left Riemann sum. What can we expect?} An \blank{underestimate}. Each height comes from the left end, "
         r"the lowest point of its piece, so every rectangle sits below the graph and misses a little area."),
    Text(r"\textbf{$f$ is increasing, and we use a right Riemann sum?} An overestimate. Each height comes from the right end, the highest point of its piece, "
         r"so the rectangles poke up above the graph."),
    Text(r"\textbf{$f$ is decreasing?} It's the reverse. Going downhill, the left end is the high point, so a left sum \blank{overestimates}, and a right "
         r"sum underestimates."),
    Formula("Over- and underestimates", (
        r"$f$ increasing: left sum \blank{under}estimates, right sum overestimates. \par "
        r"$f$ decreasing: left sum overestimates, right sum underestimates. \par "
        r"$f$ concave up (a bowl): trapezoidal sum \blank{over}estimates. \par "
        r"$f$ concave down (a hill): trapezoidal sum underestimates.")),
    BigIdea(r"A Riemann sum adds widths times heights. Left, right and midpoint say where each height comes from; trapezoids average the two sides. "
            r"Increasing or decreasing decides whether left and right sums are over or under; concavity decides trapezoids."),
    Check(r"Find the left Riemann sum for $f(x) = x^2$ on $[0, 2]$ with $2$ equal pieces.", num(1),
          r"$\Delta x = 1$: $L = 1\left[f(0) + f(1)\right] = 1\left[0 + 1\right] = 1$."),
]

# ---------------------------------------------------------------- practice
P = [(x**2, 0, 4, 4, "right"), (x**2, 0, 4, 4, "left"), (x**3, 0, 2, 4, "mid"), (sp.sqrt(x), 0, 4, 4, "trap"), (1 / x, 1, 2, 2, "trap"), (4 - x**2 / 4, 0, 4, 4, "left")]
NAME = {"left": "left Riemann sum", "right": "right Riemann sum", "mid": "midpoint Riemann sum", "trap": "trapezoidal sum"}
PRACTICE = []
for f, a, b, n, k in P:
    edges = [a + sp.Rational(b - a, n) * i for i in range(n + 1)]
    v = rsum(f, edges, k)
    PRACTICE.append(Item(rf"Use a {NAME[k]} with ${n}$ equal subintervals to approximate the area under $f(x) = {sp.latex(f)}$ on $[{a}, {b}]$.", num(v),
                         rf"$\Delta x = {sp.latex(sp.Rational(b - a, n))}$. " + sum_work(f, edges, k), work="2.4cm"))
PRACTICE += [
    Item(r"The table gives $r(t)$: $t = 0, 3, 4, 8$ hours; $r(t) = 10, 14, 12, 6$ gallons per hour. Use a right Riemann sum with the subintervals in the table to approximate "
         r"the total gallons from $t = 0$ to $t = 8$.", num(78),
         r"Widths $3, 1, 4$, each height from the right end: " + sum_work({0: 10, 3: 14, 4: 12, 8: 6}, [0, 3, 4, 8], "right", "r", unit="gallons"), work="1.8cm"),
    Item(r"Using the same table, find the trapezoidal approximation of the total gallons from $t = 0$ to $t = 8$.", num(85),
         sum_work({0: 10, 3: 14, 4: 12, 8: 6}, [0, 3, 4, 8], "trap", "r", unit="gallons"), work="1.8cm"),
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
                rf"$\Delta x = {sp.latex(sp.Rational(b - a, n))}$. " + sum_work(f, edges, k), work="2cm")


QUIZ = [
    Variants(q(x**2 + 1, 0, 3, 3, "left"), q(x**2 + 1, 0, 3, 3, "right"), q(2 * x + 1, 0, 4, 4, "left")),
    Variants(q(x**2, 0, 4, 2, "mid"), q(x**2, 1, 5, 2, "mid"), q(x**3, 0, 4, 2, "mid")),
    Variants(q(x**2, 0, 4, 4, "trap"), q(x**2, 0, 2, 2, "trap"), q(x**3, 0, 2, 2, "trap")),
    Variants(*[Item(rf"Table: $x = {', '.join(map(str, xs))}$; $f(x) = {', '.join(map(str, ys))}$. Find the {NAME[k]} with the subintervals in the table.",
                    num(rsum(dict(zip(xs, ys)), xs, k)), rf"Widths ${', '.join(str(b - a) for a, b in zip(xs, xs[1:]))}$: " + sum_work(dict(zip(xs, ys)), xs, k),
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
        r"$\Delta x = 2$: " + sum_work(x**2, [0, 2, 4], "trap"), why_not={"A": "the left sum", "D": "the right sum"}),
    MCQ(r"Table: $t = 0, 1, 3, 6$; $v(t) = 2, 3, 5, 4$. The right Riemann sum with the subintervals in the table is", [r"$14$", r"$25$", r"$12$", r"$32$"], "B",
        r"Widths $1, 2, 3$: " + sum_work({0: 2, 1: 3, 3: 5, 6: 4}, [0, 1, 3, 6], "right", "v"), why_not={"C": "the heights added without widths"}),
    MCQ(r"$f$ is positive, decreasing and concave up on $[a, b]$. Which approximation of the area under $f$ is an underestimate?", [r"the left sum",
        r"the trapezoidal sum", r"both the left and right sums", r"the right sum"], "D", r"Decreasing: the right sum is too small. Concave up: the trapezoidal sum is too big."),
    MCQ(r"The midpoint sum with $2$ equal subintervals for the area under $f(x) = x^3$ on $[0, 2]$ is", [r"$1$", r"$\frac72$", r"$4$", r"$5$"], "B",
        r"$\Delta x = 1$, midpoints $0.5$ and $1.5$: " + sum_work(x**3, [0, 1, 2], "mid", dec=True), why_not={"C": "the exact area", "D": "the trapezoidal sum"}),
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
             sum_work({0: 4, 2: 6, 5: 7, 9: 9, 10: 12}, [0, 2, 5, 9, 10], "left", "R", unit="gallons"), [(1, "left Riemann sum setup"), (1, "answer")], work="2.4cm"),
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
