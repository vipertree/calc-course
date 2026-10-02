"""Topic 1.2: Defining limits and using limit notation.

CED: LIM-1.A (notation), LIM-1.B (interpret; multiple representations). Epsilon-delta is
excluded from the exam, so the "closeness game" appears only as an informal picture.
Running example matches the video: g(x) = (x^2 - 1)/(x - 1), a line with a hole at (1, 2).
"""
import sympy as sp

from calclib import (VideoExample, Variants, FRQ, MCQ, BigIdea, Check, Definition, Example, Formula, Item, Part, Section,
                     Table, Text, Topic, Video, close, num, same, selfcheck)
from calclib.figs import graph

x = sp.symbols("x")
G = (x**2 - 1) / (x - 1)
XS = [sp.Rational(9, 10), sp.Rational(99, 100), sp.Rational(999, 1000),
      sp.Rational(1001, 1000), sp.Rational(101, 100), sp.Rational(11, 10)]
for v in XS:
    same(f"g({v})", G.subs(x, v), v + 1)
same("lim g", sp.limit(G, x, 1), 2)


def dec(v):
    return f"{float(v):g}"


FIG_HOLE = graph("t1_2_hole", [("x+1", -1.5, 3.2)], xr=(-1.5, 3.5), yr=(-1, 4.5), open=[(1, 2)],
                 caption=r"$g(x) = \dfrac{x^2-1}{x-1}$: the line $y = x+1$ with a hole at $(1,2)$.")
FIG_MOVED = graph("t1_2_moved", [("x+1", -1.5, 3.2)], xr=(-1.5, 3.5), yr=(-1, 5.5), open=[(1, 2)], closed=[(1, 5)],
                  caption=r"$k(x)$: the same line, but $k(1) = 5$.")
FIG_EX = graph("t1_2_ex", [("0.5*(x-2)^2+3", -0.5, 4.5)], xr=(-0.5, 4.5), yr=(-0.5, 6), open=[(2, 3)], closed=[(2, 1)],
               caption=r"The graph of $f$.")

rows_x = " & ".join(f"${dec(v)}$" for v in XS)
rows_y = " & ".join(f"${dec(v + 1)}$" for v in XS)

NOTES = [
    Video("s1_2.py::Lesson", "Defining limits", 4),

    Section("Approaching a value"),
    Text(r"Let \[ g(x) = \frac{x^2-1}{x-1}. \] At $x = 1$ the formula gives \mblank{\tfrac00}, so $g(1)$ is "
         r"\blank{undefined}. The table shows what $g(x)$ does \emph{near} $x=1$."),
    Table(r"$x$ & " + rows_x + r" \\ $g(x)$ & " + rows_y, "c|cccccc"),
    FIG_HOLE,
    Text(r"As $x$ approaches $1$ from either side, $g(x)$ approaches \mblank{2}."),

    Section("The definition"),
    Definition("Limit (informal definition)", (
        r"Given a function $f$, the \textbf{limit of $f(x)$ as $x$ approaches $c$} is a real number $L$ if $f(x)$ "
        r"can be made \blank{arbitrarily close} to $L$ by taking $x$ \blank{sufficiently close} to $c$, "
        r"but \blank{not equal} to $c$.")),
    Formula("Limit notation", (
        r"\[ \lim_{x\to c} f(x) = L \]"
        r"Read: ``the limit of $f(x)$ as $x$ approaches $c$ is $L$.'' "
        r"For $g$ above: $\displaystyle \lim_{x\to 1}\frac{x^2-1}{x-1} = \mblank{2}$.\par "
        r"One-sided limits: $\displaystyle \lim_{x\to c^-} f(x)$ lets $x$ approach $c$ from the \blank{left} "
        r"(values less than $c$); $\displaystyle \lim_{x\to c^+} f(x)$ from the \blank{right}.")),
    Text(r"\textbf{The closeness game.} Someone draws a band around the height $L$, as thin as they like. If you can "
         r"always find a window around $c$ where the graph stays inside the band (ignoring $x=c$ itself), then the "
         r"limit is $L$. This game is the formal (epsilon-delta) definition of a limit. It is good to know the idea is airtight, "
         r"but the AP exam does not test it: an intuitive understanding of \emph{approaches} is all the exam needs."),

    Section("The limit ignores the point itself"),
    FIG_MOVED,
    Text(r"Here $k(1) = \mblank{5}$, but $\displaystyle\lim_{x\to1} k(x) = \mblank{2}$. "
         r"The value \emph{at} $c$ and the limit \emph{as $x$ approaches} $c$ answer different questions."),
    BigIdea(r"A limit describes where the outputs are heading, not where they end up. It never uses $f(c)$."),
    VideoExample('Reading a graph', work="2.2cm"),
    FIG_EX,

    Section("Translating between words and symbols"),
    VideoExample('Symbols to words', work="2cm"),
    VideoExample('Words to symbols', work="1.6cm"),
    Check(r"A function $k$ has $k(4) = -1$. As $x$ gets close to $4$ from either side, $k(x)$ gets close to $6$. "
          r"Find \[ \lim_{x\to4} k(x). \]", num(6),
          r"The limit depends only on values near $4$, not at $4$: \[ \lim_{x\to4}k(x) = 6. \]"),
]

