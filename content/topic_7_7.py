"""Topic 7.7: Finding particular solutions using initial conditions and separation of variables.

CED: FUN-7.E (FUN-7.E.1-FUN-7.E.3): an initial condition picks one solution from the family; substitute it right after
integrating to find C, then solve for y, choosing the sign that fits the point; the solution's domain is an interval
containing the initial point on which it is defined. Lesson example: x/y with y(1) = 2. Worked examples: 2xy with
y(0) = 3, a cooling cup, xy^2 with y(0) = 1 (domain).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, check, expr, num, same, selfcheck)

x = sp.symbols("x")


def ok(y, rhs, x0, y0):
    """y solves y' = rhs(x, y) and passes through (x0, y0)."""
    return sp.simplify(sp.diff(y, x) - rhs(x, y)) == 0 and sp.simplify(y.subs(x, x0) - y0) == 0


check("lesson", all([ok(sp.sqrt(x**2 + 3), lambda a, b: a / b, 1, 2), ok(3 * sp.exp(x**2), lambda a, b: 2 * a * b, 0, 3), ok(70 + 120 * sp.exp(-x / 10), lambda a, b: -(b - 70) / 10, 0, 190),
                     ok(2 / (2 - x**2), lambda a, b: a * b**2, 0, 1)]))

NOTES = [
    Video("s7_7.py::Lesson", "Particular solutions", 4),

    Section("Picking one solution"),
    Formula("Particular solution", (
        r"\textbf{1.} Separate and integrate (one $+\,C$). \par \textbf{2.} Substitute the initial condition \blank{right away} to find $C$. \par "
        r"\textbf{3.} Solve for $y$; choose the sign that fits the initial point. \par \textbf{4.} The domain is an interval containing the initial point where the solution is defined.")),
    Text(r"$\frac{dy}{dx} = \frac xy$, $y(1) = 2$: $\frac{y^2}{2} = \frac{x^2}{2} + C$; at $(1, 2)$, $C = \frac32$; $y^2 = x^2 + 3$; $y = \blank{+\sqrt{x^2 + 3}}$ since $y(1) > 0$."),
    VideoExample('Find C right away', work="3cm"),
    BigIdea(r"Separate, integrate, and substitute the initial condition to find $C$ before solving for $y$. Pick the sign that matches the point and watch the domain."),
    Check(r"Find the particular solution of $\frac{dy}{dx} = y$ with $y(0) = 4$.", expr(4 * sp.exp(x)), r"$\ln|y| = x + C$, $C = \ln 4$: $y = 4e^x$."),
]

# ---------------------------------------------------------------- practice
P = [(lambda a, b: 3 * b, r"3y", 0, 5, 5 * sp.exp(3 * x)), (lambda a, b: a * b, r"xy", 0, 2, 2 * sp.exp(x**2 / 2)), (lambda a, b: a**2 / b, r"\frac{x^2}{y}", 0, 3, sp.sqrt(sp.Rational(2, 3) * x**3 + 9)),
     (lambda a, b: -a / b, r"-\frac xy", 0, -4, -sp.sqrt(16 - x**2)), (lambda a, b: b**2, r"y^2", 0, 1, 1 / (1 - x)), (lambda a, b: (b - 10) / 2, r"\frac{y - 10}{2}", 0, 4, 10 - 6 * sp.exp(x / 2)),
     (lambda a, b: sp.cos(a) * b, r"y\cos x", 0, 2, 2 * sp.exp(sp.sin(x))), (lambda a, b: sp.exp(a - b), r"e^{x - y}", 0, 0, sp.log(sp.exp(x)))]
for rhs, t, x0, y0, y in P:
    check(f"p {t}", ok(y, rhs, x0, y0))
PRACTICE = [Item(rf"Find the particular solution of $\dfrac{{dy}}{{dx}} = {t}$ with $y({x0}) = {y0}$.", expr(sp.simplify(y), display=sp.latex(sp.simplify(y))),
                 rf"Separate, integrate, find $C$ at $({x0}, {y0})$: $y = {sp.latex(sp.simplify(y))}$.", work="2.8cm") for _, t, x0, y0, y in P]
PRACTICE += [
    Item(r"The particular solution of $\frac{dy}{dx} = y^2$ with $y(0) = 1$ is $y = \frac{1}{1 - x}$. On what interval is it defined?", selfcheck(r"x < 1"), r"Undefined at $x = 1$; the interval containing $0$ is $(-\infty, 1)$.", work="1.2cm"),
]

# ---------------------------------------------------------------- quiz
QUIZ = [Variants(*[Item(rf"Find the particular solution of $\dfrac{{dy}}{{dx}} = {t}$ with $y({x0}) = {y0}$.", expr(sp.simplify(y), display=sp.latex(sp.simplify(y))), rf"$y = {sp.latex(sp.simplify(y))}$.", work="2.4cm")
                   for _, t, x0, y0, y in P[k:k + 3]]) for k in (0, 3)]
