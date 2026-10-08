"""Topic 9.4 (BC): Vector-valued functions and their derivatives. Narration comes from transcripts/9_4.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "9.4"

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
            bug = always_redraw(lambda: ladybug(0.35).move_to(ax.c2p(bx(tt.get_value()), by(tt.get_value()))))
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
