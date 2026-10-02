"""Topic 3.1: The chain rule.

CED: FUN-3.C.1 (chain rule for composite functions). Built the way Adder asked (2026-09-30):
  1. open with fixed rates that multiply (cookies per hour times dollars per cookie), in dy/dx language;
  2. the nudge picture: a small change passes through two stretches, and the limit makes it exact;
  3. show that dy/dx = dy/du * du/dx is underspecified: dy/du must be evaluated at u = g(x);
  4. finish with (f(g(x)))' = f'(g(x)) g'(x).
The video uses the same bakery and the same y = u^3, u = x^2 + 1 example.
"""
import sympy as sp

from calclib import (VideoExample, FRQ, MCQ, BigIdea, Check, Example, Formula, Item, Part, Section, Table, Text, Topic, Variants, Video,
                     expr, num, same, selfcheck)

x, u, t = sp.symbols("x u t")
pi = sp.pi


def D(e, v=x):
    return sp.simplify(sp.diff(e, v))


# the running example: y = u^3 with u = x^2 + 1, at x = 1
same("u(1)", (x**2 + 1).subs(x, 1), 2)
same("dy/du at u=2", sp.diff(u**3, u).subs(u, 2), 12)
same("dy/dx at 1", D((x**2 + 1)**3).subs(x, 1), 24)
same("the mistake", sp.diff(u**3, u).subs(u, 1) * 2, 6)

NOTES = [
    Video("s3_1.py::Lesson", "The chain rule", 6),

    Section("Rates that multiply"),
    Text(r"A bakery sells cookies at a steady \blank{$24$ cookies per hour}, and each cookie earns 3 dollars. Its income grows at "
         r"\[ \frac{3\text{ dollars}}{\text{cookie}}\cdot\frac{24\text{ cookies}}{\text{hour}} = \mblank{72}\text{ dollars per hour.} \] "
         r"The cookies cancel, the way units do. One rate feeds the next."),
    Text(r"In derivative notation, with $D$ dollars, $c$ cookies and $t$ hours: "
         r"\[ \frac{dD}{dt} = \frac{dD}{dc}\cdot\frac{dc}{dt} = 3\cdot 24 = 72. \]"),

    Section("When the rates change: the nudge picture"),
    Text(r"Now let $y$ depend on $u$, and $u$ depend on $x$. Nudge $x$ by $dx$. Then $u$ moves by about "
         r"$\displaystyle \dfrac{du}{dx}\,dx$, and that change in $u$ moves $y$ by about \[ \frac{dy}{du}\,du. \] Each stage \blank{stretches} the nudge "
         r"by its own rate. As long as $du \ne 0$, \[ \frac{dy}{dx} = \frac{dy}{du}\cdot\frac{du}{dx}, \] "
         r"and letting the nudge $dx$ shrink to $0$ turns both fractions into derivatives."),
    Formula("Chain rule in Leibniz notation", (
        r"If $y$ is a function of $u$ and $u$ is a function of $x$, then \[ \frac{dy}{dx} = \frac{dy}{du}\cdot\frac{du}{dx}. \]")),

    Section("Where each rate is measured"),
    Text(r"Let $y = u^3$ and $u = x^2 + 1$. Find $\dfrac{dy}{dx}$ at $x = 1$. The pieces are $\dfrac{dy}{du} = 3u^2$ and "
         r"$\dfrac{du}{dx} = 2x$. At $x = 1$, $\dfrac{du}{dx} = 2$."),
    Text(r"But $\dfrac{dy}{du} = 3u^2$ is a function of $u$, so which $u$? When $x = 1$, $u = 1^2 + 1 = \mblank{2}$, so $\dfrac{dy}{du}$ "
         r"must be measured at $u = 2$: $3(2)^2 = 12$. Then $\displaystyle \frac{dy}{dx} = 12\cdot 2 = \mblank{24}$."),
    Text(r"\textbf{The trap.} Plugging $x = 1$ into $3u^2$ as if it were $u$ gives $3\cdot 2 = 6$. That's wrong. The formula "
         r"\[ \frac{dy}{dx} = \frac{dy}{du}\cdot\frac{du}{dx} \] doesn't say \emph{where} each derivative is measured; it is a little "
         r"underspecified. The outer rate has to be taken at the \blank{matching} point, $u = g(x)$."),

    Section("The chain rule with function names"),
    Formula("Chain rule", (
        r"\[ \frac{d}{dx}\Big[f\big(g(x)\big)\Big] = \mblank{f'\big(g(x)\big)}\cdot \mblank{g'(x)} \]"
        r"The derivative of the outside, evaluated at the \blank{inside}, times the derivative of the inside. This version says exactly "
        r"where $f'$ is measured. \par Naming the inside $u = g(x)$ gives the short form to remember: \[ \big[f(u)\big]' = \mblank{f'(u)\cdot u'}. \]")),
    Example("A power of a polynomial", r"Find \[ \frac{d}{dx}\left[(x^2 + 1)^3\right], \] and check it at $x = 1$.",
            r"Outside $f(u) = u^3$, inside $g(x) = x^2 + 1$: $3(x^2 + 1)^2\cdot 2x = 6x(x^2+1)^2$. At $x = 1$: $6\cdot 4 = 24$, as above.",
            work="2.4cm", beat="The trap"),
    VideoExample('Trig and exponential', work="2.2cm"),
    VideoExample('A root', work="2.4cm"),
    BigIdea(r"Rates multiply along a chain. Each derivative is measured at its own input: the outer one at $g(x)$."),
    Check(r"Find \[ \frac{d}{dx}(5x - 2)^4. \]", expr("20*(5*x-2)**3"), r"$4(5x - 2)^3\cdot 5 = 20(5x-2)^3$."),
]
same("gas", sp.Rational(1, 30) * 60, 2)
same("ex power", D((x**2 + 1)**3), 6 * x * (x**2 + 1)**2)
same("ex trig/exp", [D(sp.sin(3 * x)), D(sp.exp(x**2))], [3 * sp.cos(3 * x), 2 * x * sp.exp(x**2)])
same("ex root", sp.simplify(D(sp.sqrt(1 + sp.cos(x))) + sp.sin(x) / (2 * sp.sqrt(1 + sp.cos(x)))), 0)
same("ex table", 7 * 5, 35)

