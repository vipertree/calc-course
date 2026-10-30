"""Topic 6.14 BC: Selecting techniques for antidifferentiation, the BC version. Numbered 6.15 internally so it fits the
site's lesson numbers and file names; the syllabus labels it "6.14 BC" (docs/ab-bc-versions.md).

CED 6.14 (skill 1.C, selecting a procedure) over every antidifferentiation objective: FUN-6.C/FUN-6.D (basic rules,
rewriting, substitution, long division, completing the square) and the BC-only FUN-6.E (integration by parts) and
FUN-6.F (linear partial fractions). A toolkit, not a decision tree (Adder, 1.7), with substitution checked first.
Lesson example: choose a tool for four integrals. Worked examples: two pairs built from the same pieces, x ln x (parts)
against ln x / x (substitution), and 2/(x^2 - 1) (partial fractions) against 2x/(x^2 - 1) (substitution).
The AB version is content/topic_6_14.py.
"""
import sympy as sp

from calclib import (VideoExample, MCQ, BigIdea, Check, Item, Section, Table, Text, Topic, Variants, Video, expr, num, same, selfcheck)

x = sp.symbols("x", real=True)
C = sp.Symbol("C")
L = lambda e: sp.log(sp.Abs(e))


def tex(F):
    import re
    t = (sp.latex(F).replace(r"\log{", r"\ln{").replace(r"\operatorname{atan}", r"\arctan").replace(r"\operatorname{asin}", r"\arcsin"))
    return re.sub(r"\\ln\{\\left\(\\left\|\{(.+?)\}\\right\| \\right\)\}", r"\\ln|\1|", t)


def plus_c(f, F):
    for v in (sp.Rational(37, 7), sp.Rational(53, 9)):
        assert abs(sp.N((sp.diff(F, x) - f).subs(x, v))) < 1e-12, (f, F)
    return expr(F + C, display=tex(F) + " + C")


TOOL = {"sub": "substitution", "basic": "basic rules", "rewrite": "rewrite first", "div": "long division", "square": "complete the square",
        "parts": "integration by parts", "pf": "partial fractions"}

NOTES = [
    Video("s6_15.py::Lesson", "Choosing a technique", 6.8),

    Section("A toolkit, not a flowchart"),
    Table(r"a basic form (power, trig, $e^x$, $\frac1x$) & basic rules \\ "
          r"a product, a power of a sum, or a sum over one term & rewrite first \\ "
          r"an inside function whose derivative is a factor & substitution \\ "
          r"a fraction, top degree $\ge$ bottom degree & long division \\ "
          r"$1$ over a quadratic that won't factor & complete the square \\ "
          r"a product of two kinds of functions, no inside derivative & integration by parts \\ "
          r"a fraction whose bottom factors into different lines & partial fractions", "ll", header=r"Notice & Tool"),
    Text(r"Check for substitution first: it is quick to spot, and it is often faster than parts or partial fractions. The same pieces can need different tools:"
         r"\[ \int x\ln x\,dx \text{ by parts}, \]\[ \int \frac{\ln x}{x}\,dx \text{ by substitution}, \]"
         r"\[ \int \frac{2}{x^2 - 1}\,dx \text{ by partial fractions}, \]\[ \int \frac{2x}{x^2 - 1}\,dx \text{ by substitution}. \]"),
    VideoExample('Choosing the tool', work="3.4cm"),
    BigIdea(r"Check for substitution first, then notice the integrand's other features, choose the tool they call for, and switch tools if the first doesn't work."),
    Check(r"Which tool fits $\int x^2\ln x\,dx$?", selfcheck(r"\text{integration by parts, } u = \ln x,\ dv = x^2\,dx"),
          r"No inside function has its derivative as a factor. It is a product of two kinds of functions, and $\ln x$ gets simpler when differentiated."),
]

