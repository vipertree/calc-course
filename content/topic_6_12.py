"""Topic 6.12 (BC only): Integrating using linear partial fractions.

CED: FUN-6.F (FUN-6.F.1): a rational function whose denominator factors into distinct linear factors splits into
A/(x - r) + B/(x - s); find A and B by multiplying through and substituting the roots; each piece integrates to a log.
Lesson examples: 1/(x^2 - 1), (x + 7)/(x^2 - x - 6). Worked examples: (5x + 1)/((x - 1)(x + 2)), 1/(x(x - 1)) on [2, 3].
"""
import sympy as sp

from calclib import (VideoExample, MCQ, BigIdea, Check, Formula, Item, Section, Text, Topic, Variants, Video, expr, num, same)

x = sp.symbols("x", real=True)
C = sp.Symbol("C")


def anti(f):
    """Integrate the partial fractions of f, writing ln|.| for each linear factor."""
    out = 0
    for term in sp.Add.make_args(sp.apart(f, x)):
        num_, den = sp.fraction(sp.factor(term))
        if sp.degree(den, x) == 1:
            a = sp.Poly(den, x).LC()
            out += num_ / a * sp.log(sp.Abs(den / a))
        else:
            out += sp.integrate(term, x)
    return out


def tex(F):
    import re
    t = (sp.latex(F).replace(r"\log{", r"\ln{").replace(r"\operatorname{atan}", r"\arctan").replace(r"\operatorname{asin}", r"\arcsin"))
    return re.sub(r"\\ln\{\\left\(\\left\|\{(.+?)\}\\right\| \\right\)\}", r"\\ln|\1|", t)      # ln{(|x - 1|)} -> ln|x - 1|


def plus_c(f):
    F = anti(f)
    for v in (sp.Rational(37, 7), sp.Rational(53, 9)):
        assert abs(sp.N((sp.diff(F, x) - f).subs(x, v))) < 1e-12, (f, F)
    return expr(F + C, display=tex(F) + " + C"), F


same("lesson", [sp.apart(1 / (x**2 - 1)), sp.apart((x + 7) / (x**2 - x - 6)), sp.apart((5 * x + 1) / ((x - 1) * (x + 2)))],
     [1 / (2 * (x - 1)) - 1 / (2 * (x + 1)), 2 / (x - 3) - 1 / (x + 2), 2 / (x - 1) + 3 / (x + 2)])
same("ex2", [sp.simplify(sp.integrate(1 / (x * (x - 1)), (x, 2, 3)) - sp.log(sp.Rational(4, 3)))], [0])

NOTES = [
    Video("s6_12.py::Lesson", "Partial fractions", 4),

    Section("Splitting a fraction"),
    Formula("Linear partial fractions", (
        r"If the denominator factors into distinct linear factors, \[ \frac{p(x)}{(x - r)(x - s)} = \frac{A}{x - r} + \frac{B}{x - s}. \] "
        r"Multiply through by the denominator, then substitute $x = r$ and $x = s$ to find $A$ and $B$. Each piece integrates to a log: "
        r"$\int \frac{A}{x - r}\,dx = \blank{A\ln|x - r|} + C$.")),
    Text(r"If the degree of the top is at least the degree of the bottom, divide first (Topic 6.10)."),
    VideoExample('The method', work="3cm"),
    VideoExample('Using the method', work="3cm"),
    BigIdea(r"Partial fractions runs fraction addition backward: split into $\frac{A}{x - r} + \frac{B}{x - s}$, find $A$ and $B$ at the roots, integrate to logs."),
    Check(r"Find $A$ and $B$: $\dfrac{3}{(x - 1)(x + 2)} = \dfrac{A}{x - 1} + \dfrac{B}{x + 2}$. Enter $A$.", num(1), r"$3 = A(x + 2) + B(x - 1)$: $x = 1$ gives $A = 1$; $x = -2$ gives $B = -1$."),
]

# ---------------------------------------------------------------- practice
P = [2 / ((x - 1) * (x + 1)), 4 / (x**2 - 4), (3 * x + 1) / ((x + 1) * (x - 2)), (x + 4) / (x**2 + x - 2), 1 / (x**2 + 3 * x), (5 * x - 2) / (x**2 - x - 2),
     (2 * x + 3) / (x**2 + 3 * x + 2), 6 / (x**2 - 9)]
PRACTICE = []
for f in P:
    ans, F = plus_c(f)
    PRACTICE.append(Item(rf"Find $\displaystyle\int {sp.latex(f)}\,dx$.", ans, rf"$= {sp.latex(sp.apart(f, x))}$, so the integral is ${tex(F)} + C$.", work="2.6cm"))
PRACTICE += [
    Item(r"Evaluate $\displaystyle\int_3^5 \frac{2}{x^2 - 1}\,dx$.", num(sp.simplify(sp.integrate(2 / (x**2 - 1), (x, 3, 5)))),
         r"$\frac{2}{x^2 - 1} = \frac{1}{x - 1} - \frac{1}{x + 1}$: $\left[\ln\left|\frac{x - 1}{x + 1}\right|\right]_3^5 = \ln\frac23 - \ln\frac12 = \ln\frac43$.", work="2.4cm"),
]
same("p def", [sp.simplify(sp.integrate(2 / (x**2 - 1), (x, 3, 5)) - sp.log(sp.Rational(4, 3)))], [0])

