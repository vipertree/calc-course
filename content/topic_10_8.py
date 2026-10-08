"""Topic 10.8 (BC): Ratio test for convergence.

CED: LIM-7.A (LIM-7.A.11): L = lim |a_(n+1)/a_n|; L < 1 converges (absolutely), L > 1 or infinity diverges, L = 1
inconclusive; (n + 1)! = (n + 1) n!. Lesson example: n/3^n, L = 1/3. Worked examples: 2^n/n! (L = 0); n!/10^n (L = oo);
1/n^2 (L = 1, inconclusive).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)

n = sp.symbols("n", positive=True, integer=True)


def ratio(a):
    return sp.limit(sp.Abs(sp.simplify(sp.combsimp(a.subs(n, n + 1) / a))), n, sp.oo)


same("lesson", [ratio(n / 3**n)], [sp.Rational(1, 3)])
same("ex", [ratio(2**n / sp.factorial(n)), ratio(sp.factorial(n) / 10**n), ratio(1 / n**2)], [0, sp.oo, 1])

NOTES = [
    Video("s10_8.py::Lesson", "The ratio test", 4),

    Section("The test"),
    Formula("Ratio test", (r"Let $L = \lim_{n\to\infty} \left|\dfrac{a_{n+1}}{a_n}\right|$. If $L < 1$, $\sum a_n$ \blank{converges (absolutely)}. If $L > 1$ or $L = \infty$, it \blank{diverges}. If $L = 1$, the test is \blank{inconclusive}.")),
    Text(r"Far out, such a series behaves like a geometric series with ratio $L$."),
    VideoExample('Using the ratio test', work="4cm"),
    Formula("Factorials", (r"$n! = n(n - 1)\cdots 2 \cdot 1$, so $(n + 1)! = \blank{(n + 1)\cdot n!}$ and $\dfrac{n!}{(n + 1)!} = \dfrac{1}{n + 1}$.")),
    Text(r"Use the ratio test for factorials and exponentials. For $p$-series and rational functions of $n$ it always gives $L = 1$."),
    BigIdea(r"$L = \lim |a_{n+1}/a_n|$: below $1$ converges, above $1$ diverges, $1$ says nothing."),
    Check(r"Find $L$ for $\sum \frac{5^n}{n!}$.", selfcheck(r"0;\ \text{converges}"), r"$\frac{5}{n + 1} \to 0$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Apply the ratio test to $\sum \frac{n}{2^n}$.", selfcheck(r"L = \tfrac12;\ \text{converges}"), r"$\frac{n + 1}{2n} \to \frac12$.", work="1.6cm"),
    Item(r"Apply the ratio test to $\sum \frac{3^n}{n^2}$.", selfcheck(r"L = 3;\ \text{diverges}"), r"$\frac{3n^2}{(n + 1)^2} \to 3$.", work="1.6cm"),
    Item(r"Apply the ratio test to $\sum \frac{n!}{n^n}$.", selfcheck(r"L = \tfrac1e;\ \text{converges}"), r"$\frac{(n + 1)!}{(n + 1)^{n+1}}\cdot\frac{n^n}{n!} = \left(\frac{n}{n + 1}\right)^n \to \frac1e$.", work="2.2cm"),
    Item(r"Apply the ratio test to $\sum \frac{(2n)!}{(n!)^2}$.", selfcheck(r"L = 4;\ \text{diverges}"), r"$\frac{(2n + 2)(2n + 1)}{(n + 1)^2} \to 4$.", work="2.2cm"),
    Item(r"Apply the ratio test to $\sum \frac{n^3}{n!}$.", selfcheck(r"L = 0;\ \text{converges}"), r"$\frac{(n + 1)^3}{n^3}\cdot\frac{1}{n + 1} \to 0$.", work="1.8cm"),
    Item(r"Apply the ratio test to $\sum \frac{(-1)^n 4^n}{5^n n}$.", selfcheck(r"L = \tfrac45;\ \text{converges absolutely}"), r"$\frac{4n}{5(n + 1)} \to \frac45$.", work="1.8cm"),
    Item(r"What does the ratio test say about $\sum \frac{1}{n}$?", selfcheck(r"L = 1;\ \text{inconclusive}"), r"$\frac{n}{n + 1} \to 1$.", work="1.2cm"),
    Item(r"Apply the ratio test to $\sum \frac{n^2 2^n}{3^n}$.", selfcheck(r"L = \tfrac23;\ \text{converges}"), r"$\frac{(n + 1)^2}{n^2}\cdot\frac23 \to \frac23$.", work="1.8cm"),
]
same("p", [ratio(n / 2**n), ratio(3**n / n**2), ratio(sp.factorial(n) / n**n), ratio(sp.factorial(2 * n) / sp.factorial(n)**2), ratio(n**3 / sp.factorial(n)), ratio(n**2 * 2**n / 3**n)],
     [sp.Rational(1, 2), 3, sp.exp(-1), 4, 0, sp.Rational(2, 3)])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"If $\lim \left|\frac{a_{n+1}}{a_n}\right| = 1$, then $\sum a_n$", [r"converges", r"diverges", r"converges to $1$", r"may converge or diverge"], "D", r"Inconclusive."),
    ),
    Variants(
        Item(r"Find $L$ for $\sum \frac{n}{4^n}$ and decide convergence.", selfcheck(r"\tfrac14;\ \text{converges}"), r"$\frac{n + 1}{4n}$.", work="1.4cm"),
        Item(r"Find $L$ for $\sum \frac{2^n}{n}$ and decide convergence.", selfcheck(r"2;\ \text{diverges}"), r"$\frac{2n}{n + 1}$.", work="1.4cm"),
        Item(r"Find $L$ for $\sum \frac{10^n}{n!}$ and decide convergence.", selfcheck(r"0;\ \text{converges}"), r"$\frac{10}{n + 1}$.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"$\dfrac{(n + 2)!}{n!} = $", [r"$2$", r"$(n + 2)(n + 1)$", r"$n + 2$", r"$(n + 2)!$"], "B", r"$(n + 2)! = (n + 2)(n + 1)n!$."),
        MCQ(r"$\dfrac{(n - 1)!}{(n + 1)!} = $", [r"$\frac{1}{n(n + 1)}$", r"$\frac{1}{n + 1}$", r"$n(n + 1)$", r"$\frac12$"], "A", r"$(n + 1)! = (n + 1)n(n - 1)!$."),
    ),
    Variants(
        MCQ(r"For which series is the ratio test inconclusive?", [r"$\sum \frac{1}{2^n}$", r"$\sum \frac{n}{n^3 + 1}$", r"$\sum \frac{n!}{3^n}$", r"$\sum \frac{1}{n!}$"], "B", r"Rational functions of $n$ give $L = 1$."),
    ),
    Variants(
        Item(r"Find $L$ for $\sum \frac{3^n}{(n + 1)!}$.", selfcheck(r"0"), r"$\frac{3}{n + 2} \to 0$.", work="1.2cm"),
        Item(r"Find $L$ for $\sum \frac{n^5}{5^n}$.", selfcheck(r"\tfrac15"), r"$\left(\frac{n + 1}{n}\right)^5\frac15$.", work="1.2cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"For $\sum_{n=1}^\infty \frac{n!}{(2n)!}$, the ratio test gives $L = $", [r"$0$", r"$\frac12$", r"$\frac14$", r"$1$"], "A", r"$\frac{n + 1}{(2n + 2)(2n + 1)} \to 0$."),
    MCQ(r"Which series diverges by the ratio test?", [r"$\sum \frac{2^n}{n!}$", r"$\sum \frac{n}{e^n}$", r"$\sum \frac{n^2}{2^n}$", r"$\sum \frac{3^n}{n^3}$"], "D", r"$L = 3$."),
    MCQ(r"The ratio test applied to $\sum \frac{(n + 1)^2}{n!}$ gives", [r"$L = 1$, inconclusive", r"$L = 0$, converges", r"$L = \infty$, diverges", r"$L = 2$, diverges"], "B", r"$\frac{(n + 2)^2}{(n + 1)^2}\cdot\frac{1}{n + 1} \to 0$."),
    MCQ(r"For which value of $x$ does $\sum \frac{x^n}{2^n}$ diverge by the ratio test?", [r"$x = 1$", r"$x = -1$", r"$x = 3$", r"$x = 0$"], "C", r"$L = \frac{|x|}{2}$; $x = 3$ gives $\frac32 > 1$."),
]
same("m", [ratio(sp.factorial(n) / sp.factorial(2 * n)), ratio((n + 1)**2 / sp.factorial(n))], [0, 0])

FRQS = []

TOPIC = Topic(
    number="10.8", title="Ratio Test for Convergence",
    unit="Unit 10: Infinite Sequences and Series", ced=["LIM-7.A", "LIM-7.A.11"],
    goals=r"Use the ratio test, simplifying factorials and powers, and recognize when it is inconclusive.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
