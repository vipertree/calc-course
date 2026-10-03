"""Topic 10.6 (BC): Comparison tests for convergence.

CED: LIM-7.A (LIM-7.A.8, LIM-7.A.9): direct comparison (0 <= a_n <= b_n: sum b_n converges => sum a_n converges; sum a_n
diverges => sum b_n diverges) and limit comparison (lim a_n/b_n = c, 0 < c < infinity: same behavior). Lesson example:
1/(n^2 + 3) by direct comparison; (2n + 1)/(n^3 - n + 5) by limit comparison with 1/n^2. Worked examples: (ln n)/n
diverges; sin^2 n/n^2 converges; 1/(2^n - 1) by limit comparison with 1/2^n.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)

n = sp.symbols("n", positive=True)
L = lambda a: sp.limit(a, n, sp.oo)

same("lesson", [L((2 * n + 1) / (n**3 - n + 5) / (1 / n**2))], [2])
same("ex", [L((1 / (2**n - 1)) / (1 / 2**n))], [1])

NOTES = [
    Video("s10_6.py::Lesson", "Comparison tests", 4),

    Section("Direct comparison"),
    Formula("Direct comparison test", (r"Suppose $0 \le a_n \le b_n$ for all $n$ (from some point on). If $\sum b_n$ converges, then $\sum a_n$ \blank{converges}. If $\sum a_n$ diverges, then $\sum b_n$ \blank{diverges}.")),
    Text(r"Smaller than convergent: converges. Bigger than divergent: diverges. Smaller than divergent, or bigger than convergent: no conclusion."),
    VideoExample('A direct comparison', work="2.6cm"),
    Section("Limit comparison"),
    Formula("Limit comparison test", (r"If $a_n, b_n > 0$ and $\lim_{n\to\infty} \frac{a_n}{b_n} = c$ with \blank{$0 < c < \infty$}, then $\sum a_n$ and $\sum b_n$ both converge or both diverge.")),
    Text(r"\textbf{Choosing $b_n$.} Keep the dominant term on top and bottom: $\frac{2n + 1}{n^3 - n + 5}$ behaves like $\frac{n}{n^3} = \frac{1}{n^2}$. Compare with $p$-series and geometric series."),
    BigIdea(r"Compare with a known series: direct comparison needs the right inequality; limit comparison needs a positive, finite limit of the ratio."),
    Check(r"Does $\sum \frac{1}{n^3 + n}$ converge?", selfcheck(r"\text{converges}"), r"$\frac{1}{n^3 + n} < \frac{1}{n^3}$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Does $\sum \frac{1}{n^2 + 5n}$ converge?", selfcheck(r"\text{converges}"), r"$< \frac{1}{n^2}$.", work="1.2cm"),
    Item(r"Does $\sum \frac{1}{\sqrt n - 0.5}$ converge?", selfcheck(r"\text{diverges}"), r"$> \frac{1}{\sqrt n}$, which diverges ($p = \frac12$).", work="1.4cm"),
    Item(r"Does $\sum \frac{3^n}{4^n + 1}$ converge?", selfcheck(r"\text{converges}"), r"$< \left(\frac34\right)^n$ (geometric).", work="1.4cm"),
    Item(r"Does $\sum \frac{n + 1}{n^2}$ converge?", selfcheck(r"\text{diverges}"), r"$> \frac1n$.", work="1.2cm"),
    Item(r"Use limit comparison on $\sum \frac{3n^2 + 1}{n^4 + 2}$.", selfcheck(r"\text{converges}"), r"$b_n = \frac{1}{n^2}$; limit $3$.", work="1.6cm"),
    Item(r"Use limit comparison on $\sum \frac{1}{\sqrt{n^2 + 1}}$.", selfcheck(r"\text{diverges}"), r"$b_n = \frac1n$; limit $1$.", work="1.6cm"),
    Item(r"Use limit comparison on $\sum \frac{2^n}{3^n - n}$.", selfcheck(r"\text{converges}"), r"$b_n = \left(\frac23\right)^n$; limit $1$.", work="1.6cm"),
    Item(r"Use limit comparison on $\sum \sin\frac1n$.", selfcheck(r"\text{diverges}"), r"$b_n = \frac1n$; $\lim \frac{\sin(1/n)}{1/n} = 1$.", work="1.6cm"),
    Item(r"Does $\sum \frac{\arctan n}{n^2}$ converge?", selfcheck(r"\text{converges}"), r"$0 < \arctan n < \frac\pi2$: $< \frac{\pi/2}{n^2}$.", work="1.4cm"),
]
same("p", [L((3 * n**2 + 1) / (n**4 + 2) * n**2), L(n / sp.sqrt(n**2 + 1)), L(sp.sin(1 / n) * n)], [3, 1, 1])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"If $0 \le a_n \le b_n$ and $\sum a_n$ converges, then $\sum b_n$", [r"converges", r"diverges", r"may converge or diverge", r"converges to the same sum"], "C", r"Bigger than convergent: no conclusion."),
        MCQ(r"If $0 \le a_n \le b_n$ and $\sum b_n$ diverges, then $\sum a_n$", [r"converges", r"diverges", r"may converge or diverge", r"converges to $0$"], "C", r"Smaller than divergent: no conclusion."),
    ),
    Variants(
        Item(r"Does $\sum \frac{1}{n^2 + 1}$ converge? Name the comparison.", selfcheck(r"\text{converges: } < \tfrac{1}{n^2}"), r"Direct comparison with $\frac{1}{n^2}$.", work="1.2cm"),
        Item(r"Does $\sum \frac{1}{n - 0.5}$ converge? Name the comparison.", selfcheck(r"\text{diverges: } > \tfrac1n"), r"Direct comparison with $\frac1n$.", work="1.2cm"),
    ),
    Variants(
        Item(r"For $\sum \frac{5n^3 - 2}{n^5 + n}$, find $b_n$ and $\lim \frac{a_n}{b_n}$.", selfcheck(r"b_n = \tfrac{1}{n^2};\ 5"), r"Dominant terms $\frac{5n^3}{n^5}$.", work="1.4cm"),
        Item(r"For $\sum \frac{n}{\sqrt{n^3 + 4}}$, find $b_n$ and $\lim \frac{a_n}{b_n}$.", selfcheck(r"b_n = \tfrac{1}{\sqrt n};\ 1"), r"$\frac{n}{n^{3/2}}$.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"Using limit comparison with $\frac1n$, $\sum \frac{n + 3}{n^2 + 1}$", [r"converges", r"diverges", r"is inconclusive", r"converges to $1$"], "B", r"Limit $1$ and $\sum \frac1n$ diverges."),
        MCQ(r"Using limit comparison with $\frac{1}{n^2}$, $\sum \frac{n + 3}{n^3 + 1}$", [r"converges", r"diverges", r"is inconclusive", r"converges to $3$"], "A", r"Limit $1$ and $\sum \frac{1}{n^2}$ converges."),
    ),
    Variants(
        Item(r"Does $\sum \frac{\cos^2 n}{2^n}$ converge?", selfcheck(r"\text{converges}"), r"$\le \frac{1}{2^n}$.", work="1.2cm"),
        Item(r"Does $\sum \frac{2 + \sin n}{n}$ converge?", selfcheck(r"\text{diverges}"), r"$\ge \frac1n$.", work="1.2cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"Which series converges?", [r"$\sum \frac{n}{n^2 + 1}$", r"$\sum \frac{1}{\sqrt{n + 1}}$", r"$\sum \frac{n}{n^3 + 1}$", r"$\sum \frac{\ln n}{n}$"], "C", r"Behaves like $\frac{1}{n^2}$."),
    MCQ(r"Limit comparison of $\sum \frac{1}{n\sqrt{n} + 1}$ with which series shows convergence?", [r"$\sum \frac1n$", r"$\sum \frac{1}{n^{3/2}}$", r"$\sum \frac{1}{\sqrt n}$", r"$\sum \frac{1}{n^2}$"], "B", r"Dominant term $n^{3/2}$; limit $1$."),
    MCQ(r"If $a_n > 0$ and $\lim_{n\to\infty} n^2 a_n = 4$, then $\sum a_n$", [r"diverges", r"converges to $4$", r"may converge or diverge", r"converges"], "D", r"Limit comparison with $\frac{1}{n^2}$: $\frac{a_n}{1/n^2} \to 4$."),
    MCQ(r"Which comparison shows that $\sum \frac{1}{n + \ln n}$ diverges?", [r"$\frac{1}{n + \ln n} \le \frac1n$", r"limit comparison with $\frac1n$ (limit $1$)", r"$\frac{1}{n + \ln n} \le \frac{1}{n^2}$", r"$\frac{1}{n + \ln n} \ge \frac{1}{n^2}$"], "B",
        r"$\frac{n}{n + \ln n} \to 1$ and the harmonic series diverges.", why_not={"A": "smaller than a divergent series: no conclusion"}),
]
same("m", [L(n * n / (n**3 + 1)), L(n**sp.Rational(3, 2) / (n * sp.sqrt(n) + 1)), L(n / (n + sp.log(n)))], [0, 1, 1])

FRQS = []

TOPIC = Topic(
    number="10.6", title="Comparison Tests for Convergence",
    unit="Unit 10: Infinite Sequences and Series", ced=["LIM-7.A", "LIM-7.A.8", "LIM-7.A.9"],
    goals=r"Use direct and limit comparison with known series to decide convergence.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
