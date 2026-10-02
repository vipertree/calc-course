"""Topic 1.8: Determining limits using the squeeze theorem.

CED: LIM-1.E.2 (squeeze theorem). Illustrative examples from the CED: sin(x)/x -> 1 and
(1 - cos x)/x -> 0, both shown here, the first by the unit-circle area squeeze.
"""
import sympy as sp

from calclib import (VideoExample, Variants, FRQ, MCQ, BigIdea, Check, Example, Figure, Formula, Item, Part, Section, Text, Topic, Video,
                     limchain, num, same, selfcheck)
from calclib.figs import graph

x = sp.symbols("x")
same("x^2 sin(1/x)", sp.limit(x**2 * sp.sin(1 / x), x, 0), 0)
same("sinx/x", sp.limit(sp.sin(x) / x, x, 0), 1)
same("1-cosx/x", sp.limit((1 - sp.cos(x)) / x, x, 0), 0)

FIG_SQ = graph("t1_8_squeeze", [("x^2*sin(deg(1/x))", -1, -0.01), ("x^2*sin(deg(1/x))", 0.01, 1),
                                ("x^2", -1, 1, "dashed"), ("-x^2", -1, 1, "dashed")],
               xr=(-1, 1), yr=(-1, 1), xstep=0.5, ystep=0.5, samples=700, w="6.4cm", h="5cm",
               caption=r"$-x^2 \le x^2\sin\frac1x \le x^2$")
FIG_CIRCLE = Figure(name="t1_8_circle", caption=r"Small triangle $\le$ sector $\le$ large triangle.", tikz=(
    r"\begin{tikzpicture}[scale=2.4]"
    r"\draw[->, line width=0.5pt] (-0.15,0) -- (1.35,0); \draw[->, line width=0.5pt] (0,-0.1) -- (0,1.25);"
    r"\draw[line width=0.9pt] (1,0) arc (0:90:1);"
    r"\fill[pattern=north east lines, pattern color=black!45] (0,0) -- (1,0) arc (0:50:1) -- cycle;"
    r"\draw[line width=0.8pt] (0,0) -- ({cos(50)},{sin(50)}) -- ({cos(50)},0);"
    r"\draw[line width=0.8pt, densely dashed] (0,0) -- (1,{tan(50)}) -- (1,0);"
    r"\node[font=\footnotesize] at (0.2,0.09) {$x$}; \draw (0.15,0) arc (0:50:0.15);"
    r"\node[right, font=\footnotesize] at (1,{tan(50)}) {$(1,\tan x)$};"
    r"\node[above right, font=\footnotesize] at ({cos(50)},{sin(50)}) {$(\cos x,\sin x)$};"
    r"\node[below, font=\footnotesize] at (1,0) {$1$};"
    r"\end{tikzpicture}"))
FIG_SINC = graph("t1_8_sinc", [("cos(deg(x))", -1.5, 1.5, "dashed"), ("1", -1.5, 1.5, "dashed"),
                               ("sin(deg(x))/x", -1.5, -0.001), ("sin(deg(x))/x", 0.001, 1.5)],
                 xr=(-1.5, 1.5), yr=(0, 1.2), open=[(0, 1)], xstep=0.5, ystep=0.5, w="6.4cm", h="5cm",
                 caption=r"$\cos x \le \dfrac{\sin x}{x} \le 1$")

