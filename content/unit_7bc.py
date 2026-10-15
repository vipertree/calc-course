"""Unit 7 BC test: the whole of Unit 7, BC topics 7.5 (Euler's method) and 7.9 (logistic models) included
(docs/ab-bc-versions.md).

Built from the AB test (content/unit_7.py) in the same AP format and forms: three no-calculator slots give way to
Euler's method and logistic models, the calculator tangent-line slot becomes a two-step Euler approximation, FRQ 1's
tangent-line part becomes an Euler's method part, and FRQ 3 becomes a logistic-model question. Item ids start
"u7bc", so scores never mix with the AB test's. Every key is checked with sympy.
"""
from dataclasses import replace

import sympy as sp

from calclib import FRQ, Part, UnitTest, Variants, check, close, num, same, selfcheck
from content import unit_7 as ab
from content.unit_7 import pick

x, y, t = sp.symbols("x y t", real=True)


def euler(rhs, x0, y0, h, n):
    """n steps of Euler's method for dy/dx = rhs(x, y) from (x0, y0), exactly when the inputs are rational."""
    for _ in range(n):
        y0 = y0 + h * rhs(x0, y0)
        x0 = x0 + h
    return y0


f3 = lambda v: f"${float(v):.3f}$"

# ---------------------------------------------------------------- the BC slots (no calculator)
h = sp.Rational(1, 2)
same("Euler A", [euler(lambda a, b: a + b, 0, 1, h, 2), euler(lambda a, b: a + b, 0, 1, 1, 1)], [sp.Rational(5, 2), 2])
same("Euler B", [euler(lambda a, b: b - a, 0, 3, h, 2), euler(lambda a, b: b - a, 0, 3, 1, 1)], [sp.Rational(13, 2), 6])
EULER = Variants(
    pick(r"$y = f(x)$ is the solution of $\frac{dy}{dx} = x + y$ with $f(0) = 1$. Euler's method with two steps of size $0.5$, starting at $x = 0$, gives $f(1) \approx$",
         r"$2.5$", [r"$2$", r"$3$", r"$2e - 2$"], "C",
         r"Slope at $(0, 1)$ is $1$: $f(0.5) \approx 1 + 0.5(1) = 1.5$. Slope at $(0.5, 1.5)$ is $2$: $f(1) \approx 1.5 + 0.5(2) = 2.5$.",
         {r"$2$": "one step of size $1$", r"$2e - 2$": "the exact value, not Euler's approximation"}),
    pick(r"$y = f(x)$ is the solution of $\frac{dy}{dx} = y - x$ with $f(0) = 3$. Euler's method with two steps of size $0.5$, starting at $x = 0$, gives $f(1) \approx$",
         r"$6.5$", [r"$6$", r"$5$", r"$7$"], "A",
         r"Slope at $(0, 3)$ is $3$: $f(0.5) \approx 3 + 0.5(3) = 4.5$. Slope at $(0.5, 4.5)$ is $4$: $f(1) \approx 4.5 + 0.5(4) = 6.5$.", {r"$6$": "one step of size $1$"}),
)
LIMIT = Variants(
    pick(r"$\frac{dP}{dt} = 0.2P\left(1 - \frac{P}{500}\right)$ and $P(0) = 600$. Then $\lim_{t\to\infty} P(t) = $", r"$500$", [r"$600$", r"$250$", r"$\infty$"], "B",
         r"A logistic model approaches its carrying capacity, $500$. Here $P$ starts above it, so $\frac{dP}{dt} < 0$ and $P$ falls toward $500$.", {r"$250$": "where the growth is fastest"}),
    pick(r"$\frac{dy}{dt} = 3y(8 - y)$ and $y(0) = 2$. Then $\lim_{t\to\infty} y(t) = $", r"$8$", [r"$2$", r"$4$", r"$\infty$"], "D",
         r"The carrying capacity is $8$: for $0 < y < 8$ the rate is positive, and it shrinks to $0$ as $y$ nears $8$.", {r"$4$": "where the growth is fastest"}),
)
same("logistic fastest", [sp.solve(sp.diff(sp.Rational(2, 5) * y * (1 - y / 1200), y), y)[0], sp.solve(sp.diff(y * (10 - y) / 5, y), y)[0]], [600, 5])
FASTEST = Variants(
    pick(r"A population satisfies $\frac{dP}{dt} = 0.4P\left(1 - \frac{P}{1200}\right)$ with $P(0) = 100$. The population is growing fastest when $P = $", r"$600$",
         [r"$1200$", r"$100$", r"$300$"], "A", r"A logistic population grows fastest at half its carrying capacity: $\frac{1200}{2} = 600$."),
    pick(r"$\frac{dy}{dt} = \frac{y(10 - y)}{5}$ with $y(0) = 1$. $y$ is increasing fastest when $y = $", r"$5$", [r"$10$", r"$1$", r"$\frac52$"], "C",
         r"$\frac{dy}{dt}$ is a downward parabola in $y$ with zeros $0$ and $10$, so it is greatest at $y = 5$, half the carrying capacity."),
)

