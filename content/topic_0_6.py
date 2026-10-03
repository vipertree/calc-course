"""Topic 0.6: Solving trigonometric equations (trig review; not a CED topic).

Two angles per value in one turn (plus 2k pi); isolate the trig function; factor instead of dividing by a trig function;
rewrite with an identity so the angles match; for kx, solve over k turns then divide. Lesson example: 2cos x + 1 = 0.
Worked examples: tan x = -1, 2sin^2 x - sin x - 1 = 0, cos 2x = cos x, sin 2x = sqrt(3)/2.
"""
import sympy as sp

from calclib import (VideoExample, MCQ, BigIdea, Check, Formula, Item, Section, Text, Topic, Variants, Video, num, same, selfcheck)
from calclib.figs import unit_circle

pi, x = sp.pi, sp.Symbol("x", real=True)


def roots(eq, n=24000):
    """Numeric roots of eq on [0, 2pi): grid points where |eq| has a small local minimum, polished with findroot."""
    import mpmath
    f = sp.lambdify(x, eq, "mpmath")
    h = 2 * mpmath.pi / n
    vals = [abs(f(k * h)) for k in range(n + 2)]
    out = []
    for k in range(n + 1):
        if vals[k] <= vals[k - 1] and vals[k] <= vals[k + 1] and vals[k] < 1e-2:
            try:
                r = mpmath.findroot(f, k * h, tol=1e-20)
            except (ValueError, ZeroDivisionError):
                r = k * h
            if abs(f(r)) < 1e-9:
                r = float(r) % (2 * float(sp.pi))
                if min((abs(r - o) for o in out), default=1) > 1e-6 and 2 * float(sp.pi) - r > 1e-6:
                    out.append(r)
    return sorted(out)


def sols(eq, want):
    """The solutions of eq = 0 on [0, 2pi) are exactly `want` (each checked exactly, the count numerically)."""
    for w in want:
        if sp.simplify(eq.subs(x, w)) != 0:
            raise SystemExit(f"solution check failed: {w} does not solve {eq}")
    got = roots(eq)
    if len(got) != len(want) or any(abs(a - float(b)) > 1e-6 for a, b in zip(got, sorted(want, key=float))):
        raise SystemExit(f"solution check failed: {eq}: numeric roots {got}, want {sorted(want, key=float)}")


sols(2 * sp.cos(x) + 1, {2 * pi / 3, 4 * pi / 3})
sols(2 * sp.sin(x)**2 - sp.sin(x), {0, pi, pi / 6, 5 * pi / 6})
sols(sp.sin(2 * x) - sp.cos(x), {pi / 2, 3 * pi / 2, pi / 6, 5 * pi / 6})
sols(sp.sin(2 * x) - 1, {pi / 4, 5 * pi / 4})
sols(sp.tan(x) + 1, {3 * pi / 4, 7 * pi / 4})
sols(2 * sp.sin(x)**2 - sp.sin(x) - 1, {7 * pi / 6, 11 * pi / 6, pi / 2})
sols(sp.cos(2 * x) - sp.cos(x), {0, 2 * pi / 3, 4 * pi / 3})
sols(sp.sin(2 * x) - sp.sqrt(3) / 2, {pi / 6, pi / 3, 7 * pi / 6, 4 * pi / 3})

FIG_HALF = unit_circle("t0_6_half", [(float(pi) / 6, r"$\frac{\pi}{6}$"), (5 * float(pi) / 6, r"$\frac{5\pi}{6}$")],
                       caption=r"$\sin x = \frac12$: two points at height $\frac12$ in one turn.", labels=False)

