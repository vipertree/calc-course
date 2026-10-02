"""Unit 3 test: Differentiation: Composite, Implicit, and Inverse Functions. AP format: 12 MCQ (no calculator),
4 MCQ (calculator), 3 FRQ. Two forms (A and B) for every slot.

Covers 3.1-3.6. Choices are built by `pick`, which puts the keyed answer at a planned letter, so a key can't drift from its
choices. Every keyed value is checked with sympy.
"""
import sympy as sp

from calclib import FRQ, MCQ, Part, UnitTest, Variants, check, close, expr, num, same, selfcheck

x, y, t = sp.symbols("x y t")
pi = sp.pi


def D(e, v=x, n=1):
    return sp.simplify(sp.diff(e, v, n))


def imp(F):
    return sp.simplify(-sp.diff(F, x) / sp.diff(F, y))


def pick(stem, right, wrong, letter, solution, why=None, calc=False):
    """MCQ with the correct choice placed at `letter`. `wrong` is three distractors, keyed by why-text if given."""
    k = "ABCD".index(letter)
    choices = list(wrong)
    choices.insert(k, right)
    why_not = {}
    if why:
        for text, reason in why.items():
            why_not["ABCD"[choices.index(text)]] = reason
    return MCQ(stem, choices, letter, solution, why_not=why_not, calc=calc)


