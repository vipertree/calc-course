"""Topic 1.9: Connecting multiple representations of limits.

CED: LIM-1.B.1, LIM-1.C, LIM-1.D (synthesis). The centerpiece matches the video: a composite
limit where the inner function (a graph) approaches 3 from above, so the outer piecewise
formula must be read from the right.
"""
import sympy as sp

from calclib import (VideoExample, Variants, FRQ, MCQ, BigIdea, Check, Example, FigureRow, Formula, Item, Part, Section, Table,
                     Text, Topic, Video, dne, num, same, selfcheck)
from calclib.figs import graph

x, u = sp.symbols("x u")
fL, fR = u + 1, 10 - u                      # f(u) = u + 1 (u < 3), 10 - u (u >= 3)
gA = 3 + (x - 2)**2                          # approaches 3 from above
gB = 3 - (x - 2)**2                          # approaches 3 from below
same("f(g) above", sp.limit(fR.subs(u, gA), x, 2), 7)
same("f(g) below", sp.limit(fL.subs(u, gB), x, 2), 4)
for v, want in [(sp.Rational(5, 2), sp.Rational(675, 100)), (sp.Rational(23, 10), sp.Rational(691, 100)),
                (sp.Rational(21, 10), sp.Rational(699, 100))]:
    same(f"table g({v})", fR.subs(u, gA.subs(x, v)), want)

FIG_G = graph("t1_9_g", [("3+(x-2)^2", 0.2, 3.8)], xr=(0, 4), yr=(0, 6.5), w="5.4cm", h="4.6cm",
              caption=r"The graph of $g$.")
FIG_H = graph("t1_9_h", [("3-(x-2)^2", 0.2, 3.8)], xr=(0, 4), yr=(0, 4.5), w="5.4cm", h="4.6cm",
              caption=r"The graph of $h$.")
FIG_HOLE = graph("t1_9_hole", [("x+2", -1, 4.5)], xr=(-1, 4.5), yr=(-0.5, 7), open=[(2, 4)], closed=[(2, 1)],
                 w="5.4cm", h="4.6cm", caption=r"The graph of $f$.")

NOTES = [
    Video("s1_9.py::Lesson", "Four views of a limit", 3),

    Section("Four views of one limit"),
    Text(r"Let $\displaystyle f(x) = \dfrac{x^2-4}{x-2}$ for $x \ne 2$, with $f(2) = 1$. \textbf{Formula:} for $x\ne2$, $f(x) = x + 2$, so "
         r"$\displaystyle \lim_{x\to2} f(x) = \mblank{4}$. \textbf{Graph:} a line with a \blank{hole} at $(2, 4)$ and a dot at "
         r"$(2,1)$. \textbf{Table:} $f(1.99) = \mblank{3.99}$ and $f(2.01) = \mblank{4.01}$. \textbf{Words:} as $x$ gets close "
         r"to $2$, $f(x)$ gets close to $4$, even though $f(2) = 1$."),
    FIG_HOLE,
    Formula("What each view is good at", (
        r"\textbf{Formula:} exact values and algebra. \par "
        r"\textbf{Graph:} one-sided behavior, jumps, holes, asymptotes. \par "
        r"\textbf{Table:} numerical evidence near a point. \par "
        r"\textbf{Words:} meaning and units in context.")),

    Section("Composite limits across representations"),
    FigureRow([FIG_G, FIG_H]),
    Text(r"Let \[ f(u) = \begin{cases} u + 1, & u < 3 \\ 10 - u, & u \ge 3. \end{cases} \] \quad To find "
         r"$\displaystyle \lim_{x\to2} f(g(x))$, work from the inside out. As $x \to 2$, $g(x) \to \mblank{3}$ "
         r"from \blank{above}, so the inputs to $f$ are slightly more than $3$. We need "
         r"$\displaystyle \lim_{u\to3^+} f(u) = \mblank{7}$. So $\displaystyle \lim_{x\to2} f(g(x)) = \mblank{7}$."),
    Text(r"For $h$, the inputs approach $3$ from \blank{below}, so $\displaystyle\lim_{x\to2} f(h(x)) = "
         r"\lim_{u\to3^-} f(u) = \mblank{4}$."),
    BigIdea(r"For $\displaystyle \lim_{x\to c} f(g(x))$: find where $g(x)$ is heading \emph{and from which side}, then take "
            r"that one-sided limit of $f$."),

    Section("Mixing a table and a formula"),
    VideoExample('Table meets formula', work="2.4cm"),
    Check(r"Using the graph of $g$ and the formula for $f$ above, find \[ \lim_{x\to 3} f(g(x)). \]", num(6),
          r"$g(x) \to g(3) = 4$, and $f$ is the single formula $10 - u$ near $u = 4$, so the limit is $10 - 4 = 6$."),
]
same("check", fR.subs(u, gA.subs(x, 3)), 6)
same("frq a L", sp.limit(x**2, x, 3), 9)
same("frq b", sp.limit((2 * u + 1).subs(u, gA), x, 2), 7)
same("frq c", gA.subs(x, sp.limit(x**2, x, 1)), 4)

