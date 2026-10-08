"""Topic 8.1: Finding the average value of a function on an interval.

CED: CHA-4.B (CHA-4.B.1): the average value of a continuous f on [a, b] is 1/(b - a) times the integral of f from a to b.
Built from the average of n equally spaced samples; the picture is the rectangle with the same area; a continuous f
reaches its average value at some c (Mean Value Theorem for integrals). Average value (a height) is not average rate of
change (a slope). Lesson example: x^2 on [1, 4], average 7, reached at sqrt 7. Worked examples: from a graph (segment and
semicircle), sin x on [0, pi], a trapezoidal average from a table.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)
from calclib.figs import graph, region

x = sp.symbols("x", real=True)


def avg(f, a, b):
    return sp.simplify(sp.integrate(f, (x, a, b)) / (b - a))


def trap(ts, vs):
    return sum(sp.Rational(b - a, 2) * (u + v) for a, b, u, v in zip(ts, ts[1:], vs, vs[1:]))


same("lesson", [avg(x**2, 1, 4)], [7])
same("ex1", [(4 + 2 * sp.pi) / 6], [(2 + sp.pi) / 3])
same("ex2", [avg(sp.sin(x), 0, sp.pi)], [2 / sp.pi])
same("ex3", [trap([0, 2, 4, 6, 8], [60, 64, 70, 68, 62]) / 8], [sp.Rational(263, 4)])

FIG_LEVEL = region("t8_1_level", [("x^2", 0, 4.1)], (0, 4.5), (0, 17), [(lambda v: v * v, lambda v: 0, 1, 4)], ystep=4, hlines=[7],
                   labels=[(4.2, 7, "right", r"$y = 7$")], caption=r"$f(x) = x^2$ on $[1, 4]$: the shaded area equals the area of the $3$-by-$7$ rectangle under $y = 7$.")
FIG_G = graph("t8_1_g", [("x", 0, 2), ("2+0*x", 2, 4), ("2-(x-4)", 4, 6)], (0, 6.5), (0, 3),
              caption=r"The graph of $g$: three line segments.")
same("g", [sp.Rational(1, 2) * 2 * 2 + 2 * 2 + sp.Rational(1, 2) * 2 * (2 + 0)], [8])

NOTES = [
    Video("s8_1.py::Lesson", "Average value of a function", 6),

    Section("From a list to an integral"),
    Text(r"The average of $n$ equally spaced samples is $\dfrac{f(x_1) + \cdots + f(x_n)}{n}$. Since $n = \dfrac{b - a}{\Delta x}$, that equals "
         r"$\dfrac{1}{b - a}\sum f(x_k)\,\Delta x$: a Riemann sum divided by the length of the interval. More samples turn the sum into an integral."),
    Formula("Average value", (
        r"The average value of a continuous function $f$ on $[a, b]$ is \[ f_{\text{avg}} = \blank{\frac{1}{b - a}\int_a^b f(x)\,dx}. \] "
        r"In words: add everything up with the integral, then divide by the length of the interval.")),
    Section("The picture"),
    Text(r"$f_{\text{avg}}\cdot(b - a) = \int_a^b f(x)\,dx$: the average value is the height of the rectangle on $[a, b]$ with the same area as the region. "
         r"Think of the region as water leveling out."),
    FIG_LEVEL,
    Formula("Mean Value Theorem for integrals", (
        r"If $f$ is continuous on $[a, b]$, there is at least one $c$ in $[a, b]$ with \[ f(c) = \blank{\frac{1}{b - a}\int_a^b f(x)\,dx}. \] "
        r"A continuous function reaches its average value somewhere in the interval.")),
    VideoExample('Average value of x squared', work="3.6cm"),
    Text(r"\textbf{Inputs and outputs.} The average value is an output ($7$). Where $f$ equals it is an input ($x = \sqrt7$). Questions ask for each separately."),
    Section("Not the average rate of change"),
    Text(r"Average rate of change is a slope, $\dfrac{f(b) - f(a)}{b - a}$; average value is a height, $\dfrac{1}{b - a}\int_a^b f(x)\,dx$. For $x^2$ on $[1, 4]$ they are $5$ and $7$. "
         r"They agree in one place: the average value of $f'$ equals the average rate of change of $f$, because $\int_a^b f'(x)\,dx = f(b) - f(a)$."),
    BigIdea(r"Average value $=$ integral $\div$ length of the interval: the height of the rectangle with the same area."),
    Check(r"Find the average value of $f(x) = 6x$ on $[0, 2]$.", selfcheck(r"6"), r"$\frac12\int_0^2 6x\,dx = \frac12 \cdot 12$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Find the average value of $f(x) = 3x^2$ on $[0, 2]$.", num(avg(3 * x**2, 0, 2)), r"$\frac12\left[x^3\right]_0^2 = 4$.", work="1.4cm"),
    Item(r"Find the average value of $f(x) = 4 - x$ on $[0, 4]$.", num(avg(4 - x, 0, 4)), r"$\frac14 \cdot 8 = 2$ (a triangle of area $8$).", work="1.2cm"),
    Item(r"Find the average value of $f(x) = \sqrt x$ on $[0, 9]$.", num(avg(sp.sqrt(x), 0, 9)), r"$\frac19\left[\frac23x^{3/2}\right]_0^9 = \frac19 \cdot 18 = 2$.", work="1.4cm"),
    Item(r"Find the average value of $f(x) = \cos x$ on $\left[0, \frac\pi2\right]$.", num(avg(sp.cos(x), 0, sp.pi / 2), tol=1e-3), r"$\frac2\pi\left[\sin x\right]_0^{\pi/2} = \frac2\pi \approx 0.637$.", work="1.4cm"),
    Item(r"Find the average value of $f(x) = \frac1x$ on $[1, e]$.", num(avg(1 / x, 1, sp.E), tol=1e-3), r"$\frac{1}{e - 1}\left[\ln x\right]_1^e = \frac{1}{e - 1} \approx 0.582$.", work="1.4cm"),
    Item(r"$f(x) = x^2$ on $[0, 3]$. Find the value of $c$ in $[0, 3]$ where $f(c)$ equals the average value.", num(sp.sqrt(3), tol=1e-3),
         r"Average $= \frac13 \cdot 9 = 3$; $c^2 = 3$, $c = \sqrt3$ (the negative root is outside $[0, 3]$).", work="1.8cm"),
    Item(r"The graph of $g$ is shown (three segments). Find the average value of $g$ on $[0, 6]$.", num(sp.Rational(4, 3)), r"Area $= 2 + 4 + 2 = 8$; $\frac86 = \frac43$.", work="1.4cm", figure=FIG_G),
    Item(r"Find the average rate of change of $f(x) = x^3$ on $[0, 2]$, and the average value of $f$ on $[0, 2]$.", selfcheck(r"4 \text{ and } 2"),
         r"Rate: $\frac{8 - 0}{2} = 4$. Value: $\frac12\left[\frac{x^4}{4}\right]_0^2 = 2$.", work="1.8cm"),
    Item(r"$\int_2^7 f(x)\,dx = 30$. What is the average value of $f$ on $[2, 7]$?", num(6), r"$\frac{30}{5}$.", work="1cm"),
    Item(r"The average value of $f$ on $[1, 5]$ is $9$. Find $\int_1^5 f(x)\,dx$.", num(36), r"$9 \cdot 4$.", work="1cm"),
    Item(r"Velocity $v(t)$ in m/s is $10, 14, 12, 8$ at $t = 0, 3, 6, 9$ seconds. Use a trapezoidal sum to approximate the average velocity on $0 \le t \le 9$.",
         num(trap([0, 3, 6, 9], [10, 14, 12, 8]) / 9, tol=1e-3), r"$\frac{3}{2}(10 + 2\cdot14 + 2\cdot12 + 8) = 105$; $\frac{105}{9} \approx 11.67$ m/s.", work="2cm"),
    Item(r"Find $k > 0$ so that the average value of $f(x) = 2x$ on $[0, k]$ is $5$.", num(5), r"$\frac1k\left[x^2\right]_0^k = k = 5$.", work="1.4cm"),
]
same("p", [trap([0, 3, 6, 9], [10, 14, 12, 8])], [105])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find the average value of $f(x) = x^2 + 1$ on $[0, 3]$.", num(avg(x**2 + 1, 0, 3)), r"$\frac13(9 + 3) = 4$.", work="1.2cm"),
        Item(r"Find the average value of $f(x) = 2x + 3$ on $[1, 5]$.", num(avg(2 * x + 3, 1, 5)), r"$\frac14\left[x^2 + 3x\right]_1^5 = \frac14(40 - 4) = 9$.", work="1.2cm"),
        Item(r"Find the average value of $f(x) = x^3$ on $[0, 2]$.", num(avg(x**3, 0, 2)), r"$\frac12 \cdot 4 = 2$.", work="1.2cm"),
    ),
    Variants(
        Item(r"Find the average value of $f(x) = \sin x$ on $\left[0, \frac\pi2\right]$.", num(avg(sp.sin(x), 0, sp.pi / 2), tol=1e-3), r"$\frac2\pi \cdot 1 \approx 0.637$.", work="1.2cm"),
        Item(r"Find the average value of $f(x) = e^x$ on $[0, 1]$.", num(avg(sp.exp(x), 0, 1), tol=1e-3), r"$e - 1 \approx 1.718$.", work="1.2cm"),
        Item(r"Find the average value of $f(x) = \sec^2 x$ on $\left[0, \frac\pi4\right]$.", num(avg(sp.sec(x)**2, 0, sp.pi / 4), tol=1e-3), r"$\frac4\pi \cdot 1 \approx 1.273$.", work="1.2cm"),
    ),
    Variants(
        Item(r"$f(x) = 3x^2$ on $[0, 2]$. Find $c$ with $f(c)$ equal to the average value.", num(2 / sp.sqrt(3), tol=1e-3), r"Average $4$; $3c^2 = 4$, $c = \frac{2}{\sqrt3} \approx 1.155$.", work="1.4cm"),
        Item(r"$f(x) = 2x$ on $[1, 5]$. Find $c$ with $f(c)$ equal to the average value.", num(3), r"Average $6$; $c = 3$.", work="1.4cm"),
        Item(r"$f(x) = x^2$ on $[0, 6]$. Find $c$ with $f(c)$ equal to the average value.", num(2 * sp.sqrt(3), tol=1e-3), r"Average $12$; $c = \sqrt{12} \approx 3.464$.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"For $f(x) = x^2$ on $[0, 3]$, which is true?", [r"The average value is $3$ and the average rate of change is $3$", r"The average value is $3$ and the average rate of change is $9$",
            r"The average value is $9$ and the average rate of change is $3$", r"Both are $\frac92$"], "A", r"Value: $\frac13 \cdot 9 = 3$. Rate: $\frac{9 - 0}{3} = 3$. (A coincidence here.)"),
        MCQ(r"For $f(x) = x^2$ on $[0, 6]$, which is true?", [r"Both are $6$", r"The average value is $12$ and the average rate of change is $6$",
            r"The average value is $6$ and the average rate of change is $12$", r"The average value is $36$ and the average rate of change is $6$"], "B", r"Value: $\frac16 \cdot 72 = 12$. Rate: $\frac{36}{6} = 6$."),
    ),
    Variants(
        Item(r"$\int_0^8 f(x)\,dx = 20$. Find the average value of $f$ on $[0, 8]$.", num(sp.Rational(5, 2)), r"$\frac{20}{8}$.", work="1cm"),
        Item(r"The average value of $f$ on $[-2, 4]$ is $3$. Find $\int_{-2}^4 f(x)\,dx$.", num(18), r"$3 \cdot 6$.", work="1cm"),
        Item(r"The average value of $f'$ on $[1, 3]$ is $5$ and $f(1) = 2$. Find $f(3)$.", num(12), r"$\int_1^3 f' = 10 = f(3) - f(1)$.", work="1.2cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"The average value of $f(x) = \frac{1}{x^2}$ on $[1, 4]$ is", [r"$\frac34$", r"$\frac{1}{16}$", r"$\frac14$", r"$\frac{15}{16}$"], "C", r"$\frac13\left[-\frac1x\right]_1^4 = \frac13 \cdot \frac34 = \frac14$.",
        why_not={"A": "forgot to divide by the length $3$"}),
    MCQ(r"$f$ is continuous, and its average value on $[2, 6]$ is $5$. Which must be true?", [r"$f(4) = 5$", r"$\int_2^6 f(x)\,dx = 5$", r"$f(6) - f(2) = 20$", r"$f(c) = 5$ for some $c$ in $[2, 6]$"], "D",
        r"The Mean Value Theorem for integrals."),
    MCQ(r"The temperature of a liquid is $T(t) = 20 + 10e^{-0.2t}$ degrees Celsius. To three decimal places, its average temperature over $0 \le t \le 5$ is", [r"$26.321$", r"$23.679$", r"$25.000$", r"$28.647$"], "A",
        r"$\frac15\int_0^5 T(t)\,dt \approx 26.321$.", calc=True),
    MCQ(r"The average value of $f(x) = 3x^2 - 2x$ on $[0, k]$ is $k^2 - k$. For $k > 0$, which is true?", [r"It holds only for $k = 1$", r"It holds for every $k > 0$", r"It holds for no $k > 0$", r"It holds only for $k = 2$"], "B",
        r"$\frac1k\left[x^3 - x^2\right]_0^k = k^2 - k$ for every $k$."),
]
t = sp.symbols("t")
close("m3", float(sp.integrate(20 + 10 * sp.exp(-sp.Rational(1, 5) * t), (t, 0, 5)) / 5), 26.321, 5e-4)
same("m1", [avg(1 / x**2, 1, 4)], [sp.Rational(1, 4)])
k = sp.symbols("k", positive=True)
same("m4", [sp.simplify(sp.integrate(3 * x**2 - 2 * x, (x, 0, k)) / k)], [k**2 - k])

# ---------------------------------------------------------------- FRQ
TS, RS = [0, 4, 6, 10, 12], [30, 42, 48, 40, 36]
same("frq", [trap(TS, RS), trap(TS, RS) / 12, sp.Rational(40 - 42, 10 - 4)], [486, sp.Rational(81, 2), -sp.Rational(1, 3)])
FRQS = [
    FRQ("Visitors to a museum", (
        r"Visitors arrive at a museum at a rate modeled by a differentiable function $R$, where $R(t)$ is measured in people per hour and $t$ is hours after the museum opens. Selected values are in the table."
        r"\par\smallskip\centerline{\begin{tabular}{c|ccccc} $t$ (hours) & 0 & 4 & 6 & 10 & 12 \\ \hline $R(t)$ (people per hour) & 30 & 42 & 48 & 40 & 36\end{tabular}}"), [
        Part("a", r"Use a trapezoidal sum with the four subintervals indicated by the table to approximate $\displaystyle\int_0^{12} R(t)\,dt$. Show the computations that lead to your answer.", num(486),
             r"$4\cdot\frac{30 + 42}{2} + 2\cdot\frac{42 + 48}{2} + 4\cdot\frac{48 + 40}{2} + 2\cdot\frac{40 + 36}{2} = 144 + 90 + 176 + 76 = 486$.", [(1, "trapezoidal sum"), (1, "answer")], work="2.4cm"),
        Part("b", r"Use your answer from part (a) to approximate the average rate at which visitors arrive over $0 \le t \le 12$. Indicate units of measure.", num(sp.Rational(81, 2), tol=0.01, display=r"40.5\ \text{people per hour}"),
             r"$\frac{1}{12}\int_0^{12} R(t)\,dt \approx \frac{486}{12} = 40.5$ people per hour.", [(1, "divides by $12$"), (1, "answer with units")], work="1.8cm"),
        Part("c", r"Must there be a time $t$, $4 < t < 10$, at which $R'(t) = -\frac13$? Justify your answer.", selfcheck(r"\text{Yes, by the Mean Value Theorem}"),
             r"$R$ is differentiable, so it is continuous. $\frac{R(10) - R(4)}{10 - 4} = \frac{40 - 42}{6} = -\frac13$. By the Mean Value Theorem, yes.", [(1, "difference quotient"), (1, "MVT with conditions")], work="2cm"),
        Part("d", r"Explain the difference in meaning between $\frac{1}{12}\int_0^{12} R(t)\,dt$ and $\frac{R(12) - R(0)}{12}$.", selfcheck(r"\text{average arrival rate vs. average rate of change of the arrival rate}"),
             r"The first is the average number of people arriving per hour over the twelve hours. The second is the average rate at which the arrival rate changes, in people per hour per hour.",
             [(1, "both meanings")], work="2cm"),
    ], frq_type="Table"),
]

TOPIC = Topic(
    number="8.1", title="Finding the Average Value of a Function on an Interval",
    unit="Unit 8: Applications of Integration", ced=["CHA-4.B", "CHA-4.B.1"],
    goals=r"Find the average value of a function on an interval, find where the function equals it, and tell it apart from the average rate of change.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
