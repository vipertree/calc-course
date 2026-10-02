"""Topic 1.5: Determining limits using algebraic properties of limits.

CED: LIM-1.D (one-sided limits analytically or graphically; limit theorems for sums,
differences, products, quotients, composites). Includes the AP favourite: a product whose
limit exists although one factor's limit does not.
"""
import sympy as sp

from calclib import (VideoExample, Variants, FRQ, MCQ, BigIdea, Check, Example, FigureRow, Formula, Item, Part, Section, Table, limchain,
                     Text, Topic, Video, dne, num, same, selfcheck)
from calclib.figs import graph

x, t, k = sp.symbols("x t k")

# worked example 1: lim f = 3, lim g = -2
F, G = sp.Integer(3), sp.Integer(-2)
EX1 = [(r"2f(x) - g(x)", 2 * F - G), (r"f(x)\,g(x)", F * G), (r"\dfrac{f(x)}{g(x)}", F / G),
       (r"[f(x)]^2 + g(x)", F**2 + G), (r"\sqrt{f(x)+6}", sp.sqrt(F + 6))]
same("ex1 values", [v for _, v in EX1][2], sp.Rational(-3, 2))

FIG_F = graph("t1_5_f", [("x+1", -2, 1), ("-x", 1, 3)], xr=(-2, 3), yr=(-3, 3), open=[(1, 2)], closed=[(1, -1)],
              w="5.4cm", h="4.4cm", caption=r"The graph of $f$.")
FIG_G = graph("t1_5_g", [("x-1", -2, 3)], xr=(-2, 3), yr=(-3, 3), w="5.4cm", h="4.4cm", caption=r"The graph of $g$.")
# sympy's one-sided limits of Piecewise pick the wrong branch, so check each side with its own branch
fL, fR, gl = x + 1, -x, x - 1
same("fg left", sp.limit(fL * gl, x, 1), 0)
same("fg right", sp.limit(fR * gl, x, 1), 0)
same("f+g left", sp.limit(fL + gl, x, 1), 2)
same("f+g right", sp.limit(fR + gl, x, 1), -1)
same("f+g at 0", (fL + gl).subs(x, 0), 0)
same("f/g at 2", (fR / gl).subs(x, 2), -2)

same("pw left", sp.limit(x**2 + 1, x, 2), 5)
same("pw right", sp.limit(3 * x - 1, x, 2), 5)

ex1_rows = r" \qquad ".join(rf"({'abcde'[i]})\ \lim_{{x\to4}}\left[{e}\right]" for i, (e, v) in enumerate(EX1[:3])) + r" \\ " + \
    r" \qquad ".join(rf"({'abcde'[i + 3]})\ \lim_{{x\to4}}\left[{e}\right]" for i, (e, v) in enumerate(EX1[3:]))

