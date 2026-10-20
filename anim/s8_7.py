"""Topic 8.7: Volumes with square and rectangle cross sections. Narration comes from transcripts/8_7.md.

Adder's notes (2026-10-14): the bread opening is a real 3D loaf seen at an angle, and a slice is pulled out of it. After
the title, a proper introduction: this is one type of volume problem (known cross sections perpendicular to an axis),
the same base with different shapes standing on it, the area of one slice, and the volume as the sum of infinitely many
thin slices, shown with more and more slabs until the stack looks smooth. Every example sketches the base flat first,
as a student would, then tilts to the angled view to see the sections, then tilts back: on paper only the base is drawn.
3D pictures come from anim/solids.py.
"""
import numpy as np
from manim import *

from kit import *
from solids import *
from style import *

ZERO = lambda s: 0.0
F = lambda s: 1.2 + 0.5 * np.sin(1.2 * s)          # the intro's base: under y = f(x), 0 <= x <= 4
SQ = lambda s: np.sqrt(max(s, 0.0))
KINDS = [("square", None, ACCUM, r"\text{squares}"), ("rect", 1.0, DERIV, r"\text{rectangles, height } 1"),
         ("equilateral", None, SECANT, r"\text{triangles}"), ("semicircle", None, TANGENT, r"\text{semicircles}")]


def pulled_slice(sl, k, v, pull, turn):
    """Slice k of the loaf lifted out (pull 0 -> 1), then carried forward and to the right, bigger (pull 1 -> 2), and
    turned toward the viewer (turn 0 -> 1)."""
    lift, go = min(pull, 1.0), max(pull - 1.0, 0.0)
    w = v.toward()
    phi = np.degrees(np.arctan2(w[1], w[0]))
    R = rot("z", phi * 0.3 * turn) * (1 + 0.5 * go)
    return sl[k].moved(R=R, t=(6.4 * go, -0.6 * lift - 1.4 * go, 1.5 * lift - 0.6 * go))


