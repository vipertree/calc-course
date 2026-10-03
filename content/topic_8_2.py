"""Topic 8.2: Connecting position, velocity, and acceleration of functions using integrals.

CED: CHA-4.C (CHA-4.C.1, CHA-4.C.2): displacement is the integral of velocity; total distance is the integral of speed
|v|; position s(t) = s(0) + integral of v; velocity v(t) = v(0) + integral of a. Without a calculator, total distance
splits where v changes sign (a sign chart every time). Lesson example: v = t^2 - 6t + 8 on [0, 5], s(0) = 1.
Worked examples: from a velocity graph made of segments, from acceleration, working backward to s(0).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)
from calclib.figs import graph

t = sp.symbols("t", real=True)


def I(f, a, b):
    return sp.integrate(f, (t, a, b))


def dist(v, a, b):
    """Total distance: split at the real zeros of v inside (a, b)."""
    cuts = sorted({a, b} | {r for r in sp.solve(v, t) if r.is_real and a < r < b})
    return sum(abs(I(v, p, q)) for p, q in zip(cuts, cuts[1:]))


v0 = t**2 - 6 * t + 8
same("lesson", [I(v0, 0, 5), 1 + I(v0, 0, 5), dist(v0, 0, 5)], [sp.Rational(20, 3), sp.Rational(23, 3), sp.Rational(28, 3)])
same("ex2", [dist(3 * t**2 - 3, 0, 2)], [6])
same("ex3", [5 - I(3 * t**2 - 2, 0, 2)], [1])

FIG_V = graph("t8_2_v", [("-2*x", 0, 1), ("-2+0*x", 1, 3), ("-2+2*(x-3)", 3, 6)], (0, 6.5), (-3, 5), xlabel="t", ylabel="v(t)",
              caption=r"The velocity of a particle, $0 \le t \le 6$: three segments.")
same("fig", [-1 - 4 - 1, sp.Rational(1, 2) * 2 * 4], [-6, 4])

NOTES = [
    Video("s8_2.py::Lesson", "Motion with integrals", 6),

    Section("Displacement and position"),
    Formula("Displacement", (r"Since $s' = v$, the Fundamental Theorem gives \[ \int_a^b v(t)\,dt = \blank{s(b) - s(a)}, \] the net change in position. Area below the axis counts as backward motion and cancels.")),
    Formula("Position and velocity from a starting value", (
        r"\[ s(t) = \blank{s(0)} + \int_0^t v(u)\,du, \qquad v(t) = v(0) + \blank{\int_0^t a(u)\,du}. \] Where you start, plus the net change since.")),
    Section("Total distance"),
    Formula("Total distance", (r"\[ \text{total distance} = \blank{\int_a^b |v(t)|\,dt}. \] Without a calculator, find where $v$ changes sign, split the interval there, and add the pieces as positive numbers.")),
    Text(r"Make a sign chart for $v$ every time: the zeros of $v$ cut $[a, b]$ into pieces, one test value per piece."),
    VideoExample('Displacement and distance', work="4.6cm"),
    BigIdea(r"$\int v\,dt$ is displacement (it can cancel); $\int |v|\,dt$ is total distance (it never cancels). Position is the start plus the integral of velocity."),
    Check(r"$v(t) = 2t - 4$ on $[0, 3]$. Find the displacement and the total distance.", selfcheck(r"-3 \text{ and } 5"), r"$\int_0^3 = 9 - 12 = -3$. Split at $2$: $4 + 1 = 5$."),
]

# ---------------------------------------------------------------- practice
# the calculator item's key, computed numerically
_vt = lambda s: s * sp.exp(-s / 2) - sp.Rational(2, 5)
_roots = sorted(float(sp.nsolve(_vt(t), t, g)) for g in (0.6, 4.3))
_cuts = [0.0] + _roots + [6.0]
_d = sum(abs(float(sp.Integral(_vt(t), (t, p, q)).evalf())) for p, q in zip(_cuts, _cuts[1:]))
PRACTICE = [
    Item(r"$v(t) = 3t^2 - 2t$ for $0 \le t \le 2$. Find the displacement.", num(I(3 * t**2 - 2 * t, 0, 2)), r"$\left[t^3 - t^2\right]_0^2 = 4$.", work="1.4cm"),
    Item(r"$v(t) = t - 3$ for $0 \le t \le 5$. Find the total distance.", num(dist(t - 3, 0, 5)), r"Split at $3$: $\frac92 + 2 = \frac{13}{2}$.", work="1.8cm"),
    Item(r"$v(t) = t^2 - 4$ for $0 \le t \le 3$, and $s(0) = 2$. Find $s(3)$.", num(2 + I(t**2 - 4, 0, 3)), r"$2 + (9 - 12) = -1$.", work="1.4cm"),
    Item(r"$v(t) = t^2 - 4$ for $0 \le t \le 3$. Find the total distance.", num(dist(t**2 - 4, 0, 3)), r"Split at $2$: $\left|\frac83 - 8\right| + \left|(-3) - \left(-\frac{16}{3}\right)\right| = \frac{16}{3} + \frac73 = \frac{23}{3}$.", work="2.2cm"),
    Item(r"$a(t) = 4 - 2t$ and $v(0) = 1$. Find $v(3)$.", num(1 + I(4 - 2 * t, 0, 3)), r"$1 + (12 - 9) = 4$.", work="1.4cm"),
    Item(r"$v(t) = \cos t$ for $0 \le t \le \pi$. Find the displacement and the total distance.", selfcheck(r"0 \text{ and } 2"), r"$\int_0^\pi \cos t\,dt = 0$; split at $\frac\pi2$: $1 + 1 = 2$.", work="1.8cm"),
    Item(r"The graph of $v$ is shown. Find the displacement on $[0, 6]$.", num(-2), r"Below: $1 + 4 + 1 = 6$; above: $4$. $4 - 6 = -2$.", work="1.6cm", figure=FIG_V),
    Item(r"Using the same graph, find the total distance on $[0, 6]$.", num(10), r"$6 + 4 = 10$.", work="1.2cm"),
    Item(r"$v(t) = 6t^2 - 6$ and $s(1) = 3$. Find $s(0)$.", num(3 - I(6 * t**2 - 6, 0, 1)), r"$3 = s(0) + (2 - 6)$, so $s(0) = 7$.", work="1.6cm"),
    Item(r"A particle has $a(t) = 6t - 6$, $v(0) = 3$, $s(0) = 0$. Find $s(2)$.", num(I(3 * t**2 - 6 * t + 3, 0, 2)), r"$v = 3t^2 - 6t + 3$; $s(2) = \left[t^3 - 3t^2 + 3t\right]_0^2 = 2$.", work="2cm"),
    Item(r"$v(t) = te^{-t/2} - 0.4$. Use a calculator to find the total distance traveled on $0 \le t \le 6$.", num(sp.Float(round(_d, 4)), tol=2e-3),
         rf"$\int_0^6 |v(t)|\,dt \approx {_d:.3f}$.", work="1.6cm", calc=True),
]
# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"$v(t) = 4t^3$ on $[0, 2]$. Find the displacement.", num(16), r"$\left[t^4\right]_0^2$.", work="1cm"),
        Item(r"$v(t) = 6t - 3t^2$ on $[0, 3]$. Find the displacement.", num(I(6 * t - 3 * t**2, 0, 3)), r"$27 - 27 = 0$.", work="1cm"),
        Item(r"$v(t) = e^t$ on $[0, \ln 4]$. Find the displacement.", num(3), r"$4 - 1$.", work="1cm"),
    ),
    Variants(
        Item(r"$v(t) = 2t - 6$ on $[0, 5]$. Find the total distance.", num(dist(2 * t - 6, 0, 5)), r"Split at $3$: $9 + 4 = 13$.", work="1.6cm"),
        Item(r"$v(t) = 3 - t$ on $[0, 4]$. Find the total distance.", num(dist(3 - t, 0, 4)), r"Split at $3$: $\frac92 + \frac12 = 5$.", work="1.6cm"),
        Item(r"$v(t) = t^2 - 1$ on $[0, 2]$. Find the total distance.", num(dist(t**2 - 1, 0, 2)), r"Split at $1$: $\frac23 + \frac43 = 2$.", work="1.6cm"),
    ),
    Variants(
        Item(r"$v(t) = 3t^2 + 1$ and $s(0) = 4$. Find $s(2)$.", num(4 + I(3 * t**2 + 1, 0, 2)), r"$4 + 10$.", work="1.2cm"),
        Item(r"$v(t) = \sin t$ and $s(0) = 1$. Find $s(\pi)$.", num(3), r"$1 + 2$.", work="1.2cm"),
        Item(r"$v(t) = 2t$ and $s(3) = 10$. Find $s(1)$.", num(10 - I(2 * t, 1, 3)), r"$10 - 8 = 2$.", work="1.2cm"),
    ),
    Variants(
        Item(r"$a(t) = 2$ and $v(0) = -4$. When does the particle change direction?", num(2), r"$v = -4 + 2t = 0$ at $t = 2$ (sign changes).", work="1.2cm"),
        Item(r"$a(t) = 6t$ and $v(0) = -12$. When does the particle change direction ($t > 0$)?", num(2), r"$v = 3t^2 - 12 = 0$ at $t = 2$.", work="1.2cm"),
        Item(r"$a(t) = -4$ and $v(0) = 10$. When does the particle change direction?", num(sp.Rational(5, 2)), r"$v = 10 - 4t = 0$ at $t = \frac52$.", work="1.2cm"),
    ),
    Variants(
        MCQ(r"Which expression gives the total distance traveled on $[0, 6]$ by a particle with velocity $v(t)$?", [r"$\int_0^6 v(t)\,dt$", r"$\left|\int_0^6 v(t)\,dt\right|$", r"$\int_0^6 |v(t)|\,dt$", r"$v(6) - v(0)$"], "C",
            r"Integrate speed.", why_not={"B": "the size of the displacement"}),
        MCQ(r"Which expression gives the position at $t = 4$ of a particle with velocity $v(t)$ and $s(0) = 3$?", [r"$3 + \int_0^4 v(t)\,dt$", r"$\int_0^4 v(t)\,dt$", r"$3 + v(4)$", r"$3 + \int_0^4 |v(t)|\,dt$"], "A",
            r"Start plus net change."),
    ),
]

# ---------------------------------------------------------------- test prep
_v4 = lambda s: sp.sqrt(s) * sp.cos(s)
_r4 = [0.0, float(sp.pi / 2), float(3 * sp.pi / 2), 5.0]
_d4 = sum(abs(float(sp.Integral(_v4(t), (t, p, q)).evalf())) for p, q in zip(_r4, _r4[1:]))
close("m4", _d4, 4.318, 5e-3)
MCQS = [
    MCQ(r"A particle moves with $v(t) = t^2 - 2t$ for $0 \le t \le 3$. The total distance traveled is", [r"$0$", r"$\frac43$", r"$\frac83$", r"$\frac{8}{3}$ to the left"], "C",
        r"Split at $2$: $\frac43 + \frac43 = \frac83$.", why_not={"A": "the displacement"}),
    MCQ(r"$a(t) = 12t^2$, $v(0) = 0$ and $s(0) = 5$. Then $s(1) = $", [r"$6$", r"$9$", r"$17$", r"$1$"], "A", r"$v = 4t^3$, $s(1) = 5 + 1 = 6$."),
    MCQ(r"The velocity of a car, in feet per second, is positive on $[0, 10]$. Which gives the average velocity over $[0, 10]$?", [r"$\frac{v(10) - v(0)}{10}$", r"$\frac{1}{10}\int_0^{10} v'(t)\,dt$",
        r"$\int_0^{10} v(t)\,dt$", r"$\frac{1}{10}\int_0^{10} v(t)\,dt$"], "D", r"Average value of $v$: displacement over time."),
    MCQ(r"A particle has $v(t) = \sqrt t\cos t$. To three decimal places, the total distance traveled on $0 \le t \le 5$ is", [r"$2.728$", r"$4.318$", r"$3.142$", r"$-2.728$"], "B",
        rf"$\int_0^5 |v(t)|\,dt \approx {_d4:.3f}$.", why_not={"D": "the displacement", "A": "the size of the displacement"}, calc=True),
]
same("m1", [dist(t**2 - 2 * t, 0, 3), 5 + I(4 * t**3, 0, 1)], [sp.Rational(8, 3), 6])

# ---------------------------------------------------------------- FRQ
vF = t**2 - 5 * t + 4
same("frq", [vF.subs(t, 2), sp.diff(vF, t).subs(t, 2), dist(vF, 0, 5), 3 + I(vF, 0, 5)], [-2, -1, sp.Rational(49, 6), sp.Rational(13, 6)])
FRQS = [
    FRQ("A particle on a line", (r"A particle moves along the $x$-axis with velocity $v(t) = t^2 - 5t + 4$ for $0 \le t \le 5$. At $t = 0$ the particle is at $x = 3$."), [
        Part("a", r"Is the speed of the particle increasing or decreasing at $t = 2$? Give a reason for your answer.", selfcheck(r"\text{increasing}"),
             r"$v(2) = -2 < 0$ and $a(2) = 2(2) - 5 = -1 < 0$. Same sign, so the speed is increasing.", [(1, "$v(2)$ and $a(2)$"), (1, "increasing with reason")], work="2cm"),
        Part("b", r"Find all times $t$, $0 < t < 5$, at which the particle changes direction. Justify your answer.", selfcheck(r"t = 1 \text{ and } t = 4"),
             r"$v(t) = (t - 1)(t - 4)$ changes sign at $t = 1$ (from $+$ to $-$) and at $t = 4$ (from $-$ to $+$).", [(1, "both times"), (1, "sign-change justification")], work="2cm"),
        Part("c", r"Find the total distance traveled by the particle for $0 \le t \le 5$.", num(sp.Rational(49, 6)),
             r"$\int_0^1 v = \frac{11}{6}$, $\int_1^4 v = -\frac92$, $\int_4^5 v = \frac{11}{6}$. Distance $= \frac{11}{6} + \frac92 + \frac{11}{6} = \frac{49}{6}$.",
             [(1, "splits at turning points"), (1, "integrals"), (1, "answer")], work="3cm"),
        Part("d", r"Find the position of the particle at $t = 5$.", num(sp.Rational(13, 6)), r"$3 + \int_0^5 v(t)\,dt = 3 - \frac56 = \frac{13}{6}$.", [(1, "answer")], work="1.6cm"),
    ], frq_type="Particle motion"),
]
same("frq pieces", [I(vF, 0, 1), I(vF, 1, 4), I(vF, 4, 5)], [sp.Rational(11, 6), -sp.Rational(9, 2), sp.Rational(11, 6)])

TOPIC = Topic(
    number="8.2", title="Connecting Position, Velocity, and Acceleration of Functions Using Integrals",
    unit="Unit 8: Applications of Integration", ced=["CHA-4.C", "CHA-4.C.1", "CHA-4.C.2"],
    goals=r"Use integrals of velocity and acceleration to find displacement, total distance, position, and velocity.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
