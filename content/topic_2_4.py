"""Topic 2.4: Connecting differentiability and continuity.

CED: FUN-2.A (differentiability implies continuity; continuity does not imply differentiability;
corners, cusps, vertical tangents and discontinuities). The piecewise check matches the video:
x^2 (x <= 1) and 2x - 1 (x > 1) are differentiable at 1.
"""
import sympy as sp

from calclib import (Variants, FRQ, MCQ, BigIdea, Check, Definition, Example, FigureRow, Formula, Item, Part, Section,
                     Table, Text, Topic, Video, VideoExample, num, same, selfcheck)
from calclib.figs import graph

x, a, b, k = sp.symbols("x a b k")
same("seam value", [(x**2).subs(x, 1), (2 * x - 1).subs(x, 1)], [1, 1])
same("seam slope", [sp.diff(x**2, x).subs(x, 1), sp.diff(2 * x - 1, x)], [2, 2])

FIG_CORNER = graph("t2_4_corner", [("abs(x)", -2, 2)], xr=(-2, 2), yr=(-0.5, 2.2), w="4.4cm", h="3.6cm", caption="corner")
FIG_CUSP = graph("t2_4_cusp", [("(x^2)^(1/3)", -2, 2)], xr=(-2, 2), yr=(-0.5, 2.2), w="4.4cm", h="3.6cm", samples=300,
                 caption="cusp")
FIG_VERT = graph("t2_4_vert", [("-(-x)^(1/3)", -2, 0), ("x^(1/3)", 0, 2)], xr=(-2, 2), yr=(-1.6, 1.6), w="4.4cm", h="3.6cm",
                 samples=300, caption="vertical tangent")
FIG_JUMP = graph("t2_4_jump", [("x+1", -2, 0), ("x-1", 0, 2)], xr=(-2, 2), yr=(-2, 2), open=[(0, 1)], closed=[(0, -1)],
                 w="4.4cm", h="3.6cm", caption="discontinuity")

NOTES = [
    Video("s2_4.py::Lesson", "When derivatives fail", 3),

    Section("Differentiable means locally linear"),
    Definition("Differentiable", (
        r"$f$ is \textbf{differentiable at $x = c$} if $f'(c)$ \blank{exists}. Graphically, zooming in near $(c, f(c))$ makes the "
        r"graph look more and more like a single non-vertical \blank{line}: the graph is \emph{locally linear}.")),
    Text(r"Zoomed in near the origin, $y = \sin(2x) + 0.001$ looks exactly like the line $y = \mblank{2x + 0.001}$, its tangent line there. "
         r"Zoom out and it's a wave. Up close, a differentiable function looks like its tangent line."),

    Section("Four ways a derivative can fail"),
    FigureRow([FIG_CORNER, FIG_CUSP, FIG_VERT, FIG_JUMP]),
    Table(r"corner & $|x|$ at $0$ & left slope $\mblank{-1}$, right slope $\mblank{1}$ \\ "
          r"cusp & $x^{2/3}$ at $0$ & slopes go to $-\infty$ and $\infty$ \\ "
          r"vertical tangent & $x^{1/3}$ at $0$ & slope is \blank{infinite} \\ "
          r"discontinuity & a jump or hole & no tangent line at all", "lll", header=r"feature & example & why $f'(c)$ fails"),
    Text(r"\textbf{What the pictures are really asking:} does the limit in the definition of the derivative \blank{exist}? For $|x|$ at $0$ it is "
         r"\[ \lim_{h\to 0}\frac{|h|}{h}, \] which is $-1$ from the left and $1$ from the right, so it doesn't exist. At a cusp or a vertical tangent, the quotients blow up."),

    Section("Differentiability and continuity"),
    Formula("A one-way relationship", (
        r"If $f$ is differentiable at $c$, then $f$ is \blank{continuous} at $c$. \par "
        r"The converse is \blank{false}: $|x|$ is continuous at $0$ but not differentiable there.")),
    Text(r"So a discontinuity guarantees the derivative fails, but continuity is not enough to guarantee a derivative: it guarantees \blank{nothing} about the derivative."),

    Section("Piecewise functions"),
    VideoExample("Check value and slope", work="3cm"),
    Formula("Differentiable at a seam $x = c$", (
        r"1. The pieces have the same \blank{value} at $c$ (continuity). \par "
        r"2. The pieces have the same \blank{slope} at $c$ (the one-sided derivatives agree).")),
    BigIdea(r"Differentiable implies continuous, never the other way around. Check both value and slope at a seam."),
    Check(r"Find $k$ so that \[ g(x) = \begin{cases} x^2 + k, & x \le 2 \\ 4x - 1, & x > 2 \end{cases} \] is continuous at $x = 2$. "
          r"(With that $k$, the slopes also match: $2x = 4$ and $4$.)", num(3), r"$4 + k = 7$, so $k = 3$."),
]
same("check k", sp.solve(sp.Eq(4 + k, 7), k)[0], 3)

