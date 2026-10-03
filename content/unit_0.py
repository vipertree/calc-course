"""Unit 0 test: Trig Review. Same format as the AP-style unit tests: 12 MCQ (no calculator), 4 MCQ (calculator), 3 FRQ.
Two forms (A and B) for every slot. Covers 0.1-0.7.

Choices are built by `pick`, which puts the keyed answer at a planned letter. Every keyed value is checked with sympy.
The FRQs use AP phrasing ("Show that", "Find all values", "Indicate units of measure") on trig-only setups: a sinusoid
model, identities and equations, and a right-triangle / inverse-trig context.
"""
import sympy as sp

from calclib import FRQ, MCQ, Part, UnitTest, Variants, check, close, num, same, selfcheck

x, t = sp.symbols("x t", real=True)
pi, r2, r3 = sp.pi, sp.sqrt(2), sp.sqrt(3)
deg = lambda d: d * pi / 180

LA = "BCADCBDACDABDBCA"      # planned answer letters, form A then form B (each letter 4 times per form)
LB = "CADBADBCBACDACDB"


def pick(stem, right, wrong, letter, solution, why=None, calc=False):
    """MCQ with the correct choice placed at `letter`. `wrong` is three distractors, keyed by why-text if given."""
    k = "ABCD".index(letter)
    choices = list(wrong)
    choices.insert(k, right)
    assert len(set(choices)) == 4, choices
    why_not = {}
    if why:
        for text, reason in why.items():
            why_not["ABCD"[choices.index(text)]] = reason
    return MCQ(stem, choices, letter, solution, why_not=why_not, calc=calc)


def slot(n, a, b):
    """Slot n (0-based): a and b are (stem, right, wrong, solution, why) tuples for forms A and B."""
    calc = n >= 12
    return Variants(pick(a[0], a[1], a[2], LA[n], a[3], a[4] if len(a) > 4 else None, calc),
                    pick(b[0], b[1], b[2], LB[n], b[3], b[4] if len(b) > 4 else None, calc))


# ---------------------------------------------------------------- part A: no calculator
same("A1", [225 * pi / 180, sp.Rational(7, 6) * 180], [5 * pi / 4, 210])
same("A2", [9 * 2 * pi / 3, sp.Rational(1, 2) * 36 * 5 * pi / 6], [6 * pi, 15 * pi])
same("A3", [sp.cos(7 * pi / 6), sp.sin(7 * pi / 4)], [-r3 / 2, -r2 / 2])
same("A4", [sp.tan(5 * pi / 3), 1 / sp.cos(5 * pi / 4)], [-r3, -r2])
same("A6", [-sp.sqrt(1 - sp.Rational(25, 169)), -sp.Rational(4, 5) / sp.Rational(3, 5)], [-sp.Rational(12, 13), -sp.Rational(4, 3)])
same("A7", [2 * pi / (pi / 3), 2 + 5], [6, 7])
same("A8", [sp.simplify((sp.sec(x)**2 - 1) * sp.cos(x)**2 - sp.sin(x)**2), sp.simplify(sp.sin(x) / sp.csc(x) + sp.cos(x) / sp.sec(x))], [0, 1])
same("A9", [sp.sin(pi / 12), sp.sin(7 * pi / 12)], [(sp.sqrt(6) - r2) / 4, (sp.sqrt(6) + r2) / 4])
same("A10", [2 * sp.sin(7 * pi / 6) + 1, 2 * sp.sin(11 * pi / 6) + 1, 2 * sp.cos(3 * pi / 4)**2 - 1], [0, 0, 0])
same("A11", [sp.acos(-r3 / 2), sp.asin(sp.sin(4 * pi / 3))], [5 * pi / 6, -pi / 3])
same("A12", [sp.cos(sp.atan(sp.Rational(3, 4))), sp.sin(sp.acos(-sp.Rational(5, 13)))], [sp.Rational(4, 5), sp.Rational(12, 13)])

