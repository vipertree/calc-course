"""Topic 1.3: Estimating limit values from graphs.

CED: LIM-1.C (one-sided limits; graphs; scale can hide behaviour; ways a limit can fail:
unbounded, oscillating, left != right). The CED's own examples appear in section 3:
1/x^2 -> infinity, |x|/x DNE, sin(1/x) DNE, 1/x DNE.
"""
import sympy as sp

from calclib import (Variants, FRQ, MCQ, BigIdea, Check, FigureRow, Formula, Item, Part, Section, Table, Text, Topic, Video,
                     dne, infinite, num, same, selfcheck)
from calclib.figs import graph

x = sp.symbols("x")

FIG_JUMP = graph("t1_3_jump", [("x+1", -1, 2), ("0.5*x+3", 2, 5)], xr=(-1, 5), yr=(-0.5, 6),
                 open=[(2, 3)], closed=[(2, 4)], caption=r"A jump at $x=2$.")
# the multi-feature example
FIG_F = graph("t1_3_f", [("x+3", -4, -1), ("1-x", -1, 2), ("0.5*x", 2, 5)], xr=(-4, 5), yr=(-2, 3.5),
              open=[(-1, 2), (2, -1)], closed=[(-1, 0), (2, 1)], caption=r"The graph of $f$.")
FIG_ABS = graph("t1_3_absx", [("-1", -2, 0), ("1", 0, 2)], xr=(-2, 2), yr=(-2, 2), open=[(0, -1), (0, 1)],
                w="4.6cm", h="3.8cm", caption=r"$y = \dfrac{|x|}{x}$")
FIG_INV2 = graph("t1_3_inv2", [("1/x^2", -2, -0.4), ("1/x^2", 0.4, 2)], xr=(-2, 2), yr=(-0.5, 6), vlines=[0],
                 w="4.6cm", h="3.8cm", ystep=2, caption=r"$y = \dfrac{1}{x^2}$")
FIG_SIN = graph("t1_3_sin", [("sin(deg(1/x))", -1, -0.015), ("sin(deg(1/x))", 0.015, 1)], xr=(-1, 1), yr=(-1.4, 1.4),
                w="4.6cm", h="3.8cm", xstep=1, samples=900, caption=r"$y = \sin\dfrac1x$")

for tag, e, side, want in [("absx L", sp.Abs(x) / x, "-", -1), ("absx R", sp.Abs(x) / x, "+", 1),
                           ("inv2", 1 / x**2, "+", sp.oo), ("inv R", 1 / x, "+", sp.oo), ("inv L", 1 / x, "-", -sp.oo)]:
    same(tag, sp.limit(e, x, 0, side), want)

