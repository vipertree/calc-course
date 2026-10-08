"""Unit 8 test: Applications of Integration. AP format: 12 MCQ (no calculator), 4 MCQ (calculator), 3 FRQ.
Two forms (A and B) for every slot. Covers the AB topics 8.1-8.12 (8.13, arc length, is BC-only and left out).

Choices are built by `pick`, which puts the keyed answer at a planned letter. Every keyed value is checked with sympy.
"""
import sympy as sp

from calclib import FRQ, MCQ, Part, UnitTest, Variants, close, num, same, selfcheck
from calclib.figs import region

x, t, y = sp.symbols("x t y", real=True)
I = lambda f, a, b, v=x: sp.simplify(sp.integrate(f, (v, a, b)))
N = lambda f, a, b, v=x: float(sp.Integral(f, (v, a, b)).evalf())


def pick(stem, right, wrong, letter, solution, why=None, calc=False):
    k = "ABCD".index(letter)
    choices = list(wrong)
    choices.insert(k, right)
    why_not = {}
    if why:
        for text, reason in why.items():
            why_not["ABCD"[choices.index(text)]] = reason
    return MCQ(stem, choices, letter, solution, why_not=why_not, calc=calc)


def dist(v, a, b):
    cuts = sorted({a, b} | {r for r in sp.solve(v, t) if r.is_real and a < r < b})
    return sum(abs(I(v, p, q, t)) for p, q in zip(cuts, cuts[1:]))


# ---------------------------------------------------------------- part A: no calculator
same("A1", [I(x**2 + 1, 0, 3) / 3, I(1 / x, 1, sp.E) / (sp.E - 1)], [4, 1 / (sp.E - 1)])
same("A3", [dist(t - 2, 0, 4), dist(3 - t, 0, 6)], [4, 9])
same("A4", [-2 + I(6 * t**2, 0, 1, t), -3 + I(4, 0, 2, t)], [0, 5])
same("A5", [30 + I(10 - 2 * t, 0, 4, t), 10 + I(6 - t, 0, 6, t)], [54, 28])
same("A7", [I(x - x**2, 0, 1), I(2 * x - x**2, 0, 2)], [sp.Rational(1, 6), sp.Rational(4, 3)])
same("A8", [I(4 - y**2, -2, 2, y), I(y + 2 - y**2, -1, 2, y)], [sp.Rational(32, 3), sp.Rational(9, 2)])
same("A9", [2 * I(x - x**3, 0, 1), 2 * I(sp.sin(x), 0, sp.pi)], [sp.Rational(1, 2), 4])
same("A10", [I(x, 0, 4), sp.pi / 8 * I((2 - x)**2, 0, 2)], [8, sp.pi / 3])
same("A11", [sp.pi * I(x, 0, 4), sp.pi * I(x**4, 0, 1)], [8 * sp.pi, sp.pi / 5])

