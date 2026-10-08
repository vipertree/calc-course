"""Topic 9.5 (BC): Integrating vector-valued functions.

CED: FUN-8.A (FUN-8.A.1, FUN-8.A.2): integrate componentwise with a constant vector; the definite integral of velocity is
the displacement vector; r(t) = r(0) + integral of v. Lesson example: v = <2t, 3t^2>, r(0) = <1, -2>: r(2) = <5, 6>.
Worked examples: integral of <sin t, cos t> on [0, pi] (<2, 0>); a thrown ball (lands at t = 15/8, x = 75);
v = <e^t, 1/(t + 1)>, r(0) = <2, 0>: r(1) = <e + 1, ln 2>.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)

t = sp.symbols("t", real=True)


def integ(v, a, b):
    return [sp.simplify(sp.integrate(c, (t, a, b))) for c in v]


def pos(v, r0, s):
    return [sp.simplify(r + sp.integrate(c, (t, 0, s))) for c, r in zip(v, r0)]


def vec(v):
    return r"\langle " + ",\ ".join(sp.latex(c) for c in v) + r"\rangle"


same("lesson", [pos([2 * t, 3 * t**2], [1, -2], 2)], [[5, 6]])
same("ex", [integ([sp.sin(t), sp.cos(t)], 0, sp.pi), sp.solve(30 * t - 16 * t**2, t), pos([sp.exp(t), 1 / (t + 1)], [2, 0], 1)], [[2, 0], [0, sp.Rational(15, 8)], [sp.E + 1, sp.log(2)]])

NOTES = [
    Video("s9_5.py::Lesson", "Integrating vector functions", 4),

    Section("Componentwise"),
    Formula("Integrating a vector-valued function", (r"\[ \int \langle x(t), y(t)\rangle\,dt = \left\langle \int x(t)\,dt,\ \int y(t)\,dt\right\rangle + \blank{\langle C_1, C_2\rangle}. \]")),
    Formula("Displacement and position", (r"\[ \int_a^b \vec v(t)\,dt = \blank{\vec r(b) - \vec r(a)}, \qquad \vec r(t) = \blank{\vec r(0)} + \int_0^t \vec v(u)\,du. \] Velocity comes from acceleration the same way.")),
    VideoExample('Position from velocity', work="3.6cm"),
    BigIdea(r"Integrate each component; a starting point fixes the constant vector. $\int_a^b \vec v\,dt$ is the displacement vector."),
    Check(r"$\vec v(t) = \langle 1,\ 2t\rangle$, $\vec r(0) = \langle 0, 3\rangle$. Find $\vec r(t)$.", selfcheck(r"\langle t,\ t^2 + 3\rangle"), r"Integrate and match at $t = 0$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Evaluate $\int_0^1 \langle 3t^2,\ 4t\rangle\,dt$.", selfcheck(vec(integ([3 * t**2, 4 * t], 0, 1))), r"$\langle 1, 2\rangle$.", work="1.2cm"),
    Item(r"Evaluate $\int_0^{\pi/2} \langle \cos t,\ \sin 2t\rangle\,dt$.", selfcheck(vec(integ([sp.cos(t), sp.sin(2 * t)], 0, sp.pi / 2))), r"$\langle 1, 1\rangle$.", work="1.4cm"),
    Item(r"$\vec v(t) = \langle 6t,\ e^t\rangle$ and $\vec r(0) = \langle 1, 1\rangle$. Find $\vec r(t)$.", selfcheck(r"\langle 3t^2 + 1,\ e^t\rangle"), r"$\langle 3t^2 + C_1, e^t + C_2\rangle$; $C_1 = 1$, $C_2 = 0$.", work="1.6cm"),
    Item(r"$\vec v(t) = \langle 2t - 2,\ 3\rangle$ and $\vec r(0) = \langle 4, -1\rangle$. Find $\vec r(3)$.", selfcheck(vec(pos([2 * t - 2, 3], [4, -1], 3))), r"$\langle 4, -1\rangle + \langle 3, 9\rangle = \langle 7, 8\rangle$.", work="1.6cm"),
    Item(r"$\vec a(t) = \langle 2,\ 6t\rangle$, $\vec v(0) = \langle 1, 0\rangle$, $\vec r(0) = \langle 0, 0\rangle$. Find $\vec r(1)$.", selfcheck(r"\langle 2, 1\rangle"), r"$\vec v = \langle 2t + 1, 3t^2\rangle$; $\vec r = \langle t^2 + t, t^3\rangle$.", work="1.8cm"),
    Item(r"$\vec v(t) = \langle \frac{1}{t},\ 2t\rangle$ for $t \ge 1$ and $\vec r(1) = \langle 0, 0\rangle$. Find $\vec r(e)$.", selfcheck(r"\langle 1,\ e^2 - 1\rangle"), r"$\langle \ln t, t^2 - 1\rangle$ at $e$.", work="1.6cm"),
    Item(r"A particle has $\vec v(t) = \langle t^2,\ 4\rangle$. Find its displacement vector from $t = 0$ to $t = 3$.", selfcheck(vec(integ([t**2, 4], 0, 3))), r"$\langle 9, 12\rangle$.", work="1.2cm"),
    Item(r"A ball is thrown from $\langle 0, 12\rangle$ with velocity $\langle 20, 16\rangle$ ft/s and $\vec a = \langle 0, -32\rangle$. When does it hit the ground?", num(sp.Rational(3, 2)),
         r"$y = 12 + 16t - 16t^2 = 0$: $4t^2 - 4t - 3 = 0$, $(2t - 3)(2t + 1) = 0$, $t = \frac32$ (the other root is negative).", work="2cm"),
]
same("p", [pos([2 * t + 1, 3 * t**2], [0, 0], 1), integ([1 / t, 2 * t], 1, sp.E), [s for s in sp.solve(12 + 16 * t - 16 * t**2, t) if s > 0]], [[2, 1], [1, sp.E**2 - 1], [sp.Rational(3, 2)]])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Evaluate $\int_0^2 \langle t,\ 3t^2\rangle\,dt$.", selfcheck(r"\langle 2, 8\rangle"), r"$\left\langle \frac{t^2}{2}, t^3\right\rangle_0^2$.", work="1.2cm"),
        Item(r"Evaluate $\int_0^1 \langle 2t,\ e^t\rangle\,dt$.", selfcheck(r"\langle 1,\ e - 1\rangle"), r"$\langle t^2, e^t\rangle_0^1$.", work="1.2cm"),
        Item(r"Evaluate $\int_1^4 \langle \sqrt t,\ 1\rangle\,dt$.", selfcheck(r"\langle \tfrac{14}{3},\ 3\rangle"), r"$\left\langle \frac23 t^{3/2}, t\right\rangle_1^4$.", work="1.2cm"),
    ),
    Variants(
        Item(r"$\vec v(t) = \langle 2t,\ 1\rangle$, $\vec r(0) = \langle 3, 5\rangle$. Find $\vec r(2)$.", selfcheck(vec(pos([2 * t, 1], [3, 5], 2))), r"$\langle 3, 5\rangle + \langle 4, 2\rangle$.", work="1.4cm"),
        Item(r"$\vec v(t) = \langle 1,\ 4t^3\rangle$, $\vec r(0) = \langle -1, 2\rangle$. Find $\vec r(1)$.", selfcheck(vec(pos([1, 4 * t**3], [-1, 2], 1))), r"$\langle -1, 2\rangle + \langle 1, 1\rangle$.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"$\int_0^{\pi} \langle \cos t,\ \sin t\rangle\,dt = $", [r"$\langle 0, 0\rangle$", r"$\langle 2, 0\rangle$", r"$\langle 0, 2\rangle$", r"$\langle 0, -2\rangle$"], "C", r"$\int_0^\pi \cos t\,dt = 0$, $\int_0^\pi \sin t\,dt = 2$."),
        MCQ(r"$\int_0^{1} \langle 4t^3,\ 2\rangle\,dt = $", [r"$\langle 1, 2\rangle$", r"$\langle 4, 2\rangle$", r"$\langle 12, 0\rangle$", r"$\langle 1, 0\rangle$"], "A", r"$\langle t^4, 2t\rangle_0^1$."),
    ),
    Variants(
        Item(r"$\vec a(t) = \langle 0,\ -10\rangle$, $\vec v(0) = \langle 5, 20\rangle$. Find $\vec v(t)$ and the time when the vertical velocity is $0$.", selfcheck(r"\langle 5,\ 20 - 10t\rangle;\ t = 2"), r"Integrate and match.", work="1.6cm"),
        Item(r"$\vec a(t) = \langle 2,\ 0\rangle$, $\vec v(0) = \langle -4, 3\rangle$. When is the horizontal velocity $0$?", num(2), r"$\vec v = \langle 2t - 4, 3\rangle$.", work="1.6cm"),
    ),
    Variants(
        MCQ(r"If $\vec v(t)$ is a particle's velocity, $\int_1^3 \vec v(t)\,dt$ is", [r"its speed at $t = 3$", r"the distance it travels", r"its displacement vector from $t = 1$ to $t = 3$", r"its position at $t = 3$"], "C", r"$\vec r(3) - \vec r(1)$.", why_not={"B": "distance uses the speed, not the velocity vector"}),
    ),
]

# ---------------------------------------------------------------- test prep
_r = [float(sp.Integral(sp.sqrt(t + 1), (t, 0, 3)).evalf()) + 1, float(sp.Integral(sp.sin(t**2), (t, 0, 3)).evalf()) + 2]
MCQS = [
    MCQ(r"A particle has $\vec v(t) = \langle 3t^2,\ 2t\rangle$ and $\vec r(1) = \langle 2, 0\rangle$. Then $\vec r(2) = $", [r"$\langle 9, 3\rangle$", r"$\langle 8, 4\rangle$", r"$\langle 7, 3\rangle$", r"$\langle 10, 4\rangle$"], "A",
        r"$\langle 2, 0\rangle + \int_1^2 \langle 3t^2, 2t\rangle\,dt = \langle 2, 0\rangle + \langle 7, 3\rangle$.", why_not={"C": "the displacement only"}),
    MCQ(r"$\vec a(t) = \langle 6t,\ -2\rangle$, $\vec v(0) = \langle 0, 4\rangle$, $\vec r(0) = \langle 1, 0\rangle$. Then $\vec r(1) = $", [r"$\langle 1, 3\rangle$", r"$\langle 2, 3\rangle$", r"$\langle 2, 4\rangle$", r"$\langle 3, 2\rangle$"], "B",
        r"$\vec v = \langle 3t^2, 4 - 2t\rangle$; $\vec r = \langle t^3 + 1, 4t - t^2\rangle$."),
    MCQ(r"$\int_0^{\ln 2} \langle e^t,\ e^{2t}\rangle\,dt = $", [r"$\langle 2, 4\rangle$", r"$\langle 1, 3\rangle$", r"$\langle 2, 2\rangle$", r"$\langle 1, \frac32\rangle$"], "D", r"$\langle e^t, \frac12e^{2t}\rangle_0^{\ln 2} = \langle 1, \frac32\rangle$."),
    MCQ(r"A particle has $\vec v(t) = \langle \sqrt{t + 1},\ \sin(t^2)\rangle$ and $\vec r(0) = \langle 1, 2\rangle$. To three decimal places, $\vec r(3) = $", [rf"$\langle {_r[0] - 1:.3f},\ {_r[1] - 2:.3f}\rangle$", r"$\langle 2.000,\ 2.412\rangle$",
        rf"$\langle {_r[0]:.3f},\ {_r[1]:.3f}\rangle$", rf"$\langle {_r[0]:.3f},\ {_r[1] - 2:.3f}\rangle$"], "C", rf"$\langle 1, 2\rangle + \int_0^3 \vec v\,dt \approx \langle {_r[0]:.3f}, {_r[1]:.3f}\rangle$.", why_not={"A": "the displacement only"}, calc=True),
]
same("m", [pos([3 * t**2, 2 * t], [0, 0], 2), integ([3 * t**2, 2 * t], 1, 2), integ([sp.exp(t), sp.exp(2 * t)], 0, sp.log(2))], [[8, 4], [7, 3], [1, sp.Rational(3, 2)]])
close("m4", _r[0], 1 + sp.Rational(14, 3), 1e-6)

FRQS = []

TOPIC = Topic(
    number="9.5", title="Integrating Vector-Valued Functions",
    unit="Unit 9: Parametric Equations, Polar Coordinates, and Vector-Valued Functions", ced=["FUN-8.A", "FUN-8.A.1", "FUN-8.A.2"],
    goals=r"Integrate vector-valued functions componentwise and recover position from velocity and a starting point.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