NOTES = [
    Video("s1_3.py::Lesson", "Limits from graphs", 4),

    Section("One-sided limits"),
    FIG_JUMP,
    Text(r"As $x$ approaches $2$ from the left, the graph heads to height \mblank{3}. From the right it heads to "
         r"height \blank{$4$}."),
    Formula("One-sided limits", (
        r"\[ \lim_{x\to c^-} f(x) = L \quad\text{(left-hand limit)} \qquad\qquad \lim_{x\to c^+} f(x) = R "
        r"\quad\text{(right-hand limit)} \]"
        r"If $f$ is defined on both sides of $c$, the two-sided limit $\displaystyle \lim_{x\to c} f(x)$ exists and equals $L$ "
        r"exactly when \blank{both one-sided limits exist and are equal} to $L$. If the one-sided limits are different, the "
        r"limit \blank{does not exist}.")),
    Text(r"For the jump above, $\displaystyle \lim_{x\to2^-}f(x)=3$ and $\displaystyle \lim_{x\to2^+}f(x)=4$, so "
         r"$\displaystyle \lim_{x\to2}f(x)$ \blank{does not exist}, even though $f(2) = 4$."),

    Text(r"\textbf{At the edge of a domain.} $\sqrt{x}$ is only defined for $x \ge 0$, so near $x = 0$ there is no left side "
         r"to approach from. At an endpoint like this, the limit is the one-sided limit from the side where the function "
         r"lives: \[ \lim_{x\to0}\sqrt{x} = \lim_{x\to0^+}\sqrt{x} = 0. \] Writing the one-sided version, "
         r"$\displaystyle \lim_{x\to0^+}\sqrt{x}$, is always safe, and it is what you will usually see on the AP exam."),

    Section("Reading limits from a graph"),
    FIG_F,
    Table(r"$\displaystyle \lim_{x\to -1} f(x)$ & \mblank{2} & $f(-1)$ & \mblank{0} \\ "
          r"$\displaystyle \lim_{x\to 2^-} f(x)$ & \mblank{-1} & $\displaystyle \lim_{x\to 2^+} f(x)$ & \mblank{1} \\ "
          r"$\displaystyle \lim_{x\to 2} f(x)$ & \blank{does not exist} & $f(2)$ & \mblank{1} \\ "
          r"$\displaystyle \lim_{x\to 0} f(x)$ & \mblank{1} & $\displaystyle \lim_{x\to 4} f(x)$ & \mblank{2}",
          "cccc"),

    Section("Three ways a limit can fail to exist"),
    Table(r"\textbf{Jump} & $\displaystyle \lim_{x\to0^-}\frac{|x|}{x} = -1$, "
          r"$\displaystyle \lim_{x\to0^+}\frac{|x|}{x} = 1$ & the left and right limits disagree \\ "
          r"\textbf{Unbounded} & $\displaystyle \lim_{x\to0}\frac{1}{x^2} = \infty$ & outputs grow without bound \\ "
          r"\textbf{Oscillation} & $\displaystyle \lim_{x\to0}\sin\frac1x$ does not exist & outputs never settle on one value",
          "lll", header=r"type & example & why the limit fails"),
    FigureRow([FIG_ABS, FIG_INV2, FIG_SIN]),
    Text(r"Writing $\displaystyle \lim_{x\to0}\frac1{x^2} = \infty$ describes \emph{how} the limit fails: $\infty$ is not "
         r"a real number, so the limit still does not exist. For $\dfrac1x$, the left side goes to $-\infty$ and the "
         r"right side to $\infty$, so we can only say $\displaystyle \lim_{x\to0}\frac1x$ \blank{does not exist}."),

    Section("Graphs can hide behavior"),
    Text(r"A calculator draws a graph from finitely many points. Graph $y = \dfrac{x^2-1}{x-1}$ and the hole at $(1,2)$ "
         r"is usually invisible. Zoom out too far and small features vanish; zoom in and big ones leave the screen. "
         r"Use a graph to \emph{estimate} a limit, then confirm with a table or with algebra."),
    BigIdea(r"To read a limit from a graph, approach from each side and ask whether both sides head to the same height. "
            r"The point at $x = c$ itself never matters."),
    Check(r"For the graph of $f$ in Section 2, find \[ \lim_{x\to -3} f(x). \]", num(0),
          r"Near $x=-3$ the graph is the line $y=x+3$, which heads to $0$."),
]

# ---------------------------------------------------------------- practice
FIG_G = graph("t1_3_g", [("3/(x+2)", -4, -2.6), ("3/(x+2)", -1.4, 1), ("x+1", 1, 4)], xr=(-4, 4), yr=(-5, 5.5),
              vlines=[-2], open=[(1, 1)], closed=[(1, 2)], ystep=2, caption=r"The graph of $g$.")
