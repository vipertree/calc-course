"""Topic 1.8: Determining limits using the squeeze theorem. Narration comes from transcripts/1_8.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def wiggle(x):
    return x * x * np.sin(1 / x) if x != 0 else 0


class Lesson(TranscriptScene):
    NUM = "1.8"

    def view(self, R, w=10, h=5.0):
        """x^2 sin(1/x) on [-R, R], sampled finely enough that every wiggle shows, with the hole at 0."""
        ax = Axes(x_range=[-R, R, R / 2], y_range=[-R * R * 1.15, R * R * 1.15, R * R], x_length=w, y_length=h, tips=False,
                  axis_config={"color": DIM, "stroke_width": 2, "include_ticks": False})
        side = np.unique(np.concatenate([np.geomspace(R * 1e-3, R, 6000), np.linspace(R * 1e-3, R, 3000)]))
        parts = VGroup()
        for s in (1, -1):
            pts = [ax.c2p(s * x, wiggle(s * x)) for x in side]
            parts.add(VMobject(color=FUNC, stroke_width=3).set_points_as_corners(pts))
        hole = Circle(radius=0.09, color=FUNC, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(ax.c2p(0, 0))
        tag = M(rf"-{R:g} \le x \le {R:g}", 30, DIM).next_to(ax, DOWN, buff=0.15).align_to(ax, RIGHT)
        return VGroup(ax, parts, hole, tag).shift(DOWN * 0.4)

    def construct(self):
        v = self.view(0.5)
        lab = M(r"y = x^2\sin\frac1x", 48, FUNC).to_corner(UL, buff=0.6)
        with self.beat("A function that won't hold still") as b:
            self.play(FadeIn(v[0]), FadeIn(v[3]), Write(lab), run_time=1)
            self.play(Create(v[1]), run_time=2.4)
            b.line(1)
            note = T(r"undefined at $x = 0$", 34, TANGENT).next_to(v[2], UP, buff=0.5).shift(RIGHT * 1.2)
            arrow = Arrow(note.get_bottom(), v[2].get_center(), color=TANGENT, buff=0.12, stroke_width=4)
            self.play(FadeIn(v[2], scale=2), FadeIn(note), GrowArrow(arrow), run_time=1)
            b.line(2)
            self.play(FadeOut(note), FadeOut(arrow), run_time=0.4)
            for R in (0.12, 0.03):
                self.play(Transform(v, self.view(R)), run_time=2.2)
                self.wait(0.6)
            b.line(3)
            self.play(Transform(v, self.view(0.5)), run_time=1.6)
            self.play(Indicate(v[1], color=SECANT, scale_factor=1.02), run_time=1.2)
        self.clear()
        self.title()

        ax, al = plot_axes([-0.5, 0.5, 0.25], [-0.25, 0.25, 0.125], w=10, h=5.4, coords=False)
        ax.shift(DOWN * 0.3)
        curve = VGroup(ax.plot(wiggle, x_range=[0.003, 0.5], color=FUNC, use_smoothing=False, stroke_width=4),
                       ax.plot(wiggle, x_range=[-0.5, -0.003], color=FUNC, use_smoothing=False, stroke_width=4))
        up = DashedVMobject(ax.plot(lambda x: x * x, x_range=[-0.5, 0.5], color=SECANT, stroke_width=4), num_dashes=50)
        dn = DashedVMobject(ax.plot(lambda x: -x * x, x_range=[-0.5, 0.5], color=TANGENT, stroke_width=4), num_dashes=50)
        with self.beat("Trapped between two parabolas") as b:
            self.add(ax, curve)
            ineq = M(r"-1 \le \sin\frac1x \le 1", 48).to_corner(UL, buff=0.5)
            self.play(Write(ineq), run_time=1)
            ineq2 = M(r"-x^2 \le x^2\sin\frac1x \le x^2", 48).next_to(ineq, DOWN, aligned_edge=LEFT)
            self.play(Write(ineq2), run_time=1.2)
            b.line(1)
            self.play(Create(up), Create(dn), run_time=1.4)
            b.line(2)
            self.play(Flash(ax.c2p(0, 0), color=SECANT, flash_radius=0.4), run_time=1)
        self.clear()

        with self.beat("The theorem") as b:
            thm = callout(r"If $g(x) \le f(x) \le h(x)$ near $c$, and $\displaystyle\lim_{x\to c} g(x) = \lim_{x\to c} h(x) = L$, then $\displaystyle\lim_{x\to c} f(x) = L$.", INK, 38)
            thm.set_max_width(12.5).shift(UP * 1)
            self.play(FadeIn(thm), run_time=1.2)
            wl, wr = Rectangle(width=0.3, height=1.6, color=SECANT, fill_opacity=0.8), Rectangle(width=0.3, height=1.6, color=TANGENT, fill_opacity=0.8)
            ball = Circle(radius=0.3, color=FUNC, fill_opacity=0.9)
            wl.move_to(LEFT * 3 + DOWN * 1.8)
            wr.move_to(RIGHT * 3 + DOWN * 1.8)
            ball.move_to(DOWN * 1.8 + RIGHT * 0.6)
            self.play(FadeIn(wl), FadeIn(wr), FadeIn(ball), run_time=0.6)
            self.play(wl.animate.move_to(LEFT * 0.45 + DOWN * 1.8), wr.animate.move_to(RIGHT * 0.45 + DOWN * 1.8), ball.animate.move_to(DOWN * 1.8), run_time=1.6)
        self.clear()

        # ---------------------------------------------------------------- unit circle
        R = 2.6
        O = LEFT * 3.2 + DOWN * 1.6
        th = 0.75
        P = O + R * np.array([np.cos(th), np.sin(th), 0])
        A = O + R * RIGHT
        Tp = O + R * np.array([1, np.tan(th), 0])
        circ = Arc(radius=R, start_angle=-0.15, angle=PI / 2 + 0.3, arc_center=O, color=DIM)
        axes_ = VGroup(Line(O + LEFT * 0.3, O + RIGHT * (R + 0.6), color=DIM), Line(O + DOWN * 0.3, O + UP * (R + 0.4), color=DIM))
        tri_s = Polygon(O, A, P, color=SECANT, fill_color=SECANT, fill_opacity=0.35, stroke_width=3)
        sector = Sector(radius=R, angle=th, arc_center=O, color=AREA, fill_color=AREA, fill_opacity=0.35, stroke_width=3)
        tri_l = Polygon(O, A, Tp, color=TANGENT, fill_color=TANGENT, fill_opacity=0.25, stroke_width=3)
        ang = Arc(radius=0.5, angle=th, arc_center=O, color=INK)
        alab = M("x", 36).move_to(O + 0.75 * np.array([np.cos(th / 2), np.sin(th / 2), 0]))
        with self.beat("The most important squeeze") as b:
            b.line(1)
            self.play(Create(axes_), Create(circ), run_time=1)
            self.play(Create(Line(O, P, color=INK)), Create(ang), FadeIn(alab), run_time=1)
            for shape in (tri_s, sector, tri_l):
                self.play(FadeIn(shape), run_time=0.9)
            b.line(2)
            areas = VGroup(M(r"\tfrac12\sin x", 44, SECANT), M(r"\tfrac12 x", 44, AREA), M(r"\tfrac12\tan x", 44, TANGENT)).arrange(DOWN, buff=0.5, aligned_edge=LEFT).to_edge(RIGHT, buff=1.2)
            for m in areas:
                self.play(Write(m), run_time=0.8)
        self.clear()

        with self.beat("Rearranging the inequality") as b:
            bd = Board()
            bd.anchor = UP * 3
            bd.write(self, r"\tfrac12\sin x \le \tfrac12 x \le \tfrac12\tan x")
            b.line(1)
            bd.write(self, r"\sin x \le x \le \frac{\sin x}{\cos x}")
            b.line(2)
            bd.write(self, r"1 \le \frac{x}{\sin x} \le \frac{1}{\cos x}")
            b.line(3)
            bd.write(self, r"\cos x \le \frac{\sin x}{x} \le 1", SECANT)
        self.clear()

        ax2, al2 = plot_axes([-2, 2, 1], [0, 1.4, 0.5], w=9, h=4.6)
        ax2.shift(DOWN * 0.4)
        with self.beat("The squeeze closes") as b:
            self.play(FadeIn(ax2), Create(ax2.plot(np.cos, x_range=[-2, 2], color=TANGENT, stroke_width=4)),
                      Create(ax2.plot(lambda x: 1, x_range=[-2, 2], color=SECANT, stroke_width=4)), run_time=1.4)
            b.line(1)
            sinc = VGroup(ax2.plot(lambda x: np.sin(x) / x, x_range=[-2, -0.01], color=FUNC, stroke_width=5),
                          ax2.plot(lambda x: np.sin(x) / x, x_range=[0.01, 2], color=FUNC, stroke_width=5), open_dot(ax2, 0, 1))
            self.play(Create(sinc), run_time=1.4)
            res = M(r"\lim_{x\to0}\frac{\sin x}{x} = 1", 54, FUNC).to_edge(UP, buff=0.5)
            self.play(Write(res), run_time=1.2)
        self.clear()
        self.example("Match the angle", r"Find $\displaystyle\lim_{x\to0}\frac{\sin(5x)}{x}$.",
                     [r"\lim_{x\to0}\frac{\sin 5x}{x} = \lim_{x\to0} 5\cdot\frac{\sin 5x}{5x}", r"u = 5x \to 0: \quad \frac{\sin u}{u} \to 1", r"= 5 \cdot 1 = 5"], at=[1, 2, 3])
        self.example("Rewrite first", r"Find $\displaystyle\lim_{x\to0}\frac{\tan x}{x}$.",
                     [r"\lim_{x\to0}\frac{\tan x}{x} = \lim_{x\to0}\frac{\sin x}{x}\cdot\frac{1}{\cos x}", r"= 1 \cdot \frac{1}{1} = 1"], at=[1, 2])
        self.example("Squeeze with a bounded factor", r"Find $\displaystyle\lim_{x\to0} x\cos\frac{1}{x^2}$.",
                     [r"-1 \le \cos\frac{1}{x^2} \le 1", r"-|x| \le x\cos\frac{1}{x^2} \le |x|", r"\lim_{x\to0}(-|x|) = \lim_{x\to0}|x| = 0", r"\lim_{x\to0} x\cos\frac{1}{x^2} = 0"], at=[1, 2, 3, 4])

        self.example("A second special limit", r"$\displaystyle\lim_{x\to0}\frac{1 - \cos x}{x}$",
                     [r"\lim_{x\to0}\frac{1 - \cos x}{x}\cdot\frac{1 + \cos x}{1 + \cos x} = \lim_{x\to0}\frac{\sin^2 x}{x(1 + \cos x)}",
                      r"= \lim_{x\to0}\frac{\sin x}{x}\cdot\frac{\sin x}{1 + \cos x}", r"= 1\cdot\frac{0}{2} = 0"], at=[0, 1, 2])

        with self.beat("Close") as b:
            two = VGroup(callout(r"$\displaystyle\lim_{x\to0}\frac{\sin x}{x} = 1$", FUNC, 44), callout(r"$\displaystyle\lim_{x\to0}\frac{1 - \cos x}{x} = 0$", FUNC, 44)).arrange(RIGHT, buff=0.8)
            note = T(r"($x$ in radians)", 32, DIM).next_to(two, DOWN, buff=0.4)
            self.play(FadeIn(two), FadeIn(note), run_time=1.2)
        self.clear()

        self.examples_card()
        a1, _ = plot_axes([-1, 1, 0.5], [-1, 1, 0.5], w=5.2, h=4.4, coords=False)
        fig1 = VGroup(a1, a1.plot(lambda x: x * np.cos(3 / x) if x else 0, x_range=[0.005, 1], color=FUNC, use_smoothing=False),
                      a1.plot(lambda x: x * np.cos(3 / x) if x else 0, x_range=[-1, -0.005], color=FUNC, use_smoothing=False),
                      DashedVMobject(a1.plot(abs, x_range=[-1, 1], color=SECANT)), DashedVMobject(a1.plot(lambda x: -abs(x), x_range=[-1, 1], color=TANGENT)))
        self.example("Example 1: A squeeze with cosine", r"Find $\displaystyle\lim_{x\to0} x\cos\frac3x$.",
                     [r"-1 \le \cos\frac3x \le 1", r"-|x| \le x\cos\frac3x \le |x|", r"\lim_{x\to0}\pm|x| = 0,\ \text{so}\ 0"], figure=fig1, at=[1, 2, 3])
        a2, _ = plot_axes([2, 6, 1], [3, 11, 2], w=5.2, h=4.4)
        fig2 = VGroup(a2, a2.plot(lambda x: 4 * x - 9, x_range=[3, 5], color=TANGENT), a2.plot(lambda x: x * x - 4 * x + 7, x_range=[2, 6], color=SECANT),
                      closed_dot(a2, 4, 7))
        self.example("Example 2: Squeezed by a line and a parabola", r"$4x - 9 \le f(x) \le x^2 - 4x + 7$. Find $\displaystyle\lim_{x\to4} f(x)$.",
                     [r"4(4) - 9 = 7", r"16 - 16 + 7 = 7", r"\lim_{x\to4} f(x) = 7"], figure=fig2, at=[1, 2, 3])
        self.example("Example 3: Using the special limit", r"Find $\displaystyle\lim_{x\to0}\frac{\sin 5x}{3x}$.",
                     [r"\lim_{u\to0}\frac{\sin u}{u} = 1 \ \text{(angle and denominator must match)}", r"\lim_{x\to0}\frac53\cdot\frac{\sin 5x}{5x}",
                      r"5x \to 0", r"= \frac53\cdot 1 = \frac53"], at=[1, 2, 3, 4])
        self.finish()
