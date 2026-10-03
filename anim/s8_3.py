"""Topic 8.3: Accumulation in applied contexts. Narration comes from transcripts/8_3.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "8.3"

    def construct(self):
        with self.beat("In and out") as b:
            tank, water = water_tank(2.6, 3.4)
            tank.shift(LEFT * 2.4)
            drain = Line(tank[0].get_corner(DR) + LEFT * 0.4, tank[0].get_corner(DR) + LEFT * 0.4 + DOWN * 0.6, color=DIM, stroke_width=8)
            level = ValueTracker(0.3)
            w = always_redraw(lambda: water(level.get_value()).move_to(tank[0], aligned_edge=DOWN).shift(UP * 0.04))
            tin = T("in: $E(t)$ liters per hour", 28, ACCUM).next_to(tank[1], UP, buff=0.15)
            tout = T("out: $D(t)$ liters per hour", 28, TANGENT).next_to(drain, DOWN, buff=0.15)
            self.add(w)
            self.play(FadeIn(tank), FadeIn(drain), FadeIn(tin), FadeIn(tout), run_time=1)
            gauge = always_redraw(lambda: M(rf"A(t) = {int(20 + 160 * level.get_value())}\ \text{{L}}", 40, FUNC).to_edge(RIGHT, buff=1.2))
            self.add(gauge)
            self.play(level.animate.set_value(0.8), run_time=2.4)
            b.line(1)
            self.play(level.animate.set_value(0.5), run_time=2)
            b.line(2)
        self.clear()
        self.title()

        with self.beat("Amount equals start plus net change") as b:
            r1 = VGroup(M(r"A'(t) = E(t) - D(t)", 48), T("rate in minus rate out", 30, DIM)).arrange(DOWN, buff=0.15).shift(UP * 1.8)
            self.play(Write(r1), run_time=1)
            b.line(1)
            r2 = VGroup(M(r"A(t) = A(0) + \int_0^t \big(E(u) - D(u)\big)\,du", 48, ACCUM), T("start + net change", 30, DIM)).arrange(DOWN, buff=0.15)
            self.play(Write(r2), run_time=1.2)
            b.line(2)
            r3 = T("what you had, plus what came in, minus what went out", 34, FUNC).shift(DOWN * 2)
            self.play(FadeIn(r3), run_time=0.8)
        self.clear()

        with self.beat("Units of an integral") as b:
            u = M(r"\underbrace{E(t)}_{\text{liters/hour}}\ \cdot\ \underbrace{dt}_{\text{hours}} \ \longrightarrow\ \underbrace{\int E(t)\,dt}_{\text{liters}}", 48).shift(UP * 1.6)
            self.play(Write(u), run_time=1.4)
            b.line(1)
            what = T("what accumulates", 28, ACCUM)
            how = T("a total", 28, FUNC)
            when = T("over which interval", 28, SECANT)
            VGroup(how, what, when).arrange(RIGHT, buff=0.9).shift(DOWN * 0.2)
            self.play(FadeIn(VGroup(how, what, when)), run_time=0.8)
            b.line(2)
            s = Tex(r"$\int_2^5 E(t)\,dt$ is the ", "total", " number of ", r"liters that flow in\ ", "from $t = 2$ to $t = 5$ hours", ".", font_size=34, color=INK).shift(DOWN * 1.6)
            s[1].set_color(FUNC)
            s[3].set_color(ACCUM)
            s[4].set_color(SECANT)
            self.play(FadeIn(s), run_time=1)
        self.clear()

        with self.beat("When is the amount greatest?") as b:
            E = lambda s: 3 + 0.2 * s
            D = lambda s: 0.5 + 0.12 * s**2
            c = (0.2 + np.sqrt(0.04 + 4 * 0.12 * 2.5)) / (2 * 0.12)
            ax, al = plot_axes([0, 8, 1], [0, 8, 2], w=6, h=3.6, coords=False, xlabel="t", ylabel="")
            VGroup(ax, al).to_edge(LEFT, buff=0.5).shift(UP * 0.5)
            ge = ax.plot(E, x_range=[0, 7.5], color=ACCUM, stroke_width=4)
            gd = ax.plot(D, x_range=[0, 7.5], color=TANGENT, stroke_width=4)
            self.play(FadeIn(ax), FadeIn(al), Create(ge), Create(gd), FadeIn(M("E", 32, ACCUM).next_to(ax.c2p(7.5, E(7.5)), RIGHT, buff=0.1)),
                      FadeIn(M("D", 32, TANGENT).next_to(ax.c2p(6.9, D(6.9)), LEFT, buff=0.1)), run_time=1.2)
            self.play(FadeIn(region(ax, E, D, 0, c, color=GRASS, opacity=0.4)), FadeIn(region(ax, D, E, c, 7.5, color=TANGENT, opacity=0.3)), run_time=1)
            b.line(1)
            ch = sign_chart(["c"], ["+", "-"], name="A'", width=5.4, size=38, words=["rising", "falling"]).to_edge(RIGHT, buff=0.5).shift(UP * 1)
            self.play(FadeIn(ch), run_time=1)
            self.play(FadeIn(T("max", 30, SECANT).next_to(ch, UP, buff=0.15)), run_time=0.6)
            b.line(2)
            cand = VGroup(T("candidates:", 30, DIM), M(r"t = 0, \ \ t = c, \ \ \text{right endpoint}", 36)).arrange(DOWN, buff=0.15).next_to(ch, DOWN, buff=0.8)
            self.play(FadeIn(cand), run_time=0.8)
        self.clear()

        ch = staged_chart([4], ["+", "-"], words=["rising", "falling"], name="A'", width=5.5)
        self.example("Water in a tank", r"Water flows into a tank at $E(t) = 8 + 2t$ liters per hour and drains at $D(t) = t^2$ liters per hour, $0 \le t \le 6$. The tank holds $50$ liters at $t = 0$. "
                     r"(a) Is the amount increasing or decreasing at $t = 5$? (b) How much water is in the tank at $t = 6$? (c) When is the amount greatest, and what is it?",
                     [r"\text{(a) } A'(5) = E(5) - D(5) = 18 - 25 = -7 < 0", r"\text{TEXT:decreasing at } t = 5", r"\text{(b) } A(6) = 50 + \int_0^6 \left(8 + 2t - t^2\right) dt",
                      r"= 50 + \left[8t + t^2 - \tfrac{t^3}{3}\right]_0^6", r"= 50 + (48 + 36 - 72)", r"= 62 \text{ liters}",
                      r"\text{(c) } 8 + 2t - t^2 = 0", r"t^2 - 2t - 8 = 0", r"(t - 4)(t + 2) = 0", r"t = 4 \ \ (t = -2 \text{ is outside})",
                      r"A'(1) = 8 + 2 - 1 = 9 > 0", r"A'(5) = -7 < 0", r"A(0) = 50, \ \ A(4) = \tfrac{230}{3} \approx 76.7, \ \ A(6) = 62", r"\text{greatest: } \tfrac{230}{3} \text{ liters at } t = 4"],
                     at=[1, 1, 2, 3, 3, 3, 4, 4, 5, 5, 6, 6, 7, 8], figure=ch, figure_at=5,
                     cues={10: reveal_sign(ch, 0), 11: lambda sc: (reveal_sign(ch, 1)(sc), reveal_words(ch)(sc)), 13: mark_point(ch, 0, "max")})

        with self.beat("Close") as b:
            card = VGroup(M(r"A(t) = A(0) + \int_0^t (\text{rate in} - \text{rate out})", 42, ACCUM), T("units: rate units $\\times$ time units", 34),
                          T("greatest: where rate in $-$ rate out changes from $+$ to $-$,", 34, SECANT), T("checked against the endpoints", 34, SECANT)).arrange(DOWN, buff=0.4)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Interpret in context", r"Oil leaks from a tanker at $R(t)$ gallons per hour, $t$ in hours. Interpret (a) $\int_2^5 R(t)\,dt = 140$ and (b) $R'(3) = -4$, with units.",
                     [r"\text{TEXT:(a) A total of } 140 \text{ gallons leak from } t = 2 \text{ to } t = 5 \text{ hours.}",
                      r"\text{TEXT:(b) At } t = 3 \text{ hours, the leak rate is decreasing at } 4 \text{ gallons per hour per hour.}"], at=[1, 2])
        tab = table(["t", "0", "2", "5", "8"], [["P'(t)", "30", "40", "25", "10"]], size=34)
        self.example("Example 2: From a table of rates", VGroup(T(r"A town has $1200$ people at $t = 0$ (years). Use a trapezoidal sum to approximate $P(8)$.", 38), tab).arrange(DOWN, buff=0.3),
                     [r"\int_0^8 P'(t)\,dt \approx 2\cdot\tfrac{30 + 40}{2} + 3\cdot\tfrac{40 + 25}{2} + 3\cdot\tfrac{25 + 10}{2}", r"= 70 + 97.5 + 52.5", r"= 220",
                      r"P(8) \approx 1200 + 220 = 1420 \text{ people}"], at=[1, 1, 2, 3],
                     text=r"A town's population changes at $P'(t) = 30, 40, 25, 10$ people per year at $t = 0, 2, 5, 8$ years, and $P(0) = 1200$. Use a trapezoidal sum to approximate $P(8)$.")
        ch3 = staged_chart([4], ["+", "-"], words=["warming", "cooling"], name="H'", width=5)
        self.example("Example 3: The warmest moment", r"A room's temperature changes at $H'(t) = 4 - t$ degrees per minute for $0 \le t \le 6$, and $H(0) = 60$. Find the maximum temperature and when it occurs.",
                     [r"4 - t = 0, \ \ t = 4", r"H(4) = 60 + \int_0^4 (4 - t)\,dt = 60 + 8 = 68", r"H(6) = 60 + (24 - 18) = 66", r"\text{maximum } 68^\circ \text{ at } t = 4 \text{ minutes}"],
                     at=[1, 2, 2, 3], figure=ch3, figure_at=1, cues={1: lambda sc: (reveal_sign(ch3, 0, 1)(sc), reveal_words(ch3)(sc))})
        self.finish()