A = [
    Variants(
        pick(r"If $f(x) = \left(x^2 + 1\right)^4$, then $f'(1) =$", r"$64$", [r"$16$", r"$32$", r"$128$"], "B",
             r"$4\left(x^2+1\right)^3\cdot 2x = 4(8)(2) = 64$.", {r"$32$": "forgot the inside derivative"}),
        pick(r"If $f(x) = (3x - 1)^5$, then $f'(1) =$", r"$240$", [r"$80$", r"$48$", r"$405$"], "A",
             r"$5(3x-1)^4\cdot 3 = 5(16)(3) = 240$.", {r"$80$": "forgot the inside derivative"}),
    ),
    Variants(
        pick(r"$\dfrac{d}{dx}\sin\left(x^2\right) =$", r"$2x\cos\left(x^2\right)$", [r"$\cos\left(x^2\right)$", r"$-2x\sin\left(x^2\right)$", r"$2\cos(2x)$"], "C",
             r"Outside $\sin$, inside $x^2$: $\cos\left(x^2\right)\cdot 2x$.", {r"$\cos\left(x^2\right)$": "forgot the inside derivative"}),
        pick(r"$\dfrac{d}{dx}e^{\cos x} =$", r"$-\sin x\,e^{\cos x}$", [r"$e^{\cos x}$", r"$\sin x\,e^{\cos x}$", r"$e^{-\sin x}$"], "D",
             r"$e^{\cos x}\cdot(-\sin x)$.", {r"$e^{\cos x}$": "forgot the inside derivative"}),
    ),
    Variants(
        pick(r"$f(2) = 3$, $f'(2) = -1$, $g(3) = 4$, $g'(3) = 5$ and $g'(2) = 6$. If $h(x) = g\big(f(x)\big)$, then $h'(2) =$",
             r"$-5$", [r"$-6$", r"$5$", r"$-4$"], "A", r"$g'\big(f(2)\big)f'(2) = g'(3)(-1) = -5$.", {r"$-6$": "used $g'(2)$"}),
        pick(r"$f(1) = 4$, $f'(1) = 2$, $g(4) = 0$, $g'(4) = -3$ and $g'(1) = 7$. If $h(x) = g\big(f(x)\big)$, then $h'(1) =$",
             r"$-6$", [r"$14$", r"$0$", r"$-3$"], "C", r"$g'\big(f(1)\big)f'(1) = g'(4)(2) = -6$.", {r"$14$": "used $g'(1)$", r"$0$": "that's $h(1)$"}),
    ),
    Variants(
        pick(r"For $x^2 + 3xy + y^2 = 11$, the slope at $(1, 2)$ is", r"$-\dfrac87$", [r"$-\dfrac78$", r"$\dfrac87$", r"$-2$"], "D",
             r"$y' = -\dfrac{2x + 3y}{3x + 2y} = -\dfrac{8}{7}$.", {r"$-\dfrac78$": "inverted"}),
        pick(r"For $x^2y + y^3 = 10$, the slope at $(1, 2)$ is", r"$-\dfrac{4}{13}$", [r"$-\dfrac{13}{4}$", r"$\dfrac{4}{13}$", r"$-4$"], "B",
             r"$2xy + x^2y' + 3y^2y' = 0$, so $y' = -\dfrac{2xy}{x^2 + 3y^2} = -\dfrac{4}{13}$.", {r"$-\dfrac{13}{4}$": "inverted"}),
    ),
    Variants(
        pick(r"$f(x) = x^3 + 2x + 1$. If $g = f^{-1}$, then $g'(4) =$", r"$\dfrac15$", [r"$\dfrac{1}{50}$", r"$5$", r"$\dfrac14$"], "B",
             r"$f(1) = 4$ and $f'(1) = 5$.", {r"$\dfrac{1}{50}$": "used $f'(4)$", r"$5$": "forgot the reciprocal"}),
        pick(r"$f(x) = x^5 + x - 1$. If $g = f^{-1}$, then $g'(1) =$", r"$\dfrac16$", [r"$6$", r"$1$", r"$\dfrac15$"], "D",
             r"$f(1) = 1$ and $f'(1) = 6$.", {r"$6$": "forgot the reciprocal"}),
    ),
    Variants(
        pick(r"If $f(x) = \arctan(2x)$, then $f'\!\left(\tfrac12\right) =$", r"$1$", [r"$\dfrac12$", r"$\dfrac\pi4$", r"$2$"], "A",
             r"$\dfrac{2}{1 + 4x^2} = \dfrac22 = 1$.", {r"$\dfrac\pi4$": "that's $f\\left(\\frac12\\right)$", r"$\dfrac12$": "forgot the chain rule"}),
        pick(r"If $f(x) = \arcsin\left(\tfrac x2\right)$, then $f'(1) =$", r"$\dfrac{1}{\sqrt3}$", [r"$\dfrac{2}{\sqrt3}$", r"$\dfrac\pi6$", r"$\dfrac12$"], "C",
             r"$\dfrac{1/2}{\sqrt{1 - 1/4}} = \dfrac{1}{\sqrt3}$.", {r"$\dfrac{2}{\sqrt3}$": "forgot the chain rule", r"$\dfrac\pi6$": "that's $f(1)$"}),
    ),
    Variants(
        pick(r"If $y = xe^x$, then $y''(0) =$", r"$2$", [r"$1$", r"$0$", r"$e$"], "C", r"$y'' = 2e^x + xe^x = 2$ at $0$.", {r"$1$": "that's $y'(0)$"}),
        pick(r"If $y = \cos(2x)$, then $y''(0) =$", r"$-4$", [r"$-2$", r"$4$", r"$0$"], "A", r"$y'' = -4\cos(2x) = -4$ at $0$.", {r"$-2$": "chain rule applied once"}),
    ),
    Variants(
        pick(r"For $x^2 + y^2 = 9$, $\dfrac{d^2y}{dx^2} =$", r"$-\dfrac{9}{y^3}$", [r"$-\dfrac xy$", r"$\dfrac{9}{y^3}$", r"$-\dfrac{1}{y}$"], "D",
             r"$y' = -\frac xy$; then $y'' = -\dfrac{x^2 + y^2}{y^3} = -\dfrac{9}{y^3}$.", {r"$-\dfrac xy$": "that's $y'$"}),
        pick(r"For $x^2 + 4y^2 = 4$, $\dfrac{d^2y}{dx^2} =$", r"$-\dfrac{1}{4y^3}$", [r"$-\dfrac{x}{4y}$", r"$\dfrac{1}{4y^3}$", r"$-\dfrac{4}{y^3}$"], "B",
             r"$y' = -\frac{x}{4y}$; then $y'' = -\dfrac{4y^2 + x^2}{16y^3} = -\dfrac{4}{16y^3}$.", {r"$-\dfrac{x}{4y}$": "that's $y'$"}),
    ),
    Variants(
        pick(r"An invertible $g$ has $g(2) = 5$ and $g'(2) = \frac34$. Then $\left(g^{-1}\right)'(5) =$", r"$\dfrac43$", [r"$\dfrac34$", r"$\dfrac25$", r"$-\dfrac43$"], "B",
             r"$\dfrac{1}{3/4} = \dfrac43$.", {r"$\dfrac34$": "forgot the reciprocal"}),
        pick(r"An invertible $g$ has $g(0) = 3$ and $g'(0) = -2$. Then $\left(g^{-1}\right)'(3) =$", r"$-\dfrac12$", [r"$-2$", r"$\dfrac13$", r"$\dfrac12$"], "D",
             r"$\dfrac{1}{-2} = -\dfrac12$.", {r"$-2$": "forgot the reciprocal"}),
    ),
    Variants(
        pick(r"A particle's position is $s(t) = t^3 - 6t^2 + 5$. Its acceleration at $t = 1$ is", r"$-6$", [r"$-9$", r"$0$", r"$6$"], "A",
             r"$a = 6t - 12 = -6$ at $t = 1$.", {r"$-9$": "that's the velocity"}),
        pick(r"A particle's position is $s(t) = 2t^3 - 3t^2$. Its acceleration at $t = 2$ is", r"$18$", [r"$12$", r"$4$", r"$24$"], "C",
             r"$a = 12t - 6 = 18$ at $t = 2$.", {r"$12$": "that's the velocity", r"$4$": "that's the position"}),
    ),
    Variants(
        pick(r"If $y = \ln(\sin x)$, then $y'\!\left(\tfrac\pi4\right) =$", r"$1$", [r"$\sqrt2$", r"$0$", r"$-1$"], "C",
             r"$\dfrac{\cos x}{\sin x} = \cot\frac\pi4 = 1$."),
        pick(r"If $y = \ln(\cos x)$, then $y'\!\left(\tfrac\pi3\right) =$", r"$-\sqrt3$", [r"$\sqrt3$", r"$-\dfrac{1}{\sqrt3}$", r"$2$"], "B",
             r"$\dfrac{-\sin x}{\cos x} = -\tan\frac\pi3 = -\sqrt3$.", {r"$\sqrt3$": "lost the minus sign"}),
    ),
    Variants(
        pick(r"$f(2) = -1$ and $f'(2) = 4$. The derivative of $\big[f(x)\big]^3$ at $x = 2$ is", r"$12$", [r"$-12$", r"$48$", r"$3$"], "D",
             r"$3f(2)^2 f'(2) = 3(1)(4) = 12$.", {r"$-12$": "sign of $(-1)^2$", r"$48$": "used $f'(2)^2$"}),
        pick(r"$f(0) = 0$ and $f'(0) = 5$. The derivative of $e^{f(x)}$ at $x = 0$ is", r"$5$", [r"$1$", r"$e^5$", r"$0$"], "A",
             r"$e^{f(0)}f'(0) = 1\cdot 5 = 5$.", {r"$1$": "forgot the inside derivative"}),
    ),
]
same("A1", [D((x**2 + 1)**4).subs(x, 1), D((3 * x - 1)**5).subs(x, 1)], [64, 240])
same("A4", [(x**2 + 3 * x * y + y**2).subs({x: 1, y: 2}), imp(x**2 + 3 * x * y + y**2 - 11).subs({x: 1, y: 2}),
            (x**2 * y + y**3).subs({x: 1, y: 2}), imp(x**2 * y + y**3 - 10).subs({x: 1, y: 2})], [11, sp.Rational(-8, 7), 10, sp.Rational(-4, 13)])
