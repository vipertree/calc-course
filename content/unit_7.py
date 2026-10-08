"""Unit 7 test: Differential Equations. AP format: 12 MCQ (no calculator), 4 MCQ (calculator), 3 FRQ.
Two forms (A and B) for every slot. Covers the AB topics 7.1-7.4 and 7.6-7.8 (the BC-only topics 7.5 and 7.9 are left out).

Choices are built by `pick`, which puts the keyed answer at a planned letter. Every keyed value is checked with sympy.
"""
import sympy as sp

from calclib import FRQ, MCQ, Part, UnitTest, Variants, close, num, same, selfcheck
from calclib.figs import slope_field

x, y, t, C = sp.symbols("x y t C", real=True)
Y = sp.Function("Y")


def pick(stem, right, wrong, letter, solution, why=None, calc=False):
    k = "ABCD".index(letter)
    choices = list(wrong)
    choices.insert(k, right)
    why_not = {}
    if why:
        for text, reason in why.items():
            why_not["ABCD"[choices.index(text)]] = reason
    return MCQ(stem, choices, letter, solution, why_not=why_not, calc=calc)


def solves(sol, rhs, var=x):
    """sol(var) satisfies dy/dvar = rhs(var, y)."""
    return sp.simplify(sp.diff(sol, var) - rhs(var, sol)) == 0


def d2(rhs):
    """d^2y/dx^2 from dy/dx = rhs(x, y), in terms of x and y."""
    f = rhs(x, y)
    return sp.expand(sp.diff(f, x) + sp.diff(f, y) * f)


def check(name, flag):
    if not flag:
        raise SystemExit(f"check failed: {name}")


# ---------------------------------------------------------------- part A: no calculator
check("A1", solves(3 * sp.exp(2 * x), lambda a, b: 2 * b) and sp.simplify(sp.diff(2 * sp.cos(x), x, 2) + 2 * sp.cos(x)) == 0)
same("A4", [(x**2 - y).subs({x: 2, y: 1}), (x * y + 1).subs({x: -1, y: 3})], [3, -2])
same("A5", [d2(lambda a, b: a + b), d2(lambda a, b: a * b)], [1 + x + y, y + x**2 * y])
same("A6", [d2(lambda a, b: b - a**2).subs({x: 1, y: 4}), d2(lambda a, b: 2 * a - b).subs({x: 0, y: -3})], [1, -1])
check("A7", solves(sp.sqrt(x**2 + 5), lambda a, b: a / b) and solves(4 * sp.exp(sp.sin(x)), lambda a, b: b * sp.cos(a)))
check("A8", solves(3 * sp.exp(x**2), lambda a, b: 2 * a * b) and solves(sp.exp(1 - sp.cos(x)), lambda a, b: b * sp.sin(a)))
y9a = 4 * sp.exp(x**3)
y9b = sp.sqrt(2 * sp.exp(x) - 1)
check("A9", solves(y9a, lambda a, b: 3 * a**2 * b) and solves(y9b, lambda a, b: sp.exp(a) / b))
same("A9 values", [y9a.subs(x, 1), y9b.subs(x, sp.log(5)), y9a.subs(x, 0), y9b.subs(x, 0)], [4 * sp.E, 3, 4, 1])
same("A10", [50 * (sp.Rational(200, 50))**sp.Rational(3, 2), 96 * sp.Rational(1, 2)**(sp.Rational(15, 5))], [400, 12])
check("A12", solves(1 / (1 - x), lambda a, b: b**2) and solves(1 / (1 - x**2), lambda a, b: 2 * a * b**2))

