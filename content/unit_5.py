"""Unit 5 test: Analytical Applications of Differentiation. AP format: 12 MCQ (no calculator), 4 MCQ (calculator), 3 FRQ.
Two forms (A and B) for every slot.

Covers 5.1-5.12. Choices are built by `pick`, which puts the keyed answer at a planned letter, so a key can't drift from its
choices. Every keyed value is checked with sympy.
"""
import sympy as sp

from calclib import FRQ, MCQ, Part, UnitTest, Variants, close, expr, num, same, selfcheck

x, y = sp.symbols("x y", real=True)
pi = sp.pi


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


def mvt_c(f, a, b):
    m = (f.subs(x, b) - f.subs(x, a)) / (b - a)
    return sorted(c for c in sp.solve(sp.diff(f, x) - m, x) if c.is_real and a < c < b)


def extremes(f, a, b):
    cs = [c for c in sp.solveset(sp.diff(f, x), x, sp.Interval.open(a, b))] + [a, b]
    vals = [sp.simplify(f.subs(x, c)) for c in cs]
    return max(vals, key=float), min(vals, key=float)


A = [
    Variants(
        pick(r"The value of $c$ guaranteed by the Mean Value Theorem for $f(x) = x^2 - 4x$ on $[1, 5]$ is", r"$3$", [r"$2$", r"$\frac52$", r"$4$"], "C",
             r"Average rate $\frac{5 - (-3)}{4} = 2$; $2c - 4 = 2$ at $c = 3$.", {r"$2$": "that's the average rate"}),
        pick(r"The value of $c$ guaranteed by the Mean Value Theorem for $f(x) = x^2 + 2x$ on $[0, 4]$ is", r"$2$", [r"$6$", r"$1$", r"$3$"], "A",
             r"Average rate $\frac{24 - 0}{4} = 6$; $2c + 2 = 6$ at $c = 2$.", {r"$6$": "that's the average rate"}),
    ),
    Variants(
        pick(r"For which function on $[-1, 1]$ does the Mean Value Theorem NOT apply?", r"$f(x) = |x|$", [r"$f(x) = x^3$", r"$f(x) = e^x$", r"$f(x) = \cos x$"], "D",
             r"$|x|$ has a corner at $0$: not differentiable on $(-1, 1)$."),
        pick(r"For which function on $[0, 2]$ does the Mean Value Theorem NOT apply?", r"$f(x) = \frac{1}{x - 1}$", [r"$f(x) = x^2$", r"$f(x) = \sqrt{x + 1}$", r"$f(x) = \sin x$"], "B",
             r"Not continuous at $1$."),
    ),
    Variants(
        pick(r"The critical points of $f(x) = x^3 - 12x + 4$ are", r"$x = -2, 2$", [r"$x = 0$ only", r"$x = -4, 4$", r"$x = 2$ only"], "A", r"$f'(x) = 3x^2 - 12 = 0$."),
        pick(r"The critical points of $f(x) = x^3 - 3x^2 - 9x$ are", r"$x = -1, 3$", [r"$x = 1, -3$", r"$x = 0, 3$", r"$x = 3$ only"], "C", r"$f'(x) = 3(x - 3)(x + 1) = 0$."),
    ),
    Variants(
        pick(r"$f(x) = x^4 - 8x^2$ is increasing on", r"$(-2, 0)$ and $(2, \infty)$", [r"$(0, 2)$ only", r"$(-\infty, -2)$ and $(0, 2)$", r"$(2, \infty)$ only"], "B",
             r"$f'(x) = 4x(x - 2)(x + 2)$: signs $-, +, -, +$."),
        pick(r"$f(x) = x^4 - 2x^2$ is decreasing on", r"$(-\infty, -1)$ and $(0, 1)$", [r"$(-1, 0)$ and $(1, \infty)$", r"$(-1, 1)$", r"$(0, 1)$ only"], "D",
             r"$f'(x) = 4x(x - 1)(x + 1)$: signs $-, +, -, +$."),
    ),
    Variants(
        pick(r"$f'(x) = (x + 1)(x - 3)^2$. $f$ has a relative minimum at", r"$x = -1$ only", [r"$x = 3$ only", r"$x = -1$ and $x = 3$", r"no $x$"], "A",
             r"$f'$ changes from $-$ to $+$ at $-1$; no sign change at $3$."),
        pick(r"$f'(x) = (x - 2)(x + 4)^2$. $f$ has a relative minimum at", r"$x = 2$ only", [r"$x = -4$ only", r"$x = 2$ and $x = -4$", r"no $x$"], "C",
             r"$f'$ changes from $-$ to $+$ at $2$; no sign change at $-4$."),
    ),
    Variants(
        pick(r"The absolute maximum value of $f(x) = x^3 - 3x$ on $[0, 2]$ is", r"$2$", [r"$0$", r"$-2$", r"$1$"], "D", r"Candidates $f(0) = 0$, $f(1) = -2$, $f(2) = 2$.",
             {r"$-2$": "that's the minimum"}),
        pick(r"The absolute minimum value of $f(x) = x^3 - 3x^2$ on $[-1, 3]$ is", r"$-4$", [r"$0$", r"$-2$", r"$2$"], "B", r"Candidates $f(-1) = -4$, $f(0) = 0$, $f(2) = -4$, $f(3) = 0$."),
    ),
    Variants(
        pick(r"The graph of $f(x) = x^3 - 6x^2 + 1$ is concave down on", r"$(-\infty, 2)$", [r"$(2, \infty)$", r"$(0, 4)$", r"$(-\infty, 0)$"], "A", r"$f''(x) = 6x - 12 < 0$ for $x < 2$."),
        pick(r"The graph of $f(x) = x^3 + 3x^2 - 5$ is concave up on", r"$(-1, \infty)$", [r"$(-\infty, -1)$", r"$(-2, 0)$", r"$(0, \infty)$"], "C", r"$f''(x) = 6x + 6 > 0$ for $x > -1$."),
    ),
    Variants(
        pick(r"The points of inflection of $f(x) = x^4 - 6x^2$ are at", r"$x = \pm 1$", [r"$x = 0$", r"$x = \pm\sqrt3$", r"$x = 0, \pm\sqrt3$"], "B", r"$f''(x) = 12x^2 - 12$ changes sign at $\pm 1$.",
             {r"$x = 0, \pm\sqrt3$": "those are the critical points"}),
        pick(r"$f''(x) = x^2(x - 2)$. How many points of inflection does $f$ have?", r"$1$", [r"$0$", r"$2$", r"$3$"], "B", r"$f''$ changes sign only at $2$."),
    ),
    Variants(
        pick(r"$f'(3) = 0$ and $f''(3) = -2$. At $x = 3$, $f$ has", r"a relative maximum", [r"a relative minimum", r"a point of inflection", r"no conclusion possible"], "D",
             r"Second Derivative Test: concave down at a horizontal tangent."),
        pick(r"$f'(-1) = 0$ and $f''(-1) = 5$. At $x = -1$, $f$ has", r"a relative minimum", [r"a relative maximum", r"a point of inflection", r"no conclusion possible"], "D",
             r"Second Derivative Test: concave up at a horizontal tangent."),
    ),
    Variants(
        pick(r"The graph of $f'$ has a relative maximum at $x = 2$. Then the graph of $f$ has", r"a point of inflection at $x = 2$",
             [r"a relative maximum at $x = 2$", r"a relative minimum at $x = 2$", r"a horizontal tangent at $x = 2$"], "C", r"$f'$ changes from increasing to decreasing: concavity changes."),
        pick(r"On $(0, 3)$, $f'$ is negative and increasing. On $(0, 3)$, $f$ is", r"decreasing and concave up", [r"increasing and concave up", r"decreasing and concave down", r"increasing and concave down"], "A",
             r"$f' < 0$: decreasing. $f'$ increasing: concave up."),
    ),
    Variants(
        pick(r"Two positive numbers have sum $14$. The largest possible product is", r"$49$", [r"$48$", r"$45$", r"$196$"], "B", r"$x(14 - x)$ is largest at $x = 7$."),
        pick(r"A rectangle has perimeter $32$. Its largest possible area is", r"$64$", [r"$60$", r"$256$", r"$16$"], "A", r"An $8 \times 8$ square."),
    ),
    Variants(
        pick(r"On the curve $x^2 + y^2 - 6y = 16$, the tangent line is horizontal at", r"$(0, 8)$ and $(0, -2)$", [r"$(5, 3)$ and $(-5, 3)$", r"$(0, 3)$", r"$(4, 0)$ and $(-4, 0)$"], "D",
             r"$y' = \frac{x}{3 - y} = 0$ at $x = 0$: $y^2 - 6y - 16 = 0$.", {r"$(5, 3)$ and $(-5, 3)$": "those are the vertical tangents"}),
        pick(r"On the curve $x^2 + y^2 + 4x = 21$, the tangent line is vertical at", r"$(3, 0)$ and $(-7, 0)$", [r"$(-2, 5)$ and $(-2, -5)$", r"$(-2, 0)$", r"$(0, \pm\sqrt{21})$"], "A",
             r"$y' = -\frac{x + 2}{y}$; $y = 0$ gives $x^2 + 4x - 21 = 0$.", {r"$(-2, 5)$ and $(-2, -5)$": "those are the horizontal tangents"}),
    ),
]
same("A1", [mvt_c(x**2 - 4 * x, 1, 5), mvt_c(x**2 + 2 * x, 0, 4)], [[3], [2]])
same("A6", [extremes(x**3 - 3 * x, 0, 2)[0], extremes(x**3 - 3 * x**2, -1, 3)[1]], [2, -4])

