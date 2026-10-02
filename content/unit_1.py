"""Unit 1 test: Limits and Continuity. AP format: 12 MCQ (no calculator), 4 MCQ (calculator), 3 FRQ.

Covers 1.2-1.16. Every keyed answer is checked with sympy below its question.
"""
import math

import sympy as sp

from calclib import FRQ, MCQ, Part, UnitTest, Variants, check, close, dne, infinite, limchain, num, same, selfcheck
from calclib.figs import graph

x, k, a, b, t = sp.symbols("x k a b t")
oo = sp.oo

FIG = graph("u1_f", [("1-x", -4, -2), ("x+5", -2, 1), ("1/(3-x)", 1, 2.8), ("1/(3-x)", 3.2, 5)],
            xr=(-4, 5), yr=(-5.5, 7), vlines=[3], open=[(-2, 3), (1, 6)], closed=[(-2, -1), (1, 0.5)], ystep=2,
            w="8cm", h="5.4cm", caption=r"The graph of $f$.")
same("fig -2", [sp.limit(1 - x, x, -2), sp.limit(x + 5, x, -2)], [3, 3])
same("fig 1", [sp.limit(x + 5, x, 1), (1 / (3 - x)).subs(x, 1)], [6, sp.Rational(1, 2)])
same("fig 3", [sp.limit(1 / (3 - x), x, 3, "-"), sp.limit(1 / (3 - x), x, 3, "+")], [oo, -oo])

