"""Topic 2.9: The quotient rule.

CED: FUN-3.B.2 (quotient rule). Derived from the product rule in the notes, as in the video.
The average-cost example matches the video: C(n) = 2000 + 5n, average cost falls $0.20 per item at n = 100.
"""
import sympy as sp

from calclib import (Variants, FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Text, Topic, Video, VideoExample, expr, num,
                     same, selfcheck)

x, n = sp.symbols("x n")
same("example", sp.simplify(sp.diff((x**2 + 1) / (x - 3), x) - (x**2 - 6 * x - 1) / (x - 3)**2), 0)
same("avg cost", sp.diff((2000 + 5 * n) / n, n).subs(n, 100), sp.Rational(-1, 5))


def D(e):
    return sp.simplify(sp.diff(e, x))


NOTES = [
    Video("s2_9.py::Lesson", "The quotient rule", 3),

    Section("Deriving the rule"),
    Text(r"\textbf{Picture it.} A rectangle with area $f$ and width $g$ has height $Q = \dfrac{f}{g}$. Nudge $x$: "
         r"\[ df = Q\,dg + g\,dQ + dg\,dQ, \] two strips and a corner, just like the product rule. "
         r"Divide by $dx$ and let the nudge shrink to $0$; the corner vanishes."),
    Text(r"Let $Q = \dfrac{f}{g}$, so $f = Qg$. By the product rule, $f' = Q'g + Qg'$. Solving, "
         r"\[ Q' = \frac{f' - Qg'}{g} = \frac{f' - \frac{f}{g}g'}{g} = \frac{f'g - fg'}{g^2}. \]"),
    Formula("Quotient rule", (
        r"\[ \frac{d}{dx}\left[\frac{f(x)}{g(x)}\right] = \frac{g(x)\,f'(x) - f(x)\,g'(x)}{\left[g(x)\right]^2}, \qquad g(x) \ne 0 \]"
        r"With $u$ on top and $v$ on the bottom (each one a function of $x$): \[ \left(\frac{u}{v}\right)' = \frac{u'v - uv'}{v^2}. \] "
        r"``Low d-high minus high d-low, over the square of what's below.'' The order of the numerator matters.")),
    Text(r"\textbf{How to work one.} Label the top $u$ and the bottom $v$, write $u'$ and $v'$, then assemble $\dfrac{u'v - uv'}{v^2}$. "
         r"To find the derivative at one point, you only need the four numbers $u(a)$, $v(a)$, $u'(a)$, $v'(a)$."),

    Section("Using it well"),
    VideoExample("A rational function", work="2.6cm"),
    VideoExample("With exponentials", work="2.2cm"),
    VideoExample("At a point, no formula needed", work="2.6cm"),
    VideoExample("Rewrite instead", work="2.2cm"),
    VideoExample("In context", work="2.8cm"),
    BigIdea(r"Low d-high minus high d-low, over low squared. Rewrite first when the bottom is a single power of $x$."),
    Check(r"Find \[ \frac{d}{dx}\left[\frac{x}{x+2}\right]. \]", expr("2/(x+2)**2"), r"\[ \frac{(x+2)(1) - x(1)}{(x+2)^2} = \frac{2}{(x+2)^2}. \]"),
]
same("ex2", D(sp.exp(x) / x), sp.exp(x) * (x - 1) / x**2)
same("check", D(x / (x + 2)), 2 / (x + 2)**2)

# ---------------------------------------------------------------- practice
P = [(r"y = \dfrac{3x - 1}{2x + 5}", (3 * x - 1) / (2 * x + 5)), (r"y = \dfrac{x^2}{x^2 + 1}", x**2 / (x**2 + 1)),
     (r"y = \dfrac{\sin x}{x}", sp.sin(x) / x), (r"y = \dfrac{\ln x}{x}", sp.log(x) / x),
     (r"y = \dfrac{e^x}{1 + e^x}", sp.exp(x) / (1 + sp.exp(x))), (r"y = \dfrac{x^4 - 3x^2}{x^2}", (x**4 - 3 * x**2) / x**2)]
SOL = [r"$\dfrac{(2x+5)(3) - (3x-1)(2)}{(2x+5)^2} = \dfrac{17}{(2x+5)^2}$.", r"$\dfrac{(x^2+1)(2x) - x^2(2x)}{(x^2+1)^2} = \dfrac{2x}{(x^2+1)^2}$.",
       r"$\dfrac{x\cos x - \sin x}{x^2}$.", r"$\dfrac{x\cdot\frac1x - \ln x}{x^2} = \dfrac{1 - \ln x}{x^2}$.",
       r"$\dfrac{(1+e^x)e^x - e^x e^x}{(1+e^x)^2} = \dfrac{e^x}{(1+e^x)^2}$.", r"Simplify first: $x^2 - 3$, derivative $2x$."]
