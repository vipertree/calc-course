"""Unit 9 test (BC): Parametric Equations, Polar Coordinates, and Vector-Valued Functions. AP format: 12 MCQ (no
calculator), 4 MCQ (calculator), 3 FRQ, two forms for every slot. Covers 9.1-9.9 (all BC).

Choices are built by `pick`, which puts the keyed answer at a planned letter. Every keyed value is checked with sympy.
"""
import sympy as sp

from calclib import FRQ, MCQ, Part, UnitTest, Variants, close, num, same, selfcheck
from calclib.figs import graph

t, th = sp.symbols("t theta", real=True)
NI = lambda f, a, b, v=t: float(sp.Integral(f, (v, a, b)).evalf())


def pick(stem, right, wrong, letter, solution, why=None, calc=False):
    k = "ABCD".index(letter)
    choices = list(wrong)
    choices.insert(k, right)
    why_not = {}
    if why:
        for text, reason in why.items():
            why_not["ABCD"[choices.index(text)]] = reason
    return MCQ(stem, choices, letter, solution, why_not=why_not, calc=calc)


def d1(xt, yt):
    return sp.simplify(sp.diff(yt, t) / sp.diff(xt, t))


def d2(xt, yt):
    return sp.simplify(sp.diff(d1(xt, yt), t) / sp.diff(xt, t))


def pslope(f):
    return sp.simplify(sp.diff(f * sp.sin(th), th) / sp.diff(f * sp.cos(th), th))


def parea(R, r, a, b):
    return sp.simplify(sp.integrate(R**2 - r**2, (th, a, b)) / 2)


# ---------------------------------------------------------------- part A
same("A1", [d1(t**2 + 1, t**3).subs(t, 1), d1(sp.exp(t), t**2).subs(t, 1)], [sp.Rational(3, 2), 2 / sp.E])
same("A3", [d2(t**2, t**3).subs(t, 1), d2(2 * t, t**3).subs(t, 2)], [sp.Rational(3, 4), 3])
same("A6", [sp.sqrt(3**2 + (2 * 2)**2), sp.sqrt(12**2 + 6**2)], [5, 6 * sp.sqrt(5)])
same("A11", [parea(2 * sp.cos(th), 0, -sp.pi / 2, sp.pi / 2), parea(sp.cos(2 * th), 0, -sp.pi / 4, sp.pi / 4)], [sp.pi, sp.pi / 8])

