"""Topic 4.7: Using L'Hospital's Rule for determining limits of indeterminate forms.

CED: LIM-4.A (LIM-4.A.1, LIM-4.A.2): when a limit of f/g has the form 0/0 or inf/inf, it equals the limit of f'/g' (if
that exists). Why it works at 0/0 comes from 4.6: near a, f and g are both close to their tangent lines through (a, 0),
so their ratio is close to the ratio of the slopes. Worked examples: sin(3x)/x, ln(x)/x at infinity, (e^x - 1 - x)/x^2
(twice). AP requires showing the form is indeterminate before using the rule.
"""
import sympy as sp

from calclib import (FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Text, Topic, Variants, Video, expr, num,
                     same, selfcheck)

x = sp.symbols("x")
oo = sp.oo

same("sin3x", sp.limit(sp.sin(3 * x) / x, x, 0), 3)
same("lnx", sp.limit(sp.log(x) / x, x, oo), 0)
same("twice", sp.limit((sp.exp(x) - 1 - x) / x**2, x, 0), sp.Rational(1, 2))

NOTES = [
    Video("s4_7.py::Lesson", "L'Hospital's Rule", 4),

    Section("Indeterminate forms"),
    Text(r"In Unit 1, a limit that came out as $\frac00$ needed algebra: factor, use a conjugate, or use a known limit. "
         r"$\frac00$ and $\frac{\infty}{\infty}$ are called \blank{indeterminate} forms: the form alone doesn't tell you the limit."),
    Formula("L'Hospital's Rule", (
        r"If \[ \lim_{x \to a} f(x) = 0 \text{ and } \lim_{x \to a} g(x) = 0, \] or both limits are infinite, then \[ \lim_{x \to a} \frac{f(x)}{g(x)} = "
        r"\lim_{x \to a} \frac{\blank{f'(x)}}{\blank{g'(x)}}, \] provided the limit on the right exists. The same holds for $x \to \infty$.")),
    Text(r"\textbf{Not the quotient rule.} Differentiate the top and the bottom \emph{separately}."),

    Section("Why it works"),
    Text(r"At a $\frac00$ form, both $f$ and $g$ pass through height $0$ at $x = a$. Near $a$, each is close to its tangent line (Topic 4.6): "
         r"\[ f(x) \approx f'(a)(x - a), \qquad g(x) \approx g'(a)(x - a). \] The factors $x - a$ cancel, so \[ \frac{f(x)}{g(x)} \approx \frac{f'(a)}{g'(a)}. \]"),

    Section("Using it on the AP exam"),
    Text(r"\textbf{Show the form first.} Write the limits of the top and the bottom separately and state that the form is $\frac00$ or "
         r"$\frac{\infty}{\infty}$. The AP exam awards a point for that check, and the rule gives wrong answers when it is skipped."),
    Example("Check before you use it", r"Find \[ \lim_{x \to 1} \frac{x^2 + 1}{x + 1}. \]",
            r"Plug in: $\frac{2}{2} = 1$. This is not an indeterminate form, so the limit is $1$. (Using the rule here would give $\frac{2x}{1} \to 2$: wrong.)", work="2cm", beat="Check the form first"),
    Text(r"If the new limit is still $\frac00$ or $\frac{\infty}{\infty}$, you may use the rule \blank{again}."),
    BigIdea(r"At $\frac00$ or $\frac{\infty}{\infty}$, the limit of a ratio equals the limit of the ratio of the derivatives. Check the form first, every time."),
    Check(r"Find \[ \lim_{x \to 0} \frac{\tan x}{x}. \]", num(1), r"$\frac00$; the rule gives \[ \lim_{x \to 0} \frac{\sec^2 x}{1} = 1. \]"),
]

