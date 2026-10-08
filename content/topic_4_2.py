"""Topic 4.2: Straight-line motion: connecting position, velocity, and acceleration.

CED: CHA-3.B (CHA-3.B.1, CHA-3.B.2): v = x', a = v' = x''; direction from the sign of v; speed |v|; speeding up when v and a
share a sign. Total distance appears once, as the quick method from position at the turning points; AP free response
expects the integral of |v| (Topic 8.2), so practice and test prep do not drill the turning-point method.
Running example (matches the worked examples): x(t) = t^3 - 6t^2 + 9t, at rest at t = 1 and 3, total distance on [0, 4] is 12.
"""
import sympy as sp

from calclib import (FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Table, Text, Topic, Variants, Video, expr, num,
                     same, selfcheck)
from calclib.figs import graph

t = sp.symbols("t")


def V(xt):
    return sp.diff(xt, t)


def A(xt):
    return sp.diff(xt, t, 2)


def dist(xt, a, b):
    """Total distance on [a, b] from position at the turning points."""
    pts = sorted({a, b, *[r for r in sp.solve(V(xt), t) if r.is_real and a < r < b]})
    return sum(abs(xt.subs(t, q) - xt.subs(t, p)) for p, q in zip(pts, pts[1:]))


X = t**3 - 6 * t**2 + 9 * t
same("rest", sorted(sp.solve(V(X), t)), [1, 3])
same("dist", [dist(X, 0, 4), X.subs(t, 4) - X.subs(t, 0)], [12, 4])

FIG = graph("t4_2_x", [("x^3-6*x^2+9*x", 0, 4.2)], xr=(0, 4.5), yr=(-1, 6), closed=[(1, 4), (3, 0)], xlabel="t", ylabel="x(t)",
            caption=r"Position $x(t) = t^3 - 6t^2 + 9t$. The graph is not the path: the particle moves along a line, back and forth.")