A = [
    slot(0, (r"$225^\circ$ in radians is", r"$\frac{5\pi}{4}$", [r"$\frac{3\pi}{4}$", r"$\frac{4\pi}{5}$", r"$\frac{5\pi}{3}$"], r"$225 \cdot \frac{\pi}{180} = \frac{5\pi}{4}$.",
             {r"$\frac{4\pi}{5}$": "the fraction is upside down"}),
         (r"$\frac{7\pi}{6}$ radians in degrees is", r"$210^\circ$", [r"$150^\circ$", r"$240^\circ$", r"$315^\circ$"], r"$\frac{7 \cdot 180}{6} = 210^\circ$.",
             {r"$150^\circ$": r"that is $\frac{5\pi}{6}$"})),
    slot(1, (r"An angle of $\frac{2\pi}{3}$ on a circle of radius $9$ cuts off an arc of length", r"$6\pi$", [r"$3\pi$", r"$27\pi$", r"$120$"], r"$s = r\theta = 9 \cdot \frac{2\pi}{3}$.",
             {r"$27\pi$": "that is the sector area", r"$120$": "the angle must be in radians"}),
         (r"A sector of a circle of radius $6$ with angle $\frac{5\pi}{6}$ has area", r"$15\pi$", [r"$5\pi$", r"$30\pi$", r"$\frac{5\pi}{2}$"], r"$A = \frac12 \cdot 36 \cdot \frac{5\pi}{6} = 15\pi$.",
             {r"$5\pi$": "that is the arc length", r"$30\pi$": r"the formula has a $\frac12$"})),
    slot(2, (r"$\cos\frac{7\pi}{6} = $", r"$-\frac{\sqrt3}{2}$", [r"$-\frac12$", r"$\frac{\sqrt3}{2}$", r"$\frac12$"], r"Reference angle $\frac{\pi}{6}$, quadrant III: cosine negative.",
             {r"$-\frac12$": r"that is $\sin\frac{7\pi}{6}$", r"$\frac{\sqrt3}{2}$": "cosine is negative in quadrant III"}),
         (r"$\sin\frac{7\pi}{4} = $", r"$-\frac{\sqrt2}{2}$", [r"$\frac{\sqrt2}{2}$", r"$-\frac12$", r"$-1$"], r"Reference angle $\frac{\pi}{4}$, quadrant IV: sine negative.",
             {r"$\frac{\sqrt2}{2}$": "sine is negative in quadrant IV"})),
    slot(3, (r"$\tan\frac{5\pi}{3} = $", r"$-\sqrt3$", [r"$\sqrt3$", r"$-\frac{\sqrt3}{3}$", r"$-\frac{\sqrt3}{2}$"], r"$\frac{-\sqrt3/2}{1/2} = -\sqrt3$.",
             {r"$-\frac{\sqrt3}{3}$": r"that is $\cot\frac{5\pi}{3}$", r"$-\frac{\sqrt3}{2}$": r"that is $\sin\frac{5\pi}{3}$"}),
         (r"$\sec\frac{5\pi}{4} = $", r"$-\sqrt2$", [r"$\sqrt2$", r"$-\frac{\sqrt2}{2}$", r"$-1$"], r"$\frac{1}{-\sqrt2/2} = -\sqrt2$.",
             {r"$-\frac{\sqrt2}{2}$": r"that is $\cos\frac{5\pi}{4}$"})),
    slot(4, (r"If $\sin\theta < 0$ and $\tan\theta < 0$, the terminal side of $\theta$ is in quadrant", "IV", ["I", "II", "III"], r"Sine negative: III or IV. Tangent negative needs cosine positive: IV.",
             {"III": r"in quadrant III, $\tan\theta > 0$"}),
         (r"If $\cos\theta < 0$ and $\cot\theta > 0$, the terminal side of $\theta$ is in quadrant", "III", ["I", "II", "IV"], r"Cosine negative: II or III. Cotangent positive needs sine negative too: III.",
             {"II": r"in quadrant II, $\cot\theta < 0$"})),
    slot(5, (r"$\sin\theta = -\frac{5}{13}$ and $\theta$ is in quadrant III. Then $\cos\theta = $", r"$-\frac{12}{13}$", [r"$\frac{12}{13}$", r"$-\frac{8}{13}$", r"$\frac{5}{12}$"],
             r"$\cos^2\theta = 1 - \frac{25}{169} = \frac{144}{169}$; negative in quadrant III.", {r"$\frac{12}{13}$": "cosine is negative in quadrant III", r"$\frac{5}{12}$": r"that is $\tan\theta$"}),
         (r"$\cos\theta = \frac35$ and $\theta$ is in quadrant IV. Then $\tan\theta = $", r"$-\frac43$", [r"$\frac43$", r"$-\frac34$", r"$-\frac45$"],
             r"$\sin\theta = -\frac45$, so $\tan\theta = \frac{-4/5}{3/5}$.", {r"$-\frac45$": r"that is $\sin\theta$", r"$-\frac34$": r"that is $\cot\theta$"})),
    slot(6, (r"The period of $y = 4\cos\left(\frac{\pi x}{3}\right) - 1$ is", r"$6$", [r"$\frac{2\pi}{3}$", r"$4$", r"$\frac{\pi}{3}$"], r"$\frac{2\pi}{\pi/3} = 6$.",
             {r"$4$": "that is the amplitude"}),
         (r"The maximum value of $y = 2 - 5\sin(3x)$ is", r"$7$", [r"$2$", r"$5$", r"$-3$"], r"Midline $2$, amplitude $5$: $2 + 5$.", {r"$-3$": "that is the minimum"})),
    slot(7, (r"$(\sec^2 x - 1)\cos^2 x = $", r"$\sin^2 x$", [r"$1$", r"$\tan^2 x$", r"$\cos^2 x$"], r"$\sec^2 x - 1 = \tan^2 x$, and $\tan^2 x\cos^2 x = \sin^2 x$.",
             {r"$\tan^2 x$": r"that is only the first factor"}),
         (r"$\dfrac{\sin x}{\csc x} + \dfrac{\cos x}{\sec x} = $", r"$1$", [r"$\sin x + \cos x$", r"$2$", r"$\tan x$"], r"$\sin^2 x + \cos^2 x = 1$.")),
    slot(8, (r"$\sin\frac{\pi}{12} = $", r"$\frac{\sqrt6 - \sqrt2}{4}$", [r"$\frac{\sqrt6 + \sqrt2}{4}$", r"$\frac{\sqrt3 - 1}{2}$", r"$\frac{1}{12}$"],
             r"$\sin\left(\frac{\pi}{3} - \frac{\pi}{4}\right) = \frac{\sqrt3}{2}\cdot\frac{\sqrt2}{2} - \frac12\cdot\frac{\sqrt2}{2}$.", {r"$\frac{\sqrt6 + \sqrt2}{4}$": r"that is $\cos\frac{\pi}{12}$"}),
         (r"$\sin\frac{7\pi}{12} = $", r"$\frac{\sqrt6 + \sqrt2}{4}$", [r"$\frac{\sqrt6 - \sqrt2}{4}$", r"$\frac{\sqrt2 - \sqrt6}{4}$", r"$\frac{\sqrt3 + 1}{2}$"],
             r"$\sin\left(\frac{\pi}{3} + \frac{\pi}{4}\right) = \frac{\sqrt3}{2}\cdot\frac{\sqrt2}{2} + \frac12\cdot\frac{\sqrt2}{2}$.", {r"$\frac{\sqrt2 - \sqrt6}{4}$": r"that is $\cos\frac{7\pi}{12}$"})),
    slot(9, (r"The solutions of $2\sin x + 1 = 0$ for $0 \le x < 2\pi$ are", r"$\frac{7\pi}{6}, \frac{11\pi}{6}$", [r"$\frac{\pi}{6}, \frac{5\pi}{6}$", r"$\frac{4\pi}{3}, \frac{5\pi}{3}$", r"$\frac{5\pi}{6}, \frac{7\pi}{6}$"],
             r"$\sin x = -\frac12$: reference angle $\frac{\pi}{6}$ in quadrants III and IV.", {r"$\frac{\pi}{6}, \frac{5\pi}{6}$": r"those solve $\sin x = \frac12$"}),
         (r"The solutions of $2\cos^2 x - 1 = 0$ for $0 \le x < 2\pi$ are", r"$\frac{\pi}{4}, \frac{3\pi}{4}, \frac{5\pi}{4}, \frac{7\pi}{4}$", [r"$\frac{\pi}{4}, \frac{7\pi}{4}$", r"$\frac{\pi}{3}, \frac{5\pi}{3}$", r"$\frac{\pi}{4}, \frac{5\pi}{4}$"],
             r"$\cos x = \pm\frac{\sqrt2}{2}$: all four quadrants.", {r"$\frac{\pi}{4}, \frac{7\pi}{4}$": r"keep both signs of $\pm\frac{\sqrt2}{2}$"})),
    slot(10, (r"$\arccos\left(-\frac{\sqrt3}{2}\right) = $", r"$\frac{5\pi}{6}$", [r"$-\frac{\pi}{6}$", r"$\frac{7\pi}{6}$", r"$\frac{2\pi}{3}$"], r"In $[0, \pi]$, reference angle $\frac{\pi}{6}$, quadrant II.",
              {r"$-\frac{\pi}{6}$": r"arccosine's range is $[0, \pi]$", r"$\frac{7\pi}{6}$": r"$\frac{7\pi}{6}$ is outside $[0, \pi]$"}),
         (r"$\arcsin\left(\sin\frac{4\pi}{3}\right) = $", r"$-\frac{\pi}{3}$", [r"$\frac{4\pi}{3}$", r"$\frac{\pi}{3}$", r"$-\frac{\sqrt3}{2}$"], r"$\sin\frac{4\pi}{3} = -\frac{\sqrt3}{2}$, and $\arcsin\left(-\frac{\sqrt3}{2}\right) = -\frac{\pi}{3}$.",
              {r"$\frac{4\pi}{3}$": r"$\frac{4\pi}{3}$ is outside arcsine's range", r"$-\frac{\sqrt3}{2}$": "arcsine returns an angle"})),
    slot(11, (r"$\cos\left(\arctan\frac34\right) = $", r"$\frac45$", [r"$\frac35$", r"$\frac43$", r"$\frac54$"], r"Opposite $3$, adjacent $4$, hypotenuse $5$: $\frac{4}{5}$.", {r"$\frac35$": "that is the sine"}),
         (r"$\sin\left(\arccos\left(-\frac{5}{13}\right)\right) = $", r"$\frac{12}{13}$", [r"$-\frac{12}{13}$", r"$\frac{5}{13}$", r"$-\frac{5}{12}$"],
              r"$\arccos\left(-\frac{5}{13}\right)$ is in quadrant II, where sine is positive: $\sqrt{1 - \frac{25}{169}}$.", {r"$-\frac{12}{13}$": "arccosine answers in quadrants I and II, where sine is positive"})),
]