PRACTICE = [Item(rf"Find $\dfrac{{dy}}{{dx}}$ for ${tex}$.", expr(str(D(e))), sol, work="2.2cm") for (tex, e), sol in zip(P, SOL)]
PRACTICE += [
    Item(r"$f(2) = 6$, $f'(2) = 1$, $g(2) = 3$, $g'(2) = -2$. Find the derivative of $\dfrac{f(x)}{g(x)}$ at $x = 2$.", num(sp.Rational(5, 3)),
         r"$\dfrac{3(1) - 6(-2)}{3^2} = \dfrac{15}{9} = \dfrac53$.", work="1.8cm"),
    Item(r"Find the equation for the line tangent to $y = \dfrac{x}{x - 1}$ at $x = 2$.", expr("-x+4"),
         r"$y' = \dfrac{-1}{(x-1)^2} = -1$ at $x=2$; point $(2, 2)$: $y = -x + 4$.", work="2.2cm"),
    Item(r"Where does $y = \dfrac{\ln x}{x}$ have a horizontal tangent line?", num(sp.E), r"$\dfrac{1 - \ln x}{x^2} = 0$ gives $x = e$.",
         work="1.8cm"),
    Item(r"Kai writes $\dfrac{d}{dx}\left[\dfrac{f}{g}\right] = \dfrac{fg' - gf'}{g^2}$. What is wrong?", selfcheck(r"\text{sign reversed}"),
         r"The numerator is reversed, so Kai's answer is the negative of the correct derivative. It should be $gf' - fg'$.", work="1.6cm"),
]
same("p7", sp.Rational(3 * 1 - 6 * (-2), 9), sp.Rational(5, 3))
same("p8", sp.expand(2 + D(x / (x - 1)).subs(x, 2) * (x - 2)), -x + 4)
same("p9", sp.solve(D(sp.log(x) / x), x), [sp.E])

# extra practice (round 1)
P2 = [(r"y = \dfrac{x + 4}{x - 2}", (x + 4) / (x - 2), r"$\dfrac{(x-2)(1) - (x+4)(1)}{(x-2)^2} = \dfrac{-6}{(x-2)^2}$."),
      (r"y = \dfrac{5}{x^2 + 3}", 5 / (x**2 + 3), r"$\dfrac{(x^2+3)(0) - 5(2x)}{(x^2+3)^2} = \dfrac{-10x}{(x^2+3)^2}$."),
      (r"y = \dfrac{\cos x}{x}", sp.cos(x) / x, r"$\dfrac{x(-\sin x) - \cos x}{x^2} = -\dfrac{x\sin x + \cos x}{x^2}$."),
      (r"y = \dfrac{x}{e^x}", x / sp.exp(x), r"$\dfrac{e^x - xe^x}{e^{2x}} = \dfrac{1 - x}{e^x}$."),
      (r"y = \tan x = \dfrac{\sin x}{\cos x}", sp.tan(x),
       r"$\dfrac{\cos x\cos x - \sin x(-\sin x)}{\cos^2 x} = \dfrac{1}{\cos^2 x} = \sec^2 x$.")]
for tex, e, sol in P2:
    PRACTICE.append(Item(rf"Find $\dfrac{{dy}}{{dx}}$ for ${tex}$.", expr(str(sp.simplify(D(e)))), sol, work="2.2cm"))