# ---------------------------------------------------------------- practice
F5 = (x**2 - 9) / (x - 3)
F6 = (x**2 + x - 6) / (x - 2)
F9 = (sp.sqrt(x + 4) - 2) / x
same("p5", sp.limit(F5, x, 3), 6)
same("p6", sp.limit(F6, x, 2), 5)
same("p9", sp.limit(F9, x, 0), sp.Rational(1, 4))
P5X = [sp.Rational(29, 10), sp.Rational(299, 100), sp.Rational(301, 100), sp.Rational(31, 10)]
tab5 = (r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $x$ & " + " & ".join(dec(v) for v in P5X)
        + r" \\ \hline $f(x)$ & " + " & ".join(dec(F5.subs(x, v)) for v in P5X) + r"\end{tabular}}")
FIG_P = graph("t1_2_p3", [("-0.5*x+1.5", -4, 3.5)], xr=(-4, 3.5), yr=(-1, 5), open=[(-1, 2)], closed=[(-1, 4)],
              caption=r"The graph of $f$.")

PRACTICE = [
    Item(r"Explain in words what $\displaystyle\lim_{x\to 5} f(x) = -3$ means.",
         selfcheck(r"\text{As } x \text{ gets close to 5, } f(x) \text{ gets close to } -3"),
         r"As $x$ gets closer and closer to $5$ (from both sides, without equaling $5$), $f(x)$ gets closer and closer to $-3$.",
         work="1.8cm"),
    Item(r"Write in limit notation: ``As $t$ approaches $0$ from the right, $P(t)$ approaches $12$.''",
         selfcheck(r"\lim_{t\to0^+}P(t)=12"), r"$\displaystyle\lim_{t\to0^+} P(t) = 12$.", work="1.5cm"),
    Item(r"Use the graph of $f$ to find $\displaystyle\lim_{x\to -1} f(x)$.", num(2),
         r"Both sides of the graph head toward the hole at height $2$.", figure=FIG_P, work="1.5cm"),
    Item(r"Use the same graph to find $f(-1)$.", num(4), r"The filled dot is at height $4$.", work="1.2cm"),
    Item(r"Use the table to estimate $\displaystyle\lim_{x\to 3} f(x)$." + tab5, num(6),
         r"From both sides the outputs close in on $6$ ($5.9, 5.99$ and $6.01, 6.1$).", work="1.5cm"),
    Item(r"Let $g(x) = \dfrac{x^2+x-6}{x-2}$. Is $g(2)$ defined? Make a table with $x = 1.9, 1.99, 2.01, 2.1$ and "
         r"estimate $\displaystyle\lim_{x\to2} g(x)$.", num(5),
         r"$g(2) = \frac00$ is undefined. The table gives $4.9, 4.99, 5.01, 5.1$, so the limit is about $5$.",
         calc=True),
    Item(r"True or false: if $f(3) = 7$, then $\displaystyle\lim_{x\to3} f(x) = 7$. Explain.",
         selfcheck(r"\text{False}"),
         (r"False. The limit ignores the value at $3$. For example, $f(x) = x$ for $x \ne 3$ with $f(3) = 7$ has "
          r"limit $3$ at $x=3$."), work="2cm"),
    Item(r"$V(t)$ is the volume of water, in liters, in a tub $t$ minutes after the tap is opened. Interpret "
         r"$\displaystyle\lim_{t\to10} V(t) = 250$.",
         selfcheck(r"\text{Near } t=10\text{ min, volume near 250 L}"),
         r"As the time approaches 10 minutes, the volume of water in the tub approaches 250 liters.", work="1.8cm"),
    Item(r"Estimate $\displaystyle\lim_{x\to0}\frac{\sqrt{x+4}-2}{x}$ using a table with $x = \pm 0.1$, $\pm0.01$, "
         r"$\pm 0.001$.", num(sp.Rational(1, 4), tol=0.0005, display="0.25"),
         r"At $x = -0.1, -0.01, -0.001$ the values are $0.2516$, $0.25016$, $0.250016$; at $x = 0.1, 0.01, 0.001$ they "
         r"are $0.2485$, $0.24984$, $0.249984$. Both sides close in on $0.25$.",
         calc=True),
    Item(r"Sketch the graph of a function with $\displaystyle\lim_{x\to2} f(x) = 1$ and $f(2) = 3$.",
         selfcheck(r"\text{Graph through a hole at } (2,1) \text{ with a dot at } (2,3)"),
         r"Any graph that approaches height $1$ from both sides of $x=2$, with an open circle at $(2,1)$ and a filled dot at $(2,3)$.",
         work="3cm"),
]
close("p9 table -", F9.subs(x, sp.Rational(-1, 10)).evalf(), 0.2516, 1e-4)
close("p9 table +", F9.subs(x, sp.Rational(1, 10)).evalf(), 0.2485, 1e-4)

