"""Topic 10.15 (BC): Representing functions as power series. Narration comes from transcripts/10_15.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "10.15"

    def construct(self):
        with self.beat("Calculus on a series") as b:
            mid = M(r"\frac{1}{1 - x} = 1 + x + x^2 + x^3 + \cdots", 42)
            self.play(Write(mid), run_time=1)
            b.line(1)
            up = M(r"\frac{1}{(1 - x)^2} = 1 + 2x + 3x^2 + \cdots", 38, DERIV).shift(UP * 2.4)
            dn = M(r"-\ln(1 - x) = x + \frac{x^2}{2} + \frac{x^3}{3} + \cdots", 38, ACCUM).shift(DOWN * 2.4)
            a1 = Arrow(mid.get_top(), up.get_bottom(), buff=0.15, color=DERIV)
            a2 = Arrow(mid.get_bottom(), dn.get_top(), buff=0.15, color=ACCUM)
            self.play(GrowArrow(a1), FadeIn(M(r"\tfrac{d}{dx}", 32, DERIV).next_to(a1, RIGHT, buff=0.1)), Write(up), run_time=1.2)
            self.play(GrowArrow(a2), FadeIn(M(r"\int", 36, ACCUM).next_to(a2, RIGHT, buff=0.1)), Write(dn), run_time=1.2)
            b.line(2)
        self.clear()
        self.title()

        with self.beat("Term by term") as b:
            r0 = M(r"f(x) = \sum c_n (x - a)^n, \ |x - a| < R", 42).to_edge(UP, buff=0.7)
            box = formula_box(VGroup(M(r"f'(x) = \sum n\,c_n (x - a)^{n-1}", 42), M(r"\int f(x)\,dx = C + \sum \frac{c_n (x - a)^{n+1}}{n + 1}", 42)).arrange(DOWN, buff=0.35), ACCUM).next_to(r0, DOWN, buff=0.5)
            self.play(Write(r0), FadeIn(box), run_time=1.4)
            b.line(1)
            self.play(FadeIn(VGroup(T("same radius $R$", 34, DERIV), T("endpoints can change: check them again", 34, TANGENT)).arrange(DOWN, buff=0.3).next_to(box, DOWN, buff=0.5)), run_time=0.8)
        self.clear()

        line = NumberLine(x_range=[-2, 2, 1], length=5, include_numbers=True, font_size=24, color=DIM)
        fig = VGroup(line, Line(line.n2p(-1), line.n2p(1), color=DERIV, stroke_width=8), Circle(radius=0.11, color=DERIV, stroke_width=4, fill_color=BG, fill_opacity=1).move_to(line.n2p(-1)), Dot(line.n2p(1), radius=0.11, color=DERIV))
        self.example("A series for ln(1 + x)", r"Find the Maclaurin series for $\ln(1 + x)$ and its interval of convergence.",
                     [r"\frac{1}{1 + x} = 1 - x + x^2 - x^3 + \cdots, \ |x| < 1", r"\ln(1 + x) = \int_0^x \frac{dt}{1 + t}", r"= \int_0^x \left(1 - t + t^2 - t^3 + \cdots\right) dt", r"= x - \tfrac{x^2}{2} + \tfrac{x^3}{3} - \tfrac{x^4}{4} + \cdots",
                      r"= \sum_{n=0}^{\infty} \frac{(-1)^n x^{n+1}}{n + 1}, \ R = 1", r"x = 1: \ 1 - \tfrac12 + \tfrac13 - \cdots \ \text{converges (AST)}", r"x = -1: \ -\left(1 + \tfrac12 + \tfrac13 + \cdots\right) \ \text{diverges}", r"(-1, 1]"],
                     at=[1, 2, 3, 3, 4, 5, 5, 6], figure=fig, figure_at=6)

        with self.beat("Close") as b:
            card = VGroup(T("differentiate or integrate term by term", 36), T("radius unchanged; recheck endpoints", 36, TANGENT), T("start from a known series (often geometric); fix $C$ with a known value", 32, DIM)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Arctangent", r"Find the Maclaurin series for $\arctan x$.",
                     [r"\frac{1}{1 + t^2} = \sum (-1)^n t^{2n}, \ |t| < 1", r"\arctan x = \int_0^x \frac{dt}{1 + t^2}", r"= \sum \frac{(-1)^n x^{2n+1}}{2n + 1} = x - \tfrac{x^3}{3} + \tfrac{x^5}{5} - \cdots", r"\text{interval } [-1, 1]"], at=[1, 2, 2, 3])
        self.example("Example 2: Differentiating the geometric series", r"Find a power series for $\frac{1}{(1 - x)^2}$.",
                     [r"\frac{1}{1 - x} = \sum x^n", r"\frac{d}{dx}: \ \frac{1}{(1 - x)^2} = \sum_{n=1}^{\infty} n x^{n-1} = 1 + 2x + 3x^2 + \cdots, \ |x| < 1"], at=[1, 1])
        self.example("Example 3: Summing a series with calculus", r"Find $\displaystyle\sum_{n=1}^{\infty} \frac{n}{2^n}$.",
                     [r"\sum n x^{n-1} = \frac{1}{(1 - x)^2}, \ \text{so} \ \sum n x^n = \frac{x}{(1 - x)^2}", r"x = \tfrac12: \ \sum \frac{n}{2^n} = \frac{1/2}{(1/2)^2} = 2"], at=[1, 2])
        self.finish()
