"""Topic 5.12: Exploring behaviors of implicit relations.

CED: FUN-4.D (FUN-4.D.1), FUN-4.E (FUN-4.E.1, FUN-4.E.2): on an implicitly defined curve, horizontal tangents are where
dy/dx = 0 (numerator 0, denominator not), vertical tangents where the denominator is 0 (numerator not); d2y/dx2 tells
concavity and classifies a point with a horizontal tangent. Worked examples: the circle x^2 + y^2 - 4x + 6y = 12,
y^2 = x^3 - 3x + 3 (horizontal tangents), and its concavity at (1, 1).
"""
import sympy as sp

from calclib import (FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Text, Topic, Variants, Video, num,
                     same, selfcheck)

x, y = sp.symbols("x y", real=True)


def dydx(F):
    return sp.simplify(-sp.diff(F, x) / sp.diff(F, y))


def d2(F):
    """d2y/dx2 as an expression in x and y."""
    yp = dydx(F)
    return sp.simplify(sp.diff(yp, x) + sp.diff(yp, y) * yp)


def horiz(F):
    n = sp.numer(sp.together(dydx(F)))
    return sorted(sp.solve([n, F], [x, y], dict=False), key=lambda p: (float(p[0]), float(p[1])))


def vert(F):
    dd = sp.denom(sp.together(dydx(F)))
    return sorted(sp.solve([dd, F], [x, y], dict=False), key=lambda p: (float(p[0]), float(p[1])))


C1 = x**2 + y**2 - 4 * x + 6 * y - 12
C2 = y**2 - x**3 + 3 * x - 3
same("ex1", [horiz(C1), vert(C1)], [[(2, -8), (2, 2)], [(-3, -3), (7, -3)]])
same("ex2", [horiz(C2)], [[(-1, -sp.sqrt(5)), (-1, sp.sqrt(5)), (1, -1), (1, 1)]])
same("ex3", [d2(C2).subs({x: 1, y: 1})], [3])

NOTES = [
    Video("s5_12.py::Lesson", "Implicit curves", 4),

    Section("Horizontal and vertical tangents"),
    Text(r"For a curve given by an equation in $x$ and $y$, implicit differentiation (Topic 3.2) often gives $\frac{dy}{dx}$ as a fraction in $x$ and $y$. "
         r"Call its numerator $N$ and its denominator $D$, and study each on its own. What makes a slope go off to infinity? A denominator heading to zero: "
         r"that's where vertical tangents come from."),
    Formula("Tangents on an implicit curve", (
        r"Write \[ \frac{dy}{dx} = \frac{N(x, y)}{D(x, y)}. \] "
        r"\textbf{Horizontal} tangent: \blank{$N = 0$} and $D \ne 0$. \par "
        r"\textbf{Vertical} tangent: \blank{$D = 0$} and $N \ne 0$. \par "
        r"Then solve together with the \blank{equation of the curve} to find the points.")),
    Text(r"\textbf{Is the point on the curve?} On $xy = 1$, $\frac{dy}{dx} = -\frac{y}{x}$ has $D = 0$ when $x = 0$. But no point of the curve has $x = 0$ "
         r"($xy$ would be $0$, not $1$). There is \blank{no tangent line} there at all, vertical or otherwise."),
    Text(r"\textbf{Don't forget the curve.} $N = 0$ alone is a line or a curve of candidates; only the points that also lie on the original curve count."),
    Example("A circle", r"Find the points on $x^2 + y^2 = 25$ where the tangent is horizontal.",
            r"\[ \frac{dy}{dx} = -\frac{x}{y} = 0 \] when $x = 0$. On the curve, $y^2 = 25$: the points $(0, 5)$ and $(0, -5)$.", work="2.4cm", beat="Back to the curve"),

    Section("Concavity on an implicit curve"),
    Text(r"Differentiate $\frac{dy}{dx}$ again (implicitly, then substitute $\frac{dy}{dx}$) to get $\frac{d^2y}{dx^2}$. Its sign at a point gives the concavity there. "
         r"At a point with a horizontal tangent, $\frac{d^2y}{dx^2} > 0$ means the curve has a relative \blank{minimum} there, and $< 0$ a relative maximum."),
    BigIdea(r"Horizontal tangent: $N = 0$ (and $D \ne 0$). Vertical tangent: $D = 0$ (and $N \ne 0$), at a point that is really on the curve. Always solve with the curve's equation. The second derivative tells concavity."),
    Check(r"$\dfrac{dy}{dx} = \dfrac{3 - x}{y + 2}$ on some curve. Where could a vertical tangent be?", selfcheck(r"y = -2"), r"Where the denominator is $0$: on the line $y = -2$ (and on the curve)."),
]

