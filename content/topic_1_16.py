"""Topic 1.16: Working with the Intermediate Value Theorem.

CED: FUN-1.A (IVT: if f is continuous on [a, b] and d is between f(a) and f(b), then there is a
c in [a, b] with f(c) = d). Justification language follows AP scoring expectations: name the
theorem, state continuity on the closed interval, and show the target value is between.
"""
import sympy as sp

from calclib import (VideoExample, Variants, FRQ, MCQ, BigIdea, Check, Example, FigureRow, Formula, Item, Part, Section, Table, Text, Topic,
                     Video, check, num, same, selfcheck)
from calclib.figs import graph

x = sp.symbols("x")
P = x**3 + x - 1
same("P(0)", P.subs(x, 0), -1)
same("P(1)", P.subs(x, 1), 1)

F = 0.25 * (x - 2)**3 + 0.5 * x + 2
fa, fb = float(F.subs(x, 0.5)), float(F.subs(x, 4))
FIG_IVT = graph("t1_16_ivt", [("0.25*(x-2)^3+0.5*x+2", 0.5, 4)], xr=(0, 4.8), yr=(0, 7), hlines=[3.5],
                closed=[(0.5, round(fa, 3)), (4, round(fb, 3))],
                labels=[(0.5, round(fa, 3), "below right", r"$(a, f(a))$"), (4, round(fb, 3), "left", r"$(b, f(b))$"),
                        (4.8, 3.5, "above left", r"$y = k$")],
                w="6.6cm", h="4.8cm", caption=r"A continuous $f$ on $[a, b]$ crosses every height between $f(a)$ and $f(b)$.")
FIG_JUMP = graph("t1_16_jump", [("0.5*x+1", 0, 2), ("0.5*x+4", 2, 4)], xr=(0, 4.8), yr=(0, 7), hlines=[3.5],
                 open=[(2, 2)], closed=[(2, 5)], w="6.6cm", h="4.8cm",
                 caption=r"With a jump, the graph can skip the height $k$.")

