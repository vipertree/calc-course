"""Topic 8.10: Disc method about other axes. Narration comes from transcripts/8_10.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "8.10"

    def construct(self):
        par = lambda s: s * s
        with self.beat("A different axis") as b:
            ax, al = plot_axes([-2.6, 2.6, 1], [-4.6, 8.6, 2], w=5, h=5.6, coords=False)
            VGroup(ax, al).shift(LEFT * 2.6)
            reg = region(ax, lambda s: 4, par, -2, 2)
            self.play(FadeIn(ax), FadeIn(al), FadeIn(reg), Create(ax.plot(par, x_range=[-2.3, 2.3], color=FUNC, stroke_width=4)), run_time=1)
            s1 = solid_of_revolution(ax, lambda s: 4, -2, 2, r_in=par, axis_y=0, n=7)
            self.play(FadeIn(s1), FadeIn(T("a hole: next topic", 28, DIM).next_to(ax, RIGHT, buff=0.2)), run_time=1.2)
            b.line(1)
            ax2, al2 = plot_axes([-2.6, 2.6, 1], [-0.6, 8.6, 2], w=4.6, h=5.6, coords=False)
            VGroup(ax2, al2).to_edge(RIGHT, buff=0.6)
            axis = DashedLine(ax2.c2p(-2.6, 4), ax2.c2p(2.6, 4), color=TANGENT, stroke_width=5)
            self.play(FadeIn(ax2), FadeIn(al2), FadeIn(region(ax2, lambda s: 4, par, -2, 2)), Create(axis), FadeIn(M("y = 4", 28, TANGENT).next_to(axis, RIGHT, buff=0.1)), run_time=1)
            self.play(FadeIn(solid_of_revolution(ax2, lambda s: 4 - s * s, -2, 2, axis_y=4, n=9)), run_time=1.2)
            b.line(2)
        self.clear()
        self.title()

        with self.beat("The radius is a distance to the axis") as b:
            ax, al = plot_axes([-2.6, 2.6, 1], [-0.6, 5, 1], w=5, h=4.8)
            VGroup(ax, al).to_edge(LEFT, buff=0.6)
            axis = DashedLine(ax.c2p(-2.6, 4), ax.c2p(2.6, 4), color=TANGENT, stroke_width=5)
            self.play(FadeIn(ax), FadeIn(al), FadeIn(region(ax, lambda s: 4, par, -2, 2)), Create(ax.plot(par, x_range=[-2.2, 2.2], color=FUNC, stroke_width=4)), Create(axis), run_time=1)
            x0 = 1.1
            good = Line(ax.c2p(x0, par(x0)), ax.c2p(x0, 4), color=SECANT, stroke_width=6)
            self.play(Create(good), FadeIn(M("R = 4 - x^2", 32, SECANT).next_to(good, RIGHT, buff=0.1)), run_time=1)
            b.line(1)
            bad = Line(ax.c2p(-x0, 0), ax.c2p(-x0, par(x0)), color=DIM, stroke_width=6)
            bl = M("R = x^2", 32, DIM).next_to(bad, LEFT, buff=0.1)
            self.play(Create(bad), FadeIn(bl), run_time=0.8)
            self.play(Create(Cross(bl, stroke_color=TANGENT, scale_factor=0.9)), FadeIn(T("that's the distance to the $x$-axis", 26, TANGENT).next_to(bl, DOWN, buff=0.3)), run_time=0.8)
            b.line(2)
            board = VGroup(M(r"R = (\text{bigger}) - (\text{smaller})", 38), M(r"\text{axis above the curve: } R = k - f(x)", 32), M(r"\text{axis below the curve: } R = f(x) - k", 32)).arrange(DOWN, buff=0.4).to_edge(RIGHT, buff=0.4)
            self.play(FadeIn(board), run_time=1)
        self.clear()

        ax, _ = plot_axes([-2.6, 2.6, 1], [-0.6, 8.6, 2], w=3.8, h=4.6)
        fig = VGroup(ax, region(ax, lambda s: 4, par, -2, 2, opacity=0.4), ax.plot(par, x_range=[-2.2, 2.2], color=FUNC, stroke_width=4), DashedLine(ax.c2p(-2.6, 4), ax.c2p(2.6, 4), color=TANGENT, stroke_width=4),
                     solid_of_revolution(ax, lambda s: 4 - s * s, -2, 2, axis_y=4, n=8), Line(ax.c2p(1.1, 1.21), ax.c2p(1.1, 4), color=SECANT, stroke_width=5))
        self.example("Spinning about y = 4", r"The region bounded by $y = x^2$ and $y = 4$ is revolved about the line $y = 4$. Find the volume.",
                     [r"x^2 = 4 \text{ at } x = \pm2", r"R(x) = 4 - x^2", r"R^2 = \left(4 - x^2\right)^2 = 16 - 8x^2 + x^4", r"V = \pi\int_{-2}^{2} \left(16 - 8x^2 + x^4\right) dx",
                      r"= 2\pi\left[16x - \tfrac{8x^3}{3} + \tfrac{x^5}{5}\right]_0^2", r"= 2\pi\left(32 - \tfrac{64}{3} + \tfrac{32}{5}\right)", r"= \tfrac{512\pi}{15} \approx 107.23"], at=[1, 2, 3, 4, 4, 5, 5], figure=fig)

        with self.beat("Vertical lines too") as b:
            ax, al = plot_axes([-0.6, 2.6, 1], [-1.6, 1.6, 1], w=4.8, h=4.6)
            VGroup(ax, al).to_edge(LEFT, buff=0.8)
            axis = DashedLine(ax.c2p(1, -1.6), ax.c2p(1, 1.6), color=TANGENT, stroke_width=5)
            self.play(FadeIn(ax), FadeIn(al), FadeIn(region(ax, lambda y: 1, lambda y: y * y, -1, 1, var="y")),
                      Create(ax.plot_parametric_curve(lambda s: np.array([s * s, s, 0]), t_range=[-1.3, 1.3, 0.01], color=FUNC, stroke_width=4)), Create(axis), run_time=1)
            self.play(FadeIn(solid_about_vertical(ax, lambda y: 1 - y * y, -1, 1, axis_x=1, n=9)), run_time=1.2)
            board = VGroup(T("vertical axis: horizontal slices, integrate in $y$", 32), M(r"R = (\text{axis}) - (\text{curve}) = 1 - y^2", 38, SECANT)).arrange(DOWN, buff=0.5).to_edge(RIGHT, buff=0.5)
            self.play(FadeIn(board[0]), run_time=0.8)
            b.line(1)
            y0 = 0.5
            self.play(Create(Line(ax.c2p(y0 * y0, y0), ax.c2p(1, y0), color=SECANT, stroke_width=6)), Write(board[1]), run_time=1)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(formula_box(M(r"V = \pi\int R^2\ (dx \text{ or } dy)", 46, ACCUM), ACCUM), T("$R$ = distance from the axis to the curve: bigger $-$ smaller", 34),
                          M(r"\text{axis } y = k: \ R = |f(x) - k| \qquad \text{axis } x = k: \ R = |g(y) - k|", 36, SECANT)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        ax, _ = plot_axes([-0.3, 4.6, 1], [-0.3, 4.4, 1], w=4.2, h=4)
        fig1 = VGroup(ax, region(ax, lambda s: 2, np.sqrt, 0, 4, opacity=0.4), ax.plot(np.sqrt, x_range=[0, 4.3], color=FUNC, stroke_width=4), DashedLine(ax.c2p(-0.3, 2), ax.c2p(4.6, 2), color=TANGENT, stroke_width=4),
                      solid_of_revolution(ax, lambda s: 2 - np.sqrt(s), 0, 4, axis_y=2, n=7))
        self.example("Example 1: About y = 2", r"The region bounded by $y = \sqrt x$, $y = 2$, and the $y$-axis is revolved about the line $y = 2$. Find the volume.",
                     [r"\sqrt x = 2 \text{ at } x = 4", r"R = 2 - \sqrt x", r"R^2 = 4 - 4\sqrt x + x", r"V = \pi\int_0^4 \left(4 - 4\sqrt x + x\right) dx", r"= \pi\left[4x - \tfrac83x^{3/2} + \tfrac{x^2}{2}\right]_0^4",
                      r"= \pi\left(16 - \tfrac{64}{3} + 8\right)", r"= \tfrac{8\pi}{3} \approx 8.38"], at=[1, 1, 2, 2, 3, 3, 3], figure=fig1)
        ax, _ = plot_axes([-0.6, 2.4, 1], [-1.4, 1.4, 1], w=3.6, h=3.6)
        fig2 = VGroup(ax, region(ax, lambda y: 1, lambda y: y * y, -1, 1, var="y", opacity=0.4), ax.plot_parametric_curve(lambda s: np.array([s * s, s, 0]), t_range=[-1.2, 1.2, 0.01], color=FUNC, stroke_width=4),
                      DashedLine(ax.c2p(1, -1.4), ax.c2p(1, 1.4), color=TANGENT, stroke_width=4), solid_about_vertical(ax, lambda y: 1 - y * y, -1, 1, axis_x=1, n=7))
        self.example("Example 2: About x = 1", r"The region bounded by $x = y^2$ and $x = 1$ is revolved about the line $x = 1$. Find the volume.",
                     [r"y^2 = 1 \text{ at } y = \pm1", r"R = 1 - y^2", r"R^2 = 1 - 2y^2 + y^4", r"V = \pi\int_{-1}^{1} \left(1 - 2y^2 + y^4\right) dy", r"= 2\pi\left(1 - \tfrac23 + \tfrac15\right)",
                      r"= \tfrac{16\pi}{15} \approx 3.35"], at=[1, 1, 2, 3, 3, 3], figure=fig2)
        ax, _ = plot_axes([-0.3, 2.4, 1], [-0.3, 1.4, 1], w=3.8, h=3)
        fig3 = VGroup(ax, region(ax, par, lambda s: 0, 0, 1, opacity=0.4), ax.plot(par, x_range=[0, 1.15], color=FUNC, stroke_width=4), DashedLine(ax.c2p(1, -0.3), ax.c2p(1, 1.4), color=TANGENT, stroke_width=4),
                      solid_about_vertical(ax, lambda y: 1 - np.sqrt(y), 0, 1, axis_x=1, n=6))
        self.example("Example 3: A vertical axis on the right", r"The region bounded by $y = x^2$, the $x$-axis, and $x = 1$ is revolved about the line $x = 1$. Find the volume.",
                     [r"TEXT:Horizontal slices, $0 \le y \le 1$; the curve is $x = \sqrt y$.", r"R = 1 - \sqrt y", r"R^2 = 1 - 2\sqrt y + y", r"V = \pi\int_0^1 \left(1 - 2\sqrt y + y\right) dy",
                      r"= \pi\left(1 - \tfrac43 + \tfrac12\right)", r"= \tfrac\pi6 \approx 0.52"], at=[1, 2, 2, 3, 3, 3], figure=fig3)
        self.finish()
