"""Topic 8.12: Washer method about other axes. Narration comes from transcripts/8_12.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "8.12"

    def construct(self):
        line, par = (lambda s: s), (lambda s: s * s)

        def scene_axes(yr, w=4.6, h=5, coords=False):
            return plot_axes([-0.3, 1.4, 0.5], yr, w=w, h=h, coords=coords)

        with self.beat("Moving the axis") as b:
            ax, al = scene_axes([-3.2, 1.4, 1])
            VGroup(ax, al).shift(LEFT * 3)
            axis = DashedLine(ax.c2p(-0.3, -1), ax.c2p(1.4, -1), color=TANGENT, stroke_width=5)
            self.play(FadeIn(ax), FadeIn(al), FadeIn(region(ax, line, par, 0, 1)), Create(ax.plot(line, x_range=[0, 1.15], color=FUNC, stroke_width=4)),
                      Create(ax.plot(par, x_range=[0, 1.1], color=DERIV, stroke_width=4)), Create(axis), FadeIn(M("y = -1", 28, TANGENT).next_to(axis, RIGHT, buff=0.1)), run_time=1.2)
            self.play(FadeIn(solid_of_revolution(ax, lambda s: s + 1, 0, 1, r_in=lambda s: s * s + 1, axis_y=-1, n=7)), run_time=1.4)
            b.line(1)
            ax2, al2 = scene_axes([-0.3, 4.4, 1])
            VGroup(ax2, al2).to_edge(RIGHT, buff=0.8)
            axis2 = DashedLine(ax2.c2p(-0.3, 2), ax2.c2p(1.4, 2), color=TANGENT, stroke_width=5)
            self.play(FadeIn(ax2), FadeIn(al2), FadeIn(region(ax2, line, par, 0, 1)), Create(axis2), FadeIn(M("y = 2", 28, TANGENT).next_to(axis2, RIGHT, buff=0.1)), run_time=1)
            self.play(FadeIn(solid_of_revolution(ax2, lambda s: 2 - s * s, 0, 1, r_in=lambda s: 2 - s, axis_y=2, n=7)), run_time=1.2)
            b.line(2)
        self.clear()
        self.title()

        with self.beat("Measuring from the axis") as b:
            ax, al = plot_axes([-0.3, 1.4, 0.5], [-1.4, 1.4, 0.5], w=5, h=5)
            VGroup(ax, al).to_edge(LEFT, buff=0.6)
            axis = DashedLine(ax.c2p(-0.3, -1), ax.c2p(1.4, -1), color=TANGENT, stroke_width=5)
            self.play(FadeIn(ax), FadeIn(al), FadeIn(region(ax, line, par, 0, 1)), Create(ax.plot(line, x_range=[0, 1.15], color=FUNC, stroke_width=4)), Create(ax.plot(par, x_range=[0, 1.1], color=DERIV, stroke_width=4)), Create(axis), run_time=1)
            x0 = 0.7
            Rl = Line(ax.c2p(x0 + 0.02, -1), ax.c2p(x0 + 0.02, line(x0)), color=SECANT, stroke_width=6)
            rl = Line(ax.c2p(x0 - 0.02, -1), ax.c2p(x0 - 0.02, par(x0)), color=TANGENT, stroke_width=6)
            self.play(Create(Rl), FadeIn(M(r"R = x - (-1) = x + 1", 30, SECANT).to_edge(RIGHT, buff=0.6).shift(UP * 1.6)), run_time=1)
            b.line(1)
            self.play(Create(rl), FadeIn(M(r"r = x^2 - (-1) = x^2 + 1", 30, TANGENT).to_edge(RIGHT, buff=0.6).shift(UP * 0.8)), run_time=1)
            gap = nudge_arrow(ax.c2p(-0.15, -1), ax.c2p(-0.15, 0), label="1", side=LEFT, color=DIM)
            self.play(FadeIn(gap), run_time=0.6)
            b.line(2)
            board = VGroup(M(r"\text{radius} = (\text{farther value}) - (\text{nearer value})", 32), M(r"\text{axis below: curve} - k", 32), M(r"\text{axis above: } k - \text{curve}", 32)).arrange(DOWN, buff=0.3).to_edge(RIGHT, buff=0.4).shift(DOWN * 1.2)
            self.play(FadeIn(board), run_time=1)
        self.clear()

        ax, _ = plot_axes([-0.3, 1.4, 0.5], [-3.2, 1.4, 1], w=3.6, h=4.6)
        fig = VGroup(ax, region(ax, line, par, 0, 1, opacity=0.4), ax.plot(line, x_range=[0, 1.15], color=FUNC, stroke_width=4), ax.plot(par, x_range=[0, 1.1], color=DERIV, stroke_width=4),
                     DashedLine(ax.c2p(-0.3, -1), ax.c2p(1.4, -1), color=TANGENT, stroke_width=4), solid_of_revolution(ax, lambda s: s + 1, 0, 1, r_in=lambda s: s * s + 1, axis_y=-1, n=6))
        self.example("About y = −1", r"The region between $y = x$ and $y = x^2$ is revolved about the line $y = -1$. Find the volume.",
                     [r"R = x - (-1) = x + 1", r"r = x^2 - (-1) = x^2 + 1", r"R^2 = x^2 + 2x + 1", r"r^2 = x^4 + 2x^2 + 1", r"R^2 - r^2 = 2x - x^2 - x^4", r"V = \pi\int_0^1 \left(2x - x^2 - x^4\right) dx",
                      r"= \pi\left(1 - \tfrac13 - \tfrac15\right)", r"= \tfrac{7\pi}{15} \approx 1.47"], at=[1, 1, 2, 2, 3, 4, 4, 4], figure=fig)

        with self.beat("An axis above the region") as b:
            ax, al = plot_axes([-0.3, 1.4, 0.5], [-0.3, 2.4, 0.5], w=5, h=4.6)
            VGroup(ax, al).to_edge(LEFT, buff=0.6)
            axis = DashedLine(ax.c2p(-0.3, 2), ax.c2p(1.4, 2), color=TANGENT, stroke_width=5)
            self.play(FadeIn(ax), FadeIn(al), FadeIn(region(ax, line, par, 0, 1)), Create(ax.plot(line, x_range=[0, 1.15], color=FUNC, stroke_width=4)), Create(ax.plot(par, x_range=[0, 1.1], color=DERIV, stroke_width=4)), Create(axis), run_time=1)
            x0 = 0.6
            self.play(Create(Line(ax.c2p(x0 + 0.02, 2), ax.c2p(x0 + 0.02, par(x0)), color=SECANT, stroke_width=6)), Create(Line(ax.c2p(x0 - 0.02, 2), ax.c2p(x0 - 0.02, line(x0)), color=TANGENT, stroke_width=6)), run_time=1)
            b.line(1)
            board = VGroup(M(r"R = 2 - x^2, \ \ r = 2 - x", 36, SECANT), T("now the parabola is farther", 30, DIM),
                           M(r"V = \pi\int_0^1 \left((2 - x^2)^2 - (2 - x)^2\right) dx", 32), M(r"= \pi\int_0^1 \left(x^4 - 5x^2 + 4x\right) dx = \tfrac{8\pi}{15}", 32, ACCUM)).arrange(DOWN, buff=0.35).to_edge(RIGHT, buff=0.4)
            self.play(FadeIn(board[:2]), run_time=1)
            b.line(2)
            self.play(Write(board[2]), run_time=1)
            self.play(Write(board[3]), run_time=1)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(formula_box(M(r"V = \pi\int \left(R^2 - r^2\right)", 48, ACCUM), ACCUM), T("measure both radii from the axis: bigger $-$ smaller", 34),
                          T("which curve is outer depends on where the axis is", 34, SECANT), T("draw the axis and both radii first", 34, DIM)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        ax, _ = plot_axes([-2.6, 1.4, 1], [-0.3, 1.4, 0.5], w=4.4, h=2.8)
        fig1 = VGroup(ax, region(ax, np.sqrt, lambda y: y, 0, 1, var="y", opacity=0.4), ax.plot(line, x_range=[0, 1.15], color=FUNC, stroke_width=4), ax.plot(par, x_range=[0, 1.1], color=DERIV, stroke_width=4),
                      DashedLine(ax.c2p(-1, -0.3), ax.c2p(-1, 1.4), color=TANGENT, stroke_width=4), solid_about_vertical(ax, lambda y: np.sqrt(y) + 1, 0, 1, r_in=lambda y: y + 1, axis_x=-1, n=6))
        self.example("Example 1: About x = −1", r"The region between $y = x$ and $y = x^2$ is revolved about the line $x = -1$. Find the volume.",
                     [r"TEXT:Vertical axis: horizontal washers, $0 \le y \le 1$.", r"\text{line } x = y, \ \ \text{parabola } x = \sqrt y", r"R = \sqrt y + 1, \ \ r = y + 1",
                      r"R^2 - r^2 = \left(y + 2\sqrt y + 1\right) - \left(y^2 + 2y + 1\right) = 2\sqrt y - y - y^2", r"V = \pi\int_0^1 \left(2\sqrt y - y - y^2\right) dy", r"= \pi\left(\tfrac43 - \tfrac12 - \tfrac13\right)", r"= \tfrac\pi2"],
                     at=[1, 1, 2, 3, 3, 3, 3], figure=fig1)
        ax, _ = plot_axes([-2.6, 2.6, 1], [-8.4, 4.4, 2], w=3.4, h=4.6, coords=False)
        fig2 = VGroup(ax, region(ax, lambda s: 4, par, -2, 2, opacity=0.4), ax.plot(par, x_range=[-2.2, 2.2], color=FUNC, stroke_width=4), DashedLine(ax.c2p(-2.6, -2), ax.c2p(2.6, -2), color=TANGENT, stroke_width=4),
                      solid_of_revolution(ax, lambda s: 6, -2, 2, r_in=lambda s: s * s + 2, axis_y=-2, n=7))
        self.example("Example 2: About y = −2", r"The region between $y = x^2$ and $y = 4$ is revolved about the line $y = -2$. Find the volume.",
                     [r"x^2 = 4 \text{ at } x = \pm2", r"R = 4 - (-2) = 6, \ \ r = x^2 + 2", r"R^2 - r^2 = 36 - \left(x^4 + 4x^2 + 4\right) = 32 - 4x^2 - x^4", r"V = \pi\int_{-2}^{2} \left(32 - 4x^2 - x^4\right) dx",
                      r"= 2\pi\left(64 - \tfrac{32}{3} - \tfrac{32}{5}\right)", r"= \tfrac{1408\pi}{15} \approx 294.89"], at=[1, 1, 2, 3, 3, 3], figure=fig2)
        ax, _ = plot_axes([-0.3, 4.4, 1], [-0.3, 6.4, 1], w=3.8, h=4.6, coords=False)
        fig3 = VGroup(ax, region(ax, np.sqrt, lambda s: s / 2, 0, 4, opacity=0.4), ax.plot(np.sqrt, x_range=[0, 4.3], color=FUNC, stroke_width=4), ax.plot(lambda s: s / 2, x_range=[0, 4.3], color=DERIV, stroke_width=4),
                      DashedLine(ax.c2p(-0.3, 3), ax.c2p(4.4, 3), color=TANGENT, stroke_width=4), solid_of_revolution(ax, lambda s: 3 - s / 2, 0, 4, r_in=lambda s: 3 - np.sqrt(s), axis_y=3, n=7))
        self.example("Example 3: About y = 3", r"The region between $y = \sqrt x$ and $y = \frac x2$ is revolved about the line $y = 3$. Find the volume.",
                     [r"TEXT:The curves meet at $x = 0$ and $x = 4$; the axis is above, so $\frac x2$ (lower) is farther.", r"R = 3 - \tfrac x2, \ \ r = 3 - \sqrt x",
                      r"R^2 - r^2 = \left(9 - 3x + \tfrac{x^2}{4}\right) - \left(9 - 6\sqrt x + x\right) = \tfrac{x^2}{4} - 4x + 6\sqrt x", r"V = \pi\int_0^4 \left(\tfrac{x^2}{4} - 4x + 6\sqrt x\right) dx",
                      r"= \pi\left(\tfrac{16}{3} - 32 + 32\right)", r"= \tfrac{16\pi}{3} \approx 16.76"], at=[1, 1, 2, 3, 3, 3], figure=fig3)
        self.finish()
