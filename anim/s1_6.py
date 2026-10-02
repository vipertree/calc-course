"""Topic 1.6: Determining limits using algebraic manipulation. Narration comes from transcripts/1_6.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "1.6"

    def construct(self):
        with self.beat("Zero over zero is a message") as b:
            e = M(r"\lim_{x\to3}\frac{x^2 - 9}{x - 3}", 72, FUNC).shift(UP * 1.6)
            self.play(Write(e), run_time=1.2)
            z = M(r"\frac{9 - 9}{3 - 3} = \frac00", 60, TANGENT).next_to(e, DOWN, buff=0.6)
            self.play(Write(z), run_time=1)
            b.line(1)
            sign = VGroup(RoundedRectangle(width=5.4, height=1.2, corner_radius=0.15, color=SECANT, fill_color=PANEL, fill_opacity=1, stroke_width=4),
                          T("keep going", 48, SECANT))
            sign.next_to(z, DOWN, buff=0.6)
            post = Line(sign.get_bottom(), sign.get_bottom() + DOWN * 0.8, color=DIM, stroke_width=8)
            self.play(FadeIn(sign), Create(post), run_time=1)
            b.line(2)
            fork = VGroup(T("a number", 36, DERIV), T("no limit at all", 36, TANGENT)).arrange(RIGHT, buff=3).next_to(post, DOWN, buff=0.2)
            self.play(FadeIn(fork[0], shift=LEFT * 0.3), run_time=0.7)
            self.play(FadeIn(fork[1], shift=RIGHT * 0.3), run_time=0.7)
        self.clear()
        self.title()

        ax, al = plot_axes([0, 5, 1], [0, 9, 1], w=7.2, h=5.2)
        VGroup(ax, al).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        with self.beat("Two functions, one missing point") as b:
            fac = M(r"\frac{x^2 - 9}{x - 3} = \frac{(x - 3)(x + 3)}{x - 3}", 44).to_edge(RIGHT, buff=0.5).shift(UP * 2.2)
            self.play(Write(fac), run_time=1.4)
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(lambda x: x + 3, x_range=[0, 5], color=DERIV, stroke_width=8)), run_time=1.4)
            orig = ax.plot(lambda x: x + 3, x_range=[0, 5], color=FUNC, stroke_width=4)
            b.line(1)
            self.play(Create(orig), FadeIn(open_dot(ax, 3, 6)), run_time=1.2)
            leg = VGroup(M(r"y = x + 3", 40, DERIV), M(r"y = \frac{x^2 - 9}{x - 3}\ \ (\text{hole at } x = 3)", 40, FUNC)).arrange(DOWN, aligned_edge=LEFT).next_to(fac, DOWN, buff=0.6)
            self.play(FadeIn(leg), run_time=1)
            b.line(2)
            self.play(Indicate(leg, color=SECANT), run_time=1.2)
        self.clear()

        with self.beat("The key fact") as b:
            box = callout(r"If $f(x) = g(x)$ for all $x$ near $c$ (except possibly at $c$), then $\displaystyle\lim_{x\to c} f(x) = \lim_{x\to c} g(x)$.", INK, 38)
            box.set_max_width(12.5).shift(UP * 1.2)
            self.play(FadeIn(box), run_time=1.2)
            b.line(1)
            ch = M(r"\lim_{x\to3}\frac{x^2 - 9}{x - 3} = \lim_{x\to3}(x + 3) = 3 + 3 = 6", 50, SECANT).next_to(box, DOWN, buff=0.8)
            self.play(Write(ch), run_time=1.6)
        self.clear()

        self.example("Tool one: factor and cancel", r"Factor and cancel",
                     [r"\lim_{x\to2}\frac{x^3 - 8}{x - 2} = \lim_{x\to2}\frac{(x - 2)(x^2 + 2x + 4)}{x - 2}", r"= \lim_{x\to2}(x^2 + 2x + 4) = 4 + 4 + 4 = 12"], at=[0, 1])
        self.example("Factor", r"Find $\displaystyle\lim_{x\to2}\frac{x^3 - 8}{x - 2}$.",
                     [r"\text{plug in: } \frac{0}{0}", r"\lim_{x\to2}\frac{x^3 - 8}{x - 2} = \lim_{x\to2}\frac{\cancel{(x - 2)}(x^2 + 2x + 4)}{\cancel{x - 2}}", r"= \lim_{x\to2}(x^2 + 2x + 4) = 4 + 4 + 4 = 12"], at=[1, 2, 3])
        with self.beat("Conjugates, a quick review") as b:
            head = T("From algebra: the conjugate", 40, DIM).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), run_time=0.6)
            b.line(1)
            ident = M(r"(a + b)(a - b) = a^2 - b^2", 56, SECANT).next_to(head, DOWN, buff=0.6)
            self.play(Write(ident), run_time=1.2)
            board = Board()
            board.anchor = ident.get_bottom() + DOWN * 0.6
            b.line(2)
            board.write(self, r"\frac{1}{\sqrt5 - 2}")
            b.line(3)
            board.write(self, r"= \frac{1}{\sqrt5 - 2}\cdot\frac{\sqrt5 + 2}{\sqrt5 + 2} = \frac{\sqrt5 + 2}{5 - 4}")
            b.line(4)
            board.write(self, r"= \sqrt5 + 2", color=DERIV)
        self.clear()

        self.example("Tool two: the conjugate", r"Multiply by the conjugate",
                     [r"\lim_{x\to0}\frac{\sqrt{x + 4} - 2}{x}\cdot\frac{\sqrt{x + 4} + 2}{\sqrt{x + 4} + 2}", r"= \lim_{x\to0}\frac{x}{x(\sqrt{x + 4} + 2)}",
                      r"= \lim_{x\to0}\frac{1}{\sqrt{x + 4} + 2} = \frac14"], at=[0, 1, 1])
        self.example("Conjugate", r"Find $\displaystyle\lim_{x\to0}\frac{\sqrt{x + 4} - 2}{x}$.",
                     [r"\lim_{x\to0}\frac{\sqrt{x + 4} - 2}{x}\cdot\frac{\sqrt{x + 4} + 2}{\sqrt{x + 4} + 2}", r"= \lim_{x\to0}\frac{(x + 4) - 4}{x\left(\sqrt{x + 4} + 2\right)}", r"= \lim_{x\to0}\frac{\cancel{x}}{\cancel{x}\left(\sqrt{x + 4} + 2\right)}", r"= \lim_{x\to0}\frac{1}{\sqrt{x + 4} + 2} = \frac14"], at=[1, 2, 3, 4])
        self.example("Tool three: clear the fractions", r"Combine the fractions",
                     [r"\lim_{x\to3}\frac{\frac1x - \frac13}{x - 3} = \lim_{x\to3}\frac{\frac{3 - x}{3x}}{x - 3}", r"= \lim_{x\to3}\frac{-1}{3x} = -\frac19"], at=[0, 1])
        self.example("Combine fractions", r"Find $\displaystyle\lim_{x\to3}\frac{\frac1x - \frac13}{x - 3}$.",
                     [r"\lim_{x\to3}\frac{\frac1x - \frac13}{x - 3} = \lim_{x\to3}\frac{\frac{3 - x}{3x}}{x - 3}", r"= \lim_{x\to3}\frac{-\cancel{(x - 3)}}{3x\cancel{(x - 3)}}", r"= \lim_{x\to3}\left(-\frac{1}{3x}\right) = -\frac19"], at=[1, 2, 3])
        with self.beat("Tool four: trig identities") as b:
            R, O, th = 2.2, LEFT * 3.8 + DOWN * 0.8, 0.85
            P = O + R * np.array([np.cos(th), np.sin(th), 0])
            foot = O + RIGHT * R * np.cos(th)
            circ = VGroup(Circle(radius=R, color=DIM, stroke_width=3).move_to(O),
                          Line(O + LEFT * (R + 0.3), O + RIGHT * (R + 0.3), color=DIM, stroke_width=2),
                          Line(O + DOWN * (R + 0.3), O + UP * (R + 0.3), color=DIM, stroke_width=2))
            tri = VGroup(Line(O, P, color=INK, stroke_width=5), Line(O, foot, color=FUNC, stroke_width=6), Line(foot, P, color=SECANT, stroke_width=6))
            labs = VGroup(M("1", 36).move_to((O + P) / 2 + np.array([-0.25, 0.25, 0])), M(r"\cos x", 34, FUNC).next_to(tri[1], DOWN, buff=0.12),
                          M(r"\sin x", 34, SECANT).next_to(tri[2], RIGHT, buff=0.12), M("x", 32).move_to(O + 0.5 * np.array([np.cos(th / 2), np.sin(th / 2), 0])))
            self.play(Create(circ), run_time=1)
            self.play(Create(tri), FadeIn(labs), run_time=1.2)
            b.line(1)
            pyth = M(r"\sin^2 x + \cos^2 x = 1", 60, INK)
            box = formula_box(pyth, DERIV).to_edge(RIGHT, buff=0.8).shift(UP * 1.6)
            self.play(Indicate(tri, color=DERIV), FadeIn(box), run_time=1.4)
            b.line(2)
            forms = VGroup(M(r"1 - \cos^2 x = \sin^2 x", 42), M(r"1 - \sin^2 x = \cos^2 x", 42)).arrange(DOWN, buff=0.35).next_to(box, DOWN, buff=0.5)
            self.play(FadeIn(forms), run_time=1)
            star = T(r"the one identity AP Calculus expects you to know", 30, DERIV).next_to(forms, DOWN, buff=0.4)
            self.play(FadeIn(star), run_time=0.8)
        self.clear()
        self.example("Tool four, in a limit", r"Use the Pythagorean identity",
                     [r"\lim_{x\to0}\frac{\sin^2 x}{1 - \cos x} = \lim_{x\to0}\frac{1 - \cos^2 x}{1 - \cos x} = \lim_{x\to0}\frac{(1 - \cos x)(1 + \cos x)}{1 - \cos x}",
                      r"= \lim_{x\to0}(1 + \cos x) = 2"], at=[0, 1])
        self.example("Identity", r"Find $\displaystyle\lim_{x\to0}\frac{\sin^2 x}{1 - \cos x}$.",
                     [r"\sin^2 x = 1 - \cos^2 x", r"\lim_{x\to0}\frac{1 - \cos^2 x}{1 - \cos x} = \lim_{x\to0}\frac{\cancel{(1 - \cos x)}(1 + \cos x)}{\cancel{1 - \cos x}}", r"= \lim_{x\to0}(1 + \cos x) = 2"], at=[1, 2, 3])

        a2, al2 = plot_axes([0, 6, 1], [-6, 6, 2], w=6.4, h=4.8)
        VGroup(a2, al2).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.3)
        with self.beat("A different message") as b:
            q = M(r"\lim_{x\to3}\frac{x + 1}{x - 3}:\quad \frac{4}{0}", 52, TANGENT).to_edge(LEFT, buff=0.7).shift(UP * 1.6)
            self.play(Write(q), run_time=1.2)
            b.line(1)
            self.play(FadeIn(a2), FadeIn(al2), FadeIn(asymptote(a2, 3, [-6, 6])),
                      Create(a2.plot(lambda x: (x + 1) / (x - 3), x_range=[0, 2.62], color=FUNC, stroke_width=4)),
                      Create(a2.plot(lambda x: (x + 1) / (x - 3), x_range=[3.4, 6], color=FUNC, stroke_width=4)), run_time=1.8)
            t = T(r"no hole to fix:\\ a vertical asymptote", 40, SECANT).next_to(q, DOWN, buff=0.8).align_to(q, LEFT)
            self.play(FadeIn(t), run_time=0.8)
        self.clear()

        with self.beat("Close") as b:
            top = callout("substitute", INK, 44).shift(UP * 2.2)
            br = VGroup(T(r"a number: done", 38, DERIV), T(r"$\frac00$: rewrite, try again", 38, SECANT), T(r"$\frac{\text{nonzero}}{0}$: unbounded", 38, TANGENT)).arrange(RIGHT, buff=0.8).shift(DOWN * 0.6)
            arrows = VGroup(*[Arrow(top.get_bottom(), m.get_top(), color=DIM, buff=0.15) for m in br])
            self.play(FadeIn(top), run_time=0.6)
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(m)) for a, m in zip(arrows, br)], lag_ratio=0.5), run_time=2.4)
        self.clear()

        self.examples_card()
        self.example("Example 1: Factor and cancel", r"Find $\displaystyle\lim_{x\to-4}\frac{x^2 + x - 12}{x + 4}$.",
                     [r"\frac{16 - 4 - 12}{-4 + 4} = \frac00", r"\lim_{x\to-4}\frac{(x + 4)(x - 3)}{x + 4}", r"= \lim_{x\to-4}(x - 3)", r"= -7"], at=[1, 2, 3, 4])
        self.example("Example 2: A conjugate in the denominator", r"Find $\displaystyle\lim_{x\to9}\frac{x - 9}{\sqrt x - 3}$.",
                     [r"\lim_{x\to9}\frac{(x - 9)(\sqrt x + 3)}{(\sqrt x - 3)(\sqrt x + 3)}", r"= \lim_{x\to9}\frac{(x - 9)(\sqrt x + 3)}{x - 9}", r"= \lim_{x\to9}(\sqrt x + 3)",
                      r"= 3 + 3 = 6"], at=[1, 2, 2, 3])
        self.example("Example 3: Zero over zero, and still no limit", r"Find $\displaystyle\lim_{x\to1}\frac{x - 1}{x^2 - 2x + 1}$.",
                     [r"\lim_{x\to1}\frac{x - 1}{(x - 1)^2}", r"= \lim_{x\to1}\frac{1}{x - 1}", r"\text{substitute: } \frac{1}{0}",
                      r"\lim_{x\to1^-} = -\infty, \quad \lim_{x\to1^+} = \infty", r"\text{does not exist}"], at=[1, 2, 3, 4, 5])
        self.finish()
