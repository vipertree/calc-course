"""Topic 6.3: Riemann sums, summation notation, and definite integral notation.

CED: LIM-5.B (LIM-5.B.1, LIM-5.B.2), LIM-5.C (LIM-5.C.1, LIM-5.C.2): write Riemann sums in sigma notation; the definite
integral is the limit of Riemann sums as the number of subintervals goes to infinity; translate between a limit of a
Riemann sum and a definite integral. Worked examples: evaluate a sum, a limit to an integral, an integral by geometry.
AP asks this topic as multiple choice only, so FRQS is empty.
"""
import sympy as sp

from calclib import (VideoExample, MCQ, BigIdea, Check, Formula, Item, Section, Text, Topic, Variants, Video, close, num, same, selfcheck)

x, n, k = sp.symbols("x n k", positive=True)


def lim_sum(term, N=20000):
    """lim_{n->oo} sum_{k=1}^{n} term(k, n), estimated numerically with n = N (checked against integrals with close())."""
    f = sp.lambdify(k, term.subs(n, N), "math")
    return sum(f(j) for j in range(1, N + 1))


close("lesson", lim_sum((1 + 2 * k / n)**2 * 2 / n), float(sp.integrate(x**2, (x, 1, 3))), 1e-3)
same("ex", [sum((sp.Rational(2 * j, 4))**3 * sp.Rational(1, 2) for j in range(1, 5)), sp.integrate(sp.sqrt(4 - x**2), (x, -2, 2))], [sp.Rational(25, 4), 2 * sp.pi])

NOTES = [
    Video("s6_3.py::Lesson", "Sums and integrals", 5),

    Section("Sigma notation"),
    Formula("Summation notation", (
        r"\[ \sum_{k=1}^{n} a_k = a_1 + a_2 + \cdots + a_n. \] The \blank{counter} $k$ starts at the bottom number and goes up to the top number; "
        r"for each value, work out the expression and add.")),
    Text(r"$\displaystyle\sum_{k=1}^{4} (2k + 1) = 3 + 5 + 7 + 9 = 24$."),
    Formula("A right Riemann sum in sigma notation", (
        r"With $n$ equal pieces of $[a, b]$: $\Delta x = \dfrac{b - a}{n}$, the right end of piece $k$ is $x_k = a + k\,\Delta x$, and "
        r"\[ R_n = \sum_{k=1}^{n} f(x_k)\,\Delta x = \sum_{k=1}^{n} f\left(a + k\,\frac{b - a}{n}\right)\frac{b - a}{n}. \]")),

    Section("The definite integral"),
    Formula("Definite integral", (
        r"\[ \int_a^b f(x)\,dx = \lim_{n\to\infty} \sum_{k=1}^{n} f(x_k)\,\Delta x. \] "
        r"$a$ and $b$ are the \blank{limits of integration}, $f(x)$ is the \blank{integrand}, and $dx$ stands for a tiny width. "
        r"If $f \ge 0$, the integral is the exact area under the graph from $a$ to $b$.")),
    Text(r"\textbf{From a limit to an integral.} Find $\Delta x$ (so $b - a$), read $a$ from $x_k = a + k\,\Delta x$, then see what is done to $x_k$: that's $f$."),
    VideoExample('From sum to integral', work="2.4cm"),
    Text(r"\textbf{Geometry.} When the region is a familiar shape, its area gives the integral: $\int_{-2}^{2} \sqrt{4 - x^2}\,dx$ is half a circle of radius $2$, so it equals $2\pi$."),
    BigIdea(r"$\Sigma$ means add up. A Riemann sum adds $f(x_k)\,\Delta x$; the definite integral is the limit of those sums as $n \to \infty$."),
    Check(r"Evaluate $\displaystyle\sum_{k=1}^{3} k^2$.", num(14), r"$1 + 4 + 9 = 14$."),
]

