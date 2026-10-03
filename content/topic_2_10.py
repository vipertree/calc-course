"""Topic 2.10: Derivatives of tan x, cot x, sec x and csc x.

CED: FUN-3.B.3 (rewrite trig functions and use the quotient rule). The notes derive tan x with the quotient rule and
show the unit-circle nudge picture for it (Adder: geometric proofs where we can), as the video does.
"""
import sympy as sp

from calclib import (FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Text, Topic, Variants, Video, VideoExample, expr,
                     limchain, num, same, selfcheck)

x, t = sp.symbols("x t")
pi = sp.pi


def D(e):
    return sp.simplify(sp.diff(e, x))


same("tan", sp.simplify(D(sp.tan(x)) - 1 / sp.cos(x)**2), 0)
same("sec", sp.simplify(D(1 / sp.cos(x)) - sp.sin(x) / sp.cos(x)**2), 0)
same("cot", sp.simplify(D(sp.cot(x)) + 1 / sp.sin(x)**2), 0)
same("csc", sp.simplify(D(1 / sp.sin(x)) + sp.cos(x) / sp.sin(x)**2), 0)

NOTES = [
    Video("s2_10.py::Lesson", "Four more trig derivatives", 4),

    Section("A quick review"),
    Text(r"On the unit circle, the point at angle $\theta$ is $(\cos\theta, \sin\theta)$. The other four trig functions are built from those two: "
         r"\[ \tan\theta = \frac{\sin\theta}{\cos\theta}, \quad \cot\theta = \frac{\cos\theta}{\sin\theta}, \quad "
         r"\sec\theta = \frac{1}{\cos\theta}, \quad \csc\theta = \frac{1}{\sin\theta}. \] "
         r"Cotangent is the reciprocal of tangent, secant is the reciprocal of cosine, and cosecant is the reciprocal of sine. "
         r"Secant goes with cosine and cosecant with sine: each pair has exactly one ``co.'' "
         r"We'll also need the Pythagorean identity: \[ \sin^2\theta + \cos^2\theta = 1. \]"),

    Section("Tangent, from the quotient rule"),
    Text(r"Write \[ \tan x = \frac{\sin x}{\cos x} \] and use the quotient rule: "
         r"\[ \begin{aligned} \frac{d}{dx}\tan x &= \frac{\cos x\cdot\cos x - \sin x\cdot(-\sin x)}{\cos^2 x} \\ "
         r"&= \frac{\cos^2 x + \sin^2 x}{\cos^2 x} = \frac{1}{\cos^2 x}, \end{aligned} \] "
         r"using the Pythagorean identity $\cos^2 x + \sin^2 x = 1$, so $\dfrac{d}{dx}\tan x = \mblank{\sec^2 x}$."),
    Text(r"\textbf{Picture it.} On the unit circle, the ray at angle $\theta$ meets the line $x = 1$ at height $\tan\theta$, at a distance "
         r"\blank{$\sec\theta$} from the origin. Nudge the angle by $d\theta$: that point sweeps about $\sec\theta\cdot d\theta$ "
         r"sideways, and because the line $x = 1$ is tilted at angle $\theta$ to that sweep, the height changes by about "
         r"$\sec\theta\cdot\sec\theta\,d\theta$. Dividing by $d\theta$ and letting $d\theta \to 0$ gives $\sec^2\theta$."),

    Section("Secant, cotangent, cosecant"),
    Text(r"\[ \sec x = \frac{1}{\cos x}, \] so by the quotient rule "
         r"\[ \begin{aligned} \frac{d}{dx}\sec x &= \frac{\cos x\cdot 0 - 1\cdot(-\sin x)}{\cos^2 x} \\ "
         r"&= \frac{\sin x}{\cos^2 x} = \frac{1}{\cos x}\cdot\frac{\sin x}{\cos x}, \end{aligned} \] "
         r"which is $\mblank{\sec x\tan x}$. "
         r"Cotangent and cosecant work the same way, starting from $\dfrac{\cos x}{\sin x}$ and $\dfrac{1}{\sin x}$."),
    Formula("Six trig derivatives ($x$ in radians)", (
        r"\[ \frac{d}{dx}\sin x = \cos x \qquad \frac{d}{dx}\tan x = \mblank{\sec^2 x} \qquad \frac{d}{dx}\sec x = \mblank{\sec x\tan x} \]"
        r"\[ \frac{d}{dx}\cos x = -\sin x \qquad \frac{d}{dx}\cot x = \mblank{-\csc^2 x} \qquad \frac{d}{dx}\csc x = \mblank{-\csc x\cot x} \]"
        r"Pattern: the ``co'' functions (cosine, cotangent, cosecant) get a \blank{minus sign}, and each is the mirror of its partner.")),

    Section("Using them"),
    VideoExample("A product with tangent", work="2cm"),
    VideoExample("A tangent line", work="2.4cm"),
    BigIdea(r"Rewrite each trig function with sine and cosine, and the quotient rule does the rest. Memorize the six results."),
    Check(r"Find the slope of $y = \sec x$ at $x = 0$.", num(0), r"$\sec 0\tan 0 = 1\cdot 0 = 0$."),
]
same("ex3 slope", sp.diff(sp.tan(x), x).subs(x, pi / 4), 2)

