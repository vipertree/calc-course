"""Topic 9.3 (BC): Finding arc lengths of curves given by parametric equations.

CED: CHA-6.B (CHA-6.B.1): L = integral from a to b of sqrt((dx/dt)^2 + (dy/dt)^2) dt; the integrand is the speed, so L
is the distance traveled. Circle check (2 pi r). Lesson example: x = t^2, y = (2/3)t^3, 0 <= t <= sqrt 3 (14/3).
Worked examples: half a circle of radius 3 (3 pi); one arch of the cycloid (8); x = e^t, y = t on [0, 1] (2.003).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)

t = sp.symbols("t", real=True)


def speed2(xt, yt):
    return sp.simplify(sp.diff(xt, t)**2 + sp.diff(yt, t)**2)


def length_n(xt, yt, a, b):
    return float(sp.Integral(sp.sqrt(sp.diff(xt, t)**2 + sp.diff(yt, t)**2), (t, a, b)).evalf())


same("lesson", [sp.factor(speed2(t**2, sp.Rational(2, 3) * t**3)), sp.integrate(2 * t * sp.sqrt(1 + t**2), (t, 0, sp.sqrt(3)))], [4 * t**2 * (t**2 + 1), sp.Rational(14, 3)])
same("ex", [speed2(3 * sp.cos(t), 3 * sp.sin(t)), sp.simplify(speed2(t - sp.sin(t), 1 - sp.cos(t)) - (2 - 2 * sp.cos(t))), sp.integrate(2 * sp.sin(t / 2), (t, 0, 2 * sp.pi))], [9, 0, 8])
close("ex3", length_n(sp.exp(t), t, 0, 1), 2.003, 5e-4)

NOTES = [
    Video("s9_3.py::Lesson", "Parametric arc length", 5),

    Section("Tiny hypotenuses in time"),
    Text(r"In a tiny time $dt$ the point moves $dx$ across and $dy$ up: $ds^2 = dx^2 + dy^2$, so $ds = \sqrt{\left(\frac{dx}{dt}\right)^2 + \left(\frac{dy}{dt}\right)^2}\,dt$."),
    Formula("Parametric arc length", (r"If $x'$ and $y'$ are continuous and the curve is traced once for $a \le t \le b$, \[ L = \blank{\int_a^b \sqrt{\left(\frac{dx}{dt}\right)^2 + \left(\frac{dy}{dt}\right)^2}\,dt}. \] "
                                      r"The integrand is the speed, so $L$ is the distance traveled.")),
    Text(r"\textbf{Check.} $x = r\cos t$, $y = r\sin t$, $0 \le t \le 2\pi$: the integrand is $r$, and $L = 2\pi r$."),
    VideoExample('An exact length', work="4.6cm"),
    Text(r"\textbf{Usually a calculator.} Most parametric arc lengths have no elementary antiderivative: set up the integral and evaluate it numerically."),
    BigIdea(r"Arc length $= \int \sqrt{(x')^2 + (y')^2}\,dt$: distance traveled is speed integrated over time."),
    Check(r"Write the integral for the length of $x = t^2$, $y = t^3$, $0 \le t \le 2$.", selfcheck(r"\int_0^2 \sqrt{4t^2 + 9t^4}\,dt"), r"$x' = 2t$, $y' = 3t^2$."),
]

# ---------------------------------------------------------------- practice
_p4 = length_n(t**2, t**3, 0, 1)
_p7 = length_n(sp.cos(t), 2 * sp.sin(t), 0, 2 * sp.pi)
PRACTICE = [
    Item(r"Find the length of $x = 2t$, $y = 3t$ for $0 \le t \le 4$.", num(4 * sp.sqrt(13), tol=1e-3), r"$\int_0^4 \sqrt{13}\,dt = 4\sqrt{13} \approx 14.422$.", work="1.4cm"),
    Item(r"Find the length of $x = 5\cos t$, $y = 5\sin t$ for $0 \le t \le \frac\pi2$.", num(5 * sp.pi / 2, tol=1e-3), r"Integrand $5$: $\frac{5\pi}{2}$.", work="1.4cm"),
    Item(r"Find the length of $x = t^2$, $y = \frac23t^3$ for $0 \le t \le 1$.", num(sp.integrate(2 * t * sp.sqrt(1 + t**2), (t, 0, 1)), tol=1e-3), r"$\int_0^1 2t\sqrt{1 + t^2}\,dt = \frac23\left(2^{3/2} - 1\right) \approx 1.219$.", work="2cm"),
    Item(r"Use a calculator to find the length of $x = t^2$, $y = t^3$ for $0 \le t \le 1$.", num(sp.Float(round(_p4, 4)), tol=2e-3), rf"$\int_0^1 \sqrt{{4t^2 + 9t^4}}\,dt \approx {_p4:.3f}$.", work="1.4cm", calc=True),
    Item(r"Find the length of $x = e^t\cos t$, $y = e^t\sin t$ for $0 \le t \le 1$.", num(sp.sqrt(2) * (sp.E - 1), tol=1e-3),
         r"$(x')^2 + (y')^2 = 2e^{2t}$: $\int_0^1 \sqrt2 e^t\,dt = \sqrt2(e - 1) \approx 2.430$.", work="2.2cm"),
    Item(r"Write, but do not evaluate, the length of $x = \ln t$, $y = t^2$ for $1 \le t \le 3$.", selfcheck(r"\int_1^3 \sqrt{\frac{1}{t^2} + 4t^2}\,dt"), r"$x' = \frac1t$, $y' = 2t$.", work="1.2cm"),
    Item(r"Use a calculator to find the perimeter of the ellipse $x = \cos t$, $y = 2\sin t$, $0 \le t \le 2\pi$.", num(sp.Float(round(_p7, 4)), tol=2e-3), rf"$\int_0^{{2\pi}} \sqrt{{\sin^2 t + 4\cos^2 t}}\,dt \approx {_p7:.3f}$.", work="1.4cm", calc=True),
    Item(r"Find the length of $x = t - \sin t$, $y = 1 - \cos t$ for $0 \le t \le \pi$.", num(4), r"Half the arch: $\int_0^\pi 2\sin\frac t2\,dt = 4$.", work="1.8cm"),
]
same("p", [speed2(sp.exp(t) * sp.cos(t), sp.exp(t) * sp.sin(t)), sp.integrate(2 * sp.sin(t / 2), (t, 0, sp.pi))], [2 * sp.exp(2 * t), 4])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"Which gives the length of $x = t^3$, $y = t^2$ for $0 \le t \le 1$?", [r"$\int_0^1 \sqrt{t^6 + t^4}\,dt$", r"$\int_0^1 \sqrt{9t^4 + 4t^2}\,dt$", r"$\int_0^1 \left(3t^2 + 2t\right) dt$", r"$\int_0^1 \sqrt{1 + \frac{4}{9t^2}}\,dt$"], "B",
            r"$x' = 3t^2$, $y' = 2t$.", why_not={"A": "used $x$ and $y$ instead of their derivatives", "C": "added instead of using Pythagoras"}),
        MCQ(r"Which gives the length of $x = \sin t$, $y = t$ for $0 \le t \le \pi$?", [r"$\int_0^\pi \sqrt{\sin^2 t + t^2}\,dt$", r"$\int_0^\pi (\cos t + 1)\,dt$", r"$\int_0^\pi \sqrt{1 + \cos^2 t}\,dt$", r"$\int_0^\pi \sqrt{1 + \sin^2 t}\,dt$"], "C",
            r"$x' = \cos t$, $y' = 1$."),
    ),
    Variants(
        Item(r"Find the length of $x = 4t$, $y = 3t$ for $0 \le t \le 2$.", num(10), r"Speed $5$: $10$.", work="1.2cm"),
        Item(r"Find the length of $x = 6t$, $y = 8t$ for $0 \le t \le 1$.", num(10), r"Speed $10$: $10$.", work="1.2cm"),
        Item(r"Find the length of $x = 2\cos t$, $y = 2\sin t$ for $0 \le t \le \pi$.", num(2 * sp.pi, tol=1e-3), r"Speed $2$: $2\pi$.", work="1.2cm"),
    ),
    Variants(
        Item(r"Find the length of $x = t^2$, $y = \frac23 t^3$ for $0 \le t \le 2\sqrt2$.", num(sp.integrate(2 * t * sp.sqrt(1 + t**2), (t, 0, 2 * sp.sqrt(2)))), r"$\frac23\left(9^{3/2} - 1\right) = \frac{52}{3}$.", work="2cm"),
        Item(r"Find the length of $x = \frac{t^2}{2}$, $y = \frac13 t^3$ for $0 \le t \le \sqrt8$.", num(sp.integrate(t * sp.sqrt(1 + t**2), (t, 0, sp.sqrt(8)))), r"Speed $t\sqrt{1 + t^2}$: $\frac13\left(27 - 1\right) = \frac{26}{3}$.", work="2cm"),
    ),
    Variants(
        Item(r"Use a calculator: length of $x = t$, $y = t^2$ for $0 \le t \le 2$.", num(sp.Float(round(length_n(t, t**2, 0, 2), 4)), tol=2e-3), rf"$\int_0^2 \sqrt{{1 + 4t^2}}\,dt \approx {length_n(t, t**2, 0, 2):.3f}$.", work="1.2cm", calc=True),
        Item(r"Use a calculator: length of $x = \cos t$, $y = t$ for $0 \le t \le \pi$.", num(sp.Float(round(length_n(sp.cos(t), t, 0, sp.pi), 4)), tol=2e-3), rf"$\int_0^\pi \sqrt{{\sin^2 t + 1}}\,dt \approx {length_n(sp.cos(t), t, 0, sp.pi):.3f}$.", work="1.2cm", calc=True),
    ),
    Variants(
        MCQ(r"For a moving point $(x(t), y(t))$, the quantity $\sqrt{\left(x'(t)\right)^2 + \left(y'(t)\right)^2}$ is", [r"the acceleration", r"the slope of the path", r"the displacement", r"the speed"], "D", r"Its integral is the distance traveled."),
    ),
]

# ---------------------------------------------------------------- test prep
_m4 = length_n(t**3 - t, t**2, 0, 2)
MCQS = [
    MCQ(r"The length of $x = 3t^2$, $y = 2t^3$ for $0 \le t \le 1$ is", [r"$2\left(2\sqrt2 - 1\right)$", r"$4\sqrt2$", r"$2\sqrt2 - 1$", r"$\frac{2}{3}\left(2\sqrt2 - 1\right)$"], "A",
        r"Speed $\sqrt{36t^2 + 36t^4} = 6t\sqrt{1 + t^2}$: $\int_0^1 6t\sqrt{1 + t^2}\,dt = 2\left(2^{3/2} - 1\right)$."),
    MCQ(r"The length of one arch of $x = 2(t - \sin t)$, $y = 2(1 - \cos t)$, $0 \le t \le 2\pi$, is", [r"$8$", r"$4\pi$", r"$16$", r"$8\pi$"], "C", r"Twice the unit cycloid's $8$."),
    MCQ(r"A particle moves with $x'(t) = 2\cos t$ and $y'(t) = 2\sin t$. The distance it travels for $0 \le t \le 3$ is", [r"$2$", r"$6$", r"$3$", r"$12$"], "B", r"Speed $2$ for $3$ units of time."),
    MCQ(r"To three decimal places, the length of $x = t^3 - t$, $y = t^2$ for $0 \le t \le 2$ is", [r"$6.000$", r"$4.000$", rf"${_m4:.3f}$", r"$8.944$"], "C", rf"$\int_0^2 \sqrt{{(3t^2 - 1)^2 + 4t^2}}\,dt \approx {_m4:.3f}$.", calc=True),
]
close("m4", _m4, 8.103, 5e-3)
same("m", [sp.integrate(6 * t * sp.sqrt(1 + t**2), (t, 0, 1))], [2 * (2 * sp.sqrt(2) - 1)])

FRQS = []

TOPIC = Topic(
    number="9.3", title="Finding Arc Lengths of Curves Given by Parametric Equations",
    unit="Unit 9: Parametric Equations, Polar Coordinates, and Vector-Valued Functions", ced=["CHA-6.B", "CHA-6.B.1"],
    goals=r"Find the length of a parametric curve by integrating the speed.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