# ---------------------------------------------------------------- practice
P1 = [x**2 + y**2 - 6 * x - 16, x**2 + 4 * y**2 - 16, x**2 - x * y + y**2 - 3, y**2 - x**3 + 12 * x]
PRACTICE = [
    Item(r"Find the points on $x^2 + y^2 - 6x = 16$ where the tangent line is horizontal. Enter the larger $y$-coordinate.", num(5),
         r"$\frac{dy}{dx} = \frac{3 - x}{y} = 0$ at $x = 3$; then $y^2 = 25$: $(3, 5)$ and $(3, -5)$.", work="2.4cm"),
    Item(r"Find the points on $x^2 + y^2 - 6x = 16$ where the tangent line is vertical. Enter the larger $x$-coordinate.", num(8),
         r"Denominator $y = 0$: $x^2 - 6x - 16 = 0$, $x = 8$ or $-2$.", work="2.2cm"),
    Item(r"Find the points on the ellipse $x^2 + 4y^2 = 16$ where the tangent line is vertical. Enter the positive $x$-coordinate.", num(4),
         r"$\frac{dy}{dx} = -\frac{x}{4y}$; vertical where $y = 0$: $x = \pm 4$.", work="2cm"),
    Item(r"Find the points on $x^2 - xy + y^2 = 3$ where the tangent is horizontal. Enter the positive $y$-coordinate.", num(2),
         r"$\frac{dy}{dx} = \frac{y - 2x}{2y - x}$; horizontal where $y = 2x$: $x^2 - 2x^2 + 4x^2 = 3$, $x = \pm1$: $(1, 2)$ and $(-1, -2)$.", work="2.6cm"),
    Item(r"Find the points on $y^2 = x^3 - 12x$ where the tangent is horizontal. Enter their $x$-coordinate.", num(-2),
         r"$2y\,y' = 3x^2 - 12$, so $y' = 0$ where $x = \pm 2$. Only $x = -2$ gives $y^2 = 16 > 0$: $(-2, 4)$ and $(-2, -4)$.", work="2.6cm"),
    Item(r"For $x^2 + y^2 = 25$, find $\dfrac{d^2y}{dx^2}$ at $(3, 4)$. Is the curve concave up or down there?", num(sp.Rational(-25, 64)),
         r"$y' = -\frac{x}{y}$, $y'' = -\frac{y - x y'}{y^2} = -\frac{x^2 + y^2}{y^3} = -\frac{25}{64}$: concave down.", work="2.6cm"),
    Item(r"For $y^2 = x^3 - 12x$, does the curve have a relative maximum or minimum at $(-2, 4)$?", selfcheck(r"\text{relative maximum}"),
         r"$y'' = \frac{6x - 2(y')^2}{2y}$; at $(-2, 4)$, $y' = 0$, so $y'' = \frac{-12}{8} < 0$: a relative maximum of the upper branch.", work="2.6cm"),
    Item(r"Why does $\frac{dy}{dx} = \frac{N}{D}$ need $D \ne 0$ for a horizontal tangent?", selfcheck(r"\frac00 \text{ is undetermined}"),
         r"If both are $0$, the slope is $\frac00$, which isn't determined by this formula; the point needs separate analysis.", work="1.4cm"),
]
same("p", [horiz(P1[0]), vert(P1[0]), vert(P1[1]), horiz(P1[2]), d2(x**2 + y**2 - 25).subs({x: 3, y: 4}), d2(P1[3]).subs({x: -2, y: 4})],
     [[(3, -5), (3, 5)], [(-2, 0), (8, 0)], [(-4, 0), (4, 0)], [(-1, -2), (1, 2)], sp.Rational(-25, 64), sp.Rational(-3, 2)])
