"""Unit 2 test: Differentiation, Definition and Fundamental Properties. AP format: 12 MCQ (no calculator),
4 MCQ (calculator), 3 FRQ. Two forms: every slot has a version A and a version B.

Covers 2.1-2.10. Every keyed answer is checked with sympy below its question.
"""
import sympy as sp

from calclib import FRQ, MCQ, Part, UnitTest, Variants, check, close, expr, limchain, num, same, selfcheck

x, t, h = sp.symbols("x t h")
pi = sp.pi


def D(e, v=x):
    return sp.simplify(sp.diff(e, v))


MEANS = {"A": "that's a value, not a rate", "C": "that's a total change over an interval"}

# ================================================================ Part A (no calculator)
A = [
    Variants(
        MCQ(r"$\displaystyle\lim_{h\to0}\frac{(2+h)^4 - 16}{h}$ is", [r"$0$", r"$16$", r"$32$", r"nonexistent"], "C",
            r"It is $f'(2)$ for $f(x) = x^4$: $4(2)^3 = 32$.", why_not={"B": "that's $f(2)$", "A": "treated $\\frac00$ as $0$"}),
        MCQ(r"$\displaystyle\lim_{h\to0}\frac{\sqrt{9+h} - 3}{h}$ is", [r"$\dfrac16$", r"$\dfrac13$", r"$3$", r"nonexistent"], "A",
            r"It is $f'(9)$ for $f(x) = \sqrt x$: $\dfrac{1}{2\sqrt9} = \dfrac16$.", why_not={"B": "forgot the $2$ in $\\frac{1}{2\\sqrt x}$"}),
    ),
    Variants(
        MCQ(r"If $f(x) = x^3 - 5x$, then $f'(-1) =$", [r"$-2$", r"$2$", r"$4$", r"$-8$"], "A", r"$3x^2 - 5 = 3 - 5 = -2$.",
            why_not={"C": "that's $f(-1)$"}),
        MCQ(r"If $f(x) = 2x^4 - x^2$, then $f'(-1) =$", [r"$1$", r"$-6$", r"$6$", r"$-10$"], "B", r"$8x^3 - 2x = -8 + 2 = -6$.",
            why_not={"A": "that's $f(-1)$", "C": "sign error"}),
    ),
    Variants(
        MCQ(r"If $y = 4\sqrt{x} - \dfrac{3}{x}$, then $\dfrac{dy}{dx}$ at $x = 4$ is", [r"$\dfrac54$", r"$\dfrac{13}{16}$", r"$\dfrac{19}{16}$", r"$1$"], "C",
            r"$\dfrac{dy}{dx} = 2x^{-1/2} + 3x^{-2}$, which is $1 + \frac{3}{16} = \frac{19}{16}$ at $x = 4$.", why_not={"B": "sign error on the second term"}),
        MCQ(r"If $y = 6\sqrt[3]{x} + \dfrac{2}{x^2}$, then $\dfrac{dy}{dx}$ at $x = 1$ is", [r"$6$", r"$0$", r"$-2$", r"$2$"], "C",
            r"$\dfrac{dy}{dx} = 2x^{-2/3} - 4x^{-3}$, which is $2 - 4 = -2$ at $x = 1$.", why_not={"D": "sign error on the second term"}),
    ),
    Variants(
        MCQ(r"The line tangent to $y = xe^x$ at $x = 0$ is", [r"$y = 1$", r"$y = x$", r"$y = x + 1$", r"$y = ex$"], "B",
            r"$y' = e^x + xe^x = 1$ at $x = 0$, and the point is $(0, 0)$."),
        MCQ(r"The line tangent to $y = x\sin x$ at $x = \dfrac\pi2$ is", [r"$y = x$", r"$y = \dfrac\pi2$", r"$y = x + \dfrac\pi2$", r"$y = -x + \pi$"], "A",
            r"$y' = \sin x + x\cos x = 1$ at $x = \frac\pi2$, and the point is $\left(\frac\pi2, \frac\pi2\right)$: $y = x$."),
    ),
    Variants(
        MCQ(r"$\dfrac{d}{dx}\left[\dfrac{\sin x}{x}\right] =$",
            [r"$\dfrac{x\cos x - \sin x}{x^2}$", r"$\dfrac{\sin x - x\cos x}{x^2}$", r"$\cos x$", r"$\dfrac{\cos x - \sin x}{x^2}$"], "A",
            r"Low d-high minus high d-low, over low squared.", why_not={"B": "numerator reversed", "C": "divided the derivatives"}),
        MCQ(r"$\dfrac{d}{dx}\left[\dfrac{x}{\cos x}\right] =$",
            [r"$\dfrac{\cos x - x\sin x}{\cos^2 x}$", r"$\dfrac{\cos x + x\sin x}{\cos^2 x}$", r"$-\dfrac{1}{\sin x}$", r"$\dfrac{x\sin x}{\cos^2 x}$"], "B",
            r"$\dfrac{\cos x\cdot 1 - x(-\sin x)}{\cos^2 x}$.", why_not={"A": "lost the sign of $-\\sin x$", "C": "divided the derivatives"}),
    ),
    Variants(
        MCQ(r"If $y = x^2\ln x$, then $y'(1) =$", [r"$0$", r"$1$", r"$2$", r"$e$"], "B", r"$2x\ln x + x = 0 + 1 = 1$ at $x = 1$.",
            why_not={"A": "that's $y(1)$"}),
        MCQ(r"If $y = \sqrt{x}\,\ln x$, then $y'(1) =$", [r"$1$", r"$0$", r"$\dfrac12$", r"$2$"], "A",
            r"$\dfrac{\ln x}{2\sqrt x} + \dfrac{\sqrt x}{x} = 0 + 1 = 1$ at $x = 1$.", why_not={"B": "that's $y(1)$"}),
    ),
    Variants(
        MCQ(r"Where is $f(x) = |x - 2| + 1$ not differentiable?", [r"$x = 0$", r"$x = 1$", r"$x = 2$", r"$f$ is differentiable everywhere"], "C",
            r"A corner at $x = 2$: slopes $-1$ and $1$."),
        MCQ(r"Where is $f(x) = (x + 1)^{2/3}$ not differentiable?", [r"$x = -1$", r"$x = 0$", r"$x = 1$", r"$f$ is differentiable everywhere"], "A",
            r"A cusp at $x = -1$."),
    ),
    Variants(
        MCQ(r"$f(x) = x^2$ for $x \le 1$ and $f(x) = ax + b$ for $x > 1$. Which pair $(a, b)$ makes $f$ differentiable at $x = 1$?",
            [r"$(2, -1)$", r"$(1, 0)$", r"$(2, 1)$", r"$(-1, 2)$"], "A",
            r"Slopes: $2x = 2$, so $a = 2$. Values: $1 = a + b$, so $b = -1$.", why_not={"B": "only continuous, not smooth", "C": "values don't match"}),
        MCQ(r"$f(x) = x^3$ for $x \le 2$ and $f(x) = ax + b$ for $x > 2$. Which pair $(a, b)$ makes $f$ differentiable at $x = 2$?",
            [r"$(12, 8)$", r"$(4, 0)$", r"$(12, -16)$", r"$(-16, 12)$"], "C",
            r"Slopes: $3x^2 = 12$, so $a = 12$. Values: $8 = 24 + b$, so $b = -16$.", why_not={"B": "only continuous, not smooth", "A": "values don't match"}),
    ),
    Variants(
        MCQ(r"Values of a differentiable function $f$ are shown."
            r"\par\centerline{\begin{tabular}{c|cccc} $t$ & 0 & 2 & 5 & 7 \\ \hline $f(t)$ & 10 & 14 & 23 & 25\end{tabular}}"
            r"\par The best estimate of $f'(3.5)$ is", [r"$3$", r"$4.5$", r"$2$", r"$9$"], "A",
            r"$\dfrac{23 - 14}{5 - 2} = 3$.", why_not={"D": "forgot to divide by the change in $t$"}),
        MCQ(r"Values of a differentiable function $g$ are shown."
            r"\par\centerline{\begin{tabular}{c|cccc} $t$ & 1 & 4 & 6 & 9 \\ \hline $g(t)$ & 50 & 44 & 35 & 29\end{tabular}}"
            r"\par The best estimate of $g'(5)$ is", [r"$-4.5$", r"$-9$", r"$-3$", r"$4.5$"], "A",
            r"$\dfrac{35 - 44}{6 - 4} = -4.5$.", why_not={"B": "forgot to divide", "D": "sign error"}),
    ),
    Variants(
        MCQ(r"$P(t)$ is the number of fish in a lake $t$ years after 2020, and $P'(4) = -300$. Which statement is true?",
            [r"There are $-300$ fish in 2024.", r"The lake lost 300 fish from 2020 to 2024.", r"The population fell by 300 over four years.",
             r"In 2024 the population is decreasing at 300 fish per year."], "D", r"A derivative is a rate at an instant, with units.",
            why_not={"A": MEANS["A"], "B": MEANS["C"], "C": MEANS["C"]}),
        MCQ(r"$V(t)$ is the volume of a balloon in liters $t$ seconds after it starts inflating, and $V'(10) = 2.5$. Which statement is true?",
            [r"The balloon holds 2.5 liters at 10 seconds.", r"At 10 seconds, the volume is increasing at 2.5 liters per second.",
             r"The balloon gains 2.5 liters in the first 10 seconds.", r"It takes 2.5 seconds to add 10 liters."], "B",
            r"A derivative is a rate at an instant, with units.", why_not=MEANS),
    ),
    Variants(
        MCQ(r"If $f(x) = \sec x$, then $f'\!\left(\dfrac\pi3\right) =$", [r"$4$", r"$2\sqrt3$", r"$\dfrac{\sqrt3}{2}$", r"$2$"], "B",
            r"$\sec\frac\pi3\tan\frac\pi3 = 2\sqrt3$.", why_not={"D": "that's $f\\left(\\frac\\pi3\\right)$", "A": "used $\\sec^2$"}),
        MCQ(r"If $f(x) = \cot x$, then $f'\!\left(\dfrac\pi6\right) =$", [r"$4$", r"$-4$", r"$-2$", r"$-\dfrac14$"], "B",
            r"$-\csc^2\frac\pi6 = -4$.", why_not={"A": "missing the minus sign", "C": "forgot to square"}),
    ),
    Variants(
        MCQ(r"Which function is not differentiable at $x = 0$?", [r"$x^3$", r"$\sin x$", r"$x^{1/3}$", r"$e^x$"], "C",
            r"$x^{1/3}$ has a vertical tangent at $0$."),
        MCQ(r"Which function is continuous but not differentiable at $x = 1$?", [r"$(x-1)^2$", r"$\dfrac{1}{x-1}$", r"$x - 1$", r"$|x - 1|$"], "D",
            r"$|x - 1|$ has a corner at $1$.", why_not={"B": "not even continuous"}),
    ),
]
same("A1", [sp.limit(((2 + h)**4 - 16) / h, h, 0), sp.limit((sp.sqrt(9 + h) - 3) / h, h, 0)], [32, sp.Rational(1, 6)])
same("A2", [D(x**3 - 5 * x).subs(x, -1), D(2 * x**4 - x**2).subs(x, -1)], [-2, -6])
same("A3", [D(4 * sp.sqrt(x) - 3 / x).subs(x, 4), D(6 * x**sp.Rational(1, 3) + 2 / x**2).subs(x, 1)], [sp.Rational(19, 16), -2])
same("A4", [D(x * sp.exp(x)).subs(x, 0), D(x * sp.sin(x)).subs(x, pi / 2), (x * sp.sin(x)).subs(x, pi / 2)], [1, 1, pi / 2])
same("A5", [sp.simplify(D(sp.sin(x) / x) - (x * sp.cos(x) - sp.sin(x)) / x**2),
            sp.simplify(D(x / sp.cos(x)) - (sp.cos(x) + x * sp.sin(x)) / sp.cos(x)**2)], [0, 0])
