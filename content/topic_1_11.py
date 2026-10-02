"""Topic 1.11: Defining continuity at a point.

CED: LIM-2.A.2 (f is continuous at c provided f(c) exists, the limit exists, and they are equal).
The worked justification matches the video: x^2 + 1 (x < 2) and 4x - 3 (x >= 2) at x = 2.
"""
import sympy as sp

from calclib import (VideoExample, Variants, limchain, FRQ, MCQ, BigIdea, Check, Definition, Example, Item, Part, Section, Table, Text, Topic,
                     Video, dne, num, same, selfcheck)
from calclib.figs import graph

x, k = sp.symbols("x k")
same("left", sp.limit(x**2 + 1, x, 2), 5)
# the notes graph: pieces x+1 | x+3 | 5-x | (x-3)^2/2 + 2, with dots at height 3
same("graph x=1", [sp.limit(x + 3, x, 1), sp.limit(5 - x, x, 1)], [4, 4])
same("graph x=3", [sp.limit(5 - x, x, 3), sp.limit((x - 3)**2 / 2 + 2, x, 3)], [2, 2])
same("graph x=-1", [sp.limit(x + 1, x, -1), sp.limit(x + 3, x, -1)], [0, 2])
same("right", sp.limit(4 * x - 3, x, 2), 5)

FIG_T = graph("t1_11_test", [("x+1", -3, -1), ("x+3", -1, 1), ("5-x", 1, 3), ("0.5*(x-3)^2+2", 3, 4.5)],
              xr=(-3, 4.5), yr=(-2.5, 5), open=[(-1, 0), (-1, 2), (1, 4), (3, 2)], closed=[(-1, 3), (1, 3), (3, 3)],
              w="7.6cm", h="5.2cm", caption=r"The graph of $f$.")

