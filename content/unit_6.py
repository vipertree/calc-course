"""Unit 6 test: Integration and Accumulation of Change. AP format: 12 MCQ (no calculator), 4 MCQ (calculator), 3 FRQ.
Two forms (A and B) for every slot. Covers the AB topics 6.1-6.10 and 6.14 (the BC-only topics 6.11-6.13 are left out).

Choices are built by `pick`, which puts the keyed answer at a planned letter. Every keyed value is checked with sympy.
"""
import sympy as sp

from calclib import FRQ, MCQ, Part, UnitTest, Variants, close, num, same, selfcheck
from calclib.figs import graph

x, t = sp.symbols("x t", real=True)
I = lambda f, a, b, v=x: sp.simplify(sp.integrate(f, (v, a, b)))
exact = lambda e: sp.nsimplify(sp.N(e, 30), [sp.pi])


def pick(stem, right, wrong, letter, solution, why=None, calc=False):
    k = "ABCD".index(letter)
    choices = list(wrong)
    choices.insert(k, right)
    why_not = {}
    if why:
        for text, reason in why.items():
            why_not["ABCD"[choices.index(text)]] = reason
    return MCQ(stem, choices, letter, solution, why_not=why_not, calc=calc)


A = [
    Variants(
        pick(r"The left Riemann sum for $f(x) = x^2$ on $[0, 4]$ with $4$ equal subintervals is", r"$14$", [r"$30$", r"$\frac{64}{3}$", r"$22$"], "B",
             r"$1(0 + 1 + 4 + 9) = 14$.", {r"$30$": "the right sum", r"$\frac{64}{3}$": "the exact area"}),
        pick(r"The right Riemann sum for $f(x) = x^2$ on $[0, 4]$ with $2$ equal subintervals is", r"$40$", [r"$8$", r"$\frac{64}{3}$", r"$24$"], "D",
             r"$2(4 + 16) = 40$.", {r"$8$": "the left sum", r"$24$": "the trapezoidal sum"}),
    ),
    Variants(
        pick(r"$f$ is positive, decreasing and concave up on $[a, b]$. Which sums overestimate $\int_a^b f(x)\,dx$?", r"the left sum and the trapezoidal sum",
             [r"the right sum only", r"the right sum and the trapezoidal sum", r"the left sum only"], "A", r"Decreasing: left over. Concave up: trapezoid over."),
        pick(r"$f$ is positive, increasing and concave down on $[a, b]$. Which sums underestimate $\int_a^b f(x)\,dx$?", r"the left sum and the trapezoidal sum",
             [r"the right sum only", r"the right sum and the trapezoidal sum", r"the left sum only"], "C", r"Increasing: left under. Concave down: trapezoid under."),
    ),
    Variants(
        pick(r"$\displaystyle\lim_{n\to\infty} \sum_{k=1}^{n} \left(2 + \frac{3k}{n}\right)^2 \frac3n = $", r"$\int_2^5 x^2\,dx$", [r"$\int_0^3 x^2\,dx$", r"$\int_2^3 x^2\,dx$", r"$\int_0^1 (2 + 3x)^2\,dx$"], "A",
             r"$\Delta x = \frac3n$, $x_k = 2 + \frac{3k}{n}$: $a = 2$, $b = 5$."),
        pick(r"$\displaystyle\lim_{n\to\infty} \sum_{k=1}^{n} \sqrt{\frac{4k}{n}} \cdot \frac4n = $", r"$\int_0^4 \sqrt x\,dx$", [r"$\int_0^1 \sqrt x\,dx$", r"$\int_1^4 \sqrt x\,dx$", r"$4\int_0^4 \sqrt x\,dx$"], "B",
             r"$\Delta x = \frac4n$, $x_k = \frac{4k}{n}$: $a = 0$, $b = 4$."),
    ),
    Variants(
        pick(r"$\dfrac{d}{dx}\displaystyle\int_0^{x^2} \sin t\,dt = $", r"$2x\sin\left(x^2\right)$", [r"$\sin\left(x^2\right)$", r"$\sin x$", r"$-\cos\left(x^2\right)$"], "C",
             r"FTC with the chain rule.", {r"$\sin\left(x^2\right)$": "missing the factor $2x$"}),
        pick(r"$\dfrac{d}{dx}\displaystyle\int_x^3 e^{t^2}\,dt = $", r"$-e^{x^2}$", [r"$e^{x^2}$", r"$e^9 - e^{x^2}$", r"$2xe^{x^2}$"], "D", r"Swap the limits: $-\int_3^x e^{t^2}\,dt$."),
    ),
    Variants(
        pick(r"$\displaystyle\int_1^2 \left(3x^2 - 1\right) dx = $", r"$6$", [r"$7$", r"$11$", r"$5$"], "A", r"$\left[x^3 - x\right]_1^2 = 6 - 0$."),
        pick(r"$\displaystyle\int_0^{\pi/2} \cos x\,dx = $", r"$1$", [r"$0$", r"$-1$", r"$\frac\pi2$"], "B", r"$\sin\frac\pi2 - \sin 0 = 1$."),
    ),
    Variants(
        pick(r"If $\int_0^5 f(x)\,dx = 8$ and $\int_3^5 f(x)\,dx = 3$, then $\int_0^3 2f(x)\,dx = $", r"$10$", [r"$5$", r"$22$", r"$16$"], "C", r"$\int_0^3 f = 8 - 3 = 5$; times $2$."),
        pick(r"If $\int_1^4 f(x)\,dx = 6$ and $\int_1^4 g(x)\,dx = 2$, then $\int_4^1 \left[f(x) - 3g(x)\right] dx = $", r"$0$", [r"$12$", r"$-12$", r"$4$"], "A", r"$-(6 - 6) = 0$."),
    ),
    Variants(
        pick(r"$g(x) = \int_0^x f(t)\,dt$, where $f$ is positive on $(0, 4)$, negative on $(4, 9)$, and positive on $(9, 12)$. On $[0, 12]$, $g$ has a relative maximum at", r"$x = 4$ only",
             [r"$x = 9$ only", r"$x = 4$ and $x = 9$", r"$x = 12$"], "B", r"$g' = f$ changes from $+$ to $-$ only at $4$.", {r"$x = 9$ only": "that's the relative minimum"}),
        pick(r"$g(x) = \int_0^x f(t)\,dt$, where the graph of $f$ is increasing on $(0, 3)$ and decreasing on $(3, 7)$. The graph of $g$ has a point of inflection at", r"$x = 3$",
             [r"$x = 0$", r"$x = 7$", r"where $f = 0$"], "D", r"$g'' = f'$ changes sign at $3$."),
    ),
    Variants(
        pick(r"$\displaystyle\int \frac{x^2 + 1}{x}\,dx = $", r"$\frac{x^2}{2} + \ln|x| + C$", [r"$\frac{\frac{x^3}{3} + x}{\frac{x^2}{2}} + C$", r"$x + \ln|x| + C$", r"$\frac{x^2}{2} - \frac{1}{x^2} + C$"], "A",
             r"Split: $x + \frac1x$."),
        pick(r"$\displaystyle\int \sec x\tan x\,dx = $", r"$\sec x + C$", [r"$\tan x + C$", r"$\frac{\sec^2 x}{2} + C$", r"$-\sec x + C$"], "C", r"$\frac{d}{dx}\sec x = \sec x\tan x$."),
    ),
    Variants(
        pick(r"$\displaystyle\int x e^{x^2}\,dx = $", r"$\frac12 e^{x^2} + C$", [r"$e^{x^2} + C$", r"$2e^{x^2} + C$", r"$\frac{x^2}{2}e^{x^2} + C$"], "D", r"$u = x^2$, $x\,dx = \frac12\,du$."),
        pick(r"$\displaystyle\int \frac{\cos x}{1 + \sin x}\,dx = $", r"$\ln|1 + \sin x| + C$", [r"$\ln|\cos x| + C$", r"$\frac{\sin x}{x + \cos x} + C$", r"$-\frac{1}{(1 + \sin x)^2} + C$"], "A",
             r"$u = 1 + \sin x$."),
    ),
    Variants(
        pick(r"$\displaystyle\int_0^1 x\left(x^2 + 1\right)^3 dx = $", r"$\frac{15}{8}$", [r"$\frac{15}{4}$", r"$2$", r"$\frac{1}{8}$"], "B", r"$u = x^2 + 1$ from $1$ to $2$: $\frac12\left[\frac{u^4}{4}\right]_1^2 = \frac{15}{8}$.",
             {r"$\frac{15}{4}$": "forgot the $\\frac12$"}),
        pick(r"$\displaystyle\int_0^{\pi/2} \sin x\cos x\,dx = $", r"$\frac12$", [r"$1$", r"$0$", r"$-\frac12$"], "C", r"$u = \sin x$ from $0$ to $1$: $\left[\frac{u^2}{2}\right]_0^1$."),
    ),
    Variants(
        pick(r"$\displaystyle\int \frac{dx}{x^2 + 2x + 2} = $", r"$\arctan(x + 1) + C$", [r"$\ln\left(x^2 + 2x + 2\right) + C$", r"$\frac12\arctan\frac{x + 1}{2} + C$", r"$\arctan x + C$"], "A",
             r"$(x + 1)^2 + 1$."),
        pick(r"$\displaystyle\int \frac{dx}{\sqrt{4 - x^2}} = $", r"$\arcsin\frac x2 + C$", [r"$\frac12\arcsin\frac x2 + C$", r"$\arcsin x + C$", r"$\frac12\arctan\frac x2 + C$"], "D", r"$a = 2$."),
    ),
    Variants(
        pick(r"$f(1) = 3$ and $f'(x) = 2x$. Then $f(3) = $", r"$11$", [r"$8$", r"$9$", r"$6$"], "B", r"$f(3) = 3 + \int_1^3 2x\,dx = 3 + 8$.", {r"$8$": "the change, not the value"}),
        pick(r"A particle's velocity is $v(t) = 3t^2$, and its position at $t = 0$ is $2$. Its position at $t = 2$ is", r"$10$", [r"$8$", r"$12$", r"$14$"], "A",
             r"$2 + \int_0^2 3t^2\,dt = 2 + 8$."),
    ),
]
same("A", [sum(k**2 for k in range(4)), I(3 * x**2 - 1, 1, 2), I(sp.cos(x), 0, sp.pi / 2), 2 * (8 - 3), I(x * (x**2 + 1)**3, 0, 1), I(sp.sin(x) * sp.cos(x), 0, sp.pi / 2), 3 + I(2 * x, 1, 3), 2 + I(3 * t**2, 0, 2, t)],
     [14, 6, 1, 10, sp.Rational(15, 8), sp.Rational(1, 2), 11, 10])
