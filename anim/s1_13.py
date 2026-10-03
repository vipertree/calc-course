"""Topic 1.13: Removing discontinuities. Narration comes from transcripts/1_13.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "1.13"

    def construct(self):
        ax, al = plot_axes([0, 7, 1], [0, 12, 2], w=7.4, h=5.2)
        VGroup(ax, al).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        hole = open_dot(ax, 4, 8)
        with self.beat("Patching a hole") as b:
            e = M(r"f(x) = \frac{x^2 - 16}{x - 4}", 48, FUNC).to_edge(RIGHT, buff=0.6).shift(UP * 2)
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(lambda x: x + 4, x_range=[0, 7], color=FUNC, stroke_width=5)), FadeIn(hole), Write(e), run_time=1.8)
            lim = M(r"\lim_{x\to4} f(x) = 8", 44, SECANT).next_to(e, DOWN, buff=0.5)
            self.play(Write(lim), run_time=1)
            b.line(1)
            drop = Dot(ax.c2p(4, 11.5), color=SECANT, radius=0.1)
            self.play(FadeIn(drop), run_time=0.3)
            self.play(drop.animate.move_to(ax.c2p(4, 8)), run_time=1, rate_func=rate_functions.ease_in_quad)
            self.play(FadeOut(hole), Flash(drop, color=SECANT), run_time=0.6)
        self.clear()
        self.title()

        with self.beat("Which breaks can be removed") as b:
            minis = VGroup()
            for kind in ("hole", "jump", "asym"):
                a, _ = plot_axes([0, 2, 1], [0, 3, 1], w=3.4, h=2.6, coords=False)
                if kind == "hole":
                    g = VGroup(a.plot(lambda x: 1 + 0.5 * x, x_range=[0, 2], color=FUNC), open_dot(a, 1, 1.5))
                elif kind == "jump":
                    g = VGroup(a.plot(lambda x: 0.8, x_range=[0, 1], color=FUNC), a.plot(lambda x: 2.2, x_range=[1, 2], color=FUNC))
                else:
                    g = VGroup(a.plot(lambda x: 1.5 + 0.2 / (1 - x), x_range=[0, 0.93], color=FUNC), a.plot(lambda x: 1.5 + 0.2 / (1 - x), x_range=[1.07, 2], color=FUNC),
                               asymptote(a, 1, [0, 3]))
                minis.add(VGroup(a, g))
            minis.arrange(RIGHT, buff=0.8)
            self.play(FadeIn(minis), run_time=1)
            fix = Dot(minis[0][0].c2p(1, 1.5), color=SECANT, radius=0.09)
            self.play(FadeIn(fix, scale=2), FadeIn(Text("✓", color=DERIV, font_size=40).next_to(minis[0], DOWN)), run_time=0.8)
            b.line(1)
            self.play(FadeIn(Text("✗", color=TANGENT, font_size=40).next_to(minis[1], DOWN)), FadeIn(Text("✗", color=TANGENT, font_size=40).next_to(minis[2], DOWN)), run_time=0.8)
        self.clear()

        with self.beat("Writing the repaired function") as b:
            rep = M(r"f(x) = \begin{cases} \dfrac{x^2 - 16}{x - 4}, & x \ne 4 \\ 8, & x = 4 \end{cases}", 60)
            self.play(Write(rep), run_time=1.8)
            self.play(Indicate(rep[0][-6:], color=SECANT), run_time=1)
        self.clear()

        a2, al2 = plot_axes([-1, 4, 1], [-2, 10, 2], w=7.2, h=5.2)
        VGroup(a2, al2).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        k = ValueTracker(3)
        left = always_redraw(lambda: a2.plot(lambda x: k.get_value() * x + 1, x_range=[-1, 2], color=SECANT, stroke_width=5))
        with self.beat("Choosing a parameter") as b:
            pw = M(r"f(x) = \begin{cases} kx + 1, & x < 2 \\ x^2 - 1, & x \ge 2 \end{cases}", 44).to_edge(RIGHT, buff=0.5).shift(UP * 1.8)
            self.play(FadeIn(a2), FadeIn(al2), Write(pw), run_time=1.2)
            self.play(Create(a2.plot(lambda x: x * x - 1, x_range=[2, 3.3], color=TANGENT, stroke_width=5)), FadeIn(closed_dot(a2, 2, 3, TANGENT)), run_time=1)
            self.add(left)
            b.line(1)
            self.play(k.animate.set_value(-0.5), run_time=1.4)
            self.play(k.animate.set_value(2.2), run_time=1.2)
            b.line(2)
            eq = M(r"2k + 1 = 3,\ \text{so}\ k = 1", 46, SECANT).next_to(pw, DOWN, buff=0.6)
            self.play(k.animate.set_value(1), Write(eq), run_time=1.4)
        self.clear()

        self.example("Two unknowns, two seams", r"Find $a$ and $b$: \[ f(x) = \begin{cases} x + a, & x < -1 \\ bx^2 + 1, & -1 \le x \le 2 \\ 3x - 1, & x > 2 \end{cases} \]",
                     [r"x = -1:\ \ -1 + a = b + 1", r"x = 2:\ \ 4b + 1 = 5,\ \text{so}\ b = 1", r"a = 3"], at=[0, 1, 1])
        self.example("Two seams", r"Find $a$ and $b$ so that $f(x) = \begin{cases} x + a, & x < -1 \\ bx^2 + 1, & -1 \le x \le 2 \\ 3x - 1, & x > 2 \end{cases}$ is continuous everywhere.",
                     [r"x = 2: \ 4b + 1 = 3(2) - 1 = 5,\ \text{so}\ b = 1", r"x = -1: \ -1 + a = b(-1)^2 + 1 = 2", r"a = 3"], at=[1, 2, 3])

        with self.beat("Close") as b:
            card = VGroup(T("fill a hole with the limit", 46, SECANT), T("match the pieces at every seam", 46, TANGENT)).arrange(DOWN, buff=0.6)
            self.play(FadeIn(card[0]), run_time=0.8)
            self.play(FadeIn(card[1]), run_time=0.8)
        self.clear()

        self.examples_card()
        self.example("Example 1: Fill the hole", r"$f(x) = \dfrac{x^2 - 5x + 6}{x - 3}$. What value of $f(3)$ makes $f$ continuous?",
                     [r"f(3) \text{ should equal } \lim_{x\to3} f(x)", r"\lim_{x\to3}\frac{(x - 2)(x - 3)}{x - 3} = \lim_{x\to3}(x - 2) = 1", r"f(3) = 1"], at=[1, 2, 3])
        self.example("Example 2: A hole hiding behind a root", r"$g(x) = \dfrac{\sqrt{x + 1} - 2}{x - 3}$. What value of $g(3)$ removes the discontinuity?",
                     [r"\frac00:\ \text{use the conjugate}", r"\lim_{x\to3}\frac{(x + 1) - 4}{(x - 3)(\sqrt{x + 1} + 2)}", r"= \lim_{x\to3}\frac{1}{\sqrt{x + 1} + 2} = \frac14",
                      r"g(3) = \frac14"], at=[1, 2, 3, 3])
        self.example("Example 3: Two seams, two unknowns", r"Find $a$ and $b$ so that $f$ is continuous everywhere. \[ f(x) = \begin{cases} ax + 2, & x < 1 \\ x^2 + b, & 1 \le x \le 3 \\ 4x - 1, & x > 3 \end{cases} \]",
                     [r"x = 3:\ \ f(3) = 9 + b, \quad \lim_{x\to3^+}(4x - 1) = 11,\ \text{so}\ b = 2",
                      r"x = 1:\ \ \lim_{x\to1^-}(ax + 2) = a + 2, \quad f(1) = 1 + b = 3", r"a + 2 = 3,\ \text{so}\ a = 1"], at=[1, 2, 3])
        self.finish()
