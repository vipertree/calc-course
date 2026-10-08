"""Topic 9.8 (BC): Area of a polar region. Narration comes from transcripts/9_8.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "9.8"

    def construct(self):
        car = lambda s: 1 + np.cos(s)
        with self.beat("Slicing a pizza instead") as b:
            ax, _ = plot_axes([-0.8, 2.4, 1], [-1.6, 1.6, 1], w=5, h=5, coords=False)
            ax.shift(LEFT * 2)
            self.play(FadeIn(ax), FadeIn(polar_region(ax, car, 0, TAU)), Create(polar_curve(ax, car, 0, TAU)), run_time=1)
            rects = VGroup(*[Rectangle(width=0.18, height=0.4 + 1.6 * abs(np.sin(k)), stroke_color=DIM, stroke_width=2).move_to(ax.c2p(-0.2 + 0.25 * k, 0)) for k in range(10)])
            self.play(FadeIn(rects), run_time=0.8)
            self.play(FadeOut(rects), run_time=0.6)
            b.line(1)
            wedges = VGroup(*[polar_wedge(ax, car, k * TAU / 24, TAU / 24, color=SECANT if k % 2 else DERIV, opacity=0.55) for k in range(24)])
            self.play(LaggedStart(*[FadeIn(w) for w in wedges], lag_ratio=0.05), run_time=1.6)
            b.line(2)
            pizza = VGroup(Circle(radius=1.2, stroke_color="#C68B59", stroke_width=8, fill_color="#F2C14E", fill_opacity=1), *[Line(ORIGIN, 1.2 * np.array([np.cos(a), np.sin(a), 0]), color="#C68B59", stroke_width=3) for a in np.linspace(0, TAU, 9)[:-1]]).to_edge(RIGHT, buff=1)
            self.play(FadeIn(pizza), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("The area of a sector") as b:
            sec = VGroup(Circle(radius=1.6, color=DIM), Sector(radius=1.6, angle=0.7, fill_color=SECANT, fill_opacity=0.6, stroke_width=0), M("r", 30).move_to([0.9, -0.2, 0]), M(r"\Delta\theta", 28, SECANT).move_to([0.75, 0.3, 0])).to_edge(LEFT, buff=1).shift(UP * 1)
            self.play(FadeIn(sec), run_time=1)
            rows = VGroup(M(r"\text{sector} = \tfrac{\Delta\theta}{2\pi}\cdot\pi r^2", 40), M(r"= \tfrac12 r^2\,\Delta\theta", 40)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.8).shift(UP * 1.4)
            self.play(Write(rows[0]), run_time=1)
            b.line(1)
            self.play(Write(rows[1]), run_time=0.8)
            b.line(2)
            ax, _ = plot_axes([-0.8, 2.4, 1], [-1.6, 1.6, 1], w=3.2, h=3.2, coords=False)
            ax.to_edge(LEFT, buff=1).shift(DOWN * 1.6)
            self.play(FadeIn(ax), Create(polar_curve(ax, car, 0, TAU)), FadeIn(polar_wedge(ax, car, 0.6, 0.2)), FadeIn(M(r"\approx \tfrac12 [f(\theta)]^2\,\Delta\theta", 36).next_to(ax, RIGHT, buff=0.4)), run_time=1)
            b.line(3)
            self.play(FadeIn(formula_box(M(r"A = \tfrac12\int_\alpha^\beta r^2\,d\theta", 46, ACCUM), ACCUM).to_edge(RIGHT, buff=0.6).shift(DOWN * 1.8)), run_time=0.8)
        self.clear()

        ax, _ = plot_axes([-0.8, 2.4, 1], [-1.6, 1.6, 1], w=3.4, h=3.4)
        fig = VGroup(ax, polar_region(ax, car, 0, TAU), polar_curve(ax, car, 0, TAU))
        self.example("The area inside a cardioid", r"Find the area inside $r = 1 + \cos\theta$.",
                     [r"\text{traced once for } 0 \le \theta \le 2\pi", r"A = \tfrac12\int_0^{2\pi} (1 + \cos\theta)^2\,d\theta", r"(1 + \cos\theta)^2 = 1 + 2\cos\theta + \cos^2\theta", r"\cos^2\theta = \tfrac12(1 + \cos 2\theta)",
                      r"= \tfrac32 + 2\cos\theta + \tfrac12\cos 2\theta", r"A = \tfrac12\left[\tfrac{3\theta}{2} + 2\sin\theta + \tfrac14\sin 2\theta\right]_0^{2\pi}", r"= \tfrac12(3\pi) = \tfrac{3\pi}{2} \approx 4.71"],
                     at=[1, 2, 2, 3, 4, 5, 5], figure=fig, follow=True)

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

        self.examples_card()
        ax, _ = plot_axes([-1.2, 1.2, 1], [-1.2, 1.2, 1], w=3.2, h=3.2, coords=False)
        fig1 = VGroup(ax, polar_curve(ax, lambda s: np.sin(2 * s), 0, TAU, color=DIM, width=3), polar_region(ax, lambda s: np.sin(2 * s), 0, PI / 2))
        self.example("Example 1: One petal of a rose", r"Find the area of one petal of $r = \sin 2\theta$.",
                     [r"\text{one petal: } 0 \le \theta \le \tfrac\pi2", r"A = \tfrac12\int_0^{\pi/2} \sin^2 2\theta\,d\theta", r"\sin^2 2\theta = \tfrac12(1 - \cos 4\theta)", r"= \tfrac14\left[\theta - \tfrac14\sin 4\theta\right]_0^{\pi/2}",
                      r"= \tfrac14 \cdot \tfrac\pi2 = \tfrac\pi8 \approx 0.39"], at=[1, 1, 2, 3, 3], figure=fig1)
        self.example("Example 2: A circle, checked", r"Find the area inside $r = 4\sin\theta$.",
                     [r"\text{traced once for } 0 \le \theta \le \pi", r"A = \tfrac12\int_0^\pi 16\sin^2\theta\,d\theta", r"= 8 \cdot \tfrac12\int_0^\pi (1 - \cos 2\theta)\,d\theta", r"= 4\pi", r"\text{check: radius } 2: \ \pi(2)^2 = 4\pi"],
                     at=[1, 2, 2, 2, 3])
        self.example("Example 3: A spiral's sweep", r"Find the area swept out by the spiral $r = \theta$ for $0 \le \theta \le \pi$.",
                     [r"A = \tfrac12\int_0^\pi \theta^2\,d\theta", r"= \tfrac12\left[\tfrac{\theta^3}{3}\right]_0^\pi", r"= \tfrac{\pi^3}{6} \approx 5.17"], at=[1, 1, 2])
        self.finish()