# ---------------------------------------------------------------- practice
PRACTICE = [
    Item(r"Evaluate $\displaystyle\sum_{k=1}^{5} (3k - 1)$.", num(40), r"$2 + 5 + 8 + 11 + 14 = 40$.", work="1.2cm"),
    Item(r"Evaluate $\displaystyle\sum_{k=0}^{3} 2^k$.", num(15), r"$1 + 2 + 4 + 8 = 15$.", work="1.2cm"),
    Item(r"Evaluate $\displaystyle\sum_{k=1}^{4} \frac{k}{2} \cdot \frac12$, a right Riemann sum for $f(x) = x$ on $[0, 2]$.", num(sp.Rational(5, 2)),
         r"$\frac12\left(\frac12 + 1 + \frac32 + 2\right) = \frac12(5) = 2.5$.", work="1.4cm"),
    Item(r"Write the right Riemann sum for $f(x) = x^2$ on $[0, 3]$ with $n$ equal subintervals in sigma notation.",
         selfcheck(r"\sum_{k=1}^{n} \left(\frac{3k}{n}\right)^2 \frac3n"), r"$\Delta x = \frac3n$, $x_k = \frac{3k}{n}$: $\sum_{k=1}^{n} \left(\frac{3k}{n}\right)^2 \frac3n$.", work="1.6cm"),
    Item(r"Write the right Riemann sum for $f(x) = \sqrt x$ on $[1, 5]$ with $n$ equal subintervals in sigma notation.",
         selfcheck(r"\sum_{k=1}^{n} \sqrt{1 + \frac{4k}{n}} \cdot \frac4n"), r"$\Delta x = \frac4n$, $x_k = 1 + \frac{4k}{n}$.", work="1.6cm"),
    Item(r"Write $\displaystyle\lim_{n\to\infty} \sum_{k=1}^{n} \left(\frac{5k}{n}\right)^3 \frac5n$ as a definite integral.", selfcheck(r"\int_0^5 x^3\,dx"),
         r"$\Delta x = \frac5n$, $x_k = \frac{5k}{n}$ so $a = 0$, $b = 5$, $f(x) = x^3$.", work="1.4cm"),
    Item(r"Write $\displaystyle\lim_{n\to\infty} \sum_{k=1}^{n} \cos\left(2 + \frac{3k}{n}\right) \frac3n$ as a definite integral.", selfcheck(r"\int_2^5 \cos x\,dx"),
         r"$\Delta x = \frac3n$, $x_k = 2 + \frac{3k}{n}$, so $a = 2$, $b = 5$, $f(x) = \cos x$.", work="1.4cm"),
    Item(r"Write $\displaystyle\lim_{n\to\infty} \sum_{k=1}^{n} \frac{1}{1 + \frac{k}{n}} \cdot \frac1n$ as a definite integral.", selfcheck(r"\int_1^2 \frac1x\,dx"),
         r"$\Delta x = \frac1n$, $x_k = 1 + \frac kn$, so $a = 1$, $b = 2$, $f(x) = \frac1x$.", work="1.4cm"),
    Item(r"Evaluate $\displaystyle\int_0^4 3\,dx$ using geometry.", num(12), r"A rectangle: height $3$, width $4$.", work="1cm"),
    Item(r"Evaluate $\displaystyle\int_0^6 \frac x2\,dx$ using geometry.", num(9), r"A triangle: base $6$, height $3$: $\frac12(6)(3) = 9$.", work="1.2cm"),
    Item(r"Evaluate $\displaystyle\int_{-3}^{3} \sqrt{9 - x^2}\,dx$ using geometry.", num(sp.Rational(9, 2) * sp.pi), r"Half a circle of radius $3$: $\frac12\pi(9) = \frac{9\pi}{2}$.", work="1.2cm"),
    Item(r"Evaluate $\displaystyle\int_0^2 \sqrt{4 - x^2}\,dx$ using geometry.", num(sp.pi), r"A quarter circle of radius $2$: $\frac14\pi(4) = \pi$.", work="1.2cm"),
]
same("p", [sum(3 * j - 1 for j in range(1, 6)), sum(sp.Rational(j, 2) * sp.Rational(1, 2) for j in range(1, 5)),
           sp.integrate(sp.sqrt(9 - x**2), (x, -3, 3)), sp.integrate(sp.sqrt(4 - x**2), (x, 0, 2))], [40, sp.Rational(5, 2), 9 * sp.pi / 2, sp.pi])
close("p lim1", lim_sum((5 * k / n)**3 * 5 / n), 625 / 4, 0.1)
close("p lim2", lim_sum(sp.cos(2 + 3 * k / n) * 3 / n), float(sp.sin(5) - sp.sin(2)), 1e-3)
close("p lim3", lim_sum(1 / (1 + k / n) / n), float(sp.log(2)), 1e-3)

