"""Unit 4 test: Contextual Applications of Differentiation. AP format: 12 MCQ (no calculator), 4 MCQ (calculator), 3 FRQ.
Two forms (A and B) for every slot.

Covers 4.1-4.7. Choices are built by `pick`, which puts the keyed answer at a planned letter, so a key can't drift from its
choices. Every keyed value is checked with sympy.
"""
import sympy as sp

from calclib import FRQ, MCQ, Part, UnitTest, Variants, close, expr, num, same, selfcheck

x, t = sp.symbols("x t")
pi = sp.pi


def pick(stem, right, wrong, letter, solution, why=None, calc=False):
    """MCQ with the correct choice placed at `letter`. `wrong` is three distractors, keyed by why-text if given."""
    k = "ABCD".index(letter)
    choices = list(wrong)
    choices.insert(k, right)
    why_not = {}
    if why:
        for text, reason in why.items():
            why_not["ABCD"[choices.index(text)]] = reason
    return MCQ(stem, choices, letter, solution, why_not=why_not, calc=calc)


def dist(xf, a, b):
    """Total distance traveled by position xf(t) on [a, b]."""
    v = sp.diff(xf, t)
    pts = [a] + sorted(r for r in sp.solve(v, t) if r.is_real and a < r < b) + [b]
    return sum(abs(xf.subs(t, q) - xf.subs(t, p)) for p, q in zip(pts, pts[1:]))


def lin(f, a, at):
    return f.subs(x, a) + sp.diff(f, x).subs(x, a) * (at - a)


