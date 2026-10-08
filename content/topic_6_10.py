"""Topic 6.10: Integrating functions using long division and completing the square.

CED: FUN-6.D (FUN-6.D.1, FUN-6.D.2): when the numerator's degree is at least the denominator's, divide first; when the
denominator is an irreducible quadratic, complete the square and use integral du/(a^2 + u^2) = (1/a) arctan(u/a) + C or
integral du/sqrt(a^2 - u^2) = arcsin(u/a) + C. Worked examples: (x^3 + 1)/(x - 1), an arcsine after completing the square,
x/(x + 1) on [0, 1].
"""
import sympy as sp

from calclib import (VideoExample, MCQ, BigIdea, Check, Formula, Item, Section, Text, Topic, Variants, Video, expr, num, same)

x = sp.symbols("x", real=True)
C = sp.Symbol("C")


def tex(F):
    import re
    t = (sp.latex(F).replace(r"\log{", r"\ln{").replace(r"\operatorname{atan}", r"\arctan").replace(r"\operatorname{asin}", r"\arcsin"))
    return re.sub(r"\\ln\{\\left\(\\left\|\{(.+?)\}\\right\| \\right\)\}", r"\\ln|\1|", t)      # ln{(|x - 1|)} -> ln|x - 1|


def plus_c(f, F):
    assert sp.simplify(sp.diff(F, x) - f) == 0 or all(abs(complex(sp.N((sp.diff(F, x) - f).subs(x, v)))) < 1e-9 for v in (sp.Rational(7, 3), sp.Rational(9, 2))), (f, F)
    return expr(F + C, display=tex(F) + " + C")


same("lesson", [sp.div(x**2 + 3 * x + 5, x + 1), sp.div(x**3 + 1, x - 1), sp.integrate(x / (x + 1), (x, 0, 1))], [(x + 2, 3), (x**2 + x + 1, 2), 1 - sp.log(2)])

NOTES = [
    Video("s6_10.py::Lesson", "Long division and completing the square", 5),

    Section("Divide first"),
    Text(r"If the degree of the numerator is at least the degree of the denominator, use long division: \[ \frac{x^2 + 3x + 5}{x + 1} = x + 2 + \frac{3}{x + 1}, \] "
         r"so $\int \frac{x^2 + 3x + 5}{x + 1}\,dx = \frac{x^2}{2} + 2x + \blank{3\ln|x + 1|} + C$."),

    Section("Complete the square"),
    Formula("Two forms", (
        r"\[ \int \frac{du}{a^2 + u^2} = \frac1a\arctan\frac ua + C \qquad \int \frac{du}{\sqrt{a^2 - u^2}} = \blank{\arcsin\frac ua} + C \] "
        r"For a quadratic denominator that won't factor, complete the square to reach one of these forms.")),
    VideoExample('Complete the square', work="2.8cm"),
    BigIdea(r"Top degree at least bottom degree: divide first. Quadratic bottom that won't factor: complete the square, then arctangent or arcsine."),
    Check(r"Find $\displaystyle\int \frac{1}{x^2 + 9}\,dx$.", plus_c(1 / (x**2 + 9), sp.atan(x / 3) / 3), r"$a = 3$: $\frac13\arctan\frac x3 + C$."),
]

# ---------------------------------------------------------------- practice
P = [((x**2 + 2 * x - 1) / (x + 3), x**2 / 2 - x + 2 * sp.log(sp.Abs(x + 3))), ((2 * x + 5) / (x + 1), 2 * x + 3 * sp.log(sp.Abs(x + 1))),
     ((x**3 - 2 * x) / (x - 2), x**3 / 3 + x**2 + 2 * x + 4 * sp.log(sp.Abs(x - 2))), (x**2 / (x**2 + 1), x - sp.atan(x)),
     (1 / (x**2 + 2 * x + 5), sp.atan((x + 1) / 2) / 2), (1 / (x**2 - 6 * x + 10), sp.atan(x - 3)), (1 / sp.sqrt(4 - x**2), sp.asin(x / 2)),
     (1 / sp.sqrt(8 + 2 * x - x**2), sp.asin((x - 1) / 3)), (1 / (4 * x**2 + 1), sp.atan(2 * x) / 2)]
