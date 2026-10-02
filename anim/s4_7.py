"""Topic 4.7: L'Hospital's Rule. Narration comes from transcripts/4_7.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "4.7"

    def construct(self):
        ax, al = plot_axes([-1.5, 1.5, 0.5], [-1.5, 1.5, 0.5], w=6.4, h=5.6, coords=False)
        VGroup(ax, al).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        f = lambda s: np.sin(3 * s)
        X = ValueTracker(1.2)
        with self.beat("A race to zero") as b:
            cf = ax.plot(f, x_range=[-1.5, 1.5], color=FUNC, stroke_width=5)
            cg = ax.plot(lambda s: s, x_range=[-1.5, 1.5], color=SECANT, stroke_width=5)
            labs = VGroup(M(r"f(x) = \sin(3x)", 36, FUNC), M(r"g(x) = x", 36, SECANT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.8).shift(UP * 2.3)
            self.play(FadeIn(ax), FadeIn(al), Create(cf), Create(cg), FadeIn(labs), run_time=1.4)
            dots = always_redraw(lambda: VGroup(Dot(ax.c2p(X.get_value(), f(X.get_value())), color=FUNC), Dot(ax.c2p(X.get_value(), X.get_value()), color=SECANT)))
            read = always_redraw(lambda: VGroup(
                M(rf"x = {X.get_value():.3f}", 34, DIM),
                M(rf"f(x) = {f(X.get_value()):.3f}", 34, FUNC),
                M(rf"g(x) = {X.get_value():.3f}", 34, SECANT),
                M(rf"\frac{{f(x)}}{{g(x)}} = {f(X.get_value()) / X.get_value():.3f}", 38, TANGENT),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(labs, DOWN, buff=0.6).align_to(labs, LEFT))
            self.add(dots)
            self.play(FadeIn(read), run_time=0.5)
            b.line(1)
            self.play(X.animate.set_value(0.3), run_time=2.5)
            self.play(X.animate.set_value(0.002), run_time=2.5)
            b.line(2)
            self.play(Indicate(read[3], color=TANGENT), run_time=1)
        self.clear()
        self.title()

        W = ValueTracker(1.5)
        frame = Square(side_length=5.6, color=DIM, stroke_width=3).to_edge(LEFT, buff=0.9).shift(DOWN * 0.2)
        box = Axes(x_range=[-1, 1], y_range=[-1, 1], x_length=5.6, y_length=5.6, tips=False, axis_config={"stroke_opacity": 0}).move_to(frame)
        # in window units: u = x / W, v = y / (3W), so y = 3x is the diagonal and y = x is a third as steep
        cur_f = always_redraw(lambda: box.plot(lambda u: np.clip(np.sin(3 * W.get_value() * u) / (3 * W.get_value()), -1, 1), x_range=[-1, 1, 0.01], color=FUNC, stroke_width=5))
        cur_g = always_redraw(lambda: box.plot(lambda u: u / 3, x_range=[-1, 1], color=SECANT, stroke_width=5))
        with self.beat("Zoom in on zero over zero") as b:
            self.play(Create(frame), Create(cur_f), Create(cur_g), FadeIn(Dot(box.c2p(0, 0), color=INK)), run_time=1.2)
            b.line(1)
            self.play(W.animate.set_value(0.02), run_time=3)
            looks = VGroup(M(r"f(x) \approx 3x", 40, FUNC), M(r"g(x) \approx 1x", 40, SECANT)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=1.2).shift(UP * 1.6)
            self.play(FadeIn(looks), run_time=0.8)
            b.line(2)
            ratio = M(r"\frac{f(x)}{g(x)} \approx \frac{3x}{1x} = \frac{3}{1}", 48, TANGENT).next_to(looks, DOWN, buff=0.7)
            self.play(Write(ratio), run_time=1.2)
            slopes = M(r"= \frac{f'(0)}{g'(0)}", 48, TANGENT).next_to(ratio, DOWN, buff=0.4).align_to(ratio, LEFT).shift(RIGHT * 1.1)
            self.play(Write(slopes), run_time=0.8)
        self.clear()

        with self.beat("The rule") as b:
            rule = VGroup(M(r"\text{If } \lim_{x \to a} f(x) = 0 \text{ and } \lim_{x \to a} g(x) = 0,", 42),
                          T(r"or both limits are infinite, then", 36, DIM),
                          M(r"\lim_{x \to a} \frac{f(x)}{g(x)} = \lim_{x \to a} \frac{f'(x)}{g'(x)}", 54, TANGENT)).arrange(DOWN, buff=0.4).shift(UP * 0.5)
            frame2 = SurroundingRectangle(rule, color=TANGENT, buff=0.35)
            self.play(FadeIn(rule[0]), FadeIn(rule[1]), run_time=1)
            self.play(Write(rule[2]), Create(frame2), run_time=1.4)
            b.line(1)
            nq = T("not the quotient rule", 38, SECANT).next_to(frame2, DOWN, buff=0.5)
            self.play(FadeIn(nq), run_time=0.6)
        self.clear()

        with self.beat("Check the form first") as b:
            top = M(r"\lim_{x \to 1} \frac{x^2 + 1}{x + 1}", 60).to_edge(UP, buff=0.6)
            self.play(Write(top), run_time=1)
            b.line(1)
            ok = M(r"= \frac{2}{2} = 1", 54, DERIV).next_to(top, DOWN, buff=0.6).shift(LEFT * 3)
            bad = M(r"\lim_{x \to 1} \frac{2x}{1} = 2", 48, DIM).next_to(top, DOWN, buff=0.6).shift(RIGHT * 3.2)
            self.play(FadeIn(ok), run_time=0.8)
            self.play(FadeIn(bad), run_time=0.8)
            self.play(Create(Cross(bad, stroke_color=TANGENT, scale_factor=0.9)), run_time=0.6)
            b.line(2)
            ap = T(r"On the AP exam: show $\frac{0}{0}$ or $\frac{\infty}{\infty}$ first.", 40, SECANT).shift(DOWN * 1.9)
            self.play(FadeIn(ap), run_time=0.8)
        self.clear()

        with self.beat("Close") as b:
            steps = VGroup(T(r"1. Check the form: $\frac00$ or $\frac{\infty}{\infty}$?", 42), T("2. Differentiate the top and the bottom separately.", 42),
                           T("3. Take the new limit; repeat if it's still indeterminate.", 42)).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
            for m in steps:
                self.play(FadeIn(m, shift=RIGHT * 0.2), run_time=0.6)
        self.clear()

        self.examples_card()
        self.example("Example 1: A sine over x", r"Find $\displaystyle\lim_{x \to 0} \frac{\sin(3x)}{x}$.",
                     [r"\lim_{x \to 0} \sin(3x) = 0,\ \ \lim_{x \to 0} x = 0:\ \ \frac00", r"\lim_{x \to 0} \frac{3\cos(3x)}{1}", r"= 3"], at=[1, 2, 3])
        self.example("Example 2: A log against a line", r"Find $\displaystyle\lim_{x \to \infty} \frac{\ln x}{x}$.",
                     [r"\lim_{x \to \infty} \ln x = \infty,\ \ \lim_{x \to \infty} x = \infty:\ \ \frac{\infty}{\infty}", r"\lim_{x \to \infty} \frac{1/x}{1}", r"= 0"], at=[1, 2, 3])
        self.example("Example 3: Twice", r"Find $\displaystyle\lim_{x \to 0} \frac{e^x - 1 - x}{x^2}$.",
                     [r"\text{top} \to 1 - 1 - 0 = 0,\ \ \text{bottom} \to 0:\ \ \frac00", r"\lim_{x \to 0} \frac{e^x - 1}{2x}",
                      r"\text{still } \frac00", r"\lim_{x \to 0} \frac{e^x}{2} = \frac12"], at=[1, 2, 3, 4])
        self.finish()