# ---------------------------------------------------------------- practice
P = [(x * sp.exp(2 * x), x * sp.exp(2 * x) / 2 - sp.exp(2 * x) / 4, "parts"), (x * sp.exp(x**2), sp.exp(x**2) / 2, "sub"),
     ((x + 5) / ((x - 1) * (x + 2)), 2 * L(x - 1) - L(x + 2), "pf"), (1 / (x**2 + 4 * x + 5), sp.atan(x + 2), "square"),
     (x**2 * sp.log(x), x**3 * sp.log(x) / 3 - x**3 / 9, "parts"), (sp.log(x)**2 / x, sp.log(x)**3 / 3, "sub"),
     (1 / (x**2 - 9), L(x - 3) / 6 - L(x + 3) / 6, "pf"), (2 * x / (x**2 - 9), L(x**2 - 9), "sub"),
     (x * sp.sin(x), sp.sin(x) - x * sp.cos(x), "parts"), ((x**2 + 1) / (x - 1), x**2 / 2 + x + 2 * L(x - 1), "div"),
     (x * sp.cos(x**2), sp.sin(x**2) / 2, "sub"), ((3 * x + 1) / (x**2 + x), L(x) + 2 * L(x + 1), "pf")]
PRACTICE = [Item(rf"Find $\displaystyle\int {sp.latex(f)}\,dx$.", plus_c(f, F), rf"Tool: {TOOL[k]}. ${tex(F)} + C$.", work="2.6cm") for f, F, k in P]


# ---------------------------------------------------------------- quiz
def pick_tool(f, k, letters):
    ch = [TOOL[t] for t in letters]
    return MCQ(rf"Which technique fits $\int {sp.latex(f)}\,dx$ best?", ch, "ABCD"[letters.index(k)], rf"{TOOL[k].capitalize()}.")


def find(f, F, work="1.8cm"):
    return Item(rf"Find $\displaystyle\int {sp.latex(f)}\,dx$.", plus_c(f, F), rf"${tex(F)} + C$.", work=work)


