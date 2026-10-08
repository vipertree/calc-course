"""AP Calculus AB Practice Exam 1. Original questions in the AP format:
Section I Part A (30 MC, no calculator, 60 min), Part B (15 MC, calculator, 45 min);
Section II Part A (2 FRQ, calculator, 30 min), Part B (4 FRQ, no calculator, 60 min).

Every keyed answer is computed here with sympy and checked against what the question prints. Calculator answers
are checked numerically to three decimal places, the AP standard. Each question carries the syllabus topic it
tests, which the score report uses to point back to lessons.
"""
import sympy as sp

from calclib import FRQ, MCQ, Exam, Part, check, close, expr, limchain, num, same, selfcheck
from calclib.figs import graph, region, slope_field

x, t, y, h = sp.symbols("x t y h", real=True)
I = lambda f, a, b, v=x: sp.simplify(sp.integrate(f, (v, a, b)))
N = lambda f, a, b, v=x: float(sp.Integral(f, (v, a, b)).evalf(30))


def pick(stem, right, wrong, letter, solution, why=None, calc=False, topic="", figure=None):
    """An MCQ with the keyed answer at a planned letter. why maps a wrong choice's text to the slip behind it."""
    k = "ABCD".index(letter)
    choices = list(wrong)
    choices.insert(k, right)
    why_not = {"ABCD"[choices.index(c)]: r for c, r in (why or {}).items()}
    return MCQ(stem, choices, letter, solution, why_not=why_not, calc=calc, topic=topic, figure=figure)


def f3(v):
    """A calculator answer, three decimal places."""
    return f"${v:.3f}$"


# ====================================================================== Section I, Part A: no calculator
same("A1", sp.limit((x**2 - 9) / (x**2 - x - 6), x, 3), sp.Rational(6, 5))
same("A2", sp.limit((4 * x**3 - x) / (2 - 5 * x**3), x, sp.oo), -sp.Rational(4, 5))
k_ = sp.symbols("k")
same("A3", sp.solve(sp.Eq(k_ * 2 + 1, 4 - k_), k_), [1])
check("A4 hole at 1", sp.limit((x - 1) / (x**2 - 1), x, 1) == sp.Rational(1, 2))
check("A4 asymptote at -1", sp.limit((x - 1) / (x**2 - 1), x, -1, "+") == sp.oo)
same("A5", sp.limit((sp.sin(sp.pi / 3 + h) - sp.sin(sp.pi / 3)) / h, h, 0), sp.Rational(1, 2))
same("A6", sp.diff(x**2 * sp.exp(x), x).subs(x, 1), 3 * sp.E)
same("A7", sp.diff((2 * x + 1) / (x - 1), x).subs(x, 2), -3)
same("A8", sp.diff(sp.sin(2 * x)**3, x), 6 * sp.sin(2 * x)**2 * sp.cos(2 * x))
# A9 table: f(1)=4, f'(1)=2, g(1)=3, g'(1)=-2; f(3)=7, f'(3)=5, g(3)=1, g'(3)=6
TAB9 = {1: (4, 2, 3, -2), 3: (7, 5, 1, 6)}
same("A9", TAB9[TAB9[1][2]][1] * TAB9[1][3], -10)
fA10 = x**3 + 2 * x + 1
same("A10", [fA10.subs(x, 1), 1 / sp.diff(fA10, x).subs(x, 1)], [4, sp.Rational(1, 5)])
same("A11", sp.diff(sp.atan(3 * x), x).subs(x, sp.Rational(1, 3)), sp.Rational(3, 2))
yx = sp.Function("y")(x)
dA12 = sp.solve(sp.diff(x**2 + x * yx + yx**2 - 7, x), sp.diff(yx, x))[0]
same("A12", [1 + 2 + 4, dA12.subs(yx, 2).subs(x, 1)], [7, -sp.Rational(4, 5)])
same("A13", sp.diff(x * sp.exp(2 * x), x, 2).subs(x, 0), 4)
vA14 = sp.diff(t**3 - 6 * t**2 + 9 * t, t)
check("A14 moving left on (1, 3)", sp.solve_univariate_inequality(vA14 < 0, t, relational=False) == sp.Interval.open(1, 3))
r_ = sp.symbols("r", positive=True)
same("A15", sp.diff(sp.Rational(4, 3) * sp.pi * r_**3, r_).subs(r_, 5) * 2, 200 * sp.pi)
same("A16", sp.sqrt(9) + sp.diff(sp.sqrt(x), x).subs(x, 9) * sp.Rational(6, 10), sp.Rational(31, 10))
same("A17", sp.limit((sp.exp(2 * x) - 1 - 2 * x) / x**2, x, 0), 2)
same("A18", sp.solve(sp.Eq(2 * x - 4, ((3**2 - 12) - 0) / 3), x), [sp.Rational(3, 2)])
same("A19", max((x**3 - 3 * x).subs(x, c) for c in (0, 1, 2)), 2)
fpA20 = x * (x - 2)**2
check("A20 sign change at 0 only", fpA20.subs(x, -0.5) < 0 < fpA20.subs(x, 0.5) and fpA20.subs(x, 1.5) > 0 and fpA20.subs(x, 2.5) > 0)
check("A21 concave down on (-1, 1)", sp.solve_univariate_inequality(sp.diff(x**4 - 6 * x**2, x, 2) < 0, x, relational=False) == sp.Interval.open(-1, 1))
XS23, FS23 = [0, 2, 5, 6], [4, 1, 3, 7]
right23 = sum((b - a) * v for a, b, v in zip(XS23, XS23[1:], FS23[1:]))
left23 = sum((b - a) * v for a, b, v in zip(XS23, XS23[1:], FS23))
same("A23", [right23, left23], [18, 14])
same("A24", sp.diff(sp.Integral(sp.sqrt(1 + t**3), (t, 0, x**2)), x).subs(x, 2), 4 * sp.sqrt(65))
same("A25", 2 * (8 - 3) + (3 - 1), 12)
same("A26", I(2 * x + 1 / x, 1, sp.E), sp.E**2)
same("A27", I(x * sp.exp(x**2), 0, 1), (sp.E - 1) / 2)
same("A28", sp.diff(sp.atan(x + 2), x), 1 / (x**2 + 4 * x + 5))
same("A29", [sp.diff(3 * sp.exp(x**2 / 2), x) - x * 3 * sp.exp(x**2 / 2), 3 * sp.exp(0)], [0, 3])
same("A30", [sp.solve(sp.Eq(4 - x**2, x + 2), x), I(4 - x**2 - (x + 2), -2, 1)], [[-2, 1], sp.Rational(9, 2)])

TABLE9 = (r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $x$ & $f(x)$ & $f'(x)$ & $g(x)$ & $g'(x)$ \\ \hline "
          + r" \\ ".join(f"${k}$ & ${a}$ & ${b}$ & ${c}$ & ${d}$" for k, (a, b, c, d) in TAB9.items()) + r"\end{tabular}}")
TABLE23 = (r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $x$ & " + " & ".join(f"${v}$" for v in XS23)
           + r" \\ \hline $f(x)$ & " + " & ".join(f"${v}$" for v in FS23) + r"\end{tabular}}")