NOTES = [
    Video("s1_8.py::Lesson", "The squeeze theorem", 4.5),

    Section("Trapping a function"),
    Text(r"Near $0$, $\sin\frac1x$ oscillates, and algebra can't simplify $x^2\sin\frac1x$. But $\displaystyle -1 \le \sin\dfrac1x \le 1$, and "
         r"multiplying by $x^2 \ge 0$ gives $\mblank{-x^2} \le x^2\sin\frac1x \le \blank{$x^2$}$."),
    FIG_SQ,
    Formula("Squeeze theorem", (
        r"If $g(x) \le f(x) \le h(x)$ for all $x$ near $c$ (except possibly at $c$), and "
        r"\[ \lim_{x\to c} g(x) = \lim_{x\to c} h(x) = L, \] then $\displaystyle \lim_{x\to c} f(x) = \mblank{L}$.")),
    Text(r"Since $\displaystyle \lim_{x\to0}(-x^2) = 0$ and $\displaystyle \lim_{x\to0}x^2 = 0$, the squeeze theorem gives "
         r"$\displaystyle \lim_{x\to0}x^2\sin\frac1x = \mblank{0}$."),

    Section("Why $\\frac{\\sin x}{x}$ approaches 1"),
    FIG_CIRCLE,
    Text(r"For a small angle $0 < x < \frac\pi2$ on the unit circle, compare three areas: "
         r"small triangle $\frac12\sin x$, sector $\frac12 x$, large triangle $\frac12\tan x$. So "
         r"$\sin x \le x \le \tan x$. Divide by $\sin x > 0$ and take reciprocals (which reverses the inequalities): "
         r"$\mblank{\cos x} \le \dfrac{\sin x}{x} \le \blank{$1$}$."),
    FIG_SINC,
    Text(r"Since $\displaystyle \lim_{x\to0^+}\cos x = 1$ and $\displaystyle \lim_{x\to0^+}1 = 1$, the squeeze theorem gives "
         r"\[ \lim_{x\to0^+}\frac{\sin x}{x} = 1. \] The function is even, so the left-hand limit is also $1$."),
    Formula("Two special trig limits ($x$ in radians)", (
        r"\[ \lim_{x\to 0}\frac{\sin x}{x} = \mblank{1} \qquad\qquad \lim_{x\to 0}\frac{1-\cos x}{x} = \mblank{0} \]"
        r"The second follows from the first:"
        r"\[ \lim_{x\to0}\frac{1-\cos x}{x} = \lim_{x\to0}\frac{1-\cos x}{x}\cdot\frac{1+\cos x}{1+\cos x} = "
        r"\lim_{x\to0}\frac{\sin x}{x}\cdot\frac{\sin x}{1+\cos x} = 1\cdot\frac02 = 0. \]")),

    Section("Using the special limits"),
    VideoExample('Match the angle', work="2.6cm"),
    VideoExample('Rewrite first', work="2.4cm"),
    VideoExample('Squeeze with a bounded factor', work="2.4cm"),
    BigIdea(r"When a function is too wild for algebra, trap it. If the two walls meet, the function inside goes where they go."),
    Check(r"Find \[ \lim_{x\to0}\frac{\sin(3x)}{\sin(4x)}. \]", num(sp.Rational(3, 4)),
          limchain(0, [r"\frac{\sin 3x}{\sin 4x}", r"\frac{\sin 3x}{3x}\cdot\frac{4x}{\sin 4x}\cdot\frac{3}{4}"], r"1\cdot1\cdot\frac34 = \frac34")),
]
same("ex1", sp.limit(sp.sin(5 * x) / x, x, 0), 5)
same("ex2", sp.limit(sp.tan(x) / x, x, 0), 1)
same("ex3", sp.limit(x * sp.cos(1 / x**2), x, 0), 0)
same("check", sp.limit(sp.sin(3 * x) / sp.sin(4 * x), x, 0), sp.Rational(3, 4))

