"""Topic 3.2: Implicit differentiation.

CED: FUN-3.D.1 (implicit differentiation; the chain rule on terms in y). The circle x^2 + y^2 = 25 at (3, 4) matches the video.
"""
import sympy as sp

from calclib import (FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Text, Topic, Variants, Video, expr, num,
                     same, selfcheck)
from calclib.figs import graph

x, y, t = sp.symbols("x y t")


def imp(F):
    """dy/dx for the curve F(x, y) = 0."""
    return sp.simplify(-sp.diff(F, x) / sp.diff(F, y))


same("circle", imp(x**2 + y**2 - 25).subs({x: 3, y: 4}), sp.Rational(-3, 4))
same("ex2", imp(x**2 + x * y + y**2 - 7).subs({x: 1, y: 2}), sp.Rational(-4, 5))

FIG_C = graph("t3_2_circle", [("sqrt(25-x^2)", -5, 5), ("-sqrt(25-x^2)", -5, 5), ("4-0.75*(x-3)", 0.5, 6.3, "dashed")],
              xr=(-6, 7), yr=(-6, 6.5), closed=[(3, 4)], labels=[(3, 4, "above right", r"$(3, 4)$")], samples=240, xstep=2, ystep=2,
              w="6cm", h="5.6cm", caption=r"The circle $x^2 + y^2 = 25$ and its tangent line at $(3, 4)$.")

NOTES = [
    Video("s3_2.py::Lesson", "Implicit differentiation", 5),

    Section("A curve that isn't a function"),
    FIG_C,
    Text(r"The circle $x^2 + y^2 = 25$ fails the vertical line test, so it isn't the graph of one function. But near the point $(3, 4)$ it "
         r"looks like the graph of a function, and it has a tangent line there. We want its \blank{slope} without solving for $y$."),
    Text(r"\textbf{The idea.} Near $(3, 4)$, treat $y$ as some function of $x$, even though we don't write it down. Then $y^2$ is a "
         r"\blank{composite} function, and the chain rule says \[ \frac{d}{dx}\left[y^2\right] = \mblank{2y\,\frac{dy}{dx}} \]."),

    Section("The method"),
    Formula("Implicit differentiation", (
        r"1. Differentiate both sides of the equation with respect to $x$. Every time you differentiate a term with $y$ in it, "
        r"multiply by \blank{$\dfrac{dy}{dx}$} (the chain rule). \par "
        r"2. Collect the $\dfrac{dy}{dx}$ terms on one side and \blank{solve} for $\dfrac{dy}{dx}$.")),
    Example("The circle", r"Find $\dfrac{dy}{dx}$ for $x^2 + y^2 = 25$, and find the slope at $(3, 4)$.",
            r"$\displaystyle 2x + 2y\dfrac{dy}{dx} = 0$, so \[ \frac{dy}{dx} = -\frac{x}{y}. \] At $(3, 4)$ the slope is $-\dfrac34$.", work="2.4cm", beat="Why the answer has y in it"),
    Text(r"The answer uses \emph{both} $x$ and $y$: the circle has two points above $x = 3$, and $-\dfrac{x}{y}$ gives the slope at each one. "
         r"At $(3, -4)$ it is $\dfrac34$."),
    Example("A product term", r"Find $\dfrac{dy}{dx}$ for $x^2 + xy + y^2 = 7$, then the slope at $(1, 2)$.",
            r"\[ 2x + \left(y + x\frac{dy}{dx}\right) + 2y\frac{dy}{dx} = 0. \] Collect: \[ (x + 2y)\frac{dy}{dx} = -(2x + y), \] so "
            r"\[ \frac{dy}{dx} = -\frac{2x + y}{x + 2y}. \] At $(1, 2)$: $-\dfrac45$.", work="3cm", beat="A product term"),
    Example("Horizontal and vertical tangents", r"Where does $x^2 + y^2 = 25$ have horizontal tangent lines? Vertical ones?",
            r"\[ \frac{dy}{dx} = -\frac{x}{y}. \] Horizontal when the numerator is $0$ ($x = 0$): $(0, \pm5)$. Vertical when the denominator is $0$ "
            r"($y = 0$): $(\pm5, 0)$.", work="2.4cm", beat="Horizontal and vertical tangents"),
    BigIdea(r"Differentiate everything. Each $y$ term picks up a factor of $\frac{dy}{dx}$ from the chain rule. Then solve for $\frac{dy}{dx}$."),
    Check(r"Find $\dfrac{dy}{dx}$ for $y^3 + x = 5$.", expr("-1/(3*y**2)"), r"$\displaystyle 3y^2\dfrac{dy}{dx} + 1 = 0$, so \[ \frac{dy}{dx} = -\frac{1}{3y^2}. \]"),
]
same("ex3", imp(sp.sin(y) + sp.exp(x) - y), sp.exp(x) / (1 - sp.cos(y)))
same("check", imp(y**3 + x - 5), -1 / (3 * y**2))