B = [
    Variants(
        pick(r"$f(x) = e^{x} - 3x$ on $[0, 2]$. The value of $c$ guaranteed by the Mean Value Theorem is about", r"$1.161$", [r"$1.099$", r"$0.195$", r"$1.000$"], "B",
             r"Average rate $\frac{e^2 - 6 - 1}{2} \approx 0.195$; $e^c - 3 = 0.195$ gives $c \approx 1.161$.", {r"$0.195$": "that's the average rate"}, calc=True),
        pick(r"$f(x) = \sin(2x)$ on $[0, 1]$. The value of $c$ guaranteed by the Mean Value Theorem is about", r"$0.549$", [r"$0.909$", r"$0.455$", r"$0.785$"], "C",
             r"Average rate $\sin 2 \approx 0.909$; $2\cos(2c) = 0.909$ gives $c \approx 0.549$.", {r"$0.909$": "that's the average rate"}, calc=True),
    ),
    Variants(
        pick(r"$f'(x) = x^3 - 5x + 1$. At about what $x$ does $f$ have a relative maximum?", r"$0.202$", [r"$-2.330$", r"$2.128$", r"$1.291$"], "A",
             r"Roots of $f'$: about $-2.330$, $0.202$, $2.128$; $f'$ goes $-, +, -, +$.", calc=True),
        pick(r"$f'(x) = x^3 - 4x + 2$. At about what $x$ does $f$ have a relative maximum?", r"$0.539$", [r"$-2.214$", r"$1.675$", r"$1.155$"], "D",
             r"Roots of $f'$: about $-2.214$, $0.539$, $1.675$; $f'$ goes $-, +, -, +$.", calc=True),
    ),
    Variants(
        pick(r"The absolute maximum value of $g(x) = x e^{-x/3}$ on $[0, 6]$ is about", r"$1.104$", [r"$0.812$", r"$3.000$", r"$0.717$"], "A",
             r"$g' = \left(1 - \frac x3\right)e^{-x/3} = 0$ at $3$: $g(3) = 3e^{-1} \approx 1.104$; $g(6) \approx 0.812$.", calc=True),
        pick(r"The absolute minimum value of $g(x) = x^2 - 4\ln x$ on $[1, 3]$ is about", r"$0.614$", [r"$1.000$", r"$1.414$", r"$4.606$"], "B",
             r"$g' = 2x - \frac4x = 0$ at $\sqrt2$: $g\left(\sqrt2\right) = 2 - 2\ln 2 \approx 0.614$.", calc=True),
    ),
    Variants(
        pick(r"A closed can must hold $500$ cm$^3$. The radius that uses the least material is about", r"$4.301$ cm", [r"$8.603$ cm", r"$5.642$ cm", r"$3.414$ cm"], "C",
             r"$S = 2\pi r^2 + \frac{1000}{r}$, $S' = 0$ at $r^3 = \frac{250}{\pi}$.", {r"$8.603$ cm": "that's the height"}, calc=True),
        pick(r"A closed can must hold $1000$ cm$^3$. The radius that uses the least material is about", r"$5.419$ cm", [r"$10.839$ cm", r"$7.937$ cm", r"$4.301$ cm"], "D",
             r"$S = 2\pi r^2 + \frac{2000}{r}$, $S' = 0$ at $r^3 = \frac{500}{\pi}$.", {r"$10.839$ cm": "that's the height"}, calc=True),
    ),
]
u = sp.symbols("u")
close("B13", sp.nsolve(sp.exp(u) - 3 - (sp.exp(2) - 7) / 2, u, 1), 1.161, 5e-4)
close("B13b", sp.acos(sp.sin(2) / 2) / 2, 0.549, 5e-4)
close("B14", sorted(sp.Poly(u**3 - 5 * u + 1).nroots())[1], 0.202, 5e-4)
close("B14b", sorted(sp.Poly(u**3 - 4 * u + 2).nroots())[1], 0.539, 5e-4)
close("B15", 3 * sp.exp(-1), 1.104, 5e-4)
close("B15b", 2 - 2 * sp.log(2), 0.614, 5e-4)
close("B16", (250 / sp.pi)**sp.Rational(1, 3), 4.301, 5e-4)
close("B16b", (500 / sp.pi)**sp.Rational(1, 3), 5.419, 5e-4)


