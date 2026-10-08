"""Topic 9.4 (BC): Defining and differentiating vector-valued functions.

CED: CHA-3.H (CHA-3.H.1, CHA-3.H.2): r(t) = <x(t), y(t)>; derivatives componentwise: v = r' (tangent to the path, length
= speed), a = r''. Lesson example: r = <t^2, t^3 - 3t> at t = 2: v = <4, 9>, a = <2, 12>, speed sqrt 97. Worked
examples: the unit circle (v perpendicular to r, a = -r); <e^2t, ln(t + 1)> at 0; direction of motion of
<t^2 - 4t, t^3> at t = 1.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)

t = sp.symbols("t", real=True)


def vel(r):
    return [sp.diff(c, t) for c in r]


def at(vec, s):
    return [sp.simplify(c.subs(t, s)) for c in vec]


rL = [t**2, t**3 - 3 * t]
same("lesson", [at(vel(rL), 2), at(vel(vel(rL)), 2), sp.sqrt(sum(c**2 for c in at(vel(rL), 2)))], [[4, 9], [2, 12], sp.sqrt(97)])
same("ex", [at(vel([sp.exp(2 * t), sp.log(t + 1)]), 0), at(vel(vel([sp.exp(2 * t), sp.log(t + 1)])), 0), at(vel([t**2 - 4 * t, t**3]), 1)], [[2, 1], [4, -1], [-2, 3]])


def vec(v):
    return r"\langle " + ",\ ".join(sp.latex(c) for c in v) + r"\rangle"


NOTES = [
    Video("s9_4.py::Lesson", "Vector-valued functions", 4),

    Section("Vectors made of functions"),
    Text(r"A vector-valued function $\vec r(t) = \langle x(t), y(t)\rangle$ points from the origin to the moving point. It carries the same information as the parametric equations $x = x(t)$, $y = y(t)$."),
    Formula("Derivatives, componentwise", (r"\[ \vec v(t) = \vec r\,'(t) = \blank{\langle x'(t),\ y'(t)\rangle}, \qquad \vec a(t) = \vec r\,''(t) = \blank{\langle x''(t),\ y''(t)\rangle}. \]")),
    Formula("What the velocity vector tells you", (r"Direction: the way the point is moving, tangent to the path. Length: the \blank{speed} $|\vec v| = \sqrt{(x')^2 + (y')^2}$. Slope of the path: $\frac{y'}{x'}$.")),
    VideoExample('Velocity and acceleration at a time', work="3.4cm"),
    Text(r"\textbf{Signs of the components.} $x' > 0$: moving right; $x' < 0$: moving left. $y' > 0$: moving up; $y' < 0$: moving down."),
    BigIdea(r"Differentiate each component. $\vec r\,'$ is the velocity (tangent, length = speed); $\vec r\,''$ is the acceleration."),
    Check(r"$\vec r(t) = \langle 3t,\ t^2\rangle$. Find $\vec v(1)$ and the speed at $t = 1$.", selfcheck(r"\langle 3, 2\rangle,\ \sqrt{13}"), r"$\vec v = \langle 3, 2t\rangle$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"$\vec r(t) = \langle t^3,\ 2t\rangle$. Find $\vec v(t)$.", selfcheck(vec(vel([t**3, 2 * t]))), r"Differentiate each component.", work="1cm"),
    Item(r"$\vec r(t) = \langle \sin 2t,\ \cos t\rangle$. Find $\vec v\left(\frac\pi2\right)$.", selfcheck(vec(at(vel([sp.sin(2 * t), sp.cos(t)]), sp.pi / 2))), r"$\langle 2\cos 2t, -\sin t\rangle$ at $\frac\pi2$.", work="1.2cm"),
    Item(r"$\vec r(t) = \langle t^2 + 1,\ t^3\rangle$. Find $\vec a(1)$.", selfcheck(vec(at(vel(vel([t**2 + 1, t**3])), 1))), r"$\vec a = \langle 2, 6t\rangle$.", work="1.2cm"),
    Item(r"$\vec r(t) = \langle 3\cos t,\ 3\sin t\rangle$. Find the speed.", num(3), r"$|\langle -3\sin t, 3\cos t\rangle| = 3$.", work="1.2cm"),
    Item(r"$\vec r(t) = \langle e^t,\ e^{-t}\rangle$. Find the speed at $t = 0$.", num(sp.sqrt(2), tol=1e-3), r"$\vec v(0) = \langle 1, -1\rangle$: $\sqrt2$.", work="1.2cm"),
    Item(r"$\vec r(t) = \langle t^2 - 2t,\ t^2 + t\rangle$. At $t = \frac12$, is the particle moving left or right? Up or down?", selfcheck(r"\text{left and up}"), r"$\vec v\left(\tfrac12\right) = \langle -1, 2\rangle$.", work="1.4cm"),
    Item(r"$\vec r(t) = \langle t^2,\ t^3\rangle$. Find the slope of the path at $t = 2$.", num(3), r"$\frac{y'}{x'} = \frac{3t^2}{2t} = \frac{3t}{2} = 3$.", work="1.2cm"),
    Item(r"$\vec r(t) = \langle \ln t,\ t^2\rangle$, $t > 0$. Find $\vec v(1)$ and $\vec a(1)$.", selfcheck(r"\vec v(1) = \langle 1, 2\rangle,\ \vec a(1) = \langle -1, 2\rangle"), r"$\vec v = \langle \frac1t, 2t\rangle$, $\vec a = \langle -\frac{1}{t^2}, 2\rangle$.", work="1.4cm"),
    Item(r"At what time $t \ge 0$ is the particle with $\vec r(t) = \langle t^2 - 6t,\ 4t\rangle$ moving straight up?", num(3), r"$x' = 2t - 6 = 0$ at $t = 3$, while $y' = 4 > 0$.", work="1.2cm"),
]
same("p", [at(vel([sp.log(t), t**2]), 1), at(vel(vel([sp.log(t), t**2])), 1), at(vel([t**2 - 2 * t, t**2 + t]), sp.Rational(1, 2))], [[1, 2], [-1, 2], [-1, 2]])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"$\vec r(t) = \langle t^2,\ 5t\rangle$. Find the speed at $t = 6$.", num(13), r"$\vec v(6) = \langle 12, 5\rangle$: $13$.", work="1.2cm"),
        Item(r"$\vec r(t) = \langle 4t,\ t^2\rangle$. Find the speed at $t = \frac32$.", num(5), r"$\vec v = \langle 4, 3\rangle$: $5$.", work="1.2cm"),
        Item(r"$\vec r(t) = \langle t^3,\ 4t\rangle$. Find the speed at $t = 1$.", num(5), r"$\vec v = \langle 3, 4\rangle$: $5$.", work="1.2cm"),
    ),
    Variants(
        MCQ(r"$\vec r(t) = \langle \cos t,\ \sin t\rangle$. The acceleration vector points", [r"along the velocity", r"toward the center of the circle", r"away from the center", r"straight up"], "B", r"$\vec a = -\vec r$."),
    ),
    Variants(
        Item(r"$\vec r(t) = \langle e^{t},\ t^2\rangle$. Find $\vec a(0)$.", selfcheck(r"\langle 1, 2\rangle"), r"$\langle e^t, 2\rangle$.", work="1.2cm"),
        Item(r"$\vec r(t) = \langle \sin t,\ t^3\rangle$. Find $\vec a(0)$.", selfcheck(r"\langle 0, 0\rangle"), r"$\langle -\sin t, 6t\rangle$ at $0$.", work="1.2cm"),
    ),
    Variants(
        MCQ(r"$\vec r(t) = \langle t^2 - 4t,\ 3 - t\rangle$. At $t = 1$ the particle is moving", [r"right and up", r"right and down", r"left and up", r"left and down"], "D", r"$\vec v(1) = \langle -2, -1\rangle$."),
        MCQ(r"$\vec r(t) = \langle t^3 - 3t,\ t^2\rangle$. At $t = 2$ the particle is moving", [r"right and up", r"right and down", r"left and up", r"left and down"], "A", r"$\vec v(2) = \langle 9, 4\rangle$."),
    ),
    Variants(
        Item(r"$\vec r(t) = \langle 2t + 1,\ t^2 - 4t\rangle$. When is the velocity horizontal?", num(2), r"$y' = 2t - 4 = 0$ at $t = 2$ (with $x' = 2 \ne 0$).", work="1.2cm"),
        Item(r"$\vec r(t) = \langle t^2 - 2t,\ 3t\rangle$. When is the velocity vertical?", num(1), r"$x' = 2t - 2 = 0$ at $t = 1$.", work="1.2cm"),
    ),
]

# ---------------------------------------------------------------- test prep
_m4 = float(sp.sqrt(sum(c**2 for c in at(vel([sp.exp(t) * sp.sin(t), t**2]), 1))).evalf())
MCQS = [
    MCQ(r"If $\vec r(t) = \langle t^2 - 1,\ e^{2t}\rangle$, then $\vec a(0) = $", [r"$\langle 2, 4\rangle$", r"$\langle 0, 2\rangle$", r"$\langle 2, 2\rangle$", r"$\langle -1, 1\rangle$"], "A", r"$\vec a = \langle 2, 4e^{2t}\rangle$.",
        why_not={"B": "that is $\\vec v(0)$", "D": "that is $\\vec r(0)$"}),
    MCQ(r"A particle has $\vec r(t) = \langle 3t^2,\ 4t^2\rangle$. Its speed at $t = 1$ is", [r"$5$", r"$7$", r"$10$", r"$14$"], "C", r"$\vec v(1) = \langle 6, 8\rangle$."),
    MCQ(r"$\vec r(t) = \langle t^3 - 12t,\ t^2\rangle$, $t > 0$. The particle is momentarily moving straight up when $t = $", [r"$1$", r"$\sqrt{12}$", r"$4$", r"$2$"], "D", r"$x' = 3t^2 - 12 = 0$ at $t = 2$, where $y' = 4 > 0$."),
    MCQ(r"A particle has $\vec r(t) = \langle e^t\sin t,\ t^2\rangle$. To three decimal places, its speed at $t = 1$ is", [rf"${_m4:.3f}$", r"$2.287$", r"$4.887$", r"$3.000$"], "A",
        rf"$\vec v(1) = \langle e(\sin 1 + \cos 1),\ 2\rangle$; speed $\approx {_m4:.3f}$.", calc=True),
]
close("m4", _m4, 4.255, 5e-4)

FRQS = []

TOPIC = Topic(
    number="9.4", title="Defining and Differentiating Vector-Valued Functions",
    unit="Unit 9: Parametric Equations, Polar Coordinates, and Vector-Valued Functions", ced=["CHA-3.H", "CHA-3.H.1", "CHA-3.H.2"],
    goals=r"Differentiate vector-valued functions to find velocity, acceleration, speed, and direction of motion.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
