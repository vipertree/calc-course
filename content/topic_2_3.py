"""Topic 2.3: Estimating derivatives of a function at a point.

CED: CHA-2.C (derivative at a point estimated from tables, graphs, technology). The weather
table in the notes matches the video: T'(6) is about (66 - 63)/(7 - 5) = 1.5 degrees per hour.
"""
import sympy as sp

from calclib import (Variants, FRQ, MCQ, BigIdea, Check, Desmos, Example, Formula, Item, Part, Section, Table, Text,
                     Topic, Video, VideoExample, check, close, num, same, selfcheck)
from calclib.figs import graph

x, h = sp.symbols("x h")
same("T'(6)", sp.Rational(66 - 63, 7 - 5), sp.Rational(3, 2))

FIG_TAN = graph("t2_3_tan", [("0.25*(x-1)^2+1", -0.5, 5.5), ("x-1", 0.6, 5.4, "dashed")], xr=(-0.5, 5.5), yr=(-0.5, 6),
                closed=[(3, 2), (1, 0), (5, 4)], labels=[(3, 2, "above left", r"$(3, f(3))$")], w="6.4cm", h="4.8cm",
                caption=r"The tangent line at $x = 3$ passes through the grid points $(1, 0)$ and $(5, 4)$.")
same("fig tangent slope", sp.diff(sp.Rational(1, 4) * (x - 1)**2 + 1, x).subs(x, 3), 1)

NOTES = [
    Video("s2_3.py::Lesson", "Estimating derivatives", 3),

    Section("From a table"),
    Table(r"$t$ (hours) & 0 & 2 & 5 & 7 & 10 \\ $T(t)$ ($^\circ$F) & 48 & 55 & 63 & 66 & 64", "c|ccccc"),
    Text(r"To estimate $T'(6)$, use the data \blank{closest} to $t = 6$ on each side: "
         r"\[ T'(6) \approx \frac{T(7) - T(5)}{7 - 5} = \mblank{1.5} \] \blank{degrees per hour}."),
    Formula("Estimating $f'(c)$ from data", (
        r"Pick data points close to $c$, on one side of $c$ or on both sides, and use their average rate of change:"
        r"\[ f'(c) \approx \frac{f(b) - f(a)}{b - a}. \]"
        r"The average rate of change (a \blank{secant} slope) is your \textbf{estimate} of the instantaneous rate of change (a \blank{tangent} slope).")),
    VideoExample("Only one side", work="2cm"),

    Section("From a graph"),
    FIG_TAN,
    Text(r"Draw the tangent line at the point and pick two points on the \blank{tangent line} (not the curve) that are easy to read. "
         r"Here $\displaystyle f'(3) \approx \frac{4 - 0}{5 - 1} = \mblank{1}$. A wide run between the two points makes the reading more accurate."),

    Section("With technology"),
    Desmos("A numerical derivative", r"Desmos computes derivatives numerically. Change $a$ to see $f'(a)$ for $f(x) = x^3$.",
           [{"id": "f", "latex": r"f(x)=x^{3}", "color": "#2d70b3"},
            {"id": "a", "latex": r"a=1.5", "sliderBounds": {"min": "-2", "max": "2", "step": "0.1"}},
            {"id": "m", "latex": r"m=f'(a)"},
            {"id": "tan", "latex": r"y=f(a)+m(x-a)", "color": "#c74440"},
            {"id": "P", "latex": r"(a,f(a))", "color": "#000000"}],
           {"left": -3, "right": 3, "bottom": -8, "top": 8}),
    Text(r"A calculator can be fooled at a corner. For $|x|$ at $x = 0$, the average rate of change from $x = -0.001$ to $x = 0.001$ is \mblank{0}, "
         r"but $|x|$ has no tangent line at $0$. Topic 2.4 explains when a derivative fails to exist."),
    BigIdea(r"Without a formula, a derivative is estimated by a secant slope over the smallest interval the data allow, with units "
            r"of output per input."),
    Check(r"The temperature table again: \par\smallskip\centerline{\begin{tabular}{c|ccccc} $t$ (hours) & 0 & 2 & 5 & 7 & 10 \\ \hline $T(t)$ ($^\circ$F) & 48 & 55 & 63 & 66 & 64\end{tabular}} \par Estimate $T'(1)$.", num(sp.Rational(7, 2)),
          r"\[ \frac{T(2) - T(0)}{2 - 0} = \frac{55 - 48}{2} = 3.5 \] degrees per hour."),
]
same("T'(10)", sp.Rational(64 - 66, 3), sp.Rational(-2, 3))
same("abs centered", (abs(sp.Symbol("h", positive=True)) - abs(-sp.Symbol("h", positive=True))) / 2, 0)