# ================================================================ free response
def graph_frq(fp, lo, hi):
    """f'(x) given as a cubic; extrema, concavity, inflection, candidates on [lo, hi] given f(lo)."""
    cs = sorted(sp.solve(fp, x))
    sgn = lambda c: (fp.subs(x, c - sp.Rational(1, 100)) > 0, fp.subs(x, c + sp.Rational(1, 100)) > 0)
    mx = [c for c in cs if sgn(c) == (True, False)]
    mn = [c for c in cs if sgn(c) == (False, True)]
    f2 = sp.diff(fp, x)
    inf = sorted(sp.solve(f2, x), key=float)
    inc = sp.solve_univariate_inequality(fp > 0, x, relational=False)
    cdn = sp.solve_univariate_inequality(f2 < 0, x, relational=False)
    both = inc.intersect(cdn)
    frq = FRQ("Analyzing a function from its derivative", (
        rf"A twice-differentiable function $f$ has derivative $f'(x) = {sp.latex(sp.expand(fp))} = {sp.latex(sp.factor(fp))}$ for all $x$."), [
        Part("a", r"Find the $x$-coordinates of all relative extrema of $f$ and classify each. Justify. Enter the location of the relative maximum.", num(mx[0]),
             rf"$f'$ changes from $+$ to $-$ at $x = {sp.latex(mx[0])}$ (relative maximum)" + "".join(rf"; from $-$ to $+$ at $x = {sp.latex(c)}$ (relative minimum)" for c in mn) + ".",
             [(1, "critical points"), (1, "classification"), (1, "justification with $f'$")], work="2.8cm"),
        Part("b", r"Find the $x$-coordinates of the points of inflection of $f$. Justify. Enter the smaller one.", num(inf[0]),
             rf"$f''(x) = {sp.latex(f2)}$ changes sign at $x = {', '.join(sp.latex(c) for c in inf)}$.", [(1, "$f''$"), (1, "both points with sign change")], work="2.2cm"),
        Part("c", r"On what interval(s) is $f$ both increasing and concave down?", selfcheck(sp.latex(both)),
             rf"Increasing where $f' > 0$: ${sp.latex(inc)}$. Concave down where $f'' < 0$: ${sp.latex(cdn)}$. Both: ${sp.latex(both)}$.", [(1, "interval")], work="2cm"),
    ], frq_type="Analyzing a function")
    return frq, [mx, mn, inf, both]