A = [
    Variants(
        pick(r"The average value of $f(x) = x^2 + 1$ on $[0, 3]$ is", r"$4$", [r"$3$", r"$12$", r"$\frac{10}{3}$"], "B", r"$\frac13\int_0^3 (x^2 + 1)\,dx = \frac13(9 + 3)$.", {r"$12$": "forgot to divide by $3$", r"$3$": "the average rate of change"}),
        pick(r"The average value of $f(x) = \frac1x$ on $[1, e]$ is", r"$\frac{1}{e - 1}$", [r"$1$", r"$\frac{e - 1}{2}$", r"$\frac1e$"], "A", r"$\frac{1}{e - 1}\int_1^e \frac1x\,dx = \frac{1}{e - 1}$.", {r"$1$": "forgot to divide by $e - 1$"}),
    ),
    Variants(
        pick(r"If $\int_2^6 f(x)\,dx = 12$, the average value of $f$ on $[2, 6]$ is", r"$3$", [r"$12$", r"$2$", r"$48$"], "C", r"$\frac{12}{4}$."),
        pick(r"The average value of $f$ on $[1, 5]$ is $7$. Then $\int_1^5 f(x)\,dx = $", r"$28$", [r"$7$", r"$\frac74$", r"$35$"], "D", r"$7 \cdot 4$.", {r"$35$": "multiplied by $5$ instead of the length $4$"}),
    ),
    Variants(
        pick(r"A particle moves with $v(t) = t - 2$ for $0 \le t \le 4$. The total distance traveled is", r"$4$", [r"$0$", r"$2$", r"$8$"], "A", r"Split at $2$: $2 + 2$.", {r"$0$": "the displacement"}),
        pick(r"A particle moves with $v(t) = 3 - t$ for $0 \le t \le 6$. The total distance traveled is", r"$9$", [r"$0$", r"$\frac92$", r"$18$"], "B", r"Split at $3$: $\frac92 + \frac92$.", {r"$0$": "the displacement"}),
    ),
    Variants(
        pick(r"A particle has $v(t) = 6t^2$ and $x(0) = -2$. Then $x(1) = $", r"$0$", [r"$2$", r"$4$", r"$-2$"], "D", r"$-2 + \int_0^1 6t^2\,dt = -2 + 2$.", {r"$2$": "forgot the starting position"}),
        pick(r"A particle has $a(t) = 4$ and $v(0) = -3$. Then $v(2) = $", r"$5$", [r"$8$", r"$-3$", r"$11$"], "A", r"$-3 + 8$."),
    ),
    Variants(
        pick(r"A tank holds $30$ L at $t = 0$. Water enters at $10$ L/min and leaves at $2t$ L/min. How much water is in the tank at $t = 4$?", r"$54$", [r"$70$", r"$46$", r"$24$"], "C",
             r"$30 + \int_0^4 (10 - 2t)\,dt = 30 + 40 - 16$.", {r"$70$": "ignored the water leaving", r"$24$": "forgot the starting $30$"}),
        pick(r"Snow depth changes at $6 - t$ cm per hour for $0 \le t \le 8$, and the depth is $10$ cm at $t = 0$. The greatest depth is", r"$28$ cm", [r"$18$ cm", r"$26$ cm", r"$16$ cm"], "A",
             r"$6 - t$ changes from $+$ to $-$ at $t = 6$: $10 + 18 = 28$; at $t = 8$ it is $26$."),
    ),
    Variants(
        pick(r"Water leaks from a tank at $R(t)$ gallons per hour. Which is the best interpretation of $\int_0^5 R(t)\,dt = 40$?", r"A total of $40$ gallons leak out in the first $5$ hours",
             [r"The tank holds $40$ gallons at $t = 5$", r"The leak rate is $40$ gallons per hour at $t = 5$", r"The leak rate changes by $40$ gallons per hour in $5$ hours"], "D", r"The integral of a rate is a total amount."),
        pick(r"$P(t)$ is a population and $t$ is in years. The units of $\int_0^{10} P'(t)\,dt$ are", r"people", [r"people per year", r"years", r"people per year per year"], "B", r"$\int P' = $ change in $P$."),
    ),
    Variants(
        pick(r"The area of the region between $y = x$ and $y = x^2$ is", r"$\frac16$", [r"$\frac12$", r"$\frac13$", r"$\frac56$"], "C", r"$\int_0^1 (x - x^2)\,dx$."),
        pick(r"The area of the region between $y = 2x$ and $y = x^2$ is", r"$\frac43$", [r"$4$", r"$\frac83$", r"$\frac{20}{3}$"], "A", r"$\int_0^2 (2x - x^2)\,dx = 4 - \frac83$."),
    ),
    Variants(
        pick(r"The area of the region between $x = y^2$ and $x = 4$ is", r"$\frac{32}{3}$", [r"$\frac{16}{3}$", r"$16$", r"$8$"], "B", r"$\int_{-2}^2 (4 - y^2)\,dy$.", {r"$\frac{16}{3}$": "only the half above the $x$-axis"}),
        pick(r"The area of the region between $x = y^2$ and $x = y + 2$ is", r"$\frac92$", [r"$\frac{10}{3}$", r"$\frac{7}{6}$", r"$\frac{27}{2}$"], "D", r"$\int_{-1}^2 (y + 2 - y^2)\,dy$."),
    ),
    Variants(
        pick(r"The total area of the regions between $y = x^3$ and $y = x$ is", r"$\frac12$", [r"$0$", r"$\frac14$", r"$1$"], "A", r"Two pieces of $\frac14$.", {r"$0$": "the pieces cancel"}),
        pick(r"The total area between $y = \sin x$ and the $x$-axis for $0 \le x \le 2\pi$ is", r"$4$", [r"$0$", r"$2$", r"$2\pi$"], "C", r"Two arches of area $2$.", {r"$0$": "the arches cancel"}),
    ),
    Variants(
        pick(r"The base of a solid is the region under $y = \sqrt x$ for $0 \le x \le 4$. Cross sections perpendicular to the $x$-axis are squares. The volume is", r"$8$", [r"$\frac{16}{3}$", r"$16$", r"$8\pi$"], "A",
             r"$\int_0^4 (\sqrt x)^2\,dx = 8$.", {r"$8\pi$": "the disc volume"}),
        pick(r"The base of a solid is the region under $y = 2 - x$ for $0 \le x \le 2$. Cross sections perpendicular to the $x$-axis are semicircles. The volume is", r"$\frac\pi3$", [r"$\frac{4\pi}{3}$", r"$\frac{8\pi}{3}$", r"$\frac{\pi}{6}$"], "B",
             r"$\frac\pi8\int_0^2 (2 - x)^2\,dx = \frac\pi8 \cdot \frac83$.", {r"$\frac{4\pi}{3}$": "used $\\frac\\pi2 s^2$ (radius $s$)"}),
    ),
    Variants(
        pick(r"The region under $y = \sqrt x$ for $0 \le x \le 4$ is revolved about the $x$-axis. The volume is", r"$8\pi$", [r"$\frac{16\pi}{3}$", r"$16\pi$", r"$4\pi$"], "D", r"$\pi\int_0^4 x\,dx$.", {r"$\frac{16\pi}{3}$": "forgot to square the radius"}),
        pick(r"The region under $y = x^2$ for $0 \le x \le 1$ is revolved about the $x$-axis. The volume is", r"$\frac\pi5$", [r"$\frac\pi3$", r"$\frac{\pi}{2}$", r"$\pi$"], "C", r"$\pi\int_0^1 x^4\,dx$.", {r"$\frac\pi3$": "forgot to square the radius"}),
    ),
    Variants(
        pick(r"The region between $y = x$ and $y = x^2$ is revolved about the line $y = -1$. Which gives the volume?", r"$\pi\int_0^1 \left((x + 1)^2 - (x^2 + 1)^2\right) dx$",
             [r"$\pi\int_0^1 \left(x^2 - x^4\right) dx$", r"$\pi\int_0^1 \left((x + 1) - (x^2 + 1)\right)^2 dx$", r"$\pi\int_0^1 \left((x - 1)^2 - (x^2 - 1)^2\right) dx$"], "B",
             r"Radii measured from $y = -1$: $R = x + 1$, $r = x^2 + 1$.", {r"$\pi\int_0^1 \left(x^2 - x^4\right) dx$": "about the $x$-axis"}),
        pick(r"The region between $y = x$ and $y = x^2$ is revolved about the $x$-axis. Which gives the volume?", r"$\pi\int_0^1 \left(x^2 - x^4\right) dx$",
             [r"$\pi\int_0^1 \left(x - x^2\right)^2 dx$", r"$\pi\int_0^1 \left(x^4 - x^2\right) dx$", r"$2\pi\int_0^1 \left(x - x^2\right) dx$"], "D", r"$R = x$, $r = x^2$.", {r"$\pi\int_0^1 \left(x - x^2\right)^2 dx$": "squared the difference"}),
    ),
]

