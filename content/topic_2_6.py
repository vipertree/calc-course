"""Topic 2.6: Derivative rules: constant, sum, difference, and constant multiple.

CED: FUN-3.A.2 (constant, sum, difference, constant-multiple rules).
"""
import sympy as sp

from calclib import (Variants, FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Table, Text, Topic, Video, VideoExample,
                     expr, num, same, selfcheck)

x = sp.symbols("x")
t = sp.symbols("t")
same("poly", sp.diff(4 * x**3 - 5 * x**2 + 7 * x - 2, x), 12 * x**2 - 10 * x + 7)


def D(e, v=x):
    return sp.expand(sp.diff(e, v))


NOTES = [
    Video("s2_6.py::Lesson", "Four basic rules", 2.5),

    Section("The rules"),
    Formula("Basic derivative rules", (
        r"\textbf{Constant:} $\displaystyle \dfrac{d}{dx}[c] = \mblank{0}$. \qquad "
        r"\textbf{Constant multiple:} $\displaystyle \frac{d}{dx}[c\,f(x)] = \mblank{c\,f'(x)}$. \par "
        r"\textbf{Sum and difference:} \[ \frac{d}{dx}[f(x) \pm g(x)] = \mblank{f'(x) \pm g'(x)} \].")),
    Text(r"Adding a constant shifts a graph \blank{vertically} and does not change any slope. Multiplying by $c$ stretches every "
         r"rise by $c$, so every slope is multiplied by \mblank{c}."),

    Section("Differentiating term by term"),
    VideoExample("A polynomial", work="2cm"),
    Text(r"\textbf{Name what you write.} Write ``$f(x) = \ldots$'' for the function and ``$f'(x) = \ldots$'' (or $y'$, or $\dfrac{dy}{dx}$) for its derivative, never a bare expression."),
    VideoExample("Rewrite, then differentiate", work="2.4cm"),
    Text(r"\textbf{Splitting a fraction} works only when the denominator is a \blank{single term}: \[ \frac{x^3 - 2x + 5}{x} = \frac{x^3}{x} - \frac{2x}{x} + \frac5x, \quad\text{but}\quad \frac{5}{x + 2} \ne \frac5x + \frac52. \]"),
    Text(r"\textbf{Horizontal tangents.} A horizontal line has slope \blank{$0$}, so ``where is the tangent horizontal?'' really asks ``where does the \blank{derivative} equal $0$?''"),
    VideoExample("Horizontal tangents", work="2cm"),
    VideoExample("In context", work="2.4cm"),
    BigIdea(r"Constants vanish, constant multiples come along, and sums split into sums of derivatives."),
    Check(r"Find \[ \frac{d}{dx}\left[3\sqrt{x} - \frac{2}{x} + \pi^2\right]. \]", expr("3/(2*sqrt(x)) + 2/x**2"),
          r"\[ 3\cdot\frac12x^{-1/2} - 2(-1)x^{-2} + 0 = \frac{3}{2\sqrt x} + \frac{2}{x^2}. \] Note $\pi^2$ is a constant."),
]
same("ex2", D((x**3 - 2 * x + 5) / x), 2 * x - 5 / x**2)
same("ex3", sorted(sp.solve(3 * x**2 - 12, x)), [-2, 2])
n = sp.symbols("n")
same("ex4", sp.diff(500 + 20 * n - n**2 / 100, n).subs(n, 100), 18)
same("check", D(3 * sp.sqrt(x) - 2 / x + sp.pi**2), 3 / (2 * sp.sqrt(x)) + 2 / x**2)

# ---------------------------------------------------------------- practice
P = [(r"y = 7x^4 - 3x^2 + 9", 7 * x**4 - 3 * x**2 + 9), (r"y = \dfrac{x^5}{10} - 4x", x**5 / 10 - 4 * x),
     (r"y = 6\sqrt{x} + \dfrac{3}{x^2}", 6 * sp.sqrt(x) + 3 / x**2), (r"y = (2x + 1)^2", (2 * x + 1)**2),
     (r"y = \dfrac{x^2 + 4x}{\sqrt{x}}", (x**2 + 4 * x) / sp.sqrt(x)), (r"y = 5 - \dfrac{x}{3} + e^2", 5 - x / 3 + sp.E**2)]
