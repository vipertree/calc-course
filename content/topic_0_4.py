"""Trig Review lesson 0.4 (T4): The six trigonometric functions of any angle (trig review; not a CED topic).

T1 does right triangles and T3 puts them on the unit circle. This lesson takes any point (x, y) on a terminal side, at
distance r from the origin: sin = y/r, cos = x/r, tan = y/x; csc, sec, cot as reciprocals for every angle; where each
is undefined. Lesson example: the point (-5, 12). Worked examples: sec(5pi/4) and csc(5pi/6), the point (4, -3),
sin and sec from tan = 2 in quadrant III, tan and csc from cos = -5/13 in quadrant II.
"""
import sympy as sp

from calclib import (VideoExample, MCQ, BigIdea, Check, Formula, Item, Section, Text, Topic, Variants, Video, num, same, selfcheck)
from calclib.figs import unit_circle

pi, r2, r3, r5 = sp.pi, sp.sqrt(2), sp.sqrt(3), sp.sqrt(5)
R = sp.Rational
same("lesson", [sp.sqrt(25 + 144), R(12, 13), R(-5, 13), R(12, -5)], [13, R(12, 13), R(-5, 13), R(-12, 5)])
same("recip", [R(13, 12), R(13, -5), R(-5, 12), 1 / sp.cos(pi / 3)], [R(13, 12), R(-13, 5), R(-5, 12), 2])
same("ex1", [1 / sp.cos(5 * pi / 4), 1 / sp.sin(5 * pi / 6)], [-r2, 2])
same("ex2", [sp.sqrt(16 + 9), R(5, -3), R(5, 4), R(4, -3)], [5, R(-5, 3), R(5, 4), R(-4, 3)])
same("ex3", [-2 / r5, r5 / -1], [-2 * r5 / 5, -r5])
same("ex4", [sp.sqrt(169 - 25), R(12, -5), R(13, 12)], [12, R(-12, 5), R(13, 12)])

FIG_PT = unit_circle("t0_4_point", [(float(sp.atan2(4, -3)), r"$\left(-\frac35, \frac45\right)$")], triangle=float(sp.atan2(4, -3)),
                     caption=r"$(-3, 4)$ is $5$ from the origin. Divide by $5$ and it lands on the unit circle at $\left(-\frac35, \frac45\right)$, so $\cos\theta = -\frac35$ and $\sin\theta = \frac45$.")