# ---------------------------------------------------------------- part B: calculator
b1a = N(sp.sin(x**2), 0, 2) / 2
b1b = N(sp.exp(-x**2), 0, 2) / 2
vA = t * sp.sin(t) - 1
rA = sorted(float(sp.nsolve(vA, t, g)) for g in (1.1, 2.8))
b2a = sum(abs(N(vA, p, q, t)) for p, q in zip([0.0] + rA, rA + [4.0]))
vB = sp.cos(t**2)
rB = [float(sp.sqrt(sp.pi / 2)), float(sp.sqrt(3 * sp.pi / 2)), float(sp.sqrt(5 * sp.pi / 2))]
b2b = sum(abs(N(vB, p, q, t)) for p, q in zip([0.0] + rB, rB + [3.0]))
cA = [float(sp.nsolve(sp.cos(x) - x**2, x, g)) for g in (-0.8, 0.8)]
b3a = N(sp.cos(x) - x**2, cA[0], cA[1])
cB = float(sp.nsolve(2 * sp.sin(x) - x, x, 1.9))
b3b = 2 * N(2 * sp.sin(x) - x, 0, cB)
b4a = float(sp.pi) * N(sp.log(x)**2, 1, 3)
b4b = float(sp.pi * (sp.pi / 4 + 2))
same("B4b", [sp.pi * I((sp.cos(x) + 1)**2 - 1, 0, sp.pi / 2)], [sp.pi * (sp.pi / 4 + 2)])
for name, v in (("b1a", b1a), ("b1b", b1b), ("b2a", b2a), ("b2b", b2b), ("b3a", b3a), ("b3b", b3b), ("b4a", b4a), ("b4b", b4b)):
    close(name, v, round(v, 3), 5e-4)