# the AB test's slots 2 (a modeling statement), 5 (the second derivative from dy/dx) and 12 (where a particular
# solution is defined) make room
A = list(ab.A)
for k, slot in ((1, EULER), (4, LIMIT), (11, FASTEST)):
    A[k] = slot

# ---------------------------------------------------------------- calculator: two Euler steps
rA = lambda a, b: sp.sqrt(a + b**2)
rB = lambda a, b: sp.log(a + b)
eA = sp.N(euler(rA, 1, 2, sp.Rational(1, 10), 2), 20)
eB = sp.N(euler(rB, 2, 3, sp.Rational(1, 2), 2), 20)
close("B4 Euler A", eA, 2.469, 5e-4)
close("B4 Euler B", eB, 4.725, 5e-4)
EULER_CALC = Variants(
    pick(r"$y = f(x)$ solves $\frac{dy}{dx} = \sqrt{x + y^2}$ with $f(1) = 2$. Euler's method with two steps of size $0.1$, starting at $x = 1$, gives $f(1.2) \approx $", f3(eA),
         [r"$2.447$", r"$2.224$", r"$2.200$"], "B",
         rf"$f(1.1) \approx 2 + 0.1\sqrt5 \approx 2.2236$; then $f(1.2) \approx 2.2236 + 0.1\sqrt{{1.1 + 2.2236^2}} \approx {float(eA):.3f}$.", {r"$2.447$": "one step of size $0.2$", r"$2.224$": "only the first step"}, calc=True),
    pick(r"$y = f(x)$ solves $\frac{dy}{dx} = \ln(x + y)$ with $f(2) = 3$. Euler's method with two steps of size $0.5$, starting at $x = 2$, gives $f(3) \approx $", f3(eB),
         [r"$4.609$", r"$3.805$", r"$4.000$"], "D",
         rf"$f(2.5) \approx 3 + 0.5\ln 5 \approx 3.8047$; then $f(3) \approx 3.8047 + 0.5\ln(6.3047) \approx {float(eB):.3f}$.", {r"$4.609$": "one step of size $1$", r"$3.805$": "only the first step"}, calc=True),
)
B = list(ab.B)
B[3] = EULER_CALC

# ---------------------------------------------------------------- FRQ 1: Euler's method in place of the tangent line
same("F1 Euler", [euler(ab.rA, 1, 0, sp.Rational(1, 10), 2), euler(ab.rB, 2, 1, sp.Rational(1, 10), 2)], [sp.Rational(398, 1000), sp.Rational(801, 1000)])
eulerA = Part("b", r"Use Euler's method, starting at $x = 1$ with two steps of equal size, to approximate $f(1.2)$. Show the work that leads to your answer.", num(sp.Rational(398, 1000)),
              r"$\frac{dy}{dx}$ at $(1, 0)$ is $1(2 - 0) = 2$, so $f(1.1) \approx 0 + 0.1(2) = 0.2$. At $(1.1, 0.2)$ it is $1.1(1.8) = 1.98$, so $f(1.2) \approx 0.2 + 0.1(1.98) = 0.398$.",
              [(1, "Euler's method with two steps"), (1, "approximation")], work="2.4cm")
eulerB = Part("b", r"Use Euler's method, starting at $x = 2$ with two steps of equal size, to approximate $f(2.2)$. Show the work that leads to your answer.", num(sp.Rational(801, 1000)),
              r"$\frac{dy}{dx}$ at $(2, 1)$ is $1(1 - 2) = -1$, so $f(2.1) \approx 1 + 0.1(-1) = 0.9$. At $(2.1, 0.9)$ it is $0.9(-1.1) = -0.99$, so $f(2.2) \approx 0.9 + 0.1(-0.99) = 0.801$.",
              [(1, "Euler's method with two steps"), (1, "approximation")], work="2.4cm")
F1A = replace(ab.F1A, parts=[eulerA if p.label == "b" else p for p in ab.F1A.parts])
F1B = replace(ab.F1B, parts=[eulerB if p.label == "b" else p for p in ab.F1B.parts])