NOTES = [
    Video("s1_16.py::Lesson", "The Intermediate Value Theorem", 3),

    Section("The theorem"),
    Formula("Intermediate Value Theorem (IVT)", (
        r"If $f$ is \blank{continuous} on the closed interval $[a, b]$ and $k$ is any number \blank{between} $f(a)$ and $f(b)$, "
        r"then there is at least one number $c$ in $[a, b]$ with $f(c) = \mblank{k}$.")),
    FigureRow([FIG_IVT, FIG_JUMP]),
    Text(r"The IVT guarantees that $c$ \blank{exists}; it does not say where $c$ is, or how many there are. "
         r"It sounds like common sense, and it is. But every condition matters: if $f$ is not continuous, the conclusion "
         r"can fail, as the jump shows."),

    Section("Proving an equation has a solution"),
    VideoExample('A root exists', work="3cm"),
    VideoExample('A given value', work="3cm"),

    Section("Reading a table"),
    Table(r"$x$ & $1$ & $3$ & $4$ & $7$ \\ $g(x)$ & $5$ & $-2$ & $1$ & $6$", "c|cccc"),
    Text(r"$g$ is continuous on $[1, 7]$. The values change sign on $[1, 3]$ and on $[3, 4]$, so $g$ has at least "
         r"\blank{$2$} zeros on $[1, 7]$. The IVT also guarantees $g(c) = 4$ for at least \mblank{2} values of $c$: one in "
         r"$(1, 3)$, since $4$ is between $5$ and $-2$, and one in $(4, 7)$, since $4$ is between $1$ and $6$."),
    VideoExample('Justify with the IVT', work="3.4cm"),
    BigIdea(r"A justification using the IVT says three things: $f$ is continuous on $[a, b]$; the target value is between $f(a)$ and "
            r"$f(b)$; therefore some $c$ in the interval gives that value."),
    Text(r"\textbf{On the AP exam.} Justifications like this are among the most important skills the exam tests. Expect at least one "
         r"question that asks for an IVT justification, or one for its cousin, the Mean Value Theorem (Unit 5). Write all three parts."),
    Check(r"$h$ is continuous with $h(0) = 3$ and $h(2) = -5$. What is the least number of solutions of $h(x) = 0$ on $[0, 2]$?",
          num(1), r"$0$ is between $3$ and $-5$, so the IVT guarantees at least one."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"$f$ is continuous on $[2, 6]$ with $f(2) = 10$ and $f(6) = -4$. What does the IVT guarantee about $f(c) = 3$?",
         selfcheck(r"c \in (2,6)"), r"$3$ is between $-4$ and $10$, so $f(c) = 3$ for at least one $c$ in $(2, 6)$.", work="1.8cm"),
    Item(r"Show that $x^4 - 3x + 1 = 0$ has a root in $[0, 1]$. Enter the value of the function at $x = 1$.", num(-1),
         r"The polynomial is continuous. $f(0) = 1 > 0$ and $f(1) = -1 < 0$. By the IVT, a root lies in $(0, 1)$.", work="2.4cm"),
    Item(r"Values of a continuous function $k$ are shown."
         r"\par\smallskip\centerline{\begin{tabular}{c|ccccc} $x$ & 0 & 2 & 5 & 6 & 9 \\ \hline $k(x)$ & 4 & $-1$ & 3 & 7 & $-2$\end{tabular}}"
         r"\par What is the fewest number of zeros $k$ must have on $[0, 9]$?", num(3),
         r"Sign changes on $[0,2]$, $[2,5]$ and $[6,9]$: at least $3$ zeros.", work="1.8cm"),
    Item(r"Using the same table, what is the fewest number of solutions of $k(x) = 5$ on $[0, 9]$?", num(2),
         r"$5$ lies between $3$ and $7$ (on $[5,6]$) and between $7$ and $-2$ (on $[6,9]$): at least $2$.", work="1.8cm"),
    Item(r"Let $f(x) = \dfrac{1}{x}$. Then $f(-1) = -1$ and $f(1) = 1$, yet $f(x) \ne 0$ for all $x$. Why doesn't this contradict "
         r"the IVT?", selfcheck(r"\text{not continuous on } [-1,1]"),
         r"$f$ is not continuous on $[-1, 1]$ (it is undefined at $0$), so the IVT does not apply.", work="1.8cm"),
    Item(r"Show that $e^x = 3 - x$ has a solution in $[0, 1]$. Enter $g(1)$ for $g(x) = e^x + x - 3$, rounded to three decimals.",
         num(sp.E - 2, tol=0.0006, display=r"\approx 0.718"),
         r"$g$ is continuous. $g(0) = -2 < 0$ and $g(1) = e - 2 \approx 0.718 > 0$, so $g(c) = 0$ for some $c$ in $(0,1)$.",
         work="2.4cm", calc=True),
    Item(r"A car's speed is $0$ mph at 1:00 PM and $65$ mph at 1:10 PM. Use the IVT to explain why the speed was exactly $40$ mph "
         r"at some moment. What assumption do you need?", selfcheck(r"\text{speed is continuous}"),
         r"Assuming speed changes continuously, $40$ is between $0$ and $65$, so by the IVT the speed was $40$ mph at some time "
         r"between 1:00 and 1:10.", work="2.2cm"),
    Item(r"Is the converse true? If $f(c) = k$ for every $k$ between $f(a)$ and $f(b)$, must $f$ be continuous? Give an example "
         r"or explain.", selfcheck(r"\text{No}"),
         r"No. Let $f(x) = \sin\frac1x$ for $x \ne 0$ and $f(0) = 0$. On $[-1, 1]$ it takes every value between $-1$ and $1$ "
         r"(infinitely often), yet it is not continuous at $0$. The IVT only goes one direction.", work="2cm"),
]
same("p2", (x**4 - 3 * x + 1).subs(x, 1), -1)