# ---------------------------------------------------------------- practice (20)
PR = [
    (r"\frac{\sin(7x)}{x}", sp.sin(7 * x) / x, [r"7\cdot\frac{\sin 7x}{7x}"], r"7\cdot 1 = 7"),
    (r"\frac{x}{\sin(2x)}", x / sp.sin(2 * x), [r"\frac12\cdot\frac{2x}{\sin 2x}"], r"\frac12\cdot 1 = \frac12"),
    (r"\frac{\sin^2 x}{x^2}", sp.sin(x)**2 / x**2, [r"\left(\frac{\sin x}{x}\right)^2"], r"1^2 = 1"),
    (r"\frac{1-\cos x}{x^2}", (1 - sp.cos(x)) / x**2, [r"\frac{1-\cos^2 x}{x^2(1+\cos x)}", r"\left(\frac{\sin x}{x}\right)^2\frac{1}{1+\cos x}"],
     r"1\cdot\frac12 = \frac12"),
    (r"\frac{\sin x\cos x}{3x}", sp.sin(x) * sp.cos(x) / (3 * x), [r"\frac13\cdot\frac{\sin x}{x}\cdot\cos x"], r"\frac13\cdot1\cdot1 = \frac13"),
    (r"\frac{\tan(2x)}{x}", sp.tan(2 * x) / x, [r"2\cdot\frac{\sin 2x}{2x}\cdot\frac{1}{\cos 2x}"], r"2\cdot1\cdot1 = 2"),
    (r"\frac{\sin(5x)}{3x}", sp.sin(5 * x) / (3 * x), [r"\frac53\cdot\frac{\sin 5x}{5x}"], r"\frac53"),
    (r"\frac{\sin(x^2)}{x^2}", sp.sin(x**2) / x**2, None, None),
    (r"\frac{\sin(6x)}{\sin(2x)}", sp.sin(6 * x) / sp.sin(2 * x), [r"\frac{\sin 6x}{6x}\cdot\frac{2x}{\sin 2x}\cdot 3"], r"3"),
    (r"\frac{1-\cos(2x)}{x}", (1 - sp.cos(2 * x)) / x, [r"2\cdot\frac{1-\cos 2x}{2x}"], r"2\cdot 0 = 0"),
    (r"\frac{x^2}{\sin^2(3x)}", x**2 / sp.sin(3 * x)**2, [r"\frac19\left(\frac{3x}{\sin 3x}\right)^2"], r"\frac19"),
    (r"\frac{\sin x}{x^2+x}", sp.sin(x) / (x**2 + x), [r"\frac{\sin x}{x}\cdot\frac{1}{x+1}"], r"1\cdot 1 = 1"),
]
SUB = (r"Let $u = x^2$. As $x \to 0$, $u \to 0$, so $\displaystyle\lim_{x\to0}\frac{\sin(x^2)}{x^2} = "
       r"\lim_{u\to0}\frac{\sin u}{u} = 1$.")
PRACTICE = [Item(rf"Find $\displaystyle\lim_{{x\to0}}{tex}$.", num(sp.limit(e, x, 0)),
                 limchain(0, [tex] + steps, val) if steps else SUB, work="2cm")
            for tex, e, steps, val in PR]
R = sp.Rational
for (tex, e, steps, val), want in zip(PR, [7, R(1, 2), 1, R(1, 2), R(1, 3), 2, R(5, 3), 1, 3, 0, R(1, 9), 1]):
    same(f"practice {tex}", sp.limit(e, x, 0), want)   # the typed final values in PR must match these
