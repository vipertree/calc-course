"""Topic 10.4 (BC): Integral test for convergence.

CED: LIM-7.A (LIM-7.A.6): if f is positive, continuous, and decreasing for x >= N and a_n = f(n), then sum a_n and the
integral of f from N to infinity both converge or both diverge; the integral's value is not the sum. Lesson example:
n/(n^2 + 1) diverges. Worked examples: 1/n^2 converges (sum pi^2/6, integral 1); n e^(-n^2) converges; 1/(n ln n)
diverges.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)

x = sp.symbols("x", positive=True)
Ii = lambda f, a: sp.integrate(f, (x, a, sp.oo))

same("lesson", [Ii(x / (x**2 + 1), 1)], [sp.oo])
same("ex", [Ii(1 / x**2, 1), sp.simplify(Ii(x * sp.exp(-x**2), 1)), Ii(1 / (x * sp.log(x)), 2)], [1, 1 / (2 * sp.E), sp.oo])

NOTES = [
    Video("s10_4.py::Lesson", "The integral test", 4),

    Section("Rectangles and a curve"),
    Text(r"Rectangles of width $1$ and heights $f(1), f(2), \ldots$ have total area $\sum f(n)$. Shifted right they fit under $y = f(x)$; shifted left they cover it. So the series and the improper integral are both finite or both infinite."),
    Formula("Integral test", (r"If $f$ is \blank{positive}, \blank{continuous}, and \blank{decreasing} for $x \ge N$, and $a_n = f(n)$, then \[ \sum_{n=N}^\infty a_n \quad \text{and} \quad \int_N^\infty f(x)\,dx \] both converge or both diverge.")),
    Text(r"State all three conditions when you use the test. The test decides convergence; it does not give the sum: $\int_1^\infty \frac{dx}{x^2} = 1$, but $\sum \frac{1}{n^2} = \frac{\pi^2}{6}$."),
    VideoExample('Using the integral test', work="4cm"),
    BigIdea(r"For positive, continuous, decreasing $f$, $\sum f(n)$ and $\int f(x)\,dx$ converge or diverge together."),
    Check(r"Does $\sum \frac{1}{n^3}$ converge? Use the integral test.", selfcheck(r"\text{converges}"), r"$\int_1^\infty x^{-3}\,dx = \frac12$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Use the integral test on $\sum_{n=1}^\infty \frac{1}{n^{3/2}}$.", selfcheck(r"\text{converges}"), r"$\int_1^\infty x^{-3/2}\,dx = 2$.", work="1.6cm"),
    Item(r"Use the integral test on $\sum_{n=1}^\infty \frac{1}{2n + 1}$.", selfcheck(r"\text{diverges}"), r"$\int_1^\infty \frac{dx}{2x + 1} = \lim \frac12\ln(2x + 1)\Big|_1^b = \infty$.", work="1.8cm"),
    Item(r"Use the integral test on $\sum_{n=1}^\infty \frac{1}{n^2 + 1}$.", selfcheck(r"\text{converges}"), r"$\int_1^\infty \frac{dx}{x^2 + 1} = \frac\pi2 - \frac\pi4 = \frac\pi4$.", work="1.8cm"),
    Item(r"Use the integral test on $\sum_{n=1}^\infty e^{-n}$.", selfcheck(r"\text{converges}"), r"$\int_1^\infty e^{-x}\,dx = \frac1e$ (also geometric).", work="1.4cm"),
    Item(r"Use the integral test on $\sum_{n=1}^\infty \frac{\ln n}{n}$.", selfcheck(r"\text{diverges}"), r"$\int_1^\infty \frac{\ln x}{x}\,dx = \lim \frac{(\ln x)^2}{2}\Big|_1^b = \infty$ (decreasing for $x \ge e$).", work="2cm"),
    Item(r"Use the integral test on $\sum_{n=2}^\infty \frac{1}{n(\ln n)^2}$.", selfcheck(r"\text{converges}"), r"$\int_2^\infty \frac{dx}{x(\ln x)^2} = \lim\left[-\frac{1}{\ln x}\right]_2^b = \frac{1}{\ln 2}$.", work="2cm"),
    Item(r"Find the value of $\int_1^\infty \frac{dx}{x^2 + 1}$. Is it the sum of $\sum_{n=1}^\infty \frac{1}{n^2 + 1}$?", selfcheck(r"\tfrac\pi4;\ \text{no}"), r"$\frac\pi4$; the test only shows the series converges.", work="1.6cm"),
    Item(r"Why can't the integral test be used on $\sum \frac{\sin^2 n}{n^2}$?", selfcheck(r"f(x) = \frac{\sin^2 x}{x^2} \text{ is not decreasing}"), r"The function oscillates, so it isn't decreasing (use comparison instead, 10.6).", work="1.4cm"),
]
same("p", [Ii(x**sp.Rational(-3, 2), 1), Ii(1 / (x**2 + 1), 1), sp.simplify(Ii(1 / (x * sp.log(x)**2), 2))], [2, sp.pi / 4, 1 / sp.log(2)])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"Which is NOT a condition of the integral test for $\sum f(n)$?", [r"$f$ is positive", r"$f$ is continuous", r"$f$ is decreasing", r"$f$ is differentiable at every integer with $f'(n) = 0$"], "D", r"Positive, continuous, decreasing."),
    ),
    Variants(
        Item(r"Use the integral test on $\sum \frac{1}{n^4}$.", selfcheck(r"\text{converges}"), r"$\int_1^\infty x^{-4}\,dx = \frac13$.", work="1.4cm"),
        Item(r"Use the integral test on $\sum \frac{1}{\sqrt[3]{n}}$.", selfcheck(r"\text{diverges}"), r"$\int_1^\infty x^{-1/3}\,dx = \infty$.", work="1.4cm"),
    ),
    Variants(
        Item(r"Use the integral test on $\sum \frac{1}{n + 4}$.", selfcheck(r"\text{diverges}"), r"$\int_1^\infty \frac{dx}{x + 4} = \infty$.", work="1.4cm"),
        Item(r"Use the integral test on $\sum \frac{2}{(n + 1)^2}$.", selfcheck(r"\text{converges}"), r"$\int_1^\infty \frac{2\,dx}{(x + 1)^2} = 1$.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"$\int_1^\infty f(x)\,dx = 3$ and $f$ is positive, continuous, and decreasing. Then $\sum_{n=1}^\infty f(n)$", [r"equals $3$", r"converges", r"diverges", r"equals $3 + f(1)$"], "B", r"Same behavior; the value differs.", why_not={"A": "the integral's value is not the sum"}),
    ),
    Variants(
        Item(r"Use the integral test on $\sum n e^{-n}$.", selfcheck(r"\text{converges}"), r"$\int_1^\infty xe^{-x}\,dx = \frac2e$ (decreasing for $x \ge 1$).", work="1.6cm"),
        Item(r"Use the integral test on $\sum \frac{n}{n^2 + 4}$.", selfcheck(r"\text{diverges}"), r"$\int \frac{x}{x^2 + 4}\,dx = \frac12\ln(x^2 + 4) \to \infty$.", work="1.6cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"Which improper integral decides the convergence of $\sum_{n=1}^\infty \frac{n}{e^{n^2}}$ by the integral test?", [r"$\int_1^\infty \frac{x}{e^x}\,dx$", r"$\int_1^\infty xe^{-x^2}\,dx$", r"$\int_0^1 xe^{-x^2}\,dx$", r"$\int_1^\infty e^{-x^2}\,dx$"], "B", r"$f(x) = xe^{-x^2}$."),
    MCQ(r"$\int_2^\infty \frac{dx}{x(\ln x)^p}$ converges exactly when", [r"$p > 1$", r"$p \ge 1$", r"$p < 1$", r"$p > 0$"], "A", r"$u = \ln x$ gives $\int_{\ln 2}^\infty u^{-p}\,du$."),
    MCQ(r"Using the integral test, $\sum_{n=1}^\infty \frac{1}{n^2 + 2n + 2}$", [r"diverges, since $\int_1^\infty \frac{dx}{(x + 1)^2 + 1} = \infty$", r"converges to $\frac\pi2 - \arctan 2$", r"diverges by the $n$th term test", r"converges, since $\int_1^\infty \frac{dx}{(x + 1)^2 + 1} = \frac\pi2 - \arctan 2$"], "D",
        r"The integral is finite, so the series converges; the integral's value is not the sum.", why_not={"B": "the integral's value is not the sum"}),
    MCQ(r"For which series does the integral test apply?", [r"$\sum \frac{(-1)^n}{n}$", r"$\sum \frac{1}{n^2}$", r"$\sum \frac{\cos^2 n}{n^2}$", r"$\sum (-2)^{-n}$"], "B", r"Needs a positive, continuous, decreasing $f$."),
]
same("m", [sp.simplify(Ii(1 / ((x + 1)**2 + 1), 1))], [sp.pi / 2 - sp.atan(2)])

FRQS = []

TOPIC = Topic(
    number="10.4", title="Integral Test for Convergence",
    unit="Unit 10: Infinite Sequences and Series", ced=["LIM-7.A", "LIM-7.A.6"],
    goals=r"Check the conditions of the integral test and use an improper integral to decide convergence.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