# ---------------------------------------------------------------- practice
P = [(r"x^2 + 4y^2 = 16", x**2 + 4 * y**2 - 16), (r"xy = 6", x * y - 6), (r"y^2 = x^3 - 2x", y**2 - x**3 + 2 * x),
     (r"x^3 + y^3 = 9", x**3 + y**3 - 9), (r"x^2y + y = 4", x**2 * y + y - 4), (r"e^y = x^2 + 1", sp.exp(y) - x**2 - 1),
     (r"\cos y = x", sp.cos(y) - x), (r"x + \sin(xy) = 1", x + sp.sin(x * y) - 1)]
SOL = [r"$2x + 8y\,y' = 0$: $y' = -\dfrac{x}{4y}$.", r"$y + xy' = 0$: $y' = -\dfrac{y}{x}$.", r"$2yy' = 3x^2 - 2$: $y' = \dfrac{3x^2 - 2}{2y}$.",
       r"$3x^2 + 3y^2y' = 0$: $y' = -\dfrac{x^2}{y^2}$.", r"$2xy + x^2y' + y' = 0$: $y' = -\dfrac{2xy}{x^2 + 1}$.",
       r"$e^y y' = 2x$: $y' = \dfrac{2x}{e^y}$.", r"$-\sin y\,y' = 1$: $y' = -\dfrac{1}{\sin y}$.",
       r"$1 + \cos(xy)(y + xy') = 0$: $y' = -\dfrac{1 + y\cos(xy)}{x\cos(xy)}$."]
PRACTICE = [Item(rf"Find $\dfrac{{dy}}{{dx}}$ for ${tex}$. (Your answer may use $x$ and $y$.)", expr(str(imp(F))), sol, work="2.2cm")
            for (tex, F), sol in zip(P, SOL)]
PRACTICE += [
    Item(r"Find the slope of $x^2 + 4y^2 = 16$ at $\left(2, \sqrt3\right)$.", num(-1 / (2 * sp.sqrt(3))),
         r"$y' = -\dfrac{x}{4y} = -\dfrac{2}{4\sqrt3} = -\dfrac{1}{2\sqrt3}$.", work="1.6cm"),
    Item(r"Find the slope of $xy = 6$ at $(2, 3)$.", num(sp.Rational(-3, 2)), r"$y' = -\dfrac{y}{x} = -\dfrac32$.", work="1.4cm"),
    Item(r"Find the slope of $x^3 + y^3 = 9$ at $(1, 2)$.", num(sp.Rational(-1, 4)), r"$y' = -\dfrac{x^2}{y^2} = -\dfrac14$.", work="1.4cm"),
    Item(r"Find the equation for the line tangent to $x^2 + y^2 = 13$ at $(2, -3)$.", expr("2*x/3 - 13/3"),
         r"$y' = -\dfrac xy = \dfrac23$ at $(2, -3)$. $y + 3 = \frac23(x - 2)$, so $y = \frac23x - \frac{13}3$.", work="2cm"),
    Item(r"Find the equation for the line tangent to $x^2 + xy + y^2 = 7$ at $(1, 2)$.", expr("-4*x/5 + 14/5"),
         r"Slope $-\dfrac45$ (from the notes). $y - 2 = -\frac45(x - 1)$, so $y = -\frac45x + \frac{14}5$.", work="2cm"),
    Item(r"At what points does $x^2 + 4y^2 = 16$ have horizontal tangent lines? Enter the positive $y$-value.", num(2),
         r"$y' = -\dfrac{x}{4y} = 0$ when $x = 0$; then $4y^2 = 16$, $y = \pm2$.", work="2cm"),
    Item(r"At what points does $x^2 + 4y^2 = 16$ have vertical tangent lines? Enter the positive $x$-value.", num(4),
         r"The denominator $4y$ is $0$ when $y = 0$; then $x^2 = 16$, $x = \pm4$.", work="2cm"),
    Item(r"For $y^2 = x^3 - 2x$, find $\dfrac{dy}{dx}$ at $(2, 2)$.", num(sp.Rational(5, 2)), r"$\dfrac{3x^2 - 2}{2y} = \dfrac{10}{4} = \dfrac52$.", work="1.6cm"),
    Item(r"Find $\dfrac{dy}{dx}$ for $\sqrt{x} + \sqrt{y} = 5$.", expr("-sqrt(y)/sqrt(x)"),
         r"$\dfrac{1}{2\sqrt x} + \dfrac{1}{2\sqrt y}y' = 0$, so $y' = -\dfrac{\sqrt y}{\sqrt x}$.", work="2cm"),
    Item(r"Find $\dfrac{dy}{dx}$ for $\ln y = x^2$, and write it using only $x$.", expr("2*x*exp(x**2)"),
         r"$\dfrac{1}{y}y' = 2x$, so $y' = 2xy$. Since $y = e^{x^2}$, $y' = 2xe^{x^2}$.", work="2cm"),
    Item(r"Maya differentiates $x^2 + y^2 = 25$ and writes $2x + 2y = 0$. What did she forget?", selfcheck(r"\tfrac{dy}{dx} \text{ on } 2y"),
         r"The chain rule on $y^2$: it should be $2y\dfrac{dy}{dx}$, since $y$ depends on $x$.", work="1.4cm"),
    Item(r"Show that the slope of $x^2 + y^2 = r^2$ at any point is perpendicular to the radius to that point.", selfcheck(r"-\tfrac xy \cdot \tfrac yx = -1"),
         r"The radius from $(0,0)$ to $(x, y)$ has slope $\frac yx$. The tangent slope is $-\frac xy$. Their product is $-1$, so they are perpendicular.",
         work="2cm"),
]
same("p slopes", [imp(x**2 + 4 * y**2 - 16).subs({x: 2, y: sp.sqrt(3)}), imp(x * y - 6).subs({x: 2, y: 3}),
                  imp(x**3 + y**3 - 9).subs({x: 1, y: 2}), imp(y**2 - x**3 + 2 * x).subs({x: 2, y: 2})],
     [-1 / (2 * sp.sqrt(3)), sp.Rational(-3, 2), sp.Rational(-1, 4), sp.Rational(5, 2)])