same("p5", [[p for p in horiz(P1[3]) if p[1].is_real]], [[(-2, -4), (-2, 4)]])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"On $x^2 + y^2 - 2y = 8$, find the points with horizontal tangents. Enter the larger $y$-coordinate.", num(4), r"$y' = \frac{-x}{y - 1} = 0$ at $x = 0$: $y^2 - 2y - 8 = 0$, $y = 4, -2$.", work="2.2cm"),
        Item(r"On $x^2 + y^2 + 4y = 5$, find the points with horizontal tangents. Enter the larger $y$-coordinate.", num(1), r"$y' = \frac{-x}{y + 2} = 0$ at $x = 0$: $y^2 + 4y - 5 = 0$, $y = 1, -5$.", work="2.2cm"),
        Item(r"On $x^2 + y^2 - 8y = 9$, find the points with horizontal tangents. Enter the larger $y$-coordinate.", num(9), r"$y' = \frac{-x}{y - 4} = 0$ at $x = 0$: $y^2 - 8y - 9 = 0$, $y = 9, -1$.", work="2.2cm"),
    ),
    Variants(
        Item(r"On $x^2 + 9y^2 = 36$, find the points with vertical tangents. Enter the positive $x$-coordinate.", num(6), r"$y' = -\frac{x}{9y}$; $y = 0$ gives $x = \pm 6$.", work="1.8cm"),
        Item(r"On $4x^2 + y^2 = 16$, find the points with vertical tangents. Enter the positive $x$-coordinate.", num(2), r"$y' = -\frac{4x}{y}$; $y = 0$ gives $x = \pm 2$.", work="1.8cm"),
        Item(r"On $x^2 + 2y^2 = 18$, find the points with vertical tangents. Enter the positive $x$-coordinate.", num(sp.sqrt(18)), r"$y' = -\frac{x}{2y}$; $y = 0$ gives $x = \pm\sqrt{18}$.", work="1.8cm"),
    ),
    Variants(
        MCQ(r"$\dfrac{dy}{dx} = \dfrac{2x - y}{x - 4y}$ on a curve. Horizontal tangents can occur only where", [r"$y = 2x$", r"$x = 4y$", r"$x = 0$", r"$y = 0$"], "A", r"Numerator zero."),
        MCQ(r"$\dfrac{dy}{dx} = \dfrac{2x - y}{x - 4y}$ on a curve. Vertical tangents can occur only where", [r"$y = 2x$", r"$x = 4y$", r"$x = 0$", r"$y = 0$"], "B", r"Denominator zero."),
        MCQ(r"$\dfrac{dy}{dx} = \dfrac{x + 3}{1 - y}$ on a curve. Horizontal tangents can occur only where", [r"$y = 1$", r"$y = -3$", r"$x = -3$", r"$x = 1$"], "C", r"Numerator zero."),
    ),
    Variants(
        MCQ(r"At a point on a curve, $\dfrac{dy}{dx} = 0$ and $\dfrac{d^2y}{dx^2} = 2$. The curve has", [r"a relative maximum there", r"a relative minimum there", r"a vertical tangent there", r"an inflection point there"], "B",
            r"Horizontal tangent, concave up."),
        MCQ(r"At a point on a curve, $\dfrac{dy}{dx} = 0$ and $\dfrac{d^2y}{dx^2} = -5$. The curve has", [r"a relative maximum there", r"a relative minimum there", r"a vertical tangent there", r"an inflection point there"], "A",
            r"Horizontal tangent, concave down."),
        MCQ(r"At a point on a curve, $\dfrac{dy}{dx} = \dfrac{3}{0}$. The curve has", [r"a relative maximum there", r"a horizontal tangent there", r"a relative minimum there", r"a vertical tangent there"], "D",
            r"Nonzero over zero: vertical tangent."),
    ),
    Variants(
        Item(r"For $x^2 + y^2 = 100$, find $\dfrac{d^2y}{dx^2}$ at $(6, 8)$.", num(sp.Rational(-100, 512)), r"$y'' = -\frac{x^2 + y^2}{y^3} = -\frac{100}{512}$.", work="2.2cm"),
        Item(r"For $x^2 + y^2 = 169$, find $\dfrac{d^2y}{dx^2}$ at $(5, 12)$.", num(sp.Rational(-169, 1728)), r"$y'' = -\frac{x^2 + y^2}{y^3} = -\frac{169}{1728}$.", work="2.2cm"),
        Item(r"For $x^2 + y^2 = 25$, find $\dfrac{d^2y}{dx^2}$ at $(4, -3)$.", num(sp.Rational(25, 27)), r"$y'' = -\frac{x^2 + y^2}{y^3} = -\frac{25}{-27} = \frac{25}{27}$.", work="2.2cm"),
    ),
]
same("q", [d2(x**2 + y**2 - 100).subs({x: 6, y: 8}), d2(x**2 + y**2 - 169).subs({x: 5, y: 12}), d2(x**2 + y**2 - 25).subs({x: 4, y: -3})],
     [sp.Rational(-100, 512), sp.Rational(-169, 1728), sp.Rational(25, 27)])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"How many points on $x^2 + xy + y^2 = 12$ have a horizontal tangent?", [r"$0$", r"$1$", r"$2$", r"$4$"], "C",
        r"$y' = -\frac{2x + y}{x + 2y}$; $y = -2x$ gives $3x^2 = 12$: $(2, -4)$ and $(-2, 4)$."),
    MCQ(r"At which point on $y^3 + y = x^2$ is the tangent line horizontal?", [r"$(1, 1)$", r"$(0, 0)$", r"$(0, 1)$", r"none"], "B", r"$y'(3y^2 + 1) = 2x$, so $y' = 0$ at $x = 0$, where $y = 0$."),
    MCQ(r"For $xy = 4$, $\dfrac{d^2y}{dx^2}$ at $(2, 2)$ is", [r"$-1$", r"$\frac12$", r"$2$", r"$1$"], "D",
        r"$y = \frac4x$, $y'' = \frac{8}{x^3} = 1$."),
    MCQ(r"The curve $x^2 + 3y^2 - 2xy = 8$ has a vertical tangent at a point with positive $x$. That $x$ is about", [r"$2.828$", r"$2$", r"$3.464$", r"$1.633$"], "C",
        r"$y' = \frac{y - x}{3y - x}$; vertical where $x = 3y$: $9y^2 + 3y^2 - 6y^2 = 8$, $y = \frac{2}{\sqrt3}$, $x = 2\sqrt3 \approx 3.464$.", calc=True),
]
same("m", [len(horiz(x**2 + x * y + y**2 - 12)), d2(x * y - 4).subs({x: 2, y: 2}), [p for p in vert(x**2 + 3 * y**2 - 2 * x * y - 8) if p[0] > 0][0][0]], [2, 1, 2 * sp.sqrt(3)])