A = [
    Variants(
        pick(r"For $x = t^2 + 1$, $y = t^3$, $\frac{dy}{dx}$ at $t = 1$ is", r"$\frac32$", [r"$3$", r"$\frac23$", r"$6$"], "B", r"$\frac{3t^2}{2t}$ at $t = 1$.", {r"$\frac23$": "inverted the quotient"}),
        pick(r"For $x = e^t$, $y = t^2$, $\frac{dy}{dx}$ at $t = 1$ is", r"$\frac2e$", [r"$2e$", r"$\frac e2$", r"$2$"], "A", r"$\frac{2t}{e^t}$ at $t = 1$.", {r"$\frac e2$": "inverted the quotient"}),
    ),
    Variants(
        pick(r"The curve $x = t^2$, $y = t^3 - 3t$ has horizontal tangents at", r"$(1, -2)$ and $(1, 2)$", [r"$(0, 0)$", r"$(1, 0)$ only", r"$(3, 0)$ and $(0, 0)$"], "C", r"$\frac{dy}{dt} = 3t^2 - 3 = 0$ at $t = \pm1$."),
        pick(r"The curve $x = t^3 - 3t$, $y = t^2$ has vertical tangents at", r"$(-2, 1)$ and $(2, 1)$", [r"$(0, 0)$", r"$(0, 3)$", r"$(2, 1)$ only"], "C", r"$\frac{dx}{dt} = 3t^2 - 3 = 0$ at $t = \pm1$."),
    ),
    Variants(
        pick(r"For $x = t^2$, $y = t^3$, $\frac{d^2y}{dx^2}$ at $t = 1$ is", r"$\frac34$", [r"$3$", r"$\frac32$", r"$6$"], "D", r"$\frac{dy}{dx} = \frac32t$; $\frac{d}{dt} = \frac32$; $\div 2t$.", {r"$3$": "divided $\\frac{d^2y}{dt^2}$ by $\\frac{d^2x}{dt^2}$"}),
        pick(r"For $x = 2t$, $y = t^3$, $\frac{d^2y}{dx^2}$ at $t = 2$ is", r"$3$", [r"$6$", r"$12$", r"$\frac32$"], "D", r"$\frac{dy}{dx} = \frac{3t^2}{2}$; $\frac{d}{dt} = 3t$; $\div 2$: $\frac{3t}{2} = 3$.", {r"$6$": "forgot to divide by $\\frac{dx}{dt}$"}),
    ),
    Variants(
        pick(r"The length of the curve $x = t^2$, $y = t^3$, $0 \le t \le 1$, is", r"$\int_0^1 \sqrt{4t^2 + 9t^4}\,dt$", [r"$\int_0^1 \sqrt{t^4 + t^6}\,dt$", r"$\int_0^1 \left(2t + 3t^2\right) dt$", r"$\int_0^1 \sqrt{1 + \frac94 t^2}\,dt$"], "B",
             r"$\int \sqrt{(x')^2 + (y')^2}\,dt$.", {r"$\int_0^1 \sqrt{t^4 + t^6}\,dt$": "used $x$ and $y$, not their derivatives"}),
        pick(r"The length of the curve $x = e^t$, $y = e^{-t}$, $0 \le t \le 1$, is", r"$\int_0^1 \sqrt{e^{2t} + e^{-2t}}\,dt$", [r"$\int_0^1 \left(e^t - e^{-t}\right) dt$", r"$\int_0^1 \sqrt{1 + e^{-4t}}\,dt$", r"$\int_0^1 \sqrt{e^{t} + e^{-t}}\,dt$"], "B",
             r"$x' = e^t$, $y' = -e^{-t}$."),
    ),
    Variants(
        pick(r"The length of the path $x = 3t$, $y = 4t$, $0 \le t \le 2$, is", r"$10$", [r"$5$", r"$14$", r"$7$"], "C", r"Speed $5$ for $2$ units of time."),
        pick(r"The length of the path $x = 2\cos t$, $y = 2\sin t$, $0 \le t \le \pi$, is", r"$2\pi$", [r"$\pi$", r"$4\pi$", r"$4$"], "A", r"Half a circle of radius $2$."),
    ),
    Variants(
        pick(r"A particle has $\vec r(t) = \langle 3t,\ t^2\rangle$. Its speed at $t = 2$ is", r"$5$", [r"$7$", r"$\sqrt{13}$", r"$25$"], "D", r"$\vec v(2) = \langle 3, 4\rangle$."),
        pick(r"A particle has $\vec r(t) = \langle t^3,\ 6t\rangle$. Its speed at $t = 2$ is", r"$6\sqrt5$", [r"$18$", r"$\sqrt{72}$", r"$12$"], "B", r"$\vec v(2) = \langle 12, 6\rangle$: $\sqrt{180}$."),
    ),
    Variants(
        pick(r"If $\vec r(t) = \langle e^{2t},\ t^3\rangle$, then $\vec a(0) = $", r"$\langle 4, 0\rangle$", [r"$\langle 2, 0\rangle$", r"$\langle 1, 0\rangle$", r"$\langle 4, 6\rangle$"], "A", r"$\vec a = \langle 4e^{2t}, 6t\rangle$.", {r"$\langle 2, 0\rangle$": "that is $\\vec v(0)$"}),
        pick(r"If $\vec r(t) = \langle \ln(t + 1),\ t^2\rangle$, then $\vec a(0) = $", r"$\langle -1, 2\rangle$", [r"$\langle 1, 0\rangle$", r"$\langle 1, 2\rangle$", r"$\langle 0, 2\rangle$"], "C", r"$\vec a = \left\langle -\frac{1}{(t + 1)^2}, 2\right\rangle$.", {r"$\langle 1, 0\rangle$": "that is $\\vec v(0)$"}),
    ),
    Variants(
        pick(r"A particle has $\vec v(t) = \langle 2t,\ 1\rangle$ and $\vec r(0) = \langle 1, 3\rangle$. Then $\vec r(2) = $", r"$\langle 5, 5\rangle$", [r"$\langle 4, 2\rangle$", r"$\langle 5, 3\rangle$", r"$\langle 4, 5\rangle$"], "A", r"$\langle 1, 3\rangle + \langle 4, 2\rangle$.", {r"$\langle 4, 2\rangle$": "the displacement only"}),
        pick(r"A particle has $\vec v(t) = \langle 3t^2,\ 2t\rangle$ and $\vec r(1) = \langle 0, 0\rangle$. Then $\vec r(2) = $", r"$\langle 7, 3\rangle$", [r"$\langle 8, 4\rangle$", r"$\langle 12, 4\rangle$", r"$\langle 6, 2\rangle$"], "D", r"$\int_1^2 \langle 3t^2, 2t\rangle\,dt = \langle 7, 3\rangle$."),
    ),
    Variants(
        pick(r"A particle has $x'(t) = t^2 - 4t$ and $y'(t) = t + 1$. For which $t > 0$ is it moving to the left?", r"$0 < t < 4$", [r"$t > 4$", r"$t > 0$", r"$0 < t < 2$"], "B", r"$x' < 0$ on $(0, 4)$."),
        pick(r"A particle has $x'(t) = t + 1$ and $y'(t) = 2t - 6$. For which $t > 0$ is it moving down?", r"$0 < t < 3$", [r"$t > 3$", r"$t > 0$", r"$0 < t < 6$"], "C", r"$y' < 0$ on $(0, 3)$."),
    ),
    Variants(
        pick(r"The polar curve $r = 4\cos\theta$ is the circle", r"$(x - 2)^2 + y^2 = 4$", [r"$x^2 + y^2 = 16$", r"$x^2 + (y - 2)^2 = 4$", r"$(x - 4)^2 + y^2 = 16$"], "D", r"$x^2 + y^2 = 4x$."),
        pick(r"The polar curve $r = 2\sin\theta$ is the circle", r"$x^2 + (y - 1)^2 = 1$", [r"$x^2 + y^2 = 4$", r"$(x - 1)^2 + y^2 = 1$", r"$x^2 + (y - 2)^2 = 4$"], "B", r"$x^2 + y^2 = 2y$."),
    ),
    Variants(
        pick(r"The area of the region inside $r = 2\cos\theta$ is", r"$\pi$", [r"$2\pi$", r"$4\pi$", r"$\frac\pi2$"], "A", r"A circle of radius $1$.", {r"$2\pi$": "integrated over $[0, 2\\pi]$, counting it twice"}),
        pick(r"The area of one petal of $r = \cos 2\theta$ is", r"$\frac\pi8$", [r"$\frac\pi4$", r"$\frac\pi2$", r"$\frac{\pi}{16}$"], "D", r"$\frac12\int_{-\pi/4}^{\pi/4} \cos^2 2\theta\,d\theta$."),
    ),
    Variants(
        pick(r"Which gives the area inside $r = 2$ and outside $r = 2 - 2\cos\theta$?", r"$\frac12\int_{-\pi/2}^{\pi/2} \left(4 - (2 - 2\cos\theta)^2\right) d\theta$", [r"$\frac12\int_{-\pi/2}^{\pi/2} (2\cos\theta)^2\,d\theta$",
             r"$\frac12\int_0^{2\pi} \left(4 - (2 - 2\cos\theta)^2\right) d\theta$", r"$\int_{-\pi/2}^{\pi/2} \left(4 - (2 - 2\cos\theta)^2\right) d\theta$"], "C", r"They meet where $\cos\theta = 0$; $r = 2$ is outer for $|\theta| < \frac\pi2$.",
             {r"$\frac12\int_{-\pi/2}^{\pi/2} (2\cos\theta)^2\,d\theta$": "squared the difference of the radii"}),
        pick(r"Which gives the area inside $r = 3\sin\theta$ and outside $r = 1 + \sin\theta$?", r"$\frac12\int_{\pi/6}^{5\pi/6} \left(9\sin^2\theta - (1 + \sin\theta)^2\right) d\theta$", [r"$\frac12\int_{\pi/6}^{5\pi/6} (2\sin\theta - 1)^2\,d\theta$",
             r"$\frac12\int_0^\pi \left(9\sin^2\theta - (1 + \sin\theta)^2\right) d\theta$", r"$\int_{\pi/6}^{5\pi/6} (2\sin\theta - 1)\,d\theta$"], "A", r"They meet where $\sin\theta = \frac12$.",
             {r"$\frac12\int_{\pi/6}^{5\pi/6} (2\sin\theta - 1)^2\,d\theta$": "squared the difference of the radii"}),
    ),
]

