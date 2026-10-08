"""Topic 7.9 (BC): Logistic models. Narration comes from transcripts/7_9.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "7.9"

    def construct(self):
        L, k = 10, 0.9
        P = lambda t, P0=0.4: L / (1 + (L - P0) / P0 * np.exp(-k * t))
        ax, al = plot_axes([0, 10, 2], [0, 12, 2], w=7, h=4.8, xlabel="t", ylabel="P")
        VGroup(ax, al).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        with self.beat("Growth that levels off") as b:
            self.play(FadeIn(T("BC only", 28, DIM).to_corner(UR, buff=0.4)), FadeIn(ax), FadeIn(al), run_time=0.6)
            self.play(Create(ax.plot(P, x_range=[0, 10], color=FUNC, stroke_width=5)), run_time=2)
            b.line(1)
            cap = DashedLine(ax.c2p(0, L), ax.c2p(10, L), color=SECANT)
            self.play(Create(cap), FadeIn(T("carrying capacity $L$", 28, SECANT).next_to(ax.c2p(5, L), UP, buff=0.12)), run_time=0.8)
            b.line(2)
            self.play(Write(M(r"\frac{dP}{dt} = kP\left(1 - \frac PL\right)", 44, ACCUM).to_edge(RIGHT, buff=0.6).shift(UP * 0.6)), run_time=1.2)
        self.clear()
        self.title()

        with self.beat("Reading the equation") as b:
            de = M(r"\frac{dP}{dt} = kP\left(1 - \frac PL\right)", 48, ACCUM).to_edge(UP, buff=0.5)
            self.play(Write(de), run_time=1)
            rows = VGroup(T(r"$P$ small: $1 - \frac PL \approx 1$, so $\frac{dP}{dt} \approx kP$ (nearly exponential)", 32),
                          T(r"$0 < P < L$: $\frac{dP}{dt} > 0$ (growing)", 32, DERIV), T(r"$P > L$: $\frac{dP}{dt} < 0$ (shrinking toward $L$)", 32, TANGENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(de, DOWN, buff=0.5)
            self.play(FadeIn(rows[0]), run_time=0.8)
            b.line(1)
            self.play(FadeIn(rows[1]), run_time=0.6)
            self.play(FadeIn(rows[2]), run_time=0.6)
            b.line(2)
            lim = M(r"P = 0, \ P = L: \text{ equilibria}; \qquad P(0) > 0: \ \lim_{t\to\infty} P(t) = L", 40, SECANT).next_to(rows, DOWN, buff=0.6)
            lim.set_max_width(13)
            self.play(Write(lim), run_time=1.2)
        self.clear()

        pa, pl = plot_axes([0, 10, 5], [0, 3, 1], w=6, h=4, xlabel="P", ylabel=r"\frac{dP}{dt}")
        VGroup(pa, pl).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        with self.beat("Fastest growth at half the capacity") as b:
            self.play(FadeIn(pa), FadeIn(pl), FadeIn(M(r"\frac{dP}{dt} = kP - \frac kLP^2", 40, ACCUM).to_edge(RIGHT, buff=0.6).shift(UP * 2)), run_time=1)
            b.line(1)
            self.play(Create(pa.plot(lambda p: k * p * (1 - p / L), x_range=[0, 10], color=FUNC, stroke_width=5)), run_time=1.2)
            b.line(2)
            v = Dot(pa.c2p(5, k * 5 * 0.5), color=SECANT)
            self.play(FadeIn(v), FadeIn(T(r"fastest at $P = \frac L2$", 30, SECANT).next_to(v, UP, buff=0.15)), Create(DashedLine(pa.c2p(5, 0), pa.c2p(5, k * 2.5), color=DIM)), run_time=1)
            sa, _ = plot_axes([0, 10, 2], [0, 12, 2], w=4, h=3, coords=False)
            s_curve = VGroup(sa, sa.plot(P, x_range=[0, 10], color=FUNC, stroke_width=4), Dot(sa.c2p(np.log(24) / k, 5), color=SECANT),
                             T("inflection at $P = \\frac L2$", 26, SECANT)).to_edge(RIGHT, buff=0.6).shift(DOWN * 1.2)
            s_curve[3].next_to(sa, DOWN, buff=0.15)
            self.play(FadeIn(s_curve), run_time=1)
        self.clear()

        self.example("Using the model", r"$\dfrac{dP}{dt} = 0.4P\left(1 - \dfrac{P}{1000}\right)$, $P(0) = 100$. (a) Find $\lim_{t\to\infty} P(t)$. (b) For what $P$ is it growing fastest? (c) Concave up or down at $P = 300$?",
                     [r"\text{(a) } L = 1000, \ P(0) > 0: \ \lim_{t\to\infty} P(t) = 1000", r"\text{(b) } P = \frac L2 = 500", r"\text{(c) } 300 < 500: \ \text{growth still speeding up, concave up}"], at=[1, 2, 3], follow=True)

        with self.beat("Close") as b:
            card = VGroup(M(r"\frac{dP}{dt} = kP\left(1 - \frac PL\right): \ L \text{ is the carrying capacity}", 40, ACCUM), M(r"P(0) > 0: \ \lim P = L", 40),
                          T(r"Fastest growth (inflection point) at $P = \frac L2$.", 36), M(r"P = \frac{L}{1 + Ae^{-kt}}", 42, SECANT)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Find L first", r"$\dfrac{dP}{dt} = 0.002P(500 - P)$. Find the carrying capacity and the population at which it grows fastest.",
                     [r"0.002P(500 - P) = 0.002 \cdot 500 \cdot P\left(1 - \frac{P}{500}\right) = P\left(1 - \frac{P}{500}\right)", r"k = 1, \ \ L = 500", r"\text{fastest at } P = 250"], at=[1, 2, 3])
        self.example("Example 2: The solution formula", r"The solution of $\dfrac{dP}{dt} = kP\left(1 - \dfrac PL\right)$ is $P = \dfrac{L}{1 + Ae^{-kt}}$. For $L = 1000$, $k = 0.4$, $P(0) = 100$, find $A$ and $P(5)$.",
                     [r"P(0) = \frac{1000}{1 + A} = 100", r"1 + A = 10, \ \ A = 9", r"P(5) = \frac{1000}{1 + 9e^{-2}} \approx 450.9"], at=[1, 2, 3])
        self.finish()