same("p tangents", [sp.expand(-3 + imp(x**2 + y**2 - 13).subs({x: 2, y: -3}) * (x - 2)), sp.expand(2 + sp.Rational(-4, 5) * (x - 1))],
     [2 * x / 3 - sp.Rational(13, 3), -4 * x / 5 + sp.Rational(14, 5)])
same("p roots", sp.simplify(imp(sp.sqrt(x) + sp.sqrt(y) - 5) + sp.sqrt(y) / sp.sqrt(x)), 0)

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find $\dfrac{dy}{dx}$ for $x^2 + y^2 = 36$.", expr("-x/y"), r"$2x + 2yy' = 0$: $y' = -\dfrac xy$.", work="1.6cm"),
        Item(r"Find $\dfrac{dy}{dx}$ for $3x^2 + y^2 = 12$.", expr("-3*x/y"), r"$6x + 2yy' = 0$: $y' = -\dfrac{3x}{y}$.", work="1.6cm"),
        Item(r"Find $\dfrac{dy}{dx}$ for $y^2 - x^2 = 4$.", expr("x/y"), r"$2yy' - 2x = 0$: $y' = \dfrac xy$.", work="1.6cm"),
    ),
    Variants(
        Item(r"Find $\dfrac{dy}{dx}$ for $xy + y = 10$.", expr("-y/(x+1)"), r"$y + xy' + y' = 0$: $y' = -\dfrac{y}{x+1}$.", work="1.8cm"),
        Item(r"Find $\dfrac{dy}{dx}$ for $x^2y = 8$.", expr("-2*y/x"), r"$2xy + x^2y' = 0$: $y' = -\dfrac{2y}{x}$.", work="1.8cm"),
        Item(r"Find $\dfrac{dy}{dx}$ for $xy^2 = 4$.", expr("-y/(2*x)"), r"$y^2 + 2xyy' = 0$: $y' = -\dfrac{y}{2x}$.", work="1.8cm"),
    ),
    Variants(
        Item(r"Find the slope of $x^2 + xy + y^2 = 7$ at $(2, 1)$.", num(sp.Rational(-5, 4)),
             r"$y' = -\dfrac{2x + y}{x + 2y} = -\dfrac{5}{4}$.", work="1.8cm"),
        Item(r"Find the slope of $x^3 + y^3 = 2xy$ at $(1, 1)$.", num(-1),
             r"$3x^2 + 3y^2y' = 2y + 2xy'$, so $y' = \dfrac{2y - 3x^2}{3y^2 - 2x} = \dfrac{-1}{1} = -1$.", work="1.8cm"),
        Item(r"Find the slope of $y^2 = x^3 + 1$ at $(2, 3)$.", num(2), r"$2yy' = 3x^2$, so $y' = \dfrac{3x^2}{2y} = \dfrac{12}{6} = 2$.", work="1.8cm"),
    ),
    Variants(
        MCQ(r"When differentiating implicitly with respect to $x$, $\dfrac{d}{dx}\left[y^3\right] =$",
            [r"$3y^2$", r"$3y^2\,\dfrac{dy}{dx}$", r"$3x^2$", r"$y^3\,\dfrac{dy}{dx}$"], "B", r"Chain rule: $y$ is a function of $x$.",
            why_not={"A": "forgot the chain rule"}),
        MCQ(r"When differentiating implicitly with respect to $x$, $\dfrac{d}{dx}\left[\sin y\right] =$",
            [r"$\cos y$", r"$\cos x\,\dfrac{dy}{dx}$", r"$\cos y\,\dfrac{dy}{dx}$", r"$-\cos y\,\dfrac{dy}{dx}$"], "C", r"Chain rule on $\sin y$.",
            why_not={"A": "forgot the chain rule"}),
        MCQ(r"When differentiating implicitly with respect to $x$, $\dfrac{d}{dx}\left[xy\right] =$",
            [r"$y + x\,\dfrac{dy}{dx}$", r"$\dfrac{dy}{dx}$", r"$x + y$", r"$1\cdot\dfrac{dy}{dx}$"], "A", r"Product rule, with the chain rule on $y$.",
            why_not={"B": "that's the product of the derivatives"}),
    ),
    Variants(
        MCQ(r"At which point does $x^2 + y^2 = 9$ have a vertical tangent line?", [r"$(0, 3)$", r"$(3, 0)$", r"$(0, -3)$", r"$(\sqrt3, \sqrt6)$"], "B",
            r"$y' = -\frac xy$ is undefined (vertical) when $y = 0$ and $x \ne 0$.", why_not={"A": "that's a horizontal tangent"}),
        MCQ(r"At which point does $x^2 + 4y^2 = 4$ have a horizontal tangent line?", [r"$(2, 0)$", r"$(-2, 0)$", r"$(1, \frac{\sqrt3}{2})$", r"$(0, 1)$"], "D",
            r"$y' = -\frac{x}{4y} = 0$ when $x = 0$: $(0, \pm1)$.", why_not={"A": "that's a vertical tangent"}),
        MCQ(r"For $xy = 4$, the slope at $(1, 4)$ is", [r"$4$", r"$-4$", r"$-\dfrac14$", r"$\dfrac14$"], "B", r"$y' = -\dfrac yx = -4$.",
            why_not={"C": "inverted"}),
    ),
]
same("q slopes", [imp(x**2 + x * y + y**2 - 7).subs({x: 2, y: 1}), imp(x**3 + y**3 - 2 * x * y).subs({x: 1, y: 1}),
                  imp(y**2 - x**3 - 1).subs({x: 2, y: 3}), imp(x * y - 4).subs({x: 1, y: 4})], [sp.Rational(-5, 4), -1, 2, -4])