# ---------------------------------------------------------------- practice
P = [(r"y = (3x + 1)^5", (3 * x + 1)**5, r"$5(3x+1)^4\cdot 3 = 15(3x+1)^4$."),
     (r"y = (x^2 - 4x)^3", (x**2 - 4 * x)**3, r"$3(x^2 - 4x)^2(2x - 4)$."),
     (r"y = \sqrt{2x + 5}", sp.sqrt(2 * x + 5), r"$\dfrac{1}{2\sqrt{2x+5}}\cdot 2 = \dfrac{1}{\sqrt{2x+5}}$."),
     (r"y = \dfrac{1}{(x^3 + 1)^2}", (x**3 + 1)**-2, r"$-2(x^3+1)^{-3}\cdot 3x^2 = -\dfrac{6x^2}{(x^3+1)^3}$."),
     (r"y = \cos(4x)", sp.cos(4 * x), r"$-\sin(4x)\cdot 4 = -4\sin 4x$."),
     (r"y = \sin(x^2)", sp.sin(x**2), r"$\cos(x^2)\cdot 2x$."),
     (r"y = e^{5x}", sp.exp(5 * x), r"$5e^{5x}$."),
     (r"y = e^{\sin x}", sp.exp(sp.sin(x)), r"$e^{\sin x}\cos x$."),
     (r"y = \ln(x^2 + 1)", sp.log(x**2 + 1), r"$\dfrac{1}{x^2 + 1}\cdot 2x = \dfrac{2x}{x^2+1}$."),
     (r"y = \tan(3x)", sp.tan(3 * x), r"$3\sec^2(3x)$."),
     (r"y = \sin^2 x", sp.sin(x)**2, r"Outside $u^2$, inside $\sin x$: $2\sin x\cos x$."),
     (r"y = \sqrt{\ln x}", sp.sqrt(sp.log(x)), r"$\dfrac{1}{2\sqrt{\ln x}}\cdot\dfrac1x$.")]