# extra practice (round 1)
G = x**3 - 4 * x + 2
PRACTICE += [
    Item(r"$f$ is continuous on $[-3, 1]$ with $f(-3) = 2$ and $f(1) = 8$. Must $f(c) = 5$ for some $c$ in $[-3, 1]$? "
         r"Must $f(c) = 0$?", selfcheck(r"\text{Yes; not necessarily}"),
         r"$5$ is between $2$ and $8$, so the IVT guarantees $f(c) = 5$ for some $c$ in $(-3, 1)$. $0$ is not between "
         r"$2$ and $8$, so the IVT says nothing about it. $f$ might or might not reach $0$.", work="2cm"),
    Item(r"Show that $x^3 - 4x + 2 = 0$ has a root in $[1, 2]$. Enter the value of the left side at $x = 1$.", num(G.subs(x, 1)),
         rf"The polynomial is continuous on $[1, 2]$. At $x = 1$ it is ${G.subs(x, 1)} < 0$ and at $x = 2$ it is "
         rf"${G.subs(x, 2)} > 0$. By the IVT, it equals $0$ somewhere in $(1, 2)$.", work="2.4cm"),
    Item(r"How many roots does the IVT guarantee for $x^3 - 4x + 2 = 0$ on $[-3, 2]$? Test the integers $-3, -2, \ldots, 2$.",
         num(3),
         "The values at $x = -3, -2, -1, 0, 1, 2$ are " + ", ".join(f"${G.subs(x, i)}$" for i in range(-3, 3))
         + r". The sign changes on $[-3, -2]$, $[0, 1]$ and $[1, 2]$, so there are at least $3$ roots. A cubic has at most "
         r"$3$, so there are exactly $3$.", work="2.6cm"),
    Item(r"Show that $\sin x = \frac12 x$ has a solution in $\left[\frac\pi2, \pi\right]$. Enter $h\!\left(\frac\pi2\right)$ for "
         r"$h(x) = \sin x - \frac12 x$, rounded to three decimals.",
         num(1 - sp.pi / 4, tol=0.0006, display=r"\approx 0.215"),
         r"$h$ is continuous. $h\!\left(\frac\pi2\right) = 1 - \frac\pi4 \approx 0.215 > 0$ and $h(\pi) = -\frac\pi2 < 0$. "
         r"By the IVT, $h(c) = 0$ for some $c$ in the interval, so $\sin c = \frac12 c$.", work="2.4cm", calc=True),
    Item(r"Values of a continuous function $w$ are shown."
         r"\par\smallskip\centerline{\begin{tabular}{c|ccccc} $t$ & 0 & 3 & 5 & 8 & 10 \\ \hline $w(t)$ & $-3$ & 2 & 6 & 1 & 4\end{tabular}}"
         r"\par What is the fewest number of solutions of $w(t) = 3$ on $[0, 10]$?", num(3),
         r"$3$ is between $2$ and $6$ on $[3, 5]$, between $6$ and $1$ on $[5, 8]$, and between $1$ and $4$ on $[8, 10]$. "
         r"At least $3$ solutions.", work="1.8cm"),
    Item(r"Using the same table, what is the fewest number of zeros $w$ must have on $[0, 10]$?", num(1),
         r"The only sign change is on $[0, 3]$, from $-3$ to $2$. At least $1$ zero.", work="1.6cm"),
    Item(r"Let $f(x) = \begin{cases} x + 1, & x < 2 \\ x + 3, & x \ge 2. \end{cases}$ Then $f(0) = 1$ and $f(3) = 6$. Is there a "
         r"$c$ in $[0, 3]$ with $f(c) = 4$? Does this contradict the IVT?", selfcheck(r"\text{No; no}"),
         r"No such $c$: the left piece stays below $3$ and the right piece starts at $5$. This does not contradict the IVT, "
         r"because $f$ has a jump at $x = 2$ and so is not continuous on $[0, 3]$.", work="2.2cm"),
    Item(r"$g$ is continuous with $g(1) = k^2$ and $g(4) = 2k + 3$. For $k = 2$, is $g(c) = 5$ guaranteed for some $c$ in "
         r"$[1, 4]$? Enter $g(4)$.", num(7),
         r"With $k = 2$, $g(1) = 4$ and $g(4) = 7$. Since $5$ is between $4$ and $7$ and $g$ is continuous, the IVT "
         r"guarantees it.", work="2cm"),
    Item(r"Jordan hikes up a trail from 8 AM to noon. The next day Jordan walks back down the same trail from 8 AM to noon. "
         r"Explain why there is a spot on the trail where Jordan is at the same time of day both days.",
         selfcheck(r"\text{IVT on the difference}"),
         r"Let $u(t)$ and $d(t)$ be the distances from the trailhead on the up day and the down day. Then $D(t) = u(t) - d(t)$ "
         r"is continuous, $D(8) < 0$ and $D(12) > 0$. By the IVT, $D(c) = 0$ for some time $c$: both days put Jordan at "
         r"the same spot at time $c$.", work="2.6cm"),
    Item(r"A tank holds $500$ gallons at noon and $120$ gallons at 3 PM. The volume $V(t)$ is continuous. Name the theorem "
         r"and explain why the tank held exactly $300$ gallons at some time between noon and 3 PM.",
         selfcheck(r"\text{IVT}"),
         r"The Intermediate Value Theorem: $V$ is continuous on the interval and $120 < 300 < 500$, so $V(c) = 300$ for some "
         r"$c$ between noon and 3 PM.", work="2cm"),
]
same("x1 G(1), G(2)", [G.subs(x, 1), G.subs(x, 2)], [-1, 2])
same("x1 G ints", [G.subs(x, i) for i in range(-3, 3)], [-13, 2, 5, 2, -1, 2])
same("x1 h", sp.N(sp.sin(sp.pi / 2) - sp.pi / 4), sp.N(1 - sp.pi / 4))
same("x1 g", [2**2, 2 * 2 + 3], [4, 7])

