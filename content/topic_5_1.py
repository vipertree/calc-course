"""Topic 5.1: Using the Mean Value Theorem.

CED: FUN-1.B (FUN-1.B.1): if f is continuous on [a, b] and differentiable on (a, b), some c in (a, b) has
f'(c) = (f(b) - f(a))/(b - a). Geometric picture: slide the secant line parallel to itself until it just touches the curve.
Worked examples: x^3 - x on [0, 2], |x| on [-1, 2] (fails), a car trip (instantaneous speed = average speed).
AP: a justification names the theorem AND checks both conditions.
"""
import sympy as sp

from calclib.figs import graph
from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Text, Topic, Variants, Video, num,
                     same, selfcheck)

x = sp.symbols("x")


def mvt_c(f, a, b):
    """The c values in (a, b) where f'(c) equals the average rate of change."""
    m = (f.subs(x, b) - f.subs(x, a)) / (b - a)
    return sorted(c for c in sp.solve(sp.diff(f, x) - m, x) if c.is_real and a < c < b)


same("ex1", mvt_c(x**3 - x, 0, 2), [2 / sp.sqrt(3)])

NOTES = [
    Video("s5_1.py::Lesson", "The Mean Value Theorem", 4),

    Section("The theorem"),
    Text(r"If you drive $120$ miles in $2$ hours, your average speed is $60$ mph. At some moment, your speedometer must have read exactly "
         r"\blank{60} mph. The Mean Value Theorem says the same thing about any smooth function."),
    Formula("The Mean Value Theorem (MVT)", (
        r"If $f$ is \blank{continuous} on $[a, b]$ and \blank{differentiable} on $(a, b)$, then there is at least one $c$ in $(a, b)$ with "
        r"\[ f'(c) = \frac{f(b) - f(a)}{b - a}. \]")),
    Text(r"\textbf{In words.} At some point $c$ between $a$ and $b$, the \blank{instantaneous} rate of change equals the "
         r"\blank{average} rate of change over $[a, b]$. There can be more than one such $c$. The theorem guarantees at least one."),
    Text(r"\textbf{The picture.} The right side is the slope of the \blank{secant} line from $\left(a, f(a)\right)$ to $\left(b, f(b)\right)$. "
         r"The theorem says some \blank{tangent} line in between is parallel to it: slide the secant line sideways until it just touches the curve."),
    graph("t5_1_pic", [("0.25*x^3 - x + 1", -0.5, 2.6), ("1", -0.3, 2.3, "dashed"), ("0.25*1.1547^3 - 1.1547 + 1 + 0*x", 0.6, 1.7)], (-0.5, 2.6), (-1, 3.5),
          closed=[(0, 1), (2, 1)], labels=[(0, 1, "above left", "$a$"), (2, 1, "below right", "$b$")], caption="The secant line from $a$ to $b$ (dashed), and a tangent line parallel to it."),

    Section("Both conditions matter"),
    Text(r"If $f$ has a jump, a hole, or a corner, the conclusion can fail. $f(x) = |x|$ on $[-1, 2]$ has average rate of change "
         r"\[ \frac{2 - 1}{2 - (-1)} = \frac13, \] but $f'(x)$ is only ever $-1$ or $1$. The theorem doesn't apply: $f$ is not differentiable at \blank{$0$}."),
    Text(r"\textbf{Closed and open.} $f$ must be continuous on the closed interval $[a, b]$, endpoints included, but differentiable "
         r"only on the open interval $(a, b)$: the endpoints don't need a derivative. On most problems this difference never comes up. "
         r"You'll usually have a polynomial or another function that is continuous and differentiable well past both ends of the interval."),
    Text(r"\textbf{On the AP exam:} to use the MVT, say so by name and check \blank{both} conditions. A table of values from a differentiable "
         r"function is enough: differentiable implies continuous."),
    VideoExample('From given values', work="2.4cm"),
    Text(r"\textbf{From a table.} A classic AP question gives a table of values and asks whether $f'(c)$ must equal some number $k$. "
         r"The average rate over the whole table often isn't $k$. Try pairs of values until one gives an average rate of change of exactly "
         r"\blank{$k$}, then apply the MVT on that smaller interval. (Example 4 in the video.)"),
    BigIdea(r"Somewhere between $a$ and $b$, the instantaneous rate equals the average rate, as long as $f$ is continuous on $[a, b]$ and differentiable on $(a, b)$."),
    Check(r"Find the $c$ guaranteed by the MVT for $f(x) = x^2$ on $[1, 3]$.", num(2), r"Average rate $\frac{9 - 1}{3 - 1} = 4$. Set $f'(c) = 2c$ equal to it: $2c = 4$, so $c = 2$, which is in $(1, 3)$."),
]