A = [
    Variants(
        pick(r"Which function is a solution of the differential equation $\frac{dy}{dx} = 2y$?", r"$y = 3e^{2x}$", [r"$y = 2e^{x}$", r"$y = x^2$", r"$y = e^{2x} + 1$"], "B",
             r"$y' = 6e^{2x} = 2\left(3e^{2x}\right)$.", {r"$y = e^{2x} + 1$": "$y' = 2e^{2x}$ but $2y = 2e^{2x} + 2$"}),
        pick(r"Which function is a solution of the differential equation $y'' + y = 0$?", r"$y = 2\cos x$", [r"$y = e^{x}$", r"$y = \cos x + 1$", r"$y = x^2$"], "A",
             r"$y'' = -2\cos x = -y$.", {r"$y = \cos x + 1$": "$y'' + y = 1$"}),
    ),
    Variants(
        pick(r"The rate of change of a population $P$ with respect to time is proportional to the square root of $P$. Which equation models this?",
             r"$\frac{dP}{dt} = k\sqrt P$", [r"$P = k\sqrt t$", r"$\frac{dP}{dt} = \sqrt{kP}\,t$", r"$\frac{dP}{dt} = k\sqrt t$"], "C", r"Rate $= k \cdot$ (square root of the amount)."),
        pick(r"The temperature $T$ of a cup of coffee changes at a rate proportional to the difference between $T$ and the room temperature of $70$. Which equation models this?",
             r"$\frac{dT}{dt} = k(T - 70)$", [r"$\frac{dT}{dt} = kT - 70t$", r"$T = k(t - 70)$", r"$\frac{dT}{dt} = k(t - 70)$"], "D", r"Rate $= k \cdot$ (difference)."),
    ),
    Variants(
        pick(r"In the slope field for $\frac{dy}{dx} = x(y - 2)$, the segments are horizontal", r"along the $y$-axis and along the line $y = 2$",
             [r"along the $x$-axis only", r"along the line $y = 2$ only", r"along the line $y = x$"], "A", r"$\frac{dy}{dx} = 0$ when $x = 0$ or $y = 2$."),
        pick(r"In the slope field for $\frac{dy}{dx} = y - x$, the segments are horizontal", r"along the line $y = x$",
             [r"along the $x$-axis", r"along the $y$-axis", r"along the line $y = -x$"], "A", r"$\frac{dy}{dx} = 0$ when $y = x$."),
    ),
    Variants(
        pick(r"For $\frac{dy}{dx} = x^2 - y$, the slope of the solution curve through $(2, 1)$ is", r"$3$", [r"$-3$", r"$5$", r"$1$"], "D", r"$4 - 1 = 3$."),
        pick(r"For $\frac{dy}{dx} = xy + 1$, the slope of the solution curve through $(-1, 3)$ is", r"$-2$", [r"$4$", r"$-4$", r"$2$"], "C", r"$(-1)(3) + 1 = -2$."),
    ),
    Variants(
        pick(r"If $\frac{dy}{dx} = x + y$, then $\frac{d^2y}{dx^2} = $", r"$1 + x + y$", [r"$1$", r"$2$", r"$1 + y$"], "D", r"$\frac{d^2y}{dx^2} = 1 + \frac{dy}{dx} = 1 + x + y$.",
             {r"$1$": "treats $y$ as a constant", r"$2$": "uses $\\frac{dy}{dx} = 1$"}),
        pick(r"If $\frac{dy}{dx} = xy$, then $\frac{d^2y}{dx^2} = $", r"$y + x^2y$", [r"$y$", r"$1$", r"$x + y$"], "B", r"Product rule: $y + x\frac{dy}{dx} = y + x \cdot xy$.",
             {r"$y$": "treats $y$ as a constant"}),
    ),
    Variants(
        pick(r"For $\frac{dy}{dx} = y - x^2$, the solution curve through $(1, 4)$ is", r"increasing and concave up", [r"increasing and concave down", r"decreasing and concave up", r"decreasing and concave down"], "A",
             r"$\frac{dy}{dx} = 3 > 0$; $\frac{d^2y}{dx^2} = \frac{dy}{dx} - 2x = 3 - 2 = 1 > 0$."),
        pick(r"For $\frac{dy}{dx} = 2x - y$, the solution curve through $(0, -3)$ is", r"increasing and concave down", [r"increasing and concave up", r"decreasing and concave up", r"decreasing and concave down"], "A",
             r"$\frac{dy}{dx} = 3 > 0$; $\frac{d^2y}{dx^2} = 2 - \frac{dy}{dx} = -1 < 0$."),
    ),
    Variants(
        pick(r"The general solution of $\frac{dy}{dx} = \frac xy$ is", r"$y^2 - x^2 = C$", [r"$y = x + C$", r"$y^2 + x^2 = C$", r"$y = \frac{x^2}{2} + C$"], "C",
             r"$y\,dy = x\,dx$, $\frac{y^2}{2} = \frac{x^2}{2} + C$."),
        pick(r"The general solution of $\frac{dy}{dx} = y\cos x$ is", r"$y = Ce^{\sin x}$", [r"$y = \sin x + C$", r"$y = e^{\sin x} + C$", r"$y = Ce^{\cos x}$"], "D",
             r"$\frac{dy}{y} = \cos x\,dx$, $\ln|y| = \sin x + C$, $y = Ce^{\sin x}$.", {r"$y = e^{\sin x} + C$": "the constant multiplies after exponentiating"}),
    ),
    Variants(
        pick(r"The solution of $\frac{dy}{dx} = 2xy$ with $y(0) = 3$ is", r"$y = 3e^{x^2}$", [r"$y = e^{x^2} + 2$", r"$y = 3e^{2x}$", r"$y = x^2 + 3$"], "B",
             r"$\ln|y| = x^2 + C$, $y = Ae^{x^2}$, $A = 3$.", {r"$y = e^{x^2} + 2$": "adds the constant after exponentiating"}),
        pick(r"The solution of $\frac{dy}{dx} = y\sin x$ with $y(0) = 1$ is", r"$y = e^{1 - \cos x}$", [r"$y = e^{-\cos x}$", r"$y = e^{\cos x - 1}$", r"$y = 1 - \cos x$"], "C",
             r"$\ln|y| = -\cos x + C$; $0 = -1 + C$, so $C = 1$."),
    ),
    Variants(
        pick(r"$y = f(x)$ is the solution of $\frac{dy}{dx} = 3x^2y$ with $f(0) = 4$. Then $f(1) = $", r"$4e$", [r"$e^4$", r"$4 + e$", r"$12$"], "A",
             r"$\ln|y| = x^3 + C$, $y = 4e^{x^3}$, $f(1) = 4e$."),
        pick(r"$y = f(x)$ is the solution of $\frac{dy}{dx} = \frac{e^x}{y}$ with $f(0) = 1$. Then $f(\ln 5) = $", r"$3$", [r"$\sqrt5$", r"$9$", r"$5$"], "D",
             r"$\frac{y^2}{2} = e^x + C$, $C = -\frac12$, so $y^2 = 2e^x - 1$ and $f(\ln 5) = \sqrt9$."),
    ),
    Variants(
        pick(r"$\frac{dy}{dt} = ky$, $y(0) = 50$, and $y(2) = 200$. Then $y(3) = $", r"$400$", [r"$300$", r"$800$", r"$250$"], "D",
             r"$e^{2k} = 4$, so $e^{k} = 2$ and $y(3) = 50 \cdot 8$."),
        pick(r"A substance decays at a rate proportional to the amount present, with half-life $5$ years. From $96$ grams, how much remains after $15$ years?", r"$12$ grams",
             [r"$48$ grams", r"$24$ grams", r"$32$ grams"], "D", r"Three half-lives: $96 \cdot \frac18$."),
    ),
    Variants(
        pick(r"$\frac{dy}{dt} = 0.5(80 - y)$ and $y(0) = 20$. Then $\lim_{t\to\infty} y(t) = $", r"$80$", [r"$20$", r"$40$", r"$\infty$"], "C",
             r"Below $80$ the rate is positive and shrinks to $0$; $y$ approaches the equilibrium $80$."),
        pick(r"$\frac{dT}{dt} = -0.1(T - 68)$ and $T(0) = 200$. Then $\lim_{t\to\infty} T(t) = $", r"$68$", [r"$0$", r"$200$", r"$132$"], "B",
             r"Above $68$ the rate is negative; $T$ falls toward the equilibrium $68$."),
    ),
    Variants(
        pick(r"The solution of $\frac{dy}{dx} = y^2$ with $y(0) = 1$ is $y = \frac{1}{1 - x}$. On what interval is this particular solution defined?", r"$x < 1$",
             [r"all real $x$", r"$x > 1$", r"$x \ne 1$"], "A", r"The solution must be an interval containing $x = 0$ on which it is differentiable."),
        pick(r"The solution of $\frac{dy}{dx} = 2xy^2$ with $y(0) = 1$ is $y = \frac{1}{1 - x^2}$. On what interval is this particular solution defined?", r"$-1 < x < 1$",
             [r"all real $x$", r"$x \ne \pm 1$", r"$x > -1$"], "A", r"The interval must contain $x = 0$ and avoid $x = \pm 1$."),
    ),
]

