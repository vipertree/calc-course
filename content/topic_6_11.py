"""Topic 6.11 (BC only): Integrating using integration by parts.

CED: FUN-6.E (FUN-6.E.1): integral u dv = uv - integral v du, from the product rule; choose u to simplify when
differentiated (LIATE as a guide) and dv to be integrable; a four-box table (u, dv, du, v). Lesson examples: x e^x,
ln x on [1, e]. Worked examples: x cos x, x^2 e^x (parts twice), arctan x.
"""
import sympy as sp

from calclib import (VideoExample, MCQ, BigIdea, Check, Formula, Item, Section, Text, Topic, Variants, Video, expr, num, same)

x = sp.symbols("x", positive=True)
C = sp.Symbol("C")


def tex(F):
    return (sp.latex(F).replace(r"\log{", r"\ln{").replace(r"\operatorname{atan}", r"\arctan").replace(r"\operatorname{asin}", r"\arcsin"))


def plus_c(f, F):
    assert sp.simplify(sp.diff(F, x) - f) == 0, (f, F)
    return expr(F + C, display=tex(F) + " + C")


same("lesson", [sp.integrate(sp.log(x), (x, 1, sp.E))], [1])

NOTES = [
    Video("s6_11.py::Lesson", "Integration by parts", 5),

    Section("The product rule, backward"),
    Formula("Integration by parts", (
        r"\[ \int u\,dv = uv - \blank{\int v\,du}. \] Choose $u$ to be the part that gets simpler when differentiated; $dv$ is everything else, "
        r"including $dx$. A guide for $u$: \textbf{LIATE} (logarithmic, inverse trig, algebraic, trig, exponential), top of the list first.")),
    Text(r"Keep a four-box table: $u$ and $dv$ on top, $du$ (differentiate) and $v$ (integrate) underneath."),
    VideoExample('A first example', work="2.6cm"),
    VideoExample('A definite integral', work="2.6cm"),
    Text(r"\textbf{Repeat or substitute.} Sometimes the new integral needs parts again (each time the power of $x$ drops), or a substitution."),
    BigIdea(r"Integration by parts trades $\int u\,dv$ for $uv - \int v\,du$. Choose $u$ to simplify when differentiated."),
    Check(r"Find $\displaystyle\int x\sin x\,dx$.", plus_c(x * sp.sin(x), -x * sp.cos(x) + sp.sin(x)), r"$u = x$, $dv = \sin x\,dx$: $-x\cos x + \sin x + C$."),
]

# ---------------------------------------------------------------- practice
P = [(x * sp.exp(2 * x), x * sp.exp(2 * x) / 2 - sp.exp(2 * x) / 4, r"u = x,\ dv = e^{2x}\,dx"), (x * sp.sin(3 * x), -x * sp.cos(3 * x) / 3 + sp.sin(3 * x) / 9, r"u = x,\ dv = \sin 3x\,dx"),
     (x * sp.log(x), x**2 * sp.log(x) / 2 - x**2 / 4, r"u = \ln x,\ dv = x\,dx"), (x**2 * sp.log(x), x**3 * sp.log(x) / 3 - x**3 / 9, r"u = \ln x,\ dv = x^2\,dx"),
     (x * sp.exp(-x), -x * sp.exp(-x) - sp.exp(-x), r"u = x,\ dv = e^{-x}\,dx"), (x**2 * sp.cos(x), x**2 * sp.sin(x) + 2 * x * sp.cos(x) - 2 * sp.sin(x), r"u = x^2 \text{ (twice)}"),
     (sp.asin(x), x * sp.asin(x) + sp.sqrt(1 - x**2), r"u = \arcsin x,\ dv = dx"), (sp.log(x) / x**2, -sp.log(x) / x - 1 / x, r"u = \ln x,\ dv = x^{-2}\,dx")]
