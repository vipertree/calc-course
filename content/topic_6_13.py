"""Topic 6.13 (BC only): Evaluating improper integrals.

CED: LIM-6.A (LIM-6.A.1-LIM-6.A.3): an integral over an infinite interval, or of a function that is unbounded at a point
of the interval, is a limit of definite integrals; it converges if the limit exists (a number) and diverges otherwise;
limit notation is required. p-integrals: integral_1^oo x^(-p) dx converges exactly when p > 1. Lesson example: the
hidden asymptote in integral_{-1}^{1} x^(-2) dx. Worked examples: e^(-2x) on [0, oo), x/(x^2 + 1) on [1, oo).
"""
import sympy as sp

from calclib import (VideoExample, MCQ, BigIdea, Check, Formula, Item, Section, Text, Topic, Variants, Video, num, same, selfcheck)

x = sp.symbols("x", positive=True)
oo = sp.oo

same("lesson", [sp.integrate(x**-2, (x, 1, oo)), sp.integrate(1 / x, (x, 1, oo)), sp.integrate(x**sp.Rational(-1, 2), (x, 0, 1)), sp.integrate(x**-2, (x, 0, 1))], [1, oo, 2, oo])
same("ex", [sp.integrate(sp.exp(-2 * x), (x, 0, oo)), sp.integrate(x / (x**2 + 1), (x, 1, oo))], [sp.Rational(1, 2), oo])


def item(f, a, b, how, work="2.4cm"):
    v = sp.integrate(f, (x, a, b))
    ans = num(v) if v.is_finite else selfcheck(r"\text{diverges}")
    verdict = rf"converges to ${sp.latex(v)}$" if v.is_finite else r"the limit is infinite, so it diverges"
    return Item(rf"Evaluate $\displaystyle\int_{{{sp.latex(a)}}}^{{{sp.latex(b)}}} {sp.latex(f)}\,dx$, or show that it diverges.", ans, how + rf" The integral {verdict}.", work=work)


