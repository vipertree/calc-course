"""AP Calculus BC Practice Exam 1. Original questions in the current AP format:
Section I Part A (29 MC, no calculator, 62 min), Part B (13 MC, calculator, 38 min);
Section II Part A (2 FRQ, calculator, 30 min), Part B (4 FRQ, no calculator, 60 min).

Weighted like the BC exam: about 60% of the multiple choice is AB-level material (Units 1-8) and about 40% is
BC-only (6.11-6.13, 7.5, 7.9, 8.13, Units 9 and 10). The free response follows the usual BC mix: a rate problem
in context and a polar area problem with a calculator, then a graph of f', a differential equation in context,
parametric motion and a power series with an error bound without one.

Every keyed answer is computed here with sympy and checked against what the question prints. Calculator answers
are checked numerically to three decimal places. Each question carries the syllabus topic it tests, which the score
report uses to point back to lessons.
"""
import math

import sympy as sp

from calclib import FRQ, MCQ, Exam, Part, check, close, expr, limchain, num, same, selfcheck
from calclib.figs import graph

x, t, y, n = sp.symbols("x t y n", real=True)
th = sp.symbols("theta", real=True)
N = lambda f, a, b, v=x: float(sp.Integral(f, (v, a, b)).evalf(30))


def pick(stem, right, wrong, letter, solution, calc=False, topic="", figure=None):
    """An MCQ with the keyed answer at a planned letter."""
    k = "ABCD".index(letter)
    choices = list(wrong)
    choices.insert(k, right)
    return MCQ(stem, choices, letter, solution, calc=calc, topic=topic, figure=figure)


def numpick(stem, right, wrong, solution, topic="", fmt=None, figure=None):
    """A calculator MCQ with numeric choices in increasing order, as on the AP exam. The keyed letter is wherever the
    right value sorts to."""
    fmt = fmt or (lambda v: f"${v:.3f}$")
    vals = sorted([right] + list(wrong))
    texts = [fmt(v) for v in vals]
    check(f"numpick distinct: {stem[:40]}", len(set(texts)) == 4, str(texts))
    return MCQ(stem, texts, "ABCD"[vals.index(right)], solution, calc=True, topic=topic, figure=figure)


def r3(label, v):
    """Pin a calculator answer: the printed value is v rounded to three decimals."""
    close(label, v, round(v, 3), 5e-4 + 1e-12)
    return v


def sign_changes(f, a, b, steps=4000):
    """Where a numeric function changes sign on [a, b], found on a fine grid."""
    grid = [a + (b - a) * k / steps for k in range(steps + 1)]
    vals = [f(v) for v in grid]
    return [grid[k] for k in range(steps) if vals[k] * vals[k + 1] < 0]


def converges(term, var=n, start=1):
    """True or False from sympy's convergence tests (None if sympy can't decide, which fails the check)."""
    r = sp.Sum(term, (var, start, sp.oo)).is_convergent()
    return None if r is None else bool(r)


# ====================================================================== Section I, Part A: no calculator
same("A1", sp.limit((3 * x**2 - 5 * x) / sp.sqrt(4 * x**4 + 1), x, sp.oo), sp.Rational(3, 2))
a_ = sp.symbols("a")
same("A2 a", sp.solve((x**2 + a_ * x - 6).subs(x, 2), a_), [1])
same("A2 k", sp.limit((x**2 + x - 6) / (x - 2), x, 2), 5)
m_, b_ = sp.symbols("m b")
s3 = sp.solve([sp.Eq(2 * m_ + b_, 2**3 - 2), sp.Eq(m_, sp.diff(x**3 - x, x).subs(x, 2))], [m_, b_])
same("A3", [s3[m_], s3[b_]], [11, -16])
same("A4", sp.diff(sp.asin(x**2), x).subs(x, sp.Rational(1, 2)), 4 / sp.sqrt(15))
same("A5", [(x + sp.exp(x)).subs(x, 0), 1 / sp.diff(x + sp.exp(x), x).subs(x, 0)], [1, sp.Rational(1, 2)])
yx = sp.Function("y")(x)
dA6 = sp.solve(sp.diff(x**2 * yx + yx**3 - 2, x), sp.diff(yx, x))[0]
same("A6", [1 + 1, dA6.subs(yx, 1).subs(x, 1)], [2, -sp.Rational(1, 2)])
v7, a7 = t**2 - 4 * t + 3, 2 * t - 4
check("A7 speed increasing where v and a share a sign",
      sp.solve_univariate_inequality(v7 * a7 > 0, t, relational=False).intersect(sp.Interval(0, sp.oo))
      == sp.Union(sp.Interval.open(1, 2), sp.Interval.open(3, sp.oo)))
same("A8", sp.limit((1 + 3 / x)**x, x, sp.oo), sp.exp(3))
f9 = x**4 - 4 * x**3 + 6
same("A9 zeros of f''", sp.solve(sp.diff(f9, x, 2), x), [0, 2])
check("A9 f'' changes sign at both", all(sp.diff(f9, x, 2).subs(x, c - sp.Rational(1, 10)) * sp.diff(f9, x, 2).subs(x, c + sp.Rational(1, 10)) < 0 for c in (0, 2)))
fp10 = x**2 - 2 * x - 8
same("A10", [sp.solve(fp10, x), [sp.diff(fp10, x).subs(x, c) for c in (-2, 4)]], [[-2, 4], [-6, 6]])
F11 = sp.Piecewise((2 - 2 * x, x <= 2), (2 * x - 6, x <= 4), (2, True))
same("A11 zeros of f", [F11.subs(x, 1), F11.subs(x, 3)], [0, 0])
check("A11 f: + to - at 1, - to + at 3", F11.subs(x, 0.5) > 0 > F11.subs(x, 1.5) and F11.subs(x, 2.5) < 0 < F11.subs(x, 3.5))
same("A12", sp.integrate(sp.sin(x) / sp.cos(x)**2, (x, 0, sp.pi / 3)), 1)
ans13 = x / 2 * sp.sin(2 * x) + sp.cos(2 * x) / 4
same("A13", sp.simplify(sp.diff(ans13, x) - x * sp.cos(2 * x)), 0)
ans14 = 2 * sp.log(x - 1) + 3 * sp.log(x + 2)
same("A14", sp.simplify(sp.diff(ans14, x) - (5 * x + 1) / (x**2 + x - 2)), 0)
same("A14 partial fractions", sp.apart((5 * x + 1) / (x**2 + x - 2), x), 2 / (x - 1) + 3 / (x + 2))
bb = sp.symbols("b", positive=True)
same("A15", sp.limit(sp.integrate(x * sp.exp(-x**2), (x, 0, bb)), bb, sp.oo), sp.Rational(1, 2))
same("A16", sp.integrate(sp.sqrt(x), (x, 1, 4)), sp.Rational(14, 3))
close("A16 the sum is that integral", sum(3 / 4000 * math.sqrt(1 + 3 * k / 4000) for k in range(1, 4001)), 14 / 3, 2e-3)
e17 = [(0, sp.Integer(1))]
for _ in range(2):
    X, Y = e17[-1]
    e17.append((X + sp.Rational(1, 2), Y + sp.Rational(1, 2) * (X + Y)))
same("A17 Euler", e17[-1], (1, sp.Rational(5, 2)))
P = sp.symbols("P", positive=True)
same("A18 fastest growth where dP/dt is largest", sp.solve(sp.diff(sp.Rational(2, 5) * P * (1 - P / 600), P), P), [300])
sol19 = 1 / (1 - sp.sin(x))
same("A19", [sp.simplify(sp.diff(sol19, x) - sol19**2 * sp.cos(x)), sol19.subs(x, 0)], [0, 1])
X20, Y20 = t**2 + 1, t**3 - 3 * t
same("A20", (sp.diff(Y20, t) / sp.diff(X20, t)).subs(t, 2), sp.Rational(9, 4))
X21, Y21 = t**2, t**3 + t
d1_21 = sp.diff(Y21, t) / sp.diff(X21, t)
same("A21", sp.simplify(sp.diff(d1_21, t) / sp.diff(X21, t)).subs(t, 1), sp.Rational(1, 2))
same("A22", sp.Rational(1, 2) * sp.integrate((2 * sp.sin(3 * th))**2, (th, 0, sp.pi / 3)), sp.pi / 3)
check("A22 one petal is 0 to pi/3", sp.sin(3 * sp.pi / 3) == 0 and sp.sin(3 * sp.pi / 6) == 1)
same("A23", sp.Sum(3 * sp.Rational(-2, 5)**n, (n, 1, sp.oo)).doit(), -sp.Rational(6, 7))
nI = sp.symbols("n", positive=True, integer=True)
check("A24 I diverges", converges(nI / (nI**2 + 1), nI) is False and sp.limit(nI / (nI**2 + 1) / (1 / nI), nI, sp.oo) == 1)
check("A24 II converges (AST)", sp.limit(1 / sp.log(nI + 1), nI, sp.oo) == 0)
check("A24 III diverges (nth term)", sp.limit(nI / (nI + 2), nI, sp.oo) == 1)
check("A25 conditional", converges(1 / sp.sqrt(nI), nI) is False and sp.limit(1 / sp.sqrt(nI), nI, sp.oo) == 0)
check("A25 others absolute or divergent", converges(1 / nI**2, nI) and sp.limit(nI / (2 * nI + 1), nI, sp.oo) == sp.Rational(1, 2)
      and converges(sp.Rational(2, 3)**nI, nI))