A = [
    MCQ(r"$\displaystyle\lim_{x\to3}\frac{x^2-9}{x^2-2x-3}$ is", [r"$0$", r"$1$", r"$\dfrac32$", r"Does not exist"], "C",
        limchain(3, [r"\frac{(x-3)(x+3)}{(x-3)(x+1)}", r"\frac{x+3}{x+1}"], r"\frac64 = \frac32"), why_not={"D": "stopped at $\\frac00$"}),
    MCQ(r"The graph of $f$ is shown. What is $\displaystyle\lim_{x\to-2}f(x)$?",
        [r"$-1$", r"$3$", r"$1$", r"Does not exist."], "B", r"Both pieces approach height $3$; the dot at $-1$ is $f(-2)$.",
        why_not={"A": "that is $f(-2)$"}, figure=FIG),
    MCQ(r"The graph of $f$ is shown. Which statement about $f$ at $x = 1$ is true?",
        [r"$\displaystyle\lim_{x\to1}f(x) = 6$", r"$f$ is continuous at $x = 1$", r"$f$ has a removable discontinuity at $x = 1$",
         r"$f$ has a jump discontinuity at $x = 1$"], "D", r"Left-hand limit $6$, right-hand limit $\frac12$: a jump.", figure=FIG),
    MCQ(r"The graph of $f$ is shown. $\displaystyle\lim_{x\to3^-}f(x)$ is", [r"$-\infty$", r"$\infty$", r"$0$", r"$\dfrac12$"], "B",
        r"The graph rises without bound as $x$ approaches $3$ from the left.", why_not={"A": "that is the right-hand limit"}, figure=FIG),
    MCQ(r"$\displaystyle\lim_{x\to0}\frac{\sin(5x)}{2x}$ is", [r"$\dfrac25$", r"$1$", r"$\dfrac52$", r"$5$"], "C",
        limchain(0, [r"\frac52\cdot\frac{\sin5x}{5x}"], r"\frac52"), why_not={"A": "inverted"}),
    MCQ(r"$\displaystyle\lim_{x\to\infty}\frac{4x^2-1}{3+2x-x^2}$ is", [r"$-4$", r"$4$", r"$0$", r"$-\dfrac13$"], "A",
        limchain(r"\infty", [r"\frac{4-\frac1{x^2}}{\frac3{x^2}+\frac2x-1}"], r"\frac{4}{-1} = -4"),
        why_not={"B": "sign of the leading coefficient", "D": "used the constant terms"}),
    MCQ(r"Let $g(x) = \begin{cases} kx - 1, & x < 2 \\ x^2 + k, & x \ge 2. \end{cases}$ For what value of $k$ is $g$ continuous at $x = 2$?",
        [r"$1$", r"$3$", r"$4$", r"$5$"], "D", r"$2k - 1 = 4 + k$, so $k = 5$."),
    MCQ(r"$\displaystyle\lim_{x\to4}\frac{\sqrt x - 2}{x - 4}$ is", [r"$\dfrac14$", r"$\dfrac12$", r"$0$", r"$4$"], "A",
        r"Multiply by the conjugate: " + limchain(4, [r"\frac{x-4}{(x-4)(\sqrt x+2)}", r"\frac{1}{\sqrt x + 2}"], r"\frac14")),
    MCQ(r"What are all vertical asymptotes of $y = \dfrac{x^2-1}{x^2+x-2}$?",
        [r"$x = 1$ only", r"$x = -2$ only", r"$x = 1$ and $x = -2$", r"$y = 1$"], "B",
        r"$\dfrac{(x-1)(x+1)}{(x-1)(x+2)}$: $x - 1$ cancels (a hole); $x = -2$ remains.", why_not={"C": "$x=1$ is a hole"}),
    MCQ(r"A continuous function $h$ has the values shown."
        r"\par\centerline{\begin{tabular}{c|ccccc} $x$ & 0 & 1 & 3 & 4 & 6 \\ \hline $h(x)$ & $-2$ & 3 & 1 & $-1$ & 2\end{tabular}}"
        r"\par What is the fewest number of zeros $h$ must have on $[0, 6]$?", [r"$1$", r"$2$", r"$3$", r"$4$"], "C",
        r"Sign changes on $[0,1]$, $[3,4]$ and $[4,6]$."),
    MCQ(r"If $2x - 1 \le g(x) \le x^2$ for all $x$ near $1$, then $\displaystyle\lim_{x\to1}g(x)$ is",
        [r"$0$", r"$1$", r"$2$", r"not determined"], "B", r"Both bounds approach $1$; by the squeeze theorem the limit is $1$."),
    MCQ(r"$\displaystyle\lim_{x\to2^-}\frac{|x-2|}{x^2-4}$ is", [r"$\dfrac14$", r"$0$", r"$-\infty$", r"$-\dfrac14$"], "D",
        r"For $x<2$, $|x-2| = -(x-2)$, so " + limchain(2, [r"\frac{-(x-2)}{(x-2)(x+2)}", r"\frac{-1}{x+2}"], r"-\frac14", side="^-"),
        why_not={"A": "sign error"}),
]
same("A1", sp.limit((x**2 - 9) / (x**2 - 2 * x - 3), x, 3), sp.Rational(3, 2))
same("A5", sp.limit(sp.sin(5 * x) / (2 * x), x, 0), sp.Rational(5, 2))
same("A6", sp.limit((4 * x**2 - 1) / (3 + 2 * x - x**2), x, oo), -4)
same("A7", sp.solve(sp.Eq(2 * k - 1, 4 + k), k)[0], 5)
same("A8", sp.limit((sp.sqrt(x) - 2) / (x - 4), x, 4), sp.Rational(1, 4))
same("A12", sp.limit(-(x - 2) / (x**2 - 4), x, 2), sp.Rational(-1, 4))

