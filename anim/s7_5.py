"""Topic 7.5 (BC): Euler's method. Narration comes from transcripts/7_5.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def euler(f, x0, y0, h, n):
    pts = [(x0, y0)]
    for _ in range(n):
        y0 = y0 + h * f(x0, y0)
        x0 = x0 + h
        pts.append((x0, y0))
    return pts


class Lesson(TranscriptScene):
    NUM = "7.5"

    def construct(self):
        f = lambda x, y: x + y
        ax, al = plot_axes([0, 1.2, 0.5], [0, 4, 1], w=6, h=5.2)
        VGroup(ax, al).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        exact = lambda x: 2 * np.exp(x) - x - 1
        pts = euler(f, 0, 1, 0.5, 2)
        with self.beat("Walking along tangent lines") as b:
            field = slope_field(ax, f, np.arange(0.1, 1.2, 0.2), np.arange(0.5, 4, 0.5), length=0.28)
            self.play(FadeIn(T("BC only", 28, DIM).to_corner(UR, buff=0.4)), FadeIn(ax), FadeIn(al), FadeIn(field), Create(ax.plot(exact, x_range=[0, 1.1], color=FUNC, stroke_width=3, stroke_opacity=0.5)), run_time=1.4)
            b.line(1)
            d0 = Dot(ax.c2p(*pts[0]), color=SECANT)
            self.play(FadeIn(d0), run_time=0.4)
            self.play(Create(Line(ax.c2p(*pts[0]), ax.c2p(*pts[1]), color=SECANT, stroke_width=5)), FadeIn(Dot(ax.c2p(*pts[1]), color=SECANT)), run_time=1)
            b.line(2)
            self.play(Create(Line(ax.c2p(*pts[1]), ax.c2p(*pts[2]), color=SECANT, stroke_width=5)), FadeIn(Dot(ax.c2p(*pts[2]), color=SECANT)), run_time=1)
            self.play(FadeIn(Dot(ax.c2p(1, exact(1)), color=FUNC)), FadeIn(M(r"\text{true } y(1) \approx 3.44", 30, FUNC).next_to(ax.c2p(1, exact(1)), LEFT, buff=0.2)), run_time=0.6)
        self.clear()
        self.title()

        with self.beat("The method") as b:
            rule = VGroup(M(r"m_n = \frac{dy}{dx} \text{ at } (x_n, y_n)", 40), M(r"y_{n+1} = y_n + h \cdot m_n, \quad x_{n+1} = x_n + h", 40, ACCUM)).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.5)
            self.play(Write(rule[0]), run_time=1)
            b.line(1)
            self.play(Write(rule[1]), run_time=1)
            tab = table([r"x", r"y", r"\text{slope}", r"\Delta y = h \cdot \text{slope}"], [["0", "1", "1", "0.5"], ["0.5", "1.5", "2", "1"], ["1", "2.5", r"\ ", r"\ "]], size=38).next_to(rule, DOWN, buff=0.6)
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab[1]), run_time=0.6)
            b.line(2)
            self.play(FadeIn(VGroup(*tab.cells[1])), run_time=0.8)
            b.line(3)
            self.play(FadeIn(VGroup(*tab.cells[2])), run_time=0.8)
            self.play(FadeIn(VGroup(*tab.cells[3])), FadeIn(M(r"y(1) \approx 2.5", 40, ACCUM).next_to(tab, DOWN, buff=0.5)), run_time=0.8)
        self.clear()

        ax, al = plot_axes([0, 1.2, 0.5], [0, 4, 1], w=5.4, h=4.8)
        VGroup(ax, al).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        with self.beat("Over or under?") as b:
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(exact, x_range=[0, 1.1], color=FUNC, stroke_width=4)),
                      Create(VGroup(Line(ax.c2p(*pts[0]), ax.c2p(*pts[1]), color=SECANT, stroke_width=5), Line(ax.c2p(*pts[1]), ax.c2p(*pts[2]), color=SECANT, stroke_width=5))), run_time=1.2)
            b.line(1)
            d2 = M(r"\frac{d^2y}{dx^2} = 1 + \frac{dy}{dx} = 1 + x + y > 0", 38).to_edge(RIGHT, buff=0.5).shift(UP * 1.8)
            self.play(Write(d2), run_time=1.2)
            b.line(2)
            rules = VGroup(T("concave up: Euler underestimates", 32, DERIV), T("concave down: Euler overestimates", 32, TANGENT), M(r"y(1) = 2e - 2 \approx 3.437", 36, FUNC)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
            rules.next_to(d2, DOWN, buff=0.6).align_to(d2, LEFT)
            self.play(FadeIn(rules), run_time=1)
        self.clear()

        self.example("Smaller steps", r"$\dfrac{dy}{dx} = y - x$, $y(0) = 2$. Use Euler's method with two steps of size $0.25$ to approximate $y(0.5)$.",
                     [r"(0, 2): \ \text{slope } 2, \ \Delta y = 0.25(2) = 0.5", r"(0.25, 2.5): \ \text{slope } 2.5 - 0.25 = 2.25, \ \Delta y = 0.5625", r"y(0.5) \approx 2.5 + 0.5625 = 3.0625"], at=[1, 2, 3])

        with self.beat("Close") as b:
            card = VGroup(M(r"y_{n+1} = y_n + h \cdot \left(\tfrac{dy}{dx} \text{ at } (x_n, y_n)\right)", 42, ACCUM), T(r"Use a table: $x$, $y$, slope, $\Delta y$.", 36),
                          T("Concave up: underestimate. Concave down: overestimate.", 34, SECANT)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=1.6)
        self.clear()

        self.examples_card()
        self.example("Example 1: Two steps", r"$\dfrac{dy}{dx} = 2x$, $y(1) = 3$. Use Euler's method with two steps of size $0.5$ to approximate $y(2)$. Over or under?",
                     [r"(1, 3): \ \text{slope } 2, \ \Delta y = 1", r"(1.5, 4): \ \text{slope } 3, \ \Delta y = 1.5", r"y(2) \approx 5.5", r"\frac{d^2y}{dx^2} = 2 > 0: \ \text{concave up, an underestimate}"], at=[1, 2, 3, 4])
        self.finish()
