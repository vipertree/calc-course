"""Topic 8.9: Volume with the disc method: revolving around the x- or y-axis.

CED: CHA-5.D (CHA-5.D.1, CHA-5.D.2): revolving a region about an axis makes a solid whose cross sections perpendicular to
the axis are discs of radius R, so V = pi * integral of R^2 (dx for a horizontal axis, dy for a vertical one); R is the
distance from the axis to the curve. Lesson example: sqrt x on [0, 4] about the x-axis (8 pi); cone check (18 pi);
y = x^2, y = 4, y-axis about the y-axis (8 pi). Worked examples: x^2 on [0, 2] (32 pi/5); e^x on [0, 1] (pi(e^2 - 1)/2);
x^3, y = 8, y-axis about the y-axis (96 pi/5).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)
from calclib.figs import region

x, y = sp.symbols("x y", real=True)


def disc(R, a, b, v=x):
    return sp.simplify(sp.pi * sp.integrate(sp.expand(R**2), (v, a, b)))


same("lesson", [disc(sp.sqrt(x), 0, 4), disc(x / 2, 0, 6), disc(sp.sqrt(y), 0, 4, y)], [8 * sp.pi, 18 * sp.pi, 8 * sp.pi])
same("ex", [disc(x**2, 0, 2), disc(sp.exp(x), 0, 1), disc(y**sp.Rational(1, 3), 0, 8, y)], [32 * sp.pi / 5, sp.pi * (sp.E**2 - 1) / 2, 96 * sp.pi / 5])

FIG = region("t8_9_root", [("sqrt(x)", 0, 4.3)], (-0.3, 4.6), (-0.3, 2.4), [(lambda v: v**0.5, lambda v: 0, 0, 4)], vlines=[4],
             caption=r"The region under $y = \sqrt x$, $0 \le x \le 4$. Revolved about the $x$-axis, the slice at $x$ is a disc of radius $\sqrt x$.")

NOTES = [
    Video("s8_9.py::Lesson", "The disc method", 5),

    Section("Every slice is a disc"),
    Text(r"Revolving a region about a line sweeps out a solid of revolution. Slices perpendicular to the axis are discs; the radius is the distance from the axis to the curve."),
    Formula("Disc method", (r"About a horizontal axis: \[ V = \blank{\pi\int_a^b [R(x)]^2\,dx}. \] About a vertical axis: \[ V = \blank{\pi\int_c^d [R(y)]^2\,dy}. \] "
                            r"Slice perpendicular to the axis and integrate along it.")),
    FIG,
    VideoExample('Discs on a root', work="3cm"),
    Text(r"\textbf{A check.} Revolving $y = \frac x2$, $0 \le x \le 6$, about the $x$-axis gives a cone of radius $3$ and height $6$: $\pi\int_0^6 \frac{x^2}{4}\,dx = 18\pi = \frac13\pi(3^2)(6)$."),
    Section("Around the $y$-axis"),
    Text(r"For a vertical axis the discs are horizontal: write the curve as $x$ in terms of $y$. Revolving the region bounded by $y = x^2$, $y = 4$ and the $y$-axis about the $y$-axis: $R = \sqrt y$, $V = \pi\int_0^4 y\,dy = 8\pi$."),
    BigIdea(r"$V = \pi\int R^2$, with $R$ the distance from the axis to the curve; integrate along the axis."),
    Check(r"The region under $y = 3$ for $0 \le x \le 2$ is revolved about the $x$-axis. Find the volume.", selfcheck(r"18\pi"), r"A cylinder: $\pi\int_0^2 9\,dx$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"The region under $y = x$ for $0 \le x \le 3$ is revolved about the $x$-axis. Find the volume.", num(disc(x, 0, 3), tol=1e-3), r"$\pi\int_0^3 x^2\,dx = 9\pi$.", work="1.4cm"),
    Item(r"The region under $y = \sqrt{x}$ for $0 \le x \le 9$ is revolved about the $x$-axis. Find the volume.", num(disc(sp.sqrt(x), 0, 9), tol=1e-3), r"$\pi\int_0^9 x\,dx = \frac{81\pi}{2}$.", work="1.4cm"),
    Item(r"The region under $y = 4 - x^2$ for $-2 \le x \le 2$ is revolved about the $x$-axis. Find the volume.", num(disc(4 - x**2, -2, 2), tol=1e-3), r"$\pi\int_{-2}^2 (4 - x^2)^2\,dx = \frac{512\pi}{15}$.", work="1.8cm"),
    Item(r"The region under $y = \frac1x$ for $1 \le x \le 4$ is revolved about the $x$-axis. Find the volume.", num(disc(1 / x, 1, 4), tol=1e-3), r"$\pi\int_1^4 x^{-2}\,dx = \frac{3\pi}{4}$.", work="1.4cm"),
    Item(r"The region under $y = \sqrt{\sin x}$ for $0 \le x \le \pi$ is revolved about the $x$-axis. Find the volume.", num(2 * sp.pi, tol=1e-3), r"$\pi\int_0^\pi \sin x\,dx = 2\pi$.", work="1.4cm"),
    Item(r"The region bounded by $y = x^2$, $y = 9$ and the $y$-axis ($x \ge 0$) is revolved about the $y$-axis. Find the volume.", num(disc(sp.sqrt(y), 0, 9, y), tol=1e-3), r"$\pi\int_0^9 y\,dy = \frac{81\pi}{2}$.", work="1.6cm"),
    Item(r"The region bounded by $y = 2x$, $y = 4$ and the $y$-axis is revolved about the $y$-axis. Find the volume.", num(disc(y / 2, 0, 4, y), tol=1e-3),
         r"$R = \frac y2$: $\pi\int_0^4 \frac{y^2}{4}\,dy = \frac{16\pi}{3}$ (a cone).", work="1.6cm"),
    Item(r"The region bounded by $x = 4 - y^2$ and the $y$-axis is revolved about the $y$-axis. Find the volume.", num(disc(4 - y**2, -2, 2, y), tol=1e-3), r"$\pi\int_{-2}^2 (4 - y^2)^2\,dy = \frac{512\pi}{15}$.", work="1.8cm"),
    Item(r"Use the disc method to show that a ball of radius $r$ has volume $\frac43\pi r^3$.", selfcheck(r"\pi\int_{-r}^{r} (r^2 - x^2)\,dx = \tfrac43\pi r^3"),
         r"Revolve $y = \sqrt{r^2 - x^2}$ about the $x$-axis: $\pi\int_{-r}^r (r^2 - x^2)\,dx = \pi\left(2r^3 - \frac23r^3\right) = \frac43\pi r^3$.", work="2.2cm"),
    Item(r"The region under $y = e^{-x}$ for $0 \le x \le \ln 3$ is revolved about the $x$-axis. Find the volume.", num(disc(sp.exp(-x), 0, sp.log(3)), tol=1e-3), r"$\pi\int_0^{\ln 3} e^{-2x}\,dx = \frac\pi2\left(1 - \frac19\right) = \frac{4\pi}{9}$.", work="1.8cm"),
]

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"The region under $y = 2x$ for $0 \le x \le 1$ is revolved about the $x$-axis. Find the volume.", num(disc(2 * x, 0, 1), tol=1e-3), r"$\frac{4\pi}{3}$.", work="1.2cm"),
        Item(r"The region under $y = x^2$ for $0 \le x \le 1$ is revolved about the $x$-axis. Find the volume.", num(disc(x**2, 0, 1), tol=1e-3), r"$\frac\pi5$.", work="1.2cm"),
        Item(r"The region under $y = \sqrt x$ for $0 \le x \le 2$ is revolved about the $x$-axis. Find the volume.", num(disc(sp.sqrt(x), 0, 2), tol=1e-3), r"$2\pi$.", work="1.2cm"),
    ),
    Variants(
        Item(r"The region bounded by $y = x^2$, $y = 1$ and the $y$-axis is revolved about the $y$-axis. Find the volume.", num(disc(sp.sqrt(y), 0, 1, y), tol=1e-3), r"$\pi\int_0^1 y\,dy = \frac\pi2$.", work="1.4cm"),
        Item(r"The region bounded by $y = x^3$, $y = 1$ and the $y$-axis is revolved about the $y$-axis. Find the volume.", num(disc(y**sp.Rational(1, 3), 0, 1, y), tol=1e-3), r"$\pi\int_0^1 y^{2/3}\,dy = \frac{3\pi}{5}$.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"The region under $y = \sqrt{x}$, $0 \le x \le 4$, is revolved about the $x$-axis. Which gives the volume?", [r"$\pi\int_0^4 \sqrt x\,dx$", r"$\pi\int_0^4 x\,dx$", r"$\int_0^4 \pi x^2\,dx$", r"$2\pi\int_0^4 x\,dx$"], "B", r"$R^2 = x$.",
            why_not={"A": "forgot to square the radius"}),
        MCQ(r"The region bounded by $y = x^2$, $y = 4$ and the $y$-axis is revolved about the $y$-axis. Which gives the volume?", [r"$\pi\int_0^2 x^4\,dx$", r"$\pi\int_0^4 y^2\,dy$", r"$\pi\int_0^4 y\,dy$", r"$\pi\int_0^2 (4 - x^2)^2\,dx$"], "C",
            r"Horizontal discs, $R = \sqrt y$.", why_not={"A": "discs about the $x$-axis"}),
    ),
    Variants(
        Item(r"The region under $y = \sec x$ for $0 \le x \le \frac\pi4$ is revolved about the $x$-axis. Find the volume.", num(sp.pi, tol=1e-3), r"$\pi\int_0^{\pi/4} \sec^2 x\,dx = \pi$.", work="1.4cm"),
        Item(r"The region under $y = \frac{1}{\sqrt x}$ for $1 \le x \le e$ is revolved about the $x$-axis. Find the volume.", num(sp.pi, tol=1e-3), r"$\pi\int_1^e \frac1x\,dx = \pi$.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"Revolving $y = \frac{r}{h}x$, $0 \le x \le h$, about the $x$-axis gives", [r"a cylinder", r"a cone of radius $h$ and height $r$", r"a ball", r"a cone of radius $r$ and height $h$"], "D", r"Radius grows linearly from $0$ to $r$ over length $h$."),
    ),
]

# ---------------------------------------------------------------- test prep
_m4 = float(disc(sp.sqrt(sp.log(x)), 1, 3))
close("m4", _m4, 4.071, 5e-3)
MCQS = [
    MCQ(r"The region under $y = x^{3/2}$ for $0 \le x \le 2$ is revolved about the $x$-axis. The volume is", [r"$2\pi$", r"$8\pi$", r"$4\pi$", r"$\frac{16\pi}{5}$"], "C", r"$\pi\int_0^2 x^3\,dx = 4\pi$."),
    MCQ(r"The region bounded by $y = \ln x$, the $y$-axis, $y = 0$ and $y = 1$ is revolved about the $y$-axis. The volume is", [r"$\frac\pi2\left(e^2 - 1\right)$", r"$\pi(e - 1)$", r"$\pi e^2$", r"$\frac\pi2 e^2$"], "A",
        r"$x = e^y$: $\pi\int_0^1 e^{2y}\,dy = \frac\pi2\left(e^2 - 1\right)$."),
    MCQ(r"Which integral gives the volume when the region under $y = \cos x$, $0 \le x \le \frac\pi2$, is revolved about the $x$-axis?", [r"$\pi\int_0^{\pi/2} \cos x\,dx$", r"$2\pi\int_0^{\pi/2} \cos x\,dx$",
        r"$\int_0^{\pi/2} \pi\cos x^2\,dx$", r"$\pi\int_0^{\pi/2} \cos^2 x\,dx$"], "D", r"$R = \cos x$, squared."),
    MCQ(r"The region under $y = \sqrt{\ln x}$ for $1 \le x \le 3$ is revolved about the $x$-axis. To three decimal places, the volume is", [r"$1.296$", rf"${_m4:.3f}$", r"$8.142$", r"$2.035$"], "B",
        rf"$\pi\int_1^3 \ln x\,dx \approx {_m4:.3f}$.", why_not={"A": "forgot the factor $\\pi$"}, calc=True),
]
same("m", [disc(x**sp.Rational(3, 2), 0, 2), disc(sp.exp(y), 0, 1, y)], [4 * sp.pi, sp.pi * (sp.E**2 - 1) / 2])

FRQS = []

TOPIC = Topic(
    number="8.9", title="Volume with Disc Method: Revolving Around the x- or y-Axis",
    unit="Unit 8: Applications of Integration", ced=["CHA-5.D", "CHA-5.D.1", "CHA-5.D.2"],
    goals=r"Find volumes of solids of revolution about the $x$- or $y$-axis with the disc method.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
