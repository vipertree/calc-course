"""Topic 5.12: Behaviors of implicit relations. Narration comes from transcripts/5_12.md."""
import numpy as np
from manim import *

from kit import *
from style import *

R0 = -2.1038034  # the real root of x^3 - 3x + 3: where y = 0 on y^2 = x^3 - 3x + 3


def branches(ax, color=FUNC):
    g = lambda s: np.sqrt(max(s**3 - 3 * s + 3, 0))
    up = ax.plot(g, x_range=[R0, 2.2, 0.005], color=color, stroke_width=5)
    dn = ax.plot(lambda s: -g(s), x_range=[R0, 2.2, 0.005], color=color, stroke_width=5)
    return VGroup(up, dn)


class Lesson(TranscriptScene):
    NUM = "5.12"

    def construct(self):
        ax, al = plot_axes([-3, 3, 1], [-4, 4, 1], w=6.6, h=6, coords=False)
        VGroup(ax, al).to_edge(LEFT, buff=0.8).shift(DOWN * 0.1)
        with self.beat("A curve that isn't a function") as b:
            eq = M(r"y^2 = x^3 - 3x + 3", 46).to_edge(RIGHT, buff=0.8).shift(UP * 2.4)
            self.play(FadeIn(ax), FadeIn(al), Create(branches(ax)), Write(eq), run_time=1.6)
            two = VGroup(DashedLine(ax.c2p(0, -3.6), ax.c2p(0, 3.6), color=DIM), Dot(ax.c2p(0, np.sqrt(3)), color=SECANT), Dot(ax.c2p(0, -np.sqrt(3)), color=SECANT))
            self.play(Create(two), run_time=0.8)
            b.line(1)
            flats = VGroup(*[Line(ax.c2p(px - 0.5, py), ax.c2p(px + 0.5, py), color=TANGENT, stroke_width=5)
                             for px, py in ((1, 1), (1, -1), (-1, np.sqrt(5)), (-1, -np.sqrt(5)))])
            self.play(FadeOut(two), Create(flats), run_time=1.2)
            vert = Line(ax.c2p(R0, -0.9), ax.c2p(R0, 0.9), color=DERIV, stroke_width=5)
            self.play(Create(vert), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("Top and bottom of the slope") as b:
            frac = M(r"\frac{dy}{dx} = \frac{N}{D}", 64).shift(UP * 2)
            tags = VGroup(T("top", 30, DIM).next_to(frac, RIGHT, buff=0.3).shift(UP * 0.4), T("bottom", 30, DIM).next_to(frac, RIGHT, buff=0.3).shift(DOWN * 0.4))
            self.play(Write(frac), FadeIn(tags), run_time=1)
            b.line(1)
            c1 = VGroup(M(r"N = 0,\ D \ne 0", 40, TANGENT), Line(LEFT, RIGHT, color=TANGENT, stroke_width=6), T("horizontal tangent", 32)).arrange(DOWN, buff=0.4)
            c2 = VGroup(M(r"D = 0,\ N \ne 0", 40, DERIV), Line(DOWN * 0.8, UP * 0.8, color=DERIV, stroke_width=6), T("vertical tangent", 32)).arrange(DOWN, buff=0.3)
            VGroup(c1, c2).arrange(RIGHT, buff=2.2).shift(DOWN * 1)
            self.play(FadeIn(c1), run_time=0.8)
            b.line(2)
            self.play(FadeIn(c2), run_time=0.8)
        self.clear()

        ax, al = plot_axes([-6, 6, 2], [-6, 6, 2], w=5.6, h=5.6, coords=False)
        VGroup(ax, al).to_edge(LEFT, buff=1).shift(DOWN * 0.1)
        with self.beat("Back to the curve") as b:
            circ = Circle(radius=ax.c2p(5, 0)[0] - ax.c2p(0, 0)[0], color=FUNC, stroke_width=5).move_to(ax.c2p(0, 0))
            self.play(FadeIn(ax), FadeIn(al), Create(circ), run_time=1)
            note = VGroup(M(r"\frac{dy}{dx} = -\frac{x}{y}", 44), M(r"\text{top} = 0:\ x = 0", 40, SECANT)).arrange(DOWN, buff=0.4).to_edge(RIGHT, buff=1).shift(UP * 1)
            line = DashedLine(ax.c2p(0, -6), ax.c2p(0, 6), color=SECANT)
            self.play(FadeIn(note), Create(line), run_time=1)
            b.line(1)
            pts = VGroup(Dot(ax.c2p(0, 5), color=TANGENT, radius=0.1), Dot(ax.c2p(0, -5), color=TANGENT, radius=0.1))
            lab = M(r"(0, 5),\ (0, -5)", 40, TANGENT).next_to(note, DOWN, buff=0.6)
            self.play(FadeIn(pts), FadeIn(lab), run_time=0.8)
        self.clear()

        with self.beat("Concavity") as b:
            l1 = T(r"$\dfrac{d^2y}{dx^2}$: differentiate $\dfrac{dy}{dx}$ again, then substitute $\dfrac{dy}{dx}$.", 40).shift(UP * 1.2)
            self.play(FadeIn(l1), run_time=0.8)
            b.line(1)
            l2 = VGroup(M(r"\frac{dy}{dx} = 0,\ \frac{d^2y}{dx^2} > 0:\ \text{relative minimum}", 42, DERIV),
                        M(r"\frac{dy}{dx} = 0,\ \frac{d^2y}{dx^2} < 0:\ \text{relative maximum}", 42, TANGENT)).arrange(DOWN, buff=0.4).shift(DOWN * 1)
            self.play(FadeIn(l2), run_time=0.8)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(M(r"\text{Horizontal: top} = 0", 46, TANGENT), M(r"\text{Vertical: bottom} = 0", 46, DERIV), T("Then solve with the curve's equation.", 40, SECANT)).arrange(DOWN, buff=0.5)
            self.play(FadeIn(card), run_time=1)
        self.clear()

        self.examples_card()
        self.example("Example 1: A shifted circle",
                     r"Find the points on $x^2 + y^2 - 4x + 6y = 12$ where the tangent is horizontal, and where it is vertical.",
                     [r"2x + 2yy' - 4 + 6y' = 0,\ \ y' = \frac{2 - x}{y + 3}", r"\text{horizontal: } x = 2,\ \ y^2 + 6y - 16 = 0", r"(2, 2),\ (2, -8)",
                      r"\text{vertical: } y = -3,\ \ x^2 - 4x - 21 = 0:\ (7, -3),\ (-3, -3)"], at=[1, 2, 3, 4])
        self.example("Example 2: A cubic curve", r"Find the points on $y^2 = x^3 - 3x + 3$ where the tangent is horizontal.",
                     [r"2yy' = 3x^2 - 3,\ \ y' = \frac{3x^2 - 3}{2y}", r"\text{top} = 0 \text{ at } x = \pm 1", r"x = 1:\ y^2 = 1:\ (1, 1),\ (1, -1)",
                      r"x = -1:\ y^2 = 5:\ \left(-1, \sqrt5\right),\ \left(-1, -\sqrt5\right)"], at=[1, 2, 3, 4])
        self.example("Example 3: Which way it bends",
                     r"On $y^2 = x^3 - 3x + 3$, find $\dfrac{d^2y}{dx^2}$ at $(1, 1)$. What does the curve have there?",
                     [r"2(y')^2 + 2y\,y'' = 6x", r"(1, 1):\ y' = 0,\ \ 2y'' = 6,\ \ y'' = 3 > 0", r"\text{horizontal tangent, concave up: relative minimum}"], at=[1, 2, 3])
        self.finish()
