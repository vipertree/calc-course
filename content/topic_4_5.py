"""Topic 4.5: Solving related rates problems.

CED: CHA-3.E (CHA-3.E.1): the full procedure, with geometry (Pythagorean theorem, similar triangles, volume formulas,
right-triangle trig) to relate the quantities. Worked examples: a sliding 13-ft ladder, a conical tank (similar triangles),
two cars leaving an intersection.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Text, Topic, Variants, Video, expr, num,
                     same, selfcheck)

t = sp.symbols("t")
x, y, z, r, h, V, s, th = [sp.Function(n)(t) for n in ("x", "y", "z", "r", "h", "V", "s", "th")]
d = lambda f: sp.diff(f, t)


def solve_rate(lhs, rhs, want, known):
    sol = sp.solve(sp.Eq(d(lhs), d(rhs)), d(want))[0]
    return sp.simplify(sol.subs(known))


same("ladder", solve_rate(x**2 + y**2, 169, y, {d(x): 2, x: 5, y: 12}), sp.Rational(-5, 6))
same("cone", solve_rate(sp.pi / 27 * h**3, V, h, {d(V): 2, h: 6}), 1 / (2 * sp.pi))
same("cars", solve_rate(z**2, x**2 + y**2, z, {d(x): 40, d(y): 30, x: 80, y: 60, z: 100}), 50)

NOTES = [
    Video("s4_5.py::Lesson", "Solving related rates", 5),

    Section("A procedure"),
    Formula("Solving a related rates problem", (
        r"\textbf{1.} Draw a picture. Label every quantity that \blank{changes} with a variable, and every constant with its number. \par "
        r"\textbf{2.} Write down the given rates and the rate you want, with signs: shrinking quantities have \blank{negative} rates. \par "
        r"\textbf{3.} Write an equation relating the quantities. \par "
        r"\textbf{4.} Differentiate with respect to $t$. \par "
        r"\textbf{5.} Substitute the values \emph{at the moment asked about}, and solve. Answer with units.")),

    Section("Where the equation comes from"),
    Text(r"Most equations come from a few sources: the \blank{Pythagorean theorem} for right triangles, \blank{similar triangles} for shadows "
         r"and cones, volume and area formulas, and right-triangle trig for angles."),
    Text(r"\textbf{Eliminate first.} If a problem gives a rate for only one of two linked variables (like $r$ and $h$ in a cone with fixed "
         r"proportions), use the geometry to write one variable in terms of the other \emph{before} differentiating."),
    VideoExample('A shadow', work="3cm"),
    BigIdea(r"Picture, rates with signs, an equation that holds at every moment, differentiate, then substitute the values at the moment asked."),
    Check(r"In a related rates problem, a quantity is shrinking at $3$ cm/s. What value do you use for its rate?", num(-3),
          r"$-3$ cm/s: shrinking means a negative rate."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"A $10$-ft ladder leans against a wall. The bottom slides away at $1$ ft/s. How fast does the top slide down when the bottom is $6$ ft from the wall?",
         num(sp.Rational(-3, 4)), r"$x^2 + y^2 = 100$; at $x = 6$, $y = 8$. $2(6)(1) + 2(8)\dfrac{dy}{dt} = 0$, so $\dfrac{dy}{dt} = -\frac34$ ft/s.", work="2.6cm"),
    Item(r"A $25$-ft ladder slides so that its top falls at $2$ ft/s. How fast is the bottom moving when the top is $7$ ft high?", num(sp.Rational(7, 12)),
         r"At $y = 7$, $x = 24$. $2(24)\dfrac{dx}{dt} + 2(7)(-2) = 0$, so $\dfrac{dx}{dt} = \frac{7}{12}$ ft/s.", work="2.6cm"),
    Item(r"Water drains from a cone (point down) with radius $3$ m and height $6$ m at $2$ m$^3$/min. How fast is the depth falling when it is $4$ m?",
         num(-1 / (2 * sp.pi)), r"$r = \frac h2$, so $V = \frac{\pi}{12}h^3$. $-2 = \frac{\pi}{4}h^2\dfrac{dh}{dt} = 4\pi\dfrac{dh}{dt}$, so $\dfrac{dh}{dt} = -\frac{1}{2\pi}$ m/min.",
         work="2.8cm"),
    Item(r"Sand pours into a conical pile whose height always equals its radius, at $9\pi$ ft$^3$/min. How fast is the height rising when $h = 3$ ft?", num(1),
         r"$V = \frac{\pi}{3}h^3$, so $9\pi = \pi h^2\dfrac{dh}{dt} = 9\pi\dfrac{dh}{dt}$: $\dfrac{dh}{dt} = 1$ ft/min.", work="2.4cm"),
    Item(r"Two cyclists leave the same point, one north at $12$ mph and one east at $16$ mph. How fast is the distance between them growing after $1$ hour?",
         num(20), r"$x = 16$, $y = 12$, $z = 20$. $20\dfrac{dz}{dt} = 16(16) + 12(12) = 400$, so $\dfrac{dz}{dt} = 20$ mph.", work="2.6cm"),
    Item(r"A spherical balloon is inflated at $36\pi$ cm$^3$/s. How fast is the radius growing when $r = 3$ cm?", num(1),
         r"$36\pi = 4\pi(9)\dfrac{dr}{dt}$, so $\dfrac{dr}{dt} = 1$ cm/s.", work="2cm"),
    Item(r"For the same balloon, how fast is the surface area $S = 4\pi r^2$ growing when $r = 3$ cm?", num(24 * sp.pi),
         r"$\dfrac{dS}{dt} = 8\pi r\dfrac{dr}{dt} = 8\pi(3)(1) = 24\pi$ cm$^2$/s.", work="2cm"),
    Item(r"A $6$-ft man walks toward an $18$-ft lamppost at $3$ ft/s. How fast is his shadow changing?", num(sp.Rational(-3, 2)),
         r"$\frac{18}{x + s} = \frac{6}{s}$ gives $s = \frac x2$, so $\dfrac{ds}{dt} = \frac12(-3) = -1.5$ ft/s: shrinking.", work="2.6cm"),
    Item(r"A kite flies at a height of $60$ ft and drifts horizontally away at $5$ ft/s. How fast is the string being let out when $80$ ft of horizontal distance separate the kite and the flyer?",
         num(4), r"$z^2 = x^2 + 60^2$; at $x = 80$, $z = 100$. $100\dfrac{dz}{dt} = 80(5)$, so $\dfrac{dz}{dt} = 4$ ft/s.", work="2.6cm"),
    Item(r"A cylindrical tank of radius $2$ m fills at $8\pi$ m$^3$/min. How fast does the water level rise?", num(2),
         r"$V = 4\pi h$, so $8\pi = 4\pi\dfrac{dh}{dt}$ and $\dfrac{dh}{dt} = 2$ m/min.", work="2cm"),
    Item(r"A plane flies horizontally at $6$ km altitude, at $500$ km/h, directly over a radar station. How fast is the distance to the station growing when it is $10$ km away?",
         num(400), r"$z^2 = x^2 + 36$; at $z = 10$, $x = 8$. $10\dfrac{dz}{dt} = 8(500)$, so $\dfrac{dz}{dt} = 400$ km/h.", work="2.6cm"),
    Item(r"A square's diagonal grows at $\sqrt2$ cm/s. How fast is its area growing when the side is $5$ cm?", num(10),
         r"$A = \frac{D^2}{2}$, so $\dfrac{dA}{dt} = D\dfrac{dD}{dt} = 5\sqrt2\cdot\sqrt2 = 10$ cm$^2$/s.", work="2.4cm"),
    Item(r"Lin watches a balloon rise straight up at $4$ m/s from a point $30$ m away. How fast is the angle of elevation $\theta$ increasing when the balloon is $30$ m high?",
         num(sp.Rational(1, 15)), r"$\tan\theta = \frac{y}{30}$. $\sec^2\theta\,\dfrac{d\theta}{dt} = \frac{1}{30}\dfrac{dy}{dt}$. At $y = 30$, $\theta = \frac\pi4$, $\sec^2\theta = 2$: "
         r"$2\dfrac{d\theta}{dt} = \frac{4}{30}$, so $\dfrac{d\theta}{dt} = \frac{1}{15}$ rad/s.", work="2.8cm"),
    Item(r"Oil spreads in a circle whose area grows at $50$ m$^2$/min. How fast is the radius growing when $r = 5$ m?", num(5 / sp.pi),
         r"$50 = 2\pi(5)\dfrac{dr}{dt}$, so $\dfrac{dr}{dt} = \frac{5}{\pi}$ m/min.", work="2cm"),
]
th0 = sp.symbols("theta")
same("p", [solve_rate(x**2 + y**2, 100, y, {d(x): 1, x: 6, y: 8}), solve_rate(x**2 + y**2, 625, x, {d(y): -2, x: 24, y: 7}),
           solve_rate(sp.pi / 12 * h**3, V, h, {d(V): -2, h: 4}), solve_rate(sp.pi / 3 * h**3, V, h, {d(V): 9 * sp.pi, h: 3}),
           solve_rate(z**2, x**2 + y**2, z, {d(x): 16, d(y): 12, x: 16, y: 12, z: 20}), solve_rate(sp.Rational(4, 3) * sp.pi * r**3, V, r, {d(V): 36 * sp.pi, r: 3}),
           solve_rate(z**2, x**2 + 3600, z, {d(x): 5, x: 80, z: 100}), solve_rate(z**2, x**2 + 36, z, {d(x): 500, x: 8, z: 10}),
           solve_rate(sp.tan(th), y / 30, th, {d(y): 4, th: sp.pi / 4}), solve_rate(sp.pi * r**2, V, r, {d(V): 50, r: 5})],
     [sp.Rational(-3, 4), sp.Rational(7, 12), -1 / (2 * sp.pi), 1, 20, 1, 4, 400, sp.Rational(1, 15), 5 / sp.pi])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"A $13$-ft ladder slides away from a wall at $3$ ft/s at the bottom. How fast does the top fall when the bottom is $12$ ft out?", num(sp.Rational(-36, 5)),
             r"$y = 5$. $2(12)(3) + 2(5)\dfrac{dy}{dt} = 0$, so $\dfrac{dy}{dt} = -7.2$ ft/s.", work="2.4cm"),
        Item(r"A $17$-ft ladder slides away from a wall at $2$ ft/s at the bottom. How fast does the top fall when the bottom is $8$ ft out?", num(sp.Rational(-16, 15)),
             r"$y = 15$. $2(8)(2) + 2(15)\dfrac{dy}{dt} = 0$, so $\dfrac{dy}{dt} = -\frac{16}{15}$ ft/s.", work="2.4cm"),
        Item(r"A $5$-m ladder slides away from a wall at $1$ m/s at the bottom. How fast does the top fall when the bottom is $3$ m out?", num(sp.Rational(-3, 4)),
             r"$y = 4$. $2(3)(1) + 2(4)\dfrac{dy}{dt} = 0$, so $\dfrac{dy}{dt} = -\frac34$ m/s.", work="2.4cm"),
    ),
    Variants(
        Item(r"Two cars leave an intersection: one north at $30$ mph, one east at $40$ mph. How fast is the distance between them growing after $1$ hour?", num(50),
             r"$x = 40$, $y = 30$, $z = 50$: $50\dfrac{dz}{dt} = 40(40) + 30(30) = 2500$, so $50$ mph.", work="2.4cm"),
        Item(r"Two boats leave a dock: one south at $5$ km/h, one west at $12$ km/h. How fast is the distance between them growing after $2$ hours?", num(13),
             r"$x = 24$, $y = 10$, $z = 26$: $26\dfrac{dz}{dt} = 24(12) + 10(5) = 338$, so $13$ km/h.", work="2.4cm"),
        Item(r"Two runners leave a corner: one north at $6$ m/s, one east at $8$ m/s. How fast is the distance between them growing after $5$ s?", num(10),
             r"$x = 40$, $y = 30$, $z = 50$: $50\dfrac{dz}{dt} = 40(8) + 30(6) = 500$, so $10$ m/s.", work="2.4cm"),
    ),
    Variants(
        Item(r"A sphere's volume grows at $100\pi$ cm$^3$/s. How fast is the radius growing when $r = 5$ cm?", num(1), r"$100\pi = 4\pi(25)\dfrac{dr}{dt}$.", work="1.8cm"),
        Item(r"A sphere's volume grows at $64\pi$ cm$^3$/s. How fast is the radius growing when $r = 4$ cm?", num(1), r"$64\pi = 4\pi(16)\dfrac{dr}{dt}$.", work="1.8cm"),
        Item(r"A sphere's volume shrinks at $8\pi$ cm$^3$/s. How fast is the radius changing when $r = 2$ cm?", num(sp.Rational(-1, 2)), r"$-8\pi = 4\pi(4)\dfrac{dr}{dt}$.", work="1.8cm"),
    ),
    Variants(
        MCQ(r"A conical tank (point down) has radius $5$ and height $10$. To relate $V$ to $h$ alone, use", [r"$r = 2h$", r"$r = \frac h2$", r"$r = 5$", r"$h = 10$"], "B",
            r"Similar triangles: $\frac rh = \frac{5}{10}$.", why_not={"C": "the water's radius changes as it fills"}),
        MCQ(r"A conical tank (point down) has radius $6$ and height $3$. To relate $V$ to $h$ alone, use", [r"$r = \frac h2$", r"$r = 6$", r"$r = 2h$", r"$h = 3$"], "C",
            r"Similar triangles: $\frac rh = \frac63$."),
        MCQ(r"A conical tank (point down) has radius $4$ and height $12$. To relate $V$ to $h$ alone, use", [r"$r = 3h$", r"$r = \frac h3$", r"$r = 4$", r"$h = 12$"], "B",
            r"Similar triangles: $\frac rh = \frac{4}{12}$."),
    ),
    Variants(
        MCQ(r"In a related rates problem, when should you substitute the numbers for the instant asked about?", [r"Before writing the equation",
            r"Before differentiating", r"After differentiating", r"Never"], "C", r"Quantities that change must stay variables until you have differentiated."),
        MCQ(r"A balloon is deflating. The sign of $\dfrac{dV}{dt}$ is", [r"positive", r"negative", r"zero", r"it depends on $r$"], "B", r"Decreasing volume: negative rate."),
        MCQ(r"Which equation relates a ladder's bottom distance $x$ and top height $y$ for a $10$-ft ladder?", [r"$x + y = 10$", r"$x^2 + y^2 = 100$",
            r"$xy = 10$", r"$y = 10 - x$"], "B", r"The ladder is the hypotenuse of a right triangle."),
    ),
]
same("q", [solve_rate(x**2 + y**2, 169, y, {d(x): 3, x: 12, y: 5}), solve_rate(x**2 + y**2, 289, y, {d(x): 2, x: 8, y: 15}),
           solve_rate(x**2 + y**2, 25, y, {d(x): 1, x: 3, y: 4}), solve_rate(z**2, x**2 + y**2, z, {d(x): 12, d(y): 5, x: 24, y: 10, z: 26}),
           solve_rate(z**2, x**2 + y**2, z, {d(x): 8, d(y): 6, x: 40, y: 30, z: 50}), solve_rate(sp.Rational(4, 3) * sp.pi * r**3, V, r, {d(V): -8 * sp.pi, r: 2})],
     [sp.Rational(-36, 5), sp.Rational(-16, 15), sp.Rational(-3, 4), 13, 10, sp.Rational(-1, 2)])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"Water flows into a cone (point down) of radius $2$ ft and height $8$ ft at $\pi$ ft$^3$/min. How fast is the depth rising when it is $4$ ft?",
        [r"$1$ ft/min", r"$\frac14$ ft/min", r"$\frac{1}{16}$ ft/min", r"$4$ ft/min"], "A",
        r"$r = \frac h4$, $V = \frac{\pi}{48}h^3$. $\pi = \frac{\pi}{16}h^2\dfrac{dh}{dt} = \pi\dfrac{dh}{dt}$ at $h = 4$, so $1$ ft/min."),
    MCQ(r"A point moves along $y = x^2$ with $\dfrac{dx}{dt} = 3$. How fast is its distance from the origin changing at $(1, 1)$?",
        [r"$3\sqrt2$", r"$\dfrac{9}{\sqrt2}$", r"$9$", r"$\dfrac{3}{\sqrt2}$"], "B",
        r"$D^2 = x^2 + x^4$, so $2D\dfrac{dD}{dt} = (2x + 4x^3)\dfrac{dx}{dt} = 18$ at $x = 1$, and $D = \sqrt2$: $\dfrac{dD}{dt} = \frac{9}{\sqrt2}$."),
    MCQ(r"The edge of a cube grows at $2$ cm/s. When the volume is $27$ cm$^3$, the surface area grows at", [r"$24$ cm$^2$/s", r"$36$ cm$^2$/s", r"$72$ cm$^2$/s", r"$54$ cm$^2$/s"], "C",
        r"$s = 3$. $S = 6s^2$, so $\dfrac{dS}{dt} = 12s\dfrac{ds}{dt} = 12(3)(2) = 72$."),
    MCQ(r"A $6$-ft person walks away from a $24$-ft lamppost at $6$ ft/s. The tip of the shadow moves at", [r"$2$ ft/s", r"$6$ ft/s", r"$4$ ft/s", r"$8$ ft/s"], "D",
        r"$\frac{24}{x + s} = \frac{6}{s}$ gives $s = \frac x3$. The tip is at $x + s = \frac{4x}{3}$, moving at $\frac43(6) = 8$ ft/s.", why_not={"A": "that's the shadow's length"}),
]
xx = sp.symbols("xx")
same("m", [solve_rate(sp.pi / 48 * h**3, V, h, {d(V): sp.pi, h: 4}), sp.Rational(18, 1) / (2 * sp.sqrt(2)), 12 * 3 * 2, sp.Rational(4, 3) * 6],
     [1, 9 / sp.sqrt(2), 72, 8])

FRQS = [
    FRQ("A draining funnel", (
        r"A funnel has the shape of a cone with its vertex pointing down. The funnel has radius $6$ centimeters at the top and "
        r"height $12$ centimeters. Coffee drains out of the funnel at a constant rate of $3$ cubic centimeters per second. "
        r"Let $h$ be the depth of the coffee and $r$ be the radius of the coffee's surface, both measured in centimeters. "
        r"(The volume $V$ of a cone with radius $r$ and height $h$ is $V = \frac13\pi r^2 h$.)"), [
        Part("a", r"Show that the volume of the coffee in the funnel is $V = \dfrac{\pi}{12}h^3$.",
             selfcheck(r"V = \tfrac{\pi}{12}h^3"),
             r"By similar triangles, $\dfrac{r}{h} = \dfrac{6}{12}$, so $r = \dfrac{h}{2}$. Then "
             r"$V = \dfrac13\pi\left(\dfrac{h}{2}\right)^2 h = \dfrac{\pi}{12}h^3$.",
             [(1, "$r = \\frac{h}{2}$ from similar triangles"), (1, "substitutes to get $V = \\frac{\\pi}{12}h^3$")], work="2.4cm"),
        Part("b", r"Find the rate at which the depth of the coffee is changing at the instant the coffee is $4$ centimeters deep. "
                  r"Indicate units of measure.",
             num(-3 / (4 * sp.pi), tol=0.001, display=r"-\tfrac{3}{4\pi}\ \text{centimeters per second}"),
             r"$\dfrac{dV}{dt} = \dfrac{\pi}{4}h^2\dfrac{dh}{dt}$. With $\dfrac{dV}{dt} = -3$ and $h = 4$: "
             r"$-3 = 4\pi\dfrac{dh}{dt}$, so $\dfrac{dh}{dt} = -\dfrac{3}{4\pi} \approx -0.239$ centimeters per second.",
             [(1, "$\\frac{dV}{dt} = \\frac{\\pi}{4}h^2\\frac{dh}{dt}$"), (1, "uses $\\frac{dV}{dt} = -3$"), (1, "answer with units")],
             work="3cm"),
        Part("c", r"At the instant the coffee is $4$ centimeters deep, find the rate at which the radius of the coffee's surface is "
                  r"changing.", num(-3 / (8 * sp.pi), tol=0.001, display=r"-\tfrac{3}{8\pi}"),
             r"$r = \dfrac{h}{2}$, so $\dfrac{dr}{dt} = \dfrac12\cdot\dfrac{dh}{dt} = -\dfrac{3}{8\pi}$ centimeters per second.",
             [(1, "answer $-\\frac{3}{8\\pi}$")], work="2cm"),
    ], frq_type="Related rates"),
]
h5 = sp.Function("h")(t)
V5 = sp.Rational(1, 3) * sp.pi * (h5 / 2)**2 * h5
same("frq a", sp.expand(V5), sp.pi / 12 * h5**3)
hp5 = sp.symbols("hp5")
dh5 = sp.solve(sp.Eq(sp.diff(V5, t).subs(sp.diff(h5, t), hp5).subs(h5, 4), -3), hp5)
same("frq b", dh5, [-3 / (4 * sp.pi)])
same("frq c", dh5[0] / 2, -3 / (8 * sp.pi))

TOPIC = Topic(
    number="4.5", title="Solving Related Rates Problems",
    unit="Unit 4: Contextual Applications of Differentiation", ced=["CHA-3.E", "CHA-3.E.1"],
    goals=r"Solve related rates problems: draw and label, relate the quantities, differentiate with respect to time, then substitute.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