same("g piece at 1", (3 / (x + 2)).subs(x, 1), 1)
PRACTICE = [
    Item(r"Use the graph of $g$ to find $\displaystyle\lim_{x\to -2^-} g(x)$.", infinite(-1),
         r"Just left of $x=-2$ the graph drops without bound: $-\infty$. (Type $-\infty$ or $-$infinity.)",
         figure=FIG_G, work="1.2cm"),
    Item(r"Find $\displaystyle\lim_{x\to -2^+} g(x)$.", infinite(1), r"Just right of $x=-2$ the graph rises without bound.",
         work="1.2cm"),
    Item(r"Find $\displaystyle\lim_{x\to 1^-} g(x)$.", num(1), r"The left piece heads to the open circle at height $1$.",
         work="1.2cm"),
    Item(r"Find $\displaystyle\lim_{x\to 1^+} g(x)$.", num(2), r"The right piece starts at height $2$.", work="1.2cm"),
    Item(r"Find $\displaystyle\lim_{x\to 1} g(x)$. If it does not exist, type DNE.", dne(),
         r"The one-sided limits are $1$ and $2$. They disagree, so the limit does not exist.", work="1.2cm"),
    Item(r"Find $g(1)$ and $\displaystyle\lim_{x\to 3} g(x)$. Enter the limit.", num(4),
         r"$g(1) = 2$ (filled dot). Near $x=3$ the graph is $y = x+1$, so the limit is $4$.", work="1.2cm"),
    Item(r"Let $f(x) = \dfrac{|x-3|}{x-3}$. Find $\displaystyle\lim_{x\to 3^+} f(x)$.", num(1),
         r"For $x > 3$, $|x-3| = x-3$, so $f(x) = 1$.", work="1.5cm"),
    Item(r"Explain why $\displaystyle\lim_{x\to0}\frac{1}{x}$ does not exist, and why writing ``$=\infty$'' would be wrong.",
         selfcheck(r"\text{left} \to -\infty,\ \text{right} \to \infty"),
         r"From the left, $\frac1x \to -\infty$; from the right, $\frac1x \to \infty$. The sides go in opposite "
         r"directions, so neither $\infty$ nor $-\infty$ describes the two-sided behavior.", work="2cm"),
    Item(r"Sketch a function with $\displaystyle\lim_{x\to1^-} f(x) = 2$, $\displaystyle\lim_{x\to1^+} f(x) = -1$ and "
         r"$f(1) = 0$.", selfcheck(r"\text{jump at } x=1,\ \text{dot at } (1,0)"),
         r"Any graph arriving at an open circle at $(1,2)$ from the left, leaving from an open circle at $(1,-1)$ on the "
         r"right, with a filled dot at $(1,0)$.", work="3cm"),
    Item(r"Rosa graphs $y = \dfrac{x^2-4}{x-2}$ on her calculator and sees a straight line. She concludes "
         r"``$f(2) = 4$.'' What is wrong, and what is true instead?",
         selfcheck(r"f(2)\text{ undefined; } \lim_{x\to2}=4"),
         r"The function is undefined at $x=2$ (it yields $\frac00$). The screen is too coarse to show the hole. What is "
         r"true is $\displaystyle\lim_{x\to2}\frac{x^2-4}{x-2} = 4$.", work="2.2cm"),
]
same("p7", sp.limit(sp.Abs(x - 3) / (x - 3), x, 3, "+"), 1)

# extra practice (round 1)
FIG_P3 = graph("t1_3_p11", [("2", -4, -2), ("x+4", -2, 0), ("-x+1", 0, 2), ("1/(x-2)", 2.2, 4)], xr=(-4, 4), yr=(-1.5, 5.5),
               vlines=[2], open=[(0, 4), (2, -1)], closed=[(0, 1)], caption=r"The graph of $k$.")
PRACTICE += [
    Item(r"The graph of $k$ is shown. Find $\displaystyle\lim_{x\to-2^-} k(x)$.", num(2), r"The left piece is the constant $2$.",
         figure=FIG_P3, work="1.2cm"),
    Item(r"Find $\displaystyle\lim_{x\to-2^+} k(x)$.", num(2), r"The piece $x + 4$ heads to $2$ as $x \to -2^+$.", work="1.2cm"),
    Item(r"Find $\displaystyle\lim_{x\to-2} k(x)$.", num(2), r"Both one-sided limits equal $2$, so the limit is $2$.", work="1.2cm"),
    Item(r"Find $\displaystyle\lim_{x\to0} k(x)$, or type DNE.", dne(),
         r"$\displaystyle\lim_{x\to0^-}(x+4) = 4$ and $\displaystyle\lim_{x\to0^+}(-x+1) = 1$. The one-sided limits differ.", work="1.2cm"),
    Item(r"Find $k(0)$.", num(1), r"The filled dot at $x = 0$ is at height $1$.", work="1cm"),
    Item(r"Find $\displaystyle\lim_{x\to2^+} k(x)$.", infinite(1), r"Just right of $x = 2$ the graph rises without bound.", work="1.2cm"),
    Item(r"Find $\displaystyle\lim_{x\to2^-} k(x)$.", num(-1), r"The piece $-x + 1$ heads to $-1$.", work="1.2cm"),
    Item(r"Find $\displaystyle\lim_{x\to0^-}\frac{|x|}{x}$.", num(-1), r"For $x < 0$, $|x| = -x$, so the quotient is $-1$.", work="1.2cm"),
    Item(r"Find $\displaystyle\lim_{x\to0}\frac{1}{x^4}$. Use $\infty$ if appropriate.", infinite(1),
         r"$x^4$ is small and positive on both sides, so the quotient grows without bound.", work="1.2cm"),
    Item(r"Does $\displaystyle\lim_{x\to0}\cos\frac1x$ exist? Explain.", selfcheck(r"\text{No: oscillates}"),
         r"No. As $x\to0$, $\frac1x$ grows without bound, so $\cos\frac1x$ keeps swinging between $-1$ and $1$ and never settles.",
         work="1.8cm"),
]
same("fig k -2", [sp.limit(x + 4, x, -2), 2], [2, 2])
same("fig k 0", [sp.limit(x + 4, x, 0), sp.limit(-x + 1, x, 0)], [4, 1])
same("fig k 2", [sp.limit(-x + 1, x, 2), sp.limit(1 / (x - 2), x, 2, "+")], [-1, sp.oo])