F1A, gA = graph_frq((x + 1) * (x - 3) * (x - 5), 0, 0)
F1B, gB = graph_frq((x + 2) * (x - 1) * (x - 4), 0, 0)
same("F1 A", [gA[0], gA[1], gA[2]], [[3], [-1, 5], [sp.Rational(7, 3) - 2 * sp.sqrt(7) / 3, sp.Rational(7, 3) + 2 * sp.sqrt(7) / 3]])
same("F1 B", [gB[0], gB[1], gB[2]], [[1], [-2, 4], [1 - sp.sqrt(3), 1 + sp.sqrt(3)]])


def box_frq(n):
    V = x * (n - 2 * x)**2
    c = sp.Rational(n, 6)
    vmax = V.subs(x, c)
    frq = FRQ("The largest box", (rf"An open box is made from a ${n} \times {n}$ inch square sheet by cutting a square of side $x$ inches from each corner and folding up the sides."), [
        Part("a", r"Write the volume $V$ of the box as a function of $x$, and give the domain.", expr(str(V), var="x"),
             rf"The base is ${n} - 2x$ on a side and the height is $x$: $V(x) = x({n} - 2x)^2$, $0 \le x \le {sp.latex(sp.Rational(n, 2))}$.", [(1, "volume"), (1, "domain")], work="2cm"),
        Part("b", r"Find the value of $x$ that gives the largest volume. Justify your answer.", num(c),
             rf"$V'(x) = ({n} - 2x)({n} - 6x) = 0$ at $x = {sp.latex(c)}$ and $x = {sp.latex(sp.Rational(n, 2))}$. Candidates: $V(0) = 0$, $V\left({sp.latex(c)}\right) = {sp.latex(vmax)}$, "
             rf"$V\left({sp.latex(sp.Rational(n, 2))}\right) = 0$. The maximum is at $x = {sp.latex(c)}$.", [(1, "$V'$"), (1, "critical point"), (1, "candidates justification")], work="2.8cm"),
        Part("c", r"What is the largest volume? Include units.", num(vmax), rf"${sp.latex(vmax)}$ cubic inches.", [(1, "value with units")], work="1.2cm"),
    ], frq_type="Optimization")
    return frq, [c, vmax]


