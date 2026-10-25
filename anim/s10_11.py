"""Topic 10.11 (BC): Taylor polynomials. Narration comes from transcripts/10_11.md."""
import math

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

        with self.beat("Building a polynomial at a") as b:
            # Adder (2026-10-14): slow down before "centered at a". A curve, a point a, and the polynomial built there one
            # derivative at a time (value, slope, concavity, ...), each hugging the curve over a wider stretch
            f = lambda s: 2 + np.sin(s - 2.2)
            A = 2.9          # each degree hugs a wider stretch here (within 0.12: 0.3, 1.3, 2.0, 3.1 wide)
            d = [f(A), np.cos(A - 2.2), -np.sin(A - 2.2), -np.cos(A - 2.2)]
            polys = [lambda s, k=k: sum(d[j] / math.factorial(j) * (s - A)**j for j in range(k + 1)) for k in range(4)]
            ax, al = plot_axes([0, 6.2, 1], [0, 4.4, 1], w=6.8, h=4.6, coords=False)
            VGroup(ax, al).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
            curve = ax.plot(f, x_range=[0, 6.2], color=FUNC, stroke_width=5)
            fl = M("y = f(x)", 30, FUNC).next_to(ax.c2p(0.7, f(0.7)), UP, buff=0.3)
            pt = Dot(ax.c2p(A, f(A)), radius=0.09, color=INK)
            drop = DashedLine(ax.c2p(A, 0), ax.c2p(A, f(A)), color=DIM, stroke_width=2, dash_length=0.1)
            alab = M("a", 32).next_to(ax.c2p(A, 0), DOWN, buff=0.15)
            self.play(FadeIn(ax), FadeIn(al), Create(curve), FadeIn(fl), run_time=1.2)
            self.play(Create(drop), FadeIn(pt), FadeIn(alab), run_time=0.8)

            def span(P):
                """the stretch around a where P stays inside the window"""
                xs = np.linspace(0, 6.2, 621)
                ok = [(0.05 <= P(x) <= 4.35) for x in xs]
                i = int(np.argmin(np.abs(xs - A)))
                lo = hi = i
                while lo > 0 and ok[lo - 1]:
                    lo -= 1
                while hi < len(xs) - 1 and ok[hi + 1]:
                    hi += 1
                return [xs[lo], xs[hi]]
            cols = [TANGENT, SECANT, DERIV, ACCUM]
            words = [r"$P_0$: matches $f(a)$", r"$P_1$: also matches $f'(a)$", r"$P_2$: also matches $f''(a)$", r"$P_3$: also matches $f'''(a)$"]
            labs = VGroup(*[T(w, 32, c) for w, c in zip(words, cols)]).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.5).shift(UP * 0.6)
            graphs = []
            for k in range(4):
                b.line(k + 1)
                g = ax.plot(polys[k], x_range=span(polys[k]), color=cols[k], stroke_width=4)
                graphs.append(g)
                self.play(Create(g), FadeIn(labs[k], shift=LEFT * 0.2), *([graphs[k - 1].animate.set_stroke(opacity=0.35)] if k else []), run_time=1.4)
            # the stretch where the cubic stays within 0.1 of the curve
            xs = np.linspace(0, 6.2, 621)
            near = [x for x in xs if abs(polys[3](x) - f(x)) < 0.12]
            close_br = BraceBetweenPoints(ax.c2p(min(near), 0), ax.c2p(max(near), 0), DOWN, color=ACCUM).shift(DOWN * 0.45)
            self.play(FadeIn(close_br), run_time=0.8)
            b.line(5)
            means = VGroup(T("value: where the curve is", 30, TANGENT), T("$f'$: which way it's heading", 30, SECANT), T("$f''$: how it bends", 30, DERIV),
                           T("$f'''$: how the bending changes", 30, ACCUM)).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(labs, aligned_edge=LEFT)
            self.play(FadeOut(labs), FadeIn(means), run_time=1)
            b.line(6)
            easy = T("polynomials: only adding and multiplying", 30, DIM).next_to(means, DOWN, buff=0.7).align_to(means, LEFT)
            self.play(FadeIn(easy), run_time=0.8)
        self.clear()

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

        # the formula stays boxed in the top right corner through the worked examples (Adder: formulas stay on screen)
        self.example_ref = r"P_n(x) = \sum_{k=0}^{n} \frac{f^{(k)}(a)}{k!}(x - a)^k"
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