# extra practice (round 1)
FIG_P2 = graph("t1_2_p11", [("0.75*(x+1)^2-1", -3.5, 1), ("3-x", 1, 3.5)], xr=(-3.5, 3.5), yr=(-1.5, 4.5), open=[(1, 2)],
               closed=[(1, 4), (-1, -1)], caption=r"The graph of $g$.")
PRACTICE += [
    Item(r"Write in limit notation: ``As $x$ approaches $4$, $g(x)$ approaches $-2$.''", selfcheck(r"\lim_{x\to4}g(x)=-2"),
         r"$\displaystyle\lim_{x\to4} g(x) = -2$.", work="1.2cm"),
    Item(r"Use the graph of $g$ to find $\displaystyle\lim_{x\to1} g(x)$.", num(2),
         r"From the left, $0.75(x+1)^2 - 1$ heads to $2$; from the right, $3 - x$ heads to $2$. So $\displaystyle\lim_{x\to1}g(x) = 2$.",
         figure=FIG_P2, work="1.4cm"),
    Item(r"Using the same graph, find $g(1)$.", num(4), r"The filled dot at $x=1$ is at height $4$.", work="1cm"),
    Item(r"Using the same graph, find $\displaystyle\lim_{x\to-1} g(x)$.", num(-1),
         r"The graph is unbroken at $x = -1$ and passes through $(-1, -1)$, so the limit is $-1$.", work="1.2cm"),
    Item(r"Using the same graph, find $\displaystyle\lim_{x\to3} g(x)$.", num(0), r"Near $x=3$ the graph is $y = 3 - x$, heading to $0$.",
         work="1.2cm"),
    Item(r"Make a table with $x = 1.9, 1.99, 2.01, 2.1$ to estimate $\displaystyle\lim_{x\to2}\frac{x^2-4}{x-2}$.", num(4),
         r"The outputs are $3.9, 3.99, 4.01, 4.1$, heading to $4$.", calc=True, work="2cm"),
    Item(r"Make a table to estimate $\displaystyle\lim_{x\to1}\frac{x^3-1}{x-1}$.", num(3),
         r"At $x = 0.99$ and $1.01$ the outputs are $2.9701$ and $3.0301$, heading to $3$.", calc=True, work="2cm"),
    Item(r"True or false: if $\displaystyle\lim_{x\to2}f(x) = 6$, then $f(2)$ must be defined. Explain.", selfcheck(r"\text{False}"),
         r"False. A limit ignores the value at $2$; $f$ could have a hole there. For example, $\dfrac{x^2-4}{x-2}\cdot\frac32$ has limit $6$ "
         r"at $2$ but is undefined there.", work="1.8cm"),
    Item(r"$C(p)$ is the number of cups of lemonade sold per day when the price is $p$ dollars. Interpret "
         r"$\displaystyle\lim_{p\to2} C(p) = 140$.", selfcheck(r"\text{near \$2, about 140 cups per day}"),
         r"As the price gets closer and closer to \$2, the number of cups sold per day gets closer and closer to 140.", work="1.8cm"),
    Item(r"For the graph of $f$ in the notes (hole at $(2, 3)$, dot at $(2, 1)$), find $\displaystyle\lim_{x\to2}f(x) - f(2)$.", num(2),
         r"$3 - 1 = 2$.", work="1.2cm"),
]
same("p15 table", [(x**2 - 4) / (x - 2) for _ in [0]][0].subs(x, sp.Rational(199, 100)), sp.Rational(399, 100))
same("p16", sp.limit((x**3 - 1) / (x - 1), x, 1), 3)
same("fig g", [sp.limit(sp.Rational(3, 4) * (x + 1)**2 - 1, x, 1), sp.limit(3 - x, x, 1)], [2, 2])

