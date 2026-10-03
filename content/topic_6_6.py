"""Topic 6.6: Applying properties of definite integrals.

CED: LIM-5.C (LIM-5.C.3-LIM-5.C.5): integrals over
an interval of zero width, reversed limits, constant multiples, sums and differences, adding adjacent intervals,
and integrals of piecewise and absolute-value functions by splitting and geometry. Worked examples: |x| on [-2, 4], a
piecewise function, finding a constant. AP asks this as multiple choice (or inside graph FRQs), so FRQS is empty.
"""
import sympy as sp

from calclib import (VideoExample, MCQ, BigIdea, Check, Formula, Item, Section, Text, Topic, Variants, Video, num, same)
from calclib.figs import graph

x = sp.symbols("x", real=True)

same("given", [3 * 6 - 2 * (-2), 10 - 4, -2 * 6, 6 + 3], [22, 6, -12, 9])
same("ex", [sp.integrate(sp.Abs(x), (x, -2, 4)), sp.integrate(2, (x, -1, 1)) + sp.integrate(x + 1, (x, 1, 3)), sp.Rational(16 - 7, 3)], [10, 10, 3])

# integrals of a function known only through these values (used across the problems below)
I_F_03, I_F_37, I_G_03 = 5, -2, 4
FIG_H = graph("t6_6_h", [("3+0*x", -2, 1), ("4-x", 1, 5)], xr=(-2, 5), yr=(-2, 4), ylabel="h(x)", caption="The graph of $h$: two line segments.")
H = sp.Piecewise((3, x < 1), (4 - x, True))
same("h", [sp.integrate(H, (x, -2, 1)), sp.integrate(H, (x, 1, 4)), sp.integrate(H, (x, 4, 5)), sp.integrate(H, (x, -2, 5))], [9, sp.Rational(9, 2), -sp.Rational(1, 2), 13])

