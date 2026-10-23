"""Topic 9.4 (BC): Vector-valued functions and their derivatives. Narration comes from transcripts/9_4.md."""
import numpy as np
from manim import *

from kit import *
from props import walk_along
from style import *


class Lesson(TranscriptScene):
    NUM = "9.4"
    # velocity, acceleration and speed stay in the corner during every worked example (Adder, 2026-10-14)
    example_ref = (r"\begin{aligned}\vec v(t) &= \vec r\,'(t) = \langle x'(t),\ y'(t)\rangle\\ \vec a(t) &= \vec r\,''(t) = \langle x''(t),\ y''(t)\rangle\\"
                   r" \text{speed} &= |\vec v(t)| = \sqrt{(x')^2 + (y')^2}\end{aligned}")

    def construct(self):
        bx = lambda s: 2.5 * np.sin(1.3 * s)
        by = lambda s: 1.2 + 1.4 * np.sin(2.1 * s)
        dbx = lambda s: 2.5 * 1.3 * np.cos(1.3 * s)
        dby = lambda s: 1.4 * 2.1 * np.cos(2.1 * s)
        with self.beat("An arrow that follows the bug") as b:
            ax, _ = plot_axes([-3, 3, 1], [-0.6, 3, 1], w=7, h=4.4, coords=False)
            tt = ValueTracker(0.2)
            self.play(FadeIn(ax), Create(param_curve(ax, bx, by, 0, 3.2, color=DIM, width=2)), run_time=1)
            pos = always_redraw(lambda: Arrow(ax.c2p(0, 0), ax.c2p(bx(tt.get_value()), by(tt.get_value())), buff=0, color=FUNC, stroke_width=5))
            bug = walk_along(ladybug(0.35), ax, bx, by, tt)      # she faces her velocity (Adder, 2026-10-14)
            self.add(pos, bug)
            self.play(tt.animate.set_value(1.4), run_time=2)
            b.line(1)
            self.play(FadeIn(M(r"\vec r(t) = \langle x(t),\ y(t)\rangle", 38, FUNC).to_corner(UL, buff=0.5)), run_time=0.8)
            b.line(2)
            vel = always_redraw(lambda: Arrow(ax.c2p(bx(tt.get_value()), by(tt.get_value())), ax.c2p(bx(tt.get_value()) + 0.3 * dbx(tt.get_value()), by(tt.get_value()) + 0.3 * dby(tt.get_value())), buff=0, color=DERIV, stroke_width=5))
            self.add(vel)
            self.play(tt.animate.set_value(3.0), run_time=2.4)
        self.clear()
        self.title()

        # a brisk review of vectors before vector-valued functions (Adder, 2026-10-14)
        def grid():
            ax, _ = plot_axes([-3.5, 5.5, 1], [-2.5, 4.5, 1], w=6.3, h=4.9, coords=False)
            return ax.to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)

        def arrow(ax, p, q, color=FUNC, w=6):
            return Arrow(ax.c2p(*p), ax.c2p(*q), buff=0, color=color, stroke_width=w, max_tip_length_to_length_ratio=0.18)

        with self.beat("What a vector is") as b:
            ax = grid()
            pl = NumberPlane(x_range=[-3.5, 5.5, 1], y_range=[-2.5, 4.5, 1], x_length=6.3, y_length=4.9,
                             background_line_style={"stroke_color": DIM, "stroke_width": 1, "stroke_opacity": 0.35},
                             axis_config={"stroke_opacity": 0}).move_to(ax.c2p(1, 1))
            self.play(FadeIn(pl), FadeIn(ax), run_time=0.8)
            v = arrow(ax, (0, 0), (3, 2))
            self.play(GrowArrow(v), run_time=1.2)
            notes = VGroup(T("a vector: a length and a direction", 32), M(r"\langle 3,\ 2\rangle", 46, FUNC), T("3 right, 2 up", 30, DIM),
                           T("the same vector, drawn anywhere", 30, SECANT)).arrange(DOWN, buff=0.45).to_edge(RIGHT, buff=0.5).shift(UP * 0.6)
            self.play(FadeIn(notes[0]), run_time=0.6)
            b.line(1)
            legs = VGroup(DashedLine(ax.c2p(0, 0), ax.c2p(3, 0), color=DERIV, stroke_width=4), DashedLine(ax.c2p(3, 0), ax.c2p(3, 2), color=DERIV, stroke_width=4))
            leg_l = VGroup(M("3", 30, DERIV).next_to(legs[0], DOWN, buff=0.12), M("2", 30, DERIV).next_to(legs[1], RIGHT, buff=0.12))
            self.play(Create(legs[0]), FadeIn(leg_l[0]), run_time=0.8)
            self.play(Create(legs[1]), FadeIn(leg_l[1]), run_time=0.8)
            tag = M(r"\langle 3,\ 2\rangle", 32, FUNC).next_to(ax.c2p(3, 2), UR, buff=0.08)
            self.play(FadeIn(tag), FadeIn(notes[1:3]), run_time=0.8)
            b.line(2)
            moved = v.copy().set_color(SECANT)
            self.play(moved.animate.shift(ax.c2p(-3, 1) - ax.c2p(0, 0)), FadeOut(legs), FadeOut(leg_l), run_time=1.6)
            self.play(FadeIn(Dot(ax.c2p(-3, 1), radius=0.06, color=SECANT)), FadeIn(notes[3]), run_time=0.6)
        self.clear()

        with self.beat("Adding and scaling vectors") as b:
            ax = grid()
            self.play(FadeIn(ax), run_time=0.6)
            u = arrow(ax, (0, 0), (3, 1), FUNC)
            vt = arrow(ax, (3, 1), (4, 3), DERIV)
            ul = M(r"\vec u", 32, FUNC).next_to(ax.c2p(1.5, 0.5), DOWN, buff=0.2)
            vl = M(r"\vec v", 32, DERIV).next_to(ax.c2p(3.5, 2), RIGHT, buff=0.15)
            self.play(GrowArrow(u), FadeIn(ul), run_time=0.9)
            self.play(GrowArrow(vt), FadeIn(vl), run_time=0.9)
            board = VGroup(M(r"\langle 3,\ 1\rangle + \langle 1,\ 2\rangle", 42), M(r"= \langle 4,\ 3\rangle", 42, ACCUM)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.7).shift(UP * 1.8)
            b.line(1)
            sm = arrow(ax, (0, 0), (4, 3), ACCUM)
            sl = M(r"\vec u + \vec v", 32, ACCUM).next_to(ax.c2p(1.8, 1.35), UL, buff=0.1)
            self.play(GrowArrow(sm), FadeIn(sl), run_time=1.2)
            self.play(FadeIn(board[0]), run_time=0.6)
            self.play(FadeIn(board[1]), run_time=0.6)
            b.line(2)
            self.play(FadeOut(VGroup(u, vt, sm, ul, vl, sl)), board.animate.set_opacity(0.4), run_time=0.6)
            v1 = arrow(ax, (0, 0), (1, 2), DERIV, 8)
            v2 = arrow(ax, (0, 0), (2, 4), FUNC, 5)
            vn = arrow(ax, (0, 0), (-1, -2), SECANT, 6)
            v1l = M(r"\vec v = \langle 1,\ 2\rangle", 32, DERIV).next_to(ax.c2p(1, 2), RIGHT, buff=0.2)
            v2l = M(r"2\vec v = \langle 2,\ 4\rangle", 32, FUNC).next_to(ax.c2p(2, 4), RIGHT, buff=0.15)
            vnl = M(r"-\vec v = \langle -1,\ -2\rangle", 32, SECANT).next_to(ax.c2p(-1, -2), LEFT, buff=0.15).shift(UP * 0.25)
            self.play(GrowArrow(v1), FadeIn(v1l), run_time=0.8)
            self.play(GrowArrow(v2), FadeIn(v2l), run_time=1.2)
            self.bring_to_front(v1)
            self.play(GrowArrow(vn), FadeIn(vnl), run_time=1.0)
        self.clear()

        with self.beat("The length of a vector") as b:
            ax = grid()
            self.play(FadeIn(ax), run_time=0.6)
            v = arrow(ax, (0, 0), (4, 3), FUNC)
            legs = VGroup(Line(ax.c2p(0, 0), ax.c2p(4, 0), color=DERIV, stroke_width=4), Line(ax.c2p(4, 0), ax.c2p(4, 3), color=DERIV, stroke_width=4),
                          Square(0.22, color=DIM, stroke_width=2).move_to(ax.c2p(4, 0) + LEFT * 0.11 + UP * 0.11))
            leg_l = VGroup(M("4", 32, DERIV).next_to(legs[0], DOWN, buff=0.12), M("3", 32, DERIV).next_to(legs[1], RIGHT, buff=0.12))
            mag = M(r"|\vec v|", 32, FUNC).move_to(ax.c2p(1.6, 1.9))
            self.play(GrowArrow(v), run_time=0.9)
            self.play(Create(legs[0]), FadeIn(leg_l[0]), run_time=0.8)
            self.play(Create(legs[1]), FadeIn(leg_l[1]), FadeIn(legs[2]), run_time=0.8)
            self.play(FadeIn(mag), run_time=0.5)
            board = VGroup(M(r"|\langle a,\ b\rangle| = \sqrt{a^2 + b^2}", 42), M(r"|\langle 4,\ 3\rangle| = \sqrt{4^2 + 3^2}", 40),
                           M(r"= \sqrt{25} = 5", 40, ACCUM)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5).shift(UP * 1.2)
            b.line(1)
            self.play(Write(board[0]), run_time=1)
            b.line(2)
            self.play(FadeIn(board[1]), run_time=0.7)
            self.play(FadeIn(board[2]), run_time=0.7)
        self.clear()

        with self.beat("Position vectors") as b:
            ax = grid()
            px = lambda s: 2 + 2 * np.sin(s)
            py = lambda s: 3 - 1.4 * (1 - np.cos(s))
            tt = ValueTracker(0.0)
            P = lambda: ax.c2p(px(tt.get_value()), py(tt.get_value()))
            self.play(FadeIn(ax), run_time=0.6)
            dot = always_redraw(lambda: Dot(P(), radius=0.08, color=INK))
            pt = M(r"(2,\ 3)", 30, INK).next_to(ax.c2p(2, 3), UP, buff=0.15)
            self.play(FadeIn(dot), FadeIn(pt), run_time=0.6)
            pos = Arrow(ax.c2p(0, 0), P(), buff=0, color=FUNC, stroke_width=6, max_tip_length_to_length_ratio=0.18)
            self.play(GrowArrow(pos), run_time=1.0)
            pos.add_updater(lambda m: m.become(Arrow(ax.c2p(0, 0), P(), buff=0, color=FUNC, stroke_width=6, max_tip_length_to_length_ratio=0.18)))
            lab = M(r"\text{position vector } \langle 2,\ 3\rangle", 40, FUNC).to_edge(RIGHT, buff=0.5).shift(UP * 1.2)
            self.play(FadeIn(lab), run_time=0.6)
            b.line(1)
            trail = TracedPath(dot.get_center, stroke_color=DIM, stroke_width=3)
            self.add(trail)
            self.bring_to_front(pos, dot)
            lab2 = M(r"\vec r(t) = \langle x(t),\ y(t)\rangle", 42, FUNC).move_to(lab)
            self.play(FadeOut(pt), tt.animate.set_value(2.6), run_time=3.2)
            self.play(FadeTransform(lab, lab2), run_time=0.8)
            pos.clear_updaters()
        self.clear()

        with self.beat("Vectors made of functions") as b:
            rows = VGroup(M(r"\vec r(t) = \langle x(t),\ y(t)\rangle", 46, FUNC), T("the same information as $x = x(t)$, $y = y(t)$", 30, DIM),
                          M(r"\vec r\,'(t) = \langle x'(t),\ y'(t)\rangle = \vec v(t)", 46, DERIV), M(r"\vec r\,''(t) = \langle x''(t),\ y''(t)\rangle = \vec a(t)", 46, SECANT),
                          T("differentiate each component", 34, INK)).arrange(DOWN, buff=0.4)
            self.play(FadeIn(rows[:2]), run_time=1)
            b.line(1)
            self.play(Write(rows[2]), run_time=1)
            b.line(2)
            self.play(Write(rows[3]), FadeIn(rows[4]), run_time=1)
        self.clear()

        with self.beat("What the velocity vector means") as b:
            ax, _ = plot_axes([-3, 3, 1], [-0.6, 3, 1], w=6, h=4, coords=False)
            ax.to_edge(LEFT, buff=0.4)
            s0 = 0.9
            self.play(FadeIn(ax), Create(param_curve(ax, bx, by, 0, 3.2)), run_time=1)
            v = Arrow(ax.c2p(bx(s0), by(s0)), ax.c2p(bx(s0) + 0.35 * dbx(s0), by(s0) + 0.35 * dby(s0)), buff=0, color=DERIV, stroke_width=6)
            self.play(GrowArrow(v), run_time=0.8)
            notes = VGroup(T("direction: the way the point moves (tangent)", 30, DERIV), M(r"\text{length} = |\vec v| = \sqrt{(x')^2 + (y')^2} = \text{speed}", 34), M(r"\text{slope of the path} = \frac{y'}{x'}", 34, SECANT)).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.3)
            self.play(FadeIn(notes[0]), run_time=0.8)
            b.line(1)
            self.play(FadeIn(notes[1]), run_time=0.8)
            b.line(2)
            self.play(FadeIn(notes[2]), run_time=0.8)
        self.clear()

        X = lambda s: s * s
        Y = lambda s: s**3 - 3 * s
        ax, _ = plot_axes([-0.5, 6.5, 1], [-2.8, 4.5, 1], w=4, h=4.2)
        fig = VGroup(ax, param_curve(ax, X, Y, -2, 2.2), Arrow(ax.c2p(4, 2), ax.c2p(4 + 0.25 * 4, 2 + 0.25 * 9), buff=0, color=DERIV, stroke_width=5), Dot(ax.c2p(4, 2), color=INK))
        self.example("Velocity and acceleration at a time", r"$\vec r(t) = \langle t^2,\ t^3 - 3t\rangle$. Find the velocity, acceleration, and speed at $t = 2$.",
                     [r"\vec v(t) = \vec r\,'(t) = \langle 2t,\ 3t^2 - 3\rangle", r"\vec v(2) = \langle 4,\ 9\rangle", r"\vec a(t) = \vec r\,''(t) = \langle 2,\ 6t\rangle", r"\vec a(2) = \langle 2,\ 12\rangle",
                      r"\text{speed} = |\vec v(2)| = \sqrt{4^2 + 9^2} = \sqrt{97} \approx 9.85"], at=[1, 2, 3, 3, 4], figure=fig, figure_at=2, follow=True)

        with self.beat("Close") as b:
            card = VGroup(M(r"\vec r(t) = \langle x(t),\ y(t)\rangle", 42, FUNC), M(r"\vec v = \vec r\,' = \langle x', y'\rangle: \ \text{tangent, length} = \text{speed}", 38, DERIV),
                          M(r"\vec a = \vec r\,'' = \langle x'', y''\rangle", 40, SECANT), T("differentiate componentwise", 36)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        ax, _ = plot_axes([-1.6, 1.6, 1], [-1.6, 1.6, 1], w=3.4, h=3.4, coords=False)
        s1 = 0.7
        P = ax.c2p(np.cos(s1), np.sin(s1))
        fig1 = VGroup(ax, param_curve(ax, np.cos, np.sin, 0, TAU), Arrow(ax.c2p(0, 0), P, buff=0, color=FUNC, stroke_width=4),
                      Arrow(P, ax.c2p(np.cos(s1) - 0.6 * np.sin(s1), np.sin(s1) + 0.6 * np.cos(s1)), buff=0, color=DERIV, stroke_width=4),
                      Arrow(P, ax.c2p(0.4 * np.cos(s1), 0.4 * np.sin(s1)), buff=0, color=SECANT, stroke_width=4))
        self.example("Example 1: Around the circle", r"$\vec r(t) = \langle \cos t,\ \sin t\rangle$. Find $\vec v(t)$ and $\vec a(t)$, and describe their directions.",
                     [r"\vec v(t) = \langle -\sin t,\ \cos t\rangle", r"\vec r \cdot \vec v = -\cos t\sin t + \sin t\cos t = 0", r"TEXT:So $\vec v$ is perpendicular to $\vec r$ (tangent), and $|\vec v| = 1$.",
                      r"\vec a(t) = \langle -\cos t,\ -\sin t\rangle = -\vec r(t)", r"TEXT:The acceleration points to the center."], at=[1, 1, 1, 2, 2], figure=fig1)
        self.example("Example 2: Mixed components", r"$\vec r(t) = \langle e^{2t},\ \ln(t + 1)\rangle$. Find $\vec v(0)$ and $\vec a(0)$.",
                     [r"\vec v(t) = \left\langle 2e^{2t},\ \tfrac{1}{t + 1}\right\rangle", r"\vec v(0) = \langle 2,\ 1\rangle", r"\vec a(t) = \left\langle 4e^{2t},\ -\tfrac{1}{(t + 1)^2}\right\rangle", r"\vec a(0) = \langle 4,\ -1\rangle"], at=[1, 1, 2, 2])
        self.example("Example 3: Which way is it moving?", r"$\vec r(t) = \langle t^2 - 4t,\ t^3\rangle$. At $t = 1$, is the particle moving left or right? Up or down?",
                     [r"\vec v(t) = \langle 2t - 4,\ 3t^2\rangle", r"\vec v(1) = \langle -2,\ 3\rangle", r"x' < 0: \text{ moving left}; \quad y' > 0: \text{ moving up}"], at=[1, 1, 2])
        self.finish()
