"""Topic 10.11 (BC): Finding Taylor polynomial approximations of functions.

CED: LIM-8.A (LIM-8.A.1, LIM-8.A.2): P_n(x) = sum_{k=0}^n f^(k)(a)/k! (x - a)^k matches f and its first n derivatives at a;
Maclaurin when a = 0; the coefficient of (x - a)^k is f^(k)(a)/k!. Lesson example: P_3 for ln x at 1, ln 1.2 ~ 0.182667.
Worked examples: e^x (e^0.1 ~ 1.105167); cos x degree 4; a polynomial from a table of derivative values (f(2.1) ~ 2.921).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Table, Text, Topic, Variants, Video, close, expr, num, same, selfcheck)

x = sp.symbols("x", real=True)


def taylor(f, a, nn):
    return sp.expand(sum(sp.diff(f, x, k).subs(x, a) / sp.factorial(k) * (x - a)**k for k in range(nn + 1)))


same("lesson", [sp.expand(taylor(sp.log(x), 1, 3) - ((x - 1) - (x - 1)**2 / 2 + (x - 1)**3 / 3))], [0])
close("lesson value", float(taylor(sp.log(x), 1, 3).subs(x, sp.Rational(6, 5))), 0.182667, 1e-6)
same("ex", [taylor(sp.exp(x), 0, 3), taylor(sp.cos(x), 0, 4)], [1 + x + x**2 / 2 + x**3 / 6, 1 - x**2 / 2 + x**4 / 24])
P3 = 3 - (x - 2) + 2 * (x - 2)**2 + (x - 2)**3
same("ex3", [P3.subs(x, sp.Rational(21, 10))], [sp.Rational(2921, 1000)])

NOTES = [
    Video("s10_11.py::Lesson", "Taylor polynomials", 5),

    Section("Matching derivatives"),
    Text(r"The tangent line matches $f$'s value and slope at $a$. A Taylor polynomial of degree $n$ also matches the second, third, ..., $n$th derivatives, so it stays close to $f$ over a wider range."),
    Formula("Taylor polynomial", (r"\[ P_n(x) = f(a) + f'(a)(x - a) + \frac{f''(a)}{2!}(x - a)^2 + \cdots + \frac{f^{(n)}(a)}{n!}(x - a)^n. \] "
                                  r"The coefficient of $(x - a)^k$ is \blank{$\frac{f^{(k)}(a)}{k!}$}. With $a = 0$ it is a \blank{Maclaurin} polynomial.")),
    VideoExample('ln x near 1', work="4.6cm"),
    Text(r"\textbf{Reading derivatives from a polynomial.} If $P(x) = \sum c_k (x - a)^k$ is the Taylor polynomial, then $f^{(k)}(a) = k!\,c_k$."),
    BigIdea(r"Table of derivatives at the center, divide by $k!$: those are the coefficients."),
    Check(r"Find the second-degree Maclaurin polynomial for $\frac{1}{1 - x}$.", selfcheck(r"1 + x + x^2"), r"$f(0) = 1$, $f'(0) = 1$, $f''(0) = 2$; divide by $k!$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Find the third-degree Maclaurin polynomial for $\sin x$.", expr(taylor(sp.sin(x), 0, 3)), r"$x - \frac{x^3}{6}$.", work="1.6cm"),
    Item(r"Find the second-degree Taylor polynomial for $\sqrt x$ centered at $x = 4$.", expr(taylor(sp.sqrt(x), 4, 2)), r"$2 + \frac14(x - 4) - \frac{1}{64}(x - 4)^2$.", work="2cm"),
    Item(r"Use your answer to the previous problem to estimate $\sqrt{4.2}$.", num(taylor(sp.sqrt(x), 4, 2).subs(x, sp.Rational(21, 5)), tol=1e-6), r"$2 + 0.05 - 0.000625 = 2.049375$.", work="1.2cm"),
    Item(r"Find the third-degree Maclaurin polynomial for $e^{2x}$.", expr(taylor(sp.exp(2 * x), 0, 3)), r"$1 + 2x + 2x^2 + \frac43x^3$.", work="1.6cm"),
    Item(r"Find the third-degree Taylor polynomial for $\frac1x$ centered at $x = 1$.", expr(taylor(1 / x, 1, 3)), r"$1 - (x - 1) + (x - 1)^2 - (x - 1)^3$.", work="2cm"),
    Item(r"$f(0) = 2$, $f'(0) = -3$, $f''(0) = 8$. Find the second-degree Maclaurin polynomial for $f$.", expr(2 - 3 * x + 4 * x**2), r"$2 - 3x + \frac82x^2$.", work="1.2cm"),
    Item(r"The third-degree Taylor polynomial for $g$ about $x = 1$ is $5 + 2(x - 1) - 3(x - 1)^2 + 4(x - 1)^3$. Find $g''(1)$ and $g'''(1)$.", selfcheck(r"g''(1) = -6,\ g'''(1) = 24"), r"$g''(1) = 2!(-3)$, $g'''(1) = 3!(4)$.", work="1.4cm"),
    Item(r"Find the fourth-degree Maclaurin polynomial for $\ln(1 + x)$.", expr(taylor(sp.log(1 + x), 0, 4)), r"$x - \frac{x^2}{2} + \frac{x^3}{3} - \frac{x^4}{4}$.", work="1.8cm"),
]

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"In a Taylor polynomial centered at $a$, the coefficient of $(x - a)^3$ is", [r"$f'''(a)$", r"$\frac{f'''(a)}{3}$", r"$\frac{f'''(a)}{3!}$", r"$3!\,f'''(a)$"], "C", r"$\frac{f^{(k)}(a)}{k!}$."),
    ),
    Variants(
        Item(r"Find the second-degree Maclaurin polynomial for $e^{-x}$.", expr(taylor(sp.exp(-x), 0, 2)), r"$1 - x + \frac{x^2}{2}$.", work="1.2cm"),
        Item(r"Find the second-degree Maclaurin polynomial for $\cos 2x$.", expr(taylor(sp.cos(2 * x), 0, 2)), r"$1 - 2x^2$.", work="1.2cm"),
        Item(r"Find the second-degree Maclaurin polynomial for $(1 + x)^3$.", expr(taylor((1 + x)**3, 0, 2)), r"$1 + 3x + 3x^2$.", work="1.2cm"),
    ),
    Variants(
        Item(r"$f(1) = 4$, $f'(1) = 2$, $f''(1) = -6$. Write the second-degree Taylor polynomial about $x = 1$ and estimate $f(1.1)$.", selfcheck(r"4 + 2(x - 1) - 3(x - 1)^2;\ 4.17"), r"$4 + 0.2 - 0.03$.", work="1.6cm"),
        Item(r"$f(0) = 1$, $f'(0) = -2$, $f''(0) = 10$. Write the second-degree Maclaurin polynomial and estimate $f(0.1)$.", selfcheck(r"1 - 2x + 5x^2;\ 0.85"), r"$1 - 0.2 + 0.05$.", work="1.6cm"),
    ),
    Variants(
        MCQ(r"The Taylor polynomial $P(x) = 3 - 2(x - 5) + 6(x - 5)^2$ is for $f$ about $x = 5$. Then $f''(5) = $", [r"$6$", r"$12$", r"$3$", r"$-2$"], "B", r"$2! \cdot 6$.", why_not={"A": "forgot to multiply by $2!$"}),
    ),
    Variants(
        Item(r"Find the third-degree Taylor polynomial for $\sin x$ about $x = \pi$.", selfcheck(r"-(x - \pi) + \tfrac16(x - \pi)^3"), r"Values at $\pi$: $0, -1, 0, 1$.", work="1.8cm"),
        Item(r"Find the second-degree Taylor polynomial for $e^x$ about $x = 1$.", selfcheck(r"e + e(x - 1) + \tfrac e2(x - 1)^2"), r"All derivatives are $e$ at $1$.", work="1.6cm"),
    ),
]
same("q", [taylor(sp.sin(x), sp.pi, 3).subs(x, sp.pi + 1)], [-1 + sp.Rational(1, 6)])

# ---------------------------------------------------------------- test prep
_m4 = float(taylor(sp.exp(sp.sin(x)), 0, 2).subs(x, sp.Rational(1, 5)))
MCQS = [
    MCQ(r"The third-degree Maclaurin polynomial for $\frac{1}{1 + x}$ is", [r"$1 + x + x^2 + x^3$", r"$1 - x + x^2 - x^3$", r"$1 - x + \frac{x^2}{2} - \frac{x^3}{6}$", r"$x - \frac{x^2}{2} + \frac{x^3}{3}$"], "B", r"$f^{(k)}(0) = (-1)^k k!$."),
    MCQ(r"If $P_2(x) = 1 + 3x - x^2$ is the second-degree Maclaurin polynomial for $f$, then $f'(0) + f''(0) = $", [r"$2$", r"$-2$", r"$5$", r"$1$"], "D", r"$f'(0) = 3$, $f''(0) = 2!(-1) = -2$."),
    MCQ(r"The second-degree Taylor polynomial for $\ln x$ about $x = 2$ is", [r"$\ln 2 + \frac12(x - 2) - \frac18(x - 2)^2$", r"$\ln 2 + \frac12(x - 2) - \frac14(x - 2)^2$", r"$\frac12(x - 2) - \frac18(x - 2)^2$", r"$\ln 2 + 2(x - 2) - 4(x - 2)^2$"], "A", r"$f'' (2) = -\frac14$, divided by $2!$."),
    MCQ(r"The second-degree Maclaurin polynomial for $e^{\sin x}$ is $1 + x + \frac{x^2}{2}$. Using it, $e^{\sin 0.2} \approx$", [r"$1.200$", r"$1.221$", rf"${_m4:.3f}$", r"$1.180$"], "C", rf"$1 + 0.2 + 0.02 = {_m4:.2f}$.", calc=True),
]
same("m", [taylor(1 / (1 + x), 0, 3), taylor(sp.exp(sp.sin(x)), 0, 2)], [1 - x + x**2 - x**3, 1 + x + x**2 / 2])

FRQS = []

TOPIC = Topic(
    number="10.11", title="Finding Taylor Polynomial Approximations of Functions",
    unit="Unit 10: Infinite Sequences and Series", ced=["LIM-8.A", "LIM-8.A.1", "LIM-8.A.2"],
    goals=r"Build Taylor and Maclaurin polynomials from derivatives and use them to approximate function values.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
