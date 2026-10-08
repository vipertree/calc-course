"""Topic 8.5: Finding the area between curves expressed as functions of y.

CED: CHA-5.A (CHA-5.A.3, CHA-5.A.4): with x = f(y) on the right and x = g(y) on the left for c <= y <= d, the area is
the integral of f(y) - g(y) dy. Choose dy when the left and right boundaries don't change (or the curves are given as x
in terms of y). Lesson example: x = y^2 - 4 and x = 2y - 1, area 32/3. Choosing dy: sqrt x, x - 2, y = 0 done both ways
(10/3). Worked examples: x = 4 - y^2 and the y-axis; y = ln x as x = e^y; x = y^2 and x = 2 - y^2.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)
from calclib.figs import region

x, y = sp.symbols("x y", real=True)


def area_y(right, left, c, d):
    return sp.simplify(sp.integrate(right - left, (y, c, d)))


same("lesson", [sorted(sp.solve(sp.Eq(y**2 - 4, 2 * y - 1), y)), area_y(2 * y - 1, y**2 - 4, -1, 3)], [[-1, 3], sp.Rational(32, 3)])
same("both ways", [sp.integrate(sp.sqrt(x), (x, 0, 4)) - sp.integrate(x - 2, (x, 2, 4)), area_y(y + 2, y**2, 0, 2)], [sp.Rational(10, 3), sp.Rational(10, 3)])
same("ex", [area_y(4 - y**2, 0, -2, 2), area_y(sp.exp(y), 0, 0, 1), area_y(2 - y**2, y**2, -1, 1)], [sp.Rational(32, 3), sp.E - 1, sp.Rational(8, 3)])

FIG = region("t8_5_both", [("sqrt(x)", 0, 4.4), ("x-2", 2, 4.4)], (-0.3, 4.6), (-0.3, 2.4), [(lambda v: v + 2, lambda v: v * v, 0, 2)], var="y",
             caption=r"The region bounded by $y = \sqrt x$, $y = x - 2$ and $y = 0$. Horizontal slices run from $x = y^2$ to $x = y + 2$.")

NOTES = [
    Video("s8_5.py::Lesson", "Area with respect to y", 5),

    Section("Right minus left"),
    Text(r"Slice horizontally. The slice at height $y$ runs from the left curve to the right curve: length $f(y) - g(y)$, thickness $dy$."),
    Formula("Area with respect to $y$", (r"If $f(y) \ge g(y)$ for $c \le y \le d$, the area between $x = f(y)$ and $x = g(y)$ is \[ A = \int_c^d \blank{\big(f(y) - g(y)\big)}\,dy = \int_c^d (\text{right} - \text{left})\,dy. \] "
                                          r"The limits are $y$ values, and each curve must be written as $x = $ (something in $y$).")),
    Section("Choosing $dy$"),
    Text(r"The region below needs two integrals in $x$ (the bottom switches at $x = 2$): $\int_0^4 \sqrt x\,dx - \int_2^4 (x - 2)\,dx = \frac{10}{3}$. In $y$ it needs one: $\int_0^2 (y + 2 - y^2)\,dy = \frac{10}{3}$."),
    FIG,
    Text(r"Use $dy$ when the left and right boundaries stay the same all the way up, or when the curves are already given as $x$ in terms of $y$."),
    VideoExample('A parabola and a line, sideways', work="4.6cm"),
    BigIdea(r"Horizontal slices: area $= \int_c^d (\text{right} - \text{left})\,dy$ with $y$ limits."),
    Check(r"Find the area between $x = y^2$ and $x = 4$.", selfcheck(r"\tfrac{32}{3}"), r"$\int_{-2}^2 (4 - y^2)\,dy$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Find the area between $x = y^2$ and $x = y + 6$.", num(area_y(y + 6, y**2, -2, 3)), r"Meet at $y = -2, 3$: $\int_{-2}^3 (y + 6 - y^2)\,dy = \frac{125}{6}$.", work="2cm"),
    Item(r"Find the area between $x = 9 - y^2$ and the $y$-axis.", num(area_y(9 - y**2, 0, -3, 3)), r"$\int_{-3}^3 (9 - y^2)\,dy = 36$.", work="1.6cm"),
    Item(r"Find the area between $x = y^3$ and $x = 4y$ for $0 \le y \le 2$.", num(area_y(4 * y, y**3, 0, 2)), r"$4y \ge y^3$ on $[0, 2]$: $8 - 4 = 4$.", work="1.6cm"),
    Item(r"Find the area bounded by $y = \sqrt x$, $y = 0$ and $x = 4$ by integrating with respect to $y$.", num(area_y(4, y**2, 0, 2)), r"$\int_0^2 (4 - y^2)\,dy = \frac{16}{3}$.", work="1.8cm"),
    Item(r"Find the area bounded by $y = x^3$, $y = 8$ and the $y$-axis.", num(area_y(y**sp.Rational(1, 3), 0, 0, 8)), r"$x = y^{1/3}$: $\int_0^8 y^{1/3}\,dy = \frac34 \cdot 16 = 12$.", work="1.8cm"),
    Item(r"Find the area between $x = 2y^2$ and $x = 4 + y^2$.", num(area_y(4 + y**2, 2 * y**2, -2, 2)), r"Meet at $y = \pm2$: $\int_{-2}^2 (4 - y^2)\,dy = \frac{32}{3}$.", work="1.8cm"),
    Item(r"Find the area bounded by $y = \ln x$, $y = 0$, $y = 2$ and the $y$-axis.", num(area_y(sp.exp(y), 0, 0, 2), tol=1e-3), r"$\int_0^2 e^y\,dy = e^2 - 1 \approx 6.389$.", work="1.6cm"),
    Item(r"The region bounded by $y = x$, $y = 2 - x$ and $y = 0$ is a triangle. Find its area with an integral in $y$.", num(area_y(2 - y, y, 0, 1)), r"$x = y$ to $x = 2 - y$ for $0 \le y \le 1$: $\int_0^1 (2 - 2y)\,dy = 1$.", work="1.8cm"),
    Item(r"Find the area between $x = y^2 - 1$ and $x = 1 - y^2$.", num(area_y(1 - y**2, y**2 - 1, -1, 1)), r"$\int_{-1}^1 (2 - 2y^2)\,dy = \frac83$.", work="1.6cm"),
    Item(r"Find the area between $x = \sin y$ and the $y$-axis for $0 \le y \le \pi$.", num(2), r"$\int_0^\pi \sin y\,dy = 2$.", work="1.2cm"),
]

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find the area between $x = y^2$ and $x = 1$.", num(area_y(1, y**2, -1, 1)), r"$\int_{-1}^1 (1 - y^2)\,dy = \frac43$.", work="1.4cm"),
        Item(r"Find the area between $x = y^2$ and $x = 9$.", num(area_y(9, y**2, -3, 3)), r"$36$.", work="1.4cm"),
        Item(r"Find the area between $x = 4 - y^2$ and $x = 0$.", num(area_y(4 - y**2, 0, -2, 2)), r"$\frac{32}{3}$.", work="1.4cm"),
    ),
    Variants(
        Item(r"Find the area between $x = y^2$ and $x = y + 2$.", num(area_y(y + 2, y**2, -1, 2)), r"$\frac92$.", work="1.8cm"),
        Item(r"Find the area between $x = y^2$ and $x = 2y$.", num(area_y(2 * y, y**2, 0, 2)), r"$\frac43$.", work="1.8cm"),
        Item(r"Find the area between $x = y^2 - 2y$ and $x = 0$.", num(area_y(0, y**2 - 2 * y, 0, 2)), r"$\int_0^2 (2y - y^2)\,dy = \frac43$.", work="1.8cm"),
    ),
    Variants(
        MCQ(r"Which integral gives the area between $x = y^2$ and $x = y + 2$?", [r"$\int_{-1}^{2} (y^2 - y - 2)\,dy$", r"$\int_{0}^{4} (y + 2 - y^2)\,dy$", r"$\int_{-1}^{2} (y + 2 - y^2)\,dy$", r"$\int_{1}^{4} (y + 2 - y^2)\,dy$"], "C",
            r"Meet at $y = -1, 2$; the line is on the right."),
        MCQ(r"Which integral gives the area bounded by $y = \sqrt x$, $y = 0$ and $x = 9$, in terms of $y$?", [r"$\int_0^3 (9 - y^2)\,dy$", r"$\int_0^9 (9 - y^2)\,dy$", r"$\int_0^3 (y^2 - 9)\,dy$", r"$\int_0^3 y^2\,dy$"], "A",
            r"From $x = y^2$ to $x = 9$, $0 \le y \le 3$."),
    ),
    Variants(
        MCQ(r"For which region is integrating with respect to $y$ easier?", [r"Between $y = x^2$ and $y = 4$", r"Between $y = \sqrt x$, $y = x - 2$ and $y = 0$", r"Between $y = \sin x$ and $y = 0$ on $[0, \pi]$", r"Between $y = x$ and $y = x^2$"], "B",
            r"In $x$ the bottom switches at $x = 2$; in $y$ it's one integral."),
    ),
    Variants(
        Item(r"Find the area bounded by $y = e^x$, $y = e$ and the $y$-axis using an integral in $y$.", num(1), r"$x = \ln y$: $\int_1^e \ln y\,dy = 1$ (or $\int_0^1 (e - e^x)\,dx = 1$).", work="1.8cm"),
        Item(r"Find the area bounded by $y = x^2$ ($x \ge 0$), $y = 4$ and the $y$-axis using an integral in $y$.", num(area_y(sp.sqrt(y), 0, 0, 4)), r"$\int_0^4 \sqrt y\,dy = \frac{16}{3}$.", work="1.8cm"),
    ),
]

# ---------------------------------------------------------------- test prep
_r = [float(sp.nsolve(sp.exp(y / 2) - (4 - y**2), y, g)) for g in (-1.9, 1.3)]
_m4 = float(sp.Integral(4 - y**2 - sp.exp(y / 2), (y, _r[0], _r[1])).evalf())
MCQS = [
    MCQ(r"The area between $x = y^2 - 1$ and the $y$-axis is", [r"$\frac23$", r"$\frac43$", r"$2$", r"$\frac83$"], "B", r"$\int_{-1}^1 (1 - y^2)\,dy = \frac43$."),
    MCQ(r"The area of the region bounded by $y = \sqrt x$, $y = 6 - x$ and $y = 0$ is", [r"$\frac{22}{3}$", r"$\frac{16}{3}$", r"$8$", r"$\frac{32}{3}$"], "A",
        r"In $y$: $\int_0^2 \big((6 - y) - y^2\big)\,dy = 12 - 2 - \frac83 = \frac{22}{3}$."),
    MCQ(r"Which gives the area between $x = 3 - y^2$ and $x = -1$?", [r"$\int_{-2}^{2} (2 - y^2)\,dy$", r"$\int_{-1}^{3} (4 - y^2)\,dy$", r"$\int_{0}^{2} (4 - y^2)\,dy$", r"$\int_{-2}^{2} (4 - y^2)\,dy$"], "D",
        r"Right minus left: $(3 - y^2) - (-1)$; meet at $y = \pm2$."),
    MCQ(r"The curves $x = 4 - y^2$ and $x = e^{y/2}$ bound a region. To three decimal places, its area is", [r"$5.902$", rf"${_m4:.3f}$", r"$7.125$", r"$4.218$"], "B",
        rf"They meet at $y \approx {_r[0]:.4f}$ and $y \approx {_r[1]:.4f}$; $\int (4 - y^2 - e^{{y/2}})\,dy \approx {_m4:.3f}$.", calc=True),
]
same("m", [area_y(1 - y**2, 0, -1, 1), area_y(6 - y, y**2, 0, 2), area_y(4 - y**2, 0, -2, 2)], [sp.Rational(4, 3), sp.Rational(22, 3), sp.Rational(32, 3)])
close("m4", _m4, 6.745, 5e-3)

FRQS = []

TOPIC = Topic(
    number="8.5", title="Finding the Area Between Curves Expressed as Functions of y",
    unit="Unit 8: Applications of Integration", ced=["CHA-5.A", "CHA-5.A.3", "CHA-5.A.4"],
    goals=r"Find the area between curves by integrating right minus left with respect to $y$, and choose when $dy$ is easier.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