same("A6", [D(x**2 * sp.log(x)).subs(x, 1), D(sp.sqrt(x) * sp.log(x)).subs(x, 1)], [1, 1])
same("A8", [2 * 1, 1 - 2, 3 * 2**2, 8 - 24], [2, -1, 12, -16])
same("A9", [sp.Rational(23 - 14, 3), sp.Rational(35 - 44, 2)], [3, sp.Rational(-9, 2)])
same("A11", [D(1 / sp.cos(x)).subs(x, pi / 3), D(sp.cot(x)).subs(x, pi / 6)], [2 * sp.sqrt(3), -4])

# ================================================================ Part B (calculator)
B = [
    Variants(
        MCQ(r"If $f(x) = x^3e^{-x}$, then $f'(1.5)$ is closest to", [r"$1.004$", r"$-0.502$", r"$3.375$", r"$0.753$"], "D",
            r"A numerical derivative gives about $0.753$.", calc=True),
        MCQ(r"If $f(x) = x^2\cos x$, then $f'(2)$ is closest to", [r"$-1.665$", r"$3.584$", r"$-5.302$", r"$0.416$"], "C",
            r"A numerical derivative gives about $-5.302$.", calc=True),
    ),
    Variants(
        MCQ(r"If $g(x) = \dfrac{\ln x}{x^2}$, then $g'(2)$ is closest to", [r"$0.173$", r"$0.250$", r"$-0.250$", r"$-0.048$"], "D",
            r"A numerical derivative gives about $-0.048$.", calc=True),
        MCQ(r"If $g(x) = \dfrac{e^x}{x+1}$, then $g'(1)$ is closest to", [r"$1.359$", r"$2.718$", r"$0$", r"$0.680$"], "D",
            r"A numerical derivative gives about $0.680$ (exactly $\frac e4$).", calc=True),
    ),
    Variants(
        MCQ(r"At what value of $x$ does $y = e^x - 3x$ have a horizontal tangent line?", [r"$0$", r"$1.099$", r"$3$", r"$0.693$"], "B",
            r"$e^x - 3 = 0$ gives $x = \ln 3 \approx 1.099$.", calc=True),
        MCQ(r"At what value of $x$ does $y = e^x - 5x$ have a horizontal tangent line?", [r"$5$", r"$0.693$", r"$1.609$", r"$0$"], "C",
            r"$e^x - 5 = 0$ gives $x = \ln 5 \approx 1.609$.", calc=True),
    ),
    Variants(
        MCQ(r"For $f(x) = \sqrt{x + 1}$, the average rate of change on $[0, 3]$ is $\frac13$. At what $x$ in $(0, 3)$ is $f'(x) = \frac13$?",
            [r"$1.25$", r"$1.5$", r"$0.5$", r"$2$"], "A",
            r"$\dfrac{1}{2\sqrt{x+1}} = \dfrac13$ gives $\sqrt{x+1} = 1.5$, so $x = 1.25$.", calc=True),
        MCQ(r"For $f(x) = \sqrt{x + 4}$, the average rate of change on $[0, 5]$ is $\frac15$. At what $x$ in $(0, 5)$ is $f'(x) = \frac15$?",
            [r"$2.5$", r"$2.25$", r"$1$", r"$3$"], "B",
            r"$\dfrac{1}{2\sqrt{x+4}} = \dfrac15$ gives $\sqrt{x+4} = 2.5$, so $x = 2.25$.", calc=True),
    ),
]
close("B13", sp.diff(x**3 * sp.exp(-x), x).subs(x, 1.5), 0.753, 5e-4)
close("B13b", sp.diff(x**2 * sp.cos(x), x).subs(x, 2), -5.302, 5e-4)
close("B14", sp.diff(sp.log(x) / x**2, x).subs(x, 2), -0.048, 5e-4)
close("B14b", sp.diff(sp.exp(x) / (x + 1), x).subs(x, 1), 0.680, 5e-4)
same("B15", [sp.solve(sp.exp(x) - 3, x)[0], sp.solve(sp.exp(x) - 5, x)[0]], [sp.log(3), sp.log(5)])
same("B16", [sp.solve(sp.Eq(1 / (2 * sp.sqrt(x + 1)), sp.Rational(1, 3)), x)[0], sp.solve(sp.Eq(1 / (2 * sp.sqrt(x + 4)), sp.Rational(1, 5)), x)[0]],
     [sp.Rational(5, 4), sp.Rational(9, 4)])


