"""Topic 3.4: Differentiating inverse trigonometric functions.

CED: FUN-3.E.2 (derivatives of inverse trig functions via implicit differentiation / the inverse rule). arcsin and arctan are derived
with a reference triangle, the picture used in the video; the other four are listed.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Example, Figure, Formula, Item, Part, Section, Text, Topic, Variants, Video, expr,
                     num, same, selfcheck)

x, t = sp.symbols("x t")
pi = sp.pi


def D(e):
    return sp.simplify(sp.diff(e, x))


same("asin", sp.simplify(D(sp.asin(x)) - 1 / sp.sqrt(1 - x**2)), 0)
same("atan", sp.simplify(D(sp.atan(x)) - 1 / (1 + x**2)), 0)
same("acos", sp.simplify(D(sp.acos(x)) + 1 / sp.sqrt(1 - x**2)), 0)

FIG_T = Figure(name="t3_4_triangle", caption=r"If $\sin y = x$, label the triangle and read off $\cos y = \sqrt{1 - x^2}$.",
               tikz=(r"\begin{tikzpicture}[scale=1.3]"
                     r"\draw[line width=0.9pt] (0,0) -- (3,0) -- (3,1.8) -- cycle; \draw (2.8,0) -- (2.8,0.2) -- (3,0.2);"
                     r"\node[below] at (1.5,0) {$\sqrt{1 - x^2}$}; \node[right] at (3,0.9) {$x$}; \node[above left] at (1.5,0.95) {$1$};"
                     r"\draw (0.6,0) arc (0:31:0.6); \node at (0.85,0.2) {$y$};"
                     r"\end{tikzpicture}"))

NOTES = [
    Video("s3_4.py::Lesson", "Derivatives of inverse trig functions", 5),

    Section("Arcsine, by implicit differentiation"),
    Text(r"Let $y = \arcsin x$, so $\sin y = x$ with \[ -\frac\pi2 \le y \le \frac\pi2. \] Differentiate implicitly: "
         r"$\displaystyle \cos y\,\dfrac{dy}{dx} = 1$, so $\displaystyle \frac{dy}{dx} = \mblank{\frac{1}{\cos y}}$."),
    FIG_T,
    Text(r"To write $\cos y$ in terms of $x$, draw a right triangle with angle $y$, opposite side $x$ and hypotenuse $1$. The Pythagorean "
         r"theorem gives the adjacent side, \blank{$\sqrt{1 - x^2}$}, so $\cos y = \sqrt{1 - x^2}$ and "
         r"\[ \frac{d}{dx}\arcsin x = \mblank{\frac{1}{\sqrt{1 - x^2}}} \]."),

    Section("Arctangent"),
    Text(r"Let $y = \arctan x$, so $\tan y = x$. Then \[ \sec^2 y\,\frac{dy}{dx} = 1. \] Since $\sec^2 y = 1 + \tan^2 y = 1 + x^2$, "
         r"$\displaystyle \frac{d}{dx}\arctan x = \mblank{\frac{1}{1 + x^2}}$."),
    Formula("Inverse trig derivatives", (
        r"\[ \frac{d}{dx}\arcsin x = \frac{1}{\sqrt{1 - x^2}} \qquad \frac{d}{dx}\arccos x = \mblank{-\frac{1}{\sqrt{1 - x^2}}} \qquad "
        r"\frac{d}{dx}\arctan x = \frac{1}{1 + x^2} \]"
        r"\[ \frac{d}{dx}\operatorname{arccot} x = -\frac{1}{1 + x^2} \qquad \frac{d}{dx}\operatorname{arcsec} x = \frac{1}{|x|\sqrt{x^2 - 1}} "
        r"\qquad \frac{d}{dx}\operatorname{arccsc} x = -\frac{1}{|x|\sqrt{x^2 - 1}} \]"
        r"Each ``co'' version is the \blank{negative} of its partner. With the chain rule: "
        r"\[ \frac{d}{dx}\arctan\big(u(x)\big) = \frac{u'}{1 + u^2}. \]")),

    Section("Using them"),
    VideoExample('Arcsine with the chain rule', work="2.2cm"),
    BigIdea(r"Differentiate $\sin y = x$ (or $\tan y = x$) implicitly, then use a triangle or an identity to write the answer in $x$."),
    Check(r"Find $\dfrac{d}{dx}\arctan x$ at $x = 2$.", num(sp.Rational(1, 5)), r"\[ \frac{1}{1 + 4} = \frac15. \]"),
]
same("ex slope", D(sp.asin(x)).subs(x, sp.Rational(1, 2)), 2 / sp.sqrt(3))
same("ex chain", [D(sp.atan(3 * x)), sp.simplify(D(sp.asin(x**2)) - 2 * x / sp.sqrt(1 - x**4))], [3 / (1 + 9 * x**2), 0])

# ---------------------------------------------------------------- practice
P = [(r"y = \arctan(5x)", sp.atan(5 * x), r"$\dfrac{5}{1 + 25x^2}$."),
     (r"y = \arcsin(2x)", sp.asin(2 * x), r"$\dfrac{2}{\sqrt{1 - 4x^2}}$."),
     (r"y = \arccos(x^3)", sp.acos(x**3), r"$-\dfrac{3x^2}{\sqrt{1 - x^6}}$."),
     (r"y = \arctan\left(\sqrt x\right)", sp.atan(sp.sqrt(x)), r"$\dfrac{1}{1 + x}\cdot\dfrac{1}{2\sqrt x}$."),
     (r"y = x\arctan x", x * sp.atan(x), r"$\arctan x + \dfrac{x}{1 + x^2}$."),
     (r"y = \arcsin\left(\dfrac x3\right)", sp.asin(x / 3), r"$\dfrac{1/3}{\sqrt{1 - x^2/9}} = \dfrac{1}{\sqrt{9 - x^2}}$."),
     (r"y = \arctan\left(e^x\right)", sp.atan(sp.exp(x)), r"$\dfrac{e^x}{1 + e^{2x}}$."),
     (r"y = \left(\arcsin x\right)^2", sp.asin(x)**2, r"$\dfrac{2\arcsin x}{\sqrt{1 - x^2}}$.")]
PRACTICE = [Item(rf"Find $\dfrac{{dy}}{{dx}}$ for ${tex}$.", expr(str(D(e))), sol, work="1.8cm") for tex, e, sol in P]
PRACTICE += [
    Item(r"Find the slope of $y = \arctan x$ at $x = \sqrt3$.", num(sp.Rational(1, 4)), r"$\dfrac{1}{1 + 3} = \dfrac14$.", work="1.2cm"),
    Item(r"Find the slope of $y = \arcsin x$ at $x = 0$.", num(1), r"$\dfrac{1}{\sqrt{1 - 0}} = 1$.", work="1.2cm"),
    Item(r"Find the slope of $y = \arccos x$ at $x = \frac{\sqrt3}2$.", num(-2), r"$-\dfrac{1}{\sqrt{1 - \frac34}} = -2$.", work="1.4cm"),
    Item(r"Find the equation for the line tangent to $y = \arcsin x$ at $x = 0$.", expr("x"), r"Point $(0, 0)$, slope $1$: $y = x$.", work="1.6cm"),
    Item(r"Find the equation for the line tangent to $y = 2\arctan x$ at $x = 1$.", expr("x + pi/2 - 1"),
         r"Point $\left(1, \frac\pi2\right)$, slope $\dfrac{2}{2} = 1$: $y = x - 1 + \frac\pi2$.", work="1.8cm"),
    Item(r"Where is the slope of $y = \arctan x$ largest? Enter the $x$-value.", num(0),
         r"$\dfrac{1}{1 + x^2}$ is largest when $x^2$ is smallest, at $x = 0$.", work="1.4cm"),
    Item(r"Use the triangle method to show that $\dfrac{d}{dx}\arccos x = -\dfrac{1}{\sqrt{1 - x^2}}$.", selfcheck(r"-\tfrac{1}{\sqrt{1-x^2}}"),
         r"$\cos y = x$ gives $-\sin y\,y' = 1$, so $y' = -\dfrac{1}{\sin y}$. With adjacent $x$ and hypotenuse $1$, the opposite side is "
         r"$\sqrt{1 - x^2}$, so $\sin y = \sqrt{1 - x^2}$.", work="2.4cm"),
    Item(r"Explain why $\dfrac{d}{dx}\left[\arcsin x + \arccos x\right] = 0$, and what that says about $\arcsin x + \arccos x$.",
         selfcheck(r"\text{constant } \tfrac\pi2"),
         r"The two derivatives are negatives, so the sum's derivative is $0$ and the sum is constant: it equals $\frac\pi2$ (check at $x = 0$).",
         work="1.8cm"),
    Item(r"Why is $\dfrac{1}{\sqrt{1 - x^2}}$ undefined at $x = \pm1$? Describe the graph of $\arcsin x$ there.", selfcheck(r"\text{vertical tangents}"),
         r"The denominator is $0$. The graph of $\arcsin x$ has vertical tangent lines at its endpoints.", work="1.6cm"),
    Item(r"A camera 50 meters from a road watches a car. The camera angle is $\theta = \arctan\left(\frac{x}{50}\right)$, where $x$ is the car's "
         r"distance down the road in meters. Find $\dfrac{d\theta}{dx}$ when $x = 50$, in radians per meter.", num(sp.Rational(1, 100)),
         r"$\dfrac{1/50}{1 + (x/50)^2} = \dfrac{1/50}{2} = \dfrac{1}{100}$ at $x = 50$.", work="2cm"),
    Item(r"Find $\dfrac{d}{dx}\arctan\left(\dfrac1x\right)$ and simplify. What do you notice?", expr("-1/(x**2+1)"),
         r"$\dfrac{1}{1 + 1/x^2}\cdot\left(-\dfrac{1}{x^2}\right) = -\dfrac{1}{x^2 + 1}$: the negative of the derivative of $\arctan x$.", work="2cm"),
    Item(r"$f(x) = \arctan x$ and $g(x) = x^3$. Find the derivative of $f\big(g(x)\big)$ at $x = 1$.", num(sp.Rational(3, 2)),
         r"$f'\big(g(1)\big)\,g'(1) = \dfrac{1}{1 + 1}\cdot 3 = \dfrac32$.", work="1.6cm"),
]
same("p", [D(sp.atan(x)).subs(x, sp.sqrt(3)), D(sp.acos(x)).subs(x, sp.sqrt(3) / 2), D(sp.atan(x / 50)).subs(x, 50),
           D(sp.atan(1 / x)), D(sp.atan(x**3)).subs(x, 1), sp.expand(pi / 2 + D(2 * sp.atan(x)).subs(x, 1) * (x - 1))],
     [sp.Rational(1, 4), -2, sp.Rational(1, 100), -1 / (x**2 + 1), sp.Rational(3, 2), x + pi / 2 - 1])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find $\dfrac{d}{dx}\arctan(2x)$.", expr("2/(1+4*x**2)"), r"$\dfrac{2}{1 + 4x^2}$.", work="1.4cm"),
        Item(r"Find $\dfrac{d}{dx}\arcsin(4x)$.", expr("4/sqrt(1-16*x**2)"), r"$\dfrac{4}{\sqrt{1 - 16x^2}}$.", work="1.4cm"),
        Item(r"Find $\dfrac{d}{dx}\arctan\left(x^2\right)$.", expr("2*x/(1+x**4)"), r"$\dfrac{2x}{1 + x^4}$.", work="1.4cm"),
    ),
    Variants(
        Item(r"Find the slope of $y = \arcsin x$ at $x = \frac{\sqrt2}{2}$.", num(sp.sqrt(2)), r"$\dfrac{1}{\sqrt{1 - \frac12}} = \sqrt2$.", work="1.4cm"),
        Item(r"Find the slope of $y = \arctan x$ at $x = -1$.", num(sp.Rational(1, 2)), r"$\dfrac{1}{1 + 1} = \dfrac12$.", work="1.4cm"),
        Item(r"Find the slope of $y = \arccos x$ at $x = 0$.", num(-1), r"$-\dfrac{1}{\sqrt{1 - 0}} = -1$.", work="1.4cm"),
    ),
    Variants(
        Item(r"Find $\dfrac{d}{dx}\left[x\arcsin x\right]$.", expr("asin(x) + x/sqrt(1-x**2)"), r"$\arcsin x + \dfrac{x}{\sqrt{1 - x^2}}$.", work="1.6cm"),
        Item(r"Find $\dfrac{d}{dx}\left[x^2\arctan x\right]$.", expr("2*x*atan(x) + x**2/(1+x**2)"), r"$2x\arctan x + \dfrac{x^2}{1 + x^2}$.", work="1.6cm"),
        Item(r"Find $\dfrac{d}{dx}\left[e^x\arctan x\right]$.", expr("exp(x)*atan(x) + exp(x)/(1+x**2)"), r"$e^x\arctan x + \dfrac{e^x}{1 + x^2}$.", work="1.6cm"),
    ),
    Variants(
        MCQ(r"$\dfrac{d}{dx}\arccos x =$", [r"$\dfrac{1}{\sqrt{1-x^2}}$", r"$-\dfrac{1}{\sqrt{1-x^2}}$", r"$-\dfrac{1}{1+x^2}$", r"$-\sin x$"], "B",
            r"The negative of the arcsine derivative.", why_not={"A": "that's arcsine", "D": "that's $\\frac{d}{dx}\\cos x$"}),
        MCQ(r"$\dfrac{d}{dx}\arctan x =$", [r"$\sec^2 x$", r"$\dfrac{1}{\sqrt{1-x^2}}$", r"$\dfrac{1}{1+x^2}$", r"$\dfrac{1}{\tan x}$"], "C",
            r"From $\tan y = x$ and $\sec^2 y = 1 + x^2$.", why_not={"A": "that's $\\frac{d}{dx}\\tan x$", "D": "arctan is not $\\frac{1}{\\tan}$"}),
        MCQ(r"Which is the derivative of $\arcsin x$?", [r"$\dfrac{1}{\sqrt{1-x^2}}$", r"$\cos x$", r"$\dfrac{1}{\cos x}$", r"$\dfrac{1}{1+x^2}$"], "A",
            r"From $\sin y = x$ and the reference triangle.", why_not={"C": "that's $\\frac{1}{\\cos y}$ before rewriting in $x$"}),
    ),
    Variants(
        MCQ(r"The line tangent to $y = \arctan x$ at $x = 0$ is", [r"$y = 0$", r"$y = \frac\pi4 x$", r"$y = x + 1$", r"$y = x$"], "D",
            r"Point $(0, 0)$, slope $1$."),
        MCQ(r"If $f(x) = \arcsin(3x)$, then $f'(0) =$", [r"$1$", r"$3$", r"$\dfrac13$", r"$0$"], "B", r"$\dfrac{3}{\sqrt{1 - 9x^2}} = 3$ at $0$.",
            why_not={"A": "forgot the chain rule"}),
        MCQ(r"If $f(x) = \arctan(x - 1)$, then $f'(1) =$", [r"$\dfrac12$", r"$0$", r"$1$", r"$\dfrac\pi4$"], "C", r"$\dfrac{1}{1 + (x-1)^2} = 1$ at $x = 1$.",
            why_not={"A": "evaluated $\\frac{1}{1+x^2}$ at $1$", "B": "that's $f(1)$"}),
    ),
]
same("q", [D(sp.asin(x)).subs(x, sp.sqrt(2) / 2), D(sp.atan(x)).subs(x, -1), D(sp.acos(x)).subs(x, 0), D(sp.asin(3 * x)).subs(x, 0),
           D(sp.atan(x - 1)).subs(x, 1)], [sp.sqrt(2), sp.Rational(1, 2), -1, 3, 1])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"If $f(x) = \arctan\left(x^2\right)$, then $f'(1) =$", [r"$1$", r"$\dfrac12$", r"$2$", r"$\dfrac\pi4$"], "A",
        r"$\dfrac{2x}{1 + x^4} = \dfrac22 = 1$.", why_not={"B": "forgot the chain rule", "D": "that's $f(1)$"}),
    MCQ(r"$\dfrac{d}{dx}\arcsin\left(\dfrac{x}{2}\right) =$", [r"$\dfrac{1}{2\sqrt{1 - x^2}}$", r"$\dfrac{2}{\sqrt{4 - x^2}}$",
        r"$\dfrac{1}{\sqrt{4 - x^2}}$", r"$\dfrac{1}{\sqrt{1 - x^2/4}}$"], "C",
        r"$\dfrac{1/2}{\sqrt{1 - x^2/4}} = \dfrac{1/2}{\frac12\sqrt{4 - x^2}} = \dfrac{1}{\sqrt{4 - x^2}}$.", why_not={"D": "forgot the chain rule"}),
    MCQ(r"$g$ is the inverse of $f(x) = \tan x$ on $\left(-\frac\pi2, \frac\pi2\right)$. What is $g'(1)$?", [r"$2$", r"$\sec^2 1$", r"$\dfrac\pi4$", r"$\dfrac12$"], "D",
        r"$g = \arctan$, and $\dfrac{1}{1 + 1} = \dfrac12$. (Or: $f\left(\frac\pi4\right) = 1$ and $f'\left(\frac\pi4\right) = 2$.)", why_not={"A": "forgot the reciprocal"}),
    MCQ(r"The slope of the curve $y = \arcsin x$ is $2$ at which $x > 0$?", [r"$\dfrac12$", r"$\dfrac{\sqrt3}{2}$", r"$\dfrac{\sqrt2}{2}$", r"$\dfrac14$"], "B",
        r"$\dfrac{1}{\sqrt{1 - x^2}} = 2$ gives $1 - x^2 = \frac14$, so $x = \frac{\sqrt3}{2}$."),
]
same("m", [D(sp.atan(x**2)).subs(x, 1), sp.simplify(D(sp.asin(x / 2)) - 1 / sp.sqrt(4 - x**2)), D(sp.atan(x)).subs(x, 1),
           [r for r in sp.solve(sp.Eq(1 / sp.sqrt(1 - x**2), 2), x) if r > 0][0]], [1, 0, sp.Rational(1, 2), sp.sqrt(3) / 2])

FRQS = [
    FRQ("A lighthouse beam", (
        r"A lighthouse stands 2 kilometers from a straight shoreline. Its beam lights a spot on the shore $x$ kilometers from the point "
        r"nearest the lighthouse, and the beam's angle is $\theta(x) = \arctan\left(\dfrac{x}{2}\right)$ radians."), [
        Part("a", r"Find $\theta'(x)$.", expr("2/(4 + x**2)"), r"$\dfrac{1/2}{1 + x^2/4} = \dfrac{2}{4 + x^2}$.", [(1, "chain rule"), (1, "simplified")],
             work="2cm"),
        Part("b", r"Find $\theta'(2)$ and interpret it with units.", num(sp.Rational(1, 4)),
             r"$\dfrac{2}{8} = \dfrac14$: when the spot is 2 km down the shore, the angle grows by about $\frac14$ radian per kilometer the spot moves.",
             [(1, "value"), (1, "units and meaning")], work="2cm"),
        Part("c", r"Is $\theta'(x)$ larger when the spot is near the lighthouse or far away? Explain using the formula.", selfcheck(r"\text{near}"),
             r"$\dfrac{2}{4 + x^2}$ shrinks as $x$ grows. Far down the shore, moving the spot changes the angle very little.",
             [(1, "near, with reason from the formula")], work="1.8cm"),
    ], frq_type="Rates in context"),
]
same("frq", [D(sp.atan(x / 2)), D(sp.atan(x / 2)).subs(x, 2)], [2 / (4 + x**2), sp.Rational(1, 4)])

TOPIC = Topic(
    number="3.4", title="Differentiating Inverse Trigonometric Functions",
    unit="Unit 3: Differentiation: Composite, Implicit, and Inverse Functions", ced=["FUN-3.E", "FUN-3.E.2"],
    goals=r"Derive and use the derivatives of $\arcsin x$, $\arccos x$ and $\arctan x$, alone and with the chain rule.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
