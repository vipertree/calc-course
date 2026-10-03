"""Topic 6.8: Finding antiderivatives and indefinite integrals: basic rules and notation.

CED: FUN-6.B (FUN-6.B.1-FUN-6.B.3): the indefinite integral is the family of antiderivatives, F(x) + C; basic rules from
reversing derivative rules (powers, constant multiples, sums, e^x, 1/x, the six trig derivatives, arctan and arcsin);
rewrite (powers, split fractions, expand) before integrating; use a point to find C. Worked examples: expand first,
split a fraction, find C. Answers that are antiderivatives are keyed as F + C (the grader accepts any constant but
requires the + C).
"""
import sympy as sp

from calclib import (VideoExample, MCQ, BigIdea, Check, Formula, Item, Section, Table, Text, Topic, Variants, Video, expr, num, same)

x = sp.symbols("x", positive=True)
C = sp.Symbol("C")


def anti(f):
    """An antiderivative of f, with logs of |x| written for 1/x terms (x > 0 here, so sympy's log(x) is shown as ln|x|)."""
    F = sp.integrate(sp.expand(f), x)
    return F.subs(sp.sin(x) / sp.cos(x), sp.tan(x)).subs(1 / sp.cos(x), sp.sec(x))      # the forms students write


def tex(F):
    return sp.latex(F).replace(r"\log{\left(x \right)}", r"\ln|x|").replace(r"\operatorname{atan}", r"\arctan")


def plus_c(f, display=None):
    F = anti(f)
    return expr(F + C, display=display or (tex(F) + " + C"))


same("lesson", [sp.simplify(sp.diff(2 * x**sp.Rational(3, 2) + 4 / x + 2 * sp.sin(x), x) - (3 * sp.sqrt(x) - 4 / x**2 + 2 * sp.cos(x))),
                sp.expand(anti((x**2 + 1)**2)), sp.simplify(anti((x**3 - 2 * x + 5) / x) - (x**3 / 3 - 2 * x + 5 * sp.log(x)))], [0, x**5 / 5 + 2 * x**3 / 3 + x, 0])

NOTES = [
    Video("s6_8.py::Lesson", "Indefinite integrals", 5),

    Section("A family of antiderivatives"),
    Text(r"$x^2$, $x^2 + 1$ and $x^2 - 7$ all have derivative $2x$: adding a constant never changes the derivative."),
    Formula("Indefinite integral", (
        r"\[ \int f(x)\,dx = F(x) + C, \quad \text{where } F'(x) = f(x). \] $C$ is the \blank{constant of integration}. "
        r"A definite integral (with limits) is a \blank{number}; an indefinite integral is a family of functions.")),

    Section("The basic rules"),
    Table(r"$\int x^n\,dx = \dfrac{x^{n+1}}{n + 1} + C$ ($n \ne -1$) & $\int \dfrac1x\,dx = \blank{\ln|x|} + C$ \\ "
          r"$\int k\,f(x)\,dx = k\int f(x)\,dx$ & $\int e^x\,dx = e^x + C$ \\ "
          r"$\int \left[f \pm g\right] dx = \int f\,dx \pm \int g\,dx$ & $\int \dfrac{1}{1 + x^2}\,dx = \arctan x + C$ \\ "
          r"$\int \cos x\,dx = \sin x + C$ & $\int \sin x\,dx = \blank{-\cos x} + C$ \\ "
          r"$\int \sec^2 x\,dx = \tan x + C$ & $\int \csc^2 x\,dx = -\cot x + C$ \\ "
          r"$\int \sec x\tan x\,dx = \sec x + C$ & $\int \csc x\cot x\,dx = -\csc x + C$ \\ "
          r"$\int \dfrac{1}{\sqrt{1 - x^2}}\,dx = \arcsin x + C$ & ", "ll"),
    Text(r"\textbf{Memory tip:} the minus signs belong to the co-functions' derivatives read backward: $\sin$, $\csc^2$ and $\csc\cot$ all pick up a negative."),
    Text(r"\textbf{Rewrite first.} There is no product or quotient rule for integrals. Write roots as powers ($\frac{1}{\sqrt x} = x^{-1/2}$), split a fraction with one term on the bottom, and expand products."),
    VideoExample('Term by term', work="2.6cm"),
    Text(r"\textbf{Finding $C$.} Given $f'$ and one value of $f$, integrate to get $F(x) + C$, then substitute the point to solve for $C$."),
    BigIdea(r"An indefinite integral is an antiderivative plus $C$. Read derivative rules backward, rewrite into powers first, and always add $C$."),
    Check(r"Find $\displaystyle\int \left(4x^3 - 6x\right) dx$.", plus_c(4 * x**3 - 6 * x), r"$x^4 - 3x^2 + C$."),
]

# ---------------------------------------------------------------- practice
P = [5 * x**4 - 3, x**sp.Rational(2, 3), 1 / x**3, 3 / sp.sqrt(x), (x + 2) * (x - 3), (x**2 - 4) / x**2, 2 * sp.cos(x) - 3 * sp.sin(x), sp.sec(x)**2 + sp.exp(x),
     4 / x, 5 / (1 + x**2), sp.sec(x) * sp.tan(x), (sp.sqrt(x) + 1)**2]