# ---------------------------------------------------------------- part B: calculator
v13 = [float(30 * sp.tan(deg(41))), float(80 * sp.sin(deg(37)))]
v14a = [float(sp.acos(sp.Rational(2, 5))), float(2 * pi - sp.acos(sp.Rational(2, 5)))]
v14b = [float(pi - sp.atan(3)), float(2 * pi - sp.atan(3))]
v15 = [float(10 + 4 * sp.sin(pi * sp.Rational(5, 2) / 6)), float(30 - 25 * sp.cos(pi * sp.Rational(6, 5) / 3))]
v16 = [float(sp.atan(sp.Rational(2, 15)) * 180 / pi), float(sp.acos(sp.Rational(18, 70)) * 180 / pi)]
close("B13", v13[0], 26.08, 0.005); close("B13b", v13[1], 48.15, 0.005)
close("B14", v14a[0], 1.159, 5e-4); close("B14'", v14a[1], 5.124, 5e-4)
close("B14b", v14b[0], 1.893, 5e-4); close("B14b'", v14b[1], 5.034, 5e-4)
close("B15", v15[0], 13.864, 5e-4); close("B15b", v15[1], 22.275, 5e-4)
close("B16", v16[0], 7.595, 5e-4); close("B16b", v16[1], 75.10, 0.005)