A = [
    Variants(
        pick(r"$V(t)$ is the volume of water in a pool, in gallons, $t$ hours after noon. What does $V'(3) = -40$ mean?",
             r"At 3 p.m., the volume is decreasing at 40 gallons per hour.", [r"At 3 p.m., the pool holds $-40$ gallons.",
             r"Between noon and 3 p.m., the pool lost 40 gallons.", r"At 3 p.m., the volume is decreasing at 40 hours per gallon."], "A",
             r"A derivative is a rate at an instant, in output units per input unit.", {r"Between noon and 3 p.m., the pool lost 40 gallons.": "that's an average over an interval"}),
        pick(r"$T(m)$ is the temperature of an oven, in $^\circ$F, $m$ minutes after it is switched on. What does $T'(10) = 15$ mean?",
             r"At 10 minutes, the temperature is rising at $15^\circ$F per minute.", [r"At 10 minutes, the temperature is $15^\circ$F.",
             r"In the first 10 minutes, the temperature rose $15^\circ$F.", r"It takes 15 minutes to rise $10^\circ$F."], "B",
             r"A derivative is a rate at an instant, in output units per input unit.", {r"In the first 10 minutes, the temperature rose $15^\circ$F.": "that's an average over an interval"}),
    ),
    Variants(
        pick(r"A particle moves with position $x(t) = t^3 - 3t^2 - 9t + 2$ for $t \ge 0$. At what time is it at rest?", r"$t = 3$",
             [r"$t = 1$", r"$t = 0$", r"$t = 9$"], "C", r"$v(t) = 3t^2 - 6t - 9 = 3(t - 3)(t + 1) = 0$ at $t = 3$.", {r"$t = 1$": "that's where $a = 0$"}),
        pick(r"A particle moves with position $x(t) = t^3 - 12t + 1$ for $t \ge 0$. At what time is it at rest?", r"$t = 2$",
             [r"$t = 0$", r"$t = 12$", r"$t = 4$"], "A", r"$v(t) = 3t^2 - 12 = 0$ at $t = 2$.", {r"$t = 0$": "that's where $a = 0$"}),
    ),
    Variants(
        pick(r"A particle's velocity is $v(t) = t^2 - 4t + 3$. At $t = 2.5$, the particle is", r"slowing down",
             [r"speeding up", r"at rest", r"moving right"], "D", r"$v(2.5) = -0.75 < 0$ and $a(2.5) = 2(2.5) - 4 = 1 > 0$: opposite signs.",
             {r"speeding up": "$v$ and $a$ have opposite signs", r"moving right": "$v < 0$ means moving left"}),
        pick(r"A particle's velocity is $v(t) = t^2 - 6t + 8$. At $t = 5$, the particle is", r"speeding up",
             [r"slowing down", r"at rest", r"moving left"], "C", r"$v(5) = 3 > 0$ and $a(5) = 2(5) - 6 = 4 > 0$: same signs.",
             {r"moving left": "$v > 0$ means moving right"}),
    ),
    Variants(
        pick(r"A particle moves with position $x(t) = t^2 - 4t$. What is the total distance it travels from $t = 0$ to $t = 5$?", r"$13$",
             [r"$5$", r"$9$", r"$4$"], "B", r"It turns at $t = 2$: $x(0) = 0$, $x(2) = -4$, $x(5) = 5$. Distance $4 + 9 = 13$.", {r"$5$": "that's the displacement"}),
        pick(r"A particle moves with position $x(t) = t^2 - 6t$. What is the total distance it travels from $t = 0$ to $t = 8$?", r"$34$",
             [r"$16$", r"$25$", r"$9$"], "D", r"It turns at $t = 3$: $x(0) = 0$, $x(3) = -9$, $x(8) = 16$. Distance $9 + 25 = 34$.", {r"$16$": "that's the displacement"}),
    ),
    Variants(
        pick(r"The radius of a circle grows at $3$ cm/s. How fast is its area growing when $r = 5$ cm?", r"$30\pi$ cm$^2$/s",
             [r"$10\pi$ cm$^2$/s", r"$25\pi$ cm$^2$/s", r"$6\pi$ cm$^2$/s"], "D", r"$\dfrac{dA}{dt} = 2\pi r\dfrac{dr}{dt} = 2\pi(5)(3)$.",
             {r"$10\pi$ cm$^2$/s": "forgot $\\frac{dr}{dt}$", r"$25\pi$ cm$^2$/s": "that's the area"}),
        pick(r"The radius of a sphere grows at $1$ cm/s. How fast is its volume growing when $r = 2$ cm?", r"$16\pi$ cm$^3$/s",
             [r"$\frac{32}{3}\pi$ cm$^3$/s", r"$4\pi$ cm$^3$/s", r"$8\pi$ cm$^3$/s"], "A", r"$\dfrac{dV}{dt} = 4\pi r^2\dfrac{dr}{dt} = 4\pi(4)(1)$.",
             {r"$\frac{32}{3}\pi$ cm$^3$/s": "that's the volume"}),
    ),
    Variants(
        pick(r"$x$ and $y$ are functions of $t$ with $x^2 + y^2 = 25$. When $x = 3$ and $y = 4$, $\dfrac{dx}{dt} = 4$. Then $\dfrac{dy}{dt} =$", r"$-3$",
             [r"$3$", r"$-\frac{16}{3}$", r"$-4$"], "A", r"$2(3)(4) + 2(4)\dfrac{dy}{dt} = 0$, so $\dfrac{dy}{dt} = -3$.", {r"$3$": "lost the sign"}),
        pick(r"$x$ and $y$ are functions of $t$ with $x^2 + y^2 = 100$. When $x = 6$ and $y = 8$, $\dfrac{dx}{dt} = 2$. Then $\dfrac{dy}{dt} =$", r"$-\frac32$",
             [r"$\frac32$", r"$-\frac83$", r"$-2$"], "B", r"$2(6)(2) + 2(8)\dfrac{dy}{dt} = 0$, so $\dfrac{dy}{dt} = -\frac32$.", {r"$\frac32$": "lost the sign"}),
    ),
    Variants(
        pick(r"Using the line tangent to $y = \sqrt x$ at $x = 16$, the approximation of $\sqrt{16.4}$ is", r"$4.05$",
             [r"$4.1$", r"$4.4$", r"$4.025$"], "B", r"$4 + \frac18(0.4) = 4.05$.", {r"$4.1$": "used slope $\\frac14$"}),
        pick(r"Using the line tangent to $y = \sqrt[3]{x}$ at $x = 27$, the approximation of $\sqrt[3]{27.54}$ is", r"$3.02$",
             [r"$3.18$", r"$3.54$", r"$3.06$"], "A", r"$3 + \frac{1}{27}(0.54) = 3.02$.", {r"$3.18$": "used slope $\\frac13$"}),
    ),
    Variants(
        pick(r"$f(1) = 3$ and $f'(1) = -2$. Using the line tangent to the graph of $f$ at $x = 1$, $f(1.2) \approx$", r"$2.6$",
             [r"$3.4$", r"$2.8$", r"$-0.4$"], "C", r"$3 + (-2)(0.2) = 2.6$.", {r"$3.4$": "lost the sign", r"$-0.4$": "that's only the change"}),
        pick(r"$f(4) = -1$ and $f'(4) = 5$. Using the line tangent to the graph of $f$ at $x = 4$, $f(3.9) \approx$", r"$-1.5$",
             [r"$-0.5$", r"$0.5$", r"$-0.9$"], "D", r"$-1 + 5(-0.1) = -1.5$.", {r"$-0.5$": "moved the wrong way"}),
    ),
    Variants(
        pick(r"\[ \lim_{x \to 0} \frac{e^{2x} - 1}{\sin x} = \]", r"$2$", [r"$0$", r"$1$", r"Does not exist"], "A",
             r"$\frac00$; \[ \lim_{x \to 0} \frac{2e^{2x}}{\cos x} = 2. \]", {r"$1$": "forgot the chain rule on $e^{2x}$"}),
        pick(r"\[ \lim_{x \to 0} \frac{\sin(5x)}{2x} = \]", r"$\frac52$", [r"$\frac25$", r"$5$", r"$0$"], "C",
             r"$\frac00$; \[ \lim_{x \to 0} \frac{5\cos(5x)}{2} = \frac52. \]", {r"$\frac25$": "inverted"}),
    ),
    Variants(
        pick(r"\[ \lim_{x \to \infty} \frac{2x^2 - 1}{5x^2 + 3x} = \]", r"$\frac25$", [r"$0$", r"$\infty$", r"$\frac43$"], "B",
             r"$\frac{\infty}{\infty}$ twice: $\frac{4x}{10x + 3} \to \frac{4}{10}$."),
        pick(r"\[ \lim_{x \to \infty} \frac{x^3}{e^{x}} = \]", r"$0$", [r"$1$", r"$6$", r"$\infty$"], "D",
             r"$\frac{\infty}{\infty}$ three times: $\frac{6}{e^x} \to 0$.", {r"$6$": "stopped at the numerator"}),
    ),
    Variants(
        pick(r"The cost of making $x$ chairs is $C(x) = 500 + 20x - 0.01x^2$ dollars. The marginal cost at $x = 100$ is", r"$18$ dollars per chair",
             [r"$2400$ dollars", r"$20$ dollars per chair", r"$24$ dollars per chair"], "C", r"$C'(x) = 20 - 0.02x$, so $C'(100) = 18$.",
             {r"$2400$ dollars": "that's $C(100)$"}),
        pick(r"The revenue from selling $x$ lamps is $R(x) = 50x - 0.02x^2$ dollars. The marginal revenue at $x = 500$ is", r"$30$ dollars per lamp",
             [r"$20000$ dollars", r"$50$ dollars per lamp", r"$40$ dollars per lamp"], "D", r"$R'(x) = 50 - 0.04x$, so $R'(500) = 30$.",
             {r"$20000$ dollars": "that's $R(500)$"}),
    ),
    Variants(
        pick(r"Water enters a tank at $R(t) = 3t^2 + 2$ liters per hour and leaves at $D(t) = 8t$ liters per hour. At $t = 2$, the amount of water is",
             r"decreasing at $2$ liters per hour", [r"increasing at $2$ liters per hour", r"increasing at $30$ liters per hour", r"decreasing at $14$ liters per hour"], "A",
             r"$R(2) - D(2) = 14 - 16 = -2$.", {r"increasing at $30$ liters per hour": "added the rates"}),
        pick(r"Water enters a tank at $R(t) = 20 + 2t$ liters per hour and leaves at $D(t) = t^2$ liters per hour. At $t = 4$, the amount of water is",
             r"increasing at $12$ liters per hour", [r"decreasing at $12$ liters per hour", r"increasing at $44$ liters per hour", r"increasing at $28$ liters per hour"], "B",
             r"$R(4) - D(4) = 28 - 16 = 12$.", {r"increasing at $44$ liters per hour": "added the rates"}),
    ),
]
same("A2", [sp.solve(3 * t**2 - 6 * t - 9, t), sp.solve(3 * t**2 - 12, t)], [[-1, 3], [-2, 2]])
same("A3", [(t**2 - 4 * t + 3).subs(t, sp.Rational(5, 2)), (t**2 - 6 * t + 8).subs(t, 5)], [sp.Rational(-3, 4), 3])
same("A4", [dist(t**2 - 4 * t, 0, 5), dist(t**2 - 6 * t, 0, 8)], [13, 34])
same("A7", [lin(sp.sqrt(x), 16, sp.Rational(164, 10)), lin(sp.cbrt(x), 27, sp.Rational(2754, 100))], [sp.Rational(405, 100), sp.Rational(302, 100)])
same("A9", [sp.limit((sp.exp(2 * x) - 1) / sp.sin(x), x, 0), sp.limit(sp.sin(5 * x) / (2 * x), x, 0)], [2, sp.Rational(5, 2)])
same("A10", [sp.limit((2 * x**2 - 1) / (5 * x**2 + 3 * x), x, sp.oo), sp.limit(x**3 / sp.exp(x), x, sp.oo)], [sp.Rational(2, 5), 0])