NOTES = [
    Video("s0_6.py::Lesson", "Solving trigonometric equations", 8),

    Section("Two angles per value"),
    Text(r"In one turn, $\sin x = c$ (for $-1 < c < 1$) has two solutions: the points of the unit circle at height $c$. Likewise $\cos x = c$ has two, at the points with "
         r"$x$-coordinate $c$. Adding $2k\pi$ gives all the others."),
    FIG_HALF,
    Formula("Method", (r"1. \blank{Isolate} the trig function (or move everything to one side and factor). \\ 2. Find the \blank{reference angle}. "
                       r"\\ 3. Use every quadrant where the sign is right. \\ 4. List the solutions in the interval asked for.")),
    VideoExample("Solving 2cos x + 1 = 0", work="3cm"),

    Section("Factoring and identities"),
    Text(r"\textbf{Never divide by a trig function}: dividing $2\sin^2 x = \sin x$ by $\sin x$ loses $x = 0$ and $x = \pi$. Move everything to one side and factor: "
         r"$\sin x(2\sin x - 1) = 0$."),
    Text(r"When the angles don't match ($\sin 2x$ and $\cos x$), rewrite with an identity first: $2\sin x\cos x = \cos x$, then factor out $\cos x$."),

    Section("Multiple angles"),
    Text(r"For $\sin 2x = 1$ on $0 \le x < 2\pi$, the angle $2x$ runs over $0 \le 2x < 4\pi$: two turns. Solve for $2x$ on both turns ($\frac{\pi}{2}$, $\frac{5\pi}{2}$), then divide: $x = \frac{\pi}{4}, \frac{5\pi}{4}$."),
    BigIdea(r"Find every solution in the interval: two per turn for most values, and $k$ turns' worth when the angle is $kx$."),
    Check(r"Solve $\cos x = 0$ for $0 \le x < 2\pi$.", selfcheck(r"x = \frac{\pi}{2}, \ \frac{3\pi}{2}"), r"The top and bottom of the circle."),
]