# ---------------------------------------------------------------- quiz
FIG_H = graph("t1_3_h", [("-x", -3, 0), ("x^2", 0, 2), ("1", 2, 3)], xr=(-3, 3), yr=(-0.5, 4.5),
              open=[(0, 0), (2, 4)], closed=[(0, 2), (2, 1)], caption=r"The graph of $h$.")
FIG_H2 = graph("t1_3_h2", [("x+2", -3, 1), ("5-2*x", 1, 3)], xr=(-3, 3), yr=(-1.5, 4.5),
               open=[(1, 3)], closed=[(1, -1)], caption=r"The graph of $h$.")
FIG_H3 = graph("t1_3_h3", [("0.5*x^2", -3, -1), ("x+2", -1, 3)], xr=(-3, 3), yr=(-0.5, 5),
               open=[(-1, 0.5), (-1, 1)], closed=[(-1, 3)], caption=r"The graph of $h$.")
FIG_J1 = graph("t1_3_j1", [("x^2", -1, 2), ("1", 2, 3)], xr=(-1, 3), yr=(-0.5, 4.5), open=[(2, 4)], closed=[(2, 1)],
               caption=r"The graph of $g$.")
FIG_J2 = graph("t1_3_j2", [("3-x", -1, 1), ("x+1", 1, 3)], xr=(-1, 3), yr=(-0.5, 4.5), open=[(1, 2)], closed=[(1, 3)],
               caption=r"The graph of $g$.")
FIG_J3 = graph("t1_3_j3", [("0.5*x+3", -1, 2), ("x-1", 2, 4)], xr=(-1, 4), yr=(-0.5, 4.5), open=[(2, 4)], closed=[(2, 1)],
               caption=r"The graph of $g$.")
