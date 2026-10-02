"""Topic 1.6: Determining limits using algebraic manipulation.

CED: LIM-1.E.1 (rewrite into equivalent forms before evaluating). Tools, in the order the
video shows them: factor and cancel, conjugates, combining fractions, trig identities. Also
contrasts 0/0 (rewrite) with nonzero/0 (unbounded). Every solution keeps limit notation on
every line: the functions differ at c, but their limits agree.
"""
import sympy as sp

from calclib import (VideoExample, Variants, FRQ, MCQ, BigIdea, Check, Definition, Example, Formula, Item, Part, Section, Text, Topic, Video,
                     check, dne, infinite, limchain, num, same, selfcheck)

x, h = sp.symbols("x h")


def L(e, c, d="+-", v=x):
    return sp.limit(e, v, c) if d == "+-" else sp.limit(e, v, c, d)


same("intro", L((x**2 - 9) / (x - 3), 3), 6)
same("cubes", L((x**3 - 8) / (x - 2), 2), 12)
same("conj", L((sp.sqrt(x + 4) - 2) / x, 0), sp.Rational(1, 4))
same("fractions", L((1 / x - sp.Rational(1, 3)) / (x - 3), 3), sp.Rational(-1, 9))
same("trig", L(sp.sin(x)**2 / (1 - sp.cos(x)), 0), 2)
same("nonzero/0 L", L((x + 1) / (x - 3), 3, "-"), -sp.oo)
same("nonzero/0 R", L((x + 1) / (x - 3), 3, "+"), sp.oo)

NOTES = [
    Video("s1_6.py::Lesson", "Algebra for 0/0 limits", 4),

    Section("What 0/0 tells you"),
    Text(r"Substituting $x = 3$ into $\dfrac{x^2-9}{x-3}$ yields \mblank{\tfrac00}. This is called an "
         r"\textbf{indeterminate form}: it gives no answer yet. It means \blank{rewrite the expression}. After rewriting, the "
         r"limit may turn out to be a number, or it may still \blank{not exist}: "
         r"\[ \lim_{x\to1}\frac{x-1}{(x-1)^2} = \lim_{x\to1}\frac{1}{x-1}, \] and that goes to $-\infty$ from the left "
         r"and $\infty$ from the right."),
    Definition("The key fact", (
        r"If $f(x) = g(x)$ for all $x$ near $c$ (except possibly at $x = c$), then "
        r"\[ \lim_{x\to c} f(x) = \lim_{x\to c} g(x). \]")),
    Text(r"$\dfrac{x^2-9}{x-3}$ and $x + 3$ are \emph{not} the same function: the first is undefined at $x = 3$, and its graph is "
         r"the line $y = x+3$ with a \blank{hole} at $(3, 6)$. But they agree for every $x \ne 3$, so their \emph{limits} at $3$ agree:"
         r"\[ \lim_{x\to3}\frac{x^2-9}{x-3} = \lim_{x\to3}\frac{(x-3)(x+3)}{x-3} = \lim_{x\to3}(x+3) = \mblank{6} \]."
         r"Keep the limit notation on every line. Writing $\displaystyle \dfrac{x^2-9}{x-3} = x + 3$ without it is false at $x = 3$."),

    Section("The toolkit"),
    Formula("Rewriting strategies for $\\frac00$", (
        r"\textbf{1. Factor and cancel} a common factor. \par "
        r"\textbf{2. Multiply by the conjugate} when a square root is involved: $(\sqrt a - b)(\sqrt a + b) = a - b^2$. \par "
        r"\textbf{3. Combine fractions} over a common denominator. \par "
        r"\textbf{4. Use an identity}, such as $\sin^2 x = 1 - \cos^2 x$. \par "
        r"\textbf{5. Expand} a power, then simplify.")),
    VideoExample('Factor', work="2.6cm"),
    Formula("Review: conjugates", (
        r"The conjugate of $a + b$ is $a - b$, and \[ (a + b)(a - b) = a^2 - b^2. \] "
        r"Multiplying by a conjugate clears a square root. From algebra: "
        r"\[ \frac{1}{\sqrt5 - 2} = \frac{1}{\sqrt5 - 2}\cdot\frac{\sqrt5 + 2}{\sqrt5 + 2} = \frac{\sqrt5 + 2}{5 - 4} = \sqrt5 + 2. \] "
        r"The same move works inside a limit.")),
    VideoExample('Conjugate', work="2.8cm"),
    VideoExample('Combine fractions', work="2.8cm"),
    Formula("The Pythagorean identity", (
        r"\[ \sin^2 x + \cos^2 x = 1 \] "
        r"It is the Pythagorean theorem on the unit circle: the point at angle $x$ has legs $\cos x$ and $\sin x$ and hypotenuse $1$. "
        r"This is the one trig identity AP Calculus expects you to know. Know its other forms too: "
        r"$1 - \cos^2 x = \mblank{\sin^2 x}$ and $1 - \sin^2 x = \mblank{\cos^2 x}$.")),
    VideoExample('Identity', work="2.6cm"),

    Section("When substitution yields nonzero over zero"),
    Text(r"At $x = 3$, $\dfrac{x+1}{x-3}$ yields $\dfrac40$. No rewriting helps: the numerator stays near $4$ while the "
         r"denominator shrinks to $0$, so the quotient grows without bound. Here "
         r"$\displaystyle \lim_{x\to3^-}\frac{x+1}{x-3} = \mblank{-\infty}$ and "
         r"$\displaystyle \lim_{x\to3^+}\frac{x+1}{x-3} = \mblank{\infty}$, so the two-sided limit \blank{does not exist}."),
    BigIdea(r"Substitute first and read the result: a number means done; $\frac00$ means rewrite and try again; "
            r"$\displaystyle \dfrac{\text{nonzero}}{0}$ means unbounded behavior (Topic 1.14). Keep writing $\lim$ until the last step."),
    Check(r"Find \[ \lim_{h\to0}\frac{(3+h)^2-9}{h}. \]", num(6),
          limchain(0, [r"\frac{(3+h)^2-9}{h}", r"\frac{6h+h^2}{h}", r"(6+h)"], 6, var="h")),
]
same("check", L(((3 + h)**2 - 9) / h, 0, v=h), 6)

