"""Topic 0.7: Inverse trigonometric functions (trig review; not a CED topic; Topic 3.4 differentiates them).

Restricting sine, cosine and tangent to one-to-one pieces; arcsin, arccos, arctan with their inputs and outputs; the
notation sin^-1 x = arcsin x (not 1/sin x); sin(arcsin x) = x but arcsin(sin x) answers in arcsin's range; triangles for
compositions; solving with a calculator. Lesson example: arcsin(-1/2), arccos(-1/2), arctan(sqrt 3). Worked examples:
arctan(-1) and arccos(-sqrt2/2), cos(arcsin 2/3), tan(arccos x), 3 sin x = 1.
"""
import sympy as sp

from calclib import (VideoExample, MCQ, BigIdea, Check, Formula, Item, Section, Table, Text, Topic, Variants, Video, close, expr, num, same, selfcheck)
from calclib.figs import graph

pi, x = sp.pi, sp.Symbol("x", positive=True)
r2, r3 = sp.sqrt(2), sp.sqrt(3)
same("lesson", [sp.asin(-sp.Rational(1, 2)), sp.acos(-sp.Rational(1, 2)), sp.atan(r3)], [-pi / 6, 2 * pi / 3, pi / 3])
same("undo", [sp.asin(sp.sin(5 * pi / 6))], [pi / 6])
same("ex1", [sp.atan(-1), sp.acos(-r2 / 2)], [-pi / 4, 3 * pi / 4])
same("ex2", [sp.cos(sp.asin(sp.Rational(2, 3)))], [sp.sqrt(5) / 3])
same("ex3", [sp.simplify(sp.tan(sp.acos(sp.Rational(1, 3))) - sp.sqrt(1 - sp.Rational(1, 9)) * 3)], [0])
close("ex4", float(sp.asin(sp.Rational(1, 3))), 0.340, 5e-4)
close("ex4b", float(pi - sp.asin(sp.Rational(1, 3))), 2.802, 5e-4)

FIG_INV = graph("t0_7_inv", [("rad(asin(x))", -1, 1), ("rad(atan(x))", -4, 4, "dashed")], xr=(-4.2, 4.2), yr=(-1.9, 1.9), w="9cm", h="4.6cm",
                hlines=(1.5708, -1.5708), caption=r"$y = \arcsin x$ (solid) and $y = \arctan x$ (dashed, with asymptotes $y = \pm\frac{\pi}{2}$).")