PART_A = [
    pick(r"$\displaystyle\lim_{x\to 3} \frac{x^2 - 9}{x^2 - x - 6}$ is", r"$\frac65$", [r"$1$", r"$0$", r"nonexistent"], "B",
         r"Both the numerator and the denominator are $0$ at $x = 3$, so factor and cancel: "
         + limchain(3, [r"\frac{x^2 - 9}{x^2 - x - 6}", r"\frac{(x - 3)(x + 3)}{(x - 3)(x + 2)}", r"\frac{x + 3}{x + 2}"], r"\frac65") + ".",
         {r"$1$": "divided the leading coefficients, which is the method for a limit at infinity",
          r"nonexistent": "stopped at the form $\\frac00$, which only says more work is needed"}, topic="1.6"),
    pick(r"$\displaystyle\lim_{x\to\infty} \frac{4x^3 - x}{2 - 5x^3}$ is", r"$-\frac45$", [r"$\frac45$", r"$0$", r"$-2$"], "C",
         r"Divide the numerator and the denominator by $x^3$: $\displaystyle\lim_{x\to\infty} \frac{4x^3 - x}{2 - 5x^3} = \lim_{x\to\infty} \frac{4 - \frac{1}{x^2}}{\frac{2}{x^3} - 5} = \frac{4 - 0}{0 - 5} = -\frac45$.",
         {r"$\frac45$": "dropped the sign of $-5x^3$", r"$-2$": "divided by the constant term $2$ instead of the leading coefficient"}, topic="1.15"),
    pick(r"Let $f(x) = \begin{cases} kx + 1, & x < 2 \\ x^2 - k, & x \ge 2. \end{cases}$ For what value of $k$ is $f$ continuous for all real numbers?",
         r"$1$", [r"$3$", r"$\frac53$", r"$-1$"], "A",
         r"Each piece is continuous, so only $x = 2$ needs checking. $\displaystyle\lim_{x\to 2^-} f(x) = 2k + 1$ and $\displaystyle\lim_{x\to 2^+} f(x) = 4 - k = f(2)$. "
         r"These must be equal: $2k + 1 = 4 - k$, so $3k = 3$, and therefore $k = 1$.",
         {r"$\frac53$": "set $2k + 1 = 4 + k$, losing the sign of $-k$"}, topic="1.13"),
    pick(r"Which of the following are the vertical asymptotes of the graph of $y = \dfrac{x - 1}{x^2 - 1}$?",
         r"$x = -1$ only", [r"$x = 1$ only", r"$x = -1$ and $x = 1$", r"There are none."], "D",
         r"$\frac{x - 1}{x^2 - 1} = \frac{x - 1}{(x - 1)(x + 1)} = \frac{1}{x + 1}$ for $x \ne 1$. "
         r"At $x = 1$, $\displaystyle\lim_{x\to 1} \frac{x - 1}{x^2 - 1} = \lim_{x\to 1} \frac{1}{x + 1} = \frac12$, so the graph has a hole there, not an asymptote. "
         r"At $x = -1$, $\displaystyle\lim_{x\to -1^+} \frac{x - 1}{x^2 - 1} = \lim_{x\to -1^+} \frac{1}{x + 1} = \infty$, so $x = -1$ is a vertical asymptote.",
         {r"$x = -1$ and $x = 1$": "took every zero of the denominator without checking for a common factor"}, topic="1.14"),
    pick(r"$\displaystyle\lim_{h\to 0} \frac{\sin\left(\frac\pi3 + h\right) - \sin\left(\frac\pi3\right)}{h}$ is",
         r"$\frac12$", [r"$\frac{\sqrt3}{2}$", r"$0$", r"$-\frac12$"], "A",
         r"This is the definition of the derivative of $\sin x$ at $x = \frac\pi3$. The derivative of $\sin x$ is $\cos x$, so the limit is $\cos\frac\pi3 = \frac12$.",
         {r"$\frac{\sqrt3}{2}$": "gave $\\sin\\frac\\pi3$, the value of the function instead of its derivative"}, topic="2.2"),
    pick(r"If $f(x) = x^2 e^x$, then $f'(1) = $", r"$3e$", [r"$2e$", r"$e$", r"$e^2$"], "C",
         r"By the product rule, $f'(x) = 2x e^x + x^2 e^x$, so $f'(1) = 2e + e = 3e$.",
         {r"$2e$": "multiplied the two derivatives, $2x \\cdot e^x$, instead of using the product rule"}, topic="2.8"),
    pick(r"If $f(x) = \dfrac{2x + 1}{x - 1}$, then $f'(2) = $", r"$-3$", [r"$3$", r"$2$", r"$-\frac13$"], "B",
         r"By the quotient rule, $f'(x) = \frac{2(x - 1) - (2x + 1)(1)}{(x - 1)^2} = \frac{-3}{(x - 1)^2}$, so $f'(2) = \frac{-3}{1} = -3$.",
         {r"$3$": "subtracted in the wrong order in the numerator", r"$2$": "divided the derivative of the top by the derivative of the bottom"}, topic="2.9"),
    pick(r"$\dfrac{d}{dx}\left[\sin^3(2x)\right] = $", r"$6\sin^2(2x)\cos(2x)$",
         [r"$3\sin^2(2x)\cos(2x)$", r"$3\sin^2(2x)$", r"$6\cos^2(2x)$"], "D",
         r"The chain rule, twice: $\frac{d}{dx}\left[(\sin 2x)^3\right] = 3(\sin 2x)^2 \cdot \cos(2x) \cdot 2 = 6\sin^2(2x)\cos(2x)$.",
         {r"$3\sin^2(2x)\cos(2x)$": "left out the factor $2$ from the inside function $2x$"}, topic="3.1"),
    pick(r"The table gives values of the differentiable functions $f$ and $g$ and their derivatives. If $h(x) = f(g(x))$, then $h'(1) = $" + TABLE9,
         r"$-10$", [r"$-4$", r"$-14$", r"$30$"], "A",
         r"By the chain rule, $h'(1) = f'(g(1)) \cdot g'(1) = f'(3) \cdot (-2) = 5(-2) = -10$.",
         {r"$-4$": "used $f'(1)$ instead of $f'(g(1)) = f'(3)$", r"$-14$": "used $f(3)$ instead of $f'(3)$"}, topic="3.1"),
    pick(r"Let $f(x) = x^3 + 2x + 1$, and let $g$ be the inverse function of $f$. What is the value of $g'(4)$?",
         r"$\frac15$", [r"$\frac{1}{50}$", r"$5$", r"$50$"], "C",
         r"$f(1) = 1 + 2 + 1 = 4$, so $g(4) = 1$. Then $g'(4) = \frac{1}{f'(g(4))} = \frac{1}{f'(1)} = \frac{1}{3 + 2} = \frac15$.",
         {r"$\frac{1}{50}$": "evaluated $f'$ at $4$ instead of at $g(4) = 1$", r"$5$": "gave $f'(1)$ without taking the reciprocal"}, topic="3.3"),
    pick(r"If $y = \arctan(3x)$, what is the value of $\dfrac{dy}{dx}$ at $x = \frac13$?", r"$\frac32$", [r"$\frac12$", r"$\frac{3}{10}$", r"$\frac\pi4$"], "B",
         r"$\frac{dy}{dx} = \frac{3}{1 + (3x)^2}$. At $x = \frac13$, $\frac{dy}{dx} = \frac{3}{1 + 1} = \frac32$.",
         {r"$\frac12$": "left out the factor $3$ from the chain rule", r"$\frac\pi4$": "gave $y$, not $\\frac{dy}{dx}$"}, topic="3.4"),
    pick(r"What is the slope of the line tangent to the curve $x^2 + xy + y^2 = 7$ at the point $(1, 2)$?", r"$-\frac45$",
         [r"$-\frac54$", r"$-1$", r"$\frac45$"], "D",
         r"Differentiate implicitly: $2x + y + x\frac{dy}{dx} + 2y\frac{dy}{dx} = 0$, so $\frac{dy}{dx} = -\frac{2x + y}{x + 2y}$. At $(1, 2)$, $\frac{dy}{dx} = -\frac{4}{5}$.",
         {r"$-1$": "differentiated $xy$ as $y$, leaving out the $x\\frac{dy}{dx}$ term of the product rule", r"$-\frac54$": "turned the fraction upside down"}, topic="3.2"),
    pick(r"If $f(x) = x e^{2x}$, then $f''(0) = $", r"$4$", [r"$2$", r"$1$", r"$0$"], "A",
         r"$f'(x) = e^{2x} + 2x e^{2x}$ and $f''(x) = 2e^{2x} + 2e^{2x} + 4x e^{2x} = 4e^{2x} + 4x e^{2x}$, so $f''(0) = 4$.",
         {r"$1$": "gave $f'(0)$", r"$2$": "differentiated only the first term of $f'$"}, topic="3.6"),
    pick(r"A particle moves along the $x$-axis so that its position at time $t \ge 0$ is $x(t) = t^3 - 6t^2 + 9t$. For which values of $t$ is the particle moving to the left?",
         r"$1 < t < 3$", [r"$t > 3$ only", r"$0 \le t < 2$", r"$0 < t < 1$ and $t > 3$"], "C",
         r"$v(t) = x'(t) = 3t^2 - 12t + 9 = 3(t - 1)(t - 3)$. The particle moves left when $v(t) < 0$, which is for $1 < t < 3$.",
         {r"$0 \le t < 2$": "used where the acceleration $6t - 12$ is negative", r"$0 < t < 1$ and $t > 3$": "gave where the particle moves to the right"}, topic="4.2"),
    pick(r"Kofi inflates a spherical balloon so that its radius increases at a rate of $2$ centimeters per second. At the instant the radius is $5$ centimeters, how fast is the volume of the balloon increasing? (The volume of a sphere with radius $r$ is $V = \frac43\pi r^3$.)",
         r"$200\pi$ cubic centimeters per second", [r"$100\pi$ cubic centimeters per second", r"$40\pi$ cubic centimeters per second", r"$\frac{500\pi}{3}$ cubic centimeters per second"], "D",
         r"$\frac{dV}{dt} = 4\pi r^2 \frac{dr}{dt} = 4\pi(5)^2(2) = 200\pi$ cubic centimeters per second.",
         {r"$100\pi$ cubic centimeters per second": "left out $\\frac{dr}{dt} = 2$", r"$\frac{500\pi}{3}$ cubic centimeters per second": "gave the volume, not its rate of change"}, topic="4.5"),
    pick(r"Using the line tangent to the graph of $f(x) = \sqrt{x}$ at $x = 9$, what is the approximation of $\sqrt{9.6}$?",
         r"$3.1$", [r"$3.2$", r"$3.3$", r"$3.6$"], "B",
         r"$f(9) = 3$ and $f'(x) = \frac{1}{2\sqrt x}$, so $f'(9) = \frac16$. The tangent line is $y = 3 + \frac16(x - 9)$, so $\sqrt{9.6} \approx 3 + \frac16(0.6) = 3.1$.",
         {r"$3.2$": "used $\\frac{1}{\\sqrt x}$ for the derivative, dropping the $\\frac12$", r"$3.6$": "used slope $1$"}, topic="4.6"),
    pick(r"$\displaystyle\lim_{x\to 0} \frac{e^{2x} - 1 - 2x}{x^2}$ is", r"$2$", [r"$1$", r"$4$", r"$0$"], "A",
         r"At $x = 0$ the fraction has the form $\frac00$, so use L'Hospital's Rule: $\displaystyle\lim_{x\to 0} \frac{e^{2x} - 1 - 2x}{x^2} = \lim_{x\to 0} \frac{2e^{2x} - 2}{2x}$. "
         r"This is again $\frac00$, so use the rule once more: $\displaystyle\lim_{x\to 0} \frac{2e^{2x} - 2}{2x} = \lim_{x\to 0} \frac{4e^{2x}}{2} = 2$.",
         {r"$4$": "forgot the $2$ in the denominator after the second step", r"$0$": "plugged in $0$ after only one application of the rule"}, topic="4.7"),
    pick(r"Let $f(x) = x^2 - 4x$. What value of $c$ satisfies the conclusion of the Mean Value Theorem for $f$ on the interval $[0, 3]$?",
         r"$\frac32$", [r"$2$", r"$1$", r"$3$"], "D",
         r"$\frac{f(3) - f(0)}{3 - 0} = \frac{-3 - 0}{3} = -1$. Set $f'(c) = 2c - 4 = -1$, so $c = \frac32$, which is in $(0, 3)$.",
         {r"$2$": "found where $f'(c) = 0$ instead of where $f'(c)$ equals the average rate of change"}, topic="5.1"),
    pick(r"What is the absolute maximum value of $f(x) = x^3 - 3x$ on the closed interval $[0, 2]$?", r"$2$", [r"$0$", r"$-2$", r"$1$"], "C",
         r"$f'(x) = 3x^2 - 3 = 0$ at $x = 1$ in the interval. Candidates: $f(0) = 0$, $f(1) = -2$, $f(2) = 2$. The absolute maximum value is $2$.",
         {r"$-2$": "gave the value at the critical point, which is the minimum", r"$1$": "gave the $x$-value of the critical point"}, topic="5.5"),
    pick(r"The derivative of a function $f$ is $f'(x) = x(x - 2)^2$. Which of the following is true?",
         r"$f$ has a relative minimum at $x = 0$ and no other relative extrema.",
         [r"$f$ has a relative maximum at $x = 0$ and a relative minimum at $x = 2$.", r"$f$ has relative minima at $x = 0$ and $x = 2$.", r"$f$ has a relative maximum at $x = 2$ and no other relative extrema."], "B",
         r"$f'(x) = 0$ at $x = 0$ and $x = 2$. Since $(x - 2)^2 \ge 0$, $f'$ has the sign of $x$: negative for $x < 0$ and positive for $x > 0$ (except at $x = 2$). "
         r"So $f'$ changes from negative to positive at $x = 0$, a relative minimum, and does not change sign at $x = 2$, so there is no extremum there.",
         {r"$f$ has relative minima at $x = 0$ and $x = 2$.": "treated every zero of $f'$ as an extremum without checking for a sign change"}, topic="5.4"),
    pick(r"On which interval is the graph of $f(x) = x^4 - 6x^2$ concave down?", r"$(-1, 1)$",
         [r"$\left(-\sqrt3, \sqrt3\right)$", r"$(-\infty, -1)$ and $(1, \infty)$", r"$\left(0, \sqrt3\right)$"], "A",
         r"$f'(x) = 4x^3 - 12x$ and $f''(x) = 12x^2 - 12 = 12(x - 1)(x + 1)$. $f''(x) < 0$ for $-1 < x < 1$, so the graph is concave down on $(-1, 1)$.",
         {r"$(-\infty, -1)$ and $(1, \infty)$": "gave where the graph is concave up", r"$\left(0, \sqrt3\right)$": "gave where $f$ is decreasing"}, topic="5.6"),
    pick(r"A function $f$ is twice differentiable with $f'(2) = 0$ and $f''(2) = -3$. Which of the following must be true?",
         r"$f$ has a relative maximum at $x = 2$.", [r"$f$ has a relative minimum at $x = 2$.", r"The graph of $f$ has a point of inflection at $x = 2$.", r"$f$ is decreasing at $x = 2$."], "D",
         r"$f'(2) = 0$ and $f''(2) < 0$, so the graph is concave down at a horizontal tangent. By the Second Derivative Test, $f$ has a relative maximum at $x = 2$.",
         {r"$f$ has a relative minimum at $x = 2$.": "reversed the Second Derivative Test"}, topic="5.7"),
    pick(r"The function $f$ is continuous on $[0, 6]$, and selected values of $f$ are shown in the table. Using the subintervals $[0, 2]$, $[2, 5]$, and $[5, 6]$, what is the right Riemann sum approximation of $\displaystyle\int_0^6 f(x)\,dx$?" + TABLE23,
         r"$18$", [r"$14$", r"$16$", r"$11$"], "C",
         r"Each subinterval's width times the value at its right end: $2 \cdot f(2) + 3 \cdot f(5) + 1 \cdot f(6) = 2(1) + 3(3) + 1(7) = 18$.",
         {r"$14$": "used left endpoints", r"$16$": "used the trapezoidal sum", r"$11$": "added the right-endpoint values without multiplying by the widths"}, topic="6.2"),
    pick(r"Let $g(x) = \displaystyle\int_0^{x^2} \sqrt{1 + t^3}\,dt$. What is $g'(2)$?", r"$4\sqrt{65}$", [r"$\sqrt{65}$", r"$2\sqrt{65}$", r"$3$"], "B",
         r"By the Fundamental Theorem of Calculus and the chain rule, $g'(x) = \sqrt{1 + (x^2)^3} \cdot 2x$. So $g'(2) = \sqrt{1 + 64} \cdot 4 = 4\sqrt{65}$.",
         {r"$\sqrt{65}$": "left out the chain-rule factor $2x$", r"$3$": "put $x$ in place of $t$ instead of $x^2$, and left out the chain-rule factor"}, topic="6.4"),
    pick(r"If $\displaystyle\int_1^5 f(x)\,dx = 8$ and $\displaystyle\int_3^5 f(x)\,dx = 3$, then $\displaystyle\int_1^3 \left(2f(x) + 1\right) dx = $",
         r"$12$", [r"$11$", r"$10$", r"$17$"], "D",
         r"$\int_1^3 f(x)\,dx = 8 - 3 = 5$. Then $\int_1^3 \left(2f(x) + 1\right) dx = 2(5) + \int_1^3 1\,dx = 10 + 2 = 12$.",
         {r"$11$": "integrated the constant $1$ as $1$ instead of as the interval length $2$", r"$10$": "left out the $\\int_1^3 1\\,dx$ term"}, topic="6.6"),
    pick(r"$\displaystyle\int_1^e \left(2x + \frac1x\right) dx = $", r"$e^2$", [r"$e^2 - 1$", r"$e^2 + 1$", r"$2e - 1$"], "A",
         r"$\int_1^e \left(2x + \frac1x\right) dx = \left[x^2 + \ln x\right]_1^e = (e^2 + 1) - (1 + 0) = e^2$.",
         {r"$e^2 - 1$": "left out the $\\ln x$ term", r"$e^2 + 1$": "forgot to subtract the value at $x = 1$"}, topic="6.7"),
    pick(r"$\displaystyle\int_0^1 x e^{x^2}\,dx = $", r"$\frac{e - 1}{2}$", [r"$e - 1$", r"$\frac{e}{2}$", r"$2(e - 1)$"], "B",
         r"Let $u = x^2$, so $du = 2x\,dx$; $u$ runs from $0$ to $1$. $\int_0^1 x e^{x^2}\,dx = \frac12\int_0^1 e^u\,du = \frac12(e - 1)$.",
         {r"$e - 1$": "left out the $\\frac12$ from $du = 2x\\,dx$", r"$\frac{e}{2}$": "forgot to subtract $e^0$"}, topic="6.9"),
    pick(r"$\displaystyle\int \frac{1}{x^2 + 4x + 5}\,dx = $", r"$\arctan(x + 2) + C$",
         [r"$\ln\left|x^2 + 4x + 5\right| + C$", r"$\frac12\arctan\left(\frac{x + 2}{2}\right) + C$", r"$-\frac{1}{x + 2} + C$"], "C",
         r"Complete the square: $x^2 + 4x + 5 = (x + 2)^2 + 1$. So $\int \frac{dx}{(x + 2)^2 + 1} = \arctan(x + 2) + C$.",
         {r"$\ln\left|x^2 + 4x + 5\right| + C$": "the numerator is not the derivative of the denominator", r"$\frac12\arctan\left(\frac{x + 2}{2}\right) + C$": "used $(x + 2)^2 + 4$"}, topic="6.10"),
    pick(r"Let $y = f(x)$ be the solution to the differential equation $\dfrac{dy}{dx} = xy$ with the initial condition $f(0) = 3$. Which of the following is $f(x)$?",
         r"$3e^{x^2/2}$", [r"$e^{x^2/2} + 2$", r"$3e^{x^2}$", r"$3 + \frac{x^2}{2}$"], "D",
         r"Separate: $\frac{dy}{y} = x\,dx$, so $\ln|y| = \frac{x^2}{2} + C$ and $y = Ke^{x^2/2}$. Since $f(0) = 3$, $K = 3$. Therefore $f(x) = 3e^{x^2/2}$.",
         {r"$e^{x^2/2} + 2$": "added the constant after solving for $y$ instead of while integrating"}, topic="7.7"),
    pick(r"What is the area of the region bounded by the graphs of $y = 4 - x^2$ and $y = x + 2$?", r"$\frac92$", [r"$\frac76$", r"$\frac{10}{3}$", r"$9$"], "A",
         r"The graphs meet where $4 - x^2 = x + 2$, so $x^2 + x - 2 = 0$ and $x = -2$ or $x = 1$. On $[-2, 1]$ the parabola is on top: "
         r"$\int_{-2}^1 \left(4 - x^2 - (x + 2)\right) dx = \left[2x - \frac{x^2}{2} - \frac{x^3}{3}\right]_{-2}^1 = \frac76 - \left(-\frac{10}{3}\right) = \frac92$.",
         {r"$\frac76$": "integrated from $0$ to $1$ only"}, topic="8.4"),
]


