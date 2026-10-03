"""Topic 10.10 (BC): Alternating series error bound.

CED: LIM-7.B (LIM-7.B.1): for an alternating series satisfying the AST with sum S, |S - S_n| <= b_(n+1); S lies between
S_n and S_(n+1), so the error has the sign of the first omitted term. Lesson example: S_4 for sum (-1)^(n+1)/n^2 =
115/144, error <= 1/25, underestimate. Worked examples: alternating harmonic needs n >= 1000 for error < 0.001; 1/e
through n = 4 (3/8, error <= 1/120); sin 0.5 with two terms (error <= 0.00026).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)

k = sp.symbols("k", integer=True, positive=True)
S = lambda terms: sum(terms)

same("lesson", [S([sp.Rational((-1)**(j + 1), j**2) for j in range(1, 5)])], [sp.Rational(115, 144)])
close("lesson err", float(sp.pi**2 / 12 - sp.Rational(115, 144)), 0.0239, 1e-4)
same("ex2", [S([sp.Rational((-1)**j, sp.factorial(j)) for j in range(0, 5)])], [sp.Rational(3, 8)])
close("ex3", 0.5 - 0.5**3 / 6, 0.479167, 1e-6)

NOTES = [
    Video("s10_10.py::Lesson", "Alternating series error bound", 4),

    Section("The bound"),
    Formula("Alternating series error bound", (r"If $\sum (-1)^{n+1} b_n$ satisfies the alternating series test and has sum $S$, then \[ |S - S_n| \le \blank{b_{n+1}}, \] the first omitted term.")),
    Text(r"\textbf{Over or under?} $S$ lies between $S_n$ and $S_{n+1}$. If the first omitted term is positive, $S_n$ is an underestimate; if negative, an overestimate."),
    VideoExample('Bounding an error', work="4cm"),
    Text(r"\textbf{How many terms?} To guarantee error $< E$, find $n$ with $b_{n+1} < E$. For $\sum \frac{(-1)^{n+1}}{n}$ and $E = 0.001$: $\frac{1}{n + 1} < 0.001$, so $n \ge 1000$."),
    BigIdea(r"Error $\le$ first omitted term; its sign tells over or under. Check the AST conditions first."),
    Check(r"Bound the error in using $S_3$ for $\sum \frac{(-1)^{n+1}}{n^3}$.", selfcheck(r"\tfrac{1}{64}"), r"$b_4 = \frac{1}{64}$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Bound the error in using $S_5$ for $\sum_{n=1}^\infty \frac{(-1)^{n+1}}{n}$.", num(sp.Rational(1, 6)), r"$b_6 = \frac16$.", work="1cm"),
    Item(r"Find $S_3$ for $\sum_{n=1}^\infty \frac{(-1)^{n+1}}{2^n}$ and bound the error.", selfcheck(r"S_3 = \tfrac38;\ \text{error} \le \tfrac{1}{16}"), r"$\frac12 - \frac14 + \frac18 = \frac38$; $b_4 = \frac{1}{16}$.", work="1.6cm"),
    Item(r"Is $S_3$ an overestimate or underestimate of $\sum_{n=1}^\infty \frac{(-1)^{n+1}}{n^2}$?", selfcheck(r"\text{overestimate}"), r"The first omitted term, $-\frac{1}{16}$, is negative.", work="1.2cm"),
    Item(r"How many terms of $\sum \frac{(-1)^{n+1}}{n^2}$ guarantee an error less than $0.01$?", num(10), r"$\frac{1}{(n + 1)^2} < 0.01$: $n + 1 > 10$, $n \ge 10$.", work="1.4cm"),
    Item(r"How many terms of $\sum \frac{(-1)^{n}}{n!}$ (from $n = 0$) guarantee an error less than $0.001$?", num(7), r"Need $\frac{1}{(N)!} < 0.001$ for the first omitted term: $7! = 5040$, so terms $n = 0, \ldots, 6$: $7$ terms.", work="1.8cm"),
    Item(r"Use two nonzero terms of $\cos x = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \cdots$ to estimate $\cos 0.2$, and bound the error.", selfcheck(r"0.98;\ \text{error} \le 6.7 \times 10^{-5}"),
         r"$1 - \frac{0.04}{2} = 0.98$; error $\le \frac{0.2^4}{24} \approx 0.0000667$.", work="1.8cm"),
    Item(r"The series $\sum \frac{(-1)^n n}{n^2 + 1}$ satisfies the AST. Bound the error in using $S_4$ (from $n = 1$).", num(sp.Rational(5, 26)), r"$b_5 = \frac{5}{26}$.", work="1.2cm"),
]
same("p", [sp.Rational(1, 2) - sp.Rational(1, 4) + sp.Rational(1, 8), sp.Rational(5, 26)], [sp.Rational(3, 8), sp.Rational(5, 5**2 + 1)])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Bound the error in using $S_9$ for $\sum \frac{(-1)^{n+1}}{n}$.", num(sp.Rational(1, 10)), r"$b_{10}$.", work="1cm"),
        Item(r"Bound the error in using $S_4$ for $\sum \frac{(-1)^{n+1}}{n^3}$.", num(sp.Rational(1, 125)), r"$b_5 = \frac{1}{125}$.", work="1cm"),
        Item(r"Bound the error in using $S_3$ for $\sum \frac{(-1)^{n+1}}{3^n}$.", num(sp.Rational(1, 81)), r"$b_4 = \frac{1}{81}$.", work="1cm"),
    ),
    Variants(
        MCQ(r"For an alternating series satisfying the AST, $S_6$ is an underestimate when", [r"the 6th term is positive", r"the 7th term is positive", r"the 7th term is negative", r"always"], "B", r"The error has the sign of the first omitted term."),
    ),
    Variants(
        Item(r"How many terms of $\sum \frac{(-1)^{n+1}}{n}$ guarantee an error less than $0.05$?", num(20), r"$\frac{1}{n + 1} < 0.05$: $n \ge 20$.", work="1.2cm"),
        Item(r"How many terms of $\sum \frac{(-1)^{n+1}}{\sqrt n}$ guarantee an error less than $0.1$?", num(100), r"$\frac{1}{\sqrt{n + 1}} < 0.1$: $n + 1 > 100$, $n \ge 100$.", work="1.2cm"),
    ),
    Variants(
        MCQ(r"Using $1 - \frac13 + \frac15$ to approximate $\frac\pi4 = 1 - \frac13 + \frac15 - \frac17 + \cdots$ gives an error of at most", [r"$\frac15$", r"$\frac17$", r"$\frac19$", r"$\frac{1}{15}$"], "B", r"The first omitted term."),
    ),
    Variants(
        Item(r"Estimate $\sin 0.1$ with one term of $x - \frac{x^3}{6} + \cdots$ and bound the error.", selfcheck(r"0.1;\ \text{error} \le 1.7 \times 10^{-4}"), r"Error $\le \frac{0.001}{6}$.", work="1.4cm"),
        Item(r"Estimate $e^{-0.1}$ with $1 - 0.1$ and bound the error.", selfcheck(r"0.9;\ \text{error} \le 0.005"), r"Next term $\frac{0.01}{2}$.", work="1.4cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"The sum of $\sum_{n=1}^\infty \frac{(-1)^{n+1}}{n^2}$ is approximated by $S_5$. The error is at most", [r"$\frac{1}{36}$", r"$\frac{1}{25}$", r"$\frac{1}{30}$", r"$\frac{1}{49}$"], "A", r"$b_6 = \frac{1}{36}$.", why_not={"B": "that is the last term used"}),
    MCQ(r"What is the least $n$ such that $S_n$ approximates $\sum_{n=1}^\infty \frac{(-1)^{n+1}}{n^3}$ with error less than $0.001$?", [r"$8$", r"$9$", r"$10$", r"$11$"], "C",
        r"Need $\frac{1}{(n + 1)^3} < 0.001$, so $(n + 1)^3 > 1000$ and $n + 1 \ge 11$: $n = 10$.", why_not={"B": "$n + 1 = 10$ gives exactly $0.001$, not less"}),
    MCQ(r"$S = \sum_{n=1}^\infty \frac{(-1)^{n+1}}{n!}$ and $S_3 = 1 - \frac12 + \frac16 = \frac23$. Which is true?", [r"$S = \frac23$", r"$\frac23 - \frac{1}{24} \le S \le \frac23$", r"$\frac23 \le S \le \frac23 + \frac{1}{24}$", r"$|S - \frac23| \le \frac16$ only"], "B",
        r"The first omitted term is $-\frac{1}{24}$: $S$ lies between $S_3$ and $S_3 - \frac{1}{24}$."),
    MCQ(r"Using $1 - \frac{x^2}{2}$ for $\cos x$ at $x = 0.5$, the alternating series error bound is", [r"$\frac{0.5^2}{2}$", r"$\frac{0.5^3}{6}$", r"$\frac{0.5^6}{720}$", r"$\frac{0.5^4}{24}$"], "D", r"The first omitted term is $\frac{x^4}{4!}$."),
]
same("m", [sp.Rational(1, 6**2), 1 - sp.Rational(1, 2) + sp.Rational(1, 6)], [sp.Rational(1, 36), sp.Rational(2, 3)])

FRQS = []

TOPIC = Topic(
    number="10.10", title="Alternating Series Error Bound",
    unit="Unit 10: Infinite Sequences and Series", ced=["LIM-7.B", "LIM-7.B.1"],
    goals=r"Bound the error of a partial sum of an alternating series, and tell whether it over- or underestimates.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