NOTES = [
    Video("s0_7.py::Lesson", "Inverse trigonometric functions", 7),

    Section("Restricting to one piece"),
    Text(r"To run a function backward, every output must come from one input. Sine repeats, so we keep one piece on which it takes each value once: "
         r"sine on $\left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$, cosine on $[0, \pi]$, tangent on $\left(-\frac{\pi}{2}, \frac{\pi}{2}\right)$."),
    Formula("Definitions", (r"$\arcsin x$ is the angle in $\left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$ whose sine is $x$. "
                            r"$\arccos x$ is the angle in $\blank{[0, \pi]}$ whose cosine is $x$. "
                            r"$\arctan x$ is the angle in $\blank{\left(-\frac{\pi}{2}, \frac{\pi}{2}\right)}$ whose tangent is $x$.")),
    Table(r"$\arcsin x$ & $-1 \le x \le 1$ & $-\frac{\pi}{2} \le y \le \frac{\pi}{2}$ \\[5pt] $\arccos x$ & $-1 \le x \le 1$ & $0 \le y \le \pi$ \\[5pt] "
          r"$\arctan x$ & all real $x$ & $-\frac{\pi}{2} < y < \frac{\pi}{2}$", "l|c|c", header=r"function & inputs & outputs"),
    FIG_INV,
    VideoExample("Evaluating inverse trig functions", work="3cm"),

    Section("Notation and compositions"),
    Text(r"$\sin^{-1} x$ means $\arcsin x$, \textbf{not} $\frac{1}{\sin x}$ (that is $\csc x$)."),
    Text(r"$\sin(\arcsin x) = x$ for $-1 \le x \le 1$. The other order answers in arcsine's range: $\arcsin\left(\sin\frac{5\pi}{6}\right) = \arcsin\frac12 = \frac{\pi}{6}$."),
    Text(r"\textbf{Compositions with a triangle.} For $\cos(\arcsin\frac23)$, let $\theta = \arcsin\frac23$: opposite $2$, hypotenuse $3$, adjacent $\sqrt5$, so $\cos\theta = \frac{\sqrt5}{3}$."),
    Text(r"\textbf{Calculator.} $\arcsin$ gives only one solution of $\sin x = c$. Find the other from the quadrants: for $\sin x = \frac13$, $x \approx 0.340$ and $x \approx \pi - 0.340 \approx 2.802$."),
    BigIdea(r"An inverse trig function returns an angle, always from its own range: $\left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$ for arcsine and arctangent (open for arctangent), $[0, \pi]$ for arccosine."),
    Check(r"Find $\arccos 0$.", selfcheck(r"\frac{\pi}{2}"), r"The angle in $[0, \pi]$ with cosine $0$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Find $\arcsin\frac{\sqrt2}{2}$.", num(pi / 4, display=r"\frac{\pi}{4}"), r"In $\left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$ with sine $\frac{\sqrt2}{2}$.", work="0.8cm"),
    Item(r"Find $\arccos\frac{\sqrt3}{2}$.", num(pi / 6, display=r"\frac{\pi}{6}"), r"In $[0, \pi]$ with cosine $\frac{\sqrt3}{2}$.", work="0.8cm"),
    Item(r"Find $\arctan\left(-\sqrt3\right)$.", num(-pi / 3, display=r"-\frac{\pi}{3}"), r"Tangent is odd; $-\frac{\pi}{3}$ is in range.", work="0.8cm"),
    Item(r"Find $\arccos(-1)$.", num(pi, display=r"\pi"), r"$\cos\pi = -1$.", work="0.8cm"),
    Item(r"Find $\arcsin(-1)$.", num(-pi / 2, display=r"-\frac{\pi}{2}"), r"$\sin\left(-\frac{\pi}{2}\right) = -1$.", work="0.8cm"),
    Item(r"Find $\arccos\left(-\frac{\sqrt3}{2}\right)$.", num(5 * pi / 6, display=r"\frac{5\pi}{6}"), r"Reference angle $\frac{\pi}{6}$ in quadrant II.", work="1cm"),
    Item(r"Find $\arcsin\left(\sin\frac{2\pi}{3}\right)$.", num(pi / 3, display=r"\frac{\pi}{3}"), r"$\sin\frac{2\pi}{3} = \frac{\sqrt3}{2}$, and $\arcsin\frac{\sqrt3}{2} = \frac{\pi}{3}$.", work="1cm"),
    Item(r"Find $\arccos\left(\cos\left(-\frac{\pi}{4}\right)\right)$.", num(pi / 4, display=r"\frac{\pi}{4}"), r"$\cos\left(-\frac{\pi}{4}\right) = \frac{\sqrt2}{2}$; arccosine answers in $[0, \pi]$.", work="1cm"),
    Item(r"Find $\sin\left(\arccos\frac{4}{5}\right)$.", num(sp.Rational(3, 5), display=r"\frac35"), r"Adjacent $4$, hypotenuse $5$, opposite $3$.", work="1.2cm"),
    Item(r"Find $\sec\left(\arctan\frac{5}{12}\right)$.", num(sp.Rational(13, 12), display=r"\frac{13}{12}"), r"Opposite $5$, adjacent $12$, hypotenuse $13$.", work="1.2cm"),
    Item(r"Write $\cos(\arcsin x)$ as an algebraic expression.", expr(sp.sqrt(1 - x**2)), r"Opposite $x$, hypotenuse $1$: $\sqrt{1 - x^2}$ (nonnegative, since arcsine is in quadrant I or IV).", work="1.4cm"),
    Item(r"Solve $\tan x = 2$ for $0 \le x < 2\pi$, to three decimal places.", selfcheck(r"x \approx 1.107, \ 4.249"), r"$\arctan 2 \approx 1.107$; add $\pi$: $4.249$.", work="1.4cm", calc=True),
]
same("p", [sp.acos(-r3 / 2), sp.asin(sp.sin(2 * pi / 3)), sp.acos(sp.cos(-pi / 4)), sp.sin(sp.acos(sp.Rational(4, 5))), 1 / sp.cos(sp.atan(sp.Rational(5, 12)))],
     [5 * pi / 6, pi / 3, pi / 4, sp.Rational(3, 5), sp.Rational(13, 12)])