# ====================================================================== Section I, Part B: graphing calculator
def numpick(stem, right, wrong, solution, why=None, topic="", fmt=f3, figure=None):
    """A calculator MCQ with numeric choices listed in increasing order, as on the AP exam. right and wrong are
    numbers; why maps a wrong number to the slip behind it. The keyed letter is wherever the right value sorts to."""
    vals = sorted([right] + list(wrong))
    texts = [fmt(v) for v in vals]
    check(f"numpick distinct: {stem[:40]}", len(set(texts)) == 4, str(texts))
    letter = "ABCD"[vals.index(right)]
    why_not = {"ABCD"[vals.index(w)]: r for w, r in (why or {}).items()}
    return MCQ(stem, texts, letter, solution, why_not=why_not, calc=True, topic=topic, figure=figure)


def r3(label, v):
    """Pin a calculator answer: the printed value is v rounded to three decimals."""
    close(label, v, round(v, 3), 5e-4 + 1e-12)
    return v


H1 = 20 + 70 * sp.exp(-sp.Rational(4, 100) * t)
b1 = r3("B1", float(sp.diff(H1, t).subs(t, 10)))
b1avg = float((H1.subs(t, 10) - H1.subs(t, 0)) / 10)
R2 = 2 + sp.sin(t**2 / 4)
b2 = r3("B2", 12 + N(R2, 0, 4, t))
fp3 = lambda v: v * sp.cos(v**2)
crit3 = [sp.sqrt(k * sp.pi / 2) for k in (1, 3, 5)]
check("B3 three zeros of f' in (0, 3)", all(0 < float(c) < 3 for c in crit3) and float(sp.sqrt(7 * sp.pi / 2)) > 3)
maxes3 = sum(1 for c in crit3 if fp3(float(c) - 1e-3) > 0 > fp3(float(c) + 1e-3))
same("B3 relative maxima", maxes3, 2)
V4 = sp.log(t**2 + 1) - sp.Rational(6, 5)
turn4 = float(sp.nsolve(V4, t, 1.5))
b4 = r3("B4", abs(N(V4, 0, turn4, t)) + abs(N(V4, turn4, 3, t)))
disp4 = N(V4, 0, 3, t)
V5 = sp.exp(sp.sin(t)) - t / 2
b5 = r3("B5", float(sp.diff(V5, t).subs(t, 2)))
F6 = sp.sqrt(1 + x**3)
b6 = r3("B6", N(F6, 0, 2) / 2)
TOP7, BOT7 = 2 - x**2, sp.exp(x)
a7 = float(sp.nsolve(TOP7 - BOT7, x, -1.3))
c7 = float(sp.nsolve(TOP7 - BOT7, x, 0.5))
b7 = r3("B7", N(TOP7 - BOT7, a7, c7))
b8 = r3("B8", N((TOP7 - BOT7)**2, a7, c7))
b8wash = float(sp.pi) * N(TOP7**2 - BOT7**2, a7, c7)
b9 = r3("B9", float(sp.log((sp.E**2 - 1) / 2)))
same("B9 is the MVT point", sp.exp(sp.log((sp.E**2 - 1) / 2)), (sp.exp(2) - 1) / 2)
b10int = N(sp.log(1 + t**2), 1, 3, t)
b10 = r3("B10", 5 + b10int)
b11 = r3("B11", float(50 * sp.Rational(84, 100)**sp.Rational(5, 2)))
same("B11 model", [50 * sp.Rational(84, 100)**sp.Rational(4, 4)], [42])
R12 = 60 + 45 * sp.sin(t**2 / 12)
b12 = N(R12, 0, 8, t)
check("B12 rounds to 561", round(b12) == 561, str(b12))
f13 = lambda v: float(sp.exp(sp.Float(v)**2))
b13 = r3("B13", 0.25 * (f13(0) + 2 * f13(0.5) + 2 * f13(1) + 2 * f13(1.5) + f13(2)))
b13left = 0.5 * (f13(0) + f13(0.5) + f13(1) + f13(1.5))
b13right = 0.5 * (f13(0.5) + f13(1) + f13(1.5) + f13(2))
F14 = sp.exp(x / 2) + sp.cos(x)
b14 = r3("B14", float(F14.subs(x, 1) + sp.Rational(1, 5) * sp.diff(F14, x).subs(x, 1)))
G15 = sp.sin(x) - (x**3 - 2 * x)
c15 = float(sp.nsolve(x**3 - 2 * x - sp.sin(x), x, 1.8))
check("B15 odd functions: the regions match", sp.simplify(G15.subs(x, -x) + G15) == 0)
b15 = r3("B15", 2 * N(G15, 0, c15))