NOTES = [
    Video("s4_2.py::Lesson", "Motion on a line", 5),

    Section("Position, velocity, acceleration"),
    Formula("Position, velocity, acceleration", (
        r"$x(t)$: \textbf{position}, in meters (you may also see $s(t)$ or $y(t)$) \par "
        r"$v(t) = x'(t)$: \textbf{velocity}, the rate of change of position, in meters per second \par "
        r"$a(t) = v'(t)$: \textbf{acceleration}, the rate of change of velocity, in meters per second per second. "
        r"Since $v = x'$, also $a(t) = x''(t)$.")),
    Text(r"A particle moving along a line has a direction at every moment, and it comes from the \blank{sign} of the velocity: "
         r"$v(t) > 0$ means moving right (or up), $v(t) < 0$ means moving left (or down), and $v(t) = 0$ means \blank{at rest}."),
    FIG,
    Example("Where is it moving left?", (
        r"For $x(t) = t^3 - 6t^2 + 9t$, $t \ge 0$, find where the particle moves right and where it moves left."), (
        r"Moving right means $v(t) > 0$; moving left means $v(t) < 0$. "
        r"\[ v(t) = 3t^2 - 12t + 9 = 3(t^2 - 4t + 3) = 3(t - 1)(t - 3). \] "
        r"$v(t) = 0$ when $t - 1 = 0$ or $t - 3 = 0$: $t = 1$ or $t = 3$. "
        r"$v$ is a polynomial, so it is continuous and can change sign only at its zeros: one test value per section is enough. "
        r"\[ \begin{array}{l|ccc} & 0 < t < 1 & 1 < t < 3 & t > 3 \\ \hline \text{test} & v(0) = 9 & v(2) = -3 & v(4) = 9 \\ "
        r"3 & + & + & + \\ t - 1 & - & + & + \\ t - 3 & - & - & + \\ \hline v(t) & + & - & + \\ \text{motion} & \text{right} & \text{left} & \text{right} "
        r"\end{array} \] Both methods agree: right on $(0, 1)$, left on $(1, 3)$, right after $3$, at rest at $t = 1$ and $t = 3$."), work="5cm"),

    Section("Speed, and speeding up"),
    Formula("Speed", r"Speed is the size of the velocity: \[ \text{speed} = |v(t)|. \] Velocity has a direction; speed does not."),
    Formula("Speeding up or slowing down", (
        r"Check the signs of $v$ and $a$. \textbf{Same} signs: speeding up. \textbf{Different} signs: slowing down. "
        r"Positive acceleration alone does \emph{not} mean speeding up: a car backing up while braking has $v < 0$ and $a > 0$.")),
    Table(r"$v > 0$ & $a > 0$ & moving right, pushed right & \blank{speeding up} \\ "
          r"$v < 0$ & $a < 0$ & moving left, pushed left & \blank{speeding up} \\ "
          r"$v > 0$ & $a < 0$ & moving right, pulled left & \blank{slowing down} \\ "
          r"$v < 0$ & $a > 0$ & moving left, pushed right & \blank{slowing down}", "llll",
          header=r"velocity & acceleration & picture & so the particle is"),

    Section("Distance traveled"),
    Text(r"The AP question reads: ``What is the total distance traveled from $t = a$ to $t = b$?'' The \textbf{displacement}, "
         r"$x(b) - x(a)$, is final position minus initial position. It is \emph{not} what that question asks: the particle can turn "
         r"around, and total distance adds up every stretch traveled, whichever direction."),
    Text(r"\textbf{The quick way, when you know $x(t)$:} split the trip at the \blank{turning points} (where $v$ changes sign) and add "
         r"$|x(t_{k+1}) - x(t_k)|$ over the pieces. In Unit 8 you will find total distance as the integral of $|v(t)|$, which is what "
         r"AP free-response questions expect (Topic 8.2)."),
    Table(r"displacement & $x(b) - x(a)$ & net change in position \\ total distance & sum of $|x(t_{k+1}) - x(t_k)|$ & every meter traveled, "
          r"counting each direction", "lll", header=r"quantity & how to find it & meaning"),
    BigIdea(r"Velocity tells direction, speed tells how fast, and acceleration tells how the velocity is changing. "
            r"Speeding up means $v$ and $a$ agree in sign."),
    Check(r"A particle has $v(3) = -4$ and $a(3) = -2$. Is it speeding up or slowing down at $t = 3$?", selfcheck(r"\text{speeding up}"),
          r"Speeding up: $v$ and $a$ have the same sign."),
]

