"""Topic 2.5: Applying the power rule.

CED: FUN-3.A.1 (power rule for real exponents). The square/cube growth pictures in the video
motivate d/dx x^2 = 2x and d/dx x^3 = 3x^2 before the general rule.
"""
import sympy as sp

from calclib import (Variants, FRQ, MCQ, BigIdea, Check, Example, Figure, Formula, Item, Part, Section, Table, Text,
                     Topic, Video, VideoExample, expr, num, same, selfcheck)

x = sp.symbols("x", positive=True)
X = sp.symbols("x")
same("square nudge", sp.expand((X + sp.Symbol("d"))**2 - X**2), 2 * X * sp.Symbol("d") + sp.Symbol("d")**2)
same("x^2", sp.diff(x**2, x), 2 * x)
same("x^3", sp.diff(x**3, x), 3 * x**2)

FIG_SQ = Figure(name="t2_5_square", caption=r"Growing the side from $x$ to $x + dx$ adds two strips of area $x\,dx$ and a tiny corner.",
                tikz=(r"\begin{tikzpicture}[scale=1.1]"
                      r"\fill[wash] (0,0) rectangle (3,3); \draw[line width=0.9pt] (0,0) rectangle (3,3);"
                      r"\fill[pattern=north east lines, pattern color=black!55] (3,0) rectangle (3.45,3);"
                      r"\fill[pattern=north east lines, pattern color=black!55] (0,3) rectangle (3,3.45);"
                      r"\fill[black!70] (3,3) rectangle (3.45,3.45); \draw (3,0) rectangle (3.45,3.45); \draw (0,3) -- (3,3.45) (0,3.45) -- (3,3.45);"
                      r"\draw (0,3) rectangle (3,3.45);"
                      r"\node at (1.5,1.5) {$x^2$}; \node[below] at (1.5,0) {$x$}; \node[below] at (3.22,0) {$dx$};"
                      r"\node[right] at (3.45,1.5) {$x\,dx$}; \node[above] at (1.5,3.45) {$x\,dx$}; \node[right] at (3.45,3.3) {$(dx)^2$};"
                      r"\end{tikzpicture}"))


def D(e):
    return sp.simplify(sp.diff(e, x))