TAB26 = [3, -1, 4, 12]                                   # f(2), f'(2), f''(2), f'''(2)
P26 = sum(sp.Integer(c) / sp.factorial(k) * (x - 2)**k for k, c in enumerate(TAB26))
same("A26", P26.subs(x, sp.Rational(5, 2)), sp.Rational(13, 4))
same("A27", sp.Integer(6) * sp.Rational(1, 2)**4 / sp.factorial(4), sp.Rational(1, 64))
same("A28 radius", sp.limit(((nI + 1) * 3**(nI + 1)) / (nI * 3**nI), nI, sp.oo), 3)
check("A28 x = 5 diverges, x = -1 converges", converges(1 / nI, nI) is False and converges((-1)**nI / nI, nI) is True)
same("A29", sp.Sum((-1)**n * (sp.pi / 3)**(2 * n) / sp.factorial(2 * n), (n, 0, sp.oo)).doit(), sp.Rational(1, 2))

TABLE26 = (r"\par\smallskip\centerline{\begin{tabular}{cccc} $f(2)$ & $f'(2)$ & $f''(2)$ & $f'''(2)$ \\ \hline "
           + " & ".join(f"${v}$" for v in TAB26) + r"\end{tabular}}")
FIG11 = graph("exam_bc1_a11", [("2-2*x", 0, 2), ("2*x-6", 2, 4), ("2", 4, 6)], (-0.5, 6.5), (-2.6, 2.6),
              closed=[(0, 2), (6, 2)], caption=r"The graph of $f$, which consists of three line segments.", w="7.5cm", h="5cm")