NOTES = [
    Video("s1_5.py::Lesson", "The limit laws", 3.5),

    Section("The limit laws"),
    Formula("Limit laws", (
        r"If $\displaystyle \lim_{x\to c} f(x) = L$ and $\displaystyle \lim_{x\to c} g(x) = M$ both \blank{exist}, then"
        r"\[ \lim_{x\to c}[f(x)\pm g(x)] = L \pm M, \qquad \lim_{x\to c} k\,f(x) = kL, \qquad "
        r"\lim_{x\to c} f(x)\,g(x) = LM, \]"
        r"\[ \lim_{x\to c}\frac{f(x)}{g(x)} = \frac{L}{M}\ \text{ provided } \mblank{M \ne 0}, \qquad "
        r"\lim_{x\to c}[f(x)]^n = L^n. \]"
        r"The same laws hold for one-sided limits.")),
    VideoExample('Using given limits', work="3.2cm"),

    Section("Direct substitution"),
    Formula("Direct substitution", (
        r"If $p$ is a polynomial, $\displaystyle \lim_{x\to c} p(x) = \mblank{p(c)}$. If $r = \frac{p}{q}$ is rational and "
        r"$q(c) \ne 0$, then \[ \lim_{x\to c} r(x) = r(c). \] The same is true for roots, exponentials, logarithms "
        r"and trig functions at points in their domains.")),
    VideoExample('Plug in', work="2.4cm"),
    Formula("Composite functions", (
        r"If $\displaystyle \lim_{x\to c} g(x) = L$ and $f$ is continuous at $L$, then "
        r"\[ \lim_{x\to c} f(g(x)) = f\!\left(\lim_{x\to c} g(x)\right) = f(L). \] "
        r"For example, $\displaystyle \lim_{x\to3}\sqrt{x^2+7} = \sqrt{16} = \mblank{4}$.")),

    Section("Piecewise functions and one-sided limits"),
    Text(r"Let \[ f(x) = \begin{cases} x^2 + 1, & x < 2 \\ 3x - 1, & x \ge 2. \end{cases} \] Use the piece that lives on each side: "
         r"$\displaystyle \lim_{x\to2^-} f(x) = \mblank{5}$ and $\displaystyle \lim_{x\to2^+} f(x) = \mblank{5}$, "
         r"so $\displaystyle \lim_{x\to2} f(x) = \mblank{5}$."),

    Section("Limits from two graphs"),
    FigureRow([FIG_F, FIG_G]),
    Table(r"$\displaystyle \lim_{x\to1} f(x)$ & \blank{does not exist} & $\displaystyle \lim_{x\to1} g(x)$ & \mblank{0} \\ "
          r"$\displaystyle \lim_{x\to1}[f(x)\,g(x)]$ & \mblank{0} & $\displaystyle \lim_{x\to1}[f(x)+g(x)]$ & \blank{does not exist} \\ "
          r"$\displaystyle \lim_{x\to0}[f(x)+g(x)]$ & \mblank{0} & $\displaystyle \lim_{x\to2}\frac{f(x)}{g(x)}$ & \mblank{-2}",
          "cccc"),
    Text(r"The product law cannot be used at $x = 1$, because $\displaystyle \lim_{x\to1} f(x)$ does not exist. "
         r"Check each side instead: from the left, $f \to 2$ and $g \to 0$, so $fg \to 0$; from the right, $f\to -1$ and "
         r"$g \to 0$, so $fg \to 0$. Both sides agree."),
    BigIdea(r"Limits obey the rules of arithmetic, as long as each limit exists and no denominator heads to $0$. "
            r"When a law can't be used, go back to one-sided limits."),
    Check(r"Find \[ \lim_{x\to2}\frac{3x^2-5}{x+1}. \]", num(sp.Rational(7, 3)),
          r"The denominator is $3 \ne 0$ at $x=2$, so substitute: \[ \frac{12-5}{3} = \frac73. \]"),
]
same("ex2a", sp.limit(x**3 - 4 * x + 1, x, 2), 1)
same("ex2b", sp.limit((x**2 + 3) / (x - 2), x, -1), sp.Rational(-4, 3))
same("composite", sp.limit(sp.sqrt(x**2 + 7), x, 3), 4)
same("check", sp.limit((3 * x**2 - 5) / (x + 1), x, 2), sp.Rational(7, 3))

# ---------------------------------------------------------------- practice
FIG_P = graph("t1_5_p", [("0.5*x+1", -1, 2), ("3-x", 2, 4), ("4-x", -1, 4, "dashed")], xr=(-1, 4), yr=(-1.5, 5.5),
              open=[(2, 2)], closed=[(2, 1)], caption=r"$f$ (solid) and $g$ (dashed).")