PART_B = [
    numpick(r"Priya pours a cup of coffee. Its temperature, in degrees Celsius, is modeled by $H(t) = 20 + 70e^{-0.04t}$, where $t$ is the time in minutes since she poured it. "
            r"What is the rate of change of the temperature of the coffee at time $t = 10$ minutes, in degrees Celsius per minute?",
            b1, [b1avg, -b1, -2.8],
            rf"$H'(t) = 70(-0.04)e^{{-0.04t}} = -2.8e^{{-0.04t}}$, so $H'(10) = -2.8e^{{-0.4}} \approx {b1:.3f}$ degrees Celsius per minute.",
            {b1avg: "the average rate of change over the first $10$ minutes", -2.8: "used $H'(0)$"}, topic="4.3"),
    numpick(r"Rainwater flows into Tariq's rain barrel at a rate of $r(t) = 2 + \sin\left(\frac{t^2}{4}\right)$ liters per hour, where $t$ is in hours. "
            r"At time $t = 0$ the barrel holds $12$ liters. How many liters of water are in the barrel at time $t = 4$?",
            b2, [b2 - 12, 12 + 4 * float(R2.subs(t, 4)), 12 + float(R2.subs(t, 4))],
            rf"The amount at $t = 4$ is the starting amount plus the total that flows in: $12 + \int_0^4 r(t)\,dt \approx 12 + {b2 - 12:.3f} = {b2:.3f}$ liters.",
            {b2 - 12: "left out the $12$ liters already in the barrel", 12 + 4 * float(R2.subs(t, 4)): "multiplied the rate at $t = 4$ by $4$ hours instead of integrating"}, topic="8.3"),
    numpick(r"The derivative of a function $f$ is $f'(x) = x\cos\left(x^2\right)$. How many relative maxima does $f$ have on the interval $0 < x < 3$?",
            2, [1, 3, 4],
            r"$f'(x) = 0$ in $(0, 3)$ where $\cos(x^2) = 0$, so at $x = \sqrt{\pi/2} \approx 1.253$, $\sqrt{3\pi/2} \approx 2.171$, and $\sqrt{5\pi/2} \approx 2.802$. "
            r"Graphing $f'$ shows it changes from positive to negative at $1.253$ and $2.802$, and from negative to positive at $2.171$. "
            r"So $f$ has relative maxima at $x \approx 1.253$ and $x \approx 2.802$: two of them.",
            {3: "counted every zero of $f'$, including the relative minimum"}, topic="5.4", fmt=lambda v: f"${v}$"),
    numpick(r"A particle moves along a line with velocity $v(t) = \ln\left(t^2 + 1\right) - 1.2$ for $0 \le t \le 3$. What is the total distance traveled by the particle over this time interval?",
            b4, [disp4, abs(disp4), turn4],
            rf"Total distance traveled is $\int_0^3 |v(t)|\,dt \approx {b4:.3f}$. (The velocity changes sign at $t \approx {turn4:.3f}$, so the displacement $\int_0^3 v(t)\,dt \approx {disp4:.3f}$ is not the distance.)",
            {disp4: "gave the displacement", abs(disp4): "took the absolute value of the displacement instead of integrating the speed", turn4: "gave the time at which the particle changes direction"}, topic="8.2"),
    numpick(r"A particle moves along the $x$-axis with velocity $v(t) = e^{\sin t} - \frac{t}{2}$. What is the acceleration of the particle at time $t = 2$?",
            b5, [-b5, float(V5.subs(t, 2)), float((V5.subs(t, 2) - V5.subs(t, 0)) / 2)],
            rf"$a(t) = v'(t) = \cos t \cdot e^{{\sin t}} - \frac12$, so $a(2) = \cos 2 \cdot e^{{\sin 2}} - \frac12 \approx {b5:.3f}$.",
            {float(V5.subs(t, 2)): "gave the velocity $v(2)$", float((V5.subs(t, 2) - V5.subs(t, 0)) / 2): "gave the average acceleration on $[0, 2]$"}, topic="4.2"),
    numpick(r"What is the average value of $f(x) = \sqrt{1 + x^3}$ on the interval $[0, 2]$?",
            b6, [2 * b6, 1.0, float(sp.sqrt(2))],
            rf"$\frac{{1}}{{2 - 0}}\int_0^2 \sqrt{{1 + x^3}}\,dx \approx \frac{{{2 * b6:.4f}}}{{2}} \approx {b6:.3f}$.",
            {2 * b6: "forgot to divide by the length of the interval", 1.0: "gave the average rate of change, $\\frac{f(2) - f(0)}{2}$", float(sp.sqrt(2)): "gave $f(1)$, the value at the midpoint"}, topic="8.1"),
    numpick(r"Let $R$ be the region bounded by the graphs of $y = 2 - x^2$ and $y = e^x$. What is the area of $R$?",
            b7, [b7 / 2, b8, c7 - a7],
            rf"The graphs meet at $x = a \approx {a7:.4f}$ and $x = b \approx {c7:.4f}$ (store these in the calculator). Between them $2 - x^2$ is on top, so the area is $\int_a^b \left(2 - x^2 - e^x\right) dx \approx {b7:.3f}$.",
            {c7 - a7: "gave the width of the region, $b - a$", b8: "squared the integrand"}, topic="8.4"),
    numpick(r"Let $R$ be the region bounded by the graphs of $y = 2 - x^2$ and $y = e^x$. $R$ is the base of a solid whose cross sections perpendicular to the $x$-axis are squares. What is the volume of the solid?",
            b8, [b7, b8wash, b8 / 2],
            rf"With $a \approx {a7:.4f}$ and $b \approx {c7:.4f}$ where the graphs meet, each square has side $2 - x^2 - e^x$, so the volume is $\int_a^b \left(2 - x^2 - e^x\right)^2 dx \approx {b8:.3f}$.",
            {b7: "gave the area of the base", b8wash: "found the volume of revolution about the $x$-axis"}, topic="8.7"),
    numpick(r"Let $f(x) = e^x$. What value of $c$ in the interval $(0, 2)$ satisfies the conclusion of the Mean Value Theorem for $f$ on $[0, 2]$?",
            b9, [1.0, (math_e2 := float((sp.E**2 - 1) / 2)), math_e2 / 2],
            rf"The average rate of change is $\frac{{e^2 - 1}}{{2}} \approx {math_e2:.4f}$. Solve $f'(c) = e^c = \frac{{e^2 - 1}}{{2}}$: $c = \ln\left(\frac{{e^2 - 1}}{{2}}\right) \approx {b9:.3f}$.",
            {1.0: "used the midpoint of the interval", math_e2: "gave the average rate of change instead of $c$"}, topic="5.1"),
    numpick(r"Let $g(x) = 5 + \displaystyle\int_1^x \ln\left(1 + t^2\right) dt$. What is $g(3)$?",
            b10, [b10int, 5 + float(sp.log(10)), 5 - b10int],
            rf"$g(3) = 5 + \int_1^3 \ln(1 + t^2)\,dt \approx 5 + {b10int:.3f} = {b10:.3f}$.",
            {b10int: "left out the $5$", 5 + float(sp.log(10)): "put $3$ into the integrand instead of integrating"}, topic="6.4"),
    numpick(r"In Mei's lab, a sample of a radioactive substance decays at a rate proportional to its mass. The sample has a mass of $50$ grams at time $t = 0$ and $42$ grams at $t = 4$ days. What is the mass of the sample at $t = 10$ days?",
            b11, [30.0, float(50 * sp.Rational(84, 100)**10), float(50 * sp.exp(-sp.Rational(4, 10)))],
            rf"$\frac{{dm}}{{dt}} = km$, so $m(t) = 50e^{{kt}}$. From $m(4) = 42$, $e^{{4k}} = 0.84$, so $k = \frac{{\ln 0.84}}{{4}}$. Then $m(10) = 50e^{{10k}} = 50(0.84)^{{10/4}} \approx {b11:.3f}$ grams.",
            {30.0: "assumed the mass drops by the same amount each day", float(50 * sp.Rational(84, 100)**10): "treated $0.84$ as the daily factor instead of the factor for $4$ days"}, topic="7.8"),
    numpick(r"Lucía runs a food truck. During an $8$-hour shift, she takes in money at a rate of $r(t) = 60 + 45\sin\left(\frac{t^2}{12}\right)$ dollars per hour, where $t$ is the number of hours since the shift began. To the nearest dollar, how much money does she take in during the shift?",
            561, [480, round(b12 / 8), round(8 * float(R12.subs(t, 8)))],
            rf"The total is $\int_0^8 r(t)\,dt \approx {b12:.3f}$, which is \${round(b12)} to the nearest dollar.",
            {480: "used only the constant part of the rate, $60 \\cdot 8$", round(b12 / 8): "gave the average rate in dollars per hour", round(8 * float(R12.subs(t, 8))): "multiplied the rate at the end of the shift by $8$ hours"},
            topic="8.3", fmt=lambda v: rf"\${v}"),
    numpick(r"What is the trapezoidal sum approximation of $\displaystyle\int_0^2 e^{x^2}\,dx$ using four subintervals of equal length?",
            b13, [b13left, b13right, N(sp.exp(x**2), 0, 2)],
            r"Each subinterval has width $0.5$: $\frac{0.5}{2}\left(f(0) + 2f(0.5) + 2f(1) + 2f(1.5) + f(2)\right) \approx " + f"{b13:.3f}" + r"$.",
            {b13left: "the left Riemann sum", b13right: "the right Riemann sum", N(sp.exp(x**2), 0, 2): "the value of the integral, not the trapezoidal sum"}, topic="6.3"),
    numpick(r"Let $f(x) = e^{x/2} + \cos x$. The line tangent to the graph of $f$ at $x = 1$ is used to approximate $f(1.2)$. What is the approximation?",
            b14, [float(F14.subs(x, sp.Rational(6, 5))), float(F14.subs(x, 1) + sp.diff(F14, x).subs(x, 1)), float(F14.subs(x, 1))],
            rf"$f(1) \approx {float(F14.subs(x, 1)):.4f}$ and $f'(x) = \frac12 e^{{x/2}} - \sin x$, so $f'(1) \approx {float(sp.diff(F14, x).subs(x, 1)):.4f}$. "
            rf"Then $f(1.2) \approx f(1) + f'(1)(0.2) \approx {b14:.3f}$.",
            {float(F14.subs(x, sp.Rational(6, 5))): "gave $f(1.2)$ itself, not the tangent-line approximation", float(F14.subs(x, 1) + sp.diff(F14, x).subs(x, 1)): "used a step of $1$ instead of $0.2$"}, topic="4.6"),
    numpick(r"What is the total area of the regions enclosed by the graphs of $y = \sin x$ and $y = x^3 - 2x$?",
            b15, [b15 / 2, c15, 0.0],
            rf"The graphs meet at $x = 0$ and $x = \pm c$, where $c \approx {c15:.4f}$. On $(0, c)$, $\sin x$ is on top; the region on $(-c, 0)$ is the same size, since both functions are odd. "
            rf"Total area $= \int_{{-c}}^{{c}} \left|\sin x - (x^3 - 2x)\right| dx \approx {b15:.3f}$.",
            {0.0: "integrated without absolute value, so the two regions canceled", b15 / 2: "found only one of the two regions"}, topic="8.6"),
]


