"""Topic 8.12: Washer method about other axes. Narration comes from transcripts/8_12.md.

Adder's notes (2026-10-14, the same advice as 8.9-8.11): the opening shows the solid first, the rotation, the solid
from many angles, then how we slice it; washers and the hollow read as 3D (the inner wall drawn darker with rings on
it, the axis through the hole). Examples sketch the curves, where they meet and the region, draw the axis, spin once,
show ONE thin washer at the x (or y) we care about with its R and r, then go back to the flat sketch. No "bigger minus
smaller" rule: each radius is measured on the picture from the axis to its curve, with the arithmetic justified in
words ("the axis is one unit below the x-axis, so the distance up to the line is x + 1"). 3D pictures come from
anim/solids.py (rev_stage / rev_cues).
"""
import numpy as np
from manim import *

from kit import *
from solids import *
from style import *

LINE = lambda s: s
PAR = lambda s: s * s
SQ = lambda s: np.sqrt(max(s, 0.0))
REF_X = r"V = \pi\int_a^b \left([R(x)]^2 - [r(x)]^2\right) dx"
REF_Y = r"V = \pi\int_c^d \left([R(y)]^2 - [r(y)]^2\right) dy"


def gap(st, v, p):
    """The one-unit gap between the axis y = -1 and the x-axis, as a little labeled double arrow (param gap)."""
    if p["gap"] < 0.01 or p["fit"] > 0.5:
        return []
    a = DoubleArrow(v.P(1.35, 0, -1), v.P(1.35, 0, 0), buff=0, color=DIM, stroke_width=3, tip_length=0.1, max_tip_length_to_length_ratio=0.3)
    lab = st.label("gap", "1", 28, DIM).next_to(a, RIGHT, buff=0.1)
    return [a.set_opacity(p["gap"]), lab.set_opacity(p["gap"])]


def below(scale=1.7, at=0.7, pose=(-36.0, 18.0), turn=-22.0, extra=None, extra_params=None):
    """The region between y = x and y = x^2, with the axis y = -1 below it."""
    return rev_stage([(LINE, 0, 1.18, FUNC, "y = x", (0.55, 0.95), "x"), (PAR, 0, 1.1, FUNC, "y = x^2", (1.4, 0.75), "x")],
                     region_outline(LINE, PAR, 0, 1), "x", -1.0, LINE, (-0.4, 1.7), (-1.5, 1.45), at=at, shade=(LINE, PAR, 0, 1, "x"), hole=PAR,
                     axis_tex="y = -1", axis_lab=(1.45, -1.25), ticks={"x": [1], "y": [1]}, scale=scale, pose=pose, turn=turn,
                     extra=extra, extra_params=extra_params, lab_at=0.3)