# ---------------------------------------------------------------- part B: calculator
b1a = NI(sp.sqrt(sp.cos(t**2)**2 + sp.exp(t)), 0, 2)
b1b = NI(sp.sqrt(t + sp.cos(t)**2), 0, 3)
b2a = 1 + NI(sp.sin(t**2), 0, 1)
b2b = float(pslope(th + sp.sin(th)).subs(th, 2).evalf())
b3a = float(parea(2 + sp.sin(3 * th), 0, 0, 2 * sp.pi))
b3b = float(parea(1 + sp.cos(th)**2, 0, 0, sp.pi))
b4a = NI(sp.sqrt(4 * t**2 + 9 * t**4), 0, 1)
b4b = NI(sp.sqrt(sp.exp(2 * t) + 1), 0, 1)
for name, v, key in (("b1a", b1a, 3.828), ("b1b", b1b, 4.121), ("b2a", b2a, 1.310), ("b2b", b2b, 0.235), ("b3a", b3a, 14.137), ("b3b", b3b, 3.731), ("b4a", b4a, 1.440), ("b4b", b4b, 2.003)):
    close(name, v, key, 5e-4)
f3 = lambda v: f"${v:.3f}$"

B = [
    Variants(
        pick(r"A particle has $x'(t) = \cos(t^2)$ and $y'(t) = e^{t/2}$. The distance it travels for $0 \le t \le 2$ is", f3(b1a), [f3(NI(sp.cos(t**2), 0, 2) + NI(sp.exp(t / 2), 0, 2)), r"$2.000$", f3(2 * b1a)], "B",
             rf"$\int_0^2 \sqrt{{\cos^2(t^2) + e^t}}\,dt \approx {b1a:.3f}$.", calc=True),
        pick(r"A particle has $x'(t) = \sqrt t$ and $y'(t) = \cos t$. The distance it travels for $0 \le t \le 3$ is", f3(b1b), [r"$3.464$", f3(b1b / 2), r"$5.196$"], "D", rf"$\int_0^3 \sqrt{{t + \cos^2 t}}\,dt \approx {b1b:.3f}$.", calc=True),
    ),
    Variants(
        pick(r"A particle has $x'(t) = \sin(t^2)$ and is at $x = 1$ when $t = 0$. Its $x$-coordinate at $t = 1$ is", f3(b2a), [f3(b2a - 1), f3(1 + float(sp.sin(1))), r"$1.500$"], "A", rf"$1 + \int_0^1 \sin(t^2)\,dt \approx {b2a:.3f}$.", {f3(b2a - 1): "the change only"}, calc=True),
        pick(r"The slope of the polar curve $r = \theta + \sin\theta$ at $\theta = 2$ is", f3(b2b), [f3(float(1 + sp.cos(2))), r"$-1.416$", r"$2.909$"], "C", rf"$\frac{{dy/d\theta}}{{dx/d\theta}} \approx {b2b:.3f}$.", {f3(float(1 + sp.cos(2))): "that is $\\frac{dr}{d\\theta}$"}, calc=True),
    ),
    Variants(
        pick(r"The area of the region inside $r = 2 + \sin 3\theta$ is", f3(b3a), [f3(2 * b3a), f3(b3a / 3), f3(4 * float(sp.pi))], "D", rf"$\frac12\int_0^{{2\pi}} (2 + \sin 3\theta)^2\,d\theta \approx {b3a:.3f}$.", calc=True),
        pick(r"The area of the region swept by $r = 1 + \cos^2\theta$ for $0 \le \theta \le \pi$ is", f3(b3b), [f3(2 * b3b), r"$1.571$", r"$5.890$"], "B", rf"$\frac12\int_0^\pi (1 + \cos^2\theta)^2\,d\theta \approx {b3b:.3f}$.", calc=True),
    ),
    Variants(
        pick(r"The length of the curve $x = t^2$, $y = t^3$ for $0 \le t \le 1$ is", f3(b4a), [r"$1.414$", f3(b4a / 2), r"$2.500$"], "C", rf"$\int_0^1 \sqrt{{4t^2 + 9t^4}}\,dt \approx {b4a:.3f}$.", {r"$1.414$": "the straight-line distance"}, calc=True),
        pick(r"The length of the curve $x = e^t$, $y = t$ for $0 \le t \le 1$ is", f3(b4b), [r"$1.718$", r"$1.988$", f3(2 * b4b)], "A", rf"$\int_0^1 \sqrt{{e^{{2t}} + 1}}\,dt \approx {b4b:.3f}$.", calc=True),
    ),
]

