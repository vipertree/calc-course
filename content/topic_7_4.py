"""Topic 7.4: Reasoning using slope fields.

CED: FUN-7.C (FUN-7.C.3): use slope fields to sketch particular solutions and describe their behavior; equilibrium
solutions y = c where dy/dx = 0 for all x; long-run behavior; concavity from d2y/dx2 found by differentiating the
equation (y depends on x) and substituting dy/dx. Lesson example: y(2 - y). Worked examples: equilibria of y^2 - 4,
d2y/dx2 for x - y at (0, 1).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, expr, num, same, selfcheck)
from calclib.figs import slope_field

x = sp.symbols("x")
Y = sp.Function("y")(x)


def second(rhs):
    """d2y/dx2 for dy/dx = rhs(x, y): differentiate implicitly, then substitute dy/dx. Returns an expression in x and y."""
    y = sp.Symbol("y")
    r = rhs(x, Y)
    d2 = sp.diff(r, x).subs(sp.Derivative(Y, x), r)
    return sp.expand(d2.subs(Y, y))


y = sp.Symbol("y")
same("lesson", [sp.solve(y * (2 - y), y), second(lambda a, b: b * (2 - b)).subs(y, sp.Rational(3, 2)), second(lambda a, b: a - b), second(lambda a, b: a - b).subs({x: 0, y: 1})],
     [[0, 2], -sp.Rational(3, 4), 1 - x + y, 2])

FIG = slope_field("t7_4_frq", lambda a, c: a * (c - 1), [-2, -1, 0, 1, 2], [-1, 0, 1, 2, 3], (-2.5, 2.5), (-1.5, 3.5), caption=r"The slope field for $\frac{dy}{dx} = x(y - 1)$.")
FIG_L = slope_field("t7_4_l", lambda a, c: c * (2 - c), [0, 1, 2, 3, 4], [-0.5, 0, 0.5, 1, 1.5, 2, 2.5], (-0.5, 4.5), (-1, 3), caption=r"The slope field for $\frac{dy}{dx} = y(2 - y)$.")

NOTES = [
    Video("s7_4.py::Lesson", "Reasoning with slope fields", 4),

    Section("Reading a slope field"),
    Text(r"To sketch the solution through a point, start at the point and move both ways, staying \blank{tangent} to the segments; the curve never cuts across them."),
    FIG_L,
    Formula("Equilibrium solutions", (
        r"If $\frac{dy}{dx} = 0$ whenever $y = c$, then the constant function $y = c$ is a solution: an \blank{equilibrium solution}. Find them by setting the right side "
        r"(as a function of $y$) equal to $0$. For $\frac{dy}{dx} = y(2 - y)$: $y = 0$ and $y = 2$.")),
    Text(r"\textbf{Long run.} Solutions often level off at an equilibrium: for $y(2 - y)$, every solution with $y(0) > 0$ has $\lim_{x\to\infty} y = 2$."),
    Formula("Concavity", (r"Find $\frac{d^2y}{dx^2}$ by differentiating the equation with respect to $x$ (each $y$ term picks up a factor $\frac{dy}{dx}$), then substitute $\frac{dy}{dx}$. "
                          r"Its \blank{sign} at a point gives the concavity of the solution there.")),
    VideoExample('Concavity from the equation', work="3cm"),
    BigIdea(r"Slope fields show particular solutions, equilibria and long-run behavior; $\frac{d^2y}{dx^2}$ from the equation gives concavity."),
    Check(r"Find the equilibrium solutions of $\frac{dy}{dt} = 3y - y^2$.", selfcheck(r"y = 0,\ y = 3"), r"$y(3 - y) = 0$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Find the equilibrium solutions of $\frac{dy}{dt} = y^2 - 9$.", selfcheck(r"y = 3,\ y = -3"), r"$(y - 3)(y + 3) = 0$.", work="1cm"),
    Item(r"Find the equilibrium solutions of $\frac{dP}{dt} = 0.1P(500 - P)$.", selfcheck(r"P = 0,\ P = 500"), r"$P(500 - P) = 0$.", work="1cm"),
    Item(r"Find the equilibrium solution of $\frac{dT}{dt} = -0.2(T - 70)$.", selfcheck(r"T = 70"), r"$T - 70 = 0$.", work="1cm"),
    Item(r"$\frac{dy}{dx} = x + y$. Find $\frac{d^2y}{dx^2}$ in terms of $x$ and $y$.", expr(second(lambda a, b: a + b), display=sp.latex(second(lambda a, b: a + b))), r"$1 + \frac{dy}{dx} = 1 + x + y$.", work="1.4cm"),
    Item(r"$\frac{dy}{dx} = xy$. Find $\frac{d^2y}{dx^2}$ in terms of $x$ and $y$.", expr(second(lambda a, b: a * b), display=sp.latex(second(lambda a, b: a * b))),
         r"$y + x\frac{dy}{dx} = y + x^2y$.", work="1.4cm"),
    Item(r"$\frac{dy}{dx} = xy$. Is the solution through $(1, 2)$ concave up or concave down there?", selfcheck(r"\text{concave up}"), r"$\frac{d^2y}{dx^2} = y + x^2y = 2 + 2 = 4 > 0$.", work="1.4cm"),
    Item(r"$\frac{dy}{dx} = y(2 - y)$ and $y(0) = 3$. Find $\lim_{x\to\infty} y(x)$.", num(2), r"Solutions above $2$ fall toward the equilibrium $y = 2$.", work="1cm", figure=FIG_L),
    Item(r"$\frac{dy}{dx} = y(2 - y)$ and $y(0) = 1$. Is the solution increasing or decreasing at $x = 0$?", selfcheck(r"\text{increasing}"), r"$1(2 - 1) = 1 > 0$.", work="1cm"),
    Item(r"$\frac{dy}{dx} = 1 - y^2$. Find $\frac{d^2y}{dx^2}$ in terms of $y$, and the concavity of the solution through $(0, \frac12)$ there.", selfcheck(r"-2y(1 - y^2);\ \text{concave down}"),
         r"$\frac{d^2y}{dx^2} = -2y\frac{dy}{dx} = -2y(1 - y^2)$; at $y = \frac12$: $-1 \cdot \frac34 < 0$.", work="1.6cm"),
]
same("p", [second(lambda a, b: a * b).subs({x: 1, y: 2}), sp.factor(second(lambda a, b: 1 - b**2)), second(lambda a, b: 1 - b**2).subs(y, sp.Rational(1, 2))], [4, 2 * y * (y - 1) * (y + 1), -sp.Rational(3, 4)])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find the equilibrium solutions of $\frac{dy}{dt} = y(y - 4)$.", selfcheck(r"y = 0,\ y = 4"), r"$y = 0$ or $y = 4$.", work="1cm"),
        Item(r"Find the equilibrium solutions of $\frac{dy}{dt} = (y + 1)(3 - y)$.", selfcheck(r"y = -1,\ y = 3"), r"$y = -1$ or $y = 3$.", work="1cm"),
        Item(r"Find the equilibrium solution of $\frac{dy}{dt} = 5 - y$.", selfcheck(r"y = 5"), r"$y = 5$.", work="1cm"),
    ),
    Variants(*[Item(rf"$\dfrac{{dy}}{{dx}} = {sp.latex(r(x, y))}$. Find $\dfrac{{d^2y}}{{dx^2}}$ in terms of $x$ and $y$.", expr(second(r), display=sp.latex(second(r))), rf"${sp.latex(second(r))}$.", work="1.4cm")
               for r in (lambda a, b: 2 * a - b, lambda a, b: a**2 + b, lambda a, b: b - a)]),
    Variants(*[Item(rf"$\dfrac{{dy}}{{dx}} = {sp.latex(r(x, y))}$. Is the solution through $({p}, {q})$ concave up or concave down there?",
                    selfcheck(r"\text{concave up}" if second(r).subs({x: p, y: q}) > 0 else r"\text{concave down}"), rf"$\frac{{d^2y}}{{dx^2}} = {sp.latex(second(r))} = {second(r).subs({x: p, y: q})}$ there.", work="1.4cm")
               for r, p, q in ((lambda a, b: a - b, 1, 3), (lambda a, b: a * b, -1, 1), (lambda a, b: b**2, 0, 2))]),
    Variants(
        MCQ(r"For $\frac{dy}{dx} = y(3 - y)$, the solution with $y(0) = 1$ has $\lim_{x\to\infty} y = $", [r"$0$", r"$1$", r"$3$", r"$\infty$"], "C", r"It rises toward the equilibrium $y = 3$."),
        MCQ(r"For $\frac{dy}{dx} = y(3 - y)$, the solution with $y(0) = 5$ has $\lim_{x\to\infty} y = $", [r"$5$", r"$3$", r"$0$", r"$\infty$"], "B", r"It falls toward the equilibrium $y = 3$."),
        MCQ(r"For $\frac{dT}{dt} = -0.3(T - 20)$, the solution with $T(0) = 90$ has $\lim_{t\to\infty} T = $", [r"$90$", r"$0$", r"$-20$", r"$20$"], "D", r"It falls toward the equilibrium $T = 20$."),
    ),
    Variants(
        MCQ(r"Which statement about a slope field's solution curves is true?", [r"They may cross the segments", r"They follow the segments", r"They are always lines", r"They are always increasing"], "B", r"Solutions are tangent to the segments."),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"Which is an equilibrium solution of $\frac{dy}{dx} = (y - 2)\sin x$?", [r"$y = 2$", r"$y = 0$", r"$x = 0$", r"$y = \sin x$"], "A", r"$y = 2$ makes the right side $0$ for every $x$."),
    MCQ(r"If $\frac{dy}{dx} = x^2 - y$, then $\frac{d^2y}{dx^2} = $", [r"$2x - y$", r"$2x - x^2 + y$", r"$2x + x^2 - y$", r"$2x - 1$"], "B", r"$2x - \frac{dy}{dx} = 2x - x^2 + y$."),
    MCQ(r"For $\frac{dy}{dx} = x(y - 1)$, the solution through $(1, 3)$ at that point is", [r"decreasing and concave up", r"decreasing and concave down", r"increasing and concave down", r"increasing and concave up"], "D",
        r"$\frac{dy}{dx} = 2 > 0$; $\frac{d^2y}{dx^2} = (y - 1)(1 + x^2) = 4 > 0$."),
    MCQ(r"For $\frac{dy}{dt} = y^2 - 1$, between which equilibria does the solution with $y(0) = 0$ stay?", [r"$y = 0$ and $y = 1$", r"$y = -1$ and $y = 0$", r"$y = -1$ and $y = 1$", r"none: it goes to $\infty$"], "C",
        r"Equilibria $y = \pm1$; a solution can't cross them."),
]
same("m", [second(lambda a, b: a**2 - b), sp.factor(second(lambda a, b: a * (b - 1))).subs({x: 1, y: 3})], [2 * x - x**2 + y, 4])

d2 = second(lambda a, b: a * (b - 1))
same("frq", [sp.factor(d2), d2.subs({x: 1, y: 2})], [(y - 1) * (x**2 + 1), 2])
FRQS = [
    FRQ("A slope field", (r"Consider the differential equation $\dfrac{dy}{dx} = x(y - 1)$. Its slope field is shown."), [
        Part("a", r"On the slope field, sketch the solution curve that passes through the point $(0, 2)$.", selfcheck(r"\text{a curve through } (0, 2) \text{ following the segments, rising on both sides}"),
             r"The curve passes through $(0, 2)$ with a horizontal tangent, rises to the left and to the right (slopes $x(y - 1)$ have the sign of $x$ there), and follows the segments.",
             [(1, "solution curve through $(0, 2)$"), (1, "follows the slope field")], work="3cm"),
        Part("b", r"Find $\dfrac{d^2y}{dx^2}$ in terms of $x$ and $y$.", expr(d2, display=sp.latex(sp.factor(d2))),
             r"$\dfrac{d^2y}{dx^2} = (y - 1) + x\dfrac{dy}{dx} = (y - 1) + x \cdot x(y - 1) = (y - 1)(1 + x^2)$.", [(1, "product rule"), (1, "substitutes $\\frac{dy}{dx}$")], work="2.4cm"),
        Part("c", r"Is the graph of the solution through $(1, 2)$ concave up or concave down at that point? Give a reason for your answer.", selfcheck(r"\text{concave up}"),
             r"At $(1, 2)$: $\frac{d^2y}{dx^2} = (2 - 1)(1 + 1) = 2 > 0$, so the graph is concave up there.", [(1, "concave up with reason")], work="1.6cm"),
        Part("d", r"Is $y = 1$ a solution of the differential equation? Explain.", selfcheck(r"\text{yes}"),
             r"Yes. If $y = 1$, then $\frac{dy}{dx} = 0$ and $x(y - 1) = x \cdot 0 = 0$, so both sides agree for every $x$.", [(1, "yes, with explanation")], work="1.6cm"),
    ], frq_type="Differential equation", figure=FIG),
]

TOPIC = Topic(
    number="7.4", title="Reasoning Using Slope Fields",
    unit="Unit 7: Differential Equations", ced=["FUN-7.C", "FUN-7.C.3"],
    goals=r"Use slope fields to sketch particular solutions, find equilibrium solutions and long-run behavior, and determine concavity from the differential equation.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
