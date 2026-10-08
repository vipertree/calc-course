"""Topic 4.5: Solving related rates problems. Narration comes from transcripts/4_5.md.

Adder (2026-10-03): 4.5 solves the SAME examples 4.4 set up (shadow, ladder, cone, two cars, ripple). Each opens by
recalling the setup, names every step (know, want, fixed, equation, differentiate, substitute and solve), and has a
labeled diagram."""
import numpy as np
from manim import *

from kit import *
from style import *
from props import brick_wall, fig_cars, fig_cone, fig_ladder, fig_ripple, fig_shadow, ladder, water_cone

CONE_V = r" (The volume of a cone with radius $r$ and height $h$ is $V = \tfrac13\pi r^2 h$.)"


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

        steps = VGroup(T(r"1. \textbf{Know:} values at the instant, given rates", 38), T(r"2. \textbf{Want:} the rate you're after", 38),
                       T(r"3. \textbf{Fixed:} constants that never change", 38), T(r"4. \textbf{Equation:} relate the quantities", 38),
                       T(r"5. \textbf{Differentiate} with respect to $t$", 38),
                       T(r"6. \textbf{Substitute and solve}, with units", 38, SECANT)).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        with self.beat("Six steps") as b:
            self.play(FadeIn(steps[:5], shift=RIGHT * 0.2), run_time=1.2)
            b.line(1)
            self.play(FadeIn(steps[5], shift=RIGHT * 0.2), Circumscribe(steps[5], color=SECANT), run_time=1.2)
            b.line(2)
            self.play(Indicate(steps[4], color=SECANT), run_time=1)
        self.clear()

        with self.beat("Where the equation comes from") as b:
            tri = VGroup(Polygon(ORIGIN, RIGHT * 2, RIGHT * 2 + UP * 1.4, color=INK), M(r"x^2 + y^2 = z^2", 32))
            sim = VGroup(VGroup(Polygon(ORIGIN, RIGHT * 2.2, UP * 1.5, color=INK), Polygon(ORIGIN, RIGHT * 1.1, UP * 0.75, color=SECANT)), M(r"\frac{r}{h} = \frac{R}{H}", 32))
            cone, _, _ = water_cone(0.6, H=1.6, R=0.8)
            vol = VGroup(cone, M(r"V = \tfrac13\pi r^2 h \ \ (\text{given})", 30))
            ang = VGroup(VGroup(Polygon(ORIGIN, RIGHT * 2, RIGHT * 2 + UP * 1.4, color=INK), Arc(0.5, 0, np.arctan(0.7), color=TANGENT)), M(r"\tan\theta = \frac{y}{x}", 32))
            cards = VGroup(tri, sim, vol, ang)
            for c in cards:
                c.arrange(DOWN, buff=0.35)
            cards.arrange_in_grid(2, 2, buff=(1.6, 0.8)).shift(DOWN * 0.2)
            self.play(FadeIn(tri), run_time=0.6)
            b.line(1)
            self.play(FadeIn(sim), run_time=0.6)
            b.line(2)
            self.play(FadeIn(vol), FadeIn(ang), run_time=0.8)
        self.clear()

        with self.beat("Eliminate first") as b:
            fig = fig_cone(0.6, H=4.2, R=1.4).shift(LEFT * 3.5 + DOWN * 0.4)
            self.play(FadeIn(fig[0]), run_time=1)
            b.line(1)
            self.play(FadeIn(fig[1:]), run_time=1)
            eq = VGroup(M(r"\frac{r}{h} = \frac{3}{9}", 52), M(r"r = \frac{h}{3}", 56, DERIV)).arrange(DOWN, buff=0.6).to_edge(RIGHT, buff=1.4).shift(UP * 0.8)
            self.play(Write(eq[0]), run_time=1)
            b.line(2)
            self.play(Write(eq[1]), run_time=0.8)
            v = M(r"V = \tfrac13\pi\left(\tfrac{h}{3}\right)^2 h = \tfrac{\pi}{27}h^3", 44).next_to(eq, DOWN, buff=0.7)
            self.play(Write(v), run_time=1.2)
        self.clear()
        self.example("A shadow", r"Ana, who is $5$ ft tall, walks away from a $15$-ft lamppost at $4$ ft/s. How fast is her shadow lengthening?",
                     [r"TEXT:Know: $\frac{dx}{dt} = 4$ ft/s. Want: $\frac{ds}{dt}$.", r"TEXT:Fixed: $15$ and $5$ ft.",
                      r"\frac{15}{x + s} = \frac{5}{s},\ \text{so}\ s = \frac x2,\quad \frac{ds}{dt} = \frac12\,\frac{dx}{dt}",
                      r"\frac{ds}{dt} = \frac12(4) = 2 \text{ ft/s}", r"TEXT:The shadow lengthens at $2$ ft/s, at every moment."],
                     at=[1, 1, 2, 3, 4], figure=fig_shadow(), follow=True)

        with self.beat("Close") as b:
            again = steps.copy().scale(0.9)
            self.play(FadeIn(again), run_time=0.8)
            self.play(again[4].animate.set_color(TANGENT), again[5].animate.set_color(TANGENT), run_time=0.8)
        self.clear()

        self.examples_card()
        self.example("Example 1: The ladder",
                     r"A $13$-ft ladder leans against a wall. The bottom slides away at $2$ ft/s. How fast is the top sliding down when the bottom is $5$ ft from the wall?",
                     [r"TEXT:Know: $\frac{dx}{dt} = 2$ ft/s, $x = 5$ ft.", r"TEXT:Want: $\frac{dy}{dt}$. Fixed: $13$ ft.",
                      r"x^2 + y^2 = 13^2, \quad 2x\,\frac{dx}{dt} + 2y\,\frac{dy}{dt} = 0", r"x = 5:\ \ y = \sqrt{169 - 25} = 12",
                      r"2(5)(2) + 2(12)\,\frac{dy}{dt} = 0", r"\frac{dy}{dt} = -\frac{20}{24} = -\frac56\ \text{ft/s}",
                      r"TEXT:The top slides down at $\frac56$ ft/s."], at=[1, 1, 2, 3, 4, 5, 5], figure=fig_ladder())
        self.example("Example 2: Filling a cone",
                     r"Water pours into a cone, point down, $9$ ft tall with radius $3$ ft, at $2$ ft$^3$/min. How fast is the water rising when it is $6$ ft deep? (The volume of a cone with radius $r$ and height $h$ is $V = \tfrac13\pi r^2 h$.)",
                     [r"TEXT:Know: $\frac{dV}{dt} = 2$ ft$^3$/min, $h = 6$ ft.", r"TEXT:Want: $\frac{dh}{dt}$. Fixed: $r = \frac h3$.",
                      r"V = \frac{\pi}{27}h^3, \quad \frac{dV}{dt} = \frac{\pi}{9}h^2\,\frac{dh}{dt}", r"2 = \frac{\pi}{9}(36)\,\frac{dh}{dt} = 4\pi\,\frac{dh}{dt}",
                      r"\frac{dh}{dt} = \frac{1}{2\pi} \approx 0.16\ \text{ft/min}"], at=[1, 1, 2, 3, 4], figure=fig_cone())
        self.example("Example 3: Two cars",
                     r"Two cars leave an intersection at the same time, one north at $30$ mph and one east at $40$ mph. How fast is the distance between them growing after $2$ hours?",
                     [r"TEXT:Know: $\frac{dx}{dt} = 40$, $\frac{dy}{dt} = 30$ mph,", r"TEXT:\quad $t = 2$ h. Want: $\frac{dz}{dt}$.",
                      r"z^2 = x^2 + y^2, \quad z\,\frac{dz}{dt} = x\,\frac{dx}{dt} + y\,\frac{dy}{dt}", r"x = 80,\ \ y = 60,\ \ z = \sqrt{6400 + 3600} = 100",
                      r"100\,\frac{dz}{dt} = 80(40) + 60(30) = 5000", r"\frac{dz}{dt} = 50\ \text{mph}"], at=[1, 1, 2, 3, 4, 5], figure=fig_cars())
        self.example("Example 4: The ripple's area", r"A ripple's radius grows at $2$ cm/s. How fast is the area growing when $r = 10$ cm?",
                     [r"TEXT:Know: $\frac{dr}{dt} = 2$ cm/s, $r = 10$ cm.", r"TEXT:Want: $\frac{dA}{dt}$.", r"A = \pi r^2, \quad \frac{dA}{dt} = 2\pi r\,\frac{dr}{dt}",
                      r"\frac{dA}{dt} = 2\pi(10)(2) = 40\pi \approx 126\ \text{cm}^2\text{/s}"], at=[1, 1, 2, 3], figure=fig_ripple())
        self.finish()