same("A5", [(x**3 + 2 * x + 1).subs(x, 1), 1 / D(x**3 + 2 * x + 1).subs(x, 1), (x**5 + x - 1).subs(x, 1), 1 / D(x**5 + x - 1).subs(x, 1)],
     [4, sp.Rational(1, 5), 1, sp.Rational(1, 6)])
same("A6", [D(sp.atan(2 * x)).subs(x, sp.Rational(1, 2)), D(sp.asin(x / 2)).subs(x, 1)], [1, 1 / sp.sqrt(3)])
same("A7", [D(x * sp.exp(x), n=2).subs(x, 0), D(sp.cos(2 * x), n=2).subs(x, 0)], [2, -4])
same("A10", [D(t**3 - 6 * t**2 + 5, t, 2).subs(t, 1), D(2 * t**3 - 3 * t**2, t, 2).subs(t, 2)], [-6, 18])
same("A11", [D(sp.log(sp.sin(x))).subs(x, pi / 4), D(sp.log(sp.cos(x))).subs(x, pi / 3)], [1, -sp.sqrt(3)])

B = [
    Variants(
        pick(r"If $f(x) = \sqrt{x^3 + 1}\,\sin x$, then $f'(2)$ is closest to", r"$0.570$", [r"$-1.248$", r"$2.728$", r"$1.817$"], "A",
             r"A numerical derivative gives about $0.570$.", calc=True),
        pick(r"If $f(x) = \ln\left(x^2 + 3\right)\cos x$, then $f'(1)$ is closest to", r"$-0.896$", [r"$0.270$", r"$-1.166$", r"$0.749$"], "D",
             r"A numerical derivative gives about $-0.896$.", calc=True),
    ),
    Variants(
        pick(r"$g$ is the inverse of $f(x) = x^3 + e^x$. Then $g'(2)$ is closest to", r"$0.353$", [r"$0.587$", r"$2.831$", r"$0.137$"], "C",
             r"Solve $f(a) = 2$: $a \approx 0.5867$. Then $g'(2) = \dfrac{1}{3a^2 + e^a} \approx 0.353$.", {r"$0.587$": "that's $g(2)$"}, calc=True),
        pick(r"$g$ is the inverse of $f(x) = x + e^{x/2}$. Then $g'(3)$ is closest to", r"$0.525$", [r"$1.188$", r"$1.906$", r"$0.333$"], "B",
             r"Solve $f(a) = 3$: $a \approx 1.188$. Then $g'(3) = \dfrac{1}{1 + \frac12e^{a/2}} \approx 0.525$.", {r"$1.188$": "that's $g(3)$"}, calc=True),
    ),
    Variants(
        pick(r"A particle's position is $s(t) = \sin\left(t^2\right)$. Its acceleration at $t = 1.5$ is closest to", r"$-8.259$",
             [r"$-1.884$", r"$0.778$", r"$-4.130$"], "B", r"$s''(t) = 2\cos\left(t^2\right) - 4t^2\sin\left(t^2\right)$; at $1.5$ that's about $-8.259$.", calc=True),
        pick(r"A particle's position is $s(t) = e^{-t}\cos(2t)$. Its acceleration at $t = 1$ is closest to", r"$1.797$",
             [r"$-0.153$", r"$0.511$", r"$-1.797$"], "A", r"A numerical second derivative gives about $1.797$.", calc=True),
    ),
    Variants(
        pick(r"The slope of $y = \arcsin\left(x^2\right)$ at $x = 0.6$ is closest to", r"$1.286$", [r"$0.643$", r"$0.368$", r"$1.200$"], "D",
             r"$\dfrac{2x}{\sqrt{1 - x^4}} \approx 1.286$ at $x = 0.6$.", {r"$0.643$": "forgot the chain rule"}, calc=True),
        pick(r"The slope of $y = \arctan\left(e^x\right)$ at $x = 0.5$ is closest to", r"$0.443$", [r"$1.649$", r"$0.269$", r"$0.976$"], "C",
             r"$\dfrac{e^x}{1 + e^{2x}} \approx 0.443$ at $x = 0.5$.", calc=True),
    ),
]
close("B13", D(sp.sqrt(x**3 + 1) * sp.sin(x)).subs(x, 2), 0.570, 5e-4)
close("B13b", D(sp.log(x**2 + 3) * sp.cos(x)).subs(x, 1), -0.896, 5e-4)
a14 = sp.nsolve(x**3 + sp.exp(x) - 2, x, 0.5)
b14 = sp.nsolve(x + sp.exp(x / 2) - 3, x, 1)
close("B14", 1 / (3 * a14**2 + sp.exp(a14)), 0.353, 5e-4)
close("B14b", 1 / (1 + sp.exp(b14 / 2) / 2), 0.525, 5e-4)
close("B15", sp.diff(sp.sin(t**2), t, 2).subs(t, 1.5), -8.259, 5e-4)
close("B15b", sp.diff(sp.exp(-t) * sp.cos(2 * t), t, 2).subs(t, 1), 1.797, 5e-4)
close("B16", D(sp.asin(x**2)).subs(x, 0.6), 1.286, 5e-4)
close("B16b", D(sp.atan(sp.exp(x))).subs(x, 0.5), 0.443, 5e-4)


