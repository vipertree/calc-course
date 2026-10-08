"""Topic 9.9 (BC): Finding the area of the region bounded by two polar curves.

CED: CHA-5.D (CHA-5.D.10): A = (1/2) integral of (R^2 - r^2) dtheta with R the outer and r the inner curve; limits where
the curves intersect; square each radius separately; split when the boundary changes. Lesson example: inside
r = 3 cos theta, outside r = 1 + cos theta (pi). Worked examples: inside r = 2 sin theta outside r = 1 (pi/3 + sqrt3/2);
inside both r = 1 and r = 2 cos theta (2 pi/3 - sqrt3/2); inside r = 2 + 2 sin theta outside r = 3 (4.653).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)
from calclib.figs import graph

th = sp.symbols("theta", real=True)


def between(R, r, a, b):
    return sp.simplify(sp.integrate(R**2 - r**2, (th, a, b)) / 2)


same("lesson", [between(3 * sp.cos(th), 1 + sp.cos(th), -sp.pi / 3, sp.pi / 3)], [sp.pi])
same("ex", [between(2 * sp.sin(th), 1, sp.pi / 6, 5 * sp.pi / 6), sp.simplify(sp.pi / 3 + sp.integrate(4 * sp.cos(th)**2, (th, sp.pi / 3, sp.pi / 2))), between(2 + 2 * sp.sin(th), 3, sp.pi / 6, 5 * sp.pi / 6)],
     [sp.pi / 3 + sp.sqrt(3) / 2, 2 * sp.pi / 3 - sp.sqrt(3) / 2, 9 * sp.sqrt(3) / 2 - sp.pi])

FIG = graph("t9_9_two", [], (-0.6, 3.4), (-2, 2), w="5cm", h="5cm",
            extra=r"\addplot[fn, domain=-90:90, samples=200, variable=\t]({3*cos(\t)*cos(\t)},{3*cos(\t)*sin(\t)});\addplot[fn2, domain=0:360, samples=200, variable=\t]({(1+cos(\t))*cos(\t)},{(1+cos(\t))*sin(\t)});",
            caption=r"$r = 3\cos\theta$ (solid) and $r = 1 + \cos\theta$ (dashed) meet at $\theta = \pm\frac\pi3$.")
FIG_FRQ = graph("t9_9_frq", [], (-1, 4.5), (-3.2, 3.2), w="5.4cm", h="5.4cm",
                extra=r"\addplot[fn, domain=0:360, samples=200, variable=\t]({(2+2*cos(\t))*cos(\t)},{(2+2*cos(\t))*sin(\t)});\addplot[fn2, domain=0:360, samples=200, variable=\t]({3*cos(\t)},{3*sin(\t)});",
                caption=r"$r = 2 + 2\cos\theta$ (solid) and the circle $r = 3$ (dashed).")

NOTES = [
    Video("s9_9.py::Lesson", "Area between polar curves", 5),

    Section("Outer squared minus inner squared"),
    Text(r"A thin wedge of the region between two curves is a big sector (radius $R$) minus a small one (radius $r$): area $\frac12\left(R^2 - r^2\right)\Delta\theta$."),
    Formula("Area between polar curves", (r"\[ A = \blank{\frac12\int_\alpha^\beta \left(R^2 - r^2\right) d\theta}, \] with $R$ the outer curve and $r$ the inner one (measured from the origin). Square each radius separately: $(R - r)^2 \ne R^2 - r^2$.")),
    Text(r"\textbf{Limits.} Set the two $r$'s equal to find where the curves cross. If the outer or inner curve changes partway, split the integral."),
    FIG,
    VideoExample('Inside the circle, outside the cardioid', work="5cm"),
    BigIdea(r"$A = \frac12\int (R^2 - r^2)\,d\theta$: intersections for limits, squares taken separately, split where the boundary changes."),
    Check(r"Find the area between the circles $r = 2$ and $r = 3$.", selfcheck(r"5\pi"), r"$\frac12\int_0^{2\pi} (9 - 4)\,d\theta$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Find the area inside $r = 4$ and outside $r = 2$.", num(between(4, 2, 0, 2 * sp.pi), tol=1e-3), r"$\frac12\int_0^{2\pi} 12\,d\theta = 12\pi$.", work="1.2cm"),
    Item(r"Find where $r = 1 + \sin\theta$ and $r = 3\sin\theta$ intersect, for $0 \le \theta \le \pi$.", selfcheck(r"\theta = \tfrac\pi6,\ \tfrac{5\pi}{6}"), r"$1 + \sin\theta = 3\sin\theta$: $\sin\theta = \frac12$.", work="1.2cm"),
    Item(r"Find the area inside $r = 3\sin\theta$ and outside $r = 1 + \sin\theta$.", num(between(3 * sp.sin(th), 1 + sp.sin(th), sp.pi / 6, 5 * sp.pi / 6), tol=1e-3), r"$\frac12\int_{\pi/6}^{5\pi/6} \left(8\sin^2\theta - 2\sin\theta - 1\right) d\theta = \pi$.", work="2.4cm"),
    Item(r"Find the area inside $r = 2\cos\theta$ and outside $r = 1$.", num(between(2 * sp.cos(th), 1, -sp.pi / 3, sp.pi / 3), tol=1e-3), r"$\theta = \pm\frac\pi3$: $\frac12\int (4\cos^2\theta - 1)\,d\theta = \frac\pi3 + \frac{\sqrt3}{2}$.", work="2.2cm"),
    Item(r"Write, but do not evaluate, the area inside $r = 2$ and outside $r = 2 - 2\cos\theta$.", selfcheck(r"\tfrac12\int_{-\pi/2}^{\pi/2} \left(4 - (2 - 2\cos\theta)^2\right) d\theta"), r"They meet where $\cos\theta = 0$; $r = 2$ is outer for $|\theta| < \frac\pi2$.", work="1.6cm"),
    Item(r"Use a calculator: area inside $r = 3 + 2\sin\theta$ and outside $r = 2$.", num(between(3 + 2 * sp.sin(th), 2, -sp.pi / 6, 7 * sp.pi / 6), tol=2e-3),
         r"They meet where $\sin\theta = -\frac12$: $-\frac\pi6$ and $\frac{7\pi}{6}$. $\frac12\int_{-\pi/6}^{7\pi/6} \left((3 + 2\sin\theta)^2 - 4\right) d\theta \approx 24.187$.", work="2cm", calc=True),
]
close("p6", float(between(3 + 2 * sp.sin(th), 2, -sp.pi / 6, 7 * sp.pi / 6)), 24.187, 5e-3)
same("p3", [between(3 * sp.sin(th), 1 + sp.sin(th), sp.pi / 6, 5 * sp.pi / 6), between(2 * sp.cos(th), 1, -sp.pi / 3, sp.pi / 3)], [sp.pi, sp.pi / 3 + sp.sqrt(3) / 2])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"The area inside $r = R(\theta)$ and outside $r = r(\theta)$ for $\alpha \le \theta \le \beta$ (with $R \ge r \ge 0$) is", [r"$\frac12\int_\alpha^\beta (R - r)^2\,d\theta$", r"$\int_\alpha^\beta (R - r)\,d\theta$",
            r"$\frac12\int_\alpha^\beta \left(R^2 - r^2\right) d\theta$", r"$\pi\int_\alpha^\beta \left(R^2 - r^2\right) d\theta$"], "C", r"Big sector minus small sector.", why_not={"A": "squared the difference"}),
    ),
    Variants(
        Item(r"Find the area inside $r = 5$ and outside $r = 3$.", num(16 * sp.pi, tol=1e-3), r"$\frac12 \cdot 2\pi(25 - 9) = 16\pi$.", work="1.2cm"),
        Item(r"Find the area inside $r = 3$ and outside $r = 1$.", num(8 * sp.pi, tol=1e-3), r"$8\pi$.", work="1.2cm"),
    ),
    Variants(
        Item(r"Find the values of $\theta$ in $[0, 2\pi)$ where $r = 1$ and $r = 2\cos\theta$ intersect.", selfcheck(r"\tfrac\pi3,\ \tfrac{5\pi}{3}"), r"$\cos\theta = \frac12$.", work="1cm"),
        Item(r"Find the values of $\theta$ in $[0, 2\pi)$ where $r = 3$ and $r = 2 + 2\cos\theta$ intersect.", selfcheck(r"\tfrac\pi3,\ \tfrac{5\pi}{3}"), r"$\cos\theta = \frac12$.", work="1cm"),
    ),
    Variants(
        Item(r"Find the area inside $r = 2\sin\theta$ and outside $r = 1$.", num(between(2 * sp.sin(th), 1, sp.pi / 6, 5 * sp.pi / 6), tol=1e-3), r"$\frac\pi3 + \frac{\sqrt3}{2} \approx 1.913$.", work="2cm"),
        Item(r"Find the area inside $r = 4\cos\theta$ and outside $r = 2$.", num(between(4 * sp.cos(th), 2, -sp.pi / 3, sp.pi / 3), tol=1e-3), r"$\frac12\int_{-\pi/3}^{\pi/3} (16\cos^2\theta - 4)\,d\theta = \frac{4\pi}{3} + 2\sqrt3$.", work="2cm"),
    ),
    Variants(
        MCQ(r"Which integral gives the area inside $r = 2$ and outside $r = 2 - 2\sin\theta$?", [r"$\frac12\int_0^\pi \left(4 - (2 - 2\sin\theta)^2\right) d\theta$", r"$\frac12\int_0^{2\pi} \left(4 - (2 - 2\sin\theta)^2\right) d\theta$",
            r"$\frac12\int_0^\pi (2\sin\theta)^2\,d\theta$", r"$\int_0^\pi \left(4 - (2 - 2\sin\theta)^2\right) d\theta$"], "A", r"They meet at $0$ and $\pi$; $r = 2$ is outer for $0 < \theta < \pi$."),
    ),
]

# ---------------------------------------------------------------- test prep
_m4 = float(between(2 + sp.cos(th), 2, -sp.pi / 2, sp.pi / 2))
MCQS = [
    MCQ(r"The area inside $r = 6\cos\theta$ and outside $r = 3$ is", [r"$3\pi + \frac{9\sqrt3}{2}$", r"$9\pi$", r"$6\pi$", r"$3\pi$"], "A", r"$\theta = \pm\frac\pi3$: $\frac12\int_{-\pi/3}^{\pi/3} (36\cos^2\theta - 9)\,d\theta = 3\pi + \frac{9\sqrt3}{2}$."),
    MCQ(r"The curves $r = 1 + \cos\theta$ and $r = 1 - \cos\theta$ intersect at", [r"$\theta = 0$ only", r"$\theta = \pi$ only", r"$\theta = \frac\pi2$ and $\frac{3\pi}{2}$ (and the origin)", r"$\theta = \frac\pi4$"], "C", r"$\cos\theta = 0$; both also pass through the pole."),
    MCQ(r"Which gives the area of the region inside both $r = 1$ and $r = 1 + \cos\theta$ for $\frac\pi2 \le \theta \le \frac{3\pi}{2}$?", [r"$\frac12\int_{\pi/2}^{3\pi/2} 1\,d\theta$",
        r"$\frac12\int_{\pi/2}^{3\pi/2} \left(1 - (1 + \cos\theta)^2\right) d\theta$", r"$\frac12\int_{\pi/2}^{3\pi/2} \cos^2\theta\,d\theta$", r"$\frac12\int_{\pi/2}^{3\pi/2} (1 + \cos\theta)^2\,d\theta$"], "D",
        r"There $1 + \cos\theta \le 1$, so the cardioid is the boundary."),
    MCQ(r"To three decimal places, the area inside $r = 2 + \cos\theta$ and outside $r = 2$ is", [rf"${_m4:.3f}$", r"$3.142$", r"$9.571$", r"$2.000$"], "A", rf"$\frac12\int_{{-\pi/2}}^{{\pi/2}} \left((2 + \cos\theta)^2 - 4\right) d\theta \approx {_m4:.3f}$.", why_not={"C": "forgot the $\\frac12$"}, calc=True),
]
same("m", [between(6 * sp.cos(th), 3, -sp.pi / 3, sp.pi / 3)], [3 * sp.pi + 9 * sp.sqrt(3) / 2])
close("m4", _m4, float(4 + sp.pi / 4), 1e-9)

# ---------------------------------------------------------------- FRQ
rF = 2 + 2 * sp.cos(th)
_aF = float(between(rF, 3, -sp.pi / 3, sp.pi / 3))
xF, yF = rF * sp.cos(th), rF * sp.sin(th)
same("frq", [sp.diff(rF, th).subs(th, sp.pi / 2), sp.simplify((sp.diff(yF, th) / sp.diff(xF, th)).subs(th, sp.pi / 2)), sp.diff(rF, th).subs(th, sp.pi / 3) * 3],
     [-2, 1, -3 * sp.sqrt(3)])
close("frq a", _aF, float(9 * sp.sqrt(3) / 2 - sp.pi), 1e-9)
FRQS = [
    FRQ("Two polar curves", (r"The graphs of the polar curves $r = 3$ and $r = 2 + 2\cos\theta$ are shown. They intersect at $\theta = \frac\pi3$ and $\theta = -\frac\pi3$."), [
        Part("a", r"Let $R$ be the region inside the graph of $r = 2 + 2\cos\theta$ and outside the graph of $r = 3$. Find the area of $R$.", num(9 * sp.sqrt(3) / 2 - sp.pi, tol=1e-3, display=r"\tfrac{9\sqrt3}{2} - \pi"),
             r"$\frac12\int_{-\pi/3}^{\pi/3} \left((2 + 2\cos\theta)^2 - 9\right) d\theta = \frac{9\sqrt3}{2} - \pi \approx 4.653$.", [(1, "limits and constant"), (1, "integrand"), (1, "answer")], work="3cm"),
        Part("b", r"For the curve $r = 2 + 2\cos\theta$, find $\frac{dr}{d\theta}$ at $\theta = \frac\pi2$. Is the curve moving toward or away from the origin there?", selfcheck(r"-2;\ \text{toward}"),
             r"$\frac{dr}{d\theta} = -2\sin\theta = -2$. Since $r = 2 > 0$ and $r$ is decreasing, the curve is moving toward the origin.", [(1, "$\\frac{dr}{d\\theta}$"), (1, "toward, with reason")], work="1.8cm"),
        Part("c", r"Find the slope of the line tangent to $r = 2 + 2\cos\theta$ at $\theta = \frac\pi2$.", num(1),
             r"$x = (2 + 2\cos\theta)\cos\theta$, $y = (2 + 2\cos\theta)\sin\theta$. At $\frac\pi2$: $\frac{dx}{d\theta} = -2\sin\theta\cos\theta - (2 + 2\cos\theta)\sin\theta = -2$ and $\frac{dy}{d\theta} = -2\sin^2\theta + (2 + 2\cos\theta)\cos\theta = -2$. Slope $1$.",
             [(1, "$\\frac{dx}{d\\theta}$ and $\\frac{dy}{d\\theta}$"), (1, "slope")], work="2.6cm"),
        Part("d", r"A particle moves along $r = 2 + 2\cos\theta$ so that $\frac{d\theta}{dt} = 3$ for all $t$. Find $\frac{dr}{dt}$ when $\theta = \frac\pi3$.", num(-3 * sp.sqrt(3), tol=1e-3, display=r"-3\sqrt3"),
             r"$\frac{dr}{dt} = \frac{dr}{d\theta}\cdot\frac{d\theta}{dt} = -2\sin\frac\pi3 \cdot 3 = -3\sqrt3$.", [(1, "chain rule"), (1, "answer")], work="1.8cm"),
    ], frq_type="Polar", figure=FIG_FRQ),
]

TOPIC = Topic(
    number="9.9", title="Finding the Area of the Region Bounded by Two Polar Curves",
    unit="Unit 9: Parametric Equations, Polar Coordinates, and Vector-Valued Functions", ced=["CHA-5.D", "CHA-5.D.10"],
    goals=r"Find areas between polar curves with $\frac12\int (R^2 - r^2)\,d\theta$, using intersections for the limits.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