G14 = (sp.exp(x) - 1 - x) / x**2
tab14 = " & ".join(f"{float(G14.subs(x, v)):.4f}" for v in [-0.1, -0.01, 0.01, 0.1])
B = [
    MCQ(r"$\displaystyle\lim_{x\to0}\frac{3^x-1}{x}$ is closest to", [r"$0$", r"$1$", r"$1.099$", r"$3$"], "C",
        r"A table with $x = \pm0.001$ gives about $1.0986$. (The exact value is $\ln 3$.)", calc=True),
    MCQ(r"Values of $g(x) = \dfrac{e^x-1-x}{x^2}$ are shown."
        r"\par\centerline{\begin{tabular}{c|cccc} $x$ & $-0.1$ & $-0.01$ & $0.01$ & $0.1$ \\ \hline $g(x)$ & " + tab14 + r"\end{tabular}}"
        r"\par Which is the best estimate of $\displaystyle\lim_{x\to0}g(x)$?", [r"$0.48$", r"$0.5$", r"$0.52$", r"$1$"], "B",
        r"Both sides close in on $0.5$.", calc=True),
    MCQ(r"$g(x) = x^3 - 4x + 1$ has a zero in $[0, 1]$ by the IVT. What is that zero, to three decimal places?",
        [r"$0.254$", r"$0.500$", r"$1.861$", r"$-2.115$"], "A", r"Use a graphing calculator: the zero in $[0, 1]$ is about $0.254$.",
        why_not={"C": "a different zero, outside $[0,1]$", "D": "a different zero, outside $[0,1]$"}, calc=True),
    MCQ(r"Which is a horizontal asymptote of $y = \dfrac{2e^x + 5}{e^x - 1}$ as $x \to -\infty$?",
        [r"$y = 2$", r"$y = 5$", r"$y = 0$", r"$y = -5$"], "D", r"As $x\to-\infty$, $e^x \to 0$, so " + limchain(r"-\infty", [r"\frac{2e^x+5}{e^x-1}"], r"\frac{5}{-1} = -5") + ".",
        why_not={"A": "that is the asymptote as $x \\to \\infty$"}, calc=True),
]
close("B13", (3**0.001 - 1) / 0.001, 1.0992, 5e-4)
same("B14", sp.limit(G14, x, 0), sp.Rational(1, 2))
roots = [r for r in sp.Poly(x**3 - 4 * x + 1).nroots() if r.is_real]
check("B15 root in [0,1]", any(0 < float(r) < 1 and abs(float(r) - 0.254) < 5e-4 for r in roots), str(roots))
same("B16", sp.limit((2 * sp.exp(x) + 5) / (sp.exp(x) - 1), x, -oo), -5)

F1 = (x**2 + a * x - 6) / (x - 2)
FIG2 = graph("u1_g", [("2", -3, -1), ("x^2-1", -1, 2), ("5-x", 2, 4)], xr=(-3, 4), yr=(-1.5, 4), open=[(-1, 2), (2, 3)],
             closed=[(-1, 0), (2, 1)], w="7cm", h="5cm", caption=r"The graph of $g$.")