# ---------------------------------------------------------------- practice
FIG_P = graph("t1_9_p", [("x+1", -2, 1), ("x", 1, 3)], xr=(-2, 3), yr=(-1.5, 3.5), open=[(1, 2), (1, 1)],
              closed=[(1, 3)], caption=r"The graph of $p$.")
PRACTICE = [
    Item(r"The graph of $p$ is shown. Find $\displaystyle\lim_{x\to1^-} p(x)$.", num(2), r"The left piece heads to $2$.",
         figure=FIG_P, work="1.2cm"),
    Item(r"Find $\displaystyle\lim_{x\to1^+} p(x)$.", num(1), r"The right piece heads to $1$.", work="1.2cm"),
    Item(r"Let $q(x) = x^2 - 3$. Find $\displaystyle\lim_{x\to0} p(q(x))$. (Hint: which side of $-3$ do the values of $q$ "
         r"approach from?)", num(-2),
         r"$q(x) = x^2 - 3 \to -3$ from above. Near $u = -3$, $p(u) = u + 1$ is a single formula, so the limit is $-2$.", work="2.2cm"),
    Item(r"Let $r(x) = 1 + x^2$. Find $\displaystyle\lim_{x\to0} p(r(x))$.", num(1),
         r"$r(x) \to 1$ from above, so use $\displaystyle\lim_{u\to1^+}p(u) = 1$.", work="2cm"),
    Item(r"Let $s(x) = 1 - x^2$. Find $\displaystyle\lim_{x\to0} p(s(x))$.", num(2),
         r"$s(x) \to 1$ from below, so use $\displaystyle\lim_{u\to1^-}p(u) = 2$.", work="2cm"),
    Item(r"Let $w(x) = 1 + x$. Find $\displaystyle\lim_{x\to0} p(w(x))$, or type DNE.", dne(),
         r"$w(x) \to 1$ from below when $x<0$ and from above when $x > 0$, giving $2$ and $1$. The limit does not exist.",
         work="2cm"),
    Item(r"Values of $m$ are given."
         r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $x$ & 3.9 & 3.99 & 4.01 & 4.1 \\ \hline "
         r"$m(x)$ & $-0.9$ & $-0.99$ & $-1.01$ & $-1.1$\end{tabular}}"
         r"\par Assuming the pattern continues, find $\displaystyle\lim_{x\to4}\frac{x}{m(x)}$.", num(-4),
         r"$m(x) \to -1$, so the quotient heads to $\dfrac{4}{-1} = -4$.", work="1.8cm"),
    Item(r"The statement ``the population $P(t)$ approaches 5000 as $t$ approaches 10 years'' is given. Write it in limit "
         r"notation and describe what a graph of $P$ would show near $t = 10$.",
         selfcheck(r"\lim_{t\to10}P(t)=5000"),
         r"$\displaystyle\lim_{t\to10}P(t) = 5000$. Near $t=10$ the graph heads to height $5000$ from both sides.", work="2cm"),
]
same("p3", sp.limit((u + 1).subs(u, x**2 - 3), x, 0), -2)

