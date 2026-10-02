"""Topic 1.10: Exploring types of discontinuities.

CED: LIM-2.A.1 (removable, jump, and vertical-asymptote discontinuities). The formula
section matches the video: (x^2 - x - 2)/(x^2 - 4) has a hole at (2, 3/4) and an asymptote at x = -2.
"""
import sympy as sp

from calclib import (VideoExample, Variants, FRQ, MCQ, BigIdea, Check, Example, FigureRow, Formula, Item, Part, Section, Table, limchain,
                     Text, Topic, Video, dne, infinite, num, same, selfcheck)
from calclib.figs import graph

x = sp.symbols("x")
R = (x**2 - x - 2) / (x**2 - 4)
same("hole y", sp.limit(R, x, 2), sp.Rational(3, 4))
same("VA right", sp.limit(R, x, -2, "+"), -sp.oo)
same("VA left", sp.limit(R, x, -2, "-"), sp.oo)

FIG_ALL = graph("t1_10_all", [("0.5*x+2", -4, 2), ("1/(4-x)-1.5", 2, 3.78), ("-1/(x-4)", 4.22, 6)],
                xr=(-4, 6), yr=(-4.5, 5), vlines=[4], open=[(-1, 1.5), (2, 3)], closed=[(-1, 3.5), (2, -1)],
                w="8cm", h="5.2cm", ystep=2, caption=r"Three breaks: at $x=-1$, $x=2$ and $x=4$.")
FIG_RAT = graph("t1_10_rat", [("(x+1)/(x+2)", -6, -2.3), ("(x+1)/(x+2)", -1.7, 5)], xr=(-6, 5), yr=(-3, 5),
                vlines=[-2], open=[(2, 0.75)], w="7cm", h="5cm",
                caption=r"$y = \dfrac{x^2-x-2}{x^2-4}$: a hole at $x = 2$ and an asymptote at $x = -2$.")

NOTES = [
    Video("s1_10.py::Lesson", "Three kinds of breaks", 2.5),

    Section("Three kinds of discontinuity"),
    Text(r"Informally, a function is \textbf{continuous} where you can draw its graph without lifting your pencil. "
         r"Where you must lift it, the function has a \textbf{discontinuity}."),
    FIG_ALL,
    Table(r"\textbf{Removable} & $x = \mblank{-1}$ & a hole; the limit \blank{exists} but differs from the value (or the value is missing) \\ "
          r"\textbf{Jump} & $x = \mblank{2}$ & the one-sided limits exist but are \blank{not equal} \\ "
          r"\textbf{Infinite} & $x = \mblank{4}$ & the function is \blank{unbounded}: a vertical asymptote",
          "lcl", header=r"type & where & what happens"),
    Text(r"A fourth kind, \emph{oscillating}, appears in functions like $\sin\frac1x$ at $0$. It is less common on the exam."),

    Section("Predicting breaks from a rational function"),
    Text(r"\[ \frac{x^2-x-2}{x^2-4} = \frac{(x-2)(x+1)}{(x-2)(x+2)}. \] The factor $x - 2$ \blank{cancels}, which leaves a hole at "
         r"$x = 2$. Its height is $\displaystyle \frac{2+1}{2+2} = \mblank{\tfrac34}$. The factor $x + 2$ stays in the denominator, so there is a "
         r"vertical \blank{asymptote} at $x = -2$."),
    FIG_RAT,
    Formula("Rational functions", (
        r"After factoring $\dfrac{p(x)}{q(x)}$: a zero of $q$ that \textbf{cancels} gives a \blank{removable} discontinuity; "
        r"a zero of $q$ that \textbf{remains} in the denominator gives an \blank{infinite} discontinuity.")),

    Section("Piecewise functions"),
    VideoExample('Where the pieces meet', work="2.2cm"),
    BigIdea(r"Removable: the limit exists. Jump: the one-sided limits disagree. Infinite: the outputs are unbounded."),
    Check(r"$\displaystyle g(x) = \dfrac{x^2-5x+6}{x-3}$ has a removable discontinuity at $x = 3$. What is the $y$-coordinate of the hole?",
          num(1), limchain(3, [r"\frac{(x-3)(x-2)}{x-3}", r"(x-2)"], 1) + r", so the hole is at height $1$."),
]
same("check", sp.limit((x**2 - 5 * x + 6) / (x - 3), x, 3), 1)