# ---------------------------------------------------------------- FRQ 3 (BC): a logistic model
def logistic_frq(intro, var, M, c, start, at, unit_t, things):
    P, start = sp.Symbol(var), sp.Integer(start)
    rate = P * (M - P) / c
    second = sp.factor(sp.diff(rate, P) * rate)
    e = euler(lambda a, b: b * (M - b) / sp.Integer(c), 0, start, 1, 2)
    r0 = start * (M - start) / sp.Integer(c)
    p1 = start + r0
    r1 = p1 * (M - p1) / sp.Integer(c)
    same(f"logistic {var} Euler", [p1 + r1], [e])
    same(f"logistic {var}", [sp.diff(rate, P).subs(P, sp.Rational(M, 2)), second - (M - 2 * P) * P * (M - P) / c**2], [0, 0])
    check(f"logistic {var} concave up at {at}", second.subs(P, at) > 0)
    d = sp.latex(sp.Symbol(var))
    return FRQ("A logistic model", intro, [
        Part("a", rf"Find $\displaystyle\lim_{{t\to\infty}} {d}(t)$.", num(M), rf"The carrying capacity: ${d}(0) = {start}$ is between $0$ and ${M}$, so ${d}(t) \to {M}$.", [(1, "answer")], work="1.4cm"),
        Part("b", rf"What is the number of {things} when ${d}$ is growing the fastest?", num(M // 2), rf"A logistic model grows fastest at half the carrying capacity: ${d} = {M // 2}$.",
             [(1, "answer")], work="1.4cm"),
        Part("c", rf"Find $\dfrac{{d^2{d}}}{{dt^2}}$ in terms of ${d}$. Is the graph of ${d}$ concave up or concave down when ${d} = {at}$? Give a reason for your answer.",
             selfcheck(rf"\frac{{d^2{d}}}{{dt^2}} = \frac{{{M} - 2{d}}}{{{c}}}\cdot\frac{{d{d}}}{{dt}};\ \text{{concave up}}"),
             rf"$\dfrac{{d^2{d}}}{{dt^2}} = \dfrac{{{M} - 2{d}}}{{{c}}}\cdot\dfrac{{d{d}}}{{dt}} = \dfrac{{({M} - 2{d}){d}({M} - {d})}}{{{c**2}}}$. At ${d} = {at}$ both factors are positive, "
             rf"so $\dfrac{{d^2{d}}}{{dt^2}} > 0$ and the graph is concave up.", [(1, rf"$\frac{{d^2{d}}}{{dt^2}}$"), (1, "concave up with reason")], work="2.6cm"),
        Part("d", rf"Use Euler's method, starting at $t = 0$ with two steps of equal size, to approximate ${d}(2)$. Show the work that leads to your answer.", num(e, tol=1e-3),
             rf"${d}'(0) = \frac{{{start}({M - start})}}{{{c}}} = {sp.latex(r0)}$, so ${d}(1) \approx {start} + {sp.latex(r0)} = {sp.latex(p1)}$. "
             rf"Then ${d}'(1) \approx \frac{{{sp.latex(p1)}({sp.latex(M - p1)})}}{{{c}}} = {float(r1):g}$, so ${d}(2) \approx {sp.latex(p1)} + {float(r1):g} = {float(e):g}$ {unit_t}.", [(1, "Euler's method with two steps"), (1, "approximation")], work="2.4cm"),
    ], frq_type="Differential equation")


F3A = logistic_frq(r"The number of fish in a lake is modeled by a function $P$ that satisfies the logistic differential equation $\dfrac{dP}{dt} = \dfrac{P(1000 - P)}{2000}$, "
                   r"where $t$ is measured in years. At time $t = 0$ there are $200$ fish in the lake.", "P", 1000, 2000, 200, 200, "fish", "fish")
F3B = logistic_frq(r"The number of people who have heard a rumor is modeled by a function $R$ that satisfies the logistic differential equation $\dfrac{dR}{dt} = \dfrac{R(400 - R)}{1000}$, "
                   r"where $t$ is measured in hours. At time $t = 0$, $100$ people have heard the rumor.", "R", 400, 1000, 100, 100, "people", "people who have heard the rumor")
same("F3 Euler", [euler(lambda a, b: b * (1000 - b) / 2000, 0, 200, 1, 2), euler(lambda a, b: b * (400 - b) / 1000, 0, 100, 1, 2)], [sp.Rational(3808, 10), sp.Rational(1651, 10)])

TEST = UnitTest(unit=7, version="BC", title="Differential Equations", mcq_a=A, mcq_b=B,
                frq=[Variants(F1A, F1B), Variants(ab.F2A, ab.F2B), Variants(F3A, F3B)])