B = [
    Variants(
        pick(r"A particle's velocity is $v(t) = \sin\left(t^2\right)$. At what time $t > 0$ does it first change direction?", r"$1.772$",
             [r"$1.253$", r"$3.142$", r"$2.507$"], "B", r"$v$ first changes sign where $t^2 = \pi$: $t = \sqrt\pi \approx 1.772$.", {r"$3.142$": "that's $t^2$"}, calc=True),
        pick(r"A particle's velocity is $v(t) = \cos\left(t^2\right)$. At what time $t > 0$ does it first change direction?", r"$1.253$",
             [r"$1.571$", r"$1.772$", r"$2.171$"], "A", r"$v$ first changes sign where $t^2 = \frac\pi2$: $t \approx 1.253$.", {r"$1.571$": "that's $t^2$"}, calc=True),
    ),
    Variants(
        pick(r"The radius of a sphere grows at $0.5$ cm/s. How fast is the volume growing when $r = 3.2$ cm?", r"$64.340$ cm$^3$/s",
             [r"$137.258$ cm$^3$/s", r"$128.680$ cm$^3$/s", r"$20.106$ cm$^3$/s"], "D", r"$4\pi(3.2)^2(0.5) \approx 64.340$.", {r"$137.258$ cm$^3$/s": "that's the volume"}, calc=True),
        pick(r"The radius of a sphere grows at $0.4$ cm/s. How fast is the volume growing when $r = 2.7$ cm?", r"$36.644$ cm$^3$/s",
             [r"$82.448$ cm$^3$/s", r"$91.609$ cm$^3$/s", r"$13.572$ cm$^3$/s"], "C", r"$4\pi(2.7)^2(0.4) \approx 36.644$.", {r"$82.448$ cm$^3$/s": "that's the volume"}, calc=True),
    ),
    Variants(
        pick(r"Let $f(x) = xe^{x/3}$. Using the line tangent to the graph of $f$ at $x = 2$, $f(2.1)$ is approximately", r"$4.220$",
             [r"$4.229$", r"$3.896$", r"$3.571$"], "C", r"$f(2) = 2e^{2/3} \approx 3.896$ and $f'(2) = \frac53e^{2/3} \approx 3.246$, so $3.896 + 0.325 \approx 4.220$.",
             {r"$3.896$": "that's $f(2)$", r"$4.229$": "that's $f(2.1)$ itself"}, calc=True),
        pick(r"Let $f(x) = \ln\left(x^2 + 1\right)$. Using the line tangent to the graph of $f$ at $x = 2$, $f(1.9)$ is approximately", r"$1.529$",
             [r"$1.609$", r"$1.689$", r"$1.536$"], "A", r"$f(2) = \ln 5 \approx 1.609$ and $f'(2) = \frac45$, so $1.609 - 0.08 \approx 1.529$.",
             {r"$1.609$": "that's $f(2)$", r"$1.536$": "that's $f(1.9)$ itself"}, calc=True),
    ),
    Variants(
        pick(r"A particle's position is $x(t) = t\cos t$. What is its speed at $t = 2$?", r"$2.235$", [r"$-2.235$", r"$0.832$", r"$1.403$"], "D",
             r"$v(t) = \cos t - t\sin t$, so $v(2) \approx -2.235$. Speed is $|v|$.", {r"$-2.235$": "that's the velocity; speed is never negative", r"$0.832$": "that's $|x(2)|$"}, calc=True),
        pick(r"A particle's position is $x(t) = e^{-t}\sin(2t)$. What is its speed at $t = 1$?", r"$0.641$", [r"$-0.641$", r"$0.335$", r"$1.741$"], "C",
             r"$v(t) = e^{-t}\left(2\cos 2t - \sin 2t\right)$, so $v(1) \approx -0.641$. Speed is $|v|$.", {r"$-0.641$": "that's the velocity; speed is never negative", r"$0.335$": "that's $x(1)$"}, calc=True),
    ),
]
close("B13", sp.sqrt(pi), 1.772, 5e-4)
close("B13b", sp.sqrt(pi / 2), 1.253, 5e-4)
close("B14", 4 * pi * 3.2**2 * 0.5, 64.340, 5e-4)
close("B14b", 4 * pi * 2.7**2 * 0.4, 36.644, 5e-4)
close("B15", lin(x * sp.exp(x / 3), 2, sp.Rational(21, 10)), 4.220, 5e-4)
close("B15 exact", (x * sp.exp(x / 3)).subs(x, 2.1), 4.229, 5e-4)
close("B15b", lin(sp.log(x**2 + 1), 2, sp.Rational(19, 10)), 1.529, 5e-4)
close("B15b exact", sp.log(1.9**2 + 1), 1.528, 5e-4)
close("B16", -sp.diff(t * sp.cos(t), t).subs(t, 2), 2.235, 5e-4)
close("B16b", -sp.diff(sp.exp(-t) * sp.sin(2 * t), t).subs(t, 1), 0.641, 5e-4)
close("B16b x", (sp.exp(-t) * sp.sin(2 * t)).subs(t, 1), 0.335, 5e-4)