B = [
    slot(12, (r"From a point $30$ m from the base of a tree, the angle up to the top of the tree is $41^\circ$. To the nearest hundredth of a meter, the tree is", r"$26.08$ m", [r"$19.68$ m", r"$34.51$ m", r"$22.64$ m"],
              r"$h = 30\tan 41^\circ \approx 26.08$.", {r"$19.68$ m": r"that uses $\sin 41^\circ$", r"$22.64$ m": r"that uses $\cos 41^\circ$"}),
         (r"A kite string $80$ m long makes a $37^\circ$ angle with the ground. To the nearest hundredth of a meter, the kite's height is", r"$48.15$ m", [r"$63.89$ m", r"$60.28$ m", r"$106.16$ m"],
              r"$h = 80\sin 37^\circ \approx 48.15$.", {r"$63.89$ m": r"that uses $\cos 37^\circ$", r"$60.28$ m": r"that uses $\tan 37^\circ$"})),
    slot(13, (r"The solutions of $5\cos x = 2$ for $0 \le x < 2\pi$ are", r"$1.159$ and $5.124$", [r"$1.159$ and $1.983$", r"$0.412$ and $2.730$", r"$1.159$ only"],
              r"$\cos x = 0.4$: $\arccos 0.4 \approx 1.159$, and the quadrant IV angle $2\pi - 1.159 \approx 5.124$.", {r"$1.159$ only": "arccosine gives only one of the two solutions", r"$0.412$ and $2.730$": r"those solve $\sin x = 0.4$"}),
         (r"The solutions of $\tan x = -3$ for $0 \le x < 2\pi$ are", r"$1.893$ and $5.034$", [r"$-1.249$ and $1.893$", r"$1.249$ and $4.391$", r"$1.893$ only"],
              r"$\arctan(-3) \approx -1.249$; add $\pi$ and $2\pi$ to land in $[0, 2\pi)$: $1.893$ and $5.034$.", {r"$1.249$ and $4.391$": r"those solve $\tan x = 3$"})),
    slot(14, (r"The depth of water in a bay is $d(t) = 10 + 4\sin\left(\frac{\pi t}{6}\right)$ meters, $t$ hours after midnight. To the nearest thousandth, the depth at $t = 2.5$ is",
              r"$13.864$ m", [r"$10.183$ m", r"$12.000$ m", r"$14.000$ m"], r"$10 + 4\sin\frac{5\pi}{12} \approx 13.864$.", {r"$10.183$ m": "the calculator was in degree mode"}),
         (r"A rider's height on a Ferris wheel is $h(t) = 30 - 25\cos\left(\frac{\pi t}{3}\right)$ meters after $t$ minutes. To the nearest thousandth, $h(1.2)$ is",
              r"$22.275$ m", [r"$5.016$ m", r"$37.725$ m", r"$30.000$ m"], r"$30 - 25\cos(0.4\pi) \approx 22.275$.", {r"$5.016$ m": "the calculator was in degree mode", r"$37.725$ m": "the sign of the cosine term was flipped"})),
    slot(15, (r"A ramp rises $2$ ft over a horizontal run of $15$ ft. To the nearest thousandth of a degree, the angle it makes with the ground is",
              r"$7.595^\circ$", [r"$7.660^\circ$", r"$0.133^\circ$", r"$82.405^\circ$"], r"$\arctan\frac{2}{15} \approx 7.595^\circ$.", {r"$0.133^\circ$": "that is the angle in radians", r"$82.405^\circ$": "that is the angle at the top"}),
         (r"A $7$ m ladder leans against a wall with its foot $1.8$ m from the wall. To the nearest hundredth of a degree, the angle between the ladder and the ground is",
              r"$75.10^\circ$", [r"$14.90^\circ$", r"$75.58^\circ$", r"$1.31^\circ$"], r"$\cos\theta = \frac{1.8}{7}$, $\theta = \arccos\frac{1.8}{7} \approx 75.10^\circ$.", {r"$14.90^\circ$": "that is the angle with the wall"})),
]

