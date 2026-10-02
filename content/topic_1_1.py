"""Topic 1.1: Introducing calculus: can change occur at an instant?

CED: CHA-1.A (rate of change at an instant from average rates over intervals),
CHA-1.A.1-3. Opens with Zeno's arrow (Aristotle, Physics VI.9). Running example matches the
video: the arrow's distance s(t) = 60t - 12t^2 meters (a strongly slowed arrow, so the graph visibly curves; Adder asked
for a curve over realism); average velocity on [1, 2] is 24 m/s and averages on shrinking intervals close in on 36 m/s. Adder's rule: 1.1 does NOT resolve Zeno. It estimates, notes that an
average over any interval says nothing about the instant itself, and only hints at limits. Unit 2 resolves it.
"""
import sympy as sp

from calclib import (VideoExample, Variants, FRQ, MCQ, BigIdea, Check, Definition, Desmos, Example, Formula, Item, Part, Section,
                     Table, Text, Topic, Video, close, expr, num, same, selfcheck)
from calclib.figs import graph

t, d, x, h = sp.symbols("t d x h")
S = sp.Lambda(t, 60 * t - 12 * t**2)


def avg(f, a, b):
    return (f(b) - f(a)) / (b - a)


same("s(1), s(2)", [S(1), S(2)], [48, 72])
same("avg [1,2]", avg(S, 1, 2), 24)
same("avg [1,1+d]", sp.simplify(avg(S, 1, 1 + d)), 36 - 12 * d)
ROWS = [(1, 24), (sp.Rational(1, 2), 30), (sp.Rational(1, 10), sp.Rational(174, 5)), (sp.Rational(1, 100), sp.Rational(897, 25)),
        (sp.Rational(1, 1000), sp.Rational(8997, 250)), (sp.Rational(-1, 10), sp.Rational(186, 5)), (sp.Rational(-1, 100), sp.Rational(903, 25))]
for dv, want in ROWS:
    same(f"avg dt={dv}", avg(S, 1, 1 + dv), want)
same("limit", sp.limit(avg(S, 1, 1 + d), d, 0), 36)


def dec(v):
    v = sp.nsimplify(v)
    return str(int(v)) if v.is_Integer else f"{float(v):g}"


FIG = graph("t1_1_arrow", [("60*x-12*x^2", 0, 2.5), ("48+24*(x-1)", 0.4, 2.5, "dashed")], xr=(0, 2.7), yr=(0, 90),
            closed=[(1, 48), (2, 72)], xstep=0.5, ystep=20, w="7.6cm", h="5.6cm", xlabel="t", ylabel="s(t)",
            labels=[(1, 48, "above left", r"$(1, 48)$"), (2, 72, "below right", r"$(2, 72)$")],
            caption=r"The arrow's distance, $s(t) = 60t - 12t^2$. The dashed secant line joins $t = 1$ and $t = 2$.")

rows = " \\\\ ".join(f"${dec(dv)}$ & $[{dec(min(1, 1 + dv))},\\ {dec(max(1, 1 + dv))}]$ & ${dec(want)}$"
                     for dv, want in ROWS)

ZENO = (r"``If everything when it occupies an equal space is at rest, and if that which is in locomotion is always occupying "
        r"such a space at any moment, the flying arrow is therefore motionless.'' \par "
        r"\hfill{\small Aristotle, \emph{Physics} VI.9, describing Zeno's argument (trans. Hardie and Gaye)}")

