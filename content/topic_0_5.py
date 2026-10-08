"""Topic 0.5: Trigonometric identities (trig review; not a CED topic).

The three Pythagorean identities; even/odd and cofunction identities; sum and difference formulas; double-angle formulas
(three forms of cos 2a); power-reducing formulas (needed later to integrate sin^2 and cos^2). Lesson example: simplify
(1 - cos^2 x)/(sin x cos x). Worked examples: cos(pi/12), verifying sec x - cos x = sin x tan x, sin 2x and cos 2x from
sin x = 3/5, simplifying sin 2x/(1 + cos 2x).
"""
import sympy as sp

from calclib import (VideoExample, MCQ, BigIdea, Check, Formula, Item, Section, Text, Topic, Variants, Video, expr, num, same, selfcheck)

pi, x = sp.pi, sp.Symbol("x")
r2, r3 = sp.sqrt(2), sp.sqrt(3)


def ident(name, a, b):
    """a == b for every x (checked symbolically, then at sample points)."""
    if sp.simplify(a - b) != 0:
        for v in (0.3, 1.1, 2.5, -0.7):
            if abs(complex(sp.N((a - b).subs(x, v)))) > 1e-9:
                raise SystemExit(f"identity check failed: {name}")


ident("lesson", (1 - sp.cos(x)**2) / (sp.sin(x) * sp.cos(x)), sp.tan(x))
same("ex1", [sp.cos(pi / 12)], [(sp.sqrt(6) + r2) / 4])
ident("ex2", 1 / sp.cos(x) - sp.cos(x), sp.sin(x) * sp.tan(x))
same("ex3", [2 * sp.Rational(3, 5) * (-sp.Rational(4, 5)), 1 - 2 * sp.Rational(9, 25)], [-sp.Rational(24, 25), sp.Rational(7, 25)])
ident("ex4", sp.sin(2 * x) / (1 + sp.cos(2 * x)), sp.tan(x))
ident("power", sp.sin(x)**2, (1 - sp.cos(2 * x)) / 2)