NOTES = [
    Video("s1_11.py::Lesson", "Continuity at a point", 2.5),

    Section("The definition"),
    Definition("Continuity at a point", (
        r"A function $f$ is \textbf{continuous at $x = c$} provided \par "
        r"\quad 1. \blank{$f(c)$} exists, \par "
        r"\quad 2. $\displaystyle \lim_{x\to c} f(x)$ \blank{exists}, and \par "
        r"\quad 3. $\displaystyle \lim_{x\to c} f(x) = \mblank{f(c)}$.")),
    Text(r"In one sentence: the limit equals the \blank{value}. If any condition fails, $f$ is discontinuous at $c$."),
    FIG_T,
    Table(r"$x = -1$ & $f(-1) = \mblank{3}$ & limit \blank{does not exist} & condition \mblank{2} fails \\ "
          r"$x = 1$ & $f(1) = \mblank{3}$ & limit $= \mblank{4}$ & condition \mblank{3} fails \\ "
          r"$x = 3$ & $f(3) = \mblank{3}$ & limit $= \mblank{2}$ & condition \mblank{3} fails \\ "
          r"$x = 0$ & $f(0) = \mblank{3}$ & limit $= \mblank{3}$ & \blank{continuous}",
          "llll", header=r"point & value & limit & verdict"),

    Section("Writing a justification"),
    VideoExample('Justify continuity', work="3.6cm"),
    VideoExample('Justify discontinuity', work="3cm"),
    Text(r"\textbf{One-sided continuity.} At an endpoint of a domain, use the one-sided limit. For example, $\sqrt x$ is "
         r"continuous \blank{from the right} at $x = 0$ because \[ \lim_{x\to0^+}\sqrt x = 0 = \sqrt0. \]"),
    BigIdea(r"Continuity at $c$ means the limit equals the function value. A justification names all three pieces: $f(c)$, the limit, "
            r"and the fact that they are equal."),
    Check(r"Let \[ h(x) = \begin{cases} 2x + k, & x < 1 \\ x^2 + 4, & x \ge 1. \end{cases} \] For what value of $k$ is $h$ "
          r"continuous at $x = 1$?", num(3), r"Need $2 + k = 5$, so $k = 3$."),
]
same("ex g", sp.limit((x**2 - 9) / (x - 3), x, 3), 6)
same("check", sp.solve(sp.Eq(2 + k, 5), k)[0], 3)

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Using the graph of $f$ from the notes, find $f(1)$ and $\displaystyle\lim_{x\to1}f(x)$. Enter the limit.", num(4),
         r"$f(1) = 3$ and the limit is $4$, so $f$ is not continuous at $x = 1$.", figure=FIG_T, work="1.4cm"),
    Item(r"Which of the three conditions fails for $f$ at $x = -1$? Enter its number.", num(2),
         r"$f(-1) = 3$ exists, but the one-sided limits are $0$ and $2$, so the limit does not exist.", work="1.4cm"),
    Item(r"Is $p(x) = \begin{cases} x^3, & x \le 1 \\ 2x - 1, & x > 1 \end{cases}$ continuous at $x = 1$? Justify.",
         selfcheck(r"\text{Yes}"),
         r"$p(1) = 1$; left limit $1$, right limit $2 - 1 = 1$. The limit is $1 = p(1)$, so $p$ is continuous at $1$.", work="2.8cm"),
    Item(r"Is $q(x) = \begin{cases} \dfrac{x^2-4}{x+2}, & x \ne -2 \\ -4, & x = -2 \end{cases}$ continuous at $x = -2$? "
         r"Enter the limit, then justify.", num(-4),
         limchain(-2, [r"\frac{x^2-4}{x+2}", r"\frac{(x-2)(x+2)}{x+2}", r"(x-2)"], -4) + r", which equals $q(-2)$. Continuous.", work="2.6cm"),
    Item(r"Find $k$ so that $r(x) = \begin{cases} kx + 1, & x < 3 \\ x^2 - 2, & x \ge 3 \end{cases}$ is continuous at $x = 3$.",
         num(2), r"$3k + 1 = 7$, so $k = 2$.", work="2cm"),
    Item(r"Find $k$ so that $s(x) = \begin{cases} \dfrac{\sin(kx)}{x}, & x \ne 0 \\ 4, & x = 0 \end{cases}$ is continuous at $x = 0$.",
         num(4), r"$\displaystyle\lim_{x\to0}\frac{\sin kx}{x} = k$, so $k = 4$.", work="2cm"),
    Item(r"Explain why $f(x) = \dfrac{1}{x-2}$ is not continuous at $x = 2$, naming the condition that fails.",
         selfcheck(r"f(2)\text{ undefined}"), r"$f(2)$ is undefined, so condition 1 fails (and the limit does not exist either).",
         work="1.8cm"),
    Item(r"Is $g(x) = \sqrt{x - 1}$ continuous from the right at $x = 1$? Explain.", selfcheck(r"\text{Yes}"),
         r"Yes: $g(1) = 0$ and $\displaystyle\lim_{x\to1^+}\sqrt{x-1} = 0$.", work="1.8cm"),
    Item(r"Sketch a function with $f(2) = 3$, $\displaystyle\lim_{x\to2}f(x) = 3$, but which is discontinuous at $x = 4$ "
         r"because $\displaystyle\lim_{x\to4}f(x)$ does not exist.", selfcheck(r"\text{a jump at } x = 4"),
         r"Any graph passing through $(2,3)$ with no break there, and a jump at $x = 4$.", work="3cm"),
]
same("p5", sp.solve(sp.Eq(3 * k + 1, 7), k)[0], 2)
same("p6", sp.limit(sp.sin(4 * x) / x, x, 0), 4)

