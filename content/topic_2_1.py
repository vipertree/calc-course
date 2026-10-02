"""Topic 2.1: Defining average and instantaneous rates of change at a point.

CED: CHA-2.A (difference quotients), CHA-2.B.1 (derivative at a point as a limit,
both forms). The running story matches the video: Amara's distance from home,
s(t) = t^3 - 9t^2 + 24t miles after t hours.
"""
import sympy as sp

from calclib import (Variants, limchain, FRQ, MCQ, BigIdea, Check, Definition, Desmos, Example, Figure, Formula, Item,
                     Meanings, Part, Section, Table, Text, Topic, Video, VideoExample, check, close, expr,
                     num, same, selfcheck)

t, x, h = sp.symbols("t x h")
S = t**3 - 9 * t**2 + 24 * t
s = sp.Lambda(t, S)


def avg(f, a, b):
    return (f(b) - f(a)) / (b - a)


# ---------------------------------------------------------------- facts used below
same("s(1)", s(1), 16)
same("s(4)", s(4), 16)
same("s(0)", s(0), 0)
same("s(2)", s(2), 20)
same("avg [1,4]", avg(s, 1, 4), 0)
same("avg [0,2]", avg(s, 0, 2), 10)
H_ROWS = [(1, 4), (sp.Rational(1, 2), sp.Rational(25, 4)), (sp.Rational(1, 10), sp.Rational(841, 100)),
          (sp.Rational(1, 100), sp.Rational(89401, 10000)), (sp.Rational(-1, 10), sp.Rational(961, 100)),
          (sp.Rational(-1, 100), sp.Rational(90601, 10000))]
for hv, want in H_ROWS:
    same(f"avg rate h={hv}", (s(1 + hv) - s(1)) / hv, want)
same("s'(1)", sp.limit((s(1 + h) - s(1)) / h, h, 0), 9)
same("s'(1) via diff", sp.diff(S, t).subs(t, 1), 9)

# Example 2: f(x) = x^2 at a = 3
f2 = sp.Lambda(x, x**2)
same("ex2 quotient", sp.simplify((f2(3 + h) - f2(3)) / h), 6 + h)
# Example 3: g(x) = 1/x, a = 2, x -> a form
g3 = sp.Lambda(x, 1 / x)
same("ex3 simplified", sp.simplify((g3(x) - g3(2)) / (x - 2)), -1 / (2 * x))
same("ex3 value", sp.limit((g3(x) - g3(2)) / (x - 2), x, 2), sp.Rational(-1, 4))
# Example 4: recognise ((2+h)^3 - 8)/h
same("ex4", sp.limit(((2 + h)**3 - 8) / h, h, 0), 12)


def fmt(v):
    return sp.latex(sp.nsimplify(v)) if sp.nsimplify(v).is_Integer else f"{float(v):g}"


# ---------------------------------------------------------------- figures
AXIS = (r"\begin{axis}[calcaxes, width=8.2cm, height=5.6cm, xmin=0, xmax=5.4, ymin=0, ymax=25,"
        r" xtick={1,2,3,4,5}, ytick={4,8,...,24}, xlabel={$t$}, ylabel={$s(t)$}]")
FIG_SECANT = Figure(name="t2_1_secant", caption="Amara's distance from home. The dashed line is a secant line.", tikz=(
    r"\begin{tikzpicture}" + AXIS +
    r"\addplot[fn, domain=0:5.2]{x^3-9*x^2+24*x};"
    r"\addplot[secant, domain=0.3:4.7]{16};"
    r"\addplot[pt] coordinates {(1,16) (4,16)};"
    r"\node[above left, font=\small] at (axis cs:1,16) {$(1,16)$};"
    r"\node[below right, font=\small] at (axis cs:4,16) {$(4,16)$};"
    r"\end{axis}\end{tikzpicture}"))
FIG_TANGENT = Figure(name="t2_1_tangent", caption="The tangent line at $t=1$ has slope $s'(1)=9$.", tikz=(
    r"\begin{tikzpicture}" + AXIS +
    r"\addplot[fn, domain=0:5.2]{x^3-9*x^2+24*x};"
    r"\addplot[tangent, domain=0.1:2.0]{16+9*(x-1)};"
    r"\addplot[secant, domain=0.4:2.2]{16+4*(x-1)};"
    r"\addplot[pt] coordinates {(1,16) (2,20)};"
    r"\node[right, font=\footnotesize, align=left] at (axis cs:2.45,23.2) {secant, $h=1$: slope $4$};"
    r"\node[left, font=\footnotesize, align=right] at (axis cs:1.35,22.8) {tangent:\\slope $9$};"
    r"\end{axis}\end{tikzpicture}"))

