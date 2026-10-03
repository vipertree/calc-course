"""Topic 3.4: Differentiating inverse trigonometric functions.

CED: FUN-3.E.2 (derivatives of inverse trig functions via implicit differentiation / the inverse rule). arcsin and arctan are derived
with a reference triangle, the picture used in the video; the other four are listed.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Example, Figure, Formula, Item, Part, Section, Table, Text, Topic, Variants, Video, expr,
                     close, num, same, selfcheck)

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

def _circle(dx, arc, labels, holes=(), caption=""):
    out = (rf"\begin{{scope}}[shift={{({dx},0)}}]\draw[gray] (-1.35,0) -- (1.35,0); \draw[gray] (0,-1.35) -- (0,1.35); \draw (0,0) circle (1);"
           rf"\draw[line width=2.4pt] {arc};")
    out += "".join(rf"\draw[line width=1pt, fill=white] {h} circle (0.07);" for h in holes)
    out += "".join(rf"\node[{pos}] at {at} {{{t}}};" for pos, at, t in labels)
    return out + rf"\node at (0,-2.05) {{\small {caption}}};\end{{scope}}"


FIG_C = Figure(name="t3_4_circles", caption=r"The piece of the unit circle each inverse function answers from.",
               tikz=(r"\begin{tikzpicture}[scale=1.1]"
                     + _circle(0, r"(0,-1) arc (-90:90:1)", [("above right", "(0,1)", r"$\frac\pi2$"), ("below right", "(0,-1)", r"$-\frac\pi2$")],
                               caption=r"$\arcsin x$: right half")
                     + _circle(4.4, r"(1,0) arc (0:180:1)", [("above right", "(1,0)", r"$0$"), ("above left", "(-1,0)", r"$\pi$")],
                               caption=r"$\arccos x$: top half")
                     + _circle(8.8, r"(0,-1) arc (-90:90:1)", [("above right", "(0,1)", r"$\frac\pi2$"), ("below right", "(0,-1)", r"$-\frac\pi2$")],
                               holes=("(0,1)", "(0,-1)"), caption=r"$\arctan x$: right half, no ends")
                     + r"\end{tikzpicture}"))

NOTES = [
    Video("s3_4.py::Lesson", "Derivatives of inverse trig functions", 10),

    Section("The inverse trig functions"),
    Text(r"An inverse trig function takes a number and gives back an angle: $\arcsin x$ is the angle whose sine is $x$. "
         r"On the unit circle, sine is the height of the point at that angle, cosine is its left-right position, and tangent is the "
         r"slope of the line from the center to the point."),
    Text(r"A trig function is not one-to-one: $\sin\frac\pi6$ and $\sin\frac{5\pi}6$ are both $\frac12$. To undo it, we keep one piece "
         r"of the circle that gives each output exactly once. Arcsine uses the \blank{right} half, from $-\frac\pi2$ to $\frac\pi2$. "
         r"Arccosine uses the \blank{top} half, from $0$ to $\pi$. Arctangent uses the right half without its two ends, since a "
         r"vertical line has no slope."),
    FIG_C,
    Table(r"$\arcsin x$ & $-1 \le x \le 1$ & $\left[-\frac\pi2, \frac\pi2\right]$ & right half \\ "
          r"$\arccos x$ & $-1 \le x \le 1$ & $\mblank{[0, \pi]}$ & top half \\ "
          r"$\arctan x$ & \blank{every real $x$} & $\left(-\frac\pi2, \frac\pi2\right)$ & right half, no ends \\ "
          r"$\operatorname{arcsec} x$ & $|x| \ge 1$ & $[0, \pi]$, not $\frac\pi2$ & top half, no top",
          "llll", header=r"function & inputs (domain) & outputs (range) & piece of the circle"),
    Text(r"Secant is $\frac{1}{\cos x}$, so $\operatorname{arcsec} x = \arccos\frac1x$. Arccosecant and arccotangent are built the same "
         r"way and rarely come up."),
    Text(r"To evaluate one, find the point on the allowed piece of the circle. "
         r"$\arcsin\frac12 = \mblank{\frac{\pi}{6}}$, \quad $\arccos\left(-\frac{\sqrt2}{2}\right) = \mblank{\frac{3\pi}{4}}$, \quad "
         r"$\arctan(-1) = \mblank{-\frac{\pi}{4}}$, \quad $\arcsin(-1) = \mblank{-\frac{\pi}{2}}$. "
         r"The answer must be in the range: $\frac{3\pi}{4}$ also has tangent $-1$, but it is not on the right half."),
    Check(r"Find $\arccos(-1)$.", num(pi), r"The point $(-1, 0)$ is at angle $\pi$, on the top half."),
    Check(r"Find $\arcsin\left(-\frac{\sqrt3}{2}\right)$.", num(-pi / 3), r"On the right half, height $-\frac{\sqrt3}2$ is at $-\frac\pi3$."),
    Check(r"Find $\arctan\sqrt3$.", num(pi / 3), r"Slope $\sqrt3$ on the right half is at $\frac\pi3$."),

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

    Section("Arcsecant"),
    Text(r"Let $y = \operatorname{arcsec} x$, so $\sec y = x$ with $0 \le y \le \pi$, $y \ne \frac\pi2$. Differentiate: "
         r"$\sec y\tan y\,\dfrac{dy}{dx} = 1$, so $\dfrac{dy}{dx} = \dfrac{1}{x\tan y}$. Since $\tan^2 y = \sec^2 y - 1 = x^2 - 1$, "
         r"$\tan y = \pm\sqrt{x^2 - 1}$. On this range $\tan y$ has the same sign as $x$ (both positive below $\frac\pi2$, both negative "
         r"above it), so $x\tan y = |x|\sqrt{x^2 - 1}$ and \[ \frac{d}{dx}\operatorname{arcsec} x = \frac{1}{|x|\sqrt{x^2 - 1}}. \]"),

    Section("All six"),
    Formula("Inverse trig derivatives", (
        r"\[ \frac{d}{dx}\arcsin x = \frac{1}{\sqrt{1 - x^2}} \qquad \frac{d}{dx}\operatorname{arcsec} x = \frac{1}{|x|\sqrt{x^2 - 1}} "
        r"\qquad \frac{d}{dx}\arctan x = \frac{1}{1 + x^2} \]"
        r"\[ \frac{d}{dx}\arccos x = \mblank{-\frac{1}{\sqrt{1 - x^2}}} \qquad \frac{d}{dx}\operatorname{arccsc} x = -\frac{1}{|x|\sqrt{x^2 - 1}} "
        r"\qquad \frac{d}{dx}\operatorname{arccot} x = -\frac{1}{1 + x^2} \]"
        r"Each ``co'' version is the \blank{negative} of its partner. With the chain rule: "
        r"\[ \frac{d}{dx}\arctan\big(u(x)\big) = \frac{u'}{1 + u^2}. \]")),
    Text(r"Don't worry too much about the proofs. You do need to memorize these six. Two tips: the minus signs belong to the co-functions, "
         r"every time. And \textbf{S} for subtraction: the \textbf{s}ine and \textbf{s}ecant derivatives have a subtraction under the "
         r"square root ($1 - x^2$ and $x^2 - 1$), while arctangent has an \blank{addition}, $1 + x^2$, and no square root."),

    Section("Using them"),
    VideoExample('Arcsine with the chain rule', work="2.2cm"),

    Section("The absolute value in arcsecant"),
    VideoExample('Arcsecant of x squared', work="2.2cm"),
    VideoExample('Arcsecant of x cubed', work="2.2cm"),
    Text(r"An even power of $x$ is never negative, so its absolute value is itself and the absolute value can be dropped. "
         r"An odd power keeps the sign of $x$, so an absolute value \blank{stays} on the $x$."),
    BigIdea(r"Differentiate $\sin y = x$ (or $\tan y = x$) implicitly, then use a triangle or an identity to write the answer in $x$."),
    Check(r"Find $\dfrac{d}{dx}\arctan x$ at $x = 2$.", num(sp.Rational(1, 5)), r"\[ \frac{1}{1 + 4} = \frac15. \]"),
]
same("values", [sp.asin(sp.Rational(1, 2)), sp.acos(-sp.sqrt(2) / 2), sp.atan(-1), sp.asin(-1), sp.acos(-1), sp.asin(-sp.sqrt(3) / 2),
                sp.atan(sp.sqrt(3)), sp.asec(2)], [pi / 6, 3 * pi / 4, -pi / 4, -pi / 2, pi, -pi / 3, pi / 3, pi / 3])
same("asec", sp.simplify(D(sp.asec(x)).subs(x, 2) - 1 / (2 * sp.sqrt(3))), 0)
same("asec neg", sp.simplify(D(sp.asec(x)).subs(x, -2) - 1 / (2 * sp.sqrt(3))), 0)
_p = sp.Symbol("p", positive=True)


def both_sides(f, g):
    """f == g for x > 1 and for x < -1 (the absolute value makes the two sides differ)."""
    return [sp.simplify((f - g).subs(x, 1 + _p)), sp.simplify((f - g).subs(x, -1 - _p))]


same("asec x^2", both_sides(D(sp.asec(x**2)), 2 / (x * sp.sqrt(x**4 - 1))), [0, 0])
same("asec x^2 rule", both_sides(2 * x / (sp.Abs(x**2) * sp.sqrt(x**4 - 1)), 2 / (x * sp.sqrt(x**4 - 1))), [0, 0])
same("asec x^3", both_sides(D(sp.asec(x**3)), 3 / (sp.Abs(x) * sp.sqrt(x**6 - 1))), [0, 0])
same("asec x^3 rule", both_sides(3 * x**2 / (sp.Abs(x**3) * sp.sqrt(x**6 - 1)), 3 / (sp.Abs(x) * sp.sqrt(x**6 - 1))), [0, 0])
same("asec x^3 at -2", [D(sp.asec(x**3)).subs(x, -2), (3 / (x * sp.sqrt(x**6 - 1))).subs(x, -2)], [3 / (2 * sp.sqrt(63)), -3 / (2 * sp.sqrt(63))])  # dropping |x| flips the sign
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
EV = [(r"\arcsin\frac{\sqrt3}{2}", sp.asin(sp.sqrt(3) / 2), pi / 3, r"On the right half, height $\frac{\sqrt3}2$ is at $\frac\pi3$."),
      (r"\arccos\left(-\frac12\right)", sp.acos(-sp.Rational(1, 2)), 2 * pi / 3, r"On the top half, left-right position $-\frac12$ is at $\frac{2\pi}3$."),
      (r"\arctan\left(-\sqrt3\right)", sp.atan(-sp.sqrt(3)), -pi / 3, r"On the right half, slope $-\sqrt3$ is at $-\frac\pi3$."),
      (r"\arccos 0", sp.acos(0), pi / 2, r"The top of the circle, $\frac\pi2$."),
      (r"\arcsin\left(-\frac{\sqrt2}{2}\right)", sp.asin(-sp.sqrt(2) / 2), -pi / 4, r"On the right half, height $-\frac{\sqrt2}2$ is at $-\frac\pi4$."),
      (r"\operatorname{arcsec} 2", sp.asec(2), pi / 3, r"$\arccos\frac12 = \frac\pi3$."),
      (r"\arccos\left(\cos\frac{5\pi}{3}\right)", sp.acos(sp.cos(5 * pi / 3)), pi / 3,
       r"$\cos\frac{5\pi}3 = \frac12$, and the angle on the top half with cosine $\frac12$ is $\frac\pi3$, not $\frac{5\pi}3$."),
      (r"\arcsin\left(\sin\frac{3\pi}{4}\right)", sp.asin(sp.sin(3 * pi / 4)), pi / 4,
       r"$\sin\frac{3\pi}4 = \frac{\sqrt2}2$, and on the right half that height is at $\frac\pi4$.")]
same("evaluate", [e for _, e, _, _ in EV], [v for _, _, v, _ in EV])
PRACTICE = [Item(rf"Find ${tex}$.", num(v), sol, work="1cm") for tex, _, v, sol in EV]
PRACTICE += [Item(r"Explain why $\arcsin\frac12$ is $\frac\pi6$ and not $\frac{5\pi}6$, even though both have sine $\frac12$.",
                  selfcheck(r"\text{the range is } \left[-\tfrac\pi2, \tfrac\pi2\right]"),
                  r"Arcsine only answers with angles from $-\frac\pi2$ to $\frac\pi2$ (the right half of the circle), and "
                  r"$\frac{5\pi}6$ is outside that.", work="1.4cm")]
PRACTICE += [Item(rf"Find $\dfrac{{dy}}{{dx}}$ for ${tex}$.", expr(str(D(e))), sol, work="1.8cm") for tex, e, sol in P]
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
    FRQ("Algae on a lake", (
        r"Algae appear on a lake at time $t = 0$ and begin to spread. The area of the lake covered by algae is modeled by "
        r"$A(t) = 12\arctan\left(\dfrac{t}{3}\right)$, where $A(t)$ is measured in acres and $t$ is measured in weeks."), [
        Part("a", r"Find $A'(3)$. Using correct units, interpret the meaning of $A'(3)$ in the context of the problem.",
             num(2, display=r"2\ \text{acres per week}"),
             r"$A'(t) = 12\cdot\dfrac{1/3}{1 + (t/3)^2} = \dfrac{36}{9 + t^2}$, so $A'(3) = \dfrac{36}{18} = 2$. At time $t = 3$ weeks, "
             r"the area covered by algae is increasing at a rate of $2$ acres per week.",
             [(1, "$A'(t)$ with the chain rule"), (1, "$A'(3) = 2$"), (1, "interpretation with units")], work="3cm"),
        Part("b", r"Find the time $t$, for $0 < t < 3$, when the instantaneous rate of change of $A$ equals the average rate of change "
                  r"of $A$ over the time interval $0 \le t \le 3$.",
             num(sp.sqrt(36 / sp.pi - 9), tol=0.001, display=r"\sqrt{\tfrac{36}{\pi} - 9} \approx 1.568"),
             r"The average rate of change is $\dfrac{A(3) - A(0)}{3} = \dfrac{12\cdot\frac{\pi}{4} - 0}{3} = \pi$ acres per week. "
             r"Solve $\dfrac{36}{9 + t^2} = \pi$: $t^2 = \dfrac{36}{\pi} - 9$, so $t = \sqrt{\dfrac{36}{\pi} - 9} \approx 1.568$ weeks.",
             [(1, "average rate of change $\\pi$"), (1, "answer")], work="3cm"),
        Part("c", r"Assume the algae continue to spread according to this model for all $t > 0$. Write a limit expression that "
                  r"describes the end behavior of the rate of change of the area covered by algae. Evaluate this limit expression.",
             num(0),
             r"$\displaystyle\lim_{t\to\infty} A'(t) = \lim_{t\to\infty}\frac{36}{9 + t^2} = 0$.",
             [(1, "$\\displaystyle\\lim_{t\\to\\infty} A'(t)$"), (1, "value $0$")], work="2.2cm"),
    ], frq_type="Rate in context"),
]
A4 = 12 * sp.atan(t / 3)
same("frq a", [sp.simplify(sp.diff(A4, t) - 36 / (9 + t**2)), sp.diff(A4, t).subs(t, 3)], [0, 2])
avg4 = (A4.subs(t, 3) - A4.subs(t, 0)) / 3
same("frq b avg", avg4, sp.pi)
close("frq b", sp.nsolve(sp.diff(A4, t) - avg4, t, 1.5), float(sp.sqrt(36 / sp.pi - 9)), 1e-9)
same("frq c", sp.limit(sp.diff(A4, t), t, sp.oo), 0)

TOPIC = Topic(
    number="3.4", title="Differentiating Inverse Trigonometric Functions",
    unit="Unit 3: Differentiation: Composite, Implicit, and Inverse Functions", ced=["FUN-3.E", "FUN-3.E.2"],
    goals=r"Derive and use the derivatives of $\arcsin x$, $\arccos x$ and $\arctan x$, alone and with the chain rule.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