# ---------------------------------------------------------------- practice
I = r" for $0 \le x < 2\pi$."
PRACTICE = [
    Item(r"Solve $\cos x = \frac{\sqrt2}{2}$" + I, selfcheck(r"x = \frac{\pi}{4}, \ \frac{7\pi}{4}"), r"Reference angle $\frac{\pi}{4}$; cosine positive in I and IV.", work="1.2cm"),
    Item(r"Solve $2\sin x + \sqrt3 = 0$" + I, selfcheck(r"x = \frac{4\pi}{3}, \ \frac{5\pi}{3}"), r"$\sin x = -\frac{\sqrt3}{2}$: III and IV.", work="1.4cm"),
    Item(r"Solve $\tan x = \sqrt3$" + I, selfcheck(r"x = \frac{\pi}{3}, \ \frac{4\pi}{3}"), r"Tangent positive in I and III.", work="1.2cm"),
    Item(r"Solve $\sin x = -1$" + I, num(3 * pi / 2, display=r"\frac{3\pi}{2}"), r"The bottom of the circle.", work="1cm"),
    Item(r"Solve $4\cos^2 x = 1$" + I, selfcheck(r"x = \frac{\pi}{3}, \ \frac{2\pi}{3}, \ \frac{4\pi}{3}, \ \frac{5\pi}{3}"), r"$\cos x = \pm\frac12$: keep both signs.", work="1.6cm"),
    Item(r"Solve $\sin x\cos x = 0$" + I, selfcheck(r"x = 0, \ \frac{\pi}{2}, \ \pi, \ \frac{3\pi}{2}"), r"$\sin x = 0$ or $\cos x = 0$.", work="1.4cm"),
    Item(r"Solve $2\cos^2 x + \cos x = 0$" + I, selfcheck(r"x = \frac{\pi}{2}, \ \frac{3\pi}{2}, \ \frac{2\pi}{3}, \ \frac{4\pi}{3}"), r"$\cos x(2\cos x + 1) = 0$.", work="1.6cm"),
    Item(r"Solve $2\cos^2 x - 3\cos x + 1 = 0$" + I, selfcheck(r"x = 0, \ \frac{\pi}{3}, \ \frac{5\pi}{3}"), r"$(2\cos x - 1)(\cos x - 1) = 0$.", work="1.8cm"),
    Item(r"Solve $\cos 2x = \frac12$" + I, selfcheck(r"x = \frac{\pi}{6}, \ \frac{5\pi}{6}, \ \frac{7\pi}{6}, \ \frac{11\pi}{6}"), r"$2x = \frac{\pi}{3}, \frac{5\pi}{3}, \frac{7\pi}{3}, \frac{11\pi}{3}$.", work="1.8cm"),
    Item(r"Solve $\sin 2x = \sin x$" + I, selfcheck(r"x = 0, \ \pi, \ \frac{\pi}{3}, \ \frac{5\pi}{3}"), r"$\sin x(2\cos x - 1) = 0$.", work="1.8cm"),
    MCQ(r"A student divides $\tan^2 x = \tan x$ by $\tan x$ and gets $\tan x = 1$. Which solutions in $0 \le x < 2\pi$ are lost?", [r"$\frac{\pi}{4}$ and $\frac{5\pi}{4}$", r"$0$ and $\pi$", r"$\frac{\pi}{2}$ and $\frac{3\pi}{2}$", "none"], "B",
        r"$\tan x(\tan x - 1) = 0$ also gives $\tan x = 0$: $x = 0, \pi$.", {"A": "those are the ones the student found", "C": r"$\tan x$ is undefined there"}),
    Item(r"The Ferris wheel height is $h(t) = 25 - 20\cos\left(\frac{\pi t}{2}\right)$. Find the times $0 \le t < 4$ when $h(t) = 15$.", selfcheck(r"t = \frac23, \ \frac{10}{3}"),
         r"$\cos\frac{\pi t}{2} = \frac12$: $\frac{\pi t}{2} = \frac{\pi}{3}, \frac{5\pi}{3}$, so $t = \frac23, \frac{10}{3}$.", work="2cm"),
]
sols(4 * sp.cos(x)**2 - 1, {pi / 3, 2 * pi / 3, 4 * pi / 3, 5 * pi / 3})
sols(2 * sp.cos(x)**2 - 3 * sp.cos(x) + 1, {0, pi / 3, 5 * pi / 3})
sols(sp.cos(2 * x) - sp.Rational(1, 2), {pi / 6, 5 * pi / 6, 7 * pi / 6, 11 * pi / 6})
sols(sp.sin(2 * x) - sp.sin(x), {0, pi, pi / 3, 5 * pi / 3})
same("p12", [25 - 20 * sp.cos(pi * sp.Rational(2, 3) / 2), 25 - 20 * sp.cos(pi * sp.Rational(10, 3) / 2)], [15, 15])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Solve $2\sin x = 1$" + I, selfcheck(r"x = \frac{\pi}{6}, \ \frac{5\pi}{6}"), r"$\sin x = \frac12$.", work="1.2cm"),
        Item(r"Solve $2\cos x = \sqrt3$" + I, selfcheck(r"x = \frac{\pi}{6}, \ \frac{11\pi}{6}"), r"$\cos x = \frac{\sqrt3}{2}$: I and IV.", work="1.2cm"),
        Item(r"Solve $\sqrt2\sin x + 1 = 0$" + I, selfcheck(r"x = \frac{5\pi}{4}, \ \frac{7\pi}{4}"), r"$\sin x = -\frac{\sqrt2}{2}$: III and IV.", work="1.2cm"),
    ),
    Variants(
        Item(r"Solve $\tan x + \sqrt3 = 0$" + I, selfcheck(r"x = \frac{2\pi}{3}, \ \frac{5\pi}{3}"), r"Tangent negative in II and IV.", work="1.2cm"),
        Item(r"Solve $\sqrt3\tan x = 1$" + I, selfcheck(r"x = \frac{\pi}{6}, \ \frac{7\pi}{6}"), r"$\tan x = \frac{\sqrt3}{3}$: I and III.", work="1.2cm"),
    ),
    Variants(
        Item(r"Solve $2\sin^2 x + \sin x = 0$" + I, selfcheck(r"x = 0, \ \pi, \ \frac{7\pi}{6}, \ \frac{11\pi}{6}"), r"$\sin x(2\sin x + 1) = 0$.", work="1.6cm"),
        Item(r"Solve $2\cos^2 x = \cos x$" + I, selfcheck(r"x = \frac{\pi}{2}, \ \frac{3\pi}{2}, \ \frac{\pi}{3}, \ \frac{5\pi}{3}"), r"$\cos x(2\cos x - 1) = 0$.", work="1.6cm"),
    ),
    Variants(
        Item(r"Solve $2\sin^2 x + \sin x - 1 = 0$" + I, selfcheck(r"x = \frac{\pi}{6}, \ \frac{5\pi}{6}, \ \frac{3\pi}{2}"), r"$(2\sin x - 1)(\sin x + 1) = 0$.", work="1.8cm"),
        Item(r"Solve $2\cos^2 x + \cos x - 1 = 0$" + I, selfcheck(r"x = \frac{\pi}{3}, \ \pi, \ \frac{5\pi}{3}"), r"$(2\cos x - 1)(\cos x + 1) = 0$.", work="1.8cm"),
    ),
    Variants(
        MCQ(r"How many solutions does $\sin 3x = 1$ have for $0 \le x < 2\pi$?", ["1", "2", "3", "6"], "C", r"$3x$ covers three turns, one solution per turn.", {"A": "the angle $3x$ goes around three times"}),
        MCQ(r"How many solutions does $\cos 2x = 0$ have for $0 \le x < 2\pi$?", ["2", "4", "1", "8"], "B", r"$2x$ covers two turns, two solutions per turn.", {"A": "the angle $2x$ goes around twice"}),
    ),
]
sols(2 * sp.sin(x)**2 + sp.sin(x) - 1, {pi / 6, 5 * pi / 6, 3 * pi / 2})
sols(2 * sp.cos(x)**2 + sp.cos(x) - 1, {pi / 3, pi, 5 * pi / 3})
same("q5", [len(roots(sp.sin(3 * x) - 1)), len(roots(sp.cos(2 * x)))], [3, 4])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"The solutions of $2\cos x + \sqrt2 = 0$ for $0 \le x < 2\pi$ are", [r"$\frac{\pi}{4}, \frac{7\pi}{4}$", r"$\frac{3\pi}{4}, \frac{5\pi}{4}$", r"$\frac{3\pi}{4}, \frac{7\pi}{4}$", r"$\frac{5\pi}{4}, \frac{7\pi}{4}$"], "B",
        r"$\cos x = -\frac{\sqrt2}{2}$: quadrants II and III.", {"A": "cosine is negative here", "D": "that is where sine is negative"}),
    MCQ(r"How many solutions does $\sin^2 x = \frac14$ have for $0 \le x < 2\pi$?", ["1", "2", "3", "4"], "D", r"$\sin x = \pm\frac12$: two angles each.", {"B": r"keep both signs of $\pm\frac12$"}),
    MCQ(r"Which value is a solution of $\cos 2x = \sin x$?", [r"$\frac{\pi}{6}$", r"$\frac{\pi}{3}$", r"$\frac{\pi}{4}$", r"$\pi$"], "A",
        r"$1 - 2\sin^2 x = \sin x$: $(2\sin x - 1)(\sin x + 1) = 0$, so $\sin x = \frac12$ or $-1$; $\frac{\pi}{6}$ works."),
    MCQ(r"The depth of water is $d(t) = 8 + 3\cos\left(\frac{\pi t}{6}\right)$ meters, $t$ hours after midnight. At what times $0 \le t < 12$ is the depth $9.5$ m?",
        [r"$t = 1, 11$", r"$t = 4, 8$", r"$t = 2, 10$", r"$t = 2, 4$"], "C", r"$\cos\frac{\pi t}{6} = \frac12$: $\frac{\pi t}{6} = \frac{\pi}{3}, \frac{5\pi}{3}$, so $t = 2, 10$.",
        {"B": r"that solves $\cos\frac{\pi t}{6} = -\frac12$"}),
]
sols(2 * sp.cos(x) + sp.sqrt(2), {3 * pi / 4, 5 * pi / 4})
sols(sp.cos(2 * x) - sp.sin(x), {pi / 6, 5 * pi / 6, 3 * pi / 2})
same("m4", [8 + 3 * sp.cos(pi * 2 / 6), 8 + 3 * sp.cos(pi * 10 / 6)], [sp.Rational(19, 2), sp.Rational(19, 2)])

FRQS = []

TOPIC = Topic(
    number="0.6", title="Solving Trigonometric Equations",
    unit="Unit 0: Trig Review", ced=["Prerequisite: solving trigonometric equations"],
    goals=r"Find every solution of a trig equation in an interval, by isolating, factoring, using identities, and handling multiple angles.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
