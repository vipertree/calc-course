"""Topic 10.12 (BC): Lagrange error bound.

CED: LIM-8.B (LIM-8.B.1): |f(x) - P_n(x)| <= M/(n + 1)! |x - a|^(n+1), M an upper bound for |f^(n+1)(z)| between a and x.
Lesson example: e^0.1 with P_3, M = 1.2, bound 0.000005. Worked examples: sin 0.5 with P_3 (0.0026); ln 1.2 with P_3
about 1 (M = 6, 0.0004); a given bound |f^(4)| <= 12 at 2.5 about 2 (0.03125).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, expr, num, same, selfcheck)

x = sp.symbols("x", real=True)
lag = lambda M, n_, d: sp.Rational(M) / sp.factorial(n_ + 1) * sp.Rational(d)**(n_ + 1)

same("lesson", [lag(sp.Rational(6, 5), 3, sp.Rational(1, 10))], [sp.Rational(1, 200000)])
same("ex", [lag(1, 3, sp.Rational(1, 2)), lag(6, 3, sp.Rational(1, 5)), lag(12, 3, sp.Rational(1, 2))], [sp.Rational(1, 384), sp.Rational(1, 2500), sp.Rational(1, 32)])
close("e0.1 actual", float(sp.exp(sp.Rational(1, 10)) - (1 + sp.Rational(1, 10) + sp.Rational(1, 200) + sp.Rational(1, 6000))), 4.25e-6, 1e-7)

NOTES = [
    Video("s10_12.py::Lesson", "Lagrange error bound", 4),

    Section("The bound"),
    Formula("Lagrange error bound", (r"If $P_n$ is the $n$th-degree Taylor polynomial for $f$ about $a$, then \[ |f(x) - P_n(x)| \le \blank{\frac{M}{(n + 1)!}\,|x - a|^{n+1}}, \] where $M \ge |f^{(n+1)}(z)|$ for every $z$ between $a$ and $x$.")),
    Text(r"It looks like the next Taylor term, with the next derivative replaced by its largest possible size. Any $M$ you can justify works; on the exam $M$ is often given."),
    VideoExample('Bounding the error for e to the 0.1', work="4cm"),
    Text(r"\textbf{Finding $M$.} For $f^{(4)}(x) = -\frac{6}{x^4}$ on $[1, 1.2]$, the size $\frac{6}{z^4}$ is largest at $z = 1$: $M = 6$."),
    BigIdea(r"Error $\le \frac{M}{(n + 1)!}|x - a|^{n+1}$: the worst-case next term."),
    Check(r"$|f'''(x)| \le 4$ near $0$. Bound $|f(0.1) - P_2(0.1)|$ for the Maclaurin polynomial.", selfcheck(r"\tfrac{4}{6}(0.1)^3 \approx 0.00067"), r"$n = 2$: $\frac{4}{3!}(0.1)^3$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Bound the error in approximating $\cos(0.2)$ by $1 - \frac{x^2}{2}$ using Lagrange with $n = 3$ (note $P_3 = P_2$).", num(lag(1, 3, sp.Rational(1, 5)), tol=1e-6), r"$M = 1$: $\frac{(0.2)^4}{24} \approx 0.0000667$.", work="1.6cm"),
    Item(r"Bound the error in approximating $e^{0.5}$ with $P_2(x) = 1 + x + \frac{x^2}{2}$, using $M = 2$.", num(lag(2, 2, sp.Rational(1, 2)), tol=1e-4), r"$\frac{2}{3!}(0.5)^3 = \frac{0.25}{6} \approx 0.0417$.", work="1.6cm"),
    Item(r"Why is $M = 2$ justified in the previous problem?", selfcheck(r"e^z \le e^{0.5} < 2 \text{ on } [0, 0.5]"), r"$f'''(z) = e^z \le e^{0.5} \approx 1.65 < 2$.", work="1.2cm"),
    Item(r"$|f^{(5)}(x)| \le 40$ on $[0, 1]$. Bound $|f(0.4) - P_4(0.4)|$ for the Maclaurin polynomial.", num(lag(40, 4, sp.Rational(2, 5)), tol=1e-5), r"$\frac{40}{5!}(0.4)^5 = \frac{40 \cdot 0.01024}{120} \approx 0.00341$.", work="1.6cm"),
    Item(r"Bound the error in using $P_1(x) = 1 + \frac12(x - 1)$ for $\sqrt x$ at $x = 1.1$.", num(sp.Rational(1, 4) / 2 * sp.Rational(1, 100), tol=1e-6), r"$f'' = -\frac14 z^{-3/2}$, $M = \frac14$ on $[1, 1.1]$: $\frac{1/4}{2!}(0.1)^2 = 0.00125$.", work="2cm"),
    Item(r"How large must $n$ be so that the Maclaurin polynomial $P_n$ for $e^x$ approximates $e^{1}$ with error less than $0.001$ (use $M = 3$)?", num(6), r"$\frac{3}{(n + 1)!} < 0.001$: $(n + 1)! > 3000$, so $n + 1 = 7$, $n = 6$.", work="2cm"),
]
same("p", [lag(40, 4, sp.Rational(2, 5)), lag(2, 2, sp.Rational(1, 2))], [sp.Rational(64, 18750), sp.Rational(1, 24)])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"The Lagrange error bound for $P_n$ uses which derivative?", [r"$f^{(n)}$", r"$f^{(n+1)}$", r"$f'$", r"$f^{(n-1)}$"], "B", r"The next one after the polynomial's degree."),
    ),
    Variants(
        Item(r"$|f'''(x)| \le 6$. Bound $|f(1.2) - P_2(1.2)|$ for the Taylor polynomial about $1$.", num(lag(6, 2, sp.Rational(1, 5)), tol=1e-5), r"$\frac{6}{3!}(0.2)^3 = 0.008$.", work="1.2cm"),
        Item(r"$|f^{(4)}(x)| \le 24$. Bound $|f(0.5) - P_3(0.5)|$ for the Maclaurin polynomial.", num(lag(24, 3, sp.Rational(1, 2)), tol=1e-5), r"$\frac{24}{24}(0.5)^4 = 0.0625$.", work="1.2cm"),
        Item(r"$|f''(x)| \le 10$. Bound $|f(3.1) - P_1(3.1)|$ for the tangent line at $3$.", num(lag(10, 1, sp.Rational(1, 10)), tol=1e-5), r"$\frac{10}{2}(0.1)^2 = 0.05$.", work="1.2cm"),
    ),
    Variants(
        Item(r"Bound the error in $\sin(0.3) \approx 0.3$ using Lagrange with $n = 2$.", num(lag(1, 2, sp.Rational(3, 10)), tol=1e-6), r"$M = 1$: $\frac{0.027}{6} = 0.0045$.", work="1.2cm"),
        Item(r"Bound the error in $e^{0.2} \approx 1.2$ using Lagrange with $n = 1$ and $M = 1.5$.", num(lag(sp.Rational(3, 2), 1, sp.Rational(1, 5)), tol=1e-6), r"$\frac{1.5}{2}(0.04) = 0.03$.", work="1.2cm"),
    ),
    Variants(
        MCQ(r"For $f(x) = \ln x$ and $P_2$ about $x = 1$, the best $M$ for $|f'''(z)|$ on $[1, 1.5]$ is", [r"$\frac{2}{1.5^3}$", r"$2$", r"$1$", r"$\frac{1}{1.5}$"], "B", r"$f''' = \frac{2}{x^3}$ is largest at $x = 1$."),
    ),
    Variants(
        Item(r"$P_3$ approximates $f$ about $0$ and $|f^{(4)}| \le 5$ on $[0, 1]$. Is $|f(1) - P_3(1)| < 0.25$ guaranteed?", selfcheck(r"\text{yes: bound } \tfrac{5}{24} \approx 0.208"), r"$\frac{5}{4!} \cdot 1^4$.", work="1.4cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$P_2(x) = 1 - \frac{x^2}{2}$ approximates $\cos x$. The Lagrange error bound at $x = 0.6$ with $n = 2$ is", [r"$0.036$", r"$0.06$", r"$0.0054$", r"$0.18$"], "A", r"$M = 1$: $\frac{0.216}{6} = 0.036$."),
    MCQ(r"$|f^{(4)}(x)| \le 8$ for all $x$. The third-degree Taylor polynomial about $x = 2$ approximates $f(2.5)$ with error at most", [r"$\frac{1}{48}$", r"$\frac{1}{4}$", r"$\frac{1}{12}$", r"$\frac{1}{2}$"], "A", r"$\frac{8}{24}(0.5)^4 = \frac{1}{48}$."),
    MCQ(r"Which is the Lagrange error bound for approximating $e^{0.2}$ with $P_3(x) = 1 + x + \frac{x^2}{2} + \frac{x^3}{6}$, using $M = e^{0.2}$?", [r"$\frac{e^{0.2}(0.2)^3}{6}$", r"$\frac{(0.2)^4}{24}$", r"$\frac{e^{0.2}(0.2)^4}{24}$", r"$\frac{e^{0.2}(0.2)^4}{4}$"], "C", r"$n + 1 = 4$."),
    MCQ(r"For the Maclaurin polynomial $P_n$ of $\sin x$, the Lagrange bound at $x = 1$ is $\frac{1}{(n + 1)!}$. The least $n$ guaranteeing error below $0.001$ is", [r"$4$", r"$5$", r"$7$", r"$6$"], "D", r"$\frac{1}{7!} = \frac{1}{5040} < 0.001$ but $\frac{1}{6!} = \frac{1}{720} > 0.001$: $n + 1 = 7$."),
]
same("m", [lag(1, 2, sp.Rational(3, 5)), lag(8, 3, sp.Rational(1, 2))], [sp.Rational(9, 250), sp.Rational(1, 48)])

# ---------------------------------------------------------------- FRQ
P3 = 2 - 3 * (x - 1) + 2 * (x - 1)**2 - 2 * (x - 1)**3
same("frq", [P3.subs(x, sp.Rational(6, 5)), lag(30, 3, sp.Rational(1, 5)), sp.expand(sp.diff(P3, x) - (-3 + 4 * (x - 1) - 6 * (x - 1)**2))], [sp.Rational(183, 125), sp.Rational(1, 500), 0])
FRQS = [
    FRQ("A Taylor polynomial", (r"Let $f$ be a function with derivatives of all orders. $f(1) = 2$, $f'(1) = -3$, $f''(1) = 4$, $f'''(1) = -12$, and $\left|f^{(4)}(x)\right| \le 30$ for $1 \le x \le 1.5$."), [
        Part("a", r"Write the third-degree Taylor polynomial for $f$ about $x = 1$.", selfcheck(r"2 - 3(x - 1) + 2(x - 1)^2 - 2(x - 1)^3"),
             r"$P_3(x) = 2 - 3(x - 1) + \frac{4}{2!}(x - 1)^2 + \frac{-12}{3!}(x - 1)^3 = 2 - 3(x - 1) + 2(x - 1)^2 - 2(x - 1)^3$.", [(1, "first two terms"), (1, "last two terms")], work="2.4cm"),
        Part("b", r"Use the polynomial from part (a) to approximate $f(1.2)$.", num(sp.Rational(183, 125)), r"$2 - 0.6 + 2(0.04) - 2(0.008) = 1.464$.", [(1, "answer")], work="1.6cm"),
        Part("c", r"Use the Lagrange error bound to show that the approximation in part (b) differs from $f(1.2)$ by less than $0.003$.", selfcheck(r"\tfrac{30}{4!}(0.2)^4 = 0.002 < 0.003"),
             r"$|f(1.2) - P_3(1.2)| \le \frac{30}{4!}(0.2)^4 = \frac{30 \cdot 0.0016}{24} = 0.002 < 0.003$.", [(1, "form of the bound"), (1, "value and conclusion")], work="2cm"),
        Part("d", r"Write the second-degree Taylor polynomial for $f'$ about $x = 1$.", selfcheck(r"-3 + 4(x - 1) - 6(x - 1)^2"),
             r"$f'(1) + f''(1)(x - 1) + \frac{f'''(1)}{2!}(x - 1)^2 = -3 + 4(x - 1) - 6(x - 1)^2$ (the derivative of $P_3$).", [(1, "polynomial")], work="1.8cm"),
    ], frq_type="Taylor polynomial"),
]

TOPIC = Topic(
    number="10.12", title="Lagrange Error Bound",
    unit="Unit 10: Infinite Sequences and Series", ced=["LIM-8.B", "LIM-8.B.1"],
    goals=r"Bound the error of a Taylor polynomial approximation with the Lagrange error bound.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