# ---------------------------------------------------------------- part B: calculator
tb1a = 4 * sp.log(sp.Rational(5, 2)) / sp.log(sp.Rational(5, 4))
tb1b = 3 * sp.log(4) / sp.log(sp.Rational(5, 4))
close("B1", sp.N(tb1a), 16.425, 5e-4)
close("B1b", sp.N(tb1b), 18.638, 5e-4)
TB2a = 20 + 70 * (sp.Rational(40, 70))**sp.Rational(25, 10)
TB2b = 350 + (70 - 350) * (sp.Rational(280 - 120, 280))**2
close("B2", sp.N(TB2a), 37.278, 5e-4)
same("B2b", [TB2b], [sp.Rational(1810, 7)])
close("B2b n", sp.N(TB2b), 258.571, 5e-4)
check("B3", solves(2 * sp.exp(sp.sin(x)), lambda a, b: b * sp.cos(a)) and solves(3 * sp.exp(sp.atan(x)), lambda a, b: b / (1 + a**2)))
close("B3 v", sp.N(2 * sp.exp(sp.sin(1))), 4.640, 5e-4)
close("B3b v", sp.N(3 * sp.exp(sp.atan(2))), 9.077, 5e-4)
close("B4", sp.N(2 + sp.Rational(2, 10) * sp.sqrt(5)), 2.447, 5e-4)
close("B4b", sp.N(3 + sp.Rational(1, 10) * sp.log(5)), 3.161, 5e-4)

