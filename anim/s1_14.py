"""Topic 1.14: Connecting infinite limits and vertical asymptotes. Narration comes from transcripts/1_14.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def branch_plot(ax, f, c, xr, gap=0.12, **kw):
    return VGroup(ax.plot(f, x_range=[xr[0], c - gap], **kw), ax.plot(f, x_range=[c + gap, xr[1]], **kw))


class Lesson(TranscriptScene):
    NUM = "1.14"

    def division_bars(self):
        rows = VGroup(*[M(rf"1 \div {d} = {q}", 44) for d, q in [("0.1", "10"), ("0.01", "100"), ("0.001", "1000")]]).arrange(DOWN, buff=0.6, aligned_edge=LEFT).shift(LEFT * 3.5)
        bars = VGroup(*[Rectangle(width=0.8, height=h_, fill_color=TANGENT, fill_opacity=0.8, stroke_width=0) for h_ in (0.5, 1.8, 5.2)]).arrange(RIGHT, buff=0.4, aligned_edge=DOWN)
        bars.shift(RIGHT * 3 + DOWN * 0.2)
        return rows, bars

    def construct(self):
        rows, bars = self.division_bars()
        with self.beat("Dividing by almost nothing") as b:
            for r, bar in zip(rows, bars):
                self.play(Write(r), GrowFromEdge(bar, DOWN), run_time=1)
            b.line(1)
            self.play(Indicate(bars[-1], color=SECANT), run_time=1)
        self.clear()
        self.title()

        ax, al = plot_axes([0, 4, 1], [0, 8, 2], w=7, h=5.2)
        VGroup(ax, al).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        f = lambda x: 1 / (x - 2) ** 2
        with self.beat("Infinite limits") as b:
            self.play(FadeIn(ax), FadeIn(al), FadeIn(asymptote(ax, 2, [0, 8])), Create(branch_plot(ax, f, 2, [0, 4], gap=0.36, color=FUNC, stroke_width=5)), run_time=1.8)
            st = M(r"\lim_{x\to2}\frac{1}{(x - 2)^2} = \infty", 48, FUNC).to_edge(RIGHT, buff=0.5).shift(UP * 1.5)
            self.play(Write(st), run_time=1.2)
            b.line(1)
            note = T(r"still does not exist: \\ $\infty$ says \emph{how} it fails", 38, SECANT).next_to(st, DOWN, buff=0.6)
            self.play(FadeIn(note), run_time=0.8)
        with self.beat("Vertical asymptotes") as b:
            va = T(r"vertical asymptote $x = 2$", 34, DIM).next_to(ax.c2p(2, 8), UP, buff=0.1)
            self.play(FadeIn(va), run_time=0.8)
            b.line(1)
            self.play(FadeOut(note), FadeOut(st), run_time=0.4)
            a2, _ = plot_axes([0, 4, 1], [-6, 6, 2], w=5.2, h=4.4)
            a2.to_edge(RIGHT, buff=0.6).shift(DOWN * 0.3)
            self.play(FadeIn(a2), FadeIn(asymptote(a2, 2, [-6, 6])), Create(branch_plot(a2, lambda x: 1 / (x - 2), 2, [0, 4], gap=0.17, color=FUNC, stroke_width=4)), run_time=1.4)
        self.clear()

        with self.beat("Finding the sign") as b:
            e = M(r"\frac{x + 3}{(x - 1)(x + 2)}\quad \text{near } x = 1", 54, FUNC).to_edge(UP, buff=0.6)
            self.play(Write(e), run_time=1.2)
            nl = NumberLine(x_range=[0, 2, 1], length=8, color=DIM, include_numbers=True, font_size=30).shift(DOWN * 0.2)
            self.play(Create(nl), run_time=0.6)
            top = M(r"x + 3 \approx 4 > 0, \quad x + 2 \approx 3 > 0", 40).next_to(e, DOWN, buff=0.6)
            self.play(Write(top), run_time=1)
            b.line(1)
            sg = VGroup(M(r"x - 1 < 0", 36, SECANT).next_to(nl.n2p(0.5), DOWN, buff=0.5), M(r"x - 1 > 0", 36, TANGENT).next_to(nl.n2p(1.5), DOWN, buff=0.5))
            self.play(FadeIn(sg), run_time=0.8)
            b.line(2)
            fr = VGroup(M(r"\frac{(+)}{(-)(+)} = -", 44, SECANT).next_to(sg[0], DOWN, buff=0.35),
                        M(r"\frac{(+)}{(+)(+)} = +", 44, TANGENT).next_to(sg[1], DOWN, buff=0.35))
            self.play(Write(fr[0]), run_time=0.9)
            self.play(Write(fr[1]), run_time=0.9)
            b.line(3)
            res = VGroup(M(r"\lim_{x\to1^-}\frac{x + 3}{(x - 1)(x + 2)} = -\infty", 38, SECANT),
                         M(r"\lim_{x\to1^+}\frac{x + 3}{(x - 1)(x + 2)} = \infty", 38, TANGENT)).arrange(RIGHT, buff=0.9).to_edge(DOWN, buff=0.3)
            self.play(FadeOut(top), Write(res), run_time=1.2)
        self.clear()
        self.example("A sign chart", r"Let $f(x) = \dfrac{x + 3}{(x - 1)(x + 2)}$. Find $\displaystyle\lim_{x\to1^-} f(x)$ and $\displaystyle\lim_{x\to1^+} f(x)$.",
                     [r"\text{near } x = 1: \ x + 3 \approx 4 > 0, \quad x + 2 \approx 3 > 0", r"\text{left: } \frac{(+)}{(-)(+)} = -,\ \text{so}\ \lim_{x\to1^-} f(x) = -\infty", r"\text{right: } \frac{(+)}{(+)(+)} = +,\ \text{so}\ \lim_{x\to1^+} f(x) = \infty"], at=[1, 2, 3])

        with self.beat("Not every zero of the denominator") as b:
            e = M(r"\frac{x^2 - 1}{x - 1} = \frac{(x - 1)(x + 1)}{x - 1}", 56).shift(UP * 1.6)
            self.play(Write(e), run_time=1.4)
            a3, _ = plot_axes([-1, 3, 1], [-1, 4, 1], w=5.4, h=3.4)
            a3.shift(DOWN * 1.6)
            self.play(FadeIn(a3), Create(a3.plot(lambda x: x + 1, x_range=[-1, 3], color=FUNC, stroke_width=4)), FadeIn(open_dot(a3, 1, 2)), run_time=1.2)
            self.play(FadeIn(T("a hole, not an asymptote", 36, SECANT).next_to(a3, RIGHT, buff=0.3)), run_time=0.8)
        self.clear()

        with self.beat("Beyond rational functions") as b:
            panels = VGroup()
            a4, _ = plot_axes([0, 4, 1], [-3, 2, 1], w=3.8, h=3, coords=False)
            panels.add(VGroup(a4, a4.plot(np.log, x_range=[0.05, 4], color=FUNC), asymptote(a4, 0, [-3, 2]), M(r"\ln x", 34).next_to(a4, DOWN)))
            a5, _ = plot_axes([-3, 3, 1], [-4, 4, 1], w=3.8, h=3, coords=False)
            tp = VGroup(*[a5.plot(np.tan, x_range=[lo, hi], color=FUNC) for lo, hi in [(-3, -1.82), (-1.32, 1.32), (1.82, 3)]])
            panels.add(VGroup(a5, tp, asymptote(a5, -np.pi / 2, [-4, 4]), asymptote(a5, np.pi / 2, [-4, 4]), M(r"\tan x", 34).next_to(a5, DOWN)))
            a6, _ = plot_axes([-2, 2, 1], [0, 6, 1], w=3.8, h=3, coords=False)
            ep = VGroup(a6.plot(lambda x: np.exp(1 / x), x_range=[0.56, 2], color=FUNC), a6.plot(lambda x: np.exp(1 / x), x_range=[-2, -0.05], color=FUNC))
            panels.add(VGroup(a6, ep, asymptote(a6, 0, [0, 6]), M(r"e^{1/x}", 34).next_to(a6, DOWN)))
            panels.arrange(RIGHT, buff=0.5)
            self.play(FadeIn(panels[0]), run_time=1)
            b.line(1)
            self.play(FadeIn(panels[1]), FadeIn(panels[2]), run_time=1.2)
        self.clear()

        with self.beat("Close") as b:
            rows, bars = self.division_bars()
            self.play(FadeIn(rows), FadeIn(bars), run_time=1.2)
        self.clear()

        self.examples_card()
        self.example("Example 1: One side at a time", r"Find $\displaystyle\lim_{x\to4^-}\frac{2x + 1}{x - 4}$ and $\displaystyle\lim_{x\to4^+}\frac{2x + 1}{x - 4}$.",
                     [r"\frac{9}{0}:\ \text{unbounded}", r"2x + 1 \approx 9 > 0", r"x \to 4^-:\ \frac{(+)}{(-)} = -,\ \text{so}\ \lim_{x\to4^-}\frac{2x + 1}{x - 4} = -\infty", r"x \to 4^+:\ \frac{(+)}{(+)} = +,\ \text{so}\ \lim_{x\to4^+}\frac{2x + 1}{x - 4} = \infty"],
                     at=[1, 2, 3, 4])
        self.example("Example 2: Which zeros make asymptotes?", r"Find the vertical asymptotes of $f(x) = \dfrac{x^2 - 9}{x^2 - 2x - 3}$.",
                     [r"\text{denominator } 0 \text{ at } x = 3,\ x = -1", r"\frac{(x - 3)(x + 3)}{(x - 3)(x + 1)}", r"x = 3:\ \text{hole}; \quad x = -1:\ \text{vertical asymptote}"],
                     at=[1, 2, 3])
        self.example("Example 3: Same sign on both sides", r"Find $\displaystyle\lim_{x\to0}\frac{x - 2}{x^2}$.",
                     [r"\frac{-2}{0}", r"\text{top} < 0, \quad x^2 > 0 \text{ on both sides:}\ \ \frac{(-)}{(+)} = -", r"\lim_{x\to0}\frac{x - 2}{x^2} = -\infty"], at=[1, 2, 3])
        self.finish()