# ================================================================ free response
def motion_frq(xf, T, t_c):
    v, a = sp.expand(sp.diff(xf, t)), sp.expand(sp.diff(xf, t, 2))
    rest = sorted(sp.solve(v, t))
    vc, ac = v.subs(t, t_c), a.subs(t, t_c)
    word = "speeding up" if vc * ac > 0 else "slowing down"
    d = dist(xf, 0, T)
    pts = [0] + rest + [T]
    frq = FRQ("A particle on a line", (
        rf"A particle moves along the $x$-axis with position $x(t) = {sp.latex(xf)}$ feet at time $t$ seconds, $0 \le t \le {T}$."), [
        Part("a", r"Find the velocity $v(t)$.", expr(str(v), var="t"), rf"$v(t) = {sp.latex(v)} = {sp.latex(sp.factor(v))}$.", [(1, "velocity")], work="1.6cm"),
        Part("b", r"At what times is the particle at rest? Enter the later one.", num(rest[-1]),
             rf"$v(t) = 0$ at $t = {rest[0]}$ and $t = {rest[1]}$.", [(1, "sets $v = 0$"), (1, "both times")], work="1.8cm"),
        Part("c", rf"Is the particle speeding up or slowing down at $t = {t_c}$? Give a reason.", selfcheck(rf"\text{{{word}}}"),
             rf"$v({t_c}) = {sp.latex(vc)}$ and $a({t_c}) = {sp.latex(ac)}$. They have {'the same sign' if vc * ac > 0 else 'opposite signs'}, so the particle is {word}.",
             [(1, "finds $v$ and $a$"), (1, "conclusion with the sign reason")], work="2.2cm"),
        Part("d", rf"Find the total distance the particle travels from $t = 0$ to $t = {T}$.", num(d),
             r"The particle turns at the rest times. " + ", ".join(f"$x({p}) = {xf.subs(t, p)}$" for p in pts)
             + rf". Distance $= {' + '.join(str(abs(xf.subs(t, q) - xf.subs(t, p))) for p, q in zip(pts, pts[1:]))} = {d}$ feet.",
             [(1, "uses the turning points"), (1, "positions"), (1, "total")], work="3cm"),
    ], frq_type="Particle motion")
    return frq, [v, rest, word, d]


