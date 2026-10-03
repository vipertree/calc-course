"""Topic 10.14 (BC): Finding Taylor or Maclaurin series for a function.

CED: LIM-8.D (LIM-8.D.1, LIM-8.D.2): the Taylor series sum f^(n)(a)/n! (x - a)^n; the Maclaurin series for e^x, sin x,
cos x (all x) and 1/(1 - x) (|x| < 1); new series by substitution and multiplication. Lesson example: e^(-x^2) =
sum (-1)^n x^(2n)/n!. Worked examples: x cos x; sin 3x; e^x about 1.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Table, Text, Topic, Variants, Video, close, expr, num, same, selfcheck)

x = sp.symbols("x", real=True)
ser = lambda f, k: sp.series(f, x, 0, k).removeO()

same("lesson", [ser(sp.exp(-x**2), 8)], [1 - x**2 + x**4 / 2 - x**6 / 6])
same("ex", [ser(x * sp.cos(x), 6), ser(sp.sin(3 * x), 6)], [x - x**3 / 2 + x**5 / 24, 3 * x - sp.Rational(9, 2) * x**3 + sp.Rational(81, 40) * x**5])

NOTES = [
    Video("s10_14.py::Lesson", "Taylor and Maclaurin series", 4),

    Section("Four series to know"),
    Table(r"$e^x$ & $1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots$ & $\sum \frac{x^n}{n!}$ & all $x$ \\ "
          r"$\sin x$ & $x - \frac{x^3}{3!} + \frac{x^5}{5!} - \cdots$ & $\mblank{\sum \frac{(-1)^n x^{2n+1}}{(2n + 1)!}}$ & all $x$ \\ "
          r"$\cos x$ & $1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \cdots$ & $\mblank{\sum \frac{(-1)^n x^{2n}}{(2n)!}}$ & all $x$ \\ "
          r"$\frac{1}{1 - x}$ & $1 + x + x^2 + \cdots$ & $\sum x^n$ & $\mblank{-1 < x < 1}$ \\", "llll", header=r"function & series & general term & interval"),
    Text(r"Memory tips: sine has the odd powers and starts with $x$; cosine has the even powers and starts with $1$; both alternate. $e^x$ has every power, all positive."),
    Formula("Taylor series", (r"\[ f(x) = \sum_{n=0}^\infty \blank{\frac{f^{(n)}(a)}{n!}}(x - a)^n \] (Maclaurin when $a = 0$), wherever the series converges to $f$.")),
    VideoExample('New series from old', work="4cm"),
    Text(r"\textbf{Building new series.} Substitute ($u = -x^2$, $u = 3x$), multiply by powers of $x$, or differentiate and integrate term by term (10.15). Substitution keeps the interval in terms of $u$."),
    BigIdea(r"Start from a known series and transform it, instead of taking many derivatives."),
    Check(r"Write the Maclaurin series for $e^{2x}$.", selfcheck(r"\sum \frac{2^n x^n}{n!}"), r"Substitute $u = 2x$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Find the first four nonzero terms of the Maclaurin series for $e^{3x}$.", expr(ser(sp.exp(3 * x), 4)), r"$1 + 3x + \frac92x^2 + \frac92x^3$.", work="1.4cm"),
    Item(r"Find the first three nonzero terms of the Maclaurin series for $\cos(x^2)$.", expr(ser(sp.cos(x**2), 9)), r"$1 - \frac{x^4}{2} + \frac{x^8}{24}$.", work="1.4cm"),
    Item(r"Find the Maclaurin series for $\frac{1}{1 + x}$ and its interval.", selfcheck(r"\sum (-1)^n x^n,\ -1 < x < 1"), r"Substitute $-x$ into $\frac{1}{1 - u}$.", work="1.4cm"),
    Item(r"Find the Maclaurin series for $\frac{1}{1 - x^2}$.", selfcheck(r"\sum x^{2n},\ -1 < x < 1"), r"$u = x^2$.", work="1.2cm"),
    Item(r"Find the first three nonzero terms of the Maclaurin series for $x^2 e^{x}$.", expr(ser(x**2 * sp.exp(x), 5)), r"$x^2 + x^3 + \frac{x^4}{2}$.", work="1.4cm"),
    Item(r"Write the general term of the Maclaurin series for $\sin(x^2)$.", selfcheck(r"\frac{(-1)^n x^{4n+2}}{(2n + 1)!}"), r"$(x^2)^{2n+1} = x^{4n+2}$.", work="1.2cm"),
    Item(r"Find the Taylor series for $\frac1x$ about $x = 1$.", selfcheck(r"\sum (-1)^n (x - 1)^n"), r"$\frac1x = \frac{1}{1 + (x - 1)}$.", work="1.4cm"),
    Item(r"The Maclaurin series of $f$ is $\sum_{n=0}^\infty \frac{(n + 1)x^n}{3^n}$. Find $f'''(0)$.", num(sp.Rational(4 * 6, 27)), r"$f'''(0) = 3!\,c_3 = 6 \cdot \frac{4}{27} = \frac{8}{9}$.", work="1.4cm"),
]
same("p", [ser(sp.exp(3 * x), 4), ser(sp.cos(x**2), 9), ser(x**2 * sp.exp(x), 5), sp.Rational(4 * 6, 27)], [1 + 3 * x + sp.Rational(9, 2) * x**2 + sp.Rational(9, 2) * x**3, 1 - x**4 / 2 + x**8 / 24, x**2 + x**3 + x**4 / 2, sp.Rational(8, 9)])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"The Maclaurin series for $\cos x$ is", [r"$\sum \frac{(-1)^n x^{2n+1}}{(2n + 1)!}$", r"$\sum \frac{x^n}{n!}$", r"$\sum \frac{(-1)^n x^{2n}}{(2n)!}$", r"$\sum (-1)^n x^n$"], "C", r"Even powers, alternating, even factorials."),
        MCQ(r"The Maclaurin series for $\sin x$ is", [r"$\sum \frac{(-1)^n x^{2n+1}}{(2n + 1)!}$", r"$\sum \frac{(-1)^n x^{2n}}{(2n)!}$", r"$\sum \frac{x^{2n+1}}{(2n + 1)!}$", r"$\sum \frac{(-1)^n x^n}{n!}$"], "A", r"Odd powers, alternating."),
    ),
    Variants(
        Item(r"Find the first three nonzero terms of the Maclaurin series for $e^{-x}$.", expr(ser(sp.exp(-x), 3)), r"$1 - x + \frac{x^2}{2}$.", work="1.2cm"),
        Item(r"Find the first three nonzero terms of the Maclaurin series for $\sin(2x)$.", expr(ser(sp.sin(2 * x), 6)), r"$2x - \frac43x^3 + \frac{4}{15}x^5$.", work="1.2cm"),
    ),
    Variants(
        MCQ(r"The interval of convergence of the Maclaurin series for $\frac{1}{1 - 2x}$ is", [r"$-1 < x < 1$", r"$-\frac12 < x < \frac12$", r"$-2 < x < 2$", r"all $x$"], "B", r"$|2x| < 1$."),
    ),
    Variants(
        Item(r"Find the general term of the Maclaurin series for $x e^{x^2}$.", selfcheck(r"\frac{x^{2n+1}}{n!}"), r"$x \cdot \frac{(x^2)^n}{n!}$.", work="1.2cm"),
        Item(r"Find the general term of the Maclaurin series for $\frac{x}{1 + x^2}$.", selfcheck(r"(-1)^n x^{2n+1}"), r"$x\sum (-x^2)^n$.", work="1.2cm"),
    ),
    Variants(
        MCQ(r"The coefficient of $x^4$ in the Maclaurin series for $\cos(3x)$ is", [r"$\frac{3}{8}$", r"$\frac{81}{4}$", r"$\frac{27}{8}$", r"$-\frac{27}{8}$"], "C", r"$\frac{(3x)^4}{4!} = \frac{81x^4}{24} = \frac{27}{8}x^4$.", why_not={"B": "divided by $4$ instead of $4!$"}),
    ),
]
same("q", [ser(sp.cos(3 * x), 5).coeff(x, 4)], [sp.Rational(27, 8)])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"The Maclaurin series for $\frac{1}{1 + x^2}$ is", [r"$\sum (-1)^n x^{2n}$", r"$\sum x^{2n}$", r"$\sum (-1)^n x^n$", r"$\sum \frac{(-1)^n x^{2n}}{n!}$"], "A", r"Substitute $u = -x^2$ into $\frac{1}{1 - u}$."),
    MCQ(r"The third nonzero term of the Maclaurin series for $x\sin x$ is", [r"$\frac{x^4}{6}$", r"$-\frac{x^4}{6}$", r"$\frac{x^6}{120}$", r"$\frac{x^5}{120}$"], "C", r"$x\left(x - \frac{x^3}{6} + \frac{x^5}{120}\right)$."),
    MCQ(r"Which is the Taylor series for $\cos x$ about $x = \pi$?", [r"$\sum \frac{(-1)^n (x - \pi)^{2n}}{(2n)!}$", r"$\sum \frac{(-1)^{n+1} (x - \pi)^{2n}}{(2n)!}$", r"$\sum \frac{(x - \pi)^{2n}}{(2n)!}$", r"$\sum \frac{(-1)^{n} (x - \pi)^{2n+1}}{(2n + 1)!}$"], "B", r"$\cos x = -\cos(x - \pi)$."),
    MCQ(r"If $f(x) = \sum_{n=0}^\infty \frac{x^n}{2^n n!}$, then $f(x) = $", [r"$e^{2x}$", r"$2e^x$", r"$\frac{1}{1 - x/2}$", r"$e^{x/2}$"], "D", r"$\sum \frac{(x/2)^n}{n!}$."),
]
same("m", [ser(1 / (1 + x**2), 6), ser(x * sp.sin(x), 7)], [1 - x**2 + x**4, x**2 - x**4 / 6 + x**6 / 120])

# ---------------------------------------------------------------- FRQ
g = sp.sin(x) / x
same("frq", [ser(g, 6), sp.integrate(1 - x**2 / 6, (x, 0, 1)), sp.integrate(x**4 / 120, (x, 0, 1))], [1 - x**2 / 6 + x**4 / 120, sp.Rational(17, 18), sp.Rational(1, 600)])
FRQS = [
    FRQ("A Maclaurin series", (r"Let $g(x) = \frac{\sin x}{x}$ for $x \ne 0$ and $g(0) = 1$."), [
        Part("a", r"Write the first three nonzero terms and the general term of the Maclaurin series for $g$.", selfcheck(r"1 - \frac{x^2}{6} + \frac{x^4}{120} - \cdots;\ \frac{(-1)^n x^{2n}}{(2n + 1)!}"),
             r"Divide the sine series by $x$: $1 - \frac{x^2}{3!} + \frac{x^4}{5!} - \cdots$, general term $\frac{(-1)^n x^{2n}}{(2n + 1)!}$.", [(1, "terms"), (1, "general term")], work="2.2cm"),
        Part("b", r"Find the interval of convergence of the series in part (a). Justify your answer.", selfcheck(r"\text{all real } x"),
             r"Ratio test: $\left|\frac{x^{2n+2}}{(2n + 3)!}\cdot\frac{(2n + 1)!}{x^{2n}}\right| = \frac{x^2}{(2n + 3)(2n + 2)} \to 0 < 1$ for every $x$. The series converges for all $x$.", [(1, "ratio test"), (1, "conclusion")], work="2.4cm"),
        Part("c", r"Use the first two nonzero terms of the series to approximate $\displaystyle\int_0^1 g(x)\,dx$.", num(sp.Rational(17, 18)), r"$\int_0^1 \left(1 - \frac{x^2}{6}\right) dx = 1 - \frac{1}{18} = \frac{17}{18}$.", [(1, "integral of the terms"), (1, "answer")], work="2cm"),
        Part("d", r"Show that the approximation in part (c) differs from $\displaystyle\int_0^1 g(x)\,dx$ by less than $\frac{1}{500}$.", selfcheck(r"\tfrac{1}{600} < \tfrac{1}{500}"),
             r"$\int_0^1 g(x)\,dx = 1 - \frac{1}{18} + \frac{1}{600} - \cdots$ is alternating with terms decreasing to $0$, so the error is at most the first omitted term, $\frac{1}{600} < \frac{1}{500}$.",
             [(1, "alternating series error bound"), (1, "value and comparison")], work="2.2cm"),
    ], frq_type="Taylor series"),
]

TOPIC = Topic(
    number="10.14", title="Finding Taylor or Maclaurin Series for a Function",
    unit="Unit 10: Infinite Sequences and Series", ced=["LIM-8.D", "LIM-8.D.1", "LIM-8.D.2"],
    goals=r"Write Taylor and Maclaurin series, using the four basic series and substitution or multiplication.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
