"""Topic 2.8: The product rule.

CED: FUN-3.B.1 (product rule). The growing-rectangle picture in the notes matches the video.
"""
import sympy as sp

from calclib import (Variants, FRQ, MCQ, BigIdea, Check, Example, Figure, Formula, Item, Part, Section, Table, Text, Topic,
                     Video, VideoExample, expr, num, same, selfcheck)

x = sp.symbols("x")
same("example", sp.diff(x**2 * sp.sin(x), x), 2 * x * sp.sin(x) + x**2 * sp.cos(x))
same("revenue", 2 * 300 + 40 * (-10), 200)

FIG_RECT = Figure(name="t2_8_rect", caption=r"A product as an area, $A = w\,l$. Growing both sides adds $l\,dw + w\,dl$, plus a tiny corner.",
                  tikz=(r"\begin{tikzpicture}[scale=1.05]"
                        r"\fill[wash] (0,0) rectangle (4,2.4); \draw[line width=0.9pt] (0,0) rectangle (4,2.4);"
                        r"\fill[pattern=north east lines, pattern color=black!55] (4,0) rectangle (4.5,2.4); \draw (4,0) rectangle (4.5,2.4);"
                        r"\fill[pattern=north west lines, pattern color=black!55] (0,2.4) rectangle (4,2.8); \draw (0,2.4) rectangle (4,2.8);"
                        r"\fill[black!70] (4,2.4) rectangle (4.5,2.8);"
                        r"\node at (2,1.2) {$w\,l$}; \node[below] at (2,0) {$w$}; \node[left] at (0,1.2) {$l$};"
                        r"\node[below] at (4.25,0) {$dw$}; \node[left] at (0,2.6) {$dl$};"
                        r"\node[right] at (4.5,1.2) {$l\,dw$}; \node[above] at (2,2.8) {$w\,dl$};"
                        r"\end{tikzpicture}"))


def D(e):
    return sp.simplify(sp.diff(e, x))


NOTES = [
    Video("s2_8.py::Lesson", "The product rule", 3),

    Section("Not the product of the derivatives"),
    Text(r"\[ \frac{d}{dx}[x\cdot x] = \frac{d}{dx}[x^2] = \mblank{2x} \], but the product of the derivatives is $1\cdot 1 = \mblank{1}$. "
         r"So the derivative of a product is \emph{not} the product of the derivatives."),

    Section("The product rule"),
    FIG_RECT,
    Text(r"Let $w$ and $l$ depend on $x$. Nudging $x$ by $dx$ adds two strips and a corner: "
         r"\[ dA = l\,dw + w\,dl + dw\,dl. \] Divide by $dx$: "
         r"\[ \frac{dA}{dx} = l\,\frac{dw}{dx} + w\,\frac{dl}{dx} + dw\cdot\frac{dl}{dx}. \] "
         r"As the nudge shrinks to $0$, $dw \to \mblank{0}$, so the corner term vanishes and "
         r"\[ \frac{dA}{dx} = \mblank{l\,\frac{dw}{dx} + w\,\frac{dl}{dx}} \]."),
    Formula("Product rule", (
        r"\[ \frac{d}{dx}\left[f(x)\,g(x)\right] = \mblank{f'(x)\,g(x) + f(x)\,g'(x)} \]"
        r"With $u$ and $v$ for the two factors (each one a function of $x$, multiplied together): \[ (uv)' = \mblank{u'v + uv'}. \] "
        r"In words: derivative of the first times the second, plus the first times the derivative of the second.")),
    Text(r"\textbf{How to work one.} Underline the two factors and label them $u$ and $v$. Write $u' = \ldots$ and $v' = \ldots$. Then put the four pieces into $u'v + uv'$."),
    VideoExample("Two factors", work="2.2cm"),
    VideoExample("Exponential times a polynomial", work="2.2cm"),
    Text(r"\textbf{At a point.} To find $f'(a)$ you don't need the derivative as a formula: find the four numbers $u(a)$, $v(a)$, $u'(a)$, $v'(a)$ and put them into the rule."),
    VideoExample("At a point, no formula needed", work="2.6cm"),
    VideoExample("In context", work="2.2cm"),
    BigIdea(r"Each factor takes a turn changing while the other holds still; add the two contributions."),
    Check(r"Find \[ \frac{d}{dx}\left[x\ln x\right]. \]", expr("log(x) + 1"), r"\[ 1\cdot\ln x + x\cdot\frac1x = \ln x + 1. \]"),
]
same("ex2", D((x**3 - 1) * sp.exp(x)), sp.exp(x) * (x**3 + 3 * x**2 - 1))
same("check", D(x * sp.log(x)), sp.log(x) + 1)

