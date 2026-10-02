"""Unit 5 test: Analytical Applications of Differentiation. AP format: 12 MCQ (no calculator), 4 MCQ (calculator), 3 FRQ.
Two forms (A and B) for every slot.

Covers 5.1-5.12. Choices are built by `pick`, which puts the keyed answer at a planned letter, so a key can't drift from its
choices. Every keyed value is checked with sympy.
"""
import sympy as sp

from calclib import FRQ, MCQ, Part, UnitTest, Variants, check, close, expr, num, same, selfcheck
from calclib.figs import graph

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
def iv(lst):
    return r" \text{ and } ".join(rf"\left({sp.latex(a)}, {sp.latex(b)}\right)" for a, b in lst) or r"\text{none}"


def graph_frq(name, verts, c, fc):
    """f' is piecewise linear through verts. Extrema, inflection points, increasing and concave down, tangent line at x = c."""
    segs = []
    for (x0, y0), (x1, y1) in zip(verts, verts[1:]):
        m = sp.Rational(y1 - y0, x1 - x0)
        segs.append((m, x0, y0, x1))
    lo, hi = verts[0][0], verts[-1][0]
    fp_at = lambda v: next(y0 + m * (v - x0) for m, x0, y0, x1 in segs if x0 <= v <= x1)
    zeros = []
    for m, x0, y0, x1 in segs:
        z = x0 - sp.Rational(y0) / m
        if x0 < z < x1 or (z == x1 and x1 != hi):
            zeros.append(z)
    eps = sp.Rational(1, 100)
    mx = [z for z in zeros if fp_at(z - eps) > 0 > fp_at(z + eps)]
    mn = [z for z in zeros if fp_at(z - eps) < 0 < fp_at(z + eps)]
    infl = [x1 for (m, _, _, x1), (m2, _, _, _) in zip(segs, segs[1:]) if m * m2 < 0]
    # increasing (f' > 0) and concave down (f' decreasing): pieces of negative-slope segments where f' > 0
    both = []
    for m, x0, y0, x1 in segs:
        if m < 0:
            z = x0 - sp.Rational(y0) / m
            a, b = x0, min(max(z, x0), x1)
            if b > a and fp_at((a + b) / 2) > 0:
                both.append((a, b))
    slope_c = fp_at(c)
    line = sp.expand(fc + slope_c * (x - c))
    fig = graph(name, [(f"{m}*(x-({x0}))+({y0})", x0, x1) for m, x0, y0, x1 in segs], xr=(lo, hi),
                yr=(min(v for _, v in verts) - 0.5, max(v for _, v in verts) + 0.5), ylabel="f'(x)", w="7.5cm", h="5cm",
                caption="The graph of $f'$.")
    ext = r";\ ".join([rf"\text{{relative maximum at }} x = {sp.latex(z)}" for z in mx]
                        + [rf"\text{{relative minimum at }} x = {sp.latex(z)}" for z in mn])
    frq = FRQ("Reading the graph of a derivative", (
        rf"The function $f$ is defined on the closed interval ${lo} \le x \le {hi}$ and satisfies $f({c}) = {fc}$. The graph of $f'$, "
        r"the derivative of $f$, consists of three line segments, as shown in the figure."), [
        Part("a", rf"Find the $x$-coordinate of each relative extremum of $f$ on the open interval ${lo} < x < {hi}$, and classify each "
                  r"as a relative minimum or a relative maximum. Justify your answers.", selfcheck(ext),
             "; ".join([rf"$f'$ changes from positive to negative at $x = {sp.latex(z)}$, so $f$ has a relative maximum there" for z in mx]
                       + [rf"$f'$ changes from negative to positive at $x = {sp.latex(z)}$, so $f$ has a relative minimum there" for z in mn]) + ".",
             [(1, "relative maximum location(s) with justification"), (1, "relative minimum location(s) with justification")], work="3cm"),
        Part("b", r"Find the $x$-coordinate of each point of inflection of the graph of $f$. Give a reason for your answer.",
             selfcheck(r"x = " + r" \text{ and } x = ".join(sp.latex(v) for v in infl)),
             r"The graph of $f$ has a point of inflection where $f'$ changes from increasing to decreasing or from decreasing to "
             rf"increasing: at $x = {' and $x = '.join(sp.latex(v) + '$' for v in infl)}.",
             [(1, "both $x$-values"), (1, "reason: $f'$ changes from increasing to decreasing or vice versa")], work="2.4cm"),
        Part("c", r"On what open intervals, if any, is the graph of $f$ both increasing and concave down? Give a reason for your answer.",
             selfcheck(iv(both)),
             rf"$f$ is increasing where $f' > 0$, and the graph is concave down where $f'$ is decreasing. Both hold on ${iv(both)}$.",
             [(1, "intervals"), (1, "reason")], work="2.4cm"),
        Part("d", rf"Write an equation for the line tangent to the graph of $f$ at $x = {c}$.", expr(str(line)),
             rf"From the graph, $f'({c}) = {sp.latex(slope_c)}$, and $f({c}) = {fc}$. The tangent line is $y = {fc} + ({sp.latex(slope_c)})(x - {c})$.",
             [(1, f"$f'({c}) = {sp.latex(slope_c)}$ from the graph"), (1, "tangent line equation")], work="2.2cm"),
    ], frq_type="Graph of f'", figure=fig)
    return frq, [mx, mn, infl, both, line]