# ---------------------------------------------------------------- quiz
G2 = x**3 + x - 4
G3 = x**4 - 3 * x - 2
QUIZ = [
    Variants(
        MCQ(r"$f$ is continuous on $[1, 5]$, $f(1) = 7$ and $f(5) = 2$. Which must be true?",
            [r"$f(c) = 1$ for some $c$ in $(1,5)$", r"$f(c) = 4$ for some $c$ in $(1,5)$", r"$f(3) = 4.5$", r"$f$ is decreasing"], "B",
            r"$4$ is between $2$ and $7$.", why_not={"A": "$1$ is not between $2$ and $7$", "C": "the IVT doesn't give values at specific points"}),
        MCQ(r"$f$ is continuous on $[-2, 3]$, $f(-2) = -4$ and $f(3) = 6$. Which must be true?",
            [r"$f(0) = 0$", r"$f(c) = 7$ for some $c$ in $(-2, 3)$", r"$f$ is increasing", r"$f(c) = 5$ for some $c$ in $(-2, 3)$"], "D",
            r"$5$ is between $-4$ and $6$.", why_not={"B": "$7$ is not between $-4$ and $6$", "A": "the IVT doesn't say where"}),
        MCQ(r"$f$ is continuous on $[0, 10]$, $f(0) = 3$ and $f(10) = 3$. Which must be true?",
            [r"$f(c) = 3$ for some $c$ in $[0, 10]$", r"$f(c) = 0$ for some $c$ in $(0, 10)$", r"$f(5) = 3$", r"$f$ is constant"], "A",
            r"$c = 0$ works. The IVT promises nothing new here: no value other than $3$ is guaranteed between $f(0)$ and $f(10)$.",
            why_not={"B": "$0$ is not between $3$ and $3$", "D": "the graph can wander in between"}),
    ),
    Variants(
        Item(r"Values of a continuous $g$: $g(0) = -3$, $g(2) = 1$, $g(4) = -1$, $g(6) = 5$. What is the fewest number of zeros of $g$ on $[0, 6]$?",
             num(3), r"Sign changes on $[0,2]$, $[2,4]$, $[4,6]$.", work="1.6cm"),
        Item(r"Values of a continuous $g$: $g(1) = 4$, $g(3) = 2$, $g(5) = -2$, $g(7) = -6$. What is the fewest number of zeros of $g$ on $[1, 7]$?",
             num(1), r"The only sign change is on $[3, 5]$.", work="1.6cm"),
        Item(r"Values of a continuous $g$: $g(0) = 2$, $g(1) = 5$, $g(3) = 1$, $g(4) = 6$. What is the fewest number of solutions of $g(x) = 3$ on $[0, 4]$?",
             num(3), r"$3$ is between $2$ and $5$ on $[0,1]$, between $5$ and $1$ on $[1,3]$, and between $1$ and $6$ on $[3,4]$.", work="1.6cm"),
    ),
    Variants(
        Item(r"For $h(x) = x^3 - 2x - 5$, find $h(2)$. (Together with $h(3) = 16$, this shows a root in $(2,3)$.)", num(-1),
             r"$8 - 4 - 5 = -1$.", work="1.4cm"),
        Item(r"For $h(x) = x^3 + x - 4$, find $h(1)$. (Together with $h(2) = 6$, this shows a root in $(1,2)$.)", num(G2.subs(x, 1)),
             rf"$1 + 1 - 4 = {G2.subs(x, 1)}$.", work="1.4cm"),
        Item(r"For $h(x) = x^4 - 3x - 2$, find $h(2)$. (Together with $h(1) = -4$, this shows a root in $(1,2)$.)", num(G3.subs(x, 2)),
             rf"$16 - 6 - 2 = {G3.subs(x, 2)}$.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"Which is required to apply the IVT to $f$ on $[a, b]$?",
            [r"$f$ is differentiable on $(a,b)$", r"$f(a) = f(b)$", r"$f$ is continuous on $[a, b]$", r"$f(a) < 0 < f(b)$"], "C",
            r"Continuity on the closed interval is the only hypothesis.", why_not={"A": "that's the Mean Value Theorem (Unit 5)"}),
        MCQ(r"A student writes: ``$f(1) = -2$ and $f(4) = 3$, so by the IVT $f$ has a zero in $(1, 4)$.'' What is missing?",
            [r"That $f$ is differentiable", r"That $f$ is continuous on $[1, 4]$", r"That $f(0) = 0$", r"Nothing"], "B",
            r"The IVT needs continuity on the closed interval, and a full justification says so.", why_not={"D": "continuity must be stated"}),
        MCQ(r"Which conclusion does the IVT give?",
            [r"A value is reached at least once in the interval.", r"A value is reached exactly once.", r"The function is increasing.",
             r"The maximum is at an endpoint."], "A", r"The IVT guarantees existence, not uniqueness or location.",
            why_not={"B": "there can be several such points"}),
    ),
    Variants(
        MCQ(r"$f(x) = \begin{cases} x + 1, & x < 1 \\ x + 3, & x \ge 1 \end{cases}$ on $[0, 2]$ has $f(0) = 1$ and $f(2) = 5$. "
            r"Is there a $c$ with $f(c) = 3$?", [r"Yes, by the IVT", r"No; the IVT does not apply and $f$ skips $3$", r"Yes, $c = 1$", r"Yes, $c = 2$"], "B",
            r"$f$ jumps from values near $2$ to $4$ at $x = 1$, skipping $3$. It is not continuous, so the IVT doesn't apply.",
            why_not={"C": "$f(1) = 4$"}),
        MCQ(r"$f(x) = \dfrac{1}{x}$ has $f(-1) = -1$ and $f(1) = 1$. Why doesn't the IVT guarantee a zero in $(-1, 1)$?",
            [r"Because $f$ is not continuous on $[-1, 1]$", r"Because $0$ is not between $-1$ and $1$", r"Because $f$ is decreasing", r"It does guarantee one."], "A",
            r"$f$ is undefined at $0$, so it is not continuous on $[-1, 1]$.", why_not={"B": "$0$ is between them", "D": "$\\frac1x$ is never $0$"}),
        MCQ(r"$g$ is continuous on $[2, 6]$ with $g(2) = 5$ and $g(6) = -1$. How many solutions of $g(x) = 0$ must there be in $(2, 6)$?",
            [r"Exactly one", r"At least one", r"At least two", r"None are guaranteed"], "B",
            r"$0$ is between $-1$ and $5$, so at least one. The IVT never says ``exactly''.", why_not={"A": "there could be more"}),
    ),
]
same("q3", (x**3 - 2 * x - 5).subs(x, 2), -1)
same("q versions", [G2.subs(x, 1), G2.subs(x, 2), G3.subs(x, 2), G3.subs(x, 1)], [-2, 6, 8, -4])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"The function $f$ is continuous on $[-2, 4]$ with $f(-2) = 5$, $f(0) = -1$, $f(4) = 3$. What is the fewest number of "
        r"values of $x$ in $[-2,4]$ with $f(x) = 2$?", [r"$0$", r"$1$", r"$2$", r"$3$"], "C",
        r"$2$ is between $5$ and $-1$, and between $-1$ and $3$."),
    MCQ(r"Let $g(x) = x^5 + 2x - 7$. On which interval does the IVT guarantee a zero of $g$?",
        [r"$[1, 2]$", r"$[0, 1]$", r"$[-1, 0]$", r"$[2, 3]$"], "A", r"$g(1) = -4 < 0 < 29 = g(2)$."),
    MCQ(r"A continuous function $h$ has $h(1) = 4$ and $h(3) = 4$. Which must be true?",
        [r"$h(2) = 4$", r"$h$ has no zeros on $[1,3]$", r"$h$ is constant", r"none of these"], "D",
        r"The IVT says nothing new when the endpoint values are equal: $h$ could dip below zero or rise in between."),
    MCQ(r"Temperature $T(t)$ is continuous, with $T(0) = 45^\circ$ and $T(6) = 70^\circ$. Which statement is justified by the IVT?",
        [r"$T(3) = 57.5^\circ$", r"The temperature was $60^\circ$ at some time in $(0, 6)$",
         r"The temperature increased at $\frac{25}{6}$ degrees per hour", r"The temperature never exceeded $70^\circ$"], "B",
        r"$60$ is between $45$ and $70$.", why_not={"C": "an average rate; that's not the IVT"}),
]
same("m2", [(x**5 + 2 * x - 7).subs(x, 1), (x**5 + 2 * x - 7).subs(x, 2)], [-4, 29])