PART_A = [
    pick(r"$\displaystyle\lim_{x\to\infty} \frac{3x^2 - 5x}{\sqrt{4x^4 + 1}}$ is", r"$\frac32$", [r"$\frac34$", r"$3$", r"$0$"], "A",
         r"For $x > 0$, $\sqrt{4x^4 + 1} = x^2\sqrt{4 + \frac{1}{x^4}}$. Divide the numerator and the denominator by $x^2$: "
         r"$\displaystyle\lim_{x\to\infty} \frac{3x^2 - 5x}{\sqrt{4x^4 + 1}} = \lim_{x\to\infty} \frac{3 - \frac5x}{\sqrt{4 + \frac{1}{x^4}}} = \frac{3}{\sqrt4} = \frac32$.",
         topic="1.15"),
    pick(r"Let $f(x) = \begin{cases} \dfrac{x^2 + ax - 6}{x - 2}, & x \ne 2 \\ k, & x = 2. \end{cases}$ For what values of the constants $a$ and $k$ is $f$ continuous at $x = 2$?",
         r"$a = 1$ and $k = 5$", [r"$a = 1$ and $k = 0$", r"$a = -1$ and $k = 5$", r"$a = 1$ and $k = 3$"], "A",
         r"For $\displaystyle\lim_{x\to 2} f(x)$ to exist, the numerator must be $0$ at $x = 2$: $4 + 2a - 6 = 0$, so $a = 1$. Then "
         + limchain(2, [r"\frac{x^2 + x - 6}{x - 2}", r"\frac{(x + 3)(x - 2)}{x - 2}", r"(x + 3)"], "5")
         + r". For continuity, $f(2) = k$ must equal this limit, so $k = 5$.", topic="1.13"),
    pick(r"Let $f(x) = \begin{cases} x^3 - x, & x \le 2 \\ mx + b, & x > 2. \end{cases}$ If $f$ is differentiable at $x = 2$, what are the values of $m$ and $b$?",
         r"$m = 11$ and $b = -16$", [r"$m = 11$ and $b = 6$", r"$m = 12$ and $b = -18$", r"$m = 3$ and $b = 0$"], "D",
         r"A differentiable function is continuous, so the pieces meet at $x = 2$: $2m + b = 2^3 - 2 = 6$. "
         r"The slopes must also match: $m = \frac{d}{dx}\left(x^3 - x\right)$ at $x = 2$, which is $3(2)^2 - 1 = 11$. Then $b = 6 - 22 = -16$.",
         topic="2.4"),
    pick(r"If $y = \arcsin\left(x^2\right)$, what is the value of $\dfrac{dy}{dx}$ at $x = \frac12$?", r"$\frac{4}{\sqrt{15}}$",
         [r"$\frac{2}{\sqrt3}$", r"$\frac{1}{\sqrt{15}}$", r"$\frac{16}{15}$"], "D",
         r"$\frac{dy}{dx} = \frac{1}{\sqrt{1 - \left(x^2\right)^2}} \cdot 2x = \frac{2x}{\sqrt{1 - x^4}}$. At $x = \frac12$: $\frac{1}{\sqrt{1 - \frac{1}{16}}} = \frac{1}{\sqrt{15/16}} = \frac{4}{\sqrt{15}}$.",
         topic="3.4"),
    pick(r"Let $f(x) = x + e^x$, and let $g$ be the inverse function of $f$. What is the value of $g'(1)$?", r"$\frac12$",
         [r"$\frac{1}{1 + e}$", r"$2$", r"$1 + e$"], "A",
         r"$f(0) = 0 + e^0 = 1$, so $g(1) = 0$. $f'(x) = 1 + e^x$, so $g'(1) = \frac{1}{f'(g(1))} = \frac{1}{f'(0)} = \frac{1}{2}$.",
         topic="3.3"),
    pick(r"What is the slope of the line tangent to the curve $x^2 y + y^3 = 2$ at the point $(1, 1)$?", r"$-\frac12$",
         [r"$-\frac23$", r"$-2$", r"$\frac12$"], "A",
         r"Differentiate implicitly, with the product rule on $x^2y$: $2xy + x^2\frac{dy}{dx} + 3y^2\frac{dy}{dx} = 0$, so $\frac{dy}{dx} = -\frac{2xy}{x^2 + 3y^2}$. "
         r"At $(1, 1)$, $\frac{dy}{dx} = -\frac{2}{4} = -\frac12$.", topic="3.2"),
    pick(r"A particle moves along the $x$-axis with velocity $v(t) = t^2 - 4t + 3$ for $t \ge 0$. For which values of $t$ is the speed of the particle increasing?",
         r"$1 < t < 2$ and $t > 3$", [r"$t > 2$ only", r"$0 \le t < 1$ and $t > 3$", r"$1 < t < 3$"], "A",
         r"$v(t) = (t - 1)(t - 3)$ and $a(t) = v'(t) = 2t - 4$. The speed increases when $v$ and $a$ have the same sign. "
         r"On $1 < t < 2$, $v < 0$ and $a < 0$; on $t > 3$, $v > 0$ and $a > 0$. On $0 \le t < 1$ and $2 < t < 3$ the signs differ, so the speed decreases there.",
         topic="4.2"),
    pick(r"$\displaystyle\lim_{x\to\infty} \left(1 + \frac3x\right)^x$ is", r"$e^3$", [r"$1$", r"$3$", r"$e^{1/3}$"], "D",
         r"Let $L$ be the limit and take the natural log of the expression: $\ln\left(1 + \frac3x\right)^x = \frac{\ln\left(1 + \frac3x\right)}{\frac1x}$, which has the form $\frac00$ as $x\to\infty$. By L'Hospital's Rule, "
         r"$\displaystyle\lim_{x\to\infty} \frac{\ln\left(1 + \frac3x\right)}{\frac1x} = \lim_{x\to\infty} \frac{\frac{-3/x^2}{1 + 3/x}}{-\frac{1}{x^2}} = \lim_{x\to\infty} \frac{3}{1 + \frac3x} = 3$. "
         r"Therefore $\ln L = 3$, so $L = e^3$.", topic="4.7"),
    pick(r"At which values of $x$ does the graph of $f(x) = x^4 - 4x^3 + 6$ have a point of inflection?", r"$x = 0$ and $x = 2$",
         [r"$x = 0$ and $x = 3$", r"$x = 3$ only", r"$x = 2$ only"], "B",
         r"$f'(x) = 4x^3 - 12x^2$ and $f''(x) = 12x^2 - 24x = 12x(x - 2)$. $f''$ changes from positive to negative at $x = 0$ and from negative to positive at $x = 2$, "
         r"so the graph has points of inflection at both.", topic="5.6"),
    pick(r"The derivative of a function $f$ is $f'(x) = x^2 - 2x - 8$. Which of the following is true?",
         r"$f$ has a relative maximum at $x = -2$ and a relative minimum at $x = 4$.",
         [r"$f$ has a relative minimum at $x = -2$ and a relative maximum at $x = 4$.", r"$f$ has a relative minimum at $x = 1$ only.",
          r"$f$ has relative minima at $x = -2$ and $x = 4$."], "D",
         r"$f'(x) = (x - 4)(x + 2) = 0$ at $x = -2$ and $x = 4$, and $f''(x) = 2x - 2$. Since $f''(-2) = -6 < 0$, $f$ has a relative maximum at $x = -2$. "
         r"Since $f''(4) = 6 > 0$, $f$ has a relative minimum at $x = 4$.", topic="5.7"),
    pick(r"The graph of the function $f$ on $0 \le x \le 6$ is shown. Let $g(x) = \displaystyle\int_0^x f(t)\,dt$. Which of the following is true?",
         r"$g$ has a relative maximum at $x = 1$ and a relative minimum at $x = 3$.",
         [r"$g$ has a relative minimum at $x = 1$ and a relative maximum at $x = 3$.", r"$g$ has a relative minimum at $x = 2$ and no relative maximum.",
          r"$g$ has a relative maximum at $x = 4$ and no relative minimum."], "B",
         r"$g'(x) = f(x)$. From the graph, $f$ changes from positive to negative at $x = 1$, so $g$ has a relative maximum there, "
         r"and $f$ changes from negative to positive at $x = 3$, so $g$ has a relative minimum there.", topic="6.5", figure=FIG11),
    pick(r"$\displaystyle\int_0^{\pi/3} \frac{\sin x}{\cos^2 x}\,dx = $", r"$1$", [r"$2$", r"$\frac12$", r"$\sqrt3 - 1$"], "A",
         r"Let $u = \cos x$, so $du = -\sin x\,dx$; $u$ runs from $1$ to $\frac12$. "
         r"$\int_0^{\pi/3} \frac{\sin x}{\cos^2 x}\,dx = -\int_1^{1/2} u^{-2}\,du = \int_{1/2}^1 u^{-2}\,du = \left[-\frac1u\right]_{1/2}^1 = -1 + 2 = 1$.",
         topic="6.9"),
    pick(r"$\displaystyle\int x\cos(2x)\,dx = $", r"$\frac{x}{2}\sin(2x) + \frac14\cos(2x) + C$",
         [r"$\frac{x}{2}\sin(2x) - \frac14\cos(2x) + C$", r"$\frac{x^2}{4}\sin(2x) + C$", r"$x\sin(2x) + \frac12\cos(2x) + C$"], "D",
         r"Integrate by parts with $u = x$ and $dv = \cos(2x)\,dx$, so $du = dx$ and $v = \frac12\sin(2x)$: "
         r"$\int x\cos(2x)\,dx = \frac{x}{2}\sin(2x) - \int \frac12\sin(2x)\,dx = \frac{x}{2}\sin(2x) + \frac14\cos(2x) + C$.", topic="6.11"),
    pick(r"$\displaystyle\int \frac{5x + 1}{x^2 + x - 2}\,dx = $", r"$2\ln|x - 1| + 3\ln|x + 2| + C$",
         [r"$3\ln|x - 1| + 2\ln|x + 2| + C$", r"$\frac52\ln\left|x^2 + x - 2\right| + C$", r"$2\ln|x + 1| + 3\ln|x - 2| + C$"], "B",
         r"$x^2 + x - 2 = (x - 1)(x + 2)$. Write $\frac{5x + 1}{(x - 1)(x + 2)} = \frac{A}{x - 1} + \frac{B}{x + 2}$, so $5x + 1 = A(x + 2) + B(x - 1)$. "
         r"At $x = 1$: $6 = 3A$, so $A = 2$. At $x = -2$: $-9 = -3B$, so $B = 3$. Therefore the integral is $2\ln|x - 1| + 3\ln|x + 2| + C$.",
         topic="6.12"),
    pick(r"$\displaystyle\int_0^\infty x e^{-x^2}\,dx$ is", r"$\frac12$", [r"$1$", r"$-\frac12$", r"divergent"], "C",
         r"$\displaystyle\int_0^\infty x e^{-x^2}\,dx = \lim_{b\to\infty} \int_0^b x e^{-x^2}\,dx = \lim_{b\to\infty} \left[-\frac12 e^{-x^2}\right]_0^b = \lim_{b\to\infty} \left(\frac12 - \frac12 e^{-b^2}\right) = \frac12$.",
         topic="6.13"),
    pick(r"$\displaystyle\lim_{n\to\infty} \sum_{k=1}^n \frac3n\sqrt{1 + \frac{3k}{n}}$ is", r"$\frac{14}{3}$",
         [r"$2\sqrt3$", r"$\frac{14}{9}$", r"$\frac{16}{3}$"], "D",
         r"This is a right Riemann sum with $\Delta x = \frac3n$ and $x_k = 1 + \frac{3k}{n}$, which run from $1$ to $4$. "
         r"So the limit is $\int_1^4 \sqrt x\,dx = \left[\frac23 x^{3/2}\right]_1^4 = \frac23(8 - 1) = \frac{14}{3}$.", topic="6.3"),
    pick(r"Let $y = f(x)$ be the solution to the differential equation $\dfrac{dy}{dx} = x + y$ with the initial condition $f(0) = 1$. "
         r"What is the approximation for $f(1)$ found by using Euler's method, starting at $x = 0$, with two steps of equal size?",
         r"$2.5$", [r"$2$", r"$2.75$", r"$3.5$"], "B",
         r"The step size is $0.5$. At $(0, 1)$, $\frac{dy}{dx} = 1$, so $f(0.5) \approx 1 + 0.5(1) = 1.5$. "
         r"At $(0.5, 1.5)$, $\frac{dy}{dx} = 2$, so $f(1) \approx 1.5 + 0.5(2) = 2.5$.", topic="7.5"),
    pick(r"The number of fish in a pond, $P(t)$, satisfies the logistic differential equation $\dfrac{dP}{dt} = 0.4P\left(1 - \dfrac{P}{600}\right)$, where $t$ is measured in years. "
         r"If $P(0) = 100$, what is the number of fish when the population is growing the fastest?",
         r"$300$", [r"$100$", r"$150$", r"$600$"], "C",
         r"$\frac{dP}{dt}$ is a quadratic in $P$ that is $0$ at $P = 0$ and $P = 600$, so it is greatest halfway between, at $P = 300$. "
         r"Since $P(0) = 100 < 300$ and $P$ increases toward the carrying capacity $600$, the population passes $300$ and grows fastest there.", topic="7.9"),
    pick(r"Let $y = f(x)$ be the solution to the differential equation $\dfrac{dy}{dx} = y^2\cos x$ with the initial condition $f(0) = 1$. Which of the following is $f(x)$?",
         r"$\dfrac{1}{1 - \sin x}$", [r"$\dfrac{1}{1 + \sin x}$", r"$e^{\sin x}$", r"$\dfrac{1}{\cos x}$"], "A",
         r"Separate: $y^{-2}\,dy = \cos x\,dx$, so $-\frac1y = \sin x + C$. With $x = 0$, $y = 1$: $-1 = 0 + C$, so $C = -1$. "
         r"Then $-\frac1y = \sin x - 1$, and therefore $y = \frac{1}{1 - \sin x}$.", topic="7.7"),
    pick(r"A curve is defined by the parametric equations $x = t^2 + 1$ and $y = t^3 - 3t$. What is the slope of the line tangent to the curve at the point where $t = 2$?",
         r"$\frac94$", [r"$\frac49$", r"$9$", r"$\frac25$"], "D",
         r"$\frac{dy}{dx} = \frac{dy/dt}{dx/dt} = \frac{3t^2 - 3}{2t}$. At $t = 2$, $\frac{dy}{dx} = \frac{12 - 3}{4} = \frac94$.", topic="9.1"),
    pick(r"A curve is defined by the parametric equations $x = t^2$ and $y = t^3 + t$. What is the value of $\dfrac{d^2y}{dx^2}$ at the point where $t = 1$?",
         r"$\frac12$", [r"$1$", r"$2$", r"$3$"], "A",
         r"$\frac{dy}{dx} = \frac{3t^2 + 1}{2t}$. Then $\frac{d}{dt}\left(\frac{dy}{dx}\right) = \frac{6t \cdot 2t - (3t^2 + 1) \cdot 2}{4t^2} = \frac{6t^2 - 2}{4t^2}$, which is $1$ at $t = 1$. "
         r"So $\frac{d^2y}{dx^2} = \frac{\frac{d}{dt}\left(\frac{dy}{dx}\right)}{dx/dt} = \frac{1}{2} $ at $t = 1$.", topic="9.2"),
    pick(r"What is the area of one petal of the polar curve $r = 2\sin(3\theta)$?", r"$\frac\pi3$", [r"$\pi$", r"$\frac{2\pi}{3}$", r"$\frac\pi6$"], "B",
         r"One petal is traced for $0 \le \theta \le \frac\pi3$, where $r \ge 0$. Area $= \frac12\int_0^{\pi/3} 4\sin^2(3\theta)\,d\theta = \int_0^{\pi/3} \left(1 - \cos(6\theta)\right) d\theta = \left[\theta - \frac{\sin(6\theta)}{6}\right]_0^{\pi/3} = \frac\pi3$.",
         topic="9.8"),
    pick(r"$\displaystyle\sum_{n=1}^\infty 3\left(-\frac25\right)^n = $", r"$-\frac67$", [r"$\frac{15}{7}$", r"$5$", r"$-2$"], "D",
         r"A geometric series with first term $3\left(-\frac25\right) = -\frac65$ and ratio $-\frac25$, and $\left|-\frac25\right| < 1$, so it converges to "
         r"$\frac{-6/5}{1 - \left(-\frac25\right)} = \frac{-6/5}{7/5} = -\frac67$.", topic="10.2"),
    pick(r"Which of the following series converge?\par\smallskip"
         r"\quad I. $\displaystyle\sum_{n=1}^\infty \frac{n}{n^2 + 1}$\qquad II. $\displaystyle\sum_{n=1}^\infty \frac{(-1)^n}{\ln(n + 1)}$\qquad III. $\displaystyle\sum_{n=1}^\infty \frac{(-1)^n n}{n + 2}$",
         r"II only", [r"I and II only", r"II and III only", r"I, II, and III"], "A",
         r"I diverges: $\frac{n}{n^2 + 1}$ behaves like $\frac1n$, and $\displaystyle\lim_{n\to\infty} \frac{n/(n^2 + 1)}{1/n} = \lim_{n\to\infty} \frac{n^2}{n^2 + 1} = 1$, so by the limit comparison test with the harmonic series it diverges. "
         r"II converges by the alternating series test: $\frac{1}{\ln(n + 1)}$ decreases and $\displaystyle\lim_{n\to\infty} \frac{1}{\ln(n + 1)} = 0$. "
         r"III diverges by the $n$th term test: $\displaystyle\lim_{n\to\infty} \frac{n}{n + 2} = 1$, so the terms do not approach $0$.", topic="10.7"),
    pick(r"Which of the following series is conditionally convergent?", r"$\displaystyle\sum_{n=1}^\infty \frac{(-1)^n}{\sqrt n}$",
         [r"$\displaystyle\sum_{n=1}^\infty \frac{(-1)^n}{n^2}$", r"$\displaystyle\sum_{n=1}^\infty \frac{(-1)^n n}{2n + 1}$", r"$\displaystyle\sum_{n=1}^\infty (-1)^n\left(\frac23\right)^n$"], "C",
         r"$\sum \frac{(-1)^n}{\sqrt n}$ converges by the alternating series test, but $\sum \frac{1}{\sqrt n}$ is a $p$-series with $p = \frac12 \le 1$, which diverges. So it is conditionally convergent. "
         r"$\sum \frac{1}{n^2}$ and $\sum \left(\frac23\right)^n$ converge, so those two are absolutely convergent, and $\sum \frac{(-1)^n n}{2n + 1}$ diverges by the $n$th term test.",
         topic="10.9"),
    pick(r"The function $f$ has derivatives of all orders. Selected values of $f$ and its derivatives are shown in the table. "
         r"What is the approximation of $f(2.5)$ given by the third-degree Taylor polynomial for $f$ about $x = 2$?" + TABLE26,
         r"$3.25$", [r"$3$", r"$3.5$", r"$5$"], "B",
         r"$P_3(x) = 3 - (x - 2) + \frac{4}{2!}(x - 2)^2 + \frac{12}{3!}(x - 2)^3 = 3 - (x - 2) + 2(x - 2)^2 + 2(x - 2)^3$. "
         r"$P_3(2.5) = 3 - 0.5 + 2(0.25) + 2(0.125) = 3.25$.", topic="10.11"),
    pick(r"The function $f$ has derivatives of all orders, and $\left|f^{(4)}(x)\right| \le 6$ for $0 \le x \le 0.5$. The third-degree Taylor polynomial for $f$ about $x = 0$ is used to approximate $f(0.5)$. "
         r"Of the following, which is the smallest bound on the error of this approximation given by the Lagrange error bound?",
         r"$\frac{1}{64}$", [r"$\frac{1}{16}$", r"$\frac18$", r"$\frac38$"], "C",
         r"The Lagrange error bound for $P_3$ is $\frac{\max\left|f^{(4)}\right|}{4!}|x - 0|^4 = \frac{6}{24}(0.5)^4 = \frac14 \cdot \frac{1}{16} = \frac{1}{64}$.",
         topic="10.12"),
    pick(r"What is the interval of convergence of the power series $\displaystyle\sum_{n=1}^\infty \frac{(x - 2)^n}{n \cdot 3^n}$?",
         r"$-1 \le x < 5$", [r"$-1 < x < 5$", r"$-1 < x \le 5$", r"$-1 \le x \le 5$"], "D",
         r"Ratio test: $\displaystyle\lim_{n\to\infty} \left|\frac{(x - 2)^{n + 1}}{(n + 1)3^{n + 1}} \cdot \frac{n \cdot 3^n}{(x - 2)^n}\right| = \lim_{n\to\infty} \frac{n}{n + 1} \cdot \frac{|x - 2|}{3} = \frac{|x - 2|}{3}$. "
         r"The series converges when $\frac{|x - 2|}{3} < 1$, so $-1 < x < 5$. At $x = 5$ the series is $\sum \frac1n$, which diverges. "
         r"At $x = -1$ it is $\sum \frac{(-1)^n}{n}$, which converges by the alternating series test. Therefore the interval is $-1 \le x < 5$.", topic="10.13"),
    pick(r"$\displaystyle\sum_{n=0}^\infty \frac{(-1)^n}{(2n)!}\left(\frac\pi3\right)^{2n} = $", r"$\frac12$", [r"$\frac{\sqrt3}{2}$", r"$-\frac12$", r"$0$"], "A",
         r"The Maclaurin series for $\cos x$ is $\displaystyle\sum_{n=0}^\infty \frac{(-1)^n x^{2n}}{(2n)!}$, and it converges for all $x$. With $x = \frac\pi3$, the sum is $\cos\frac\pi3 = \frac12$.",
         topic="10.14"),
]