# ---------------------------------------------------------------- practice
P = [(r"y = x^3\cos x", x**3 * sp.cos(x)), (r"y = e^x\sin x", sp.exp(x) * sp.sin(x)), (r"y = (2x + 1)(x^2 - 4)", (2 * x + 1) * (x**2 - 4)),
     (r"y = \sqrt{x}\,e^x", sp.sqrt(x) * sp.exp(x)), (r"y = x^2\ln x", x**2 * sp.log(x)), (r"y = \sin x\cos x", sp.sin(x) * sp.cos(x))]
SOL = [r"$3x^2\cos x - x^3\sin x$.", r"$e^x\sin x + e^x\cos x$.", r"$2(x^2 - 4) + (2x+1)(2x) = 6x^2 + 2x - 8$.",
       r"$\dfrac{e^x}{2\sqrt x} + \sqrt x\,e^x$.", r"$2x\ln x + x$.", r"$\cos^2 x - \sin^2 x$."]
PRACTICE = [Item(rf"Find $\dfrac{{dy}}{{dx}}$ for ${tex}$.", expr(str(D(e))), sol, work="2cm") for (tex, e), sol in zip(P, SOL)]
PRACTICE += [
    Item(r"$f(1) = 2$, $f'(1) = 3$, $g(1) = -4$, $g'(1) = 5$. If $h(x) = f(x)g(x)$, find $h'(1)$.", num(-2),
         r"$3(-4) + 2(5) = -2$.", work="1.6cm"),
    Item(r"Find the equation for the line tangent to $y = xe^x$ at $x = 0$.", expr("x"), r"$y' = e^x + xe^x = 1$ at $0$; point $(0,0)$: $y = x$.",
         work="1.8cm"),
    Item(r"Where does $y = xe^x$ have a horizontal tangent line?", num(-1), r"$e^x(1 + x) = 0$ gives $x = -1$.", work="1.6cm"),
    Item(r"Use the product rule twice to find $\dfrac{d}{dx}\left[x^2e^x\sin x\right]$.",
         expr(str(D(x**2 * sp.exp(x) * sp.sin(x)))),
         r"$2xe^x\sin x + x^2e^x\sin x + x^2e^x\cos x$. Each of the three factors takes a turn.", work="2.6cm"),
]
same("p7", 3 * (-4) + 2 * 5, -2)
same("p9", sp.solve(D(x * sp.exp(x)), x), [-1])

# extra practice (round 1)
P2 = [(r"y = x^4 e^x", x**4 * sp.exp(x), r"$4x^3e^x + x^4e^x$."),
      (r"y = x\cos x", x * sp.cos(x), r"$\cos x - x\sin x$."),
      (r"y = (x^2 + 3)\ln x", (x**2 + 3) * sp.log(x), r"$2x\ln x + \dfrac{x^2 + 3}{x}$."),
      (r"y = \sqrt{x}\sin x", sp.sqrt(x) * sp.sin(x), r"$\dfrac{\sin x}{2\sqrt x} + \sqrt x\cos x$."),
      (r"y = e^x\cos x", sp.exp(x) * sp.cos(x), r"$e^x\cos x - e^x\sin x$.")]
