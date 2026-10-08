"""Topic 1.15: Connecting limits at infinity and horizontal asymptotes. Narration comes from transcripts/1_15.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def f(x):
    return (3 * x * x + x) / (x * x + 1)


def view(R):
    ax, al = plot_axes([-R, R, R / 5], [-1, 4, 1], w=10.5, h=4.8, coords=False)
    ax.shift(DOWN * 0.3)
    lab = M(rf"-{R:.3g} \le x \le {R:.3g}", 34, DIM).next_to(ax, DOWN, buff=0.2)
    # sample densely near 0, where the dip is narrow at wide windows (a coarse plot invents wiggles there)
    xs = np.unique(np.concatenate([np.linspace(-R, R, 800), np.linspace(-min(R, 12), min(R, 12), 800)]))
    curve = VMobject(color=FUNC, stroke_width=5).set_points_smoothly([ax.c2p(x, f(x)) for x in xs])
    return VGroup(ax, curve, DashedLine(ax.c2p(-R, 3), ax.c2p(R, 3), color=SECANT), lab)


class Lesson(TranscriptScene):
    NUM = "1.15"

    def construct(self):
        v = view(5)
        with self.beat("Zooming out") as b:
            self.play(FadeIn(v[0]), Create(v[1]), FadeIn(v[3]), run_time=1.6)
            b.line(1)
            # a real, continuous zoom out: the window is redrawn every frame on a log scale (no morphing between levels)
            self.remove(v, *v)          # its pieces were added one by one, so remove them too
            z = ValueTracker(np.log10(5))
            v = always_redraw(lambda: view(10 ** z.get_value()))
            self.add(v)
            self.play(z.animate.set_value(np.log10(500)), run_time=3.2, rate_func=smooth)
            v.clear_updaters()
            self.play(Create(v[2]), run_time=0.8)
        self.clear()
        self.title()

        v = view(50)
        self.add(v)
        with self.beat("Limits at infinity") as b:
            st = M(r"\lim_{x\to\infty} f(x) = 3", 54, SECANT).to_edge(UP, buff=0.4)
            self.play(Write(st), run_time=1.2)
            b.line(1)
            card = callout(r"a horizontal line: $y = c$ \\ $y = 3$: every point at height $3$", INK, 32).to_corner(DL, buff=0.5).shift(UP * 0.4)
            self.play(FadeIn(card), Indicate(v[2], color=SECANT), run_time=1.2)
            b.line(2)
            ha = T(r"horizontal asymptote $y = 3$", 36, SECANT).next_to(v[0].c2p(30, 3), UP, buff=0.2)
            self.play(FadeIn(ha), FadeOut(card), run_time=0.8)
        self.clear()

        with self.beat("The biggest term wins") as b:
            e = M(r"\frac{3x^2 + x}{x^2 + 1}", 64, FUNC).to_edge(UP, buff=0.5)
            self.play(Write(e), run_time=1)
            b.line(1)
            items = [("3x^2", 3e6, FUNC), ("x", 1e3, DIM), ("x^2", 1e6, FUNC), ("1", 1, DIM)]
            bars = VGroup()
            for name, val, col in items:
                ln = max(0.04, 9 * val / 3e6)
                bars.add(VGroup(M(name, 36, col), Rectangle(width=ln, height=0.35, fill_color=col, fill_opacity=0.85, stroke_width=0)).arrange(RIGHT, buff=0.3))
            bars.arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(e, DOWN, buff=0.5)
            sub = M(r"x = 1000", 36, DIM).next_to(bars, UP, buff=0.15).align_to(bars, RIGHT)
            self.play(FadeIn(sub), LaggedStart(*[GrowFromEdge(bb, LEFT) for bb in bars], lag_ratio=0.3), run_time=2)
            b.line(2)
            big = callout(r"For large $x$, only the fastest-growing terms matter.", DERIV, 34).next_to(bars, DOWN, buff=0.4)
            self.play(FadeIn(big), run_time=0.8)
            b.line(3)
            self.play(FadeOut(bars), FadeOut(sub), big.animate.next_to(e, DOWN, buff=0.4), run_time=0.8)
            chain = M(r"\lim_{x\to\infty}\frac{3x^2 + x}{x^2 + 1} = \lim_{x\to\infty}\frac{3x^2}{x^2}", 48).next_to(big, DOWN, buff=0.6)
            self.play(Write(chain), run_time=1.4)
            b.line(4)
            lk = M(r"= \lim_{x\to\infty} 3 = 3", 48, SECANT).next_to(chain, DOWN, buff=0.35)
            self.play(Write(lk), run_time=1)
        self.clear()

        self.example("Dividing by the highest power", r"Divide top and bottom by $x^2$",
                     [r"\lim_{x\to\infty}\frac{3x^2 + x}{x^2 + 1} = \lim_{x\to\infty}\frac{3 + \frac1x}{1 + \frac{1}{x^2}}", r"= \frac{3 + 0}{1 + 0} = 3"], at=[0, 1], follow=True)

        with self.beat("Three cases for rational functions") as b:
            cols = VGroup(VGroup(T("bottom degree bigger", 34, DIM), M(r"\frac{2x}{x^2 + 1} \to 0", 44)),
                          VGroup(T("equal degrees", 34, DIM), M(r"\frac{6x^2}{2x^2 + 1} \to \frac62 = 3", 44)),
                          VGroup(T("top degree bigger", 34, DIM), M(r"\frac{x^3}{x^2 + 1} \to \infty", 44)))
            for c in cols:
                c.arrange(DOWN, buff=0.4)
            cols.arrange(RIGHT, buff=0.9)
            b.line(1)
            self.play(FadeIn(cols[0]), run_time=0.8)
            self.play(FadeIn(cols[1]), run_time=0.8)
            b.line(2)
            self.play(FadeIn(cols[2]), run_time=0.8)
            no = T("no horizontal asymptote", 30, TANGENT).next_to(cols[2], DOWN, buff=0.3)
            self.play(FadeIn(no), run_time=0.6)
        self.clear()

        with self.beat("Other functions") as b:
            a1, _ = plot_axes([0, 6, 1], [0, 1.2, 0.5], w=3.8, h=2.8, coords=False)
            a2, _ = plot_axes([-6, 6, 2], [0, 6, 1], w=3.8, h=2.8, coords=False)
            a3, _ = plot_axes([1, 20, 5], [-0.4, 1, 0.5], w=3.8, h=2.8, coords=False)
            p1 = VGroup(a1, a1.plot(lambda x: np.exp(-x), x_range=[0, 6], color=FUNC), M(r"e^{-x}", 32).next_to(a1, DOWN))
            p2 = VGroup(a2, a2.plot(lambda x: 5 / (1 + np.exp(-x)), x_range=[-6, 6], color=FUNC), DashedLine(a2.c2p(-6, 5), a2.c2p(6, 5), color=SECANT),
                        M(r"\frac{5}{1 + e^{-x}}", 32).next_to(a2, DOWN))
            p3 = VGroup(a3, a3.plot(lambda x: np.sin(x) / x, x_range=[1, 20], color=FUNC), M(r"\frac{\sin x}{x}", 32).next_to(a3, DOWN))
            VGroup(p1, p2, p3).arrange(RIGHT, buff=0.5)
            self.play(FadeIn(p1), run_time=1)
            b.line(1)
            self.play(FadeIn(p2), run_time=1)
            b.line(2)
            self.play(FadeIn(p3), run_time=1)
        self.clear()
        self.example("Roots at negative infinity", r"Find $\displaystyle\lim_{x\to-\infty}\frac{\sqrt{4x^2 + 1}}{x}$.",
                     [r"\text{leading terms: } \frac{\sqrt{4x^2}}{x} = \frac{2|x|}{x}", r"x < 0: \ |x| = -x", r"\lim_{x\to-\infty}\frac{\sqrt{4x^2 + 1}}{x} = \lim_{x\to-\infty}\frac{2(-x)}{x} = -2"], at=[1, 2, 3], follow=True)

        with self.beat("Close") as b:
            v = view(500)
            self.play(FadeIn(v), run_time=1.2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Equal degrees", r"Find $\displaystyle\lim_{x\to\infty}\frac{4x^2 - 3x}{2x^2 + 5}$.",
                     [r"\text{leading terms: } 4x^2 \text{ and } 2x^2", r"\lim_{x\to\infty}\frac{4x^2 - 3x}{2x^2 + 5} = \lim_{x\to\infty}\frac{4x^2}{2x^2}",
                      r"= \lim_{x\to\infty} 2 = 2", r"y = 2 \text{ is a horizontal asymptote}"],
                     at=[1, 2, 3, 4])
        self.example("Example 2: A square root at negative infinity", r"Find $\displaystyle\lim_{x\to-\infty}\frac{5x + 1}{\sqrt{x^2 + 4}}$.",
                     [r"\lim_{x\to-\infty}\frac{5x + 1}{\sqrt{x^2 + 4}} = \lim_{x\to-\infty}\frac{5x}{\sqrt{x^2}}", r"\sqrt{x^2} = |x| = -x \ \text{ for } x < 0",
                      r"= \lim_{x\to-\infty}\frac{5x}{-x} = \lim_{x\to-\infty}(-5) = -5", r"\text{at } +\infty:\ \lim_{x\to\infty}\frac{5x}{x} = 5"], at=[1, 2, 3, 4])
        self.example("Example 3: Compare the degrees", r"Two limits at infinity.",
                     [r"PART:(a) $\displaystyle\lim_{x\to\infty}\frac{x^2 + 1}{x - 3}$",
                      r"\lim_{x\to\infty}\frac{x^2 + 1}{x - 3} = \lim_{x\to\infty}\frac{x^2}{x} = \lim_{x\to\infty} x = \infty",
                      r"PART:(b) $\displaystyle\lim_{x\to\infty}\frac{7x}{x^3 - 1}$",
                      r"\lim_{x\to\infty}\frac{7x}{x^3 - 1} = \lim_{x\to\infty}\frac{7x}{x^3} = \lim_{x\to\infty}\frac{7}{x^2} = 0"], at=[1, 2, 3, 4],
                     text=r"Find (a) $\displaystyle\lim_{x\to\infty}\frac{x^2 + 1}{x - 3}$ and (b) $\displaystyle\lim_{x\to\infty}\frac{7x}{x^3 - 1}$.")
        self.finish()