# ---------------------------------------------------------------- guided notes
rows = " \\\\ ".join(
    f"${fmt(hv)}$ & ${fmt(1 + hv)}$ & ${fmt(want)}$" for hv, want in H_ROWS)

NOTES = [
    Video("s2_1.py::Lesson", "From average to instant", 3),

    Section("Average rate of change"),
    Text(r"Amara drives along a straight road. Her distance from home after $t$ hours is "
         r"$s(t) = t^3 - 9t^2 + 24t$ miles."),
    Text(r"Her \textbf{average velocity} over a stretch of time is the change in position divided by the "
         r"change in time. From $t=0$ to $t=2$ she went from \mblank{0} miles to \blank{$20$} miles, "
         r"so her average velocity was \blank{$10$} miles per hour."),
    Formula("Average rate of change", (
        r"The average rate of change of $f$ on $[a,b]$ is"
        r"\[ \frac{f(b)-f(a)}{b-a} \qquad\text{or, with } b = a+h,\qquad \frac{f(a+h)-f(a)}{h}. \]"
        r"Units: \blank{output units} per \blank{input unit}. \quad "
        r"Graphically, it is the slope of the \blank{secant} line through $(a, f(a))$ and $(b, f(b))$.")),
    FIG_SECANT,
    Text(r"\textbf{An average hides things.} From $t=1$ to $t=4$: \[ \frac{s(4)-s(1)}{4-1} = \frac{16-16}{3} = \blank{0} \] miles per hour. "
         r"She drove out to $20$ miles and back to $16$, so she moved the whole time. Her average \emph{speed} (distance traveled over time) was "
         r"\[ \frac{4 + 4}{3} \approx \blank{2.67} \] miles per hour. Velocity keeps track of direction, so the trip out and the trip back cancel."),

    Section("Shrinking the interval"),
    Text(r"To find her speed at the single instant $t=1$, shrink the interval. "
         r"Compute $\dfrac{s(1+h)-s(1)}{h}$ for smaller and smaller $h$. Negative $h$ means the second time is "
         r"\emph{before} $t=1$."),
    Table(rows, "ccc", header=r"$h$ & $1+h$ & average rate on the interval (mph)"),
    Desmos("Drag $h$ toward 0", r"Drag the slider for $h$. Watch the secant slope as $h$ gets close to $0$ from either side.",
           [{"id": "s", "latex": r"s(t)=t^{3}-9t^{2}+24t", "color": "#2d70b3"},
            {"id": "h", "latex": r"h=1", "sliderBounds": {"min": "-1", "max": "3", "step": "0.001"}},
            {"id": "m", "latex": r"m=\frac{s(1+h)-s(1)}{h}"},
            {"id": "sec", "latex": r"y=s(1)+m(t-1)", "color": "#c98a00", "lineStyle": "DASHED"},
            {"id": "P", "latex": r"(1,s(1))", "color": "#000000"},
            {"id": "Q", "latex": r"(1+h,s(1+h))", "color": "#000000"}],
           {"left": -0.5, "right": 5.5, "bottom": -2, "top": 26}),
    Text(r"From both sides, the average rates approach \blank{$9$}. We say her "
         r"\textbf{instantaneous rate of change} at $t=1$ is $9$ miles per hour."),
    Text(r"Setting $h = 0$ directly gives $\dfrac{0}{0}$, which has no value. "
         r"A \blank{limit} lets $h$ get close to $0$ without ever equaling $0$."),

    Section("The derivative at a point"),
    Formula("Definition of the derivative at $x = a$", (
        r"\[ f'(a) = \lim_{h\to 0}\frac{f(a+h)-f(a)}{h} \qquad\text{or}\qquad "
        r"f'(a) = \lim_{x\to a}\frac{f(x)-f(a)}{x-a}, \]"
        r"provided the limit exists. Both say the same thing: the average rate of change on a shrinking "
        r"interval, in the limit.")),
    Text(r"\textbf{Why two forms?} Call the second input $x$ instead of $a + h$. Then the gap between the inputs is $h = \mblank{x - a}$, "
         r"and shrinking $h$ to $0$ is the same as sliding $x$ toward $a$. Same secant slopes, same limit."),
    Meanings(("da", "dg"), caption="The derivative, two ways."),
    Definition("Two meanings of $f'(a)$", (
        r"\textbf{Analytically:} $f'(a)$ is the \blank{instantaneous rate of change} of $f$ at $x=a$.\par"
        r"\textbf{Graphically:} $f'(a)$ is the \blank{slope of the tangent line} to the graph of $f$ at $x=a$.")),
    FIG_TANGENT,
    BigIdea(r"A derivative is a limit of average rates. On the graph, it is a limit of secant slopes."),
    VideoExample("Zeno's arrow, answered", work="3.2cm"),

    Section("Computing a derivative from the definition"),
    Text(r"\textbf{Factor and cancel $h$.} After the constants cancel, every term on top has a factor of $h$. Factor it out and cancel it "
         r"with the $h$ on the bottom. That's allowed because $h \neq 0$ inside the limit."),
    VideoExample("The h form", work="3cm"),
    VideoExample("The x to a form", work="3.2cm"),
    Text(r"\textbf{Limits that are derivatives.} Soon we'll have rules that find derivatives in a line or two. Then a limit like "
         r"\[ \lim_{h\to 0}\frac{(3+h)^3-27}{h} \] on a test is a derivative in disguise: recognize it as $f'(a)$ with $f(x) = \mblank{x^3}$ and "
         r"$a = \mblank{3}$, and use the rules instead of the algebra."),
    Check(r"For $f(x) = 5x - x^2$, use either form of the definition to find $f'(1)$.",
          num(3), limchain(0, [r"\frac{f(1+h)-f(1)}{h}", r"\frac{5+5h-1-2h-h^2-4}{h}", r"\frac{3h-h^2}{h}", r"(3-h)"], r"3", var="h")),
]
same("zeno", sp.limit((60 * (1 + h) - 12 * (1 + h)**2 - 48) / h, h, 0), 36)
same("check f'(1)", sp.limit(((5 * (1 + h) - (1 + h)**2) - 4) / h, h, 0), 3)

