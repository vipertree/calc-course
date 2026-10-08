"""Topic 4.1: Interpreting the meaning of the derivative in context.

CED: CHA-3.A (CHA-3.A.1, CHA-3.A.2): the derivative of a function is its instantaneous rate of change, with units of
(output units) per (input unit). The interpretation sentence template here is the one the AP rubrics reward: it names
the input value with units, the quantity, increasing/decreasing, and the rate with units.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Table, Text, Topic, Variants, Video, expr, num,
                     check, same, selfcheck)

x, t = sp.symbols("x t")

NOTES = [
    Video("s4_1.py::Lesson", "The derivative in context", 4),

    Section("A rate with units"),
    Text(r"If $f(x)$ measures some quantity and $x$ is the input, then $f'(a)$ is the \blank{instantaneous rate of change} of that quantity "
         r"at $x = a$. Its units are the units of $f$ \blank{per} unit of $x$."),
    Formula("Units of the derivative", (
        r"\[ \text{units of } f'(x) = \frac{\text{units of } f}{\text{units of } x} \] "
        r"Volume in gallons, time in minutes: $V'(t)$ is in gallons per minute. Cost in dollars, $x$ items: $C'(x)$ is in dollars per item.")),

    Section("Saying what $f'(a)$ means"),
    Formula("The interpretation sentence", (
        r"At [input $= a$, with units], [the quantity] is [increasing or decreasing] at a rate of [$|f'(a)|$, with units]. \par "
        r"The sign of $f'(a)$ chooses the word: positive means \blank{increasing}, negative means \blank{decreasing}.")),
    VideoExample('Draining a tank', work="2.2cm"),
    Text(r"Three things the sentence never says: that $3$ liters drain \emph{over} the next minute (that's an estimate, not a fact), "
         r"that the tank holds $-3$ liters (that would be $W(5)$), or ``the derivative is $-3$'' with no context."),

    Section("Value, average rate, instantaneous rate"),
    Table(r"$f(a)$ & the amount at $x = a$ & liters \\ "
          r"$\dfrac{f(b) - f(a)}{b - a}$ & the average rate of change on $[a, b]$ & liters per minute \\ "
          r"$f'(a)$ & the rate of change at the instant $x = a$ & liters per minute", "lll",
          header=r"expression & meaning & units (tank example)"),
    Text(r"An average rate is not an instantaneous rate. But when all you have is a table of values, the average rate over the "
         r"\blank{smallest} interval around $a$ is your best \blank{estimate} of $f'(a)$, the instantaneous rate."),
    BigIdea(r"A derivative in context is a rate: name the moment, name the quantity, say increasing or decreasing, and give the "
            r"rate with its units."),
    Check(r"$P(t)$ is the population of a town, in people, $t$ years after 2020. What are the units of $P'(t)$?",
          selfcheck(r"\text{people per year}"), r"People per year: units of $P$ over units of $t$."),
]
same("coffee", sp.Rational(141 - 162, 6), sp.Rational(-7, 2))

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"$A(r)$ is the area of a circle, in square centimeters, with radius $r$ centimeters. Give the units of $A'(r)$.",
         selfcheck(r"\text{cm}^2\text{ per cm}"), r"Square centimeters per centimeter.", work="1.2cm"),
    Item(r"$D(t)$ is the distance, in miles, that Malia has hiked $t$ hours after starting. Interpret $D'(2) = 2.5$.",
         selfcheck(r"\text{2.5 miles per hour at } t = 2"),
         r"At $t = 2$ hours, the distance Malia has hiked is increasing at a rate of $2.5$ miles per hour.", work="1.8cm"),
    Item(r"$T(h)$ is the air temperature, in $^\circ$C, at an altitude of $h$ kilometers. Interpret $T'(3) = -6.5$.",
         selfcheck(r"\text{decreasing } 6.5^\circ\text{C per km}"),
         r"At an altitude of $3$ km, the temperature is decreasing at a rate of $6.5^\circ$C per kilometer of altitude.", work="1.8cm"),
    Item(r"$C(n)$ is the cost, in dollars, of producing $n$ skateboards. $C'(150) = 42$. Estimate the cost of producing the 151st skateboard.",
         num(42, display=r"\$42"), r"The rate is $42$ dollars per skateboard at $n = 150$, so one more costs about \$42.", work="1.6cm"),
    Item(r"$V(t)$ is the volume of air, in liters, in Jun's lungs $t$ seconds into a breath. If $V'(1.5) = 0.4$, is Jun breathing in or out at $t = 1.5$? Explain.",
         selfcheck(r"\text{in: volume increasing}"), r"In: $V'(1.5) > 0$, so the volume of air is increasing.", work="1.6cm"),
    Item(r"$R(p)$ is the number of rides sold per day when the ticket price is $p$ dollars. What are the units of $R'(p)$, and would you expect $R'(p)$ to be positive or negative?",
         selfcheck(r"\text{rides per day per dollar; negative}"),
         r"Rides per day, per dollar of price. Usually negative: raising the price sells fewer rides.", work="1.8cm"),
    Item(r"A balloon's radius $r(t)$, in inches, satisfies $r'(10) = 0.2$, where $t$ is in seconds. Interpret.",
         selfcheck(r"\text{0.2 inches per second at } t = 10"),
         r"At $t = 10$ seconds, the radius of the balloon is increasing at a rate of $0.2$ inches per second.", work="1.6cm"),
    Item(r"$S(t)$ is the number of songs in Amara's playlist $t$ days after she made it. Explain the difference between $S(30) = 120$ and $S'(30) = 2$.",
         selfcheck(r"\text{amount vs rate}"),
         r"$S(30) = 120$: after 30 days the playlist has 120 songs. $S'(30) = 2$: at day 30, the number of songs is increasing at 2 songs per day.", work="2cm"),
    Item(r"The table gives the depth $d(t)$, in centimeters, of snow $t$ hours after midnight. Estimate $d'(5)$.",
         num(sp.Rational(3, 2), display=r"1.5\text{ cm per hour}"),
         r"\[ d'(5) \approx \frac{d(6) - d(4)}{6 - 4} = \frac{21 - 18}{2} = 1.5 \text{ cm per hour}. \]", work="2cm",
         ),
    Item(r"Using the snow table, interpret your estimate of $d'(5)$ in context.", selfcheck(r"\text{increasing about 1.5 cm/hr at 5 am}"),
         r"At 5 a.m., the depth of the snow is increasing at about $1.5$ centimeters per hour.", work="1.6cm"),
    Item(r"$G(m)$ is the number of gallons of gas left in Tomás's tank after driving $m$ miles. What does $G'(m) = -\frac{1}{32}$ mean?",
         selfcheck(r"\text{uses 1/32 gallon per mile}"),
         r"After $m$ miles, the gas in the tank is decreasing at $\frac1{32}$ gallon per mile: the car gets 32 miles per gallon.", work="1.8cm"),
    Item(r"$h(t) = -16t^2 + 80t$ is a ball's height in feet after $t$ seconds. Find $h'(1)$ and interpret it.", num(48, display=r"48\text{ ft/s}"),
         r"$h'(t) = -32t + 80$, so $h'(1) = 48$. At $t = 1$ second, the ball's height is increasing at $48$ feet per second.", work="2cm"),
    Item(r"For the same ball, find $h'(4)$ and interpret it.", num(-48, display=r"-48\text{ ft/s}"),
         r"$h'(4) = -48$. At $t = 4$ seconds, the height is decreasing at $48$ feet per second.", work="1.6cm"),
    Item(r"$P(t) = 500 + 40t - t^2$ is the number of members of a gym $t$ weeks after it opened. Find $P'(10)$ with units.", num(20, display=r"20\text{ members per week}"),
         r"$P'(t) = 40 - 2t$, so $P'(10) = 20$ members per week.", work="1.6cm"),
    Item(r"For the gym, when is the membership neither increasing nor decreasing?", num(20, display=r"t = 20\text{ weeks}"),
         r"$P'(t) = 40 - 2t = 0$ at $t = 20$ weeks.", work="1.4cm"),
    Item(r"Sam runs a bakery. $B(x)$ is the profit, in dollars, from selling $x$ loaves. They find $B'(60) = -0.5$. Should Sam bake a 61st loaf? Explain.",
         selfcheck(r"\text{no: profit decreasing}"),
         r"Probably not: at $60$ loaves, profit is decreasing at about \$0.50 per additional loaf.", work="1.8cm"),
    Item(r"$f(x)$ is the number of calories in $x$ grams of a granola. $f'(x) = 4.2$ for all $x$. Explain what $4.2$ means.",
         selfcheck(r"\text{4.2 calories per gram}"), r"Each additional gram adds $4.2$ calories: the granola has 4.2 calories per gram.", work="1.6cm"),
    Item(r"$L(t)$ is the length, in centimeters, of a plant $t$ days after planting. Which is larger in a typical week, $L(7)$ or $L'(7)$? What does each measure?",
         selfcheck(r"L(7)\text{ (a length) vs } L'(7)\text{ (cm per day)}"),
         r"$L(7)$ is the plant's length after a week; $L'(7)$ is how fast it is growing then, in cm per day. Usually $L(7)$ is larger, but they "
         r"measure different things.", work="2cm"),
    Item(r"The rate of change of the amount of medicine $M(t)$, in mg, in a patient's blood is $M'(t) = -0.3M(t)$. At a moment when $M = 50$ mg, interpret $M'$.",
         num(-15, display=r"-15\text{ mg per hour}"), r"$M' = -15$: the amount of medicine is decreasing at $15$ mg per hour (with $t$ in hours).", work="1.8cm"),
    Item(r"$W(t)$ gives a puppy's weight in pounds at age $t$ months, with $W(4) = 12$ and $W'(4) = 3$. Use these to estimate $W(4.5)$.",
         num(sp.Rational(27, 2)), r"$W(4.5) \approx W(4) + W'(4)\cdot 0.5 = 12 + 1.5 = 13.5$ pounds.", work="1.8cm"),
]
SNOW = r"\[ \begin{array}{c|cccc} t \text{ (hours)} & 2 & 4 & 6 & 8 \\ \hline d(t) \text{ (cm)} & 11 & 18 & 21 & 22 \end{array} \]"
PRACTICE[8].stem += SNOW
same("practice", [sp.diff(-16 * t**2 + 80 * t, t).subs(t, 1), sp.diff(-16 * t**2 + 80 * t, t).subs(t, 4), sp.diff(500 + 40 * t - t**2, t).subs(t, 10),
                  sp.solve(40 - 2 * t, t)[0], sp.Rational(21 - 18, 2), 12 + 3 * sp.Rational(1, 2)],
     [48, -48, 20, 20, sp.Rational(3, 2), sp.Rational(27, 2)])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"$V(t)$ is the volume of water, in gallons, in a pool $t$ hours after filling begins. Give the units of $V'(t)$.",
             selfcheck(r"\text{gallons per hour}"), r"Gallons per hour.", work="1cm"),
        Item(r"$M(p)$ is the mass, in grams, of a crystal after $p$ days in solution. Give the units of $M'(p)$.",
             selfcheck(r"\text{grams per day}"), r"Grams per day.", work="1cm"),
        Item(r"$Q(s)$ is the fuel used, in liters, by a ship traveling at $s$ knots for one hour. Give the units of $Q'(s)$.",
             selfcheck(r"\text{liters per knot}"), r"Liters per knot.", work="1cm"),
    ),
    Variants(
        Item(r"$N(t)$ is the number of people in a stadium $t$ minutes after the gates open. Interpret $N'(20) = 350$.",
             selfcheck(r"\text{increasing 350 people/min at } t = 20"),
             r"At $t = 20$ minutes, the number of people in the stadium is increasing at $350$ people per minute.", work="1.6cm"),
        Item(r"$H(t)$ is the height of the tide, in feet, $t$ hours after midnight. Interpret $H'(9) = -0.8$.",
             selfcheck(r"\text{decreasing 0.8 ft/hr at 9 am}"),
             r"At 9 a.m., the height of the tide is decreasing at $0.8$ feet per hour.", work="1.6cm"),
        Item(r"$B(t)$ is the balance, in dollars, of Kai's savings account $t$ years after opening. Interpret $B'(4) = 120$.",
             selfcheck(r"\text{increasing \$120 per year at } t = 4"),
             r"At $t = 4$ years, the balance is increasing at \$120 per year.", work="1.6cm"),
    ),
    Variants(
        Item(r"$s(t) = 3t^2 - 12t$ is an object's position in meters at $t$ seconds. Find $s'(1)$, with units.", num(-6),
             r"$s'(t) = 6t - 12$, so $s'(1) = -6$ meters per second.", work="1.4cm"),
        Item(r"$s(t) = t^3 - 2t$ is an object's position in meters at $t$ seconds. Find $s'(2)$, with units.", num(10),
             r"$s'(t) = 3t^2 - 2$, so $s'(2) = 10$ meters per second.", work="1.4cm"),
        Item(r"$s(t) = 20t - 5t^2$ is an object's position in meters at $t$ seconds. Find $s'(3)$, with units.", num(-10),
             r"$s'(t) = 20 - 10t$, so $s'(3) = -10$ meters per second.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"$F(t)$ is the number of fish in a lake $t$ months after stocking. Which statement interprets $F'(6) = -40$?",
            [r"After 6 months there are $40$ fewer fish", r"At 6 months, the number of fish is decreasing at 40 fish per month",
             r"The lake loses 40 fish over 6 months", r"There are $-40$ fish after 6 months"], "B", r"$F'$ is a rate: fish per month, at the instant $t = 6$.",
            why_not={"A": "that's a change in amount, not a rate", "D": "that would be $F(6)$"}),
        MCQ(r"$E(v)$ is the energy, in joules, a cyclist uses per kilometer at speed $v$ km/h. $E'(25) = 30$ means", [
            r"at 25 km/h, energy per kilometer is increasing at 30 joules per km/h of speed", r"the cyclist uses 30 joules at 25 km/h",
            r"the cyclist speeds up 30 km/h", r"energy per kilometer is 25 joules"], "A", r"Units: joules per kilometer, per km/h of speed."),
        MCQ(r"$D(p)$ is the number of phones sold when the price is $p$ dollars. Which is most likely?", [r"$D'(400) = 300$", r"$D'(400) = -300$",
            r"$D(400) = -300$", r"$D'(400) = 0$ for every price"], "B", r"Raising the price usually lowers sales, so $D'$ is negative.",
            why_not={"C": "sales can't be negative"}),
    ),
    Variants(
        Item(r"$T(t)$ is a pizza's temperature in $^\circ$F after $t$ minutes, with $T(10) = 300$ and $T(14) = 260$. Estimate $T'(12)$.", num(-10),
             r"\[ T'(12) \approx \frac{260 - 300}{14 - 10} = -10^\circ\text{F per minute}. \]", work="1.6cm"),
        Item(r"$A(t)$ is the area of an oil spill in square miles after $t$ hours, with $A(2) = 5$ and $A(6) = 17$. Estimate $A'(4)$.", num(3),
             r"\[ A'(4) \approx \frac{17 - 5}{6 - 2} = 3 \text{ square miles per hour}. \]", work="1.6cm"),
        Item(r"$R(t)$ is the rainfall total, in mm, after $t$ hours, with $R(1) = 4$ and $R(5) = 14$. Estimate $R'(3)$.", num(sp.Rational(5, 2)),
             r"\[ R'(3) \approx \frac{14 - 4}{5 - 1} = 2.5 \text{ mm per hour}. \]", work="1.6cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$V(t)$ is the volume of a balloon in cubic inches, $t$ seconds after inflation begins. The units of $V'(t)$ are", [r"cubic inches",
        r"seconds per cubic inch", r"cubic inches per second", r"inches per second"], "C", r"Units of $V$ per unit of $t$."),
    MCQ(r"$P(x)$ is the profit, in dollars, from selling $x$ tickets. If $P'(150) = 12$, which is the best estimate?", [
        r"$P(150) = 12$", r"Selling the 151st ticket adds about \$12 of profit", r"Profit is \$12 per ticket for every ticket", r"150 tickets earn \$12"], "B",
        r"$P'(150) \approx P(151) - P(150)$."),
    MCQ(r"The temperature of a room is $R(t) = 68 + 4\sin\left(\frac{\pi t}{12}\right)$, in $^\circ$F, $t$ hours after midnight. At $t = 18$, the temperature is", [
        r"increasing", r"decreasing", r"at its maximum", r"neither increasing nor decreasing"], "D",
        r"$R'(t) = \frac{\pi}{3}\cos\left(\frac{\pi t}{12}\right)$, and $R'(18) = \frac\pi3\cos\frac{3\pi}{2} = 0$.",
        why_not={"C": "$t = 18$ is the minimum, $64^\\circ$F"}),
    MCQ(r"$W(t)$, in liters, is the water in a reservoir after $t$ days, and $W'(t) = 200 - 30t$. On day 5 the water level is", [
        r"rising at 50 liters per day", r"falling at 50 liters per day", r"rising at 200 liters per day", r"falling at 150 liters per day"], "A",
        r"$W'(5) = 200 - 150 = 50 > 0$."),
]
same("tp", [sp.diff(68 + 4 * sp.sin(sp.pi * t / 12), t).subs(t, 18), 200 - 30 * 5], [0, 50])

FRQS = [
    FRQ("A cooling oven", (
        r"An oven is turned off at time $t = 0$. The temperature of the oven is modeled by a differentiable function $F$, where "
        r"$F(t)$ is measured in degrees Fahrenheit and $t$ is measured in minutes. Selected values of $F(t)$ are given in the table."
        r"\par\smallskip\centerline{\begin{tabular}{c|ccccc} $t$ (minutes) & 0 & 5 & 12 & 20 & 30 \\ \hline "
        r"$F(t)$ ($^\circ$F) & 425 & 380 & 330 & 285 & 245\end{tabular}}"), [
        Part("a", r"Use the data in the table to estimate $F'(16)$. Show the work that leads to your answer. Indicate units of measure.",
             num(sp.Rational(-45, 8), tol=0.005, display=r"-\tfrac{45}{8} = -5.625\ \text{degrees Fahrenheit per minute}"),
             r"$F'(16) \approx \dfrac{F(20) - F(12)}{20 - 12} = \dfrac{285 - 330}{8} = -5.625$ degrees Fahrenheit per minute.",
             [(1, "difference quotient with $F(20)$ and $F(12)$, and the answer"), (1, "units")], work="2.6cm"),
        Part("b", r"Using correct units, interpret the meaning of $F'(16)$ in the context of the problem.",
             selfcheck(r"\text{At } t = 16\text{, the temperature is decreasing about 5.6 degrees F per minute}"),
             r"At time $t = 16$ minutes, the temperature of the oven is decreasing at a rate of about $5.625$ degrees Fahrenheit per minute.",
             [(1, "rate of change of temperature, at $t = 16$, with units")], work="2cm"),
        Part("c", r"The temperature of the oven can also be modeled by $G(t) = 425 - 9.5t + 0.12t^2$ for $0 \le t \le 30$. Using this "
                  r"model, find $G'(16)$.", num(sp.Rational(-283, 50), tol=0.005, display=r"-5.66"),
             r"$G'(t) = -9.5 + 0.24t$, so $G'(16) = -9.5 + 3.84 = -5.66$ degrees Fahrenheit per minute.",
             [(1, "answer $-5.66$")], work="1.8cm"),
        Part("d", r"For $0 < t < 30$, is the temperature of the oven, as modeled by $G$, changing at an increasing rate or at a "
                  r"decreasing rate? Give a reason for your answer.", selfcheck(r"\text{At an increasing rate}"),
             r"$G''(t) = 0.24 > 0$, so the rate of change $G'(t)$ is increasing: the temperature is changing at an increasing rate "
             r"(it is falling more and more slowly).",
             [(1, "increasing rate, because $G''(t) > 0$")], work="2cm"),
    ], frq_type="Table"),
]
G1 = 425 - sp.Rational(19, 2) * t + sp.Rational(12, 100) * t**2
same("frq", [sp.Rational(285 - 330, 8)], [sp.Rational(-45, 8)])
same("frq c", sp.diff(G1, t).subs(t, 16), sp.Rational(-283, 50))
check("frq d", sp.diff(G1, t, 2) > 0)
# the model should resemble the data
check("frq model", all(abs(G1.subs(t, a) - b) < 4 for a, b in [(0, 425), (5, 380), (12, 330), (20, 285), (30, 245)]))

TOPIC = Topic(
    number="4.1", title="Interpreting the Meaning of the Derivative in Context",
    unit="Unit 4: Contextual Applications of Differentiation", ced=["CHA-3.A", "CHA-3.A.1", "CHA-3.A.2"],
    goals=r"Interpret a derivative as a rate of change in context, with correct units and the words increasing or decreasing.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
