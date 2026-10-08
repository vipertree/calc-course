"""Topic 0.7: Inverse trigonometric functions. Narration comes from transcripts/0_7.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def ramp_scene():
    """A wheelchair ramp (rise 1, run 12, drawn steeper so it reads) up to a door."""
    g = -1.8
    A, B = LEFT * 5 + UP * g, RIGHT * 1.5 + UP * g
    C = B + UP * 1.1
    ramp = Polygon(A, B, C, stroke_color=INK, stroke_width=3, fill_color="#B8B2A7", fill_opacity=1)
    rail = VGroup(Line(A + UP * 0.55, C + UP * 0.55, color=DIM, stroke_width=4), *[Line(A + s * (C - A), A + s * (C - A) + UP * 0.55, color=DIM, stroke_width=3) for s in (0.05, 0.35, 0.65, 0.95)])
    wall = Rectangle(width=2.6, height=3.6, stroke_color=INK, stroke_width=3, fill_color="#D9C7A7", fill_opacity=1).move_to(B + RIGHT * 1.3 + UP * 1.8)
    door = Rectangle(width=0.9, height=1.7, stroke_color=INK, stroke_width=3, fill_color="#7A4E2D", fill_opacity=1).move_to(C + RIGHT * 0.65 + UP * 0.85)
    ground = Line(LEFT * 6 + UP * g, RIGHT * 4.5 + UP * g, color=SAND, stroke_width=6)
    labs = VGroup(M(r"12 \text{ ft}", 30).next_to(Line(A, B), DOWN, buff=0.2), M(r"1 \text{ ft}", 30, FUNC).next_to(Line(B, C), LEFT, buff=0.12),
                  Arc(radius=1.2, angle=np.arctan2(1.1, 6.5), arc_center=A, color=SECANT, stroke_width=4), M(r"\theta", 30, SECANT).move_to(A + RIGHT * 1.55 + UP * 0.12))
    return VGroup(ground, wall, door, ramp, rail, labs)


def triangle_for(opp, adj, hyp, a, b):
    return right_triangle(a, b, opp=opp, adj=adj, hyp=hyp, angle=r"\theta", size=30)


class Lesson(TranscriptScene):
    NUM = "0.7"

    def construct(self):
        with self.beat("Working backward") as b:
            sc = ramp_scene()
            self.play(FadeIn(sc[:5]), run_time=1)
            self.play(FadeIn(sc[5]), run_time=0.8)
            b.line(1)
            self.play(Write(M(r"\tan\theta = \frac{1}{12}", 46, TANGENT).to_corner(UL, buff=0.7)), run_time=0.8)
            self.play(FadeIn(M(r"\theta = \ ?", 46, SECANT).to_corner(UL, buff=0.7).shift(DOWN * 1.3)), run_time=0.6)
            b.line(2)
            self.play(FadeIn(T("ratio $\\to$ angle: inverse trig", 36, ACCUM).to_edge(UP, buff=0.6).shift(RIGHT * 2)), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("Why the domain is restricted") as b:
            ax, labs = pi_axes(-2, 2, [-1.5, 1.5, 1], w=11, h=3.6)
            VGroup(ax, labs).shift(DOWN * 0.4)
            full = ax.plot(np.sin, x_range=[-2 * PI, 2 * PI], color=FUNC, stroke_width=4)
            self.play(FadeIn(ax), FadeIn(labs), Create(full), run_time=1.2)
            self.play(Create(DashedLine(ax.c2p(-2 * PI, 0.5), ax.c2p(2 * PI, 0.5), color=SECANT)),
                      *[FadeIn(Dot(ax.c2p(v, 0.5), color=SECANT)) for v in (-11 * PI / 6, -7 * PI / 6, PI / 6, 5 * PI / 6)], run_time=1)
            b.line(1)
            piece = ax.plot(np.sin, x_range=[-PI / 2, PI / 2], color=DERIV, stroke_width=8)
            self.play(full.animate.set_opacity(0.2), Create(piece), run_time=1.2)
            self.play(FadeIn(M(r"-\tfrac{\pi}{2} \le x \le \tfrac{\pi}{2}", 36, DERIV).to_edge(UP, buff=0.6)), run_time=0.6)
            b.line(2)
            self.play(Indicate(Dot(ax.c2p(PI / 6, 0.5), color=SECANT, radius=0.13)), run_time=1)
        self.clear()

        with self.beat("Arcsine") as b:
            card = formula_box(VGroup(M(r"\arcsin x = \text{the angle } \theta \text{ in } \left[-\tfrac{\pi}{2}, \tfrac{\pi}{2}\right] \text{ with } \sin\theta = x", 38)), DERIV).to_edge(UP, buff=0.5)
            self.play(FadeIn(card), run_time=1)
            b.line(1)
            io = VGroup(M(r"\text{inputs: } -1 \le x \le 1", 36), M(r"\text{outputs: } -\tfrac{\pi}{2} \le \theta \le \tfrac{\pi}{2}", 36, DERIV)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
            uc = TrigCircle(r=1.3, center=LEFT * 4.2 + DOWN * 2.3, ticks=False)
            self.play(FadeIn(io), run_time=0.8)
            self.play(Create(uc), Create(uc.arc(-PI / 2, PI / 2, DERIV)), run_time=0.8)
            b.line(2)
            ax, _ = plot_axes([-1.8, 1.8, 1], [-1.8, 1.8, 1], w=4.6, h=4.6, coords=False)
            ax.to_edge(RIGHT, buff=0.8).shift(DOWN * 0.8)
            self.play(FadeIn(ax), Create(DashedLine(ax.c2p(-1.8, -1.8), ax.c2p(1.8, 1.8), color=DIM)),
                      Create(ax.plot(np.sin, x_range=[-PI / 2, PI / 2], color=FUNC, stroke_width=4)), run_time=1)
            self.play(Create(ax.plot(np.arcsin, x_range=[-0.999, 0.999], color=DERIV, stroke_width=5)), FadeIn(M(r"y = \arcsin x", 30, DERIV).next_to(ax.c2p(1, PI / 2), LEFT, buff=0.2)), run_time=1.2)
        self.clear()

        with self.beat("Arccosine and arctangent") as b:
            uc = TrigCircle(r=1.4, center=LEFT * 4.6 + UP * 1.2, ticks=False)
            self.play(Create(uc), Create(uc.arc(0, PI, ACCUM)), FadeIn(M(r"\arccos x \in [0, \pi]", 36, ACCUM).next_to(uc, RIGHT, buff=0.5)), run_time=1)
            b.line(1)
            ax, _ = plot_axes([-4, 4, 1], [-2, 2, 1], w=6.6, h=3.2, coords=False)
            ax.to_edge(DOWN, buff=0.5).to_edge(RIGHT, buff=0.6)
            self.play(FadeIn(ax), Create(ax.plot(np.arctan, x_range=[-4, 4], color=TANGENT, stroke_width=5)), FadeIn(M(r"\arctan x \in \left(-\tfrac{\pi}{2}, \tfrac{\pi}{2}\right)", 36, TANGENT).to_edge(RIGHT, buff=0.6).shift(UP * 1.6)), run_time=1.2)
            b.line(2)
            self.play(Create(DashedLine(ax.c2p(-4, PI / 2), ax.c2p(4, PI / 2), color=DIM)), Create(DashedLine(ax.c2p(-4, -PI / 2), ax.c2p(4, -PI / 2), color=DIM)),
                      FadeIn(M(r"y = \tfrac{\pi}{2}", 26, DIM).next_to(ax.c2p(-4, PI / 2), UP, buff=0.08)), FadeIn(M(r"y = -\tfrac{\pi}{2}", 26, DIM).next_to(ax.c2p(4, -PI / 2), DOWN, buff=0.08)), run_time=1)
            tab = table([r"\text{function}", r"\text{inputs}", r"\text{outputs}"], [[r"\arcsin", "[-1, 1]", r"\left[-\tfrac{\pi}{2}, \tfrac{\pi}{2}\right]"], [r"\arccos", "[-1, 1]", r"[0, \pi]"],
                                                                     [r"\arctan", r"\text{all reals}", r"\left(-\tfrac{\pi}{2}, \tfrac{\pi}{2}\right)"]], size=30).to_edge(LEFT, buff=0.5).shift(DOWN * 1.9)
            self.play(FadeIn(tab), run_time=0.8)
        self.clear()

        uc = TrigCircle(r=1.9)
        evfig = VGroup(uc, uc.ray(-PI / 6, DERIV), uc.dot(-PI / 6, DERIV), uc.coord(-PI / 6, r"-\tfrac{\pi}{6}", DERIV, 28, 0.4),
                       uc.ray(2 * PI / 3, ACCUM), uc.dot(2 * PI / 3, ACCUM), uc.coord(2 * PI / 3, r"\tfrac{2\pi}{3}", ACCUM, 28, 0.4),
                       uc.ray(PI / 3, TANGENT), uc.dot(PI / 3, TANGENT), uc.coord(PI / 3, r"\tfrac{\pi}{3}", TANGENT, 28, 0.4))
        self.example("Evaluating inverse trig functions", r"Find $\arcsin\left(-\frac12\right)$, $\arccos\left(-\frac12\right)$, and $\arctan\sqrt3$.",
                     [r"\arcsin\left(-\tfrac12\right): \ \theta \in \left[-\tfrac{\pi}{2}, \tfrac{\pi}{2}\right], \ \sin\theta = -\tfrac12", r"= -\frac{\pi}{6}",
                      r"\arccos\left(-\tfrac12\right): \ \theta \in [0, \pi], \text{ reference angle } \tfrac{\pi}{3}, \text{ quadrant II}", r"= \pi - \frac{\pi}{3} = \frac{2\pi}{3}",
                      r"\arctan\sqrt3 = \frac{\pi}{3}"], at=[1, 2, 3, 4, 5], figure=evfig, figure_at=2, follow=True)

        with self.beat("Notation") as b:
            big = M(r"\sin^{-1} x = \arcsin x", 64, DERIV).shift(UP * 1.4)
            self.play(Write(big), run_time=1)
            b.line(1)
            wrong = M(r"\sin^{-1} x \ne \frac{1}{\sin x}", 52, TANGENT).next_to(big, DOWN, buff=0.7)
            self.play(Write(wrong), run_time=0.8)
            self.play(FadeIn(M(r"\frac{1}{\sin x} = \csc x = (\sin x)^{-1}", 44).next_to(wrong, DOWN, buff=0.6)), run_time=0.8)
        self.clear()

        with self.beat("Undoing, within limits") as b:
            r1 = M(r"\sin(\arcsin x) = x \quad \text{for } -1 \le x \le 1", 44, DERIV).to_edge(UP, buff=0.6)
            self.play(Write(r1), run_time=1)
            b.line(1)
            uc = TrigCircle(r=2.0, center=LEFT * 3.6 + DOWN * 1.0)
            self.play(Create(uc), Create(uc.arc(-PI / 2, PI / 2, DERIV, 7)), run_time=0.8)
            self.play(Create(uc.ray(5 * PI / 6, FUNC)), FadeIn(uc.dot(5 * PI / 6)), FadeIn(uc.coord(5 * PI / 6, r"\tfrac{5\pi}{6}", FUNC, 28, 0.4)), run_time=0.8)
            self.play(Create(DashedLine(uc.pt(5 * PI / 6), uc.pt(PI / 6), color=SECANT)), FadeIn(uc.dot(PI / 6, DERIV)), FadeIn(uc.coord(PI / 6, r"\tfrac{\pi}{6}", DERIV, 28, 0.4)), run_time=0.8)
            steps = VGroup(M(r"\sin\tfrac{5\pi}{6} = \tfrac12", 40), M(r"\arcsin\tfrac12 = \tfrac{\pi}{6}", 40, DERIV)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).to_edge(RIGHT, buff=1).shift(UP * 0.4)
            self.play(Write(steps), run_time=1)
            b.line(2)
            self.play(FadeIn(formula_box(M(r"\arcsin\left(\sin\tfrac{5\pi}{6}\right) = \tfrac{\pi}{6}, \ \text{not } \tfrac{5\pi}{6}", 38, SECANT), SECANT).next_to(steps, DOWN, buff=0.6)), run_time=0.8)
        self.clear()

        with self.beat("Close") as b:
            tab = table([r"\text{function}", r"\text{inputs}", r"\text{outputs}"], [[r"\arcsin", "[-1, 1]", r"\left[-\tfrac{\pi}{2}, \tfrac{\pi}{2}\right]"], [r"\arccos", "[-1, 1]", r"[0, \pi]"],
                                                                     [r"\arctan", r"\text{all reals}", r"\left(-\tfrac{\pi}{2}, \tfrac{\pi}{2}\right)"]], size=40).shift(UP * 0.6)
            note = M(r"\sin^{-1} x \text{ means } \arcsin x, \text{ not } \frac{1}{\sin x}", 40, TANGENT).next_to(tab, DOWN, buff=0.8)
            self.play(FadeIn(tab), run_time=1)
            self.play(FadeIn(note), run_time=0.8)
        self.clear()

        self.examples_card()
        self.example("Example 1: Two more values", r"Find $\arctan(-1)$ and $\arccos\left(-\frac{\sqrt2}{2}\right)$.",
                     [r"\tan\left(-\tfrac{\pi}{4}\right) = -1, \ \ -\tfrac{\pi}{4} \in \left(-\tfrac{\pi}{2}, \tfrac{\pi}{2}\right)", r"\arctan(-1) = -\frac{\pi}{4}",
                      r"\text{reference angle } \tfrac{\pi}{4}, \text{ quadrant II}", r"\arccos\left(-\tfrac{\sqrt2}{2}\right) = \pi - \frac{\pi}{4} = \frac{3\pi}{4}"], at=[1, 2, 3, 4])
        self.example("Example 2: A triangle for a composition", r"Find $\cos\left(\arcsin\frac23\right)$.",
                     [r"\theta = \arcsin\tfrac23: \ \sin\theta = \tfrac23, \ \theta \text{ in quadrant I}", r"\text{adjacent} = \sqrt{9 - 4} = \sqrt5", r"\cos\theta > 0",
                      r"\cos\theta = \frac{\text{adj}}{\text{hyp}} = \frac{\sqrt5}{3}"], at=[1, 2, 3, 4], figure=triangle_for("2", r"\sqrt5", "3", 2.6, 2.33), figure_at=2)
        self.example("Example 3: A composition in terms of x", r"Write $\tan(\arccos x)$ as an algebraic expression, for $0 < x \le 1$.",
                     [r"\theta = \arccos x: \ \cos\theta = \frac{x}{1}", r"\text{opposite} = \sqrt{1 - x^2}", r"\tan\theta = \frac{\text{opp}}{\text{adj}}", r"\tan(\arccos x) = \frac{\sqrt{1 - x^2}}{x}"],
                     at=[1, 2, 3, 4], figure=triangle_for(r"\sqrt{1 - x^2}", "x", "1", 2.0, 2.6), figure_at=1)
        self.example("Example 4: Solving with a calculator", r"Solve $3\sin x = 1$ for $0 \le x < 2\pi$, to three decimal places.",
                     [r"\sin x = \frac13", r"\arcsin\tfrac13 \approx 0.340 \quad \text{(radian mode)}", r"\sin > 0 \text{ in quadrants I and II}", r"x \approx \pi - 0.340",
                      r"x \approx 0.340 \ \text{ or } \ x \approx 2.802"], at=[1, 1, 2, 3, 4])
        self.finish()
