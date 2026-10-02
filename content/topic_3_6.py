"""Topic 3.6: Calculating higher-order derivatives.

CED: FUN-3.F.2 (second and higher derivatives; notation; second derivative of implicitly defined relations). The meaning
(acceleration as the rate of change of velocity) is introduced here; concavity waits for Unit 5. The stacked
position / velocity / acceleration picture matches the video.
"""
import sympy as sp

from calclib import (FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Text, Topic, Variants, Video, expr, num,
                     same, selfcheck)

x, y, t = sp.symbols("x y t")
pi = sp.pi


def D(e, v=x, n=1):
    return sp.simplify(sp.diff(e, v, n))


def imp2(F):
    """y'' for the curve F(x, y) = 0, written with x and y (y' substituted)."""
    yp = -sp.diff(F, x) / sp.diff(F, y)
    Y = sp.Function("Y")(x)
    ypp = sp.diff(yp.subs(y, Y), x).subs(sp.Derivative(Y, x), yp.subs(y, Y)).subs(Y, y)
    return sp.simplify(ypp)


S = t**3 - 6 * t**2 + 9 * t
same("motion", [D(S, t), D(S, t, 2), D(S, t, 2).subs(t, 3)], [3 * t**2 - 12 * t + 9, 6 * t - 12, 6])
same("circle y''", sp.simplify(imp2(x**2 + y**2 - 25).subs(x**2, 25 - y**2)), -25 / y**3)

NOTES = [
    Video("s3_6.py::Lesson", "Higher-order derivatives", 4),

    Section("Derivatives of derivatives"),
    Text(r"The derivative $f'$ is a function, so it has its own derivative. That is the \blank{second derivative}, $f''$. Its derivative is "
         r"$f'''$, the third derivative, and so on."),
    Formula("Notation", (
        r"\[ f''(x) \qquad y'' \qquad \frac{d^2y}{dx^2} \qquad \frac{d^2}{dx^2}\big[f(x)\big] \qquad\qquad f^{(4)}(x) \text{ for the fourth} \]"
        r"$\dfrac{d^2y}{dx^2}$ means \[ \frac{d}{dx}\left(\frac{dy}{dx}\right): \] the rate of change of the \blank{rate of change}.")),

    Section("What the second derivative measures"),
    Text(r"If $s(t)$ is position, then $s'(t) = v(t)$ is velocity, and $s''(t) = v'(t) = a(t)$ is \blank{acceleration}: how fast the velocity "
         r"itself is changing. Its units are distance per time, per time, like meters per second per second."),
    Example("A particle", r"A particle has position $s(t) = t^3 - 6t^2 + 9t$ meters at $t$ seconds. Find its velocity and acceleration at $t = 3$.",
            r"$v(t) = 3t^2 - 12t + 9$, so $v(3) = 0$. $a(t) = 6t - 12$, so $a(3) = 6$ m/s$^2$. The particle is momentarily stopped, but its "
            r"velocity is increasing.", work="2.6cm", beat="Reading t = 3"),

    Section("Second derivatives of implicit curves"),
    Example("The circle", r"For $x^2 + y^2 = 25$, find $\dfrac{d^2y}{dx^2}$ in terms of $x$ and $y$.",
            r"First, $y' = -\dfrac xy$. Quotient rule: \[ y'' = -\frac{y\cdot 1 - x\,y'}{y^2} = -\frac{y + \frac{x^2}{y}}{y^2} = -\frac{y^2 + x^2}{y^3}. \] "
            r"The curve says $x^2 + y^2 = 25$, so $y'' = -\dfrac{25}{y^3}$.", work="3.2cm", beat="Implicit second derivatives"),
    Text(r"Two moves matter: substitute the formula for $y'$ wherever it appears, and use the original \blank{equation} to simplify."),
    BigIdea(r"Differentiate again. For motion, the second derivative is acceleration: the rate of change of velocity."),
    Check(r"Find $\dfrac{d^2y}{dx^2}$ for $y = \sin(3x)$.", expr("-9*sin(3*x)"), r"$y' = 3\cos 3x$ and $y'' = -9\sin 3x$."),
]
same("ex1", D(x**4 - 3 * x**2 + sp.exp(2 * x), n=2), 12 * x**2 - 6 + 4 * sp.exp(2 * x))
same("ex motion", [D(S, t).subs(t, 3), D(S, t, 2).subs(t, 3)], [0, 6])

