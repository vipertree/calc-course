"""Topic 5.5: Using the Candidates Test to determine absolute (global) extrema.

CED: FUN-4.A (FUN-4.A.3): for a continuous f on [a, b], the absolute extrema are among f at the critical points and at
the endpoints; evaluate them all and compare. Worked examples: x^3 - 3x + 1 on [0, 3], x - 2 ln x on [1, e^2],
sin x + cos x on [0, pi].
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num,
                     same, selfcheck)

x = sp.symbols("x", real=True)


def candidates(f, a, b):
    """{x: f(x)} at the endpoints and the critical points (f' = 0) inside (a, b)."""
    cs = [c for c in sp.solveset(sp.diff(f, x), x, sp.Interval.open(a, b))]
    return {c: sp.simplify(f.subs(x, c)) for c in sorted(set([a, b] + cs), key=float)}


def extremes(f, a, b):
    c = candidates(f, a, b)
    return max(c.values(), key=float), min(c.values(), key=float)


same("ex1", list(extremes(x**3 - 3 * x + 1, 0, 3)), [19, -1])
same("ex2", list(extremes(x - 2 * sp.log(x), 1, sp.E**2)), [sp.E**2 - 4, 2 - 2 * sp.log(2)])
same("ex3", list(extremes(sp.sin(x) + sp.cos(x), 0, sp.pi)), [sp.sqrt(2), -1])

NOTES = [
    Video("s5_5.py::Lesson", "The Candidates Test", 4),

    Section("Where an absolute extremum can be"),
    Text(r"On a closed interval $[a, b]$, a continuous function has an absolute max and min (the Extreme Value Theorem). Each one is either at a "
         r"\blank{critical point} inside the interval or at an \blank{endpoint}. So there's a short list of candidates."),
    Formula("The Candidates Test (closed interval method)", (
        r"To find the absolute extrema of a continuous $f$ on $[a, b]$: \par "
        r"\textbf{1.} Find the critical points of $f$ in $(a, b)$. \par "
        r"\textbf{2.} Evaluate $f$ at each critical point and at both \blank{endpoints}. \par "
        r"\textbf{3.} The largest value is the absolute \blank{maximum}; the smallest is the absolute \blank{minimum}.")),
    Text(r"The answer is a \emph{value} of $f$; say where it happens too. ``The absolute maximum is $19$, at $x = 3$.''"),
    Text(r"\textbf{Justification.} On the AP exam, show the table of candidates. That table \emph{is} the justification."),
    VideoExample('A parabola on an interval', work="3cm"),
    BigIdea(r"On a closed interval, test every candidate: the critical points and the endpoints. Biggest wins, smallest loses."),
    Check(r"Find the absolute maximum value of $f(x) = 3 - x^2$ on $[-1, 2]$.", num(3), r"Candidates $f(-1) = 2$, $f(0) = 3$, $f(2) = -1$: max $3$."),
]

# ---------------------------------------------------------------- practice
P = [
    (x**2 - 6 * x + 2, 0, 5, "minimum"),
    (x**3 - 12 * x, -3, 5, "maximum"),
    (x**3 - 12 * x, -3, 5, "minimum"),
    (2 * x**3 - 3 * x**2 - 12 * x + 1, -2, 3, "maximum"),
    (x**4 - 2 * x**2 + 3, -2, 1, "minimum"),
    (x * sp.exp(-x), 0, 3, "maximum"),
    (x + 4 / x, 1, 5, "minimum"),
    (sp.sin(x) - x / 2, 0, sp.pi, "maximum"),
]
PRACTICE = []
for f, a, b, ask in P:
    c = candidates(f, a, b)
    big, small = extremes(f, a, b)
    v = big if ask == "maximum" else small
    PRACTICE.append(Item(rf"Find the absolute {ask} value of $f(x) = {sp.latex(f)}$ on $\left[{sp.latex(a)}, {sp.latex(b)}\right]$.", num(v),
                         r"Candidates: " + ", ".join(rf"$f\left({sp.latex(k)}\right) = {sp.latex(val)}$" for k, val in c.items()) + rf". The absolute {ask} is ${sp.latex(v)}$.",
                         work="2.8cm"))
PRACTICE += [
    Item(r"Selected values of a differentiable $g$ on $[0, 6]$ are $g(0) = 5$, $g(6) = 2$. Its only critical points are $x = 2$, where $g(2) = 9$, and $x = 4$, where $g(4) = -1$. "
         r"Find the absolute minimum value of $g$ on $[0, 6]$.", num(-1), r"Candidates $5, 9, -1, 2$: the smallest is $-1$, at $x = 4$.", work="1.6cm"),
    Item(r"Amara says the absolute maximum of $f(x) = x^3 - 3x$ on $[0, 3]$ is $f(1) = -2$, since $1$ is the only critical point. What did she miss? Find the absolute maximum.",
         num(18), r"She skipped the endpoints. $f(0) = 0$, $f(1) = -2$, $f(3) = 18$: the absolute maximum is $18$ at $x = 3$.", work="2cm"),
]
same("p", [extremes(x**3 - 3 * x, 0, 3)[0]], [18])

# ---------------------------------------------------------------- quiz
def q_item(f, a, b, ask):
    big, small = extremes(f, a, b)
    v = big if ask == "maximum" else small
    return Item(rf"Find the absolute {ask} value of $f(x) = {sp.latex(f)}$ on $[{a}, {b}]$.", num(v),
                r"Candidates: " + ", ".join(rf"$f({sp.latex(k)}) = {sp.latex(val)}$" for k, val in candidates(f, a, b).items()) + ".", work="2.4cm")


QUIZ = [
    Variants(q_item(x**2 - 4 * x + 1, 0, 3, "minimum"), q_item(x**2 + 2 * x - 3, -2, 1, "minimum"), q_item(5 + 6 * x - x**2, 0, 4, "maximum")),
    Variants(q_item(x**3 - 3 * x**2, -1, 3, "maximum"), q_item(x**3 - 3 * x**2, -1, 3, "minimum"), q_item(x**3 - 3 * x, -2, 3, "maximum")),
    Variants(
        MCQ(r"To find the absolute extrema of a continuous $f$ on $[a, b]$, you must check", [r"only the critical points", r"only the endpoints",
            r"the critical points and the endpoints", r"only where $f'' = 0$"], "C", r"Both kinds of candidates."),
        MCQ(r"$f$ is continuous on $[1, 7]$ with one critical point, at $x = 4$, where $f$ has a relative minimum. The absolute maximum of $f$ on $[1, 7]$ is", [r"at $x = 1$ or $x = 7$",
            r"at $x = 4$", r"not guaranteed to exist", r"at the midpoint"], "A", r"The only interior candidate is a minimum, so the maximum is at an endpoint."),
        MCQ(r"$f(0) = 3$, $f(2) = -5$, $f(5) = 1$ and $f(8) = 4$, where $2$ and $5$ are the only critical points of $f$ on $[0, 8]$. The absolute maximum is", [r"$3$",
            r"$1$", r"$-5$", r"$4$"], "D", r"Largest candidate: $4$."),
    ),
    Variants(q_item(x * sp.exp(-x), 0, 2, "maximum"), q_item(x - sp.log(x), sp.Rational(1, 2), 2, "minimum"), q_item(x**2 * sp.exp(-x), 0, 4, "maximum")),
    Variants(
        Item(r"Find the absolute minimum value of $f(x) = x + \dfrac{9}{x}$ on $[1, 6]$.", num(6), r"$f'(x) = 1 - \frac{9}{x^2} = 0$ at $3$. Candidates $f(1) = 10$, $f(3) = 6$, $f(6) = 7.5$.", work="2.2cm"),
        Item(r"Find the absolute minimum value of $f(x) = x + \dfrac{16}{x}$ on $[2, 8]$.", num(8), r"$f'(x) = 1 - \frac{16}{x^2} = 0$ at $4$. Candidates $f(2) = 10$, $f(4) = 8$, $f(8) = 10$.", work="2.2cm"),
        Item(r"Find the absolute maximum value of $f(x) = x + \dfrac{4}{x}$ on $[1, 4]$.", num(5), r"$f'(x) = 1 - \frac{4}{x^2} = 0$ at $2$. Candidates $f(1) = 5$, $f(2) = 4$, $f(4) = 5$.", work="2.2cm"),
    ),
]
same("q5", [extremes(x + 9 / x, 1, 6)[1], extremes(x + 16 / x, 2, 8)[1], extremes(x + 4 / x, 1, 4)[0]], [6, 8, 5])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"The absolute maximum value of $f(x) = x^3 - 3x^2 + 1$ on $[-2, 3]$ is", [r"$1$", r"$-3$", r"$-19$", r"$3$"], "A", r"Candidates: $f(-2) = -19$, $f(0) = 1$, $f(2) = -3$, $f(3) = 1$."),
    MCQ(r"The absolute minimum value of $f(x) = 2\sin x + \cos(2x)$ on $[0, \pi]$ is", [r"$0$", r"$1$", r"$1.5$", r"$-1$"], "B",
        r"$f'(x) = 2\cos x(1 - 2\sin x) = 0$ at $\frac\pi6, \frac\pi2, \frac{5\pi}6$. Candidates $f(0) = 1$, $f\left(\frac\pi6\right) = 1.5$, $f\left(\frac\pi2\right) = 1$, $f(\pi) = 1$."),
    MCQ(r"$f$ is continuous on $[0, 5]$ and $f'(x) = (x - 1)(x - 4)$. The absolute minimum of $f$ on $[0, 5]$ must be the smaller of", [r"$f(1)$ and $f(4)$",
        r"$f(4)$ and $f(5)$", r"$f(0)$ and $f(4)$", r"$f(0)$ and $f(5)$"], "C",
        r"$f$ increases on $(0, 1)$ and $(4, 5)$ and decreases on $(1, 4)$. So $f(1) > f(0)$ and $f(5) > f(4)$: only $f(0)$ and $f(4)$ can be the minimum."),
    MCQ(r"The absolute maximum value of $g(x) = xe^{-x/2}$ on $[0, 5]$ is about", [r"$0.410$", r"$0.736$", r"$0.607$", r"$2$"], "B",
        r"$g'(x) = \left(1 - \frac x2\right)e^{-x/2} = 0$ at $x = 2$; $g(2) = 2e^{-1} \approx 0.736$; $g(5) \approx 0.410$.", calc=True),
]
same("m", [extremes(x**3 - 3 * x**2 + 1, -2, 3)[0], extremes(2 * sp.sin(x) + sp.cos(2 * x), 0, sp.pi)[1]], [1, 1])
close("m4", extremes(x * sp.exp(-x / 2), 0, 5)[0], 0.736, 5e-4)

