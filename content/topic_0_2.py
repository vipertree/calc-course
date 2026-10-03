"""Topic 0.2: The unit circle (trig review; not a CED topic).

cos and sin as the coordinates of the point at angle theta on the unit circle; cos^2 + sin^2 = 1; the quadrantal angles;
the 45-45-90 and 30-60-90 triangles give the first-quadrant values; reference angles; signs by quadrant; tan = sin/cos as
the slope of the terminal side. Lesson example: cos and sin of 5pi/6. Worked examples: 4pi/3, -pi/4, 3pi and 3pi/2,
cos from sin = 3/5 in quadrant II.
"""
import sympy as sp

from calclib import (VideoExample, MCQ, BigIdea, Check, Formula, Item, Section, Table, Text, Topic, Variants, Video, num, same, selfcheck)
from calclib.figs import unit_circle

pi, r2, r3 = sp.pi, sp.sqrt(2), sp.sqrt(3)
same("lesson", [sp.cos(5 * pi / 6), sp.sin(5 * pi / 6)], [-r3 / 2, sp.Rational(1, 2)])
same("ex", [sp.cos(4 * pi / 3), sp.sin(4 * pi / 3), sp.sin(-pi / 4), sp.cos(-pi / 4), sp.cos(3 * pi), sp.sin(3 * pi / 2)],
     [-sp.Rational(1, 2), -r3 / 2, -r2 / 2, r2 / 2, -1, -1])
same("ex4", [-sp.sqrt(1 - sp.Rational(9, 25)), sp.Rational(3, 5) / (-sp.Rational(4, 5))], [-sp.Rational(4, 5), -sp.Rational(3, 4)])

FIG_DEF = unit_circle("t0_2_def", [(0.9, r"$(\cos\theta, \sin\theta)$")], triangle=0.9, caption="The point at angle $\\theta$ is $(\\cos\\theta, \\sin\\theta)$.")
FIG_REF = unit_circle("t0_2_ref", [(5 * float(pi) / 6, r"$\left(-\frac{\sqrt3}{2}, \frac12\right)$"), (float(pi) / 6, r"$\left(\frac{\sqrt3}{2}, \frac12\right)$")],
                      triangle=5 * float(pi) / 6, caption="$\\frac{5\\pi}{6}$ has reference angle $\\frac{\\pi}{6}$: same numbers, the quadrant sets the signs.")