PRACTICE = [Item(rf"Find $\dfrac{{dy}}{{dx}}$ for ${tex}$.", expr(str(D(e))), sol, work="1.8cm") for tex, e, sol in P]
PRACTICE += [
    Item(r"A printer prints 12 pages per minute, and each page uses 0.05 milliliters of ink. How fast does it use ink, in mL per minute?",
         num(sp.Rational(3, 5), display=r"0.6\text{ mL/min}"),
         r"$\dfrac{dI}{dt} = \dfrac{dI}{dp}\cdot\dfrac{dp}{dt} = 0.05\cdot 12 = 0.6$ mL per minute.", work="1.6cm"),
    Item(r"A hiker climbs a trail that rises 150 feet per mile of trail, walking at 2.5 miles per hour. How fast is the hiker gaining "
         r"elevation, in feet per hour?", num(375, display=r"375\text{ ft/hr}"),
         r"$\dfrac{dE}{dt} = \dfrac{dE}{dm}\cdot\dfrac{dm}{dt} = 150\cdot 2.5 = 375$ feet per hour.", work="1.6cm"),
    Item(r"Let $y = u^4$ and $u = 3x - 1$. Find $\dfrac{dy}{dx}$ when $x = 1$.", num(96),
         r"At $x = 1$, $u = 2$. $\dfrac{dy}{du} = 4u^3 = 32$ at $u = 2$, and $\dfrac{du}{dx} = 3$. So $\dfrac{dy}{dx} = 96$.", work="2cm"),
    Item(r"Let $y = \sqrt{u}$ and $u = x^2 + 5$. Find $\dfrac{dy}{dx}$ when $x = 2$.", num(sp.Rational(2, 3)),
         r"At $x = 2$, $u = 9$. $\dfrac{dy}{du} = \dfrac{1}{2\sqrt u} = \dfrac16$ at $u = 9$, and $\dfrac{du}{dx} = 2x = 4$. So $\dfrac{dy}{dx} = \dfrac46 = \dfrac23$.",
         work="2cm"),
    Item(r"Using the table in the notes, find $k'(4)$ for $k(x) = g\big(f(x)\big)$. The table: $f(4) = 0$, $f'(4) = 7$; and you'll need "
         r"$g'(0) = 2$.", num(14), r"$k'(4) = g'\big(f(4)\big)\cdot f'(4) = g'(0)\cdot 7 = 2\cdot 7 = 14$.", work="1.8cm"),
    Item(r"$f(2) = 5$, $f'(2) = -3$, $g(5) = 1$ and $g'(5) = 4$. Find the derivative of $g\big(f(x)\big)$ at $x = 2$.", num(-12),
         r"$g'\big(f(2)\big)\cdot f'(2) = g'(5)\cdot(-3) = 4(-3) = -12$.", work="1.6cm"),
    Item(r"Find the equation for the line tangent to $y = (2x - 3)^4$ at $x = 2$.", expr("8*x-15"),
         r"Point $(2, 1)$. Slope $4(2x-3)^3\cdot 2 = 8$ at $x = 2$. $y - 1 = 8(x - 2)$, so $y = 8x - 15$.", work="2cm"),
    Item(r"A student writes $\dfrac{d}{dx}\cos(x^2) = -\sin(2x)$. Explain the mistake and give the correct derivative.",
         selfcheck(r"-2x\sin(x^2)"),
         r"They put the inside's derivative inside the sine. The outside's derivative is evaluated at the inside, then multiplied by the "
         r"inside's derivative: $-\sin(x^2)\cdot 2x$.", work="1.8cm"),
]
same("p rates", [sp.Rational(5, 100) * 12, 150 * sp.Rational(5, 2)], [sp.Rational(3, 5), 375])
same("p leibniz", [sp.diff(u**4, u).subs(u, 2) * 3, sp.diff(sp.sqrt(u), u).subs(u, 9) * 4], [96, sp.Rational(2, 3)])
same("p tangent", sp.expand(1 + D((2 * x - 3)**4).subs(x, 2) * (x - 2)), 8 * x - 15)

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"A factory makes 40 widgets per hour, and each widget needs 3 bolts. How fast does it use bolts, in bolts per hour?", num(120),
             r"$\dfrac{dB}{dt} = \dfrac{dB}{dw}\cdot\dfrac{dw}{dt} = 3\cdot 40 = 120$ bolts per hour.", work="1.4cm"),
        Item(r"A cyclist rides at 18 kilometers per hour and burns 30 calories per kilometer. How fast is the cyclist burning calories, "
             r"in calories per hour?", num(540), r"$30\cdot 18 = 540$ calories per hour.", work="1.4cm"),
        Item(r"A pool fills at 15 gallons per minute, and each gallon raises the water level by $0.02$ inches. How fast is the level rising, "
             r"in inches per minute?", num(sp.Rational(3, 10), display="0.3"), r"$0.02\cdot 15 = 0.3$ inches per minute.", work="1.4cm"),
    ),
    Variants(
        Item(r"Find $\dfrac{d}{dx}\left[(2x^2 + 3)^4\right]$.", expr("16*x*(2*x**2+3)**3"), r"$4(2x^2+3)^3\cdot 4x = 16x(2x^2+3)^3$.", work="1.8cm"),
        Item(r"Find $\dfrac{d}{dx}\left[(1 - 5x)^6\right]$.", expr("-30*(1-5*x)**5"), r"$6(1 - 5x)^5\cdot(-5) = -30(1-5x)^5$.", work="1.8cm"),
        Item(r"Find $\dfrac{d}{dx}\sqrt{x^3 + 8}$.", expr("3*x**2/(2*sqrt(x**3+8))"), r"$\dfrac{1}{2\sqrt{x^3+8}}\cdot 3x^2$.", work="1.8cm"),
    ),
    Variants(
        Item(r"Find $\dfrac{d}{dx}\left[e^{3x^2}\right]$.", expr("6*x*exp(3*x**2)"), r"$e^{3x^2}\cdot 6x$.", work="1.6cm"),
        Item(r"Find $\dfrac{d}{dx}\sin(x^3)$.", expr("3*x**2*cos(x**3)"), r"$\cos(x^3)\cdot 3x^2$.", work="1.6cm"),
        Item(r"Find $\dfrac{d}{dx}\ln(4x + 1)$.", expr("4/(4*x+1)"), r"$\dfrac{1}{4x+1}\cdot 4$.", work="1.6cm"),
    ),
    Variants(
        Item(r"Let $y = u^3$ and $u = x^2 - 2$. Find $\dfrac{dy}{dx}$ when $x = 2$.", num(48),
             r"At $x = 2$, $u = 2$. $\dfrac{dy}{du} = 3u^2 = 12$ at $u = 2$, and $\dfrac{du}{dx} = 2x = 4$. So $48$.", work="2cm"),
        Item(r"Let $y = \dfrac1u$ and $u = 3x + 1$. Find $\dfrac{dy}{dx}$ when $x = 1$.", num(sp.Rational(-3, 16)),
             r"At $x = 1$, $u = 4$. $\dfrac{dy}{du} = -\dfrac{1}{u^2} = -\dfrac1{16}$ at $u = 4$, and $\dfrac{du}{dx} = 3$. So $-\dfrac3{16}$.", work="2cm"),
        Item(r"Let $y = u^2 + u$ and $u = x^3$. Find $\dfrac{dy}{dx}$ when $x = -1$.", num(-3),
             r"At $x = -1$, $u = -1$. $\dfrac{dy}{du} = 2u + 1 = -1$ at $u = -1$, and $\dfrac{du}{dx} = 3x^2 = 3$. So $-3$.", work="2cm"),
    ),
    Variants(
        MCQ(r"$f(3) = 2$, $f'(3) = 5$, $g(2) = 3$, $g'(2) = -1$ and $g'(3) = 4$. What is the derivative of $g\big(f(x)\big)$ at $x = 3$?",
            [r"$20$", r"$-5$", r"$-1$", r"$4$"], "B", r"$g'\big(f(3)\big)\cdot f'(3) = g'(2)\cdot 5 = -5$.",
            why_not={"A": "used $g'(3)$ instead of $g'(f(3))$", "C": "forgot to multiply by $f'(3)$"}),
        MCQ(r"$h(1) = 4$, $h'(1) = 2$, $k(4) = 0$, $k'(4) = -3$ and $k'(1) = 6$. What is the derivative of $k\big(h(x)\big)$ at $x = 1$?",
            [r"$12$", r"$-3$", r"$-6$", r"$0$"], "C", r"$k'\big(h(1)\big)\cdot h'(1) = k'(4)\cdot 2 = -6$.",
            why_not={"A": "used $k'(1)$ instead of $k'(h(1))$", "B": "forgot to multiply by $h'(1)$", "D": "that's $k(h(1))$"}),
        MCQ(r"If $y = f(x^2)$ and $f'(4) = 3$, what is $\dfrac{dy}{dx}$ at $x = 2$?", [r"$3$", r"$6$", r"$12$", r"$48$"], "C",
            r"$f'(x^2)\cdot 2x = f'(4)\cdot 4 = 12$.", why_not={"A": "forgot the inside derivative", "B": "used $2$ instead of $2x$"}),
    ),
]
same("q versions", [D((2 * x**2 + 3)**4), D((1 - 5 * x)**6), D(sp.exp(3 * x**2)), sp.diff(u**3, u).subs(u, 2) * 4,
                    sp.diff(1 / u, u).subs(u, 4) * 3, sp.diff(u**2 + u, u).subs(u, -1) * 3],
     [16 * x * (2 * x**2 + 3)**3, -30 * (1 - 5 * x)**5, 6 * x * sp.exp(3 * x**2), 48, sp.Rational(-3, 16), -3])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"If $f(x) = \sqrt{x^2 + 9}$, then $f'(4) =$", [r"$\dfrac45$", r"$\dfrac{1}{10}$", r"$8$", r"$\dfrac{2}{5}$"], "A",
        r"$\dfrac{x}{\sqrt{x^2+9}} = \dfrac45$ at $x = 4$.", why_not={"B": "forgot the inside derivative", "D": "lost the factor of 2"}),
    MCQ(r"$\dfrac{d}{dx}\left[\cos^3(2x)\right] =$",
        [r"$3\cos^2(2x)$", r"$-6\cos^2(2x)\sin(2x)$", r"$-3\cos^2(2x)\sin(2x)$", r"$6\cos^2(2x)\sin(2x)$"], "B",
        r"Three layers: $3\cos^2(2x)\cdot(-\sin 2x)\cdot 2$.", why_not={"C": "forgot the innermost $2$", "D": "lost the minus sign"}),
    MCQ(r"The table gives values of $f$, $f'$, $g$ and $g'$."
        r"\par\centerline{\begin{tabular}{c|cccc} $x$ & $f(x)$ & $f'(x)$ & $g(x)$ & $g'(x)$ \\ \hline 1 & 2 & 3 & 3 & $-2$ \\ 3 & 1 & 4 & 2 & 5\end{tabular}}"
        r"\par If $h(x) = f\big(g(x)\big)$, then $h'(1) =$", [r"$-6$", r"$15$", r"$-4$", r"$-8$"], "D",
        r"$f'\big(g(1)\big)\cdot g'(1) = f'(3)\cdot(-2) = 4(-2) = -8$.", why_not={"A": "used $f'(1)$"}),
    MCQ(r"A balloon's radius grows at 2 cm per second. Its volume is $V = \frac43\pi r^3$. How fast is the volume growing when $r = 5$ cm?",
        [r"$100\pi$ cm$^3$/s", r"$200\pi$ cm$^3$/s", r"$\frac{500}{3}\pi$ cm$^3$/s", r"$50\pi$ cm$^3$/s"], "B",
        r"$\dfrac{dV}{dt} = \dfrac{dV}{dr}\cdot\dfrac{dr}{dt} = 4\pi r^2\cdot 2 = 200\pi$ at $r = 5$.",
        why_not={"A": "forgot the factor $\\frac{dr}{dt} = 2$", "C": "that's the volume"}),
]
same("m1", D(sp.sqrt(x**2 + 9)).subs(x, 4), sp.Rational(4, 5))
same("m2", sp.simplify(D(sp.cos(2 * x)**3) + 6 * sp.cos(2 * x)**2 * sp.sin(2 * x)), 0)
same("m4", sp.diff(sp.Rational(4, 3) * pi * u**3, u).subs(u, 5) * 2, 200 * pi)