FRQS = [
    FRQ("Reservoir level", (
        r"The water level of a reservoir is modeled by a continuous function $W$, where $W(t)$ is measured in feet and $t$ is "
        r"measured in months after January 1. Selected values of $W(t)$ are given in the table."
        r"\par\smallskip\centerline{\begin{tabular}{c|ccccc} $t$ (months) & 0 & 2 & 5 & 8 & 11 \\ \hline "
        r"$W(t)$ (feet) & 42 & 48 & 39 & 36 & 44\end{tabular}}"), [
        Part("a", r"Find the average rate of change of $W$ over the interval $5 \le t \le 11$. Show the work that leads to your "
                  r"answer. Indicate units of measure.",
             num(sp.Rational(5, 6), tol=0.005, display=r"\tfrac56\ \text{feet per month}"),
             r"$\dfrac{W(11) - W(5)}{11 - 5} = \dfrac{44 - 39}{6} = \dfrac56$ feet per month.",
             [(1, "difference quotient and answer"), (1, "units")], work="2.6cm"),
        Part("b", r"Must there be a value $c$, for $2 < c < 8$, such that $W(c) = 40$? Justify your answer.",
             selfcheck(r"\text{Yes}"),
             r"$W$ is continuous on $2 \le t \le 8$, and $W(8) = 36 < 40 < 48 = W(2)$. By the Intermediate Value Theorem, there must "
             r"be a value $c$, with $2 < c < 8$, such that $W(c) = 40$.",
             [(1, "$W(8) < 40 < W(2)$"), (1, "yes, using continuity and the Intermediate Value Theorem")], work="2.8cm"),
        Part("c", r"For $0 \le t \le 11$, what is the fewest number of times at which $W(t)$ must equal $45$? Give a reason for your answer.",
             num(2),
             r"$W(0) = 42 < 45 < 48 = W(2)$ and $W(2) = 48 > 45 > 39 = W(5)$. Since $W$ is continuous, the Intermediate Value Theorem "
             r"gives a time in $(0, 2)$ and a time in $(2, 5)$ at which $W(t) = 45$. So $W(t)$ must equal $45$ at least two times.",
             [(1, "answer $2$"), (1, "reason: intervals $(0, 2)$ and $(2, 5)$ with the Intermediate Value Theorem")], work="3cm"),
    ], frq_type="Table"),
]
W = {0: 42, 2: 48, 5: 39, 8: 36, 11: 44}
same("frq a", sp.Rational(W[11] - W[5], 11 - 5), sp.Rational(5, 6))
check("frq b", W[8] < 40 < W[2])
# 45 is crossed on (0,2) and (2,5) only: no other consecutive pair brackets 45
ts = sorted(W)
check("frq c", sum((W[p] - 45) * (W[q] - 45) < 0 for p, q in zip(ts, ts[1:])) == 2)

TOPIC = Topic(
    number="1.16", title="Working with the Intermediate Value Theorem",
    unit="Unit 1: Limits and Continuity", ced=["FUN-1.A", "FUN-1.A.1"],
    goals=r"Apply the Intermediate Value Theorem to continuous functions given by formulas or tables, and justify conclusions with it.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
