"""Topic 10.6 (BC): Comparison tests. Narration comes from transcripts/10_6.md."""
import numpy as np
from manim import *

from kit import *
from props import car_sprite, empire_state_building, lamppost, person_walking
from style import *


class Lesson(TranscriptScene):
    NUM = "10.6"

    def construct(self):
        with self.beat("A ceiling and a floor") as b:
            # Adder (2026-10-14): comparison as a bounding line. Our series is bars, the known one dots with a faint
            # dashed guide through them; both stay discrete (one mark per n)
            def panel(xr, yr, ns, known, ours, kc, oc, klab, olab):
                ax, al = plot_axes(xr, yr, w=5.6, h=3.9, xlabel="n", ylabel="", font=24)
                ux = ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]
                bars = VGroup(*[Rectangle(width=0.32 * ux, height=ax.c2p(0, ours(k))[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=oc, fill_opacity=0.85)
                                .move_to(ax.c2p(k, 0), aligned_edge=DOWN) for k in ns])
                # the guide starts where it enters the graph, so it never runs off the top
                x0 = max(ns[0] - 0.4, next(x for x in np.linspace(0.3, ns[0], 400) if known(x) <= 0.97 * yr[1]))
                guide = DashedVMobject(ax.plot(known, x_range=[x0, ns[-1] + 0.4], color=kc, stroke_width=2.5), num_dashes=34).set_stroke(opacity=0.5)
                dots = VGroup(*[Dot(ax.c2p(k, known(k)), radius=0.07, color=kc) for k in ns])
                labs = VGroup(T(klab, 28, kc), T(olab, 28, oc)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(ax, UP, buff=0.25)
                return VGroup(ax, al), bars, VGroup(guide, dots), labs
            A = panel([0, 10.5, 2], [0, 1.1, 0.5], list(range(1, 11)), lambda s: 1 / s**2, lambda s: 1 / (s**2 + 3), DERIV, ACCUM,
                      r"known: $\sum \frac{1}{n^2}$ is finite", r"ours: $a_n = \frac{1}{n^2 + 3}$")
            B = panel([0, 16, 2], [0, 0.4, 0.2], list(range(4, 16)), lambda s: 1 / s, lambda s: np.log(s) / s, SECANT, TANGENT,
                      r"known: $\sum \frac1n$ is infinite", r"ours: $a_n = \frac{\ln n}{n}$")
            VGroup(VGroup(*A), VGroup(*B)).arrange(RIGHT, buff=0.9)
            VGroup(*B).shift(UP * (A[0][0].get_bottom()[1] - B[0][0].get_bottom()[1]))     # both x-axes on one line
            VGroup(*A, *B).shift(DOWN * 0.15)
            self.play(FadeIn(A[0]), run_time=0.6)
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in A[1]], lag_ratio=0.12), FadeIn(A[3][1]), run_time=1.4)
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in A[2][1]], lag_ratio=0.12), run_time=1.2)
            self.play(Create(A[2][0]), FadeIn(A[3][0]), run_time=1)
            b.line(1)
            capA = T("under a finite ceiling: finite", 30, ACCUM).next_to(A[0], DOWN, buff=0.3)
            self.play(Indicate(A[2][1], color=DERIV, scale_factor=1.3), FadeIn(capA), run_time=1.2)
            b.line(2)
            self.play(FadeIn(B[0]), FadeIn(B[2]), FadeIn(B[3][0]), run_time=1)
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in B[1]], lag_ratio=0.1), FadeIn(B[3][1]), run_time=1.4)
            capB = T("over an infinite floor: infinite", 30, TANGENT).next_to(B[0], DOWN, buff=0.3)
            self.play(FadeIn(capB), run_time=0.6)
            b.line(3)
        self.clear()
        self.title()

        with self.beat("Direct comparison") as b:
            box = formula_box(VGroup(M(r"0 \le a_n \le b_n:", 38), M(r"\sum b_n \text{ converges},\ \text{so}\ \sum a_n \text{ converges}", 36), M(r"\sum a_n \text{ diverges},\ \text{so}\ \sum b_n \text{ diverges}", 36)).arrange(DOWN, buff=0.2), ACCUM).to_edge(UP, buff=0.6)
            self.play(FadeIn(box), run_time=1.2)
            b.line(1)
            w1 = T("smaller than something small (convergent): small, so it converges", 32, DERIV).next_to(box, DOWN, buff=0.6)
            self.play(FadeIn(w1), run_time=0.8)
            b.line(2)
            w2 = T("bigger than something big (divergent): big, so it diverges", 32, SECANT).next_to(w1, DOWN, buff=0.4)
            self.play(FadeIn(w2), run_time=0.8)
        self.clear()

        with self.beat("When it settles nothing") as b:
            # Adder: spend extra beats on the cases that settle nothing
            def row(left, right, col, mark):
                return VGroup(M(mark, 40, col), T(left, 36), T(right, 36, col))
            rows = VGroup(row("smaller than small:", "converges", ACCUM, r"\checkmark"), row("bigger than big:", "diverges", ACCUM, r"\checkmark"),
                          row("bigger than small:", "tells you nothing", TANGENT, r"\times"), row("smaller than big:", "tells you nothing", TANGENT, r"\times"))
            for r_ in rows:
                r_[1].next_to(r_[0], RIGHT, buff=0.35)
                r_[2].next_to(r_[0], RIGHT, buff=0.35 + 4.4)
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to(UP * 0.5)
            for r_ in rows:                    # one column for the words, one for the verdicts
                r_[1].set_x(rows[0][0].get_right()[0] + 0.35 + r_[1].width / 2)
                r_[2].set_x(rows[0][0].get_right()[0] + 4.75 + r_[2].width / 2)
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), run_time=0.8)
            self.play(FadeIn(rows[2]), run_time=0.8)
            self.play(Indicate(rows[2][2], color=TANGENT), run_time=1)
            b.line(1)
            self.play(FadeIn(rows[3]), run_time=0.8)
            self.play(Indicate(rows[3][2], color=TANGENT), run_time=1)
            b.line(2)
            frame = SurroundingRectangle(VGroup(rows[2], rows[3]), color=TANGENT, buff=0.2, corner_radius=0.1)
            lab = T("settles nothing", 40, TANGENT).next_to(frame, DOWN, buff=0.35)
            self.play(Create(frame), FadeIn(lab), run_time=1)
        self.clear()

        with self.beat("The Empire State Building") as b:
            # Adder's example: bigger than the Empire State Building means huge; smaller doesn't say much
            gy = -3.25
            grd = Line([-6.8, gy, 0], [6.8, gy, 0], color=DIM, stroke_width=3)
            esb = empire_state_building(5.9).move_to([-5.0, gy, 0], aligned_edge=DOWN)
            meas = DoubleArrow([-3.85, gy, 0], [-3.85, esb.get_top()[1], 0], buff=0, color=DIM, stroke_width=3, tip_length=0.18)
            ft = T("1,454 ft", 30, DIM).next_to(meas, RIGHT, buff=0.15).shift(UP * 1.2)
            self.play(Create(grd), FadeIn(esb, shift=UP * 0.2), run_time=1)
            self.play(GrowFromCenter(meas), FadeIn(ft), run_time=0.8)
            big = T("bigger than it: huge", 38, ACCUM).move_to([2.2, 2.9, 0])
            self.play(FadeIn(big), run_time=0.8)
            b.line(1)
            small = T("smaller than it: a person? a car? a lamppost?", 34, SECANT).next_to(big, DOWN, buff=0.45).set_x(2.2)
            things = Group(person_walking(1.2), car_sprite(1.7), lamppost(2.3))
            for k, (th, x) in enumerate(zip(things, [-1.4, 0.9, 3.6])):
                th.move_to([x, gy, 0], aligned_edge=DOWN)
            nts = T("(not to scale)", 24, DIM).move_to([1.2, gy - 0.3, 0])
            self.play(FadeIn(small), LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in things], lag_ratio=0.3), FadeIn(nts), run_time=1.4)
            b.line(2)
            bound = T("all under 1,454 feet: at least a finite bound", 32).next_to(small, DOWN, buff=0.4).set_x(2.2)
            self.play(FadeIn(bound), run_time=0.8)
            b.line(3)
            self.play(FadeOut(things), FadeOut(nts), FadeOut(small), FadeOut(bound), run_time=0.6)
            sky = Arrow([-1.6, gy, 0], [-1.6, 3.55, 0], buff=0, color=TANGENT, stroke_width=10, max_tip_length_to_length_ratio=0.06)
            inf = T(r"infinitely tall", 32, TANGENT).next_to(sky.get_top(), RIGHT, buff=0.25).shift(DOWN * 0.35)
            self.play(GrowArrow(sky), run_time=1.0)
            self.play(FadeIn(inf), FadeOut(big), run_time=0.6)
            no1 = T("smaller than this: no bound at all", 34, TANGENT).move_to([2.5, 1.2, 0])
            no2 = T("bigger than something small:\\\\could still be anything", 34, TANGENT).next_to(no1, DOWN, buff=0.6)
            self.play(FadeIn(no1), run_time=0.8)
            self.play(FadeIn(no2), run_time=0.8)
        self.clear()

        # the direct comparison test stays up in the corner through its worked examples (Adder: formulas stay on screen)
        self.example_ref = r"\begin{aligned}&0 \le a_n \le b_n\text{:}\\ &\textstyle\sum b_n \text{ converges, so}\\ &\qquad\textstyle\sum a_n \text{ converges}\\ &\textstyle\sum a_n \text{ diverges, so}\\ &\qquad\textstyle\sum b_n \text{ diverges}\end{aligned}"
        self.example("A direct comparison", r"Does $\displaystyle\sum_{n=1}^{\infty} \frac{1}{n^2 + 3}$ converge?",
                     [r"n^2 + 3 > n^2, \ \text{so} \ \frac{1}{n^2 + 3} < \frac{1}{n^2}", r"\sum \frac{1}{n^2} \text{ converges } (p = 2)", r"TEXT:By direct comparison, $\sum \frac{1}{n^2 + 3}$ converges."], at=[1, 2, 3], follow=True)

        with self.beat("Limit comparison") as b:
            box = formula_box(M(r"a_n, b_n > 0, \ \lim \frac{a_n}{b_n} = c, \ 0 < c < \infty: \ \text{same behavior}", 38, ACCUM).set_max_width(11), ACCUM).to_edge(UP, buff=0.5)
            self.play(FadeIn(box), run_time=1)
            b.line(1)
            rows = VGroup(M(r"\sum \frac{2n + 1}{n^3 - n + 5}: \ b_n = \frac{n}{n^3} = \frac{1}{n^2}", 38), M(r"\lim \frac{(2n + 1)/(n^3 - n + 5)}{1/n^2} = \lim \frac{2n^3 + n^2}{n^3 - n + 5} = 2", 38),
                          M(r"0 < 2 < \infty, \ \sum \tfrac{1}{n^2} \text{ converges: converges}", 38, ACCUM)).arrange(DOWN, buff=0.45).next_to(box, DOWN, buff=0.6)
            self.play(Write(rows[0]), run_time=1)
            b.line(2)
            self.play(Write(rows[1]), run_time=1.2)
            b.line(3)
            self.play(Write(rows[2]), run_time=1)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(T("direct: smaller than small converges; bigger than big diverges", 32), T("bigger than small, or smaller than big: settles nothing", 32, TANGENT), T("limit: $\\lim \\frac{a_n}{b_n} = c$, $0 < c < \\infty$: same behavior", 34, ACCUM),
                          T("compare with $p$-series or geometric series; build $b_n$ from the dominant terms", 30, DIM)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Bigger than harmonic", r"Does $\displaystyle\sum_{n=3}^{\infty} \frac{\ln n}{n}$ converge?", [r"n \ge 3: \ \ln n > 1, \ \text{so} \ \frac{\ln n}{n} > \frac1n", r"\sum \tfrac1n \text{ diverges}", r"\text{diverges by direct comparison}"], at=[1, 2, 2])
        self.example("Example 2: A bounded numerator", r"Does $\displaystyle\sum_{n=1}^{\infty} \frac{\sin^2 n}{n^2}$ converge?", [r"0 \le \sin^2 n \le 1, \ \text{so} \ 0 \le \frac{\sin^2 n}{n^2} \le \frac{1}{n^2}", r"\sum \tfrac{1}{n^2} \text{ converges}", r"\text{converges by direct comparison}"], at=[1, 2, 2])
        lim_ref = r"\begin{aligned}&a_n, b_n > 0,\ \lim \tfrac{a_n}{b_n} = c,\\ &0 < c < \infty\text{: same behavior}\end{aligned}"
        self.example("Example 3: Limit comparison with a geometric series", r"Does $\displaystyle\sum_{n=1}^{\infty} \frac{1}{2^n - 1}$ converge?",
                     [r"b_n = \frac{1}{2^n}", r"TEXT:Direct comparison goes the wrong way: $\frac{1}{2^n - 1} > \frac{1}{2^n}$.", r"\lim \frac{1/(2^n - 1)}{1/2^n} = \lim \frac{2^n}{2^n - 1} = 1", r"0 < 1 < \infty, \ \sum \tfrac{1}{2^n} \text{ converges: converges}"], at=[1, 1, 2, 3], ref=lim_ref)
        self.finish()
