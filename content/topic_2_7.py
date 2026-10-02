"""Topic 2.7: Derivatives of cos x, sin x, e^x, and ln x.

CED: FUN-3.A.3 (specific rules for sine, cosine, exponential, logarithm). The sine proof in the
notes uses the two special limits proved in Topic 1.8.
"""
import sympy as sp

from calclib import (Variants, FRQ, MCQ, BigIdea, Check, Example, FigureRow, Formula, Item, Part, Section, Text, Topic,
                     Video, VideoExample, expr, num, same, selfcheck)
from calclib.figs import graph

x, h, t = sp.symbols("x h t")
same("sine by definition", sp.limit((sp.sin(x + h) - sp.sin(x)) / h, h, 0), sp.cos(x))
same("e base", sp.limit((sp.exp(h) - 1) / h, h, 0), 1)

FIG_SIN = graph("t2_7_sin", [("sin(deg(x))", -3.3, 6.5), ("cos(deg(x))", -3.3, 6.5, "dashed")], xr=(-3.5, 6.6), yr=(-1.4, 1.4),
                xstep=1, w="8cm", h="3.8cm", caption=r"$y = \sin x$ (solid) and its slope function $y = \cos x$ (dashed).")
FIG_EXP = graph("t2_7_exp", [("exp(x)", -3, 1.5), ("ln(x)", 0.05, 4.5, "dashed"), ("x", -3, 4.5)], xr=(-3, 4.5), yr=(-3, 4.5),
                w="5.6cm", h="5.6cm", caption=r"$e^x$ (solid) and $\ln x$ (dashed): mirror images across $y = x$.")

NOTES = [
    Video("s2_7.py::Lesson", "Four special derivatives", 4),

    Section("Sine and cosine"),
    FIG_SIN,
    Text(r"The slope of $\sin x$ is $1$ at $x = 0$, $0$ at $x = \frac\pi2$ and $-1$ at $x = \pi$. The slope function is "
         r"\blank{$\cos x$}."),
    Text(r"\textbf{Proof.} Use the sum identity $\sin(x+h) = \sin x\cos h + \cos x\sin h$, then split the fraction: "
         r"\[ \begin{aligned} \frac{d}{dx}\sin x &= \lim_{h\to0}\frac{\sin(x+h) - \sin x}{h} \\ "
         r"&= \lim_{h\to0}\frac{\sin x\cos h + \cos x\sin h - \sin x}{h} \\ "
         r"&= \sin x\cdot\lim_{h\to0}\frac{\cos h - 1}{h} + \cos x\cdot\lim_{h\to0}\frac{\sin h}{h}. \end{aligned} \] "
         r"By Topic 1.8, $\displaystyle \lim_{h\to0}\frac{\cos h - 1}{h} = \mblank{0}$ and "
         r"$\displaystyle \lim_{h\to0}\frac{\sin h}{h} = \mblank{1}$, so the derivative is $\sin x\cdot 0 + \cos x\cdot 1 = \cos x$."),

    Section("The exponential and the natural log"),
    Text(r"\textbf{A puzzle.} Can a function be its own derivative? Its slope would have to equal its \blank{height} everywhere: as the function's value "
         r"gets higher, its rate of change must increase too. Nearly flat where it's small, steep where it's big."),
    FIG_EXP,
    Text(r"The slope of $2^x$ at $x = 0$ is about $0.693$ (Topic 1.1); the slope of $3^x$ there is about $1.099$. The number "
         r"$e \approx 2.718$ is the base whose slope at $0$ is exactly \mblank{1}. As a result, the slope of $e^x$ at every point "
         r"equals its \blank{height}."),
    Formula("Four derivatives ($x$ in radians)", (
        r"\[ \frac{d}{dx}[\sin x] = \mblank{\cos x} \qquad \frac{d}{dx}[\cos x] = \mblank{-\sin x} \]"
        r"\[ \frac{d}{dx}\left[e^x\right] = \mblank{e^x} \qquad \frac{d}{dx}[\ln x] = \mblank{\tfrac1x} \quad (x > 0) \]")),

    Section("Using the new rules"),
    VideoExample("Combine with earlier rules", work="2cm"),
    VideoExample("A tangent line", work="2cm"),
    VideoExample("In context", work="2.4cm"),
    BigIdea(r"Sine's slope is cosine, cosine's slope is negative sine, $e^x$ is its own slope, and $\ln x$ has slope $\frac1x$."),
    Check(r"Find the slope of the tangent line to $y = \ln x$ at $x = 5$.", num(sp.Rational(1, 5)), r"$\frac1x = \frac15$."),
]
same("ex1", sp.diff(3 * sp.sin(x) - 4 * sp.exp(x) + 2 * sp.log(x) - sp.cos(x), x),
     3 * sp.cos(x) - 4 * sp.exp(x) + 2 / x + sp.sin(x))
