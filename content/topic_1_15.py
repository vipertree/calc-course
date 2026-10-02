"""Topic 1.15: Connecting limits at infinity and horizontal asymptotes.

CED: LIM-2.D (limits at infinity; horizontal asymptotes; relative growth of dominant terms).
"""
import sympy as sp

from calclib import (VideoExample, Variants, limchain, FRQ, MCQ, BigIdea, Check, Definition, Example, FigureRow, Formula, Item, Part, Section,
                     Table, Text, Topic, Video, dne, infinite, num, same, selfcheck)
from calclib.figs import graph

x = sp.symbols("x")
oo = sp.oo
same("intro", sp.limit((3 * x**2 + x) / (x**2 + 1), x, oo), 3)
same("logistic -", sp.limit(5 / (1 + sp.exp(-x)), x, -oo), 0)
same("logistic +", sp.limit(5 / (1 + sp.exp(-x)), x, oo), 5)
same("sinx/x", sp.limit(sp.sin(x) / x, x, oo), 0)

FIG_R = graph("t1_15_r", [("(3*x^2+x)/(x^2+1)", -12, 12)], xr=(-12, 12), yr=(-1, 4.5), hlines=[3], xstep=4,
              w="7cm", h="4.4cm", samples=240, caption=r"$y = \dfrac{3x^2+x}{x^2+1}$ approaches $y = 3$ at both ends.")
FIG_L = graph("t1_15_logistic", [("5/(1+exp(-x))", -8, 8)], xr=(-8, 8), yr=(-0.5, 6), hlines=[0, 5], xstep=4, ystep=1,
              w="5.2cm", h="4cm", caption=r"$\dfrac{5}{1+e^{-x}}$: two horizontal asymptotes")
FIG_S = graph("t1_15_sinc", [("sin(deg(x))/x", 0.3, 30), ("1/x", 0.3, 30, "dashed"), ("-1/x", 0.3, 30, "dashed")],
              xr=(0, 30), yr=(-1, 1.2), xstep=10, ystep=0.5, w="5.2cm", h="4cm", samples=400,
              caption=r"$\dfrac{\sin x}{x}$, squeezed by $\pm\dfrac1x$")

NOTES = [
    Video("s1_15.py::Lesson", "Limits at infinity", 3),

    Section("Limits at infinity"),
    Text(r"\textbf{Reminder.} A horizontal line has an equation of the form $y = c$: every point on the line $y = 3$ has height $3$, "
         r"whatever $x$ is."),
    Definition("Horizontal asymptote", (
        r"If $\displaystyle \lim_{x\to\infty} f(x) = L$ or $\displaystyle \lim_{x\to-\infty} f(x) = L$ for a real number $L$, then the "
        r"line \blank{$y = L$} is a \textbf{horizontal asymptote} of the graph of $f$.")),
    FIG_R,
    BigIdea(r"For large enough $x$, only the fastest-growing terms matter. They dominate everything else."),
    Text(r"So keep the limit notation and write a chain: the limit of the original equals the limit of the leading terms, "
         r"which simplifies to the answer. \[ \lim_{x\to\infty}\frac{3x^2+x}{x^2+1} = \lim_{x\to\infty}\frac{3x^2}{x^2} = \lim_{x\to\infty} 3 = 3. \] "
         r"To make the dominance exact, divide the top and bottom by \blank{$x^2$}: "
         r"\[ \lim_{x\to\infty}\frac{3 + \frac1x}{1 + \frac1{x^2}} = \frac{3+0}{1+0} = \mblank{3} \]."),

    Section("Rational functions: compare degrees"),
    Formula("End behavior of $\\dfrac{p(x)}{q(x)}$", (
        r"$\bullet$ degree of $p$ $<$ degree of $q$: $\displaystyle \lim_{x\to\pm\infty} = \mblank{0}$. \par "
        r"$\bullet$ degrees equal: the limit is the ratio of the \blank{leading coefficients}. \par "
        r"$\bullet$ degree of $p$ $>$ degree of $q$: the function is \blank{unbounded}; there is no horizontal asymptote.")),
    Table(r"$\dfrac{5x+2}{x^2-3}$ & \mblank{0} \\ $\dfrac{4x^3-x}{2x^3+7}$ & \mblank{2} \\ "
          r"$\dfrac{x^2+1}{x-4}$ & \mblank{\infty}", "cc", header=r"function & $\displaystyle \lim_{x\to\infty}$"),

    Section("Beyond rational functions"),
    FigureRow([FIG_L, FIG_S]),
    Text(r"$\displaystyle \lim_{x\to\infty}e^{-x} = \mblank{0}$ and $\displaystyle \lim_{x\to-\infty}e^{x} = \mblank{0}$. "
         r"A function may have different horizontal asymptotes at each end: $\dfrac{5}{1+e^{-x}}$ has $y = 0$ on the left and "
         r"$y = \mblank{5}$ on the right. Since \[ -\frac1x \le \frac{\sin x}{x} \le \frac1x \] for $x > 0$, the squeeze theorem gives "
         r"$\displaystyle \lim_{x\to\infty}\frac{\sin x}{x} = \mblank{0}$."),
    VideoExample('Roots at negative infinity', work="3cm"),
    BigIdea(r"In the long run, the fastest-growing terms decide everything. A finite limit at infinity is a horizontal asymptote."),
    Check(r"Find \[ \lim_{x\to\infty}\frac{6x^2 - 5}{3 + 2x - 3x^2}. \]", num(-2), r"\[ \lim_{x\to\infty}\frac{6x^2 - 5}{3 + 2x - 3x^2} = \lim_{x\to\infty}\frac{6x^2}{-3x^2} = \lim_{x\to\infty}(-2) = -2. \]"),
]
same("table", [sp.limit((5 * x + 2) / (x**2 - 3), x, oo), sp.limit((4 * x**3 - x) / (2 * x**3 + 7), x, oo),
               sp.limit((x**2 + 1) / (x - 4), x, oo)], [0, 2, oo])