same("q derivs", [imp(3 * x**2 + y**2 - 12), imp(y**2 - x**2 - 4), imp(x * y + y - 10), imp(x**2 * y - 8), imp(x * y**2 - 4)],
     [-3 * x / y, x / y, -y / (x + 1), -2 * y / x, -y / (2 * x)])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"If $x^2 - 3xy + y^2 = -1$, then $\dfrac{dy}{dx}$ at $(1, 2)$ is", [r"$-\dfrac14$", r"$4$", r"$\dfrac14$", r"$-4$"], "B",
        r"$2x - 3y - 3xy' + 2yy' = 0$, so $y' = \dfrac{3y - 2x}{2y - 3x} = \dfrac{6 - 2}{4 - 3} = 4$.", why_not={"D": "sign slip moving terms"}),
    MCQ(r"An equation of the line tangent to $x^2 + y^2 = 25$ at $(-4, 3)$ is",
        [r"$y - 3 = -\frac43(x + 4)$", r"$y - 3 = \frac34(x + 4)$", r"$y - 3 = \frac43(x + 4)$", r"$y + 4 = \frac43(x - 3)$"], "C",
        r"$y' = -\frac xy = \frac43$ at $(-4, 3)$.", why_not={"A": "sign error", "B": "that's the radius direction", "D": "swapped the coordinates"}),
    MCQ(r"If $xy^3 = 8$, then $\dfrac{dy}{dx}$ at $(1, 2)$ is", [r"$-\dfrac23$", r"$-\dfrac{3}{2}$", r"$-2$", r"$\dfrac{2}{3}$"], "A",
        r"$y^3 + 3xy^2y' = 0$, so $y' = -\dfrac{y}{3x} = -\dfrac23$.", why_not={"B": "inverted"}),
    MCQ(r"If $e^{xy} = x$, then $\dfrac{dy}{dx}$ at $(1, 0)$ is", [r"$0$", r"$-1$", r"$e$", r"$1$"], "D",
        r"$e^{xy}(y + xy') = 1$. At $(1, 0)$: $1\cdot(0 + y') = 1$, so $y' = 1$.", why_not={"A": "that's $y$"}),
]
same("m1", [(x**2 - 3 * x * y + y**2).subs({x: 1, y: 2}), imp(x**2 - 3 * x * y + y**2 + 1).subs({x: 1, y: 2})], [-1, 4])
same("m2", imp(x**2 + y**2 - 25).subs({x: -4, y: 3}), sp.Rational(4, 3))
same("m3", imp(x * y**3 - 8).subs({x: 1, y: 2}), sp.Rational(-2, 3))
same("m4", imp(sp.exp(x * y) - x).subs({x: 1, y: 0}), 1)