# ====================================================================== Section I, Part B: graphing calculator
N1 = 400 * t**2 * sp.exp(-sp.Rational(3, 5) * t)
b1 = r3("B1", float(sp.diff(N1, t).subs(t, 3)))
same("B1 exact", sp.diff(N1, t).subs(t, 3), 240 * sp.exp(-sp.Rational(9, 5)))

F2 = sp.exp(x / 2) + x
avg2 = float((F2.subs(x, 4) - F2.subs(x, 0)) / 4)
b2 = r3("B2", float(sp.nsolve(sp.diff(F2, x) - avg2, x, 2)))
check("B2 c in (0, 4) and unique (f' increasing)", 0 < b2 < 4 and sp.diff(F2, x, 2).subs(x, 0) > 0)

FP3 = sp.exp(x) - 3 * x
z3 = sorted(float(sp.nsolve(FP3, x, g)) for g in (0.6, 1.5))
same("B3 two zeros of f' on (0, 3)", len(sign_changes(sp.lambdify(x, FP3), 0, 3)), 2)
check("B3 + - + : max then min", FP3.subs(x, 0.3) > 0 > FP3.subs(x, 1) and FP3.subs(x, 2) > 0)
close("B3 printed zeros", z3[0], 0.619, 5e-4)
close("B3 printed zeros", z3[1], 1.512, 5e-4)
close("B3 inflection", math.log(3), 1.099, 5e-4)

Y4 = math.sqrt(10**2 - 6.5**2)
b4 = r3("B4", -6.5 * 0.5 / Y4)

FP5 = sp.sin(x**2) + 1
b5 = r3("B5", 3 + N(FP5, 1, 3))

k6 = sp.log(sp.Rational(350, 200)) / 3
b6 = r3("B6", float(sp.log(5) / k6))

V8 = 3 * sp.cos(t**2 / 4)
turn8 = float(sp.sqrt(2 * sp.pi))
same("B8 one turn on (0, 4)", len(sign_changes(sp.lambdify(t, V8), 0, 4)), 1)
disp8 = N(V8, 0, 4, t)
dist8 = abs(N(V8, 0, turn8, t)) + abs(N(V8, turn8, 4, t))
b8 = r3("B8", -2 + disp8)

W9 = 40 * t * sp.exp(-t / 10)
out9 = N(W9, 0, 12, t)
same("B9 exact", sp.simplify(sp.integrate(W9, (t, 0, 12))), 4000 - 8800 * sp.exp(-sp.Rational(6, 5)))
b9 = 5000 - out9
close("B9 to the cent", b9, float(1000 + 8800 * sp.exp(-sp.Rational(6, 5))), 1e-9)

TOP10, BOT10 = 2 * sp.cos(x), x**2 - 1
a10 = float(sp.nsolve(TOP10 - BOT10, x, 1.2))
check("B10 symmetric region", sp.simplify((TOP10 - BOT10).subs(x, -x) - (TOP10 - BOT10)) == 0)
b10 = r3("B10", N(TOP10 - BOT10, -a10, a10))
b12 = r3("B12", float(sp.pi) * N((3 - BOT10)**2 - (3 - TOP10)**2, -a10, a10))
check("B12 region below y = 3", float(TOP10.subs(x, 0)) < 3)

b13 = r3("B13", N(sp.sqrt(1 + x**4), 0, 2))
XP14, YP14 = sp.log(t**2 + 1), 2 * sp.cos(t)
b14 = r3("B14", N(sp.sqrt(XP14**2 + YP14**2), 0, 2, t))
disp14 = math.hypot(N(XP14, 0, 2, t), N(YP14, 0, 2, t))

R15 = 2 * th - sp.sin(th)
dy15 = sp.diff(R15 * sp.sin(th), th)
b15 = r3("B15", float(dy15.subs(th, 2)))
dx15 = float(sp.diff(R15 * sp.cos(th), th).subs(th, 2))

