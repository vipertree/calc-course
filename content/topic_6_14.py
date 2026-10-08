"""Topic 6.14: Selecting techniques for antidifferentiation.

CED: FUN-6.D/FUN-6.E/FUN-6.F (selection): choose among basic rules, rewriting, substitution, long division, completing
the square, and (BC) integration by parts and partial fractions, by noticing the integrand's features: a toolkit, not a
decision tree (Adder, 1.7). Lesson example: choose a tool for four integrals. Worked examples: three integrals from the
same pieces needing substitution, completing the square, and long division.
"""
import sympy as sp

from calclib import (VideoExample, MCQ, BigIdea, Check, Formula, Item, Section, Table, Text, Topic, Variants, Video, expr, num, same, selfcheck)

x = sp.symbols("x", real=True)
C = sp.Symbol("C")


def tex(F):
    import re
    t = (sp.latex(F).replace(r"\log{", r"\ln{").replace(r"\operatorname{atan}", r"\arctan").replace(r"\operatorname{asin}", r"\arcsin"))
    return re.sub(r"\\ln\{\\left\(\\left\|\{(.+?)\}\\right\| \\right\)\}", r"\\ln|\1|", t)


def plus_c(f, F):
    for v in (sp.Rational(37, 7), sp.Rational(53, 9)):
        assert abs(sp.N((sp.diff(F, x) - f).subs(x, v))) < 1e-12, (f, F)
    return expr(F + C, display=tex(F) + " + C")


TOOL = {"sub": "substitution", "basic": "basic rules", "rewrite": "rewrite first", "div": "long division", "square": "complete the square", "parts": "integration by parts (BC)",
        "pf": "partial fractions (BC)"}

NOTES = [
    Video("s6_14.py::Lesson", "Choosing a technique", 4),

    Section("A toolkit, not a flowchart"),
    Table(r"a basic form (power, trig, $e^x$, $\frac1x$) & basic rules \\ "
          r"a product, a power of a sum, or a sum over one term & \blank{rewrite first} \\ "
          r"an inside function whose derivative is a factor & \blank{substitution} \\ "
          r"a fraction, top degree $\ge$ bottom degree & long division \\ "
          r"$1$ over a quadratic that won't factor & \blank{complete the square} \\ "
          r"a product of two different kinds of functions & integration by parts (BC) \\ "
          r"a fraction whose bottom factors into lines & partial fractions (BC)", "ll", header=r"Notice & Tool"),
    Text(r"Look at the features, pick the tool, and try another if it fails. The same pieces can need different tools: $\int \frac{x + 1}{x^2 + 2x + 5}\,dx$ (substitution), "
         r"$\int \frac{1}{x^2 + 2x + 5}\,dx$ (complete the square), $\int \frac{x^2 + 2x + 5}{x + 1}\,dx$ (long division)."),
    VideoExample('Choosing the tool', work="3cm"),
    BigIdea(r"Notice the integrand's features, choose the tool they call for, and switch tools if the first doesn't work."),
    Check(r"Which tool fits $\int x^2 e^{x^3}\,dx$?", selfcheck(r"\text{substitution, } u = x^3"), r"$x^3$ is inside and $3x^2$, its derivative, is a factor up to a constant."),
]

# ---------------------------------------------------------------- practice
P = [((x + 1) / (x**2 + 2 * x + 5), sp.log(x**2 + 2 * x + 5) / 2, "sub"), (1 / (x**2 + 2 * x + 5), sp.atan((x + 1) / 2) / 2, "square"),
     ((x**2 + 2 * x + 5) / (x + 1), x**2 / 2 + x + 4 * sp.log(sp.Abs(x + 1)), "div"), ((3 * x - 2)**2, (3 * x - 2)**3 / 9, "sub"), (sp.cos(x) * sp.exp(sp.sin(x)), sp.exp(sp.sin(x)), "sub"),
     ((x**3 + 2 * x) / x**2, x**2 / 2 + 2 * sp.log(sp.Abs(x)), "rewrite"), (1 / sp.sqrt(9 - x**2), sp.asin(x / 3), "basic"), (sp.sec(x)**2 / sp.tan(x), sp.log(sp.Abs(sp.tan(x))), "sub"),
     (x**2 / (x + 2), x**2 / 2 - 2 * x + 4 * sp.log(sp.Abs(x + 2)), "div"), (1 / (x**2 - 4 * x + 8), sp.atan((x - 2) / 2) / 2, "square")]
PRACTICE = [Item(rf"Find $\displaystyle\int {sp.latex(f)}\,dx$.", plus_c(f, F), rf"Tool: {TOOL[k]}. ${tex(F)} + C$.", work="2.4cm") for f, F, k in P]