PRACTICE = [Item(rf"Find $\displaystyle\int {sp.latex(f) if not f.is_Add else '(' + sp.latex(f) + ')'}\,dx$.", plus_c(f), rf"$= {tex(anti(f))} + C$.", work="1.8cm") for f in P]
PRACTICE += [
    Item(r"$f'(x) = 3x^2 + 2x$ and $f(1) = 5$. Find $f(x)$.", expr(x**3 + x**2 + 3), r"$f(x) = x^3 + x^2 + C$; $5 = 1 + 1 + C$, so $C = 3$.", work="1.8cm"),
    Item(r"$f'(x) = \cos x$ and $f(\pi) = 2$. Find $f(x)$.", expr(sp.sin(x) + 2), r"$f(x) = \sin x + C$; $2 = 0 + C$.", work="1.6cm"),
    Item(r"$f''(x) = 6x$, $f'(0) = 1$ and $f(0) = 4$. Find $f(x)$.", expr(x**3 + x + 4), r"$f'(x) = 3x^2 + 1$, then $f(x) = x^3 + x + 4$.", work="2cm"),
]
same("p ivp", [(x**3 + x**2 + 3).subs(x, 1), (sp.sin(x) + 2).subs(x, sp.pi), sp.diff(x**3 + x + 4, x, 2)], [5, 2, 6 * x])

# ---------------------------------------------------------------- quiz
def q(f):
    return Item(rf"Find $\displaystyle\int {sp.latex(f) if not f.is_Add else '(' + sp.latex(f) + ')'}\,dx$.", plus_c(f), rf"$= {tex(anti(f))} + C$.", work="1.4cm")


QUIZ = [
    Variants(q(6 * x**2 + 1), q(8 * x**3 - 2 * x), q(10 * x**4 + 3)),
    Variants(q(sp.sqrt(x)), q(1 / x**2), q(x**sp.Rational(-1, 3))),
    Variants(q(3 * sp.cos(x)), q(-2 * sp.sin(x)), q(sp.csc(x)**2)),
    Variants(q(2 / x + sp.exp(x)), q((x**2 + 3) / x), q(1 / (1 + x**2))),
    Variants(
        Item(r"$f'(x) = 4x - 1$ and $f(2) = 9$. Find $f(x)$.", expr(2 * x**2 - x + 3), r"$2x^2 - x + C$; $9 = 8 - 2 + C$, $C = 3$.", work="1.4cm"),
        Item(r"$f'(x) = e^x$ and $f(0) = 5$. Find $f(x)$.", expr(sp.exp(x) + 4), r"$e^x + C$; $5 = 1 + C$, $C = 4$.", work="1.4cm"),
        Item(r"$f'(x) = 3\sqrt x$ and $f(4) = 20$. Find $f(x)$.", expr(2 * x**sp.Rational(3, 2) + 4), r"$2x^{3/2} + C$; $20 = 16 + C$, $C = 4$.", work="1.4cm"),
    ),
]
same("q ivp", [(2 * x**2 - x + 3).subs(x, 2), (sp.exp(x) + 4).subs(x, 0), (2 * x**sp.Rational(3, 2) + 4).subs(x, 4)], [9, 5, 20])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$\displaystyle\int \frac{x^2 + 1}{\sqrt x}\,dx = $", [r"$\frac25 x^{5/2} + 2x^{1/2} + C$", r"$\frac{\frac13x^3 + x}{\frac23x^{3/2}} + C$", r"$\frac52 x^{5/2} + \frac12 x^{1/2} + C$", r"$\frac25 x^{5/2} + C$"], "A",
        r"$x^{3/2} + x^{-1/2}$ integrates to $\frac25x^{5/2} + 2x^{1/2} + C$.", why_not={"B": "integrated the top and bottom separately"}),
    MCQ(r"$\displaystyle\int \left(\sec^2 x - \csc x\cot x\right) dx = $", [r"$\tan x - \csc x + C$", r"$\tan x + \csc x + C$", r"$\sec x + \cot x + C$", r"$2\sec x\tan x + C$"], "B",
        r"$\int \csc x\cot x\,dx = -\csc x$, so subtracting it gives $+\csc x$."),
    MCQ(r"If $f'(x) = \frac{1}{x}$ for $x > 0$ and $f(1) = 3$, then $f(e) = $", [r"$3$", r"$e + 2$", r"$\frac1e + 3$", r"$4$"], "D", r"$f(x) = \ln x + 3$, $f(e) = 4$."),
    MCQ(r"Which is an antiderivative of $\frac{3}{1 + x^2}$?", [r"$3\arcsin x$", r"$3\ln\left(1 + x^2\right)$", r"$3\arctan x + 7$", r"$\frac{3x}{x + \frac{x^3}{3}}$"], "C",
        r"$\frac{d}{dx}\arctan x = \frac{1}{1 + x^2}$; any constant can be added."),
]
same("m", [sp.simplify(anti((x**2 + 1) / sp.sqrt(x)) - (sp.Rational(2, 5) * x**sp.Rational(5, 2) + 2 * sp.sqrt(x))), sp.simplify(sp.diff(sp.tan(x) + sp.csc(x), x) - (sp.sec(x)**2 - sp.csc(x) * sp.cot(x)))], [0, 0])

FRQS = []

TOPIC = Topic(
    number="6.8", title="Finding Antiderivatives and Indefinite Integrals: Basic Rules and Notation",
    unit="Unit 6: Integration and Accumulation of Change", ced=["FUN-6.B", "FUN-6.B.1", "FUN-6.B.2", "FUN-6.B.3"],
    goals=r"Find indefinite integrals with the basic rules, rewriting first when needed, and use a known value to find the constant of integration.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