f3 = lambda v: f"${v:.3f}$"

B = [
    Variants(
        pick(r"The average value of $f(x) = \sin\left(x^2\right)$ on $[0, 2]$ is", f3(b1a), [f3(2 * b1a), r"$0.500$", f3(b1a / 2)], "A", rf"$\frac12\int_0^2 \sin(x^2)\,dx \approx {b1a:.3f}$.", {f3(2 * b1a): "forgot to divide by $2$"}, calc=True),
        pick(r"The average value of $f(x) = e^{-x^2}$ on $[0, 2]$ is", f3(b1b), [f3(2 * b1b), r"$0.500$", f3(b1b / 2)], "C", rf"$\frac12\int_0^2 e^{{-x^2}}\,dx \approx {b1b:.3f}$.", {f3(2 * b1b): "forgot to divide by $2$"}, calc=True),
    ),
    Variants(
        pick(r"A particle moves with $v(t) = t\sin t - 1$ for $0 \le t \le 4$. The total distance traveled is", f3(b2a), [f3(N(vA, 0, 4, t)), f3(abs(N(vA, 0, 4, t))), r"$4.000$"], "B",
             rf"$\int_0^4 |v(t)|\,dt \approx {b2a:.3f}$.", {f3(N(vA, 0, 4, t)): "the displacement"}, calc=True),
        pick(r"A particle moves with $v(t) = \cos\left(t^2\right)$ for $0 \le t \le 3$. The total distance traveled is", f3(b2b), [f3(N(vB, 0, 3, t)), r"$3.000$", f3(2 * b2b)], "D",
             rf"$\int_0^3 |v(t)|\,dt \approx {b2b:.3f}$.", {f3(N(vB, 0, 3, t)): "the displacement"}, calc=True),
    ),
    Variants(
        pick(r"The curves $y = \cos x$ and $y = x^2$ enclose a region. Its area is", f3(b3a), [f3(b3a / 2), f3(2 * b3a), r"$0.824$"], "C", rf"They meet at $x \approx \pm{cA[1]:.4f}$; $\int (\cos x - x^2)\,dx \approx {b3a:.3f}$.", calc=True),
        pick(r"The curves $y = 2\sin x$ and $y = x$ enclose two regions. Their total area is", f3(b3b), [r"$0.000$", f3(b3b / 2), f3(2 * b3b)], "B", rf"They meet at $0$ and $\pm{cB:.4f}$; area $\approx {b3b:.3f}$.", {r"$0.000$": "the pieces cancel"}, calc=True),
    ),
    Variants(
        pick(r"The region under $y = \ln x$ for $1 \le x \le 3$ is revolved about the $x$-axis. The volume is", f3(b4a), [f3(b4a / float(sp.pi)), f3(float(sp.pi) * N(sp.log(x), 1, 3)), f3(2 * b4a)], "A",
             rf"$\pi\int_1^3 (\ln x)^2\,dx \approx {b4a:.3f}$.", {f3(float(sp.pi) * N(sp.log(x), 1, 3)): "forgot to square the radius"}, calc=True),
        pick(r"The region under $y = \cos x$ for $0 \le x \le \frac\pi2$ is revolved about the line $y = -1$. The volume is", f3(b4b), [f3(float(sp.pi**2 / 4)), f3(float(sp.pi * (sp.pi / 4 + 1))), f3(float(sp.pi * (3 * sp.pi / 4 + 2)))], "D",
             rf"$R = \cos x + 1$, $r = 1$: $\pi\int_0^{{\pi/2}} (\cos^2 x + 2\cos x)\,dx = \pi\left(\frac\pi4 + 2\right) \approx {b4b:.3f}$.", {f3(float(sp.pi**2 / 4)): "revolved about the $x$-axis"}, calc=True),
    ),
]

