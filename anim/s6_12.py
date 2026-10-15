"""Topic 6.12 (BC): Linear partial fractions. Narration comes from transcripts/6_12.md.

Adder's 6.12 notes (2026-10-14): no "BC only" in the video. Take the method nice and slow: whenever the denominator is a
product of factors, rewrite as A over the first factor plus B over the second, and so on; then a little equation for A
and B; choose x values that cancel one term or the other; say "let x = 1" and write "Let x = 1" on the board, so it's
clear we haven't solved anything for x. Only distinct linear factors: the CED's FUN-6.F.1 says "linear, nonrepeating".
"""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "6.12"
    # the split being practiced stays in the corner during the examples (formulas stay on screen)
    example_ref = r"\frac{p(x)}{(x - r)(x - s)} = \frac{A}{x - r} + \frac{B}{x - s}"

    def construct(self):
        with self.beat("Adding fractions, backward") as b:
            fwd = M(r"\frac{2}{x - 1} + \frac{3}{x + 2}", r"=", r"\frac{2(x + 2) + 3(x - 1)}{(x - 1)(x + 2)}", r"=", r"\frac{5x + 1}{(x - 1)(x + 2)}", 44).shift(UP * 0.8)
            fwd.set_max_width(13)
            self.play(Write(fwd), run_time=1.6)
            b.line(1)
            arc = CurvedArrow(fwd[4].get_bottom() + DOWN * 0.2, fwd[0].get_bottom() + DOWN * 0.2, color=ACCUM, angle=-TAU / 6)
            self.play(Create(arc), FadeIn(T("partial fractions", 32, ACCUM).next_to(arc, DOWN, buff=0.15)), run_time=1)
            b.line(2)
            self.play(FadeIn(M(r"\int \frac{A}{x - r}\,dx = A\ln|x - r| + C", 44, SECANT).to_edge(DOWN, buff=0.7)), run_time=0.8)
        self.clear()
        self.title()

        self.example("The method", r"Find $\displaystyle\int \frac{1}{x^2 - 1}\,dx$.",
                     [r"x^2 - 1 = (x - 1)(x + 1)", r"\frac{1}{(x - 1)(x + 1)} = \frac{A}{x - 1} + \frac{B}{x + 1}",
                      r"TEXT:Multiply both sides by $(x - 1)(x + 1)$.", r"1 = A(x + 1) + B(x - 1)",
                      r"TEXT:Pick $x$ values that make one term cancel.",
                      r"\text{Let } x = 1\text{:} \quad 1 = A(1 + 1) + B(1 - 1)", r"1 = 2A, \ \text{so } A = \tfrac12",
                      r"\text{Let } x = -1\text{:} \quad 1 = A(-1 + 1) + B(-1 - 1)", r"1 = -2B, \ \text{so } B = -\tfrac12",
                      r"\int \left(\frac{1/2}{x - 1} - \frac{1/2}{x + 1}\right) dx = \tfrac12\ln|x - 1| - \tfrac12\ln|x + 1| + C"],
                     at=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], follow=True, size=40)
        self.example("Using the method", r"Find $\displaystyle\int \frac{x + 7}{x^2 - x - 6}\,dx$.",
                     [r"x^2 - x - 6 = (x - 3)(x + 2)", r"\frac{x + 7}{(x - 3)(x + 2)} = \frac{A}{x - 3} + \frac{B}{x + 2}", r"x + 7 = A(x + 2) + B(x - 3)",
                      r"\text{Let } x = 3\text{:} \quad 10 = 5A, \ \text{so } A = 2", r"\text{Let } x = -2\text{:} \quad 5 = -5B, \ \text{so } B = -1",
                      r"\int \left(\frac{2}{x - 3} - \frac{1}{x + 2}\right) dx = 2\ln|x - 3| - \ln|x + 2| + C"], at=[1, 2, 3, 4, 5, 6], size=42)

        with self.beat("Close") as b:
            card = VGroup(T("Factor the denominator.", 36), M(r"\frac{A}{\text{first factor}} + \frac{B}{\text{second factor}} + \cdots", 42),
                          T("Multiply through. Let $x$ be each root to find $A$ and $B$.", 36), M(r"\text{each piece: } A\ln|\text{linear}|", 40, ACCUM),
                          T("Top degree too big? Divide first.", 32, DIM)).arrange(DOWN, buff=0.4)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Undo the addition", r"Find $\displaystyle\int \frac{5x + 1}{(x - 1)(x + 2)}\,dx$.",
                     [r"\frac{5x + 1}{(x - 1)(x + 2)} = \frac{A}{x - 1} + \frac{B}{x + 2}", r"5x + 1 = A(x + 2) + B(x - 1)",
                      r"\text{Let } x = 1\text{:} \quad 6 = 3A, \ \text{so } A = 2", r"\text{Let } x = -2\text{:} \quad -9 = -3B, \ \text{so } B = 3",
                      r"\int \left(\frac{2}{x - 1} + \frac{3}{x + 2}\right) dx = 2\ln|x - 1| + 3\ln|x + 2| + C"],
                     at=[1, 1, 2, 2, 3], size=42)
        self.example("Example 2: A definite integral", r"Evaluate $\displaystyle\int_2^3 \frac{1}{x(x - 1)}\,dx$.",
                     [r"\frac{1}{x(x - 1)} = \frac{A}{x} + \frac{B}{x - 1}", r"1 = A(x - 1) + Bx", r"\text{Let } x = 0\text{:} \quad 1 = -A, \ \text{so } A = -1", r"\text{Let } x = 1\text{:} \quad 1 = B, \ \text{so } B = 1",
                      r"\int_2^3 \left(\frac{-1}{x} + \frac{1}{x - 1}\right) dx = \left[\ln|x - 1| - \ln|x|\right]_2^3",
                      r"= (\ln 2 - \ln 3) - (\ln 1 - \ln 2) = 2\ln 2 - \ln 3 = \ln\tfrac43"],
                     at=[1, 1, 2, 2, 3, 4], size=42)
        self.finish()