# ---------------------------------------------------------------- practice
P = [(x**2 + 2 * x, 0, 4), (x**3, 0, 3), (sp.sqrt(x), 0, 4), (x**2 - 4 * x + 1, 1, 5), (1 / x, 1, 4), (x**3 - 3 * x, -2, 2)]
PRACTICE = []
for f, a, b in P:
    cs = mvt_c(f, a, b)
    PRACTICE.append(Item(rf"Find every value of $c$ guaranteed by the Mean Value Theorem for $f(x) = {sp.latex(f)}$ on $[{a}, {b}]$."
                         + (" Enter the larger one." if len(cs) > 1 else ""), num(cs[-1]),
                         rf"Average rate ${sp.latex((f.subs(x, b) - f.subs(x, a)) / (b - a))}$; $f'(c) = {sp.latex(sp.diff(f, x).subs(x, sp.Symbol('c')))}$ equals it at "
                         rf"$c = {', '.join(sp.latex(c) for c in cs)}$.", work="2.4cm"))
same("p", [mvt_c(f, a, b) for f, a, b in P], [[2], [sp.sqrt(3)], [1], [3], [2], [-2 / sp.sqrt(3), 2 / sp.sqrt(3)]])
PRACTICE += [
    Item(r"Does the Mean Value Theorem apply to $f(x) = \dfrac{1}{x - 2}$ on $[0, 4]$? Explain.", selfcheck(r"\text{no}"),
         r"No: $f$ is not continuous at $x = 2$, which is in $[0, 4]$.", work="1.6cm"),
    Item(r"Does the Mean Value Theorem apply to $f(x) = x^{2/3}$ on $[-1, 8]$? Explain.", selfcheck(r"\text{no}"),
         r"No: $f'(x) = \frac{2}{3x^{1/3}}$ is undefined at $x = 0$, so $f$ is not differentiable on $(-1, 8)$ (it has a cusp).", work="1.6cm"),
    Item(r"Ana drives a toll road. She enters at 1:00 p.m. and exits $150$ miles later at 3:00 p.m. The speed limit is $65$ mph. Use the MVT to show she was speeding at some moment.",
         num(75), r"Her position is differentiable, so by the MVT her speed at some moment equals her average speed, $\frac{150}{2} = 75$ mph $> 65$.", work="2cm"),
    Item(r"$g$ is differentiable with $g(2) = 7$ and $g(6) = -1$. What value must $g'$ take somewhere in $(2, 6)$?", num(-2),
         r"By the MVT, $g'(c) = \frac{-1 - 7}{6 - 2} = -2$ for some $c$ in $(2, 6)$.", work="1.6cm"),
    Item(r"$h$ is differentiable, $h(0) = 3$, and $h'(x) \le 2$ for all $x$. What is the largest possible value of $h(5)$?", num(13),
         r"By the MVT, $\frac{h(5) - 3}{5} = h'(c) \le 2$, so $h(5) \le 13$.", work="2cm"),
]
PRACTICE.append(Item(r"A differentiable function $T$ has $T(0) = 80$, $T(4) = 60$ and $T(10) = 48$. Must $T'(t) = -5$ at some $t$ in $(0, 4)$? Explain.",
                    selfcheck(r"\text{yes}"), r"Yes: $\frac{60 - 80}{4 - 0} = -5$, and $T$ is differentiable (so also continuous), so the MVT applies on $[0, 4]$.", work="1.8cm"))

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(*[Item(rf"Find the value of $c$ guaranteed by the Mean Value Theorem for $f(x) = {sp.latex(f)}$ on $[{a}, {b}]$.", num(mvt_c(f, a, b)[0]),
                    rf"Set $f'(c)$ equal to the average rate ${sp.latex((f.subs(x, b) - f.subs(x, a)) / (b - a))}$: $c = {sp.latex(mvt_c(f, a, b)[0])}$.", work="2cm")
               for f, a, b in [(x**2 - 2 * x, 0, 4), (3 * x**2 + 1, -1, 3), (x**2 + 5 * x, 2, 6)]]),
    Variants(
        Item(r"$f$ is differentiable with $f(3) = 10$ and $f(7) = 2$. By the MVT, $f'(c) = $ what number for some $c$ in $(3, 7)$?", num(-2), r"$\frac{2 - 10}{4} = -2$.", work="1.4cm"),
        Item(r"$f$ is differentiable with $f(-1) = 4$ and $f(5) = 22$. By the MVT, $f'(c) = $ what number for some $c$ in $(-1, 5)$?", num(3), r"$\frac{22 - 4}{6} = 3$.", work="1.4cm"),
        Item(r"$f$ is differentiable with $f(0) = -6$ and $f(8) = 6$. By the MVT, $f'(c) = $ what number for some $c$ in $(0, 8)$?", num(sp.Rational(3, 2)), r"$\frac{6 + 6}{8} = \frac32$.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"For which function on $[-1, 1]$ does the Mean Value Theorem apply?", [r"$f(x) = |x|$", r"$f(x) = \frac1x$", r"$f(x) = x^3$", r"$f(x) = x^{1/3}$"], "C",
            r"$x^3$ is a polynomial: continuous and differentiable everywhere.", why_not={"A": "corner at $0$", "B": "not continuous at $0$", "D": "vertical tangent at $0$"}),
        MCQ(r"For which function on $[0, 2]$ does the Mean Value Theorem apply?", [r"$f(x) = \frac{1}{x - 1}$", r"$f(x) = e^x$", r"$f(x) = |x - 1|$", r"$f(x) = \sqrt{x - 1}$"], "B",
            r"$e^x$ is continuous and differentiable everywhere.", why_not={"A": "not continuous at $1$", "C": "corner at $1$", "D": "not defined on $[0, 1)$"}),
        MCQ(r"For which function on $[1, 3]$ does the Mean Value Theorem apply?", [r"$f(x) = |x - 2|$", r"$f(x) = \frac{1}{x - 2}$", r"$f(x) = (x - 2)^{2/3}$", r"$f(x) = \ln x$"], "D",
            r"$\ln x$ is continuous and differentiable for $x > 0$.", why_not={"A": "corner at $2$", "B": "not continuous at $2$", "C": "cusp at $2$"}),
    ),
    Variants(
        MCQ(r"A runner covers $10$ km in $50$ minutes. Which must be true?", [r"At some moment, she ran exactly $0.2$ km per minute.", r"She ran $0.2$ km per minute the whole time.",
            r"Her top speed was $0.2$ km per minute.", r"She never ran faster than $0.2$ km per minute."], "A", r"The MVT guarantees the average rate is hit at some instant."),
        MCQ(r"A tank's volume went from $200$ L to $80$ L in $30$ minutes. Which must be true?", [r"It drained at $4$ L/min the whole time.", r"At some moment, it was draining at exactly $4$ L/min.",
            r"It never drained faster than $4$ L/min.", r"It was never filling."], "B", r"The MVT guarantees the average rate is hit at some instant."),
        MCQ(r"A plane climbs from $2000$ ft to $14000$ ft in $8$ minutes. Which must be true?", [r"It climbed at $1500$ ft/min the whole time.", r"It never descended.",
            r"At some moment, it was climbing at exactly $1500$ ft/min.", r"Its top climb rate was $1500$ ft/min."], "C", r"The MVT guarantees the average rate is hit at some instant."),
    ),
    Variants(
        Item(r"$h$ is differentiable, $h(1) = 5$, and $h'(x) \le 3$ for all $x$. What is the largest possible value of $h(4)$?", num(14), r"$h(4) \le 5 + 3(3) = 14$.", work="1.6cm"),
        Item(r"$h$ is differentiable, $h(0) = -2$, and $h'(x) \ge 4$ for all $x$. What is the smallest possible value of $h(3)$?", num(10), r"$h(3) \ge -2 + 4(3) = 10$.", work="1.6cm"),
        Item(r"$h$ is differentiable, $h(2) = 1$, and $h'(x) \le -1$ for all $x$. What is the largest possible value of $h(6)$?", num(-3), r"$h(6) \le 1 - 4 = -3$.", work="1.6cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"Let $f(x) = x^3 - 4x$. The value of $c$ in $(0, 2)$ guaranteed by the Mean Value Theorem on $[0, 2]$ is", [r"$1$", r"$\frac{2}{\sqrt3}$", r"$\sqrt2$", r"$\frac43$"], "B",
        r"Average rate $0$; $3c^2 - 4 = 0$, so $c = \frac{2}{\sqrt3}$."),
    MCQ(r"$f$ is differentiable on $[2, 8]$ with $f(2) = 5$ and $f(8) = -7$. Which must be true?", [r"$f(c) = 0$ for some $c$ in $(2, 8)$ only",
        r"$f'(c) = 2$ for some $c$ in $(2, 8)$", r"$f'(c) = -2$ for some $c$ in $(2, 8)$", r"$f'(c) = 0$ for some $c$ in $(2, 8)$"], "C",
        r"$\frac{-7 - 5}{6} = -2$. (Choice A is true too, by the IVT, but the word \emph{only} makes it false.)"),
    MCQ(r"$f(x) = x^{2/3}$ on $[-8, 8]$: the average rate of change is $0$, but $f'(x) \ne 0$ for every $x$. Why doesn't this contradict the MVT?",
        [r"$f$ is not continuous on $[-8, 8]$", r"$f(-8) \ne f(8)$", r"The MVT only applies to polynomials", r"$f$ is not differentiable at $x = 0$"], "D",
        r"$f'(x) = \frac{2}{3x^{1/3}}$ is undefined at $0$: a cusp."),
    MCQ(r"A differentiable $g$ has $g(0) = 1$ and $g(4) = 9$. Which value of $g'$ is guaranteed somewhere in $(0, 4)$?", [r"$2$", r"$9$", r"$\frac94$", r"$8$"], "A",
        r"$\frac{9 - 1}{4} = 2$."),
]
same("m", [mvt_c(x**3 - 4 * x, 0, 2)], [[2 / sp.sqrt(3)]])