# extra practice (round 1)
PRACTICE += [
    Item(r"Using the graph of $p$, find $\displaystyle\lim_{x\to0}p(1 + x^3)$, or type DNE.", dne(),
         r"$1 + x^3$ approaches $1$ from below when $x < 0$ and from above when $x > 0$, giving $2$ and $1$. The limit does not exist.",
         figure=FIG_P, work="2cm"),
    Item(r"Using the graph of $p$, find $\displaystyle\lim_{x\to2} p(x - 1)$, or type DNE.", dne(),
         r"As $x\to2^-$, $x - 1 \to 1^-$ and $p \to 2$; as $x \to 2^+$, $x - 1 \to 1^+$ and $p \to 1$.", work="2cm"),
    Item(r"Using the graph of $p$, find $\displaystyle\lim_{x\to-1}p(x)$.", num(0), r"The left piece $x + 1$ is unbroken at $-1$: $0$.",
         work="1.2cm"),
    Item(r"Let $f(u) = \begin{cases} 2u, & u < 4 \\ u + 5, & u \ge 4 \end{cases}$ and $g(x) = 4 - x^2$. Find $\displaystyle\lim_{x\to0}f(g(x))$.",
         num(8), r"$g(x) = 4 - x^2$ approaches $4$ from below, so use $\displaystyle\lim_{u\to4^-}2u = 8$.", work="2cm"),
    Item(r"With $f$ from Problem 12 and $h(x) = 4 + x^2$, find $\displaystyle\lim_{x\to0}f(h(x))$.", num(9),
         r"$h(x)$ approaches $4$ from above: $\displaystyle\lim_{u\to4^+}(u + 5) = 9$.", work="1.8cm"),
    Item(r"Values of $m$ near $x = 2$ are given."
         r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $x$ & 1.9 & 1.99 & 2.01 & 2.1 \\ \hline $m(x)$ & 2.9 & 2.99 & 3.01 & 3.1\end{tabular}}"
         r"\par Assuming the pattern continues, find $\displaystyle\lim_{x\to2}\left[m(x)^2 - x\right]$.", num(7),
         r"The table suggests $\displaystyle\lim_{x\to2}m(x) = 3$, so the limit is $9 - 2 = 7$.", work="1.8cm"),
    Item(r"For $m$ in Problem 14, find $\displaystyle\lim_{x\to2}\frac{x}{m(x) - 1}$.", num(1),
         r"$\dfrac{2}{3 - 1} = 1$.", work="1.4cm"),
    Item(r"Translate into limit notation: ``As the price $p$ approaches \$5 from above, the demand $D(p)$ approaches 200 units.''",
         selfcheck(r"\lim_{p\to5^+}D(p)=200"), r"$\displaystyle\lim_{p\to5^+}D(p) = 200$.", work="1.2cm"),
    Item(r"$\displaystyle\lim_{x\to3}f(x) = 4$, and $g$ is continuous with $g(4) = -1$. Find $\displaystyle\lim_{x\to3}g(f(x))$.", num(-1),
         r"$g$ is continuous at $4$, so the limit is $g(4) = -1$.", work="1.4cm"),
    Item(r"Give an example of two functions $f$ and $g$ with $\displaystyle\lim_{x\to0}g(x) = 1$ but $\displaystyle\lim_{x\to0}f(g(x))$ "
         r"not equal to $f(1)$.", selfcheck(r"\text{e.g. } f \text{ with a jump at } 1"),
         r"One example: $f(u) = 0$ for $u < 1$ and $f(u) = 5$ for $u \ge 1$, with $g(x) = 1 - x^2$. Then $f(g(x)) = 0$ near $0$, but $f(1) = 5$.",
         work="2.2cm"),
]
same("p12", sp.limit(2 * (4 - x**2), x, 0), 8)
same("p13", sp.limit((4 + x**2) + 5, x, 0), 9)

# ---------------------------------------------------------------- quiz
FIG_P2 = graph("t1_9_p2", [("2-x", -2, 0), ("x^2-1", 0, 2)], xr=(-2, 2), yr=(-1.5, 4.5), open=[(0, 2), (0, -1)],
               closed=[(0, 0)], caption=r"The graph of $p$.")
FIG_P3 = graph("t1_9_p3", [("0.5*x+1", -1, 2), ("x-1", 2, 4)], xr=(-1, 4), yr=(-0.5, 3.5), open=[(2, 2)],
               closed=[(2, 1)], caption=r"The graph of $p$.")