# ---------------------------------------------------------------- quiz
QUIZ = [
    Variants(
        Item(r"Evaluate $\displaystyle\sum_{k=1}^{4} (k + 2)$.", num(18), r"$3 + 4 + 5 + 6 = 18$.", work="1cm"),
        Item(r"Evaluate $\displaystyle\sum_{k=1}^{3} (2k)^2$.", num(56), r"$4 + 16 + 36 = 56$.", work="1cm"),
        Item(r"Evaluate $\displaystyle\sum_{k=2}^{5} (10 - k)$.", num(26), r"$8 + 7 + 6 + 5 = 26$.", work="1cm"),
    ),
    Variants(
        MCQ(r"$\displaystyle\lim_{n\to\infty} \sum_{k=1}^{n} \left(\frac{2k}{n}\right)^2 \frac2n = $", [r"$\int_0^1 x^2\,dx$", r"$\int_0^2 x^2\,dx$", r"$\int_0^2 2x^2\,dx$", r"$\int_1^2 x^2\,dx$"], "B",
            r"$\Delta x = \frac2n$, $x_k = \frac{2k}{n}$: $a = 0$, $b = 2$."),
        MCQ(r"$\displaystyle\lim_{n\to\infty} \sum_{k=1}^{n} \left(3 + \frac{k}{n}\right)^2 \frac1n = $", [r"$\int_0^1 x^2\,dx$", r"$\int_3^4 x^2\,dx$", r"$\int_0^3 x^2\,dx$", r"$\int_3^4 (3 + x)^2\,dx$"], "B",
            r"$\Delta x = \frac1n$, $x_k = 3 + \frac kn$: $a = 3$, $b = 4$, $f(x) = x^2$."),
        MCQ(r"$\displaystyle\lim_{n\to\infty} \sum_{k=1}^{n} e^{4k/n} \cdot \frac4n = $", [r"$\int_0^4 e^x\,dx$", r"$\int_0^1 e^{4x}\,dx$", r"$\int_0^4 e^{4x}\,dx$", r"$\int_1^4 e^x\,dx$"], "A",
            r"$\Delta x = \frac4n$, $x_k = \frac{4k}{n}$: $a = 0$, $b = 4$, $f(x) = e^x$."),
    ),
    Variants(
        Item(r"Evaluate $\displaystyle\int_1^5 2\,dx$ using geometry.", num(8), r"Rectangle: $2 \times 4$.", work="1cm"),
        Item(r"Evaluate $\displaystyle\int_0^4 x\,dx$ using geometry.", num(8), r"Triangle: $\frac12(4)(4)$.", work="1cm"),
        Item(r"Evaluate $\displaystyle\int_0^2 (x + 1)\,dx$ using geometry.", num(4), r"Trapezoid: $\frac{1 + 3}{2}(2)$.", work="1cm"),
    ),
    Variants(
        Item(r"Evaluate $\displaystyle\int_{-1}^{1} \sqrt{1 - x^2}\,dx$ using geometry.", num(sp.pi / 2), r"Half a unit circle: $\frac\pi2$.", work="1cm"),
        Item(r"Evaluate $\displaystyle\int_0^5 \sqrt{25 - x^2}\,dx$ using geometry.", num(sp.Rational(25, 4) * sp.pi), r"Quarter circle of radius $5$: $\frac{25\pi}{4}$.", work="1cm"),
        Item(r"Evaluate $\displaystyle\int_{-4}^{4} \sqrt{16 - x^2}\,dx$ using geometry.", num(8 * sp.pi), r"Half a circle of radius $4$: $8\pi$.", work="1cm"),
    ),
    Variants(
        MCQ(r"For $f(x) = x^2$ on $[0, 4]$ with $n$ equal subintervals, the right Riemann sum is", [r"$\sum_{k=1}^{n} \left(\frac{4k}{n}\right)^2 \frac4n$",
            r"$\sum_{k=1}^{n} \left(\frac kn\right)^2 \frac4n$", r"$\sum_{k=1}^{n} \left(\frac{4k}{n}\right)^2 \frac1n$", r"$\sum_{k=0}^{n-1} \left(\frac{4k}{n}\right)^2 \frac4n$"], "A",
            r"$\Delta x = \frac4n$ and $x_k = \frac{4k}{n}$, $k = 1, \dots, n$.", why_not={"D": "that's the left sum"}),
        MCQ(r"For $f(x) = x^3$ on $[1, 3]$ with $n$ equal subintervals, the right Riemann sum is", [r"$\sum_{k=1}^{n} \left(\frac{2k}{n}\right)^3 \frac2n$",
            r"$\sum_{k=1}^{n} \left(1 + \frac{2k}{n}\right)^3 \frac2n$", r"$\sum_{k=1}^{n} \left(1 + \frac{k}{n}\right)^3 \frac1n$", r"$\sum_{k=1}^{n} \left(1 + \frac{2k}{n}\right)^3 \frac1n$"], "B",
            r"$\Delta x = \frac2n$ and $x_k = 1 + \frac{2k}{n}$."),
        MCQ(r"For $f(x) = \sin x$ on $[0, \pi]$ with $n$ equal subintervals, the right Riemann sum is", [r"$\sum_{k=1}^{n} \sin\left(\frac{k}{n}\right) \frac\pi n$",
            r"$\sum_{k=1}^{n} \sin\left(\frac{\pi k}{n}\right) \frac1n$", r"$\sum_{k=1}^{n} \sin\left(\frac{\pi k}{n}\right) \frac\pi n$", r"$\sum_{k=1}^{n} \sin(\pi k) \frac\pi n$"], "C",
            r"$\Delta x = \frac\pi n$ and $x_k = \frac{\pi k}{n}$."),
    ),
]
same("q", [sum(j + 2 for j in range(1, 5)), sum((2 * j)**2 for j in range(1, 4)), sum(10 - j for j in range(2, 6))], [18, 56, 26])