QUIZ = [
    Variants(pick_tool(x * sp.exp(3 * x), "parts", ["sub", "parts", "pf", "square"]), pick_tool(1 / ((x - 2) * (x + 3)), "pf", ["sub", "parts", "pf", "square"]),
             pick_tool(x**2 * sp.exp(x**3), "sub", ["sub", "parts", "pf", "div"])),
    Variants(find(x * sp.exp(-x), -x * sp.exp(-x) - sp.exp(-x)), find(x * sp.cos(x), x * sp.sin(x) + sp.cos(x)), find(sp.log(x), x * sp.log(x) - x)),
    Variants(find(1 / (x * (x + 1)), L(x) - L(x + 1)), find((x + 3) / (x**2 - 1), 2 * L(x - 1) - L(x + 1)), find(4 / (x**2 - 4), L(x - 2) - L(x + 2))),
    Variants(find(x * sp.sqrt(x**2 + 4), (x**2 + 4)**sp.Rational(3, 2) / 3), find(1 / (x**2 + 6 * x + 10), sp.atan(x + 3)), find(x**2 / (x + 1), x**2 / 2 - x + L(x + 1))),
    Variants(
        Item(r"Evaluate $\displaystyle\int_0^1 x e^x\,dx$.", num(1), r"Parts, $u = x$, $dv = e^x\,dx$: $\left[x e^x - e^x\right]_0^1 = 0 - (-1) = 1$.", work="1.6cm"),
        Item(r"Evaluate $\displaystyle\int_0^1 \frac{2}{(x + 1)(x + 2)}\,dx$.", num(2 * sp.log(sp.Rational(4, 3))),
             r"Partial fractions: $\frac{2}{x + 1} - \frac{2}{x + 2}$. $\left[2\ln|x + 1| - 2\ln|x + 2|\right]_0^1 = (2\ln 2 - 2\ln 3) - (0 - 2\ln 2) = 2\ln\frac43$.", work="1.6cm"),
        Item(r"Evaluate $\displaystyle\int_1^e \frac{\ln x}{x}\,dx$.", num(sp.Rational(1, 2)), r"$u = \ln x$ from $0$ to $1$: $\left[\frac{u^2}{2}\right]_0^1 = \frac12$.", work="1.6cm"),
    ),
]
same("q5", [sp.integrate(x * sp.exp(x), (x, 0, 1)), sp.integrate(2 / ((x + 1) * (x + 2)), (x, 0, 1)), sp.integrate(sp.log(x) / x, (x, 1, sp.E))],
     [1, 2 * sp.log(sp.Rational(4, 3)), sp.Rational(1, 2)])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$\displaystyle\int x e^{3x}\,dx = $", [r"$\frac{x}{3}e^{3x} + \frac19 e^{3x} + C$", r"$\frac{x^2}{6}e^{3x} + C$", r"$\frac{x}{3}e^{3x} - \frac19 e^{3x} + C$", r"$3xe^{3x} - 3e^{3x} + C$"], "C",
        r"Parts, $u = x$, $dv = e^{3x}\,dx$: $du = dx$, $v = \frac13e^{3x}$. $\frac x3e^{3x} - \int \frac13e^{3x}\,dx = \frac x3e^{3x} - \frac19e^{3x} + C$.",
        why_not={"A": "sign error: parts subtracts $\\int v\\,du$", "B": "integrated each factor separately"}),
    MCQ(r"$\displaystyle\int \frac{1}{x^2 + 3x + 2}\,dx = $", [r"$\ln|x + 1| - \ln|x + 2| + C$", r"$\ln\left|x^2 + 3x + 2\right| + C$", r"$\ln|x + 2| - \ln|x + 1| + C$", r"$\arctan\left(x + \frac32\right) + C$"], "A",
        r"$\frac{1}{(x + 1)(x + 2)} = \frac{1}{x + 1} - \frac{1}{x + 2}$.", why_not={"B": "that needs $2x + 3$ on top"}),
    MCQ(r"Which integral is best done by integration by parts?", [r"$\int x\cos\left(x^2\right) dx$", r"$\int \cos x\,e^{\sin x}\,dx$", r"$\int \frac{1}{x^2 - 4}\,dx$", r"$\int x\cos x\,dx$"], "D",
        r"In $\int x\cos x\,dx$ no inside function has its derivative as a factor; $u = x$, $dv = \cos x\,dx$. The first two are substitutions and the third is partial fractions."),
    MCQ(r"$\displaystyle\int \frac{2x + 3}{x^2 + 3x}\,dx = $", [r"$\ln|x| - \ln|x + 3| + C$", r"$\ln\left|x^2 + 3x\right| + C$", r"$(2x + 3)\ln\left|x^2 + 3x\right| + C$", r"$\frac{2x + 3}{2x + 3} + C$"], "B",
        r"The top is the derivative of the bottom: $u = x^2 + 3x$. (Partial fractions gives $\ln|x| + \ln|x + 3|$, the same function.)"),
]
same("m1", [sp.simplify(sp.diff(x / 3 * sp.exp(3 * x) - sp.exp(3 * x) / 9, x) - x * sp.exp(3 * x))], [0])
same("m2", [sp.simplify(sp.diff(sp.log(x + 1) - sp.log(x + 2), x) - 1 / (x**2 + 3 * x + 2))], [0])
same("m4", [sp.simplify(sp.diff(sp.log(x**2 + 3 * x), x) - (2 * x + 3) / (x**2 + 3 * x))], [0])

FRQS = []

TOPIC = Topic(
    number="6.15", title="Selecting Techniques for Antidifferentiation",
    unit="Unit 6: Integration and Accumulation of Change", ced=["FUN-6.C", "FUN-6.D", "FUN-6.E", "FUN-6.F", "skill 1.C"],
    goals=r"Choose an appropriate technique (basic rules, rewriting, substitution, long division, completing the square, integration by parts, partial fractions) by noticing the features of an integrand.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
