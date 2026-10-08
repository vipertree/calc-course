"""Topic 4.4: Introduction to related rates.

CED: CHA-3.D (CHA-3.D.1): when quantities related by an equation change with time, differentiating the equation with
respect to t (implicitly, using the chain rule) relates their rates.

Adder (2026-10-03): 4.4 only sets problems up. Every example stops at the differentiated equation: list what you know,
what you want, what is fixed, write the equation, differentiate with respect to t. Topic 4.5 takes the SAME examples
(ripple, ladder, cone, two cars, shadow) and substitutes and solves. 3D volume formulas are always stated in the problem,
as on the AP exam; 2D formulas (circle, triangle, rectangle, Pythagorean theorem, similar triangles) are not.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Example, Figure, FigureRow, Formula, Item, Part, Section, Text, Topic,
                     Variants, Video, expr, num, same, selfcheck)

t = sp.symbols("t")
x, y, z, r, s, h, V, A, l, w = [sp.Function(n)(t) for n in ("x", "y", "z", "r", "s", "h", "V", "A", "l", "w")]
d = lambda f: sp.diff(f, t)

# ---------------------------------------------------------------- diagrams, shared with 4.5
FIG_RIPPLE = Figure(name="rr_ripple", caption=r"The ripple: radius $r$, area $A = \pi r^2$.", tikz=(
    r"\begin{tikzpicture}[scale=0.8]\fill[wash] (0,0) circle (1.3); \draw[line width=0.9pt] (0,0) circle (1.3);"
    r"\draw[line width=0.6pt, black!50] (0,0) circle (0.9); \fill (0,0) circle (1.5pt);"
    r"\draw[line width=0.9pt] (0,0) -- (1.3,0) node[midway, above] {$r$};\end{tikzpicture}"))
FIG_LADDER = Figure(name="rr_ladder", caption=r"The ladder: $x^2 + y^2 = 13^2$.", tikz=(
    r"\begin{tikzpicture}[scale=0.8]\fill[pattern=north east lines, pattern color=black!45] (-0.28,0) rectangle (0,3.2);"
    r"\draw[line width=0.9pt] (0,0) -- (0,3.2); \draw[line width=0.9pt] (-0.3,0) -- (3,0);"
    r"\draw[line width=2.4pt] (1.3,0) -- (0,2.8); \draw (0,0.25) -- (0.25,0.25) -- (0.25,0);"
    r"\node[below] at (0.65,0) {$x$}; \node[left] at (-0.28,1.4) {$y$}; \node[above right] at (0.62,1.45) {$13$};\end{tikzpicture}"))
FIG_CONE = Figure(name="rr_cone", caption=r"The cone: water depth $h$, surface radius $r$; $\frac rh = \frac39$.", tikz=(
    r"\begin{tikzpicture}[scale=0.8]\fill[wash] (0,0) -- (-1,2) -- (1,2) -- cycle; \draw (0,2) ellipse (1 and 0.17);"
    r"\draw[line width=0.9pt] (-1.5,3) -- (0,0) -- (1.5,3); \draw[line width=0.9pt] (0,3) ellipse (1.5 and 0.25);"
    r"\draw[dashed] (0,0) -- (0,2) node[midway, left] {$h$}; \draw (0,2) -- (1,2) node[midway, above] {$r$};"
    r"\draw[<->] (2,0) -- (2,3) node[midway, right] {$9$}; \node[above] at (0.75,3.25) {$3$};\end{tikzpicture}"))
FIG_CARS = Figure(name="rr_cars", caption=r"Two cars: $z^2 = x^2 + y^2$.", tikz=(
    r"\begin{tikzpicture}[scale=0.8]\draw[->] (0,0) -- (3.4,0) node[right] {E}; \draw[->] (0,0) -- (0,2.7) node[above] {N};"
    r"\fill (2.8,0) circle (2.5pt); \fill (0,2.1) circle (2.5pt); \draw[line width=1.4pt] (2.8,0) -- (0,2.1) node[midway, above right] {$z$};"
    r"\node[below] at (1.4,0) {$x$}; \node[left] at (0,1.05) {$y$};\end{tikzpicture}"))
FIG_SHADOW = Figure(name="rr_shadow", caption=r"The shadow: $\frac{15}{x + s} = \frac{5}{s}$.", tikz=(
    r"\begin{tikzpicture}[scale=0.8]\draw[line width=0.9pt] (-0.3,0) -- (4.6,0); \draw[line width=2pt] (0,0) -- (0,3);"
    r"\fill (0,3) circle (3pt); \draw[line width=2pt] (2.4,0) -- (2.4,1); \draw[dashed] (0,3) -- (3.6,0);"
    r"\node[left] at (0,1.5) {$15$}; \node[right] at (2.4,0.6) {$5$}; \node[below] at (1.2,0) {$x$};"
    r"\node[below] at (3,0) {$s$};\end{tikzpicture}"))
DIAGRAMS = [FigureRow([FIG_RIPPLE, FIG_LADDER, FIG_CONE]), FigureRow([FIG_CARS, FIG_SHADOW])]

STEPS = (r"\textbf{1. Know:} the quantities at the instant and the rates you are given, with units. \par "
         r"\textbf{2. Want:} the quantity or rate you are looking for. \par "
         r"\textbf{3. Fixed:} constants that never change (a ladder's length, a cone's proportions). These can go in from the start. \par "
         r"\textbf{4. Equation:} relate the quantities, usually from geometry. \par "
         r"\textbf{5. Differentiate} with respect to $t$, \emph{before} substituting anything that changes.")

NOTES = [
    Video("s4_4.py::Lesson", "Rates that are related", 8),

    Section("Everything depends on time"),
    Text(r"When several quantities change together, each one is a function of time $t$. If an equation links the quantities, then "
         r"differentiating that equation with respect to \blank{$t$} links their \blank{rates}."),
    Formula("Differentiating with respect to $t$", (
        r"Every variable gets the chain rule: \[ \frac{d}{dt}\left[r^2\right] = 2r\,\frac{dr}{dt}, \qquad \frac{d}{dt}\left[x y\right] = \frac{dx}{dt}\,y + x\,\frac{dy}{dt}. \] "
        r"Constants differentiate to $0$. A quantity that is changing must stay a \emph{variable} until after you differentiate.")),
    VideoExample('A growing square', work="2.6cm"),
    Text(r"\textbf{The common mistake.} Substituting $s = 4$ \emph{before} differentiating turns $A = s^2$ into $A = 16$, whose derivative is $0$. "
         r"Differentiate first, \blank{then} substitute."),

    Section("Formulas you need"),
    BigIdea(r"There is no formula sheet on the AP exam. Know the 2D formulas by heart: the area $\pi r^2$ and circumference $2\pi r$ of a "
            r"circle, the area $\frac12 bh$ of a triangle and $lw$ of a rectangle, the \blank{Pythagorean theorem} $a^2 + b^2 = c^2$, and "
            r"\blank{similar triangles}. A 3D formula (the volume of a cone, cylinder or sphere) is given in the problem when you need one."),

    Section("Setting up a related rates problem"),
    Formula("Five steps to the related rates equation", STEPS + r" \par Topic 4.5 adds the last step: substitute the values at the instant, and solve."),
    *DIAGRAMS,
    Text(r"These five setups (the ripple, the ladder, the cone, two cars, and the shadow) are the worked examples. Each one stops at "
         r"the differentiated equation; Topic 4.5 solves the same problems."),

    Section("Reading the rates"),
    Text(r"$\dfrac{dx}{dt} > 0$ means $x$ is increasing; $\dfrac{dx}{dt} < 0$ means $x$ is decreasing. Give each rate the units of its quantity "
         r"per unit of time."),
    BigIdea(r"An equation that relates quantities also relates their rates: differentiate both sides with respect to $t$, using the chain rule on every variable."),
    Check(r"$V = \frac43\pi r^3$. Write $\dfrac{dV}{dt}$ in terms of $r$ and $\dfrac{dr}{dt}$.", selfcheck(r"\frac{dV}{dt} = 4\pi r^2\,\frac{dr}{dt}"),
          r"\[ \frac{dV}{dt} = 4\pi r^2\,\frac{dr}{dt}. \]"),
]
same("square", d(s**2), 2 * s * d(s))
same("ripple", d(sp.pi * r**2), 2 * sp.pi * r * d(r))
same("ladder", d(x**2 + y**2), 2 * x * d(x) + 2 * y * d(y))
same("cone", sp.expand(sp.Rational(1, 3) * sp.pi * (h / 3)**2 * h), sp.pi / 27 * h**3)
same("cone d", d(sp.pi / 27 * h**3), sp.pi / 9 * h**2 * d(h))
same("shadow", sp.solve(sp.Eq(15 * s, 5 * (x + s)), s), [x / 2])

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
SET = r"Set it up: list what you know, what you want and what is fixed, write the equation, and differentiate with respect to $t$. (Don't solve yet.)"
PRACTICE += [
    Item(r"The radius of a circle grows at $3$ cm/s. We want how fast the area grows when $r = 5$ cm. " + SET,
         selfcheck(r"\frac{dA}{dt} = 2\pi r\,\frac{dr}{dt}"),
         r"Know: $\dfrac{dr}{dt} = 3$ cm/s, $r = 5$ cm. Want: $\dfrac{dA}{dt}$. Fixed: nothing. Equation: $A = \pi r^2$. "
         r"Differentiate: $\dfrac{dA}{dt} = 2\pi r\,\dfrac{dr}{dt}$.", work="2.2cm"),
    Item(r"A cube's edge grows at $0.5$ cm/min. We want how fast its volume grows when the edge is $4$ cm. (A cube with edge $s$ has volume "
         r"$V = s^3$.) " + SET, selfcheck(r"\frac{dV}{dt} = 3s^2\,\frac{ds}{dt}"),
         r"Know: $\dfrac{ds}{dt} = 0.5$ cm/min, $s = 4$ cm. Want: $\dfrac{dV}{dt}$. Equation: $V = s^3$. Differentiate: "
         r"$\dfrac{dV}{dt} = 3s^2\,\dfrac{ds}{dt}$.", work="2.2cm"),
    Item(r"A spherical balloon's radius grows at $0.2$ in/s. We want how fast its volume grows when $r = 5$ in. (The volume of a sphere "
         r"with radius $r$ is $V = \tfrac43\pi r^3$.) " + SET, selfcheck(r"\frac{dV}{dt} = 4\pi r^2\,\frac{dr}{dt}"),
         r"Know: $\dfrac{dr}{dt} = 0.2$ in/s, $r = 5$ in. Want: $\dfrac{dV}{dt}$. Equation: $V = \tfrac43\pi r^3$. Differentiate: "
         r"$\dfrac{dV}{dt} = 4\pi r^2\,\dfrac{dr}{dt}$.", work="2.2cm"),
    Item(r"A $10$-ft ladder leans against a wall, and its bottom slides away at $1$ ft/s. We want how fast the top slides down when the "
         r"bottom is $6$ ft from the wall. " + SET, selfcheck(r"2x\,\frac{dx}{dt} + 2y\,\frac{dy}{dt} = 0"),
         r"Know: $\dfrac{dx}{dt} = 1$ ft/s, $x = 6$ ft. Want: $\dfrac{dy}{dt}$. Fixed: the ladder, $10$ ft. Equation: $x^2 + y^2 = 100$. "
         r"Differentiate: $2x\,\dfrac{dx}{dt} + 2y\,\dfrac{dy}{dt} = 0$.", work="2.4cm"),
    Item(r"Water drains from a cone, point down, with radius $3$ m and height $6$ m, at $2$ m$^3$/min. We want how fast the depth $h$ falls "
         r"when it is $4$ m. (The volume of a cone with radius $r$ and height $h$ is $V = \tfrac13\pi r^2 h$.) " + SET,
         selfcheck(r"\frac{dV}{dt} = \frac{\pi}{4}h^2\,\frac{dh}{dt}"),
         r"Know: $\dfrac{dV}{dt} = -2$ m$^3$/min, $h = 4$ m. Want: $\dfrac{dh}{dt}$. Fixed: the cone's shape, $\dfrac rh = \dfrac36$, so "
         r"$r = \dfrac h2$. Equation: $V = \tfrac13\pi\left(\tfrac h2\right)^2 h = \tfrac{\pi}{12}h^3$. Differentiate: "
         r"$\dfrac{dV}{dt} = \dfrac{\pi}{4}h^2\,\dfrac{dh}{dt}$.", work="2.8cm"),
    Item(r"Two cyclists leave the same point, one north at $12$ mph and one east at $16$ mph. We want how fast the distance $z$ between "
         r"them grows after $1$ hour. " + SET, selfcheck(r"z\,\frac{dz}{dt} = x\,\frac{dx}{dt} + y\,\frac{dy}{dt}"),
         r"Know: $\dfrac{dx}{dt} = 16$ mph (east), $\dfrac{dy}{dt} = 12$ mph (north), $t = 1$ h. Want: $\dfrac{dz}{dt}$. Equation: "
         r"$z^2 = x^2 + y^2$. Differentiate: $2z\,\dfrac{dz}{dt} = 2x\,\dfrac{dx}{dt} + 2y\,\dfrac{dy}{dt}$.", work="2.4cm"),
    Item(r"A $6$-ft man walks toward an $18$-ft lamppost at $3$ ft/s. Let $x$ be his distance from the post and $s$ the length of his "
         r"shadow. " + SET, selfcheck(r"\frac{ds}{dt} = \frac12\,\frac{dx}{dt}"),
         r"Know: $\dfrac{dx}{dt} = -3$ ft/s. Want: $\dfrac{ds}{dt}$. Fixed: the heights $18$ and $6$. Similar triangles: "
         r"$\dfrac{18}{x + s} = \dfrac{6}{s}$, so $18s = 6x + 6s$ and $s = \dfrac x2$. Differentiate: $\dfrac{ds}{dt} = \dfrac12\,\dfrac{dx}{dt}$.",
         work="2.6cm"),
    Item(r"A kite flies at a constant height of $60$ ft and drifts horizontally away from the flyer. Let $x$ be the horizontal distance "
         r"and $z$ the length of string. Write the equation relating them and differentiate it with respect to $t$.",
         selfcheck(r"z\,\frac{dz}{dt} = x\,\frac{dx}{dt}"),
         r"Fixed: the height, $60$ ft. $z^2 = x^2 + 60^2$, so $2z\,\dfrac{dz}{dt} = 2x\,\dfrac{dx}{dt}$: the constant $60^2$ "
         r"differentiates to $0$.", work="2cm"),
    Item(r"A rectangle's length $l$ grows at $2$ m/s and its width $w$ shrinks at $1$ m/s. Write $\dfrac{dA}{dt}$ in terms of $l$, $w$ "
         r"and their rates, and say what goes in for $\dfrac{dw}{dt}$.", selfcheck(r"\frac{dA}{dt} = \frac{dl}{dt}\,w + l\,\frac{dw}{dt};\ \frac{dw}{dt} = -1"),
         r"$A = lw$, so $\dfrac{dA}{dt} = \dfrac{dl}{dt}\,w + l\,\dfrac{dw}{dt}$. The width shrinks, so $\dfrac{dw}{dt} = -1$ m/s.", work="2cm"),
    Item(r"$y = x^3$, and $x$ increases at $2$ units per second. Write $\dfrac{dy}{dt}$ in terms of $x$ and $\dfrac{dx}{dt}$.",
         selfcheck(r"\frac{dy}{dt} = 3x^2\,\frac{dx}{dt}"), r"\[ \frac{dy}{dt} = 3x^2\,\frac{dx}{dt}. \]", work="1.4cm"),
    Item(r"Explain why you may not substitute $r = 5$ into $A = \pi r^2$ before differentiating with respect to $t$.",
         selfcheck(r"r \text{ is changing}"), r"$r$ is changing. Substituting first makes $A = 25\pi$, a constant, and its derivative would be $0$.", work="1.4cm"),
    Item(r"In the ladder problem above, which quantity is fixed, and why may it be substituted before you differentiate?",
         selfcheck(r"\text{the ladder's length}"), r"The ladder's length, $10$ ft, never changes, so it is a constant at every moment, not just at the instant.",
         work="1.4cm"),
]
same("p", [d(sp.pi / 12 * h**3), d(z**2 - x**2 - 3600), sp.solve(sp.Eq(18 * s, 6 * (x + s)), s), d(l * w), d(x**3)],
     [sp.pi / 4 * h**2 * d(h), 2 * z * d(z) - 2 * x * d(x), [x / 2], d(l) * w + l * d(w), 3 * x**2 * d(x)])

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
        Item(r"The radius of a circle grows at $2$ m/s. Write the equation relating $\dfrac{dA}{dt}$ and $\dfrac{dr}{dt}$, and say what goes in for "
             r"$\dfrac{dr}{dt}$.", selfcheck(r"\frac{dA}{dt} = 2\pi r\,\frac{dr}{dt},\ \frac{dr}{dt} = 2"),
             r"$A = \pi r^2$, so $\dfrac{dA}{dt} = 2\pi r\,\dfrac{dr}{dt}$, with $\dfrac{dr}{dt} = 2$ m/s.", work="1.6cm"),
        Item(r"The side of a square shrinks at $3$ cm/s. Write the equation relating $\dfrac{dA}{dt}$ and $\dfrac{ds}{dt}$, and say what goes in "
             r"for $\dfrac{ds}{dt}$.", selfcheck(r"\frac{dA}{dt} = 2s\,\frac{ds}{dt},\ \frac{ds}{dt} = -3"),
             r"$A = s^2$, so $\dfrac{dA}{dt} = 2s\,\dfrac{ds}{dt}$, with $\dfrac{ds}{dt} = -3$ cm/s (shrinking).", work="1.6cm"),
        Item(r"The circumference $C$ of a circle grows at $4$ in/s. Write the equation relating $\dfrac{dC}{dt}$ and $\dfrac{dr}{dt}$.",
             selfcheck(r"\frac{dC}{dt} = 2\pi\,\frac{dr}{dt}"), r"$C = 2\pi r$, so $\dfrac{dC}{dt} = 2\pi\,\dfrac{dr}{dt}$.", work="1.6cm"),
    ),
    Variants(
        MCQ(r"A $13$-ft ladder slides down a wall. With $x$ the bottom's distance from the wall and $y$ the top's height, which equation holds at every moment?",
            [r"$x + y = 13$", r"$x^2 + y^2 = 169$", r"$xy = 13$", r"$x^2 + y^2 = 13$"], "B", r"The ladder is the hypotenuse: $x^2 + y^2 = 13^2$."),
        MCQ(r"A $17$-ft ladder slides down a wall. With $x$ the bottom's distance from the wall and $y$ the top's height, which equation holds at every moment?",
            [r"$x^2 + y^2 = 17$", r"$x + y = 17$", r"$x^2 + y^2 = 289$", r"$y = 17 - x$"], "C", r"The ladder is the hypotenuse: $x^2 + y^2 = 17^2$."),
        MCQ(r"A $5$-m ladder slides down a wall. With $x$ the bottom's distance from the wall and $y$ the top's height, which equation holds at every moment?",
            [r"$x^2 + y^2 = 25$", r"$x + y = 5$", r"$xy = 5$", r"$x^2 - y^2 = 25$"], "A", r"The ladder is the hypotenuse: $x^2 + y^2 = 5^2$."),
    ),
    Variants(
        MCQ(r"Differentiating $xy = 20$ with respect to $t$ gives", [r"$\dfrac{dx}{dt}\dfrac{dy}{dt} = 0$", r"$\dfrac{dx}{dt}\,y + x\,\dfrac{dy}{dt} = 0$",
            r"$x\,\dfrac{dx}{dt} + y\,\dfrac{dy}{dt} = 0$", r"$\dfrac{dx}{dt}\,y + x\,\dfrac{dy}{dt} = 20$"], "B", r"Product rule; the constant gives $0$."),
        MCQ(r"Differentiating $z^2 = x^2 + 36$ with respect to $t$ gives", [r"$2z\,\dfrac{dz}{dt} = 2x\,\dfrac{dx}{dt} + 36$", r"$2z = 2x$",
            r"$2z\,\dfrac{dz}{dt} = 2x\,\dfrac{dx}{dt}$", r"$z\,\dfrac{dz}{dt} = 36$"], "C", r"The constant $36$ differentiates to $0$."),
        MCQ(r"Differentiating $y = x^2 + 3x$ with respect to $t$ gives", [r"$\dfrac{dy}{dt} = 2x + 3$", r"$\dfrac{dy}{dt} = (2x + 3)\,\dfrac{dx}{dt}$",
            r"$\dfrac{dy}{dt} = 2x\,\dfrac{dx}{dt} + 3$", r"$\dfrac{dy}{dt} = x^2\,\dfrac{dx}{dt}$"], "B", r"Chain rule on every term in $x$."),
    ),
    Variants(
        MCQ(r"Which step comes first in a related rates problem?", [r"Substitute the given values", r"Differentiate with respect to $t$",
            r"List what you know and what you want", r"Solve for the unknown rate"], "C", r"Know, want, fixed, equation, differentiate; then substitute."),
        MCQ(r"A student substitutes $r = 5$ into $A = \pi r^2$ and then differentiates. The result is", [r"correct", r"$\dfrac{dA}{dt} = 0$, which is wrong",
            r"$10\pi\,\dfrac{dr}{dt}$", r"$25\pi$"], "B", r"$A = 25\pi$ is a constant, so its derivative is $0$. Differentiate first."),
        MCQ(r"If $\dfrac{dx}{dt} < 0$, then", [r"$x$ is negative", r"$x$ is decreasing", r"$x$ is increasing", r"$x$ is constant"], "B", r"A negative rate means decreasing."),
    ),
]
same("q", [d(x * y), d(z**2 - x**2 - 36), d(x**2 + 3 * x)], [d(x) * y + x * d(y), 2 * z * d(z) - 2 * x * d(x), (2 * x + 3) * d(x)])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"The area $A$ of a circle increases at $10\pi$ cm$^2$/s. Which equation relates the rates at the instant $r = 5$ cm?",
        [r"$10\pi = 2\pi(5)$", r"$10\pi = 2\pi(5)\dfrac{dr}{dt}$", r"$10\pi = \pi(25)\dfrac{dr}{dt}$", r"$\dfrac{dr}{dt} = 2\pi(5)(10\pi)$"], "B",
        r"$\dfrac{dA}{dt} = 2\pi r\dfrac{dr}{dt}$, with $\dfrac{dA}{dt} = 10\pi$ and $r = 5$.", why_not={"A": "forgot $\\frac{dr}{dt}$"}),
    MCQ(r"If $y = 2x^2 - 3x$, then $\dfrac{dy}{dt} =$", [r"$4x - 3$", r"$(4x - 3)\dfrac{dx}{dt}$", r"$4x\dfrac{dx}{dt} - 3$", r"$(2x^2 - 3x)\dfrac{dx}{dt}$"], "B",
        r"Chain rule on every term in $x$.", why_not={"A": "forgot $\\frac{dx}{dt}$"}),
    MCQ(r"The volume of a sphere is $V = \frac43\pi r^3$. Differentiating with respect to $t$ gives", [r"$\dfrac{dV}{dt} = 4\pi r^2$",
        r"$\dfrac{dV}{dt} = \frac43\pi r^3\dfrac{dr}{dt}$", r"$\dfrac{dV}{dt} = 4\pi r^2\dfrac{dr}{dt}$", r"$\dfrac{dV}{dt} = \frac43\pi\dfrac{dr}{dt}$"], "C",
        r"Chain rule: $\frac43\pi \cdot 3r^2\,\dfrac{dr}{dt}$."),
    MCQ(r"$x$ and $y$ are functions of $t$ with $x^2y = 12$. Differentiating with respect to $t$ gives", [r"$2xy\,\dfrac{dx}{dt} + x^2\,\dfrac{dy}{dt} = 0$",
        r"$2x\,\dfrac{dx}{dt}\,\dfrac{dy}{dt} = 0$", r"$2xy + x^2 = 0$", r"$2x\,\dfrac{dx}{dt} + \dfrac{dy}{dt} = 12$"], "A", r"Product rule, then the chain rule on $x^2$."),
]
same("m", [d(sp.pi * r**2), d(2 * x**2 - 3 * x), d(sp.Rational(4, 3) * sp.pi * r**3), d(x**2 * y)],
     [2 * sp.pi * r * d(r), (4 * x - 3) * d(x), 4 * sp.pi * r**2 * d(r), 2 * x * y * d(x) + x**2 * d(y)])

FRQS = [
    FRQ("Rolling out dough", (
        r"A baker rolls a lump of dough into the shape of a cylinder. As the dough is rolled, its radius $r$ and height $h$, both "
        r"measured in centimeters, change with time $t$, measured in seconds, but its volume stays the same. "
        r"(The volume of a cylinder with radius $r$ and height $h$ is $V = \pi r^2 h$.)"), [
        Part("a", r"Differentiate $V = \pi r^2 h$ with respect to $t$.",
             selfcheck(r"\frac{dV}{dt} = 2\pi rh\,\frac{dr}{dt} + \pi r^2\,\frac{dh}{dt}"),
             r"Product rule, with the chain rule on $r^2$: $\dfrac{dV}{dt} = 2\pi rh\,\dfrac{dr}{dt} + \pi r^2\,\dfrac{dh}{dt}$.",
             [(1, "product rule"), (1, "chain rule: $\\frac{dr}{dt}$ and $\\frac{dh}{dt}$ both appear")], work="2.4cm"),
        Part("b", r"Explain why $\dfrac{dV}{dt} = 0$, and write the equation that relates $\dfrac{dr}{dt}$ and $\dfrac{dh}{dt}$ at any moment.",
             selfcheck(r"0 = 2\pi rh\,\frac{dr}{dt} + \pi r^2\,\frac{dh}{dt}"),
             r"The volume stays the same, so it is constant and $\dfrac{dV}{dt} = 0$: $0 = 2\pi rh\,\dfrac{dr}{dt} + \pi r^2\,\dfrac{dh}{dt}$.",
             [(1, "volume constant, so $\\frac{dV}{dt} = 0$"), (1, "the equation")], work="2.2cm"),
        Part("c", r"The top of the dough is a circle with area $A = \pi r^2$. Write $\dfrac{dA}{dt}$ in terms of $r$ and $\dfrac{dr}{dt}$. "
                  r"If the radius is increasing, is the area of the top increasing or decreasing?",
             selfcheck(r"\frac{dA}{dt} = 2\pi r\,\frac{dr}{dt};\ \text{increasing}"),
             r"$\dfrac{dA}{dt} = 2\pi r\,\dfrac{dr}{dt}$. With $r > 0$ and $\dfrac{dr}{dt} > 0$, $\dfrac{dA}{dt} > 0$: increasing.",
             [(1, "$\\frac{dA}{dt} = 2\\pi r\\frac{dr}{dt}$"), (1, "increasing, with the sign reason")], work="2cm"),
    ], frq_type="Related rates"),
]
same("frq a", d(sp.pi * r**2 * h), 2 * sp.pi * r * h * d(r) + sp.pi * r**2 * d(h))

TOPIC = Topic(
    number="4.4", title="Introduction to Related Rates",
    unit="Unit 4: Contextual Applications of Differentiation", ced=["CHA-3.D", "CHA-3.D.1"],
    goals=r"Set up a related rates problem: name the changing quantities, write an equation that relates them, and differentiate it "
          r"with respect to time.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
