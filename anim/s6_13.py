"""Topic 6.13 (BC): Improper integrals. Narration comes from transcripts/6_13.md.

Adder's 6.13 notes (2026-10-14): no "BC only" in the video. Remind students infinity is not a number: the integral to
infinity means up to b, then b -> infinity; a finite limit converges, otherwise it diverges. In the first example show
-1/b - (-1), not -1/b + 1. The integral of 1/x^2 from -1 to 1 gets a graph showing what's happening.
"""
import numpy as np
from manim import *

from kit import *
from style import *


DEF = r"\int_a^\infty f(x)\,dx = \lim_{b\to\infty} \int_a^b f(x)\,dx"


def hidden_asymptote():
    """y = 1/x^2 on [-1, 1]: both branches run up the y-axis. The region under it is clipped at the top of the window,
    so its edge follows the curve exactly; the asymptote at x = 0 and two arrows going up come in with a cue."""
    ax, al = plot_axes([-1.25, 1.25, 0.5], [0, 12, 2], w=5.6, h=5.4, coords=False, ylabel="")
    # x labels only: the y-axis is the asymptote, and numbers beside it would sit inside the shading
    ax.add_coordinates({-1: "-1", 1: "1"})
    f = lambda s: 1 / s**2
    xc = 1 / np.sqrt(12)                                      # where the curve leaves the window
    curves = VGroup(ax.plot(f, x_range=[-1.25, -xc], color=FUNC, stroke_width=5), ax.plot(f, x_range=[xc, 1.25], color=FUNC, stroke_width=5))
    lft = [ax.c2p(t, f(t)) for t in np.linspace(-1, -xc, 40)]
    rgt = [ax.c2p(t, f(t)) for t in np.linspace(xc, 1, 40)]
    region = Polygon(ax.c2p(-1, 0), *lft, ax.c2p(-xc, 12), ax.c2p(xc, 12), *rgt, ax.c2p(1, 0),
                     stroke_width=0, fill_color=AREA, fill_opacity=0.45)
    asym = DashedLine(ax.c2p(0, 0), ax.c2p(0, 12), color=TANGENT, stroke_width=4, dash_length=0.12)
    ups = VGroup(*[Arrow(ax.c2p(sx * 0.62, 7.5), ax.c2p(sx * 0.62, 11.6), buff=0, color=TANGENT, stroke_width=5, max_tip_length_to_length_ratio=0.25) for sx in (-1, 1)])
    inf = VGroup(*[M(r"\infty", 34, TANGENT).next_to(u, sx * RIGHT, buff=0.1).align_to(u, UP) for u, sx in zip(ups, (-1, 1))])
    fig = VGroup(ax, al, curves)
    return fig, region, VGroup(asym, ups, inf)


