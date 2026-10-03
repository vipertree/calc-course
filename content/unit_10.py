"""Unit 10 test (BC): Infinite Sequences and Series. AP format: 12 MCQ (no calculator), 4 MCQ (calculator), 3 FRQ, two
forms for every slot. Covers 10.1-10.15 (all BC).

Choices are built by `pick`, which puts the keyed answer at a planned letter. Every keyed value is checked with sympy.
"""
import sympy as sp

from calclib import FRQ, MCQ, Part, UnitTest, Variants, close, num, same, selfcheck

x = sp.symbols("x", real=True)
n = sp.symbols("n", integer=True, positive=True)
ser = lambda f, k: sp.series(f, x, 0, k).removeO()


def pick(stem, right, wrong, letter, solution, why=None, calc=False):
    k = "ABCD".index(letter)
    choices = list(wrong)
    choices.insert(k, right)
    why_not = {}
    if why:
        for text, reason in why.items():
            why_not["ABCD"[choices.index(text)]] = reason
    return MCQ(stem, choices, letter, solution, why_not=why_not, calc=calc)


same("A1", [sp.summation(1 / (n * (n + 1)), (n, 1, sp.oo)), sp.summation(1 / ((n + 1) * (n + 2)), (n, 1, sp.oo))], [1, sp.Rational(1, 2)])
same("A2", [sp.summation(3 * sp.Rational(2, 5)**(n - 1), (n, 1, sp.oo)), sp.summation(sp.Rational(-1, 3)**n, (n, 1, sp.oo))], [5, -sp.Rational(1, 4)])
same("A10", [ser(sp.exp(-x**2), 7), ser(x * sp.sin(x), 7)], [1 - x**2 + x**4 / 2 - x**6 / 6, x**2 - x**4 / 6 + x**6 / 120])