FRQS = [
    FRQ("Making a function continuous", (
        r"Let $f(x) = \begin{cases} \dfrac{x^2 + ax - 6}{x - 2}, & x < 2 \\ bx + 1, & x \ge 2, \end{cases}$ where $a$ and $b$ are constants."), [
        Part("a", r"Find the value of $a$ for which $\displaystyle\lim_{x\to2^-}f(x)$ exists as a real number. Explain your reasoning.",
             num(1), r"The denominator approaches $0$, so for a finite limit the numerator must approach $0$ too: $4 + 2a - 6 = 0$, so $a = 1$.",
             [(1, "numerator must be $0$ at $x=2$"), (1, "$a = 1$")], work="2.6cm"),
        Part("b", r"With that value of $a$, find $\displaystyle\lim_{x\to2^-}f(x)$.", num(5),
             limchain(2, [r"\frac{(x+3)(x-2)}{x-2}", r"(x + 3)"], 5, side="^-"), [(1, "factors"), (1, "answer $5$")], work="2.4cm"),
        Part("c", r"Find the value of $b$ for which $f$ is continuous at $x = 2$. Justify your answer.",
             num(2), r"$f(2) = 2b + 1$ and $\displaystyle\lim_{x\to2^+}f(x) = 2b + 1$. Continuity needs $2b + 1 = 5$, so $b = 2$; then "
                     r"$\displaystyle\lim_{x\to2}f(x) = 5 = f(2)$.",
             [(1, "$b = 2$"), (1, "justification: the limit at $x = 2$ equals $f(2)$")], work="2.8cm"),
    ], frq_type="Limits and continuity"),
    FRQ("Reading a graph", r"The graph of $g$ is shown. Let $h(x) = x^2 + 1$.", [
        Part("a", r"For each of $g(-1)$ and $\displaystyle\lim_{x\to-1}g(x)$, find the value or state that it does not exist.",
             selfcheck(r"g(-1) = 0;\ \text{the limit does not exist}"),
             r"$g(-1) = 0$. From the left, $g = 2$; from the right, $x^2 - 1 \to 0$. The one-sided limits differ, so the limit does not exist.",
             [(1, "$g(-1) = 0$ and both one-sided limits"), (1, "does not exist, with reason")], work="2.4cm"),
        Part("b", r"Is $g$ continuous at $x = 2$? Use the definition of continuity to explain your answer.", selfcheck(r"\text{No}"),
             r"No. $\displaystyle\lim_{x\to2^-}g(x) = 2^2 - 1 = 3$ and $\displaystyle\lim_{x\to2^+}g(x) = 5 - 2 = 3$, so "
             r"$\displaystyle\lim_{x\to2}g(x) = 3$. But $g(2) = 1 \ne 3$, so $g$ is not continuous at $x = 2$.",
             [(1, "$\\displaystyle\\lim_{x\\to2}g(x) = 3$"), (1, "no, because the limit is not equal to $g(2) = 1$")], work="2.6cm"),
        Part("c", r"Find the value of $\displaystyle\lim_{x\to2}\frac{g(x)}{h(x)}$, or show that it does not exist.", num(sp.Rational(3, 5)),
             r"$\displaystyle\lim_{x\to2}g(x) = 3$ and $\displaystyle\lim_{x\to2}h(x) = 5 \ne 0$, so "
             r"$\displaystyle\lim_{x\to2}\frac{g(x)}{h(x)} = \frac35$.",
             [(1, "uses both limits"), (1, "answer $\\frac35$")], work="2.2cm"),
    ], frq_type="Limits and continuity", figure=FIG2),
    FRQ("River flow", (
        r"The rate at which water flows past a point on a river is modeled by a continuous function $R$, where $R(t)$ is measured in "
        r"cubic feet per second and $t$ is measured in hours, for $0 \le t \le 12$. Selected values of $R(t)$ are given in the table."
        r"\par\smallskip\centerline{\begin{tabular}{c|ccccc} $t$ (hr) & 0 & 3 & 5 & 9 & 12 \\ \hline "
        r"$R(t)$ & 210 & 245 & 230 & 190 & 225\end{tabular}}"), [
        Part("a", r"Find the average rate of change of $R$ over the interval $3 \le t \le 9$. Show the work that leads to your answer. Indicate units of measure.", num(sp.Rational(-55, 6), tol=0.005,
             display=r"-\tfrac{55}{6}\ \text{ft}^3/\text{s per hr}"),
             r"$\dfrac{190 - 245}{6} = -\dfrac{55}{6} \approx -9.167$ cubic feet per second per hour.",
             [(1, "difference quotient"), (1, "value with units")], work="2.2cm"),
        Part("b", r"For $0 \le t \le 12$, what is the fewest number of times at which $R(t)$ must equal $220$? Give a reason for your answer.", num(3),
             r"$R$ is continuous. $220$ is between $210$ and $245$ (on $[0,3]$), between $230$ and $190$ (on $[5,9]$), and between $190$ "
             r"and $225$ (on $[9,12]$). By the IVT, $R(t) = 220$ at least three times.",
             [(1, "continuity and bracketing values"), (1, "IVT named with conclusion"), (1, "three times")], work="3cm"),
        Part("c", r"Use the data in the table to estimate $R'(4)$. Show the work that leads to your answer.", num(sp.Rational(-15, 2)),
             r"$\dfrac{R(5) - R(3)}{5 - 3} = \dfrac{230 - 245}{2} = -7.5$ cubic feet per second per hour.",
             [(1, "estimate $-7.5$")], work="2cm"),
    ], frq_type="Table", calc=True),
]
same("F1a", sp.solve(sp.Eq(4 + 2 * a - 6, 0), a)[0], 1)
same("F1b", sp.limit((x**2 + x - 6) / (x - 2), x, 2), 5)
same("F1c", sp.solve(sp.Eq(2 * b + 1, 5), b)[0], 2)
same("F2", [sp.limit(x**2 - 1, x, 2), 5 - 2, sp.limit(x**2 - 1, x, 2) / (2**2 + 1)], [3, 3, sp.Rational(3, 5)])

