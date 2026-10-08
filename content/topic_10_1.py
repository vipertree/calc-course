"""Topic 10.1 (BC): Defining convergent and divergent infinite series.

CED: LIM-7.A (LIM-7.A.1, LIM-7.A.2): the nth partial sum S_n = a_1 + ... + a_n; the series converges to S if S_n -> S,
otherwise it diverges. Lesson example: telescoping sum of 1/(n(n + 1)) = 1. Worked examples: sum of 2 diverges;
S_n = 3n/(n + 1) converges to 3; telescoping 1/n - 1/(n + 2) = 3/2.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)

n = sp.symbols("n", positive=True, integer=True)
N = sp.symbols("N", positive=True, integer=True)


def ssum(a, start=1):
    return sp.simplify(sp.summation(a, (n, start, sp.oo)))


same("lesson", [ssum(1 / (n * (n + 1))), sp.simplify(sp.summation(1 / (n * (n + 1)), (n, 1, N)))], [1, N / (N + 1)])
same("ex", [sp.limit(3 * N / (N + 1), N, sp.oo), ssum(1 / n - 1 / (n + 2))], [3, sp.Rational(3, 2)])

NOTES = [
    Video("s10_1.py::Lesson", "Convergent and divergent series", 4),

    Section("Partial sums"),
    Text(r"An infinite series $\sum_{n=1}^\infty a_n = a_1 + a_2 + a_3 + \cdots$ can't be added term by term forever. Instead, add the first $n$ terms."),
    Formula("Convergence of a series", (r"The $n$th partial sum is $S_n = \blank{a_1 + a_2 + \cdots + a_n}$. The series \blank{converges} to $S$ if $\lim_{n\to\infty} S_n = S$; otherwise it \blank{diverges}.")),
    Text(r"\textbf{Three behaviors.} $\sum 1$: $S_n = n \to \infty$ (diverges). $\sum (-1)^{n+1}$: $S_n$ alternates $1, 0, 1, 0, \ldots$ (diverges). $\sum \left(\frac12\right)^n$: $S_n \to 1$ (converges to $1$)."),
    VideoExample('A telescoping series', work="3.6cm"),
    Text(r"\textbf{Telescoping.} When each term is a difference like $\frac1n - \frac{1}{n + 1}$, the partial sum collapses: only the first and last pieces survive."),
    BigIdea(r"A series converges exactly when its partial sums approach a limit; that limit is the sum."),
    Check(r"$S_n = 5 - \frac1n$. Does the series converge? To what?", selfcheck(r"\text{converges to } 5"), r"$\lim S_n = 5$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Find $S_4$ for $\sum_{n=1}^\infty \frac1n$.", num(sp.Rational(25, 12)), r"$1 + \frac12 + \frac13 + \frac14 = \frac{25}{12}$.", work="1.2cm"),
    Item(r"Find $S_3$ for $\sum_{n=1}^\infty (-2)^n$.", num(-6), r"$-2 + 4 - 8 = -6$.", work="1cm"),
    Item(r"The partial sums of a series are $S_n = \frac{2n + 1}{n}$. Find the sum of the series.", num(2), r"$\lim S_n = 2$.", work="1cm"),
    Item(r"The partial sums of a series are $S_n = n^2$. Does the series converge?", selfcheck(r"\text{diverges}"), r"$S_n \to \infty$.", work="1cm"),
    Item(r"Find $\sum_{n=1}^\infty \left(\frac1n - \frac{1}{n + 1}\right)$.", num(1), r"$S_n = 1 - \frac{1}{n + 1} \to 1$.", work="1.4cm"),
    Item(r"Find $\sum_{n=1}^\infty \frac{2}{n(n + 2)}$.", num(ssum(2 / (n * (n + 2)))), r"$\frac{2}{n(n + 2)} = \frac1n - \frac{1}{n + 2}$: sum $\frac32$.", work="1.8cm"),
    Item(r"Find $\sum_{n=1}^\infty \left(\frac{1}{\sqrt n} - \frac{1}{\sqrt{n + 1}}\right)$.", num(1), r"$S_n = 1 - \frac{1}{\sqrt{n + 1}} \to 1$.", work="1.6cm"),
    Item(r"The partial sums of a series are $S_n = 4 - \frac{3}{2^n}$. Find $a_1$, $a_2$ and the sum.", selfcheck(r"a_1 = \tfrac52,\ a_2 = \tfrac34,\ S = 4"), r"$a_1 = S_1 = \frac52$; $a_2 = S_2 - S_1 = \frac{13}{4} - \frac52 = \frac34$; sum $4$.", work="1.8cm"),
]

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"A series converges when", [r"its terms are all positive", r"its terms approach $0$", r"its partial sums approach a finite limit", r"its partial sums are bounded"], "C", r"The definition.",
            why_not={"B": "necessary but not enough (the harmonic series)"}),
    ),
    Variants(
        Item(r"$S_n = \frac{5n}{n + 2}$. Find the sum of the series.", num(5), r"$\lim S_n = 5$.", work="1cm"),
        Item(r"$S_n = 3 - \frac{2}{n}$. Find the sum of the series.", num(3), r"$3$.", work="1cm"),
        Item(r"$S_n = \frac{n}{2n + 1}$. Find the sum of the series.", num(sp.Rational(1, 2)), r"$\frac12$.", work="1cm"),
    ),
    Variants(
        Item(r"Find $\sum_{n=1}^\infty \left(\frac{1}{n + 1} - \frac{1}{n + 2}\right)$.", num(sp.Rational(1, 2)), r"$S_n = \frac12 - \frac{1}{n + 2}$.", work="1.4cm"),
        Item(r"Find $\sum_{n=2}^\infty \left(\frac1n - \frac{1}{n + 1}\right)$.", num(sp.Rational(1, 2)), r"$S_n = \frac12 - \frac{1}{n + 1}$.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"The series $1 - 1 + 1 - 1 + \cdots$", [r"converges to $0$", r"converges to $\frac12$", r"converges to $1$", r"diverges"], "D", r"$S_n$ alternates between $1$ and $0$."),
    ),
    Variants(
        Item(r"$S_n = 2 - \frac{1}{n}$. Find $a_3$.", num(sp.Rational(1, 6)), r"$S_3 - S_2 = \frac53 - \frac32 = \frac16$.", work="1.2cm"),
        Item(r"$S_n = n^2 + n$. Find $a_4$.", num(8), r"$S_4 - S_3 = 20 - 12 = 8$.", work="1.2cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$\displaystyle\sum_{n=1}^\infty \frac{1}{(n + 1)(n + 2)} = $", [r"$\frac12$", r"$1$", r"$\frac13$", r"$\frac32$"], "A", r"$\frac{1}{n + 1} - \frac{1}{n + 2}$ telescopes to $\frac12$."),
    MCQ(r"If the $n$th partial sum of $\sum a_n$ is $S_n = \frac{n - 1}{n + 1}$, then $\sum a_n$", [r"diverges", r"converges to $0$", r"converges to $-1$", r"converges to $1$"], "D", r"$\lim S_n = 1$.", why_not={"C": "that is $S_0$"}),
    MCQ(r"If $S_n = \ln n$ for a series $\sum a_n$, the series", [r"converges to $0$", r"diverges", r"converges to $1$", r"converges to $e$"], "B", r"$\ln n \to \infty$."),
    MCQ(r"$\displaystyle\sum_{n=1}^\infty \left(\frac{1}{2n - 1} - \frac{1}{2n + 1}\right) = $", [r"$\frac12$", r"$\infty$", r"$1$", r"$\frac13$"], "C", r"Telescopes: $1 - \frac{1}{2N + 1} \to 1$."),
]
same("m", [ssum(1 / ((n + 1) * (n + 2))), ssum(1 / (2 * n - 1) - 1 / (2 * n + 1))], [sp.Rational(1, 2), 1])

FRQS = []

TOPIC = Topic(
    number="10.1", title="Defining Convergent and Divergent Infinite Series",
    unit="Unit 10: Infinite Sequences and Series", ced=["LIM-7.A", "LIM-7.A.1", "LIM-7.A.2"],
    goals=r"Use partial sums to decide whether a series converges, and find sums of telescoping series.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