NOTES = [
    Video("s2_5.py::Lesson", "The power rule", 3.5),

    Section("Why $x^2$ has derivative $2x$"),
    FIG_SQ,
    Text(r"\textbf{The nudge $dx$.} Historically, $dx$ was thought of as an \emph{infinitesimal}: an infinitely small change in $x$. "
         r"For us, $dx$ is just a tiny nudge to $x$, and we watch what happens as that nudge shrinks toward $0$."),
    Text(r"When the side of a square grows from $x$ to $x + dx$, its area grows by two strips and a corner: "
         r"\[ dA = 2x\,dx + (dx)^2. \] Divide by $dx$: \[ \frac{dA}{dx} = 2x + dx. \] "
         r"As the nudge shrinks to $0$, the corner vanishes from the rate and $\displaystyle \frac{dA}{dx} = \mblank{2x}$. "
         r"The corner shrinks faster than the strips."),
    Text(r"A cube of side $x$ gains three slabs, three rods and one tiny cube: "
         r"\[ dV = 3x^2\,dx + 3x\,(dx)^2 + (dx)^3, \qquad \frac{dV}{dx} = 3x^2 + 3x\,dx + (dx)^2. \] As $dx \to 0$, only "
         r"the slabs are left: $\displaystyle \frac{d}{dx}x^3 = \mblank{3x^2}$."),
    Text(r"Dividing by $dx$ and then letting the nudge shrink to $0$ is the limit definition of the derivative, written in short form. "
         r"It's fine to think of $dx$ and $dy$ as \blank{infinitely small} changes, as long as you know the formal definition comes from \blank{limits}."),

    Section("The power rule"),
    Formula("Power rule", (
        r"\[ \frac{d}{dx}\left[x^n\right] = \mblank{n x^{n-1}} \qquad \text{for any real number } n \]."
        r"Special cases: $\displaystyle \dfrac{d}{dx}[x] = \mblank{1}$ and $\displaystyle \frac{d}{dx}[1] = \frac{d}{dx}[x^0] = \mblank{0}$.")),
    Text(r"\textbf{Two steps.} (1) Multiply by the exponent: bring it down \blank{in front}. (2) \blank{Subtract one} from the exponent. "
         r"For $x^5$: the $5$ comes down front, and $5 - 1 = 4$, so \[ \frac{d}{dx}\left[x^5\right] = 5x^4. \]"),
    Table(r"$\dfrac{1}{x^3}$ & $x^{-3}$ & $-3x^{-4}$ \\ $\sqrt{x}$ & $x^{1/2}$ & $\tfrac12 x^{-1/2}$ \\ "
          r"$\sqrt[3]{x^2}$ & $x^{2/3}$ & $\tfrac23 x^{-1/3}$ \\ $x\sqrt{x}$ & $x^{3/2}$ & $\tfrac32 x^{1/2}$",
          "ccc", header=r"function & rewritten & derivative"),
    Text(r"\textbf{Rewrite first.} Radicals become fractional exponents; $x$ in a denominator becomes a negative exponent."),
    VideoExample("Slope and rate", work="3cm"),
    VideoExample("Tangent line", work="2.6cm"),
    BigIdea(r"Bring the exponent down and subtract one. Rewrite radicals and reciprocals as powers first."),
    Check(r"Find \[ \frac{d}{dx}\left[\frac{1}{x^5}\right]. \]", expr("-5*x**(-6)"), r"$x^{-5}$ gives \[ -5x^{-6} = -\frac{5}{x^6}. \]"),
]
same("table", [D(x**-3), D(sp.sqrt(x)), D(x**sp.Rational(2, 3)), D(x * sp.sqrt(x))],
     [-3 * x**-4, 1 / (2 * sp.sqrt(x)), sp.Rational(2, 3) * x**sp.Rational(-1, 3), sp.Rational(3, 2) * sp.sqrt(x)])
same("ex tangent", sp.expand(2 + sp.Rational(1, 4) * (X - 4)), X / 4 + 1)

# ---------------------------------------------------------------- practice
P = [(r"x^9", x**9), (r"x^{-4}", x**-4), (r"\dfrac{1}{x^2}", x**-2), (r"x^{3/4}", x**sp.Rational(3, 4)),
     (r"\sqrt[5]{x}", x**sp.Rational(1, 5)), (r"\dfrac{1}{\sqrt{x}}", x**sp.Rational(-1, 2)), (r"x^2\sqrt{x}", x**sp.Rational(5, 2)),
     (r"x^{\pi}", x**sp.pi)]
PRACTICE = [Item(rf"Find $\dfrac{{dy}}{{dx}}$ for $y = {tex}$.", expr(str(D(e))), rf"${sp.latex(D(e))}$", work="1.4cm")
            for tex, e in P]
PRACTICE += [
    Item(r"Find the slope of the tangent line to $y = x^{-1}$ at $x = 2$.", num(sp.Rational(-1, 4)), r"$-x^{-2} = -\frac14$.", work="1.4cm"),
    Item(r"Find the equation for the line tangent to $y = x^3$ at $x = -2$.", expr("12*x+16"),
         r"Slope $3(4) = 12$, point $(-2, -8)$: $y = 12x + 16$.", work="2cm"),
    Item(r"At what $x$-value does $y = x^{3/2}$ have a tangent line with slope $3$?", num(4),
         r"$\frac32 x^{1/2} = 3$, so $\sqrt x = 2$ and $x = 4$.", work="1.8cm"),
    Item(r"The volume of a cube with edge $s$ inches is $V = s^3$. Find $\dfrac{dV}{ds}$ when $s = 3$ and include units.", num(27),
         r"$3s^2 = 27$ cubic inches per inch.", work="1.6cm"),
]
same("p10", sp.expand(-8 + 12 * (X + 2)), 12 * X + 16)
same("p11", sp.solve(sp.Eq(sp.Rational(3, 2) * sp.sqrt(x), 3), x)[0], 4)