# ---------------------------------------------------------------- practice
FIG_P = graph("t2_4_p", [("-x-1", -4, -2), ("x+3", -2, 0), ("3-0.5*x^2", 0, 2), ("1", 2, 3), ("x-1", 3, 4.5)],
              xr=(-4, 4.5), yr=(-1, 4), open=[(2, 1)], closed=[(2, 2.5)], w="7.4cm", h="4.6cm", caption=r"The graph of $f$.")
PRACTICE = [
    Item(r"The graph of $f$ is shown. At how many of the $x$-values $-2$, $0$, $2$ and $3$ is $f$ NOT differentiable?", num(4),
         r"$x = -2$: corner (slopes $-1$ and $1$). $x = 0$: corner (slopes $1$ and $0$). $x = 2$: discontinuity. "
         r"$x = 3$: corner (slopes $0$ and $1$). All four.", figure=FIG_P, work="2cm"),
    Item(r"At which of those $x$-values is $f$ continuous but not differentiable? Enter how many.", num(3),
         r"$-2$, $0$ and $3$ (the corners). At $2$ it is not even continuous.", work="1.6cm"),
    Item(r"Is $g(x) = |x - 4|$ differentiable at $x = 4$? Explain.", selfcheck(r"\text{No: corner}"),
         r"No. Left slope $-1$, right slope $1$: a corner.", work="1.6cm"),
    Item(r"Is $h(x) = \sqrt[3]{x - 1}$ differentiable at $x = 1$? Explain.", selfcheck(r"\text{No: vertical tangent}"),
         r"No. The graph has a vertical tangent at $x = 1$: the difference quotient $\dfrac{\sqrt[3]{h}}{h}$ grows without bound "
         r"as $h \to 0$.", work="1.6cm"),
    Item(r"Let $p(x) = \begin{cases} x^2 - 2x, & x < 3 \\ 4x - 9, & x \ge 3. \end{cases}$ Is $p$ differentiable at $x = 3$? "
         r"Enter the left-hand slope at $x=3$.", num(4),
         r"Values: $9 - 6 = 3$ and $12 - 9 = 3$. Slopes: $2x - 2 = 4$ and $4$. Differentiable, with $p'(3) = 4$.", work="2.4cm"),
    Item(r"Let $q(x) = \begin{cases} x^2, & x < 1 \\ 3x - 2, & x \ge 1. \end{cases}$ Is $q$ differentiable at $x = 1$? Enter the "
         r"right-hand slope.", num(3),
         r"Values: $1$ and $1$ (continuous). Slopes: $2$ and $3$. They differ, so $q$ is not differentiable at $1$.", work="2.4cm"),
    Item(r"Find $a$ and $b$ so that $r(x) = \begin{cases} ax^2, & x \le 2 \\ 4x + b, & x > 2 \end{cases}$ is differentiable at "
         r"$x = 2$. Enter $a$.", num(1),
         r"Slopes: $4a = 4$, so $a = 1$. Values: $4a = 8 + b$, so $b = -4$.", work="2.6cm"),
    Item(r"True or false: if $f$ is continuous at $x = 5$, then $f'(5)$ exists. Explain.", selfcheck(r"\text{False}"),
         r"False. $|x - 5|$ is continuous at $5$ but has a corner there.", work="1.6cm"),
    Item(r"True or false: if $f'(5)$ exists, then $\displaystyle\lim_{x\to5}f(x) = f(5)$. Explain.", selfcheck(r"\text{True}"),
         r"True. Differentiability implies continuity, and continuity means the limit equals the value.", work="1.6cm"),
]
same("p5", [(x**2 - 2 * x).subs(x, 3), 4 * 3 - 9, sp.diff(x**2 - 2 * x, x).subs(x, 3)], [3, 3, 4])
s7 = sp.solve([sp.Eq(4 * a, 4), sp.Eq(4 * a, 8 + b)], [a, b])
same("p7", [s7[a], s7[b]], [1, -4])