# ---------------------------------------------------------------- FRQ 1: rates from a table
trap = lambda ts, vs: sum(sp.Rational(b - a, 2) * (u + v) for a, b, u, v in zip(ts, ts[1:], vs, vs[1:]))
TA, RA = [0, 3, 5, 9, 12], [20, 26, 30, 24, 18]
TB, RB = [0, 2, 6, 8, 10], [40, 60, 90, 70, 50]
same("F1A", [trap(TA, RA), trap(TA, RA) / 12, 100 + trap(TA, RA) - I(2 * t, 0, 12, t), sp.Rational(24 - 30, 9 - 5)], [296, sp.Rational(74, 3), 252, -sp.Rational(3, 2)])
same("F1B", [trap(TB, RB), trap(TB, RB) / 10, 30 + trap(TB, RB) - I(5 * t, 0, 10, t), sp.Rational(70 - 90, 8 - 6)], [680, 68, 460, -10])


def table_frq(title, intro, ts, rs, unit, start, out_rate, out_tex, total, avg, amount, a, b, slope, tunit, what):
    tab = r"\par\smallskip\centerline{\begin{tabular}{c|ccccc} $t$ (" + tunit + ") & " + " & ".join(map(str, ts)) + r" \\ \hline $R(t)$ (" + unit + ") & " + " & ".join(map(str, rs)) + r"\end{tabular}}"
    pieces = " + ".join(rf"{q - p}\cdot\frac{{{u} + {v}}}{{2}}" for p, q, u, v in zip(ts, ts[1:], rs, rs[1:]))
    return FRQ(title, intro + tab, [
        Part("a", rf"Use a trapezoidal sum with the four subintervals indicated by the table to approximate $\displaystyle\int_{{0}}^{{{ts[-1]}}} R(t)\,dt$. Show the computations that lead to your answer.", num(total),
             rf"${pieces} = {total}$.", [(1, "trapezoidal sum"), (1, "answer")], work="2.4cm"),
        Part("b", rf"Use your answer from part (a) to approximate the average value of $R(t)$ over $0 \le t \le {ts[-1]}$. Indicate units of measure.", num(avg, tol=0.01),
             rf"$\frac{{1}}{{{ts[-1]}}}\int_0^{{{ts[-1]}}} R(t)\,dt \approx \frac{{{total}}}{{{ts[-1]}}} \approx {float(avg):.2f}$ {unit}.", [(1, "divides by the length"), (1, "answer with units")], work="1.8cm"),
        Part("c", rf"{what} at the rate ${out_tex}$ {unit}. At $t = 0$ there are ${start}$. Use your answer from part (a) to approximate the amount at $t = {ts[-1]}$.", num(amount),
             rf"${start} + \int_0^{{{ts[-1]}}} R(t)\,dt - \int_0^{{{ts[-1]}}} {out_tex}\,dt \approx {start} + {total} - {int(I(out_rate, 0, ts[-1], t))} = {amount}$.",
             [(1, "start + in $-$ out"), (1, "integral of the out-rate"), (1, "answer")], work="2.6cm"),
        Part("d", rf"$R$ is differentiable. Must there be a time $t$, ${a} < t < {b}$, at which $R'(t) = {sp.latex(slope)}$? Justify your answer.", selfcheck(r"\text{Yes, by the Mean Value Theorem}"),
             rf"$R$ is differentiable, hence continuous, on $[{a}, {b}]$, and $\frac{{R({b}) - R({a})}}{{{b} - {a}}} = {sp.latex(slope)}$. By the Mean Value Theorem, yes.", [(1, "difference quotient"), (1, "MVT with conditions")], work="2cm"),
    ], frq_type="Table")


