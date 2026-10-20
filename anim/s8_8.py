"""Topic 8.8: Volumes with triangle and semicircle cross sections. Narration comes from transcripts/8_8.md.

Adder's notes (2026-10-14, the 8.7 notes hold here too): real 3D angled views; after the title, an introduction to this
type of volume problem (known cross sections perpendicular to an axis), the area of one slice, and the sum of thin
slabs growing into the smooth solid; every example sketches the base flat first, tilts to see the sections, then tilts
back, since on paper only the base is drawn. 3D pictures come from anim/solids.py.
"""
import numpy as np
from manim import *

from kit import *
from solids import *
from style import *

ZERO = lambda s: 0.0
PAR = lambda s: 4 - s * s
F = lambda s: 1.2 + 0.5 * np.sin(1.2 * s)
SQ = lambda s: np.sqrt(max(s, 0.0))


class Lesson(TranscriptScene):
    NUM = "8.8"

    def construct(self):
        # ---------------------------------------------------------------- cold open: one base, three solids
        with self.beat("Same base, new shapes") as b:
            kinds = [("square", ACCUM, r"\text{squares}"), ("equilateral", SECANT, r"\text{triangles}"), ("semicircle", TANGENT, r"\text{semicircles}")]

            def draw(st, v, rise, kind):
                out = list(floor_axes(st, v, (-2.7, 2.9), (-0.4, 4.6), ticks={"x": [-2, 2]}))
                out.append(floor_region(v, PAR, ZERO, -2, 2, opacity=0.35))
                out.append(floor_curve(v, PAR, -2.1, 2.1))
                if rise > 0.01:
                    kd, col, _ = kinds[int(kind)]
                    out.append(section_solid(kd, PAR, ZERO, -2, 2, n=40, color=col, m=18, rise=rise))
                return out
            st = Stage(draw, View(origin=LEFT * 1.4 + DOWN * 2.2, scale=0.95, yaw=-50, pitch=24), rise=0, kind=0)
            st.reserve({"rise": 1, "yaw": -50}, {"rise": 1, "yaw": -85})
            st.move_to(LEFT * 1.4 + DOWN * 0.2)
            name = M(kinds[0][2], 40, kinds[0][1]).to_corner(UR, buff=0.6)
            self.play(FadeIn(st), run_time=0.8)
            self.play(st.to("rise", 1), FadeIn(name), run_time=1.6)
            for i in (1, 2):
                if i == 2:
                    b.line(1)
                self.play(st.to("rise", 0), FadeOut(name), st.spin(-5), run_time=1.0)
                st.set("kind", i)
                name = M(kinds[i][2], 40, kinds[i][1]).to_corner(UR, buff=0.6)
                self.play(st.to("rise", 1), FadeIn(name), st.spin(-5), run_time=1.4)
                self.wait(0.6)
            self.play(st.spin(-25), run_time=3)
            b.line(2)
            self.play(FadeIn(formula_box(M(r"V = \int_a^b A(x)\,dx", 44, ACCUM), ACCUM).next_to(name, DOWN, buff=0.6)), run_time=0.8)
        self.clear()
        self.title()

        # ---------------------------------------------------------------- the kind of problem, and the sum of slices
        with self.beat("Cross sections, again") as b:
            head = T("Volume with known cross sections", 46).to_edge(UP, buff=0.4)

            def draw(st, v, curve, seg, one, n, many, smooth, lift):
                out = list(floor_axes(st, v, (-0.4, 4.8), (-0.4, 2.4), ticks={"x": [1, 2, 3, 4], "y": [1, 2]}))
                out.append(floor_region(v, F, ZERO, 0, 4, opacity=0.35 * curve))
                if curve > 0.01:
                    out.append(floor_curve(v, F, 0, 4.3 * curve))
                if curve > 0.98:
                    out.append(st.label("f", "y = f(x)", 30, FUNC).move_to(v.P(4.35, 2.15, 0)))
                if seg > 0.01:
                    out.append(floor_segment(v, F, ZERO, 2.25).set_stroke(opacity=seg))
                if smooth > 0.5:
                    out.append(section_solid("semicircle", F, ZERO, 0, 4, n=48, color=TANGENT, m=18))
                elif many > 0.01:
                    nn = int(round(n))
                    out += slabs("semicircle", F, ZERO, 0, 4, nn, gap=0.18 if nn < 30 else 0.0, color=TANGENT, rise=many)
                if one > 0.01:
                    out.append(slab("semicircle", F, ZERO, 2.25, 0.5, color=SECANT, rise=one).moved(t=(0, 0, 1.4 * lift)))
                return out
            st = Stage(draw, View(origin=LEFT * 5.8 + DOWN * 2.2, scale=1.6, yaw=0, pitch=90), curve=0, seg=0, one=0, n=4, many=0, smooth=0, lift=0)
            self.play(FadeIn(head), FadeIn(st), run_time=0.8)
            self.play(st.to("curve", 1), run_time=1.4)
            self.play(st.to("yaw", -32), st.to("pitch", 24), run_time=2.2)
            b.line(1)
            self.play(st.to("seg", 1), run_time=0.8)
            self.play(st.to("one", 1), run_time=1.2)
            self.play(st.to("lift", 1), run_time=1.0)
            v = st.view()
            one = slab("semicircle", F, ZERO, 2.25, 0.5).moved(t=(0, 0, 1.4))
            cap = max(one.faces[:2], key=lambda f: f.normal @ v.toward())
            other = one.faces[0] if cap is one.faces[1] else one.faces[1]
            Ax, dx = face_labels(v, cap, other, "A(x)", r"\Delta x")
            self.play(FadeIn(Ax), FadeIn(dx), run_time=0.8)
            b.line(2)
            self.play(FadeOut(Ax), FadeOut(dx), st.to("one", 0), st.to("lift", 0), st.to("seg", 0), run_time=0.6)
            tag = M("n = 4", 34, DIM).to_corner(UR, buff=0.5).shift(DOWN * 0.8)
            self.play(st.to("many", 1), FadeIn(tag), run_time=1)
            self.wait(0.8)
            for n in (8, 16, 40):
                new = M(f"n = {n}", 34, DIM).move_to(tag)
                self.play(st.to("n", n), FadeOut(tag), FadeIn(new), run_time=0.5)
                tag = new
                self.wait(0.9)
            new = T("smooth", 34, DIM).move_to(tag)
            self.play(st.to("smooth", 1), FadeOut(tag), FadeIn(new), run_time=0.6)
            b2 = M(r"V \approx \sum A(x)\,\Delta x", 40).next_to(new, DOWN, buff=0.5)
            b3 = formula_box(M(r"V = \int_a^b A(x)\,dx", 46, ACCUM), ACCUM).next_to(b2, DOWN, buff=0.4)
            self.play(Write(b2), run_time=0.9)
            self.play(FadeIn(b3), run_time=0.8)
            b.line(3)
            q = M("A(x) = \\, ?", 40, SECANT).next_to(b3, DOWN, buff=0.5)
            self.play(FadeIn(q), run_time=0.6)
            self.play(Circumscribe(q, color=SECANT), run_time=1)
        self.clear()

        with self.beat("Areas from the side s") as b:
            s = 2.4

            def shape(kind, color):
                p0, p1 = LEFT * s / 2, RIGHT * s / 2
                return VGroup(cross_section(kind, p0, p1, color=color), M("s", 30, INK).next_to(ORIGIN, DOWN, buff=0.15))
            eq = shape("equilateral", SECANT)
            eq.add(DashedLine(ORIGIN, UP * s * 0.866, color=DIM), M(r"\tfrac{\sqrt3}{2}s", 26, DIM).next_to(UP * s * 0.43, RIGHT, buff=0.08))
            sc = shape("semicircle", DERIV)
            sc.add(Line(ORIGIN, RIGHT * s / 2, color=TANGENT, stroke_width=4), M(r"r = \tfrac s2", 26, TANGENT).next_to(RIGHT * s / 4, UP, buff=0.1))
            ir = shape("isosceles_right", ACCUM)
            VGroup(eq, sc, ir).arrange(RIGHT, buff=1.4).shift(UP * 1)
            f1 = M(r"\tfrac12 \cdot s \cdot \tfrac{\sqrt3}{2}s = \tfrac{\sqrt3}{4}s^2", 32, SECANT).next_to(eq, DOWN, buff=0.6)
            f2 = M(r"\tfrac12\pi\left(\tfrac s2\right)^2 = \tfrac\pi8 s^2", 32, DERIV).next_to(sc, DOWN, buff=0.6)
            f3 = M(r"\tfrac12 s^2", 32, ACCUM).next_to(ir, DOWN, buff=0.6)
            self.play(FadeIn(eq), Write(f1), run_time=1.2)
            b.line(1)
            self.play(FadeIn(sc), Write(f2), run_time=1.2)
            b.line(2)
            self.play(FadeIn(ir), Write(f3), run_time=1)
            b.line(3)
            self.play(FadeIn(M(r"s = \text{top} - \text{bottom}", 40, INK).to_edge(DOWN, buff=0.6)), run_time=0.8)
        self.clear()

        # ---------------------------------------------------------------- the lesson example: sketch, slice, solve
        st = base_stage([(PAR, -2.15, 2.15, FUNC, "y = 4 - x^2", (2.0, 3.4), "x")], (PAR, ZERO, -2, 2), "semicircle", (-2.7, 2.9), (-0.4, 4.6), at=0.25, n=8,
                        ticks={"x": [-2, 2], "y": [4]}, color=DERIV, scale=0.85)
        c = base_cues(st)
        self.example("Semicircles on a parabola", r"The base of a solid is the region between $y = 4 - x^2$ and the $x$-axis. Cross sections perpendicular to the $x$-axis are semicircles. Find the volume.",
                     [r"TEXT:$y = 4 - x^2$: opens down from $(0, 4)$", r"4 - x^2 = 0 \text{ at } x = \pm2", r"s(x) = 4 - x^2", r"TEXT:On paper: draw the base and one slice",
                      r"r = \tfrac s2 = \tfrac{4 - x^2}{2}", r"A(x) = \tfrac12\pi r^2 = \tfrac\pi8\left(4 - x^2\right)^2", r"\left(4 - x^2\right)^2 = 16 - 8x^2 + x^4",
                      r"V = \tfrac\pi8\int_{-2}^{2} \left(16 - 8x^2 + x^4\right) dx", r"= \tfrac\pi8 \cdot 2\left(32 - \tfrac{64}{3} + \tfrac{32}{5}\right)",
                      r"= \tfrac\pi8 \cdot \tfrac{512}{15}", r"= \tfrac{64\pi}{15} \approx 13.40"], at=[1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 9], figure=st, figure_at=1, follow=True, size=42,
                     ref=r"V = \int_a^b A(x)\,dx, \quad A = \tfrac\pi8 s^2",
                     cues={0: c["draw"](0), 1: c["shade"](), 2: c["seg"](), 3: c["both"](c["stand"](), c["fill"](), lambda sc: sc.wait(1.0), c["flat"]())})

        with self.beat("Leg or hypotenuse?") as b:
            def tri(kind, color):
                def draw(st, v, rise):
                    out = [Line(v.P(0, -1.3, 0), v.P(0, 1.3, 0), color=SECANT, stroke_width=6)]
                    if rise > 0.01:
                        out.append(prism(profile(kind, -1.3, 1.3, rise=rise), -0.3, 0.3, "x", color=color))
                    return out
                s_ = Stage(draw, View(scale=1.0, yaw=-58, pitch=20), rise=0)
                return s_.reserve({"rise": 1}, {"rise": 1, "yaw": -30})
            t1, t2 = tri("leg", ACCUM), tri("hyp", SECANT)
            Group(t1, t2).arrange(RIGHT, buff=2.6).to_edge(UP, buff=0.5)
            s = 2.0
            leg = VGroup(cross_section("isosceles_right", LEFT * s / 2, RIGHT * s / 2, color=ACCUM), M("s", 30).next_to(ORIGIN, DOWN, buff=0.15), M("s", 30).next_to(LEFT * s / 2 + UP * s / 2, LEFT, buff=0.15))
            hyp = VGroup(cross_section("isosceles_hyp", LEFT * s / 2, RIGHT * s / 2, color=SECANT), M("s", 30).next_to(ORIGIN, DOWN, buff=0.15),
                         M(r"\tfrac{s}{\sqrt2}", 28).next_to(LEFT * s / 4 + UP * s / 4, UL, buff=0.05))
            leg.next_to(t1, DOWN, buff=0.3)
            hyp.next_to(t2, DOWN, buff=0.3).align_to(leg, DOWN)
            self.play(FadeIn(t1), FadeIn(t2), run_time=0.6)
            self.play(t1.to("rise", 1), t2.to("rise", 1), run_time=1.2)
            b.line(1)
            self.play(FadeIn(leg), t1.spin(28), run_time=1.2)
            self.play(Write(M(r"\text{leg on base: } \tfrac12 s^2", 36, ACCUM).next_to(leg, DOWN, buff=0.35)), run_time=1)
            b.line(2)
            self.play(FadeIn(hyp), t2.spin(28), run_time=1.2)
            self.play(Write(M(r"\text{hypotenuse on base: } \tfrac12\left(\tfrac{s}{\sqrt2}\right)^2 = \tfrac14 s^2", 36, SECANT).next_to(hyp, DOWN, buff=0.35)), run_time=1.2)
            self.play(FadeIn(T("read which side is on the base", 32, TANGENT).to_edge(DOWN, buff=0.3)), run_time=0.8)
        self.clear()

        with self.beat("Close") as b:
            tab = table([r"\text{shape (side } s \text{ on the base)}", r"A"], [[r"\text{square}", r"s^2"], [r"\text{equilateral triangle}", r"\tfrac{\sqrt3}{4}s^2"],
                        [r"\text{isosceles right, leg on base}", r"\tfrac12 s^2"], [r"\text{isosceles right, hypotenuse on base}", r"\tfrac14 s^2"], [r"\text{semicircle, diameter on base}", r"\tfrac\pi8 s^2"]], size=34).shift(UP * 0.5)
            self.play(FadeIn(tab), run_time=1.4)
            self.play(FadeIn(M(r"V = \int A(x)\,dx, \quad s = \text{top} - \text{bottom}", 40, ACCUM).next_to(tab, DOWN, buff=0.5)), run_time=0.8)
        self.clear()

        self.examples_card()
        # Example 1: equilateral triangles under sqrt x
        st = base_stage([(np.sqrt, 0, 4.5, FUNC, r"y = \sqrt x", (5.05, 2.0), "x")], (SQ, ZERO, 0, 4), "equilateral", (-0.4, 5.0), (-0.4, 2.7), at=2.25, n=8,
                        ticks={"x": [1, 2, 3, 4], "y": [1, 2]}, color=TANGENT, scale=1.15, lines=[(4, 0, 4, 2.4, DIM, "x = 4", (4.0, 2.75))])
        c = base_cues(st)
        self.example("Example 1: Equilateral triangles", r"The base is the region under $y = \sqrt x$ for $0 \le x \le 4$. Cross sections perpendicular to the $x$-axis are equilateral triangles. Find the volume.",
                     [r"TEXT:The base: under $y = \sqrt x$, from $0$ to $4$", r"s = \sqrt x", r"TEXT:On paper: draw the base and one slice", r"A(x) = \tfrac{\sqrt3}{4}\left(\sqrt x\right)^2 = \tfrac{\sqrt3}{4}x",
                      r"V = \tfrac{\sqrt3}{4}\int_0^4 x\,dx", r"= \tfrac{\sqrt3}{4}(8)", r"= 2\sqrt3 \approx 3.46"], at=[1, 2, 3, 4, 5, 5, 5], figure=st, figure_at=1, size=42,
                     ref=r"V = \int_a^b A(x)\,dx, \quad A = \tfrac{\sqrt3}{4}s^2",
                     cues={0: c["both"](c["draw"](0, 1), c["shade"]()), 1: c["seg"](), 2: c["both"](c["stand"](), c["fill"](), lambda sc: sc.wait(1.0), c["flat"]())})
        # Example 2: the disk, hypotenuse on the base
        ct = lambda s: np.sqrt(max(4 - s * s, 0.0))
        cb = lambda s: -ct(s)
        st = base_stage([(ct, -2, 2, FUNC, r"y = \sqrt{4 - x^2}", (1.9, 2.45), "x"), (cb, -2, 2, FUNC, r"y = -\sqrt{4 - x^2}", (1.95, -2.45), "x")], (ct, cb, -2, 2), "hyp",
                        (-2.7, 2.9), (-2.7, 2.9), at=0.25, n=8, ticks={"x": [-2, 2], "y": [-2, 2]}, color=ACCUM, scale=0.85, pose=(-40.0, 28.0))
        c = base_cues(st)
        self.example("Example 2: Hypotenuse on a disk", r"The base is the disk $x^2 + y^2 \le 4$. Cross sections perpendicular to the $x$-axis are isosceles right triangles with the hypotenuse on the base. Find the volume.",
                     [r"\text{top: } y = \sqrt{4 - x^2}", r"\text{bottom: } y = -\sqrt{4 - x^2}", r"s = 2\sqrt{4 - x^2}", r"TEXT:On paper: draw the base and one slice",
                      r"A = \tfrac14 s^2 = \tfrac14 \cdot 4\left(4 - x^2\right) = 4 - x^2", r"V = \int_{-2}^{2} \left(4 - x^2\right) dx", r"= \tfrac{32}{3}"], at=[1, 1, 2, 3, 4, 5, 5], figure=st, figure_at=1, size=42,
                     ref=r"V = \int_a^b A(x)\,dx, \quad A = \tfrac14 s^2",
                     cues={0: c["both"](c["draw"](0, 1), c["shade"]()), 2: c["seg"](), 3: c["both"](c["stand"](), c["fill"](), lambda sc: sc.wait(1.0), c["flat"]())})
        # Example 3: between 2x and x^2, a leg on the base
        st = base_stage([(lambda s: 2 * s, -0.1, 2.25, FUNC, "y = 2x", (1.55, 4.15), "x"), (lambda s: s * s, -0.1, 2.15, DERIV, "y = x^2", (2.65, 4.3), "x")],
                        (lambda s: 2 * s, lambda s: s * s, 0, 2), "leg", (-0.3, 2.8), (-0.3, 4.9), at=1.125, n=8, ticks={"x": [1, 2], "y": [2, 4]}, scale=1.0, pose=(-14.0, 46.0))
        c = base_cues(st)
        self.example("Example 3: Leg on the base", r"The base is the region between $y = 2x$ and $y = x^2$. Cross sections perpendicular to the $x$-axis are isosceles right triangles with a leg on the base. Find the volume.",
                     [r"TEXT:$y = 2x$: a line, slope $2$; $y = x^2$: a parabola", r"x^2 = 2x", r"x(x - 2) = 0, \text{ so } x = 0, \ x = 2", r"TEXT:On $(0, 2)$, $2x$ is on top.", r"s = 2x - x^2",
                      r"TEXT:On paper: draw the base and one slice", r"A = \tfrac12 s^2 = \tfrac12\left(2x - x^2\right)^2", r"\left(2x - x^2\right)^2 = 4x^2 - 4x^3 + x^4",
                      r"V = \tfrac12\int_0^2 \left(4x^2 - 4x^3 + x^4\right) dx", r"= \tfrac12\left(\tfrac{32}{3} - 16 + \tfrac{32}{5}\right)", r"= \tfrac12 \cdot \tfrac{16}{15} = \tfrac{8}{15}"],
                     at=[1, 2, 2, 3, 3, 4, 5, 5, 6, 6, 7], figure=st, figure_at=1, size=42, ref=r"V = \int_a^b A(x)\,dx, \quad A = \tfrac12 s^2",
                     cues={0: c["draw"](0, 1), 3: c["shade"](), 4: c["seg"](), 5: c["both"](c["stand"](), c["fill"](), lambda sc: sc.wait(1.0), c["flat"]())})
        self.finish()