# ================================================================ free response
def table_chain(v, c1, c2, c3):
    """v: {x: (f, f', g, g')}, f increasing. h = f(g(x)) at c1, tangent to k = g(f(x)) at c2, m = g^2 at c3, (f^-1)'(f(c3))."""
    xs = sorted(v)
    rows = " \\\\ ".join(f"${c}$ & ${v[c][0]}$ & ${v[c][1]}$ & ${v[c][2]}$ & ${v[c][3]}$" for c in xs)
    g1 = v[c1][2]
    hp = v[g1][1] * v[c1][3]
    f2 = v[c2][0]
    k2, kp = v[f2][2], v[f2][3] * v[c2][1]
    line = sp.expand(k2 + kp * (x - c2))
    mp = 2 * v[c3][2] * v[c3][3]
    finv = sp.Rational(1, v[c3][1])
    frq = FRQ("Composite and inverse functions from a table", (
        r"The functions $f$ and $g$ are differentiable for all real numbers, and $f$ is strictly increasing. The table gives values "
        r"of the functions and their derivatives at selected values of $x$. Let $f^{-1}$ be the inverse function of $f$."
        r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $x$ & $f(x)$ & $f'(x)$ & $g(x)$ & $g'(x)$ \\ \hline " + rows + r"\end{tabular}}"), [
        Part("a", rf"Let $h$ be the function defined by $h(x) = f\big(g(x)\big)$. Find $h'({c1})$. Show the work that leads to your answer.", num(hp),
             rf"$h'({c1}) = f'\big(g({c1})\big)g'({c1}) = f'({g1})\cdot({v[c1][3]}) = ({v[g1][1]})({v[c1][3]}) = {hp}$.", [(1, "chain rule"), (1, f"answer ${hp}$")], work="2.2cm"),
        Part("b", rf"Let $k$ be the function defined by $k(x) = g\big(f(x)\big)$. Write an equation for the line tangent to the graph of $k$ at $x = {c2}$.", expr(str(line)),
             rf"$k({c2}) = g\big(f({c2})\big) = g({f2}) = {k2}$, and $k'({c2}) = g'({f2})f'({c2}) = ({v[f2][3]})({v[c2][1]}) = {kp}$. "
             rf"The tangent line is $y = {k2} + {kp}(x - {c2})$.", [(1, f"$k({c2}) = {k2}$"), (1, f"$k'({c2}) = {kp}$"), (1, "tangent line equation")], work="2.6cm"),
        Part("c", rf"Let $m$ be the function defined by $m(x) = \big[g(x)\big]^2$. Find $m'({c3})$.", num(mp),
             rf"$m'({c3}) = 2g({c3})g'({c3}) = 2({v[c3][2]})({v[c3][3]}) = {mp}$.", [(1, "chain rule and value")], work="1.6cm"),
        Part("d", rf"Find $\left(f^{{-1}}\right)'({v[c3][0]})$. Show the work that leads to your answer.", num(finv),
             rf"$f({c3}) = {v[c3][0]}$, so $\left(f^{{-1}}\right)'({v[c3][0]}) = \dfrac{{1}}{{f'({c3})}} = {sp.latex(finv)}$.",
             [(1, "$f^{-1}$ evaluated at the matching point, and the reciprocal")], work="1.8cm"),
    ], frq_type="Derivatives from a table")
    return frq, [hp, line, mp, finv]


