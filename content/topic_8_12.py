"""Topic 8.12: Volume with the washer method: revolving around other axes.

CED: CHA-5.D (CHA-5.D.7, CHA-5.D.8): about a horizontal or vertical line that doesn't bound the region, slices are
washers with radii measured from the axis (bigger - smaller); which curve is outer depends on where the axis is.
Lesson example: y = x and y = x^2 about y = -1 (7 pi/15) and about y = 2 (8 pi/15). Worked examples: same region about
x = -1 (pi/2); x^2 and y = 4 about y = -2 (1408 pi/15); sqrt x and x/2 about y = 3 (16 pi/3).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)
from calclib.figs import region

x, y = sp.symbols("x y", real=True)


def washer(R, r, a, b, v=x):
    return sp.simplify(sp.pi * sp.integrate(sp.expand(R**2 - r**2), (v, a, b)))


same("lesson", [washer(x + 1, x**2 + 1, 0, 1), washer(2 - x**2, 2 - x, 0, 1)], [7 * sp.pi / 15, 8 * sp.pi / 15])
same("ex", [washer(sp.sqrt(y) + 1, y + 1, 0, 1, y), washer(6, x**2 + 2, -2, 2), washer(3 - x / 2, 3 - sp.sqrt(x), 0, 4)], [sp.pi / 2, 1408 * sp.pi / 15, 16 * sp.pi / 3])

FIG = region("t8_12_axis", [("x", -0.2, 1.2), ("x^2", -0.2, 1.15)], (-0.3, 1.4), (-1.4, 1.4), [(lambda v: v, lambda v: v * v, 0, 1)], hlines=[-1], xstep=0.5, ystep=0.5,
             labels=[(1.35, -1, "above left", r"$y = -1$")], caption=r"About $y = -1$: $R = x + 1$ (to the line) and $r = x^2 + 1$ (to the parabola).")
FIG_FRQ = region("t8_12_frq", [("4-x^2", -2.4, 2.1), ("x+2", -2.6, 1.6)], (-2.7, 2.2), (-1.3, 5.3), [(lambda v: 4 - v * v, lambda v: v + 2, -2, 1)], labels=[(-0.5, 2.6, "center", "$R$")],
                 caption=r"Region $R$, between $y = 4 - x^2$ and $y = x + 2$.")

NOTES = [
    Video("s8_12.py::Lesson", "Washers about other axes", 5),

    Section("Measure from the axis"),
    Text(r"Every radius starts at the axis of revolution. With the axis $y = -1$ below the region, the distance up to $y = x$ is $x - (-1) = x + 1$."),
    Formula("Radii about $y = k$ or $x = k$", (r"Radius $=$ (farther value) $-$ (nearer value): \blank{curve $- k$} if the axis is below (or left), \blank{$k -$ curve} if it is above (or right). Then \[ V = \pi\int \left(R^2 - r^2\right). \]")),
    FIG,
    VideoExample('About y = −1', work="4.6cm"),
    Text(r"\textbf{Outer depends on the axis.} About $y = 2$ (above the region), the parabola is farther: $R = 2 - x^2$, $r = 2 - x$, and $V = \frac{8\pi}{15}$."),
    BigIdea(r"Sketch the axis and both radii first. Each radius is bigger minus smaller, measured from the axis; then $V = \pi\int (R^2 - r^2)$."),
    Check(r"The region between $y = 1$ and $y = 2$ for $0 \le x \le 3$ is revolved about $y = -1$. Find the volume.", selfcheck(r"15\pi"), r"$R = 3$, $r = 2$: $\pi\int_0^3 (9 - 4)\,dx = 15\pi$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"The region between $y = x$ and $y = x^2$ is revolved about $y = -2$. Find the volume.", num(washer(x + 2, x**2 + 2, 0, 1), tol=1e-3), r"$\pi\int_0^1 \left((x + 2)^2 - (x^2 + 2)^2\right) dx = \frac{4\pi}{5}$.", work="2.2cm"),
    Item(r"The region between $y = x$ and $y = x^2$ is revolved about $y = 1$. Find the volume.", num(washer(1 - x**2, 1 - x, 0, 1), tol=1e-3), r"$R = 1 - x^2$, $r = 1 - x$: $\pi\int_0^1 \left(x^4 - 3x^2 + 2x\right) dx = \frac\pi5$.", work="2.2cm"),
    Item(r"The region between $y = x$ and $y = x^2$ is revolved about $x = 2$. Find the volume.", num(washer(2 - y, 2 - sp.sqrt(y), 0, 1, y), tol=1e-3), r"$R = 2 - y$, $r = 2 - \sqrt y$: $\frac\pi2$.", work="2.2cm"),
    Item(r"The region between $y = x^2$ and $y = 4$ is revolved about $y = -1$. Find the volume.", num(washer(5, x**2 + 1, -2, 2), tol=1e-2), r"$R = 5$, $r = x^2 + 1$: $\pi\int_{-2}^2 \left(24 - x^4 - 2x^2\right) dx = \frac{1088\pi}{15}$.", work="2.2cm"),
    Item(r"The region between $y = \sqrt x$ and the $x$-axis for $0 \le x \le 4$ is revolved about $y = 3$. Find the volume.", num(washer(3, 3 - sp.sqrt(x), 0, 4), tol=1e-3),
         r"$R = 3$, $r = 3 - \sqrt x$: $\pi\int_0^4 \left(6\sqrt x - x\right) dx = 24\pi$.", work="2.2cm"),
    Item(r"The region between $y = \sqrt x$ and the $x$-axis for $0 \le x \le 4$ is revolved about $x = 5$. Find the volume.", num(washer(5 - y**2, 1, 0, 2, y), tol=1e-3),
         r"$R = 5 - y^2$, $r = 5 - 4 = 1$, $0 \le y \le 2$: $\frac{416\pi}{15}$.", work="2.2cm"),
    Item(r"The region between $y = 2x$ and $y = x^2$ is revolved about $y = 4$. Write, but do not evaluate, the integral.", selfcheck(r"\pi\int_0^2 \left((4 - x^2)^2 - (4 - 2x)^2\right) dx"), r"The axis is above; the parabola is farther.", work="1.6cm"),
    Item(r"The region between $y = e^x$ and $y = 1$ for $0 \le x \le 1$ is revolved about $y = -1$. Write, but do not evaluate, the integral.", selfcheck(r"\pi\int_0^1 \left((e^x + 1)^2 - 4\right) dx"), r"$R = e^x + 1$, $r = 2$.", work="1.6cm"),
]
same("p", [washer(x + 2, x**2 + 2, 0, 1), washer(1 - x**2, 1 - x, 0, 1), washer(5, x**2 + 1, -2, 2), washer(3, 3 - sp.sqrt(x), 0, 4), washer(5 - y**2, 1, 0, 2, y)],
     [4 * sp.pi / 5, sp.pi / 5, 1088 * sp.pi / 15, 24 * sp.pi, 416 * sp.pi / 15])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"The region between $y = x$ and $y = x^2$ is revolved about $y = -3$. The outer radius is", [r"$x^2 + 3$", r"$x - 3$", r"$x + 3$", r"$3 - x$"], "C", r"From $-3$ up to the farther curve, $y = x$."),
        MCQ(r"The region between $y = x$ and $y = x^2$ is revolved about $y = 3$. The outer radius is", [r"$3 - x^2$", r"$3 - x$", r"$x^2 + 3$", r"$x - 3$"], "A", r"From $3$ down to the farther curve, $y = x^2$."),
    ),
    Variants(
        Item(r"The region between $y = 1$ and $y = 2$, $0 \le x \le 2$, is revolved about $y = 3$. Find the volume.", num(washer(2, 1, 0, 2), tol=1e-3), r"$R = 3 - 1 = 2$, $r = 3 - 2 = 1$: $6\pi$.", work="1.6cm"),
        Item(r"The region between $y = 1$ and $y = 3$, $0 \le x \le 1$, is revolved about $y = -1$. Find the volume.", num(washer(4, 2, 0, 1), tol=1e-3), r"$R = 4$, $r = 2$: $12\pi$.", work="1.6cm"),
    ),
    Variants(
        Item(r"The region between $y = x$ and $y = x^2$ is revolved about $y = -1$. Write the integral for the volume.", selfcheck(r"\pi\int_0^1 \left((x + 1)^2 - (x^2 + 1)^2\right) dx"), r"$R = x + 1$, $r = x^2 + 1$.", work="1.4cm"),
        Item(r"The region between $y = x$ and $y = x^2$ is revolved about $x = -1$. Write the integral for the volume.", selfcheck(r"\pi\int_0^1 \left((\sqrt y + 1)^2 - (y + 1)^2\right) dy"), r"$R = \sqrt y + 1$, $r = y + 1$.", work="1.4cm"),
    ),
    Variants(
        Item(r"The region between $y = x^2$ and $y = 1$ is revolved about $y = -1$. Find the volume.", num(washer(2, x**2 + 1, -1, 1), tol=1e-3), r"$\pi\int_{-1}^1 \left(4 - (x^2 + 1)^2\right) dx = \frac{56\pi}{15}$.", work="2cm"),
        Item(r"The region between $y = x^2$ and $y = 1$ is revolved about $y = 2$. Find the volume.", num(washer(2 - x**2, 1, -1, 1), tol=1e-3), r"$\pi\int_{-1}^1 \left((2 - x^2)^2 - 1\right) dx = \frac{64\pi}{15}$.", work="2cm"),
    ),
    Variants(
        MCQ(r"Moving the axis of revolution from $y = 0$ down to $y = -1$ changes both radii by", [r"subtracting $1$", r"adding $1$", r"doubling them", r"nothing"], "B", r"Every distance up from the axis grows by $1$."),
    ),
]

# ---------------------------------------------------------------- test prep
_c = float(sp.nsolve(sp.exp(-x) - x, x, 0.6))
_m4 = float(sp.pi * sp.Integral((sp.exp(-x) + 1)**2 - (x + 1)**2, (x, 0, _c)).evalf())
MCQS = [
    MCQ(r"The region between $y = x^2$ and $y = 4$ is revolved about $y = 5$. Which gives the volume?", [r"$\pi\int_{-2}^2 \left((5 - x^2)^2 - 1\right) dx$", r"$\pi\int_{-2}^2 \left((5 - x^2) - 1\right)^2 dx$",
        r"$\pi\int_{-2}^2 \left(25 - x^4\right) dx$", r"$\pi\int_{-2}^2 \left(1 - (5 - x^2)^2\right) dx$"], "A", r"$R = 5 - x^2$, $r = 5 - 4 = 1$."),
    MCQ(r"The region between $y = x$ and $y = x^2$ is revolved about $x = 2$. The volume is", [r"$\frac\pi6$", r"$\frac{2\pi}{15}$", r"$\frac{\pi}{2}$", r"$\pi$"], "C",
        r"$\pi\int_0^1 \left((2 - y)^2 - (2 - \sqrt y)^2\right) dy = \pi\int_0^1 \left(y^2 - 5y + 4\sqrt y\right) dy = \frac\pi2$."),
    MCQ(r"The region between $y = \sqrt x$ and $y = x$ is revolved about $y = 1$. The volume is", [r"$\frac\pi6$", r"$\frac{\pi}{3}$", r"$\frac{\pi}{2}$", r"$\frac{\pi}{12}$"], "A",
        r"$R = 1 - x$, $r = 1 - \sqrt x$: $\pi\int_0^1 \left(x^2 - 3x + 2\sqrt x\right) dx = \pi\left(\frac13 - \frac32 + \frac43\right) = \frac\pi6$."),
    MCQ(r"The region in the first quadrant between $y = e^{-x}$ and $y = x$ (and the $y$-axis) is revolved about $y = -1$. To three decimal places, the volume is", [r"$1.013$", r"$3.183$", r"$6.367$", rf"${_m4:.3f}$"], "D",
        rf"They meet at $x \approx {_c:.4f}$; $\pi\int_0^{{{_c:.4f}}} \left((e^{{-x}} + 1)^2 - (x + 1)^2\right) dx \approx {_m4:.3f}$.", calc=True),
]
close("m4", _m4, 2.584, 5e-3)
same("m", [washer(2 - y, 2 - sp.sqrt(y), 0, 1, y), washer(1 - x, 1 - sp.sqrt(x), 0, 1)], [sp.pi / 2, sp.pi / 6])

# ---------------------------------------------------------------- FRQ
f, g = 4 - x**2, x + 2
same("frq", [sorted(sp.solve(sp.Eq(f, g), x)), sp.integrate(f - g, (x, -2, 1)), washer(f + 1, g + 1, -2, 1), washer(5 - g, 5 - f, -2, 1), sp.integrate((f - g)**2, (x, -2, 1))],
     [[-2, 1], sp.Rational(9, 2), 153 * sp.pi / 5, 117 * sp.pi / 5, sp.Rational(81, 10)])
FRQS = [
    FRQ("Area and volume", (r"Let $R$ be the region bounded by the graphs of $y = 4 - x^2$ and $y = x + 2$, as shown."), [
        Part("a", r"Find the area of $R$.", num(sp.Rational(9, 2)), r"$4 - x^2 = x + 2$ gives $x = -2$ and $x = 1$. $\int_{-2}^1 \left(2 - x - x^2\right) dx = \frac92$.", [(1, "limits"), (1, "integral"), (1, "answer")], work="2.6cm"),
        Part("b", r"Find the volume of the solid generated when $R$ is revolved about the horizontal line $y = -1$.", num(153 * sp.pi / 5, tol=0.01, display=r"\tfrac{153\pi}{5}"),
             r"$R_{\text{out}} = (4 - x^2) + 1 = 5 - x^2$, $r_{\text{in}} = (x + 2) + 1 = x + 3$. $V = \pi\int_{-2}^1 \left((5 - x^2)^2 - (x + 3)^2\right) dx = \frac{153\pi}{5}$.",
             [(1, "outer radius"), (1, "inner radius"), (1, "integral and answer")], work="3cm"),
        Part("c", r"Write, but do not evaluate, an integral expression for the volume of the solid generated when $R$ is revolved about the horizontal line $y = 5$.", selfcheck(r"\pi\int_{-2}^{1} \left((3 - x)^2 - (1 + x^2)^2\right) dx"),
             r"The axis is above $R$, so the line is farther: $R_{\text{out}} = 5 - (x + 2) = 3 - x$, $r_{\text{in}} = 5 - (4 - x^2) = 1 + x^2$. $V = \pi\int_{-2}^1 \left((3 - x)^2 - (1 + x^2)^2\right) dx$.",
             [(1, "radii"), (1, "integral expression")], work="2.4cm"),
        Part("d", r"$R$ is the base of a solid whose cross sections perpendicular to the $x$-axis are squares. Find the volume of the solid.", num(sp.Rational(81, 10)),
             r"$\int_{-2}^1 \left(2 - x - x^2\right)^2 dx = \frac{81}{10}$.", [(1, "integrand"), (1, "answer")], work="2cm"),
    ], frq_type="Area and volume", figure=FIG_FRQ),
]

TOPIC = Topic(
    number="8.12", title="Volume with Washer Method: Revolving Around Other Axes",
    unit="Unit 8: Applications of Integration", ced=["CHA-5.D", "CHA-5.D.7", "CHA-5.D.8"],
    goals=r"Find volumes with the washer method when the axis of revolution is a horizontal or vertical line other than the coordinate axes.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
