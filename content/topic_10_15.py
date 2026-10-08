"""Topic 10.15 (BC): Representing functions as power series.

CED: LIM-8.E/LIM-8.F/LIM-8.G (term-by-term calculus): a power series can be differentiated and integrated term by term with
the same radius; endpoints must be rechecked; new series from the geometric series. Lesson example: ln(1 + x) =
sum (-1)^n x^(n+1)/(n + 1) on (-1, 1]. Worked examples: arctan x on [-1, 1]; 1/(1 - x)^2 = sum n x^(n-1);
sum n/2^n = 2.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, expr, num, same, selfcheck)

x = sp.symbols("x", real=True)
n = sp.symbols("n", integer=True, nonnegative=True)
ser = lambda f, k: sp.series(f, x, 0, k).removeO()

same("lesson", [ser(sp.log(1 + x), 5)], [x - x**2 / 2 + x**3 / 3 - x**4 / 4])
same("ex", [ser(sp.atan(x), 6), ser(1 / (1 - x)**2, 3), sp.summation(n / sp.Integer(2)**n, (n, 1, sp.oo))], [x - x**3 / 3 + x**5 / 5, 1 + 2 * x + 3 * x**2, 2])

NOTES = [
    Video("s10_15.py::Lesson", "Functions as power series", 4),

    Section("Term by term"),
    Formula("Calculus with power series", (r"If $f(x) = \sum c_n (x - a)^n$ for $|x - a| < R$, then \[ f'(x) = \blank{\sum n c_n (x - a)^{n-1}}, \qquad \int f(x)\,dx = C + \blank{\sum \frac{c_n (x - a)^{n+1}}{n + 1}}, \] "
                                           r"both with the same radius $R$. The endpoints can change: check them again.")),
    VideoExample('A series for ln(1 + x)', work="4.6cm"),
    Text(r"\textbf{Useful results.} $\ln(1 + x) = \sum \frac{(-1)^n x^{n+1}}{n + 1}$ on $(-1, 1]$; $\arctan x = \sum \frac{(-1)^n x^{2n+1}}{2n + 1}$ on $[-1, 1]$; $\frac{1}{(1 - x)^2} = \sum n x^{n-1}$ on $(-1, 1)$."),
    BigIdea(r"Start from a known series, differentiate or integrate term by term, fix the constant with a known value, and recheck the endpoints."),
    Check(r"Differentiate $\sum_{n=0}^\infty \frac{x^n}{n!}$ term by term. What do you get?", selfcheck(r"\text{the same series: } (e^x)' = e^x"), r"$\sum \frac{n x^{n-1}}{n!} = \sum \frac{x^{n-1}}{(n - 1)!}$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Find the first four nonzero terms of the Maclaurin series for $\ln(1 - x)$.", expr(ser(sp.log(1 - x), 5)), r"Integrate $-\frac{1}{1 - x} = -\sum x^n$: $-x - \frac{x^2}{2} - \frac{x^3}{3} - \frac{x^4}{4}$.", work="1.6cm"),
    Item(r"Find a power series for $\frac{1}{(1 + x)^2}$.", selfcheck(r"\sum_{n=1}^\infty (-1)^{n+1} n x^{n-1}"), r"$-\frac{d}{dx}\frac{1}{1 + x} = -\frac{d}{dx}\sum (-1)^n x^n$.", work="1.6cm"),
    Item(r"Find the Maclaurin series for $\ln(1 + x^2)$.", selfcheck(r"\sum \frac{(-1)^n x^{2n+2}}{n + 1}"), r"Substitute $x^2$ into the series for $\ln(1 + u)$.", work="1.4cm"),
    Item(r"Find the first three nonzero terms of the Maclaurin series for $\arctan(2x)$.", expr(ser(sp.atan(2 * x), 6)), r"$2x - \frac{8x^3}{3} + \frac{32x^5}{5}$.", work="1.4cm"),
    Item(r"Find $\sum_{n=1}^\infty \frac{n}{3^n}$.", num(sp.summation(n / sp.Integer(3)**n, (n, 1, sp.oo))), r"$\frac{x}{(1 - x)^2}$ at $x = \frac13$: $\frac{1/3}{4/9} = \frac34$.", work="1.6cm"),
    Item(r"Use the series for $\ln(1 + x)$ to write $\ln 2$ as a series.", selfcheck(r"1 - \tfrac12 + \tfrac13 - \tfrac14 + \cdots"), r"$x = 1$ is in the interval $(-1, 1]$.", work="1.2cm"),
    Item(r"Find the Maclaurin series for $\int_0^x e^{-t^2}\,dt$.", selfcheck(r"\sum \frac{(-1)^n x^{2n+1}}{n!(2n + 1)}"), r"Integrate $\sum \frac{(-1)^n t^{2n}}{n!}$.", work="1.6cm"),
    Item(r"Use three terms of the series in the previous problem to approximate $\int_0^{0.5} e^{-t^2}\,dt$.", num(sp.Rational(1, 2) - sp.Rational(1, 24) + sp.Rational(1, 320), tol=1e-5), r"$0.5 - \frac{0.125}{3} + \frac{0.03125}{10} \approx 0.461458$.", work="1.6cm"),
]
same("p", [ser(sp.log(1 - x), 5), ser(sp.atan(2 * x), 6)], [-x - x**2 / 2 - x**3 / 3 - x**4 / 4, 2 * x - sp.Rational(8, 3) * x**3 + sp.Rational(32, 5) * x**5])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"When a power series is integrated term by term, its radius of convergence", [r"doubles", r"stays the same", r"shrinks", r"becomes infinite"], "B", r"Same radius; endpoints may change."),
    ),
    Variants(
        Item(r"Find the first three nonzero terms of the series for $\ln(1 + 2x)$.", expr(ser(sp.log(1 + 2 * x), 4)), r"$2x - 2x^2 + \frac83x^3$.", work="1.4cm"),
        Item(r"Find the first three nonzero terms of the series for $\arctan(x^2)$.", expr(ser(sp.atan(x**2), 11)), r"$x^2 - \frac{x^6}{3} + \frac{x^{10}}{5}$.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"The interval of convergence of $\sum \frac{(-1)^n x^{n+1}}{n + 1}$ is", [r"$(-1, 1)$", r"$[-1, 1)$", r"$(-1, 1]$", r"$[-1, 1]$"], "C", r"It's $\ln(1 + x)$: $x = 1$ converges, $x = -1$ diverges."),
        MCQ(r"The interval of convergence of $\sum \frac{(-1)^n x^{2n+1}}{2n + 1}$ is", [r"$(-1, 1)$", r"$[-1, 1)$", r"$(-1, 1]$", r"$[-1, 1]$"], "D", r"It's $\arctan x$: both endpoints converge (AST)."),
    ),
    Variants(
        Item(r"Find $\sum_{n=1}^\infty n\left(\frac14\right)^{n-1}$.", num(sp.Rational(16, 9)), r"$\frac{1}{(1 - 1/4)^2} = \frac{16}{9}$.", work="1.2cm"),
        Item(r"Find $\sum_{n=1}^\infty \frac{n}{4^n}$.", num(sp.Rational(4, 9)), r"$\frac{1/4}{(3/4)^2}$.", work="1.2cm"),
    ),
    Variants(
        MCQ(r"Differentiating $\sum_{n=0}^\infty x^n$ term by term gives a series for", [r"$\ln(1 - x)$", r"$\frac{1}{(1 - x)^2}$", r"$\frac{1}{1 - x^2}$", r"$-\frac{1}{(1 - x)^2}$"], "B", r"$\frac{d}{dx}\frac{1}{1 - x}$."),
    ),
]

# ---------------------------------------------------------------- test prep
_m4 = float(sp.Rational(1, 2) - sp.Rational(1, 24) + sp.Rational(1, 320))
MCQS = [
    MCQ(r"The Maclaurin series for $\ln(1 + x)$ is", [r"$\sum \frac{(-1)^n x^{n+1}}{n + 1}$", r"$\sum \frac{x^{n+1}}{n + 1}$", r"$\sum (-1)^n x^n$", r"$\sum \frac{(-1)^n x^n}{n!}$"], "A", r"Integrate $\frac{1}{1 + x}$."),
    MCQ(r"Which series converges to $\frac\pi4$?", [r"$1 + \frac13 + \frac15 + \cdots$", r"$1 - \frac12 + \frac13 - \cdots$", r"$1 - \frac13 + \frac15 - \frac17 + \cdots$", r"$1 - \frac{1}{3!} + \frac{1}{5!} - \cdots$"], "C", r"$\arctan 1$.", why_not={"B": "that is $\\ln 2$", "D": "that is $\\sin 1$"}),
    MCQ(r"$\sum_{n=1}^\infty n x^{n-1}$ converges to $\frac{1}{(1 - x)^2}$ for", [r"all $x$", r"$-1 \le x \le 1$", r"$-1 \le x < 1$", r"$-1 < x < 1$"], "D", r"Same radius as $\sum x^n$; both endpoints diverge (terms don't go to $0$)."),
    MCQ(r"Using three nonzero terms of the series for $\int_0^x e^{-t^2}\,dt$, the approximation of $\int_0^{0.5} e^{-t^2}\,dt$ is", [r"$0.500$", rf"${_m4:.4f}$", r"$0.4583$", r"$0.4794$"], "B", rf"$0.5 - \frac{{0.5^3}}{{3}} + \frac{{0.5^5}}{{10}} \approx {_m4:.4f}$."),
]
same("m", [ser(sp.log(1 + x), 4)], [x - x**2 / 2 + x**3 / 3])

FRQS = []

TOPIC = Topic(
    number="10.15", title="Representing Functions as Power Series",
    unit="Unit 10: Infinite Sequences and Series", ced=["LIM-8.F", "LIM-8.F.1", "LIM-8.G.1"],
    goals=r"Differentiate and integrate power series term by term to represent functions and find sums.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