PRACTICE += [
    Item(r"$f(1) = 4$, $f'(1) = -2$, $g(1) = 2$, $g'(1) = 3$. Find the derivative of $\dfrac{f(x)}{g(x)}$ at $x = 1$.",
         num(-4), r"$\dfrac{g(1)f'(1) - f(1)g'(1)}{g(1)^2} = \dfrac{2(-2) - 4(3)}{4} = -4$.", work="1.8cm"),
    Item(r"Find the equation for the line tangent to $y = \dfrac{2x}{x + 1}$ at $x = 1$.", expr("x/2+1/2"),
         r"$y' = \dfrac{(x+1)(2) - 2x}{(x+1)^2} = \dfrac{2}{(x+1)^2}$, which is $\frac12$ at $x = 1$. Point $(1, 1)$: "
         r"$y = \frac12 x + \frac12$.", work="2.2cm"),
    Item(r"Where does $y = \dfrac{x^2}{x + 1}$ have horizontal tangent lines? Enter the nonzero $x$-value.", num(-2),
         r"$y' = \dfrac{(x+1)(2x) - x^2}{(x+1)^2} = \dfrac{x^2 + 2x}{(x+1)^2}$. The numerator $x(x + 2)$ is $0$ at $x = 0$ "
         r"and $x = -2$.", work="2.2cm"),
    Item(r"Find $\dfrac{dy}{dx}$ for $y = \dfrac{x^3 + x}{x}$ two ways: with the quotient rule, and by simplifying first. "
         r"Enter the result.", expr("2*x"),
         r"Simplifying: $y = x^2 + 1$ (for $x \ne 0$), so $y' = 2x$. The quotient rule gives "
         r"$\dfrac{x(3x^2 + 1) - (x^3 + x)}{x^2} = \dfrac{2x^3}{x^2} = 2x$, the same answer with more work.", work="2.4cm"),
    Item(r"The average cost per shirt of printing $n$ shirts is $A(n) = \dfrac{200 + 4n}{n}$ dollars. Find $A'(50)$ and "
         r"interpret it.", num(-sp.Rational(2, 25), display=r"-0.08\text{ dollars per shirt}"),
         r"$A'(n) = \dfrac{n(4) - (200 + 4n)}{n^2} = -\dfrac{200}{n^2}$, so $A'(50) = -0.08$. At $50$ shirts, the average "
         r"cost is falling by about $8$ cents per additional shirt.", work="2.4cm"),
]
same("x1 derivs", [sp.simplify(D(e) - want) for (_, e, _), want in zip(P2, [
    -6 / (x - 2)**2, -10 * x / (x**2 + 3)**2, -(x * sp.sin(x) + sp.cos(x)) / x**2, (1 - x) / sp.exp(x), 1 / sp.cos(x)**2])],
     [0, 0, 0, 0, 0])