A = [
    Variants(
        pick(r"$\displaystyle\sum_{n=1}^\infty \frac{1}{n(n + 1)} = $", r"$1$", [r"$\frac12$", r"$2$", r"divergent"], "B", r"Telescopes: $S_N = 1 - \frac{1}{N + 1}$."),
        pick(r"$\displaystyle\sum_{n=1}^\infty \frac{1}{(n + 1)(n + 2)} = $", r"$\frac12$", [r"$1$", r"$\frac13$", r"divergent"], "A", r"Telescopes to $\frac12$."),
    ),
    Variants(
        pick(r"$\displaystyle\sum_{n=1}^\infty 3\left(\frac25\right)^{n-1} = $", r"$5$", [r"$2$", r"$\frac{15}{2}$", r"divergent"], "D", r"$a = 3$, $r = \frac25$: $\frac{3}{3/5}$."),
        pick(r"$\displaystyle\sum_{n=1}^\infty \left(-\frac13\right)^{n} = $", r"$-\frac14$", [r"$\frac34$", r"$-\frac13$", r"$\frac14$"], "C", r"$\frac{-1/3}{4/3}$."),
    ),
    Variants(
        pick(r"Which series diverges by the $n$th term test?", r"$\sum \frac{n}{2n + 1}$", [r"$\sum \frac1n$", r"$\sum \frac{1}{n^2}$", r"$\sum \frac{(-1)^n}{n}$"], "A", r"$\frac{n}{2n + 1} \to \frac12$.", {r"$\sum \frac1n$": "diverges, but its terms go to $0$"}),
        pick(r"Which series diverges by the $n$th term test?", r"$\sum \cos\frac1n$", [r"$\sum \frac{1}{\sqrt n}$", r"$\sum \frac{1}{n\ln n}$", r"$\sum \frac{n}{3^n}$"], "B", r"$\cos\frac1n \to 1$."),
    ),
    Variants(
        pick(r"Which $p$-series converges?", r"$\sum \frac{1}{n^{3/2}}$", [r"$\sum \frac{1}{\sqrt n}$", r"$\sum \frac1n$", r"$\sum \frac{1}{n^{0.99}}$"], "C", r"$p = \frac32 > 1$."),
        pick(r"Which $p$-series diverges?", r"$\sum \frac{1}{\sqrt[3]{n}}$", [r"$\sum \frac{1}{n^2}$", r"$\sum \frac{1}{n^{1.1}}$", r"$\sum n^{-\pi}$"], "D", r"$p = \frac13$."),
    ),
    Variants(
        pick(r"By the integral test, $\sum_{n=2}^\infty \frac{1}{n(\ln n)^2}$", r"converges", [r"diverges", r"converges to $\frac{1}{\ln 2}$", r"cannot be tested"], "A", r"$\int_2^\infty \frac{dx}{x(\ln x)^2} = \frac{1}{\ln 2}$ is finite.", {r"converges to $\frac{1}{\ln 2}$": "the integral's value is not the sum"}),
        pick(r"By the integral test, $\sum_{n=1}^\infty \frac{n}{n^2 + 1}$", r"diverges", [r"converges", r"converges to $\frac{\ln 2}{2}$", r"cannot be tested"], "C", r"$\int \frac{x}{x^2 + 1}\,dx = \frac12\ln(x^2 + 1) \to \infty$."),
    ),
    Variants(
        pick(r"By limit comparison with $\frac{1}{n^2}$, $\sum \frac{2n + 1}{n^3 + 4}$", r"converges", [r"diverges", r"is inconclusive", r"converges to $2$"], "A", r"Limit $2$; $\sum \frac{1}{n^2}$ converges."),
        pick(r"By limit comparison with $\frac1n$, $\sum \frac{n + 3}{n^2 + 1}$", r"diverges", [r"converges", r"is inconclusive", r"converges to $1$"], "B", r"Limit $1$; harmonic diverges."),
    ),
    Variants(
        pick(r"$\sum_{n=1}^\infty \frac{(-1)^n}{\sqrt n}$ is", r"conditionally convergent", [r"absolutely convergent", r"divergent", r"convergent to $0$"], "D", r"$\sum \frac{1}{\sqrt n}$ diverges; AST converges."),
        pick(r"$\sum_{n=1}^\infty \frac{(-1)^n}{n^2}$ is", r"absolutely convergent", [r"conditionally convergent", r"divergent", r"convergent only by the AST"], "C", r"$\sum \frac{1}{n^2}$ converges."),
    ),
    Variants(
        pick(r"For $\sum \frac{n^2}{3^n}$, the ratio test gives $L = $", r"$\frac13$", [r"$1$", r"$3$", r"$0$"], "A", r"$\frac{(n + 1)^2}{3n^2} \to \frac13$."),
        pick(r"For $\sum \frac{3^n}{n!}$, the ratio test gives $L = $", r"$0$", [r"$3$", r"$1$", r"$\frac13$"], "D", r"$\frac{3}{n + 1} \to 0$."),
    ),
    Variants(
        pick(r"Using $S_4$ to approximate $\sum_{n=1}^\infty \frac{(-1)^{n+1}}{n}$, the error is at most", r"$\frac15$", [r"$\frac14$", r"$\frac{1}{20}$", r"$\frac{1}{120}$"], "B", r"The first omitted term.", {r"$\frac14$": "the last term used"}),
        pick(r"Using $S_3$ to approximate $\sum_{n=1}^\infty \frac{(-1)^{n+1}}{n^2}$, the error is at most", r"$\frac{1}{16}$", [r"$\frac19$", r"$\frac{1}{25}$", r"$\frac14$"], "A", r"$b_4 = \frac{1}{16}$."),
    ),
    Variants(
        pick(r"The first three nonzero terms of the Maclaurin series for $e^{-x^2}$ are", r"$1 - x^2 + \frac{x^4}{2}$", [r"$1 - x + \frac{x^2}{2}$", r"$1 + x^2 + \frac{x^4}{2}$", r"$1 - x^2 + x^4$"], "C", r"Substitute $u = -x^2$ into $e^u$."),
        pick(r"The first three nonzero terms of the Maclaurin series for $x\sin x$ are", r"$x^2 - \frac{x^4}{6} + \frac{x^6}{120}$", [r"$x - \frac{x^3}{6} + \frac{x^5}{120}$", r"$x^2 - \frac{x^4}{2} + \frac{x^6}{24}$", r"$x^2 + \frac{x^4}{6} + \frac{x^6}{120}$"], "A", r"$x$ times the sine series."),
    ),
    Variants(
        pick(r"The interval of convergence of $\sum_{n=1}^\infty \frac{(x - 2)^n}{n \cdot 3^n}$ is", r"$[-1, 5)$", [r"$(-1, 5)$", r"$(-1, 5]$", r"$[-1, 5]$"], "D", r"$R = 3$; $x = 5$: harmonic; $x = -1$: AST."),
        pick(r"The interval of convergence of $\sum_{n=1}^\infty \frac{x^n}{n^2}$ is", r"$[-1, 1]$", [r"$(-1, 1)$", r"$[-1, 1)$", r"$(-1, 1]$"], "B", r"$R = 1$; both endpoints converge ($p = 2$)."),
    ),
    Variants(
        pick(r"The Maclaurin series for $\ln(1 + x)$ is", r"$\sum_{n=0}^\infty \frac{(-1)^n x^{n+1}}{n + 1}$", [r"$\sum_{n=0}^\infty \frac{x^{n+1}}{n + 1}$", r"$\sum_{n=0}^\infty (-1)^n x^n$", r"$\sum_{n=0}^\infty \frac{(-1)^n x^n}{n!}$"], "C", r"Integrate $\frac{1}{1 + x}$."),
        pick(r"The Maclaurin series for $\arctan x$ is", r"$\sum_{n=0}^\infty \frac{(-1)^n x^{2n+1}}{2n + 1}$", [r"$\sum_{n=0}^\infty \frac{(-1)^n x^{2n+1}}{(2n + 1)!}$", r"$\sum_{n=0}^\infty (-1)^n x^{2n}$", r"$\sum_{n=0}^\infty \frac{x^{2n+1}}{2n + 1}$"], "D", r"Integrate $\frac{1}{1 + x^2}$.", {r"$\sum_{n=0}^\infty \frac{(-1)^n x^{2n+1}}{(2n + 1)!}$": "that is $\\sin x$"}),
    ),
]

