"""Topic 1.14: Connecting infinite limits and vertical asymptotes.

CED: LIM-2.D.1 (infinite limits), LIM-2.D.2 (asymptotic and unbounded behavior described with limits).
"""
import sympy as sp

from calclib import (VideoExample, Variants, FRQ, MCQ, BigIdea, Check, Definition, Example, FigureRow, Formula, Item, Part, Section,
                     Text, Topic, Video, dne, infinite, num, same, selfcheck)
from calclib.figs import graph

x = sp.symbols("x")
F = (x + 3) / ((x - 1) * (x + 2))
same("sign L", sp.limit(F, x, 1, "-"), -sp.oo)
same("sign R", sp.limit(F, x, 1, "+"), sp.oo)
same("-2 L", sp.limit(F, x, -2, "-"), sp.oo)
same("-2 R", sp.limit(F, x, -2, "+"), -sp.oo)

FIG_A = graph("t1_14_a", [("1/(x-2)^2", -0.5, 1.55), ("1/(x-2)^2", 2.45, 4.5)], xr=(-0.5, 4.5), yr=(-1, 5), vlines=[2],
              w="4.8cm", h="4cm", caption=r"$\dfrac{1}{(x-2)^2}$")
FIG_B = graph("t1_14_b", [("1/(x-2)", -0.5, 1.8), ("1/(x-2)", 2.2, 4.5)], xr=(-0.5, 4.5), yr=(-5, 5), vlines=[2],
              w="4.8cm", h="4cm", ystep=2, caption=r"$\dfrac{1}{x-2}$")
FIG_LN = graph("t1_14_ln", [("ln(x)", 0.02, 4.5)], xr=(-0.5, 4.5), yr=(-4, 2), vlines=[0], w="4.8cm", h="4cm",
               ystep=2, caption=r"$\ln x$")

NOTES = [
    Video("s1_14.py::Lesson", "Infinite limits", 3),

    Section("Infinite limits"),
    Definition("Infinite limit", (
        r"$\displaystyle \lim_{x\to c} f(x) = \infty$ means the values of $f(x)$ \blank{grow without bound} as $x$ approaches $c$ "
        r"(similarly for $-\infty$). The limit still does not \blank{exist} as a real number; the symbol describes how it fails.")),
    FigureRow([FIG_A, FIG_B, FIG_LN]),
    Text(r"$\displaystyle \lim_{x\to2}\frac{1}{(x-2)^2} = \mblank{\infty}$. For $\dfrac1{x-2}$: "
         r"$\displaystyle \lim_{x\to2^-} = \mblank{-\infty}$ and $\displaystyle \lim_{x\to2^+} = \mblank{\infty}$. "
         r"And $\displaystyle \lim_{x\to0^+}\ln x = \mblank{-\infty}$."),
    Formula("Vertical asymptote", (
        r"The line $x = c$ is a \textbf{vertical asymptote} of $f$ if \blank{at least one} of "
        r"$\displaystyle \lim_{x\to c^-} f(x)$, \[ \lim_{x\to c^+} f(x) \] is $\infty$ or $-\infty$.")),

    Section("Finding the signs"),
    VideoExample('A sign chart', work="3cm"),
    Text(r"\textbf{Cancel first.} $\displaystyle \dfrac{x^2-1}{x-1} = x + 1$ for $x \ne 1$: the zero of the denominator \blank{cancels}, so "
         r"$x = 1$ is a hole, not a vertical asymptote."),
    BigIdea(r"A vertical asymptote comes from a nonzero quantity divided by one shrinking to zero. The signs on each side tell you "
            r"whether the graph goes up or down."),
    Check(r"Find \[ \lim_{x\to3^-}\frac{2x}{x-3}. \]", infinite(-1),
          r"$2x \to 6 > 0$ and $x - 3 \to 0^-$, so the quotient goes to $-\infty$."),
]

# ---------------------------------------------------------------- practice
P = [
    (r"\displaystyle\lim_{x\to4^+}\frac{3}{x-4}", 3 / (x - 4), 4, "+", r"$\frac{3}{0^+}$: $\infty$."),
    (r"\displaystyle\lim_{x\to4^-}\frac{3}{x-4}", 3 / (x - 4), 4, "-", r"$\frac{3}{0^-}$: $-\infty$."),
    (r"\displaystyle\lim_{x\to-1}\frac{x-2}{(x+1)^2}", (x - 2) / (x + 1)**2, -1, "+-",
     r"Numerator $\to -3$, denominator $\to 0^+$ on both sides: $-\infty$."),
    (r"\displaystyle\lim_{x\to0^+}\frac{x-1}{x^2+x}", (x - 1) / (x**2 + x), 0, "+",
     r"$\frac{x-1}{x(x+1)}$: numerator $\to -1$, denominator $\to 0^+$: $-\infty$."),
    (r"\displaystyle\lim_{x\to\pi/2^-}\tan x", sp.tan(x), sp.pi / 2, "-", r"$\sin x \to 1$ and $\cos x \to 0^+$: $\infty$."),
    (r"\displaystyle\lim_{x\to2}\frac{x+1}{x-2}", (x + 1) / (x - 2), 2, "+-",
     r"The sides go to $-\infty$ and $\infty$: the limit does not exist (and is not $\pm\infty$)."),
]


