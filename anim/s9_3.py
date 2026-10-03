"""Topic 9.3 (BC): Arc length of parametric curves. Narration comes from transcripts/9_3.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "9.3"

    def construct(self):
        bx = lambda s: 2.5 * np.sin(1.3 * s)
        by = lambda s: 2 * np.sin(2.1 * s)
        with self.beat("How far did it go?") as b:
            ax, _ = plot_axes([-3, 3, 1], [-2.6, 2.6, 1], w=6, h=4.8, coords=False)
            ax.to_edge(LEFT, buff=0.6)
            path = param_curve(ax, bx, by, 0, 3)
            bug = ladybug(0.4).move_to(ax.c2p(0, 0))
            pedo = VGroup(RoundedRectangle(width=2.2, height=0.9, corner_radius=0.15, stroke_color=INK), T("pedometer", 24, DIM)).arrange(DOWN, buff=0.1).to_corner(UR, buff=0.6)
            self.play(FadeIn(ax), FadeIn(bug), FadeIn(pedo), run_time=0.8)
            self.play(Create(path), MoveAlongPath(bug, path), run_time=2.6, rate_func=linear)
            old = VGroup(M(r"L = \int \sqrt{1 + [f'(x)]^2}\,dx", 34), M("?", 48, TANGENT)).arrange(RIGHT, buff=0.3).next_to(pedo, DOWN, buff=0.8)
            self.play(FadeIn(old), run_time=0.8)
            b.line(1)
            b.line(2)
        self.clear()
        self.title()

        with self.beat("Tiny hypotenuses in time") as b:
            p, q = np.array([-4.6, -0.6, 0]), np.array([-2.6, 0.8, 0])
            c = np.array([q[0], p[1], 0])
            tri = VGroup(Line(p, c, color=DIM, stroke_width=4), Line(c, q, color=DIM, stroke_width=4), Line(p, q, color=SECANT, stroke_width=5))
            self.play(Create(tri), FadeIn(M("dx", 30).next_to(tri[0], DOWN, buff=0.1)), FadeIn(M("dy", 30).next_to(tri[1], RIGHT, buff=0.1)), FadeIn(M("ds", 30, SECANT).next_to(tri[2].get_center(), UL, buff=0.1)),
                      FadeIn(T("all in time $dt$", 28, DIM).next_to(tri, DOWN, buff=0.6)), run_time=1)
            rows = [r"ds^2 = dx^2 + dy^2", r"\left(\tfrac{ds}{dt}\right)^2 = \left(\tfrac{dx}{dt}\right)^2 + \left(\tfrac{dy}{dt}\right)^2", r"ds = \sqrt{\left(\tfrac{dx}{dt}\right)^2 + \left(\tfrac{dy}{dt}\right)^2}\,dt"]
            board = VGroup(*[M(r, 36) for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4).shift(UP * 1.3)
            b.line(1)
            self.play(Write(board[0]), run_time=0.8)
            self.play(Write(board[1]), run_time=1)
            b.line(2)
            self.play(Write(board[2]), run_time=1)
            box = formula_box(M(r"L = \int_a^b \sqrt{\left(\tfrac{dx}{dt}\right)^2 + \left(\tfrac{dy}{dt}\right)^2}\,dt", 40, ACCUM), ACCUM).next_to(board, DOWN, buff=0.5)
            self.play(FadeIn(box), run_time=0.8)
            b.line(3)
            self.play(FadeIn(T("the integrand is the speed: length $= \\int$ speed $dt$", 30, DERIV).next_to(box, DOWN, buff=0.3)), run_time=0.8)
        self.clear()

        with self.beat("A check with a circle") as b:
            ax, _ = plot_axes([-1.4, 1.4, 1], [-1.4, 1.4, 1], w=3.6, h=3.6, coords=False)
            ax.to_edge(LEFT, buff=1)
            self.play(FadeIn(ax), Create(param_curve(ax, np.cos, np.sin, 0, TAU)), FadeIn(M("r", 30).move_to(ax.c2p(0.5, 0.15))), run_time=1)
            rows = VGroup(M(r"\tfrac{dx}{dt} = -r\sin t, \ \ \tfrac{dy}{dt} = r\cos t", 36), M(r"r^2\left(\sin^2 t + \cos^2 t\right) = r^2", 36), M(r"L = \int_0^{2\pi} r\,dt = 2\pi r", 40, ACCUM)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.6)
            self.play(Write(rows[0]), run_time=1)
            b.line(1)
            self.play(Write(rows[1]), run_time=1)
            b.line(2)
            self.play(Write(rows[2]), FadeIn(M(r"\checkmark", 56, GRASS).next_to(rows[2], DOWN, buff=0.3)), run_time=1)
        self.clear()

        self.example("An exact length", r"Find the length of the curve $x = t^2$, $y = \frac23t^3$ for $0 \le t \le \sqrt3$.",
                     [r"\tfrac{dx}{dt} = 2t, \ \ \tfrac{dy}{dt} = 2t^2", r"\left(\tfrac{dx}{dt}\right)^2 + \left(\tfrac{dy}{dt}\right)^2 = 4t^2 + 4t^4", r"= 4t^2\left(1 + t^2\right)",
                      r"\sqrt{4t^2(1 + t^2)} = 2t\sqrt{1 + t^2} \ \ (t \ge 0)", r"L = \int_0^{\sqrt3} 2t\sqrt{1 + t^2}\,dt", r"u = 1 + t^2, \ du = 2t\,dt, \ u: 1 \to 4",
                      r"= \int_1^4 \sqrt u\,du = \left[\tfrac23u^{3/2}\right]_1^4", r"= \tfrac23(8 - 1) = \tfrac{14}{3} \approx 4.67"], at=[1, 2, 2, 3, 4, 4, 5, 5])

        with self.beat("Close") as b:
            card = VGroup(formula_box(M(r"L = \int_a^b \sqrt{\left(\tfrac{dx}{dt}\right)^2 + \left(\tfrac{dy}{dt}\right)^2}\,dt", 44, ACCUM), ACCUM), T("the integrand is the speed", 34, DERIV),
                          T("check: a circle gives $2\\pi r$", 34), T("usually: set up, then calculator", 34, SECANT)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Half a circle", r"Find the length of $x = 3\cos t$, $y = 3\sin t$ for $0 \le t \le \pi$.",
                     [r"\tfrac{dx}{dt} = -3\sin t, \ \ \tfrac{dy}{dt} = 3\cos t", r"\left(\tfrac{dx}{dt}\right)^2 + \left(\tfrac{dy}{dt}\right)^2 = 9", r"L = \int_0^\pi 3\,dt = 3\pi \approx 9.42"], at=[1, 1, 2])
        ax, _ = plot_axes([-0.3, 6.6, 1], [-0.3, 2.4, 1], w=5.6, h=2.4, coords=False)
        fig2 = VGroup(ax, param_curve(ax, lambda s: s - np.sin(s), lambda s: 1 - np.cos(s), 0, TAU), Circle(radius=(ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]), color=DIM).move_to(ax.c2p(np.pi, 1)))
        self.example("Example 2: One arch of a cycloid", r"Find the length of one arch of the cycloid $x = t - \sin t$, $y = 1 - \cos t$, $0 \le t \le 2\pi$.",
                     [r"\tfrac{dx}{dt} = 1 - \cos t, \ \ \tfrac{dy}{dt} = \sin t", r"1 - 2\cos t + \cos^2 t + \sin^2 t = 2 - 2\cos t", r"2 - 2\cos t = 4\sin^2\tfrac t2",
                      r"\sqrt{\ } = 2\sin\tfrac t2 \ \ (\ge 0 \text{ on } [0, 2\pi])", r"L = \int_0^{2\pi} 2\sin\tfrac t2\,dt = \left[-4\cos\tfrac t2\right]_0^{2\pi} = 4 + 4 = 8"], at=[1, 1, 2, 2, 3], figure=fig2)
        self.example("Example 3: A calculator length", r"Find the length of $x = e^t$, $y = t$ for $0 \le t \le 1$.",
                     [r"\tfrac{dx}{dt} = e^t, \ \ \tfrac{dy}{dt} = 1", r"L = \int_0^1 \sqrt{e^{2t} + 1}\,dt", r"\approx 2.003 \ \ (\text{calculator})"], at=[1, 1, 2])
        self.finish()
