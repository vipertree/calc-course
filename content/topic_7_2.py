"""Topic 7.2: Verifying solutions for differential equations.

CED: FUN-7.A (FUN-7.A.1, FUN-7.A.2): a function is a solution if substituting it and its derivatives makes the equation
true for every x in the domain; solutions usually form families (y = Ce^{3x} for y' = 3y); a condition picks one.
Lesson example: e^{2x} fails y'' - y = 0. Worked examples: a first-order check, sin 2x for y'' + 4y = 0, finding C.
"""
import sympy as sp

from calclib import (VideoExample, MCQ, BigIdea, Check, Formula, Item, Section, Text, Topic, Variants, Video, num, same, selfcheck)

x, C = sp.symbols("x C")


def residual(lhs):
    """lhs is the equation moved to one side, as a function of a candidate y; returns a function of y to simplify."""
    return lambda y: sp.simplify(lhs(y))


same("lesson", [sp.diff(5 * sp.exp(3 * x), x) - 3 * 5 * sp.exp(3 * x), sp.simplify(sp.diff(sp.exp(2 * x), x, 2) - sp.exp(2 * x)), sp.expand(x * sp.diff(x**2 + 2 * x, x) - (x**2 + 2 * x)),
                sp.diff(sp.sin(2 * x), x, 2) + 4 * sp.sin(2 * x)], [0, 3 * sp.exp(2 * x), x**2, 0])

