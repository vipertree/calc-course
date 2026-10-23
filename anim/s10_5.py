"""Topic 10.5 (BC): Harmonic series and p-series. Narration comes from transcripts/10_5.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "10.5"

    def construct(self):
        with self.beat("The harmonic series grows forever") as b:
            # Adder (2026-10-14): show a graph of the harmonic series' values. One dot per n, never a curve
            head = M(r"1 + \tfrac12 + \tfrac13 + \tfrac14 + \cdots", 48).to_edge(UP, buff=0.4)
            ax, al = plot_axes([0, 42, 5], [0, 4.6, 1], w=10.4, h=5.0, xlabel="n", ylabel="")
            VGroup(ax, al).next_to(head, DOWN, buff=0.35).set_x(-0.2)
            self.play(Write(head), FadeIn(ax), FadeIn(al), run_time=1.2)
            terms = VGroup(*[Dot(ax.c2p(k, 1 / k), radius=0.05, color=DERIV) for k in range(1, 41)])
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in terms], lag_ratio=0.08), run_time=2.4)
            t_lab = T(r"the sequence: $\frac1n \to 0$", 32, DERIV).next_to(ax.c2p(40, 0), UP, buff=0.55).shift(LEFT * 1.2)
            self.play(FadeIn(t_lab), run_time=0.6)
            b.line(1)
            sums, tot = [], 0.0
            for k in range(1, 41):
                tot += 1 / k
                sums.append(Dot(ax.c2p(k, tot), radius=0.055, color=TANGENT))
            sums = VGroup(*sums)
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in sums], lag_ratio=0.1), run_time=3.2)
            s_lab = T(r"the series: $S_n$", 32, TANGENT).move_to(ax.c2p(9, 4.1))
            last = M(r"S_{40} \approx 4.28", 32, TANGENT).next_to(sums[-1], DOWN, buff=0.5).shift(LEFT * 0.4)
            self.play(FadeIn(s_lab), FadeIn(last), Indicate(sums[-1], scale_factor=2), run_time=1)
            b.line(2)
            self.play(Indicate(sums, color=TANGENT, scale_factor=1.15), run_time=1.2)
        self.clear()

        with self.beat("Grouping the terms") as b:
            r1 = M(r"1 + \tfrac12 + \tfrac13 + \tfrac14 + \tfrac15 + \tfrac16 + \tfrac17 + \tfrac18 + \cdots", 46).shift(UP * 2)
            r2 = M(r"1 + \tfrac12 + \left(\tfrac13 + \tfrac14\right) + \left(\tfrac15 + \tfrac16 + \tfrac17 + \tfrac18\right) + \cdots", 44).next_to(r1, DOWN, buff=0.6)
            self.play(FadeIn(r1), run_time=0.6)
            self.play(Write(r2), run_time=1.2)
            unders = VGroup(M(r"\ge \tfrac12", 34, SECANT).next_to(r2, DOWN, buff=0.3).shift(LEFT * 0.6), M(r"\ge \tfrac12", 34, SECANT).next_to(r2, DOWN, buff=0.3).shift(RIGHT * 2.6))
            self.play(FadeIn(unders), run_time=0.8)
            b.line(1)
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

        # the test stays up in the corner through the worked examples (Adder: formulas stay on screen)
        self.example_ref = r"\begin{aligned}&\textstyle\sum \frac{1}{n^p}\text{ converges if } p > 1,\\ &\text{diverges if } p \le 1\end{aligned}"
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
