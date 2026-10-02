"""Topic 1.10: Exploring types of discontinuities. Narration comes from transcripts/1_10.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def pA(x):
    return 0.3 * x + 3


def pB(x):
    return 1 + 1 / (3 - x)


def broken_graph():
    ax, al = plot_axes([-5, 6, 1], [-4, 6, 1], w=11, h=5.6, coords=False)
    ax.shift(DOWN * 0.3)
    pieces = [ax.plot(pA, x_range=[-5, -3], color=FUNC, stroke_width=5), ax.plot(pA, x_range=[-3, 0], color=FUNC, stroke_width=5),
              ax.plot(pB, x_range=[0, 2.75], color=FUNC, stroke_width=5), ax.plot(pB, x_range=[3.2, 6], color=FUNC, stroke_width=5)]
    marks = VGroup(open_dot(ax, -3, pA(-3)), closed_dot(ax, -3, 4.6, FUNC), open_dot(ax, 0, 3), closed_dot(ax, 0, pB(0), FUNC),
                   asymptote(ax, 3, [-4, 6]))
    return ax, pieces, marks


class Lesson(TranscriptScene):
    NUM = "1.10"

    def construct(self):
        ax0, _ = plot_axes([-3, 3, 1], [-2, 4, 1], w=9, h=4.6, coords=False)
        smooth = ax0.plot(lambda x: 1 + 0.6 * np.sin(1.2 * x) + 0.1 * x * x, x_range=[-3, 3], color=FUNC, stroke_width=5)
        with self.beat("The pencil test") as b:
            pen = Dot(color=SECANT, radius=0.12)
            # the graph is all there first; then the pencil traces it without lifting
            self.play(FadeIn(ax0), Create(smooth), run_time=1.2)
            pen.move_to(smooth.get_start())
            self.play(FadeIn(pen), run_time=0.3)
            self.play(MoveAlongPath(pen, smooth), run_time=2.2)
            b.line(1)
            self.play(FadeOut(ax0), FadeOut(smooth), FadeOut(pen), run_time=0.5)
            ax, pieces, marks = broken_graph()
            self.play(FadeIn(ax), FadeIn(marks[4]), *[Create(pc) for pc in pieces], FadeIn(marks[:4]), run_time=1.2)
            for i, pc in enumerate(pieces):
                pen.move_to(pc.get_start())
                self.play(FadeIn(pen), run_time=0.2)
                self.play(MoveAlongPath(pen, pc), run_time=0.9)
                if i < 3:
                    self.play(Flash(pen.get_center(), color=TANGENT), FadeOut(pen), run_time=0.4)
        self.clear()
        self.title()

        ax, pieces, marks = broken_graph()
        self.add(ax, *pieces, marks)
        with self.beat("Removable: a hole") as b:
            self.play(self.camera.frame.animate.scale(0.45).move_to(ax.c2p(-3, 3.2)), run_time=1.6)
            b.line(1)
            self.play(Indicate(marks[1], color=SECANT, scale_factor=2), run_time=1)
            b.line(2)
            self.play(FadeIn(T("removable", 30, SECANT).next_to(ax.c2p(-3, 1.6), DOWN)), run_time=0.8)
        with self.beat("Jump") as b:
            self.play(self.camera.frame.animate.move_to(ax.c2p(0, 2.1)), run_time=1.4)
            gap = Line(ax.c2p(0, pB(0)), ax.c2p(0, 3), color=TANGENT, stroke_width=6)
            self.play(Create(gap), FadeIn(T("jump", 30, TANGENT).next_to(gap, RIGHT, buff=0.2)), run_time=0.9)
        with self.beat("Vertical asymptote") as b:
            self.play(self.camera.frame.animate.move_to(ax.c2p(3, 1)), run_time=1.4)
            self.play(FadeIn(T("vertical asymptote", 30, DERIV).next_to(ax.c2p(3.2, 4.5), LEFT)), run_time=0.8)
        self.play(self.camera.frame.animate.scale(1 / 0.45).move_to(ORIGIN + DOWN * (config.frame_height * 0.22 / 2 - 0.45)), run_time=1.2)
        self.clear()

        with self.beat("Reading the formula") as b:
            bd = Board()
            bd.anchor = UP * 3
            bd.write(self, r"\frac{x^2 - x - 2}{x^2 - 4} = \frac{(x - 2)(x + 1)}{(x - 2)(x + 2)}")
            b.line(1)
            bd.write(self, r"x - 2 \text{ cancels: hole at } x = 2,\ \text{height } \frac{2 + 1}{2 + 2} = \frac34", SECANT)
            b.line(2)
            bd.write(self, r"x + 2 \text{ stays: vertical asymptote } x = -2", TANGENT)
        self.clear()

        a2, al2 = plot_axes([-1, 3, 1], [-1, 5, 1], w=7, h=5)
        VGroup(a2, al2).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        with self.beat("Piecewise functions") as b:
            pw = M(r"f(x) = \begin{cases} x + 1, & x < 1 \\ x^2, & x \ge 1 \end{cases}", 44).to_edge(RIGHT, buff=0.6).shift(UP * 1.6)
            self.play(FadeIn(a2), FadeIn(al2), Write(pw), run_time=1.2)
            self.play(Create(a2.plot(lambda x: x + 1, x_range=[-1, 1], color=SECANT, stroke_width=5)), FadeIn(open_dot(a2, 1, 2, SECANT)),
                      Create(a2.plot(lambda x: x * x, x_range=[1, 2.2], color=TANGENT, stroke_width=5)), FadeIn(closed_dot(a2, 1, 1, TANGENT)), run_time=1.6)
            b.line(1)
            r = VGroup(M(r"\text{left} \to 2", 40, SECANT), M(r"\text{right} \to 1", 40, TANGENT), T("a jump at $x = 1$", 40)).arrange(DOWN, aligned_edge=LEFT).next_to(pw, DOWN, buff=0.5)
            self.play(FadeIn(r), run_time=1)
        self.clear()
        self.example("Where the pieces meet", r"Let $f(x) = \begin{cases} x + 1, & x < 1 \\ x^2, & x \ge 1 \end{cases}$. Is $f$ continuous at $x = 1$? If not, classify the discontinuity.",
                     [r"\lim_{x\to1^-}(x + 1) = 2", r"\lim_{x\to1^+}x^2 = 1", r"\text{the one-sided limits differ: a jump discontinuity}"], at=[1, 2, 3])

        with self.beat("Close") as b:
            names = ["removable", "jump", "vertical asymptote"]
            subs = ["a hole: limit exists", "one-sided limits disagree", "unbounded"]
            cols = [SECANT, TANGENT, DERIV]
            cards = VGroup(*[VGroup(T(n_, 44, c_), T(s_, 30, DIM)).arrange(DOWN, buff=0.25) for n_, s_, c_ in zip(names, subs, cols)]).arrange(RIGHT, buff=1.2)
            self.play(LaggedStart(*[FadeIn(cd) for cd in cards], lag_ratio=0.4), run_time=2)
            b.line(1)
            # two families: removable (a hole) and nonremovable (a jump or a vertical asymptote)
            br = Brace(cards[1:], UP, color=TANGENT)
            self.play(GrowFromCenter(br), FadeIn(T("nonremovable", 36, TANGENT).next_to(br, UP, buff=0.15)), run_time=1)
        self.clear()

        self.examples_card()
        self.example("Example 1: Classify from a formula", r"Find and classify the discontinuities of $f(x) = \dfrac{x^2 + 2x - 15}{x^2 - 9}$.",
                     [r"x^2 - 9 = 0 \text{ at } x = \pm3", r"\frac{(x + 5)(x - 3)}{(x - 3)(x + 3)}", r"x = 3:\ \text{removable, hole at height } \frac86 = \frac43",
                      r"x = -3:\ \text{vertical asymptote (nonremovable)}"], at=[1, 2, 3, 4])
        a3, _ = plot_axes([0, 4, 1], [0, 8, 2], w=4.6, h=4)
        fig3 = VGroup(a3, a3.plot(lambda x: 2 * x - 1, x_range=[0, 2], color=FUNC), a3.plot(lambda x: x * x - 1, x_range=[2, 3], color=FUNC),
                      open_dot(a3, 2, 3), closed_dot(a3, 2, 5, SECANT))
        self.example("Example 2: A piecewise function with a misplaced point", r"Find and classify the discontinuity at $x = 2$: \[ f(x) = \begin{cases} 2x - 1, & x < 2 \\ 5, & x = 2 \\ x^2 - 1, & x > 2 \end{cases} \]",
                     [r"\lim_{x\to2^-} f(x) = \lim_{x\to2^-}(2x - 1) = 3, \qquad \lim_{x\to2^+} f(x) = \lim_{x\to2^+}(x^2 - 1) = 3",
                      r"\lim_{x\to2} f(x) = 3, \quad f(2) = 5 \ne 3", r"\text{removable discontinuity}"], figure=fig3, at=[1, 2, 2])
        self.example("Example 3: A jump from an absolute value", r"Classify the discontinuity of $f(x) = \dfrac{|x + 1|}{x + 1}$ at $x = -1$.",
                     [r"x < -1:\ \frac{-(x + 1)}{x + 1} = -1", r"x > -1:\ \frac{x + 1}{x + 1} = 1", r"-1 \ne 1:\ \text{jump}"], at=[1, 2, 3])
        self.finish()
