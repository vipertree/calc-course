"""Topic 9.9 (BC): Area between two polar curves. Narration comes from transcripts/9_9.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "9.9"

    def construct(self):
        circ = lambda s: 3 * np.cos(s)
        card = lambda s: 1 + np.cos(s)
        with self.beat("Between two polar curves") as b:
            ax, _ = plot_axes([-0.6, 3.4, 1], [-2, 2, 1], w=5.4, h=5.4, coords=False)
            ax.shift(LEFT * 1.6)
            self.play(FadeIn(ax), Create(polar_curve(ax, circ, -PI / 2, PI / 2, color=FUNC)), Create(polar_curve(ax, card, 0, TAU, color=DERIV)), run_time=1.2)
            self.play(FadeIn(polar_region(ax, circ, -PI / 3, PI / 3, inner=card)), run_time=1)
            b.line(1)
            t0, dt = 0.5, 0.12
            outer = Polygon(*[ax.c2p(circ(v) * np.cos(v), circ(v) * np.sin(v)) for v in (t0, t0 + dt)] + [ax.c2p(card(v) * np.cos(v), card(v) * np.sin(v)) for v in (t0 + dt, t0)],
                            stroke_color=SECANT, stroke_width=2, fill_color=SECANT, fill_opacity=0.8)
            inner = polar_wedge(ax, card, t0, dt, color=DIM, opacity=0.4)
            self.play(FadeIn(outer), FadeIn(inner), run_time=1)
            b.line(2)
            self.play(FadeIn(M(r"\text{outer} - \text{inner}", 40).to_edge(RIGHT, buff=0.8)), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("Outer squared minus inner squared") as b:
            big = Sector(radius=2.4, angle=0.5, start_angle=0.3, fill_color=SECANT, fill_opacity=0.6, stroke_width=0)
            small = Sector(radius=1.3, angle=0.5, start_angle=0.3, fill_color=BG, fill_opacity=1, stroke_color=DIM, stroke_width=2)
            grp = VGroup(big, small, M("R", 30, SECANT).move_to(2.6 * np.array([np.cos(0.2), np.sin(0.2), 0])), M("r", 30, DIM).move_to(1.1 * np.array([np.cos(0.2), np.sin(0.2), 0]))).to_edge(LEFT, buff=1.2)
            self.play(FadeIn(grp), run_time=1)
            rows = VGroup(M(r"\tfrac12 R^2\,\Delta\theta - \tfrac12 r^2\,\Delta\theta = \tfrac12\left(R^2 - r^2\right)\Delta\theta", 36), formula_box(M(r"A = \tfrac12\int_\alpha^\beta \left(R^2 - r^2\right) d\theta", 44, ACCUM), ACCUM),
                          M(r"(R - r)^2 \ne R^2 - r^2", 36, TANGENT), T("limits: set the two $r$'s equal", 32)).arrange(DOWN, buff=0.45).to_edge(RIGHT, buff=0.5)
            self.play(Write(rows[0]), run_time=1)
            b.line(1)
            self.play(FadeIn(rows[1]), run_time=0.8)
            b.line(2)
            self.play(FadeIn(rows[2]), run_time=0.6)
            b.line(3)
            self.play(FadeIn(rows[3]), run_time=0.6)
        self.clear()

        ax, _ = plot_axes([-0.6, 3.4, 1], [-2, 2, 1], w=3.6, h=3.6)
        fig = VGroup(ax, polar_region(ax, circ, -PI / 3, PI / 3, inner=card), polar_curve(ax, circ, -PI / 2, PI / 2, color=FUNC), polar_curve(ax, card, 0, TAU, color=DERIV))
        self.example("Inside the circle, outside the cardioid", r"Find the area inside $r = 3\cos\theta$ and outside $r = 1 + \cos\theta$.",
                     [r"3\cos\theta = 1 + \cos\theta", r"\cos\theta = \tfrac12, \ \ \theta = \pm\tfrac\pi3", r"R = 3\cos\theta, \ \ r = 1 + \cos\theta", r"R^2 - r^2 = 9\cos^2\theta - \left(1 + 2\cos\theta + \cos^2\theta\right) = 8\cos^2\theta - 2\cos\theta - 1",
                      r"8\cos^2\theta = 4 + 4\cos 2\theta: \ \ R^2 - r^2 = 3 + 4\cos 2\theta - 2\cos\theta", r"A = \tfrac12\int_{-\pi/3}^{\pi/3} \left(3 + 4\cos 2\theta - 2\cos\theta\right) d\theta",
                      r"= \tfrac12\left[3\theta + 2\sin 2\theta - 2\sin\theta\right]_{-\pi/3}^{\pi/3}", r"= \tfrac12(2\pi) = \pi"], at=[1, 1, 2, 3, 4, 5, 5, 6], figure=fig, follow=True)

        with self.beat("Close") as b:
            cardv = VGroup(formula_box(M(r"A = \tfrac12\int_\alpha^\beta \left(R^2 - r^2\right) d\theta", 46, ACCUM), ACCUM), T("$R$: outer curve, $r$: inner curve (from the origin)", 34), T("limits: set the $r$'s equal", 34),
                           T("square each radius separately", 34, TANGENT)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in cardv], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        ax, _ = plot_axes([-1.6, 1.6, 1], [-0.4, 2.4, 1], w=3.4, h=3, coords=False)
        fig1 = VGroup(ax, polar_region(ax, lambda s: 2 * np.sin(s), PI / 6, 5 * PI / 6, inner=lambda s: 1), polar_curve(ax, lambda s: 2 * np.sin(s), 0, PI, color=FUNC), polar_curve(ax, lambda s: 1, 0, TAU, color=DERIV))
        self.example("Example 1: Inside a circle, outside another", r"Find the area inside $r = 2\sin\theta$ and outside $r = 1$.",
                     [r"2\sin\theta = 1 \text{ at } \theta = \tfrac\pi6, \ \tfrac{5\pi}{6}", r"A = \tfrac12\int_{\pi/6}^{5\pi/6} \left(4\sin^2\theta - 1\right) d\theta", r"4\sin^2\theta = 2 - 2\cos 2\theta: \ \text{integrand } 1 - 2\cos 2\theta",
                      r"= \tfrac12\left[\theta - \sin 2\theta\right]_{\pi/6}^{5\pi/6}", r"= \tfrac12\left(\tfrac{2\pi}{3} + \sqrt3\right) = \tfrac\pi3 + \tfrac{\sqrt3}{2} \approx 1.91"], at=[1, 1, 2, 3, 3], figure=fig1)
        ax, _ = plot_axes([-1.4, 2.4, 1], [-1.4, 1.4, 1], w=3.6, h=2.8, coords=False)
        lens_out = lambda s: min(1.0, 2 * np.cos(s)) if abs(s) < PI / 2 else 0.0
        fig2 = VGroup(ax, polar_region(ax, lens_out, -PI / 2, PI / 2), polar_curve(ax, lambda s: 1, 0, TAU, color=DERIV), polar_curve(ax, lambda s: 2 * np.cos(s), -PI / 2, PI / 2, color=FUNC))
        self.example("Example 2: The region inside both", r"Find the area of the region inside both $r = 1$ and $r = 2\cos\theta$.",
                     [r"2\cos\theta = 1: \ \theta = \pm\tfrac\pi3", r"TEXT:For $|\theta| \le \frac\pi3$ the boundary is $r = 1$; for $\frac\pi3 \le |\theta| \le \frac\pi2$ it is $r = 2\cos\theta$.",
                      r"A = 2\left[\tfrac12\int_0^{\pi/3} 1\,d\theta + \tfrac12\int_{\pi/3}^{\pi/2} 4\cos^2\theta\,d\theta\right]", r"= \tfrac\pi3 + \left[2\theta + \sin 2\theta\right]_{\pi/3}^{\pi/2}", r"= \tfrac\pi3 + \tfrac\pi3 - \tfrac{\sqrt3}{2} = \tfrac{2\pi}{3} - \tfrac{\sqrt3}{2} \approx 1.23"],
                     at=[1, 1, 2, 3, 3], figure=fig2)
        self.example("Example 3: A calculator problem", r"Find the area inside $r = 2 + 2\sin\theta$ and outside $r = 3$.",
                     [r"2 + 2\sin\theta = 3 \text{ at } \theta = \tfrac\pi6, \ \tfrac{5\pi}{6}", r"A = \tfrac12\int_{\pi/6}^{5\pi/6} \left((2 + 2\sin\theta)^2 - 9\right) d\theta", r"\approx 4.653 \ \ (\text{calculator})"], at=[1, 2, 2])
        self.finish()