F1A = table_frq("Water in a tank", r"Water is pumped into a tank at a rate modeled by a differentiable function $R$, where $R(t)$ is in gallons per hour and $t$ is in hours. Selected values are in the table.",
                TA, RA, "gallons per hour", "100 \\text{ gallons}", 2 * t, "D(t) = 2t", 296, sp.Rational(74, 3), 252, 5, 9, -sp.Rational(3, 2), "hours", "Water also drains from the tank")
F1B = table_frq("Visitors at a fair", r"Visitors enter a fair at a rate modeled by a differentiable function $R$, where $R(t)$ is in people per hour and $t$ is in hours after the gates open. Selected values are in the table.",
                TB, RB, "people per hour", "30 \\text{ people}", 5 * t, "L(t) = 5t", 680, 68, 460, 6, 8, -10, "hours", "Visitors leave the fair")

# ---------------------------------------------------------------- FRQ 2: particle motion
vA2 = t**2 - 6 * t + 5
vB2 = 3 * t**2 - 12 * t + 9
same("F2A", [dist(vA2, 0, 6), 2 + I(vA2, 0, 6, t), vA2.subs(t, 2), sp.diff(vA2, t).subs(t, 2)], [sp.Rational(46, 3), -4, -3, -2])
same("F2B", [dist(vB2, 0, 4), 1 + I(vB2, 0, 4, t), vB2.subs(t, sp.Rational(5, 2)), sp.diff(vB2, t).subs(t, sp.Rational(5, 2))], [12, 5, -sp.Rational(9, 4), 3])
F2A = FRQ("A particle on a line", (r"A particle moves along the $x$-axis with velocity $v(t) = t^2 - 6t + 5$ for $0 \le t \le 6$. At $t = 0$ the particle is at $x = 2$."), [
    Part("a", r"At what times $t$, $0 < t < 6$, does the particle change direction? Justify your answer.", selfcheck(r"t = 1 \text{ and } t = 5"),
         r"$v(t) = (t - 1)(t - 5)$ changes sign at $t = 1$ ($+$ to $-$) and $t = 5$ ($-$ to $+$).", [(1, "both times"), (1, "sign-change justification")], work="2cm"),
    Part("b", r"Find the total distance traveled by the particle for $0 \le t \le 6$.", num(sp.Rational(46, 3)),
         r"$\int_0^1 v = \frac73$, $\int_1^5 v = -\frac{32}{3}$, $\int_5^6 v = \frac73$. Distance $= \frac73 + \frac{32}{3} + \frac73 = \frac{46}{3}$.", [(1, "splits at turns"), (1, "integrals"), (1, "answer")], work="3cm"),
    Part("c", r"Find the position of the particle at $t = 6$.", num(-4), r"$2 + \int_0^6 v(t)\,dt = 2 + \left(\frac73 - \frac{32}{3} + \frac73\right) = 2 - 6 = -4$.", [(1, "answer")], work="1.8cm"),
    Part("d", r"Is the speed of the particle increasing or decreasing at $t = 2$? Give a reason for your answer.", selfcheck(r"\text{increasing}"),
         r"$v(2) = -3 < 0$ and $a(2) = v'(2) = 2(2) - 6 = -2 < 0$. Same sign: the speed is increasing.", [(1, "$v(2)$ and $a(2)$"), (1, "increasing with reason")], work="1.8cm"),
], frq_type="Particle motion")
F2B = FRQ("A particle on a line", (r"A particle moves along the $x$-axis with velocity $v(t) = 3t^2 - 12t + 9$ for $0 \le t \le 4$. At $t = 0$ the particle is at $x = 1$."), [
    Part("a", r"At what times $t$, $0 < t < 4$, does the particle change direction? Justify your answer.", selfcheck(r"t = 1 \text{ and } t = 3"),
         r"$v(t) = 3(t - 1)(t - 3)$ changes sign at $t = 1$ ($+$ to $-$) and $t = 3$ ($-$ to $+$).", [(1, "both times"), (1, "sign-change justification")], work="2cm"),
    Part("b", r"Find the total distance traveled by the particle for $0 \le t \le 4$.", num(12),
         r"With $\int v\,dt = t^3 - 6t^2 + 9t$: $\int_0^1 v = 4$, $\int_1^3 v = -4$, $\int_3^4 v = 4$. Distance $= 12$.", [(1, "splits at turns"), (1, "integrals"), (1, "answer")], work="3cm"),
    Part("c", r"Find the position of the particle at $t = 4$.", num(5), r"$1 + \int_0^4 v(t)\,dt = 1 + 4 = 5$.", [(1, "answer")], work="1.8cm"),
    Part("d", r"Is the speed of the particle increasing or decreasing at $t = 2.5$? Give a reason for your answer.", selfcheck(r"\text{decreasing}"),
         r"$v(2.5) = -2.25 < 0$ and $a(2.5) = 6(2.5) - 12 = 3 > 0$. Opposite signs: the speed is decreasing.", [(1, "$v(2.5)$ and $a(2.5)$"), (1, "decreasing with reason")], work="1.8cm"),
], frq_type="Particle motion")

