"""Topic 8.4: Finding the area between curves expressed as functions of x.

CED: CHA-5.A (CHA-5.A.1, CHA-5.A.2): the area between y = f(x) and y = g(x) on [a, b] with f >= g is the integral of
f(x) - g(x); limits are where the curves meet when the region is bounded only by them; works below the x-axis.
Lesson example: y = x and y = x^2 - 2, area 9/2. Worked examples: sqrt x and x/2 (4/3); cos x and sin x on [0, pi/4]
(sqrt 2 - 1); e^x, y = 1, x = 2 (e^2 - 3).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)
from calclib.figs import region

x = sp.symbols("x", real=True)


def area(top, bot, a, b):
    return sp.simplify(sp.integrate(top - bot, (x, a, b)))


def meet(f, g):
    return sorted(sp.solve(sp.Eq(f, g), x))


same("lesson", [meet(x, x**2 - 2), area(x, x**2 - 2, -1, 2)], [[-1, 2], sp.Rational(9, 2)])
same("ex", [area(sp.sqrt(x), x / 2, 0, 4), area(sp.cos(x), sp.sin(x), 0, sp.pi / 4), area(sp.exp(x), 1, 0, 2)], [sp.Rational(4, 3), sp.sqrt(2) - 1, sp.E**2 - 3])

FIG = region("t8_4_region", [("x", -1.8, 2.8), ("x^2-2", -1.8, 2.25)], (-2, 3), (-2.5, 3), [(lambda v: v, lambda v: v * v - 2, -1, 2)],
             labels=[(2.5, 2.5, "left", r"$y = x$"), (2.1, 2.4, "right", r"$y = x^2 - 2$")], caption=r"The region between $y = x$ (top) and $y = x^2 - 2$ (bottom), partly below the $x$-axis.")
FIG_Q = region("t8_4_q", [("4-x^2", -2.3, 2.3), ("x+2", -2.5, 1.5)], (-2.5, 2.5), (-1, 4.5), [(lambda v: 4 - v * v, lambda v: v + 2, -2, 1)],
               caption=r"The region between $y = 4 - x^2$ and $y = x + 2$.")

NOTES = [
    Video("s8_4.py::Lesson", "Area between curves", 6),

    Section("Top minus bottom"),
    Text(r"Slice the region into thin vertical rectangles. The rectangle at $x$ runs from the bottom curve to the top curve: height $f(x) - g(x)$, width $dx$."),
    Formula("Area between curves", (r"If $f(x) \ge g(x)$ on $[a, b]$, the area between them is \[ A = \int_a^b \blank{\big(f(x) - g(x)\big)}\,dx = \int_a^b (\text{top} - \text{bottom})\,dx. \]")),
    Text(r"This works below the $x$-axis too: top $= 1$ and bottom $= -2$ give height $1 - (-2) = 3$. Sliding both curves up doesn't change top minus bottom."),
    Section("Limits and which curve is on top"),
    Text(r"If only the two curves bound the region, the limits are where they meet: set $f(x) = g(x)$ and solve. Then test a point between the limits to see which curve is on top."),
    FIG,
    VideoExample('Area between a line and a parabola', work="4.6cm"),
    BigIdea(r"Area between curves $= \int (\text{top} - \text{bottom})\,dx$; limits where the curves meet; a test point tells you which is on top."),
    Check(r"Find the area between $y = x^2$ and $y = x$.", selfcheck(r"\tfrac16"), r"Meet at $0$ and $1$; $x$ on top: $\frac12 - \frac13$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Find the area between $y = x^2$ and $y = 2x$.", num(area(2 * x, x**2, 0, 2)), r"Meet at $0$, $2$; $2x$ on top: $4 - \frac83 = \frac43$.", work="2cm"),
    Item(r"Find the area of the region shown, between $y = 4 - x^2$ and $y = x + 2$.", num(area(4 - x**2, x + 2, -2, 1)),
         r"$4 - x^2 = x + 2$ gives $x = -2, 1$. $\int_{-2}^1 (2 - x - x^2)\,dx = \frac92$.", work="2.4cm", figure=FIG_Q),
    Item(r"Find the area between $y = x^3$ and $y = x$ for $0 \le x \le 1$.", num(area(x, x**3, 0, 1)), r"$x \ge x^3$ on $[0, 1]$: $\frac12 - \frac14 = \frac14$.", work="1.6cm"),
    Item(r"Find the area between $y = x^2 - 4$ and the $x$-axis.", num(area(0, x**2 - 4, -2, 2)), r"The axis is on top: $\int_{-2}^2 (4 - x^2)\,dx = \frac{32}{3}$.", work="1.8cm"),
    Item(r"Find the area between $y = e^x$ and $y = e^{-x}$ for $0 \le x \le 1$.", num(area(sp.exp(x), sp.exp(-x), 0, 1), tol=1e-3), r"$\left[e^x + e^{-x}\right]_0^1 = e + \frac1e - 2 \approx 1.086$.", work="1.8cm"),
    Item(r"Find the area between $y = \sqrt x$ and $y = x^2$.", num(area(sp.sqrt(x), x**2, 0, 1)), r"Meet at $0$, $1$: $\frac23 - \frac13 = \frac13$.", work="1.8cm"),
    Item(r"Find the area between $y = \frac1x$, $y = 0$, $x = 1$ and $x = e^2$.", num(2), r"$\left[\ln x\right]_1^{e^2} = 2$.", work="1.4cm"),
    Item(r"Find the area between $y = 6 - x^2$ and $y = x^2 - 2$.", num(area(6 - x**2, x**2 - 2, -2, 2)), r"Meet at $\pm2$: $\int_{-2}^2 (8 - 2x^2)\,dx = \frac{64}{3}$.", work="2cm"),
    Item(r"Find the area between $y = \sin x$ and $y = 0$ for $0 \le x \le \pi$.", num(2), r"$\left[-\cos x\right]_0^\pi = 2$.", work="1.2cm"),
    Item(r"Find the area between $y = 2\cos x$ and $y = 1$ for $-\frac\pi3 \le x \le \frac\pi3$.", num(area(2 * sp.cos(x), 1, -sp.pi / 3, sp.pi / 3), tol=1e-3),
         r"$\left[2\sin x - x\right]_{-\pi/3}^{\pi/3} = 2\sqrt3 - \frac{2\pi}{3} \approx 1.370$.", work="2cm"),
]

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find the area between $y = x$ and $y = x^2$ on $[0, 1]$.", num(area(x, x**2, 0, 1)), r"$\frac12 - \frac13$.", work="1.4cm"),
        Item(r"Find the area between $y = 3x$ and $y = x^2$.", num(area(3 * x, x**2, 0, 3)), r"Meet at $0$, $3$: $\frac{27}{2} - 9 = \frac92$.", work="1.6cm"),
        Item(r"Find the area between $y = 4x$ and $y = x^3$ for $0 \le x \le 2$.", num(area(4 * x, x**3, 0, 2)), r"$8 - 4 = 4$.", work="1.6cm"),
    ),
    Variants(
        Item(r"Find the area between $y = 9 - x^2$ and $y = 0$.", num(area(9 - x**2, 0, -3, 3)), r"$\int_{-3}^3 (9 - x^2)\,dx = 36$.", work="1.6cm"),
        Item(r"Find the area between $y = x^2 - 1$ and $y = 0$.", num(area(0, x**2 - 1, -1, 1)), r"$\int_{-1}^1 (1 - x^2)\,dx = \frac43$.", work="1.6cm"),
        Item(r"Find the area between $y = 2 - 2x^2$ and $y = 0$.", num(area(2 - 2 * x**2, 0, -1, 1)), r"$\frac83$.", work="1.6cm"),
    ),
    Variants(
        MCQ(r"Which integral gives the area between $y = x + 2$ and $y = x^2$?", [r"$\int_{-1}^{2} (x^2 - x - 2)\,dx$", r"$\int_{-1}^{2} (x + 2 - x^2)\,dx$", r"$\int_{0}^{2} (x + 2 - x^2)\,dx$", r"$\int_{-2}^{1} (x + 2 - x^2)\,dx$"], "B",
            r"Meet at $-1$, $2$; the line is on top."),
        MCQ(r"Which integral gives the area between $y = 1 - x^2$ and $y = x^2 - 1$?", [r"$\int_{-1}^{1} 0\,dx$", r"$\int_{0}^{1} (2 - 2x^2)\,dx$", r"$\int_{-1}^{1} (2x^2 - 2)\,dx$", r"$\int_{-1}^{1} (2 - 2x^2)\,dx$"], "D",
            r"Meet at $\pm1$; $1 - x^2$ on top."),
    ),
    Variants(
        Item(r"Find the area between $y = \cos x$ and $y = 0$ for $0 \le x \le \frac\pi2$.", num(1), r"$\sin\frac\pi2 - \sin 0$.", work="1.2cm"),
        Item(r"Find the area between $y = e^x$ and $y = 0$ for $0 \le x \le \ln 5$.", num(4), r"$5 - 1$.", work="1.2cm"),
        Item(r"Find the area between $y = \frac1x$ and $y = 0$ for $1 \le x \le e$.", num(1), r"$\ln e - \ln 1$.", work="1.2cm"),
    ),
    Variants(
        Item(r"Find the area between $y = x^2 - 2x$ and $y = x$.", num(area(x, x**2 - 2 * x, 0, 3)), r"Meet at $0$, $3$: $\int_0^3 (3x - x^2)\,dx = \frac92$.", work="1.8cm"),
        Item(r"Find the area between $y = x^2 + 1$ and $y = 2x + 1$.", num(area(2 * x + 1, x**2 + 1, 0, 2)), r"Meet at $0$, $2$: $\frac43$.", work="1.8cm"),
        Item(r"Find the area between $y = 8 - x^2$ and $y = x^2$.", num(area(8 - x**2, x**2, -2, 2)), r"Meet at $\pm2$: $\frac{64}{3}$.", work="1.8cm"),
    ),
]

# ---------------------------------------------------------------- test prep
_c = [float(sp.nsolve(sp.cos(x) - x**2, x, g)) for g in (-0.8, 0.8)]
_m4 = float(sp.Integral(sp.cos(x) - x**2, (x, _c[0], _c[1])).evalf())
close("m4", _m4, 1.095, 5e-3)
MCQS = [
    MCQ(r"The area between $y = x^2$ and $y = 4$ is", [r"$\frac{16}{3}$", r"$8$", r"$\frac{32}{3}$", r"$16$"], "C", r"$\int_{-2}^2 (4 - x^2)\,dx = \frac{32}{3}$.", why_not={"A": "only half the region"}),
    MCQ(r"The area between $y = \sqrt x$, $y = 0$ and $x = 9$ is", [r"$18$", r"$27$", r"$6$", r"$9$"], "A", r"$\left[\frac23x^{3/2}\right]_0^9 = 18$."),
    MCQ(r"The area of the region between $y = x^3$ and $y = x$ (both pieces) is", [r"$0$", r"$\frac14$", r"$1$", r"$\frac12$"], "D", r"Meet at $-1, 0, 1$; each piece has area $\frac14$.", why_not={"A": "the pieces cancel when integrated as one"}),
    MCQ(r"The curves $y = \cos x$ and $y = x^2$ bound a region. To three decimal places, its area is", [r"$0.824$", r"$1.095$", r"$1.648$", r"$0.547$"], "B", rf"They meet at $x \approx \pm{_c[1]:.4f}$; $\int (\cos x - x^2)\,dx \approx {_m4:.3f}$.", calc=True),
]
same("m", [area(4, x**2, -2, 2), area(sp.sqrt(x), 0, 0, 9), 2 * area(x, x**3, 0, 1)], [sp.Rational(32, 3), 18, sp.Rational(1, 2)])

FRQS = []

TOPIC = Topic(
    number="8.4", title="Finding the Area Between Curves Expressed as Functions of x",
    unit="Unit 8: Applications of Integration", ced=["CHA-5.A", "CHA-5.A.1", "CHA-5.A.2"],
    goals=r"Find the area between two curves by integrating top minus bottom with respect to $x$.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
