"""Trig Review lesson 0.1 (T1): Right-triangle trigonometry (trig review; not a CED topic).

Plain SOH CAH TOA in degrees (Adder, 2026-10-08: "good old SOH CAH TOA stuff"): hypotenuse, opposite and adjacent named
from an angle; similar triangles share their ratios; sine, cosine, tangent and their flips cosecant, secant, cotangent;
finding a side (unknown on top, then on the bottom); finding an angle with the inverse keys; angles of elevation and
depression. Lesson examples: legs 8 and 15, a tree's height, the angle up to a rooftop. Worked examples: a ladder, a kite
string, a skateboard ramp, solving a whole triangle.
"""
import sympy as sp

from calclib import (VideoExample, MCQ, BigIdea, Check, Formula, Item, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)
from calclib.figs import triangle

pi = sp.pi
deg = lambda d: d * pi / 180
D = lambda r: float(r * 180 / pi)          # radians -> degrees, for inverse-key answers
same("lesson", [sp.sqrt(8**2 + 15**2)], [17])
close("tree", float(20 * sp.tan(deg(35))), 14.0, 0.05)
close("roof", D(sp.atan(sp.Rational(3, 5))), 31.0, 0.05)
close("ex1", float(6 * sp.sin(deg(70))), 5.64, 0.005)
close("ex2", float(30 / sp.sin(deg(40))), 46.7, 0.05)
close("ex3", D(sp.asin(sp.Rational(3, 10))), 17.5, 0.05)
close("ex4", float(12 * sp.sin(deg(25))), 5.07, 0.005)
close("ex4b", float(12 * sp.cos(deg(25))), 10.88, 0.005)

FIG_SOH = triangle("t0_1_soh", 4, 3, opp="opposite", adj="adjacent", hyp="hypotenuse", caption="Sides named from the angle $\\theta$.")

