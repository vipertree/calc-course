"""Topic 10.2 (BC): Working with geometric series.

CED: LIM-7.A (LIM-7.A.3, LIM-7.A.4): a + ar + ar^2 + ... has S_n = a(1 - r^n)/(1 - r); it converges to a/(1 - r) when
|r| < 1 and diverges when |r| >= 1; a is the first term actually in the sum. Lesson example: sum from 0 of 3(2/5)^n = 5.
Worked examples: sum from 1 of (-1/3)^n = -1/4; 2(3/2)^n diverges; 0.777... = 7/9.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)

n = sp.symbols("n", integer=True, nonnegative=True)


def gsum(a_n, start):
    return sp.simplify(sp.summation(a_n, (n, start, sp.oo)))


same("lesson", [gsum(3 * sp.Rational(2, 5)**n, 0)], [5])
same("ex", [gsum(sp.Rational(-1, 3)**n, 1), gsum(sp.Rational(7, 10) * sp.Rational(1, 10)**n, 0)], [-sp.Rational(1, 4), sp.Rational(7, 9)])

NOTES = [
    Video("s10_2.py::Lesson", "Geometric series", 4),

    Section("Partial sums"),
    Text(r"A geometric series has first term $a$ and ratio $r$: $a + ar + ar^2 + \cdots$. Subtracting $rS_n$ from $S_n$ cancels everything but $a - ar^n$."),
    Formula("Geometric partial sum", (r"\[ S_n = a + ar + \cdots + ar^{n-1} = \blank{\frac{a\left(1 - r^n\right)}{1 - r}} \quad (r \ne 1). \]")),
    Formula("Geometric series", (r"\[ a + ar + ar^2 + \cdots = \blank{\frac{a}{1 - r}} \ \text{ if } |r| < 1, \] and the series \blank{diverges} if $|r| \ge 1$. In words: first term over one minus the ratio.")),
    VideoExample('Summing a geometric series', work="3cm"),
    Text(r"\textbf{Starting index.} $a$ is the first term in the sum: $\sum_{n=1}^\infty \left(\frac12\right)^n = 1$ but $\sum_{n=0}^\infty \left(\frac12\right)^n = 2$."),
    BigIdea(r"Geometric: converges iff $|r| < 1$, to $\frac{\text{first term}}{1 - r}$."),
    Check(r"Find $\sum_{n=0}^\infty 4\left(\frac14\right)^n$.", selfcheck(r"\tfrac{16}{3}"), r"$\frac{4}{1 - 1/4}$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Find $\sum_{n=0}^\infty \left(\frac13\right)^n$.", num(gsum(sp.Rational(1, 3)**n, 0)), r"$\frac{1}{1 - 1/3} = \frac32$.", work="1.2cm"),
    Item(r"Find $\sum_{n=1}^\infty 5\left(\frac25\right)^n$.", num(gsum(5 * sp.Rational(2, 5)**n, 1)), r"$a = 2$, $r = \frac25$: $\frac{2}{3/5} = \frac{10}{3}$.", work="1.4cm"),
    Item(r"Find $\sum_{n=0}^\infty \frac{(-1)^n}{2^n}$.", num(gsum((-sp.Rational(1, 2))**n, 0)), r"$\frac{1}{1 + 1/2} = \frac23$.", work="1.2cm"),
    Item(r"Does $\sum_{n=0}^\infty \left(\frac{5}{4}\right)^n$ converge?", selfcheck(r"\text{diverges}"), r"$|r| = \frac54 \ge 1$.", work="1cm"),
    Item(r"Find $\sum_{n=2}^\infty \frac{3}{4^n}$.", num(gsum(3 / sp.Integer(4)**n, 2)), r"$a = \frac{3}{16}$, $r = \frac14$: $\frac{3/16}{3/4} = \frac14$.", work="1.4cm"),
    Item(r"Write $0.\overline{36} = 0.363636\ldots$ as a fraction.", num(sp.Rational(4, 11)), r"$\frac{36/100}{1 - 1/100} = \frac{36}{99} = \frac{4}{11}$.", work="1.4cm"),
    Item(r"For which $x$ does $\sum_{n=0}^\infty (2x)^n$ converge?", selfcheck(r"-\tfrac12 < x < \tfrac12"), r"$|2x| < 1$.", work="1.2cm"),
    Item(r"Find the sum $\sum_{n=0}^\infty x^n$ in terms of $x$, for $|x| < 1$.", selfcheck(r"\frac{1}{1 - x}"), r"$a = 1$, $r = x$.", work="1cm"),
    Item(r"A ball is dropped from $10$ ft and each bounce reaches $60\%$ of the previous height. Find the total vertical distance traveled.", num(40),
         r"Down $10$, then up and down each bounce: $10 + 2\sum_{k=1}^\infty 10(0.6)^k = 10 + 2 \cdot \frac{6}{0.4} = 40$ ft.", work="2cm"),
    Item(r"Find $\sum_{n=1}^\infty \frac{2^{n} + 3^{n}}{6^{n}}$.", num(gsum(sp.Rational(1, 3)**n, 1) + gsum(sp.Rational(1, 2)**n, 1)), r"$\sum \left(\frac13\right)^n + \sum \left(\frac12\right)^n = \frac12 + 1 = \frac32$.", work="1.8cm"),
]
same("p", [10 + 2 * gsum(10 * sp.Rational(3, 5)**n, 1)], [40])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find $\sum_{n=0}^\infty 6\left(\frac12\right)^n$.", num(12), r"$\frac{6}{1/2}$.", work="1cm"),
        Item(r"Find $\sum_{n=0}^\infty 2\left(\frac34\right)^n$.", num(8), r"$\frac{2}{1/4}$.", work="1cm"),
        Item(r"Find $\sum_{n=0}^\infty 9\left(-\frac12\right)^n$.", num(6), r"$\frac{9}{3/2}$.", work="1cm"),
    ),
    Variants(
        Item(r"Find $\sum_{n=1}^\infty \left(\frac23\right)^n$.", num(2), r"$a = \frac23$: $\frac{2/3}{1/3}$.", work="1.2cm"),
        Item(r"Find $\sum_{n=3}^\infty \left(\frac12\right)^n$.", num(sp.Rational(1, 4)), r"$a = \frac18$: $\frac{1/8}{1/2}$.", work="1.2cm"),
    ),
    Variants(
        MCQ(r"Which geometric series converges?", [r"$\sum 3^n$", r"$\sum \left(-\frac43\right)^n$", r"$\sum \left(-\frac34\right)^n$", r"$\sum 1^n$"], "C", r"Only $|r| = \frac34 < 1$."),
        MCQ(r"Which geometric series diverges?", [r"$\sum \left(\frac{1}{e}\right)^n$", r"$\sum \left(\frac{\pi}{3}\right)^n$", r"$\sum \left(-\frac12\right)^n$", r"$\sum 0.99^n$"], "B", r"$\frac\pi3 > 1$."),
    ),
    Variants(
        Item(r"Write $0.\overline{5}$ as a fraction.", num(sp.Rational(5, 9)), r"$\frac{5/10}{9/10}$.", work="1.2cm"),
        Item(r"Write $0.\overline{12}$ as a fraction.", num(sp.Rational(4, 33)), r"$\frac{12}{99}$.", work="1.2cm"),
    ),
    Variants(
        Item(r"For which $x$ does $\sum_{n=0}^\infty \left(\frac{x}{3}\right)^n$ converge, and to what?", selfcheck(r"-3 < x < 3;\ \frac{3}{3 - x}"), r"$\left|\frac x3\right| < 1$; sum $\frac{1}{1 - x/3}$.", work="1.6cm"),
        Item(r"For which $x$ does $\sum_{n=0}^\infty (x - 1)^n$ converge, and to what?", selfcheck(r"0 < x < 2;\ \frac{1}{2 - x}"), r"$|x - 1| < 1$; sum $\frac{1}{1 - (x - 1)}$.", work="1.6cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$\displaystyle\sum_{n=1}^\infty 4\left(-\frac13\right)^{n} = $", [r"$-1$", r"$3$", r"$-\frac43$", r"$6$"], "A", r"$a = -\frac43$, $r = -\frac13$: $\frac{-4/3}{4/3} = -1$.", why_not={"B": "started at $n = 0$"}),
    MCQ(r"If $\sum_{n=0}^\infty a r^n = 6$ and $a = 2$, then $r = $", [r"$\frac13$", r"$\frac23$", r"$3$", r"$\frac12$"], "B", r"$\frac{2}{1 - r} = 6$."),
    MCQ(r"$\displaystyle\sum_{n=0}^\infty \frac{3^{n+1}}{5^n} = $", [r"$\frac52$", r"$\frac{15}{2}$", r"$3$", r"divergent"], "B", r"$a = 3$, $r = \frac35$: $\frac{3}{2/5}$."),
    MCQ(r"For what values of $x$ does $\sum_{n=0}^\infty \left(\frac{2}{x}\right)^n$ converge?", [r"$|x| < 2$", r"$x > 2$ only", r"$-2 < x < 2,\ x \ne 0$", r"$|x| > 2$"], "D", r"$\left|\frac2x\right| < 1$ iff $|x| > 2$."),
]
same("m", [gsum(4 * sp.Rational(-1, 3)**n, 1), gsum(3 * sp.Rational(3, 5)**n, 0)], [-1, sp.Rational(15, 2)])

FRQS = []

TOPIC = Topic(
    number="10.2", title="Working with Geometric Series",
    unit="Unit 10: Infinite Sequences and Series", ced=["LIM-7.A", "LIM-7.A.3", "LIM-7.A.4"],
    goals=r"Decide whether a geometric series converges and find its sum.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