fpL, fpR, gp = x / 2 + 1, 3 - x, 4 - x
same("p10 left", sp.limit(fpL * gp, x, 2), 4)
same("p11 left", sp.limit(gp.subs(x, fpL), x, 2), 2)
same("p11 right", sp.limit(gp.subs(x, fpR), x, 2), 3)
PRACTICE = [
    Item(r"Given $\displaystyle\lim_{x\to a} f(x) = 5$ and $\displaystyle\lim_{x\to a} g(x) = -1$, find "
         r"$\displaystyle\lim_{x\to a}[3f(x) + 2g(x)]$.", num(13), r"$3(5) + 2(-1) = 13$.", work="1.5cm"),
    Item(r"With the same limits, find $\displaystyle\lim_{x\to a} f(x)g(x)$.", num(-5), r"$5(-1) = -5$.", work="1.2cm"),
    Item(r"With the same limits, find $\displaystyle\lim_{x\to a}\frac{g(x)}{f(x)}$.", num(sp.Rational(-1, 5)),
         r"The denominator's limit is $5 \ne 0$: $\dfrac{-1}{5}$.", work="1.2cm"),
    Item(r"With the same limits, find $\displaystyle\lim_{x\to a}\sqrt{f(x) - 1}$.", num(2),
         r"$\sqrt{5 - 1} = 2$ (the square root is continuous at $4$).", work="1.2cm"),
    Item(r"Find $\displaystyle\lim_{x\to-2}(x^3 + 2x^2 - x + 4)$.", num(6), r"$-8 + 8 + 2 + 4 = 6$.", work="1.2cm"),
    Item(r"Find $\displaystyle\lim_{t\to\pi}(t\sin t + \cos t)$.", num(-1), r"$\pi\cdot 0 + (-1) = -1$.", work="1.2cm"),
    Item(r"Find $\displaystyle\lim_{x\to1}\frac{2x+1}{x^2+3}$.", num(sp.Rational(3, 4)), r"$\dfrac{3}{4}$.", work="1.2cm"),
    Item(r"Let $h(x) = \begin{cases} 2x + 3, & x < 1 \\ 2, & x = 1 \\ x^2 + 4, & x > 1. \end{cases}$ "
         r"Find $\displaystyle\lim_{x\to1} h(x)$.", num(5),
         r"Left: $2 + 3 = 5$. Right: $1 + 4 = 5$. The sides agree; $h(1) = 2$ doesn't matter.", work="1.8cm"),
    Item(r"Let $k(x) = \begin{cases} x^2, & x < 2 \\ 5 - x, & x \ge 2. \end{cases}$ Find $\displaystyle\lim_{x\to2} k(x)$, "
         r"or type DNE.", dne(), r"Left: $4$. Right: $3$. The limit does not exist.", work="1.5cm"),
    Item(r"The graphs of $f$ (solid) and $g$ (dashed) are shown. Find $\displaystyle\lim_{x\to2^-}[f(x)\,g(x)]$.",
         num(4), r"From the left, $f \to 2$ and $g \to 2$, so the product heads to $4$.", figure=FIG_P, work="1.4cm"),
    Item(r"Using the same graphs, find $\displaystyle\lim_{x\to2} g(f(x))$, or type DNE.", dne(),
         r"As $x\to2^-$, $f(x)\to2$, so $g(f(x)) \to g(2) = 2$. As $x \to 2^+$, $f(x) \to 1$, so $g(f(x)) \to g(1) = 3$. "
         r"The sides disagree.", work="2cm"),
]
same("p5", sp.limit(x**3 + 2 * x**2 - x + 4, x, -2), 6)
same("p6", sp.limit(t * sp.sin(t) + sp.cos(t), t, sp.pi), -1)
same("p7", sp.limit((2 * x + 1) / (x**2 + 3), x, 1), sp.Rational(3, 4))

