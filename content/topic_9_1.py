"""Topic 9.1 (BC): Defining and differentiating parametric equations.

CED: CHA-3.G (CHA-3.G.1): for x = x(t), y = y(t), dy/dx = (dy/dt)/(dx/dt) where dx/dt != 0; horizontal tangents where
dy/dt = 0 (dx/dt != 0), vertical where dx/dt = 0 (dy/dt != 0); orientation; eliminating the parameter. Lesson example:
x = t^2 - 1, y = t^3 - 3t, tangent at t = 2: y - 2 = (9/4)(x - 3). Worked examples: the unit circle; horizontal and
vertical tangents of x = t^2 - 2t, y = t^3 - 12t; eliminating the parameter from x = 2t + 1, y = t^2.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, expr, num, same, selfcheck)
from calclib.figs import graph

t = sp.symbols("t", real=True)


def slope(xt, yt):
    return sp.simplify(sp.diff(yt, t) / sp.diff(xt, t))


xL, yL = t**2 - 1, t**3 - 3 * t
same("lesson", [slope(xL, yL).subs(t, 2), xL.subs(t, 2), yL.subs(t, 2), sorted(sp.solve(sp.diff(yL, t), t)), sp.solve(sp.diff(xL, t), t)], [sp.Rational(9, 4), 3, 2, [-1, 1], [0]])
same("ex1", [slope(sp.cos(t), sp.sin(t)).subs(t, sp.pi / 4)], [-1])
xE, yE = t**2 - 2 * t, t**3 - 12 * t
same("ex2", [[(xE.subs(t, s), yE.subs(t, s)) for s in (2, -2, 1)]], [[(0, -16), (8, 16), (-1, -11)]])

FIG = graph("t9_1_curve", [], (-1.6, 3.6), (-2.8, 2.8), extra=r"\addplot[fn, domain=-2.1:2.1, samples=200, variable=\t]({\t*\t-1},{\t*\t*\t-3*\t});",
            caption=r"$x = t^2 - 1$, $y = t^3 - 3t$ for $-2.1 \le t \le 2.1$. It passes through $x = 0$ twice.")

NOTES = [
    Video("s9_1.py::Lesson", "Parametric equations", 6),

    Section("Parametric curves"),
    Text(r"Parametric equations give each coordinate in terms of a parameter $t$: $x = x(t)$, $y = y(t)$. Plot points in order of $t$; the direction of increasing $t$ is the \emph{orientation}. "
         r"A parametric curve can loop or double back, which $y = f(x)$ cannot."),
    FIG,
    Formula("Slope of a parametric curve", (r"By the chain rule, $\frac{dy}{dt} = \frac{dy}{dx}\cdot\frac{dx}{dt}$, so \[ \frac{dy}{dx} = \blank{\frac{dy/dt}{dx/dt}} \quad \text{where } \frac{dx}{dt} \ne 0. \]")),
    VideoExample('A tangent line', work="3.6cm"),
    Formula("Horizontal and vertical tangents", (r"Horizontal tangent: \blank{$\frac{dy}{dt} = 0$} and $\frac{dx}{dt} \ne 0$. Vertical tangent: \blank{$\frac{dx}{dt} = 0$} and $\frac{dy}{dt} \ne 0$. If both are $0$, look more closely.")),
    Text(r"\textbf{Eliminating the parameter.} Solve one equation for $t$ and substitute: $x = 2t + 1$, $y = t^2$ gives $y = \frac{(x - 1)^2}{4}$."),
    BigIdea(r"$\frac{dy}{dx} = \frac{dy/dt}{dx/dt}$. Find the point by plugging the same $t$ into $x(t)$ and $y(t)$."),
    Check(r"$x = 3t$, $y = t^2 + 1$. Find $\frac{dy}{dx}$ at $t = 3$.", selfcheck(r"2"), r"$\frac{2t}{3}$ at $t = 3$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"$x = t^2$, $y = t^3$. Find $\frac{dy}{dx}$ in terms of $t$.", expr(slope(t**2, t**3), var="t"), r"$\frac{3t^2}{2t} = \frac{3t}{2}$.", work="1.2cm"),
    Item(r"$x = 2t - 1$, $y = t^2 + 3t$. Find the slope of the curve at $t = 1$.", num(slope(2 * t - 1, t**2 + 3 * t).subs(t, 1)), r"$\frac{2t + 3}{2} = \frac52$.", work="1.2cm"),
    Item(r"$x = e^t$, $y = e^{2t}$. Find $\frac{dy}{dx}$ at $t = 0$.", num(slope(sp.exp(t), sp.exp(2 * t)).subs(t, 0)), r"$\frac{2e^{2t}}{e^t} = 2e^t = 2$.", work="1.2cm"),
    Item(r"$x = 3\cos t$, $y = 2\sin t$. Find $\frac{dy}{dx}$ at $t = \frac\pi4$.", num(slope(3 * sp.cos(t), 2 * sp.sin(t)).subs(t, sp.pi / 4)), r"$\frac{2\cos t}{-3\sin t} = -\frac23$.", work="1.4cm"),
    Item(r"$x = t^2 + 1$, $y = 2t^3$. Find the equation of the tangent line at $t = 1$.", selfcheck(r"y - 2 = 3(x - 2)"), r"Point $(2, 2)$; slope $\frac{6t^2}{2t} = 3t = 3$.", work="1.8cm"),
    Item(r"$x = t^3 - 3t$, $y = t^2$. At what values of $t$ is the tangent line vertical?", selfcheck(r"t = \pm1"), r"$\frac{dx}{dt} = 3t^2 - 3 = 0$ at $t = \pm1$, where $\frac{dy}{dt} = \pm2 \ne 0$.", work="1.4cm"),
    Item(r"$x = t^2 - 4t$, $y = t^2 - 2t$. Find the point where the tangent line is horizontal.", selfcheck(r"(-3, -1)"), r"$\frac{dy}{dt} = 2t - 2 = 0$ at $t = 1$ ($\frac{dx}{dt} = -2$): $(-3, -1)$.", work="1.6cm"),
    Item(r"$x = \sqrt t$, $y = t + 1$. Eliminate the parameter.", selfcheck(r"y = x^2 + 1, \ x \ge 0"), r"$t = x^2$, so $y = x^2 + 1$ with $x \ge 0$.", work="1.2cm"),
    Item(r"$x = \sin t$, $y = \cos^2 t$. Find $\frac{dy}{dx}$ in terms of $t$, and simplify.", selfcheck(r"-2\sin t"), r"$\frac{-2\cos t\sin t}{\cos t} = -2\sin t$ (where $\cos t \ne 0$).", work="1.6cm"),
    Item(r"$x = t - \sin t$, $y = 1 - \cos t$. Find $\frac{dy}{dx}$ at $t = \frac\pi2$.", num(slope(t - sp.sin(t), 1 - sp.cos(t)).subs(t, sp.pi / 2)), r"$\frac{\sin t}{1 - \cos t} = \frac{1}{1} = 1$.", work="1.4cm"),
]

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"$x = t^2 + t$, $y = t^3$. Find $\frac{dy}{dx}$ at $t = 1$.", num(slope(t**2 + t, t**3).subs(t, 1)), r"$\frac{3t^2}{2t + 1} = 1$.", work="1.2cm"),
        Item(r"$x = 4t$, $y = t^2 - 1$. Find $\frac{dy}{dx}$ at $t = 2$.", num(slope(4 * t, t**2 - 1).subs(t, 2)), r"$\frac{2t}{4} = 1$.", work="1.2cm"),
        Item(r"$x = \ln t$, $y = t^2$. Find $\frac{dy}{dx}$ at $t = 3$.", num(slope(sp.log(t), t**2).subs(t, 3)), r"$\frac{2t}{1/t} = 2t^2 = 18$.", work="1.2cm"),
    ),
    Variants(
        MCQ(r"$x = t^2 - 4$, $y = t^3 - 3t$. At which $t$ is the tangent horizontal?", [r"$t = 0$", r"$t = \pm1$", r"$t = \pm2$", r"$t = \pm\sqrt3$"], "B", r"$\frac{dy}{dt} = 3t^2 - 3 = 0$, and $\frac{dx}{dt} = 2t \ne 0$ there."),
        MCQ(r"$x = t^2 - 4$, $y = t^3 - 3t$. At which $t$ is the tangent vertical?", [r"$t = 0$", r"$t = \pm1$", r"$t = \pm2$", r"$t = 4$"], "A", r"$\frac{dx}{dt} = 2t = 0$, and $\frac{dy}{dt} = -3 \ne 0$."),
    ),
    Variants(
        Item(r"$x = 2\cos t$, $y = 2\sin t$. Find $\frac{dy}{dx}$ at $t = \frac\pi3$.", num(slope(2 * sp.cos(t), 2 * sp.sin(t)).subs(t, sp.pi / 3), tol=1e-3), r"$-\cot\frac\pi3 = -\frac{1}{\sqrt3} \approx -0.577$.", work="1.4cm"),
        Item(r"$x = \cos t$, $y = \sin t$. Find $\frac{dy}{dx}$ at $t = \frac\pi6$.", num(slope(sp.cos(t), sp.sin(t)).subs(t, sp.pi / 6), tol=1e-3), r"$-\cot\frac\pi6 = -\sqrt3 \approx -1.732$.", work="1.4cm"),
    ),
    Variants(
        Item(r"$x = t + 1$, $y = t^2$. Write the tangent line at $t = 2$.", selfcheck(r"y - 4 = 4(x - 3)"), r"Point $(3, 4)$, slope $2t = 4$.", work="1.6cm"),
        Item(r"$x = t^2$, $y = 3t$. Write the tangent line at $t = 1$.", selfcheck(r"y - 3 = \tfrac32(x - 1)"), r"Point $(1, 3)$, slope $\frac{3}{2t} = \frac32$.", work="1.6cm"),
    ),
    Variants(
        MCQ(r"Eliminating the parameter from $x = t - 2$, $y = t^2$ gives", [r"$y = x^2 - 2$", r"$y = (x - 2)^2$", r"$y = (x + 2)^2$", r"$y = x^2 + 4$"], "C", r"$t = x + 2$."),
        MCQ(r"Eliminating the parameter from $x = 3t$, $y = t + 1$ gives", [r"$y = \frac x3 + 1$", r"$y = 3x + 1$", r"$y = \frac{x + 1}{3}$", r"$y = 3(x + 1)$"], "A", r"$t = \frac x3$."),
    ),
]

# ---------------------------------------------------------------- test prep
_m4 = float(slope(t**2 + sp.sin(t), t * sp.exp(t)).subs(t, 1).evalf())
MCQS = [
    MCQ(r"For $x = t^3 + t$, $y = t^4 - 2t^2$, $\frac{dy}{dx}$ at $t = 1$ is", [r"$0$", r"$1$", r"$-1$", r"$\frac14$"], "A", r"$\frac{4t^3 - 4t}{3t^2 + 1} = \frac04 = 0$."),
    MCQ(r"The curve $x = t^2$, $y = t^3 - 12t$ has horizontal tangents at", [r"$(0, 0)$ only", r"$(2, -16)$ only", r"$(4, -16)$ and $(4, 16)$", r"$(2, \pm16)$"], "C", r"$3t^2 - 12 = 0$ at $t = \pm2$: $(4, -16)$ and $(4, 16)$."),
    MCQ(r"An equation of the tangent line to $x = \sec t$, $y = \tan t$ at $t = \frac\pi4$ is", [r"$y - 1 = \sqrt2(x - \sqrt2)$", r"$y - 1 = \frac{1}{\sqrt2}(x - 1)$", r"$y - \sqrt2 = \sqrt2(x - 1)$", r"$y - 1 = \frac{1}{\sqrt2}(x - \sqrt2)$"], "A",
        r"$\frac{dy}{dx} = \frac{\sec^2 t}{\sec t\tan t} = \frac{\sec t}{\tan t} = \sqrt2$ at $\frac\pi4$; point $(\sqrt2, 1)$."),
    MCQ(r"For $x = t^2 + \sin t$, $y = te^t$, to three decimal places $\frac{dy}{dx}$ at $t = 1$ is", [r"$2.000$", rf"${_m4:.3f}$", r"$0.394$", r"$5.437$"], "B", rf"$\frac{{(1 + t)e^t}}{{2t + \cos t}}$ at $t = 1$: $\frac{{2e}}{{2 + \cos 1}} \approx {_m4:.3f}$.", calc=True),
]
same("m", [slope(t**3 + t, t**4 - 2 * t**2).subs(t, 1), slope(sp.sec(t), sp.tan(t)).subs(t, sp.pi / 4)], [0, sp.sqrt(2)])

FRQS = []

TOPIC = Topic(
    number="9.1", title="Defining and Differentiating Parametric Equations",
    unit="Unit 9: Parametric Equations, Polar Coordinates, and Vector-Valued Functions", ced=["CHA-3.G", "CHA-3.G.1"],
    goals=r"Find $\frac{dy}{dx}$ for parametric curves, write tangent lines, and locate horizontal and vertical tangents.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