# ---------------------------------------------------------------- quiz
FIG_Q = graph("t1_2_q1", [("0.4*(x-3)^2-1", -0.5, 6)], xr=(-0.5, 6), yr=(-2, 4), open=[(3, -1)], closed=[(3, 2)],
              caption=r"The graph of $f$.")
HQ = sp.log(x) / (x**2 - 1)
QX = [sp.Rational(9, 10), sp.Rational(99, 100), sp.Rational(101, 100), sp.Rational(11, 10)]
tabq = (r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $x$ & " + " & ".join(dec(v) for v in QX)
        + r" \\ \hline $h(x)$ & " + " & ".join(f"{float(HQ.subs(x, v)):.4f}" for v in QX) + r"\end{tabular}}")
same("q4", sp.limit(HQ, x, 1), sp.Rational(1, 2))
FIG_Q2 = graph("t1_2_q2", [("3-0.5*(x-2)^2", -1, 5)], xr=(-1, 5), yr=(-2, 4), open=[(2, 3)], closed=[(2, 1)],
               caption=r"The graph of $f$.")
FIG_Q3 = graph("t1_2_q3", [("sqrt(x+1)", -1, 6)], xr=(-1, 6), yr=(-1, 5), open=[(3, 2)], closed=[(3, 4)], samples=200,
               caption=r"The graph of $f$.")


def table(expr, xs, name="h"):
    return (r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $x$ & " + " & ".join(dec(v) for v in xs)
            + rf" \\ \hline ${name}(x)$ & " + " & ".join(f"{float(expr.subs(x, v)):.4f}" for v in xs) + r"\end{tabular}}")


