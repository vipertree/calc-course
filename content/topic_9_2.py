"""Topic 9.2 (BC): Second derivatives of parametric equations.

CED: CHA-3.G (CHA-3.G.2): d^2y/dx^2 = [d/dt (dy/dx)] / (dx/dt), not (d^2y/dt^2)/(d^2x/dt^2); its sign gives concavity.
Lesson example: x = t^2 - 1, y = t^3 - 3t: d^2y/dx^2 = (3t^2 + 3)/(4t^3), 15/32 at t = 2 (concave up; concave up for
t > 0). Worked examples: the unit circle at pi/4 (-2 sqrt 2); x = e^t, y = e^-t (2e^-3t); x = t + 1, y = t^3 - 3t^2
(concave up for t > 1).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, expr, num, same, selfcheck)

t = sp.symbols("t", real=True)


def d1(xt, yt):
    return sp.simplify(sp.diff(yt, t) / sp.diff(xt, t))


def d2(xt, yt):
    return sp.simplify(sp.diff(d1(xt, yt), t) / sp.diff(xt, t))


same("lesson", [d2(t**2 - 1, t**3 - 3 * t), d2(t**2 - 1, t**3 - 3 * t).subs(t, 2)], [(3 * t**2 + 3) / (4 * t**3), sp.Rational(15, 32)])
same("ex", [d2(sp.cos(t), sp.sin(t)).subs(t, sp.pi / 4), d2(sp.exp(t), sp.exp(-t)), d2(t + 1, t**3 - 3 * t**2)], [-2 * sp.sqrt(2), 2 * sp.exp(-3 * t), 6 * t - 6])

NOTES = [
    Video("s9_2.py::Lesson", "Parametric second derivatives", 5),

    Section("Differentiate the slope, then divide by $dx/dt$"),
    Text(r"$\frac{dy}{dx}$ is a function of $t$. To differentiate anything with respect to $x$, differentiate it with respect to $t$ and divide by $\frac{dx}{dt}$."),
    Formula("Second derivative", (r"\[ \frac{d^2y}{dx^2} = \blank{\frac{\frac{d}{dt}\left(\frac{dy}{dx}\right)}{dx/dt}}. \] It is \emph{not} $\dfrac{d^2y/dt^2}{d^2x/dt^2}$.")),
    VideoExample('Concavity at a point', work="4cm"),
    Text(r"\textbf{Concavity on intervals.} Make a sign chart in $t$ for $\frac{d^2y}{dx^2}$: $\frac{3t^2 + 3}{4t^3}$ has the sign of $t$, so the curve is concave up (a bowl) for $t > 0$ and concave down (a hill) for $t < 0$."),
    BigIdea(r"$\frac{d^2y}{dx^2} = \frac{d}{dt}\left(\frac{dy}{dx}\right) \div \frac{dx}{dt}$. Never divide the second derivatives."),
    Check(r"$x = 2t$, $y = t^3$. Find $\frac{d^2y}{dx^2}$.", selfcheck(r"\tfrac{3t}{2}"), r"$\frac{dy}{dx} = \frac{3t^2}{2}$; $\frac{d}{dt}\left(\frac{3t^2}{2}\right) = 3t$; divide by $\frac{dx}{dt} = 2$: $\frac{3t}{2}$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"$x = t^2$, $y = t^3$. Find $\frac{d^2y}{dx^2}$ in terms of $t$.", expr(d2(t**2, t**3), var="t"), r"$\frac{dy}{dx} = \frac32t$; $\frac{d}{dt} = \frac32$; $\div 2t$: $\frac{3}{4t}$.", work="1.6cm"),
    Item(r"$x = 3t$, $y = t^2 + t$. Find $\frac{d^2y}{dx^2}$.", num(d2(3 * t, t**2 + t)), r"$\frac{dy}{dx} = \frac{2t + 1}{3}$; $\frac{d}{dt} = \frac23$; $\div 3$: $\frac29$.", work="1.6cm"),
    Item(r"$x = t^2 + 1$, $y = t^4$. Find $\frac{d^2y}{dx^2}$ at $t = 1$.", num(d2(t**2 + 1, t**4).subs(t, 1)), r"$\frac{dy}{dx} = 2t^2$; $\frac{d}{dt} = 4t$; $\div 2t$: $2$.", work="1.6cm"),
    Item(r"$x = \sin t$, $y = \cos t$. Find $\frac{d^2y}{dx^2}$ at $t = \frac\pi4$.", num(d2(sp.sin(t), sp.cos(t)).subs(t, sp.pi / 4), tol=1e-3), r"$\frac{dy}{dx} = -\tan t$; $\frac{d}{dt} = -\sec^2 t$; $\div \cos t$: $-\sec^3 t = -2\sqrt2$.", work="1.8cm"),
    Item(r"$x = e^t$, $y = te^t$. Find $\frac{d^2y}{dx^2}$ at $t = 0$.", num(d2(sp.exp(t), t * sp.exp(t)).subs(t, 0)), r"$\frac{dy}{dx} = 1 + t$; $\frac{d}{dt} = 1$; $\div e^t$: $e^{-t} = 1$.", work="1.6cm"),
    Item(r"$x = t - 1$, $y = t^3 - 6t^2$. For which $t$ is the curve concave down?", selfcheck(r"t < 2"), r"$\frac{d^2y}{dx^2} = 6t - 12 < 0$ for $t < 2$.", work="1.6cm"),
    Item(r"$x = \ln t$, $y = t^2$ ($t > 0$). Find $\frac{d^2y}{dx^2}$ and the concavity.", selfcheck(r"4t^2 > 0;\ \text{concave up}"), r"$\frac{dy}{dx} = 2t^2$; $\frac{d}{dt} = 4t$; $\div \frac1t$: $4t^2 > 0$.", work="1.8cm"),
    Item(r"$x = t^2$, $y = t^3 - 3t$. A student computes $\frac{d^2y}{dx^2} = \frac{6t}{2} = 3t$. What went wrong, and what is the correct value at $t = 1$?", selfcheck(r"\text{divided } \tfrac{d^2y}{dt^2} \text{ by } \tfrac{d^2x}{dt^2};\ \tfrac32"),
         r"The student divided the second derivatives. Correct: $\frac{dy}{dx} = \frac{3t^2 - 3}{2t}$, $\frac{d^2y}{dx^2} = \frac{3t^2 + 3}{4t^3} = \frac{6}{4} = \frac32$ at $t = 1$.", work="2.2cm"),
]
same("p", [d2(t**2, t**3), d2(t - 1, t**3 - 6 * t**2), d2(sp.log(t), t**2), d2(t**2, t**3 - 3 * t).subs(t, 1)], [3 / (4 * t), 6 * t - 12, 4 * t**2, sp.Rational(3, 2)])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"$x = 2t$, $y = t^2$. Find $\frac{d^2y}{dx^2}$.", num(d2(2 * t, t**2)), r"$\frac{dy}{dx} = t$; $\frac{d}{dt} = 1$; $\div 2$: $\frac12$.", work="1.4cm"),
        Item(r"$x = 4t$, $y = t^3$. Find $\frac{d^2y}{dx^2}$ at $t = 2$.", num(d2(4 * t, t**3).subs(t, 2)), r"$\frac{dy}{dx} = \frac{3t^2}{4}$; $\frac{d}{dt} = \frac{3t}{2}$; $\div 4$: $\frac{3t}{8} = \frac34$.", work="1.4cm"),
        Item(r"$x = t + 2$, $y = t^4$. Find $\frac{d^2y}{dx^2}$ at $t = 1$.", num(d2(t + 2, t**4).subs(t, 1)), r"$12t^2 = 12$.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"Which is the correct formula for $\frac{d^2y}{dx^2}$ of a parametric curve?", [r"$\frac{d^2y/dt^2}{d^2x/dt^2}$", r"$\frac{d}{dt}\left(\frac{dy}{dx}\right)$", r"$\frac{\frac{d}{dt}\left(\frac{dy}{dx}\right)}{dx/dt}$", r"$\frac{dy/dt}{dx/dt}$"], "C",
            r"Differentiate the slope in $t$, then divide by $\frac{dx}{dt}$.", why_not={"A": "the classic wrong shortcut", "B": "forgot to divide by $\\frac{dx}{dt}$"}),
    ),
    Variants(
        Item(r"$x = t^2$, $y = t^3 + 3t$, $t > 0$. Is the curve concave up or concave down at $t = 2$?", selfcheck(r"\text{concave up}"),
             r"$\frac{dy}{dx} = \frac{3t^2 + 3}{2t} = \frac32t + \frac32t^{-1}$; $\frac{d}{dt} = \frac32 - \frac32t^{-2}$; $\div 2t$: $\frac{3t^2 - 3}{4t^3} = \frac{9}{32} > 0$ at $t = 2$.", work="2cm"),
        Item(r"$x = t^2$, $y = t^3 + 3t$, $t > 0$. Is the curve concave up or concave down at $t = \frac12$?", selfcheck(r"\text{concave down}"),
             r"$\frac{d^2y}{dx^2} = \frac{3t^2 - 3}{4t^3} = \frac{-9/4}{1/2} = -\frac92 < 0$ at $t = \frac12$.", work="2cm"),
    ),
    Variants(
        Item(r"$x = t - 3$, $y = t^3 - 3t$. For which $t$ is the curve concave up?", selfcheck(r"t > 0"), r"$\frac{d^2y}{dx^2} = 6t > 0$ for $t > 0$.", work="1.4cm"),
        Item(r"$x = 2t$, $y = t^3 - 6t^2$. For which $t$ is the curve concave down?", selfcheck(r"t < 2"), r"$\frac{dy}{dx} = \frac{3t^2 - 12t}{2}$; $\frac{d}{dt} = 3t - 6$; $\div 2$: $\frac{3t - 6}{2} < 0$ for $t < 2$.", work="1.6cm"),
    ),
    Variants(
        Item(r"$x = e^t$, $y = e^{3t}$. Find $\frac{d^2y}{dx^2}$ at $t = 0$.", num(d2(sp.exp(t), sp.exp(3 * t)).subs(t, 0)), r"$\frac{dy}{dx} = 3e^{2t}$; $\frac{d}{dt} = 6e^{2t}$; $\div e^t$: $6e^t = 6$.", work="1.6cm"),
        Item(r"$x = t^3$, $y = t^6$. Find $\frac{d^2y}{dx^2}$.", num(d2(t**3, t**6)), r"$\frac{dy}{dx} = 2t^3$; $\frac{d}{dt} = 6t^2$; $\div 3t^2$: $2$ (it is $y = x^2$).", work="1.6cm"),
    ),
]
same("q", [d2(t**2, t**3 + 3 * t).subs(t, 2), d2(t**2, t**3 + 3 * t).subs(t, sp.Rational(1, 2))], [sp.Rational(9, 32), -sp.Rational(9, 2)])

# ---------------------------------------------------------------- test prep
_m4 = float(d2(t + sp.sin(t), sp.cos(t)).subs(t, 1).evalf())
MCQS = [
    MCQ(r"For $x = t^2 + 1$, $y = t^3$, $\frac{d^2y}{dx^2}$ at $t = 2$ is", [r"$\frac38$", r"$\frac34$", r"$3$", r"$\frac{3}{16}$"], "A", r"$\frac{dy}{dx} = \frac32t$; $\frac{d}{dt} = \frac32$; $\div 2t = 4$: $\frac38$.",
        why_not={"B": "forgot to divide by $\\frac{dx}{dt}$"}),
    MCQ(r"For $x = \cos t$, $y = \sin t$, $0 < t < \pi$, the curve is", [r"concave up", r"concave up for $t < \frac\pi2$ only", r"concave down for $t > \frac\pi2$ only", r"concave down"], "D", r"$\frac{d^2y}{dx^2} = -\csc^3 t < 0$ on $(0, \pi)$: the top half of a circle."),
    MCQ(r"For $x = e^{2t}$, $y = e^{t}$, $\frac{d^2y}{dx^2} = $", [r"$\frac14 e^{-3t}$", r"$-\frac14 e^{-3t}$", r"$\frac12 e^{-t}$", r"$-\frac12 e^{-t}$"], "B", r"$\frac{dy}{dx} = \frac12 e^{-t}$; $\frac{d}{dt} = -\frac12 e^{-t}$; $\div 2e^{2t}$: $-\frac14 e^{-3t}$."),
    MCQ(r"For $x = t + \sin t$, $y = \cos t$, to three decimal places $\frac{d^2y}{dx^2}$ at $t = 1$ is", [r"$-0.540$", r"$-0.351$", rf"${_m4:.3f}$", r"$0.153$"], "C",
        rf"$\frac{{dy}}{{dx}} = \frac{{-\sin t}}{{1 + \cos t}}$; differentiate in $t$ and divide by $1 + \cos t$: $\approx {_m4:.3f}$ at $t = 1$.", calc=True),
]
close("m4", _m4, -0.421, 5e-3)
same("m", [d2(t**2 + 1, t**3).subs(t, 2), d2(sp.cos(t), sp.sin(t)), d2(sp.exp(2 * t), sp.exp(t))], [sp.Rational(3, 8), -1 / sp.sin(t)**3, -sp.exp(-3 * t) / 4])

FRQS = []

TOPIC = Topic(
    number="9.2", title="Second Derivatives of Parametric Equations",
    unit="Unit 9: Parametric Equations, Polar Coordinates, and Vector-Valued Functions", ced=["CHA-3.G", "CHA-3.G.2"],
    goals=r"Find $\frac{d^2y}{dx^2}$ for parametric curves and use it to decide concavity.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