COMP = {"C": "that is the value at the point", "D": "only one side of $f$ is ever used"}
QUIZ = [
    Variants(
        Item(r"Use the graph of $p$ to find $p(1)$.", num(3), r"The filled dot is at height $3$.", figure=FIG_P, work="1cm"),
        Item(r"Use the graph of $p$ to find $p(0)$.", num(0), r"The filled dot is at height $0$.", figure=FIG_P2, work="1cm"),
        Item(r"Use the graph of $p$ to find $p(2)$.", num(1), r"The filled dot is at height $1$.", figure=FIG_P3, work="1cm"),
    ),
    Variants(
        Item(r"Use the graph of $p$ to find $\displaystyle\lim_{x\to0} p(1 - x^4)$.", num(2),
             r"$1 - x^4$ approaches $1$ from below, so use the left piece: $2$.", figure=FIG_P, work="1.6cm"),
        Item(r"Use the graph of $p$ to find $\displaystyle\lim_{x\to0} p(-x^2)$.", num(2),
             r"$-x^2$ approaches $0$ from below, so use the left piece: $2$.", figure=FIG_P2, work="1.6cm"),
        Item(r"Use the graph of $p$ to find $\displaystyle\lim_{x\to0} p(2 - x^2)$.", num(2),
             r"$2 - x^2$ approaches $2$ from below, so use the left piece: $2$.", figure=FIG_P3, work="1.6cm"),
    ),
    Variants(
        Item(r"Use the graph of $p$ to find $\displaystyle\lim_{x\to0} p(1 + x^4)$.", num(1),
             r"$1 + x^4$ approaches $1$ from above, so use the right piece: $1$.", figure=FIG_P, work="1.6cm"),
        Item(r"Use the graph of $p$ to find $\displaystyle\lim_{x\to0} p(x^2)$.", num(-1),
             r"$x^2$ approaches $0$ from above, so use the right piece: $-1$.", figure=FIG_P2, work="1.6cm"),
        Item(r"Use the graph of $p$ to find $\displaystyle\lim_{x\to0} p(2 + x^2)$.", num(1),
             r"$2 + x^2$ approaches $2$ from above, so use the right piece: $1$.", figure=FIG_P3, work="1.6cm"),
    ),
    Variants(
        MCQ(r"$\displaystyle\lim_{x\to2} g(x) = 5$, and $g(x) < 5$ for all $x$ near $2$. If $f(u) = 3$ for $u < 5$ and $f(u) = 8$ for "
            r"$u \ge 5$, what is $\displaystyle\lim_{x\to2} f(g(x))$?", [r"$3$", r"$5$", r"$8$", r"Does not exist."], "A",
            r"The inputs to $f$ stay below $5$, so $f(g(x)) = 3$ near $x=2$.", why_not={"C": "that is $f(5)$", "D": COMP["D"]}),
        MCQ(r"$\displaystyle\lim_{x\to0} g(x) = 1$, and $g(x) > 1$ for all $x \ne 0$ near $0$. If $f(u) = u^2$ for $u < 1$ and "
            r"$f(u) = 4u$ for $u \ge 1$, what is $\displaystyle\lim_{x\to0} f(g(x))$?", [r"$1$", r"$4$", r"$2$", r"Does not exist."], "B",
            r"The inputs to $f$ stay above $1$, so use $4u$: the limit is $4$.", why_not={"A": "that piece is never used", "D": COMP["D"]}),
        MCQ(r"$\displaystyle\lim_{x\to3} g(x) = 0$, with $g(x) < 0$ on the left of $3$ and $g(x) > 0$ on the right. If "
            r"$f(u) = -1$ for $u < 0$ and $f(u) = 1$ for $u \ge 0$, what is $\displaystyle\lim_{x\to3} f(g(x))$?",
            [r"$-1$", r"$1$", r"$0$", r"Does not exist."], "D",
            r"From the left of $3$, $f(g(x)) = -1$; from the right, $1$. The sides disagree.",
            why_not={"A": "that's only one side", "B": "that's only one side", "C": "that's the inside limit"}),
    ),
    Variants(
        MCQ(r"Which representation directly shows that a limit fails to exist because of a jump?",
            [r"A single value $f(c)$", r"A graph near $x = c$", r"The domain of $f$", r"The range of $f$"], "B",
            r"A graph shows each side of $c$; a jump is visible."),
        MCQ(r"A table shows $f(2.9) = 5.1$, $f(2.99) = 5.01$, $f(3.01) = 4.99$, $f(3.1) = 4.9$. The graph of $f$ shows a filled dot at "
            r"$(3, 1)$. What is $\displaystyle\lim_{x\to3} f(x)$?", [r"$1$", r"$5$", r"Does not exist.", r"$3$"], "B",
            r"The table shows both sides heading to $5$. The dot is the value $f(3)$, which the limit ignores.",
            why_not={"A": "that's $f(3)$", "C": "the two sides agree"}),
        MCQ(r"``As the temperature $T$ approaches $0^\circ$C from above, the time $t(T)$ for ice to form grows without bound.'' "
            r"Which statement matches?", [r"$\displaystyle\lim_{T\to0^+} t(T) = \infty$", r"$t(0) = \infty$",
             r"$\displaystyle\lim_{T\to\infty} t(T) = 0$", r"$\displaystyle\lim_{T\to0^-} t(T) = 0$"], "A",
            r"``Approaches $0$ from above'' is $T \to 0^+$, and ``grows without bound'' is $= \infty$.",
            why_not={"B": "a value, not a limit", "C": "input and output are swapped"}),
    ),
]

