"""Topic 8.11: Volume with the washer method: revolving around the x- or y-axis.

CED: CHA-5.D (CHA-5.D.5, CHA-5.D.6): when the region doesn't touch the axis, slices are washers:
V = pi * integral of (R^2 - r^2), R from the axis to the farther curve, r to the nearer; square each radius
separately. Lesson example: y = x and y = x^2 about the x-axis (2 pi/15), then about the y-axis (pi/6). Worked
examples: sqrt x and x about the x-axis (pi/6); 4 - x^2 and y = 3 about the x-axis (136 pi/15); 2x and x^2 about the
y-axis (8 pi/3).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)
from calclib.figs import region

x, y = sp.symbols("x y", real=True)


def washer(R, r, a, b, v=x):
    return sp.simplify(sp.pi * sp.integrate(sp.expand(R**2 - r**2), (v, a, b)))


same("lesson", [washer(x, x**2, 0, 1), washer(sp.sqrt(y), y, 0, 1, y)], [2 * sp.pi / 15, sp.pi / 6])
same("ex", [washer(sp.sqrt(x), x, 0, 1), washer(4 - x**2, 3, -1, 1), washer(sp.sqrt(y), y / 2, 0, 4, y)], [sp.pi / 6, 136 * sp.pi / 15, 8 * sp.pi / 3])

FIG = region("t8_11_w", [("x", 0, 1.15), ("x^2", 0, 1.1)], (-0.2, 1.3), (-0.2, 1.3), [(lambda v: v, lambda v: v * v, 0, 1)], xstep=0.5, ystep=0.5,
             caption=r"The region between $y = x$ and $y = x^2$. About the $x$-axis, $R = x$ and $r = x^2$.")

NOTES = [
    Video("s8_11.py::Lesson", "The washer method", 5),

    Section("Outer and inner radius"),
    Text(r"If there is a gap between the region and the axis, each slice is a washer: a disc with a hole."),
    Formula("Washer method", (r"\[ V = \pi\int_a^b \blank{\left(R(x)^2 - r(x)^2\right)}\,dx, \] where $R$ is the distance from the axis to the farther curve and $r$ the distance to the nearer curve. "
                              r"About the $y$-axis, use $dy$ and radii in terms of $y$.")),
    Text(r"\textbf{Square each radius separately.} $(R - r)^2 \ne R^2 - r^2$: with $R = 3$, $r = 2$, $(3 - 2)^2 = 1$ but $9 - 4 = 5$."),
    FIG,
    VideoExample('Washers between a line and a parabola', work="4cm"),
    Text(r"\textbf{Which curve is outer depends on the axis.} About the $y$-axis the same region has $R = \sqrt y$ (the parabola) and $r = y$ (the line): $V = \pi\int_0^1 (y - y^2)\,dy = \frac\pi6$."),
    BigIdea(r"Washers: $V = \pi\int (R^2 - r^2)$ with $R$ to the farther curve and $r$ to the nearer one."),
    Check(r"The region between $y = 2$ and $y = 1$ for $0 \le x \le 3$ is revolved about the $x$-axis. Find the volume.", selfcheck(r"9\pi"), r"$\pi\int_0^3 (4 - 1)\,dx$: a thick-walled pipe."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"The region between $y = x$ and $y = x^3$ for $0 \le x \le 1$ is revolved about the $x$-axis. Find the volume.", num(washer(x, x**3, 0, 1), tol=1e-3), r"$\pi\int_0^1 (x^2 - x^6)\,dx = \frac{4\pi}{21}$.", work="1.8cm"),
    Item(r"The region between $y = 2x$ and $y = x^2$ is revolved about the $x$-axis. Find the volume.", num(washer(2 * x, x**2, 0, 2), tol=1e-3), r"$\pi\int_0^2 (4x^2 - x^4)\,dx = \frac{64\pi}{15}$.", work="1.8cm"),
    Item(r"The region between $y = \sqrt x$ and $y = \frac x2$ is revolved about the $x$-axis. Find the volume.", num(washer(sp.sqrt(x), x / 2, 0, 4), tol=1e-3), r"$\pi\int_0^4 \left(x - \frac{x^2}{4}\right) dx = \frac{8\pi}{3}$.", work="1.8cm"),
    Item(r"The region between $y = 5$ and $y = x^2 + 1$ is revolved about the $x$-axis. Find the volume.", num(washer(5, x**2 + 1, -2, 2), tol=1e-2),
         r"Meet at $x = \pm2$: $\pi\int_{-2}^2 \left(25 - (x^2 + 1)^2\right) dx = \frac{1088\pi}{15}$.", work="2.2cm"),
    Item(r"The region between $y = x$ and $y = x^2$ is revolved about the $y$-axis. Find the volume.", num(washer(sp.sqrt(y), y, 0, 1, y), tol=1e-3), r"$R = \sqrt y$, $r = y$: $\frac\pi6$.", work="1.8cm"),
    Item(r"The region between $x = y^2$ and $x = 2y$ is revolved about the $y$-axis. Find the volume.", num(washer(2 * y, y**2, 0, 2, y), tol=1e-3),
         r"Meet at $y = 0, 2$; $2y \ge y^2$ there, so $R = 2y$, $r = y^2$: $\pi\int_0^2 (4y^2 - y^4)\,dy = \frac{64\pi}{15}$.", work="2cm"),
    Item(r"The region bounded by $y = e^x$, $y = 1$ and $x = 1$ is revolved about the $x$-axis. Find the volume.", num(washer(sp.exp(x), 1, 0, 1), tol=1e-3), r"$\pi\int_0^1 (e^{2x} - 1)\,dx = \pi\left(\frac{e^2 - 1}{2} - 1\right) = \frac\pi2(e^2 - 3)$.", work="2cm"),
    Item(r"The region between $y = \sqrt x$ and $y = x^2$ is revolved about the $x$-axis. Write and evaluate the integral.", num(washer(sp.sqrt(x), x**2, 0, 1), tol=1e-3), r"$\pi\int_0^1 (x - x^4)\,dx = \frac{3\pi}{10}$.", work="1.8cm"),
]
same("p", [washer(5, x**2 + 1, -2, 2), washer(2 * y, y**2, 0, 2, y), washer(sp.exp(x), 1, 0, 1)], [1088 * sp.pi / 15, 64 * sp.pi / 15, sp.pi * (sp.E**2 - 3) / 2])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"The region between $y = x$ and $y = x^2$ is revolved about the $x$-axis. Which gives the volume?", [r"$\pi\int_0^1 \left(x - x^2\right)^2 dx$", r"$\pi\int_0^1 \left(x^2 - x^4\right) dx$",
            r"$\pi\int_0^1 \left(x^4 - x^2\right) dx$", r"$2\pi\int_0^1 \left(x - x^2\right) dx$"], "B", r"$R = x$, $r = x^2$.", why_not={"A": "squared the difference instead of each radius"}),
        MCQ(r"The region between $y = \sqrt x$ and $y = x$ is revolved about the $x$-axis. Which gives the volume?", [r"$\pi\int_0^1 \left(\sqrt x - x\right)^2 dx$", r"$\pi\int_0^1 \left(x^2 - x\right) dx$",
            r"$\pi\int_0^1 \left(x - x^2\right) dx$", r"$\pi\int_0^1 \left(\sqrt x - x\right) dx$"], "C", r"$R = \sqrt x$, $r = x$.", why_not={"A": "squared the difference instead of each radius"}),
    ),
    Variants(
        Item(r"The region between $y = 2$ and $y = x$ for $0 \le x \le 2$ is revolved about the $x$-axis. Find the volume.", num(washer(2, x, 0, 2), tol=1e-3), r"$\pi\int_0^2 (4 - x^2)\,dx = \frac{16\pi}{3}$.", work="1.6cm"),
        Item(r"The region between $y = 1$ and $y = x^2$ for $0 \le x \le 1$ is revolved about the $x$-axis. Find the volume.", num(washer(1, x**2, 0, 1), tol=1e-3), r"$\pi\int_0^1 (1 - x^4)\,dx = \frac{4\pi}{5}$.", work="1.6cm"),
        Item(r"The region between $y = 3$ and $y = \sqrt x$ for $0 \le x \le 9$ is revolved about the $x$-axis. Find the volume.", num(washer(3, sp.sqrt(x), 0, 9), tol=1e-2), r"$\pi\int_0^9 (9 - x)\,dx = \frac{81\pi}{2}$.", work="1.6cm"),
    ),
    Variants(
        Item(r"The region between $y = x$ and $y = x^2$ is revolved about the $y$-axis. Which curve gives the outer radius?", selfcheck(r"y = x^2 \ (x = \sqrt y)"), r"For $0 < y < 1$, $\sqrt y > y$.", work="1cm"),
        Item(r"The region between $y = x$ and $y = x^2$ is revolved about the $x$-axis. Which curve gives the outer radius?", selfcheck(r"y = x"), r"For $0 < x < 1$, $x > x^2$.", work="1cm"),
    ),
    Variants(
        Item(r"The region between $y = x^2$ and $y = 2x$ is revolved about the $y$-axis. Find the volume.", num(washer(sp.sqrt(y), y / 2, 0, 4, y), tol=1e-3), r"$\frac{8\pi}{3}$.", work="1.8cm"),
        Item(r"The region between $y = x^3$ and $y = x$, $0 \le x \le 1$, is revolved about the $y$-axis. Find the volume.", num(washer(y**sp.Rational(1, 3), y, 0, 1, y), tol=1e-3), r"$\pi\int_0^1 \left(y^{2/3} - y^2\right) dy = \frac{4\pi}{15}$.", work="1.8cm"),
    ),
    Variants(
        MCQ(r"A washer has outer radius $5$ and inner radius $3$. The area of its face is", [r"$4\pi$", r"$34\pi$", r"$16\pi$", r"$2\pi$"], "C", r"$\pi(25 - 9)$.", why_not={"A": "used $(5 - 3)^2$"}),
    ),
]

# ---------------------------------------------------------------- test prep
_c = float(sp.nsolve(sp.cos(x) - x, x, 0.7))
_m4 = float(sp.pi * sp.Integral(sp.cos(x)**2 - x**2, (x, 0, _c)).evalf())
MCQS = [
    MCQ(r"The region between $y = 4$ and $y = x^2$ is revolved about the $x$-axis. The volume is", [r"$\frac{256\pi}{5}$", r"$\frac{512\pi}{15}$", r"$\frac{128\pi}{5}$", r"$\frac{32\pi}{3}$"], "A",
        r"$\pi\int_{-2}^2 (16 - x^4)\,dx = \pi\left(64 - \frac{64}{5}\right) = \frac{256\pi}{5}$.", why_not={"B": "used $(4 - x^2)^2$"}),
    MCQ(r"The region between $y = x^2$ and $y = x^3$ for $0 \le x \le 1$ is revolved about the $x$-axis. The volume is", [r"$\frac{\pi}{12}$", r"$\frac{\pi}{35}$", r"$\frac{2\pi}{35}$", r"$\frac{\pi}{5}$"], "C",
        r"$\pi\int_0^1 (x^4 - x^6)\,dx = \pi\left(\frac15 - \frac17\right)$."),
    MCQ(r"The region in the first quadrant between $y = 2x$ and $y = x^2$ is revolved about the $y$-axis. Which gives the volume?", [r"$\pi\int_0^2 \left(4x^2 - x^4\right) dx$", r"$\pi\int_0^4 \left(\frac{y^2}{4} - y\right) dy$",
        r"$\pi\int_0^2 \left(y - \frac{y^2}{4}\right) dy$", r"$\pi\int_0^4 \left(y - \frac{y^2}{4}\right) dy$"], "D", r"$R = \sqrt y$, $r = \frac y2$, $0 \le y \le 4$.", why_not={"A": "washers about the $x$-axis"}),
    MCQ(r"The region in the first quadrant between $y = \cos x$ and $y = x$ (and the $y$-axis) is revolved about the $x$-axis. To three decimal places, the volume is", [r"$0.575$", r"$0.484$", rf"${_m4:.3f}$", r"$3.861$"], "C",
        rf"They meet at $x \approx {_c:.4f}$; $\pi\int_0^{{{_c:.4f}}} \left(\cos^2 x - x^2\right) dx \approx {_m4:.3f}$.", calc=True),
]
same("m", [washer(4, x**2, -2, 2), washer(x**2, x**3, 0, 1)], [256 * sp.pi / 5, 2 * sp.pi / 35])
close("m4", _m4, 1.520, 5e-3)

FRQS = []

TOPIC = Topic(
    number="8.11", title="Volume with Washer Method: Revolving Around the x- or y-Axis",
    unit="Unit 8: Applications of Integration", ced=["CHA-5.D", "CHA-5.D.5", "CHA-5.D.6"],
    goals=r"Find volumes of solids of revolution with a hole, using outer and inner radii about the $x$- or $y$-axis.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
