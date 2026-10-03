"""Topic 0.3: The six trigonometric functions. Narration comes from transcripts/0_3.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def tree(height=3.2):
    """A leafy tree (vector art); the base of the trunk is at the group's bottom center."""
    trunk = Polygon([-0.14, 0, 0], [0.14, 0, 0], [0.09, height * 0.55, 0], [-0.09, height * 0.55, 0], stroke_width=0, fill_color="#8B5A2B", fill_opacity=1)
    greens = ["#3E7C3A", "#4E9A45", "#5DAF52"]
    crown = VGroup(*[Circle(radius=r, stroke_width=0, fill_color=greens[k % 3], fill_opacity=1).move_to([dx, height * 0.55 + dy, 0])
                     for k, (r, dx, dy) in enumerate(((0.75, 0, 0.55), (0.6, -0.55, 0.3), (0.6, 0.55, 0.3), (0.55, 0, 0.95), (0.45, -0.35, 0.85), (0.45, 0.35, 0.85)))])
    return VGroup(trunk, crown)


def surveyor_scene(d=6.0, ang=35):
    """Ground, a tree, a sighting tripod d units away, the right triangle with the 35 degree angle."""
    g = -2.6
    T0 = np.array([3.0, g, 0])
    tr = tree(3.4).move_to(T0, aligned_edge=DOWN)
    top = np.array([T0[0], g + d * np.tan(np.radians(ang)), 0])
    S = T0 + LEFT * d
    ground = Line(LEFT * 6.3 + UP * g, RIGHT * 5.5 + UP * g, color=SAND, stroke_width=6)
    tripod = Line(S, S + 0.45 * np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang)), 0]), color=INK, stroke_width=8)   # the sighting tube
    tri = Polygon(S, T0, top, stroke_color=SECANT, stroke_width=3)
    sight = DashedLine(S, top, color=SECANT)
    arc = Arc(radius=0.8, angle=np.radians(ang), arc_center=S, color=SECANT, stroke_width=4)
    labs = VGroup(M(r"20 \text{ m}", 30).next_to(Line(S, T0), DOWN, buff=0.2), M(f"{ang}^\\circ", 30, SECANT).move_to(S + 1.2 * np.array([np.cos(np.radians(ang / 2)), np.sin(np.radians(ang / 2)), 0])),
                  M("h", 34, FUNC).next_to(Line(T0, top), RIGHT, buff=0.15))
    return VGroup(ground, tr, tripod, tri, sight, arc, labs)


def ladder_scene():
    """A ladder at 70 degrees against a brick wall."""
    g, L, a = -2.4, 4.6, np.radians(70)
    W = np.array([1.6, g, 0])
    foot = W + LEFT * L * np.cos(a)
    topp = W + UP * L * np.sin(a)
    bricks = VGroup(*[Rectangle(width=0.7, height=0.3, stroke_color="#7A3B2E", stroke_width=1.5, fill_color="#B5543C", fill_opacity=1)
                      .move_to(W + RIGHT * (0.35 + 0.7 * c + 0.35 * (r % 2)) + UP * (0.15 + 0.3 * r)) for r in range(16) for c in range(2)])
    rails = VGroup(Line(foot, topp, color="#C9A227", stroke_width=6), Line(foot + LEFT * 0.25, topp + LEFT * 0.25, color="#C9A227", stroke_width=6))
    rungs = VGroup(*[Line(foot + s * (topp - foot), foot + s * (topp - foot) + LEFT * 0.25, color="#C9A227", stroke_width=4) for s in np.linspace(0.08, 0.95, 10)])
    ground = Line(W + LEFT * 3.2, W + RIGHT * 1.8, color=SAND, stroke_width=6)
    labs = VGroup(M(r"6 \text{ m}", 28).move_to((foot + topp) / 2 + LEFT * 0.6), M(r"70^\circ", 28, SECANT).move_to(foot + RIGHT * 0.65 + UP * 0.35),
                  DashedLine(W + LEFT * 0.05, topp + LEFT * 0.05, color=FUNC), M("h", 32, FUNC).move_to(W + UP * L * np.sin(a) / 2 + LEFT * 0.35))
    return VGroup(bricks, ground, rails, rungs, labs)