PART_B = [
    numpick(r"The number of people at a farmers market $t$ hours after it opens is modeled by $N(t) = 400t^2 e^{-0.6t}$. "
            r"At what rate, in people per hour, is the number of people at the market changing at time $t = 3$?",
            b1, [float(N1.subs(t, 3)) / 3, float(400 * 6 * sp.exp(-1.8)), -b1],
            rf"$N'(t) = 400\left(2t e^{{-0.6t}} - 0.6t^2 e^{{-0.6t}}\right)$, so $N'(3) \approx {b1:.3f}$ people per hour.", topic="4.3"),
    numpick(r"Let $f(x) = e^{x/2} + x$. What value of $c$ in the open interval $(0, 4)$ satisfies the conclusion of the Mean Value Theorem for $f$ on the closed interval $[0, 4]$?",
            b2, [2.0, avg2, b2 / 2],
            rf"The average rate of change is $\frac{{f(4) - f(0)}}{{4}} = \frac{{e^2 + 3}}{{4}} \approx {avg2:.4f}$. "
            rf"Solve $f'(c) = \frac12 e^{{c/2}} + 1 = \frac{{e^2 + 3}}{{4}}$ with the calculator: $c \approx {b2:.3f}$.", topic="5.1"),
    pick(r"The derivative of a function $f$ is $f'(x) = e^x - 3x$. At which values of $x$ in the open interval $0 < x < 3$ does $f$ have a relative minimum?",
         r"$x \approx 1.512$ only", [r"$x \approx 0.619$ only", r"$x \approx 1.099$ only", r"$x \approx 0.619$ and $x \approx 1.512$"], "B",
         rf"Graph $f'$: it is $0$ at $x \approx {z3[0]:.3f}$ and $x \approx {z3[1]:.3f}$. $f'$ changes from positive to negative at ${z3[0]:.3f}$ (a relative maximum) "
         rf"and from negative to positive at ${z3[1]:.3f}$. So $f$ has a relative minimum at $x \approx {z3[1]:.3f}$ only.", calc=True, topic="5.4"),
    numpick(r"Nasrin leans a $10$-foot ladder against a vertical wall. The bottom of the ladder slides away from the wall at a constant rate of $0.5$ foot per second. "
            r"How fast, in feet per second, is the top of the ladder moving down the wall at the instant the bottom is $6.5$ feet from the wall? (A negative value means the top is moving down.)",
            b4, [-b4, -6.5 / Y4, -Y4 / 6.5 * 0.5],
            rf"Let $x$ be the distance from the wall to the bottom and $y$ the height of the top, so $x^2 + y^2 = 100$ and $2x\frac{{dx}}{{dt}} + 2y\frac{{dy}}{{dt}} = 0$. "
            rf"When $x = 6.5$, $y = \sqrt{{100 - 6.5^2}} \approx {Y4:.4f}$, so $\frac{{dy}}{{dt}} = -\frac{{x}}{{y}}\frac{{dx}}{{dt}} \approx -\frac{{6.5}}{{{Y4:.4f}}}(0.5) \approx {b4:.3f}$ feet per second.",
            topic="4.5"),
    numpick(r"The derivative of a function $f$ is $f'(x) = \sin\left(x^2\right) + 1$, and $f(1) = 3$. What is the value of $f(3)$?",
            b5, [b5 - 3, 3 + float(FP5.subs(x, 3)) * 2, 3 + N(sp.sin(x**2), 1, 3)],
            rf"$f(3) = f(1) + \int_1^3 f'(x)\,dx = 3 + \int_1^3 \left(\sin\left(x^2\right) + 1\right) dx \approx 3 + {b5 - 3:.3f} = {b5:.3f}$.", topic="6.7"),
    numpick(r"A culture of bacteria in Tomás's lab grows at a rate proportional to the number of bacteria present. There are $200$ bacteria at time $t = 0$ and $350$ bacteria at $t = 3$ hours. "
            r"At what time $t$, in hours, will there be $1000$ bacteria?",
            b6, [16.0, 3 * 5 / 1.75, float(5 * 3 / sp.log(sp.Rational(350, 200)))],
            rf"$\frac{{dB}}{{dt}} = kB$, so $B(t) = 200e^{{kt}}$. From $B(3) = 350$, $e^{{3k}} = 1.75$, so $k = \frac{{\ln 1.75}}{{3}}$. "
            rf"Solve $200e^{{kt}} = 1000$: $t = \frac{{\ln 5}}{{k}} = \frac{{3\ln 5}}{{\ln 1.75}} \approx {b6:.3f}$ hours.", topic="7.8"),
    numpick(r"A particle moves along the $x$-axis with velocity $v(t) = 3\cos\left(\frac{t^2}{4}\right)$ for $0 \le t \le 4$. At time $t = 0$ the particle is at $x = -2$. What is the position of the particle at time $t = 4$?",
            b8, [disp8, -2 + dist8, -2 - disp8],
            rf"$x(4) = x(0) + \int_0^4 v(t)\,dt \approx -2 + {disp8:.3f} = {b8:.3f}$.", topic="8.2"),
    numpick(r"An ATM holds $\$5{,}000$ at the start of a $12$-hour day. During the day, money is withdrawn at a rate of $W(t) = 40te^{-0.1t}$ dollars per hour, where $t$ is the number of hours since the start of the day. "
            r"How much money is in the ATM at the end of the day?",
            b9, [out9, 5000 + out9, 5000 - 12 * float(W9.subs(t, 12))],
            rf"$5000 - \int_0^{{12}} W(t)\,dt \approx 5000 - {out9:.2f} = {b9:.2f}$, so \${b9:,.2f}.", topic="8.3",
            fmt=lambda v: rf"\${v:,.2f}"),
    numpick(r"Let $R$ be the region bounded by the graphs of $y = 2\cos x$ and $y = x^2 - 1$. What is the area of $R$?",
            b10, [b10 / 2, 2 * a10, b10 + 2 * N(2 * BOT10, 0, a10)],
            rf"The graphs meet at $x = \pm a$, where $a \approx {a10:.4f}$ (store it in the calculator). On $(-a, a)$, $2\cos x$ is on top, so the area is "
            rf"$\int_{{-a}}^a \left(2\cos x - \left(x^2 - 1\right)\right) dx \approx {b10:.3f}$.", topic="8.4"),
    numpick(r"Let $R$ be the region bounded by the graphs of $y = 2\cos x$ and $y = x^2 - 1$. What is the volume of the solid generated when $R$ is revolved about the horizontal line $y = 3$?",
            b12, [b12 / 2, float(sp.pi) * N((TOP10 - BOT10)**2, -a10, a10), float(sp.pi) * N((TOP10 + 3)**2 - (BOT10 + 3)**2, -a10, a10)],
            rf"With $a \approx {a10:.4f}$, the outer radius is $3 - \left(x^2 - 1\right) = 4 - x^2$ and the inner radius is $3 - 2\cos x$. "
            rf"Volume $= \pi\int_{{-a}}^a \left(\left(4 - x^2\right)^2 - (3 - 2\cos x)^2\right) dx \approx {b12:.3f}$.", topic="8.12"),
    numpick(r"What is the length of the curve $y = \frac{x^3}{3}$ from $x = 0$ to $x = 2$?",
            b13, [float(sp.sqrt(4 + sp.Rational(64, 9))), N(sp.sqrt(1 + x**6 / 9), 0, 2), N(1 + x**4, 0, 2)],
            rf"$\frac{{dy}}{{dx}} = x^2$, so the length is $\int_0^2 \sqrt{{1 + \left(x^2\right)^2}}\,dx = \int_0^2 \sqrt{{1 + x^4}}\,dx \approx {b13:.3f}$.", topic="8.13"),
    numpick(r"A particle moves in the $xy$-plane so that $\dfrac{dx}{dt} = \ln\left(t^2 + 1\right)$ and $\dfrac{dy}{dt} = 2\cos t$. What is the total distance traveled by the particle from $t = 0$ to $t = 2$?",
            b14, [disp14, float(sp.sqrt(XP14**2 + YP14**2).subs(t, 2)), N(XP14 + sp.Abs(YP14), 0, 2, t)],
            rf"Total distance traveled $= \int_0^2 \sqrt{{\left(\frac{{dx}}{{dt}}\right)^2 + \left(\frac{{dy}}{{dt}}\right)^2}}\,dt = \int_0^2 \sqrt{{\left(\ln\left(t^2 + 1\right)\right)^2 + 4\cos^2 t}}\,dt \approx {b14:.3f}$.",
            topic="9.6"),
    numpick(r"A curve is given by the polar equation $r = 2\theta - \sin\theta$. What is the value of $\dfrac{dy}{d\theta}$ at $\theta = 2$?",
            b15, [float(sp.diff(R15, th).subs(th, 2)), dx15, float((R15 * sp.sin(th)).subs(th, 2))],
            rf"$y = r\sin\theta = (2\theta - \sin\theta)\sin\theta$, so $\frac{{dy}}{{d\theta}} = (2 - \cos\theta)\sin\theta + (2\theta - \sin\theta)\cos\theta$. At $\theta = 2$ this is about ${b15:.3f}$.",
            topic="9.7"),
]


# ====================================================================== Section II, Part A: calculator
# ---- Question 1: bikes returned and checked out at a bike-share station
R1 = 9 + 7 * sp.sin(t**2 / 12)
C1 = 3 + 2 * t
D1 = R1 - C1
q1a = r3("Q1a", N(R1, 0, 8, t))
q1b = r3("Q1b", float(sp.diff(R1, t).subs(t, 4)))
q1c = r3("Q1c", 30 + N(D1, 0, 8, t))
turns1 = sign_changes(sp.lambdify(t, D1), 0, 8)
same("Q1 one sign change of B' on [0, 8]", len(turns1), 1)
c1 = float(sp.nsolve(D1, t, turns1[0]))
check("Q1 B' + to -", float(D1.subs(t, c1 - 0.01)) > 0 > float(D1.subs(t, c1 + 0.01)))
peak1 = 30 + N(D1, 0, c1, t)
check("Q1d least at t = 8", q1c < 30 < peak1)

FRQ1 = FRQ("Bike-share station", (
    r"Bikes are returned to a bike-share station that Daniela manages at a rate modeled by $R(t) = 9 + 7\sin\left(\frac{t^2}{12}\right)$ bikes per hour, "
    r"and bikes are checked out of the station at a rate modeled by $C(t) = 3 + 2t$ bikes per hour. Both are valid for $0 \le t \le 8$, where $t$ is measured in hours. "
    r"At time $t = 0$, there are $30$ bikes at the station."), [
    Part("a", r"How many bikes are returned to the station during the time interval $0 \le t \le 8$?",
         num(round(q1a, 3), tol=0.0015), rf"$\int_0^8 R(t)\,dt \approx {q1a:.3f}$ bikes.",
         [(1, r"Writes the integral $\int_0^8 R(t)\,dt$."), (1, rf"Gives the answer, ${q1a:.3f}$ bikes.")], work="2.4cm", topic="8.3"),
    Part("b", r"Find the value of $R'(4)$. Using correct units, interpret the meaning of $R'(4)$ in the context of the problem.",
         num(round(q1b, 3), tol=0.0015, display=rf"R'(4) \approx {q1b:.3f}"),
         rf"$R'(4) \approx {q1b:.3f}$. At time $t = 4$ hours, the rate at which bikes are returned to the station is increasing at ${q1b:.3f}$ bikes per hour per hour.",
         [(1, rf"Gives $R'(4) \approx {q1b:.3f}$."),
          (1, rf"Interprets, with units: at time $t = 4$ hours, the rate at which bikes are returned is increasing at ${q1b:.3f}$ bikes per hour per hour.")], work="2.4cm", topic="4.1"),
    Part("c", r"How many bikes are at the station at time $t = 8$?",
         num(round(q1c, 3), tol=0.0015), rf"$30 + \int_0^8 \left(R(t) - C(t)\right) dt \approx {q1c:.3f}$ bikes.",
         [(1, r"Writes $30 + \int_0^8 \left(R(t) - C(t)\right) dt$."), (1, rf"Gives the answer, ${q1c:.3f}$ bikes.")], work="2.4cm", topic="8.3"),
    Part("d", r"At what time $t$, for $0 \le t \le 8$, is the number of bikes at the station least? Justify your answer.",
         num(8, display=r"t = 8"),
         rf"Let $B(t)$ be the number of bikes at the station, so $B'(t) = R(t) - C(t)$. $B'(t) = 0$ when $t = c \approx {c1:.3f}$, and this is the only critical point on $0 < t < 8$. "
         rf"Candidates: $B(0) = 30$, $B(c) = 30 + \int_0^c \left(R(t) - C(t)\right) dt \approx {peak1:.3f}$, and $B(8) \approx {q1c:.3f}$ from part (c). "
         rf"Therefore the number of bikes is least at $t = 8$ hours.",
         [(1, r"Sets $R(t) - C(t) = 0$."), (1, rf"Finds the critical point $t \approx {c1:.3f}$ and computes $B$ there."),
          (1, r"Compares $B$ at the critical point and both endpoints, and answers $t = 8$.")], work="3.4cm", topic="5.5"),
], calc=True, frq_type="Rate in context")

