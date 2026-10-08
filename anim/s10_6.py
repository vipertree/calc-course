"""Topic 10.6 (BC): Comparison tests. Narration comes from transcripts/10_6.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "10.6"

    def construct(self):
        with self.beat("Smaller than something finite") as b:
            def bars(big, small, col_big, col_small, lab_big, lab_small, scale):
                g = VGroup()
                for k in range(1, 9):
                    hb, hs = big(k) * scale, small(k) * scale
                    g.add(VGroup(Rectangle(width=0.4, height=hb, stroke_width=0, fill_color=col_big, fill_opacity=0.5).move_to([0.55 * k, hb / 2, 0]),
                                 Rectangle(width=0.4, height=hs, stroke_width=0, fill_color=col_small, fill_opacity=0.9).move_to([0.55 * k, hs / 2, 0])))
                return VGroup(g, M(lab_big, 28, col_big).next_to(g, UP, buff=0.15), M(lab_small, 28, col_small).next_to(g, DOWN, buff=0.15))
            p1 = bars(lambda k: 1 / k**2, lambda k: 1 / (k**2 + 3), DERIV, ACCUM, r"b_n = \tfrac{1}{n^2}\ (\text{finite sum})", r"a_n = \tfrac{1}{n^2 + 3}", 2.2)
            p2 = bars(lambda k: np.log(k + 2) / (k + 2), lambda k: 1 / (k + 2), SECANT, TANGENT, r"\tfrac{\ln n}{n}", r"\tfrac1n\ (\text{infinite sum})", 4.0)
            VGroup(p1, p2).arrange(RIGHT, buff=1.2)
            self.play(FadeIn(p1), run_time=1.2)
            b.line(1)
            self.play(FadeIn(p2), run_time=1.2)
            b.line(2)
        self.clear()
        self.title()

        with self.beat("Direct comparison") as b:
            box = formula_box(VGroup(M(r"0 \le a_n \le b_n:", 38), M(r"\sum b_n \text{ converges},\ \text{so}\ \sum a_n \text{ converges}", 36), M(r"\sum a_n \text{ diverges},\ \text{so}\ \sum b_n \text{ diverges}", 36)).arrange(DOWN, buff=0.2), ACCUM).to_edge(UP, buff=0.6)
            self.play(FadeIn(box), run_time=1.2)
            b.line(1)
            words = T("smaller than convergent: converges; bigger than divergent: diverges", 32).next_to(box, DOWN, buff=0.5)
            self.play(FadeIn(words), run_time=0.8)
            b.line(2)
            self.play(FadeIn(T("smaller than divergent, or bigger than convergent: no conclusion", 32, TANGENT).next_to(words, DOWN, buff=0.4)), run_time=0.8)
        self.clear()

        self.example("A direct comparison", r"Does $\displaystyle\sum_{n=1}^{\infty} \frac{1}{n^2 + 3}$ converge?",
                     [r"n^2 + 3 > n^2, \ \text{so} \ \frac{1}{n^2 + 3} < \frac{1}{n^2}", r"\sum \frac{1}{n^2} \text{ converges } (p = 2)", r"TEXT:By direct comparison, $\sum \frac{1}{n^2 + 3}$ converges."], at=[1, 2, 3])

        with self.beat("Limit comparison") as b:
            box = formula_box(M(r"a_n, b_n > 0, \ \lim \frac{a_n}{b_n} = c, \ 0 < c < \infty: \ \text{same behavior}", 38, ACCUM).set_max_width(11), ACCUM).to_edge(UP, buff=0.5)
            self.play(FadeIn(box), run_time=1)
            b.line(1)
            rows = VGroup(M(r"\sum \frac{2n + 1}{n^3 - n + 5}: \ b_n = \frac{n}{n^3} = \frac{1}{n^2}", 38), M(r"\lim \frac{(2n + 1)/(n^3 - n + 5)}{1/n^2} = \lim \frac{2n^3 + n^2}{n^3 - n + 5} = 2", 38),
                          M(r"0 < 2 < \infty, \ \sum \tfrac{1}{n^2} \text{ converges: converges}", 38, ACCUM)).arrange(DOWN, buff=0.45).next_to(box, DOWN, buff=0.6)
            self.play(Write(rows[0]), run_time=1)
            b.line(2)
            self.play(Write(rows[1]), run_time=1.2)
            b.line(3)
            self.play(Write(rows[2]), run_time=1)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(T("direct: smaller than convergent converges; bigger than divergent diverges", 32), T("limit: $\\lim \\frac{a_n}{b_n} = c$, $0 < c < \\infty$: same behavior", 34, ACCUM),
                          T("compare with $p$-series or geometric series; build $b_n$ from the dominant terms", 30, DIM)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Bigger than harmonic", r"Does $\displaystyle\sum_{n=3}^{\infty} \frac{\ln n}{n}$ converge?", [r"n \ge 3: \ \ln n > 1, \ \text{so} \ \frac{\ln n}{n} > \frac1n", r"\sum \tfrac1n \text{ diverges}", r"\text{diverges by direct comparison}"], at=[1, 2, 2])
        self.example("Example 2: A bounded numerator", r"Does $\displaystyle\sum_{n=1}^{\infty} \frac{\sin^2 n}{n^2}$ converge?", [r"0 \le \sin^2 n \le 1, \ \text{so} \ 0 \le \frac{\sin^2 n}{n^2} \le \frac{1}{n^2}", r"\sum \tfrac{1}{n^2} \text{ converges}", r"\text{converges by direct comparison}"], at=[1, 2, 2])
        self.example("Example 3: Limit comparison with a geometric series", r"Does $\displaystyle\sum_{n=1}^{\infty} \frac{1}{2^n - 1}$ converge?",
                     [r"b_n = \frac{1}{2^n}", r"TEXT:Direct comparison goes the wrong way: $\frac{1}{2^n - 1} > \frac{1}{2^n}$.", r"\lim \frac{1/(2^n - 1)}{1/2^n} = \lim \frac{2^n}{2^n - 1} = 1", r"0 < 1 < \infty, \ \sum \tfrac{1}{2^n} \text{ converges: converges}"], at=[1, 1, 2, 3])
        self.finish()