F2A, bA = box_frq(18)
F2B, bB = box_frq(30)
same("F2", [bA, bB], [[3, 432], [5, 2000]])


def curve_frq(F, tex, ytex):
    yp = sp.simplify(-sp.diff(F, x) / sp.diff(F, y))
    n, d = sp.fraction(sp.together(yp))
    hz = sorted(sp.solve([n, F], [x, y]), key=lambda p: float(p[1]))
    vt = sorted(sp.solve([d, F], [x, y]), key=lambda p: float(p[0]))
    Y = sp.Function("Y")(x)
    ypp = sp.diff(yp.subs(y, Y), x).subs(sp.Derivative(Y, x), yp.subs(y, Y)).subs(Y, y)
    top = hz[-1]
    v = sp.simplify(ypp.subs({x: top[0], y: top[1]}))
    frq = FRQ("Tangents to an implicit curve", rf"Consider the curve ${tex}$.", [
        Part("a", rf"Show that $\dfrac{{dy}}{{dx}} = {ytex}$.", selfcheck(ytex), r"Differentiate implicitly and solve for $\frac{dy}{dx}$.", [(1, "implicit differentiation"), (1, "solves")], work="2.2cm"),
        Part("b", r"Find the points where the tangent line is horizontal. Enter the larger $y$-coordinate.", num(top[1]),
             r"Numerator zero, together with the curve: " + ", ".join(rf"$\left({sp.latex(p[0])}, {sp.latex(p[1])}\right)$" for p in hz) + ".", [(1, "numerator $= 0$"), (1, "points")], work="2.4cm"),
        Part("c", r"Find the points where the tangent line is vertical. Enter the larger $x$-coordinate.", num(vt[-1][0]),
             r"Denominator zero, together with the curve: " + ", ".join(rf"$\left({sp.latex(p[0])}, {sp.latex(p[1])}\right)$" for p in vt) + ".", [(1, "denominator $= 0$"), (1, "points")], work="2.4cm"),
        Part("d", rf"Find $\dfrac{{d^2y}}{{dx^2}}$ at $\left({sp.latex(top[0])}, {sp.latex(top[1])}\right)$. Does the curve have a relative maximum or minimum there?", num(v),
             rf"At that point $\frac{{dy}}{{dx}} = 0$, and $\frac{{d^2y}}{{dx^2}} = {sp.latex(v)}$, so the curve has a relative {'maximum' if v < 0 else 'minimum'} there.",
             [(1, "value"), (1, "conclusion")], work="2.6cm"),
    ], frq_type="Implicit differentiation")
    return frq, [top, vt[-1], v]


F3A, cA = curve_frq(x**2 + y**2 - 4 * y - 12, r"x^2 + y^2 - 4y = 12", r"\dfrac{x}{2 - y}")
F3B, cB = curve_frq(x**2 + y**2 + 6 * x - 16, r"x^2 + y^2 + 6x = 16", r"-\dfrac{x + 3}{y}")
same("F3 A", [cA[0][1], cA[1][0], cA[2]], [6, 4, sp.Rational(-1, 4)])
same("F3 B", [cB[0][1], cB[1][0], cB[2]], [5, 2, sp.Rational(-1, 5)])

TEST = UnitTest(unit=5, title="Analytical Applications of Differentiation", mcq_a=A, mcq_b=B,
                frq=[Variants(F1A, F1B), Variants(F2A, F2B), Variants(F3A, F3B)])
