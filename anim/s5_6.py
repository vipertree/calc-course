"""Topic 5.6: Concavity. Narration comes from transcripts/5_6.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "5.6"

    def construct(self):
        def arc_panel(sign):
            a, _ = plot_axes([-2, 2, 1], [-2.5, 2.5, 1], w=5, h=4, coords=False)
            g = (lambda s: 0.5 * s * s - 1) if sign > 0 else (lambda s: 1 - 0.5 * s * s)
            dg = (lambda s: s) if sign > 0 else (lambda s: -s)
            S = ValueTracker(-1.6)
            tl = always_redraw(lambda: tangent_line(a, g, S.get_value(), dg(S.get_value()), [S.get_value() - 0.6, S.get_value() + 0.6]).set_stroke(width=5))
            rd = always_redraw(lambda: M(rf"\text{{slope}} = {dg(S.get_value()):+.1f}", 34, TANGENT).next_to(a, DOWN, buff=0.3))
            return VGroup(a, a.plot(g, x_range=[-2, 2], color=FUNC, stroke_width=5)), S, tl, rd
        cup, S1, t1, r1 = arc_panel(1)
        cap, S2, t2, r2 = arc_panel(-1)
        VGroup(cup, cap).arrange(RIGHT, buff=1.5).shift(UP * 0.4)
        with self.beat("Bowls and hills") as b:
            self.play(FadeIn(cup), FadeIn(cap), run_time=1)
            self.play(FadeIn(T("bowl", 34, SECANT).next_to(cup, UP, buff=0.2)), FadeIn(T("hill", 34, SECANT).next_to(cap, UP, buff=0.2)), run_time=0.6)
            b.line(1)
            self.add(t1, r1)
            self.play(S1.animate.set_value(1.6), run_time=3, rate_func=linear)
            b.line(2)
            self.add(t2, r2)
            self.play(S2.animate.set_value(1.6), run_time=3, rate_func=linear)
        self.clear()
        self.title()

        with self.beat("Why up and down") as b:
            def eye():
                return VGroup(Ellipse(width=0.7, height=0.34, color=INK, stroke_width=3), Dot(radius=0.08, color=INK))
            hill = FunctionGraph(lambda s: 1 - 0.35 * s * s, x_range=[-2.2, 2.2], color=FUNC, stroke_width=4).move_to(LEFT * 3.4 + UP * 0.3)
            self.play(Create(hill), run_time=1)
            b.line(1)
            e_lo = eye().next_to(hill, DOWN, buff=0.7)
            l_lo = T("from below: caved in, concave", 32, SECANT).next_to(e_lo, DOWN, buff=0.25)
            e_hi = eye().next_to(hill, UP, buff=0.7)
            l_hi = T("from above: bulging out, convex", 32, SECANT).next_to(e_hi, UP, buff=0.25)
            self.play(FadeIn(e_lo), FadeIn(l_lo), run_time=0.8)
            self.wait(1.2)
            self.play(FadeIn(e_hi), FadeIn(l_hi), run_time=0.8)
            b.line(2)
            open_dn = Arrow(hill.get_bottom() + DOWN * 0.9, hill.get_bottom() + UP * 0.5, color=TANGENT, buff=0, stroke_width=5)
            n_dn = T("opens downward: concave down", 34, TANGENT).next_to(open_dn, DOWN, buff=0.3)
            self.play(FadeOut(e_lo), FadeOut(l_lo), FadeOut(e_hi), FadeOut(l_hi), run_time=0.5)
            self.play(GrowArrow(open_dn), FadeIn(n_dn), run_time=0.8)
            b.line(3)
            bowl = FunctionGraph(lambda s: 0.35 * s * s - 1, x_range=[-2.2, 2.2], color=FUNC, stroke_width=4).move_to(RIGHT * 3.4 + DOWN * 0.3)
            open_up = Arrow(bowl.get_top() + UP * 0.9, bowl.get_top() + DOWN * 0.5, color=DERIV, buff=0, stroke_width=5)
            n_up = T("opens upward: concave up", 34, DERIV).next_to(open_up, UP, buff=0.3)
            self.play(Create(bowl), run_time=0.8)
            self.play(GrowArrow(open_up), FadeIn(n_up), run_time=0.8)
        self.clear()

        with self.beat("Concavity and the second derivative") as b:
            up = VGroup(T("concave up", 44, DERIV), M(r"f' \text{ increasing},\ \ f'' > 0", 42), T("above its tangent lines", 34, DIM)).arrange(DOWN, buff=0.3)
            dn = VGroup(T("concave down", 44, TANGENT), M(r"f' \text{ decreasing},\ \ f'' < 0", 42), T("below its tangent lines", 34, DIM)).arrange(DOWN, buff=0.3)
            VGroup(up, dn).arrange(RIGHT, buff=1.6)
            self.play(FadeIn(up[:2]), run_time=0.8)
            b.line(1)
            self.play(FadeIn(dn[:2]), run_time=0.8)
            b.line(2)
            self.play(FadeIn(up[2]), FadeIn(dn[2]), run_time=0.8)
        self.clear()

        ax, al = plot_axes([-1, 3, 1], [-4, 2, 1], w=7, h=4.4, coords=False)
        VGroup(ax, al).to_edge(UP, buff=0.4).shift(LEFT * 2)
        f = lambda s: s**3 - 3 * s**2 + 1
        with self.beat("Points of inflection") as b:
            cap = ax.plot(f, x_range=[-0.9, 1], color=TANGENT, stroke_width=6)
            cupc = ax.plot(f, x_range=[1, 3], color=DERIV, stroke_width=6)
            self.play(FadeIn(ax), FadeIn(al), Create(cap), run_time=1)
            self.play(Create(cupc), run_time=0.8)
            ip = VGroup(Dot(ax.c2p(1, -1), color=INK, radius=0.1), T("point of inflection", 30, SECANT).next_to(ax.c2p(1, -1), RIGHT, buff=0.3).shift(UP * 0.2))
            self.play(FadeIn(ip), run_time=0.6)
            b.line(1)
            ch = sign_chart([1], ["-", "+"], name="f''", width=6).next_to(VGroup(ax, al), DOWN, buff=0.6)
            lab = M(r"f''(x) = 6x - 6", 38).next_to(ch, RIGHT, buff=0.6)
            self.play(FadeIn(ch), FadeIn(lab), run_time=1)
            b.line(2)
            x4 = VGroup(M(r"y = x^4:\ f''(0) = 0", 34), T("but a bowl on both sides", 30, DIM)).arrange(DOWN, buff=0.2).to_edge(RIGHT, buff=0.6).shift(UP * 1.6)
            self.play(FadeIn(x4), run_time=0.8)
        self.clear()
        k0 = staged_chart([-1], ["-", "+"], words=["down", "up"], name="f''", width=7)
        self.example("Concavity of a cubic", r"Where is $f(x) = x^3 + 3x^2$ concave up? Find any points of inflection.",
                     [r"f'(x) = 3x^2 + 6x", r"f''(x) = 6x + 6", r"6x + 6 = 0, \ \ 6x = -6, \ \ x = -1", r"f''(-2) = -12 + 6 = -6 < 0", r"f''(0) = 6 > 0",
                      r"\text{concave down on } (-\infty, -1), \text{ up on } (-1, \infty)", r"f(-1) = -1 + 3 = 2: \ \text{inflection point } (-1, 2)"],
                     at=[1, 2, 3, 4, 5, 6, 7], figure=k0, figure_at=4,
                     cues={3: reveal_sign(k0, 0), 4: lambda sc: (reveal_sign(k0, 1)(sc), reveal_words(k0)(sc)), 6: mark_point(k0, 0, "inflection")})

        with self.beat("Close") as b:
            a1, _ = plot_axes([-1, 1, 1], [-1, 1, 1], w=2.6, h=2.2, coords=False)
            a2, _ = plot_axes([-1, 1, 1], [-1, 1, 1], w=2.6, h=2.2, coords=False)
            a3, _ = plot_axes([-1, 1, 1], [-1, 1, 1], w=2.6, h=2.2, coords=False)
            p1 = VGroup(a1.plot(lambda s: s * s - 0.5, x_range=[-1, 1], color=DERIV, stroke_width=5), M("f'' > 0", 34, DERIV))
            p2 = VGroup(a2.plot(lambda s: 0.5 - s * s, x_range=[-1, 1], color=TANGENT, stroke_width=5), M("f'' < 0", 34, TANGENT))
            p3 = VGroup(a3.plot(lambda s: s**3, x_range=[-1, 1], color=FUNC, stroke_width=5), Dot(a3.c2p(0, 0), color=INK), T(r"$f''$ changes sign", 30, SECANT))
            for p in (p1, p2):
                p[1].next_to(p[0], DOWN, buff=0.4)
            p3[2].next_to(p3[0], DOWN, buff=0.4)
            row = VGroup(p1, p3, p2).arrange(RIGHT, buff=1.4)
            self.play(LaggedStart(FadeIn(p1), FadeIn(p3), FadeIn(p2), lag_ratio=0.4), run_time=1.6)
        self.clear()

        self.examples_card()
        k1 = staged_chart([2], ["-", "+"], words=["down", "up"], name="f''", width=7)
        self.example("Example 1: A cubic", r"Where is $f(x) = x^3 - 6x^2 + 5$ concave up? Concave down? Find any points of inflection.",
                     [r"f'(x) = 3x^2 - 12x", r"f''(x) = 6x - 12", r"6x - 12 = 0, \ \text{so}\ x = 2", r"f''(0) = -12 < 0", r"f''(3) = 18 - 12 = 6 > 0",
                      r"\text{concave down on } (-\infty, 2), \text{ up on } (2, \infty)", r"f(2) = 8 - 24 + 5 = -11: \ \text{inflection point } (2, -11)"],
                     at=[1, 2, 3, 4, 5, 6, 7], figure=k1, figure_at=4,
                     cues={3: reveal_sign(k1, 0), 4: lambda sc: (reveal_sign(k1, 1)(sc), reveal_words(k1)(sc)), 6: mark_point(k1, 0, "inflection")})
        k2 = staged_chart([0, 2], ["+", "-", "+"], words=["up", "down", "up"], name="f''", width=7)
        self.example("Example 2: Two candidates", r"Find the points of inflection of $f(x) = x^4 - 4x^3$.",
                     [r"f'(x) = 4x^3 - 12x^2", r"f''(x) = 12x^2 - 24x", r"= 12x(x - 2), \ \text{zero at } x = 0,\ 2",
                      r"f''(-1) = 12 + 24 = 36 > 0", r"f''(1) = 12 - 24 = -12 < 0", r"f''(3) = 108 - 72 = 36 > 0",
                      r"f(0) = 0, \ \ f(2) = 16 - 32 = -16", r"\text{inflection points: } (0, 0) \text{ and } (2, -16)"],
                     at=[1, 2, 3, 4, 5, 6, 7, 7], figure=k2, figure_at=4,
                     cues={3: reveal_sign(k2, 0), 4: reveal_sign(k2, 1), 5: lambda sc: (reveal_sign(k2, 2)(sc), reveal_words(k2)(sc)),
                           6: lambda sc: (mark_point(k2, 0, "inflection")(sc), mark_point(k2, 1, "inflection")(sc))})
        k3 = staged_chart([-2], ["-", "+"], words=["down", "up"], name="f''", width=7)
        self.example("Example 3: An exponential", r"Where is $f(x) = xe^{x}$ concave down?",
                     [r"f'(x) = e^x + xe^x = (x + 1)e^x", r"f''(x) = e^x + (x + 1)e^x = (x + 2)e^x", r"TEXT:$e^x > 0$, so $f''$ has the sign of $x + 2$: zero at $x = -2$.",
                      r"f''(-3) = (-1)e^{-3} < 0", r"f''(0) = 2 > 0", r"\text{concave down on } (-\infty, -2)"],
                     at=[1, 2, 3, 4, 5, 6], figure=k3, figure_at=3,
                     cues={3: reveal_sign(k3, 0), 4: lambda sc: (reveal_sign(k3, 1)(sc), reveal_words(k3)(sc))})
        self.finish()
