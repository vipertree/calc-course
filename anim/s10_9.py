"""Topic 10.9 (BC): Absolute and conditional convergence. Narration comes from transcripts/10_9.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "10.9"

    def construct(self):
        with self.beat("Two kinds of convergence") as b:
            left = VGroup(M(r"1 - \tfrac14 + \tfrac19 - \tfrac{1}{16} + \cdots", 38), M(r"1 + \tfrac14 + \tfrac19 + \tfrac{1}{16} + \cdots \ \text{converges}", 32, DERIV), T("converges even without the signs", 28, DERIV)).arrange(DOWN, buff=0.35)
            right = VGroup(M(r"1 - \tfrac12 + \tfrac13 - \tfrac14 + \cdots", 38), M(r"1 + \tfrac12 + \tfrac13 + \tfrac14 + \cdots \ \text{diverges}", 32, TANGENT), T("converges only because of the signs", 28, TANGENT)).arrange(DOWN, buff=0.35)
            VGroup(left, right).arrange(RIGHT, buff=0.8)
            self.play(FadeIn(left[0]), FadeIn(right[0]), run_time=1)
            b.line(1)
            self.play(FadeIn(left[1:]), run_time=1)
            b.line(2)
            self.play(FadeIn(right[1:]), run_time=1)
        self.clear()
        self.title()

        with self.beat("Definitions") as b:
            rows = VGroup(T("absolutely convergent: $\\sum |a_n|$ converges", 36, DERIV), T("conditionally convergent: $\\sum a_n$ converges but $\\sum |a_n|$ diverges", 34, SECANT),
                          formula_box(T("If $\\sum |a_n|$ converges, then $\\sum a_n$ converges.", 36, ACCUM), ACCUM)).arrange(DOWN, buff=0.5).to_edge(UP, buff=0.6)
            self.play(FadeIn(rows[0]), run_time=0.8)
            b.line(1)
            self.play(FadeIn(rows[1]), run_time=0.8)
            b.line(2)
            boxes = VGroup(*[VGroup(RoundedRectangle(width=3.6, height=1, corner_radius=0.15, stroke_color=c, fill_color=c, fill_opacity=0.15), T(w, 28, c)) for w, c in
                             (("absolutely convergent", DERIV), ("conditionally convergent", SECANT), ("divergent", TANGENT))]).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.6)
            for bx in boxes:
                bx[1].move_to(bx[0])
            self.play(FadeIn(rows[2]), FadeIn(boxes), run_time=1.2)
        self.clear()

        with self.beat("A plan for classifying") as b:
            pre = T("first: if $a_n \\not\\to 0$, divergent ($n$th term test)", 32, TANGENT).to_edge(UP, buff=0.6)
            steps = VGroup(T("1. Test $\\sum |a_n|$ ($p$-series, comparison, ratio, integral). Converges: absolutely convergent.", 30, DERIV),
                           T("2. If $\\sum |a_n|$ diverges, test $\\sum a_n$ (usually the AST). Converges: conditionally convergent.", 30, SECANT),
                           T("3. Otherwise: divergent.", 30, TANGENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(pre, DOWN, buff=0.6)
            self.play(FadeIn(pre), run_time=0.8)
            b.line(1)
            self.play(FadeIn(steps[0]), run_time=0.8)
            b.line(2)
            self.play(FadeIn(steps[1]), FadeIn(steps[2]), run_time=1)
        self.clear()

        self.example("Three classifications", r"Classify as absolutely convergent, conditionally convergent, or divergent: (a) $\sum \frac{(-1)^n}{n^2}$ (b) $\sum \frac{(-1)^n}{n}$ (c) $\sum (-1)^n\frac{n}{n + 1}$.",
                     [r"\text{(a) } \sum \tfrac{1}{n^2} \text{ converges } (p = 2): \ \text{absolutely convergent}", r"\text{(b) } \sum \tfrac1n \text{ diverges; } \sum \tfrac{(-1)^n}{n} \text{ converges (AST)}", r"\text{conditionally convergent}",
                      r"\text{(c) } \tfrac{n}{n + 1} \to 1 \ne 0: \ \text{divergent}"], at=[1, 2, 2, 3])

        with self.beat("Close") as b:
            card = VGroup(T("absolute: $\\sum |a_n|$ converges (and then $\\sum a_n$ converges)", 34, DERIV), T("conditional: $\\sum a_n$ converges, $\\sum |a_n|$ diverges", 34, SECANT), T("check the absolute values first", 34)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Root n with alternating signs", r"Classify $\sum \frac{(-1)^n}{\sqrt n}$.", [r"\sum \tfrac{1}{\sqrt n} \text{ diverges } (p = \tfrac12)", r"\sum \tfrac{(-1)^n}{\sqrt n} \text{ converges (AST)}", r"\text{conditionally convergent}"], at=[1, 2, 2])
        self.example("Example 2: Signs that don't alternate", r"Classify $\sum \frac{\sin n}{n^2}$.", [r"\left|\tfrac{\sin n}{n^2}\right| \le \tfrac{1}{n^2}", r"\sum \tfrac{1}{n^2} \text{ converges, so } \sum \left|\tfrac{\sin n}{n^2}\right| \text{ converges}", r"\text{absolutely convergent (hence convergent)}"], at=[1, 2, 3])
        self.example("Example 3: n ln n", r"Classify $\displaystyle\sum_{n=2}^{\infty} \frac{(-1)^n}{n\ln n}$.", [r"\sum \tfrac{1}{n\ln n} \text{ diverges (integral test)}", r"\tfrac{1}{n\ln n} \text{ decreases to } 0: \text{ converges (AST)}", r"\text{conditionally convergent}"], at=[1, 2, 2])
        self.finish()