# extra practice (round 1)
Fv, Gv = sp.Integer(-2), sp.Integer(6)      # lim f = -2, lim g = 6 for problems 12-15
PRACTICE += [
    Item(r"Given $\displaystyle\lim_{x\to c} f(x) = -2$ and $\displaystyle\lim_{x\to c} g(x) = 6$, find "
         r"$\displaystyle\lim_{x\to c}\left[f(x)^3 + g(x)\right]$.", num(Fv**3 + Gv),
         rf"$\displaystyle\lim_{{x\to c}}f(x)^3 + \lim_{{x\to c}}g(x) = (-2)^3 + 6 = {Fv**3 + Gv}$.", work="1.6cm"),
    Item(r"With the same limits, find $\displaystyle\lim_{x\to c}\frac{g(x)}{f(x) + 5}$.", num(Gv / (Fv + 5)),
         rf"The denominator's limit is $-2 + 5 = 3 \ne 0$: $\dfrac{{6}}{{3}} = {sp.latex(Gv / (Fv + 5))}$.", work="1.6cm"),
    Item(r"With the same limits, find $\displaystyle\lim_{x\to c}\sqrt{g(x) - 2f(x)}$.", num(sp.sqrt(Gv - 2 * Fv)),
         rf"$\sqrt{{6 - 2(-2)}} = \sqrt{{10}}$.", work="1.4cm"),
    Item(r"With the same limits, can the quotient law give $\displaystyle\lim_{x\to c}\frac{g(x)}{f(x) + 2}$? Explain.",
         selfcheck(r"\text{No: denominator limit is } 0"),
         r"No. $\displaystyle\lim_{x\to c}[f(x) + 2] = 0$, and the quotient law requires a nonzero denominator limit.", work="1.6cm"),
    Item(r"Find $\displaystyle\lim_{x\to4}\left(3\sqrt{x} - x^2\right)$.", num(-10), r"Substitute: $3(2) - 16 = -10$.", work="1.2cm"),
    Item(r"Find $\displaystyle\lim_{x\to0}\frac{e^x + \cos x}{x + 2}$.", num(1), r"Substitute: $\dfrac{1 + 1}{2} = 1$.", work="1.2cm"),
    Item(r"Find $\displaystyle\lim_{x\to-1}\left(x^2 + 1\right)^3$.", num(8), r"The composite rule: $(1 + 1)^3 = 8$.", work="1.2cm"),
    Item(r"Let $p(x) = \begin{cases} 3 - x, & x < 2 \\ \sqrt{x + 2}, & x \ge 2. \end{cases}$ Find $\displaystyle\lim_{x\to2} p(x)$, or type DNE.",
         dne(), limchain(2, [r"(3-x)"], 1, side="^-") + r" and " + limchain(2, [r"\sqrt{x+2}"], 2, side="^+") + r". The sides disagree.",
         work="1.8cm"),
    Item(r"Let $q(x) = \begin{cases} x^2 - 5, & x < 3 \\ kx - 2, & x \ge 3. \end{cases}$ For what $k$ does $\displaystyle\lim_{x\to3} q(x)$ exist?",
         num(2), r"Left: $9 - 5 = 4$. Right: $3k - 2$. Set $3k - 2 = 4$: $k = 2$.", work="1.8cm"),
    Item(r"If $\displaystyle\lim_{x\to1}[3f(x) - 2] = 7$, find $\displaystyle\lim_{x\to1}f(x)$.", num(3),
         r"$3L - 2 = 7$, so $L = 3$.", work="1.4cm"),
]
k_ = sp.symbols("k_")
same("p19", sp.solve(sp.Eq(3 * k_ - 2, 4), k_)[0], 2)
same("p15", [sp.limit(3 * sp.sqrt(x) - x**2, x, 4), sp.limit((sp.exp(x) + sp.cos(x)) / (x + 2), x, 0)], [-10, 1])