# ---------------------------------------------------------------- free response
def sinusoid_frq(intro, model_q, model_ans, model_sol, fn, b_prompt, b_ans, b_sol, c_level, c_times, c_sol, d_prompt, d_ans, d_sol, units, word="height"):
    return FRQ("Question 1", intro, [
        Part("a", model_q, selfcheck(model_ans), model_sol, [(1, "amplitude and midline"), (1, "period"), (1, "correct starting position")], work="3cm"),
        Part("b", b_prompt, selfcheck(b_ans), b_sol, [(1, "value"), (1, "time")], work="2.4cm"),
        Part("c", rf"Find all times $t$ in the interval given at which the {word} is ${c_level}$ {units}. Show the work that leads to your answer.",
             selfcheck(c_times), c_sol, [(1, "sets up the equation for the cosine"), (1, "reference angle"), (1, "both times")], work="3.4cm"),
        Part("d", d_prompt, selfcheck(d_ans), d_sol, [(1, "answer with reason")], work="2cm"),
    ], frq_type="Sinusoid model")


hA = 24 - 20 * sp.cos(pi * t / 3)
same("F1A", [hA.subs(t, 0), hA.subs(t, 3), hA.subs(t, 2), hA.subs(t, 4)], [4, 44, 34, 34])
F1A = sinusoid_frq(
    r"A Ferris wheel has a radius of $20$ meters, and its center is $24$ meters above the ground. The wheel turns at a constant rate, making one full turn every "
    r"$6$ minutes. A rider boards at the lowest point of the wheel at time $t = 0$. Let $h(t)$ be the rider's height above the ground, in meters, for $0 \le t \le 6$.",
    r"Write an equation for $h(t)$.", r"h(t) = 24 - 20\cos\left(\frac{\pi t}{3}\right)",
    r"Midline $24$, amplitude $20$, period $6$ so $B = \frac{2\pi}{6} = \frac{\pi}{3}$. The rider starts at a minimum, so $h(t) = 24 - 20\cos\left(\frac{\pi t}{3}\right)$.",
    hA, r"Find the rider's maximum height and the time $t$ at which it occurs.", r"44 \text{ m at } t = 3",
    r"The maximum is $24 + 20 = 44$ m, when $\cos\frac{\pi t}{3} = -1$: $\frac{\pi t}{3} = \pi$, $t = 3$ minutes (halfway around).",
    34, r"t = 2 \text{ and } t = 4",
    r"$24 - 20\cos\frac{\pi t}{3} = 34$ gives $\cos\frac{\pi t}{3} = -\frac12$. With $0 \le \frac{\pi t}{3} \le 2\pi$: $\frac{\pi t}{3} = \frac{2\pi}{3}$ or $\frac{4\pi}{3}$, so $t = 2$ or $t = 4$.",
    r"For how many minutes of each turn is the rider more than $34$ meters above the ground? Give a reason for your answer.", r"2 \text{ minutes}",
    r"The height is above $34$ m between $t = 2$ and $t = 4$ (the maximum, $t = 3$, is between them), so for $2$ minutes.", "meters")