same("ex3", sp.diff(30 - 25 * sp.cos(t), t).subs(t, sp.pi / 2), 25)

# ---------------------------------------------------------------- practice
P = [(r"y = 5\cos x - 2\sin x", 5 * sp.cos(x) - 2 * sp.sin(x)), (r"y = e^x + x^e", sp.exp(x) + x**sp.E),
     (r"y = 4\ln x - \dfrac{1}{x}", 4 * sp.log(x) + -1 / x), (r"y = \dfrac{\sin x}{3} + 7", sp.sin(x) / 3 + 7),
     (r"y = \ln(x^3)", 3 * sp.log(x)), (r"y = 2e^x - \pi\cos x", 2 * sp.exp(x) - sp.pi * sp.cos(x))]
SOL = [r"$-5\sin x - 2\cos x$.", r"$e^x + e\,x^{e-1}$ (the second term uses the power rule).", r"$\dfrac4x + \dfrac{1}{x^2}$.",
       r"$\dfrac{\cos x}{3}$.", r"Rewrite $\ln(x^3) = 3\ln x$: $\dfrac3x$.", r"$2e^x + \pi\sin x$."]
PRACTICE = [Item(rf"Find $\dfrac{{dy}}{{dx}}$ for ${tex}$.", expr(str(sp.diff(e, x))), sol, work="1.6cm")
            for (tex, e), sol in zip(P, SOL)]
PRACTICE += [
    Item(r"Find the equation for the line tangent to $y = \sin x$ at $x = \pi$.", expr("pi - x"),
         r"Point $(\pi, 0)$, slope $\cos\pi = -1$: $y = -(x - \pi) = \pi - x$.", work="2cm"),
    Item(r"Find the equation for the line tangent to $y = \ln x$ at $x = 1$.", expr("x - 1"), r"Point $(1, 0)$, slope $1$: $y = x - 1$.",
         work="1.8cm"),
    Item(r"$y = x + 2\cos x$ has two horizontal tangent lines for $x$ in $(0, \pi)$. Find the smaller $x$-value.", num(sp.pi / 6),
         r"$1 - 2\sin x = 0$, so $\sin x = \frac12$: $x = \frac\pi6$ or $\frac{5\pi}{6}$. The smaller is $\frac\pi6$.",
         work="2cm"),
    Item(r"Where does $y = e^x$ have slope $5$?", num(sp.log(5)), r"$e^x = 5$ gives $x = \ln 5$.", work="1.4cm"),
]
same("p9 roots", sorted(sp.solve(1 - 2 * sp.sin(x), x)), [sp.pi / 6, 5 * sp.pi / 6])

# extra practice (round 1)
P2 = [(r"y = 3e^x - 4\ln x", 3 * sp.exp(x) - 4 * sp.log(x), r"$3e^x - \dfrac4x$."),
      (r"y = \sin x + \cos x", sp.sin(x) + sp.cos(x), r"$\cos x - \sin x$."),
      (r"y = \ln\sqrt{x}", sp.log(x) / 2, r"Rewrite $\ln\sqrt x = \frac12\ln x$: $\dfrac{1}{2x}$."),
      (r"y = e^{x + 2}", sp.exp(2) * sp.exp(x), r"Rewrite $e^{x+2} = e^2\cdot e^x$, a constant times $e^x$: $e^{x+2}$."),
      (r"y = x^3 - 2\cos x + e", x**3 - 2 * sp.cos(x) + sp.E, r"$3x^2 + 2\sin x$.")]
for tex, e, sol in P2:
    PRACTICE.append(Item(rf"Find $\dfrac{{dy}}{{dx}}$ for ${tex}$.", expr(str(sp.diff(e, x))), sol, work="1.6cm"))