F1A, cA = table_chain({1: (2, 3, 3, -2), 2: (3, 4, 1, 5), 3: (6, 2, 2, 1)}, 1, 2, 3)
F1B, cB = table_chain({0: (1, 3, 2, -1), 1: (2, 2, 0, 4), 2: (4, 5, 1, 3)}, 0, 1, 2)
same("F1 A", cA, [-4, 4 * x - 6, 4, sp.Rational(1, 2)])
same("F1 B", cB, [-5, 6 * x - 5, 6, sp.Rational(1, 5)])


def curve_frq(F, tex, dydx_tex, pt, sign):
    """Implicit curve F = 0: dy/dx, tangent at pt, horizontal tangents, y'' where y' = 0."""
    yp = imp(F)
    slope = yp.subs({x: pt[0], y: pt[1]})
    line = sp.expand(pt[1] + slope * (x - pt[0]))
    num_ = sp.numer(sp.together(yp))
    hz = [s_ for s_ in sp.solve([num_, F], [x, y], dict=True)]
    hz_pos = [h for h in hz if h[y] > 0][0]
    Y = sp.Function("Y")(x)
    ypp = sp.diff(yp.subs(y, Y), x).subs(sp.Derivative(Y, x), yp.subs(y, Y)).subs(Y, y)
    ypp_val = sp.simplify(ypp.subs({x: hz_pos[x], y: hz_pos[y]}))
    frq = FRQ("An implicitly defined curve", rf"Consider the curve given by the equation ${tex}$.", [
        Part("a", rf"Show that $\dfrac{{dy}}{{dx}} = {dydx_tex}$.", selfcheck(dydx_tex),
             r"Differentiate implicitly, using the product rule on the $xy$ term and the chain rule on each $y$ term, then solve for $\frac{dy}{dx}$.",
             [(1, "implicit differentiation"), (1, "solves for $\\frac{dy}{dx}$")], work="2.6cm"),
        Part("b", rf"Write an equation for the line tangent to the curve at the point $({pt[0]}, {pt[1]})$.", expr(str(line)),
             rf"The slope there is ${sp.latex(slope)}$, so the tangent line is $y = {pt[1]} + {sp.latex(slope)}(x - ({pt[0]}))$.", [(1, "slope"), (1, "tangent line equation")], work="2.2cm"),
        Part("c", r"Find the coordinates of all points on the curve at which the line tangent to the curve is horizontal.",
             selfcheck(r"\text{ and }".join(f"({h[x]}, {h[y]})" for h in hz)),
             r"Set the numerator of $\frac{dy}{dx}$ to $0$, substitute into the curve, and solve: the points are "
             + " and ".join(f"$({h[x]}, {h[y]})$" for h in hz) + ". At each, the denominator of $\\frac{dy}{dx}$ is not $0$.",
             [(1, "sets the numerator of $\\frac{dy}{dx}$ equal to $0$"), (1, "substitutes into the equation of the curve"), (1, "both points")], work="3cm"),
        Part("d", rf"Find the value of $\dfrac{{d^2y}}{{dx^2}}$ at the point $({hz_pos[x]}, {hz_pos[y]})$. Does the curve have a relative minimum, "
                  r"a relative maximum, or neither at this point? Justify your answer.", num(ypp_val),
             rf"Differentiate $\frac{{dy}}{{dx}}$ with the quotient rule. At $({hz_pos[x]}, {hz_pos[y]})$, $\frac{{dy}}{{dx}} = 0$, which simplifies the work: "
             rf"$\dfrac{{d^2y}}{{dx^2}} = {sp.latex(ypp_val)}$. Since $\dfrac{{dy}}{{dx}} = 0$ and $\dfrac{{d^2y}}{{dx^2}} {'<' if ypp_val < 0 else '>'} 0$ "
             rf"there, the curve has a relative {'maximum' if ypp_val < 0 else 'minimum'} at $({hz_pos[x]}, {hz_pos[y]})$.",
             [(1, "value of $\\frac{d^2y}{dx^2}$"), (1, "classification with justification")], work="3.4cm"),
    ], frq_type="Implicit differentiation")
    return frq, [yp, line, hz_pos[y], ypp_val]


