"""Topic 6.4: The Fundamental Theorem of Calculus and accumulation functions.

CED: FUN-5.A (FUN-5.A.1-FUN-5.A.4): F(x) = integral from a to x of f(t) dt is an accumulation function; if f is
continuous, F'(x) = f(x) (the Fundamental Theorem of Calculus); with a function of x on top, d/dx F(g(x)) = F'(g(x)) g'(x).
Adder's rewrite (2026-10-14): big F; F(1), F(2) as triangle areas for f(t) = 2t; the theorem stated as "If F(x) = ...,
then F'(x) = f(x)"; plain substitution before the chain rule; problems read "F(x) = ..., find F'(x)" with varied names.
Worked examples: the chain rule with the inner function named, x on the bottom, x at both ends (split the integral).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, FigureRow, Formula, Item, Part, Section, Text, Topic, Variants, Video, expr, num,
                     same, selfcheck)
from calclib.figs import graph

x, t = sp.symbols("x t", real=True)


def d_acc(f, lo, hi):
    """d/dx of the integral of f(t) from lo to hi (limits may depend on x), by the FTC and the chain rule."""
    return sp.simplify(f.subs(t, hi) * sp.diff(hi, x) - f.subs(t, lo) * sp.diff(lo, x))


# the lesson's video: F(1), F(2), F(3) for f(t) = 2t; F'(2) = 3; g'(4) = 4; the chain-rule examples; x at both ends
same("ftc", [sp.integrate(2 * t, (t, 0, v)) for v in (1, 2, 3)] + [sp.diff(sp.integrate(2 * t, (t, 0, x)), x)], [1, 4, 9, 2 * x])
same("video", [d_acc(sp.sqrt(1 + t**3), 1, x).subs(x, 2), d_acc(t**2 - 3 * t, 2, x).subs(x, 4), d_acc(sp.cos(t), 1, x**2), d_acc(sp.exp(t**2), 3, sp.sin(x)),
               d_acc(t**4 + 1, x, 5), d_acc(sp.sqrt(t**4 + 1), 3 * x, x**2)],
     [3, 4, 2 * x * sp.cos(x**2), sp.exp(sp.sin(x)**2) * sp.cos(x), -(x**4 + 1), 2 * x * sp.sqrt(x**8 + 1) - 3 * sp.sqrt(81 * x**4 + 1)])

FP = sp.Piecewise((2, t < 2), (2 - 2 * (t - 2), t < 4), (-2 + (t - 4), True))
FIG_F = graph("t6_4_f", [("2+0*x", 0, 2), ("2-2*(x-2)", 2, 4), ("-2+(x-4)", 4, 6)], xr=(0, 6), yr=(-3, 3), ylabel="f(t)", xlabel="t",
              caption="The graph of $f$, made of three line segments.")
G = lambda v: sp.integrate(FP, (t, 0, v))
same("frq", [G(2), G(3), G(4), G(6), FP.subs(t, 3), FP.subs(t, 5)], [4, 5, 4, 2, 0, -1])

# F(1) and F(2) as triangles under f(t) = 2t, and F(x) = x^2 graphed as a function of its own
FIG_TRI = graph("t6_4_tri", [("2*x", 0, 3.2)], xr=(0, 3.5), yr=(0, 7), xlabel="t", ylabel="f(t)", w="5.4cm", h="4.6cm",
                under=r"\fill[ink!12] (axis cs:0,0) -- (axis cs:2,0) -- (axis cs:2,4) -- cycle;"
                      r"\fill[ink!30] (axis cs:0,0) -- (axis cs:1,0) -- (axis cs:1,2) -- cycle;",
                caption=r"The graph of $f(t) = 2t$. $F(1)$ is the dark triangle; $F(2)$ is the whole shaded triangle.")
FIG_SQ = graph("t6_4_sq", [("x^2", 0, 3.1)], xr=(0, 3.5), yr=(0, 10), ystep=2, xlabel="x", ylabel="F(x)", w="5.4cm", h="4.6cm",
               closed=[(0, 0), (1, 1), (2, 4), (3, 9)], caption=r"The graph of $F(x) = \int_0^x 2t\,dt = x^2$.")

NOTES = [
    Video("s6_4.py::Lesson", "The Fundamental Theorem of Calculus", 9.3),

    Section("Accumulation functions"),
    Formula("Accumulation function", (
        r"\[ F(x) = \int_a^x f(t)\,dt \] We integrate $f(t)$ from a fixed start $a$ up to a moving end $x$, so $F(x)$ is the area under $f$ "
        r"from $a$ to $x$: a running total. The variable inside is $t$, so it doesn't get mixed up with the input $x$. At the start, $F(a) = \blank{0}$.")),
    Text(r"\textbf{Example.} Let $f(t) = 2t$ and $F(x) = \int_0^x 2t\,dt$. Each value of $F$ is a triangle's area: "
         r"$F(1) = \frac12(1)(2) = \blank{1}$, $F(2) = \frac12(2)(4) = \blank{4}$, and $F(3) = \frac12(3)(6) = 9$. "
         r"So $F(x) = x^2$. $F$ is a function of its own, with its own graph, so it has a derivative."),
    FigureRow([FIG_TRI, FIG_SQ]),

    Section("The Fundamental Theorem of Calculus"),
    Text(r"Nudge $x$ by $\Delta x$. $F$ grows by $\Delta F$, which is the thin sliver of area under $f$ from $x$ to $x + \Delta x$. The sliver is almost a "
         r"rectangle, $f(x)$ tall and $\Delta x$ wide, so $\Delta F \approx f(x) \cdot \Delta x$ and $\frac{\Delta F}{\Delta x} \approx f(x)$. "
         r"As $\Delta x \to 0$ this becomes exact: \[ F'(x) = \lim_{\Delta x \to 0} \frac{\Delta F}{\Delta x} = f(x). \]"),
    Formula("The Fundamental Theorem of Calculus", (
        r"For a continuous function $f$: \[ \text{If } F(x) = \int_a^x f(t)\,dt, \ \text{ then } \ F'(x) = \blank{f(x)}. \]")),
    Text(r"\textbf{Check it.} For $f(t) = 2t$ we found $F(x) = x^2$, and $F'(x) = 2x = f(x)$."),
    BigIdea(r"Integrating and taking a derivative undo each other: integrate $f$ up to $x$, take the derivative, and you get $f$ back. "
            r"The Fundamental Theorem joins the two halves of calculus, derivatives (slopes and rates) and integrals (Riemann sums and areas)."),
    VideoExample('Just substitute', work="1.6cm"),
    VideoExample('Using the theorem', work="2.2cm"),

    Section("With the chain rule"),
    Formula("A function of $x$ on top", (
        r"Let $F(x) = \int_a^x f(t)\,dt$. A function $g(x)$ on top is $F$ of the inner function: \[ \int_a^{g(x)} f(t)\,dt = F(g(x)). \] "
        r"By the chain rule, \[ \frac{d}{dx}F(g(x)) = F'(g(x)) \cdot g'(x) = f(g(x)) \cdot \blank{g'(x)}. \]")),
    VideoExample('With the chain rule', work="3cm"),
    Formula("The Fundamental Theorem, with a function on top", (
        r"\[ \frac{d}{dx}\int_a^{u(x)} f(t)\,dt = \blank{f(u(x))} \cdot u'(x). \] "
        r"Put the top limit into $f$, then multiply by the top limit's derivative.")),
    Text(r"\textbf{$x$ on the bottom.} Swap the limits first, which changes the sign: \[ \int_x^b f(t)\,dt = -\int_b^x f(t)\,dt. \] "
         r"\textbf{$x$ at both ends.} Split the integral at a fixed number $c$, so each piece has one moving limit: "
         r"\[ \int_{u(x)}^{v(x)} f(t)\,dt = -\int_c^{u(x)} f(t)\,dt + \int_c^{v(x)} f(t)\,dt. \]"),
    Check(r"$F(x) = \int_1^x \frac{1}{1 + t^2}\,dt$. Find $F'(x)$.", expr(1 / (1 + x**2)), r"By the Fundamental Theorem: $F'(x) = \frac{1}{1 + x^2}$."),
]

# ---------------------------------------------------------------- practice: "F(x) = ..., find F'(x)", with varied names
P = [("F", sp.sqrt(t**2 + 5), 0, x), ("G", sp.exp(-t**2), 2, x), ("h", t * sp.sin(t), sp.pi, x), ("k", sp.cos(t), 0, 3 * x), ("P", t**3, 1, x**2),
     ("Q", sp.log(t), 1, sp.exp(x)), ("r", 1 + t**2, x, 4), ("S", t**2 + 1, x**3, 2), ("W", 1 / (1 + t**2), 2 * x, x**3)]


def how(lo, hi):
    """The note after a practice answer: which move the problem needed."""
    lo, hi = sp.sympify(lo), sp.sympify(hi)
    if lo.has(x) and hi.has(x):
        return r" (split at a fixed number, then the chain rule on each limit)"
    if lo.has(x):
        return r" (swap the limits: the sign changes)" + (r", then the chain rule" if lo != x else "")
    if hi != x:
        return r" (chain rule: the inner function is $" + sp.latex(hi) + r"$)"
    return r" (the Fundamental Theorem: put $x$ in for $t$)"


PRACTICE = [Item(rf"${n}(x) = \displaystyle\int_{{{sp.latex(lo)}}}^{{{sp.latex(hi)}}} {sp.latex(f)}\,dt$. Find ${n}'(x)$.", expr(d_acc(f, lo, hi)),
                 rf"${n}'(x) = {sp.latex(d_acc(f, lo, hi))}$" + how(lo, hi), work="1.8cm" if sp.sympify(lo).has(x) and sp.sympify(hi).has(x) else "1.6cm")
            for n, f, lo, hi in P]
PRACTICE += [
    Item(r"$g(x) = \displaystyle\int_1^x \left(t^3 - 4t\right) dt$. Find $g'(2)$.", num(0), r"$g'(x) = x^3 - 4x$, so $g'(2) = 8 - 8 = 0$.", work="1.4cm"),
    Item(r"$H(x) = \displaystyle\int_5^x \cos(\pi t)\,dt$. Find $H(5)$ and $H'(5)$. Enter $H'(5)$.", num(-1), r"$H(5) = 0$; $H'(5) = \cos 5\pi = -1$.", work="1.4cm"),
    Item(r"Jordan sets out a rain barrel. Rain collects in it at a rate of $r(t) = \frac{6t}{t + 1}$ liters per hour, $t$ hours after they set it out. "
         r"$V(x) = \displaystyle\int_0^x r(t)\,dt$ is the water collected in the first $x$ hours. Find $V'(3)$ and give its units.", num(sp.Rational(9, 2)),
         r"By the Fundamental Theorem, $V'(x) = r(x)$, so $V'(3) = \frac{18}{4} = 4.5$ liters per hour: 3 hours in, the water in the barrel is rising at $4.5$ liters per hour.",
         work="1.6cm"),
    Item(r"$g(x) = \displaystyle\int_0^x f(t)\,dt$ with $f$ as shown. Find $g(4)$.", num(4), r"Area: $(2)(2) = 4$, then $+1$ and $-1$ from the triangles on $[2, 3]$ and $[3, 4]$: $g(4) = 4$.",
         work="1.6cm", figure=FIG_F),
    Item(r"With the same $f$ and $g(x) = \displaystyle\int_0^x f(t)\,dt$, find $g'(5)$.", num(-1), r"$g'(5) = f(5) = -1$.", work="1.2cm"),
]
same("p", [d_acc(t**3 - 4 * t, 1, x).subs(x, 2), d_acc(sp.cos(sp.pi * t), 5, x).subs(x, 5), d_acc(6 * t / (t + 1), 0, x).subs(x, 3),
           d_acc(1 / (1 + t**2), 2 * x, x**3)],
     [0, -1, sp.Rational(9, 2), 3 * x**2 / (1 + x**6) - 2 / (1 + 4 * x**2)])

# ---------------------------------------------------------------- quiz
def q(n, f, lo, hi):
    return Item(rf"${n}(x) = \displaystyle\int_{{{sp.latex(lo)}}}^{{{sp.latex(hi)}}} {sp.latex(f)}\,dt$. Find ${n}'(x)$.", expr(d_acc(f, lo, hi)),
                rf"${n}'(x) = {sp.latex(d_acc(f, lo, hi))}$.", work="1.4cm")


QUIZ = [
    Variants(q("F", t**2 + 1, 0, x), q("G", sp.sin(t**2), 1, x), q("H", sp.sqrt(1 + t), 3, x)),
    Variants(q("P", sp.cos(t), 0, x**2), q("Q", sp.exp(t), 0, 2 * x), q("R", t**2, 1, sp.sin(x))),
    Variants(q("k", t**3, x, 2), q("m", sp.exp(t), x, 0), q("n", sp.sqrt(t), x, 4)),
    Variants(
        Item(r"$g(x) = \displaystyle\int_2^x (3t - 1)\,dt$. Find $g'(3)$.", num(8), r"$g'(3) = 9 - 1 = 8$.", work="1cm"),
        Item(r"$g(x) = \displaystyle\int_0^x \left(t^2 + t\right) dt$. Find $g'(2)$.", num(6), r"$g'(2) = 4 + 2 = 6$.", work="1cm"),
        Item(r"$g(x) = \displaystyle\int_1^x \frac{t}{t + 1}\,dt$. Find $g'(1)$.", num(sp.Rational(1, 2)), r"$g'(1) = \frac12$.", work="1cm"),
    ),
    Variants(
        Item(r"$g(x) = \displaystyle\int_4^x \sqrt{t^3 + 1}\,dt$. Find $g(4)$.", num(0), r"The integral from $4$ to $4$ is $0$.", work="1cm"),
        Item(r"$g(x) = \displaystyle\int_{-1}^x e^{t^2}\,dt$. Find $g(-1)$.", num(0), r"The integral from $-1$ to $-1$ is $0$.", work="1cm"),
        Item(r"$g(x) = \displaystyle\int_\pi^x \frac{\sin t}{t}\,dt$. Find $g(\pi)$.", num(0), r"The integral from $\pi$ to $\pi$ is $0$.", work="1cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"If $H(x) = \displaystyle\int_0^{x^3} \sqrt{1 + t^2}\,dt$, then $H'(x) = $", [r"$\sqrt{1 + x^6}$", r"$3x^2\sqrt{1 + x^6}$", r"$3x^2\sqrt{1 + x^2}$", r"$\sqrt{1 + x^2}$"], "B",
        r"The inner function is $g(x) = x^3$: $H'(x) = \sqrt{1 + \left(x^3\right)^2} \cdot 3x^2 = 3x^2\sqrt{1 + x^6}$.", why_not={"A": "missing the chain rule factor"}),
    MCQ(r"If $F(x) = \displaystyle\int_2^x \frac{1}{t^2 + 1}\,dt$, then $F'(2) = $", [r"$0$", r"$\frac15$", r"$\frac{1}{4}$", r"$-\frac{4}{25}$"], "B", r"$F'(2) = \frac{1}{4 + 1} = \frac15$.",
        why_not={"A": "that's $F(2)$"}),
    MCQ(r"If $G(x) = \displaystyle\int_x^1 \cos\left(t^2\right) dt$, then $G'(x) = $", [r"$\cos\left(x^2\right)$", r"$2x\cos\left(x^2\right)$", r"$\cos 1 - \cos\left(x^2\right)$", r"$-\cos\left(x^2\right)$"], "D",
        r"Swap the limits: $G(x) = -\int_1^x \cos(t^2)\,dt$, so $G'(x) = -\cos(x^2)$."),
    MCQ(r"$g(x) = \displaystyle\int_0^x f(t)\,dt$, where $f$ is continuous. Which is true?", [r"$g'(x) = f'(x)$", r"$g(x) = f(x)$", r"$g'(x) = f(x)$", r"$g'(x) = f(x) - f(0)$"], "C",
        r"The Fundamental Theorem of Calculus."),
]
same("m", [d_acc(sp.sqrt(1 + t**2), 0, x**3), d_acc(1 / (t**2 + 1), 2, x).subs(x, 2), d_acc(sp.cos(t**2), x, 1)],
     [3 * x**2 * sp.sqrt(x**6 + 1), sp.Rational(1, 5), -sp.cos(x**2)])

FRQS = [
    FRQ("An accumulation function", (
        r"The continuous function $f$ is defined on $0 \le t \le 6$. Its graph, made of three line segments, is shown. Let $g(x) = \displaystyle\int_0^x f(t)\,dt$."), [
        Part("a", r"Find $g(2)$ and $g(4)$.", selfcheck(r"g(2) = 4,\ \ g(4) = 4"),
             r"$g(2) = (2)(2) = 4$. On $[2, 4]$ the area above the axis ($\frac12(1)(2) = 1$) and below ($1$) cancel, so $g(4) = 4 + 1 - 1 = 4$.",
             [(1, "$g(2)$"), (1, "$g(4)$")], work="2.4cm"),
        Part("b", r"Find $g'(3)$ and $g'(5)$.", selfcheck(r"g'(3) = 0,\ \ g'(5) = -1"), r"By the Fundamental Theorem of Calculus, $g'(x) = f(x)$: $g'(3) = f(3) = 0$ and $g'(5) = f(5) = -1$.",
             [(1, "$g'(x) = f(x)$ with both values")], work="1.8cm"),
        Part("c", r"Find $g(6)$.", num(2), r"$g(6) = g(4) + \int_4^6 f(t)\,dt = 4 - \frac12(2)(2) = 2$.", [(1, "answer")], work="1.6cm"),
    ], frq_type="Graph of f'", figure=FIG_F),
]

TOPIC = Topic(
    number="6.4", title="The Fundamental Theorem of Calculus and Accumulation Functions",
    unit="Unit 6: Integration and Accumulation of Change", ced=["FUN-5.A", "FUN-5.A.1", "FUN-5.A.2", "FUN-5.A.3", "FUN-5.A.4"],
    goals=r"Represent accumulation functions with definite integrals and find their derivatives with the Fundamental Theorem of Calculus, including the chain rule.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
