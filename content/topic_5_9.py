"""Topic 5.9: Connecting a function, its first derivative, and its second derivative.

CED: FUN-4.A (FUN-4.A.11): key features of the graphs of f, f' and f'' are related. Three levels: f'' tells how f'
changes, f' tells how f changes. Worked examples: f'(x) = (x - 1)^2(x - 4) (all features), a sign table, and
f'(2) = 0 with f''(x) = (x - 2)e^x (inconclusive second derivative test resolved by thinking about f').
"""
import sympy as sp

from calclib import (FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Table, Text, Topic, Variants, Video, close, num,
                     same, selfcheck, check)

x = sp.symbols("x", real=True)

fp1 = (x - 1)**2 * (x - 4)
same("ex1", [sp.factor(sp.diff(fp1, x)), sp.solve(sp.diff(fp1, x), x)], [3 * (x - 1) * (x - 3), [1, 3]])

NOTES = [
    Video("s5_9.py::Lesson", "Three graphs, one function", 4),

    Section("Three levels"),
    Text(r"$f''$ tells you how $f'$ changes, and $f'$ tells you how $f$ changes. Every question about $f$ is answered one or two levels down."),
    Table(r"$f$ increasing & $f' > 0$ & \\ "
          r"$f$ decreasing & $f' < 0$ & \\ "
          r"$f$ concave up & $f'$ \blank{increasing} & $f'' > 0$ \\ "
          r"$f$ concave down & $f'$ decreasing & $f'' \mblank{< 0}$ \\ "
          r"relative extremum of $f$ & $f'$ changes sign & \\ "
          r"inflection point of $f$ & $f'$ has a relative extremum & $f''$ changes sign", "lll", header=r"$f$ & $f'$ & $f''$"),
    Text(r"\textbf{Justify at the right level.} ``$f$ is concave up because $f''$ is positive'' or ``because $f'$ is increasing'' both work. "
         r"``Because $f$ curves up'' restates the claim; it isn't a reason."),

    Section("Putting it together"),
    BigIdea(r"Answer each question about $f$ at the level that decides it: direction and extrema from $f'$, concavity and inflection from $f''$ (or from $f'$ rising and falling)."),
    Check(r"$f'$ is negative and increasing on $(0, 4)$. Describe $f$ on $(0, 4)$.", selfcheck(r"\text{decreasing, concave up}"), r"$f' < 0$: decreasing. $f'$ increasing: concave up."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"$f'(x) = x^2(x - 3)$. Find the $x$-coordinates of the points of inflection of $f$. Enter the larger.", num(2),
         r"$f''(x) = 3x^2 - 6x = 3x(x - 2)$ changes sign at $0$ and $2$.", work="2cm"),
    Item(r"$f'(x) = x^2(x - 3)$. Does $f$ have a relative extremum at $x = 0$? Explain.", selfcheck(r"\text{no}"),
         r"$f'$ is negative on both sides of $0$ (since $x^2 > 0$ and $x - 3 < 0$): no sign change, no extremum.", work="1.6cm"),
    Item(r"$f''(x) = (x + 1)(x - 2)$ and $f'(-1) = 0$. Is $f(-1)$ a relative maximum, a relative minimum, or neither?", selfcheck(r"\text{neither}"),
         r"$f''(-1) = 0$: the Second Derivative Test is silent. $f''$ changes from $+$ to $-$ at $-1$, so $f'$ has a relative max of $0$ there: $f' \le 0$ nearby, "
         r"so $f$ keeps decreasing. Neither (it's an inflection point).", work="2.6cm"),
    Item(r"On $(1, 3)$, $f$ is increasing and its graph is concave down. Is $f'$ increasing or decreasing on $(1, 3)$? Is $f''$ positive or negative?", selfcheck(r"\text{decreasing; negative}"),
         r"Concave down: $f'$ decreasing, $f'' < 0$.", work="1.4cm"),
    Item(r"$g'(x) = e^{x}(x^2 - 4)$. Where is $g$ decreasing? Enter the right endpoint.", num(2), r"$e^x > 0$; $x^2 - 4 < 0$ on $(-2, 2)$.", work="1.6cm"),
    Item(r"$g'(x) = e^{x}(x^2 - 4)$. Find the $x$-coordinates of the inflection points of $g$. Enter the larger.", num(-1 + sp.sqrt(5)),
         r"$g''(x) = e^x(x^2 + 2x - 4) = 0$ at $x = -1 \pm \sqrt5$, with sign changes.", work="2.2cm"),
    Item(r"$f(2) = 5$, $f'(2) = 0$, $f''(2) = -3$. Describe the graph of $f$ near $x = 2$.", selfcheck(r"\text{relative maximum at } (2, 5)\text{, concave down}"),
         r"Horizontal tangent, concave down: a relative maximum at $(2, 5)$, with the graph bending down.", work="1.4cm"),
    Item(r"The graph of $f''$ is positive on $(-\infty, 1)$ and negative on $(1, \infty)$. Where does $f'$ have its relative maximum?", num(1),
         r"$f'' = (f')'$ changes from $+$ to $-$ at $x = 1$, so $f'$ has a relative maximum there.", work="1.4cm"),
    Item(r"$f'(x) = \sin x$ on $(0, 2\pi)$. Where is $f$ concave down? Enter the left endpoint.", num(sp.pi / 2), r"$f''(x) = \cos x < 0$ on $\left(\frac\pi2, \frac{3\pi}{2}\right)$.", work="1.6cm"),
    Item(r"$h$ is twice differentiable, $h' > 0$ and $h'' > 0$ everywhere, and $h(0) = 2$. Which is larger: $h(1) - h(0)$ or $h(2) - h(1)$?", selfcheck(r"h(2) - h(1)"),
         r"$h$ is increasing more and more steeply ($h'$ increasing), so it gains more on $[1, 2]$ than on $[0, 1]$.", work="1.6cm"),
]
same("p", [sp.solve(sp.diff(x**2 * (x - 3), x), x), sorted(sp.solve(sp.diff(sp.exp(x) * (x**2 - 4), x), x), key=float)], [[0, 2], [-1 - sp.sqrt(5), -1 + sp.sqrt(5)]])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"$f'(x) = (x - 2)^2(x + 1)$. How many relative extrema does $f$ have?", num(1), r"$f'$ changes sign only at $-1$.", work="1.4cm"),
        Item(r"$f'(x) = x(x - 4)^2$. How many relative extrema does $f$ have?", num(1), r"$f'$ changes sign only at $0$.", work="1.4cm"),
        Item(r"$f'(x) = (x + 3)^2(x - 1)^2$. How many relative extrema does $f$ have?", num(0), r"$f' \ge 0$ everywhere: no sign changes.", work="1.4cm"),
    ),
    Variants(
        Item(r"$f'(x) = (x - 2)^2(x + 1)$. Find the $x$-coordinates of the inflection points of $f$. Enter the smaller.", num(0), r"$f''(x) = 3x(x - 2)$ changes sign at $0$ and $2$.", work="2cm"),
        Item(r"$f'(x) = x(x - 4)^2$. Find the $x$-coordinates of the inflection points of $f$. Enter the smaller.", num(sp.Rational(4, 3)), r"$f''(x) = (x - 4)(3x - 4)$ changes sign at $\frac43$ and $4$.", work="2cm"),
        Item(r"$f'(x) = x^3 - 3x$. Find the $x$-coordinates of the inflection points of $f$. Enter the smaller.", num(-1), r"$f''(x) = 3x^2 - 3$ changes sign at $\pm 1$.", work="2cm"),
    ),
    Variants(
        MCQ(r"On an interval, $f' < 0$ and $f'' > 0$. The graph of $f$ is", [r"increasing and concave up", r"decreasing and concave down", r"decreasing and concave up", r"increasing and concave down"], "C", r"Read each sign."),
        MCQ(r"On an interval, $f' > 0$ and $f'' < 0$. The graph of $f$ is", [r"increasing and concave down", r"increasing and concave up", r"decreasing and concave up", r"decreasing and concave down"], "A", r"Read each sign."),
        MCQ(r"On an interval, $f' < 0$ and $f'' < 0$. The graph of $f$ is", [r"increasing and concave up", r"decreasing and concave up", r"increasing and concave down", r"decreasing and concave down"], "D", r"Read each sign."),
    ),
    Variants(
        MCQ(r"$f$ has an inflection point at $x = 3$. Which must be true?", [r"$f'(3) = 0$", r"$f'$ has a relative extremum at $x = 3$", r"$f$ has a relative extremum at $x = 3$", r"$f(3) = 0$"], "B",
            r"Concavity changes where $f'$ switches between increasing and decreasing."),
        MCQ(r"$f'$ has a relative minimum at $x = 1$. Which must be true about $f$?", [r"$f$ has a relative minimum at $1$", r"$f(1) = 0$", r"$f$ has an inflection point at $1$", r"$f'(1) = 0$"], "C",
            r"$f'$ switches from decreasing to increasing: concavity changes."),
        MCQ(r"$f''$ changes from negative to positive at $x = -2$. Then", [r"$f$ has a relative minimum at $-2$", r"$f$ has an inflection point at $-2$", r"$f'(-2) = 0$", r"$f$ is increasing at $-2$"], "B",
            r"Concavity changes."),
    ),
    Variants(
        Item(r"$f'(5) = 0$ and $f''(x) < 0$ for all $x$. What is $f(5)$ for $f$ on $(-\infty, \infty)$?", selfcheck(r"\text{the absolute maximum}"),
             r"$f'$ is decreasing everywhere and crosses $0$ at $5$, so $f' > 0$ before and $f' < 0$ after: $f(5)$ is the absolute maximum.", work="1.8cm"),
        Item(r"$f'(-1) = 0$ and $f''(x) > 0$ for all $x$. What is $f(-1)$ for $f$ on $(-\infty, \infty)$?", selfcheck(r"\text{the absolute minimum}"),
             r"$f'$ is increasing everywhere and crosses $0$ at $-1$: $f$ falls, then rises. $f(-1)$ is the absolute minimum.", work="1.8cm"),
        Item(r"$f'(0) = 0$ and $f''(x) > 0$ for all $x$. What is $f(0)$ for $f$ on $(-\infty, \infty)$?", selfcheck(r"\text{the absolute minimum}"),
             r"$f'$ is increasing and crosses $0$ at $0$: $f(0)$ is the absolute minimum.", work="1.8cm"),
    ),
]
same("q", [sp.solve(sp.diff(x * (x - 4)**2, x), x), sp.solve(sp.diff((x - 2)**2 * (x + 1), x), x)], [[sp.Rational(4, 3), 4], [0, 2]])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$f'(x) = x^3(x - 2)^2$. Which is true?", [r"$f$ has a relative maximum at $x = 2$", r"$f$ has a relative minimum at $x = 0$ only",
        r"$f$ has relative minima at $x = 0$ and $x = 2$", r"$f$ has no relative extrema"], "B", r"$f'$ changes from $-$ to $+$ at $0$; no sign change at $2$."),
    MCQ(r"$f$ is twice differentiable, $f'(1) = 0$, and $f''(x) < 0$ for all $x \ne 1$. At $x = 1$, $f$ has", [r"a relative minimum", r"a relative maximum",
        r"an inflection point", r"no conclusion possible"], "B",
        r"$f'$ is decreasing on both sides of $1$ and equals $0$ there, so $f' > 0$ before and $f' < 0$ after: a relative maximum."),
    MCQ(r"$g''(x) = (x - 1)(x - 3)$. On which interval is $g'$ decreasing?", [r"$(-\infty, 1)$", r"$(3, \infty)$", r"$(1, 3)$", r"$(-\infty, 3)$"], "C", r"$g'' < 0$ on $(1, 3)$."),
    MCQ(r"$f'(x) = \cos(x^2) - 0.5$ on $(0, 2)$. At about what $x$ does $f$ have a relative maximum?", [r"$1.023$", r"$1.253$", r"$0.724$", r"$1.772$"], "A",
        r"$f' = 0$ where $x^2 = \frac\pi3$: $x \approx 1.023$; $f'$ changes from $+$ to $-$ there.", calc=True),
]
close("m", sp.sqrt(sp.pi / 3), 1.023, 5e-4)