PRACTICE = [Item(rf"Find $\displaystyle\int {sp.latex(f)}\,dx$.", plus_c(f, F), rf"$= {tex(F)} + C$.", work="2.2cm") for f, F in P]
PRACTICE += [
    Item(r"Evaluate $\displaystyle\int_0^1 \frac{x^2}{x + 1}\,dx$.", num(sp.integrate(x**2 / (x + 1), (x, 0, 1))),
         r"$\frac{x^2}{x + 1} = x - 1 + \frac{1}{x + 1}$: $\left[\frac{x^2}{2} - x + \ln|x + 1|\right]_0^1 = -\frac12 + \ln 2$.", work="2.2cm"),
    Item(r"Evaluate $\displaystyle\int_{-1}^{1} \frac{1}{x^2 + 2x + 2}\,dx$.", num(sp.integrate(1 / (x**2 + 2 * x + 2), (x, -1, 1))),
         r"$(x + 1)^2 + 1$: $\left[\arctan(x + 1)\right]_{-1}^{1} = \arctan 2 - 0 = \arctan 2$.", work="2.2cm"),
]
same("p", [sp.integrate(x**2 / (x + 1), (x, 0, 1)), sp.integrate(1 / (x**2 + 2 * x + 2), (x, -1, 1))], [sp.log(2) - sp.Rational(1, 2), sp.atan(2)])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(*[Item(rf"Find $\displaystyle\int {sp.latex(f)}\,dx$.", plus_c(f, F), rf"Divide first: ${tex(F)} + C$.", work="1.8cm")
               for f, F in (((x + 4) / (x + 1), x + 3 * sp.log(sp.Abs(x + 1))), ((x**2 + 1) / (x - 1), x**2 / 2 + x + 2 * sp.log(sp.Abs(x - 1))), ((3 * x - 1) / (x + 2), 3 * x - 7 * sp.log(sp.Abs(x + 2))))]),
    Variants(*[Item(rf"Find $\displaystyle\int {sp.latex(f)}\,dx$.", plus_c(f, F), rf"${tex(F)} + C$.", work="1.6cm")
               for f, F in ((1 / (x**2 + 16), sp.atan(x / 4) / 4), (1 / (x**2 + 25), sp.atan(x / 5) / 5), (1 / sp.sqrt(9 - x**2), sp.asin(x / 3)))]),
    Variants(*[Item(rf"Find $\displaystyle\int {sp.latex(f)}\,dx$.", plus_c(f, F), rf"Complete the square: ${tex(F)} + C$.", work="1.8cm")
               for f, F in ((1 / (x**2 + 4 * x + 5), sp.atan(x + 2)), (1 / (x**2 - 2 * x + 5), sp.atan((x - 1) / 2) / 2), (1 / (x**2 + 6 * x + 13), sp.atan((x + 3) / 2) / 2))]),
    Variants(
        MCQ(r"$x^2 - 8x + 25$ written by completing the square is", [r"$(x - 4)^2 + 9$", r"$(x - 8)^2 + 25$", r"$(x - 4)^2 + 25$", r"$(x + 4)^2 + 9$"], "A", r"$x^2 - 8x + 16 + 9$."),
        MCQ(r"$x^2 + 10x + 34$ written by completing the square is", [r"$(x + 10)^2 + 34$", r"$(x + 5)^2 + 9$", r"$(x - 5)^2 + 9$", r"$(x + 5)^2 + 34$"], "B", r"$x^2 + 10x + 25 + 9$."),
        MCQ(r"$-x^2 + 4x + 5$ written by completing the square is", [r"$5 - (x - 2)^2$", r"$(x - 2)^2 + 9$", r"$9 - (x - 2)^2$", r"$9 - (x + 2)^2$"], "C", r"$-(x^2 - 4x + 4) + 4 + 5$."),
    ),
    Variants(
        Item(r"Evaluate $\displaystyle\int_0^1 \frac{1}{1 + x^2}\,dx$.", num(sp.pi / 4), r"$\arctan 1 - \arctan 0 = \frac\pi4$.", work="1.2cm"),
        Item(r"Evaluate $\displaystyle\int_0^1 \frac{1}{\sqrt{4 - x^2}}\,dx$.", num(sp.pi / 6), r"$\arcsin\frac12 - 0 = \frac\pi6$.", work="1.2cm"),
        Item(r"Evaluate $\displaystyle\int_0^3 \frac{1}{9 + x^2}\,dx$.", num(sp.pi / 12), r"$\frac13\arctan 1 = \frac{\pi}{12}$.", work="1.2cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$\displaystyle\int \frac{x^2 + x}{x + 2}\,dx = $", [r"$\frac{x^2}{2} + \ln|x + 2| + C$", r"$\frac{x^2}{2} - x + 2\ln|x + 2| + C$", r"$\frac{\frac{x^3}{3} + \frac{x^2}{2}}{\frac{x^2}{2} + 2x} + C$",
        r"$x^2 - x + 2\ln|x + 2| + C$"], "B", r"$\frac{x^2 + x}{x + 2} = x - 1 + \frac{2}{x + 2}$."),
    MCQ(r"$\displaystyle\int \frac{dx}{x^2 + 2x + 10} = $", [r"$\arctan(x + 1) + C$", r"$\frac13\arctan(x + 1) + C$", r"$\ln\left|x^2 + 2x + 10\right| + C$", r"$\frac13\arctan\frac{x + 1}{3} + C$"], "D",
        r"$(x + 1)^2 + 9$, $a = 3$."),
    MCQ(r"$\displaystyle\int_0^{3/2} \frac{dx}{\sqrt{9 - x^2}} = $", [r"$\frac\pi6$", r"$\frac\pi3$", r"$\frac{\pi}{2}$", r"$\frac{1}{3}$"], "A", r"$\arcsin\frac12 - \arcsin 0 = \frac\pi6$."),
    MCQ(r"Which integral is best done by long division first?", [r"$\int \frac{1}{x^2 + 4}\,dx$", r"$\int \frac{2x}{x^2 + 4}\,dx$", r"$\int \frac{x^3}{x^2 + 4}\,dx$", r"$\int \frac{1}{\sqrt{4 - x^2}}\,dx$"], "C",
        r"Top degree $3 \ge$ bottom degree $2$."),
]
same("m", [sp.div(x**2 + x, x + 2), sp.integrate(1 / sp.sqrt(9 - x**2), (x, 0, sp.Rational(3, 2)))], [(x - 1, 2), sp.pi / 6])

FRQS = []

TOPIC = Topic(
    number="6.10", title="Integrating Functions Using Long Division and Completing the Square",
    unit="Unit 6: Integration and Accumulation of Change", ced=["FUN-6.D", "FUN-6.D.1", "FUN-6.D.2"],
    goals=r"Rewrite integrands with long division or by completing the square, then integrate with basic rules, arctangent and arcsine.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