F1A, gA = graph_frq("u5_fpa", [(-3, 2), (-1, -2), (2, 1), (4, -1)], 0, 5)
F1B, gB = graph_frq("u5_fpb", [(-4, -2), (-1, 1), (2, -2), (4, 2)], 1, 4)
same("F1 A", [gA[0], gA[1], gA[2], gA[4]], [[-2, 3], [1], [-1, 2], 5 - x])
same("F1 A both", [list(p) for p in gA[3]], [[-3, -2], [2, 3]])
same("F1 B", [gB[0], gB[1], gB[2], gB[4]], [[0], [-2, 3], [-1, 2], 5 - x])
same("F1 B both", [list(p) for p in gB[3]], [[-1, 0]])


def param_frq(f_tex, f, crit_at, kcrit, kind, kinfl, kinfl_tex, fp_tex, fpp_tex, infl_steps):
    """f(x) with positive constant k: f', f''; k for a critical point at crit_at and its classification; k for an inflection point on the x-axis."""
    fp, fpp = sp.diff(f, x), sp.diff(f, x, 2)
    fpp_c = fpp.subs({k: kcrit, x: crit_at})
    frq = FRQ("A family of functions", (
        rf"Let $f$ be the function defined by $f(x) = {f_tex}$ for $x > 0$, where $k$ is a positive constant."), [
        Part("a", r"Find $f'(x)$ and $f''(x)$.", selfcheck(rf"f'(x) = {fp_tex},\ f''(x) = {fpp_tex}"),
             rf"$f'(x) = {fp_tex}$ and $f''(x) = {fpp_tex}$.", [(1, "$f'(x)$"), (1, "$f''(x)$")], work="2.4cm"),
        Part("b", rf"For what value of the constant $k$ does $f$ have a critical point at $x = {crit_at}$? For this value of $k$, determine "
                  rf"whether $f$ has a relative minimum, relative maximum, or neither at $x = {crit_at}$. Justify your answer.",
             selfcheck(rf"k = {sp.latex(kcrit)};\ \text{{relative {kind}}}"),
             rf"$f'({crit_at}) = {sp.latex(fp.subs(x, crit_at))} = 0$ gives $k = {sp.latex(kcrit)}$. Then $f''({crit_at}) = {sp.latex(fpp_c)} "
             rf"{'>' if fpp_c > 0 else '<'} 0$, so by the Second Derivative Test $f$ has a relative {kind} at $x = {crit_at}$.",
             [(1, f"$k = {sp.latex(kcrit)}$"), (1, f"$f''({crit_at})$"), (1, f"relative {kind} with justification")], work="3cm"),
        Part("c", r"For a certain value of the constant $k$, the graph of $f$ has a point of inflection on the $x$-axis. Find this value of $k$.",
             num(kinfl, tol=0.001, display=kinfl_tex),
             infl_steps,
             [(1, "$f''(x) = 0$ and $f(x) = 0$ at the same $x$"), (1, f"answer $k = {kinfl_tex}$")], work="3cm"),
    ], frq_type="Function analysis")
    return frq, [fp, fpp, kcrit, fpp_c, kinfl]


k = sp.symbols("k", positive=True)
fA = k * sp.sqrt(x) - sp.log(x)
F2A, pA = param_frq(r"k\sqrt{x} - \ln x", fA, 4, 1, "minimum", 4 / sp.exp(2), r"\dfrac{4}{e^2}",
                    r"\dfrac{k}{2\sqrt{x}} - \dfrac{1}{x}", r"-\dfrac{k}{4x^{3/2}} + \dfrac{1}{x^2}",
                    r"$f''(x) = 0$ when $\dfrac{1}{x^2} = \dfrac{k}{4x^{3/2}}$, so $\sqrt{x} = \dfrac4k$ and $x = \dfrac{16}{k^2}$. The point is on "
                    r"the $x$-axis when $f\!\left(\dfrac{16}{k^2}\right) = 4 - \ln\dfrac{16}{k^2} = 0$, so $\dfrac{16}{k^2} = e^4$ and "
                    r"$k = \dfrac{4}{e^2}$. ($f''$ changes sign there, from positive to negative.)")
fB = k * sp.log(x) + 1 / x
F2B, pB = param_frq(r"k\ln x + \dfrac{1}{x}", fB, 2, sp.Rational(1, 2), "minimum", 2 * sp.sqrt(sp.E), r"2\sqrt{e}",
                    r"\dfrac{k}{x} - \dfrac{1}{x^2}", r"-\dfrac{k}{x^2} + \dfrac{2}{x^3}",
                    r"$f''(x) = 0$ when $\dfrac{2}{x^3} = \dfrac{k}{x^2}$, so $x = \dfrac2k$. The point is on the $x$-axis when "
                    r"$f\!\left(\dfrac2k\right) = k\ln\dfrac2k + \dfrac{k}{2} = 0$, so $\ln\dfrac2k = -\dfrac12$ and $k = 2\sqrt{e}$. "
                    r"($f''$ changes sign there, from positive to negative.)")
