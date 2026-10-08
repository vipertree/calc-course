"""Topic 10.3 (BC): The nth term test for divergence.

CED: LIM-7.A (LIM-7.A.5): if lim a_n != 0 (or does not exist), sum a_n diverges; if lim a_n = 0 the test is inconclusive
(1/n diverges, 1/n^2 converges). Lesson example: n/(2n + 1) -> 1/2, diverges. Worked examples: (-1)^n (limit DNE);
(1 + 1/n)^n -> e; 1/sqrt n (inconclusive).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)

n = sp.symbols("n", positive=True)
L = lambda a: sp.limit(a, n, sp.oo)

same("lesson", [L(n / (2 * n + 1))], [sp.Rational(1, 2)])
same("ex", [L((1 + 1 / n)**n), L(1 / sp.sqrt(n))], [sp.E, 0])

NOTES = [
    Video("s10_3.py::Lesson", "The nth term test", 4),

    Section("The test"),
    Formula("$n$th term test for divergence", (r"If $\lim_{n\to\infty} a_n \ne 0$ or the limit does not exist, then $\sum a_n$ \blank{diverges}. If $\lim_{n\to\infty} a_n = 0$, the test is \blank{inconclusive}.")),
    Text(r"\textbf{Why.} If $\sum a_n = S$, then $a_n = S_n - S_{n-1} \to S - S = 0$."),
    VideoExample('Using the test', work="2.6cm"),
    Text(r"\textbf{Zero is not enough.} $\frac1n \to 0$ and $\sum \frac1n$ diverges; $\frac{1}{n^2} \to 0$ and $\sum \frac{1}{n^2}$ converges. Never conclude convergence from the $n$th term test."),
    BigIdea(r"Terms not going to $0$: diverges. Terms going to $0$: try another test."),
    Check(r"What does the $n$th term test say about $\sum \frac{3n^2}{n^2 + 1}$?", selfcheck(r"\text{diverges (terms} \to 3)"), r"$\lim a_n = 3 \ne 0$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Apply the $n$th term test to $\sum \frac{2n - 1}{5n + 3}$.", selfcheck(r"\text{diverges}"), r"$a_n \to \frac25 \ne 0$.", work="1.2cm"),
    Item(r"Apply the $n$th term test to $\sum \frac{n}{n^2 + 1}$.", selfcheck(r"\text{inconclusive}"), r"$a_n \to 0$.", work="1.2cm"),
    Item(r"Apply the $n$th term test to $\sum \cos\frac1n$.", selfcheck(r"\text{diverges}"), r"$\cos\frac1n \to 1$.", work="1.2cm"),
    Item(r"Apply the $n$th term test to $\sum \frac{e^n}{n^3}$.", selfcheck(r"\text{diverges}"), r"$\frac{e^n}{n^3} \to \infty$ (exponentials beat powers).", work="1.2cm"),
    Item(r"Apply the $n$th term test to $\sum n\sin\frac1n$.", selfcheck(r"\text{diverges}"), r"$n\sin\frac1n = \frac{\sin(1/n)}{1/n} \to 1$.", work="1.4cm"),
    Item(r"Apply the $n$th term test to $\sum \frac{\ln n}{n}$.", selfcheck(r"\text{inconclusive}"), r"$\frac{\ln n}{n} \to 0$ (L'Hospital).", work="1.4cm"),
    Item(r"Apply the $n$th term test to $\sum (-1)^n\frac{n}{n + 1}$.", selfcheck(r"\text{diverges}"), r"The terms approach $\pm1$ alternately: the limit does not exist.", work="1.4cm"),
    Item(r"Apply the $n$th term test to $\sum \left(1 - \frac2n\right)^n$.", selfcheck(r"\text{diverges}"), r"$\left(1 - \frac2n\right)^n \to e^{-2} \ne 0$.", work="1.4cm"),
]
same("p", [L((2 * n - 1) / (5 * n + 3)), L(n * sp.sin(1 / n)), L((1 - 2 / n)**n), L(sp.log(n) / n)], [sp.Rational(2, 5), 1, sp.exp(-2), 0])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"If $\lim_{n\to\infty} a_n = 0$, then $\sum a_n$", [r"converges", r"diverges", r"converges to $0$", r"may converge or diverge"], "D", r"The test is inconclusive."),
    ),
    Variants(
        MCQ(r"Which series diverges by the $n$th term test?", [r"$\sum \frac{1}{n^2}$", r"$\sum \frac{n^2}{n^2 + 4}$", r"$\sum \frac1n$", r"$\sum \frac{1}{2^n}$"], "B", r"$\frac{n^2}{n^2 + 4} \to 1$.", why_not={"C": "it diverges, but not by this test: its terms go to $0$"}),
        MCQ(r"Which series diverges by the $n$th term test?", [r"$\sum \frac{1}{\sqrt n}$", r"$\sum \frac{\ln n}{n}$", r"$\sum \sqrt{\frac{n}{n + 1}}$", r"$\sum \frac{n}{3^n}$"], "C", r"$\sqrt{\frac{n}{n + 1}} \to 1$."),
    ),
    Variants(
        Item(r"Find $\lim a_n$ for $a_n = \frac{3n + 2}{n}$, and state what the $n$th term test says.", selfcheck(r"3;\ \text{diverges}"), r"$3 \ne 0$.", work="1.2cm"),
        Item(r"Find $\lim a_n$ for $a_n = \frac{n + 1}{n^2}$, and state what the $n$th term test says.", selfcheck(r"0;\ \text{inconclusive}"), r"$0$.", work="1.2cm"),
    ),
    Variants(
        MCQ(r"A student writes: ``$\frac{1}{n} \to 0$, so $\sum \frac1n$ converges by the $n$th term test.'' The student is", [r"correct", r"wrong: the test never shows convergence", r"wrong: $\frac1n$ does not approach $0$", r"correct only for $n \ge 1$"], "B", r"The test can only show divergence."),
    ),
    Variants(
        Item(r"Apply the $n$th term test to $\sum \arctan n$.", selfcheck(r"\text{diverges}"), r"$\arctan n \to \frac\pi2 \ne 0$.", work="1.2cm"),
        Item(r"Apply the $n$th term test to $\sum \frac{1}{\ln n}$ ($n \ge 2$).", selfcheck(r"\text{inconclusive}"), r"$\frac{1}{\ln n} \to 0$.", work="1.2cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"Which of the following series must diverge?", [r"$\sum \frac{n}{n^3 + 1}$", r"$\sum \frac{(-1)^n}{n}$", r"$\sum \frac{1}{n^{3/2}}$", r"$\sum \frac{4n^2}{(2n + 1)^2}$"], "D", r"$\frac{4n^2}{(2n + 1)^2} \to 1 \ne 0$."),
    MCQ(r"If $\sum a_n$ converges, which must be true?", [r"$\lim a_n = 0$", r"$a_n > 0$ for all $n$", r"$\sum |a_n|$ converges", r"$\lim a_n = 1$"], "A", r"The contrapositive of the $n$th term test.", why_not={"C": "conditional convergence (10.9)"}),
    MCQ(r"$\lim_{n\to\infty} a_n$ for $a_n = \frac{2^n}{2^n + n}$ is", [r"$0$", r"$1$", r"$2$", r"does not exist"], "B", r"$\frac{1}{1 + n/2^n} \to 1$, so $\sum a_n$ diverges."),
    MCQ(r"What can be concluded about $\sum \frac{n!}{n^n}$ from the $n$th term test alone?", [r"it converges", r"it diverges", r"nothing: the terms go to $0$", r"it converges to $0$"], "C", r"$\frac{n!}{n^n} \to 0$; another test (ratio) is needed."),
]
same("m", [L(4 * n**2 / (2 * n + 1)**2), L(2**n / (2**n + n))], [1, 1])

FRQS = []

TOPIC = Topic(
    number="10.3", title="The nth Term Test for Divergence",
    unit="Unit 10: Infinite Sequences and Series", ced=["LIM-7.A", "LIM-7.A.5"],
    goals=r"Use the $n$th term test to show divergence, and recognize when it is inconclusive.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
