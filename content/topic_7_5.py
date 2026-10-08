"""Topic 7.5 (BC only): Approximating solutions using Euler's method.

CED: FUN-7.D (FUN-7.D.1, FUN-7.D.2): from (x_n, y_n), y_{n+1} = y_n + h * (dy/dx at (x_n, y_n)), x_{n+1} = x_n + h; a table
keeps the steps; concave-up solutions make Euler's method underestimate (tangent lines lie below), concave-down
overestimate. Lesson examples: x + y from (0, 1) with h = 0.5; y - x from (0, 2) with h = 0.25. Worked example: 2x from (1, 3).
"""
import sympy as sp

from calclib import (VideoExample, MCQ, BigIdea, Check, Formula, Item, Section, Table, Text, Topic, Variants, Video, num, same, selfcheck)

R = sp.Rational


def euler(f, x0, y0, h, n):
    """Euler approximation after n steps of size h (exact rationals)."""
    x0, y0, h = sp.nsimplify(x0), sp.nsimplify(y0), sp.nsimplify(h)
    for _ in range(n):
        y0 = y0 + h * f(x0, y0)
        x0 = x0 + h
    return y0


same("lesson", [euler(lambda x, y: x + y, 0, 1, R(1, 2), 2), euler(lambda x, y: y - x, 0, 2, R(1, 4), 2), euler(lambda x, y: 2 * x, 1, 3, R(1, 2), 2)], [R(5, 2), R(49, 16), R(11, 2)])

NOTES = [
    Video("s7_5.py::Lesson", "Euler's method", 4),

    Section("Walking along tangent lines"),
    Formula("Euler's method", (
        r"With step size $h$, from the point $(x_n, y_n)$: \[ y_{n+1} = y_n + h \cdot \blank{\frac{dy}{dx}\Big|_{(x_n, y_n)}}, \qquad x_{n+1} = x_n + h. \] "
        r"Each step follows the tangent line for a distance $h$.")),
    Table(r"$0$ & $1$ & $1$ & $0.5$ \\ $0.5$ & $1.5$ & $2$ & $1$ \\ $1$ & $2.5$ & & ", "cccc", header=r"$x$ & $y$ & slope $x + y$ & $\Delta y = h \cdot$ slope"),
    Text(r"For $\frac{dy}{dx} = x + y$, $y(0) = 1$, $h = 0.5$: $y(1) \approx 2.5$ (the exact value is $2e - 2 \approx 3.437$)."),
    Formula("Over or under", (r"If the solution is concave \blank{up}, its tangent lines lie below it and Euler's method \blank{under}estimates. Concave down: it overestimates. "
                              r"Find the concavity from $\frac{d^2y}{dx^2}$ (Topic 7.4).")),
    VideoExample('Smaller steps', work="2.6cm"),
    BigIdea(r"Euler's method: new $y$ = old $y$ + step size $\times$ slope, repeated. Concavity decides over or under."),
    Check(r"$\frac{dy}{dx} = y$, $y(0) = 1$. One Euler step of size $0.1$ gives $y(0.1) \approx$ ?", num(R(11, 10)), r"$1 + 0.1(1) = 1.1$."),
]

# ---------------------------------------------------------------- practice
P = [(lambda x, y: x * y, "xy", 1, 2, R(1, 2), 2), (lambda x, y: x - y, "x - y", 0, 1, R(1, 2), 2), (lambda x, y: y**2, "y^2", 0, 1, R(1, 10), 2),
     (lambda x, y: 3 * x**2, "3x^2", 0, 1, R(1, 2), 2), (lambda x, y: y - 2 * x, "y - 2x", 0, 3, R(1, 4), 2), (lambda x, y: 1 + y, "1 + y", 1, 0, R(1, 2), 3)]
PRACTICE = [Item(rf"$\dfrac{{dy}}{{dx}} = {t}$, $y({x0}) = {y0}$. Use Euler's method with ${n}$ steps of size ${sp.latex(h)}$ to approximate $y({sp.latex(x0 + n * h)})$.",
                 num(euler(f, x0, y0, h, n)), rf"The result is ${sp.latex(euler(f, x0, y0, h, n))}$.", work="2.4cm") for f, t, x0, y0, h, n in P]
PRACTICE += [
    Item(r"$\frac{dy}{dx} = 3x^2$, $y(0) = 1$. Is the Euler approximation of $y(1)$ with step $0.5$ an overestimate or an underestimate?", selfcheck(r"\text{underestimate}"),
         r"$\frac{d^2y}{dx^2} = 6x \ge 0$: concave up, so Euler underestimates. (Exact $y(1) = 2$; Euler gives $1.375$.)", work="1.6cm"),
    Item(r"$\frac{dy}{dx} = -y$, $y(0) = 4$. Is Euler's method an overestimate or an underestimate for $x > 0$? ($y > 0$.)", selfcheck(r"\text{underestimate}"),
         r"$\frac{d^2y}{dx^2} = -\frac{dy}{dx} = y > 0$: concave up, so it underestimates.", work="1.6cm"),
]
same("p", [euler(lambda x, y: 3 * x**2, 0, 1, R(1, 2), 2)], [R(11, 8)])

