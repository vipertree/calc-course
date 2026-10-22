"""Topic 8.10: Disc method about other axes. Narration comes from transcripts/8_10.md.

Adder's notes (2026-10-14, with 8.9's): the same angled sweep that keeps its volume; text never runs over the graph
(the old "that's the distance to the x-axis" sat on the x-axis like a strike-through, so all words now live on the
board beside the picture); examples draw the curves, find and shade the region, spin it once, then show ONE disc at x
with its R, never the whole rotated region with all its slices. 3D pictures come from anim/solids.py.
"""
import numpy as np
from manim import *

from kit import *
from solids import *
from style import *

ZERO = lambda s: 0.0
ONE = lambda s: 1.0
FOUR = lambda s: 4.0
SQ = lambda s: np.sqrt(max(s, 0.0))
PAR = lambda s: s * s
REF_X = r"V = \pi\int_a^b [R(x)]^2\,dx"
REF_Y = r"V = \pi\int_c^d [R(y)]^2\,dy"


def about_four(at=1.1, scale=0.55, extra=None, extra_params=None, ticks=None):
    """The region between y = x^2 and y = 4, with the axis y = 4."""
    return rev_stage([(PAR, -2.12, 2.12, FUNC, "y = x^2", (2.6, 3.4), "x")], region_outline(FOUR, PAR, -2, 2), "x", 4.0, PAR, (-2.8, 3.0), (-0.6, 8.6),
                     at=at, shade=(FOUR, PAR, -2, 2, "x"), axis_tex="y = 4", axis_lab=(-1.15, 4.6), ticks=ticks or {"x": [-2, 2], "y": [4, 8]}, scale=scale,
                     pose=(-36.0, 16.0), turn=-20.0, extra=extra, extra_params=extra_params)


def about_one(at=0.5, scale=1.15):
    """The region between x = y^2 and x = 1, with the axis x = 1."""
    return rev_stage([(PAR, -1.2, 1.2, FUNC, "x = y^2", (1.75, 1.3), "y")], outline_y(ONE, PAR, -1, 1), "y", 1.0, PAR, (-0.6, 2.5), (-1.6, 1.75),
                     at=at, shade=(ONE, PAR, -1, 1, "y"), axis_tex="x = 1", axis_lab=(1.4, -1.45), ticks={"x": [1, 2], "y": [-1, 1]}, scale=scale,
                     pose=(-26.0, 26.0), turn=-12.0)


