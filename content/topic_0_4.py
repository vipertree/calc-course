"""Topic 0.4: Graphs of sine, cosine, and tangent (trig review; not a CED topic).

sin and cos as waves of period 2pi and range [-1, 1]; cos is sin shifted left pi/2; y = A sin(B(x - C)) + D: amplitude |A|,
period 2pi/|B|, shift C, midline y = D; tan: period pi, asymptotes where cos x = 0; sec, csc, cot from their partners.
Lesson example: y = 3cos(2x) + 1. Worked examples: y = -2 sin(pi x/3) + 5, an equation from a graph, a Ferris wheel,
asymptotes of tan(2x).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, expr, num, same, selfcheck)
from calclib.figs import graph

pi, x, t = sp.pi, sp.Symbol("x"), sp.Symbol("t")
same("ex1", [2 * pi / (pi / 3)], [6])
same("ex2", [(3 * sp.cos(pi * x / 2) + 2).subs(x, v) for v in (0, 2, 4)], [5, -1, 5])
h = 25 - 20 * sp.cos(pi * t / 2)
same("ex3", [h.subs(t, 0), h.subs(t, 1), h.subs(t, 2)], [5, 25, 45])

FIG_SINCOS = graph("t0_4_sincos", [("sin(deg(x))", -6.5, 6.5), ("cos(deg(x))", -6.5, 6.5, "dashed")], xr=(-6.6, 6.6), yr=(-1.5, 1.5), xpi=0.5, w="12cm", h="4cm",
                   caption=r"$y = \sin x$ (solid) and $y = \cos x$ (dashed): period $2\pi$, range $-1 \le y \le 1$.")
FIG_TAN = graph("t0_4_tan", [("tan(deg(x))", -4.6, -1.72), ("tan(deg(x))", -1.42, 1.42), ("tan(deg(x))", 1.72, 4.6)], xr=(-4.7, 4.7), yr=(-4.5, 4.5), xpi=0.5,
                vlines=(-4.712, -1.5708, 1.5708, 4.712), w="9cm", h="5cm", caption=r"$y = \tan x$: period $\pi$, asymptotes at $x = \frac{\pi}{2} + k\pi$.")

NOTES = [
    Video("s0_4.py::Lesson", "Graphs of sine, cosine, and tangent", 9),

    Section("Sine and cosine"),
    Text(r"Plot the height of the point on the unit circle against the angle and you get $y = \sin x$; plot how far across and you get $y = \cos x$. "
         r"Both repeat every $2\pi$ (their \textbf{period}) and stay between $-1$ and $1$. Cosine is sine slid $\frac{\pi}{2}$ to the left."),
    FIG_SINCOS,
    Text(r"$\sin x = 0$ at $x = k\pi$; $\cos x = 0$ at $x = \frac{\pi}{2} + k\pi$ ($k$ any integer)."),

    Section("Transformations"),
    Formula("Sinusoids", (r"\[ y = A\sin\big(B(x - C)\big) + D \qquad \text{or} \qquad y = A\cos\big(B(x - C)\big) + D \] "
                          r"amplitude $= \blank{|A|}$, \quad period $= \blank{\frac{2\pi}{|B|}}$, \quad shift $C$ to the right, \quad midline $y = \blank{D}$. "
                          r"The maximum is $D + |A|$ and the minimum is $D - |A|$. A negative $A$ flips the wave.")),
    VideoExample("Describing a cosine graph", work="3cm"),

    Section("Tangent and the reciprocal functions"),
    Text(r"$\tan x = \frac{\sin x}{\cos x}$ is zero where $\sin x = 0$ and has a vertical asymptote where $\cos x = 0$. Each branch rises; the period is $\pi$."),
    FIG_TAN,
    Text(r"$\sec x$ and $\csc x$ are U-shaped branches touching $\cos x$ and $\sin x$ at their peaks and troughs, with asymptotes where the partner is $0$. "
         r"$\cot x$ has falling branches and asymptotes at $x = k\pi$."),
    BigIdea(r"Read a sinusoid's shape off its formula: amplitude from $A$, period from $B$, shift from $C$, midline from $D$."),
    Check(r"Find the period of $y = \cos(4x)$.", selfcheck(r"\frac{\pi}{2}"), r"$\frac{2\pi}{4} = \frac{\pi}{2}$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Find the amplitude of $y = -5\cos x$.", num(5), r"$|-5| = 5$.", work="0.8cm"),
    Item(r"Find the period of $y = \sin(3x)$.", num(2 * pi / 3, display=r"\frac{2\pi}{3}"), r"$\frac{2\pi}{3}$.", work="0.8cm"),
    Item(r"Find the period of $y = \cos\left(\frac{x}{2}\right)$.", num(4 * pi, display=r"4\pi"), r"$\frac{2\pi}{1/2} = 4\pi$.", work="0.8cm"),
    Item(r"Find the period of $y = \sin(\pi x)$.", num(2), r"$\frac{2\pi}{\pi} = 2$.", work="0.8cm"),
    Item(r"Find the maximum value of $y = 4\sin(2x) - 3$.", num(1), r"$-3 + 4 = 1$.", work="0.8cm"),
    Item(r"Find the minimum value of $y = 2 - 6\cos x$.", num(-4), r"Midline $2$, amplitude $6$: $2 - 6 = -4$.", work="0.8cm"),
    Item(r"Find the midline of $y = 3\cos(x - \pi) + 7$.", selfcheck("y = 7"), r"$D = 7$.", work="0.8cm"),
    Item(r"Find the period of $y = \tan(3x)$.", num(pi / 3, display=r"\frac{\pi}{3}"), r"Tangent's period is $\pi$; $\frac{\pi}{3}$.", work="0.8cm"),
    MCQ(r"Which function has a maximum at $x = 0$?", [r"$y = \sin x$", r"$y = -\cos x$", r"$y = \cos x$", r"$y = \tan x$"], "C", r"$\cos 0 = 1$, its largest value.",
        {"B": r"$-\cos x$ has a minimum at $0$", "A": r"$\sin 0 = 0$ is on the midline"}),
    Item(r"Write a sine function with amplitude $2$, period $\pi$, and midline $y = -1$.", selfcheck(r"y = 2\sin(2x) - 1"), r"$B = \frac{2\pi}{\pi} = 2$: $y = 2\sin(2x) - 1$.", work="1.2cm"),
    Item(r"Find the first vertical asymptote of $y = \tan\left(\frac{x}{2}\right)$ to the right of $x = 0$.", num(pi, display=r"\pi"), r"$\frac{x}{2} = \frac{\pi}{2}$, so $x = \pi$.", work="1cm"),
    Item(r"The temperature in a city is modeled by $T(m) = 60 - 20\cos\left(\frac{\pi m}{6}\right)$ degrees, $m$ months after January 1. What is the highest temperature, and in which month $m$ does it occur ($0 \le m < 12$)?",
         selfcheck(r"80^\circ \text{ at } m = 6"), r"Maximum $60 + 20 = 80$ when $\cos\frac{\pi m}{6} = -1$: $\frac{\pi m}{6} = \pi$, $m = 6$ (July 1).", work="1.6cm"),
]
same("p", [2 * pi / (sp.Rational(1, 2)), 2 * pi / pi], [4 * pi, 2])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find the period of $y = 3\sin(4x)$.", num(pi / 2, display=r"\frac{\pi}{2}"), r"$\frac{2\pi}{4}$.", work="0.8cm"),
        Item(r"Find the period of $y = \cos\left(\frac{\pi x}{4}\right)$.", num(8), r"$\frac{2\pi}{\pi/4} = 8$.", work="0.8cm"),
        Item(r"Find the period of $y = -2\sin(6x) + 1$.", num(pi / 3, display=r"\frac{\pi}{3}"), r"$\frac{2\pi}{6}$.", work="0.8cm"),
    ),
    Variants(
        Item(r"Find the maximum value of $y = 5 - 3\sin(2x)$.", num(8), r"$5 + 3$.", work="0.8cm"),
        Item(r"Find the minimum value of $y = 4\cos(x) + 9$.", num(5), r"$9 - 4$.", work="0.8cm"),
        Item(r"Find the maximum value of $y = -7\cos(3x) - 2$.", num(5), r"$-2 + 7$.", work="0.8cm"),
    ),
    Variants(
        MCQ(r"The graph of $y = \sin\left(x - \frac{\pi}{3}\right)$ is the graph of $y = \sin x$ shifted", [r"left $\frac{\pi}{3}$", r"right $\frac{\pi}{3}$", r"up $\frac{\pi}{3}$", r"down $\frac{\pi}{3}$"], "B",
            r"$x - C$ slides right $C$.", {"A": r"$x + \frac{\pi}{3}$ would slide left"}),
        MCQ(r"The graph of $y = \cos x - 2$ is the graph of $y = \cos x$ shifted", [r"left $2$", r"right $2$", r"up $2$", r"down $2$"], "D", r"Subtracting outside lowers the midline.",
            {"B": "a shift right changes $x$, inside"}),
    ),
    Variants(
        Item(r"Find the vertical asymptotes of $y = \tan x$ for $0 \le x \le 2\pi$.", selfcheck(r"x = \frac{\pi}{2}, \ \frac{3\pi}{2}"), r"Where $\cos x = 0$.", work="1cm"),
        Item(r"Find the vertical asymptotes of $y = \sec x$ for $0 \le x \le 2\pi$.", selfcheck(r"x = \frac{\pi}{2}, \ \frac{3\pi}{2}"), r"Where $\cos x = 0$.", work="1cm"),
        Item(r"Find the vertical asymptotes of $y = \csc x$ for $0 < x < 2\pi$.", selfcheck(r"x = \pi"), r"Where $\sin x = 0$.", work="1cm"),
    ),
    Variants(
        Item(r"A sinusoid has a maximum of $9$ and a minimum of $1$. Find its amplitude.", num(4), r"$\frac{9 - 1}{2}$.", work="1cm"),
        Item(r"A sinusoid has a maximum of $3$ and a minimum of $-7$. Find its midline value $D$.", num(-2), r"$\frac{3 + (-7)}{2}$.", work="1cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"Which equation has amplitude $3$ and period $4\pi$?", [r"$y = 3\sin(2x)$", r"$y = 3\sin\left(\frac{x}{2}\right)$", r"$y = 4\sin(3x)$", r"$y = \frac12\sin(3x)$"], "B",
        r"$\frac{2\pi}{1/2} = 4\pi$.", {"A": r"period $\pi$"}),
    MCQ(r"The depth of water in a harbor is $d(t) = 8 + 3\cos\left(\frac{\pi t}{6}\right)$ meters, $t$ hours after midnight. When is the water first at its lowest after midnight?",
        [r"$t = 3$", r"$t = 12$", r"$t = 6$", r"$t = 9$"], "C", r"Lowest when $\cos\frac{\pi t}{6} = -1$: $\frac{\pi t}{6} = \pi$, $t = 6$.", {"B": "that is the next high tide", "A": "the depth is at the midline then"}),
    MCQ(r"Which function has period $\pi$ and passes through the origin?", [r"$y = \cos(2x)$", r"$y = \sin\left(\frac{x}{2}\right)$", r"$y = \tan(2x)$", r"$y = \tan x$"], "D",
        r"$\tan x$ has period $\pi$ and $\tan 0 = 0$.", {"A": r"$\cos 0 = 1$", "C": r"period $\frac{\pi}{2}$"}),
    MCQ(r"A sinusoid has a maximum at $(0, 6)$ and the next minimum at $(5, 2)$. Which equation fits?",
        [r"$y = 2\cos\left(\frac{\pi x}{5}\right) + 4$", r"$y = 4\cos\left(\frac{\pi x}{5}\right) + 2$", r"$y = 2\cos\left(\frac{2\pi x}{5}\right) + 4$", r"$y = 2\sin\left(\frac{\pi x}{5}\right) + 4$"], "A",
        r"Midline $4$, amplitude $2$, period $10$ so $B = \frac{\pi}{5}$, and a maximum at $0$ means cosine.", {"C": "max to min is half a period, so the period is 10", "D": "sine starts on the midline"}),
]
d = 8 + 3 * sp.cos(pi * t / 6)
same("m2", [d.subs(t, 6)], [5])
y4 = 2 * sp.cos(pi * x / 5) + 4
same("m4", [y4.subs(x, 0), y4.subs(x, 5)], [6, 2])

FRQS = []

TOPIC = Topic(
    number="0.4", title="Graphs of Sine, Cosine, and Tangent",
    unit="Trig Review (a free module)", ced=["Prerequisite: graphs of trigonometric functions"],
    goals=r"Graph sine, cosine and tangent, and read amplitude, period, shift and midline from $y = A\sin\big(B(x - C)\big) + D$.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
