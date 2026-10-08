"""Topic 4.4: Introduction to related rates. Narration comes from transcripts/4_4.md.

Adder (2026-10-03): 4.4 only SETS UP related rates problems. Every example ends at the differentiated equation, written
in five named steps (know, want, fixed, equation, differentiate). Topic 4.5 solves the same examples."""
import numpy as np
from manim import *

from kit import *
from style import *
from props import fig_cars, fig_cone, fig_ladder, fig_ripple, fig_shadow, fig_square, pond_ripple

CONE_V = r" (The volume of a cone with radius $r$ and height $h$ is $V = \tfrac13\pi r^2 h$.)"
SETUP = r" Set it up: stop at the differentiated equation."


def stone():
    s = Ellipse(width=0.42, height=0.3).set_fill(DIM, 1).set_stroke(INK, 2)
    return VGroup(s, Ellipse(width=0.14, height=0.07).set_fill(WHITE, 0.45).set_stroke(width=0).move_to(s).shift(UP * 0.06 + LEFT * 0.07))


class Lesson(TranscriptScene):
    NUM = "4.4"

    def construct(self):
        R = ValueTracker(0.05)
        center = LEFT * 3
        pond = Ellipse(width=7.2, height=6.4).set_fill(FUNC, 0.1).set_stroke(FUNC, 2, opacity=0.35).move_to(center)
        ring = always_redraw(lambda: pond_ripple(R.get_value(), center))
        read = always_redraw(lambda: VGroup(M(rf"r = {R.get_value() * 4:.1f}\text{{ cm}}", 40, SECANT),
                                            M(rf"A = {np.pi * (R.get_value() * 4) ** 2:.0f}\text{{ cm}}^2", 40, FUNC)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=1.2))
        with self.beat("A ripple") as b:
            st = stone().move_to(center + UP * 3.4)
            self.play(FadeIn(pond), run_time=0.6)
            self.play(st.animate.move_to(center).scale(0.6), run_time=0.8, rate_func=rate_functions.ease_in_quad)
            self.play(FadeOut(st, scale=0.3), run_time=0.2)
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
            right = VGroup(M(r"\frac{dA}{dt} = 2\pi r\,\frac{dr}{dt}", 46, DERIV), T(r"then $r = 10$, $\frac{dr}{dt} = 2$ go in", 32, DIM)).arrange(DOWN, buff=0.45)
            right.shift(RIGHT * 3.2 + DOWN * 0.4)
            self.play(FadeIn(right[0]), run_time=1)
            b.line(2)
            self.play(FadeIn(right[1]), run_time=0.8)
            nxt = T(r"Substituting and solving: Topic 4.5", 34, SECANT).to_edge(DOWN, buff=0.8)
            self.play(FadeIn(nxt), run_time=0.8)
        self.clear()

        with self.beat("Formulas you need") as b:
            head = T(r"No formula sheet on the AP exam", 46, SECANT).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), run_time=0.8)
            b.line(1)
            know = VGroup(T(r"Know these by heart:", 36, DIM),
                          M(r"\text{circle: } A = \pi r^2, \quad C = 2\pi r", 40),
                          M(r"\text{triangle: } A = \tfrac12 bh \qquad \text{rectangle: } A = lw", 40),
                          M(r"a^2 + b^2 = c^2 \qquad \text{similar triangles}", 40)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            know.next_to(head, DOWN, buff=0.5)
            for m in know:
                self.play(FadeIn(m, shift=RIGHT * 0.2), run_time=0.6)
            b.line(2)
            given = callout(r"Cone, cylinder, sphere: the volume formula \\ is given in the problem when you need it.", INK, 34)
            given.next_to(know, DOWN, buff=0.5)
            self.play(FadeIn(given), run_time=0.8)
        self.clear()

        steps = VGroup(T(r"1. \textbf{Know:} values at the instant, and the given rates", 38),
                       T(r"2. \textbf{Want:} the rate you're after", 38),
                       T(r"3. \textbf{Fixed:} constants that never change", 38),
                       T(r"4. \textbf{Equation:} relate the quantities", 38),
                       T(r"5. \textbf{Differentiate} with respect to $t$", 38)).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        with self.beat("Five steps to the equation") as b:
            for i, m in enumerate(steps):
                b.line(i + 1)
                self.play(FadeIn(m, shift=RIGHT * 0.2), run_time=0.6)
        self.clear()

        self.example("A growing square", r"The side $s$ of a square grows at $3$ cm/s. How fast is its area $A$ growing when $s = 4$ cm? Set it up: stop at the differentiated equation.",
                     [r"TEXT:Know: $\frac{ds}{dt} = 3$ cm/s,", r"TEXT:\quad and $s = 4$ cm now.", r"TEXT:Want: $\frac{dA}{dt}$. Fixed: none.",
                      r"A = s^2", r"\frac{dA}{dt} = 2s\,\frac{ds}{dt}"], at=[1, 1, 2, 3, 4], figure=fig_square(), follow=True)

        with self.beat("Close") as b:
            again = steps.copy().scale(0.9)
            self.play(FadeIn(again), run_time=0.8)
            b.line(1)
            self.play(again[4].animate.set_color(SECANT), run_time=0.8)
        self.clear()

        self.examples_card()
        self.example("Example 1: The ripple's area", r"A ripple's radius grows at $2$ cm/s. How fast is the area growing when $r = 10$ cm? Set it up: stop at the differentiated equation.",
                     [r"TEXT:Know: $\frac{dr}{dt} = 2$ cm/s, $r = 10$ cm.", r"TEXT:Want: $\frac{dA}{dt}$.", r"A = \pi r^2",
                      r"\frac{dA}{dt} = 2\pi r\,\frac{dr}{dt}"], at=[1, 1, 2, 3], figure=fig_ripple())
        self.example("Example 2: The ladder",
                     r"A $13$-ft ladder leans against a wall. The bottom slides away at $2$ ft/s. How fast is the top sliding down when the bottom is $5$ ft from the wall? Set it up: stop at the differentiated equation.",
                     [r"TEXT:Know: $\frac{dx}{dt} = 2$ ft/s, $x = 5$ ft.", r"TEXT:Want: $\frac{dy}{dt}$.",
                      r"TEXT:Fixed: the ladder, $13$ ft.", r"x^2 + y^2 = 13^2", r"2x\,\frac{dx}{dt} + 2y\,\frac{dy}{dt} = 0"],
                     at=[1, 2, 3, 4, 5], figure=fig_ladder(), follow=True)
        self.example("Example 3: Filling a cone",
                     r"Water pours into a cone, point down, $9$ ft tall with radius $3$ ft, at $2$ ft$^3$/min. How fast is the water rising when it is $6$ ft deep? (The volume of a cone with radius $r$ and height $h$ is $V = \tfrac13\pi r^2 h$.) Set it up: stop at the differentiated equation.",
                     [r"TEXT:Know: $\frac{dV}{dt} = 2$ ft$^3$/min, $h = 6$ ft.", r"TEXT:Want: $\frac{dh}{dt}$.",
                      r"TEXT:Fixed: the cone's shape.", r"\frac rh = \frac39,\ \text{so}\ r = \frac h3",
                      r"V = \frac13\pi\left(\frac h3\right)^2 h = \frac{\pi}{27}h^3", r"\frac{dV}{dt} = \frac{\pi}{9}h^2\,\frac{dh}{dt}"],
                     at=[1, 1, 2, 2, 3, 4], figure=fig_cone(), follow=True)
        self.example("Example 4: Two cars",
                     r"Two cars leave an intersection at the same time, one north at $30$ mph and one east at $40$ mph. How fast is the distance between them growing after $2$ hours? Set it up: stop at the differentiated equation.",
                     [r"TEXT:Know: $\frac{dx}{dt} = 40$ mph east,", r"TEXT:\quad $\frac{dy}{dt} = 30$ mph north, $t = 2$ h.", r"TEXT:Want: $\frac{dz}{dt}$.",
                      r"z^2 = x^2 + y^2", r"2z\,\frac{dz}{dt} = 2x\,\frac{dx}{dt} + 2y\,\frac{dy}{dt}"], at=[1, 1, 2, 3, 4], figure=fig_cars())
        self.example("Example 5: A shadow",
                     r"Ana, who is $5$ ft tall, walks away from a $15$-ft lamppost at $4$ ft/s. How fast is her shadow lengthening? Set it up: stop at the differentiated equation.",
                     [r"TEXT:Know: $\frac{dx}{dt} = 4$ ft/s.", r"TEXT:Want: $\frac{ds}{dt}$. Fixed: $15$ and $5$ ft.",
                      r"\frac{15}{x + s} = \frac{5}{s}", r"15s = 5x + 5s,\ \text{so}\ s = \frac x2", r"\frac{ds}{dt} = \frac12\,\frac{dx}{dt}"],
                     at=[1, 1, 2, 3, 4], figure=fig_shadow())
        self.finish()
