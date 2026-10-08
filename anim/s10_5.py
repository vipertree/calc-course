"""Topic 10.5 (BC): Harmonic series and p-series. Narration comes from transcripts/10_5.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "10.5"

    def construct(self):
        with self.beat("The harmonic series grows forever") as b:
            r1 = M(r"1 + \tfrac12 + \tfrac13 + \tfrac14 + \tfrac15 + \tfrac16 + \tfrac17 + \tfrac18 + \cdots", 46).shift(UP * 2)
            self.play(Write(r1), run_time=1.2)
            b.line(1)
            r2 = M(r"1 + \tfrac12 + \left(\tfrac13 + \tfrac14\right) + \left(\tfrac15 + \tfrac16 + \tfrac17 + \tfrac18\right) + \cdots", 44).next_to(r1, DOWN, buff=0.6)
            self.play(Write(r2), run_time=1.2)
            unders = VGroup(M(r"\ge \tfrac12", 34, SECANT).next_to(r2, DOWN, buff=0.3).shift(LEFT * 0.6), M(r"\ge \tfrac12", 34, SECANT).next_to(r2, DOWN, buff=0.3).shift(RIGHT * 2.6))
            self.play(FadeIn(unders), run_time=0.8)
            b.line(2)
            sums = M(r"S_1 = 1,\ S_2 = 1.5,\ S_4 \ge 2,\ S_8 \ge 2.5,\ S_{16} \ge 3, \ \ldots", 38, TANGENT).next_to(unders, DOWN, buff=0.7)
            self.play(Write(sums), FadeIn(T("diverges", 40, TANGENT).next_to(sums, DOWN, buff=0.4)), run_time=1.2)
        self.clear()
        self.title()

        with self.beat("The p-series test") as b:
            box = formula_box(M(r"\sum_{n=1}^{\infty} \frac{1}{n^p}: \ \text{converges if } p > 1, \ \text{diverges if } p \le 1", 40, ACCUM).set_max_width(11), ACCUM).to_edge(UP, buff=0.6)
            self.play(FadeIn(box), run_time=1)
            b.line(1)
            why = M(r"\int_1^\infty x^{-p}\,dx = \left[\frac{x^{1-p}}{1 - p}\right]_1^\infty \ \text{finite iff } p > 1", 38).next_to(box, DOWN, buff=0.6)
            self.play(Write(why), run_time=1.2)
            b.line(2)
            line = NumberLine(x_range=[0, 3, 1], length=8, include_numbers=True, font_size=28, color=DIM).shift(DOWN * 2)
            div = Line(line.n2p(0), line.n2p(1), color=TANGENT, stroke_width=10)
            conv = Line(line.n2p(1), line.n2p(3), color=DERIV, stroke_width=10)
            self.play(Create(line), Create(div), Create(conv), FadeIn(Dot(line.n2p(1), color=TANGENT, radius=0.12)), FadeIn(T("diverges", 30, TANGENT).next_to(div, UP, buff=0.2)),
                      FadeIn(T("converges", 30, DERIV).next_to(conv, UP, buff=0.2)), FadeIn(M("p", 34).next_to(line, RIGHT, buff=0.2)), run_time=1.2)
        self.clear()

        line = NumberLine(x_range=[0, 3.5, 1], length=6, include_numbers=True, font_size=26, color=DIM)
        marks = [(1.01, "a", DERIV), (0.5, "b", TANGENT), (np.pi, "c", DERIV), (0.99, "d", TANGENT)]
        fig = VGroup(line, Line(line.n2p(0), line.n2p(1), color=TANGENT, stroke_width=6), Line(line.n2p(1), line.n2p(3.5), color=DERIV, stroke_width=6),
                     *[VGroup(Dot(line.n2p(v), color=c), M(l, 26, c).next_to(line.n2p(v), UP, buff=0.15 + 0.25 * (k % 2))) for k, (v, l, c) in enumerate(marks)])
        self.example("Classifying p-series", r"Classify each series: (a) $\sum \frac{1}{n^{1.01}}$ (b) $\sum \frac{1}{\sqrt n}$ (c) $\sum \frac{1}{n^\pi}$ (d) $\sum n^{-0.99}$.",
                     [r"\text{(a) } p = 1.01 > 1: \ \text{converges}", r"\text{(b) } \tfrac{1}{\sqrt n} = \tfrac{1}{n^{1/2}}, \ p = \tfrac12 \le 1: \ \text{diverges}", r"\text{(c) } p = \pi > 1: \ \text{converges}",
                      r"\text{(d) } n^{-0.99} = \tfrac{1}{n^{0.99}}, \ p = 0.99 \le 1: \ \text{diverges}"], at=[1, 2, 3, 4], figure=fig, figure_at=1, follow=True)

        with self.beat("Close") as b:
            card = VGroup(M(r"\text{harmonic } \sum \tfrac1n \text{ diverges}", 42, TANGENT), formula_box(M(r"\sum \frac{1}{n^p}: \ p > 1 \text{ converges}, \ p \le 1 \text{ diverges}", 42, ACCUM), ACCUM),
                          T("rewrite roots and negative exponents to read off $p$", 34)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: A constant multiple", r"Does $\displaystyle\sum_{n=1}^{\infty} \frac{3}{n^4}$ converge?", [r"3\sum \frac{1}{n^4}: \ p = 4 > 1", r"\text{converges}"], at=[1, 1])
        self.example("Example 2: Simplify first", r"Does $\displaystyle\sum_{n=1}^{\infty} \frac{n^2}{n^{3.5}}$ converge?", [r"\frac{n^2}{n^{3.5}} = \frac{1}{n^{1.5}}", r"p = 1.5 > 1: \ \text{converges}"], at=[1, 1])
        self.example("Example 3: A cube root", r"Does $\displaystyle\sum_{n=1}^{\infty} \frac{1}{\sqrt[3]{n^2}}$ converge?", [r"\sqrt[3]{n^2} = n^{2/3}", r"p = \tfrac23 \le 1: \ \text{diverges}"], at=[1, 1])
        self.finish()