FRQS = [
    FRQ("A cyclist's ride", (
        r"Rosa rides a bike along a straight road. Her position is modeled by a twice-differentiable function $s$, where $s(t)$ is "
        r"measured in meters and $t$ is measured in seconds. Selected values of $s(t)$ are given in the table. Rosa's velocity is "
        r"$v(t) = s'(t)$, and $v(0) = 5$ and $v(60) = 5$ meters per second."
        r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $t$ (seconds) & 0 & 20 & 50 & 60 \\ \hline "
        r"$s(t)$ (meters) & 0 & 140 & 380 & 500\end{tabular}}"), [
        Part("a", r"Approximate $s'(10)$ using the average rate of change of $s$ over the interval $0 \le t \le 20$. Show the work "
                  r"that leads to your answer. Indicate units of measure.",
             num(7, display=r"7\ \text{meters per second}"),
             r"$s'(10) \approx \dfrac{s(20) - s(0)}{20 - 0} = \dfrac{140}{20} = 7$ meters per second.",
             [(1, "difference quotient and answer"), (1, "units")], work="2.4cm"),
        Part("b", r"Must there be a value $c$, for $20 < c < 50$, such that $v(c) = 8$? Justify your answer.",
             selfcheck(r"\text{Yes}"),
             r"$\dfrac{s(50) - s(20)}{50 - 20} = \dfrac{380 - 140}{30} = 8$. Because $s$ is differentiable, $s$ is continuous on "
             r"$20 \le t \le 50$ and differentiable on $20 < t < 50$. By the Mean Value Theorem, there must be a value $c$, with "
             r"$20 < c < 50$, such that $v(c) = s'(c) = 8$.",
             [(1, "average rate of change $8$ on $20 \\le t \\le 50$"), (1, "yes, using the Mean Value Theorem with its conditions")],
             work="2.8cm"),
        Part("c", r"Explain why there must be a value $c$, for $0 < c < 60$, such that $v'(c) = 0$.",
             selfcheck(r"v(0) = v(60) \text{ and the Mean Value Theorem}"),
             r"$s$ is twice differentiable, so $v = s'$ is differentiable and therefore continuous on $0 \le t \le 60$. "
             r"$\dfrac{v(60) - v(0)}{60 - 0} = \dfrac{5 - 5}{60} = 0$. By the Mean Value Theorem, there must be a value $c$, with "
             r"$0 < c < 60$, such that $v'(c) = 0$.",
             [(1, "$\\frac{v(60) - v(0)}{60 - 0} = 0$"), (1, "justification using the Mean Value Theorem")], work="2.8cm"),
    ], frq_type="Table"),
]
same("frq", [sp.Rational(140, 20), sp.Rational(380 - 140, 30), sp.Rational(5 - 5, 60)], [7, 8, 0])

TOPIC = Topic(
    number="5.1", title="Using the Mean Value Theorem",
    unit="Unit 5: Analytical Applications of Differentiation", ced=["FUN-1.B", "FUN-1.B.1"],
    goals=r"State the Mean Value Theorem, check its conditions, and use it to find where the instantaneous rate equals the average rate.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