NOTES = [
    Video("s0_4.py::Lesson", "The six trigonometric functions", 7),

    Section("Any angle, any point"),
    Text(r"A point on the terminal side of $\theta$ doesn't have to be on the unit circle. Dividing its coordinates by its distance $r$ from the origin "
         r"moves it onto the unit circle, where the coordinates are $\cos\theta$ and $\sin\theta$."),
    Formula("A point on the terminal side", (r"If $(x, y)$ is on the terminal side of $\theta$ at distance $r = \sqrt{x^2 + y^2}$ from the origin, then "
                                            r"\[ \sin\theta = \blank{\frac{y}{r}}, \qquad \cos\theta = \blank{\frac{x}{r}}, \qquad \tan\theta = \blank{\frac{y}{x}}. \] "
                                            r"In quadrant I this is SOH CAH TOA with opposite $y$, adjacent $x$ and hypotenuse $r$; elsewhere the signs of $x$ and $y$ give the signs.")),
    FIG_PT,
    VideoExample("A point on the terminal side", work="3cm"),

    Section("The reciprocal functions"),
    Formula("Cosecant, secant, cotangent", r"\[ \csc\theta = \frac{1}{\sin\theta} = \frac{r}{y}, \qquad \sec\theta = \frac{1}{\cos\theta} = \frac{r}{x}, \qquad \cot\theta = \frac{1}{\tan\theta} = \frac{\cos\theta}{\sin\theta} = \frac{x}{y}. \]"
            r"Memory tip: each pair has exactly one ``co'': sine with \textbf{co}secant, \textbf{co}sine with secant."),
    Text(r"At a landmark angle, flip the unit-circle value: $\cos\frac{\pi}{3} = \frac12$, so $\sec\frac{\pi}{3} = 2$."),
    Text(r"\textbf{Undefined.} $\tan\theta$ and $\sec\theta$ divide by $\cos\theta$: undefined at $\frac{\pi}{2} + k\pi$. $\cot\theta$ and $\csc\theta$ divide by $\sin\theta$: undefined at $k\pi$."),
    BigIdea(r"For any angle, a point $(x, y)$ on its terminal side and its distance $r$ give all six functions: $\sin\theta = \frac{y}{r}$, $\cos\theta = \frac{x}{r}$, $\tan\theta = \frac{y}{x}$, and their reciprocals."),
    Check(r"Find $\sec\frac{\pi}{3}$.", selfcheck("2"), r"$\cos\frac{\pi}{3} = \frac12$, so $\sec\frac{\pi}{3} = 2$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Find $\csc\frac{\pi}{6}$.", num(2), r"$\frac{1}{\sin(\pi/6)} = \frac{1}{1/2} = 2$.", work="0.8cm"),
    Item(r"Find $\sec\frac{3\pi}{4}$.", num(-r2, display=r"-\sqrt2"), r"$\frac{1}{-\sqrt2/2} = -\sqrt2$.", work="1cm"),
    Item(r"Find $\cot\frac{\pi}{3}$.", num(r3 / 3, display=r"\frac{\sqrt3}{3}"), r"$\frac{\cos}{\sin} = \frac{1/2}{\sqrt3/2} = \frac{1}{\sqrt3} = \frac{\sqrt3}{3}$.", work="1cm"),
    Item(r"Find $\csc\frac{3\pi}{2}$.", num(-1), r"$\sin\frac{3\pi}{2} = -1$.", work="0.8cm"),
    Item(r"Find $\sec\pi$.", num(-1), r"$\cos\pi = -1$, so $\sec\pi = \frac{1}{-1} = -1$.", work="0.8cm"),
    Item(r"The point $(5, -12)$ is on the terminal side of $\theta$. Find $\sin\theta$.", num(-R(12, 13), display=r"-\frac{12}{13}"), r"$r = 13$, $\sin\theta = \frac{y}{r} = -\frac{12}{13}$.", work="1.2cm"),
    Item(r"The point $(-8, 15)$ is on the terminal side of $\theta$. Find $\cos\theta$ and $\tan\theta$.", selfcheck(r"\cos\theta = -\frac{8}{17}, \ \tan\theta = -\frac{15}{8}"),
         r"$r = \sqrt{64 + 225} = 17$. $\cos\theta = \frac{x}{r} = -\frac{8}{17}$, $\tan\theta = \frac{y}{x} = -\frac{15}{8}$.", work="1.4cm"),
    Item(r"The point $(-2, -2)$ is on the terminal side of $\theta$. Find $\sec\theta$.", num(-r2, display=r"-\sqrt2"), r"$r = 2\sqrt2$, $\sec\theta = \frac{r}{x} = \frac{2\sqrt2}{-2} = -\sqrt2$.", work="1.2cm"),
    Item(r"The point $(3, -4)$ is on the terminal side of $\theta$. Find $\csc\theta$, $\sec\theta$, and $\cot\theta$.", selfcheck(r"\csc\theta = -\frac54, \ \sec\theta = \frac53, \ \cot\theta = -\frac34"),
         r"$r = 5$. $\csc\theta = \frac{r}{y} = -\frac54$, $\sec\theta = \frac{r}{x} = \frac53$, $\cot\theta = \frac{x}{y} = -\frac34$.", work="1.6cm"),
    MCQ(r"For which value of $\theta$ is $\cot\theta$ undefined?", [r"$\frac{\pi}{2}$", r"$\pi$", r"$\frac{\pi}{4}$", r"$\frac{3\pi}{2}$"], "B", r"$\cot\theta = \frac{\cos\theta}{\sin\theta}$ and $\sin\pi = 0$.",
        {"A": r"$\cot\frac{\pi}{2} = 0$", "D": r"$\cot\frac{3\pi}{2} = 0$"}),
    Item(r"$\cos\theta = \frac{2}{5}$ and $\theta$ is in quadrant IV. Find $\tan\theta$.", num(-sp.sqrt(21) / 2, display=r"-\frac{\sqrt{21}}{2}"),
         r"Point $(2, y)$ with $r = 5$: $y = -\sqrt{21}$; $\tan\theta = -\frac{\sqrt{21}}{2}$.", work="1.6cm"),
    Item(r"$\sec\theta = -2$ and $\pi < \theta < \frac{3\pi}{2}$. Find $\tan\theta$.", num(r3, display=r"\sqrt3"),
         r"$\cos\theta = -\frac12$: point $(-1, y)$ with $r = 2$, and $y = -\sqrt3$ in quadrant III. $\tan\theta = \frac{-\sqrt3}{-1} = \sqrt3$.", work="1.6cm"),
]
same("p", [1 / sp.cos(3 * pi / 4), sp.cot(pi / 3), 1 / sp.sin(3 * pi / 2), 1 / sp.cos(pi), sp.sqrt(64 + 225), sp.tan(4 * pi / 3)], [-r2, r3 / 3, -1, -1, 17, r3])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"The point $(-3, -4)$ is on the terminal side of $\theta$. Find $\tan\theta$.", num(R(4, 3), display=r"\frac43"), r"$\frac{y}{x} = \frac{-4}{-3} = \frac43$.", work="1cm"),
        Item(r"The point $(12, -5)$ is on the terminal side of $\theta$. Find $\sin\theta$.", num(-R(5, 13), display=r"-\frac{5}{13}"), r"$r = 13$, $\frac{y}{r} = -\frac{5}{13}$.", work="1cm"),
        Item(r"The point $(-6, 8)$ is on the terminal side of $\theta$. Find $\cos\theta$.", num(-R(3, 5), display=r"-\frac35"), r"$r = 10$, $\frac{x}{r} = -\frac{6}{10} = -\frac35$.", work="1cm"),
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
        Item(r"The point $(-8, 6)$ is on the terminal side of $\theta$. Find $\sec\theta$.", num(-R(5, 4), display=r"-\frac54"), r"$r = 10$, $\frac{r}{x} = -\frac{10}{8} = -\frac54$.", work="1cm"),
        Item(r"The point $(-5, -12)$ is on the terminal side of $\theta$. Find $\csc\theta$.", num(-R(13, 12), display=r"-\frac{13}{12}"), r"$r = 13$, $\frac{r}{y} = -\frac{13}{12}$.", work="1cm"),
    ),
    Variants(
        Item(r"$\cos\theta = \frac35$ and $\theta$ is in quadrant IV. Find $\csc\theta$.", num(-R(5, 4), display=r"-\frac54"),
             r"Point $(3, y)$ with $r = 5$: $y = -4$ in quadrant IV. $\csc\theta = \frac{r}{y} = -\frac54$.", work="1.4cm"),
        Item(r"$\sin\theta = -\frac23$ and $\theta$ is in quadrant III. Find $\sec\theta$.", num(-3 * r5 / 5, display=r"-\frac{3\sqrt5}{5}"),
             r"Point $(x, -2)$ with $r = 3$: $x = -\sqrt5$ in quadrant III. $\sec\theta = \frac{r}{x} = -\frac{3}{\sqrt5} = -\frac{3\sqrt5}{5}$.", work="1.4cm"),
    ),
]
same("q", [1 / sp.cos(pi / 6), 1 / sp.sin(pi / 4), sp.cot(5 * pi / 6), sp.cot(3 * pi / 4), 1 / sp.sin(4 * pi / 3), -3 / r5], [2 * r3 / 3, r2, -r3, -1, -2 * r3 / 3, -3 * r5 / 5])