# extra practice (round 1)
PRACTICE += [
    Item(r"Using the graph of $f$ from the notes, is $f$ continuous at $x = 3$? Enter $\displaystyle\lim_{x\to3}f(x)$.", num(2),
         r"Both one-sided limits are $2$, so the limit is $2$. But $f(3) = 3 \ne 2$, so $f$ is not continuous at $x = 3$.",
         figure=FIG_T, work="1.4cm"),
    Item(r"Using the graph of $f$ from the notes, find $\displaystyle\lim_{x\to0}f(x)$ and decide whether $f$ is continuous "
         r"at $x = 0$.", num(3),
         r"Near $x = 0$ the graph is the line $y = x + 3$ with no break, so the limit is $3 = f(0)$. Continuous.",
         figure=FIG_T, work="1.4cm"),
    Item(r"Is $h(x) = \begin{cases} x^2 - 1, & x < 2 \\ 2x - 1, & x \ge 2 \end{cases}$ continuous at $x = 2$? "
         r"Enter the left-hand limit.", num(3),
         r"$\displaystyle\lim_{x\to2^-}(x^2-1) = 3$ and $\displaystyle\lim_{x\to2^+}(2x-1) = 3$, so the limit is $3$. "
         r"$h(2) = 3$ as well, so $h$ is continuous at $x = 2$.", work="2.4cm"),
    Item(r"Is $m(x) = \begin{cases} 3 - x, & x < 1 \\ x + 2, & x \ge 1 \end{cases}$ continuous at $x = 1$? "
         r"Enter $\displaystyle\lim_{x\to1}m(x)$ (or DNE).", dne(),
         r"$\displaystyle\lim_{x\to1^-}(3-x) = 2$ but $\displaystyle\lim_{x\to1^+}(x+2) = 3$. The one-sided limits differ, "
         r"so the limit does not exist and $m$ is not continuous at $x = 1$.", work="2.4cm"),
    Item(r"Find $k$ so that $u(x) = \begin{cases} x^2 + k, & x \le -1 \\ 3x + 5, & x > -1 \end{cases}$ is continuous "
         r"at $x = -1$.", num(1),
         r"The left piece gives $u(-1) = 1 + k$ and the right-hand limit is $3(-1) + 5 = 2$. Setting $1 + k = 2$ gives $k = 1$.",
         work="2cm"),
    Item(r"Find $k$ so that $v(x) = \begin{cases} \dfrac{x^2 - 9}{x - 3}, & x \ne 3 \\ k, & x = 3 \end{cases}$ is continuous "
         r"at $x = 3$.", num(6),
         limchain(3, [r"\frac{x^2-9}{x-3}", r"\frac{(x-3)(x+3)}{x-3}", r"(x+3)"], 6) + r", so $k = 6$.", work="2cm"),
    Item(r"Find $a$ so that $w(x) = \begin{cases} ax^2, & x < 2 \\ a + 6, & x \ge 2 \end{cases}$ is continuous at $x = 2$.",
         num(2), r"Match the pieces at $x = 2$: $4a = a + 6$, so $3a = 6$ and $a = 2$.", work="2cm"),
    Item(r"Let $f(x) = \dfrac{x^2 + x - 6}{x - 2}$. Which condition for continuity at $x = 2$ fails? Enter its number.",
         num(1),
         r"$f(2)$ is undefined (the denominator is $0$), so condition 1 fails. The limit does exist: "
         + limchain(2, [r"\frac{(x+3)(x-2)}{x-2}", r"(x+3)"], 5) + ".", work="1.8cm"),
    Item(r"A function has $f(5) = 7$, $\displaystyle\lim_{x\to5^-}f(x) = 7$ and $\displaystyle\lim_{x\to5^+}f(x) = 9$. "
         r"Which condition for continuity at $x = 5$ fails? Enter its number.", num(2),
         r"$f(5)$ exists, but the one-sided limits are $7$ and $9$, so $\displaystyle\lim_{x\to5}f(x)$ does not exist. "
         r"Condition 2 fails.", work="1.4cm"),
    Item(r"Is $F(x) = \begin{cases} \dfrac{\sin x}{x}, & x \ne 0 \\ 1, & x = 0 \end{cases}$ continuous at $x = 0$? Justify.",
         selfcheck(r"\text{Yes}"),
         r"$F(0) = 1$, and $\displaystyle\lim_{x\to0}\frac{\sin x}{x} = 1$. The limit exists and equals $F(0)$, so $F$ is "
         r"continuous at $x = 0$.", work="2.2cm"),
]
same("x1 h", [sp.limit(x**2 - 1, x, 2), sp.limit(2 * x - 1, x, 2)], [3, 3])
same("x1 m", [sp.limit(3 - x, x, 1), sp.limit(x + 2, x, 1)], [2, 3])
same("x1 u", sp.solve(sp.Eq(1 + k, 3 * (-1) + 5), k)[0], 1)
same("x1 v", sp.limit((x**2 - 9) / (x - 3), x, 3), 6)
same("x1 w", sp.solve(sp.Eq(4 * k, k + 6), k)[0], 2)
same("x1 f", sp.limit((x**2 + x - 6) / (x - 2), x, 2), 5)
same("x1 F", sp.limit(sp.sin(x) / x, x, 0), 1)

