"""Topic 2.2: Defining the derivative of a function and using derivative notation.

CED: CHA-2.B.2 (the derivative function as a limit), CHA-2.B.3 (notations dy/dx, f'(x), y'),
CHA-2.B.4 (graphical, numerical, analytical, verbal), CHA-2.C.1 (tangent line equations).
The running example matches the video: f(x) = x^2, f'(x) = 2x, tangent at x = 3: y = 6x - 9.
"""
import sympy as sp

from calclib import (Variants, limchain, FRQ, MCQ, BigIdea, Check, Definition, Example, FigureRow, Formula, Item, Part,
                     Section, Table, Text, Topic, Video, VideoExample, expr, num, same, selfcheck)
from calclib.figs import graph

x, h, t = sp.symbols("x h t")


def deriv_def(f):
    return sp.simplify(sp.limit((f.subs(x, x + h) - f) / h, h, 0))


same("x^2", deriv_def(x**2), 2 * x)
same("tangent", sp.expand(9 + 6 * (x - 3)), 6 * x - 9)

FIG_F = graph("t2_2_f", [("x^2", -2.2, 2.2), ("2*x-1", 0.2, 2.2, "dashed")], xr=(-2.5, 2.5), yr=(-1, 4.5), closed=[(1, 1)],
              w="5.2cm", h="4.4cm", caption=r"$f(x) = x^2$ with its tangent line at $x=1$")
FIG_FP = graph("t2_2_fp", [("2*x", -2.2, 2.2)], xr=(-2.5, 2.5), yr=(-4.5, 4.5), closed=[(-1, -2), (0, 0), (1, 2)],
               w="5.2cm", h="4.4cm", ystep=2, caption=r"$f'(x) = 2x$: the slopes, plotted")

NOTES = [
    Video("s2_2.py::Lesson", "The derivative function", 3.5),

    Section("From one slope to a slope function"),
    Text(r"In Topic 2.1 we found $f'(a)$ at one point. Letting the point vary gives a new function that reports the "
         r"slope of the tangent line at \blank{every} $x$."),
    FigureRow([FIG_F, FIG_FP]),
    Definition("The derivative of $f$", (
        r"\[ f'(x) = \lim_{h\to0}\frac{f(x+h)-f(x)}{h}, \]"
        r"provided the limit exists. The domain of $f'$ is the set of $x$ where this limit \blank{exists}.")),
    VideoExample("The derivative of x squared", work="3cm"),

    Section("Notation"),
    Text(r"\textbf{Prime notation.} The derivative of $f$ is written $f'(x)$. If $y = f(x)$, then $y'$ means the same thing, written \blank{shorter}. "
         r"(Later we'll take derivatives of curves that aren't functions, and $y'$ is handy there.) Any letters work: if $g(t) = t^3$, its derivative is "
         r"\mblank{g'(t)}; if $A(r) = \pi r^2$, its derivative is \mblank{A'(r)}."),
    Text(r"\textbf{Leibniz notation.} A secant line's run is $\Delta x$ and its rise is $\Delta y$ ($\Delta$ is a capital delta, meaning ``change in''). "
         r"Shrink the triangle and the changes become tiny nudges, written $dx$ and $dy$ (a lowercase delta looks like a $d$). The tangent slope is "
         r"\[ \frac{dy}{dx}, \] the ratio of two tiny changes. It follows the variables: $\dfrac{ds}{dt}$ is how fast position $s$ changes per unit of \blank{time}."),
    Text(r"\textbf{An instruction.} $\frac{d}{dx}\left[x^2\right]$ means ``take the derivative of $x^2$ with respect to $x$'': \[ \frac{d}{dx}\left[x^2\right] = 2x. \]"),
    Text(r"\textbf{At a point.} $f'(3)$ means the derivative evaluated at $x = 3$. For $f(x) = x^2$, $f'(3) = 2 \cdot 3 = \mblank{6}$. "
         r"In Leibniz notation the same number is written \[ \left.\frac{dy}{dx}\right|_{x=3} = 6. \]"),
    Formula("Two meanings of every derivative value", (
        r"\textbf{Analytically:} $f'(a)$ is the \blank{instantaneous rate of change} of $f$ at $a$, in units of "
        r"\blank{output units per input unit}. \par "
        r"\textbf{Graphically:} $f'(a)$ is the \blank{slope of the tangent line} to $y = f(x)$ at $x = a$.")),

    Section("Tangent lines"),
    Formula("Point-slope form of a line", (
        r"The line through $(x_1, y_1)$ with slope $m$: \[ y - y_1 = m(x - x_1). \]")),
    Formula("Equation of the tangent line at $x = a$", (
        r"\[ y - f(a) = f'(a)\,(x - a) \]"
        r"You need two things: the point $\bigl(a, f(a)\bigr)$ and the slope \mblank{f'(a)}.")),
    Text(r"Leaving a tangent line in point-slope form is fine, \blank{unless} the question asks for a form, or you need to match a simplified multiple-choice answer."),
    VideoExample("A tangent line", work="2.6cm"),
    VideoExample("Units", work="2cm"),
    BigIdea(r"$f'$ is a function. Each of its values is both a rate of change and a slope."),
    Check(r"Use the definition to find $f'(x)$ for $f(x) = 3x^2 - x$.", expr("6*x-1"),
          limchain(0, [r"\frac{3(x+h)^2 - (x+h) - 3x^2 + x}{h}", r"\frac{6xh + 3h^2 - h}{h}", r"(6x + 3h - 1)"], r"6x - 1", var="h")),
]
same("check", deriv_def(3 * x**2 - x), 6 * x - 1)

