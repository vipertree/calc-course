"""Topic 5.10: Introduction to optimization. Narration comes from transcripts/5_10.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "5.10"

    def pen(self, X, origin, k=0.035):
        """The riverside pen for depth X (feet), drawn at scale k units per foot, hanging below `origin` (the river's bank):
        a grassy patch, a wooden fence on three sides, and a sheep that grazes in the middle."""
        def draw():
            x = X.get_value()
            y = 200 - 2 * x
            w, h = y * k, x * k
            tl = origin + LEFT * w / 2
            grass = Rectangle(width=w, height=max(h, 0.001), stroke_width=0, fill_color=GRASS, fill_opacity=0.9).move_to(tl + RIGHT * w / 2 + DOWN * h / 2)
            fence = fence_path([tl, tl + DOWN * h, tl + DOWN * h + RIGHT * w, tl + RIGHT * w])
            out = VGroup(grass, fence)
            room = min(w, h)
            if room > 0.45:
                out.add(sheep(min(0.6, room * 0.55)).move_to(grass.get_center()))
            return out
        return always_redraw(draw)

    def construct(self):
        river = river_band(7.4, 0.7).to_edge(UP, buff=0.3).shift(LEFT * 3.1)
        river.add(T("river", 26, WATER_HI).move_to(river[0]).shift(RIGHT * 2.9))
        meadow = Rectangle(width=7.4, height=5.6, stroke_width=0, fill_color=MEADOW, fill_opacity=0.35).next_to(river, DOWN, buff=0)
        X = ValueTracker(10)
        pen = self.pen(X, river[0].get_bottom())
        ax, al = plot_axes([0, 100, 25], [0, 6000, 2000], w=5, h=4, coords=False, xlabel="x", ylabel="A")
        VGroup(ax, al).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.6)
        A = lambda x: x * (200 - 2 * x)
        with self.beat("A fixed amount of fence") as b:
            self.play(FadeIn(meadow), FadeIn(river), run_time=0.6)
            self.add(pen)
            read = always_redraw(lambda: M(rf"A = {A(X.get_value()):,.0f}\ \text{{ft}}^2", 36, FUNC).next_to(river, DOWN, buff=4.4))
            self.play(FadeIn(read), FadeIn(ax), FadeIn(al), run_time=0.8)
            trace = always_redraw(lambda: ax.plot(A, x_range=[10, max(X.get_value(), 10.5)], color=FUNC, stroke_width=4))
            dot = always_redraw(lambda: Dot(ax.c2p(X.get_value(), A(X.get_value())), color=SECANT))
            self.add(trace, dot)
            self.play(X.animate.set_value(90), run_time=3, rate_func=linear)
            b.line(1)
            self.play(X.animate.set_value(50), run_time=2)
            b.line(2)
            self.play(Indicate(dot, color=TANGENT, scale_factor=1.8), run_time=1)
        self.clear()
        self.title()

        with self.beat("What optimization means") as b:
            l1 = VGroup(T(r"optimize:", 44, SECANT), T("make it the best", 44)).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.7)
            self.play(FadeIn(l1), run_time=0.8)
            b.line(1)
            l2 = T("in math, best means a maximum or a minimum", 40).next_to(l1, DOWN, buff=0.6)
            chips = VGroup(*[formula_box(T(t, 32, c), c) for t, c in (("most area", DERIV), ("least cost", TANGENT), ("shortest time", TANGENT))]).arrange(RIGHT, buff=0.5)
            chips.next_to(l2, DOWN, buff=0.4)
            b.line(2)
            self.play(FadeIn(l2), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.3), run_time=1.2)
            b.line(3)
            l3 = T(r"max or min? \ the derivative", 40, DERIV).next_to(chips, DOWN, buff=0.6)
            self.play(FadeIn(l3), run_time=0.8)
            b.line(4)
            l4 = T(r"situation $\to$ function: the hard part", 40, SECANT).next_to(l3, DOWN, buff=0.5)
            self.play(FadeIn(l4), run_time=0.8)
            b.line(5)
            l5 = formula_box(T("differentiable function: we can optimize it", 38, FUNC), FUNC).next_to(l4, DOWN, buff=0.5)
            self.play(FadeIn(l5), run_time=0.8)
        self.clear()

        with self.beat("One quantity, one variable") as b:
            lines = VGroup(M(r"\text{Area: } A = xy", 46), M(r"\text{Constraint: } 2x + y = 200", 46, SECANT), M(r"A(x) = x(200 - 2x)", 50, FUNC),
                           M(r"\text{domain: } 0 < x < 100", 46, DIM)).arrange(DOWN, buff=0.55)
            for k, m in enumerate(lines):
                if k:
                    b.line(k)
                self.play(Write(m), run_time=1)
        self.clear()
        W = ValueTracker(8)
        holder = Rectangle(width=4.2, height=3.9, stroke_opacity=0)     # the picture's spot; the live rectangle is drawn inside it
        k = 0.17

        def live_rect():
            w, l = W.get_value(), 20 - W.get_value()
            r = Rectangle(width=max(k * w, 0.02), height=max(k * l, 0.02), color=FUNC, stroke_width=5, fill_color=FUNC, fill_opacity=0.2).move_to(holder)
            return VGroup(r, M("w", 34, SECANT).next_to(r, DOWN, buff=0.15), M(r"\ell", 34, SECANT).next_to(r, RIGHT, buff=0.15))
        rect = always_redraw(live_rect)
        no = VGroup(M(r"\ell = -5?", 34, TANGENT), T("No such rectangle.", 30, TANGENT)).arrange(DOWN, buff=0.15)

        def show_no(sc):
            no.move_to(holder.get_top() + DOWN * 0.45)     # above the rectangle, below the problem
            sc.play(FadeIn(no), Wiggle(no), run_time=1)

        def flatten(sc):
            sc.play(FadeOut(no), run_time=0.3)
            sc.play(W.animate.set_value(19.4), run_time=1.6)
            sc.play(W.animate.set_value(0.6), run_time=2)
            sc.play(W.animate.set_value(8), run_time=1)
        self.example("Setting up", r"A rectangle has perimeter $40$. Write its area as a function of its width $w$, and give the domain.",
                     [r"2w + 2\ell = 40", r"2\ell = 40 - 2w, \ \ \ell = 20 - w", r"A(w) = w(20 - w)", r"w = 25: \ \ell = 20 - 25 = -5 \ \text{(no rectangle)}",
                      r"TEXT:As $w \to 20$ or $w \to 0$, the rectangle flattens to a line.", r"\text{domain: } 0 < w < 20"],
                     at=[1, 2, 3, 4, 5, 6], figure=holder,
                     cues={0: lambda sc: sc.add(rect), 3: show_no, 4: flatten}, follow=True)

        with self.beat("Then it's a Unit 5 problem") as b:
            lines = VGroup(M(r"A'(x) = 200 - 4x", 44), M(r"200 - 4x = 0, \ \ 4x = 200, \ \ x = 50", 44), M(r"A''(x) = -4 < 0:\ \text{maximum}", 44, DERIV),
                           M(r"y = 200 - 2(50) = 100", 44), M(r"A(50) = 50 \cdot 100 = 5000\ \text{ft}^2", 48, FUNC)).arrange(DOWN, buff=0.45)
            b.line(1)
            for k2, m in zip((1, 2, 3, 4, 4), lines):
                b.line(k2)
                self.play(Write(m), run_time=1)
        self.clear()

        with self.beat("Close") as b:
            steps = VGroup(T("1. Name the quantity.", 40), T("2. Write it with the variables.", 40), T("3. Use the constraint to get one variable.", 40),
                           T("4. Find the domain.", 40), T("Then find the absolute max or min.", 40, SECANT)).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in steps], lag_ratio=0.3), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Largest product", r"Two numbers add to $20$. What is the largest possible product?",
                     [r"P = xy,\ \ x + y = 20,\ \ y = 20 - x", r"P(x) = x(20 - x) = 20x - x^2", r"P'(x) = 20 - 2x", r"20 - 2x = 0, \ \ x = 10",
                      r"P''(x) = -2 < 0: \ \text{maximum}", r"y = 20 - 10 = 10, \ \ P = 10 \cdot 10 = 100"], at=[1, 2, 3, 3, 4, 5])
        self.example("Example 2: The riverside pen", r"A rectangular pen along a river uses $200$ ft of fence on three sides. What dimensions give the largest area?",
                     [r"A(x) = x(200 - 2x) = 200x - 2x^2,\ \ 0 < x < 100", r"A'(x) = 200 - 4x", r"200 - 4x = 0, \ \ x = 50",
                      r"A'' = -4 < 0,\ \text{only critical point: absolute max}", r"y = 200 - 100 = 100",
                      r"50 \text{ ft by } 100 \text{ ft},\ \ A = 5000\ \text{ft}^2"], at=[1, 2, 2, 3, 4, 4])
        self.example("Example 3: A number and its reciprocal", r"Find the positive number $x$ for which $x + \dfrac{9}{x}$ is as small as possible.",
                     [r"f'(x) = 1 - \frac{9}{x^2}", r"1 - \frac{9}{x^2} = 0, \ \ \frac{9}{x^2} = 1, \ \ x^2 = 9, \ \ x = \pm 3", r"\text{only } x = 3 \text{ is positive}",
                      r"f''(x) = \frac{18}{x^3}, \ \ f''(3) = \frac{18}{27} > 0", r"\text{only critical point on } (0, \infty):\ \text{absolute min}",
                      r"f(3) = 3 + 3 = 6"], at=[1, 2, 2, 3, 4, 4])
        self.finish()