# ====================================================================== Section II, Part A: calculator
# ---- Question 1: rates in and out
E1 = 24 + 10 * sp.sin(t**2 / 20)
U1 = 2 * t + 14
D1 = E1 - U1
q1a = r3("Q1a", N(E1, 0, 10, t))
q1b = r3("Q1b", float(D1.subs(t, 7)))
grid1 = [k / 200 for k in range(2001)]
signs1 = [float(D1.subs(t, v)) for v in grid1]
same("Q1 one sign change of A' on [0, 10]", sum(1 for p, q in zip(signs1, signs1[1:]) if p * q < 0), 1)
q1c = r3("Q1c", float(sp.nsolve(D1, t, 7.3)))
check("Q1c + to -", float(D1.subs(t, q1c - 0.01)) > 0 > float(D1.subs(t, q1c + 0.01)))
q1d = r3("Q1d", 200 + N(D1, 0, 10, t))
q1max = 200 + N(D1, 0, q1c, t)
check("Q1c beats the endpoints", q1max > 200 and q1max > q1d)

FRQ1 = FRQ("Irrigation tank", (
    r"Rowan runs the irrigation tank at a community garden. On one day, water is pumped into the tank at a rate modeled by "
    r"$E(t) = 24 + 10\sin\left(\frac{t^2}{20}\right)$ gallons per hour, and the garden's sprinklers draw water out of the tank at a rate modeled by "
    r"$U(t) = 2t + 14$ gallons per hour, where $t$ is measured in hours and $0 \le t \le 10$. At time $t = 0$, the tank holds $200$ gallons of water."), [
    Part("a", r"How many gallons of water are pumped into the tank during the time interval $0 \le t \le 10$?",
         num(round(q1a, 3), tol=0.0015), rf"$\int_0^{{10}} E(t)\,dt \approx {q1a:.3f}$ gallons.",
         [(1, r"Writes the integral $\int_0^{10} E(t)\,dt$."), (1, rf"Gives the answer, ${q1a:.3f}$ gallons (any value that rounds correctly to three decimal places).")],
         work="2.4cm", topic="8.3"),
    Part("b", r"Is the amount of water in the tank increasing or decreasing at time $t = 7$? Give a reason for your answer.",
         selfcheck(r"\text{increasing}"),
         rf"Let $A(t)$ be the amount of water in the tank. $A'(7) = E(7) - U(7) \approx {q1b:.3f}$ gallons per hour. Since $A'(7) > 0$, the amount of water is increasing at $t = 7$.",
         [(1, r"Considers $E(7) - U(7)$."), (1, r"Says the amount is increasing because $E(7) - U(7) > 0$.")], work="2cm", topic="8.3"),
    Part("c", r"At what time $t$, for $0 \le t \le 10$, is the amount of water in the tank greatest? Justify your answer.",
         num(round(q1c, 3), tol=0.0015, display=rf"t \approx {q1c:.3f}"),
         rf"$A'(t) = E(t) - U(t) = 0$ when $t = c \approx {q1c:.3f}$. $A'(t) > 0$ for $0 < t < c$ and $A'(t) < 0$ for $c < t < 10$, "
         rf"so $A$ increases and then decreases, and $c$ is the only critical point. Therefore the amount of water is greatest at $t \approx {q1c:.3f}$ hours. "
         rf"(The candidates test also works: $A(0) = 200$, $A(c) \approx {q1max:.3f}$, and $A(10) \approx {q1d:.3f}$.)",
         [(1, r"Sets $E(t) - U(t) = 0$."), (1, rf"Finds $t \approx {q1c:.3f}$."),
          (1, r"Justifies a maximum: $A'$ changes from positive to negative there and it is the only critical point, or compares $A$ at the critical point and both endpoints.")],
         work="3cm", topic="5.5"),
    Part("d", r"How many gallons of water are in the tank at time $t = 10$?",
         num(round(q1d, 3), tol=0.0015), rf"$A(10) = 200 + \int_0^{{10}} \left(E(t) - U(t)\right) dt \approx {q1d:.3f}$ gallons.",
         [(1, r"Writes $200 + \int_0^{10} \left(E(t) - U(t)\right) dt$."), (1, rf"Gives the answer, ${q1d:.3f}$ gallons.")], work="2.4cm", topic="8.3"),
], calc=True, frq_type="Rates in and out")