# ---------------------------------------------------------------- practice
P = [(r"y = 4\tan x", 4 * sp.tan(x), r"$4\sec^2 x$."),
     (r"y = \sec x + \csc x", 1 / sp.cos(x) + 1 / sp.sin(x), r"$\sec x\tan x - \csc x\cot x$."),
     (r"y = x - \cot x", x - sp.cot(x), r"$1 + \csc^2 x$."),
     (r"y = 5\csc x", 5 / sp.sin(x), r"$-5\csc x\cot x$."),
     (r"y = x\sec x", x / sp.cos(x), r"Product rule: $\sec x + x\sec x\tan x$."),
     (r"y = e^x\tan x", sp.exp(x) * sp.tan(x), r"Product rule: $e^x\tan x + e^x\sec^2 x$."),
     (r"y = \dfrac{\tan x}{x}", sp.tan(x) / x, r"Quotient rule: $\dfrac{x\sec^2 x - \tan x}{x^2}$."),
     (r"y = \sin x\,\sec x", sp.tan(x), r"Simplify first: $\sin x\sec x = \tan x$, so $\sec^2 x$.")]
PRACTICE = [Item(rf"Find $\dfrac{{dy}}{{dx}}$ for ${tex}$.", expr(str(D(e))), sol, work="1.8cm") for tex, e, sol in P]
PRACTICE += [
    Item(r"Find the slope of the tangent line to $y = \tan x$ at $x = 0$.", num(1), r"$\sec^2 0 = 1$.", work="1.2cm"),
    Item(r"Find the slope of the tangent line to $y = \sec x$ at $x = \dfrac\pi3$.", num(2 * sp.sqrt(3)),
         r"$\sec\frac\pi3\tan\frac\pi3 = 2\sqrt3$.", work="1.4cm"),
    Item(r"Find the slope of the tangent line to $y = \cot x$ at $x = \dfrac\pi2$.", num(-1), r"$-\csc^2\frac\pi2 = -1$.", work="1.4cm"),
    Item(r"Find the slope of the tangent line to $y = \csc x$ at $x = \dfrac\pi6$.", num(-2 * sp.sqrt(3)),
         r"$-\csc\frac\pi6\cot\frac\pi6 = -2\sqrt3$.", work="1.4cm"),
    Item(r"Find the equation for the line tangent to $y = \sec x$ at $x = 0$.", expr("1"),
         r"Point $(0, 1)$, slope $\sec 0\tan 0 = 0$: the horizontal line $y = 1$.", work="1.8cm"),
    Item(r"Find the equation for the line tangent to $y = 2\tan x$ at $x = \dfrac\pi4$.", expr("4*x - pi + 2"),
         r"Point $\left(\frac\pi4, 2\right)$, slope $2\sec^2\frac\pi4 = 4$: $y - 2 = 4\left(x - \frac\pi4\right)$, so $y = 4x - \pi + 2$.",
         work="2cm"),
    Item(r"Use the quotient rule on $\cot x = \dfrac{\cos x}{\sin x}$ to show that its derivative is $-\csc^2 x$.",
         selfcheck(r"-\csc^2 x"),
         r"$\dfrac{\sin x(-\sin x) - \cos x\cos x}{\sin^2 x} = \dfrac{-(\sin^2 x + \cos^2 x)}{\sin^2 x} = -\dfrac{1}{\sin^2 x} = -\csc^2 x$, using the Pythagorean identity $\sin^2 x + \cos^2 x = 1$.",
         work="2.6cm"),
    Item(r"For $0 < x < \pi$, where does $y = x - 2\sin x$ have a horizontal tangent? (A warm-up with the older rules.)",
         num(pi / 3), r"$1 - 2\cos x = 0$, so $\cos x = \frac12$ and $x = \frac\pi3$.", work="1.8cm"),
    Item(r"For $0 \le x < \frac{\pi}{2}$, where does $y = 2x - \tan x$ have a horizontal tangent?", num(pi / 4),
         r"$2 - \sec^2 x = 0$, so $\sec^2 x = 2$, $\cos x = \frac{1}{\sqrt2}$, and $x = \frac\pi4$.", work="2cm"),
    Item(r"A ramp covers 10 feet of ground and rises at angle $\theta$, so its height is $h(\theta) = 10\tan\theta$ feet. "
         r"Find $h'\!\left(\frac\pi6\right)$ and give its units.", num(sp.Rational(40, 3), display=r"\tfrac{40}{3}\text{ ft per radian}"),
         r"$h'(\theta) = 10\sec^2\theta$, and $\sec^2\frac\pi6 = \frac43$, so $h'\!\left(\frac\pi6\right) = \frac{40}{3}$ feet per radian.",
         work="2.2cm"),
    Item(r"Is $\sec x$ ever $0$? Use this to explain why the slope of $\tan x$ is never $0$.", selfcheck(r"\text{no; } \sec^2 x \ge 1"),
         r"$\sec x = \frac{1}{\cos x}$ can't be $0$; in fact $|\sec x| \ge 1$, so $\sec^2 x \ge 1$. The tangent graph always rises with "
         r"slope at least $1$.", work="1.8cm"),
    Item(r"$f(x) = \tan x$. Find $f'(x)$ and $f''(x)$, the derivative of $f'$. Enter $f''(x)$.", expr("2*tan(x)/cos(x)**2"),
         r"$f'(x) = \sec^2 x = \sec x\cdot\sec x$. Product rule: $f''(x) = 2\sec x\cdot\sec x\tan x = 2\sec^2 x\tan x$.", work="2.2cm"),
]
same("p slopes", [D(sp.tan(x)).subs(x, 0), D(1 / sp.cos(x)).subs(x, pi / 3), D(sp.cot(x)).subs(x, pi / 2), D(1 / sp.sin(x)).subs(x, pi / 6)],
     [1, 2 * sp.sqrt(3), -1, -2 * sp.sqrt(3)])
