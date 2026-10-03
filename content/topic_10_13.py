"""Topic 10.13 (BC): Radius and interval of convergence of power series.

CED: LIM-8.C (LIM-8.C.1, LIM-8.C.2): a power series sum c_n (x - a)^n converges absolutely for |x - a| < R and diverges for
|x - a| > R; R may be 0 or infinity; endpoints are checked separately. Lesson example: (x - 2)^n/(n 3^n): R = 3,
interval [-1, 5). Worked examples: x^n/n! (R = oo); n! x^n (R = 0); x^n/n^2 ([-1, 1]).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)

n = sp.symbols("n", positive=True, integer=True)


def radius(c):
    """R = 1/lim |c_(n+1)/c_n|."""
    L = sp.limit(sp.Abs(sp.combsimp(c.subs(n, n + 1) / c)), n, sp.oo)
    return sp.oo if L == 0 else (0 if L == sp.oo else 1 / L)


same("lesson", [radius(1 / (n * 3**n))], [3])
same("ex", [radius(1 / sp.factorial(n)), radius(sp.factorial(n)), radius(1 / n**2)], [sp.oo, 0, 1])

NOTES = [
    Video("s10_13.py::Lesson", "Radius and interval of convergence", 4),

    Section("Radius and interval"),
    Formula("Radius of convergence", (r"A power series $\sum c_n (x - a)^n$ has a radius $R$: it converges \blank{absolutely} for $|x - a| < R$ and \blank{diverges} for $|x - a| > R$. "
                                      r"$R$ may be $0$ (only $x = a$) or $\infty$ (all $x$). The endpoints $x = a \pm R$ must be \blank{checked separately}.")),
    Text(r"\textbf{Method.} Apply the ratio test to $|a_{n+1}/a_n|$ with $x$ in it; $L < 1$ gives $|x - a| < R$. Then substitute each endpoint and test the resulting number series (often a $p$-series or alternating series)."),
    VideoExample('Finding the interval', work="4.6cm"),
    BigIdea(r"Ratio test for the radius; separate tests for the endpoints."),
    Check(r"Find the radius of convergence of $\sum \frac{x^n}{2^n}$.", selfcheck(r"R = 2"), r"Geometric with ratio $\frac x2$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Find the radius of convergence of $\sum \frac{x^n}{5^n}$.", num(radius(1 / sp.Integer(5)**n)), r"$|x| < 5$.", work="1.2cm"),
    Item(r"Find the interval of convergence of $\sum \frac{x^n}{n}$.", selfcheck(r"[-1, 1)"), r"$R = 1$; $x = 1$: harmonic diverges; $x = -1$: AST converges.", work="1.8cm"),
    Item(r"Find the interval of convergence of $\sum \frac{(x - 3)^n}{n^2}$.", selfcheck(r"[2, 4]"), r"$R = 1$; both endpoints give $p = 2$ series (absolutely convergent).", work="1.8cm"),
    Item(r"Find the radius of convergence of $\sum \frac{n x^n}{4^n}$.", num(radius(n / sp.Integer(4)**n)), r"$L = \frac{|x|}{4}$: $R = 4$.", work="1.4cm"),
    Item(r"Find the interval of convergence of $\sum \frac{(x + 1)^n}{\sqrt n}$.", selfcheck(r"[-2, 0)"), r"$R = 1$; $x = 0$: $\sum \frac{1}{\sqrt n}$ diverges; $x = -2$: $\sum \frac{(-1)^n}{\sqrt n}$ converges.", work="2cm"),
    Item(r"Find the radius of convergence of $\sum \frac{(2x)^n}{n!}$.", selfcheck(r"\infty"), r"$\frac{2|x|}{n + 1} \to 0$.", work="1.2cm"),
    Item(r"Find the interval of convergence of $\sum \frac{(x - 1)^n}{n \cdot 2^n}$.", selfcheck(r"[-1, 3)"), r"$R = 2$; $x = 3$: harmonic; $x = -1$: AST.", work="2cm"),
    Item(r"Find the interval of convergence of $\sum n(x - 5)^n$.", selfcheck(r"(4, 6)"), r"$R = 1$; at both endpoints the terms don't go to $0$.", work="1.6cm"),
]
same("p", [radius(1 / n), radius(n), radius(1 / (n * 2**n)), radius(2**n / sp.factorial(n))], [1, 1, 2, sp.oo])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find the radius of convergence of $\sum \frac{x^n}{3^n}$.", num(3), r"$|x| < 3$.", work="1cm"),
        Item(r"Find the radius of convergence of $\sum \frac{x^n}{n \cdot 6^n}$.", num(6), r"$R = 6$.", work="1cm"),
        Item(r"Find the radius of convergence of $\sum 2^n x^n$.", num(sp.Rational(1, 2)), r"$|2x| < 1$.", work="1cm"),
    ),
    Variants(
        MCQ(r"A power series centered at $2$ has radius $3$. At which $x$ must it converge?", [r"$x = 5$", r"$x = -1$", r"$x = 4$", r"$x = 6$"], "C", r"$|4 - 2| < 3$; endpoints are uncertain.", why_not={"A": "an endpoint: unknown"}),
        MCQ(r"A power series centered at $0$ has radius $4$. At which $x$ must it diverge?", [r"$x = 4$", r"$x = -5$", r"$x = 3$", r"$x = -4$"], "B", r"$|-5| > 4$."),
    ),
    Variants(
        Item(r"Find the interval of convergence of $\sum \frac{(-1)^n x^n}{n}$.", selfcheck(r"(-1, 1]"), r"$x = 1$: AST; $x = -1$: harmonic.", work="1.8cm"),
        Item(r"Find the interval of convergence of $\sum \frac{x^n}{n^3}$.", selfcheck(r"[-1, 1]"), r"$p = 3$ at both ends.", work="1.8cm"),
    ),
    Variants(
        MCQ(r"The interval of convergence of $\sum x^n$ is", [r"$[-1, 1]$", r"$[-1, 1)$", r"$(-1, 1]$", r"$(-1, 1)$"], "D", r"At $x = \pm1$ the terms don't go to $0$."),
    ),
    Variants(
        Item(r"Find the radius of convergence of $\sum \frac{n!\,x^n}{10^n}$.", num(0), r"$\frac{(n + 1)|x|}{10} \to \infty$ unless $x = 0$.", work="1.2cm"),
        Item(r"Find the radius of convergence of $\sum \frac{x^{n}}{(2n)!}$.", selfcheck(r"\infty"), r"Ratio $\frac{|x|}{(2n + 2)(2n + 1)} \to 0$.", work="1.2cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"The interval of convergence of $\sum_{n=1}^\infty \frac{(x - 4)^n}{n}$ is", [r"$[3, 5)$", r"$(3, 5]$", r"$[3, 5]$", r"$(3, 5)$"], "A", r"$x = 5$: harmonic diverges; $x = 3$: AST converges."),
    MCQ(r"The radius of convergence of $\sum_{n=0}^\infty \frac{n^2 x^n}{3^{n}}$ is", [r"$1$", r"$\frac13$", r"$9$", r"$3$"], "D", r"$L = \frac{|x|}{3}$."),
    MCQ(r"For which $x$ does $\sum_{n=1}^\infty \frac{(x + 2)^n}{n^2 \cdot 2^n}$ converge?", [r"$-4 < x < 0$", r"$-4 \le x \le 0$", r"$-4 \le x < 0$", r"$-1 \le x \le 1$"], "B", r"$R = 2$ about $-2$; both endpoints give $\sum \frac{(\pm1)^n}{n^2}$, convergent."),
    MCQ(r"If $\sum c_n x^n$ converges at $x = -3$ and diverges at $x = 5$, which must be true?", [r"it converges at $x = 4$", r"it converges at $x = 2$", r"it diverges at $x = -4$", r"$R = 4$"], "B", r"$R \ge 3$ and $R \le 5$; $|2| < 3$."),
]
same("m", [radius(1 / n), radius(n**2 / sp.Integer(3)**n), radius(1 / (n**2 * 2**n))], [1, 3, 2])

FRQS = []

TOPIC = Topic(
    number="10.13", title="Radius and Interval of Convergence of Power Series",
    unit="Unit 10: Infinite Sequences and Series", ced=["LIM-8.C", "LIM-8.C.1", "LIM-8.C.2"],
    goals=r"Find the radius and interval of convergence of a power series, checking endpoints separately.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
