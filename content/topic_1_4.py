"""Topic 1.4: Estimating limit values from tables.

CED: LIM-1.C.5 (numerical information can be used to estimate limits).
Running example matches the video: sin(x)/x near 0. Traps: sin(pi/x) sampled at 10^-k,
and (1 - cos x)/x^2 losing everything to rounding at tiny x.
"""
import math

import sympy as sp

from calclib import (VideoExample, Variants, FRQ, MCQ, BigIdea, Check, Definition, Example, Item, Part, Section, Table, Text,
                     Topic, Video, close, dne, num, same, selfcheck)

x = sp.symbols("x")
same("sinx/x", sp.limit(sp.sin(x) / x, x, 0), 1)
same("1-cos", sp.limit((1 - sp.cos(x)) / x**2, x, 0), sp.Rational(1, 2))
same("x^3-1", sp.limit((x**3 - 1) / (x - 1), x, 1), 3)
same("2^x", sp.limit((2**x - 1) / x, x, 0), sp.log(2))
for k in (1, 2, 3):
    close(f"sin(pi/x) at 10^-{k}", sp.sin(sp.pi / sp.Rational(1, 10**k)), 0, 1e-12)
close("sin(pi/x) at 2/21", sp.sin(sp.pi * sp.Rational(21, 2)), 1, 1e-12)
close("calc rounding", (1 - math.cos(1e-9)) / 1e-18, 0.0, 0)      # the trap is real in floating point


def sx(v):
    return math.sin(v) / v


XS = [-0.1, -0.01, -0.001, 0.001, 0.01, 0.1]
FMT = {0.1: "0.998334", 0.01: "0.999983", 0.001: "0.99999983"}
for v in XS:
    places = len(FMT[abs(v)].split(".")[1])
    close(f"table {v}", sx(v), float(FMT[abs(v)]), 0.5 * 10 ** -places)

row_x = " & ".join(f"${v:g}$" for v in XS)
row_y = " & ".join(f"${FMT[abs(v)]}$" for v in XS)

