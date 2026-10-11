"""Trig Review lesson 0.4 (T4): The six trigonometric functions of any angle. Narration comes from transcripts/0_4.md."""
import numpy as np
from manim import *

from kit import *
from style import *


# the point-on-the-terminal-side rule, stacked so the corner card stays readable during examples
POINT_REF = r"\begin{aligned}\sin\theta &= \tfrac{y}{r}\\ \cos\theta &= \tfrac{x}{r}\\ \tan\theta &= \tfrac{y}{x}\end{aligned}"


def point_axes(x, y, xr, yr, unit=0.32, label=None, r_label=None):
    """Small axes with the ray from the origin to (x, y), the point, its label, and the r on the ray."""
    ax, al = plot_axes([xr[0], xr[1], 1], [yr[0], yr[1], 1], w=unit * (xr[1] - xr[0]), h=unit * (yr[1] - yr[0]), coords=False)
    P, O = ax.c2p(x, y), ax.c2p(0, 0)
    g = VGroup(ax, al, Line(O, P, color=INK, stroke_width=4), Dot(P, color=FUNC),
               M(label or f"({x}, {y})", 28, FUNC).next_to(P, UP if y > 0 else DOWN, buff=0.15),
               Arc(radius=0.35, angle=np.arctan2(y, x) % TAU, arc_center=O, color=SECANT, stroke_width=3))
    if r_label:
        n = np.array([-y, x, 0]) / np.hypot(x, y)
        g.add(M(r_label, 26).move_to((O + P) / 2 + 0.3 * n))
    return g