NOTES = [
    Video("s0_5.py::Lesson", "Trigonometric identities", 8),

    Text(r"An \textbf{identity} is an equation that is true for every input where both sides are defined. Calculus uses identities to rewrite expressions into easier forms."),

    Section("Pythagorean identities"),
    Formula("Pythagorean identities", r"\[ \sin^2\theta + \cos^2\theta = 1, \qquad \tan^2\theta + 1 = \sec^2\theta, \qquad 1 + \cot^2\theta = \csc^2\theta. \] "
            r"The second and third come from dividing the first by $\cos^2\theta$ and by $\sin^2\theta$."),
    VideoExample("Simplifying an expression", work="2.6cm"),

    Section("Even, odd, and cofunction identities"),
    Formula("Symmetry", r"\[ \cos(-\theta) = \cos\theta, \qquad \sin(-\theta) = -\sin\theta, \qquad \tan(-\theta) = -\tan\theta \] "
            r"\[ \sin\left(\tfrac{\pi}{2} - \theta\right) = \cos\theta, \qquad \cos\left(\tfrac{\pi}{2} - \theta\right) = \sin\theta \]"),
    Text(r"Cosine is \textbf{even} (its graph is symmetric about the $y$-axis); sine and tangent are \textbf{odd}. ``Cosine'' is the sine of the complementary angle."),

    Section("Sum, difference, and double angles"),
    Formula("Sum and difference", r"\[ \sin(a \pm b) = \sin a\cos b \pm \cos a\sin b, \qquad \cos(a \pm b) = \cos a\cos b \mp \sin a\sin b. \] "
            r"Warning: $\sin(a + b) \ne \sin a + \sin b$."),
    Formula("Double angles", (r"Set $b = a$: \[ \sin 2a = \blank{2\sin a\cos a}, \qquad \cos 2a = \cos^2 a - \sin^2 a = \blank{2\cos^2 a - 1} = \blank{1 - 2\sin^2 a}. \]")),
    Formula("Power-reducing", (r"Solve the last two forms of $\cos 2x$ for the square: \[ \cos^2 x = \blank{\frac{1 + \cos 2x}{2}}, \qquad \sin^2 x = \blank{\frac{1 - \cos 2x}{2}}. \]")),
    BigIdea(r"Most simplifications start from $\sin^2\theta + \cos^2\theta = 1$ or from rewriting everything in sines and cosines."),
    Check(r"Simplify $\cos^2 x - \cos^4 x$ as a product of powers of $\sin x$ and $\cos x$.", selfcheck(r"\sin^2 x\cos^2 x"), r"$\cos^2 x(1 - \cos^2 x) = \cos^2 x\sin^2 x$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Simplify $\sin x\cot x$.", expr(sp.cos(x)), r"$\sin x \cdot \frac{\cos x}{\sin x} = \cos x$.", work="1cm"),
    Item(r"Simplify $\sec^2 x - \tan^2 x$.", num(1), r"$\tan^2 x + 1 = \sec^2 x$.", work="1cm"),
    Item(r"Simplify $\dfrac{1 - \sin^2 x}{\cos x}$.", expr(sp.cos(x)), r"$\frac{\cos^2 x}{\cos x} = \cos x$.", work="1cm"),
    Item(r"Simplify $(1 + \tan^2 x)\cos^2 x$.", num(1), r"$\sec^2 x\cos^2 x = 1$.", work="1cm"),
    Item(r"Simplify $\cos(-x)\sec x$.", num(1), r"$\cos(-x) = \cos x$.", work="1cm"),
    Item(r"Find the exact value of $\sin\frac{\pi}{12}$.", num((sp.sqrt(6) - r2) / 4, display=r"\frac{\sqrt6 - \sqrt2}{4}"),
         r"$\sin\left(\frac{\pi}{3} - \frac{\pi}{4}\right) = \frac{\sqrt3}{2}\cdot\frac{\sqrt2}{2} - \frac12\cdot\frac{\sqrt2}{2}$.", work="1.6cm"),
    Item(r"Find the exact value of $\cos\frac{7\pi}{12}$.", num((r2 - sp.sqrt(6)) / 4, display=r"\frac{\sqrt2 - \sqrt6}{4}"),
         r"$\cos\left(\frac{\pi}{3} + \frac{\pi}{4}\right) = \frac12\cdot\frac{\sqrt2}{2} - \frac{\sqrt3}{2}\cdot\frac{\sqrt2}{2}$.", work="1.6cm"),
    Item(r"$\cos x = \frac{5}{13}$ and $x$ is in quadrant I. Find $\sin 2x$.", num(sp.Rational(120, 169), display=r"\frac{120}{169}"), r"$\sin x = \frac{12}{13}$; $2 \cdot \frac{12}{13}\cdot\frac{5}{13}$.", work="1.4cm"),
    Item(r"$\cos x = -\frac{1}{3}$. Find $\cos 2x$.", num(-sp.Rational(7, 9), display=r"-\frac79"), r"$2\cos^2 x - 1 = \frac29 - 1$.", work="1.2cm"),
    Item(r"Write $\cos^2(3x)$ without a square.", expr((1 + sp.cos(6 * x)) / 2), r"$\frac{1 + \cos 6x}{2}$.", work="1cm"),
    MCQ(r"Which is an identity?", [r"$\sin 2x = 2\sin x$", r"$\cos(x + y) = \cos x + \cos y$", r"$\sin^2 x = 1 - \cos^2 x$", r"$\tan^2 x = \sec^2 x + 1$"], "C",
        r"From $\sin^2 x + \cos^2 x = 1$.", {"D": r"$\tan^2 x = \sec^2 x - 1$", "A": r"try $x = \frac{\pi}{2}$: $0 \ne 2$"}),
    Item(r"Show that $\dfrac{\cos x}{1 - \sin x} = \dfrac{1 + \sin x}{\cos x}$.", selfcheck(r"\text{multiply by } \tfrac{1 + \sin x}{1 + \sin x}"),
         r"$\frac{\cos x(1 + \sin x)}{1 - \sin^2 x} = \frac{\cos x(1 + \sin x)}{\cos^2 x} = \frac{1 + \sin x}{\cos x}$.", work="2.4cm"),
]
same("p", [sp.sin(pi / 12), sp.cos(7 * pi / 12), 2 * sp.Rational(12, 13) * sp.Rational(5, 13), 2 * sp.Rational(1, 9) - 1], [(sp.sqrt(6) - r2) / 4, (r2 - sp.sqrt(6)) / 4, sp.Rational(120, 169), -sp.Rational(7, 9)])
ident("p12", sp.cos(x) / (1 - sp.sin(x)), (1 + sp.sin(x)) / sp.cos(x))

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Simplify $\tan x\cos x$.", expr(sp.sin(x)), r"$\frac{\sin x}{\cos x}\cos x$.", work="1cm"),
        Item(r"Simplify $\cot x\sec x$.", expr(1 / sp.sin(x), display=r"\csc x"), r"$\frac{\cos x}{\sin x}\cdot\frac{1}{\cos x} = \csc x$.", work="1cm"),
        Item(r"Simplify $\csc x\tan x$.", expr(1 / sp.cos(x), display=r"\sec x"), r"$\frac{1}{\sin x}\cdot\frac{\sin x}{\cos x} = \sec x$.", work="1cm"),
    ),
    Variants(
        Item(r"Simplify $\csc^2 x - \cot^2 x$.", num(1), r"$1 + \cot^2 x = \csc^2 x$.", work="1cm"),
        Item(r"Simplify $\dfrac{1 - \cos^2 x}{\sin x}$.", expr(sp.sin(x)), r"$\frac{\sin^2 x}{\sin x}$.", work="1cm"),
        Item(r"Simplify $\dfrac{\sec^2 x - 1}{\tan x}$.", expr(sp.tan(x)), r"$\frac{\tan^2 x}{\tan x}$.", work="1cm"),
    ),
    Variants(
        Item(r"Find the exact value of $\cos\frac{5\pi}{12}$.", num((sp.sqrt(6) - r2) / 4, display=r"\frac{\sqrt6 - \sqrt2}{4}"), r"$\cos\left(\frac{\pi}{4} + \frac{\pi}{6}\right)$.", work="1.6cm"),
        Item(r"Find the exact value of $\sin\frac{5\pi}{12}$.", num((sp.sqrt(6) + r2) / 4, display=r"\frac{\sqrt6 + \sqrt2}{4}"), r"$\sin\left(\frac{\pi}{4} + \frac{\pi}{6}\right)$.", work="1.6cm"),
    ),
    Variants(
        Item(r"$\sin x = \frac45$ and $x$ is in quadrant II. Find $\sin 2x$.", num(-sp.Rational(24, 25), display=r"-\frac{24}{25}"), r"$\cos x = -\frac35$; $2\cdot\frac45\cdot\left(-\frac35\right)$.", work="1.4cm"),
        Item(r"$\sin x = \frac{1}{4}$. Find $\cos 2x$.", num(sp.Rational(7, 8), display=r"\frac78"), r"$1 - 2\cdot\frac{1}{16}$.", work="1.2cm"),
        Item(r"$\cos x = \frac{3}{5}$ and $x$ is in quadrant IV. Find $\sin 2x$.", num(-sp.Rational(24, 25), display=r"-\frac{24}{25}"), r"$\sin x = -\frac45$; $2\cdot\left(-\frac45\right)\cdot\frac35$.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"$\sin^2 x = $", [r"$\frac{1 + \cos 2x}{2}$", r"$\frac{1 - \cos 2x}{2}$", r"$1 - \cos 2x$", r"$\frac{1 - \cos x}{2}$"], "B", r"Solve $\cos 2x = 1 - 2\sin^2 x$ for $\sin^2 x$.", {"A": r"that is $\cos^2 x$"}),
        MCQ(r"$\cos^2 x = $", [r"$\frac{1 - \cos 2x}{2}$", r"$1 + \cos 2x$", r"$\frac{1 + \cos 2x}{2}$", r"$\frac{1 + \cos x}{2}$"], "C", r"Solve $\cos 2x = 2\cos^2 x - 1$ for $\cos^2 x$.", {"A": r"that is $\sin^2 x$"}),
    ),
]
same("q", [sp.cos(5 * pi / 12), sp.sin(5 * pi / 12)], [(sp.sqrt(6) - r2) / 4, (sp.sqrt(6) + r2) / 4])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$\dfrac{\sin x}{1 + \cos x} + \dfrac{1 + \cos x}{\sin x} = $", [r"$2\csc x$", r"$2\sec x$", r"$1$", r"$2\sin x$"], "A",
        r"Common denominator: $\frac{\sin^2 x + 1 + 2\cos x + \cos^2 x}{\sin x(1 + \cos x)} = \frac{2(1 + \cos x)}{\sin x(1 + \cos x)} = \frac{2}{\sin x}$."),
    MCQ(r"$\cos^4 x - \sin^4 x = $", [r"$1$", r"$\cos 2x$", r"$\sin 2x$", r"$\cos^2 x$"], "B", r"$(\cos^2 x - \sin^2 x)(\cos^2 x + \sin^2 x) = \cos 2x \cdot 1$.", {"A": "that drops the first factor"}),
    MCQ(r"If $\tan x = \frac34$ and $x$ is in quadrant III, then $\sin 2x = $", [r"$-\frac{24}{25}$", r"$\frac{7}{25}$", r"$\frac{12}{25}$", r"$\frac{24}{25}$"], "D",
        r"$\sin x = -\frac35$, $\cos x = -\frac45$; $2\left(-\frac35\right)\left(-\frac45\right) = \frac{24}{25}$.", {"A": "both sine and cosine are negative, so the product is positive", "B": r"that is $\cos 2x$"}),
    MCQ(r"Which expression equals $\sin\left(x + \frac{\pi}{2}\right)$?", [r"$\sin x$", r"$-\sin x$", r"$\cos x$", r"$-\cos x$"], "C",
        r"$\sin x\cos\frac{\pi}{2} + \cos x\sin\frac{\pi}{2} = \cos x$.", {"A": r"$\sin\left(x + \frac{\pi}{2}\right) \ne \sin x + \sin\frac{\pi}{2}$ either"}),
]
ident("m1", sp.sin(x) / (1 + sp.cos(x)) + (1 + sp.cos(x)) / sp.sin(x), 2 / sp.sin(x))
ident("m2", sp.cos(x)**4 - sp.sin(x)**4, sp.cos(2 * x))
same("m3", [2 * (-sp.Rational(3, 5)) * (-sp.Rational(4, 5))], [sp.Rational(24, 25)])
ident("m4", sp.sin(x + pi / 2), sp.cos(x))

FRQS = []

TOPIC = Topic(
    number="0.5", title="Trigonometric Identities",
    unit="Trig Review (a free module)", ced=["Prerequisite: trigonometric identities"],
    goals=r"Use the Pythagorean, symmetry, sum, double-angle and power-reducing identities to simplify expressions and find exact values.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
