"""Topic 4.3: Rates of change in other contexts. Narration comes from transcripts/4_3.md."""
import numpy as np
from manim import *

from kit import *
from style import *
from props import Tank, cash_register, petri_dish, thermometer


def panel(title, icon):
    box = RoundedRectangle(width=3.6, height=2.6, corner_radius=0.15, color=DIM, fill_color=PANEL, fill_opacity=1)
    icon.set_max_height(1.45).set_max_width(2.6)
    return Group(box, icon.move_to(box.get_center() + UP * 0.32), T(title, 28, SECANT).move_to(box.get_bottom() + UP * 0.38))


class Lesson(TranscriptScene):
    NUM = "4.3"

    def panels(self):
        return Group(panel("bacteria per hour", petri_dish()), panel("dollars per item", cash_register()),
                     panel("degrees per minute", thermometer())).arrange(RIGHT, buff=0.5)

    def construct(self):
        ps = self.panels()
        with self.beat("Rates everywhere") as b:
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in ps], lag_ratio=0.3), run_time=1.8)
            b.line(1)
            self.play(*[Indicate(p[2], color=SECANT) for p in ps], run_time=1)
        self.clear()
        self.title()

        ax, al = plot_axes([0, 10, 2], [0, 12, 4], w=7.4, h=5, coords=False, xlabel="t", ylabel="P")
        VGroup(ax, al).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        P = lambda s: 12 * (1 - np.exp(-0.25 * s)) + 0.4
        dP = lambda s: 3 * np.exp(-0.25 * s)
        with self.beat("The rate of the rate") as b:
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(P, x_range=[0, 10], color=FUNC, stroke_width=5)), run_time=1.4)
            l1 = M(r"P' > 0:\ \text{growing}", 40, DERIV).to_edge(RIGHT, buff=0.6).shift(UP * 1.6)
            self.play(FadeIn(l1), run_time=0.6)
            b.line(1)
            for s in (1, 4, 8):
                self.play(Create(tangent_line(ax, P, s, dP(s), [s - 1, s + 1])), run_time=0.6)
            b.line(2)
            l2 = M(r"P'' < 0:\ \text{growing more slowly}", 36, TANGENT).next_to(l1, DOWN, buff=0.5).to_edge(RIGHT, buff=0.4)
            self.play(FadeIn(l2), run_time=0.8)
        self.clear()

        with self.beat("Rate in, rate out") as b:
            tk = Tank(0.45, width=2.6, height=3.0, inlet=True).shift(LEFT * 3.3 + DOWN * 0.7)
            lvl = tk.level
            inflow = M("R(t)", 36, DERIV).next_to(tk.faucet, UP, buff=0.35).shift(LEFT * 0.9)
            out = M("D(t)", 36, TANGENT).next_to(tk.mouth, RIGHT, buff=0.25).shift(UP * 0.1)
            self.play(FadeIn(tk), run_time=0.8)
            tk.pour_on().drain_on()
            self.play(FadeIn(inflow), FadeIn(out), run_time=1)
            b.line(1)
            eq = M(r"A'(t) = R(t) - D(t)", 56).to_edge(RIGHT, buff=0.8).shift(UP * 1.4)
            self.play(Write(eq), run_time=1.2)
            b.line(2)
            up = M(r"R > D:\ \text{increasing}", 40, DERIV).next_to(eq, DOWN, buff=0.6)
            dn = M(r"R < D:\ \text{decreasing}", 40, TANGENT).next_to(up, DOWN, buff=0.4)
            tk.pour_on(1.4).drain_on(0.5)
            self.play(FadeIn(up), lvl.animate.set_value(0.8), run_time=2.4)
            tk.pour_on(0.35).drain_on(2.0)
            self.play(FadeIn(dn), lvl.animate.set_value(0.3), run_time=2.4)
        self.clear()

        ax, al = plot_axes([0, 200, 50], [0, 6000, 2000], w=7.2, h=4.8, coords=False, xlabel="x", ylabel="C")
        VGroup(ax, al).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        C = lambda q: 1000 + 30 * q - 0.05 * q * q
        with self.beat("Marginal cost") as b:
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(C, x_range=[0, 200], color=FUNC, stroke_width=5)), run_time=1.2)
            b.line(1)
            self.play(Create(tangent_line(ax, C, 100, 20, [60, 140])), FadeIn(closed_dot(ax, 100, C(100), INK)), run_time=1)
            lab = M(r"C'(100) = 20 \ \text{dollars per item}", 40, TANGENT).to_edge(RIGHT, buff=0.5).shift(UP * 1.6)
            self.play(Write(lab), run_time=1)
            b.line(2)
            est = M(r"C(101) - C(100) \approx C'(100)", 40, SECANT).next_to(lab, DOWN, buff=0.5)
            self.play(Write(est), run_time=1)
        self.clear()

        with self.beat("Close") as b:
            ps = self.panels().shift(UP * 0.6)
            ders = VGroup(M(r"B'(t)", 40), M(r"C'(x)", 40), M(r"H'(t)", 40))
            for d, p in zip(ders, ps):
                d.next_to(p, DOWN, buff=0.3)
            self.play(FadeIn(ps), FadeIn(ders), run_time=1.2)
        self.clear()

        self.examples_card()
        self.example("Example 1: A fish population",
                     r"A lake has $P(t) = 1200 + 80t - 2t^2$ fish after $t$ months. Find $P'(5)$ and $P''(5)$, and interpret each.",
                     [r"P'(t) = 80 - 4t, \quad P'(5) = 60", r"TEXT:At 5 months, the fish population is increasing at 60 fish per month.",
                      r"P''(t) = -4", r"TEXT:The growth rate is decreasing by 4 fish per month, each month: growing, but more slowly."], at=[1, 2, 3, 3])
        self.example("Example 2: In and out of a tank",
                     r"Water flows into a tank at $R(t) = 20 + 4t$ gal/min and drains at $D(t) = 3t^2$ gal/min. Is the amount of water increasing or decreasing at $t = 3$? At $t = 4$?",
                     [r"t = 3:\ \ R(3) - D(3) = 32 - 27 = 5 > 0,\ \text{so}\ \text{increasing at 5 gal/min}",
                      r"t = 4:\ \ R(4) - D(4) = 36 - 48 = -12 < 0", r",\ \text{so}\ \text{decreasing at 12 gal/min}"], at=[1, 2, 3])
        self.example("Example 3: Marginal profit",
                     r"Revenue $R(x) = 40x - 0.02x^2$ and cost $C(x) = 12x + 3000$ dollars for $x$ items. Find $P'(500)$, and the $x$ where $P'(x) = 0$.",
                     [r"P(x) = R(x) - C(x) = 28x - 0.02x^2 - 3000", r"P'(x) = 28 - 0.04x", r"P'(500) = 8 \ \text{dollars per item}", r"P'(x) = 0 \ \text{at}\ x = 700"],
                     at=[1, 1, 2, 3])
        self.finish()