same("A2", [2 * (2**2 + 4**2), sum(k**2 for k in range(4))], [40, 14])

B = [
    Variants(
        pick(r"$\displaystyle\int_0^2 e^{-x^2}\,dx \approx $", r"$0.882$", [r"$0.746$", r"$1.000$", r"$0.018$"], "B", r"With a calculator: $0.88208$.", calc=True),
        pick(r"$\displaystyle\int_1^3 \ln\left(x^2 + 1\right) dx \approx $", r"$3.142$", [r"$2.303$", r"$1.609$", r"$4.159$"], "C", r"With a calculator: $3.14190$.", calc=True),
    ),
    Variants(
        pick(r"Water flows into a tank at $R(t) = 5 + 2\sin t$ liters per minute. How many liters flow in from $t = 0$ to $t = 4$?", r"$23.307$", [r"$3.486$", r"$21.307$", r"$25.307$"], "A",
             r"$\int_0^4 (5 + 2\sin t)\,dt \approx 23.307$.", {r"$3.486$": "that's $R(4)$"}, calc=True),
        pick(r"Sand is added to a pile at $R(t) = 8 - 3\cos\left(\frac t2\right)$ cubic feet per hour. How much sand is added from $t = 0$ to $t = 6$?", r"$47.153$", [r"$10.970$", r"$48.000$", r"$44.847$"], "D",
             r"$\int_0^6 R(t)\,dt \approx 47.153$.", calc=True),
    ),
    Variants(
        pick(r"$g(x) = \displaystyle\int_0^x \sqrt{1 + t^3}\,dt$. Then $g(2) \approx $", r"$3.241$", [r"$3.000$", r"$2.000$", r"$4.000$"], "C", r"With a calculator: $3.24131$.", {r"$3.000$": "that's $g'(2)$"}, calc=True),
        pick(r"$g(x) = \displaystyle\int_0^x \sqrt{1 + t^4}\,dt$. Then $g(1.5) \approx $", r"$2.031$", [r"$2.462$", r"$1.500$", r"$3.250$"], "B", r"With a calculator: $2.03084$.", {r"$2.462$": "that's $g'(1.5)$"}, calc=True),
    ),
    Variants(
        pick(r"A particle moves with velocity $v(t) = t\cos t$ for $t \ge 0$, and its position at $t = 0$ is $1$. Its position at $t = 3$ is about", r"$-0.567$", [r"$-1.567$", r"$-2.970$", r"$0.433$"], "A",
             r"$1 + \int_0^3 t\cos t\,dt \approx 1 - 1.567 = -0.567$.", {r"$-1.567$": "the displacement, not the position"}, calc=True),
        pick(r"A particle moves with velocity $v(t) = t\sin t$ for $t \ge 0$, and its position at $t = 0$ is $2$. Its position at $t = 2$ is about", r"$3.742$", [r"$1.742$", r"$1.819$", r"$3.819$"], "D",
             r"$2 + \int_0^2 t\sin t\,dt \approx 2 + 1.742 = 3.742$.", {r"$1.742$": "the displacement, not the position"}, calc=True),
    ),
]
close("B1", sp.N(sp.Integral(sp.exp(-x**2), (x, 0, 2))), 0.882, 5e-4)
close("B1b", sp.N(sp.Integral(sp.log(x**2 + 1), (x, 1, 3))), 3.142, 5e-4)
close("B2", sp.N(I(5 + 2 * sp.sin(t), 0, 4, t)), 23.307, 5e-4)
close("B2b", sp.N(I(8 - 3 * sp.cos(t / 2), 0, 6, t)), 47.153, 5e-4)
close("B3", sp.N(sp.Integral(sp.sqrt(1 + t**3), (t, 0, 2))), 3.241, 5e-4)
close("B3b", sp.N(sp.Integral(sp.sqrt(1 + t**4), (t, 0, 1.5))), 2.031, 5e-4)
close("B4", sp.N(1 + I(t * sp.cos(t), 0, 3, t)), -0.567, 5e-4)
close("B4b", sp.N(2 + I(t * sp.sin(t), 0, 2, t)), 3.742, 5e-4)

