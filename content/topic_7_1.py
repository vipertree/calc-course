"""Topic 7.1: Modeling situations with differential equations.

CED: CHA-7.A (CHA-7.A.1, CHA-7.A.2): a differential equation relates a function to its derivatives; its solutions are
functions; translate verbal descriptions ("the rate of change of y is proportional to ...") into differential
equations; evaluate a differential equation at a point to get a rate and its sign. Worked examples: a rumor
(jointly proportional), a slope at a point, cooling coffee. AP asks this inside later DE questions, so FRQS is empty.
"""
import sympy as sp

from calclib import (VideoExample, MCQ, BigIdea, Check, Formula, Item, Section, Table, Text, Topic, Variants, Video, num, same, selfcheck)

P, y, x, T = sp.symbols("P y x T")
same("lesson", [(sp.Rational(3, 10) * P * (1 - P / 500)).subs(P, 100), (sp.Rational(3, 10) * P * (1 - P / 500)).subs(P, 600), (-sp.Rational(1, 10) * (T - 70)).subs(T, 130)], [24, -36, -6])

NOTES = [
    Video("s7_1.py::Lesson", "Differential equations", 5),

    Section("Rules for rates"),
    Text(r"A \blank{differential equation} is an equation that involves a derivative. It gives a rule for how a quantity changes, such as $\frac{dT}{dt} = -k(T - 70)$ for cooling coffee. "
         r"A \blank{solution} is a function (not a number) whose derivative obeys the rule: every $y = x^3 + C$ solves $\frac{dy}{dx} = 3x^2$."),
    Table(r"the rate of change of $y$ is proportional to $y$ & $\dfrac{dy}{dt} = \blank{ky}$ \\ "
          r"proportional to the square root of $y$ & $\dfrac{dy}{dt} = k\sqrt y$ \\ "
          r"inversely proportional to $y$ & $\dfrac{dy}{dt} = \dfrac ky$ \\ "
          r"proportional to the difference between $y$ and $70$ & $\dfrac{dy}{dt} = k(y - 70)$ \\ "
          r"jointly proportional to $y$ and $1000 - y$ & $\dfrac{dy}{dt} = \blank{ky(1000 - y)}$", "ll", header=r"In words & Differential equation"),
    Text(r"\textbf{Reading the rate.} Substitute the given values into the right side: the result is the rate of change there, and its \blank{sign} tells whether the quantity is increasing or decreasing."),
    VideoExample('Reading the rate', work="2.4cm"),
    BigIdea(r"A differential equation is a rule for a rate of change; its solutions are functions. Translate ``proportional to'' as a constant times, and plug in to read the rate."),
    Check(r"The rate of change of $A$ is proportional to the cube of $A$. Write a differential equation for $A$.", selfcheck(r"\frac{dA}{dt} = kA^3"), r"$\frac{dA}{dt} = kA^3$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"The rate of change of a population $P$ is proportional to $P$. Write a differential equation for $P$.", selfcheck(r"\frac{dP}{dt} = kP"), r"$\frac{dP}{dt} = kP$.", work="1cm"),
    Item(r"The rate at which a cup of tea cools is proportional to the difference between its temperature $H$ and the room temperature, $68^\circ$F. Write a differential equation for $H$.",
         selfcheck(r"\frac{dH}{dt} = k(H - 68)"), r"$\frac{dH}{dt} = k(H - 68)$ (with $k < 0$ for cooling).", work="1.2cm"),
    Item(r"The rate of change of $V$ is inversely proportional to the square root of $V$. Write a differential equation for $V$.", selfcheck(r"\frac{dV}{dt} = \frac{k}{\sqrt V}"),
         r"$\frac{dV}{dt} = \frac{k}{\sqrt V}$.", work="1cm"),
    Item(r"A disease spreads in a town of $5000$ at a rate jointly proportional to the number $N$ infected and the number not infected. Write a differential equation for $N$.",
         selfcheck(r"\frac{dN}{dt} = kN(5000 - N)"), r"$\frac{dN}{dt} = kN(5000 - N)$.", work="1.2cm"),
    Item(r"$\frac{dy}{dx} = 3x - 2y$. Find $\frac{dy}{dx}$ at $(1, 4)$.", num(-5), r"$3(1) - 2(4) = -5$.", work="1cm"),
    Item(r"$\frac{dy}{dx} = xy^2$. Is the solution through $(-2, 3)$ increasing or decreasing there?", selfcheck(r"\text{decreasing}"), r"$(-2)(9) = -18 < 0$.", work="1cm"),
    Item(r"$\frac{dP}{dt} = 0.04P\left(1 - \frac{P}{800}\right)$. Find $\frac{dP}{dt}$ when $P = 200$.", num(6), r"$0.04(200)(0.75) = 6$.", work="1.2cm"),
    Item(r"$\frac{dT}{dt} = -0.2(T - 25)$, with $T$ in $^\circ$C and $t$ in minutes. Find $\frac{dT}{dt}$ when $T = 75$ and interpret it.", num(-10),
         r"$-0.2(50) = -10$: when the temperature is $75^\circ$C, it is decreasing at $10^\circ$C per minute.", work="1.4cm"),
    Item(r"Which function is a solution of $\frac{dy}{dx} = 2x$: $y = x^2 + 5$ or $y = 2x^2$?", selfcheck(r"y = x^2 + 5"), r"$\frac{d}{dx}(x^2 + 5) = 2x$; $\frac{d}{dx}(2x^2) = 4x$.", work="1cm"),
]
same("p", [(3 * x - 2 * y).subs({x: 1, y: 4}), (x * y**2).subs({x: -2, y: 3}), (sp.Rational(4, 100) * P * (1 - P / 800)).subs(P, 200), (-sp.Rational(1, 5) * (T - 25)).subs(T, 75)], [-5, -18, 6, -10])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"``The rate of change of $y$ is proportional to $y$'' is", [r"$\frac{dy}{dt} = ky$", r"$y = kt$", r"$\frac{dy}{dt} = k$", r"$\frac{dy}{dt} = \frac ky$"], "A", r"Rate of change $= k \cdot y$."),
        MCQ(r"``The rate of change of $Q$ is inversely proportional to $Q$'' is", [r"$\frac{dQ}{dt} = kQ$", r"$\frac{dQ}{dt} = \frac kQ$", r"$Q = \frac kt$", r"$\frac{dQ}{dt} = -Q$"], "B", r"Inversely proportional: $\frac{k}{Q}$."),
        MCQ(r"``The rate of change of $W$ is proportional to the difference between $W$ and $50$'' is", [r"$\frac{dW}{dt} = kW - 50$", r"$\frac{dW}{dt} = k(50W)$", r"$\frac{dW}{dt} = k(W - 50)$", r"$W = k(t - 50)$"], "C", r"$k$ times the difference."),
    ),
    Variants(*[Item(rf"$\dfrac{{dy}}{{dx}} = {sp.latex(e)}$. Find $\dfrac{{dy}}{{dx}}$ at $({a}, {b})$.", num(e.subs({x: a, y: b})), rf"${e.subs({x: a, y: b})}$.", work="1cm")
               for e, a, b in ((x + y**2, 2, -1), (x * y - 3, 2, 4), (y - x**2, 1, 5))]),
    Variants(
        Item(r"$\frac{dP}{dt} = 0.5P\left(1 - \frac{P}{200}\right)$. Is $P$ increasing or decreasing when $P = 250$?", selfcheck(r"\text{decreasing}"), r"$0.5(250)(-0.25) < 0$.", work="1cm"),
        Item(r"$\frac{dP}{dt} = 0.5P\left(1 - \frac{P}{200}\right)$. Is $P$ increasing or decreasing when $P = 50$?", selfcheck(r"\text{increasing}"), r"$0.5(50)(0.75) > 0$.", work="1cm"),
        Item(r"$\frac{dH}{dt} = -0.3(H - 20)$. Is $H$ increasing or decreasing when $H = 10$?", selfcheck(r"\text{increasing}"), r"$-0.3(-10) = 3 > 0$.", work="1cm"),
    ),
    Variants(
        Item(r"$\frac{dT}{dt} = -0.05(T - 70)$, in $^\circ$F per minute. Find $\frac{dT}{dt}$ when $T = 150$.", num(-4), r"$-0.05(80) = -4$.", work="1cm"),
        Item(r"$\frac{dT}{dt} = -0.1(T - 20)$, in $^\circ$C per minute. Find $\frac{dT}{dt}$ when $T = 90$.", num(-7), r"$-0.1(70) = -7$.", work="1cm"),
        Item(r"$\frac{dT}{dt} = -0.2(T - 65)$, in $^\circ$F per minute. Find $\frac{dT}{dt}$ when $T = 40$.", num(5), r"$-0.2(-25) = 5$.", work="1cm"),
    ),
    Variants(
        MCQ(r"Which is a solution of $\frac{dy}{dx} = \cos x$?", [r"$y = -\sin x$", r"$y = \sin x + 4$", r"$y = \cos x$", r"$y = -\cos x$"], "B", r"$\frac{d}{dx}(\sin x + 4) = \cos x$."),
        MCQ(r"Which is a solution of $\frac{dy}{dx} = e^x$?", [r"$y = xe^x$", r"$y = e^x - 3$", r"$y = e^{x+1}$ only", r"$y = \ln x$"], "B", r"$\frac{d}{dx}(e^x - 3) = e^x$."),
        MCQ(r"Which is a solution of $\frac{dy}{dx} = \frac1x$ for $x > 0$?", [r"$y = -\frac{1}{x^2}$", r"$y = e^x$", r"$y = \ln x + 2$", r"$y = x$"], "C", r"$\frac{d}{dx}(\ln x + 2) = \frac1x$."),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"The number $N$ of bacteria grows at a rate proportional to the square root of $N$. Which equation models this?", [r"$\frac{dN}{dt} = k\sqrt N$", r"$N = k\sqrt t$", r"$\frac{dN}{dt} = \sqrt{kN}$ only", r"$\frac{dN}{dt} = kN^2$"], "A",
        r"Rate $= k\sqrt N$."),
    MCQ(r"$\frac{dy}{dx} = y\left(4 - y\right)$. For which value of $y$ is the solution decreasing?", [r"$y = 1$", r"$y = 3$", r"$y = 5$", r"$y = 2$"], "C", r"$5(4 - 5) = -5 < 0$."),
    MCQ(r"Newton's law of cooling for an object at temperature $T$ in a room at $72^\circ$ is", [r"$\frac{dT}{dt} = kT$", r"$\frac{dT}{dt} = k(T - 72)$", r"$T = 72e^{kt}$ only", r"$\frac{dT}{dt} = 72k$"], "B",
        r"The rate is proportional to the difference from room temperature."),
    MCQ(r"A tank drains at a rate proportional to the square root of the depth $h$ of the water. With $k > 0$, the model is", [r"$\frac{dh}{dt} = k\sqrt h$", r"$\frac{dh}{dt} = kh$", r"$\frac{dh}{dt} = \frac{k}{\sqrt h}$", r"$\frac{dh}{dt} = -k\sqrt h$"], "D",
        r"Draining means $h$ decreases: $-k\sqrt h$."),
]
same("m", [(y * (4 - y)).subs(y, 5)], [-5])

FRQS = []

TOPIC = Topic(
    number="7.1", title="Modeling Situations with Differential Equations",
    unit="Unit 7: Differential Equations", ced=["CHA-7.A", "CHA-7.A.1", "CHA-7.A.2"],
    goals=r"Translate verbal descriptions into differential equations and use a differential equation to find a rate of change and its sign.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
