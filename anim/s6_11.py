"""Topic 6.11 (BC): Integration by parts. Narration comes from transcripts/6_11.md.

Adder's 6.11 notes (2026-10-14): no "BC only" in the video (the site marks it). Besides LIATE, say how to choose: u gets
simpler when differentiated, dv at least doesn't get much more complicated when integrated. In x e^x, point out both, and
that the other way round raises x's exponent. In the ln x example write dv = 1 dx (integrating the constant 1); v = x is
"more" complicated, but the setup has an x that cancels.
"""
import numpy as np
from manim import *

from kit import *
from style import *


def parts_table(u, dv, du, v):
    """The four-box table: u and dv on top, du and v underneath. Entries start hidden; fill(...) cues reveal them."""
    labels = [r"u =", r"dv =", r"du =", r"v ="]
    vals = [u, dv, du, v]
    boxes = VGroup()
    for k, (lab, val) in enumerate(zip(labels, vals)):
        cell = VGroup(Rectangle(width=3.3, height=0.95, stroke_color=DIM, stroke_width=2),
                      M(lab, 34, SECANT if k < 2 else DERIV), M(val, 34))
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
    NUM = "6.11"
    example_ref = r"\int u\,dv = uv - \int v\,du"

    def construct(self):
        with self.beat("The product rule, backward") as b:
            r1 = M(r"(uv)' = u'v + uv'", 54).shift(UP * 1.8)
            self.play(Write(r1), run_time=1)
            b.line(1)
            r2 = M(r"uv = \int v\,du + \int u\,dv", 54).next_to(r1, DOWN, buff=0.6)
            self.play(Write(r2), run_time=1.2)
            b.line(2)
            r3 = formula_box(M(r"\int u\,dv = uv - \int v\,du", 60, ACCUM), ACCUM).next_to(r2, DOWN, buff=0.7)
            self.play(FadeIn(r3), run_time=1)
        self.clear()
        self.title()

        with self.beat("Choosing u") as b:
            tab = parts_table("", "", "", "").to_edge(LEFT, buff=0.8).shift(UP * 1.3)
            self.play(FadeIn(tab), run_time=0.8)
            b.line(1)
            ru = T("$u$: gets simpler when you differentiate it", 30, SECANT)
            rdv = VGroup(T("$dv$: doesn't get much more complicated", 30, DERIV), T("when you integrate it (includes $dx$)", 30, DERIV)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            rules = VGroup(ru, rdv).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(tab, DOWN, buff=0.6).align_to(tab, LEFT)
            self.play(FadeIn(ru), Indicate(tab[0][1], color=SECANT), run_time=0.8)
            b.line(2)
            self.play(FadeIn(rdv), Indicate(tab[1][1], color=DERIV), run_time=0.8)
            b.line(3)
            liate = VGroup(*[T(w, 34, SECANT if k == 0 else INK) for k, w in enumerate(("Logarithmic", "Inverse trig", "Algebraic", "Trig", "Exponential"))]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            letters = VGroup(*[M(w[0], 40, SECANT).next_to(t, LEFT, buff=0.3) for w, t in zip(("L", "I", "A", "T", "E"), liate)])
            g = VGroup(letters, liate).to_edge(RIGHT, buff=1.0).shift(DOWN * 0.3)
            arrow = Arrow(g.get_corner(DL) + LEFT * 0.4, g.get_corner(UL) + LEFT * 0.4, color=SECANT, buff=0)
            self.play(FadeIn(g), GrowArrow(arrow), FadeIn(T("choose $u$ from the top", 28, SECANT).next_to(g, UP, buff=0.3)), run_time=1)
        self.clear()

        t1 = parts_table("x", r"e^x\,dx", "dx", "e^x")
        self.example("A first example", r"Find $\displaystyle\int x e^x\,dx$.",
                     [r"u = x, \ \ dv = e^x\,dx", r"TEXT:$x$ gets simpler: $du = dx$.", r"TEXT:$e^x$ is no worse: $v = e^x$.",
                      r"TEXT:The other way, $v = \frac{x^2}{2}$: a bigger exponent.",
                      r"\int x e^x\,dx = x e^x - \int e^x\,dx", r"= x e^x - e^x + C"], at=[1, 2, 3, 4, 5, 6], figure=t1,
                     cues={0: fill(t1, 0, 1), 1: fill(t1, 2), 2: fill(t1, 3)}, follow=True, size=42)
        t2 = parts_table(r"\ln x", r"1\,dx", r"\frac1x\,dx", "x")
        self.example("A definite integral", r"Evaluate $\displaystyle\int_1^e \ln x\,dx$.",
                     [r"u = \ln x", r"dv = 1\,dx", r"du = \frac1x\,dx, \ \ v = x", r"\left[x\ln x\right]_1^e - \int_1^e x \cdot \frac1x\,dx",
                      r"\cancel{x} \cdot \frac{1}{\cancel{x}} = 1", r"= \left[x\ln x - x\right]_1^e",
                      r"= (e \cdot 1 - e) - (1 \cdot 0 - 1)", r"= 0 - (-1) = 1"],
                     at=[0, 1, 2, 3, 4, 4, 5, 6], figure=t2, follow=True, size=40,
                     cues={0: fill(t2, 0), 1: fill(t2, 1), 2: fill(t2, 2, 3)})

        with self.beat("Close") as b:
            card = VGroup(M(r"\int u\,dv = uv - \int v\,du", 50, ACCUM), T("$u$: gets simpler when differentiated (LIATE).", 34),
                          T("$dv$: the rest, including $dx$; no worse when integrated.", 34), T("Use the four-box table.", 34, SECANT)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        e1 = parts_table("x", r"\cos x\,dx", "dx", r"\sin x")
        self.example("Example 1: A trig factor", r"Find $\displaystyle\int x\cos x\,dx$.",
                     [r"u = x, \ dv = \cos x\,dx, \ du = dx, \ v = \sin x", r"= x\sin x - \int \sin x\,dx", r"= x\sin x - (-\cos x)", r"= x\sin x + \cos x + C"], at=[1, 2, 3, 4], figure=e1,
                     cues={0: fill(e1, 0, 1, 2, 3)})
        e2 = parts_table("x^2", r"e^x\,dx", r"2x\,dx", "e^x")
        e2b = parts_table("2x", r"e^x\,dx", r"2\,dx", "e^x")

        def second(sc):
            e2b.move_to(e2)
            for c in e2b:
                c[2].set_opacity(1)
            sc.play(FadeOut(e2), FadeIn(e2b), run_time=0.8)
        self.example("Example 2: Parts twice", r"Find $\displaystyle\int x^2 e^x\,dx$.",
                     [r"= x^2 e^x - \int 2x e^x\,dx", r"\int 2x e^x\,dx = 2x e^x - \int 2e^x\,dx = 2x e^x - 2e^x", r"\int x^2 e^x\,dx = x^2 e^x - 2x e^x + 2e^x + C", r"= e^x\left(x^2 - 2x + 2\right) + C"],
                     at=[1, 2, 3, 4], figure=e2, cues={0: fill(e2, 0, 1, 2, 3), 1: second})
        e3 = parts_table(r"\arctan x", r"1\,dx", r"\frac{1}{1 + x^2}\,dx", "x")
        self.example("Example 3: An inverse trig function", r"Find $\displaystyle\int \arctan x\,dx$.",
                     [r"u = \arctan x, \ dv = 1\,dx, \ du = \frac{dx}{1 + x^2}, \ v = x", r"= x\arctan x - \int \frac{x}{1 + x^2}\,dx",
                      r"w = 1 + x^2, \ dw = 2x\,dx: \ \int \frac{x}{1 + x^2}\,dx = \tfrac12\ln\left(1 + x^2\right)", r"x\arctan x - \tfrac12\ln\left(1 + x^2\right) + C"],
                     at=[1, 2, 3, 4], figure=e3, cues={0: fill(e3, 0, 1, 2, 3)})
        self.finish()
