"""Topic 8.9: Disc method about the x- or y-axis. Narration comes from transcripts/8_9.md.

Adder's notes (2026-10-14): the best solids-of-revolution animations. An angled view; the region sweeps slowly around
the axis and the volume it sweeps STAYS; then the whole solid as one big solid, seen from different angles, so the
rotation lands; then slowly slice it: the slice is a circle (a disc), seen face on and edge on. Examples start from the
student's sketch (curves, region), then show the rotation, then only ONE disc at the spot we care about with its R,
never a stack of cross sections. 3D pictures come from anim/solids.py (rev_stage / rev_cues for the examples).
"""
import numpy as np
from manim import *

from kit import *
from solids import *
from style import *

ZERO = lambda s: 0.0
SQ = lambda s: np.sqrt(max(s, 0.0))
B = lambda s: 1.15 + 0.5 * np.sin(1.25 * s)         # "One big solid": a bead-shaped profile, 0.67 to 1.65 on [0, 4]
X0, DX = 2.3, 0.14                                   # where the bead is sliced, and the slice's thickness
BEAD = region_outline(B, ZERO, 0, 4, n=40)
BEAD_L = region_outline(B, ZERO, 0, X0 - DX / 2, n=24)
BEAD_R = region_outline(B, ZERO, X0 + DX / 2, 4, n=20)
REF_X = r"V = \pi\int_a^b [R(x)]^2\,dx"
REF_Y = r"V = \pi\int_c^d [R(y)]^2\,dy"


def ring(v, r, x, frac, n=64):
    """The cut line drawn around the solid at x (radius r), frac of the way around: only the half that faces us, drawn
    over the solid (sorting thin line pieces against the surface let bits of the back half show at the silhouette)."""
    w = v.toward()
    out = []
    th = np.linspace(0, TAU * frac, max(2, int(n * frac)) + 1)
    for a, b_ in zip(th[:-1], th[1:]):
        m = (a + b_) / 2
        if np.array([0.0, -np.sin(m), np.cos(m)]) @ w > 0:
            out.append(Line(v.P(x, -r * np.sin(a), r * np.cos(a)), v.P(x, -r * np.sin(b_), r * np.cos(b_)), color=SECANT, stroke_width=5))
    return out


def bead(st, v, curve, shade, sweep, side, cut_line, split, cut, pieces, ghost, rad, many, n, smooth, top):
    """The lesson's solid: drawn flat, swept, seen whole, cut, one slice alone, then rebuilt from discs."""
    v = v.turned(origin=v.origin + (v.origin - v.P(2.0, 0, 0)))       # it turns about its own middle, not the origin
    out = list(upright_axes(st, v, (-0.5, 4.9), (-2.2, 2.3), ticks={"x": [1, 2, 3, 4]}))
    lit = shade * max(0.0, 1 - sweep / 0.04)
    if lit > 0.01:
        out.append(upright_region(v, B, ZERO, 0, 4, opacity=0.45 * lit))
    if curve > 0.01:
        out.append(upright_curve(v, B, 0, 4 * curve))
    if curve > 0.98 and sweep < 0.01:
        out.append(st.label("f", "y = f(x)", 30, FUNC).move_to(v.P(4.45, 0, 1.1)))
    if many > 0.01:
        if smooth > 0.5:
            out.append(revolve(BEAD, "x", 0.0, nt=48))
        else:
            nn = int(round(n))
            w = 4.0 / nn
            out += [disc(B((i + 0.5) * w), (i + 0.5) * w, w * (0.82 if nn < 30 else 1.0), nt=40) for i in range(nn)]
    elif sweep > 1e-3:
        t1 = TAU if sweep > 0.999 else sweep * TAU
        if split < 0.5:
            out.append(revolve(BEAD, "x", 0.0, 0.0, t1, nt=48))
            if cut_line > 0.01:
                out += ring(v, B(X0), X0, cut_line)
        else:
            if ghost > 0.01:
                out += [revolve(BEAD, "x", 0.0, nt=48, opacity=0.35 * ghost, grid=True), VMobject()]
            if pieces > 0.01:
                g, op = 0.8 * cut, (1.0 if pieces > 0.99 else pieces)
                out.append(revolve(BEAD_L, "x", 0.0, nt=48, opacity=op).moved(t=(-g, 0, 0)))
                out.append(revolve(BEAD_R, "x", 0.0, nt=48, opacity=op).moved(t=(g, 0, 0)))
            out.append(disc(B(X0), X0, DX, color=SECANT))
    if side > 0.01:
        # the outline seen from the side: the curve and its mirror image, traced over the solid
        out.append(upright_curve(v, B, 0, 4).set_stroke(opacity=side))
        out.append(upright_curve(v, lambda s: -B(s), 0, 4, color=FUNC).set_stroke(opacity=side).set_stroke(width=4))
    if top > 0.01:
        out.append(upright_curve(v, B, 0, 4).set_stroke(opacity=top))
    if rad > 0.01:
        off = DX / 2 * (1 if np.array([1.0, 0, 0]) @ v.toward() >= 0 else -1)
        p0, p1 = v.P(X0 + off, 0, 0), v.P(X0 + off, 0, B(X0))
        p1 = p0 + (p1 - p0) * min(1.0, rad)
        out += [Line(p0, p1, color=BG, stroke_width=11), Line(p0, p1, color=TANGENT, stroke_width=6)]
        if rad > 0.98:
            lab = st.label("R", "R(x)", 32, TANGENT).next_to((p0 + p1) / 2, LEFT, buff=0.14)
            out += [SurroundingRectangle(lab, buff=0.05, corner_radius=0.06, stroke_width=0).set_fill(BG, 0.85), lab]
    return out, v


