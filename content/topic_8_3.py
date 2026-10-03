"""Topic 8.3: Using accumulation functions and definite integrals in applied contexts.

CED: CHA-4.D (CHA-4.D.1, CHA-4.D.2): the definite integral of a rate of change gives the net change (accumulation)
over the interval; units of the integral are rate units times input units; amount = initial amount + integral of
(rate in - rate out); the amount is greatest where rate in - rate out changes from + to -, checked against the
endpoints. Lesson example: tank with E(t) = 8 + 2t, D(t) = t^2, A(0) = 50. Worked examples: interpret an integral and
a derivative in context; trapezoidal sum of a rate from a table; maximum temperature from H'(t) = 4 - t.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)

t = sp.symbols("t", real=True)


def I(f, a, b):
    return sp.integrate(f, (t, a, b))


def trap(ts, vs):
    return sum(sp.Rational(b - a, 2) * (u + v) for a, b, u, v in zip(ts, ts[1:], vs, vs[1:]))


net = 8 + 2 * t - t**2
same("lesson", [net.subs(t, 5), 50 + I(net, 0, 6), 50 + I(net, 0, 4)], [-7, 62, sp.Rational(230, 3)])
same("ex2", [1200 + trap([0, 2, 5, 8], [30, 40, 25, 10])], [1420])
same("ex3", [60 + I(4 - t, 0, 4), 60 + I(4 - t, 0, 6)], [68, 66])

NOTES = [
    Video("s8_3.py::Lesson", "Accumulation in context", 6),

    Section("Start plus net change"),
    Formula("Amount from rates", (
        r"If the amount $A$ changes at rate $A'(t) = E(t) - D(t)$ (rate in minus rate out), then \[ A(t) = \blank{A(0)} + \int_0^t \blank{\big(E(u) - D(u)\big)}\,du. \] "
        r"What you had, plus what came in, minus what went out.")),
    Section("Units and interpretation"),
    Text(r"An integral's units are the rate's units times the input's units: (liters per hour)(hours) $=$ liters. To interpret $\int_a^b R(t)\,dt$, say "
         r"\emph{what} accumulates, that it is a \emph{total}, and \emph{over which interval}, with units."),
    Text(r"\textbf{Example sentence.} $\int_2^5 E(t)\,dt$ is the total number of liters of water that flow into the tank from $t = 2$ to $t = 5$ hours."),
    Section("Greatest and least amounts"),
    Text(r"$A$ increases while $E(t) > D(t)$ and decreases while $E(t) < D(t)$. A sign chart for $E - D$ finds the critical points. For the absolute maximum on a closed interval, compare $A$ at the critical points and both endpoints."),
    VideoExample('Water in a tank', work="5cm"),
    Text(r"\textbf{Inputs and outputs.} ``How much'' is answered with an amount ($\frac{230}{3}$ liters); ``when'' with a time ($t = 4$ hours)."),
    BigIdea(r"Amount $=$ start $+ \int$(rate in $-$ rate out). Integral units are rate units times time units. The amount peaks where the net rate changes from $+$ to $-$; check the endpoints."),
    Check(r"A tank has $20$ L at $t = 0$; water enters at $3$ L/min and leaves at $t$ L/min. How much is in it at $t = 4$?", selfcheck(r"24 \text{ L}"), r"$20 + \int_0^4 (3 - t)\,dt = 20 + 12 - 8$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Water enters a tank at $R(t) = 6 + t$ liters per minute. The tank holds $10$ liters at $t = 0$ and nothing leaves. How much water is there at $t = 4$?", num(10 + I(6 + t, 0, 4)),
         r"$10 + \left[6t + \frac{t^2}{2}\right]_0^4 = 10 + 32 = 42$ liters.", work="1.6cm"),
    Item(r"A population changes at $P'(t) = 40 - 6t$ people per year, with $P(0) = 500$. Find $P(5)$.", num(500 + I(40 - 6 * t, 0, 5)), r"$500 + (200 - 75) = 625$.", work="1.4cm"),
    Item(r"Using the same population, at what time is it greatest on $0 \le t \le 10$?", num(sp.Rational(20, 3), tol=1e-3),
         r"$40 - 6t = 0$ at $t = \frac{20}{3}$; $P'$ changes from $+$ to $-$. $P\left(\frac{20}{3}\right) \approx 633.3$ beats $P(0) = 500$ and $P(10) = 600$.", work="2cm"),
    Item(r"Sand is added to a pile at $A(t) = 4$ tons per hour and removed at $R(t) = t$ tons per hour, $0 \le t \le 6$. The pile has $12$ tons at $t = 0$. How much is there at $t = 6$?",
         num(12 + I(4 - t, 0, 6)), r"$12 + (24 - 18) = 18$ tons.", work="1.6cm"),
    Item(r"For the sand pile, when is the pile largest, and how large is it?", selfcheck(r"20 \text{ tons at } t = 4"), r"$4 - t$ changes from $+$ to $-$ at $t = 4$: $12 + (16 - 8) = 20$ tons; $P(0) = 12$, $P(6) = 18$.", work="2cm"),
    Item(r"$R(t)$ is the rate, in gallons per minute, at which water drains from a pool. What are the units of $\int_0^{30} R(t)\,dt$?", selfcheck(r"\text{gallons}"), r"Gallons per minute times minutes.", work="0.8cm"),
    Item(r"$C(t)$ is the rate, in cars per hour, at which cars pass a toll booth, $t$ hours after 6 a.m. Interpret $\int_1^3 C(t)\,dt = 850$.", selfcheck(r"850 \text{ cars pass from 7 a.m. to 9 a.m.}"),
         r"A total of $850$ cars pass the toll booth from $t = 1$ to $t = 3$ hours (7 a.m. to 9 a.m.).", work="1.4cm"),
    Item(r"Rain falls at a rate $r(t)$ inches per hour, given by $0.2, 0.5, 0.4, 0.1$ at $t = 0, 1, 3, 4$. Use a trapezoidal sum to approximate the total rainfall on $0 \le t \le 4$.",
         num(trap([0, 1, 3, 4], [sp.Rational(1, 5), sp.Rational(1, 2), sp.Rational(2, 5), sp.Rational(1, 10)])),
         r"$1\cdot\frac{0.2 + 0.5}{2} + 2\cdot\frac{0.5 + 0.4}{2} + 1\cdot\frac{0.4 + 0.1}{2} = 0.35 + 0.9 + 0.25 = 1.5$ inches.", work="2cm"),
    Item(r"A bakery's profit grows at $P'(t) = 120\sqrt t$ dollars per month. Find the profit gained from $t = 1$ to $t = 4$.", num(I(120 * sp.sqrt(t), 1, 4)), r"$\left[80t^{3/2}\right]_1^4 = 640 - 80 = 560$ dollars.", work="1.6cm"),
    Item(r"$V(t)$ is the volume of water in a tank, and $V(0) = 200$. If $V'(t) = 10 - 2t$, find the volume at $t = 8$ and say whether it is increasing or decreasing then.", selfcheck(r"216;\ \text{decreasing}"),
         r"$V(8) = 200 + (80 - 64) = 216$; $V'(8) = -6 < 0$, decreasing.", work="1.8cm"),
]
same("p", [12 + I(4 - t, 0, 4), 500 + I(40 - 6 * t, 0, sp.Rational(20, 3)), 500 + I(40 - 6 * t, 0, 10), 200 + I(10 - 2 * t, 0, 8)], [20, sp.Rational(1900, 3), 600, 216])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"An amount starts at $30$ and changes at $A'(t) = 2t + 1$. Find $A(3)$.", num(30 + I(2 * t + 1, 0, 3)), r"$30 + 12$.", work="1.2cm"),
        Item(r"An amount starts at $100$ and changes at $A'(t) = -3t^2$. Find $A(2)$.", num(100 + I(-3 * t**2, 0, 2)), r"$100 - 8$.", work="1.2cm"),
        Item(r"An amount starts at $5$ and changes at $A'(t) = e^t$. Find $A(\ln 3)$.", num(7), r"$5 + (3 - 1)$.", work="1.2cm"),
    ),
    Variants(
        Item(r"Water enters at $E(t) = 10$ L/hr and leaves at $D(t) = 2t$ L/hr for $0 \le t \le 8$. At what time is the amount greatest?", num(5), r"$10 - 2t$ changes from $+$ to $-$ at $t = 5$.", work="1.4cm"),
        Item(r"People enter a park at $E(t) = 300 - 20t$ per hour and leave at $L(t) = 40t$ per hour, $0 \le t \le 10$. At what time is the number of people greatest?", num(5),
             r"$300 - 60t$ changes from $+$ to $-$ at $t = 5$.", work="1.4cm"),
        Item(r"Snow falls at $S(t) = 6$ cm/hr and melts at $M(t) = 3\sqrt t$ cm/hr, $0 \le t \le 9$. At what time is the snow deepest?", num(4), r"$6 = 3\sqrt t$ at $t = 4$.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"$R(t)$ is in liters per minute and $t$ is in minutes. The units of $\int_0^{10} R'(t)\,dt$ are", [r"liters", r"liters per minute", r"liters per minute per minute", r"minutes"], "B",
            r"$\int R' = $ change in $R$, in $R$'s units."),
        MCQ(r"$R(t)$ is in people per hour and $t$ is in hours. The units of $\int_2^6 R(t)\,dt$ are", [r"people per hour", r"hours", r"people", r"people per hour per hour"], "C", r"(people per hour)(hours)."),
    ),
    Variants(
        Item(r"Rates of flow $F(t)$ in L/min are $4, 6, 9$ at $t = 0, 3, 5$. Use a trapezoidal sum to approximate the total flow on $0 \le t \le 5$.", num(trap([0, 3, 5], [4, 6, 9])), r"$15 + 15 = 30$ L.", work="1.6cm"),
        Item(r"Rates of flow $F(t)$ in L/min are $8, 2, 4$ at $t = 0, 2, 6$. Use a left Riemann sum to approximate the total flow on $0 \le t \le 6$.", num(2 * 8 + 4 * 2), r"$16 + 8 = 24$ L.", work="1.6cm"),
        Item(r"Rates of flow $F(t)$ in L/min are $5, 7, 3$ at $t = 0, 4, 6$. Use a right Riemann sum to approximate the total flow on $0 \le t \le 6$.", num(4 * 7 + 2 * 3), r"$28 + 6 = 34$ L.", work="1.6cm"),
    ),
    Variants(
        Item(r"A tank holds $40$ gallons at $t = 0$. Water enters at $5$ gal/hr and leaves at $t + 1$ gal/hr. Find the greatest amount on $0 \le t \le 10$.", num(40 + I(4 - t, 0, 4)),
             r"Peak at $t = 4$: $40 + 8 = 48$; ends: $40$ and $40 - 10 = 30$.", work="1.8cm"),
        Item(r"A tank holds $40$ gallons at $t = 0$. Water enters at $5$ gal/hr and leaves at $t + 1$ gal/hr. Find the least amount on $0 \le t \le 10$.", num(40 + I(4 - t, 0, 10)),
             r"Candidates: $40$, $48$, $40 + (40 - 50) = 30$. Least: $30$.", work="1.8cm"),
    ),
]

# ---------------------------------------------------------------- test prep
W = lambda s: 30 + 10 * sp.sin(s / 2)
_m3 = float(sp.Integral(W(t), (t, 0, 6)).evalf())
close("m3", _m3, 219.800, 5e-3)
MCQS = [
    MCQ(r"Oil leaks from a tank at $L(t)$ gallons per hour. Which is the best interpretation of $\int_0^{4} L(t)\,dt = 18$?", [r"The leak rate is $18$ gallons per hour at $t = 4$",
        r"The tank has $18$ gallons at $t = 4$", r"The leak rate increases by $18$ gallons per hour over $4$ hours", r"A total of $18$ gallons leak out in the first $4$ hours"], "D", r"The integral of a rate is a total."),
    MCQ(r"A tank holds $60$ L at $t = 0$. Water enters at $E(t) = 12$ L/min and leaves at $D(t) = 3t$ L/min. How much water is in the tank at $t = 6$?", [r"$78$", r"$72$", r"$60$", r"$114$"], "A",
        r"$60 + \int_0^6 (12 - 3t)\,dt = 60 + 72 - 54 = 78$.", why_not={"B": "the water that entered, ignoring the start and the drain", "D": "ignored the drain"}),
    MCQ(r"Water flows into a reservoir at $W(t) = 30 + 10\sin\left(\frac t2\right)$ thousand gallons per day. To the nearest thousand gallons, how much flows in from $t = 0$ to $t = 6$?", [r"$31$", r"$220$", r"$180$", r"$250$"], "B",
        rf"$\int_0^6 W(t)\,dt \approx {_m3:.1f}$ thousand gallons.", calc=True),
    MCQ(r"$P(t)$ people are in a store, $P'(t) = 60 - 15t$ for $0 \le t \le 8$ hours, $P(0) = 20$. The number of people is greatest at", [r"$t = 0$", r"$t = 8$", r"$t = 4$", r"$t = 2$"], "C", r"$P'$ changes from $+$ to $-$ at $t = 4$."),
]
same("m2", [60 + I(12 - 3 * t, 0, 6)], [78])

# ---------------------------------------------------------------- FRQ
netF = (20 + 4 * t) - (t**2 + 8)
AF = lambda b: 100 + I(netF, 0, b)
same("frq", [netF.subs(t, 3), AF(6), AF(8), sp.solve(netF, t)], [15, 172, sp.Rational(460, 3), [-2, 6]])
FRQS = [
    FRQ("Water in a cistern", (
        r"Water flows into a cistern at the rate $E(t) = 20 + 4t$ gallons per hour and is pumped out at the rate $D(t) = t^2 + 8$ gallons per hour, for $0 \le t \le 8$. "
        r"At time $t = 0$ the cistern holds $100$ gallons."), [
        Part("a", r"Is the amount of water in the cistern increasing or decreasing at $t = 3$? Give a reason for your answer.", selfcheck(r"\text{increasing}"),
             r"$E(3) - D(3) = 32 - 17 = 15 > 0$, so the amount is increasing.", [(1, "increasing with reason")], work="1.6cm"),
        Part("b", r"Using correct units, interpret the meaning of $\displaystyle\int_0^8 D(t)\,dt$ in the context of the problem.", selfcheck(r"\text{total gallons pumped out from } t = 0 \text{ to } t = 8"),
             r"The total number of gallons of water pumped out of the cistern from $t = 0$ to $t = 8$ hours.", [(1, "interpretation with units")], work="1.6cm"),
        Part("c", r"Write an expression for $A(t)$, the amount of water in the cistern at time $t$, and find $A(8)$.", selfcheck(r"A(t) = 100 + \int_0^t (E(u) - D(u))\,du;\ A(8) = \tfrac{460}{3}"),
             r"$A(t) = 100 + \int_0^t \big(12 + 4u - u^2\big)\,du = 100 + 12t + 2t^2 - \frac{t^3}{3}$. $A(8) = 100 + 96 + 128 - \frac{512}{3} = \frac{460}{3} \approx 153.3$ gallons.",
             [(1, "integral expression"), (1, "antiderivative"), (1, "$A(8)$")], work="3cm"),
        Part("d", r"At what time $t$, $0 \le t \le 8$, is the amount of water in the cistern greatest? Justify your answer.", num(6),
             r"$E(t) - D(t) = 12 + 4t - t^2 = -(t - 6)(t + 2) = 0$ at $t = 6$, changing from $+$ to $-$. Candidates: $A(0) = 100$, $A(6) = 172$, $A(8) = \frac{460}{3}$. Greatest at $t = 6$ hours.",
             [(1, "sets $E - D = 0$"), (1, "candidates test"), (1, "answer with justification")], work="3cm"),
    ], frq_type="Rate in context"),
]

TOPIC = Topic(
    number="8.3", title="Using Accumulation Functions and Definite Integrals in Applied Contexts",
    unit="Unit 8: Applications of Integration", ced=["CHA-4.D", "CHA-4.D.1", "CHA-4.D.2"],
    goals=r"Find amounts from rates in and out, interpret integrals with units, and find when an amount is greatest.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