# ================================================================ free response
def motion(s, T, t_mid, t_avg, name):
    v = sp.expand(sp.diff(s, t))
    rest = sorted(sp.solve(v, t))
    vm = v.subs(t, t_mid)
    avg = sp.Rational(s.subs(t, t_avg) - s.subs(t, 0), t_avg)
    tex = sp.latex(s)
    return FRQ("Particle motion", (
        rf"A particle moves along the $x$-axis. Its position at time $t$ seconds is $s(t) = {tex}$ meters, for $0 \le t \le {T}$."), [
        Part("a", r"Find the velocity $v(t)$.", expr(str(v), var="t"), rf"$v(t) = s'(t) = {sp.latex(v)}$.", [(1, "derivative")], work="1.6cm"),
        Part("b", rf"Find $v({t_mid})$. Is the particle moving left or right at $t = {t_mid}$? Explain.", num(vm),
             rf"$v({t_mid}) = {vm}$. The velocity is negative, so the particle is moving left, at ${-vm}$ meters per second.",
             [(1, "value"), (1, "left, because $v < 0$")], work="2cm"),
        Part("c", r"At what times is the particle at rest? Enter the later one.", num(rest[-1]),
             rf"$v(t) = 0$ when $t = {rest[0]}$ or $t = {rest[1]}$.", [(1, "sets $v(t) = 0$"), (1, "both times")], work="2cm"),
        Part("d", rf"Find the average velocity of the particle over $0 \le t \le {t_avg}$.", num(avg),
             rf"$\dfrac{{s({t_avg}) - s(0)}}{{{t_avg} - 0}} = \dfrac{{{s.subs(t, t_avg)} - 0}}{{{t_avg}}} = {sp.latex(avg)}$ meters per second.",
             [(1, "difference quotient"), (1, "value")], work="2cm"),
    ], frq_type="Particle motion"), (v, rest, vm, avg)