NOTES = [
    Video("s1_1.py::Lesson", "Zeno's arrow", 5.5),

    Section("Zeno's arrow"),
    Text(ZENO),
    Text(r"Zeno's point: at any single instant, the arrow occupies one position and has no time to move. A photograph "
         r"shows \emph{where} the arrow is, not \emph{how fast} it is going. To measure speed you need \blank{two} moments."),

    Section("Average rate of change"),
    Text(r"An arrow's distance from the bow after $t$ seconds is $s(t) = 60t - 12t^2$ meters, for $0 \le t \le 2.5$. It slows down as it flies."),
    Text(r"\textbf{Reading the graph.} The graph below is \emph{not} the arrow's path through the air. The arrow flies in an arc, "
         r"but $s(t)$ only tracks its distance from the bow along the ground. That distance is on the vertical axis; "
         r"the horizontal axis is \blank{time}."),
    Formula("Average rate of change", (
        r"The average rate of change of $f$ over the interval $[a, b]$ is"
        r"\[ \frac{\Delta f}{\Delta x} = \frac{f(b)-f(a)}{b-a}. \]"
        r"For position, this is the \blank{average velocity}. Its units are output units per input unit. On a graph it is the "
        r"slope of the \blank{secant} line through $\bigl(a, f(a)\bigr)$ and $\bigl(b, f(b)\bigr)$.")),
    Text(r"You may know secant lines from geometry: a secant of a circle is a line through two of its points. "
         r"In calculus the idea is the same for any curve: a line through two points on the graph."),
    FIG,
    VideoExample('Two average velocities', work="3cm"),

    Section("Shrinking the interval"),
    Text(r"To learn about the velocity at the single instant $t = 1$, use intervals $[1, 1 + \Delta t]$ with $\Delta t$ getting smaller. "
         r"A negative $\Delta t$ puts the second time \emph{before} $t = 1$."),
    Table(rows, "ccc", header=r"$\Delta t$ & interval & average velocity (m/s)"),
    Desmos("Shrink the interval", r"Drag the slider for $\Delta t$ toward $0$ from both sides and watch the average velocity.",
           [{"id": "s", "latex": r"s(t)=60t-12t^{2}", "color": "#2d70b3"},
            {"id": "d", "latex": r"d=1", "sliderBounds": {"min": "-0.9", "max": "1.4", "step": "0.001"}},
            {"id": "m", "latex": r"m=\frac{s(1+d)-s(1)}{d}"},
            {"id": "sec", "latex": r"y=s(1)+m(x-1)", "color": "#c98a00", "lineStyle": "DASHED"},
            {"id": "P", "latex": r"(1,s(1))", "color": "#000000"},
            {"id": "Q", "latex": r"(1+d,s(1+d))", "color": "#000000"}],
           {"left": -0.3, "right": 2.8, "bottom": -5, "top": 90}),
    Text(r"From both sides, the average velocities close in on \blank{$36$} m/s."),

    Section("Why not an interval of length zero?"),
    Text(r"If $\Delta t = 0$, both times are the same: \[ \frac{s(1)-s(1)}{1-1} = \frac{0}{0}, \] which is \blank{undefined}. "
         r"The average rate of change cannot be computed at a single point. This is Zeno's paradox written as arithmetic."),
    Text(r"Every number in the table is an average over an \blank{interval} of time, and during every one of those intervals the "
         r"arrow moves. Shorter intervals give better and better \blank{estimates}, but even a very short interval is not a "
         r"single instant."),
    BigIdea(r"The open question: can there be a rate of change at a single instant, when nothing changes during that instant? "
            r"The averages close in on one number. Whether that number deserves to be called the arrow's velocity at $t = 1$ is "
            r"the question calculus was invented to answer. This unit builds the tool it needs, called a \emph{limit}."),

    Section("Estimating a rate from data"),
    VideoExample('A sprinter', work="2.6cm"),
    Check(r"Find the arrow's average velocity on $[2, 2.1]$, $[2, 2.01]$ and $[2, 2.001]$. What number do the averages close in on?",
          num(12, display=r"12\text{ m/s}"),
          (r"\[ \frac{s(2.1)-s(2)}{0.1} = \frac{73.08-72}{0.1} = 10.8 \] m/s. The shorter intervals give $11.88$ and $11.988$. "
           r"The averages close in on $12$ m/s.")),
]
same("check", avg(S, 2, sp.Rational(21, 10)), sp.Rational(108, 10))
same("check 0.01", avg(S, 2, sp.Rational(201, 100)), sp.Rational(1188, 100))
same("check lim", sp.limit(avg(S, 2, 2 + d), d, 0), 12)

