"""Topic 9.1 (BC): Parametric equations and their derivatives. Narration comes from transcripts/9_1.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "9.1"

    def construct(self):
        X = lambda s: s * s - 1
        Y = lambda s: s**3 - 3 * s
        with self.beat("A path with a clock") as b:
            ax, _ = plot_axes([-4, 4, 1], [-3, 3, 1], w=7.4, h=5, coords=False)
            ax.shift(LEFT * 1)
            bx = lambda s: 2.5 * np.sin(1.3 * s)
            by = lambda s: 2 * np.sin(2.1 * s)
            trail = param_curve(ax, bx, by, 0, 4.2, color=FUNC)
            bug = ladybug(0.45).move_to(ax.c2p(bx(0), by(0)))
            clock = VGroup(Circle(radius=0.5, stroke_color=INK, stroke_width=3), M("t", 32)).to_corner(UR, buff=0.6)
            self.play(FadeIn(ax), FadeIn(bug), FadeIn(clock), run_time=0.8)
            self.play(Create(trail), MoveAlongPath(bug, trail), run_time=3, rate_func=linear)
            b.line(1)
            stamps = VGroup(*[Dot(ax.c2p(bx(s), by(s)), color=SECANT) for s in (0, 1, 2, 3, 4)])
            self.play(FadeIn(stamps), FadeIn(M(r"(x(t),\ y(t))", 40, SECANT).next_to(clock, DOWN, buff=0.4)), run_time=1)
            b.line(2)
            self.play(FadeIn(VGroup(M(r"x = x(t)", 36), M(r"y = y(t)", 36)).arrange(DOWN, buff=0.2).to_edge(RIGHT, buff=0.6)), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("Plotting a parametric curve") as b:
            ts = [-2, -1, 0, 1, 2]
            tab = table(["t", "x = t^2 - 1", "y = t^3 - 3t"], [[str(s), str(X(s)), str(Y(s))] for s in ts], size=32).to_edge(LEFT, buff=0.5)
            ax, al = plot_axes([-1.6, 3.6, 1], [-2.8, 2.8, 1], w=5, h=5)
            VGroup(ax, al).to_edge(RIGHT, buff=0.5)
            self.play(FadeIn(tab), FadeIn(ax), FadeIn(al), run_time=1)
            dots = VGroup(*[Dot(ax.c2p(X(s), Y(s)), color=SECANT) for s in ts])
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in dots], lag_ratio=0.3), run_time=1.4)
            curve = param_curve(ax, X, Y, -2.1, 2.1)
            arrows = VGroup(*[Arrow(ax.c2p(X(s), Y(s)), ax.c2p(X(s + 0.15), Y(s + 0.15)), buff=0, color=FUNC, stroke_width=4, max_tip_length_to_length_ratio=0.9) for s in (-1.5, -0.5, 0.5, 1.5)])
            b.line(1)
            self.play(Create(curve), FadeIn(arrows), run_time=1.6)
            b.line(2)
            self.play(Indicate(dots[1]), Indicate(dots[3]), run_time=1)
        self.clear()

        with self.beat("The slope of a parametric curve") as b:
            rows = [r"\frac{dy}{dt} = \frac{dy}{dx}\cdot\frac{dx}{dt}", r"\frac{dy}{dx} = \frac{dy/dt}{dx/dt}"]
            r1 = M(rows[0], 50).shift(UP * 1.6)
            self.play(Write(r1), run_time=1)
            b.line(1)
            box = formula_box(VGroup(M(rows[1], 54, ACCUM), T(r"provided $\frac{dx}{dt} \ne 0$", 28, DIM)).arrange(DOWN, buff=0.2), ACCUM)
            self.play(FadeIn(box), run_time=1)
            b.line(2)
            ax, _ = plot_axes([0, 3, 1], [0, 2, 1], w=3.4, h=2.2, coords=False)
            ax.to_edge(DOWN, buff=0.4)
            p, q = ax.c2p(0.8, 0.6), ax.c2p(2.0, 1.5)
            c = np.array([q[0], p[1], 0])
            self.play(FadeIn(ax), Create(Line(p, q, color=FUNC, stroke_width=5)), Create(Line(p, c, color=DIM)), Create(Line(c, q, color=DIM)),
                      FadeIn(M("dx", 28).next_to(Line(p, c), DOWN, buff=0.08)), FadeIn(M("dy", 28).next_to(Line(c, q), RIGHT, buff=0.08)), run_time=1)
        self.clear()

        ax, _ = plot_axes([-1.6, 4.4, 1], [-2.8, 3.6, 1], w=4.2, h=4.4)
        fig = VGroup(ax, param_curve(ax, X, Y, -2.1, 2.15), Dot(ax.c2p(3, 2), color=TANGENT), Line(ax.c2p(1.2, 2 - 9 / 4 * 1.8), ax.c2p(4.2, 2 + 9 / 4 * 1.2), color=TANGENT, stroke_width=4))
        self.example("A tangent line", r"For $x = t^2 - 1$, $y = t^3 - 3t$, find $\frac{dy}{dx}$ and the equation of the tangent line at $t = 2$.",
                     [r"\frac{dx}{dt} = 2t", r"\frac{dy}{dt} = 3t^2 - 3", r"\frac{dy}{dx} = \frac{3t^2 - 3}{2t}", r"t = 2: \ \frac{dy}{dx} = \frac{12 - 3}{4} = \frac94",
                      r"x(2) = 3, \ \ y(2) = 8 - 6 = 2", r"y - 2 = \tfrac94(x - 3)"], at=[1, 1, 2, 3, 4, 5], figure=fig, figure_at=4, follow=True)

        with self.beat("Horizontal and vertical tangents") as b:
            ax, al = plot_axes([-1.6, 3.6, 1], [-2.8, 2.8, 1], w=4.8, h=4.8)
            VGroup(ax, al).to_edge(LEFT, buff=0.6)
            self.play(FadeIn(ax), FadeIn(al), Create(param_curve(ax, X, Y, -2.1, 2.1)), run_time=1)
            board = VGroup(M(r"\text{horizontal: } \tfrac{dy}{dt} = 0, \ \tfrac{dx}{dt} \ne 0", 34, DERIV), M(r"\text{vertical: } \tfrac{dx}{dt} = 0, \ \tfrac{dy}{dt} \ne 0", 34, SECANT),
                           T("both $0$: look closer", 30, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4).shift(UP * 1.4)
            self.play(Write(board[0]), run_time=1)
            b.line(1)
            self.play(Write(board[1]), FadeIn(board[2]), run_time=1)
            b.line(2)
            hs = VGroup(*[Line(ax.c2p(-0.7, yy), ax.c2p(0.7, yy), color=DERIV, stroke_width=5) for yy in (-2, 2)])
            vs = Line(ax.c2p(-1, -0.8), ax.c2p(-1, 0.8), color=SECANT, stroke_width=5)
            notes = VGroup(M(r"t = \pm1: \ (0, -2), \ (0, 2)", 32, DERIV), M(r"t = 0: \ (-1, 0)", 32, SECANT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(board, DOWN, buff=0.6)
            self.play(Create(hs), FadeIn(notes[0]), run_time=1)
            self.play(Create(vs), FadeIn(notes[1]), run_time=1)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(M(r"x = x(t), \ \ y = y(t): \ t \text{ is the parameter}", 40), formula_box(M(r"\frac{dy}{dx} = \frac{dy/dt}{dx/dt}", 50, ACCUM), ACCUM),
                          M(r"\text{horizontal: } \tfrac{dy}{dt} = 0; \quad \text{vertical: } \tfrac{dx}{dt} = 0", 38, SECANT)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        ax, _ = plot_axes([-1.4, 1.4, 1], [-1.4, 1.4, 1], w=3.4, h=3.4, coords=False)
        r2 = np.sqrt(2) / 2
        fig1 = VGroup(ax, param_curve(ax, np.cos, np.sin, 0, TAU), Dot(ax.c2p(r2, r2), color=TANGENT), Line(ax.c2p(r2 - 0.6, r2 + 0.6), ax.c2p(r2 + 0.6, r2 - 0.6), color=TANGENT, stroke_width=4))
        self.example("Example 1: Around a circle", r"For $x = \cos t$, $y = \sin t$, find $\frac{dy}{dx}$ and the slope at $t = \frac\pi4$.",
                     [r"\frac{dx}{dt} = -\sin t, \ \ \frac{dy}{dt} = \cos t", r"\frac{dy}{dx} = \frac{\cos t}{-\sin t} = -\cot t", r"t = \tfrac\pi4: \ -\cot\tfrac\pi4 = -1"], at=[1, 2, 2], figure=fig1)
        self.example("Example 2: Finding the tangents", r"Find the points where $x = t^2 - 2t$, $y = t^3 - 12t$ has horizontal or vertical tangents.",
                     [r"\frac{dy}{dt} = 3t^2 - 12 = 0 \text{ at } t = \pm2, \text{ where } \frac{dx}{dt} = 2t - 2 \ne 0", r"t = 2: \ (0, -16); \quad t = -2: \ (8, 16) \quad \text{(horizontal)}",
                      r"\frac{dx}{dt} = 2t - 2 = 0 \text{ at } t = 1, \text{ where } \frac{dy}{dt} = -9 \ne 0", r"t = 1: \ (-1, -11) \quad \text{(vertical)}"], at=[1, 1, 2, 3])
        self.example("Example 3: Eliminating the parameter", r"Write $x = 2t + 1$, $y = t^2$ as an equation in $x$ and $y$, and check the slope both ways.",
                     [r"t = \tfrac{x - 1}{2}", r"y = \left(\tfrac{x - 1}{2}\right)^2 = \tfrac{(x - 1)^2}{4}", r"\frac{dy}{dx} = \tfrac{x - 1}{2}", r"\text{parametric: } \frac{dy}{dx} = \frac{2t}{2} = t = \tfrac{x - 1}{2}"], at=[1, 2, 3, 3])
        self.finish()
