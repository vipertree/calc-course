"""Topic 5.10: Introduction to optimization problems.

CED: FUN-4.B (FUN-4.B.1): the derivative finds the max or min of a quantity on an interval. 5.10 is setting up: name the
quantity, write it as a function of ONE variable using a constraint, find the domain. 5.11 is the full solve.
Worked examples: two numbers with sum 20 and largest product; a riverside pen with 200 ft of fence; x + 9/x.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Text, Topic, Variants, Video, expr, num,
                     same, selfcheck)

x = sp.symbols("x", positive=True)


def best(f, lo, hi, kind="max"):
    """(x*, f(x*)) for the absolute max/min of f on [lo, hi] by the candidates test."""
    cs = [c for c in sp.solveset(sp.diff(f, x), x, sp.Interval.open(lo, hi))] + [lo, hi]
    cs = [c for c in cs if f.subs(x, c).is_finite]
    pick = max if kind == "max" else min
    c = pick(cs, key=lambda c: float(f.subs(x, c)))
    return c, sp.simplify(f.subs(x, c))


same("ex1", list(best(x * (20 - x), 0, 20)), [10, 100])
same("ex2", list(best(x * (200 - 2 * x), 0, 100)), [50, 5000])
same("ex3", list(best(x + 9 / x, sp.Rational(1, 100), 100, "min")), [3, 6])

NOTES = [
    Video("s5_10.py::Lesson", "Introduction to optimization", 4),

    Section("What optimization is"),
    Text(r"Optimization means finding the \blank{largest} or \blank{smallest} value of a quantity: the most area, the least material, the lowest cost. "
         r"It's the Candidates Test (Topic 5.5) applied to a function you build yourself."),
    Formula("Setting up an optimization problem", (
        r"\textbf{1.} Name the quantity to optimize, and draw a picture. \par "
        r"\textbf{2.} Write that quantity as a function of the variables. \par "
        r"\textbf{3.} Use a \blank{constraint} (a fixed amount of fence, a fixed volume, a fixed sum) to rewrite it as a function of \blank{one} variable. \par "
        r"\textbf{4.} Find the \blank{domain}: the values of that variable that make sense.")),
    VideoExample('Setting up', work="2.6cm"),

    Section("Then solve"),
    Text(r"With $A(w)$ in hand, it's Unit 5 as usual: $A'(w) = 20 - 2w = 0$ at $w = 10$, and $A'' = -2 < 0$, so the area is largest for the $10 \times 10$ square: $100$."),
    Text(r"\textbf{Check the answer makes sense.} An optimal width of $-3$ or $50$ in this problem would mean an error in the setup or the domain."),
    BigIdea(r"Optimization: one quantity, written as a function of one variable (use the constraint), on a sensible domain, then find its absolute max or min."),
    Check(r"Two positive numbers have product $36$. Write their sum as a function of one of them, $x$.", expr(x + 36 / x, var="x"), r"The other is $\frac{36}{x}$, so $S(x) = x + \frac{36}{x}$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Two numbers add to $30$. Write their product $P$ as a function of one of them, $x$.", expr(x * (30 - x), var="x"), r"The other is $30 - x$: $P(x) = x(30 - x)$.", work="1.4cm"),
    Item(r"Two numbers add to $30$. What is the largest possible product?", num(225), r"$P'(x) = 30 - 2x = 0$ at $x = 15$; $P(15) = 225$.", work="1.8cm"),
    Item(r"A rectangle has perimeter $60$ cm. Write its area as a function of its width $x$.", expr(x * (30 - x), var="x"),
         r"$\ell = 30 - x$, so $A(x) = x(30 - x)$, for $0 < x < 30$.", work="1.6cm"),
    Item(r"A rectangle has area $64$ m$^2$. Write its perimeter as a function of its width $x$.", expr(2 * x + 128 / x, var="x"),
         r"$\ell = \frac{64}{x}$, so $P(x) = 2x + \frac{128}{x}$, for $x > 0$.", work="1.6cm"),
    Item(r"A rectangle has area $64$ m$^2$. What is the smallest possible perimeter?", num(32), r"$P'(w) = 2 - \frac{128}{w^2} = 0$ at $w = 8$: a square, $P = 32$.", work="2cm"),
    Item(r"Taini fences a rectangular garden against a barn wall, so only three sides need fence. She has $120$ ft of fence. Write the area as a function of $x$, the side perpendicular to the wall.",
         expr(x * (120 - 2 * x), var="x"), r"The side parallel to the wall is $120 - 2x$: $A(x) = x(120 - 2x)$, for $0 < x < 60$.", work="2cm"),
    Item(r"For Taini's garden, what is the largest possible area?", num(1800), r"$A'(x) = 120 - 4x = 0$ at $x = 30$; $A(30) = 30 \cdot 60 = 1800$ ft$^2$.", work="1.8cm"),
    Item(r"What positive number $x$ makes $x + \dfrac{4}{x}$ as small as possible?", num(2), r"$1 - \frac{4}{x^2} = 0$ at $x = 2$; $f'' = \frac{8}{x^3} > 0$.", work="1.8cm"),
    Item(r"A box with a square base and no top has volume $32$ ft$^3$. Write its surface area as a function of the base edge $x$.", expr(x**2 + 128 / x, var="x"),
         r"Height $h = \frac{32}{x^2}$. Area $= x^2 + 4xh = x^2 + \frac{128}{x}$.", work="2.2cm"),
    Item(r"For that box, what base edge gives the least surface area?", num(4), r"$2x - \frac{128}{x^2} = 0$: $x^3 = 64$, $x = 4$.", work="1.8cm"),
    Item(r"A farmer has $200$ m of fence for a rectangular pen divided into two equal halves by one more fence parallel to a side. What is the largest total area?", num(sp.Rational(5000, 3)),
         r"With $x$ the length of the three parallel fences: $3x + 2y = 200$, $A = xy = x\left(100 - \frac32x\right)$. $A' = 100 - 3x = 0$ at $x = \frac{100}{3}$, $A = \frac{5000}{3} \approx 1667$ m$^2$.", work="2.8cm"),
]
same("p", [best(x * (30 - x), 0, 30)[1], best(2 * x + 128 / x, sp.Rational(1, 100), 100, "min")[1], best(x * (120 - 2 * x), 0, 60)[1],
           best(x + 4 / x, sp.Rational(1, 100), 100, "min")[0], best(x**2 + 128 / x, sp.Rational(1, 100), 100, "min")[0], best(x * (100 - sp.Rational(3, 2) * x), 0, sp.Rational(200, 3))[1]],
     [225, 32, 1800, 2, 4, sp.Rational(5000, 3)])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Two numbers add to $16$. What is the largest possible product?", num(64), r"$x(16 - x)$ is largest at $x = 8$: $64$.", work="1.6cm"),
        Item(r"Two numbers add to $24$. What is the largest possible product?", num(144), r"$x(24 - x)$ is largest at $x = 12$: $144$.", work="1.6cm"),
        Item(r"Two numbers add to $50$. What is the largest possible product?", num(625), r"$x(50 - x)$ is largest at $x = 25$: $625$.", work="1.6cm"),
    ),
    Variants(
        MCQ(r"A rectangle has perimeter $100$. Its area as a function of its width $w$ is", [r"$w(100 - w)$", r"$w(50 - w)$", r"$100w$", r"$w^2 + 50$"], "B", r"$\ell = 50 - w$."),
        MCQ(r"A rectangle has area $50$. Its perimeter as a function of its width $w$ is", [r"$2w + \frac{100}{w}$", r"$2w + \frac{50}{w}$", r"$w + \frac{50}{w}$", r"$50w$"], "A", r"$\ell = \frac{50}{w}$, so $2w + 2\ell$."),
        MCQ(r"A rectangle against a wall uses $80$ ft of fence on three sides. Its area as a function of the side $x$ perpendicular to the wall is", [r"$x(80 - x)$",
            r"$x(40 - x)$", r"$x(80 - 2x)$", r"$2x(80 - x)$"], "C", r"The side along the wall is $80 - 2x$."),
    ),
    Variants(
        Item(r"Find the positive number $x$ that minimizes $x + \dfrac{25}{x}$.", num(5), r"$1 - \frac{25}{x^2} = 0$ at $x = 5$.", work="1.6cm"),
        Item(r"Find the positive number $x$ that minimizes $x + \dfrac{49}{x}$.", num(7), r"$1 - \frac{49}{x^2} = 0$ at $x = 7$.", work="1.6cm"),
        Item(r"Find the positive number $x$ that minimizes $4x + \dfrac{1}{x}$.", num(sp.Rational(1, 2)), r"$4 - \frac{1}{x^2} = 0$ at $x = \frac12$.", work="1.6cm"),
    ),
    Variants(
        MCQ(r"In an optimization problem, the constraint is used to", [r"find the derivative", r"rewrite the quantity in terms of one variable", r"check the second derivative", r"find the units"], "B",
            r"With one variable, it's a Unit 5 max/min problem."),
        MCQ(r"A pen's width $x$ must satisfy $0 < x < 25$. Calculus gives a critical point at $x = 40$. What does that mean?", [r"The best width is $40$", r"Use $x = 25$",
            r"The critical point is outside the domain, so check the endpoints and other critical points", r"The pen can't be built"], "C", r"Only candidates in the domain count."),
        MCQ(r"Why must a domain be found in an optimization problem?", [r"To decide which candidates are possible", r"To find the derivative", r"Because the AP exam requires units", r"It isn't needed"], "A",
            r"The candidates test works on the domain."),
    ),
    Variants(
        Item(r"A rectangle with perimeter $36$ has the largest possible area. What is that area?", num(81), r"A $9 \times 9$ square: $81$.", work="1.6cm"),
        Item(r"A rectangle with perimeter $48$ has the largest possible area. What is that area?", num(144), r"A $12 \times 12$ square: $144$.", work="1.6cm"),
        Item(r"A rectangle with perimeter $20$ has the largest possible area. What is that area?", num(25), r"A $5 \times 5$ square: $25$.", work="1.6cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"The sum of two positive numbers is $12$. What is the largest possible value of the product of one number and the square of the other?", [r"$256$", r"$216$", r"$288$", r"$144$"], "A",
        r"$P = x^2(12 - x)$, $P' = 24x - 3x^2 = 0$ at $x = 8$: $64 \cdot 4 = 256$."),
    MCQ(r"A rectangle is inscribed under $y = 12 - x^2$ with its base on the $x$-axis, symmetric about the $y$-axis. The largest possible area is", [r"$24$", r"$16$", r"$32$", r"$48$"], "C",
        r"$A = 2x(12 - x^2)$, $A' = 24 - 6x^2 = 0$ at $x = 2$: $A = 4 \cdot 8 = 32$."),
    MCQ(r"Which point on the line $y = 2x$ is closest to $(5, 0)$?", [r"$(2, 4)$", r"$(1, 2)$", r"$\left(\frac52, 5\right)$", r"$(0, 0)$"], "B",
        r"$D^2 = (x - 5)^2 + 4x^2$; derivative $2(x - 5) + 8x = 0$ at $x = 1$."),
    MCQ(r"The cost of a trip at speed $v$ mph is $C(v) = \dfrac{6000}{v} + 1.5v$. The cheapest speed is about", [r"$40$ mph", r"$55$ mph", r"$75$ mph", r"$63$ mph"], "D",
        r"$C' = -\frac{6000}{v^2} + 1.5 = 0$ at $v = \sqrt{4000} \approx 63.2$.", calc=True),
]
same("m", [best(x**2 * (12 - x), 0, 12)[1], best(2 * x * (12 - x**2), 0, 2 * sp.sqrt(3))[1], best((x - 5)**2 + 4 * x**2, 0, 5, "min")[0]], [256, 32, 1])

FRQS = [
    FRQ("Fencing a pen", (r"Rafael has $240$ ft of fence to build a rectangular pen along a straight river. No fence is needed along the river. "
                          r"Let $x$ be the length of each side perpendicular to the river."), [
        Part("a", r"Write the area $A$ of the pen as a function of $x$, and give its domain.", expr(x * (240 - 2 * x), var="x"),
             r"The side along the river is $240 - 2x$, so $A(x) = x(240 - 2x)$, with $0 < x < 120$.", [(1, "area function"), (1, "domain")], work="2cm"),
        Part("b", r"Find the value of $x$ that gives the largest area. Justify that it is a maximum.", num(60),
             r"$A'(x) = 240 - 4x = 0$ at $x = 60$. $A''(x) = -4 < 0$, and it is the only critical point, so it is the absolute maximum.", [(1, "$A' = 0$"), (1, "justification")], work="2.2cm"),
        Part("c", r"What is the largest area?", num(7200), r"$A(60) = 60 \cdot 120 = 7200$ ft$^2$.", [(1, "value with units")], work="1.2cm"),
    ], frq_type="Optimization"),
]
same("frq", list(best(x * (240 - 2 * x), 0, 120)), [60, 7200])

TOPIC = Topic(
    number="5.10", title="Introduction to Optimization Problems",
    unit="Unit 5: Analytical Applications of Differentiation", ced=["FUN-4.B", "FUN-4.B.1"],
    goals=r"Set up an optimization problem: name the quantity, use a constraint to write it in one variable, and find the domain.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