# ---------------------------------------------------------------- practice
PR = [
    (t**2 - 6 * t + 5, 0, 6), (2 * t**3 - 9 * t**2 + 12 * t, 0, 3), (t**3 - 12 * t + 1, 0, 4), (-t**2 + 8 * t, 0, 10),
]
same("pr rest", [sorted(sp.solve(V(e), t)) for e, _, _ in PR], [[3], [1, 2], [-2, 2], [4]])
PRACTICE = [
    Item(r"A particle's position is $x(t) = t^2 - 6t + 5$ for $t \ge 0$. Find $v(t)$ and $a(t)$. Enter $v(t)$.", expr("2*t - 6", var="t"),
         r"$v(t) = 2t - 6$ and $a(t) = 2$.", work="1.4cm"),
    Item(r"For $x(t) = t^2 - 6t + 5$, when is the particle at rest?", num(3), r"At rest means $v(t) = 0$: $v(t) = 2t - 6 = 0$ at $t = 3$.", work="1.2cm"),
    Item(r"For $x(t) = t^2 - 6t + 5$, on what interval is the particle moving left?", selfcheck(r"0 \le t < 3"),
         r"Moving left means $v(t) < 0$: $v(t) = 2t - 6 < 0$ for $0 \le t < 3$.", work="1.2cm"),
    Item(r"For $x(t) = t^2 - 6t + 5$, is the particle speeding up or slowing down at $t = 2$?", selfcheck(r"\text{slowing down}"),
         r"Speeding up means $v$ and $a$ share a sign. $v(2) = -2 < 0$ and $a(2) = 2 > 0$: opposite signs, so slowing down.", work="1.6cm"),
    Item(r"A particle's position is $x(t) = 2t^3 - 9t^2 + 12t$. At what times is it at rest? Enter the later time.", num(2),
         r"At rest means $v(t) = 0$: $v = 6t^2 - 18t + 12 = 6(t - 1)(t - 2) = 0$ at $t = 1$ and $t = 2$.", work="1.8cm"),
    Item(r"For $x(t) = 2t^3 - 9t^2 + 12t$, on what interval is the particle moving left?", selfcheck(r"1 < t < 2"),
         r"Moving left means $v(t) < 0$. $v(t) = 6(t - 1)(t - 2)$: test $v(1.5) = -1.5 < 0$, so left on $1 < t < 2$.", work="2cm"),
    Item(r"For $x(t) = 2t^3 - 9t^2 + 12t$, is the particle speeding up or slowing down at $t = 1.75$?", selfcheck(r"\text{slowing down}"),
         r"Slowing down means $v$ and $a$ have opposite signs. $v(1.75) = -1.125 < 0$ and $a(1.75) = 12(1.75) - 18 = 3 > 0$: opposite, so slowing down.", work="2cm"),
    Item(r"A particle's velocity is $v(t) = t^2 - 4t + 3$. Find its acceleration at $t = 1$.", num(-2), r"$a(t) = 2t - 4$, so $a(1) = -2$.", work="1.2cm"),
    Item(r"For $v(t) = t^2 - 4t + 3$, is the particle speeding up or slowing down at $t = 2.5$?", selfcheck(r"\text{slowing down}"),
         r"$v(2.5) = -0.75 < 0$ and $a(2.5) = 1 > 0$: opposite signs, so slowing down.", work="1.8cm"),
    Item(r"For $v(t) = t^2 - 4t + 3$, find the speed at $t = 2$.", num(1), r"Speed $= |v(2)| = |-1| = 1$.", work="1cm"),
    Item(r"A ball is thrown upward with height $h(t) = -16t^2 + 48t + 6$ feet. When does it reach its highest point?", num(sp.Rational(3, 2)),
         r"At the top the ball is momentarily at rest: $h'(t) = 0$. $-32t + 48 = 0$ at $t = 1.5$ seconds.", work="1.4cm"),
    Item(r"For the same ball, what is its velocity when it is at height $6$ feet on the way down?", num(-48),
         r"$-16t^2 + 48t = 0$ at $t = 3$; $h'(3) = -96 + 48 = -48$ feet per second.", work="1.6cm"),
    Item(r"For the same ball, what is its acceleration at any time?", num(-32), r"$h''(t) = -32$ feet per second per second.", work="1cm"),
    Item(r"A particle has $x(t) = t^3 - 12t + 1$ for $t \ge 0$. When is it moving right?", selfcheck(r"t > 2"),
         r"Moving right means $v(t) > 0$: $v = 3t^2 - 12 > 0$ for $t > 2$.", work="1.4cm"),
    Item(r"For $x(t) = t^3 - 12t + 1$, find the acceleration at the time the particle is at rest.", num(12),
         r"At rest means $v(t) = 0$: $3t^2 - 12 = 0$ at $t = 2$ (for $t \ge 0$). $a(t) = 6t$, so $a(2) = 12$.", work="1.6cm"),
    Item(r"For $x(t) = t^3 - 12t + 1$, find the displacement on $[0, 4]$.", num(16), r"$x(4) - x(0) = 17 - 1 = 16$.", work="1.2cm"),
    Item(r"Esperanza rides a bike along a straight path. Her velocity is $v(t) = 6 - 2t$ m/s. Is she speeding up or slowing down at $t = 4$? Explain.",
         selfcheck(r"\text{speeding up}"), r"$v(4) = -2 < 0$ and $a = -2 < 0$: same sign, so speeding up (moving backward faster).", work="1.6cm"),
    Item(r"Explain why a particle with $a(t) > 0$ can still be slowing down.", selfcheck(r"\text{if } v < 0"),
         r"If $v < 0$, positive acceleration pulls the velocity toward $0$: the speed $|v|$ decreases.", work="1.4cm"),
    Item(r"A particle's position is $x(t) = 4\sin t$ for $0 \le t \le 2\pi$. When is it at rest? Enter the smaller time.", num(sp.pi / 2),
         r"At rest means $v(t) = 0$: $v = 4\cos t = 0$ at $t = \frac\pi2$ and $t = \frac{3\pi}{2}$.", work="1.4cm"),
    Item(r"For $x(t) = 4\sin t$, find the acceleration when $t = \frac\pi2$, and say which way the particle then starts to move.", num(-4),
         r"$a = -4\sin t = -4$: from rest at $x = 4$, it starts moving left.", work="1.6cm"),
]
same("p", [V(t**2 - 6 * t + 5).subs(t, 2), A(t**2 - 6 * t + 5).subs(t, 2), V(2 * t**3 - 9 * t**2 + 12 * t).subs(t, sp.Rational(3, 2)),
           V(2 * t**3 - 9 * t**2 + 12 * t).subs(t, sp.Rational(7, 4)), A(2 * t**3 - 9 * t**2 + 12 * t).subs(t, sp.Rational(7, 4)),
           (t**2 - 4 * t + 3).subs(t, sp.Rational(5, 2)), A(t**3 - 12 * t + 1).subs(t, 2), (t**3 - 12 * t + 1).subs(t, 4) - 1,
           V(-16 * t**2 + 48 * t + 6).subs(t, 3)],
     [-2, 2, sp.Rational(-3, 2), sp.Rational(-9, 8), 3, sp.Rational(-3, 4), 12, 16, -48])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"A particle's position is $x(t) = t^3 - 3t^2 + 2$. Find its velocity at $t = 3$.", num(9), r"$v = 3t^2 - 6t$, so $v(3) = 27 - 18 = 9$.", work="1.4cm"),
        Item(r"A particle's position is $x(t) = 2t^2 - 7t$. Find its velocity at $t = 1$.", num(-3), r"$v = 4t - 7$, so $v(1) = -3$.", work="1.4cm"),
        Item(r"A particle's position is $x(t) = t^3 - t$. Find its velocity at $t = 2$.", num(11), r"$v = 3t^2 - 1$, so $v(2) = 11$.", work="1.4cm"),
    ),
    Variants(
        Item(r"$x(t) = t^2 - 8t + 3$. When is the particle at rest?", num(4), r"$v = 2t - 8 = 0$ at $t = 4$.", work="1.2cm"),
        Item(r"$x(t) = t^3 - 3t$ for $t \ge 0$. When is the particle at rest?", num(1), r"$v = 3t^2 - 3 = 0$ at $t = 1$ (for $t \ge 0$).", work="1.2cm"),
        Item(r"$x(t) = t^3 - 6t^2$ for $t > 0$. When is the particle at rest?", num(4), r"$v = 3t^2 - 12t = 3t(t - 4) = 0$ at $t = 4$.", work="1.2cm"),
    ),
    Variants(
        MCQ(r"A particle's velocity is $v(t) = 2t - 5$. At $t = 1$ the particle is", [r"speeding up", r"slowing down", r"at rest", r"moving right"], "B",
            r"$v(1) = -3 < 0$ and $a = 2 > 0$: opposite signs.", why_not={"A": "check the signs of both $v$ and $a$"}),
        MCQ(r"A particle's velocity is $v(t) = 3 - t^2$. At $t = 2$ the particle is", [r"slowing down", r"at rest", r"speeding up", r"moving right"], "C",
            r"$v(2) = -1 < 0$ and $a(2) = -4 < 0$: same sign."),
        MCQ(r"A particle's velocity is $v(t) = t^2 - 1$. At $t = 0.5$ the particle is", [r"moving right", r"speeding up", r"at rest", r"slowing down"], "D",
            r"$v(0.5) = -0.75 < 0$ and $a(0.5) = 1 > 0$: opposite signs."),
    ),
    Variants(
        Item(r"$v(t) = t^2 - 6t$. Find the speed at $t = 2$.", num(8), r"$v(2) = -8$, so the speed is $8$.", work="1cm"),
        Item(r"$v(t) = 4 - t^2$. Find the speed at $t = 3$.", num(5), r"$v(3) = -5$, so the speed is $5$.", work="1cm"),
        Item(r"$v(t) = 2t - 9$. Find the speed at $t = 1$.", num(7), r"$v(1) = -7$, so the speed is $7$.", work="1cm"),
    ),
    Variants(
        Item(r"$x(t) = t^2 - 4t$. On what interval is the particle moving left?", selfcheck(r"t < 2"),
             r"Moving left means $v(t) < 0$: $v = 2t - 4 < 0$ for $t < 2$.", work="1.4cm"),
        Item(r"$x(t) = t^3 - 3t^2$ for $t \ge 0$. On what interval is the particle moving left?", selfcheck(r"0 < t < 2"),
             r"Moving left means $v(t) < 0$: $v = 3t^2 - 6t = 3t(t - 2) < 0$ for $0 < t < 2$.", work="1.4cm"),
        Item(r"$x(t) = 6t - t^2$. On what interval is the particle moving left?", selfcheck(r"t > 3"),
             r"Moving left means $v(t) < 0$: $v = 6 - 2t < 0$ for $t > 3$.", work="1.4cm"),
    ),
]
same("q", [V(t**3 - 3 * t**2 + 2).subs(t, 3), V(2 * t**2 - 7 * t).subs(t, 1), V(t**3 - t).subs(t, 2),
           sp.solve(V(t**3 - 3 * t**2), t)], [9, -3, 11, [0, 2]])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"A particle moves with position $x(t) = t^3 - 6t^2 + 9t$. On which interval is it moving left?", [r"$(0, 1)$", r"$(1, 3)$", r"$(3, \infty)$", r"$(2, \infty)$"], "B",
        r"Moving left means $v(t) < 0$. $v = 3(t - 1)(t - 3) < 0$ between the roots.", why_not={"D": "that's where $a > 0$"}),
    MCQ(r"A particle's velocity is $v(t) = \sin t$ for $0 \le t \le 2\pi$. On which interval is it speeding up?",
        [r"$\left(0, \frac\pi2\right)$ only", r"$\left(\frac\pi2, \pi\right)$", r"$\left(0, \frac\pi2\right)$ and $\left(\pi, \frac{3\pi}{2}\right)$", r"$\left(\pi, 2\pi\right)$"], "C",
        r"$a = \cos t$. $v$ and $a$ share a sign on $\left(0, \frac\pi2\right)$ (both positive) and $\left(\pi, \frac{3\pi}{2}\right)$ (both negative)."),
    MCQ(r"A ball's height is $h(t) = -16t^2 + 64t + 80$ feet. Its velocity when it hits the ground is", [r"$-64$ ft/s", r"$-96$ ft/s", r"$-160$ ft/s", r"$96$ ft/s"], "B",
        r"$h = 0$: $t^2 - 4t - 5 = 0$, so $t = 5$. $h'(5) = -160 + 64 = -96$ ft/s.", why_not={"D": "it's moving down"}),
    MCQ(r"For $x(t) = t^3 - 6t^2 + 9t$, the acceleration when the particle first comes to rest is", [r"$6$", r"$0$", r"$-3$", r"$-6$"], "D",
        r"At rest means $v = 0$: first at $t = 1$, and $a(1) = 6(1) - 12 = -6$.", why_not={"A": "that's at the second stop, $t = 3$"}),
]
same("m", [sp.solve(-16 * t**2 + 64 * t + 80, t)[-1], V(-16 * t**2 + 64 * t + 80).subs(t, 5), A(X).subs(t, 1)], [5, -96, -6])