close("p12", float(sp.atan(2) + pi), 4.249, 5e-4)

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find $\arcsin\frac{\sqrt3}{2}$.", num(pi / 3, display=r"\frac{\pi}{3}"), r"$\sin\frac{\pi}{3} = \frac{\sqrt3}{2}$.", work="0.8cm"),
        Item(r"Find $\arcsin\left(-\frac{\sqrt2}{2}\right)$.", num(-pi / 4, display=r"-\frac{\pi}{4}"), r"Sine is odd.", work="0.8cm"),
        Item(r"Find $\arctan\frac{\sqrt3}{3}$.", num(pi / 6, display=r"\frac{\pi}{6}"), r"$\tan\frac{\pi}{6} = \frac{\sqrt3}{3}$.", work="0.8cm"),
    ),
    Variants(
        Item(r"Find $\arccos\left(-\frac{\sqrt2}{2}\right)$.", num(3 * pi / 4, display=r"\frac{3\pi}{4}"), r"Quadrant II.", work="0.8cm"),
        Item(r"Find $\arccos\frac12$.", num(pi / 3, display=r"\frac{\pi}{3}"), r"$\cos\frac{\pi}{3} = \frac12$.", work="0.8cm"),
        Item(r"Find $\arccos\left(-\frac{\sqrt3}{2}\right)$.", num(5 * pi / 6, display=r"\frac{5\pi}{6}"), r"Quadrant II.", work="0.8cm"),
    ),
    Variants(
        MCQ(r"$\arcsin\left(\sin\frac{3\pi}{4}\right) = $", [r"$\frac{3\pi}{4}$", r"$\frac{\pi}{4}$", r"$-\frac{\pi}{4}$", r"$\frac{\sqrt2}{2}$"], "B", r"$\sin\frac{3\pi}{4} = \frac{\sqrt2}{2}$; $\arcsin\frac{\sqrt2}{2} = \frac{\pi}{4}$.",
            {"A": r"$\frac{3\pi}{4}$ is outside arcsine's range", "D": "arcsine returns an angle"}),
        MCQ(r"$\arccos\left(\cos\frac{5\pi}{3}\right) = $", [r"$\frac{5\pi}{3}$", r"$-\frac{\pi}{3}$", r"$\frac{\pi}{3}$", r"$\frac12$"], "C", r"$\cos\frac{5\pi}{3} = \frac12$; $\arccos\frac12 = \frac{\pi}{3}$.",
            {"A": r"$\frac{5\pi}{3}$ is outside $[0, \pi]$", "B": r"arccosine never returns a negative angle"}),
    ),
    Variants(
        Item(r"Find $\tan\left(\arcsin\frac{3}{5}\right)$.", num(sp.Rational(3, 4), display=r"\frac34"), r"Opposite $3$, hypotenuse $5$, adjacent $4$.", work="1.2cm"),
        Item(r"Find $\cos\left(\arctan\frac{8}{15}\right)$.", num(sp.Rational(15, 17), display=r"\frac{15}{17}"), r"Opposite $8$, adjacent $15$, hypotenuse $17$.", work="1.2cm"),
        Item(r"Find $\sin\left(\arccos\frac{5}{13}\right)$.", num(sp.Rational(12, 13), display=r"\frac{12}{13}"), r"Adjacent $5$, hypotenuse $13$, opposite $12$.", work="1.2cm"),
    ),
    Variants(
        MCQ(r"$\sin^{-1} x$ means", [r"$\frac{1}{\sin x}$", r"$\csc x$", r"$-\sin x$", r"$\arcsin x$"], "D", r"The $-1$ marks the inverse function.", {"A": r"that is $(\sin x)^{-1}$"}),
        MCQ(r"Which value is in the range of $\arccos x$?", [r"$-\frac{\pi}{4}$", r"$\frac{3\pi}{4}$", r"$\frac{3\pi}{2}$", r"$-\pi$"], "B", r"The range is $[0, \pi]$.", {"A": r"that is in arcsine's range"}),
    ),
]
same("q", [sp.tan(sp.asin(sp.Rational(3, 5))), sp.cos(sp.atan(sp.Rational(8, 15))), sp.sin(sp.acos(sp.Rational(5, 13)))], [sp.Rational(3, 4), sp.Rational(15, 17), sp.Rational(12, 13)])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$\arctan(-1) + \arccos(-1) = $", [r"$\frac{3\pi}{4}$", r"$0$", r"$\frac{5\pi}{4}$", r"$-\frac{5\pi}{4}$"], "A", r"$-\frac{\pi}{4} + \pi = \frac{3\pi}{4}$.", {"B": r"$\arccos(-1) = \pi$, not $\frac{\pi}{4}$"}),
    MCQ(r"$\cos\left(\arcsin\left(-\frac{1}{3}\right)\right) = $", [r"$-\frac{2\sqrt2}{3}$", r"$\frac{2\sqrt2}{3}$", r"$\frac{\sqrt2}{3}$", r"$-\frac13$"], "B",
        r"$\arcsin\left(-\frac13\right)$ is in quadrant IV, where cosine is positive: $\sqrt{1 - \frac19} = \frac{2\sqrt2}{3}$.", {"A": "arcsine of a negative number is in quadrant IV, where cosine is positive"}),
    MCQ(r"A ramp rises $1$ ft over a horizontal run of $12$ ft. To the nearest tenth of a degree, its angle with the ground is", [r"$4.8^\circ$", r"$85.2^\circ$", r"$0.1^\circ$", r"$4.5^\circ$"], "A",
        r"$\arctan\frac{1}{12} \approx 4.76^\circ$ (degree mode).", {"C": "that is the angle in radians, rounded", "B": "that is the angle at the top"}, calc=True),
    MCQ(r"Which equation has exactly one solution?", [r"$\sin x = \frac12$ for $0 \le x < 2\pi$", r"$\cos x = 0$ for $0 \le x < 2\pi$", r"$\tan x = 3$ for $0 \le x < 2\pi$", r"$\tan x = 3$ for $-\frac{\pi}{2} < x < \frac{\pi}{2}$"], "D",
        r"Tangent takes each value once on $\left(-\frac{\pi}{2}, \frac{\pi}{2}\right)$: $x = \arctan 3$.", {"C": r"$\arctan 3$ and $\arctan 3 + \pi$"}),
]
same("m", [sp.atan(-1) + sp.acos(-1), sp.cos(sp.asin(-sp.Rational(1, 3)))], [3 * pi / 4, 2 * r2 / 3])
close("m3", float(sp.atan(sp.Rational(1, 12)) * 180 / pi), 4.76, 0.005)

FRQS = []

TOPIC = Topic(
    number="0.7", title="Inverse Trigonometric Functions",
    unit="Trig Review (a free module)", ced=["Prerequisite: inverse trigonometric functions"],
    goals=r"Evaluate $\arcsin$, $\arccos$ and $\arctan$ from their ranges, simplify compositions with a triangle, and solve trig equations with a calculator.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
