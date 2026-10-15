"""Unit 8 BC test: the whole of Unit 8, BC topic 8.13 (arc length) included (docs/ab-bc-versions.md).

Built from the AB test (content/unit_8.py) in the same AP format and forms: two no-calculator slots and one calculator
slot give way to arc length, and FRQ 3's "revolve about a line" part becomes a perimeter (arc length) part. Item ids
start "u8bc", so scores never mix with the AB test's. Every key is checked with sympy.
"""
from dataclasses import replace

import sympy as sp

from calclib import Part, UnitTest, Variants, close, same, selfcheck
from content import unit_8 as ab
from content.unit_8 import pick

x = sp.symbols("x", real=True)
I = lambda f, a, b: sp.simplify(sp.integrate(f, (x, a, b)))
arc = lambda f, a, b: sp.Integral(sp.sqrt(1 + sp.diff(f, x)**2), (x, a, b))

# ---------------------------------------------------------------- the BC slots (no calculator)
same("arc integrands", [sp.diff(x**2, x)**2, sp.diff(sp.sin(x), x)**2], [4 * x**2, sp.cos(x)**2])
SETUP = Variants(
    pick(r"Which integral gives the length of the graph of $y = x^2$ from $x = 0$ to $x = 2$?", r"$\int_0^2 \sqrt{1 + 4x^2}\,dx$",
         [r"$\int_0^2 \sqrt{1 + x^4}\,dx$", r"$\int_0^2 (1 + 2x)\,dx$", r"$\int_0^2 \sqrt{1 + 2x}\,dx$"], "D",
         r"Length $= \int_a^b \sqrt{1 + \left(\frac{dy}{dx}\right)^2}\,dx$ with $\frac{dy}{dx} = 2x$, so $\left(\frac{dy}{dx}\right)^2 = 4x^2$.",
         {r"$\int_0^2 \sqrt{1 + x^4}\,dx$": "squared $y$ instead of $\\frac{dy}{dx}$", r"$\int_0^2 \sqrt{1 + 2x}\,dx$": "forgot to square $\\frac{dy}{dx}$"}),
    pick(r"Which integral gives the length of the graph of $y = \sin x$ from $x = 0$ to $x = \pi$?", r"$\int_0^\pi \sqrt{1 + \cos^2 x}\,dx$",
         [r"$\int_0^\pi \sqrt{1 + \sin^2 x}\,dx$", r"$\int_0^\pi (1 + \cos x)\,dx$", r"$\int_0^\pi \sqrt{1 - \cos^2 x}\,dx$"], "B",
         r"$\frac{dy}{dx} = \cos x$, so the length is $\int_0^\pi \sqrt{1 + \cos^2 x}\,dx$.", {r"$\int_0^\pi \sqrt{1 + \sin^2 x}\,dx$": "squared $y$ instead of $\\frac{dy}{dx}$"}),
)
g = sp.Rational(2, 3) * x**sp.Rational(3, 2)
same("arc exact", [sp.simplify(1 + sp.diff(g, x)**2 - (1 + x)), I(sp.sqrt(1 + x), 0, 3), I(sp.sqrt(1 + x), 0, 8), g.subs(x, 3)], [0, sp.Rational(14, 3), sp.Rational(52, 3), 2 * sp.sqrt(3)])
EXACT = Variants(
    pick(r"The length of the graph of $y = \frac23 x^{3/2}$ from $x = 0$ to $x = 3$ is", r"$\frac{14}{3}$", [r"$2\sqrt3$", r"$7$", r"$\frac{16}{3}$"], "A",
         r"$\frac{dy}{dx} = x^{1/2}$, so $1 + \left(\frac{dy}{dx}\right)^2 = 1 + x$. $\int_0^3 \sqrt{1 + x}\,dx = \left[\frac23(1 + x)^{3/2}\right]_0^3 = \frac23(8 - 1) = \frac{14}{3}$.",
         {r"$2\sqrt3$": "that's $y(3)$, the height"}),
    pick(r"The length of the graph of $y = \frac23 x^{3/2}$ from $x = 0$ to $x = 8$ is", r"$\frac{52}{3}$", [r"$18$", r"$\frac{32\sqrt2}{3}$", r"$26$"], "C",
         r"$\frac{dy}{dx} = x^{1/2}$, so the length is $\int_0^8 \sqrt{1 + x}\,dx = \frac23\left(27 - 1\right) = \frac{52}{3}$.", {r"$\frac{32\sqrt2}{3}$": "that's $y(8)$, the height"}),
)

