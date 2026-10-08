"""Topic 8.7: Volumes with cross sections: squares and rectangles.

CED: CHA-5.C (CHA-5.C.1): the volume of a solid with known cross sections of area A(x) perpendicular to the x-axis is
the integral of A(x) dx (or A(y) dy for cross sections perpendicular to the y-axis). The side of a cross section is
top - bottom across the base. Lesson example: squares on y = sqrt x, 0 <= x <= 4 (8). Worked examples: squares between
y = x and y = x^2 (1/30); rectangles of height 3 on y = 4 - x^2 (32); squares perpendicular to the y-axis between
x = y^2 and x = 4 (512/15).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)
from calclib.figs import region

x, y = sp.symbols("x y", real=True)


def vol(A, a, b, v=x):
    return sp.simplify(sp.integrate(sp.expand(A), (v, a, b)))


same("lesson", [vol(x, 0, 4)], [8])
same("ex", [vol((x - x**2)**2, 0, 1), vol(3 * (4 - x**2), -2, 2), vol((4 - y**2)**2, -2, 2, y)], [sp.Rational(1, 30), 32, sp.Rational(512, 15)])

FIG_BASE = region("t8_7_base", [("sqrt(x)", 0, 4.4)], (-0.3, 4.6), (-0.3, 2.4), [(lambda v: v**0.5, lambda v: 0, 0, 4)], vlines=[4],
                  caption=r"The base: the region under $y = \sqrt x$ for $0 \le x \le 4$. Each cross section stands on a vertical segment of length $\sqrt x$.")
FIG_Q = region("t8_7_q", [("2-x/2", -0.3, 4.3)], (-0.3, 4.5), (-0.3, 2.4), [(lambda v: 2 - v / 2, lambda v: 0, 0, 4)], caption=r"The triangle bounded by $y = 2 - \frac x2$ and the axes.")

NOTES = [
    Video("s8_7.py::Lesson", "Cross sections: squares and rectangles", 5),

    Section("Volume is the integral of area"),
    Text(r"A thin slice of a solid is almost a slab: volume $\approx$ (area of its face) $\times$ (thickness). Adding the slices and letting them get thin gives an integral."),
    Formula("Volume by cross sections", (r"If the cross section perpendicular to the $x$-axis at $x$ has area $A(x)$, \[ V = \blank{\int_a^b A(x)\,dx}. \] "
                                          r"For cross sections perpendicular to the $y$-axis, $V = \int_c^d A(y)\,dy$.")),
    Section("Squares and rectangles on a base"),
    Text(r"The base region lies flat. At each $x$, the segment across the base runs from the bottom curve to the top curve: that segment is a side of the cross section, $s(x) = \text{top} - \text{bottom}$."),
    FIG_BASE,
    Formula("Areas to know", (r"Square with side $s$: $A = \blank{s^2}$. Rectangle with base $s$ and height $h$: $A = \blank{sh}$ (the height is given: a number, or a multiple of $s$).")),
    VideoExample('Squares on a root', work="3cm"),
    BigIdea(r"$V = \int A(x)\,dx$. The side of each cross section is top $-$ bottom across the base; square it for squares, multiply by the height for rectangles."),
    Check(r"The base is the region under $y = 2$ for $0 \le x \le 3$; cross sections perpendicular to the $x$-axis are squares. Find the volume.", selfcheck(r"12"), r"$\int_0^3 4\,dx$: a $3 \times 2 \times 2$ box."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"The base is the region under $y = x$ for $0 \le x \le 3$. Cross sections perpendicular to the $x$-axis are squares. Find the volume.", num(vol(x**2, 0, 3)), r"$\int_0^3 x^2\,dx = 9$.", work="1.6cm"),
    Item(r"The base is the region between $y = 1 - x^2$ and the $x$-axis. Cross sections perpendicular to the $x$-axis are squares. Find the volume.", num(vol((1 - x**2)**2, -1, 1)),
         r"$\int_{-1}^1 (1 - x^2)^2\,dx = \frac{16}{15}$.", work="2cm"),
    Item(r"The base is the triangle shown. Cross sections perpendicular to the $x$-axis are squares. Find the volume.", num(vol((2 - x / 2)**2, 0, 4)), r"$\int_0^4 \left(2 - \frac x2\right)^2 dx = \frac{16}{3}$.", work="2cm", figure=FIG_Q),
    Item(r"The base is the region under $y = e^x$ for $0 \le x \le 1$. Cross sections perpendicular to the $x$-axis are squares. Find the volume.", num(vol(sp.exp(2 * x), 0, 1), tol=1e-3),
         r"$\int_0^1 e^{2x}\,dx = \frac{e^2 - 1}{2} \approx 3.195$.", work="1.6cm"),
    Item(r"The base is the region between $y = \sqrt x$ and $y = x$. Cross sections perpendicular to the $x$-axis are squares. Find the volume.", num(vol((sp.sqrt(x) - x)**2, 0, 1)),
         r"$\int_0^1 \left(x - 2x^{3/2} + x^2\right) dx = \frac12 - \frac45 + \frac13 = \frac{1}{30}$.", work="2.2cm"),
    Item(r"The base is the region under $y = 2\sqrt x$ for $0 \le x \le 4$. Cross sections perpendicular to the $x$-axis are rectangles of height $5$. Find the volume.", num(vol(5 * 2 * sp.sqrt(x), 0, 4)),
         r"$\int_0^4 10\sqrt x\,dx = \frac{160}{3}$.", work="1.8cm"),
    Item(r"The base is the region between $y = 4 - x^2$ and the $x$-axis. Cross sections perpendicular to the $x$-axis are rectangles whose height is half the base. Find the volume.",
         num(vol(sp.Rational(1, 2) * (4 - x**2)**2, -2, 2)), r"$A = \frac12(4 - x^2)^2$; $V = \frac12 \cdot \frac{512}{15} = \frac{256}{15}$.", work="2cm"),
    Item(r"The base is the region between $x = y^2$ and $x = 1$. Cross sections perpendicular to the $y$-axis are squares. Find the volume.", num(vol((1 - y**2)**2, -1, 1, y)),
         r"$\int_{-1}^1 (1 - y^2)^2\,dy = \frac{16}{15}$.", work="2cm"),
    Item(r"The base is the region under $y = \sin x$ for $0 \le x \le \pi$. Cross sections perpendicular to the $x$-axis are squares. Find the volume.", num(sp.pi / 2, tol=1e-3),
         r"$\int_0^\pi \sin^2 x\,dx = \frac\pi2$.", work="1.6cm"),
    Item(r"The base is the region under $y = \frac1x$ for $1 \le x \le 3$. Cross sections perpendicular to the $x$-axis are squares. Find the volume.", num(vol(1 / x**2, 1, 3)), r"$\int_1^3 x^{-2}\,dx = \frac23$.", work="1.6cm"),
]
same("p", [vol(sp.sin(x)**2, 0, sp.pi)], [sp.pi / 2])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Base: under $y = \sqrt x$, $0 \le x \le 9$. Square cross sections perpendicular to the $x$-axis. Find the volume.", num(vol(x, 0, 9)), r"$\int_0^9 x\,dx = \frac{81}{2}$.", work="1.4cm"),
        Item(r"Base: under $y = 2x$, $0 \le x \le 2$. Square cross sections perpendicular to the $x$-axis. Find the volume.", num(vol(4 * x**2, 0, 2)), r"$\int_0^2 4x^2\,dx = \frac{32}{3}$.", work="1.4cm"),
        Item(r"Base: under $y = x^2$, $0 \le x \le 1$. Square cross sections perpendicular to the $x$-axis. Find the volume.", num(vol(x**4, 0, 1)), r"$\frac15$.", work="1.4cm"),
    ),
    Variants(
        Item(r"Base: between $y = x$ and $y = x^2$. Rectangles of height $6$ perpendicular to the $x$-axis. Find the volume.", num(vol(6 * (x - x**2), 0, 1)), r"$6 \cdot \frac16 = 1$.", work="1.6cm"),
        Item(r"Base: under $y = 9 - x^2$, $-3 \le x \le 3$. Rectangles of height $2$ perpendicular to the $x$-axis. Find the volume.", num(vol(2 * (9 - x**2), -3, 3)), r"$2 \cdot 36 = 72$.", work="1.6cm"),
        Item(r"Base: under $y = \cos x$, $-\frac\pi2 \le x \le \frac\pi2$. Rectangles of height $4$ perpendicular to the $x$-axis. Find the volume.", num(8), r"$4 \cdot 2 = 8$.", work="1.6cm"),
    ),
    Variants(
        MCQ(r"The base is the region between $y = 2x$ and $y = x^2$. Which gives the volume if cross sections perpendicular to the $x$-axis are squares?",
            [r"$\int_0^2 \left(4x^2 - x^4\right) dx$", r"$\int_0^2 \left(2x - x^2\right) dx$", r"$\int_0^2 \left(2x - x^2\right)^2 dx$", r"$\int_0^4 \left(2x - x^2\right)^2 dx$"], "C", r"Side $2x - x^2$, squared.",
            why_not={"A": "squared each curve instead of the side"}),
        MCQ(r"The base is the region between $y = 3$ and $y = x^2 - 1$. Which gives the volume if cross sections perpendicular to the $x$-axis are squares?",
            [r"$\int_{-2}^{2} \left(4 - x^2\right)^2 dx$", r"$\int_{-2}^{2} \left(9 - (x^2 - 1)^2\right) dx$", r"$\int_{0}^{2} \left(4 - x^2\right)^2 dx$", r"$\int_{-2}^{2} \left(4 - x^2\right) dx$"], "A", r"Side $3 - (x^2 - 1) = 4 - x^2$.",
            why_not={"B": "squared each curve instead of the side"}),
    ),
    Variants(
        Item(r"Base: between $x = y^2$ and $x = 4$. Rectangles of height $1$ perpendicular to the $y$-axis. Find the volume.", num(vol(4 - y**2, -2, 2, y)), r"$\int_{-2}^2 (4 - y^2)\,dy = \frac{32}{3}$.", work="1.6cm"),
        Item(r"Base: between $x = 0$ and $x = 2 - y$, $0 \le y \le 2$. Squares perpendicular to the $y$-axis. Find the volume.", num(vol((2 - y)**2, 0, 2, y)), r"$\frac83$.", work="1.6cm"),
    ),
    Variants(
        MCQ(r"A solid's cross sections perpendicular to the $x$-axis have area $A(x) = 3x^2$ for $0 \le x \le 2$. Its volume is", [r"$8$", r"$12$", r"$24$", r"$4$"], "A", r"$\int_0^2 3x^2\,dx = 8$."),
        MCQ(r"A solid's cross sections perpendicular to the $x$-axis have area $A(x) = 6\sqrt x$ for $0 \le x \le 4$. Its volume is", [r"$16$", r"$48$", r"$32$", r"$12$"], "C", r"$\left[4x^{3/2}\right]_0^4 = 32$."),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"The base of a solid is the region between $y = x^2$ and $y = 4$. Cross sections perpendicular to the $y$-axis are squares. The volume is", [r"$16$", r"$32$", r"$8$", r"$\frac{64}{3}$"], "B",
        r"At height $y$ the side is $2\sqrt y$: $\int_0^4 4y\,dy = 32$.", why_not={"C": "used side $\\sqrt y$ (half the width)"}),
    MCQ(r"The base of a solid is the region under $y = \frac{2}{\sqrt x}$ for $1 \le x \le e$. Cross sections perpendicular to the $x$-axis are squares. The volume is", [r"$2$", r"$e$", r"$4(e - 1)$", r"$4$"], "D",
        r"$\int_1^e \frac4x\,dx = 4$."),
    MCQ(r"A solid's base is the region between $y = x$ and the $x$-axis for $0 \le x \le 6$. Cross sections perpendicular to the $x$-axis are rectangles of height $2$. The volume is", [r"$36$", r"$72$", r"$18$", r"$12$"], "A",
        r"$\int_0^6 2x\,dx = 36$."),
    MCQ(r"The base of a solid is the region under $y = \sqrt{\cos x}$ for $-\frac\pi2 \le x \le \frac\pi2$. Cross sections perpendicular to the $x$-axis are squares. To three decimal places, the volume is", [r"$1.000$", r"$1.571$", r"$2.000$", r"$3.142$"], "C",
        r"$\int_{-\pi/2}^{\pi/2} \cos x\,dx = 2$.", calc=True),
]
same("m", [vol(4 * y, 0, 4, y), vol(4 / x, 1, sp.E), vol(2 * x, 0, 6), vol(sp.cos(x), -sp.pi / 2, sp.pi / 2)], [32, 4, 36, 2])

FRQS = []

TOPIC = Topic(
    number="8.7", title="Volumes with Cross Sections: Squares and Rectangles",
    unit="Unit 8: Applications of Integration", ced=["CHA-5.C", "CHA-5.C.1"],
    goals=r"Find the volume of a solid with square or rectangular cross sections by integrating the cross-sectional area.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
