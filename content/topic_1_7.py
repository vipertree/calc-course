"""Topic 1.7: Selecting procedures for determining limits.

CED: LIM-1.D, LIM-1.E (synthesis topic). The lesson is a decision procedure: substitute,
read the result (number / 0/0 / nonzero/0), and let the form pick the tool. Absolute values
and piecewise functions get split by side. Every practice answer is computed by sympy, and
every solution keeps limit notation on each line.
"""
import sympy as sp

from calclib import (VideoExample, Variants, FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Text, Topic, Video,
                     check, dne, infinite, limchain, num, same, selfcheck)

x = sp.symbols("x")


def lim(e, c, d=None):
    return sp.limit(e, x, c) if d is None else sp.limit(e, x, c, d)


def answer(e, c):
    """Two-sided limit as an Answer, checked from both sides (sympy's default limit is one-sided)."""
    lft, rgt = lim(e, c, "-"), lim(e, c, "+")
    if lft == rgt:
        return infinite(1) if lft == sp.oo else infinite(-1) if lft == -sp.oo else num(lft)
    return dne()


same("worked", lim((x**2 + 2 * x - 8) / (sp.sqrt(x + 5) - 1), -4), -12)
same("abs L", lim(sp.Abs(x - 2) / (x - 2), 2, "-"), -1)
same("abs R", lim(sp.Abs(x - 2) / (x - 2), 2, "+"), 1)
same("sign L", lim((x + 1) / (x - 2)**2, 2, "-"), sp.oo)

NOTES = [
    Video("s1_7.py::Lesson", "Choosing a method", 3),

    Section("Substitute, then read the result"),
    Formula(r"A decision procedure for $\displaystyle\lim_{x\to c} f(x)$", (
        r"\textbf{1. Substitute} $x = c$. \par "
        r"\quad $\bullet$ A number (and $f$ is a single nice formula near $c$): that number is the limit. \par "
        r"\quad $\bullet$ $\frac00$ (or $\frac{\infty}{\infty}$, which shows up when $x \to \infty$; see Topic 1.15): these forms are "
        r"\emph{indeterminate}, so rewrite. Factor, use a conjugate, combine fractions, or use an identity. Then substitute again, and read "
        r"the new result the same way: it can still come out $\displaystyle \dfrac{\text{nonzero}}{0}$, and the limit may not exist. \par "
        r"\quad $\bullet$ $\displaystyle \dfrac{\text{nonzero}}{0}$: the function is unbounded near $c$. Check the sign on each side. \par "
        r"\textbf{2. Split into sides} whenever the formula changes at $c$: piecewise functions and absolute values. \par "
        r"\textbf{Coming later:} once we can take derivatives (Unit 4), \emph{L'Hôpital's rule} gives one more tool for "
        r"$\frac00$ and $\frac{\infty}{\infty}$.")),
    VideoExample('Signs near a zero denominator', work="3cm"),
    VideoExample('Absolute value', work="2.4cm"),
    VideoExample('Two tools in one', work="3.4cm"),
    BigIdea(r"Let the form choose the tool: roots suggest conjugates, polynomials suggest factoring, nested fractions "
            r"suggest a common denominator, and a formula that changes at $c$ means split into sides."),
    Check(r"Find \[ \lim_{x\to0}\frac{\frac{1}{x+2}-\frac12}{x}. \]", num(sp.Rational(-1, 4)),
          limchain(0, [r"\frac{\frac{2-(x+2)}{2(x+2)}}{x}", r"\frac{-x}{2x(x+2)}", r"\frac{-1}{2(x+2)}"], r"-\frac14")),
]
same("check", lim((1 / (x + 2) - sp.Rational(1, 2)) / x, 0), sp.Rational(-1, 4))


def two_sided(c, tex, lft_steps, lval, rgt_steps, rval):
    lft = limchain(c, [tex] + lft_steps, lval, side="^-")
    rgt = limchain(c, [tex] + rgt_steps, rval, side="^+")
    return lft + r" and " + rgt + r". The sides disagree, so the limit does not exist."