same("p tangent", sp.expand(2 + D(2 * sp.tan(x)).subs(x, pi / 4) * (x - pi / 4)), 4 * x - pi + 2)
same("p horiz", [sp.solve(1 - 2 * sp.cos(x), x)[0], D(2 * x - sp.tan(x)).subs(x, pi / 4)], [pi / 3, 0])
same("p ladder", D(10 * sp.tan(x)).subs(x, pi / 6), sp.Rational(40, 3))
same("p second", sp.simplify(sp.diff(sp.tan(x), x, 2) - 2 * sp.tan(x) / sp.cos(x)**2), 0)

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find $\dfrac{dy}{dx}$ for $y = 3\tan x + \sec x$.", expr("3/cos(x)**2 + tan(x)/cos(x)"), r"$3\sec^2 x + \sec x\tan x$.", work="1.4cm"),
        Item(r"Find $\dfrac{dy}{dx}$ for $y = 2\cot x - x$.", expr("-2/sin(x)**2 - 1"), r"$-2\csc^2 x - 1$.", work="1.4cm"),
        Item(r"Find $\dfrac{dy}{dx}$ for $y = \csc x + 4\tan x$.", expr("-cos(x)/sin(x)**2 + 4/cos(x)**2"), r"$-\csc x\cot x + 4\sec^2 x$.", work="1.4cm"),
    ),
    Variants(
        Item(r"Find $\dfrac{d}{dx}\left[x\tan x\right]$.", expr("tan(x) + x/cos(x)**2"), r"$\tan x + x\sec^2 x$.", work="1.6cm"),
        Item(r"Find $\dfrac{d}{dx}\left[x^2\sec x\right]$.", expr("2*x/cos(x) + x**2*tan(x)/cos(x)"), r"$2x\sec x + x^2\sec x\tan x$.", work="1.6cm"),
        Item(r"Find $\dfrac{d}{dx}\left[e^x\cot x\right]$.", expr("exp(x)*cot(x) - exp(x)/sin(x)**2"), r"$e^x\cot x - e^x\csc^2 x$.", work="1.6cm"),
    ),
    Variants(
        Item(r"Find the slope of the tangent line to $y = \tan x$ at $x = \dfrac\pi3$.", num(4), r"$\sec^2\frac\pi3 = 2^2 = 4$.", work="1.4cm"),
        Item(r"Find the slope of the tangent line to $y = \sec x$ at $x = \dfrac\pi4$.", num(sp.sqrt(2)), r"$\sec\frac\pi4\tan\frac\pi4 = \sqrt2$.", work="1.4cm"),
        Item(r"Find the slope of the tangent line to $y = \cot x$ at $x = \dfrac\pi4$.", num(-2), r"$-\csc^2\frac\pi4 = -2$.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"$\dfrac{d}{dx}\sec x =$", [r"$\sec^2 x$", r"$\sec x\tan x$", r"$-\csc x\cot x$", r"$\tan^2 x$"], "B", r"From $\frac{1}{\cos x}$ and the quotient rule.",
            why_not={"A": "that's for $\\tan x$", "C": "that's for $\\csc x$"}),
        MCQ(r"$\dfrac{d}{dx}\cot x =$", [r"$\csc^2 x$", r"$-\tan^2 x$", r"$-\csc^2 x$", r"$\sec^2 x$"], "C", r"Co-functions get the minus sign.",
            why_not={"A": "missing the minus", "D": "that's for $\\tan x$"}),
        MCQ(r"$\dfrac{d}{dx}\csc x =$", [r"$-\csc x\cot x$", r"$\csc x\cot x$", r"$-\csc^2 x$", r"$\sec x\tan x$"], "A", r"Co-functions get the minus sign.",
            why_not={"B": "missing the minus", "C": "that's for $\\cot x$"}),
    ),
    Variants(
        MCQ(r"The tangent line to $y = \tan x$ at $x = 0$ is", [r"$y = 0$", r"$y = 1$", r"$y = x$", r"$y = x + 1$"], "C",
            r"Point $(0, 0)$, slope $\sec^2 0 = 1$: $y = x$."),
        MCQ(r"The tangent line to $y = \sec x$ at $x = 0$ is", [r"$y = 1$", r"$y = x$", r"$y = x + 1$", r"$y = 0$"], "A",
            r"Point $(0, 1)$, slope $\sec 0\tan 0 = 0$: the horizontal line $y = 1$."),
        MCQ(r"The tangent line to $y = \cot x$ at $x = \dfrac\pi2$ is", [r"$y = x - \frac\pi2$", r"$y = 0$", r"$y = -1$", r"$y = -x + \frac\pi2$"], "D",
            r"Point $\left(\frac\pi2, 0\right)$, slope $-\csc^2\frac\pi2 = -1$: $y = -\left(x - \frac\pi2\right)$."),
    ),
]
same("q slopes", [D(sp.tan(x)).subs(x, pi / 3), D(1 / sp.cos(x)).subs(x, pi / 4), D(sp.cot(x)).subs(x, pi / 4)], [4, sp.sqrt(2), -2])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"If $f(x) = \tan x - 2x$, then $f'\!\left(\dfrac\pi4\right) =$", [r"$0$", r"$-1$", r"$2$", r"$1 - \dfrac\pi2$"], "A",
        r"$\sec^2\frac\pi4 - 2 = 2 - 2 = 0$.", why_not={"D": "that's $f\\left(\\frac\\pi4\\right)$"}),
    MCQ(r"$\displaystyle\lim_{h\to0}\frac{\tan\left(\frac\pi3 + h\right) - \sqrt3}{h}$ is", [r"$\sqrt3$", r"$2$", r"$4$", r"$0$"], "C",
        r"It is the derivative of $\tan x$ at $\frac\pi3$: $\sec^2\frac\pi3 = 4$.", why_not={"B": "that's $\\sec\\frac\\pi3$"}),
    MCQ(r"Which is the derivative of $\dfrac{1 + \sec x}{\tan x}$? (Hint: simplify first.)",
        [r"$\dfrac{\sec x\tan x}{\sec^2 x}$", r"$-\dfrac{1}{1 - \cos x}$", r"$\csc x$", r"$\sec^2 x$"], "B",
        r"$\dfrac{1 + \sec x}{\tan x} = \dfrac{\cos x + 1}{\sin x}$. Quotient rule: $\dfrac{-\sin^2 x - (\cos x + 1)\cos x}{\sin^2 x} = "
        r"\dfrac{-(1 + \cos x)}{1 - \cos^2 x} = -\dfrac{1}{1 - \cos x}$ (the Pythagorean identity turns $\sin^2 x$ into $1 - \cos^2 x$).", why_not={"A": "divided the derivatives"}),
    MCQ(r"A searchlight 50 meters from a wall makes angle $\theta$ with the perpendicular, and its spot is $s = 50\tan\theta$ meters from "
        r"the nearest point of the wall. How fast is $s$ changing with respect to $\theta$ when $\theta = \frac\pi4$?",
        [r"$50$ m per radian", r"$25$ m per radian", r"$100$ m per radian", r"$50\sqrt2$ m per radian"], "C",
        r"$\frac{ds}{d\theta} = 50\sec^2\theta = 50\cdot 2 = 100$.", why_not={"A": "forgot to square $\\sec$", "D": "used $\\sec$ instead of $\\sec^2$"}),
]
same("m1", D(sp.tan(x) - 2 * x).subs(x, pi / 4), 0)
same("m2", sp.limit((sp.tan(pi / 3 + x) - sp.sqrt(3)) / x, x, 0), 4)
same("m3", sp.simplify(D((1 + 1 / sp.cos(x)) / sp.tan(x)) + 1 / (1 - sp.cos(x))), 0)
same("m4", D(50 * sp.tan(x)).subs(x, pi / 4), 100)