dB = 7 + 5 * sp.cos(pi * (t - 2) / 6)
same("F1B", [dB.subs(t, 2), dB.subs(t, 8), dB.subs(t, 0), dB.subs(t, 6), dB.subs(t, 10)], [12, 2, sp.Rational(19, 2), sp.Rational(9, 2), sp.Rational(9, 2)])
F1B = sinusoid_frq(
    r"The depth of water in a harbor rises and falls with the tide. On a certain day, high tide is $12$ meters at $t = 2$ hours after midnight and the next low tide "
    r"is $2$ meters at $t = 8$. The depth $D(t)$, in meters, is modeled by a sinusoidal function of $t$ for $0 \le t < 12$.",
    r"Write an equation for $D(t)$.", r"D(t) = 7 + 5\cos\left(\frac{\pi(t - 2)}{6}\right)",
    r"Midline $\frac{12 + 2}{2} = 7$, amplitude $\frac{12 - 2}{2} = 5$. High to low is half a period, so the period is $12$ and $B = \frac{\pi}{6}$. "
    r"A maximum at $t = 2$: $D(t) = 7 + 5\cos\left(\frac{\pi(t - 2)}{6}\right)$.",
    dB, r"Find the depth of the water at midnight, $t = 0$.", r"9.5 \text{ m}",
    r"$D(0) = 7 + 5\cos\left(-\frac{\pi}{3}\right) = 7 + \frac52 = 9.5$ m.",
    4.5, r"t = 6 \text{ and } t = 10",
    r"$7 + 5\cos\frac{\pi(t - 2)}{6} = 4.5$ gives $\cos\frac{\pi(t - 2)}{6} = -\frac12$, so $\frac{\pi(t - 2)}{6} = \frac{2\pi}{3}$ or $\frac{4\pi}{3}$ (in $\left[-\frac{\pi}{3}, \frac{5\pi}{3}\right)$): $t = 6$ or $t = 10$.",
    r"A boat needs at least $4.5$ meters of water. For how many hours between $t = 0$ and $t = 12$ can it use the harbor? Give a reason for your answer.", r"8 \text{ hours}",
    r"The depth is below $4.5$ m only between $t = 6$ and $t = 10$ (low tide, $t = 8$, is between them), so the boat can use the harbor for $12 - 4 = 8$ hours.", "meters", word="depth")
# part (b) of F1B asks a depth, not a maximum: relabel its rubric
F1B.parts[1].rubric = [(1, "substitutes $t = 0$"), (1, "value with units")]


def ident_frq(show, show_sol, eq_tex, eq_sols, eq_sol, given, s2, c2, c_sol):
    return FRQ("Question 2", r"Answer the following without a calculator.", [
        Part("a", rf"Show that ${show}$ for all $x$ where both sides are defined.", selfcheck(show), show_sol, [(1, "uses an appropriate identity"), (1, "verifies the identity")], work="3.4cm"),
        Part("b", rf"Find all values of $x$ in the interval $0 \le x < 2\pi$ that satisfy ${eq_tex}$. Show the work that leads to your answer.", selfcheck(eq_sols), eq_sol,
             [(1, "rewrites in one trig function"), (1, "factors"), (1, "all solutions, no extras")], work="3.6cm"),
        Part("c", rf"{given} Find the exact values of $\sin 2\theta$ and $\cos 2\theta$.", selfcheck(rf"\sin 2\theta = {s2}, \ \cos 2\theta = {c2}"), c_sol,
             [(1, r"the missing value of $\sin\theta$ or $\cos\theta$, with its sign"), (1, r"$\sin 2\theta$"), (1, r"$\cos 2\theta$")], work="3cm"),
    ], frq_type="Identities and equations")


