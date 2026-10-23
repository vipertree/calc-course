"""Topic 8.11: Washer method about the axes. Narration comes from transcripts/8_11.md.

Adder's notes (2026-10-14, the same advice as 8.9/8.10): in the opening, first see the solid, watch the rotation, see
the solid from many angles, then slice it. The old washers were flat rings of one color with no depth, so the hollow
never read as a hollow: now the solid's inner wall is drawn darker with rings on it, so you can see into the bowl, the
axis runs through the hole, a quarter is cut away to show the wall, and the washer shows its inner wall from an angle.
Examples start from the student's sketch (curves, where they meet, the region), spin it once, then show ONE thin
washer at the x (or y) we care about with its R and r, found as distances from the axis to each curve, and go back to
the flat sketch. 3D pictures come from anim/solids.py (rev_stage / rev_cues).
"""
import numpy as np
from manim import *

from kit import *
from props import washing_machine
from solids import *
from style import *

LINE = lambda s: s
PAR = lambda s: s * s
SQ = lambda s: np.sqrt(max(s, 0.0))
TOP = lambda s: 1.7 + 0.35 * np.sin(1.3 * s)          # "One hollow solid": two wavy curves with a gap below them
BOT = lambda s: 0.8 + 0.18 * np.cos(1.6 * s)
X0 = 2.3
REF_X = r"V = \pi\int_a^b \left([R(x)]^2 - [r(x)]^2\right) dx"
REF_Y = r"V = \pi\int_c^d \left([R(y)]^2 - [r(y)]^2\right) dy"


def thickness(st, v, p):
    """The slice's thickness, a little double arrow over it, when it is seen edge on (param dx)."""
    if p["dx"] < 0.01:
        return []
    y = TOP(X0) + 0.25
    a = DoubleArrow(v.P(X0 - 0.075, 0, y), v.P(X0 + 0.075, 0, y), buff=0, color=INK, stroke_width=3, tip_length=0.1,
                    max_tip_length_to_length_ratio=0.45).shift(UP * 0.12)
    lab = st.label("dx", r"\Delta x", 30, INK).next_to(a, UP, buff=0.08)
    return [a.set_opacity(p["dx"]), lab.set_opacity(p["dx"])]


WOOD_GRAIN = "#9A6B3C"


def hardware_washer(stv):
    """8.11's real washer: a steel washer (the same radii ratio as the slice at X0) with a wood screw through it, in its
    own Stage. Params: drop (the screw above, 1 -> seated, 0), sop (its opacity), board (a board's opacity), rise (0 ->
    1: the board comes up and the screw turns into it), out (the screw backs out), tip (0: axis upright; 1: on edge,
    axis along x), go (0 -> 1: moves onto the slice of the hollow solid, drawn with stv["v"]), thin (to the slice's
    thickness), fade (its opacity)."""
    R0, r0 = TOP(X0), BOT(X0)
    rw = r0 / R0

    def draw(st_, v, drop, sop, board, rise, out, tip, go, thin, fade):
        tw = 0.12 + (0.15 / R0 - 0.12) * thin
        items = []
        zb = -tw / 2 - 2.0 * (1 - rise)
        if board > 0.01:
            bd = prism([(-1.5, zb - 0.45), (1.5, zb - 0.45), (1.5, zb), (-1.5, zb)], -1.8, 1.8, "x", color=WOOD_SIDE, cap_color=WOOD_SIDE,
                       side_color=WOOD, opacity=board)
            xs = np.linspace(-1.8, 1.8, 40)
            for f in bd.faces:                  # wood grain: thin wavy strips along the board, on its top and front
                if f.normal[2] > 0.9:
                    f.decor = [np.array([(x, y + 0.04 * np.sin(2.1 * x + 7 * y), zb + 1e-3) for x in xs] +
                                        [(x, y + 0.012 + 0.04 * np.sin(2.1 * x + 7 * y), zb + 1e-3) for x in xs[::-1]]) for y in (-1.2, -0.7, -0.15, 0.45, 1.0)]
                elif f.normal[1] < -0.9:
                    f.decor = [np.array([(x, -1.5 - 1e-3, z + 0.03 * np.sin(1.7 * x + 9 * z)) for x in xs] +
                                        [(x, -1.5 - 1e-3, z + 0.012 + 0.03 * np.sin(1.7 * x + 9 * z)) for x in xs[::-1]]) for z in (zb - 0.34, zb - 0.21, zb - 0.1)]
                f.decor_color = WOOD_GRAIN
            items.append(bd)
        w = washer(1.0, rw, 0.0, tw, axis="y", color=STEEL, inner_color=STEEL_DARK, opacity=fade)
        sc = []
        if sop > 0.01:
            sc = screw(tw / 2 + 1.4 * drop + 2.0 * out, turn=540 * rise - 540 * out, clip=zb if board > 0.01 else None, opacity=sop)
        if sc:
            items += [merge(w, sc[0], closed=True)] + sc[1:]
        else:
            items.append(w.moved(R=rot("y", 90 * tip), about=(0, 0, 0)) if tip > 1e-3 else w)
        if go > 1e-3 and "v" in stv:
            t = stv["v"]
            v = v.turned(origin=(1 - go) * v.origin + go * t.P(X0, 0, 0), scale=(1 - go) * v.scale + go * t.scale * R0)
        return items, v
    return Stage(draw, View(scale=1.9, yaw=-30, pitch=30), drop=1.0, sop=0.0, board=0.0, rise=0.0, out=0.0, tip=0.0, go=0.0, thin=0.0, fade=1.0)


