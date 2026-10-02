"""Topic 5.11: Solving optimization problems. Narration comes from transcripts/5_11.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "5.11"

    def sheet(self, X, center, k=0.3):
        """The 12 x 12 sheet with corner squares of side X (inches) cut out, drawn k units per inch, plus the folded box in an oblique view beside it."""
        def draw():
            x = X.get_value()
            s = 12 * k
            c = x * k
            outline = VMobject(color=INK, stroke_width=3).set_points_as_corners([
                [-s / 2 + c, s / 2, 0], [s / 2 - c, s / 2, 0], [s / 2 - c, s / 2 - c, 0], [s / 2, s / 2 - c, 0], [s / 2, -s / 2 + c, 0], [s / 2 - c, -s / 2 + c, 0],
                [s / 2 - c, -s / 2, 0], [-s / 2 + c, -s / 2, 0], [-s / 2 + c, -s / 2 + c, 0], [-s / 2, -s / 2 + c, 0], [-s / 2, s / 2 - c, 0], [-s / 2 + c, s / 2 - c, 0],
                [-s / 2 + c, s / 2, 0]]).shift(center)
            base = Square(side_length=s - 2 * c, stroke_width=0, fill_color=FUNC, fill_opacity=0.35).move_to(center)
            folds = DashedVMobject(Square(side_length=max(s - 2 * c, 0.01), color=DIM, stroke_width=2), num_dashes=24).move_to(center)
            return VGroup(base, folds, outline)
        return always_redraw(draw)

    def box(self, X, center, k=0.22):
        def draw():
            x = X.get_value()
            w, h = (12 - 2 * x) * k, x * k
            d = np.array([0.45, 0.3, 0]) * w
            p = center + DOWN * h / 2 + LEFT * (w + d[0]) / 2
            front = Polygon(p, p + RIGHT * w, p + RIGHT * w + UP * h, p + UP * h, color=SECANT, fill_color=FUNC, fill_opacity=0.35, stroke_width=3)
            side = Polygon(p + RIGHT * w, p + RIGHT * w + d, p + RIGHT * w + d + UP * h, p + RIGHT * w + UP * h, color=SECANT, fill_color=FUNC, fill_opacity=0.2, stroke_width=3)
            back = VGroup(Line(p + UP * h, p + UP * h + d, color=SECANT), Line(p + UP * h + d, p + RIGHT * w + UP * h + d, color=SECANT))
            return VGroup(front, side, back)
        return always_redraw(draw)

    def construct(self):
        X = ValueTracker(0.5)
        sh = self.sheet(X, LEFT * 4)
        bx = self.box(X, RIGHT * 1.2 + DOWN * 0.2)
        V = lambda x: x * (12 - 2 * x)**2
        read = always_redraw(lambda: VGroup(M(rf"x = {X.get_value():.1f}\ \text{{in}}", 36, DIM), M(rf"V = {V(X.get_value()):.0f}\ \text{{in}}^3", 40, FUNC))
                             .arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.6).shift(UP * 1.5))
        with self.beat("Folding a box") as b:
            self.add(sh, bx)
            self.play(FadeIn(read), run_time=0.6)
            self.play(X.animate.set_value(2), run_time=1.6)
            b.line(1)
            self.play(X.animate.set_value(0.4), run_time=1.6)
            self.play(X.animate.set_value(5), run_time=2.2)
            b.line(2)
            self.play(X.animate.set_value(2), run_time=2)
        self.clear()
        self.title()

        with self.beat("The whole procedure") as b:
            steps = VGroup(T("1. Draw, label, name the quantity.", 40), T("2. One variable and a domain.", 40), T("3. Critical points.", 40),
                           T("4. Justify: absolute max or min.", 40), T("5. Answer the question, with units.", 40)).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
            self.play(FadeIn(steps[0], shift=RIGHT * 0.2), run_time=0.6)
            b.line(1)
            self.play(FadeIn(steps[1], shift=RIGHT * 0.2), run_time=0.6)
            b.line(2)
            self.play(FadeIn(steps[2], shift=RIGHT * 0.2), run_time=0.6)
            self.play(FadeIn(steps[3], shift=RIGHT * 0.2), run_time=0.6)
            b.line(3)
            self.play(FadeIn(steps[4], shift=RIGHT * 0.2), run_time=0.6)
        self.clear()

        with self.beat("Justifying the answer") as b:
            def card(title, body, color):
                t = VGroup(T(title, 38, color), T(body, 32)).arrange(DOWN, buff=0.3)
                return VGroup(RoundedRectangle(width=6, height=2.6, corner_radius=0.15, color=color), t)
            c1 = card("Closed interval", r"compare the candidates: \\ critical points and endpoints", DERIV)
            c2 = card("Open interval", r"one critical point that's a \\ relative extremum: it's absolute", TANGENT)
            VGroup(c1, c2).arrange(RIGHT, buff=0.5)
            self.play(FadeIn(c1), run_time=0.8)
            b.line(1)
            self.play(FadeIn(c2), run_time=0.8)
        self.clear()
        self.example("Closest point", r"Find the point on the line $y = x + 1$ closest to $(3, 0)$.",
                     [r"D^2 = (x - 3)^2 + (x + 1)^2", r"\frac{d}{dx}D^2 = 2(x - 3) + 2(x + 1) = 4x - 4 = 0 \text{ at } x = 1", r"(1, 2), \quad D = \sqrt{4 + 4} = 2\sqrt2"], at=[1, 2, 3])

        with self.beat("Close") as b:
            X2 = ValueTracker(2)
            bx2 = self.box(X2, UP * 0.4)
            self.add(bx2)
            self.play(FadeIn(M(r"x = 2\ \text{in},\ \ V = 128\ \text{in}^3", 44, FUNC).shift(DOWN * 2)), run_time=0.8)
        self.clear()

        self.examples_card()
        self.example("Example 1: The open box",
                     r"An open box is made from a $12 \times 12$ inch sheet by cutting squares of side $x$ from the corners. What $x$ gives the largest volume, and what is that volume?",
                     [r"V(x) = x(12 - 2x)^2,\ \ 0 \le x \le 6", r"V'(x) = (12 - 2x)(12 - 6x) = 0 \text{ at } x = 2,\ 6", r"V(0) = 0,\ \ V(2) = 128,\ \ V(6) = 0",
                      r"x = 2 \text{ in},\ \ V = 128\ \text{in}^3"], at=[1, 2, 3, 4])
        self.example("Example 2: The closest point", r"Find the point on $y = \sqrt{x}$ closest to $(3, 0)$.",
                     [r"D^2 = (x - 3)^2 + \left(\sqrt x\right)^2 = x^2 - 5x + 9", r"\frac{d}{dx}D^2 = 2x - 5 = 0 \text{ at } x = \frac52",
                      r"\text{second derivative } 2 > 0,\ \text{only critical point: minimum}", r"\left(\frac52, \sqrt{\frac52}\right),\ \ D = \frac{\sqrt{11}}{2}"], at=[1, 2, 3, 4])
        self.example("Example 3: The can", r"A closed cylindrical can holds $16\pi$ in$^3$. What radius and height use the least material?",
                     [r"\pi r^2 h = 16\pi \ \Rightarrow\ h = \frac{16}{r^2}", r"S = 2\pi r^2 + 2\pi r h = 2\pi r^2 + \frac{32\pi}{r}",
                      r"S' = 4\pi r - \frac{32\pi}{r^2} = 0 \text{ at } r^3 = 8,\ r = 2", r"S'' > 0,\ \text{only critical point: } r = 2 \text{ in},\ h = 4 \text{ in}"], at=[1, 2, 3, 4])
        self.finish()