# ---------------------------------------------------------------- practice
PR = [
    (r"f(x) = 5x - 2", 5 * x - 2, limchain(0, [r"\frac{5(x+h) - 2 - 5x + 2}{h}", r"\frac{5h}{h}", r"5"], r"5", var="h")),
    (r"f(x) = x^2 + 4x", x**2 + 4 * x, limchain(0, [r"\frac{(x+h)^2 + 4(x+h) - x^2 - 4x}{h}", r"\frac{2xh + h^2 + 4h}{h}", r"(2x + h + 4)"], r"2x + 4", var="h")),
    (r"f(x) = x^3", x**3, limchain(0, [r"\frac{(x+h)^3 - x^3}{h}", r"\frac{3x^2h + 3xh^2 + h^3}{h}", r"(3x^2 + 3xh + h^2)"], r"3x^2", var="h")),
    (r"f(x) = \dfrac{1}{x}", 1 / x, limchain(0, [r"\frac{\frac{1}{x+h} - \frac1x}{h}", r"\frac{x - (x+h)}{hx(x+h)}", r"\frac{-1}{x(x+h)}"], r"-\frac{1}{x^2}", var="h")),
    (r"f(x) = \sqrt{x}", sp.sqrt(x), "Multiply by the conjugate: " + limchain(0, [r"\frac{\sqrt{x+h} - \sqrt x}{h}", r"\frac{(x+h) - x}{h(\sqrt{x+h} + \sqrt x)}", r"\frac{1}{\sqrt{x+h} + \sqrt x}"], r"\frac{1}{2\sqrt x}", var="h")),
]
PRACTICE = [Item(rf"Use the definition of the derivative to find $f'(x)$ for ${tex}$.", expr(str(deriv_def(e))), sol, work="3cm")
            for tex, e, sol in PR]
