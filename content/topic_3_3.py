"""Topic 3.3: Differentiating inverse functions.

CED: FUN-3.E.1 (derivative of an inverse: (f^-1)'(b) = 1 / f'(f^-1(b))). The mirror picture (reflection across y = x swaps rise
and run) is the visual proof, as in the video. Running example: f(x) = x^3 + x, f(1) = 2, so (f^-1)'(2) = 1/4.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Table, Text, Topic, Variants, Video, expr,
                     num, same, selfcheck)
from calclib.figs import graph

x, y = sp.symbols("x y")


def inv_slope(f, a):
    """(f^-1)'(f(a)) = 1 / f'(a)."""
    return sp.nsimplify(1 / sp.diff(f, x).subs(x, a))


same("run", [(x**3 + x).subs(x, 1), inv_slope(x**3 + x, 1)], [2, sp.Rational(1, 4)])

FIG_M = graph("t3_3_mirror", [("0.25*x^2+1", 0, 3.4), ("2*sqrt(x-1)", 1, 3.9, "dashed"), ("x", -0.5, 4)],
              xr=(-0.5, 4.2), yr=(-0.5, 4.2), labels=[],
              extra=r"\addplot[closed] coordinates {(1,1.25)(1.25,1)};"
                    r"\node[font=\footnotesize, left] at (axis cs:1,1.25) {$(a, b)$};\node[font=\footnotesize, below right] at (axis cs:1.25,1) {$(b, a)$};",
              w="5.6cm", h="5.6cm", caption=r"A function (solid), its inverse (dashed), and the mirror line $y = x$.")

NOTES = [
    Video("s3_3.py::Lesson", "Derivatives of inverse functions", 5),

    Section("The mirror picture"),
    FIG_M,
    Text(r"The graph of $f^{-1}$ is the graph of $f$ reflected across the line $y = x$. The point $(a, b)$ on $f$ becomes the point "
         r"\blank{$(b, a)$} on $f^{-1}$."),
    Text(r"Reflecting across $y = x$ swaps every horizontal distance with a vertical one. So a tangent line with rise over run "
         r"$\displaystyle \dfrac{\Delta y}{\Delta x}$ turns into one with rise over run \blank{$\dfrac{\Delta x}{\Delta y}$}: the slope becomes its reciprocal."),
    Formula("Derivative of an inverse", (
        r"If $f(a) = b$ and $f'(a) \ne 0$, then $\displaystyle \left(f^{-1}\right)'(b) = \mblank{\frac{1}{f'(a)}}$. "
        r"The slopes are reciprocals \blank{at matching points}: $b$ for the inverse, $a$ for $f$.")),

    Section("Using it"),
    Example("Without a formula for the inverse", (
        r"$f(x) = x^3 + x$. Find $\left(f^{-1}\right)'(2)$."),
        r"We need the $a$ with $f(a) = 2$: $a^3 + a = 2$ gives $a = 1$. $f'(x) = 3x^2 + 1$, so $f'(1) = 4$. Then "
        r"\[ \left(f^{-1}\right)'(2) = \frac{1}{f'(1)} = \frac14. \]", work="2.6cm", beat="An example without the inverse"),
    Text(r"\textbf{The trap.} $\displaystyle \dfrac{1}{f'(2)} = \dfrac{1}{13}$ is wrong. The input $2$ belongs to $f^{-1}$; on the graph of $f$, the matching "
         r"point is $x = \mblank{1}$."),
    Table(r"$x$ & $g(x)$ & $g'(x)$ \\ $1$ & $4$ & $3$ \\ $4$ & $6$ & $\frac12$", "c|cc"),
    VideoExample('From a table', work="2cm"),
    Example("Why implicit differentiation agrees", r"Let $y = f^{-1}(x)$, so $f(y) = x$. Differentiate implicitly.",
            r"$\displaystyle f'(y)\,\dfrac{dy}{dx} = 1$, so \[ \frac{dy}{dx} = \frac{1}{f'(y)} = \frac{1}{f'\left(f^{-1}(x)\right)}: \] the same formula.", work="2.4cm", beat="Implicit differentiation agrees"),
    VideoExample('The natural log, again', work="2cm"),
    BigIdea(r"The inverse's slope is the reciprocal of the original's slope, at the mirrored point."),
    Check(r"$f(3) = 7$ and $f'(3) = 5$. Find $\left(f^{-1}\right)'(7)$.", num(sp.Rational(1, 5)), r"\[ \frac{1}{f'(3)} = \frac15. \]"),
]
same("trap", 1 / sp.diff(x**3 + x, x).subs(x, 2), sp.Rational(1, 13))

# ---------------------------------------------------------------- practice
PR = [(x**3 + 2 * x, r"x^3 + 2x", 3), (x**5 + x, r"x^5 + x", 2), (2 * x + sp.exp(x), r"2x + e^x", 1),
      (x**3 + x**2 + x, r"x^3 + x^2 + x", 3), (sp.sqrt(x + 5), r"\sqrt{x + 5}", 3)]
PRACTICE = []
for f, tex, b in PR:
    a = [r for r in sp.solve(sp.Eq(f, b), x) if r.is_real][0]
    PRACTICE.append(Item(rf"$f(x) = {tex}$ is invertible. Find $\left(f^{-1}\right)'({b})$.", num(inv_slope(f, a)),
                         rf"$f({sp.latex(a)}) = {b}$, and $f'({sp.latex(a)}) = {sp.latex(sp.diff(f, x).subs(x, a))}$, so "
                         rf"$\left(f^{{-1}}\right)'({b}) = {sp.latex(inv_slope(f, a))}$.", work="2.2cm"))
PRACTICE += [
    Item(r"$f(2) = 5$ and $f'(2) = -4$. Find $\left(f^{-1}\right)'(5)$.", num(sp.Rational(-1, 4)), r"$\dfrac{1}{f'(2)} = -\dfrac14$.", work="1.2cm"),
    Item(r"$h(0) = 3$, $h'(0) = 2$, $h(3) = 8$, $h'(3) = 6$. Find $\left(h^{-1}\right)'(3)$.", num(sp.Rational(1, 2)),
         r"$h(0) = 3$, so the matching point is $x = 0$: $\dfrac{1}{h'(0)} = \dfrac12$. ($h'(3)$ is a distractor.)", work="1.6cm"),
    Item(r"The line $y = 4x - 7$ is tangent to the graph of an invertible $f$ at $x = 2$. Find $\left(f^{-1}\right)'(1)$.", num(sp.Rational(1, 4)),
         r"$f(2) = 4(2) - 7 = 1$ and $f'(2) = 4$. So $\left(f^{-1}\right)'(1) = \dfrac14$.", work="1.8cm"),
    Item(r"Let $g = f^{-1}$ with $f(x) = x^3 + x + 1$. Find the equation for the line tangent to $g$ at $x = 3$.", expr("x/4 + 1/4"),
         r"$f(1) = 3$, so $g(3) = 1$. $f'(1) = 4$, so $g'(3) = \dfrac14$. Line: $y - 1 = \frac14(x - 3)$, so $y = \frac14x + \frac14$.", work="2.4cm"),
    Item(r"$f(x) = e^{2x}$. Find $\left(f^{-1}\right)'(1)$ two ways: with the formula, and by finding $f^{-1}$.", num(sp.Rational(1, 2)),
         r"Formula: $f(0) = 1$, $f'(0) = 2$, so $\frac12$. Directly: $f^{-1}(x) = \frac12\ln x$, derivative $\frac{1}{2x} = \frac12$ at $x = 1$.",
         work="2.4cm"),
    Item(r"Use implicit differentiation on $y^3 = x$ to find the derivative of $\sqrt[3]{x}$. Write it using only $x$.", expr("1/(3*x**(2/3))"),
         r"$3y^2y' = 1$, so $y' = \dfrac{1}{3y^2} = \dfrac{1}{3x^{2/3}}$. This matches the power rule.", work="2cm"),
    Item(r"$f$ is increasing with $f(4) = 10$ and $f'(4) = 0.2$. Is the graph of $f^{-1}$ steep or shallow at $x = 10$? Enter its slope.", num(5),
         r"$\dfrac{1}{0.2} = 5$: steep, as the mirror of a shallow slope should be.", work="1.4cm"),
    Item(r"Why does the formula require $f'(a) \ne 0$? Describe the inverse's graph at $(b, a)$ when $f'(a) = 0$.",
         selfcheck(r"\text{vertical tangent}"),
         r"A horizontal tangent on $f$ reflects into a vertical tangent on $f^{-1}$, which has no slope. The reciprocal $\frac10$ is undefined.", work="1.8cm"),
    Item(r"Values of an invertible $g$ are given: $g(2) = 5$, $g'(2) = \frac14$, $g(5) = 9$, $g'(5) = 3$. Find $\left(g^{-1}\right)'(5)$.", num(4),
         r"$g(2) = 5$, so use $x = 2$: $\dfrac{1}{g'(2)} = 4$.", work="1.6cm"),
    Item(r"Values of an invertible $g$ are given: $g(2) = 5$, $g'(2) = \frac14$, $g(5) = 9$, $g'(5) = 3$. Find $\left(g^{-1}\right)'(9)$.",
         num(sp.Rational(1, 3)), r"$g(5) = 9$, so use $x = 5$: $\dfrac{1}{g'(5)} = \dfrac13$.", work="1.6cm"),
    Item(r"$f(x) = x + \sin x$ is invertible. Find $\left(f^{-1}\right)'(0)$.", num(sp.Rational(1, 2)),
         r"$f(0) = 0$, so the matching point is $x = 0$. $f'(0) = 1 + \cos 0 = 2$, so $\left(f^{-1}\right)'(0) = \dfrac12$.", work="1.8cm"),
]
same("p gens", [inv_slope(f, [r for r in sp.solve(sp.Eq(f, b), x) if r.is_real][0]) for f, _, b in PR],
     [sp.Rational(1, 5), sp.Rational(1, 6), sp.Rational(1, 3), sp.Rational(1, 6), 6])
same("p tangent", [(x**3 + x + 1).subs(x, 1), inv_slope(x**3 + x + 1, 1), sp.expand(1 + sp.Rational(1, 4) * (x - 3))],
     [3, sp.Rational(1, 4), x / 4 + sp.Rational(1, 4)])
same("p others", [inv_slope(sp.exp(2 * x), 0), inv_slope(x + sp.sin(x), 0), sp.diff(sp.log(x) / 2, x).subs(x, 1)],
     [sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(1, 2)])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"$f(4) = 9$ and $f'(4) = 3$. Find $\left(f^{-1}\right)'(9)$.", num(sp.Rational(1, 3)), r"$\dfrac{1}{f'(4)} = \dfrac13$.", work="1.2cm"),
        Item(r"$f(-1) = 2$ and $f'(-1) = -5$. Find $\left(f^{-1}\right)'(2)$.", num(sp.Rational(-1, 5)), r"$\dfrac{1}{f'(-1)} = -\dfrac15$.", work="1.2cm"),
        Item(r"$f(0) = 6$ and $f'(0) = \frac23$. Find $\left(f^{-1}\right)'(6)$.", num(sp.Rational(3, 2)), r"$\dfrac{1}{2/3} = \dfrac32$.", work="1.2cm"),
    ),
    Variants(
        Item(r"$f(x) = x^3 + 2x$ is invertible. Find $\left(f^{-1}\right)'(3)$.", num(sp.Rational(1, 5)),
             r"$f(1) = 3$ and $f'(1) = 3 + 2 = 5$, so $\dfrac15$.", work="2cm"),
        Item(r"$f(x) = x^5 + 3x$ is invertible. Find $\left(f^{-1}\right)'(4)$.", num(sp.Rational(1, 8)),
             r"$f(1) = 4$ and $f'(1) = 5 + 3 = 8$, so $\dfrac18$.", work="2cm"),
        Item(r"$f(x) = e^x + x$ is invertible. Find $\left(f^{-1}\right)'(1)$.", num(sp.Rational(1, 2)),
             r"$f(0) = 1$ and $f'(0) = 1 + 1 = 2$, so $\dfrac12$.", work="2cm"),
    ),
    Variants(
        Item(r"$g(1) = 3$, $g'(1) = 4$, $g(3) = 7$, $g'(3) = 2$. Find $\left(g^{-1}\right)'(3)$.", num(sp.Rational(1, 4)),
             r"$g(1) = 3$, so use $x = 1$: $\dfrac{1}{g'(1)} = \dfrac14$.", work="1.6cm"),
        Item(r"$g(2) = 0$, $g'(2) = 5$, $g(0) = 2$, $g'(0) = -1$. Find $\left(g^{-1}\right)'(2)$.", num(-1),
             r"$g(0) = 2$, so use $x = 0$: $\dfrac{1}{g'(0)} = -1$.", work="1.6cm"),
        Item(r"$g(5) = 1$, $g'(5) = 10$, $g(1) = 5$, $g'(1) = \frac12$. Find $\left(g^{-1}\right)'(1)$.", num(sp.Rational(1, 10)),
             r"$g(5) = 1$, so use $x = 5$: $\dfrac{1}{g'(5)} = \dfrac1{10}$.", work="1.6cm"),
    ),
    Variants(
        MCQ(r"$f(2) = 7$. Which expression equals $\left(f^{-1}\right)'(7)$?", [r"$\dfrac{1}{f'(7)}$", r"$\dfrac{1}{f'(2)}$", r"$-f'(2)$", r"$f'(7)$"], "B",
            r"Reciprocal of $f'$ at the matching point $x = 2$.", why_not={"A": "wrong point: $7$ is an output of $f$"}),
        MCQ(r"Reflecting the graph of $f$ across $y = x$ turns a tangent slope of $3$ at $(a, b)$ into what slope at $(b, a)$?",
            [r"$-3$", r"$3$", r"$\dfrac13$", r"$-\dfrac13$"], "C", r"Reflection swaps rise and run.", why_not={"D": "that's a perpendicular slope"}),
        MCQ(r"If $f'(a) = 0$ and $f(a) = b$, the graph of $f^{-1}$ at $(b, a)$ has", [r"a horizontal tangent", r"slope $1$", r"a corner",
            r"a vertical tangent"], "D", r"A horizontal tangent reflects into a vertical one."),
    ),
    Variants(
        MCQ(r"If $y = f^{-1}(x)$, implicit differentiation of $f(y) = x$ gives $\dfrac{dy}{dx} =$",
            [r"$f'(y)$", r"$\dfrac{1}{f'(y)}$", r"$\dfrac{1}{f'(x)}$", r"$f'(x)$"], "B", r"$f'(y)\,y' = 1$."),
        MCQ(r"$f(x) = x^3$ for $x > 0$. The slope of $f^{-1}$ at $x = 8$ is", [r"$12$", r"$\dfrac{1}{192}$", r"$\dfrac{1}{12}$", r"$\dfrac18$"], "C",
            r"$f(2) = 8$, $f'(2) = 12$, so $\frac{1}{12}$.", why_not={"B": "used $f'(8)$"}),
        MCQ(r"The line $y = 2x + 1$ is tangent to invertible $f$ at $x = 3$. What is $\left(f^{-1}\right)'(7)$?", [r"$2$", r"$\dfrac12$", r"$\dfrac17$", r"$3$"], "B",
            r"$f(3) = 7$ and $f'(3) = 2$, so $\frac12$."),
    ),
]
same("q", [inv_slope(x**3 + 2 * x, 1), inv_slope(x**5 + 3 * x, 1), inv_slope(sp.exp(x) + x, 0), inv_slope(x**3, 2)],
     [sp.Rational(1, 5), sp.Rational(1, 8), sp.Rational(1, 2), sp.Rational(1, 12)])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$f(x) = x^3 + 4x - 1$. If $g = f^{-1}$, then $g'(4) =$", [r"$\dfrac17$", r"$\dfrac{1}{52}$", r"$7$", r"$\dfrac14$"], "A",
        r"$f(1) = 4$ and $f'(1) = 7$, so $g'(4) = \frac17$.", why_not={"B": "used $f'(4)$"}),
    MCQ(r"The table gives values of an invertible $f$."
        r"\par\centerline{\begin{tabular}{c|ccc} $x$ & 1 & 2 & 3 \\ \hline $f(x)$ & 3 & 1 & $-2$ \\ $f'(x)$ & $-4$ & $-2$ & $-5$\end{tabular}}"
        r"\par If $g = f^{-1}$, then $g'(1) =$", [r"$-\dfrac14$", r"$-4$", r"$-\dfrac12$", r"$-2$"], "C",
        r"$f(2) = 1$, so $g'(1) = \dfrac{1}{f'(2)} = -\dfrac12$.", why_not={"A": "used $f'(1)$"}),
    MCQ(r"$f(x) = \ln x + x$. If $g = f^{-1}$, what is $g'(1)$?", [r"$2$", r"$1$", r"$\dfrac1e$", r"$\dfrac12$"], "D",
        r"$f(1) = 1$ and $f'(1) = 1 + 1 = 2$, so $\frac12$."),
    MCQ(r"$g$ is the inverse of $f(x) = 2x + \cos x$. Which is an equation of the line tangent to $g$ at $x = 1$?",
        [r"$y = \frac12x - \frac12$", r"$y = \frac12(x - 1)$", r"$y = 2(x - 1)$", r"$y - 1 = \frac12x$"], "B",
        r"$f(0) = 1$, so $g(1) = 0$. $f'(0) = 2 - \sin 0 = 2$, so $g'(1) = \frac12$: $y = \frac12(x - 1)$.",
        why_not={"C": "used $f'$ instead of its reciprocal"}),
]
same("m", [inv_slope(x**3 + 4 * x - 1, 1), inv_slope(sp.log(x) + x, 1), inv_slope(2 * x + sp.cos(x), 0)],
     [sp.Rational(1, 7), sp.Rational(1, 2), sp.Rational(1, 2)])

FRQS = [
    FRQ("An inverse from a table", (
        r"The function $f$ is differentiable and increasing. Selected values are given."
        r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $x$ & $0$ & $1$ & $3$ & $4$ \\ \hline $f(x)$ & $1$ & $3$ & $4$ & $8$ \\ "
        r"$f'(x)$ & $2$ & $\frac12$ & $\frac14$ & $5$\end{tabular}}"
        r"\par Let $g$ be the inverse of $f$."), [
        Part("a", r"Find $g(3)$ and $g'(3)$. Enter $g'(3)$.", num(2),
             r"$f(1) = 3$, so $g(3) = 1$ and $g'(3) = \dfrac{1}{f'(1)} = 2$.", [(1, "$g(3) = 1$"), (1, "$g'(3) = 2$")], work="2cm"),
        Part("b", r"Write an equation for the line tangent to the graph of $g$ at $x = 4$.", expr("4*x - 13"),
             r"$f(3) = 4$, so $g(4) = 3$ and $g'(4) = \dfrac{1}{f'(3)} = 4$. The line is $y - 3 = 4(x - 4)$.", [(1, "point"), (1, "slope and equation")],
             work="2.2cm"),
        Part("c", r"Let $k(x) = \big[f(x)\big]^2$. Find $k'(4)$.", num(80),
             r"By the chain rule, $2f(4)f'(4) = 2(8)(5) = 80$.", [(1, "chain rule and value")], work="1.8cm"),
    ], frq_type="Table of values / rates"),
]
same("frq", [sp.Rational(1, 1) / sp.Rational(1, 2), 1 / sp.Rational(1, 4), 2 * 8 * 5, sp.expand(3 + 4 * (x - 4))], [2, 4, 80, 4 * x - 13])

TOPIC = Topic(
    number="3.3", title="Differentiating Inverse Functions",
    unit="Unit 3: Differentiation: Composite, Implicit, and Inverse Functions", ced=["FUN-3.E", "FUN-3.E.1"],
    goals=r"Find the derivative of an inverse function at a point, from a formula, a table or a tangent line.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