def ans(e, c, d):
    if d == "+-":
        lft, rgt = sp.limit(e, x, c, "-"), sp.limit(e, x, c, "+")
        v = lft if lft == rgt else None
    else:
        v = sp.limit(e, x, c, d)
    if v is None:
        return dne()
    return infinite(1) if v == sp.oo else infinite(-1) if v == -sp.oo else num(v)


PRACTICE = [Item(rf"Find ${tex}$. Use $\infty$, $-\infty$ or DNE as needed.", ans(e, c, d), sol, work="1.8cm")
            for tex, e, c, d, sol in P]
PRACTICE += [
    Item(r"How many vertical asymptotes does $g(x) = \dfrac{x^2-4}{x^2-x-2}$ have?", num(1),
         r"$\dfrac{(x-2)(x+2)}{(x-2)(x+1)}$: $x - 2$ cancels (hole at $x=2$); $x = -1$ is the only vertical asymptote.",
         work="2cm"),
    Item(r"Give the equation of the vertical asymptote of $h(x) = \ln(x - 5)$. Enter the $x$-value.", num(5),
         r"$\displaystyle\lim_{x\to5^+}\ln(x-5) = -\infty$, so $x = 5$.", work="1.4cm"),
    Item(r"Write a rational function with a vertical asymptote at $x = 3$ where both sides go to $-\infty$.",
         selfcheck(r"\text{e.g. } -\dfrac{1}{(x-3)^2}"), r"For example $-\dfrac{1}{(x-3)^2}$: the squared factor keeps one sign.",
         work="1.6cm"),
]
same("p7 VA count", len([r for r in sp.solve(sp.denom(sp.cancel((x**2 - 4) / (x**2 - x - 2))), x)]), 1)

# extra practice (round 1)
P2 = [
    (r"\displaystyle\lim_{x\to3^+}\frac{x+1}{x-3}", (x + 1) / (x - 3), 3, "+", sp.oo,
     r"The numerator approaches $4 > 0$ and the denominator approaches $0$ through positive values, so the limit is $\infty$."),
    (r"\displaystyle\lim_{x\to3^-}\frac{x+1}{x-3}", (x + 1) / (x - 3), 3, "-", -sp.oo,
     r"The numerator approaches $4 > 0$ and the denominator approaches $0$ through negative values, so the limit is $-\infty$."),
    (r"\displaystyle\lim_{x\to-2^-}\frac{5}{x+2}", 5 / (x + 2), -2, "-", -sp.oo,
     r"For $x$ just left of $-2$, $x + 2$ is a small negative number, so $\frac{5}{x+2}$ is large and negative: $-\infty$."),
    (r"\displaystyle\lim_{x\to0}\frac{-2}{x^2}", -2 / x**2, 0, "+-", -sp.oo,
     r"$x^2 > 0$ on both sides and approaches $0$, so $\frac{-2}{x^2}$ is large and negative from both sides: $-\infty$."),
    (r"\displaystyle\lim_{x\to1^-}\frac{x}{1-x}", x / (1 - x), 1, "-", sp.oo,
     r"For $x$ just below $1$, $1 - x$ is a small positive number and $x$ is near $1$, so the limit is $\infty$."),
    (r"\displaystyle\lim_{x\to2}\frac{x-5}{(x-2)^2}", (x - 5) / (x - 2)**2, 2, "+-", -sp.oo,
     r"The numerator approaches $-3 < 0$ and $(x-2)^2$ approaches $0$ through positive values on both sides: $-\infty$."),
    (r"\displaystyle\lim_{x\to0^+}\ln x", sp.log(x), 0, "+", -sp.oo,
     r"As $x$ shrinks toward $0$, $\ln x$ decreases without bound: $-\infty$."),
    (r"\displaystyle\lim_{x\to-1}\frac{x}{x+1}", x / (x + 1), -1, "+-", None,
     r"From the left the limit is $\infty$ (numerator near $-1$, denominator $0^-$) and from the right it is $-\infty$. "
     r"The sides disagree, so the limit does not exist."),
]
for tex, e, c, d, want, sol in P2:
    got = ans(e, c, d)
    PRACTICE.append(Item(rf"Find ${tex}$. Use $\infty$, $-\infty$ or DNE as needed.", got, sol, work="1.8cm"))
    if d == "+-":
        l, r = sp.limit(e, x, c, "-"), sp.limit(e, x, c, "+")
        assert (l != r) if want is None else (l == r == want), tex
    else:
        same("x1 " + tex[:30], sp.limit(e, x, c, d), want)
