"""Topic 10.7 (BC): Alternating series test. Narration comes from transcripts/10_7.md."""
import numpy as np
from manim import *

from kit import *
from props import Frog
from style import *


class Lesson(TranscriptScene):
    NUM = "10.7"

    def construct(self):
        with self.beat("Two steps forward, one step back") as b:
            # Adder (2026-10-14): a real-looking frog, actually animated, slower, leaving a trail of its path (props.Frog)
            line = NumberLine(x_range=[0, 1.1, 0.25], length=11, include_numbers=True, decimal_number_config={"num_decimal_places": 2}, font_size=24, color=DIM).shift(DOWN * 2.3)
            frog = Frog(line.n2p(0), height=0.85)
            self.add(frog.trail)
            self.play(Create(line), FadeIn(frog), run_time=0.8)
            sums, s = [], 0.0
            for k in range(1, 9):
                s += (-1)**(k + 1) / k
                sums.append(s)
            hop_col = lambda k: DERIV if k % 2 else FUNC          # rightward hops one color, leftward the other
            for k in range(1, 5):
                frog.hop(self, line.n2p(sums[k - 1]), run_time=1.8, peak=max(abs(sums[k - 1] - (sums[k - 2] if k > 1 else 0)) * 10 / 3, 1.0), color=hop_col(k), trail_opacity=0.8)
            b.line(1)
            row = M(r"S_1 = 1,\ \ S_2 = 0.5,\ \ S_3 \approx 0.83,\ \ S_4 \approx 0.58,\ \ \ldots", 36).move_to(UP * 2.35)
            self.play(LaggedStart(*[FadeIn(part) for part in row[0]], lag_ratio=0.04), run_time=2.4)
            b.line(2)
            for k, rt in zip(range(5, 9), [1.8, 1.7, 1.6, 1.5]):
                frog.hop(self, line.n2p(sums[k - 1]), run_time=rt, peak=1.0, color=hop_col(k), trail_opacity=0.8)     # arcs clear the frog
            x2 = line.n2p(np.log(2))
            self.play(Create(DashedLine(x2 + DOWN * 0.15, x2 + UP * 3.4, color=ACCUM)), FadeIn(M(r"\approx 0.69", 32, ACCUM).next_to(x2 + UP * 3.4, UP, buff=0.12)),
                      frog.sit.animate.set_opacity(0.45), run_time=1)      # the frog steps back so its trail shows
            b.line(3)
            self.play(FadeIn(M(r"1 - \tfrac12 + \tfrac13 - \tfrac14 + \cdots", 42).to_edge(UP, buff=0.35)), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("The test") as b:
            box = formula_box(VGroup(M(r"\sum (-1)^{n+1} b_n, \ b_n > 0, \ \text{converges if}", 38), M(r"\text{(1) } b_{n+1} \le b_n \ \text{(decreasing)} \quad \text{(2) } \lim b_n = 0", 36)).arrange(DOWN, buff=0.2), ACCUM).to_edge(UP, buff=0.6)
            self.play(FadeIn(box), run_time=1)
            b.line(1)
            b.line(2)
            line = NumberLine(x_range=[0.4, 1.05, 0.1], length=10, color=DIM).shift(DOWN * 1.4)
            s, prev = 0.0, None
            brackets = VGroup()
            for k in range(1, 7):
                s_new = s + (-1)**(k + 1) / k
                if prev is not None:
                    lo, hi = sorted([s, s_new])
                    brackets.add(Line(line.n2p(lo), line.n2p(hi), color=SECANT, stroke_width=6).shift(UP * 0.18 * k))
                prev, s = s, s_new
            self.play(Create(line), LaggedStart(*[Create(br) for br in brackets], lag_ratio=0.3), run_time=1.6)
            b.line(3)
            self.play(FadeIn(T("terms alternate in sign, shrink in size, and go to zero", 32).to_edge(DOWN, buff=0.4)), run_time=0.8)
        self.clear()

        # the alternating series test stays up in the corner through the worked examples (Adder: formulas stay on screen)
        self.example_ref = r"\begin{aligned}&\textstyle\sum (-1)^{n+1} b_n,\ b_n > 0\text{,}\\ &\text{converges if } b_n \text{ is decreasing}\\ &\text{and } \lim b_n = 0\end{aligned}"
        self.example("The alternating harmonic series", r"Show that $\displaystyle\sum_{n=1}^{\infty} \frac{(-1)^{n+1}}{n}$ converges.",
                     [r"b_n = \tfrac1n > 0", r"b_{n+1} = \tfrac{1}{n + 1} < \tfrac1n = b_n: \ \text{decreasing}", r"\lim \tfrac1n = 0", r"TEXT:By the alternating series test, the series converges.", r"\text{(its sum is } \ln 2 \approx 0.693)"], at=[1, 2, 3, 3, 3], follow=True)

        with self.beat("When the test fails") as b:
            r1 = M(r"\sum (-1)^n \frac{n}{n + 1}: \ b_n = \frac{n}{n + 1} \to 1 \ne 0", 40).shift(UP * 1.4)
            self.play(Write(r1), run_time=1)
            self.play(FadeIn(T("diverges by the $n$th term test", 34, TANGENT).next_to(r1, DOWN, buff=0.4)), run_time=0.8)
            b.line(1)
            self.play(FadeIn(T("$b_n \\to 0$ but not decreasing: the alternating series test is inconclusive", 32, DIM).shift(DOWN * 1.2)), run_time=0.8)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(T("$\\sum (-1)^n b_n$, $b_n > 0$: converges if $b_n$ is decreasing and $b_n \\to 0$", 34, ACCUM), T("state both conditions", 34), T("$b_n \\not\\to 0$: diverges ($n$th term test)", 34, TANGENT)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Root of n", r"Does $\displaystyle\sum_{n=1}^{\infty} \frac{(-1)^n}{\sqrt n}$ converge?", [r"b_n = \tfrac{1}{\sqrt n}: \ \text{positive, decreasing, } \to 0", r"\text{converges by the alternating series test}"], at=[1, 1])
        self.example("Example 2: Sizes that don't shrink to zero", r"Does $\displaystyle\sum_{n=1}^{\infty} (-1)^n \frac{2n}{n + 3}$ converge?", [r"b_n = \tfrac{2n}{n + 3} \to 2 \ne 0", r"\text{diverges by the } n\text{th term test}"], at=[1, 1], ref=r"\begin{aligned}&n\text{th term test:}\\ &\lim a_n \ne 0\text{, so}\\ &\textstyle\sum a_n \text{ diverges}\end{aligned}")
        self.example("Example 3: A log in the denominator", r"Does $\displaystyle\sum_{n=2}^{\infty} \frac{(-1)^n}{\ln n}$ converge?",
                     [r"b_n = \tfrac{1}{\ln n} > 0 \text{ for } n \ge 2", r"\ln n \text{ increases, so } b_n \text{ decreases}", r"\lim \tfrac{1}{\ln n} = 0", r"\text{converges by the alternating series test}"], at=[1, 1, 2, 2])
        self.finish()
