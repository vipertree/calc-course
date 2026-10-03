"""Topic 4.6: Approximating values of a function using local linearity and linearization.

CED: CHA-3.F (CHA-3.F.1, CHA-3.F.2): near x = a the tangent line L(x) = f(a) + f'(a)(x - a) approximates f; the
approximation is better closer to a, and whether it is too big or too small depends on which side of the tangent line
the curve lies. (Concavity gets its name in 5.6; here the picture does the work.) Worked examples: sqrt(26) from x = 25,
an estimate from given f(2), f'(2), cube root of 8.12.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Text, Topic, Variants, Video, expr, num,
                     same, selfcheck)

x = sp.symbols("x")


def lin(f, a, at):
    """The tangent-line value at `at` for f linearized at a."""
    return sp.nsimplify(f.subs(x, a) + sp.diff(f, x).subs(x, a) * (at - a))


same("sqrt26", lin(sp.sqrt(x), 25, 26), sp.Rational(51, 10))
same("given", 7 + (-3) * sp.Rational(1, 10), sp.Rational(67, 10))
same("cbrt", lin(sp.cbrt(x), 8, sp.Rational(812, 100)), sp.Rational(201, 100))

NOTES = [
    Video("s4_6.py::Lesson", "Zoom in on a curve", 4),

    Section("Local linearity"),
    Text(r"Zoom in far enough on a differentiable function and its graph looks like a straight line: its \blank{tangent line}. "
         r"Close to the point of tangency, the line and the curve are nearly the same, so the line's value is a good estimate of the function's."),
    Formula("The linearization of $f$ at $x = a$", (
        r"\[ L(x) = f(a) + f'(a)(x - a) \] "
        r"For $x$ near $a$, \[ f(x) \approx L(x). \] This is the point-slope form of the tangent line, with the point $\left(a, f(a)\right)$ and slope $f'(a)$. "
        r"You don't need to think of it as a new formula: write the equation of the tangent line, a skill you already have, and "
        r"evaluate it at the $x$ you care about. Start at a point and move along the slope a little.")),
    Text(r"\textbf{Choosing $a$.} Pick an $a$ close to the $x$ you want, where $f(a)$ and $f'(a)$ are easy to find exactly. To estimate $\sqrt{26}$, "
         r"use $a = \mblank{25}$."),
    VideoExample('Using given values', work="2cm"),

    Section("Too big or too small?"),
    Text(r"If the curve lies \blank{below} its tangent line near $a$ (it bends down away from the line), the estimate $L(x)$ is an "
         r"\blank{overestimate}. If the curve lies above its tangent line (it bends up), $L(x)$ is an \blank{underestimate}."),
    Text(r"In Unit 5 you will name these shapes: concave down and concave up. A negative second derivative means the curve bends down."),
    BigIdea(r"Up close, a curve is its tangent line. Use the tangent line to estimate nearby values, and look at which way the curve bends to "
            r"tell whether the estimate is too big or too small."),
    Check(r"$g(1) = 3$ and $g'(1) = -2$. Estimate $g(1.1)$.", num(sp.Rational(28, 10)), r"\[ 3 + (-2)(0.1) = 2.8. \]"),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Find the linearization of $f(x) = x^3$ at $x = 2$.", expr(12 * x - 16, var="x"), r"$f(2) = 8$, $f'(2) = 12$: $L(x) = 8 + 12(x - 2) = 12x - 16$.", work="1.8cm"),
    Item(r"Use a linearization to estimate $\sqrt{49.7}$.", num(sp.Rational(705, 100)), r"At $a = 49$: $7 + \frac{1}{14}(0.7) = 7.05$.", work="2cm"),
    Item(r"Use a linearization to estimate $\sqrt{15.6}$.", num(sp.Rational(395, 100)), r"At $a = 16$: $4 + \frac18(-0.4) = 3.95$.", work="2cm"),
    Item(r"Use a linearization to estimate $\sqrt[3]{27.27}$.", num(sp.Rational(301, 100)), r"At $a = 27$: $3 + \frac{1}{27}(0.27) = 3.01$.", work="2cm"),
    Item(r"Find the linearization of $f(x) = \ln x$ at $x = 1$, and use it to estimate $\ln 1.05$.", num(sp.Rational(5, 100)),
         r"$L(x) = 0 + 1(x - 1) = x - 1$, so $\ln 1.05 \approx 0.05$.", work="2cm"),
    Item(r"Find the linearization of $f(x) = e^x$ at $x = 0$, and use it to estimate $e^{-0.02}$.", num(sp.Rational(98, 100)),
         r"$L(x) = 1 + x$, so $e^{-0.02} \approx 0.98$.", work="2cm"),
    Item(r"Find the linearization of $f(x) = \sin x$ at $x = 0$, and use it to estimate $\sin(0.03)$.", num(sp.Rational(3, 100)),
         r"$L(x) = 0 + 1(x - 0) = x$, so $\sin(0.03) \approx 0.03$.", work="2cm"),
    Item(r"$f(3) = -1$ and $f'(3) = 4$. Estimate $f(2.9)$.", num(sp.Rational(-14, 10)), r"$-1 + 4(-0.1) = -1.4$.", work="1.6cm"),
    Item(r"$h(10) = 250$ and $h'(10) = -12$. Estimate $h(10.5)$.", num(244), r"$250 + (-12)(0.5) = 244$.", work="1.6cm"),
    Item(r"Find the linearization of $f(x) = \dfrac{1}{x}$ at $x = 2$, and use it to estimate $\dfrac{1}{2.1}$.", num(sp.Rational(19, 40)),
         r"$f(2) = \frac12$, $f'(2) = -\frac14$. $L(2.1) = \frac12 - \frac14(0.1) = 0.475$.", work="2.2cm"),
    Item(r"Kenji's estimate of $\sqrt{26}$ from the tangent line at $x = 25$ is $5.1$. The graph of $y = \sqrt x$ bends down, below its tangent lines. "
         r"Is $5.1$ too big or too small?", selfcheck(r"\text{too big}"), r"The curve lies below the tangent line, so the line's value $5.1$ is an overestimate.", work="1.6cm"),
    Item(r"The graph of $f$ bends up, above its tangent lines, near $x = 1$. Is $L(1.2)$ an overestimate or an underestimate of $f(1.2)$?",
         selfcheck(r"\text{underestimate}"), r"The curve lies above the line, so the line's value is too small.", work="1.4cm"),
    Item(r"The temperature of a pie is $T(5) = 180$ degrees and is falling at $6$ degrees per minute at $t = 5$. Estimate $T(5.5)$.", num(177),
         r"$T'(5) = -6$: $180 - 6(0.5) = 177$ degrees.", work="1.6cm"),
    Item(r"Find the equation for the line tangent to $y = \sqrt{x + 3}$ at $x = 1$, and use it to estimate $\sqrt{4.2}$.", num(sp.Rational(205, 100)),
         r"At $x = 1$: $y = 2$, slope $\frac{1}{4}$. $L(x) = 2 + \frac14(x - 1)$; $\sqrt{4.2}$ is $x = 1.2$, so $2 + 0.05 = 2.05$.", work="2.4cm"),
]
same("p", [lin(x**3, 2, x), lin(sp.sqrt(x), 49, sp.Rational(497, 10)), lin(sp.sqrt(x), 16, sp.Rational(156, 10)), lin(sp.cbrt(x), 27, sp.Rational(2727, 100)),
           lin(sp.log(x), 1, sp.Rational(105, 100)), lin(sp.exp(x), 0, sp.Rational(-2, 100)), lin(sp.sin(x), 0, sp.Rational(3, 100)), lin(1 / x, 2, sp.Rational(21, 10)),
           lin(sp.sqrt(x + 3), 1, sp.Rational(12, 10))],
     [12 * x - 16, sp.Rational(705, 100), sp.Rational(395, 100), sp.Rational(301, 100), sp.Rational(5, 100), sp.Rational(98, 100), sp.Rational(3, 100),
      sp.Rational(19, 40), sp.Rational(205, 100)])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Use a linearization to estimate $\sqrt{36.6}$.", num(sp.Rational(605, 100)), r"At $a = 36$: $6 + \frac{1}{12}(0.6) = 6.05$.", work="1.8cm"),
        Item(r"Use a linearization to estimate $\sqrt{64.8}$.", num(sp.Rational(805, 100)), r"At $a = 64$: $8 + \frac{1}{16}(0.8) = 8.05$.", work="1.8cm"),
        Item(r"Use a linearization to estimate $\sqrt{99}$.", num(sp.Rational(995, 100)), r"At $a = 100$: $10 + \frac{1}{20}(-1) = 9.95$.", work="1.8cm"),
    ),
    Variants(
        Item(r"$f(2) = 5$ and $f'(2) = -3$. Estimate $f(2.1)$.", num(sp.Rational(47, 10)), r"$5 - 3(0.1) = 4.7$.", work="1.4cm"),
        Item(r"$f(6) = 1$ and $f'(6) = 8$. Estimate $f(5.9)$.", num(sp.Rational(2, 10)), r"$1 + 8(-0.1) = 0.2$.", work="1.4cm"),
        Item(r"$f(0) = 4$ and $f'(0) = 0.5$. Estimate $f(0.4)$.", num(sp.Rational(42, 10)), r"$4 + 0.5(0.4) = 4.2$.", work="1.4cm"),
    ),
    Variants(
        Item(r"Find the linearization of $f(x) = x^2 + 1$ at $x = 3$.", expr(6 * x - 8, var="x"), r"$10 + 6(x - 3) = 6x - 8$.", work="1.6cm"),
        Item(r"Find the linearization of $f(x) = x^3 - x$ at $x = 1$.", expr(2 * x - 2, var="x"), r"$0 + 2(x - 1) = 2x - 2$.", work="1.6cm"),
        Item(r"Find the linearization of $f(x) = 4\sqrt x$ at $x = 4$.", expr(x + 4, var="x"), r"$8 + 1(x - 4) = x + 4$.", work="1.6cm"),
    ),
    Variants(
        MCQ(r"The graph of $f$ lies below its tangent line at $x = a$. The estimate $L(a + 0.1)$ is", [r"an overestimate", r"an underestimate", r"exact",
            r"impossible to judge"], "A", r"The line is above the curve, so its values are too big."),
        MCQ(r"The graph of $f$ lies above its tangent line at $x = a$. The estimate $L(a - 0.1)$ is", [r"an overestimate", r"an underestimate", r"exact",
            r"impossible to judge"], "B", r"The line is below the curve, so its values are too small."),
        MCQ(r"$f$ is a linear function. The linearization of $f$ at any point gives estimates that are", [r"overestimates", r"underestimates", r"exact",
            r"impossible to judge"], "C", r"A line's tangent line is itself."),
    ),
    Variants(
        MCQ(r"To estimate $\sqrt[3]{7.9}$ with a linearization, the best choice of $a$ is", [r"$a = 7.9$", r"$a = 1$", r"$a = 8$", r"$a = 0$"], "C",
            r"$8$ is close to $7.9$ and $\sqrt[3]{8} = 2$ is exact.", why_not={"A": "you can't evaluate the function there exactly; that's the problem"}),
        MCQ(r"To estimate $\ln(0.98)$ with a linearization, the best choice of $a$ is", [r"$a = 0$", r"$a = e$", r"$a = 0.98$", r"$a = 1$"], "D",
            r"$\ln 1 = 0$ exactly, and $1$ is close to $0.98$.", why_not={"A": "$\\ln 0$ is undefined"}),
        MCQ(r"To estimate $\cos(0.05)$ with a linearization, the best choice of $a$ is", [r"$a = 0$", r"$a = \frac{\pi}{2}$", r"$a = 0.05$", r"$a = 1$"], "A",
            r"$\cos 0 = 1$ exactly, and $0$ is close to $0.05$."),
    ),
]
same("q", [lin(sp.sqrt(x), 36, sp.Rational(366, 10)), lin(sp.sqrt(x), 64, sp.Rational(648, 10)), lin(sp.sqrt(x), 100, 99),
           lin(x**2 + 1, 3, x), lin(x**3 - x, 1, x), lin(4 * sp.sqrt(x), 4, x)],
     [sp.Rational(605, 100), sp.Rational(805, 100), sp.Rational(995, 100), 6 * x - 8, 2 * x - 2, x + 4])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"The line tangent to the graph of $f$ at $x = 3$ is $y = 2x - 1$. What is the approximation of $f(3.2)$ from this line?",
        [r"$5$", r"$5.4$", r"$5.2$", r"$6.4$"], "B", r"$2(3.2) - 1 = 5.4$."),
    MCQ(r"Let $f(x) = \sqrt{x}$. The tangent line at $x = 9$ is used to estimate $f(9.6)$. The estimate is", [r"$3.1$, an overestimate", r"$3.1$, an underestimate",
        r"$3.2$, an overestimate", r"$3.2$, an underestimate"], "A",
        r"$3 + \frac16(0.6) = 3.1$. The graph of $\sqrt x$ bends down, below its tangent lines, so $3.1$ is too big."),
    MCQ(r"$g(1) = 4$, $g(1.5) = 3$ and $g(2) = 1$. A student estimates $g'(1.5)$ with the difference quotient from $x = 1$ to $x = 2$ and uses it in "
        r"the tangent line at $x = 1.5$ to estimate $g(1.6)$. The estimate is", [r"$2.6$", r"$3.3$", r"$2.7$", r"$3.1$"], "C",
        r"$g'(1.5) \approx \frac{1 - 4}{1} = -3$. $3 - 3(0.1) = 2.7$."),
    MCQ(r"For which value of $x$ does the linearization of $f(x) = x^2$ at $x = 5$ give the worst estimate?", [r"$x = 5.1$", r"$x = 4.9$", r"$x = 5.5$", r"$x = 6$"], "D",
        r"The error is $(x - 5)^2$, largest for the $x$ farthest from $5$."),
]
same("m", [2 * sp.Rational(32, 10) - 1, lin(sp.sqrt(x), 9, sp.Rational(96, 10)), 3 - 3 * sp.Rational(1, 10)], [sp.Rational(54, 10), sp.Rational(31, 10), sp.Rational(27, 10)])

FRQS = [
    FRQ("A melting snowbank", (
        r"The depth of a snowbank is modeled by a twice-differentiable function $D$, where $D(t)$ is measured in inches and $t$ is "
        r"measured in days. It is known that $D(0) = 30$ and $D'(t) = -\dfrac{12}{t + 2}$ for $t \ge 0$."), [
        Part("a", r"Find $D'(0)$. Using correct units, interpret the meaning of $D'(0)$ in the context of the problem.",
             num(-6, display=r"-6\ \text{inches per day}"),
             r"$D'(0) = -\dfrac{12}{2} = -6$. At time $t = 0$, the depth of the snowbank is decreasing at a rate of $6$ inches per day.",
             [(1, "$D'(0) = -6$"), (1, "interpretation with units")], work="2.4cm"),
        Part("b", r"Write an equation for the line tangent to the graph of $D$ at $t = 0$. Use the tangent line to approximate $D(0.5)$.",
             num(27),
             r"The tangent line is $y = 30 - 6t$, so $D(0.5) \approx 30 - 6(0.5) = 27$ inches.",
             [(1, "tangent line equation"), (1, "approximation $27$")], work="2.4cm"),
        Part("c", r"Find $D''(t)$. Use $D''(t)$ to determine whether the approximation in part (b) is an underestimate or an "
                  r"overestimate of $D(0.5)$. Give a reason for your answer.", selfcheck(r"\text{Underestimate}"),
             r"$D''(t) = \dfrac{12}{(t + 2)^2} > 0$ for $t \ge 0$, so the graph of $D$ is concave up on $0 \le t \le 0.5$ and lies above "
             r"its tangent line there. The approximation is an underestimate.",
             [(1, "$D''(t)$"), (1, "underestimate, with the reason $D'' > 0$")], work="2.6cm"),
    ], frq_type="Linearization"),
]
tt = sp.symbols("t")
Dp6 = -12 / (tt + 2)
same("frq", [Dp6.subs(tt, 0), 30 + Dp6.subs(tt, 0) * sp.Rational(1, 2)], [-6, 27])
same("frq c", sp.diff(Dp6, tt), 12 / (tt + 2)**2)

TOPIC = Topic(
    number="4.6", title="Approximating Values of a Function Using Local Linearity and Linearization",
    unit="Unit 4: Contextual Applications of Differentiation", ced=["CHA-3.F", "CHA-3.F.1", "CHA-3.F.2"],
    goals=r"Use the tangent line to approximate a function's values near a point, and tell whether the estimate is too big or too small.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