PRACTICE += [
    Item(r"Use the squeeze theorem to find $\displaystyle\lim_{x\to0} x^2\cos\frac{3}{x}$. State the two bounding functions.", num(0),
         r"$-x^2 \le x^2\cos\frac3x \le x^2$, and $\displaystyle\lim_{x\to0}(-x^2) = \lim_{x\to0}x^2 = 0$, so the limit is $0$.", work="2.4cm"),
    Item(r"Suppose $4x - 5 \le f(x) \le x^2 - 2x + 4$ for all $x$ near $3$. Find $\displaystyle\lim_{x\to3} f(x)$.", num(7),
         r"$\displaystyle\lim_{x\to3}(4x-5) = 7$ and $\displaystyle\lim_{x\to3}(x^2-2x+4) = 7$. By the squeeze theorem the limit is $7$.", work="2cm"),
    Item(r"Suppose $1 - x^2 \le g(x) \le \cos x$ near $0$. Find $\displaystyle\lim_{x\to0} g(x)$.", num(1),
         r"$\displaystyle\lim_{x\to0}(1 - x^2) = 1$ and $\displaystyle\lim_{x\to0}\cos x = 1$, so the limit is $1$.", work="1.6cm"),
    Item(r"Use the squeeze theorem to find $\displaystyle\lim_{x\to0}\sqrt{x}\,\sin\frac{1}{x}$ (for $x > 0$).", num(0),
         r"$-\sqrt x \le \sqrt x\sin\frac1x \le \sqrt x$ and both bounds approach $0$ as $x\to0^+$.", work="2cm"),
    Item(r"Use the squeeze theorem to find $\displaystyle\lim_{x\to\infty}\frac{\cos x}{x}$.", num(0),
         r"For $x > 0$, $-\frac1x \le \frac{\cos x}{x} \le \frac1x$, and both bounds approach $0$ as $x\to\infty$.", work="2cm"),
    Item(r"If $|h(x) - 5| \le 2|x - 1|$ for all $x$, find $\displaystyle\lim_{x\to1}h(x)$.", num(5),
         r"$5 - 2|x-1| \le h(x) \le 5 + 2|x-1|$, and both bounds approach $5$ as $x\to1$.", work="2cm"),
    Item(r"Ana tries the squeeze theorem on $\displaystyle\lim_{x\to0}\sin\frac1x$ using $-1 \le \sin\frac1x \le 1$. Why doesn't it work?",
         selfcheck(r"\text{bounds have different limits}"),
         r"The bounds $-1$ and $1$ have different limits, so nothing is squeezed. (In fact this limit does not exist.)", work="2cm"),
    Item(r"Show that $\displaystyle\lim_{x\to0}\frac{\sin x}{x} = 1$ is only true in radians: estimate the limit if $x$ is measured in "
         r"degrees, using $x = 0.01^\circ$.", num(sp.pi / 180, tol=0.0001, display=r"\frac{\pi}{180}\approx 0.01745"),
         r"$\dfrac{\sin(0.01^\circ)}{0.01} \approx 0.01745 = \frac{\pi}{180}$. In degrees the limit is $\frac\pi{180}$, not $1$.",
         calc=True, work="2cm"),
]
same("p13", sp.limit(x**2 * sp.cos(3 / x), x, 0), 0)

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find $\displaystyle\lim_{x\to0}\frac{\sin(4x)}{x}$.", num(4), limchain(0, [r"4\cdot\frac{\sin 4x}{4x}"], 4), work="1.8cm"),
        Item(r"Find $\displaystyle\lim_{x\to0}\frac{\sin(5x)}{2x}$.", num(sp.Rational(5, 2)), limchain(0, [r"\frac52\cdot\frac{\sin 5x}{5x}"], r"\frac52"), work="1.8cm"),
        Item(r"Find $\displaystyle\lim_{x\to0}\frac{\sin(x/3)}{x}$.", num(sp.Rational(1, 3)), limchain(0, [r"\frac13\cdot\frac{\sin(x/3)}{x/3}"], r"\frac13"), work="1.8cm"),
    ),
    Variants(
        Item(r"Find $\displaystyle\lim_{x\to0}\frac{3x}{\sin x}$.", num(3), limchain(0, [r"3\cdot\frac{x}{\sin x}"], 3), work="1.8cm"),
        Item(r"Find $\displaystyle\lim_{x\to0}\frac{\sin(2x)}{\sin(6x)}$.", num(sp.Rational(1, 3)),
             limchain(0, [r"\frac{2}{6}\cdot\frac{\sin 2x}{2x}\cdot\frac{6x}{\sin 6x}"], r"\frac13"), work="1.8cm"),
        Item(r"Find $\displaystyle\lim_{x\to0}\frac{\tan x}{x}$.", num(1),
             limchain(0, [r"\frac{\sin x}{x}\cdot\frac{1}{\cos x}"], r"1\cdot1 = 1"), work="1.8cm"),
    ),
    Variants(
        Item(r"If $2 - x^2 \le h(x) \le 2 + x^2$ for all $x$, find $\displaystyle\lim_{x\to0} h(x)$.", num(2),
             r"Both bounds approach $2$; by the squeeze theorem the limit is $2$.", work="1.6cm"),
        Item(r"If $3x - 2 \le h(x) \le x^2 + x - 1$ for all $x$, find $\displaystyle\lim_{x\to1} h(x)$.", num(1),
             r"At $x = 1$ the lower bound gives $1$ and the upper bound gives $1$. By the squeeze theorem the limit is $1$.", work="1.6cm"),
        Item(r"If $\cos x \le h(x) \le 1 + x^2$ for all $x$ near $0$, find $\displaystyle\lim_{x\to0} h(x)$.", num(1),
             r"$\cos x \to 1$ and $1 + x^2 \to 1$, so by the squeeze theorem the limit is $1$.", work="1.6cm"),
    ),
    Variants(
        MCQ(r"Which pair of functions can be used to squeeze $x\sin\dfrac1x$ as $x\to0$?",
            [r"$-1$ and $1$", r"$-|x|$ and $|x|$", r"$0$ and $x$", r"$-x^2$ and $x^2$"], "B",
            r"$\left|x\sin\frac1x\right| \le |x|$, and $\displaystyle\lim_{x\to0}(\pm|x|) = 0$.",
            why_not={"A": "these bounds don't meet", "C": "the function is negative for some $x>0$",
                     "D": "the function is not always between $-x^2$ and $x^2$"}),
        MCQ(r"Which pair of functions can be used to squeeze $x^2\cos\dfrac{1}{x}$ as $x\to0$?",
            [r"$-1$ and $1$", r"$0$ and $x^2$", r"$-x^2$ and $x^2$", r"$-x$ and $x$"], "C",
            r"$-1 \le \cos\frac1x \le 1$, so multiplying by $x^2 \ge 0$ gives $-x^2 \le x^2\cos\frac1x \le x^2$. Both bounds go to $0$.",
            why_not={"A": "these bounds don't meet", "B": "the function can be negative", "D": "for negative $x$ the order flips"}),
        MCQ(r"$-|x| \le g(x) \le |x|$ near $0$. What does the squeeze theorem say about $\displaystyle\lim_{x\to0} g(x)$?",
            [r"It is $0$.", r"It is $1$.", r"Does not exist.", r"Nothing: we need the formula for $g$."], "A",
            r"Both bounds approach $0$, so $g$ is squeezed to $0$.", why_not={"D": "the bounds are enough"}),
    ),
    Variants(
        MCQ(r"$\displaystyle\lim_{x\to0}\frac{1-\cos x}{x}$ equals", [r"$0$", r"$\dfrac12$", r"$1$", r"Does not exist"], "A",
            r"One of the two special limits.", why_not={"B": "that is $\\lim \\frac{1-\\cos x}{x^2}$"}),
        MCQ(r"$\displaystyle\lim_{x\to0}\frac{\sin x}{x}$ equals (with $x$ in radians)", [r"$0$", r"$\pi$", r"Does not exist", r"$1$"], "D",
            r"One of the two special limits, proved with the unit-circle squeeze.", why_not={"A": "that's $\\sin 0$"}),
        MCQ(r"$\displaystyle\lim_{x\to0}\frac{5(1-\cos x)}{x}$ equals", [r"$5$", r"$0$", r"$\dfrac52$", r"Does not exist"], "B",
            r"$5\cdot\displaystyle\lim_{x\to0}\frac{1-\cos x}{x} = 5\cdot0 = 0$.", why_not={"A": "the special limit is $0$, not $1$"}),
    ),
]
same("q versions", [sp.limit(sp.sin(5 * x) / (2 * x), x, 0), sp.limit(sp.sin(x / 3) / x, x, 0), sp.limit(sp.sin(2 * x) / sp.sin(6 * x), x, 0),
                    sp.limit(sp.tan(x) / x, x, 0), 3 * 1 - 2, 1 + 1 - 1], [sp.Rational(5, 2), sp.Rational(1, 3), sp.Rational(1, 3), 1, 1, 1])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$\displaystyle\lim_{x\to0}\frac{\sin(3x)}{2x}$ is", [r"$0$", r"$\dfrac23$", r"$\dfrac32$", r"$1$"], "C",
        limchain(0, [r"\frac32\cdot\frac{\sin3x}{3x}"], r"\frac32"), why_not={"B": "inverted"}),
    MCQ(r"If $3x - 2 \le f(x) \le x^3$ for $x$ near $1$, then $\displaystyle\lim_{x\to1} f(x)$ is",
        [r"$1$", r"$0$", r"$3$", r"not determined by this information"], "A",
        r"$\displaystyle\lim_{x\to1}(3x-2) = 1 = \lim_{x\to1}x^3$, so the squeeze theorem gives $1$."),
    MCQ(r"$\displaystyle\lim_{x\to0}\frac{x^2}{1-\cos x}$ is", [r"$0$", r"$1$", r"$\dfrac12$", r"$2$"], "D",
        limchain(0, [r"\frac{x^2(1+\cos x)}{\sin^2 x}", r"\left(\frac{x}{\sin x}\right)^2(1+\cos x)"], r"1\cdot 2 = 2"),
        why_not={"C": "forgot to take the reciprocal"}),
    MCQ(r"Which limit can be found with the squeeze theorem using the bounds $\pm x^2$?",
        [r"$\displaystyle\lim_{x\to0}\frac{\sin x}{x}$", r"$\displaystyle\lim_{x\to0} x^2\sin\frac{1}{x^3}$",
         r"$\displaystyle\lim_{x\to0}\frac1{x}\sin x$", r"$\displaystyle\lim_{x\to0}\cos\frac1x$"], "B",
        r"$|\sin(\cdot)| \le 1$, so $-x^2 \le x^2\sin\frac1{x^3} \le x^2$."),
]
same("m1", sp.limit(sp.sin(3 * x) / (2 * x), x, 0), sp.Rational(3, 2))
same("m3", sp.limit(x**2 / (1 - sp.cos(x)), x, 0), 2)