same("x1 val", sp.Rational(2 * (-2) - 4 * 3, 4), -4)
same("x1 tan", sp.expand(1 + D(2 * x / (x + 1)).subs(x, 1) * (x - 1)), x / 2 + sp.Rational(1, 2))
same("x1 horiz", sorted(sp.solve(D(x**2 / (x + 1)), x)), [-2, 0])
same("x1 cost", D((200 + 4 * x) / x).subs(x, 50), -sp.Rational(2, 25))

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find $\dfrac{d}{dx}\left[\dfrac{x+1}{x-1}\right]$.", expr("-2/(x-1)**2"), r"$\dfrac{(x-1) - (x+1)}{(x-1)^2} = \dfrac{-2}{(x-1)^2}$.", work="2cm"),
        Item(r"Find $\dfrac{d}{dx}\left[\dfrac{2x}{x+3}\right]$.", expr("6/(x+3)**2"), r"$\dfrac{2(x+3) - 2x}{(x+3)^2} = \dfrac{6}{(x+3)^2}$.", work="2cm"),
        Item(r"Find $\dfrac{d}{dx}\left[\dfrac{x^2}{x+1}\right]$.", expr("(x**2+2*x)/(x+1)**2"),
             r"$\dfrac{2x(x+1) - x^2}{(x+1)^2} = \dfrac{x^2 + 2x}{(x+1)^2}$.", work="2cm"),
    ),
    Variants(
        Item(r"Find $\dfrac{d}{dx}\left[\dfrac{\cos x}{x}\right]$.", expr("(-x*sin(x) - cos(x))/x**2"), r"$\dfrac{-x\sin x - \cos x}{x^2}$.", work="2cm"),
        Item(r"Find $\dfrac{d}{dx}\left[\dfrac{e^x}{x}\right]$.", expr("(x*exp(x) - exp(x))/x**2"), r"$\dfrac{xe^x - e^x}{x^2}$.", work="2cm"),
        Item(r"Find $\dfrac{d}{dx}\left[\dfrac{\ln x}{x^2}\right]$.", expr("(1 - 2*log(x))/x**3"),
             r"$\dfrac{x^2\cdot\frac1x - 2x\ln x}{x^4} = \dfrac{1 - 2\ln x}{x^3}$.", work="2cm"),
    ),
    Variants(
        Item(r"$f(1) = 4$, $f'(1) = 2$, $g(1) = 2$, $g'(1) = 3$. Find $\left(\dfrac{f}{g}\right)'(1)$.", num(-2),
             r"$\dfrac{2(2) - 4(3)}{4} = -2$.", work="1.6cm"),
        Item(r"$f(0) = 3$, $f'(0) = -1$, $g(0) = 1$, $g'(0) = 2$. Find $\left(\dfrac{f}{g}\right)'(0)$.", num(-7),
             r"$\dfrac{1(-1) - 3(2)}{1} = -7$.", work="1.6cm"),
        Item(r"$g(2) = 4$ and $g'(2) = 1$. Find the derivative of $\dfrac{1}{g(x)}$ at $x = 2$.", num(sp.Rational(-1, 16)),
             r"$\dfrac{g(2)\cdot0 - 1\cdot g'(2)}{g(2)^2} = \dfrac{-1}{16}$.", work="1.6cm"),
    ),
    Variants(
        MCQ(r"Which is the quickest correct approach to $\dfrac{d}{dx}\left[\dfrac{6}{x^3}\right]$?",
            [r"The quotient rule", r"Rewrite as $6x^{-3}$ and use the power rule", r"Divide the derivatives: $\dfrac{0}{3x^2}$", r"The product rule"], "B",
            r"$6x^{-3}$ gives $-18x^{-4}$.", why_not={"C": "never divide derivatives"}),
        MCQ(r"Which is the quickest correct approach to $\dfrac{d}{dx}\left[\dfrac{x^3 - 4x}{x}\right]$?",
            [r"Simplify to $x^2 - 4$ first", r"The quotient rule is the only way", r"Divide the derivatives", r"The product rule"], "A",
            r"For $x \ne 0$, it's $x^2 - 4$, so the derivative is $2x$.", why_not={"C": "never divide derivatives"}),
        MCQ(r"Which is the correct quotient rule?",
            [r"$\left(\dfrac fg\right)' = \dfrac{f'}{g'}$", r"$\left(\dfrac fg\right)' = \dfrac{fg' - gf'}{g^2}$",
             r"$\left(\dfrac fg\right)' = \dfrac{gf' - fg'}{g^2}$", r"$\left(\dfrac fg\right)' = \dfrac{gf' + fg'}{g^2}$"], "C",
            r"Low d-high minus high d-low, over the square of what's below.", why_not={"B": "the order is reversed", "A": "never divide derivatives"}),
    ),
    Variants(
        MCQ(r"$\dfrac{d}{dx}\left[\dfrac{x}{e^x}\right] =$", [r"$\dfrac{1-x}{e^x}$", r"$\dfrac{x-1}{e^x}$", r"$\dfrac{1}{e^x}$", r"$1 - x$"], "A",
            r"$\dfrac{e^x - xe^x}{e^{2x}} = \dfrac{1-x}{e^x}$."),
        MCQ(r"$\dfrac{d}{dx}\left[\dfrac{\sin x}{\cos x}\right] =$", [r"$-1$", r"$\dfrac{1}{\cos^2x}$", r"$\dfrac{\cos x}{-\sin x}$", r"$\sin^2 x$"], "B",
            r"$\dfrac{\cos x\cos x + \sin x\sin x}{\cos^2 x} = \dfrac{1}{\cos^2 x}$.", why_not={"C": "divided the derivatives"}),
        MCQ(r"$\dfrac{d}{dx}\left[\dfrac{3}{x^2+1}\right] =$", [r"$\dfrac{3}{2x}$", r"$\dfrac{6x}{(x^2+1)^2}$", r"$-\dfrac{3}{(x^2+1)^2}$", r"$-\dfrac{6x}{(x^2+1)^2}$"], "D",
            r"$\dfrac{(x^2+1)\cdot 0 - 3\cdot 2x}{(x^2+1)^2}$.", why_not={"B": "lost the minus sign", "A": "divided the derivatives"}),
    ),
]
same("q versions", [D(2 * x / (x + 3)), D(x**2 / (x + 1)), D(sp.log(x) / x**2), sp.Rational(1 * -1 - 3 * 2, 1), sp.Rational(-1, 16)],
     [6 / (x + 3)**2, (x**2 + 2 * x) / (x + 1)**2, (1 - 2 * sp.log(x)) / x**3, -7, sp.Rational(-1, 16)])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"If $f(x) = \dfrac{x^2}{x + 1}$, then $f'(1) =$", [r"$\dfrac12$", r"$1$", r"$\dfrac34$", r"$\dfrac14$"], "C",
        r"$\dfrac{(x+1)2x - x^2}{(x+1)^2} = \dfrac{4 - 1}{4} = \dfrac34$."),
    MCQ(r"Using the table, find the derivative of $\dfrac{g(x)}{f(x)}$ at $x = 0$."
        r"\par\centerline{\begin{tabular}{c|cccc} $x$ & $f(x)$ & $f'(x)$ & $g(x)$ & $g'(x)$ \\ \hline 0 & 2 & $-1$ & 5 & 3\end{tabular}}",
        [r"$\dfrac{11}{4}$", r"$\dfrac{1}{4}$", r"$-\dfrac{11}{4}$", r"$-3$"], "A",
        r"$\dfrac{f g' - g f'}{f^2} = \dfrac{2(3) - 5(-1)}{4} = \dfrac{11}{4}$.", why_not={"C": "reversed the numerator"}),
    MCQ(r"The slope of the tangent line to $y = \dfrac{2x}{x^2 + 1}$ at $x = 0$ is", [r"$0$", r"$1$", r"$-2$", r"$2$"], "D",
        r"$\dfrac{(x^2+1)2 - 2x(2x)}{(x^2+1)^2} = 2$ at $x = 0$."),
    MCQ(r"Where does $f(x) = \dfrac{x}{x^2 + 4}$ have horizontal tangent lines?", [r"$x = \pm 2$", r"$x = 0$", r"$x = \pm 4$", r"nowhere"], "A",
        r"$\dfrac{4 - x^2}{(x^2+4)^2} = 0$ gives $x = \pm2$."),
]
same("m1", sp.diff(x**2 / (x + 1), x).subs(x, 1), sp.Rational(3, 4))
same("m2", sp.Rational(2 * 3 - 5 * (-1), 4), sp.Rational(11, 4))
same("m4", sorted(sp.solve(sp.diff(x / (x**2 + 4), x), x)), [-2, 2])

