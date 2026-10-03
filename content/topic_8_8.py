"""Topic 8.8: Volumes with cross sections: triangles and semicircles.

CED: CHA-5.C (CHA-5.C.1): V = integral of A(x) dx with A from the side s = top - bottom: equilateral triangle
(sqrt 3/4) s^2; isosceles right triangle with a leg on the base s^2/2, with the hypotenuse on the base s^2/4; semicircle
with diameter on the base (pi/8) s^2. Lesson example: semicircles on y = 4 - x^2 (64 pi/15). Worked examples:
equilateral triangles on sqrt x (2 sqrt 3); hypotenuse on the disk x^2 + y^2 <= 4 (32/3); leg on the base between
2x and x^2 (8/15).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Table, Text, Topic, Variants, Video, close, num, same, selfcheck)
from calclib.figs import region

x, y = sp.symbols("x y", real=True)
EQ, LEG, HYP, SEMI = sp.sqrt(3) / 4, sp.Rational(1, 2), sp.Rational(1, 4), sp.pi / 8


def vol(k, s, a, b, v=x):
    return sp.simplify(k * sp.integrate(sp.expand(s**2), (v, a, b)))


same("lesson", [vol(SEMI, 4 - x**2, -2, 2)], [64 * sp.pi / 15])
same("ex", [vol(EQ, sp.sqrt(x), 0, 4), vol(HYP, 2 * sp.sqrt(4 - x**2), -2, 2), vol(LEG, 2 * x - x**2, 0, 2)], [2 * sp.sqrt(3), sp.Rational(32, 3), sp.Rational(8, 15)])

FIG_R = region("t8_8_r", [("sqrt(x)", 0, 4.4), ("x/2", 0, 4.4)], (-0.3, 4.6), (-0.3, 2.5), [(lambda v: v**0.5, lambda v: v / 2, 0, 4)],
               labels=[(2.2, 1.3, "center", "$R$")], caption=r"Region $R$, between $y = \sqrt x$ and $y = \frac x2$.")

NOTES = [
    Video("s8_8.py::Lesson", "Cross sections: triangles and semicircles", 5),

    Section("Areas in terms of the side on the base"),
    Text(r"The method is the same as for squares: $V = \int A(x)\,dx$ with $s(x) = \text{top} - \text{bottom}$ across the base. Only the area formula changes."),
    Table(r"square & $s^2$ \\ equilateral triangle & $\mblank{\frac{\sqrt3}{4}s^2}$ \\ isosceles right triangle, leg on the base & $\mblank{\frac12 s^2}$ \\ "
          r"isosceles right triangle, hypotenuse on the base & $\mblank{\frac14 s^2}$ \\ semicircle, diameter on the base & $\mblank{\frac\pi8 s^2}$ \\",
          "ll", header=r"Cross section (side $s$ on the base) & Area $A$"),
    Text(r"\textbf{Semicircles.} The side on the base is the \emph{diameter}, so $r = \frac s2$ and $A = \frac12\pi\left(\frac s2\right)^2 = \frac\pi8 s^2$."),
    Text(r"\textbf{Isosceles right triangles.} With a leg on the base, both legs are $s$. With the hypotenuse on the base, each leg is $\frac{s}{\sqrt2}$, so $A = \frac14 s^2$."),
    VideoExample('Semicircles on a parabola', work="4.6cm"),
    BigIdea(r"Find $s$ across the base, put it in the shape's area formula, and integrate. A semicircle's side on the base is its diameter."),
    Check(r"The base is the region under $y = 2$ for $0 \le x \le 5$; cross sections perpendicular to the $x$-axis are semicircles. Find the volume.", selfcheck(r"\tfrac{5\pi}{2}"),
          r"$\int_0^5 \frac\pi8 \cdot 4\,dx = \frac{5\pi}{2}$ (half a cylinder of radius $1$, length $5$)."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Base: under $y = x$ for $0 \le x \le 3$. Equilateral triangles perpendicular to the $x$-axis. Find the volume.", num(vol(EQ, x, 0, 3), tol=1e-3), r"$\frac{\sqrt3}{4}\int_0^3 x^2\,dx = \frac{9\sqrt3}{4} \approx 3.897$.", work="1.6cm"),
    Item(r"Base: under $y = \sqrt x$ for $0 \le x \le 4$. Semicircles perpendicular to the $x$-axis. Find the volume.", num(vol(SEMI, sp.sqrt(x), 0, 4), tol=1e-3), r"$\frac\pi8\int_0^4 x\,dx = \pi$.", work="1.6cm"),
    Item(r"Base: between $y = x$ and $y = x^2$. Semicircles perpendicular to the $x$-axis. Find the volume.", num(vol(SEMI, x - x**2, 0, 1), tol=1e-4), r"$\frac\pi8 \cdot \frac1{30} = \frac{\pi}{240}$.", work="1.8cm"),
    Item(r"Base: under $y = 2 - x$ for $0 \le x \le 2$. Isosceles right triangles with a leg on the base, perpendicular to the $x$-axis. Find the volume.", num(vol(LEG, 2 - x, 0, 2)), r"$\frac12\int_0^2 (2 - x)^2\,dx = \frac43$.", work="1.8cm"),
    Item(r"Base: the disk $x^2 + y^2 \le 9$. Squares perpendicular to the $x$-axis. Find the volume.", num(vol(1, 2 * sp.sqrt(9 - x**2), -3, 3)), r"$s = 2\sqrt{9 - x^2}$: $\int_{-3}^3 4(9 - x^2)\,dx = 144$.", work="2cm"),
    Item(r"Base: the disk $x^2 + y^2 \le 9$. Equilateral triangles perpendicular to the $x$-axis. Find the volume.", num(vol(EQ, 2 * sp.sqrt(9 - x**2), -3, 3), tol=1e-2), r"$\frac{\sqrt3}{4} \cdot 144 = 36\sqrt3 \approx 62.35$.", work="1.6cm"),
    Item(r"Base: under $y = \frac{1}{x}$ for $1 \le x \le 2$. Isosceles right triangles with the hypotenuse on the base. Find the volume.", num(vol(HYP, 1 / x, 1, 2)), r"$\frac14\int_1^2 x^{-2}\,dx = \frac18$.", work="1.6cm"),
    Item(r"Base: between $x = y^2$ and $x = 4$. Semicircles perpendicular to the $y$-axis. Find the volume.", num(vol(SEMI, 4 - y**2, -2, 2, y), tol=1e-3), r"$\frac\pi8 \cdot \frac{512}{15} = \frac{64\pi}{15}$.", work="1.8cm"),
    Item(r"Base: under $y = e^{-x}$ for $0 \le x \le \ln 2$. Equilateral triangles perpendicular to the $x$-axis. Find the volume.", num(vol(EQ, sp.exp(-x), 0, sp.log(2)), tol=1e-4),
         r"$\frac{\sqrt3}{4}\int_0^{\ln2} e^{-2x}\,dx = \frac{\sqrt3}{4} \cdot \frac38 = \frac{3\sqrt3}{32}$.", work="1.8cm"),
    Item(r"Base: region $R$ between $y = \sqrt x$ and $y = \frac x2$ (shown). Semicircles perpendicular to the $x$-axis. Find the volume.", num(vol(SEMI, sp.sqrt(x) - x / 2, 0, 4), tol=1e-4),
         r"$\frac\pi8\int_0^4 \left(\sqrt x - \frac x2\right)^2 dx = \frac\pi8 \cdot \frac{8}{15} = \frac{\pi}{15}$.", work="2cm", figure=FIG_R),
]

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"A cross section is a semicircle whose diameter, on the base, has length $s$. Its area is", [r"$\frac\pi2 s^2$", r"$\pi s^2$", r"$\frac\pi8 s^2$", r"$\frac\pi4 s^2$"], "C", r"$r = \frac s2$; $\frac12\pi r^2$.",
            why_not={"A": "used $r = s$"}),
        MCQ(r"A cross section is an equilateral triangle with side $s$ on the base. Its area is", [r"$\frac{\sqrt3}{4}s^2$", r"$\frac12 s^2$", r"$\frac{\sqrt3}{2}s^2$", r"$\frac{\sqrt3}{2}s$"], "A", r"Height $\frac{\sqrt3}{2}s$."),
        MCQ(r"A cross section is an isosceles right triangle with its hypotenuse, of length $s$, on the base. Its area is", [r"$\frac12 s^2$", r"$s^2$", r"$\frac{\sqrt2}{2}s^2$", r"$\frac14 s^2$"], "D", r"Legs $\frac{s}{\sqrt2}$."),
    ),
    Variants(
        Item(r"Base: under $y = 2\sqrt x$, $0 \le x \le 1$. Semicircles perpendicular to the $x$-axis. Find the volume.", num(vol(SEMI, 2 * sp.sqrt(x), 0, 1), tol=1e-3), r"$\frac\pi8\int_0^1 4x\,dx = \frac\pi4$.", work="1.4cm"),
        Item(r"Base: under $y = x$, $0 \le x \le 2$. Semicircles perpendicular to the $x$-axis. Find the volume.", num(vol(SEMI, x, 0, 2), tol=1e-3), r"$\frac\pi8 \cdot \frac83 = \frac\pi3$.", work="1.4cm"),
        Item(r"Base: under $y = 4$, $0 \le x \le 3$. Semicircles perpendicular to the $x$-axis. Find the volume.", num(vol(SEMI, 4, 0, 3), tol=1e-3), r"$\frac\pi8 \cdot 48 = 6\pi$.", work="1.4cm"),
    ),
    Variants(
        Item(r"Base: under $y = \sqrt x$, $0 \le x \le 6$. Equilateral triangles perpendicular to the $x$-axis. Find the volume.", num(vol(EQ, sp.sqrt(x), 0, 6), tol=1e-3), r"$\frac{\sqrt3}{4} \cdot 18 = \frac{9\sqrt3}{2}$.", work="1.4cm"),
        Item(r"Base: under $y = 3 - x$, $0 \le x \le 3$. Isosceles right triangles with a leg on the base. Find the volume.", num(vol(LEG, 3 - x, 0, 3)), r"$\frac12 \cdot 9 = \frac92$.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"Base: the region between $y = x^2$ and $y = 1$. Which gives the volume for semicircles perpendicular to the $x$-axis?", [r"$\frac\pi8\int_{-1}^1 \left(1 - x^2\right)^2 dx$", r"$\frac\pi2\int_{-1}^1 \left(1 - x^2\right)^2 dx$",
            r"$\pi\int_{-1}^1 \left(1 - x^2\right)^2 dx$", r"$\frac\pi8\int_{0}^1 \left(1 - x^2\right) dx$"], "A", r"$s = 1 - x^2$, $A = \frac\pi8 s^2$."),
        MCQ(r"Base: the region between $y = \sqrt x$ and the $x$-axis, $0 \le x \le 4$. Which gives the volume for equilateral triangles perpendicular to the $x$-axis?", [r"$\frac{\sqrt3}{2}\int_0^4 x\,dx$",
            r"$\frac{\sqrt3}{4}\int_0^4 \sqrt x\,dx$", r"$\frac{\sqrt3}{4}\int_0^4 x\,dx$", r"$\frac12\int_0^4 x\,dx$"], "C", r"$s^2 = x$."),
    ),
    Variants(
        Item(r"Base: the disk $x^2 + y^2 \le 1$. Isosceles right triangles with the hypotenuse on the base, perpendicular to the $x$-axis. Find the volume.", num(vol(HYP, 2 * sp.sqrt(1 - x**2), -1, 1)),
             r"$A = 1 - x^2$: $\frac43$.", work="1.6cm"),
        Item(r"Base: the disk $x^2 + y^2 \le 1$. Semicircles perpendicular to the $x$-axis. Find the volume.", num(vol(SEMI, 2 * sp.sqrt(1 - x**2), -1, 1), tol=1e-3), r"$\frac\pi8 \cdot 4 \cdot \frac43 = \frac{2\pi}{3}$ (a half ball).", work="1.6cm"),
    ),
]

# ---------------------------------------------------------------- test prep
_m4 = float(vol(SEMI, sp.exp(x / 2), 0, 2))
close("m4", _m4, 2.509, 5e-3)
MCQS = [
    MCQ(r"The base of a solid is the region under $y = \sqrt{x}$ for $0 \le x \le 2$. Cross sections perpendicular to the $x$-axis are equilateral triangles. The volume is", [r"$\frac{\sqrt3}{2}$", r"$\sqrt3$", r"$2\sqrt3$", r"$\frac{\sqrt3}{4}$"], "A",
        r"$\frac{\sqrt3}{4}\int_0^2 x\,dx = \frac{\sqrt3}{2}$."),
    MCQ(r"The base of a solid is the disk $x^2 + y^2 \le 4$. Cross sections perpendicular to the $x$-axis are semicircles. The volume is", [r"$\frac{8\pi}{3}$", r"$\frac{32\pi}{3}$", r"$\frac{16\pi}{3}$", r"$4\pi$"], "C",
        r"$s = 2\sqrt{4 - x^2}$: $\frac\pi8\int_{-2}^2 4(4 - x^2)\,dx = \frac\pi2 \cdot \frac{32}{3} = \frac{16\pi}{3}$, half a ball of radius $2$.", why_not={"B": "the whole ball"}),
    MCQ(r"The base of a solid is the region between $y = 1 - x$ and the axes. Cross sections perpendicular to the $x$-axis are isosceles right triangles with the hypotenuse on the base. The volume is", [r"$\frac16$", r"$\frac13$", r"$\frac14$", r"$\frac{1}{12}$"], "D",
        r"$\frac14\int_0^1 (1 - x)^2\,dx = \frac{1}{12}$.", why_not={"A": "used a leg on the base"}),
    MCQ(r"The base of a solid is the region under $y = e^{x/2}$ for $0 \le x \le 2$. Cross sections perpendicular to the $x$-axis are semicircles. To three decimal places, the volume is", [r"$1.254$", rf"${_m4:.3f}$", r"$5.018$", r"$10.036$"], "B",
        rf"$\frac\pi8\int_0^2 e^x\,dx = \frac\pi8(e^2 - 1) \approx {_m4:.3f}$.", calc=True),
]
same("m", [vol(EQ, sp.sqrt(x), 0, 2), vol(SEMI, 2 * sp.sqrt(4 - x**2), -2, 2), vol(HYP, 1 - x, 0, 1)], [sp.sqrt(3) / 2, 16 * sp.pi / 3, sp.Rational(1, 12)])

# ---------------------------------------------------------------- FRQ
same("frq", [sp.integrate(sp.sqrt(x) - x / 2, (x, 0, 4)), vol(1, sp.sqrt(x) - x / 2, 0, 4), vol(SEMI, sp.sqrt(x) - x / 2, 0, 4), vol(EQ, 2 * y - y**2, 0, 2, y)],
     [sp.Rational(4, 3), sp.Rational(8, 15), sp.pi / 15, 4 * sp.sqrt(3) / 15])
FRQS = [
    FRQ("A region and three solids", (r"Let $R$ be the region in the first quadrant bounded by the graphs of $y = \sqrt x$ and $y = \frac x2$, as shown."), [
        Part("a", r"Find the area of $R$.", num(sp.Rational(4, 3)), r"The curves meet at $x = 0$ and $x = 4$. $\int_0^4 \left(\sqrt x - \frac x2\right) dx = \frac{16}{3} - 4 = \frac43$.", [(1, "limits"), (1, "integral and answer")], work="2.4cm"),
        Part("b", r"$R$ is the base of a solid whose cross sections perpendicular to the $x$-axis are squares. Find the volume of the solid.", num(sp.Rational(8, 15)),
             r"$\int_0^4 \left(\sqrt x - \frac x2\right)^2 dx = \int_0^4 \left(x - x^{3/2} + \frac{x^2}{4}\right) dx = 8 - \frac{64}{5} + \frac{16}{3} = \frac{8}{15}$.", [(1, "integrand"), (1, "answer")], work="2.6cm"),
        Part("c", r"$R$ is the base of a solid whose cross sections perpendicular to the $x$-axis are semicircles. Find the volume of the solid.", num(sp.pi / 15, tol=1e-4, display=r"\tfrac{\pi}{15}"),
             r"$\frac\pi8\int_0^4 \left(\sqrt x - \frac x2\right)^2 dx = \frac\pi8 \cdot \frac{8}{15} = \frac{\pi}{15}$.", [(1, "semicircle area with $r = \\frac s2$"), (1, "answer")], work="2cm"),
        Part("d", r"$R$ is the base of a solid whose cross sections perpendicular to the $y$-axis are equilateral triangles. Write, but do not evaluate, an integral expression for the volume of the solid.",
             selfcheck(r"\frac{\sqrt3}{4}\int_0^2 \left(2y - y^2\right)^2 dy"),
             r"In terms of $y$: the left boundary is $x = y^2$ and the right is $x = 2y$, for $0 \le y \le 2$. $V = \frac{\sqrt3}{4}\int_0^2 \left(2y - y^2\right)^2 dy$.",
             [(1, "boundaries in $y$"), (1, "integrand and limits")], work="2.2cm"),
    ], frq_type="Area and volume", figure=FIG_R),
]

TOPIC = Topic(
    number="8.8", title="Volumes with Cross Sections: Triangles and Semicircles",
    unit="Unit 8: Applications of Integration", ced=["CHA-5.C", "CHA-5.C.1"],
    goals=r"Find volumes of solids whose cross sections are triangles or semicircles standing on a base region.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
