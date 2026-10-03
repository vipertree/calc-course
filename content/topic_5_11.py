"""Topic 5.11: Solving optimization problems.

CED: FUN-4.C (FUN-4.C.1): full optimization in context, with a justification that the answer is the absolute extremum
(Candidates Test on a closed interval, or the only-critical-point argument on an open one) and units.
Worked examples: open box from a 12 x 12 sheet, the point on y = sqrt(x) closest to (3, 0), a can of volume 16 pi with
least surface area.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, expr, num,
                     same, selfcheck, check)

x, r = sp.symbols("x r", positive=True)


def best(f, v, lo, hi, kind="max"):
    cs = [c for c in sp.solveset(sp.diff(f, v), v, sp.Interval.open(lo, hi))] + [lo, hi]
    cs = [c for c in cs if f.subs(v, c).is_finite]
    c = (max if kind == "max" else min)(cs, key=lambda c: float(f.subs(v, c)))
    return c, sp.simplify(f.subs(v, c))


same("box", list(best(x * (12 - 2 * x)**2, x, 0, 6)), [2, 128])
same("closest", list(best((x - 3)**2 + x, x, 0, 10, "min")), [sp.Rational(5, 2), sp.Rational(11, 4)])
same("can", list(best(2 * sp.pi * r**2 + 32 * sp.pi / r, r, sp.Rational(1, 100), 100, "min")), [2, 24 * sp.pi])

NOTES = [
    Video("s5_11.py::Lesson", "Solving optimization problems", 5),

    Section("The whole procedure"),
    Formula("Solving an optimization problem", (
        r"\textbf{1.} Draw and label. Name the quantity to optimize. \par "
        r"\textbf{2.} Write it in terms of one variable, using the constraint. Give the \blank{domain}. \par "
        r"\textbf{3.} Find the critical points in the domain. \par "
        r"\textbf{4.} \blank{Justify} that you have the absolute max or min: \par "
        r"\quad closed interval: compare the candidates (critical points and endpoints); \par "
        r"\quad open interval: one critical point that is a relative extremum (first or second derivative test). \par "
        r"\textbf{5.} Answer the question that was asked, with \blank{units}.")),
    Text(r"\textbf{Answer the question asked.} If the question asks for the dimensions, give both dimensions, not just $x$. If it asks for the largest area, give the area."),

    Section("Distance problems"),
    Text(r"To find the point on a curve closest to a given point, minimize the \emph{square} of the distance. It's smallest at the same place as the distance, "
         r"and it has no square root to differentiate."),
    VideoExample('Closest point', work="2.8cm"),
    BigIdea(r"Set up with one variable on a domain, find the critical points, justify that the answer is absolute, and answer the question asked with units."),
    Check(r"A rectangle has perimeter $12$. What is its largest possible area?", num(9), r"A $3 \times 3$ square: $9$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"An open box is made from a $10 \times 10$ inch sheet by cutting equal squares of side $x$ from the corners and folding up the sides. What $x$ gives the largest volume? (The volume of a box is length $\times$ width $\times$ height.)",
         num(sp.Rational(5, 3)), r"$V = x(10 - 2x)^2$, $0 < x < 5$. $V' = (10 - 2x)(10 - 6x) = 0$ at $x = \frac53$ (in the domain). Candidates: $V(0) = 0$, $V\left(\frac53\right) \approx 74.1$, $V(5) = 0$.", work="3cm"),
    Item(r"Find the point on $y = x^2$ closest to $(0, 2)$. Enter its positive $x$-coordinate.", num(sp.sqrt(sp.Rational(3, 2))),
         r"$D^2 = x^2 + (x^2 - 2)^2$. Derivative $2x + 4x(x^2 - 2) = 2x(2x^2 - 3) = 0$ at $x = 0, \pm\sqrt{3/2}$. $D^2(0) = 4$, $D^2\left(\sqrt{3/2}\right) = \frac74$: the minimum.", work="3cm"),
    Item(r"A can (closed cylinder) holds $54\pi$ cm$^3$. What radius gives the least surface area? (A cylinder of radius $r$ and height $h$ has volume $V = \pi r^2 h$ and surface area $S = 2\pi r^2 + 2\pi r h$.)", num(3),
         r"$h = \frac{54}{r^2}$. $S = 2\pi r^2 + 2\pi r h = 2\pi r^2 + \frac{108\pi}{r}$. $S' = 4\pi r - \frac{108\pi}{r^2} = 0$ at $r^3 = 27$, $r = 3$; $S'' > 0$.", work="3cm"),
    Item(r"A rectangle is inscribed in a semicircle of radius $2$, with its base on the diameter. What is its largest possible area?", num(4),
         r"With corner $(x, \sqrt{4 - x^2})$: $A = 2x\sqrt{4 - x^2}$. $A' = 0$ at $x = \sqrt2$: $A = 2\sqrt2\cdot\sqrt2 = 4$.", work="3cm"),
    Item(r"A poster has $50$ in$^2$ of print, with margins of $4$ in at top and bottom and $2$ in at each side. What width of the printed area minimizes the poster's total area?",
         num(5), r"Print $x$ by $\frac{50}{x}$. Total $(x + 4)\left(\frac{50}{x} + 8\right) = 82 + 8x + \frac{200}{x}$. Derivative $8 - \frac{200}{x^2} = 0$ at $x = 5$.", work="3cm"),
    Item(r"Kofi walks from a point $3$ km from a straight road to a town on the road $5$ km past the nearest point. He walks $3$ km/h off-road and $5$ km/h on the road. "
         r"How far from the nearest point should he reach the road to minimize his time?", num(sp.Rational(9, 4)),
         r"$T = \frac{\sqrt{9 + x^2}}{3} + \frac{5 - x}{5}$. $T' = \frac{x}{3\sqrt{9 + x^2}} - \frac15 = 0$: $5x = 3\sqrt{9 + x^2}$, $16x^2 = 81$, $x = \frac94$ km.", work="3.2cm"),
    Item(r"A box with a square base and open top must hold $108$ in$^3$. Find the dimensions that use the least material. Enter the base edge." + r" (The volume of a box is length $\times$ width $\times$ height.)", num(6),
         r"$S = x^2 + \frac{432}{x}$. $S' = 2x - \frac{432}{x^2} = 0$ at $x = 6$; height $3$. A $6 \times 6 \times 3$ box.", work="2.8cm"),
    Item(r"The sum of a positive number and twice another positive number is $40$. What is the largest possible product?", num(200),
         r"$x + 2y = 40$: $P = y(40 - 2y)$, $P' = 40 - 4y = 0$ at $y = 10$, $x = 20$: $P = 200$.", work="2.2cm"),
    Item(r"A wire $20$ cm long is bent into a rectangle. Which dimensions give the largest area? Enter the width.", num(5), r"Perimeter $20$: a $5 \times 5$ square.", work="1.8cm"),
    Item(r"In Kofi's walk, why is it enough to compare $T(0)$, $T\left(\frac94\right)$ and $T(5)$?", selfcheck(r"\text{Candidates Test on } [0, 5]"),
         r"$T$ is continuous on the closed interval $[0, 5]$, so its minimum is at a critical point or an endpoint.", work="1.4cm"),
]
same("p", [best(x * (10 - 2 * x)**2, x, 0, 5)[0], best(x**2 + (x**2 - 2)**2, x, 0, 3, "min")[0], best(2 * sp.pi * r**2 + 108 * sp.pi / r, r, sp.Rational(1, 100), 100, "min")[0],
           best(2 * x * sp.sqrt(4 - x**2), x, 0, 2)[1], best(82 + 8 * x + 200 / x, x, sp.Rational(1, 100), 100, "min")[0],
           best(sp.sqrt(9 + x**2) / 3 + (5 - x) / 5, x, 0, 5, "min")[0], best(x**2 + 432 / x, x, sp.Rational(1, 100), 100, "min")[0], best(x * (40 - 2 * x), x, 0, 20)[1]],
     [sp.Rational(5, 3), sp.sqrt(sp.Rational(3, 2)), 3, 4, 5, sp.Rational(9, 4), 6, 200])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(*[Item(rf"An open box is made from a ${n} \times {n}$ inch sheet by cutting squares of side $x$ from the corners. What is the largest possible volume? (The volume of a box is length $\times$ width $\times$ height.)",
                    num(best(x * (n - 2 * x)**2, x, 0, sp.Rational(n, 2))[1]),
                    rf"$V = x({n} - 2x)^2$; $V' = 0$ at $x = {sp.latex(sp.Rational(n, 6))}$: $V = {sp.latex(best(x * (n - 2 * x)**2, x, 0, sp.Rational(n, 2))[1])}$ in$^3$.", work="2.6cm")
               for n in (6, 18, 24)]),
    Variants(
        Item(r"A closed can holds $2\pi$ in$^3$. What radius gives the least surface area?", num(1), r"$S = 2\pi r^2 + \frac{4\pi}{r}$; $S' = 0$ at $r^3 = 1$.", work="2.4cm"),
        Item(r"A closed can holds $128\pi$ in$^3$. What radius gives the least surface area?", num(4), r"$S = 2\pi r^2 + \frac{256\pi}{r}$; $S' = 0$ at $r^3 = 64$.", work="2.4cm"),
        Item(r"A closed can holds $250\pi$ in$^3$. What radius gives the least surface area?", num(5), r"$S = 2\pi r^2 + \frac{500\pi}{r}$; $S' = 0$ at $r^3 = 125$.", work="2.4cm"),
    ),
    Variants(
        Item(r"Find the point on $y = \sqrt{x}$ closest to $(4, 0)$. Enter its $x$-coordinate.", num(sp.Rational(7, 2)), r"$D^2 = (x - 4)^2 + x$; derivative $2x - 7 = 0$.", work="2.2cm"),
        Item(r"Find the point on $y = \sqrt{x}$ closest to $(2, 0)$. Enter its $x$-coordinate.", num(sp.Rational(3, 2)), r"$D^2 = (x - 2)^2 + x$; derivative $2x - 3 = 0$.", work="2.2cm"),
        Item(r"Find the point on $y = \sqrt{x}$ closest to $(5, 0)$. Enter its $x$-coordinate.", num(sp.Rational(9, 2)), r"$D^2 = (x - 5)^2 + x$; derivative $2x - 9 = 0$.", work="2.2cm"),
    ),
    Variants(
        MCQ(r"To find the closest point on a curve to $(a, b)$, it's easiest to minimize", [r"the distance $D$", r"$D^2$", r"$\sqrt{D}$", r"$\frac{1}{D}$"], "B",
            r"$D^2$ has its minimum at the same place, with no square root."),
        MCQ(r"An optimization function on the open interval $(0, \infty)$ has one critical point, a relative minimum. Then that point is", [r"the absolute minimum",
            r"not necessarily the absolute minimum", r"an inflection point", r"the absolute maximum"], "A", r"A lone relative extremum on an interval is absolute."),
        MCQ(r"An optimization question asks for the dimensions of a box. After finding $x = 4$, you should", [r"answer $4$", r"answer the volume", r"give every dimension, with units",
            r"check that $x = 4$ is an integer"], "C", r"Answer the question asked."),
    ),
    Variants(
        Item(r"A rectangular field with area $600$ m$^2$ is fenced, with one extra fence down the middle parallel to one pair of sides. Find the least total length of fence.", num(120),
             r"With $x$ the length of the three parallel fences: $xy = 600$, $F = 3x + 2y = 3x + \frac{1200}{x}$. $F' = 3 - \frac{1200}{x^2} = 0$ at $x = 20$: $F = 60 + 60 = 120$ m.",
             work="2.8cm"),
        Item(r"A rectangle has area $100$. What is its least possible perimeter?", num(40), r"A $10 \times 10$ square.", work="1.8cm"),
        Item(r"A rectangle has area $49$. What is its least possible perimeter?", num(28), r"A $7 \times 7$ square.", work="1.8cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"A rectangle has one corner at the origin and the opposite corner on $y = 6 - 2x$ in the first quadrant. Its largest possible area is", [r"$\frac92$", r"$9$", r"$6$", r"$3$"], "A",
        r"$A = x(6 - 2x)$, $A' = 6 - 4x = 0$ at $x = \frac32$: $A = \frac32 \cdot 3 = \frac92$."),
    MCQ(r"A cylinder is inscribed in a sphere of radius $3$. The height $h$ that maximizes the cylinder's volume $V = \pi\left(9 - \frac{h^2}{4}\right)h$ is", [r"$3$", r"$\sqrt3$", r"$2\sqrt3$", r"$6$"], "C",
        r"$V' = \pi\left(9 - \frac{3h^2}{4}\right) = 0$ at $h^2 = 12$."),
    MCQ(r"A $36$-inch wire is cut into two pieces; one forms a square and the other a circle. To minimize the total area, the square's piece should be about", [r"$20.2$ in",
        r"$15.8$ in", r"$36$ in", r"$0$ in"], "A",
        r"$A = \left(\frac x4\right)^2 + \frac{(36 - x)^2}{4\pi}$; $A' = \frac x8 - \frac{36 - x}{2\pi} = 0$ at $x = \frac{144}{\pi + 4} \approx 20.2$.", calc=True),
    MCQ(r"The point on $y = e^x$ closest to the origin has $x$-coordinate about", [r"$0$", r"$-1$", r"$-0.567$", r"$-0.426$"], "D",
        r"Minimize $x^2 + e^{2x}$: $2x + 2e^{2x} = 0$, so $x \approx -0.426$.", calc=True),
]
close("m3", 144 / (sp.pi + 4), 20.2, 0.05)
close("m4", sp.nsolve(sp.Symbol("u") + sp.exp(2 * sp.Symbol("u")), sp.Symbol("u"), -0.4), -0.426, 5e-4)

FRQS = [
    FRQ("The cheapest box", (r"A closed box with a square base of side $x$ feet and height $h$ feet must hold $54$ cubic feet (its volume is $x^2 h$). Material for the "
                             r"top and bottom costs $2$ dollars per square foot, and material for the sides costs $1$ dollar per square foot."), [
        Part("a", r"Show that the cost, in dollars, of the material for the box is $C(x) = 4x^2 + \dfrac{216}{x}$ for $x > 0$.",
             selfcheck(r"C(x) = 4x^2 + \frac{216}{x}"),
             r"The volume is $x^2h = 54$, so $h = \dfrac{54}{x^2}$. The top and bottom cost $2\cdot 2x^2 = 4x^2$ dollars. The four sides "
             r"have area $4xh = \dfrac{216}{x}$ square feet and cost $\dfrac{216}{x}$ dollars. So $C(x) = 4x^2 + \dfrac{216}{x}$.",
             [(1, "$h = \\frac{54}{x^2}$"), (1, "assembles $C(x)$")], work="2.6cm"),
        Part("b", r"Find the value of $x$ that minimizes the cost of the box. Justify your answer.", num(3),
             r"$C'(x) = 8x - \dfrac{216}{x^2} = 0$ when $x^3 = 27$, so $x = 3$. $C'(x) < 0$ for $0 < x < 3$ and $C'(x) > 0$ for $x > 3$, "
             r"so $C$ has its absolute minimum on $x > 0$ at $x = 3$.",
             [(1, "$C'(x)$"), (1, "critical point $x = 3$"), (1, "justification for an absolute minimum")], work="3cm"),
        Part("c", r"Find the minimum cost of the box.", num(108, display=r"108\ \text{dollars}"),
             r"$C(3) = 36 + 72 = 108$ dollars.", [(1, "answer $108$")], work="1.4cm"),
    ], frq_type="Function analysis"),
]
C11 = 4 * x**2 + 216 / x
same("frq", [sp.solve(sp.diff(C11, x), x), C11.subs(x, 3)], [[3], 108])
check("frq b", sp.diff(C11, x).subs(x, 2) < 0 and sp.diff(C11, x).subs(x, 4) > 0)

TOPIC = Topic(
    number="5.11", title="Solving Optimization Problems",
    unit="Unit 5: Analytical Applications of Differentiation", ced=["FUN-4.C", "FUN-4.C.1"],
    goals=r"Solve optimization problems in context, justify that the answer is an absolute extremum, and answer with units.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
same("frq", list(best(4 * x**2 + 216 / x, x, sp.Rational(1, 100), 100, "min")), [3, 108])
same("q5", [best(3 * x + 1200 / x, x, sp.Rational(1, 100), 100, "min")[1]], [120])
