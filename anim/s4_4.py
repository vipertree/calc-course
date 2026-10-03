"""Topic 4.4: Introduction to related rates. Narration comes from transcripts/4_4.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "4.4"

    def construct(self):
        R = ValueTracker(0.05)
        center = LEFT * 3
        ring = always_redraw(lambda: Circle(radius=R.get_value(), color=FUNC, stroke_width=4, fill_color=FUNC, fill_opacity=0.15).move_to(center))
        read = always_redraw(lambda: VGroup(M(rf"r = {R.get_value() * 4:.1f}\text{{ cm}}", 40, SECANT),
                                            M(rf"A = {np.pi * (R.get_value() * 4) ** 2:.0f}\text{{ cm}}^2", 40, FUNC)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=1.2))
        with self.beat("A ripple") as b:
            stone = Dot(center + UP * 3, color=INK, radius=0.12)
            self.play(stone.animate.move_to(center), run_time=0.8, rate_func=rate_functions.ease_in_quad)
            self.remove(stone)
            self.add(ring, read)
            self.play(R.animate.set_value(1.25), run_time=3, rate_func=linear)
            b.line(1)
            self.play(R.animate.set_value(2.5), run_time=3, rate_func=linear)
            b.line(2)
            self.play(Indicate(read, color=SECANT), run_time=1)
        self.clear()
        self.title()

        with self.beat("Everything depends on time") as b:
            eq = M(r"A", r"=", r"\pi", r"r", r"^2", 80).shift(UP * 0.6)
            self.play(Write(eq), run_time=1)
            tags = VGroup(M(r"A(t)", 34, FUNC).next_to(eq[0], DOWN, buff=0.5), M(r"r(t)", 34, SECANT).next_to(eq[3], DOWN, buff=0.5))
            self.play(FadeIn(tags), run_time=0.8)
            b.line(1)
            dd = M(r"\frac{d}{dt}", 60, DIM).next_to(eq, LEFT, buff=0.4)
            self.play(FadeIn(dd), run_time=0.6)
        self.clear()

        with self.beat("The chain rule on every variable") as b:
            l1 = M(r"\frac{d}{dt}\big[A\big] = \frac{d}{dt}\big[\pi r^2\big]", 60).shift(UP * 1.2)
            self.play(Write(l1), run_time=1.2)
            b.line(1)
            l2 = M(r"\frac{dA}{dt} = 2\pi r\cdot", r"\frac{dr}{dt}", 64).next_to(l1, DOWN, buff=0.8)
            self.play(Write(l2), run_time=1.2)
            b.line(2)
            self.play(l2[1].animate.set_color(SECANT), Circumscribe(l2[1], color=SECANT), run_time=1.2)
        self.clear()

        with self.beat("Differentiate first, then substitute") as b:
            top = M(r"A = \pi r^2", 56).to_edge(UP, buff=0.5)
            self.play(Write(top), run_time=0.8)
            wrong = VGroup(M(r"r = 10:\ A = 100\pi", 42), M(r"\frac{dA}{dt} = 0", 42, TANGENT)).arrange(DOWN, buff=0.4).shift(LEFT * 3.4 + DOWN * 0.4)
            self.play(FadeIn(wrong), run_time=1)
            self.play(Create(Cross(wrong, stroke_color=TANGENT, scale_factor=0.8)), run_time=0.6)
            b.line(1)
            right = VGroup(M(r"\frac{dA}{dt} = 2\pi r\,\frac{dr}{dt}", 42), M(r"r = 10,\ \frac{dr}{dt} = 2", 42, DIM)).arrange(DOWN, buff=0.4).shift(RIGHT * 3.2 + DOWN * 0.4)
            self.play(FadeIn(right), run_time=1)
            b.line(2)
            res = M(r"\frac{dA}{dt} = 2\pi(10)(2) = 40\pi\ \text{cm}^2\text{/s}", 46, DERIV).next_to(right, DOWN, buff=0.6)
            self.play(Write(res), run_time=1.2)
        self.clear()
        self.example("A growing square", r"The side $s$ of a square grows at $3$ cm/s. How fast is its area $A = s^2$ growing when $s = 4$ cm?",
                     [r"A = s^2,\ \text{so}\ \frac{dA}{dt} = 2s\,\frac{ds}{dt}", r"= 2(4)(3) = 24 \text{ cm}^2\text{/s}"], at=[1, 2])

        with self.beat("Close") as b:
            steps = VGroup(T("1. Relate the quantities.", 44), T(r"2. Differentiate with respect to $t$.", 44), T("3. Substitute.", 44)).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
            for m in steps:
                self.play(FadeIn(m, shift=RIGHT * 0.2), run_time=0.6)
        self.clear()

        self.examples_card()
        self.example("Example 1: The ripple's area", r"A ripple's radius grows at $2$ cm/s. How fast is the area growing when $r = 10$ cm?",
                     [r"A = \pi r^2", r"\frac{dA}{dt} = 2\pi r\,\frac{dr}{dt}", r"= 2\pi(10)(2) = 40\pi\ \text{cm}^2\text{/s}"], at=[1, 2, 3])
        self.example("Example 2: A point on a circle", r"$x^2 + y^2 = 25$. When $x = 3$ and $y = 4$, $\dfrac{dx}{dt} = 2$. Find $\dfrac{dy}{dt}$.",
                     [r"2x\,\frac{dx}{dt} + 2y\,\frac{dy}{dt} = 0", r"2(3)(2) + 2(4)\,\frac{dy}{dt} = 0", r"\frac{dy}{dt} = -\frac{12}{8} = -\frac32"], at=[1, 2, 3])
        self.example("Example 3: A melting ice cube", r"An ice cube's edge shrinks at $0.1$ cm/min. How fast is its volume changing when the edge is $5$ cm?",
                     [r"V = s^3, \quad \frac{dV}{dt} = 3s^2\,\frac{ds}{dt}", r"\frac{ds}{dt} = -0.1", r"\frac{dV}{dt} = 3(25)(-0.1) = -7.5\ \text{cm}^3\text{/min}"], at=[1, 2, 3])
        self.finish()