# ---------------------------------------------------------------- practice
T = sp.symbols("T")
PRACTICE = [
    Item(r"Find the average rate of change of $f(x) = x^3 - 2x$ on $[1, 3]$.",
         num(11), r"$\dfrac{f(3)-f(1)}{3-1} = \dfrac{21-(-1)}{2} = 11$."),
    Item(r"The table gives the temperature $W(t)$ of a cup of tea, in $^\circ$C, $t$ minutes after it was poured."
         r"\par\smallskip\centerline{\begin{tabular}{c|ccccc} $t$ & 0 & 2 & 5 & 9 & 12 \\ \hline $W(t)$ & 92 & 84 & 75 & 66 & 61\end{tabular}}"
         r"\par Find the average rate of change of $W$ on $[2, 9]$. Include units.",
         num(sp.Rational(-18, 7), tol=0.005, display=r"-\tfrac{18}{7}\ ^\circ\text{C/min}"),
         r"$\dfrac{66-84}{9-2} = -\dfrac{18}{7} \approx -2.571$ degrees Celsius per minute."),
    Item(r"Using the table in Problem 2, estimate $W'(7)$. Show the computation you use.",
         num(sp.Rational(-9, 4), tol=0.005, display=r"-\tfrac{9}{4}"),
         r"Use the closest data on each side: $\dfrac{W(9)-W(5)}{9-5} = \dfrac{66-75}{4} = -2.25\ ^\circ$C per minute."),
    Item(r"Use the definition of the derivative to find $f'(2)$ for $f(x) = 3x^2 + 1$.",
         num(12), "$f'(2) = $ " + limchain(0, [r"\frac{3(2+h)^2+1-13}{h}", r"\frac{12h+3h^2}{h}", r"(12+3h)"], r"12", var="h")),
    Item(r"Use the definition of the derivative to find $g'(4)$ for $g(x) = \sqrt{x}$.",
         num(sp.Rational(1, 4)),
         "Multiply by the conjugate: " + limchain(0, [r"\frac{\sqrt{4+h}-2}{h}", r"\frac{(4+h)-4}{h(\sqrt{4+h}+2)}", r"\frac{1}{\sqrt{4+h}+2}"], r"\frac14", var="h")),
    Item(r"Use the $x\to a$ form of the definition to find $k'(-1)$ for $k(x) = x^2 + 4x$.",
         num(2), r"$k(-1) = -3$, so " + limchain(-1, [r"\frac{x^2+4x-(-3)}{x-(-1)}", r"\frac{(x+1)(x+3)}{x+1}", r"(x+3)"], 2)),
    Item(r"Each limit below is $f'(a)$ for some $f$ and $a$. Name $f$ and $a$, then evaluate."
         r"\par (a) $\displaystyle\lim_{h\to 0}\frac{\sqrt{9+h}-3}{h}$ \qquad (b) $\displaystyle\lim_{x\to 5}\frac{x^2-25}{x-5}$",
         selfcheck(r"(a)\ \sqrt{x},\ 3,\ \tfrac16;\ (b)\ x^2,\ 5,\ 10"),
         r"(a) $f(x)=\sqrt{x}$, $a=9$: " + limchain(0, [r"\frac{\sqrt{9+h}-3}{h}", r"\frac{h}{h(\sqrt{9+h}+3)}", r"\frac{1}{\sqrt{9+h}+3}"], r"\frac16", var="h") + r". (b) $f(x)=x^2$, $a=5$: " + limchain(5, [r"\frac{x^2-25}{x-5}", r"(x+5)"], 10) + "."),
    Item(r"A balloon's volume is $V(r) = \tfrac43\pi r^3$ cubic inches when its radius is $r$ inches. "
         r"Find the average rate of change of $V$ as $r$ goes from $2$ to $2.1$. Round to three decimal places.",
         num(sp.Rational(4, 3) * sp.pi * (sp.Rational(21, 10)**3 - 8) / sp.Rational(1, 10), tol=0.0005,
             display=r"\approx 52.821\ \text{in}^3\text{/in}"),
         r"$\dfrac{V(2.1)-V(2)}{0.1} = \dfrac{\frac43\pi(9.261-8)}{0.1} \approx 52.821$ cubic inches per inch.",
         calc=True),
    Item(r"Kenji says that because $\dfrac{f(a+h)-f(a)}{h}$ has $h$ in the denominator, you can never plug in "
         r"$h = 0$, so $f'(a)$ can never be found exactly. Explain what is wrong with Kenji's reasoning.",
         selfcheck(r"\text{The limit uses values near } h=0\text{, not } h=0\text{ itself.}"),
         (r"A limit describes what the quotient approaches as $h$ gets close to $0$; it never requires $h = 0$. "
          r"After simplifying (allowed, since $h\neq0$), the limit can often be found exactly, as in $x^2$ at $a=3$: "
          + limchain(0, [r"\frac{h(6+h)}{h}", r"(6+h)"], r"6", var="h") + "."),
         work="2.5cm"),
    Item(r"The graph of $f$ passes through $(1, 5)$ and $(1.01, 5.0302)$. Estimate $f'(1)$.",
         num(sp.Rational(302, 100), tol=0.005, display="3.02"),
         r"$\dfrac{5.0302-5}{0.01} = 3.02$. A secant over a very short interval approximates the tangent slope."),
]
same("p1", avg(sp.Lambda(x, x**3 - 2 * x), 1, 3), 11)
same("p2", sp.Rational(66 - 84, 9 - 2), sp.Rational(-18, 7))
same("p4", sp.limit((3 * (2 + h)**2 + 1 - 13) / h, h, 0), 12)
same("p5", sp.limit((sp.sqrt(4 + h) - 2) / h, h, 0), sp.Rational(1, 4))
same("p6", sp.limit((x**2 + 4 * x + 3) / (x + 1), x, -1), 2)
same("p7a", sp.limit((sp.sqrt(9 + h) - 3) / h, h, 0), sp.Rational(1, 6))
same("p7b", sp.limit((x**2 - 25) / (x - 5), x, 5), 10)
close("p8", sp.N(sp.Rational(4, 3) * sp.pi * (sp.Rational(21, 10)**3 - 8) * 10), 52.821, tol=5e-4)