for lab, f, p, crit_at in [("F2 A", fA, pA, 4), ("F2 B", fB, pB, 2)]:
    same(lab + " crit", sp.solve(sp.diff(f, x).subs(x, crit_at), k), [p[2]])
    check(lab + " min", p[3] > 0)
    xi = sp.solve(sp.diff(f, x, 2), x)
    check(lab + " one inflection", len(xi) == 1)
    same(lab + " infl on axis", sp.simplify(f.subs(x, xi[0]).subs(k, p[4])), 0)
    xv = xi[0].subs(k, p[4])
    fpp = sp.diff(f, x, 2).subs(k, p[4])
    check(lab + " sign change", fpp.subs(x, xv / 2) > 0 and fpp.subs(x, 2 * xv) < 0)
same("F2 A fp", sp.simplify(pA[0] - (k / (2 * sp.sqrt(x)) - 1 / x)), 0)
same("F2 A fpp", sp.simplify(pA[1] - (-k / (4 * x**sp.Rational(3, 2)) + 1 / x**2)), 0)
same("F2 B fp", sp.simplify(pB[0] - (k / x - 1 / x**2)), 0)
same("F2 B fpp", sp.simplify(pB[1] - (-k / x**2 + 2 / x**3)), 0)


def curve_frq(F, tex, ytex):
    yp = sp.simplify(-sp.diff(F, x) / sp.diff(F, y))
    n, d = sp.fraction(sp.together(yp))
    hz = sorted(sp.solve([n, F], [x, y]), key=lambda p: float(p[1]))
    vt = sorted(sp.solve([d, F], [x, y]), key=lambda p: float(p[0]))
    Y = sp.Function("Y")(x)
    ypp = sp.diff(yp.subs(y, Y), x).subs(sp.Derivative(Y, x), yp.subs(y, Y)).subs(Y, y)
    top = hz[-1]
    v = sp.simplify(ypp.subs({x: top[0], y: top[1]}))
    pts = lambda L: r" \text{ and } ".join(rf"\left({sp.latex(p[0])}, {sp.latex(p[1])}\right)" for p in L)
    frq = FRQ("Tangents to an implicit curve", rf"Consider the curve given by the equation ${tex}$.", [
        Part("a", rf"Show that $\dfrac{{dy}}{{dx}} = {ytex}$.", selfcheck(ytex),
             r"Differentiate both sides with respect to $x$, using the chain rule on each $y$ term, and solve for $\frac{dy}{dx}$.",
             [(1, "implicit differentiation"), (1, "verifies the expression for $\\frac{dy}{dx}$")], work="2.4cm"),
        Part("b", r"Find the coordinates of all points on the curve at which the line tangent to the curve is horizontal.", selfcheck(pts(hz)),
             r"The numerator of $\frac{dy}{dx}$ is $0$; substituting into the equation of the curve gives $" + pts(hz) + "$.",
             [(1, "sets the numerator equal to $0$"), (1, "both points")], work="2.4cm"),
        Part("c", r"Find the coordinates of all points on the curve at which the line tangent to the curve is vertical.", selfcheck(pts(vt)),
             r"The denominator of $\frac{dy}{dx}$ is $0$; substituting into the equation of the curve gives $" + pts(vt) + "$.",
             [(1, "sets the denominator equal to $0$"), (1, "both points")], work="2.4cm"),
        Part("d", rf"Find the value of $\dfrac{{d^2y}}{{dx^2}}$ at the point $\left({sp.latex(top[0])}, {sp.latex(top[1])}\right)$. Does the curve "
                  r"have a relative minimum, a relative maximum, or neither at this point? Justify your answer.", num(v),
             rf"At that point $\frac{{dy}}{{dx}} = 0$, and $\frac{{d^2y}}{{dx^2}} = {sp.latex(v)} {'<' if v < 0 else '>'} 0$, so the curve has a "
             rf"relative {'maximum' if v < 0 else 'minimum'} there.",
             [(1, "value of $\\frac{d^2y}{dx^2}$"), (1, "classification with justification")], work="2.8cm"),
    ], frq_type="Implicit differentiation")
    return frq, [top, vt[-1], v]


F3A, cA = curve_frq(x**2 + y**2 - 4 * y - 12, r"x^2 + y^2 - 4y = 12", r"\dfrac{x}{2 - y}")
F3B, cB = curve_frq(x**2 + y**2 + 6 * x - 16, r"x^2 + y^2 + 6x = 16", r"-\dfrac{x + 3}{y}")
same("F3 A", [cA[0][1], cA[1][0], cA[2]], [6, 4, sp.Rational(-1, 4)])
same("F3 B", [cB[0][1], cB[1][0], cB[2]], [5, 2, sp.Rational(-1, 5)])

TEST = UnitTest(unit=5, title="Analytical Applications of Differentiation", mcq_a=A, mcq_b=B,
                frq=[Variants(F1A, F1B), Variants(F2A, F2B), Variants(F3A, F3B)])