# ---------------------------------------------------------------- practice (20)
P = [
    ((x**2 + 2 * x - 8) / (x + 4), -4, [r"\frac{(x+4)(x-2)}{x+4}", r"(x-2)"]),
    ((x**2 - 1) / (x**2 + 3 * x - 4), 1, [r"\frac{(x-1)(x+1)}{(x-1)(x+4)}", r"\frac{x+1}{x+4}"]),
    ((sp.sqrt(x) - 3) / (x - 9), 9, [r"\frac{(\sqrt x - 3)(\sqrt x+3)}{(x-9)(\sqrt x+3)}", r"\frac{x-9}{(x-9)(\sqrt x+3)}", r"\frac{1}{\sqrt x+3}"]),
    ((sp.sqrt(1 + x) - sp.sqrt(1 - x)) / x, 0, [r"\frac{(1+x)-(1-x)}{x\left(\sqrt{1+x}+\sqrt{1-x}\right)}", r"\frac{2}{\sqrt{1+x}+\sqrt{1-x}}"]),
    ((1 / (x + 2) - sp.Rational(1, 4)) / (x - 2), 2, [r"\frac{\frac{4-(x+2)}{4(x+2)}}{x-2}", r"\frac{-(x-2)}{4(x+2)(x-2)}", r"\frac{-1}{4(x+2)}"]),
    (sp.cos(x)**2 / (1 - sp.sin(x)), sp.pi / 2, [r"\frac{(1-\sin x)(1+\sin x)}{1-\sin x}", r"(1+\sin x)"]),
    ((x**3 + 1) / (x + 1), -1, [r"\frac{(x+1)(x^2-x+1)}{x+1}", r"(x^2-x+1)"]),
    ((x**2 - 5 * x + 6) / (x**2 - 9), 3, [r"\frac{(x-2)(x-3)}{(x-3)(x+3)}", r"\frac{x-2}{x+3}"]),
    ((x**4 - 16) / (x - 2), 2, [r"\frac{(x-2)(x+2)(x^2+4)}{x-2}", r"(x+2)(x^2+4)"]),
    ((2 * x**2 - x - 3) / (x + 1), -1, [r"\frac{(2x-3)(x+1)}{x+1}", r"(2x-3)"]),
    ((x - 16) / (sp.sqrt(x) - 4), 16, [r"\frac{(\sqrt x-4)(\sqrt x+4)}{\sqrt x - 4}", r"(\sqrt x + 4)"]),
    ((sp.sqrt(x + 5) - 3) / (x - 4), 4, [r"\frac{(x+5)-9}{(x-4)\left(\sqrt{x+5}+3\right)}", r"\frac{1}{\sqrt{x+5}+3}"]),
    ((1 / x - sp.Rational(1, 5)) / (x - 5), 5, [r"\frac{\frac{5-x}{5x}}{x-5}", r"\left(-\frac{1}{5x}\right)"]),
    ((1 - sp.cos(x)) / sp.sin(x)**2, 0, [r"\frac{1-\cos x}{(1-\cos x)(1+\cos x)}", r"\frac{1}{1+\cos x}"]),
    ((x**3 - 27) / (x - 3), 3, [r"\frac{(x-3)(x^2+3x+9)}{x-3}", r"(x^2+3x+9)"]),
]
TEX = [r"\frac{x^2+2x-8}{x+4}", r"\frac{x^2-1}{x^2+3x-4}", r"\frac{\sqrt x - 3}{x-9}", r"\frac{\sqrt{1+x}-\sqrt{1-x}}{x}",
       r"\frac{\frac{1}{x+2}-\frac14}{x-2}", r"\frac{\cos^2 x}{1-\sin x}", r"\frac{x^3+1}{x+1}", r"\frac{x^2-5x+6}{x^2-9}",
       r"\frac{x^4-16}{x-2}", r"\frac{2x^2-x-3}{x+1}", r"\frac{x-16}{\sqrt x - 4}", r"\frac{\sqrt{x+5}-3}{x-4}",
       r"\frac{\frac1x-\frac15}{x-5}", r"\frac{1-\cos x}{\sin^2 x}", r"\frac{x^3-27}{x-3}"]