class Lesson(TranscriptScene):
    NUM = "8.10"

    def construct(self):
        # ---------------------------------------------------------------- cold open: the same region, two axes
        with self.beat("A different axis") as b:
            left = rev_stage([(PAR, -2.12, 2.12, FUNC, "y = x^2", (2.55, 3.3), "x")], region_outline(FOUR, PAR, -2, 2), "x", 0.0, FOUR, (-2.8, 3.0), (-4.6, 4.9),
                             at=0.0, shade=(FOUR, PAR, -2, 2, "x"), ticks={"x": [-2, 2], "y": [4]}, scale=0.52, pose=(-40.0, 18.0), turn=-16.0)
            right = about_four(scale=0.52, ticks={"x": [-2, 2], "y": [4]})
            left.move_to(LEFT * 3.5 + UP * 0.1)
            right.move_to(RIGHT * 3.3 + UP * 0.1)
            cl, cr = rev_cues(left), rev_cues(right)
            self.play(FadeIn(left), FadeIn(right), run_time=0.6)
            self.play(left.to("c0", 1), right.to("c0", 1), run_time=1.2)
            self.play(left.to("shade", 1), right.to("shade", 1), right.to("axis", 1), run_time=1.0)
            b.line(1)
            cl["spin"](rt=1.4, sweep=3.0, hold=0)(self)
            hole = T("a hole: next topic", 30, DIM).next_to(left, DOWN, buff=0.15)
            self.play(FadeIn(hole), left.spin(-16), run_time=1.2)
            b.line(2)
            cr["spin"](rt=1.4, sweep=3.0, hold=0)(self)
            b.line(3)
            self.play(left.spin(-16), right.spin(-20), run_time=3)
        self.clear()
        self.title()

        # ---------------------------------------------------------------- the radius: from the curve to THIS axis
        with self.beat("The radius is a distance to the axis") as b:
            x0 = 1.1

            def wrong(st, v, p):
                if p["wrong"] < 0.01:
                    return []
                q0, q1 = v.P(-x0, 0, 0), v.P(-x0, 0, PAR(x0))
                return [Line(q0, q0 + (q1 - q0) * min(1.0, p["wrong"]), color=DIM, stroke_width=6)]
            st = about_four(at=x0, scale=0.62, extra=wrong, extra_params={"wrong": 0.0})
            st.move_to(LEFT * 3.6 + DOWN * 0.1)
            c = rev_cues(st)
            self.play(FadeIn(st), run_time=0.6)
            c["draw"](0, rt=1.2)(self)
            c["axis"]()(self)
            c["shade"]()(self)
            b.line(1)
            c["rad"](rt=1.0)(self)
            good = M(r"R = 4 - x^2", 44, TANGENT)
            bad = M(r"R = x^2", 40, DIM)
            why = T("$x^2$ is the distance down to the $x$-axis", 28, DIM)
            rules = VGroup(M(r"R = (\text{bigger}) - (\text{smaller})", 38), M(r"\text{axis above the curve: } R = k - f(x)", 32),
                           M(r"\text{axis below the curve: } R = f(x) - k", 32))
            board = VGroup(good, bad, why, rules.arrange(DOWN, buff=0.3)).arrange(DOWN, buff=0.4).move_to(RIGHT * 3.3 + DOWN * 0.1)
            why.next_to(bad, DOWN, buff=0.15)
            self.play(Write(good), run_time=1)
            b.line(2)
            self.play(st.to("wrong", 1), FadeIn(bad), run_time=1.0)
            strike = Line(bad.get_left() + LEFT * 0.1, bad.get_right() + RIGHT * 0.1, color=TANGENT, stroke_width=5)
            self.play(Create(strike), FadeIn(why), run_time=0.8)
            b.line(3)
            self.play(st.to("wrong", 0), run_time=0.5)
            c["spin"](rt=1.4, sweep=3.0, hold=0.8)(self)
            c["slice"](rt=1.2)(self)
            self.wait(1.0)
            c["flat"](rt=1.4)(self)
            b.line(4)
            self.play(FadeIn(rules), run_time=1)
        self.clear()

        # ---------------------------------------------------------------- the lesson example
        st = about_four(at=1.1, scale=0.6)
        c = rev_cues(st)
        self.example("Spinning about y = 4", r"The region bounded by $y = x^2$ and $y = 4$ is revolved about the line $y = 4$. Find the volume.",
                     [r"TEXT:Sketch: the parabola, the line $y = 4$, the region between", r"x^2 = 4 \text{ at } x = \pm2", r"TEXT:One slice at $x$: a disc centered on $y = 4$",
                      r"R(x) = 4 - x^2", r"R^2 = \left(4 - x^2\right)^2 = 16 - 8x^2 + x^4", r"V = \pi\int_{-2}^{2} \left(16 - 8x^2 + x^4\right) dx",
                      r"= 2\pi\left[16x - \tfrac{8x^3}{3} + \tfrac{x^5}{5}\right]_0^2", r"= 2\pi\left(32 - \tfrac{64}{3} + \tfrac{32}{5}\right)", r"= \tfrac{512\pi}{15} \approx 107.23"],
                     at=[1, 1, 2, 3, 4, 5, 5, 6, 6], figure=st, figure_at=1, follow=True, size=40, ref=REF_X,
                     cues={0: c["both"](c["draw"](0), c["axis"](), c["shade"]()), 2: c["both"](c["spin"](rt=1.4, sweep=3.0, hold=1.0), c["slice"](rt=1.0)),
                           3: c["both"](c["rad"](), lambda sc: sc.wait(0.8), c["flat"](rt=1.4))})

        # ---------------------------------------------------------------- vertical axes
        with self.beat("Vertical lines too") as b:
            st = about_one(scale=1.2)
            st.move_to(LEFT * 3.5 + DOWN * 0.1)
            c = rev_cues(st)
            board = VGroup(T("vertical axis: horizontal slices, integrate in $y$", 30),
                           M(r"R = (\text{axis}) - (\text{curve}) = 1 - y^2", 38, TANGENT)).arrange(DOWN, buff=0.5).move_to(RIGHT * 3.4 + UP * 0.3)
            self.play(FadeIn(st), run_time=0.6)
            c["draw"](0, rt=1.2)(self)
            c["axis"]()(self)
            c["shade"]()(self)
            b.line(1)
            c["spin"](rt=1.4, sweep=3.0, hold=0.6)(self)
            self.play(FadeIn(board[0]), run_time=0.6)
            c["slice"](rt=1.0)(self)
            b.line(2)
            c["rad"]()(self)
            self.play(Write(board[1]), run_time=1)
            c["flat"](rt=1.4)(self)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(formula_box(M(r"V = \pi\int R^2\ (dx \text{ or } dy)", 46, ACCUM), ACCUM), T("$R$ = distance from the axis to the curve: bigger $-$ smaller", 34),
                          M(r"\text{axis } y = k: \ R = |f(x) - k| \qquad \text{axis } x = k: \ R = |g(y) - k|", 36, SECANT)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c_) for c_ in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        # Example 1: sqrt x, y = 2 and the y-axis, about y = 2
        TWO = lambda s: 2.0
        st = rev_stage([(np.sqrt, 0, 4.6, FUNC, r"y = \sqrt x", (4.2, 1.45), "x")], region_outline(TWO, SQ, 0, 4), "x", 2.0, SQ, (-0.5, 5.0), (-0.5, 4.6),
                       at=1.2, shade=(TWO, SQ, 0, 4, "x"), axis_tex="y = 2", axis_lab=(4.55, 2.4), ticks={"x": [4], "y": [2, 4]}, scale=0.9, pose=(-36.0, 18.0))
        c = rev_cues(st)
        self.example("Example 1: About y = 2", r"The region bounded by $y = \sqrt x$, $y = 2$, and the $y$-axis is revolved about the line $y = 2$. Find the volume.",
                     [r"TEXT:Sketch: $y = \sqrt x$, the line $y = 2$, the region between", r"\sqrt x = 2 \text{ at } x = 4", r"TEXT:One slice at $x$: a disc centered on $y = 2$",
                      r"R = 2 - \sqrt x", r"R^2 = 4 - 4\sqrt x + x", r"V = \pi\int_0^4 \left(4 - 4\sqrt x + x\right) dx", r"= \pi\left[4x - \tfrac83x^{3/2} + \tfrac{x^2}{2}\right]_0^4",
                      r"= \pi\left(16 - \tfrac{64}{3} + 8\right)", r"= \tfrac{8\pi}{3} \approx 8.38"], at=[1, 1, 2, 2, 3, 3, 4, 4, 4], figure=st, figure_at=1, size=40, ref=REF_X,
                     cues={0: c["both"](c["draw"](0), c["axis"](), c["shade"]()), 2: c["both"](c["spin"](rt=1.4, sweep=2.8, hold=0.8), c["slice"](rt=1.0)),
                           3: c["both"](c["rad"](), lambda sc: sc.wait(0.6), c["flat"](rt=1.4))})
        # Example 2: x = y^2 and x = 1, about x = 1
        st = about_one()
        c = rev_cues(st)
        self.example("Example 2: About x = 1", r"The region bounded by $x = y^2$ and $x = 1$ is revolved about the line $x = 1$. Find the volume.",
                     [r"TEXT:Sketch: $x = y^2$ opens to the right; the line $x = 1$", r"y^2 = 1 \text{ at } y = \pm1", r"TEXT:One slice at $y$: a horizontal disc", r"R = 1 - y^2",
                      r"R^2 = 1 - 2y^2 + y^4", r"V = \pi\int_{-1}^{1} \left(1 - 2y^2 + y^4\right) dy", r"= 2\pi\left(1 - \tfrac23 + \tfrac15\right)", r"= \tfrac{16\pi}{15} \approx 3.35"],
                     at=[1, 1, 2, 2, 3, 4, 4, 4], figure=st, figure_at=1, size=42, ref=REF_Y,
                     cues={0: c["both"](c["draw"](0), c["axis"](), c["shade"]()), 2: c["both"](c["spin"](rt=1.4, sweep=2.8, hold=0.8), c["slice"](rt=1.0)),
                           3: c["both"](c["rad"](), lambda sc: sc.wait(0.6), c["flat"](rt=1.4))})
        # Example 3: under x^2 on [0, 1], about x = 1
        st = rev_stage([(PAR, 0, 1.15, FUNC, "y = x^2", (0.45, 1.05), "x")], outline_y(ONE, SQ, 0, 1), "y", 1.0, SQ, (-0.4, 2.4), (-0.4, 1.55),
                       at=0.4, shade=(ONE, SQ, 0, 1, "y"), axis_tex="x = 1", axis_lab=(1.45, 1.4), ticks={"x": [1, 2], "y": [1]}, scale=1.7, pose=(-26.0, 26.0), turn=-12.0)
        c = rev_cues(st)
        self.example("Example 3: A vertical axis on the right", r"The region bounded by $y = x^2$, the $x$-axis, and $x = 1$ is revolved about the line $x = 1$. Find the volume.",
                     [r"TEXT:Sketch: under $y = x^2$, from $x = 0$ to the line $x = 1$", r"TEXT:Horizontal slices, $0 \le y \le 1$; the curve is $x = \sqrt y$.", r"R = 1 - \sqrt y",
                      r"R^2 = 1 - 2\sqrt y + y", r"V = \pi\int_0^1 \left(1 - 2\sqrt y + y\right) dy", r"= \pi\left(1 - \tfrac43 + \tfrac12\right)", r"= \tfrac\pi6 \approx 0.52"],
                     at=[1, 2, 2, 3, 4, 4, 4], figure=st, figure_at=1, size=42, ref=REF_Y,
                     cues={0: c["both"](c["draw"](0), c["axis"](), c["shade"]()), 1: c["both"](c["spin"](rt=1.4, sweep=2.8, hold=0.8), c["slice"](rt=1.0)),
                           2: c["both"](c["rad"](), lambda sc: sc.wait(0.6), c["flat"](rt=1.4))})
        self.finish()