F1A, chkA = motion(t**3 - 6 * t**2 + 9 * t, 5, 2, 4, "A")
F1B, chkB = motion(t**3 - 9 * t**2 + 24 * t, 6, 3, 3, "B")
same("F1 A", [chkA[1], chkA[2], chkA[3]], [[1, 3], -3, 1])
same("F1 B", [chkB[1], chkB[2], chkB[3]], [[2, 4], -3, 6])


def table_frq(c1, c2, vals):
    """vals: {x: (f, f', g, g')}. h = f g, k = f / g, p = x^2 f."""
    f1, df1, g1, dg1 = vals[c1]
    f2, df2, g2, dg2 = vals[c2]
    hp = df2 * g2 + f2 * dg2
    kp = sp.Rational(g1 * df1 - f1 * dg1, g1**2)
    h2 = f2 * g2
    line = sp.expand(h2 + hp * (x - c2))
    pp = 2 * c1 * f1 + c1**2 * df1
    rows = " \\\\ ".join(f"{c} & {vals[c][0]} & {vals[c][1]} & {vals[c][2]} & {vals[c][3]}" for c in (c1, c2))
    return FRQ("Rules from a table", (
        r"The functions $f$ and $g$ are differentiable. Selected values are given."
        r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $x$ & $f(x)$ & $f'(x)$ & $g(x)$ & $g'(x)$ \\ \hline " + rows + r"\end{tabular}}"
        r"\par Let $h(x) = f(x)g(x)$, $k(x) = \dfrac{f(x)}{g(x)}$ and $p(x) = x^2 f(x)$."), [
        Part("a", rf"Find $h'({c2})$.", num(hp),
             rf"$h'({c2}) = f'({c2})g({c2}) + f({c2})g'({c2}) = ({df2})({g2}) + ({f2})({dg2}) = {hp}$.", [(1, "product rule"), (1, "value")], work="2cm"),
        Part("b", rf"Find $k'({c1})$.", num(kp),
             rf"$k'({c1}) = \dfrac{{g({c1})f'({c1}) - f({c1})g'({c1})}}{{g({c1})^2}} = \dfrac{{({g1})({df1}) - ({f1})({dg1})}}{{{g1**2}}} = {sp.latex(kp)}$.",
             [(1, "quotient rule"), (1, "value")], work="2.2cm"),
        Part("c", rf"Write an equation for the line tangent to the graph of $h$ at $x = {c2}$.", expr(str(line)),
             rf"$h({c2}) = ({f2})({g2}) = {h2}$ and the slope is ${hp}$: $y - ({h2}) = {hp}(x - {c2})$.", [(1, "point and slope"), (1, "equation")],
             work="2cm"),
        Part("d", rf"Find $p'({c1})$.", num(pp),
             rf"$p'(x) = 2xf(x) + x^2f'(x)$, so $p'({c1}) = 2({c1})({f1}) + ({c1**2})({df1}) = {pp}$.", [(1, "product rule with $x^2$"), (1, "value")],
             work="2cm"),
    ], frq_type="Table of values / rates"), (hp, kp, line, pp)