PW = {"A": "that is only one side", "B": "that is only the other side", "D": "limits are not averaged"}
QUIZ = [
    Variants(
        Item(r"Use the graph of $h$ to find $\displaystyle\lim_{x\to 0} h(x)$.", num(0),
             r"Both sides head to the open circle at the origin. The filled dot at height $2$ doesn't matter.", figure=FIG_H, work="1.2cm"),
        Item(r"Use the graph of $h$ to find $\displaystyle\lim_{x\to 1} h(x)$.", num(3),
             r"Both sides head to the open circle at height $3$. The filled dot at $-1$ doesn't matter.", figure=FIG_H2, work="1.2cm"),
        Item(r"Use the graph of $h$ to find $\displaystyle\lim_{x\to -1} h(x)$, or type DNE.", dne(),
             r"From the left the graph heads to $\frac12$; from the right it heads to $1$. They disagree, so the limit does not exist.",
             figure=FIG_H3, work="1.2cm"),
    ),
    Variants(
        Item(r"Use the graph of $g$ to find $\displaystyle\lim_{x\to 2^-} g(x)$.", num(4), r"From the left, the piece $y = x^2$ heads to $4$.",
             figure=FIG_J1, work="1cm"),
        Item(r"Use the graph of $g$ to find $\displaystyle\lim_{x\to 1^+} g(x)$.", num(2), r"From the right, the piece $y = x + 1$ heads to $2$.",
             figure=FIG_J2, work="1cm"),
        Item(r"Use the graph of $g$ to find $\displaystyle\lim_{x\to 2^+} g(x)$.", num(1), r"From the right, the piece $y = x - 1$ heads to $1$.",
             figure=FIG_J3, work="1cm"),
    ),
    Variants(
        MCQ(r"Let $h(x) = x^2$ for $x < 2$ and $h(x) = 1$ for $x \ge 2$. Which is true about $\displaystyle\lim_{x\to 2} h(x)$?",
            [r"It equals $4$.", r"It equals $1$.", r"Does not exist.", r"It equals $\dfrac{4+1}{2}$."], "C",
            r"From the left the limit is $4$; from the right it is $1$. They disagree.", why_not=PW),
        MCQ(r"Let $k(x) = 3 - x$ for $x < 1$ and $k(x) = x + 1$ for $x \ge 1$. Which is true about $\displaystyle\lim_{x\to 1} k(x)$?",
            [r"It equals $2$.", r"Does not exist.", r"It equals $3$.", r"It equals $1$."], "A",
            r"From the left, $3 - 1 = 2$. From the right, $1 + 1 = 2$. Both sides agree, so the limit is $2$.",
            why_not={"B": "the sides agree here", "C": "that's the left piece at $x = 0$", "D": "that's the input, not the output"}),
        MCQ(r"Let $m(x) = \dfrac{|x - 3|}{x - 3}$. Which is true about $\displaystyle\lim_{x\to 3} m(x)$?",
            [r"It equals $1$.", r"It equals $0$.", r"It equals $-1$.", r"Does not exist."], "D",
            r"From the left $m = -1$; from the right $m = 1$. The sides disagree.",
            why_not={"A": "that's only the right side", "C": "that's only the left side", "B": "limits are not averaged"}),
    ),
    Variants(
        MCQ(r"Near $x = 0$, which function's limit fails to exist because it oscillates?",
            [r"$\dfrac{1}{x^2}$", r"$\sin\dfrac{1}{x}$", r"$\dfrac{|x|}{x}$", r"$x\sin x$"], "B",
            r"$\sin\frac1x$ swings between $-1$ and $1$ infinitely often near $0$.",
            why_not={"A": "unbounded, not oscillating", "C": "a jump", "D": "this limit exists and equals $0$"}),
        MCQ(r"Near $x = 0$, which function's limit fails to exist because it is unbounded?",
            [r"$\cos\dfrac{1}{x}$", r"$\dfrac{|x|}{x}$", r"$\dfrac{1}{x^2}$", r"$x^2 + 1$"], "C",
            r"$\frac{1}{x^2}$ grows without bound on both sides of $0$.",
            why_not={"A": "oscillates", "B": "a jump", "D": "this limit exists and equals $1$"}),
        MCQ(r"Near $x = 0$, which function's limit fails to exist because of a jump?",
            [r"$\dfrac{|x|}{x}$", r"$\sin\dfrac{1}{x}$", r"$\dfrac{1}{x^4}$", r"$\dfrac{\sin x}{x}$"], "A",
            r"$\frac{|x|}{x}$ is $-1$ on the left and $1$ on the right.",
            why_not={"B": "oscillates", "C": "unbounded", "D": "this limit exists and equals $1$"}),
    ),
    Variants(
        Item(r"Use the graph of $h$ to find $h(0)$.", num(2), r"The filled dot is at height $2$.", figure=FIG_H, work="1cm"),
        Item(r"Use the graph of $h$ to find $h(1)$.", num(-1), r"The filled dot is at height $-1$.", figure=FIG_H2, work="1cm"),
        Item(r"Use the graph of $h$ to find $h(-1)$.", num(3), r"The filled dot is at height $3$.", figure=FIG_H3, work="1cm"),
    ),
]
same("q versions", [sp.limit(x**2 / 2, x, -1), sp.limit(x + 2, x, -1), sp.limit(3 - x, x, 1), sp.limit(x + 1, x, 1)],
     [sp.Rational(1, 2), 1, 2, 2])

# ---------------------------------------------------------------- test prep
FIG_K = graph("t1_3_k", [("x+2", -3, -1), ("-x", -1, 1), ("x", 1, 3)], xr=(-3, 3), yr=(-2, 3.2),
              open=[(-1, 1), (1, -1), (1, 1)], closed=[(-1, 2), (1, 0)], caption=r"The graph of $k$.")