same("roots", sp.limit(sp.sqrt(4 * x**2 + 1) / x, x, -oo), -2)
same("check", sp.limit((6 * x**2 - 5) / (3 + 2 * x - 3 * x**2), x, oo), -2)

# ---------------------------------------------------------------- practice
P = [
    (r"\displaystyle\lim_{x\to\infty}\frac{7x-3}{2x+5}", (7 * x - 3) / (2 * x + 5), oo),
    (r"\displaystyle\lim_{x\to-\infty}\frac{x^2+4}{x^3-1}", (x**2 + 4) / (x**3 - 1), -oo),
    (r"\displaystyle\lim_{x\to\infty}\frac{1-4x^3}{2x^3+x}", (1 - 4 * x**3) / (2 * x**3 + x), oo),
    (r"\displaystyle\lim_{x\to\infty}\frac{x^3}{x^2+1}", x**3 / (x**2 + 1), oo),
    (r"\displaystyle\lim_{x\to\infty}\frac{\sqrt{9x^2+x}}{3x-1}", sp.sqrt(9 * x**2 + x) / (3 * x - 1), oo),
    (r"\displaystyle\lim_{x\to-\infty}\frac{\sqrt{9x^2+x}}{3x-1}", sp.sqrt(9 * x**2 + x) / (3 * x - 1), -oo),
    (r"\displaystyle\lim_{x\to\infty}(2 + 3e^{-x})", 2 + 3 * sp.exp(-x), oo),
    (r"\displaystyle\lim_{x\to\infty}\frac{\cos x}{x}", sp.cos(x) / x, oo),
]


def ans(v):
    return infinite(1) if v == oo else infinite(-1) if v == -oo else num(v)


SOL = [limchain(r"\infty", [r"\frac{7x-3}{2x+5}", r"\frac{7-\frac3x}{2+\frac5x}"], r"\frac72"), limchain(r"-\infty", [r"\frac{x^2+4}{x^3-1}", r"\frac{\frac1x+\frac4{x^3}}{1-\frac1{x^3}}"], 0), limchain(r"\infty", [r"\frac{1-4x^3}{2x^3+x}", r"\frac{\frac1{x^3}-4}{2+\frac1{x^2}}"], -2),
       r"Top degree bigger; the function grows without bound: $\infty$.", limchain(r"\infty", [r"\frac{3x\sqrt{1+\frac1{9x}}}{3x-1}", r"\frac{3\sqrt{1+\frac1{9x}}}{3-\frac1x}"], 1),
       r"For $x<0$, $\sqrt{9x^2} = -3x$, so the limit is $\dfrac{-3}{3} = -1$.", limchain(r"\infty", [r"(2+3e^{-x})"], r"2 + 3\cdot0 = 2"),
       r"$-\frac1x \le \frac{\cos x}{x} \le \frac1x$ for $x>0$; squeeze: $0$."]
