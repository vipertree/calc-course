"""Topic 0.3: The six trigonometric functions (trig review; not a CED topic).

Right-triangle ratios (SOH CAH TOA) from scaling the unit-circle triangle; sin = y/r, cos = x/r, tan = y/x for a point on
the terminal side; csc, sec, cot as reciprocals; where each is undefined. Lesson example: legs 8 and 15. Worked examples:
sec(5pi/4) and csc(5pi/6), a tree's height, a ladder, sin and sec from tan = 2 in quadrant III.
"""
import sympy as sp

from calclib import (VideoExample, MCQ, BigIdea, Check, Formula, Item, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)
from calclib.figs import triangle

pi, r2, r3, r5 = sp.pi, sp.sqrt(2), sp.sqrt(3), sp.sqrt(5)
deg = lambda d: d * pi / 180
same("lesson", [sp.sqrt(8**2 + 15**2)], [17])
same("ex1", [1 / sp.cos(5 * pi / 4), 1 / sp.sin(5 * pi / 6)], [-r2, 2])
close("ex2", float(20 * sp.tan(deg(35))), 14.0, 0.05)
close("ex3", float(6 * sp.sin(deg(70))), 5.64, 0.005)
same("ex4", [-2 / r5, r5 / -1], [-2 * r5 / 5, -r5])

FIG_SOH = triangle("t0_3_soh", 4, 3, opp="opposite", adj="adjacent", hyp="hypotenuse", caption="Sides named from the angle $\\theta$.")