# ---------------------------------------------------------------- part B: calculator
_b1a = float(sum(sp.Rational((-1)**(k + 1), k**3) for k in range(1, 5)))
_b1b = float(sum(sp.Rational((-1)**k, sp.factorial(k)) for k in range(0, 5)))
_b2a = float(sp.Rational(1, 2) - sp.Rational(1, 24) + sp.Rational(1, 320))
_b2b = float(1 + sp.Rational(3, 10) + sp.Rational(9, 200) + sp.Rational(27, 6000))
_b3a = float(sp.Rational(30, 24) * sp.Rational(1, 5)**4)
_b3b = float(sp.Rational(12, 24) * sp.Rational(1, 2)**4)
_b4a = float(sp.log(sp.Rational(6, 5)) - (sp.Rational(1, 5) - sp.Rational(1, 50) + sp.Rational(1, 375)))
_b4b = float(sp.sin(sp.Rational(1, 2)) - (sp.Rational(1, 2) - sp.Rational(1, 48)))
f4 = lambda v: f"${v:.4f}$"
B = [
    Variants(
        pick(r"$S_4$ for $\sum_{n=1}^\infty \frac{(-1)^{n+1}}{n^3}$ is", f4(_b1a), [f4(_b1a + 1 / 125), r"$0.8750$", r"$1.0000$"], "B", rf"$1 - \frac18 + \frac{{1}}{{27}} - \frac{{1}}{{64}} \approx {_b1a:.4f}$.", calc=True),
        pick(r"The terms through $n = 4$ of $\sum_{n=0}^\infty \frac{(-1)^n}{n!}$ add to", f4(_b1b), [r"$0.3679$", r"$0.3333$", r"$0.4167$"], "C", rf"$1 - 1 + \frac12 - \frac16 + \frac{{1}}{{24}} = {_b1b:.4f}$.", {r"$0.3679$": "that is $\\frac1e$, the full sum"}, calc=True),
    ),
    Variants(
        pick(r"Using three nonzero terms of the series for $\int_0^x e^{-t^2}\,dt$, $\int_0^{0.5} e^{-t^2}\,dt \approx$", f4(_b2a), [r"$0.5000$", r"$0.4583$", r"$0.4794$"], "A", rf"$0.5 - \frac{{0.125}}{{3}} + \frac{{0.03125}}{{10}} \approx {_b2a:.4f}$.", calc=True),
        pick(r"The third-degree Maclaurin polynomial for $e^x$ gives $e^{0.3} \approx$", f4(_b2b), [r"$1.3000$", r"$1.3450$", r"$1.3499$"], "D", rf"$1 + 0.3 + 0.045 + 0.0045 = {_b2b:.4f}$.", {r"$1.3499$": "that is $e^{0.3}$ itself"}, calc=True),
    ),
    Variants(
        pick(r"$|f^{(4)}(x)| \le 30$ on $[1, 1.5]$. The Lagrange error bound for $P_3$ about $1$ at $x = 1.2$ is", f4(_b3a), [r"$0.0400$", r"$0.0080$", r"$0.0004$"], "D", rf"$\frac{{30}}{{4!}}(0.2)^4 = {_b3a:.4f}$.", calc=True),
        pick(r"$|f^{(4)}(x)| \le 12$ on $[1, 3]$. The Lagrange error bound for $P_3$ about $2$ at $x = 2.5$ is", f4(_b3b), [r"$0.1250$", r"$0.0156$", r"$0.0625$"], "A", rf"$\frac{{12}}{{4!}}(0.5)^4 = {_b3b:.4f}$.", calc=True),
    ),
    Variants(
        pick(r"$P_3(x) = (x - 1) - \frac12(x - 1)^2 + \frac13(x - 1)^3$ approximates $\ln x$. The actual error $|\ln 1.2 - P_3(1.2)|$ is about", f4(abs(_b4a)), [r"$0.0004$", r"$0.0200$", r"$0.1823$"], "C", rf"$|0.18232 - 0.18267| \approx {abs(_b4a):.4f}$, below the Lagrange bound $0.0004$.", calc=True),
        pick(r"The actual error $|\sin 0.5 - (0.5 - \frac{0.5^3}{6})|$ is about", f4(abs(_b4b)), [r"$0.0026$", r"$0.0208$", r"$0.4794$"], "B", rf"$|0.479426 - 0.479167| \approx {abs(_b4b):.4f}$.", {r"$0.0026$": "the Lagrange bound, not the actual error"}, calc=True),
    ),
]

