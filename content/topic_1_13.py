"""Topic 1.13: Removing discontinuities.

CED: LIM-2.C.1 (redefine the value at a removable discontinuity to equal the limit),
LIM-2.C.2 (piecewise continuity at a boundary: the pieces must agree with each other and
with the value). The two-seam example matches the video (a = 3, b = 1).
"""
import sympy as sp

from calclib import (VideoExample, Variants, limchain, FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Text, Topic, Video,
                     num, same, selfcheck)

x, a, b, k = sp.symbols("x a b k")
same("hole", sp.limit((x**2 - 16) / (x - 4), x, 4), 8)
same("hinge k", sp.solve(sp.Eq(2 * k + 1, 3), k)[0], 1)
sol = sp.solve([sp.Eq(-1 + a, b + 1), sp.Eq(4 * b + 1, 5)], [a, b])
same("two seams", [sol[a], sol[b]], [3, 1])

NOTES = [
    Video("s1_13.py::Lesson", "Removing discontinuities", 2.5),

    Section("Filling a hole"),
    Text(r"$\displaystyle f(x) = \dfrac{x^2-16}{x-4}$ is undefined at $x = 4$, but $\displaystyle \lim_{x\to4}f(x) = \mblank{8}$. Defining "
         r"$f(4) = 8$ makes $f$ continuous at $4$:"
         r"\[ g(x) = \begin{cases} \dfrac{x^2-16}{x-4}, & x \ne 4 \\ 8, & x = 4. \end{cases} \]"),
    Formula("Removing a discontinuity", (
        r"If $\displaystyle \lim_{x\to c} f(x) = L$ exists but $f(c) \ne L$ (or $f(c)$ is undefined), the discontinuity is "
        r"\blank{removable}: redefine $f(c) = L$.\par "
        r"Jump and infinite discontinuities \blank{cannot} be removed by changing one value, because the limit does not exist.")),

    Section("Matching pieces at a seam"),
    Text(r"For \[ f(x) = \begin{cases} kx + 1, & x < 2 \\ x^2 - 1, & x \ge 2, \end{cases} \] continuity at $x = 2$ requires the "
         r"left piece at $2$ to equal the right piece at $2$: $2k + 1 = \mblank{3}$, so $k = \mblank{1}$."),
    VideoExample('Two seams', work="3.4cm"),
    BigIdea(r"A removable discontinuity is fixed by defining the value as the limit. A piecewise function is continuous at a seam "
            r"when the pieces meet each other and the value there."),
    Check(r"What value should $h(0)$ have so that $\displaystyle h(x) = \dfrac{\sin 3x}{x}$ is continuous at $0$?", num(3),
          r"\[ \lim_{x\to0}\frac{\sin3x}{x} = 3. \]"),
]

# ---------------------------------------------------------------- practice
P = [
    (r"\dfrac{x^2-25}{x+5}", (x**2 - 25) / (x + 5), -5, [r"\frac{(x-5)(x+5)}{x+5}", r"(x-5)"]),
    (r"\dfrac{x^2-3x}{x^2-9}", (x**2 - 3 * x) / (x**2 - 9), 3, [r"\frac{x(x-3)}{(x-3)(x+3)}", r"\frac{x}{x+3}"]),
    (r"\dfrac{\sqrt{x}-3}{x-9}", (sp.sqrt(x) - 3) / (x - 9), 9, [r"\frac{\sqrt x-3}{(\sqrt x-3)(\sqrt x+3)}", r"\frac{1}{\sqrt x+3}"]),
    (r"\dfrac{1-\cos x}{x}", (1 - sp.cos(x)) / x, 0, [r"\frac{1-\cos x}{x}"]),
]
PRACTICE = [Item(rf"$f(x) = {tex}$ has a removable discontinuity at $x = {c}$. What value should $f({c})$ be given to make $f$ continuous there?",
                 num(sp.limit(e, x, c)),
                 limchain(c, steps, sp.latex(sp.limit(e, x, c))) + rf", so define $f({c}) = {sp.latex(sp.limit(e, x, c))}$."
                 + (r" (This is one of the special limits from 1.8.)" if c == 0 else ""), work="2cm")
            for tex, e, c, steps in P]
