"""Topic 6.12 (BC): Linear partial fractions. Narration comes from transcripts/6_12.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "6.12"

    def construct(self):
        with self.beat("Adding fractions, backward") as b:
            bc = T("BC only", 28, DIM).to_corner(UR, buff=0.4)
            fwd = M(r"\frac{2}{x - 1} + \frac{3}{x + 2}", r"=", r"\frac{2(x + 2) + 3(x - 1)}{(x - 1)(x + 2)}", r"=", r"\frac{5x + 1}{(x - 1)(x + 2)}", 44).shift(UP * 0.8)
            fwd.set_max_width(13)
            self.play(FadeIn(bc), Write(fwd), run_time=1.6)
            b.line(1)
            arc = CurvedArrow(fwd[4].get_bottom() + DOWN * 0.2, fwd[0].get_bottom() + DOWN * 0.2, color=ACCUM, angle=-TAU / 6)
            self.play(Create(arc), FadeIn(T("partial fractions", 32, ACCUM).next_to(arc, DOWN, buff=0.15)), run_time=1)
            b.line(2)
            self.play(FadeIn(M(r"\int \frac{A}{x - r}\,dx = A\ln|x - r| + C", 44, SECANT).to_edge(DOWN, buff=0.7)), run_time=0.8)
        self.clear()
        self.title()

        self.example("The method", r"Find $\displaystyle\int \frac{1}{x^2 - 1}\,dx$.",
                     [r"x^2 - 1 = (x - 1)(x + 1)", r"\frac{1}{(x - 1)(x + 1)} = \frac{A}{x - 1} + \frac{B}{x + 1}", r"1 = A(x + 1) + B(x - 1)",
                      r"x = 1: \ 1 = 2A, \ A = \tfrac12; \quad x = -1: \ 1 = -2B, \ B = -\tfrac12", r"\int \left(\frac{1/2}{x - 1} - \frac{1/2}{x + 1}\right) dx = \tfrac12\ln|x - 1| - \tfrac12\ln|x + 1| + C"],
                     at=[0, 1, 2, 3, 4], follow=True)
        self.example("Using the method", r"Find $\displaystyle\int \frac{x + 7}{x^2 - x - 6}\,dx$.",
                     [r"x^2 - x - 6 = (x - 3)(x + 2)", r"\frac{A}{x - 3} + \frac{B}{x + 2}: \ \ x + 7 = A(x + 2) + B(x - 3)", r"x = 3: \ 10 = 5A, \ A = 2", r"x = -2: \ 5 = -5B, \ B = -1",
                      r"\int \left(\frac{2}{x - 3} - \frac{1}{x + 2}\right) dx = 2\ln|x - 3| - \ln|x + 2| + C"], at=[1, 2, 3, 3, 4])

        with self.beat("Close") as b:
            card = VGroup(T("Factor the denominator into distinct linear factors.", 36), M(r"\frac{A}{\text{first factor}} + \frac{B}{\text{second factor}}", 42),
                          T("Multiply through; plug in each root to find $A$ and $B$.", 36), M(r"\text{each piece: } A\ln|\text{linear}|", 40, ACCUM),
                          T("Top degree too big? Divide first.", 32, DIM)).arrange(DOWN, buff=0.4)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Undo the addition", r"Find $\displaystyle\int \frac{5x + 1}{(x - 1)(x + 2)}\,dx$.",
                     [r"5x + 1 = A(x + 2) + B(x - 1)", r"x = 1: \ 6 = 3A, \ A = 2; \quad x = -2: \ -9 = -3B, \ B = 3", r"\int \left(\frac{2}{x - 1} + \frac{3}{x + 2}\right) dx = 2\ln|x - 1| + 3\ln|x + 2| + C"],
                     at=[1, 2, 3])
        self.example("Example 2: A definite integral", r"Evaluate $\displaystyle\int_2^3 \frac{1}{x(x - 1)}\,dx$.",
                     [r"1 = A(x - 1) + Bx", r"x = 0: \ A = -1; \quad x = 1: \ B = 1", r"\left[\ln|x - 1| - \ln|x|\right]_2^3", r"= (\ln 2 - \ln 3) - (\ln 1 - \ln 2) = 2\ln 2 - \ln 3 = \ln\tfrac43"],
                     at=[1, 2, 3, 4])
        self.finish()
