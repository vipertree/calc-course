"""Topic 1.7: Selecting procedures for determining limits. Narration comes from transcripts/1_7.md."""
from manim import *

from kit import *
from style import *


def box(text, color=INK, w=None, size=36):
    t = T(text, size, color)
    r = RoundedRectangle(width=(w or t.width + 0.6), height=t.height + 0.5, corner_radius=0.12, color=color, fill_color=PANEL, fill_opacity=1, stroke_width=3)
    return VGroup(r, t.move_to(r))


class Lesson(TranscriptScene):
    NUM = "1.7"

    def construct(self):
        cards = [r"\lim_{x\to2}(x^3 - x)", r"\lim_{x\to1}\frac{x^2 - 1}{x - 1}", r"\lim_{x\to4}\frac{\sqrt x - 2}{x - 4}",
                 r"\lim_{x\to0}\frac{|x|}{x}", r"\lim_{x\to3}\frac{x + 1}{(x - 3)^2}", r"\lim_{x\to0}\frac{\sin^2 x}{1 - \cos x}"]
        with self.beat("A pile of limits") as b:
            pile = VGroup(*[VGroup(RoundedRectangle(width=3.8, height=1.6, corner_radius=0.12, color=DIM, fill_color=PANEL, fill_opacity=1), M(c, 34))
                            for c in cards])
            for m in pile:
                m[1].move_to(m[0])
            pile.arrange_in_grid(2, 3, buff=0.4)
            self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.5, rate_func=rush_from) for m in pile], lag_ratio=0.15), run_time=2.2)
            b.line(1)
            self.play(Indicate(pile, color=SECANT, scale_factor=1.03), run_time=1)
        self.clear()
        self.title()

        # the toolkit tray: four slots along the bottom, a tool card drops into each (Adder: a toolkit, not a decision tree)
        names = ["Direct substitution", "Rewrite and cancel", "Special identities", "Split into sides"]
        colors = [DERIV, SECANT, ACCUM, TANGENT]
        slots = VGroup(*[RoundedRectangle(width=3.1, height=0.95, corner_radius=0.12, color=DIM, stroke_width=2) for _ in names]
                       ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.35)
        tools = [box(n, c, w=3.1, size=28).move_to(sl) for n, c, sl in zip(names, colors, slots)]
        tray = VGroup(slots)

        def drop(k):
            card = tools[k]
            self.play(FadeIn(card, shift=DOWN * 1.2), run_time=0.7)
            tray.add(card)

        def detail(*mobs):
            g = VGroup(*mobs).arrange(DOWN, buff=0.45).move_to(UP * 1.1)
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in g], lag_ratio=0.35), run_time=1.6)
            return g

        with self.beat("Tool one: direct substitution") as b:
            self.play(Create(slots), run_time=1)
            drop(0)
            res = VGroup(box("a number", DERIV, size=30), box(r"$\frac00$", SECANT, size=30), box(r"$\frac{\text{nonzero}}{0}$", TANGENT, size=30)).arrange(RIGHT, buff=0.8)
            d = detail(M(r"\lim_{x\to c} f(x) \ \to\ f(c)", 48, INK), res)
            b.line(1)
            self.play(Indicate(res[0], color=DERIV), run_time=0.8)
            b.line(2)
            self.play(Indicate(res[1], color=SECANT), Indicate(res[2], color=TANGENT), run_time=1)
            self.play(FadeOut(d), run_time=0.5)

        with self.beat("Tool two: rewrite and cancel") as b:
            drop(1)
            b.line(1)
            ex = VGroup(M(r"\frac{x^2 - 1}{x - 1} = \frac{(x - 1)(x + 1)}{x - 1}", 38),
                        M(r"\frac{\sqrt x - 2}{x - 4}\cdot\frac{\sqrt x + 2}{\sqrt x + 2}", 38),
                        M(r"\frac{\frac{1}{x + 2} - \frac12}{x} = \frac{-x}{2x(x + 2)}", 38))
            d = detail(*ex)
            b.line(2)
            self.play(Indicate(d, color=SECANT, scale_factor=1.02), run_time=1)
            b.line(3)
            inf = M(r"\text{also } \frac{\infty}{\infty} \text{ (Topic 1.15)}", 34, SECANT).next_to(d, RIGHT, buff=0.4)
            self.play(FadeIn(inf, shift=LEFT * 0.2), run_time=0.8)
            self.play(FadeOut(d), FadeOut(inf), run_time=0.5)

        with self.beat("Tool three: special identities") as b:
            drop(2)
            b.line(1)
            d = detail(M(r"\sin^2 x + \cos^2 x = 1", 48, ACCUM),
                       M(r"\sin^2 x = 1 - \cos^2 x = (1 - \cos x)(1 + \cos x)", 40))
            self.play(FadeOut(d), run_time=0.5)

        with self.beat("Tool four: split into sides") as b:
            drop(3)
            b.line(1)
            nl = NumberLine(x_range=[-1, 1, 1], length=4.5, color=DIM, include_numbers=False)
            c_lab = M("c", 34).next_to(nl.n2p(0), DOWN, buff=0.15)
            signs = VGroup(M("-", 44, TANGENT).next_to(nl.n2p(-0.5), UP), M("+", 44, DERIV).next_to(nl.n2p(0.5), UP))
            d = detail(T(r"piecewise \quad absolute value \quad $\frac{\text{nonzero}}{0}$", 34), VGroup(nl, c_lab, signs))
            b.line(2)
            res = T(r"same sign: $\pm\infty$ \quad opposite signs: DNE", 32).next_to(d, DOWN, buff=0.3)
            self.play(FadeIn(res), run_time=0.8)
        self.clear()
        self.example("Signs near a zero denominator", r"Find (a) $\displaystyle\lim_{x\to2}\frac{x + 1}{(x - 2)^2}$ and (b) $\displaystyle\lim_{x\to2}\frac{x + 1}{x - 2}$.",
                     [r"\text{(a) } \frac{3}{0}: \ (x - 2)^2 > 0 \text{ on both sides}", r"\lim_{x\to2}\frac{x + 1}{(x - 2)^2} = \infty", r"\text{(b) } \lim_{x\to2^-}\frac{x + 1}{x - 2} = -\infty, \quad \lim_{x\to2^+}\frac{x + 1}{x - 2} = \infty", r"\text{the limit does not exist}"], at=[1, 2, 3, 4], follow=True)

        with self.beat("Absolute values and pieces") as b:
            e = M(r"\lim_{x\to2}\frac{|x - 2|}{x - 2}", 64, FUNC).shift(UP * 1.8)
            self.play(Write(e), run_time=1)
            b.line(1)
            nl = NumberLine(x_range=[0, 4, 1], length=9, color=DIM, include_numbers=True, font_size=30).shift(DOWN * 0.2)
            lft = M(r"x < 2:\ \ \frac{-(x - 2)}{x - 2} = -1", 40, SECANT).next_to(nl.n2p(1), DOWN, buff=0.6)
            rgt = M(r"x > 2:\ \ \frac{x - 2}{x - 2} = 1", 40, TANGENT).next_to(nl.n2p(3.2), DOWN, buff=0.6)
            self.play(Create(nl), run_time=0.8)
            self.play(Write(lft), run_time=1)
            self.play(Write(rgt), run_time=1)
            dn = T("the sides disagree: no limit", 38).to_edge(DOWN, buff=0.4)
            self.play(FadeIn(dn), run_time=0.6)
        self.clear()
        self.example("Absolute value", r"Find $\displaystyle\lim_{x\to2}\frac{|x - 2|}{x - 2}$.",
                     [r"\lim_{x\to2^-}\frac{|x - 2|}{x - 2} = \lim_{x\to2^-}\frac{-(x - 2)}{x - 2} = -1", r"\lim_{x\to2^+}\frac{|x - 2|}{x - 2} = \lim_{x\to2^+}\frac{x - 2}{x - 2} = 1", r"\text{the sides disagree: the limit does not exist}"], at=[1, 2, 3])

        self.example("Working through one", r"$\displaystyle\lim_{x\to-4}\frac{x^2 + 2x - 8}{\sqrt{x + 5} - 1}$",
                     [r"\frac{16 - 8 - 8}{\sqrt1 - 1} = \frac00", r"\lim_{x\to-4}\frac{(x^2 + 2x - 8)(\sqrt{x + 5} + 1)}{(x + 5) - 1}",
                      r"= \lim_{x\to-4}\frac{(x + 4)(x - 2)(\sqrt{x + 5} + 1)}{x + 4}", r"= (-6)(2) = -12"], at=[0, 1, 2, 2])
        self.example("Two tools in one", r"Find $\displaystyle\lim_{x\to-4}\frac{x^2 + 2x - 8}{\sqrt{x + 5} - 1}$.",
                     [r"\lim_{x\to-4}\frac{(x + 4)(x - 2)}{\sqrt{x + 5} - 1}\cdot\frac{\sqrt{x + 5} + 1}{\sqrt{x + 5} + 1}", r"= \lim_{x\to-4}\frac{\cancel{(x + 4)}(x - 2)\left(\sqrt{x + 5} + 1\right)}{\cancel{x + 4}}", r"= \lim_{x\to-4}(x - 2)\left(\sqrt{x + 5} + 1\right) = (-6)(2) = -12"], at=[1, 2, 3])

        with self.beat("Close") as b:
            names2 = ["Direct substitution", "Rewrite and cancel", "Special identities", "Split into sides"]
            kit_ = VGroup(*[box(n, c, w=4.6, size=32) for n, c in zip(names2, [DERIV, SECANT, ACCUM, TANGENT])])
            later = VGroup(DashedVMobject(RoundedRectangle(width=4.6, height=0.95, corner_radius=0.12, color=DIM), num_dashes=40),
                           T(r"coming later: L'Hospital's Rule", 28, DIM))
            later[1].move_to(later[0])
            grid = VGroup(*kit_, later).arrange_in_grid(3, 2, buff=(0.5, 0.35)).move_to(ORIGIN)
            head = T("A toolkit for limits", 44).next_to(grid, UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(m, shift=DOWN * 0.3) for m in kit_], lag_ratio=0.25), run_time=2)
            b.line(1)
            self.play(Create(later[0]), FadeIn(later[1]), run_time=1)
        self.clear()

        self.examples_card()
        self.example("Example 1: Nothing to fix", r"Find $\displaystyle\lim_{x\to2}\frac{x^2 + 1}{x + 3}$.",
                     [r"\frac{4 + 1}{2 + 3} = \frac{5}{5}", r"= 1"], at=[1, 2])
        self.example("Example 2: Fractions inside a fraction", r"Find $\displaystyle\lim_{x\to0}\frac{\frac{1}{x + 2} - \frac12}{x}$.",
                     [r"\frac{\frac12 - \frac12}{0} = \frac00", r"\lim_{x\to0}\frac{\frac{2 - (x + 2)}{2(x + 2)}}{x} = \lim_{x\to0}\frac{-x}{2x(x + 2)}",
                      r"= \lim_{x\to0}\frac{-1}{2(x + 2)}", r"= -\frac14"], at=[1, 2, 3, 4])
        self.example("Example 3: Nonzero over zero", r"Find $\displaystyle\lim_{x\to5}\frac{x + 1}{(x - 5)^2}$.",
                     [r"\frac{6}{0}", r"\text{top} \approx 6 > 0, \quad (x - 5)^2 > 0 \text{ on both sides}", r"\lim_{x\to5}\frac{x + 1}{(x - 5)^2} = \infty"], at=[1, 2, 3])
        self.finish()