# ---------------------------------------------------------------- practice
P = [(r"y = 5x^4 - 2x^3 + 7", 5 * x**4 - 2 * x**3 + 7, r"$y' = 20x^3 - 6x^2$, $y'' = 60x^2 - 12x$."),
     (r"y = \sqrt{x}", sp.sqrt(x), r"$y' = \frac12x^{-1/2}$, $y'' = -\frac14x^{-3/2}$."),
     (r"y = e^{-3x}", sp.exp(-3 * x), r"$y' = -3e^{-3x}$, $y'' = 9e^{-3x}$."),
     (r"y = \ln x", sp.log(x), r"$y' = \frac1x$, $y'' = -\frac{1}{x^2}$."),
     (r"y = x\sin x", x * sp.sin(x), r"$y' = \sin x + x\cos x$, $y'' = 2\cos x - x\sin x$."),
     (r"y = \dfrac{1}{x^2}", x**-2, r"$y' = -2x^{-3}$, $y'' = 6x^{-4}$."),
     (r"y = \tan x", sp.tan(x), r"$y' = \sec^2 x$, $y'' = 2\sec^2 x\tan x$."),
     (r"y = xe^{x}", x * sp.exp(x), r"$y' = e^x + xe^x$, $y'' = 2e^x + xe^x$."),
     (r"y = (2x + 1)^5", (2 * x + 1)**5, r"$y' = 10(2x+1)^4$, $y'' = 80(2x+1)^3$."),
     (r"y = \arctan x", sp.atan(x), r"$y' = \frac{1}{1 + x^2}$, $y'' = -\frac{2x}{(1 + x^2)^2}$.")]