class Lesson(TranscriptScene):
    NUM = "8.7"

    def construct(self):
        # ---------------------------------------------------------------- cold open: a real loaf, one slice pulled out
        with self.beat("Slicing a loaf") as b:
            K = 6

            def loaf(st, v, gap, pull, turn):
                sl = bread_slices(-2.4, 2.4, 10, gap=gap, w=2.0, h=1.15, dome=0.62)
                if pull > 0:
                    sl[K] = pulled_slice(sl, K, v, pull, turn)
                return [cutting_board(-2.9, 2.9, -1.5, 1.5), *sl]
            st = Stage(loaf, View(origin=LEFT * 4.0 + DOWN * 0.6, scale=1.05, yaw=-38, pitch=22), gap=0, pull=0, turn=0)
            self.play(FadeIn(st), run_time=1)
            self.play(st.to("gap", 0.14), run_time=1.6)
            b.line(1)
            self.play(st.to("pull", 1), run_time=1.4)
            self.play(st.to("pull", 2), st.to("turn", 1), run_time=1.8)
            v = st.view()
            sl = pulled_slice(bread_slices(-2.4, 2.4, 10, gap=0.14, w=2.0, h=1.15, dome=0.62), K, v, 2, 1)
            front, back = sl.faces[1], sl.faces[0]
            if front.normal @ v.toward() < 0:
                front, back = back, front
            A = M("A", 52, INK).move_to(v.P(front.pts.mean(axis=0)) + UP * 0.1)
            # the thickness along the bottom edge on the side that shows
            fp, bp = v.P(front.pts), v.P(back.pts)
            low = np.where(fp[:, 1] < fp[:, 1].min() + 0.25)[0]
            i = int(low[np.argmax(np.linalg.norm(fp[low] - bp[low], axis=1))])
            thick = nudge_arrow(fp[i] + DOWN * 0.3, bp[i] + DOWN * 0.3, label=r"\text{thickness}", side=DOWN)
            board = M(r"\text{volume of a slice} \approx \text{area of its face} \times \text{thickness}", 40).to_edge(UP, buff=0.6)
            self.play(FadeIn(A), FadeIn(thick), run_time=0.8)
            self.play(Write(board), run_time=1.2)
            b.line(2)
            self.play(Indicate(board, color=SECANT), run_time=1.2)
        self.clear()
        self.title()

        # ---------------------------------------------------------------- what kind of problem this is
        with self.beat("One kind of volume problem") as b:
            head = T("Volume with known cross sections", 46).to_edge(UP, buff=0.4)

            def intro(st, v, curve, shade, seg, one, kind):
                out = list(floor_axes(st, v, (-0.4, 4.8), (-0.4, 2.4), ticks={"x": [1, 2, 3, 4], "y": [1, 2]}))
                if shade > 0:
                    out.append(floor_region(v, F, ZERO, 0, 4, opacity=0.35 * shade))
                if curve > 0.01:
                    out.append(floor_curve(v, F, 0, 4.3 * curve))
                if curve > 0.98:
                    out.append(st.label("f", "y = f(x)", 30, FUNC).move_to(v.P(4.35, 2.15, 0)))
                if seg > 0.01:
                    out.append(floor_segment(v, F, ZERO, 2.0).set_stroke(opacity=seg))
                if one > 0.01:
                    kd, h, col, _ = KINDS[int(kind)]
                    out.append(slab(kd, F, ZERO, 2.0, 0.22, color=col, height=h, rise=one))
                return out
            st = Stage(intro, View(origin=LEFT * 5.4 + DOWN * 2.0, scale=1.75, yaw=0, pitch=90), curve=0, shade=0, seg=0, one=0, kind=0)
            self.play(FadeIn(head), FadeIn(st), run_time=0.8)
            b.line(1)
            self.play(st.to("curve", 1), run_time=1.6)
            base = T("the base", 36, AREA).move_to(RIGHT * 4.8 + UP * 1.0)
            self.play(st.to("shade", 1), FadeIn(base), run_time=1)
            b.line(2)
            self.play(FadeOut(base), st.to("yaw", -30), st.to("pitch", 24), run_time=2.4)
            self.play(st.to("seg", 1), run_time=0.8)
            b.line(3)
            name = T(r"square", 38, ACCUM).move_to(RIGHT * 4.6 + UP * 1.4)
            self.play(st.to("one", 1), FadeIn(name), run_time=1.2)
            for i in (1, 2, 3):
                new = T([r"rectangle, height 1", r"triangle", r"semicircle"][i - 1], 36, KINDS[i][2]).move_to(name)
                self.play(st.to("one", 0), FadeOut(name), run_time=0.5)
                st.set("kind", i)
                self.play(st.to("one", 1), FadeIn(new), run_time=0.9)
                name = new
                self.wait(0.3)
        self.clear()

        # ---------------------------------------------------------------- one base, four solids
        with self.beat("Same base, different solids") as b:
            def solid_of(i):
                kd, h, col, _ = KINDS[i]

                def draw(st, v, rise):
                    out = list(floor_axes(st, v, (-0.4, 4.6), (-0.4, 2.2), labels=False))
                    out.append(floor_region(v, F, ZERO, 0, 4, opacity=0.35))
                    out.append(floor_curve(v, F, 0, 4))
                    if rise > 0.01:
                        out.append(section_solid(kd, F, ZERO, 0, 4, n=36, color=col, height=h, m=16, rise=rise))
                    return out
                return Stage(draw, View(scale=1.0, yaw=-30, pitch=24), rise=0)
            stages = [solid_of(i) for i in range(4)]
            cells = []
            for i, s in enumerate(stages):
                s.reserve({"rise": 1, "yaw": -30}, {"rise": 1, "yaw": 15})
                cells.append(Group(s, M(KINDS[i][3], 32, KINDS[i][2])).arrange(DOWN, buff=0.15))
            grid = Group(*cells).arrange_in_grid(2, 2, buff=(1.0, 0.3)).move_to(LEFT * 0.6 + UP * 0.1)
            for c in cells:
                c[1].next_to(c[0], DOWN, buff=0.1)
            self.play(*[FadeIn(c) for c in cells], run_time=1)
            b.line(1)
            for s in stages:
                self.play(s.to("rise", 1), run_time=1.1)
            self.play(*[s.spin(45) for s in stages], run_time=3.5)
            b.line(2)
            box = SurroundingRectangle(Group(cells[0], cells[1]), color=SECANT, buff=0.12, corner_radius=0.1)
            nxt = T(r"next lesson", 30, DIM).next_to(Group(cells[2], cells[3]), RIGHT, buff=0.25)
            self.play(Create(box), run_time=0.8)
            self.play(FadeIn(nxt), run_time=0.6)
        self.clear()

        # ---------------------------------------------------------------- the volume is a sum of thin slices
        with self.beat("Volume is a sum of slices") as b:
            def squares(st, v, n, lift, smooth, hl):
                out = list(floor_axes(st, v, (-0.4, 4.7), (-0.4, 2.2), ticks={"x": [4]}))
                out.append(floor_region(v, F, ZERO, 0, 4, opacity=0.35))
                if smooth > 0.5:
                    out.append(section_solid("square", F, ZERO, 0, 4, n=60))
                    return out
                nn = int(round(n))
                sl = slabs("square", F, ZERO, 0, 4, nn, gap=0.18 if nn < 30 else 0.0)
                if hl > 0.5:
                    k = nn // 2
                    sl[k] = sl[k].recolor(SECANT).moved(t=(0, -0.6 * lift, 2.1 * lift))
                out += sl
                return out
            st = Stage(squares, View(origin=LEFT * 5.8 + DOWN * 2.3, scale=1.6, yaw=-32, pitch=22), n=8, lift=0, smooth=0, hl=1)
            self.play(FadeIn(st), run_time=0.8)
            self.play(st.to("lift", 1), run_time=1.2)
            v = st.view()
            one = slabs("square", F, ZERO, 0, 4, 8, gap=0.18)[4].moved(t=(0, -0.6, 2.1))
            cap = max(one.faces[:2], key=lambda f: f.normal @ v.toward())
            other = one.faces[0] if cap is one.faces[1] else one.faces[1]
            Ax, dx = face_labels(v, cap, other, "A(x)", r"\Delta x")
            b1 = M(r"\text{volume of one slab} \approx A(x)\,\Delta x", 36).to_corner(UR, buff=0.4)
            self.play(FadeIn(Ax), FadeIn(dx), run_time=0.8)
            self.play(Write(b1), run_time=1)
            b.line(1)
            self.play(FadeOut(Ax), FadeOut(dx), st.to("lift", 0), run_time=0.8)
            st.set("hl", 0)
            tag = M("n = 8", 34, DIM).next_to(b1, DOWN, buff=0.5)
            for n in (4, 8, 16, 40):
                new = M(f"n = {n}", 34, DIM).move_to(tag)
                self.play(st.to("n", n), FadeOut(tag), FadeIn(new), run_time=0.5)
                tag = new
                self.wait(1.0)
            new = T("smooth", 34, DIM).move_to(tag)
            self.play(st.to("smooth", 1), FadeOut(tag), FadeIn(new), run_time=0.6)
            tag = new
            b.line(2)
            b2 = M(r"V \approx \sum A(x)\,\Delta x", 40).next_to(tag, DOWN, buff=0.5)
            b3 = formula_box(M(r"V = \int_a^b A(x)\,dx", 46, ACCUM), ACCUM).next_to(b2, DOWN, buff=0.4)
            b4 = T("add up infinitely many thin slices", 30, DIM).next_to(b3, DOWN, buff=0.25)
            self.play(Write(b2), run_time=0.9)
            self.play(FadeIn(b3), FadeIn(b4), run_time=1)
            b.line(3)
            q = M("A(x) = \\, ?", 40, SECANT).next_to(b4, DOWN, buff=0.4)
            self.play(FadeIn(q), run_time=0.6)
            self.play(Circumscribe(q, color=SECANT), run_time=1)
        self.clear()

        # ---------------------------------------------------------------- the side across the base
        with self.beat("The side across the base") as b:
            up = lambda s: 2.3 + 0.3 * np.sin(1.1 * s)
            lo = lambda s: 0.5 + 0.25 * np.cos(1.3 * s)
            st = base_stage([(up, 0, 4.2, FUNC, r"\text{top}", (4.55, 2.15), "x"), (lo, 0, 4.2, DERIV, r"\text{bottom}", (4.7, 0.75), "x")],
                            (up, lo, 0.3, 3.9), "square", (-0.4, 4.8), (-0.4, 3.0), at=2.2, n=8, scale=1.2, seg_label=None)
            st.move_to(LEFT * 2.6 + DOWN * 0.4)
            cue = base_cues(st)
            self.play(FadeIn(st), run_time=0.6)
            cue["draw"](0, 1)(self)
            cue["shade"]()(self)
            cue["seg"]()(self)
            sx = M(r"s(x) = \text{top} - \text{bottom}", 40, SECANT).move_to(RIGHT * 3.3 + UP * 1.6)
            self.play(Write(sx), run_time=1)
            b.line(1)
            self.play(Indicate(sx, color=SECANT), run_time=1)
            b.line(2)
            cue["stand"]()(self)
            area = M(r"\text{square: } A = s^2", 40, ACCUM).next_to(sx, DOWN, buff=0.7)
            self.play(Write(area), run_time=1)
        self.clear()

        # ---------------------------------------------------------------- the lesson example: sketch, slice, solve
        st = base_stage([(np.sqrt, 0, 4.5, FUNC, r"y = \sqrt x", (5.05, 2.0), "x")], (SQ, ZERO, 0, 4), "square", (-0.4, 5.0), (-0.4, 2.7),
                        at=2.25, n=8, ticks={"x": [1, 2, 3, 4], "y": [1, 2]}, scale=1.15, lines=[(4, 0, 4, 2.4, DIM, "x = 4", (4.0, 2.75))])
        c = base_cues(st)
        self.example("Squares on a root", r"The base of a solid is the region bounded by $y = \sqrt x$, the $x$-axis, and $x = 4$. Cross sections perpendicular to the $x$-axis are squares. Find the volume.",
                     [r"TEXT:$y = \sqrt x$: starts at the origin, rises, bends over", r"TEXT:The base: under $y = \sqrt x$, from $x = 0$ to $x = 4$",
                      r"s(x) = \sqrt x - 0 = \sqrt x", r"TEXT:On paper: draw the base and one slice", r"A(x) = s^2 = \left(\sqrt x\right)^2 = x", r"V = \int_0^4 x\,dx",
                      r"= \left[\tfrac{x^2}{2}\right]_0^4", r"= 8"], at=[1, 2, 3, 4, 5, 6, 6, 6], figure=st, figure_at=1, follow=True, size=42,
                     ref=r"V = \int_a^b A(x)\,dx, \quad A = s^2",
                     cues={0: c["draw"](0), 1: c["both"](c["draw"](1), c["shade"]()), 2: c["seg"](), 3: c["both"](c["stand"](), c["fill"](), c["flat"]())})

        # ---------------------------------------------------------------- rectangles
        with self.beat("Rectangles") as b:
            head = M(r"\text{rectangle: } A = \text{base} \times \text{height}", 44).to_edge(UP, buff=0.5)
            self.play(Write(head), run_time=1)
            b.line(1)

            def rects(height):
                def draw(st, v, rise):
                    out = list(floor_axes(st, v, (-0.4, 4.6), (-0.4, 2.4), labels=False))
                    out.append(floor_region(v, SQ, ZERO, 0, 4, opacity=0.35))
                    out.append(floor_curve(v, np.sqrt, 0, 4.3))
                    if rise > 0.01:
                        out += slabs("rect", SQ, ZERO, 0, 4, 8, gap=0.25, height=height, color=DERIV, rise=rise)
                    return out
                s = Stage(draw, View(scale=0.95, yaw=-34, pitch=22), rise=0)
                return s.reserve({"rise": 1})
            r1, r2 = rects(3.0), rects(lambda s: 2 * s)
            Group(r1, r2).arrange(RIGHT, buff=1.0).next_to(head, DOWN, buff=0.3)
            l1 = M(r"\text{height } 3: \ A(x) = 3\,s(x)", 36).next_to(r1, DOWN, buff=0.2)
            l2 = M(r"\text{height } 2s: \ A(x) = s \cdot 2s = 2s^2", 36).next_to(r2, DOWN, buff=0.2)
            self.play(FadeIn(r1), FadeIn(r2), run_time=0.8)
            self.play(r1.to("rise", 1), FadeIn(l1), run_time=1.4)
            self.play(r2.to("rise", 1), FadeIn(l2), run_time=1.4)
            b.line(2)
            self.play(FadeIn(M(r"s(x) = \text{top} - \text{bottom}", 38, SECANT).to_edge(DOWN, buff=0.3)), run_time=0.8)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(formula_box(M(r"V = \int_a^b A(x)\,dx", 50, ACCUM), ACCUM), M(r"\text{side } s(x) = \text{top} - \text{bottom of the base}", 38),
                          M(r"\text{square: } s^2 \qquad \text{rectangle: base} \times \text{height}", 38, SECANT), T("sketch the base flat; picture the slice", 36, DIM)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c_) for c_ in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        # Example 1: between y = x and y = x^2
        st = base_stage([(lambda s: s, -0.1, 1.25, FUNC, "y = x", (1.32, 1.12), "x"), (lambda s: s * s, -0.1, 1.15, DERIV, "y = x^2", (1.38, 1.48), "x")],
                        (lambda s: s, lambda s: s * s, 0, 1), "square", (-0.25, 1.5), (-0.25, 1.45), at=0.5625, n=8, ticks={"x": [1], "y": [1]}, scale=3.4, pose=(-14.0, 48.0))
        c = base_cues(st)
        self.example("Example 1: Squares between two curves", r"The base is the region between $y = x$ and $y = x^2$. Cross sections perpendicular to the $x$-axis are squares. Find the volume.",
                     [r"TEXT:$y = x$: a line; $y = x^2$: a parabola", r"x^2 = x", r"x^2 - x = 0", r"x(x - 1) = 0, \text{ so } x = 0, \ x = 1", r"TEXT:On $(0, 1)$, $x$ is on top.",
                      r"s(x) = x - x^2", r"TEXT:On paper: draw the base and one slice", r"A(x) = \left(x - x^2\right)^2 = x^2 - 2x^3 + x^4", r"V = \int_0^1 \left(x^2 - 2x^3 + x^4\right) dx", r"= \tfrac13 - \tfrac12 + \tfrac15",
                      r"= \tfrac{1}{30}"], at=[1, 2, 2, 2, 3, 3, 4, 5, 6, 6, 6], figure=st, figure_at=1, size=42, ref=r"V = \int_a^b A(x)\,dx, \quad A = s^2",
                     cues={0: c["draw"](0, 1), 4: c["shade"](), 5: c["seg"](), 6: c["both"](c["stand"](), c["fill"](), lambda sc: sc.wait(1.0), c["flat"]())})
        # Example 2: rectangles of height 3 on 4 - x^2
        par = lambda s: 4 - s * s
        st = base_stage([(par, -2.15, 2.15, FUNC, "y = 4 - x^2", (1.9, 3.4), "x")], (par, ZERO, -2, 2), "rect", (-2.7, 2.9), (-0.4, 4.6), at=0.25, n=8,
                        ticks={"x": [-2, 2], "y": [4]}, height=3.0, scale=0.85)
        c = base_cues(st)
        self.example("Example 2: Rectangles of height 3", r"The base is the region between $y = 4 - x^2$ and the $x$-axis. Cross sections perpendicular to the $x$-axis are rectangles of height $3$. Find the volume.",
                     [r"4 - x^2 = 0 \text{ at } x = \pm2", r"s(x) = 4 - x^2", r"TEXT:On paper: draw the base and one slice", r"A(x) = 3\left(4 - x^2\right)", r"V = \int_{-2}^{2} 3\left(4 - x^2\right) dx", r"= 3\left[4x - \tfrac{x^3}{3}\right]_{-2}^{2}",
                      r"= 3 \cdot \tfrac{32}{3}", r"= 32"], at=[1, 2, 3, 4, 5, 5, 5, 5], figure=st, figure_at=1, size=42, ref=r"V = \int_a^b A(x)\,dx, \quad A = \text{base} \times \text{height}",
                     cues={0: c["both"](c["draw"](0), c["shade"]()), 1: c["seg"](), 2: c["both"](c["stand"](), c["fill"](), lambda sc: sc.wait(1.5), c["flat"]())})
        # Example 3: perpendicular to the y-axis
        st = base_stage([(lambda y: y * y, -2.2, 2.2, DERIV, "x = y^2", (3.1, 2.25), "y")], (lambda y: 4.0, lambda y: y * y, -2, 2), "square", (-0.4, 5.0), (-2.6, 2.8),
                        at=0.25, n=8, var="y", ticks={"x": [4], "y": [-2, 2]}, scale=0.75, pose=(-50.0, 26.0), lines=[(4, -2.4, 4, 2.4, FUNC, "x = 4", (4.6, 1.5))])
        c = base_cues(st)
        self.example("Example 3: Perpendicular to the y-axis", r"The base is the region between $x = y^2$ and $x = 4$. Cross sections perpendicular to the $y$-axis are squares. Find the volume.",
                     [r"TEXT:Horizontal slices: integrate in $y$.", r"y^2 = 4 \text{ at } y = \pm2", r"s(y) = 4 - y^2", r"TEXT:On paper: draw the base and one slice", r"A(y) = \left(4 - y^2\right)^2 = 16 - 8y^2 + y^4",
                      r"V = \int_{-2}^{2} \left(16 - 8y^2 + y^4\right) dy", r"= 2\left(32 - \tfrac{64}{3} + \tfrac{32}{5}\right)", r"= \tfrac{512}{15} \approx 34.13"],
                     at=[1, 2, 3, 4, 5, 6, 6, 6], figure=st, figure_at=1, size=42, ref=r"V = \int_c^d A(y)\,dy, \quad A = s^2",
                     cues={0: c["draw"](0, 1), 1: c["shade"](), 2: c["seg"](), 3: c["both"](c["stand"](), c["fill"](), lambda sc: sc.wait(1.5), c["flat"]())})
        self.finish()