H2, X2 = (x**3 - 8) / (x - 2), [sp.Rational(19, 10), sp.Rational(199, 100), sp.Rational(201, 100), sp.Rational(21, 10)]
H3, X3 = (sp.exp(x) - 1) / x, [sp.Rational(-1, 10), sp.Rational(-1, 100), sp.Rational(1, 100), sp.Rational(1, 10)]
same("q4 versions", [sp.limit(H2, x, 2), sp.limit(H3, x, 0)], [12, 1])
MUST = {"A": "the value at the point can be anything, or undefined", "B": "the function may be defined there",
        "D": "outputs approach the limit; they need not equal it"}
QUIZ = [
    Variants(
        Item(r"Use the graph of $f$ to find $\displaystyle\lim_{x\to3} f(x)$.", num(-1),
             r"Both sides approach the open circle at height $-1$.", figure=FIG_Q, work="1.2cm"),
        Item(r"Use the graph of $f$ to find $\displaystyle\lim_{x\to2} f(x)$.", num(3),
             r"Both sides approach the open circle at height $3$. The filled dot below it doesn't matter.", figure=FIG_Q2, work="1.2cm"),
        Item(r"Use the graph of $f$ to find $\displaystyle\lim_{x\to3} f(x)$.", num(2),
             r"Both sides approach the open circle at height $2$. The filled dot above it doesn't matter.", figure=FIG_Q3, work="1.2cm"),
    ),
    Variants(
        Item(r"Use the graph of $f$ to find $f(3)$.", num(2), r"The filled dot is at height $2$.", figure=FIG_Q, work="1.2cm"),
        Item(r"Use the graph of $f$ to find $f(2)$.", num(1), r"The filled dot is at height $1$.", figure=FIG_Q2, work="1.2cm"),
        Item(r"Use the graph of $f$ to find $f(3)$.", num(4), r"The filled dot is at height $4$.", figure=FIG_Q3, work="1.2cm"),
    ),
    Variants(
        MCQ(r"Which statement is the meaning of $\displaystyle\lim_{x\to4} g(x) = 9$?",
            [r"$g(4) = 9$.", r"As $x$ gets close to $4$, $g(x)$ gets close to $9$.",
             r"As $x$ gets close to $9$, $g(x)$ gets close to $4$.", r"$g(x)$ is never equal to $9$."], "B",
            r"The number under the arrow is the input $x$ approaches; the number on the right is where the outputs head.",
            why_not={"A": "the limit does not tell you the value at $4$", "C": "the input and output are reversed"}),
        MCQ(r"Which statement is the meaning of $\displaystyle\lim_{t\to-1} p(t) = 6$?",
            [r"As $t$ gets close to $6$, $p(t)$ gets close to $-1$.", r"$p(-1) = 6$.", r"$p(t)$ is never equal to $6$.",
             r"As $t$ gets close to $-1$, $p(t)$ gets close to $6$."], "D",
            r"The input $t$ heads to $-1$; the outputs head to $6$.",
            why_not={"B": "the limit does not tell you the value at $-1$", "A": "the input and output are reversed"}),
        MCQ(r"A sentence says: ``As $x$ approaches $0$, $r(x)$ approaches $-2$.'' Which is the same statement?",
            [r"$\displaystyle\lim_{x\to0} r(x) = -2$", r"$r(0) = -2$", r"$\displaystyle\lim_{x\to-2} r(x) = 0$", r"$r(-2) = 0$"], "A",
            r"What $x$ approaches goes under the arrow; where the outputs head goes on the right.",
            why_not={"B": "that is a value, not a limit", "C": "the input and output are reversed"}),
    ),
    Variants(
        Item(r"Use the table to estimate $\displaystyle\lim_{x\to1} h(x)$." + tabq, num(sp.Rational(1, 2), tol=0.01, display="0.5"),
             r"The outputs close in on $0.5$ from both sides.", work="1.2cm"),
        Item(r"Use the table to estimate $\displaystyle\lim_{x\to2} h(x)$." + table(H2, X2), num(12, tol=0.05, display="12"),
             r"The outputs close in on $12$ from both sides.", work="1.2cm"),
        Item(r"Use the table to estimate $\displaystyle\lim_{x\to0} h(x)$." + table(H3, X3), num(1, tol=0.01, display="1"),
             r"The outputs close in on $1$ from both sides.", work="1.2cm"),
    ),
    Variants(
        MCQ(r"A function satisfies $\displaystyle\lim_{x\to2} f(x) = 5$. Which must be true?",
            [r"$f(2) = 5$", r"$f(2)$ is undefined", r"$f(1.999)$ is close to $5$", r"$f(x) = 5$ for all $x$ near $2$"], "C",
            r"The limit only promises outputs close to $5$ for inputs close to $2$. It says nothing about $f(2)$ itself.", why_not=MUST),
        MCQ(r"A function satisfies $\displaystyle\lim_{x\to-3} g(x) = 1$. Which must be true?",
            [r"$g(-3) = 1$", r"$g(-3)$ is undefined", r"$g(x) = 1$ for all $x$ near $-3$", r"$g(-2.999)$ is close to $1$"], "D",
            r"Inputs close to $-3$ give outputs close to $1$. Nothing is promised about $g(-3)$ itself.",
            why_not={"A": MUST["A"], "B": MUST["B"], "C": MUST["D"]}),
        MCQ(r"$k(5) = 8$ and $\displaystyle\lim_{x\to5} k(x) = 2$. Which is true?",
            [r"This is impossible.", r"The graph of $k$ has a point at $(5, 8)$, and the graph heads to height $2$ near $x = 5$.",
             r"$k(4.999)$ is close to $8$.", r"$k(5)$ must equal $2$."], "B",
            r"The value and the limit answer different questions, so they can differ: a filled dot at $(5, 8)$ above a hole at $(5, 2)$.",
            why_not={"A": "the value and the limit can differ", "C": "near $5$, outputs are close to the limit, $2$",
                     "D": MUST["A"]}),
    ),
]

