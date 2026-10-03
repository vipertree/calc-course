"""Topic 10.4 (BC): The integral test. Narration comes from transcripts/10_4.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "10.4"

    def construct(self):
        f = lambda s: 2.4 / s
        with self.beat("Rectangles and a curve") as b:
            ax, al = plot_axes([0, 8.5, 1], [0, 2.8, 1], w=8, h=4)
            VGroup(ax, al).shift(DOWN * 0.3)
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(f, x_range=[0.9, 8.4], color=FUNC, stroke_width=4)), run_time=1)
            rects = riemann_boxes(ax, f, list(range(1, 9)), kind="left", color=SECANT, opacity=0.4)
            self.play(LaggedStart(*[FadeIn(r) for r in rects], lag_ratio=0.1), run_time=1.4)
            b.line(1)
            self.play(FadeIn(region(ax, f, lambda s: 0, 1, 8.4, opacity=0.3)), run_time=0.8)
            self.play(FadeIn(T("series = rectangles; integral = area under the curve", 30).to_edge(UP, buff=0.4)), run_time=0.6)
            b.line(2)
        self.clear()
        self.title()

        with self.beat("The test and why it works") as b:
            def pic(kind):
                ax, _ = plot_axes([0, 7.5, 1], [0, 2.8, 1], w=4.6, h=2.8)
                return VGroup(ax, riemann_boxes(ax, f, list(range(1, 8)), kind=kind, color=SECANT, opacity=0.4), ax.plot(f, x_range=[0.9, 7.4], color=FUNC, stroke_width=4))
            p1, p2 = pic("right"), pic("left")
            VGroup(p1, p2).arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.5)
            l1 = M(r"\sum_{n=2}^{\infty} f(n) \le \int_1^\infty f(x)\,dx", 32).next_to(p1, DOWN, buff=0.2)
            l2 = M(r"\int_1^\infty f(x)\,dx \le \sum_{n=1}^{\infty} f(n)", 32).next_to(p2, DOWN, buff=0.2)
            self.play(FadeIn(p1), FadeIn(l1), run_time=1)
            b.line(1)
            self.play(FadeIn(p2), FadeIn(l2), run_time=1)
            b.line(2)
            box = formula_box(T(r"$f$ positive, continuous, decreasing, $a_n = f(n)$: $\sum a_n$ and $\int_1^\infty f(x)\,dx$ both converge or both diverge", 30, ACCUM).set_max_width(11), ACCUM).to_edge(DOWN, buff=0.4)
            self.play(FadeIn(box), run_time=1)
            b.line(3)
        self.clear()

        self.example("Using the integral test", r"Use the integral test to decide whether $\displaystyle\sum_{n=1}^{\infty} \frac{n}{n^2 + 1}$ converges.",
                     [r"f(x) = \frac{x}{x^2 + 1}", r"TEXT:Positive for $x \ge 1$; continuous.", r"f'(x) = \frac{1 - x^2}{(x^2 + 1)^2} \le 0 \text{ for } x \ge 1: \ \text{decreasing}",
                      r"\int_1^\infty \frac{x}{x^2 + 1}\,dx = \lim_{b\to\infty} \tfrac12\ln(x^2 + 1)\Big|_1^b", r"= \lim_{b\to\infty} \tfrac12\left[\ln(b^2 + 1) - \ln 2\right] = \infty", r"TEXT:The integral diverges, so the series diverges."],
                     at=[1, 1, 2, 3, 4, 5])

        with self.beat("Close") as b:
            card = VGroup(T("$f$ positive, continuous, decreasing; $a_n = f(n)$", 36), T("$\\sum a_n$ and $\\int f(x)\\,dx$ behave the same", 36, ACCUM), T("the integral's value is not the series' sum", 34, TANGENT)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: One over n squared", r"Does $\displaystyle\sum_{n=1}^{\infty} \frac{1}{n^2}$ converge?",
                     [r"f(x) = \tfrac{1}{x^2}: \ \text{positive, continuous, decreasing}", r"\int_1^\infty x^{-2}\,dx = \lim_{b\to\infty}\left[-\tfrac1x\right]_1^b = 1", r"\text{converges}", r"\text{(the sum is } \tfrac{\pi^2}{6} \approx 1.645\text{, not } 1)"], at=[1, 2, 2, 3])
        self.example("Example 2: An exponential times n", r"Does $\displaystyle\sum_{n=1}^{\infty} ne^{-n^2}$ converge?",
                     [r"f(x) = xe^{-x^2}: \ f' = e^{-x^2}\left(1 - 2x^2\right) < 0 \text{ for } x \ge 1", r"\int_1^\infty xe^{-x^2}\,dx = \lim\left[-\tfrac12 e^{-x^2}\right]_1^b = \tfrac{1}{2e}", r"\text{converges}"], at=[1, 2, 3])
        self.example("Example 3: n ln n", r"Does $\displaystyle\sum_{n=2}^{\infty} \frac{1}{n\ln n}$ converge?",
                     [r"f(x) = \tfrac{1}{x\ln x}: \ \text{positive, continuous, decreasing for } x \ge 2", r"\int_2^\infty \frac{dx}{x\ln x} = \lim\left[\ln(\ln x)\right]_2^b = \infty", r"\text{diverges}"], at=[1, 2, 3])
        self.finish()
