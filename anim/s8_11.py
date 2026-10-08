"""Topic 8.11: Washer method about the axes. Narration comes from transcripts/8_11.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def washer_face(R, r, color=SECANT):
    """A flat ring seen face-on: a disc of radius R with a hole of radius r (screen units)."""
    return Annulus(inner_radius=r, outer_radius=R, color=color, fill_opacity=0.7, stroke_color=color, stroke_width=3)


class Lesson(TranscriptScene):
    NUM = "8.11"

    def construct(self):
        line, par = (lambda s: s), (lambda s: s * s)
        with self.beat("A hole in the middle") as b:
            ax, al = plot_axes([-0.2, 1.3, 0.5], [-1.2, 1.2, 0.5], w=5.4, h=4.8, coords=False)
            VGroup(ax, al).to_edge(LEFT, buff=0.6)
            self.play(FadeIn(ax), FadeIn(al), FadeIn(region(ax, line, par, 0, 1)), Create(ax.plot(line, x_range=[0, 1.1], color=FUNC, stroke_width=4)),
                      Create(ax.plot(par, x_range=[0, 1.05], color=DERIV, stroke_width=4)), run_time=1)
            self.play(FadeIn(solid_of_revolution(ax, line, 0, 1, r_in=par, n=8)), run_time=1.4)
            b.line(1)
            face = washer_face(1.3, 0.55).to_edge(RIGHT, buff=1.4).shift(UP * 0.8)
            metal = VGroup(Annulus(inner_radius=0.3, outer_radius=0.75, color="#A8A8A8", fill_opacity=1, stroke_color=INK, stroke_width=2)).next_to(face, DOWN, buff=0.6)
            self.play(FadeIn(face), FadeIn(metal), FadeIn(T("a washer", 30, DIM).next_to(metal, RIGHT, buff=0.3)), run_time=1)
            b.line(2)
            self.play(FadeIn(M(r"\text{disc} - \text{hole}", 38, INK).next_to(face, UP, buff=0.3)), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("Outer radius and inner radius") as b:
            top = lambda s: 2.2 + 0.3 * np.sin(1.5 * s)
            bot = lambda s: 0.9 + 0.2 * np.cos(s)
            ax, al = plot_axes([-0.2, 4.4, 1], [-0.3, 3, 1], w=5.4, h=3.8, coords=False)
            VGroup(ax, al).to_edge(LEFT, buff=0.4).shift(UP * 0.6)
            self.play(FadeIn(ax), FadeIn(al), FadeIn(region(ax, top, bot, 0.3, 4)), Create(ax.plot(top, x_range=[0.3, 4], color=FUNC, stroke_width=4)), Create(ax.plot(bot, x_range=[0.3, 4], color=DERIV, stroke_width=4)), run_time=1)
            x0 = 2.4
            Rl = Line(ax.c2p(x0 + 0.06, 0), ax.c2p(x0 + 0.06, top(x0)), color=SECANT, stroke_width=6)
            rl = Line(ax.c2p(x0 - 0.06, 0), ax.c2p(x0 - 0.06, bot(x0)), color=TANGENT, stroke_width=6)
            self.play(Create(Rl), FadeIn(M(r"R(x)\text{, outer}", 28, SECANT).next_to(Rl, RIGHT, buff=0.1).shift(UP * 0.4)), run_time=0.8)
            self.play(Create(rl), FadeIn(M(r"r(x)\text{, inner}", 28, TANGENT).next_to(rl, LEFT, buff=0.1)), run_time=0.8)
            b.line(1)
            face = washer_face(1.1, 0.5).to_edge(RIGHT, buff=1.2).shift(UP * 1.6)
            board = VGroup(M(r"A(x) = \pi R^2 - \pi r^2 = \pi\left(R^2 - r^2\right)", 34), formula_box(M(r"V = \pi\int_a^b \left(R(x)^2 - r(x)^2\right) dx", 38, ACCUM), ACCUM)).arrange(DOWN, buff=0.3).next_to(face, DOWN, buff=0.3).to_edge(RIGHT, buff=0.3)
            self.play(FadeIn(face), Write(board[0]), run_time=1)
            b.line(2)
            self.play(FadeIn(board[1]), run_time=0.8)
            b.line(3)
            warn = VGroup(M(r"(R - r)^2 \ne R^2 - r^2", 36, TANGENT), M(r"(3 - 2)^2 = 1, \quad 9 - 4 = 5", 32)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.3).shift(LEFT * 2.5)
            self.play(FadeIn(warn), run_time=1)
        self.clear()

        ax, _ = plot_axes([-0.2, 1.3, 0.5], [-1.2, 1.2, 0.5], w=4, h=4)
        fig = VGroup(ax, region(ax, line, par, 0, 1, opacity=0.4), ax.plot(line, x_range=[0, 1.1], color=FUNC, stroke_width=4), ax.plot(par, x_range=[0, 1.05], color=DERIV, stroke_width=4),
                     solid_of_revolution(ax, line, 0, 1, r_in=par, n=7))
        self.example("Washers between a line and a parabola", r"The region between $y = x$ and $y = x^2$ is revolved about the $x$-axis. Find the volume.",
                     [r"x = x^2 \text{ at } x = 0, 1", r"TEXT:On $(0, 1)$, $x > x^2$, so $R = x$ and $r = x^2$.", r"V = \pi\int_0^1 \left(x^2 - \left(x^2\right)^2\right) dx", r"= \pi\int_0^1 \left(x^2 - x^4\right) dx",
                      r"= \pi\left[\tfrac{x^3}{3} - \tfrac{x^5}{5}\right]_0^1", r"= \pi\left(\tfrac13 - \tfrac15\right)", r"= \tfrac{2\pi}{15} \approx 0.42"], at=[1, 2, 3, 3, 4, 4, 5], figure=fig, follow=True)

        with self.beat("Around the y-axis") as b:
            ax, al = plot_axes([-1.3, 1.3, 0.5], [-0.2, 1.3, 0.5], w=5, h=3.6, coords=False)
            VGroup(ax, al).to_edge(LEFT, buff=0.5).shift(UP * 0.5)
            self.play(FadeIn(ax), FadeIn(al), FadeIn(region(ax, np.sqrt, lambda y: y, 0, 1, var="y")), Create(ax.plot(line, x_range=[0, 1.1], color=FUNC, stroke_width=4)), Create(ax.plot(par, x_range=[0, 1.1], color=DERIV, stroke_width=4)), run_time=1)
            self.play(FadeIn(solid_about_vertical(ax, np.sqrt, 0, 1, r_in=lambda y: y, n=7)), run_time=1.2)
            board = VGroup(M(r"\text{line: } x = y, \ \ \text{parabola: } x = \sqrt y", 34), M(r"R = \sqrt y, \ \ r = y", 36, SECANT), M(r"V = \pi\int_0^1 \left(y - y^2\right) dy = \tfrac\pi6", 36, ACCUM)).arrange(DOWN, buff=0.4).to_edge(RIGHT, buff=0.4)
            self.play(Write(board[0]), run_time=1)
            b.line(1)
            y0 = 0.45
            self.play(Create(Line(ax.c2p(0, y0 + 0.02), ax.c2p(np.sqrt(y0), y0 + 0.02), color=SECANT, stroke_width=5)), Create(Line(ax.c2p(0, y0 - 0.02), ax.c2p(y0, y0 - 0.02), color=TANGENT, stroke_width=5)), Write(board[1]), run_time=1)
            b.line(2)
            self.play(Write(board[2]), run_time=1)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(formula_box(M(r"V = \pi\int \left(R^2 - r^2\right)", 48, ACCUM), ACCUM), T("$R$: axis to the farther curve; $r$: axis to the nearer curve", 34), T("square each radius separately", 34, TANGENT)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        ax, _ = plot_axes([-0.2, 1.3, 0.5], [-1.2, 1.2, 0.5], w=3.6, h=3.6)
        fig1 = VGroup(ax, region(ax, np.sqrt, line, 0, 1, opacity=0.4), ax.plot(np.sqrt, x_range=[0, 1.2], color=FUNC, stroke_width=4), ax.plot(line, x_range=[0, 1.2], color=DERIV, stroke_width=4), solid_of_revolution(ax, np.sqrt, 0, 1, r_in=line, n=7))
        self.example("Example 1: Root and line about the x-axis", r"The region between $y = \sqrt x$ and $y = x$ is revolved about the $x$-axis. Find the volume.",
                     [r"\sqrt x = x \text{ at } x = 0, 1", r"R = \sqrt x, \ \ r = x", r"V = \pi\int_0^1 \left(x - x^2\right) dx", r"= \pi\left(\tfrac12 - \tfrac13\right)", r"= \tfrac\pi6 \approx 0.52"], at=[1, 1, 2, 3, 3], figure=fig1)
        ax, _ = plot_axes([-1.4, 1.4, 1], [-4.4, 4.4, 1], w=3, h=4.4, coords=False)
        fig2 = VGroup(ax, region(ax, lambda s: 4 - s * s, lambda s: 3, -1, 1, opacity=0.4), ax.plot(lambda s: 4 - s * s, x_range=[-1.3, 1.3], color=FUNC, stroke_width=4), Line(ax.c2p(-1.4, 3), ax.c2p(1.4, 3), color=DERIV, stroke_width=4),
                      solid_of_revolution(ax, lambda s: 4 - s * s, -1, 1, r_in=lambda s: 3, n=7))
        self.example("Example 2: A parabola and a line, about the x-axis", r"The region between $y = 4 - x^2$ and $y = 3$ is revolved about the $x$-axis. Find the volume.",
                     [r"4 - x^2 = 3 \text{ at } x = \pm1", r"R = 4 - x^2, \ \ r = 3", r"R^2 - r^2 = \left(16 - 8x^2 + x^4\right) - 9 = 7 - 8x^2 + x^4", r"V = \pi\int_{-1}^{1} \left(7 - 8x^2 + x^4\right) dx",
                      r"= 2\pi\left(7 - \tfrac83 + \tfrac15\right)", r"= \tfrac{136\pi}{15} \approx 28.48"], at=[1, 1, 2, 3, 3, 3], figure=fig2)
        ax, _ = plot_axes([-2.4, 2.4, 1], [-0.3, 4.4, 1], w=3.8, h=3.8)
        fig3 = VGroup(ax, region(ax, np.sqrt, lambda y: y / 2, 0, 4, var="y", opacity=0.4), ax.plot(lambda s: 2 * s, x_range=[0, 2.1], color=FUNC, stroke_width=4), ax.plot(par, x_range=[0, 2.05], color=DERIV, stroke_width=4),
                      solid_about_vertical(ax, np.sqrt, 0, 4, r_in=lambda y: y / 2, n=7))
        self.example("Example 3: About the y-axis", r"The region between $y = 2x$ and $y = x^2$ is revolved about the $y$-axis. Find the volume.",
                     [r"2x = x^2 \text{ at } x = 0, 2\text{, so } 0 \le y \le 4", r"\text{line: } x = \tfrac y2, \ \ \text{parabola: } x = \sqrt y", r"TEXT:At $y = 1$: $\sqrt1 = 1 > \tfrac12$, so $R = \sqrt y$ and $r = \tfrac y2$.",
                      r"V = \pi\int_0^4 \left(y - \tfrac{y^2}{4}\right) dy", r"= \pi\left(8 - \tfrac{16}{3}\right)", r"= \tfrac{8\pi}{3} \approx 8.38"], at=[1, 1, 2, 3, 3, 3], figure=fig3)
        self.finish()
