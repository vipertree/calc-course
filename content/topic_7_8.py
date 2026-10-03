"""Topic 7.8: Exponential models with differential equations.

CED: FUN-7.F (FUN-7.F.1-FUN-7.F.3): dy/dt = ky has solution y = y0 e^(kt) (growth for k > 0, decay for k < 0); find k
from a second data point; half-life and doubling time ln 2 / |k|. Lesson example: P(0) = 500, P(3) = 800, find P(6).
Worked examples: a half-life, a tripling time.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)

t = sp.symbols("t")
same("lesson", [500 * sp.Rational(8, 5)**2], [1280])
close("ex1", float(80 * sp.Rational(1, 2)**sp.Rational(5, 2)), 14.142, 1e-3)
close("ex2", float(4 * sp.log(10) / sp.log(3)), 8.384, 1e-3)

NOTES = [
    Video("s7_8.py::Lesson", "Exponential models", 4),

    Section("Rate proportional to amount"),
    Formula("Exponential model", (
        r"\[ \frac{dy}{dt} = ky \quad \text{has solution} \quad y = \blank{y_0e^{kt}}, \] where $y_0 = y(0)$. If $k > 0$ the quantity grows; if $k < 0$ it decays.")),
    Text(r"Derivation: $\frac{dy}{y} = k\,dt$, $\ln|y| = kt + C$, $y = Ae^{kt}$, and $A = y(0)$."),
    Text(r"\textbf{Finding $k$.} Substitute a second data point and solve: $P(0) = 500$, $P(3) = 800$ gives $e^{3k} = \frac85$, $k = \frac13\ln\frac85$."),
    VideoExample('Finding k from data', work="3cm"),
    Formula("Half-life and doubling time", (r"Half-life ($k < 0$) and doubling time ($k > 0$): \[ T = \blank{\frac{\ln 2}{|k|}}, \] independent of the starting amount.")),
    BigIdea(r"A rate proportional to the amount means $y = y_0e^{kt}$. A second data point gives $k$; $\frac{\ln 2}{|k|}$ is the doubling time or half-life."),
    Check(r"$\frac{dy}{dt} = 0.3y$ and $y(0) = 20$. Find $y(t)$.", selfcheck(r"y = 20e^{0.3t}"), r"$y = y_0e^{kt}$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"$\frac{dP}{dt} = 0.02P$ and $P(0) = 1000$. Find $P(50)$.", num(1000 * sp.E, tol=0.5), r"$P = 1000e^{0.02t}$, $P(50) = 1000e \approx 2718.3$.", work="1.4cm"),
    Item(r"A quantity decays at a rate proportional to itself, from $200$ to $150$ in $4$ hours. Find $k$.", num(sp.log(sp.Rational(3, 4)) / 4, tol=1e-3),
         r"$150 = 200e^{4k}$, $k = \frac14\ln\frac34 \approx -0.0719$.", work="1.6cm"),
    Item(r"Using the same quantity, how much remains after $12$ hours?", num(sp.Rational(675, 8), tol=1e-3), r"$200\left(\frac34\right)^3 = 84.375$.", work="1.4cm"),
    Item(r"A population doubles every $6$ years. What is $k$ in $P = P_0e^{kt}$?", num(sp.log(2) / 6, tol=1e-4), r"$e^{6k} = 2$, $k = \frac{\ln 2}{6} \approx 0.1155$.", work="1.2cm"),
    Item(r"An isotope has $k = -0.0231$ per year. Find its half-life.", num(sp.log(2) / sp.Rational(231, 10000), tol=0.05), r"$\frac{\ln 2}{0.0231} \approx 30.0$ years.", work="1.2cm"),
    Item(r"A sample of $60$ mg has a half-life of $5$ hours. How much remains after $15$ hours?", num(sp.Rational(15, 2)), r"Three half-lives: $60 \cdot \frac18 = 7.5$ mg.", work="1.2cm"),
    Item(r"$\frac{dy}{dt} = ky$, $y(0) = 4$, $y(2) = 36$. Find $y(1)$.", num(12), r"$e^{2k} = 9$, so $e^k = 3$ and $y(1) = 12$.", work="1.4cm"),
    Item(r"Money grows continuously at $4\%$: $\frac{dA}{dt} = 0.04A$. How long does it take to double?", num(sp.log(2) / sp.Rational(4, 100), tol=0.01), r"$\frac{\ln 2}{0.04} \approx 17.33$ years.", work="1.2cm"),
]

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"The solution of $\frac{dy}{dt} = -0.4y$ with $y(0) = 50$ is", [r"$y = 50e^{-0.4t}$", r"$y = 50 - 0.4t$", r"$y = -0.4e^{50t}$", r"$y = 50e^{0.4t}$"], "A", r"$y = y_0e^{kt}$."),
        MCQ(r"The solution of $\frac{dy}{dt} = 1.2y$ with $y(0) = 3$ is", [r"$y = 1.2e^{3t}$", r"$y = 3e^{1.2t}$", r"$y = 3 + 1.2t$", r"$y = 3.6t$"], "B", r"$y = y_0e^{kt}$."),
    ),
    Variants(
        Item(r"$y(0) = 10$, $y(3) = 80$, $y = y_0e^{kt}$. Find $y(1)$.", num(20), r"$e^{3k} = 8$, $e^k = 2$.", work="1.2cm"),
        Item(r"$y(0) = 81$, $y(4) = 1$, $y = y_0e^{kt}$. Find $y(2)$.", num(9), r"$e^{4k} = \frac{1}{81}$, $e^{2k} = \frac19$.", work="1.2cm"),
        Item(r"$y(0) = 5$, $y(2) = 20$, $y = y_0e^{kt}$. Find $y(4)$.", num(80), r"$e^{2k} = 4$, $y(4) = 5 \cdot 16$.", work="1.2cm"),
    ),
    Variants(
        Item(r"A substance has a half-life of $8$ days. What fraction remains after $24$ days?", num(sp.Rational(1, 8)), r"Three half-lives.", work="1cm"),
        Item(r"A substance has a half-life of $3$ hours. What fraction remains after $12$ hours?", num(sp.Rational(1, 16)), r"Four half-lives.", work="1cm"),
        Item(r"A substance has a half-life of $20$ years. What fraction remains after $10$ years?", num(1 / sp.sqrt(2), tol=1e-3), r"Half a half-life: $\left(\frac12\right)^{1/2} \approx 0.707$.", work="1cm"),
    ),
    Variants(
        Item(r"Find the doubling time when $k = 0.1$.", num(10 * sp.log(2), tol=0.01), r"$\frac{\ln 2}{0.1} \approx 6.93$.", work="1cm"),
        Item(r"Find the doubling time when $k = 0.07$.", num(sp.log(2) / sp.Rational(7, 100), tol=0.01), r"$\frac{\ln 2}{0.07} \approx 9.90$.", work="1cm"),
        Item(r"Find the half-life when $k = -0.5$.", num(2 * sp.log(2), tol=0.01), r"$\frac{\ln 2}{0.5} \approx 1.39$.", work="1cm"),
    ),
    Variants(
        MCQ(r"Which situation is modeled by $\frac{dy}{dt} = ky$?", [r"A car moving at constant speed", r"A population whose growth rate is proportional to its size", r"Water draining at a constant rate", r"A ball thrown upward"], "B",
            r"Rate proportional to amount."),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"A population grows at a rate proportional to its size. It is $2000$ now and $3000$ in $5$ years. In $10$ years it will be", [r"$4000$", r"$4500$", r"$5000$", r"$6000$"], "B",
        r"$e^{5k} = 1.5$, so $2000(1.5)^2 = 4500$."),
    MCQ(r"Radium has a half-life of about $1600$ years. What percent remains after $800$ years?", [r"$50\%$", r"$75\%$", r"$70.7\%$", r"$25\%$"], "C", r"$\left(\frac12\right)^{1/2} \approx 0.707$."),
    MCQ(r"If $\frac{dy}{dt} = ky$ and $y$ triples every $2$ hours, then $k = $", [r"$\frac{\ln 2}{3}$", r"$\frac32$", r"$2\ln 3$", r"$\frac{\ln 3}{2}$"], "D", r"$e^{2k} = 3$."),
    MCQ(r"$\frac{dA}{dt} = 0.05A$ with $A(0) = 1000$. To the nearest dollar, $A(10) = $", [r"$1649$", r"$1500$", r"$1629$", r"$1051$"], "A", r"$1000e^{0.5} \approx 1648.72$.", calc=True),
]
close("m4", float(1000 * sp.exp(sp.Rational(1, 2))), 1648.72, 0.01)
same("m1", [2000 * sp.Rational(3, 2)**2], [4500])

FRQS = []

TOPIC = Topic(
    number="7.8", title="Exponential Models with Differential Equations",
    unit="Unit 7: Differential Equations", ced=["FUN-7.F", "FUN-7.F.1", "FUN-7.F.2", "FUN-7.F.3"],
    goals=r"Solve $\frac{dy}{dt} = ky$, find $k$ from data, and use half-life and doubling time.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