# ---- Question 2: area and volume
F2, G2 = 6 / (1 + x**2), x
a2 = float(sp.nsolve(F2 - G2, x, 1.6))
same("Q2 meet where x^3 + x = 6", sp.simplify((F2 - G2) * (1 + x**2)), 6 - x - x**3)
q2a = r3("Q2a", N(F2 - G2, 0, a2))
q2b = r3("Q2b", float(sp.pi) * N((F2 + 1)**2 - (G2 + 1)**2, 0, a2))
q2c = r3("Q2c", N((F2 - G2)**2, 0, a2))
FIG2 = region("exam_ab1_q2", [("6/(1+x^2)", 0, 3.2), ("x", 0, 3.2)], (-0.3, 3.3), (-0.3, 6.6),
              [(lambda v: 6 / (1 + v * v), lambda v: v, 0, a2)], labels=[(0.45, 2.6, "center", "$R$")],
              caption=r"The region $R$, bounded by $y = \frac{6}{1 + x^2}$, $y = x$, and the $y$-axis.", w="6cm", h="6cm", ystep=1)
FRQ2 = FRQ("Region between two curves", (
    r"Let $R$ be the region in the first quadrant bounded by the graph of $y = \dfrac{6}{1 + x^2}$, the line $y = x$, and the $y$-axis, as shown in the figure."), [
    Part("a", r"Find the area of $R$.", num(round(q2a, 3), tol=0.0015),
         rf"The graphs meet where $\frac{{6}}{{1 + x^2}} = x$, at $x = a \approx {a2:.4f}$. Area $= \int_0^a \left(\frac{{6}}{{1 + x^2}} - x\right) dx \approx {q2a:.3f}$.",
         [(1, r"Writes an integral with the correct integrand and limits $0$ and $a$."), (1, rf"Gives the answer, ${q2a:.3f}$.")], work="2.6cm", topic="8.4"),
    Part("b", r"Find the volume of the solid generated when $R$ is revolved about the horizontal line $y = -1$.", num(round(q2b, 3), tol=0.0015),
         rf"Outer radius $\frac{{6}}{{1 + x^2}} + 1$, inner radius $x + 1$. Volume $= \pi\int_0^a \left(\left(\frac{{6}}{{1 + x^2}} + 1\right)^2 - (x + 1)^2\right) dx \approx {q2b:.3f}$.",
         [(1, r"Uses the constant $\pi$ and the limits $0$ and $a$."), (1, r"Writes the integrand $\left(\frac{6}{1 + x^2} + 1\right)^2 - (x + 1)^2$."),
          (1, rf"Gives the answer, ${q2b:.3f}$.")], work="3cm", topic="8.12"),
    Part("c", r"$R$ is the base of a solid. For this solid, each cross section perpendicular to the $x$-axis is a square. Find the volume of the solid.", num(round(q2c, 3), tol=0.0015),
         rf"Each square has side $\frac{{6}}{{1 + x^2}} - x$. Volume $= \int_0^a \left(\frac{{6}}{{1 + x^2}} - x\right)^2 dx \approx {q2c:.3f}$.",
         [(1, r"Writes the integral of the square of the side length."), (1, rf"Gives the answer, ${q2c:.3f}$.")], work="2.6cm", topic="8.7"),
    Part("d", r"The vertical line $x = k$ divides $R$ into two regions of equal area. Write, but do not solve, an equation involving one or more integrals whose solution gives the value of $k$.",
         selfcheck(r"\int_0^k \left(\tfrac{6}{1 + x^2} - x\right) dx = \tfrac12\int_0^a \left(\tfrac{6}{1 + x^2} - x\right) dx"),
         r"The area to the left of $x = k$ must be half of the area of $R$: $\int_0^k \left(\frac{6}{1 + x^2} - x\right) dx = \frac12\int_0^a \left(\frac{6}{1 + x^2} - x\right) dx$. "
         rf"(Equally, $\int_0^k \left(\frac{{6}}{{1 + x^2}} - x\right) dx = \int_k^a \left(\frac{{6}}{{1 + x^2}} - x\right) dx$, or $= \frac{{{q2a:.3f}}}{{2}}$.)",
         [(1, r"Writes an integral for the area of one of the two pieces, from $0$ to $k$ or from $k$ to $a$."), (1, r"Writes a correct equation.")], work="2.2cm", topic="8.4"),
], calc=True, frq_type="Area and volume", figure=FIG2)


# ====================================================================== Section II, Part B: no calculator
# ---- Question 3: a table of velocities, with the Mean Value Theorem
T3, V3 = [0, 3, 8, 10, 15], [120, 150, 190, 170, 140]
q3a = sp.Rational(V3[3] - V3[2], T3[3] - T3[2])
q3b = sum((b - a) * v for a, b, v in zip(T3, T3[1:], V3[1:]))
q3c = sp.Rational(V3[2] - V3[1], T3[2] - T3[1])
W3 = 3 * t**2 - 24 * t + 36
same("Q3", [q3a, q3b, q3c, sp.factor(W3)], [-10, 2440, 8, 3 * (t - 2) * (t - 6)])
P3 = sp.integrate(W3, t)
q3d = sum(abs(P3.subs(t, b) - P3.subs(t, a)) for a, b in [(0, 2), (2, 6), (6, 8)])
same("Q3d", [q3d, [P3.subs(t, k) for k in (0, 2, 6, 8)]], [96, [0, 32, 0, 32]])
TABLE3 = (r"\par\smallskip\centerline{\begin{tabular}{c|ccccc} $t$ (minutes) & " + " & ".join(f"${v}$" for v in T3)
          + r" \\ \hline $v(t)$ (meters per minute) & " + " & ".join(f"${v}$" for v in V3) + r"\end{tabular}}")
