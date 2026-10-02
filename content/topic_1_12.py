"""Topic 1.12: Confirming continuity over an interval.

CED: LIM-2.B.1 (continuous on an interval = continuous at each point), LIM-2.B.2 (polynomial,
rational, power, exponential, logarithmic and trig functions are continuous on their domains).
"""
import sympy as sp

from calclib import (VideoExample, Variants, FRQ, MCQ, BigIdea, Check, Definition, Example, Formula, Item, Part, Section, Text, Topic,
                     Video, num, same, selfcheck)

x, a = sp.symbols("x a")
same("seam", [sp.limit(x**2, x, 1), sp.limit(2 - x, x, 1)], [1, 1])

NOTES = [
    Video("s1_12.py::Lesson", "Continuity on an interval", 2.5),

    Section("Continuity on an interval"),
    Definition("Continuous on an interval", (
        r"A function is \textbf{continuous on an interval} if it is continuous at \blank{every point} of the interval. On a closed "
        r"interval $[a, b]$, continuity at the endpoints means \blank{one-sided} continuity: from the right at $a$ and from the "
        r"left at $b$.")),
    Formula("Functions that are continuous on their domains", (
        r"Polynomials, rational functions, powers and roots, exponentials, logarithms, $\sin x$, $\cos x$ and $\tan x$ are "
        r"continuous at every point in their \blank{domains}.\par "
        r"Sums, differences, products and \blank{compositions} of continuous functions are continuous; quotients are too, "
        r"except where the \blank{denominator is zero}.")),

    Section("Finding intervals of continuity"),
    VideoExample('Read the domain', work="2.8cm"),
    VideoExample('Logs and trig', work="2.8cm"),

    Section("Piecewise functions: check the seams"),
    Text(r"For \[ p(x) = \begin{cases} x^2, & x < 1 \\ 2 - x, & x \ge 1, \end{cases} \] each piece is a polynomial, so the only "
         r"place to check is the seam $x = 1$: left limit $\mblank{1}$, right limit $\mblank{1}$, $p(1) = \mblank{1}$. "
         r"So $p$ is continuous on \mblank{(-\infty, \infty)}."),
    BigIdea(r"To confirm continuity on an interval: check the domain of each formula, then check every seam where the formula changes."),
    Check(r"At how many $x$-values is $\displaystyle r(x) = \dfrac{x+2}{x^2-5x+6}$ discontinuous?", num(2),
          r"$x^2 - 5x + 6 = (x-2)(x-3)$, so $r$ is discontinuous at $x = 2$ and $x = 3$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"On which interval is $f(x) = \sqrt{5 - x}$ continuous? Enter the right endpoint.", num(5),
         r"$(-\infty, 5]$, with left-sided continuity at $5$.", work="1.4cm"),
    Item(r"At how many $x$-values is $g(x) = \dfrac{x}{x^2 - 16}$ discontinuous?", num(2), r"At $x = \pm4$.", work="1.4cm"),
    Item(r"Where is $h(x) = \ln(x + 3)$ continuous? Enter the left endpoint of the interval.", num(-3), r"$(-3, \infty)$.",
         work="1.4cm"),
    Item(r"Where is $k(x) = \dfrac{1}{\sqrt{x} - 2}$ continuous?", selfcheck(r"[0,4)\cup(4,\infty)"),
         r"Need $x \ge 0$ and $\sqrt x \ne 2$: $[0, 4) \cup (4, \infty)$.", work="1.6cm"),
    Item(r"Where is $m(x) = e^{1/x}$ continuous?", selfcheck(r"x \ne 0"),
         r"$\frac1x$ is continuous for $x \ne 0$ and $e^u$ everywhere, so the composition is continuous for $x \ne 0$.", work="1.6cm"),
    Item(r"Let $p(x) = \begin{cases} x + 3, & x < 0 \\ 3\cos x, & 0 \le x \le \pi \\ x - \pi - 3, & x > \pi. \end{cases}$ "
         r"At how many seams is $p$ discontinuous?", num(0),
         r"At $0$: $3$, $3\cos0 = 3$, $p(0)=3$. At $\pi$: $3\cos\pi = -3$ and $\pi - \pi - 3 = -3$. Continuous everywhere.",
         work="2.4cm"),
    Item(r"Find $a$ so that $q(x) = \begin{cases} ax^2, & x \le 2 \\ 4x - 4, & x > 2 \end{cases}$ is continuous on "
         r"$(-\infty, \infty)$.", num(1), r"$4a = 4$, so $a = 1$.", work="1.8cm"),
    Item(r"Is $\dfrac{\sin x}{x}$ continuous on $[1, 5]$? Explain.", selfcheck(r"\text{Yes}"),
         r"Yes. It is a quotient of continuous functions and the denominator is never $0$ on $[1, 5]$.", work="1.6cm"),
]
same("p6 at 0", [sp.limit(x + 3, x, 0), 3 * sp.cos(0)], [3, 3])
same("p6 at pi", [3 * sp.cos(sp.pi), sp.pi - sp.pi - 3], [-3, -3])
same("p7", sp.solve(sp.Eq(4 * a, 4), a)[0], 1)