FRQS = [
    FRQ("Three levels of one function", (
        r"Let $f$ be a twice-differentiable function with $f(0) = 0$ and $f'(x) = (x - 1)^2(x - 4)$ for all real numbers $x$."), [
        Part("a", r"Find the $x$-coordinate of each relative extremum of $f$, and classify each as a relative minimum or a relative "
                  r"maximum. Justify your answer.", selfcheck(r"\text{relative minimum at } x = 4 \text{ only}"),
             r"$f'(x) = 0$ at $x = 1$ and $x = 4$. $f'(x) < 0$ on both sides of $x = 1$, so there is no extremum there. $f'$ changes from "
             r"negative to positive at $x = 4$, so $f$ has a relative minimum at $x = 4$ and no other relative extremum.",
             [(1, "relative minimum at $x = 4$ with justification"), (1, "explains that $x = 1$ is not an extremum")], work="2.8cm"),
        Part("b", r"Find $f''(x)$. Find the $x$-coordinates of all points of inflection of the graph of $f$. Justify your answer.",
             selfcheck(r"f''(x) = 3(x - 1)(x - 3);\ x = 1 \text{ and } x = 3"),
             r"$f''(x) = 2(x - 1)(x - 4) + (x - 1)^2 = 3(x - 1)(x - 3)$. $f''$ changes sign at $x = 1$ and at $x = 3$, so the graph of "
             r"$f$ has points of inflection there.",
             [(1, "$f''(x)$"), (1, "$x = 1$ and $x = 3$ with justification")], work="2.8cm"),
        Part("c", r"On what open intervals, if any, is the graph of $f$ both decreasing and concave up? Give a reason for your answer.",
             selfcheck(r"(-\infty, 1) \text{ and } (3, 4)"),
             r"$f$ is decreasing where $f'(x) < 0$: for $x < 4$, $x \ne 1$. The graph is concave up where $f''(x) > 0$: for $x < 1$ or "
             r"$x > 3$. Both hold on $(-\infty, 1)$ and $(3, 4)$.",
             [(1, "intervals with reason")], work="2.4cm"),
    ], frq_type="Function analysis"),
]
fp9 = (x - 1)**2 * (x - 4)
same("frq b", sp.factor(sp.diff(fp9, x)), 3 * (x - 1) * (x - 3))
check("frq a", fp9.subs(x, 0) < 0 and fp9.subs(x, 2) < 0 and fp9.subs(x, 5) > 0)
check("frq c", all(fp9.subs(x, v) < 0 and sp.diff(fp9, x).subs(x, v) > 0 for v in (-3, 0, sp.Rational(7, 2)))
      and sp.diff(fp9, x).subs(x, 2) < 0)

TOPIC = Topic(
    number="5.9", title="Connecting a Function, Its First Derivative, and Its Second Derivative",
    unit="Unit 5: Analytical Applications of Differentiation", ced=["FUN-4.A", "FUN-4.A.11"],
    goals=r"Relate the features of $f$, $f'$ and $f''$, and justify each claim about $f$ at the level that decides it.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