# ---------------------------------------------------------------- practice
P = [
    (r"\lim_{x \to 0} \frac{\sin(5x)}{x}", sp.sin(5 * x) / x, 0, r"\frac00;\ \ \lim_{x \to 0} \frac{5\cos(5x)}{1} = 5"),
    (r"\lim_{x \to 2} \frac{x^3 - 8}{x - 2}", (x**3 - 8) / (x - 2), 2, r"\frac00;\ \ \lim_{x \to 2} \frac{3x^2}{1} = 12"),
    (r"\lim_{x \to 0} \frac{e^{2x} - 1}{x}", (sp.exp(2 * x) - 1) / x, 0, r"\frac00;\ \ \lim_{x \to 0} \frac{2e^{2x}}{1} = 2"),
    (r"\lim_{x \to 1} \frac{\ln x}{x - 1}", sp.log(x) / (x - 1), 1, r"\frac00;\ \ \lim_{x \to 1} \frac{1/x}{1} = 1"),
    (r"\lim_{x \to 0} \frac{1 - \cos x}{x^2}", (1 - sp.cos(x)) / x**2, 0, r"\frac00 \to \lim_{x \to 0} \frac{\sin x}{2x},\ \text{still } \frac00 \to \lim_{x \to 0} \frac{\cos x}{2} = \frac12"),
    (r"\lim_{x \to \infty} \frac{x^2}{e^x}", x**2 / sp.exp(x), oo, r"\frac{\infty}{\infty} \to \lim_{x \to \infty} \frac{2x}{e^x} \to \lim_{x \to \infty} \frac{2}{e^x} = 0"),
    (r"\lim_{x \to \infty} \frac{5x^2 - 3}{2x^2 + x}", (5 * x**2 - 3) / (2 * x**2 + x), oo, r"\frac{\infty}{\infty} \to \lim_{x \to \infty} \frac{10x}{4x + 1} \to \lim_{x \to \infty} \frac{10}{4} = \frac52"),
    (r"\lim_{x \to \infty} \frac{\ln x}{\sqrt x}", sp.log(x) / sp.sqrt(x), oo, r"\frac{\infty}{\infty} \to \lim_{x \to \infty} \frac{1/x}{1/(2\sqrt x)} = \lim_{x \to \infty} \frac{2}{\sqrt x} = 0"),
    (r"\lim_{x \to 0} \frac{x}{\arctan x}", x / sp.atan(x), 0, r"\frac00;\ \ \lim_{x \to 0} \frac{1}{1/(1 + x^2)} = 1"),
    (r"\lim_{x \to \pi} \frac{\sin x}{x - \pi}", sp.sin(x) / (x - sp.pi), sp.pi, r"\frac00;\ \ \lim_{x \to \pi} \frac{\cos x}{1} = -1"),
    (r"\lim_{x \to 0} \frac{x^2 + 3x}{x + 4}", (x**2 + 3 * x) / (x + 4), 0, r"\text{Not indeterminate: plug in, } \frac04 = 0"),
]
PRACTICE = [Item(rf"Find \[ {tex}. \]", num(sp.limit(f, x, a)), rf"\[ {sol} \]", work="2.2cm") for tex, f, a, sol in P]
PRACTICE += [
    Item(r"Ifeoma writes \[ \lim_{x \to 0} \frac{\cos x}{x + 1} = \lim_{x \to 0} \frac{-\sin x}{1} = 0. \] What went wrong, and what is the limit?", num(1),
         r"The form is $\frac11$, not indeterminate, so the rule doesn't apply. Plugging in gives $1$.", work="2cm"),
    Item(r"$f(3) = g(3) = 0$, $f'(3) = 4$ and $g'(3) = -2$, with $f'$ and $g'$ continuous. Find \[ \lim_{x \to 3} \frac{f(x)}{g(x)}. \]", num(-2),
         r"$\frac00$, so the limit is $\frac{f'(3)}{g'(3)} = \frac{4}{-2} = -2$.", work="1.8cm"),
]
same("p", [sp.limit(f, x, a) for _, f, a, _ in P], [5, 12, 2, 1, sp.Rational(1, 2), 0, sp.Rational(5, 2), 0, 1, -1, 0])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find \[ \lim_{x \to 0} \frac{\sin(4x)}{x}. \]", num(4), r"$\frac00$; \[ \lim_{x \to 0} \frac{4\cos(4x)}{1} = 4. \]", work="1.8cm"),
        Item(r"Find \[ \lim_{x \to 0} \frac{\sin(7x)}{x}. \]", num(7), r"$\frac00$; \[ \lim_{x \to 0} \frac{7\cos(7x)}{1} = 7. \]", work="1.8cm"),
        Item(r"Find \[ \lim_{x \to 0} \frac{\sin(2x)}{3x}. \]", num(sp.Rational(2, 3)), r"$\frac00$; \[ \lim_{x \to 0} \frac{2\cos(2x)}{3} = \frac23. \]", work="1.8cm"),
    ),
    Variants(
        Item(r"Find \[ \lim_{x \to 0} \frac{e^{3x} - 1}{x}. \]", num(3), r"$\frac00$; \[ \lim_{x \to 0} \frac{3e^{3x}}{1} = 3. \]", work="1.8cm"),
        Item(r"Find \[ \lim_{x \to 0} \frac{e^{x} - 1}{4x}. \]", num(sp.Rational(1, 4)), r"$\frac00$; \[ \lim_{x \to 0} \frac{e^{x}}{4} = \frac14. \]", work="1.8cm"),
        Item(r"Find \[ \lim_{x \to 0} \frac{1 - e^{x}}{2x}. \]", num(sp.Rational(-1, 2)), r"$\frac00$; \[ \lim_{x \to 0} \frac{-e^{x}}{2} = -\frac12. \]", work="1.8cm"),
    ),
    Variants(
        Item(r"Find \[ \lim_{x \to \infty} \frac{x}{e^{x}}. \]", num(0), r"$\frac{\infty}{\infty}$; \[ \lim_{x \to \infty} \frac{1}{e^{x}} = 0. \]", work="1.8cm"),
        Item(r"Find \[ \lim_{x \to \infty} \frac{\ln x}{x^2}. \]", num(0), r"$\frac{\infty}{\infty}$; \[ \lim_{x \to \infty} \frac{1/x}{2x} = \lim_{x \to \infty} \frac{1}{2x^2} = 0. \]", work="1.8cm"),
        Item(r"Find \[ \lim_{x \to \infty} \frac{3x + \ln x}{x}. \]", num(3), r"$\frac{\infty}{\infty}$; \[ \lim_{x \to \infty} \frac{3 + 1/x}{1} = 3. \]", work="1.8cm"),
    ),
    Variants(
        MCQ(r"For which limit can L'Hospital's Rule be used directly?", [r"$\displaystyle\lim_{x \to 0} \frac{x + 1}{x + 2}$", r"$\displaystyle\lim_{x \to 0} \frac{x^2}{\sin x}$",
            r"$\displaystyle\lim_{x \to 0} \frac{\cos x}{x}$", r"$\displaystyle\lim_{x \to 1} \frac{x}{\ln x + 1}$"], "B", r"Only B has the form $\frac00$."),
        MCQ(r"For which limit can L'Hospital's Rule be used directly?", [r"$\displaystyle\lim_{x \to 2} \frac{x^2 - 4}{x - 2}$", r"$\displaystyle\lim_{x \to 2} \frac{x^2 + 4}{x - 2}$",
            r"$\displaystyle\lim_{x \to 0} \frac{e^x}{x + 1}$", r"$\displaystyle\lim_{x \to 0} \frac{\cos x}{1 - x}$"], "A", r"Only A has the form $\frac00$."),
        MCQ(r"For which limit can L'Hospital's Rule be used directly?", [r"$\displaystyle\lim_{x \to 0} \frac{x}{e^x}$", r"$\displaystyle\lim_{x \to \infty} \frac{1}{\ln x}$",
            r"$\displaystyle\lim_{x \to 0} \frac{\sin x}{x + 1}$", r"$\displaystyle\lim_{x \to \infty} \frac{x^3}{e^x}$"], "D", r"Only D has an indeterminate form, $\frac{\infty}{\infty}$."),
    ),
    Variants(
        Item(r"$f(1) = 0$, $g(1) = 0$, $f'(1) = 6$ and $g'(1) = 3$, with $f'$ and $g'$ continuous. Find \[ \lim_{x \to 1} \frac{f(x)}{g(x)}. \]", num(2), r"$\frac00$: $\frac63 = 2$.", work="1.4cm"),
        Item(r"$f(0) = 0$, $g(0) = 0$, $f'(0) = -5$ and $g'(0) = 2$, with $f'$ and $g'$ continuous. Find \[ \lim_{x \to 0} \frac{f(x)}{g(x)}. \]", num(sp.Rational(-5, 2)), r"$\frac00$: $\frac{-5}{2}$.", work="1.4cm"),
        Item(r"$f(4) = 0$, $g(4) = 0$, $f'(4) = 1$ and $g'(4) = 8$, with $f'$ and $g'$ continuous. Find \[ \lim_{x \to 4} \frac{f(x)}{g(x)}. \]", num(sp.Rational(1, 8)), r"$\frac00$: $\frac18$.", work="1.4cm"),
    ),
]
same("q", [sp.limit(sp.sin(2 * x) / (3 * x), x, 0), sp.limit((1 - sp.exp(x)) / (2 * x), x, 0), sp.limit(sp.log(x) / x**2, x, oo), sp.limit((3 * x + sp.log(x)) / x, x, oo)],
     [sp.Rational(2, 3), sp.Rational(-1, 2), 0, 3])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"\[ \lim_{x \to 0} \frac{e^{x} - \cos x}{x} = \]", [r"$0$", r"$1$", r"$2$", r"Does not exist"], "B",
        r"$\frac00$; \[ \lim_{x \to 0} \frac{e^x + \sin x}{1} = 1. \]"),
    MCQ(r"\[ \lim_{x \to 0} \frac{x - \sin x}{x^3} = \]", [r"$0$", r"$1$", r"$\frac13$", r"$\frac16$"], "D",
        r"Three uses of the rule: $\frac{1 - \cos x}{3x^2} \to \frac{\sin x}{6x} \to \frac{\cos x}{6} \to \frac16$."),
    MCQ(r"$f$ and $g$ are differentiable with $f(2) = g(2) = 0$, $f'(2) = 3$ and $g'(2) = 4$. What is \[ \lim_{x \to 2} \frac{f(x)}{g(x)}? \]",
        [r"$\frac34$", r"$\frac43$", r"$0$", r"Does not exist"], "A", r"$\frac00$, so the limit is $\frac{f'(2)}{g'(2)} = \frac34$."),
    MCQ(r"\[ \lim_{x \to \infty} \frac{4x^3 + x}{e^{x/2}} = \]", [r"$8$", r"$\infty$", r"$0$", r"$4$"], "C",
        r"$\frac{\infty}{\infty}$ three times; the exponential always wins: $0$."),
]
same("m", [sp.limit((sp.exp(x) - sp.cos(x)) / x, x, 0), sp.limit((x - sp.sin(x)) / x**3, x, 0), sp.limit((4 * x**3 + x) / sp.exp(x / 2), x, oo)], [1, sp.Rational(1, 6), 0])

