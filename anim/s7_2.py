"""Topic 7.2: Verifying solutions for differential equations. Narration comes from transcripts/7_2.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "7.2"

    def construct(self):
        with self.beat("A different kind of solution") as b:
            sep = Line(UP * 3.2, DOWN * 3.2, color=DIM, stroke_width=2)
            lh = T("algebra", 38, DIM).move_to([-3.6, 2.9, 0])
            le = M(r"2x + 1 = 7", 52).next_to(lh, DOWN, buff=0.5)
            ls = M(r"\text{solution: } x = 3", 44, SECANT).next_to(le, DOWN, buff=0.5)
            lv = T("a value", 32, SECANT).next_to(ls, DOWN, buff=0.25)
            nl = NumberLine(x_range=[0, 6, 1], length=4.6, color=DIM, include_numbers=True, font_size=26).next_to(lv, DOWN, buff=0.6)
            dot = Dot(nl.n2p(3), color=SECANT, radius=0.11)
            self.play(FadeIn(sep), FadeIn(lh), Write(le), run_time=1)
            self.play(FadeIn(ls), FadeIn(lv), FadeIn(nl), FadeIn(dot, scale=1.6), run_time=1)
            b.line(1)
            rh = T("differential equation", 38, DIM).move_to([3.6, 2.9, 0])
            re_ = M(r"\frac{dy}{dx} = 3y", 52, ACCUM).next_to(rh, DOWN, buff=0.4)
            rs = M(r"\text{solution: a function } y = \dots", 40, FUNC).next_to(re_, DOWN, buff=0.4)
            rc = T("a curve", 32, FUNC).next_to(rs, DOWN, buff=0.2)
            ax, _ = plot_axes([-1.5, 1, 1], [-4, 4, 2], w=3.6, h=2.4, coords=False)
            ax.next_to(rc, DOWN, buff=0.3)
            curves = VGroup(*[ax.plot(lambda s, c=c: c * np.exp(3 * s), x_range=[-1.5, 0.6 if abs(c) > 1 else 0.85], color=FUNC, stroke_width=3) for c in (-2, -1, -0.5, 0.5, 1, 2)])
            self.play(FadeIn(rh), Write(re_), run_time=1)
            self.play(FadeIn(rs), FadeIn(rc), FadeIn(ax), Create(curves[3]), run_time=1)
            many = T("often many", 30, FUNC).next_to(ax, RIGHT, buff=0.2)
            self.play(LaggedStart(*[Create(c) for k, c in enumerate(curves) if k != 3], lag_ratio=0.2), FadeIn(many), run_time=1.4)
            b.line(2)
            self.play(Indicate(re_, color=ACCUM), run_time=1)
        self.clear()
        self.title()

        with self.beat("Does it fit?") as b:
            de = M(r"\frac{dy}{dx} = 3y", 56, ACCUM).to_edge(UP, buff=0.5)
            want = T("we want: $y$ in terms of $x$ whose derivative is $3y$", 30, DIM).next_to(de, DOWN, buff=0.3)
            self.play(Write(de), FadeIn(want), run_time=1)
            ask = T("given a $y$, does the statement hold?", 34, SECANT).next_to(want, DOWN, buff=0.35)
            self.play(FadeIn(ask), run_time=0.7)
            b.line(1)
            cand = M(r"y = 5e^{3x} \ ?", 48).next_to(ask, DOWN, buff=0.45)
            self.play(FadeIn(cand), run_time=0.7)
            lhs = VGroup(T("left side", 28, DIM), M(r"\frac{dy}{dx} = 15e^{3x}", 44)).arrange(DOWN, buff=0.2)
            rhs = VGroup(T("right side", 28, DIM), M(r"3y = 3\left(5e^{3x}\right) = 15e^{3x}", 44)).arrange(DOWN, buff=0.2)
            VGroup(lhs, rhs).arrange(RIGHT, buff=1.2).next_to(cand, DOWN, buff=0.5)
            self.play(FadeIn(lhs), run_time=0.8)
            b.line(2)
            self.play(FadeIn(rhs), run_time=0.8)
            tick = M(r"\checkmark", 64, DERIV).next_to(VGroup(lhs, rhs), DOWN, buff=0.3)
            self.play(FadeIn(tick, scale=1.5), run_time=0.6)
        self.clear()

        with self.beat("The test") as b:
            steps = VGroup(T("1. Differentiate the candidate as many times as the equation needs.", 32), T("2. Substitute $y$, $y'$ (and $y''$) into both sides.", 32),
                           T("3. Simplify: a solution makes the sides equal for every $x$.", 32)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(UP, buff=0.6)
            self.play(FadeIn(steps[0]), run_time=0.6)
            b.line(1)
            self.play(FadeIn(steps[1]), run_time=0.6)
            b.line(2)
            self.play(FadeIn(steps[2]), run_time=0.6)
            b.line(3)
            ax, _ = plot_axes([-1.5, 1, 1], [-4, 4, 2], w=4.2, h=3, coords=False)
            fam = VGroup(ax, *[ax.plot(lambda s, c=c: c * np.exp(3 * s), x_range=[-1.5, 0.6 if abs(c) > 1 else 0.85], color=FUNC, stroke_width=3) for c in (-2, -1, -0.5, 0.5, 1, 2)])
            fam.next_to(steps, DOWN, buff=0.5).shift(LEFT * 2.5)
            lab = M(r"y = Ce^{3x}: \ y' = 3Ce^{3x} = 3y", 40, ACCUM).next_to(fam, RIGHT, buff=0.6)
            self.play(FadeIn(fam), Write(lab), run_time=1.2)
        self.clear()

        self.example("One that fails", r"Is $y = e^{2x}$ a solution of $y'' - y = 0$?",
                     [r"y' = 2e^{2x}, \ \ y'' = 4e^{2x}", r"y'' - y = 4e^{2x} - e^{2x} = 3e^{2x}", r"3e^{2x} \ne 0: \ \text{not a solution}"], at=[1, 2, 3], follow=True)

        with self.beat("Close") as b:
            card = VGroup(T("Differentiate, substitute, simplify.", 40, ACCUM), T("Equal for every $x$: a solution.", 38), T("Solutions usually come in families.", 36, DIM)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=1.6)
        self.clear()

        self.examples_card()
        self.example("Example 1: A first-order equation", r"Show that $y = x^2 + 2x$ is a solution of $xy' - y = x^2$.",
                     [r"y' = 2x + 2", r"xy' - y = x(2x + 2) - \left(x^2 + 2x\right)", r"= 2x^2 + 2x - x^2 - 2x = x^2", r"\text{matches the right side: a solution}"], at=[1, 2, 3, 4])
        self.example("Example 2: A second-order equation", r"Show that $y = \sin 2x$ is a solution of $y'' + 4y = 0$.",
                     [r"y' = 2\cos 2x, \ \ y'' = -4\sin 2x", r"y'' + 4y = -4\sin 2x + 4\sin 2x = 0", r"\text{matches: a solution}"], at=[1, 2, 3])
        self.example("Example 3: Finding the constant", r"$y = \dfrac{1}{x + C}$ solves $\dfrac{dy}{dx} = -y^2$. Find $C$ so that $y(0) = \frac12$.",
                     [r"y' = -\frac{1}{(x + C)^2} = -y^2 \ \checkmark", r"y(0) = \frac1C = \frac12", r"C = 2: \ \ y = \frac{1}{x + 2}"], at=[1, 2, 3])
        self.finish()