NOTES = [
    Video("s0_1.py::Lesson", "Right-triangle trigonometry", 10),

    Section("Naming the sides"),
    Text(r"The side across from the right angle is the \textbf{hypotenuse}, the longest side. Pick one of the other angles and call it $\theta$: "
         r"the leg across from $\theta$ is the \textbf{opposite} side, and the leg touching $\theta$ is the \textbf{adjacent} side. "
         r"Switch to the other acute angle and opposite and adjacent trade places; the hypotenuse never changes."),
    FIG_SOH,

    Section("The three ratios"),
    Text(r"Right triangles with the same acute angle have the same shape, so the ratio of any two sides depends only on the angle, not on the size of the triangle."),
    Formula("SOH CAH TOA", r"\[ \sin\theta = \blank{\frac{\text{opposite}}{\text{hypotenuse}}}, \qquad \cos\theta = \blank{\frac{\text{adjacent}}{\text{hypotenuse}}}, \qquad \tan\theta = \blank{\frac{\text{opposite}}{\text{adjacent}}}. \]"),
    VideoExample("Ratios from sides", work="3cm"),

    Section("The reciprocal ratios"),
    Formula("Cosecant, secant, cotangent", r"\[ \csc\theta = \frac{\text{hypotenuse}}{\text{opposite}} = \frac{1}{\sin\theta}, \qquad \sec\theta = \frac{\text{hypotenuse}}{\text{adjacent}} = \frac{1}{\cos\theta}, \qquad "
            r"\cot\theta = \frac{\text{adjacent}}{\text{opposite}} = \frac{1}{\tan\theta}. \] Memory tip: each pair has exactly one ``co'': sine with \textbf{co}secant, \textbf{co}sine with secant."),

    Section("Finding a side"),
    Text(r"Name the sides from the angle you know, pick the ratio that uses the side you know and the side you want, then solve. "
         r"Set the calculator to \textbf{degree mode} for angles in degrees."),
    VideoExample("Finding a side", work="2.6cm"),

    Section("Finding an angle"),
    Text(r"The inverse keys $\sin^{-1}$, $\cos^{-1}$ and $\tan^{-1}$ run a ratio backward: a ratio goes in and the angle comes out. "
         r"$\tan 35^\circ \approx 0.7002$, so $\tan^{-1}(0.7002) \approx 35^\circ$. (Lesson T8 covers them in detail.) "
         r"The angle up from the horizontal to a line of sight is the \textbf{angle of elevation}; the angle down from the horizontal is the \textbf{angle of depression}."),
    VideoExample("Finding an angle", work="2.4cm"),
    BigIdea(r"In a right triangle the angle fixes the ratios of the sides. Know one side and one acute angle and you can find every side; know two sides and you can find the angles."),
    Check(r"A right triangle has hypotenuse $10$ and a leg of $6$ opposite the angle $\theta$. Find $\cos\theta$.", selfcheck(r"\frac45"),
          r"The other leg is $\sqrt{100 - 36} = 8$, so $\cos\theta = \frac{8}{10} = \frac45$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    MCQ(r"In a right triangle, the hypotenuse is", ["the side opposite the right angle", r"the side opposite $\theta$", r"the side adjacent to $\theta$", "the shortest side"], "A",
        r"It is across from the $90^\circ$ angle, and it is always the longest side.", {"D": "the hypotenuse is the longest side"}),
    Item(r"A right triangle has legs $3$ and $4$. $\theta$ is opposite the side of length $3$. Find $\cos\theta$.", num(sp.Rational(4, 5), display=r"\frac45"), r"Hypotenuse $5$; $\cos\theta = \frac{\text{adj}}{\text{hyp}} = \frac45$.", work="1.2cm"),
    Item(r"A right triangle has hypotenuse $13$ and one leg $5$. $\theta$ is opposite the leg of length $5$. Find $\tan\theta$.", num(sp.Rational(5, 12), display=r"\frac{5}{12}"),
         r"Other leg $\sqrt{169 - 25} = 12$; $\tan\theta = \frac{5}{12}$.", work="1.4cm"),
    Item(r"A right triangle has legs $7$ and $24$. $\theta$ is opposite the side of length $7$. Find $\sec\theta$.", num(sp.Rational(25, 24), display=r"\frac{25}{24}"),
         r"Hypotenuse $\sqrt{49 + 576} = 25$; $\sec\theta = \frac{\text{hyp}}{\text{adj}} = \frac{25}{24}$.", work="1.4cm"),
    Item(r"In a right triangle, $\sin\theta = \frac{3}{5}$. Find $\csc\theta$ and $\cot\theta$.", selfcheck(r"\csc\theta = \frac53, \ \cot\theta = \frac43"),
         r"Opposite $3$, hypotenuse $5$, so adjacent $4$. $\csc\theta = \frac53$, $\cot\theta = \frac43$.", work="1.4cm"),
    Item(r"A kite string $50$ m long makes a $40^\circ$ angle with the ground. How high is the kite, to the nearest tenth of a meter?", num(50 * sp.sin(deg(40)), tol=0.05),
         r"$\sin 40^\circ = \frac{h}{50}$, so $h = 50\sin 40^\circ \approx 32.1$ m.", work="1.4cm", calc=True),
    Item(r"Ana stands $15$ m from the base of a flagpole. The angle of elevation to its top is $52^\circ$. How tall is the flagpole, to the nearest tenth of a meter?", num(15 * sp.tan(deg(52)), tol=0.05),
         r"$\tan 52^\circ = \frac{h}{15}$, so $h = 15\tan 52^\circ \approx 19.2$ m.", work="1.4cm", calc=True),
    Item(r"A wire runs from the top of a $9$ m pole to the ground, making a $62^\circ$ angle with the ground. How long is the wire, to the nearest tenth of a meter?", num(9 / sp.sin(deg(62)), tol=0.05),
         r"$\sin 62^\circ = \frac{9}{L}$, so $L = \frac{9}{\sin 62^\circ} \approx 10.2$ m.", work="1.6cm", calc=True),
    Item(r"From the top of a $40$ m cliff, the angle of depression to a boat is $25^\circ$. How far is the boat from the base of the cliff, to the nearest meter?", num(40 / sp.tan(deg(25)), tol=0.5),
         r"The angle of elevation from the boat is also $25^\circ$: $\tan 25^\circ = \frac{40}{d}$, so $d = \frac{40}{\tan 25^\circ} \approx 86$ m.", work="1.6cm", calc=True),
    Item(r"A ramp rises $1.2$ m over a horizontal distance of $8$ m. Find the angle it makes with the ground, in degrees, to the nearest tenth.", num(D(sp.atan(sp.Rational(3, 20))), tol=0.05),
         r"$\tan\theta = \frac{1.2}{8} = 0.15$, $\theta = \tan^{-1}(0.15) \approx 8.5^\circ$.", work="1.4cm", calc=True),
    Item(r"A $5$ m ladder leans against a wall with its foot $1.5$ m from the wall. Find the angle between the ladder and the ground, to the nearest tenth of a degree.", num(D(sp.acos(sp.Rational(3, 10))), tol=0.05),
         r"$\cos\theta = \frac{1.5}{5} = 0.3$, $\theta = \cos^{-1}(0.3) \approx 72.5^\circ$.", work="1.4cm", calc=True),
    Item(r"A right triangle has a leg of $10$ adjacent to a $38^\circ$ angle. Find the other acute angle, the other leg, and the hypotenuse, to the nearest hundredth.",
         selfcheck(r"52^\circ, \ 7.81, \ 12.69"), r"$90^\circ - 38^\circ = 52^\circ$; opposite $= 10\tan 38^\circ \approx 7.81$; hypotenuse $= \frac{10}{\cos 38^\circ} \approx 12.69$.", work="2cm", calc=True),
]
close("p6", float(50 * sp.sin(deg(40))), 32.14, 0.01)
close("p7", float(15 * sp.tan(deg(52))), 19.20, 0.01)
close("p8", float(9 / sp.sin(deg(62))), 10.19, 0.01)
close("p9", float(40 / sp.tan(deg(25))), 85.78, 0.01)
close("p10", D(sp.atan(0.15)), 8.53, 0.01)
close("p11", D(sp.acos(0.3)), 72.54, 0.01)
close("p12", float(10 * sp.tan(deg(38))), 7.81, 0.005)
close("p12b", float(10 / sp.cos(deg(38))), 12.69, 0.005)

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"A right triangle has legs $7$ and $24$. $\theta$ is opposite the side of length $7$. Find $\sin\theta$.", num(sp.Rational(7, 25), display=r"\frac{7}{25}"), r"Hypotenuse $25$; $\frac{\text{opp}}{\text{hyp}} = \frac{7}{25}$.", work="1.2cm"),
        Item(r"A right triangle has legs $9$ and $40$. $\theta$ is opposite the side of length $40$. Find $\cos\theta$.", num(sp.Rational(9, 41), display=r"\frac{9}{41}"), r"Hypotenuse $41$; adjacent $9$.", work="1.2cm"),
        Item(r"A right triangle has legs $20$ and $21$. $\theta$ is opposite the side of length $20$. Find $\tan\theta$.", num(sp.Rational(20, 21), display=r"\frac{20}{21}"), r"Opposite over adjacent.", work="1.2cm"),
    ),
    Variants(
        Item(r"A right triangle has legs $5$ and $12$. $\theta$ is opposite the side of length $5$. Find $\csc\theta$.", num(sp.Rational(13, 5), display=r"\frac{13}{5}"), r"Hypotenuse $13$; $\frac{\text{hyp}}{\text{opp}} = \frac{13}{5}$.", work="1.2cm"),
        Item(r"A right triangle has legs $8$ and $15$. $\theta$ is opposite the side of length $8$. Find $\sec\theta$.", num(sp.Rational(17, 15), display=r"\frac{17}{15}"), r"Hypotenuse $17$; $\frac{\text{hyp}}{\text{adj}} = \frac{17}{15}$.", work="1.2cm"),
        Item(r"A right triangle has legs $6$ and $8$. $\theta$ is opposite the side of length $8$. Find $\cot\theta$.", num(sp.Rational(3, 4), display=r"\frac34"), r"$\frac{\text{adj}}{\text{opp}} = \frac{6}{8} = \frac34$.", work="1.2cm"),
    ),
    Variants(
        Item(r"A $10$ m ladder makes a $65^\circ$ angle with the ground. How high up the wall does it reach, to the nearest hundredth of a meter?", num(10 * sp.sin(deg(65)), tol=0.01), r"$10\sin 65^\circ \approx 9.06$ m.", work="1.2cm", calc=True),
        Item(r"From $40$ m away, the angle of elevation to the top of a building is $52^\circ$. How tall is it, to the nearest tenth of a meter?", num(40 * sp.tan(deg(52)), tol=0.05), r"$40\tan 52^\circ \approx 51.2$ m.", work="1.2cm", calc=True),
    ),
    Variants(
        Item(r"A kite is $25$ m above the ground, and its string makes a $35^\circ$ angle with the ground. How long is the string, to the nearest tenth of a meter?", num(25 / sp.sin(deg(35)), tol=0.05),
             r"$\sin 35^\circ = \frac{25}{L}$, so $L = \frac{25}{\sin 35^\circ} \approx 43.6$ m.", work="1.4cm", calc=True),
        Item(r"From the top of a $60$ m tower, the angle of depression to a car is $18^\circ$. How far is the car from the base of the tower, to the nearest meter?", num(60 / sp.tan(deg(18)), tol=0.5),
             r"$\tan 18^\circ = \frac{60}{d}$, so $d = \frac{60}{\tan 18^\circ} \approx 185$ m.", work="1.4cm", calc=True),
    ),
    Variants(
        Item(r"A slide is $3$ m long and its top is $1.8$ m above the ground. Find the angle the slide makes with the ground, to the nearest tenth of a degree.", num(D(sp.asin(sp.Rational(3, 5))), tol=0.05),
             r"$\sin\theta = \frac{1.8}{3} = 0.6$, $\theta = \sin^{-1}(0.6) \approx 36.9^\circ$.", work="1.2cm", calc=True),
        Item(r"Kenji stands $35$ m from a tower $20$ m tall. Find the angle of elevation from where he stands to the top, to the nearest tenth of a degree.", num(D(sp.atan(sp.Rational(4, 7))), tol=0.05),
             r"$\tan\theta = \frac{20}{35}$, $\theta = \tan^{-1}\left(\frac{4}{7}\right) \approx 29.7^\circ$.", work="1.2cm", calc=True),
    ),
]
close("q4a", float(25 / sp.sin(deg(35))), 43.59, 0.01)
close("q4b", float(60 / sp.tan(deg(18))), 184.66, 0.01)
close("q5", D(sp.asin(0.6)), 36.87, 0.01)
close("q5b", D(sp.atan(sp.Rational(4, 7))), 29.74, 0.01)

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"In a right triangle, $\sin\theta = \frac{5}{13}$. Then $\tan\theta = $", [r"$\frac{12}{13}$", r"$\frac{5}{12}$", r"$\frac{13}{12}$", r"$\frac{12}{5}$"], "B",
        r"Legs $5$ and $12$, hypotenuse $13$: $\tan\theta = \frac{5}{12}$.", {"A": r"that is $\cos\theta$", "D": r"that is $\cot\theta$"}),
    MCQ(r"A plane takes off at a $12^\circ$ angle and flies in a straight line. After it has flown $3000$ m, what is its altitude, to the nearest meter?",
        [r"$638$ m", r"$2934$ m", r"$14{,}114$ m", r"$624$ m"], "D", r"$3000\sin 12^\circ \approx 623.7$.", {"A": r"that uses $\tan 12^\circ$", "B": r"that is the horizontal distance"}, calc=True),
    MCQ(r"A ramp's surface is $6$ m long and its high end is $1.5$ m off the ground. Which equation gives the angle $\theta$ the ramp makes with the ground?",
        [r"$\theta = \tan^{-1}\left(\frac{1.5}{6}\right)$", r"$\theta = \sin^{-1}\left(\frac{1.5}{6}\right)$", r"$\theta = \cos^{-1}\left(\frac{1.5}{6}\right)$", r"$\theta = \sin\left(\frac{1.5}{6}\right)$"], "B",
        r"The height is opposite $\theta$ and the surface is the hypotenuse: $\sin\theta = \frac{1.5}{6}$.", {"A": r"$6$ m is the hypotenuse, not the adjacent side", "D": "an angle comes from the inverse key"}),
    MCQ(r"From the top of a lighthouse $30$ m tall, the angle of depression to a boat is $15^\circ$. To the nearest meter, how far is the boat from the base of the lighthouse?",
        [r"$8$ m", r"$31$ m", r"$112$ m", r"$116$ m"], "C", r"$\tan 15^\circ = \frac{30}{d}$, so $d = \frac{30}{\tan 15^\circ} \approx 112$ m.",
        {"A": r"that is $30\tan 15^\circ$", "D": r"that is the line of sight, $\frac{30}{\sin 15^\circ}$"}, calc=True),
]
close("m2", float(3000 * sp.sin(deg(12))), 623.7, 0.05)
close("m2b", float(3000 * sp.tan(deg(12))), 637.7, 0.1)
close("m4", float(30 / sp.tan(deg(15))), 111.96, 0.01)
close("m4b", float(30 / sp.sin(deg(15))), 115.91, 0.01)
close("m4c", float(30 * sp.tan(deg(15))), 8.04, 0.01)

FRQS = []

TOPIC = Topic(
    number="0.1", title="Right-Triangle Trigonometry",
    unit="Trig Review (a free module)", ced=["Prerequisite: right-triangle trigonometry"],
    goals=r"Name the sides of a right triangle from an angle, use SOH CAH TOA and the reciprocal ratios, and find missing sides and angles in degrees.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