check("F2A a", all(abs(float(((1 - sp.cos(2 * x)) / sp.sin(2 * x) - sp.tan(x)).subs(x, v))) < 1e-12 for v in (0.3, 1.1, 2.0, 4.0)))
same("F2A b", [2 * sp.cos(v)**2 + 3 * sp.sin(v) - 3 for v in (pi / 6, 5 * pi / 6, pi / 2)], [0, 0, 0])
same("F2A c", [2 * (-2 * r2 / 3) * (-sp.Rational(1, 3)), 2 * sp.Rational(1, 9) - 1], [4 * r2 / 9, -sp.Rational(7, 9)])
F2A = ident_frq(r"\frac{1 - \cos 2x}{\sin 2x} = \tan x",
                r"$\frac{1 - (1 - 2\sin^2 x)}{2\sin x\cos x} = \frac{2\sin^2 x}{2\sin x\cos x} = \frac{\sin x}{\cos x} = \tan x$.",
                r"2\cos^2 x + 3\sin x - 3 = 0", r"x = \frac{\pi}{6}, \ \frac{\pi}{2}, \ \frac{5\pi}{6}",
                r"$2(1 - \sin^2 x) + 3\sin x - 3 = 0$, so $2\sin^2 x - 3\sin x + 1 = 0$ and $(2\sin x - 1)(\sin x - 1) = 0$. $\sin x = \frac12$: $x = \frac{\pi}{6}, \frac{5\pi}{6}$; $\sin x = 1$: $x = \frac{\pi}{2}$.",
                r"$\cos\theta = -\frac13$ and $\pi < \theta < \frac{3\pi}{2}$.", r"\frac{4\sqrt2}{9}", r"-\frac79",
                r"$\sin\theta = -\sqrt{1 - \frac19} = -\frac{2\sqrt2}{3}$ (quadrant III). $\sin 2\theta = 2\left(-\frac{2\sqrt2}{3}\right)\left(-\frac13\right) = \frac{4\sqrt2}{9}$; $\cos 2\theta = 2\cos^2\theta - 1 = -\frac79$.")

check("F2B a", all(abs(float((sp.sec(x) - sp.sin(x) * sp.tan(x) - sp.cos(x)).subs(x, v))) < 1e-12 for v in (0.3, 1.1, 2.0, 4.0)))
same("F2B b", [2 * sp.sin(v)**2 - sp.cos(v) - 1 for v in (pi / 3, pi, 5 * pi / 3)], [0, 0, 0])
same("F2B c", [2 * sp.Rational(2, 5) * (-sp.sqrt(21) / 5), 1 - 2 * sp.Rational(4, 25)], [-4 * sp.sqrt(21) / 25, sp.Rational(17, 25)])
F2B = ident_frq(r"\sec x - \sin x\tan x = \cos x",
                r"$\frac{1}{\cos x} - \frac{\sin^2 x}{\cos x} = \frac{1 - \sin^2 x}{\cos x} = \frac{\cos^2 x}{\cos x} = \cos x$.",
                r"2\sin^2 x - \cos x - 1 = 0", r"x = \frac{\pi}{3}, \ \pi, \ \frac{5\pi}{3}",
                r"$2(1 - \cos^2 x) - \cos x - 1 = 0$, so $2\cos^2 x + \cos x - 1 = 0$ and $(2\cos x - 1)(\cos x + 1) = 0$. $\cos x = \frac12$: $x = \frac{\pi}{3}, \frac{5\pi}{3}$; $\cos x = -1$: $x = \pi$.",
                r"$\sin\theta = \frac25$ and $\frac{\pi}{2} < \theta < \pi$.", r"-\frac{4\sqrt{21}}{25}", r"\frac{17}{25}",
                r"$\cos\theta = -\sqrt{1 - \frac{4}{25}} = -\frac{\sqrt{21}}{5}$ (quadrant II). $\sin 2\theta = 2\cdot\frac25\cdot\left(-\frac{\sqrt{21}}{5}\right) = -\frac{4\sqrt{21}}{25}$; $\cos 2\theta = 1 - 2\sin^2\theta = \frac{17}{25}$.")
# the solution sets in (b) are complete: checked numerically by 0.6's root scan
from content.topic_0_6 import roots  # noqa: E402
same("F2 counts", [len(roots(2 * sp.cos(x)**2 + 3 * sp.sin(x) - 3)), len(roots(2 * sp.sin(x)**2 - sp.cos(x) - 1))], [3, 3])