# ---------------------------------------------------------------- practice
TAB = (r"\par\smallskip\centerline{\begin{tabular}{c|cccccc} $x$ & 0 & 1 & 3 & 4 & 6 & 9 \\ \hline "
       r"$g(x)$ & 12 & 10 & 7 & 7 & 9 & 15\end{tabular}}")
PRACTICE = [
    Item(r"Values of a differentiable function $g$ are shown." + TAB + r"\par Estimate $g'(2)$.", num(sp.Rational(-3, 2)),
         r"$\dfrac{g(3) - g(1)}{3 - 1} = \dfrac{7 - 10}{2} = -1.5$.", work="1.6cm"),
    Item(r"Using the same table, estimate $g'(5)$.", num(1), r"$\dfrac{g(6) - g(4)}{6 - 4} = \dfrac{9 - 7}{2} = 1$.", work="1.6cm"),
    Item(r"Using the same table, estimate $g'(7.5)$.", num(2), r"$\dfrac{g(9) - g(6)}{9 - 6} = \dfrac{15 - 9}{3} = 2$.", work="1.6cm"),
    Item(r"Using the same table, estimate $g'(3.5)$. What does your estimate suggest about the graph of $g$ near $x = 3.5$?",
         num(0), r"$\dfrac{7 - 7}{1} = 0$: the tangent line is nearly horizontal there.", work="1.8cm"),
    Item(r"For $f(x) = 2^x$, compute the average rate of change on $[-0.01, 0.01]$, $\dfrac{f(0.01) - f(-0.01)}{0.02}$, to estimate $f'(0)$. "
         r"Round to four decimal places.", num(sp.Rational(6932, 10000), tol=0.00006, display="0.6932"),
         r"$\dfrac{2^{0.01} - 2^{-0.01}}{0.02} \approx 0.6932$. (The exact value is $\ln 2 \approx 0.6931$.)", calc=True, work="1.8cm"),
    Item(r"Use a calculator to find $f'(1)$ for $f(x) = \sin(x^2)$, to three decimal places.",
         num(2 * sp.cos(1), tol=0.0006, display=r"\approx 1.081"), r"A numerical derivative gives about $1.081$.", calc=True,
         work="1.4cm"),
    Item(r"A graph of $h$ has a tangent line at $x = -1$ that passes through $(-3, 5)$ and $(1, -3)$. Estimate $h'(-1)$.", num(-2),
         r"$\dfrac{-3 - 5}{1 - (-3)} = \dfrac{-8}{4} = -2$.", work="1.4cm"),
    Item(r"A calculator reports that the derivative of $|x - 2|$ at $x = 2$ is $0$. Explain why this is misleading.",
         selfcheck(r"\text{corner: no tangent line}"),
         r"The graph has a corner at $x = 2$: slope $-1$ on the left and $1$ on the right. There is no tangent line, so the "
         r"derivative does not exist; a calculator using points on both sides averages $-1$ and $1$ to get $0$.", work="2.2cm"),
    Item(r"$D(t)$ is the depth of snow, in inches, $t$ hours after midnight. $D(4) = 6.2$ and $D(5) = 7.0$. Estimate $D'(4.5)$ and "
         r"interpret it with units.", num(sp.Rational(4, 5), tol=0.001, display=r"0.8\text{ in/hr}"),
         r"$\dfrac{7.0 - 6.2}{1} = 0.8$. At 4:30 AM the snow depth is increasing at about 0.8 inches per hour.", work="2cm"),
]
close("p5", (2**0.01 - 2**-0.01) / 0.02, 0.6932, 6e-5)
close("p6", 2 * sp.cos(1), 1.0806, 1e-4)