NOTES = [
    Video("s1_4.py::Lesson", "Limits from tables", 3.5),

    Section("Building a table"),
    Text(r"Substituting $x = 0$ into $\dfrac{\sin x}{x}$ yields $\dfrac00$. A calculator in \textbf{radian mode} "
         r"gives these values."),
    Table(r"$x$ & " + row_x + r" \\ $\dfrac{\sin x}{x}$ & " + row_y, "c|cccccc"),
    Text(r"From both sides the outputs close in on \blank{$1$}, so we estimate "
         r"$\displaystyle \lim_{x\to0}\frac{\sin x}{x} = \mblank{1}$."),
    Definition("A good table", (
        r"$\bullet$ uses inputs on \blank{both sides} of $c$;\par "
        r"$\bullet$ moves steadily closer to $c$ (for example, by factors of $10$);\par "
        r"$\bullet$ is read for a pattern: outputs that \blank{converge} on one value.")),

    Section("When tables mislead"),
    Text(r"\textbf{Unlucky inputs.} For $\displaystyle f(x) = \sin\dfrac{\pi}{x}$, the inputs $x = 0.1, 0.01, 0.001$ give "
         r"$\sin(10\pi), \sin(100\pi), \sin(1000\pi)$, which all equal \mblank{0}. But at $\displaystyle x = \dfrac{2}{21} \approx 0.095$, "
         r"$f(x) = \sin(10.5\pi) = \mblank{1}$. The function oscillates, so "
         r"$\displaystyle \lim_{x\to0}\sin\frac\pi x = $ \blank{does not exist}."),
    Text(r"\textbf{Rounding.} \[ \lim_{x\to0}\frac{1-\cos x}{x^2} = \frac12, \] but at $x = 10^{-9}$ a calculator "
         r"rounds $\cos x$ to exactly $1$ and reports $0$. When outputs suddenly collapse or jump at very small inputs, "
         r"suspect \blank{rounding}."),
    BigIdea(r"A table gives evidence for a limit, not proof. Check it against a graph, and later against algebra."),

    Section("Reading tables you are given"),
    Table(r"$x$ & $1.9$ & $1.99$ & $1.999$ & $2.001$ & $2.01$ & $2.1$ \\ "
          r"$g(x)$ & $3.9$ & $3.99$ & $3.999$ & $5.001$ & $5.01$ & $5.1$", "c|cccccc"),
    Text(r"$\displaystyle \lim_{x\to2^-} g(x) \approx \mblank{4}$, \quad $\displaystyle \lim_{x\to2^+} g(x) \approx \mblank{5}$, "
         r"\quad so $\displaystyle \lim_{x\to2} g(x) = $ \blank{does not exist}."),
    VideoExample('Your own table', work="3cm"),
    Check(r"Use a table to estimate $\displaystyle \lim_{x\to0}\frac{2^x-1}{x}$ to three decimal places.",
          num(sp.log(2), tol=0.0015, display=r"\approx 0.693"),
          r"At $x = \pm0.001$: $0.69339$ and $0.69291$. The limit is about $0.693$. (It is exactly $\ln 2$, as Topic 1.1 hinted.)"),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Use the table to estimate $\displaystyle\lim_{x\to 3} f(x)$."
         r"\par\smallskip\centerline{\begin{tabular}{c|cccccc} $x$ & 2.9 & 2.99 & 2.999 & 3.001 & 3.01 & 3.1 \\ \hline "
         r"$f(x)$ & $-0.62$ & $-0.962$ & $-0.9962$ & $-1.0038$ & $-1.038$ & $-1.38$\end{tabular}}", num(-1),
         r"Both sides close in on $-1$.", work="1.2cm"),
    Item(r"Use the table to estimate $\displaystyle\lim_{t\to 0^+} P(t)$."
         r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $t$ & 0.1 & 0.01 & 0.001 & 0.0001 \\ \hline "
         r"$P(t)$ & 2.594 & 2.705 & 2.717 & 2.718\end{tabular}}", num(sp.E, tol=0.002, display=r"\approx 2.718"),
         r"The outputs settle at about $2.718$. (These are values of $(1+t)^{1/t}$; the limit is the number $e$.)",
         work="1.2cm"),
    Item(r"Estimate $\displaystyle\lim_{x\to0}\frac{\tan x}{x}$ with a table. Use radian mode.", num(1),
         r"$x = \pm0.1$: $1.00335$; $\pm0.01$: $1.0000333$; $\pm0.001$: $1.00000033$. The limit is $1$.", calc=True),
    Item(r"Estimate $\displaystyle\lim_{x\to4}\frac{\sqrt{x}-2}{x-4}$ with a table.", num(sp.Rational(1, 4), tol=0.001,
         display="0.25"), r"$x = 3.99$: $0.25016$; $4.01$: $0.24984$. The limit is $0.25$.", calc=True),
    Item(r"Selected values of $h$ are shown. Estimate $\displaystyle\lim_{x\to-1} h(x)$, or type DNE."
         r"\par\smallskip\centerline{\begin{tabular}{c|cccccc} $x$ & $-1.1$ & $-1.01$ & $-1.001$ & $-0.999$ & $-0.99$ & $-0.9$ \\ \hline "
         r"$h(x)$ & 6.8 & 6.98 & 6.998 & 2.001 & 2.01 & 2.1\end{tabular}}", dne(),
         r"From the left the outputs head to $7$; from the right, to $2$. The limit does not exist.", work="1.2cm"),
    Item(r"For $h$ in Problem 5, what is $\displaystyle\lim_{x\to-1^-} h(x)$?", num(7), r"The left-side values approach $7$.",
         work="1cm"),
    Item(r"Jae evaluates $f(x) = \cos\dfrac{\pi}{x}$ at $x = 0.1, 0.01, 0.001$ and gets $1, 1, 1$. Jae concludes the limit "
         r"as $x\to0$ is $1$. Test $x = \frac{2}{21}$ and $x = \frac{1}{11}$, and decide whether Jae is right.",
         selfcheck(r"\text{No: } f(\tfrac{2}{21}) = 0,\ f(\tfrac1{11}) = -1"),
         r"$\cos(10.5\pi) = 0$ and $\cos(11\pi) = -1$. The outputs keep swinging between $-1$ and $1$, so the limit does not "
         r"exist. Jae's inputs all landed on peaks.", work="2.5cm", calc=True),
    Item(r"A calculator gives $\dfrac{1-\cos x}{x^2} = 0$ at $x = 10^{-9}$ but $0.5000$ at $x = 10^{-4}$. Which output "
         r"should you trust, and why?", selfcheck(r"0.5"),
         r"Trust $0.5$. At $x = 10^{-9}$, $\cos x$ is so close to $1$ that the calculator stores it as exactly $1$, so the "
         r"numerator becomes $0$ by rounding.", work="2cm"),
    Item(r"Use a table to estimate $\displaystyle\lim_{x\to0}\frac{e^{2x}-1}{x}$.", num(2),
         r"$x = \pm0.001$: $2.002$ and $1.998$. The limit is $2$.", calc=True),
    Item(r"The temperature of a cup of tea, $T(t)$ in $^\circ$F, is measured near $t = 5$ minutes."
         r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $t$ & 4.9 & 4.99 & 5.01 & 5.1 \\ \hline "
         r"$T(t)$ & 151.2 & 150.12 & 149.88 & 148.8\end{tabular}}"
         r"\par Estimate $\displaystyle\lim_{t\to5} T(t)$ and explain what it means in context.",
         num(150, tol=0.05, display=r"150\ ^\circ\text{F}"),
         r"About $150$. As the time approaches 5 minutes, the tea's temperature approaches $150^\circ$F.", work="2cm"),
]
same("p3", sp.limit(sp.tan(x) / x, x, 0), 1)
same("p4", sp.limit((sp.sqrt(x) - 2) / (x - 4), x, 4), sp.Rational(1, 4))
same("p9", sp.limit((sp.exp(2 * x) - 1) / x, x, 0), 2)
close("p7 a", sp.cos(sp.pi * sp.Rational(21, 2)), 0, 1e-12)
close("p7 b", sp.cos(sp.pi * 11), -1, 1e-12)
close("p2", (1 + 0.0001) ** (1 / 0.0001), 2.718, 5e-4)