# extra practice (round 1)
P2 = [(r"x^{12}", x**12, None), (r"\dfrac{1}{x^5}", x**-5, r"Rewrite as $x^{-5}$."),
      (r"\sqrt[3]{x^2}", x**sp.Rational(2, 3), r"Rewrite as $x^{2/3}$."),
      (r"\dfrac{1}{\sqrt[4]{x}}", x**sp.Rational(-1, 4), r"Rewrite as $x^{-1/4}$."),
      (r"x\sqrt[3]{x}", x**sp.Rational(4, 3), r"Rewrite as $x^1\cdot x^{1/3} = x^{4/3}$."),
      (r"\dfrac{x^5}{x^2}", x**3, r"Simplify first: $x^3$.")]
for tex, e, pre in P2:
    PRACTICE.append(Item(rf"Find $\dfrac{{dy}}{{dx}}$ for $y = {tex}$.", expr(str(D(e))),
                         ((pre + " Then ") if pre else "") + rf"$\dfrac{{dy}}{{dx}} = {sp.latex(D(e))}$.", work="1.4cm"))
PRACTICE += [
    Item(r"Find the slope of the tangent line to $y = \sqrt{x}$ at $x = 16$.", num(sp.Rational(1, 8)),
         r"$\dfrac{dy}{dx} = \frac12 x^{-1/2} = \dfrac{1}{2\sqrt x}$, and at $x = 16$ that is $\dfrac{1}{8}$.", work="1.6cm"),
    Item(r"Find the equation for the line tangent to $y = \dfrac{1}{x^2}$ at $x = 1$.", expr("3-2*x"),
         r"$\dfrac{dy}{dx} = -2x^{-3}$, so the slope at $x = 1$ is $-2$. Point $(1, 1)$: $y - 1 = -2(x - 1)$, so $y = -2x + 3$.",
         work="2cm"),
    Item(r"Where does $y = x^4$ have a tangent line with slope $32$?", num(2),
         r"$4x^3 = 32$, so $x^3 = 8$ and $x = 2$.", work="1.6cm"),
    Item(r"The area of a circle is $A = \pi r^2$. Using the power rule on $r^2$, $\dfrac{dA}{dr} = 2\pi r$. Find $\dfrac{dA}{dr}$ "
         r"when $r = 5$ cm and interpret it.", num(10 * sp.pi, display=r"10\pi\ \text{cm}^2\text{/cm}"),
         r"$2\pi(5) = 10\pi \approx 31.4$. When the radius is $5$ cm, the area grows by about $31.4$ square centimeters for each "
         r"centimeter the radius grows.", work="2cm"),
]
same("x1 derivs", [D(e) for _, e, _ in P2],
     [12 * x**11, -5 * x**-6, sp.Rational(2, 3) * x**sp.Rational(-1, 3), -sp.Rational(1, 4) * x**sp.Rational(-5, 4),
      sp.Rational(4, 3) * x**sp.Rational(1, 3), 3 * x**2])