# extra practice (round 1)
TAB2 = (r"\par\smallskip\centerline{\begin{tabular}{c|ccccc} $t$ (min) & 0 & 4 & 10 & 12 & 20 \\ \hline "
        r"$R(t)$ (gal/min) & 30 & 26 & 20 & 17 & 5\end{tabular}}")
RT = {0: 30, 4: 26, 10: 20, 12: 17, 20: 5}
PX = -sp.Rational(1, 2) * (x - 2)**2 + sp.Rational(9, 2)
FIG_P = graph("t2_3_px", [("-0.5*(x-2)^2+4.5", -0.5, 4.8), ("-x+7", 1.6, 5.4, "dashed")], xr=(-0.5, 5.5), yr=(-0.5, 5.5),
              closed=[(3, 4), (2, 5), (5, 2)], w="6cm", h="4.6cm",
              caption=r"The graph of $p$ (solid) and its tangent line at $x = 3$ (dashed).")
same("x1 fig tangent", [PX.subs(x, 3), sp.diff(PX, x).subs(x, 3)], [4, -1])
PRACTICE += [
    Item(r"Water drains from a tank at a rate $R(t)$, shown in the table." + TAB2 + r"\par Estimate $R'(11)$. Include units.",
         num(sp.Rational(-3, 2), display=r"-1.5\ \text{gal/min}^2"),
         rf"$\dfrac{{R(12) - R(10)}}{{12 - 10}} = \dfrac{{{RT[12]} - {RT[10]}}}{{2}} = -1.5$ gallons per minute per minute.",
         work="1.8cm"),
    Item(r"Using the same table, estimate $R'(2)$.", num(-1),
         rf"$\dfrac{{R(4) - R(0)}}{{4 - 0}} = \dfrac{{{RT[4]} - {RT[0]}}}{{4}} = -1$.", work="1.6cm"),
    Item(r"Using the same table, estimate $R'(16)$, and say in words what it means.", num(sp.Rational(-3, 2)),
         rf"$\dfrac{{R(20) - R(12)}}{{20 - 12}} = \dfrac{{{RT[20]} - {RT[12]}}}{{8}} = -1.5$. At $t = 16$ the draining rate is "
         r"dropping by about $1.5$ gallons per minute, each minute.", work="2cm"),
    Item(r"Using the same table, estimate $R'(10)$ with the nearest data point on each side of $t = 10$.",
         num(sp.Rational(-9, 8)),
         rf"$\dfrac{{R(12) - R(4)}}{{12 - 4}} = \dfrac{{{RT[12]} - {RT[4]}}}{{8}} = -\dfrac98$.", work="1.8cm"),
    Item(r"Use the graph to find $p'(3)$.", num(-1),
         r"The tangent line at $x = 3$ passes through $(2, 5)$ and $(5, 2)$, so its slope is $\dfrac{2 - 5}{5 - 2} = -1$.",
         figure=FIG_P, work="1.4cm"),
    Item(r"For $f(x) = \ln x$, compute $\dfrac{f(1.01) - f(0.99)}{0.02}$ to estimate $f'(1)$. Round to four decimal places.",
         num(1, tol=0.00006, display="1.0000"),
         r"$\dfrac{\ln 1.01 - \ln 0.99}{0.02} \approx 1.0000$. So the slope of $\ln x$ at $x = 1$ is about $1$.",
         calc=True, work="1.8cm"),
    Item(r"Use a calculator to find $f'(0.5)$ for $f(x) = xe^{-x}$, to three decimal places.",
         num(sp.Rational(1, 2) * sp.exp(-sp.Rational(1, 2)), tol=0.0006, display=r"\approx 0.303"),
         r"A numerical derivative gives about $0.303$.", calc=True, work="1.4cm"),
    Item(r"$k(1.9) = 3.61$, $k(2) = 4$ and $k(2.1) = 4.41$. Estimate $k'(2)$ using the points on both sides of $x = 2$.", num(4),
         r"$\dfrac{4.41 - 3.61}{2.1 - 1.9} = \dfrac{0.8}{0.2} = 4$.", work="1.6cm"),
    Item(r"$A(t)$ is the area of an oil spill, in square meters, $t$ hours after a leak starts. $A(2) = 150$ and $A(4) = 230$. "
         r"Estimate $A'(3)$ and interpret it with units.", num(40, display=r"40\ \text{m}^2\text{/hr}"),
         r"$\dfrac{230 - 150}{4 - 2} = 40$. Three hours after the leak starts, the spill is growing by about $40$ square meters "
         r"per hour.", work="2cm"),
    Item(r"For $f(x) = \sqrt[3]{x}$, compute the average rate of change from $x = -0.001$ to $x = 0.001$. What happens as the interval shrinks, and what "
         r"does that say about $f'(0)$?", selfcheck(r"\text{grows without bound; } f'(0) \text{ does not exist}"),
         r"It is $\dfrac{0.1 - (-0.1)}{0.002} = 100$, and it keeps growing as the interval shrinks. The tangent "
         r"line at $x = 0$ is vertical, so $f'(0)$ does not exist.", calc=True, work="2.2cm"),
]
same("x1 R", [sp.Rational(17 - 20, 2), sp.Rational(26 - 30, 4), sp.Rational(5 - 17, 8), sp.Rational(17 - 26, 8)],
     [sp.Rational(-3, 2), -1, sp.Rational(-3, 2), sp.Rational(-9, 8)])