def triangle_frq(intro, a_prompt, a_ans, a_sol, b_prompt, b_ans, b_sol, c_prompt, c_ans, c_sol, d_prompt, d_ans, d_sol):
    return FRQ("Question 3", intro, [
        Part("a", a_prompt, a_ans, a_sol, [(1, "inverse tangent setup"), (1, "answer in degrees")], work="2.4cm"),
        Part("b", b_prompt, selfcheck(b_ans), b_sol, [(1, "triangle sides"), (1, "both exact values")], work="2.4cm"),
        Part("c", c_prompt, c_ans, c_sol, [(1, "setup"), (1, "answer with units")], work="2.4cm"),
        Part("d", d_prompt, d_ans, d_sol, [(1, "answer with units")], work="1.6cm"),
    ], calc=True, frq_type="Right triangles")


cA = float(30 / sp.tan(deg(20)))
close("F3A", float(sp.atan(sp.Rational(3, 4)) * 180 / pi), 36.87, 0.005)
close("F3A c", cA, 82.42, 0.005)
F3A = triangle_frq(
    r"A lighthouse stands on the shore. The top of the lighthouse is $30$ meters above the water. A boat is $40$ meters from the base of the lighthouse. "
    r"The angle of depression from the top of the lighthouse to the boat is $\theta$ (equal to the angle of elevation from the boat to the top).",
    r"Find $\theta$ in degrees. Show the work that leads to your answer.", num(sp.atan(sp.Rational(3, 4)) * 180 / pi, tol=0.01),
    r"$\tan\theta = \frac{30}{40}$, so $\theta = \arctan\frac34 \approx 36.87^\circ$.",
    r"Without using a calculator, find the exact values of $\sin\theta$ and $\cos\theta$.", r"\sin\theta = \frac35, \ \cos\theta = \frac45",
    r"The line of sight is the hypotenuse: $\sqrt{30^2 + 40^2} = 50$. $\sin\theta = \frac{30}{50} = \frac35$, $\cos\theta = \frac{40}{50} = \frac45$.",
    r"Later, the angle of depression to the boat is $20^\circ$. How far is the boat from the base of the lighthouse then? Indicate units of measure.", num(cA, tol=0.01),
    r"$\tan 20^\circ = \frac{30}{d}$, so $d = \frac{30}{\tan 20^\circ} \approx 82.42$ meters.",
    r"How far did the boat move between the two sightings, assuming it moved directly away from the lighthouse? Indicate units of measure.", num(cA - 40, tol=0.01),
    rf"$82.42 - 40 \approx 42.42$ meters.")

cB = float(120 / sp.tan(deg(50)))
close("F3B", float(sp.atan(sp.Rational(12, 5)) * 180 / pi), 67.38, 0.005)
close("F3B c", cB, 100.69, 0.005)
F3B = triangle_frq(
    r"A drone hovers $120$ meters directly above a point $P$ on level ground. An observer stands on the ground $50$ meters from $P$. "
    r"The angle of elevation from the observer to the drone is $\theta$.",
    r"Find $\theta$ in degrees. Show the work that leads to your answer.", num(sp.atan(sp.Rational(12, 5)) * 180 / pi, tol=0.01),
    r"$\tan\theta = \frac{120}{50}$, so $\theta = \arctan\frac{12}{5} \approx 67.38^\circ$.",
    r"Without using a calculator, find the exact values of $\cos\theta$ and $\tan\theta$.", r"\cos\theta = \frac{5}{13}, \ \tan\theta = \frac{12}{5}",
    r"The line of sight is $\sqrt{120^2 + 50^2} = 130$. $\cos\theta = \frac{50}{130} = \frac{5}{13}$, $\tan\theta = \frac{120}{50} = \frac{12}{5}$.",
    r"The observer walks directly away from $P$ until the angle of elevation is $50^\circ$; the drone does not move. How far is the observer from $P$ then? Indicate units of measure.", num(cB, tol=0.01),
    r"$\tan 50^\circ = \frac{120}{d}$, so $d = \frac{120}{\tan 50^\circ} \approx 100.69$ meters.",
    r"How far did the observer walk? Indicate units of measure.", num(cB - 50, tol=0.01),
    r"$100.69 - 50 \approx 50.69$ meters.")

TEST = UnitTest(unit=0, title="Trig Review", mcq_a=A, mcq_b=B, frq=[Variants(F1A, F1B), Variants(F2A, F2B), Variants(F3A, F3B)])
