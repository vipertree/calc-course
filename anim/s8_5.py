"""Topic 8.5: Area between curves (functions of y). Narration comes from transcripts/8_5.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def side(ax, g, y0, y1, color=FUNC):
    """The curve x = g(y) for y0 <= y <= y1."""
    return ax.plot_parametric_curve(lambda s: np.array([g(s), s, 0.0]), t_range=[y0, y1, 0.01], color=color, stroke_width=4)


class Lesson(TranscriptScene):
    NUM = "8.5"

    def construct(self):
        left = lambda y: y**2
        right = lambda y: y + 2
        with self.beat("Turning the slices sideways") as b:
            ax, al = plot_axes([-0.5, 4.5, 1], [-0.5, 2.5, 1], w=6.4, h=4)
            VGroup(ax, al).shift(DOWN * 0.2)
            self.play(FadeIn(ax), FadeIn(al), Create(side(ax, left, 0, 2.2, DERIV)), Create(side(ax, right, -0.5, 2.3, FUNC)), Create(Line(ax.c2p(-0.5, 0), ax.c2p(4.5, 0), color=DIM)), run_time=1.2)
            vs = VGroup(*[slice_rect(ax, np.sqrt, (lambda s: 0) if s < 2 else (lambda s: s - 2), s, 0.18) for s in (0.8, 1.6, 2.6, 3.4)])
            qs = VGroup(*[M("?", 32, TANGENT).next_to(r, DOWN, buff=0.08) for r in vs])
            self.play(FadeIn(vs), FadeIn(qs), run_time=1)
            b.line(1)
            hs = VGroup(*[slice_rect(ax, right, left, y, 0.14, var="y") for y in (0.3, 0.8, 1.3, 1.8)])
            self.play(FadeOut(qs), ReplacementTransform(vs, hs), run_time=1.4)
            b.line(2)
            self.play(FadeIn(nudge_arrow(ax.c2p(right(1.3) + 0.15, 1.23), ax.c2p(right(1.3) + 0.15, 1.37), label="dy", side=RIGHT)), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("Right minus left") as b:
            R = lambda y: 3.2 + 0.4 * np.sin(1.5 * y)
            L = lambda y: 0.6 + 0.3 * (y - 1.5)**2
            ax, al = plot_axes([0, 4.5, 1], [0, 3.5, 1], w=5.6, h=4.2, coords=False)
            VGroup(ax, al).to_edge(LEFT, buff=0.5)
            self.play(FadeIn(ax), FadeIn(al), FadeIn(region(ax, R, L, 0.3, 3.0, var="y", opacity=0.3)), Create(side(ax, R, 0.3, 3.0, FUNC)), Create(side(ax, L, 0.3, 3.0, DERIV)), run_time=1.2)
            sl = slice_rect(ax, R, L, 1.6, 0.16, var="y", label="dy")
            self.play(FadeIn(sl), FadeIn(M(r"f(y) - g(y)", 30, SECANT).next_to(ax.c2p((R(1.6) + L(1.6)) / 2, 1.7), UP, buff=0.1)), run_time=1)
            b.line(1)
            board = VGroup(M(r"\text{area} = \int_c^d \big(f(y) - g(y)\big)\,dy", 40), formula_box(M(r"\int (\text{right} - \text{left})\,dy", 42, ACCUM), ACCUM)).arrange(DOWN, buff=0.5).to_edge(RIGHT, buff=0.4)
            self.play(Write(board[0]), FadeIn(board[1]), run_time=1.2)
            b.line(2)
            self.play(FadeIn(T("write each curve as $x = $ (something in $y$)", 30, DIM).next_to(board, DOWN, buff=0.5)), run_time=0.8)
        self.clear()

        with self.beat("Choosing dy") as b:
            def pic():
                ax, _ = plot_axes([-0.3, 4.5, 1], [-0.3, 2.5, 1], w=4.8, h=2.8)
                return ax, VGroup(ax, region(ax, right, left, 0, 2, var="y", opacity=0.3), side(ax, left, 0, 2.15, DERIV), ax.plot(lambda s: s - 2, x_range=[2, 4.4], color=FUNC, stroke_width=4))
            ax1, p1 = pic()
            ax2, p2 = pic()
            VGroup(p1, p2).arrange(RIGHT, buff=0.8).to_edge(UP, buff=0.6)
            self.play(FadeIn(p1), FadeIn(p2), run_time=1)
            b.line(1)
            v1 = VGroup(*[slice_rect(ax1, np.sqrt, (lambda s: 0) if s < 2 else (lambda s: s - 2), s, 0.16) for s in np.arange(0.3, 4, 0.5)], DashedLine(ax1.c2p(2, 0), ax1.c2p(2, 2.4), color=TANGENT))
            w1 = M(r"\int_0^4 \sqrt x\,dx - \int_2^4 (x - 2)\,dx = \tfrac{16}{3} - 2 = \tfrac{10}{3}", 30).next_to(p1, DOWN, buff=0.4)
            self.play(FadeIn(v1), Write(w1), run_time=1.4)
            b.line(2)
            h2 = VGroup(*[slice_rect(ax2, right, left, y, 0.12, var="y") for y in np.arange(0.2, 2, 0.35)])
            w2 = M(r"\int_0^2 \left(y + 2 - y^2\right) dy = 2 + 4 - \tfrac83 = \tfrac{10}{3}", 30).next_to(p2, DOWN, buff=0.4)
            self.play(FadeIn(h2), Write(w2), run_time=1.4)
            self.play(FadeIn(T("same area", 34, ACCUM).next_to(VGroup(w1, w2), DOWN, buff=0.4)), run_time=0.6)
            b.line(3)
            self.play(FadeIn(T("$dy$: the left and right curves don't change", 32, SECANT).to_edge(DOWN, buff=0.4)), run_time=0.8)
        self.clear()

        ax, _ = plot_axes([-4.5, 5.5, 1], [-1.8, 3.8, 1], w=5, h=4.4)
        p, l = (lambda y: y**2 - 4), (lambda y: 2 * y - 1)
        fig = VGroup(ax, region(ax, l, p, -1, 3, var="y", opacity=0.35), side(ax, p, -1.8, 3.1, DERIV), side(ax, l, -1.6, 3.2, FUNC), slice_rect(ax, l, p, 1.0, 0.14, var="y", label="dy"))
        self.example("A parabola and a line, sideways", r"Find the area of the region bounded by $x = y^2 - 4$ and $x = 2y - 1$.",
                     [r"y^2 - 4 = 2y - 1", r"y^2 - 2y - 3 = 0", r"(y - 3)(y + 1) = 0", r"y = -1, \ \ y = 3", r"TEXT:Test $y = 0$: line $-1$, parabola $-4$, so the line is on the right.",
                      r"A = \int_{-1}^{3} \big((2y - 1) - (y^2 - 4)\big)\,dy", r"= \int_{-1}^{3} \left(-y^2 + 2y + 3\right) dy", r"= \left[-\tfrac{y^3}{3} + y^2 + 3y\right]_{-1}^{3}",
                      r"= (-9 + 9 + 9) - \left(\tfrac13 + 1 - 3\right)", r"= 9 - \left(-\tfrac53\right)", r"= \tfrac{32}{3}"],
                     at=[1, 2, 2, 2, 3, 4, 4, 5, 6, 6, 7], figure=fig, figure_at=3)

        with self.beat("Close") as b:
            card = VGroup(formula_box(M(r"\text{Area} = \int_c^d (\text{right} - \text{left})\,dy", 46, ACCUM), ACCUM), T("limits: $y$ values", 36), T("use $dy$ when the left and right curves don't change", 34, SECANT)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        ax, _ = plot_axes([-0.5, 4.5, 1], [-2.5, 2.5, 1], w=3.6, h=3.6)
        fig1 = VGroup(ax, region(ax, lambda y: 4 - y**2, lambda y: 0, -2, 2, var="y", opacity=0.35), side(ax, lambda y: 4 - y**2, -2.2, 2.2, FUNC))
        self.example("Example 1: Against the y-axis", r"Find the area between $x = 4 - y^2$ and the $y$-axis.",
                     [r"TEXT:The $y$-axis is $x = 0$; $4 - y^2 = 0$ at $y = \pm2$.", r"A = \int_{-2}^{2} \left((4 - y^2) - 0\right) dy", r"= \left[4y - \tfrac{y^3}{3}\right]_{-2}^{2}",
                      r"= \left(8 - \tfrac83\right) - \left(-8 + \tfrac83\right)", r"= \tfrac{32}{3}"], at=[1, 2, 3, 3, 3], figure=fig1)
        ax, _ = plot_axes([-0.3, 3, 1], [-0.3, 1.4, 0.5], w=4, h=2.8, coords=False)
        fig2 = VGroup(ax, region(ax, np.exp, lambda y: 0, 0, 1, var="y", opacity=0.35), ax.plot(np.log, x_range=[0.5, 3], color=FUNC, stroke_width=4), DashedLine(ax.c2p(0, 1), ax.c2p(3, 1), color=DIM))
        self.example("Example 2: Solve for x first", r"Find the area of the region bounded by $y = \ln x$, the $y$-axis, $y = 0$, and $y = 1$.",
                     [r"y = \ln x, \ \text{so} \ x = e^y", r"\text{left: } x = 0, \ \ \text{right: } x = e^y", r"A = \int_0^1 e^y\,dy", r"= \left[e^y\right]_0^1", r"= e - 1 \approx 1.72"], at=[1, 2, 3, 3, 3], figure=fig2)
        ax, _ = plot_axes([-0.3, 2.3, 1], [-1.5, 1.5, 1], w=3.4, h=3.6)
        fig3 = VGroup(ax, region(ax, lambda y: 2 - y**2, lambda y: y**2, -1, 1, var="y", opacity=0.35), side(ax, lambda y: y**2, -1.4, 1.4, DERIV), side(ax, lambda y: 2 - y**2, -1.4, 1.4, FUNC))
        self.example("Example 3: Two sideways parabolas", r"Find the area between $x = y^2$ and $x = 2 - y^2$.",
                     [r"y^2 = 2 - y^2", r"2y^2 = 2, \ \ y = \pm1", r"TEXT:Test $y = 0$: $2 - y^2$ gives $2$, $y^2$ gives $0$, so $x = 2 - y^2$ is on the right.", r"A = \int_{-1}^{1} \left(2 - 2y^2\right) dy",
                      r"= \left[2y - \tfrac23y^3\right]_{-1}^{1}", r"= \tfrac43 - \left(-\tfrac43\right) = \tfrac83"], at=[1, 1, 2, 3, 3, 3], figure=fig3)
        self.finish()
