"""Topic 4.4: Introduction to related rates.

CED: CHA-3.D (CHA-3.D.1): when quantities related by an equation change with time, differentiating the equation with
respect to t (implicitly, using the chain rule) relates their rates. 4.4 is the differentiation step; 4.5 is the full
procedure. Worked examples: ripple area, the circle x^2 + y^2 = 25 with respect to t, a melting ice cube.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Text, Topic, Variants, Video, expr, num,
                     same, selfcheck)

t = sp.symbols("t")
x, y, r, s, h, V, A = [sp.Function(n)(t) for n in "xyrshVA"]


def ddt(lhs, rhs, want, known):
    """Differentiate lhs = rhs in t, solve for the derivative `want`, substitute `known` (a dict of values, derivatives first)."""
    eq = sp.Eq(sp.diff(lhs, t), sp.diff(rhs, t))
    sol = sp.solve(eq, sp.diff(want, t))[0]
    return sp.simplify(sol.subs(known))


same("ripple", sp.diff(sp.pi * r**2, t).subs({sp.diff(r, t): 2, r: 10}), 40 * sp.pi)
same("circle", ddt(x**2 + y**2, 25, y, {sp.diff(x, t): 2, x: 3, y: 4}), sp.Rational(-3, 2))
same("cube", sp.diff(s**3, t).subs({sp.diff(s, t): sp.Rational(1, 10), s: 5}), sp.Rational(15, 2))

NOTES = [
    Video("s4_4.py::Lesson", "Rates that are related", 4),

    Section("Everything depends on time"),
    Text(r"When several quantities change together, each one is a function of time $t$. If an equation links the quantities, then "
         r"differentiating that equation with respect to \blank{$t$} links their \blank{rates}."),
    Formula("Differentiating with respect to $t$", (
        r"Every variable gets the chain rule: \[ \frac{d}{dt}\left[r^2\right] = 2r\,\frac{dr}{dt}, \qquad \frac{d}{dt}\left[x y\right] = \frac{dx}{dt}\,y + x\,\frac{dy}{dt}. \] "
        r"Constants differentiate to $0$. A quantity that is changing must stay a \emph{variable} until after you differentiate.")),
    VideoExample('A growing square', work="2.2cm"),
    Text(r"\textbf{The common mistake.} Substituting $s = 4$ \emph{before} differentiating turns $A = s^2$ into $A = 16$, whose derivative is $0$. "
         r"Differentiate first, \blank{then} substitute."),

    Section("Reading the rates"),
    Text(r"$\dfrac{dx}{dt} > 0$ means $x$ is increasing; $\dfrac{dx}{dt} < 0$ means $x$ is decreasing. Give each rate the units of its quantity "
         r"per unit of time."),
    BigIdea(r"An equation that relates quantities also relates their rates: differentiate both sides with respect to $t$, using the chain rule on every variable."),
    Check(r"$V = \frac43\pi r^3$. Write $\dfrac{dV}{dt}$ in terms of $r$ and $\dfrac{dr}{dt}$.", selfcheck(r"\frac{dV}{dt} = 4\pi r^2\,\frac{dr}{dt}"),
          r"\[ \frac{dV}{dt} = 4\pi r^2\,\frac{dr}{dt}. \]"),
]

# ---------------------------------------------------------------- practice
P = [
    (r"$A = \pi r^2$", r"\frac{dA}{dt} = 2\pi r\,\frac{dr}{dt}"),
    (r"$V = s^3$", r"\frac{dV}{dt} = 3s^2\,\frac{ds}{dt}"),
    (r"$x^2 + y^2 = 100$", r"2x\,\frac{dx}{dt} + 2y\,\frac{dy}{dt} = 0"),
    (r"$xy = 12$", r"\frac{dx}{dt}\,y + x\,\frac{dy}{dt} = 0"),
    (r"$V = \pi r^2 h$ (both $r$ and $h$ change)", r"\frac{dV}{dt} = 2\pi r h\,\frac{dr}{dt} + \pi r^2\,\frac{dh}{dt}"),
    (r"$z^2 = x^2 + y^2$", r"2z\,\frac{dz}{dt} = 2x\,\frac{dx}{dt} + 2y\,\frac{dy}{dt}"),
]
PRACTICE = [Item(rf"Differentiate with respect to $t$: {eq}.", selfcheck(ans), rf"\[ {ans} \]", work="1.6cm") for eq, ans in P]
PRACTICE += [
    Item(r"The radius of a circle grows at $3$ cm/s. How fast is the area growing when $r = 5$ cm?", num(30 * sp.pi),
         r"\[ \frac{dA}{dt} = 2\pi r\,\frac{dr}{dt} = 2\pi(5)(3) = 30\pi \text{ cm}^2\text{/s}. \]", work="2cm"),
    Item(r"A cube's edge grows at $0.5$ cm/min. How fast is its volume growing when the edge is $4$ cm?", num(24),
         r"\[ \frac{dV}{dt} = 3s^2\,\frac{ds}{dt} = 3(16)(0.5) = 24 \text{ cm}^3\text{/min}. \]", work="2cm"),
    Item(r"A spherical balloon's radius grows at $0.2$ in/s. How fast is its volume growing when $r = 5$ in?", num(20 * sp.pi),
         r"\[ \frac{dV}{dt} = 4\pi r^2\,\frac{dr}{dt} = 4\pi(25)(0.2) = 20\pi \text{ in}^3\text{/s}. \]", work="2cm"),
    Item(r"$x^2 + y^2 = 100$. When $x = 6$ and $y = 8$, $\dfrac{dx}{dt} = 4$. Find $\dfrac{dy}{dt}$.", num(-3),
         r"$2(6)(4) + 2(8)\dfrac{dy}{dt} = 0$, so $\dfrac{dy}{dt} = -3$.", work="2cm"),
    Item(r"$xy = 12$. When $x = 3$, $\dfrac{dx}{dt} = 2$. Find $\dfrac{dy}{dt}$.", num(sp.Rational(-8, 3)),
         r"$y = 4$. $2(4) + 3\dfrac{dy}{dt} = 0$, so $\dfrac{dy}{dt} = -\frac83$.", work="2cm"),
    Item(r"$y = x^3$, and $x$ increases at $2$ units per second. How fast is $y$ changing when $x = 2$?", num(24),
         r"\[ \frac{dy}{dt} = 3x^2\,\frac{dx}{dt} = 3(4)(2) = 24. \]", work="1.6cm"),
    Item(r"A square's area shrinks at $8$ cm$^2$/s. How fast is the side shrinking when the side is $2$ cm?", num(-2),
         r"$\dfrac{dA}{dt} = 2s\dfrac{ds}{dt}$: $-8 = 2(2)\dfrac{ds}{dt}$, so $\dfrac{ds}{dt} = -2$ cm/s.", work="2cm"),
    Item(r"The volume of a cube grows at $12$ cm$^3$/s. How fast is the edge growing when the edge is $2$ cm?", num(1),
         r"$12 = 3(4)\dfrac{ds}{dt}$, so $\dfrac{ds}{dt} = 1$ cm/s.", work="2cm"),
    Item(r"Explain why you may not substitute $r = 5$ into $A = \pi r^2$ before differentiating with respect to $t$.",
         selfcheck(r"r \text{ is changing}"), r"$r$ is changing. Substituting first makes $A = 25\pi$, a constant, and its derivative would be $0$.", work="1.4cm"),
    Item(r"$z^2 = x^2 + y^2$ with $x = 3$, $y = 4$, $\dfrac{dx}{dt} = 1$, $\dfrac{dy}{dt} = 2$. Find $\dfrac{dz}{dt}$.", num(sp.Rational(11, 5)),
         r"$z = 5$. $2(5)\dfrac{dz}{dt} = 2(3)(1) + 2(4)(2) = 22$, so $\dfrac{dz}{dt} = 2.2$.", work="2cm"),
    Item(r"A rectangle's length grows at $2$ m/s and its width shrinks at $1$ m/s. How fast is the area changing when the length is $10$ m and the width is $4$ m?",
         num(-2), r"$\dfrac{dA}{dt} = \dfrac{dl}{dt}w + l\dfrac{dw}{dt} = 2(4) + 10(-1) = -2$ m$^2$/s.", work="2cm"),
    Item(r"Kwame watches a circular ink spot grow. Its area grows at $6\pi$ cm$^2$/s. How fast is its radius growing when $r = 3$ cm?", num(1),
         r"$6\pi = 2\pi(3)\dfrac{dr}{dt}$, so $\dfrac{dr}{dt} = 1$ cm/s.", work="2cm"),
]
same("p", [sp.diff(sp.pi * r**2, t).subs({sp.diff(r, t): 3, r: 5}), sp.diff(s**3, t).subs({sp.diff(s, t): sp.Rational(1, 2), s: 4}),
           sp.diff(sp.Rational(4, 3) * sp.pi * r**3, t).subs({sp.diff(r, t): sp.Rational(1, 5), r: 5}),
           ddt(x**2 + y**2, 100, y, {sp.diff(x, t): 4, x: 6, y: 8}), ddt(x * y, 12, y, {sp.diff(x, t): 2, x: 3, y: 4}),
           ddt(s**2, A, s, {sp.diff(A, t): -8, s: 2}), ddt(s**3, V, s, {sp.diff(V, t): 12, s: 2}),
           ddt(h**2, x**2 + y**2, h, {sp.diff(x, t): 1, sp.diff(y, t): 2, x: 3, y: 4, h: 5}),
           (sp.diff(x * y, t)).subs({sp.diff(x, t): 2, sp.diff(y, t): -1, x: 10, y: 4}), ddt(sp.pi * r**2, A, r, {sp.diff(A, t): 6 * sp.pi, r: 3})],
     [30 * sp.pi, 24, 20 * sp.pi, -3, sp.Rational(-8, 3), -2, 1, sp.Rational(11, 5), -2, 1])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"Differentiating $A = \pi r^2$ with respect to $t$ gives", [r"$\dfrac{dA}{dt} = 2\pi r$", r"$\dfrac{dA}{dt} = 2\pi r\,\dfrac{dr}{dt}$",
            r"$\dfrac{dA}{dt} = \pi r^2\,\dfrac{dr}{dt}$", r"$\dfrac{dA}{dt} = 2\pi\,\dfrac{dr}{dt}$"], "B", r"Chain rule on $r^2$.", why_not={"A": "forgot $\\frac{dr}{dt}$"}),
        MCQ(r"Differentiating $V = s^3$ with respect to $t$ gives", [r"$\dfrac{dV}{dt} = 3s^2$", r"$\dfrac{dV}{dt} = s^3\,\dfrac{ds}{dt}$",
            r"$\dfrac{dV}{dt} = 3s^2\,\dfrac{ds}{dt}$", r"$\dfrac{dV}{dt} = 3s\,\dfrac{ds}{dt}$"], "C", r"Chain rule on $s^3$.", why_not={"A": "forgot $\\frac{ds}{dt}$"}),
        MCQ(r"Differentiating $x^2 + y^2 = 9$ with respect to $t$ gives", [r"$2x + 2y = 0$", r"$2x\,\dfrac{dx}{dt} + 2y\,\dfrac{dy}{dt} = 9$",
            r"$\dfrac{dy}{dt} = -\dfrac xy$", r"$2x\,\dfrac{dx}{dt} + 2y\,\dfrac{dy}{dt} = 0$"], "D", r"Chain rule on each square; the constant gives $0$."),
    ),
    Variants(
        Item(r"The radius of a circle grows at $2$ m/s. How fast is the area growing when $r = 6$ m?", num(24 * sp.pi), r"$2\pi(6)(2) = 24\pi$ m$^2$/s.", work="1.6cm"),
        Item(r"The radius of a circle grows at $4$ m/s. How fast is the area growing when $r = 3$ m?", num(24 * sp.pi), r"$2\pi(3)(4) = 24\pi$ m$^2$/s.", work="1.6cm"),
        Item(r"The radius of a circle grows at $0.5$ m/s. How fast is the area growing when $r = 10$ m?", num(10 * sp.pi), r"$2\pi(10)(0.5) = 10\pi$ m$^2$/s.", work="1.6cm"),
    ),
    Variants(
        Item(r"A cube's edge grows at $2$ cm/s. How fast is its volume growing when the edge is $3$ cm?", num(54), r"$3(9)(2) = 54$ cm$^3$/s.", work="1.6cm"),
        Item(r"A cube's edge grows at $0.1$ cm/s. How fast is its volume growing when the edge is $10$ cm?", num(30), r"$3(100)(0.1) = 30$ cm$^3$/s.", work="1.6cm"),
        Item(r"A cube's edge shrinks at $1$ cm/s. How fast is its volume changing when the edge is $2$ cm?", num(-12), r"$3(4)(-1) = -12$ cm$^3$/s.", work="1.6cm"),
    ),
    Variants(
        Item(r"$x^2 + y^2 = 25$, $x = 4$, $y = 3$, $\dfrac{dx}{dt} = 3$. Find $\dfrac{dy}{dt}$.", num(-4), r"$2(4)(3) + 2(3)\dfrac{dy}{dt} = 0$, so $\dfrac{dy}{dt} = -4$.", work="1.8cm"),
        Item(r"$x^2 + y^2 = 169$, $x = 5$, $y = 12$, $\dfrac{dx}{dt} = 6$. Find $\dfrac{dy}{dt}$.", num(sp.Rational(-5, 2)), r"$2(5)(6) + 2(12)\dfrac{dy}{dt} = 0$, so $\dfrac{dy}{dt} = -2.5$.", work="1.8cm"),
        Item(r"$xy = 20$, $x = 4$, $\dfrac{dx}{dt} = 1$. Find $\dfrac{dy}{dt}$.", num(sp.Rational(-5, 4)), r"$y = 5$. $5 + 4\dfrac{dy}{dt} = 0$, so $\dfrac{dy}{dt} = -\frac54$.", work="1.8cm"),
    ),
    Variants(
        MCQ(r"Which step comes first in a related rates problem?", [r"Substitute the given values", r"Differentiate with respect to $t$",
            r"Write an equation relating the quantities", r"Solve for the unknown rate"], "C", r"First relate the quantities, then differentiate, then substitute."),
        MCQ(r"A student substitutes $r = 5$ into $A = \pi r^2$ and then differentiates. The result is", [r"correct", r"$\dfrac{dA}{dt} = 0$, which is wrong",
            r"$10\pi\,\dfrac{dr}{dt}$", r"$25\pi$"], "B", r"$A = 25\pi$ is a constant, so its derivative is $0$. Differentiate first."),
        MCQ(r"If $\dfrac{dx}{dt} < 0$, then", [r"$x$ is negative", r"$x$ is decreasing", r"$x$ is increasing", r"$x$ is constant"], "B", r"A negative rate means decreasing."),
    ),
]
same("q", [ddt(x**2 + y**2, 25, y, {sp.diff(x, t): 3, x: 4, y: 3}), ddt(x**2 + y**2, 169, y, {sp.diff(x, t): 6, x: 5, y: 12}),
           ddt(x * y, 20, y, {sp.diff(x, t): 1, x: 4, y: 5})], [-4, sp.Rational(-5, 2), sp.Rational(-5, 4)])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"The area of a circle increases at $10\pi$ cm$^2$/s. When $r = 5$ cm, the radius increases at", [r"$2$ cm/s", r"$1$ cm/s", r"$\frac12$ cm/s", r"$10$ cm/s"], "B",
        r"$10\pi = 2\pi(5)\dfrac{dr}{dt}$, so $\dfrac{dr}{dt} = 1$."),
    MCQ(r"If $y = 2x^2 - 3x$ and $\dfrac{dx}{dt} = 4$, then $\dfrac{dy}{dt}$ when $x = 1$ is", [r"$1$", r"$-1$", r"$8$", r"$4$"], "D",
        r"$\dfrac{dy}{dt} = (4x - 3)\dfrac{dx}{dt} = (1)(4) = 4$.", why_not={"A": "forgot $\\frac{dx}{dt}$"}),
    MCQ(r"The volume of a sphere decreases at $16\pi$ cm$^3$/min. When $r = 2$ cm, the radius is changing at", [r"$-4$ cm/min", r"$-\frac12$ cm/min", r"$-1$ cm/min", r"$-2$ cm/min"], "C",
        r"$-16\pi = 4\pi(4)\dfrac{dr}{dt}$, so $\dfrac{dr}{dt} = -1$."),
    MCQ(r"$x$ and $y$ satisfy $x^2y = 12$. When $x = 2$, $\dfrac{dx}{dt} = 3$. Then $\dfrac{dy}{dt} =$", [r"$-9$", r"$9$", r"$-3$", r"$-\frac92$"], "A",
        r"$y = 3$. $2xy\dfrac{dx}{dt} + x^2\dfrac{dy}{dt} = 0$: $2(2)(3)(3) + 4\dfrac{dy}{dt} = 0$, so $\dfrac{dy}{dt} = -9$."),
]
same("m", [ddt(sp.pi * r**2, A, r, {sp.diff(A, t): 10 * sp.pi, r: 5}), sp.diff(2 * x**2 - 3 * x, t).subs({sp.diff(x, t): 4, x: 1}),
           ddt(sp.Rational(4, 3) * sp.pi * r**3, V, r, {sp.diff(V, t): -16 * sp.pi, r: 2}), ddt(x**2 * y, 12, y, {sp.diff(x, t): 3, x: 2, y: 3})],
     [1, 4, -1, -9])

FRQS = [
    FRQ("A growing cylinder", (
        r"A cylinder's radius $r$ and height $h$ both change with time. Its volume is $V = \pi r^2 h$. At a certain instant, $r = 3$ cm, $h = 10$ cm, "
        r"$\dfrac{dr}{dt} = 0.5$ cm/s and $\dfrac{dh}{dt} = -1$ cm/s."), [
        Part("a", r"Find $\dfrac{dV}{dt}$ in terms of $r$, $h$, $\dfrac{dr}{dt}$ and $\dfrac{dh}{dt}$.", selfcheck(r"2\pi r h\,r' + \pi r^2 h'"),
             r"Product rule and chain rule: \[ \frac{dV}{dt} = 2\pi r h\,\frac{dr}{dt} + \pi r^2\,\frac{dh}{dt}. \]", [(1, "product rule"), (1, "chain rule factors")], work="2cm"),
        Part("b", r"Find $\dfrac{dV}{dt}$ at that instant. Is the volume increasing or decreasing?", num(21 * sp.pi),
             r"\[ \frac{dV}{dt} = 2\pi(3)(10)(0.5) + \pi(9)(-1) = 30\pi - 9\pi = 21\pi \text{ cm}^3\text{/s}, \] which is positive, so the volume is increasing.",
             [(1, "value with units"), (1, "increasing, with reason")], work="2cm"),
        Part("c", r"At that instant, what rate of change of $h$ would keep the volume constant?", num(sp.Rational(-10, 3)),
             r"Set $\dfrac{dV}{dt} = 0$: $30\pi + 9\pi\dfrac{dh}{dt} = 0$, so $\dfrac{dh}{dt} = -\dfrac{10}{3}$ cm/s.", [(1, "sets $\\frac{dV}{dt} = 0$"), (1, "answer")], work="2cm"),
    ], frq_type="Related rates"),
]
same("frq", [sp.diff(sp.pi * r**2 * h, t).subs({sp.diff(r, t): sp.Rational(1, 2), sp.diff(h, t): -1, r: 3, h: 10}),
             ddt(sp.pi * r**2 * h, 0, h, {sp.diff(r, t): sp.Rational(1, 2), r: 3, h: 10})], [21 * sp.pi, sp.Rational(-10, 3)])

TOPIC = Topic(
    number="4.4", title="Introduction to Related Rates",
    unit="Unit 4: Contextual Applications of Differentiation", ced=["CHA-3.D", "CHA-3.D.1"],
    goals=r"Differentiate an equation that relates changing quantities with respect to time, and use it to find one rate from another.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