B = [
    Variants(
        pick(r"A population grows at a rate proportional to its size. It is $1200$ at $t = 0$ and $1500$ at $t = 4$ years. When does it reach $3000$?", r"$t \approx 16.43$",
             [r"$t \approx 10.00$", r"$t \approx 24.00$", r"$t \approx 12.31$"], "A", r"$e^{4k} = 1.25$; solve $1200e^{kt} = 3000$: $t = \frac{4\ln 2.5}{\ln 1.25} \approx 16.43$.", calc=True),
        pick(r"A drug leaves the body at a rate proportional to the amount present. The amount falls from $100$ mg to $80$ mg in $3$ hours. When is $25$ mg left?", r"$t \approx 18.64$",
             [r"$t \approx 11.25$", r"$t \approx 9.32$", r"$t \approx 15.00$"], "C", r"$e^{3k} = 0.8$; $t = \frac{3\ln 4}{\ln 1.25} \approx 18.64$.", calc=True),
    ),
    Variants(
        pick(r"$\frac{dT}{dt} = k(T - 20)$, $T(0) = 90$, and $T(10) = 60$. Find $T(25)$.", r"$37.28$", [r"$30.00$", r"$15.00$", r"$41.43$"], "B",
             r"$T - 20 = 70e^{kt}$ with $e^{10k} = \frac47$: $T(25) = 20 + 70\left(\frac47\right)^{2.5} \approx 37.28$.", calc=True),
        pick(r"$\frac{dT}{dt} = k(T - 350)$, $T(0) = 70$, and $T(1) = 190$. Find $T(2)$.", r"$258.57$", [r"$310.00$", r"$280.00$", r"$230.00$"], "D",
             r"$T - 350 = -280e^{kt}$ with $e^{k} = \frac{160}{280} = \frac47$: $T(2) = 350 - 280\left(\frac47\right)^2 \approx 258.57$.", {r"$310.00$": "assumes a linear change"}, calc=True),
    ),
    Variants(
        pick(r"$y = f(x)$ is the solution of $\frac{dy}{dx} = y\cos x$ with $f(0) = 2$. Then $f(1) \approx $", r"$4.640$", [r"$3.081$", r"$2.000$", r"$5.437$"], "C",
             r"$f(x) = 2e^{\sin x}$, $f(1) = 2e^{\sin 1} \approx 4.640$.", calc=True),
        pick(r"$y = f(x)$ is the solution of $\frac{dy}{dx} = \frac{y}{1 + x^2}$ with $f(0) = 3$. Then $f(2) \approx $", r"$9.077$", [r"$4.500$", r"$6.000$", r"$22.167$"], "A",
             r"$f(x) = 3e^{\arctan x}$, $f(2) = 3e^{\arctan 2} \approx 9.077$.", calc=True),
    ),
    Variants(
        pick(r"$y = f(x)$ solves $\frac{dy}{dx} = \sqrt{x + y^2}$ with $f(1) = 2$. The tangent line at $x = 1$ gives $f(1.2) \approx $", r"$2.447$", [r"$2.200$", r"$2.894$", r"$2.000$"], "D",
             r"Slope $\sqrt{1 + 4} = \sqrt5$; $f(1.2) \approx 2 + 0.2\sqrt5 \approx 2.447$.", calc=True),
        pick(r"$y = f(x)$ solves $\frac{dy}{dx} = \ln(x + y)$ with $f(2) = 3$. The tangent line at $x = 2$ gives $f(2.1) \approx $", r"$3.161$", [r"$3.100$", r"$3.069$", r"$4.609$"], "B",
             r"Slope $\ln 5$; $f(2.1) \approx 3 + 0.1\ln 5 \approx 3.161$.", calc=True),
    ),
]

