"""Topic 2.10: Derivatives of tan, cot, sec and csc. Narration comes from transcripts/2_10.md."""
import numpy as np
from manim import *

from kit import *
from style import *

SIX = [(r"\sin x", r"\cos x"), (r"\tan x", r"\sec^2 x"), (r"\sec x", r"\sec x\tan x"),
       (r"\cos x", r"-\sin x"), (r"\cot x", r"-\csc^2 x"), (r"\csc x", r"-\csc x\cot x")]


def six_table(filled=(0, 1, 2, 3, 4, 5), size=42):
    cells = VGroup()
    for i, (f, d) in enumerate(SIX):
        right = M(d, size, DERIV) if i in filled else M(r"?", size, DIM)
        cells.add(VGroup(M(f, size), M(r"\to", size, DIM), right).arrange(RIGHT, buff=0.3))
    cells.arrange_in_grid(2, 3, buff=(1.0, 0.8))
    return cells


class Lesson(TranscriptScene):
    NUM = "2.10"

    def construct(self):
        with self.beat("Four functions left") as b:
            tb = six_table(filled=(0, 3))
            self.play(FadeIn(tb), run_time=1)
            self.play(Indicate(tb[0][2], color=DERIV), Indicate(tb[3][2], color=DERIV), run_time=1)
            b.line(1)
            self.play(*[Indicate(tb[i][2], color=SECANT) for i in (1, 2, 4, 5)], run_time=1)
        self.clear()
        self.title()

        with self.beat("A quick review") as b:
            R, O = 2.0, LEFT * 4 + DOWN * 0.3
            th = 0.9
            circ = Circle(radius=R, color=DIM).move_to(O)
            P = O + R * np.array([np.cos(th), np.sin(th), 0])
            pts = VGroup(Line(O, P, color=INK), DashedLine(P, np.array([P[0], O[1], 0]), color=SECANT), DashedLine(np.array([P[0], O[1], 0]), O, color=DERIV), Dot(P, color=INK))
            labs = VGroup(M(r"\sin\theta", 32, SECANT).next_to(np.array([P[0], (P[1] + O[1]) / 2, 0]), RIGHT, buff=0.1),
                          M(r"\cos\theta", 32, DERIV).next_to(np.array([(P[0] + O[0]) / 2, O[1], 0]), DOWN, buff=0.15),
                          M(r"\theta", 30).move_to(O + 0.5 * np.array([np.cos(th / 2), np.sin(th / 2), 0])))
            self.play(Create(circ), Create(pts), FadeIn(labs), run_time=1.4)
            rows = VGroup(M(r"\tan\theta = \frac{\sin\theta}{\cos\theta}", 40), M(r"\cot\theta = \frac{\cos\theta}{\sin\theta}", 40),
                          M(r"\sec\theta = \frac{1}{\cos\theta}", 40), M(r"\csc\theta = \frac{1}{\sin\theta}", 40)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).to_edge(RIGHT, buff=1.4)
            b.line(1)
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), run_time=0.8)
            b.line(2)
            self.play(FadeIn(rows[2]), FadeIn(rows[3]), run_time=0.8)
            pair = VGroup(SurroundingRectangle(rows[2], color=DERIV, buff=0.1), SurroundingRectangle(rows[3], color=SECANT, buff=0.1))
            self.play(Create(pair), run_time=0.8)
            b.line(3)
            self.play(Indicate(rows, color=FUNC), run_time=0.8)
        self.clear()

        with self.beat("Tangent by the quotient rule") as b:
            board = Board()
            board.anchor = UP * 3.2
            board.write(self, r"\tan x = \frac{\sin x}{\cos x}")
            b.line(1)
            board.write(self, r"\frac{d}{dx}\tan x = \frac{\cos x \cdot \cos x - \sin x \cdot (-\sin x)}{\cos^2 x}")
            b.line(2)
            board.write(self, r"= \frac{\cos^2 x + \sin^2 x}{\cos^2 x}")
            b.line(3)
            board.write(self, r"= \frac{1}{\cos^2 x} = \sec^2 x", color=DERIV)
        self.clear()

        R, O = 2.0, LEFT * 4.6 + DOWN * 1.8
        th, dth = 0.6, 0.22
        pt = lambda a: O + R * np.array([1, np.tan(a), 0])
        with self.beat("A picture of the nudge") as b:
            circ = Circle(radius=R, color=DIM, stroke_width=3).move_to(O)
            vline = Line(O + R * RIGHT + DOWN * 0.6, O + R * RIGHT + UP * R * 1.5, color=FUNC, stroke_width=4)
            self.play(Create(circ), FadeIn(Line(O + LEFT * 0.4, O + RIGHT * (R + 0.6), color=DIM, stroke_width=2)), run_time=1)
            b.line(1)
            P = pt(th)
            ray = Line(O, P + (P - O) * 0.15, color=INK, stroke_width=4)
            self.play(Create(vline), FadeIn(M("x = 1", 30, FUNC).next_to(vline, DOWN, buff=0.1)), run_time=0.8)
            self.play(Create(ray), FadeIn(Dot(P, color=INK)), FadeIn(M(r"\theta", 32).move_to(O + 0.5 * np.array([np.cos(th / 2), np.sin(th / 2), 0]))), run_time=1)
            tanb = BraceBetweenPoints(O + R * RIGHT, P, RIGHT, color=SECANT)
            self.play(FadeIn(tanb), FadeIn(M(r"\tan\theta", 32, SECANT).next_to(tanb, RIGHT, buff=0.1)),
                      FadeIn(M(r"\sec\theta", 32, TANGENT).move_to((O + P) / 2 + np.array([-np.sin(th), np.cos(th), 0]) * 0.35)), run_time=1)
            b.line(2)
            Q = pt(th + dth)
            ray2 = Line(O, Q + (Q - O) * 0.1, color=DIM, stroke_width=3)
            self.play(Create(ray2), FadeIn(Dot(Q, color=TANGENT)), run_time=1)
            step = Line(P, Q, color=TANGENT, stroke_width=6)
            self.play(Create(step), run_time=0.6)
        with self.beat("Two stretches") as b:
            # the zoomed triangle: sweep (perpendicular to the ray, length sec*dth) and the vertical step that follows the line
            sec = 1 / np.cos(th)
            Z = RIGHT * 2.2 + DOWN * 1.0
            k = 2.0                                   # zoom factor for the inset (in units of R * dth)
            u = np.array([-np.sin(th), np.cos(th), 0])  # direction of the sweep
            sweep = Line(Z, Z + u * sec * k, color=SECANT, stroke_width=6)
            vert = Line(Z, Z + UP * sec * sec * k, color=TANGENT, stroke_width=6)
            join = DashedLine(sweep.get_end(), vert.get_end(), color=DIM)
            frame = SurroundingRectangle(VGroup(sweep, vert), color=DIM, buff=0.6)
            self.play(Create(frame), run_time=0.6)
            b.line(1)
            self.play(Create(sweep), FadeIn(M(r"\sec\theta\cdot d\theta", 32, SECANT).next_to(sweep.get_center(), LEFT, buff=0.2)), run_time=1)
            b.line(2)
            self.play(Create(vert), Create(join), run_time=1)
            ang = Angle(vert, sweep, radius=0.5, color=INK, other_angle=False)
            self.play(Create(ang), FadeIn(M(r"\theta", 30).next_to(ang, UP, buff=0.05)), run_time=0.6)
            b.line(3)
            lab = M(r"\frac{\sec\theta\,d\theta}{\cos\theta} = \sec^2\theta\,d\theta", 38, TANGENT).next_to(frame, UP, buff=0.3)
            self.play(Write(lab), run_time=1.2)
            b.line(4)
            lim = M(r"d\theta \to 0:\quad \frac{d(\tan\theta)}{d\theta} = \sec^2\theta", 44, DERIV).to_edge(UP, buff=0.3).shift(RIGHT * 1.5)
            self.play(Write(lim), FadeOut(lab), run_time=1.2)
        self.clear()

        with self.beat("Secant") as b:
            board = Board()
            board.anchor = UP * 3.0
            board.write(self, r"\sec x = \frac{1}{\cos x}")
            board.write(self, r"\frac{d}{dx}\sec x = \frac{\cos x \cdot 0 - 1 \cdot (-\sin x)}{\cos^2 x} = \frac{\sin x}{\cos^2 x}")
            b.line(1)
            board.write(self, r"= \frac{1}{\cos x}\cdot\frac{\sin x}{\cos x} = \sec x\tan x", color=DERIV)
        self.clear()

        with self.beat("The co-functions") as b:
            tb = six_table()
            self.play(FadeIn(tb[:3]), run_time=0.8)
            self.play(FadeIn(tb[3:]), run_time=0.8)
            b.line(1)
            self.play(*[Indicate(tb[i], color=SECANT, scale_factor=1.05) for i in (3, 4, 5)], run_time=1.2)
            b.line(2)
            for i in (3, 4, 5):
                self.play(Indicate(tb[i][2], color=TANGENT), run_time=0.6)
        self.clear()

        ax, al = plot_axes([0, 1.4, 0.5], [0, 4, 1], w=6, h=5)
        VGroup(ax, al).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        self.example("A product with tangent", r"Find $\dfrac{d}{dx}\left[x^2\tan x\right]$.",
                     [r"\underbrace{x^2}_{u}\,\underbrace{\tan x}_{v}", r"u' = 2x, \qquad v' = \sec^2 x", r"u'v + uv' = 2x\tan x + x^2\sec^2 x"], at=[1, 1, 2])
        fig = VGroup(ax, al, ax.plot(np.tan, x_range=[0, 1.32], color=FUNC, stroke_width=4), closed_dot(ax, PI / 4, 1, INK),
                     tangent_line(ax, np.tan, PI / 4, 2, [0.3, 1.3]))
        self.example("A tangent line", r"Find the equation for the line tangent to $y = \tan x$ at $x = \dfrac\pi4$.",
                     [r"\text{point: } \left(\tfrac{\pi}{4}, 1\right)", r"\text{slope: } \sec^2\tfrac{\pi}{4} = (\sqrt2)^2 = 2", r"y - 1 = 2\left(x - \tfrac{\pi}{4}\right)"],
                     figure=fig, at=[1, 2, 3])

        with self.beat("Close") as b:
            tb = six_table(size=38).shift(UP * 0.5)
            note = T(r"rewrite with sine and cosine", 36, SECANT).next_to(tb, DOWN, buff=0.7)
            self.play(FadeIn(tb), FadeIn(note), run_time=1.2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Sums and multiples", r"Find $\dfrac{dy}{dx}$ for $y = 3\tan x - 2\sec x + x^2$.",
                     [r"3\tan x \to 3\sec^2 x", r"-2\sec x \to -2\sec x\tan x", r"x^2 \to 2x", r"\frac{dy}{dx} = 3\sec^2 x - 2\sec x\tan x + 2x"], at=[1, 2, 3, 4])
        self.example("Example 2: A product with a trig factor", r"Find the derivative of $x^2\cot x$.",
                     [r"\underbrace{x^2}_{u}\,\underbrace{\cot x}_{v}:\quad u' = 2x, \quad v' = -\csc^2 x", r"u'v = 2x\cot x", r"uv' = x^2(-\csc^2 x)",
                      r"\frac{d}{dx}\big[x^2\cot x\big] = 2x\cot x - x^2\csc^2 x"], at=[1, 1, 2, 3])
        a3, _ = plot_axes([0, 1.4, 0.5], [0, 0.8, 0.2], w=5.4, h=3.8)
        top = PI / 2 - 1
        fig3 = VGroup(a3, a3.plot(lambda x: 2 * x - np.tan(x), x_range=[0, 1.1], color=FUNC, stroke_width=4),
                      Line(a3.c2p(PI / 4 - 0.3, top), a3.c2p(PI / 4 + 0.3, top), color=TANGENT, stroke_width=4), closed_dot(a3, PI / 4, top, INK))
        self.example("Example 3: Where is the slope a given value?", r"For $0 \le x < \frac{\pi}{2}$, where does $y = 2x - \tan x$ have a horizontal tangent?",
                     [r"\text{horizontal} \Rightarrow \text{when is } y' = 0\,?", r"y' = 2 - \sec^2 x = 0 \ \Rightarrow\ \sec^2 x = 2", r"\cos^2 x = \frac12, \quad \cos x = \frac{1}{\sqrt2}", r"x = \frac{\pi}{4}"],
                     figure=fig3, at=[1, 2, 3, 4])
        self.finish()
