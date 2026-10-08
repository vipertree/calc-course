"""Topic 10.5 (BC): Harmonic series and p-series.

CED: LIM-7.A (LIM-7.A.7): the harmonic series diverges (grouping argument); sum 1/n^p converges iff p > 1 (integral
test). Lesson example: classify 1/n^1.01, 1/sqrt n, 1/n^pi, n^-0.99. Worked examples: 3/n^4; n^2/n^3.5; 1/cbrt(n^2).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)

x = sp.symbols("x", positive=True)
p_int = lambda p: sp.integrate(x**(-p), (x, 1, sp.oo))
same("p-series", [p_int(sp.Rational(3, 2)), p_int(1), p_int(sp.Rational(1, 2)), p_int(4)], [2, sp.oo, sp.oo, sp.Rational(1, 3)])

NOTES = [
    Video("s10_5.py::Lesson", "Harmonic and p-series", 3),

    Section("The harmonic series"),
    Text(r"$1 + \frac12 + \left(\frac13 + \frac14\right) + \left(\frac15 + \cdots + \frac18\right) + \cdots$: each group is at least $\frac12$, so the partial sums grow without bound. The harmonic series \textbf{diverges}, even though its terms go to $0$."),
    Formula("$p$-series", (r"\[ \sum_{n=1}^\infty \frac{1}{n^p} \ \text{ converges if } \blank{p > 1} \ \text{ and diverges if } \blank{p \le 1}. \] (By the integral test: $\int_1^\infty x^{-p}\,dx$ is finite exactly when $p > 1$.)")),
    VideoExample('Classifying p-series', work="3cm"),
    Text(r"\textbf{Read off $p$.} Rewrite roots and negative exponents: $\frac{1}{\sqrt n} = \frac{1}{n^{1/2}}$, $n^{-0.99} = \frac{1}{n^{0.99}}$. Constant multiples don't change convergence."),
    BigIdea(r"$\sum \frac{1}{n^p}$: $p > 1$ converges; $p \le 1$ (including the harmonic series) diverges."),
    Check(r"Does $\sum \frac{1}{n^{1/3}}$ converge?", selfcheck(r"\text{diverges}"), r"$p = \frac13 \le 1$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Does $\sum \frac{1}{n^5}$ converge?", selfcheck(r"\text{converges}"), r"$p = 5 > 1$.", work="0.8cm"),
    Item(r"Does $\sum \frac{1}{n^{0.5}}$ converge?", selfcheck(r"\text{diverges}"), r"$p = 0.5$.", work="0.8cm"),
    Item(r"Does $\sum \frac{4}{\sqrt{n^3}}$ converge?", selfcheck(r"\text{converges}"), r"$\frac{4}{n^{3/2}}$, $p = \frac32$.", work="1cm"),
    Item(r"Does $\sum \frac{\sqrt n}{n^2}$ converge?", selfcheck(r"\text{converges}"), r"$\frac{1}{n^{3/2}}$.", work="1cm"),
    Item(r"Does $\sum \frac{n}{n^{1.5}}$ converge?", selfcheck(r"\text{diverges}"), r"$\frac{1}{n^{0.5}}$.", work="1cm"),
    Item(r"Does $\sum \frac{1}{n^{e}}$ converge?", selfcheck(r"\text{converges}"), r"$p = e > 1$.", work="0.8cm"),
    Item(r"Does $\sum \frac{1}{5n}$ converge?", selfcheck(r"\text{diverges}"), r"$\frac15$ times the harmonic series.", work="0.8cm"),
    Item(r"For which values of $p$ does $\sum \frac{1}{n^{2p - 1}}$ converge?", selfcheck(r"p > 1"), r"$2p - 1 > 1$.", work="1cm"),
    Item(r"For which values of $k$ does $\sum n^{k}$ converge?", selfcheck(r"k < -1"), r"$n^k = \frac{1}{n^{-k}}$; need $-k > 1$.", work="1cm"),
]

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"Which $p$-series converges?", [r"$\sum \frac{1}{n}$", r"$\sum \frac{1}{\sqrt n}$", r"$\sum \frac{1}{n^{1.1}}$", r"$\sum \frac{1}{n^{0.9}}$"], "C", r"$p = 1.1 > 1$."),
        MCQ(r"Which $p$-series diverges?", [r"$\sum \frac{1}{n^2}$", r"$\sum \frac{1}{n\sqrt n}$", r"$\sum n^{-1.5}$", r"$\sum \frac{1}{\sqrt[4]{n}}$"], "D", r"$p = \frac14$."),
    ),
    Variants(
        Item(r"Does $\sum \frac{n^3}{n^5}$ converge?", selfcheck(r"\text{converges}"), r"$\frac{1}{n^2}$.", work="1cm"),
        Item(r"Does $\sum \frac{n^2}{n^3}$ converge?", selfcheck(r"\text{diverges}"), r"$\frac1n$.", work="1cm"),
    ),
    Variants(
        MCQ(r"The harmonic series $\sum \frac1n$", [r"converges because $\frac1n \to 0$", r"diverges", r"converges to $\ln 2$", r"converges to $1$"], "B", r"Grouping or the integral test.", why_not={"A": "terms going to $0$ is not enough"}),
    ),
    Variants(
        Item(r"For which $p$ does $\sum \frac{1}{n^{p + 2}}$ converge?", selfcheck(r"p > -1"), r"$p + 2 > 1$.", work="1cm"),
        Item(r"For which $p$ does $\sum \frac{1}{n^{3p}}$ converge?", selfcheck(r"p > \tfrac13"), r"$3p > 1$.", work="1cm"),
    ),
    Variants(
        Item(r"Does $\sum \frac{7}{n^{\pi/3}}$ converge?", selfcheck(r"\text{converges}"), r"$\frac\pi3 > 1$.", work="1cm"),
        Item(r"Does $\sum \frac{2}{n^{\ln 2}}$ converge?", selfcheck(r"\text{diverges}"), r"$\ln 2 \approx 0.69 < 1$.", work="1cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"Which of the following converge? I. $\sum \frac{1}{n^{3/2}}$ \ II. $\sum \frac{1}{n^{2/3}}$ \ III. $\sum \frac{1}{n^{1.001}}$", [r"I only", r"I and III only", r"II only", r"I, II and III"], "B", r"$p > 1$ for I and III."),
    MCQ(r"$\sum_{n=1}^\infty n^{-p}$ diverges for", [r"$p > 1$", r"$p = 2$", r"$p \le 1$", r"$p \ge 1$"], "C", r"The $p$-series test.", why_not={"D": "$p = 1$ diverges but $p > 1$ converges"}),
    MCQ(r"$\sum_{n=1}^\infty \frac{n^2}{n^{k}}$ converges exactly when", [r"$k > 1$", r"$k > 2$", r"$k > 0$", r"$k > 3$"], "D", r"$\frac{1}{n^{k - 2}}$: need $k - 2 > 1$."),
    MCQ(r"Which statement about $\sum \frac1n$ and $\sum \frac{1}{n^2}$ is true?", [r"both converge", r"both diverge", r"the first diverges and the second converges", r"the first converges and the second diverges"], "C", r"$p = 1$ and $p = 2$."),
]

FRQS = []

TOPIC = Topic(
    number="10.5", title="Harmonic Series and p-Series",
    unit="Unit 10: Infinite Sequences and Series", ced=["LIM-7.A", "LIM-7.A.7"],
    goals=r"Know that the harmonic series diverges and decide when a $p$-series converges.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