NOTES = [
    Video("s6_13.py::Lesson", "Improper integrals", 5),

    Section("Improper integrals are limits"),
    Formula("Improper integrals", (
        r"\[ \int_a^\infty f(x)\,dx = \lim_{b\to\infty} \int_a^b f(x)\,dx. \] If $f$ is unbounded at $x = a$: $\displaystyle\int_a^c f(x)\,dx = \lim_{t\to a^+} \int_t^c f(x)\,dx$. "
        r"If the limit is a number, the integral \blank{converges}; if it is infinite or doesn't exist, the integral \blank{diverges}.")),
    Text(r"\textbf{Write the limit on every line.} Never plug in $\infty$ directly."),
    Text(r"$\int_1^\infty \frac{1}{x^2}\,dx = \lim_{b\to\infty}\left(1 - \frac1b\right) = 1$ converges; $\int_1^\infty \frac1x\,dx = \lim_{b\to\infty} \ln b = \infty$ diverges."),
    Formula("$p$-integrals", (r"$\displaystyle\int_1^\infty \frac{1}{x^p}\,dx$ converges if $p \blank{> 1}$ and diverges if $p \le 1$.")),
    Text(r"\textbf{Check inside the interval.} If $f$ is unbounded at a point inside $[a, b]$, split there. The Fundamental Theorem needs $f$ continuous on the whole interval."),
    VideoExample('A hidden asymptote', work="3cm"),
    BigIdea(r"Every improper integral is a limit: replace $\infty$ or the asymptote with a variable, integrate, take the limit. A number converges; infinite diverges."),
    Check(r"Evaluate $\displaystyle\int_1^\infty \frac{1}{x^3}\,dx$.", num(sp.Rational(1, 2)), r"$\lim_{b\to\infty}\left[-\frac{1}{2x^2}\right]_1^b = \frac12$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    item(x**-4, 1, oo, r"$\lim_{b\to\infty}\left[-\frac{1}{3x^3}\right]_1^b$."),
    item(1 / sp.sqrt(x), 1, oo, r"$\lim_{b\to\infty}\left[2\sqrt x\right]_1^b$."),
    item(sp.exp(-x), 0, oo, r"$\lim_{b\to\infty}\left[-e^{-x}\right]_0^b$."),
    item(x**sp.Rational(-1, 3), 0, 8, r"$\lim_{t\to0^+}\left[\frac32x^{2/3}\right]_t^8$."),
    item(1 / x, 0, 1, r"$\lim_{t\to0^+}\left[\ln x\right]_t^1$."),
    item(1 / (1 + x**2), 0, oo, r"$\lim_{b\to\infty}\left[\arctan x\right]_0^b$."),
    item(x * sp.exp(-x**2), 0, oo, r"$u = x^2$: $\lim_{b\to\infty}\left[-\frac12e^{-x^2}\right]_0^b$."),
    item(1 / (x * sp.log(x)**2), sp.E, oo, r"$u = \ln x$: $\lim_{b\to\infty}\left[-\frac{1}{\ln x}\right]_e^b$."),
    Item(r"For which values of $p$ does $\displaystyle\int_1^\infty \frac{1}{x^p}\,dx$ converge?", selfcheck(r"p > 1"), r"The $p$-integral rule.", work="1cm"),
    Item(r"Evaluate $\displaystyle\int_0^2 \frac{1}{(x - 1)^2}\,dx$, or show that it diverges.", selfcheck(r"\text{diverges}"),
         r"Unbounded at $x = 1$, inside $[0, 2]$. $\int_1^2 (x - 1)^{-2}\,dx = \lim_{t\to1^+}\left[-\frac{1}{x - 1}\right]_t^2 = \lim_{t\to1^+}\left(-1 + \frac{1}{t - 1}\right) = \infty$: diverges.", work="2.4cm"),
]
same("p", [sp.integrate((x - 1)**-2, (x, 1, 2))], [oo])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(item(x**-2, 2, oo, "", "1.6cm"), item(x**-3, 1, oo, "", "1.6cm"), item(x**sp.Rational(-3, 2), 1, oo, "", "1.6cm")),
    Variants(item(sp.exp(-3 * x), 0, oo, "", "1.6cm"), item(sp.exp(-x / 2), 0, oo, "", "1.6cm"), item(sp.exp(-x), 1, oo, "", "1.6cm")),
    Variants(item(x**sp.Rational(-1, 2), 0, 4, "", "1.6cm"), item(x**sp.Rational(-2, 3), 0, 1, "", "1.6cm"), item(1 / sp.sqrt(x), 0, 9, "", "1.6cm")),
    Variants(
        MCQ(r"Which integral converges?", [r"$\int_1^\infty \frac{1}{\sqrt x}\,dx$", r"$\int_1^\infty \frac{1}{x}\,dx$", r"$\int_1^\infty \frac{1}{x^{1.01}}\,dx$", r"$\int_1^\infty \frac{1}{x^{0.99}}\,dx$"], "C", r"$p = 1.01 > 1$."),
        MCQ(r"Which integral diverges?", [r"$\int_1^\infty x^{-2}\,dx$", r"$\int_1^\infty x^{-1/2}\,dx$", r"$\int_0^\infty e^{-x}\,dx$", r"$\int_0^1 x^{-1/2}\,dx$"], "B", r"$p = \frac12 \le 1$."),
        MCQ(r"$\int_0^1 \frac{1}{x^p}\,dx$ converges when", [r"$p > 1$", r"$p \ge 1$", r"$p = 1$", r"$p < 1$"], "D", r"Near $0$ the rule flips: $\left[\frac{x^{1-p}}{1 - p}\right]_t^1$ has a finite limit when $1 - p > 0$."),
    ),
    Variants(
        MCQ(r"$\displaystyle\int_{-1}^{2} \frac{1}{x^3}\,dx$", [r"$= \frac38$", r"$= -\frac38$", r"diverges", r"$= 0$"], "C", r"Unbounded at $x = 0$, inside $[-1, 2]$; $\int_0^2 x^{-3}\,dx$ diverges.", why_not={"A": "plugged in across the asymptote"}),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$\displaystyle\int_0^\infty \frac{2}{1 + x^2}\,dx = $", [r"$\pi$", r"$\frac\pi2$", r"$2$", r"divergent"], "A", r"$\lim_{b\to\infty} 2\arctan b = 2 \cdot \frac\pi2$."),
    MCQ(r"$\displaystyle\int_1^\infty x e^{-x^2}\,dx = $", [r"$\frac{1}{e}$", r"$\frac{1}{2e}$", r"$\frac{e}{2}$", r"divergent"], "B", r"$\lim_{b\to\infty}\left[-\frac12e^{-x^2}\right]_1^b = \frac{1}{2e}$."),
    MCQ(r"$\displaystyle\int_0^4 \frac{dx}{\sqrt{4 - x}} = $", [r"$2$", r"divergent", r"$8$", r"$4$"], "D", r"$\lim_{t\to4^-}\left[-2\sqrt{4 - x}\right]_0^t = 0 + 4 = 4$."),
    MCQ(r"For what $k$ does $\displaystyle\int_1^\infty \frac{1}{x^{k - 2}}\,dx$ converge?", [r"$k > 1$", r"$k > 2$", r"$k > 3$", r"$k < 3$"], "C", r"$p = k - 2 > 1$."),
]
same("m", [sp.integrate(2 / (1 + x**2), (x, 0, oo)), sp.integrate(x * sp.exp(-x**2), (x, 1, oo)), sp.integrate(1 / sp.sqrt(4 - x), (x, 0, 4))], [sp.pi, sp.exp(-1) / 2, 4])

FRQS = []

TOPIC = Topic(
    number="6.13", title="Evaluating Improper Integrals",
    unit="Unit 6: Integration and Accumulation of Change", ced=["LIM-6.A", "LIM-6.A.1", "LIM-6.A.2", "LIM-6.A.3"],
    goals=r"Evaluate improper integrals as limits, deciding whether they converge or diverge.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