# the AB test's slots 2 (a second average-value question) and 9 (a third area question) make room
A = list(ab.A)
A[1], A[8] = SETUP, EXACT

# ---------------------------------------------------------------- calculator: an arc length
cA = float(arc(sp.sin(x), 0, sp.pi).evalf())
cB = float(arc(sp.exp(x), 0, 1).evalf())
close("B3 arc A", cA, 3.820, 5e-4)
close("B3 arc B", cB, 2.003, 5e-4)
f3 = lambda v: f"${v:.3f}$"
CALC = Variants(
    pick(r"The length of the graph of $y = \sin x$ from $x = 0$ to $x = \pi$ is", f3(cA), [r"$3.142$", r"$2.000$", r"$7.640$"], "C",
         rf"$\int_0^\pi \sqrt{{1 + \cos^2 x}}\,dx \approx {cA:.3f}$.", {r"$3.142$": "the length of the interval", r"$2.000$": "the area under the arch"}, calc=True),
    pick(r"The length of the graph of $y = e^x$ from $x = 0$ to $x = 1$ is", f3(cB), [r"$1.718$", r"$1.414$", r"$2.718$"], "B",
         rf"$\int_0^1 \sqrt{{1 + e^{{2x}}}}\,dx \approx {cB:.3f}$.", {r"$1.718$": "the area under the curve"}, calc=True),
)
B = list(ab.B)
B[2] = CALC

# ---------------------------------------------------------------- FRQ 3: a perimeter in place of the second washer
same("F3 perimeter", [sp.sqrt(2**2 + 4**2), sp.sqrt(2**2 + 2**2), sp.diff(x**2, x)**2, sp.diff(x**2 / 2, x)**2], [2 * sp.sqrt(5), 2 * sp.sqrt(2), 4 * x**2, x**2])
perA = Part("c", r"Write, but do not evaluate, an expression involving one or more integrals that gives the perimeter of $R$.", selfcheck(r"2\sqrt5 + \int_0^2 \sqrt{1 + 4x^2}\,dx"),
            r"The boundary is the segment of $y = 2x$ from $(0, 0)$ to $(2, 4)$, of length $\sqrt{2^2 + 4^2} = 2\sqrt5$, and the arc of $y = x^2$, with $\frac{dy}{dx} = 2x$. "
            r"Perimeter $= 2\sqrt5 + \int_0^2 \sqrt{1 + 4x^2}\,dx$.", [(1, "arc length integral for $y = x^2$"), (1, "perimeter expression")], work="2.2cm")
perB = Part("c", r"Write, but do not evaluate, an expression involving one or more integrals that gives the perimeter of $R$.", selfcheck(r"2\sqrt2 + \int_0^2 \sqrt{1 + x^2}\,dx"),
            r"The boundary is the segment of $y = x$ from $(0, 0)$ to $(2, 2)$, of length $2\sqrt2$, and the arc of $y = \frac{x^2}{2}$, with $\frac{dy}{dx} = x$. "
            r"Perimeter $= 2\sqrt2 + \int_0^2 \sqrt{1 + x^2}\,dx$.", [(1, "arc length integral for $y = \\frac{x^2}{2}$"), (1, "perimeter expression")], work="2.2cm")
F3A = replace(ab.F3A, parts=[perA if p.label == "c" else p for p in ab.F3A.parts])
F3B = replace(ab.F3B, parts=[perB if p.label == "c" else p for p in ab.F3B.parts])

TEST = UnitTest(unit=8, version="BC", title="Applications of Integration", mcq_a=A, mcq_b=B,
                frq=[Variants(ab.F1A, ab.F1B), Variants(ab.F2A, ab.F2B), Variants(F3A, F3B)])