PRACTICE += [
    Item(r"Find the equation for the line tangent to $y = \cos x$ at $x = \dfrac\pi2$.", expr("pi/2 - x"),
         r"Point $\left(\frac\pi2, 0\right)$, slope $-\sin\frac\pi2 = -1$: $y = -\left(x - \frac\pi2\right) = \frac\pi2 - x$.",
         work="2cm"),
    Item(r"Find the equation for the line tangent to $y = 2\ln x$ at $x = e$.", expr("2*x/E"),
         r"Point $(e, 2)$, slope $\frac2e$: $y - 2 = \frac2e(x - e)$, so $y = \frac2e x$.", work="2cm"),
    Item(r"Where does $y = 3\ln x$ have slope $\dfrac12$?", num(6), r"$\dfrac3x = \dfrac12$, so $x = 6$.", work="1.4cm"),
    Item(r"Find the smallest positive $x$ where $y = \sin x - x$ has a horizontal tangent.", num(2 * sp.pi),
         r"$\cos x - 1 = 0$ means $\cos x = 1$, so $x = 0, 2\pi, 4\pi, \ldots$ The smallest positive one is $2\pi$.",
         work="1.8cm"),
    Item(r"A mass on a spring has position $s(t) = 5\cos t$ cm at time $t$ seconds. Find the velocity at $t = \dfrac{\pi}{6}$.",
         num(-sp.Rational(5, 2), display=r"-2.5\text{ cm/s}"),
         r"$v(t) = -5\sin t$, so $v\!\left(\frac\pi6\right) = -5\cdot\frac12 = -2.5$ cm/s.", work="1.8cm"),
]
same("x1 derivs", [sp.diff(e, x) for _, e, _ in P2],
     [3 * sp.exp(x) - 4 / x, sp.cos(x) - sp.sin(x), 1 / (2 * x), sp.exp(x + 2), 3 * x**2 + 2 * sp.sin(x)])
same("x1 tan cos", sp.expand(0 - (x - sp.pi / 2)), sp.pi / 2 - x)
same("x1 tan ln", sp.expand(2 + (2 / sp.E) * (x - sp.E)), 2 * x / sp.E)
same("x1 ln slope", sp.solve(sp.Eq(3 / x, sp.Rational(1, 2)), x), [6])
same("x1 v", sp.diff(5 * sp.cos(t), t).subs(t, sp.pi / 6), -sp.Rational(5, 2))

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find $f'(x)$ for $f(x) = 6\sin x + 3e^x$.", expr("6*cos(x)+3*exp(x)"), r"$6\cos x + 3e^x$.", work="1.4cm"),
        Item(r"Find $f'(x)$ for $f(x) = 4\cos x - e^x$.", expr("-4*sin(x)-exp(x)"), r"$-4\sin x - e^x$.", work="1.4cm"),
        Item(r"Find $f'(x)$ for $f(x) = 2e^x + \sin x - x^2$.", expr("2*exp(x)+cos(x)-2*x"), r"$2e^x + \cos x - 2x$.", work="1.4cm"),
    ),
    Variants(
        Item(r"Find $\dfrac{dy}{dx}$ for $y = 5\ln x - 2\cos x$.", expr("5/x+2*sin(x)"), r"$\dfrac5x + 2\sin x$.", work="1.4cm"),
        Item(r"Find $\dfrac{dy}{dx}$ for $y = \ln x + \dfrac{3}{x}$.", expr("1/x-3/x**2"), r"$\dfrac1x - \dfrac{3}{x^2}$.", work="1.4cm"),
        Item(r"Find $\dfrac{dy}{dx}$ for $y = \ln(x^4)$.", expr("4/x"), r"Rewrite as $4\ln x$: $\dfrac4x$.", work="1.4cm"),
    ),
    Variants(
        Item(r"Find the slope of the tangent line to $y = \cos x$ at $x = \frac\pi2$.", num(-1), r"$-\sin\frac\pi2 = -1$.", work="1.4cm"),
        Item(r"Find the slope of the tangent line to $y = \sin x$ at $x = \frac\pi3$.", num(sp.Rational(1, 2)), r"$\cos\frac\pi3 = \frac12$.", work="1.4cm"),
        Item(r"Find the slope of the tangent line to $y = e^x$ at $x = \ln 3$.", num(3), r"$e^{\ln 3} = 3$.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"Which function is its own derivative?", [r"$\ln x$", r"$e^x$", r"$x^e$", r"$\sin x$"], "B", r"$\frac{d}{dx}e^x = e^x$."),
        MCQ(r"Which function has derivative $-\sin x$?", [r"$\sin x$", r"$-\cos x$", r"$\cos x$", r"$\tan x$"], "C", r"$\frac{d}{dx}\cos x = -\sin x$.",
            why_not={"B": "that has derivative $\\sin x$"}),
        MCQ(r"Which function has derivative $\dfrac1x$ for $x > 0$?", [r"$\ln x$", r"$x^{-1}$", r"$e^x$", r"$-\dfrac{1}{x^2}$"], "A", r"$\frac{d}{dx}\ln x = \frac1x$.",
            why_not={"B": "that IS $\\frac1x$; its derivative is $-\\frac1{x^2}$"}),
    ),
    Variants(
        MCQ(r"If $f(x) = \ln x$, then $f'(e)$ is", [r"$1$", r"$e$", r"$\dfrac1e$", r"$0$"], "C", r"$\frac1x$ at $x = e$.", why_not={"A": "that is $f(e)$"}),
        MCQ(r"If $f(x) = 3\sin x$, then $f'(\pi)$ is", [r"$0$", r"$3$", r"$-3$", r"$3\pi$"], "C", r"$3\cos\pi = -3$.", why_not={"A": "that is $f(\\pi)$"}),
        MCQ(r"If $f(x) = e^x - x$, then $f'(0)$ is", [r"$1$", r"$0$", r"$e - 1$", r"$-1$"], "B", r"$e^0 - 1 = 0$.", why_not={"A": "that is $f(0)$"}),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$\displaystyle\lim_{h\to0}\frac{\cos\left(\frac\pi3 + h\right) - \frac12}{h}$ is",
        [r"$-\dfrac{\sqrt3}{2}$", r"$\dfrac12$", r"$\dfrac{\sqrt3}{2}$", r"$0$"], "A",
        r"It is the derivative of $\cos x$ at $\frac\pi3$: $-\sin\frac\pi3 = -\frac{\sqrt3}2$.", why_not={"C": "forgot the negative"}),
    MCQ(r"The line tangent to $y = 2e^x$ at $x = 0$ is", [r"$y = x + 2$", r"$y = 2x$", r"$y = 2x + 2$", r"$y = 2x + 1$"], "C",
        r"Point $(0, 2)$, slope $2$."),
    MCQ(r"If $f(x) = x^2 - \ln x$, for what value of $x > 0$ is $f'(x) = 0$?", [r"$1$", r"$\sqrt2$", r"$\dfrac12$", r"$\dfrac{\sqrt2}{2}$"], "D",
        r"$2x - \frac1x = 0$ gives $x^2 = \frac12$, so $x = \frac{\sqrt2}2$.", why_not={"C": "forgot the square root"}),
    MCQ(r"A weight on a spring has position $s(t) = 4\sin t$ cm. What is its velocity at $t = \pi$?",
        [r"$0$ cm/s", r"$4$ cm/s", r"$-4$ cm/s", r"$4\pi$ cm/s"], "C", r"$v = 4\cos t$, and $4\cos\pi = -4$."),
]
same("m1", sp.limit((sp.cos(sp.pi / 3 + h) - sp.Rational(1, 2)) / h, h, 0), -sp.sqrt(3) / 2)
same("m3", [r for r in sp.solve(sp.diff(x**2 - sp.log(x), x), x) if r > 0], [sp.sqrt(2) / 2])