# ---------------------------------------------------------------- FRQ 1: slope field and a particular solution
rA = lambda a, b: a * (2 - b)
fA = 2 - 2 * sp.exp((1 - x**2) / 2)
check("F1A", solves(fA, rA))
same("F1A", [fA.subs(x, 1), rA(1, 0), d2(rA).subs({x: 0, y: 1}), sp.factor(d2(rA))], [0, 2, 1, sp.factor((2 - y) * (1 - x**2))])
FIG1A = slope_field("tU7_1a", lambda a, c: a * (2 - c), [-2, -1, 0, 1, 2], [-1, 0, 1, 2, 3], (-2.5, 2.5), (-1.5, 3.5), caption=r"The slope field for $\frac{dy}{dx} = x(2 - y)$.")
F1A = FRQ("A slope field", (r"Consider the differential equation $\dfrac{dy}{dx} = x(2 - y)$. Its slope field is shown. Let $y = f(x)$ be the particular solution with $f(1) = 0$."), [
    Part("a", r"On the slope field, sketch the solution curve that passes through the point $(0, 1)$.", selfcheck(r"\text{a curve through } (0, 1) \text{ that rises on both sides toward } y = 2"),
         r"The curve has a horizontal tangent at $(0, 1)$, rises to the left and to the right toward $y = 2$ without reaching it, and follows the segments.",
         [(1, "solution curve through $(0, 1)$"), (1, "follows the slope field")], work="2.6cm"),
    Part("b", r"Write an equation for the line tangent to the graph of $f$ at $x = 1$, and use it to approximate $f(1.1)$.", selfcheck(r"y = 2(x - 1);\ f(1.1) \approx 0.2"),
         r"Slope $1 \cdot (2 - 0) = 2$, so $y = 2(x - 1)$ and $f(1.1) \approx 0.2$.", [(1, "tangent line"), (1, "approximation")], work="2cm"),
    Part("c", r"Find $\dfrac{d^2y}{dx^2}$ in terms of $x$ and $y$. Is the solution curve through $(0, 1)$ concave up or concave down at that point? Give a reason.",
         selfcheck(r"\frac{d^2y}{dx^2} = (2 - y)(1 - x^2);\ \text{concave up}"),
         r"$\dfrac{d^2y}{dx^2} = (2 - y) + x\left(-\dfrac{dy}{dx}\right) = (2 - y) - x^2(2 - y) = (2 - y)(1 - x^2)$. At $(0, 1)$: $(1)(1) = 1 > 0$, so concave up.",
         [(1, "$\\frac{d^2y}{dx^2}$"), (1, "concave up with reason")], work="2.6cm"),
    Part("d", r"Find $y = f(x)$, the particular solution with $f(1) = 0$.", selfcheck(r"f(x) = 2 - 2e^{(1 - x^2)/2}"),
         r"$\dfrac{dy}{2 - y} = x\,dx$, so $-\ln|2 - y| = \dfrac{x^2}{2} + C$. At $(1, 0)$: $-\ln 2 = \frac12 + C$. "
         r"Then $\ln(2 - y) = \ln 2 + \frac12 - \frac{x^2}{2}$, so $2 - y = 2e^{(1 - x^2)/2}$ and $f(x) = 2 - 2e^{(1 - x^2)/2}$.",
         [(1, "separates variables"), (1, "antiderivatives"), (1, "constant of integration"), (1, "uses the initial condition"), (1, "solves for $y$")], work="4cm"),
], frq_type="Differential equation", figure=FIG1A)
rB = lambda a, b: b * (1 - a)
fB = sp.exp(x - x**2 / 2)
check("F1B", solves(fB, rB))
same("F1B", [fB.subs(x, 2), rB(2, 1), d2(rB).subs({x: 1, y: 3}), sp.factor(d2(rB))], [1, -1, -3, sp.factor(y * ((1 - x)**2 - 1))])
FIG1B = slope_field("tU7_1b", lambda a, c: c * (1 - a), [-1, 0, 1, 2, 3], [-2, -1, 0, 1, 2], (-1.5, 3.5), (-2.5, 2.5), caption=r"The slope field for $\frac{dy}{dx} = y(1 - x)$.")
F1B = FRQ("A slope field", (r"Consider the differential equation $\dfrac{dy}{dx} = y(1 - x)$. Its slope field is shown. Let $y = f(x)$ be the particular solution with $f(2) = 1$."), [
    Part("a", r"On the slope field, sketch the solution curve that passes through the point $(0, 1)$.", selfcheck(r"\text{a curve through } (0, 1) \text{ that peaks at } x = 1 \text{ and falls toward } y = 0"),
         r"The curve rises from $(0, 1)$, has a horizontal tangent at $x = 1$, then falls toward the $x$-axis, following the segments.",
         [(1, "solution curve through $(0, 1)$"), (1, "follows the slope field")], work="2.6cm"),
    Part("b", r"Write an equation for the line tangent to the graph of $f$ at $x = 2$, and use it to approximate $f(2.2)$.", selfcheck(r"y = 1 - (x - 2);\ f(2.2) \approx 0.8"),
         r"Slope $1 \cdot (1 - 2) = -1$, so $y = 1 - (x - 2)$ and $f(2.2) \approx 0.8$.", [(1, "tangent line"), (1, "approximation")], work="2cm"),
    Part("c", r"Find $\dfrac{d^2y}{dx^2}$ in terms of $x$ and $y$. Is the solution curve through $(1, 3)$ concave up or concave down at that point? Give a reason.",
         selfcheck(r"\frac{d^2y}{dx^2} = y\left[(1 - x)^2 - 1\right];\ \text{concave down}"),
         r"$\dfrac{d^2y}{dx^2} = \dfrac{dy}{dx}(1 - x) - y = y(1 - x)^2 - y$. At $(1, 3)$: $3(0) - 3 = -3 < 0$, so concave down.",
         [(1, "$\\frac{d^2y}{dx^2}$"), (1, "concave down with reason")], work="2.6cm"),
    Part("d", r"Find $y = f(x)$, the particular solution with $f(2) = 1$.", selfcheck(r"f(x) = e^{x - x^2/2}"),
         r"$\dfrac{dy}{y} = (1 - x)\,dx$, so $\ln|y| = x - \dfrac{x^2}{2} + C$. At $(2, 1)$: $0 = 2 - 2 + C$, so $C = 0$ and $f(x) = e^{x - x^2/2}$.",
         [(1, "separates variables"), (1, "antiderivatives"), (1, "constant of integration"), (1, "uses the initial condition"), (1, "solves for $y$")], work="4cm"),
], frq_type="Differential equation", figure=FIG1B)