# ---------------------------------------------------------------- FRQ 1: plane motion (calculator)
xA, yA = 2 + sp.sin(t**2), 3 * sp.exp(-t / 2)
sA1 = float(sp.sqrt(xA**2 + yA**2).subs(t, 1).evalf())
aA1 = [float(sp.diff(xA, t).subs(t, 1)), float(sp.diff(yA, t).subs(t, 1))]
pA = (0 + NI(xA, 0, 2), 1 + NI(yA, 0, 2))
dA = NI(sp.sqrt(xA**2 + yA**2), 0, 2)
mA = float((yA / xA).subs(t, 1))
xB, yB = t * sp.sin(t), 2 - t
sB1 = float(sp.sqrt(xB**2 + yB**2).subs(t, 1).evalf())
aB1 = [float(sp.diff(xB, t).subs(t, 1)), float(sp.diff(yB, t).subs(t, 1))]
pB = (1 + NI(xB, 0, 3), 0 + NI(yB, 0, 3))
dB = NI(sp.sqrt(xB**2 + yB**2), 0, 3)


def motion_frq(xp, yp, xs, ys, start, s1, a1, pos, b, dist, d_part, d_sol):
    return FRQ("Motion in the plane", (rf"A particle moves in the $xy$-plane so that $\frac{{dx}}{{dt}} = {xs}$ and $\frac{{dy}}{{dt}} = {ys}$ for $t \ge 0$. At $t = 0$ the particle is at ${start}$."), [
        Part("a", r"Find the speed of the particle and its acceleration vector at $t = 1$.", selfcheck(rf"{s1:.3f};\ \langle {a1[0]:.3f},\ {a1[1]:.3f}\rangle"),
             rf"Speed $= \sqrt{{x'(1)^2 + y'(1)^2}} \approx {s1:.3f}$. $\vec a(1) = \langle x''(1), y''(1)\rangle \approx \langle {a1[0]:.3f}, {a1[1]:.3f}\rangle$.", [(1, "speed"), (1, "acceleration vector")], work="2.4cm"),
        Part("b", rf"Find the position of the particle at $t = {b}$.", selfcheck(rf"({pos[0]:.3f},\ {pos[1]:.3f})"),
             rf"$x({b}) = x(0) + \int_0^{{{b}}} x'(t)\,dt \approx {pos[0]:.3f}$; $y({b}) = y(0) + \int_0^{{{b}}} y'(t)\,dt \approx {pos[1]:.3f}$.", [(1, "$x$-coordinate"), (1, "$y$-coordinate")], work="2.4cm"),
        Part("c", rf"Find the total distance traveled by the particle for $0 \le t \le {b}$.", num(sp.Float(round(dist, 4)), tol=2e-3), rf"$\int_0^{{{b}}} \sqrt{{x'(t)^2 + y'(t)^2}}\,dt \approx {dist:.3f}$.", [(1, "integral"), (1, "answer")], work="1.8cm"),
        Part("d", d_part, selfcheck(d_sol[0]), d_sol[1], [(1, "answer with reason")], work="1.8cm"),
    ], frq_type="Parametric / vector motion", calc=True)