# ---------------------------------------------------------------- FRQ 1: Taylor polynomial (from 10.12)
P3 = 2 - 3 * (x - 1) + 2 * (x - 1)**2 - 2 * (x - 1)**3
same("F1A", [P3.subs(x, sp.Rational(6, 5)), sp.Rational(30, 24) * sp.Rational(1, 5)**4], [sp.Rational(183, 125), sp.Rational(1, 500)])
F1A = FRQ("A Taylor polynomial", (r"$f$ has derivatives of all orders, with $f(1) = 2$, $f'(1) = -3$, $f''(1) = 4$, $f'''(1) = -12$, and $\left|f^{(4)}(x)\right| \le 30$ for $1 \le x \le 1.5$."), [
    Part("a", r"Write the third-degree Taylor polynomial for $f$ about $x = 1$.", selfcheck(r"2 - 3(x - 1) + 2(x - 1)^2 - 2(x - 1)^3"), r"Divide each derivative by its factorial.", [(1, "first two terms"), (1, "last two terms")], work="2.2cm"),
    Part("b", r"Use it to approximate $f(1.2)$.", num(sp.Rational(183, 125)), r"$2 - 0.6 + 0.08 - 0.016 = 1.464$.", [(1, "answer")], work="1.4cm"),
    Part("c", r"Use the Lagrange error bound to show that $|f(1.2) - P_3(1.2)| < 0.003$.", selfcheck(r"\tfrac{30}{4!}(0.2)^4 = 0.002 < 0.003"), r"$\frac{30}{24}(0.0016) = 0.002$.", [(1, "bound"), (1, "conclusion")], work="1.8cm"),
    Part("d", r"Write the second-degree Taylor polynomial for $f'$ about $x = 1$.", selfcheck(r"-3 + 4(x - 1) - 6(x - 1)^2"), r"Differentiate $P_3$.", [(1, "polynomial")], work="1.6cm"),
], frq_type="Taylor polynomial")
Q3 = 5 + 2 * (x - 2) - 3 * (x - 2)**2 + (x - 2)**3
same("F1B", [Q3.subs(x, sp.Rational(21, 10)), sp.Rational(18, 24) * sp.Rational(1, 10)**4], [sp.Rational(5171, 1000), sp.Rational(3, 40000)])
F1B = FRQ("A Taylor polynomial", (r"$h$ has derivatives of all orders, with $h(2) = 5$, $h'(2) = 2$, $h''(2) = -6$, $h'''(2) = 6$, and $\left|h^{(4)}(x)\right| \le 18$ for $2 \le x \le 2.5$."), [
    Part("a", r"Write the third-degree Taylor polynomial for $h$ about $x = 2$.", selfcheck(r"5 + 2(x - 2) - 3(x - 2)^2 + (x - 2)^3"), r"$\frac{-6}{2!} = -3$, $\frac{6}{3!} = 1$.", [(1, "first two terms"), (1, "last two terms")], work="2.2cm"),
    Part("b", r"Use it to approximate $h(2.1)$.", num(sp.Rational(5171, 1000)), r"$5 + 0.2 - 0.03 + 0.001 = 5.171$.", [(1, "answer")], work="1.4cm"),
    Part("c", r"Use the Lagrange error bound to show that $|h(2.1) - P_3(2.1)| < 0.0001$.", selfcheck(r"\tfrac{18}{4!}(0.1)^4 = 0.000075 < 0.0001"), r"$\frac{18}{24}(0.0001) = 0.000075$.", [(1, "bound"), (1, "conclusion")], work="1.8cm"),
    Part("d", r"Is $h$ increasing or decreasing at $x = 2$? Is its graph concave up or concave down there? Explain.", selfcheck(r"\text{increasing; concave down}"), r"$h'(2) = 2 > 0$; $h''(2) = -6 < 0$.", [(1, "both with reasons")], work="1.6cm"),
], frq_type="Taylor polynomial")

