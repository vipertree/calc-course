"""Topic 4.5: Solving related rates problems. Narration comes from transcripts/4_5.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def cone_fig(depth=0.6, H=4.2, Rr=1.4):
    """A cone, point down, with water to `depth` (fraction of H). Returns (group, tip point)."""
    tip = ORIGIN
    rim_l, rim_r = tip + UP * H + LEFT * Rr, tip + UP * H + RIGHT * Rr
    shell = VGroup(Line(tip, rim_l, color=INK), Line(tip, rim_r, color=INK), DashedLine(rim_l, rim_r, color=DIM))
    h = H * depth
    r = Rr * depth
    water = Polygon(tip, tip + UP * h + LEFT * r, tip + UP * h + RIGHT * r, color=FUNC, fill_color=FUNC, fill_opacity=0.45, stroke_width=0)
    return VGroup(water, shell), h, r


class Lesson(TranscriptScene):
    NUM = "4.5"

    def construct(self):
        L, base = 5.4, np.array([-4.8, -3.0, 0])
        X = ValueTracker(0.8)
        wall = Line(base, base + UP * 6, color=DIM, stroke_width=6)
        floor = Line(base, base + RIGHT * 6.4, color=DIM, stroke_width=6)
        top = lambda: base + UP * np.sqrt(L * L - X.get_value() ** 2)
        foot = lambda: base + RIGHT * X.get_value()
        ladder = always_redraw(lambda: Line(foot(), top(), color=SECANT, stroke_width=8))
        dots = always_redraw(lambda: VGroup(Dot(foot(), color=DERIV, radius=0.1), Dot(top(), color=TANGENT, radius=0.1)))
        speed = always_redraw(lambda: VGroup(
            M(r"\text{foot: } 2\ \text{ft/s}", 40, DERIV),
            M(rf"\text{{top: }} {2 * X.get_value() / np.sqrt(L * L - X.get_value() ** 2):.2f}\ \text{{ft/s}}", 40, TANGENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.9).shift(UP * 1.2))
        with self.beat("A sliding ladder") as b:
            self.play(Create(wall), Create(floor), run_time=0.8)
            self.add(ladder, dots)
            self.play(FadeIn(speed), run_time=0.6)
            self.play(X.animate.set_value(2.6), run_time=3, rate_func=linear)
            b.line(1)
            self.play(X.animate.set_value(5.1), run_time=3.2, rate_func=linear)
            b.line(2)
            self.play(Indicate(speed[1], color=TANGENT), run_time=1)
        self.clear()
        self.title()

        steps = VGroup(T("1. Draw and label.", 42), T("2. Rates you know, rate you want, with signs.", 42),
                       T("3. An equation that holds at every moment.", 42), T(r"4. Differentiate with respect to $t$.", 42),
                       T("5. Substitute, then solve.", 42)).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        with self.beat("Five steps") as b:
            for i, m in enumerate(steps):
                b.line(min(i + 1, 4))
                self.play(FadeIn(m, shift=RIGHT * 0.2), run_time=0.6)
        self.clear()

        with self.beat("Where the equation comes from") as b:
            tri = VGroup(Polygon(ORIGIN, RIGHT * 2, RIGHT * 2 + UP * 1.4, color=INK), M(r"x^2 + y^2 = z^2", 32))
            sim = VGroup(VGroup(Polygon(ORIGIN, RIGHT * 2.2, UP * 1.5, color=INK), Polygon(ORIGIN, RIGHT * 1.1, UP * 0.75, color=SECANT)), M(r"\frac{r}{h} = \frac{R}{H}", 32))
            cone, _, _ = cone_fig(0.6, H=1.6, Rr=0.8)
            vol = VGroup(cone, M(r"V = \tfrac13\pi r^2 h", 32))
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
            cone, h, r = cone_fig(0.6)
            cone.shift(LEFT * 3.5 + DOWN * 2.4)
            self.play(Create(cone[1]), FadeIn(cone[0]), run_time=1)
            b.line(1)
            tip = cone[1][0].get_start()
            hline = DashedLine(tip, tip + UP * h, color=SECANT)
            rline = Line(tip + UP * h, tip + UP * h + RIGHT * r, color=DERIV, stroke_width=5)
            labs = VGroup(M("h", 36, SECANT).next_to(hline, LEFT, buff=0.15), M("r", 36, DERIV).next_to(rline, UP, buff=0.1))
            big = VGroup(M("9", 32, DIM).next_to(cone[1][0], LEFT, buff=0.5), M("3", 32, DIM).next_to(cone[1][2], UP, buff=0.15).shift(RIGHT * 0.7))
            self.play(Create(hline), Create(rline), FadeIn(labs), FadeIn(big), run_time=1)
            eq = VGroup(M(r"\frac{r}{h} = \frac{3}{9}", 52), M(r"r = \frac{h}{3}", 56, DERIV)).arrange(DOWN, buff=0.6).to_edge(RIGHT, buff=1.4).shift(UP * 0.6)
            self.play(Write(eq[0]), run_time=1)
            b.line(2)
            self.play(Write(eq[1]), run_time=0.8)
            v = M(r"V = \tfrac13\pi\left(\tfrac{h}{3}\right)^2 h = \tfrac{\pi}{27}h^3", 44).next_to(eq, DOWN, buff=0.7)
            self.play(Write(v), run_time=1.2)
        self.clear()
        self.example("A shadow", r"Ana, who is $5$ ft tall, walks away from a $15$-ft lamppost at $4$ ft/s. How fast is her shadow lengthening?",
                     [r"\frac{15}{x + s} = \frac{5}{s},\ \text{so}\ 15s = 5x + 5s", r"s = \frac{x}{2}", r"\frac{ds}{dt} = \frac12\,\frac{dx}{dt} = \frac12(4) = 2 \text{ ft/s}"], at=[1, 2, 3])

        with self.beat("Close") as b:
            again = steps.copy().scale(0.9)
            self.play(FadeIn(again), run_time=0.8)
            self.play(again[3].animate.set_color(TANGENT), again[4].animate.set_color(TANGENT), run_time=0.8)
        self.clear()

        self.examples_card()
        self.example("Example 1: The ladder",
                     r"A $13$-ft ladder leans against a wall. The bottom slides away at $2$ ft/s. How fast is the top sliding down when the bottom is $5$ ft from the wall?",
                     [r"x^2 + y^2 = 169", r"2x\,\frac{dx}{dt} + 2y\,\frac{dy}{dt} = 0", r"x = 5:\ \ y = \sqrt{169 - 25} = 12",
                      r"2(5)(2) + 2(12)\,\frac{dy}{dt} = 0", r"\frac{dy}{dt} = -\frac{20}{24} = -\frac56\ \text{ft/s}"], at=[1, 2, 3, 4, 5])
        self.example("Example 2: Filling a cone",
                     r"Water pours into a cone, point down, $9$ ft tall with radius $3$ ft, at $2$ ft$^3$/min. How fast is the water rising when it is $6$ ft deep?",
                     [r"\frac{r}{h} = \frac39,\ \text{so}\ r = \frac h3", r"V = \frac13\pi\left(\frac h3\right)^2 h = \frac{\pi}{27}h^3",
                      r"\frac{dV}{dt} = \frac{\pi}{9}h^2\,\frac{dh}{dt}", r"2 = \frac{\pi}{9}(36)\frac{dh}{dt} = 4\pi\,\frac{dh}{dt}",
                      r"\frac{dh}{dt} = \frac{1}{2\pi} \approx 0.16\ \text{ft/min}"], at=[1, 2, 3, 4, 5])
        self.example("Example 3: Two cars",
                     r"Two cars leave an intersection at the same time, one north at $30$ mph and one east at $40$ mph. How fast is the distance between them growing after $2$ hours?",
                     [r"z^2 = x^2 + y^2", r"z\,\frac{dz}{dt} = x\,\frac{dx}{dt} + y\,\frac{dy}{dt}", r"x = 80,\ \ y = 60,\ \ z = 100",
                      r"100\,\frac{dz}{dt} = 80(40) + 60(30) = 5000", r"\frac{dz}{dt} = 50\ \text{mph}"], at=[1, 2, 3, 4, 5])
        self.finish()