class Lesson(TranscriptScene):
    NUM = "8.9"

    def construct(self):
        # ---------------------------------------------------------------- cold open: a region sweeps out a solid
        with self.beat("Spinning a region") as b:
            st = rev_stage([(np.sqrt, 0, 4.4, FUNC, r"y = \sqrt x", (4.55, 2.45), "x")], region_outline(SQ, ZERO, 0, 4), "x", 0.0, SQ, (-0.5, 5.0), (-2.5, 2.7),
                           at=2.0, shade=(SQ, ZERO, 0, 4, "x"), lines=[(4, 0, 4, 2, DIM, None, None)], ticks={"x": [1, 2, 3, 4]}, scale=1.3, pose=(-32.0, 20.0), turn=-26.0)
            st.move_to(DOWN * 0.2)
            c = rev_cues(st)
            self.play(FadeIn(st), run_time=0.6)
            c["draw"](0, 1, rt=1.4)(self)
            c["shade"]()(self)
            b.line(1)
            c["spin"](rt=1.6, sweep=6.0, hold=0)(self)
            b.line(2)
            self.play(st.spin(-16), run_time=3.5)
            b.line(3)
            self.play(st.spin(24), st.tilt(28), run_time=3)
        self.clear()
        self.title()

        # ---------------------------------------------------------------- the whole solid, slowly
        st = Stage(bead, View(origin=LEFT * 3.3 + DOWN * 0.3, scale=1.3, yaw=0, pitch=0), fresh_labels=True, curve=0, shade=0, sweep=0, side=0,
                   cut_line=0, split=0, cut=0, pieces=1, ghost=0, rad=0, many=0, n=8, smooth=0, top=0)
        tag_at = RIGHT * 3.8 + UP * 1.6
        with self.beat("One big solid") as b:
            self.play(FadeIn(st), run_time=0.6)
            self.play(st.to("curve", 1), run_time=1.6)
            self.play(st.to("shade", 1), run_time=0.8)
            b.line(1)
            self.play(st.to("yaw", -32), st.to("pitch", 20), run_time=2)
            tag = T("a quarter turn", 36, DIM).move_to(tag_at)
            self.play(st.to("sweep", 0.25), FadeIn(tag), run_time=2.4)
            b.line(2)
            new = T("halfway", 36, DIM).move_to(tag_at)
            self.play(st.to("sweep", 0.5), FadeOut(tag), FadeIn(new), run_time=2.0)
            tag = new
            new = T("all the way around", 36, DIM).move_to(tag_at)
            self.play(st.to("sweep", 1), FadeOut(tag), FadeIn(new), run_time=2.4)
            tag = new
            b.line(3)
            self.play(FadeOut(tag), st.to("yaw", 0), st.to("pitch", 0), run_time=2.6)
            side = T("from the side", 36, DIM).move_to(tag_at)
            self.play(st.to("side", 1), FadeIn(side), run_time=1.4)
            b.line(4)
            end = T("from the end", 36, DIM).move_to(tag_at)
            self.play(st.to("side", 0), FadeOut(side), run_time=0.5)
            self.play(st.to("yaw", -90), st.to("pitch", 6), FadeIn(end), run_time=3)
            self.wait(1.2)
            self.play(FadeOut(end), st.to("yaw", -38), st.to("pitch", 22), run_time=2.6)
            self.play(st.spin(-16), run_time=2.5)

        # ---------------------------------------------------------------- slice it: one disc, from every side
        with self.beat("Every slice is a disc") as b:
            self.play(st.to("cut_line", 1), run_time=1.6)
            b.line(1)
            st.set("cut_line", 0)
            st.set("split", 1)
            self.play(st.to("cut", 1), run_time=1.6)
            self.play(st.to("pieces", 0), run_time=1.2)
            st.set("cut", 0)
            face = T("face on: a circle", 36, DIM).move_to(tag_at)
            self.play(st.to("yaw", -90), st.to("pitch", 6), FadeIn(face), run_time=2.2)
            self.wait(1.0)
            edge = T("edge on: thin", 36, DIM).move_to(tag_at)
            self.play(st.to("yaw", 0), st.to("pitch", 4), FadeOut(face), FadeIn(edge), run_time=2.2)
            v = bead_view(st)
            dx = nudge_arrow(v.P(X0 - DX / 2, 0, B(X0)) + UP * 0.3, v.P(X0 + DX / 2, 0, B(X0)) + UP * 0.3, label=r"\Delta x", side=UP)
            self.play(FadeIn(dx), run_time=0.6)
            self.wait(1.0)
            self.play(FadeOut(dx), FadeOut(edge), st.to("yaw", -38), st.to("pitch", 22), run_time=2.4)
            b.line(2)
            self.play(st.to("ghost", 1), st.to("top", 1), run_time=1.2)
            self.play(st.to("rad", 1), run_time=1.0)
            b.line(3)
            b1 = M(r"A(x) = \pi\,[R(x)]^2", 42)
            b2 = M(r"\text{one disc: } \pi\,[R(x)]^2\,\Delta x", 38)
            b3 = formula_box(M(r"V = \pi\int_a^b [R(x)]^2\,dx", 44, ACCUM), ACCUM)
            b4 = T("$R$ = distance from the axis to the curve", 28, DIM)
            board = VGroup(b1, b2, b3, b4).arrange(DOWN, buff=0.45).move_to(RIGHT * 3.9 + DOWN * 0.2)
            self.play(Write(b1), run_time=1)
            self.play(Write(b2), run_time=1)
            b.line(4)
            self.play(st.to("rad", 0), st.to("ghost", 0), st.to("top", 0), run_time=0.8)
            tag = M("n = 8", 34, DIM).move_to(LEFT * 3.3 + UP * 3.4)
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
            b.line(5)
            self.play(st.spin(-20), run_time=3)
        self.clear()

        # ---------------------------------------------------------------- the lesson example: sketch, spin, one disc
        st = rev_stage([(np.sqrt, 0, 4.4, FUNC, r"y = \sqrt x", (4.55, 2.45), "x")], region_outline(SQ, ZERO, 0, 4), "x", 0.0, SQ, (-0.5, 5.0), (-2.5, 2.7),
                       at=2.25, shade=(SQ, ZERO, 0, 4, "x"), lines=[(4, 0, 4, 2, DIM, "x = 4", (4.0, 2.4))], ticks={"x": [1, 2, 3, 4], "y": [-2, 2]}, scale=1.1)
        c = rev_cues(st)
        self.example("Discs on a root", r"The region under $y = \sqrt x$ for $0 \le x \le 4$ is revolved about the $x$-axis. Find the volume.",
                     [r"TEXT:The region: under $y = \sqrt x$, from $x = 0$ to $x = 4$", r"TEXT:One slice at $x$: a disc", r"R(x) = \sqrt x - 0 = \sqrt x",
                      r"A(x) = \pi\left(\sqrt x\right)^2 = \pi x", r"V = \pi\int_0^4 x\,dx", r"= \pi\left[\tfrac{x^2}{2}\right]_0^4", r"= 8\pi \approx 25.13"],
                     at=[1, 2, 3, 4, 5, 5, 5], figure=st, figure_at=1, follow=True, size=42, ref=REF_X,
                     cues={0: c["both"](c["draw"](0, 1), c["shade"]()), 1: c["both"](c["spin"](rt=1.6, sweep=3.0, hold=1.2), c["slice"](rt=1.2)),
                           2: c["both"](c["rad"](), lambda sc: sc.wait(1.0), c["flat"]())})

        # ---------------------------------------------------------------- the cone check
        with self.beat("A check with a cone") as b:
            half = lambda s: s / 2
            st = rev_stage([(half, 0, 6.4, FUNC, r"y = \tfrac x2", (6.0, 3.75), "x")], region_outline(half, ZERO, 0, 6), "x", 0.0, half, (-0.5, 7.0), (-0.5, 3.8),
                           at=4.0, shade=(half, ZERO, 0, 6, "x"), lines=[(6, 0, 6, 3, DIM, None, None)], ticks={"x": [6], "y": [3]}, scale=0.8, pose=(-34.0, 18.0), turn=-18.0)
            st.move_to(LEFT * 3.4 + DOWN * 0.2)
            c = rev_cues(st)
            self.play(FadeIn(st), run_time=0.6)
            c["draw"](0, 1, rt=1.0)(self)
            c["shade"](rt=0.6)(self)
            c["spin"](rt=1.4, sweep=2.6, hold=1.0)(self)
            b.line(1)
            r1 = M(r"\pi\int_0^6 \left(\tfrac x2\right)^2 dx = \pi \cdot \tfrac{216}{12} = 18\pi", 38).move_to(RIGHT * 3.4 + UP * 1.0)
            self.play(Write(r1), run_time=1)
            b.line(2)
            r2 = M(r"\tfrac13\pi r^2 h = \tfrac13\pi(3^2)(6) = 18\pi", 38, ACCUM).next_to(r1, DOWN, buff=0.6)
            self.play(Write(r2), run_time=1)
            self.play(FadeIn(M(r"\checkmark", 60, GRASS).next_to(r2, DOWN, buff=0.3)), run_time=0.5)
        self.clear()

        # ---------------------------------------------------------------- about the y-axis
        with self.beat("Around the y-axis") as b:
            sq = lambda s: s * s
            st = rev_stage([(sq, 0, 2.1, FUNC, "y = x^2", (2.65, 3.6), "x")], outline_y(SQ, ZERO, 0, 4), "y", 0.0, SQ, (-2.6, 3.0), (-0.5, 4.9),
                           at=2.2, shade=(SQ, ZERO, 0, 4, "y"), lines=[(0, 4, 2, 4, DIM, "y = 4", (2.75, 4.3))], ticks={"x": [-2, 2], "y": [4]}, scale=0.95,
                           pose=(-24.0, 26.0), turn=-12.0)
            st.move_to(LEFT * 3.6 + DOWN * 0.2)
            c = rev_cues(st)
            self.play(FadeIn(st), run_time=0.6)
            c["draw"](0, 1, rt=1.2)(self)
            c["shade"](rt=0.6)(self)
            b.line(1)
            c["spin"](rt=1.6, sweep=3.0, hold=1.0)(self)
            board = VGroup(T("horizontal slices: integrate in $y$", 30), M(r"x = \sqrt y, \ \ R(y) = \sqrt y", 38),
                           M(r"V = \pi\int_0^4 \left(\sqrt y\right)^2 dy = \pi\int_0^4 y\,dy = 8\pi", 34, ACCUM)).arrange(DOWN, buff=0.45).move_to(RIGHT * 3.4 + UP * 0.6)
            self.play(FadeIn(board[0]), run_time=0.6)
            b.line(2)
            c["slice"](rt=1.2)(self)
            c["rad"]()(self)
            self.play(Write(board[1]), run_time=0.8)
            c["flat"](rt=1.6)(self)
            b.line(3)
            self.play(Write(board[2]), run_time=1)
            b.line(4)
            self.play(FadeIn(T("slice perpendicular to the axis; integrate along it", 30, SECANT).to_edge(DOWN, buff=0.4)), run_time=0.8)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(M(r"V = \pi\int [R(x)]^2\,dx \ \ (\text{axis horizontal})", 42, ACCUM), M(r"V = \pi\int [R(y)]^2\,dy \ \ (\text{axis vertical})", 42, ACCUM),
                          T("$R$ = distance from the axis to the curve", 36), T("slice perpendicular to the axis", 36, SECANT)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c_) for c_ in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        # Example 1: x^2 on [0, 2] about the x-axis
        sq = lambda s: s * s
        st = rev_stage([(sq, 0, 2.08, FUNC, "y = x^2", (1.45, 3.9), "x")], region_outline(sq, ZERO, 0, 2), "x", 0.0, sq, (-0.4, 2.6), (-0.6, 4.7),
                       at=1.5, shade=(sq, ZERO, 0, 2, "x"), lines=[(2, 0, 2, 4, DIM, "x = 2", (2.35, 2.0))], ticks={"x": [1, 2], "y": [4]}, scale=1.3, pose=(-36.0, 18.0))
        c = rev_cues(st)
        self.example("Example 1: A parabola about the x-axis", r"The region under $y = x^2$ for $0 \le x \le 2$ is revolved about the $x$-axis. Find the volume.",
                     [r"TEXT:The region: under $y = x^2$, from $0$ to $2$", r"TEXT:One slice at $x$: a disc", r"R = x^2", r"V = \pi\int_0^2 \left(x^2\right)^2 dx", r"= \pi\int_0^2 x^4\,dx",
                      r"= \pi\left[\tfrac{x^5}{5}\right]_0^2", r"= \tfrac{32\pi}{5} \approx 20.11"], at=[1, 2, 2, 3, 3, 4, 4], figure=st, figure_at=1, size=42, ref=REF_X,
                     cues={0: c["both"](c["draw"](0, 1), c["shade"]()), 1: c["both"](c["spin"](rt=1.4, sweep=2.8, hold=1.0), c["slice"](rt=1.0)),
                           2: c["both"](c["rad"](), lambda sc: sc.wait(0.6), c["flat"](rt=1.4))})
        # Example 2: e^x on [0, 1] about the x-axis
        st = rev_stage([(np.exp, 0, 1.12, FUNC, "y = e^x", (1.35, 3.35), "x")], region_outline(np.exp, ZERO, 0, 1), "x", 0.0, np.exp, (-0.4, 1.6), (-0.5, 3.3),
                       at=0.6, shade=(np.exp, ZERO, 0, 1, "x"), lines=[(1, 0, 1, np.e, DIM, "x = 1", (1.3, 1.3))], ticks={"x": [1], "y": [1, 3]}, scale=1.7, pose=(-44.0, 18.0))
        c = rev_cues(st)
        self.example("Example 2: An exponential about the x-axis", r"The region under $y = e^x$ for $0 \le x \le 1$ is revolved about the $x$-axis. Find the volume.",
                     [r"TEXT:The region: under $y = e^x$, from $0$ to $1$", r"TEXT:One slice at $x$: a disc", r"R = e^x, \ \ R^2 = e^{2x}", r"V = \pi\int_0^1 e^{2x}\,dx",
                      r"= \pi\left[\tfrac12 e^{2x}\right]_0^1", r"= \tfrac\pi2\left(e^2 - 1\right) \approx 10.04"], at=[1, 2, 2, 2, 3, 3], figure=st, figure_at=1, size=42, ref=REF_X,
                     cues={0: c["both"](c["draw"](0, 1), c["shade"]()), 1: c["both"](c["spin"](rt=1.4, sweep=2.8, hold=1.0), c["slice"](rt=1.0)),
                           2: c["both"](c["rad"](), lambda sc: sc.wait(0.6), c["flat"](rt=1.4))})
        # Example 3: x^3, y = 8 and the y-axis, about the y-axis
        cube = lambda s: s ** 3
        cbrt = lambda y: np.cbrt(max(y, 0.0))
        st = rev_stage([(cube, 0, 2.03, FUNC, "y = x^3", (2.55, 6.2), "x")], outline_y(cbrt, ZERO, 0, 8), "y", 0.0, cbrt, (-2.6, 3.0), (-0.8, 9.4),
                       at=4.0, shade=(cbrt, ZERO, 0, 8, "y"), lines=[(0, 8, 2, 8, DIM, "y = 8", (2.75, 8.6))], ticks={"x": [-2, 2], "y": [8]}, scale=0.6, pose=(-24.0, 26.0), turn=-12.0)
        c = rev_cues(st)
        self.example("Example 3: A cubic about the y-axis", r"The region bounded by $y = x^3$, $y = 8$, and the $y$-axis is revolved about the $y$-axis. Find the volume.",
                     [r"TEXT:The region: between $y = x^3$ and the $y$-axis, below $y = 8$", r"TEXT:Horizontal discs: integrate in $y$ from $0$ to $8$.", r"x = y^{1/3}, \ \ R = y^{1/3}",
                      r"V = \pi\int_0^8 y^{2/3}\,dy", r"= \pi\left[\tfrac35 y^{5/3}\right]_0^8", r"= \pi \cdot \tfrac35 \cdot 32", r"= \tfrac{96\pi}{5} \approx 60.32"],
                     at=[1, 2, 2, 3, 3, 4, 4], figure=st, figure_at=1, size=42, ref=REF_Y,
                     cues={0: c["both"](c["draw"](0, 1), c["shade"]()), 1: c["both"](c["spin"](rt=1.4, sweep=2.8, hold=1.0), c["slice"](rt=1.0)),
                           2: c["both"](c["rad"](), lambda sc: sc.wait(0.6), c["flat"](rt=1.4))})
        self.finish()


def bead_view(st):
    """The view bead() draws with right now (it recenters on the solid's middle)."""
    v = st.view()
    return v.turned(origin=v.origin + (v.origin - v.P(2.0, 0, 0)))