# ---------------------------------------------------------------- practice: a deliberate mix (20)
MIX = [
    (r"(2x^2 - 5x + 1)", 2 * x**2 - 5 * x + 1, "3", 3, r"Substitute: $2(9) - 15 + 1 = 4$."),
    (r"\frac{x^2-4}{x^2+5x+6}", (x**2 - 4) / (x**2 + 5 * x + 6), "-2", -2,
     limchain(-2, [r"\frac{(x-2)(x+2)}{(x+2)(x+3)}", r"\frac{x-2}{x+3}"], -4)),
    (r"\frac{\sqrt{x+3}-2}{x-1}", (sp.sqrt(x + 3) - 2) / (x - 1), "1", 1,
     limchain(1, [r"\frac{(x+3)-4}{(x-1)\left(\sqrt{x+3}+2\right)}", r"\frac{1}{\sqrt{x+3}+2}"], r"\frac14")),
    (r"\frac{|x+3|}{x+3}", sp.Abs(x + 3) / (x + 3), "-3", -3,
     r"$\displaystyle\lim_{x\to-3^-}\frac{-(x+3)}{x+3} = -1$ and $\displaystyle\lim_{x\to-3^+}\frac{x+3}{x+3} = 1$: the limit does not exist."),
    (r"\frac{x}{(x-4)^2}", x / (x - 4)**2, "4", 4, r"$\frac40$ with a positive denominator on both sides: $\infty$."),
    (r"\frac{x^2+1}{x-1}", (x**2 + 1) / (x - 1), "1", 1,
     r"$\frac20$; the denominator changes sign at $1$, so the one-sided limits are $-\infty$ and $\infty$. The limit does not exist."),
    (r"\frac{(x+1)^2-1}{x}", ((x + 1)**2 - 1) / x, "0", 0, limchain(0, [r"\frac{x^2+2x}{x}", r"(x+2)"], 2)),
    (r"\frac{\sin^2 x}{1+\cos x}", sp.sin(x)**2 / (1 + sp.cos(x)), r"\pi", sp.pi,
     limchain(r"\pi", [r"\frac{(1-\cos x)(1+\cos x)}{1+\cos x}", r"(1-\cos x)"], 2)),
    (r"\frac{\frac1x-\frac15}{x-5}", (1 / x - sp.Rational(1, 5)) / (x - 5), "5", 5,
     limchain(5, [r"\frac{\frac{5-x}{5x}}{x-5}", r"\left(-\frac{1}{5x}\right)"], r"-\frac1{25}")),
    (r"\frac{x^3-2x^2}{x^2-4}", (x**3 - 2 * x**2) / (x**2 - 4), "2", 2,
     limchain(2, [r"\frac{x^2(x-2)}{(x-2)(x+2)}", r"\frac{x^2}{x+2}"], 1)),
    (r"\frac{x^2-7x+12}{x-3}", (x**2 - 7 * x + 12) / (x - 3), "3", 3, limchain(3, [r"\frac{(x-3)(x-4)}{x-3}", r"(x-4)"], -1)),
    (r"\frac{4-x}{2-\sqrt x}", (4 - x) / (2 - sp.sqrt(x)), "4", 4, limchain(4, [r"\frac{(2-\sqrt x)(2+\sqrt x)}{2-\sqrt x}", r"(2+\sqrt x)"], 4)),
    (r"\frac{x-3}{x^2-6x+9}", (x - 3) / (x**2 - 6 * x + 9), "3", 3,
     r"$\dfrac{x-3}{(x-3)^2}$ simplifies to $\dfrac{1}{x-3}$ for $x \ne 3$, whose one-sided limits are $-\infty$ and $\infty$. "
     r"The limit does not exist."),
    (r"\frac{2x-1}{(x+2)^2}", (2 * x - 1) / (x + 2)**2, "-2", -2, r"$\frac{-5}{0}$ with a positive denominator on both sides: $-\infty$."),
    (r"\frac{|2x-6|}{x-3}", sp.Abs(2 * x - 6) / (x - 3), "3", 3,
     r"$\displaystyle\lim_{x\to3^-}\frac{-2(x-3)}{x-3} = -2$ and $\displaystyle\lim_{x\to3^+}\frac{2(x-3)}{x-3} = 2$: the limit does not exist."),
    (r"\frac{\frac{2}{x}-1}{x-2}", (2 / x - 1) / (x - 2), "2", 2,
     limchain(2, [r"\frac{\frac{2-x}{x}}{x-2}", r"\left(-\frac1x\right)"], r"-\frac12")),
    (r"\frac{x^2-x}{\sqrt{x}-1}", (x**2 - x) / (sp.sqrt(x) - 1), "1", 1,
     limchain(1, [r"\frac{x(\sqrt x-1)(\sqrt x+1)}{\sqrt x-1}", r"x(\sqrt x+1)"], 2)),
    (r"\cos\!\left(\frac{\pi x}{x+1}\right)", sp.cos(sp.pi * x / (x + 1)), "1", 1,
     r"Substitute: $\cos\frac{\pi}{2} = 0$. The function is continuous there, so the limit is $0$."),
]
PRACTICE = [Item(rf"Find $\displaystyle\lim_{{x\to{cs}}}{tex}$. Type DNE if the limit does not exist.", answer(e, c), sol, work="2.2cm")
            for tex, e, cs, c, sol in MIX]