F1A = motion_frq(xA, yA, r"2 + \sin(t^2)", r"3e^{-t/2}", r"(0, 1)", sA1, aA1, pA, 2, dA, r"Find the slope of the line tangent to the path of the particle at $t = 1$.",
                 (rf"{mA:.3f}", rf"$\frac{{dy}}{{dx}} = \frac{{y'(1)}}{{x'(1)}} = \frac{{3e^{{-1/2}}}}{{2 + \sin 1}} \approx {mA:.3f}$."))
F1B = motion_frq(xB, yB, r"t\sin t", r"2 - t", r"(1, 0)", sB1, aB1, pB, 3, dB, r"For $0 < t < 3$, when is the particle moving to the left? Give a reason.",
                 (r"\text{never}", r"$x'(t) = t\sin t > 0$ for $0 < t < 3$ (since $0 < t < \pi$), so the particle is never moving left on this interval."))

# ---------------------------------------------------------------- FRQ 2: polar
same("F2A", [parea(3 * sp.sin(th), 1 + sp.sin(th), sp.pi / 6, 5 * sp.pi / 6), sp.simplify(pslope(3 * sp.sin(th)).subs(th, sp.pi / 3)), sp.diff(1 + sp.sin(th), th).subs(th, sp.pi / 3) * 2], [sp.pi, -sp.sqrt(3), 1])
same("F2B", [parea(2 * sp.cos(th), 1, -sp.pi / 3, sp.pi / 3), sp.simplify(pslope(2 * sp.cos(th)).subs(th, sp.pi / 6)), sp.diff(2 * sp.cos(th), th).subs(th, sp.pi / 6) * 3], [sp.pi / 3 + sp.sqrt(3) / 2, -1 / sp.sqrt(3), -3])
FIG2A = graph("tU9_2a", [], (-2, 2), (-0.4, 3.4), w="5cm", h="5cm",
              extra=r"\addplot[fn, domain=0:180, samples=200, variable=\t]({3*sin(\t)*cos(\t)},{3*sin(\t)*sin(\t)});\addplot[fn2, domain=0:360, samples=200, variable=\t]({(1+sin(\t))*cos(\t)},{(1+sin(\t))*sin(\t)});",
              caption=r"$r = 3\sin\theta$ (solid) and $r = 1 + \sin\theta$ (dashed).")
