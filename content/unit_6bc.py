"""Unit 6 BC test: the whole of Unit 6, BC topics 6.11-6.13 and 6.14 BC included (docs/ab-bc-versions.md).

Same AP format and forms as the AB test (content/unit_6.py), which it is built from: four no-calculator slots of the
AB test give way to integration by parts (6.11), partial fractions (6.12), an improper integral (6.13) and a BC
technique choice (6.14 BC), and the third FRQ becomes a BC question on parts, partial fractions and improper
integrals. Item ids start "u6bc", so scores never mix with the AB test's. Every key is checked with sympy.
"""
import sympy as sp

from calclib import FRQ, Part, UnitTest, Variants, num, same, selfcheck
from content import unit_6 as ab
from content.unit_6 import pick

x, t = sp.symbols("x t", real=True)
I = lambda f, a, b: sp.simplify(sp.integrate(f, (x, a, b)))
L = lambda e: sp.log(sp.Abs(e))


def antideriv(F, f):
    """F' = f, checked at two points (logs of absolute values stay real there)."""
    for v in (sp.Rational(37, 7), sp.Rational(53, 9)):
        assert abs(sp.N((sp.diff(F, x) - f).subs(x, v))) < 1e-12, (F, f)


# ---------------------------------------------------------------- the BC slots (no calculator)
antideriv(x / 2 * sp.sin(2 * x) + sp.cos(2 * x) / 4, x * sp.cos(2 * x))
antideriv(-x * sp.exp(-x) - sp.exp(-x), x * sp.exp(-x))
antideriv(L(x - 1) - L(x + 2), 3 / ((x - 1) * (x + 2)))
antideriv(x**3 / 3 * sp.log(x) - x**3 / 9, x**2 * sp.log(x))
antideriv(x * sp.log(x) - x, sp.log(x))
same("BC improper", [sp.integrate(x**-3, (x, 1, sp.oo)), I(2 / ((x - 1) * (x + 1)), 3, 5)], [sp.Rational(1, 2), sp.log(sp.Rational(4, 3))])
same("BC converge", [sp.integrate(x**-2, (x, 1, sp.oo)), sp.integrate(x**sp.Rational(-1, 2), (x, 1, sp.oo)), sp.integrate(1 / x, (x, 1, sp.oo))], [1, sp.oo, sp.oo])