close("x1 ln", (sp.log(1.01) - sp.log(0.99)) / 0.02, 1.0000, 6e-5)
close("x1 xe", sp.diff(x * sp.exp(-x), x).subs(x, 0.5), 0.3033, 1e-4)
same("x1 k", (sp.Rational(441, 100) - sp.Rational(361, 100)) / sp.Rational(2, 10), 4)
same("x1 A", sp.Rational(230 - 150, 2), 40)
close("x1 cbrt", (0.001**(1 / 3) * 2) / 0.002, 100, 1e-6)

# ---------------------------------------------------------------- quiz
TW = (r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $t$ & 0 & 3 & 5 & 8 \\ \hline $W(t)$ & 20 & 29 & 33 & 30\end{tabular}}")
TQ = (r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $x$ & 1 & 2 & 6 & 7 \\ \hline $q(x)$ & 10 & 16 & 4 & 1\end{tabular}}")
TK = (r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $t$ & 0 & 4 & 6 & 10 \\ \hline $K(t)$ & 3 & 11 & 20 & 12\end{tabular}}")
QUIZ = [
    Variants(
        Item(r"Values of $W$ are shown." + TW + r"\par Estimate $W'(4)$.", num(2), r"$\dfrac{33 - 29}{5 - 3} = 2$.", work="1.6cm"),
        Item(r"Values of $q$ are shown." + TQ + r"\par Estimate $q'(4)$.", num(-3), r"$\dfrac{4 - 16}{6 - 2} = -3$.", work="1.6cm"),
        Item(r"Values of $K$ are shown." + TK + r"\par Estimate $K'(5)$.", num(sp.Rational(9, 2)), r"$\dfrac{20 - 11}{6 - 4} = 4.5$.", work="1.6cm"),
    ),
    Variants(
        Item(r"Values of $W$ are shown." + TW + r"\par Estimate $W'(7)$.", num(-1), r"$\dfrac{30 - 33}{8 - 5} = -1$.", work="1.6cm"),
        Item(r"Values of $q$ are shown." + TQ + r"\par Estimate $q'(1.5)$.", num(6), r"$\dfrac{16 - 10}{2 - 1} = 6$.", work="1.6cm"),
        Item(r"Values of $K$ are shown." + TK + r"\par Estimate $K'(8)$.", num(-2), r"$\dfrac{12 - 20}{10 - 6} = -2$.", work="1.6cm"),
    ),
    Variants(
        MCQ(r"A table gives $f(x)$ at $x = 1, 4, 6, 9$. Which gives the best estimate of $f'(5)$?",
            [r"$\dfrac{f(9) - f(1)}{8}$", r"$\dfrac{f(6) - f(4)}{2}$", r"$\dfrac{f(9) - f(6)}{3}$", r"$\dfrac{f(4) - f(1)}{3}$"], "B",
            r"Use the data points closest to $5$: $x = 4$ and $x = 6$.",
            why_not={"A": "points far from 5 give a poor estimate", "C": "both points are past 5, and not the closest", "D": "both points are before 5, and not the closest"}),
        MCQ(r"A table gives $f$ at $x = 1, 3, 4, 8$. Which quotient gives the best estimate of $f'(3.5)$?",
            [r"$\dfrac{f(8) - f(1)}{7}$", r"$\dfrac{f(4) - f(1)}{3}$", r"$\dfrac{f(4) - f(3)}{1}$", r"$\dfrac{f(8) - f(3)}{5}$"], "C",
            r"Use the closest data on each side of $3.5$: $x = 3$ and $x = 4$.", why_not={"A": "far too wide"}),
        MCQ(r"A calculator reports the derivative of $|x - 1|$ at $x = 1$ as $0$. What is true?",
            [r"The derivative is $0$.", r"The derivative is $1$.", r"The graph has a corner at $x = 1$, so the derivative does not exist.",
             r"The derivative is $-1$."], "C", r"The left slope is $-1$ and the right slope is $1$. Points on both sides average them to $0$, which is misleading."),
    ),
    Variants(
        Item(r"A tangent line to the graph of $f$ at $x = 2$ passes through $(0, 1)$ and $(4, 7)$. Estimate $f'(2)$.",
             num(sp.Rational(3, 2)), r"$\dfrac{7 - 1}{4 - 0} = 1.5$.", work="1.4cm"),
        Item(r"A tangent line to the graph of $g$ at $x = -1$ passes through $(-3, 4)$ and $(1, -2)$. Estimate $g'(-1)$.",
             num(sp.Rational(-3, 2)), r"$\dfrac{-2 - 4}{1 - (-3)} = -1.5$.", work="1.4cm"),
        Item(r"A tangent line to the graph of $h$ at $x = 5$ passes through $(2, 3)$ and $(8, 5)$. Estimate $h'(5)$.",
             num(sp.Rational(1, 3)), r"$\dfrac{5 - 3}{8 - 2} = \dfrac13$.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"$R(t)$ gallons per minute is the rate water flows into a pool. $R(10) = 42$ and $R(12) = 45$. The best estimate of $R'(11)$ "
            r"and its units are", [r"$1.5$ gallons per minute", r"$1.5$ gallons per minute per minute", r"$3$ gallons",
                                   r"$43.5$ gallons per minute"], "B",
            r"$\dfrac{45 - 42}{2} = 1.5$. $R$ is already a rate, so $R'$ has units of gallons per minute per minute.",
            why_not={"A": "units of $R$, not $R'$", "D": "averaged the values"}),
        MCQ(r"$H(t)$ is a plant's height in centimeters after $t$ days. $H(6) = 14$ and $H(10) = 22$. The best estimate of $H'(8)$ and "
            r"its units are", [r"$2$ cm", r"$18$ cm per day", r"$8$ cm per day", r"$2$ cm per day"], "D",
            r"$\dfrac{22 - 14}{10 - 6} = 2$ centimeters per day.", why_not={"B": "averaged the values", "C": "forgot to divide by 4"}),
        MCQ(r"$v(t)$ is a car's velocity in meters per second. $v(3) = 12$ and $v(5) = 20$. The best estimate of $v'(4)$ and its units are",
            [r"$4$ m/s per second", r"$4$ m/s", r"$8$ m/s per second", r"$16$ m"], "A",
            r"$\dfrac{20 - 12}{5 - 3} = 4$ meters per second, per second: an acceleration.", why_not={"B": "units of $v$, not $v'$", "C": "forgot to divide by 2"}),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"The table gives values of a differentiable function $f$."
        r"\par\centerline{\begin{tabular}{c|ccccc} $x$ & 1.0 & 1.2 & 1.4 & 1.6 & 1.8 \\ \hline $f(x)$ & 3.0 & 3.5 & 3.9 & 4.2 & 4.4\end{tabular}}"
        r"\par Which is the best estimate of $f'(1.5)$?", [r"$1.5$", r"$0.3$", r"$4.05$", r"$3$"], "A",
        r"$\dfrac{4.2 - 3.9}{0.2} = 1.5$.", why_not={"B": "forgot to divide by $0.2$", "C": "averaged the $f$ values"}),
    MCQ(r"If $f(x) = x^3 - x$, which is closest to $\dfrac{f(2.01) - f(1.99)}{0.02}$?", [r"$6$", r"$11$", r"$12$", r"$0.22$"], "B",
        r"It approximates $f'(2) = 3(4) - 1 = 11$. (Exactly $11.0001$.)", why_not={"C": "forgot the $-x$ term"}),
    MCQ(r"The graph of $g$ has a sharp corner at $x = 3$. Which is true?",
        [r"$g'(3) = 0$", r"$g(3)$ does not exist", r"$g$ is not continuous at $x = 3$", r"$g'(3)$ does not exist"], "D",
        r"A corner has no single tangent line.", why_not={"A": "a calculator using points on both sides can suggest this, wrongly"}),
    MCQ(r"A student estimates $f'(4)$ using $f(3.9) = 2.73$ and $f(4.1) = 2.81$. The estimate is", [r"$0.08$", r"$0.8$", r"$0.4$", r"$0.04$"], "C",
        r"$\dfrac{2.81 - 2.73}{0.2} = 0.4$.", why_not={"A": "forgot to divide", "B": "divided by $0.1$"}),
]
close("m2", ((2.01**3 - 2.01) - (1.99**3 - 1.99)) / 0.02, 11.0001, 1e-6)