PRACTICE += [
    Item(r"Find $k$ so that $\begin{cases} x^2 + k, & x < 1 \\ 3x - 2, & x \ge 1 \end{cases}$ is continuous.", num(0),
         r"$1 + k = 1$, so $k = 0$.", work="1.6cm"),
    Item(r"Find $k$ so that $\begin{cases} kx^2, & x \le 3 \\ 2x + k, & x > 3 \end{cases}$ is continuous.", num(sp.Rational(3, 4)),
         r"$9k = 6 + k$, so $k = \frac34$.", work="1.8cm"),
    Item(r"Find $a$ and $b$ so that $\begin{cases} ax + 1, & x < 1 \\ x^2 + b, & 1 \le x \le 3 \\ 2x + 4, & x > 3 \end{cases}$ "
         r"is continuous. Enter $a$.", num(1),
         r"Seam $x = 3$: $9 + b = 10$, so $b = 1$. Seam $x = 1$: $a + 1 = 1 + b = 2$, so $a = 1$.", work="2.6cm"),
    Item(r"Can $f(x) = \dfrac{x}{|x|}$ be made continuous at $0$ by choosing $f(0)$? Explain.", selfcheck(r"\text{No}"),
         r"No. The one-sided limits are $-1$ and $1$, so no single value works. It's a jump.", work="1.8cm"),
    Item(r"Can $g(x) = \dfrac{x+1}{x-2}$ be made continuous at $x = 2$ by choosing $g(2)$? Explain.", selfcheck(r"\text{No}"),
         r"No. The function is unbounded near $2$, so there is no finite limit to use.", work="1.8cm"),
]
same("p5", sp.solve(sp.Eq(1 + k, 1), k)[0], 0)
same("p6", sp.solve(sp.Eq(9 * k, 6 + k), k)[0], sp.Rational(3, 4))
s7 = sp.solve([sp.Eq(a + 1, 1 + b), sp.Eq(9 + b, 10)], [a, b])
same("p7", [s7[a], s7[b]], [1, 1])

