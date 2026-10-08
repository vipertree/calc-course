"""Topic 8.6: Finding the area between curves that intersect at more than two points.

CED: CHA-5.B (CHA-5.B.1): when the curves cross inside the interval, split at the crossings and integrate top minus
bottom on each piece; area = integral of |f - g|. A sign chart for f - g decides which curve is on top on each piece;
integrating f - g across the crossings lets the pieces cancel. Lesson example: y = x^3 - x^2 and y = 2x, area 37/12.
Worked examples: sin and cos on [0, pi] (2 sqrt 2); x^3 - 3x and x (8); x^4 - 2x^2 and the axis (touching, not crossing).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)
from calclib.figs import region

x = sp.symbols("x", real=True)


def total_area(f, g, a, b):
    """Area between f and g on [a, b], split at every real crossing inside."""
    cuts = sorted({a, b} | {r for r in sp.solve(sp.Eq(f, g), x) if r.is_real and a < r < b})
    return sp.nsimplify(sp.simplify(sum(abs(sp.integrate(f - g, (x, p, q))) for p, q in zip(cuts, cuts[1:]))))


same("lesson", [total_area(x**3 - x**2, 2 * x, -1, 2), sp.integrate(x**3 - x**2 - 2 * x, (x, -1, 2))], [sp.Rational(37, 12), -sp.Rational(9, 4)])
same("ex", [total_area(sp.sin(x), sp.cos(x), 0, sp.pi), total_area(x**3 - 3 * x, x, -2, 2), sp.simplify(sp.integrate(2 * x**2 - x**4, (x, -sp.sqrt(2), sp.sqrt(2))))],
     [2 * sp.sqrt(2), 8, 16 * sp.sqrt(2) / 15])

fR = x**3 - 6 * x**2 + 8 * x
FIG_RS = region("t8_6_rs", [("x^3-6*x^2+8*x", -0.2, 4.2)], (-0.5, 4.5), (-4, 4), [(lambda v: v**3 - 6 * v**2 + 8 * v, lambda v: 0, 0, 2), (lambda v: 0, lambda v: v**3 - 6 * v**2 + 8 * v, 2, 4)],
                labels=[(1, 1, "center", "$R$"), (3, -1, "center", "$S$")], caption=r"The graph of $f(x) = x^3 - 6x^2 + 8x$ with regions $R$ and $S$.")

NOTES = [
    Video("s8_6.py::Lesson", "Curves that cross more than twice", 6),

    Section("Split at the crossings"),
    Text(r"When the curves cross inside the interval, top and bottom trade places. Where $f - g > 0$, $f$ is on top; where $f - g < 0$, $g$ is."),
    Formula("Area with crossings", (r"\[ A = \int_a^b \blank{|f(x) - g(x)|}\,dx. \] Without a calculator: make a sign chart for $f - g$, split at its zeros, integrate top minus bottom on each piece, and add.")),
    Text(r"\textbf{Why one integral fails.} For $y = x^3 - x^2$ and $y = 2x$, $\int_{-1}^2 \big((x^3 - x^2) - 2x\big)\,dx = \frac{5}{12} - \frac83 = -\frac94$: the pieces cancel. The area is $\frac{5}{12} + \frac83 = \frac{37}{12}$."),
    VideoExample('Three crossings', work="5cm"),
    Text(r"\textbf{Touching is not crossing.} A zero of $f - g$ where the sign doesn't change (like $x^2$ at $0$) doesn't swap top and bottom. The sign chart shows it."),
    Text(r"\textbf{Calculator.} On calculator questions, $\int_a^b |f(x) - g(x)|\,dx$ can be entered directly; you still need the outer crossing points as limits."),
    BigIdea(r"Area is $\int |f - g|\,dx$: split where $f - g$ changes sign and add the pieces. Areas never cancel."),
    Check(r"Find the area between $y = x^3$ and $y = x$.", selfcheck(r"\tfrac12"), r"Crossings $-1, 0, 1$; each piece is $\frac14$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Find the area between $y = x^3$ and $y = 4x$.", num(total_area(x**3, 4 * x, -2, 2)), r"Crossings $-2, 0, 2$; each piece $\int_0^2 (4x - x^3)\,dx = 4$. Total $8$.", work="2cm"),
    Item(r"Find the area between $y = x^3 - x$ and the $x$-axis.", num(total_area(x**3 - x, 0, -1, 1)), r"Each piece is $\frac14$; total $\frac12$.", work="1.8cm"),
    Item(r"Find the area between $y = \sin x$ and the $x$-axis for $0 \le x \le 2\pi$.", num(4), r"$2 + 2$.", work="1.4cm"),
    Item(r"Find $\int_0^{2\pi} \sin x\,dx$ and explain why it isn't the area in the previous problem.", selfcheck(r"0;\ \text{the two arches cancel}"), r"$0$: the arch below the axis counts as negative.", work="1.4cm"),
    Item(r"Find the area between $y = x^2 - 2x$ and the $x$-axis for $0 \le x \le 3$.", num(total_area(x**2 - 2 * x, 0, 0, 3)), r"Split at $2$: $\frac43 + \frac43 = \frac83$.", work="1.8cm"),
    Item(r"Find the area between $y = x^3 - 2x^2$ and $y = 3x$.", num(total_area(x**3 - 2 * x**2, 3 * x, -1, 3)),
         r"$x(x - 3)(x + 1) = 0$: crossings $-1, 0, 3$. Pieces $\frac{7}{12}$ and $\frac{45}{4}$; total $\frac{71}{6}$.", work="2.4cm"),
    Item(r"Find the area of regions $R$ and $S$ together (shown).", num(total_area(fR, 0, 0, 4)), r"$\int_0^2 f = 4$ and $\int_2^4 f = -4$: area $8$.", work="1.8cm", figure=FIG_RS),
    Item(r"Find the area between $y = \cos x$ and $y = 0$ for $0 \le x \le \pi$.", num(2), r"Split at $\frac\pi2$: $1 + 1$.", work="1.4cm"),
    Item(r"Find the area between $y = x^2(x - 3)$ and the $x$-axis for $0 \le x \le 4$.", num(total_area(x**2 * (x - 3), 0, 0, 4)),
         r"Touches at $0$, crosses at $3$: $\int_0^3 = -\frac{27}{4}$ and $\int_3^4 = \frac{27}{4}$, so the area is $\frac{27}{2}$.", work="2.2cm"),
    Item(r"Find the area between $y = e^x - 2$ and the $x$-axis for $0 \le x \le 2$.", num(total_area(sp.exp(x) - 2, 0, 0, 2), tol=1e-3), r"Split at $\ln 2$: $(2\ln 2 - 1) + (e^2 - 6 + 2\ln 2) = e^2 - 7 + 4\ln 2 \approx 3.162$.", work="2.2cm"),
]
same("p", [sp.integrate(x**2 * (x - 3), (x, 0, 3)), sp.integrate(x**2 * (x - 3), (x, 3, 4)), total_area(x**3 - 2 * x**2, 3 * x, -1, 3)], [-sp.Rational(27, 4), sp.Rational(27, 4), sp.Rational(71, 6)])
same("p e", [total_area(sp.exp(x) - 2, 0, 0, 2)], [sp.E**2 - 7 + 4 * sp.log(2)])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find the area between $y = x^3$ and $y = 9x$.", num(total_area(x**3, 9 * x, -3, 3)), r"Each piece $\int_0^3 (9x - x^3)\,dx = \frac{81}{4}$; total $\frac{81}{2}$.", work="1.8cm"),
        Item(r"Find the area between $y = x^3$ and $y = x$.", num(total_area(x**3, x, -1, 1)), r"$\frac14 + \frac14$.", work="1.8cm"),
        Item(r"Find the area between $y = x^3 - 4x$ and the $x$-axis.", num(total_area(x**3 - 4 * x, 0, -2, 2)), r"$4 + 4$.", work="1.8cm"),
    ),
    Variants(
        Item(r"Find the area between $y = x - 1$ and the $x$-axis for $0 \le x \le 3$.", num(total_area(x - 1, 0, 0, 3)), r"$\frac12 + 2 = \frac52$.", work="1.4cm"),
        Item(r"Find the area between $y = 2 - x$ and the $x$-axis for $0 \le x \le 4$.", num(total_area(2 - x, 0, 0, 4)), r"$2 + 2 = 4$.", work="1.4cm"),
        Item(r"Find the area between $y = x^2 - 1$ and the $x$-axis for $0 \le x \le 2$.", num(total_area(x**2 - 1, 0, 0, 2)), r"$\frac23 + \frac43 = 2$.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"Which gives the area between $y = x^3$ and $y = x$ on $[-1, 1]$?", [r"$\int_{-1}^{1} (x - x^3)\,dx$", r"$2\int_{0}^{1} (x - x^3)\,dx$", r"$\int_{-1}^{1} (x^3 - x)\,dx$", r"$\int_{0}^{1} (x - x^3)\,dx$"], "B",
            r"The pieces are mirror images; integrating straight across gives $0$.", why_not={"A": "the pieces cancel to $0$"}),
        MCQ(r"Which gives the area between $y = \sin x$ and the $x$-axis on $[0, 2\pi]$?", [r"$\int_0^{2\pi} \sin x\,dx$", r"$\int_0^{\pi} \sin x\,dx$", r"$\int_0^{2\pi} |\sin x|\,dx$", r"$\left|\int_0^{2\pi} \sin x\,dx\right|$"], "C",
            r"Integrate the absolute value.", why_not={"A": "the arches cancel to $0$"}),
    ),
    Variants(
        Item(r"Find the area between $y = \sin x$ and $y = \cos x$ for $0 \le x \le \frac\pi2$.", num(total_area(sp.sin(x), sp.cos(x), 0, sp.pi / 2), tol=1e-3), r"Split at $\frac\pi4$: $2(\sqrt2 - 1) \approx 0.828$.", work="2cm"),
        Item(r"Find the area between $y = \cos x$ and the $x$-axis for $0 \le x \le \frac{3\pi}{2}$.", num(3), r"Split at $\frac\pi2$: $1 + 2$.", work="2cm"),
    ),
    Variants(
        Item(r"Find the area between $y = x^3 - x^2$ and $y = 0$ for $0 \le x \le 2$.", num(total_area(x**3 - x**2, 0, 0, 2)), r"Split at $1$: $\frac{1}{12} + \frac{17}{12} = \frac32$.", work="1.8cm"),
        Item(r"Find the area between $y = x(x - 1)(x - 2)$ and the $x$-axis.", num(total_area(x * (x - 1) * (x - 2), 0, 0, 2)), r"$\frac14 + \frac14 = \frac12$.", work="1.8cm"),
    ),
]

# ---------------------------------------------------------------- test prep
_g = lambda v: 2 * sp.sin(v)
_xs = [0.0, float(sp.nsolve(2 * sp.sin(x) - x, x, 1.9))]
_m4 = 2 * float(sp.Integral(2 * sp.sin(x) - x, (x, 0, _xs[1])).evalf())
MCQS = [
    MCQ(r"The total area of the regions between $y = x^3 - 9x$ and the $x$-axis is", [r"$0$", r"$\frac{81}{4}$", r"$81$", r"$\frac{81}{2}$"], "D", r"Each piece is $\frac{81}{4}$.", why_not={"A": "the pieces cancel"}),
    MCQ(r"$\int_0^5 f(x)\,dx = 3$, and $f$ is negative only on $(1, 2)$, where $\int_1^2 f(x)\,dx = -4$. The total area between $f$ and the $x$-axis on $[0, 5]$ is", [r"$11$", r"$3$", r"$7$", r"$-1$"], "A",
        r"The positive parts add to $3 + 4 = 7$; area $= 7 + 4 = 11$."),
    MCQ(r"How many separate regions do $y = x^3 - 3x^2 + 2x$ and the $x$-axis enclose?", [r"$1$", r"$2$", r"$3$", r"$4$"], "B", r"Crossings at $0, 1, 2$: two regions."),
    MCQ(r"The curves $y = 2\sin x$ and $y = x$ enclose two regions. To three decimal places, their total area is", [r"$0.000$", r"$0.858$", rf"${_m4:.3f}$", r"$3.790$"], "C",
        rf"They cross at $0$ and $x \approx \pm{_xs[1]:.4f}$; by symmetry the area is $2\int_0^{{{_xs[1]:.4f}}} (2\sin x - x)\,dx \approx {_m4:.3f}$.", calc=True),
]
same("m", [total_area(x**3 - 9 * x, 0, -3, 3)], [sp.Rational(81, 2)])
close("m4", _m4, 1.683, 5e-3)

# ---------------------------------------------------------------- FRQ
same("frq", [sp.integrate(fR, (x, 0, 2)), total_area(fR, 0, 0, 4), sp.integrate(fR, (x, 0, 4))], [4, 8, 0])
FRQS = [
    FRQ("Two regions", (r"Let $f(x) = x^3 - 6x^2 + 8x$. The graph of $f$ and the $x$-axis enclose region $R$, for $0 \le x \le 2$, and region $S$, for $2 \le x \le 4$, as shown."), [
        Part("a", r"Find the area of $R$.", num(4), r"$\int_0^2 \left(x^3 - 6x^2 + 8x\right) dx = \left[\tfrac{x^4}{4} - 2x^3 + 4x^2\right]_0^2 = 4 - 16 + 16 = 4$.", [(1, "integral"), (1, "answer")], work="2.4cm"),
        Part("b", r"Find the total area of $R$ and $S$.", num(8), r"$\int_2^4 f(x)\,dx = 0 - 4 = -4$, so $S$ has area $4$. Total: $8$.", [(1, "handles the sign of $S$"), (1, "answer")], work="2.2cm"),
        Part("c", r"Find $\displaystyle\int_0^4 f(x)\,dx$. Explain why it is not the total area of $R$ and $S$.", selfcheck(r"0;\ S \text{ is below the axis, so it counts as negative}"),
             r"$\int_0^4 f(x)\,dx = 4 + (-4) = 0$. $S$ lies below the $x$-axis, so its integral is negative and cancels $R$.", [(1, "value $0$"), (1, "explanation")], work="2cm"),
        Part("d", r"The vertical line $x = k$ divides $R$ into two regions of equal area. Write, but do not solve, an equation involving an integral that $k$ satisfies.", selfcheck(r"\int_0^k \left(x^3 - 6x^2 + 8x\right) dx = 2"),
             r"$\int_0^k \left(x^3 - 6x^2 + 8x\right) dx = 2$ (half of the area of $R$).", [(1, "integral equation")], work="1.6cm"),
    ], frq_type="Area and volume", figure=FIG_RS),
]

TOPIC = Topic(
    number="8.6", title="Finding the Area Between Curves That Intersect at More Than Two Points",
    unit="Unit 8: Applications of Integration", ced=["CHA-5.B", "CHA-5.B.1"],
    goals=r"Find the area between curves that cross inside the interval by splitting at the crossings.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