QUIZ += [
    Variants(
        Item(r"$T = 70 + 130e^{-0.2t}$ solves a cooling equation. Find $T(0)$.", num(200), r"$70 + 130 = 200$.", work="1cm"),
        Item(r"$T = 20 + 60e^{-0.1t}$. Find $T(0)$.", num(80), r"$20 + 60 = 80$.", work="1cm"),
        Item(r"$T = 65 + 25e^{-0.3t}$. Find $T(0)$.", num(90), r"$65 + 25 = 90$.", work="1cm"),
    ),
    Variants(
        MCQ(r"After separating and integrating $\frac{dy}{dx} = \frac{x}{y}$, you have $\frac{y^2}{2} = \frac{x^2}{2} + C$. With $y(2) = -1$, $C = $", [r"$-\frac32$", r"$\frac32$", r"$\frac52$", r"$-\frac52$"], "A",
            r"$\frac12 = 2 + C$."),
        MCQ(r"With $y(2) = -1$, the particular solution of $\frac{dy}{dx} = \frac xy$ is", [r"$y = \sqrt{x^2 - 3}$", r"$y = -\sqrt{x^2 - 3}$", r"$y = -\sqrt{x^2 + 3}$", r"$y = x - 3$"], "B", r"$y^2 = x^2 - 3$, negative branch."),
    ),
    Variants(
        MCQ(r"The particular solution of $\frac{dy}{dx} = 2y$ with $y(1) = e^2$ is", [r"$y = e^{2x}$", r"$y = e^2e^{2x}$", r"$y = 2e^{x}$", r"$y = e^{2x} + e^2$"], "A", r"$y = Ae^{2x}$, $Ae^2 = e^2$."),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"If $\frac{dy}{dx} = \frac{y}{x}$ for $x > 0$ and $y(2) = 6$, then $y(5) = $", [r"$9$", r"$15$", r"$30$", r"$12$"], "B", r"$y = Ax$, $A = 3$."),
    MCQ(r"If $\frac{dy}{dt} = 0.5y$ and $y(0) = 40$, then $y(2) = $", [r"$41$", r"$80$", r"$40e$", r"$40e^{2}$"], "C", r"$y = 40e^{0.5t}$, $y(2) = 40e$."),
    MCQ(r"The solution of $\frac{dy}{dx} = -\frac{2x}{y}$ with $y(0) = 3$ is", [r"$y = \sqrt{9 - 2x^2}$", r"$y = \sqrt{9 - x^2}$", r"$y = 3 - x^2$", r"$y = \sqrt{9 + 2x^2}$"], "A", r"$\frac{y^2}{2} = -x^2 + C$, $C = \frac92$: $y^2 = 9 - 2x^2$.", why_not={"B": "dropped the factor $2$"}),
    MCQ(r"$\frac{dy}{dx} = e^{y}x$ with $y(0) = 0$. Then $y = $", [r"$\ln\left(1 + \frac{x^2}{2}\right)$", r"$-\ln\left(1 + \frac{x^2}{2}\right)$", r"$\frac{x^2}{2}$", r"$-\ln\left(1 - \frac{x^2}{2}\right)$"], "D",
        r"$-e^{-y} = \frac{x^2}{2} + C$, $C = -1$: $e^{-y} = 1 - \frac{x^2}{2}$."),
]
check("m", all([ok(3 * x, lambda a, b: b / a, 2, 6), ok(40 * sp.exp(x / 2), lambda a, b: b / 2, 0, 40), ok(sp.sqrt(9 - 2 * x**2), lambda a, b: -2 * a / b, 0, 3),
                ok(-sp.log(1 - x**2 / 2), lambda a, b: sp.exp(b) * a, 0, 0)]))

F = 2 + sp.exp(x**2 / 2 + x)
d2 = lambda a, b: (b - 2) * (1 + (a + 1)**2)
check("frq", ok(F, lambda a, b: (a + 1) * (b - 2), 0, 3))
same("frq vals", [d2(0, 3), 3 + 1 * sp.Rational(2, 10)], [2, sp.Rational(16, 5)])
FRQS = [
    FRQ("A separable differential equation", (r"Consider the differential equation $\dfrac{dy}{dx} = (x + 1)(y - 2)$. Let $y = f(x)$ be the particular solution with $f(0) = 3$."), [
        Part("a", r"Write an equation for the line tangent to the graph of $f$ at $x = 0$. Use the tangent line to approximate $f(0.2)$.", num(sp.Rational(16, 5)),
             r"$\frac{dy}{dx}\Big|_{(0, 3)} = (1)(1) = 1$. The tangent line is $y = 3 + x$, so $f(0.2) \approx 3.2$.", [(1, "tangent line"), (1, "approximation")], work="2.4cm"),
        Part("b", r"Given that $\dfrac{d^2y}{dx^2} = (y - 2)\left(1 + (x + 1)^2\right)$, is the approximation in part (a) an overestimate or an underestimate? Give a reason for your answer.",
             selfcheck(r"\text{underestimate}"), r"At $(0, 3)$, $\frac{d^2y}{dx^2} = (1)(2) = 2 > 0$, so the graph of $f$ is concave up near $x = 0$ and lies above its tangent line: an underestimate.",
             [(1, "underestimate with reason")], work="1.8cm"),
        Part("c", r"Find $y = f(x)$, the particular solution with $f(0) = 3$.", expr(F, display=sp.latex(F)),
             r"$\dfrac{dy}{y - 2} = (x + 1)\,dx$, so $\ln|y - 2| = \dfrac{x^2}{2} + x + C$. At $(0, 3)$: $\ln 1 = 0 + C$, $C = 0$. So $|y - 2| = e^{x^2/2 + x}$, and since $f(0) - 2 > 0$, "
             r"$f(x) = 2 + e^{x^2/2 + x}$.", [(1, "separates variables"), (1, "antiderivatives"), (1, "constant of integration"), (1, "uses the initial condition"), (1, "solves for $y$")], work="4cm"),
    ], frq_type="Differential equation"),
]

TOPIC = Topic(
    number="7.7", title="Finding Particular Solutions Using Initial Conditions and Separation of Variables",
    unit="Unit 7: Differential Equations", ced=["FUN-7.E", "FUN-7.E.1", "FUN-7.E.2", "FUN-7.E.3"],
    goals=r"Find particular solutions of separable differential equations from initial conditions, choosing the right sign and stating the domain.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
