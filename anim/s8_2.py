"""Topic 8.2: Position, velocity, and acceleration with integrals. Narration comes from transcripts/8_2.md.

Adder's notes (2026-10-14): the car turns around to face west, it doesn't back up. Displacement is introduced as
"integrating a rate yields net change" (v is the rate of change of s). Total distance goes slowly: the odometer, the
integral of |v|, everything turned positive on the graph, |...| typed straight into Desmos, by hand the negative piece's
opposite; then |integral of v| versus integral of |v| shown with numbers. Example 1's graph has a real corner at (5, 0) so
the shading matches the segments.
"""
import numpy as np
from manim import *

from kit import *
from style import *
from props import car_sprite, face


def vel(s):
    return 2.2 * np.sin(1.1 * s) + 0.6


def turn_around(scene, car, run_time=0.7):
    """The car turns to face the other way (Adder: it turns around, it doesn't drive in reverse): it narrows to a sliver
    as it swings round, then widens again facing the new way."""
    scene.play(car.animate.stretch(0.06, 0), run_time=run_time / 2)
    car.stretch(-1, 0)
    car.facing = -car.facing
    scene.play(car.animate.stretch(1 / 0.06, 0), run_time=run_time / 2)


def odometer(n, digits=5):
    """A car's odometer: white digits in dark wheels, in a rounded bezel."""
    wheels = VGroup(*[VGroup(RoundedRectangle(width=0.46, height=0.62, corner_radius=0.05, stroke_width=0, fill_color="#222222", fill_opacity=1),
                             Text(d, font="DejaVu Sans Mono", color="#F4F4F4", font_size=34)) for d in str(n).rjust(digits, "0")])
    for w in wheels:
        w[1].move_to(w[0])
    wheels.arrange(RIGHT, buff=0.06)
    bezel = RoundedRectangle(width=wheels.width + 0.3, height=wheels.height + 0.26, corner_radius=0.12, stroke_color=DIM, stroke_width=3,
                             fill_color="#3A3A3A", fill_opacity=1).move_to(wheels)
    return VGroup(bezel, wheels)


