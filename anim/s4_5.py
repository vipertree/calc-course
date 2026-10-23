"""Topic 4.5: Solving related rates problems. Narration comes from transcripts/4_5.md.

Adder (2026-10-23): 4.5 solves the SAME problems as 4.4, in the same order (ripple, ladder, two cars, shadow, cone), now
with the numbers. Six steps: know (with anything fixed noted there), want, equation (fixed quantities go in as numbers),
differentiate, substitute and solve, answer with units. No separate "fixed" step. The car problem has Priya driving
TOWARD the intersection, in meters per second, so dx/dt is negative."""
import numpy as np
from manim import *

from kit import *
from style import *
from props import brick_wall, car_sprite, face, fig_cars, fig_cone, fig_ladder, fig_ripple, fig_shadow, ladder


class Lesson(TranscriptScene):
    NUM = "4.5"

    def construct(self):
        L, base = 5.4, np.array([-4.6, -3.0, 0])
        X = ValueTracker(0.8)
        wall = brick_wall(height=6.2, width=0.6, brick_h=0.3).next_to(base, LEFT, buff=0).align_to(base, DOWN)
        floor = Line(base + LEFT * 0.6, base + RIGHT * 6.4, color=DIM, stroke_width=6)
        top = lambda: base + UP * np.sqrt(L * L - X.get_value() ** 2)
        foot = lambda: base + RIGHT * X.get_value()
        lad = always_redraw(lambda: ladder(foot(), top(), width=0.5))
        dots = always_redraw(lambda: VGroup(Dot(foot(), color=DERIV, radius=0.1), Dot(top(), color=TANGENT, radius=0.1)))
        speed = always_redraw(lambda: VGroup(
            M(r"\text{foot: } 2\ \text{ft/s}", 40, DERIV),
            M(rf"\text{{top: }} {2 * X.get_value() / np.sqrt(L * L - X.get_value() ** 2):.2f}\ \text{{ft/s}}", 40, TANGENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.9).shift(UP * 1.2))
        with self.beat("A sliding ladder") as b:
            self.play(FadeIn(wall), Create(floor), run_time=0.8)
            self.add(lad, dots)
            self.play(FadeIn(speed), run_time=0.6)
            self.play(X.animate.set_value(2.6), run_time=3, rate_func=linear)
            b.line(1)
            self.play(X.animate.set_value(5.1), run_time=3.2, rate_func=linear)
            b.line(2)
            self.play(Indicate(speed[1], color=TANGENT), run_time=1)
        self.clear()
        self.title()

        steps = VGroup(T(r"1. \textbf{Know:} the rates and values given, with units, and anything fixed", 36),
                       T(r"2. \textbf{Want:} the rate you're after", 36),
                       T(r"3. \textbf{Equation:} relate the quantities (fixed ones are numbers)", 36),
                       T(r"4. \textbf{Differentiate} with respect to $t$", 36),
                       T(r"5. \textbf{Substitute} the values at the instant, and \textbf{solve}", 36, SECANT),
                       T(r"6. \textbf{Answer} with units, and say what it means", 36, SECANT)).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        steps.set_max_width(12.6)
        with self.beat("Six steps") as b:
            for i, m in enumerate(steps):
                b.line(i + 1)
                self.play(FadeIn(m, shift=RIGHT * 0.2), run_time=0.6)
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
        self.clear()

        with self.beat("Shrinking means negative") as b:
            o = np.array([-4.6, -0.6, 0])
            road = Line(o + LEFT * 0.8, o + RIGHT * 10.2, color=DIM, stroke_width=26, stroke_opacity=0.35)
            cross = Line(o + DOWN * 2.4, o + UP * 2.4, color=DIM, stroke_width=26, stroke_opacity=0.35)
            P = ValueTracker(80.0)
            k = 0.1                                       # scene units per meter
            car = face(car_sprite(1.1), -1)
            car.add_updater(lambda m: m.move_to(o + RIGHT * (P.get_value() * k) + UP * 0.32))
            gap = always_redraw(lambda: BraceBetweenPoints(o, o + RIGHT * P.get_value() * k, DOWN, color=DIM).shift(DOWN * 0.15))
            xl = always_redraw(lambda: M(rf"x = {P.get_value():.0f}\ \text{{m}}", 36).next_to(gap, DOWN, buff=0.1))
            rate = M(r"\frac{dx}{dt} = -20\ \text{m/s}", 46, TANGENT).to_edge(UP, buff=0.7).shift(RIGHT * 1.5)
            b.line(1)
            self.play(FadeIn(road), FadeIn(cross), FadeIn(car), FadeIn(gap), FadeIn(xl), run_time=0.8)
            self.play(P.animate.set_value(40), run_time=2.4, rate_func=linear)
            self.play(Write(rate), run_time=0.8)
            b.line(2)
            rule = callout(r"Shrinking: a negative rate. \quad Growing: a positive rate.", INK, 34).to_edge(DOWN, buff=0.5)
            self.play(FadeIn(rule), run_time=0.8)
            car.clear_updaters()
        self.clear()

        self.example("The ripple",
                     r"A stone drops into a pond, and a circular ripple spreads out. Its radius grows at $2$ cm/s. How fast is the area inside the ripple growing when the radius is $10$ cm?",
                     [r"TEXT:Know: $\frac{dr}{dt} = 2$ cm/s, and $r = 10$ cm now.", r"TEXT:Want: $\frac{dA}{dt}$.", r"A = \pi r^2",
                      r"\frac{dA}{dt} = 2\pi r\,\frac{dr}{dt}", r"\frac{dA}{dt} = 2\pi(10)(2)", r"\frac{dA}{dt} = 40\pi \approx 126",
                      r"TEXT:The area grows at $40\pi \approx 126$ cm$^2$/s."], at=[1, 2, 3, 4, 5, 6, 7], figure=fig_ripple(), follow=True)

        with self.beat("Close") as b:
            again = steps.copy().scale(0.9)
            self.play(FadeIn(again), run_time=0.8)
            self.play(again[3].animate.set_color(TANGENT), again[4].animate.set_color(TANGENT), run_time=0.8)
        self.clear()

        self.examples_card()
        self.example("Example 1: The ladder",
                     r"A $13$-ft ladder leans against a wall, and its bottom slides away from the wall at $2$ ft/s. How fast is the top sliding down when the bottom is $5$ ft from the wall?",
                     [r"TEXT:Know: $\frac{dx}{dt} = 2$ ft/s, and $x = 5$ ft now.", r"TEXT:\quad The ladder is fixed at $13$ ft.", r"TEXT:Want: $\frac{dy}{dt}$.",
                      r"x^2 + y^2 = 13^2 \quad (13\text{ is fixed})", r"2x\,\frac{dx}{dt} + 2y\,\frac{dy}{dt} = 0", r"x = 5:\ \ y = \sqrt{169 - 25} = 12",
                      r"2(5)(2) + 2(12)\,\frac{dy}{dt} = 0", r"20 + 24\,\frac{dy}{dt} = 0", r"\frac{dy}{dt} = -\frac{20}{24} = -\frac56\ \text{ft/s}",
                      r"TEXT:The top slides down at $\frac56$ ft/s."], at=[1, 1, 2, 3, 4, 5, 6, 7, 8, 9], figure=fig_ladder(), follow=True)
        self.example("Example 2: Two cars",
                     r"Priya drives west toward an intersection at $20$ m/s, and Kai drives north away from it at $15$ m/s. How fast is the distance between the two cars changing when Priya is $80$ m from the intersection and Kai is $60$ m from it?",
                     [r"TEXT:Know: $\frac{dx}{dt} = -20$ m/s ($x$ shrinking), $x = 80$ m,", r"TEXT:\quad $\frac{dy}{dt} = 15$ m/s, $y = 60$ m.", r"TEXT:Want: $\frac{dz}{dt}$.",
                      r"z^2 = x^2 + y^2", r"2z\,\frac{dz}{dt} = 2x\,\frac{dx}{dt} + 2y\,\frac{dy}{dt}", r"z = \sqrt{6400 + 3600} = 100",
                      r"2(100)\,\frac{dz}{dt} = 2(80)(-20) + 2(60)(15)", r"200\,\frac{dz}{dt} = -3200 + 1800 = -1400", r"\frac{dz}{dt} = -7\ \text{m/s}",
                      r"TEXT:The distance is shrinking at $7$ m/s."], at=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], figure=fig_cars())
        self.example("Example 3: A shadow",
                     r"Ana, who is $5$ ft tall, walks away from a $15$-ft lamppost at $4$ ft/s. How fast is her shadow lengthening when she is $10$ ft from the post?",
                     [r"TEXT:Know: $\frac{dx}{dt} = 4$ ft/s, and $x = 10$ ft now.", r"TEXT:\quad The heights are fixed at $15$ ft and $5$ ft.", r"TEXT:Want: $\frac{ds}{dt}$.",
                      r"\frac{15}{x + s} = \frac{5}{s},\ \text{so}\ s = \frac x2", r"\frac{ds}{dt} = \frac12\,\frac{dx}{dt}", r"\frac{ds}{dt} = \frac12(4) = 2\ \text{ft/s}",
                      r"TEXT:The shadow lengthens at $2$ ft/s.", r"TEXT:($x = 10$ never went in: it's $2$ ft/s everywhere.)"],
                     at=[1, 1, 2, 3, 4, 5, 6, 7], figure=fig_shadow())
        self.example("Example 4: Filling a cone",
                     r"Water pours into a cone, point down, that is $9$ ft tall with radius $3$ ft at the top, at $2$ ft$^3$/min. How fast is the water rising when it is $6$ ft deep? (The volume of a cone with radius $r$ and height $h$ is $V = \tfrac13\pi r^2 h$.)",
                     [r"TEXT:Know: $\frac{dV}{dt} = 2$ ft$^3$/min, and $h = 6$ ft now.", r"TEXT:\quad The cone is fixed: $9$ ft tall, radius $3$ ft.", r"TEXT:Want: $\frac{dh}{dt}$.",
                      r"r = \frac h3,\ \text{so}\ V = \frac{\pi}{27}h^3", r"\frac{dV}{dt} = \frac{\pi}{9}h^2\,\frac{dh}{dt}", r"2 = \frac{\pi}{9}(6)^2\,\frac{dh}{dt}",
                      r"2 = 4\pi\,\frac{dh}{dt}", r"\frac{dh}{dt} = \frac{2}{4\pi} = \frac{1}{2\pi}", r"TEXT:The water rises at $\frac{1}{2\pi} \approx 0.159$ ft/min."],
                     at=[1, 1, 2, 3, 4, 5, 6, 7, 8], figure=fig_cone())
        self.finish()