PRACTICE += [
    Item(r"How many vertical asymptotes does $f(x) = \dfrac{x + 3}{x^2 + 2x - 3}$ have?", num(1),
         r"$\dfrac{x+3}{(x+3)(x-1)}$. The factor $x + 3$ cancels, leaving a hole at $x = -3$. Only $x = 1$ is a vertical "
         r"asymptote.", work="2cm"),
    Item(r"Give the $x$-value of the vertical asymptote of $g(x) = \dfrac{2x}{x + 4}$, and describe the behavior from "
         r"the right using a limit. Enter the $x$-value.", num(-4),
         r"$x = -4$. From the right, the numerator approaches $-8$ and the denominator $0^+$, so "
         r"$\displaystyle\lim_{x\to-4^+}\frac{2x}{x+4} = -\infty$.", work="2cm"),
]
same("x1 va count", len(sp.solve(sp.denom(sp.cancel((x + 3) / (x**2 + 2 * x - 3))), x)), 1)
same("x1 g right", sp.limit(2 * x / (x + 4), x, -4, "+"), -sp.oo)

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find $\displaystyle\lim_{x\to5^-}\frac{x}{x-5}$.", infinite(-1), r"The top heads to $5$ and the bottom to $0^-$: $-\infty$.", work="1.4cm"),
        Item(r"Find $\displaystyle\lim_{x\to-3^+}\frac{2}{x+3}$.", infinite(1), r"The top is $2$ and the bottom heads to $0^+$: $\infty$.", work="1.4cm"),
        Item(r"Find $\displaystyle\lim_{x\to1^+}\frac{x-4}{x-1}$.", infinite(-1), r"The top heads to $-3$ and the bottom to $0^+$: $-\infty$.", work="1.4cm"),
    ),
    Variants(
        Item(r"Find $\displaystyle\lim_{x\to0}\frac{-2}{x^2}$.", infinite(-1), r"$x^2$ is positive on both sides and shrinks to $0$: $-\infty$.", work="1.4cm"),
        Item(r"Find $\displaystyle\lim_{x\to2}\frac{x+1}{(x-2)^2}$.", infinite(1), r"The top heads to $3$, and the square is positive on both sides: $\infty$.", work="1.4cm"),
        Item(r"Find $\displaystyle\lim_{x\to-1}\frac{1}{x+1}$, or type DNE.", dne(), r"From the left, $-\infty$; from the right, $\infty$. The limit does not exist.", work="1.4cm"),
    ),
    Variants(
        Item(r"How many vertical asymptotes does $\dfrac{x+1}{x^2-1}$ have?", num(1),
             r"$\dfrac{x+1}{(x-1)(x+1)}$: $x + 1$ cancels (a hole), so only $x = 1$.", work="1.6cm"),
        Item(r"How many vertical asymptotes does $\dfrac{x}{x^2-4x}$ have?", num(1),
             r"$\dfrac{x}{x(x-4)}$: $x$ cancels (a hole at $0$), so only $x = 4$.", work="1.6cm"),
        Item(r"How many vertical asymptotes does $\dfrac{x+2}{x^2-9}$ have?", num(2),
             r"$\dfrac{x+2}{(x-3)(x+3)}$: nothing cancels, so $x = 3$ and $x = -3$.", work="1.6cm"),
    ),
    Variants(
        MCQ(r"The line $x = 2$ is a vertical asymptote of which function?",
            [r"$\dfrac{x-2}{x+2}$", r"$\dfrac{x^2-4}{x-2}$", r"$\dfrac{x}{x^2-4}$", r"$\dfrac{x-2}{x^2+4}$"], "C",
            r"$\dfrac{x}{(x-2)(x+2)}$: at $x = 2$ the numerator is $2 \ne 0$.", why_not={"B": "hole at $x=2$"}),
        MCQ(r"The line $x = -1$ is a vertical asymptote of which function?",
            [r"$\dfrac{x+1}{x^2-1}$", r"$\dfrac{x+1}{x^2+1}$", r"$\ln(x + 2)$", r"$\dfrac{x^2+1}{x+1}$"], "D",
            r"At $x = -1$ the top is $2$ and the bottom is $0$.",
            why_not={"A": "$x + 1$ cancels: a hole at $-1$, and the asymptote is at $x = 1$", "B": "the bottom is never $0$",
                     "C": "asymptote at $x = -2$"}),
        MCQ(r"The line $x = 0$ is a vertical asymptote of which function?", [r"$\dfrac{\sin x}{x}$", r"$\ln x$", r"$e^x$", r"$\dfrac{x^2}{x}$"], "B",
            r"$\ln x \to -\infty$ as $x \to 0^+$.", why_not={"A": "a hole: the limit is $1$", "D": "a hole"}),
    ),
    Variants(
        MCQ(r"$\displaystyle\lim_{x\to c^+} f(x) = \infty$ and $\displaystyle\lim_{x\to c^-} f(x) = 3$. Which is true?",
            [r"$x = c$ is a vertical asymptote", r"$f$ has a removable discontinuity at $c$", r"$\displaystyle\lim_{x\to c}f(x) = \infty$",
             r"$x = c$ is not an asymptote because the left side is finite"], "A", r"One infinite one-sided limit is enough.",
            why_not={"D": "one side is enough"}),
        MCQ(r"Which statement does $\displaystyle\lim_{x\to4}f(x) = -\infty$ mean?",
            [r"$f(4) = -\infty$", r"As $x$ approaches $4$, $f(x)$ decreases without bound", r"$f$ has a hole at $x = 4$", r"The limit is a very negative number"], "B",
            r"The outputs fall below every number; the limit doesn't exist as a number, and $-\infty$ says how it fails.",
            why_not={"A": "$-\\infty$ is not a value", "D": "it isn't a number at all"}),
        MCQ(r"$f(x) = \dfrac{x-3}{x^2-9}$. Which is true at $x = 3$?",
            [r"$x = 3$ is a vertical asymptote.", r"$f$ has a hole at $x = 3$.", r"$f$ is continuous at $x = 3$.", r"$\displaystyle\lim_{x\to3}f(x) = \infty$"], "B",
            r"$x - 3$ cancels, and $\displaystyle\lim_{x\to3}\frac{1}{x+3} = \frac16$: a hole.", why_not={"A": "the factor cancels", "C": "$f(3)$ is undefined"}),
    ),
]
same("q versions", [sp.limit(2 / (x + 3), x, -3, "+"), sp.limit((x - 4) / (x - 1), x, 1, "+"), sp.limit((x + 1) / (x - 2)**2, x, 2),
                    sp.limit((x - 3) / (x**2 - 9), x, 3), sp.limit((x + 1) / (x**2 - 1), x, -1)],
     [sp.oo, -sp.oo, sp.oo, sp.Rational(1, 6), sp.Rational(-1, 2)])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$\displaystyle\lim_{x\to3^+}\frac{x^2-9}{x^2-6x+9}$ is", [r"$0$", r"$1$", r"$\infty$", r"$-\infty$"], "C",
        r"$\dfrac{(x-3)(x+3)}{(x-3)^2} = \dfrac{x+3}{x-3}$; from the right that is $\frac{6}{0^+} \to \infty$."),
    MCQ(r"Which of the following lines is a vertical asymptote of $y = \dfrac{x^2-3x}{x^2-9}$?",
        [r"$x = -3$", r"$x = 3$", r"$x = 0$", r"$y = 1$"], "A",
        r"$\dfrac{x(x-3)}{(x-3)(x+3)} = \dfrac{x}{x+3}$; only $x = -3$ survives.", why_not={"B": "hole", "D": "horizontal, not vertical"}),
    MCQ(r"$\displaystyle\lim_{x\to0^-}\frac{1}{x^3}$ is", [r"$\infty$", r"$-\infty$", r"$0$", r"$1$"], "B",
        r"For $x < 0$, $x^3 < 0$ and small, so $\frac1{x^3} \to -\infty$."),
    MCQ(r"The graph of $f(x) = \dfrac{x - a}{x^2 - 4}$ has exactly one vertical asymptote. Which could be the value of $a$?",
        [r"$0$", r"$1$", r"$4$", r"$2$"], "D", r"If $a = 2$, the factor $x - 2$ cancels, leaving only $x = -2$.",
        why_not={"A": "two asymptotes, $x=\\pm2$"}),
]
same("m1", sp.limit((x**2 - 9) / (x**2 - 6 * x + 9), x, 3, "+"), sp.oo)

# AP does not ask this topic as free response; the multiple-choice questions above cover it.
# See .claude/skills/ap-frq/SKILL.md.
FRQS = []

TOPIC = Topic(
    number="1.14", title="Connecting Infinite Limits and Vertical Asymptotes",
    unit="Unit 1: Limits and Continuity", ced=["LIM-2.D", "LIM-2.D.1", "LIM-2.D.2"],
    goals=r"Describe unbounded behavior with infinite limits and use it to find and analyze vertical asymptotes.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