FIG2B = graph("tU9_2b", [], (-1.4, 2.4), (-1.4, 1.4), w="5.4cm", h="4.2cm",
              extra=r"\addplot[fn, domain=-90:90, samples=200, variable=\t]({2*cos(\t)*cos(\t)},{2*cos(\t)*sin(\t)});\addplot[fn2, domain=0:360, samples=200, variable=\t]({cos(\t)},{sin(\t)});",
              caption=r"$r = 2\cos\theta$ (solid) and $r = 1$ (dashed).")
F2A = FRQ("Two polar curves", (r"The polar curves $r = 3\sin\theta$ and $r = 1 + \sin\theta$ are shown for $0 \le \theta \le \pi$."), [
    Part("a", r"Find the values of $\theta$, $0 \le \theta \le \pi$, at which the curves intersect.", selfcheck(r"\theta = \tfrac\pi6,\ \tfrac{5\pi}{6}"), r"$3\sin\theta = 1 + \sin\theta$: $\sin\theta = \frac12$.", [(1, "both values")], work="1.6cm"),
    Part("b", r"Find the area of the region inside $r = 3\sin\theta$ and outside $r = 1 + \sin\theta$.", num(sp.pi, tol=1e-3, display=r"\pi"),
         r"$\frac12\int_{\pi/6}^{5\pi/6} \left(9\sin^2\theta - (1 + \sin\theta)^2\right) d\theta = \frac12\int_{\pi/6}^{5\pi/6} \left(8\sin^2\theta - 2\sin\theta - 1\right) d\theta = \pi$.",
         [(1, "limits and constant"), (1, "integrand"), (1, "answer")], work="3.2cm"),
    Part("c", r"Find the slope of the line tangent to $r = 3\sin\theta$ at $\theta = \frac\pi3$.", num(-sp.sqrt(3), tol=1e-3, display=r"-\sqrt3"),
         r"$x = 3\sin\theta\cos\theta = \frac32\sin 2\theta$, $y = 3\sin^2\theta$. $\frac{dy}{dx} = \frac{3\sin 2\theta}{3\cos 2\theta} = \tan\frac{2\pi}{3} = -\sqrt3$.", [(1, "derivatives"), (1, "slope")], work="2.4cm"),
    Part("d", r"A particle moves along $r = 1 + \sin\theta$ with $\frac{d\theta}{dt} = 2$. Find $\frac{dr}{dt}$ at $\theta = \frac\pi3$, and say whether the particle is moving toward or away from the origin.", selfcheck(r"1;\ \text{away}"),
         r"$\frac{dr}{dt} = \cos\theta \cdot \frac{d\theta}{dt} = \frac12 \cdot 2 = 1 > 0$, with $r > 0$: moving away from the origin.", [(1, "chain rule and value"), (1, "away, with reason")], work="2cm"),
], frq_type="Polar", figure=FIG2A)
F2B = FRQ("Two polar curves", (r"The polar curves $r = 2\cos\theta$ and $r = 1$ are shown."), [
    Part("a", r"Find the values of $\theta$, $-\frac\pi2 \le \theta \le \frac\pi2$, at which the curves intersect.", selfcheck(r"\theta = \pm\tfrac\pi3"), r"$2\cos\theta = 1$: $\cos\theta = \frac12$.", [(1, "both values")], work="1.6cm"),
    Part("b", r"Find the area of the region inside $r = 2\cos\theta$ and outside $r = 1$.", num(sp.pi / 3 + sp.sqrt(3) / 2, tol=1e-3, display=r"\tfrac\pi3 + \tfrac{\sqrt3}{2}"),
         r"$\frac12\int_{-\pi/3}^{\pi/3} \left(4\cos^2\theta - 1\right) d\theta = \frac12\int_{-\pi/3}^{\pi/3} (1 + 2\cos 2\theta)\,d\theta = \frac\pi3 + \frac{\sqrt3}{2}$.", [(1, "limits and constant"), (1, "integrand"), (1, "answer")], work="3.2cm"),
    Part("c", r"Find the slope of the line tangent to $r = 2\cos\theta$ at $\theta = \frac\pi6$.", num(-1 / sp.sqrt(3), tol=1e-3, display=r"-\tfrac{1}{\sqrt3}"),
         r"$x = 2\cos^2\theta$, $y = 2\sin\theta\cos\theta = \sin 2\theta$. $\frac{dy}{dx} = \frac{2\cos 2\theta}{-2\sin 2\theta} = -\cot\frac\pi3 = -\frac{1}{\sqrt3}$.", [(1, "derivatives"), (1, "slope")], work="2.4cm"),
    Part("d", r"A particle moves along $r = 2\cos\theta$ with $\frac{d\theta}{dt} = 3$. Find $\frac{dr}{dt}$ at $\theta = \frac\pi6$, and say whether the particle is moving toward or away from the origin.", selfcheck(r"-3;\ \text{toward}"),
         r"$\frac{dr}{dt} = -2\sin\theta\cdot 3 = -3 < 0$, with $r = \sqrt3 > 0$: moving toward the origin.", [(1, "chain rule and value"), (1, "toward, with reason")], work="2cm"),
], frq_type="Polar", figure=FIG2B)