same("x1 sqrt", D(sp.sqrt(x)).subs(x, 16), sp.Rational(1, 8))
same("x1 tan", sp.expand(1 - 2 * (X - 1)), 3 - 2 * X)
same("x1 x4", sp.solve(sp.Eq(4 * x**3, 32), x), [2])

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Find $\dfrac{d}{dx}\left[x^{12}\right]$.", expr("12*x**11"), r"$12x^{11}$.", work="1.2cm"),
        Item(r"Find $\dfrac{d}{dx}\left[x^{-5}\right]$.", expr("-5*x**(-6)"), r"$-5x^{-6}$.", work="1.2cm"),
        Item(r"Find $\dfrac{d}{dx}\left[x^{7/2}\right]$.", expr("7*x**(5/2)/2"), r"$\frac72 x^{5/2}$.", work="1.2cm"),
    ),
    Variants(
        Item(r"Find $\dfrac{d}{dx}\left[\sqrt[3]{x}\right]$.", expr("x**(-2/3)/3"), r"Rewrite as $x^{1/3}$: $\frac13 x^{-2/3}$.", work="1.4cm"),
        Item(r"Find $\dfrac{d}{dx}\left[\dfrac{1}{\sqrt{x}}\right]$.", expr("-x**(-3/2)/2"), r"Rewrite as $x^{-1/2}$: $-\frac12 x^{-3/2}$.", work="1.4cm"),
        Item(r"Find $\dfrac{d}{dx}\left[x^2\sqrt{x}\right]$.", expr("5*x**(3/2)/2"), r"Rewrite as $x^{5/2}$: $\frac52 x^{3/2}$.", work="1.4cm"),
    ),
    Variants(
        Item(r"Find the slope of the tangent line to $y = \dfrac{1}{x^3}$ at $x = 1$.", num(-3), r"$-3x^{-4} = -3$ at $x = 1$.", work="1.4cm"),
        Item(r"Find the slope of the tangent line to $y = \sqrt{x}$ at $x = 25$.", num(sp.Rational(1, 10)), r"$\frac12x^{-1/2} = \frac{1}{10}$ at $x = 25$.", work="1.4cm"),
        Item(r"Find the slope of the tangent line to $y = x^5$ at $x = -1$.", num(5), r"$5x^4 = 5$ at $x = -1$.", work="1.4cm"),
    ),
    Variants(
        MCQ(r"If $f(x) = x^{-2}$, then $f'(x) =$", [r"$-2x^{-1}$", r"$-2x^{-3}$", r"$2x^{-3}$", r"$-x^{-3}$"], "B",
            r"Bring down $-2$ and subtract $1$ from the exponent: $-3$.", why_not={"A": "added $1$ to the exponent"}),
        MCQ(r"If $f(x) = x^{1/4}$, then $f'(x) =$", [r"$\frac14x^{5/4}$", r"$4x^{-3/4}$", r"$\frac14x^{-3/4}$", r"$x^{-3/4}$"], "C",
            r"Bring down $\frac14$ and subtract $1$: $\frac14 - 1 = -\frac34$.", why_not={"A": "added $1$ to the exponent"}),
        MCQ(r"If $f(x) = \dfrac{1}{x}$, then $f'(x) =$", [r"$-\dfrac{1}{x^2}$", r"$\dfrac{1}{x^2}$", r"$\ln x$", r"$-\dfrac1x$"], "A",
            r"$x^{-1}$ gives $-x^{-2}$.", why_not={"C": "that's going the other direction"}),
    ),
    Variants(
        MCQ(r"The tangent line to $y = x^4$ at $x = 1$ is", [r"$y = 4x - 3$", r"$y = 4x + 1$", r"$y = x^3$", r"$y = 4x$"], "A",
            r"Slope $4$, point $(1, 1)$: $y = 4x - 3$."),
        MCQ(r"The tangent line to $y = x^3$ at $x = 2$ is", [r"$y = 12x$", r"$y = 3x + 2$", r"$y = 12x - 16$", r"$y = 12x + 8$"], "C",
            r"Slope $3(4) = 12$, point $(2, 8)$: $y - 8 = 12(x - 2)$."),
        MCQ(r"The tangent line to $y = \sqrt{x}$ at $x = 4$ is", [r"$y = \frac14x + 1$", r"$y = \frac14x + 2$", r"$y = 4x - 14$", r"$y = \frac12x$"], "A",
            r"Slope $\frac{1}{2\sqrt4} = \frac14$, point $(4, 2)$: $y = \frac14x + 1$."),
    ),
]
same("q versions", [D(x**sp.Rational(7, 2)), D(x**sp.Rational(-1, 2)), D(x**sp.Rational(1, 2)).subs(x, 25), sp.expand(X**0 * (8 + 12 * (X - 2)))],
     [sp.Rational(7, 2) * x**sp.Rational(5, 2), -x**sp.Rational(-3, 2) / 2, sp.Rational(1, 10), 12 * X - 16])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"If $y = \dfrac{1}{\sqrt[4]{x}}$, then $\dfrac{dy}{dx} =$",
        [r"$-\dfrac14 x^{-5/4}$", r"$\dfrac14 x^{-3/4}$", r"$-\dfrac14 x^{-3/4}$", r"$-4x^{-5}$"], "A",
        r"$y = x^{-1/4}$, so $y' = -\frac14 x^{-5/4}$.", why_not={"C": "subtracted wrong", "B": "treated as $x^{1/4}$"}),
    MCQ(r"At what point does $y = x^3$ have a tangent line parallel to $y = 12x - 5$ with positive $x$-coordinate?",
        [r"$(1, 1)$", r"$(12, 1728)$", r"$(2, 8)$", r"$(4, 64)$"], "C", r"$3x^2 = 12$ gives $x = 2$."),
    MCQ(r"$\displaystyle\lim_{h\to0}\frac{(2+h)^5 - 32}{h}$ is", [r"$32$", r"$5$", r"$0$", r"$80$"], "D",
        r"It is the derivative of $x^5$ at $x = 2$: $5(2)^4 = 80$.", why_not={"A": "that is $2^5$"}),
    MCQ(r"Which function has derivative $\dfrac{3}{2}\sqrt{x}$?", [r"$x^{3/2}$", r"$\sqrt{x^3} + x$", r"$\dfrac32 x^{1/2}$", r"$x^{1/2}$"], "A",
        r"$\frac{d}{dx}x^{3/2} = \frac32 x^{1/2}$."),
]
same("m3", sp.limit(((2 + x)**5 - 32) / x, x, 0), 80)