PRACTICE += [
    Item(r"Let $f(x) = \begin{cases} \dfrac{x^2-1}{x-1}, & x < 1 \\ 3 - x, & x \ge 1. \end{cases}$ Find $\displaystyle\lim_{x\to1} f(x)$.",
         num(2), limchain(1, [r"\frac{x^2-1}{x-1}", r"(x+1)"], 2, side="^-") + r" and " + limchain(1, [r"(3-x)"], 2, side="^+")
         + r". The sides agree, so the limit is $2$.", work="2cm"),
    Item(r"Let $g(x) = \begin{cases} x^2 + 2, & x < 0 \\ \dfrac{\sin 2x}{x}, & x > 0. \end{cases}$ Find $\displaystyle\lim_{x\to0} g(x)$.",
         num(2), limchain(0, [r"(x^2+2)"], 2, side="^-") + r" and $\displaystyle\lim_{x\to0^+}\frac{\sin 2x}{x} = 2$ (Topic 1.4's table "
         r"suggests this; Topic 1.8 proves it). The limit is $2$.", work="2cm"),
]
same("p19 left", lim((x**2 - 1) / (x - 1), 1), 2)
same("p20", lim(sp.sin(2 * x) / x, 0), 2)

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find $\displaystyle\lim_{x\to-1}\frac{x^2-3x-4}{x+1}$.", num(-5),
             limchain(-1, [r"\frac{(x-4)(x+1)}{x+1}", r"(x-4)"], -5), work="2cm"),
        Item(r"Find $\displaystyle\lim_{x\to2}\frac{x^2+x-6}{x^2-4}$.", num(sp.Rational(5, 4)),
             limchain(2, [r"\frac{(x+3)(x-2)}{(x+2)(x-2)}", r"\frac{x+3}{x+2}"], r"\frac54"), work="2cm"),
        Item(r"Find $\displaystyle\lim_{x\to4}\frac{x^2-5x}{x+1}$.", num(sp.Rational(-4, 5)),
             r"Substitution works: $\dfrac{16-20}{5} = -\dfrac45$.", work="2cm"),
    ),
    Variants(
        Item(r"Find $\displaystyle\lim_{x\to0}\frac{\sqrt{x+9}-3}{x}$.", num(sp.Rational(1, 6)),
             limchain(0, [r"\frac{(x+9)-9}{x\left(\sqrt{x+9}+3\right)}", r"\frac1{\sqrt{x+9}+3}"], r"\frac16"), work="2cm"),
        Item(r"Find $\displaystyle\lim_{x\to0}\frac{\frac{1}{x-2}+\frac12}{x}$.", num(sp.Rational(-1, 4)),
             limchain(0, [r"\frac{\frac{2+(x-2)}{2(x-2)}}{x}", r"\frac{1}{2(x-2)}"], r"-\frac14"), work="2cm"),
        Item(r"Find $\displaystyle\lim_{x\to1}\frac{\sqrt{x+3}-2}{x-1}$.", num(sp.Rational(1, 4)),
             limchain(1, [r"\frac{(x+3)-4}{(x-1)\left(\sqrt{x+3}+2\right)}", r"\frac1{\sqrt{x+3}+2}"], r"\frac14"), work="2cm"),
    ),
    Variants(
        Item(r"Find $\displaystyle\lim_{x\to3}\frac{x-5}{(x-3)^2}$. Type DNE if it does not exist.", infinite(-1),
             r"$\frac{-2}{0}$; the denominator is positive on both sides, so both one-sided limits are $-\infty$: the limit is $-\infty$.",
             work="1.8cm"),
        Item(r"Find $\displaystyle\lim_{x\to-2}\frac{x+6}{(x+2)^2}$. Type DNE if it does not exist.", infinite(1),
             r"$\frac{4}{0}$; the top is positive and the bottom is positive on both sides, so the limit is $\infty$.", work="1.8cm"),
        Item(r"Find $\displaystyle\lim_{x\to1}\frac{x+1}{x-1}$. Type DNE if it does not exist.", dne(),
             r"$\frac20$; the bottom is negative on the left and positive on the right, so the sides go to $-\infty$ and $\infty$. "
             r"The limit does not exist.", work="1.8cm"),
    ),
    Variants(
        MCQ(r"Which method fits $\displaystyle\lim_{x\to4}\frac{x-4}{\sqrt x - 2}$ best?",
            [r"Direct substitution", r"Multiply by the conjugate $\sqrt x + 2$", r"Combine fractions", r"Split into sides"], "B",
            r"Substitution gives $\frac00$ and there is a square root: use the conjugate. "
            + limchain(4, [r"\frac{(x-4)(\sqrt x+2)}{x-4}", r"(\sqrt x+2)"], 4), why_not={"A": "substitution gives $\\frac00$"}),
        MCQ(r"Which method fits $\displaystyle\lim_{x\to0}\frac{\frac{1}{x+3}-\frac13}{x}$ best?",
            [r"Direct substitution", r"Multiply by a conjugate", r"Combine the fractions in the numerator", r"Split into sides"], "C",
            r"Substitution gives $\frac00$, and the numerator is a difference of fractions: combine them over $3(x+3)$ first.",
            why_not={"A": "substitution gives $\\frac00$", "B": "there is no square root"}),
        MCQ(r"Which method fits $\displaystyle\lim_{x\to2}\frac{|x-2|}{x-2}$ best?",
            [r"Split into sides", r"Factor and cancel", r"Multiply by a conjugate", r"Direct substitution"], "A",
            r"An absolute value changes its formula at $x = 2$, so find each one-sided limit.",
            why_not={"D": "substitution gives $\\frac00$", "B": "nothing factors out of an absolute value"}),
    ),
    Variants(
        MCQ(r"$\displaystyle\lim_{x\to-5}\frac{|x+5|}{x+5}$ is", [r"$-1$", r"$0$", r"$1$", r"Does not exist"], "D",
            r"The left-hand limit is $-1$ and the right-hand limit is $1$.", why_not={"A": "left side only", "C": "right side only"}),
        MCQ(r"$\displaystyle\lim_{x\to3^-}\frac{|x-3|}{x-3}$ is", [r"$1$", r"$-1$", r"$0$", r"Does not exist"], "B",
            r"For $x < 3$, $|x - 3| = -(x - 3)$, so the quotient is $-1$.", why_not={"A": "that's the right side", "D": "a one-sided limit can exist even when the two-sided one doesn't"}),
        MCQ(r"$\displaystyle\lim_{x\to0}\frac{x^2}{|x|}$ is", [r"$1$", r"Does not exist", r"$0$", r"$-1$"], "C",
            r"$\frac{x^2}{|x|} = |x|$ for $x \ne 0$, and $|x|$ heads to $0$ from both sides.",
            why_not={"B": "both sides agree here", "A": "that's $\\frac{|x|}{x}$ on the right"}),
    ),
]
same("q1", lim((x**2 - 3 * x - 4) / (x + 1), -1), -5)
same("q2", lim((sp.sqrt(x + 9) - 3) / x, 0), sp.Rational(1, 6))
same("q3", lim((x - 5) / (x - 3)**2, 3), -sp.oo)
same("q4", lim((x - 4) / (sp.sqrt(x) - 2), 4), 4)
same("q versions", [lim((x**2 + x - 6) / (x**2 - 4), 2), lim((x**2 - 5 * x) / (x + 1), 4), lim((1 / (x - 2) + sp.Rational(1, 2)) / x, 0),
                    lim((sp.sqrt(x + 3) - 2) / (x - 1), 1), lim((x + 6) / (x + 2)**2, -2), lim(x**2 / sp.Abs(x), 0)],
     [sp.Rational(5, 4), sp.Rational(-4, 5), sp.Rational(-1, 4), sp.Rational(1, 4), sp.oo, 0])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$\displaystyle\lim_{x\to2}\frac{x^2-x-2}{x^2-4}$ is", [r"$0$", r"$\dfrac34$", r"$1$", r"Does not exist"], "B",
        limchain(2, [r"\frac{(x-2)(x+1)}{(x-2)(x+2)}", r"\frac{x+1}{x+2}"], r"\frac34")),
    MCQ(r"$\displaystyle\lim_{x\to0}\frac{x}{\sqrt{x+1}-1}$ is", [r"$2$", r"$1$", r"$\dfrac12$", r"$0$"], "A",
        limchain(0, [r"\frac{x\left(\sqrt{x+1}+1\right)}{(x+1)-1}", r"\left(\sqrt{x+1}+1\right)"], 2), why_not={"C": "inverted the result"}),
    MCQ(r"$\displaystyle\lim_{x\to-2^+}\frac{x-1}{x+2}$ is", [r"$-\infty$", r"$0$", r"$\infty$", r"$-\dfrac14$"], "A",
        r"$\frac{-3}{0}$. For $x$ slightly above $-2$, $x + 2 > 0$ and $x - 1 < 0$, so the quotient is large and negative.",
        why_not={"C": "ignored the sign of the numerator"}),
    MCQ(r"Let $g(x) = \begin{cases} \dfrac{\sin^2 x}{1-\cos x}, & x \ne 0 \\ 5, & x = 0. \end{cases}$ What is $\displaystyle\lim_{x\to0} g(x)$?",
        [r"$0$", r"$1$", r"$5$", r"$2$"], "D",
        limchain(0, [r"\frac{(1-\cos x)(1+\cos x)}{1-\cos x}", r"(1+\cos x)"], 2) + r". The value $g(0) = 5$ does not affect the limit.",
        why_not={"C": "used $g(0)$"}),
]
same("m1", lim((x**2 - x - 2) / (x**2 - 4), 2), sp.Rational(3, 4))
same("m2", lim(x / (sp.sqrt(x + 1) - 1), 0), 2)
same("m3", lim((x - 1) / (x + 2), -2, "+"), -sp.oo)
same("m4", lim(sp.sin(x)**2 / (1 - sp.cos(x)), 0), 2)

# AP does not ask this topic as free response; the multiple-choice questions above cover it.
# See .claude/skills/ap-frq/SKILL.md.
FRQS = []

TOPIC = Topic(
    number="1.7", title="Selecting Procedures for Determining Limits",
    unit="Unit 1: Limits and Continuity", ced=["LIM-1.D", "LIM-1.E"],
    goals=r"Choose an efficient method for a limit by substituting first and reading the form of the result.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
