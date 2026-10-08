"""Topic 0.1: Angles and radian measure (trig review; not a CED topic).

Prerequisite for every trig topic in the course: angles in standard position, radians (one radius of arc), converting
with 180 degrees = pi, the landmark angles, coterminal angles, arc length s = r theta and sector area A = r^2 theta / 2.
Lesson example: 150 degrees to radians. Worked examples: 5pi/4 to degrees, coterminal with 17pi/6, a pendulum's arc,
a pizza slice.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)
from calclib.figs import unit_circle

pi = sp.pi
same("lesson", [150 * pi / 180], [5 * pi / 6])
same("ex1-2", [sp.Rational(5, 4) * 180, sp.Rational(17, 6) * pi - 2 * pi], [225, 5 * pi / 6])
close("ex3", float(80 * pi / 6), 41.89, 0.01)
close("ex4", float(sp.Rational(1, 2) * 64 * pi / 4), 25.13, 0.01)

FIG_LAND = unit_circle("t0_1_land", [(k * float(pi) / 6, l) for k, l in ((0, "$0$"), (1, r"$\frac{\pi}{6}$"), (3, r"$\frac{\pi}{2}$"), (5, r"$\frac{5\pi}{6}$"),
                                                                        (6, r"$\pi$"), (9, r"$\frac{3\pi}{2}$"))] +
                       [(float(pi) / 4, r"$\frac{\pi}{4}$"), (float(pi) / 3, r"$\frac{\pi}{3}$")],
                       caption="Landmark angles. Count in sixths, fourths, or thirds of $\\pi$.", labels=False)

NOTES = [
    Video("s0_1.py::Lesson", "Angles and radian measure", 6),

    Section("Angles in standard position"),
    Text(r"An angle in \textbf{standard position} starts on the positive $x$-axis (the \textbf{initial side}) and turns to the \textbf{terminal side}. "
         r"Counterclockwise turns are positive; clockwise turns are negative."),

    Section("Radians"),
    Text(r"Lay one radius of a circle along the circle: the angle it cuts off is \textbf{one radian}, about $57.3^\circ$. The circumference is $2\pi r$, "
         r"so $2\pi$ radius lengths fit around."),
    Formula("Radian facts", (r"A full turn is \[ 360^\circ = \blank{2\pi} \text{ radians}, \qquad \text{so} \qquad 180^\circ = \blank{\pi} \text{ radians}. \]"
                             r"Degrees to radians: multiply by $\frac{\pi}{180^\circ}$. Radians to degrees: multiply by $\frac{180^\circ}{\pi}$.")),
    VideoExample("Converting 150 degrees", work="2.4cm"),
    Text(r"\textbf{Landmark angles.} $30^\circ = \frac{\pi}{6}$, $45^\circ = \frac{\pi}{4}$, $60^\circ = \frac{\pi}{3}$, $90^\circ = \frac{\pi}{2}$, $180^\circ = \pi$, "
         r"$270^\circ = \frac{3\pi}{2}$. The rest are multiples: $\frac{5\pi}{6}$ is five $30^\circ$ steps, $150^\circ$."),
    FIG_LAND,

    Section("Coterminal angles"),
    Text(r"Angles with the same terminal side are \textbf{coterminal}. Adding or subtracting $2\pi$ (any number of times) gives a coterminal angle: "
         r"$\frac{\pi}{3}$, $\frac{7\pi}{3}$ and $-\frac{5\pi}{3}$ all point the same way."),

    Section("Arc length and sector area"),
    Formula("Arc length and sector area", (r"On a circle of radius $r$, an angle of $\theta$ radians cuts off \[ \text{arc length } s = \blank{r\theta} "
                                           r"\qquad \text{and a sector of area } A = \blank{\tfrac12 r^2\theta}. \] Both need $\theta$ in radians.")),
    BigIdea(r"Half a turn is $\pi$ radians. Radians measure an angle by the arc it cuts off on a circle of radius $1$, which is why calculus uses them."),
    Check(r"Convert $240^\circ$ to radians.", selfcheck(r"\frac{4\pi}{3}"), r"$240 \cdot \frac{\pi}{180} = \frac{4\pi}{3}$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Convert $45^\circ$ to radians.", num(pi / 4, display=r"\frac{\pi}{4}"), r"$45 \cdot \frac{\pi}{180} = \frac{\pi}{4}$.", work="1cm"),
    Item(r"Convert $300^\circ$ to radians.", num(5 * pi / 3, display=r"\frac{5\pi}{3}"), r"$300 \cdot \frac{\pi}{180} = \frac{5\pi}{3}$.", work="1cm"),
    Item(r"Convert $-135^\circ$ to radians.", num(-3 * pi / 4, display=r"-\frac{3\pi}{4}"), r"$-135 \cdot \frac{\pi}{180} = -\frac{3\pi}{4}$.", work="1cm"),
    Item(r"Convert $\frac{2\pi}{3}$ to degrees.", num(120, display=r"120^\circ"), r"$\frac{2\pi}{3} \cdot \frac{180}{\pi} = 120^\circ$.", work="1cm"),
    Item(r"Convert $\frac{7\pi}{6}$ to degrees.", num(210, display=r"210^\circ"), r"$\frac{7 \cdot 180}{6} = 210^\circ$.", work="1cm"),
    Item(r"Convert $2$ radians to degrees, to the nearest tenth.", num(360 / pi, tol=0.05), r"$2 \cdot \frac{180}{\pi} \approx 114.6^\circ$.", work="1cm", calc=True),
    Item(r"Find the angle between $0$ and $2\pi$ coterminal with $\frac{11\pi}{4}$.", num(3 * pi / 4, display=r"\frac{3\pi}{4}"), r"$\frac{11\pi}{4} - \frac{8\pi}{4} = \frac{3\pi}{4}$.", work="1.2cm"),
    Item(r"Find the angle between $0$ and $2\pi$ coterminal with $-\frac{\pi}{6}$.", num(11 * pi / 6, display=r"\frac{11\pi}{6}"), r"$-\frac{\pi}{6} + \frac{12\pi}{6} = \frac{11\pi}{6}$.", work="1.2cm"),
    MCQ(r"In which quadrant is the terminal side of $\frac{5\pi}{3}$?", ["I", "II", "III", "IV"], "D", r"$\frac{5\pi}{3} = 300^\circ$, between $270^\circ$ and $360^\circ$.",
        {"C": r"$\frac{5\pi}{3}$ is past $\frac{3\pi}{2}$"}),
    Item(r"A circle has radius $6$ cm. Find the length of the arc cut off by an angle of $\frac{\pi}{3}$.", num(2 * pi, display=r"2\pi \text{ cm}"), r"$s = r\theta = 6 \cdot \frac{\pi}{3} = 2\pi$ cm.", work="1.2cm"),
    Item(r"A sector of a circle of radius $10$ has area $25\pi$. Find its angle in radians.", num(pi / 2, display=r"\frac{\pi}{2}"),
         r"$\frac12 \cdot 100 \cdot \theta = 25\pi$, so $\theta = \frac{\pi}{2}$.", work="1.4cm"),
    Item(r"A wheel of radius $35$ cm rolls without slipping through $3$ full turns. How far does it roll, to the nearest centimeter?", num(210 * pi, tol=0.5),
         r"$\theta = 6\pi$, $s = 35 \cdot 6\pi = 210\pi \approx 660$ cm.", work="1.4cm", calc=True),
]
same("p", [300 * pi / 180, -135 * pi / 180, sp.Rational(7, 6) * 180, sp.Rational(11, 4) * pi - 2 * pi], [5 * pi / 3, -3 * pi / 4, 210, 3 * pi / 4])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Convert $210^\circ$ to radians.", num(7 * pi / 6, display=r"\frac{7\pi}{6}"), r"$210 \cdot \frac{\pi}{180} = \frac{7\pi}{6}$.", work="1cm"),
        Item(r"Convert $135^\circ$ to radians.", num(3 * pi / 4, display=r"\frac{3\pi}{4}"), r"$135 \cdot \frac{\pi}{180} = \frac{3\pi}{4}$.", work="1cm"),
        Item(r"Convert $330^\circ$ to radians.", num(11 * pi / 6, display=r"\frac{11\pi}{6}"), r"$330 \cdot \frac{\pi}{180} = \frac{11\pi}{6}$.", work="1cm"),
    ),
    Variants(
        Item(r"Convert $\frac{3\pi}{2}$ to degrees.", num(270, display=r"270^\circ"), r"$\frac{3 \cdot 180}{2} = 270^\circ$.", work="1cm"),
        Item(r"Convert $\frac{5\pi}{6}$ to degrees.", num(150, display=r"150^\circ"), r"$\frac{5 \cdot 180}{6} = 150^\circ$.", work="1cm"),
        Item(r"Convert $\frac{7\pi}{4}$ to degrees.", num(315, display=r"315^\circ"), r"$\frac{7 \cdot 180}{4} = 315^\circ$.", work="1cm"),
    ),
    Variants(
        Item(r"Find the angle between $0$ and $2\pi$ coterminal with $\frac{13\pi}{6}$.", num(pi / 6, display=r"\frac{\pi}{6}"), r"Subtract $2\pi = \frac{12\pi}{6}$.", work="1cm"),
        Item(r"Find the angle between $0$ and $2\pi$ coterminal with $-\frac{3\pi}{4}$.", num(5 * pi / 4, display=r"\frac{5\pi}{4}"), r"Add $2\pi = \frac{8\pi}{4}$.", work="1cm"),
        Item(r"Find the angle between $0$ and $2\pi$ coterminal with $\frac{10\pi}{3}$.", num(4 * pi / 3, display=r"\frac{4\pi}{3}"), r"Subtract $2\pi = \frac{6\pi}{3}$.", work="1cm"),
    ),
    Variants(
        Item(r"Find the arc length cut off by an angle of $\frac{3\pi}{4}$ on a circle of radius $8$.", num(6 * pi, display=r"6\pi"), r"$s = 8 \cdot \frac{3\pi}{4} = 6\pi$.", work="1cm"),
        Item(r"Find the arc length cut off by an angle of $\frac{\pi}{5}$ on a circle of radius $15$.", num(3 * pi, display=r"3\pi"), r"$s = 15 \cdot \frac{\pi}{5} = 3\pi$.", work="1cm"),
    ),
    Variants(
        Item(r"Find the area of a sector with radius $6$ and angle $\frac{\pi}{3}$.", num(6 * pi, display=r"6\pi"), r"$A = \frac12 \cdot 36 \cdot \frac{\pi}{3} = 6\pi$.", work="1cm"),
        Item(r"Find the area of a sector with radius $4$ and angle $\frac{3\pi}{2}$.", num(12 * pi, display=r"12\pi"), r"$A = \frac12 \cdot 16 \cdot \frac{3\pi}{2} = 12\pi$.", work="1cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"Which angle is coterminal with $\frac{\pi}{4}$?", [r"$-\frac{\pi}{4}$", r"$\frac{5\pi}{4}$", r"$\frac{9\pi}{4}$", r"$\frac{3\pi}{4}$"], "C",
        r"$\frac{\pi}{4} + 2\pi = \frac{9\pi}{4}$.", {"B": r"$\frac{\pi}{4} + \pi$ points the opposite way", "A": "that is its reflection across the $x$-axis"}),
    MCQ(r"An angle of $1$ radian is closest to", [r"$1^\circ$", r"$57^\circ$", r"$90^\circ$", r"$180^\circ$"], "B", r"$\frac{180^\circ}{\pi} \approx 57.3^\circ$.",
        {"D": r"that is $\pi$ radians"}),
    MCQ(r"A sprinkler sprays water over a sector of radius $20$ feet and angle $120^\circ$. What area does it water?",
        [r"$\frac{400\pi}{3}$ ft$^2$", r"$\frac{40\pi}{3}$ ft$^2$", r"$2400$ ft$^2$", r"$800\pi$ ft$^2$"], "A",
        r"$120^\circ = \frac{2\pi}{3}$, $A = \frac12 \cdot 400 \cdot \frac{2\pi}{3} = \frac{400\pi}{3}$.", {"B": "that is the arc length", "C": "the angle must be in radians"}),
    MCQ(r"The minute hand of a clock is $9$ cm long. How far does its tip travel in $20$ minutes?",
        [r"$3\pi$ cm", r"$9\pi$ cm", r"$27\pi$ cm", r"$6\pi$ cm"], "D", r"$20$ minutes is $\frac13$ of a turn, $\theta = \frac{2\pi}{3}$, $s = 9 \cdot \frac{2\pi}{3} = 6\pi$.",
        {"A": r"$\theta = \frac{\pi}{3}$ would be $10$ minutes"}),
]
same("m", [sp.Rational(1, 2) * 400 * 2 * pi / 3, 9 * 2 * pi / 3], [400 * pi / 3, 6 * pi])

FRQS = []

TOPIC = Topic(
    number="0.1", title="Angles and Radian Measure",
    unit="Trig Review (a free module)", ced=["Prerequisite: radian measure"],
    goals=r"Measure angles in radians, convert to and from degrees, find coterminal angles, and use $s = r\theta$ and $A = \frac12 r^2\theta$.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