# ---------------------------------------------------------------- FRQ 1: table
TA = {0: 10, 2: 14, 5: 15, 9: 19, 12: 26}
TB = {0: 20, 3: 17, 4: 15, 8: 9, 10: 8}
left = lambda d: sum((b - a) * d[a] for a, b in zip(sorted(d), sorted(d)[1:]))
trap = lambda d: sum(sp.Rational(b - a, 2) * (d[a] + d[b]) for a, b in zip(sorted(d), sorted(d)[1:]))
same("F1", [left(TA), trap(TB), sp.Rational(19 - 15, 4), sp.Rational(9 - 15, 4)], [179, sp.Rational(273, 2), 1, -sp.Rational(3, 2)])
F1A = FRQ("Water into a tank", (
    r"Water flows into a tank at a rate modeled by a twice-differentiable, increasing function $R$, where $R(t)$ is measured in gallons per hour and $t$ is measured in hours. "
    r"Selected values of $R(t)$ are given in the table."
    r"\par\smallskip\centerline{\begin{tabular}{c|ccccc} $t$ (hours) & 0 & 2 & 5 & 9 & 12 \\ \hline $R(t)$ (gallons per hour) & 10 & 14 & 15 & 19 & 26\end{tabular}}"), [
    Part("a", r"Use the data in the table to approximate $R'(7)$. Show the computations that lead to your answer. Indicate units of measure.", num(1, display=r"1\ \text{gallon per hour per hour}"),
         r"$R'(7) \approx \dfrac{R(9) - R(5)}{9 - 5} = \dfrac{19 - 15}{4} = 1$ gallon per hour per hour.", [(1, "difference quotient and answer"), (1, "units")], work="2.2cm"),
    Part("b", r"Use a left Riemann sum with the four subintervals indicated by the table to approximate $\displaystyle\int_0^{12} R(t)\,dt$. Show the computations that lead to your answer.",
         num(left(TA)), r"$2(10) + 3(14) + 4(15) + 3(19) = 20 + 42 + 60 + 57 = 179$.", [(1, "left Riemann sum setup"), (1, "answer")], work="2.4cm"),
    Part("c", r"Using correct units, interpret the meaning of $\displaystyle\int_0^{12} R(t)\,dt$ in the context of the problem.",
         selfcheck(r"\text{the total gallons that flow in from } t = 0 \text{ to } t = 12"), r"$\int_0^{12} R(t)\,dt$ is the total number of gallons of water that flow into the tank from $t = 0$ to $t = 12$ hours.",
         [(1, "interpretation with units")], work="1.6cm"),
    Part("d", r"Is the approximation in part (b) an overestimate or an underestimate of $\displaystyle\int_0^{12} R(t)\,dt$? Give a reason for your answer.", selfcheck(r"\text{underestimate}"),
         r"$R$ is increasing, so on each subinterval the left endpoint gives the least value of $R$. The left Riemann sum is an underestimate.", [(1, "underestimate with reason")], work="1.6cm"),
], frq_type="Table")
F1B = FRQ("Draining a tank", (
    r"Water drains from a tank at a rate modeled by a twice-differentiable function $D$, where $D(t)$ is measured in liters per minute and $t$ is measured in minutes, and $D''(t) > 0$ "
    r"for $0 < t < 10$. Selected values of $D(t)$ are given in the table."
    r"\par\smallskip\centerline{\begin{tabular}{c|ccccc} $t$ (minutes) & 0 & 3 & 4 & 8 & 10 \\ \hline $D(t)$ (liters per minute) & 20 & 17 & 15 & 9 & 8\end{tabular}}"), [
    Part("a", r"Use the data in the table to approximate $D'(6)$. Show the computations that lead to your answer. Indicate units of measure.", num(-sp.Rational(3, 2), display=r"-1.5\ \text{liters per minute per minute}"),
         r"$D'(6) \approx \dfrac{D(8) - D(4)}{8 - 4} = \dfrac{9 - 15}{4} = -1.5$ liters per minute per minute.", [(1, "difference quotient and answer"), (1, "units")], work="2.2cm"),
    Part("b", r"Use a trapezoidal sum with the four subintervals indicated by the table to approximate $\displaystyle\int_0^{10} D(t)\,dt$. Show the computations that lead to your answer.",
         num(trap(TB)), r"$3 \cdot \frac{20 + 17}{2} + 1 \cdot \frac{17 + 15}{2} + 4 \cdot \frac{15 + 9}{2} + 2 \cdot \frac{9 + 8}{2} = 55.5 + 16 + 48 + 17 = 136.5$.",
         [(1, "trapezoidal sum setup"), (1, "answer")], work="2.6cm"),
    Part("c", r"Using correct units, interpret the meaning of $\displaystyle\int_0^{10} D(t)\,dt$ in the context of the problem.",
         selfcheck(r"\text{the total liters drained from } t = 0 \text{ to } t = 10"), r"$\int_0^{10} D(t)\,dt$ is the total number of liters of water that drain from the tank from $t = 0$ to $t = 10$ minutes.",
         [(1, "interpretation with units")], work="1.6cm"),
    Part("d", r"Is the approximation in part (b) an overestimate or an underestimate of $\displaystyle\int_0^{10} D(t)\,dt$? Give a reason for your answer.", selfcheck(r"\text{overestimate}"),
         r"$D''(t) > 0$, so the graph of $D$ is concave up and each trapezoid's top lies above the graph. The trapezoidal sum is an overestimate.", [(1, "overestimate with reason")], work="1.6cm"),
], frq_type="Table")