class Lesson(TranscriptScene):
    NUM = "8.2"

    def construct(self):
        with self.beat("Out and back") as b:
            road = NumberLine(x_range=[-5, 35, 5], length=11, color=DIM, include_numbers=True, font_size=26).shift(DOWN * 0.6)
            car = car_sprite(1.1).next_to(road.n2p(0), UP, buff=0.05)
            odo = VGroup(T("odometer", 28, DIM), M("0", 40, INK)).arrange(DOWN, buff=0.1).to_corner(UR, buff=0.6)
            self.play(Create(road), FadeIn(car), FadeIn(odo), run_time=1)
            self.play(car.animate.next_to(road.n2p(30), UP, buff=0.05), Transform(odo[1], M("30", 40, INK).move_to(odo[1])), run_time=2)
            turn_around(self, car)
            self.play(car.animate.next_to(road.n2p(20), UP, buff=0.05), Transform(odo[1], M("40", 40, INK).move_to(odo[1])), run_time=1.2)
            b.line(1)
            disp = Arrow(road.n2p(0) + DOWN * 0.9, road.n2p(20) + DOWN * 0.9, buff=0, color=ACCUM, stroke_width=6)
            self.play(GrowArrow(disp), FadeIn(T("displacement: 20 miles", 32, ACCUM).next_to(disp, DOWN, buff=0.15)), run_time=1)
            b.line(2)
            self.play(Indicate(odo), FadeIn(T("distance: 40 miles", 32, INK).next_to(odo, DOWN, buff=0.2)), run_time=1)
        self.clear()
        self.title()

        with self.beat("Displacement is the integral of velocity") as b:
            rem = formula_box(VGroup(T("integrating a rate of change yields net change", 32, ACCUM),
                                     M(r"\int_a^b f'(t)\,dt = f(b) - f(a)", 40)).arrange(DOWN, buff=0.2), ACCUM).to_edge(UP, buff=0.5)
            self.play(FadeIn(rem), run_time=1)
            b.line(1)
            vr = VGroup(T("velocity $=$ rate of change of position", 32), M(r"v(t) = s'(t)", 40, DERIV)).arrange(RIGHT, buff=0.6).next_to(rem, DOWN, buff=0.5)
            self.play(FadeIn(vr), run_time=1)
            b.line(2)
            self.play(FadeOut(rem), vr.animate.to_edge(UP, buff=0.4), run_time=0.8)
            ax, al = plot_axes([0, 5.5, 1], [-2, 3.2, 1], w=5.8, h=3.6, coords=False, xlabel="t", ylabel="v")
            VGroup(ax, al).to_edge(LEFT, buff=0.5).shift(DOWN * 0.7)
            curve = ax.plot(vel, x_range=[0, 5.5], color=DERIV, stroke_width=4)
            board = VGroup(M(r"\int_a^b v(t)\,dt = s(b) - s(a)", 42), T("displacement: net change in position", 30, ACCUM),
                           T("where you end up, relative to where you started", 28, DIM)).arrange(DOWN, buff=0.3).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.5)
            self.play(FadeIn(ax), FadeIn(al), Create(curve), Write(board[0]), run_time=1.2)
            b.line(3)
            self.play(FadeIn(board[1:]), run_time=0.8)
            b.line(4)
            up = region(ax, lambda s: max(vel(s), 0), lambda s: 0, 0, 5.5, color=AREA)
            dn = region(ax, lambda s: 0, lambda s: min(vel(s), 0), 0, 5.5, color=TANGENT)
            self.play(FadeIn(up), FadeIn(dn), FadeIn(M("+", 48, AREA).move_to(ax.c2p(1.4, 1.2))), FadeIn(M("-", 48, TANGENT).move_to(ax.c2p(4.1, -0.7))), run_time=1)
        self.clear()

        with self.beat("Position from a starting point") as b:
            r1 = M(r"s(t) = s(0) + \int_0^t v(u)\,du", 50).shift(UP * 1.4)
            self.play(Write(r1), run_time=1)
            b.line(1)
            l1 = T("where you start", 28, FUNC).next_to(r1[0][5:9], DOWN, buff=0.5)
            l2 = T("how far you've moved since", 28, ACCUM).next_to(r1[0][10:], DOWN, buff=0.5)
            self.play(FadeIn(l1), FadeIn(l2), run_time=0.8)
            b.line(2)
            r2 = M(r"v(t) = v(0) + \int_0^t a(u)\,du", 50, DERIV).shift(DOWN * 1.6)
            self.play(Write(r2), run_time=1)
        self.clear()

        with self.beat("Total distance") as b:
            odo = odometer(30).to_edge(UP, buff=0.6)
            cap = T("odometer", 28, DIM).next_to(odo, DOWN, buff=0.15)
            self.play(FadeIn(odo), FadeIn(cap), run_time=0.8)
            b.line(1)
            car = car_sprite(1.0).next_to(odo, LEFT, buff=1.2)
            face(car, -1)
            self.play(FadeIn(car), run_time=0.4)
            self.play(car.animate.shift(LEFT * 2.2), Transform(odo, odometer(40).move_to(odo)), run_time=1.6)
            rule = T("total distance: travel in either direction adds", 34, INK).next_to(cap, DOWN, buff=0.35)
            self.play(FadeIn(rule), run_time=0.8)
            b.line(2)
            self.play(FadeOut(car), FadeOut(odo), FadeOut(cap), rule.animate.to_edge(UP, buff=0.4), run_time=0.8)
            ax, al = plot_axes([0, 5.5, 1], [-2, 3.2, 1], w=6, h=3.6, coords=False, xlabel="t", ylabel="")
            VGroup(ax, al).to_edge(LEFT, buff=0.5).shift(DOWN * 0.6)
            curve = ax.plot(vel, x_range=[0, 5.5], color=DERIV, stroke_width=4)
            vlab = M(r"v(t)", 32, DERIV).next_to(ax.c2p(1.4, vel(1.4)), UP, buff=0.12)
            up = region(ax, lambda s: max(vel(s), 0), lambda s: 0, 0, 5.5)
            dn = region(ax, lambda s: 0, lambda s: min(vel(s), 0), 0, 5.5, color=TANGENT)
            f1 = M(r"\text{total distance} = \int_a^b |v(t)|\,dt", 40).to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
            self.play(FadeIn(ax), FadeIn(al), Create(curve), FadeIn(vlab), FadeIn(up), FadeIn(dn), Write(f1), run_time=1.4)
            b.line(3)
            flip = ax.plot(lambda s: abs(vel(s)), x_range=[0, 5.5], color=DERIV, stroke_width=4)
            dn2 = region(ax, lambda s: abs(min(vel(s), 0)), lambda s: 0, 0, 5.5)
            self.play(Transform(curve, flip), Transform(dn, dn2), Transform(vlab, M(r"|v(t)|", 32, DERIV).move_to(vlab)), run_time=1.6)
            self.play(FadeIn(T("everything positive", 30, AREA).next_to(f1, DOWN, buff=0.5)), run_time=0.6)
        self.clear()

        with self.beat("Total distance by hand") as b:
            lt = T("On a calculator (Desmos)", 32, DIM).move_to([-3.6, 2.6, 0])
            entry = desmos_entry(r"\int_{0}^{5}|v(t)|\,dt").next_to(lt, DOWN, buff=0.35)
            self.play(FadeIn(lt), FadeIn(entry), run_time=1)
            b.line(1)
            rt = T("By hand", 32, DIM).move_to([3.4, 2.6, 0])
            ch = sign_chart(["c"], ["+", "-"], name="v", width=5.4, size=38).next_to(rt, DOWN, buff=0.4)
            self.play(FadeIn(rt), FadeIn(ch), run_time=1)
            b.line(2)
            split = M(r"\int_a^b |v(t)|\,dt", r"= \int_a^c v(t)\,dt", r"+ \left(-\int_c^b v(t)\,dt\right)", 42).move_to(DOWN * 1.2)
            split.set_max_width(12.4)
            br = Brace(split[2], DOWN, color=TANGENT)
            opp = T("the opposite of the negative piece", 30, TANGENT).next_to(br, DOWN, buff=0.1)
            self.play(Write(split), run_time=1.4)
            self.play(FadeIn(br), FadeIn(opp), run_time=0.8)
            b.line(3)
            self.play(Indicate(split[1:], color=AREA), run_time=1)
        self.clear()

        with self.beat("Not the absolute value of the integral") as b:
            ax, al = plot_axes([0, 5.5, 1], [-2, 3.2, 1], w=5.4, h=3.2, coords=False, xlabel="t", ylabel="v")
            VGroup(ax, al).move_to(UP * 1.6)
            curve = ax.plot(vel, x_range=[0, 5.5], color=DERIV, stroke_width=4)
            up = region(ax, lambda s: max(vel(s), 0), lambda s: 0, 0, 5.5)
            dn = region(ax, lambda s: 0, lambda s: min(vel(s), 0), 0, 5.5, color=TANGENT)
            self.play(FadeIn(ax), FadeIn(al), Create(curve), run_time=1)
            b.line(1)
            self.play(FadeIn(up), FadeIn(dn), FadeIn(M("30", 40, INK).move_to(ax.c2p(1.4, 1.1))), FadeIn(M("-10", 36, INK).move_to(ax.c2p(4.15, -0.55))), run_time=1)
            b.line(2)
            left = VGroup(M(r"\left|\int v\,dt\right| = |30 + (-10)| = |20| = 20", 38), T("the size of the displacement", 30, ACCUM)).arrange(DOWN, buff=0.2)
            right = VGroup(M(r"\int |v|\,dt = 30 + 10 = 40", 38), T("total distance", 30, AREA)).arrange(DOWN, buff=0.2)
            left.move_to([-3.5, -1.9, 0])
            right.move_to([3.7, -1.9, 0])
            self.play(Write(left[0]), run_time=1.4)
            self.play(FadeIn(left[1]), run_time=0.6)
            b.line(3)
            self.play(Write(right[0]), run_time=1.2)
            self.play(FadeIn(right[1]), FadeIn(M(r"\neq", 56, TANGENT).move_to([0.25, -1.9, 0])), run_time=0.6)
        self.clear()

        ch = staged_chart([2, 4], ["+", "-", "+"], words=["right", "left", "right"], name="v", width=6.5)
        self.example("Displacement and distance", r"A particle moves along a line with $v(t) = t^2 - 6t + 8$ for $0 \le t \le 5$, and $s(0) = 1$. Find (a) the displacement, (b) the position at $t = 5$, (c) the total distance.",
                     [r"\text{(a) } \int_0^5 \left(t^2 - 6t + 8\right) dt", r"= \left[\tfrac{t^3}{3} - 3t^2 + 8t\right]_0^5", r"= \tfrac{125}{3} - 75 + 40", r"= \tfrac{20}{3}",
                      r"\text{(b) } s(5) = 1 + \tfrac{20}{3} = \tfrac{23}{3}", r"\text{(c) } v = (t - 2)(t - 4)", r"t = 2, \ \ t = 4",
                      r"v(1) = 1 - 6 + 8 = 3 > 0", r"v(3) = 9 - 18 + 8 = -1 < 0", r"v(5) = 25 - 30 + 8 = 3 > 0",
                      r"\int_0^2 v\,dt = \tfrac{20}{3}", r"\int_2^4 v\,dt = -\tfrac43", r"\int_4^5 v\,dt = \tfrac43", r"\text{opposite of } -\tfrac43\!: \ \tfrac43",
                      r"\text{distance} = \tfrac{20}{3} + \tfrac43 + \tfrac43 = \tfrac{28}{3}"],
                     at=[1, 1, 2, 2, 3, 4, 4, 5, 5, 5, 6, 6, 6, 7, 8], size=42, figure=ch, figure_at=4,
                     cues={7: reveal_sign(ch, 0), 8: reveal_sign(ch, 1), 9: lambda sc: (reveal_sign(ch, 2)(sc), reveal_words(ch)(sc))}, follow=True)

        with self.beat("Close") as b:
            card = VGroup(M(r"\text{displacement} = \int v\,dt \ \ (\text{can cancel})", 40, ACCUM),
                          M(r"\text{total distance} = \int |v|\,dt \ \ (\text{never cancels})", 40, DERIV), T("split where $v$ changes sign", 32, DIM),
                          M(r"s(t) = s(0) + \int_0^t v", 40), M(r"v(t) = v(0) + \int_0^t a", 40)).arrange(DOWN, buff=0.4)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2.4)
        self.clear()

        self.examples_card()
        pts = [(0, 0), (2, 4), (4, 4), (5, 0), (6, -2), (8, -2)]    # (5, 0) is a corner: the shading's edge (Adder)
        ax, _ = plot_axes([0, 8.5, 1], [-3, 5, 1], w=5.4, h=3.6, xlabel="t", ylabel="v")
        vg = VGroup(*[Line(ax.c2p(*p), ax.c2p(*q), color=DERIV, stroke_width=4) for p, q in zip(pts, pts[1:])])
        fig1 = VGroup(ax, vg, Polygon(ax.c2p(0, 0), ax.c2p(2, 4), ax.c2p(4, 4), ax.c2p(5, 0), stroke_width=0, fill_color=AREA, fill_opacity=0.4),
                      Polygon(ax.c2p(5, 0), ax.c2p(6, -2), ax.c2p(8, -2), ax.c2p(8, 0), stroke_width=0, fill_color=TANGENT, fill_opacity=0.4))
        self.example("Example 1: From a velocity graph", r"The graph of $v$ is shown. Find the displacement and the total distance on $[0, 8]$.",
                     [r"\text{above} = \tfrac12(2)(4) + 2(4) + \tfrac12(1)(4) = 14", r"\text{below} = \tfrac12(1)(2) + 2(2) = 5", r"\text{displacement} = 14 - 5 = 9", r"\text{distance} = 14 + 5 = 19"],
                     at=[1, 2, 3, 3], figure=fig1,
                     text=r"The graph of $v$ on $[0, 8]$ is made of segments from $(0, 0)$ to $(2, 4)$, to $(4, 4)$, to $(5, 0)$, to $(6, -2)$, to $(8, -2)$. Find the displacement and the total distance on $[0, 8]$.",
                     notes_graph=dict(fns=[("2*x", 0, 2), ("4+0*x", 2, 4), ("4-4*(x-4)", 4, 5), ("-2*(x-5)", 5, 6), ("-2+0*x", 6, 8)], xr=(0, 8.5), yr=(-3, 5), xlabel="t", ylabel="v(t)"))
        ch2 = staged_chart([1], ["-", "+"], words=["left", "right"], name="v", width=5)
        self.example("Example 2: From acceleration", r"A particle has $a(t) = 6t$ and $v(0) = -3$. Find $v(t)$, then the total distance on $[0, 2]$.",
                     [r"v(t) = -3 + \int_0^t 6u\,du", r"= 3t^2 - 3", r"3t^2 - 3 = 0: \ t = 1 \ \ (t = -1 \text{ is outside})", r"\int_0^1 v\,dt = \left[t^3 - 3t\right]_0^1 = -2",
                      r"\int_1^2 v\,dt = 2 - (-2) = 4", r"\text{distance} = 2 + 4 = 6"], at=[1, 1, 2, 3, 3, 3], figure=ch2, figure_at=2,
                     cues={3: lambda sc: (reveal_sign(ch2, 0, 1)(sc), reveal_words(ch2)(sc))})
        self.example("Example 3: Working backward", r"A particle has $v(t) = 3t^2 - 2$, and $s(2) = 5$. Find $s(0)$.",
                     [r"s(2) = s(0) + \int_0^2 \left(3t^2 - 2\right) dt", r"5 = s(0) + \left[t^3 - 2t\right]_0^2", r"5 = s(0) + 4", r"s(0) = 1"], at=[1, 2, 2, 3])
        self.finish()
