"""Topic 9.7 (BC): Defining polar coordinates and differentiating in polar form.

CED: CHA-3.I (CHA-3.I.1, CHA-3.I.2): x = r cos theta, y = r sin theta, r^2 = x^2 + y^2; r = f(theta) is parametric in theta,
so dy/dx = (dy/dtheta)/(dx/dtheta) with dx/dtheta = f' cos - f sin, dy/dtheta = f' sin + f cos; dr/dtheta > 0 (r > 0)
means moving away from the origin. Lesson example: r = 1 + cos theta at pi/2: slope 1, tangent y - 1 = x. Worked
examples: r = 4 sin theta is x^2 + (y - 2)^2 = 4; spiral r = theta at pi/2 (slope -2/pi); r = 1 + 2 sin theta at pi/3
(moving away).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)
from calclib.figs import graph

th = sp.symbols("theta", real=True)


def pslope(f):
    x, y = f * sp.cos(th), f * sp.sin(th)
    return sp.simplify(sp.diff(y, th) / sp.diff(x, th))


same("lesson", [pslope(1 + sp.cos(th)).subs(th, sp.pi / 2), (1 + sp.cos(th)).subs(th, sp.pi / 2)], [1, 1])
same("ex", [sp.simplify(pslope(th).subs(th, sp.pi / 2)), sp.diff(1 + 2 * sp.sin(th), th).subs(th, sp.pi / 3)], [-2 / sp.pi, 1])

FIG = graph("t9_7_card", [], (-0.8, 2.4), (-1.6, 1.6), extra=r"\addplot[fn, domain=0:360, samples=200, variable=\t]({(1+cos(\t))*cos(\t)},{(1+cos(\t))*sin(\t)});",
            caption=r"The cardioid $r = 1 + \cos\theta$.")

NOTES = [
    Video("s9_7.py::Lesson", "Polar coordinates", 6),

    Section("Polar coordinates"),
    Formula("Conversions", (r"\[ x = \blank{r\cos\theta}, \quad y = \blank{r\sin\theta}, \quad r^2 = x^2 + y^2, \quad \tan\theta = \frac yx. \]")),
    Text(r"A polar curve gives $r$ as a function of $\theta$; as $\theta$ sweeps around, the distance from the origin changes. $r = 2$ is a circle, $r = \theta$ a spiral, $r = 1 + \cos\theta$ a cardioid."),
    FIG,
    Section("Slopes"),
    Formula("Slope of a polar curve", (r"With $x = f(\theta)\cos\theta$ and $y = f(\theta)\sin\theta$, \[ \frac{dy}{dx} = \blank{\frac{dy/d\theta}{dx/d\theta}} = \frac{f'(\theta)\sin\theta + f(\theta)\cos\theta}{f'(\theta)\cos\theta - f(\theta)\sin\theta}. \] "
                                      r"The slope is \emph{not} $\frac{dr}{d\theta}$.")),
    VideoExample("The cardioid's tangent line", work="4.6cm"),
    Formula("What $\\frac{dr}{d\\theta}$ means", (r"When $r > 0$: \blank{$\frac{dr}{d\theta} > 0$} means the curve is moving away from the origin; $\frac{dr}{d\theta} < 0$ means it is moving toward the origin.")),
    BigIdea(r"A polar curve is parametric in $\theta$: slope $= \frac{dy/d\theta}{dx/d\theta}$, with the product rule. $\frac{dr}{d\theta}$ says toward or away from the origin."),
    Check(r"Convert $(r, \theta) = \left(4, \frac\pi6\right)$ to rectangular coordinates.", selfcheck(r"\left(2\sqrt3,\ 2\right)"), r"$4\cos\frac\pi6$, $4\sin\frac\pi6$."),
]

# ---------------------------------------------------------------- practice
def dxy(f, a):
    x, y = f * sp.cos(th), f * sp.sin(th)
    return sp.simplify(sp.diff(x, th).subs(th, a)), sp.simplify(sp.diff(y, th).subs(th, a))


same("p", [dxy(2 * sp.sin(th), sp.pi / 4), pslope(2 + sp.cos(th)).subs(th, sp.pi / 2), sp.simplify(pslope(3 * sp.cos(th)).subs(th, sp.pi / 6))], [(0, 2), sp.Rational(1, 2), -sp.sqrt(3) / 3])
PRACTICE = [
    Item(r"Convert $(r, \theta) = \left(6, \frac{2\pi}{3}\right)$ to rectangular coordinates.", selfcheck(r"\left(-3,\ 3\sqrt3\right)"), r"$6\cos\frac{2\pi}{3} = -3$, $6\sin\frac{2\pi}{3} = 3\sqrt3$.", work="1.2cm"),
    Item(r"Write $r = 6\cos\theta$ in rectangular form.", selfcheck(r"(x - 3)^2 + y^2 = 9"), r"$r^2 = 6r\cos\theta$: $x^2 + y^2 = 6x$, so $(x - 3)^2 + y^2 = 9$.", work="1.6cm"),
    Item(r"Write $x^2 + y^2 = 25$ in polar form.", selfcheck(r"r = 5"), r"$r^2 = 25$.", work="1cm"),
    Item(r"For $r = 2\sin\theta$, show that the tangent line at $\theta = \frac\pi4$ is vertical.", selfcheck(r"\tfrac{dx}{d\theta} = 0,\ \tfrac{dy}{d\theta} = 2"),
         r"$x = 2\sin\theta\cos\theta = \sin 2\theta$, $y = 2\sin^2\theta$. $\frac{dx}{d\theta} = 2\cos 2\theta = 0$ and $\frac{dy}{d\theta} = 2\sin 2\theta = 2$ at $\frac\pi4$.", work="2cm"),
    Item(r"Find the slope of $r = 2 + \cos\theta$ at $\theta = \frac\pi2$.", num(sp.Rational(1, 2)), r"$\frac{dx}{d\theta} = -\sin\theta\cos\theta - (2 + \cos\theta)\sin\theta = -2$, $\frac{dy}{d\theta} = -\sin^2\theta + (2 + \cos\theta)\cos\theta = -1$: $\frac12$.", work="2.2cm"),
    Item(r"Find the slope of $r = 3\cos\theta$ at $\theta = \frac\pi6$.", num(-sp.sqrt(3) / 3, tol=1e-3), r"$x = 3\cos^2\theta$, $y = 3\sin\theta\cos\theta$: $\frac{3\cos 2\theta}{-3\sin 2\theta} = -\cot\frac\pi3 = -\frac{1}{\sqrt3}$.", work="2cm"),
    Item(r"For $r = 3 - 2\cos\theta$, is the curve moving toward or away from the origin at $\theta = \frac\pi2$?", selfcheck(r"\text{away}"), r"$r = 3 > 0$ and $\frac{dr}{d\theta} = 2\sin\theta = 2 > 0$.", work="1.4cm"),
    Item(r"For $r = 4\cos\theta$, is the curve moving toward or away from the origin at $\theta = \frac\pi4$?", selfcheck(r"\text{toward}"), r"$r = 2\sqrt2 > 0$, $\frac{dr}{d\theta} = -4\sin\theta < 0$.", work="1.4cm"),
    Item(r"Find the slope of the spiral $r = 2\theta$ at $\theta = \pi$.", num(sp.simplify(pslope(2 * th).subs(th, sp.pi))), r"$\frac{dx}{d\theta} = 2\cos\theta - 2\theta\sin\theta = -2$, $\frac{dy}{d\theta} = 2\sin\theta + 2\theta\cos\theta = -2\pi$: slope $\pi$.", work="2cm"),
]
same("p9", [pslope(2 * th).subs(th, sp.pi)], [sp.pi])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Convert $(r, \theta) = \left(2, \frac\pi2\right)$ to rectangular coordinates.", selfcheck(r"(0, 2)"), r"$2\cos\frac\pi2$, $2\sin\frac\pi2$.", work="1cm"),
        Item(r"Convert $(r, \theta) = (3, \pi)$ to rectangular coordinates.", selfcheck(r"(-3, 0)"), r"$3\cos\pi$, $3\sin\pi$.", work="1cm"),
        Item(r"Convert $(x, y) = (1, 1)$ to polar coordinates with $r > 0$.", selfcheck(r"\left(\sqrt2,\ \tfrac\pi4\right)"), r"$r = \sqrt2$, $\tan\theta = 1$.", work="1cm"),
    ),
    Variants(
        MCQ(r"The polar equation $r = 2\cos\theta$ is the circle", [r"$x^2 + y^2 = 4$", r"$(x - 1)^2 + y^2 = 1$", r"$x^2 + (y - 1)^2 = 1$", r"$(x - 2)^2 + y^2 = 4$"], "B", r"$x^2 + y^2 = 2x$."),
        MCQ(r"The polar equation $r = 6\sin\theta$ is the circle", [r"$x^2 + (y - 3)^2 = 9$", r"$(x - 3)^2 + y^2 = 9$", r"$x^2 + y^2 = 36$", r"$x^2 + (y - 6)^2 = 36$"], "A", r"$x^2 + y^2 = 6y$."),
    ),
    Variants(
        MCQ(r"For a polar curve $r = f(\theta)$, $\frac{dy}{dx} = $", [r"$f'(\theta)$", r"$\frac{f'(\theta)\cos\theta + f(\theta)\sin\theta}{f'(\theta)\sin\theta - f(\theta)\cos\theta}$", r"$\frac{f'(\theta)\sin\theta + f(\theta)\cos\theta}{f'(\theta)\cos\theta - f(\theta)\sin\theta}$", r"$\frac{f(\theta)}{f'(\theta)}$"], "C",
            r"$\frac{dy/d\theta}{dx/d\theta}$ with the product rule.", why_not={"A": "that is $\\frac{dr}{d\\theta}$"}),
    ),
    Variants(
        Item(r"Find the slope of $r = 1 + \sin\theta$ at $\theta = 0$.", num(sp.simplify(pslope(1 + sp.sin(th)).subs(th, 0))), r"$\frac{dx}{d\theta} = \cos^2\theta - (1 + \sin\theta)\sin\theta = 1$, $\frac{dy}{d\theta} = \cos\theta\sin\theta + (1 + \sin\theta)\cos\theta = 1$: $1$.", work="2cm"),
        Item(r"Find the slope of $r = 4$ at $\theta = \frac\pi4$.", num(-1), r"A circle: $-\cot\frac\pi4 = -1$.", work="1.4cm"),
    ),
    Variants(
        Item(r"For $r = 2 + \sin\theta$, is the curve moving toward or away from the origin at $\theta = \frac{3\pi}{4}$?", selfcheck(r"\text{toward}"), r"$\frac{dr}{d\theta} = \cos\frac{3\pi}{4} < 0$, $r > 0$.", work="1.2cm"),
        Item(r"For $r = 2 + \sin\theta$, is the curve moving toward or away from the origin at $\theta = \frac\pi4$?", selfcheck(r"\text{away}"), r"$\frac{dr}{d\theta} = \cos\frac\pi4 > 0$, $r > 0$.", work="1.2cm"),
    ),
]
same("q", [pslope(1 + sp.sin(th)).subs(th, 0), pslope(4 + 0 * th).subs(th, sp.pi / 4)], [1, -1])

# ---------------------------------------------------------------- test prep
_m4 = float(pslope(th + sp.sin(th)).subs(th, 2).evalf())
MCQS = [
    MCQ(r"The slope of the curve $r = 2\theta$ at $\theta = \frac\pi2$ is", [r"$-\frac2\pi$", r"$\frac2\pi$", r"$-\frac\pi2$", r"$2$"], "A", r"$\frac{dx}{d\theta} = -\pi$, $\frac{dy}{d\theta} = 2$.", why_not={"D": "that is $\\frac{dr}{d\\theta}$"}),
    MCQ(r"Which point on $r = 2\cos\theta$, $0 \le \theta < \pi$, has a horizontal tangent?", [r"$\theta = 0$", r"$\theta = \frac\pi2$", r"$\theta = \frac\pi4$", r"$\theta = \frac\pi3$"], "C",
        r"$y = 2\sin\theta\cos\theta = \sin 2\theta$; $\frac{dy}{d\theta} = 2\cos 2\theta = 0$ at $\frac\pi4$, where $\frac{dx}{d\theta} = -2\sin 2\theta \ne 0$."),
    MCQ(r"For $r = 3 + 2\cos\theta$, at $\theta = \frac\pi2$ the curve is", [r"moving away from the origin", r"at the origin", r"not moving", r"moving toward the origin"], "D", r"$\frac{dr}{d\theta} = -2\sin\theta = -2 < 0$, $r = 3 > 0$."),
    MCQ(r"To three decimal places, the slope of $r = \theta + \sin\theta$ at $\theta = 2$ is", [r"$0.584$", rf"${_m4:.3f}$", r"$-1.416$", r"$2.909$"], "B", rf"$\frac{{dy/d\theta}}{{dx/d\theta}}$ at $\theta = 2$: $\approx {_m4:.3f}$.", calc=True),
]
same("m", [pslope(2 * th).subs(th, sp.pi / 2)], [-2 / sp.pi])
close("m4", _m4, 0.235, 5e-4)

FRQS = []

TOPIC = Topic(
    number="9.7", title="Defining Polar Coordinates and Differentiating in Polar Form",
    unit="Unit 9: Parametric Equations, Polar Coordinates, and Vector-Valued Functions", ced=["CHA-3.I", "CHA-3.I.1", "CHA-3.I.2"],
    goals=r"Convert between polar and rectangular coordinates, find slopes of polar curves, and interpret $\frac{dr}{d\theta}$.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
