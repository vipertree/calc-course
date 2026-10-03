"""Topic 9.8 (BC): Finding the area of a polar region or the area bounded by a single polar curve.

CED: CHA-5.D/CHA-5.E (polar area): a sector has area (1/2) r^2 dtheta, so A = (1/2) integral of r^2 dtheta; limits where
the radius starts and stops sweeping the region (often r = 0), each piece swept once. Lesson example: inside
r = 1 + cos theta (3 pi/2). Worked examples: one petal of r = sin 2 theta (pi/8); r = 4 sin theta on [0, pi] (4 pi);
spiral r = theta on [0, pi] (pi^3/6).
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)
from calclib.figs import graph

th = sp.symbols("theta", real=True)


def parea(r, a, b):
    return sp.simplify(sp.integrate(r**2, (th, a, b)) / 2)


same("lesson", [parea(1 + sp.cos(th), 0, 2 * sp.pi)], [3 * sp.pi / 2])
same("ex", [parea(sp.sin(2 * th), 0, sp.pi / 2), parea(4 * sp.sin(th), 0, sp.pi), parea(th, 0, sp.pi)], [sp.pi / 8, 4 * sp.pi, sp.pi**3 / 6])

FIG = graph("t9_8_rose", [], (-1.2, 1.2), (-1.2, 1.2), extra=r"\addplot[fn, domain=0:360, samples=300, variable=\t]({sin(2*\t)*cos(\t)},{sin(2*\t)*sin(\t)});", w="5cm", h="5cm",
            caption=r"The rose $r = \sin 2\theta$: one petal for each interval of length $\frac\pi2$.")

NOTES = [
    Video("s9_8.py::Lesson", "Polar area", 5),

    Section("Wedges, not rectangles"),
    Text(r"A sector of a circle with angle $\Delta\theta$ is the fraction $\frac{\Delta\theta}{2\pi}$ of the whole circle, so its area is $\frac{\Delta\theta}{2\pi}\cdot\pi r^2 = \frac12 r^2\,\Delta\theta$."),
    Formula("Polar area", (r"The area of the region swept by $r = f(\theta)$ for $\alpha \le \theta \le \beta$ is \[ A = \blank{\frac12\int_\alpha^\beta r^2\,d\theta}. \]")),
    VideoExample('The area inside a cardioid', work="4.6cm"),
    Section("Choosing the limits"),
    Text(r"Find where the radius starts and stops sweeping the region, often where $r = 0$. Trace the curve so each piece is swept exactly once: $r = 4\sin\theta$ is traced once on $[0, \pi]$, not $[0, 2\pi]$."),
    FIG,
    Formula("Power-reducing identities", (r"$\cos^2\theta = \frac12(1 + \cos 2\theta)$, \quad $\sin^2\theta = \frac12(1 - \cos 2\theta)$.")),
    BigIdea(r"$A = \frac12\int r^2\,d\theta$, with limits that sweep the region exactly once."),
    Check(r"Find the area inside the circle $r = 3$ using the polar area formula.", selfcheck(r"9\pi"), r"$\frac12\int_0^{2\pi} 9\,d\theta$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Find the area inside $r = 2\cos\theta$.", num(parea(2 * sp.cos(th), -sp.pi / 2, sp.pi / 2), tol=1e-3), r"Traced once for $-\frac\pi2 \le \theta \le \frac\pi2$: $\frac12\int 4\cos^2\theta\,d\theta = \pi$.", work="1.8cm"),
    Item(r"Find the area inside $r = 2 + 2\sin\theta$.", num(parea(2 + 2 * sp.sin(th), 0, 2 * sp.pi), tol=1e-3), r"$\frac12\int_0^{2\pi} (2 + 2\sin\theta)^2\,d\theta = 6\pi$.", work="2cm"),
    Item(r"Find the area of one petal of $r = \cos 3\theta$.", num(parea(sp.cos(3 * th), -sp.pi / 6, sp.pi / 6), tol=1e-4), r"$-\frac\pi6 \le \theta \le \frac\pi6$: $\frac12\int \cos^2 3\theta\,d\theta = \frac{\pi}{12}$.", work="2cm"),
    Item(r"Find the area of the region swept by $r = e^{\theta}$ for $0 \le \theta \le 1$.", num(parea(sp.exp(th), 0, 1), tol=1e-3), r"$\frac12\int_0^1 e^{2\theta}\,d\theta = \frac{e^2 - 1}{4} \approx 1.597$.", work="1.6cm"),
    Item(r"Find the area of the region inside $r = \sqrt{\theta}$ for $0 \le \theta \le 2\pi$.", num(parea(sp.sqrt(th), 0, 2 * sp.pi), tol=1e-3), r"$\frac12\int_0^{2\pi} \theta\,d\theta = \pi^2$.", work="1.4cm"),
    Item(r"Write, but do not evaluate, an integral for the area of the region inside $r = 3 + \cos\theta$ in the first quadrant.", selfcheck(r"\tfrac12\int_0^{\pi/2} (3 + \cos\theta)^2\,d\theta"), r"First quadrant: $0 \le \theta \le \frac\pi2$.", work="1.2cm"),
    Item(r"Find the total area enclosed by the rose $r = \sin 2\theta$ (all four petals).", num(parea(sp.sin(2 * th), 0, 2 * sp.pi), tol=1e-3), r"$4 \cdot \frac\pi8 = \frac\pi2$.", work="1.4cm"),
    Item(r"Use a calculator to find the area inside $r = 2 + \sin(3\theta)$.", num(parea(2 + sp.sin(3 * th), 0, 2 * sp.pi), tol=1e-3), r"$\frac12\int_0^{2\pi} (2 + \sin 3\theta)^2\,d\theta = \frac{9\pi}{2} \approx 14.137$.", work="1.4cm", calc=True),
]
same("p", [parea(2 * sp.cos(th), -sp.pi / 2, sp.pi / 2), parea(2 + 2 * sp.sin(th), 0, 2 * sp.pi), parea(sp.cos(3 * th), -sp.pi / 6, sp.pi / 6), parea(2 + sp.sin(3 * th), 0, 2 * sp.pi)],
     [sp.pi, 6 * sp.pi, sp.pi / 12, 9 * sp.pi / 2])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"The area inside $r = f(\theta)$ for $\alpha \le \theta \le \beta$ is", [r"$\int_\alpha^\beta r\,d\theta$", r"$\frac12\int_\alpha^\beta r^2\,d\theta$", r"$\pi\int_\alpha^\beta r^2\,d\theta$", r"$\int_\alpha^\beta r^2\,d\theta$"], "B", r"Sectors of area $\frac12 r^2\,d\theta$."),
    ),
    Variants(
        Item(r"Find the area inside $r = 6\sin\theta$.", num(parea(6 * sp.sin(th), 0, sp.pi), tol=1e-3), r"$\frac12\int_0^\pi 36\sin^2\theta\,d\theta = 9\pi$.", work="1.6cm"),
        Item(r"Find the area inside $r = 4\cos\theta$.", num(parea(4 * sp.cos(th), -sp.pi / 2, sp.pi / 2), tol=1e-3), r"$4\pi$ (radius $2$).", work="1.6cm"),
    ),
    Variants(
        Item(r"Find the area inside $r = 1 - \cos\theta$.", num(parea(1 - sp.cos(th), 0, 2 * sp.pi), tol=1e-3), r"$\frac{3\pi}{2}$.", work="2cm"),
        Item(r"Find the area inside $r = 1 + \sin\theta$.", num(parea(1 + sp.sin(th), 0, 2 * sp.pi), tol=1e-3), r"$\frac{3\pi}{2}$.", work="2cm"),
    ),
    Variants(
        MCQ(r"Which limits give one petal of $r = \cos 2\theta$?", [r"$0 \le \theta \le \frac\pi2$", r"$0 \le \theta \le \pi$", r"$-\frac\pi4 \le \theta \le \frac\pi4$", r"$0 \le \theta \le \frac\pi4$"], "C", r"$\cos 2\theta = 0$ at $\pm\frac\pi4$, positive between.",
            why_not={"D": "half a petal"}),
        MCQ(r"Which limits give one petal of $r = \sin 3\theta$?", [r"$0 \le \theta \le \frac\pi3$", r"$0 \le \theta \le \frac\pi6$", r"$0 \le \theta \le \pi$", r"$0 \le \theta \le \frac{2\pi}{3}$"], "A", r"$\sin 3\theta = 0$ at $0$ and $\frac\pi3$."),
    ),
    Variants(
        Item(r"Find the area swept by $r = 2\theta$ for $0 \le \theta \le \pi$.", num(parea(2 * th, 0, sp.pi), tol=1e-2), r"$\frac12\int_0^\pi 4\theta^2\,d\theta = \frac{2\pi^3}{3}$.", work="1.4cm"),
        Item(r"Find the area swept by $r = \theta^2$ for $0 \le \theta \le 1$.", num(parea(th**2, 0, 1)), r"$\frac12\int_0^1 \theta^4\,d\theta = \frac{1}{10}$.", work="1.4cm"),
    ),
]

# ---------------------------------------------------------------- test prep
_m4 = float(parea(1 + sp.cos(th)**2, 0, sp.pi).evalf())
MCQS = [
    MCQ(r"The area of the region inside $r = 3\cos\theta$ is", [r"$\frac{9\pi}{4}$", r"$\frac{9\pi}{2}$", r"$9\pi$", r"$3\pi$"], "A", r"A circle of radius $\frac32$: $\frac12\int_{-\pi/2}^{\pi/2} 9\cos^2\theta\,d\theta = \frac{9\pi}{4}$.",
        why_not={"B": "integrated over $[0, 2\\pi]$, counting the circle twice"}),
    MCQ(r"The area of one petal of $r = 2\sin 2\theta$ is", [r"$\frac\pi8$", r"$\frac\pi4$", r"$\frac\pi2$", r"$\pi$"], "C", r"$\frac12\int_0^{\pi/2} 4\sin^2 2\theta\,d\theta = \frac\pi2$."),
    MCQ(r"Which gives the area of the region inside $r = 2 + \cos\theta$ for $0 \le \theta \le \pi$?", [r"$\int_0^\pi (2 + \cos\theta)\,d\theta$", r"$\frac12\int_0^\pi (2 + \cos\theta)\,d\theta$",
        r"$\pi\int_0^\pi (2 + \cos\theta)^2\,d\theta$", r"$\frac12\int_0^\pi (2 + \cos\theta)^2\,d\theta$"], "D", r"$\frac12\int r^2\,d\theta$."),
    MCQ(r"To three decimal places, the area of the region swept by $r = 1 + \cos^2\theta$ for $0 \le \theta \le \pi$ is", [r"$1.571$", r"$2.749$", rf"${_m4:.3f}$", r"$5.890$"], "C", rf"$\frac12\int_0^\pi (1 + \cos^2\theta)^2\,d\theta \approx {_m4:.3f}$.", calc=True),
]
close("m4", _m4, 3.731, 5e-4)
same("m", [parea(3 * sp.cos(th), -sp.pi / 2, sp.pi / 2), parea(2 * sp.sin(2 * th), 0, sp.pi / 2)], [9 * sp.pi / 4, sp.pi / 2])

FRQS = []

TOPIC = Topic(
    number="9.8", title="Find the Area of a Polar Region or the Area Bounded by a Single Polar Curve",
    unit="Unit 9: Parametric Equations, Polar Coordinates, and Vector-Valued Functions", ced=["CHA-5.D", "CHA-5.D.9"],
    goals=r"Find the area of a region bounded by a polar curve with $\frac12\int r^2\,d\theta$.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