# ---------------------------------------------------------------- FRQ 2: Maclaurin series (from 10.14)
g = sp.sin(x) / x
same("F2A", [ser(g, 6), sp.integrate(1 - x**2 / 6, (x, 0, 1)), sp.integrate(x**4 / 120, (x, 0, 1))], [1 - x**2 / 6 + x**4 / 120, sp.Rational(17, 18), sp.Rational(1, 600)])
F2A = FRQ("A Maclaurin series", (r"Let $g(x) = \frac{\sin x}{x}$ for $x \ne 0$ and $g(0) = 1$."), [
    Part("a", r"Write the first three nonzero terms and the general term of the Maclaurin series for $g$.", selfcheck(r"1 - \frac{x^2}{6} + \frac{x^4}{120};\ \frac{(-1)^n x^{2n}}{(2n + 1)!}"), r"Divide the sine series by $x$.", [(1, "terms"), (1, "general term")], work="2cm"),
    Part("b", r"Find the interval of convergence. Justify your answer.", selfcheck(r"\text{all } x"), r"Ratio test: $\frac{x^2}{(2n + 3)(2n + 2)} \to 0$.", [(1, "ratio test"), (1, "conclusion")], work="2cm"),
    Part("c", r"Use the first two nonzero terms to approximate $\int_0^1 g(x)\,dx$.", num(sp.Rational(17, 18)), r"$1 - \frac{1}{18}$.", [(1, "answer")], work="1.6cm"),
    Part("d", r"Show that the approximation in part (c) is within $\frac{1}{500}$ of $\int_0^1 g(x)\,dx$.", selfcheck(r"\tfrac{1}{600} < \tfrac{1}{500}"), r"Alternating, decreasing terms: error $\le \frac{1}{600}$.", [(1, "AST error bound")], work="1.8cm"),
], frq_type="Taylor series")
h2 = sp.log(1 + x)
same("F2B", [ser(h2, 5), sp.integrate(x - x**2 / 2, (x, 0, sp.Rational(1, 2))), sp.integrate(x**3 / 3, (x, 0, sp.Rational(1, 2)))], [x - x**2 / 2 + x**3 / 3 - x**4 / 4, sp.Rational(5, 48), sp.Rational(1, 192)])
F2B = FRQ("A Maclaurin series", (r"Let $f(x) = \ln(1 + x)$."), [
    Part("a", r"Starting from the series for $\frac{1}{1 + x}$, write the first four nonzero terms and the general term of the Maclaurin series for $f$.", selfcheck(r"x - \frac{x^2}{2} + \frac{x^3}{3} - \frac{x^4}{4};\ \frac{(-1)^n x^{n+1}}{n + 1}"),
         r"Integrate $\sum (-1)^n x^n$ term by term; the constant is $0$ since $f(0) = 0$.", [(1, "terms"), (1, "general term")], work="2.2cm"),
    Part("b", r"Find the interval of convergence. Justify your answer, including the endpoints.", selfcheck(r"(-1, 1]"), r"$R = 1$; $x = 1$: alternating harmonic converges; $x = -1$: $-\sum \frac{1}{n + 1}$ diverges.", [(1, "radius"), (1, "endpoints")], work="2.2cm"),
    Part("c", r"Use the first two nonzero terms to approximate $\int_0^{1/2} f(x)\,dx$.", num(sp.Rational(5, 48)), r"$\int_0^{1/2} \left(x - \frac{x^2}{2}\right) dx = \frac18 - \frac{1}{48} = \frac{5}{48}$.", [(1, "answer")], work="1.8cm"),
    Part("d", r"Show that the approximation in part (c) differs from $\int_0^{1/2} f(x)\,dx$ by less than $0.006$.", selfcheck(r"\tfrac{1}{192} \approx 0.0052 < 0.006"), r"The integrated series alternates with decreasing terms; error $\le \int_0^{1/2} \frac{x^3}{3}\,dx = \frac{1}{192}$.", [(1, "AST error bound")], work="1.8cm"),
], frq_type="Taylor series")

