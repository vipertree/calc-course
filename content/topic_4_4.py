"""Topic 4.4: Introduction to related rates.

CED: CHA-3.D (CHA-3.D.1): when quantities related by an equation change with time, differentiating the equation with
respect to t (implicitly, using the chain rule) relates their rates.

Adder (2026-10-23): 4.4 and 4.5 go through the SAME problems in the same order: the ripple, the ladder, two cars (Priya
driving toward the intersection, Kai away), the shadow, the cone. In 4.4 no problem gives a rate or a value at an instant:
each says "write an equation that relates ..., then differentiate with respect to time". Four steps: draw and label, name
what changes, relate, differentiate. A fixed quantity (the ladder's 13 ft) is noted when the equation is written, never as
a step. Practice, quiz and test prep here are equations and derivatives only; 4.5 has the know/want strategy and solves.
3D volume formulas are always stated in the problem, as on the AP exam; 2D formulas (circle, triangle, rectangle, Pythagorean theorem, similar triangles) are not.
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
FIG_CARS = Figure(name="rr_cars", caption=r"Two cars: Priya drives toward the intersection, Kai away; $z^2 = x^2 + y^2$.", tikz=(
    r"\begin{tikzpicture}[scale=0.8]\draw[line width=5pt, black!15] (-0.3,0) -- (3.6,0); \draw[line width=5pt, black!15] (0,-0.3) -- (0,2.9);"
    r"\node[right] at (3.6,0) {E}; \node[above] at (0,2.9) {N};"
    r"\fill (2.8,0) circle (2.5pt); \fill (0,2.1) circle (2.5pt); \draw[line width=1.4pt] (2.8,0) -- (0,2.1) node[midway, above right] {$z$};"
    r"\draw[->, line width=0.9pt] (2.8,-0.3) -- (2.1,-0.3); \draw[->, line width=0.9pt] (-0.3,2.1) -- (-0.3,2.7);"
    r"\node[below] at (1.2,0) {$x$}; \node[left] at (0,1.0) {$y$};\end{tikzpicture}"))
FIG_SHADOW = Figure(name="rr_shadow", caption=r"The shadow: $\frac{15}{x + s} = \frac{5}{s}$.", tikz=(
    r"\begin{tikzpicture}[scale=0.8]\draw[line width=0.9pt] (-0.3,0) -- (4.6,0); \draw[line width=2pt] (0,0) -- (0,3);"
    r"\fill (0,3) circle (3pt); \draw[line width=2pt] (2.4,0) -- (2.4,1); \draw[dashed] (0,3) -- (3.6,0);"
    r"\node[left] at (0,1.5) {$15$}; \node[right] at (2.4,0.6) {$5$}; \node[below] at (1.2,0) {$x$};"
    r"\node[below] at (3,0) {$s$};\end{tikzpicture}"))
DIAGRAMS = [FigureRow([FIG_RIPPLE, FIG_LADDER, FIG_CARS]), FigureRow([FIG_SHADOW, FIG_CONE])]

STEPS = (r"\textbf{1. Draw and label} a picture. \par "
         r"\textbf{2. Name what changes:} each changing quantity gets a letter and is a function of $t$. Anything that never "
         r"changes (a ladder's length, a cone's height and radius) stays a number. \par "
         r"\textbf{3. Relate:} write an equation that holds at every moment, usually from geometry. \par "
         r"\textbf{4. Differentiate} both sides with respect to $t$, with the chain rule on every variable.")

NOTES = [
    Video("s4_4.py::Lesson", "Rates that are related", 7.2),

    Section("Everything depends on time"),
    Text(r"When several quantities change together, each one is a function of time $t$. If an equation links the quantities, then "
         r"differentiating that equation with respect to \blank{$t$} links their \blank{rates}."),
    Formula("Differentiating with respect to $t$", (
        r"Every variable gets the chain rule: \[ \frac{d}{dt}\left[r^2\right] = 2r\,\frac{dr}{dt}, \qquad \frac{d}{dt}\left[x y\right] = \frac{dx}{dt}\,y + x\,\frac{dy}{dt}. \] "
        r"A constant, such as a ladder's fixed length, differentiates to $0$.")),

    Section("Formulas you need"),
    BigIdea(r"There is no formula sheet on the AP exam. Know the 2D formulas by heart: the area $\pi r^2$ and circumference $2\pi r$ of a "
            r"circle, the area $\frac12 bh$ of a triangle and $lw$ of a rectangle, the \blank{Pythagorean theorem} $a^2 + b^2 = c^2$, and "
            r"\blank{similar triangles}. A 3D formula (the volume of a cone, cylinder or sphere) is given in the problem when you need one."),
    Text(r"Most equations come from a picture: the Pythagorean theorem for right triangles, similar triangles for shadows and cones, "
         r"volume and area formulas for tanks and balloons, and right-triangle trig for angles."),
    Text(r"\textbf{One variable too many.} When the question relates two quantities but the formula has a third (the water's radius $r$ "
         r"in a cone, when the question is about the volume and the depth), use the geometry to write the extra one in terms of the "
         r"others \emph{before} differentiating."),

    Section("Writing the related rates equation"),
    Formula("Four steps to the related rates equation", STEPS + r" \par Topic 4.5 puts in the numbers for an instant and solves."),
    *DIAGRAMS,
    VideoExample('The ripple', work="2.6cm"),
    Text(r"The ripple, the ladder, two cars, the shadow and the cone are this topic's problems. Topic 4.5 solves the same five "
         r"problems, in the same order, once the rates and values at an instant are given."),
    BigIdea(r"An equation that relates quantities also relates their rates: differentiate both sides with respect to $t$, using the chain rule on every variable."),
    Check(r"$V = \frac43\pi r^3$. Write $\dfrac{dV}{dt}$ in terms of $r$ and $\dfrac{dr}{dt}$.", selfcheck(r"\frac{dV}{dt} = 4\pi r^2\,\frac{dr}{dt}"),
          r"\[ \frac{dV}{dt} = 4\pi r^2\,\frac{dr}{dt}. \]"),
]
same("ripple", d(sp.pi * r**2), 2 * sp.pi * r * d(r))
same("ladder", d(x**2 + y**2 - 13**2), 2 * x * d(x) + 2 * y * d(y))
same("cars", d(z**2 - x**2 - y**2), 2 * z * d(z) - 2 * x * d(x) - 2 * y * d(y))
same("shadow", sp.solve(sp.Eq(15 * s, 5 * (x + s)), s), [x / 2])
same("shadow d", d(x / 2), d(x) / 2)
same("cone", sp.expand(sp.Rational(1, 3) * sp.pi * (h / 3)**2 * h), sp.pi / 27 * h**3)
same("cone d", d(sp.pi / 27 * h**3), sp.pi / 9 * h**2 * d(h))

# ---------------------------------------------------------------- practice: equations and derivatives only (Adder, 2026-10-23)
P = [
    (r"$A = \pi r^2$", r"\frac{dA}{dt} = 2\pi r\,\frac{dr}{dt}"),
    (r"$V = s^3$", r"\frac{dV}{dt} = 3s^2\,\frac{ds}{dt}"),
    (r"$x^2 + y^2 = 100$", r"2x\,\frac{dx}{dt} + 2y\,\frac{dy}{dt} = 0"),
    (r"$xy = 12$", r"\frac{dx}{dt}\,y + x\,\frac{dy}{dt} = 0"),
    (r"$V = \pi r^2 h$ (both $r$ and $h$ change)", r"\frac{dV}{dt} = 2\pi r h\,\frac{dr}{dt} + \pi r^2\,\frac{dh}{dt}"),
    (r"$z^2 = x^2 + y^2$", r"2z\,\frac{dz}{dt} = 2x\,\frac{dx}{dt} + 2y\,\frac{dy}{dt}"),
]
PRACTICE = [Item(rf"Differentiate with respect to $t$: {eq}.", selfcheck(ans), rf"\[ {ans} \]", work="1.6cm") for eq, ans in P]
DIFF = r" Then differentiate with respect to time."
PRACTICE += [
    Item(r"Oil spreads on a lake in a circle. Write an equation that relates the area $A$ of the slick and its radius $r$." + DIFF,
         selfcheck(r"\frac{dA}{dt} = 2\pi r\,\frac{dr}{dt}"),
         r"Changing: $A$ and $r$. $A = \pi r^2$, so $\dfrac{dA}{dt} = 2\pi r\,\dfrac{dr}{dt}$.", work="2cm"),
    Item(r"A cube of ice melts and keeps its shape. Write an equation that relates its volume $V$ and its edge $s$." + DIFF +
         r" (A cube with edge $s$ has volume $V = s^3$.)", selfcheck(r"\frac{dV}{dt} = 3s^2\,\frac{ds}{dt}"),
         r"Changing: $V$ and $s$. $V = s^3$, so $\dfrac{dV}{dt} = 3s^2\,\dfrac{ds}{dt}$.", work="2cm"),
    Item(r"A spherical balloon is being inflated. Write an equation that relates its volume $V$ and its radius $r$." + DIFF +
         r" (The volume of a sphere with radius $r$ is $V = \tfrac43\pi r^3$.)", selfcheck(r"\frac{dV}{dt} = 4\pi r^2\,\frac{dr}{dt}"),
         r"Changing: $V$ and $r$. $V = \tfrac43\pi r^3$, so $\dfrac{dV}{dt} = 4\pi r^2\,\dfrac{dr}{dt}$.", work="2cm"),
    Item(r"A $10$-ft ladder leans against a wall, and its bottom slides away from the wall. Write an equation that relates the bottom's "
         r"distance $x$ from the wall and the height $y$ of the top." + DIFF, selfcheck(r"2x\,\frac{dx}{dt} + 2y\,\frac{dy}{dt} = 0"),
         r"Changing: $x$ and $y$. The ladder stays $10$ ft long, so $x^2 + y^2 = 10^2$. Differentiate: "
         r"$2x\,\dfrac{dx}{dt} + 2y\,\dfrac{dy}{dt} = 0$.", work="2.2cm"),
    Item(r"Water drains from a cone, point down, with radius $3$ m at the top and height $6$ m. Write an equation that relates the volume "
         r"$V$ of the water and its depth $h$." + DIFF + r" (The volume of a cone with radius $r$ and height $h$ is $V = \tfrac13\pi r^2 h$.)",
         selfcheck(r"V = \frac{\pi}{12}h^3,\ \frac{dV}{dt} = \frac{\pi}{4}h^2\,\frac{dh}{dt}"),
         r"Changing: $V$, $h$ and the water's radius $r$. The cone stays $3$ by $6$, so similar triangles give $\dfrac rh = \dfrac36$ and "
         r"$r = \dfrac h2$. Then $V = \tfrac13\pi\left(\tfrac h2\right)^2 h = \tfrac{\pi}{12}h^3$, and "
         r"$\dfrac{dV}{dt} = \dfrac{\pi}{4}h^2\,\dfrac{dh}{dt}$.", work="2.8cm"),
    Item(r"Mateo bikes south toward a corner, and Jun bikes east away from it. Let $x$ be Jun's distance from the corner, $y$ Mateo's, "
         r"and $z$ the distance between them. Write an equation that relates $x$, $y$ and $z$." + DIFF,
         selfcheck(r"2z\,\frac{dz}{dt} = 2x\,\frac{dx}{dt} + 2y\,\frac{dy}{dt}"),
         r"The roads meet at a right angle: $z^2 = x^2 + y^2$. Differentiate: $2z\,\dfrac{dz}{dt} = 2x\,\dfrac{dx}{dt} + 2y\,\dfrac{dy}{dt}$. "
         r"Which way each rider goes does not change the equation.", work="2.4cm"),
    Item(r"A $6$-ft man walks toward an $18$-ft lamppost. Let $x$ be his distance from the post and $s$ the length of his shadow. Write "
         r"an equation that relates $x$ and $s$." + DIFF, selfcheck(r"s = \frac x2,\ \frac{ds}{dt} = \frac12\,\frac{dx}{dt}"),
         r"The heights stay $18$ and $6$. Similar triangles: $\dfrac{18}{x + s} = \dfrac{6}{s}$, so $18s = 6x + 6s$, $12s = 6x$ and "
         r"$s = \dfrac x2$. Differentiate: $\dfrac{ds}{dt} = \dfrac12\,\dfrac{dx}{dt}$.", work="2.6cm"),
    Item(r"A kite flies at a constant height of $60$ ft and drifts horizontally away from the flyer. Let $x$ be the horizontal distance "
         r"and $z$ the length of string. Write an equation that relates them." + DIFF, selfcheck(r"z\,\frac{dz}{dt} = x\,\frac{dx}{dt}"),
         r"The height stays $60$ ft: $z^2 = x^2 + 60^2$, so $2z\,\dfrac{dz}{dt} = 2x\,\dfrac{dx}{dt}$, since the constant $60^2$ "
         r"differentiates to $0$.", work="2cm"),
    Item(r"A cylindrical tank with radius $2$ m is filling with water. Write an equation that relates the volume $V$ of the water and its "
         r"depth $h$." + DIFF + r" (The volume of a cylinder with radius $r$ and height $h$ is $V = \pi r^2 h$.)",
         selfcheck(r"V = 4\pi h,\ \frac{dV}{dt} = 4\pi\,\frac{dh}{dt}"),
         r"The radius stays $2$ m: $V = \pi(2)^2 h = 4\pi h$, so $\dfrac{dV}{dt} = 4\pi\,\dfrac{dh}{dt}$.", work="2cm"),
    Item(r"Lin stands $30$ m from where a balloon is rising straight up. Write an equation that relates the angle of elevation $\theta$ "
         r"and the balloon's height $y$." + DIFF, selfcheck(r"\sec^2\theta\,\frac{d\theta}{dt} = \frac{1}{30}\,\frac{dy}{dt}"),
         r"The distance stays $30$ m: $\tan\theta = \dfrac{y}{30}$. Differentiate: $\sec^2\theta\,\dfrac{d\theta}{dt} = \dfrac{1}{30}\,\dfrac{dy}{dt}$.",
         work="2.2cm"),
    Item(r"A rectangle's length $l$ and width $w$ both change. Write $\dfrac{dA}{dt}$ in terms of $l$, $w$ and their rates.",
         selfcheck(r"\frac{dA}{dt} = \frac{dl}{dt}\,w + l\,\frac{dw}{dt}"),
         r"$A = lw$, so the product rule gives $\dfrac{dA}{dt} = \dfrac{dl}{dt}\,w + l\,\dfrac{dw}{dt}$.", work="1.8cm"),
    Item(r"$y = x^3$, and $x$ changes with time. Write $\dfrac{dy}{dt}$ in terms of $x$ and $\dfrac{dx}{dt}$.",
         selfcheck(r"\frac{dy}{dt} = 3x^2\,\frac{dx}{dt}"), r"\[ \frac{dy}{dt} = 3x^2\,\frac{dx}{dt}. \]", work="1.4cm"),
]
th = sp.Function("th")(t)
same("p", [d(sp.pi * r**2), d(s**3), d(sp.Rational(4, 3) * sp.pi * r**3), d(x**2 + y**2 - 100),
           sp.expand(sp.Rational(1, 3) * sp.pi * (h / 2)**2 * h), d(sp.pi / 12 * h**3), sp.solve(sp.Eq(18 * s, 6 * (x + s)), s),
           d(z**2 - x**2 - 3600), d(sp.pi * 2**2 * h), d(sp.tan(th) - y / 30), d(l * w), d(x**3)],
     [2 * sp.pi * r * d(r), 3 * s**2 * d(s), 4 * sp.pi * r**2 * d(r), 2 * x * d(x) + 2 * y * d(y),
      sp.pi / 12 * h**3, sp.pi / 4 * h**2 * d(h), [x / 2],
      2 * z * d(z) - 2 * x * d(x), 4 * sp.pi * d(h), (1 + sp.tan(th)**2) * d(th) - d(y) / 30, d(l) * w + l * d(w), 3 * x**2 * d(x)])

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
        Item(r"The radius $r$ of a circle changes with time. Write an equation that relates its area $A$ and $r$, then differentiate it with "
             r"respect to $t$.", selfcheck(r"A = \pi r^2,\ \frac{dA}{dt} = 2\pi r\,\frac{dr}{dt}"),
             r"$A = \pi r^2$, so $\dfrac{dA}{dt} = 2\pi r\,\dfrac{dr}{dt}$.", work="1.6cm"),
        Item(r"The side $s$ of a square changes with time. Write an equation that relates its area $A$ and $s$, then differentiate it with "
             r"respect to $t$.", selfcheck(r"A = s^2,\ \frac{dA}{dt} = 2s\,\frac{ds}{dt}"),
             r"$A = s^2$, so $\dfrac{dA}{dt} = 2s\,\dfrac{ds}{dt}$.", work="1.6cm"),
        Item(r"The radius $r$ of a circle changes with time. Write an equation that relates its circumference $C$ and $r$, then differentiate "
             r"it with respect to $t$.", selfcheck(r"C = 2\pi r,\ \frac{dC}{dt} = 2\pi\,\frac{dr}{dt}"),
             r"$C = 2\pi r$, so $\dfrac{dC}{dt} = 2\pi\,\dfrac{dr}{dt}$.", work="1.6cm"),
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
        MCQ(r"Which step comes first when you write a related rates equation?", [r"Differentiate with respect to $t$",
            r"Draw and label a picture", r"Substitute the given values", r"Solve for the unknown rate"], "B",
            r"Draw and label, name what changes, relate, then differentiate."),
        MCQ(r"A $13$-ft ladder slides down a wall, so $x^2 + y^2 = 13^2$. Differentiating with respect to $t$, the derivative of $13^2$ is",
            [r"$26$", r"$169$", r"$0$", r"$26\,\dfrac{dx}{dt}$"], "C", r"The ladder's length is fixed, so $13^2$ is a constant and its derivative is $0$."),
        MCQ(r"Priya drives toward an intersection and Kai drives away from it on a road at a right angle to hers. With $x$ and $y$ their "
            r"distances from the intersection and $z$ the distance between them, which equation holds at every moment?",
            [r"$z = x + y$", r"$z^2 = x^2 + y^2$", r"$z^2 = x^2 - y^2$", r"$z = xy$"], "B",
            r"The roads meet at a right angle, so $z$ is the hypotenuse. Which way each car goes does not change the equation."),
    ),
]
same("q", [d(x * y), d(z**2 - x**2 - 36), d(x**2 + 3 * x)], [d(x) * y + x * d(y), 2 * z * d(z) - 2 * x * d(x), (2 * x + 3) * d(x)])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"Water fills a cone, point down, whose height is twice its radius at every level. With $h$ the depth of the water, which "
        r"equation relates $\dfrac{dV}{dt}$ and $\dfrac{dh}{dt}$? (The volume of a cone with radius $r$ and height $h$ is $V = \tfrac13\pi r^2 h$.)",
        [r"$\dfrac{dV}{dt} = \dfrac{\pi}{4}h^2\,\dfrac{dh}{dt}$", r"$\dfrac{dV}{dt} = \dfrac{\pi}{12}h^3\,\dfrac{dh}{dt}$",
         r"$\dfrac{dV}{dt} = \pi h^2\,\dfrac{dh}{dt}$", r"$\dfrac{dV}{dt} = \dfrac{\pi}{4}h^2$"], "A",
        r"$r = \dfrac h2$, so $V = \dfrac13\pi\left(\dfrac h2\right)^2 h = \dfrac{\pi}{12}h^3$ and $\dfrac{dV}{dt} = \dfrac{\pi}{4}h^2\,\dfrac{dh}{dt}$.",
        why_not={r"$\dfrac{dV}{dt} = \dfrac{\pi}{4}h^2$": "forgot $\\frac{dh}{dt}$"}),
    MCQ(r"If $y = 2x^2 - 3x$, then $\dfrac{dy}{dt} =$", [r"$4x - 3$", r"$(4x - 3)\dfrac{dx}{dt}$", r"$4x\dfrac{dx}{dt} - 3$", r"$(2x^2 - 3x)\dfrac{dx}{dt}$"], "B",
        r"Chain rule on every term in $x$.", why_not={"A": "forgot $\\frac{dx}{dt}$"}),
    MCQ(r"The volume of a sphere is $V = \frac43\pi r^3$. Differentiating with respect to $t$ gives", [r"$\dfrac{dV}{dt} = 4\pi r^2$",
        r"$\dfrac{dV}{dt} = \frac43\pi r^3\dfrac{dr}{dt}$", r"$\dfrac{dV}{dt} = 4\pi r^2\dfrac{dr}{dt}$", r"$\dfrac{dV}{dt} = \frac43\pi\dfrac{dr}{dt}$"], "C",
        r"Chain rule: $\frac43\pi \cdot 3r^2\,\dfrac{dr}{dt}$."),
    MCQ(r"$x$ and $y$ are functions of $t$ with $x^2y = 12$. Differentiating with respect to $t$ gives", [r"$2xy\,\dfrac{dx}{dt} + x^2\,\dfrac{dy}{dt} = 0$",
        r"$2x\,\dfrac{dx}{dt}\,\dfrac{dy}{dt} = 0$", r"$2xy + x^2 = 0$", r"$2x\,\dfrac{dx}{dt} + \dfrac{dy}{dt} = 12$"], "A", r"Product rule, then the chain rule on $x^2$."),
]
same("m", [d(sp.pi / 12 * h**3), d(2 * x**2 - 3 * x), d(sp.Rational(4, 3) * sp.pi * r**3), d(x**2 * y)],
     [sp.pi / 4 * h**2 * d(h), (4 * x - 3) * d(x), 4 * sp.pi * r**2 * d(r), 2 * x * y * d(x) + x**2 * d(y)])
same("m cone", sp.expand(sp.Rational(1, 3) * sp.pi * (h / 2)**2 * h), sp.pi / 12 * h**3)

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
        Part("c", r"The top of the dough is a circle with area $A = \pi r^2$. Write an expression for $\dfrac{dA}{dt}$ in terms of $r$ and "
                  r"$\dfrac{dr}{dt}$.", selfcheck(r"\frac{dA}{dt} = 2\pi r\,\frac{dr}{dt}"),
             r"$\dfrac{dA}{dt} = 2\pi r\,\dfrac{dr}{dt}$, by the chain rule on $r^2$.", [(1, "$\\frac{dA}{dt} = 2\\pi r\\frac{dr}{dt}$")], work="1.6cm"),
    ], frq_type="Related rates"),
]
same("frq a", d(sp.pi * r**2 * h), 2 * sp.pi * r * h * d(r) + sp.pi * r**2 * d(h))

TOPIC = Topic(
    number="4.4", title="Introduction to Related Rates",
    unit="Unit 4: Contextual Applications of Differentiation", ced=["CHA-3.D", "CHA-3.D.1"],
    goals=r"Write the equation for a related rates problem: draw and label, name the changing quantities, relate them, and "
          r"differentiate the equation with respect to time.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
