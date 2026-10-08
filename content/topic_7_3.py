"""Topic 7.3: Sketching slope fields.

CED: FUN-7.C (FUN-7.C.1, FUN-7.C.2): a slope field shows, at each point, a short segment with slope given by the
differential equation; solution curves follow the segments. Patterns: depends only on x (same slope in each column),
only on y (same slope in each row), flat where the right side is zero. Lesson example: nine segments for dy/dx = x - y.
Worked examples: dy/dx = y/2 by rows, matching a field to -x/y. Slope-field sketches appear as FRQ parts in 7.7 and later.
"""
import sympy as sp

from calclib import (VideoExample, MCQ, BigIdea, Check, Formula, Item, Section, Text, Topic, Variants, Video, num, same, selfcheck)
from calclib.figs import slope_field

x, y = sp.symbols("x y")
same("lesson", [[(a - c) for a in (-1, 0, 1) for c in (-1, 0, 1)], [sp.Rational(c, 2) for c in (-2, 0, 2)]], [[0, -1, -2, 1, 0, -1, 2, 1, 0], [-1, 0, 1]])

G = [-1.5, -1, -0.5, 0, 0.5, 1, 1.5]
FIG_XMY = slope_field("t7_3_xmy", lambda a, c: a - c, G, G, (-2, 2), (-2, 2), caption=r"The slope field for $\frac{dy}{dx} = x - y$.")
FIG_X = slope_field("t7_3_x", lambda a, c: a, G, G, (-2, 2), (-2, 2), caption="Slope field A.")
FIG_Y = slope_field("t7_3_y", lambda a, c: c, G, G, (-2, 2), (-2, 2), caption="Slope field B.")
FIG_XY = slope_field("t7_3_xy", lambda a, c: a * c, G, G, (-2, 2), (-2, 2), caption="Slope field C.")

