"""Topic 6.14 BC (6.15 internally): Selecting techniques for antidifferentiation, with every tool in the course,
integration by parts and partial fractions included. The AB version is s6_14.py (docs/ab-bc-versions.md). The video
never calls anything BC (Adder, 6.11 review). Narration comes from transcripts/6_15.md."""
import numpy as np
from manim import *

from kit import *
from style import *
from s6_14 import tool_tray

PARTS = r"\int u\,dv = uv - \int v\,du"


def parts_table(u, dv, du, v):
    """The four-box table from 6.11: u and dv on top, du and v underneath. Entries start hidden; fill(...) reveals them."""
    labels = [r"u =", r"dv =", r"du =", r"v ="]
    boxes = VGroup()
    for k, (lab, val) in enumerate(zip(labels, [u, dv, du, v])):
        cell = VGroup(Rectangle(width=3.3, height=0.95, stroke_color=DIM, stroke_width=2), M(lab, 34, SECANT if k < 2 else DERIV), M(val, 34))
        cell[1].move_to(cell[0]).align_to(cell[0], LEFT).shift(RIGHT * 0.15)
        cell[2].next_to(cell[1], RIGHT, buff=0.15)
        cell[2].set_max_width(3.3 - cell[1].width - 0.4)
        cell[2].set_opacity(0)
        boxes.add(cell)
    boxes[1].next_to(boxes[0], RIGHT, buff=0)
    boxes[2].next_to(boxes[0], DOWN, buff=0)
    boxes[3].next_to(boxes[2], RIGHT, buff=0)
    return boxes


def fill(tab, *ks):
    return lambda scene: scene.play(*[tab[k][2].animate.set_opacity(1) for k in ks], run_time=0.6)