NOTES = [
    Video("s0_3.py::Lesson", "The six trigonometric functions", 7),

    Section("Right-triangle ratios"),
    Text(r"Scaling the unit-circle triangle by $r$ keeps the angle and makes the legs $r\cos\theta$ and $r\sin\theta$. So in any right triangle:"),
    Formula("SOH CAH TOA", r"\[ \sin\theta = \frac{\text{opposite}}{\text{hypotenuse}}, \qquad \cos\theta = \frac{\text{adjacent}}{\text{hypotenuse}}, \qquad \tan\theta = \frac{\text{opposite}}{\text{adjacent}}. \]"),
    FIG_SOH,
    VideoExample("Ratios from sides", work="3cm"),

    Section("Any angle"),
    Formula("A point on the terminal side", (r"If $(x, y)$ is on the terminal side of $\theta$ at distance $r = \sqrt{x^2 + y^2}$ from the origin, then "
                                            r"\[ \sin\theta = \blank{\frac{y}{r}}, \qquad \cos\theta = \blank{\frac{x}{r}}, \qquad \tan\theta = \blank{\frac{y}{x}}. \]")),

    Section("The reciprocal functions"),
    Formula("Cosecant, secant, cotangent", r"\[ \csc\theta = \frac{1}{\sin\theta}, \qquad \sec\theta = \frac{1}{\cos\theta}, \qquad \cot\theta = \frac{1}{\tan\theta} = \frac{\cos\theta}{\sin\theta}. \]"
            r"Memory tip: each pair has exactly one ``co'': sine with \textbf{co}secant, \textbf{co}sine with secant."),
    Text(r"\textbf{Undefined.} $\tan\theta$ and $\sec\theta$ divide by $\cos\theta$: undefined at $\frac{\pi}{2} + k\pi$. $\cot\theta$ and $\csc\theta$ divide by $\sin\theta$: undefined at $k\pi$."),
    BigIdea(r"Sine, cosine and tangent are ratios of sides; cosecant, secant and cotangent are their reciprocals. For angles past $\frac{\pi}{2}$, use a point $(x, y)$ and its distance $r$."),
    Check(r"Find $\sec\frac{\pi}{3}$.", selfcheck("2"), r"$\cos\frac{\pi}{3} = \frac12$, so $\sec\frac{\pi}{3} = 2$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"A right triangle has legs $3$ and $4$. $\theta$ is opposite the side of length $3$. Find $\cos\theta$.", num(sp.Rational(4, 5), display=r"\frac45"), r"Hypotenuse $5$; $\cos\theta = \frac45$.", work="1.2cm"),
    Item(r"A right triangle has hypotenuse $13$ and one leg $5$. $\theta$ is opposite the leg of length $5$. Find $\tan\theta$.", num(sp.Rational(5, 12), display=r"\frac{5}{12}"),
         r"Other leg $\sqrt{169 - 25} = 12$; $\tan\theta = \frac{5}{12}$.", work="1.4cm"),
    Item(r"Find $\csc\frac{\pi}{6}$.", num(2), r"$\frac{1}{\sin(\pi/6)} = \frac{1}{1/2} = 2$.", work="0.8cm"),
    Item(r"Find $\sec\frac{3\pi}{4}$.", num(-r2, display=r"-\sqrt2"), r"$\frac{1}{-\sqrt2/2} = -\sqrt2$.", work="1cm"),
    Item(r"Find $\cot\frac{\pi}{3}$.", num(r3 / 3, display=r"\frac{\sqrt3}{3}"), r"$\frac{\cos}{\sin} = \frac{1/2}{\sqrt3/2} = \frac{1}{\sqrt3} = \frac{\sqrt3}{3}$.", work="1cm"),
    Item(r"Find $\csc\frac{3\pi}{2}$.", num(-1), r"$\sin\frac{3\pi}{2} = -1$.", work="0.8cm"),
    Item(r"The point $(5, -12)$ is on the terminal side of $\theta$. Find $\sin\theta$.", num(-sp.Rational(12, 13), display=r"-\frac{12}{13}"), r"$r = 13$, $\sin\theta = \frac{y}{r} = -\frac{12}{13}$.", work="1.2cm"),
    Item(r"The point $(-2, -2)$ is on the terminal side of $\theta$. Find $\sec\theta$.", num(-r2, display=r"-\sqrt2"), r"$r = 2\sqrt2$, $\sec\theta = \frac{r}{x} = \frac{2\sqrt2}{-2} = -\sqrt2$.", work="1.2cm"),
    MCQ(r"For which value of $\theta$ is $\cot\theta$ undefined?", [r"$\frac{\pi}{2}$", r"$\pi$", r"$\frac{\pi}{4}$", r"$\frac{3\pi}{2}$"], "B", r"$\cot\theta = \frac{\cos\theta}{\sin\theta}$ and $\sin\pi = 0$.",
        {"A": r"$\cot\frac{\pi}{2} = 0$", "D": r"$\cot\frac{3\pi}{2} = 0$"}),
    Item(r"A kite string $50$ m long makes a $40^\circ$ angle with the ground. How high is the kite, to the nearest tenth of a meter?", num(50 * sp.sin(deg(40)), tol=0.05),
         r"$h = 50\sin 40^\circ \approx 32.1$ m.", work="1.4cm", calc=True),
    Item(r"A ramp rises $1.2$ m over a horizontal distance of $8$ m. Find the angle it makes with the ground, in degrees, to the nearest tenth.", num(sp.atan(sp.Rational(12, 80)) * 180 / pi, tol=0.05),
         r"$\tan\theta = \frac{1.2}{8} = 0.15$, $\theta = \tan^{-1}(0.15) \approx 8.5^\circ$.", work="1.4cm", calc=True),
    Item(r"$\cos\theta = \frac{2}{5}$ and $\theta$ is in quadrant IV. Find $\tan\theta$.", num(-sp.sqrt(21) / 2, display=r"-\frac{\sqrt{21}}{2}"),
         r"Point $(2, y)$ with $r = 5$: $y = -\sqrt{21}$; $\tan\theta = -\frac{\sqrt{21}}{2}$.", work="1.6cm"),
]
same("p", [1 / sp.cos(3 * pi / 4), sp.cot(pi / 3), 1 / sp.sin(3 * pi / 2)], [-r2, r3 / 3, -1])
close("p10", float(50 * sp.sin(deg(40))), 32.14, 0.01)
close("p11", float(sp.atan(0.15) * 180 / sp.pi), 8.53, 0.01)

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"A right triangle has legs $7$ and $24$. $\theta$ is opposite the side of length $7$. Find $\sin\theta$.", num(sp.Rational(7, 25), display=r"\frac{7}{25}"), r"Hypotenuse $25$.", work="1.2cm"),
        Item(r"A right triangle has legs $9$ and $40$. $\theta$ is opposite the side of length $40$. Find $\cos\theta$.", num(sp.Rational(9, 41), display=r"\frac{9}{41}"), r"Hypotenuse $41$; adjacent $9$.", work="1.2cm"),
        Item(r"A right triangle has legs $20$ and $21$. $\theta$ is opposite the side of length $20$. Find $\tan\theta$.", num(sp.Rational(20, 21), display=r"\frac{20}{21}"), r"Opposite over adjacent.", work="1.2cm"),
    ),
    Variants(
        Item(r"Find $\sec\frac{\pi}{6}$.", num(2 * r3 / 3, display=r"\frac{2\sqrt3}{3}"), r"$\frac{1}{\sqrt3/2} = \frac{2}{\sqrt3} = \frac{2\sqrt3}{3}$.", work="1cm"),
        Item(r"Find $\csc\frac{\pi}{4}$.", num(r2, display=r"\sqrt2"), r"$\frac{1}{\sqrt2/2} = \sqrt2$.", work="1cm"),
        Item(r"Find $\sec\frac{2\pi}{3}$.", num(-2), r"$\frac{1}{-1/2} = -2$.", work="1cm"),
    ),
    Variants(
        Item(r"Find $\cot\frac{5\pi}{6}$.", num(-r3, display=r"-\sqrt3"), r"$\frac{-\sqrt3/2}{1/2} = -\sqrt3$.", work="1cm"),
        Item(r"Find $\cot\frac{3\pi}{4}$.", num(-1), r"$\frac{-\sqrt2/2}{\sqrt2/2} = -1$.", work="1cm"),
        Item(r"Find $\csc\frac{4\pi}{3}$.", num(-2 * r3 / 3, display=r"-\frac{2\sqrt3}{3}"), r"$\frac{1}{-\sqrt3/2} = -\frac{2\sqrt3}{3}$.", work="1cm"),
    ),
    Variants(
        Item(r"The point $(-8, 6)$ is on the terminal side of $\theta$. Find $\cos\theta$.", num(-sp.Rational(4, 5), display=r"-\frac45"), r"$r = 10$, $\frac{x}{r} = -\frac{8}{10}$.", work="1cm"),
        Item(r"The point $(-5, -12)$ is on the terminal side of $\theta$. Find $\csc\theta$.", num(-sp.Rational(13, 12), display=r"-\frac{13}{12}"), r"$r = 13$, $\frac{r}{y} = -\frac{13}{12}$.", work="1cm"),
    ),
    Variants(
        Item(r"A $10$ m ladder makes a $65^\circ$ angle with the ground. How high up the wall does it reach, to the nearest hundredth?", num(10 * sp.sin(deg(65)), tol=0.01), r"$10\sin 65^\circ \approx 9.06$ m.", work="1.2cm", calc=True),
        Item(r"From $40$ m away, the angle up to the top of a building is $52^\circ$. How tall is it, to the nearest tenth?", num(40 * sp.tan(deg(52)), tol=0.05), r"$40\tan 52^\circ \approx 51.2$ m.", work="1.2cm", calc=True),
    ),
]
same("q", [1 / sp.cos(pi / 6), 1 / sp.sin(pi / 4), sp.cot(5 * pi / 6), sp.cot(3 * pi / 4), 1 / sp.sin(4 * pi / 3)], [2 * r3 / 3, r2, -r3, -1, -2 * r3 / 3])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"In a right triangle, $\sin\theta = \frac{5}{13}$. Then $\tan\theta = $", [r"$\frac{12}{13}$", r"$\frac{5}{12}$", r"$\frac{13}{12}$", r"$\frac{12}{5}$"], "B",
        r"Legs $5$ and $12$, hypotenuse $13$: $\tan\theta = \frac{5}{12}$.", {"A": r"that is $\cos\theta$", "D": r"that is $\cot\theta$"}),
    MCQ(r"$\sec\theta = -2$ and $\sin\theta > 0$. Then $\theta$ could be", [r"$\frac{\pi}{3}$", r"$\frac{4\pi}{3}$", r"$\frac{5\pi}{3}$", r"$\frac{2\pi}{3}$"], "D",
        r"$\cos\theta = -\frac12$ with $\sin\theta > 0$: quadrant II, $\frac{2\pi}{3}$.", {"B": r"$\sin\frac{4\pi}{3} < 0$", "A": r"$\sec\frac{\pi}{3} = 2$"}),
    MCQ(r"A plane takes off at a $12^\circ$ angle and flies in a straight line. After it has flown $3000$ m, what is its altitude, to the nearest meter?",
        [r"$624$ m", r"$638$ m", r"$2934$ m", r"$14{,}114$ m"], "A", r"$3000\sin 12^\circ \approx 623.7$.", {"B": r"that uses $\tan 12^\circ$", "C": r"that is the horizontal distance"}, calc=True),
    MCQ(r"Which expression equals $\cot\theta\,\sec\theta$ wherever both are defined?", [r"$\sin\theta$", r"$\cos\theta$", r"$\tan\theta$", r"$\csc\theta$"], "D",
        r"$\frac{\cos\theta}{\sin\theta} \cdot \frac{1}{\cos\theta} = \frac{1}{\sin\theta}$."),
]
close("m3", float(3000 * sp.sin(deg(12))), 623.7, 0.05)
close("m3b", float(3000 * sp.tan(deg(12))), 637.7, 0.1)
same("m4", [sp.simplify(sp.cot(sp.Symbol("t")) / sp.cos(sp.Symbol("t")) - 1 / sp.sin(sp.Symbol("t")))], [0])

FRQS = []

TOPIC = Topic(
    number="0.3", title="The Six Trigonometric Functions",
    unit="Trig Review (a free module)", ced=["Prerequisite: right-triangle and reciprocal trigonometric functions"],
    goals=r"Use SOH CAH TOA and the reciprocal functions $\csc$, $\sec$, $\cot$ to evaluate trig functions and solve right triangles.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