# ---- Question 2: polar area
r2 = 2 + 2 * sp.sin(th)
same("Q2 meet r = 3 at pi/6 and 5pi/6", sp.solve(sp.Eq(r2, 3), th), [sp.pi / 6, 5 * sp.pi / 6])
q2a_exact = sp.Rational(1, 2) * sp.integrate(r2**2 - 9, (th, sp.pi / 6, 5 * sp.pi / 6))
same("Q2a exact", sp.simplify(q2a_exact), 9 * sp.sqrt(3) / 2 - sp.pi)
q2a = r3("Q2a", float(q2a_exact))
q2b = r3("Q2b", float(sp.diff(r2, th).subs(th, 7 * sp.pi / 6)))
same("Q2b exact, and r > 0 there", [sp.diff(r2, th).subs(th, 7 * sp.pi / 6), r2.subs(th, 7 * sp.pi / 6)], [-sp.sqrt(3), 1])
X2, Y2 = r2 * sp.cos(th), r2 * sp.sin(th)
slope2 = sp.simplify((sp.diff(Y2, th) / sp.diff(X2, th)).subs(th, sp.pi / 4))
same("Q2c exact", sp.nsimplify(slope2), -1 - sp.sqrt(2))
q2c = r3("Q2c", float(slope2))
q2d = r3("Q2d", float((sp.diff(Y2, th) * 2 * t).subs(th, t**2).subs(t, 1)))

_pts_out = [(float(r2.subs(th, a) * sp.cos(a)), float(r2.subs(th, a) * sp.sin(a))) for a in [math.pi / 6 + (2 * math.pi / 3) * k / 60 for k in range(61)]]
_pts_in = [(3 * math.cos(a), 3 * math.sin(a)) for a in [5 * math.pi / 6 - (2 * math.pi / 3) * k / 60 for k in range(61)]]
FILL2 = r"\fill[ink!14] " + " -- ".join(f"(axis cs:{p:.4f},{q:.4f})" for p, q in _pts_out + _pts_in) + " -- cycle;"
FIG2 = graph("exam_bc1_q2", [], (-3.6, 3.6), (-3.6, 4.6), w="7cm", h="8cm", ystep=1, under=FILL2,
             extra=r"\addplot[fn, domain=0:360, samples=240, variable=\t]({(2+2*sin(\t))*cos(\t)},{(2+2*sin(\t))*sin(\t)});"
                   r"\addplot[fn2, domain=0:360, samples=200, variable=\t]({3*cos(\t)},{3*sin(\t)});"
                   r"\node[font=\footnotesize] at (axis cs:0,3.5) {$R$};",
             caption=r"The cardioid $r = 2 + 2\sin\theta$ (solid) and the circle $r = 3$ (dashed). The shaded region $R$ is inside the cardioid and outside the circle.")
FRQ2 = FRQ("Polar curves", (
    r"The figure shows the graphs of the polar curves $r = 2 + 2\sin\theta$ and $r = 3$ for $0 \le \theta \le 2\pi$. "
    r"Let $R$ be the shaded region that is inside the graph of $r = 2 + 2\sin\theta$ and outside the graph of $r = 3$."), [
    Part("a", r"Find the area of $R$.", num(round(q2a, 3), tol=0.0015),
         rf"The curves meet where $2 + 2\sin\theta = 3$, so $\sin\theta = \frac12$ and $\theta = \frac\pi6$ or $\theta = \frac{{5\pi}}{{6}}$. "
         rf"Area $= \frac12\int_{{\pi/6}}^{{5\pi/6}} \left((2 + 2\sin\theta)^2 - 3^2\right) d\theta \approx {q2a:.3f}$.",
         [(1, r"Finds the limits $\theta = \frac\pi6$ and $\theta = \frac{5\pi}{6}$."), (1, r"Writes the integrand $\frac12\left((2 + 2\sin\theta)^2 - 9\right)$."),
          (1, rf"Gives the answer, ${q2a:.3f}$.")], work="3.4cm", topic="9.9"),
    Part("b", r"For the curve $r = 2 + 2\sin\theta$, find the value of $\dfrac{dr}{d\theta}$ at $\theta = \dfrac{7\pi}{6}$. Explain what this value indicates about the distance between the point on the curve and the origin.",
         num(round(q2b, 3), tol=0.0015, display=rf"\tfrac{{dr}}{{d\theta}} \approx {q2b:.3f}"),
         rf"$\frac{{dr}}{{d\theta}} = 2\cos\theta$, so at $\theta = \frac{{7\pi}}{{6}}$, $\frac{{dr}}{{d\theta}} = -\sqrt3 \approx {q2b:.3f}$. "
         r"Since $r = 1 > 0$ there and $\frac{dr}{d\theta} < 0$, the point on the curve is getting closer to the origin as $\theta$ increases through $\frac{7\pi}{6}$.",
         [(1, rf"Gives $\frac{{dr}}{{d\theta}} \approx {q2b:.3f}$."), (1, r"Explains: the distance between the point and the origin is decreasing, since $r > 0$ and $\frac{dr}{d\theta} < 0$.")],
         work="2.6cm", topic="9.7"),
    Part("c", r"Find the slope of the line tangent to the curve $r = 2 + 2\sin\theta$ at the point where $\theta = \dfrac{\pi}{4}$.",
         num(round(q2c, 3), tol=0.0015),
         rf"With $x = r\cos\theta$ and $y = r\sin\theta$, the slope is $\frac{{dy}}{{dx}} = \frac{{dy/d\theta}}{{dx/d\theta}} = \frac{{2\cos\theta\sin\theta + (2 + 2\sin\theta)\cos\theta}}{{2\cos\theta\cos\theta - (2 + 2\sin\theta)\sin\theta}}$. "
         rf"At $\theta = \frac\pi4$ this is about ${q2c:.3f}$.",
         [(1, r"Writes $\frac{dy}{dx} = \frac{dy/d\theta}{dx/d\theta}$ with $x = (2 + 2\sin\theta)\cos\theta$ and $y = (2 + 2\sin\theta)\sin\theta$."), (1, rf"Gives the answer, ${q2c:.3f}$.")],
         work="2.8cm", topic="9.7"),
    Part("d", r"A particle moves along the curve $r = 2 + 2\sin\theta$. At time $t$ seconds, the particle is at the point on the curve with $\theta = t^2$. "
              r"Find the rate at which the $y$-coordinate of the particle is changing at time $t = 1$.",
         num(round(q2d, 3), tol=0.0015),
         rf"$y = (2 + 2\sin\theta)\sin\theta$, so $\frac{{dy}}{{dt}} = \frac{{dy}}{{d\theta}} \cdot \frac{{d\theta}}{{dt}} = \left(2\cos\theta\sin\theta + (2 + 2\sin\theta)\cos\theta\right) \cdot 2t$. "
         rf"At $t = 1$, $\theta = 1$, and $\frac{{dy}}{{dt}} \approx {q2d:.3f}$.",
         [(1, r"Uses the chain rule: $\frac{dy}{dt} = \frac{dy}{d\theta} \cdot \frac{d\theta}{dt}$ with $\frac{d\theta}{dt} = 2t$."), (1, rf"Gives the answer, ${q2d:.3f}$.")],
         work="2.8cm", topic="9.7"),
], calc=True, frq_type="Polar", figure=FIG2)


# ====================================================================== Section II, Part B: no calculator
# ---- Question 3: the graph of f'
u3 = sp.symbols("u", real=True)
semi3 = sp.integrate(sp.sqrt(4 - u3**2), (u3, -2, 2))           # the semicircle piece, x = u - 2 on [-4, 0]
FP3G = {"seg1": -x, "seg2": 2 * x - 6}
f3 = {0: sp.Integer(3)}
f3[-4] = f3[0] - semi3
f3[2] = f3[0] + sp.integrate(FP3G["seg1"], (x, 0, 2))
f3[3] = f3[2] + sp.integrate(FP3G["seg2"], (x, 2, 3))
f3[4] = f3[2] + sp.integrate(FP3G["seg2"], (x, 2, 4))
same("Q3 values", [f3[-4], f3[4], f3[3]], [3 - 2 * sp.pi, 1, 0])
same("Q3c limit", sp.limit((f3[3] + sp.integrate(FP3G["seg2"], (x, 3, x))) / (x - 3)**2, x, 3), 1)
check("Q3d min at x = -4", float(f3[-4]) < min(0, float(f3[0]), float(f3[3]), float(f3[4])))
FIG3 = graph("exam_bc1_q3", [("sqrt(max(0,4-(x+2)^2))", -4, 0), ("-x", 0, 2), ("2*x-6", 2, 4)], (-4.6, 4.6), (-2.6, 2.6),
             closed=[(-4, 0), (4, 2)], caption=r"The graph of $f'$, the derivative of $f$.", w="11cm", h="6.2cm", ylabel="y", samples=200)