PRACTICE = [Item(rf"Find $\displaystyle\int {sp.latex(f)}\,dx$.", plus_c(f, F), rf"${u}$: ${tex(F)} + C$.", work="2.6cm") for f, F, u in P]
PRACTICE += [
    Item(r"Evaluate $\displaystyle\int_0^1 x e^x\,dx$.", num(sp.integrate(x * sp.exp(x), (x, 0, 1))), r"$\left[x e^x - e^x\right]_0^1 = 0 - (-1) = 1$.", work="2cm"),
    Item(r"Evaluate $\displaystyle\int_0^\pi x\sin x\,dx$.", num(sp.integrate(x * sp.sin(x), (x, 0, sp.pi))), r"$\left[-x\cos x + \sin x\right]_0^\pi = \pi$.", work="2cm"),
]
same("p def", [sp.integrate(x * sp.exp(x), (x, 0, 1)), sp.integrate(x * sp.sin(x), (x, 0, sp.pi))], [1, sp.pi])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(*[Item(rf"Find $\displaystyle\int {sp.latex(f)}\,dx$.", plus_c(f, F), rf"${tex(F)} + C$.", work="2cm")
               for f, F in ((x * sp.exp(3 * x), x * sp.exp(3 * x) / 3 - sp.exp(3 * x) / 9), (x * sp.cos(2 * x), x * sp.sin(2 * x) / 2 + sp.cos(2 * x) / 4), (x * sp.exp(x / 2), 2 * x * sp.exp(x / 2) - 4 * sp.exp(x / 2)))]),
    Variants(*[Item(rf"Find $\displaystyle\int {sp.latex(f)}\,dx$.", plus_c(f, F), rf"${tex(F)} + C$.", work="2cm")
               for f, F in ((sp.log(x), x * sp.log(x) - x), (x**3 * sp.log(x), x**4 * sp.log(x) / 4 - x**4 / 16), (sp.sqrt(x) * sp.log(x), sp.Rational(2, 3) * x**sp.Rational(3, 2) * sp.log(x) - sp.Rational(4, 9) * x**sp.Rational(3, 2)))]),
    Variants(
        MCQ(r"For $\int x^2 e^{5x}\,dx$ by parts, the best choice is", [r"$u = e^{5x}$", r"$u = x^2$", r"$u = x^2 e^{5x}$", r"$u = 5x$"], "B", r"Algebraic before exponential; $x^2$ simplifies when differentiated."),
        MCQ(r"For $\int x\ln x\,dx$ by parts, the best choice is", [r"$u = x$", r"$u = x\ln x$", r"$u = \ln x$", r"$dv = \ln x\,dx$"], "C", r"Logarithmic first; and $\ln x$ is hard to integrate."),
        MCQ(r"For $\int x\arctan x\,dx$ by parts, the best choice is", [r"$u = \arctan x$", r"$u = x$", r"$dv = \arctan x\,dx$", r"$u = 1 + x^2$"], "A", r"Inverse trig before algebraic."),
    ),
    Variants(*[Item(rf"Evaluate $\displaystyle\int_{{{a}}}^{{{sp.latex(b)}}} {sp.latex(f)}\,dx$.", num(sp.integrate(f, (x, a, b))), rf"By parts: ${sp.latex(sp.integrate(f, (x, a, b)))}$.", work="2cm")
               for f, a, b in ((x * sp.exp(-x), 0, 1), (sp.log(x), 1, sp.E**2), (x * sp.cos(x), 0, sp.pi / 2))]),
    Variants(
        MCQ(r"$\int x f''(x)\,dx = $", [r"$x f'(x) - f(x) + C$", r"$x f'(x) + f(x) + C$", r"$\frac{x^2}{2} f''(x) + C$", r"$f'(x) - x f(x) + C$"], "A", r"$u = x$, $dv = f''(x)\,dx$, $v = f'(x)$."),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$\displaystyle\int x e^{2x}\,dx = $", [r"$\frac12 x e^{2x} - \frac14 e^{2x} + C$", r"$\frac12 x e^{2x} + \frac14 e^{2x} + C$", r"$x e^{2x} - e^{2x} + C$", r"$\frac{x^2}{4}e^{2x} + C$"], "A",
        r"$u = x$, $v = \frac12 e^{2x}$: $\frac12 x e^{2x} - \int \frac12 e^{2x}\,dx$."),
    MCQ(r"$\displaystyle\int_1^e x\ln x\,dx = $", [r"$\frac{e^2}{2}$", r"$\frac{e^2 + 1}{4}$", r"$\frac{e^2 - 1}{4}$", r"$1$"], "B", r"$\left[\frac{x^2}{2}\ln x - \frac{x^2}{4}\right]_1^e = \frac{e^2}{4} + \frac14$."),
    MCQ(r"If $\int x\cos x\,dx = x\sin x - \int g(x)\,dx$, then $g(x) = $", [r"$\cos x$", r"$-\sin x$", r"$x\cos x$", r"$\sin x$"], "D", r"$v\,du = \sin x\,dx$."),
    MCQ(r"$f(1) = 2$, $f(3) = 5$, $f'(1) = 4$, $f'(3) = 6$, and $\int_1^3 f(x)\,dx = 7$. $\displaystyle\int_1^3 x f'(x)\,dx = $", [r"$13$", r"$8$", r"$6$", r"$20$"], "C",
        r"$u = x$, $dv = f'(x)\,dx$: $[x f(x)]_1^3 - \int_1^3 f(x)\,dx = (15 - 2) - 7 = 6$."),
]
same("m", [sp.simplify(sp.integrate(x * sp.exp(2 * x), x) - (x * sp.exp(2 * x) / 2 - sp.exp(2 * x) / 4)), sp.integrate(x * sp.log(x), (x, 1, sp.E)), (3 * 5 - 1 * 2) - 7],
     [0, (sp.E**2 + 1) / 4, 6])

FRQS = []

TOPIC = Topic(
    number="6.11", title="Integrating Using Integration by Parts",
    unit="Unit 6: Integration and Accumulation of Change", ced=["FUN-6.E", "FUN-6.E.1"],
    goals=r"Find indefinite and definite integrals with integration by parts, choosing $u$ and $dv$ well.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
