"""Topic 4.1: Interpreting the meaning of the derivative in context. Narration comes from transcripts/4_1.md."""
import numpy as np
from manim import *

from kit import *
from style import *
from props import Tank, coffee_mug


class Lesson(TranscriptScene):
    NUM = "4.1"

    def construct(self):
        tk = Tank(0.72).shift(LEFT * 3.5)
        with self.beat("A number with a story") as b:
            self.play(FadeIn(tk), run_time=0.8)
            tk.drain_on()
            st = M(r"W'(5) = -3", 72).shift(RIGHT * 2.5)
            self.play(Write(st), tk.level.animate.set_value(0.66), run_time=1.6, rate_func=linear)
            b.line(1)
            self.play(Indicate(st, color=SECANT), tk.level.animate.set_value(0.6), run_time=1.6, rate_func=linear)
        self.clear()
        self.title()

        with self.beat("Units first") as b:
            tk = Tank(0.6).scale(0.8).to_edge(LEFT, buff=0.8)
            labs = VGroup(M(r"W(t):\ \text{liters}", 44, FUNC), M(r"t:\ \text{minutes}", 44, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(tk, RIGHT, buff=0.8).shift(UP * 1.2)
            self.play(FadeIn(tk), FadeIn(labs), run_time=1)
            b.line(1)
            u = M(r"\text{units of } W' = \frac{\text{liters}}{\text{minutes}} = \text{liters per minute}", 46, SECANT).next_to(labs, DOWN, buff=0.7).align_to(labs, LEFT)
            self.play(Write(u), run_time=1.4)
            b.line(2)
            more = VGroup(M(r"V(t):\ \text{gallons},\ t:\ \text{hours},\ \text{so}\ \text{gallons per hour}", 36),
                          M(r"C(n):\ \text{dollars},\ n:\ \text{items},\ \text{so}\ \text{dollars per item}", 36)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            more.next_to(u, DOWN, buff=0.6).align_to(labs, LEFT)
            self.play(FadeIn(more[0]), run_time=0.7)
            self.play(FadeIn(more[1]), run_time=0.7)
        self.clear()

        with self.beat("The sentence") as b:
            slots = [("At", None), ("$t = 5$ minutes,", SECANT), ("the amount of water in the tank", FUNC), ("is", None),
                     ("decreasing", TANGENT), ("at a rate of", None), ("$3$ liters per minute.", DERIV)]
            words = VGroup(*[T(w, 42, c or INK) for w, c in slots])
            line1 = VGroup(*words[:3]).arrange(RIGHT, buff=0.25)
            line2 = VGroup(*words[3:]).arrange(RIGHT, buff=0.25)
            VGroup(line1, line2).arrange(DOWN, buff=0.5).shift(UP * 0.6)
            boxes = VGroup(*[SurroundingRectangle(words[i], color=words[i].get_color(), buff=0.1) for i in (1, 2, 4, 6)])
            tags = VGroup(*[T(n, 28, DIM).next_to(bx, DOWN, buff=0.12) for n, bx in zip(["when", "what", "which way", "how fast"], boxes)])
            self.play(FadeIn(words[0]), FadeIn(words[3]), FadeIn(words[5]), run_time=0.8)
            for k, i in enumerate((1, 2, 4, 6)):
                b.line(k + 1)
                self.play(FadeIn(words[i]), Create(boxes[k]), FadeIn(tags[k]), run_time=0.8)
        self.clear()
        self.example("Draining a tank", r"$W(t)$ is the number of liters of water in a tank $t$ minutes after a drain opens. Interpret $W'(5) = -3$.",
                     [r"\text{when: } t = 5 \text{ minutes}", r"\text{what: the amount of water}", r"\text{which way: } -3 < 0, \text{ decreasing}",
                      r"\text{how fast: } 3 \text{ liters per minute}", r"TEXT:At $t = 5$ minutes, the amount of water in the tank is decreasing at a rate of $3$ liters per minute."], at=[1, 1, 1, 2, 3], follow=True)

        with self.beat("Three wrong readings") as b:
            bad = VGroup(T(r"``The tank holds $-3$ liters.''", 40), T(r"``Exactly $3$ liters drain over the next minute.''", 40),
                         T(r"``The derivative is $-3$.''", 40)).arrange(DOWN, buff=0.7, aligned_edge=LEFT)
            for k, m in enumerate(bad):
                b.line(k + 1)
                self.play(FadeIn(m), run_time=0.6)
                self.play(Create(Line(m.get_left(), m.get_right(), color=TANGENT, stroke_width=5)), run_time=0.5)
        self.clear()

        with self.beat("Value, average, instant") as b:
            tb = table([r"\text{expression}", r"\text{meaning}", r"\text{units}"],
                       [[r"W(5)", r"\text{the amount at } t = 5", r"\text{liters}"],
                        [r"\frac{W(8) - W(2)}{8 - 2}", r"\text{the average rate on } [2, 8]", r"\text{liters/min}"],
                        [r"W'(5)", r"\text{the rate at the instant } t = 5", r"\text{liters/min}"]], size=38, gap=0.5)
            self.play(FadeIn(tb[1]), FadeIn(tb[0][0]), run_time=0.6)
            for r in (1, 2, 3):
                self.play(FadeIn(tb[0][r], shift=RIGHT * 0.2), run_time=0.8)
        self.clear()

        with self.beat("Close") as b:
            s = T(r"At $t = 5$ minutes, the amount of water in the tank \\ is decreasing at a rate of $3$ liters per minute.", 42)
            self.play(FadeIn(s), run_time=1)
            tags = T(r"when \quad what \quad which way \quad how fast", 34, SECANT).next_to(s, DOWN, buff=0.6)
            self.play(FadeIn(tags), run_time=0.8)
        self.clear()

        self.examples_card()
        cof = table(["t", "0", "4", "10", "16"], [["H(t)", "180", "162", "141", "126"]], size=38)
        for c in (2, 3):
            cof.cells[0][c].set_color(SECANT)
            cof.cells[1][c].set_color(SECANT)
        self.example("Example 1: A cooling cup of coffee",
                     Group(T(r"Coffee's temperature $H(t)$, in $^\circ$F, $t$ minutes after pouring. Estimate $H'(7)$ and explain its meaning.", 36),
                            Group(cof, coffee_mug(1.1)).arrange(RIGHT, buff=0.8)).arrange(DOWN, buff=0.3),
                     [r"\text{closest times: } t = 4 \text{ and } t = 10", r"H'(7) \approx \frac{H(10) - H(4)}{10 - 4} = \frac{141 - 162}{6} = -3.5",
                      r"TEXT:That is the average rate on $[4, 10]$. With only table values, it is our best estimate of the instantaneous rate $H'(7)$.",
                      r"TEXT:At $t = 7$ minutes, the temperature of the coffee is decreasing at about $3.5^\circ$F per minute."], at=[1, 2, 3, 4],
                     text=r"Coffee's temperature $H(t)$, in $^\circ$F, is measured $t$ minutes after it is poured. "
                          r"\[ \begin{array}{c|cccc} t & 0 & 4 & 10 & 16 \\ \hline H(t) & 180 & 162 & 141 & 126 \end{array} \] Estimate $H'(7)$ and explain its meaning.")
        self.example("Example 2: Marginal cost",
                     r"$C(n)$ is the cost, in dollars, of making $n$ bicycles, and $C'(200) = 85$. Give the units of $C'$ and explain what $C'(200) = 85$ means.",
                     [r"\text{units: dollars per bicycle}", r"TEXT:At $n = 200$ bicycles, the cost is increasing at $\$85$ per bicycle.",
                      r"TEXT:So the 201st bicycle costs about $\$85$ to make."], at=[1, 2, 3])
        ax, _ = plot_axes([0, 4, 1], [0, 70, 20], w=4.6, h=3.6)
        fig = VGroup(ax, ax.plot(lambda s: -16 * s * s + 64 * s, x_range=[0, 4], color=FUNC, stroke_width=4),
                     tangent_line(ax, lambda s: -16 * s * s + 64 * s, 3, -32, [2.4, 3.6]), closed_dot(ax, 3, 48, INK))
        self.example("Example 3: From a formula", r"A ball's height is $h(t) = -16t^2 + 64t$ feet after $t$ seconds. Find $h'(3)$ and interpret it.",
                     [r"h'(t) = -32t + 64", r"h'(3) = -96 + 64 = -32",
                      r"TEXT:At $t = 3$ seconds, the ball's height is decreasing at $32$ feet per second."], figure=fig, at=[1, 1, 2])
        self.finish()
