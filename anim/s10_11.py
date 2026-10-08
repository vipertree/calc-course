"""Topic 10.11 (BC): Taylor polynomials. Narration comes from transcripts/10_11.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "10.11"

    def construct(self):
        with self.beat("Better than a tangent line") as b:
            ax, al = plot_axes([0, 3, 1], [-1.6, 1.4, 1], w=7, h=4.6)
            VGroup(ax, al).shift(DOWN * 0.2)
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(np.log, x_range=[0.2, 3], color=FUNC, stroke_width=5)), run_time=1)
            P = [lambda s: s - 1, lambda s: (s - 1) - (s - 1)**2 / 2, lambda s: (s - 1) - (s - 1)**2 / 2 + (s - 1)**3 / 3]
            cols = [SECANT, DERIV, ACCUM]
            labs = [r"P_1", r"P_2", r"P_3"]
            g = ax.plot(P[0], x_range=[0.2, 2.6], color=cols[0], stroke_width=3)
            self.play(Create(g), FadeIn(M(labs[0], 30, cols[0]).next_to(ax.c2p(2.6, 1.6 - 0.1), LEFT, buff=0.1)), run_time=1)
            b.line(1)
            for k in (1, 2):
                self.play(Create(ax.plot(P[k], x_range=[0.2, 2.6], color=cols[k], stroke_width=3)), FadeIn(M(labs[k], 30, cols[k]).next_to(ax.c2p(2.6, P[k](2.6)), RIGHT, buff=0.1)), run_time=1)
            b.line(2)
        self.clear()
        self.title()

        with self.beat("The Taylor polynomial formula") as b:
            box = formula_box(M(r"P_n(x) = f(a) + f'(a)(x - a) + \frac{f''(a)}{2!}(x - a)^2 + \cdots + \frac{f^{(n)}(a)}{n!}(x - a)^n", 36, ACCUM).set_max_width(12), ACCUM).to_edge(UP, buff=0.6)
            self.play(FadeIn(box), run_time=1.2)
            b.line(1)
            r1 = M(r"\text{coefficient of } (x - a)^k: \ \frac{f^{(k)}(a)}{k!}", 40).next_to(box, DOWN, buff=0.5)
            r2 = M(r"\frac{d^3}{dx^3}\left[c(x - a)^3\right] = 3!\,c", 36, SECANT).next_to(r1, DOWN, buff=0.4)
            self.play(Write(r1), run_time=1)
            self.play(Write(r2), run_time=1)
            b.line(2)
            self.play(FadeIn(T("centered at $a = 0$: a Maclaurin polynomial", 32, DIM).next_to(r2, DOWN, buff=0.5)), run_time=0.8)
        self.clear()

        tab = table(["k", r"f^{(k)}(x)", r"f^{(k)}(1)", r"\tfrac{f^{(k)}(1)}{k!}"], [["0", r"\ln x", "0", "0"], ["1", r"\tfrac1x", "1", "1"], ["2", r"-\tfrac{1}{x^2}", "-1", r"-\tfrac12"], ["3", r"\tfrac{2}{x^3}", "2", r"\tfrac13"]], size=30)
        self.example("ln x near 1", r"Find the third-degree Taylor polynomial for $f(x) = \ln x$ centered at $x = 1$, and use it to approximate $\ln 1.2$.",
                     [r"f(1) = \ln 1 = 0", r"f'(x) = \tfrac1x: \ 1; \quad f''(x) = -\tfrac{1}{x^2}: \ -1; \quad f'''(x) = \tfrac{2}{x^3}: \ 2", r"\text{coefficients: } 0, \ 1, \ -\tfrac12, \ \tfrac26 = \tfrac13",
                      r"P_3(x) = (x - 1) - \tfrac12(x - 1)^2 + \tfrac13(x - 1)^3", r"P_3(1.2) = 0.2 - \tfrac12(0.04) + \tfrac13(0.008)", r"\approx 0.182667", r"\text{(} \ln 1.2 \approx 0.182322\text{)}"],
                     at=[1, 2, 3, 4, 5, 5, 6], figure=tab, figure_at=1, follow=True)

        with self.beat("Close") as b:
            card = VGroup(M(r"P_n(x) = \sum_{k=0}^{n} \frac{f^{(k)}(a)}{k!}(x - a)^k", 44, ACCUM), T("coefficient of $(x - a)^k$: $\\frac{f^{(k)}(a)}{k!}$", 34), T("make a table: derivative, value at $a$, divide by $k!$", 34, SECANT)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: e to the x", r"Find the third-degree Maclaurin polynomial for $e^x$, and use it to approximate $e^{0.1}$.",
                     [r"f^{(k)}(x) = e^x, \ f^{(k)}(0) = 1", r"P_3(x) = 1 + x + \tfrac{x^2}{2} + \tfrac{x^3}{6}", r"P_3(0.1) = 1 + 0.1 + 0.005 + 0.000167 \approx 1.105167", r"\text{(} e^{0.1} \approx 1.105171\text{)}"], at=[1, 2, 3, 3])
        self.example("Example 2: cosine", r"Find the fourth-degree Maclaurin polynomial for $\cos x$.",
                     [r"\cos, \ -\sin, \ -\cos, \ \sin, \ \cos", r"\text{at } 0: \ 1, \ 0, \ -1, \ 0, \ 1", r"P_4(x) = 1 - \tfrac{x^2}{2!} + \tfrac{x^4}{4!} = 1 - \tfrac{x^2}{2} + \tfrac{x^4}{24}"], at=[1, 1, 2])
        self.example("Example 3: From a table of values", r"$f(2) = 3$, $f'(2) = -1$, $f''(2) = 4$, $f'''(2) = 6$. Find the third-degree Taylor polynomial for $f$ about $x = 2$ and approximate $f(2.1)$.",
                     [r"P_3(x) = 3 - (x - 2) + \tfrac{4}{2!}(x - 2)^2 + \tfrac{6}{3!}(x - 2)^3", r"= 3 - (x - 2) + 2(x - 2)^2 + (x - 2)^3", r"P_3(2.1) = 3 - 0.1 + 0.02 + 0.001 = 2.921"], at=[1, 2, 3])
        self.finish()