FRQ3 = FRQ("Two runners", (
    r"Amara runs along a straight path. Her velocity is given by a differentiable function $v$, where $v(t)$ is measured in meters per minute and $t$ is measured in minutes. "
    r"Selected values of $v(t)$ for $0 \le t \le 15$ are shown in the table." + TABLE3), [
    Part("a", r"Use the data in the table to estimate the value of $v'(9)$. Show the computations that lead to your answer.",
         num(-10, display=r"-10\ \text{meters per minute per minute}"),
         r"$v'(9) \approx \frac{v(10) - v(8)}{10 - 8} = \frac{170 - 190}{2} = -10$ meters per minute per minute.",
         [(1, r"Gives $\frac{170 - 190}{10 - 8} = -10$.")], work="2cm", topic="2.3"),
    Part("b", r"Using correct units, explain the meaning of $\displaystyle\int_0^{15} v(t)\,dt$ in the context of the problem. Approximate the value of $\displaystyle\int_0^{15} v(t)\,dt$ using a right Riemann sum with the four subintervals indicated in the table.",
         num(2440, display=r"2440\ \text{meters}"),
         r"$\int_0^{15} v(t)\,dt$ is the total distance, in meters, that Amara runs from $t = 0$ to $t = 15$ minutes (her velocity is positive, so it is also how far she ends up from where she started). "
         r"Right Riemann sum: $3(150) + 5(190) + 2(170) + 5(140) = 450 + 950 + 340 + 700 = 2440$ meters.",
         [(1, r"Explains the meaning: the distance Amara runs, in meters, from $t = 0$ to $t = 15$."), (1, r"Sets up the right Riemann sum with the widths $3, 5, 2, 5$."),
          (1, r"Gives the approximation, $2440$ meters.")], work="3cm", topic="6.2"),
    Part("c", r"Must there be a time $t$, for $3 < t < 8$, at which $v'(t) = 8$? Justify your answer.",
         selfcheck(r"\text{Yes, by the Mean Value Theorem}"),
         r"$v$ is differentiable, so it is continuous on $[3, 8]$ and differentiable on $(3, 8)$. $\frac{v(8) - v(3)}{8 - 3} = \frac{190 - 150}{5} = 8$. "
         r"Therefore, by the Mean Value Theorem, there is a time $t$ with $3 < t < 8$ at which $v'(t) = 8$.",
         [(1, r"Computes $\frac{v(8) - v(3)}{8 - 3} = 8$."), (1, r"Answers yes, citing the Mean Value Theorem, with the reason it applies: $v$ is differentiable, and so continuous.")], work="2.4cm", topic="5.1"),
    Part("d", r"Diego skates back and forth along the same path. His velocity, in meters per minute, is $w(t) = 3t^2 - 24t + 36$ for $0 \le t \le 8$. Find the total distance Diego travels during the time interval $0 \le t \le 8$.",
         num(96, display=r"96\ \text{meters}"),
         r"$w(t) = 3(t - 2)(t - 6)$ changes sign at $t = 2$ and $t = 6$. An antiderivative is $W(t) = t^3 - 12t^2 + 36t$, with $W(0) = 0$, $W(2) = 32$, $W(6) = 0$, and $W(8) = 32$. "
         r"Total distance $= \int_0^8 |w(t)|\,dt = |32 - 0| + |0 - 32| + |32 - 0| = 96$ meters.",
         [(1, r"Writes $\int_0^8 |w(t)|\,dt$, or splits the interval at $t = 2$ and $t = 6$."), (1, r"Finds an antiderivative of $w$."), (1, r"Gives the answer, $96$ meters.")],
         work="3.2cm", topic="8.2"),
], frq_type="Table, Riemann sum, Mean Value Theorem")

# ---- Question 4: the graph of f' and accumulation
u4 = sp.symbols("u", real=True)
semi4 = sp.integrate(-sp.sqrt(4 - u4**2), (u4, -2, 2))          # the semicircle piece, x = u - 2 on [-4, 0]
q4 = {-4: 5 - semi4, 4: 5 + I(x, 0, 2) + I(4 - x, 2, 4), 5: 5 + I(x, 0, 2) + I(4 - x, 2, 5)}
same("Q4 f(-4), f(4), f(5)", [q4[-4], q4[4], q4[5]], [5 + 2 * sp.pi, 9, sp.Rational(17, 2)])
check("Q4 absolute max at x = -4", float(q4[-4]) > max(5, float(q4[4]), float(q4[5])))
FIG4 = graph("exam_ab1_q4", [("-sqrt(max(0,4-(x+2)^2))", -4, 0), ("x", 0, 2), ("4-x", 2, 5)], (-4.5, 5.5), (-2.5, 2.5),
             closed=[(-4, 0), (5, -1)], caption=r"The graph of $f'$, the derivative of $f$.", w="8.6cm", h="5cm", ylabel="y", samples=200)
FRQ4 = FRQ("The graph of a derivative", (
    r"Let $f$ be a function defined on the closed interval $[-4, 5]$ with $f(0) = 5$. The graph of $f'$, the derivative of $f$, consists of a semicircle and two line segments, as shown in the figure."), [
    Part("a", r"Find $f(4)$ and $f(-4)$.", selfcheck(r"f(4) = 9,\ f(-4) = 5 + 2\pi"),
         r"$f(4) = f(0) + \int_0^4 f'(x)\,dx = 5 + 4 = 9$, since the triangle from $0$ to $4$ has area $\frac12 \cdot 4 \cdot 2 = 4$. "
         r"$f(-4) = f(0) - \int_{-4}^0 f'(x)\,dx = 5 - (-2\pi) = 5 + 2\pi$, since the semicircle below the axis has area $\frac12\pi(2)^2 = 2\pi$.",
         [(1, r"$f(4) = 9$."), (1, r"$f(-4) = 5 + 2\pi$.")], work="2.6cm", topic="6.7"),
    Part("b", r"Find the $x$-coordinate of each critical point of $f$ in the open interval $-4 < x < 5$. Classify each critical point as the location of a relative minimum, a relative maximum, or neither. Justify your answers.",
         selfcheck(r"x = 0 \text{ (relative minimum)},\ x = 4 \text{ (relative maximum)}"),
         r"$f'(x) = 0$ at $x = 0$ and $x = 4$. At $x = 0$, $f'$ changes from negative to positive, so $f$ has a relative minimum there. "
         r"At $x = 4$, $f'$ changes from positive to negative, so $f$ has a relative maximum there.",
         [(1, r"Relative minimum at $x = 0$, because $f'$ changes from negative to positive."), (1, r"Relative maximum at $x = 4$, because $f'$ changes from positive to negative.")],
         work="2.6cm", topic="5.4"),
    Part("c", r"Find the $x$-coordinate of each point of inflection of the graph of $f$ for $-4 < x < 5$. Give a reason for your answer.",
         selfcheck(r"x = -2 \text{ and } x = 2"),
         r"$f'$ changes from decreasing to increasing at $x = -2$ and from increasing to decreasing at $x = 2$. So $f''$ changes sign at both, and the graph of $f$ has points of inflection at $x = -2$ and $x = 2$.",
         [(1, r"Identifies $x = -2$ and $x = 2$."), (1, r"Reason: $f'$ changes from decreasing to increasing, or from increasing to decreasing, at each.")], work="2.2cm", topic="5.9"),
    Part("d", r"Find the absolute maximum value of $f$ on the closed interval $[-4, 5]$. Justify your answer.",
         selfcheck(r"5 + 2\pi"),
         r"The candidates are the endpoints and the critical points: $f(-4) = 5 + 2\pi$, $f(0) = 5$, $f(4) = 9$, and $f(5) = 9 - \frac12 = \frac{17}{2}$. "
         r"Since $\pi > 3$, $5 + 2\pi > 11 > 9$. Therefore the absolute maximum value of $f$ is $5 + 2\pi$, at $x = -4$.",
         [(1, r"Considers the endpoints and the critical points."), (1, r"Finds $f(5) = \frac{17}{2}$ and uses the values from part (a)."), (1, r"Gives the answer, $5 + 2\pi$, with the comparison.")],
         work="2.8cm", topic="5.5"),
], frq_type="Graph of f', accumulation", figure=FIG4)

# ---- Question 5: differential equation with a slope field
dy5 = lambda X, Y: X**2 * (Y - 2)
sol5 = 2 + sp.exp((x**3 - 1) / 3)
sketch5 = 2 - sp.exp(x**3 / 3)
same("Q5 solution", [sp.diff(sol5, x) - dy5(x, sol5), sol5.subs(x, 1), sp.diff(sketch5, x) - dy5(x, sketch5), sketch5.subs(x, 0)], [0, 3, 0, 1])
d2_5 = sp.diff(dy5(x, yx), x).subs(sp.diff(yx, x), dy5(x, yx))
same("Q5 second derivative at (1, 3)", d2_5.subs(yx, 3).subs(x, 1), 3)
FIG5 = slope_field("exam_ab1_q5", lambda X, Y: X * X * (Y - 2), [-2, -1, 0, 1, 2], [-1, 0, 1, 2, 3, 4], (-2.6, 2.6), (-1.6, 4.6),
                   caption=r"The slope field for $\frac{dy}{dx} = x^2(y - 2)$.", w="6cm", h="7cm", length=0.36)