PARTS = Variants(
    pick(r"$\displaystyle\int x\cos(2x)\,dx = $", r"$\frac x2\sin(2x) + \frac14\cos(2x) + C$",
         [r"$\frac x2\sin(2x) - \frac14\cos(2x) + C$", r"$\frac{x^2}{4}\sin(2x) + C$", r"$-\frac x2\cos(2x) + \frac14\sin(2x) + C$"], "D",
         r"Parts, $u = x$, $dv = \cos(2x)\,dx$: $du = dx$, $v = \frac12\sin(2x)$. $\frac x2\sin(2x) - \int \frac12\sin(2x)\,dx = \frac x2\sin(2x) + \frac14\cos(2x) + C$.",
         {r"$\frac x2\sin(2x) - \frac14\cos(2x) + C$": "the integral of $\\sin$ is $-\\cos$", r"$-\frac x2\cos(2x) + \frac14\sin(2x) + C$": "that's $\\int x\\sin(2x)\\,dx$"}),
    pick(r"$\displaystyle\int x e^{-x}\,dx = $", r"$-xe^{-x} - e^{-x} + C$", [r"$-xe^{-x} + e^{-x} + C$", r"$xe^{-x} - e^{-x} + C$", r"$-\frac{x^2}{2}e^{-x} + C$"], "A",
         r"Parts, $u = x$, $dv = e^{-x}\,dx$: $du = dx$, $v = -e^{-x}$. $-xe^{-x} - \int \left(-e^{-x}\right) dx = -xe^{-x} - e^{-x} + C$."),
)
PARTIAL = Variants(
    pick(r"$\displaystyle\int \frac{3}{(x - 1)(x + 2)}\,dx = $", r"$\ln|x - 1| - \ln|x + 2| + C$",
         [r"$\ln|x + 2| - \ln|x - 1| + C$", r"$3\ln|(x - 1)(x + 2)| + C$", r"$\ln|x - 1| + \ln|x + 2| + C$"], "D",
         r"$3 = A(x + 2) + B(x - 1)$. Let $x = 1$: $3 = 3A$, so $A = 1$. Let $x = -2$: $3 = -3B$, so $B = -1$."),
    pick(r"$\displaystyle\int_3^5 \frac{2}{x^2 - 1}\,dx = $", r"$\ln\frac43$", [r"$\ln\frac34$", r"$2\ln\frac43$", r"$\ln 12$"], "D",
         r"$\frac{2}{(x - 1)(x + 1)} = \frac{1}{x - 1} - \frac{1}{x + 1}$. $\left[\ln|x - 1| - \ln|x + 1|\right]_3^5 = (\ln 4 - \ln 6) - (\ln 2 - \ln 4) = \ln\frac{16}{12}$."),
)
IMPROPER = Variants(
    pick(r"$\displaystyle\int_1^\infty \frac{1}{x^3}\,dx = $", r"$\frac12$", [r"$-\frac12$", r"$\frac13$", r"divergent"], "C",
         r"$\displaystyle\lim_{b\to\infty}\left[-\frac{1}{2x^2}\right]_1^b = \lim_{b\to\infty}\left(-\frac{1}{2b^2} - \left(-\frac12\right)\right) = \frac12$."),
    pick(r"Which of these improper integrals converges?", r"$\int_1^\infty \frac{1}{x^2}\,dx$", [r"$\int_1^\infty \frac{1}{\sqrt x}\,dx$", r"$\int_1^\infty \frac1x\,dx$", r"$\int_0^1 \frac{1}{x^2}\,dx$"], "B",
         r"$\displaystyle\lim_{b\to\infty}\left[-\frac1x\right]_1^b = 1$. The others grow without bound: $2\sqrt b - 2$, $\ln b$, and $\frac1a - 1$ as $a \to 0^+$."),
)
CHOOSE = Variants(
    pick(r"$\displaystyle\int x^2\ln x\,dx = $", r"$\frac{x^3}{3}\ln x - \frac{x^3}{9} + C$", [r"$\frac{x^3}{3}\ln x + C$", r"$\frac{x^3}{3}\ln x - \frac{x^3}{3} + C$", r"$2x\ln x + x + C$"], "B",
         r"Parts with $u = \ln x$, $dv = x^2\,dx$: $\frac{x^3}{3}\ln x - \int \frac{x^3}{3}\cdot\frac1x\,dx = \frac{x^3}{3}\ln x - \frac{x^3}{9} + C$."),
    pick(r"$\displaystyle\int \ln x\,dx = $", r"$x\ln x - x + C$", [r"$\frac1x + C$", r"$x\ln x + C$", r"$\frac{(\ln x)^2}{2} + C$"], "C",
         r"Parts with $u = \ln x$, $dv = 1\,dx$: $x\ln x - \int x\cdot\frac1x\,dx = x\ln x - x + C$.", {r"$\frac1x + C$": "that's the derivative"}),
)

# the AB test's slots 2, 5, 8 and 12 (a second sums-over/under question, a basic definite integral, a basic-rules
# antiderivative and a net-change value) make room; everything else is the AB test
A = list(ab.A)
for k, slot in ((1, PARTS), (4, PARTIAL), (7, CHOOSE), (11, IMPROPER)):
    A[k] = slot

