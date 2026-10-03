"""Topic 8.13 (BC): The arc length of a smooth, planar curve and distance traveled.

CED: CHA-6.A (CHA-6.A.1): for f with a continuous derivative on [a, b], L = integral of sqrt(1 + f'(x)^2) dx, from
ds^2 = dx^2 + dy^2; the x = g(y) version with dy. Checked against the distance formula on a line. Lesson example:
y = (2/3) x^(3/2) on [0, 3] (14/3). Worked examples: x^2/2 - (ln x)/4 on [1, 2] (3/2 + ln 2/4); x^2 on [0, 1] by
calculator (1.479); ln(cos x) on [0, pi/4] (ln(1 + sqrt 2)).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)

x, y = sp.symbols("x y", positive=True)


def arc(f, a, b, v=x):
    """Exact arc length when sympy finds it."""
    return sp.simplify(sp.integrate(sp.sqrt(sp.simplify(1 + sp.diff(f, v)**2)), (v, a, b)))


def arc_n(f, a, b, v=x):
    return float(sp.Integral(sp.sqrt(1 + sp.diff(f, v)**2), (v, a, b)).evalf())


same("lesson", [sp.diff(sp.Rational(2, 3) * x**sp.Rational(3, 2), x), sp.integrate(sp.sqrt(1 + x), (x, 0, 3))], [sp.sqrt(x), sp.Rational(14, 3)])
same("line", [arc(2 * x, 0, 3)], [3 * sp.sqrt(5)])
same("ex1", [sp.simplify(1 + sp.diff(x**2 / 2 - sp.log(x) / 4, x)**2 - (x + 1 / (4 * x))**2), sp.integrate(x + 1 / (4 * x), (x, 1, 2))], [0, sp.Rational(3, 2) + sp.log(2) / 4])
close("ex2", arc_n(x**2, 0, 1), 1.479, 5e-4)
close("ex3", arc_n(sp.log(sp.cos(x)), 0, sp.pi / 4), float(sp.log(1 + sp.sqrt(2))), 1e-9)

NOTES = [
    Video("s8_13.py::Lesson", "Arc length", 6),

    Section("Adding up tiny hypotenuses"),
    Text(r"A tiny piece of a smooth curve is almost straight: the hypotenuse of a right triangle with legs $dx$ and $dy$. So $ds^2 = dx^2 + dy^2$ and $ds = \sqrt{1 + \left(\frac{dy}{dx}\right)^2}\,dx$."),
    Formula("Arc length", (r"If $f'$ is continuous on $[a, b]$, the length of $y = f(x)$ from $x = a$ to $x = b$ is \[ L = \blank{\int_a^b \sqrt{1 + [f'(x)]^2}\,dx}. \] "
                           r"For $x = g(y)$, $c \le y \le d$: $L = \int_c^d \sqrt{1 + [g'(y)]^2}\,dy$.")),
    Text(r"\textbf{Check on a line.} $y = 2x$ on $[0, 3]$: $\int_0^3 \sqrt5\,dx = 3\sqrt5 = \sqrt{3^2 + 6^2}$, the distance formula."),
    VideoExample('A curve with an exact length', work="4cm"),
    Text(r"\textbf{Usually a calculator.} $\sqrt{1 + [f'(x)]^2}$ rarely has an elementary antiderivative. On the exam, set the integral up carefully and evaluate it numerically: $y = x^2$ on $[0, 1]$ has length $\int_0^1 \sqrt{1 + 4x^2}\,dx \approx 1.479$."),
    Text(r"\textbf{Distance traveled.} A particle moving along a path travels the path's arc length; on a line that is $\int |v(t)|\,dt$. Parametric motion (Unit 9) uses $\int \sqrt{(x')^2 + (y')^2}\,dt$."),
    BigIdea(r"$L = \int \sqrt{1 + [f']^2}\,dx$: Pythagoras on tiny pieces. Set it up, then usually use a calculator."),
    Check(r"Write the integral for the length of $y = \sin x$ from $0$ to $\pi$.", selfcheck(r"\int_0^\pi \sqrt{1 + \cos^2 x}\,dx"), r"$f' = \cos x$."),
]

# ---------------------------------------------------------------- practice
_p5 = arc_n(sp.exp(x), 0, 1)
_p6 = arc_n(sp.sin(x), 0, sp.pi)
PRACTICE = [
    Item(r"Find the length of $y = 3x + 1$ from $x = 0$ to $x = 4$.", num(4 * sp.sqrt(10), tol=1e-3), r"$\int_0^4 \sqrt{10}\,dx = 4\sqrt{10} \approx 12.649$.", work="1.4cm"),
    Item(r"Find the length of $y = x^{3/2}$ from $x = 0$ to $x = 4$.", num(arc(x**sp.Rational(3, 2), 0, 4), tol=1e-3),
         r"$f' = \frac32\sqrt x$: $\int_0^4 \sqrt{1 + \frac94x}\,dx = \frac{8}{27}\left(10^{3/2} - 1\right) \approx 9.073$.", work="2.2cm"),
    Item(r"Find the length of $y = \frac{x^3}{6} + \frac{1}{2x}$ from $x = 1$ to $x = 2$.", num(arc(x**3 / 6 + 1 / (2 * x), 1, 2)),
         r"$1 + [f']^2 = \left(\frac{x^2}{2} + \frac{1}{2x^2}\right)^2$: $\int_1^2 \left(\frac{x^2}{2} + \frac{1}{2x^2}\right) dx = \frac{17}{12}$.", work="2.4cm"),
    Item(r"Write, but do not evaluate, the integral for the length of $y = \ln x$ from $x = 1$ to $x = e$.", selfcheck(r"\int_1^e \sqrt{1 + \frac{1}{x^2}}\,dx"), r"$f' = \frac1x$.", work="1.2cm"),
    Item(r"Use a calculator to find the length of $y = e^x$ from $x = 0$ to $x = 1$.", num(sp.Float(round(_p5, 4)), tol=2e-3), rf"$\int_0^1 \sqrt{{1 + e^{{2x}}}}\,dx \approx {_p5:.3f}$.", work="1.4cm", calc=True),
    Item(r"Use a calculator to find the length of one arch of $y = \sin x$, $0 \le x \le \pi$.", num(sp.Float(round(_p6, 4)), tol=2e-3), rf"$\int_0^\pi \sqrt{{1 + \cos^2 x}}\,dx \approx {_p6:.3f}$.", work="1.4cm", calc=True),
    Item(r"Find the length of $x = \frac23(y - 1)^{3/2}$ from $y = 1$ to $y = 4$.", num(sp.integrate(sp.sqrt(y), (y, 1, 4))), r"$g' = \sqrt{y - 1}$, $1 + (g')^2 = y$: $\int_1^4 \sqrt y\,dy = \frac{14}{3}$.", work="2cm"),
    Item(r"Find the length of $y = \frac{e^x + e^{-x}}{2}$ from $x = 0$ to $x = \ln 2$.", num(sp.Rational(3, 4)), r"$1 + [f']^2 = \left(\frac{e^x + e^{-x}}{2}\right)^2$: $\int_0^{\ln 2} \frac{e^x + e^{-x}}{2}\,dx = \frac{2 - \frac12}{2} = \frac34$.", work="2.2cm"),
]
same("p", [arc(x**3 / 6 + 1 / (2 * x), 1, 2), sp.simplify(arc(x**sp.Rational(3, 2), 0, 4) - sp.Rational(8, 27) * (10**sp.Rational(3, 2) - 1))], [sp.Rational(17, 12), 0])
close("p8", arc_n((sp.exp(x) + sp.exp(-x)) / 2, 0, sp.log(2)), 0.75, 1e-9)

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"The length of $y = x^3$ from $x = 0$ to $x = 2$ is", [r"$\int_0^2 \sqrt{1 + x^6}\,dx$", r"$\int_0^2 \sqrt{1 + 3x^2}\,dx$", r"$\int_0^2 \sqrt{1 + 9x^4}\,dx$", r"$\int_0^2 \left(1 + 9x^4\right) dx$"], "C", r"$[f']^2 = 9x^4$."),
        MCQ(r"The length of $y = \cos x$ from $x = 0$ to $x = \pi$ is", [r"$\int_0^\pi \sqrt{1 + \sin^2 x}\,dx$", r"$\int_0^\pi \sqrt{1 + \cos^2 x}\,dx$", r"$\int_0^\pi \sqrt{1 - \sin^2 x}\,dx$", r"$\int_0^\pi (1 + \sin x)\,dx$"], "A", r"$f' = -\sin x$, squared."),
    ),
    Variants(
        Item(r"Find the length of $y = \frac43x - 2$ from $x = 0$ to $x = 3$.", num(5), r"$\int_0^3 \frac53\,dx = 5$ (a $3$-$4$-$5$ triangle).", work="1.2cm"),
        Item(r"Find the length of $y = \frac{5}{12}x$ from $x = 0$ to $x = 12$.", num(13), r"$\int_0^{12} \frac{13}{12}\,dx = 13$.", work="1.2cm"),
    ),
    Variants(
        Item(r"Find the length of $y = \frac23x^{3/2}$ from $x = 0$ to $x = 8$.", num(sp.integrate(sp.sqrt(1 + x), (x, 0, 8))), r"$\int_0^8 \sqrt{1 + x}\,dx = \frac23(27 - 1) = \frac{52}{3}$.", work="1.6cm"),
        Item(r"Find the length of $y = \frac23x^{3/2}$ from $x = 0$ to $x = 15$.", num(sp.integrate(sp.sqrt(1 + x), (x, 0, 15))), r"$\frac23(64 - 1) = 42$.", work="1.6cm"),
    ),
    Variants(
        Item(r"Use a calculator to find the length of $y = \sqrt x$ from $x = 1$ to $x = 4$.", num(sp.Float(round(arc_n(sp.sqrt(x), 1, 4), 4)), tol=2e-3), rf"$\int_1^4 \sqrt{{1 + \frac{{1}}{{4x}}}}\,dx \approx {arc_n(sp.sqrt(x), 1, 4):.3f}$.", work="1.4cm", calc=True),
        Item(r"Use a calculator to find the length of $y = \frac1x$ from $x = 1$ to $x = 3$.", num(sp.Float(round(arc_n(1 / x, 1, 3), 4)), tol=2e-3), rf"$\int_1^3 \sqrt{{1 + \frac{{1}}{{x^4}}}}\,dx \approx {arc_n(1 / x, 1, 3):.3f}$.", work="1.4cm", calc=True),
    ),
    Variants(
        MCQ(r"Arc length comes from which fact about a tiny piece of a smooth curve?", [r"$ds = dx + dy$", r"$ds^2 = dx^2 + dy^2$", r"$ds = dx \cdot dy$", r"$ds = \frac{dy}{dx}$"], "B", r"Pythagoras."),
    ),
]

# ---------------------------------------------------------------- test prep
_m4 = arc_n(x**2 / 4, 0, 2)
MCQS = [
    MCQ(r"Which gives the length of $y = \ln(\sec x)$ from $x = 0$ to $x = \frac\pi4$?", [r"$\int_0^{\pi/4} \sec x\,dx$", r"$\int_0^{\pi/4} \tan x\,dx$", r"$\int_0^{\pi/4} \sec^2 x\,dx$", r"$\int_0^{\pi/4} \sqrt{1 + \sec^2 x}\,dx$"], "A",
        r"$f' = \tan x$; $\sqrt{1 + \tan^2 x} = \sec x$.", why_not={"D": "used $f$ instead of $f'$ inside"}),
    MCQ(r"The length of $y = \frac{x^4}{8} + \frac{1}{4x^2}$ from $x = 1$ to $x = 2$ is", [r"$\frac{15}{8}$", r"$\frac{33}{16}$", r"$\frac{17}{8}$", r"$\frac{3}{2}$"], "B",
        r"$1 + [f']^2 = \left(\frac{x^3}{2} + \frac{1}{2x^3}\right)^2$: $\int_1^2 \left(\frac{x^3}{2} + \frac{1}{2x^3}\right) dx = \frac{15}{8} + \frac{3}{16} = \frac{33}{16}$."),
    MCQ(r"A curve $y = f(x)$ has $f'(x) = \sqrt{x^2 - 1}$ for $x \ge 1$. Its length from $x = 1$ to $x = 3$ is", [r"$2$", r"$\sqrt8$", r"$4$", r"$\frac92$"], "C", r"$\sqrt{1 + x^2 - 1} = x$: $\int_1^3 x\,dx = 4$."),
    MCQ(r"To three decimal places, the length of $y = \frac{x^2}{4}$ from $x = 0$ to $x = 2$ is", [r"$2.000$", r"$2.236$", rf"${_m4:.3f}$", r"$1.148$"], "C", rf"$\int_0^2 \sqrt{{1 + \frac{{x^2}}{{4}}}}\,dx \approx {_m4:.3f}$.", why_not={"B": "the straight-line distance"}, calc=True),
]
same("m", [arc(x**4 / 8 + 1 / (4 * x**2), 1, 2), sp.integrate(x, (x, 1, 3))], [sp.Rational(33, 16), 4])
close("m4", _m4, 2.296, 5e-3)

FRQS = []

TOPIC = Topic(
    number="8.13", title="The Arc Length of a Smooth, Planar Curve and Distance Traveled",
    unit="Unit 8: Applications of Integration", ced=["CHA-6.A", "CHA-6.A.1"],
    goals=r"Set up and evaluate the arc length of a smooth curve, exactly or with a calculator.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
