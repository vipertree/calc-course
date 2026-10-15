"""Topic 6.7: The Fundamental Theorem of Calculus and definite integrals.

CED: FUN-6.A (FUN-6.A.1, FUN-6.A.2) with net change: if F' = f, then integral_a^b f(x) dx = F(b) - F(a) (FTC part
2); antiderivatives by reversing derivative rules; the integral of a rate of change is the net change,
f(b) = f(a) + integral_a^b f'(x) dx.
Adder's notes (2026-10-14): picks up from 6.4's big F (no A(x)); "what is F here, where does it start, where does it
end?" with a concrete integral beside the general notation; +C from plugging in constants (same derivative, C cancels);
the power rule reversed as two steps; the first example with F(4) and F(1) before the bracket notation.
Worked examples: sin x on [0, pi], sqrt(x) on [1, 9], a plant's height from its growth rate.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Table, Text, Topic, Variants, Video, num, same,
                     selfcheck)
from calclib.figs import graph

x, t = sp.symbols("x t", real=True)
I = lambda f, a, b, v=x: sp.simplify(sp.integrate(f, (v, a, b)))
tex = lambda e: sp.latex(e).replace(r"\log{\left(x \right)}", r"\ln|x|")

same("lesson", [I(x**2, 0, 3), I(3 * x**2 - 2 * x, 1, 4), I(sp.sin(x), 0, sp.pi), I(sp.sqrt(x), 1, 9), 10 + I(6 * t - 2, 1, 3, t)], [9, 48, 2, sp.Rational(52, 3), 30])
# the opening's Riemann-sum limit, and +C: F(3) - F(0) for F = x^3/3 + C is 9 for every C
n, k = sp.symbols("n k", positive=True, integer=True)
same("riemann", [sp.limit(sp.summation((3 * k / n)**2 * 3 / n, (k, 1, n)), n, sp.oo)], [9])
same("plus C", [(x**3 / 3 + c).subs(x, 3) - (x**3 / 3 + c).subs(x, 0) for c in (0, 2, -1, 5)], [9, 9, 9, 9])
same("power rule reversed", [sp.diff(x**3 / 3, x), sp.diff(x**5 / 5, x), sp.diff(x**3 - x**2, x), (x**3 - x**2).subs(x, 4), (x**3 - x**2).subs(x, 1)],
     [x**2, x**4, 3 * x**2 - 2 * x, 48, 0])

FIG_C = graph("t6_7_plusc", [("x^3/3", 0, 2.8), ("x^3/3+2", 0, 2.8), ("x^3/3-1", 0, 2.8), ("x^3/3+5", 0, 2.8)], xr=(0, 3.6), yr=(-2, 13), ystep=2,
              ylabel="F(x)", w="6cm", h="5.6cm",
              labels=[(2.8, 7.32, "right", "$C = 0$"), (2.8, 9.32, "right", "$C = 2$"), (2.8, 6.32, "right", "$C = -1$"), (2.8, 12.32, "right", "$C = 5$")],
              caption=r"$F(x) = \frac{x^3}{3} + C$ for four values of $C$: the same curve shifted up or down, so every one has derivative $x^2$.")

NOTES = [
    Video("s6_7.py::Lesson", "Evaluating integrals", 11),

    Section("How much F changes"),
    Text(r"In topic 6.4, big $F$ was the accumulation function $F(x) = \int_a^x f(t)\,dt$, and the Fundamental Theorem said $F'(x) = f(x)$: "
         r"each small change in $F$ is a thin sliver of area under $f$. Add up all the slivers from $a$ to $b$ and you get the area under $f$; "
         r"add up all the small changes in $F$ and you get $F$'s total change, where $F$ ends minus where $F$ starts."),
    Text(r"\textbf{The question to ask.} What is $F$ here? That is, what is the integrand the derivative of? Where does $F$ start, and where does it end?"),
    Table(r"integrand & $f(x)$ & $x^2$ \\ "
          r"$F$ & $F'(x) = f(x)$ & $F(x) = \blank{\dfrac{x^3}{3}}$ \\ "
          r"where $F$ starts & $F(a)$ & $F(0) = \blank{0}$ \\ "
          r"where $F$ ends & $F(b)$ & $F(3) = \blank{9}$ \\ "
          r"the integral & $\int_a^b f(x)\,dx = F(b) - F(a)$ & $\int_0^3 x^2\,dx = \blank{9}$", "lll", header=r" & In general & For $\int_0^3 x^2\,dx$"),

    Section(r"Where $+\,C$ comes from"),
    Text(r"The function $\frac{x^3}{3}$ isn't the only one with derivative $x^2$. Adding any constant shifts the graph up or down without changing its slope, "
         r"so $F(x) = \frac{x^3}{3} + C$ works for every $C$. The constant cancels when we subtract:"),
    FIG_C,
    Table(r"$0$ & $9$ & $0$ & $9$ \\ $2$ & $11$ & $2$ & $\blank{9}$ \\ $-1$ & $8$ & $-1$ & $\blank{9}$ \\ $5$ & $14$ & $5$ & $\blank{9}$", "cccc",
          header=r"$C$ & $F(3)$ & $F(0)$ & $F(3) - F(0)$"),
    Text(r"In general, $\left(F(b) + C\right) - \left(F(a) + C\right) = F(b) - F(a)$, so any $F$ with the right derivative gives the same answer."),

    Section("The Fundamental Theorem, part 2"),
    Formula("The Fundamental Theorem of Calculus, part 2", (
        r"For a continuous function $f$: \[ \text{If } F'(x) = f(x) \text{ on } [a, b], \ \text{ then } \ \int_a^b f(x)\,dx = \blank{F(b) - F(a)}. \] "
        r"In words: the area under $f$ from $a$ to $b$ is how much $F$ changes from $a$ to $b$.")),
    BigIdea(r"To evaluate $\int_a^b f(x)\,dx$, no limit of Riemann sums is needed: find an antiderivative $F$, evaluate it at the two endpoints, and subtract."),

    Section("Running derivative rules backward"),
    Text(r"\textbf{The power rule reversed.} The power rule has two steps: multiply by the power, then subtract 1 from the exponent ($x^3 \to 3x^2$). "
         r"Reverse them in reverse order: \blank{add 1 to the exponent}, then \blank{divide by the new exponent} ($x^2 \to x^3 \to \frac{x^3}{3}$). "
         r"So $x^n$ has antiderivative $\dfrac{x^{n+1}}{n + 1}$ for every $n \ne -1$. Check with the power rule: $\frac{d}{dx}\left(\frac{x^3}{3}\right) = x^2$."),
    Table(r"$x^n$ ($n \ne -1$) & $\dfrac{x^{n+1}}{n + 1}$ \\[6pt] "
          r"$\cos x$ & $\sin x$ \\[4pt] "
          r"$\sin x$ & $\blank{-\cos x}$ \\[4pt] "
          r"$e^x$ & $e^x$ \\[4pt] "
          r"$\dfrac1x$ & $\ln|x|$ \\[6pt] "
          r"$\sec^2 x$ & $\tan x$", "ll", header=r"$f(x)$ & an antiderivative $F(x)$"),
    Formula("Bracket notation", r"\[ \Big[F(x)\Big]_a^b = F(b) - F(a): \text{ the top value minus the bottom value.} \]"),
    VideoExample('Evaluating an integral', work="3.2cm"),

    Section("Net change"),
    Formula("Net change", (
        r"\[ \int_a^b f'(x)\,dx = f(b) - f(a), \qquad f(b) = f(a) + \int_a^b f'(x)\,dx. \] "
        r"The integral of a rate of change is the \blank{net change} in the amount: where it ends equals where it starts plus how much it changed.")),
    Check(r"Evaluate $\displaystyle\int_0^2 x^3\,dx$.", num(4), r"$F(x) = \frac{x^4}{4}$, so $\left[\frac{x^4}{4}\right]_0^2 = 4 - 0 = 4$."),
]

# ---------------------------------------------------------------- practice
P = [(4 * x**3, 0, 2), (x**2 + 1, -1, 2), (6 * x - x**2, 0, 3), (1 / x**2, 1, 4), (sp.cos(x), 0, sp.pi / 2), (sp.exp(x), 0, sp.log(3)),
     (1 / x, 1, sp.E**2), (sp.sec(x)**2, 0, sp.pi / 4), (sp.sqrt(x) + 1, 0, 4), (x**3 - 2 * x, -1, 1)]
PRACTICE = []
for f, a, b in P:
    F = sp.integrate(f, x)
    PRACTICE.append(Item(rf"Evaluate $\displaystyle\int_{{{sp.latex(a)}}}^{{{sp.latex(b)}}} {sp.latex(f)}\,dx$.", num(I(f, a, b)),
                         rf"$\left[{tex(F)}\right]_{{{sp.latex(a)}}}^{{{sp.latex(b)}}} = {sp.latex(I(f, a, b))}$.", work="2cm"))
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
                rf"$\left[{tex(sp.integrate(f, x))}\right]_{{{sp.latex(a)}}}^{{{sp.latex(b)}}} = {sp.latex(I(f, a, b))}$.", work="1.6cm")


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