NOTES = [
    Video("s7_3.py::Lesson", "Slope fields", 4),

    Section("Slope fields"),
    Text(r"A \blank{slope field} draws, at each point $(x, y)$, a short segment whose slope is the value of $\frac{dy}{dx}$ there. Every solution curve follows the segments."),
    FIG_XMY,
    Formula("Patterns", (
        r"If $\frac{dy}{dx}$ depends only on $x$, the slopes are equal down each vertical \blank{column}. \par "
        r"If it depends only on $y$, the slopes are equal along each horizontal \blank{row}. \par "
        r"Where the right side is $0$, the segments are \blank{flat}.")),
    VideoExample('Sketching nine segments', work="3.2cm"),
    BigIdea(r"A slope field shows the slope from the differential equation at each point; solution curves follow the segments."),
    Check(r"For $\frac{dy}{dx} = 2x - y$, what slope is drawn at $(1, 3)$?", num(-1), r"$2(1) - 3 = -1$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [Item(rf"For $\dfrac{{dy}}{{dx}} = {sp.latex(e)}$, find the slope of the segment at $({a}, {b})$.", num(e.subs({x: a, y: b})), rf"${sp.latex(e)}$ at $({a}, {b})$: ${e.subs({x: a, y: b})}$.", work="1cm")
            for e, a, b in ((x + y, 2, -1), (x * y, -1, 3), (y**2 - x, 1, 2), (x / y, 4, 2), (2 * y - x**2, 2, 1))]
PRACTICE += [
    Item(r"For $\frac{dy}{dx} = y - 1$, where are the segments flat?", selfcheck(r"\text{along the line } y = 1"), r"$y - 1 = 0$ on the horizontal line $y = 1$.", work="1cm"),
    Item(r"For $\frac{dy}{dx} = x + 2$, describe the slopes in the column $x = 1$.", selfcheck(r"\text{all equal to } 3"), r"The slope depends only on $x$: every segment at $x = 1$ has slope $3$.", work="1cm"),
    Item(r"Slope field B is shown. Does it belong to $\frac{dy}{dx} = y$ or to $\frac{dy}{dx} = x$?", selfcheck(r"\frac{dy}{dx} = y"), r"Slopes equal along rows, flat along $y = 0$, positive above and negative below.", work="1cm", figure=FIG_Y),
    Item(r"Slope field A is shown. Does it belong to $\frac{dy}{dx} = x$ or to $\frac{dy}{dx} = xy$?", selfcheck(r"\frac{dy}{dx} = x"), r"Slopes are equal down each column, and nonzero on the $x$-axis away from $0$.", work="1cm", figure=FIG_X),
    Item(r"Slope field C is shown. Where are its segments flat?", selfcheck(r"\text{on both axes}"), r"$xy = 0$ when $x = 0$ or $y = 0$.", work="1cm", figure=FIG_XY),
]

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(*[Item(rf"For $\dfrac{{dy}}{{dx}} = {sp.latex(e)}$, find the slope at $({a}, {b})$.", num(e.subs({x: a, y: b})), rf"${e.subs({x: a, y: b})}$.", work="1cm")
               for e, a, b in ((x - 2 * y, 3, 1), (x**2 + y, -2, -1), (y / (x + 1), 1, 6))]),
    Variants(
        MCQ(r"For which equation are the slopes the same along every horizontal row?", [r"$\frac{dy}{dx} = x^2$", r"$\frac{dy}{dx} = y^2 - 1$", r"$\frac{dy}{dx} = x + y$", r"$\frac{dy}{dx} = xy$"], "B", r"Depends only on $y$."),
        MCQ(r"For which equation are the slopes the same down every vertical column?", [r"$\frac{dy}{dx} = \sin x$", r"$\frac{dy}{dx} = y$", r"$\frac{dy}{dx} = x - y$", r"$\frac{dy}{dx} = \frac yx$"], "A", r"Depends only on $x$."),
        MCQ(r"For which equation are the segments flat along the line $y = 2x$?", [r"$\frac{dy}{dx} = x - 2y$", r"$\frac{dy}{dx} = y + 2x$", r"$\frac{dy}{dx} = y - 2x$", r"$\frac{dy}{dx} = 2xy$"], "C", r"$y - 2x = 0$ on $y = 2x$."),
    ),
    Variants(
        MCQ(r"Which equation matches slope field C (shown)?", [r"$\frac{dy}{dx} = x + y$", r"$\frac{dy}{dx} = x$", r"$\frac{dy}{dx} = y$", r"$\frac{dy}{dx} = xy$"], "D", r"Flat on both axes; positive in quadrants I and III.", figure=FIG_XY),
    ),
    Variants(
        Item(r"For $\frac{dy}{dx} = x - y$, how many of the nine points with $x, y \in \{-1, 0, 1\}$ have flat segments?", num(3), r"Where $x = y$: $(-1, -1)$, $(0, 0)$, $(1, 1)$.", work="1cm"),
        Item(r"For $\frac{dy}{dx} = x + y$, how many of the nine points with $x, y \in \{-1, 0, 1\}$ have flat segments?", num(3), r"Where $x = -y$: $(-1, 1)$, $(0, 0)$, $(1, -1)$.", work="1cm"),
        Item(r"For $\frac{dy}{dx} = xy$, how many of the nine points with $x, y \in \{-1, 0, 1\}$ have flat segments?", num(5), r"Where $x = 0$ or $y = 0$: five points.", work="1cm"),
    ),
    Variants(
        Item(r"For $\frac{dy}{dx} = x^2 - y^2$, is the segment at $(1, 2)$ rising or falling?", selfcheck(r"\text{falling}"), r"$1 - 4 = -3 < 0$.", work="1cm"),
        Item(r"For $\frac{dy}{dx} = x^2 - y^2$, is the segment at $(3, 1)$ rising or falling?", selfcheck(r"\text{rising}"), r"$9 - 1 = 8 > 0$.", work="1cm"),
        Item(r"For $\frac{dy}{dx} = x^2 - y^2$, is the segment at $(2, -2)$ rising, falling, or flat?", selfcheck(r"\text{flat}"), r"$4 - 4 = 0$.", work="1cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"The slope field for which equation has segments with slope $1$ at every point of the line $y = x$?", [r"$\frac{dy}{dx} = x - y$", r"$\frac{dy}{dx} = \frac yx$", r"$\frac{dy}{dx} = x + y$", r"$\frac{dy}{dx} = xy$"], "B",
        r"$\frac yx = 1$ when $y = x$ ($x \ne 0$)."),
    MCQ(r"Slope field B (shown) belongs to", [r"$\frac{dy}{dx} = x$", r"$\frac{dy}{dx} = -y$", r"$\frac{dy}{dx} = y$", r"$\frac{dy}{dx} = x + y$"], "C", r"Equal along rows, positive above the $x$-axis.", figure=FIG_Y),
    MCQ(r"For $\frac{dy}{dx} = (x - 1)(y + 2)$, the segments are flat along", [r"$x = 1$ and $y = -2$", r"$x = -1$ and $y = 2$", r"$y = x - 1$", r"the $x$-axis only"], "A", r"The right side is $0$ when $x = 1$ or $y = -2$."),
    MCQ(r"At which point does the slope field for $\frac{dy}{dx} = 3 - xy$ have slope $-1$?", [r"$(1, 1)$", r"$(-2, 2)$", r"$(0, 4)$", r"$(2, 2)$"], "D", r"$3 - 4 = -1$."),
]
same("m", [(3 - x * y).subs({x: 2, y: 2})], [-1])

FRQS = []

TOPIC = Topic(
    number="7.3", title="Sketching Slope Fields",
    unit="Unit 7: Differential Equations", ced=["FUN-7.C", "FUN-7.C.1", "FUN-7.C.2"],
    goals=r"Sketch a slope field for a differential equation at given points, using patterns in where the slopes are equal or zero.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