# ---------------------------------------------------------------- quiz
CONT = {"A": "existence of the value alone is not enough", "C": "different formulas can still meet"}
QUIZ = [
    Variants(
        Item(r"Let $f(x) = \begin{cases} x + 5, & x < 1 \\ 3x + 3, & x \ge 1. \end{cases}$ Find $\displaystyle\lim_{x\to1}f(x)$.",
             num(6), r"Left: $1 + 5 = 6$. Right: $3 + 3 = 6$. The limit is $6$.", work="1.6cm"),
        Item(r"Let $f(x) = \begin{cases} x^2 - 1, & x < 2 \\ 2x - 1, & x \ge 2. \end{cases}$ Find $\displaystyle\lim_{x\to2}f(x)$.",
             num(3), r"Left: $4 - 1 = 3$. Right: $4 - 1 = 3$. The limit is $3$.", work="1.6cm"),
        Item(r"Let $f(x) = \begin{cases} 4 - x, & x < -1 \\ x^2 + 1, & x \ge -1. \end{cases}$ Find $\displaystyle\lim_{x\to-1}f(x)$, or type DNE.",
             dne(), r"Left: $4 + 1 = 5$. Right: $1 + 1 = 2$. The sides disagree.", work="1.6cm"),
    ),
    Variants(
        MCQ(r"Let $f(x) = x + 5$ for $x < 1$ and $f(x) = 3x + 3$ for $x \ge 1$. Which statement is correct?",
            [r"$f$ is continuous at $x=1$ because $f(1)$ exists.", r"$f$ is continuous at $x = 1$ because $\displaystyle\lim_{x\to1}f(x) = f(1) = 6$.",
             r"$f$ is not continuous at $x = 1$ because the pieces are different.", r"$f$ is not continuous at $x=1$ because $f(1)=6$."],
            "B", r"Continuity needs the limit to equal the function value; here both are $6$.", why_not=CONT),
        MCQ(r"Let $f(x) = x^2$ for $x < 3$ and $f(x) = x + 5$ for $x \ge 3$. Which statement is correct?",
            [r"$f$ is continuous at $x = 3$ because $f(3) = 8$ exists.", r"$f$ is continuous at $x = 3$ because both pieces are polynomials.",
             r"$f$ is not continuous at $x = 3$ because the one-sided limits are $9$ and $8$.", r"$f$ is not continuous at $x = 3$ because $f(3)$ is undefined."],
            "C", r"From the left, $9$; from the right, $8$. The limit doesn't exist, so condition 2 fails.",
            why_not={"A": CONT["A"], "B": "each piece is continuous, but they must meet at the seam", "D": "$f(3) = 8$ exists"}),
        MCQ(r"Let $f(x) = \dfrac{x^2 - 9}{x - 3}$ for $x \ne 3$ and $f(3) = 6$. Which statement is correct?",
            [r"$f$ is not continuous at $x = 3$ because the formula gives $\frac00$ there.", r"$f$ is not continuous at $x = 3$ because $f(3) \ne 0$.",
             r"$f$ is continuous everywhere except $x = 3$.", r"$f$ is continuous at $x = 3$ because $\displaystyle\lim_{x\to3}f(x) = 6 = f(3)$."], "D",
            r"The limit at $3$ is $3 + 3 = 6$, and $f(3)$ was defined to be $6$. They match.",
            why_not={"A": "$f(3)$ is defined separately as $6$", "C": "it is continuous at $3$ too"}),
    ),
    Variants(
        Item(r"Find $k$ so that $g(x) = \begin{cases} x^2 - k, & x < 2 \\ 3x, & x \ge 2 \end{cases}$ is continuous at $x = 2$.",
             num(-2), r"$4 - k = 6$, so $k = -2$.", work="1.8cm"),
        Item(r"Find $k$ so that $g(x) = \begin{cases} kx + 4, & x < 3 \\ x^2 - 2, & x \ge 3 \end{cases}$ is continuous at $x = 3$.",
             num(1), r"$3k + 4 = 7$, so $k = 1$.", work="1.8cm"),
        Item(r"Find $k$ so that $g(x) = \begin{cases} \dfrac{x^2 - 25}{x - 5}, & x \ne 5 \\ k, & x = 5 \end{cases}$ is continuous at $x = 5$.",
             num(10), limchain(5, [r"\frac{(x-5)(x+5)}{x-5}", r"(x+5)"], 10) + r", so $k = 10$.", work="1.8cm"),
    ),
    Variants(
        MCQ(r"$\displaystyle\lim_{x\to4}h(x) = 7$ and $h(4) = 2$. Which condition of continuity fails at $x = 4$?",
            [r"$h(4)$ exists", r"the limit exists", r"the limit equals $h(4)$", r"none; $h$ is continuous"], "C", r"Both exist, but $7 \ne 2$."),
        MCQ(r"$h(1)$ is undefined, but $\displaystyle\lim_{x\to1}h(x) = 3$. Which condition of continuity fails at $x = 1$?",
            [r"$h(1)$ exists", r"the limit exists", r"the limit equals $h(1)$", r"none; $h$ is continuous"], "A",
            r"The first condition fails: there is no point at $x = 1$."),
        MCQ(r"$h(0) = 1$, $\displaystyle\lim_{x\to0^-}h(x) = 1$ and $\displaystyle\lim_{x\to0^+}h(x) = 4$. Which condition of continuity fails "
            r"at $x = 0$?", [r"$h(0)$ exists", r"the limit exists", r"none; $h$ is continuous", r"the limit equals $h(0)$, but nothing else"], "B",
            r"The one-sided limits differ, so the limit doesn't exist.", why_not={"C": "the right side doesn't match"}),
    ),
    Variants(
        MCQ(r"Which function is continuous at $x = 0$?",
            [r"$\dfrac{|x|}{x}$", r"$\dfrac1x$", r"$\begin{cases}\frac{\sin x}{x}, & x\ne0\\ 1, & x=0\end{cases}$",
             r"$\begin{cases}x^2, & x\ne0\\ 1, & x=0\end{cases}$"], "C",
            r"$\displaystyle\lim_{x\to0}\frac{\sin x}{x} = 1$, which matches the value $1$.",
            why_not={"A": "jump", "B": "infinite discontinuity", "D": "the limit is $0$ but the value is $1$"}),
        MCQ(r"Which function is continuous at $x = 2$?",
            [r"$\begin{cases}x+1, & x<2\\ 2x-1, & x\ge2\end{cases}$", r"$\dfrac{1}{x-2}$", r"$\begin{cases}x^2, & x\ne2\\ 0, & x=2\end{cases}$",
             r"$\dfrac{x-2}{|x-2|}$"], "A", r"Both pieces give $3$ at $x = 2$, and $f(2) = 3$.",
            why_not={"B": "infinite discontinuity", "C": "the limit is $4$ but the value is $0$", "D": "jump"}),
        MCQ(r"Which function is continuous from the right at $x = 0$ but not continuous at $x = 0$?",
            [r"$\sqrt{x}$ on $[0, \infty)$", r"$\begin{cases}-1, & x<0\\ x+2, & x\ge0\end{cases}$", r"$x^2$", r"$\dfrac1x$"], "B",
            r"From the right the limit is $2 = f(0)$, but from the left it is $-1$.",
            why_not={"A": "it's continuous on its whole domain", "C": "continuous at $0$", "D": "undefined at $0$"}),
    ),
]
same("q3", sp.solve(sp.Eq(4 - k, 6), k)[0], -2)
same("q versions", [sp.solve(sp.Eq(3 * k + 4, 7), k)[0], sp.limit((x**2 - 25) / (x - 5), x, 5), 3**2, 3 + 5], [1, 10, 9, 8])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"Let $f(x) = \begin{cases} \dfrac{x^2-2x-3}{x-3}, & x \ne 3 \\ a, & x = 3. \end{cases}$ For what value of $a$ is $f$ "
        r"continuous at $x = 3$?", [r"$0$", r"$3$", r"$4$", r"$6$"], "C",
        limchain(3, [r"\frac{(x-3)(x+1)}{x-3}", r"(x+1)"], 4), why_not={"B": "substituted into $x$ only"}),
    MCQ(r"If $f$ is continuous at $x = 5$ and $f(5) = -2$, which must be true?",
        [r"$\displaystyle\lim_{x\to5}f(x) = -2$", r"$f(x) = -2$ for all $x$ near $5$", r"$f'(5)$ exists",
         r"$\displaystyle\lim_{x\to-2}f(x) = 5$"], "A", r"Continuity means the limit equals the function value.",
        why_not={"C": "continuity does not guarantee a derivative (Unit 2)"}),
    MCQ(r"Let $g(x) = \begin{cases} x^2 + bx, & x < 1 \\ 4, & x = 1 \\ 5 - x, & x > 1. \end{cases}$ Which value of $b$ makes "
        r"$g$ continuous at $x = 1$?", [r"$1$", r"$3$", r"$2$", r"No value of $b$ works"], "B",
        r"The right-hand limit is $5 - 1 = 4$ and $g(1) = 4$. The left-hand limit $1 + b$ must also be $4$, so $b = 3$.",
        why_not={"D": "the right-hand limit already matches $g(1) = 4$, so one value of $b$ works"}),
    MCQ(r"The function $h$ has $\displaystyle\lim_{x\to2^-}h(x) = 3$, $\displaystyle\lim_{x\to2^+}h(x) = 3$ and $h(2)$ undefined. "
        r"Which statement is true?", [r"$h$ is continuous at $2$", r"$h$ has a jump at $2$",
                                      r"$h$ has a removable discontinuity at $2$", r"$h$ has an infinite discontinuity at $2$"], "C",
        r"The limit exists ($3$), but $h(2)$ does not: a hole."),
]
same("m1", sp.limit((x**2 - 2 * x - 3) / (x - 3), x, 3), 4)