FIG3.tikz = FIG3.tikz.replace(r"\begin{axis}[calcaxes", r"\begin{axis}[calcaxes, xticklabel style={yshift=-3pt}", 1)
FRQ3 = FRQ("The graph of a derivative", (
    r"Let $f$ be a function defined on the closed interval $-4 \le x \le 4$ with $f(0) = 3$. The graph of $f'$, the derivative of $f$, consists of a semicircle and two line segments, as shown in the figure."), [
    Part("a", r"Find the values of $f(-4)$ and $f(4)$.", selfcheck(r"f(-4) = 3 - 2\pi,\ f(4) = 1"),
         r"$f(-4) = f(0) - \int_{-4}^0 f'(x)\,dx = 3 - 2\pi$, since the semicircle above the axis has area $\frac12\pi(2)^2 = 2\pi$. "
         r"$f(4) = f(0) + \int_0^4 f'(x)\,dx = 3 + (-2) + (-1) + 1 = 1$.",
         [(1, r"$f(-4) = 3 - 2\pi$."), (1, r"$f(4) = 1$.")], work="2.6cm", topic="6.7"),
    Part("b", r"Find the $x$-coordinate of each critical point of $f$ in the open interval $-4 < x < 4$. Classify each critical point as the location of a relative minimum, a relative maximum, or neither. Justify your answers.",
         selfcheck(r"x = 0 \text{ (relative maximum)},\ x = 3 \text{ (relative minimum)}"),
         r"$f'(x) = 0$ at $x = 0$ and $x = 3$. At $x = 0$, $f'$ changes from positive to negative, so $f$ has a relative maximum there. "
         r"At $x = 3$, $f'$ changes from negative to positive, so $f$ has a relative minimum there.",
         [(1, r"Relative maximum at $x = 0$, because $f'$ changes from positive to negative."), (1, r"Relative minimum at $x = 3$, because $f'$ changes from negative to positive.")],
         work="2.6cm", topic="5.4"),
    Part("c", r"Find the value of $\displaystyle\lim_{x\to 3} \frac{f(x)}{(x - 3)^2}$, or show that it does not exist. Justify your answer.", num(1),
         r"$f(3) = f(0) + \int_0^3 f'(x)\,dx = 3 + (-2) + (-1) = 0$, and $f$ is differentiable, so it is continuous and $\displaystyle\lim_{x\to 3} f(x) = 0$. "
         r"Also $\displaystyle\lim_{x\to 3} (x - 3)^2 = 0$. By L'Hospital's Rule, "
         r"$\displaystyle\lim_{x\to 3} \frac{f(x)}{(x - 3)^2} = \lim_{x\to 3} \frac{f'(x)}{2(x - 3)} = \lim_{x\to 3} \frac{2x - 6}{2(x - 3)} = 1$, "
         r"since $f'(x) = 2x - 6$ for $2 \le x \le 4$.",
         [(1, r"Shows $\displaystyle\lim_{x\to 3} f(x) = 0$ (from $f(3) = 0$) and $\displaystyle\lim_{x\to 3} (x - 3)^2 = 0$, and uses L'Hospital's Rule."),
          (1, r"Gives the answer, $1$.")], work="3cm", topic="4.7"),
    Part("d", r"Find the absolute minimum value of $f$ on the closed interval $-4 \le x \le 4$. Justify your answer.",
         selfcheck(r"3 - 2\pi"),
         r"The candidates are the endpoints and the critical points: $f(-4) = 3 - 2\pi$, $f(0) = 3$, $f(3) = 0$, and $f(4) = 1$. "
         r"Since $\pi > 3$, $3 - 2\pi < -3 < 0$. Therefore the absolute minimum value of $f$ is $3 - 2\pi$, at $x = -4$.",
         [(1, r"Considers the endpoints and the critical points."), (1, r"Finds $f(3) = 0$ and uses the values from part (a)."),
          (1, r"Gives the answer, $3 - 2\pi$, with the comparison.")], work="2.8cm", topic="5.5"),
], frq_type="Graph of f'", figure=FIG3)

# ---- Question 4: a differential equation in context
A_ = sp.Function("A")(t)
rhs4 = lambda T, Y: (T + 1) * (3 - Y)
sol4 = 3 - 2 * sp.exp(-(t + t**2 / 2))
same("Q4 solution", [sp.simplify(sp.diff(sol4, t) - rhs4(t, sol4)), sol4.subs(t, 0)], [0, 1])
e4 = [(sp.Integer(0), sp.Integer(1))]
for _ in range(2):
    T, Y = e4[-1]
    e4.append((T + sp.Rational(1, 2), Y + sp.Rational(1, 2) * rhs4(T, Y)))
same("Q4a Euler", e4[-1], (1, sp.Rational(11, 4)))
d2_4 = sp.diff(rhs4(t, A_), t).subs(sp.diff(A_, t), rhs4(t, A_))
same("Q4b second derivative", sp.factor(d2_4), sp.factor((3 - A_) * (1 - (t + 1)**2)))
check("Q4b overestimate: Euler beats the solution", sp.Rational(11, 4) > sol4.subs(t, 1))
FRQ4 = FRQ("Algae on a pond", (
    r"Jun studies the algae on a pond. The area covered by algae is modeled by the function $A$, where $A(t)$ is measured in square meters and $t$ is measured in weeks. "
    r"The function $A$ satisfies the differential equation $\dfrac{dA}{dt} = (t + 1)(3 - A)$, with $A(0) = 1$."), [
    Part("a", r"Use Euler's method, starting at $t = 0$, with two steps of equal size, to approximate $A(1)$. Show the computations that lead to your answer.",
         num(sp.Rational(11, 4), display=r"A(1) \approx 2.75"),
         r"The step size is $0.5$. At $(0, 1)$, $\frac{dA}{dt} = 1 \cdot 2 = 2$, so $A(0.5) \approx 1 + 0.5(2) = 2$. "
         r"At $(0.5, 2)$, $\frac{dA}{dt} = 1.5 \cdot 1 = 1.5$, so $A(1) \approx 2 + 0.5(1.5) = 2.75$ square meters.",
         [(1, r"Uses Euler's method with two steps of size $0.5$."), (1, r"Gives the approximation, $A(1) \approx 2.75$.")], work="3cm", topic="7.5"),
    Part("b", r"Find $\dfrac{d^2A}{dt^2}$ in terms of $t$ and $A$. For $0 < t < 1$, is the graph of $A$ concave up or concave down? Is the approximation in part (a) an overestimate or an underestimate of $A(1)$? Give a reason for your answer.",
         selfcheck(r"\tfrac{d^2A}{dt^2} = (3 - A)\left(1 - (t + 1)^2\right);\ \text{concave down, overestimate}"),
         r"$\frac{d^2A}{dt^2} = (3 - A) + (t + 1)\left(-\frac{dA}{dt}\right) = (3 - A) - (t + 1)^2(3 - A) = (3 - A)\left(1 - (t + 1)^2\right)$. "
         r"$A = 3$ is an equilibrium solution and $A(0) = 1 < 3$, so $3 - A > 0$. For $0 < t < 1$, $(t + 1)^2 > 1$, so $\frac{d^2A}{dt^2} < 0$ and the graph of $A$ is concave down. "
         r"Euler's method follows tangent segments, which lie above a concave-down graph, so the approximation is an overestimate.",
         [(1, r"$\frac{d^2A}{dt^2} = (3 - A) - (t + 1)^2(3 - A)$, or an equivalent expression."),
          (1, r"Concave down because $\frac{d^2A}{dt^2} < 0$ for $0 < t < 1$, so the approximation is an overestimate.")], work="3.4cm", topic="7.5"),
    Part("c", r"Find $A(t)$, the particular solution to the differential equation with the initial condition $A(0) = 1$.",
         expr("3 - 2*exp(-(t + t**2/2))", var="t", display=r"A(t) = 3 - 2e^{-(t + t^2/2)}"),
         r"Separate the variables: $\frac{dA}{3 - A} = (t + 1)\,dt$. Integrate: $-\ln|3 - A| = \frac{t^2}{2} + t + C$. "
         r"With $t = 0$, $A = 1$: $-\ln 2 = C$. Then $\ln|3 - A| = \ln 2 - t - \frac{t^2}{2}$, so $|3 - A| = 2e^{-(t + t^2/2)}$. Since $A(0) = 1 < 3$, $3 - A > 0$. "
         r"Therefore $A(t) = 3 - 2e^{-(t + t^2/2)}$.",
         [(1, r"Separates the variables."), (1, r"Antiderivatives: $-\ln|3 - A|$ and $\frac{t^2}{2} + t$."), (1, r"Includes a constant of integration."),
          (1, r"Uses the initial condition $A(0) = 1$."), (1, r"Solves for $A$: $A(t) = 3 - 2e^{-(t + t^2/2)}$.")], work="4cm", topic="7.7"),
], frq_type="Differential equation")

