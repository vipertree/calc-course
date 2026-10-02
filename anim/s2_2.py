"""Topic 2.2: The derivative as a function, and derivative notation. Narration comes from transcripts/2_2.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def f(x):
    return x * x


class Lesson(TranscriptScene):
    NUM = "2.2"

    def stacked(self):
        top, tl = plot_axes([-2, 2, 1], [0, 4, 1], w=5.6, h=2.6, ylabel="f")
        bot, bl = plot_axes([-2, 2, 1], [-4, 4, 2], w=5.6, h=2.6, ylabel="f'")
        g = VGroup(VGroup(top, tl), VGroup(bot, bl)).arrange(DOWN, buff=0.35).to_edge(LEFT, buff=0.8)
        return top, tl, bot, bl, g

    def construct(self):
        ax, al = plot_axes([-2.5, 2.5, 1], [0, 6, 1], w=7, h=5)
        VGroup(ax, al).shift(DOWN * 0.3 + LEFT * 1.5)
        x = ValueTracker(1)
        tan = always_redraw(lambda: tangent_line(ax, f, x.get_value(), 2 * x.get_value(), [x.get_value() - 0.9, x.get_value() + 0.9]))
        dot = always_redraw(lambda: closed_dot(ax, x.get_value(), f(x.get_value()), INK))
        read = always_redraw(lambda: M(rf"\text{{slope}} = {2 * x.get_value():.1f}", 40, TANGENT).to_edge(RIGHT, buff=0.7).shift(UP * 2))
        with self.beat("One slope, then every slope") as b:
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(f, x_range=[-2.4, 2.4], color=FUNC, stroke_width=5)), run_time=1.2)
            self.play(FadeIn(dot), Create(tan), FadeIn(read), run_time=1)
            b.line(2)
            self.play(x.animate.set_value(-1.8), run_time=2.5)
            self.play(x.animate.set_value(1.8), run_time=3)
            b.line(3)
            self.play(x.animate.set_value(0.5), run_time=1.2)
        self.clear()
        self.title()

        top, tl, bot, bl, g = self.stacked()
        x = ValueTracker(-1.6)
        tan = always_redraw(lambda: tangent_line(top, f, x.get_value(), 2 * x.get_value(), [max(-2, x.get_value() - 0.6), min(2, x.get_value() + 0.6)]))
        dot = always_redraw(lambda: closed_dot(top, x.get_value(), f(x.get_value()), INK))
        probe = always_redraw(lambda: DashedLine(top.c2p(x.get_value(), f(x.get_value())), bot.c2p(x.get_value(), 2 * x.get_value()), color=DIM, stroke_width=2))
        trace = TracedPath(lambda: bot.c2p(x.get_value(), 2 * x.get_value()), stroke_color=DERIV, stroke_width=5)
        with self.beat("Recording the slopes") as b:
            self.play(FadeIn(g), Create(top.plot(f, x_range=[-2, 2], color=FUNC, stroke_width=4)), run_time=1.2)
            self.play(FadeIn(dot), Create(tan), FadeIn(probe), run_time=0.8)
            self.add(trace)
            marks = VGroup()
            for i, xv in ((1, -1), (2, 0), (3, 1)):
                b.line(i)
                self.play(x.animate.set_value(xv), run_time=1.2)
                d = closed_dot(bot, xv, 2 * xv, DERIV)
                marks.add(d)
                self.play(FadeIn(d, scale=2), FadeIn(M(rf"({xv}, {2 * xv})", 30, DERIV).next_to(d, UL if xv < 0 else DR, buff=0.12)), run_time=0.6)
            b.line(4)
            self.play(x.animate.set_value(1.9), run_time=1.2)
            lab = M("y = 2x", 40, DERIV).to_edge(RIGHT, buff=1.2).shift(DOWN * 1.6)
            self.play(Write(lab), run_time=0.8)
            b.line(5)
            name = M(r"f'(x) = 2x", 50, DERIV).move_to(lab)
            self.play(ReplacementTransform(lab, name), run_time=0.8)
        self.clear()

        with self.beat("The definition") as b:
            d1 = M(r"f'(", "a", r") = \lim_{h\to0}\frac{f(", "a", r" + h) - f(", "a", r")}{h}", 60)
            for i in (1, 3, 5):
                d1[i].set_color(SECANT)
            self.play(Write(d1), run_time=1.4)
            b.line(1)
            d2 = M(r"f'(", "x", r") = \lim_{h\to0}\frac{f(", "x", r" + h) - f(", "x", r")}{h}", 60)
            for i in (1, 3, 5):
                d2[i].set_color(DERIV)
            self.play(TransformMatchingTex(d1, d2), run_time=1.4)
            b.line(2)
            self.play(Create(formula_box(d2.copy(), DERIV)[0].set_z_index(-1)), run_time=0.8)
        self.clear()

        ax, al = plot_axes([-0.5, 3, 1], [0, 8, 2], w=7, h=5, coords=False)
        VGroup(ax, al).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        x0, h = 1.2, ValueTracker(1.3)
        with self.beat("What h does here") as b:
            self.play(FadeIn(ax), Create(ax.plot(f, x_range=[-0.5, 2.8], color=FUNC, stroke_width=5)), run_time=1)
            p1 = closed_dot(ax, x0, f(x0), INK)
            xl = M("x", 34).next_to(ax.c2p(x0, 0), DOWN)
            p2 = always_redraw(lambda: closed_dot(ax, x0 + h.get_value(), f(x0 + h.get_value()), SECANT))
            xl2 = always_redraw(lambda: M("x + h", 30, SECANT).next_to(ax.c2p(x0 + h.get_value(), 0), DOWN))
            self.play(FadeIn(p1), FadeIn(xl), run_time=0.6)
            self.play(FadeIn(p2), FadeIn(xl2), run_time=0.6)
            b.line(1)
            tri = always_redraw(lambda: VGroup(DashedLine(ax.c2p(x0, f(x0)), ax.c2p(x0 + h.get_value(), f(x0)), color=DIM),
                                               DashedLine(ax.c2p(x0 + h.get_value(), f(x0)), ax.c2p(x0 + h.get_value(), f(x0 + h.get_value())), color=DIM)))
            frac = M(r"\frac{f(x + h) - f(x)}{h} = \frac{\text{rise}}{\text{run}}", 44).to_edge(RIGHT, buff=0.6).shift(UP * 1.6)
            self.play(FadeIn(tri), Write(frac), run_time=1.2)
            b.line(2)
            sec = always_redraw(lambda: ax.plot(lambda t: f(x0) + (2 * x0 + h.get_value()) * (t - x0), x_range=[x0 - 0.6, min(2.9, x0 + h.get_value() + 0.3)], color=SECANT, stroke_width=4))
            self.play(Create(sec), run_time=0.8)
            self.play(FadeOut(xl2), run_time=0.3)
            self.remove(xl2)
            self.play(h.animate.set_value(0.08), run_time=3)
        self.clear()

        self.example("The derivative of x squared", r"Use the definition to find $f'(x)$ for $f(x) = x^2$.",
                     [r"f'(x) = \lim_{h\to0}\frac{(x + h)^2 - x^2}{h}", r"= \lim_{h\to0}\frac{\cancel{x^2} + 2xh + h^2 - \cancel{x^2}}{h}",
                      r"= \lim_{h\to0}\frac{\cancel{h}(2x + h)}{\cancel{h}}", r"= \lim_{h\to0}(2x + h) = 2x"], at=[1, 2, 3, 4])

        with self.beat("Prime notation") as b:
            p1 = M(r"f'(x) = 2x", 56, DERIV).shift(UP * 2.2)
            self.play(Write(p1), run_time=0.8)
            b.line(1)
            p2 = VGroup(M(r"y = x^2", 48), M(r"y' = 2x", 48, DERIV)).arrange(RIGHT, buff=1.2).next_to(p1, DOWN, buff=0.7)
            self.play(FadeIn(p2), run_time=0.8)
            b.line(2)
            circ = VGroup(Circle(radius=0.7, color=FUNC), T("curves that aren't functions: later", 30, DIM)).arrange(RIGHT, buff=0.4).next_to(p2, DOWN, buff=0.6)
            self.play(FadeIn(circ), run_time=0.8)
            b.line(3)
            p3 = VGroup(M(r"g(t) = t^3 \ \Rightarrow\ g'(t)", 44), M(r"A(r) = \pi r^2 \ \Rightarrow\ A'(r)", 44)).arrange(RIGHT, buff=1.2).to_edge(DOWN, buff=1)
            self.play(FadeOut(circ), FadeIn(p3), run_time=1)
        self.clear()

        ax, al = plot_axes([-0.5, 3, 1], [0, 8, 2], w=6.6, h=5, coords=False)
        VGroup(ax, al).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        x0, hh = 1.0, ValueTracker(1.4)
        with self.beat("Little nudges") as b:
            self.play(FadeIn(ax), Create(ax.plot(f, x_range=[-0.5, 2.8], color=FUNC, stroke_width=5)), run_time=1)
            b.line(1)
            run = always_redraw(lambda: Line(ax.c2p(x0, f(x0)), ax.c2p(x0 + hh.get_value(), f(x0)), color=SECANT, stroke_width=4))
            rise = always_redraw(lambda: Line(ax.c2p(x0 + hh.get_value(), f(x0)), ax.c2p(x0 + hh.get_value(), f(x0 + hh.get_value())), color=SECANT, stroke_width=4))
            sec = always_redraw(lambda: Line(ax.c2p(x0, f(x0)), ax.c2p(x0 + hh.get_value(), f(x0 + hh.get_value())), color=TANGENT, stroke_width=4))
            big = VGroup(M(r"\Delta x", 34, SECANT), M(r"\Delta y", 34, SECANT))
            big[0].add_updater(lambda m: m.next_to(run, DOWN, buff=0.12))
            big[1].add_updater(lambda m: m.next_to(rise, RIGHT, buff=0.12))
            self.play(Create(run), Create(rise), FadeIn(big), run_time=1)
            note = T(r"$\Delta$: capital delta, ``change in''", 32, DIM).to_edge(RIGHT, buff=0.5).shift(UP * 2.4)
            self.play(FadeIn(note), run_time=0.6)
            b.line(2)
            ratio = M(r"\frac{\Delta y}{\Delta x}", 60, TANGENT).to_edge(RIGHT, buff=2).shift(UP * 0.6)
            self.play(Create(sec), Write(ratio), run_time=1)
            b.line(3)
            self.play(hh.animate.set_value(0.25), run_time=2.5)
            letters = VGroup(M(r"\Delta", 56), M(r"\to", 40, DIM), M(r"\delta", 56), M(r"\approx", 40, DIM), M(r"d", 56)).arrange(RIGHT, buff=0.3).next_to(ratio, DOWN, buff=0.8)
            self.play(LaggedStart(*[FadeIn(m) for m in letters], lag_ratio=0.3), run_time=1.4)
            small = VGroup(M(r"dx", 30, SECANT), M(r"dy", 30, SECANT))
            small[0].add_updater(lambda m: m.next_to(run, DOWN, buff=0.12))
            small[1].add_updater(lambda m: m.next_to(rise, RIGHT, buff=0.12))
            for m in big:
                m.clear_updaters()
            self.play(ReplacementTransform(big, small), run_time=0.8)
            b.line(4)
            dydx = M(r"\frac{dy}{dx}", 60, TANGENT).move_to(ratio)
            self.play(ReplacementTransform(ratio, dydx), run_time=1)
            self.play(Indicate(dydx, color=TANGENT), run_time=0.8)
            for m in small:
                m.clear_updaters()
        self.clear()

        with self.beat("Other letters, same idea") as b:
            rows = VGroup(VGroup(M(r"\frac{ds}{dt}", 54, DERIV), T(r"how fast position $s$ changes per unit of time $t$", 34)).arrange(RIGHT, buff=0.5),
                          VGroup(M(r"\frac{dA}{dr}", 54, DERIV), T(r"how fast area $A$ changes as the radius $r$ grows", 34)).arrange(RIGHT, buff=0.5),
                          VGroup(M(r"\frac{d}{dx}\left[x^2\right] = 2x", 54, DERIV), T("an instruction: take the derivative", 34)).arrange(RIGHT, buff=0.5)
                          ).arrange(DOWN, buff=0.7, aligned_edge=LEFT)
            self.play(FadeIn(rows[0]), run_time=0.8)
            b.line(1)
            self.play(FadeIn(rows[1]), run_time=0.8)
            b.line(2)
            self.play(FadeIn(rows[2]), run_time=0.8)
        self.clear()

        with self.beat("Evaluating at a point") as b:
            e1 = VGroup(M(r"f'(x) = 2x", 50), M(r"f'(3) = 2 \cdot 3 = 6", 50, DERIV)).arrange(DOWN, buff=0.5, aligned_edge=LEFT).shift(LEFT * 3.2)
            self.play(Write(e1), run_time=1.2)
            b.line(1)
            e2 = M(r"\left.\frac{dy}{dx}\right|_{x = 3} = 6", 56, DERIV).shift(RIGHT * 3.2)
            self.play(Write(e2), run_time=1.2)
            same_ = T("the same number", 34, SECANT).shift(DOWN * 1.8)
            self.play(FadeIn(same_), Circumscribe(e1[1], color=SECANT), Circumscribe(e2, color=SECANT), run_time=1.2)
        self.clear()

        with self.beat("Point-slope form") as b:
            pax, pal = plot_axes([-1, 5, 1], [-1, 5, 1], w=5, h=4.4, coords=False)
            VGroup(pax, pal).to_edge(LEFT, buff=0.8)
            ln = pax.plot(lambda t: 1 + 0.75 * (t - 1), x_range=[-0.8, 4.8], color=SECANT, stroke_width=4)
            pt = VGroup(closed_dot(pax, 1, 1, INK), M(r"(x_1, y_1)", 30).next_to(pax.c2p(1, 1), DR, buff=0.1))
            self.play(FadeIn(pax), FadeIn(pal), Create(ln), FadeIn(pt), FadeIn(M("m", 34, SECANT).next_to(pax.c2p(4, 3.25), UL, buff=0.1)), run_time=1.2)
            ps = M(r"y - y_1 = m(x - x_1)", 52).to_edge(RIGHT, buff=0.7).shift(UP * 1.2)
            self.play(Write(ps), Create(SurroundingRectangle(ps, color=SECANT, buff=0.2)), run_time=1.2)
            b.line(1)
            tl_ = M(r"y - f(a) = f'(a)(x - a)", 52, TANGENT).next_to(ps, DOWN, buff=0.9)
            self.play(Write(tl_), run_time=1.2)
        self.clear()

        a2, _ = plot_axes([0, 4, 1], [0, 16, 4], w=5, h=4.4)
        fig2 = VGroup(a2, a2.plot(f, x_range=[0, 4], color=FUNC, stroke_width=4), a2.plot(lambda t: 6 * t - 9, x_range=[1.6, 4], color=TANGENT, stroke_width=4),
                      closed_dot(a2, 3, 9, INK))
        self.example("A tangent line", r"Find the equation of the line tangent to $f(x) = x^2$ at $x = 3$. Write it in slope-intercept form.",
                     [r"f(3) = 9 \ \Rightarrow\ (3, 9)", r"f'(3) = 2 \cdot 3 = 6", r"y - 9 = 6(x - 3)", r"y = 6x - 18 + 9 = 6x - 9",
                      r"TEXT:Point-slope form is fine unless a form is asked for, or you are matching a simplified choice."], figure=fig2, at=[1, 2, 3, 4, 5])
        self.example("Units", r"$V(t)$ is the volume of water in a tank, in liters, $t$ minutes after it starts draining. Interpret $V'(4) = -12$.",
                     [r"\text{units of } V' = \frac{\text{liters}}{\text{minute}}", r"-12 < 0:\ \text{decreasing}",
                      r"TEXT:At $t = 4$ minutes, the volume of water is decreasing at $12$ liters per minute.",
                      r"TEXT:On the AP exam you must write a sentence like this: when, how fast with units, and increasing or decreasing."], at=[1, 2, 3, 4])

        top, tl, bot, bl, g = self.stacked()
        x = ValueTracker(-1.8)
        with self.beat("Close") as b:
            tan = always_redraw(lambda: tangent_line(top, f, x.get_value(), 2 * x.get_value(), [max(-2, x.get_value() - 0.6), min(2, x.get_value() + 0.6)]))
            probe = always_redraw(lambda: DashedLine(top.c2p(x.get_value(), f(x.get_value())), bot.c2p(x.get_value(), 2 * x.get_value()), color=DIM, stroke_width=2))
            self.play(FadeIn(g), Create(top.plot(f, x_range=[-2, 2], color=FUNC, stroke_width=4)), Create(bot.plot(lambda t: 2 * t, x_range=[-2, 2], color=DERIV, stroke_width=4)), run_time=1.2)
            self.add(tan, probe)
            self.play(x.animate.set_value(1.8), run_time=3)
        self.clear()

        self.examples_card()
        self.example("Example 1: A derivative from the definition", r"Use the definition to find $f'(x)$ for $f(x) = 3x^2 - 5x$.",
                     [r"f'(x) = \lim_{h\to0}\frac{3(x + h)^2 - 5(x + h) - (3x^2 - 5x)}{h}",
                      r"= \lim_{h\to0}\frac{3x^2 + 6xh + 3h^2 - 5x - 5h - 3x^2 + 5x}{h}",
                      r"= \lim_{h\to0}\frac{\cancel{3x^2} + 6xh + 3h^2 - \cancel{5x} - 5h - \cancel{3x^2} + \cancel{5x}}{h}",
                      r"= \lim_{h\to0}\frac{\cancel{h}(6x + 3h - 5)}{\cancel{h}}", r"= \lim_{h\to0}(6x + 3h - 5) = 6x - 5"], at=[1, 2, 3, 4, 5])
        self.example("Example 2: A reciprocal", r"Use the definition to find $g'(x)$ for $g(x) = \dfrac{2}{x}$.",
                     [r"g'(x) = \lim_{h\to0}\frac{\frac{2}{x + h} - \frac{2}{x}}{h} = \lim_{h\to0}\frac{\frac{2x - 2(x + h)}{x(x + h)}}{h}",
                      r"= \lim_{h\to0}\frac{\cancel{2x} - \cancel{2x} - 2h}{h\,x(x + h)}", r"= \lim_{h\to0}\frac{-2\cancel{h}}{\cancel{h}\,x(x + h)}",
                      r"= \lim_{h\to0}\frac{-2}{x(x + h)} = -\frac{2}{x^2}"], at=[1, 2, 3, 4])
        a3, _ = plot_axes([0, 3, 1], [-3, 12, 3], w=5, h=4.4)
        fig3 = VGroup(a3, a3.plot(lambda t: 3 * t * t - 5 * t, x_range=[0, 3], color=FUNC, stroke_width=4),
                      a3.plot(lambda t: 2 + 7 * (t - 2), x_range=[1.4, 3], color=TANGENT, stroke_width=4), closed_dot(a3, 2, 2, INK))
        self.example("Example 3: A tangent line", r"Find the equation for the line tangent to $f(x) = 3x^2 - 5x$ at $x = 2$.",
                     [r"f(2) = 12 - 10 = 2 \ \Rightarrow\ (2, 2)", r"f'(2) = 6(2) - 5 = 7", r"y - 2 = 7(x - 2)"], figure=fig3, at=[1, 2, 3])
        self.finish()