FRQS = [
    FRQ("Continuity with a parameter", (
        r"Let $f$ be the function defined by $f(x) = \begin{cases} ax + 2, & x < 1 \\ x^2 + 3, & x \ge 1, \end{cases}$ "
        r"where $a$ is a constant."), [
        Part("a", r"Find the value of $a$ for which $f$ is continuous at $x = 1$. Show the work that leads to your answer.", num(2),
             r"$f(1) = 1 + 3 = 4$ and $\displaystyle\lim_{x\to1^+}f(x) = \lim_{x\to1^+}(x^2+3) = 4$. "
             r"$\displaystyle\lim_{x\to1^-}f(x) = \lim_{x\to1^-}(ax+2) = a + 2$. Continuity at $x = 1$ needs $a + 2 = 4$, so $a = 2$.",
             [(1, "one-sided limits $a + 2$ and $4$ (or $f(1) = 4$)"), (1, "answer $a = 2$")], work="3cm"),
        Part("b", r"Let $a = 3$. Is $f$ continuous at $x = 1$? Use the definition of continuity to explain your answer.",
             selfcheck(r"\text{No}"),
             r"$\displaystyle\lim_{x\to1^-}f(x) = 3(1) + 2 = 5$ and $\displaystyle\lim_{x\to1^+}f(x) = 1 + 3 = 4$. The one-sided limits "
             r"are not equal, so $\displaystyle\lim_{x\to1}f(x)$ does not exist and $f$ is not continuous at $x = 1$.",
             [(1, "both one-sided limits, $5$ and $4$"), (1, "answer no, because the limit does not exist")], work="3cm"),
    ], frq_type="Limits and continuity"),
]
same("frq a", sp.solve(sp.Eq(k + 2, 4), k)[0], 2)
same("frq b", [3 * 1 + 2, 1 + 3], [5, 4])

TOPIC = Topic(
    number="1.11", title="Defining Continuity at a Point",
    unit="Unit 1: Limits and Continuity", ced=["LIM-2.A", "LIM-2.A.2"],
    goals=r"Use the three-part definition to decide and justify whether a function is continuous at a point.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