# ---------------------------------------------------------------- test prep
FIG_M = graph("t1_9_m", [("2-x", -1, 1), ("x+1", 1, 3)], xr=(-1, 3), yr=(-0.5, 4.5), open=[(1, 1), (1, 2)],
              closed=[(1, 4)], caption=r"The graph of $f$.")
MCQS = [
    MCQ(r"The graph of $f$ is shown. What is $\displaystyle\lim_{x\to0} f(1 + x^2)$?",
        [r"$1$", r"$2$", r"$4$", r"Does not exist."], "B",
        r"$1 + x^2 \to 1$ from above, so the right-hand limit of $f$ at $1$ applies: $2$.",
        why_not={"A": "used the left-hand limit", "C": "used $f(1)$"}, figure=FIG_M),
    MCQ(r"Using the same graph, $\displaystyle\lim_{x\to1}f(x)$ is", [r"$1$", r"$2$", r"$4$", r"Does not exist"], "D",
        r"Left $1$, right $2$."),
    MCQ(r"$f(x) = \dfrac{x^2-9}{x-3}$ for $x \ne 3$ and $f(3) = 0$. Which is true?",
        [r"$\displaystyle\lim_{x\to3}f(x) = 0$", r"The graph of $f$ has a vertical asymptote at $x=3$", r"$\displaystyle\lim_{x\to3}f(x) = 6$",
         r"$\displaystyle\lim_{x\to3}f(x)$ does not exist"], "C", r"For $x\ne3$, $f(x) = x + 3 \to 6$.",
        why_not={"A": "used $f(3)$", "B": "the factor cancels, leaving a hole, not an asymptote"}),
    MCQ(r"A table shows $h(2.9) = 7.1$, $h(2.99) = 7.01$, $h(3.01) = 6.99$, $h(3.1) = 6.9$. Assuming the pattern continues, "
        r"$\displaystyle\lim_{x\to3}\sqrt{h(x) + 2}$ is", [r"$\sqrt7$", r"$7$", r"$9$", r"$3$"], "D",
        r"$h(x) \to 7$, so $\sqrt{h(x)+2} \to \sqrt9 = 3$.", why_not={"C": "forgot the square root"}),
]

# AP does not ask this topic as free response; the multiple-choice questions above cover it.
# See .claude/skills/ap-frq/SKILL.md.
FRQS = []

TOPIC = Topic(
    number="1.9", title="Connecting Multiple Representations of Limits",
    unit="Unit 1: Limits and Continuity", ced=["LIM-1.B.1", "LIM-1.C", "LIM-1.D"],
    goals=r"Move between formulas, graphs, tables and words to find limits, including composite limits where the "
          r"direction of approach matters.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
