"""Topic 1.5: Determining limits using algebraic properties of limits. Narration comes from transcripts/1_5.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "1.5"

    def construct(self):
        with self.beat("From estimating to computing") as b:
            thumbs = VGroup(*[VGroup(RoundedRectangle(width=3.6, height=2.6, corner_radius=0.15, color=DIM), T(n_, 36, DIM))
                              for n_ in ["graph", "table", "formula"]]).arrange(RIGHT, buff=0.5)
            self.play(FadeIn(thumbs), run_time=1)
            b.line(1)
            self.play(FadeOut(thumbs[0]), FadeOut(thumbs[1]), thumbs[2].animate.scale(2.2).move_to(ORIGIN).set_color(FUNC), run_time=1.4)
        self.clear()
        self.title()

        ax, al = plot_axes([0, 4, 1], [0, 6, 1], w=7.4, h=5.2, coords=False)
        VGroup(ax, al).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        f = lambda x: 3 + 0.4 * np.sin(2 * (x - 2))
        g = lambda x: 2 - 0.3 * (x - 2)
        cf = ax.plot(f, x_range=[0, 4], color=FUNC, stroke_width=4)
        cg = ax.plot(g, x_range=[0, 4], color=DERIV, stroke_width=4)
        cs = ax.plot(lambda x: f(x) + g(x), x_range=[0, 4], color=SECANT, stroke_width=5)
        xv = ValueTracker(0.6)
        bars = always_redraw(lambda: VGroup(
            Line(ax.c2p(xv.get_value(), 0), ax.c2p(xv.get_value(), g(xv.get_value())), color=DERIV, stroke_width=8),
            Line(ax.c2p(xv.get_value(), g(xv.get_value())), ax.c2p(xv.get_value(), g(xv.get_value()) + f(xv.get_value())), color=FUNC, stroke_width=8)))
        cmark = DashedLine(ax.c2p(2, 0), ax.c2p(2, 6), color=DIM)
        with self.beat("Adding two functions") as b:
            self.play(FadeIn(ax), FadeIn(al), Create(cf), Create(cg), FadeIn(cmark), FadeIn(M("c", 32, DIM).next_to(ax.c2p(2, 0), DOWN)), run_time=1.6)
            labs = VGroup(M(r"f \to 3", 40, FUNC), M(r"g \to 2", 40, DERIV)).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT, buff=1).shift(UP * 1.5)
            self.play(Write(labs), run_time=1)
            b.line(1)
            self.add(bars)
            self.play(Create(cs), run_time=0.8)
            self.play(xv.animate.set_value(1.98), run_time=2)
            s_ = M(r"f + g \to 3 + 2 = 5", 40, SECANT).next_to(labs, DOWN, buff=0.5, aligned_edge=LEFT)
            self.play(Write(s_), run_time=1)
            b.line(2)
            law = M(r"\lim (f + g) = \lim f + \lim g", 44).to_edge(DOWN, buff=0.5)
            self.play(Write(law), run_time=1.2)
        self.clear()

        with self.beat("The limit laws") as b:
            laws = VGroup(
                M(r"\lim\,(f - g) = 3 - 2 = 1", 44), M(r"\lim\,(2f) = 2\cdot 3 = 6", 44), M(r"\lim\,(f g) = 3\cdot 2 = 6", 44),
                M(r"\lim\, f^2 = 3^2 = 9", 44), M(r"\lim\,\frac{f}{g} = \frac{3}{2} \quad (\lim g \ne 0)", 44)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
            for m in laws[:4]:
                self.play(Write(m), run_time=0.7)
            b.line(1)
            self.play(Write(laws[4]), run_time=1)
            self.play(Indicate(laws[4][0][-9:], color=TANGENT), run_time=1)
            b.line(2)
            note = T("each law assumes the individual limits exist", 36, SECANT).to_edge(DOWN, buff=0.4)
            self.play(FadeIn(note), run_time=0.8)
        self.clear()

        with self.beat("Direct substitution") as b:
            bd = Board()
            bd.anchor = UP * 3
            bd.write(self, r"\lim_{x\to2}\left(x^3 - 4x + 1\right)")
            bd.write(self, r"= \lim_{x\to2} x^3 - 4\lim_{x\to2} x + \lim_{x\to2} 1")
            bd.write(self, r"= 8 - 8 + 1 = 1")
            b.line(1)
            bd.write(self, r"\text{rational: } \lim_{x\to c}\frac{p(x)}{q(x)} = \frac{p(c)}{q(c)} \quad \text{if } q(c) \ne 0", SECANT)
            b.line(2)
            box = callout("Direct substitution: always try it first.", SECANT, 40).to_edge(DOWN, buff=0.4)
            self.play(FadeIn(box), run_time=0.8)
        self.clear()
        self.example("Plug in", r"Find (a) $\displaystyle\lim_{x\to2}(x^3 - 4x + 1)$ and (b) $\displaystyle\lim_{x\to-1}\frac{x^2 + 3}{x - 2}$.",
                     [r"\text{(a) } \lim_{x\to2}(x^3 - 4x + 1) = 8 - 8 + 1 = 1", r"\text{(b) } x - 2 \to -3 \ne 0", r"\lim_{x\to-1}\frac{x^2 + 3}{x - 2} = \frac{4}{-3} = -\frac43"], at=[1, 2, 3])

        with self.beat("Composite functions") as b:
            inner = M(r"g(x) \to 9", 52, DERIV).shift(LEFT * 4)
            mach = VGroup(RoundedRectangle(width=2.6, height=1.6, corner_radius=0.2, color=FUNC, stroke_width=4), M(r"\sqrt{\ \ }", 52, FUNC))
            out = M(r"\sqrt{g(x)} \to 3", 52, SECANT).shift(RIGHT * 4.2)
            a1 = Arrow(inner.get_right(), mach.get_left(), color=DIM)
            a2 = Arrow(mach.get_right(), out.get_left(), color=DIM)
            self.play(Write(inner), run_time=0.8)
            self.play(FadeIn(mach), GrowArrow(a1), run_time=0.8)
            self.play(GrowArrow(a2), Write(out), run_time=1)
            b.line(1)
            note = T(r"works when the outer function is continuous at $9$ (Topic 1.11)", 34, DIM).to_edge(DOWN, buff=0.6)
            self.play(FadeIn(note), run_time=0.8)
        self.clear()
        self.example("Using given limits", r"Suppose $\displaystyle\lim_{x\to4} f(x) = 3$ and $\displaystyle\lim_{x\to4} g(x) = -2$. Find the limit as $x \to 4$ of (a) $2f(x) - g(x)$, (b) $f(x)g(x)$, (c) $\dfrac{f(x)}{g(x)}$, (d) $\left[f(x)\right]^2 + g(x)$, (e) $\sqrt{f(x) + 6}$.",
                     [r"\text{(a) } \lim_{x\to4}\left[2f(x) - g(x)\right] = 2(3) - (-2) = 8", r"\text{(b) } \lim_{x\to4} f(x)g(x) = 3(-2) = -6", r"\text{(c) } \lim_{x\to4}\frac{f(x)}{g(x)} = \frac{3}{-2} = -\frac32", r"\text{(d) } \lim_{x\to4}\left(\left[f(x)\right]^2 + g(x)\right) = 3^2 + (-2) = 7", r"\text{(e) } \lim_{x\to4}\sqrt{f(x) + 6} = \sqrt{3 + 6} = 3"], at=[1, 2, 3, 4, 5])

        ax2, al2 = plot_axes([0, 4, 1], [0, 12, 2], w=7, h=5)
        VGroup(ax2, al2).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        lp = ax2.plot(lambda x: x * x + 1, x_range=[0, 2], color=SECANT, stroke_width=5)
        rp = ax2.plot(lambda x: 3 * x - 1, x_range=[2, 4], color=TANGENT, stroke_width=5)
        with self.beat("Pieces and sides") as b:
            pw = M(r"f(x) = \begin{cases} x^2 + 1, & x < 2 \\ 3x - 1, & x \ge 2 \end{cases}", 42).to_edge(RIGHT, buff=0.6).shift(UP * 1.8)
            self.play(FadeIn(ax2), FadeIn(al2), Write(pw), run_time=1.4)
            b.line(1)
            self.play(Create(lp), run_time=1)
            l1 = M(r"\lim_{x\to2^-}(x^2 + 1) = 5", 40, SECANT).next_to(pw, DOWN, buff=0.5)
            self.play(Write(l1), run_time=1)
            self.play(Create(rp), run_time=1)
            l2 = M(r"\lim_{x\to2^+}(3x - 1) = 5", 40, TANGENT).next_to(l1, DOWN, buff=0.3)
            self.play(Write(l2), run_time=1)
            b.line(2)
            l3 = M(r"\lim_{x\to2} f(x) = 5", 46).next_to(l2, DOWN, buff=0.4)
            self.play(Write(l3), run_time=1)
        self.clear()

        with self.beat("A limit that exists anyway") as b:
            ax, al = plot_axes([-1, 3, 1], [-2, 3, 1], w=6.2, h=4.8)
            VGroup(ax, al).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.3)
            fdef = M(r"f(x) = \begin{cases} 2, & x < 1 \\ -1, & x \ge 1 \end{cases}", 44, FUNC).to_edge(LEFT, buff=0.7).shift(UP * 2.2)
            fj = VGroup(ax.plot(lambda x: 2, x_range=[-1, 1], color=FUNC, stroke_width=5), ax.plot(lambda x: -1, x_range=[1, 3], color=FUNC, stroke_width=5),
                        open_dot(ax, 1, 2), closed_dot(ax, 1, -1, FUNC))
            # 1. f alone
            self.play(Write(fdef), FadeIn(ax), FadeIn(al), run_time=1.4)
            self.play(Create(fj), run_time=1.4)
            b.line(1)
            fdne = M(r"\lim_{x\to1} f(x) \text{ does not exist}", 36, FUNC).next_to(fdef, DOWN, buff=0.3).align_to(fdef, LEFT)
            self.play(Flash(ax.c2p(1, 0.5), color=TANGENT), Write(fdne), run_time=1.2)
            # 2. g alone
            b.line(2)
            gdef = M(r"g(x) = x - 1, \qquad \lim_{x\to1} g(x) = 0", 40, DERIV).next_to(fdne, DOWN, buff=0.45).align_to(fdef, LEFT)
            gz = ax.plot(lambda x: x - 1, x_range=[-1, 3], color=DERIV, stroke_width=4)
            self.play(fj.animate.set_opacity(0.3), Write(gdef), Create(gz), run_time=1.6)
            self.play(Flash(ax.c2p(1, 0), color=DERIV), run_time=0.7)
            # 3. multiply them, piece by piece
            b.line(3)
            hdef = M(r"h(x) = f(x)\cdot g(x)", 44, SECANT).next_to(gdef, DOWN, buff=0.5).align_to(fdef, LEFT)
            self.play(Write(hdef), run_time=1.2)
            b.line(4)
            hcases = M(r"= \begin{cases} 2(x - 1), & x < 1 \\ -(x - 1), & x \ge 1 \end{cases}", 44, SECANT).next_to(hdef, DOWN, buff=0.3).align_to(fdef, LEFT).shift(RIGHT * 0.9)
            self.play(Write(hcases), run_time=1.8)
            # 4. h on its own
            b.line(5)
            hp = VGroup(ax.plot(lambda x: 2 * (x - 1), x_range=[-0.25, 1], color=SECANT, stroke_width=6),
                        ax.plot(lambda x: -(x - 1), x_range=[1, 3], color=SECANT, stroke_width=6))
            self.play(FadeOut(fj), FadeOut(gz), run_time=0.6)
            self.play(Create(hp), run_time=1.6)
            self.play(Flash(ax.c2p(1, 0), color=SECANT), run_time=0.8)
            # 5. the one-sided limits, in full
            b.line(6)
            self.play(FadeOut(VGroup(fdef, fdne, gdef)), VGroup(hdef, hcases).animate.to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.7), run_time=0.8)
            lims = VGroup(M(r"\lim_{x\to1^-} h(x) = \lim_{x\to1^-} 2(x - 1) = 0", 38, SECANT),
                          M(r"\lim_{x\to1^+} h(x) = \lim_{x\to1^+} -(x - 1) = 0", 38, SECANT),
                          M(r"\lim_{x\to1} h(x) = 0", 44, INK)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
            lims.next_to(hcases, DOWN, buff=0.6).to_edge(LEFT, buff=0.7)
            for m in lims:
                self.play(Write(m), run_time=1)
            b.line(7)
            note = T(r"the product law doesn't apply, \\ but checking each side works", 32, DIM).next_to(lims, DOWN, buff=0.5).align_to(lims, LEFT)
            self.play(FadeIn(note), run_time=0.8)
        self.clear()

        with self.beat("Close") as b:
            card = callout("try direct substitution first", SECANT, 48)
            self.play(FadeIn(card), run_time=1)
        self.clear()

        # ---------------------------------------------------------------- worked examples
        self.examples_card()
        self.example("Example 1: Using the laws",
                     r"$\displaystyle\lim_{x\to3} f(x) = 4$ and $\displaystyle\lim_{x\to3} g(x) = -2$. Find each limit.",
                     [r"PART:(a) $\displaystyle\lim_{x\to3}\big(3f(x) - f(x)g(x)\big)$",
                      r"\lim_{x\to3}\big(3f(x) - f(x)g(x)\big) = 3(4) - (4)(-2)", r"= 12 + 8 = 20",
                      r"PART:(b) $\displaystyle\lim_{x\to3}\frac{f(x)}{g(x) + 5}$",
                      r"\lim_{x\to3}\frac{f(x)}{g(x) + 5} = \frac{4}{-2 + 5}", r"= \frac43"], at=[1, 2, 3, 4, 5, 6],
                     text=r"$\displaystyle\lim_{x\to3} f(x) = 4$ and $\displaystyle\lim_{x\to3} g(x) = -2$. Find "
                          r"(a) $\displaystyle\lim_{x\to3}\big(3f(x) - f(x)g(x)\big)$ and (b) $\displaystyle\lim_{x\to3}\frac{f(x)}{g(x) + 5}$.")
        self.example("Example 2: Direct substitution", r"Find $\displaystyle\lim_{x\to-1}\frac{x^2 + 2x + 5}{x + 3}$.",
                     [r"\text{denominator: } -1 + 3 = 2 \ne 0 \ \checkmark", r"\frac{1 - 2 + 5}{2} = \frac{4}{2} = 2"], at=[1, 2])
        self.example("Example 3: A composite and a piecewise", r"Two limits at $x = 2$.",
                     [r"PART:(a) Find $\displaystyle\lim_{x\to2}\sqrt{x + 7}$.",
                      r"\lim_{x\to2}\sqrt{x + 7} = \sqrt{2 + 7} = \sqrt9 = 3",
                      r"PART:(b) $f(x) = \begin{cases} x^2 - 3, & x < 2 \\ 5 - x, & x \ge 2 \end{cases}$ \quad Find $\displaystyle\lim_{x\to2} f(x)$.",
                      r"\lim_{x\to2^-} f(x) = \lim_{x\to2^-}(x^2 - 3) = 1, \qquad \lim_{x\to2^+} f(x) = \lim_{x\to2^+}(5 - x) = 3",
                      r"\lim_{x\to2} f(x)\ \text{does not exist}"], at=[1, 2, 3, 4, 5],
                     text=r"(a) Find $\displaystyle\lim_{x\to2}\sqrt{x + 7}$. "
                          r"(b) Find $\displaystyle\lim_{x\to2} f(x)$ for \[ f(x) = \begin{cases} x^2 - 3, & x < 2 \\ 5 - x, & x \ge 2. \end{cases} \]")
        self.finish()