# ================================================================ form B
FIGB = graph("u1_fb", [("x+3", -4, -1), ("2*x+4", -1, 1), ("1/(x-3)", 1, 2.8), ("1/(x-3)", 3.2, 5)],
             xr=(-4, 5), yr=(-5.5, 7), vlines=[3], open=[(-1, 2), (1, 6)], closed=[(-1, 4), (1, -0.5)], ystep=2,
             w="8cm", h="5.4cm", caption=r"The graph of $f$.")
same("figB", [sp.limit(x + 3, x, -1), sp.limit(2 * x + 4, x, -1), sp.limit(2 * x + 4, x, 1), (1 / (x - 3)).subs(x, 1),
              sp.limit(1 / (x - 3), x, 3, "-")], [2, 2, 6, sp.Rational(-1, 2), -oo])
A2 = [
    MCQ(r"$\displaystyle\lim_{x\to-2}\frac{x^2-4}{x^2+5x+6}$ is", [r"$-4$", r"$0$", r"$4$", r"Does not exist"], "A",
        limchain(-2, [r"\frac{(x-2)(x+2)}{(x+2)(x+3)}", r"\frac{x-2}{x+3}"], -4), why_not={"D": "stopped at $\\frac00$"}),
    MCQ(r"The graph of $f$ is shown. What is $\displaystyle\lim_{x\to-1}f(x)$?", [r"$4$", r"$2$", r"$0$", r"Does not exist."], "B",
        r"Both pieces approach height $2$; the dot at $4$ is $f(-1)$.", why_not={"A": "that is $f(-1)$"}, figure=FIGB),
    MCQ(r"The graph of $f$ is shown. Which statement about $f$ at $x = 1$ is true?",
        [r"$\displaystyle\lim_{x\to1}f(x) = 6$", r"$f$ is continuous at $x = 1$", r"$f(1) = -\frac12$ and $f$ has a jump discontinuity at $x = 1$",
         r"$f$ has a removable discontinuity at $x = 1$"], "C", r"Left-hand limit $6$, right-hand limit $-\frac12 = f(1)$: a jump.", figure=FIGB),
    MCQ(r"The graph of $f$ is shown. $\displaystyle\lim_{x\to3^-}f(x)$ is", [r"$\infty$", r"$-\infty$", r"$0$", r"$-\dfrac12$"], "B",
        r"The graph falls without bound as $x$ approaches $3$ from the left.", why_not={"A": "that is the right-hand limit"}, figure=FIGB),
    MCQ(r"$\displaystyle\lim_{x\to0}\frac{\sin(3x)}{4x}$ is", [r"$\dfrac43$", r"$1$", r"$\dfrac34$", r"$3$"], "C",
        limchain(0, [r"\frac34\cdot\frac{\sin3x}{3x}"], r"\frac34"), why_not={"A": "inverted"}),
    MCQ(r"$\displaystyle\lim_{x\to-\infty}\frac{2x^3+x}{5-4x^3}$ is", [r"$\dfrac12$", r"$-\dfrac12$", r"$0$", r"$-\infty$"], "B",
        limchain(r"-\infty", [r"\frac{2+\frac1{x^2}}{\frac5{x^3}-4}"], r"-\frac12"), why_not={"A": "sign of the leading coefficient"}),
    MCQ(r"Let $g(x) = \begin{cases} kx - 3, & x < 3 \\ x^2 - k, & x \ge 3. \end{cases}$ For what value of $k$ is $g$ continuous at $x = 3$?",
        [r"$1$", r"$2$", r"$3$", r"$6$"], "C", r"$3k - 3 = 9 - k$, so $4k = 12$ and $k = 3$."),
    MCQ(r"$\displaystyle\lim_{x\to9}\frac{x - 9}{\sqrt x - 3}$ is", [r"$6$", r"$\dfrac16$", r"$0$", r"$3$"], "A",
        limchain(9, [r"\frac{(\sqrt x-3)(\sqrt x+3)}{\sqrt x - 3}", r"(\sqrt x + 3)"], 6), why_not={"B": "inverted"}),
    MCQ(r"What are all vertical asymptotes of $y = \dfrac{x^2-4}{x^2-x-2}$?",
        [r"$x = 2$ only", r"$x = -1$ only", r"$x = 2$ and $x = -1$", r"$y = 1$"], "B",
        r"$\dfrac{(x-2)(x+2)}{(x-2)(x+1)}$: $x - 2$ cancels (a hole); $x = -1$ remains.", why_not={"C": "$x = 2$ is a hole"}),
    MCQ(r"A continuous function $h$ has the values shown."
        r"\par\centerline{\begin{tabular}{c|ccccc} $x$ & 0 & 2 & 3 & 5 & 7 \\ \hline $h(x)$ & 4 & $-1$ & $-3$ & 2 & 5\end{tabular}}"
        r"\par What is the fewest number of zeros $h$ must have on $[0, 7]$?", [r"$1$", r"$2$", r"$3$", r"$4$"], "B",
        r"Sign changes on $[0,2]$ and $[3,5]$ only."),
    MCQ(r"If $4x - 4 \le g(x) \le x^2$ for all $x$ near $2$, then $\displaystyle\lim_{x\to2}g(x)$ is",
        [r"$0$", r"$2$", r"$4$", r"not determined"], "C", r"Both bounds give $4$ at $x = 2$; by the squeeze theorem the limit is $4$."),
    MCQ(r"$\displaystyle\lim_{x\to3^+}\frac{|x-3|}{x^2-9}$ is", [r"$-\dfrac16$", r"$\dfrac16$", r"$0$", r"$\infty$"], "B",
        r"For $x>3$, $|x-3| = x-3$, so " + limchain(3, [r"\frac{x-3}{(x-3)(x+3)}", r"\frac{1}{x+3}"], r"\frac16", side="^+"),
        why_not={"A": "that's the left side"}),
]
same("A2 versions", [sp.limit((x**2 - 4) / (x**2 + 5 * x + 6), x, -2), sp.limit(sp.sin(3 * x) / (4 * x), x, 0),
                     sp.limit((2 * x**3 + x) / (5 - 4 * x**3), x, -oo), sp.solve(sp.Eq(3 * k - 3, 9 - k), k)[0],
                     sp.limit((x - 9) / (sp.sqrt(x) - 3), x, 9), sp.limit((x - 3) / (x**2 - 9), x, 3, "+")],
     [-4, sp.Rational(3, 4), sp.Rational(-1, 2), 3, 6, sp.Rational(1, 6)])