# extra practice (round 1)
PRACTICE += [
    Item(r"Find the average rate of change of $g(x) = \sqrt{x}$ on $[4, 9]$.", num(sp.Rational(1, 5)),
         r"$\dfrac{g(9)-g(4)}{9-4} = \dfrac{3-2}{5} = \dfrac15$.", work="1.6cm"),
    Item(r"Find the average rate of change of $f(x) = \dfrac{6}{x}$ on $[1, 3]$.", num(-2),
         r"$\dfrac{f(3)-f(1)}{3-1} = \dfrac{2-6}{2} = -2$.", work="1.6cm"),
    Item(r"Amara's distance from home is $s(t) = t^3 - 9t^2 + 24t$ miles after $t$ hours. Find her average velocity on "
         r"$[2, 4]$ and say what it means.", num(-2),
         r"$\dfrac{s(4)-s(2)}{4-2} = \dfrac{16-20}{2} = -2$ miles per hour. Over those two hours her distance from home "
         r"shrank by an average of $2$ miles each hour.", work="1.8cm"),
    Item(r"Fill in the difference quotients $\dfrac{f(1+h)-f(1)}{h}$ for $f(x) = x^3$ at $h = 0.1$ and $h = 0.01$, "
         r"then guess $f'(1)$.", num(3),
         "At $h = 0.1$: $3.31$. At $h = 0.01$: $3.0301$. The values approach $3$, so $f'(1) = 3$.", work="2.2cm"),
    Item(r"Use the definition of the derivative to find $f'(-2)$ for $f(x) = x^2 - 3x$.", num(-7),
         "$f'(-2) = $ " + limchain(0, [r"\frac{(-2+h)^2 - 3(-2+h) - 10}{h}", r"\frac{-7h + h^2}{h}", r"(-7 + h)"], -7, var="h"),
         work="3cm"),
    Item(r"Use the definition of the derivative to find $f'(3)$ for $f(x) = \dfrac{1}{x+1}$.", num(sp.Rational(-1, 16)),
         "$f'(3) = $ " + limchain(0, [r"\frac{\frac{1}{4+h} - \frac14}{h}", r"\frac{4 - (4+h)}{4h(4+h)}", r"\frac{-1}{4(4+h)}"],
                                  r"-\frac{1}{16}", var="h"), work="3cm"),
    Item(r"Use the $x \to a$ form to find $f'(2)$ for $f(x) = x^3$.", num(12),
         "$f'(2) = $ " + limchain(2, [r"\frac{x^3 - 8}{x - 2}", r"\frac{(x-2)(x^2 + 2x + 4)}{x - 2}", r"(x^2 + 2x + 4)"], 12),
         work="3cm"),
    Item(r"$\displaystyle\lim_{h\to0}\frac{(1+h)^5 - 1}{h}$ is $f'(a)$ for some $f$ and $a$. Name $f$ and $a$.",
         selfcheck(r"f(x) = x^5,\ a = 1"),
         r"It matches $\dfrac{f(a+h) - f(a)}{h}$ with $f(x) = x^5$ and $a = 1$, since $1^5 = 1$.", work="1.6cm"),
    Item(r"A pot of soup cools, and its temperature is $T(m)$ degrees Fahrenheit $m$ minutes after it leaves the stove. "
         r"Explain the meaning of $\dfrac{T(10) - T(4)}{10 - 4} = -3.5$ and of $T'(4) = -5$, with units.",
         selfcheck(r"\text{average vs. instantaneous}"),
         r"From minute $4$ to minute $10$, the soup cooled by an average of $3.5$ degrees per minute. At the instant $m = 4$, "
         r"its temperature was dropping at $5$ degrees per minute.", work="2.4cm"),
    Item(r"The points $(2, 7)$ and $(2.001, 7.012)$ are on the graph of $f$. Estimate $f'(2)$.",
         num(12, tol=0.005), r"$\dfrac{7.012 - 7}{0.001} = 12$. A secant over a tiny interval is close to the tangent.",
         work="1.4cm"),
]
same("x1 a", avg(sp.Lambda(x, sp.sqrt(x)), 4, 9), sp.Rational(1, 5))
same("x1 b", avg(sp.Lambda(x, 6 / x), 1, 3), -2)
same("x1 c", [s(4), s(2), avg(s, 2, 4)], [16, 20, -2])
same("x1 d", [((1 + h)**3 - 1) / h for h in (sp.Rational(1, 10), sp.Rational(1, 100))],
     [sp.Rational(331, 100), sp.Rational(30301, 10000)])
