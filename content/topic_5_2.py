"""Topic 5.2: Extreme Value Theorem, global versus local extrema, and critical points.

CED: FUN-1.C (FUN-1.C.1-1.C.3): a continuous function on a closed interval has an absolute max and min (EVT); local extrema
happen only at critical points (f' = 0 or f' undefined), but not every critical point is an extremum.
Worked examples: critical points of x^3 - 3x^2, of x^(2/3)(x - 5) (one where f' is undefined), and an EVT check (1/x on [-1, 1]).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Text, Topic, Variants, Video, num,
                     same, selfcheck)
from calclib.figs import graph

x = sp.symbols("x", real=True)


def crit(f):
    """Critical points: zeros of f' plus points in the domain of f where f' is undefined."""
    d = sp.together(sp.diff(f, x))
    zs = sp.solve(sp.numer(d), x)
    us = [u for u in sp.solve(sp.denom(d), x) if f.subs(x, u).is_finite]
    return sorted(set(zs + us))


same("ex1", crit(x**3 - 3 * x**2), [0, 2])
same("ex2", crit(sp.cbrt(x)**2 * (x - 5)), [0, 2])

NOTES = [
    Video("s5_2.py::Lesson", "Highest and lowest points", 4),

    Section("Absolute and relative extrema"),
    Text(r"An \blank{absolute} (global) maximum is the largest value $f$ takes on its whole domain or interval. A \blank{relative} (local) maximum "
         r"is larger than every value nearby. Minimums are the same, with smallest."),
    graph("t5_2_pic", [("0.3*x^3 - 1.8*x^2 + 2.7*x + 1", -0.3, 4.6)], (-0.5, 5), (-1, 5), closed=[(-0.3, 0.02), (1, 2.2), (3, 1), (4.6, 4.53)],
          labels=[(1, 2.2, "above", "rel. max"), (3, 1, "below", "rel. min"), (4.6, 4.53, "left", "abs. max"), (-0.3, 0.02, "right", "abs. min")],
          caption="Extrema of a function on a closed interval."),

    Section("The Extreme Value Theorem"),
    Formula("Extreme Value Theorem (EVT)", (
        r"If $f$ is \blank{continuous} on the \blank{closed} interval $[a, b]$, then $f$ has both an absolute maximum and an absolute minimum on $[a, b]$.")),
    Text(r"Both conditions matter. $f(x) = x$ on the open interval $(0, 1)$ has no maximum: it gets close to $1$ but never reaches it. "
         r"$f(x) = \frac1x$ on $[-1, 1]$ isn't continuous at $0$, and it has no maximum."),

    Section("Critical points"),
    Formula("Critical point", (
        r"A \blank{critical point} of $f$ is an $x = c$ in the domain of $f$ where \[ f'(c) = 0 \quad \text{or} \quad f'(c) \text{ is undefined.} \]")),
    Text(r"Relative extrema can only happen at critical points: at a smooth peak the tangent is \blank{horizontal}, and at a sharp peak (a corner or cusp) "
         r"there is no tangent at all. But a critical point need not be an extremum: $f(x) = x^3$ has $f'(0) = 0$ and keeps rising through $0$."),
    VideoExample('Find the critical points', work="2.4cm"),
    BigIdea(r"Continuous on a closed interval: an absolute max and min are guaranteed. Relative extrema hide at critical points, where $f' = 0$ or $f'$ is undefined."),
    Check(r"Find the critical point of $f(x) = x^2 - 6x + 1$.", num(3), r"$f'(x) = 2x - 6 = 0$ at $x = 3$."),
]

# ---------------------------------------------------------------- practice
P = [x**3 - 12 * x, x**2 - 10 * x + 4, 2 * x**3 + 3 * x**2 - 36 * x, x**4 - 2 * x**2, x * sp.exp(-x), x - 2 * sp.log(x), sp.Abs(x - 4), sp.cbrt(x) * (x - 4)]
ANS = [[-2, 2], [5], [-3, 2], [-1, 0, 1], [1], [2], [4], [0, 1]]
PRACTICE = []
for f, ans in zip(P, ANS):
    many = len(ans) > 1
    d = sp.diff(f, x) if not isinstance(f, sp.Abs) else None
    sol = (rf"$f'(x) = {sp.latex(sp.factor(sp.together(d)))}$. " if d is not None else r"$f$ has a corner at $x = 4$, where $f'$ is undefined. ") + \
        rf"Critical point{'s' if many else ''}: $x = {', '.join(str(a) for a in ans)}$."
    PRACTICE.append(Item(rf"Find all critical points of $f(x) = {sp.latex(f)}$." + (" Enter the largest." if many else ""), num(ans[-1]), sol, work="2.2cm"))
same("p", [crit(f) for f in P if not isinstance(f, sp.Abs)], [a for f, a in zip(P, ANS) if not isinstance(f, sp.Abs)])
PRACTICE += [
    Item(r"Does the Extreme Value Theorem guarantee an absolute maximum for $f(x) = \dfrac{1}{x - 2}$ on $[0, 3]$? Explain.", selfcheck(r"\text{no}"),
         r"No: $f$ is not continuous at $x = 2$, which is in $[0, 3]$.", work="1.6cm"),
    Item(r"Does the Extreme Value Theorem guarantee an absolute maximum for $f(x) = x^2$ on $(0, 2)$? Explain.", selfcheck(r"\text{no}"),
         r"No: the interval is open. (Indeed $x^2$ gets close to $4$ but never reaches it there.)", work="1.6cm"),
    Item(r"Does the Extreme Value Theorem guarantee an absolute maximum for $f(x) = e^{x}\cos x$ on $[0, \pi]$? Explain.", selfcheck(r"\text{yes}"),
         r"Yes: $f$ is continuous on the closed interval $[0, \pi]$.", work="1.6cm"),
    Item(r"Malik says $x = 0$ is a relative minimum of $f(x) = x^3$, because $f'(0) = 0$. Is he right?", selfcheck(r"\text{no}"),
         r"No. $f'(0) = 0$ makes $0$ a critical point, but $x^3$ increases through $0$: $f(x) < 0$ just left of $0$ and $f(x) > 0$ just right. It is not an extremum.", work="1.8cm"),
]

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(*[Item(rf"Find all critical points of $f(x) = {sp.latex(f)}$. Enter the largest.", num(crit(f)[-1]),
                    rf"$f'(x) = {sp.latex(sp.factor(sp.diff(f, x)))} = 0$ at $x = {', '.join(sp.latex(c) for c in crit(f))}$.", work="2cm")
               for f in (x**3 - 27 * x, x**3 - 3 * x**2 - 9 * x, 2 * x**3 - 6 * x)]),
    Variants(*[Item(rf"Find the critical point of $f(x) = {sp.latex(f)}$.", num(crit(f)[0]), rf"$f'(x) = {sp.latex(sp.factor(sp.together(sp.diff(f, x))))}$.", work="1.8cm")
               for f in (x * sp.exp(2 * x), x * sp.exp(-3 * x), x - sp.log(x))]),
    Variants(
        MCQ(r"On which interval does the Extreme Value Theorem guarantee that $f(x) = \dfrac{1}{x}$ has an absolute maximum?", [r"$(0, 1)$", r"$[-1, 1]$", r"$[1, 2]$", r"$(1, 2)$"], "C",
            r"Only $[1, 2]$ is closed and avoids the discontinuity at $0$."),
        MCQ(r"On which interval does the Extreme Value Theorem guarantee that $f(x) = \tan x$ has an absolute maximum?", [r"$\left[0, \frac\pi4\right]$", r"$[0, \pi]$", r"$\left(0, \frac\pi4\right)$", r"$\left[0, \frac\pi2\right)$"], "A",
            r"Only $\left[0, \frac\pi4\right]$ is closed and avoids the asymptote at $\frac\pi2$."),
        MCQ(r"On which interval does the Extreme Value Theorem guarantee that $f(x) = \ln x$ has an absolute minimum?", [r"$(0, 1]$", r"$(1, e)$", r"$[0, e]$", r"$[1, e]$"], "D",
            r"Only $[1, e]$ is closed and inside the domain."),
    ),
    Variants(
        MCQ(r"$f'(c) = 0$. Which must be true?", [r"$f$ has a relative maximum at $c$", r"$c$ is a critical point of $f$", r"$f$ has a relative extremum at $c$", r"$f(c) = 0$"], "B",
            r"$f'(c) = 0$ is the definition of a critical point; $x^3$ at $0$ shows it need not be an extremum."),
        MCQ(r"$f$ is differentiable and has a relative minimum at $x = 4$. Which must be true?", [r"$f(4) = 0$", r"$f''(4) = 0$", r"$f'(4) = 0$", r"$f'(4) > 0$"], "C",
            r"A differentiable function has a horizontal tangent at a relative extremum."),
        MCQ(r"Which function has a critical point at $x = 0$ that is NOT a relative extremum?", [r"$x^2$", r"$|x|$", r"$x^4$", r"$x^3$"], "D",
            r"$x^3$ has $f'(0) = 0$ and increases through $0$."),
    ),
    Variants(
        Item(r"$f(x) = x^{2/3}$. Find the critical point and say why it is one.", num(0), r"$f'(x) = \frac{2}{3x^{1/3}}$ is undefined at $x = 0$, which is in the domain.", work="1.6cm"),
        Item(r"$f(x) = |x + 3|$. Find the critical point and say why it is one.", num(-3), r"$f$ has a corner at $x = -3$, where $f'$ is undefined.", work="1.6cm"),
        Item(r"$f(x) = (x - 1)^{1/3}$. Find the critical point and say why it is one.", num(1), r"$f'(x) = \frac{1}{3(x - 1)^{2/3}}$ is undefined at $x = 1$, which is in the domain.", work="1.6cm"),
    ),
]
same("q", [crit(x * sp.exp(2 * x)), crit(x * sp.exp(-3 * x)), crit(x - sp.log(x))], [[sp.Rational(-1, 2)], [sp.Rational(1, 3)], [1]])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"How many critical points does $f(x) = x^4 - 4x^3$ have?", [r"$1$", r"$3$", r"$2$", r"$0$"], "C", r"$f'(x) = 4x^2(x - 3)$: $x = 0$ and $x = 3$."),
    MCQ(r"The derivative of $f$ is $f'(x) = \dfrac{x - 2}{(x + 1)^{1/3}}$, and $f$ is continuous everywhere. The critical points of $f$ are",
        [r"$x = 2$ only", r"$x = -1$ only", r"$x = 2$ and $x = 1$", r"$x = -1$ and $x = 2$"], "D", r"$f' = 0$ at $2$; $f'$ is undefined at $-1$, which is in the domain."),
    MCQ(r"Which statement is guaranteed by the Extreme Value Theorem?", [r"$f(x) = x^2$ has an absolute maximum on $[-1, 3]$", r"$f(x) = x^2$ has an absolute maximum on $(-1, 3)$",
        r"$f(x) = \frac{1}{x}$ has an absolute maximum on $[-1, 3]$", r"$f(x) = x^2$ has an absolute maximum on $(-\infty, \infty)$"], "A", r"Continuous on a closed interval."),
    MCQ(r"$g$ is differentiable everywhere. Which could be the set of $x$-values where $g$ has relative extrema?", [r"$\{0, 2\}$, where $g'(0) = 0$ and $g'(2) = 5$",
        r"$\{-1, 3\}$, where $g'(-1) = 0$ and $g'(3) = 0$", r"$\{1\}$, where $g'(1) = -2$", r"$\{4\}$, where $g'(4)$ is undefined"], "B", r"At a relative extremum, a differentiable $g$ has $g' = 0$."),
]

FRQS = [
    FRQ("Critical points from a formula", (r"Let $f(x) = x^{2/3}(x - 5)$ for all real $x$. Then \[ f'(x) = \frac{5(x - 2)}{3x^{1/3}}. \]"), [
        Part("a", r"Find the critical points of $f$. Explain why each is a critical point. Enter the larger one.", num(2),
             r"$f'(2) = 0$, and $f'(0)$ is undefined while $f(0) = 0$ is defined. So $x = 0$ and $x = 2$.", [(1, "$x = 2$ from $f' = 0$"), (1, "$x = 0$ from $f'$ undefined")], work="2.2cm"),
        Part("b", r"Does the Extreme Value Theorem guarantee that $f$ has an absolute minimum on $[-1, 4]$? Explain.", selfcheck(r"\text{yes}"),
             r"Yes: $f$ is continuous (a product of continuous functions) on the closed interval $[-1, 4]$.", [(1, "yes, continuous on a closed interval")], work="1.8cm"),
        Part("c", r"Find $f(-1)$, $f(0)$, $f(2)$ and $f(4)$. Which is smallest? (Topic 5.5 shows why that is the absolute minimum on $[-1, 4]$.) Enter the smallest value.", num(-6),
             r"$f(-1) = -6$, $f(0) = 0$, $f(2) = -3\cdot 2^{2/3} \approx -4.762$, $f(4) = -4^{2/3} \approx -2.520$. The smallest is $-6$.", [(1, "values"), (1, "smallest")], work="2.4cm"),
    ], frq_type="Analyzing a function"),
]
fr = lambda v: sp.real_root(sp.Integer(v)**2, 3) * (v - 5)
same("frq", [fr(-1), fr(0), fr(2), fr(4)], [-6, 0, -3 * 2**sp.Rational(2, 3), -(4**sp.Rational(2, 3))])

TOPIC = Topic(
    number="5.2", title="Extreme Value Theorem, Global Versus Local Extrema, and Critical Points",
    unit="Unit 5: Analytical Applications of Differentiation", ced=["FUN-1.C", "FUN-1.C.1", "FUN-1.C.2", "FUN-1.C.3"],
    goals=r"Tell absolute from relative extrema, use the Extreme Value Theorem, and find critical points.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