FRQ5 = FRQ("A differential equation", (
    r"Consider the differential equation $\dfrac{dy}{dx} = x^2(y - 2)$. A slope field for the differential equation is shown."), [
    Part("a", r"On the slope field, sketch the solution curve that passes through the point $(0, 1)$. (Copy the slope field onto your paper, or use the printed exam.)",
         selfcheck(r"\text{a curve through } (0, 1) \text{ that stays below } y = 2"),
         r"The curve passes through $(0, 1)$ with a horizontal tangent there, follows the slopes, decreases from left to right, stays below the line $y = 2$, and approaches $y = 2$ as $x$ decreases.",
         [(1, r"A curve through $(0, 1)$ that follows the slope field and stays below $y = 2$.")], work="1cm", topic="7.4"),
    Part("b", r"Let $y = f(x)$ be the particular solution to the differential equation with the initial condition $f(1) = 3$. Write an equation for the line tangent to the graph of $f$ at $x = 1$, and use it to approximate $f(1.2)$.",
         num(sp.Rational(16, 5), display=r"f(1.2) \approx 3.2"),
         r"At $(1, 3)$, $\frac{dy}{dx} = 1^2(3 - 2) = 1$. The tangent line is $y = 3 + (x - 1)$, so $f(1.2) \approx 3 + 0.2 = 3.2$.",
         [(1, r"Tangent line $y = 3 + 1(x - 1)$."), (1, r"Approximation $f(1.2) \approx 3.2$.")], work="2.4cm", topic="4.6"),
    Part("c", r"Find $\dfrac{d^2y}{dx^2}$ in terms of $x$ and $y$. Is the approximation in part (b) an overestimate or an underestimate of $f(1.2)$? Give a reason for your answer.",
         selfcheck(r"\text{underestimate}"),
         r"$\frac{d^2y}{dx^2} = 2x(y - 2) + x^2\frac{dy}{dx} = 2x(y - 2) + x^4(y - 2)$. At $(1, 3)$, $\frac{d^2y}{dx^2} = 2 + 1 = 3 > 0$, "
         r"so the graph of $f$ is concave up near $x = 1$ and lies above its tangent line. Therefore the approximation is an underestimate.",
         [(1, r"Finds $\frac{d^2y}{dx^2} = 2x(y - 2) + x^4(y - 2)$ and concludes underestimate because $\frac{d^2y}{dx^2} > 0$ at $(1, 3)$.")], work="2.6cm", topic="3.6"),
    Part("d", r"Find $y = f(x)$, the particular solution to the differential equation with the initial condition $f(1) = 3$.",
         expr("2 + exp((x**3 - 1)/3)", display=r"y = 2 + e^{(x^3 - 1)/3}"),
         r"Separate the variables: $\frac{dy}{y - 2} = x^2\,dx$. Integrate: $\ln|y - 2| = \frac{x^3}{3} + C$. "
         r"With $x = 1$, $y = 3$: $\ln 1 = \frac13 + C$, so $C = -\frac13$. Then $|y - 2| = e^{(x^3 - 1)/3}$, and since $y = 3 > 2$ at the initial point, $y - 2 > 0$. "
         r"Therefore $y = 2 + e^{(x^3 - 1)/3}$.",
         [(1, r"Separates the variables."), (1, r"Antiderivatives: $\ln|y - 2|$ and $\frac{x^3}{3}$."), (1, r"Includes a constant of integration."),
          (1, r"Uses the initial condition $f(1) = 3$."), (1, r"Solves for $y$: $y = 2 + e^{(x^3 - 1)/3}$.")], work="3.6cm", topic="7.7"),
], frq_type="Differential equation, slope field", figure=FIG5)

# ---- Question 6: implicit differentiation
C6 = x**2 - x * yx + yx**2 - 7
dydx6 = sp.solve(sp.diff(C6, x), sp.diff(yx, x))[0]
same("Q6a", sp.simplify(dydx6 - (2 * x - yx) / (x - 2 * yx)), 0)
same("Q6 points on the curve", [(x**2 - x * y + y**2).subs({x: a, y: b}) for a, b in [(2, 3), (3, 1)]], [7, 7])
same("Q6b slope at (2, 3)", dydx6.subs(yx, 3).subs(x, 2), -sp.Rational(1, 4))
d2_6 = sp.diff(dydx6, x).subs(sp.diff(yx, x), dydx6)
same("Q6d", sp.simplify(d2_6.subs(yx, 1).subs(x, 3)), 42)
hx6 = sp.solve(sp.Eq(3 * x**2, 7), x)
same("Q6c", sorted(hx6, key=float), [-sp.sqrt(21) / 3, sp.sqrt(21) / 3])
check("Q6c not vertical there", all((x - 2 * y).subs({x: v, y: 2 * v}) != 0 for v in hx6))
same("Q6c on the curve", [(x**2 - x * y + y**2 - 7).subs({x: v, y: 2 * v}) for v in hx6], [0, 0])
FRQ6 = FRQ("An implicitly defined curve", r"Consider the curve given by $x^2 - xy + y^2 = 7$.", [
    Part("a", r"Show that $\dfrac{dy}{dx} = \dfrac{2x - y}{x - 2y}$.", selfcheck(r"\tfrac{dy}{dx} = \tfrac{2x - y}{x - 2y}"),
         r"Differentiate both sides with respect to $x$: $2x - \left(y + x\frac{dy}{dx}\right) + 2y\frac{dy}{dx} = 0$. "
         r"So $(2y - x)\frac{dy}{dx} = y - 2x$, and therefore $\frac{dy}{dx} = \frac{y - 2x}{2y - x} = \frac{2x - y}{x - 2y}$.",
         [(1, r"Differentiates implicitly, using the product rule on $xy$."), (1, r"Solves for $\frac{dy}{dx}$ and shows it equals $\frac{2x - y}{x - 2y}$.")], work="2.6cm", topic="3.2"),
    Part("b", r"Write an equation for the line tangent to the curve at the point $(2, 3)$. Use it to approximate the $y$-coordinate of the point on the curve near $(2, 3)$ with $x$-coordinate $2.4$.",
         num(sp.Rational(29, 10), display=r"y \approx 2.9"),
         r"At $(2, 3)$, $\frac{dy}{dx} = \frac{4 - 3}{2 - 6} = -\frac14$. The tangent line is $y = 3 - \frac14(x - 2)$, so at $x = 2.4$, $y \approx 3 - \frac14(0.4) = 2.9$.",
         [(1, r"Tangent line $y = 3 - \frac14(x - 2)$."), (1, r"Approximation $y \approx 2.9$.")], work="2.4cm", topic="4.6"),
    Part("c", r"Find the coordinates of each point on the curve at which the line tangent to the curve is horizontal.",
         selfcheck(r"\left(\tfrac{\sqrt{21}}{3}, \tfrac{2\sqrt{21}}{3}\right),\ \left(-\tfrac{\sqrt{21}}{3}, -\tfrac{2\sqrt{21}}{3}\right)"),
         r"A horizontal tangent needs $2x - y = 0$ with $x - 2y \ne 0$. Put $y = 2x$ into the equation of the curve: $x^2 - 2x^2 + 4x^2 = 3x^2 = 7$, so $x = \pm\sqrt{\frac73} = \pm\frac{\sqrt{21}}{3}$. "
         r"At these points $x - 2y = -3x \ne 0$. The points are $\left(\frac{\sqrt{21}}{3}, \frac{2\sqrt{21}}{3}\right)$ and $\left(-\frac{\sqrt{21}}{3}, -\frac{2\sqrt{21}}{3}\right)$.",
         [(1, r"Sets $2x - y = 0$ and substitutes $y = 2x$ into the equation of the curve."), (1, r"Finds both points.")], work="2.8cm", topic="5.12"),
    Part("d", r"Find the value of $\dfrac{d^2y}{dx^2}$ at the point $(3, 1)$.", num(42),
         r"At $(3, 1)$, $\frac{dy}{dx} = \frac{6 - 1}{3 - 2} = 5$. By the quotient rule, "
         r"$\frac{d^2y}{dx^2} = \frac{\left(2 - \frac{dy}{dx}\right)(x - 2y) - (2x - y)\left(1 - 2\frac{dy}{dx}\right)}{(x - 2y)^2}$. "
         r"At $(3, 1)$ with $\frac{dy}{dx} = 5$: $\frac{(2 - 5)(1) - (5)(1 - 10)}{1^2} = -3 + 45 = 42$.",
         [(1, r"Finds $\frac{dy}{dx} = 5$ at $(3, 1)$."), (1, r"Differentiates $\frac{2x - y}{x - 2y}$ with the quotient rule, treating $y$ as a function of $x$."),
          (1, r"Gives the answer, $42$.")], work="3.2cm", topic="3.6"),
], frq_type="Implicit differentiation")


EXAM = Exam(
    slug="ab1", title="AP Calculus AB Practice Exam 1", course="AB",
    mcq_a=PART_A, mcq_b=PART_B, frq_a=[FRQ1, FRQ2], frq_b=[FRQ3, FRQ4, FRQ5, FRQ6],
    members_only=False,
)