PRACTICE += [
    Item(r"Find the equation for the line tangent to $f(x) = x^3$ at $x = 2$. Use your result from Problem 3.", expr("12*x-16"),
         r"Point $(2, 8)$, slope $3(4) = 12$: $y - 8 = 12(x - 2)$, so $y = 12x - 16$.", work="2.2cm"),
    Item(r"Find the equation for the line tangent to $f(x) = \dfrac1x$ at $x = -1$.", expr("-x-2"),
         r"Point $(-1, -1)$, slope $-\dfrac{1}{1} = -1$: $y + 1 = -(x + 1)$, so $y = -x - 2$.", work="2.2cm"),
    Item(r"If $y = \sqrt x$, find $\left.\dfrac{dy}{dx}\right|_{x=9}$.", num(sp.Rational(1, 6)), r"$\dfrac{1}{2\sqrt9} = \dfrac16$.",
         work="1.4cm"),
    Item(r"$C(n)$ is the cost, in dollars, of producing $n$ bicycles. Explain the meaning of $C'(200) = 85$, with units.",
         selfcheck(r"\$85\text{ per bike at } n=200"),
         r"When 200 bicycles are being produced, the cost is increasing at a rate of 85 dollars per bicycle.", work="2cm"),
    Item(r"The line $y = 4x - 3$ is tangent to the graph of $g$ at $x = 2$. Find $g(2)$ and $g'(2)$. Enter $g(2)$.", num(5),
         r"The tangent line touches the graph at $x = 2$: $g(2) = 4(2) - 3 = 5$. Its slope is $g'(2) = 4$.", work="1.8cm"),
]
same("p6", sp.expand(8 + 12 * (x - 2)), 12 * x - 16)
same("p7", sp.expand(-1 + (-1) * (x + 1)), -x - 2)
same("p8", sp.diff(sp.sqrt(x), x).subs(x, 9), sp.Rational(1, 6))