class Lesson(TranscriptScene):
    NUM = "0.4"

    def construct(self):
        with self.beat("A point off the unit circle") as b:
            ax, al = plot_axes([-6, 6, 1], [-6, 6, 1], w=6.2, h=6.2, coords=False)
            ax.shift(LEFT * 2.8 + DOWN * 0.1)
            O, u = ax.c2p(0, 0), ax.x_axis.get_unit_size()
            unit = Circle(radius=u, color=INK, stroke_width=3).move_to(O)
            big = Circle(radius=5 * u, color=DIM, stroke_width=2).move_to(O)
            P = ax.c2p(-3, 4)
            self.play(FadeIn(ax), FadeIn(al), Create(unit), run_time=0.8)
            self.play(Create(big), Create(Line(O, ax.c2p(-3.6, 4.8), color=INK, stroke_width=3)), run_time=1)
            dot = Dot(P, color=FUNC)
            lab = M("(-3, 4)", 30, FUNC).next_to(P, LEFT, buff=0.15)
            self.play(FadeIn(dot), FadeIn(lab), FadeIn(M(r"r = 5", 30).move_to((O + P) / 2 + RIGHT * 0.45 + UP * 0.2)), run_time=0.8)
            b.line(1)
            Q = ax.c2p(-0.6, 0.8)
            self.play(dot.animate.move_to(Q), run_time=1.6)
            div = M(r"\div 5", 30, SECANT).next_to(Line(P, Q), LEFT, buff=0.1)
            newlab = M(r"\left(-\tfrac35,\ \tfrac45\right)", 30, FUNC).move_to(Q + RIGHT * 3.2 + UP * 1.4)
            self.play(FadeIn(div), FadeIn(newlab), Create(Arrow(newlab.get_left(), Q + RIGHT * 0.1, buff=0.15, color=FUNC, stroke_width=3)), run_time=1)
            b.line(2)
            self.play(FadeIn(VGroup(M(r"\cos\theta = -\tfrac35", 40, DERIV), M(r"\sin\theta = \tfrac45", 40, FUNC)).arrange(DOWN, buff=0.3).next_to(newlab, DOWN, buff=0.8)), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("Any angle, any point") as b:
            ax, al = plot_axes([-5, 5, 1], [-5, 5, 1], w=5.6, h=5.6, coords=False)
            ax.shift(LEFT * 3 + DOWN * 0.2)
            P, O = ax.c2p(-3, 4), ax.c2p(0, 0)
            self.play(FadeIn(ax), FadeIn(al), run_time=0.6)
            self.play(Create(Line(O, P, color=INK, stroke_width=4)), FadeIn(Dot(P, color=FUNC)), FadeIn(M("(x, y)", 32, FUNC).next_to(P, UL, buff=0.1)),
                      FadeIn(M("r", 32).move_to((O + P) / 2 + RIGHT * 0.3 + UP * 0.15)), Create(Arc(radius=0.5, angle=np.arctan2(4, -3), arc_center=O, color=SECANT)), run_time=1)
            self.play(FadeIn(M(r"r = \sqrt{x^2 + y^2}", 36).to_edge(RIGHT, buff=0.8).shift(UP * 2.6)), run_time=0.6)
            b.line(1)
            unit = Circle(radius=ax.x_axis.get_unit_size(), color=DIM, stroke_width=2).move_to(O)
            Q = ax.c2p(-0.6, 0.8)
            self.play(Create(unit), FadeIn(Dot(Q, color=SECANT)), FadeIn(M(r"\left(\tfrac{x}{r},\ \tfrac{y}{r}\right)", 28, SECANT).next_to(Q, LEFT, buff=0.2)), run_time=1)
            defs = VGroup(M(r"\sin\theta = \frac{y}{r}", 42, FUNC), M(r"\cos\theta = \frac{x}{r}", 42, DERIV), M(r"\tan\theta = \frac{y}{x}", 42, TANGENT)).arrange(RIGHT, buff=0.5).to_edge(RIGHT, buff=0.4).shift(UP * 1.5)
            self.play(Write(defs), run_time=1.2)
            b.line(2)
            tri = right_triangle(2.4, 1.8, opp=r"y\ (\text{opp})", adj=r"x\ (\text{adj})", hyp=r"r", angle=r"\theta", size=28).to_edge(RIGHT, buff=1.4).shift(DOWN * 2.1)
            self.play(FadeIn(tri), FadeIn(T("quadrant I: SOH CAH TOA", 30, ACCUM).next_to(tri, UP, buff=0.3)), run_time=1)
        self.clear()

        self.example_ref = POINT_REF
        self.example("A point on the terminal side", r"The point $(-5, 12)$ is on the terminal side of $\theta$. Find $\sin\theta$, $\cos\theta$, and $\tan\theta$.",
                     [r"r = \sqrt{25 + 144} = \sqrt{169} = 13", r"\sin\theta = \frac{y}{r} = \frac{12}{13}", r"\cos\theta = \frac{x}{r} = -\frac{5}{13}",
                      r"\tan\theta = \frac{y}{x} = \frac{12}{-5} = -\frac{12}{5}", r"TEXT:Quadrant II: sine positive, cosine negative."], at=[1, 2, 3, 4, 5],
                     figure=point_axes(-5, 12, (-7, 3), (-2, 13), label="(-5, 12)", r_label="13"), follow=True)

        with self.beat("The reciprocal functions") as b:
            cols = VGroup(*[VGroup(M(top, 44, c), M(bot, 38, c), T(name, 28, DIM)).arrange(DOWN, buff=0.3) for top, bot, name, c in
                            ((r"\sin\theta", r"\csc\theta = \frac{1}{\sin\theta}", "cosecant", FUNC), (r"\cos\theta", r"\sec\theta = \frac{1}{\cos\theta}", "secant", DERIV),
                             (r"\tan\theta", r"\cot\theta = \frac{1}{\tan\theta} = \frac{\cos\theta}{\sin\theta}", "cotangent", TANGENT))]).arrange(RIGHT, buff=0.9).to_edge(UP, buff=0.6)
            self.play(FadeIn(VGroup(*[c[0] for c in cols])), run_time=0.6)
            for c in cols:
                self.play(Write(c[1]), FadeIn(c[2]), run_time=0.8)
            b.line(1)
            rs = VGroup(*[M(t, 38, c).next_to(col, DOWN, buff=0.3) for t, c, col in ((r"= \frac{r}{y}", FUNC, cols[0]), (r"= \frac{r}{x}", DERIV, cols[1]), (r"= \frac{x}{y}", TANGENT, cols[2]))])
            self.play(FadeIn(rs), run_time=0.8)
            b.line(2)
            ex = M(r"(-5, 12),\ r = 13: \quad \csc\theta = \frac{13}{12}, \quad \sec\theta = -\frac{13}{5}, \quad \cot\theta = -\frac{5}{12}", 38).next_to(rs, DOWN, buff=0.6)
            self.play(Write(ex), run_time=1.2)
            b.line(3)
            self.play(FadeIn(M(r"\cos\frac{\pi}{3} = \frac12, \ \text{so} \ \sec\frac{\pi}{3} = 2", 40, ACCUM).next_to(ex, DOWN, buff=0.6)), run_time=0.8)
        self.clear()

        with self.beat("Where they are undefined") as b:
            uc = TrigCircle(r=2.4, center=LEFT * 3 + DOWN * 0.2)
            self.play(Create(uc), run_time=0.6)
            self.play(FadeIn(uc.dot(PI / 2, TANGENT)), FadeIn(uc.dot(3 * PI / 2, TANGENT)), FadeIn(M(r"\cos\theta = 0", 32, TANGENT).next_to(uc.pt(PI / 2), UR, buff=0.15)),
                      FadeIn(M(r"\tan\theta, \ \sec\theta \text{ undefined at } \tfrac{\pi}{2}, \tfrac{3\pi}{2}, \dots", 36, TANGENT).to_edge(RIGHT, buff=0.4).shift(UP * 1)), run_time=1)
            b.line(1)
            self.play(FadeIn(uc.dot(0, FUNC)), FadeIn(uc.dot(PI, FUNC)), FadeIn(M(r"\sin\theta = 0", 32, FUNC).next_to(uc.pt(PI), UP, buff=0.3)),
                      FadeIn(M(r"\cot\theta, \ \csc\theta \text{ undefined at } 0, \pi, 2\pi, \dots", 36, FUNC).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.6)), run_time=1)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(M(r"\text{point } (x, y),\ r = \sqrt{x^2 + y^2}: \ \sin\theta = \frac{y}{r}, \ \cos\theta = \frac{x}{r}, \ \tan\theta = \frac{y}{x}", 38, ACCUM),
                          M(r"\csc\theta = \frac{1}{\sin\theta} = \frac{r}{y}, \quad \sec\theta = \frac{1}{\cos\theta} = \frac{r}{x}, \quad \cot\theta = \frac{1}{\tan\theta} = \frac{x}{y}", 38),
                          T(r"$\tan$, $\sec$ undefined where $\cos\theta = 0$; $\cot$, $\csc$ where $\sin\theta = 0$", 32, DIM)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example_ref = r"\begin{aligned}\csc\theta &= \tfrac{1}{\sin\theta}\\ \sec\theta &= \tfrac{1}{\cos\theta}\\ \cot\theta &= \tfrac{1}{\tan\theta}\end{aligned}"
        self.example("Example 1: Reciprocals at landmark angles", r"Find $\sec\frac{5\pi}{4}$ and $\csc\frac{5\pi}{6}$.",
                     [r"\cos\frac{5\pi}{4} = -\frac{\sqrt2}{2}", r"\sec\frac{5\pi}{4} = \frac{1}{-\sqrt2/2} = -\frac{2}{\sqrt2} = -\sqrt2", r"\sin\frac{5\pi}{6} = \frac12", r"\csc\frac{5\pi}{6} = 2"], at=[1, 2, 3, 4])
        self.example_ref = POINT_REF
        self.example("Example 2: A point in quadrant IV", r"The point $(4, -3)$ is on the terminal side of $\theta$. Find $\csc\theta$, $\sec\theta$, and $\cot\theta$.",
                     [r"r = \sqrt{16 + 9} = 5", r"\csc\theta = \frac{r}{y} = \frac{5}{-3} = -\frac53", r"\sec\theta = \frac{r}{x} = \frac54", r"\cot\theta = \frac{x}{y} = \frac{4}{-3} = -\frac43"],
                     at=[1, 2, 3, 4], figure=point_axes(4, -3, (-2, 6), (-5, 3), unit=0.55, r_label="r"))
        ax, al = plot_axes([-3, 1, 1], [-3, 1, 1], w=3.6, h=3.6, coords=False)
        q3 = VGroup(ax, al, Line(ax.c2p(0, 0), ax.c2p(-1, -2), color=INK, stroke_width=4), Dot(ax.c2p(-1, -2), color=FUNC), M("(-1, -2)", 26, FUNC).next_to(ax.c2p(-1, -2), LEFT, buff=0.1),
                    M(r"\sqrt5", 26).move_to(ax.c2p(-0.2, -1.2)))
        self.example("Example 3: From tangent to the rest", r"$\tan\theta = 2$ and $\theta$ is in quadrant III. Find $\sin\theta$ and $\sec\theta$.",
                     [r"\tan\theta = \frac{y}{x} = \frac{-2}{-1}", r"\text{point } (-1, -2)", r"r = \sqrt{1 + 4} = \sqrt5", r"\sin\theta = \frac{y}{r} = -\frac{2}{\sqrt5} = -\frac{2\sqrt5}{5}",
                      r"\sec\theta = \frac{r}{x} = \frac{\sqrt5}{-1} = -\sqrt5"], at=[1, 1, 2, 3, 4], figure=q3, figure_at=1)
        self.example("Example 4: From cosine to the rest", r"$\cos\theta = -\frac{5}{13}$ and $\theta$ is in quadrant II. Find $\tan\theta$ and $\csc\theta$.",
                     [r"\cos\theta = \frac{x}{r} = \frac{-5}{13}", r"\text{point } (-5, y), \ r = 13", r"y^2 = 169 - 25 = 144", r"y = \pm 12; \ \text{quadrant II, so } y = 12",
                      r"\tan\theta = \frac{y}{x} = -\frac{12}{5}, \quad \csc\theta = \frac{r}{y} = \frac{13}{12}"], at=[1, 1, 2, 3, 4],
                     figure=point_axes(-5, 12, (-7, 3), (-2, 13), label="(-5, 12)", r_label="13"), figure_at=3)
        self.finish()
