"""Topic 7.6: Finding general solutions using separation of variables.

CED: FUN-7.D (FUN-7.D.1, FUN-7.D.2): separate the variables (y's with dy, x's with dx), integrate both sides with one
constant, solve for y when possible; constants combine (A = +-e^C, K = 2C). Lesson examples: xy, x^2/y. Worked examples:
y cos x, Newton's law of cooling, e^(x - y). Full separable-DE FRQs come in 7.7.
"""
import sympy as sp

from calclib import (VideoExample, MCQ, BigIdea, Check, Formula, Item, Section, Text, Topic, Variants, Video, check, expr, same, selfcheck)

x, A, K = sp.symbols("x A K")


def solves(y, rhs):
    """True if y(x) satisfies y' = rhs(x, y) identically."""
    return sp.simplify(sp.diff(y, x) - rhs(x, y)) == 0


check("lesson", all([solves(A * sp.exp(x**2 / 2), lambda a, b: a * b), solves(sp.sqrt(sp.Rational(2, 3) * x**3 + K), lambda a, b: a**2 / b), solves(A * sp.exp(sp.sin(x)), lambda a, b: b * sp.cos(a)),
                solves(sp.log(sp.exp(x) + K), lambda a, b: sp.exp(a - b))]))

NOTES = [
    Video("s7_6.py::Lesson", "Separation of variables", 4),

    Section("Separate, integrate, solve"),
    Formula("Separation of variables", (
        r"\textbf{1.} Separate: all the $y$'s with $dy$, all the $x$'s with $dx$. \par \textbf{2.} Integrate both sides. \par "
        r"\textbf{3.} Use \blank{one} constant of integration, on the $x$ side. \par \textbf{4.} Solve for $y$ if possible.")),
    Text(r"$\frac{dy}{dx} = xy$: $\frac{dy}{y} = x\,dx$, so $\ln|y| = \frac{x^2}{2} + C$ and $|y| = e^Ce^{x^2/2}$. With $A = \pm e^C$: \[ y = \blank{Ae^{x^2/2}}. \] "
         r"Constants combine: $\pm e^C$ becomes $A$, and $2C$ becomes $K$."),
    VideoExample('Another one', work="2.8cm"),
    BigIdea(r"Separate the variables, integrate both sides with one constant, and solve for $y$: the general solution is a family."),
    Check(r"Find the general solution of $\frac{dy}{dx} = \frac{2x}{y}$.", selfcheck(r"y = \pm\sqrt{2x^2 + K}"), r"$y\,dy = 2x\,dx$, $\frac{y^2}{2} = x^2 + C$, $y = \pm\sqrt{2x^2 + K}$."),
]

# ---------------------------------------------------------------- practice
P = [(lambda a, b: 3 * b, r"3y", A * sp.exp(3 * x), r"y = Ae^{3x}"), (lambda a, b: a**2 * b, r"x^2y", A * sp.exp(x**3 / 3), r"y = Ae^{x^3/3}"),
     (lambda a, b: a / b, r"\frac xy", sp.sqrt(x**2 + K), r"y = \pm\sqrt{x^2 + K}"), (lambda a, b: b / a, r"\frac yx", A * x, r"y = Ax"),
     (lambda a, b: b**2, r"y^2", -1 / (x + K), r"y = -\frac{1}{x + K}"), (lambda a, b: sp.exp(a) * b, r"e^x y", A * sp.exp(sp.exp(x)), r"y = Ae^{e^x}"),
     (lambda a, b: -2 * (b - 5), r"-2(y - 5)", 5 + A * sp.exp(-2 * x), r"y = 5 + Ae^{-2x}"), (lambda a, b: a * sp.exp(-b), r"xe^{-y}", sp.log(x**2 / 2 + K), r"y = \ln\left(\frac{x^2}{2} + K\right)")]
for rhs, t, y, d in P:
    check(f"p {t}", solves(y, rhs))
PRACTICE = [Item(rf"Find the general solution of $\dfrac{{dy}}{{dx}} = {t}$.", selfcheck(d), rf"Separate and integrate: ${d}$.", work="2.6cm") for _, t, _, d in P]

