"""Topic 8.5: Area between curves (functions of y). Narration comes from transcripts/8_5.md.

Adder's notes (2026-10-14): dy slivers are lines, not rectangles. The sqrt(x) and x - 2 region labels its boundaries
before anything is solved. Every example sketches the graphs first, then finds and labels the intersection points.
"""
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
        bottom = lambda s: 0 if s < 2 else s - 2
        with self.beat("Turning the slices sideways") as b:
            ax, al = plot_axes([-0.5, 4.5, 1], [-0.5, 2.5, 1], w=6.4, h=4)
            VGroup(ax, al).shift(DOWN * 0.2)
            self.play(FadeIn(ax), FadeIn(al), Create(side(ax, left, 0, 2.2, DERIV)), Create(side(ax, right, -0.5, 2.3, FUNC)), Create(Line(ax.c2p(-0.5, 0), ax.c2p(4.5, 0), color=DIM)), run_time=1.2)
            vs = VGroup(*[sliver(ax, np.sqrt, bottom, s) for s in (0.8, 1.6, 2.6, 3.4)])
            qs = VGroup(*[M("?", 32, TANGENT).next_to(ax.c2p(s, bottom(s)), DOWN, buff=0.12) for s in (0.8, 1.6, 2.6, 3.4)])
            self.play(LaggedStart(*[Create(v) for v in vs], lag_ratio=0.25), FadeIn(qs), run_time=1.2)
            b.line(1)
            hs = VGroup(*[sliver(ax, right, left, y, var="y") for y in (0.3, 0.8, 1.3, 1.8)])
            self.play(FadeOut(qs), ReplacementTransform(vs, hs), run_time=1.4)
            b.line(2)
            self.play(FadeIn(nudge_arrow(ax.c2p(right(1.3) + 0.15, 1.2), ax.c2p(right(1.3) + 0.15, 1.4), label="dy", side=RIGHT)), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("Right minus left") as b:
            R = lambda y: 3.2 + 0.4 * np.sin(1.5 * y)
            L = lambda y: 0.6 + 0.3 * (y - 1.5)**2
            ax, al = plot_axes([0, 4.5, 1], [0, 3.5, 1], w=5.6, h=4.0, coords=False)
            VGroup(ax, al).to_edge(LEFT, buff=0.5).shift(UP * 0.4)
            self.play(FadeIn(ax), FadeIn(al), FadeIn(region(ax, R, L, 0.3, 3.0, var="y", opacity=0.3)), Create(side(ax, R, 0.3, 3.0, FUNC)), Create(side(ax, L, 0.3, 3.0, DERIV)),
                      FadeIn(M("g", 32, DERIV).next_to(ax.c2p(L(3.0), 3.0), LEFT, buff=0.1)), FadeIn(M("f", 32, FUNC).next_to(ax.c2p(R(3.0), 3.0), RIGHT, buff=0.1)), run_time=1.2)
            sl = sliver(ax, R, L, 1.6, var="y", width=7)
            yl = M("y", 28, SECANT).next_to(ax.c2p(0, 1.6), LEFT, buff=0.12)
            dy = nudge_arrow(ax.c2p(R(1.6) + 0.12, 1.5), ax.c2p(R(1.6) + 0.12, 1.7), label="dy", side=RIGHT, color=SECANT, size=26)
            lab = M(r"\text{sliver length: } f(y) - g(y)", 32, SECANT).next_to(ax, DOWN, buff=0.35)
            self.play(Create(sl), FadeIn(yl), FadeIn(dy), FadeIn(lab), run_time=1)
            b.line(1)
            board = VGroup(M(r"\text{area} = \int_c^d \big(f(y) - g(y)\big)\,dy", 40), formula_box(M(r"\int (\text{right} - \text{left})\,dy", 42, ACCUM), ACCUM)).arrange(DOWN, buff=0.5).to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
            self.play(Write(board[0]), FadeIn(board[1]), run_time=1.2)
            b.line(2)
            self.play(FadeIn(T("write each curve as $x = $ (something in $y$)", 30, DIM).next_to(board, DOWN, buff=0.5)), run_time=0.8)
        self.clear()

        with self.beat("Choosing dy") as b:
            def pic():
                ax, _ = plot_axes([-0.3, 4.5, 1], [-0.3, 2.5, 1], w=4.8, h=2.8)
                g = VGroup(ax, region(ax, right, left, 0, 2, var="y", opacity=0.3), side(ax, left, 0, 2.15, DERIV), ax.plot(lambda s: s - 2, x_range=[2, 4.4], color=FUNC, stroke_width=4))
                labs = VGroup(M(r"y = \sqrt x", 26, DERIV).move_to(ax.c2p(1.0, 1.6)), M("y = x - 2", 26, FUNC).move_to(ax.c2p(3.75, 0.95)), M("y = 0", 24, DIM).move_to(ax.c2p(3.5, 0.24)))
                return ax, g, labs
            ax1, p1, n1 = pic()
            ax2, p2, n2 = pic()
            VGroup(VGroup(p1, n1), VGroup(p2, n2)).arrange(RIGHT, buff=0.8).to_edge(UP, buff=0.6)
            self.play(FadeIn(p1), FadeIn(p2), run_time=1)
            self.play(LaggedStart(*[FadeIn(VGroup(u, v)) for u, v in zip(n1, n2)], lag_ratio=0.5), run_time=1.6)
            b.line(1)
            v1 = VGroup(*[sliver(ax1, np.sqrt, bottom, s, width=4) for s in np.arange(0.3, 4, 0.4)], DashedLine(ax1.c2p(2, 0), ax1.c2p(2, 2.4), color=TANGENT))
            w1 = M(r"\int_0^4 \sqrt x\,dx - \int_2^4 (x - 2)\,dx = \tfrac{16}{3} - 2 = \tfrac{10}{3}", 30).next_to(VGroup(p1, n1), DOWN, buff=0.4)
            self.play(LaggedStart(*[Create(v) for v in v1], lag_ratio=0.1), Write(w1), run_time=1.6)
            b.line(2)
            self.play(Transform(n2[0], M(r"x = y^2", 26, DERIV).move_to(n2[0])), Transform(n2[1], M("x = y + 2", 26, FUNC).move_to(n2[1])), run_time=1)
            h2 = VGroup(*[sliver(ax2, right, left, y, var="y", width=4) for y in np.arange(0.2, 2, 0.3)])
            w2 = M(r"\int_0^2 \left(y + 2 - y^2\right) dy = 2 + 4 - \tfrac83 = \tfrac{10}{3}", 30).next_to(VGroup(p2, n2), DOWN, buff=0.4)
            self.play(LaggedStart(*[Create(h) for h in h2], lag_ratio=0.1), Write(w2), run_time=1.6)
            self.play(FadeIn(T("same area", 34, ACCUM).next_to(VGroup(w1, w2), DOWN, buff=0.4)), run_time=0.6)
            b.line(3)
            self.play(FadeIn(T("$dy$: the left and right curves don't change", 32, SECANT).to_edge(DOWN, buff=0.4)), run_time=0.8)
        self.clear()

        # ---------------------------------------------------------------- the lesson example: sketch first
        ax, _ = plot_axes([-4.5, 5.5, 1], [-2.5, 3.8, 1], w=5, h=4.6)
        p, l = (lambda y: y**2 - 4), (lambda y: 2 * y - 1)
        ghost = side(ax, lambda y: y**2, -1.8, 1.8, DIM)
        para = VGroup(side(ax, p, -2.4, 3.1, DERIV), M("x = y^2 - 4", 26, DERIV).move_to(ax.c2p(-3.0, 3.0)))
        line = VGroup(side(ax, l, -1.75, 3.25, FUNC), M("x = 2y - 1", 26, FUNC).move_to(ax.c2p(3.4, 0.4)))
        shade = region(ax, l, p, -1, 3, var="y", opacity=0.3)
        pts = VGroup(point_label(ax, -3, -1, "(-3, -1)", (-3.0, -2.1), size=24), point_label(ax, 5, 3, "(5, 3)", (3.9, 3.5), size=24))
        sl = sliver(ax, l, p, 1.0, var="y")

        def sketch_parabola(sc):
            sc.play(Create(ghost), run_time=0.8)
            sc.play(ghost.animate.shift(ax.c2p(-4, 0) - ax.c2p(0, 0)), run_time=1.2)
            sc.play(FadeIn(para), FadeOut(ghost), run_time=0.6)

        self.example("A parabola and a line, sideways", r"Find the area of the region bounded by $x = y^2 - 4$ and $x = 2y - 1$.",
                     [r"TEXT:$x = y^2 - 4$: the sideways parabola $x = y^2$, shifted left $4$", r"TEXT:$x = 2y - 1$: a line through $(-1, 0)$, $2$ to the right for each $1$ up",
                      r"TEXT:The line is on the right; use $dy$.", r"y^2 - 4 = 2y - 1", r"y^2 - 2y - 3 = 0", r"(y - 3)(y + 1) = 0", r"y = -1, \ \ y = 3",
                      r"TEXT:Intersections: $(-3, -1)$ and $(5, 3)$", r"TEXT:Check $y = 0$: line $-1$, parabola $-4$.", r"TEXT:Sliver length: right $-$ left",
                      r"A = \int_{-1}^{3} \big((2y - 1) - (y^2 - 4)\big)\,dy", r"= \int_{-1}^{3} \left(-y^2 + 2y + 3\right) dy", r"= \left[-\tfrac{y^3}{3} + y^2 + 3y\right]_{-1}^{3}",
                      r"= (-9 + 9 + 9) - \left(\tfrac13 + 1 - 3\right)", r"= 9 - \left(-\tfrac53\right)", r"= \tfrac{32}{3}"],
                     at=[1, 2, 3, 4, 5, 5, 5, 6, 7, 8, 8, 8, 9, 10, 10, 11], figure=VGroup(ax), figure_at=1, size=42,
                     cues={0: sketch_parabola, 1: draw_cue(line), 2: draw_cue(shade), 7: draw_cue(pts), 9: draw_cue(sl)}, overlays=(ghost, para, line, shade, pts, sl))

        with self.beat("Close") as b:
            card = VGroup(formula_box(M(r"\text{Area} = \int_c^d (\text{right} - \text{left})\,dy", 46, ACCUM), ACCUM), T("sketch first; limits: $y$ values", 36),
                          T("use $dy$ when the left and right curves don't change", 34, SECANT)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        # Example 1: against the y-axis
        ax, _ = plot_axes([-0.5, 4.5, 1], [-2.5, 2.5, 1], w=3.8, h=3.8)
        c1 = VGroup(side(ax, lambda y: 4 - y**2, -2.2, 2.2, FUNC), M("x = 4 - y^2", 26, FUNC).move_to(ax.c2p(3.0, 1.95)))
        sh1 = VGroup(region(ax, lambda y: 4 - y**2, lambda y: 0, -2, 2, var="y", opacity=0.3), sliver(ax, lambda y: 4 - y**2, lambda y: 0, 0.5, var="y"))
        p1 = VGroup(point_label(ax, 0, 2, "(0, 2)", (0.85, 2.3), size=24), point_label(ax, 0, -2, "(0, -2)", (0.95, -2.3), size=24))
        self.example("Example 1: Against the y-axis", r"Find the area between $x = 4 - y^2$ and the $y$-axis.",
                     [r"TEXT:$x = 4 - y^2$: a sideways parabola opening left, vertex $(4, 0)$", r"TEXT:The $y$-axis is $x = 0$, on the left.", r"4 - y^2 = 0, \ \ y = \pm2",
                      r"TEXT:Intersections: $(0, 2)$ and $(0, -2)$", r"A = \int_{-2}^{2} \left((4 - y^2) - 0\right) dy", r"= \left[4y - \tfrac{y^3}{3}\right]_{-2}^{2}",
                      r"= \left(8 - \tfrac83\right) - \left(-8 + \tfrac83\right)", r"= \tfrac{32}{3}"], at=[1, 2, 3, 3, 4, 5, 5, 5], figure=VGroup(ax), figure_at=1,
                     cues={0: draw_cue(c1), 1: draw_cue(sh1), 3: draw_cue(p1)}, overlays=(c1, sh1, p1))
        # Example 2: solve for x first
        ax, _ = plot_axes([-0.3, 3.6, 1], [-0.3, 1.4, 0.5], w=4.4, h=2.8, coords=False)
        c2 = VGroup(ax.plot(np.log, x_range=[0.75, 3], color=FUNC, stroke_width=4), M(r"y = \ln x", 26, FUNC).move_to(ax.c2p(2.65, 0.55)))
        b2 = VGroup(DashedLine(ax.c2p(0, 1), ax.c2p(3, 1), color=DIM), M("y = 1", 24, DIM).move_to(ax.c2p(3.35, 1.0)))
        sh2 = VGroup(region(ax, np.exp, lambda y: 0, 0, 1, var="y", opacity=0.3), sliver(ax, np.exp, lambda y: 0, 0.5, var="y"))
        p2 = VGroup(point_label(ax, 1, 0, "(1, 0)", (1.25, -0.19), size=24), point_label(ax, np.e, 1, "(e, 1)", (2.6, 1.27), size=24))
        self.example("Example 2: Solve for x first", r"Find the area of the region bounded by $y = \ln x$, the $y$-axis, $y = 0$, and $y = 1$.",
                     [r"TEXT:$y = \ln x$: through $(1, 0)$, rising slowly", r"TEXT:the $y$-axis, and the lines $y = 0$ and $y = 1$", r"y = \ln x, \ \text{so} \ x = e^y",
                      r"TEXT:Corners on the curve: $(1, 0)$ and $(e, 1)$", r"\text{left: } x = 0, \ \ \text{right: } x = e^y", r"A = \int_0^1 e^y\,dy", r"= \left[e^y\right]_0^1", r"= e - 1 \approx 1.72"],
                     at=[1, 2, 3, 3, 4, 5, 5, 5], figure=VGroup(ax), figure_at=1,
                     cues={0: draw_cue(c2), 1: draw_cue(b2, sh2[0]), 3: draw_cue(p2), 4: draw_cue(sh2[1])}, overlays=(c2, b2, sh2, p2))
        # Example 3: two sideways parabolas
        ax, _ = plot_axes([-0.3, 2.3, 1], [-1.8, 1.8, 1], w=3.4, h=3.8)
        c3 = VGroup(side(ax, lambda y: y**2, -1.25, 1.25, DERIV), M("x = y^2", 26, DERIV).move_to(ax.c2p(1.85, 1.6)))
        d3 = VGroup(side(ax, lambda y: 2 - y**2, -1.25, 1.25, FUNC), M("x = 2 - y^2", 26, FUNC).move_to(ax.c2p(0.78, 1.62)))
        sh3 = region(ax, lambda y: 2 - y**2, lambda y: y**2, -1, 1, var="y", opacity=0.3)
        p3 = VGroup(point_label(ax, 1, 1, "(1, 1)", (1.8, 1.0), size=24), point_label(ax, 1, -1, "(1, -1)", (1.8, -1.0), size=24))
        s3 = sliver(ax, lambda y: 2 - y**2, lambda y: y**2, 0.3, var="y")
        self.example("Example 3: Two sideways parabolas", r"Find the area between $x = y^2$ and $x = 2 - y^2$.",
                     [r"TEXT:$x = y^2$: opens right, from the origin", r"TEXT:$x = 2 - y^2$: opens left, vertex $(2, 0)$", r"y^2 = 2 - y^2", r"2y^2 = 2, \ \ y = \pm1",
                      r"TEXT:Intersections: $(1, 1)$ and $(1, -1)$", r"TEXT:$x = 2 - y^2$ is on the right.", r"A = \int_{-1}^{1} \left(2 - 2y^2\right) dy",
                      r"= \left[2y - \tfrac23y^3\right]_{-1}^{1}", r"= \tfrac43 - \left(-\tfrac43\right) = \tfrac83"], at=[1, 2, 3, 3, 3, 4, 4, 4, 4], figure=VGroup(ax), figure_at=1,
                     cues={0: draw_cue(c3), 1: draw_cue(d3, sh3), 4: draw_cue(p3), 5: draw_cue(s3)}, overlays=(c3, d3, sh3, p3, s3))
        self.finish()