PRACTICE = [Item(rf"Find ${tex}$.", ans(sp.limit(e, x, c)), sol, work="1.8cm") for (tex, e, c), sol in zip(P, SOL)]
PRACTICE += [
    Item(r"Find all horizontal asymptotes of $f(x) = \dfrac{2e^x}{e^x + 3}$. Enter the larger one's $y$-value.", num(2),
         r"As $x\to\infty$: $\dfrac{2}{1 + 3e^{-x}} \to 2$. As $x \to -\infty$: $e^x \to 0$, so $f \to 0$. Asymptotes $y = 0$ and $y = 2$.",
         work="2.4cm"),
    Item(r"A cooling cup of coffee has temperature $T(t) = 70 + 110e^{-0.1t}$ degrees after $t$ minutes. Find "
         r"$\displaystyle\lim_{t\to\infty} T(t)$ and interpret it.", num(70),
         r"$70^\circ$: in the long run, the coffee cools to room temperature, $70^\circ$F.", work="2cm"),
]
same("p9 +", sp.limit(2 * sp.exp(x) / (sp.exp(x) + 3), x, oo), 2)
same("p9 -", sp.limit(2 * sp.exp(x) / (sp.exp(x) + 3), x, -oo), 0)
t = sp.symbols("t")
same("p10", sp.limit(70 + 110 * sp.exp(-t / 10), t, oo), 70)

# extra practice (round 1)
INF, NINF = r"\infty", r"-\infty"
PRACTICE += [
    Item(r"Find $\displaystyle\lim_{x\to\infty}\frac{5x^2 - x}{3 - 2x^2}$.", num(sp.Rational(-5, 2)),
         limchain(INF, [r"\frac{5x^2-x}{3-2x^2}", r"\frac{5-\frac1x}{\frac3{x^2}-2}"], r"-\frac52"), work="1.8cm"),
    Item(r"Find $\displaystyle\lim_{x\to-\infty}\frac{4x + 1}{x^2 + 7}$.", num(0),
         limchain(NINF, [r"\frac{4x+1}{x^2+7}", r"\frac{\frac4x+\frac1{x^2}}{1+\frac7{x^2}}"], 0), work="1.8cm"),
    Item(r"Find $\displaystyle\lim_{x\to-\infty}\frac{x^2 - 3}{x + 1}$. Use $\infty$ or $-\infty$ if needed.", infinite(-1),
         r"The top degree is bigger, so the quotient is unbounded. For large negative $x$ the numerator is positive and the "
         r"denominator negative, so the limit is $-\infty$.", work="1.8cm"),
    Item(r"Find $\displaystyle\lim_{x\to\infty}\frac{\sqrt{4x^2 + 1}}{x + 5}$.", num(2),
         limchain(INF, [r"\frac{x\sqrt{4+\frac1{x^2}}}{x+5}", r"\frac{\sqrt{4+\frac1{x^2}}}{1+\frac5x}"], 2), work="2cm"),
    Item(r"Find $\displaystyle\lim_{x\to-\infty}\frac{\sqrt{4x^2 + 1}}{x + 5}$.", num(-2),
         r"For $x < 0$, $\sqrt{x^2} = -x$, so " +
         limchain(NINF, [r"\frac{-x\sqrt{4+\frac1{x^2}}}{x+5}", r"\frac{-\sqrt{4+\frac1{x^2}}}{1+\frac5x}"], -2) + ".",
         work="2cm"),
    Item(r"Find $\displaystyle\lim_{x\to\infty}\frac{\sin x}{x^2}$.", num(0),
         r"For $x > 0$, $-\frac1{x^2} \le \frac{\sin x}{x^2} \le \frac1{x^2}$, and both bounds approach $0$. "
         r"By the squeeze theorem the limit is $0$.", work="1.8cm"),
    Item(r"Find $\displaystyle\lim_{x\to\infty}\frac{3e^x}{e^x + 1}$.", num(3),
         limchain(INF, [r"\frac{3e^x}{e^x+1}", r"\frac{3}{1+e^{-x}}"], 3), work="1.8cm"),
    Item(r"Find $\displaystyle\lim_{x\to\infty}\frac{x^{2}}{e^{x}}$.", num(0),
         r"Exponentials grow faster than any power of $x$, so the denominator wins: $0$.", work="1.6cm"),
    Item(r"How many horizontal asymptotes does $f(x) = \dfrac{6x}{\sqrt{x^2 + 1}}$ have? Enter the count.", num(2),
         limchain(INF, [r"\frac{6x}{x\sqrt{1+\frac1{x^2}}}"], 6) + r" and, since $\sqrt{x^2} = -x$ for $x < 0$, "
         + limchain(NINF, [r"\frac{6x}{-x\sqrt{1+\frac1{x^2}}}"], -6) + r". Two asymptotes: $y = 6$ and $y = -6$.",
         work="2.4cm"),
    Item(r"A lake is stocked with fish, and the population after $t$ years is $P(t) = \dfrac{1200t + 300}{t + 2}$. Find "
         r"$\displaystyle\lim_{t\to\infty}P(t)$ and say what it means.", num(1200),
         limchain(INF, [r"\frac{1200t+300}{t+2}", r"\frac{1200+\frac{300}t}{1+\frac2t}"], 1200, var="t")
         + r". In the long run the population levels off near $1200$ fish.", work="2cm"),
]
t = sp.symbols("t")
for e, c, want in [((5 * x**2 - x) / (3 - 2 * x**2), oo, sp.Rational(-5, 2)), ((4 * x + 1) / (x**2 + 7), -oo, 0),
                   ((x**2 - 3) / (x + 1), -oo, -oo), (sp.sqrt(4 * x**2 + 1) / (x + 5), oo, 2),
                   (sp.sqrt(4 * x**2 + 1) / (x + 5), -oo, -2), (sp.sin(x) / x**2, oo, 0),
                   (3 * sp.exp(x) / (sp.exp(x) + 1), oo, 3), (x**2 / sp.exp(x), oo, 0),
                   (6 * x / sp.sqrt(x**2 + 1), oo, 6), (6 * x / sp.sqrt(x**2 + 1), -oo, -6)]:
    same("x1 " + str(e), sp.limit(e, x, c), want)