class Lesson(TranscriptScene):
    NUM = "0.3"

    def construct(self):
        with self.beat("How tall is the tree") as b:
            sc = surveyor_scene()
            self.play(FadeIn(sc[0]), FadeIn(sc[1]), FadeIn(sc[2]), run_time=1)
            self.play(Create(sc[4]), Create(sc[5]), FadeIn(sc[6][1]), run_time=1)
            self.play(FadeIn(sc[6][0]), run_time=0.5)
            b.line(1)
            self.play(Create(sc[3]), FadeIn(sc[6][2]), run_time=1)
            b.line(2)
            self.play(FadeIn(M(r"\frac{h}{20} = \ ?", 44, FUNC).to_corner(UL, buff=0.7)), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("From the circle to any triangle") as b:
            th = 0.6
            tri1 = right_triangle(np.cos(th) * 2, np.sin(th) * 2, opp=r"\sin\theta", adj=r"\cos\theta", hyp="1", angle=r"\theta", size=30).move_to(LEFT * 4 + DOWN * 0.8)
            self.play(Create(tri1[0]), FadeIn(tri1[1:]), run_time=1)
            b.line(1)
            tri2 = right_triangle(np.cos(th) * 4.2, np.sin(th) * 4.2, opp=r"r\sin\theta", adj=r"r\cos\theta", hyp="r", angle=r"\theta", size=32)
            tri2.move_to(tri1, aligned_edge=DL)
            self.play(ReplacementTransform(tri1, tri2), run_time=1.6)
            b.line(2)
            rat = VGroup(M(r"\sin\theta = \frac{\text{opposite}}{\text{hypotenuse}}", 38, FUNC), M(r"\cos\theta = \frac{\text{adjacent}}{\text{hypotenuse}}", 38, DERIV),
                         M(r"\tan\theta = \frac{\text{opposite}}{\text{adjacent}}", 38, TANGENT)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).to_edge(RIGHT, buff=0.5).shift(UP * 0.8)
            for r_ in rat:
                self.play(Write(r_), run_time=0.8)
            b.line(3)
            self.play(FadeIn(formula_box(T("SOH \\ CAH \\ TOA", 48, ACCUM), ACCUM).next_to(rat, DOWN, buff=0.5)), run_time=0.8)
        self.clear()

        tri = right_triangle(3.6, 1.92, opp="8", adj="15", hyp="?", angle=r"\theta", size=32)
        self.example("Ratios from sides", r"A right triangle has legs $8$ and $15$. $\theta$ is the angle opposite the side of length $8$. Find $\sin\theta$, $\cos\theta$, and $\tan\theta$.",
                     [r"\text{hyp}^2 = 8^2 + 15^2 = 64 + 225 = 289", r"\text{hyp} = 17", r"\sin\theta = \frac{\text{opp}}{\text{hyp}} = \frac{8}{17}", r"\cos\theta = \frac{\text{adj}}{\text{hyp}} = \frac{15}{17}",
                      r"\tan\theta = \frac{\text{opp}}{\text{adj}} = \frac{8}{15}"], at=[1, 2, 3, 4, 5], figure=tri)

        with self.beat("Any angle, any point") as b:
            ax, al = plot_axes([-5, 5, 1], [-5, 5, 1], w=5.6, h=5.6, coords=False)
            ax.shift(LEFT * 3 + DOWN * 0.2)
            P = ax.c2p(-3, 4)
            O = ax.c2p(0, 0)
            self.play(FadeIn(ax), FadeIn(al), run_time=0.6)
            self.play(Create(Line(O, P, color=INK, stroke_width=4)), FadeIn(Dot(P, color=FUNC)), FadeIn(M("(x, y)", 32, FUNC).next_to(P, UL, buff=0.1)),
                      FadeIn(M("r", 32).move_to((O + P) / 2 + RIGHT * 0.3 + UP * 0.15)), Create(Arc(radius=0.5, angle=np.arctan2(4, -3), arc_center=O, color=SECANT)), run_time=1)
            self.play(FadeIn(M(r"r = \sqrt{x^2 + y^2}", 36).to_edge(RIGHT, buff=0.8).shift(UP * 2.6)), run_time=0.6)
            b.line(1)
            defs = VGroup(M(r"\sin\theta = \frac{y}{r}", 42, FUNC), M(r"\cos\theta = \frac{x}{r}", 42, DERIV), M(r"\tan\theta = \frac{y}{x}", 42, TANGENT)).arrange(RIGHT, buff=0.5).to_edge(RIGHT, buff=0.4).shift(UP * 1.2)
            self.play(Write(defs), run_time=1.2)
            b.line(2)
            ex = VGroup(M(r"(-3, 4): \ r = 5", 38), M(r"\sin\theta = \tfrac45, \quad \cos\theta = -\tfrac35", 38, SECANT)).arrange(DOWN, buff=0.3).to_edge(RIGHT, buff=0.8).shift(DOWN * 0.9)
            self.play(FadeIn(M("(-3, 4)", 28, DIM).next_to(P, DOWN + LEFT * 0.2, buff=0.25)), FadeIn(ex), run_time=1)
        self.clear()

        with self.beat("The reciprocal functions") as b:
            cols = VGroup(*[VGroup(M(top, 46, c), M(bot, 40, c), T(name, 28, DIM)).arrange(DOWN, buff=0.3) for top, bot, name, c in
                            ((r"\sin\theta", r"\csc\theta = \frac{1}{\sin\theta}", "cosecant", FUNC), (r"\cos\theta", r"\sec\theta = \frac{1}{\cos\theta}", "secant", DERIV),
                             (r"\tan\theta", r"\cot\theta = \frac{1}{\tan\theta} = \frac{\cos\theta}{\sin\theta}", "cotangent", TANGENT))]).arrange(RIGHT, buff=0.9).shift(UP * 1)
            self.play(FadeIn(VGroup(*[c[0] for c in cols])), run_time=0.6)
            for c in cols:
                self.play(Write(c[1]), FadeIn(c[2]), run_time=0.8)
            b.line(1)
            tip = formula_box(T(r"one ``co'' per pair: sine with \textbf{co}secant, \textbf{co}sine with secant", 32, ACCUM), ACCUM).shift(DOWN * 1.4)
            self.play(FadeIn(tip), run_time=0.8)
            b.line(2)
            self.play(FadeIn(M(r"\csc\theta = \frac{\text{hyp}}{\text{opp}}, \quad \sec\theta = \frac{\text{hyp}}{\text{adj}}, \quad \cot\theta = \frac{\text{adj}}{\text{opp}}", 36).next_to(tip, DOWN, buff=0.5)), run_time=1)
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
            card = VGroup(T("SOH \\ CAH \\ TOA", 44, ACCUM), M(r"\csc\theta = \frac{1}{\sin\theta}, \quad \sec\theta = \frac{1}{\cos\theta}, \quad \cot\theta = \frac{1}{\tan\theta}", 40),
                          M(r"\text{point } (x, y), \text{ distance } r: \ \sin\theta = \frac{y}{r}, \ \cos\theta = \frac{x}{r}, \ \tan\theta = \frac{y}{x}", 38),
                          T(r"$\tan$, $\sec$ undefined where $\cos\theta = 0$; $\cot$, $\csc$ where $\sin\theta = 0$", 32, DIM)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Reciprocals at landmark angles", r"Find $\sec\frac{5\pi}{4}$ and $\csc\frac{5\pi}{6}$.",
                     [r"\cos\frac{5\pi}{4} = -\frac{\sqrt2}{2}", r"\sec\frac{5\pi}{4} = \frac{1}{-\sqrt2/2} = -\frac{2}{\sqrt2} = -\sqrt2", r"\sin\frac{5\pi}{6} = \frac12", r"\csc\frac{5\pi}{6} = 2"], at=[1, 2, 3, 4])
        self.example("Example 2: The tree", r"From $20$ m away, the angle up to the top of a tree is $35^\circ$. How tall is the tree?",
                     [r"\tan 35^\circ = \frac{h}{20}", r"h = 20\tan 35^\circ", r"\approx 20(0.7002) \quad \text{(degree mode)}", r"\approx 14.0 \text{ m}"], at=[1, 2, 3, 4], figure=surveyor_scene())
        self.example("Example 3: The ladder", r"A $6$ m ladder leans against a wall, making a $70^\circ$ angle with the ground. How high up the wall does it reach?",
                     [r"\sin 70^\circ = \frac{h}{6}", r"h = 6\sin 70^\circ", r"\approx 6(0.9397)", r"\approx 5.64 \text{ m}"], at=[1, 2, 3, 4], figure=ladder_scene())
        ax, al = plot_axes([-3, 1, 1], [-3, 1, 1], w=3.6, h=3.6, coords=False)
        q3 = VGroup(ax, al, Line(ax.c2p(0, 0), ax.c2p(-1, -2), color=INK, stroke_width=4), Dot(ax.c2p(-1, -2), color=FUNC), M("(-1, -2)", 26, FUNC).next_to(ax.c2p(-1, -2), LEFT, buff=0.1),
                    M(r"\sqrt5", 26).move_to(ax.c2p(-0.2, -1.2)))
        self.example("Example 4: From tangent to the rest", r"$\tan\theta = 2$ and $\theta$ is in quadrant III. Find $\sin\theta$ and $\sec\theta$.",
                     [r"\tan\theta = \frac{y}{x} = \frac{-2}{-1}", r"\text{point } (-1, -2)", r"r = \sqrt{1 + 4} = \sqrt5", r"\sin\theta = \frac{y}{r} = -\frac{2}{\sqrt5} = -\frac{2\sqrt5}{5}",
                      r"\sec\theta = \frac{r}{x} = \frac{\sqrt5}{-1} = -\sqrt5"], at=[1, 1, 2, 3, 4], figure=q3, figure_at=1)
        self.finish()
