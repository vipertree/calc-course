"""Topic 10.1 (BC): Convergent and divergent series. Narration comes from transcripts/10_1.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "10.1"

    def construct(self):
        with self.beat("Adding forever") as b:
            choc, choc_dk = "#7B4B2A", "#5A341C"
            bar = Rectangle(width=8, height=1.2, stroke_color=choc_dk, stroke_width=4, fill_color=choc, fill_opacity=1).shift(UP * 1.6)
            self.play(FadeIn(bar), run_time=0.8)
            line = NumberLine(x_range=[0, 1, 0.25], length=8, include_numbers=True, decimal_number_config={"num_decimal_places": 2}, font_size=24, color=DIM).shift(DOWN * 1.2)
            self.play(Create(line), run_time=0.8)
            left = 0.0
            pieces = VGroup()
            totals = VGroup()
            for k in range(1, 6):
                w = 0.5**k
                piece = Rectangle(width=8 * w, height=1.2, stroke_color=choc_dk, stroke_width=2, fill_color=choc, fill_opacity=1).move_to(bar.get_left() + RIGHT * 8 * (left + w / 2))
                piece.align_to(bar, UP)
                seg = Line(line.n2p(left), line.n2p(left + w), color=SECANT, stroke_width=8)
                left += w
                tot = M(f"{left:.4g}", 30, SECANT).next_to(line.n2p(left), UP, buff=0.3 + 0.25 * (k % 2))
                self.play(piece.animate.set_fill(SECANT, 0.8), Create(seg), FadeIn(tot), run_time=0.6)
                pieces.add(piece)
            b.line(1)
            self.play(FadeIn(M(r"\tfrac12 + \tfrac14 + \tfrac18 + \cdots = \ ?", 44).to_edge(UP, buff=0.3)), run_time=0.8)
            b.line(2)
        self.clear()
        self.title()

        with self.beat("Partial sums") as b:
            rows = VGroup(M(r"\sum_{n=1}^{\infty} a_n = a_1 + a_2 + a_3 + \cdots", 46), M(r"S_n = a_1 + a_2 + \cdots + a_n", 46, SECANT),
                          M(r"\text{converges to } S \text{ if } \lim_{n\to\infty} S_n = S; \ \text{otherwise diverges}", 38, ACCUM), T("keep a running total; if it settles on a number, that's the sum", 32, DIM)).arrange(DOWN, buff=0.45)
            self.play(Write(rows[0]), run_time=1)
            b.line(1)
            self.play(Write(rows[1]), run_time=1)
            b.line(2)
            self.play(Write(rows[2]), run_time=1)
            b.line(3)
            self.play(FadeIn(rows[3]), run_time=0.6)
        self.clear()

        with self.beat("Three ways to behave") as b:
            def panel(vals, yr, lab, color):
                ax, _ = plot_axes([0, 9, 2], yr, w=3.6, h=2.8, coords=False, xlabel="n", ylabel="S_n")
                dots = VGroup(*[Dot(ax.c2p(k, v), color=color, radius=0.07) for k, v in enumerate(vals, start=1)])
                return VGroup(ax, dots, T(lab, 26, color).next_to(ax, DOWN, buff=0.25))
            p1 = panel(list(range(1, 9)), [0, 9, 2], "$\\sum 1$: diverges to $\\infty$", TANGENT)
            p2 = panel([1, 0, 1, 0, 1, 0, 1, 0], [-0.5, 1.5, 1], "$\\sum (-1)^{n+1}$: no single value", TANGENT)
            p3 = panel([1 - 0.5**k for k in range(1, 9)], [0, 1.2, 0.5], "$\\sum (\\frac12)^n$: converges to $1$", DERIV)
            VGroup(p1, p2, p3).arrange(RIGHT, buff=0.4)
            self.play(FadeIn(p1), run_time=1)
            b.line(1)
            self.play(FadeIn(p2), run_time=1)
            b.line(2)
            self.play(FadeIn(p3), run_time=1)
        self.clear()

        self.example("A telescoping series", r"Find the sum of $\displaystyle\sum_{n=1}^{\infty} \frac{1}{n(n + 1)}$.",
                     [r"\frac{1}{n(n + 1)} = \frac1n - \frac{1}{n + 1}", r"S_n = \left(1 - \tfrac12\right) + \left(\tfrac12 - \tfrac13\right) + \left(\tfrac13 - \tfrac14\right) + \cdots + \left(\tfrac1n - \tfrac{1}{n + 1}\right)",
                      r"TEXT:The middle terms cancel in pairs.", r"S_n = 1 - \frac{1}{n + 1}", r"\lim_{n\to\infty} S_n = 1", r"TEXT:The series converges to $1$."], at=[1, 2, 3, 3, 4, 4], follow=True)

        with self.beat("Close") as b:
            card = VGroup(M(r"S_n = a_1 + \cdots + a_n", 44, SECANT), T("converges to $S$ if $S_n \\to S$; otherwise diverges", 36), T("telescoping: terms cancel, leaving the first and last", 34, DIM)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Partial sums that grow", r"Does $\displaystyle\sum_{n=1}^{\infty} 2$ converge?", [r"S_n = 2 + 2 + \cdots + 2 = 2n", r"\lim_{n\to\infty} 2n = \infty: \ \text{diverges}"], at=[1, 1])
        self.example("Example 2: A partial sum from a formula", r"The $n$th partial sum of a series is $S_n = \frac{3n}{n + 1}$. Does the series converge? If so, to what?",
                     [r"\lim_{n\to\infty} \frac{3n}{n + 1} = 3", r"\text{converges to } 3", r"a_1 = S_1 = \tfrac32"], at=[1, 1, 2])
        self.example("Example 3: Another telescoping sum", r"Find $\displaystyle\sum_{n=1}^{\infty} \left(\frac1n - \frac{1}{n + 2}\right)$.",
                     [r"S_n = \left(1 - \tfrac13\right) + \left(\tfrac12 - \tfrac14\right) + \left(\tfrac13 - \tfrac15\right) + \cdots", r"S_n = 1 + \tfrac12 - \tfrac{1}{n + 1} - \tfrac{1}{n + 2}", r"\lim S_n = \tfrac32"], at=[1, 2, 3])
        self.finish()