# ---------------------------------------------------------------- practice (20)
B = sp.Lambda(t, 48 * t - 16 * t**2)
POP = (r"\par\smallskip\centerline{\begin{tabular}{c|ccccc} $t$ & 0 & 2 & 5 & 8 & 10 \\ \hline "
       r"$P(t)$ & 12.0 & 12.6 & 13.5 & 14.1 & 14.6\end{tabular}}")
TANK = (r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $t$ (min) & 0 & 5 & 10 & 15 \\ \hline "
        r"$V(t)$ (L) & 200 & 170 & 150 & 140\end{tabular}}")
PRACTICE = [
    Item(r"Find the average rate of change of $f(x) = x^2 + 1$ on $[1, 4]$.", num(5), r"$\dfrac{f(4)-f(1)}{4-1} = \dfrac{17-2}{3} = 5$."),
    Item(r"Find the average rate of change of $g(x) = \sqrt{x}$ on $[4, 9]$.", num(sp.Rational(1, 5)), r"$\dfrac{3-2}{9-4} = \dfrac15$."),
    Item(r"Find the average rate of change of $h(x) = \dfrac1x$ on $[1, 4]$.", num(sp.Rational(-1, 4)),
         r"$\dfrac{\frac14 - 1}{4 - 1} = \dfrac{-\frac34}{3} = -\dfrac14$."),
    Item(r"Find the average rate of change of $k(x) = x^3 - x$ on $[-1, 2]$.", num(2), r"$\dfrac{6 - 0}{2 - (-1)} = 2$."),
    Item(r"The population of a town, $P(t)$ thousand people, $t$ years after 2020:" + POP +
         r"\par Find the average rate of change of $P$ from $t = 2$ to $t = 8$. Include units.",
         num(sp.Rational(1, 4), tol=0.0005, display=r"0.25\text{ thousand people per year}"),
         r"$\dfrac{14.1-12.6}{8-2} = 0.25$ thousand people per year, or 250 people per year."),
    Item(r"Using the population table, estimate how fast the population was growing at $t = 5$.", num(sp.Rational(1, 4), tol=0.0005),
         r"Use an interval from the table with $t = 5$ in the middle: $[2, 8]$ gives $0.25$ thousand people per year."),
    Item(r"Using the population table, find the average rate of change of $P$ over the whole decade, $[0, 10]$.",
         num(sp.Rational(26, 100), tol=0.0005), r"$\dfrac{14.6 - 12.0}{10} = 0.26$ thousand people per year."),
    Item(r"A ball is thrown upward; its height is $b(t) = 48t - 16t^2$ feet. Compute its average velocity on $[1, 1+\Delta t]$ for "
         r"$\Delta t = 0.1$, $0.01$ and $-0.01$. What value do the averages close in on?",
         num(16, display=r"16\text{ ft/s}"),
         r"$14.4$, $15.84$ and $16.16$. The averages close in on $16$ ft/s from both sides."),
    Item(r"For the ball in Problem 8, find the average velocity on $[1, 3]$. What does the sign tell you?", num(-16),
         r"$\dfrac{b(3)-b(1)}{2} = \dfrac{0-32}{2} = -16$ ft/s. The ball ends lower than it started, so its net motion is downward."),
    Item(r"For the arrow, $s(t) = 60t - 12t^2$, find the average velocity on $[0.5, 1.5]$.", num(36),
         r"$\dfrac{s(1.5)-s(0.5)}{1} = \dfrac{63 - 27}{1} = 36$ m/s."),
    Item(r"For the arrow, write the average velocity on $[2, 2 + h]$ as a simplified expression in $h$ ($h \ne 0$).",
         expr("12-12*h", var="h"),
         r"$\dfrac{60(2+h) - 12(2+h)^2 - 72}{h} = \dfrac{12h - 12h^2}{h} = 12 - 12h$."),
    Item(r"Use Problem 11: evaluate $12 - 12h$ for $h = 0.1$, $0.01$ and $0.001$. What value do the averages close in on?", num(12),
         r"$10.8$, $11.88$, $11.988$. As $h$ gets smaller, $12 - 12h$ gets closer to $12$ m/s."),
    Item(r"Kiri says, ``To find the speed at exactly $t = 3$, just use the interval $[3, 3]$.'' Explain what goes wrong and what to do instead.",
         selfcheck(r"\tfrac00\text{; shrink intervals toward } t=3"),
         r"On $[3, 3]$ the average rate is $\dfrac{f(3)-f(3)}{3-3} = \dfrac00$, which is undefined. Instead, compute average rates on "
         r"shorter and shorter intervals containing $t = 3$ and find the value they approach.", work="2.5cm"),
    Item(r"For $f(x) = \dfrac1x$, write the average rate of change on $[1, 1+h]$ as a simplified expression in $h$.",
         expr("-1/(1+h)", var="h"), r"$\dfrac{\frac{1}{1+h} - 1}{h} = \dfrac{-h}{h(1+h)} = -\dfrac{1}{1+h}$ for $h \ne 0$."),
    Item(r"Use Problem 14 to estimate the rate of change of $f(x) = \dfrac1x$ at $x = 1$: what value does $-\dfrac{1}{1+h}$ "
         r"close in on as $h$ gets small?", num(-1),
         r"At $h = 0.01$ it is $-\frac{1}{1.01} \approx -0.990$; at $h = -0.01$ it is $-\frac{1}{0.99} \approx -1.010$. "
         r"The values close in on $-1$."),
    Item(r"For $f(x) = x^2$, simplify the average rate of change on $[3, 3 + h]$.", expr("6+h", var="h"),
         r"$\dfrac{(3+h)^2 - 9}{h} = \dfrac{6h + h^2}{h} = 6 + h$ for $h \ne 0$."),
    Item(r"Use Problem 16 to estimate the rate of change of $f(x) = x^2$ at $x = 3$.", num(6),
         r"$6 + h$ is $6.1$ at $h = 0.1$ and $5.99$ at $h = -0.01$. The averages close in on $6$."),
    Item(r"Let $f(x) = 2^x$. Find the average rate of change of $f$ on $[0, 0.001]$, rounded to three decimal places.",
         num(sp.Float("0.693387", 10), tol=0.0006, display="0.693"),
         r"$\dfrac{2^{0.001}-2^0}{0.001} \approx 0.693$. (This number returns in Unit 2.)", calc=True),
    Item(r"Water drains from a tank. $V(t)$ is the volume in liters after $t$ minutes." + TANK +
         r"\par Find the average rate of change of $V$ over $5 \le t \le 15$, with units.", num(-3, display=r"-3\text{ L/min}"),
         r"$\dfrac{140 - 170}{15 - 5} = -3$ liters per minute."),
    Item(r"Zeno argued that a flying arrow is motionless at every instant. Explain why computing average velocities over "
         r"shorter and shorter intervals does not, by itself, answer him.", selfcheck(r"\text{each average is about an interval}"),
         r"Every average velocity is computed over an interval of time, and the arrow moves during that interval. However short "
         r"the interval, it is still not a single instant. The averages close in on one number, but we have not yet said why that "
         r"number should count as a velocity at an instant.", work="2.5cm"),
]
same("p3", avg(sp.Lambda(x, 1 / x), 1, 4), sp.Rational(-1, 4))
same("p4", avg(sp.Lambda(x, x**3 - x), -1, 2), 2)
same("p7", sp.Rational(146 - 120, 100), sp.Rational(26, 100))
for dv, want in [(sp.Rational(1, 10), sp.Rational(72, 5)), (sp.Rational(1, 100), sp.Rational(396, 25)), (sp.Rational(-1, 100), sp.Rational(404, 25))]:
    same(f"p8 {dv}", avg(B, 1, 1 + dv), want)
