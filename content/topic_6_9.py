"""Topic 6.9: Integrating using substitution.

CED: FUN-6.C (FUN-6.C.1-FUN-6.C.3): substitution reverses the chain rule; choose u as an inside function whose
derivative is a factor (up to a constant), rewrite everything in u, integrate, back-substitute; for definite integrals,
change the limits to u values. Lesson examples: x sqrt(x^2 + 4) (fix a constant), a definite integral with new limits.
Worked examples: e^(3x), (ln x)/x, cos^2 x sin x on [0, pi/2].
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, expr, num, same)

x = sp.symbols("x", positive=True)
C = sp.Symbol("C")


def anti(f):
    F = sp.simplify(sp.integrate(f, x))
    return F.subs(sp.sin(x) / sp.cos(x), sp.tan(x))


def tex(F):
    return sp.latex(F).replace(r"\log{", r"\ln{").replace(r"\operatorname{atan}", r"\arctan")


def plus_c(f, F=None):
    F = F if F is not None else anti(f)
    assert sp.simplify(sp.diff(F, x) - f) == 0, (f, F)
    return expr(F + C, display=tex(F) + " + C")


same("lesson", [sp.integrate(x * (x**2 + 1)**3, (x, 0, 2)), sp.integrate(sp.cos(x)**2 * sp.sin(x), (x, 0, sp.pi / 2))], [78, sp.Rational(1, 3)])

NOTES = [
    Video("s6_9.py::Lesson", "Substitution", 5),

    Section("The chain rule, backward"),
    Text(r"$\frac{d}{dx}\sin\left(x^2\right) = \cos\left(x^2\right) \cdot 2x$, so $\int 2x\cos\left(x^2\right) dx = \sin\left(x^2\right) + C$. "
         r"The clue: an \blank{inside function} whose derivative is a factor of the integrand."),
    Formula("Substitution", (
        r"\textbf{1.} Choose $u$: an inside function. \par \textbf{2.} Find $du = u'(x)\,dx$; if a constant is missing, divide by it. \par "
        r"\textbf{3.} Rewrite the \blank{whole} integral in $u$ (no $x$ left). \par \textbf{4.} Integrate, then put $x$ back.")),
    VideoExample('Fixing a constant', work="3cm"),
    Formula("Definite integrals", (
        r"Change the limits to $u$ values: \[ \int_a^b f\left(g(x)\right)g'(x)\,dx = \int_{\blank{g(a)}}^{g(b)} f(u)\,du, \] "
        r"and don't go back to $x$.")),
    VideoExample('Definite integrals: change the limits', work="3cm"),
    BigIdea(r"Substitution reverses the chain rule: $u$ is an inside function, $du$ is its derivative times $dx$, and everything gets rewritten in $u$."),
    Check(r"Find $\displaystyle\int 3x^2\left(x^3 + 1\right)^4 dx$.", plus_c(3 * x**2 * (x**3 + 1)**4, (x**3 + 1)**5 / 5), r"$u = x^3 + 1$, $du = 3x^2\,dx$: $\frac{u^5}{5} + C$."),
]

# ---------------------------------------------------------------- practice
P = [(2 * x * (x**2 - 3)**5, (x**2 - 3)**6 / 6, "x^2 - 3"), (x**2 * sp.sqrt(x**3 + 2), sp.Rational(2, 9) * (x**3 + 2)**sp.Rational(3, 2), "x^3 + 2"),
     (sp.cos(5 * x), sp.sin(5 * x) / 5, "5x"), (x * sp.exp(x**2), sp.exp(x**2) / 2, "x^2"), (sp.sin(x) * sp.cos(x)**3, -sp.cos(x)**4 / 4, r"\cos x"),
     (x / (x**2 + 1), sp.log(x**2 + 1) / 2, "x^2 + 1"), (sp.sec(x)**2 * sp.tan(x)**2, sp.tan(x)**3 / 3, r"\tan x"), (sp.exp(x) / (1 + sp.exp(x)), sp.log(1 + sp.exp(x)), "1 + e^x"),
     (1 / (x * sp.log(x)), sp.log(sp.log(x)), r"\ln x"), (sp.tan(x), -sp.log(sp.cos(x)), r"\cos x")]
PRACTICE = [Item(rf"Find $\displaystyle\int {sp.latex(f)}\,dx$.", plus_c(f, F), rf"Let $u = {u}$: the result is ${tex(F)} + C$.", work="2.2cm") for f, F, u in P]
PRACTICE += [
    Item(r"Evaluate $\displaystyle\int_0^1 2x\left(x^2 + 1\right)^2 dx$.", num(sp.integrate(2 * x * (x**2 + 1)**2, (x, 0, 1))),
         r"$u = x^2 + 1$ runs from $1$ to $2$: $\int_1^2 u^2\,du = \frac83 - \frac13 = \frac73$.", work="2cm"),
    Item(r"Evaluate $\displaystyle\int_0^{\pi/4} \sec^2 x\,e^{\tan x}\,dx$.", num(sp.E - 1), r"$u = \tan x$ runs from $0$ to $1$: $\int_0^1 e^u\,du = e - 1$.", work="2cm"),
    Item(r"Evaluate $\displaystyle\int_1^{e} \frac{(\ln x)^2}{x}\,dx$.", num(sp.Rational(1, 3)), r"$u = \ln x$ runs from $0$ to $1$: $\int_0^1 u^2\,du = \frac13$.", work="2cm"),
]
same("p def", [sp.integrate(2 * x * (x**2 + 1)**2, (x, 0, 1)), sp.integrate(sp.sec(x)**2 * sp.exp(sp.tan(x)), (x, 0, sp.pi / 4)), sp.integrate(sp.log(x)**2 / x, (x, 1, sp.E))],
     [sp.Rational(7, 3), sp.E - 1, sp.Rational(1, 3)])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(*[Item(rf"Find $\displaystyle\int {sp.latex(f)}\,dx$.", plus_c(f, F), rf"${tex(F)} + C$.", work="1.6cm")
               for f, F in ((sp.exp(4 * x), sp.exp(4 * x) / 4), (sp.sin(3 * x), -sp.cos(3 * x) / 3), ((2 * x + 1)**4, (2 * x + 1)**5 / 10))]),
    Variants(*[Item(rf"Find $\displaystyle\int {sp.latex(f)}\,dx$.", plus_c(f, F), rf"${tex(F)} + C$.", work="1.6cm")
               for f, F in ((x * (x**2 + 5)**3, (x**2 + 5)**4 / 8), (x**2 * sp.cos(x**3), sp.sin(x**3) / 3), (x * sp.sqrt(1 + x**2), (1 + x**2)**sp.Rational(3, 2) / 3))]),
    Variants(*[Item(rf"Find $\displaystyle\int {sp.latex(f)}\,dx$.", plus_c(f, F), rf"${tex(F)} + C$.", work="1.6cm")
               for f, F in ((2 * x / (x**2 + 3), sp.log(x**2 + 3)), (sp.cos(x) / sp.sin(x), sp.log(sp.sin(x))), (sp.exp(2 * x) / (sp.exp(2 * x) + 1), sp.log(sp.exp(2 * x) + 1) / 2))]),
    Variants(*[Item(rf"Evaluate $\displaystyle\int_{{{sp.latex(a)}}}^{{{sp.latex(b)}}} {sp.latex(f)}\,dx$.", num(sp.integrate(f, (x, a, b))), rf"New limits for $u$; the value is ${sp.latex(sp.integrate(f, (x, a, b)))}$.", work="1.8cm")
               for f, a, b in ((x * (x**2 + 1)**3, 0, 1), (sp.cos(x) * sp.sin(x)**2, 0, sp.pi / 2), (x * sp.exp(x**2), 0, 1))]),
    Variants(
        MCQ(r"To find $\int x^3\cos\left(x^4\right) dx$, the best choice is", [r"$u = x^3$", r"$u = x^4$", r"$u = \cos x$", r"$u = \cos\left(x^4\right)$"], "B", r"The inside function, whose derivative $4x^3$ is a factor up to a constant."),
        MCQ(r"To find $\int \frac{e^x}{\left(e^x + 2\right)^2}\,dx$, the best choice is", [r"$u = e^x$", r"$u = \left(e^x + 2\right)^2$", r"$u = e^x + 2$", r"$u = \frac{1}{e^x}$"], "C", r"The inside $e^x + 2$; $du = e^x\,dx$ is in the numerator."),
        MCQ(r"With $u = x^2 + 1$, $\displaystyle\int_0^3 x\sqrt{x^2 + 1}\,dx$ becomes", [r"$\frac12\int_0^3 \sqrt u\,du$", r"$\frac12\int_1^{10} \sqrt u\,du$", r"$2\int_1^{10} \sqrt u\,du$", r"$\int_1^{10} \sqrt u\,du$"], "B",
            r"$x\,dx = \frac12\,du$, and the limits become $u(0) = 1$, $u(3) = 10$.", why_not={"A": "kept the $x$ limits"}),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$\displaystyle\int x^2\left(x^3 - 1\right)^4 dx = $", [r"$\frac{\left(x^3 - 1\right)^5}{15} + C$", r"$\frac{\left(x^3 - 1\right)^5}{5} + C$", r"$\frac{x^3\left(x^3 - 1\right)^5}{15} + C$", r"$3x^2\left(x^3 - 1\right)^5 + C$"], "A",
        r"$u = x^3 - 1$, $x^2\,dx = \frac13\,du$: $\frac13 \cdot \frac{u^5}{5}$.", why_not={"B": "forgot the $\\frac13$"}),
    MCQ(r"$\displaystyle\int_0^{\ln 2} \frac{e^x}{1 + e^x}\,dx = $", [r"$\ln 2$", r"$\ln\frac32$", r"$\frac12$", r"$\ln 3$"], "B", r"$u = 1 + e^x$ runs from $2$ to $3$: $\ln 3 - \ln 2 = \ln\frac32$."),
    MCQ(r"$\displaystyle\int \frac{\cos\sqrt x}{\sqrt x}\,dx = $", [r"$\sin\sqrt x + C$", r"$-2\sin\sqrt x + C$", r"$\frac12\sin\sqrt x + C$", r"$2\sin\sqrt x + C$"], "D", r"$u = \sqrt x$, $du = \frac{1}{2\sqrt x}\,dx$, so $\frac{dx}{\sqrt x} = 2\,du$."),
    MCQ(r"If $\int_1^3 f(x)\,dx = 6$, then $\int_0^1 f(2x + 1)\,dx = $", [r"$6$", r"$12$", r"$3$", r"$2$"], "C", r"$u = 2x + 1$ runs from $1$ to $3$ and $dx = \frac12\,du$: $\frac12(6) = 3$."),
]
same("m", [sp.simplify(sp.diff((x**3 - 1)**5 / 15, x) - x**2 * (x**3 - 1)**4), sp.simplify(sp.integrate(sp.exp(x) / (1 + sp.exp(x)), (x, 0, sp.log(2))) - sp.log(sp.Rational(3, 2))),
           sp.simplify(sp.diff(2 * sp.sin(sp.sqrt(x)), x) - sp.cos(sp.sqrt(x)) / sp.sqrt(x))], [0, 0, 0])

FRQS = []

TOPIC = Topic(
    number="6.9", title="Integrating Using Substitution",
    unit="Unit 6: Integration and Accumulation of Change", ced=["FUN-6.C", "FUN-6.C.1", "FUN-6.C.2", "FUN-6.C.3"],
    goals=r"Find indefinite and definite integrals by substitution, changing the limits of integration for definite integrals.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
