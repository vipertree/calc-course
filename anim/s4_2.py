"""Topic 4.2: Straight-line motion. Narration comes from transcripts/4_2.md.
Running example x(t) = t^3 - 6t^2 + 9t: at rest at t = 1, 3; distance on [0, 4] is 12."""
import numpy as np
from manim import *

from kit import *
from style import *


def X(t):
    return t ** 3 - 6 * t * t + 9 * t


def V(t):
    return 3 * t * t - 12 * t + 9


class Lesson(TranscriptScene):
    NUM = "4.2"

    def track(self):
        nl = NumberLine(x_range=[-1, 6, 1], length=9, color=DIM, include_numbers=True, font_size=26).to_edge(UP, buff=0.9)
        return nl

    def construct(self):
        nl = self.track()
        T_ = ValueTracker(0)
        dot = always_redraw(lambda: Dot(nl.n2p(X(T_.get_value())), color=SECANT, radius=0.14))
        ax, al = plot_axes([0, 4.5, 1], [-1, 6, 1], w=7.6, h=3.6, xlabel="t", ylabel="x(t)")
        VGroup(ax, al).to_edge(DOWN, buff=0.5)
        curve = always_redraw(lambda: ax.plot(X, x_range=[0, max(T_.get_value(), 0.01)], color=FUNC, stroke_width=4))
        with self.beat("Back and forth on a line") as b:
            self.play(Create(nl), FadeIn(ax), FadeIn(al), FadeIn(dot), run_time=1)
            self.add(curve)
            self.play(T_.animate.set_value(4.2), run_time=5, rate_func=linear)
            b.line(1)
            self.play(FadeIn(M(r"x(t) = t^3 - 6t^2 + 9t", 38, FUNC).next_to(ax, RIGHT, buff=0.2).shift(UP * 1.2)), run_time=0.8)
            b.line(2)
            note = T(r"the graph is \emph{not} the path", 34, TANGENT).next_to(nl, DOWN, buff=0.3)
            self.play(FadeIn(note), Indicate(dot, color=SECANT), run_time=1)
        self.clear()
        self.title()

        with self.beat("Three functions") as b:
            chain = VGroup(M(r"x(t)", 52, FUNC), M(r"\to", 52, DIM), M(r"v(t) = x'(t)", 52, SECANT), M(r"\to", 52, DIM),
                           M(r"a(t) = v'(t) = x''(t)", 52, TANGENT)).arrange(RIGHT, buff=0.3).shift(UP * 1.6)
            units = VGroup(T("m", 30, DIM).next_to(chain[0], DOWN), T("m/s", 30, DIM).next_to(chain[2], DOWN), T(r"m/s$^2$", 30, DIM).next_to(chain[4], DOWN))
            self.play(Write(chain[0]), run_time=0.6)
            self.play(FadeIn(chain[1]), Write(chain[2]), run_time=0.8)
            self.play(FadeIn(chain[3]), Write(chain[4]), FadeIn(units), run_time=1)
            b.line(2)
            ours = VGroup(M(r"v(t) = 3t^2 - 12t + 9", 48, SECANT), M(r"a(t) = 6t - 12", 48, TANGENT)).arrange(DOWN, buff=0.4).shift(DOWN * 1.2)
            self.play(Write(ours), run_time=1.4)
        self.clear()

        with self.beat("Direction") as b:
            v = M(r"v(t) = 3(t - 1)(t - 3)", 50, SECANT).to_edge(UP, buff=0.5)
            self.play(Write(v), run_time=1)
            b.line(1)
            sl = NumberLine(x_range=[0, 4.5, 1], length=9, color=DIM, include_numbers=True, font_size=28).shift(UP * 0.6)
            signs = VGroup(M("+", 48, DERIV).next_to(sl.n2p(0.5), UP), M("-", 48, TANGENT).next_to(sl.n2p(2), UP), M("+", 48, DERIV).next_to(sl.n2p(3.8), UP))
            self.play(Create(sl), FadeIn(signs), run_time=1.2)
            b.line(2)
            dirs = VGroup(T("right", 32, DERIV).next_to(sl.n2p(0.5), DOWN, buff=0.5), T("left", 32, TANGENT).next_to(sl.n2p(2), DOWN, buff=0.5),
                          T("right", 32, DERIV).next_to(sl.n2p(3.8), DOWN, buff=0.5))
            rests = VGroup(*[T("rest", 28, SECANT).next_to(sl.n2p(k), DOWN, buff=1.2) for k in (1, 3)])
            self.play(FadeIn(dirs), run_time=0.8)
            self.play(FadeIn(rests), *[Flash(sl.n2p(k), color=SECANT) for k in (1, 3)], run_time=1)
        self.clear()

        with self.beat("Speed") as b:
            pair = VGroup(VGroup(M(r"v = -5", 52, TANGENT), Arrow(RIGHT, LEFT, color=TANGENT)).arrange(DOWN),
                          VGroup(M(r"v = 5", 52, DERIV), Arrow(LEFT, RIGHT, color=DERIV)).arrange(DOWN)).arrange(RIGHT, buff=2.5).shift(UP * 0.6)
            self.play(FadeIn(pair), run_time=1)
            b.line(1)
            sp_ = M(r"\text{speed} = |v(t)| = 5", 52, SECANT).shift(DOWN * 1.8)
            self.play(Write(sp_), run_time=1)
        self.clear()

        with self.beat("Speeding up and slowing down") as b:
            road = Line(LEFT * 5, RIGHT * 5, color=DIM).shift(UP * 0.6)
            car = VGroup(RoundedRectangle(width=1.2, height=0.5, corner_radius=0.12, color=SECANT, fill_color=SECANT, fill_opacity=1),
                         Dot(LEFT * 0.35 + DOWN * 0.3, radius=0.12, color=INK), Dot(RIGHT * 0.35 + DOWN * 0.3, radius=0.12, color=INK)).next_to(road, UP, buff=0.05)
            self.play(Create(road), FadeIn(car), run_time=0.8)
            b.line(1)
            labs = VGroup(M(r"v < 0", 40, TANGENT), M(r"a > 0", 40, DERIV), T("slowing down", 34, DIM)).arrange(RIGHT, buff=0.8).shift(DOWN * 0.6)
            self.play(car.animate.shift(LEFT * 3), run_time=2.2, rate_func=rate_functions.ease_out_quad)
            self.play(FadeIn(labs), run_time=0.8)
            b.line(2)
            rule = callout(r"speeding up: $v$ and $a$ have the \textbf{same} sign \\ slowing down: \textbf{opposite} signs", SECANT, 36).shift(DOWN * 2.4)
            self.play(FadeIn(rule), run_time=1)
        self.clear()

        nl = self.track()
        with self.beat("Distance versus displacement") as b:
            self.play(Create(nl), run_time=0.6)
            legs = VGroup(Arrow(nl.n2p(0), nl.n2p(4), buff=0, color=SECANT).shift(DOWN * 0.5),
                          Arrow(nl.n2p(4), nl.n2p(0), buff=0, color=TANGENT).shift(DOWN * 1.0),
                          Arrow(nl.n2p(0), nl.n2p(4), buff=0, color=SECANT).shift(DOWN * 1.5))
            b.line(1)
            disp = M(r"\text{displacement} = x(4) - x(0) = 4", 44).shift(DOWN * 1.4)
            self.play(FadeIn(Dot(nl.n2p(0), color=INK)), FadeIn(Dot(nl.n2p(4), color=INK)), run_time=0.4)
            b.line(2)
            for g in legs:
                self.play(GrowArrow(g), run_time=0.8)
            dist = M(r"\text{distance} = 4 + 4 + 4 = 12", 44, SECANT).shift(DOWN * 2.4)
            disp.next_to(dist, UP, buff=0.3)
            self.play(Write(disp), Write(dist), run_time=1.4)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(M(r"x \to v \to a", 50), T(r"sign of $v$: direction", 38), T(r"$|v|$: speed", 38), T(r"$v$ and $a$ agree: speeding up", 38)).arrange(DOWN, buff=0.4)
            self.play(FadeIn(formula_box(card, DERIV)), run_time=1.2)
        self.clear()

        self.examples_card()
        self.example("Example 1: When is it moving left?", r"$x(t) = t^3 - 6t^2 + 9t$ for $t \ge 0$. When is the particle at rest? When is it moving left?",
                     [r"v(t) = 3t^2 - 12t + 9 = 3(t - 1)(t - 3)", r"v(t) = 0 \text{ at } t = 1 \text{ and } t = 3", r"v(t) < 0 \text{ for } 1 < t < 3:\ \text{moving left}"],
                     at=[1, 2, 3])
        self.example("Example 2: Speeding up or slowing down?",
                     r"For $x(t) = t^3 - 6t^2 + 9t$, is the particle speeding up or slowing down at $t = 1.5$? At $t = 2.5$?",
                     [r"t = 1.5:\ \ v = -2.25,\ \ a = 6(1.5) - 12 = -3,\ \text{so}\ \text{speeding up}",
                      r"t = 2.5:\ \ v = -2.25,\ \ a = 6(2.5) - 12 = 3,\ \text{so}\ \text{slowing down}"], at=[1, 2])
        self.example("Example 3: Total distance", r"For $x(t) = t^3 - 6t^2 + 9t$, find the total distance traveled from $t = 0$ to $t = 4$.",
                     [r"\text{turning points: } t = 1,\ 3", r"x(0) = 0,\ x(1) = 4,\ x(3) = 0,\ x(4) = 4",
                      r"|4 - 0| + |0 - 4| + |4 - 0| = 12", r"\text{displacement: } x(4) - x(0) = 4"], at=[1, 1, 2, 3])
        self.finish()