FRQS = [
    FRQ("An implicitly defined curve", r"Consider the curve given by the equation $x^2 + y^2 - 2y = 8$.", [
        Part("a", r"Show that $\dfrac{dy}{dx} = \dfrac{x}{1 - y}$.", selfcheck(r"\frac{x}{1 - y}"),
             r"$2x + 2y\dfrac{dy}{dx} - 2\dfrac{dy}{dx} = 0$, so $(2y - 2)\dfrac{dy}{dx} = -2x$ and $\dfrac{dy}{dx} = \dfrac{x}{1 - y}$.",
             [(1, "implicit differentiation"), (1, "verifies the expression for $\\frac{dy}{dx}$")], work="2.4cm"),
        Part("b", r"Find the coordinates of all points on the curve at which the line tangent to the curve is horizontal.",
             selfcheck(r"(0, 4) \text{ and } (0, -2)"),
             r"$\dfrac{dy}{dx} = 0$ when $x = 0$ (and $y \ne 1$). Then $y^2 - 2y - 8 = 0$, so $y = 4$ or $y = -2$. The points are "
             r"$(0, 4)$ and $(0, -2)$.",
             [(1, "$x = 0$"), (1, "both points")], work="2.4cm"),
        Part("c", r"Find the coordinates of all points on the curve at which the line tangent to the curve is vertical.",
             selfcheck(r"(3, 1) \text{ and } (-3, 1)"),
             r"The denominator $1 - y = 0$ when $y = 1$ (and $x \ne 0$). Then $x^2 + 1 - 2 = 8$, so $x = \pm 3$. The points are "
             r"$(3, 1)$ and $(-3, 1)$.",
             [(1, "$y = 1$"), (1, "both points")], work="2.4cm"),
        Part("d", r"Find the value of $\dfrac{d^2y}{dx^2}$ at the point $(0, 4)$. Does the curve have a relative minimum, a relative "
                  r"maximum, or neither at $(0, 4)$? Justify your answer.", num(sp.Rational(-1, 3)),
             r"$\dfrac{d^2y}{dx^2} = \dfrac{(1 - y) + x\frac{dy}{dx}}{(1 - y)^2}$. At $(0, 4)$, $\dfrac{dy}{dx} = 0$, so "
             r"$\dfrac{d^2y}{dx^2} = \dfrac{-3}{9} = -\dfrac13$. Since $\dfrac{dy}{dx} = 0$ and $\dfrac{d^2y}{dx^2} < 0$ there, the curve "
             r"has a relative maximum at $(0, 4)$.",
             [(1, "$\\frac{d^2y}{dx^2} = -\\frac13$"), (1, "relative maximum with justification")], work="2.8cm"),
    ], frq_type="Implicit differentiation"),
]
C3 = x**2 + y**2 - 2 * y - 8
same("frq", [sp.simplify(dydx(C3) - x / (1 - y)), horiz(C3), vert(C3), d2(C3).subs({x: 0, y: 4})], [0, [(0, -2), (0, 4)], [(-3, 1), (3, 1)], sp.Rational(-1, 3)])

TOPIC = Topic(
    number="5.12", title="Exploring Behaviors of Implicit Relations",
    unit="Unit 5: Analytical Applications of Differentiation", ced=["FUN-4.D", "FUN-4.D.1", "FUN-4.E", "FUN-4.E.1", "FUN-4.E.2"],
    goals=r"Find horizontal and vertical tangents on implicitly defined curves, and use $\frac{d^2y}{dx^2}$ to describe their concavity.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
