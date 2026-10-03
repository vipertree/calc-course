"""Topic 5.8: Sketching graphs of functions and their derivatives.

CED: FUN-4.A (FUN-4.A.9, FUN-4.A.10): read the graph of f' to describe f (and the reverse): zeros of f' are f's flat
spots, the sign of f' is f's direction, the slope of f' (sign of f'') is f's concavity. Worked examples: sketch f' for
x^3 - 3x; read f from the graph of f'(x) = 4 - x^2; sketch f from a list of conditions.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Table, Text, Topic, Variants, Video, num,
                     same, selfcheck)
from calclib.figs import graph

x = sp.symbols("x", real=True)

same("ex1", [sp.diff(x**3 - 3 * x, x)], [3 * x**2 - 3])
same("ex2", [sp.solve(4 - x**2, x), sp.diff(4 - x**2, x)], [[-2, 2], -2 * x])

FIG_FP = graph("t5_8_fp", [("(x+2)*(x-1)*(x-3)/2", -3, 4)], xr=(-3, 4), yr=(-6, 6), ystep=2, ylabel="f'(x)",
               caption="The graph of $f'$ (not $f$).")
FIG_FP2 = graph("t5_8_fp2", [("x^2-2*x-3", -2, 4)], xr=(-2, 4), yr=(-5, 5), ylabel="f'(x)", caption="The graph of $f'$.")
FIG_F = graph("t5_8_f", [("0.5*x^3-1.5*x", -2.5, 2.5)], xr=(-2.5, 2.5), yr=(-3, 3), ylabel="f(x)", caption="The graph of $f$.")

FIG_C = graph("t5_8_c", [("2-2*x", 0, 2), ("x-4", 2, 4), ("sqrt(abs(4-(x-6)^2))", 4, 8)], xr=(0, 8), yr=(-3, 3), ylabel="f'(x)",
              caption="The graph of $f'$ on $[0, 8]$: two segments and a semicircle.")

NOTES = [
    Video("s5_8.py::Lesson", "Graphs of f and its derivatives", 4),

    Section("Reading a graph of f'"),
    Text(r"The graph of $f'$ is a graph of slopes. Every feature of $f$ shows up in it, one level down:"),
    Table(r"$f'$ above the $x$-axis ($f' > 0$) & $f$ \blank{increasing} \\ "
          r"$f'$ below the $x$-axis ($f' < 0$) & $f$ decreasing \\ "
          r"$f'$ crosses the axis from $+$ to $-$ & relative \blank{maximum} of $f$ \\ "
          r"$f'$ crosses the axis from $-$ to $+$ & relative minimum of $f$ \\ "
          r"$f'$ increasing (rising) & $f$ concave \blank{up} \\ "
          r"$f'$ decreasing (falling) & $f$ concave down \\ "
          r"a peak or valley of $f'$ & \blank{point of inflection} of $f$", "ll", header=r"On the graph of $f'$ & What it means for $f$"),
    Text(r"\textbf{Cross, don't just touch.} $f' = 0$ gives a horizontal tangent, not always a turn. If the graph of $f'$ touches the axis and bounces "
         r"back, $f'$ doesn't change sign and $f$ has \blank{no} extremum there. A max or min needs $f'$ to change sign; an inflection point needs $f''$ "
         r"to change sign ($f'$ turns around). Topic 5.9 puts $f$, $f'$ and $f''$ together in one chart."),
    Text(r"\textbf{The common trap:} answering about the graph you see as if it were $f$. Read the axis label. A peak of $f'$ is not a maximum of $f$; it's an inflection point."),
    FIG_FP,
    VideoExample('Reading this graph', work="2.2cm"),

    Section("Sketching f' from f"),
    Text(r"To sketch $f'$, mark where $f$ has horizontal tangents (zeros of $f'$), then shade where $f$ rises ($f'$ above the axis) and falls ($f'$ below). "
         r"Steep parts of $f$ give large values of $|f'|$."),
    FIG_F,
    BigIdea(r"The graph of $f'$ is a graph of $f$'s slopes. Above the axis: $f$ rises. Crossing the axis: $f$ turns. Rising: $f$ bends up. Peaks and valleys: $f$ changes concavity."),
    Check(r"On the graph of $f'$, there is a valley (a relative minimum of $f'$) at $x = 2$. What does $f$ have at $x = 2$?", selfcheck(r"\text{a point of inflection}"),
          r"$f'$ changes from decreasing to increasing, so $f$ changes from concave down to concave up: a point of inflection."),
]

# ---------------------------------------------------------------- practice (several items read FIG_FP2: f'(x) = x^2 - 2x - 3 = (x - 3)(x + 1))
PRACTICE = [
    Item(r"The graph of $f'$ is shown. On what interval is $f$ decreasing?", selfcheck(r"(-1, 3)"), r"$f' < 0$ between $-1$ and $3$.", work="1.2cm", figure=FIG_FP2),
    Item(r"Using the same graph of $f'$, where does $f$ have a relative maximum?", num(-1), r"$f'$ changes from $+$ to $-$ at $x = -1$.", work="1.2cm"),
    Item(r"Using the same graph of $f'$, where does $f$ have a relative minimum?", num(3), r"$f'$ changes from $-$ to $+$ at $x = 3$.", work="1.2cm"),
    Item(r"Using the same graph of $f'$, on what interval is $f$ concave up?", selfcheck(r"(1, \infty)"), r"$f'$ is increasing for $x > 1$ (to the right of its vertex).", work="1.2cm"),
    Item(r"Using the same graph of $f'$, where does $f$ have a point of inflection?", num(1), r"$f'$ has its minimum at $x = 1$: it changes from decreasing to increasing.", work="1.2cm"),
    Item(r"The graph of $f$ is shown. At which $x$-values is $f'(x) = 0$? Enter the larger.", num(1),
         r"$f$ has horizontal tangents at its relative max ($x = -1$) and min ($x = 1$).", work="1.2cm", figure=FIG_F),
    Item(r"Using the same graph of $f$, is $f'(0)$ positive, negative or zero?", selfcheck(r"\text{negative}"), r"$f$ is decreasing at $x = 0$.", work="1.2cm"),
    Item(r"Using the same graph of $f$, is $f''(1.5)$ positive, negative or zero?", selfcheck(r"\text{positive}"), r"The graph of $f$ is concave up for $x > 0$.", work="1.2cm"),
    Item(r"$f'$ is a line through $(0, -2)$ with slope $1$. Describe $f$: where is it decreasing, where is its minimum, and what is its concavity?", num(2),
         r"$f'(x) = x - 2$: $f$ decreases for $x < 2$, increases after, so its minimum is at $x = 2$. $f'' = 1 > 0$: concave up everywhere (a parabola).", work="2cm"),
    Item(r"The graph of $f'$ is entirely above the $x$-axis and is decreasing. Describe the graph of $f$.", selfcheck(r"\text{increasing, concave down}"),
         r"$f' > 0$: $f$ increasing. $f'$ decreasing: $f$ concave down. Like $\sqrt x$ or $\ln x$.", work="1.4cm"),
    Item(r"A student says: ``The graph of $f'$ has a maximum at $x = 2$, so $f$ has a maximum at $x = 2$.'' Correct the statement.", selfcheck(r"\text{point of inflection}"),
         r"A maximum of $f'$ is where $f'$ stops increasing and starts decreasing: $f$ has a point of inflection there, not a maximum.", work="1.6cm"),
]
same("p", [sp.solve(x**2 - 2 * x - 3, x), sp.solve(sp.diff(x**2 - 2 * x - 3, x), x), sp.solve(sp.diff(x**3 / 2 - 3 * x / 2, x), x)], [[-1, 3], [1], [-1, 1]])

PRACTICE += [
    Item(r"The graph of $f'$ on $[0, 8]$ is shown. On what open intervals is $f$ increasing?", selfcheck(r"(0, 1) \text{ and } (4, 8)"),
         r"$f' > 0$ above the axis: on $(0, 1)$ and on $(4, 8)$ (the semicircle).", work="1.4cm", figure=FIG_C),
    Item(r"Using the same graph of $f'$, at what $x$ does $f$ have a relative maximum?", num(1),
         r"$f'$ crosses from $+$ to $-$ at $x = 1$. (At $x = 4$ it crosses from $-$ to $+$: a relative minimum.)", work="1.2cm"),
    Item(r"Using the same graph of $f'$, on what open intervals is the graph of $f$ concave down?", selfcheck(r"(0, 2) \text{ and } (6, 8)"),
         r"$f'$ is decreasing on $(0, 2)$ (the first segment) and on $(6, 8)$ (the right half of the semicircle).", work="1.4cm"),
    Item(r"Using the same graph of $f'$, find the $x$-coordinates of the inflection points of $f$. Enter the larger.", num(6),
         r"$f'$ switches from decreasing to increasing at $x = 2$ and from increasing to decreasing at $x = 6$.", work="1.4cm"),
    Item(r"$f'(x) = (x - 2)^2(x + 1)$. Does $f$ have a relative extremum at $x = 2$? Explain.", selfcheck(r"\text{no}"),
         r"No. $(x - 2)^2 \ge 0$, so $f'$ has the sign of $x + 1$, positive on both sides of $2$: no sign change.", work="1.6cm"),
    Item(r"Sketch the graph of $f(x) = x^3 - 3x^2$ by hand. Give its relative extrema and inflection point.",
         selfcheck(r"\text{max } (0, 0),\ \text{min } (2, -4),\ \text{inflection } (1, -2)"),
         r"$f'(x) = 3x(x - 2)$: signs $+, -, +$, so a relative max at $(0, 0)$ and a relative min at $(2, -4)$. $f''(x) = 6x - 6$ changes sign at $1$: "
         r"inflection point $(1, -2)$, concave down before, up after. Zeros at $x = 0$ and $x = 3$.", work="4cm"),
]
same("c", [sp.diff(x**3 - 3 * x**2, x).subs(x, 2), (x**3 - 3 * x**2).subs(x, 2), (x**3 - 3 * x**2).subs(x, 1)], [0, -4, -2])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"The graph of $f'$ crosses the $x$-axis from below to above at $x = 4$. Then $f$ has", [r"a relative minimum at $x = 4$", r"a relative maximum at $x = 4$",
            r"a point of inflection at $x = 4$", r"a zero at $x = 4$"], "A", r"$f'$ goes from $-$ to $+$."),
        MCQ(r"The graph of $f'$ crosses the $x$-axis from above to below at $x = -1$. Then $f$ has", [r"a relative minimum at $x = -1$", r"a relative maximum at $x = -1$",
            r"a point of inflection at $x = -1$", r"a zero at $x = -1$"], "B", r"$f'$ goes from $+$ to $-$."),
        MCQ(r"The graph of $f'$ touches the $x$-axis at $x = 2$ without crossing it. Then $f$ has", [r"a relative minimum at $x = 2$", r"a relative maximum at $x = 2$",
            r"no relative extremum at $x = 2$", r"a vertical tangent at $x = 2$"], "C", r"No sign change, no extremum."),
    ),
    Variants(
        MCQ(r"The graph of $f'$ has a relative maximum at $x = 3$. Then $f$ has", [r"a relative maximum at $x = 3$", r"a relative minimum at $x = 3$", r"a zero at $x = 3$",
            r"a point of inflection at $x = 3$"], "D", r"$f'$ changes from increasing to decreasing: concavity changes."),
        MCQ(r"The graph of $f'$ has a relative minimum at $x = 0$. Then $f$ has", [r"a point of inflection at $x = 0$", r"a relative minimum at $x = 0$", r"a relative maximum at $x = 0$",
            r"a zero at $x = 0$"], "A", r"$f'$ changes from decreasing to increasing: concavity changes."),
        MCQ(r"The graph of $f'$ is increasing on $(1, 5)$. On $(1, 5)$, the graph of $f$ is", [r"increasing", r"concave up", r"concave down", r"decreasing"], "B", r"$f'$ increasing means $f'' > 0$."),
    ),
    Variants(
        Item(r"$f'(x) = (x - 1)(x - 5)$. Where does the graph of $f$ have a point of inflection?", num(3), r"$f'$ is a parabola with its vertex at $x = 3$.", work="1.4cm"),
        Item(r"$f'(x) = (x + 2)(x - 4)$. Where does the graph of $f$ have a point of inflection?", num(1), r"$f'$ is a parabola with its vertex at $x = 1$.", work="1.4cm"),
        Item(r"$f'(x) = x(x - 6)$. Where does the graph of $f$ have a point of inflection?", num(3), r"$f'$ is a parabola with its vertex at $x = 3$.", work="1.4cm"),
    ),
    Variants(
        Item(r"The graph of $f$ has horizontal tangents at $x = -3$ and $x = 2$ only. How many zeros does the graph of $f'$ have?", num(2), r"Each horizontal tangent of $f$ is a zero of $f'$.", work="1.2cm"),
        Item(r"The graph of $f$ has horizontal tangents at $x = 0$, $x = 1$ and $x = 4$ only. How many zeros does the graph of $f'$ have?", num(3), r"Each horizontal tangent of $f$ is a zero of $f'$.", work="1.2cm"),
        Item(r"The graph of $f$ is a line with slope $-2$. What is the graph of $f'$?", selfcheck(r"y = -2"), r"A horizontal line at height $-2$.", work="1.2cm"),
    ),
    Variants(
        Item(r"$f$ is increasing and concave up on $(0, 3)$. On $(0, 3)$, is $f'$ positive or negative, and increasing or decreasing?", selfcheck(r"\text{positive, increasing}"),
             r"Increasing $f$: $f' > 0$. Concave up: $f'$ increasing.", work="1.2cm"),
        Item(r"$f$ is decreasing and concave up on $(2, 6)$. On $(2, 6)$, is $f'$ positive or negative, and increasing or decreasing?", selfcheck(r"\text{negative, increasing}"),
             r"Decreasing $f$: $f' < 0$. Concave up: $f'$ increasing.", work="1.2cm"),
        Item(r"$f$ is increasing and concave down on $(-1, 1)$. On $(-1, 1)$, is $f'$ positive or negative, and increasing or decreasing?", selfcheck(r"\text{positive, decreasing}"),
             r"Increasing $f$: $f' > 0$. Concave down: $f'$ decreasing.", work="1.2cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"The graph of $f'$ is shown. How many relative extrema does $f$ have on $(-3, 4)$?", [r"$1$", r"$2$", r"$3$", r"$4$"], "C",
        r"$f'$ changes sign at $-2$, $1$ and $3$.", figure=FIG_FP),
    MCQ(r"The graph of $f'$ is shown. On which interval is $f$ both decreasing and concave up?", [r"$(-2, 1)$", r"$(1, 2)$", r"$(3, 4)$", r"$(-3, -2)$"], "D",
        r"Decreasing needs $f' < 0$: $(-3, -2)$ or $(1, 3)$. Concave up needs $f'$ rising: true on $(-3, -2)$, but on $(1, 2)$ $f'$ is still falling toward its valley.", figure=FIG_FP),
    MCQ(r"Which is true of every point of inflection of a twice-differentiable $f$?", [r"$f'$ has a relative extremum there", r"$f$ has a relative extremum there",
        r"$f' = 0$ there", r"$f$ crosses the $x$-axis there"], "A", r"Concavity changes where $f'$ changes from increasing to decreasing (or back)."),
    MCQ(r"The graph of $f$ is concave down everywhere and has a maximum at $x = 2$. Which could be $f'$?", [r"$f'(x) = x - 2$", r"$f'(x) = (x - 2)^2$", r"$f'(x) = 2 - x$", r"$f'(x) = 2x$"], "C",
        r"$f'(2) = 0$, and $f'$ must be decreasing: $2 - x$."),
]
fp = (x + 2) * (x - 1) * (x - 3) / 2
same("m", [sp.solve(fp, x), sp.solve(sp.diff(fp, x), x)], [[-2, 1, 3], [sp.Rational(2, 3) - sp.sqrt(19) / 3, sp.Rational(2, 3) + sp.sqrt(19) / 3]])

FIG_FPQ = graph("t5_8_fpq", [("2*x+5", -4, -2), ("-x-1", -2, 1), ("x-3", 1, 4)], xr=(-4, 4), yr=(-3.5, 2), ylabel="f'(x)",
                caption="The graph of $f'$.")
FRQS = [
    FRQ("Reading the graph of a derivative", (
        r"The function $f$ is defined on the closed interval $-4 \le x \le 4$. The graph of $f'$, the derivative of $f$, consists "
        r"of three line segments, as shown in the figure."), [
        Part("a", r"Find all values of $x$ in the open interval $-4 < x < 4$ at which $f$ has a relative minimum. Justify your answer.",
             selfcheck(r"x = -\tfrac52 \text{ and } x = 3"),
             r"$f'$ changes from negative to positive at $x = -\frac52$ and at $x = 3$, so $f$ has a relative minimum at each.",
             [(1, "$x = -\\frac52$ and $x = 3$"), (1, "justification")], work="2.4cm"),
        Part("b", r"On what open intervals, if any, is the graph of $f$ concave down? Give a reason for your answer.",
             selfcheck(r"(-2, 1)"),
             r"The graph of $f$ is concave down on $(-2, 1)$ because $f'$ is decreasing there.",
             [(1, "interval $(-2, 1)$"), (1, "reason: $f'$ is decreasing")], work="2cm"),
        Part("c", r"Find the $x$-coordinate of each point of inflection of the graph of $f$. Give a reason for your answer.",
             selfcheck(r"x = -2 \text{ and } x = 1"),
             r"The graph of $f$ has points of inflection at $x = -2$ and $x = 1$, because $f'$ changes from increasing to decreasing "
             r"at $x = -2$ and from decreasing to increasing at $x = 1$.",
             [(1, "$x = -2$ and $x = 1$"), (1, "reason")], work="2cm"),
        Part("d", r"For each of $f''(0)$ and $f''(-2)$, find the value or explain why it does not exist.",
             selfcheck(r"f''(0) = -1;\ f''(-2)\ \text{does not exist}"),
             r"On $-2 < x < 1$, $f'$ is a line with slope $-1$, so $f''(0) = -1$. At $x = -2$ the slope of the graph of $f'$ is $2$ from "
             r"the left and $-1$ from the right, so $f'$ is not differentiable there and $f''(-2)$ does not exist.",
             [(1, "$f''(0) = -1$"), (1, "$f''(-2)$ does not exist, with explanation")], work="2.6cm"),
    ], frq_type="Graph of f'", figure=FIG_FPQ),
]
segs8 = [(2 * x + 5, -4, -2), (-x - 1, -2, 1), (x - 3, 1, 4)]
same("frq continuity", [segs8[0][0].subs(x, -2) - segs8[1][0].subs(x, -2), segs8[1][0].subs(x, 1) - segs8[2][0].subs(x, 1)], [0, 0])
zeros8 = [r for e, a, b in segs8 for r in sp.solve(e, x) if a <= r <= b]
same("frq zeros", zeros8, [sp.Rational(-5, 2), -1, 3])
same("frq d", [sp.diff(segs8[1][0], x), sp.diff(segs8[0][0], x)], [-1, 2])

TOPIC = Topic(
    number="5.8", title="Sketching Graphs of Functions and Their Derivatives",
    unit="Unit 5: Analytical Applications of Differentiation", ced=["FUN-4.A", "FUN-4.A.9", "FUN-4.A.10"],
    goals=r"Read the behavior of $f$ from a graph of $f'$, and sketch $f'$ from a graph of $f$.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
