"""Topic 10.3 (BC): The nth term test for divergence. Narration comes from transcripts/10_3.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "10.3"

    def construct(self):
        with self.beat("A pile that never stops growing") as b:
            floor = Line(LEFT * 3, RIGHT * 3, color=DIM, stroke_width=4).shift(DOWN * 3)
            self.play(Create(floor), run_time=0.5)
            y = floor.get_y()
            blocks = VGroup()
            for k in range(1, 10):
                h = 0.55 * (k / (2 * k - 1)) * 0.9 + 0.05
                blk = Rectangle(width=2.2, height=h, stroke_color=WOOD, stroke_width=2, fill_color=CARD, fill_opacity=1).move_to([0, y + h / 2, 0])
                y += h
                blocks.add(blk)
                self.play(FadeIn(blk, shift=DOWN * 0.3), run_time=0.25)
            b.line(1)
            self.play(FadeIn(T("pieces approach half a block, not zero", 30, SECANT).to_edge(RIGHT, buff=0.5)), run_time=0.8)
            b.line(2)
        self.clear()
        self.title()

        with self.beat("The test") as b:
            box = formula_box(M(r"\lim_{n\to\infty} a_n \ne 0 \ \text{(or DNE)} \ \Longrightarrow\ \sum a_n \text{ diverges}", 40, ACCUM).set_max_width(11), ACCUM).to_edge(UP, buff=0.6)
            self.play(FadeIn(box), run_time=1)
            b.line(1)
            why = M(r"\sum a_n = S \ \text{ means } \ a_n = S_n - S_{n-1} \to S - S = 0", 38).next_to(box, DOWN, buff=0.6)
            self.play(Write(why), run_time=1.2)
            b.line(2)
            warn = T("If $\\lim a_n = 0$, the test says nothing.", 38, TANGENT).next_to(why, DOWN, buff=0.7)
            self.play(FadeIn(warn), run_time=0.8)
        self.clear()

        self.example("Using the test", r"Does $\displaystyle\sum_{n=1}^{\infty} \frac{n}{2n + 1}$ converge or diverge?",
                     [r"a_n = \frac{n}{2n + 1}", r"\lim_{n\to\infty} \frac{n}{2n + 1} = \lim \frac{1}{2 + 1/n} = \frac12", r"\tfrac12 \ne 0", r"TEXT:By the $n$th term test, the series diverges."], at=[1, 2, 3, 3], follow=True)

        with self.beat("Zero isn't enough") as b:
            def panel(f, lab, col, yr):
                ax, _ = plot_axes([0, 40, 10], yr, w=4.6, h=3, coords=False, xlabel="n", ylabel="S_n")
                s, vals = 0, []
                for k in range(1, 41):
                    s += f(k)
                    vals.append(s)
                return VGroup(ax, VGroup(*[Dot(ax.c2p(k, v), color=col, radius=0.04) for k, v in enumerate(vals, start=1)]), T(lab, 28, col).next_to(ax, DOWN, buff=0.2))
            p1 = panel(lambda k: 1 / k, r"$\sum \frac1n$: terms $\to 0$, diverges (10.5)", TANGENT, [0, 5, 1])
            p2 = panel(lambda k: 1 / k**2, r"$\sum \frac{1}{n^2}$: terms $\to 0$, converges", DERIV, [0, 2, 1])
            VGroup(p1, p2).arrange(RIGHT, buff=0.8)
            self.play(FadeIn(p1), run_time=1.2)
            b.line(1)
            self.play(FadeIn(p2), run_time=1.2)
            b.line(2)
            self.play(FadeIn(T("terms $\\to 0$: use another test", 34, SECANT).to_edge(DOWN, buff=0.4)), run_time=0.6)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(T("$\\lim a_n \\ne 0$ or does not exist: $\\sum a_n$ diverges", 38, ACCUM), T("$\\lim a_n = 0$: inconclusive", 38, TANGENT), T("check it first; it's quick", 34, DIM)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: An oscillating series", r"Does $\sum (-1)^n$ converge?", [r"a_n = (-1)^n: \ -1, 1, -1, \ldots", r"\lim a_n \text{ does not exist: diverges}"], at=[1, 1])
        self.example("Example 2: A limit that's e", r"Does $\displaystyle\sum_{n=1}^{\infty} \left(1 + \frac1n\right)^n$ converge?", [r"\lim_{n\to\infty} \left(1 + \tfrac1n\right)^n = e \ne 0", r"\text{diverges}"], at=[1, 1])
        self.example("Example 3: When the test is silent", r"What does the $n$th term test say about $\displaystyle\sum_{n=1}^{\infty} \frac{1}{\sqrt n}$?",
                     [r"\lim \frac{1}{\sqrt n} = 0", r"TEXT:The test is inconclusive.", r"\text{(it diverges: a } p\text{-series with } p = \tfrac12\text{, topic 10.5)}"], at=[1, 2, 3])
        self.finish()