# extra practice (round 1)
PRACTICE += [
    Item(r"At how many $x$-values is $f(x) = \dfrac{x + 1}{x^2 - 5x + 6}$ discontinuous?", num(2),
         r"$x^2 - 5x + 6 = (x-2)(x-3)$ is $0$ at $x = 2$ and $x = 3$. A rational function is continuous everywhere else.",
         work="1.4cm"),
    Item(r"At how many $x$-values is $g(x) = \dfrac{3x}{x^2 + 4}$ discontinuous?", num(0),
         r"$x^2 + 4 \ge 4$, so the denominator is never $0$. The domain is all reals and $g$ is continuous everywhere.",
         work="1.4cm"),
    Item(r"Where is $h(x) = \sqrt{2x - 6}$ continuous? Enter the left endpoint of the interval.", num(3),
         r"Need $2x - 6 \ge 0$, so $x \ge 3$. $h$ is continuous on $[3, \infty)$, from the right at $3$.", work="1.4cm"),
    Item(r"Where is $k(x) = \ln(4 - x^2)$ continuous?", selfcheck(r"(-2,2)"),
         r"Need $4 - x^2 > 0$, so $-2 < x < 2$. $k$ is continuous on $(-2, 2)$.", work="1.6cm"),
    Item(r"Where is $m(x) = \tan x$ continuous on $[0, 2\pi]$? Enter how many points of that interval it is discontinuous at.",
         num(2),
         r"$\tan x = \frac{\sin x}{\cos x}$ fails only where $\cos x = 0$: $x = \frac\pi2$ and $x = \frac{3\pi}2$.", work="1.6cm"),
    Item(r"Find $a$ so that $n(x) = \begin{cases} 2x + a, & x < 1 \\ x^2 + 4, & x \ge 1 \end{cases}$ is continuous on "
         r"$(-\infty, \infty)$.", num(3),
         r"Each piece is a polynomial, so only the seam matters. Match at $x = 1$: $2 + a = 5$, so $a = 3$.", work="1.8cm"),
    Item(r"Find $a$ so that $r(x) = \begin{cases} a\sin x, & x < \frac\pi2 \\ x - \frac\pi2 + 6, & x \ge \frac\pi2 \end{cases}$ "
         r"is continuous on $(-\infty, \infty)$.", num(6),
         r"Match at $x = \frac\pi2$: $a\sin\frac\pi2 = a$ and $\frac\pi2 - \frac\pi2 + 6 = 6$, so $a = 6$.", work="1.8cm"),
    Item(r"Let $s(x) = \begin{cases} x^2, & x < 1 \\ 2x - 1, & 1 \le x < 3 \\ 10 - x, & x \ge 3. \end{cases}$ "
         r"At how many seams is $s$ discontinuous?", num(1),
         r"At $x = 1$: $1^2 = 1$ and $2(1) - 1 = 1$, so $s$ is continuous there. At $x = 3$: the left-hand limit is "
         r"$2(3) - 1 = 5$ but the right-hand limit is $10 - 3 = 7$, so $s$ jumps. One seam.", work="2.4cm"),
    Item(r"Is $f(x) = \dfrac{x - 2}{x^2 - 4}$ continuous on $[0, 3]$? Explain.", selfcheck(r"\text{No}"),
         r"No. $x = 2$ is in $[0, 3]$ and $f(2)$ is undefined, so $f$ is not continuous there.", work="1.6cm"),
    Item(r"Is $g(x) = e^{x}\cos x$ continuous on $(-\infty, \infty)$? Explain.", selfcheck(r"\text{Yes}"),
         r"Yes. $e^x$ and $\cos x$ are each continuous for every real $x$, and a product of continuous functions is continuous.",
         work="1.6cm"),
]
same("x1 f", sp.solve(x**2 - 5 * x + 6, x), [2, 3])
same("x1 n", sp.solve(sp.Eq(2 + a, 1 + 4), a)[0], 3)
same("x1 s", [sp.limit(x**2, x, 1), 2 * 1 - 1, 2 * 3 - 1, 10 - 3], [1, 1, 5, 7])
same("x1 k", sp.solve(4 - x**2, x), [-2, 2])

