"""Topic 10.14 (BC): Taylor and Maclaurin series. Narration comes from transcripts/10_14.md."""
import math
import numpy as np
from manim import *

from kit import *
from style import *


# the series each worked example starts from stays boxed in the top right corner (Adder: formulas stay on screen)
EXP_REF = r"e^u = \sum_{n=0}^{\infty} \frac{u^n}{n!}"
COS_REF = r"\cos x = \sum_{n=0}^{\infty} \frac{(-1)^n x^{2n}}{(2n)!}"
SIN_REF = r"\sin u = \sum_{n=0}^{\infty} \frac{(-1)^n u^{2n+1}}{(2n + 1)!}"
TAYLOR_REF = r"f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!}(x - a)^n"


class Lesson(TranscriptScene):
    NUM = "10.14"

    def construct(self):
        with self.beat("From polynomials to series") as b:
            # Adder (2026-10-14): connect to 10.11-10.13. Before, a few terms made an estimate; now infinitely many terms
            # give exact, elegant formulas for common functions
            ax, al = plot_axes([-3, 3, 1], [-1, 12, 2], w=6.2, h=4.6)
            VGroup(ax, al).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(np.exp, x_range=[-3, 2.45], color=FUNC, stroke_width=5)), run_time=1)
            cols = [SECANT, DERIV, ACCUM, TANGENT]
            Ps = []
            for k, deg in enumerate((1, 2, 4, 8)):
                P = lambda s, d=deg: sum(s**j / math.factorial(j) for j in range(d + 1))
                xs = [t for t in np.linspace(-3, 2.6, 561) if -1 <= P(t) <= 12]       # stay inside the window
                Ps.append(ax.plot(P, x_range=[xs[0], xs[-1]], color=cols[k], stroke_width=3))
            est = VGroup(T("a few terms: an estimate", 34, SECANT), M(r"P_3(0.1) = 1.105167", 36), M(r"e^{0.1} \approx 1.105171", 36, FUNC),
                         M(r"\text{error} \le 0.000005", 34, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.6).shift(UP * 0.3)
            self.play(Create(Ps[0]), Create(Ps[1]), FadeIn(est[0]), run_time=1.2)
            self.play(LaggedStart(*[FadeIn(m) for m in est[1:]], lag_ratio=0.4), run_time=1.6)
            b.line(1)
            self.play(Create(Ps[2]), run_time=0.9)
            self.play(Create(Ps[3]), run_time=0.9)
            b.line(2)
            inf = VGroup(T("infinitely many terms:", 34, ACCUM), M(r"e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots", 36, ACCUM),
                         T("for every $x$", 32, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(est, aligned_edge=LEFT)
            inf.set_max_width(6.4)
            self.play(FadeOut(est), FadeIn(inf), run_time=1)
            b.line(3)
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.6)
            row1 = VGroup(T(r"10.11 \textperiodcentered{} a Taylor polynomial: a few terms", 32, SECANT),
                          M(r"e^x \approx 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!}", 40), T("an estimate, with an error", 30, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            row2 = VGroup(T(r"10.14 \textperiodcentered{} the Taylor series: infinitely many terms", 32, ACCUM),
                          M(r"e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots = \sum_{n=0}^{\infty} \frac{x^n}{n!}", 40, ACCUM), T("exact, for every $x$", 30, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            rows = VGroup(row1, row2).arrange(DOWN, aligned_edge=LEFT, buff=0.7).to_edge(UP, buff=0.6)
            self.play(FadeIn(row1), run_time=0.8)
            self.play(FadeIn(row2), run_time=1)
            b.line(4)
            fams = M(r"e^x, \quad \sin x, \quad \cos x, \quad \frac{1}{1 - x}", 40, FUNC).next_to(rows, DOWN, buff=0.7)
            self.play(Write(fams), run_time=1.2)
        self.clear()
        self.title()

        with self.beat("Four series to know by heart") as b:
            rows = VGroup(M(r"e^x = 1 + x + \tfrac{x^2}{2!} + \tfrac{x^3}{3!} + \cdots = \sum \tfrac{x^n}{n!}, \ \text{all } x", 34),
                          M(r"\sin x = x - \tfrac{x^3}{3!} + \tfrac{x^5}{5!} - \cdots = \sum \tfrac{(-1)^n x^{2n+1}}{(2n + 1)!}, \ \text{all } x", 34),
                          M(r"\cos x = 1 - \tfrac{x^2}{2!} + \tfrac{x^4}{4!} - \cdots = \sum \tfrac{(-1)^n x^{2n}}{(2n)!}, \ \text{all } x", 34),
                          M(r"\tfrac{1}{1 - x} = 1 + x + x^2 + \cdots = \sum x^n, \ -1 < x < 1", 34)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(UP, buff=0.6)
            self.play(FadeIn(rows[0]), run_time=0.8)
            b.line(1)
            b.line(2)
            self.play(FadeIn(rows[1]), FadeIn(rows[2]), run_time=1.2)
            b.line(3)
            self.play(FadeIn(rows[3]), run_time=0.8)
            tips = T("sine: odd powers, starts with $x$; cosine: even powers, starts with $1$; both alternate", 28, DIM).to_edge(DOWN, buff=0.4)
            self.play(FadeIn(tips), run_time=0.6)
        self.clear()

        self.example("New series from old", r"Find the Maclaurin series for $e^{-x^2}$: the first four nonzero terms and the general term.",
                     [r"e^u = 1 + u + \tfrac{u^2}{2!} + \tfrac{u^3}{3!} + \cdots", r"u = -x^2", r"e^{-x^2} = 1 + (-x^2) + \tfrac{(-x^2)^2}{2!} + \tfrac{(-x^2)^3}{3!} + \cdots", r"= 1 - x^2 + \tfrac{x^4}{2} - \tfrac{x^6}{6} + \cdots",
                      r"\text{general term: } \tfrac{(-x^2)^n}{n!} = \tfrac{(-1)^n x^{2n}}{n!}", r"e^{-x^2} = \sum_{n=0}^{\infty} \tfrac{(-1)^n x^{2n}}{n!}, \ \text{all } x"], at=[1, 1, 2, 3, 4, 4], follow=True,
                     ref=EXP_REF)

        with self.beat("Close") as b:
            card = VGroup(T("know $e^x$, $\\sin x$, $\\cos x$, $\\frac{1}{1 - x}$ and their intervals", 34), T("substitute, multiply by powers of $x$, or differentiate/integrate (10.15)", 34, SECANT),
                          M(r"\text{about } a: \ \sum \frac{f^{(n)}(a)}{n!}(x - a)^n", 40, ACCUM)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Multiply by x", r"Find the Maclaurin series for $x\cos x$.", [r"\cos x = 1 - \tfrac{x^2}{2!} + \tfrac{x^4}{4!} - \cdots", r"x\cos x = x - \tfrac{x^3}{2!} + \tfrac{x^5}{4!} - \cdots", r"= \sum \tfrac{(-1)^n x^{2n+1}}{(2n)!}"], at=[1, 1, 2], ref=COS_REF)
        self.example("Example 2: Substitute 3x", r"Find the first three nonzero terms and the general term of the Maclaurin series for $\sin(3x)$.",
                     [r"\sin u = u - \tfrac{u^3}{3!} + \tfrac{u^5}{5!} - \cdots, \ u = 3x", r"= 3x - \tfrac{27x^3}{6} + \tfrac{243x^5}{120} - \cdots", r"= 3x - \tfrac92x^3 + \tfrac{81}{40}x^5 - \cdots", r"\text{general term: } \tfrac{(-1)^n (3x)^{2n+1}}{(2n + 1)!}"], at=[1, 1, 2, 3], ref=SIN_REF)
        self.example("Example 3: A Taylor series not at zero", r"Find the Taylor series for $e^x$ about $x = 1$.", [r"f^{(n)}(x) = e^x, \ f^{(n)}(1) = e", r"e^x = \sum_{n=0}^{\infty} \frac{e(x - 1)^n}{n!} = e + e(x - 1) + \frac{e(x - 1)^2}{2!} + \cdots"], at=[1, 2], ref=TAYLOR_REF)
        self.finish()
