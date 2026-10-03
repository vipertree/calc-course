"""Topic 6.4: The Fundamental Theorem of Calculus and accumulation functions.

CED: FUN-5.A (FUN-5.A.1-FUN-5.A.4): g(x) = integral from a to x of f(t) dt is an accumulation function; if f is
continuous, g'(x) = f(x) (FTC part 1); with an inside function on top, d/dx integral_a^{u(x)} f(t) dt = f(u(x)) u'(x).
Worked examples: FTC directly, sin x on top (chain rule), x on the bottom (swap the limits).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, expr, num, same,
                     selfcheck)
from calclib.figs import graph

x, t = sp.symbols("x t", real=True)


def d_acc(f, lo, hi):
    """d/dx of the integral of f(t) from lo to hi (limits may depend on x), by the FTC and the chain rule."""
    return sp.simplify(f.subs(t, hi) * sp.diff(hi, x) - f.subs(t, lo) * sp.diff(lo, x))


same("ftc", [d_acc(t**2 - 3 * t, 2, x).subs(x, 4), d_acc(sp.cos(t), 1, x**2), d_acc(t**4 + 1, x, 5)], [4, 2 * x * sp.cos(x**2), -(x**4 + 1)])

FP = sp.Piecewise((2, t < 2), (2 - 2 * (t - 2), t < 4), (-2 + (t - 4), True))
FIG_F = graph("t6_4_f", [("2+0*x", 0, 2), ("2-2*(x-2)", 2, 4), ("-2+(x-4)", 4, 6)], xr=(0, 6), yr=(-3, 3), ylabel="f(t)", xlabel="t",
              caption="The graph of $f$, made of three line segments.")
G = lambda v: sp.integrate(FP, (t, 0, v))
same("frq", [G(2), G(3), G(4), G(6), FP.subs(t, 3), FP.subs(t, 5)], [4, 5, 4, 2, 0, -1])

NOTES = [
    Video("s6_4.py::Lesson", "Accumulation functions", 5),

    Section("Accumulation functions"),
    Formula("Accumulation function", (
        r"\[ A(x) = \int_a^x f(t)\,dt \] is the running total of the area under $f$ from a fixed start $a$ to a moving end $x$. "
        r"The variable inside is $t$, so it doesn't get mixed up with the input $x$. At the start, $A(a) = \blank{0}$.")),

    Section("The Fundamental Theorem of Calculus, part 1"),
    Text(r"Move $x$ to $x + h$: the area grows by a sliver about $f(x)$ tall and $h$ wide, so $\frac{A(x + h) - A(x)}{h} \approx f(x)$. As $h \to 0$, this becomes exact."),
    Formula("FTC, part 1", (
        r"If $f$ is continuous, then \[ \frac{d}{dx}\int_a^x f(t)\,dt = \blank{f(x)}. \] "
        r"With a function of $x$ on top: \[ \frac{d}{dx}\int_a^{u(x)} f(t)\,dt = f\left(u(x)\right) \cdot \blank{u'(x)}. \]")),
    Text(r"\textbf{$x$ on the bottom.} Swap the limits first, which changes the sign: $\int_x^b f(t)\,dt = -\int_b^x f(t)\,dt$."),
    VideoExample('Using the theorem', work="2.2cm"),
    BigIdea(r"An accumulation function is a running total. Its derivative is the function being added up: $\frac{d}{dx}\int_a^x f(t)\,dt = f(x)$."),
    Check(r"Find $\dfrac{d}{dx}\displaystyle\int_1^x \frac{1}{1 + t^2}\,dt$.", expr(1 / (1 + x**2)), r"By the FTC: $\frac{1}{1 + x^2}$."),
]

# ---------------------------------------------------------------- practice
P = [(sp.sqrt(t**2 + 5), 0, x), (sp.exp(-t**2), 2, x), (t * sp.sin(t), sp.pi, x), (sp.cos(t), 0, 3 * x), (t**3, 1, x**2), (sp.log(t), 1, sp.exp(x)),
     (1 + t**2, x, 4), (t**2 + 1, x**3, 2)]
PRACTICE = [Item(rf"Find $\dfrac{{d}}{{dx}}\displaystyle\int_{{{sp.latex(lo)}}}^{{{sp.latex(hi)}}} {sp.latex(f)}\,dt$.", expr(d_acc(f, lo, hi)),
                 rf"$= {sp.latex(d_acc(f, lo, hi))}$" + (r" (chain rule on the top limit)" if hi != x and sp.sympify(hi).has(x) else "") + (r" (swap the limits: the sign changes)" if sp.sympify(lo).has(x) else ""),
                 work="1.6cm") for f, lo, hi in P]
PRACTICE += [
    Item(r"$g(x) = \displaystyle\int_1^x \left(t^3 - 4t\right) dt$. Find $g'(2)$.", num(0), r"$g'(x) = x^3 - 4x$, so $g'(2) = 8 - 8 = 0$.", work="1.4cm"),
    Item(r"$g(x) = \displaystyle\int_5^x \cos(\pi t)\,dt$. Find $g(5)$ and $g'(5)$. Enter $g'(5)$.", num(-1), r"$g(5) = 0$; $g'(5) = \cos 5\pi = -1$.", work="1.4cm"),
    Item(r"$g(x) = \displaystyle\int_0^x f(t)\,dt$ with $f$ as shown. Find $g(4)$.", num(4), r"Area: $(2)(2) = 4$, then $+1$ and $-1$ from the triangles on $[2, 3]$ and $[3, 4]$: $g(4) = 4$.",
         work="1.6cm", figure=FIG_F),
    Item(r"With the same $f$ and $g(x) = \displaystyle\int_0^x f(t)\,dt$, find $g'(5)$.", num(-1), r"$g'(5) = f(5) = -1$.", work="1.2cm"),
]
same("p", [d_acc(t**3 - 4 * t, 1, x).subs(x, 2), d_acc(sp.cos(sp.pi * t), 5, x).subs(x, 5)], [0, -1])

# ---------------------------------------------------------------- quiz
def q(f, lo, hi):
    return Item(rf"Find $\dfrac{{d}}{{dx}}\displaystyle\int_{{{sp.latex(lo)}}}^{{{sp.latex(hi)}}} {sp.latex(f)}\,dt$.", expr(d_acc(f, lo, hi)), rf"$= {sp.latex(d_acc(f, lo, hi))}$.", work="1.4cm")


QUIZ = [
    Variants(q(t**2 + 1, 0, x), q(sp.sin(t**2), 1, x), q(sp.sqrt(1 + t), 3, x)),
    Variants(q(sp.cos(t), 0, x**2), q(sp.exp(t), 0, 2 * x), q(t**2, 1, sp.sin(x))),
    Variants(q(t**3, x, 2), q(sp.exp(t), x, 0), q(sp.sqrt(t), x, 4)),
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
    MCQ(r"$\dfrac{d}{dx}\displaystyle\int_0^{x^3} \sqrt{1 + t^2}\,dt = $", [r"$\sqrt{1 + x^6}$", r"$3x^2\sqrt{1 + x^6}$", r"$3x^2\sqrt{1 + x^2}$", r"$\sqrt{1 + x^2}$"], "B",
        r"$f(x^3) \cdot 3x^2 = \sqrt{1 + x^6} \cdot 3x^2$.", why_not={"A": "missing the chain rule factor"}),
    MCQ(r"If $F(x) = \displaystyle\int_2^x \frac{1}{t^2 + 1}\,dt$, then $F'(2) = $", [r"$0$", r"$\frac15$", r"$\frac{1}{4}$", r"$-\frac{4}{25}$"], "B", r"$F'(2) = \frac{1}{4 + 1} = \frac15$.",
        why_not={"A": "that's $F(2)$"}),
    MCQ(r"$\dfrac{d}{dx}\displaystyle\int_x^1 \cos\left(t^2\right) dt = $", [r"$\cos\left(x^2\right)$", r"$2x\cos\left(x^2\right)$", r"$\cos 1 - \cos\left(x^2\right)$", r"$-\cos\left(x^2\right)$"], "D",
        r"Swap the limits: $-\int_1^x \cos(t^2)\,dt$, derivative $-\cos(x^2)$."),
    MCQ(r"$g(x) = \displaystyle\int_0^x f(t)\,dt$, where $f$ is continuous. Which is true?", [r"$g'(x) = f'(x)$", r"$g(x) = f(x)$", r"$g'(x) = f(x)$", r"$g'(x) = f(x) - f(0)$"], "C",
        r"FTC part 1."),
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