# ---------------------------------------------------------------- FRQ 2: a differential equation in context
HA = 27 + 64 * sp.exp(-t / 4)
check("F2A", sp.simplify(sp.diff(HA, t) + (HA - 27) / 4) == 0)
same("F2A", [HA.subs(t, 0), 91 + 3 * (-sp.Rational(1, 4) * 64), sp.solve(sp.Eq(HA, 43), t)[0]], [91, 43, 4 * sp.log(4)])
F2A = FRQ("Cooling tea", (
    r"At time $t = 0$ a cup of tea is $91^\circ$C, in a room that is $27^\circ$C. The temperature $H(t)$ of the tea, in degrees Celsius, satisfies "
    r"$\dfrac{dH}{dt} = -\dfrac14(H - 27)$, where $t$ is measured in minutes."), [
    Part("a", r"Write an equation for the line tangent to the graph of $H$ at $t = 0$. Use it to approximate the temperature of the tea at $t = 3$.", num(43),
         r"$H'(0) = -\frac14(64) = -16$, so $y = 91 - 16t$ and $H(3) \approx 91 - 48 = 43^\circ$C.", [(1, "tangent line"), (1, "approximation")], work="2cm"),
    Part("b", r"Find $\dfrac{d^2H}{dt^2}$ in terms of $H$. Is the approximation in part (a) an underestimate or an overestimate? Give a reason.", selfcheck(r"\frac{d^2H}{dt^2} = \tfrac{1}{16}(H - 27);\ \text{underestimate}"),
         r"$\dfrac{d^2H}{dt^2} = -\dfrac14\dfrac{dH}{dt} = \dfrac{1}{16}(H - 27) > 0$ while $H > 27$. The graph is concave up, so it lies above its tangent line: underestimate.",
         [(1, "$\\frac{d^2H}{dt^2}$"), (1, "underestimate with reason")], work="2.4cm"),
    Part("c", r"Find $H(t)$, the solution of the differential equation with $H(0) = 91$.", selfcheck(r"H(t) = 27 + 64e^{-t/4}"),
         r"$\dfrac{dH}{H - 27} = -\dfrac14\,dt$, so $\ln|H - 27| = -\dfrac t4 + C$ and $H - 27 = Ae^{-t/4}$. $H(0) = 91$ gives $A = 64$: $H(t) = 27 + 64e^{-t/4}$.",
         [(1, "separates variables"), (1, "antiderivatives"), (1, "uses the initial condition"), (1, "solves for $H$")], work="3.4cm"),
    Part("d", r"At what time is the tea $43^\circ$C?", num(4 * sp.log(4), tol=0.01, display=r"4\ln 4"),
         r"$64e^{-t/4} = 16$, $e^{-t/4} = \frac14$, $t = 4\ln 4 \approx 5.55$ minutes.", [(1, "answer")], work="1.6cm"),
], frq_type="Differential equation")
WB = 300 + 1100 * sp.exp(sp.Rational(1, 25) * t)
check("F2B", sp.simplify(sp.diff(WB, t) - (WB - 300) / 25) == 0)
same("F2B", [WB.subs(t, 0), 1400 + sp.Rational(1, 4) * 44, sp.solve(sp.Eq(WB, 2500), t)[0]], [1400, 1411, 25 * sp.log(2)])
F2B = FRQ("A growing account", (
    r"The balance $W(t)$ of an account, in dollars, satisfies $\dfrac{dW}{dt} = \dfrac{1}{25}(W - 300)$, where $t$ is measured in years. At time $t = 0$ the balance is $W(0) = 1400$."), [
    Part("a", r"Write an equation for the line tangent to the graph of $W$ at $t = 0$. Use it to approximate $W\left(\frac14\right)$.", num(1411),
         r"$W'(0) = \frac{1100}{25} = 44$, so $y = 1400 + 44t$ and $W\left(\frac14\right) \approx 1411$ dollars.", [(1, "tangent line"), (1, "approximation")], work="2cm"),
    Part("b", r"Find $\dfrac{d^2W}{dt^2}$ in terms of $W$. Is the approximation in part (a) an underestimate or an overestimate? Give a reason.",
         selfcheck(r"\frac{d^2W}{dt^2} = \tfrac{1}{625}(W - 300);\ \text{underestimate}"),
         r"$\dfrac{d^2W}{dt^2} = \dfrac{1}{25}\dfrac{dW}{dt} = \dfrac{1}{625}(W - 300) > 0$ for $W > 300$. The graph is concave up, so the tangent line lies below it: underestimate.",
         [(1, "$\\frac{d^2W}{dt^2}$"), (1, "underestimate with reason")], work="2.4cm"),
    Part("c", r"Find $W(t)$, the solution of the differential equation with $W(0) = 1400$.", selfcheck(r"W(t) = 300 + 1100e^{t/25}"),
         r"$\dfrac{dW}{W - 300} = \dfrac{1}{25}\,dt$, so $\ln|W - 300| = \dfrac{t}{25} + C$ and $W - 300 = Ae^{t/25}$. $W(0) = 1400$ gives $A = 1100$.",
         [(1, "separates variables"), (1, "antiderivatives"), (1, "uses the initial condition"), (1, "solves for $W$")], work="3.4cm"),
    Part("d", r"At what time is the balance $2500$ dollars?", num(25 * sp.log(2), tol=0.01, display=r"25\ln 2"),
         r"$1100e^{t/25} = 2200$, $e^{t/25} = 2$, $t = 25\ln 2 \approx 17.33$ years.", [(1, "answer")], work="1.6cm"),
], frq_type="Differential equation")