F1A, mA = motion_frq(2 * t**3 - 9 * t**2 + 12 * t + 1, 3, sp.Rational(1, 2))
F1B, mB = motion_frq(t**3 - 12 * t**2 + 36 * t - 5, 7, 3)
same("F1 A", mA[1] + [mA[3]], [1, 2, 11])
same("F1 B", mB[1] + [mB[3]], [2, 6, 71])
assert (mA[2], mB[2]) == ("slowing down", "speeding up")


def cone_frq(R, H, rate, h0):
    k = sp.Rational(R, H)
    h = sp.symbols("h")
    V = sp.pi * (k * h)**2 * h / 3
    dhdt = sp.simplify(-rate / sp.diff(V, h).subs(h, h0))
    Aw = sp.pi * (k * h)**2
    dAdt = sp.simplify(sp.diff(Aw, h).subs(h, h0) * dhdt)
    frq = FRQ("A draining cone", (
        rf"A tank is a cone, point down, with radius ${R}$ feet at the top and height ${H}$ feet. Water drains out at ${rate}$ cubic feet per minute. "
        r"The volume of a cone is $V = \frac13\pi r^2 h$, where $r$ is the radius of the water's surface and $h$ is the depth."), [
        Part("a", r"Write the volume of the water as a function of its depth $h$ alone.", selfcheck(rf"V = {sp.latex(V)}"),
             rf"Similar triangles: $\frac{{r}}{{h}} = \frac{{{R}}}{{{H}}}$, so $r = {sp.latex(k * h)}$ and $V = {sp.latex(V)}$.", [(1, "relates $r$ and $h$"), (1, "$V$ in terms of $h$")], work="2.2cm"),
        Part("b", rf"How fast is the depth changing when the water is ${h0}$ feet deep? Include units.", num(dhdt),
             rf"$\dfrac{{dV}}{{dt}} = {sp.latex(sp.diff(V, h))}\,\dfrac{{dh}}{{dt}}$. With $\dfrac{{dV}}{{dt}} = -{rate}$ and $h = {h0}$: "
             rf"$\dfrac{{dh}}{{dt}} = {sp.latex(dhdt)}$ feet per minute.", [(1, "differentiates with respect to $t$"), (1, "uses $-" + str(rate) + "$"), (1, "answer with units")], work="2.6cm"),
        Part("c", rf"The water's surface is a circle of area $A = \pi r^2$. How fast is $A$ changing when the water is ${h0}$ feet deep?", num(dAdt),
             rf"$A = {sp.latex(Aw)}$, so $\dfrac{{dA}}{{dt}} = {sp.latex(sp.diff(Aw, h))}\,\dfrac{{dh}}{{dt}} = {sp.latex(dAdt)}$ square feet per minute.",
             [(1, "chain rule"), (1, "value")], work="2.2cm"),
    ], frq_type="Related rates")
    return frq, [dhdt, dAdt]