# extra practice (round 1)
def _tab(e, xs, var=x, fmt="{:.4f}"):
    head = " & ".join(f"{float(v):g}" for v in xs)
    vals = " & ".join(fmt.format(float(e.subs(var, v))) for v in xs)
    return (r"\par\smallskip\centerline{\begin{tabular}{c|" + "c" * len(xs) + r"} $x$ & " + head
            + r" \\ \hline $f(x)$ & " + vals + r"\end{tabular}}")


E11 = (x**2 + x - 2) / (x - 1)
E12 = sp.sin(4 * x) / x
E13 = (sp.exp(x) - 1) / sp.sin(x)
XS = [-0.1, -0.01, 0.01, 0.1]
PRACTICE += [
    Item(r"Use the table to estimate $\displaystyle\lim_{x\to1} f(x)$." + _tab(E11, [0.9, 0.99, 1.01, 1.1]), num(3),
         r"From both sides the outputs close in on $3$.", work="1.2cm"),
    Item(r"Use the table to estimate $\displaystyle\lim_{x\to0} f(x)$." + _tab(E12, XS), num(4),
         "The outputs " + ", ".join(f"${float(E12.subs(x, v)):.4f}$" for v in XS) + " close in on $4$.", work="1.2cm"),
    Item(r"Use the table to estimate $\displaystyle\lim_{x\to0} f(x)$." + _tab(E13, XS), num(1),
         "The outputs " + ", ".join(f"${float(E13.subs(x, v)):.4f}$" for v in XS) + " close in on $1$ from both sides.", work="1.2cm"),
    Item(r"Make a table with $x = \pm0.01$ and $\pm0.001$ to estimate $\displaystyle\lim_{x\to0}\frac{\ln(1+x)}{x}$.", num(1),
         r"$x = 0.001$: $0.9995$; $x = -0.001$: $1.0005$. The limit is $1$.", calc=True, work="2cm"),
    Item(r"Make a table to estimate $\displaystyle\lim_{x\to0}\frac{3^x - 1}{x}$ to three decimal places.",
         num(sp.log(3), tol=0.0015, display=r"\approx 1.099"), r"$x = \pm0.001$: $1.0992$ and $1.0980$. The limit is about $1.099$ (exactly $\ln3$).",
         calc=True, work="2cm"),
    Item(r"Selected values of $g$ are shown."
         r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $x$ & 4.9 & 4.99 & 5.01 & 5.1 \\ \hline $g(x)$ & $-0.8$ & $-0.98$ & $2.02$ & $2.2$\end{tabular}}"
         r"\par Estimate $\displaystyle\lim_{x\to5^+} g(x)$.", num(2), r"The right-side values head to $2$.", work="1.2cm"),
    Item(r"For $g$ in Problem 16, estimate $\displaystyle\lim_{x\to5} g(x)$, or type DNE.", dne(),
         r"The left-side values head to $-1$ and the right-side values to $2$.", work="1.2cm"),
    Item(r"Eli evaluates $f(x) = \sin\dfrac{2\pi}{x}$ at $x = 1, 0.5, 0.1, 0.01$ and gets $0$ each time. Test $x = 0.8$ and decide "
         r"whether $\displaystyle\lim_{x\to0} f(x) = 0$.", selfcheck(r"\text{No}"),
         r"$f(0.8) = \sin(2.5\pi) = 1$. The function keeps oscillating near $0$, so the limit does not exist.", calc=True, work="2cm"),
    Item(r"A table for $h(x)$ near $x = 2$ shows $h(1.99) = 5.02$ and $h(2.01) = 5.02$, but $h(2) = 9$. What is the best estimate of "
         r"$\displaystyle\lim_{x\to2}h(x)$?", num(sp.Rational(502, 100), tol=0.03, display=r"\approx 5"),
         r"The value at $2$ doesn't matter; the nearby values suggest a limit of about $5$.", work="1.4cm"),
    Item(r"Explain why a table with $x = 0.1, 0.2, 0.3$ is poor evidence for $\displaystyle\lim_{x\to0}f(x)$.",
         selfcheck(r"\text{one side, not close enough}"),
         r"It uses only the right side, the inputs don't move steadily toward $0$, and none are very close to $0$.", work="1.6cm"),
]
same("p11", sp.limit(E11, x, 1), 3)
same("p12", sp.limit(E12, x, 0), 4)
same("p13", sp.limit(E13, x, 0), 1)
same("p14", sp.limit(sp.log(1 + x) / x, x, 0), 1)
close("p18", sp.sin(2 * sp.pi / sp.Rational(8, 10)), 1, 1e-12)


