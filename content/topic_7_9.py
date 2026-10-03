"""Topic 7.9: Logistic models with differential equations (BC only).

CED: FUN-7.G (FUN-7.G.1-FUN-7.G.3): dP/dt = kP(1 - P/L); the carrying capacity L is the limiting value for P(0) > 0;
growth is fastest at P = L/2, where the solution curve has its inflection point. Lesson example:
dP/dt = 0.4P(1 - P/1000), P(0) = 100. Worked examples: find L from a factored form, the solution formula.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Formula, Item, Part, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)

P, t = sp.symbols("P t")


def logistic_solution(L, k, P0):
    """P(t) = L / (1 + A e^(-kt)) with A = L/P0 - 1."""
    A = sp.Rational(L) / P0 - 1
    return L / (1 + A * sp.exp(-k * t)), A


def fastest(rate):
    """Value of P where the quadratic rate dP/dt is largest."""
    return sp.solve(sp.diff(rate, P), P)[0]


def capacity(rate):
    """Nonzero equilibrium of dP/dt."""
    return [r for r in sp.solve(rate, P) if r != 0][0]


lesson = sp.Rational(2, 5) * P * (1 - P / 1000)
same("lesson L", [capacity(lesson), fastest(lesson)], [1000, 500])
same("lesson concavity", [sp.sign(sp.diff(lesson, P).subs(P, 300))], [1])
ex1 = sp.Rational(1, 500) * P * (500 - P)
same("ex1", [capacity(ex1), fastest(ex1)], [500, 250])
sol, A = logistic_solution(1000, sp.Rational(2, 5), 100)
same("ex2 A", [A], [9])
close("ex2 P5", float(sol.subs(t, 5)), 450.9, 0.05)

NOTES = [
    Video("s7_9.py::Lesson", "Logistic models", 4),

    Section("Growth that levels off"),
    Formula("Logistic model", (
        r"\[ \frac{dP}{dt} = kP\left(1 - \frac{P}{L}\right), \] where $k > 0$ and $L$ is the \blank{carrying capacity}. "
        r"The rate is near $kP$ when $P$ is small and near $0$ when $P$ is close to $L$.")),
    Text(r"\textbf{Reading the equation.} Set $\frac{dP}{dt} = 0$: the equilibria are $P = 0$ and $P = L$. "
         r"Below $L$ the rate is positive, so $P$ climbs toward $L$; above $L$ it is negative, so $P$ falls toward $L$. "
         r"Either way, $\lim_{t\to\infty} P(t) = L$ whenever $P(0) > 0$."),
    Text(r"\textbf{Rewrite first.} $\frac{dP}{dt} = 0.002P(500 - P)$ is logistic too: factor out $500$ to get $1P\left(1 - \frac{P}{500}\right)$, so $L = 500$. "
         r"The quick route is to find where the right side is zero."),
    Formula("Fastest growth", (
        r"$\frac{dP}{dt}$ is a downward parabola in $P$ with zeros $0$ and $L$, so it is largest at \[ P = \blank{\frac L2}. \] "
        r"There $\frac{d^2P}{dt^2} = 0$: the solution curve changes from bowl (concave up, $P < \frac L2$) to hill (concave down, $\frac L2 < P < L$).")),
    VideoExample('Using the model', work="3cm"),
    Text(r"\textbf{The solution formula.} The solution is $P = \dfrac{L}{1 + Ae^{-kt}}$ with $A = \dfrac{L}{P(0)} - 1$. "
         r"The AP exam asks you to read the equation (limit, fastest growth, concavity) far more often than to use this formula."),
    BigIdea(r"In $\frac{dP}{dt} = kP\left(1 - \frac PL\right)$, the population approaches $L$ and grows fastest at $\frac L2$. Find $L$ by asking where the rate is zero."),
    Check(r"$\frac{dP}{dt} = 0.3P\left(1 - \frac{P}{2400}\right)$. At what population is it growing fastest?", selfcheck(r"P = 1200"), r"Half the carrying capacity."),
]

# ---------------------------------------------------------------- practice
r1 = sp.Rational(3, 10) * P * (1 - P / 800)
r4 = 2 * P - sp.Rational(4, 1000) * P**2
r6 = sp.Rational(1, 2) * P * (1 - P / 600)
r7 = sp.Rational(2, 10) * P - sp.Rational(1, 10000) * P**2
s8, _ = logistic_solution(900, sp.Rational(3, 10), 100)
t8 = sp.log(8) / sp.Rational(3, 10)                     # 1 + 8e^(-0.3t) = 2
same("p8", [sp.simplify(s8.subs(t, t8))], [450])
PRACTICE = [
    Item(r"$\frac{dP}{dt} = 0.3P\left(1 - \frac{P}{800}\right)$ and $P(0) = 50$. Find $\lim_{t\to\infty} P(t)$.", num(capacity(r1)), r"The carrying capacity, $800$.", work="1cm"),
    Item(r"For the same model, at what population is $P$ growing fastest?", num(fastest(r1)), r"$\frac L2 = 400$.", work="1cm"),
    Item(r"$\frac{dy}{dt} = 0.01y(250 - y)$ and $y(0) = 300$. Find $\lim_{t\to\infty} y(t)$.", num(250),
         r"The rate is negative for $y > 250$, so $y$ falls toward $250$.", work="1.2cm"),
    Item(r"$\frac{dP}{dt} = 2P - 0.004P^2$. Find the carrying capacity.", num(capacity(r4)), r"$2P(1 - 0.002P) = 0$ at $P = 500$.", work="1.2cm"),
    Item(r"A logistic population has $L = 1200$ and $P(0) = 200$. In $P = \dfrac{L}{1 + Ae^{-kt}}$, find $A$.", num(logistic_solution(1200, 1, 200)[1]),
         r"$200 = \frac{1200}{1 + A}$, so $1 + A = 6$, $A = 5$.", work="1.2cm"),
    Item(r"$\frac{dP}{dt} = 0.5P\left(1 - \frac{P}{600}\right)$. Find $\frac{dP}{dt}$ when $P = 200$.", num(r6.subs(P, 200), tol=0.01),
         r"$0.5(200)\left(\frac23\right) = \frac{200}{3} \approx 66.67$.", work="1.2cm"),
    Item(r"$\frac{dP}{dt} = 0.2P - 0.0001P^2$. At what population is $P$ growing fastest?", num(fastest(r7)), r"$L = 2000$, so $1000$.", work="1.2cm"),
    Item(r"$P(t) = \dfrac{900}{1 + 8e^{-0.3t}}$. When does $P$ reach $450$?", num(t8, tol=0.01),
         r"$1 + 8e^{-0.3t} = 2$, $e^{-0.3t} = \frac18$, $t = \frac{\ln 8}{0.3} \approx 6.93$.", work="1.6cm"),
]
same("p8 start", [s8.subs(t, 0)], [100])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        MCQ(r"Which differential equation is logistic?", [r"$\frac{dP}{dt} = 0.2P$", r"$\frac{dP}{dt} = 0.2(100 - P)$", r"$\frac{dP}{dt} = 0.2P(100 - P)$", r"$\frac{dP}{dt} = 0.2t(100 - t)$"], "C",
            r"The rate is $P$ times (capacity minus $P$)."),
        MCQ(r"Which differential equation is logistic?", [r"$\frac{dy}{dt} = 3y - 0.01y^2$", r"$\frac{dy}{dt} = 3y$", r"$\frac{dy}{dt} = 3 - 0.01y$", r"$\frac{dy}{dt} = 3t - 0.01t^2$"], "A",
            r"$3y(1 - \frac{y}{300})$."),
    ),
    Variants(
        Item(r"$\frac{dP}{dt} = 0.05P(400 - P)$. Find the carrying capacity.", num(400), r"Zero at $P = 400$.", work="1cm"),
        Item(r"$\frac{dP}{dt} = 4P - 0.02P^2$. Find the carrying capacity.", num(capacity(4 * P - sp.Rational(2, 100) * P**2)), r"$4 = 0.02P$ at $P = 200$.", work="1cm"),
        Item(r"$\frac{dP}{dt} = 0.6P\left(1 - \frac{P}{3500}\right)$. Find the carrying capacity.", num(3500), r"$L = 3500$.", work="1cm"),
    ),
    Variants(
        Item(r"$\frac{dP}{dt} = 0.1P\left(1 - \frac{P}{5000}\right)$. At what population is the growth fastest?", num(2500), r"$\frac L2$.", work="1cm"),
        Item(r"$\frac{dP}{dt} = 0.003P(900 - P)$. At what population is the growth fastest?", num(fastest(sp.Rational(3, 1000) * P * (900 - P))), r"$L = 900$, so $450$.", work="1cm"),
        Item(r"$\frac{dP}{dt} = 1.5P - 0.0025P^2$. At what population is the growth fastest?", num(fastest(sp.Rational(3, 2) * P - sp.Rational(25, 10000) * P**2)), r"$L = 600$, so $300$.", work="1cm"),
    ),
    Variants(
        Item(r"$\frac{dP}{dt} = 0.2P\left(1 - \frac{P}{700}\right)$, $P(0) = 1000$. Find $\lim_{t\to\infty} P(t)$.", num(700), r"Above $L$ the rate is negative; $P$ falls to $700$.", work="1cm"),
        Item(r"$\frac{dP}{dt} = 0.2P\left(1 - \frac{P}{700}\right)$, $P(0) = 0$. Find $\lim_{t\to\infty} P(t)$.", num(0), r"$P = 0$ is an equilibrium: nothing to grow.", work="1cm"),
        Item(r"$\frac{dP}{dt} = 0.2P\left(1 - \frac{P}{700}\right)$, $P(0) = 20$. Find $\lim_{t\to\infty} P(t)$.", num(700), r"Rises to the carrying capacity.", work="1cm"),
    ),
    Variants(
        MCQ(r"$\frac{dP}{dt} = 0.5P\left(1 - \frac{P}{200}\right)$ with $P(0) = 40$. The graph of $P$ is", [r"concave up for all $t$", r"concave down for all $t$",
            r"concave up while $P < 100$, then concave down", r"concave down while $P < 100$, then concave up"], "C", r"Bowl below $\frac L2$, hill above."),
    ),
]

# ---------------------------------------------------------------- test prep
m4, _ = logistic_solution(5000, sp.Rational(1, 2), 500)
MCQS = [
    MCQ(r"A population satisfies $\frac{dP}{dt} = 0.04P - 0.0001P^2$. Which statement is true?", [r"$P$ grows fastest when $P = 200$", r"$\lim_{t\to\infty} P = 400$ for every $P(0) > 0$",
        r"$P$ grows fastest when $P = 400$", r"$P$ decreases whenever $P > 200$"], "B", r"$0.04P(1 - \frac{P}{400})$: $L = 400$, fastest at $200$, and $P(0) > 0$ always leads to $400$."),
    MCQ(r"$\frac{dy}{dt} = 0.7y\left(1 - \frac{y}{1600}\right)$ and $y(0) = 2000$. Which is true?", [r"$y$ is increasing and $\lim y = 1600$", r"$y$ is increasing without bound",
        r"$y$ is decreasing and $\lim y = 0$", r"$y$ is decreasing and $\lim y = 1600$"], "D", r"Above the capacity the rate is negative."),
    MCQ(r"A logistic population $P$ has carrying capacity $360$. For what value of $P$ is $\frac{d^2P}{dt^2} = 0$ (with $0 < P < 360$)?", [r"$90$", r"$180$", r"$240$", r"$360$"], "B", r"The inflection point is at $\frac L2$."),
    MCQ(r"A town of $500$ has carrying capacity $5000$ and $k = 0.5$, so $P = \dfrac{5000}{1 + 9e^{-0.5t}}$. To the nearest person, $P(4) = $", [r"$2254$", r"$1500$", r"$4500$", r"$1225$"], "A",
        r"$\frac{5000}{1 + 9e^{-2}} \approx 2254$.", calc=True),
]
same("m1", [capacity(sp.Rational(4, 100) * P - sp.Rational(1, 10000) * P**2), fastest(sp.Rational(4, 100) * P - sp.Rational(1, 10000) * P**2)], [400, 200])
close("m4", float(m4.subs(t, 4)), 2254, 1)

FRQS = []

TOPIC = Topic(
    number="7.9", title="Logistic Models with Differential Equations",
    unit="Unit 7: Differential Equations", ced=["FUN-7.G", "FUN-7.G.1", "FUN-7.G.2", "FUN-7.G.3"],
    goals=r"Read a logistic differential equation: carrying capacity, limiting behavior, and where growth is fastest.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS, bc_only=True)
