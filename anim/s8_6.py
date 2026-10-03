"""Topic 8.6: Area between curves that cross more than twice. Narration comes from transcripts/8_6.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "8.6"

    def construct(self):
        f = lambda s: s**3 - s**2
        g = lambda s: 2 * s
        with self.beat("Trading places") as b:
            ax, al = plot_axes([-1.6, 2.6, 1], [-5, 7, 2], w=6.4, h=4.6)
            VGroup(ax, al).shift(DOWN * 0.2)
            gf = ax.plot(f, x_range=[-1.5, 2.45], color=FUNC, stroke_width=4)
            gg = ax.plot(g, x_range=[-1.6, 2.6], color=DERIV, stroke_width=4)
            self.play(FadeIn(ax), FadeIn(al), Create(gf), Create(gg), run_time=1.2)
            self.play(FadeIn(region(ax, f, g, -1, 0, opacity=0.4)), FadeIn(region(ax, g, f, 0, 2, color=SECANT, opacity=0.35)), run_time=1)
            b.line(1)
            tag = T("top", 30, FUNC).next_to(ax.c2p(-0.5, f(-0.5)), UP, buff=0.15)
            self.play(FadeIn(tag), run_time=0.5)
            self.play(tag.animate.next_to(ax.c2p(1, g(1)), UP, buff=0.15).set_color(DERIV), run_time=1.2)
            b.line(2)
        self.clear()
        self.title()

        with self.beat("A sign chart for f minus g") as b:
            r = VGroup(M(r"f(x) - g(x) > 0: \ f \text{ on top}", 40, DERIV), M(r"f(x) - g(x) < 0: \ g \text{ on top}", 40, TANGENT)).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.6)
            self.play(FadeIn(r), run_time=1)
            b.line(1)
            ch = sign_chart(["a", "c", "b"], [" ", "+", "-", " "], name="f - g", width=8)
            ch.shift(DOWN * 0.3)
            self.play(FadeIn(ch), run_time=1)
            b.line(2)
            under = VGroup(M(r"\int (f - g)", 32, DERIV).next_to(ch[3][1], DOWN, buff=1.4), M(r"\int (g - f)", 32, TANGENT).next_to(ch[3][2], DOWN, buff=1.4))
            self.play(FadeIn(under), run_time=0.8)
            self.play(FadeIn(formula_box(M(r"\text{area} = \int_a^b |f(x) - g(x)|\,dx", 42, ACCUM), ACCUM).to_edge(DOWN, buff=0.4)), run_time=0.8)
        self.clear()

        with self.beat("Why one integral fails") as b:
            ax, al = plot_axes([-1.6, 2.6, 1], [-5, 7, 2], w=5.4, h=4.2, coords=False)
            VGroup(ax, al).to_edge(LEFT, buff=0.5)
            self.play(FadeIn(ax), FadeIn(ax.plot(f, x_range=[-1.5, 2.45], color=FUNC, stroke_width=4)), FadeIn(ax.plot(g, x_range=[-1.6, 2.6], color=DERIV, stroke_width=4)),
                      FadeIn(region(ax, f, g, -1, 0, color=DERIV, opacity=0.4)), FadeIn(region(ax, g, f, 0, 2, color=TANGENT, opacity=0.35)),
                      FadeIn(M(r"+\tfrac{5}{12}", 30, DERIV).next_to(ax.c2p(-0.5, 0.6), UP, buff=0.4)), FadeIn(M(r"-\tfrac83", 30, TANGENT).move_to(ax.c2p(1.2, 0.8))), run_time=1.2)
            b.line(1)
            wrong = M(r"\int_{-1}^{2} (f - g)\,dx = \tfrac{5}{12} - \tfrac83 = -\tfrac94", 38).to_edge(RIGHT, buff=0.4).shift(UP * 1.2)
            self.play(Write(wrong), run_time=1)
            self.play(Create(Cross(wrong, stroke_color=TANGENT, scale_factor=0.8)), FadeIn(T("not an area: the pieces cancel", 30, TANGENT).next_to(wrong, DOWN, buff=0.3)), run_time=0.8)
            b.line(2)
            right = M(r"\tfrac{5}{12} + \tfrac83 = \tfrac{37}{12}", 42, ACCUM).next_to(wrong, DOWN, buff=1.4)
            self.play(Write(right), Create(SurroundingRectangle(right, color=ACCUM, buff=0.15)), run_time=1)
        self.clear()

        ch = staged_chart([-1, 0, 2], ["-", "+", "-", "+"], name="h", width=6.4)
        ax, _ = plot_axes([-1.6, 2.6, 1], [-5, 7, 2], w=4.4, h=3.2, coords=False)
        fig = VGroup(VGroup(ax, region(ax, f, g, -1, 0, opacity=0.4), region(ax, g, f, 0, 2, color=SECANT, opacity=0.35), ax.plot(f, x_range=[-1.5, 2.45], color=FUNC, stroke_width=4),
                            ax.plot(g, x_range=[-1.6, 2.6], color=DERIV, stroke_width=4)), ch).arrange(DOWN, buff=0.4)
        self.example("Three crossings", r"Find the area of the region between $y = x^3 - x^2$ and $y = 2x$.",
                     [r"x^3 - x^2 = 2x", r"x^3 - x^2 - 2x = 0", r"x\left(x^2 - x - 2\right) = 0", r"x(x - 2)(x + 1) = 0", r"x = -1, \ 0, \ 2", r"h(x) = (x^3 - x^2) - 2x",
                      r"h\left(-\tfrac12\right) = -\tfrac18 - \tfrac14 + 1 = \tfrac58 > 0", r"h(1) = 1 - 1 - 2 = -2 < 0",
                      r"\int_{-1}^{0} h\,dx = \left[\tfrac{x^4}{4} - \tfrac{x^3}{3} - x^2\right]_{-1}^{0} = 0 - \left(\tfrac14 + \tfrac13 - 1\right) = \tfrac{5}{12}",
                      r"\int_0^2 (-h)\,dx = -\left(4 - \tfrac83 - 4\right) = \tfrac83", r"A = \tfrac{5}{12} + \tfrac83 = \tfrac{37}{12}"],
                     at=[1, 1, 2, 2, 2, 3, 3, 4, 5, 6, 7], figure=fig, figure_at=2, cues={6: reveal_sign(ch, 1), 7: reveal_sign(ch, 2)},
                     notes_graph=dict(fns=[("x^3-x^2", -1.5, 2.45), ("2*x", -1.6, 2.6)], xr=(-1.6, 2.6), yr=(-5, 7), ystep=2))

        with self.beat("With a calculator") as b:
            screen = RoundedRectangle(width=7.2, height=2.6, corner_radius=0.2, stroke_color=INK, stroke_width=3, fill_color="#DDE6D5", fill_opacity=1)
            line1 = Text("∫(abs(X³ − X² − 2X), X, −1, 2)", font="DejaVu Sans Mono", font_size=30, color=INK).move_to(screen).shift(UP * 0.4)
            line2 = Text("3.083333333", font="DejaVu Sans Mono", font_size=30, color=INK).move_to(screen).shift(DOWN * 0.5 + RIGHT * 1.8)
            self.play(FadeIn(screen), Write(line1), run_time=1.2)
            self.play(FadeIn(line2), FadeIn(M(r"\tfrac{37}{12} \approx 3.0833", 40, ACCUM).next_to(screen, DOWN, buff=0.5)), run_time=0.8)
            b.line(1)
            self.play(FadeIn(T("limits: the outer crossings", 32, SECANT).next_to(screen, UP, buff=0.4)), run_time=0.8)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(formula_box(M(r"\text{area} = \int_a^b |f(x) - g(x)|\,dx", 46, ACCUM), ACCUM), T("sign chart for $f - g$: split at the crossings", 36),
                          T("add the pieces; never let them cancel", 36, SECANT)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        ax, _ = plot_axes([0, 3.4, 1], [-1.2, 1.2, 1], w=4.6, h=2.8, coords=False)
        fig1 = VGroup(ax, region(ax, np.cos, np.sin, 0, np.pi / 4, opacity=0.35), region(ax, np.sin, np.cos, np.pi / 4, np.pi, color=SECANT, opacity=0.3),
                      ax.plot(np.sin, x_range=[0, np.pi], color=FUNC, stroke_width=4), ax.plot(np.cos, x_range=[0, np.pi], color=DERIV, stroke_width=4))
        self.example("Example 1: Sine and cosine on [0, π]", r"Find the area between $y = \sin x$ and $y = \cos x$ for $0 \le x \le \pi$.",
                     [r"\sin x = \cos x \text{ at } x = \tfrac\pi4", r"TEXT:On $\left(0, \tfrac\pi4\right)$ cosine is on top; on $\left(\tfrac\pi4, \pi\right)$ sine is.",
                      r"\int_0^{\pi/4} (\cos x - \sin x)\,dx = \sqrt2 - 1", r"\int_{\pi/4}^{\pi} (\sin x - \cos x)\,dx = \left[-\cos x - \sin x\right]_{\pi/4}^{\pi} = 1 + \sqrt2",
                      r"A = (\sqrt2 - 1) + (1 + \sqrt2) = 2\sqrt2 \approx 2.83"], at=[1, 1, 2, 2, 3], figure=fig1)
        h2 = lambda s: s**3 - 3 * s
        ax, _ = plot_axes([-2.4, 2.4, 1], [-3, 3, 1], w=4, h=3.6, coords=False)
        fig2 = VGroup(ax, region(ax, h2, lambda s: s, -2, 0, opacity=0.35), region(ax, lambda s: s, h2, 0, 2, opacity=0.35), ax.plot(h2, x_range=[-2.2, 2.2], color=FUNC, stroke_width=4),
                      ax.plot(lambda s: s, x_range=[-2.4, 2.4], color=DERIV, stroke_width=4))
        self.example("Example 2: A symmetric pair", r"Find the area between $y = x^3 - 3x$ and $y = x$.",
                     [r"x^3 - 3x = x", r"x^3 - 4x = 0", r"x(x - 2)(x + 2) = 0: \ x = -2, 0, 2", r"\int_0^2 \big(x - (x^3 - 3x)\big)\,dx = \int_0^2 \left(4x - x^3\right) dx = 8 - 4 = 4",
                      r"TEXT:By symmetry the left piece is also $4$.", r"A = 8"],
                     at=[1, 1, 1, 2, 3, 3], figure=fig2)
        q = lambda s: s**4 - 2 * s**2
        ch3 = staged_chart([r"-\sqrt2", "0", r"\sqrt2"], ["+", "-", "-", "+"], name="y", width=6)
        self.example("Example 3: Touching is not crossing", r"Find the area between $y = x^4 - 2x^2$ and the $x$-axis.",
                     [r"x^4 - 2x^2 = x^2\left(x^2 - 2\right) = 0 \text{ at } x = 0, \pm\sqrt2", r"TEXT:Negative on both sides of $0$: the curve touches the axis there without crossing.",
                      r"A = \int_{-\sqrt2}^{\sqrt2} \left(2x^2 - x^4\right) dx", r"= 2\left[\tfrac23x^3 - \tfrac{x^5}{5}\right]_0^{\sqrt2}", r"= 2\left(\tfrac{4\sqrt2}{3} - \tfrac{4\sqrt2}{5}\right)",
                      r"= \tfrac{16\sqrt2}{15} \approx 1.51"], at=[1, 1, 2, 3, 3, 3], figure=ch3, figure_at=1, cues={1: reveal_sign(ch3, 1, 2)})
        self.finish()