F = x**2 + x * y + y**2 - 12
FRQS = [
    FRQ("An implicitly defined curve", r"Consider the curve given by the equation $x^2 + xy + y^2 = 12$.", [
        Part("a", r"Show that $\dfrac{dy}{dx} = -\dfrac{2x + y}{x + 2y}$.", selfcheck(r"-\tfrac{2x+y}{x+2y}"),
             r"Differentiate both sides with respect to $x$: $2x + y + x\dfrac{dy}{dx} + 2y\dfrac{dy}{dx} = 0$. "
             r"Then $(x + 2y)\dfrac{dy}{dx} = -(2x + y)$, so $\dfrac{dy}{dx} = -\dfrac{2x+y}{x+2y}$.",
             [(1, "implicit differentiation, with the product rule on $xy$"), (1, "verifies the expression for $\\frac{dy}{dx}$")],
             work="2.8cm"),
        Part("b", r"Write an equation for the line tangent to the curve at the point $(2, 2)$.", expr("4 - x"),
             r"At $(2, 2)$: $\dfrac{dy}{dx} = -\dfrac{6}{6} = -1$. The tangent line is $y = 2 - (x - 2)$.",
             [(1, "slope $-1$"), (1, "tangent line equation")], work="2.2cm"),
        Part("c", r"Find the coordinates of all points on the curve at which the line tangent to the curve is horizontal.",
             selfcheck(r"(2, -4) \text{ and } (-2, 4)"),
             r"Horizontal when $2x + y = 0$ (with $x + 2y \ne 0$), so $y = -2x$. Substituting: $x^2 - 2x^2 + 4x^2 = 12$, so $3x^2 = 12$ "
             r"and $x = \pm 2$. The points are $(2, -4)$ and $(-2, 4)$; at each, $x + 2y \ne 0$.",
             [(1, "sets $2x + y = 0$"), (1, "substitutes into the equation of the curve"), (1, "both points")], work="3cm"),
        Part("d", r"Find the coordinates of all points on the curve at which the line tangent to the curve is vertical.",
             selfcheck(r"(4, -2) \text{ and } (-4, 2)"),
             r"Vertical when $x + 2y = 0$ (with $2x + y \ne 0$), so $x = -2y$. Substituting: $4y^2 - 2y^2 + y^2 = 12$, so $y = \pm 2$. "
             r"The points are $(-4, 2)$ and $(4, -2)$.",
             [(1, "sets $x + 2y = 0$"), (1, "both points")], work="2.8cm"),
    ], frq_type="Implicit differentiation"),
]
same("frq", [F.subs({x: 2, y: 2}), imp(F).subs({x: 2, y: 2}), F.subs({x: -2, y: 4}), F.subs({x: 2, y: -4}), F.subs({x: 4, y: -2}),
             F.subs({x: -4, y: 2}), imp(F).subs({x: -2, y: 4})], [0, -1, 0, 0, 0, 0, 0])

TOPIC = Topic(
    number="3.2", title="Implicit Differentiation",
    unit="Unit 3: Differentiation: Composite, Implicit, and Inverse Functions", ced=["FUN-3.D", "FUN-3.D.1"],
    goals=r"Find $\frac{dy}{dx}$ for curves given by equations in $x$ and $y$, and use it for slopes and tangent lines.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