MCQS = [
    MCQ(r"The graph of $k$ is shown. Which of the following limits does not exist?",
        [r"$\displaystyle\lim_{x\to -1} k(x)$", r"$\displaystyle\lim_{x\to 0} k(x)$",
         r"$\displaystyle\lim_{x\to 1} k(x)$", r"$\displaystyle\lim_{x\to 2} k(x)$"], "C",
        r"At $x=1$ the left piece $-x$ heads to $-1$ and the right piece $x$ heads to $1$, so the limit does not exist. "
        r"At $x=-1$ both sides head to $1$ (the dot at height $2$ doesn't matter); at $0$ and $2$ the graph is unbroken.",
        why_not={"A": "the dot at $(-1,2)$ is not the limit; both sides approach $1$"}, figure=FIG_K),
    MCQ(r"$\displaystyle\lim_{x\to3^-} f(x) = 5$, $\displaystyle\lim_{x\to3^+} f(x) = 5$ and $f(3) = 2$. "
        r"What is $\displaystyle\lim_{x\to3} f(x)$?",
        [r"$2$", r"$5$", r"$\dfrac72$", r"Does not exist."], "B",
        r"Both one-sided limits equal $5$, so the limit is $5$. The value $f(3)$ does not matter.",
        why_not={"A": "used the value at $3$", "C": "averaged the limit and the value", "D": "the sides agree, so it exists"}),
    MCQ(r"$\displaystyle\lim_{x\to 0^+}\frac{2}{x}$ is", [r"$0$", r"$2$", r"$\infty$", r"$-\infty$"], "C",
        r"For small positive $x$, $\frac2x$ is large and positive, and grows without bound.",
        why_not={"D": "that is the left-hand limit"}),
    MCQ(r"Which of the following limits exist? \par I. $\displaystyle\lim_{x\to0}\frac{|x|}{x}$ \quad "
        r"II. $\displaystyle\lim_{x\to0} x\sin\frac1x$ \quad III. $\displaystyle\lim_{x\to0}\frac1{x^2}$",
        [r"II only", r"I and II only", r"II and III only", r"I, II and III"], "A",
        r"I is a jump ($-1$ and $1$). III is unbounded. In II, $\sin\frac1x$ stays between $-1$ and $1$ while $x \to 0$, "
        r"so the product is squeezed to $0$ (Topic 1.8 proves it).",
        why_not={"C": "$\\lim \\frac1{x^2} = \\infty$ describes an unbounded limit, which does not exist"}),
]
same("m4 II", sp.limit(x * sp.sin(1 / x), x, 0), 0)

FIG_Q = graph("t1_3_q", [("x+2", -2, 1), ("4-x", 1, 3), ("3", 3, 5)], xr=(-2, 5), yr=(-0.5, 4.5),
              open=[(1, 3), (3, 1)], closed=[(1, 1), (3, 3)], caption=r"The graph of $q$.")
FRQS = [
    FRQ("Reading a graph", r"The graph of the function $q$ is shown for $-2 \le x \le 5$.", [
        Part("a", r"Find $\displaystyle\lim_{x\to1} q(x)$, or state that it does not exist. Give a reason for your answer.", num(3),
             r"As $x \to 1^-$, $q(x) = x + 2 \to 3$, and as $x \to 1^+$, $q(x) = 4 - x \to 3$. Both one-sided limits are $3$, so "
             r"$\displaystyle\lim_{x\to1} q(x) = 3$. (The filled dot at $q(1) = 1$ does not affect the limit.)",
             [(1, "answer $3$ with both one-sided limits")], work="2.2cm"),
        Part("b", r"For each of $\displaystyle\lim_{x\to3^-} q(x)$, $\displaystyle\lim_{x\to3^+} q(x)$ and $\displaystyle\lim_{x\to3} q(x)$, "
                  r"find the value or state that it does not exist.",
             selfcheck(r"1,\ 3,\ \text{Does not exist}"),
             r"From the left, $q(x) = 4 - x \to 1$. From the right, $q(x) = 3$. Since $\displaystyle\lim_{x\to3^-}q(x) = 1 \ne 3 = "
             r"\lim_{x\to3^+}q(x)$, the two-sided limit $\displaystyle\lim_{x\to3} q(x)$ does not exist.",
             [(1, "left-hand limit $1$"), (1, "right-hand limit $3$"), (1, "does not exist, because the one-sided limits differ")],
             work="2.6cm"),
    ], frq_type="Continuity / limits from a graph", figure=FIG_Q),
]

TOPIC = Topic(
    number="1.3", title="Estimating Limit Values from Graphs",
    unit="Unit 1: Limits and Continuity", ced=["LIM-1.C", "LIM-1.C.1", "LIM-1.C.2", "LIM-1.C.3", "LIM-1.C.4"],
    goals=r"Read one-sided and two-sided limits from a graph, and recognize the ways a limit can fail to exist.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