same("x1 e", sp.limit(((-2 + h)**2 - 3 * (-2 + h) - 10) / h, h, 0), -7)
same("x1 f", sp.limit((1 / (4 + h) - sp.Rational(1, 4)) / h, h, 0), sp.Rational(-1, 16))
same("x1 g", sp.limit((x**3 - 8) / (x - 2), x, 2), 12)

# ---------------------------------------------------------------- quiz
MEAN = {"A": "that would be the value, not the rate", "C": "that would be a total change", "D": "an average is a secant slope, not the derivative"}
QUIZ = [
    Variants(
        Item(r"Find the average rate of change of $f(x) = x^2 + 3x$ on $[1, 4]$.", num(8),
             r"$\dfrac{f(4)-f(1)}{3} = \dfrac{28-4}{3} = 8$.", work="2cm"),
        Item(r"Find the average rate of change of $f(x) = \dfrac{12}{x}$ on $[2, 6]$.", num(-1),
             r"$\dfrac{f(6)-f(2)}{6-2} = \dfrac{2-6}{4} = -1$.", work="2cm"),
        Item(r"Find the average rate of change of $f(x) = x^3 - x$ on $[0, 3]$.", num(8),
             r"$\dfrac{f(3)-f(0)}{3-0} = \dfrac{24-0}{3} = 8$.", work="2cm"),
    ),
    Variants(
        Item(r"A tank holds $V(t)$ gallons of water $t$ hours after noon. $V(1) = 340$ and $V(5) = 220$. "
             r"Find the average rate of change of $V$ on $[1,5]$, with units.",
             num(-30, display=r"-30\text{ gal/hr}"), r"$\dfrac{220-340}{5-1} = -30$ gallons per hour.", work="2cm"),
        Item(r"A town had $P(t)$ thousand people $t$ years after 2010. $P(2) = 41$ and $P(10) = 53$. "
             r"Find the average rate of change of $P$ on $[2, 10]$, with units.",
             num(sp.Rational(3, 2), display=r"1.5\text{ thousand people/yr}"), r"$\dfrac{53-41}{10-2} = 1.5$ thousand people per year.", work="2cm"),
        Item(r"A runner has gone $D(t)$ meters after $t$ seconds. $D(10) = 62$ and $D(25) = 167$. "
             r"Find the average rate of change of $D$ on $[10, 25]$, with units.",
             num(7, display=r"7\text{ m/s}"), r"$\dfrac{167-62}{25-10} = 7$ meters per second.", work="2cm"),
    ),
    Variants(
        Item(r"Use the definition of the derivative to find $f'(1)$ for $f(x) = 3x^2 - x$.", num(5),
             "$f'(1) = $ " + limchain(0, [r"\frac{3(1+h)^2-(1+h)-2}{h}", r"\frac{5h+3h^2}{h}", r"(5+3h)"], r"5", var="h"), work="3.2cm"),
        Item(r"Use the definition of the derivative to find $f'(2)$ for $f(x) = x^2 - 4x$.", num(0),
             "$f'(2) = $ " + limchain(0, [r"\frac{(2+h)^2-4(2+h)-(-4)}{h}", r"\frac{h^2}{h}", r"h"], r"0", var="h"), work="3.2cm"),
        Item(r"Use the definition of the derivative to find $f'(-1)$ for $f(x) = 2x^2 + 5$.", num(-4),
             "$f'(-1) = $ " + limchain(0, [r"\frac{2(-1+h)^2+5-7}{h}", r"\frac{-4h+2h^2}{h}", r"(-4+2h)"], r"-4", var="h"), work="3.2cm"),
    ),
    Variants(
        MCQ(r"$\displaystyle\lim_{h\to0}\frac{\sqrt{16+h}-4}{h}$ is equal to",
            [r"$0$", r"$\dfrac18$", r"$\dfrac14$", r"The limit does not exist."], "B",
            "Multiply by the conjugate: " + limchain(0, [r"\frac{\sqrt{16+h}-4}{h}", r"\frac{h}{h(\sqrt{16+h}+4)}", r"\frac{1}{\sqrt{16+h}+4}"], r"\frac18", var="h") + ".",
            why_not={"A": "treated $0/0$ as $0$", "C": "used $\\frac{1}{\\sqrt{16}}$, dropping one of the two $4$s", "D": "stopped at $0/0$"}),
        MCQ(r"$\displaystyle\lim_{h\to0}\frac{(3+h)^2-9}{h}$ is equal to", [r"$9$", r"$0$", r"$3$", r"$6$"], "D",
            limchain(0, [r"\frac{6h+h^2}{h}", r"(6+h)"], 6, var="h") + ".", why_not={"B": "treated $0/0$ as $0$", "A": "that's $f(3)$"}),
        MCQ(r"$\displaystyle\lim_{x\to2}\frac{x^3-8}{x-2}$ is equal to", [r"$12$", r"$8$", r"$4$", r"The limit does not exist."], "A",
            limchain(2, [r"\frac{(x-2)(x^2+2x+4)}{x-2}", r"(x^2+2x+4)"], 12) + ". It is $f'(2)$ for $f(x) = x^3$.",
            why_not={"B": "that's $f(2)$", "D": "stopped at $0/0$"}),
    ),
    Variants(
        MCQ(r"$s(t)$ is Amara's distance from home in miles, $t$ hours after she leaves, and $s'(1) = 9$. Which statement is true?",
            [r"Amara is 9 miles from home at $t=1$.", r"At $t=1$, Amara's distance from home is increasing at 9 miles per hour.",
             r"Amara drives 9 miles during the first hour.", r"Amara's average speed over the first hour is 9 miles per hour."], "B",
            r"$s'(1)$ is an instantaneous rate: miles per hour at the instant $t=1$.", why_not=MEAN),
        MCQ(r"$C(n)$ is the cost, in dollars, of making $n$ bikes, and $C'(50) = 120$. Which statement is true?",
            [r"Making 50 bikes costs 120 dollars.", r"When 50 bikes have been made, the cost is rising at 120 dollars per bike.",
             r"The first 50 bikes cost 120 dollars each on average.", r"Making 120 bikes costs 50 dollars."], "B",
            r"$C'(50)$ is the rate the cost is changing, in dollars per bike, at $n = 50$.", why_not={"A": MEAN["A"], "C": MEAN["D"], "D": "input and output swapped"}),
        MCQ(r"$h(t)$ is a balloon's height in meters $t$ seconds after release, and $h'(4) = -2$. Which statement is true?",
            [r"The balloon is 2 meters high at $t = 4$.", r"The balloon falls 2 meters in the first 4 seconds.",
             r"The balloon's average velocity on $[0, 4]$ is $-2$ m/s.", r"At $t = 4$, the balloon is sinking at 2 meters per second."], "D",
            r"$h'(4) = -2$: the height is decreasing at 2 meters per second at that instant.", why_not={"A": MEAN["A"], "B": MEAN["C"], "C": MEAN["D"]}),
    ),
]
same("q1", avg(sp.Lambda(x, x**2 + 3 * x), 1, 4), 8)
same("q3", sp.limit((3 * (1 + h)**2 - (1 + h) - 2) / h, h, 0), 5)
same("q4", sp.limit((sp.sqrt(16 + h) - 4) / h, h, 0), sp.Rational(1, 8))
same("q versions", [avg(sp.Lambda(x, 12 / x), 2, 6), avg(sp.Lambda(x, x**3 - x), 0, 3), sp.Rational(53 - 41, 8), sp.Rational(167 - 62, 15),
                    sp.limit(((2 + h)**2 - 4 * (2 + h) + 4) / h, h, 0), sp.limit((2 * (-1 + h)**2 + 5 - 7) / h, h, 0)],
     [-1, 8, sp.Rational(3, 2), 7, 0, -4])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"If $f(x) = x^3 - 4x$, what is the average rate of change of $f$ on the interval $[-1, 2]$?",
        [r"$-3$", r"$-1$", r"$0$", r"$1$"], "B",
        r"$f(2) = 0$ and $f(-1) = 3$, so $\dfrac{0-3}{2-(-1)} = -1$.",
        why_not={"A": "numerator only", "C": "used $f(2)$ as the answer", "D": "reversed the numerator but not the denominator"}),
    MCQ(r"$\displaystyle\lim_{h\to0}\frac{\frac{1}{2+h}-\frac12}{h}$ is",
        [r"$-\dfrac14$", r"$-\dfrac12$", r"$\dfrac14$", r"Does not exist"], "A",
        "Combine the fractions: " + limchain(0, [r"\frac{\frac{2-(2+h)}{2(2+h)}}{h}", r"\frac{-h}{2h(2+h)}", r"\frac{-1}{2(2+h)}"], r"-\frac14", var="h") + ". "
        r"It is $f'(2)$ for $f(x) = \frac1x$.",
        why_not={"B": "dropped the $(2+h)$ factor from the denominator", "C": "lost the negative sign",
                 "D": "stopped at $0/0$"}),
    MCQ(r"The table gives values of a differentiable function $g$. "
        r"\par\centerline{\begin{tabular}{c|cccc} $x$ & 1.8 & 1.9 & 2.1 & 2.2 \\ \hline $g(x)$ & 3.10 & 3.42 & 4.02 & 4.28\end{tabular}}"
        r"\par Which is the best estimate of $g'(2)$ from the table?",
        [r"$0.3$", r"$1.5$", r"$3.0$", r"$6.0$"], "C",
        r"Use the closest points on either side: $\dfrac{g(2.1)-g(1.9)}{2.1-1.9} = \dfrac{0.60}{0.2} = 3.0$.",
        why_not={"A": "forgot to divide by $0.2$", "B": "divided by $0.4$", "D": "divided by $0.1$"}),
    MCQ(r"Which limit gives the slope of the line tangent to $y = \ln x$ at $x = e$?",
        [r"$\displaystyle\lim_{h\to0}\frac{\ln(e+h)}{h}$", r"$\displaystyle\lim_{h\to0}\frac{\ln(e+h)-1}{h}$",
         r"$\displaystyle\lim_{x\to e}\frac{\ln x - e}{x-e}$", r"$\displaystyle\lim_{h\to0}\frac{\ln(e+h)-\ln e}{e}$"], "B",
        r"$f'(e) = \lim_{h\to0}\frac{f(e+h)-f(e)}{h}$ and $f(e) = \ln e = 1$.",
        why_not={"A": "left out $f(e)$", "C": "subtracted $e$ instead of $f(e)$", "D": "divided by $e$ instead of $h$"}),
]
close("mcq3", (4.02 - 3.42) / 0.2, 3.0)
same("mcq1", avg(sp.Lambda(x, x**3 - 4 * x), -1, 2), -1)
same("mcq2", sp.limit((1 / (2 + h) - sp.Rational(1, 2)) / h, h, 0), sp.Rational(-1, 4))

