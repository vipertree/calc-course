"""Topic 6.5: Interpreting the behavior of accumulation functions involving area.

CED: FUN-5.A (FUN-5.A.1, FUN-5.A.2) with FUN-4.A applied to g(x) = integral_a^x f(t) dt: g' = f and g'' = f', so the sign
of f gives where g increases, sign changes of f give g's relative extrema, f rising/falling gives g's concavity, and
values of g are signed areas. Lesson example: a semicircle-and-segments graph of f (values, extrema, candidates test,
inflection points). Worked examples: g' from a formula with a sign chart, a tangent line to g, concavity from a graph.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Table, Text, Topic, Variants, Video, num, same,
                     selfcheck)
from calclib.figs import graph

x, t = sp.symbols("x t", real=True)

FL = sp.Piecewise((sp.sqrt(4 - (t + 2)**2), t < 0), (-t, t < 2), (t - 4, True))
exact = lambda e: sp.nsimplify(sp.N(e, 30), [sp.pi])          # sympy leaves exp_polar in semicircle integrals; snap the value back to a + b*pi
gl = lambda v: exact(sp.integrate(FL, (t, 0, v)) if v >= 0 else -sp.integrate(FL, (t, v, 0)))
same("lesson", [gl(2), gl(4), gl(6), gl(-4)], [-2, -4, -2, -2 * sp.pi])

FQ = sp.Piecewise((2 * t + 2, t < 0), (2 - t, t < 2), (-sp.sqrt(4 - (t - 4)**2), True))
gq = lambda v: exact(sp.integrate(FQ, (t, 0, v)) if v >= 0 else -sp.integrate(FQ, (t, v, 0)))
same("frq", [gq(-2), gq(-1), gq(2), gq(6)], [0, -1, 2, 2 - 2 * sp.pi])
FIG_Q = graph("t6_5_q", [("2*x+2", -2, 0), ("2-x", 0, 2), ("-sqrt(abs(4-(x-4)^2))", 2, 6)], xr=(-2, 6), yr=(-3, 3), xlabel="t", ylabel="f(t)",
              caption="The graph of $f$: two line segments and a semicircle.")

FP = sp.Piecewise((t - 1, t < 3), (2, t < 5), (2 - 2 * (t - 5), True))
FIG_P = graph("t6_5_p", [("x-1", 0, 3), ("2+0*x", 3, 5), ("2-2*(x-5)", 5, 7)], xr=(0, 7), yr=(-3, 3), xlabel="t", ylabel="f(t)",
              caption="The graph of $f$: three line segments.")
gp = lambda v: sp.integrate(FP, (t, 0, v))
same("p", [gp(1), gp(3), gp(5), gp(6), gp(7)], [-sp.Rational(1, 2), sp.Rational(3, 2), sp.Rational(11, 2), sp.Rational(13, 2), sp.Rational(11, 2)])

NOTES = [
    Video("s6_5.py::Lesson", "Reading an accumulation function", 6),

    Section("$g' = f$"),
    Text(r"For $g(x) = \int_a^x f(t)\,dt$, the Fundamental Theorem gives $g' = f$ and $g'' = f'$. So reading $g$ from the graph of $f$ is reading a function from the graph of its derivative (Topic 5.9's chart, one level up)."),
    Table(r"$f$ positive & $g$ \blank{increasing} \\ "
          r"$f$ negative & $g$ decreasing \\ "
          r"$f$ changes sign, $+$ to $-$ & $g$ has a relative \blank{maximum} \\ "
          r"$f$ changes sign, $-$ to $+$ & $g$ has a relative minimum \\ "
          r"$f$ increasing & $g$ concave \blank{up} \\ "
          r"$f$ decreasing & $g$ concave down \\ "
          r"$f$ has a relative max or min & $g$ has an \blank{inflection point}", "ll", header=r"Graph of $f$ & $g(x) = \int_a^x f(t)\,dt$"),
    Text(r"\textbf{Values of $g$} are signed areas from $a$ to $x$. If $x < a$, the limits run backward: $g(x) = -\int_x^a f(t)\,dt$. "
         r"\textbf{Absolute extrema} of $g$ on a closed interval: the candidates test (critical points, where $f$ changes sign, and the endpoints)."),
    VideoExample('Reading the graph of f', work="4cm"),
    BigIdea(r"For an accumulation function, $f$ is the derivative: direction and extrema from the sign of $f$, concavity from whether $f$ rises or falls, values from signed areas."),
    Check(r"$g(x) = \int_0^x f(t)\,dt$ and $f$ changes from negative to positive at $x = 3$. What does $g$ have at $x = 3$?", selfcheck(r"\text{a relative minimum}"),
          r"$g' = f$ changes from $-$ to $+$: a relative minimum."),
]

# ---------------------------------------------------------------- practice (FIG_P: f(t) = t - 1 on [0, 3], 2 on [3, 5], 2 - 2(t - 5) on [5, 7])
PRACTICE = [
    Item(r"The graph of $f$ is shown, and $g(x) = \int_0^x f(t)\,dt$. Find $g(3)$.", num(gp(3)),
         r"$-\frac12$ from the triangle below the axis on $[0, 1]$, plus $\frac12(2)(2) = 2$ on $[1, 3]$: $g(3) = \frac32$.", work="1.6cm", figure=FIG_P),
    Item(r"Using the same graph, find $g(7)$.", num(gp(7)),
         r"$g(5) = \frac32 + (2)(2) = \frac{11}{2}$. On $[5, 6]$ the triangle above the axis adds $1$; on $[6, 7]$ the triangle below subtracts $1$. $g(7) = \frac{11}{2}$.", work="1.8cm"),
    Item(r"Using the same graph, on what interval is $g$ decreasing?", selfcheck(r"(0, 1) \text{ and } (6, 7)"), r"$g' = f < 0$ on $(0, 1)$ and on $(6, 7)$.", work="1.2cm"),
    Item(r"Using the same graph, at what $x$ does $g$ have a relative maximum?", num(6), r"$f$ changes from positive to negative at $x = 6$.", work="1.2cm"),
    Item(r"Using the same graph, find the absolute minimum value of $g$ on $[0, 7]$.", num(gp(1)),
         r"Candidates: $g(0) = 0$, $g(1) = -\frac12$, $g(6) = \frac{13}{2}$, $g(7) = \frac{11}{2}$. The minimum is $-\frac12$, at $x = 1$.", work="2cm"),
    Item(r"Using the same graph, on what interval is the graph of $g$ concave down?", selfcheck(r"(5, 7)"), r"$f$ is decreasing on $(5, 7)$.", work="1.2cm"),
    Item(r"Using the same graph, find $g''(2)$ and $g''(4)$. Enter $g''(2)$.", num(1), r"$g'' = f'$: the slope of $f$ is $1$ at $t = 2$ and $0$ at $t = 4$.", work="1.2cm"),
    Item(r"$g(x) = \int_0^x \left(t^2 - 2t - 3\right) dt$. At what $x$ does $g$ have a relative minimum?", num(3),
         r"$g'(x) = (x - 3)(x + 1)$ changes from negative to positive at $x = 3$.", work="1.8cm"),
    Item(r"$g(x) = \int_2^x \frac{1}{t}\,dt$ for $x > 0$. Write an equation for the line tangent to $g$ at $x = 2$.", selfcheck(r"y = \tfrac12(x - 2)"),
         r"$g(2) = 0$ and $g'(2) = \frac12$: $y = \frac12(x - 2)$.", work="1.6cm"),
    Item(r"$g(x) = \int_0^x e^{-t^2}\,dt$. On what interval is $g$ concave up?", selfcheck(r"(-\infty, 0)"), r"$g''(x) = -2xe^{-x^2} > 0$ for $x < 0$.", work="1.6cm"),
]
same("p2", [sp.solve(t**2 - 2 * t - 3, t)], [[-1, 3]])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"$g(x) = \int_0^x f(t)\,dt$, and $f$ is positive on $(0, 3)$ and negative on $(3, 8)$. Where does $g$ have a relative maximum?", [r"$x = 0$", r"$x = 3$", r"$x = 8$", r"nowhere"], "B",
            r"$g' = f$ changes from $+$ to $-$ at $3$."),
        MCQ(r"$g(x) = \int_0^x f(t)\,dt$, and $f$ is negative on $(0, 5)$ and positive on $(5, 9)$. Where does $g$ have a relative minimum?", [r"$x = 0$", r"$x = 9$", r"$x = 5$", r"nowhere"], "C",
            r"$g' = f$ changes from $-$ to $+$ at $5$."),
        MCQ(r"$g(x) = \int_1^x f(t)\,dt$, and $f$ is positive on $(1, 4)$, zero at $4$, and positive on $(4, 7)$. Where does $g$ have a relative extremum?", [r"$x = 4$", r"$x = 1$", r"$x = 7$", r"nowhere in $(1, 7)$"], "D",
            r"$f$ doesn't change sign at $4$: no extremum."),
    ),
    Variants(
        MCQ(r"$g(x) = \int_0^x f(t)\,dt$. The graph of $f$ is increasing on $(2, 6)$. On $(2, 6)$ the graph of $g$ is", [r"increasing", r"concave up", r"concave down", r"decreasing"], "B", r"$g'' = f' > 0$."),
        MCQ(r"$g(x) = \int_0^x f(t)\,dt$. The graph of $f$ is decreasing on $(1, 4)$. On $(1, 4)$ the graph of $g$ is", [r"concave down", r"concave up", r"decreasing", r"increasing"], "A", r"$g'' = f' < 0$."),
        MCQ(r"$g(x) = \int_0^x f(t)\,dt$. The graph of $f$ has a relative maximum at $t = 3$. At $x = 3$, the graph of $g$ has", [r"a relative maximum", r"a relative minimum",
            r"a point of inflection", r"a horizontal tangent"], "C", r"$g'' = f'$ changes from $+$ to $-$."),
    ),
    Variants(*[Item(rf"$g(x) = \int_{{{a}}}^x {sp.latex(f)}\,dt$. Find $g'({c})$.", num(f.subs(t, c)), rf"$g'(x) = {sp.latex(f.subs(t, x))}$, so $g'({c}) = {f.subs(t, c)}$.", work="1cm")
               for a, f, c in ((1, t**2 + 2 * t, 2), (0, 5 - t**2, 1), (3, t**3 - t, 2))]),
    Variants(
        Item(r"$g(x) = \int_0^x f(t)\,dt$, and the area between $f$ and the $t$-axis is $6$ above the axis on $[0, 4]$ and $2$ below the axis on $[4, 7]$. Find $g(7)$.", num(4), r"$6 - 2 = 4$.", work="1cm"),
        Item(r"$g(x) = \int_0^x f(t)\,dt$, and the area between $f$ and the $t$-axis is $3$ below the axis on $[0, 2]$ and $5$ above the axis on $[2, 6]$. Find $g(6)$.", num(2), r"$-3 + 5 = 2$.", work="1cm"),
        Item(r"$g(x) = \int_2^x f(t)\,dt$, and the area between $f$ and the $t$-axis on $[0, 2]$ is $4$, above the axis. Find $g(0)$.", num(-4), r"Backward limits: $g(0) = -\int_0^2 f(t)\,dt = -4$.", work="1cm"),
    ),
    Variants(
        Item(r"$g(x) = \int_1^x \left(3t^2 + 1\right) dt$. Write the line tangent to $g$ at $x = 1$.", selfcheck(r"y = 4(x - 1)"), r"$g(1) = 0$, $g'(1) = 4$.", work="1.2cm"),
        Item(r"$g(x) = \int_0^x \cos t\,dt$. Write the line tangent to $g$ at $x = 0$.", selfcheck(r"y = x"), r"$g(0) = 0$, $g'(0) = 1$.", work="1.2cm"),
        Item(r"$g(x) = \int_4^x \sqrt t\,dt$. Write the line tangent to $g$ at $x = 4$.", selfcheck(r"y = 2(x - 4)"), r"$g(4) = 0$, $g'(4) = 2$.", work="1.2cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$g(x) = \int_0^x f(t)\,dt$ with $f$ as in the graph of the practice problems ($f(t) = t - 1$ on $[0, 3]$, $2$ on $[3, 5]$, $2 - 2(t - 5)$ on $[5, 7]$). $g(5) = $",
        [r"$\frac32$", r"$4$", r"$\frac{11}{2}$", r"$\frac{13}{2}$"], "C", r"$\frac32 + (2)(2) = \frac{11}{2}$.", why_not={"D": "$g(6)$"}),
    MCQ(r"$g(x) = \int_0^x \left(t^3 - 3t^2\right) dt$. The graph of $g$ is concave down on", [r"$(0, 2)$", r"$(-\infty, 0)$", r"$(0, 3)$", r"$(2, \infty)$"], "A",
        r"$g''(x) = 3x^2 - 6x = 3x(x - 2) < 0$ on $(0, 2)$.", why_not={"C": "where $g' < 0$ (decreasing)"}),
    MCQ(r"$g(x) = \int_0^x f(t)\,dt$, where $f(t) = \sin t$ on $[0, 2\pi]$. The absolute maximum value of $g$ on $[0, 2\pi]$ is", [r"$1$", r"$0$", r"$\pi$", r"$2$"], "D",
        r"$g$ peaks at $x = \pi$: $g(\pi) = \int_0^\pi \sin t\,dt = 2$."),
    MCQ(r"$g(x) = \int_3^x f(t)\,dt$, and $\int_1^3 f(t)\,dt = 5$. Then $g(1) = $", [r"$-5$", r"$5$", r"$0$", r"$8$"], "A", r"$g(1) = \int_3^1 f(t)\,dt = -5$."),
]
same("m", [gp(5), sp.integrate(sp.sin(t), (t, 0, sp.pi))], [sp.Rational(11, 2), 2])

FRQS = [
    FRQ("Reading an accumulation function", (
        r"The continuous function $f$ is defined on $-2 \le t \le 6$. Its graph consists of two line segments and a semicircle, as shown. "
        r"Let $g(x) = \displaystyle\int_0^x f(t)\,dt$."), [
        Part("a", r"Find $g(-2)$ and $g(6)$.", selfcheck(r"g(-2) = 0,\ \ g(6) = 2 - 2\pi"),
             r"$g(-2) = -\int_{-2}^0 f(t)\,dt = -(-1 + 1) = 0$. $g(6) = \frac12(2)(2) - \frac12\pi(2)^2 = 2 - 2\pi$.", [(1, "$g(-2)$"), (1, "$g(6)$")], work="2.6cm"),
        Part("b", r"On what open intervals is $g$ increasing? Give a reason for your answer.", selfcheck(r"(-1, 2)"),
             r"$g'(x) = f(x) > 0$ on $-1 < x < 2$, so $g$ is increasing on $(-1, 2)$.", [(1, "interval with reason")], work="1.8cm"),
        Part("c", r"Find the absolute maximum value of $g$ on the closed interval $[-2, 6]$. Justify your answer.", num(2),
             r"$g' = f$ changes sign at $x = -1$ and $x = 2$. Candidates: $g(-2) = 0$, $g(-1) = -1$, $g(2) = 2$, $g(6) = 2 - 2\pi$. The absolute maximum is $2$, at $x = 2$.",
             [(1, "considers $x = -1$, $x = 2$ and the endpoints"), (1, "answer with justification")], work="2.6cm"),
        Part("d", r"Find the $x$-coordinate of each point of inflection of the graph of $g$ on $-2 < x < 6$. Give a reason for your answer.", selfcheck(r"x = 0 \text{ and } x = 4"),
             r"$g'' = f'$. $f$ changes from increasing to decreasing at $x = 0$ and from decreasing to increasing at $x = 4$, so the graph of $g$ has points of inflection at $x = 0$ and $x = 4$.",
             [(1, "$x = 0$ and $x = 4$"), (1, "reason")], work="2.2cm"),
    ], frq_type="Graph of f'", figure=FIG_Q),
]

TOPIC = Topic(
    number="6.5", title="Interpreting the Behavior of Accumulation Functions Involving Area",
    unit="Unit 6: Integration and Accumulation of Change", ced=["FUN-5.A", "FUN-5.A.1", "FUN-5.A.2"],
    goals=r"Determine values, intervals of increase, extrema and concavity of an accumulation function from the graph or formula of the function being accumulated.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