def hollow_bowl(scale=1.6, at=0.6, pose=(-36.0, 18.0), turn=-24.0):
    """The region between y = x and y = x^2, about the x-axis: a cone outside, a bowl inside."""
    return rev_stage([(LINE, 0, 1.18, FUNC, "y = x", (0.55, 0.95), "x"), (PAR, 0, 1.1, FUNC, "y = x^2", (1.4, 0.75), "x")],
                     region_outline(LINE, PAR, 0, 1), "x", 0.0, LINE, (-0.3, 1.6), (-1.2, 1.45), at=at, shade=(LINE, PAR, 0, 1, "x"), hole=PAR,
                     ticks={"x": [1], "y": [1]}, scale=scale, pose=pose, turn=turn)


class Lesson(TranscriptScene):
    NUM = "8.11"

    def construct(self):
        # ---------------------------------------------------------------- cold open: a region with a gap sweeps a hollow solid
        with self.beat("A hollow solid") as b:
            st = hollow_bowl(scale=2.4)
            st.move_to(DOWN * 0.2)
            c = rev_cues(st)
            tag_at = RIGHT * 4.3 + UP * 2.2
            self.play(FadeIn(st), run_time=0.6)
            c["draw"](0, 1, rt=1.4)(self)
            c["shade"]()(self)
            b.line(1)
            c["spin"](rt=1.6, sweep=5.0, hold=0)(self)
            b.line(2)
            tag = T("from the outside", 34, DIM).move_to(tag_at)
            self.play(st.to("yaw", 42), st.to("pitch", 16), FadeIn(tag), run_time=3.2)
            self.play(st.spin(-14), run_time=2.2)
            b.line(3)
            new = T("looking in the open end", 34, DIM).move_to(tag_at)
            self.play(st.to("yaw", -62), st.to("pitch", 26), FadeOut(tag), FadeIn(new), run_time=3.4)
            tag = new
            self.play(st.spin(12), run_time=2.6)
            b.line(4)
            self.play(FadeOut(tag), st.spin(-14), run_time=3)
        self.clear()
        self.title()

        # ---------------------------------------------------------------- one hollow solid, slowly, from every side
        st = rev_stage([(TOP, 0, 4, FUNC, "y = f(x)", (4.55, 1.45), "x"), (BOT, 0, 4, FUNC, "y = g(x)", (4.55, 0.62), "x")],
                       region_outline(TOP, BOT, 0, 4, n=40), "x", 0.0, TOP, (-0.5, 5.0), (-2.3, 2.5), at=X0, shade=(TOP, BOT, 0, 4, "x"), hole=BOT,
                       ticks={"x": [1, 2, 3, 4]}, scale=1.15, pose=(-36.0, 18.0), turn=-20.0, d=0.15, extra=thickness, extra_params={"dx": 0.0})
        st.move_to(LEFT * 3.0 + DOWN * 0.2)
        tag_at = RIGHT * 3.9 + UP * 1.9
        with self.beat("One hollow solid") as b:
            self.play(FadeIn(st), run_time=0.6)
            self.play(st.to("c0", 1), st.to("c1", 1), run_time=1.6)
            self.play(st.to("shade", 1), run_time=0.8)
            b.line(1)
            self.play(st.to("yaw", -36), st.to("pitch", 18), st.to("fit", 1), run_time=2)
            tag = T("a quarter turn", 36, DIM).move_to(tag_at)
            self.play(st.to("sweep", 0.25), FadeIn(tag), run_time=2.4)
            b.line(2)
            new = T("halfway", 36, DIM).move_to(tag_at)
            self.play(st.to("sweep", 0.5), FadeOut(tag), FadeIn(new), run_time=1.6)
            tag = new
            new = T("all the way around", 36, DIM).move_to(tag_at)
            self.play(st.to("sweep", 1), FadeOut(tag), FadeIn(new), run_time=2.0)
            tag = new
            b.line(3)
            new = T("from the end", 36, DIM).move_to(tag_at)
            self.play(st.to("yaw", -90), st.to("pitch", 4), FadeOut(tag), FadeIn(new), run_time=3)
            tag = new
            self.wait(1.4)
            self.play(st.to("yaw", -62), st.to("pitch", 22), FadeOut(tag), run_time=2.6)
            self.play(st.spin(20), run_time=2.6)
            b.line(4)
            tag = T("a quarter cut away", 36, DIM).move_to(tag_at)
            self.play(st.to("yaw", -36), st.to("pitch", 20), run_time=1.6)
            self.play(st.to("wedge", 1), FadeIn(tag), run_time=2.2)
            self.play(st.spin(-14), run_time=2.6)
            self.wait(1.0)
            self.play(st.to("wedge", 0), FadeOut(tag), st.spin(14), run_time=1.8)

        # ---------------------------------------------------------------- slice it: one slice, from every side
        stv = {}
        draw0 = st.draw_fn

        def keep_view(s_, v_, **p_):            # the (zoomed) view the slice is drawn with, for lining up the hardware washer
            items, vv = draw0(s_, v_, **p_)
            stv["v"] = vv
            return items, vv
        st.draw_fn = keep_view
        with self.beat("One slice") as b:
            self.play(st.to("cut_line", 1), run_time=1.6)
            b.line(1)
            st.set("cut_line", 0)
            st.set("split", 1)
            self.play(st.to("cut", 1), run_time=1.6)
            self.play(st.to("pieces", 0), run_time=1.2)
            face = T("face on: a ring", 36, DIM).move_to(tag_at)
            self.play(st.to("yaw", -90), st.to("pitch", 4), FadeIn(face), run_time=2.2)
            self.wait(1.0)
            edge = T(r"edge on: thin", 36, DIM).move_to(tag_at)
            self.play(st.to("yaw", 0), st.to("pitch", 4), FadeOut(face), FadeIn(edge), run_time=2.2)
            self.play(st.to("dx", 1), run_time=0.6)
            self.wait(1.0)
            wall = T("at an angle: the wall of the hole", 32, DIM).move_to(tag_at)
            self.play(st.to("dx", 0), FadeOut(edge), FadeIn(wall), st.to("yaw", -58), st.to("pitch", 22), run_time=2.6)
            self.play(st.spin(-14), run_time=2.2)
            self.play(FadeOut(wall), st.to("yaw", -36), st.to("pitch", 18), run_time=1.6)

        # ---------------------------------------------------------------- what a washer is (Adder, 2026-10-23)
        with self.beat("What a washer is") as b:
            tag = T("a washer", 40, INK).move_to(tag_at)
            self.play(FadeIn(tag), run_time=0.8)
            b.line(1)
            wm = washing_machine(4.6).move_to(LEFT * 1.6 + DOWN * 0.1)
            new = T("not this washer", 36, TANGENT).move_to(tag_at)
            self.play(FadeOut(st), FadeOut(tag), run_time=0.6)
            self.play(FadeIn(wm, shift=UP * 0.2), FadeIn(new), run_time=0.9)
            tag = new
            b.line(2)
            hw = hardware_washer(stv)
            hw.move_to(LEFT * 1.5 + UP * 0.9)
            new = T("this washer", 36, INK).move_to(tag_at)
            self.play(FadeOut(wm), FadeOut(tag), run_time=0.6)
            self.play(FadeIn(hw), FadeIn(new), run_time=0.8)
            tag = new
            self.play(hw.to("sop", 1), hw.to("drop", 0), run_time=2.2)
            self.play(hw.spin(-30), run_time=2.6)
            b.line(3)
            new = T("from the side", 36, DIM).move_to(tag_at)
            self.play(hw.to("pitch", 7), hw.to("yaw", -24), hw.to("board", 1), FadeOut(tag), FadeIn(new), run_time=1.8)
            tag = new
            self.play(hw.to("rise", 1), run_time=3.0)
            self.wait(1.0)
            b.line(4)
            self.play(hw.to("out", 1), hw.to("sop", 0), FadeOut(tag), run_time=1.3)
            self.play(hw.to("board", 0), run_time=0.4)
            self.play(hw.to("tip", 1), hw.to("pitch", 18), hw.to("yaw", -36), run_time=1.6)
            b.line(5)
            new = T("the slice at $x$: the same shape", 32, DIM).move_to(tag_at)
            self.play(hw.to("go", 1), FadeIn(new), run_time=2.0)
            tag = new
            st.redraw(force=True)
            self.add(st)
            self.bring_to_front(hw)
            self.play(hw.to("thin", 1), run_time=0.6)
            self.play(hw.to("fade", 0), run_time=1.2)
            self.remove(hw)
            self.wait(1.0)
            self.play(FadeOut(tag), run_time=0.6)

        # ---------------------------------------------------------------- R and r, the area, the solid from washers
        with self.beat("Every slice is a washer") as b:
            st.set("solid", 0)
            st.set("split", 0)
            st.set("one", 1)
            self.play(st.to("solid", st.ghost), run_time=1.2)
            self.play(st.to("rad", 1), run_time=1.0)
            self.wait(0.6)
            self.play(st.to("rin", 1), run_time=1.0)
            b.line(1)
            b1 = M(r"A(x) = \pi R^2 - \pi r^2", 42)
            b2 = M(r"\text{one washer: } \pi\left(R^2 - r^2\right)\Delta x", 38)
            b3 = formula_box(M(r"V = \pi\int_a^b \left([R(x)]^2 - [r(x)]^2\right) dx", 40, ACCUM), ACCUM)
            b4 = VGroup(T("$R$ = distance from the axis to the outer edge", 26, DIM), T("$r$ = distance from the axis to the inner edge", 26, DIM)).arrange(DOWN, buff=0.15)
            board = VGroup(b1, b2, b3, b4).arrange(DOWN, buff=0.42).move_to(RIGHT * 3.6 + DOWN * 0.2)
            self.play(Write(b1), run_time=1)
            self.play(Write(b2), run_time=1)
            b.line(2)
            self.play(st.to("rad", 0), st.to("rin", 0), st.to("solid", 0), st.to("one", 0), run_time=0.8)
            st.set("solid", 1)
            tag = M("n = 8", 34, DIM).move_to(LEFT * 3.0 + UP * 3.3)
            self.play(st.to("many", 1), FadeIn(tag), run_time=0.8)
            self.wait(0.8)
            for n_ in (16, 40):
                new = M(f"n = {n_}", 34, DIM).move_to(tag)
                self.play(st.to("n", n_), FadeOut(tag), FadeIn(new), run_time=0.5)
                tag = new
                self.wait(0.8)
            new = T("smooth", 34, DIM).move_to(tag)
            self.play(st.to("smooth", 1), FadeOut(tag), FadeIn(new), run_time=0.6)
            self.play(FadeIn(b3), FadeIn(b4), run_time=1)
            self.play(st.spin(-18), run_time=3)
        self.clear()

        # ---------------------------------------------------------------- square each radius on its own
        with self.beat("Square each radius separately") as b:
            def two(st_, v):
                return [washer(3.0, 2.0, 0.0, 0.5, color=SECANT, inner_color=interpolate_color(ManimColor(SECANT), ManimColor(BG), 0.3)),
                        disc(1.0, 0.0, 0.5, color=TANGENT).moved(t=(0, 0, -6.4))]
            pic = Stage(two, View(scale=0.5, yaw=-56, pitch=16))
            pic.move_to(LEFT * 3.4 + DOWN * 0.1)
            self.play(FadeIn(pic), run_time=0.8)
            b.line(1)
            ring = VGroup(M(r"R = 3,\ r = 2", 36), M(r"\pi\left(3^2 - 2^2\right) = 5\pi", 40, SECANT)).arrange(DOWN, buff=0.25)
            ring.move_to(RIGHT * 2.6 + UP * 1.5)
            self.play(FadeIn(ring), run_time=1)
            b.line(2)
            wrong = VGroup(M(r"\pi\left(3 - 2\right)^2 = \pi", 40, TANGENT), T("a disc of radius 1", 30, DIM)).arrange(DOWN, buff=0.25)
            wrong.move_to(RIGHT * 2.6 + DOWN * 1.6)
            self.play(FadeIn(wrong), run_time=1)
            self.play(Write(M(r"(R - r)^2 \ne R^2 - r^2", 40, INK).next_to(wrong, DOWN, buff=0.5)), run_time=1)
        self.clear()

        # ---------------------------------------------------------------- the lesson example: sketch, spin, one washer
        st = hollow_bowl()
        c = rev_cues(st)
        self.example("Washers between a line and a parabola", r"The region between $y = x$ and $y = x^2$ is revolved about the $x$-axis. Find the volume.",
                     [r"TEXT:Sketch: the line, the parabola, the region between", r"x^2 = x \text{ at } x = 0 \text{ and } x = 1", r"TEXT:One slice at $x$: a washer",
                      r"TEXT:From the axis up to the line, the outer edge:", r"R(x) = x", r"TEXT:From the axis up to the parabola, the inner edge:", r"r(x) = x^2",
                      r"A(x) = \pi\left(x^2 - \left(x^2\right)^2\right) = \pi\left(x^2 - x^4\right)", r"V = \pi\int_0^1 \left(x^2 - x^4\right) dx",
                      r"= \pi\left[\tfrac{x^3}{3} - \tfrac{x^5}{5}\right]_0^1", r"= \pi\left(\tfrac13 - \tfrac15\right)", r"= \tfrac{2\pi}{15} \approx 0.42"],
                     at=[1, 1, 2, 3, 3, 4, 4, 5, 6, 6, 6, 6], figure=st, figure_at=1, follow=True, size=38, ref=REF_X,
                     cues={0: c["both"](c["draw"](0, 1), c["shade"]()), 2: c["both"](c["spin"](rt=1.4, sweep=3.0, hold=1.2), c["slice"](rt=1.2)),
                           3: c["rad"](), 5: c["both"](c["rin"](), lambda sc: sc.wait(1.0), c["flat"](rt=1.4))})

        # ---------------------------------------------------------------- the same region about the y-axis
        with self.beat("Around the y-axis") as b:
            st = rev_stage([(LINE, 0, 1.18, FUNC, "y = x", (0.55, 0.95), "x"), (PAR, 0, 1.1, FUNC, "y = x^2", (1.4, 0.75), "x")],
                           outline_y(SQ, LINE, 0, 1), "y", 0.0, SQ, (-1.3, 1.7), (-0.3, 1.45), at=0.3, shade=(SQ, LINE, 0, 1, "y"), hole=LINE,
                           ticks={"x": [-1, 1], "y": [1]}, scale=1.9, pose=(-24.0, 26.0), turn=-14.0)
            st.move_to(LEFT * 3.4 + DOWN * 0.2)
            c = rev_cues(st)
            self.play(FadeIn(st), run_time=0.6)
            c["draw"](0, 1, rt=1.2)(self)
            c["shade"](rt=0.6)(self)
            c["spin"](rt=1.6, sweep=3.0, hold=0)(self)
            b.line(1)
            self.play(st.spin(st.turn_by), run_time=1.0)
            board = VGroup(T("horizontal slices: integrate in $y$", 30), M(r"\text{line: } x = y, \ \ \text{parabola: } x = \sqrt y", 34),
                           T(r"at $y = \tfrac14$: the parabola is at $\tfrac12$, \\ the line at $\tfrac14$, so the parabola is farther out", 26, DIM),
                           M(r"R(y) = \sqrt y, \ \ r(y) = y", 38),
                           M(r"V = \pi\int_0^1 \left(y - y^2\right) dy = \tfrac\pi6", 36, ACCUM)).arrange(DOWN, buff=0.4).move_to(RIGHT * 3.4 + UP * 0.2)
            self.play(FadeIn(board[0]), run_time=0.6)
            c["slice"](rt=1.2)(self)
            self.play(Write(board[1]), run_time=0.8)
            b.line(2)
            self.play(FadeIn(board[2]), run_time=0.8)
            c["rad"]()(self)
            c["rin"]()(self)
            self.play(Write(board[3]), run_time=0.8)
            c["flat"](rt=1.6)(self)
            b.line(3)
            self.play(Write(board[4]), run_time=1)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(formula_box(M(r"V = \pi\int \left(R^2 - r^2\right)", 48, ACCUM), ACCUM), T("$R$: from the axis to the outer edge", 34),
                          T("$r$: from the axis to the edge of the hole", 34), T("square each radius separately", 34, TANGENT)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c_) for c_ in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        # Example 1: root x and x about the x-axis
        st = rev_stage([(SQ, 0, 1.15, FUNC, r"y = \sqrt x", (0.62, 1.12), "x"), (LINE, 0, 1.15, FUNC, "y = x", (0.95, 0.55), "x")],
                       region_outline(SQ, LINE, 0, 1), "x", 0.0, SQ, (-0.3, 1.6), (-1.2, 1.45), at=0.45, shade=(SQ, LINE, 0, 1, "x"), hole=LINE,
                       ticks={"x": [1], "y": [1]}, scale=1.6, pose=(-36.0, 18.0))
        c = rev_cues(st)
        self.example("Example 1: Root and line about the x-axis", r"The region between $y = \sqrt x$ and $y = x$ is revolved about the $x$-axis. Find the volume.",
                     [r"TEXT:Sketch: $y = \sqrt x$, $y = x$, the region between", r"\sqrt x = x \text{ at } x = 0 \text{ and } x = 1", r"TEXT:One slice at $x$: a washer",
                      r"R(x) = \sqrt x", r"r(x) = x", r"R^2 - r^2 = x - x^2", r"V = \pi\int_0^1 \left(x - x^2\right) dx", r"= \pi\left(\tfrac12 - \tfrac13\right)",
                      r"= \tfrac\pi6 \approx 0.52"], at=[1, 1, 2, 2, 2, 3, 3, 4, 4], figure=st, figure_at=1, size=40, ref=REF_X,
                     cues={0: c["both"](c["draw"](0, 1), c["shade"]()), 2: c["both"](c["spin"](rt=1.4, sweep=2.8, hold=1.0), c["slice"](rt=1.0)),
                           3: c["rad"](), 4: c["both"](c["rin"](), lambda sc: sc.wait(0.6), c["flat"](rt=1.4))})
        # Example 2: Rowan's napkin ring, 4 - x^2 and y = 3 about the x-axis
        P4 = lambda s: 4 - s * s
        THREE = lambda s: 3.0
        st = rev_stage([(P4, -1.35, 1.35, FUNC, "y = 4 - x^2", (1.55, 4.15), "x"), (THREE, -1.6, 1.6, FUNC, "y = 3", (-1.95, 2.7), "x")],
                       region_outline(P4, THREE, -1, 1), "x", 0.0, P4, (-2.0, 2.0), (-0.5, 4.7), at=0.4, shade=(P4, THREE, -1, 1, "x"), hole=THREE,
                       ticks={"x": [-1, 1]}, scale=0.95, pose=(-40.0, 16.0), turn=-16.0)
        c = rev_cues(st)
        self.example("Example 2: A napkin ring", r"Rowan is turning a napkin ring on a lathe. Its shape is the region between $y = 4 - x^2$ and $y = 3$, revolved about the $x$-axis (in centimeters). How much wood is in the ring?",
                     [r"TEXT:Sketch: the parabola, the line $y = 3$, the region between", r"4 - x^2 = 3 \text{ at } x = \pm 1", r"TEXT:One slice at $x$: a washer",
                      r"R(x) = 4 - x^2", r"r(x) = 3", r"R^2 - r^2 = \left(16 - 8x^2 + x^4\right) - 9", r"= 7 - 8x^2 + x^4", r"V = \pi\int_{-1}^{1} \left(7 - 8x^2 + x^4\right) dx",
                      r"= 2\pi\left(7 - \tfrac83 + \tfrac15\right)", r"= \tfrac{136\pi}{15} \approx 28.48 \text{ cm}^3"], at=[1, 1, 2, 3, 3, 4, 4, 5, 5, 5], figure=st, figure_at=1, size=38, ref=REF_X,
                     cues={0: c["both"](c["draw"](0, 1), c["shade"]()), 2: c["both"](c["spin"](rt=1.4, sweep=2.8, hold=1.0), c["slice"](rt=1.0)),
                           3: c["rad"](), 4: c["both"](c["rin"](), lambda sc: sc.wait(0.6), c["flat"](rt=1.4))})
        # Example 3: 2x and x^2 about the y-axis
        HALF = lambda s: s / 2
        st = rev_stage([(lambda s: 2 * s, 0, 2.1, FUNC, "y = 2x", (0.95, 3.6), "x"), (PAR, 0, 2.1, FUNC, "y = x^2", (2.75, 3.3), "x")],
                       outline_y(SQ, HALF, 0, 4), "y", 0.0, SQ, (-2.7, 3.2), (-0.5, 4.9), at=1.0, shade=(SQ, HALF, 0, 4, "y"), hole=HALF,
                       ticks={"x": [-2, 2], "y": [4]}, scale=0.95, pose=(-24.0, 26.0), turn=-12.0)
        c = rev_cues(st)
        self.example("Example 3: About the y-axis", r"The region between $y = 2x$ and $y = x^2$ is revolved about the $y$-axis. Find the volume.",
                     [r"TEXT:Sketch: the line, the parabola, the region between", r"2x = x^2 \text{ at } x = 0 \text{ and } x = 2\text{, so } 0 \le y \le 4",
                      r"TEXT:Horizontal washers: integrate in $y$.", r"\text{line: } x = \tfrac y2, \ \ \text{parabola: } x = \sqrt y",
                      r"TEXT:At $y = 1$: $\sqrt 1 = 1$ is farther out than $\tfrac12$.", r"R(y) = \sqrt y, \ \ r(y) = \tfrac y2",
                      r"V = \pi\int_0^4 \left(y - \tfrac{y^2}{4}\right) dy", r"= \pi\left(8 - \tfrac{16}{3}\right)", r"= \tfrac{8\pi}{3} \approx 8.38"],
                     at=[1, 1, 2, 2, 3, 3, 4, 4, 4], figure=st, figure_at=1, size=40, ref=REF_Y,
                     cues={0: c["both"](c["draw"](0, 1), c["shade"]()), 2: c["both"](c["spin"](rt=1.4, sweep=2.8, hold=1.0), c["slice"](rt=1.0)),
                           4: c["both"](c["rad"](), c["rin"](), lambda sc: sc.wait(0.6), c["flat"](rt=1.4))})
        self.finish()
