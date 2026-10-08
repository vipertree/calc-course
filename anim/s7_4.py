"""Topic 7.4: Reasoning using slope fields. Narration comes from transcripts/7_4.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def logistic(y0):
    """Solution of y' = y(2 - y) with y(0) = y0 (y0 != 0, 2)."""
    A = (2 - y0) / y0
    return lambda x: 2 / (1 + A * np.exp(-2 * x))


class Lesson(TranscriptScene):
    NUM = "7.4"

    def make_field(self):
        ax, al = plot_axes([-2, 6, 1], [-1, 3, 1], w=8.4, h=5.2, coords=False)
        VGroup(ax, al).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        field = slope_field(ax, lambda x, y: y * (2 - y), np.arange(-1.5, 6, 0.5), np.arange(-0.75, 3.1, 0.25), length=0.3)
        return ax, al, field

    def construct(self):
        f = lambda x, y: y * (2 - y)
        ax, al, field = self.make_field()
        de = M(r"\frac{dy}{dx} = y(2 - y)", 40, ACCUM).to_corner(UR, buff=0.5)
        with self.beat("Reading the field") as b:
            self.play(FadeIn(ax), FadeIn(al), FadeIn(field), Write(de), run_time=1.4)
            b.line(1)
            eq = VGroup(DashedLine(ax.c2p(-2, 0), ax.c2p(6, 0), color=TANGENT, stroke_width=4), DashedLine(ax.c2p(-2, 2), ax.c2p(6, 2), color=DERIV, stroke_width=4))
            self.play(Create(eq), run_time=0.8)
            b.line(2)
            for y0, col, xr in ((1, FUNC, [-2, 6]), (3, SECANT, [0, 6])):          # y0 = 3 leaves the axes for x < 0
                g = logistic(y0)
                self.play(Create(ax.plot(g, x_range=xr, color=col, stroke_width=5)), run_time=1.2)
            low = lambda x: 2 / (1 - (2.3 / 0.3) * np.exp(-2 * x))
            self.play(Create(ax.plot(low, x_range=[-2, 0.46], color=TANGENT, stroke_width=5)), run_time=1)    # reaches y = -1 at x = 0.47
        self.clear()
        self.title()

        ax, al, field = self.make_field()
        with self.beat("Sketching a particular solution") as b:
            self.play(FadeIn(ax), FadeIn(al), FadeIn(field), run_time=0.8)
            dot = Dot(ax.c2p(0, 1), color=SECANT, radius=0.1)
            self.play(FadeIn(dot), FadeIn(T("start at the point", 28, SECANT).next_to(dot, UR, buff=0.1)), run_time=0.6)
            b.line(1)
            g = logistic(1)
            self.play(Create(ax.plot(g, x_range=[0, 6], color=FUNC, stroke_width=5)), run_time=1.4)
            self.play(Create(ax.plot(g, x_range=[0, -2], color=FUNC, stroke_width=5)), run_time=1.2)
            b.line(2)
            self.play(FadeIn(T("follow the segments; never cut across them", 28, DIM).to_corner(UR, buff=0.4)), run_time=0.6)
        self.clear()

        ax, al, field = self.make_field()
        with self.beat("Equilibrium solutions") as b:
            self.play(FadeIn(ax), FadeIn(al), FadeIn(field), run_time=0.8)
            txt = VGroup(T(r"$\frac{dy}{dx} = 0$ whenever $y = c$:", 30), T("$y = c$ is a solution", 30, ACCUM)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.4)
            self.play(FadeIn(txt), Create(Line(ax.c2p(-2, 2), ax.c2p(6, 2), color=DERIV, stroke_width=6)), run_time=1)
            b.line(1)
            self.play(Create(Line(ax.c2p(-2, 0), ax.c2p(6, 0), color=TANGENT, stroke_width=6)), FadeIn(M(r"y = 0, \ \ y = 2", 34, ACCUM).next_to(txt, DOWN, buff=0.3)), run_time=0.8)
            b.line(2)
            for y0 in (0.4, 1.2, 2.6, 3.0):
                self.play(Create(ax.plot(logistic(y0), x_range=[0, 6], color=FUNC, stroke_width=3)), run_time=0.6)
            self.play(FadeIn(M(r"\lim_{x\to\infty} y = 2", 36, DERIV).next_to(txt, DOWN, buff=1.0)), run_time=0.6)
        self.clear()

        self.example("Concavity from the equation", r"$\dfrac{dy}{dx} = y(2 - y)$. (a) Find $\dfrac{d^2y}{dx^2}$ in terms of $y$. (b) Is the solution through $(0, 1.5)$ concave up or down there?",
                     [r"\frac{dy}{dx} = 2y - y^2", r"\frac{d^2y}{dx^2} = (2 - 2y)\frac{dy}{dx}", r"= (2 - 2y) \cdot y(2 - y)", r"y = 1.5: \ (2 - 3)(1.5)(0.5) = -0.75 < 0: \ \text{concave down}"],
                     at=[1, 2, 3, 4])

        with self.beat("Close") as b:
            card = VGroup(T("Sketch through a point: follow the segments both ways.", 34), T(r"Equilibrium: $y = c$ with $\frac{dy}{dx} = 0$ for all $x$.", 34, ACCUM),
                          T("Long run: read where solutions level off.", 34), T(r"Concavity: $\frac{d^2y}{dx^2}$, differentiating implicitly, then substituting $\frac{dy}{dx}$.", 32, SECANT)).arrange(DOWN, buff=0.45)
            card.set_max_width(12.8)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Equilibrium solutions", r"Find the equilibrium solutions of $\dfrac{dy}{dt} = y^2 - 4$.",
                     [r"y^2 - 4 = 0", r"(y - 2)(y + 2) = 0", r"y = 2 \text{ and } y = -2"], at=[1, 2, 3])
        self.example("Example 2: A second derivative in x and y", r"$\dfrac{dy}{dx} = x - y$. Find $\dfrac{d^2y}{dx^2}$ in terms of $x$ and $y$, and the concavity of the solution through $(0, 1)$ there.",
                     [r"\frac{d^2y}{dx^2} = 1 - \frac{dy}{dx}", r"= 1 - (x - y) = 1 - x + y", r"(0, 1): \ 1 - 0 + 1 = 2 > 0: \ \text{concave up}"], at=[1, 2, 3])
        self.finish()