class Lesson(TranscriptScene):
    NUM = "8.12"

    def construct(self):
        # ---------------------------------------------------------------- cold open: the axis moves off the region
        with self.beat("Moving the axis") as b:
            st = below(scale=2.0)
            st.move_to(DOWN * 0.2)
            c = rev_cues(st)
            tag_at = RIGHT * 4.4 + UP * 2.2
            self.play(FadeIn(st), run_time=0.6)
            c["draw"](0, 1, rt=1.4)(self)
            c["shade"]()(self)
            c["axis"]()(self)
            b.line(1)
            c["spin"](rt=1.6, sweep=4.4, hold=0)(self)
            self.play(st.spin(-14), run_time=1.4)
            b.line(2)
            tag = T("from the end", 34, DIM).move_to(tag_at)
            self.play(st.to("yaw", -90), st.to("pitch", 4), FadeIn(tag), run_time=3)
            self.wait(1.4)
            new = T("into the hole", 34, DIM).move_to(tag_at)
            self.play(st.to("yaw", -60), st.to("pitch", 24), FadeOut(tag), FadeIn(new), run_time=2.6)
            tag = new
            self.play(st.spin(14), run_time=2.4)
            b.line(3)
            self.play(FadeOut(tag), st.to("yaw", -36), st.to("pitch", 18), run_time=1.6)
            c["slice"](rt=1.4)(self)
            c["rad"]()(self)
            c["rin"]()(self)
            self.play(st.spin(-12), run_time=2.4)
        self.clear()
        self.title()

        # ---------------------------------------------------------------- every radius starts at the axis
        with self.beat("Measuring from the axis") as b:
            st = below(scale=1.6, extra=gap, extra_params={"gap": 0.0})
            st.move_to(LEFT * 3.4 + DOWN * 0.1)
            c = rev_cues(st)
            self.play(FadeIn(st), run_time=0.6)
            c["draw"](0, 1, rt=1.2)(self)
            c["shade"](rt=0.6)(self)
            c["axis"]()(self)
            b.line(1)
            c["rad"](rt=1.0)(self)
            R = M(r"R(x) = x + 1", 42, TANGENT)
            Rw = T(r"the axis is $1$ below the $x$-axis, \\ and the line is $x$ above it", 26, DIM)
            r_ = M(r"r(x) = x^2 + 1", 42, DERIV)
            rw = T(r"$1$ up to the $x$-axis, \\ then $x^2$ up to the parabola", 26, DIM)
            last = T(r"find each radius on the picture: \\ from the axis to the curve", 30, INK)
            board = VGroup(VGroup(R, Rw).arrange(DOWN, buff=0.15), VGroup(r_, rw).arrange(DOWN, buff=0.15), last).arrange(DOWN, buff=0.55).move_to(RIGHT * 3.4 + DOWN * 0.1)
            self.play(st.to("gap", 1), run_time=0.8)
            self.play(Write(R), FadeIn(Rw), run_time=1)
            b.line(2)
            c["rin"](rt=1.0)(self)
            self.play(Write(r_), FadeIn(rw), run_time=1)
            b.line(3)
            self.play(st.to("gap", 0), run_time=0.4)
            c["spin"](rt=1.4, sweep=3.0, hold=0.4)(self)
            c["slice"](rt=1.2)(self)
            self.wait(0.4)
            c["flat"](rt=1.4)(self)
            b.line(4)
            self.play(FadeIn(last), run_time=1)
        self.clear()

        # ---------------------------------------------------------------- the lesson example
        st = below()
        c = rev_cues(st)
        self.example("About y = −1", r"The region between $y = x$ and $y = x^2$ is revolved about the line $y = -1$. Find the volume.",
                     [r"TEXT:Sketch: the line, the parabola, the region between; the axis $y = -1$", r"x^2 = x \text{ at } x = 0 \text{ and } x = 1",
                      r"TEXT:One slice at $x$: a washer centered on $y = -1$", r"TEXT:Up to the line: $1$ to the $x$-axis, then $x$ more:", r"R(x) = x + 1",
                      r"TEXT:Up to the parabola:", r"r(x) = x^2 + 1", r"R^2 = x^2 + 2x + 1", r"r^2 = x^4 + 2x^2 + 1", r"R^2 - r^2 = 2x - x^2 - x^4",
                      r"V = \pi\int_0^1 \left(2x - x^2 - x^4\right) dx", r"= \pi\left(1 - \tfrac13 - \tfrac15\right)", r"= \tfrac{7\pi}{15} \approx 1.47"],
                     at=[1, 1, 2, 3, 3, 4, 4, 5, 5, 6, 7, 7, 7], figure=st, figure_at=1, follow=True, size=38, ref=REF_X,
                     cues={0: c["both"](c["draw"](0, 1), c["shade"](), c["axis"]()), 2: c["both"](c["spin"](rt=1.4, sweep=3.0, hold=1.0), c["slice"](rt=1.2)),
                           3: c["rad"](), 5: c["both"](c["rin"](), lambda sc: sc.wait(1.0), c["flat"](rt=1.4))})

        # ---------------------------------------------------------------- the axis above the region
        with self.beat("An axis above the region") as b:
            st = rev_stage([(LINE, 0, 1.18, FUNC, "y = x", (0.55, 0.95), "x"), (PAR, 0, 1.1, FUNC, "y = x^2", (1.4, 0.75), "x")],
                           region_outline(LINE, PAR, 0, 1), "x", 2.0, PAR, (-0.4, 1.7), (-0.4, 2.6), at=0.55, shade=(LINE, PAR, 0, 1, "x"), hole=LINE,
                           axis_tex="y = 2", axis_lab=(1.4, 2.25), ticks={"x": [1], "y": [1]}, scale=1.7, pose=(-36.0, 18.0), turn=-20.0)
            st.move_to(LEFT * 3.4 + DOWN * 0.1)
            c = rev_cues(st)
            self.play(FadeIn(st), run_time=0.6)
            c["draw"](0, 1, rt=1.0)(self)
            c["shade"](rt=0.6)(self)
            c["axis"]()(self)
            c["spin"](rt=1.4, sweep=3.0, hold=0)(self)
            b.line(1)
            c["slice"](rt=1.2)(self)
            board = VGroup(T(r"the axis is above both curves, \\ so each distance down is $2$ minus the height", 26, DIM),
                           M(r"R(x) = 2 - x^2", 40, TANGENT), M(r"r(x) = 2 - x", 40, DERIV), T("now the parabola is farther", 28, DIM),
                           M(r"V = \pi\int_0^1 \left(\left(2 - x^2\right)^2 - (2 - x)^2\right) dx", 32),
                           M(r"= \pi\int_0^1 \left(x^4 - 5x^2 + 4x\right) dx = \tfrac{8\pi}{15}", 32, ACCUM)).arrange(DOWN, buff=0.32).move_to(RIGHT * 3.3 + DOWN * 0.1)
            b.line(2)
            self.play(FadeIn(board[0]), run_time=0.8)
            c["rad"]()(self)
            self.play(Write(board[1]), run_time=0.8)
            b.line(3)
            c["rin"]()(self)
            self.play(Write(board[2]), FadeIn(board[3]), run_time=0.8)
            c["flat"](rt=1.4)(self)
            b.line(4)
            self.play(Write(board[4]), run_time=1)
            self.play(Write(board[5]), run_time=1)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(formula_box(M(r"V = \pi\int \left(R^2 - r^2\right)", 48, ACCUM), ACCUM), T("both radii start at the axis", 34),
                          T("find each on the picture: from the axis to its curve", 34, SECANT), T("which curve is outer depends on where the axis is", 34, DIM)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c_) for c_ in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        # Example 1: the same region about x = -1
        st = rev_stage([(LINE, 0, 1.18, FUNC, "y = x", (0.55, 0.95), "x"), (PAR, 0, 1.1, FUNC, "y = x^2", (1.4, 0.75), "x")],
                       outline_y(SQ, LINE, 0, 1), "y", -1.0, SQ, (-1.6, 1.7), (-0.4, 1.5), at=0.35, shade=(SQ, LINE, 0, 1, "y"), hole=LINE,
                       axis_tex="x = -1", axis_lab=(-1.42, 1.3), ticks={"x": [-1, 1], "y": [1]}, scale=1.7, pose=(-24.0, 26.0), turn=-12.0)
        c = rev_cues(st)
        self.example("Example 1: About x = −1", r"The region between $y = x$ and $y = x^2$ is revolved about the line $x = -1$. Find the volume.",
                     [r"TEXT:Sketch: the line, the parabola, the region; the axis $x = -1$", r"TEXT:Vertical axis: horizontal washers, $0 \le y \le 1$",
                      r"\text{line: } x = y, \ \ \text{parabola: } x = \sqrt y", r"TEXT:The axis is $1$ left of the $y$-axis, so each radius is $1$ more than the curve's $x$:",
                      r"R(y) = \sqrt y + 1, \ \ r(y) = y + 1", r"R^2 - r^2 = \left(y + 2\sqrt y + 1\right) - \left(y^2 + 2y + 1\right)", r"= 2\sqrt y - y - y^2",
                      r"V = \pi\int_0^1 \left(2\sqrt y - y - y^2\right) dy", r"= \pi\left(\tfrac43 - \tfrac12 - \tfrac13\right)", r"= \tfrac\pi2 \approx 1.57"],
                     at=[1, 2, 2, 3, 3, 4, 4, 5, 5, 5], figure=st, figure_at=1, size=38, ref=REF_Y,
                     cues={0: c["both"](c["draw"](0, 1), c["shade"](), c["axis"]()), 1: c["both"](c["spin"](rt=1.4, sweep=2.8, hold=0.8), c["slice"](rt=1.0)),
                           3: c["both"](c["rad"](), c["rin"](), lambda sc: sc.wait(0.6), c["flat"](rt=1.4))})
        # Example 2: x^2 and y = 4 about y = -2
        FOUR = lambda s: 4.0
        st = rev_stage([(PAR, -2.15, 2.15, FUNC, "y = x^2", (2.55, 3.4), "x"), (FOUR, -2.5, 2.5, FUNC, "y = 4", (-1.0, 4.4), "x")],
                       region_outline(FOUR, PAR, -2, 2), "x", -2.0, FOUR, (-2.8, 3.0), (-2.6, 4.9), at=0.8, shade=(FOUR, PAR, -2, 2, "x"), hole=PAR,
                       axis_tex="y = -2", axis_lab=(1.9, -2.35), ticks={"x": [-2, 2]}, scale=0.62, pose=(-40.0, 16.0), turn=-16.0)
        c = rev_cues(st)
        self.example("Example 2: About y = −2", r"The region between $y = x^2$ and $y = 4$ is revolved about the line $y = -2$. Find the volume.",
                     [r"TEXT:Sketch: the parabola, the line $y = 4$, the region; the axis $y = -2$", r"x^2 = 4 \text{ at } x = \pm 2", r"TEXT:One slice at $x$: a washer centered on $y = -2$",
                      r"TEXT:The axis is $2$ below the $x$-axis, so each radius is the height plus $2$:", r"R(x) = 4 + 2 = 6, \ \ r(x) = x^2 + 2",
                      r"R^2 - r^2 = 36 - \left(x^4 + 4x^2 + 4\right)", r"= 32 - 4x^2 - x^4", r"V = \pi\int_{-2}^{2} \left(32 - 4x^2 - x^4\right) dx",
                      r"= 2\pi\left(64 - \tfrac{32}{3} - \tfrac{32}{5}\right)", r"= \tfrac{1408\pi}{15} \approx 294.89"], at=[1, 1, 2, 3, 3, 4, 4, 5, 5, 5], figure=st, figure_at=1, size=38, ref=REF_X,
                     cues={0: c["both"](c["draw"](0, 1), c["shade"](), c["axis"]()), 2: c["both"](c["spin"](rt=1.4, sweep=2.8, hold=0.8), c["slice"](rt=1.0)),
                           3: c["both"](c["rad"](), c["rin"](), lambda sc: sc.wait(0.6), c["flat"](rt=1.4))})
        # Example 3: root x and x/2 about y = 3
        HALF = lambda s: s / 2
        st = rev_stage([(SQ, 0, 4.4, FUNC, r"y = \sqrt x", (3.2, 2.15), "x"), (HALF, 0, 4.5, FUNC, r"y = \tfrac x2", (4.4, 1.75), "x")],
                       region_outline(SQ, HALF, 0, 4), "x", 3.0, HALF, (-0.4, 5.0), (-0.4, 3.6), at=1.4, shade=(SQ, HALF, 0, 4, "x"), hole=SQ,
                       axis_tex="y = 3", axis_lab=(4.4, 3.3), ticks={"x": [4], "y": [2]}, scale=0.95, pose=(-36.0, 16.0), turn=-16.0)
        c = rev_cues(st)
        self.example("Example 3: About y = 3", r"The region between $y = \sqrt x$ and $y = \frac x2$ is revolved about the line $y = 3$. Find the volume.",
                     [r"TEXT:Sketch: $y = \sqrt x$, $y = \frac x2$, the region; the axis $y = 3$", r"\sqrt x = \tfrac x2 \text{ at } x = 0 \text{ and } x = 4",
                      r"TEXT:One slice at $x$: a washer centered on $y = 3$", r"TEXT:The axis is above both curves, so each distance down is $3$ minus the height:",
                      r"R(x) = 3 - \tfrac x2, \ \ r(x) = 3 - \sqrt x", r"R^2 - r^2 = \left(9 - 3x + \tfrac{x^2}{4}\right) - \left(9 - 6\sqrt x + x\right)",
                      r"= \tfrac{x^2}{4} - 4x + 6\sqrt x", r"V = \pi\int_0^4 \left(\tfrac{x^2}{4} - 4x + 6\sqrt x\right) dx", r"= \pi\left(\tfrac{16}{3} - 32 + 32\right)",
                      r"= \tfrac{16\pi}{3} \approx 16.76"], at=[1, 1, 2, 3, 3, 4, 4, 5, 5, 5], figure=st, figure_at=1, size=38, ref=REF_X,
                     cues={0: c["both"](c["draw"](0, 1), c["shade"](), c["axis"]()), 2: c["both"](c["spin"](rt=1.4, sweep=2.8, hold=0.8), c["slice"](rt=1.0)),
                           3: c["both"](c["rad"](), c["rin"](), lambda sc: sc.wait(0.6), c["flat"](rt=1.4))})
        self.finish()