FRQS = [
    FRQ("A rising balloon", (
        r"The height of a hot-air balloon is modeled by a differentiable function $H$, where $H(t)$ is measured in feet and $t$ "
        r"is measured in minutes. Selected values of $H(t)$ are given in the table."
        r"\par\smallskip\centerline{\begin{tabular}{c|ccccc} $t$ (minutes) & 0 & 2 & 5 & 7 & 10 \\ \hline "
        r"$H(t)$ (feet) & 0 & 140 & 410 & 520 & 610\end{tabular}}"), [
        Part("a", r"Use the data in the table to estimate $H'(6)$. Show the work that leads to your answer. Indicate units of measure.",
             num(55, display=r"55\ \text{feet per minute}"),
             r"$H'(6) \approx \dfrac{H(7) - H(5)}{7 - 5} = \dfrac{520 - 410}{2} = 55$ feet per minute.",
             [(1, "difference quotient with $H(7)$ and $H(5)$, and the answer"), (1, "units")], work="2.6cm"),
        Part("b", r"Using correct units, interpret the meaning of $H'(6)$ in the context of the problem.",
             selfcheck(r"\text{At } t = 6\text{, the height is increasing about 55 feet per minute}"),
             r"At time $t = 6$ minutes, the height of the balloon is increasing at a rate of about $55$ feet per minute.",
             [(1, "rate of change of height, at $t=6$, with units")], work="2cm"),
        Part("c", r"Must there be a value $c$, for $0 < c < 10$, such that $H(c) = 500$? Justify your answer.",
             selfcheck(r"\text{Yes}"),
             r"$H$ is differentiable, so $H$ is continuous on $0 \le t \le 10$. $H(5) = 410 < 500 < 520 = H(7)$. By the Intermediate "
             r"Value Theorem, there must be a value $c$, with $5 < c < 7$, such that $H(c) = 500$.",
             [(1, "$H$ is continuous because it is differentiable"), (1, "$H(5) < 500 < H(7)$ and yes, by the Intermediate Value Theorem")],
             work="2.8cm"),
    ], frq_type="Table"),
]
same("frq a", sp.Rational(520 - 410, 7 - 5), 55)
check("frq c", 410 < 500 < 520)

TOPIC = Topic(
    number="2.3", title="Estimating Derivatives of a Function at a Point",
    unit="Unit 2: Differentiation", ced=["CHA-2.C"],
    goals=r"Estimate derivatives at a point from tables, graphs and technology, and interpret the estimates with units.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