# ---------------------------------------------------------------- quiz
def pick_tool(f, k, letters):
    ch = [TOOL[t] for t in letters]
    return MCQ(rf"Which technique fits $\int {sp.latex(f)}\,dx$ best?", ch, "ABCD"[letters.index(k)], rf"{TOOL[k].capitalize()}.")


QUIZ = [
    Variants(pick_tool(x * sp.sqrt(x**2 + 1), "sub", ["sub", "div", "square", "basic"]), pick_tool((x**2 + 1) / (x - 1), "div", ["sub", "div", "square", "rewrite"]),
             pick_tool(1 / (x**2 + 4 * x + 8), "square", ["sub", "div", "square", "rewrite"])),
    Variants(*[Item(rf"Find $\displaystyle\int {sp.latex(f)}\,dx$.", plus_c(f, F), rf"${tex(F)} + C$.", work="1.8cm") for f, F, _ in P[:3]]),
    Variants(*[Item(rf"Find $\displaystyle\int {sp.latex(f)}\,dx$.", plus_c(f, F), rf"${tex(F)} + C$.", work="1.8cm") for f, F, _ in P[3:6]]),
    Variants(*[Item(rf"Find $\displaystyle\int {sp.latex(f)}\,dx$.", plus_c(f, F), rf"${tex(F)} + C$.", work="1.8cm") for f, F, _ in P[6:9]]),
    Variants(
        Item(r"Evaluate $\displaystyle\int_0^1 \frac{2x}{x^2 + 1}\,dx$.", num(sp.log(2)), r"$u = x^2 + 1$ from $1$ to $2$: $\ln 2$.", work="1.4cm"),
        Item(r"Evaluate $\displaystyle\int_0^1 \frac{1}{x^2 + 1}\,dx$.", num(sp.pi / 4), r"$\arctan 1 = \frac\pi4$.", work="1.4cm"),
        Item(r"Evaluate $\displaystyle\int_0^1 \frac{x^2}{x^2 + 1}\,dx$.", num(1 - sp.pi / 4), r"Divide: $1 - \frac{1}{x^2 + 1}$: $1 - \frac\pi4$.", work="1.4cm"),
    ),
]
same("q5", [sp.integrate(2 * x / (x**2 + 1), (x, 0, 1)), sp.integrate(1 / (x**2 + 1), (x, 0, 1)), sp.integrate(x**2 / (x**2 + 1), (x, 0, 1))], [sp.log(2), sp.pi / 4, 1 - sp.pi / 4])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$\displaystyle\int \frac{x}{x^2 + 4}\,dx = $", [r"$\frac12\arctan\frac x2 + C$", r"$\frac12\ln\left(x^2 + 4\right) + C$", r"$\ln\left(x^2 + 4\right) + C$", r"$\frac{x^2}{2}\ln\left(x^2 + 4\right) + C$"], "B",
        r"Substitution, $u = x^2 + 4$.", why_not={"A": "that's $\\int \\frac{1}{x^2 + 4}\\,dx$"}),
    MCQ(r"$\displaystyle\int \frac{1}{x^2 + 4}\,dx = $", [r"$\frac12\ln\left(x^2 + 4\right) + C$", r"$\arctan\frac x2 + C$", r"$\frac14\arctan\frac x2 + C$", r"$\frac12\arctan\frac x2 + C$"], "D", r"$a = 2$: $\frac1a\arctan\frac xa$."),
    MCQ(r"$\displaystyle\int \frac{x^2 + 4}{x}\,dx = $", [r"$\frac{x^2}{2} + 4\ln|x| + C$", r"$\frac{\frac{x^3}{3} + 4x}{\frac{x^2}{2}} + C$", r"$x^2 + 4\ln|x| + C$", r"$\frac{x^2}{2} + \frac{4}{x^2} + C$"], "A",
        r"Split: $x + \frac4x$."),
    MCQ(r"Which integral is best done by substitution?", [r"$\int \frac{dx}{x^2 + 2x + 2}$", r"$\int \frac{x^3}{x + 1}\,dx$", r"$\int x^2\sin\left(x^3\right) dx$", r"$\int (x + 3)^2\,dx$ only by expanding"], "C",
        r"$u = x^3$; $3x^2$ is a factor up to a constant."),
]
same("m", [sp.simplify(sp.integrate(x / (x**2 + 4), x) - sp.log(x**2 + 4) / 2), sp.simplify(sp.integrate(1 / (x**2 + 4), x) - sp.atan(x / 2) / 2)], [0, 0])

FRQS = []

TOPIC = Topic(
    number="6.14", title="Selecting Techniques for Antidifferentiation",
    unit="Unit 6: Integration and Accumulation of Change", ced=["FUN-6.D", "FUN-6.E", "FUN-6.F"],
    goals=r"Choose an appropriate technique (basic rules, rewriting, substitution, long division, completing the square) by noticing the features of an integrand.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