SOL = [r"$28x^3 - 6x$.", r"$\frac12 x^4 - 4$.", r"$3x^{-1/2} - 6x^{-3}$.", r"Expand to $4x^2 + 4x + 1$: $8x + 4$.",
       r"Rewrite as $x^{3/2} + 4x^{1/2}$: $\frac32 x^{1/2} + 2x^{-1/2}$.", r"$-\frac13$ ($e^2$ is a constant)."]
PRACTICE = [Item(rf"Find $\dfrac{{dy}}{{dx}}$ for ${tex}$.", expr(str(D(e))), sol, work="1.8cm") for (tex, e), sol in zip(P, SOL)]
PRACTICE += [
    Item(r"Find the equation for the line tangent to $f(x) = x^3 - 4x^2 + 2$ at $x = 1$.", expr("-5*x+4"),
         r"$f(1) = -1$, $f'(x) = 3x^2 - 8x$, $f'(1) = -5$: $y = -5x + 4$.", work="2.2cm"),
    Item(r"At what $x$-values does $y = 2x^3 + 3x^2 - 36x$ have horizontal tangents? Enter the positive one.", num(2),
         r"$6x^2 + 6x - 36 = 6(x+3)(x-2) = 0$: $x = -3$ or $x = 2$.", work="2cm"),
    Item(r"A ball's height is $h(t) = 64t - 16t^2 + 6$ feet after $t$ seconds. Find $h'(1)$ and interpret it.", num(32),
         r"$h'(t) = 64 - 32t$, so $h'(1) = 32$: at 1 second the ball is rising at 32 feet per second.", work="2cm"),
    Item(r"If $f'(x) = g'(x)$ for all $x$, must $f(x) = g(x)$? Explain.", selfcheck(r"\text{No: they can differ by a constant}"),
         r"No. For example $x^2$ and $x^2 + 5$ have the same derivative. The graphs are vertical shifts of each other.", work="2cm"),
]
same("p7", sp.expand(-1 + (-5) * (x - 1)), -5 * x + 4)
same("p9", sp.diff(64 * t - 16 * t**2 + 6, t).subs(t, 1), 32)

# extra practice (round 1)
P2 = [(r"y = 4x^3 - 5x + \dfrac{1}{2}", 4 * x**3 - 5 * x + sp.Rational(1, 2), r"$12x^2 - 5$."),
      (r"y = \dfrac{2}{x^3} - 8\sqrt[4]{x}", 2 / x**3 - 8 * x**sp.Rational(1, 4),
       r"Rewrite as $2x^{-3} - 8x^{1/4}$: $-6x^{-4} - 2x^{-3/4}$."),
      (r"y = x^2(3x - 1)", x**2 * (3 * x - 1), r"Expand to $3x^3 - x^2$: $9x^2 - 2x$."),
      (r"y = \dfrac{6x^4 - x}{2x}", (6 * x**4 - x) / (2 * x), r"Divide first: $3x^3 - \frac12$. So $9x^2$."),
      (r"y = \pi x^2 + \sqrt{7}", sp.pi * x**2 + sp.sqrt(7), r"$2\pi x$ ($\sqrt7$ is a constant).")]
for tex, e, sol in P2:
    PRACTICE.append(Item(rf"Find $\dfrac{{dy}}{{dx}}$ for ${tex}$.", expr(str(D(e))), sol, work="1.8cm"))
PRACTICE += [
    Item(r"Find the equation for the line tangent to $f(x) = 2x^2 - \dfrac{4}{x}$ at $x = 2$.", expr("9*x-12"),
         r"$f(2) = 8 - 2 = 6$. $f'(x) = 4x + 4x^{-2}$, so $f'(2) = 8 + 1 = 9$. $y - 6 = 9(x - 2)$, so $y = 9x - 12$.",
         work="2.4cm"),
    Item(r"Find the $x$-value where the tangent line to $y = x^2 - 6x + 1$ is parallel to $y = 2x + 5$.", num(4),
         r"Parallel means slope $2$: $2x - 6 = 2$, so $x = 4$.", work="1.8cm"),
    Item(r"At how many points does $y = x^3 - 3x$ have a horizontal tangent line?", num(2),
         r"$3x^2 - 3 = 0$ gives $x = \pm1$: two points, $(1, -2)$ and $(-1, 2)$.", work="1.8cm"),
    Item(r"A particle moves along a line with position $s(t) = t^3 - 6t^2 + 9t$ meters at $t$ seconds. Find its velocity at "
         r"$t = 2$ and say which way it is moving.", num(-3, display=r"-3\text{ m/s}"),
         r"$v(t) = s'(t) = 3t^2 - 12t + 9$, so $v(2) = 12 - 24 + 9 = -3$ m/s. The particle is moving in the negative direction.",
         work="2.2cm"),
    Item(r"$f(2) = 5$ and $f'(2) = -3$. Let $g(x) = 4f(x) - x^2$. Find $g'(2)$.", num(-16),
         r"$g'(x) = 4f'(x) - 2x$, so $g'(2) = 4(-3) - 4 = -16$.", work="1.8cm"),
]
same("x1 derivs", [D(e) for _, e, _ in P2],
     [12 * x**2 - 5, -6 * x**-4 - 2 * x**sp.Rational(-3, 4), 9 * x**2 - 2 * x, 9 * x**2, 2 * sp.pi * x])