F2A, dA = curve_frq(x**2 - x * y + y**2 - 3, r"x^2 - xy + y^2 = 3", r"\dfrac{y - 2x}{2y - x}", (-1, 1), 1)
F2B, dB = curve_frq(x**2 + x * y + y**2 - 3, r"x^2 + xy + y^2 = 3", r"-\dfrac{2x + y}{x + 2y}", (1, 1), 1)
same("F2 A", dA[1:], [x + 2, 2, sp.Rational(-2, 3)])
same("F2 B", dB[1:], [2 - x, 2, sp.Rational(-2, 3)])
same("F2 forms", [sp.simplify(dA[0] - (y - 2 * x) / (2 * y - x)), sp.simplify(dB[0] + (2 * x + y) / (x + 2 * y))], [0, 0])


def motion_frq(s, T, t_a):
    v, a = sp.expand(sp.diff(s, t)), sp.expand(sp.diff(s, t, 2))
    rest = sorted(sp.solve(v, t))
    t0 = sp.solve(a, t)[0]
    frq = FRQ("Position, velocity and acceleration", (
        rf"A particle moves along the $x$-axis so that its position at time $t$ is given by $s(t) = {sp.latex(s)}$, where $s(t)$ is "
        rf"measured in meters and $t$ is measured in seconds, for $0 \le t \le {T}$."), [
        Part("a", r"Find the acceleration $a(t)$ of the particle at time $t$.", expr(str(a), var="t"),
             rf"$v(t) = {sp.latex(v)}$ and $a(t) = {sp.latex(a)}$.", [(1, "velocity"), (1, "acceleration")], work="2cm"),
        Part("b", rf"Find $a({t_a})$. Is the velocity of the particle increasing or decreasing at time $t = {t_a}$? Give a reason for your answer.", num(a.subs(t, t_a)),
             rf"$a({t_a}) = {a.subs(t, t_a)}$, which is negative, so the velocity is decreasing.", [(1, "value"), (1, "decreasing, because $a < 0$")], work="1.8cm"),
        Part("c", r"Find all times $t$ at which the particle is at rest.", selfcheck(rf"t = {rest[0]} \text{{ and }} t = {rest[1]}"),
             rf"$v(t) = 0$ at $t = {rest[0]}$ and $t = {rest[1]}$.", [(1, "sets $v = 0$"), (1, "both times")], work="2cm"),
        Part("d", r"Find the velocity of the particle at the time when its acceleration is $0$.", num(v.subs(t, t0)),
             rf"$a(t) = 0$ at $t = {sp.latex(t0)}$, and $v({sp.latex(t0)}) = {sp.latex(v.subs(t, t0))}$ meters per second.", [(1, "time when $a(t) = 0$"), (1, "velocity")], work="2cm"),
    ], frq_type="Particle motion")
    return frq, [a, a.subs(t, t_a), rest, v.subs(t, t0)]


F3A, mA = motion_frq(t**3 - 6 * t**2 + 9 * t + 1, 5, 1)
F3B, mB = motion_frq(2 * t**3 - 15 * t**2 + 24 * t, 6, 1)
same("F3 A", mA, [6 * t - 12, -6, [1, 3], -3])
same("F3 B", mB, [12 * t - 30, -18, [1, 4], sp.Rational(-27, 2)])

TEST = UnitTest(unit=3, title="Differentiation: Composite, Implicit, and Inverse Functions", mcq_a=A, mcq_b=B,
                frq=[Variants(F1A, F1B), Variants(F2A, F2B), Variants(F3A, F3B)])
