"""Topic 10.7 (BC): Alternating series test for convergence.

CED: LIM-7.A (LIM-7.A.10): sum (-1)^(n+1) b_n with b_n > 0 converges if b_n is decreasing and lim b_n = 0; if b_n does not
go to 0 the series diverges (nth term test); not decreasing: inconclusive. Lesson example: the alternating harmonic
series converges (to ln 2). Worked examples: (-1)^n/sqrt n converges; (-1)^n 2n/(n + 3) diverges; (-1)^n/ln n converges.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)

n = sp.symbols("n", positive=True)
L = lambda a: sp.limit(a, n, sp.oo)
same("ex", [L(1 / n), L(2 * n / (n + 3)), L(1 / sp.log(n))], [0, 2, 0])
close("ln2", float(sum((-1)**(k + 1) / k for k in range(1, 200001))), float(sp.log(2)), 1e-5)

NOTES = [
    Video("s10_7.py::Lesson", "The alternating series test", 4),

    Section("The test"),
    Formula("Alternating series test", (r"If $b_n > 0$, $b_n$ is \blank{decreasing}, and $\lim_{n\to\infty} b_n = \blank{0}$, then $\sum (-1)^{n+1} b_n$ (or $\sum (-1)^n b_n$) converges.")),
    Text(r"The partial sums zigzag inside shrinking intervals and settle on a limit. State both conditions when you use the test."),
    VideoExample('The alternating harmonic series', work="2.8cm"),
    Text(r"\textbf{When it doesn't apply.} If $b_n \not\to 0$, the series diverges by the $n$th term test. If $b_n \to 0$ but isn't decreasing, the alternating series test is inconclusive."),
    BigIdea(r"Alternating, decreasing in size, sizes $\to 0$: converges. Signs can rescue a series that would diverge without them ($\sum \frac{(-1)^n}{\sqrt n}$)."),
    Check(r"Does $\sum \frac{(-1)^n}{n^2}$ converge by the alternating series test?", selfcheck(r"\text{yes}"), r"$\frac{1}{n^2}$ decreases to $0$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Does $\sum \frac{(-1)^{n+1}}{2n + 1}$ converge?", selfcheck(r"\text{converges (AST)}"), r"$\frac{1}{2n + 1}$ decreases to $0$.", work="1.2cm"),
    Item(r"Does $\sum (-1)^n \frac{n + 1}{n}$ converge?", selfcheck(r"\text{diverges}"), r"Sizes $\to 1$: $n$th term test.", work="1.2cm"),
    Item(r"Does $\sum \frac{(-1)^n}{\sqrt[3]{n}}$ converge?", selfcheck(r"\text{converges (AST)}"), r"$n^{-1/3}$ decreases to $0$.", work="1.2cm"),
    Item(r"Does $\sum (-1)^n \frac{n}{n^2 + 1}$ converge?", selfcheck(r"\text{converges (AST)}"), r"$\frac{n}{n^2 + 1} \to 0$ and decreases for $n \ge 1$ (derivative $\frac{1 - x^2}{(x^2 + 1)^2} \le 0$).", work="1.8cm"),
    Item(r"Does $\sum \frac{(-1)^n n}{\ln n}$ ($n \ge 2$) converge?", selfcheck(r"\text{diverges}"), r"$\frac{n}{\ln n} \to \infty$.", work="1.2cm"),
    Item(r"Does $\sum (-1)^{n} e^{-n}$ converge?", selfcheck(r"\text{converges}"), r"AST (or geometric with $r = -\frac1e$).", work="1.2cm"),
    Item(r"Does $\sum \cos(n\pi)\frac{1}{n}$ converge?", selfcheck(r"\text{converges}"), r"$\cos(n\pi) = (-1)^n$: the alternating harmonic series.", work="1.4cm"),
    Item(r"Does $\sum (-1)^n \sin\frac1n$ converge?", selfcheck(r"\text{converges (AST)}"), r"$\sin\frac1n > 0$ decreases to $0$.", work="1.2cm"),
]

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"Which is a condition of the alternating series test for $\sum (-1)^n b_n$?", [r"$\sum b_n$ converges", r"$b_n \to 0$ and $b_n$ is decreasing", r"$b_n$ is increasing", r"$\lim \frac{b_{n+1}}{b_n} < 1$"], "B", r"Decreasing sizes that go to $0$.",
            why_not={"A": "that is absolute convergence (10.9)"}),
    ),
    Variants(
        Item(r"Does $\sum \frac{(-1)^n}{n + 4}$ converge?", selfcheck(r"\text{converges}"), r"AST.", work="1cm"),
        Item(r"Does $\sum \frac{(-1)^n 3n}{n + 1}$ converge?", selfcheck(r"\text{diverges}"), r"Sizes $\to 3$.", work="1cm"),
        Item(r"Does $\sum \frac{(-1)^{n+1}}{n^{0.1}}$ converge?", selfcheck(r"\text{converges}"), r"AST.", work="1cm"),
    ),
    Variants(
        MCQ(r"$\sum \frac{(-1)^n}{n}$ converges, but $\sum \frac1n$ diverges. This shows that", [r"the AST is wrong", r"alternating signs can make a series converge", r"every alternating series converges", r"the harmonic series converges"], "B", r"Cancellation from the signs."),
    ),
    Variants(
        Item(r"Find $\lim b_n$ for $\sum (-1)^n \frac{n^2}{n^2 + 1}$, and decide convergence.", selfcheck(r"1;\ \text{diverges}"), r"$n$th term test.", work="1.2cm"),
        Item(r"Find $\lim b_n$ for $\sum (-1)^n \frac{n}{n^2 + 1}$, and decide convergence.", selfcheck(r"0;\ \text{converges}"), r"Decreasing to $0$: AST.", work="1.2cm"),
    ),
    Variants(
        MCQ(r"Which series converges?", [r"$\sum (-1)^n \frac{n}{2n - 1}$", r"$\sum (-1)^n \ln n$", r"$\sum (-1)^n \frac{1}{n\ln n}$", r"$\sum (-1)^n e^n$"], "C", r"Sizes decrease to $0$."),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"Which of the following converge? I. $\sum \frac{(-1)^n}{n}$ \ II. $\sum \frac{(-1)^n n}{n + 1}$ \ III. $\sum \frac{(-1)^n}{\sqrt{n + 1}}$", [r"I only", r"I and III only", r"III only", r"I, II and III"], "B", r"II fails the $n$th term test."),
    MCQ(r"The alternating series test shows that $\sum_{n=1}^\infty (-1)^{n+1} b_n$ converges if", [r"$b_n \to 0$", r"$b_n$ is decreasing", r"$b_n > 0$ is decreasing and $b_n \to 0$", r"$\sum b_n$ diverges"], "C", r"Both conditions are needed."),
    MCQ(r"$\sum_{n=1}^\infty \frac{(-1)^n}{n^p}$ converges for", [r"$p > 1$ only", r"$p > 0$", r"$p \ge 1$", r"all $p$"], "B", r"For $p > 0$ the sizes decrease to $0$; for $p \le 0$ they don't go to $0$."),
    MCQ(r"For which series is the alternating series test NOT enough to show convergence, even though the series converges?", [r"$\sum \frac{(-1)^n}{n}$", r"$\sum \frac{(-1)^n}{\sqrt n}$", r"$\sum \frac{(-1)^n}{\ln n}$", r"$\sum \frac{\sin n}{n^2}$"], "D",
        r"Its signs don't strictly alternate; it converges absolutely by comparison with $\frac{1}{n^2}$."),
]

FRQS = []

TOPIC = Topic(
    number="10.7", title="Alternating Series Test for Convergence",
    unit="Unit 10: Infinite Sequences and Series", ced=["LIM-7.A", "LIM-7.A.10"],
    goals=r"Use the alternating series test, stating both conditions, and recognize when it does not apply.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