FRQS = [
    FRQ("Cooling coffee", (
        r"Marisol pours a cup of coffee. Its temperature $C(t)$, in degrees Fahrenheit, is measured at "
        r"selected times $t$, in minutes. $C$ is differentiable."
        r"\par\smallskip\centerline{\begin{tabular}{c|ccccc} $t$ (min) & 0 & 3 & 5 & 9 & 14 \\ \hline "
        r"$C(t)$ ($^\circ$F) & 180 & 162 & 153 & 139 & 126\end{tabular}}"), [
        Part("a", r"Find the average rate of change of $C$ over $0 \le t \le 14$. Include units.",
             num(sp.Rational(-27, 7), tol=0.005, display=r"-\tfrac{27}{7}\ ^\circ\text{F/min}"),
             r"$\dfrac{C(14)-C(0)}{14-0} = \dfrac{126-180}{14} = -\dfrac{27}{7} \approx -3.857$ degrees F per minute.",
             [(1, "difference quotient with correct values"), (1, "answer with units")], work="3cm"),
        Part("b", r"Use the data to estimate $C'(4)$. Show the computation that leads to your answer.",
             num(sp.Rational(-9, 2), tol=0.005, display=r"-4.5"),
             r"$C'(4) \approx \dfrac{C(5)-C(3)}{5-3} = \dfrac{153-162}{2} = -4.5$ degrees F per minute.",
             [(1, "uses $C(5)$ and $C(3)$ in a difference quotient"), (1, "value $-4.5$")], work="3cm"),
        Part("c", r"Interpret the meaning of $C'(4)$ in the context of the problem.",
             selfcheck(r"\text{At } t=4\text{, temperature decreasing about 4.5 degrees F per minute}"),
             (r"At time $t = 4$ minutes, the temperature of the coffee is changing (decreasing) at a rate of about "
              r"$4.5$ degrees Fahrenheit per minute."),
             [(1, "rate of change of temperature, at $t=4$, with units (all three needed)")], work="2.5cm"),
    ], frq_type="Table of values / rates"),
]
same("frq a", sp.Rational(126 - 180, 14), sp.Rational(-27, 7))
same("frq b", sp.Rational(153 - 162, 2), sp.Rational(-9, 2))

TOPIC = Topic(
    number="2.1", title="Average and Instantaneous Rates of Change",
    unit="Unit 2: Differentiation", ced=["CHA-2.A", "CHA-2.A.1", "CHA-2.B", "CHA-2.B.1"],
    goals=(r"Compute average rates of change with difference quotients, and write the instantaneous rate "
           r"of change at a point as a limit of those quotients."),
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