for tex, e, sol in P2:
    PRACTICE.append(Item(rf"Find $\dfrac{{dy}}{{dx}}$ for ${tex}$.", expr(str(D(e))), sol, work="2cm"))
PRACTICE += [
    Item(r"$f(3) = -1$, $f'(3) = 4$, $g(3) = 2$ and $g'(3) = 5$. If $h(x) = f(x)g(x)$, find $h'(3)$.", num(3),
         r"$h'(3) = f'(3)g(3) + f(3)g'(3) = 4(2) + (-1)(5) = 3$.", work="1.6cm"),
    Item(r"Using the same values, let $k(x) = x^2 f(x)$. Find $k'(3)$.", num(30),
         r"$k'(x) = 2xf(x) + x^2f'(x)$, so $k'(3) = 6(-1) + 9(4) = 30$.", work="1.6cm"),
    Item(r"Find the equation for the line tangent to $y = x\ln x$ at $x = 1$.", expr("x-1"),
         r"$y' = \ln x + 1$, which is $1$ at $x = 1$. Point $(1, 0)$: $y = x - 1$.", work="1.8cm"),
    Item(r"Where does $y = x^2e^x$ have horizontal tangent lines? Enter the negative $x$-value.", num(-2),
         r"$y' = 2xe^x + x^2e^x = xe^x(2 + x)$. Since $e^x > 0$, $y' = 0$ at $x = 0$ and $x = -2$.", work="2cm"),
    Item(r"Zuri says $\dfrac{d}{dx}\left[x^2\sin x\right] = 2x\cos x$. Explain the mistake and give the correct derivative.",
         selfcheck(r"2x\sin x + x^2\cos x"),
         r"Zuri multiplied the two derivatives. The product rule gives $2x\sin x + x^2\cos x$.", work="1.8cm"),
]
same("x1 derivs", [D(e) for _, e, _ in P2],
     [4 * x**3 * sp.exp(x) + x**4 * sp.exp(x), sp.cos(x) - x * sp.sin(x), 2 * x * sp.log(x) + (x**2 + 3) / x,
      sp.sin(x) / (2 * sp.sqrt(x)) + sp.sqrt(x) * sp.cos(x), sp.exp(x) * sp.cos(x) - sp.exp(x) * sp.sin(x)])