same("x1 fish", sp.limit((1200 * t + 300) / (t + 2), t, oo), 1200)

# ---------------------------------------------------------------- quiz
INF, NINF = r"\infty", r"-\infty"
QUIZ = [
    Variants(
        Item(r"Find $\displaystyle\lim_{x\to\infty}\frac{5x^2-x}{1-2x^2}$.", num(sp.Rational(-5, 2)),
             limchain(INF, [r"\frac{5-\frac1x}{\frac1{x^2}-2}"], r"-\frac52"), work="1.6cm"),
        Item(r"Find $\displaystyle\lim_{x\to\infty}\frac{6x^3+2}{3x^3-x}$.", num(2),
             limchain(INF, [r"\frac{6+\frac2{x^3}}{3-\frac1{x^2}}"], 2), work="1.6cm"),
        Item(r"Find $\displaystyle\lim_{x\to-\infty}\frac{4-7x}{2x+9}$.", num(sp.Rational(-7, 2)),
             limchain(NINF, [r"\frac{\frac4x-7}{2+\frac9x}"], r"-\frac72"), work="1.6cm"),
    ),
    Variants(
        Item(r"Find $\displaystyle\lim_{x\to-\infty}\frac{3x+1}{x^2+x+1}$.", num(0),
             limchain(NINF, [r"\frac{\frac3x+\frac1{x^2}}{1+\frac1x+\frac1{x^2}}"], 0), work="1.6cm"),
        Item(r"Find $\displaystyle\lim_{x\to\infty}\frac{10x}{x^3+2}$.", num(0),
             limchain(INF, [r"\frac{\frac{10}{x^2}}{1+\frac2{x^3}}"], 0), work="1.6cm"),
        Item(r"Find $\displaystyle\lim_{x\to\infty}\frac{\cos x}{x^2}$.", num(0),
             r"$-\frac1{x^2} \le \frac{\cos x}{x^2} \le \frac1{x^2}$ for $x \ne 0$, and both bounds head to $0$. By the squeeze theorem, $0$.",
             work="1.6cm"),
    ),
    Variants(
        Item(r"Find the horizontal asymptote of $y = \dfrac{8 - x}{2x + 3}$. Enter the $y$-value.", num(sp.Rational(-1, 2)),
             limchain(INF, [r"\frac{\frac8x-1}{2+\frac3x}"], r"-\frac12") + r", and the same at $-\infty$: $y = -\frac12$.", work="1.6cm"),
        Item(r"Find the horizontal asymptote of $y = \dfrac{3x^2}{x^2 + 4}$. Enter the $y$-value.", num(3),
             limchain(INF, [r"\frac{3}{1+\frac4{x^2}}"], 3) + r", and the same at $-\infty$: $y = 3$.", work="1.6cm"),
        Item(r"Find the horizontal asymptote of $y = 5 - 2e^{-x}$ as $x \to \infty$. Enter the $y$-value.", num(5),
             limchain(INF, [r"(5 - 2e^{-x})"], r"5 - 0 = 5"), work="1.6cm"),
    ),
    Variants(
        MCQ(r"Which function has no horizontal asymptote?",
            [r"$\dfrac{x}{x^2+1}$", r"$\dfrac{x^2}{x^2+1}$", r"$\dfrac{x^3}{x^2+1}$", r"$e^{-x^2}$"], "C",
            r"The top degree is bigger, so it is unbounded at both ends."),
        MCQ(r"Which function has two different horizontal asymptotes?",
            [r"$\dfrac{2x}{x+1}$", r"$\dfrac{2x}{\sqrt{x^2+1}}$", r"$\dfrac{2}{x^2+1}$", r"$2x + 1$"], "B",
            r"As $x \to \infty$ it heads to $2$; as $x \to -\infty$, $\sqrt{x^2} = -x$ and it heads to $-2$.",
            why_not={"A": "$y = 2$ at both ends", "C": "$y = 0$ at both ends", "D": "none at all"}),
        MCQ(r"$\displaystyle\lim_{x\to\infty} f(x) = 4$. Which is true?",
            [r"$f(x)$ never equals $4$.", r"$f$ has a vertical asymptote at $x = 4$.", r"$f(4)$ is large.", r"$y = 4$ is a horizontal asymptote of the graph."], "D",
            r"A finite limit at infinity gives a horizontal asymptote.",
            why_not={"A": "a graph can cross its horizontal asymptote", "B": "that would be a limit as $x \\to 4$"}),
    ),
    Variants(
        MCQ(r"$\displaystyle\lim_{x\to\infty}\frac{\sqrt{x^2+4}}{2x}$ is", [r"$\dfrac12$", r"$2$", r"$1$", r"$\infty$"], "A",
            limchain(INF, [r"\frac{x\sqrt{1+\frac4{x^2}}}{2x}", r"\frac{\sqrt{1+\frac4{x^2}}}{2}"], r"\frac12")),
        MCQ(r"$\displaystyle\lim_{x\to-\infty}\frac{\sqrt{9x^2+1}}{x}$ is", [r"$3$", r"$-3$", r"$9$", r"$0$"], "B",
            r"For $x < 0$, $\sqrt{9x^2} = -3x$, so " + limchain(NINF, [r"\frac{-3x\sqrt{1+\frac1{9x^2}}}{x}"], -3) + ".",
            why_not={"A": "that's the limit at $+\\infty$"}),
        MCQ(r"$\displaystyle\lim_{x\to\infty}\frac{e^x}{x^5}$ is", [r"$0$", r"$1$", r"$\infty$", r"$5$"], "C",
            r"Exponentials outgrow every power of $x$, so the quotient grows without bound.", why_not={"A": "that's $\\frac{x^5}{e^x}$"}),
    ),
]
same("q versions", [sp.limit((5 * x**2 - x) / (1 - 2 * x**2), x, sp.oo), sp.limit((6 * x**3 + 2) / (3 * x**3 - x), x, sp.oo),
                    sp.limit((4 - 7 * x) / (2 * x + 9), x, -sp.oo), sp.limit((3 * x + 1) / (x**2 + x + 1), x, -sp.oo),
                    sp.limit((8 - x) / (2 * x + 3), x, sp.oo), sp.limit(sp.sqrt(x**2 + 4) / (2 * x), x, sp.oo),
                    sp.limit(sp.sqrt(9 * x**2 + 1) / x, x, -sp.oo), sp.limit(2 * x / sp.sqrt(x**2 + 1), x, -sp.oo)],
     [sp.Rational(-5, 2), 2, sp.Rational(-7, 2), 0, sp.Rational(-1, 2), sp.Rational(1, 2), -3, -2])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$\displaystyle\lim_{x\to\infty}\frac{2x^3 + x - 1}{5 - 4x^3}$ is", [r"$\dfrac25$", r"$-\dfrac12$", r"$0$", r"$-\infty$"], "B",
        r"Equal degrees: $\dfrac{2}{-4}$.", why_not={"A": "used the constant terms"}),
    MCQ(r"The graph of $y = \dfrac{3e^x - 2}{e^x + 1}$ has which horizontal asymptotes?",
        [r"$y = 3$ only", r"$y = -2$ only", r"$y = 3$ and $y = -2$", r"$y = 1$ and $y = 3$"], "C",
        r"As $x\to\infty$: $3$. As $x\to-\infty$: $e^x \to 0$, giving $\dfrac{-2}{1} = -2$."),
    MCQ(r"$\displaystyle\lim_{x\to-\infty}\frac{\sqrt{x^2 + 3x}}{x}$ is", [r"$1$", r"$3$", r"$0$", r"$-1$"], "D",
        r"For $x < 0$, $\sqrt{x^2} = -x$, so the limit is $-1$.", why_not={"A": "treated $\\sqrt{x^2}$ as $x$"}),
    MCQ(r"Which is true about $f(x) = \dfrac{2x^2 - 8}{x^2 - 4x + 4}$?",
        [r"$y = 2$ is a horizontal asymptote and $x = 2$ is a vertical asymptote",
         r"$y = 2$ is a horizontal asymptote and there is a hole at $x = 2$",
         r"$y = -2$ is a horizontal asymptote", r"There are no asymptotes"], "A",
        r"$\dfrac{2(x-2)(x+2)}{(x-2)^2} = \dfrac{2(x+2)}{x-2}$: $x = 2$ remains in the denominator. Equal degrees give $y = 2$.",
        why_not={"B": "only one factor of $x - 2$ cancels"}),
]
same("m4 VA", sp.limit((2 * x**2 - 8) / (x**2 - 4 * x + 4), x, 2, "+"), oo)