class Lesson(TranscriptScene):
    NUM = "6.13"

    def construct(self):
        a1, l1 = plot_axes([0, 10, 1], [0, 1.2, 0.5], w=8.6, h=2.6, coords=False, ylabel="1/x^2")
        a2, l2 = plot_axes([0, 10, 1], [0, 1.2, 0.5], w=8.6, h=2.6, coords=False, ylabel="1/x")
        VGroup(VGroup(a1, l1), VGroup(a2, l2)).arrange(DOWN, buff=0.6).to_edge(LEFT, buff=0.6)
        B = ValueTracker(1.05)
        with self.beat("An endless region") as b:
            self.play(FadeIn(a1), FadeIn(l1), FadeIn(a2), FadeIn(l2),
                      Create(a1.plot(lambda s: 1 / s**2, x_range=[0.92, 10], color=FUNC, stroke_width=4)), Create(a2.plot(lambda s: 1 / s, x_range=[0.85, 10], color=FUNC, stroke_width=4)), run_time=1.2)
            sh1 = always_redraw(lambda: a1.get_area(a1.plot(lambda s: 1 / s**2, x_range=[1, B.get_value()]), x_range=[1, B.get_value()], color=DERIV, opacity=0.45))
            sh2 = always_redraw(lambda: a2.get_area(a2.plot(lambda s: 1 / s, x_range=[1, B.get_value()]), x_range=[1, B.get_value()], color=TANGENT, opacity=0.45))
            r1 = always_redraw(lambda: M(rf"1 - \tfrac1b = {1 - 1 / B.get_value():.3f}", 32, DERIV).next_to(a1, RIGHT, buff=0.3))
            r2 = always_redraw(lambda: M(rf"\ln b = {np.log(B.get_value()):.3f}", 32, TANGENT).next_to(a2, RIGHT, buff=0.3))
            self.add(sh1, sh2, r1, r2)
            b.line(1)
            self.play(B.animate.set_value(9.8), run_time=4, rate_func=rate_functions.ease_in_sine)
            b.line(2)
            self.play(FadeIn(T(r"$\to 1$", 30, DERIV).next_to(r1, DOWN, buff=0.15)), FadeIn(T(r"$\to \infty$", 30, TANGENT).next_to(r2, DOWN, buff=0.15)), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("Infinite limits of integration") as b:
            d = M(DEF, 50, ACCUM).to_edge(UP, buff=0.5)
            self.play(Write(d), run_time=1.2)
            b.line(1)
            note = VGroup(T(r"$\infty$ is not a number.", 36, TANGENT), T(r"Integrate up to $b$, then let $b \to \infty$.", 36)).arrange(DOWN, buff=0.25).next_to(d, DOWN, buff=0.5)
            self.play(FadeIn(note[0]), run_time=0.6)
            nl = NumberLine(x_range=[0, 10, 1], length=10, color=DIM, include_ticks=False).next_to(note, DOWN, buff=0.9)
            tip = Arrow(nl.n2p(9.6), nl.n2p(10.4), buff=0, color=DIM, stroke_width=3, max_tip_length_to_length_ratio=0.5)
            adot = VGroup(Dot(nl.n2p(0.5), color=INK, radius=0.08), M("a", 32).next_to(nl.n2p(0.5), DOWN, buff=0.2))
            B = ValueTracker(2.5)
            span = always_redraw(lambda: Line(nl.n2p(0.5), nl.n2p(B.get_value()), color=AREA, stroke_width=10))
            bdot = always_redraw(lambda: VGroup(Dot(nl.n2p(B.get_value()), color=SECANT, radius=0.1), M("b", 32, SECANT).next_to(nl.n2p(B.get_value()), DOWN, buff=0.2)))
            self.play(FadeIn(note[1]), Create(nl), FadeIn(tip), FadeIn(adot), FadeIn(span), FadeIn(bdot), run_time=0.8)
            self.play(B.animate.set_value(9.2), run_time=2.5, rate_func=rate_functions.ease_in_sine)
            bto = M(r"b \to \infty", 32, SECANT).next_to(tip, UP, buff=0.2)
            self.play(FadeIn(bto), run_time=0.5)
            b.line(2)
            tags = VGroup(T("a finite limit: converges", 32, DERIV), T("no finite limit: diverges", 32, TANGENT)).arrange(RIGHT, buff=1.2).next_to(nl, DOWN, buff=1.0)
            self.play(FadeIn(tags[0]), run_time=0.6)
            b.line(3)
            self.play(FadeIn(tags[1]), run_time=0.6)
        self.clear()

        self.example("Up to b, then the limit", r"Evaluate $\displaystyle\int_1^\infty \frac{1}{x^2}\,dx$.",
                     [r"= \lim_{b\to\infty} \int_1^b x^{-2}\,dx", r"= \lim_{b\to\infty} \left[-\frac1x\right]_1^b",
                      r"= \lim_{b\to\infty} \left(-\frac1b - \left(-\frac11\right)\right)", r"= \lim_{b\to\infty} \left(-\frac1b - (-1)\right)",
                      r"= 0 - (-1) = 1", r"TEXT:A finite limit: the integral converges to $1$."],
                     at=[1, 2, 3, 4, 5, 6], follow=True, ref=DEF, size=44)
        self.example("One over x", r"Evaluate $\displaystyle\int_1^\infty \frac{1}{x}\,dx$, or show that it diverges.",
                     [r"= \lim_{b\to\infty} \int_1^b \frac1x\,dx", r"= \lim_{b\to\infty} \left[\ln x\right]_1^b",
                      r"= \lim_{b\to\infty} \left(\ln b - \ln 1\right) = \lim_{b\to\infty} \ln b", r"= \infty: \ \text{diverges}",
                      r"TEXT:Write the limit on every line."],
                     at=[1, 2, 3, 4, 5], ref=DEF, size=44)

        ax, al = plot_axes([0, 1.2, 0.5], [0, 6, 1], w=4.6, h=5, coords=False)
        VGroup(ax, al).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        A = ValueTracker(0.6)
        with self.beat("A vertical asymptote") as b:
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(lambda s: 1 / np.sqrt(s), x_range=[0.028, 1.15], color=FUNC, stroke_width=4)), run_time=1)
            self.add(always_redraw(lambda: ax.get_area(ax.plot(lambda s: 1 / np.sqrt(s), x_range=[A.get_value(), 1]), x_range=[A.get_value(), 1], color=AREA, opacity=0.45)))
            b.line(1)
            rows = VGroup(M(r"\int_0^1 x^{-1/2}\,dx = \lim_{a\to0^+} \int_a^1 x^{-1/2}\,dx", 38), M(r"= \lim_{a\to0^+} \left[2\sqrt x\right]_a^1", 38),
                          M(r"= \lim_{a\to0^+} \left(2 - 2\sqrt a\right) = 2", 38, AREA)).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.5).shift(UP * 1)
            self.play(Write(rows[0]), A.animate.set_value(0.2), run_time=1.4)
            b.line(2)
            self.play(Write(rows[1]), run_time=1)
            b.line(3)
            self.play(Write(rows[2]), A.animate.set_value(0.03), run_time=1.6)
        self.clear()

        with self.beat("p-integrals") as b:
            rule = formula_box(M(r"\int_1^\infty \frac{1}{x^p}\,dx \ \text{ converges if } p > 1, \ \text{diverges if } p \le 1", 42, ACCUM), ACCUM).to_edge(UP, buff=0.6)
            self.play(FadeIn(rule), run_time=0.8)
            b.line(1)
            minis = VGroup()
            for p, col, word in ((2, DERIV, "converges (to 1)"), (1, TANGENT, "diverges"), (0.5, TANGENT, "diverges")):
                a, _ = plot_axes([0, 6, 1], [0, 1.4, 1], w=3.4, h=2, coords=False)
                g = VGroup(a, a.plot(lambda s, p=p: 1 / s**p, x_range=[0.8, 6], color=col, stroke_width=4))
                minis.add(VGroup(g, M(rf"p = {p}", 32, col), T(word, 28, col)).arrange(DOWN, buff=0.2))
            minis.arrange(RIGHT, buff=0.7).next_to(rule, DOWN, buff=0.6)
            self.play(LaggedStart(*[FadeIn(m) for m in minis], lag_ratio=0.4), run_time=1.6)
        self.clear()

        hfig, hreg, hasym = hidden_asymptote()
        self.example("A hidden asymptote", r"Evaluate $\displaystyle\int_{-1}^{1} \frac{1}{x^2}\,dx$.",
                     [r"\text{tempting: } \left[-\tfrac1x\right]_{-1}^{1} = -1 - 1 = -2", r"\text{but } \tfrac{1}{x^2} > 0",
                      r"TEXT:$\frac{1}{x^2} \to \infty$ at $x = 0$, inside $[-1, 1]$: split there.",
                      r"\int_0^1 x^{-2}\,dx = \lim_{a\to0^+} \left[-\frac1x\right]_a^1", r"= \lim_{a\to0^+} \left(-\frac11 - \left(-\frac1a\right)\right)",
                      r"= \lim_{a\to0^+} \left(-1 + \frac1a\right) = \infty", r"TEXT:That piece diverges, so the whole integral diverges."],
                     at=[1, 1, 2, 3, 4, 5, 6], figure=hfig, figure_at=1, size=40,
                     notes_graph=dict(fns=[("1/x^2", -1.25, -0.29), ("1/x^2", 0.29, 1.25)], xr=(-1.25, 1.25), yr=(0, 12), vlines=(0,), xstep=0.5, ystep=2),
                     cues={1: lambda sc: (sc.play(FadeIn(hreg), run_time=0.8), sc.bring_to_front(hfig[2])),
                           2: lambda sc: sc.play(Create(hasym[0]), GrowArrow(hasym[1][0]), GrowArrow(hasym[1][1]), FadeIn(hasym[2]), run_time=1)})

        with self.beat("Close") as b:
            card = VGroup(M(r"\int_a^\infty f\,dx = \lim_{b\to\infty} \int_a^b f\,dx", 44, ACCUM), T("Asymptote at $c$: replace $c$ by a limit.", 36),
                          T("A number: converges. Infinite or no limit: diverges.", 36), T("Write the limit on every line. Check inside the interval.", 34, SECANT)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: An exponential tail", r"Evaluate $\displaystyle\int_0^\infty e^{-2x}\,dx$.",
                     [r"= \lim_{b\to\infty} \int_0^b e^{-2x}\,dx", r"= \lim_{b\to\infty} \left[-\tfrac12 e^{-2x}\right]_0^b",
                      r"= \lim_{b\to\infty} \left(-\tfrac12 e^{-2b} - \left(-\tfrac12 e^{0}\right)\right) = \lim_{b\to\infty} \left(-\tfrac12 e^{-2b} - \left(-\tfrac12\right)\right)",
                      r"= 0 - \left(-\tfrac12\right) = \tfrac12: \ \text{converges}"],
                     at=[1, 2, 2, 4], ref=DEF)
        self.example("Example 2: A slow tail", r"Evaluate $\displaystyle\int_1^\infty \frac{x}{x^2 + 1}\,dx$.",
                     [r"= \lim_{b\to\infty} \int_1^b \frac{x}{x^2 + 1}\,dx = \lim_{b\to\infty} \left[\tfrac12\ln\left(x^2 + 1\right)\right]_1^b", r"= \lim_{b\to\infty} \left(\tfrac12\ln\left(b^2 + 1\right) - \tfrac12\ln 2\right)",
                      r"= \infty: \ \text{diverges}"], at=[1, 2, 4], ref=DEF)
        self.finish()
