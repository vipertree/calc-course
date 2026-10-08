"""Topic 8.7: Volumes with square and rectangle cross sections. Narration comes from transcripts/8_7.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "8.7"

    def construct(self):
        with self.beat("Slicing a loaf") as b:
            crust, crumb = "#B5793A", "#F2DDB0"
            loaf = RoundedRectangle(width=6, height=2.2, corner_radius=0.9, stroke_color=crust, stroke_width=6, fill_color=crumb, fill_opacity=1).shift(LEFT * 1.5)
            cuts = VGroup(*[Line(loaf.get_top() + RIGHT * k * 0.6 + DOWN * 0.1, loaf.get_bottom() + RIGHT * k * 0.6 + UP * 0.1, color=crust, stroke_width=3) for k in range(-4, 5)])
            self.play(FadeIn(loaf), run_time=0.8)
            self.play(Create(cuts), run_time=1.2)
            face = RoundedRectangle(width=2.2, height=2.2, corner_radius=0.7, stroke_color=crust, stroke_width=8, fill_color=crumb, fill_opacity=1).to_edge(RIGHT, buff=1.2).shift(UP * 0.6)
            self.play(FadeIn(face, shift=RIGHT), run_time=1)
            lab = VGroup(M("A", 44, INK).move_to(face), nudge_arrow(face.get_corner(DL) + DOWN * 0.3, face.get_corner(DL) + DOWN * 0.3 + RIGHT * 0.25, label=r"\text{thickness}", side=DOWN))
            self.play(FadeIn(lab), FadeIn(M(r"\text{volume} \approx \text{area} \times \text{thickness}", 38).to_edge(DOWN, buff=0.8)), run_time=1)
            b.line(1)
            self.play(Indicate(cuts), run_time=1)
            b.line(2)
        self.clear()
        self.title()

        with self.beat("Volume is the integral of area") as b:
            P = oblique(origin=LEFT * 4.6 + DOWN * 1.4, sx=1.5, sy=1.2)
            top = lambda s: 1.1 + 0.35 * np.sin(1.2 * s)
            bot = lambda s: -top(s)
            ax = oblique_axes(P, (-0.3, 6), (-1.8, 1.8))
            xs = np.linspace(0.3, 5.0, 12)
            solid = sections(P, top, bot, xs, "square", squash=0.75, color=ACCUM)
            self.play(FadeIn(ax), FadeIn(base_region(P, top, bot, 0.3, 5.0)), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(s) for s in solid], lag_ratio=0.1), run_time=1.6)
            k = 6
            self.play(solid[k].animate.set_fill(SECANT, 0.8).set_stroke(SECANT), FadeIn(M("A(x)", 34, SECANT).next_to(solid[k], UP, buff=0.15)), run_time=0.8)
            self.play(FadeIn(nudge_arrow(P(xs[k], bot(xs[k])) + DOWN * 0.25, P(xs[k] + 0.25, bot(xs[k])) + DOWN * 0.25, label="dx")), run_time=0.6)
            b.line(1)
            board = VGroup(M(r"V \approx \sum A(x)\,\Delta x", 40), M(r"V = \int_a^b A(x)\,dx", 44, ACCUM), T("add up the areas of the slices", 30, DIM)).arrange(DOWN, buff=0.3).to_edge(RIGHT, buff=0.4).to_edge(UP, buff=0.8)
            self.play(Write(board[0]), run_time=0.8)
            self.play(Write(board[1]), FadeIn(board[2]), run_time=1)
            b.line(2)
            self.play(Circumscribe(M("A(x) = ?", 40, SECANT).next_to(board, DOWN, buff=0.5), color=SECANT), run_time=1)
        self.clear()

        with self.beat("A base and its cross sections") as b:
            P = oblique(origin=LEFT * 4 + DOWN * 2, sx=1.6, sy=1.1)
            top = np.sqrt
            bot = lambda s: 0.0
            self.play(FadeIn(oblique_axes(P, (-0.3, 4.8), (-0.3, 2.6))), FadeIn(base_region(P, top, bot, 0, 4)), Create(base_curve(P, top, 0, 4.4)),
                      FadeIn(M(r"y = \sqrt x", 30, FUNC).next_to(P(4.4, 2.1), RIGHT, buff=0.1)), run_time=1.2)
            b.line(1)
            x0 = 2.2
            seg = Line(P(x0, 0), P(x0, top(x0)), color=SECANT, stroke_width=6)
            self.play(Create(seg), FadeIn(M(r"\text{side} = \sqrt x", 30, SECANT).next_to(seg, RIGHT, buff=0.15)), run_time=1)
            b.line(2)
            sq = cross_section("square", P(x0, 0), P(x0, top(x0)), color=SECANT)
            self.play(FadeIn(sq, shift=UP * 0.3), run_time=1)
            many = sections(P, top, bot, np.linspace(0.2, 4, 14), "square")
            self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in many], lag_ratio=0.12), run_time=2)
        self.clear()

        P = oblique(origin=LEFT * 0.4 + DOWN * 1.3, sx=1.0, sy=0.8)
        fig = VGroup(oblique_axes(P, (-0.2, 4.6), (-0.2, 2.5)), base_region(P, np.sqrt, lambda s: 0, 0, 4), base_curve(P, np.sqrt, 0, 4.3),
                     sections(P, np.sqrt, lambda s: 0, np.linspace(0.25, 4, 10), "square"))
        self.example("Squares on a root", r"The base of a solid is the region bounded by $y = \sqrt x$, the $x$-axis, and $x = 4$. Cross sections perpendicular to the $x$-axis are squares. Find the volume.",
                     [r"s(x) = \sqrt x - 0 = \sqrt x", r"A(x) = s^2 = \left(\sqrt x\right)^2 = x", r"V = \int_0^4 x\,dx", r"= \left[\tfrac{x^2}{2}\right]_0^4", r"= 8"], at=[1, 2, 3, 3, 3], figure=fig)

        with self.beat("Rectangles") as b:
            head = M(r"\text{rectangle: } A = \text{base} \times \text{height}", 44).to_edge(UP, buff=0.6)
            self.play(Write(head), run_time=1)
            b.line(1)
            P1 = oblique(origin=LEFT * 6 + DOWN * 1.2, sx=1, sy=0.8)
            P2 = oblique(origin=RIGHT * 0.6 + DOWN * 1.2, sx=1, sy=0.8)
            top = lambda s: 2 - 0.5 * (s - 1.5)**2
            c1 = VGroup(base_region(P1, top, lambda s: 0, -0.5, 3.5), *[rect_section(P1(v, 0), P1(v, top(v)), 1.2) for v in np.linspace(0, 3, 6)])
            c2 = VGroup(base_region(P2, top, lambda s: 0, -0.5, 3.5), *[rect_section(P2(v, 0), P2(v, top(v)), 2 * np.linalg.norm(P2(v, top(v)) - P2(v, 0)) * 0.6) for v in np.linspace(0, 3, 6)])
            l1 = M(r"\text{height } 3: \ A(x) = 3\,s(x)", 34).next_to(c1, DOWN, buff=0.4)
            l2 = M(r"\text{height } 2s: \ A(x) = s \cdot 2s = 2s^2", 34).next_to(c2, DOWN, buff=0.4)
            self.play(FadeIn(c1), FadeIn(c2), FadeIn(l1), FadeIn(l2), run_time=1.4)
            b.line(2)
            self.play(FadeIn(M(r"s(x) = \text{top} - \text{bottom}", 38, SECANT).to_edge(DOWN, buff=0.3)), run_time=0.8)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(formula_box(M(r"V = \int_a^b A(x)\,dx", 50, ACCUM), ACCUM), M(r"\text{side } s(x) = \text{top} - \text{bottom of the base}", 38),
                          M(r"\text{square: } s^2 \qquad \text{rectangle: base} \times \text{height}", 38, SECANT)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        P = oblique(origin=LEFT * 0.2 + DOWN * 1.0, sx=3.2, sy=2.6)
        fig1 = VGroup(oblique_axes(P, (-0.1, 1.3), (-0.1, 1.2)), base_region(P, lambda s: s, lambda s: s * s, 0, 1), base_curve(P, lambda s: s, 0, 1.1), base_curve(P, lambda s: s * s, 0, 1.05, DERIV),
                      sections(P, lambda s: s, lambda s: s * s, np.linspace(0.1, 0.9, 9), "square"))
        self.example("Example 1: Squares between two curves", r"The base is the region between $y = x$ and $y = x^2$. Cross sections perpendicular to the $x$-axis are squares. Find the volume.",
                     [r"TEXT:The curves meet at $x = 0$ and $x = 1$; $x$ is on top.", r"s(x) = x - x^2", r"A(x) = \left(x - x^2\right)^2 = x^2 - 2x^3 + x^4",
                      r"V = \int_0^1 \left(x^2 - 2x^3 + x^4\right) dx", r"= \tfrac13 - \tfrac12 + \tfrac15", r"= \tfrac{1}{30}"], at=[1, 1, 2, 3, 3, 3], figure=fig1)
        P = oblique(origin=LEFT * 0.2 + DOWN * 1.0, sx=0.9, sy=0.55)
        par = lambda s: 4 - s * s
        fig2 = VGroup(oblique_axes(P, (-2.4, 2.6), (-0.2, 4.4)), base_region(P, par, lambda s: 0, -2, 2), base_curve(P, par, -2, 2),
                      VGroup(*[rect_section(P(v, 0), P(v, par(v)), 0.9) for v in np.linspace(-1.8, 1.8, 9)]))
        self.example("Example 2: Rectangles of height 3", r"The base is the region between $y = 4 - x^2$ and the $x$-axis. Cross sections perpendicular to the $x$-axis are rectangles of height $3$. Find the volume.",
                     [r"4 - x^2 = 0 \text{ at } x = \pm2", r"s(x) = 4 - x^2", r"A(x) = 3\left(4 - x^2\right)", r"V = \int_{-2}^{2} 3\left(4 - x^2\right) dx", r"= 3\left[4x - \tfrac{x^3}{3}\right]_{-2}^{2}",
                      r"= 3 \cdot \tfrac{32}{3}", r"= 32"], at=[1, 1, 2, 3, 3, 3, 3], figure=fig2)
        P = oblique(origin=LEFT * 0.6 + DOWN * 1.2, sx=0.55, sy=0.6)
        fig3 = VGroup(oblique_axes(P, (-0.3, 4.8), (-2.4, 2.6)), base_region(P, lambda y: 4, lambda y: y * y, -2, 2, var="y"), base_curve(P, lambda y: y * y, -2.1, 2.1, DERIV, var="y"),
                      base_curve(P, lambda y: 4, -2.1, 2.1, FUNC, var="y"), sections(P, lambda y: 4, lambda y: y * y, np.linspace(1.8, -1.8, 9), "square", squash=0.5, var="y"))
        self.example("Example 3: Perpendicular to the y-axis", r"The base is the region between $x = y^2$ and $x = 4$. Cross sections perpendicular to the $y$-axis are squares. Find the volume.",
                     [r"TEXT:Perpendicular to the $y$-axis: horizontal slices, so integrate in $y$.", r"y^2 = 4 \text{ at } y = \pm2", r"s(y) = 4 - y^2", r"A(y) = \left(4 - y^2\right)^2 = 16 - 8y^2 + y^4",
                      r"V = \int_{-2}^{2} \left(16 - 8y^2 + y^4\right) dy", r"= 2\left(32 - \tfrac{64}{3} + \tfrac{32}{5}\right)", r"= \tfrac{512}{15} \approx 34.13"], at=[1, 1, 2, 2, 3, 3, 3], figure=fig3)
        self.finish()