FRQS = [
    FRQ("Limits from derivative values", (
        r"The function $f$ has a continuous second derivative for all real numbers and satisfies $f(2) = 3$, $f'(2) = 5$ and $f''(2) = -2$."), [
        Part("a", r"Find the value of $\displaystyle\lim_{x\to2}\frac{f(x) - 3}{x^2 - 4}$, or show that it does not exist. Justify your answer.",
             num(sp.Rational(5, 4)),
             r"$f$ is continuous, so $\displaystyle\lim_{x\to2}\big(f(x) - 3\big) = f(2) - 3 = 0$, and $\displaystyle\lim_{x\to2}(x^2 - 4) = 0$. "
             r"By L'Hospital's Rule, $\displaystyle\lim_{x\to2}\frac{f(x) - 3}{x^2 - 4} = \lim_{x\to2}\frac{f'(x)}{2x} = \frac{5}{4}$.",
             [(1, "shows both limits are $0$"), (1, "answer $\\frac54$ using L'Hospital's Rule")], work="2.8cm"),
        Part("b", r"Find the value of $\displaystyle\lim_{x\to2}\frac{f(x) - 3 - 5(x - 2)}{(x - 2)^2}$, or show that it does not exist. "
                  r"Justify your answer.", num(-1),
             r"Numerator and denominator both approach $0$. By L'Hospital's Rule the limit equals "
             r"$\displaystyle\lim_{x\to2}\frac{f'(x) - 5}{2(x - 2)}$. Since $f'$ is continuous, $f'(x) - 5 \to 0$; "
             r"this is again $\frac00$. Applying L'Hospital's Rule again: $\displaystyle\lim_{x\to2}\frac{f''(x)}{2} = \frac{-2}{2} = -1$.",
             [(1, "first application, with $\\frac00$ shown"), (1, "second application, with $\\frac00$ shown"), (1, "answer $-1$")],
             work="3.4cm"),
        Part("c", r"Let $k$ be a differentiable function. It is known that $\displaystyle\lim_{x\to1}\frac{k(x) - 6}{e^{x - 1} - 1} = 5$ "
                  r"and that this limit can be evaluated using L'Hospital's Rule. Find $k(1)$ and $k'(1)$. Show the work that leads to "
                  r"your answers.", selfcheck(r"k(1) = 6,\ k'(1) = 5"),
             r"L'Hospital's Rule applies only to an indeterminate form. The denominator approaches $e^0 - 1 = 0$, so the numerator must "
             r"also approach $0$: $k(1) - 6 = 0$ and $k(1) = 6$. Then the limit is $\dfrac{k'(1)}{e^{0}} = k'(1)$, so $k'(1) = 5$.",
             [(1, "$k(1) = 6$, because the numerator must approach $0$"), (1, "$k'(1) = 5$")], work="3cm"),
    ], frq_type="L'Hospital's Rule"),
]
# a concrete f with f(2) = 3, f'(2) = 5, f''(2) = -2 checks parts (a) and (b)
f7 = 3 + 5 * (x - 2) - (x - 2)**2 + (x - 2)**3
same("frq vals", [f7.subs(x, 2), sp.diff(f7, x).subs(x, 2), sp.diff(f7, x, 2).subs(x, 2)], [3, 5, -2])
same("frq a", sp.limit((f7 - 3) / (x**2 - 4), x, 2), sp.Rational(5, 4))
same("frq b", sp.limit((f7 - 3 - 5 * (x - 2)) / (x - 2)**2, x, 2), -1)
k7 = 6 + 5 * (x - 1) + 7 * (x - 1)**2
same("frq c", sp.limit((k7 - 6) / (sp.exp(x - 1) - 1), x, 1), 5)

TOPIC = Topic(
    number="4.7", title="Using L'Hospital's Rule for Determining Limits of Indeterminate Forms",
    unit="Unit 4: Contextual Applications of Differentiation", ced=["LIM-4.A", "LIM-4.A.1", "LIM-4.A.2"],
    goals=r"Recognize the indeterminate forms $\frac00$ and $\frac{\infty}{\infty}$, and use L'Hospital's Rule to find those limits.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
