"""Topic 10.14 (BC): Taylor and Maclaurin series. Narration comes from transcripts/10_14.md."""
import math
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "10.14"

    def construct(self):
        with self.beat("From polynomials to series") as b:
            ax, al = plot_axes([-3, 3, 1], [-1, 12, 2], w=7, h=4.6)
            VGroup(ax, al).shift(DOWN * 0.3)
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(np.exp, x_range=[-3, 2.45], color=FUNC, stroke_width=5)), run_time=1)
            cols = [SECANT, DERIV, ACCUM, TANGENT]
            for k, deg in enumerate((1, 2, 4, 8)):
                P = lambda s, d=deg: sum(s**j / math.factorial(j) for j in range(d + 1))
                self.play(Create(ax.plot(P, x_range=[-3, 2.6], color=cols[k], stroke_width=3)), run_time=0.7)
            b.line(1)
            self.play(FadeIn(M(r"e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots", 40, ACCUM).to_edge(UP, buff=0.3)), run_time=1)
            b.line(2)
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
                      r"\text{general term: } \tfrac{(-x^2)^n}{n!} = \tfrac{(-1)^n x^{2n}}{n!}", r"e^{-x^2} = \sum_{n=0}^{\infty} \tfrac{(-1)^n x^{2n}}{n!}, \ \text{all } x"], at=[1, 1, 2, 3, 4, 4], follow=True)

        with self.beat("Close") as b:
            card = VGroup(T("know $e^x$, $\\sin x$, $\\cos x$, $\\frac{1}{1 - x}$ and their intervals", 34), T("substitute, multiply by powers of $x$, or differentiate/integrate (10.15)", 34, SECANT),
                          M(r"\text{about } a: \ \sum \frac{f^{(n)}(a)}{n!}(x - a)^n", 40, ACCUM)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Multiply by x", r"Find the Maclaurin series for $x\cos x$.", [r"\cos x = 1 - \tfrac{x^2}{2!} + \tfrac{x^4}{4!} - \cdots", r"x\cos x = x - \tfrac{x^3}{2!} + \tfrac{x^5}{4!} - \cdots", r"= \sum \tfrac{(-1)^n x^{2n+1}}{(2n)!}"], at=[1, 1, 2])
        self.example("Example 2: Substitute 3x", r"Find the first three nonzero terms and the general term of the Maclaurin series for $\sin(3x)$.",
                     [r"\sin u = u - \tfrac{u^3}{3!} + \tfrac{u^5}{5!} - \cdots, \ u = 3x", r"= 3x - \tfrac{27x^3}{6} + \tfrac{243x^5}{120} - \cdots", r"= 3x - \tfrac92x^3 + \tfrac{81}{40}x^5 - \cdots", r"\text{general term: } \tfrac{(-1)^n (3x)^{2n+1}}{(2n + 1)!}"], at=[1, 1, 2, 3])
        self.example("Example 3: A Taylor series not at zero", r"Find the Taylor series for $e^x$ about $x = 1$.", [r"f^{(n)}(x) = e^x, \ f^{(n)}(1) = e", r"e^x = \sum_{n=0}^{\infty} \frac{e(x - 1)^n}{n!} = e + e(x - 1) + \frac{e(x - 1)^2}{2!} + \cdots"], at=[1, 2])
        self.finish()
