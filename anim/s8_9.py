"""Topic 8.9: Disc method about the x- or y-axis. Narration comes from transcripts/8_9.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "8.9"

    def construct(self):
        with self.beat("Spinning a region") as b:
            ax, al = plot_axes([-0.3, 4.6, 1], [-2.4, 2.4, 1], w=6.4, h=4.6, coords=False)
            VGroup(ax, al).shift(LEFT * 1.6)
            reg = region(ax, np.sqrt, lambda s: 0, 0, 4)
            self.play(FadeIn(ax), FadeIn(al), FadeIn(reg), Create(ax.plot(np.sqrt, x_range=[0, 4], color=FUNC, stroke_width=4)), run_time=1)
            ghost = reg.copy().set_fill(AREA, 0.25)
            self.play(Rotate(ghost, angle=PI, axis=RIGHT, about_point=ax.c2p(0, 0)), run_time=1.6)
            solid = solid_of_revolution(ax, np.sqrt, 0, 4, n=10)
            self.play(FadeOut(ghost), FadeIn(solid), run_time=1)
            b.line(1)
            wheel = VGroup(Ellipse(width=2.4, height=0.6, stroke_color=INK, stroke_width=3, fill_color="#C9B79C", fill_opacity=1),
                           Polygon([-0.6, 0.2, 0], [0.6, 0.2, 0], [0.4, 1.6, 0], [0.7, 2.3, 0], [-0.7, 2.3, 0], [-0.4, 1.6, 0], stroke_color="#8B5A2B", stroke_width=3, fill_color="#C68B59", fill_opacity=1)).to_edge(RIGHT, buff=0.8)
            self.play(FadeIn(wheel), run_time=0.8)
            b.line(2)
            self.play(FadeOut(wheel), run_time=0.6)
        self.clear()
        self.title()

        with self.beat("Every slice is a disc") as b:
            f = lambda s: 0.8 + 0.5 * np.sqrt(s)
            ax, al = plot_axes([-0.3, 4.6, 1], [-2.4, 2.4, 1], w=6, h=4.6, coords=False)
            VGroup(ax, al).to_edge(LEFT, buff=0.4)
            self.play(FadeIn(ax), FadeIn(al), FadeIn(solid_of_revolution(ax, f, 0, 4, n=10)), run_time=1)
            x0 = 2.4
            disc = Ellipse(width=2 * f(x0) * (ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1]) * 0.32, height=2 * f(x0) * (ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1]), stroke_color=SECANT, stroke_width=4, fill_color=SECANT, fill_opacity=0.6).move_to(ax.c2p(x0, 0))
            self.play(FadeIn(disc), run_time=0.8)
            b.line(1)
            rad = Line(ax.c2p(x0, 0), ax.c2p(x0, f(x0)), color=TANGENT, stroke_width=6)
            self.play(Create(rad), FadeIn(M("R(x)", 32, TANGENT).next_to(rad, RIGHT, buff=0.1)), run_time=0.8)
            b.line(2)
            board = VGroup(M(r"A(x) = \pi\,[R(x)]^2", 42), formula_box(M(r"V = \pi\int_a^b [R(x)]^2\,dx", 44, ACCUM), ACCUM), T("the radius is the distance from the axis to the curve", 28, DIM)).arrange(DOWN, buff=0.4).to_edge(RIGHT, buff=0.4)
            self.play(Write(board[0]), run_time=0.8)
            self.play(FadeIn(board[1:]), run_time=1)
            b.line(3)
        self.clear()

        ax, _ = plot_axes([-0.3, 4.6, 1], [-2.4, 2.4, 1], w=4.6, h=4)
        fig = VGroup(ax, region(ax, np.sqrt, lambda s: 0, 0, 4, opacity=0.4), ax.plot(np.sqrt, x_range=[0, 4], color=FUNC, stroke_width=4), solid_of_revolution(ax, np.sqrt, 0, 4, n=8),
                     Line(ax.c2p(2.5, 0), ax.c2p(2.5, np.sqrt(2.5)), color=TANGENT, stroke_width=5))
        self.example("Discs on a root", r"The region under $y = \sqrt x$ for $0 \le x \le 4$ is revolved about the $x$-axis. Find the volume.",
                     [r"R(x) = \sqrt x - 0 = \sqrt x", r"A(x) = \pi\left(\sqrt x\right)^2 = \pi x", r"V = \pi\int_0^4 x\,dx", r"= \pi\left[\tfrac{x^2}{2}\right]_0^4", r"= 8\pi \approx 25.13"], at=[1, 2, 3, 3, 3], figure=fig,
                     notes_graph=dict(fns=[("sqrt(x)", 0, 4)], xr=(-0.3, 4.6), yr=(-2.4, 2.4)), follow=True)

        with self.beat("A check with a cone") as b:
            ax, al = plot_axes([-0.3, 6.6, 1], [-3.6, 3.6, 1], w=6, h=4.6)
            VGroup(ax, al).to_edge(LEFT, buff=0.4)
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(lambda s: s / 2, x_range=[0, 6], color=FUNC, stroke_width=4)), run_time=1)
            self.play(FadeIn(solid_of_revolution(ax, lambda s: s / 2, 0, 6, n=8)), run_time=1)
            b.line(1)
            r1 = M(r"\pi\int_0^6 \left(\tfrac x2\right)^2 dx = \pi \cdot \tfrac{216}{12} = 18\pi", 38).to_edge(RIGHT, buff=0.4).shift(UP * 1)
            self.play(Write(r1), run_time=1)
            b.line(2)
            r2 = M(r"\tfrac13\pi r^2 h = \tfrac13\pi(3^2)(6) = 18\pi", 38, ACCUM).next_to(r1, DOWN, buff=0.6)
            self.play(Write(r2), run_time=1)
            self.play(FadeIn(M(r"\checkmark", 60, GRASS).next_to(r2, DOWN, buff=0.3)), run_time=0.5)
        self.clear()

        with self.beat("Around the y-axis") as b:
            ax, al = plot_axes([-2.4, 2.4, 1], [-0.3, 4.6, 1], w=4.6, h=4.6, coords=False)
            VGroup(ax, al).to_edge(LEFT, buff=0.6)
            self.play(FadeIn(ax), FadeIn(al), FadeIn(region(ax, lambda y: np.sqrt(y), lambda y: 0, 0, 4, var="y")), Create(ax.plot(lambda s: s * s, x_range=[0, 2], color=FUNC, stroke_width=4)),
                      Create(Line(ax.c2p(0, 4), ax.c2p(2, 4), color=FUNC, stroke_width=4)), run_time=1)
            self.play(FadeIn(solid_about_vertical(ax, np.sqrt, 0, 4, n=9)), run_time=1.2)
            b.line(1)
            y0 = 2.2
            rad = Line(ax.c2p(0, y0), ax.c2p(np.sqrt(y0), y0), color=TANGENT, stroke_width=6)
            self.play(Create(rad), FadeIn(M(r"R(y) = \sqrt y", 30, TANGENT).next_to(rad, UP, buff=0.1)), run_time=0.8)
            board = VGroup(T("horizontal slices: integrate in $y$", 30), M(r"x = \sqrt y, \ \ R(y) = \sqrt y", 38), M(r"V = \pi\int_0^4 \left(\sqrt y\right)^2 dy = \pi\int_0^4 y\,dy = 8\pi", 36, ACCUM)).arrange(DOWN, buff=0.4).to_edge(RIGHT, buff=0.4)
            self.play(FadeIn(board[0]), run_time=0.6)
            self.play(Write(board[1]), run_time=0.8)
            b.line(2)
            self.play(Write(board[2]), run_time=1)
            b.line(3)
            self.play(FadeIn(T("slice perpendicular to the axis; integrate along it", 30, SECANT).to_edge(DOWN, buff=0.4)), run_time=0.8)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(M(r"V = \pi\int [R(x)]^2\,dx \ \ (\text{axis horizontal})", 42, ACCUM), M(r"V = \pi\int [R(y)]^2\,dy \ \ (\text{axis vertical})", 42, ACCUM),
                          T("$R$ = distance from the axis to the curve", 36), T("slice perpendicular to the axis", 36, SECANT)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        ax, _ = plot_axes([-0.3, 2.4, 1], [-4.5, 4.5, 2], w=3.6, h=4.2)
        fig1 = VGroup(ax, ax.plot(lambda s: s * s, x_range=[0, 2], color=FUNC, stroke_width=4), solid_of_revolution(ax, lambda s: s * s, 0, 2, n=8))
        self.example("Example 1: A parabola about the x-axis", r"The region under $y = x^2$ for $0 \le x \le 2$ is revolved about the $x$-axis. Find the volume.",
                     [r"R = x^2", r"V = \pi\int_0^2 \left(x^2\right)^2 dx", r"= \pi\int_0^2 x^4\,dx", r"= \pi\left[\tfrac{x^5}{5}\right]_0^2", r"= \tfrac{32\pi}{5} \approx 20.11"], at=[1, 1, 1, 2, 2], figure=fig1)
        ax, _ = plot_axes([-0.3, 1.4, 1], [-3, 3, 1], w=3, h=4.2)
        fig2 = VGroup(ax, ax.plot(np.exp, x_range=[0, 1], color=FUNC, stroke_width=4), solid_of_revolution(ax, np.exp, 0, 1, n=6))
        self.example("Example 2: An exponential about the x-axis", r"The region under $y = e^x$ for $0 \le x \le 1$ is revolved about the $x$-axis. Find the volume.",
                     [r"R = e^x, \ \ R^2 = e^{2x}", r"V = \pi\int_0^1 e^{2x}\,dx", r"= \pi\left[\tfrac12 e^{2x}\right]_0^1", r"= \tfrac\pi2\left(e^2 - 1\right) \approx 10.04"], at=[1, 1, 2, 2], figure=fig2)
        ax, _ = plot_axes([-2.4, 2.4, 1], [-0.3, 8.6, 2], w=3.6, h=4.2)
        fig3 = VGroup(ax, ax.plot(lambda s: s**3, x_range=[0, 2], color=FUNC, stroke_width=4), Line(ax.c2p(0, 8), ax.c2p(2, 8), color=FUNC, stroke_width=4), solid_about_vertical(ax, lambda y: np.cbrt(y), 0, 8, n=8))
        self.example("Example 3: A cubic about the y-axis", r"The region bounded by $y = x^3$, $y = 8$, and the $y$-axis is revolved about the $y$-axis. Find the volume.",
                     [r"TEXT:Horizontal discs: integrate in $y$ from $0$ to $8$.", r"x = y^{1/3}, \ \ R = y^{1/3}", r"V = \pi\int_0^8 y^{2/3}\,dy", r"= \pi\left[\tfrac35 y^{5/3}\right]_0^8", r"= \pi \cdot \tfrac35 \cdot 32",
                      r"= \tfrac{96\pi}{5} \approx 60.32"], at=[1, 1, 2, 2, 3, 3], figure=fig3)
        self.finish()