check("A2 squeeze", sp.expand(x**2 - (4 * x - 4)) == (x - 2)**2 or sp.factor(x**2 - 4 * x + 4) == (x - 2)**2, "x^2 >= 4x-4")

G14B = (sp.exp(2 * x) - 1) / x
tab14b = " & ".join(f"{float(G14B.subs(x, v)):.4f}" for v in [-0.1, -0.01, 0.01, 0.1])
B2 = [
    MCQ(r"$\displaystyle\lim_{x\to0}\frac{5^x-1}{x}$ is closest to", [r"$0$", r"$1$", r"$5$", r"$1.609$"], "D",
        r"A table with $x = \pm0.001$ gives about $1.609$. (The exact value is $\ln 5$.)", calc=True),
    MCQ(r"Values of $g(x) = \dfrac{e^{2x}-1}{x}$ are shown."
        r"\par\centerline{\begin{tabular}{c|cccc} $x$ & $-0.1$ & $-0.01$ & $0.01$ & $0.1$ \\ \hline $g(x)$ & " + tab14b + r"\end{tabular}}"
        r"\par Which is the best estimate of $\displaystyle\lim_{x\to0}g(x)$?", [r"$2$", r"$1.98$", r"$2.02$", r"$0$"], "A",
        r"Both sides close in on $2$.", calc=True),
    MCQ(r"$g(x) = x^3 + x - 3$ has a zero in $[1, 2]$ by the IVT. What is that zero, to three decimal places?",
        [r"$1.500$", r"$0.500$", r"$2.000$", r"$1.213$"], "D", r"Use a graphing calculator: the zero is about $1.213$.", calc=True),
    MCQ(r"Which is a horizontal asymptote of $y = \dfrac{3e^x + 4}{e^x + 2}$ as $x \to \infty$?",
        [r"$y = 2$", r"$y = 4$", r"$y = 3$", r"$y = 0$"], "C",
        r"Divide by $e^x$: " + limchain(r"\infty", [r"\frac{3 + 4e^{-x}}{1 + 2e^{-x}}"], 3) + ".",
        why_not={"A": "that is the asymptote as $x \\to -\\infty$"}, calc=True),
]
close("B2 13", (5**0.001 - 1) / 0.001, 1.6094, 2e-3)
same("B2 14", sp.limit(G14B, x, 0), 2)
roots2 = [r for r in sp.Poly(x**3 + x - 3).nroots() if r.is_real]
check("B2 15 root in [1,2]", any(1 < float(r) < 2 and abs(float(r) - 1.213) < 5e-4 for r in roots2), str(roots2))
same("B2 16", [sp.limit((3 * sp.exp(x) + 4) / (sp.exp(x) + 2), x, oo), sp.limit((3 * sp.exp(x) + 4) / (sp.exp(x) + 2), x, -oo)], [3, 2])