# ---------------------------------------------------------------- practice
R4 = (x**2 - 9) / (x**2 - x - 6)
same("p4", sp.limit(R4, x, 3), sp.Rational(6, 5))
PRACTICE = [
    Item(r"The graph from the notes (three breaks) is shown. At what $x$-value is the removable discontinuity?", num(-1),
         r"At $x = -1$ both sides approach $1.5$, but the value is $3.5$.", figure=FIG_ALL, work="1cm"),
    Item(r"At what $x$-value is the jump discontinuity?", num(2), r"At $x = 2$ the sides approach $3$ and $-1$.", work="1cm"),
    Item(r"At what $x$-value is the infinite discontinuity?", num(4), r"At $x = 4$ the graph is unbounded.", work="1cm"),
    Item(r"Let $r(x) = \dfrac{x^2-9}{x^2-x-6}$. Find the $y$-coordinate of the hole in its graph.", num(sp.Rational(6, 5)),
         limchain(3, [r"\frac{(x-3)(x+3)}{(x-3)(x+2)}", r"\frac{x+3}{x+2}"], r"\frac65"), work="2cm"),
    Item(r"Where is the vertical asymptote of $r$ from Problem 4?", num(-2), r"The factor $x + 2$ remains in the denominator.",
         work="1cm"),
    Item(r"Let $g(x) = \begin{cases} 3x, & x < 1 \\ x + 4, & x \ge 1. \end{cases}$ How big is the jump at $x = 1$ "
         r"(right-hand limit minus left-hand limit)?", num(2), r"Right: $5$. Left: $3$. The jump is $5 - 3 = 2$.", work="1.6cm"),
    Item(r"Let $f(x) = \begin{cases} x^2 - 1, & x < 2 \\ 2x - 1, & x \ge 2. \end{cases}$ Find $\displaystyle\lim_{x\to2}f(x)$. "
         r"Does $f$ have a discontinuity at $x = 2$?", num(3),
         r"Both sides give $3$ and $f(2) = 3$. There is no discontinuity at $x = 2$.", work="1.8cm"),
    Item(r"Classify the discontinuity of $\dfrac{|x|}{x}$ at $x = 0$.", selfcheck(r"\text{jump}"),
         r"Jump: the left-hand limit is $-1$ and the right-hand limit is $1$.", work="1.2cm"),
    Item(r"Classify the discontinuity of $\dfrac{1}{(x-5)^2}$ at $x = 5$.", selfcheck(r"\text{infinite}"),
         r"Infinite: the function grows without bound; $x = 5$ is a vertical asymptote.", work="1.2cm"),
    Item(r"Write a formula for a function with a removable discontinuity at $x = 4$ and a vertical asymptote at $x = -1$.",
         selfcheck(r"\text{e.g. } \dfrac{x-4}{(x-4)(x+1)}"),
         r"One answer: $\dfrac{x-4}{(x-4)(x+1)}$. The factor $x - 4$ cancels (hole); $x + 1$ remains (asymptote).", work="2cm"),
]
same("p6", (x + 4).subs(x, 1) - (3 * x).subs(x, 1), 2)