FRQS = [
    FRQ("Tangent lines to a power function", r"Let $f$ be the function defined by $f(x) = x^{2/3}$ for all real numbers $x$.", [
        Part("a", r"Write an equation for the line tangent to the graph of $f$ at $x = 8$.", expr("x/3 + 4/3"),
             r"$f'(x) = \frac23 x^{-1/3}$, so $f'(8) = \frac23\cdot\frac12 = \frac13$, and $f(8) = 4$. The tangent line is "
             r"$y = 4 + \frac13(x - 8)$.",
             [(1, "$f'(8) = \\frac13$"), (1, "tangent line equation")], work="2.6cm"),
        Part("b", r"Find the $x$-coordinate of the point on the graph of $f$ at which the line tangent to the graph is parallel to "
                  r"the line $y = \frac23 x + 5$.", num(1),
             r"Parallel lines have equal slopes: $\dfrac{2}{3x^{1/3}} = \dfrac23$, so $x^{1/3} = 1$ and $x = 1$.",
             [(1, "sets $f'(x) = \\frac23$"), (1, "answer $x = 1$")], work="2.4cm"),
        Part("c", r"For each of $f'(-1)$ and $f'(0)$, find the value or explain why it does not exist.",
             selfcheck(r"f'(-1) = -\tfrac23;\ f'(0)\ \text{does not exist}"),
             r"$f'(-1) = \dfrac{2}{3(-1)^{1/3}} = -\dfrac23$. At $x = 0$, $\dfrac{f(0+h) - f(0)}{h} = \dfrac{h^{2/3}}{h} = \dfrac{1}{h^{1/3}}$, "
             r"which is unbounded as $h \to 0$ (it approaches $-\infty$ from the left and $\infty$ from the right). The limit does not "
             r"exist, so $f'(0)$ does not exist.",
             [(1, "$f'(-1) = -\\frac23$"), (1, "$f'(0)$ does not exist, with a reason")], work="2.8cm"),
    ], frq_type="Function analysis"),
]
xr_ = sp.symbols("xr_", real=True)
fr_ = sp.cbrt(xr_)**2
same("frq a", sp.expand(4 + sp.Rational(1, 3) * (xr_ - 8)), sp.expand(fr_.subs(xr_, 8) + sp.diff(fr_, xr_).subs(xr_, 8) * (xr_ - 8)))
same("frq b", sp.solve(sp.Eq(sp.Rational(2, 3) / sp.cbrt(X), sp.Rational(2, 3)), X), [1])
same("frq c", sp.Rational(2, 3) / sp.Integer(-1), sp.Rational(-2, 3))

TOPIC = Topic(
    number="2.5", title="Applying the Power Rule",
    unit="Unit 2: Differentiation", ced=["FUN-3.A", "FUN-3.A.1"],
    goals=r"Differentiate powers of $x$ with any real exponent, rewriting radicals and reciprocals first.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