# extra practice (round 1)
PRACTICE += [
    Item(r"$f(x) = \dfrac{x^2 - 7x + 10}{x - 2}$ has a removable discontinuity at $x = 2$. What value should $f(2)$ be given?",
         num(-3), limchain(2, [r"\frac{(x-2)(x-5)}{x-2}", r"(x-5)"], -3) + r", so define $f(2) = -3$.", work="2cm"),
    Item(r"$f(x) = \dfrac{x^3 - 1}{x - 1}$ has a removable discontinuity at $x = 1$. What value should $f(1)$ be given?",
         num(3), limchain(1, [r"\frac{(x-1)(x^2+x+1)}{x-1}", r"(x^2+x+1)"], 3) + r", so define $f(1) = 3$.", work="2cm"),
    Item(r"$f(x) = \dfrac{\sqrt{x + 4} - 2}{x}$ has a removable discontinuity at $x = 0$. What value should $f(0)$ be given?",
         num(sp.Rational(1, 4)),
         limchain(0, [r"\frac{(\sqrt{x+4}-2)(\sqrt{x+4}+2)}{x(\sqrt{x+4}+2)}", r"\frac{x}{x(\sqrt{x+4}+2)}",
                      r"\frac{1}{\sqrt{x+4}+2}"], r"\frac14") + r", so define $f(0) = \frac14$.", work="2.4cm"),
    Item(r"$f(x) = \dfrac{\sin 3x}{x}$ has a removable discontinuity at $x = 0$. What value should $f(0)$ be given?",
         num(3), limchain(0, [r"3\cdot\frac{\sin 3x}{3x}"], 3) + r", so define $f(0) = 3$.", work="2cm"),
    Item(r"Find $k$ so that $\begin{cases} \dfrac{x^2 - 4}{x - 2}, & x \ne 2 \\ k, & x = 2 \end{cases}$ is continuous at $x = 2$.",
         num(4), limchain(2, [r"\frac{(x-2)(x+2)}{x-2}", r"(x+2)"], 4) + r", so $k = 4$.", work="1.8cm"),
    Item(r"Find $k$ so that $\begin{cases} kx - 3, & x < 2 \\ x^2 + k, & x \ge 2 \end{cases}$ is continuous.", num(7),
         r"Match at $x = 2$: $2k - 3 = 4 + k$, so $k = 7$.", work="1.8cm"),
    Item(r"Find $k$ so that $\begin{cases} e^{x} + k, & x < 0 \\ 3\cos x, & x \ge 0 \end{cases}$ is continuous.", num(2),
         r"Match at $x = 0$: $e^0 + k = 1 + k$ and $3\cos 0 = 3$, so $k = 2$.", work="1.8cm"),
    Item(r"Find $a$ and $b$ so that $\begin{cases} x + a, & x < 0 \\ bx + 2, & 0 \le x \le 2 \\ x^2, & x > 2 \end{cases}$ "
         r"is continuous. Enter $b$.", num(1),
         r"Seam $x = 0$: $a = 2$. Seam $x = 2$: $2b + 2 = 4$, so $b = 1$.", work="2.6cm"),
    Item(r"Let $f(x) = \dfrac{x^2 - x - 6}{x^2 - 9}$. How many of its discontinuities are removable?", num(1),
         r"$\dfrac{(x-3)(x+2)}{(x-3)(x+3)}$. At $x = 3$ the factor cancels and "
         + limchain(3, [r"\frac{x+2}{x+3}"], r"\frac56") + r", so that one is removable. At $x = -3$ the function is "
         r"unbounded, so that one is not.", work="2.4cm"),
    Item(r"Can $h(x) = \begin{cases} x^2, & x < 1 \\ x + 2, & x > 1 \end{cases}$ be made continuous at $x = 1$ by choosing "
         r"$h(1)$? Explain.", selfcheck(r"\text{No}"),
         r"No. $\displaystyle\lim_{x\to1^-}x^2 = 1$ and $\displaystyle\lim_{x\to1^+}(x+2) = 3$, so the limit does not exist. "
         r"No choice of $h(1)$ can fix a jump.", work="1.8cm"),
]
same("x1 a", sp.limit((x**2 - 7 * x + 10) / (x - 2), x, 2), -3)
same("x1 b", sp.limit((x**3 - 1) / (x - 1), x, 1), 3)
same("x1 c", sp.limit((sp.sqrt(x + 4) - 2) / x, x, 0), sp.Rational(1, 4))
same("x1 d", sp.limit(sp.sin(3 * x) / x, x, 0), 3)
same("x1 k1", sp.solve(sp.Eq(2 * k - 3, 4 + k), k)[0], 7)
same("x1 k2", sp.solve(sp.Eq(1 + k, 3), k)[0], 2)
same("x1 ab", sp.solve(sp.Eq(2 * b + 2, 4), b)[0], 1)
same("x1 rem", sp.limit((x**2 - x - 6) / (x**2 - 9), x, 3), sp.Rational(5, 6))

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"What value of $f(2)$ makes $f(x) = \dfrac{x^2+x-6}{x-2}$ continuous at $x = 2$?", num(5),
             limchain(2, [r"\frac{(x+3)(x-2)}{x-2}", r"(x+3)"], 5), work="1.8cm"),
        Item(r"What value of $f(-3)$ makes $f(x) = \dfrac{x^2-9}{x+3}$ continuous at $x = -3$?", num(-6),
             limchain(-3, [r"\frac{(x-3)(x+3)}{x+3}", r"(x-3)"], -6), work="1.8cm"),
        Item(r"What value of $f(9)$ makes $f(x) = \dfrac{x-9}{\sqrt x-3}$ continuous at $x = 9$?", num(6),
             limchain(9, [r"\frac{(\sqrt x-3)(\sqrt x+3)}{\sqrt x-3}", r"(\sqrt x+3)"], 6), work="1.8cm"),
    ),
    Variants(
        Item(r"Find $k$ so that $\begin{cases} 5 - kx, & x < 2 \\ x^2 - 3, & x \ge 2 \end{cases}$ is continuous.", num(2),
             r"$5 - 2k = 1$, so $k = 2$.", work="1.8cm"),
        Item(r"Find $k$ so that $\begin{cases} kx^2, & x \le 1 \\ 3x + 2, & x > 1 \end{cases}$ is continuous.", num(5),
             r"$k = 3 + 2 = 5$.", work="1.8cm"),
        Item(r"Find $k$ so that $\begin{cases} x + k, & x < 4 \\ \sqrt{x}, & x \ge 4 \end{cases}$ is continuous.", num(-2),
             r"$4 + k = 2$, so $k = -2$.", work="1.8cm"),
    ),
    Variants(
        Item(r"What value of $g(0)$ makes $g(x) = \dfrac{\tan x}{2x}$ continuous at $0$?", num(sp.Rational(1, 2)),
             limchain(0, [r"\frac12\cdot\frac{\sin x}{x}\cdot\frac{1}{\cos x}"], r"\frac12"), work="1.6cm"),
        Item(r"What value of $g(0)$ makes $g(x) = \dfrac{\sin 3x}{x}$ continuous at $0$?", num(3),
             limchain(0, [r"3\cdot\frac{\sin 3x}{3x}"], 3), work="1.6cm"),
        Item(r"What value of $g(0)$ makes $g(x) = \dfrac{1 - \cos x}{x}$ continuous at $0$?", num(0),
             r"This is a special limit from Topic 1.8: $\displaystyle\lim_{x\to0}\frac{1-\cos x}{x} = 0$. So $g(0) = 0$.", work="1.6cm"),
    ),
    Variants(
        MCQ(r"Which discontinuity can be removed by redefining one value of the function?",
            [r"a jump", r"a vertical asymptote", r"a hole", r"an oscillation"], "C", r"Only a hole has a limit to use."),
        MCQ(r"$\displaystyle\lim_{x\to2^-}f(x) = 1$ and $\displaystyle\lim_{x\to2^+}f(x) = 3$. Can redefining $f(2)$ make $f$ continuous at $2$?",
            [r"Yes, set $f(2) = 2$.", r"Yes, set $f(2) = 1$.", r"Yes, set $f(2) = 3$.", r"No: the limit doesn't exist, so no value works."], "D",
            r"A jump has no single limit to match.", why_not={"A": "limits are not averaged"}),
        MCQ(r"$f(x) = \dfrac{x^2 - 1}{x - 1}$ for $x \ne 1$. Which definition of $f(1)$ makes $f$ continuous everywhere?",
            [r"$f(1) = 0$", r"$f(1) = 2$", r"$f(1) = 1$", r"No value works."], "B",
            r"For $x \ne 1$, $f(x)$ matches $x + 1$, whose limit at $1$ is $2$.", why_not={"A": "that's $\\frac{1-1}{\\ldots}$ thinking", "D": "it's a hole, so one value works"}),
    ),
    Variants(
        MCQ(r"$f(x) = \begin{cases} ax + b, & x < 1 \\ 4, & x = 1 \\ x^2 + a, & x > 1. \end{cases}$ Which pair $(a, b)$ makes $f$ continuous at $x = 1$?",
            [r"$(3, 1)$", r"$(1, 3)$", r"$(4, 0)$", r"$(2, 2)$"], "A",
            r"Right piece: $1 + a = 4$, so $a = 3$. Left piece: $a + b = 4$, so $b = 1$.", why_not={"B": "swapped $a$ and $b$"}),
        MCQ(r"$f(x) = \begin{cases} x + a, & x < 0 \\ b, & x = 0 \\ 2 - x^2, & x > 0. \end{cases}$ Which pair $(a, b)$ makes $f$ continuous at $x = 0$?",
            [r"$(0, 2)$", r"$(2, 2)$", r"$(2, 0)$", r"$(-2, 2)$"], "B",
            r"Right piece heads to $2$, so $b = 2$ and the left piece must head to $2$: $a = 2$.", why_not={"C": "$f(0)$ must be the limit, $2$"}),
        MCQ(r"$f(x) = \begin{cases} ax^2, & x < 2 \\ 8, & x = 2 \\ x + b, & x > 2. \end{cases}$ Which pair $(a, b)$ makes $f$ continuous at $x = 2$?",
            [r"$(4, 6)$", r"$(2, 4)$", r"$(2, 6)$", r"$(8, 6)$"], "C",
            r"Left: $4a = 8$, so $a = 2$. Right: $2 + b = 8$, so $b = 6$.", why_not={"A": "used $a \\cdot 2 = 8$", "D": "forgot to square"}),
    ),
]
same("q1", sp.limit((x**2 + x - 6) / (x - 2), x, 2), 5)
same("q2", sp.solve(sp.Eq(5 - 2 * k, 1), k)[0], 2)
same("q3", sp.limit(sp.tan(x) / (2 * x), x, 0), sp.Rational(1, 2))
same("q versions", [sp.limit((x**2 - 9) / (x + 3), x, -3), sp.limit((x - 9) / (sp.sqrt(x) - 3), x, 9), sp.limit(sp.sin(3 * x) / x, x, 0),
                    sp.limit((1 - sp.cos(x)) / x, x, 0), 4 + (-2), sp.sqrt(4)], [-6, 6, 3, 0, 2, 2])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"Let $f(x) = \dfrac{x^2-7x+10}{x-5}$ for $x \ne 5$. What value should $f(5)$ have to make $f$ continuous at $5$?",
        [r"$0$", r"$2$", r"$3$", r"$5$"], "C", limchain(5, [r"\frac{(x-5)(x-2)}{x-5}", r"(x-2)"], 3)),
    MCQ(r"For what value of $k$ is $g(x) = \begin{cases} \dfrac{e^{2x}-1}{x}, & x \ne 0 \\ k, & x = 0 \end{cases}$ continuous at $0$?",
        [r"$0$", r"$2$", r"$1$", r"$e$"], "B", r"$\displaystyle\lim_{x\to0}\frac{e^{2x}-1}{x} = 2$ (Topic 1.4 estimated it with a table).", calc=True),
    MCQ(r"$h(x) = \begin{cases} x^2 + c, & x \le 2 \\ cx + 6, & x > 2. \end{cases}$ For what value of $c$ is $h$ continuous?",
        [r"$-2$", r"$1$", r"$2$", r"no such $c$"], "A", r"$4 + c = 2c + 6$, so $c = -2$."),
    MCQ(r"Which function has a discontinuity at $x = 1$ that CANNOT be removed?",
        [r"$\dfrac{x^2-1}{x-1}$", r"$\dfrac{x-1}{x^2-1}$", r"$\dfrac{\sin(x-1)}{x-1}$", r"$\dfrac{x+1}{x-1}$"], "D",
        r"$\dfrac{x+1}{x-1}$ is unbounded near $1$.", why_not={"B": "$\\frac1{x+1}$ near $1$: removable"}),
]
same("m1", sp.limit((x**2 - 7 * x + 10) / (x - 5), x, 5), 3)
same("m2", sp.limit((sp.exp(2 * x) - 1) / x, x, 0), 2)
c = sp.symbols("c")
same("m3", sp.solve(sp.Eq(4 + c, 2 * c + 6), c)[0], -2)