f6 = 2 * x**2 - 4 / x
same("x1 tan", sp.expand(f6.subs(x, 2) + D(f6).subs(x, 2) * (x - 2)), 9 * x - 12)
same("x1 par", sp.solve(sp.Eq(2 * x - 6, 2), x), [4])
same("x1 horiz", sp.solve(D(x**3 - 3 * x), x), [-1, 1])
same("x1 v", sp.diff(t**3 - 6 * t**2 + 9 * t, t).subs(t, 2), -3)

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find $f'(x)$ for $f(x) = 3x^4 - 2x^3 + x - 8$.", expr("12*x**3-6*x**2+1"), r"$12x^3 - 6x^2 + 1$.", work="1.6cm"),
        Item(r"Find $f'(x)$ for $f(x) = 5x^3 + 4x^2 - 7x + 2$.", expr("15*x**2+8*x-7"), r"$15x^2 + 8x - 7$.", work="1.6cm"),
        Item(r"Find $f'(x)$ for $f(x) = \dfrac{x^6}{3} - 9x + \pi$.", expr("2*x**5-9"), r"$2x^5 - 9$ ($\pi$ is a constant).", work="1.6cm"),
    ),
    Variants(
        Item(r"Find $\dfrac{dy}{dx}$ for $y = \dfrac{4}{x} - 2\sqrt{x}$.", expr("-4/x**2 - 1/sqrt(x)"), r"$-4x^{-2} - x^{-1/2}$.", work="1.6cm"),
        Item(r"Find $\dfrac{dy}{dx}$ for $y = 6\sqrt[3]{x} + \dfrac{1}{x^2}$.", expr("2*x**(-2/3) - 2/x**3"), r"$2x^{-2/3} - 2x^{-3}$.", work="1.6cm"),
        Item(r"Find $\dfrac{dy}{dx}$ for $y = \dfrac{x^3 + 2x}{x}$.", expr("2*x"), r"Divide first: $x^2 + 2$. So $2x$.", work="1.6cm"),
    ),
    Variants(
        Item(r"Find the slope of the tangent line to $y = x^2 - 6x + 10$ at $x = 5$.", num(4), r"$2x - 6 = 4$ at $x = 5$.", work="1.4cm"),
        Item(r"Find the slope of the tangent line to $y = 2x^3 - x$ at $x = -1$.", num(5), r"$6x^2 - 1 = 5$ at $x = -1$.", work="1.4cm"),
        Item(r"Find the slope of the tangent line to $y = 4\sqrt{x} - x$ at $x = 4$.", num(0), r"$2x^{-1/2} - 1 = 0$ at $x = 4$.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"If $f(x) = 7x^3 + \pi^3$, then $f'(x) =$", [r"$21x^2 + 3\pi^2$", r"$21x^2$", r"$7x^2$", r"$21x^2 + \pi^3$"], "B",
            r"$\pi^3$ is a constant.", why_not={"A": "differentiated the constant $\\pi^3$"}),
        MCQ(r"If $f(x) = e^2 x + 5$, then $f'(x) =$", [r"$2e x$", r"$e^2 x$", r"$e^2$", r"$2e$"], "C",
            r"$e^2$ is a constant multiple of $x$.", why_not={"A": "treated $e^2$ like a power of $x$"}),
        MCQ(r"If $f(x) = \dfrac{x^4}{8} - 3$, then $f'(x) =$", [r"$\dfrac{x^3}{2}$", r"$\dfrac{4x^3}{8} - 3$", r"$\dfrac{x^3}{8}$", r"$\dfrac{x^3}{2} - 3$"], "A",
            r"$\frac18\cdot 4x^3 = \frac12x^3$; the constant disappears.", why_not={"D": "differentiate the constant too: it becomes $0$"}),
    ),
    Variants(
        MCQ(r"If $g(x) = 5f(x) - 3x^2$ and $f'(2) = 4$, then $g'(2) =$", [r"$8$", r"$20$", r"$32$", r"$-12$"], "A", r"$5(4) - 6(2) = 8$."),
        MCQ(r"If $g(x) = 2f(x) + x^3$ and $f'(1) = -3$, then $g'(1) =$", [r"$-6$", r"$-3$", r"$3$", r"$-5$"], "B", r"$2(-3) + 3(1) = -3$."),
        MCQ(r"If $g(x) = f(x) - 4x$ and $f'(0) = 7$, then $g'(0) =$", [r"$7$", r"$11$", r"$3$", r"$-4$"], "C", r"$7 - 4 = 3$."),
    ),
]
same("q versions", [D(6 * x**sp.Rational(1, 3) + 1 / x**2), D(2 * x**3 - x).subs(x, -1), D(4 * sp.sqrt(x) - x).subs(x, 4), 2 * -3 + 3],
     [2 * x**sp.Rational(-2, 3) - 2 / x**3, 5, 0, -3])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"If $y = \dfrac{2x^4 - x}{x^2}$, then $\dfrac{dy}{dx} =$", [r"$4x + x^{-2}$", r"$8x^3 - 1$", r"$\dfrac{8x^3-1}{2x}$", r"$4x - x^{-2}$"], "A",
        r"$y = 2x^2 - x^{-1}$, so $y' = 4x + x^{-2}$.", why_not={"C": "differentiated top and bottom separately"}),
    MCQ(r"At what value of $x$ is the tangent line to $y = x^2 - 5x$ parallel to $y = 3x + 1$?", [r"$1$", r"$2$", r"$3$", r"$4$"], "D",
        r"$2x - 5 = 3$ gives $x = 4$."),
    MCQ(r"$f(1) = 3$, $f'(1) = -2$, $g(1) = 5$, $g'(1) = 4$. If $h(x) = 3f(x) - g(x) + 2x$, then $h'(1) =$",
        [r"$-10$", r"$-8$", r"$4$", r"$-6$"], "B", r"$3(-2) - 4 + 2 = -8$.", why_not={"A": "forgot the $+2$"}),
    MCQ(r"A particle's position is $s(t) = t^3 - 6t^2 + 9t$. At which times is its velocity $0$?",
        [r"$t = 1$ and $t = 3$", r"$t = 0$ and $t = 3$", r"$t = 2$", r"$t = 0$ only"], "A", r"$3t^2 - 12t + 9 = 3(t-1)(t-3)$."),
]
same("m1", D((2 * x**4 - x) / x**2), 4 * x + x**-2)