# ---------------------------------------------------------------- FRQ 2: graph of f, g(x) = integral of f
FA = sp.Piecewise((sp.sqrt(4 - t**2), t < 2), (-(t - 2), t < 4), (-2 + (t - 4), True))
gA = lambda v: exact(sp.integrate(FA, (t, 0, v)) if v >= 0 else -sp.integrate(FA, (t, v, 0)))
same("F2A", [gA(4), gA(-2), gA(2), gA(6)], [sp.pi - 2, -sp.pi, sp.pi, sp.pi - 4])
FIG2A = graph("tU6_2a", [("sqrt(abs(4-x^2))", -2, 2), ("-(x-2)", 2, 4), ("-2+(x-4)", 4, 6)], xr=(-2, 6), yr=(-3, 3), xlabel="t", ylabel="f(t)",
              caption="The graph of $f$: a semicircle and two line segments.")
F2A = FRQ("An accumulation function", (
    r"The continuous function $f$ is defined on $-2 \le t \le 6$. Its graph consists of the upper half of the circle of radius $2$ centered at the origin and two line segments, as shown. "
    r"Let $g(x) = \displaystyle\int_0^x f(t)\,dt$."), [
    Part("a", r"Find $g(4)$ and $g(-2)$.", selfcheck(r"g(4) = \pi - 2,\ \ g(-2) = -\pi"), r"$g(4) = \pi - \frac12(2)(2) = \pi - 2$. $g(-2) = -\int_{-2}^0 f(t)\,dt = -\pi$.",
         [(1, "$g(4)$"), (1, "$g(-2)$")], work="2.4cm"),
    Part("b", r"On what open intervals is $g$ increasing? Give a reason for your answer.", selfcheck(r"(-2, 2)"), r"$g'(x) = f(x) > 0$ on $-2 < x < 2$.", [(1, "interval with reason")], work="1.6cm"),
    Part("c", r"Find the absolute minimum value of $g$ on $[-2, 6]$. Justify your answer.", num(-sp.pi),
         r"$g' = f$ changes sign only at $x = 2$. Candidates: $g(-2) = -\pi$, $g(2) = \pi$, $g(6) = \pi - 4$. The minimum is $-\pi$, at $x = -2$.",
         [(1, "considers $x = 2$ and the endpoints"), (1, "answer with justification")], work="2.4cm"),
    Part("d", r"Find the $x$-coordinate of each point of inflection of the graph of $g$ on $-2 < x < 6$. Give a reason for your answer.", selfcheck(r"x = 0 \text{ and } x = 4"),
         r"$g'' = f'$ changes sign where $f$ has its maximum ($x = 0$) and its minimum ($x = 4$).", [(1, "$x = 0$ and $x = 4$"), (1, "reason")], work="2cm"),
], frq_type="Graph of f'", figure=FIG2A)
FB = sp.Piecewise((-2 + 2 * t, t < 2), (2, t < 4), (2 - sp.sqrt(4 - (t - 6)**2), True))
gB = lambda v: exact(sp.integrate(FB, (t, 0, v)))
same("F2B", [gB(1), gB(2), gB(4), gB(8)], [-1, 0, 4, 12 - 2 * sp.pi])
FIG2B = graph("tU6_2b", [("-2+2*x", 0, 2), ("2+0*x", 2, 4), ("2-sqrt(abs(4-(x-6)^2))", 4, 8)], xr=(0, 8), yr=(-3, 3), xlabel="t", ylabel="f(t)",
              caption="The graph of $f$: two line segments and a semicircle that touches the $t$-axis at $t = 6$.")