FRQS = [
    FRQ("A squeeze", r"The function $f$ satisfies $1 - \dfrac{x^2}{2} \le f(x) \le \dfrac{\sin x}{x}$ for all $x \ne 0$ in the interval $-1 < x < 1$.", [
        Part("a", r"Find $\displaystyle\lim_{x\to0} f(x)$. Justify your answer.", num(1),
             r"$\displaystyle\lim_{x\to0}\left(1-\frac{x^2}2\right) = 1$ and $\displaystyle\lim_{x\to0}\frac{\sin x}{x} = 1$. Because "
             r"$1 - \frac{x^2}{2} \le f(x) \le \frac{\sin x}{x}$ near $x = 0$, the squeeze theorem gives $\displaystyle\lim_{x\to0} f(x) = 1$.",
             [(1, "both bounding limits equal $1$"), (1, "answer $1$, using the squeeze theorem")], work="2.8cm"),
        Part("b", r"Find the value of $\displaystyle\lim_{x\to0}\frac{f(x)\sin(2x)}{x}$, or show that it does not exist. Show the work "
                  r"that leads to your answer.", num(2),
             limchain(0, [r"\frac{f(x)\sin 2x}{x}", r"f(x)\cdot 2\cdot\frac{\sin 2x}{2x}"], r"1\cdot2\cdot1 = 2"),
             [(1, "rewrites with $\\frac{\\sin 2x}{2x}$ and uses the limit from part (a)"), (1, "answer $2$")], work="2.6cm"),
    ], frq_type="Limits and continuity"),
]
same("frq a", [sp.limit(1 - x**2 / 2, x, 0), sp.limit(sp.sin(x) / x, x, 0)], [1, 1])
same("frq b", sp.limit(sp.sin(2 * x) / x, x, 0), 2)

TOPIC = Topic(
    number="1.8", title="Determining Limits Using the Squeeze Theorem",
    unit="Unit 1: Limits and Continuity", ced=["LIM-1.E", "LIM-1.E.2"],
    goals=r"Use the squeeze theorem to find limits, including $\displaystyle\lim_{x\to0}\frac{\sin x}{x} = 1$ and "
          r"$\displaystyle\lim_{x\to0}\frac{1-\cos x}{x} = 0$.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