# extra practice (round 1)
PRACTICE += [
    Item(r"Using the graph of $f$ from Problem 1, find $f'(-1)$.", num(1),
         r"On $(-2, 0)$ the graph is the line $y = x + 3$, so the slope is $1$.", figure=FIG_P, work="1.2cm"),
    Item(r"Using the same graph, find $f'(2.5)$.", num(0), r"On $(2, 3)$ the graph is the horizontal line $y = 1$: slope $0$.",
         work="1.2cm"),
    Item(r"Is $g(x) = |x + 2|$ differentiable at $x = -2$? Enter the slope from the right.", num(1),
         r"From the left the slope is $-1$ and from the right it is $1$. The slopes differ (a corner), so $g$ is not "
         r"differentiable at $-2$.", work="1.6cm"),
    Item(r"Is $f(x) = x^{2/3}$ differentiable at $x = 0$? Name the feature of the graph.", selfcheck(r"\text{No: cusp}"),
         r"No. The graph has a cusp at the origin: it comes in steeply downward and leaves steeply upward.", work="1.6cm"),
    Item(r"Let $s(x) = \begin{cases} x^2 + 1, & x < 1 \\ 2x, & x \ge 1. \end{cases}$ Is $s$ differentiable at $x = 1$? "
         r"Enter $s'(1)$ if it exists.", num(2),
         r"Values: $1 + 1 = 2$ and $2(1) = 2$, so $s$ is continuous. Slopes: $2x = 2$ and $2$. They match, so $s'(1) = 2$.",
         work="2.4cm"),
    Item(r"Let $u(x) = \begin{cases} x^3, & x < 1 \\ 3x - 2, & x \ge 1. \end{cases}$ Is $u$ differentiable at $x = 1$? "
         r"Enter $u'(1)$ if it exists.", num(3),
         r"Values: $1$ and $3 - 2 = 1$. Slopes: $3x^2 = 3$ and $3$. Both match, so $u'(1) = 3$.", work="2.4cm"),
    Item(r"Let $v(x) = \begin{cases} 2x + 1, & x < 2 \\ x^2 + 1, & x \ge 2. \end{cases}$ Is $v$ differentiable at $x = 2$? "
         r"Enter the left-hand slope.", num(2),
         r"Values: $5$ and $5$, so $v$ is continuous. Slopes: $2$ from the left, $2x = 4$ from the right. They differ, so $v$ "
         r"has a corner and is not differentiable at $2$.", work="2.4cm"),
    Item(r"Let $w(x) = \begin{cases} x^2, & x < 0 \\ x + 1, & x \ge 0. \end{cases}$ Both pieces have slope near $0$ and $1$ "
         r"respectively. Is $w$ differentiable at $x = 0$? Explain.", selfcheck(r"\text{No: not continuous}"),
         r"No. $\displaystyle\lim_{x\to0^-}x^2 = 0$ but $w(0) = 1$, so $w$ is not continuous at $0$. A function that is not "
         r"continuous cannot be differentiable.", work="2cm"),
    Item(r"Find $a$ and $b$ so that $\begin{cases} x^3, & x \le 1 \\ ax + b, & x > 1 \end{cases}$ is differentiable at $x = 1$. "
         r"Enter $b$.", num(-2),
         r"Slopes: $3x^2 = 3$ at $x = 1$, so $a = 3$. Values: $1 = a + b = 3 + b$, so $b = -2$.", work="2.4cm"),
    Item(r"Write a function that is continuous everywhere but not differentiable at $x = 1$ and at $x = 4$.",
         selfcheck(r"\text{e.g. } |x-1| + |x-4|"),
         r"For example $|x - 1| + |x - 4|$, which has corners at both points.", work="1.6cm"),
]
same("x1 s", [(x**2 + 1).subs(x, 1), 2, sp.diff(x**2 + 1, x).subs(x, 1)], [2, 2, 2])
same("x1 u", [1, 3 - 2, sp.diff(x**3, x).subs(x, 1)], [1, 1, 3])
same("x1 v", [2 * 2 + 1, 2**2 + 1, sp.diff(x**2 + 1, x).subs(x, 2)], [5, 5, 4])
s9 = sp.solve([sp.Eq(a, 3), sp.Eq(1, a + b)], [a, b])
same("x1 ab", s9[b], -2)

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"Which function is continuous but not differentiable at $x = 0$?",
            [r"$x^2$", r"$|x|$", r"$\dfrac{1}{x}$", r"$\dfrac{x}{|x|}$"], "B", r"$|x|$ has a corner at $0$.",
            why_not={"A": "differentiable", "C": "not continuous", "D": "not continuous"}),
        MCQ(r"Which function is continuous but not differentiable at $x = 3$?",
            [r"$(x-3)^2$", r"$\dfrac{1}{x-3}$", r"$\sqrt[3]{x-3}$", r"$\dfrac{|x-3|}{x-3}$"], "C",
            r"$\sqrt[3]{x-3}$ is continuous at $3$ but has a vertical tangent there.",
            why_not={"A": "differentiable", "B": "not continuous", "D": "not continuous"}),
        MCQ(r"Which function is differentiable at $x = 1$?",
            [r"$|x - 1|$", r"$(x-1)^{2/3}$", r"$\dfrac{1}{x-1}$", r"$(x-1)^3$"], "D", r"$(x-1)^3$ is a polynomial: smooth everywhere.",
            why_not={"A": "corner", "B": "cusp", "C": "not even continuous"}),
    ),
    Variants(
        MCQ(r"If $f$ is not continuous at $x = 2$, then",
            [r"$f'(2) = 0$", r"$f'(2)$ does not exist", r"$f'(2)$ may exist", r"$f(2)$ does not exist"], "B",
            r"Differentiability requires continuity."),
        MCQ(r"If $f'(4)$ exists, then",
            [r"$f$ is continuous at $x = 4$", r"$f'(4) \ne 0$", r"$f$ has a corner at $x = 4$", r"$f(4) = 0$"], "A",
            r"Differentiable implies continuous."),
        MCQ(r"$f$ is continuous at $x = 0$. Which must be true?",
            [r"$f'(0)$ exists", r"$\displaystyle\lim_{x\to0}f(x) = f(0)$", r"$f'(0) = 0$", r"$f$ has no corner at $0$"], "B",
            r"That is what continuity means. Continuity does not guarantee a derivative.", why_not={"A": "$|x|$ is a counterexample"}),
    ),
    Variants(
        Item(r"Let $g(x) = \begin{cases} x^3, & x \le 1 \\ 3x - 2, & x > 1. \end{cases}$ Find the left-hand slope at $x = 1$.", num(3),
             r"$3x^2 = 3$ at $x=1$; the right piece also has slope $3$ and the values match ($1$), so $g$ is differentiable at $1$.", work="2cm"),
        Item(r"Let $g(x) = \begin{cases} x^2 + 2, & x \le 2 \\ 4x - 2, & x > 2. \end{cases}$ Find the left-hand slope at $x = 2$.", num(4),
             r"$2x = 4$ at $x = 2$; the right piece has slope $4$ and both pieces give $6$, so $g$ is differentiable at $2$.", work="2cm"),
        Item(r"Let $g(x) = \begin{cases} x^2, & x \le 0 \\ 2x, & x > 0. \end{cases}$ Find the right-hand slope at $x = 0$.", num(2),
             r"The right piece has slope $2$. The left piece has slope $2x = 0$ at $0$. The slopes differ, so $g$ has a corner at $0$.", work="2cm"),
    ),
    Variants(
        Item(r"Find $k$ so that $\begin{cases} kx^2, & x \le 1 \\ 6x - 3, & x > 1 \end{cases}$ is differentiable at $x = 1$.", num(3),
             r"Slopes: $2k = 6$, so $k = 3$. Values: $3 = 6 - 3$. Both match.", work="2cm"),
        Item(r"Find $k$ so that $\begin{cases} x^2 + k, & x \le 2 \\ 4x, & x > 2 \end{cases}$ is differentiable at $x = 2$.", num(4),
             r"Slopes: $2x = 4$ matches the line's slope. Values: $4 + k = 8$, so $k = 4$.", work="2cm"),
        Item(r"Find $k$ so that $\begin{cases} kx^3, & x \le 1 \\ 6x - 4, & x > 1 \end{cases}$ is differentiable at $x = 1$.", num(2),
             r"Slopes: $3k = 6$, so $k = 2$. Values: $2 = 6 - 4$. Both match.", work="2cm"),
    ),
    Variants(
        MCQ(r"The graph of $y = x^{1/3}$ at $x = 0$ has", [r"a corner", r"a cusp", r"a vertical tangent", r"a jump"], "C",
            r"The graph passes smoothly through the origin but becomes vertical there."),
        MCQ(r"The graph of $y = x^{2/3}$ at $x = 0$ has", [r"a cusp", r"a corner", r"a vertical tangent", r"a jump"], "A",
            r"Both sides come in steeply and meet at a sharp point: a cusp."),
        MCQ(r"The graph of $y = |x + 2|$ at $x = -2$ has", [r"a cusp", r"a vertical tangent", r"a jump", r"a corner"], "D",
            r"Slopes $-1$ and $1$ meet at a point: a corner."),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"Let $f(x) = \begin{cases} x^2 + 1, & x \le 1 \\ 2x, & x > 1. \end{cases}$ Which is true at $x = 1$?",
        [r"$f$ is differentiable", r"$f$ is continuous but not differentiable", r"$f$ is differentiable but not continuous",
         r"$f$ is neither continuous nor differentiable"], "A",
        r"Values: $2$ and $2$. Slopes: $2x = 2$ and $2$. Both match.", why_not={"C": "impossible: differentiable implies continuous"}),
    MCQ(r"For which value of $x$ is $f(x) = |x^2 - 4|$ not differentiable?", [r"$0$", r"$4$", r"$2$", r"$1$"], "C",
        r"$x^2 - 4$ changes sign at $x = \pm2$, creating corners.", why_not={"A": "the graph is smooth at $0$ (a local max)"}),
    MCQ(r"Which statement must be true?",
        [r"If $f$ is continuous at $c$, then $f$ is differentiable at $c$.", r"If $f'(c)$ does not exist, then $f$ is not continuous at $c$.",
         r"If $f(c)$ is undefined, then $f'(c)$ exists.", r"If $f$ is differentiable at $c$, then $f$ is continuous at $c$."], "D",
        r"Only the forward direction holds."),
    MCQ(r"Let $g(x) = \begin{cases} ax + b, & x < 2 \\ x^2, & x \ge 2. \end{cases}$ For which $a$ and $b$ is $g$ differentiable at $x=2$?",
        [r"$a = 4$, $b = -4$", r"$a = 2$, $b = 0$", r"$a = 4$, $b = 4$", r"$a = 4$, $b = 0$"], "A",
        r"Slope: $a = 4$. Value: $2a + b = 4$, so $b = -4$."),
]
s4 = sp.solve([sp.Eq(a, 4), sp.Eq(2 * a + b, 4)], [a, b])
same("m4", [s4[a], s4[b]], [4, -4])