FRQS = [
    FRQ("Concentration of a medicine", (
        r"The concentration of a medicine in a patient's bloodstream $t$ hours after an injection is modeled by "
        r"$C(t) = \dfrac{5t}{t^2 + 4}$, where $C(t)$ is measured in milligrams per liter, for $t \ge 0$."), [
        Part("a", r"Find $C'(1)$. Using correct units, interpret the meaning of $C'(1)$ in the context of the problem.",
             num(sp.Rational(3, 5), display=r"\tfrac35\ \text{milligrams per liter per hour}"),
             r"$C'(t) = \dfrac{5(t^2+4) - 5t(2t)}{(t^2+4)^2} = \dfrac{20 - 5t^2}{(t^2+4)^2}$, so $C'(1) = \dfrac{15}{25} = \dfrac35$. "
             r"At time $t = 1$ hour, the concentration is increasing at a rate of $0.6$ milligrams per liter per hour.",
             [(1, "$C'(t)$ by the quotient rule"), (1, "$C'(1) = \\frac35$"), (1, "interpretation with units")], work="3.2cm"),
        Part("b", r"Is the concentration of the medicine increasing or decreasing at time $t = 3$? Give a reason for your answer.",
             selfcheck(r"\text{Decreasing}"),
             r"$C'(3) = \dfrac{20 - 45}{13^2} = -\dfrac{25}{169} < 0$, so the concentration is decreasing at $t = 3$.",
             [(1, "decreasing, because $C'(3) < 0$")], work="2cm"),
        Part("c", r"Write an equation for the line tangent to the graph of $C$ at $t = 1$.", expr("1 + 3*(t - 1)/5", var="t"),
             r"$C(1) = \dfrac{5}{5} = 1$ and $C'(1) = \dfrac35$, so the tangent line is $y = 1 + \dfrac35(t - 1)$.",
             [(1, "tangent line equation")], work="2cm"),
    ], frq_type="Rate in context"),
]
t = sp.symbols("t")
C9 = 5 * t / (t**2 + 4)
same("frq", [sp.simplify(sp.diff(C9, t) - (20 - 5 * t**2) / (t**2 + 4)**2), sp.diff(C9, t).subs(t, 1)], [0, sp.Rational(3, 5)])
same("frq b", sp.diff(C9, t).subs(t, 3), sp.Rational(-25, 169))
same("frq c", C9.subs(t, 1), 1)

TOPIC = Topic(
    number="2.9", title="The Quotient Rule",
    unit="Unit 2: Differentiation", ced=["FUN-3.B", "FUN-3.B.2"],
    goals=r"Differentiate quotients with the quotient rule, and recognize when rewriting is faster.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
