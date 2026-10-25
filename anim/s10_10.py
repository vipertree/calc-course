"""Topic 10.10 (BC): Alternating series error bound. Narration comes from transcripts/10_10.md."""
import numpy as np
from manim import *

from kit import *
from props import Frog
from style import *


class Lesson(TranscriptScene):
    NUM = "10.10"

    def construct(self):
        with self.beat("How far off is a partial sum?") as b:
            # Adder (2026-10-14): bring back 10.7's animated frog (props.Frog), with its trail
            line = NumberLine(x_range=[0, 1.1, 0.25], length=11, include_numbers=True, numbers_to_include=[0, 0.5, 1], decimal_number_config={"num_decimal_places": 1}, font_size=24, color=DIM).shift(DOWN * 1.6)
            frog = Frog(line.n2p(0), height=0.85)
            self.add(frog.trail)
            self.play(Create(line), FadeIn(frog), run_time=0.8)
            target, sums, s = np.log(2), [], 0.0
            for k in range(1, 6):
                s += (-1)**(k + 1) / k
                sums.append(s)
            hop_col = lambda k: DERIV if k % 2 else FUNC          # 10.7's colors: rightward hops, leftward hops
            for k in range(1, 5):
                d = abs(line.n2p(sums[k - 1])[0] - frog.feet[0])
                frog.hop(self, line.n2p(sums[k - 1]), run_time=1.8, peak=min(max(d / 3, 1.0), 2.6), color=hop_col(k), trail_opacity=0.8)
            p4, pS, p5 = line.n2p(sums[3]), line.n2p(target), line.n2p(sums[4])
            y1, y2 = line.get_center()[1] - 0.4, line.get_center()[1] - 0.8
            lab4 = M("S_4", 30, SECANT).move_to([p4[0], y2 - 0.45, 0])
            self.play(FadeIn(lab4), run_time=0.6)
            b.line(1)
            sline = DashedLine(pS + UP * 0.7, [pS[0], y2 - 0.15, 0], color=ACCUM)
            labS = M("S", 30, ACCUM).move_to([pS[0], y2 - 0.45, 0])
            err = Line([p4[0], y1, 0], [pS[0], y1, 0], color=TANGENT, stroke_width=9)
            err_lab = T("error", 28, TANGENT).next_to(err, RIGHT, buff=0.25)
            self.play(Create(sline), FadeIn(labS), run_time=0.8)
            self.play(Create(err), FadeIn(err_lab), run_time=0.8)
            b.line(2)
            frog.hop(self, p5, run_time=1.8, peak=1.0, color=hop_col(5), trail_opacity=0.8)
            jump = Line([p4[0], y2, 0], [p5[0], y2, 0], color=DERIV, stroke_width=9)
            jump_lab = M("b_5", 30, DERIV).next_to(jump, RIGHT, buff=0.25)
            self.play(Create(jump), FadeIn(jump_lab), run_time=0.8)
            b.line(3)
            self.play(FadeIn(T("the next jump always overshoots the target", 32).to_edge(UP, buff=0.5)), Indicate(err, color=TANGENT), run_time=1.0)
        self.clear()
        self.title()

        with self.beat("The error bound") as b:
            box = formula_box(VGroup(T("If $\\sum (-1)^{n+1}b_n$ passes the AST and has sum $S$:", 34), M(r"|S - S_n| \le b_{n+1}", 50, ACCUM)).arrange(DOWN, buff=0.3), ACCUM).to_edge(UP, buff=0.6)
            self.play(FadeIn(box), run_time=1)
            b.line(1)
            words = T("the error is at most the first term you left out", 34).next_to(box, DOWN, buff=0.5)
            self.play(FadeIn(words), run_time=0.8)
            b.line(2)
            self.play(FadeIn(T("$S$ is between $S_n$ and $S_{n+1}$: the error has the sign of the first omitted term", 30, SECANT).next_to(words, DOWN, buff=0.5)), run_time=0.8)
        self.clear()

        # the error bound stays up in the corner through the worked examples (Adder: formulas stay on screen)
        self.example_ref = r"\begin{aligned}&\text{passes the AST:}\\ &|S - S_n| \le b_{n+1}\\ &\text{(first omitted term)}\end{aligned}"
        self.example("Bounding an error", r"Use $S_4$ to approximate $\displaystyle\sum_{n=1}^{\infty} \frac{(-1)^{n+1}}{n^2}$. Bound the error, and say whether $S_4$ is an overestimate or an underestimate.",
                     [r"TEXT:The series passes the AST: $\frac{1}{n^2}$ decreases to $0$.", r"S_4 = 1 - \tfrac14 + \tfrac19 - \tfrac{1}{16}", r"= \tfrac{115}{144} \approx 0.7986", r"\text{error} \le b_5 = \tfrac{1}{25} = 0.04",
                      r"TEXT:The first omitted term, $+\frac{1}{25}$, is positive: $S_4$ is an underestimate.", r"\text{(true sum } \tfrac{\pi^2}{12} \approx 0.8225)"], at=[1, 2, 2, 3, 4, 5], follow=True)

        with self.beat("Close") as b:
            card = VGroup(M(r"|S - S_n| \le b_{n+1}", 48, ACCUM), T("$S$ is between $S_n$ and $S_{n+1}$", 34), T("first omitted term positive: $S_n$ underestimates; negative: overestimates", 32, SECANT), T("check the AST conditions first", 32, DIM)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: How many terms?", r"How many terms of $\sum \frac{(-1)^{n+1}}{n}$ are needed to guarantee an error less than $0.001$?",
                     [r"\text{error after } n \text{ terms} \le \tfrac{1}{n + 1}", r"\tfrac{1}{n + 1} < 0.001", r"n + 1 > 1000: \ n \ge 1000"], at=[1, 1, 2])
        self.example("Example 2: Approximating 1/e", r"$\frac1e = \sum_{n=0}^\infty \frac{(-1)^n}{n!}$. Approximate $\frac1e$ with the terms through $n = 4$ and bound the error.",
                     [r"1 - 1 + \tfrac12 - \tfrac16 + \tfrac{1}{24} = \tfrac38 = 0.375", r"\text{error} \le \tfrac{1}{5!} = \tfrac{1}{120} \approx 0.0083", r"\text{(} \tfrac1e \approx 0.3679\text{)}"], at=[1, 2, 3])
        self.example("Example 3: A sine estimate", r"$\sin(0.5) = 0.5 - \frac{0.5^3}{3!} + \frac{0.5^5}{5!} - \cdots$. Estimate $\sin(0.5)$ with two terms and bound the error.",
                     [r"0.5 - \tfrac{0.125}{6} \approx 0.47917", r"\text{error} \le \tfrac{0.5^5}{120} \approx 0.00026", r"TEXT:The omitted term is positive, so the estimate is low."], at=[1, 2, 2])
        self.finish()