# ---------------------------------------------------------------- quiz
def q(f):
    ans, F = plus_c(f)
    return Item(rf"Find $\displaystyle\int {sp.latex(f)}\,dx$.", ans, rf"$= {sp.latex(sp.apart(f, x))}$: ${tex(F)} + C$.", work="2.2cm")


QUIZ = [
    Variants(q(1 / ((x - 2) * (x - 3))), q(1 / ((x + 1) * (x + 4))), q(2 / ((x - 1) * (x - 3)))),
    Variants(q(x / ((x - 1) * (x + 1))), q((x + 1) / ((x - 2) * (x + 3))), q((2 * x) / ((x - 4) * (x + 4)))),
    Variants(
        Item(r"$\dfrac{5}{(x - 2)(x + 3)} = \dfrac{A}{x - 2} + \dfrac{B}{x + 3}$. Find $A$.", num(1), r"$x = 2$: $5 = 5A$.", work="1.2cm"),
        Item(r"$\dfrac{x + 9}{(x - 1)(x + 3)} = \dfrac{A}{x - 1} + \dfrac{B}{x + 3}$. Find $A$.", num(sp.Rational(5, 2)), r"$x = 1$: $10 = 4A$.", work="1.2cm"),
        Item(r"$\dfrac{7x}{(x + 1)(x - 6)} = \dfrac{A}{x + 1} + \dfrac{B}{x - 6}$. Find $B$.", num(6), r"$x = 6$: $42 = 7B$.", work="1.2cm"),
    ),
    Variants(*[Item(rf"Evaluate $\displaystyle\int_{{{a}}}^{{{b}}} {sp.latex(f)}\,dx$.", num(sp.nsimplify(sp.simplify(sp.integrate(f, (x, a, b))))),
                    rf"Partial fractions, then logs: ${sp.latex(sp.simplify(sp.integrate(f, (x, a, b))))}$.", work="2cm")
               for f, a, b in ((1 / (x * (x + 1)), 1, 2), (1 / (x**2 - 1), 2, 3), (2 / (x * (x + 2)), 1, 2))]),
    Variants(
        MCQ(r"Which integrand calls for linear partial fractions?", [r"$\frac{1}{x^2 + 1}$", r"$\frac{2x}{x^2 + 1}$", r"$\frac{1}{x^2 - 5x + 6}$", r"$\frac{1}{\sqrt{1 - x^2}}$"], "C", r"$x^2 - 5x + 6 = (x - 2)(x - 3)$."),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$\displaystyle\int \frac{dx}{(x - 1)(x + 2)} = $", [r"$\frac13\ln\left|\frac{x - 1}{x + 2}\right| + C$", r"$\ln|(x - 1)(x + 2)| + C$", r"$\frac13\ln\left|\frac{x + 2}{x - 1}\right| + C$",
        r"$\ln|x - 1| - \ln|x + 2| + C$"], "A", r"$\frac{1}{(x - 1)(x + 2)} = \frac{1/3}{x - 1} - \frac{1/3}{x + 2}$."),
    MCQ(r"$\displaystyle\int_0^1 \frac{3}{(x + 1)(x + 4)}\,dx = $", [r"$\ln 2$", r"$\ln\frac85$", r"$\ln\frac{5}{8}$", r"$3\ln\frac85$"], "B",
        r"$\frac{1}{x + 1} - \frac{1}{x + 4}$: $[\ln(x + 1) - \ln(x + 4)]_0^1 = \ln\frac25 - \ln\frac14 = \ln\frac85$."),
    MCQ(r"$\dfrac{4x - 1}{(x - 1)(x + 2)} = \dfrac{A}{x - 1} + \dfrac{B}{x + 2}$. Then $A + B = $", [r"$1$", r"$2$", r"$3$", r"$4$"], "D", r"$A = 1$ (at $x = 1$) and $B = 3$ (at $x = -2$)."),
    MCQ(r"$\displaystyle\int \frac{x^2}{x^2 - 1}\,dx = $", [r"$\ln|x^2 - 1| + C$", r"$x + \frac12\ln\left|\frac{x - 1}{x + 1}\right| + C$", r"$x + \ln\left|\frac{x - 1}{x + 1}\right| + C$",
        r"$\frac{x^3}{3}\ln|x^2 - 1| + C$"], "B", r"Divide: $1 + \frac{1}{x^2 - 1}$, then partial fractions."),
]
same("m", [sp.apart(1 / ((x - 1) * (x + 2))), sp.simplify(sp.integrate(3 / ((x + 1) * (x + 4)), (x, 0, 1)) - sp.log(sp.Rational(8, 5))), sp.apart((4 * x - 1) / ((x - 1) * (x + 2)))],
     [1 / (3 * (x - 1)) - 1 / (3 * (x + 2)), 0, 1 / (x - 1) + 3 / (x + 2)])

FRQS = []

TOPIC = Topic(
    number="6.12", title="Integrating Using Linear Partial Fractions",
    unit="Unit 6: Integration and Accumulation of Change", ced=["FUN-6.F", "FUN-6.F.1"],
    goals=r"Integrate rational functions whose denominators factor into distinct linear factors by splitting them into partial fractions.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