# ---------------------------------------------------------------- quiz
LAW = {"C": "the value $g(c)$ is irrelevant; the limit of $g$ matters", "D": "values at $c$ don't matter"}
QUIZ = [
    Variants(
        Item(r"If $\displaystyle\lim_{x\to2} f(x) = 4$ and $\displaystyle\lim_{x\to2} g(x) = -3$, find "
             r"$\displaystyle\lim_{x\to2}\left([f(x)]^2 - 2g(x)\right)$.", num(22), r"$16 + 6 = 22$.", work="1.6cm"),
        Item(r"If $\displaystyle\lim_{x\to5} f(x) = -2$ and $\displaystyle\lim_{x\to5} g(x) = 6$, find "
             r"$\displaystyle\lim_{x\to5}\left(3f(x) + f(x)g(x)\right)$.", num(-18), r"$3(-2) + (-2)(6) = -6 - 12 = -18$.", work="1.6cm"),
        Item(r"If $\displaystyle\lim_{x\to0} f(x) = 9$ and $\displaystyle\lim_{x\to0} g(x) = 2$, find "
             r"$\displaystyle\lim_{x\to0}\frac{\sqrt{f(x)}}{g(x) + 1}$.", num(1), r"$\dfrac{\sqrt9}{2 + 1} = \dfrac33 = 1$.", work="1.6cm"),
    ),
    Variants(
        Item(r"Find $\displaystyle\lim_{x\to3}\frac{x^2 - 2x}{x+1}$.", num(sp.Rational(3, 4)), r"$\dfrac{9-6}{4} = \dfrac34$.", work="1.6cm"),
        Item(r"Find $\displaystyle\lim_{x\to-2}\frac{x^2 + 3x}{x - 1}$.", num(sp.Rational(2, 3)), r"$\dfrac{4-6}{-3} = \dfrac23$.", work="1.6cm"),
        Item(r"Find $\displaystyle\lim_{x\to4}\left(x\sqrt{x} - \frac{8}{x}\right)$.", num(6), r"$4 \cdot 2 - 2 = 6$.", work="1.6cm"),
    ),
    Variants(
        Item(r"Let $p(x) = \begin{cases} 4 - x^2, & x \le -1 \\ 2x + 5, & x > -1. \end{cases}$ Find "
             r"$\displaystyle\lim_{x\to-1} p(x)$.", num(3), r"Left: $4 - 1 = 3$. Right: $-2 + 5 = 3$.", work="1.6cm"),
        Item(r"Let $p(x) = \begin{cases} x^2 + 1, & x < 2 \\ 3x - 1, & x \ge 2. \end{cases}$ Find "
             r"$\displaystyle\lim_{x\to2} p(x)$.", num(5), r"Left: $4 + 1 = 5$. Right: $6 - 1 = 5$.", work="1.6cm"),
        Item(r"Let $p(x) = \begin{cases} 2x - 1, & x < 3 \\ x^2 - 5, & x \ge 3. \end{cases}$ Find "
             r"$\displaystyle\lim_{x\to3} p(x)$, or type DNE.", dne(), r"Left: $6 - 1 = 5$. Right: $9 - 5 = 4$. They disagree.",
             work="1.6cm"),
    ),
    Variants(
        MCQ(r"When can the quotient law $\displaystyle\lim_{x\to c}\frac{f(x)}{g(x)} = \frac{\lim f(x)}{\lim g(x)}$ be used?",
            [r"Always", r"When both limits exist and $\displaystyle\lim_{x\to c} g(x) \ne 0$", r"When $g(c) \ne 0$",
             r"When $f(c)$ and $g(c)$ both exist"], "B",
            r"Both limits must exist, and the denominator's limit must not be $0$.", why_not=LAW),
        MCQ(r"$\displaystyle\lim_{x\to1} f(x) = 3$ and $\displaystyle\lim_{x\to1} g(x) = 0$. What can you say about "
            r"$\displaystyle\lim_{x\to1}\frac{f(x)}{g(x)}$?",
            [r"It equals $0$.", r"It equals $3$.", r"The quotient law can't be used, and the limit is not a finite number.",
             r"It equals $\frac30$."], "C",
            r"The denominator's limit is $0$ and the numerator's is not, so the quotient law doesn't apply. The quotient grows without "
            r"bound, so it has no finite limit.", why_not={"D": "$\\frac30$ is not a number", "A": "the numerator heads to $3$, not $0$"}),
        MCQ(r"Which limit law explains $\displaystyle\lim_{x\to c} 5f(x) = 5\lim_{x\to c} f(x)$?",
            [r"The sum law", r"The constant multiple law", r"The quotient law", r"The power law"], "B",
            r"A constant factor can be pulled out of a limit.", why_not={"D": "no power appears"}),
    ),
    Variants(
        MCQ(r"If $\displaystyle\lim_{x\to0} g(x) = 8$, what is $\displaystyle\lim_{x\to0}\sqrt[3]{g(x)} + g(x)$?",
            [r"$2$", r"$8$", r"$10$", r"$16$"], "C", r"$\sqrt[3]{8} + 8 = 2 + 8 = 10$.",
            why_not={"A": "left off the $+g(x)$", "D": "doubled $8$"}),
        MCQ(r"If $\displaystyle\lim_{x\to2} g(x) = 25$, what is $\displaystyle\lim_{x\to2}\left(\sqrt{g(x)} - 3\right)^2$?",
            [r"$4$", r"$22$", r"$484$", r"$2$"], "A", r"$(\sqrt{25} - 3)^2 = 2^2 = 4$.",
            why_not={"B": "forgot the square root", "D": "forgot to square"}),
        MCQ(r"If $\displaystyle\lim_{x\to\pi} g(x) = 0$, what is $\displaystyle\lim_{x\to\pi}\cos\left(g(x)\right)$?",
            [r"$0$", r"$-1$", r"$\pi$", r"$1$"], "D", r"Cosine is continuous, so the limit is $\cos 0 = 1$.",
            why_not={"B": "that's $\\cos\\pi$; the inside heads to $0$, not $\\pi$", "A": "that's the inside limit"}),
    ),
]
same("q1", 4**2 - 2 * (-3), 22)
same("q2", sp.limit((x**2 - 2 * x) / (x + 1), x, 3), sp.Rational(3, 4))
same("q versions", [3 * -2 + (-2) * 6, sp.limit((x**2 + 3 * x) / (x - 1), x, -2), sp.limit(x * sp.sqrt(x) - 8 / x, x, 4)], [-18, sp.Rational(2, 3), 6])