# ---------------------------------------------------------------- quiz
QUIZ = [Variants(*[Item(rf"Find the general solution of $\dfrac{{dy}}{{dx}} = {t}$.", selfcheck(d), rf"${d}$.", work="2.2cm") for _, t, _, d in P[k:k + 3]]) for k in (0, 3)]
QUIZ += [
    Variants(
        MCQ(r"Separating $\frac{dy}{dx} = \frac{x}{y^2}$ gives", [r"$y^2\,dy = x\,dx$", r"$\frac{dy}{y^2} = x\,dx$", r"$dy = \frac{x}{y^2}\,dx$ only", r"$y^2\,dx = x\,dy$"], "A", r"Multiply by $y^2$ and $dx$."),
        MCQ(r"Separating $\frac{dy}{dx} = y\sin x$ gives", [r"$y\,dy = \sin x\,dx$", r"$\frac{dy}{y} = \sin x\,dx$", r"$\frac{dy}{\sin x} = y\,dx$", r"$dy = \sin x\,dx$"], "B", r"Divide by $y$, multiply by $dx$."),
        MCQ(r"Separating $\frac{dy}{dx} = e^{x + y}$ gives", [r"$e^y\,dy = e^x\,dx$", r"$dy = e^x\,dx$", r"$e^{-y}\,dy = e^x\,dx$", r"$e^{x + y}\,dy = dx$"], "C", r"$e^{x + y} = e^xe^y$; divide by $e^y$."),
    ),
    Variants(
        MCQ(r"The general solution of $\frac{dy}{dt} = -0.5y$ is", [r"$y = -0.5t + C$", r"$y = Ae^{-0.5t}$", r"$y = Ae^{0.5t}$", r"$y = e^{-0.5t} + C$"], "B", r"$\ln|y| = -0.5t + C$."),
        MCQ(r"The general solution of $\frac{dy}{dt} = 4y$ is", [r"$y = Ae^{4t}$", r"$y = 4t + C$", r"$y = e^{4t} + C$", r"$y = 2t^2 + C$"], "A", r"$\ln|y| = 4t + C$."),
    ),
    Variants(
        MCQ(r"In $\ln|y| = x^3 + C$, solving for $y$ gives $y = Ae^{x^3}$ where", [r"$A = C$", r"$A = \ln C$", r"$A = \pm e^C$", r"$A = e^{x^3}$"], "C", r"$|y| = e^Ce^{x^3}$."),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"The general solution of $\frac{dy}{dx} = \frac{y}{x^2}$ is", [r"$y = Ae^{-1/x}$", r"$y = Ae^{1/x}$", r"$y = -\frac1x + C$", r"$y = Ax^{-2}$"], "A", r"$\ln|y| = -\frac1x + C$."),
    MCQ(r"Which is the general solution of $\frac{dy}{dx} = 2xy^2$?", [r"$y = x^2 + C$", r"$y = \frac{1}{x^2 + C}$", r"$y = -\frac{1}{x^2 + C}$", r"$y = Ae^{x^2}$"], "C", r"$-\frac1y = x^2 + C$."),
    MCQ(r"The general solution of $\frac{dP}{dt} = 0.2(P - 100)$ is", [r"$P = 100e^{0.2t}$", r"$P = 100 + 0.2t + C$", r"$P = Ae^{0.2t}$", r"$P = 100 + Ae^{0.2t}$"], "D", r"$\ln|P - 100| = 0.2t + C$."),
    MCQ(r"$\frac{dy}{dx} = \frac{\cos x}{y}$. The general solution satisfies", [r"$y^2 = 2\sin x + K$", r"$y = \sin x + C$", r"$y^2 = \cos x + K$", r"$\ln|y| = \sin x + C$"], "A", r"$y\,dy = \cos x\,dx$: $\frac{y^2}{2} = \sin x + C$."),
]
check("m", all([solves(A * sp.exp(-1 / x), lambda a, b: b / a**2), solves(-1 / (x**2 + K), lambda a, b: 2 * a * b**2), solves(100 + A * sp.exp(x / 5), lambda a, b: (b - 100) / 5)]))

FRQS = []

TOPIC = Topic(
    number="7.6", title="Finding General Solutions Using Separation of Variables",
    unit="Unit 7: Differential Equations", ced=["FUN-7.D", "FUN-7.D.1", "FUN-7.D.2"],
    goals=r"Find general solutions of separable differential equations by separating variables and integrating.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