# ---------------------------------------------------------------- quiz
def q(f, t, x0, y0, h, n):
    return Item(rf"$\dfrac{{dy}}{{dx}} = {t}$, $y({x0}) = {y0}$. Use ${n}$ Euler steps of size ${sp.latex(h)}$ to approximate $y({sp.latex(x0 + n * h)})$.", num(euler(f, x0, y0, h, n)),
                rf"${sp.latex(euler(f, x0, y0, h, n))}$.", work="2cm")


QUIZ = [
    Variants(q(lambda x, y: y, "y", 0, 2, R(1, 2), 2), q(lambda x, y: 2 * y, "2y", 0, 1, R(1, 4), 2), q(lambda x, y: x + 1, "x + 1", 0, 0, R(1, 2), 2)),
    Variants(q(lambda x, y: x * y, "xy", 0, 1, R(1, 2), 2), q(lambda x, y: x + y, "x + y", 1, 0, R(1, 2), 2), q(lambda x, y: y - x, "y - x", 0, 1, R(1, 2), 2)),
    Variants(
        MCQ(r"If a solution is concave up on the interval, Euler's method", [r"overestimates", r"underestimates", r"is exact", r"cannot be used"], "B", r"Tangent lines lie below a concave-up curve."),
        MCQ(r"If a solution is concave down on the interval, Euler's method", [r"overestimates", r"underestimates", r"is exact", r"cannot be used"], "A", r"Tangent lines lie above a concave-down curve."),
    ),
    Variants(
        Item(r"Euler's method with step $h$ from $(2, 5)$ uses slope $-3$ there. With $h = 0.1$, find the next $y$.", num(R(47, 10)), r"$5 + 0.1(-3) = 4.7$.", work="1cm"),
        Item(r"Euler's method from $(0, 4)$ uses slope $1.5$ there. With $h = 0.2$, find the next $y$.", num(R(43, 10)), r"$4 + 0.2(1.5) = 4.3$.", work="1cm"),
        Item(r"Euler's method from $(1, -2)$ uses slope $4$ there. With $h = 0.25$, find the next $y$.", num(-1), r"$-2 + 0.25(4) = -1$.", work="1cm"),
    ),
    Variants(
        MCQ(r"For $\frac{dy}{dx} = x^2$ with $y(0) = 0$, Euler's method with step $0.5$ gives $y(1) \approx$", [r"$0$", r"$0.125$", r"$0.25$", r"$\frac13$"], "B", r"$0 + 0.5(0) = 0$, then $0 + 0.5(0.25) = 0.125$.",
            why_not={"D": "the exact value"}),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$\frac{dy}{dx} = x + 2y$, $y(0) = 1$. With two Euler steps of size $0.1$, $y(0.2) \approx$", [r"$1.2$", r"$1.44$", r"$1.45$", r"$1.21$"], "C", r"$1 + 0.1(2) = 1.2$; slope at $(0.1, 1.2)$: $2.5$; $1.2 + 0.25 = 1.45$."),
    MCQ(r"$\frac{dy}{dx} = \frac{y}{x}$, $y(1) = 2$. One Euler step of size $0.5$ gives $y(1.5) \approx$", [r"$3$", r"$2.5$", r"$4$", r"$2.75$"], "A", r"$2 + 0.5(2) = 3$."),
    MCQ(r"$\frac{dy}{dx} = 2 - y$, $y(0) = 0$. With two Euler steps of size $0.5$, $y(1) \approx$", [r"$1$", r"$2$", r"$1.25$", r"$1.5$"], "D", r"$0 + 0.5(2) = 1$; $1 + 0.5(1) = 1.5$."),
    MCQ(r"For $\frac{dy}{dx} = y$ and $y(0) = 1$, Euler's method with $n$ steps of size $\frac1n$ gives $y(1) \approx \left(1 + \frac1n\right)^n$. As $n$ grows, this approaches", [r"$1$", r"$2$", r"$e$", r"$\infty$"], "C",
        r"$\lim_{n\to\infty}\left(1 + \frac1n\right)^n = e = y(1)$."),
]
same("m", [euler(lambda x, y: x + 2 * y, 0, 1, R(1, 10), 2), euler(lambda x, y: y / x, 1, 2, R(1, 2), 1), euler(lambda x, y: 2 - y, 0, 0, R(1, 2), 2), euler(lambda x, y: x**2, 0, 0, R(1, 2), 2)],
     [R(29, 20), 3, R(3, 2), R(1, 8)])

FRQS = []

TOPIC = Topic(
    number="7.5", title="Approximating Solutions Using Euler's Method",
    unit="Unit 7: Differential Equations", ced=["FUN-7.D", "FUN-7.D.1", "FUN-7.D.2"],
    goals=r"Approximate values of a solution with Euler's method and decide from concavity whether the approximation is an over- or underestimate.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