# ---- Question 5: parametric motion
XP5, YP5 = 2 * t, t**2 - 1
same("Q5 speed is t^2 + 1", sp.simplify(XP5**2 + YP5**2 - (t**2 + 1)**2), 0)
same("Q5a", [sp.sqrt(XP5**2 + YP5**2).subs(t, 2), (YP5 / XP5).subs(t, 2)], [5, sp.Rational(3, 4)])
pos5 = lambda T: (1 + sp.integrate(XP5, (t, 0, T)), -2 + sp.integrate(YP5, (t, 0, T)))
same("Q5b", pos5(3), (10, 4))
same("Q5c", sp.integrate(t**2 + 1, (t, 0, 3)), 12)
same("Q5d horizontal tangent", [sp.solve(YP5, t), XP5.subs(t, 1), pos5(1)], [[-1, 1], 2, (2, -sp.Rational(8, 3))])
FRQ5 = FRQ("Parametric motion", (
    r"A particle moves in the $xy$-plane so that its position at time $t \ge 0$ is $(x(t), y(t))$, where $\dfrac{dx}{dt} = 2t$ and $\dfrac{dy}{dt} = t^2 - 1$. "
    r"At time $t = 0$, the particle is at the point $(1, -2)$."), [
    Part("a", r"Find the speed of the particle at time $t = 2$. Find the slope of the line tangent to the path of the particle at time $t = 2$.",
         selfcheck(r"\text{speed } 5,\ \text{slope } \tfrac34"),
         r"At $t = 2$, $\frac{dx}{dt} = 4$ and $\frac{dy}{dt} = 3$. Speed $= \sqrt{4^2 + 3^2} = 5$. Slope $= \frac{dy/dt}{dx/dt} = \frac34$.",
         [(1, r"Speed $= 5$."), (1, r"Slope $= \frac34$.")], work="2.4cm", topic="9.6"),
    Part("b", r"Find the position of the particle at time $t = 3$.", selfcheck(r"(10, 4)"),
         r"$x(3) = 1 + \int_0^3 2t\,dt = 1 + 9 = 10$ and $y(3) = -2 + \int_0^3 \left(t^2 - 1\right) dt = -2 + (9 - 3) = 4$. The particle is at $(10, 4)$.",
         [(1, r"Uses the initial point with a definite integral for each coordinate."), (1, r"Gives the position, $(10, 4)$.")], work="2.6cm", topic="9.5"),
    Part("c", r"Find the total distance traveled by the particle from time $t = 0$ to time $t = 3$.", num(12),
         r"Total distance traveled $= \int_0^3 \sqrt{(2t)^2 + \left(t^2 - 1\right)^2}\,dt = \int_0^3 \sqrt{t^4 + 2t^2 + 1}\,dt = \int_0^3 \left(t^2 + 1\right) dt = 9 + 3 = 12$.",
         [(1, r"Writes $\int_0^3 \sqrt{(2t)^2 + \left(t^2 - 1\right)^2}\,dt$."), (1, r"Simplifies the integrand to $t^2 + 1$."), (1, r"Gives the answer, $12$.")],
         work="3cm", topic="9.6"),
    Part("d", r"For $t > 0$, find the position of the particle at each time when the line tangent to its path is horizontal.",
         selfcheck(r"\left(2, -\tfrac83\right)"),
         r"The tangent line is horizontal when $\frac{dy}{dt} = 0$ and $\frac{dx}{dt} \ne 0$. For $t > 0$, $t^2 - 1 = 0$ only at $t = 1$, where $\frac{dx}{dt} = 2 \ne 0$. "
         r"$x(1) = 1 + \int_0^1 2t\,dt = 2$ and $y(1) = -2 + \int_0^1 \left(t^2 - 1\right) dt = -2 - \frac23 = -\frac83$. The particle is at $\left(2, -\frac83\right)$.",
         [(1, r"Finds $t = 1$ from $\frac{dy}{dt} = 0$, with $\frac{dx}{dt} \ne 0$."), (1, r"Gives the position, $\left(2, -\frac83\right)$.")], work="2.6cm", topic="9.1"),
], frq_type="Parametric / vector motion")

# ---- Question 6: a power series
f6 = sp.log(1 + x / 3)
ser6 = sp.series(f6, x, 0, 6).removeO()
same("Q6 the series", [ser6.coeff(x, k) for k in range(1, 6)], [(-1)**(k + 1) / (sp.Integer(k) * 3**k) for k in range(1, 6)])
same("Q6a ratio", sp.limit(((nI * 3**nI) / ((nI + 1) * 3**(nI + 1))), nI, sp.oo), sp.Rational(1, 3))
check("Q6a x = 3 converges, x = -3 diverges", converges((-1)**(nI + 1) / nI, nI) is True and converges(1 / nI, nI) is False)
same("Q6b f'", [sp.diff(ser6, x).coeff(x, k) for k in range(4)], [sp.Rational(1, 3), -sp.Rational(1, 9), sp.Rational(1, 27), -sp.Rational(1, 81)])
same("Q6c", [ser6.subs(x, 1) - (ser6.coeff(x, 3) + ser6.coeff(x, 4) + ser6.coeff(x, 5)), sp.Rational(1, 81)], [sp.Rational(5, 18), sp.Rational(1, 81)])
check("Q6c error really below 1/50", abs(float(f6.subs(x, 1)) - 5 / 18) < 1 / 81 < 1 / 50)
g6 = sp.integrate(ser6, (x, 0, x))
same("Q6d", [g6.coeff(x, k) for k in (2, 3, 4)], [sp.Rational(1, 6), -sp.Rational(1, 54), sp.Rational(1, 324)])
FRQ6 = FRQ("A power series", (
    r"The function $f$ is defined by the power series $f(x) = \displaystyle\sum_{n=1}^\infty \frac{(-1)^{n+1} x^n}{n \cdot 3^n} = \frac{x}{3} - \frac{x^2}{2 \cdot 9} + \frac{x^3}{3 \cdot 27} - \cdots + \frac{(-1)^{n+1} x^n}{n \cdot 3^n} + \cdots$ "
    r"for all real numbers $x$ for which the series converges."), [
    Part("a", r"Find the interval of convergence of the power series for $f$. Justify your answer.", selfcheck(r"-3 < x \le 3"),
         r"Ratio test: $\displaystyle\lim_{n\to\infty} \left|\frac{x^{n+1}}{(n + 1)3^{n+1}} \cdot \frac{n \cdot 3^n}{x^n}\right| = \lim_{n\to\infty} \frac{n}{n + 1} \cdot \frac{|x|}{3} = \frac{|x|}{3}$. "
         r"The series converges when $\frac{|x|}{3} < 1$, so for $-3 < x < 3$. "
         r"At $x = 3$ the series is $\sum \frac{(-1)^{n+1}}{n}$, which converges by the alternating series test, since $\frac1n$ decreases to $0$. "
         r"At $x = -3$ the series is $\sum \frac{(-1)^{n+1}(-1)^n}{n} = -\sum \frac1n$, the harmonic series, which diverges. Therefore the interval of convergence is $-3 < x \le 3$.",
         [(1, r"Sets up the ratio test and finds the limit $\frac{|x|}{3}$."), (1, r"Identifies the radius of convergence, $3$."),
          (1, r"Analyzes both endpoints and gives the interval $-3 < x \le 3$.")], work="4.4cm", topic="10.13"),
    Part("b", r"Find the first four nonzero terms and the general term of the Maclaurin series for $f'(x)$.",
         selfcheck(r"\tfrac13 - \tfrac{x}{9} + \tfrac{x^2}{27} - \tfrac{x^3}{81} + \cdots + \tfrac{(-1)^{n+1} x^{n-1}}{3^n} + \cdots"),
         r"Differentiate term by term: $f'(x) = \frac13 - \frac{x}{9} + \frac{x^2}{27} - \frac{x^3}{81} + \cdots + \frac{(-1)^{n+1} x^{n-1}}{3^n} + \cdots$.",
         [(1, r"The first four nonzero terms."), (1, r"The general term.")], work="2.6cm", topic="10.15"),
    Part("c", r"Use the first two nonzero terms of the series for $f$ to approximate $f(1)$. Show that this approximation differs from $f(1)$ by less than $\frac{1}{50}$.",
         num(sp.Rational(5, 18), display=r"f(1) \approx \tfrac{5}{18}"),
         r"$f(1) \approx \frac13 - \frac{1}{18} = \frac{5}{18}$. The series for $f(1)$, $\sum \frac{(-1)^{n+1}}{n \cdot 3^n}$, alternates, and its terms decrease in absolute value to $0$. "
         r"By the alternating series error bound, the error is at most the absolute value of the first omitted term: $\left|f(1) - \frac{5}{18}\right| \le \frac{1}{3 \cdot 27} = \frac{1}{81} < \frac{1}{50}$.",
         [(1, r"Gives the approximation $\frac{5}{18}$."), (1, r"Uses the alternating series error bound with the term $\frac{1}{81}$ and concludes the error is less than $\frac{1}{50}$.")],
         work="3cm", topic="10.10"),
    Part("d", r"Let $g(x) = \displaystyle\int_0^x f(t)\,dt$. Find the first three nonzero terms of the Maclaurin series for $g$.",
         selfcheck(r"\tfrac{x^2}{6} - \tfrac{x^3}{54} + \tfrac{x^4}{324}"),
         r"Integrate term by term from $0$ to $x$: $g(x) = \frac{x^2}{2 \cdot 3} - \frac{x^3}{3 \cdot 18} + \frac{x^4}{4 \cdot 81} - \cdots = \frac{x^2}{6} - \frac{x^3}{54} + \frac{x^4}{324} - \cdots$.",
         [(1, r"Two correct terms."), (1, r"All three terms correct.")], work="2.6cm", topic="10.15"),
], frq_type="Taylor series")


EXAM = Exam(
    slug="bc1", title="AP Calculus BC Practice Exam 1", course="BC",
    mcq_a=PART_A, mcq_b=PART_B, frq_a=[FRQ1, FRQ2], frq_b=[FRQ3, FRQ4, FRQ5, FRQ6],
    members_only=False,
    cutoffs=((5, 63), (4, 51), (3, 39), (2, 30)),
)