# ---------------------------------------------------------------- FRQ 3: area and volume
same("F3A", [I(2 * x - x**2, 0, 2), sp.pi * I(4 * x**2 - x**4, 0, 2), I((2 * x - x**2)**2, 0, 2)], [sp.Rational(4, 3), 64 * sp.pi / 15, sp.Rational(16, 15)])
same("F3B", [I(x - x**2 / 2, 0, 2), sp.pi * I(x**2 - x**4 / 4, 0, 2), sp.pi / 8 * I((x - x**2 / 2)**2, 0, 2)], [sp.Rational(2, 3), 16 * sp.pi / 15, sp.pi / 30])
FIG3A = region("tU8_3a", [("2*x", -0.2, 2.2), ("x^2", -0.2, 2.15)], (-0.4, 2.4), (-0.4, 4.6), [(lambda v: 2 * v, lambda v: v * v, 0, 2)], labels=[(1.1, 1.6, "center", "$R$")],
               caption=r"Region $R$, between $y = 2x$ and $y = x^2$.")
FIG3B = region("tU8_3b", [("x", -0.2, 2.3), ("x^2/2", -0.2, 2.3)], (-0.4, 2.5), (-0.4, 2.6), [(lambda v: v, lambda v: v * v / 2, 0, 2)], labels=[(1.1, 0.85, "center", "$R$")],
               caption=r"Region $R$, between $y = x$ and $y = \frac{x^2}{2}$.")