# ---------------------------------------------------------------- quiz
CC = {"A": "$g$ could be $0$", "C": "$f$ could be negative", "D": "$f$ could be $\\le 0$"}
QUIZ = [
    Variants(
        Item(r"At how many $x$-values is $\dfrac{x-1}{x^2+x-2}$ discontinuous?", num(2),
             r"$x^2 + x - 2 = (x+2)(x-1)$: at $x = -2$ and $x = 1$.", work="1.6cm"),
        Item(r"At how many $x$-values is $\dfrac{x+5}{x^3-4x}$ discontinuous?", num(3),
             r"$x^3 - 4x = x(x-2)(x+2)$: at $x = 0$, $2$ and $-2$.", work="1.6cm"),
        Item(r"At how many $x$-values is $\dfrac{x}{x^2+9}$ discontinuous?", num(0),
             r"$x^2 + 9$ is never $0$, so the function is continuous everywhere.", work="1.6cm"),
    ),
    Variants(
        Item(r"Find the left endpoint of the largest interval containing $x = 5$ on which $\ln(x - 2)$ is continuous.", num(2),
             r"Need $x - 2 > 0$: the interval is $(2, \infty)$.", work="1.2cm"),
        Item(r"Find the left endpoint of the largest interval containing $x = 0$ on which $\sqrt{x + 7}$ is continuous.", num(-7),
             r"Need $x + 7 \ge 0$: the interval is $[-7, \infty)$.", work="1.2cm"),
        Item(r"Find the right endpoint of the largest interval containing $x = 0$ on which $\dfrac{1}{\sqrt{4 - x}}$ is continuous.", num(4),
             r"Need $4 - x > 0$: the interval is $(-\infty, 4)$.", work="1.2cm"),
    ),
    Variants(
        Item(r"Find $b$ so that $\begin{cases} x^2 + b, & x < 3 \\ 2x + 7, & x \ge 3 \end{cases}$ is continuous everywhere.",
             num(4), r"$9 + b = 13$, so $b = 4$.", work="1.6cm"),
        Item(r"Find $b$ so that $\begin{cases} bx - 1, & x < 2 \\ x^2 + 1, & x \ge 2 \end{cases}$ is continuous everywhere.",
             num(3), r"$2b - 1 = 5$, so $b = 3$.", work="1.6cm"),
        Item(r"Find $b$ so that $\begin{cases} e^x + b, & x < 0 \\ 4\cos x, & x \ge 0 \end{cases}$ is continuous everywhere.",
             num(3), r"$1 + b = 4$, so $b = 3$.", work="1.6cm"),
    ),
    Variants(
        MCQ(r"Which function is continuous on $(-\infty, \infty)$?",
            [r"$\tan x$", r"$\dfrac{1}{x^2+1}$", r"$\sqrt{x}$", r"$\ln|x|$"], "B",
            r"$x^2 + 1$ is never $0$, so the quotient is defined, and continuous, everywhere.",
            why_not={"A": "undefined at $\\frac\\pi2 + k\\pi$", "C": "undefined for $x<0$", "D": "undefined at $0$"}),
        MCQ(r"Which function is continuous on $(-\infty, \infty)$?",
            [r"$\dfrac{x}{x-1}$", r"$\ln x$", r"$e^{x}\sin x$", r"$\sqrt{x-1}$"], "C",
            r"$e^x$ and $\sin x$ are continuous everywhere, and so is their product.",
            why_not={"A": "undefined at $1$", "B": "undefined for $x \\le 0$", "D": "undefined for $x < 1$"}),
        MCQ(r"On which interval is $\dfrac{1}{x - 4}$ continuous?", [r"$[0, 4]$", r"$[3, 5]$", r"$(-\infty, \infty)$", r"$(4, 9]$"], "D",
            r"The only discontinuity is $x = 4$, and $(4, 9]$ doesn't contain it.", why_not={"A": "contains $4$", "B": "contains $4$"}),
    ),
    Variants(
        MCQ(r"$f$ is continuous on $[0, 4]$ and $g$ is continuous on $[0,4]$. Which must be continuous on $[0,4]$?",
            [r"$\dfrac{f}{g}$", r"$f - 3g$", r"$\sqrt{f}$", r"$\ln f$"], "B",
            r"Differences and constant multiples of continuous functions are continuous.", why_not=CC),
        MCQ(r"$f$ and $g$ are continuous everywhere. Which must be continuous everywhere?",
            [r"$\dfrac{f}{g}$", r"$\ln g$", r"$f \cdot g$", r"$\dfrac{1}{f}$"], "C", r"A product of continuous functions is continuous.",
            why_not={"A": CC["A"], "B": "$g$ could be $\\le 0$", "D": "$f$ could be $0$"}),
        MCQ(r"$g$ is continuous everywhere and $g(x) > 0$ for all $x$. Which must be continuous everywhere?",
            [r"$\dfrac{1}{g(x)}$", r"$\dfrac{1}{g(x) - 1}$", r"$\dfrac{1}{x}$", r"$\dfrac{g(x)}{x}$"], "A",
            r"$g$ is never $0$, so the quotient $\frac1g$ is continuous everywhere.",
            why_not={"B": "$g$ could equal $1$", "C": "undefined at $0$", "D": "undefined at $0$"}),
    ),
]
same("q versions", [len(sp.solve(x**3 - 4 * x, x)), len([r for r in sp.solve(x**2 + 9, x) if r.is_real]),
                    sp.solve(sp.Eq(2 * a - 1, 5), a)[0], 4 - 1], [3, 0, 3, 3])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"On which interval is $f(x) = \dfrac{\sqrt{x+2}}{x-3}$ continuous?",
        [r"$(-2, \infty)$", r"$[-2, 3)$", r"$(3, \infty)$", r"$[-2, \infty)$"], "B",
        r"Need $x \ge -2$ and $x \ne 3$; of the choices only $[-2, 3)$ lies inside that set.",
        why_not={"A": "includes $x=3$", "D": "includes $x = 3$"}),
    MCQ(r"Let $g(x) = \begin{cases} \cos x, & x < 0 \\ x + k, & x \ge 0. \end{cases}$ For which $k$ is $g$ continuous everywhere?",
        [r"$-1$", r"$0$", r"$1$", r"$\pi$"], "C", r"$\cos 0 = 1$, so $k = 1$."),
    MCQ(r"How many points of discontinuity does $\dfrac{x^2-4}{x^3-4x}$ have?", [r"$0$", r"$1$", r"$2$", r"$3$"], "D",
        r"$x^3 - 4x = x(x-2)(x+2)$ is zero at three points; the function is undefined at each (two are removable).",
        why_not={"B": "counted only the non-removable one"}),
    MCQ(r"Which statement is true about $h(x) = \dfrac{|x-1|}{x-1}$ on $[2, 5]$?",
        [r"$h$ is continuous on $[2,5]$", r"$h$ has a jump in $[2,5]$", r"$h$ is undefined at $x = 2$", r"$h$ is unbounded on $[2,5]$"],
        "A", r"On $[2, 5]$, $x - 1 > 0$, so $h(x) = 1$: continuous.", why_not={"B": "the jump is at $x = 1$, outside the interval"}),
]

# AP does not ask this topic as free response; the multiple-choice questions above cover it.
# See .claude/skills/ap-frq/SKILL.md.
FRQS = []

TOPIC = Topic(
    number="1.12", title="Confirming Continuity over an Interval",
    unit="Unit 1: Limits and Continuity", ced=["LIM-2.B", "LIM-2.B.1", "LIM-2.B.2"],
    goals=r"Find the intervals on which a function is continuous using domains, known continuous families, and seam checks.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