FIG2B = graph("u1_gb", [("x+3", -3, 0), ("x^2+1", 0, 2), ("7-x", 2, 4)], xr=(-3, 4), yr=(-0.5, 5.5), open=[(0, 3), (2, 5)],
              closed=[(0, 1), (2, 2)], w="7cm", h="5cm", caption=r"The graph of $g$.")
FRQS2 = [
    FRQ("Making a function continuous", (
        r"Let $f(x) = \begin{cases} \dfrac{x^2 + ax - 12}{x - 3}, & x < 3 \\ bx - 2, & x \ge 3, \end{cases}$ where $a$ and $b$ are constants."), [
        Part("a", r"Find the value of $a$ for which $\displaystyle\lim_{x\to3^-}f(x)$ exists as a real number. Explain your reasoning.",
             num(1), r"The denominator approaches $0$, so for a finite limit the numerator must approach $0$ too: $9 + 3a - 12 = 0$, so $a = 1$.",
             [(1, "numerator must be $0$ at $x=3$"), (1, "$a = 1$")], work="2.6cm"),
        Part("b", r"With that value of $a$, find $\displaystyle\lim_{x\to3^-}f(x)$.", num(7),
             limchain(3, [r"\frac{(x+4)(x-3)}{x-3}", r"(x + 4)"], 7, side="^-"), [(1, "factors"), (1, "answer $7$")], work="2.4cm"),
        Part("c", r"Find the value of $b$ for which $f$ is continuous at $x = 3$. Justify your answer.",
             num(3), r"$f(3) = 3b - 2$ and $\displaystyle\lim_{x\to3^+}f(x) = 3b - 2$. Continuity needs $3b - 2 = 7$, so $b = 3$; then "
                     r"$\displaystyle\lim_{x\to3}f(x) = 7 = f(3)$.",
             [(1, "$b = 3$"), (1, "justification: the limit at $x = 3$ equals $f(3)$")], work="2.8cm"),
    ], frq_type="Limits and continuity"),
    FRQ("Reading a graph", r"The graph of $g$ is shown. Let $h(x) = x^2 + 1$.", [
        Part("a", r"For each of $g(0)$ and $\displaystyle\lim_{x\to0}g(x)$, find the value or state that it does not exist.",
             selfcheck(r"g(0) = 1;\ \text{the limit does not exist}"),
             r"$g(0) = 1$. From the left, $x + 3$ heads to $3$; from the right, $x^2 + 1$ heads to $1$. The one-sided limits differ, so the "
             r"limit does not exist.", [(1, "$g(0) = 1$ and both one-sided limits"), (1, "does not exist, with reason")], work="2.4cm"),
        Part("b", r"Is $g$ continuous at $x = 2$? Use the definition of continuity to explain your answer.", selfcheck(r"\text{No}"),
             r"No. $\displaystyle\lim_{x\to2^-}g(x) = 2^2 + 1 = 5$ and $\displaystyle\lim_{x\to2^+}g(x) = 7 - 2 = 5$, so "
             r"$\displaystyle\lim_{x\to2}g(x) = 5$. But $g(2) = 2 \ne 5$, so $g$ is not continuous at $x = 2$.",
             [(1, "$\\displaystyle\\lim_{x\\to2}g(x) = 5$"), (1, "no, because the limit is not equal to $g(2) = 2$")], work="2.6cm"),
        Part("c", r"Find the value of $\displaystyle\lim_{x\to2}\frac{g(x)}{h(x)}$, or show that it does not exist.", num(1),
             r"$\displaystyle\lim_{x\to2}g(x) = 5$ and $\displaystyle\lim_{x\to2}h(x) = 5 \ne 0$, so "
             r"$\displaystyle\lim_{x\to2}\frac{g(x)}{h(x)} = \frac55 = 1$.",
             [(1, "uses both limits"), (1, "answer $1$")], work="2.2cm"),
    ], frq_type="Limits and continuity", figure=FIG2B),
    FRQ("Reservoir inflow", (
        r"The rate at which water flows into a reservoir is modeled by a continuous function $R$, where $R(t)$ is measured in thousands of "
        r"gallons per hour and $t$ is measured in hours, for $0 \le t \le 12$. Selected values of $R(t)$ are given in the table."
        r"\par\smallskip\centerline{\begin{tabular}{c|ccccc} $t$ (hr) & 0 & 2 & 6 & 8 & 12 \\ \hline "
        r"$R(t)$ & 150 & 180 & 170 & 140 & 160\end{tabular}}"), [
        Part("a", r"Find the average rate of change of $R$ over the interval $2 \le t \le 8$. Show the work that leads to your answer. Indicate units of measure.", num(sp.Rational(-20, 3), tol=0.005,
             display=r"-\tfrac{20}{3}\ \text{thousand gal/hr per hr}"),
             r"$\dfrac{140 - 180}{6} = -\dfrac{20}{3} \approx -6.667$ thousand gallons per hour, per hour.",
             [(1, "difference quotient"), (1, "value with units")], work="2.2cm"),
        Part("b", r"For $0 \le t \le 12$, what is the fewest number of times at which $R(t)$ must equal $165$? Give a reason for your answer.", num(2),
             r"$R$ is continuous. $165$ is between $150$ and $180$ (on $[0,2]$) and between $170$ and $140$ (on $[6,8]$). By the IVT, "
             r"$R(t) = 165$ at least twice. (It is not between $180$ and $170$, or between $140$ and $160$.)",
             [(1, "continuity and bracketing values"), (1, "IVT named with conclusion"), (1, "two times")], work="3cm"),
        Part("c", r"Use the data in the table to estimate $R'(7)$. Show the work that leads to your answer.", num(-15),
             r"$\dfrac{R(8) - R(6)}{8 - 6} = \dfrac{140 - 170}{2} = -15$ thousand gallons per hour, per hour.",
             [(1, "estimate $-15$")], work="2cm"),
    ], frq_type="Table", calc=True),
]
same("F2B", [sp.solve(sp.Eq(9 + 3 * a - 12, 0), a)[0], sp.limit((x**2 + x - 12) / (x - 3), x, 3), sp.solve(sp.Eq(3 * b - 2, 7), b)[0],
             sp.limit(x + 3, x, 0), sp.limit(x**2 + 1, x, 0), sp.limit(x**2 + 1, x, 2), 7 - 2, sp.limit(x**2 + 1, x, 2) / (2**2 + 1)],
     [1, 7, 3, 3, 1, 5, 5, 1])

TEST = UnitTest(unit=1, title="Limits and Continuity",
                mcq_a=[Variants(p, q) for p, q in zip(A, A2)],
                mcq_b=[Variants(p, q) for p, q in zip(B, B2)],
                frq=[Variants(p, q) for p, q in zip(FRQS, FRQS2)])