F3A = FRQ("Area and volume", (r"Let $R$ be the region bounded by the graphs of $y = 2x$ and $y = x^2$, as shown."), [
    Part("a", r"Find the area of $R$.", num(sp.Rational(4, 3)), r"They meet at $x = 0$ and $x = 2$. $\int_0^2 (2x - x^2)\,dx = 4 - \frac83 = \frac43$.", [(1, "limits and integral"), (1, "answer")], work="2.2cm"),
    Part("b", r"Find the volume of the solid generated when $R$ is revolved about the $x$-axis.", num(64 * sp.pi / 15, tol=0.01, display=r"\tfrac{64\pi}{15}"),
         r"$R_{\text{out}} = 2x$, $r_{\text{in}} = x^2$: $\pi\int_0^2 \left(4x^2 - x^4\right) dx = \pi\left(\frac{32}{3} - \frac{32}{5}\right) = \frac{64\pi}{15}$.", [(1, "radii"), (1, "integral"), (1, "answer")], work="2.8cm"),
    Part("c", r"Write, but do not evaluate, an integral expression for the volume of the solid generated when $R$ is revolved about the horizontal line $y = 4$.", selfcheck(r"\pi\int_0^2 \left((4 - x^2)^2 - (4 - 2x)^2\right) dx"),
         r"The axis is above $R$, so the parabola is farther: $R_{\text{out}} = 4 - x^2$, $r_{\text{in}} = 4 - 2x$. $V = \pi\int_0^2 \left((4 - x^2)^2 - (4 - 2x)^2\right) dx$.", [(1, "radii"), (1, "integral expression")], work="2.2cm"),
    Part("d", r"$R$ is the base of a solid whose cross sections perpendicular to the $x$-axis are squares. Find the volume of the solid.", num(sp.Rational(16, 15)),
         r"$\int_0^2 (2x - x^2)^2\,dx = \int_0^2 \left(4x^2 - 4x^3 + x^4\right) dx = \frac{32}{3} - 16 + \frac{32}{5} = \frac{16}{15}$.", [(1, "integrand"), (1, "answer")], work="2.2cm"),
], frq_type="Area and volume", figure=FIG3A)
F3B = FRQ("Area and volume", (r"Let $R$ be the region bounded by the graphs of $y = x$ and $y = \frac{x^2}{2}$, as shown."), [
    Part("a", r"Find the area of $R$.", num(sp.Rational(2, 3)), r"They meet at $x = 0$ and $x = 2$. $\int_0^2 \left(x - \frac{x^2}{2}\right) dx = 2 - \frac43 = \frac23$.", [(1, "limits and integral"), (1, "answer")], work="2.2cm"),
    Part("b", r"Find the volume of the solid generated when $R$ is revolved about the $x$-axis.", num(16 * sp.pi / 15, tol=0.01, display=r"\tfrac{16\pi}{15}"),
         r"$R_{\text{out}} = x$, $r_{\text{in}} = \frac{x^2}{2}$: $\pi\int_0^2 \left(x^2 - \frac{x^4}{4}\right) dx = \pi\left(\frac83 - \frac85\right) = \frac{16\pi}{15}$.", [(1, "radii"), (1, "integral"), (1, "answer")], work="2.8cm"),
    Part("c", r"Write, but do not evaluate, an integral expression for the volume of the solid generated when $R$ is revolved about the horizontal line $y = -1$.", selfcheck(r"\pi\int_0^2 \left((x + 1)^2 - \left(\tfrac{x^2}{2} + 1\right)^2\right) dx"),
         r"$R_{\text{out}} = x + 1$, $r_{\text{in}} = \frac{x^2}{2} + 1$. $V = \pi\int_0^2 \left((x + 1)^2 - \left(\frac{x^2}{2} + 1\right)^2\right) dx$.", [(1, "radii"), (1, "integral expression")], work="2.2cm"),
    Part("d", r"$R$ is the base of a solid whose cross sections perpendicular to the $x$-axis are semicircles. Find the volume of the solid.", num(sp.pi / 30, tol=1e-4, display=r"\tfrac{\pi}{30}"),
         r"$\frac\pi8\int_0^2 \left(x - \frac{x^2}{2}\right)^2 dx = \frac\pi8\left(\frac83 - 4 + \frac85\right) = \frac\pi8 \cdot \frac{4}{15} = \frac{\pi}{30}$.", [(1, "semicircle area"), (1, "answer")], work="2.2cm"),
], frq_type="Area and volume", figure=FIG3B)

TEST = UnitTest(unit=8, title="Applications of Integration", mcq_a=A, mcq_b=B,
                frq=[Variants(F1A, F1B), Variants(F2A, F2B), Variants(F3A, F3B)])