XF = 2 * t**3 - 15 * t**2 + 24 * t + 3
FRQS = [
    FRQ("A particle on a line", (
        r"A particle moves along the $x$-axis so that its position at time $t$ is given by $x(t) = 2t^3 - 15t^2 + 24t + 3$ "
        r"for $0 \le t \le 5$."), [
        Part("a", r"Find the velocity of the particle at time $t$. During what open intervals of time $t$, for $0 < t < 5$, is the "
                  r"particle moving to the left? Give a reason for your answer.", selfcheck(r"1 < t < 4"),
             r"Moving left means $v(t) < 0$. $v(t) = 6t^2 - 30t + 24 = 6(t - 1)(t - 4)$, which is negative on the interval $1 < t < 4$.",
             [(1, "$v(t)$"), (1, "interval $1 < t < 4$ with reason $v(t) < 0$")], work="2.6cm"),
        Part("b", r"Is the speed of the particle increasing or decreasing at time $t = 2$? Give a reason for your answer.",
             selfcheck(r"\text{Increasing}"),
             r"$v(2) = 24 - 60 + 24 = -12$ and $a(t) = 12t - 30$, so $a(2) = -6$. Velocity and acceleration are both negative, so the "
             r"speed is increasing.",
             [(1, "$v(2)$ and $a(2)$"), (1, "increasing, because $v(2)$ and $a(2)$ have the same sign")], work="2.4cm"),
        Part("c", r"At time $t = 3$, is the particle moving toward the origin or away from the origin? Give a reason for your answer.",
             selfcheck(r"\text{Away from the origin}"),
             r"$x(3) = 54 - 135 + 72 + 3 = -6 < 0$ and $v(3) = 54 - 90 + 24 = -12 < 0$. The particle is to the left of the origin and moving "
             r"left, so it is moving away from the origin.",
             [(1, "$x(3)$ and $v(3)$"), (1, "away, with the reason")], work="2.4cm"),
        Part("d", r"Find the position of the particle at the time when its acceleration is $0$.", num(sp.Rational(1, 2)),
             r"$a(t) = 12t - 30 = 0$ at $t = \frac52$, and $x\!\left(\frac52\right) = \frac{125}{4} - \frac{375}{4} + 60 + 3 = \frac12$.",
             [(1, "$t = \\frac52$"), (1, "position $\\frac12$")], work="2.2cm"),
    ], frq_type="Particle motion"),
]
X2 = 2 * t**3 - 15 * t**2 + 24 * t + 3
v2, a2 = sp.diff(X2, t), sp.diff(X2, t, 2)
turns2 = sorted(sp.solve(v2, t))
same("frq a", turns2, [1, 4])
same("frq b", [v2.subs(t, 2), a2.subs(t, 2)], [-12, -6])
same("frq c", [X2.subs(t, 3), v2.subs(t, 3)], [-6, -12])
same("frq d", X2.subs(t, sp.solve(a2, t)[0]), sp.Rational(1, 2))

TOPIC = Topic(
    number="4.2", title="Straight-Line Motion: Connecting Position, Velocity, and Acceleration",
    unit="Unit 4: Contextual Applications of Differentiation", ced=["CHA-3.B", "CHA-3.B.1", "CHA-3.B.2"],
    goals=r"Use derivatives to describe a particle's motion: direction, speed, speeding up or slowing down, and distance traveled.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
