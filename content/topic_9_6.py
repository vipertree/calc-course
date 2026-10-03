"""Topic 9.6 (BC): Solving motion problems using parametric and vector-valued functions.

CED: CHA-4.D/CHA-4.E (plane motion): position = start + integral of each velocity component; speed = sqrt(x'^2 + y'^2);
distance traveled = integral of speed; slope y'/x'; direction from the signs of x', y'; at rest when both are 0.
Lesson example: x' = 2t - 4, y' = 3t^2, start (1, 0): speed sqrt 13 at t = 1, left on (0, 2), position (-3, 8) at t = 2,
distance 10.468. Worked examples: a calculator drone problem; slope and tangent line; at rest at t = 2.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Table, Text, Topic, Variants, Video, close, num, same, selfcheck)

t = sp.symbols("t", real=True)
NI = lambda f, a, b: float(sp.Integral(f, (t, a, b)).evalf())


def speed(xp, yp):
    return sp.sqrt(xp**2 + yp**2)


same("lesson", [speed(2 * t - 4, 3 * t**2).subs(t, 1), 1 + sp.integrate(2 * t - 4, (t, 0, 2)), sp.integrate(3 * t**2, (t, 0, 2))], [sp.sqrt(13), -3, 8])
close("lesson d", NI(speed(2 * t - 4, 3 * t**2), 0, 2), 10.468, 5e-4)
close("ex1", 3 + NI(sp.cos(t**2), 0, 2), 3.461, 5e-4)
close("ex1c", NI(speed(sp.cos(t**2), sp.exp(t / 2)), 0, 2), 3.828, 5e-4)

NOTES = [
    Video("s9_6.py::Lesson", "Motion in the plane", 5),

    Section("The toolkit"),
    Table(r"position at $t = b$ & $x(b) = x(a) + \int_a^b x'(t)\,dt$, and the same for $y$ \\ velocity vector & $\langle x'(t),\ y'(t)\rangle$ \\ speed & $\sqrt{(x')^2 + (y')^2}$ \\ distance traveled & $\int_a^b \sqrt{(x')^2 + (y')^2}\,dt$ \\ slope of the path & $\frac{dy}{dx} = \frac{y'}{x'}$ \\ moving left / right & $x' < 0$ / $x' > 0$ \\ moving down / up & $y' < 0$ / $y' > 0$ \\ at rest & $x' = 0$ and $y' = 0$ ", "ll", header=r"want & tool"),
    Formula("Distance versus displacement", (r"Distance traveled $= \blank{\int_a^b \sqrt{(x')^2 + (y')^2}\,dt}$. Displacement is the change in position $\langle x(b) - x(a),\ y(b) - y(a)\rangle$; its length is the straight-line distance, usually less.")),
    VideoExample('A full motion problem', work="5cm"),
    BigIdea(r"Each component separately for position; Pythagoras for speed; integrate speed for distance; divide for slope; signs for direction."),
    Check(r"$x'(t) = 3$, $y'(t) = 4$. Find the speed and the distance traveled in $2$ seconds.", selfcheck(r"5;\ 10"), r"$\sqrt{9 + 16} = 5$; $5 \cdot 2$."),
]

# ---------------------------------------------------------------- practice
_p5 = NI(speed(sp.exp(t), 2 * t), 0, 1)
_p8 = (1 + NI(sp.sin(t**2), 0, 1), 2 + NI(sp.sqrt(1 + t**3), 0, 1))
PRACTICE = [
    Item(r"$x'(t) = 6t$, $y'(t) = 8t$. Find the speed at $t = 2$.", num(20), r"$\langle 12, 16\rangle$: $20$.", work="1.2cm"),
    Item(r"$x'(t) = t^2 - 1$, $y'(t) = 2t$, and the particle is at $(0, 3)$ at $t = 0$. Find its position at $t = 3$.", selfcheck(r"(6,\ 12)"), r"$x = 0 + (9 - 3) = 6$; $y = 3 + 9 = 12$.", work="1.6cm"),
    Item(r"$x'(t) = t^2 - 4t$, $y'(t) = t + 1$. For which $t > 0$ is the particle moving left?", selfcheck(r"0 < t < 4"), r"$x' = t(t - 4) < 0$ on $(0, 4)$.", work="1.2cm"),
    Item(r"$x'(t) = 2t$, $y'(t) = 3t^2 - 3$. Find the slope of the path at $t = 2$.", num(sp.Rational(9, 4)), r"$\frac{y'}{x'} = \frac{9}{4}$.", work="1.2cm"),
    Item(r"Use a calculator: $x'(t) = e^t$, $y'(t) = 2t$. Find the distance traveled for $0 \le t \le 1$.", num(sp.Float(round(_p5, 4)), tol=2e-3), rf"$\int_0^1 \sqrt{{e^{{2t}} + 4t^2}}\,dt \approx {_p5:.3f}$.", work="1.4cm", calc=True),
    Item(r"$x'(t) = \cos t$, $y'(t) = \sin t$, start $(0, 0)$. Find the position at $t = \pi$ and the distance traveled for $0 \le t \le \pi$.", selfcheck(r"(0, 2);\ \pi"), r"Position $\langle \sin\pi, 1 - \cos\pi\rangle = (0, 2)$; speed $1$, distance $\pi$.", work="1.8cm"),
    Item(r"$x'(t) = t - 3$, $y'(t) = t^2 - 9$, $t \ge 0$. When is the particle at rest?", num(3), r"Both are $0$ only at $t = 3$.", work="1.2cm"),
    Item(r"Use a calculator: $x'(t) = \sin(t^2)$, $y'(t) = \sqrt{1 + t^3}$, and the particle is at $(1, 2)$ at $t = 0$. Find its position at $t = 1$.", selfcheck(rf"({_p8[0]:.3f},\ {_p8[1]:.3f})"),
         rf"$x(1) = 1 + \int_0^1 \sin(t^2)\,dt \approx {_p8[0]:.3f}$; $y(1) = 2 + \int_0^1 \sqrt{{1 + t^3}}\,dt \approx {_p8[1]:.3f}$.", work="1.8cm", calc=True),
]

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"$x'(t) = 3t$, $y'(t) = 4t$. Find the speed at $t = 1$.", num(5), r"$5$.", work="1cm"),
        Item(r"$x'(t) = 5$, $y'(t) = 12t$. Find the speed at $t = 1$.", num(13), r"$13$.", work="1cm"),
    ),
    Variants(
        Item(r"$x'(t) = 2t$, $y'(t) = 1$, start $(1, 1)$ at $t = 0$. Find the position at $t = 2$.", selfcheck(r"(5, 3)"), r"$(1 + 4, 1 + 2)$.", work="1.4cm"),
        Item(r"$x'(t) = 3t^2$, $y'(t) = -2$, start $(0, 4)$ at $t = 0$. Find the position at $t = 1$.", selfcheck(r"(1, 2)"), r"$(0 + 1, 4 - 2)$.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"$x'(t) = t - 2$, $y'(t) = t^2 - 1$. At $t = \frac12$ the particle is moving", [r"right and up", r"right and down", r"left and up", r"left and down"], "D", r"$x' = -\frac32 < 0$, $y' = -\frac34 < 0$."),
        MCQ(r"$x'(t) = t - 2$, $y'(t) = t^2 - 1$. At $t = 1.5$ the particle is moving", [r"right and up", r"right and down", r"left and up", r"left and down"], "C", r"$x' = -\frac12 < 0$, $y' = \frac54 > 0$."),
    ),
    Variants(
        MCQ(r"Which gives the distance traveled for $0 \le t \le 3$ by a particle with velocity $\langle x'(t), y'(t)\rangle$?", [r"$\sqrt{x(3)^2 + y(3)^2}$", r"$\int_0^3 \left(x'(t) + y'(t)\right) dt$", r"$\int_0^3 \sqrt{x'(t)^2 + y'(t)^2}\,dt$",
            r"$\sqrt{\left(\int_0^3 x'\,dt\right)^2 + \left(\int_0^3 y'\,dt\right)^2}$"], "C", r"Integrate the speed.", why_not={"D": "the straight-line distance between the endpoints"}),
    ),
    Variants(
        Item(r"$x'(t) = t^2 - 4$, $y'(t) = 2t - 4$. When is the particle at rest?", num(2), r"Both $0$ at $t = 2$.", work="1.2cm"),
        Item(r"$x'(t) = t^2 - 1$, $y'(t) = t - 2$. Is the particle ever at rest?", selfcheck(r"\text{no}"), r"$x' = 0$ at $t = \pm1$, where $y' \ne 0$.", work="1.2cm"),
    ),
]

# ---------------------------------------------------------------- test prep
_m4 = NI(speed(sp.sqrt(t), sp.cos(t)), 0, 3)
MCQS = [
    MCQ(r"A particle has $x'(t) = 4t - 2$ and $y'(t) = 3$, and is at $(2, -1)$ when $t = 0$. Its position at $t = 2$ is", [r"$(6, 5)$", r"$(4, 6)$", r"$(6, 6)$", r"$(4, 5)$"], "A", r"$x = 2 + (8 - 4)$, $y = -1 + 6$."),
    MCQ(r"A particle has $x'(t) = e^t$ and $y'(t) = e^{-t}$. Its speed at $t = 0$ is", [r"$1$", r"$\sqrt2$", r"$2$", r"$0$"], "B", r"$\sqrt{1 + 1}$."),
    MCQ(r"For which $t > 0$ does the particle with $x'(t) = t^2 - 9$, $y'(t) = t + 1$ move to the left?", [r"$t > 3$", r"$t > 0$", r"$0 < t < 9$", r"$0 < t < 3$"], "D", r"$x' < 0$ for $0 < t < 3$."),
    MCQ(r"A particle has $x'(t) = \sqrt t$ and $y'(t) = \cos t$. To three decimal places, the distance it travels for $0 \le t \le 3$ is", [r"$3.464$", rf"${_m4:.3f}$", r"$2.987$", r"$5.196$"], "B", rf"$\int_0^3 \sqrt{{t + \cos^2 t}}\,dt \approx {_m4:.3f}$.", calc=True),
]
close("m4", _m4, 4.121, 5e-4)
close("frq d", _d, 9.614, 5e-4)

# ---------------------------------------------------------------- FRQ
xp, yp = t**2 - 3 * t, sp.sqrt(t + 1)
_d = NI(speed(xp, yp), 0, 4)
_y4 = -1 + sp.integrate(yp, (t, 0, 4))
same("frq", [speed(xp, yp).subs(t, 2), [sp.diff(xp, t).subs(t, 2), sp.simplify(sp.diff(yp, t).subs(t, 2))], sp.simplify((yp / xp).subs(t, 2)), 2 + sp.integrate(xp, (t, 0, 4)), sp.simplify(_y4 - (-1 + sp.Rational(2, 3) * (5 * sp.sqrt(5) - 1)))],
     [sp.sqrt(7), [1, sp.sqrt(3) / 6], -sp.sqrt(3) / 2, -sp.Rational(2, 3), 0])
FRQS = [
    FRQ("Motion in the plane", (r"A particle moves in the $xy$-plane so that $\frac{dx}{dt} = t^2 - 3t$ and $\frac{dy}{dt} = \sqrt{t + 1}$ for $t \ge 0$. At $t = 0$ the particle is at $(2, -1)$."), [
        Part("a", r"Find the speed of the particle at $t = 2$, and its acceleration vector at $t = 2$.", selfcheck(r"\sqrt7;\ \left\langle 1,\ \tfrac{\sqrt3}{6}\right\rangle"),
             r"$\langle x'(2), y'(2)\rangle = \langle -2, \sqrt3\rangle$, speed $\sqrt{4 + 3} = \sqrt7$. $\vec a(t) = \left\langle 2t - 3,\ \frac{1}{2\sqrt{t + 1}}\right\rangle$, so $\vec a(2) = \left\langle 1, \frac{1}{2\sqrt3}\right\rangle$.",
             [(1, "speed"), (1, "acceleration vector")], work="2.6cm"),
        Part("b", r"Find the slope of the line tangent to the path of the particle at $t = 2$. Is the particle moving to the left or to the right at $t = 2$?", selfcheck(r"-\tfrac{\sqrt3}{2};\ \text{left}"),
             r"$\frac{dy}{dx} = \frac{\sqrt3}{-2}$. $x'(2) = -2 < 0$: moving left.", [(1, "slope"), (1, "left with reason")], work="1.8cm"),
        Part("c", r"Find the position of the particle at $t = 4$.", selfcheck(r"\left(-\tfrac23,\ -1 + \tfrac23\left(5\sqrt5 - 1\right)\right)"),
             r"$x(4) = 2 + \int_0^4 (t^2 - 3t)\,dt = 2 + \left(\frac{64}{3} - 24\right) = -\frac23$. $y(4) = -1 + \int_0^4 \sqrt{t + 1}\,dt = -1 + \frac23\left(5^{3/2} - 1\right) \approx 5.787$.",
             [(1, "$x(4)$"), (1, "$y(4)$")], work="2.6cm"),
        Part("d", r"Find the total distance traveled by the particle for $0 \le t \le 4$.", num(sp.Float(round(_d, 4)), tol=2e-3),
             rf"$\int_0^4 \sqrt{{(t^2 - 3t)^2 + t + 1}}\,dt \approx {_d:.3f}$.", [(1, "integral"), (1, "answer")], work="1.8cm", ),
    ], frq_type="Parametric / vector motion", calc=True),
]

TOPIC = Topic(
    number="9.6", title="Solving Motion Problems Using Parametric and Vector-Valued Functions",
    unit="Unit 9: Parametric Equations, Polar Coordinates, and Vector-Valued Functions", ced=["CHA-4.E", "CHA-4.E.1"],
    goals=r"Solve plane-motion problems: position, velocity, speed, distance traveled, slope, and direction.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