same("p9", avg(B, 1, 3), -16)
same("p10", avg(S, sp.Rational(1, 2), sp.Rational(3, 2)), 36)
same("p11", sp.simplify(avg(S, 2, 2 + h)), 12 - 12 * h)
same("p14", sp.simplify((1 / (1 + h) - 1) / h), -1 / (1 + h))
same("p16", sp.simplify(((3 + h)**2 - 9) / h), 6 + h)
close("p18", (2**0.001 - 1) / 0.001, 0.693387, 1e-5)

# ---------------------------------------------------------------- quiz
# Each slot has three versions. The web draws one per slot; paper forms A, B, C take versions 1, 2, 3.
WHY_ZERO = {"C": "the numerator is $0$ but so is the denominator, and $\\frac00$ has no value"}
QUIZ = [
    Variants(
        Item(r"Find the average rate of change of $f(x) = x^3$ on $[1, 3]$.", num(13), r"$\dfrac{27-1}{2} = 13$.", work="2cm"),
        Item(r"Find the average rate of change of $f(x) = x^2 - 2x$ on $[0, 4]$.", num(2), r"$\dfrac{f(4)-f(0)}{4-0} = \dfrac{8-0}{4} = 2$.",
             work="2cm"),
        Item(r"Find the average rate of change of $f(x) = 2x^3$ on $[0, 2]$.", num(8), r"$\dfrac{f(2)-f(0)}{2-0} = \dfrac{16-0}{2} = 8$.",
             work="2cm"),
    ),
    Variants(
        Item(r"A tank holds $V(t)$ gallons after $t$ minutes, with $V(0) = 40$ and $V(6) = 19$. Find the average rate of change of $V$ "
             r"on $[0, 6]$, with units.", num(sp.Rational(-7, 2), display=r"-3.5\text{ gal/min}"), r"$\dfrac{19-40}{6} = -3.5$ gallons per minute.",
             work="2cm"),
        Item(r"A pool holds $P(t)$ gallons $t$ hours after it starts draining, with $P(2) = 500$ and $P(10) = 260$. Find the average "
             r"rate of change of $P$ on $[2, 10]$, with units.", num(-30, display=r"-30\text{ gal/hr}"),
             r"$\dfrac{260-500}{10-2} = -30$ gallons per hour.", work="2cm"),
        Item(r"The temperature outside is $T(t)$ degrees Fahrenheit $t$ hours after sunrise, with $T(1) = 58$ and $T(5) = 74$. Find the "
             r"average rate of change of $T$ on $[1, 5]$, with units.", num(4, display=r"4\ ^\circ\text{F/hr}"),
             r"$\dfrac{74-58}{5-1} = 4$ degrees per hour.", work="2cm"),
    ),
    Variants(
        MCQ(r"Why can't the average rate of change formula be used on the interval $[2, 2]$?",
            [r"The function might not be defined at $2$.", r"It requires dividing by $2 - 2 = 0$.", r"The answer is always $0$.",
             r"Average rates only work for linear functions."], "B", r"The formula divides by $b - a$, which is $0$ here, giving $\frac00$.",
            why_not=WHY_ZERO),
        MCQ(r"A student tries to find a car's speed at exactly $t = 5$ by computing its average velocity on $[5, 5]$. What goes wrong?",
            [r"Average velocity can't be negative.", r"The answer is always $0$.", r"It requires dividing by $5 - 5 = 0$.",
             r"The interval is too long."], "C", r"The change in time is $0$, so the quotient is $\frac00$, which has no value.",
            why_not={"B": WHY_ZERO["C"]}),
        MCQ(r"Which is the best way to estimate a rate of change at the single input $x = 3$?",
            [r"Compute average rates on $[3, 3 + h]$ for smaller and smaller $h$.", r"Compute $\dfrac{f(3)}{3}$.",
             r"Compute $\dfrac{f(3) - f(3)}{3 - 3}$.", r"Compute the average rate of change on $[0, 3]$."], "A",
            r"Shorter intervals containing $x = 3$ give better and better estimates.",
            why_not={"C": "that is $\\frac00$", "D": "a long interval gives a rough average", "B": "this ratio is not a rate of change"}),
    ),
    Variants(
        Item(r"An object's position is $s(t) = 5t^2$ meters. Write its average velocity on $[2, 2+h]$ as a simplified expression in $h$ ($h \neq 0$).",
             expr("20+5*h", var="h"), r"$\dfrac{5(2+h)^2 - 20}{h} = \dfrac{20h + 5h^2}{h} = 20 + 5h$.", work="3cm"),
        Item(r"An object's position is $s(t) = 3t^2$ meters. Write its average velocity on $[1, 1+h]$ as a simplified expression in $h$ ($h \neq 0$).",
             expr("6+3*h", var="h"), r"$\dfrac{3(1+h)^2 - 3}{h} = \dfrac{6h + 3h^2}{h} = 6 + 3h$.", work="3cm"),
        Item(r"An object's position is $s(t) = t^2 + 4t$ meters. Write its average velocity on $[3, 3+h]$ as a simplified expression in $h$ "
             r"($h \neq 0$).", expr("10+h", var="h"),
             r"$\dfrac{(3+h)^2 + 4(3+h) - 21}{h} = \dfrac{10h + h^2}{h} = 10 + h$.", work="3cm"),
    ),
    Variants(
        Item(r"For $h \ne 0$, an object's average velocity on $[2, 2+h]$ is $20 + 5h$ meters per second. What value do the averages close "
             r"in on as $h$ gets close to $0$?", num(20, display=r"20\text{ m/s}"),
             r"$20 + 5h$ is $20.5$ at $h = 0.1$ and $20.05$ at $h = 0.01$. It closes in on $20$ m/s.", work="1.5cm"),
        Item(r"For $h \ne 0$, a cyclist's average velocity on $[4, 4+h]$ is $12 - 2h$ meters per second. What value do the averages close "
             r"in on as $h$ gets close to $0$?", num(12, display=r"12\text{ m/s}"),
             r"$12 - 2h$ is $11.8$ at $h = 0.1$ and $12.02$ at $h = -0.01$. It closes in on $12$ m/s.", work="1.5cm"),
        Item(r"For $h \ne 0$, a drone's average climbing rate on $[1, 1+h]$ is $7 + h - h^2$ meters per second. What value do the averages "
             r"close in on as $h$ gets close to $0$?", num(7, display=r"7\text{ m/s}"),
             r"When $h$ is small, $h$ and $h^2$ are small, so $7 + h - h^2$ is close to $7$ m/s.", work="1.5cm"),
    ),
]
S6 = sp.Lambda(t, 5 * t**2)
same("q4", sp.simplify(avg(S6, 2, 2 + h)), 20 + 5 * h)
same("q1 versions", [avg(sp.Lambda(x, x**3), 1, 3), avg(sp.Lambda(x, x**2 - 2 * x), 0, 4), avg(sp.Lambda(x, 2 * x**3), 0, 2)], [13, 2, 8])
same("q4 versions", [sp.simplify(avg(sp.Lambda(t, 3 * t**2), 1, 1 + h)), sp.simplify(avg(sp.Lambda(t, t**2 + 4 * t), 3, 3 + h))],
     [6 + 3 * h, 10 + h])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"A particle's position is $s(t) = t^2 + 2t$. What is its average velocity on $1 \le t \le 4$?", [r"$3$", r"$7$", r"$8$", r"$21$"], "B",
        r"$s(4) = 24$ and $s(1) = 3$, so $\dfrac{24-3}{4-1} = 7$.",
        why_not={"A": "divided $21$ by $7$ instead of by $3$", "C": "the velocity at the instant $t=3$, not the average",
                 "D": "forgot to divide by the length of the interval"}),
    MCQ(r"The temperature $T(t)$ of an oven, in $^\circ$F, is recorded every 2 minutes."
        r"\par\centerline{\begin{tabular}{c|ccccc} $t$ (min) & 0 & 2 & 4 & 6 & 8 \\ \hline $T(t)$ & 50 & 56 & 65 & 71 & 74\end{tabular}}"
        r"\par What is the average rate of change of $T$ over $2 \le t \le 6$?",
        [r"$3$ $^\circ$F/min", r"$3.25$ $^\circ$F/min", r"$3.75$ $^\circ$F/min", r"$15$ $^\circ$F/min"], "C",
        r"$\dfrac{T(6)-T(2)}{6-2} = \dfrac{71-56}{4} = 3.75$ degrees per minute.",
        why_not={"A": "used $[0,8]$", "B": "used $[0,4]$", "D": "forgot to divide by $4$"}),
    MCQ(r"Which is the best way to estimate the rate of change of $f$ at the single input $x = 3$?",
        [r"Compute $\dfrac{f(3)-f(3)}{3-3}$.", r"Compute the average rate of change of $f$ on $[0, 3]$.", r"Compute $\dfrac{f(3)}{3}$.",
         r"Compute average rates of change on $[3, 3+h]$ for smaller and smaller $h$ and see what value they close in on."], "D",
        r"Shorter intervals containing $x = 3$ give better and better estimates.",
        why_not={"A": "that is $\\frac00$", "B": "a fixed interval gives an average", "C": "this ratio is not a rate of change"}),
    MCQ(r"For $h \ne 0$, the average velocity of a cart on $[2, 2+h]$ is $6 + 3h - h^2$ meters per second. What value do the "
        r"average velocities close in on as $h$ gets close to $0$?", [r"$6$ m/s", r"$0$ m/s", r"$8$ m/s", r"It cannot be determined."], "A",
        r"When $h$ is small, $3h$ and $h^2$ are small, so $6 + 3h - h^2$ is close to $6$.", why_not={"C": "substituted $h = 1$"}),
]
same("m1", avg(sp.Lambda(t, t**2 + 2 * t), 1, 4), 7)