# extra practice (round 1)
PRACTICE += [
    Item(r"Use the definition of the derivative to find $f'(x)$ for $f(x) = 7 - 3x^2$.", expr("-6*x"),
         limchain(0, [r"\frac{7 - 3(x+h)^2 - 7 + 3x^2}{h}", r"\frac{-6xh - 3h^2}{h}", r"(-6x - 3h)"], "-6x", var="h"),
         work="3cm"),
    Item(r"Use the definition of the derivative to find $f'(x)$ for $f(x) = x^2 - 5x + 2$.", expr("2*x-5"),
         limchain(0, [r"\frac{(x+h)^2 - 5(x+h) + 2 - x^2 + 5x - 2}{h}", r"\frac{2xh + h^2 - 5h}{h}", r"(2x + h - 5)"],
                  "2x - 5", var="h"), work="3cm"),
    Item(r"Use the definition of the derivative to find $f'(x)$ for $f(x) = \dfrac{3}{x}$.", expr("-3/x**2"),
         limchain(0, [r"\frac{\frac{3}{x+h} - \frac3x}{h}", r"\frac{3x - 3(x+h)}{hx(x+h)}", r"\frac{-3}{x(x+h)}"],
                  r"-\frac{3}{x^2}", var="h"), work="3cm"),
    Item(r"Use the definition of the derivative to find $f'(x)$ for $f(x) = \sqrt{x + 2}$.", expr("1/(2*sqrt(x+2))"),
         "Multiply by the conjugate: " + limchain(0, [r"\frac{\sqrt{x+h+2} - \sqrt{x+2}}{h}",
                                                      r"\frac{(x+h+2) - (x+2)}{h(\sqrt{x+h+2} + \sqrt{x+2})}",
                                                      r"\frac{1}{\sqrt{x+h+2} + \sqrt{x+2}}"], r"\frac{1}{2\sqrt{x+2}}", var="h"),
         work="3.4cm"),
    Item(r"Using your answer to the previous problem, find the slope of $y = \sqrt{x+2}$ at $x = 7$.", num(sp.Rational(1, 6)),
         r"$\dfrac{1}{2\sqrt{9}} = \dfrac16$.", work="1.4cm"),
    Item(r"Find the equation for the line tangent to $f(x) = 7 - 3x^2$ at $x = 1$. Use your result from above.", expr("10-6*x"),
         r"Point $(1, 4)$, slope $f'(1) = -6$: $y - 4 = -6(x - 1)$, so $y = -6x + 10$.", work="2cm"),
    Item(r"For $f(x) = x^2 - 5x + 2$, at what $x$ is the tangent line horizontal?", num(sp.Rational(5, 2)),
         r"Horizontal means slope $0$: $f'(x) = 2x - 5 = 0$, so $x = \frac52$.", work="1.6cm"),
    Item(r"$\displaystyle\lim_{h\to0}\frac{\cos(x+h) - \cos x}{h}$ is the derivative of which function?", selfcheck(r"\cos x"),
         r"It has the form $\displaystyle\lim_{h\to0}\frac{f(x+h) - f(x)}{h}$ with $f(x) = \cos x$.", work="1.2cm"),
    Item(r"$P(t)$ is the population of a town, in people, $t$ years after 2020. Explain the meaning of $P'(3) = -140$, "
         r"with units.", selfcheck(r"\text{decreasing 140 people/yr in 2023}"),
         r"In 2023 the population was decreasing at a rate of 140 people per year.", work="1.8cm"),
    Item(r"Write three different notations for the derivative of $y = f(x)$.", selfcheck(r"f'(x),\ y',\ \frac{dy}{dx}"),
         r"Any three of $f'(x)$, $y'$, $\dfrac{dy}{dx}$, $\dfrac{d}{dx}f(x)$.", work="1.2cm"),
]
same("x1 a", deriv_def(7 - 3 * x**2), -6 * x)
same("x1 b", deriv_def(x**2 - 5 * x + 2), 2 * x - 5)
same("x1 c", deriv_def(3 / x), -3 / x**2)
same("x1 d", deriv_def(sp.sqrt(x + 2)), 1 / (2 * sp.sqrt(x + 2)))
same("x1 e", (1 / (2 * sp.sqrt(x + 2))).subs(x, 7), sp.Rational(1, 6))
same("x1 f", sp.expand(4 - 6 * (x - 1)), 10 - 6 * x)

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Use the definition of the derivative to find $f'(x)$ for $f(x) = 2x^2 + 1$.", expr("4*x"),
             limchain(0, [r"\frac{2(x+h)^2 + 1 - 2x^2 - 1}{h}", r"\frac{4xh + 2h^2}{h}", r"(4x + 2h)"], r"4x", var="h"), work="3cm"),
        Item(r"Use the definition of the derivative to find $f'(x)$ for $f(x) = x^2 - 3x$.", expr("2*x-3"),
             limchain(0, [r"\frac{(x+h)^2 - 3(x+h) - x^2 + 3x}{h}", r"\frac{2xh + h^2 - 3h}{h}", r"(2x + h - 3)"], r"2x - 3", var="h"), work="3cm"),
        Item(r"Use the definition of the derivative to find $f'(x)$ for $f(x) = 5 - x^2$.", expr("-2*x"),
             limchain(0, [r"\frac{5 - (x+h)^2 - 5 + x^2}{h}", r"\frac{-2xh - h^2}{h}", r"(-2x - h)"], r"-2x", var="h"), work="3cm"),
    ),
    Variants(
        Item(r"$f(x) = 2x^2 + 1$ has $f'(x) = 4x$. Find the equation of the tangent line at $x = 1$.", expr("4*x-1"),
             r"Point $(1, 3)$, slope $f'(1) = 4$: $y - 3 = 4(x - 1)$, so $y = 4x - 1$.", work="2cm"),
        Item(r"$f(x) = x^2 - 3x$ has $f'(x) = 2x - 3$. Find the equation of the tangent line at $x = 2$.", expr("x-4"),
             r"Point $(2, -2)$, slope $f'(2) = 1$: $y + 2 = x - 2$, so $y = x - 4$.", work="2cm"),
        Item(r"$f(x) = 5 - x^2$ has $f'(x) = -2x$. Find the equation of the tangent line at $x = -1$.", expr("2*x+6"),
             r"Point $(-1, 4)$, slope $f'(-1) = 2$: $y - 4 = 2(x + 1)$, so $y = 2x + 6$.", work="2cm"),
    ),
    Variants(
        MCQ(r"Which expression equals $f'(5)$?",
            [r"$\displaystyle\lim_{h\to0}\frac{f(5+h)}{h}$", r"$\displaystyle\lim_{h\to0}\frac{f(5+h) - f(5)}{h}$",
             r"$\displaystyle\lim_{x\to5}\frac{f(x) - f(5)}{x + 5}$", r"$\dfrac{f(5+h) - f(5)}{h}$"], "B",
            r"The definition at $x = 5$.", why_not={"A": "left out $f(5)$", "C": "the denominator should be $x - 5$", "D": "no limit: that is an average rate"}),
        MCQ(r"Which expression equals $g'(-2)$?",
            [r"$\displaystyle\lim_{x\to-2}\frac{g(x) - g(-2)}{x + 2}$", r"$\displaystyle\lim_{x\to2}\frac{g(x) - g(2)}{x - 2}$",
             r"$\displaystyle\lim_{h\to0}\frac{g(-2+h) - g(2)}{h}$", r"$\dfrac{g(x) - g(-2)}{x + 2}$"], "A",
            r"The $x \to a$ form with $a = -2$: the denominator is $x - (-2) = x + 2$.",
            why_not={"B": "that's $g'(2)$", "C": "mixed $-2$ and $2$", "D": "no limit: that is an average rate"}),
        MCQ(r"$\displaystyle\lim_{h\to0}\frac{\sqrt{9+h} - 3}{h}$ is the derivative of which function, at which input?",
            [r"$f(x) = \sqrt{x}$ at $x = 3$", r"$f(x) = \sqrt{x}$ at $x = 9$", r"$f(x) = x^2$ at $x = 9$", r"$f(x) = \sqrt{x} - 3$ at $x = 0$"], "B",
            r"It matches $\frac{f(a+h) - f(a)}{h}$ with $f(x) = \sqrt x$ and $a = 9$, since $\sqrt9 = 3$.",
            why_not={"A": "$3$ is $f(9)$, not the input"}),
    ),
    Variants(
        MCQ(r"$T(t)$ is the temperature, in $^\circ$C, $t$ hours after sunrise, and $T'(3) = 2.5$. Which is correct?",
            [r"The temperature is $2.5^\circ$C at 3 hours.", r"The temperature rises $2.5^\circ$C in the first 3 hours.",
             r"At 3 hours after sunrise, the temperature is increasing at $2.5^\circ$C per hour.",
             r"It takes 2.5 hours for the temperature to rise 3 degrees."], "C", r"A derivative is a rate, at an instant, with units."),
        MCQ(r"$W(d)$ is the weight of a puppy, in kilograms, $d$ days after birth, and $W'(20) = 0.1$. Which is correct?",
            [r"At 20 days old, the puppy is gaining weight at 0.1 kilograms per day.", r"The puppy weighs 0.1 kilograms at 20 days.",
             r"The puppy gains 0.1 kilograms in its first 20 days.", r"The puppy gains 20 kilograms per day."], "A",
            r"A derivative is a rate at an instant: kilograms per day, at day 20."),
        MCQ(r"$V(p)$ is the volume of a gas, in liters, at pressure $p$ atmospheres, and $V'(2) = -5$. Which is correct?",
            [r"At pressure 2, the volume is 5 liters.", r"The volume drops 5 liters between 0 and 2 atmospheres.",
             r"At pressure 2 atmospheres, the volume is decreasing at 5 liters per atmosphere.", r"The pressure drops 5 atmospheres per liter."], "C",
            r"The derivative is the rate of change of volume per unit of pressure, at $p = 2$."),
    ),
    Variants(
        Item(r"If $y = x^2 - 6x$, find the value of $x$ where the tangent line is horizontal. (Hint: $\dfrac{dy}{dx} = 2x - 6$.)", num(3),
             r"A horizontal tangent has slope $0$: $2x - 6 = 0$, so $x = 3$.", work="1.6cm"),
        Item(r"If $y = 3x^2 + 12x$, find the value of $x$ where the tangent line is horizontal. (Hint: $\dfrac{dy}{dx} = 6x + 12$.)", num(-2),
             r"$6x + 12 = 0$, so $x = -2$.", work="1.6cm"),
        Item(r"If $y = x^2 + 5x$, find the value of $x$ where the tangent line has slope $1$. (Hint: $\dfrac{dy}{dx} = 2x + 5$.)", num(-2),
             r"$2x + 5 = 1$, so $x = -2$.", work="1.6cm"),
    ),
]
same("q1", deriv_def(2 * x**2 + 1), 4 * x)
same("q versions", [deriv_def(x**2 - 3 * x), deriv_def(5 - x**2), sp.expand(-2 + (x - 2)), sp.expand(4 + 2 * (x + 1))],
     [2 * x - 3, -2 * x, x - 4, 2 * x + 6])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$\displaystyle\lim_{h\to0}\frac{(3+h)^4 - 81}{h}$ is", [r"$0$", r"$27$", r"$81$", r"$108$"], "D",
        r"It is $f'(3)$ for $f(x) = x^4$. Expanding: " + limchain(0, [r"\frac{(3+h)^4 - 81}{h}", r"(108 + 54h + 12h^2 + h^3)"], r"108", var="h") + ".",
        why_not={"C": "that is $f(3)$", "B": "that is $3^3$"}),
    MCQ(r"The line tangent to the graph of $f$ at $x = -2$ is $y = 3x + 5$. What are $f(-2)$ and $f'(-2)$?",
        [r"$f(-2) = -1$, $f'(-2) = 3$", r"$f(-2) = 3$, $f'(-2) = -1$", r"$f(-2) = 5$, $f'(-2) = 3$", r"$f(-2) = -1$, $f'(-2) = 5$"], "A",
        r"On the tangent line, $x = -2$ gives $y = -1$; the slope is $3$."),
    MCQ(r"If $f(x) = \dfrac{1}{x+1}$, then $f'(1)$ is", [r"$\dfrac12$", r"$-\dfrac12$", r"$-\dfrac14$", r"$\dfrac14$"], "C",
        r"From the definition, $f'(x) = -\dfrac{1}{(x+1)^2}$, so $f'(1) = -\dfrac14$.", why_not={"B": "forgot to square"}),
    MCQ(r"$P(t)$ is the population of a town, in people, $t$ years after 2000. What are the units of $P'(t)$?",
        [r"people", r"years", r"people per year", r"years per person"], "C", r"A derivative has units of output per input."),
]
same("m1", sp.limit(((3 + h)**4 - 81) / h, h, 0), 108)
same("m3", sp.diff(1 / (x + 1), x).subs(x, 1), sp.Rational(-1, 4))