same("x1 h", 4 * 2 + (-1) * 5, 3)
same("x1 k", 2 * 3 * (-1) + 9 * 4, 30)
same("x1 tan", D(x * sp.log(x)).subs(x, 1), 1)
same("x1 horiz", sorted(sp.solve(D(x**2 * sp.exp(x)), x)), [-2, 0])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find $\dfrac{d}{dx}\left[x^4 e^x\right]$.", expr("4*x**3*exp(x) + x**4*exp(x)"), r"$4x^3e^x + x^4e^x$.", work="1.6cm"),
        Item(r"Find $\dfrac{d}{dx}\left[x^2 \cos x\right]$.", expr("2*x*cos(x) - x**2*sin(x)"), r"$2x\cos x - x^2\sin x$.", work="1.6cm"),
        Item(r"Find $\dfrac{d}{dx}\left[\sqrt{x}\,\ln x\right]$.", expr("log(x)/(2*sqrt(x)) + 1/sqrt(x)"),
             r"$\dfrac{\ln x}{2\sqrt x} + \sqrt x\cdot\dfrac1x = \dfrac{\ln x}{2\sqrt x} + \dfrac{1}{\sqrt x}$.", work="1.6cm"),
    ),
    Variants(
        Item(r"Find $\dfrac{d}{dx}\left[x\sin x\right]$.", expr("sin(x) + x*cos(x)"), r"$\sin x + x\cos x$.", work="1.6cm"),
        Item(r"Find $\dfrac{d}{dx}\left[e^x\cos x\right]$.", expr("exp(x)*cos(x) - exp(x)*sin(x)"), r"$e^x\cos x - e^x\sin x$.", work="1.6cm"),
        Item(r"Find $\dfrac{d}{dx}\left[(3x - 2)(x^2 + 1)\right]$.", expr("9*x**2 - 4*x + 3"),
             r"$3(x^2 + 1) + (3x - 2)(2x) = 9x^2 - 4x + 3$.", work="1.6cm"),
    ),
    Variants(
        Item(r"$f(3) = 4$, $f'(3) = -2$, $g(3) = 1$, $g'(3) = 6$. Find the derivative of $f(x)g(x)$ at $x = 3$.", num(22),
             r"$(-2)(1) + (4)(6) = 22$.", work="1.6cm"),
        Item(r"$f(0) = -1$, $f'(0) = 5$, $g(0) = 3$, $g'(0) = 2$. Find the derivative of $f(x)g(x)$ at $x = 0$.", num(13),
             r"$(5)(3) + (-1)(2) = 13$.", work="1.6cm"),
        Item(r"$f(2) = 6$, $f'(2) = 1$. Find the derivative of $x^2 f(x)$ at $x = 2$.", num(28),
             r"$2x f(x) + x^2 f'(x) = 2(2)(6) + 4(1) = 28$.", work="1.6cm"),
    ),
    Variants(
        MCQ(r"Which is the derivative of $f(x)g(x)$?", [r"$f'(x)g'(x)$", r"$f'(x)g(x) + f(x)g'(x)$", r"$f'(x)g(x) - f(x)g'(x)$",
                                                         r"$f(x)g'(x)$"], "B", r"The product rule.",
            why_not={"A": "the tempting mistake", "C": "that sign belongs to the quotient rule numerator"}),
        MCQ(r"A student writes $\dfrac{d}{dx}\left[x^3\sin x\right] = 3x^2\cos x$. What went wrong?",
            [r"Nothing", r"They multiplied the two derivatives instead of using the product rule", r"They should have divided", r"The $3$ should be $2$"], "B",
            r"The correct derivative is $3x^2\sin x + x^3\cos x$.", why_not={"A": "check $x \\cdot x$: the rule gives $2x$, not $1$"}),
        MCQ(r"In the growing-rectangle picture of the product rule, what happens to the small corner $dw\,dl$?",
            [r"It becomes the second term of the rule", r"It doubles", r"It vanishes in the limit because $dw \to 0$", r"It equals $w\,l$"], "C",
            r"After dividing by $dx$, the corner is $dw\cdot\frac{dl}{dx}$, and $dw \to 0$."),
    ),
    Variants(
        MCQ(r"If $y = x\ln x$, then $y'(e) =$", [r"$1$", r"$e$", r"$2$", r"$e + 1$"], "C", r"$\ln x + 1 = 2$ at $x = e$."),
        MCQ(r"If $y = xe^x$, then $y'(0) =$", [r"$0$", r"$1$", r"$2$", r"$e$"], "B", r"$e^x + xe^x = 1$ at $x = 0$."),
        MCQ(r"If $y = x\cos x$, then $y'(\pi) =$", [r"$-1$", r"$0$", r"$\pi$", r"$-\pi$"], "A", r"$\cos x - x\sin x = -1 - 0 = -1$ at $x = \pi$."),
    ),
]

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"If $f(x) = x^2\cos x$, then $f'(\pi)$ is", [r"$-\pi^2$", r"$-2\pi$", r"$2\pi$", r"$\pi^2$"], "B",
        r"$2x\cos x - x^2\sin x$ at $\pi$: $2\pi(-1) - 0 = -2\pi$."),
    MCQ(r"Let $h(x) = f(x)g(x)$. Using the table, find $h'(2)$."
        r"\par\centerline{\begin{tabular}{c|cccc} $x$ & $f(x)$ & $f'(x)$ & $g(x)$ & $g'(x)$ \\ \hline 2 & $-3$ & 4 & 5 & $-1$\end{tabular}}",
        [r"$-4$", r"$-17$", r"$23$", r"$17$"], "C", r"$4(5) + (-3)(-1) = 23$.", why_not={"A": "multiplied the derivatives",
                                                                                           "D": "sign error"}),
    MCQ(r"An equation for the line tangent to $y = (x + 1)e^x$ at $x = 0$ is", [r"$y = 2x + 1$", r"$y = x + 1$", r"$y = 2x$", r"$y = e x + 1$"], "A",
        r"$y' = e^x + (x+1)e^x = 2$ at $x = 0$; point $(0, 1)$."),
    MCQ(r"The width of a rectangle is $2$ cm and growing at $0.5$ cm/s; its length is $7$ cm and shrinking at $0.2$ cm/s. At that "
        r"moment the area is changing at", [r"$-0.1$ cm²/s", r"$3.9$ cm²/s", r"$3.1$ cm²/s", r"$-0.4$ cm²/s"], "C",
        r"$A' = w'l + wl' = 0.5(7) + 2(-0.2) = 3.1$.", why_not={"A": "multiplied the rates", "B": "sign error"}),
]
same("m1", sp.diff(x**2 * sp.cos(x), x).subs(x, sp.pi), -2 * sp.pi)
same("m4", sp.Rational(5, 10) * 7 + 2 * sp.Rational(-2, 10), sp.Rational(31, 10))