FRQS = [
    FRQ("Differentiability at a seam", (
        r"Let $f$ be the function defined by $f(x) = \begin{cases} x^2 - 4x + 7, & x \le 3 \\ mx + c, & x > 3, \end{cases}$ "
        r"where $m$ and $c$ are constants."), [
        Part("a", r"Let $m = 5$ and $c = -11$. Is $f$ continuous at $x = 3$? Use the definition of continuity to explain your answer.",
             selfcheck(r"\text{Yes}"),
             r"$f(3) = 9 - 12 + 7 = 4$. $\displaystyle\lim_{x\to3^-}f(x) = 4$ and $\displaystyle\lim_{x\to3^+}(5x - 11) = 4$, so "
             r"$\displaystyle\lim_{x\to3}f(x) = 4 = f(3)$. Therefore $f$ is continuous at $x = 3$.",
             [(1, "$f(3) = 4$ and both one-sided limits equal $4$"), (1, "yes, because the limit equals $f(3)$")], work="2.8cm"),
        Part("b", r"Let $m = 5$ and $c = -11$. Is $f$ differentiable at $x = 3$? Justify your answer.",
             selfcheck(r"\text{No}"),
             r"For $x < 3$, $f'(x) = 2x - 4$, which approaches $2$ as $x \to 3^-$. For $x > 3$, $f'(x) = 5$. The slopes from the left "
             r"and right are $2$ and $5$, which are not equal, so $f$ is not differentiable at $x = 3$.",
             [(1, "slopes $2$ and $5$ from the two sides"), (1, "no, with the reason")], work="2.6cm"),
        Part("c", r"Find the values of $m$ and $c$ for which $f$ is differentiable at $x = 3$. Show the work that leads to your answer.",
             selfcheck(r"m = 2,\ c = -2"),
             r"Differentiable implies continuous, so $3m + c = f(3) = 4$. The slopes must match: $m = 2(3) - 4 = 2$. "
             r"Then $c = 4 - 3(2) = -2$.",
             [(1, "continuity condition $3m + c = 4$"), (1, "$m = 2$ from matching slopes"), (1, "$c = -2$")], work="3cm"),
    ], frq_type="Limits and continuity"),
]
same("frq a", [(x**2 - 4 * x + 7).subs(x, 3), 5 * 3 - 11], [4, 4])
same("frq b", [sp.diff(x**2 - 4 * x + 7, x).subs(x, 3), 5], [2, 5])
same("frq c", [2, 4 - 3 * 2], [sp.diff(x**2 - 4 * x + 7, x).subs(x, 3), -2])

TOPIC = Topic(
    number="2.4", title="Connecting Differentiability and Continuity",
    unit="Unit 2: Differentiation", ced=["FUN-2.A", "FUN-2.A.1", "FUN-2.A.2"],
    goals=r"Decide where a function is differentiable, and use the fact that differentiability implies continuity (but not the reverse).",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