F2A, cA = cone_frq(4, 12, 3, 6)
F2B, cB = cone_frq(5, 10, 2, 4)
same("F2 A", cA, [-3 / (4 * pi), -1])
same("F2 B", cB, [-1 / (2 * pi), -1])


def approx_frq(a, fa1, sign, at, den, den_tex):
    """f(a) = 0, f'(a) = fa1; graph above (sign > 0) or below its tangent lines; estimate f(at); lim f/den by L'Hospital."""
    est = fa1 * (at - a)
    word = "underestimate" if sign > 0 else "overestimate"
    side = "above" if sign > 0 else "below"
    lim = sp.Rational(fa1) / sp.diff(den, x).subs(x, a)
    frq = FRQ("Estimates and limits from the derivative", (
        rf"$f$ is differentiable, with $f({a}) = 0$ and $f'({a}) = {fa1}$. Near $x = {a}$, the graph of $f$ lies {side} its tangent lines."), [
        Part("a", rf"Write an equation for the line tangent to the graph of $f$ at $x = {a}$, and use it to estimate $f({at})$.", num(est),
             rf"$y = {fa1}(x - {a})$, so $f({at}) \approx {fa1}({sp.latex(sp.nsimplify(at - a))}) = {sp.latex(est)}$.", [(1, "tangent line"), (1, "estimate")], work="2cm"),
        Part("b", r"Is the estimate in part (a) an overestimate or an underestimate? Explain.", selfcheck(rf"\text{{{word}}}"),
             rf"An {word}: the graph lies {side} the tangent line, so the line's value is too {'small' if sign > 0 else 'big'}.", [(1, "answer with reason")], work="1.6cm"),
        Part("c", rf"Find $\displaystyle\lim_{{x \to {a}}} \frac{{f(x)}}{{{den_tex}}}$. Show that L'Hospital's Rule applies.", num(lim),
             rf"Both $f(x) \to f({a}) = 0$ and ${den_tex} \to 0$, so the form is $\frac00$. By L'Hospital's Rule the limit is "
             rf"$\dfrac{{f'({a})}}{{{sp.latex(sp.diff(den, x))}\big|_{{x = {a}}}}} = {sp.latex(lim)}$.", [(1, "shows $\\frac00$"), (1, "derivatives"), (1, "value")], work="2.4cm"),
    ], frq_type="Linearization and limits")
    return frq, [est, word, lim]


F3A, aA = approx_frq(2, 3, 1, sp.Rational(21, 10), x**2 - 4, r"x^2 - 4")
F3B, aB = approx_frq(1, -2, -1, sp.Rational(9, 10), x**3 - 1, r"x^3 - 1")
same("F3 A", [aA[0], aA[2]], [sp.Rational(3, 10), sp.Rational(3, 4)])
same("F3 B", [aB[0], aB[2]], [sp.Rational(2, 10), sp.Rational(-2, 3)])

TEST = UnitTest(unit=4, title="Contextual Applications of Differentiation", mcq_a=A, mcq_b=B,
                frq=[Variants(F1A, F1B), Variants(F2A, F2B), Variants(F3A, F3B)])