TAB = (r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $x$ & $f(x)$ & $f'(x)$ & $g(x)$ & $g'(x)$ \\ \hline "
       r"$0$ & $2$ & $-1$ & $3$ & $4$ \\ $2$ & $3$ & $5$ & $0$ & $-2$ \\ $3$ & $0$ & $6$ & $2$ & $1$\end{tabular}}")
FRQS = [
    FRQ("Composite functions from a table", r"The functions $f$ and $g$ are differentiable. Selected values are given." + TAB, [
        Part("a", r"Let $h(x) = f\big(g(x)\big)$. Find $h'(2)$.", num(2),
             r"$h'(2) = f'\big(g(2)\big)\cdot g'(2) = f'(0)\cdot(-2) = (-1)(-2) = 2$.", [(1, "chain rule"), (1, "value")], work="2cm"),
        Part("b", r"Let $k(x) = \big[g(x)\big]^3$. Find $k'(3)$.", num(12),
             r"$k'(3) = 3\big[g(3)\big]^2\cdot g'(3) = 3(2)^2(1) = 12$.", [(1, "chain rule on the power"), (1, "value")], work="2cm"),
        Part("c", r"Let $m(x) = g\big(f(x)\big)$. Write an equation for the line tangent to the graph of $m$ at $x = 3$.", expr("24*x-69"),
             r"$m(3) = g\big(f(3)\big) = g(0) = 3$, and $m'(3) = g'\big(f(3)\big)\cdot f'(3) = g'(0)\cdot 6 = 4\cdot 6 = 24$. "
             r"So $y - 3 = 24(x - 3)$.", [(1, "point"), (1, "slope"), (1, "equation")], work="2.4cm"),
        Part("d", r"Explain why $f'\big(g(2)\big)\cdot g'(2)$ is not the same as $f'(2)\cdot g'(2)$.", selfcheck(r"f' \text{ is read at } g(2) = 0"),
             r"The outer derivative is measured at the inside value $g(2) = 0$, so we need $f'(0) = -1$, not $f'(2) = 5$.",
             [(1, "outer derivative at $g(2)$")], work="1.8cm"),
    ], frq_type="Table of values / rates"),
]
same("frq", [(-1) * (-2), 3 * 2**2 * 1, 4 * 6], [2, 12, 24])

TOPIC = Topic(
    number="3.1", title="The Chain Rule",
    unit="Unit 3: Differentiation: Composite, Implicit, and Inverse Functions", ced=["FUN-3.C", "FUN-3.C.1"],
    goals=r"Differentiate composite functions with the chain rule, measuring the outer derivative at the inside value.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