F2B = FRQ("An accumulation function", (
    r"The continuous function $f$ is defined on $0 \le t \le 8$. Its graph consists of two line segments and the lower half of the circle of radius $2$ centered at $(6, 2)$, as shown. "
    r"Let $g(x) = \displaystyle\int_0^x f(t)\,dt$."), [
    Part("a", r"Find $g(2)$ and $g(8)$.", selfcheck(r"g(2) = 0,\ \ g(8) = 12 - 2\pi"), r"$g(2) = -1 + 1 = 0$. $g(8) = 0 + (2)(2) + \left[(4)(2) - \frac12\pi(2)^2\right] = 12 - 2\pi$.",
         [(1, "$g(2)$"), (1, "$g(8)$")], work="2.4cm"),
    Part("b", r"Find the $x$-coordinate of each relative minimum of $g$ on $0 < x < 8$. Justify your answer.", num(1), r"$g' = f$ changes from negative to positive only at $x = 1$.",
         [(1, "$x = 1$ with justification")], work="1.8cm"),
    Part("c", r"Does $g$ have a relative extremum at $x = 6$? Explain your reasoning.", selfcheck(r"\text{No}"),
         r"No. $g'(6) = f(6) = 0$, but $f(x) > 0$ on both sides of $x = 6$, so $g'$ does not change sign there.", [(1, "no, with reason")], work="1.6cm"),
    Part("d", r"On what open interval is the graph of $g$ concave down? Give a reason for your answer.", selfcheck(r"(4, 6)"), r"$g'' = f'$, and $f$ is decreasing on $4 < x < 6$.",
         [(1, "interval with reason")], work="1.6cm"),
], frq_type="Graph of f'", figure=FIG2B)