FRQS = [
    FRQ("The derivative from its definition", r"Let $f(x) = x^2 - 3x$.", [
        Part("a", r"Use the limit definition of the derivative to find $f'(x)$.", expr("2*x-3"),
             limchain(0, [r"\frac{(x+h)^2 - 3(x+h) - x^2 + 3x}{h}", r"\frac{2xh + h^2 - 3h}{h}", r"(2x + h - 3)"], r"2x - 3", var="h"),
             [(1, "correct difference quotient"), (1, "simplifies and takes the limit"), (1, "$2x - 3$")], work="3.4cm"),
        Part("b", r"Write an equation for the line tangent to the graph of $f$ at $x = 4$.", expr("5*x-16"),
             r"$f(4) = 4$ and $f'(4) = 5$: $y - 4 = 5(x - 4)$, or $y = 5x - 16$.", [(1, "point and slope"), (1, "equation")],
             work="2.4cm"),
        Part("c", r"At what point on the graph of $f$ is the tangent line horizontal? Enter the $x$-coordinate.", num(sp.Rational(3, 2)),
             r"$f'(x) = 0$ when $x = \frac32$; the point is $\left(\frac32, -\frac94\right)$.", [(1, "$x = \\frac32$ with $y$")],
             work="2cm"),
    ], frq_type="Derivative definition / tangent line"),
]
same("frq a", deriv_def(x**2 - 3 * x), 2 * x - 3)
same("frq b", sp.expand(4 + 5 * (x - 4)), 5 * x - 16)

TOPIC = Topic(
    number="2.2", title="Defining the Derivative of a Function and Using Derivative Notation",
    unit="Unit 2: Differentiation", ced=["CHA-2.B", "CHA-2.B.2", "CHA-2.B.3", "CHA-2.B.4", "CHA-2.C", "CHA-2.C.1"],
    goals=r"Find derivative functions from the limit definition, read and write derivative notation, and write tangent lines.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