# ---------------------------------------------------------------- test prep
FIG_M1 = graph("t1_2_m1", [("0.5*x+2", -1, 2), ("-x+5", 2, 5)], xr=(-1, 5), yr=(-0.5, 4.5), open=[(2, 3)],
               closed=[(2, 1)], caption=r"The graph of $f$.")
M2X = [sp.Rational(19, 10), sp.Rational(199, 100), sp.Rational(201, 100), sp.Rational(21, 10)]
M2F = x**2 + x - 1   # values 4.51, 4.9501, 5.0501, 5.51 -> limit 5
tabm2 = (r"\par\centerline{\begin{tabular}{c|cccc} $x$ & " + " & ".join(dec(v) for v in M2X)
         + r" \\ \hline $f(x)$ & " + " & ".join(f"{float(M2F.subs(x, v)):.4f}" for v in M2X) + r"\end{tabular}}")
same("m2", M2F.subs(x, 2), 5)
same("m3", sp.limit((sp.exp(x) - 1) / x, x, 0), 1)
MCQS = [
    MCQ(r"The graph of $f$ is shown. Which statement is true?",
        [r"$\displaystyle\lim_{x\to2} f(x) = 1$", r"$\displaystyle\lim_{x\to2} f(x) = 3$",
         r"$\displaystyle\lim_{x\to2} f(x)$ does not exist", r"$\displaystyle\lim_{x\to2} f(x) = f(2)$"], "B",
        r"From the left, $0.5x+2$ approaches $3$; from the right, $-x+5$ approaches $3$. Both sides agree on $3$.",
        why_not={"A": "that is $f(2)$, the filled dot", "C": "the two sides agree, so the limit exists",
                 "D": "$f(2) = 1$, which is not the limit"}, figure=FIG_M1),
    MCQ(r"Selected values of $f$ are shown." + tabm2 + r"Which is the best estimate of $\displaystyle\lim_{x\to2} f(x)$?",
        [r"$4.95$", r"$5.05$", r"$5$", r"The limit does not exist."], "C",
        r"Values from the left ($4.51$, $4.95$) and right ($5.51$, $5.05$) close in on $5$.",
        why_not={"A": "used only the left side", "B": "used only the right side"}),
    MCQ(r"Using values of $x$ close to $0$, what is $\displaystyle\lim_{x\to0}\frac{e^x-1}{x}$?",
        [r"$1$", r"$0$", r"$e$", r"It does not exist."], "A",
        r"At $x = \pm0.001$ the quotient is $1.0005$ and $0.9995$, closing in on $1$.",
        why_not={"B": "treated $\\frac00$ as $0$", "D": "stopped at $\\frac00$"}, calc=True),
    MCQ(r"The amount of water in a reservoir is $W(t)$ million gallons at time $t$ days. What does "
        r"$\displaystyle\lim_{t\to6} W(t) = 40$ mean?",
        [r"On day 6 the reservoir holds exactly 40 million gallons.",
         r"The reservoir gains 40 million gallons per day near day 6.",
         r"After 40 days, the reservoir holds 6 million gallons.",
         r"As time approaches day 6, the amount of water approaches 40 million gallons."], "D",
        r"The limit describes where the amount is heading as $t$ nears $6$.",
        why_not={"A": "the limit does not guarantee the value at $t=6$", "B": "this describes a rate, not the amount",
                 "C": "input and output are reversed"}),
]