FRQS = [
    FRQ("Water in a tank", (
        r"The amount of water in a tank is modeled by $A(t) = 2t^3 - 15t^2 + 24t + 40$, where $A(t)$ is measured in gallons and "
        r"$t$ is measured in hours, for $0 \le t \le 5$."), [
        Part("a", r"Is the amount of water in the tank increasing or decreasing at time $t = 2$? Give a reason for your answer.",
             selfcheck(r"\text{Decreasing}"),
             r"$A'(t) = 6t^2 - 30t + 24$, so $A'(2) = 24 - 60 + 24 = -12 < 0$. The amount of water is decreasing at $t = 2$.",
             [(1, "decreasing, because $A'(2) < 0$")], work="2cm"),
        Part("b", r"At what time $t$, for $0 \le t \le 5$, is the amount of water in the tank least? Justify your answer.", num(4),
             r"$A'(t) = 6(t - 1)(t - 4) = 0$ at $t = 1$ and $t = 4$. Candidates: $A(0) = 40$, $A(1) = 51$, $A(4) = 24$, $A(5) = 35$. "
             r"The amount of water is least at $t = 4$ hours.",
             [(1, "critical points $t = 1$ and $t = 4$"), (1, "considers the endpoints"), (1, "answer $t = 4$ with justification")],
             work="3.2cm"),
        Part("c", r"Find the greatest amount of water in the tank for $0 \le t \le 5$. Justify your answer.", num(51),
             r"From the candidates in part (b), the greatest amount is $A(1) = 51$ gallons.",
             [(1, "answer $51$ from the candidates")], work="1.6cm"),
    ], frq_type="Rate in context"),
]
A5 = 2 * x**3 - 15 * x**2 + 24 * x + 40
same("frq", list(extremes(A5, 0, 5)), [51, 24])
same("frq a", sp.diff(A5, x).subs(x, 2), -12)
same("frq cands", [A5.subs(x, v) for v in (0, 1, 4, 5)], [40, 51, 24, 35])

TOPIC = Topic(
    number="5.5", title="Using the Candidates Test to Determine Absolute (Global) Extrema",
    unit="Unit 5: Analytical Applications of Differentiation", ced=["FUN-4.A", "FUN-4.A.3"],
    goals=r"Find the absolute extrema of a continuous function on a closed interval by testing the critical points and the endpoints.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
