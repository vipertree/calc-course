"""Topic 9.7 (BC): Polar coordinates and polar derivatives. Narration comes from transcripts/9_7.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "9.7"

    def construct(self):
        with self.beat("A different way to say where") as b:
            sea = Rectangle(width=14, height=8, stroke_width=0, fill_color=WATER_HI, fill_opacity=0.5)
            ax, _ = plot_axes([-1, 6, 1], [-1, 5, 1], w=6, h=5)
            ax.shift(LEFT * 1.5)
            lh = lighthouse(1.2).move_to(ax.c2p(0, 0), aligned_edge=DOWN)
            boat = VGroup(Polygon([-0.3, 0, 0], [0.3, 0, 0], [0.22, -0.15, 0], [-0.22, -0.15, 0], stroke_color=INK, fill_color=WOOD, fill_opacity=1),
                          Polygon([0, 0, 0], [0, 0.4, 0], [0.22, 0.05, 0], stroke_color=INK, fill_color=PANEL, fill_opacity=1)).move_to(ax.c2p(3, 4))
            self.play(FadeIn(sea), FadeIn(ax), FadeIn(lh), FadeIn(boat), run_time=1)
            grid = VGroup(DashedLine(ax.c2p(0, 0), ax.c2p(3, 0), color=SECANT), DashedLine(ax.c2p(3, 0), ax.c2p(3, 4), color=SECANT))
            self.play(Create(grid), FadeIn(T("3 east, 4 north: $(x, y)$", 32, SECANT).to_edge(RIGHT, buff=0.5).shift(UP * 1.4)), run_time=1)
            b.line(1)
            beam = Line(ax.c2p(0, 0), ax.c2p(3, 4), color="#F6C945", stroke_width=8)
            arc = Arc(radius=0.8, start_angle=0, angle=np.arctan2(4, 3), arc_center=ax.c2p(0, 0), color=DERIV)
            self.play(Create(beam), Create(arc), FadeIn(M(r"\theta", 32, DERIV).move_to(ax.c2p(1.1, 0.4))), FadeIn(T("5 out along the beam: $(r, \\theta)$", 32, DERIV).to_edge(RIGHT, buff=0.5).shift(UP * 0.4)), run_time=1.2)
            b.line(2)
        self.clear()
        self.title()

        with self.beat("Converting between the two") as b:
            ax, _ = plot_axes([-0.5, 3, 1], [-0.5, 2.5, 1], w=4.6, h=4)
            ax.to_edge(LEFT, buff=0.8)
            P = ax.c2p(1, np.sqrt(3))
            tri = VGroup(Line(ax.c2p(0, 0), P, color=FUNC, stroke_width=5), DashedLine(P, ax.c2p(1, 0), color=DIM), Line(ax.c2p(0, 0), ax.c2p(1, 0), color=DIM, stroke_width=4))
            self.play(FadeIn(ax), Create(tri), FadeIn(Dot(P, color=FUNC)), FadeIn(M("r", 32, FUNC).next_to(tri[0].get_center(), UL, buff=0.1)),
                      FadeIn(M(r"\theta", 30, DERIV).move_to(ax.c2p(0.35, 0.15))), run_time=1)
            board = VGroup(M(r"x = r\cos\theta, \quad y = r\sin\theta", 40), M(r"r^2 = x^2 + y^2, \quad \tan\theta = \tfrac yx", 40), M(r"(r, \theta) = \left(2, \tfrac\pi3\right) \ \to\ \left(1, \sqrt3\right)", 38, SECANT)).arrange(DOWN, buff=0.5).to_edge(RIGHT, buff=0.5)
            self.play(Write(board[0]), run_time=1)
            b.line(1)
            self.play(Write(board[1]), run_time=1)
            b.line(2)
            self.play(Write(board[2]), run_time=1)
        self.clear()

        with self.beat("Polar curves") as b:
            panels = VGroup()
            for f, t1, lab in ((lambda s: 2 + 0 * s, TAU, "r = 2"), (lambda s: s / 2.2, 3 * PI, r"r = \theta"), (lambda s: 1 + np.cos(s), TAU, r"r = 1 + \cos\theta")):
                ax, _ = plot_axes([-2.5, 2.5, 1], [-2.5, 2.5, 1], w=3.4, h=3.4, coords=False)
                panels.add(VGroup(ax, polar_curve(ax, f, 0, t1), M(lab, 32).next_to(ax, DOWN, buff=0.2)))
            panels.arrange(RIGHT, buff=0.5)
            self.play(FadeIn(panels[0][0]), Create(panels[0][1]), FadeIn(panels[0][2]), run_time=1.2)
            b.line(1)
            for p in panels[1:]:
                self.play(FadeIn(p[0]), Create(p[1]), FadeIn(p[2]), run_time=1.4)
        self.clear()

        with self.beat("Slopes of polar curves") as b:
            rows = VGroup(M(r"r = f(\theta): \quad x = f(\theta)\cos\theta, \quad y = f(\theta)\sin\theta", 38), T("polar is parametric, with parameter $\\theta$", 30, DIM),
                          formula_box(M(r"\frac{dy}{dx} = \frac{dy/d\theta}{dx/d\theta}", 48, ACCUM), ACCUM),
                          M(r"\tfrac{dx}{d\theta} = f'(\theta)\cos\theta - f(\theta)\sin\theta, \quad \tfrac{dy}{d\theta} = f'(\theta)\sin\theta + f(\theta)\cos\theta", 32),
                          M(r"\frac{dy}{dx} \ne \frac{dr}{d\theta}", 40, TANGENT)).arrange(DOWN, buff=0.4)
            self.play(Write(rows[0]), FadeIn(rows[1]), run_time=1.2)
            b.line(1)
            self.play(FadeIn(rows[2]), Write(rows[3]), run_time=1.4)
            b.line(2)
            self.play(FadeIn(rows[4]), run_time=0.8)
        self.clear()

        car = lambda s: 1 + np.cos(s)
        ax, _ = plot_axes([-0.8, 2.4, 1], [-1.6, 1.6, 1], w=3.8, h=3.8)
        fig = VGroup(ax, polar_curve(ax, car, 0, TAU), Dot(ax.c2p(0, 1), color=TANGENT), Line(ax.c2p(-1, 0), ax.c2p(0.6, 1.6), color=TANGENT, stroke_width=4))
        self.example("The cardioid's tangent line", r"Find the slope of $r = 1 + \cos\theta$ at $\theta = \frac\pi2$, and the tangent line there.",
                     [r"x = (1 + \cos\theta)\cos\theta, \quad y = (1 + \cos\theta)\sin\theta", r"\tfrac{dx}{d\theta} = -\sin\theta\cos\theta - (1 + \cos\theta)\sin\theta = -\sin\theta(1 + 2\cos\theta)",
                      r"\tfrac{dy}{d\theta} = -\sin^2\theta + (1 + \cos\theta)\cos\theta = \cos\theta + \cos 2\theta", r"\theta = \tfrac\pi2: \ \tfrac{dx}{d\theta} = -1, \ \ \tfrac{dy}{d\theta} = 0 + \cos\pi = -1",
                      r"\frac{dy}{dx} = \frac{-1}{-1} = 1", r"r = 1: \ \text{point } (0, 1); \quad y - 1 = x"], at=[1, 2, 3, 4, 5, 5], figure=fig, figure_at=5)

        with self.beat("What dr/dθ tells you") as b:
            ax, _ = plot_axes([-0.8, 2.4, 1], [-1.6, 1.6, 1], w=4.6, h=4.6, coords=False)
            ax.to_edge(LEFT, buff=0.8)
            th = ValueTracker(0.3)
            rad = always_redraw(lambda: Line(ax.c2p(0, 0), ax.c2p(car(th.get_value()) * np.cos(th.get_value()), car(th.get_value()) * np.sin(th.get_value())), color=SECANT, stroke_width=5))
            self.play(FadeIn(ax), Create(polar_curve(ax, car, 0, TAU)), run_time=1)
            self.add(rad)
            self.play(th.animate.set_value(2.6), run_time=2)
            b.line(1)
            notes = VGroup(M(r"\tfrac{dr}{d\theta} > 0: \ \text{moving away from the origin}", 34, DERIV), M(r"\tfrac{dr}{d\theta} < 0: \ \text{moving toward the origin}", 34, TANGENT),
                           T("(when $r > 0$)", 28, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4)
            self.play(FadeIn(notes), run_time=1)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(M(r"x = r\cos\theta, \ \ y = r\sin\theta, \ \ r^2 = x^2 + y^2", 40), T("$r = f(\\theta)$ is parametric in $\\theta$", 34), formula_box(M(r"\frac{dy}{dx} = \frac{dy/d\theta}{dx/d\theta}", 46, ACCUM), ACCUM),
                          T("$\\frac{dr}{d\\theta}$: toward or away from the origin", 34, SECANT)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        ax, _ = plot_axes([-2.5, 2.5, 1], [-0.5, 4.5, 1], w=3.2, h=3.6)
        fig1 = VGroup(ax, polar_curve(ax, lambda s: 4 * np.sin(s), 0, PI))
        self.example("Example 1: Converting a polar equation", r"Write $r = 4\sin\theta$ in rectangular form and identify the curve.",
                     [r"r^2 = 4r\sin\theta", r"x^2 + y^2 = 4y", r"x^2 + y^2 - 4y + 4 = 4", r"x^2 + (y - 2)^2 = 4", r"\text{a circle, radius } 2, \text{ center } (0, 2)"], at=[1, 1, 2, 2, 2], figure=fig1)
        self.example("Example 2: A spiral's slope", r"Find the slope of $r = \theta$ at $\theta = \frac\pi2$.",
                     [r"x = \theta\cos\theta, \ \ y = \theta\sin\theta", r"\tfrac{dx}{d\theta} = \cos\theta - \theta\sin\theta, \ \ \tfrac{dy}{d\theta} = \sin\theta + \theta\cos\theta", r"\theta = \tfrac\pi2: \ \tfrac{dx}{d\theta} = -\tfrac\pi2, \ \ \tfrac{dy}{d\theta} = 1",
                      r"\frac{dy}{dx} = \frac{1}{-\pi/2} = -\frac2\pi \approx -0.64"], at=[1, 1, 2, 3])
        self.example("Example 3: Toward or away?", r"For $r = 1 + 2\sin\theta$, is the curve moving toward or away from the origin at $\theta = \frac\pi3$?",
                     [r"r\left(\tfrac\pi3\right) = 1 + \sqrt3 > 0", r"\tfrac{dr}{d\theta} = 2\cos\theta = 2 \cdot \tfrac12 = 1 > 0", r"TEXT:$r$ is positive and increasing: moving away from the origin."], at=[1, 2, 3])
        self.finish()
