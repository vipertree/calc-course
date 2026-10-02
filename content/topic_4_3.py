"""Topic 4.3: Rates of change in applied contexts other than motion.

CED: CHA-3.C (CHA-3.C.1): derivatives give rates in science, economics and everyday contexts. Covers rate-in minus rate-out
(at an instant only: no accumulation before Unit 6), marginal cost and profit, and the second derivative read as "the rate
itself is increasing/decreasing". Worked examples: fish population, a tank with inflow and drain, marginal profit.
"""
import sympy as sp

from calclib import (FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Text, Topic, Variants, Video, expr, num,
                     same, selfcheck)

x, t = sp.symbols("x t")
D = lambda e, v=t, n=1: sp.diff(e, v, n)

NOTES = [
    Video("s4_3.py::Lesson", "Rates everywhere", 4),

    Section("The same derivative, new contexts"),
    Text(r"Every derivative is a rate of change, whatever the quantity: bacteria per hour, dollars per item, degrees per minute. "
         r"The work is the same as for motion; the \blank{units} and the sentence change."),
    Formula("Reading the first two derivatives", (
        r"$Q'(t) > 0$: the quantity is \blank{increasing}. \qquad $Q'(t) < 0$: it is decreasing. \par "
        r"$Q''(t) > 0$: the \emph{rate} $Q'$ is increasing. \qquad $Q''(t) < 0$: the rate is \blank{decreasing}. \par "
        r"Units of $Q''$: units of $Q$ per unit of $t$, per unit of $t$.")),

    Section("Rate in, rate out"),
    Text(r"When something flows in at rate $R(t)$ and out at rate $D(t)$, the amount $A(t)$ changes at the net rate "
         r"\[ A'(t) = R(t) - D(t). \] At a given moment the amount is increasing if $R(t) > D(t)$ and decreasing if $R(t) \mblank{<} D(t)$."),

    Section("Marginal analysis"),
    Text(r"In economics, the derivative of a cost, revenue or profit function is called \emph{marginal}: $C'(x)$ is the marginal cost. "
         r"$C'(x)$ estimates the cost of producing \blank{one more} item after $x$ items. Profit is $P(x) = R(x) - C(x)$, so $P'(x) = R'(x) - C'(x)$."),
    BigIdea(r"A derivative is a rate in any context. Read its sign, give its units, and say what is changing; read the second "
            r"derivative as the rate of change of that rate."),
    Check(r"A town's population satisfies $P'(10) = 300$ people per year and $P''(10) = -20$. Is the population growing at $t = 10$? Is the growth speeding up?",
          selfcheck(r"\text{growing; growth slowing}"),
          r"Growing, since $P'(10) > 0$. But $P''(10) < 0$, so the growth rate is decreasing: the town is growing more slowly."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"A colony has $B(t) = 500 + 30t + t^2$ bacteria after $t$ hours. Find $B'(5)$ and give its units.", num(40, display=r"40\text{ bacteria per hour}"),
         r"$B'(t) = 30 + 2t$, so $B'(5) = 40$ bacteria per hour.", work="1.4cm"),
    Item(r"For the colony, find $B''(5)$ and explain its meaning.", num(2), r"$B'' = 2$: the growth rate is increasing by 2 bacteria per hour, every hour.", work="1.4cm"),
    Item(r"Water flows into a pool at $R(t) = 50 - 2t$ gallons per minute and leaks out at $L(t) = 4 + t$ gallons per minute. At $t = 10$, is the amount of water increasing or decreasing? At what rate?",
         num(16, display=r"\text{increasing at } 16\text{ gal/min}"), r"$R(10) - L(10) = 30 - 14 = 16 > 0$: increasing at 16 gallons per minute.", work="1.8cm"),
    Item(r"For the same pool, at what time is the amount of water neither increasing nor decreasing?", num(sp.Rational(46, 3)),
         r"$50 - 2t = 4 + t$ gives $t = \frac{46}{3} \approx 15.3$ minutes.", work="1.4cm"),
    Item(r"A cost function is $C(x) = 2000 + 15x - 0.01x^2$ dollars for $x$ chairs. Find the marginal cost at $x = 300$.", num(9, display=r"\$9\text{ per chair}"),
         r"$C'(x) = 15 - 0.02x$, so $C'(300) = 9$ dollars per chair.", work="1.4cm"),
    Item(r"Explain what $C'(300) = 9$ means for the chair maker.", selfcheck(r"\text{301st chair costs about \$9}"),
         r"After 300 chairs, making one more costs about \$9.", work="1.2cm"),
    Item(r"Revenue from $x$ tickets is $R(x) = 25x - 0.05x^2$ dollars. Find $R'(100)$.", num(15), r"$R'(x) = 25 - 0.1x$, so $R'(100) = 15$ dollars per ticket.", work="1.4cm"),
    Item(r"For the tickets, at what $x$ does revenue stop increasing?", num(250), r"$R'(x) = 25 - 0.1x = 0$ at $x = 250$.", work="1.2cm"),
    Item(r"A rumor spreads so that $N(t) = 80t - 2t^2$ students have heard it after $t$ hours ($0 \le t \le 20$). Find $N'(5)$ and interpret.",
         num(60), r"$N'(5) = 80 - 20 = 60$: at 5 hours, the number who have heard is increasing at 60 students per hour.", work="1.6cm"),
    Item(r"For the rumor, find $N''(5)$. Is the rumor spreading faster or slower as time goes on?", num(-4),
         r"$N'' = -4$: the spreading rate is decreasing by 4 students per hour each hour. It spreads more slowly.", work="1.4cm"),
    Item(r"Mei's coffee shop has profit $P(x) = -0.5x^2 + 40x - 300$ dollars from selling $x$ drinks. Find $P'(30)$.", num(10),
         r"$P'(x) = -x + 40$, so $P'(30) = 10$ dollars per drink.", work="1.4cm"),
    Item(r"For the coffee shop, should Mei sell more than 40 drinks if she wants more profit? Explain using $P'$.", selfcheck(r"\text{no: } P' < 0 \text{ after 40}"),
         r"No: for $x > 40$, $P'(x) < 0$, so each extra drink lowers profit.", work="1.4cm"),
    Item(r"The volume of a balloon is $V(r) = \frac43\pi r^3$ cubic cm. Find $V'(3)$ and give its units.", num(36 * sp.pi, display=r"36\pi\text{ cm}^3\text{ per cm}"),
         r"$V'(r) = 4\pi r^2$, so $V'(3) = 36\pi$ cubic centimeters per centimeter of radius.", work="1.4cm"),
    Item(r"Ice cream sales are $S(T) = 2T^2 - 40T + 300$ cones per day at temperature $T$ in $^\circ$F. Find $S'(75)$ and interpret.", num(260),
         r"$S'(T) = 4T - 40$, $S'(75) = 260$: at $75^\circ$F, daily sales increase by about 260 cones per degree.", work="1.6cm"),
    Item(r"A drug's concentration is $C(t) = 6t - t^2$ mg/L after $t$ hours ($0 \le t \le 6$). When is the concentration increasing?",
         selfcheck(r"0 \le t < 3"), r"$C'(t) = 6 - 2t > 0$ for $t < 3$.", work="1.4cm"),
    Item(r"For the drug, find the rate of change of the concentration at $t = 4$, with units.", num(-2),
         r"$C'(4) = -2$ mg/L per hour: decreasing at 2 mg/L per hour.", work="1.4cm"),
    Item(r"Snow falls at $F(t) = 2t$ cm per hour and melts at $M(t) = 6$ cm per hour. At $t = 2$, is the depth increasing or decreasing?",
         selfcheck(r"\text{decreasing at 2 cm/hr}"), r"$F(2) - M(2) = 4 - 6 = -2 < 0$: decreasing at 2 cm per hour.", work="1.4cm"),
    Item(r"A city's population (in thousands) is $P(t) = 50 + 6\sqrt{t}$, $t$ years after 2000. Find $P'(9)$.", num(1, display=r"1\text{ thousand per year}"),
         r"$P'(t) = \frac{3}{\sqrt t}$, so $P'(9) = 1$ thousand people per year.", work="1.4cm"),
    Item(r"For the city, is $P''(t)$ positive or negative? What does that say about the growth?", selfcheck(r"\text{negative: growth slowing}"),
         r"$P''(t) = -\frac{3}{2}t^{-3/2} < 0$: the city keeps growing, but more and more slowly.", work="1.4cm"),
    Item(r"A tank's temperature is $H(t) = 20 + 60e^{-0.1t}$ $^\circ$C after $t$ minutes. Find $H'(0)$ and interpret.", num(-6),
         r"$H'(t) = -6e^{-0.1t}$, so $H'(0) = -6$: at the start, the temperature is decreasing at $6^\circ$C per minute.", work="1.6cm"),
]
same("p", [D(500 + 30 * t + t**2).subs(t, 5), (50 - 2 * t - (4 + t)).subs(t, 10), sp.solve(50 - 2 * t - 4 - t, t)[0],
           D(2000 + 15 * x - x**2 / 100, x).subs(x, 300), D(25 * x - x**2 / 20, x).subs(x, 100), sp.solve(D(25 * x - x**2 / 20, x), x)[0],
           D(80 * t - 2 * t**2).subs(t, 5), D(-x**2 / 2 + 40 * x - 300, x).subs(x, 30), D(sp.Rational(4, 3) * sp.pi * x**3, x).subs(x, 3),
           D(2 * x**2 - 40 * x + 300, x).subs(x, 75), D(6 * t - t**2).subs(t, 4), D(50 + 6 * sp.sqrt(t)).subs(t, 9), D(20 + 60 * sp.exp(-t / 10)).subs(t, 0)],
     [40, 16, sp.Rational(46, 3), 9, 15, 250, 60, 10, 36 * sp.pi, 260, -2, 1, -6])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"$P(t) = 800 + 25t - t^2$ birds live on an island after $t$ years. Find $P'(5)$.", num(15), r"$P'(t) = 25 - 2t$, so $P'(5) = 15$ birds per year.", work="1.4cm"),
        Item(r"$P(t) = 300 + 12t + t^2$ cells after $t$ hours. Find $P'(4)$.", num(20), r"$P'(t) = 12 + 2t$, so $P'(4) = 20$ cells per hour.", work="1.4cm"),
        Item(r"$P(t) = 1000 - 40t + t^2$ fish in a pond after $t$ weeks. Find $P'(10)$.", num(-20), r"$P'(t) = -40 + 2t$, so $P'(10) = -20$ fish per week.", work="1.4cm"),
    ),
    Variants(
        Item(r"Water enters a tank at $R(t) = 30 - t$ L/min and leaves at $D(t) = 2t$ L/min. At $t = 6$, find the rate of change of the amount of water.",
             num(6), r"$R(6) - D(6) = 24 - 12 = 6$ L/min.", work="1.4cm"),
        Item(r"Air enters a balloon at $R(t) = 10 + t$ L/s and leaks at $D(t) = 3t$ L/s. At $t = 8$, find the rate of change of the volume.",
             num(-6), r"$R(8) - D(8) = 18 - 24 = -6$ L/s.", work="1.4cm"),
        Item(r"Sand is added to a pile at $R(t) = 12$ kg/hr and blows off at $D(t) = t^2$ kg/hr. At $t = 2$, find the rate of change of the pile's mass.",
             num(8), r"$R(2) - D(2) = 12 - 4 = 8$ kg/hr.", work="1.4cm"),
    ),
    Variants(
        Item(r"$C(x) = 500 + 8x + 0.02x^2$ is the cost of $x$ shirts. Find the marginal cost at $x = 100$.", num(12), r"$C'(x) = 8 + 0.04x$, so $C'(100) = 12$.", work="1.4cm"),
        Item(r"$C(x) = 900 + 20x - 0.01x^2$ is the cost of $x$ lamps. Find the marginal cost at $x = 200$.", num(16), r"$C'(x) = 20 - 0.02x$, so $C'(200) = 16$.", work="1.4cm"),
        Item(r"$C(x) = 1200 + 5x + 0.005x^2$ is the cost of $x$ books. Find the marginal cost at $x = 400$.", num(9), r"$C'(x) = 5 + 0.01x$, so $C'(400) = 9$.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"$P'(6) = 40$ and $P''(6) = -3$, where $P$ is a population in animals and $t$ is in years. At $t = 6$,", [
            r"the population is decreasing", r"the population is increasing, and its growth rate is decreasing", r"the population is increasing faster and faster",
            r"the population is $40$"], "B", r"$P' > 0$: increasing. $P'' < 0$: the rate is decreasing.", why_not={"A": "$P' > 0$ means increasing"}),
        MCQ(r"$V'(2) = -5$ and $V''(2) = 1$, where $V$ is a volume in liters and $t$ is in minutes. At $t = 2$,", [
            r"the volume is increasing", r"the volume is decreasing more and more quickly", r"the volume is decreasing, and the rate of change is increasing",
            r"the volume is $-5$ liters"], "C", r"$V' < 0$: decreasing. $V'' > 0$: the rate (a negative number) is increasing toward $0$."),
        MCQ(r"$T'(10) = 2$ and $T''(10) = 0.5$, where $T$ is a temperature in $^\circ$C and $t$ is in hours. At $t = 10$,", [
            r"the temperature is rising, and rising faster and faster", r"the temperature is falling", r"the temperature is $2^\circ$C",
            r"the temperature is rising more slowly"], "A", r"$T' > 0$ and $T'' > 0$."),
    ),
    Variants(
        Item(r"Profit is $P(x) = -x^2 + 60x - 400$ dollars. For what $x$ is $P'(x) = 0$?", num(30), r"$P'(x) = -2x + 60 = 0$ at $x = 30$.", work="1.2cm"),
        Item(r"Profit is $P(x) = -2x^2 + 80x - 500$ dollars. For what $x$ is $P'(x) = 0$?", num(20), r"$P'(x) = -4x + 80 = 0$ at $x = 20$.", work="1.2cm"),
        Item(r"Profit is $P(x) = -0.5x^2 + 35x - 200$ dollars. For what $x$ is $P'(x) = 0$?", num(35), r"$P'(x) = -x + 35 = 0$ at $x = 35$.", work="1.2cm"),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"Oil leaks from a tanker so that the radius of the slick is $r(t) = 2\sqrt{t}$ meters after $t$ minutes. The rate of change of the radius at $t = 4$ is",
        [r"$\frac12$ m/min", r"$1$ m/min", r"$2$ m/min", r"$4$ m/min"], "A", r"$r'(t) = \frac{1}{\sqrt t}$, so $r'(4) = \frac12$."),
    MCQ(r"Water flows into a tank at $R(t) = 5 + 4\sin t$ gal/hr and out at $D(t) = 6$ gal/hr. At $t = \pi$, the amount of water is", [
        r"increasing at 3 gal/hr", r"decreasing at 1 gal/hr", r"decreasing at 6 gal/hr", r"not changing"], "B", r"$R(\pi) - D(\pi) = 5 + 0 - 6 = -1$."),
    MCQ(r"$C(x) = 3x^2 - 12x + 50$ is the cost of producing $x$ hundred units. The marginal cost when $x = 5$ is", [r"$18$", r"$65$", r"$3$", r"$30$"], "A",
        r"$C'(x) = 6x - 12$, so $C'(5) = 18$ (dollars per hundred units).", why_not={"B": "that's $C(5)$"}),
    MCQ(r"The number of people at a fair is $F(t)$, $t$ hours after it opens. Which statement means attendance is rising but more slowly?", [
        r"$F'(t) > 0$ and $F''(t) > 0$", r"$F'(t) < 0$ and $F''(t) < 0$", r"$F'(t) < 0$ and $F''(t) > 0$", r"$F'(t) > 0$ and $F''(t) < 0$"], "D",
        r"Rising: $F' > 0$. More slowly: the rate is decreasing, $F'' < 0$."),
]
same("m", [D(2 * sp.sqrt(t)).subs(t, 4), (5 + 4 * sp.sin(t) - 6).subs(t, sp.pi), D(3 * x**2 - 12 * x + 50, x).subs(x, 5)], [sp.Rational(1, 2), -1, 18])