F_FRQ = (x**3 - 8) / (x - 2)
FX = [sp.Rational(19, 10), sp.Rational(199, 100), sp.Rational(201, 100), sp.Rational(21, 10)]
same("frq lim", sp.limit(F_FRQ, x, 2), 12)
tabf = (r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $x$ & " + " & ".join(dec(v) for v in FX)
        + r" \\ \hline $f(x)$ & " + " & ".join(f"{float(F_FRQ.subs(x, v)):g}" for v in FX) + r"\end{tabular}}")
FRQS = [
    FRQ("Estimating a limit", (
        r"The function $f$ is defined by $f(x) = \dfrac{x^3 - 8}{x - 2}$ for $x \neq 2$. Selected values are shown." + tabf), [
        Part("a", r"Explain why $f(2)$ is not defined by the formula.", selfcheck(r"\tfrac00"),
             r"Substituting $x = 2$ gives $\dfrac{8-8}{2-2} = \dfrac00$, which is undefined.",
             [(1, "shows the substitution gives $\\frac00$ (division by zero)")], work="1.8cm"),
        Part("b", r"Use the table to estimate $\displaystyle\lim_{x\to 2} f(x)$. Explain how the table supports your answer.",
             num(12), r"As $x$ approaches $2$ from the left the values ($11.41$, $11.9401$) and from the right "
                      r"($12.0601$, $12.61$) close in on $12$.",
             [(1, "estimate $12$"), (1, "refers to values from both sides approaching $12$")], work="2.5cm"),
        Part("c", r"A new function $g$ equals $f$ for $x \ne 2$ and $g(2) = 0$. Find $\displaystyle\lim_{x\to2} g(x)$ "
                  r"and explain why $g(2)$ does not affect it.", num(12),
             r"$\displaystyle\lim_{x\to2}g(x) = 12$. A limit uses only values of $x$ near $2$, never $x=2$ itself, and "
             r"$g$ agrees with $f$ there.",
             [(1, "limit $12$ with a reason about values near, not at, $x=2$")], work="2cm"),
    ], frq_type="Limits from a table"),
]

TOPIC = Topic(
    number="1.2", title="Defining Limits and Using Limit Notation",
    unit="Unit 1: Limits and Continuity", ced=["LIM-1.A", "LIM-1.A.1", "LIM-1.B", "LIM-1.B.1"],
    goals=r"Read and write limit notation, and explain what a limit says (and doesn't say) about a function.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