# ---------------------------------------------------------------- test prep
th_m3 = pi - sp.asin(R(1, 3))
MCQS = [
    MCQ(r"The point $(-7, 24)$ is on the terminal side of $\theta$. Then $\cos\theta = $", [r"$\frac{7}{25}$", r"$-\frac{24}{25}$", r"$-\frac{7}{25}$", r"$-\frac{7}{24}$"], "C",
        r"$r = \sqrt{49 + 576} = 25$, so $\cos\theta = \frac{x}{r} = -\frac{7}{25}$.", {"A": r"$x$ is negative", "D": r"that is $\cot\theta$"}),
    MCQ(r"$\sec\theta = -2$ and $\sin\theta > 0$. Then $\theta$ could be", [r"$\frac{\pi}{3}$", r"$\frac{4\pi}{3}$", r"$\frac{5\pi}{3}$", r"$\frac{2\pi}{3}$"], "D",
        r"$\cos\theta = -\frac12$ with $\sin\theta > 0$: quadrant II, $\frac{2\pi}{3}$.", {"B": r"$\sin\frac{4\pi}{3} < 0$", "A": r"$\sec\frac{\pi}{3} = 2$"}),
    MCQ(r"$\csc\theta = 3$ and $\cos\theta < 0$. Then $\tan\theta = $", [r"$-\frac{\sqrt2}{4}$", r"$\frac{\sqrt2}{4}$", r"$-2\sqrt2$", r"$-\frac{2\sqrt2}{3}$"], "A",
        r"$\sin\theta = \frac13$: point $(x, 1)$ with $r = 3$, $x = -2\sqrt2$ since cosine is negative. $\tan\theta = \frac{1}{-2\sqrt2} = -\frac{\sqrt2}{4}$.",
        {"B": "cosine is negative, so tangent is too", "C": r"that is $\cot\theta$", "D": r"that is $\cos\theta$"}),
    MCQ(r"Which expression equals $\cot\theta\,\sec\theta$ wherever both are defined?", [r"$\sin\theta$", r"$\cos\theta$", r"$\tan\theta$", r"$\csc\theta$"], "D",
        r"$\frac{\cos\theta}{\sin\theta} \cdot \frac{1}{\cos\theta} = \frac{1}{\sin\theta}$."),
]
same("m3", [sp.tan(th_m3), sp.cos(th_m3), sp.cot(th_m3)], [-r2 / 4, -2 * r2 / 3, -2 * r2])
same("m4", [sp.simplify(sp.cot(sp.Symbol("t")) / sp.cos(sp.Symbol("t")) - 1 / sp.sin(sp.Symbol("t")))], [0])

FRQS = []

TOPIC = Topic(
    number="0.4", title="The Six Trigonometric Functions",
    unit="Trig Review (a free module)", ced=["Prerequisite: trigonometric functions of any angle"],
    goals=r"Find all six trig functions of any angle from a point on its terminal side or from one known value, and know where each is undefined.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