PRACTICE = [Item(rf"Find $\dfrac{{d^2y}}{{dx^2}}$ for ${tex}$.", expr(str(D(e, n=2))), sol, work="2cm") for tex, e, sol in P]
PRACTICE += [
    Item(r"Find $f'''(x)$ for $f(x) = x^5 - 4x^3$.", expr("60*x**2 - 24"), r"$f' = 5x^4 - 12x^2$, $f'' = 20x^3 - 24x$, $f''' = 60x^2 - 24$.", work="2cm"),
    Item(r"Find $f^{(4)}(x)$ for $f(x) = \sin x$. What is $f^{(100)}(x)$?", expr("sin(x)"),
         r"$\cos x, -\sin x, -\cos x, \sin x$: the cycle repeats every four derivatives, so $f^{(4)} = \sin x$ and $f^{(100)} = \sin x$.", work="2cm"),
    Item(r"A particle's position is $s(t) = 2t^3 - 9t^2 + 12t$ meters. Find its acceleration at $t = 2$ seconds.", num(6, display=r"6\text{ m/s}^2"),
         r"$v = 6t^2 - 18t + 12$, $a = 12t - 18 = 6$ at $t = 2$.", work="1.8cm"),
    Item(r"For the same particle, at what time is the acceleration zero?", num(sp.Rational(3, 2)), r"$12t - 18 = 0$ gives $t = 1.5$ seconds.", work="1.4cm"),
    Item(r"A ball's height is $h(t) = -16t^2 + 48t + 5$ feet. Find its acceleration and explain its meaning.", num(-32, display=r"-32\text{ ft/s}^2"),
         r"$h'' = -32$: gravity decreases the upward velocity by 32 feet per second, every second.", work="1.8cm"),
    Item(r"For $xy = 4$, find $\dfrac{d^2y}{dx^2}$ in terms of $x$ and $y$.", expr("2*y/x**2"),
         r"$y' = -\dfrac yx$. Quotient rule: $y'' = -\dfrac{xy' - y}{x^2} = -\dfrac{-y - y}{x^2} = \dfrac{2y}{x^2}$.", work="2.6cm"),
    Item(r"For $y^2 = x$, find $\dfrac{d^2y}{dx^2}$ in terms of $y$.", expr("-1/(4*y**3)"),
         r"$y' = \dfrac{1}{2y}$. Then $y'' = -\dfrac{1}{2y^2}y' = -\dfrac{1}{4y^3}$.", work="2.4cm"),
    Item(r"For $x^2 + y^2 = 25$, find $\dfrac{d^2y}{dx^2}$ at $(3, 4)$.", num(sp.Rational(-25, 64)), r"$-\dfrac{25}{y^3} = -\dfrac{25}{64}$.", work="1.4cm"),
    Item(r"$f(x) = e^{kx}$ satisfies $f''(x) = 9f(x)$. Find the positive value of $k$.", num(3), r"$f'' = k^2e^{kx}$, so $k^2 = 9$ and $k = 3$.", work="1.6cm"),
    Item(r"Explain why every polynomial of degree $3$ has $f^{(4)}(x) = 0$.", selfcheck(r"\text{each derivative lowers the degree}"),
         r"Each derivative lowers the degree by one: degree 3, 2, 1, 0 (a constant), and the fourth derivative of a constant is $0$.", work="1.6cm"),
]
k = sp.symbols("k")
same("p", [D(x**5 - 4 * x**3, n=3), D(sp.sin(x), n=4), D(2 * t**3 - 9 * t**2 + 12 * t, t, 2).subs(t, 2), sp.solve(12 * t - 18, t)[0],
           sp.simplify(imp2(x * y - 4) - 2 * y / x**2), sp.simplify(imp2(y**2 - x).subs(x, y**2) + 1 / (4 * y**3)),
           (-25 / y**3).subs(y, 4)],
     [60 * x**2 - 24, sp.sin(x), 6, sp.Rational(3, 2), 0, 0, sp.Rational(-25, 64)])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find $f''(x)$ for $f(x) = 3x^4 - x^2 + 5x$.", expr("36*x**2 - 2"), r"$f' = 12x^3 - 2x + 5$, $f'' = 36x^2 - 2$.", work="1.6cm"),
        Item(r"Find $f''(x)$ for $f(x) = x^3 + \dfrac{1}{x}$.", expr("6*x + 2/x**3"), r"$f' = 3x^2 - x^{-2}$, $f'' = 6x + 2x^{-3}$.", work="1.6cm"),
        Item(r"Find $f''(x)$ for $f(x) = e^{4x} - \cos x$.", expr("16*exp(4*x) + cos(x)"), r"$f' = 4e^{4x} + \sin x$, $f'' = 16e^{4x} + \cos x$.", work="1.6cm"),
    ),
    Variants(
        Item(r"Find $\dfrac{d^2y}{dx^2}$ for $y = x\cos x$.", expr("-2*sin(x) - x*cos(x)"), r"$y' = \cos x - x\sin x$, $y'' = -2\sin x - x\cos x$.", work="1.8cm"),
        Item(r"Find $\dfrac{d^2y}{dx^2}$ for $y = x^2 e^x$.", expr("(x**2 + 4*x + 2)*exp(x)"), r"$y' = (x^2 + 2x)e^x$, $y'' = (x^2 + 4x + 2)e^x$.", work="1.8cm"),
        Item(r"Find $\dfrac{d^2y}{dx^2}$ for $y = \ln\left(x^2\right)$.", expr("-2/x**2"), r"$y = 2\ln x$, $y' = \frac2x$, $y'' = -\frac{2}{x^2}$.", work="1.8cm"),
    ),
    Variants(
        Item(r"A particle's position is $s(t) = t^3 - 3t^2 + 4$ meters. Find its acceleration at $t = 2$ seconds.", num(6),
             r"$v = 3t^2 - 6t$, $a = 6t - 6 = 6$ at $t = 2$.", work="1.6cm"),
        Item(r"A particle's position is $s(t) = 4t^2 - t^3$ meters. Find its acceleration at $t = 1$ second.", num(2),
             r"$v = 8t - 3t^2$, $a = 8 - 6t = 2$ at $t = 1$.", work="1.6cm"),
        Item(r"A particle's position is $s(t) = 2\sin t$ meters. Find its acceleration at $t = \frac\pi2$ seconds.", num(-2),
             r"$v = 2\cos t$, $a = -2\sin t = -2$ at $t = \frac\pi2$.", work="1.6cm"),
    ),
    Variants(
        MCQ(r"For $x^2 + y^2 = 16$, $\dfrac{d^2y}{dx^2} =$", [r"$-\dfrac{x}{y}$", r"$-\dfrac{16}{y^3}$", r"$\dfrac{16}{y^3}$", r"$-\dfrac{1}{y}$"], "B",
            r"$y' = -\frac xy$, then $y'' = -\dfrac{y^2 + x^2}{y^3} = -\dfrac{16}{y^3}$.", why_not={"A": "that's $y'$"}),
        MCQ(r"For $x^2 - y^2 = 1$, $\dfrac{d^2y}{dx^2} =$", [r"$\dfrac{x}{y}$", r"$\dfrac{1}{y^3}$", r"$-\dfrac{1}{y^3}$", r"$\dfrac{y^2 - x^2}{y^2}$"], "C",
            r"$y' = \frac xy$. Then $y'' = \dfrac{y - xy'}{y^2} = \dfrac{y^2 - x^2}{y^3} = -\dfrac{1}{y^3}$.", why_not={"A": "that's $y'$", "B": "sign error"}),
        MCQ(r"For $y^3 = x$, $\dfrac{d^2y}{dx^2} =$", [r"$\dfrac{1}{3y^2}$", r"$-\dfrac{2}{9y^5}$", r"$-\dfrac{2}{3y^3}$", r"$\dfrac{2}{9y^5}$"], "B",
            r"$y' = \dfrac{1}{3y^2}$. Then $y'' = -\dfrac{2}{3y^3}\,y' = -\dfrac{2}{9y^5}$.", why_not={"A": "that's $y'$", "C": "forgot the chain rule factor $y'$"}),
    ),
    Variants(
        MCQ(r"If $s(t)$ is position, then $s''(3) = -4$ means", [r"at $t = 3$ the position is $-4$", r"at $t = 3$ the velocity is decreasing at 4 units per time per time",
            r"the object moves 4 units backward in 3 seconds", r"at $t = 3$ the velocity is $-4$"], "B", r"$s''$ is acceleration: the rate of change of velocity."),
        MCQ(r"Which notation means the second derivative of $y$ with respect to $x$?", [r"$\left(\dfrac{dy}{dx}\right)^2$", r"$\dfrac{dy^2}{dx}$",
            r"$\dfrac{d^2y}{dx^2}$", r"$2\dfrac{dy}{dx}$"], "C", r"$\dfrac{d^2y}{dx^2} = \dfrac{d}{dx}\left(\dfrac{dy}{dx}\right)$.", why_not={"A": "that squares the first derivative"}),
        MCQ(r"If $f(x) = \cos x$, then $f^{(3)}(x) =$", [r"$\sin x$", r"$-\sin x$", r"$\cos x$", r"$-\cos x$"], "A",
            r"$-\sin x$, $-\cos x$, $\sin x$."),
    ),
]
same("q", [sp.simplify(imp2(x**2 - y**2 - 1).subs(x**2, 1 + y**2) + 1 / y**3), sp.simplify(imp2(y**3 - x).subs(x, y**3) + sp.Rational(2, 9) / y**5),
           D(x**2 * sp.exp(x), n=2), D(sp.cos(x), n=3)], [0, 0, (x**2 + 4 * x + 2) * sp.exp(x), sp.sin(x)])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"If $f(x) = x^2\ln x$, then $f''(1) =$", [r"$0$", r"$1$", r"$2$", r"$3$"], "D",
        r"$f' = 2x\ln x + x$, $f'' = 2\ln x + 3 = 3$ at $x = 1$.", why_not={"B": "that's $f'(1)$"}),
    MCQ(r"A particle's velocity is $v(t) = t^2 - 4t + 3$. At the time its acceleration is $0$, its velocity is", [r"$-1$", r"$0$", r"$3$", r"$2$"], "A",
        r"$a = 2t - 4 = 0$ at $t = 2$, and $v(2) = 4 - 8 + 3 = -1$.", why_not={"D": "that's the time"}),
    MCQ(r"If $y = e^{2x} + e^{-2x}$, which is equal to $\dfrac{d^2y}{dx^2}$?", [r"$2y$", r"$4y$", r"$-4y$", r"$y$"], "B",
        r"$y'' = 4e^{2x} + 4e^{-2x} = 4y$."),
    MCQ(r"For $x^3 + y^3 = 2$, $\dfrac{d^2y}{dx^2}$ at $(1, 1)$ is", [r"$-1$", r"$-2$", r"$0$", r"$-4$"], "D",
        r"$y' = -\frac{x^2}{y^2} = -1$. $y'' = -\dfrac{2xy^2 - 2x^2yy'}{y^4} = -\dfrac{2 + 2}{1} = -4$ at $(1, 1)$.", why_not={"A": "that's $y'$"}),
]
same("m", [D(x**2 * sp.log(x), n=2).subs(x, 1), (t**2 - 4 * t + 3).subs(t, 2), sp.simplify(D(sp.exp(2 * x) + sp.exp(-2 * x), n=2) - 4 * (sp.exp(2 * x) + sp.exp(-2 * x))),
           imp2(x**3 + y**3 - 2).subs({x: 1, y: 1})], [3, -1, 0, -4])