FRQS = [
    FRQ("Tide model", (
        r"The depth of water at a dock is $D(t) = 8 + 3\sin t$ feet, where $t$ is measured in hours, $0 \le t \le 7$."), [
        Part("a", r"Find $D'(t)$.", expr("3*cos(t)", var="t"), r"$D'(t) = 3\cos t$.", [(1, "derivative")], work="1.4cm"),
        Part("b", r"Find $D'(2)$. Is the water level rising or falling at $t = 2$? Explain.", num(3 * sp.cos(2), tol=0.001,
             display=r"3\cos 2 \approx -1.248"),
             r"$D'(2) = 3\cos 2 \approx -1.248 < 0$: the depth is falling at about 1.248 feet per hour.",
             [(1, "value"), (1, "falling because $D'(2) < 0$")], work="2.2cm"),
        Part("c", r"At what time in $(0, 7)$ is the depth greatest? (Hint: where is $D'(t) = 0$ and changing from positive to "
                  r"negative?)", num(sp.pi / 2), r"$3\cos t = 0$ at $t = \frac\pi2$ and $\frac{3\pi}2$; $D'$ changes from positive to "
                                                  r"negative at $\frac\pi2$, where $D = 11$ feet.",
             [(1, "$t = \\frac\\pi2$ with reason")], work="2.2cm"),
    ], frq_type="Rates in context", calc=True),
]

TOPIC = Topic(
    number="2.7", title=r"Derivatives of $\cos x$, $\sin x$, $e^x$, and $\ln x$",
    unit="Unit 2: Differentiation", ced=["FUN-3.A", "FUN-3.A.3"],
    goals=r"Differentiate $\sin x$, $\cos x$, $e^x$ and $\ln x$, and combine them with the earlier rules.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