F2A, t2A = table_frq(1, 2, {1: (3, 2, -2, 1), 2: (-1, 4, 5, -3)})
F2B, t2B = table_frq(1, 3, {1: (2, -1, 5, 2), 3: (4, 3, -2, 1)})
same("F2 A", list(t2A), [23, sp.Rational(-7, 4), 23 * x - 51, 8])
same("F2 B", list(t2B), [-2, sp.Rational(-9, 25), -2 * x - 2, 3])


def smooth_frq(left_tex, left, right_tex, right, c, steps):
    dl = D(left)
    lval, rval = left.subs(x, c), right.subs(x, c)
    sl, sr = dl.subs(x, c), D(right).subs(x, c)
    return FRQ("Continuity and differentiability", (
        rf"Let $f(x) = \begin{{cases}} {left_tex}, & x \le {c} \\ {right_tex}, & x > {c}. \end{{cases}}$"), [
        Part("a", rf"Use the limit definition of the derivative to find the derivative of $g(x) = {left_tex}$.", expr(str(dl)),
             "$g'(x) = $ " + limchain(0, steps, sp.latex(dl), var="h") + ".",
             [(1, "sets up the limit"), (1, "algebra and answer")], work="3cm"),
        Part("b", rf"Is $f$ continuous at $x = {c}$? Justify.", selfcheck(r"\text{Yes}"),
             rf"$f({c}) = {lval}$. The left piece heads to ${lval}$ and the right piece to ${rval}$, so the limit is ${lval} = f({c})$. Continuous.",
             [(1, "one-sided limits and value"), (1, "conclusion")], work="2.2cm"),
        Part("c", rf"Is $f$ differentiable at $x = {c}$? If so, enter $f'({c})$.", num(sl),
             rf"$f$ is continuous at ${c}$, the left slope is ${sl}$ and the right slope is ${sr}$. They match, so $f'({c}) = {sl}$.",
             [(1, "compares slopes"), (1, "continuity noted and answer")], work="2.2cm"),
    ], frq_type="Continuity"), (lval, rval, sl, sr, dl)


F3A, s3A = smooth_frq(r"x^2 + 1", x**2 + 1, r"2x", 2 * x, 1,
                      [r"\frac{(x+h)^2 + 1 - x^2 - 1}{h}", r"\frac{2xh + h^2}{h}", r"(2x + h)"])
F3B, s3B = smooth_frq(r"x^3", x**3, r"3x - 2", 3 * x - 2, 1,
                      [r"\frac{(x+h)^3 - x^3}{h}", r"\frac{3x^2h + 3xh^2 + h^3}{h}", r"(3x^2 + 3xh + h^2)"])
same("F3 A", list(s3A), [2, 2, 2, 2, 2 * x])
same("F3 B", list(s3B), [1, 1, 3, 3, 3 * x**2])
same("F3 defs", [sp.limit(((x + h)**2 + 1 - x**2 - 1) / h, h, 0), sp.limit(((x + h)**3 - x**3) / h, h, 0)], [2 * x, 3 * x**2])

TEST = UnitTest(unit=2, title="Differentiation: Definition and Fundamental Properties", mcq_a=A, mcq_b=B,
                frq=[Variants(F1A, F1B), Variants(F2A, F2B), Variants(F3A, F3B)])
