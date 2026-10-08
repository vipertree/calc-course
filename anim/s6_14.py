"""Topic 6.14: Selecting techniques for antidifferentiation. Narration comes from transcripts/6_14.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def tool_tray(names, bc_names, width=13):
    """A toolkit tray (Adder: a toolkit, not a decision tree), as in 1.7: a long tray with a labeled card in each slot,
    and a separate BC section at the right."""
    n = len(names) + len(bc_names)
    w = (width - 0.6) / n
    cards = VGroup()
    for k, name in enumerate(list(names) + list(bc_names)):
        bc = k >= len(names)
        card = VGroup(RoundedRectangle(width=w - 0.15, height=1.5, corner_radius=0.12, stroke_color=ACCUM if bc else SECANT, stroke_width=3, fill_color=PANEL, fill_opacity=1),
                      T(name, 24, ACCUM if bc else INK))
        card[1].set_max_width(w - 0.35).move_to(card[0])
        cards.add(card)
    cards.arrange(RIGHT, buff=0.15)
    tray = RoundedRectangle(width=cards.width + 0.4, height=1.9, corner_radius=0.2, stroke_color=DIM, stroke_width=3, fill_color=WOOD, fill_opacity=0.25).move_to(cards)
    sep = DashedLine(cards[len(names) - 1].get_right() + RIGHT * 0.075 + UP * 0.95, cards[len(names) - 1].get_right() + RIGHT * 0.075 + DOWN * 0.95, color=DIM)
    bc_tag = T("BC", 24, ACCUM).next_to(VGroup(*cards[len(names):]), UP, buff=0.15)
    return VGroup(tray, cards, sep, bc_tag)


class Lesson(TranscriptScene):
    NUM = "6.14"

    def construct(self):
        names = ["basic rules", "rewrite: expand, split, powers", "substitution", "long division", "complete the square"]
        bc = ["integration by parts", "partial fractions"]
        with self.beat("A toolkit") as b:
            tray = tool_tray(names, bc).to_edge(DOWN, buff=0.6)
            pile = VGroup(*[M(s, 34).move_to(p) for s, p in ((r"\int x e^{x^2}\,dx", UP * 2.4 + LEFT * 4), (r"\int \frac{dx}{x^2 + 9}", UP * 2.8 + LEFT * 0.6),
                                                          (r"\int \frac{x^3}{x - 1}\,dx", UP * 2.2 + RIGHT * 3.4), (r"\int (2x - 1)^2\,dx", UP * 1.1 + LEFT * 2.2),
                                                          (r"\int x\ln x\,dx", UP * 1.2 + RIGHT * 1.4), (r"\int \sec^2 x\,dx", UP * 0.9 + RIGHT * 4.8))])
            self.play(FadeIn(tray[0]), LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in tray[1]], lag_ratio=0.15), FadeIn(tray[2]), FadeIn(tray[3]), run_time=2)
            self.play(LaggedStart(*[FadeIn(p) for p in pile], lag_ratio=0.2), run_time=1.4)
            b.line(1)
            self.play(Indicate(tray[1][2], color=SECANT), pile[0].animate.set_color(SECANT), run_time=1)
            b.line(2)
            self.play(Indicate(tray[1][4], color=SECANT), pile[1].animate.set_color(SECANT), run_time=1)
        self.clear()
        self.title()

        with self.beat("What to look for") as b:
            rows = [("a basic form (power, trig, $e^x$, $1/x$)", "basic rules", SECANT), ("a product, a power of a sum, or a sum over one term", "rewrite first", SECANT),
                    ("an inside function whose derivative is a factor", "substitution", SECANT), ("a fraction, top degree $\\ge$ bottom degree", "long division", SECANT),
                    ("$1$ over a quadratic that won't factor", "complete the square", SECANT), ("a product of two different kinds of functions", "parts (BC)", ACCUM),
                    ("a fraction whose bottom factors into lines", "partial fractions (BC)", ACCUM)]
            cells = VGroup(*[VGroup(T(l, 28), T(r, 28, c)) for l, r, c in rows])
            for k, c in enumerate(cells):
                c[0].move_to(LEFT * 2.6 + UP * (2.4 - 0.72 * k))
                c[1].move_to(RIGHT * 4.3 + UP * (2.4 - 0.72 * k))
            hdr = VGroup(T("notice", 30, DIM).move_to(LEFT * 2.6 + UP * 3.2), T("tool", 30, DIM).move_to(RIGHT * 4.3 + UP * 3.2))
            self.play(FadeIn(hdr), FadeIn(cells[0]), run_time=0.8)
            for k, line in ((1, 1), (2, 2), (3, 3), (4, 3), (5, 4), (6, 4)):
                b.line(line)
                self.play(FadeIn(cells[k]), run_time=0.6)
        self.clear()

        self.example("Choosing the tool",
                     r"Choose a technique for each: (a) $\int x\cos\left(x^2\right) dx$ (b) $\int \left(x^2 + 1\right)^2 dx$ (c) $\int \frac{dx}{x^2 + 6x + 10}$ (d) $\int \sin^2 x\cos x\,dx$.",
                     [r"\text{(a) } u = x^2 \text{ (}2x \text{ is a factor): substitution, } \tfrac12\sin\left(x^2\right) + C", r"\text{(b) a power of a sum: expand, then the power rule}",
                      r"\text{(c) } (x + 3)^2 + 1: \ \arctan(x + 3) + C", r"\text{(d) } u = \sin x \text{ (}\cos x \text{ is a factor): } \tfrac13\sin^3 x + C"], at=[1, 2, 3, 4])

        with self.beat("Close") as b:
            tray = tool_tray(names, bc).shift(DOWN * 0.6)
            self.play(FadeIn(tray), run_time=1)
            self.play(FadeIn(T("Notice the features. Pick the tool. Try another if it fails.", 36, SECANT).next_to(tray, UP, buff=0.8)), run_time=0.8)
        self.clear()

        self.examples_card()
        self.example("Example 1: A substitution in disguise", r"Find $\displaystyle\int \frac{x + 1}{x^2 + 2x + 5}\,dx$.",
                     [r"\frac{d}{dx}\left(x^2 + 2x + 5\right) = 2x + 2 = 2(x + 1): \text{ a factor}", r"u = x^2 + 2x + 5, \ du = 2(x + 1)\,dx, \ (x + 1)\,dx = \tfrac12\,du",
                      r"\int \tfrac12 \cdot \frac1u\,du = \tfrac12\ln|u|", r"= \tfrac12\ln\left(x^2 + 2x + 5\right) + C"], at=[1, 2, 3, 4])
        self.example("Example 2: Same bottom, different top", r"Find $\displaystyle\int \frac{1}{x^2 + 2x + 5}\,dx$.",
                     [r"\text{no factor of } 2x + 2 \text{ on top: not substitution}", r"x^2 + 2x + 5 = (x + 1)^2 + 4", r"u = x + 1, \ a = 2: \ \int \frac{du}{u^2 + 2^2} = \tfrac12\arctan\frac u2",
                      r"= \tfrac12\arctan\frac{x + 1}{2} + C"], at=[1, 2, 3, 3])
        self.example("Example 3: Flip the fraction", r"Find $\displaystyle\int \frac{x^2 + 2x + 5}{x + 1}\,dx$.",
                     [r"\text{top degree } 2 \ge \text{bottom degree } 1: \text{ divide}", r"x^2 + 2x + 5 = (x + 1)(x + 1) + 4", r"\frac{x^2 + 2x + 5}{x + 1} = x + 1 + \frac{4}{x + 1}",
                      r"\int = \frac{x^2}{2} + x + 4\ln|x + 1| + C"], at=[1, 2, 2, 3])
        self.finish()
