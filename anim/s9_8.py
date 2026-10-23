"""Topic 9.8 (BC): Area of a polar region. Narration comes from transcripts/9_8.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "9.8"
    # the polar area formula and the identities it needs stay in the corner during every worked example (Adder, 2026-10-14)
    example_ref = (r"\begin{aligned}A &= \tfrac12\int_\alpha^\beta r^2\,d\theta\\ \cos^2\theta &= \tfrac12(1 + \cos 2\theta)\\"
                   r" \sin^2\theta &= \tfrac12(1 - \cos 2\theta)\end{aligned}")

    def construct(self):
        car = lambda s: 1 + np.cos(s)
        with self.beat("Slicing a pizza instead") as b:
            # the Riemann rectangles sit on a curve you can see, are built slowly and stay up (Adder, 2026-10-14)
            f = lambda x: 1.1 + 0.45 * np.sin(1.5 * x) + 0.12 * x
            ax, labs = plot_axes([0, 4.6, 1], [0, 2.4, 1], w=5.6, h=3.4, coords=False)
            VGroup(ax, labs).to_edge(LEFT, buff=0.6).shift(UP * 0.5)
            curve = ax.plot(f, x_range=[0, 4.4], color=FUNC, stroke_width=4)
            fl = M("y = f(x)", 32, FUNC).next_to(ax.c2p(4.4, f(4.4)), UP, buff=0.2)
            self.play(FadeIn(ax), FadeIn(labs), run_time=0.6)
            self.play(Create(curve), FadeIn(fl), run_time=1.5)
            edges = np.linspace(0.3, 3.6, 12)
            rects = riemann_boxes(ax, f, edges, "mid")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in rects], lag_ratio=0.5), run_time=3.2)
            b.line(1)
            hi = rects[-1]
            a0, a1 = edges[-2], edges[-1]
            h = f((a0 + a1) / 2)
            self.play(hi.animate.set_fill(SECANT, opacity=0.8).set_stroke(SECANT), run_time=0.6)
            hgt = nudge_arrow(ax.c2p(a1, 0), ax.c2p(a1, h), label="f(x)", side=RIGHT, color=SECANT, size=30, offset=0.15)
            wid = nudge_arrow(ax.c2p(a0, 0), ax.c2p(a1, 0), label=r"\Delta x", side=DOWN, color=SECANT, size=30, offset=0.15)
            self.play(FadeIn(hgt), run_time=0.8)
            self.play(FadeIn(wid), run_time=0.8)
            area = M(r"\text{area} \approx f(x)\,\Delta x", 36, SECANT).next_to(ax, DOWN, buff=0.75)
            self.play(FadeIn(area), run_time=0.7)
            b.line(2)
            px, _ = plot_axes([-0.8, 2.4, 1], [-1.6, 1.6, 1], w=4.2, h=4.2, coords=False)
            px.to_edge(RIGHT, buff=0.7).shift(UP * 0.3)
            reg = polar_region(px, car, 0, TAU)
            self.play(FadeIn(px), FadeIn(reg), Create(polar_curve(px, car, 0, TAU)), run_time=1.2)

            def half_height(x):
                s = np.linspace(0, PI, 400)
                ys = [car(v) * np.sin(v) for v in s if abs(car(v) * np.cos(v) - x) < 0.04]
                return max(ys) if ys else 0
            bad = VGroup(*[Rectangle(width=px.c2p(0.25, 0)[0] - px.c2p(0, 0)[0], height=2 * (px.c2p(0, half_height(x))[1] - px.c2p(0, 0)[1]),
                                     stroke_color=INK, stroke_width=3).move_to(px.c2p(x, 0)) for x in np.arange(-0.125, 2.0, 0.25)])
            self.play(LaggedStart(*[FadeIn(r) for r in bad], lag_ratio=0.3), run_time=1.8)
            b.line(3)
            pizza = VGroup(Circle(radius=1.3, stroke_color="#C68B59", stroke_width=8, fill_color="#F2C14E", fill_opacity=1),
                           *[Line(ORIGIN, 1.3 * np.array([np.cos(a), np.sin(a), 0]), color="#C68B59", stroke_width=3) for a in np.linspace(0, TAU, 9)[:-1]]).move_to(ax)
            self.play(FadeOut(VGroup(ax, labs, curve, fl, rects, hgt, wid, area, bad)), run_time=0.8)
            self.play(FadeIn(pizza), run_time=0.8)
            mid = lambda d: (lambda s: car(s + d / 2))          # radius at the middle of each wedge, so the fan hugs the curve
            wedges = VGroup(*[polar_wedge(px, mid(TAU / 36), k * TAU / 36, TAU / 36, color=SECANT if k % 2 else DERIV, opacity=0.55, arc=True) for k in range(36)])
            self.play(LaggedStart(*[FadeIn(w) for w in wedges], lag_ratio=0.4), run_time=4.0)
        self.clear()
        self.title()

        with self.beat("The area of a sector") as b:
            sec = VGroup(Circle(radius=1.8, color=DIM), Sector(radius=1.8, angle=0.7, fill_color=SECANT, fill_opacity=0.6, stroke_width=0),
                         M("r", 32).move_to([1.0, -0.25, 0]), M(r"\Delta\theta", 30, SECANT).move_to([0.75, 0.3, 0])).to_edge(LEFT, buff=1.4)
            self.play(FadeIn(sec), run_time=1)
            rows = VGroup(M(r"\text{whole circle: angle } 2\pi, \text{ area } \pi r^2", 36, DIM), M(r"\text{sector} = \tfrac{\Delta\theta}{2\pi}\cdot\pi r^2", 42),
                          M(r"= \tfrac12 r^2\,\Delta\theta", 42, SECANT)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.8)
            self.play(FadeIn(rows[0]), run_time=0.8)
            self.play(Write(rows[1]), run_time=1)
            b.line(1)
            self.play(Write(rows[2]), run_time=0.8)
        self.clear()

        with self.beat("Wedges under a polar curve") as b:
            # r is a function of theta: one slow wedge at angle theta with its own radius, then a few, then many (Adder, 2026-10-14)
            ax, _ = plot_axes([-0.6, 2.3, 1], [-1.5, 1.5, 1], w=5.1, h=5.25, coords=False)
            ax.to_edge(LEFT, buff=0.8)
            self.play(FadeIn(ax), Create(polar_curve(ax, car, 0, TAU)), run_time=1.5)
            self.play(FadeIn(M(r"r = 1 + \cos\theta", 32, FUNC).next_to(ax.c2p(1.5, -1.35), RIGHT, buff=0.1)), run_time=0.5)
            t0, dt = 0.75, 0.3
            O = ax.c2p(0, 0)
            ray = sample_r(ax, car, t0, label=r"r(\theta)", side=-1)
            self.play(Create(ray[0]), run_time=1.5)
            self.play(FadeIn(ray[1:]), run_time=0.6)
            th_arc = Arc(radius=0.55, start_angle=0, angle=t0, arc_center=O, color=INK, stroke_width=3)
            th_lab = M(r"\theta", 30).move_to(O + 0.85 * np.array([np.cos(t0 / 2), np.sin(t0 / 2), 0]))
            self.play(Create(th_arc), FadeIn(th_lab), run_time=0.8)
            b.line(1)
            P2 = ax.c2p(car(t0 + dt) * np.cos(t0 + dt), car(t0 + dt) * np.sin(t0 + dt))
            ray2 = Line(O, P2, color=DIM, stroke_width=3)
            self.play(Create(ray2), run_time=1.2)
            d_arc = Arc(radius=0.9, start_angle=t0, angle=dt, arc_center=O, color=DERIV, stroke_width=4)
            d_lab = M(r"\Delta\theta", 30, DERIV).move_to(O + 1.05 * np.array([np.cos(t0 + dt + 0.3), np.sin(t0 + dt + 0.3), 0]))
            self.play(Create(d_arc), FadeIn(d_lab), run_time=0.8)
            w0 = polar_wedge(ax, car, t0, dt, color=SECANT, opacity=0.55, arc=True)
            self.play(FadeIn(w0), run_time=1.5)
            b.line(2)
            est = M(r"\text{area} \approx \tfrac12\,[r(\theta)]^2\,\Delta\theta", 40, SECANT).to_edge(RIGHT, buff=0.6).shift(UP * 2.2)
            self.play(Write(est), run_time=1.2)
            b.line(3)
            self.play(FadeOut(VGroup(th_arc, th_lab, d_arc, d_lab, ray, ray2)), run_time=0.6)
            more = VGroup()
            for k in range(1, 4):
                t = t0 + k * dt
                w = polar_wedge(ax, car, t, dt, color=DERIV if k % 2 else SECANT, opacity=0.55, arc=True)
                rk = Line(O, ax.c2p(car(t) * np.cos(t), car(t) * np.sin(t)), color=INK, stroke_width=3)
                self.play(Create(rk), run_time=0.6)
                self.play(FadeIn(w), FadeOut(rk), run_time=0.9)
                more.add(w)
            b.line(4)
            self.play(FadeOut(w0), FadeOut(more), run_time=0.5)
            n = 60
            many = VGroup(*[polar_wedge(ax, lambda s: car(s + PI / n), k * TAU / n, TAU / n, color=SECANT if k % 2 else DERIV, opacity=0.55, arc=True) for k in range(n)])
            self.play(LaggedStart(*[FadeIn(w) for w in many], lag_ratio=0.3), run_time=4.0)
            b.line(5)
            box = formula_box(M(r"A = \tfrac12\int_\alpha^\beta r^2\,d\theta", 46, ACCUM), ACCUM).to_edge(RIGHT, buff=0.8).shift(DOWN * 0.6)
            self.play(FadeIn(box), run_time=0.8)
        self.clear()

        ax, _ = plot_axes([-0.8, 2.4, 1], [-1.6, 1.6, 1], w=3.4, h=3.4)
        sr = sample_r(ax, car, PI / 3, side=-1)
        fig = VGroup(ax, polar_region(ax, car, 0, TAU), polar_curve(ax, car, 0, TAU))
        self.example("The area inside a cardioid", r"Find the area inside $r = 1 + \cos\theta$.",
                     [r"\text{traced once for } 0 \le \theta \le 2\pi", r"A = \tfrac12\int_0^{2\pi} (1 + \cos\theta)^2\,d\theta", r"(1 + \cos\theta)^2 = 1 + 2\cos\theta + \cos^2\theta", r"\cos^2\theta = \tfrac12(1 + \cos 2\theta)",
                      r"= \tfrac32 + 2\cos\theta + \tfrac12\cos 2\theta", r"A = \tfrac12\left[\tfrac{3\theta}{2} + 2\sin\theta + \tfrac14\sin 2\theta\right]_0^{2\pi}", r"= \tfrac12(3\pi) = \tfrac{3\pi}{2} \approx 4.71"],
                     at=[1, 2, 3, 4, 5, 6, 6], figure=fig, follow=True, cues={1: draw_cue(sr, rt=1.2)}, overlays=[sr])

        with self.beat("Choosing the limits") as b:
            rose = lambda s: np.sin(2 * s)
            ax, _ = plot_axes([-1.2, 1.2, 1], [-1.2, 1.2, 1], w=4.6, h=4.6, coords=False)
            ax.to_edge(LEFT, buff=0.8)
            self.play(FadeIn(ax), Create(polar_curve(ax, rose, 0, TAU, color=DIM, width=3)), run_time=1)
            th = ValueTracker(0.01)
            rad = always_redraw(lambda: Line(ax.c2p(0, 0), ax.c2p(rose(th.get_value()) * np.cos(th.get_value()), rose(th.get_value()) * np.sin(th.get_value())), color=SECANT, stroke_width=4))
            self.add(rad)
            self.play(th.animate.set_value(PI / 2 - 0.01), FadeIn(polar_region(ax, rose, 0, PI / 2)), run_time=2)
            b.line(1)
            notes = VGroup(T("start and end where $r = 0$", 32), M(r"\sin 2\theta = 0: \ \theta = 0, \ \tfrac\pi2", 36, SECANT), T("trace the curve: each piece once", 30, DIM)).arrange(DOWN, buff=0.4).to_edge(RIGHT, buff=0.6)
            self.play(FadeIn(notes[:2]), run_time=1)
            b.line(2)
            self.play(FadeIn(notes[2]), run_time=0.6)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(M(r"\text{sector: } \tfrac12 r^2\,\Delta\theta", 40), formula_box(M(r"A = \tfrac12\int_\alpha^\beta r^2\,d\theta", 48, ACCUM), ACCUM), T("limits: where the sweep starts and stops (often $r = 0$)", 34),
                          M(r"\cos^2\theta = \tfrac12(1 + \cos 2\theta), \ \ \sin^2\theta = \tfrac12(1 - \cos 2\theta)", 34, DIM)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        # every worked example shows a sample r from the pole to the curve on its graph (Adder, 2026-10-14)
        self.examples_card()
        rose = lambda s: np.sin(2 * s)
        ax, _ = plot_axes([-1.2, 1.2, 1], [-1.2, 1.2, 1], w=3.2, h=3.2, coords=False)
        sr1 = sample_r(ax, rose, PI / 3, side=-1)
        fig1 = VGroup(ax, polar_curve(ax, rose, 0, TAU, color=DIM, width=3), polar_region(ax, rose, 0, PI / 2), polar_curve(ax, rose, 0, PI / 2))
        self.example("Example 1: One petal of a rose", r"Find the area of one petal of $r = \sin 2\theta$.",
                     [r"\text{one petal: } 0 \le \theta \le \tfrac\pi2", r"A = \tfrac12\int_0^{\pi/2} \sin^2 2\theta\,d\theta", r"\sin^2 2\theta = \tfrac12(1 - \cos 4\theta)", r"= \tfrac14\left[\theta - \tfrac14\sin 4\theta\right]_0^{\pi/2}",
                      r"= \tfrac14 \cdot \tfrac\pi2 = \tfrac\pi8 \approx 0.39"], at=[1, 1, 2, 3, 3], figure=fig1, cues={1: draw_cue(sr1, rt=1.0)}, overlays=[sr1])

        circ = lambda s: 4 * np.sin(s)
        ax, _ = plot_axes([-2.6, 2.6, 1], [-0.6, 4.6, 1], w=3.4, h=3.4, coords=False)
        sr2 = sample_r(ax, circ, PI / 3, side=-1)
        fig2 = VGroup(ax, polar_region(ax, circ, 0, PI), polar_curve(ax, circ, 0, PI))
        self.example("Example 2: A circle, checked", r"Find the area inside $r = 4\sin\theta$.",
                     [r"\text{traced once for } 0 \le \theta \le \pi", r"A = \tfrac12\int_0^\pi 16\sin^2\theta\,d\theta", r"= 8 \cdot \tfrac12\int_0^\pi (1 - \cos 2\theta)\,d\theta", r"= 4\pi", r"\text{check: radius } 2: \ \pi(2)^2 = 4\pi"],
                     at=[1, 2, 2, 2, 3], figure=fig2, cues={1: draw_cue(sr2, rt=1.0)}, overlays=[sr2])

        spiral = lambda s: s
        ax, _ = plot_axes([-3.4, 1.0, 1], [-0.6, 2.4, 1], w=4.4, h=3.0, coords=False)
        sr3 = sample_r(ax, spiral, 2 * PI / 3, side=1)
        fig3 = VGroup(ax, polar_region(ax, spiral, 0, PI), polar_curve(ax, spiral, 0, PI))
        self.example("Example 3: A spiral's sweep", r"Find the area swept out by the spiral $r = \theta$ for $0 \le \theta \le \pi$.",
                     [r"A = \tfrac12\int_0^\pi \theta^2\,d\theta", r"= \tfrac12\left[\tfrac{\theta^3}{3}\right]_0^\pi", r"= \tfrac{\pi^3}{6} \approx 5.17"], at=[1, 1, 2],
                     figure=fig3, cues={0: draw_cue(sr3, rt=1.0)}, overlays=[sr3])
        self.finish()