FRQS = [
    FRQ("A polynomial model", (
        r"The number of visitors in a museum $t$ hours after it opens is modeled by $V(t) = -4t^3 + 30t^2 + 50$ for $0 \le t \le 8$."), [
        Part("a", r"Find $V'(t)$.", expr("-12*t**2+60*t"), r"$V'(t) = -12t^2 + 60t$.", [(1, "correct derivative")], work="1.6cm"),
        Part("b", r"Find $V'(2)$ and interpret it with units.", num(72), r"$-48 + 120 = 72$: at 2 hours after opening, the number of "
             r"visitors is increasing at 72 visitors per hour.", [(1, "value $72$"), (1, "interpretation with units")], work="2cm"),
        Part("c", r"At what time $t > 0$ is the number of visitors momentarily not changing?", num(5),
             r"$-12t^2 + 60t = -12t(t - 5) = 0$: $t = 5$ hours.", [(1, "sets $V'(t) = 0$"), (1, "$t = 5$")], work="2cm"),
    ], frq_type="Rates in context"),
]
same("frq", [sp.diff(-4 * t**3 + 30 * t**2 + 50, t).subs(t, 2), sp.solve(-12 * t**2 + 60 * t, t)], [72, [0, 5]])

TOPIC = Topic(
    number="2.6", title="Derivative Rules: Constant, Sum, Difference, and Constant Multiple",
    unit="Unit 2: Differentiation", ced=["FUN-3.A", "FUN-3.A.2"],
    goals=r"Differentiate sums, differences and constant multiples of powers, including every polynomial.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
