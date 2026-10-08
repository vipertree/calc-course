"""Topic 10.8 (BC): The ratio test. Narration comes from transcripts/10_8.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "10.8"

    def construct(self):
        with self.beat("Behaving like a geometric series") as b:
            top = M(r"\tfrac13,\ \tfrac19,\ \tfrac{1}{27},\ \tfrac{1}{81},\ \ldots \quad (\text{ratio } \tfrac13)", 40, DERIV).shift(UP * 1.6)
            self.play(Write(top), run_time=1)
            b.line(1)
            bot = M(r"\tfrac13,\ \tfrac29,\ \tfrac{3}{27},\ \tfrac{4}{81},\ \tfrac{5}{243},\ \ldots", 40).shift(DOWN * 0.1)
            ratios = M(r"\text{ratios: } 0.67,\ 0.5,\ 0.44,\ 0.42,\ \ldots \to \tfrac13", 36, SECANT).next_to(bot, DOWN, buff=0.5)
            self.play(Write(bot), run_time=1)
            self.play(Write(ratios), run_time=1.2)
            b.line(2)
            self.play(FadeIn(T("ratio settles below $1$: shrinks like a convergent geometric series", 30, ACCUM).to_edge(DOWN, buff=0.5)), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("The test") as b:
            box = formula_box(VGroup(M(r"L = \lim_{n\to\infty} \left|\frac{a_{n+1}}{a_n}\right|", 44), M(r"L < 1: \text{ converges (absolutely)}; \quad L > 1: \text{ diverges}; \quad L = 1: \text{ inconclusive}", 32)).arrange(DOWN, buff=0.3), ACCUM).to_edge(UP, buff=0.6)
            self.play(FadeIn(box[0]), FadeIn(box[1][0]), run_time=1)
            b.line(1)
            self.play(FadeIn(box[1][1]), run_time=1)
            b.line(2)
            line = NumberLine(x_range=[0, 2, 1], length=8, include_numbers=True, font_size=28, color=DIM).shift(DOWN * 1.8)
            self.play(Create(line), Create(Line(line.n2p(0), line.n2p(1), color=DERIV, stroke_width=10)), Create(Line(line.n2p(1), line.n2p(2), color=TANGENT, stroke_width=10)),
                      FadeIn(M("?", 40, DIM).next_to(line.n2p(1), UP, buff=0.3)), FadeIn(T("converges", 28, DERIV).next_to(line.n2p(0.5), UP, buff=0.3)), FadeIn(T("diverges", 28, TANGENT).next_to(line.n2p(1.5), UP, buff=0.3)), run_time=1.2)
        self.clear()

        self.example("Using the ratio test", r"Does $\displaystyle\sum_{n=1}^{\infty} \frac{n}{3^n}$ converge?",
                     [r"a_n = \frac{n}{3^n}, \quad a_{n+1} = \frac{n + 1}{3^{n+1}}", r"\frac{a_{n+1}}{a_n} = \frac{n + 1}{3^{n+1}} \cdot \frac{3^n}{n}", r"= \frac{n + 1}{n} \cdot \frac{3^n}{3^{n+1}}", r"= \frac{n + 1}{n} \cdot \frac13",
                      r"L = \lim \frac{n + 1}{3n} = \frac13", r"\tfrac13 < 1: \ \text{converges}"], at=[1, 2, 3, 3, 4, 5])

        with self.beat("Factorials") as b:
            rows = VGroup(M(r"n! = n \cdot (n - 1) \cdots 2 \cdot 1", 44), M(r"(n + 1)! = (n + 1) \cdot n!", 44, SECANT), M(r"\frac{(n + 1)!}{n!} = n + 1, \qquad \frac{n!}{(n + 1)!} = \frac{1}{n + 1}", 42, ACCUM),
                          T("the ratio test is the tool of choice for factorials and exponentials", 32, DIM)).arrange(DOWN, buff=0.45)
            self.play(Write(rows[0]), run_time=1)
            b.line(1)
            self.play(Write(rows[1]), run_time=1)
            self.play(Write(rows[2]), run_time=1)
            b.line(2)
            self.play(FadeIn(rows[3]), run_time=0.6)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(M(r"L = \lim \left|\tfrac{a_{n+1}}{a_n}\right|", 44, ACCUM), T("$L < 1$ converges; $L > 1$ diverges; $L = 1$ inconclusive", 36), M(r"(n + 1)! = (n + 1)\cdot n!", 40, SECANT), T("best for factorials and exponentials", 34, DIM)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: A factorial in the denominator", r"Does $\displaystyle\sum_{n=0}^{\infty} \frac{2^n}{n!}$ converge?", [r"\frac{a_{n+1}}{a_n} = \frac{2^{n+1}}{(n + 1)!} \cdot \frac{n!}{2^n} = \frac{2}{n + 1}", r"L = 0 < 1: \ \text{converges}"], at=[1, 2])
        self.example("Example 2: A factorial on top", r"Does $\displaystyle\sum_{n=1}^{\infty} \frac{n!}{10^n}$ converge?", [r"\frac{a_{n+1}}{a_n} = \frac{(n + 1)!}{10^{n+1}} \cdot \frac{10^n}{n!} = \frac{n + 1}{10}", r"L = \infty: \ \text{diverges}"], at=[1, 1])
        self.example("Example 3: When L = 1", r"What does the ratio test say about $\displaystyle\sum \frac{1}{n^2}$?", [r"\frac{a_{n+1}}{a_n} = \frac{n^2}{(n + 1)^2} \to 1", r"\text{inconclusive}", r"\text{(converges by the } p\text{-series test, } p = 2)"], at=[1, 1, 2])
        self.finish()