# ---------------------------------------------------------------- FRQ 3 (BC): parts, partial fractions, improper integrals
fA = x * sp.exp(-x)
same("F3A", [sp.solve(sp.diff(fA, x), x)[0], I(fA, 0, 2), sp.integrate(fA, (x, 0, sp.oo))], [1, 1 - 3 * sp.exp(-2), 1])
F3A = FRQ("An unbounded region", (
    r"Let $f$ be the function given by $f(x) = xe^{-x}$ for $x \ge 0$. Let $R$ be the unbounded region in the first quadrant bounded by the graph of $f$ and the $x$-axis."), [
    Part("a", r"Find the $x$-coordinate of the absolute maximum of $f$ for $x \ge 0$. Justify your answer.", num(1),
         r"$f'(x) = e^{-x} - xe^{-x} = (1 - x)e^{-x}$, which is $0$ only at $x = 1$ and changes from positive to negative there. "
         r"$f$ increases on $[0, 1]$ and decreases for $x > 1$, so the absolute maximum is at $x = 1$.", [(1, "$f'(x)$"), (1, "answer with justification")], work="2.4cm"),
    Part("b", r"Find $\displaystyle\int_0^2 f(x)\,dx$.", num(1 - 3 * sp.exp(-2), tol=1e-3, display=r"1 - 3e^{-2}"),
         r"Parts, $u = x$, $dv = e^{-x}\,dx$: $du = dx$, $v = -e^{-x}$. $\int xe^{-x}\,dx = -xe^{-x} - e^{-x}$, so "
         r"$\left[-xe^{-x} - e^{-x}\right]_0^2 = \left(-2e^{-2} - e^{-2}\right) - (0 - 1) = 1 - 3e^{-2}$.", [(1, "integration by parts"), (1, "answer")], work="2.8cm"),
    Part("c", r"Find the area of $R$, or show that the area of $R$ is infinite.", num(1),
         r"$\displaystyle\int_0^\infty xe^{-x}\,dx = \lim_{b\to\infty}\left[-xe^{-x} - e^{-x}\right]_0^b = \lim_{b\to\infty}\left(-\frac{b}{e^b} - \frac{1}{e^b}\right) - (-1) = 0 + 1 = 1$, "
         r"since $\frac{b}{e^b} \to 0$ (L'Hospital's Rule). The area is $1$.", [(1, "improper integral as a limit"), (1, "answer")], work="2.6cm"),
], frq_type="Improper integral (BC)")
fB = 2 / (x**2 + 2 * x)
same("F3B", [I(fB, 1, 3), sp.integrate(fB, (x, 1, sp.oo)), fB.subs(x, 2), sp.diff(fB, x).subs(x, 2)], [sp.log(sp.Rational(9, 5)), sp.log(3), sp.Rational(1, 4), -sp.Rational(3, 16)])
F3B = FRQ("An unbounded region", (
    r"Let $f$ be the function given by $f(x) = \dfrac{2}{x^2 + 2x}$ for $x \ge 1$. Let $R$ be the unbounded region bounded by the graph of $f$, the $x$-axis, and the vertical line $x = 1$."), [
    Part("a", r"Find $\displaystyle\int_1^3 f(x)\,dx$.", num(sp.log(sp.Rational(9, 5)), tol=1e-3, display=r"\ln\tfrac95"),
         r"$\frac{2}{x(x + 2)} = \frac Ax + \frac{B}{x + 2}$, so $2 = A(x + 2) + Bx$. Let $x = 0$: $A = 1$. Let $x = -2$: $B = -1$. "
         r"$\left[\ln|x| - \ln|x + 2|\right]_1^3 = (\ln 3 - \ln 5) - (0 - \ln 3) = \ln\frac95$.", [(1, "partial fractions"), (1, "answer")], work="2.8cm"),
    Part("b", r"Find the area of $R$, or show that the area of $R$ is infinite.", num(sp.log(3), tol=1e-3, display=r"\ln 3"),
         r"$\displaystyle\int_1^\infty f(x)\,dx = \lim_{b\to\infty}\left[\ln\frac{x}{x + 2}\right]_1^b = \ln 1 - \ln\frac13 = \ln 3$, since $\frac{b}{b + 2} \to 1$.",
         [(1, "improper integral as a limit"), (1, "answer")], work="2.6cm"),
    Part("c", r"Let $g(x) = \displaystyle\int_1^x f(t)\,dt$. Find $g'(2)$. Is the graph of $g$ concave up or concave down at $x = 2$? Give a reason for your answer.",
         selfcheck(r"g'(2) = \tfrac14;\ \text{concave down}"),
         r"$g'(x) = f(x)$, so $g'(2) = \frac{2}{8} = \frac14$. $g''(x) = f'(x) = -\dfrac{2(2x + 2)}{\left(x^2 + 2x\right)^2}$, so $g''(2) = -\frac{12}{64} < 0$: concave down.",
         [(1, "$g'(2)$"), (1, "concave down with reason")], work="2.4cm"),
], frq_type="Improper integral (BC)")

TEST = UnitTest(unit=6, version="BC", title="Integration and Accumulation of Change", mcq_a=A, mcq_b=ab.B,
                frq=[Variants(ab.F1A, ab.F1B), Variants(ab.F2A, ab.F2B), Variants(F3A, F3B)])
