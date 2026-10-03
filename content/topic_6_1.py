"""Topic 6.1: Exploring accumulations of change.

CED: CHA-4.A (CHA-4.A.1, CHA-4.A.2): the area of the region between the graph of a rate of change and the t-axis gives
the accumulated (net) change of the quantity over an interval, in (rate units) x (time units); area below the axis
counts as negative change. Built from constant rates (rectangles) and linear rates (triangles, trapezoids).
Worked examples: what the area under a sales-rate graph means, net change vs total distance for v(t) = 4 - 2t, a
draining tank.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, num, same,
                     selfcheck)
from calclib.figs import graph

t = sp.symbols("t", real=True)


def area(pieces):
    """Signed area under a piecewise rate given as [(expr in t, a, b), ...]."""
    return sum(sp.integrate(e, (t, a, b)) for e, a, b in pieces)


def total(pieces):
    """Total (unsigned) area: integrate |rate|."""
    return sum(sp.integrate(sp.Abs(e), (t, a, b)) for e, a, b in pieces)


RAIN = [(t / 5, 0, 2), (sp.Rational(2, 5), 2, 6), (sp.Rational(2, 5) - (t - 6) / 5, 6, 8)]
same("lesson", [area(RAIN)], [sp.Rational(12, 5)])
same("ex2", [area([(4 - 2 * t, 0, 4)]), total([(4 - 2 * t, 0, 4)])], [0, 8])
same("ex3", [60 - area([(10 - 2 * t, 0, 5)])], [35])

FIG_V = graph("t6_1_v", [("2+0*x", 0, 3), ("-1+0*x", 3, 7)], xr=(0, 8), yr=(-2, 3), xlabel="t", ylabel="v(t)",
              caption="Velocity of a walker, in meters per second.")
P1 = [(3 * t / 2, 0, 2), (3 + 0 * t, 2, 5), (3 - 3 * (t - 5) / 2, 5, 7)]
FIG_P1 = graph("t6_1_p1", [("1.5*x", 0, 2), ("3+0*x", 2, 5), ("3-1.5*(x-5)", 5, 7)], xr=(0, 8), yr=(0, 4), xlabel="t", ylabel="R(t)",
               caption="$R(t)$, the rate at which a pump moves water, in gallons per minute.")
P2 = [(2 - t, 0, 4), (-2 + 0 * t, 4, 6)]
FIG_P2 = graph("t6_1_p2", [("2-x", 0, 4), ("-2+0*x", 4, 6)], xr=(0, 6), yr=(-3, 3), xlabel="t", ylabel="v(t)",
               caption="$v(t)$, the velocity of a particle, in feet per second.")
same("p figs", [area(P1), area(P2), total(P2)], [15, -4, 8])

NOTES = [
    Video("s6_1.py::Lesson", "Area under a rate", 5),

    Section("Area means amount"),
    Text(r"Water flows into a tank at $3$ gallons per minute for $4$ minutes: $(3\ \text{gal/min})(4\ \text{min}) = 12$ gallons. On the graph of "
         r"the rate, $12$ is the \blank{area} of the rectangle under it. The minutes cancel, so the area is measured in gallons."),
    Formula("Accumulated change", (
        r"The area of the region between the graph of a \blank{rate of change} and the $t$-axis, from $t = a$ to $t = b$, is the "
        r"\blank{net change} in the quantity over that interval. \par "
        r"Units: (units of the rate) $\times$ (units of $t$). \par "
        r"Area \blank{below} the axis counts as negative change.")),
    Text(r"When the rate isn't constant, the area still gives the amount. For a linear rate the region is a triangle or a trapezoid: "
         r"$r(t) = 2 + t$ on $[0, 4]$ gives $\frac{2 + 6}{2} \cdot 4 = 16$ gallons."),

    Section("Net change and total distance"),
    Text(r"For a velocity graph, the signed area is the \blank{displacement} (net change in position). Area above the axis is motion forward, "
         r"area below is motion back. The \blank{total distance} adds all the areas as positive numbers."),
    FIG_V,
    Text(r"Here the walker goes $6$ m forward, then $4$ m back: displacement $6 - 4 = 2$ m, total distance $6 + 4 = 10$ m."),
    VideoExample('Reading the area', work="3cm"),
    BigIdea(r"The area under the graph of a rate of change is the amount of change, in (rate units) $\times$ (time units). Area above the axis adds; area below subtracts."),
    Check(r"A car's speed is a constant $55$ miles per hour for $2.5$ hours. How far does it travel?", num(sp.Rational(275, 2)),
          r"The area of the rectangle: $(55)(2.5) = 137.5$ miles."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Water flows into a pool at a constant $12$ gallons per minute. How many gallons flow in from $t = 0$ to $t = 15$ minutes?", num(180),
         r"The area of the rectangle: $(12)(15) = 180$ gallons.", work="1.2cm"),
    Item(r"A rate $r(t) = 3t$ liters per hour. How many liters accumulate from $t = 0$ to $t = 4$?", num(24),
         r"A triangle with base $4$ and height $r(4) = 12$: $\frac12(4)(12) = 24$ liters.", work="1.4cm"),
    Item(r"A rate $r(t) = 5 + 2t$ cubic feet per second. Find the amount that accumulates from $t = 1$ to $t = 3$.", num(18),
         r"A trapezoid with heights $r(1) = 7$ and $r(3) = 11$, width $2$: $\frac{7 + 11}{2} \cdot 2 = 18$ cubic feet.", work="1.6cm"),
    Item(r"The graph of $R(t)$ is shown. How many gallons does the pump move from $t = 0$ to $t = 7$ minutes?", num(15),
         r"Triangle $\frac12(2)(3) = 3$, rectangle $(3)(3) = 9$, triangle $\frac12(2)(3) = 3$: $3 + 9 + 3 = 15$ gallons.", work="2cm", figure=FIG_P1),
    Item(r"Using the same graph of $R$, how many gallons does the pump move from $t = 1$ to $t = 3$?", num(sp.Rational(21, 4)),
         r"From $1$ to $2$: a trapezoid with heights $1.5$ and $3$, $\frac{1.5 + 3}{2}(1) = 2.25$. From $2$ to $3$: $3$. Total $5.25$ gallons.", work="2cm"),
    Item(r"The graph of $v(t)$ is shown. Find the displacement of the particle from $t = 0$ to $t = 6$.", num(-4),
         r"Above the axis: $\frac12(2)(2) = 2$. Below: $\frac12(2)(2) + (2)(2) = 6$. Displacement $2 - 6 = -4$ feet.", work="2cm", figure=FIG_P2),
    Item(r"Using the same graph of $v$, find the total distance the particle travels from $t = 0$ to $t = 6$.", num(8),
         r"Add the areas as positive numbers: $2 + 6 = 8$ feet.", work="1.4cm"),
    Item(r"$P(t)$ is the rate, in people per hour, at which people enter a museum, $t$ hours after it opens. What does the area under the graph of $P$ "
         r"from $t = 2$ to $t = 5$ represent? Give its units.", selfcheck(r"\text{the number of people who entered from } t = 2 \text{ to } t = 5"),
         r"(people per hour)(hours) = people: the number of people who entered between $2$ and $5$ hours after opening.", work="1.6cm"),
    Item(r"A rate graph has its vertical axis in kilojoules per second and its horizontal axis in seconds. What are the units of the area under it?",
         selfcheck(r"\text{kilojoules}"), r"(kilojoules per second)(seconds) = kilojoules.", work="1cm"),
    Item(r"Snow falls at $0.5$ inches per hour for $3$ hours, then $1$ inch per hour for $2$ hours. How many inches fall in all?", num(sp.Rational(7, 2)),
         r"Two rectangles: $(0.5)(3) + (1)(2) = 3.5$ inches.", work="1.4cm"),
    Item(r"Water leaks from a tank at $r(t) = 8 - 2t$ liters per minute for $0 \le t \le 4$. The tank held $40$ liters at $t = 0$. How much is left at $t = 4$?", num(24),
         r"The amount leaked is the triangle $\frac12(4)(8) = 16$ liters, so $40 - 16 = 24$ liters remain.", work="1.8cm"),
    Item(r"A velocity is $v(t) = t - 3$ meters per second for $0 \le t \le 6$. Find the displacement and the total distance traveled.",
         selfcheck(r"\text{displacement } 0 \text{ m, distance } 9 \text{ m}"),
         r"Below the axis on $(0, 3)$: area $4.5$. Above on $(3, 6)$: area $4.5$. Displacement $4.5 - 4.5 = 0$; total distance $4.5 + 4.5 = 9$ m.", work="1.8cm"),
]
same("p", [area([(t - 3, 0, 6)]), total([(t - 3, 0, 6)]), area([(3 * t / 2, 1, 2), (3 + 0 * t, 2, 3)]), 40 - area([(8 - 2 * t, 0, 4)])], [0, 9, sp.Rational(21, 4), 24])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"A rate is a constant $8$ gallons per minute. How many gallons accumulate in $6$ minutes?", num(48), r"$(8)(6) = 48$.", work="1cm"),
        Item(r"A rate is a constant $15$ meters per second. How many meters accumulate in $4$ seconds?", num(60), r"$(15)(4) = 60$.", work="1cm"),
        Item(r"A rate is a constant $2.5$ liters per hour. How many liters accumulate in $10$ hours?", num(25), r"$(2.5)(10) = 25$.", work="1cm"),
    ),
    Variants(
        Item(r"$r(t) = 4t$ gallons per minute. How many gallons accumulate from $t = 0$ to $t = 3$?", num(18), r"Triangle: $\frac12(3)(12) = 18$.", work="1.2cm"),
        Item(r"$r(t) = 2 + 2t$ gallons per minute. How many gallons accumulate from $t = 0$ to $t = 2$?", num(8), r"Trapezoid: $\frac{2 + 6}{2}(2) = 8$.", work="1.2cm"),
        Item(r"$r(t) = 10 - t$ gallons per minute. How many gallons accumulate from $t = 0$ to $t = 4$?", num(32), r"Trapezoid: $\frac{10 + 6}{2}(4) = 32$.", work="1.2cm"),
    ),
    Variants(
        MCQ(r"$W(t)$ is the rate, in words per minute, at which Lena types. The area under the graph of $W$ from $t = 0$ to $t = 10$ is", [
            r"her average typing speed", r"the number of words she types in the first $10$ minutes", r"her typing speed at $t = 10$", r"the change in her typing speed"], "B",
            r"(words per minute)(minutes) = words."),
        MCQ(r"$C(t)$ is the rate, in dollars per day, at which a company spends money. The area under the graph of $C$ from $t = 5$ to $t = 12$ is", [
            r"the amount spent from day $5$ to day $12$", r"the spending rate on day $12$", r"the average spending rate", r"the change in the spending rate"], "A",
            r"(dollars per day)(days) = dollars."),
        MCQ(r"$v(t)$ is a car's velocity in miles per hour, and $v(t) > 0$. The area under the graph of $v$ from $t = 0$ to $t = 2$ is", [
            r"the car's speed at $t = 2$", r"the car's acceleration", r"the distance the car travels in the first $2$ hours", r"the car's average speed"], "C",
            r"(miles per hour)(hours) = miles."),
    ),
    Variants(
        Item(r"A velocity graph has area $10$ above the axis and area $4$ below it on $[0, 8]$. What is the displacement?", num(6), r"$10 - 4 = 6$.", work="1cm"),
        Item(r"A velocity graph has area $3$ above the axis and area $7$ below it on $[0, 5]$. What is the displacement?", num(-4), r"$3 - 7 = -4$.", work="1cm"),
        Item(r"A velocity graph has area $5$ above the axis and area $5$ below it on $[0, 6]$. What is the total distance traveled?", num(10), r"$5 + 5 = 10$.", work="1cm"),
    ),
    Variants(
        Item(r"Water drains from a tank at $r(t) = 6 - 2t$ liters per minute for $0 \le t \le 3$. The tank held $20$ liters. How much is left at $t = 3$?", num(11),
             r"Drained: $\frac12(3)(6) = 9$. Left: $20 - 9 = 11$.", work="1.4cm"),
        Item(r"Sand pours onto a pile at $r(t) = 2t$ cubic feet per hour for $0 \le t \le 5$. The pile had $10$ cubic feet. How much is there at $t = 5$?", num(35),
             r"Added: $\frac12(5)(10) = 25$. Total: $10 + 25 = 35$.", work="1.4cm"),
        Item(r"An account gains money at $r(t) = 100 - 20t$ dollars per year for $0 \le t \le 5$. It started with $500$ dollars. How much is there at $t = 5$?", num(750),
             r"Added: $\frac12(5)(100) = 250$. Total: $500 + 250 = 750$.", work="1.4cm"),
    ),
]
same("q5", [20 - area([(6 - 2 * t, 0, 3)]), 10 + area([(2 * t, 0, 5)]), 500 + area([(100 - 20 * t, 0, 5)])], [11, 35, 750])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"A pipe fills a tank at $r(t) = 3 + t$ gallons per minute. How much water enters from $t = 0$ to $t = 4$?", [r"$7$ gallons", r"$12$ gallons",
        r"$20$ gallons", r"$28$ gallons"], "C", r"A trapezoid with heights $3$ and $7$, width $4$: $\frac{3 + 7}{2}(4) = 20$.",
        why_not={"A": "that's the rate at $t = 4$", "D": "that's $r(4) \\cdot 4$, a rectangle at the tallest height"}),
    MCQ(r"A particle's velocity is $v(t) = 2t - 6$ ft/s for $0 \le t \le 5$. Its displacement over that interval is", [r"$-5$ ft", r"$13$ ft", r"$4$ ft", r"$-9$ ft"], "A",
        r"Below the axis on $(0, 3)$: area $9$. Above on $(3, 5)$: area $4$. Displacement $4 - 9 = -5$.", why_not={"B": "that's the total distance"}),
    MCQ(r"$H(t)$ is the rate, in degrees Fahrenheit per hour, at which the temperature of a room changes. The area between the graph of $H$ and the $t$-axis "
        r"from $t = 1$ to $t = 4$, counting area below the axis as negative, is", [r"the temperature at $t = 4$", r"the rate of change at $t = 4$",
        r"the average temperature", r"the change in temperature from $t = 1$ to $t = 4$"], "D", r"(degrees per hour)(hours) = degrees of change."),
    MCQ(r"A rate graph is a horizontal line at height $-3$ (liters per minute) from $t = 0$ to $t = 6$. Over that interval, the amount of liquid", [
        r"increases by $18$ liters", r"decreases by $18$ liters", r"decreases by $3$ liters", r"does not change"], "B", r"Area below the axis: $-(3)(6) = -18$."),
]
same("m", [area([(3 + t, 0, 4)]), area([(2 * t - 6, 0, 5)]), total([(2 * t - 6, 0, 5)])], [20, -5, 13])

FIG_FRQ = graph("t6_1_frq", [("2*x", 0, 2), ("4+0*x", 2, 6), ("4-2*(x-6)", 6, 10), ("-4+0*x", 10, 12)], xr=(0, 12), yr=(-5, 5), xlabel="t", ylabel="v(t)",
                caption="The velocity $v(t)$ of a cyclist, in meters per second.")
VC = [(2 * t, 0, 2), (4 + 0 * t, 2, 6), (4 - 2 * (t - 6), 6, 10), (-4 + 0 * t, 10, 12)]
same("frq", [area(VC), total(VC), area(VC[:2]) + area([(4 - 2 * (t - 6), 6, 8)])], [12, 36, 24])
FRQS = [
    FRQ("A cyclist", (
        r"A cyclist rides along a straight path. Her velocity $v(t)$, in meters per second, for $0 \le t \le 12$ seconds is given by the piecewise-linear "
        r"graph shown. Positive velocity means she is moving away from her starting point."), [
        Part("a", r"Find the cyclist's displacement from $t = 0$ to $t = 12$. Show the work that leads to your answer. Indicate units of measure.",
             num(12, display=r"12\ \text{meters}"),
             r"Areas above the axis: $\frac12(2)(4) + (4)(4) + \frac12(2)(4) = 4 + 16 + 4 = 24$. Below: $\frac12(2)(4) + (2)(4) = 4 + 8 = 12$. "
             r"Displacement $24 - 12 = 12$ meters.", [(1, "areas above and below the axis"), (1, "answer with units")], work="3cm"),
        Part("b", r"Find the total distance the cyclist travels from $t = 0$ to $t = 12$.", num(36, display=r"36\ \text{meters}"),
             r"Total distance adds the areas: $24 + 12 = 36$ meters.", [(1, "answer")], work="1.6cm"),
        Part("c", r"At what time $t$, for $0 \le t \le 12$, is the cyclist farthest from her starting point in the positive direction? Give a reason for your answer.",
             num(8), r"$v(t) > 0$ for $0 < t < 8$ and $v(t) < 0$ for $8 < t < 12$, so she moves forward until $t = 8$ and then back. "
             r"At $t = 8$ she is $24$ meters from the start, and at $t = 12$ only $12$. She is farthest at $t = 8$.",
             [(1, "$t = 8$"), (1, "reason: $v$ changes from positive to negative at $t = 8$")], work="2.6cm"),
    ], frq_type="Particle motion", figure=FIG_FRQ),
]

TOPIC = Topic(
    number="6.1", title="Exploring Accumulations of Change",
    unit="Unit 6: Integration and Accumulation of Change", ced=["CHA-4.A", "CHA-4.A.1", "CHA-4.A.2"],
    goals=r"Use the area under the graph of a rate of change to find the accumulated change, with units, counting area below the axis as negative.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
