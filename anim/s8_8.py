"""Topic 8.8: Volumes with triangle and semicircle cross sections. Narration comes from transcripts/8_8.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "8.8"

    def construct(self):
        par = lambda s: 4 - s * s
        zero = lambda s: 0.0
        with self.beat("Same base, new shapes") as b:
            P = oblique(origin=DOWN * 1.6, sx=1.3, sy=0.55)
            xs = np.linspace(-1.8, 1.8, 11)
            self.play(FadeIn(oblique_axes(P, (-2.6, 2.8), (-0.3, 4.6))), FadeIn(base_region(P, par, zero, -2, 2)), Create(base_curve(P, par, -2, 2)), run_time=1)
            sol = sections(P, par, zero, xs, "square", squash=0.8)
            self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in sol], lag_ratio=0.08), run_time=1.4)
            b.line(1)
            for kind, col in (("equilateral", SECANT), ("semicircle", DERIV)):
                new = sections(P, par, zero, xs, kind, squash=0.8, color=col)
                self.play(ReplacementTransform(sol, new), run_time=1.2)
                sol = new
            b.line(2)
            self.play(FadeIn(M(r"V = \int A(x)\,dx", 44, ACCUM).to_edge(UP, buff=0.5)), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("Areas from the side s") as b:
            s = 2.4
            def shape(kind, color):
                p0, p1 = LEFT * s / 2, RIGHT * s / 2
                g = VGroup(cross_section(kind, p0, p1, color=color), M("s", 30, INK).next_to(ORIGIN, DOWN, buff=0.15))
                return g
            eq = shape("equilateral", SECANT)
            eq.add(DashedLine(ORIGIN, UP * s * 0.866, color=DIM), M(r"\tfrac{\sqrt3}{2}s", 26, DIM).next_to(UP * s * 0.43, RIGHT, buff=0.08))
            sc = shape("semicircle", DERIV)
            sc.add(Line(ORIGIN, UP * s / 2 * 0.0 + RIGHT * s / 2, color=TANGENT, stroke_width=4), M(r"r = \tfrac s2", 26, TANGENT).next_to(RIGHT * s / 4, UP, buff=0.1))
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

        P = oblique(origin=LEFT * 0.2 + DOWN * 1.2, sx=0.9, sy=0.45)
        fig = VGroup(oblique_axes(P, (-2.5, 2.7), (-0.3, 4.6)), base_region(P, par, zero, -2, 2), base_curve(P, par, -2, 2), sections(P, par, zero, np.linspace(-1.8, 1.8, 9), "semicircle", color=DERIV))
        self.example("Semicircles on a parabola", r"The base of a solid is the region between $y = 4 - x^2$ and the $x$-axis. Cross sections perpendicular to the $x$-axis are semicircles. Find the volume.",
                     [r"4 - x^2 = 0 \text{ at } x = \pm2", r"s(x) = 4 - x^2", r"r = \tfrac s2 = \tfrac{4 - x^2}{2}", r"A(x) = \tfrac12\pi r^2 = \tfrac\pi8\left(4 - x^2\right)^2",
                      r"\left(4 - x^2\right)^2 = 16 - 8x^2 + x^4", r"V = \tfrac\pi8\int_{-2}^{2} \left(16 - 8x^2 + x^4\right) dx", r"= \tfrac\pi8 \cdot 2\left(32 - \tfrac{64}{3} + \tfrac{32}{5}\right)",
                      r"= \tfrac\pi8 \cdot \tfrac{512}{15}", r"= \tfrac{64\pi}{15} \approx 13.40"], at=[1, 1, 2, 3, 4, 5, 5, 5, 6], figure=fig, follow=True)

        with self.beat("Leg or hypotenuse?") as b:
            s = 2.6
            leg = VGroup(cross_section("isosceles_right", LEFT * s / 2, RIGHT * s / 2, color=ACCUM), M("s", 30).next_to(ORIGIN, DOWN, buff=0.15), M("s", 30).next_to(LEFT * s / 2 + UP * s / 2, LEFT, buff=0.15))
            hyp = VGroup(cross_section("isosceles_hyp", LEFT * s / 2, RIGHT * s / 2, color=SECANT), M("s", 30).next_to(ORIGIN, DOWN, buff=0.15),
                         M(r"\tfrac{s}{\sqrt2}", 28).next_to(LEFT * s / 4 + UP * s / 4, UL, buff=0.05))
            VGroup(leg, hyp).arrange(RIGHT, buff=2.2).shift(UP * 0.8)
            self.play(FadeIn(leg), FadeIn(hyp), run_time=1)
            b.line(1)
            self.play(Write(M(r"\text{leg on base: } \tfrac12 s^2", 36, ACCUM).next_to(leg, DOWN, buff=0.5)), run_time=1)
            b.line(2)
            self.play(Write(M(r"\text{hypotenuse on base: } \tfrac12\left(\tfrac{s}{\sqrt2}\right)^2 = \tfrac14 s^2", 36, SECANT).next_to(hyp, DOWN, buff=0.5)), run_time=1.2)
            self.play(FadeIn(T("read which side is on the base", 32, TANGENT).to_edge(DOWN, buff=0.5)), run_time=0.8)
        self.clear()

        with self.beat("Close") as b:
            tab = table([r"\text{shape (side } s \text{ on the base)}", r"A"], [[r"\text{square}", r"s^2"], [r"\text{equilateral triangle}", r"\tfrac{\sqrt3}{4}s^2"],
                        [r"\text{isosceles right, leg on base}", r"\tfrac12 s^2"], [r"\text{isosceles right, hypotenuse on base}", r"\tfrac14 s^2"], [r"\text{semicircle, diameter on base}", r"\tfrac\pi8 s^2"]], size=34).shift(UP * 0.5)
            self.play(FadeIn(tab), run_time=1.4)
            self.play(FadeIn(M(r"V = \int A(x)\,dx, \quad s = \text{top} - \text{bottom}", 40, ACCUM).next_to(tab, DOWN, buff=0.5)), run_time=0.8)
        self.clear()

        self.examples_card()
        P = oblique(origin=LEFT * 0.2 + DOWN * 1.0, sx=1.0, sy=0.8)
        fig1 = VGroup(oblique_axes(P, (-0.2, 4.6), (-0.2, 2.5)), base_region(P, np.sqrt, zero, 0, 4), base_curve(P, np.sqrt, 0, 4.3), sections(P, np.sqrt, zero, np.linspace(0.25, 4, 10), "equilateral", color=SECANT))
        self.example("Example 1: Equilateral triangles", r"The base is the region under $y = \sqrt x$ for $0 \le x \le 4$. Cross sections perpendicular to the $x$-axis are equilateral triangles. Find the volume.",
                     [r"s = \sqrt x", r"A(x) = \tfrac{\sqrt3}{4}\left(\sqrt x\right)^2 = \tfrac{\sqrt3}{4}x", r"V = \tfrac{\sqrt3}{4}\int_0^4 x\,dx", r"= \tfrac{\sqrt3}{4}(8)", r"= 2\sqrt3 \approx 3.46"],
                     at=[1, 1, 2, 2, 2], figure=fig1)
        P = oblique(origin=LEFT * 0.2 + DOWN * 0.6, sx=0.8, sy=0.5)
        circ_t = lambda s: np.sqrt(max(4 - s * s, 0))
        circ_b = lambda s: -circ_t(s)
        fig2 = VGroup(oblique_axes(P, (-2.5, 2.7), (-2.5, 2.7)), base_region(P, circ_t, circ_b, -2, 2), base_curve(P, circ_t, -2, 2), base_curve(P, circ_b, -2, 2),
                      sections(P, circ_t, circ_b, np.linspace(-1.8, 1.8, 9), "isosceles_hyp", color=SECANT))
        self.example("Example 2: Hypotenuse on a disk", r"The base is the disk $x^2 + y^2 \le 4$. Cross sections perpendicular to the $x$-axis are isosceles right triangles with the hypotenuse on the base. Find the volume.",
                     [r"\text{top } y = \sqrt{4 - x^2}, \ \ \text{bottom } y = -\sqrt{4 - x^2}", r"s = 2\sqrt{4 - x^2}", r"A = \tfrac14 s^2 = \tfrac14 \cdot 4\left(4 - x^2\right) = 4 - x^2",
                      r"V = \int_{-2}^{2} \left(4 - x^2\right) dx", r"= \tfrac{32}{3}"], at=[1, 1, 2, 3, 3], figure=fig2)
        P = oblique(origin=LEFT * 0.2 + DOWN * 1.0, sx=1.6, sy=0.6)
        fig3 = VGroup(oblique_axes(P, (-0.2, 2.4), (-0.2, 4.4)), base_region(P, lambda s: 2 * s, lambda s: s * s, 0, 2), base_curve(P, lambda s: 2 * s, 0, 2.1), base_curve(P, lambda s: s * s, 0, 2.05, DERIV),
                      sections(P, lambda s: 2 * s, lambda s: s * s, np.linspace(0.2, 1.8, 9), "isosceles_right"))
        self.example("Example 3: Leg on the base", r"The base is the region between $y = 2x$ and $y = x^2$. Cross sections perpendicular to the $x$-axis are isosceles right triangles with a leg on the base. Find the volume.",
                     [r"TEXT:The curves meet at $x = 0$ and $x = 2$; $2x$ is on top.", r"s = 2x - x^2", r"A = \tfrac12 s^2 = \tfrac12\left(2x - x^2\right)^2", r"\left(2x - x^2\right)^2 = 4x^2 - 4x^3 + x^4",
                      r"V = \tfrac12\int_0^2 \left(4x^2 - 4x^3 + x^4\right) dx", r"= \tfrac12\left(\tfrac{32}{3} - 16 + \tfrac{32}{5}\right)", r"= \tfrac12 \cdot \tfrac{16}{15} = \tfrac{8}{15}"],
                     at=[1, 1, 1, 2, 2, 2, 3], figure=fig3)
        self.finish()