# ---------------------------------------------------------------- test prep
MCQS = [
    MCQ(r"$\displaystyle\lim_{n\to\infty} \sum_{k=1}^{n} \sqrt{1 + \frac{3k}{n}} \cdot \frac3n$ is equal to", [r"$\int_0^3 \sqrt x\,dx$", r"$\int_1^4 \sqrt x\,dx$",
        r"$\int_1^3 \sqrt x\,dx$", r"$\int_0^1 \sqrt{1 + 3x}\,dx$"], "B", r"$\Delta x = \frac3n$, $x_k = 1 + \frac{3k}{n}$: $a = 1$, $b = 4$."),
    MCQ(r"Which of the following is a right Riemann sum for $\int_2^6 \ln x\,dx$ with $n$ equal subintervals?", [r"$\sum_{k=1}^{n} \ln\left(\frac{4k}{n}\right)\frac4n$",
        r"$\sum_{k=1}^{n} \ln\left(2 + \frac{k}{n}\right)\frac4n$", r"$\sum_{k=1}^{n} \ln\left(2 + \frac{4k}{n}\right)\frac1n$", r"$\sum_{k=1}^{n} \ln\left(2 + \frac{4k}{n}\right)\frac4n$"], "D",
        r"$\Delta x = \frac{6 - 2}{n} = \frac4n$, $x_k = 2 + \frac{4k}{n}$."),
    MCQ(r"$\displaystyle\int_{-3}^{3} \left(2 + \sqrt{9 - x^2}\right) dx = $", [r"$12 + \frac{9\pi}{2}$", r"$12 + 9\pi$", r"$6 + \frac{9\pi}{2}$", r"$\frac{9\pi}{2}$"], "A",
        r"A $6 \times 2$ rectangle, area $12$, plus half a circle of radius $3$, area $\frac{9\pi}{2}$."),
    MCQ(r"$\displaystyle\sum_{k=1}^{4} \frac{k^2}{16} \cdot \frac14$ is a right Riemann sum for $f(x) = x^2$ on $[0, 1]$. Its value is", [r"$\frac13$", r"$\frac{15}{32}$",
        r"$\frac{7}{32}$", r"$\frac{15}{16}$"], "B",
        r"$\frac{1 + 4 + 9 + 16}{64} = \frac{30}{64} = \frac{15}{32}$.", why_not={"A": "the exact area"}),
]
same("m", [sp.integrate(2 + sp.sqrt(9 - x**2), (x, -3, 3)), sum(sp.Rational(j**2, 16) / 4 for j in range(1, 5))], [12 + 9 * sp.pi / 2, sp.Rational(15, 32)])
close("m lim", lim_sum(sp.sqrt(1 + 3 * k / n) * 3 / n), float(sp.integrate(sp.sqrt(x), (x, 1, 4))), 1e-3)

FRQS = []

TOPIC = Topic(
    number="6.3", title="Riemann Sums, Summation Notation, and Definite Integral Notation",
    unit="Unit 6: Integration and Accumulation of Change", ced=["LIM-5.B", "LIM-5.B.1", "LIM-5.B.2", "LIM-5.C", "LIM-5.C.1", "LIM-5.C.2"],
    goals=r"Write Riemann sums in sigma notation and translate between the limit of a Riemann sum and a definite integral.",
    notes=NOTES, practice=PRACTICE, quiz=QUIZ, mcq=MCQS, frq=FRQS)