class Lesson(TranscriptScene):
    NUM = "6.15"

    def construct(self):
        names = ["basic rules", "rewrite: expand, split, powers", "substitution", "long division", "complete the square",
                 "integration by parts", "partial fractions"]
        later = ["integration by parts", "partial fractions"]
        with self.beat("A full toolkit") as b:
            tray = tool_tray(names, accent=later).to_edge(DOWN, buff=0.6)
            pile = VGroup(*[M(s, 34).move_to(p) for s, p in ((r"\int x e^{x^2}\,dx", UP * 2.4 + LEFT * 4.4), (r"\int x\ln x\,dx", UP * 2.8 + LEFT * 0.9),
                                                          (r"\int \frac{dx}{x^2 - 4}", UP * 2.3 + RIGHT * 3.2), (r"\int (2x - 1)^2\,dx", UP * 1.0 + LEFT * 2.5),
                                                          (r"\int \frac{x^3}{x - 1}\,dx", UP * 1.1 + RIGHT * 1.1), (r"\int x\sin x\,dx", UP * 0.9 + RIGHT * 4.7))])
            self.play(FadeIn(tray[0]), LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in tray[1]], lag_ratio=0.12), run_time=2)
            self.play(LaggedStart(*[FadeIn(p) for p in pile], lag_ratio=0.2), run_time=1.4)
            b.line(1)
            self.play(Indicate(tray[1][2], color=SECANT), pile[0].animate.set_color(SECANT), run_time=1)
            self.play(Indicate(tray[1][5], color=ACCUM), pile[1].animate.set_color(ACCUM), run_time=1)
            b.line(2)
            self.play(Indicate(tray[1][6], color=ACCUM), pile[2].animate.set_color(ACCUM), run_time=1)
        self.clear()
        self.title()

        with self.beat("What to look for") as b:
            rows = [("a basic form (power, trig, $e^x$, $1/x$)", "basic rules", SECANT), ("a product, a power of a sum, or a sum over one term", "rewrite first", SECANT),
                    ("an inside function whose derivative is a factor", "substitution", SECANT), ("a fraction, top degree $\\ge$ bottom degree", "long division", SECANT),
                    ("$1$ over a quadratic that won't factor", "complete the square", SECANT),
                    ("a product of two kinds of functions, no inside derivative", "integration by parts", ACCUM),
                    ("a fraction whose bottom factors into different lines", "partial fractions", ACCUM)]
            cells = VGroup(*[VGroup(T(l, 28), T(r, 28, c)) for l, r, c in rows])
            for k, c in enumerate(cells):
                c[0].set_max_width(8.2).move_to(LEFT * 2.3 + UP * (2.4 - 0.78 * k))
                c[1].move_to(RIGHT * 4.6 + UP * (2.4 - 0.78 * k))
            hdr = VGroup(T("notice", 30, DIM).move_to(LEFT * 2.3 + UP * 3.25), T("tool", 30, DIM).move_to(RIGHT * 4.6 + UP * 3.25))
            self.play(FadeIn(hdr), FadeIn(cells[0]), run_time=0.8)
            for k, line in ((1, 1), (2, 2), (3, 3), (4, 3), (5, 4), (6, 5)):
                b.line(line)
                self.play(FadeIn(cells[k]), run_time=0.6)
                if k == 2:
                    self.play(Indicate(cells[2][1], color=SECANT), run_time=0.8)
        self.clear()

        self.example("Choosing the tool",
                     r"Choose a technique for each: (a) $\int x e^{2x}\,dx$ (b) $\int x e^{x^2}\,dx$ (c) $\int \frac{x + 5}{(x - 1)(x + 2)}\,dx$ (d) $\int \frac{dx}{x^2 + 4x + 5}$.",
                     [r"\text{(a) a product, no inside derivative: parts, } u = x, \ dv = e^{2x}\,dx",
                      r"\text{(b) } u = x^2 \text{ (}2x \text{ is a factor): substitution, } \tfrac12 e^{x^2} + C",
                      r"\text{(c) the bottom factors: partial fractions, } 2\ln|x - 1| - \ln|x + 2| + C",
                      r"\text{(d) } (x + 2)^2 + 1: \ \arctan(x + 2) + C"], at=[1, 2, 3, 4], follow=True, size=40)

        with self.beat("Close") as b:
            tray = tool_tray(names, accent=later).shift(DOWN * 0.6)
            self.play(FadeIn(tray), run_time=1)
            self.play(Indicate(tray[1][2], color=SECANT), run_time=0.8)
            self.play(FadeIn(T("Check substitution first. Notice the features. Pick the tool.", 36, SECANT).next_to(tray, UP, buff=0.8)), run_time=0.8)
        self.clear()

        self.examples_card()
        t1 = parts_table(r"\ln x", r"x\,dx", r"\frac1x\,dx", r"\frac{x^2}{2}")
        self.example("Example 1: A product of two kinds", r"Find $\displaystyle\int x\ln x\,dx$.",
                     [r"TEXT:No inside function with its derivative as a factor: parts.", r"u = \ln x, \ \ dv = x\,dx", r"du = \frac1x\,dx, \ \ v = \frac{x^2}{2}",
                      r"\int x\ln x\,dx = \frac{x^2}{2}\ln x - \int \frac{x^2}{2} \cdot \frac1x\,dx", r"\frac{x^2}{2} \cdot \frac1x = \frac x2",
                      r"= \frac{x^2}{2}\ln x - \frac{x^2}{4} + C"], at=[1, 2, 3, 4, 5, 6], figure=t1, ref=PARTS,
                     cues={1: fill(t1, 0, 1), 2: fill(t1, 2, 3)}, size=40)
        self.example("Example 2: The same pieces, rearranged", r"Find $\displaystyle\int \frac{\ln x}{x}\,dx$.",
                     [r"TEXT:$\frac{d}{dx}\ln x = \frac1x$, a factor: substitution.", r"u = \ln x, \ \ du = \frac1x\,dx", r"\int \frac{\ln x}{x}\,dx = \int u\,du = \frac{u^2}{2}",
                      r"= \frac{(\ln x)^2}{2} + C", r"TEXT:One piece is the other's derivative: substitution."], at=[1, 2, 3, 4, 5], size=44)
        self.example("Example 3: A bottom that factors", r"Find $\displaystyle\int \frac{2}{x^2 - 1}\,dx$.",
                     [r"TEXT:No $x$ on top for substitution. The bottom factors: $(x - 1)(x + 1)$.", r"\frac{2}{(x - 1)(x + 1)} = \frac{A}{x - 1} + \frac{B}{x + 1}",
                      r"2 = A(x + 1) + B(x - 1)", r"\text{Let } x = 1\text{:} \quad 2 = 2A, \ \text{so } A = 1", r"\text{Let } x = -1\text{:} \quad 2 = -2B, \ \text{so } B = -1",
                      r"\int \left(\frac{1}{x - 1} - \frac{1}{x + 1}\right) dx", r"= \ln|x - 1| - \ln|x + 1| + C"], at=[1, 2, 3, 4, 5, 6, 7], size=40)
        self.example("Example 4: Check substitution first", r"Find $\displaystyle\int \frac{2x}{x^2 - 1}\,dx$.",
                     [r"TEXT:$\frac{d}{dx}\left(x^2 - 1\right) = 2x$, the top: substitution.", r"u = x^2 - 1, \ \ du = 2x\,dx", r"\int \frac{2x}{x^2 - 1}\,dx = \int \frac1u\,du = \ln|u|",
                      r"= \ln\left|x^2 - 1\right| + C", r"TEXT:Partial fractions agrees: $\ln|x - 1| + \ln|x + 1| = \ln\left|x^2 - 1\right|$."], at=[1, 2, 3, 4, 5], size=44)
        self.finish()