NOTES = [
    Video("s0_2.py::Lesson", "The unit circle", 8),

    Section("Sine and cosine"),
    Formula("Definition", (r"The \textbf{unit circle} is $x^2 + y^2 = 1$. The point at angle $\theta$ on it is \[ (\cos\theta,\ \sin\theta). \] "
                           r"Cosine is the $\blank{x}$-coordinate (how far across); sine is the $\blank{y}$-coordinate (how far up).")),
    FIG_DEF,
    Formula("The Pythagorean identity", r"\[ \cos^2\theta + \sin^2\theta = 1 \] for every angle $\theta$, because every point of the unit circle is $1$ from the center."),

    Section("The values to know"),
    Text(r"The quadrantal angles land on the axes. The $45$-$45$-$90$ triangle with hypotenuse $1$ has legs $\frac{\sqrt2}{2}$; the $30$-$60$-$90$ triangle "
         r"(half of an equilateral triangle of side $1$) has legs $\frac12$ and $\frac{\sqrt3}{2}$."),
    Table(r"$0$ & $1$ & $0$ & $0$ \\ $\frac{\pi}{6}$ & $\frac{\sqrt3}{2}$ & $\frac12$ & $\frac{\sqrt3}{3}$ \\ $\frac{\pi}{4}$ & $\frac{\sqrt2}{2}$ & $\frac{\sqrt2}{2}$ & $1$ \\ "
          r"$\frac{\pi}{3}$ & $\frac12$ & $\frac{\sqrt3}{2}$ & $\sqrt3$ \\ $\frac{\pi}{2}$ & $0$ & $1$ & undefined \\ $\pi$ & $-1$ & $0$ & $0$ \\ $\frac{3\pi}{2}$ & $0$ & $-1$ & undefined",
          "c|c|c|c", header=r"$\theta$ & $\cos\theta$ & $\sin\theta$ & $\tan\theta$"),
    Text(r"Memory check: as the angle grows from $\frac{\pi}{6}$ to $\frac{\pi}{3}$ the point rises, so sine goes up ($\frac12$, $\frac{\sqrt2}{2}$, $\frac{\sqrt3}{2}$) and cosine goes down."),

    Section("Reference angles and signs"),
    Text(r"The \textbf{reference angle} is the acute angle between the terminal side and the $x$-axis. It gives the numbers; the quadrant gives the signs: "
         r"cosine is positive on the right half (quadrants I and IV), sine is positive on the top half (quadrants I and II)."),
    FIG_REF,
    VideoExample("Sine and cosine of 5π/6", work="3cm"),

    Section("Tangent"),
    Formula("Tangent", r"\[ \tan\theta = \frac{\sin\theta}{\cos\theta}, \] the slope of the terminal side. It is undefined where $\cos\theta = 0$ ($\theta = \frac{\pi}{2}, \frac{3\pi}{2}, \dots$)."),
    BigIdea(r"On the unit circle, $\cos\theta$ is how far across and $\sin\theta$ is how far up. Know the first quadrant; everything else is a reflection with signs."),
    Check(r"Find $\cos\frac{7\pi}{4}$.", selfcheck(r"\frac{\sqrt2}{2}"), r"Reference angle $\frac{\pi}{4}$, quadrant IV, where cosine is positive."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Find $\sin\frac{\pi}{3}$.", num(r3 / 2, display=r"\frac{\sqrt3}{2}"), r"The point at $\frac{\pi}{3}$ is $\left(\frac12, \frac{\sqrt3}{2}\right)$.", work="0.8cm"),
    Item(r"Find $\cos\frac{3\pi}{4}$.", num(-r2 / 2, display=r"-\frac{\sqrt2}{2}"), r"Reference angle $\frac{\pi}{4}$, quadrant II: cosine negative.", work="1cm"),
    Item(r"Find $\sin\frac{7\pi}{6}$.", num(-sp.Rational(1, 2), display=r"-\frac12"), r"Reference angle $\frac{\pi}{6}$, quadrant III: sine negative.", work="1cm"),
    Item(r"Find $\cos\frac{5\pi}{3}$.", num(sp.Rational(1, 2), display=r"\frac12"), r"Reference angle $\frac{\pi}{3}$, quadrant IV: cosine positive.", work="1cm"),
    Item(r"Find $\tan\frac{2\pi}{3}$.", num(-r3, display=r"-\sqrt3"), r"$\frac{\sqrt3/2}{-1/2} = -\sqrt3$.", work="1cm"),
    Item(r"Find $\sin\left(-\frac{\pi}{2}\right)$.", num(-1), r"$-\frac{\pi}{2}$ lands at $(0, -1)$.", work="0.8cm"),
    Item(r"Find $\cos\frac{11\pi}{6}$.", num(r3 / 2, display=r"\frac{\sqrt3}{2}"), r"Reference angle $\frac{\pi}{6}$, quadrant IV.", work="1cm"),
    Item(r"Find $\tan\frac{5\pi}{4}$.", num(1), r"Both coordinates are $-\frac{\sqrt2}{2}$, so the slope is $1$.", work="1cm"),
    MCQ(r"In which quadrant are $\sin\theta < 0$ and $\cos\theta > 0$?", ["I", "II", "III", "IV"], "D", r"Below the $x$-axis and to the right of the $y$-axis.",
        {"B": "that is sine positive, cosine negative"}),
    Item(r"$\cos\theta = -\frac{5}{13}$ and $\theta$ is in quadrant III. Find $\sin\theta$.", num(-sp.Rational(12, 13), display=r"-\frac{12}{13}"),
         r"$\sin^2\theta = 1 - \frac{25}{169} = \frac{144}{169}$; quadrant III, so $\sin\theta = -\frac{12}{13}$.", work="1.6cm"),
    Item(r"$\sin\theta = \frac{1}{3}$ and $\frac{\pi}{2} < \theta < \pi$. Find $\cos\theta$.", num(-2 * r2 / 3, display=r"-\frac{2\sqrt2}{3}"),
         r"$\cos^2\theta = \frac89$, and cosine is negative in quadrant II: $-\frac{2\sqrt2}{3}$.", work="1.6cm"),
    Item(r"Find $\sin\frac{13\pi}{6}$.", num(sp.Rational(1, 2), display=r"\frac12"), r"$\frac{13\pi}{6} - 2\pi = \frac{\pi}{6}$.", work="1cm"),
]
same("p", [sp.cos(3 * pi / 4), sp.sin(7 * pi / 6), sp.cos(5 * pi / 3), sp.tan(2 * pi / 3), sp.cos(11 * pi / 6), sp.tan(5 * pi / 4), sp.sin(13 * pi / 6)],
     [-r2 / 2, -sp.Rational(1, 2), sp.Rational(1, 2), -r3, r3 / 2, 1, sp.Rational(1, 2)])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find $\cos\frac{2\pi}{3}$.", num(-sp.Rational(1, 2), display=r"-\frac12"), r"Reference angle $\frac{\pi}{3}$, quadrant II.", work="1cm"),
        Item(r"Find $\sin\frac{5\pi}{4}$.", num(-r2 / 2, display=r"-\frac{\sqrt2}{2}"), r"Reference angle $\frac{\pi}{4}$, quadrant III.", work="1cm"),
        Item(r"Find $\cos\frac{7\pi}{6}$.", num(-r3 / 2, display=r"-\frac{\sqrt3}{2}"), r"Reference angle $\frac{\pi}{6}$, quadrant III.", work="1cm"),
    ),
    Variants(
        Item(r"Find $\sin\frac{5\pi}{3}$.", num(-r3 / 2, display=r"-\frac{\sqrt3}{2}"), r"Reference angle $\frac{\pi}{3}$, quadrant IV.", work="1cm"),
        Item(r"Find $\sin\frac{3\pi}{4}$.", num(r2 / 2, display=r"\frac{\sqrt2}{2}"), r"Reference angle $\frac{\pi}{4}$, quadrant II.", work="1cm"),
        Item(r"Find $\cos\left(-\frac{\pi}{3}\right)$.", num(sp.Rational(1, 2), display=r"\frac12"), r"Reference angle $\frac{\pi}{3}$, quadrant IV.", work="1cm"),
    ),
    Variants(
        Item(r"Find $\tan\frac{\pi}{6}$.", num(r3 / 3, display=r"\frac{\sqrt3}{3}"), r"$\frac{1/2}{\sqrt3/2} = \frac{1}{\sqrt3} = \frac{\sqrt3}{3}$.", work="1cm"),
        Item(r"Find $\tan\frac{4\pi}{3}$.", num(r3, display=r"\sqrt3"), r"$\frac{-\sqrt3/2}{-1/2} = \sqrt3$.", work="1cm"),
        Item(r"Find $\tan\frac{7\pi}{4}$.", num(-1), r"$\frac{-\sqrt2/2}{\sqrt2/2} = -1$.", work="1cm"),
    ),
    Variants(
        MCQ(r"Which is the value of $\cos\pi$?", [r"$0$", r"$1$", r"$-1$", "undefined"], "C", r"The point at $\pi$ is $(-1, 0)$.", {"A": r"that is $\sin\pi$"}),
        MCQ(r"Which is the value of $\sin\frac{\pi}{2}$?", [r"$1$", r"$0$", r"$-1$", "undefined"], "A", r"The point at $\frac{\pi}{2}$ is $(0, 1)$.", {"B": r"that is $\cos\frac{\pi}{2}$"}),
    ),
    Variants(
        Item(r"$\sin\theta = -\frac45$ and $\theta$ is in quadrant IV. Find $\cos\theta$.", num(sp.Rational(3, 5), display=r"\frac35"), r"$\cos^2\theta = \frac{9}{25}$; positive in quadrant IV.", work="1.4cm"),
        Item(r"$\cos\theta = \frac{8}{17}$ and $\theta$ is in quadrant IV. Find $\sin\theta$.", num(-sp.Rational(15, 17), display=r"-\frac{15}{17}"), r"$\sin^2\theta = \frac{225}{289}$; negative in quadrant IV.", work="1.4cm"),
    ),
]
same("q", [sp.cos(2 * pi / 3), sp.sin(5 * pi / 4), sp.cos(7 * pi / 6), sp.sin(5 * pi / 3), sp.sin(3 * pi / 4), sp.tan(pi / 6), sp.tan(4 * pi / 3), sp.tan(7 * pi / 4)],
     [-sp.Rational(1, 2), -r2 / 2, -r3 / 2, -r3 / 2, r2 / 2, r3 / 3, r3, -1])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$\sin\frac{11\pi}{6} = $", [r"$-\frac12$", r"$\frac12$", r"$-\frac{\sqrt3}{2}$", r"$\frac{\sqrt3}{2}$"], "A", r"Reference angle $\frac{\pi}{6}$, quadrant IV: sine negative.",
        {"B": "sine is negative in quadrant IV", "C": r"that is $\sin\frac{5\pi}{3}$"}),
    MCQ(r"If $\tan\theta > 0$ and $\sin\theta < 0$, then $\theta$ is in quadrant", ["I", "II", "III", "IV"], "C", r"Sine negative means III or IV; tangent positive needs cosine negative too: III."),
    MCQ(r"$\cos\theta = -\frac{2}{3}$ and $\pi < \theta < \frac{3\pi}{2}$. Then $\sin\theta = $",
        [r"$\frac{\sqrt5}{3}$", r"$-\frac13$", r"$\frac13$", r"$-\frac{\sqrt5}{3}$"], "D", r"$\sin^2\theta = 1 - \frac49 = \frac59$; quadrant III, so negative.", {"A": "sine is negative in quadrant III", "B": r"$1 - \frac23$ is not $\sin\theta$"}),
    MCQ(r"Which of the following is undefined?", [r"$\sin\frac{3\pi}{2}$", r"$\tan\frac{3\pi}{2}$", r"$\cos\frac{\pi}{2}$", r"$\tan\pi$"], "B", r"$\cos\frac{3\pi}{2} = 0$, so $\tan\frac{3\pi}{2} = \frac{-1}{0}$.",
        {"C": r"$\cos\frac{\pi}{2} = 0$ is defined", "D": r"$\tan\pi = \frac{0}{-1} = 0$"}),
]
same("m", [sp.sin(11 * pi / 6), -sp.sqrt(1 - sp.Rational(4, 9))], [-sp.Rational(1, 2), -sp.sqrt(5) / 3])

FRQS = []

TOPIC = Topic(
    number="0.2", title="The Unit Circle",
    unit="Unit 0: Trig Review", ced=["Prerequisite: unit circle trigonometry"],
    goals=r"Read $\sin\theta$, $\cos\theta$ and $\tan\theta$ off the unit circle at every landmark angle, using reference angles and the signs by quadrant.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