# ---------------------------------------------------------------- FRQ 3: convergence and intervals
F3A = FRQ("Convergence", (r"Consider the series $\displaystyle\sum_{n=1}^\infty \frac{(x - 3)^n}{n \cdot 2^n}$."), [
    Part("a", r"Find the radius of convergence.", num(2), r"Ratio test: $L = \frac{|x - 3|}{2}$; $R = 2$.", [(1, "ratio test"), (1, "radius")], work="2cm"),
    Part("b", r"Find the interval of convergence. Justify your conclusions at the endpoints.", selfcheck(r"[1, 5)"), r"$x = 5$: harmonic diverges; $x = 1$: $\sum \frac{(-1)^n}{n}$ converges (AST).", [(1, "each endpoint"), (1, "interval")], work="2.4cm"),
    Part("c", r"Is the series absolutely convergent, conditionally convergent, or divergent at $x = 1$? Explain.", selfcheck(r"\text{conditionally convergent}"), r"$\sum \frac{(-1)^n}{n}$ converges but $\sum \frac1n$ diverges.", [(1, "classification with reason")], work="1.6cm"),
    Part("d", r"Use the alternating series error bound to bound the error in using the first three terms of the series at $x = 1$ to approximate its sum.", num(sp.Rational(1, 4)), r"The first omitted term has size $\frac14$.", [(1, "bound")], work="1.4cm"),
], frq_type="Series")
F3B = FRQ("Convergence", (r"Consider the series $\displaystyle\sum_{n=1}^\infty \frac{(x + 1)^n}{\sqrt n}$."), [
    Part("a", r"Find the radius of convergence.", num(1), r"Ratio test: $L = |x + 1|\sqrt{\frac{n}{n + 1}} \to |x + 1|$; $R = 1$.", [(1, "ratio test"), (1, "radius")], work="2cm"),
    Part("b", r"Find the interval of convergence. Justify your conclusions at the endpoints.", selfcheck(r"[-2, 0)"), r"$x = 0$: $\sum \frac{1}{\sqrt n}$ diverges ($p = \frac12$); $x = -2$: $\sum \frac{(-1)^n}{\sqrt n}$ converges (AST).", [(1, "each endpoint"), (1, "interval")], work="2.4cm"),
    Part("c", r"Is the series absolutely convergent, conditionally convergent, or divergent at $x = -2$? Explain.", selfcheck(r"\text{conditionally convergent}"), r"The alternating series converges but $\sum \frac{1}{\sqrt n}$ diverges.", [(1, "classification with reason")], work="1.6cm"),
    Part("d", r"How many terms of the series at $x = -2$ guarantee an error less than $0.1$?", num(100), r"$\frac{1}{\sqrt{n + 1}} < 0.1$ needs $n + 1 > 100$, so $n = 100$ terms (error $\le \frac{1}{\sqrt{101}}$); $n = 99$ gives exactly $0.1$, not less.", [(1, "answer")], work="1.8cm"),
], frq_type="Series")

TEST = UnitTest(unit=10, title="Infinite Sequences and Series", mcq_a=A, mcq_b=B,
                frq=[Variants(F1A, F1B), Variants(F2A, F2B), Variants(F3A, F3B)])
