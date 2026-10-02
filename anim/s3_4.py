"""Topic 3.4: Derivatives of inverse trig functions. Narration comes from transcripts/3_4.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def triangle(scale=2.6):
    """Right triangle with angle y at the left: opposite x, hypotenuse 1, adjacent sqrt(1 - x^2)."""
    xv = 0.6
    A, B, C = ORIGIN, RIGHT * np.sqrt(1 - xv ** 2) * scale, RIGHT * np.sqrt(1 - xv ** 2) * scale + UP * xv * scale
    tri = Polygon(A, B, C, color=INK, stroke_width=4)
    corner = Square(0.2, color=DIM, stroke_width=2).move_to(B + LEFT * 0.1 + UP * 0.1)
    ang = Arc(radius=0.55, start_angle=0, angle=np.arctan2(xv, np.sqrt(1 - xv ** 2)), arc_center=A, color=SECANT)
    y = M("y", 34, SECANT).move_to(A + 0.85 * np.array([np.cos(0.3), np.sin(0.3), 0]))
    opp = M("x", 38, FUNC).next_to(Line(B, C), RIGHT, buff=0.15)
    hyp = M("1", 38).move_to((A + C) / 2 + np.array([-0.3, 0.35, 0]))
    adj = M(r"\sqrt{1 - x^2}", 38, DERIV).next_to(Line(A, B), DOWN, buff=0.15)
    return VGroup(tri, corner, ang, y), opp, hyp, adj


class Lesson(TranscriptScene):
    NUM = "3.4"

    def construct(self):
        with self.beat("Angles from ratios") as b:
            ramp = Polygon(LEFT * 5.8 + DOWN * 1.2, LEFT * 1.9 + DOWN * 1.2, LEFT * 1.9 + UP * 1.05, color=INK, fill_color=PANEL, fill_opacity=1)
            self.play(Create(ramp), FadeIn(M(r"\frac{\text{height}}{\text{length}} = \frac12", 40).next_to(ramp, DOWN, buff=0.3)), run_time=1)
            self.play(FadeIn(M(r"\theta = \ ?", 40, SECANT).move_to(LEFT * 4.6 + DOWN * 0.95)), run_time=0.6)
            b.line(1)
            ans = M(r"\arcsin\tfrac12 = \tfrac{\pi}{6}", 50, SECANT).shift(RIGHT * 2.6 + UP * 2.4)
            self.play(Write(ans), run_time=1)
            b.line(2)
            ax, _ = plot_axes([-1.8, 1.8, 1], [-1.8, 1.8, 1], w=3.8, h=3.8, coords=False)
            ax.shift(RIGHT * 2.6 + DOWN * 0.9)
            self.play(FadeIn(ax), Create(ax.plot(np.sin, x_range=[-PI / 2, PI / 2], color=FUNC, stroke_width=4)),
                      Create(ax.plot(np.arcsin, x_range=[-0.999, 0.999], color=DERIV, stroke_width=4)),
                      Create(DashedLine(ax.c2p(-1.8, -1.8), ax.c2p(1.8, 1.8), color=DIM)), run_time=1.4)
        self.clear()
        self.title()

        with self.beat("Differentiate implicitly") as b:
            board = Board()
            board.anchor = UP * 3.0
            board.write(self, r"y = \arcsin x \ \Rightarrow\ \sin y = x")
            b.line(1)
            board.write(self, r"\cos y\,\frac{dy}{dx} = 1")
            b.line(2)
            board.write(self, r"\frac{dy}{dx} = \frac{1}{\cos y}")
            b.line(3)
            self.play(Indicate(board[-1], color=TANGENT), run_time=1)
        self.clear()

        with self.beat("The triangle") as b:
            base, opp, hyp, adj = triangle()
            VGroup(base, opp, hyp, adj).to_edge(LEFT, buff=1.2).shift(DOWN * 0.4)
            self.play(Create(base), run_time=1)
            b.line(1)
            self.play(FadeIn(opp), FadeIn(hyp), FadeIn(M(r"\sin y = \frac{x}{1}", 44).to_edge(RIGHT, buff=1.4).shift(UP * 2)), run_time=0.8)
            b.line(2)
            self.play(FadeIn(adj), run_time=0.8)
            b.line(3)
            c = M(r"\cos y = \sqrt{1 - x^2}", 44, DERIV).to_edge(RIGHT, buff=1.4).shift(UP * 0.6)
            self.play(Write(c), run_time=1)
            b.line(4)
            res = formula_box(M(r"\frac{d}{dx}\arcsin x = \frac{1}{\sqrt{1 - x^2}}", 48), DERIV).to_edge(RIGHT, buff=0.8).shift(DOWN * 1.4)
            self.play(FadeIn(res), run_time=1)
        self.clear()

        with self.beat("Arctangent") as b:
            board = Board()
            board.anchor = UP * 3.0
            board.write(self, r"y = \arctan x \ \Rightarrow\ \tan y = x")
            b.line(1)
            board.write(self, r"\sec^2 y\,\frac{dy}{dx} = 1")
            b.line(2)
            board.write(self, r"\sec^2 y = 1 + \tan^2 y = 1 + x^2")
            b.line(3)
            board.write(self, r"\frac{d}{dx}\arctan x = \frac{1}{1 + x^2}", color=DERIV)
        self.clear()

        with self.beat("The family") as b:
            rows = [(r"\arcsin x", r"\frac{1}{\sqrt{1 - x^2}}", r"\arccos x", r"-\frac{1}{\sqrt{1 - x^2}}"),
                    (r"\arctan x", r"\frac{1}{1 + x^2}", r"\operatorname{arccot} x", r"-\frac{1}{1 + x^2}"),
                    (r"\operatorname{arcsec} x", r"\frac{1}{|x|\sqrt{x^2 - 1}}", r"\operatorname{arccsc} x", r"-\frac{1}{|x|\sqrt{x^2 - 1}}")]
            grid = VGroup()
            for i, (a, da, c, dc) in enumerate(rows):
                big = 44 if i < 2 else 36
                grid.add(VGroup(M(a, big), M(r"\to", big, DIM), M(da, big, DERIV)).arrange(RIGHT, buff=0.25),
                         VGroup(M(c, big), M(r"\to", big, DIM), M(dc, big, TANGENT)).arrange(RIGHT, buff=0.25))
            grid.arrange_in_grid(3, 2, buff=(1.0, 0.5), col_alignments="ll")
            self.play(FadeIn(grid[0]), FadeIn(grid[2]), run_time=0.8)
            self.play(FadeIn(grid[1]), run_time=0.6)
            b.line(1)
            self.play(FadeIn(grid[3]), FadeIn(grid[4]), FadeIn(grid[5]), run_time=1)
            self.play(*[Indicate(grid[i][2], color=TANGENT) for i in (1, 3, 5)], run_time=1)
            b.line(2)
            ch = M(r"\frac{d}{dx}\arctan\big(u(x)\big) = \frac{u'(x)}{1 + u(x)^2}", 40, SECANT).to_edge(DOWN, buff=0.5)
            self.play(Write(ch), run_time=1.2)
        self.clear()
        self.example("Arcsine with the chain rule", r"Find $\dfrac{d}{dx}\arctan(3x)$ and $\dfrac{d}{dx}\arcsin\left(x^2\right)$.",
                     [r"u = 3x,\ u' = 3: \quad \frac{1}{1 + u^2}\cdot u' = \frac{3}{1 + 9x^2}", r"u = x^2,\ u' = 2x: \quad \frac{1}{\sqrt{1 - u^2}}\cdot u' = \frac{2x}{\sqrt{1 - x^4}}"], at=[1, 2])

        with self.beat("Close") as b:
            base, opp, hyp, adj = triangle(2.2)
            tg = VGroup(base, opp, hyp, adj).to_edge(LEFT, buff=1.2)
            fs = VGroup(M(r"\frac{d}{dx}\arcsin x = \frac{1}{\sqrt{1 - x^2}}", 44), M(r"\frac{d}{dx}\arctan x = \frac{1}{1 + x^2}", 44)).arrange(DOWN, buff=0.6).to_edge(RIGHT, buff=0.8)
            self.play(FadeIn(tg), FadeIn(fs), run_time=1.2)
        self.clear()

        self.examples_card()
        self.example("Example 1: A slope", r"Find the slope of $y = \arcsin x$ at $x = \frac12$.",
                     [r"\frac{1}{\sqrt{1 - \frac14}} = \frac{1}{\sqrt{\frac34}} = \frac{1}{\frac{\sqrt3}{2}}", r"= \frac{2}{\sqrt3}"], at=[1, 2])
        self.example("Example 2: The chain rule", r"Find $\dfrac{d}{dx}\arctan(3x)$.",
                     [r"\frac{1}{1 + (3x)^2} = \frac{1}{1 + 9x^2}", r"\cdot\ 3", r"\frac{d}{dx}\arctan(3x) = \frac{3}{1 + 9x^2}"], at=[1, 2, 3])
        a3, _ = plot_axes([-1, 3, 1], [-0.5, 1.5, 0.5], w=5.4, h=3.6)
        fig = VGroup(a3, a3.plot(np.arctan, x_range=[-1, 3], color=FUNC, stroke_width=4),
                     a3.plot(lambda x: PI / 4 + (x - 1) / 2, x_range=[-0.5, 2.5], color=TANGENT, stroke_width=4), closed_dot(a3, 1, PI / 4, INK))
        self.example("Example 3: A tangent line", r"Find the equation for the line tangent to $y = \arctan x$ at $x = 1$.",
                     [r"\arctan 1 = \frac{\pi}{4} \ \Rightarrow\ \left(1, \frac{\pi}{4}\right)", r"\frac{1}{1 + 1^2} = \frac12", r"y - \frac{\pi}{4} = \frac12(x - 1)"],
                     figure=fig, at=[1, 2, 3])
        self.finish()