# ---------------------------------------------------------------- FRQ 3: an exponential model
kA = sp.log(sp.Rational(5, 2)) / 3
PA = 2000 * sp.exp(kA * t)
same("F3A", [sp.simplify(PA.subs(t, 3)), sp.simplify(PA.subs(t, 6))], [5000, 12500])
close("F3A rate", sp.N(kA * 8000), 2443.4, 0.05)
F3A = FRQ("Bacteria", (
    r"A culture of bacteria grows at a rate proportional to the number of bacteria present. There are $2000$ bacteria at time $t = 0$ and $5000$ at $t = 3$ hours. Let $P(t)$ be the number of bacteria at time $t$."), [
    Part("a", r"Write a differential equation satisfied by $P$, and give its general solution.", selfcheck(r"\frac{dP}{dt} = kP;\ P = P_0e^{kt}"),
         r"$\dfrac{dP}{dt} = kP$, so $P = P_0e^{kt}$.", [(1, "differential equation"), (1, "general solution")], work="1.8cm"),
    Part("b", r"Find the value of $k$.", num(kA, tol=1e-3, display=r"\tfrac13\ln\tfrac52"), r"$5000 = 2000e^{3k}$, $e^{3k} = \frac52$, $k = \frac13\ln\frac52 \approx 0.305$.",
         [(1, "uses the data"), (1, "answer")], work="2cm"),
    Part("c", r"How many bacteria are there at $t = 6$?", num(12500), r"$P(6) = 2000\left(e^{3k}\right)^2 = 2000\left(\frac52\right)^2 = 12500$.", [(1, "answer")], work="1.6cm"),
    Part("d", r"At what rate is the number of bacteria increasing when there are $8000$ bacteria? Indicate units of measure.", num(kA * 8000, tol=0.5, display=r"\tfrac{8000}{3}\ln\tfrac52"),
         r"$\dfrac{dP}{dt} = kP = \dfrac{8000}{3}\ln\dfrac52 \approx 2443$ bacteria per hour.", [(1, "uses $kP$"), (1, "answer with units")], work="1.8cm"),
], frq_type="Differential equation")
kB = sp.log(sp.Rational(3, 4)) / 2
AB = 40 * sp.exp(kB * t)
same("F3B", [sp.simplify(AB.subs(t, 2)), sp.simplify(AB.subs(t, 6)), sp.simplify(sp.solve(sp.Eq(AB, 10), t)[0] - 2 * sp.log(4) / sp.log(sp.Rational(4, 3)))], [30, sp.Rational(135, 8), 0])
F3B = FRQ("A medication", (
    r"A medication leaves the bloodstream at a rate proportional to the amount present. A patient has $40$ mg in the bloodstream at time $t = 0$ and $30$ mg at $t = 2$ hours. Let $A(t)$ be the amount at time $t$."), [
    Part("a", r"Write a differential equation satisfied by $A$, and give its general solution.", selfcheck(r"\frac{dA}{dt} = kA;\ A = A_0e^{kt}"),
         r"$\dfrac{dA}{dt} = kA$, so $A = A_0e^{kt}$.", [(1, "differential equation"), (1, "general solution")], work="1.8cm"),
    Part("b", r"Find the value of $k$.", num(kB, tol=1e-3, display=r"\tfrac12\ln\tfrac34"), r"$30 = 40e^{2k}$, $e^{2k} = \frac34$, $k = \frac12\ln\frac34 \approx -0.144$.",
         [(1, "uses the data"), (1, "answer")], work="2cm"),
    Part("c", r"How much medication remains at $t = 6$?", num(sp.Rational(135, 8)), r"$A(6) = 40\left(\frac34\right)^3 = 16.875$ mg.", [(1, "answer")], work="1.6cm"),
    Part("d", r"At what time is $10$ mg left? Give an exact answer.", num(2 * sp.log(4) / sp.log(sp.Rational(4, 3)), tol=0.01, display=r"\tfrac{2\ln 4}{\ln(4/3)}"),
         r"$40\left(\frac34\right)^{t/2} = 10$, $\frac t2\ln\frac34 = \ln\frac14$, $t = \dfrac{2\ln 4}{\ln\frac43} \approx 9.64$ hours.", [(1, "sets up the equation"), (1, "answer")], work="2cm"),
], frq_type="Differential equation")

TEST = UnitTest(unit=7, title="Differential Equations", mcq_a=A, mcq_b=B,
                frq=[Variants(F1A, F1B), Variants(F2A, F2B), Variants(F3A, F3B)])