NOTES = [
    Video("s7_2.py::Lesson", "Verifying solutions", 4),

    Section("The test"),
    Formula("Verifying a solution", (
        r"\textbf{1.} Differentiate the candidate as many times as the equation needs. \par \textbf{2.} Substitute $y$, $y'$, $y''$ into the equation. \par "
        r"\textbf{3.} Simplify. It is a solution exactly when the two sides are equal for \blank{every} $x$ in the domain.")),
    Text(r"$y = Ce^{3x}$ solves $\frac{dy}{dx} = 3y$ for every constant $C$: a \blank{family} of solutions. A condition such as $y(0) = 5$ picks one member ($C = 5$)."),
    VideoExample('One that fails', work="2.2cm"),
    BigIdea(r"To verify a solution: differentiate, substitute, simplify. If both sides agree for every $x$, it's a solution."),
    Check(r"Is $y = 3x + 1$ a solution of $y' = 3$?", selfcheck(r"\text{yes}"), r"$y' = 3$ for every $x$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Is $y = e^{-4x}$ a solution of $y' + 4y = 0$?", selfcheck(r"\text{yes}"), r"$-4e^{-4x} + 4e^{-4x} = 0$.", work="1.4cm"),
    Item(r"Is $y = x^3$ a solution of $xy' = 3y$?", selfcheck(r"\text{yes}"), r"$x(3x^2) = 3x^3 = 3y$.", work="1.4cm"),
    Item(r"Is $y = \cos x$ a solution of $y'' + y = 0$?", selfcheck(r"\text{yes}"), r"$-\cos x + \cos x = 0$.", work="1.4cm"),
    Item(r"Is $y = e^{x}$ a solution of $y'' - 4y = 0$?", selfcheck(r"\text{no}"), r"$e^x - 4e^x = -3e^x \ne 0$.", work="1.4cm"),
    Item(r"Is $y = \frac{1}{x}$ a solution of $y' = -y^2$?", selfcheck(r"\text{yes}"), r"$-\frac{1}{x^2} = -\left(\frac1x\right)^2$.", work="1.4cm"),
    Item(r"For what value of $k$ is $y = e^{kx}$ a solution of $y' = 5y$?", num(5), r"$ke^{kx} = 5e^{kx}$ for every $x$ when $k = 5$.", work="1.2cm"),
    Item(r"For what positive $k$ is $y = \sin(kx)$ a solution of $y'' + 9y = 0$?", num(3), r"$-k^2\sin(kx) + 9\sin(kx) = 0$, so $k^2 = 9$.", work="1.4cm"),
    Item(r"$y = Ce^{2x}$ solves $y' = 2y$. Find $C$ if $y(0) = 7$.", num(7), r"$y(0) = C = 7$.", work="1cm"),
    Item(r"$y = x^2 + C$ solves $y' = 2x$. Find $C$ if $y(3) = 4$.", num(-5), r"$9 + C = 4$.", work="1cm"),
    Item(r"Show that $y = 2e^{x} - x - 1$ is a solution of $y' = x + y$.", selfcheck(r"y' = 2e^x - 1 = x + y"), r"$y' = 2e^x - 1$ and $x + y = x + 2e^x - x - 1 = 2e^x - 1$.", work="1.8cm"),
]
y_ = 2 * sp.exp(x) - x - 1
same("p", [sp.simplify(sp.diff(sp.exp(-4 * x), x) + 4 * sp.exp(-4 * x)), sp.simplify(sp.diff(sp.cos(x), x, 2) + sp.cos(x)), sp.simplify(sp.diff(y_, x) - (x + y_)),
           sp.simplify(sp.diff(1 / x, x) + 1 / x**2)], [0, 0, 0, 0])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"Which is a solution of $y' = -2y$?", [r"$y = e^{2x}$", r"$y = 4e^{-2x}$", r"$y = -2x$", r"$y = x^{-2}$"], "B", r"$y' = -8e^{-2x} = -2y$."),
        MCQ(r"Which is a solution of $y' = 6y$?", [r"$y = 3e^{6x}$", r"$y = 6e^{x}$", r"$y = e^{x/6}$", r"$y = 6x$"], "A", r"$y' = 18e^{6x} = 6y$."),
        MCQ(r"Which is a solution of $y' = \frac{y}{2}$?", [r"$y = e^{2x}$", r"$y = \frac{x^2}{4}$", r"$y = 5e^{x/2}$", r"$y = 2e^{x}$"], "C", r"$y' = \frac52e^{x/2} = \frac y2$."),
    ),
    Variants(
        MCQ(r"Which is a solution of $y'' = -16y$?", [r"$y = e^{4x}$", r"$y = \sin 4x$", r"$y = \sin 16x$", r"$y = x^4$"], "B", r"$y'' = -16\sin 4x$."),
        MCQ(r"Which is a solution of $y'' = 9y$?", [r"$y = e^{3x}$", r"$y = \sin 3x$", r"$y = \cos 3x$", r"$y = 9x^2$"], "A", r"$y'' = 9e^{3x}$."),
        MCQ(r"Which is a solution of $y'' + y = 0$?", [r"$y = e^{-x}$", r"$y = x^2$", r"$y = 2\sin x$", r"$y = e^{x}$"], "C", r"$y'' = -2\sin x = -y$."),
    ),
    Variants(
        Item(r"For what value of $k$ is $y = e^{kx}$ a solution of $y' = -3y$?", num(-3), r"$k = -3$.", work="1cm"),
        Item(r"For what value of $k$ is $y = e^{kx}$ a solution of $y' = \frac12y$?",
             num(sp.Rational(1, 2)), r"$k = \frac12$.", work="1cm"),
        Item(r"For what value of $k$ is $y = e^{kx}$ a solution of $2y' = 10y$?", num(5), r"$2k = 10$.", work="1cm"),
    ),
    Variants(
        Item(r"$y = Ce^{-x}$ solves $y' = -y$. Find $C$ if $y(0) = 4$.", num(4), r"$C = 4$.", work="1cm"),
        Item(r"$y = Ce^{3x}$ solves $y' = 3y$. Find $C$ if $y(1) = e^3$.", num(1), r"$Ce^3 = e^3$.", work="1cm"),
        Item(r"$y = \frac{1}{C - x}$ solves $y' = y^2$. Find $C$ if $y(0) = \frac14$.", num(4), r"$\frac1C = \frac14$.", work="1cm"),
    ),
    Variants(
        Item(r"Is $y = x^2 - 1$ a solution of $y' = 2x$?", selfcheck(r"\text{yes}"), r"$y' = 2x$.", work="1cm"),
        Item(r"Is $y = e^{x^2}$ a solution of $y' = 2xy$?", selfcheck(r"\text{yes}"), r"$y' = 2xe^{x^2} = 2xy$.", work="1cm"),
        Item(r"Is $y = \ln x$ a solution of $xy' = 2$?", selfcheck(r"\text{no}"), r"$x \cdot \frac1x = 1 \ne 2$.", work="1cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"Which function is a solution of $y'' - y' - 2y = 0$?", [r"$y = e^{2x}$", r"$y = e^{x}$", r"$y = e^{-2x}$", r"$y = xe^x$"], "A", r"$4e^{2x} - 2e^{2x} - 2e^{2x} = 0$."),
    MCQ(r"If $y = Ae^{kx}$ is a solution of $y' = 0.4y$ with $y(0) = 50$, then", [r"$A = 0.4$, $k = 50$", r"$A = 50$, $k = 0.4$", r"$A = 50$, $k = -0.4$", r"$A = 20$, $k = 0.4$"], "B", r"$k = 0.4$ from the equation, $A = y(0) = 50$."),
    MCQ(r"Which is NOT a solution of $\frac{dy}{dx} = 2x$?", [r"$y = x^2$", r"$y = x^2 + 3$", r"$y = x^2 - \pi$", r"$y = 2x^2$"], "D", r"$\frac{d}{dx}(2x^2) = 4x$."),
    MCQ(r"$y = \sqrt{x^2 + C}$ solves $y\,y' = x$. If $y(0) = 3$, then $C = $", [r"$3$", r"$\sqrt3$", r"$9$", r"$0$"], "C", r"$\sqrt C = 3$."),
]
same("m", [sp.simplify(sp.diff(sp.exp(2 * x), x, 2) - sp.diff(sp.exp(2 * x), x) - 2 * sp.exp(2 * x)), sp.simplify(sp.sqrt(x**2 + 9) * sp.diff(sp.sqrt(x**2 + 9), x) - x)], [0, 0])

FRQS = []

TOPIC = Topic(
    number="7.2", title="Verifying Solutions for Differential Equations",
    unit="Unit 7: Differential Equations", ced=["FUN-7.A", "FUN-7.A.1", "FUN-7.A.2"],
    goals=r"Verify that a function is a solution of a differential equation by substituting it and its derivatives.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
