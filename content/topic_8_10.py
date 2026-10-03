"""Topic 8.10: Volume with the disc method: revolving around other axes.

CED: CHA-5.D (CHA-5.D.3, CHA-5.D.4): revolving about a horizontal line y = k or vertical line x = k that bounds the
region gives discs of radius R = distance from the axis to the curve (bigger - smaller); V = pi * integral of R^2.
Lesson example: y = x^2 and y = 4 about y = 4 (512 pi/15). Worked examples: sqrt x, y = 2, y-axis about y = 2 (8 pi/3);
x = y^2 and x = 1 about x = 1 (16 pi/15); y = x^2, x-axis, x = 1 about x = 1 (pi/6).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)
from calclib.figs import region

x, y = sp.symbols("x y", real=True)


def disc(R, a, b, v=x):
    return sp.simplify(sp.pi * sp.integrate(sp.expand(R**2), (v, a, b)))


same("lesson", [disc(4 - x**2, -2, 2)], [512 * sp.pi / 15])
same("ex", [disc(2 - sp.sqrt(x), 0, 4), disc(1 - y**2, -1, 1, y), disc(1 - sp.sqrt(y), 0, 1, y)], [8 * sp.pi / 3, 16 * sp.pi / 15, sp.pi / 6])

FIG = region("t8_10_axis", [("x^2", -2.2, 2.2)], (-2.6, 2.6), (-0.4, 5), [(lambda v: 4, lambda v: v * v, -2, 2)], hlines=[4],
             labels=[(2.5, 4, "above left", r"axis $y = 4$"), (1.1, 2.6, "right", r"$R = 4 - x^2$")], caption=r"Revolving about $y = 4$: the radius runs from the curve up to the axis.")

NOTES = [
    Video("s8_10.py::Lesson", "Discs about other axes", 5),

    Section("The radius is a distance to the axis"),
    Text(r"When the axis is a line $y = k$ or $x = k$ that bounds the region, the slices are still solid discs. Only the radius changes: it is the distance from the axis to the curve."),
    Formula("Radius about another axis", (r"Axis $y = k$: $R(x) = \blank{|f(x) - k|}$. Axis $x = k$: $R(y) = \blank{|g(y) - k|}$. Write it as bigger minus smaller. \[ V = \pi\int R^2 \]")),
    FIG,
    Text(r"\textbf{A common slip.} About $y = 4$, the radius to $y = x^2$ is $4 - x^2$, not $x^2$: $x^2$ is the distance to the $x$-axis."),
    VideoExample('Spinning about y = 4', work="4cm"),
    BigIdea(r"About any horizontal or vertical axis: $V = \pi\int R^2$, with $R$ = distance from the axis to the curve. Vertical axis means horizontal slices and $dy$."),
    Check(r"The region bounded by $y = x$, $y = 2$ and the $y$-axis is revolved about $y = 2$. Find the volume.", selfcheck(r"\tfrac{8\pi}{3}"), r"$R = 2 - x$: $\pi\int_0^2 (2 - x)^2\,dx = \frac{8\pi}{3}$ (a cone)."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"The region bounded by $y = x^2$ and $y = 1$ is revolved about $y = 1$. Find the volume.", num(disc(1 - x**2, -1, 1), tol=1e-3), r"$R = 1 - x^2$: $\frac{16\pi}{15}$.", work="1.8cm"),
    Item(r"The region bounded by $y = \sqrt x$, $y = 1$ and the $y$-axis is revolved about $y = 1$. Find the volume.", num(disc(1 - sp.sqrt(x), 0, 1), tol=1e-3), r"$\pi\int_0^1 (1 - \sqrt x)^2\,dx = \frac\pi6$.", work="1.8cm"),
    Item(r"The region bounded by $y = 9 - x^2$ and $y = 0$ is revolved about $y = 0$. Find the volume.", num(disc(9 - x**2, -3, 3), tol=1e-2), r"$\pi\int_{-3}^3 (9 - x^2)^2\,dx = \frac{1296\pi}{5}$.", work="1.8cm"),
    Item(r"The region bounded by $x = y^2$ and $x = 4$ is revolved about $x = 4$. Find the volume.", num(disc(4 - y**2, -2, 2, y), tol=1e-3), r"$\frac{512\pi}{15}$.", work="1.8cm"),
    Item(r"The region bounded by $y = e^x$, $y = e$ and the $y$-axis is revolved about $y = e$. Write the integral for the volume.", selfcheck(r"\pi\int_0^1 \left(e - e^x\right)^2 dx"), r"$R = e - e^x$ for $0 \le x \le 1$.", work="1.4cm"),
    Item(r"The region bounded by $y = 2x$, $x = 2$ and $y = 0$ is revolved about $x = 2$. Find the volume.", num(disc(2 - y / 2, 0, 4, y), tol=1e-3), r"$R = 2 - \frac y2$, $0 \le y \le 4$: $\frac{16\pi}{3}$ (a cone).", work="1.8cm"),
    Item(r"The region bounded by $y = x^3$, $y = 8$ and the $y$-axis is revolved about $y = 8$. Find the volume.", num(disc(8 - x**3, 0, 2), tol=1e-3), r"$\pi\int_0^2 (8 - x^3)^2\,dx = \pi\left(128 - 64 + \frac{128}{7}\right) = \frac{576\pi}{7}$.", work="2cm"),
    Item(r"The region bounded by $y = 1 - x^2$ and $y = 0$ is revolved about $y = 0$. Find the volume.", num(disc(1 - x**2, -1, 1), tol=1e-3), r"$\frac{16\pi}{15}$: the same as revolving the region under $y = 1$ above $y = x^2$ about $y = 1$.", work="1.6cm"),
]
same("p", [disc(8 - x**3, 0, 2), disc(9 - x**2, -3, 3)], [576 * sp.pi / 7, 1296 * sp.pi / 5])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"The region bounded by $y = x^2$ and $y = 9$ is revolved about $y = 9$. The radius at $x$ is", [r"$x^2$", r"$9 - x^2$", r"$x^2 - 9$", r"$9$"], "B", r"From the curve up to the axis.", why_not={"A": "the distance to the $x$-axis"}),
        MCQ(r"The region bounded by $x = y^2$ and $x = 9$ is revolved about $x = 9$. The radius at $y$ is", [r"$9 - y^2$", r"$y^2$", r"$y^2 - 9$", r"$3 - y$"], "A", r"From the curve over to the axis."),
    ),
    Variants(
        Item(r"The region bounded by $y = x$, $y = 1$ and the $y$-axis is revolved about $y = 1$. Find the volume.", num(disc(1 - x, 0, 1), tol=1e-3), r"$\pi\int_0^1 (1 - x)^2\,dx = \frac\pi3$.", work="1.4cm"),
        Item(r"The region bounded by $y = 2x$, $y = 2$ and the $y$-axis is revolved about $y = 2$. Find the volume.", num(disc(2 - 2 * x, 0, 1), tol=1e-3), r"$\frac{4\pi}{3}$.", work="1.4cm"),
    ),
    Variants(
        Item(r"The region bounded by $y = x^2$ and $y = 4$ is revolved about $y = 4$. Write the integral for the volume.", selfcheck(r"\pi\int_{-2}^{2} \left(4 - x^2\right)^2 dx"), r"$R = 4 - x^2$.", work="1.2cm"),
        Item(r"The region bounded by $x = y^2$ and $x = 9$ is revolved about $x = 9$. Write the integral for the volume.", selfcheck(r"\pi\int_{-3}^{3} \left(9 - y^2\right)^2 dy"), r"$R = 9 - y^2$.", work="1.2cm"),
    ),
    Variants(
        Item(r"The region bounded by $y = \sqrt x$, $y = 2$ and the $y$-axis is revolved about $y = 2$. Find the volume.", num(disc(2 - sp.sqrt(x), 0, 4), tol=1e-3), r"$\frac{8\pi}{3}$.", work="1.8cm"),
        Item(r"The region bounded by $y = x^2$, $x = 2$ and $y = 0$ is revolved about $x = 2$. Find the volume.", num(disc(2 - sp.sqrt(y), 0, 4, y), tol=1e-3), r"$\pi\int_0^4 (2 - \sqrt y)^2\,dy = \frac{8\pi}{3}$.", work="1.8cm"),
    ),
    Variants(
        MCQ(r"Revolving the region bounded by $y = x^2$ and $y = 4$ about $y = 4$ instead of about the $x$-axis", [r"gives a solid with a hole", r"gives solid discs", r"is impossible", r"gives the same volume"], "B",
            r"The region touches $y = 4$ all the way across."),
    ),
]

# ---------------------------------------------------------------- test prep
_m4 = float(disc(1 - sp.sin(x), 0, sp.pi / 2))
close("m4", _m4, 1.119, 5e-3)
MCQS = [
    MCQ(r"The region bounded by $y = x^2$ and $y = 1$ is revolved about the line $y = 1$. The volume is", [r"$\frac{8\pi}{15}$", r"$\frac{16\pi}{15}$", r"$\frac{4\pi}{3}$", r"$\frac{2\pi}{5}$"], "B", r"$\pi\int_{-1}^1 (1 - x^2)^2\,dx$.",
        why_not={"A": "only one side", "D": "used $R = x^2$"}),
    MCQ(r"Which integral gives the volume when the region bounded by $y = \sqrt x$, $y = 3$ and the $y$-axis is revolved about $y = 3$?", [r"$\pi\int_0^9 x\,dx$", r"$\pi\int_0^9 (9 - x)\,dx$",
        r"$\pi\int_0^3 \left(3 - \sqrt x\right)^2 dx$", r"$\pi\int_0^9 \left(3 - \sqrt x\right)^2 dx$"], "D", r"$R = 3 - \sqrt x$, $0 \le x \le 9$."),
    MCQ(r"The region bounded by $x = 4 - y^2$ and the $y$-axis is revolved about the $y$-axis. The volume is", [r"$\frac{512\pi}{15}$", r"$\frac{256\pi}{15}$", r"$\frac{32\pi}{3}$", r"$8\pi$"], "A", r"$\pi\int_{-2}^2 (4 - y^2)^2\,dy$."),
    MCQ(r"The region bounded by $y = \sin x$, $y = 1$ and the $y$-axis is revolved about $y = 1$. To three decimal places, the volume is", [r"$0.571$", r"$2.238$", rf"${_m4:.3f}$", r"$0.356$"], "C",
        rf"$\pi\int_0^{{\pi/2}} (1 - \sin x)^2\,dx \approx {_m4:.3f}$.", calc=True),
]
same("m", [disc(1 - x**2, -1, 1), disc(4 - y**2, -2, 2, y)], [16 * sp.pi / 15, 512 * sp.pi / 15])

FRQS = []

TOPIC = Topic(
    number="8.10", title="Volume with Disc Method: Revolving Around Other Axes",
    unit="Unit 8: Applications of Integration", ced=["CHA-5.D", "CHA-5.D.3", "CHA-5.D.4"],
    goals=r"Find volumes by the disc method when the axis of revolution is a horizontal or vertical line other than the coordinate axes.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