FRQS = [
    FRQ("Filling a tank", (
        r"Water flows into a tank. The amount of water in the tank, $W(t)$ gallons, is recorded at selected times $t$, in minutes."
        r"\par\smallskip\centerline{\begin{tabular}{c|ccccc} $t$ (min) & 0 & 4 & 6 & 10 & 12 \\ \hline "
        r"$W(t)$ (gal) & 5 & 17 & 24 & 40 & 49\end{tabular}}"), [
        Part("a", r"Find the average rate of change of $W$ over $0 \le t \le 12$. Include units.",
             num(sp.Rational(11, 3), tol=0.005, display=r"\tfrac{11}{3}\approx 3.667\text{ gal/min}"),
             r"$\dfrac{W(12)-W(0)}{12-0} = \dfrac{49-5}{12} = \dfrac{11}{3} \approx 3.667$ gallons per minute.",
             [(1, "difference quotient with correct values"), (1, "value with units")], work="3cm"),
        Part("b", r"Use the data to estimate the rate at which the amount of water is changing at $t = 8$ minutes. Show the computation "
                  r"that leads to your answer.", num(4, display=r"4\text{ gal/min}"),
             r"$\dfrac{W(10)-W(6)}{10-6} = \dfrac{40-24}{4} = 4$ gallons per minute.",
             [(1, "difference quotient using $t=6$ and $t=10$"), (1, "value $4$")], work="3cm"),
        Part("c", r"Explain why the interval $[8, 8]$ cannot be used to find the rate at $t = 8$ exactly. Describe what additional data "
                  r"would give a better estimate.", selfcheck(r"\tfrac00\text{; measurements closer to } t=8"),
             r"The average rate on $[8,8]$ is $\frac00$, which is undefined. Measurements closer to $t = 8$ on both sides (such as "
             r"$t = 7.5$ and $t = 8.5$) would give a shorter interval and a better estimate.",
             [(1, "explains $\\frac00$ and names a shorter interval containing $8$")], work="2.5cm"),
    ], frq_type="Table of values / rates"),
]

TOPIC = Topic(
    number="1.1", title="Can Change Occur at an Instant?",
    unit="Unit 1: Limits and Continuity", ced=["CHA-1.A", "CHA-1.A.1", "CHA-1.A.2", "CHA-1.A.3"],
    goals=(r"Compute average rates of change, and estimate a rate of change at an instant from average rates on shrinking "
           r"intervals."),
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