FRQS = [
    FRQ("Long-run behavior", (
        r"The number of people who have heard a rumor $t$ days after it starts is modeled by $R(t) = \dfrac{600t^2}{t^2 + 50}$ "
        r"for $t \ge 0$."), [
        Part("a", r"Find $\displaystyle\lim_{t\to\infty} R(t)$.", num(600), r"Equal degrees: $\dfrac{600}{1} = 600$.",
             [(1, "answer $600$ with method")], work="2cm"),
        Part("b", r"Interpret your answer to part (a) in the context of the problem.", selfcheck(r"600\text{ people in the long run}"),
             r"In the long run, the number of people who have heard the rumor approaches 600.",
             [(1, "long run, number of people, 600")], work="1.8cm"),
        Part("c", r"Is $R(t)$ ever equal to $600$? Explain.", selfcheck(r"\text{No}"),
             r"No. $R(t) = 600\cdot\dfrac{t^2}{t^2+50} < 600$ because $t^2 < t^2 + 50$. The graph approaches $600$ but never reaches it.",
             [(1, "no, with an algebraic reason")], work="2cm"),
    ], frq_type="Limits in context"),
]
same("frq a", sp.limit(600 * t**2 / (t**2 + 50), t, oo), 600)

TOPIC = Topic(
    number="1.15", title="Connecting Limits at Infinity and Horizontal Asymptotes",
    unit="Unit 1: Limits and Continuity", ced=["LIM-2.D", "LIM-2.D.1", "LIM-2.D.2"],
    goals=r"Find limits at infinity by comparing dominant terms, and use them to identify horizontal asymptotes.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