FRQS = [
    FRQ("A tilting camera", (
        r"A camera on the ground, 30 feet from the base of a rocket launch pad, tilts up to follow a rocket. When the camera makes "
        r"an angle of $\theta$ radians with the ground, the height of the rocket is $H(\theta) = 30\tan\theta$ feet, for "
        r"$0 \le \theta < \frac{\pi}{2}$."), [
        Part("a", r"Find $H'\!\left(\frac\pi3\right)$. Using correct units, interpret the meaning of $H'\!\left(\frac\pi3\right)$ in "
                  r"the context of the problem.", num(120, display=r"120\ \text{feet per radian}"),
             r"$H'(\theta) = 30\sec^2\theta$, so $H'\!\left(\frac\pi3\right) = 30(2)^2 = 120$. When the camera angle is $\frac\pi3$ "
             r"radians, the rocket's height is increasing at a rate of $120$ feet per radian of camera angle.",
             [(1, "$H'(\\theta) = 30\\sec^2\\theta$"), (1, "value $120$"), (1, "interpretation with units")], work="3cm"),
        Part("b", r"Find the value of $\theta$, for $0 < \theta < \frac{\pi}{2}$, at which $H'(\theta) = 60$.",
             num(sp.pi / 4, tol=0.001, display=r"\tfrac{\pi}{4}"),
             r"$30\sec^2\theta = 60$ gives $\sec^2\theta = 2$, so $\cos\theta = \frac{1}{\sqrt2}$ and $\theta = \frac{\pi}{4}$.",
             [(1, "sets $30\\sec^2\\theta = 60$"), (1, "answer $\\frac{\\pi}{4}$")], work="2.4cm"),
        Part("c", r"Write an equation for the line tangent to the graph of $H$ at $\theta = \frac{\pi}{4}$.",
             selfcheck(r"y = 30 + 60\left(\theta - \tfrac{\pi}{4}\right)"),
             r"$H\!\left(\frac\pi4\right) = 30\tan\frac\pi4 = 30$ and $H'\!\left(\frac\pi4\right) = 60$, so the tangent line is "
             r"$y = 30 + 60\left(\theta - \frac{\pi}{4}\right)$.",
             [(1, "tangent line equation")], work="2cm"),
    ], frq_type="Rate in context"),
]
same("frq", [sp.diff(30 * sp.tan(t), t).subs(t, pi / 3)], [120])
same("frq b", [r for r in sp.solve(sp.Eq(sp.diff(30 * sp.tan(t), t), 60), t) if 0 < r < pi / 2], [pi / 4])
same("frq c", (30 * sp.tan(t)).subs(t, pi / 4), 30)

TOPIC = Topic(
    number="2.10", title="Finding the Derivatives of Tangent, Cotangent, Secant, and/or Cosecant Functions",
    unit="Unit 2: Differentiation", ced=["FUN-3.B", "FUN-3.B.3"],
    goals=r"Differentiate $\tan x$, $\cot x$, $\sec x$ and $\csc x$ by rewriting with sine and cosine, and use the results with the other rules.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