CS = ["-4", "1", "9", "0", "2", r"\frac{\pi}{2}", "-1", "3", "2", "-1", "16", "4", "5", "0", "3"]
PRACTICE = []
for (e, c, steps), tex, cs in zip(P, TEX, CS):
    val = L(e, c)
    check(f"practice {tex} finite", bool(val.is_finite), str(val))
    same(f"practice {tex} both sides", L(e, c, "-"), L(e, c, "+"))
    PRACTICE.append(Item(rf"Find $\displaystyle\lim_{{x\to{cs}}}{tex}$.", num(val),
                         limchain(cs, [tex] + steps, sp.latex(val)), work="2.4cm"))
PRACTICE += [
    Item(r"Find $\displaystyle\lim_{h\to0}\frac{(2+h)^3-8}{h}$.", num(12),
         limchain(0, [r"\frac{(2+h)^3-8}{h}", r"\frac{12h+6h^2+h^3}{h}", r"(12+6h+h^2)"], 12, var="h")),
    Item(r"Find $\displaystyle\lim_{h\to0}\frac{\frac{1}{3+h}-\frac13}{h}$.", num(sp.Rational(-1, 9)),
         limchain(0, [r"\frac{\frac{3-(3+h)}{3(3+h)}}{h}", r"\frac{-h}{3h(3+h)}", r"\frac{-1}{3(3+h)}"], r"-\frac19", var="h")),
    Item(r"Find $\displaystyle\lim_{x\to2^+}\frac{x+3}{x-2}$.", infinite(1),
         r"Substitution yields $\frac50$. For $x$ slightly above $2$, the denominator is a small positive number, so the quotient "
         r"grows without bound: $\displaystyle\lim_{x\to2^+}\frac{x+3}{x-2} = \infty$."),
    Item(r"Find $\displaystyle\lim_{x\to1}\frac{x+1}{x-1}$, or type DNE.", dne(),
         r"$\frac20$. The denominator is negative for $x<1$ and positive for $x > 1$, so the one-sided limits are $-\infty$ and "
         r"$\infty$. The limit does not exist."),
    Item(r"Mei writes $\displaystyle\lim_{x\to5}\frac{x^2-25}{x-5} = \frac00 = 0$. Explain the mistake and find the limit.", num(10),
         r"$\frac00$ is indeterminate, not $0$. " + limchain(5, [r"\frac{x^2-25}{x-5}", r"\frac{(x-5)(x+5)}{x-5}", r"(x+5)"], 10)),
]
same("p16", L(((2 + h)**3 - 8) / h, 0, v=h), 12)
same("p17", L((1 / (3 + h) - sp.Rational(1, 3)) / h, 0, v=h), sp.Rational(-1, 9))
same("p18", L((x + 3) / (x - 2), 2, "+"), sp.oo)
same("p19", [L((x + 1) / (x - 1), 1, "-"), L((x + 1) / (x - 1), 1, "+")], [-sp.oo, sp.oo])

