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

        sub = box("Substitute", SECANT).to_edge(UP, buff=0.5)
        outs = VGroup(box("a number", DERIV), box(r"$\frac00$", SECANT), box(r"$\frac{\text{nonzero}}{0}$", TANGENT)).arrange(RIGHT, buff=1.4).next_to(sub, DOWN, buff=1.0)
        arr = VGroup(*[Arrow(sub.get_bottom(), o.get_top(), color=DIM, buff=0.1) for o in outs])
        with self.beat("Step one is always the same") as b:
            self.play(FadeIn(sub), run_time=0.8)
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(o)) for a, o in zip(arr, outs)], lag_ratio=0.3), run_time=1.8)
            b.line(1)
            done = T("done", 36, DERIV).next_to(outs[0], DOWN, buff=0.4)
            self.play(FadeIn(done), Indicate(outs[0], color=DERIV), run_time=1)

        with self.beat("When you get zero over zero") as b:
            tools = VGroup(*[box(t_, SECANT, size=28) for t_ in ["factor", "conjugate", "combine fractions", "identity"]]).arrange(DOWN, buff=0.18).next_to(outs[1], DOWN, buff=0.5)
            self.play(FadeIn(tools[0], shift=DOWN * 0.2), run_time=0.5)
            b.line(1)
            for m in tools[1:]:
                self.play(FadeIn(m, shift=DOWN * 0.2), run_time=0.5)
            b.line(2)
            back = CurvedArrow(tools.get_left() + LEFT * 0.1, sub.get_left() + LEFT * 0.1, angle=-PI / 2.4, color=SECANT)
            self.play(Create(back), run_time=1.2)
            b.line(3)
            inf = M(r"\text{also } \frac{\infty}{\infty}", 34, SECANT).next_to(outs[1], RIGHT, buff=0.25)
            self.play(FadeIn(inf, shift=LEFT * 0.2), run_time=0.8)

        with self.beat("When you get nonzero over zero") as b:
            sg = box("check signs on each side", TANGENT, size=28).next_to(outs[2], DOWN, buff=0.5)
            self.play(FadeIn(sg), run_time=0.8)
            nl = NumberLine(x_range=[-1, 1, 1], length=3, color=DIM, include_numbers=False).next_to(sg, DOWN, buff=0.5)
            signs = VGroup(M("-", 40, TANGENT).next_to(nl.n2p(-0.5), UP), M("+", 40, DERIV).next_to(nl.n2p(0.5), UP))
            self.play(Create(nl), FadeIn(signs), run_time=1)
            b.line(1)
            res = T(r"same: $\pm\infty$ \quad different: DNE", 28, INK).next_to(nl, DOWN, buff=0.3)
            self.play(FadeIn(res), run_time=0.8)
        self.clear()
        self.example("Signs near a zero denominator", r"Find (a) $\displaystyle\lim_{x\to2}\frac{x + 1}{(x - 2)^2}$ and (b) $\displaystyle\lim_{x\to2}\frac{x + 1}{x - 2}$.",
                     [r"\text{(a) } \frac{3}{0}: \ (x - 2)^2 > 0 \text{ on both sides}", r"\lim_{x\to2}\frac{x + 1}{(x - 2)^2} = \infty", r"\text{(b) } \lim_{x\to2^-}\frac{x + 1}{x - 2} = -\infty, \quad \lim_{x\to2^+}\frac{x + 1}{x - 2} = \infty", r"\text{the limit does not exist}"], at=[1, 2, 3, 4])

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
            sub2 = box("Substitute", SECANT).to_edge(UP, buff=0.8)
            outs2 = VGroup(box("done", DERIV), box("rewrite, then try again", SECANT), box("check signs", TANGENT)).arrange(RIGHT, buff=0.8).next_to(sub2, DOWN, buff=1.2)
            arr2 = VGroup(*[Arrow(sub2.get_bottom(), o.get_top(), color=DIM, buff=0.1) for o in outs2])
            self.play(FadeIn(sub2), LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(o)) for a, o in zip(arr2, outs2)], lag_ratio=0.3), run_time=2.2)
            b.line(1)
            lh = T(r"coming in Unit 4: L'Hôpital's rule", 30, DIM).next_to(outs2[1], DOWN, buff=0.5)
            self.play(FadeIn(lh), run_time=0.8)
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
