"""Topic 6.7: The Fundamental Theorem of Calculus and definite integrals.

CED: FUN-6.A (FUN-6.A.1, FUN-6.A.2) with net change: if F' = f, then integral_a^b f(x) dx = F(b) - F(a) (FTC part
2), proved from part 1 (F = A + C); antiderivatives by reversing derivative rules; the integral of a rate of change is
the net change, f(b) = f(a) + integral_a^b f'(x) dx. Worked examples: sin x on [0, pi], sqrt(x) on [1, 9], a plant's
height from its growth rate.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Table, Text, Topic, Variants, Video, num, same,
                     selfcheck)

x, t = sp.symbols("x t", real=True)
I = lambda f, a, b, v=x: sp.simplify(sp.integrate(f, (v, a, b)))

same("lesson", [I(x**2, 0, 3), I(3 * x**2 - 2 * x, 1, 4), I(sp.sin(x), 0, sp.pi), I(sp.sqrt(x), 1, 9), 10 + I(6 * t - 2, 1, 3, t)], [9, 48, 2, sp.Rational(52, 3), 30])

NOTES = [
    Video("s6_7.py::Lesson", "Evaluating integrals", 6),

    Section("The Fundamental Theorem, part 2"),
    Formula("FTC, part 2", (
        r"If $F$ is an \blank{antiderivative} of $f$ ($F' = f$) on $[a, b]$, then \[ \int_a^b f(x)\,dx = F(b) - F(a) = F(x)\Big|_a^b. \]")),
    Text(r"\textbf{Why.} $A(x) = \int_a^x f(t)\,dt$ has $A' = f$, so any antiderivative is $F = A + C$. Then $F(b) - F(a) = A(b) - A(a) = A(b) - 0$: the $C$'s cancel."),
    Table(r"$x^n$ ($n \ne -1$) & $\dfrac{x^{n+1}}{n + 1}$ \\ "
          r"$\cos x$ & $\sin x$ \\ "
          r"$\sin x$ & $\blank{-\cos x}$ \\ "
          r"$e^x$ & $e^x$ \\ "
          r"$\dfrac1x$ & $\ln|x|$ \\ "
          r"$\sec^2 x$ & $\tan x$", "ll", header=r"$f(x)$ & an antiderivative $F(x)$"),
    VideoExample('Evaluating an integral', work="2.6cm"),

    Section("Net change"),
    Formula("Net change", (
        r"\[ \int_a^b f'(x)\,dx = f(b) - f(a), \qquad f(b) = f(a) + \int_a^b f'(x)\,dx. \] "
        r"The integral of a rate of change is the \blank{net change} in the amount: where it ends equals where it starts plus how much it changed.")),
    BigIdea(r"To evaluate $\int_a^b f(x)\,dx$, find an antiderivative, evaluate at the top and the bottom, and subtract."),
    Check(r"Evaluate $\displaystyle\int_0^2 x^3\,dx$.", num(4), r"$\left[\frac{x^4}{4}\right]_0^2 = 4 - 0 = 4$."),
]

# ---------------------------------------------------------------- practice
P = [(4 * x**3, 0, 2), (x**2 + 1, -1, 2), (6 * x - x**2, 0, 3), (1 / x**2, 1, 4), (sp.cos(x), 0, sp.pi / 2), (sp.exp(x), 0, sp.log(3)),
     (1 / x, 1, sp.E**2), (sp.sec(x)**2, 0, sp.pi / 4), (sp.sqrt(x) + 1, 0, 4), (x**3 - 2 * x, -1, 1)]
PRACTICE = []
for f, a, b in P:
    F = sp.integrate(f, x)
    PRACTICE.append(Item(rf"Evaluate $\displaystyle\int_{{{sp.latex(a)}}}^{{{sp.latex(b)}}} {sp.latex(f)}\,dx$.", num(I(f, a, b)),
                         rf"$\left[{sp.latex(F)}\right]_{{{sp.latex(a)}}}^{{{sp.latex(b)}}} = {sp.latex(I(f, a, b))}$.", work="2cm"))
PRACTICE += [
    Item(r"$f(2) = 5$ and $f'(x) = 3x^2$. Find $f(4)$.", num(5 + I(3 * x**2, 2, 4)), r"$f(4) = 5 + \left[x^3\right]_2^4 = 5 + 56 = 61$.", work="1.6cm"),
    Item(r"Water flows into a tank at $r(t) = 4 + 2t$ liters per minute. The tank holds $30$ liters at $t = 0$. How much does it hold at $t = 5$?", num(30 + I(4 + 2 * t, 0, 5, t)),
         r"$30 + \left[4t + t^2\right]_0^5 = 30 + 45 = 75$ liters.", work="1.6cm"),
    Item(r"A particle's velocity is $v(t) = 3t^2 - 12$ m/s, and it is at $x = 4$ at $t = 0$. Where is it at $t = 3$?", num(4 + I(3 * t**2 - 12, 0, 3, t)),
         r"$4 + \left[t^3 - 12t\right]_0^3 = 4 + (27 - 36) = -5$.", work="1.6cm"),
]
same("p net", [5 + I(3 * x**2, 2, 4), 30 + I(4 + 2 * t, 0, 5, t), 4 + I(3 * t**2 - 12, 0, 3, t)], [61, 75, -5])

# ---------------------------------------------------------------- quiz
def q(f, a, b):
    return Item(rf"Evaluate $\displaystyle\int_{{{sp.latex(a)}}}^{{{sp.latex(b)}}} {sp.latex(f)}\,dx$.", num(I(f, a, b)),
                rf"$\left[{sp.latex(sp.integrate(f, x))}\right]_{{{sp.latex(a)}}}^{{{sp.latex(b)}}} = {sp.latex(I(f, a, b))}$.", work="1.6cm")


QUIZ = [
    Variants(q(2 * x, 1, 4), q(3 * x**2, 0, 2), q(4 * x**3, 1, 2)),
    Variants(q(x**2 - 4 * x, 0, 3), q(x**3 + x, 0, 2), q(6 - 2 * x, 1, 3)),
    Variants(q(sp.cos(x), 0, sp.pi), q(sp.sin(x), 0, sp.pi / 2), q(sp.sec(x)**2, 0, sp.pi / 4)),
    Variants(q(sp.exp(x), 0, 1), q(1 / x, 1, sp.E), q(sp.sqrt(x), 0, 4)),
    Variants(
        Item(r"$g(1) = 3$ and $g'(x) = 2x + 1$. Find $g(3)$.", num(3 + I(2 * x + 1, 1, 3)), r"$3 + [x^2 + x]_1^3 = 3 + 10 = 13$.", work="1.2cm"),
        Item(r"$g(0) = -2$ and $g'(x) = e^x$. Find $g(\ln 4)$.", num(-2 + I(sp.exp(x), 0, sp.log(4))), r"$-2 + [e^x]_0^{\ln 4} = -2 + 3 = 1$.", work="1.2cm"),
        Item(r"$g(2) = 7$ and $g'(x) = 6x^2$. Find $g(1)$.", num(7 + I(6 * x**2, 2, 1)), r"$7 + [2x^3]_2^1 = 7 - 14 = -7$.", work="1.2cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$\displaystyle\int_1^2 \left(x^2 - \frac{1}{x^2}\right) dx = $", [r"$\frac{11}{6}$", r"$\frac73$", r"$\frac{17}{6}$", r"$\frac{5}{6}$"], "A",
        r"$\left[\frac{x^3}{3} + \frac1x\right]_1^2 = \left(\frac83 + \frac12\right) - \left(\frac13 + 1\right) = \frac{11}{6}$."),
    MCQ(r"$\displaystyle\int_0^{\pi/3} \cos x\,dx = $", [r"$\frac12$", r"$-\frac{\sqrt3}{2}$", r"$\frac{\sqrt3}{2}$", r"$1 - \frac{\sqrt3}{2}$"], "C", r"$\sin\frac\pi3 - \sin 0 = \frac{\sqrt3}{2}$."),
    MCQ(r"$f(1) = 4$ and $f'(x) = \frac{2}{x}$ for $x > 0$. Then $f(e^3) = $", [r"$6$", r"$10$", r"$4 + \frac{2}{e^3}$", r"$7$"], "B", r"$4 + [2\ln x]_1^{e^3} = 4 + 6 = 10$."),
    MCQ(r"If $\int_0^k (2x - 3)\,dx = 4$ and $k > 0$, then $k = $", [r"$1$", r"$2$", r"$3$", r"$4$"], "D", r"$k^2 - 3k = 4$, so $(k - 4)(k + 1) = 0$ and $k = 4$."),
]
same("m", [I(x**2 - 1 / x**2, 1, 2), I(sp.cos(x), 0, sp.pi / 3), 4 + I(2 / x, 1, sp.exp(3)), I(2 * x - 3, 0, 4)], [sp.Rational(11, 6), sp.sqrt(3) / 2, 10, 4])

R = 6 * t - t**2
A = lambda v: 50 + I(R, 0, v, t)
same("frq", [A(6), A(8), R.subs(t, 7)], [86, sp.Rational(214, 3), -7])
FRQS = [
    FRQ("Water in a tank", (
        r"The amount of water in a tank is $50$ liters at time $t = 0$. For $0 \le t \le 8$, water flows into or out of the tank at the rate "
        r"$R(t) = 6t - t^2$ liters per hour, where positive values mean water is flowing in."), [
        Part("a", r"How many liters of water are in the tank at time $t = 6$? Show the work that leads to your answer.", num(86),
             r"$50 + \int_0^6 (6t - t^2)\,dt = 50 + \left[3t^2 - \frac{t^3}{3}\right]_0^6 = 50 + (108 - 72) = 86$ liters.",
             [(1, "integral"), (1, "antiderivative"), (1, "answer")], work="2.6cm"),
        Part("b", r"Is the amount of water in the tank increasing or decreasing at time $t = 7$? Give a reason for your answer.", selfcheck(r"\text{decreasing}"),
             r"$R(7) = 42 - 49 = -7 < 0$, so the amount of water is decreasing at $t = 7$.", [(1, "decreasing with reason")], work="1.6cm"),
        Part("c", r"At what time $t$, for $0 \le t \le 8$, is the amount of water in the tank greatest? Justify your answer.", num(6),
             r"$R(t) = t(6 - t) = 0$ at $t = 0$ and $t = 6$. Candidates: $A(0) = 50$, $A(6) = 86$, $A(8) = 50 + \left[3t^2 - \frac{t^3}{3}\right]_0^8 = \frac{214}{3} \approx 71.3$. "
             r"The amount is greatest at $t = 6$ hours.", [(1, "considers $t = 6$ and the endpoints"), (1, "answer with justification")], work="2.6cm"),
    ], frq_type="Rate in context"),
]

TOPIC = Topic(
    number="6.7", title="The Fundamental Theorem of Calculus and Definite Integrals",
    unit="Unit 6: Integration and Accumulation of Change", ced=["FUN-6.A", "FUN-6.A.1", "FUN-6.A.2"],
    goals=r"Evaluate definite integrals with antiderivatives (the Fundamental Theorem of Calculus) and use integrals of rates to find net change.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
