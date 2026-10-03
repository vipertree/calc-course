"""Topic 3.5: Selecting procedures for calculating derivatives.

CED: FUN-3.F (choosing among the derivative rules; rewriting first). The decision guide reads the OUTERMOST operation first,
the same flow as the video.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Text, Topic, Variants, Video, expr, num,
                     same, selfcheck)

x, y, t = sp.symbols("x y t")
pi = sp.pi


def D(e):
    return sp.simplify(sp.diff(e, x))


NOTES = [
    Video("s3_5.py::Lesson", "Choosing the right rule", 4),

    Section("Read the outermost operation first"),
    Formula("A decision guide", (
        r"Look at the outermost function or operation. \par "
        r"\quad $\bullet$ A sum or difference: differentiate \blank{term by term}. \par "
        r"\quad $\bullet$ A constant times something: keep the constant. \par "
        r"\quad $\bullet$ A product: the \blank{product rule}. \par "
        r"\quad $\bullet$ A quotient: the quotient rule, unless you can \blank{rewrite} it more simply first. \par "
        r"\quad $\bullet$ A function with an inner function inside it, like $\sin(3x)$ or $(x^2 + 1)^5$: the \blank{chain rule}. \par "
        r"\quad $\bullet$ An equation that doesn't solve easily for $y$: implicit differentiation. \par "
        r"Then repeat the question for each piece.")),
    VideoExample('Layers', work="2.2cm"),
    VideoExample('Rewrite first', work="2.2cm"),
    BigIdea(r"There is no single rule to memorize. Peel the function from the outside in, and rewrite whenever it makes the work shorter."),
    Check(r"Which rule do you use first for $\left(x^2 + 1\right)^3\cos x$?", selfcheck(r"\text{product rule}"),
          r"The outermost operation is multiplication: the product rule, with the chain rule inside the first factor."),
]
same("ex1", D(x**2 * sp.sin(3 * x)), 2 * x * sp.sin(3 * x) + 3 * x**2 * sp.cos(3 * x))
same("ex2", D((x**3 - 2 * sp.sqrt(x)) / x), 2 * x + x**sp.Rational(-3, 2))
same("ex4", sp.simplify(D(sp.log(x**2 / (x + 1))) - (2 / x - 1 / (x + 1))), 0)

# ---------------------------------------------------------------- practice
P = [(r"y = x^3 e^{-2x}", x**3 * sp.exp(-2 * x), r"Product, with the chain rule on $e^{-2x}$: $3x^2e^{-2x} - 2x^3e^{-2x}$."),
     (r"y = \dfrac{\sin x}{1 + \cos x}", sp.sin(x) / (1 + sp.cos(x)), r"Quotient: $\dfrac{\cos x(1 + \cos x) + \sin^2 x}{(1+\cos x)^2} = \dfrac{1}{1 + \cos x}$."),
     (r"y = \ln\left(x^2 + 4\right)", sp.log(x**2 + 4), r"Chain: $\dfrac{2x}{x^2 + 4}$."),
     (r"y = \left(3x - \dfrac1x\right)^4", (3 * x - 1 / x)**4, r"Chain: $4\left(3x - \frac1x\right)^3\left(3 + \frac{1}{x^2}\right)$."),
     (r"y = \dfrac{x^4 + 3x}{x^2}", (x**4 + 3 * x) / x**2, r"Rewrite $x^2 + 3x^{-1}$: $2x - 3x^{-2}$."),
     (r"y = e^{x}\tan x", sp.exp(x) * sp.tan(x), r"Product: $e^x\tan x + e^x\sec^2 x$."),
     (r"y = \sin^3(2x)", sp.sin(2 * x)**3, r"Chain twice: $3\sin^2(2x)\cos(2x)\cdot 2$."),
     (r"y = \arctan\left(x^2\right)", sp.atan(x**2), r"Chain: $\dfrac{2x}{1 + x^4}$."),
     (r"y = \sqrt{x}\,\ln x", sp.sqrt(x) * sp.log(x), r"Product: $\dfrac{\ln x}{2\sqrt x} + \dfrac{1}{\sqrt x}$."),
     (r"y = \dfrac{e^{2x}}{x}", sp.exp(2 * x) / x, r"Quotient: $\dfrac{2xe^{2x} - e^{2x}}{x^2}$."),
     (r"y = \ln\left(\dfrac{x^3}{x - 2}\right)", sp.log(x**3 / (x - 2)), r"Rewrite $3\ln x - \ln(x - 2)$: $\dfrac3x - \dfrac{1}{x - 2}$."),
     (r"y = \cos\left(\sqrt{x}\right)", sp.cos(sp.sqrt(x)), r"Chain: $-\sin\left(\sqrt x\right)\cdot\dfrac{1}{2\sqrt x}$."),
     (r"y = x^2\left(x^3 + 1\right)^5", x**2 * (x**3 + 1)**5, r"Product, then chain: $2x(x^3+1)^5 + x^2\cdot 5(x^3+1)^4\cdot 3x^2$."),
     (r"y = \dfrac{1}{\sqrt{1 - x^2}}", 1 / sp.sqrt(1 - x**2), r"Rewrite $(1 - x^2)^{-1/2}$, chain: $x(1 - x^2)^{-3/2}$.")]
PRACTICE = [Item(rf"Find $\dfrac{{dy}}{{dx}}$ for ${tex}$. Name the first rule you used.", expr(str(D(e))), sol, work="2cm")
            for tex, e, sol in P]
PRACTICE += [
    Item(r"Find $\dfrac{dy}{dx}$ for $x^2y + \sin y = 3x$.", expr("(3 - 2*x*y)/(x**2 + cos(y))"),
         r"Implicit: $2xy + x^2y' + \cos y\,y' = 3$, so $y' = \dfrac{3 - 2xy}{x^2 + \cos y}$.", work="2.2cm"),
    Item(r"$f(1) = 2$, $f'(1) = 3$, $g(1) = -1$, $g'(1) = 4$. Find the derivative of $f(x)^2 g(x)$ at $x = 1$.", num(4),
         r"Product and chain: $2f f'\cdot g + f^2 g' = 2(2)(3)(-1) + 4(4) = -12 + 16 = 4$.", work="2cm"),
    Item(r"Find the slope of $y = x e^{x^2}$ at $x = 1$.", num(3 * sp.E), r"$e^{x^2} + 2x^2e^{x^2} = 3e$ at $x = 1$.", work="1.6cm"),
    Item(r"Find the equation for the line tangent to $y = \ln(2x - 1)$ at $x = 1$.", expr("2*x - 2"),
         r"Point $(1, 0)$, slope $\dfrac{2}{2x - 1} = 2$: $y = 2x - 2$.", work="1.8cm"),
    Item(r"Chen says $\dfrac{d}{dx}\left[\dfrac{5}{x^3}\right]$ needs the quotient rule. Suggest a faster way and give the derivative.",
         expr("-15/x**4"), r"Rewrite as $5x^{-3}$: $-15x^{-4}$.", work="1.4cm"),
    Item(r"Find the $x$-values in $(0, 2\pi)$ where $y = \sin x\cos x$ has horizontal tangents. Enter the smallest.", num(pi / 4),
         r"$y' = \cos^2 x - \sin^2 x = \cos 2x = 0$ at $x = \frac\pi4, \frac{3\pi}4, \frac{5\pi}4, \frac{7\pi}4$.", work="2cm"),
]
same("p", [sp.simplify(-sp.diff(x**2 * y + sp.sin(y) - 3 * x, x) / sp.diff(x**2 * y + sp.sin(y) - 3 * x, y) - (3 - 2 * x * y) / (x**2 + sp.cos(y))),
           2 * 2 * 3 * (-1) + 4 * 4, D(x * sp.exp(x**2)).subs(x, 1), sp.expand(D(sp.log(2 * x - 1)).subs(x, 1) * (x - 1))],
     [0, 4, 3 * sp.E, 2 * x - 2])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find $\dfrac{d}{dx}\left[x^2 e^{3x}\right]$.", expr("2*x*exp(3*x) + 3*x**2*exp(3*x)"), r"$2xe^{3x} + 3x^2e^{3x}$.", work="1.8cm"),
        Item(r"Find $\dfrac{d}{dx}\left[x\cos(2x)\right]$.", expr("cos(2*x) - 2*x*sin(2*x)"), r"$\cos 2x - 2x\sin 2x$.", work="1.8cm"),
        Item(r"Find $\dfrac{d}{dx}\left[x^3\ln(x^2)\right]$.", expr("3*x**2*log(x**2) + 2*x**2"), r"$3x^2\ln(x^2) + x^3\cdot\dfrac{2}{x} = 3x^2\ln(x^2) + 2x^2$.", work="1.8cm"),
    ),
    Variants(
        Item(r"Find $\dfrac{d}{dx}\sqrt{x^2 + \sin x}$.", expr("(2*x + cos(x))/(2*sqrt(x**2 + sin(x)))"), r"$\dfrac{2x + \cos x}{2\sqrt{x^2 + \sin x}}$.", work="1.8cm"),
        Item(r"Find $\dfrac{d}{dx}\left(e^x + x^2\right)^3$.", expr("3*(exp(x)+x**2)**2*(exp(x)+2*x)"), r"$3\left(e^x + x^2\right)^2\left(e^x + 2x\right)$.", work="1.8cm"),
        Item(r"Find $\dfrac{d}{dx}\ln\left(\cos x\right)$.", expr("-tan(x)"), r"$\dfrac{-\sin x}{\cos x} = -\tan x$.", work="1.8cm"),
    ),
    Variants(
        Item(r"Find $\dfrac{d}{dx}\left[\dfrac{x^2 - 4\sqrt x}{x}\right]$.", expr("1 + 2*x**(-3/2)"), r"Rewrite $x - 4x^{-1/2}$: $1 + 2x^{-3/2}$.", work="1.8cm"),
        Item(r"Find $\dfrac{d}{dx}\ln\left(x^4\sqrt{x}\right)$.", expr("9/(2*x)"), r"Rewrite $\frac92\ln x$: $\dfrac{9}{2x}$.", work="1.8cm"),
        Item(r"Find $\dfrac{d}{dx}\left[\dfrac{6}{x^2} + \dfrac{x}{3}\right]$.", expr("-12/x**3 + 1/3"), r"Rewrite $6x^{-2} + \frac13x$: $-12x^{-3} + \frac13$.", work="1.8cm"),
    ),
    Variants(
        MCQ(r"Which rule should you apply first to $\sin\left(x^2 e^x\right)$?", [r"Product rule", r"Chain rule", r"Quotient rule", r"Power rule"], "B",
            r"The outermost function is sine of something: chain rule first (the inside then needs the product rule)."),
        MCQ(r"Which rule should you apply first to $x^2\sin(e^x)$?", [r"Chain rule", r"Quotient rule", r"Product rule", r"Power rule"], "C",
            r"The outermost operation is multiplication: product rule first."),
        MCQ(r"Which is the fastest correct approach to $\dfrac{d}{dx}\left[\dfrac{x^5 + x}{x}\right]$?",
            [r"Quotient rule", r"Product rule", r"Implicit differentiation", r"Simplify to $x^4 + 1$ first"], "D", r"Divide first: $4x^3$."),
    ),
    Variants(
        MCQ(r"$f(2) = 3$, $f'(2) = -1$. What is the derivative of $\big[f(x)\big]^3$ at $x = 2$?", [r"$-27$", r"$27$", r"$-3$", r"$-9$"], "A",
            r"$3f(2)^2f'(2) = 3(9)(-1) = -27$.", why_not={"C": "forgot to square $f(2)$", "D": "forgot the factor $3$"}),
        MCQ(r"$f(0) = 2$, $f'(0) = 5$. What is the derivative of $e^{f(x)}$ at $x = 0$?", [r"$5$", r"$5e^2$", r"$e^5$", r"$2e^2$"], "B",
            r"$e^{f(0)}f'(0) = 5e^2$.", why_not={"A": "forgot $e^{f(0)}$"}),
        MCQ(r"$f(1) = 4$, $f'(1) = 6$. What is the derivative of $\sqrt{f(x)}$ at $x = 1$?", [r"$3$", r"$\dfrac{1}{4}$", r"$\dfrac32$", r"$12$"], "C",
            r"$\dfrac{f'(1)}{2\sqrt{f(1)}} = \dfrac{6}{4} = \dfrac32$.", why_not={"A": "forgot the $\\frac12$"}),
    ),
]
same("q", [D(x**3 * sp.log(x**2)), D(sp.log(x**4 * sp.sqrt(x))), 3 * 9 * -1, 6 / (2 * sp.sqrt(4))],
     [3 * x**2 * sp.log(x**2) + 2 * x**2, sp.Rational(9, 2) / x, -27, sp.Rational(3, 2)])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"If $f(x) = x\ln\left(x^2\right)$, then $f'(e) =$", [r"$2$", r"$4$", r"$2e$", r"$3$"], "B",
        r"$\ln(x^2) + x\cdot\dfrac{2}{x} = \ln(x^2) + 2$, which is $2 + 2 = 4$ at $x = e$.", why_not={"A": "forgot the product rule"}),
    MCQ(r"$\dfrac{d}{dx}\left[e^{\sin x}\cos x\right] =$", [r"$e^{\sin x}\left(\cos^2 x - \sin x\right)$", r"$-e^{\sin x}\sin x$",
        r"$e^{\cos x}\cos x$", r"$e^{\sin x}\cos^2 x$"], "A",
        r"Product and chain: $e^{\sin x}\cos x\cdot\cos x + e^{\sin x}(-\sin x)$.", why_not={"D": "dropped the second product term"}),
    MCQ(r"$f(3) = 1$, $f'(3) = 4$, $g(1) = 5$, $g'(1) = -2$, $g'(3) = 7$. If $h(x) = x\,g\big(f(x)\big)$, then $h'(3) =$",
        [r"$29$", r"$-24$", r"$-19$", r"$84$"], "C",
        r"Product then chain: $g\big(f(3)\big) + 3g'\big(f(3)\big)f'(3) = 5 + 3(-2)(4) = -19$.", why_not={"A": "used $g'(3)$", "B": "dropped the first product term"}),
    MCQ(r"The slope of $y^2 + xy = 6$ at $(1, 2)$ is", [r"$-\dfrac25$", r"$\dfrac25$", r"$-\dfrac52$", r"$-\dfrac12$"], "A",
        r"$2yy' + y + xy' = 0$, so $y' = -\dfrac{y}{2y + x} = -\dfrac25$.", why_not={"C": "inverted"}),
]
same("m", [D(x * sp.log(x**2)).subs(x, sp.E), sp.simplify(D(sp.exp(sp.sin(x)) * sp.cos(x)) - sp.exp(sp.sin(x)) * (sp.cos(x)**2 - sp.sin(x))),
           5 + 3 * -2 * 4, sp.simplify(-sp.diff(y**2 + x * y - 6, x) / sp.diff(y**2 + x * y - 6, y)).subs({x: 1, y: 2})],
     [4, 0, -19, sp.Rational(-2, 5)])

FRQS = [
    FRQ("Choosing the rules", (
        r"Let $f$ be the function defined by $f(x) = x^2 e^{x - 2}$. Let $g$ be a differentiable function. The table gives values "
        r"of $g$ and its derivative $g'$ at selected values of $x$."
        r"\par\smallskip\centerline{\begin{tabular}{c|cc} $x$ & $2$ & $4$ \\ \hline $g(x)$ & $5$ & $-1$ \\ $g'(x)$ & $3$ & $6$"
        r"\end{tabular}}"), [
        Part("a", r"Find the slope of the line tangent to the graph of $f$ at $x = 2$.", num(8),
             r"$f'(x) = 2xe^{x-2} + x^2e^{x-2}$, so $f'(2) = 4 + 4 = 8$.",
             [(1, "$f'(x)$ with the product and chain rules"), (1, "answer $8$")], work="2.4cm"),
        Part("b", r"Let $k$ be the function defined by $k(x) = g\big(f(x)\big)$. Find $k'(2)$.", num(48),
             r"$k'(2) = g'\big(f(2)\big)\cdot f'(2) = g'(4)\cdot 8 = 6\cdot 8 = 48$, since $f(2) = 4$.",
             [(1, "$k'(x) = g'\\big(f(x)\\big)f'(x)$"), (1, "answer $48$")], work="2.2cm"),
        Part("c", r"Let $m$ be the function defined by $m(x) = \dfrac{g(2x)}{x^2 + 1}$. Find $m'(2)$. Show the work that leads to your answer.",
             num(sp.Rational(64, 25)),
             r"$m'(x) = \dfrac{2g'(2x)\,(x^2+1) - g(2x)\cdot 2x}{(x^2+1)^2}$, so "
             r"$m'(2) = \dfrac{2g'(4)(5) - g(4)(4)}{25} = \dfrac{2(6)(5) - (-1)(4)}{25} = \dfrac{64}{25}$.",
             [(1, "quotient rule"), (1, "chain rule on $g(2x)$"), (1, "answer $\\frac{64}{25}$")], work="3cm"),
    ], frq_type="Derivatives from a table"),
]
f5 = x**2 * sp.exp(x - 2)
g5 = {2: (5, 3), 4: (-1, 6)}
same("frq a", [f5.subs(x, 2), D(f5).subs(x, 2)], [4, 8])
same("frq b", g5[4][1] * D(f5).subs(x, 2), 48)
# a concrete cubic with the table's values stands in for g
c5 = sp.symbols("c0:4")
gp5 = sum(c * x**i for i, c in enumerate(c5))
gp5 = gp5.subs(sp.solve([gp5.subs(x, 2) - 5, D(gp5).subs(x, 2) - 3, gp5.subs(x, 4) + 1, D(gp5).subs(x, 4) - 6], c5))
same("frq b cubic", D(gp5.subs(x, f5)).subs(x, 2), 48)
same("frq c", D(gp5.subs(x, 2 * x) / (x**2 + 1)).subs(x, 2), sp.Rational(64, 25))

TOPIC = Topic(
    number="3.5", title="Selecting Procedures for Calculating Derivatives",
    unit="Unit 3: Differentiation: Composite, Implicit, and Inverse Functions", ced=["FUN-3.F", "FUN-3.F.1"],
    goals=r"Choose and combine the derivative rules by reading a function from the outside in, and rewrite first when it helps.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
