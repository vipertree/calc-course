"""Topic 10.9 (BC): Determining absolute or conditional convergence.

CED: LIM-7.A (LIM-7.A.12, LIM-7.A.13): absolutely convergent if sum |a_n| converges (which implies sum a_n converges);
conditionally convergent if sum a_n converges but sum |a_n| diverges. Plan: nth term check, then |a_n|, then the series
itself (usually AST). Lesson example: (-1)^n/n^2 absolute, (-1)^n/n conditional, (-1)^n n/(n + 1) divergent. Worked
examples: (-1)^n/sqrt n conditional; sin n/n^2 absolute; (-1)^n/(n ln n) conditional.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)

x = sp.symbols("x", positive=True)
same("checks", [sp.integrate(1 / x**2, (x, 1, sp.oo)), sp.integrate(1 / sp.sqrt(x), (x, 1, sp.oo)), sp.integrate(1 / (x * sp.log(x)), (x, 2, sp.oo))], [1, sp.oo, sp.oo])

NOTES = [
    Video("s10_9.py::Lesson", "Absolute and conditional convergence", 3),

    Section("Definitions"),
    Formula("Absolute and conditional convergence", (r"$\sum a_n$ is \blank{absolutely convergent} if $\sum |a_n|$ converges. It is \blank{conditionally convergent} if $\sum a_n$ converges but $\sum |a_n|$ diverges. "
                                                     r"If $\sum |a_n|$ converges, then $\sum a_n$ converges.")),
    Section("A plan"),
    Text(r"(0) If $a_n \not\to 0$: divergent. (1) Test $\sum |a_n|$ with a positive-series test; if it converges, absolutely convergent. (2) Otherwise test $\sum a_n$ itself, usually with the alternating series test; if it converges, conditionally convergent. (3) Otherwise divergent."),
    VideoExample('Three classifications', work="3.6cm"),
    Text(r"\textbf{Messy signs.} For $\sum \frac{\sin n}{n^2}$ the alternating series test doesn't apply, but $\left|\frac{\sin n}{n^2}\right| \le \frac{1}{n^2}$ gives absolute convergence."),
    BigIdea(r"Absolute: converges even with every term made positive. Conditional: converges only because of the signs."),
    Check(r"Classify $\sum \frac{(-1)^n}{n^3}$.", selfcheck(r"\text{absolutely convergent}"), r"$\sum \frac{1}{n^3}$ converges."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Classify $\sum \frac{(-1)^{n+1}}{n^{3/2}}$.", selfcheck(r"\text{absolutely convergent}"), r"$p = \frac32$.", work="1.2cm"),
    Item(r"Classify $\sum \frac{(-1)^n}{n^{2/3}}$.", selfcheck(r"\text{conditionally convergent}"), r"$\sum n^{-2/3}$ diverges; AST converges.", work="1.4cm"),
    Item(r"Classify $\sum \frac{(-1)^n 2^n}{n!}$.", selfcheck(r"\text{absolutely convergent}"), r"Ratio test on $\frac{2^n}{n!}$: $L = 0$.", work="1.4cm"),
    Item(r"Classify $\sum (-1)^n \frac{n^2}{n^2 + 1}$.", selfcheck(r"\text{divergent}"), r"Terms don't go to $0$.", work="1.2cm"),
    Item(r"Classify $\sum \frac{(-1)^n}{2n + 3}$.", selfcheck(r"\text{conditionally convergent}"), r"$\sum \frac{1}{2n + 3}$ diverges (limit comparison with $\frac1n$); AST converges.", work="1.6cm"),
    Item(r"Classify $\sum \frac{\cos n}{n^3}$.", selfcheck(r"\text{absolutely convergent}"), r"$\le \frac{1}{n^3}$.", work="1.2cm"),
    Item(r"Classify $\sum \frac{(-1)^n n}{3^n}$.", selfcheck(r"\text{absolutely convergent}"), r"Ratio test: $L = \frac13$.", work="1.4cm"),
    Item(r"Classify $\sum \frac{(-1)^n \ln n}{n}$ ($n \ge 3$).", selfcheck(r"\text{conditionally convergent}"), r"$\frac{\ln n}{n} > \frac1n$: absolute values diverge. $\frac{\ln n}{n}$ decreases to $0$ for $n \ge 3$: AST.", work="1.8cm"),
]

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"A series is conditionally convergent when", [r"$\sum |a_n|$ converges", r"$\sum a_n$ converges and $\sum |a_n|$ diverges", r"$\sum a_n$ diverges and $\sum |a_n|$ converges", r"its terms alternate in sign"], "B", r"The definition.",
            why_not={"C": "impossible: absolute convergence implies convergence"}),
    ),
    Variants(
        Item(r"Classify $\sum \frac{(-1)^n}{n^4}$.", selfcheck(r"\text{absolutely convergent}"), r"$p = 4$.", work="1cm"),
        Item(r"Classify $\sum \frac{(-1)^n}{\sqrt[3]{n}}$.", selfcheck(r"\text{conditionally convergent}"), r"$p = \frac13$; AST.", work="1cm"),
        Item(r"Classify $\sum (-1)^n \frac{3n}{n + 2}$.", selfcheck(r"\text{divergent}"), r"Terms $\to \pm3$.", work="1cm"),
    ),
    Variants(
        MCQ(r"Which series is conditionally convergent?", [r"$\sum \frac{(-1)^n}{n^2}$", r"$\sum \frac{(-1)^n}{2^n}$", r"$\sum \frac{(-1)^n}{n + 1}$", r"$\sum (-1)^n$"], "C", r"Absolute values: harmonic-like; AST converges."),
        MCQ(r"Which series is absolutely convergent?", [r"$\sum \frac{(-1)^n}{\sqrt n}$", r"$\sum \frac{(-1)^n}{\ln n}$", r"$\sum \frac{(-1)^n}{n}$", r"$\sum \frac{(-1)^n}{n\sqrt n}$"], "D", r"$p = \frac32$."),
    ),
    Variants(
        MCQ(r"If $\sum |a_n|$ converges, which must be true?", [r"$\sum a_n$ converges", r"$\sum a_n$ diverges", r"$a_n > 0$ for all $n$", r"$\sum a_n$ is conditionally convergent"], "A", r"Absolute convergence implies convergence."),
    ),
    Variants(
        Item(r"Classify $\sum \frac{(-1)^n n!}{n^n}$.", selfcheck(r"\text{absolutely convergent}"), r"Ratio test: $L = \frac1e$.", work="1.4cm"),
        Item(r"Classify $\sum \frac{(-1)^n}{n^{1.0001}}$.", selfcheck(r"\text{absolutely convergent}"), r"$p > 1$.", work="1.2cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"Which of the following is true about $\sum_{n=1}^\infty \frac{(-1)^n}{\sqrt{n + 2}}$?", [r"it diverges", r"it converges absolutely", r"it converges to $0$", r"it converges conditionally"], "D", r"$\sum \frac{1}{\sqrt{n + 2}}$ diverges; AST converges."),
    MCQ(r"Which series converges absolutely? I. $\sum \frac{(-1)^n}{n^2 + 1}$ \ II. $\sum \frac{(-1)^n n}{n^2 + 1}$ \ III. $\sum \frac{(-1)^n 3^n}{4^n}$", [r"I only", r"I and III only", r"II and III only", r"I, II and III"], "B", r"II is only conditional (behaves like $\frac1n$)."),
    MCQ(r"For which $p$ is $\sum \frac{(-1)^n}{n^p}$ conditionally convergent?", [r"$p > 1$", r"$p \le 0$", r"$0 < p \le 1$", r"all $p > 0$"], "C", r"$0 < p \le 1$: absolute values diverge but AST applies."),
    MCQ(r"$\sum a_n$ converges conditionally. Which must be true?", [r"$\lim a_n = 0$", r"$\sum |a_n|$ converges", r"$a_n$ alternates in sign", r"$\sum a_n^2$ diverges"], "A", r"Any convergent series has terms going to $0$."),
]

FRQS = []

TOPIC = Topic(
    number="10.9", title="Determining Absolute or Conditional Convergence",
    unit="Unit 10: Infinite Sequences and Series", ced=["LIM-7.A", "LIM-7.A.12", "LIM-7.A.13"],
    goals=r"Classify series as absolutely convergent, conditionally convergent, or divergent.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