PRACTICE += [
    Item(r"Find $\displaystyle\lim_{x\to2}\frac{x-2}{x^2-4x+4}$, or type DNE. Substitution yields $\frac00$, so rewrite first.", dne(),
         limchain(2, [r"\frac{x-2}{(x-2)^2}", r"\frac{1}{x-2}"], r"?") .replace(" = ?$", "$")
         + r". Now substitution yields $\frac10$: the function goes to $-\infty$ from the left and $\infty$ from the right, so "
         r"the limit does not exist. The $\frac00$ at the start did not promise a number.", work="2cm"),
]
same("0/0 then DNE", [sp.limit((x - 2) / (x**2 - 4 * x + 4), x, 2, "-"), sp.limit((x - 2) / (x**2 - 4 * x + 4), x, 2, "+")],
     [-sp.oo, sp.oo])

# ---------------------------------------------------------------- quiz
ZERO = {"A": "$\\frac00$ is not $0$", "C": "$\\frac00$ is not $1$"}
QUIZ = [
    Variants(
        Item(r"Find $\displaystyle\lim_{x\to3}\frac{x^2-x-6}{x-3}$.", num(5),
             limchain(3, [r"\frac{x^2-x-6}{x-3}", r"\frac{(x-3)(x+2)}{x-3}", r"(x+2)"], 5), work="2cm"),
        Item(r"Find $\displaystyle\lim_{x\to-4}\frac{x^2+x-12}{x+4}$.", num(-7),
             limchain(-4, [r"\frac{x^2+x-12}{x+4}", r"\frac{(x+4)(x-3)}{x+4}", r"(x-3)"], -7), work="2cm"),
        Item(r"Find $\displaystyle\lim_{x\to2}\frac{x^3-8}{x^2-4}$.", num(3),
             limchain(2, [r"\frac{(x-2)(x^2+2x+4)}{(x-2)(x+2)}", r"\frac{x^2+2x+4}{x+2}"], 3), work="2cm"),
    ),
    Variants(
        Item(r"Find $\displaystyle\lim_{x\to16}\frac{\sqrt x-4}{x-16}$.", num(sp.Rational(1, 8)),
             limchain(16, [r"\frac{\sqrt x-4}{x-16}", r"\frac{\sqrt x - 4}{(\sqrt x-4)(\sqrt x+4)}", r"\frac{1}{\sqrt x+4}"], r"\frac18"), work="2cm"),
        Item(r"Find $\displaystyle\lim_{x\to0}\frac{\sqrt{x+4}-2}{x}$.", num(sp.Rational(1, 4)),
             limchain(0, [r"\frac{(x+4)-4}{x(\sqrt{x+4}+2)}", r"\frac{1}{\sqrt{x+4}+2}"], r"\frac14"), work="2cm"),
        Item(r"Find $\displaystyle\lim_{x\to5}\frac{x-5}{\sqrt{x+4}-3}$.", num(6),
             limchain(5, [r"\frac{(x-5)(\sqrt{x+4}+3)}{(x+4)-9}", r"(\sqrt{x+4}+3)"], 6), work="2cm"),
    ),
    Variants(
        Item(r"Find $\displaystyle\lim_{x\to0}\frac{\frac{1}{x+5}-\frac15}{x}$.", num(sp.Rational(-1, 25)),
             limchain(0, [r"\frac{\frac{5-(x+5)}{5(x+5)}}{x}", r"\frac{-x}{5x(x+5)}", r"\frac{-1}{5(x+5)}"], r"-\frac1{25}"), work="2cm"),
        Item(r"Find $\displaystyle\lim_{x\to2}\frac{\frac1x-\frac12}{x-2}$.", num(sp.Rational(-1, 4)),
             limchain(2, [r"\frac{\frac{2-x}{2x}}{x-2}", r"\frac{-1}{2x}"], r"-\frac14"), work="2cm"),
        Item(r"Find $\displaystyle\lim_{x\to-1}\frac{\frac{3}{x+4}-1}{x+1}$.", num(sp.Rational(-1, 3)),
             limchain(-1, [r"\frac{\frac{3-(x+4)}{x+4}}{x+1}", r"\frac{-(x+1)}{(x+4)(x+1)}", r"\frac{-1}{x+4}"], r"-\frac13"), work="2cm"),
    ),
    Variants(
        MCQ(r"Direct substitution into a limit yields $\dfrac00$. What can you conclude?",
            [r"The limit is $0$.", r"The limit does not exist.", r"The limit is $1$.",
             r"Nothing yet; rewrite the expression and try again."], "D",
            r"$\frac00$ is indeterminate. Limits giving $\frac00$ can equal any number, or fail to exist.", why_not=ZERO),
        MCQ(r"$\displaystyle\lim_{x\to1}\frac{x-1}{x^2-2x+1}$: substitution yields $\frac00$. After rewriting, what is the limit?",
            [r"$0$", r"$1$", r"$\frac12$", r"Does not exist."], "D",
            r"It rewrites to $\frac{1}{x-1}$, which heads to $-\infty$ from the left and $\infty$ from the right. $\frac00$ never promised a number.",
            why_not={"A": ZERO["A"], "B": ZERO["C"]}),
        MCQ(r"Why is $\displaystyle\lim_{x\to3}\frac{x^2-9}{x-3} = \lim_{x\to3}(x+3)$ a correct step?",
            [r"Because $\dfrac{x^2-9}{x-3}$ and $x + 3$ are the same function.",
             r"Because the two functions agree for every $x$ near $3$ except $x = 3$, and a limit never uses $x = 3$ itself.",
             r"Because $\frac00 = 6$.", r"Because both are undefined at $3$."], "B",
            r"The functions are different (one is undefined at $3$), but they agree everywhere near $3$, so their limits agree.",
            why_not={"A": "they differ at $x = 3$", "D": "$x + 3$ is defined at $3$"}),
    ),
    Variants(
        MCQ(r"$\displaystyle\lim_{x\to1}\frac{x-1}{\sqrt x - 1}$ is", [r"$0$", r"$\dfrac12$", r"$2$", r"Does not exist"], "C",
            limchain(1, [r"\frac{(\sqrt x-1)(\sqrt x+1)}{\sqrt x - 1}", r"(\sqrt x+1)"], 2), why_not={"B": "inverted the result"}),
        MCQ(r"$\displaystyle\lim_{x\to-3}\frac{x^2+3x}{x^2-9}$ is", [r"$\dfrac12$", r"$0$", r"$-\dfrac12$", r"Does not exist"], "A",
            limchain(-3, [r"\frac{x(x+3)}{(x-3)(x+3)}", r"\frac{x}{x-3}"], r"\frac12"), why_not={"C": "sign slip in $\\frac{-3}{-6}$"}),
        MCQ(r"$\displaystyle\lim_{h\to0}\frac{(1+h)^2-1}{h}$ is", [r"$0$", r"$1$", r"Does not exist", r"$2$"], "D",
            limchain(0, [r"\frac{2h+h^2}{h}", r"(2+h)"], 2, var="h"), why_not={"A": "treated $\\frac00$ as $0$"}),
    ),
]
same("q1", L((x**2 - x - 6) / (x - 3), 3), 5)
same("q2", L((sp.sqrt(x) - 4) / (x - 16), 16), sp.Rational(1, 8))
same("q3", L((1 / (x + 5) - sp.Rational(1, 5)) / x, 0), sp.Rational(-1, 25))
same("q5", L((x - 1) / (sp.sqrt(x) - 1), 1), 2)
same("q versions", [L((x**2 + x - 12) / (x + 4), -4), L((x**3 - 8) / (x**2 - 4), 2), L((sp.sqrt(x + 4) - 2) / x, 0),
                    L((x - 5) / (sp.sqrt(x + 4) - 3), 5), L((1 / x - sp.Rational(1, 2)) / (x - 2), 2), L((3 / (x + 4) - 1) / (x + 1), -1),
                    L((x**2 + 3 * x) / (x**2 - 9), -3)],
     [-7, 3, sp.Rational(1, 4), 6, sp.Rational(-1, 4), sp.Rational(-1, 3), sp.Rational(1, 2)])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$\displaystyle\lim_{x\to-3}\frac{x^2+x-6}{x^2-9}$ is", [r"$0$", r"$\dfrac56$", r"$-\dfrac56$", r"Does not exist"], "B",
        limchain(-3, [r"\frac{(x+3)(x-2)}{(x+3)(x-3)}", r"\frac{x-2}{x-3}"], r"\frac{-5}{-6} = \frac56"),
        why_not={"C": "sign error in one factor"}),
    MCQ(r"$\displaystyle\lim_{x\to0}\frac{\sqrt{9+x}-3}{x}$ is", [r"$\dfrac16$", r"$\dfrac13$", r"$0$", r"Does not exist"], "A",
        limchain(0, [r"\frac{(9+x)-9}{x\left(\sqrt{9+x}+3\right)}", r"\frac{1}{\sqrt{9+x}+3}"], r"\frac16"), why_not={"B": "dropped a factor of 2"}),
    MCQ(r"$\displaystyle\lim_{x\to0}\frac{1-\cos^2 x}{x\sin x}$ is", [r"$0$", r"$\dfrac12$", r"$1$", r"Does not exist"], "C",
        limchain(0, [r"\frac{\sin^2 x}{x\sin x}", r"\frac{\sin x}{x}"], 1) + r" (Topic 1.4 estimated this last limit; Topic 1.8 proves it.)"),
    MCQ(r"If $f(x) = x^2 + 1$, then $\displaystyle\lim_{h\to0}\frac{f(3+h)-f(3)}{h}$ is", [r"$0$", r"$3$", r"$10$", r"$6$"], "D",
        limchain(0, [r"\frac{(3+h)^2+1-10}{h}", r"\frac{6h+h^2}{h}", r"(6+h)"], 6, var="h")
        + r" (This is the slope of $f$ at $x=3$: the derivative of Unit 2.)", why_not={"C": "that is $f(3)$"}),
]
same("m1", L((x**2 + x - 6) / (x**2 - 9), -3), sp.Rational(5, 6))
same("m2", L((sp.sqrt(9 + x) - 3) / x, 0), sp.Rational(1, 6))
same("m3", L((1 - sp.cos(x)**2) / (x * sp.sin(x)), 0), 1)
same("m4", L(((3 + h)**2 + 1 - 10) / h, 0, v=h), 6)

# AP does not ask this topic as free response; the multiple-choice questions above cover it.
# See .claude/skills/ap-frq/SKILL.md.
FRQS = []

TOPIC = Topic(
    number="1.6", title="Determining Limits Using Algebraic Manipulation",
    unit="Unit 1: Limits and Continuity", ced=["LIM-1.E", "LIM-1.E.1"],
    goals=r"Rewrite expressions (factor, conjugate, combine fractions, use identities) to evaluate limits of the form $\frac00$.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