# ---------------------------------------------------------------- FRQ 3: a parametric curve (no calculator)
x3, y3 = t**2 - 1, t**3 - 3 * t
same("F3A", [d1(x3, y3).subs(t, 2), d2(x3, y3).subs(t, 2), [(x3.subs(t, s), y3.subs(t, s)) for s in (-1, 1)]], [sp.Rational(9, 4), sp.Rational(15, 32), [(0, 2), (0, -2)]])
x4, y4 = t**2, sp.Rational(2, 3) * t**3
same("F3B", [d1(x4, y4), d2(x4, y4).subs(t, 1), sp.integrate(2 * t * sp.sqrt(1 + t**2), (t, 0, sp.sqrt(3))), y4.subs(t, 2)], [t, sp.Rational(1, 2), sp.Rational(14, 3), sp.Rational(16, 3)])
F3A = FRQ("A parametric curve", (r"A curve is defined by $x = t^2 - 1$ and $y = t^3 - 3t$ for all real $t$."), [
    Part("a", r"Find $\frac{dy}{dx}$ in terms of $t$, and write an equation of the line tangent to the curve at $t = 2$.", selfcheck(r"\frac{3t^2 - 3}{2t};\ y - 2 = \tfrac94(x - 3)"),
         r"$\frac{dy}{dx} = \frac{3t^2 - 3}{2t}$. At $t = 2$: slope $\frac94$, point $(3, 2)$: $y - 2 = \frac94(x - 3)$.", [(1, "$\\frac{dy}{dx}$"), (1, "tangent line")], work="2.4cm"),
    Part("b", r"Find the points on the curve where the tangent line is horizontal.", selfcheck(r"(0, 2) \text{ and } (0, -2)"), r"$\frac{dy}{dt} = 3t^2 - 3 = 0$ at $t = \pm1$, where $\frac{dx}{dt} = \pm2 \ne 0$: $(0, 2)$ at $t = -1$ and $(0, -2)$ at $t = 1$.",
         [(1, "values of $t$"), (1, "points")], work="2cm"),
    Part("c", r"Find $\frac{d^2y}{dx^2}$ at $t = 2$. Is the curve concave up or concave down there?", selfcheck(r"\tfrac{15}{32};\ \text{concave up}"),
         r"$\frac{dy}{dx} = \frac32t - \frac32t^{-1}$; $\frac{d}{dt} = \frac32 + \frac32t^{-2}$; $\div 2t$: $\frac{3t^2 + 3}{4t^3} = \frac{15}{32} > 0$ at $t = 2$: concave up.", [(1, "method"), (1, "value and concavity")], work="2.4cm"),
    Part("d", r"Write, but do not evaluate, an integral expression for the length of the curve from $t = 0$ to $t = 2$.", selfcheck(r"\int_0^2 \sqrt{4t^2 + (3t^2 - 3)^2}\,dt"), r"$\int_0^2 \sqrt{(2t)^2 + (3t^2 - 3)^2}\,dt$.", [(1, "integral")], work="1.4cm"),
], frq_type="Parametric")
F3B = FRQ("A parametric curve", (r"A curve is defined by $x = t^2$ and $y = \frac23 t^3$ for $t \ge 0$."), [
    Part("a", r"Find $\frac{dy}{dx}$ in terms of $t$, and write an equation of the line tangent to the curve at $t = 1$.", selfcheck(r"t;\ y - \tfrac23 = x - 1"), r"$\frac{dy}{dx} = \frac{2t^2}{2t} = t$. At $t = 1$: slope $1$, point $\left(1, \frac23\right)$.", [(1, "$\\frac{dy}{dx}$"), (1, "tangent line")], work="2.2cm"),
    Part("b", r"Find $\frac{d^2y}{dx^2}$ at $t = 1$.", num(sp.Rational(1, 2)), r"$\frac{d}{dt}(t) = 1$; $\div 2t$: $\frac{1}{2t} = \frac12$.", [(1, "answer")], work="1.6cm"),
    Part("c", r"Find the length of the curve from $t = 0$ to $t = \sqrt3$.", num(sp.Rational(14, 3)),
         r"$\sqrt{(2t)^2 + (2t^2)^2} = 2t\sqrt{1 + t^2}$; $\int_0^{\sqrt3} 2t\sqrt{1 + t^2}\,dt = \frac23(8 - 1) = \frac{14}{3}$.", [(1, "integrand"), (1, "antiderivative"), (1, "answer")], work="3cm"),
    Part("d", r"Find the point on the curve where the slope of the tangent line is $2$.", selfcheck(r"\left(4,\ \tfrac{16}{3}\right)"), r"$t = 2$: $\left(4, \frac{16}{3}\right)$.", [(1, "point")], work="1.4cm"),
], frq_type="Parametric")

TEST = UnitTest(unit=9, title="Parametric Equations, Polar Coordinates, and Vector-Valued Functions", mcq_a=A, mcq_b=B,
                frq=[Variants(F1A, F1B), Variants(F2A, F2B), Variants(F3A, F3B)])