FRQS = [
    FRQ("A particle's motion", r"A particle moves along the $x$-axis with position $x(t) = t^3 - 9t^2 + 15t + 2$ for $0 \le t \le 6$, in meters and seconds.", [
        Part("a", r"Find the velocity $v(t)$ and the acceleration $a(t)$. Enter $a(t)$.", expr("6*t - 18", var="t"),
             r"$v(t) = 3t^2 - 18t + 15$, and $a(t) = 6t - 18$.", [(1, "velocity"), (1, "acceleration")], work="2cm"),
        Part("b", r"Find the acceleration at $t = 2$. Is the velocity increasing or decreasing then? Explain.", num(-6),
             r"$a(2) = -6 < 0$, so the velocity is decreasing at $t = 2$.", [(1, "value"), (1, "decreasing, because $a < 0$")], work="1.8cm"),
        Part("c", r"At what times is the particle at rest? Enter the later one.", num(5), r"$3t^2 - 18t + 15 = 3(t - 1)(t - 5) = 0$: $t = 1$ and $t = 5$.",
             [(1, "sets $v = 0$"), (1, "both times")], work="2cm"),
        Part("d", r"Find the velocity at the moment the acceleration is zero.", num(-12), r"$a = 0$ at $t = 3$, and $v(3) = 27 - 54 + 15 = -12$ m/s.",
             [(1, "$t = 3$"), (1, "$v(3) = -12$")], work="1.8cm"),
    ], frq_type="Particle motion"),
]
X = t**3 - 9 * t**2 + 15 * t + 2
same("frq", [D(X, t, 2), D(X, t, 2).subs(t, 2), sorted(sp.solve(D(X, t), t)), D(X, t).subs(t, 3)], [6 * t - 18, -6, [1, 5], -12])

TOPIC = Topic(
    number="3.6", title="Calculating Higher-Order Derivatives",
    unit="Unit 3: Differentiation: Composite, Implicit, and Inverse Functions", ced=["FUN-3.F", "FUN-3.F.2"],
    goals=r"Find second and higher derivatives, including for implicitly defined curves, and interpret acceleration.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