NOTES = [
    Video("s6_6.py::Lesson", "Properties of integrals", 5),

    Section("The properties"),
    Formula("Properties of definite integrals", (
        r"\[ \int_a^a f(x)\,dx = \blank{0} \qquad \int_b^a f(x)\,dx = \blank{-}\int_a^b f(x)\,dx \] "
        r"\[ \int_a^b k\,f(x)\,dx = k\int_a^b f(x)\,dx \qquad \int_a^b \left[f(x) \pm g(x)\right] dx = \int_a^b f(x)\,dx \pm \int_a^b g(x)\,dx \] "
        r"\[ \int_a^b f(x)\,dx + \int_b^c f(x)\,dx = \int_a^c f(x)\,dx \]")),
    Text(r"With $\int_1^4 f(x)\,dx = 6$ and $\int_1^4 g(x)\,dx = -2$: $\int_1^4 \left[3f(x) - 2g(x)\right] dx = 3(6) - 2(-2) = 22$, and $\int_4^1 f(x)\,dx = -6$."),
    VideoExample('Splitting an interval', work="3cm"),

    Section("Piecewise functions and absolute values"),
    Text(r"Split the interval where the rule changes (or where $|\cdot|$ has its corner), then add the pieces. Geometry often gives each piece: "
         r"$\int_{-2}^{4} |x|\,dx = 2 + 8 = 10$. The integral of a constant is a rectangle: $\int_a^b k\,dx = \blank{k(b - a)}$."),
    BigIdea(r"Same interval: zero. Backward: flip the sign. Constants come out, sums split, neighboring intervals add."),
    Check(r"$\int_0^2 f(x)\,dx = 3$ and $\int_2^6 f(x)\,dx = 5$. Find $\int_0^6 f(x)\,dx$.", num(8), r"$3 + 5 = 8$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(rf"$\int_0^3 f(x)\,dx = {I_F_03}$ and $\int_3^7 f(x)\,dx = {I_F_37}$. Find $\int_0^7 f(x)\,dx$.", num(I_F_03 + I_F_37), rf"${I_F_03} + ({I_F_37}) = {I_F_03 + I_F_37}$.", work="1cm"),
    Item(rf"Using the same values, find $\int_7^3 f(x)\,dx$.", num(-I_F_37), rf"Backward limits: $-({I_F_37}) = {-I_F_37}$.", work="1cm"),
    Item(rf"Using the same values, find $\int_0^3 4f(x)\,dx$.", num(4 * I_F_03), rf"$4({I_F_03}) = {4 * I_F_03}$.", work="1cm"),
    Item(rf"$\int_0^3 f(x)\,dx = {I_F_03}$ and $\int_0^3 g(x)\,dx = {I_G_03}$. Find $\int_0^3 \left[2f(x) - g(x)\right] dx$.", num(2 * I_F_03 - I_G_03),
         rf"$2({I_F_03}) - {I_G_03} = {2 * I_F_03 - I_G_03}$.", work="1.2cm"),
    Item(rf"Using the same values, find $\int_0^3 \left[f(x) + 2\right] dx$.", num(I_F_03 + 6), rf"${I_F_03} + 2(3) = {I_F_03 + 6}$.", work="1.2cm"),
    Item(r"Evaluate $\displaystyle\int_{-3}^{1} |x|\,dx$.", num(sp.integrate(sp.Abs(x), (x, -3, 1))), r"Triangles: $\frac12(3)(3) + \frac12(1)(1) = 4.5 + 0.5 = 5$.", work="1.4cm"),
    Item(r"Evaluate $\displaystyle\int_0^4 |x - 2|\,dx$.", num(sp.integrate(sp.Abs(x - 2), (x, 0, 4))), r"Two triangles, each $\frac12(2)(2) = 2$: total $4$.", work="1.4cm"),
    Item(r"The graph of $h$ is shown. Evaluate $\displaystyle\int_{-2}^{5} h(x)\,dx$.", num(sp.integrate(H, (x, -2, 5))),
         r"Rectangle $(3)(3) = 9$; trapezoid on $[1, 4]$: $\frac{3 + 0}{2}(3) = 4.5$; triangle below the axis on $[4, 5]$: $-0.5$. Total $13$.", work="2cm", figure=FIG_H),
    Item(r"Using the same graph, evaluate $\displaystyle\int_5^{1} h(x)\,dx$.", num(-sp.integrate(H, (x, 1, 5))), r"$\int_1^5 h(x)\,dx = 4.5 - 0.5 = 4$, so backward it is $-4$.", work="1.4cm"),
    Item(r"$\int_1^6 f(x)\,dx = 12$ and $\int_1^6 \left[f(x) - k\right] dx = 2$. Find $k$.", num(2), r"$12 - 5k = 2$, so $k = 2$.", work="1.4cm"),
    Item(r"$f$ is odd and $\int_0^3 f(x)\,dx = 7$. Find $\int_{-3}^{3} f(x)\,dx$.", num(0), r"An odd function's areas on $[-3, 0]$ and $[0, 3]$ cancel: $-7 + 7 = 0$.", work="1.2cm"),
]
same("p", [sp.integrate(sp.Abs(x), (x, -3, 1)), sp.integrate(sp.Abs(x - 2), (x, 0, 4)), -sp.integrate(H, (x, 1, 5)), sp.Rational(12 - 2, 5)], [5, 4, -4, 2])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"$\int_1^5 f(x)\,dx = 8$ and $\int_5^9 f(x)\,dx = -3$. Find $\int_1^9 f(x)\,dx$.", num(5), r"$8 - 3 = 5$.", work="1cm"),
        Item(r"$\int_0^4 f(x)\,dx = 6$ and $\int_0^2 f(x)\,dx = 10$. Find $\int_2^4 f(x)\,dx$.", num(-4), r"$6 - 10 = -4$.", work="1cm"),
        Item(r"$\int_{-2}^{3} f(x)\,dx = 9$ and $\int_{-2}^{0} f(x)\,dx = 4$. Find $\int_0^3 f(x)\,dx$.", num(5), r"$9 - 4 = 5$.", work="1cm"),
    ),
    Variants(
        Item(r"$\int_2^6 f(x)\,dx = 3$. Find $\int_6^2 5f(x)\,dx$.", num(-15), r"$-5(3) = -15$.", work="1cm"),
        Item(r"$\int_0^1 f(x)\,dx = -4$. Find $\int_1^0 2f(x)\,dx$.", num(8), r"$-2(-4) = 8$.", work="1cm"),
        Item(r"$\int_3^8 f(x)\,dx = 6$. Find $\int_8^3 \frac{f(x)}{3}\,dx$.", num(-2), r"$-\frac{6}{3} = -2$.", work="1cm"),
    ),
    Variants(
        Item(r"$\int_0^5 f(x)\,dx = 4$ and $\int_0^5 g(x)\,dx = 7$. Find $\int_0^5 \left[3f(x) + g(x)\right] dx$.", num(19), r"$12 + 7 = 19$.", work="1cm"),
        Item(r"$\int_0^5 f(x)\,dx = 4$ and $\int_0^5 g(x)\,dx = 7$. Find $\int_0^5 \left[f(x) - 2g(x)\right] dx$.", num(-10), r"$4 - 14 = -10$.", work="1cm"),
        Item(r"$\int_0^5 f(x)\,dx = 4$. Find $\int_0^5 \left[f(x) + 3\right] dx$.", num(19), r"$4 + 3(5) = 19$.", work="1cm"),
    ),
    Variants(*[Item(rf"Evaluate $\displaystyle\int_{{{a}}}^{{{b}}} {sp.latex(e)}\,dx$.", num(sp.integrate(e, (x, a, b))), rf"Split at the corner and add the triangles: ${sp.integrate(e, (x, a, b))}$.", work="1.2cm")
               for e, a, b in ((sp.Abs(x), -1, 3), (sp.Abs(x - 1), -1, 2), (sp.Abs(2 * x), -2, 1))]),
    Variants(
        MCQ(r"Which is always true?", [r"$\int_a^b f(x)g(x)\,dx = \int_a^b f(x)\,dx \cdot \int_a^b g(x)\,dx$", r"$\int_a^b \left[f(x) + g(x)\right] dx = \int_a^b f(x)\,dx + \int_a^b g(x)\,dx$",
            r"$\int_a^b f(x)\,dx = \int_b^a f(x)\,dx$", r"$\int_a^b x f(x)\,dx = x\int_a^b f(x)\,dx$"], "B", r"Sums split. Products do not; reversing flips the sign; $x$ is not a constant."),
        MCQ(r"$\int_a^b f(x)\,dx = 0$ for every $f$ exactly when", [r"$a = 0$", r"$b = 0$", r"$a = b$", r"$a = -b$"], "C", r"An interval of zero width."),
        MCQ(r"Which is always true?", [r"$\int_a^b 3f(x)\,dx = 3\int_a^b f(x)\,dx$", r"$\int_a^b f(x)^2\,dx = \left(\int_a^b f(x)\,dx\right)^2$", r"$\int_b^a f(x)\,dx = \int_a^b f(x)\,dx$",
            r"$\int_a^c f(x)\,dx = \int_a^b f(x)\,dx - \int_b^c f(x)\,dx$"], "A", r"Constants come out."),
    ),
]
same("q", [sp.integrate(sp.Abs(x), (x, -1, 3)), sp.integrate(sp.Abs(x - 1), (x, -1, 2)), sp.integrate(sp.Abs(2 * x), (x, -2, 1))], [5, sp.Rational(5, 2), 5])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"If $\int_{-1}^{4} f(x)\,dx = 10$ and $\int_{2}^{4} f(x)\,dx = 3$, then $\int_{-1}^{2} \left[2f(x) + 1\right] dx = $", [r"$14$", r"$15$", r"$17$", r"$27$"], "C",
        r"$\int_{-1}^{2} f = 7$, so $2(7) + 1(3) = 17$.", why_not={"B": "added $1$ instead of the integral of $1$ over a width of $3$"}),
    MCQ(r"$\displaystyle\int_{-4}^{2} |x + 1|\,dx = $", [r"$6$", r"$9$", r"$\frac92$", r"$3$"], "B", r"Triangles $\frac12(3)(3) + \frac12(3)(3) = 9$."),
    MCQ(r"If $\int_0^3 f(x)\,dx = 2$, then $\int_3^0 \left[f(x) - 4\right] dx = $", [r"$-14$", r"$14$", r"$-10$", r"$10$"], "D",
        r"$\int_0^3 [f(x) - 4]\,dx = 2 - 12 = -10$; backward: $10$."),
    MCQ(r"$f(x) = x$ for $x < 2$ and $f(x) = 2$ for $x \ge 2$. $\int_0^5 f(x)\,dx = $", [r"$8$", r"$10$", r"$\frac{25}{2}$", r"$6$"], "A",
        r"Triangle $\frac12(2)(2) = 2$ plus rectangle $(3)(2) = 6$: $8$."),
]
same("m", [2 * (10 - 3) + 3, sp.integrate(sp.Abs(x + 1), (x, -4, 2)), -(2 - 12), sp.integrate(sp.Piecewise((x, x < 2), (2, True)), (x, 0, 5))], [17, 9, 10, 8])

FRQS = []

TOPIC = Topic(
    number="6.6", title="Applying Properties of Definite Integrals",
    unit="Unit 6: Integration and Accumulation of Change", ced=["LIM-5.C", "LIM-5.C.3", "LIM-5.C.4", "LIM-5.C.5"],
    goals=r"Use the properties of definite integrals, and split piecewise and absolute-value functions, to find definite integrals.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