FRQS = [
    FRQ("Removing a discontinuity", (
        r"Let $f$ be the function defined by $f(x) = \begin{cases} \dfrac{x^2 - 2x - 3}{x - 3}, & x < 3 \\[4pt] k, & x = 3 \\ "
        r"bx - 2, & x > 3, \end{cases}$ where $k$ and $b$ are constants."), [
        Part("a", r"Find $\displaystyle\lim_{x\to3^-}f(x)$. Show the work that leads to your answer.", num(4),
             limchain(3, [r"\frac{(x-3)(x+1)}{x-3}", r"(x+1)"], 4, side="^-"),
             [(1, "factors and cancels"), (1, "answer $4$")], work="2.6cm"),
        Part("b", r"Find the values of $k$ and $b$ for which $f$ is continuous at $x = 3$. Show the work that leads to your answer.",
             selfcheck(r"k = 4,\ b = 2"),
             r"Continuity at $x = 3$ needs $\displaystyle\lim_{x\to3^-}f(x) = \lim_{x\to3^+}f(x) = f(3)$. "
             r"$\displaystyle\lim_{x\to3^+}(bx - 2) = 3b - 2$, so $3b - 2 = 4$ and $b = 2$. Also $f(3) = k = 4$.",
             [(1, "$3b - 2 = 4$, so $b = 2$"), (1, "$k = 4$")], work="3cm"),
    ], frq_type="Limits and continuity"),
]
same("frq a", sp.limit((x**2 - 2 * x - 3) / (x - 3), x, 3, "-"), 4)
same("frq b", sp.solve(sp.Eq(3 * b - 2, 4), b)[0], 2)

TOPIC = Topic(
    number="1.13", title="Removing Discontinuities",
    unit="Unit 1: Limits and Continuity", ced=["LIM-2.C", "LIM-2.C.1", "LIM-2.C.2"],
    goals=r"Remove a removable discontinuity by redefining a value, and choose parameters that make a piecewise function continuous.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