FRQS = [
    FRQ("Product rule from a table", (
        r"The functions $f$ and $g$ are differentiable for all real numbers. The table gives values of the functions and their "
        r"derivatives at selected values of $x$."
        r"\par\smallskip\centerline{\begin{tabular}{c|cccc} $x$ & $f(x)$ & $f'(x)$ & $g(x)$ & $g'(x)$ \\ \hline "
        r"1 & 3 & $-2$ & 4 & 1 \\ 3 & 6 & 5 & $-2$ & 3\end{tabular}}"), [
        Part("a", r"Let $h$ be the function defined by $h(x) = f(x)g(x)$. Find $h'(3)$. Show the work that leads to your answer.",
             num(8), r"$h'(3) = f'(3)g(3) + f(3)g'(3) = 5(-2) + 6(3) = 8$.", [(1, "product rule"), (1, "answer $8$")],
             work="2.2cm"),
        Part("b", r"Let $k$ be the function defined by $k(x) = x^2 f(x)$. Find $k'(1)$. Show the work that leads to your answer.",
             num(4), r"$k'(x) = 2xf(x) + x^2f'(x)$, so $k'(1) = 2(1)(3) + (1)^2(-2) = 4$.",
             [(1, "$k'(x)$ by the product rule"), (1, "answer $4$")], work="2.2cm"),
        Part("c", r"Write an equation for the line tangent to the graph of $h$ at $x = 1$.", expr("-5*x+17"),
             r"$h(1) = f(1)g(1) = 12$ and $h'(1) = f'(1)g(1) + f(1)g'(1) = (-2)(4) + 3(1) = -5$. The tangent line is "
             r"$y = 12 - 5(x - 1)$.",
             [(1, "$h(1) = 12$ and $h'(1) = -5$"), (1, "tangent line equation")], work="2.4cm"),
    ], frq_type="Derivatives from a table"),
]
same("frq", [5 * (-2) + 6 * 3, 2 * 3 + 1 * (-2), (-2) * 4 + 3 * 1], [8, 4, -5])
same("frq c", sp.expand(12 - 5 * (x - 1)), -5 * x + 17)

TOPIC = Topic(
    number="2.8", title="The Product Rule",
    unit="Unit 2: Differentiation", ced=["FUN-3.B", "FUN-3.B.1"],
    goals=r"Differentiate products of functions with the product rule, from formulas, tables and contexts.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