# extra practice (round 1)
PRACTICE += [
    Item(r"Find the $y$-coordinate of the hole in the graph of $y = \dfrac{x^2 + 3x - 10}{x - 2}$.", num(7),
         limchain(2, [r"\frac{(x+5)(x-2)}{x-2}", r"(x+5)"], 7), work="1.8cm"),
    Item(r"Where is the vertical asymptote of $y = \dfrac{x^2 + 3x - 10}{x^2 - 4}$?", num(-2),
         r"$\dfrac{(x+5)(x-2)}{(x-2)(x+2)}$: $x - 2$ cancels, so $x = -2$ is the asymptote.", work="1.8cm"),
    Item(r"Find the $y$-coordinate of the hole in the graph from Problem 12.", num(sp.Rational(7, 4)),
         limchain(2, [r"\frac{x+5}{x+2}"], r"\frac74"), work="1.6cm"),
    Item(r"Let $f(x) = \begin{cases} 4 - x^2, & x < 1 \\ 2x + 1, & x \ge 1. \end{cases}$ Is there a discontinuity at $x = 1$? Enter "
         r"$\displaystyle\lim_{x\to1}f(x)$ or DNE.", num(3), r"Left: $3$. Right: $3$. Value: $3$. No discontinuity.", work="1.8cm"),
    Item(r"Let $g(x) = \begin{cases} x^3, & x < 2 \\ 10 - x, & x \ge 2. \end{cases}$ How big is the jump at $x = 2$ (right minus left)?",
         num(0), r"Left: $8$. Right: $8$. There is no jump.", work="1.6cm"),
    Item(r"Classify the discontinuity of $\dfrac{\sin x}{x}$ at $x = 0$.", selfcheck(r"\text{removable}"),
         r"Removable: the limit is $1$, but the function is undefined at $0$.", work="1.2cm"),
    Item(r"Classify the discontinuity of $\dfrac{x - 3}{|x - 3|}$ at $x = 3$.", selfcheck(r"\text{jump}"),
         r"Jump: the one-sided limits are $-1$ and $1$.", work="1.2cm"),
    Item(r"Classify the discontinuity of $\tan x$ at $x = \frac\pi2$.", selfcheck(r"\text{infinite}"),
         r"Infinite: $\tan x$ is unbounded near $\frac\pi2$.", work="1.2cm"),
    Item(r"How many $x$-values give a removable discontinuity for $\dfrac{x^2 - x}{x^3 - x}$?", num(2),
         r"$\dfrac{x(x-1)}{x(x-1)(x+1)}$: the factors $x$ and $x - 1$ cancel (two holes); $x = -1$ is an asymptote.", work="2cm"),
    Item(r"Sketch a graph with a removable discontinuity at $x = -1$, a jump at $x = 2$, and an infinite discontinuity at $x = 4$.",
         selfcheck(r"\text{hole, jump, asymptote}"), r"Any graph with a hole at $x = -1$, pieces that don't meet at $x = 2$, and a "
                                                         r"vertical asymptote at $x = 4$.", work="3cm"),
]
same("p11", sp.limit((x**2 + 3 * x - 10) / (x - 2), x, 2), 7)
same("p13", sp.limit((x**2 + 3 * x - 10) / (x**2 - 4), x, 2), sp.Rational(7, 4))

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"$q(x) = \dfrac{x^2-4x+3}{x-3}$ has a removable discontinuity at $x = 3$. Find the $y$-coordinate of the hole.",
             num(2), limchain(3, [r"\frac{(x-3)(x-1)}{x-3}", r"(x-1)"], 2), work="1.8cm"),
        Item(r"$q(x) = \dfrac{x^2+2x-8}{x+4}$ has a removable discontinuity at $x = -4$. Find the $y$-coordinate of the hole.",
             num(-6), limchain(-4, [r"\frac{(x+4)(x-2)}{x+4}", r"(x-2)"], -6), work="1.8cm"),
        Item(r"$q(x) = \dfrac{2x^2-2}{x-1}$ has a removable discontinuity at $x = 1$. Find the $y$-coordinate of the hole.",
             num(4), limchain(1, [r"\frac{2(x-1)(x+1)}{x-1}", r"2(x+1)"], 4), work="1.8cm"),
    ),
    Variants(
        Item(r"Where is the vertical asymptote of $h(x) = \dfrac{x+1}{x^2-1}$? Enter the $x$-value.", num(1),
             r"$\dfrac{x+1}{(x-1)(x+1)}$: the factor $x + 1$ cancels, and $x - 1$ remains. The asymptote is $x = 1$.", work="1.8cm"),
        Item(r"Where is the vertical asymptote of $h(x) = \dfrac{x-3}{x^2-x-6}$? Enter the $x$-value.", num(-2),
             r"$\dfrac{x-3}{(x-3)(x+2)}$: the factor $x - 3$ cancels, and $x + 2$ remains. The asymptote is $x = -2$.", work="1.8cm"),
        Item(r"Where is the vertical asymptote of $h(x) = \dfrac{x^2-4x}{x^2-9x+20}$? Enter the $x$-value.", num(5),
             r"$\dfrac{x(x-4)}{(x-4)(x-5)}$: the factor $x - 4$ cancels, and $x - 5$ remains. The asymptote is $x = 5$.", work="1.8cm"),
    ),
    Variants(
        Item(r"Find the $y$-coordinate of the hole in the graph of $h(x) = \dfrac{x+1}{x^2-1}$.", num(sp.Rational(-1, 2)),
             limchain(-1, [r"\frac{x+1}{(x-1)(x+1)}", r"\frac{1}{x-1}"], r"-\frac12"), work="1.5cm"),
        Item(r"Find the $y$-coordinate of the hole in the graph of $h(x) = \dfrac{x-3}{x^2-x-6}$.", num(sp.Rational(1, 5)),
             limchain(3, [r"\frac{x-3}{(x-3)(x+2)}", r"\frac{1}{x+2}"], r"\frac15"), work="1.5cm"),
        Item(r"Find the $y$-coordinate of the hole in the graph of $h(x) = \dfrac{x^2-4x}{x^2-9x+20}$.", num(-4),
             limchain(4, [r"\frac{x(x-4)}{(x-4)(x-5)}", r"\frac{x}{x-5}"], -4), work="1.5cm"),
    ),
    Variants(
        MCQ(r"$\displaystyle\lim_{x\to c^-}f(x) = 4$ and $\displaystyle\lim_{x\to c^+}f(x) = 1$. What kind of discontinuity does $f$ have at $c$?",
            [r"removable", r"jump", r"infinite", r"none"], "B", r"Both one-sided limits exist but differ."),
        MCQ(r"$\displaystyle\lim_{x\to c}f(x) = 5$ but $f(c) = 2$. What kind of discontinuity does $f$ have at $c$?",
            [r"removable", r"jump", r"infinite", r"none"], "A", r"The limit exists; only the value is misplaced. Moving one point fixes it."),
        MCQ(r"$\displaystyle\lim_{x\to c^+}f(x) = \infty$. What kind of discontinuity does $f$ have at $c$?",
            [r"removable", r"jump", r"infinite", r"none"], "C", r"An unbounded side means a vertical asymptote: an infinite discontinuity."),
    ),
    Variants(
        MCQ(r"Which function has a removable discontinuity at $x = 2$?",
            [r"$\dfrac{1}{x-2}$", r"$\dfrac{x}{x-2}$", r"$\dfrac{x^2-4}{x-2}$", r"$\dfrac{x-2}{x^2+4}$"], "C",
            r"The factor $x - 2$ cancels, so the limit at $2$ exists: a hole at $(2, 4)$.",
            why_not={"A": "infinite discontinuity", "B": "infinite discontinuity", "D": "continuous everywhere"}),
        MCQ(r"Which function has a jump discontinuity at $x = 0$?",
            [r"$\dfrac{x^2}{x}$", r"$\dfrac{|x|}{x}$", r"$\dfrac{1}{x^2}$", r"$\dfrac{\sin x}{x}$"], "B",
            r"$\frac{|x|}{x}$ is $-1$ on the left and $1$ on the right.",
            why_not={"A": "removable", "C": "infinite", "D": "removable"}),
        MCQ(r"Which function has an infinite discontinuity at $x = -1$?",
            [r"$\dfrac{x+1}{x^2-1}$", r"$\dfrac{x^2-1}{x+1}$", r"$\dfrac{x-1}{x+1}$", r"$|x+1|$"], "C",
            r"At $x = -1$ the top is $-2$ and the bottom is $0$: the function blows up.",
            why_not={"A": "the factor $x+1$ cancels: removable at $-1$", "B": "removable", "D": "continuous"}),
    ),
]
same("q1", sp.limit((x**2 - 4 * x + 3) / (x - 3), x, 3), 2)
same("q3", sp.limit((x + 1) / (x**2 - 1), x, -1), sp.Rational(-1, 2))
same("q versions", [sp.limit((x**2 + 2 * x - 8) / (x + 4), x, -4), sp.limit((2 * x**2 - 2) / (x - 1), x, 1),
                    sp.limit((x - 3) / (x**2 - x - 6), x, 3), sp.limit((x**2 - 4 * x) / (x**2 - 9 * x + 20), x, 4)],
     [-6, 4, sp.Rational(1, 5), -4])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"Let $f(x) = \dfrac{x^2+x-6}{x^2-4}$. Which describes the discontinuities of $f$?",
        [r"Removable at $x = 2$ and infinite at $x = -2$", r"Infinite at $x = 2$ and $x = -2$",
         r"Removable at $x = -2$ and infinite at $x = 2$", r"Removable at $x = 2$ and $x = -2$"], "A",
        r"$\dfrac{(x+3)(x-2)}{(x-2)(x+2)}$: $x - 2$ cancels, $x + 2$ remains."),
    MCQ(r"Let $g(x) = \dfrac{\sin x}{x}$ for $x \ne 0$ and $g(0) = 0$. At $x = 0$, $g$ has",
        [r"a jump discontinuity", r"an infinite discontinuity", r"a removable discontinuity", r"no discontinuity"], "C",
        r"$\displaystyle\lim_{x\to0}g(x) = 1 \ne 0 = g(0)$. The limit exists, so the discontinuity is removable.",
        why_not={"D": "the limit is $1$ but $g(0) = 0$"}),
    MCQ(r"Which function has a jump discontinuity at $x = 0$?",
        [r"$\dfrac{1}{x^2}$", r"$\dfrac{x^2}{x}$", r"$x\sin\dfrac1x$", r"$\dfrac{x}{|x|}$"], "D",
        r"$\dfrac{x}{|x|}$ is $-1$ for $x<0$ and $1$ for $x > 0$.",
        why_not={"A": "infinite", "B": "removable", "C": "removable (the limit is $0$)"}),
    MCQ(r"Let $k(x) = \begin{cases} x^2 + 1, & x < 2 \\ 7 - x, & x \ge 2. \end{cases}$ At $x = 2$, $k$ is",
        [r"continuous", r"discontinuous with a jump", r"discontinuous with a removable discontinuity", r"undefined"], "A",
        r"Left: $5$. Right: $5$. And $k(2) = 5$. No break.", why_not={"B": "the pieces meet at height 5"}),
]
same("m1 hole", sp.limit((x**2 + x - 6) / (x**2 - 4), x, 2), sp.Rational(5, 4))

F = (x**2 - 1) / (x**2 - 3 * x + 2)
# AP does not ask this topic as free response; the multiple-choice questions above cover it.
# See .claude/skills/ap-frq/SKILL.md.
FRQS = []

TOPIC = Topic(
    number="1.10", title="Exploring Types of Discontinuities",
    unit="Unit 1: Limits and Continuity", ced=["LIM-2.A", "LIM-2.A.1"],
    goals=r"Identify and classify removable, jump and infinite discontinuities from graphs and formulas.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