# ---------------------------------------------------------------- test prep
FIG_M = graph("t1_5_m1", [("x+2", -2, 0), ("x-1", 0, 2), ("x^2", -1.9, 1.9, "dashed")], xr=(-2, 2), yr=(-1.5, 3.8),
              open=[(0, 2)], closed=[(0, -1)], caption=r"$f$ (solid) and $g$ (dashed).")
MCQS = [
    MCQ(r"The graphs of $f$ (solid) and $g$ (dashed) are shown. What is $\displaystyle\lim_{x\to0}[f(x)\,g(x)]$?",
        [r"$0$", r"$-2$", r"$2$", r"Does not exist."], "A",
        r"$g(x) \to 0$ from both sides while $f$ stays bounded ($2$ from the left, $-1$ from the right). Each one-sided "
        r"product heads to $0$.",
        why_not={"D": "$\\lim f$ doesn't exist, but the product's limit can still exist"}, figure=FIG_M),
    MCQ(r"If $\displaystyle\lim_{x\to3}[2f(x) + x^2] = 5$, what is $\displaystyle\lim_{x\to3} f(x)$?",
        [r"$-7$", r"$-2$", r"$2$", r"$7$"], "B", r"$2L + 9 = 5$, so $L = -2$.",
        why_not={"A": "forgot to divide by $2$", "C": "sign error moving $9$"}),
    MCQ(r"$\displaystyle\lim_{x\to\pi/2}\frac{\sin x}{1 + \cos x}$ is", [r"$0$", r"$\dfrac12$", r"$1$", r"Does not exist"], "C",
        r"Direct substitution: $\dfrac{1}{1+0} = 1$."),
    MCQ(r"Let $f(x) = \begin{cases} x^2 + k, & x < 3 \\ 4x - 1, & x \ge 3. \end{cases}$ For what value of $k$ does "
        r"$\displaystyle\lim_{x\to3} f(x)$ exist?", [r"$-2$", r"$0$", r"$1$", r"$2$"], "D",
        r"Match the one-sided limits: $9 + k = 11$, so $k = 2$.", why_not={"A": "sign error"}),
]
same("m3", sp.limit(sp.sin(x) / (1 + sp.cos(x)), x, sp.pi / 2), 1)
same("m4", sp.solve(sp.Eq(9 + k, 11), k)[0], 2)

FRQS = [
    FRQ("Limit laws", (
        r"The functions $f$ and $g$ satisfy $\displaystyle\lim_{x\to1} f(x) = 3$ and $\displaystyle\lim_{x\to1} g(x) = -2$."), [
        Part("a", r"Find $\displaystyle\lim_{x\to1}[f(x)\,g(x) - 4x]$. Show the work that leads to your answer.", num(-10),
             r"$\displaystyle\lim_{x\to1} f(x)g(x) - \lim_{x\to1}4x = (3)(-2) - 4 = -10$.",
             [(1, "uses the product and difference laws"), (1, "answer $-10$")], work="2.5cm"),
        Part("b", r"Can the quotient law be used to find $\displaystyle\lim_{x\to1}\frac{f(x)}{g(x)+2}$? Explain.",
             selfcheck(r"\text{No}"),
             r"No. $\displaystyle\lim_{x\to1}[g(x)+2] = 0$, and the quotient law requires the denominator's limit to be nonzero.",
             [(1, "no, because the limit of the denominator is $0$")], work="2cm"),
        Part("c", r"Let $k(x) = \begin{cases} f(x), & x < 1 \\ x^2 + c, & x > 1 \end{cases}$ for a constant $c$. Find the "
                  r"value of $c$ for which $\displaystyle\lim_{x\to1} k(x)$ exists. Justify your answer.", num(2),
             r"$\displaystyle\lim_{x\to1^-}k(x) = 3$ and $\displaystyle\lim_{x\to1^+}k(x) = 1 + c$. The limit exists when "
             r"$1 + c = 3$, so $c = 2$.",
             [(1, "sets the one-sided limits equal"), (1, "$c = 2$")], work="2.5cm"),
    ], frq_type="Limits from given information"),
]

TOPIC = Topic(
    number="1.5", title="Determining Limits Using Algebraic Properties of Limits",
    unit="Unit 1: Limits and Continuity", ced=["LIM-1.D", "LIM-1.D.1", "LIM-1.D.2"],
    goals=r"Use the limit laws and direct substitution to find limits of sums, products, quotients, composites and "
          r"piecewise functions.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