FRQS = [
    FRQ("A water tank", (
        r"Water flows into a tank at the rate $R(t) = 40 + 6t - t^2$ gallons per hour and is pumped out at the rate $D(t) = 30$ gallons per hour, "
        r"for $0 \le t \le 8$ hours."), [
        Part("a", r"Is the amount of water in the tank increasing or decreasing at $t = 2$? Give a reason.", selfcheck(r"\text{increasing}"),
             r"$R(2) - D(2) = 40 + 12 - 4 - 30 = 18 > 0$, so the amount is increasing (at 18 gallons per hour).", [(1, "net rate at $t = 2$"), (1, "conclusion")], work="1.8cm"),
        Part("b", r"At what time $t$, for $0 \le t \le 8$, is the amount of water neither increasing nor decreasing?", num(3 + sp.sqrt(19)),
             r"$40 + 6t - t^2 = 30$ gives $t^2 - 6t - 10 = 0$, so $t = 3 + \sqrt{19} \approx 7.36$ hours.", [(1, "sets $R = D$"), (1, "$t \\approx 7.36$")], work="2cm"),
        Part("c", r"Find $R'(5)$ and explain its meaning in context.", num(-4),
             r"$R'(t) = 6 - 2t$, so $R'(5) = -4$: at $t = 5$ hours, the rate at which water flows in is decreasing at 4 gallons per hour per hour.",
             [(1, "$-4$"), (1, "meaning with units")], work="2cm"),
    ], frq_type="Rates in and out"),
]
same("frq", [(40 + 6 * t - t**2 - 30).subs(t, 2), max(sp.solve(40 + 6 * t - t**2 - 30, t)), D(40 + 6 * t - t**2).subs(t, 5)], [18, 3 + sp.sqrt(19), -4])

TOPIC = Topic(
    number="4.3", title="Rates of Change in Applied Contexts Other Than Motion",
    unit="Unit 4: Contextual Applications of Differentiation", ced=["CHA-3.C", "CHA-3.C.1"],
    goals=r"Use derivatives to solve and interpret rate problems in science, economics and other contexts, including rate in minus rate out.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