# ---------------------------------------------------------------- FRQ 3: rate in context / particle motion
R3 = 12 - 3 * t
A3 = lambda v: 50 + I(R3, 0, v, t)
same("F3A", [A3(6), A3(4), R3.subs(t, 5)], [68, 74, -3])
F3A = FRQ("Water in a reservoir", (
    r"The amount of water in a small reservoir is $50$ thousand liters at time $t = 0$. For $0 \le t \le 6$, water flows in or out at the rate $R(t) = 12 - 3t$ thousand liters per day, "
    r"where positive values mean water is flowing in."), [
    Part("a", r"Find the amount of water in the reservoir at time $t = 6$. Show the work that leads to your answer.", num(68),
         r"$50 + \int_0^6 (12 - 3t)\,dt = 50 + \left[12t - \frac32t^2\right]_0^6 = 50 + 72 - 54 = 68$ thousand liters.", [(1, "integral"), (1, "answer")], work="2.4cm"),
    Part("b", r"Is the amount of water increasing or decreasing at time $t = 5$? Give a reason for your answer.", selfcheck(r"\text{decreasing}"), r"$R(5) = -3 < 0$.", [(1, "decreasing with reason")], work="1.4cm"),
    Part("c", r"At what time $t$, for $0 \le t \le 6$, is the amount of water greatest? Justify your answer.", num(4),
         r"$R(t) = 0$ at $t = 4$, and $R$ changes from positive to negative there. Candidates: $A(0) = 50$, $A(4) = 74$, $A(6) = 68$. The greatest amount is at $t = 4$ days.",
         [(1, "considers $t = 4$ and the endpoints"), (1, "answer with justification")], work="2.4cm"),
    Part("d", r"Write an expression for $A(t)$, the amount of water in the reservoir at time $t$.", selfcheck(r"A(t) = 50 + 12t - \tfrac32t^2"),
         r"$A(t) = 50 + \int_0^t (12 - 3s)\,ds = 50 + 12t - \frac32t^2$.", [(1, "expression")], work="1.6cm"),
], frq_type="Rate in context")
v3 = t**2 - 4 * t + 3
x3 = lambda v: 2 + I(v3, 0, v, t)
same("F3B", [x3(3), I(sp.Abs(v3), 0, 4, t), v3.subs(t, sp.Rational(5, 2)), sp.diff(v3, t).subs(t, sp.Rational(5, 2))], [2, 4, -sp.Rational(3, 4), 1])
F3B = FRQ("A particle on a line", (
    r"A particle moves along the $x$-axis with velocity $v(t) = t^2 - 4t + 3$ for $0 \le t \le 4$. At time $t = 0$ the particle is at $x = 2$."), [
    Part("a", r"Find the position of the particle at time $t = 3$.", num(2), r"$2 + \int_0^3 (t^2 - 4t + 3)\,dt = 2 + \left[\frac{t^3}{3} - 2t^2 + 3t\right]_0^3 = 2 + (9 - 18 + 9) = 2$.",
         [(1, "integral"), (1, "answer")], work="2.4cm"),
    Part("b", r"During what open interval of time is the particle moving to the left? Give a reason for your answer.", selfcheck(r"(1, 3)"),
         r"$v(t) = (t - 1)(t - 3) < 0$ for $1 < t < 3$.", [(1, "interval with reason")], work="1.6cm"),
    Part("c", r"Find the total distance traveled by the particle for $0 \le t \le 4$.", num(4),
         r"$\int_0^4 |v(t)|\,dt = \frac43 + \frac43 + \frac43 = 4$ (the pieces on $[0, 1]$, $[1, 3]$ and $[3, 4]$).", [(1, "integral of $|v|$ or split at turns"), (1, "answer")], work="2.4cm"),
    Part("d", r"Is the speed of the particle increasing, decreasing, or neither at time $t = 2.5$? Give a reason for your answer.", selfcheck(r"\text{decreasing}"),
         r"$v(2.5) = -0.75 < 0$ and $a(2.5) = v'(2.5) = 2(2.5) - 4 = 1 > 0$. They have opposite signs, so the speed is decreasing.", [(1, "decreasing with reason")], work="1.8cm"),
], frq_type="Particle motion")

TEST = UnitTest(unit=6, title="Integration and Accumulation of Change", mcq_a=A, mcq_b=B,
                frq=[Variants(F1A, F1B), Variants(F2A, F2B), Variants(F3A, F3B)])