# ---------------------------------------------------------------- quiz
BEST = {"A": "includes the point itself and doesn't get close", "B": "only one side", "D": "only one side"}
QUIZ = [
    Variants(
        Item(r"Use the table to estimate $\displaystyle\lim_{x\to 2} f(x)$."
             r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $x$ & 1.99 & 1.999 & 2.001 & 2.01 \\ \hline "
             r"$f(x)$ & 7.96 & 7.996 & 8.004 & 8.04\end{tabular}}", num(8), r"Both sides approach $8$.", work="1cm"),
        Item(r"Use the table to estimate $\displaystyle\lim_{x\to -1} f(x)$."
             r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $x$ & $-1.01$ & $-1.001$ & $-0.999$ & $-0.99$ \\ \hline "
             r"$f(x)$ & 2.97 & 2.997 & 3.003 & 3.03\end{tabular}}", num(3), r"Both sides approach $3$.", work="1cm"),
        Item(r"Use the table to estimate $\displaystyle\lim_{x\to 4} f(x)$."
             r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $x$ & 3.99 & 3.999 & 4.001 & 4.01 \\ \hline "
             r"$f(x)$ & $-0.51$ & $-0.501$ & $-0.499$ & $-0.49$\end{tabular}}", num(sp.Rational(-1, 2), display="-0.5"),
             r"Both sides approach $-0.5$.", work="1cm"),
    ),
    Variants(
        Item(r"Use a table to estimate $\displaystyle\lim_{x\to0}\frac{\sin(3x)}{x}$ (radian mode).", num(3),
             r"$x = \pm0.001$: $2.9999955$. The limit is $3$.", work="2cm"),
        Item(r"Use a table to estimate $\displaystyle\lim_{x\to0}\frac{\tan(2x)}{x}$ (radian mode).", num(2),
             r"$x = \pm0.001$: $2.0000027$. The limit is $2$.", work="2cm"),
        Item(r"Use a table to estimate $\displaystyle\lim_{x\to0}\frac{e^{2x} - 1}{x}$.", num(2),
             r"$x = 0.001$: $2.002$; $x = -0.001$: $1.998$. The limit is $2$.", work="2cm"),
    ),
    Variants(
        MCQ(r"Which set of inputs is best for estimating $\displaystyle\lim_{x\to5} f(x)$ with a table?",
            [r"$4, 4.5, 5, 5.5, 6$", r"$4.9, 4.99, 4.999$", r"$4.9, 4.99, 4.999, 5.001, 5.01, 5.1$", r"$5.1, 5.01, 5.001$"], "C",
            r"Use both sides of $5$, closing in steadily, and never $5$ itself.", why_not=BEST),
        MCQ(r"Which set of inputs is best for estimating $\displaystyle\lim_{x\to-2} g(x)$ with a table?",
            [r"$-3, -2.5, -2, -1.5, -1$", r"$-2.1, -2.01, -2.001$", r"$-1.9, -1.99, -1.999$",
             r"$-2.1, -2.01, -2.001, -1.999, -1.99, -1.9$"], "D",
            r"Use both sides of $-2$, closing in steadily, and never $-2$ itself.", why_not={"A": BEST["A"], "B": BEST["B"], "C": BEST["D"]}),
        MCQ(r"Which set of inputs is best for estimating $\displaystyle\lim_{x\to0} h(x)$ with a table?",
            [r"$-0.1, -0.01, -0.001, 0.001, 0.01, 0.1$", r"$-1, 0, 1$", r"$0.1, 0.01, 0.001$", r"$-0.1, -0.01, -0.001$"], "A",
            r"Use both sides of $0$, closing in steadily, and never $0$ itself.", why_not={"B": BEST["A"], "C": BEST["B"], "D": BEST["D"]}),
    ),
    Variants(
        Item(r"Selected values of $g$ are shown. Estimate $\displaystyle\lim_{x\to0} g(x)$, or type DNE."
             r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $x$ & $-0.01$ & $-0.001$ & $0.001$ & $0.01$ \\ \hline "
             r"$g(x)$ & $-0.99$ & $-0.999$ & $0.999$ & $0.99$\end{tabular}}", dne(),
             r"Left side heads to $-1$, right side to $1$. The limit does not exist.", work="1cm"),
        Item(r"Selected values of $g$ are shown. Estimate $\displaystyle\lim_{x\to3} g(x)$, or type DNE."
             r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $x$ & 2.99 & 2.999 & 3.001 & 3.01 \\ \hline "
             r"$g(x)$ & 4.98 & 4.998 & 7.002 & 7.02\end{tabular}}", dne(),
             r"Left side heads to $5$, right side to $7$. The limit does not exist.", work="1cm"),
        Item(r"Selected values of $g$ are shown. Estimate $\displaystyle\lim_{x\to1} g(x)$, or type DNE."
             r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $x$ & 0.99 & 0.999 & 1.001 & 1.01 \\ \hline "
             r"$g(x)$ & 1.98 & 1.998 & 2.002 & 2.02\end{tabular}}", num(2),
             r"Both sides approach $2$, so the limit is $2$.", work="1cm"),
    ),
    Variants(
        MCQ(r"$f(x) = \sin\dfrac{\pi}{x}$ gives $f(0.1) = f(0.01) = f(0.001) = 0$. What can you conclude about "
            r"$\displaystyle\lim_{x\to0} f(x)$?",
            [r"It equals $0$.", r"It equals $\pi$.", r"Nothing yet: the evidence is too thin, and in fact the limit does not exist.",
             r"It equals $1$."], "C",
            r"Those three inputs happen to hit zeros of the sine wave. Other inputs, like $\frac2{21}$, give $1$.",
            why_not={"A": "three lucky inputs are not a pattern"}),
        MCQ(r"A calculator gives $\dfrac{1 - \cos x}{x^2} = 0$ at $x = 10^{-9}$, but about $0.5$ at $x = 0.001$. Which is the best "
            r"estimate of $\displaystyle\lim_{x\to0}\dfrac{1 - \cos x}{x^2}$?",
            [r"$0$", r"$0.5$", r"The limit does not exist.", r"$1$"], "B",
            r"At $x = 10^{-9}$, $\cos x$ rounds to exactly $1$ on the calculator, so the $0$ is a rounding error. The true limit is $\frac12$.",
            why_not={"A": "that value comes from rounding, not the function", "C": "the reliable values settle on $0.5$"}),
        MCQ(r"A table for $g$ near $x = 2$ shows $g(1.9) = 4.1$, $g(1.99) = 4.01$, $g(2.01) = 3.99$ and $g(2.1) = 3.9$. What is the best "
            r"estimate of $\displaystyle\lim_{x\to2} g(x)$?", [r"$3.9$", r"$4.1$", r"Does not exist.", r"$4$"], "D",
            r"From the left the outputs come down to $4$; from the right they go up to $4$. Both sides approach $4$.",
            why_not={"C": "the two sides approach the same value", "A": "that's one table entry, not the trend"}),
    ),
]
same("q2", sp.limit(sp.sin(3 * x) / x, x, 0), 3)
same("q2 versions", [sp.limit(sp.tan(2 * x) / x, x, 0), sp.limit((sp.exp(2 * x) - 1) / x, x, 0), sp.limit((1 - sp.cos(x)) / x**2, x, 0)],
     [2, 2, sp.Rational(1, 2)])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"Selected values of $f$ are given."
        r"\par\centerline{\begin{tabular}{c|cccccc} $x$ & 0.9 & 0.99 & 0.999 & 1.001 & 1.01 & 1.1 \\ \hline "
        r"$f(x)$ & 1.62 & 1.9602 & 1.996 & 2.004 & 2.0402 & 2.42\end{tabular}}"
        r"\par Which is the best estimate of $\displaystyle\lim_{x\to1} f(x)$?",
        [r"$2$", r"$1.996$", r"$2.004$", r"The limit does not exist."], "A",
        r"Values on both sides close in on $2$.", why_not={"B": "left side only", "C": "right side only"}),
    MCQ(r"Using values of $x$ near $0$ in radian mode, $\displaystyle\lim_{x\to0}\frac{\sin(2x)}{\sin(5x)}$ is closest to",
        [r"$0$", r"$0.4$", r"$1$", r"$2.5$"], "B",
        r"At $x = 0.001$ the ratio is $0.40000$. The limit is $\frac25$.",
        why_not={"D": "inverted the ratio", "C": "canceled the sines"}, calc=True),
    MCQ(r"The table gives values of $r$ near $x = 3$."
        r"\par\centerline{\begin{tabular}{c|cccc} $x$ & 2.99 & 2.999 & 3.001 & 3.01 \\ \hline "
        r"$r(x)$ & $-4.01$ & $-4.001$ & $6.001$ & $6.01$\end{tabular}}"
        r"\par Which statement is supported by the table?",
        [r"$\displaystyle\lim_{x\to3} r(x) = 1$", r"$\displaystyle\lim_{x\to3^-} r(x) = 6$",
         r"$\displaystyle\lim_{x\to3^+} r(x) = -4$", r"$\displaystyle\lim_{x\to3} r(x)$ does not exist"], "D",
        r"The left side heads to $-4$ and the right side to $6$.",
        why_not={"A": "averaged the one-sided limits", "B": "sides reversed", "C": "sides reversed"}),
    MCQ(r"A student uses a calculator to evaluate $g(x) = \dfrac{1-\cos x}{x^2}$ at $x = 10^{-3}$ and $x = 10^{-10}$, "
        r"getting $0.49999996$ and $0$. Which is the best explanation?",
        [r"The limit is $0$ because the smaller input is closer to $0$.",
         r"At $x = 10^{-10}$, $\cos x$ rounds to $1$, so the calculator loses the true value; the limit is $\frac12$.",
         r"The limit does not exist because the outputs disagree.",
         r"The function oscillates near $0$."], "B",
        r"Tiny inputs can defeat a calculator's precision. The trend from reasonable inputs is $\frac12$.",
        why_not={"A": "the $0$ is a rounding artifact", "D": "$g$ does not oscillate"}),
]
same("m2", sp.limit(sp.sin(2 * x) / sp.sin(5 * x), x, 0), sp.Rational(2, 5))

# AP does not ask this topic as free response; the multiple-choice questions above cover it.
# See .claude/skills/ap-frq/SKILL.md.
FRQS = []

TOPIC = Topic(
    number="1.4", title="Estimating Limit Values from Tables",
    unit="Unit 1: Limits and Continuity", ced=["LIM-1.C", "LIM-1.C.5"],
    goals=r"Build and read tables of values to estimate limits, and recognize when a table can mislead.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
