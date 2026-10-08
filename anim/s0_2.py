"""Topic 0.2: The unit circle. Narration comes from transcripts/0_2.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def quadrant_signs(uc, rows, size=30):
    """Sign labels in each quadrant of a TrigCircle: rows[q] is a list of (tex, color) for quadrant q (0 = I)."""
    out = VGroup()
    for q, items in enumerate(rows):
        a = PI / 4 + q * PI / 2
        g = VGroup(*[M(t, size, c) for t, c in items]).arrange(DOWN, buff=0.12)
        out.add(g.move_to(uc.c + 0.55 * uc.r * np.array([np.cos(a), np.sin(a), 0])))
    return out


def circle_figure(t, ref, coords):
    """A unit circle with the point at angle t, its reference triangle, and the point at the reference angle."""
    uc = TrigCircle(r=2.0)
    g = VGroup(uc, uc.drop(t, SECANT), uc.ray(t), uc.dot(t, FUNC), uc.angle_arc(t, SECANT, radius=0.45),
               DashedLine(uc.c, uc.pt(ref), color=DIM), uc.dot(ref, DIM))
    g.add(uc.coord(t, coords, FUNC, size=28))
    return g


class Lesson(TranscriptScene):
    NUM = "0.2"

    def construct(self):
        with self.beat("A point going around") as b:
            W = ferris_wheel(2.0).move_to(LEFT * 2.6 + DOWN * 0.1)
            hub = W[0].get_center()
            self.play(FadeIn(W), run_time=0.8)
            th = ValueTracker(-PI / 2)
            rider = always_redraw(lambda: Dot(hub + 2.0 * np.array([np.cos(th.get_value()), np.sin(th.get_value()), 0]), radius=0.14, color=TANGENT))
            up = always_redraw(lambda: DashedLine(rider.get_center(), np.array([1.6, rider.get_center()[1], 0]), color=FUNC))
            across = always_redraw(lambda: DashedLine(rider.get_center(), np.array([rider.get_center()[0], -3.3, 0]), color=DERIV))
            scale_up = Line(np.array([1.6, hub[1] - 2.2, 0]), np.array([1.6, hub[1] + 2.2, 0]), color=FUNC, stroke_width=4)
            scale_ac = Line(np.array([hub[0] - 2.4, -3.3, 0]), np.array([hub[0] + 2.4, -3.3, 0]), color=DERIV, stroke_width=4)
            self.play(FadeIn(rider), Create(scale_up), Create(scale_ac), Create(up), Create(across), run_time=1)
            self.play(FadeIn(T("how far up", 30, FUNC).next_to(scale_up, RIGHT, buff=0.2)), FadeIn(T("how far across", 30, DERIV).next_to(scale_ac, RIGHT, buff=0.2)), run_time=0.6)
            b.line(1)
            self.play(th.animate.set_value(-PI / 2 + 2 * PI), run_time=4, rate_func=linear)
            b.line(2)
            self.play(FadeIn(M(r"\text{across} = \cos\theta, \quad \text{up} = \sin\theta", 40).to_corner(UR, buff=0.6)), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("Sine and cosine on the unit circle") as b:
            uc = TrigCircle(r=2.6, center=LEFT * 2.8 + DOWN * 0.3)
            t = 0.9
            self.play(Create(uc), run_time=0.8)
            self.play(Create(uc.ray(t)), FadeIn(uc.angle_arc(t, label=r"\theta")), FadeIn(uc.dot(t)), FadeIn(M("P", 32, FUNC).next_to(uc.pt(t), UR, buff=0.1)), run_time=1)
            b.line(1)
            p = uc.pt(t)
            hx = Line(uc.c, np.array([p[0], uc.c[1], 0]), color=DERIV, stroke_width=6)
            vy = Line(np.array([p[0], uc.c[1], 0]), p, color=FUNC, stroke_width=6)
            self.play(Create(hx), FadeIn(M(r"x = \cos\theta", 32, DERIV).next_to(hx, DOWN, buff=0.15)), run_time=0.8)
            self.play(Create(vy), FadeIn(M(r"y = \sin\theta", 32, FUNC).next_to(vy, RIGHT, buff=0.15)), run_time=0.8)
            big = M(r"P = (\cos\theta,\ \sin\theta)", 46).to_edge(RIGHT, buff=0.6).shift(UP * 1.8)
            self.play(Write(big), run_time=0.8)
            b.line(2)
            words = VGroup(T("cosine: how far across", 34, DERIV), T("sine: how far up", 34, FUNC)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(big, DOWN, buff=0.6)
            self.play(FadeIn(words), run_time=0.8)
            b.line(3)
            pyth = formula_box(M(r"\cos^2\theta + \sin^2\theta = 1", 44, ACCUM), ACCUM).next_to(words, DOWN, buff=0.6)
            self.play(FadeIn(M(r"x^2 + y^2 = 1", 38, DIM).next_to(words, DOWN, buff=0.3)), run_time=0.6)
            self.play(FadeIn(pyth.next_to(words, DOWN, buff=1.0)), run_time=0.8)
        self.clear()

        with self.beat("The quadrantal angles") as b:
            uc = TrigCircle(r=2.4, center=LEFT * 3.2 + DOWN * 0.2)
            self.play(Create(uc), run_time=0.6)
            data = [(0, "(1, 0)", "0", "1", "0"), (PI / 2, "(0, 1)", r"\tfrac{\pi}{2}", "0", "1"), (PI, "(-1, 0)", r"\pi", "-1", "0"), (3 * PI / 2, "(0, -1)", r"\tfrac{3\pi}{2}", "0", "-1")]
            tab = table([r"\theta", r"\cos\theta", r"\sin\theta"], [[d[2], d[3], d[4]] for d in data], size=34).to_edge(RIGHT, buff=0.8)
            for k, (a, lab, _, _, _) in enumerate(data):
                if k == 1:
                    b.line(1)
                if k == 2:
                    b.line(2)
                d = np.array([np.cos(a), np.sin(a), 0])
                self.play(FadeIn(uc.dot(a, SECANT)), FadeIn(M(lab, 30, SECANT).move_to(uc.pt(a) + 0.6 * d + (UP * 0.3 if k in (0, 2) else RIGHT * 0.7))), run_time=0.6)
            self.play(FadeIn(tab), run_time=0.8)
        self.clear()

        with self.beat("The special triangles") as b:
            t45 = right_triangle(2.4, 2.4, opp=r"a", adj=r"a", hyp="1", angle=r"45^\circ").move_to(LEFT * 3.6 + UP * 0.4)
            self.play(Create(t45[0]), FadeIn(t45[1:]), run_time=1)
            b.line(1)
            work = VGroup(M(r"a^2 + a^2 = 1", 38), M(r"a^2 = \tfrac12", 38), M(r"a = \frac{1}{\sqrt2} = \frac{\sqrt2}{2}", 38, FUNC)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(t45, DOWN, buff=0.4)
            for w in work:
                self.play(Write(w), run_time=0.6)
            b.line(2)
            eq = Polygon(ORIGIN, RIGHT * 2.6, RIGHT * 1.3 + UP * 1.3 * np.sqrt(3), color=DIM, stroke_width=3).move_to(RIGHT * 2.2 + UP * 1.3)
            self.play(Create(eq), FadeIn(M("1", 28, DIM).next_to(eq, DOWN, buff=0.1)), run_time=0.8)
            half = Polygon(eq.get_vertices()[0], (eq.get_vertices()[0] + eq.get_vertices()[1]) / 2, eq.get_vertices()[2], color=INK, stroke_width=5)
            self.play(Create(half), Create(DashedLine((eq.get_vertices()[0] + eq.get_vertices()[1]) / 2, eq.get_vertices()[2], color=INK)), run_time=0.8)
            labs = VGroup(M(r"\tfrac12", 32, DERIV).next_to(Line(eq.get_vertices()[0], (eq.get_vertices()[0] + eq.get_vertices()[1]) / 2), DOWN, buff=0.45),
                          M(r"\frac{\sqrt3}{2}", 32, FUNC).move_to((eq.get_vertices()[0] + eq.get_vertices()[1]) / 2 + UP * 1.1 + RIGHT * 0.45),
                          M(r"30^\circ", 24, SECANT).move_to(eq.get_vertices()[2] + DOWN * 0.75 + LEFT * 0.12),
                          M(r"60^\circ", 24, SECANT).move_to(eq.get_vertices()[0] + RIGHT * 0.5 + UP * 0.22))
            self.play(FadeIn(labs[0]), FadeIn(labs[2:]), run_time=0.6)
            self.play(FadeIn(M(r"\sqrt{1 - \tfrac14} = \frac{\sqrt3}{2}", 32, DIM).next_to(eq, DOWN, buff=0.6)), FadeIn(labs[1]), run_time=0.8)
            b.line(3)
            pts = VGroup(M(r"\tfrac{\pi}{6}: \ \left(\tfrac{\sqrt3}{2},\ \tfrac12\right)", 38, SECANT), M(r"\tfrac{\pi}{4}: \ \left(\tfrac{\sqrt2}{2},\ \tfrac{\sqrt2}{2}\right)", 38, SECANT),
                         M(r"\tfrac{\pi}{3}: \ \left(\tfrac12,\ \tfrac{\sqrt3}{2}\right)", 38, SECANT)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_edge(RIGHT, buff=0.8).shift(DOWN * 2.0)
            self.play(FadeIn(pts[0]), FadeIn(pts[2]), run_time=0.8)
            self.play(FadeIn(pts[1]), run_time=0.5)
            b.line(4)
            self.play(Indicate(pts[0]), run_time=1)
        self.clear()

        with self.beat("Reference angles") as b:
            uc = TrigCircle(r=2.5, center=LEFT * 2.8 + DOWN * 0.3)
            t = 5 * PI / 6
            self.play(Create(uc), Create(uc.ray(t, FUNC)), FadeIn(uc.dot(t)), run_time=0.8)
            ref = Sector(radius=0.9, start_angle=t, angle=PI - t, arc_center=uc.c, fill_color=SECANT, fill_opacity=0.5, stroke_width=0)
            self.play(FadeIn(ref), FadeIn(T(r"reference angle $\frac{\pi}{6}$", 32, SECANT).to_edge(RIGHT, buff=0.8).shift(UP * 2)), run_time=0.8)
            b.line(1)
            self.play(TransformFromCopy(VGroup(uc.ray(t, FUNC), uc.dot(t)), VGroup(uc.ray(PI / 6, DIM), uc.dot(PI / 6, DIM))),
                      Create(DashedLine(uc.pt(t), uc.pt(PI / 6), color=DIM)), run_time=1.2)
            self.play(FadeIn(uc.coord(t, r"\left(-\tfrac{\sqrt3}{2},\ \tfrac12\right)", FUNC, 28)), FadeIn(uc.coord(PI / 6, r"\left(\tfrac{\sqrt3}{2},\ \tfrac12\right)", DIM, 28)), run_time=0.8)
            b.line(2)
            self.play(FadeIn(T("same numbers; the quadrant decides the signs", 32).to_edge(RIGHT, buff=0.5).shift(DOWN * 2.6)), run_time=0.8)
        self.clear()

        with self.beat("Signs by quadrant") as b:
            uc = TrigCircle(r=2.8, center=LEFT * 2.4 + DOWN * 0.2, ticks=False)
            self.play(Create(uc), run_time=0.6)
            right = Sector(radius=2.8, start_angle=-PI / 2, angle=PI, arc_center=uc.c, fill_color=DERIV, fill_opacity=0.15, stroke_width=0)
            self.play(FadeIn(right), FadeIn(T(r"$\cos\theta = x$: $+$ on the right, $-$ on the left", 30, DERIV).to_edge(RIGHT, buff=0.4).shift(UP * 2.2)), run_time=0.8)
            b.line(1)
            top = Sector(radius=2.8, start_angle=0, angle=PI, arc_center=uc.c, fill_color=FUNC, fill_opacity=0.15, stroke_width=0)
            self.play(FadeOut(right), FadeIn(top), FadeIn(T(r"$\sin\theta = y$: $+$ on top, $-$ on the bottom", 30, FUNC).to_edge(RIGHT, buff=0.4).shift(UP * 1.5)), run_time=0.8)
            b.line(2)
            self.play(FadeOut(top), run_time=0.3)
            signs = quadrant_signs(uc, [[(r"\cos +", DERIV), (r"\sin +", FUNC)], [(r"\cos -", DERIV), (r"\sin +", FUNC)],
                                        [(r"\cos -", DERIV), (r"\sin -", FUNC)], [(r"\cos +", DERIV), (r"\sin -", FUNC)]], 34)
            for s in signs:
                self.play(FadeIn(s), run_time=0.6)
            qs = VGroup(*[M(n, 30, DIM).move_to(uc.c + 0.92 * uc.r * np.array([np.cos(PI / 4 + q * PI / 2), np.sin(PI / 4 + q * PI / 2), 0])) for q, n in enumerate(["I", "II", "III", "IV"])])
            self.play(FadeIn(qs), run_time=0.5)
        self.clear()

        fig = circle_figure(5 * PI / 6, PI / 6, r"\left(-\tfrac{\sqrt3}{2},\ \tfrac12\right)")
        self.example("Sine and cosine of 5π/6", r"Find $\cos\frac{5\pi}{6}$ and $\sin\frac{5\pi}{6}$.",
                     [r"\text{reference angle: } \pi - \frac{5\pi}{6} = \frac{\pi}{6}", r"\text{at } \tfrac{\pi}{6}: \ \left(\tfrac{\sqrt3}{2},\ \tfrac12\right)",
                      r"\text{quadrant II: } \cos < 0, \ \sin > 0", r"\cos\frac{5\pi}{6} = -\frac{\sqrt3}{2}", r"\sin\frac{5\pi}{6} = \frac12"],
                     at=[1, 2, 3, 4, 5], figure=fig, figure_at=1, follow=True)

        with self.beat("Tangent") as b:
            uc = TrigCircle(r=2.5, center=LEFT * 2.8 + DOWN * 0.3)
            t = ValueTracker(0.7)
            ray = always_redraw(lambda: uc.ray(t.get_value(), FUNC))
            dot = always_redraw(lambda: uc.dot(t.get_value()))
            rise = always_redraw(lambda: Line(np.array([uc.pt(t.get_value())[0], uc.c[1], 0]), uc.pt(t.get_value()), color=FUNC, stroke_width=5))
            run = always_redraw(lambda: Line(uc.c, np.array([uc.pt(t.get_value())[0], uc.c[1], 0]), color=DERIV, stroke_width=5))
            self.play(Create(uc), FadeIn(ray), FadeIn(dot), FadeIn(rise), FadeIn(run), run_time=0.8)
            f = M(r"\tan\theta = \frac{\sin\theta}{\cos\theta}", 50, TANGENT).to_edge(RIGHT, buff=1).shift(UP * 1.8)
            self.play(Write(f), run_time=1)
            b.line(1)
            self.play(FadeIn(M(r"= \frac{\text{rise}}{\text{run}} = \text{slope of the ray}", 38, TANGENT).next_to(f, DOWN, buff=0.4)), run_time=0.8)
            b.line(2)
            self.play(t.animate.set_value(PI / 2), run_time=1.4)
            self.play(FadeIn(M(r"\theta = \tfrac{\pi}{2}: \ \cos\theta = 0, \ \tan\theta \text{ undefined}", 36, SECANT).to_edge(RIGHT, buff=0.5).shift(DOWN * 1.4)), run_time=0.8)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(M(r"(\cos\theta,\ \sin\theta) \text{ is the point at angle } \theta", 42), M(r"\cos^2\theta + \sin^2\theta = 1", 44, ACCUM),
                          M(r"\tfrac{\pi}{6}: \left(\tfrac{\sqrt3}{2}, \tfrac12\right) \quad \tfrac{\pi}{4}: \left(\tfrac{\sqrt2}{2}, \tfrac{\sqrt2}{2}\right) \quad \tfrac{\pi}{3}: \left(\tfrac12, \tfrac{\sqrt3}{2}\right)", 38, SECANT),
                          T("Reference angle gives the numbers; the quadrant gives the signs.", 34), M(r"\tan\theta = \frac{\sin\theta}{\cos\theta}", 42, TANGENT)).arrange(DOWN, buff=0.4)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2.4)
        self.clear()

        self.examples_card()
        self.example("Example 1: An angle in the third quadrant", r"Find $\cos\frac{4\pi}{3}$ and $\sin\frac{4\pi}{3}$.",
                     [r"\frac{4\pi}{3} - \pi = \frac{\pi}{3}", r"\text{at } \tfrac{\pi}{3}: \ \left(\tfrac12,\ \tfrac{\sqrt3}{2}\right)", r"\text{quadrant III: both negative}",
                      r"\cos\frac{4\pi}{3} = -\frac12, \quad \sin\frac{4\pi}{3} = -\frac{\sqrt3}{2}"], at=[1, 2, 3, 4],
                     figure=circle_figure(4 * PI / 3, PI / 3, r"\left(-\tfrac12,\ -\tfrac{\sqrt3}{2}\right)"), figure_at=1)
        self.example("Example 2: A negative angle", r"Find $\sin\left(-\frac{\pi}{4}\right)$ and $\cos\left(-\frac{\pi}{4}\right)$.",
                     [r"\text{reference angle } \tfrac{\pi}{4}, \text{ quadrant IV}", r"\text{at } \tfrac{\pi}{4}: \ \left(\tfrac{\sqrt2}{2},\ \tfrac{\sqrt2}{2}\right)", r"\text{quadrant IV: } \cos > 0, \ \sin < 0",
                      r"\sin\left(-\tfrac{\pi}{4}\right) = -\frac{\sqrt2}{2}, \quad \cos\left(-\tfrac{\pi}{4}\right) = \frac{\sqrt2}{2}"], at=[1, 2, 3, 4],
                     figure=circle_figure(-PI / 4, PI / 4, r"\left(\tfrac{\sqrt2}{2},\ -\tfrac{\sqrt2}{2}\right)"), figure_at=1)
        self.example("Example 3: Quadrantal angles", r"Find $\cos 3\pi$ and $\sin\frac{3\pi}{2}$.",
                     [r"3\pi - 2\pi = \pi", r"\text{point at } \pi: (-1, 0), \text{ so } \cos 3\pi = -1", r"\text{point at } \tfrac{3\pi}{2}: (0, -1)", r"\sin\frac{3\pi}{2} = -1"], at=[1, 2, 3, 4])
        self.example("Example 4: From sine to cosine", r"$\sin\theta = \frac35$ and $\theta$ is in quadrant II. Find $\cos\theta$ and $\tan\theta$.",
                     [r"\cos^2\theta + \sin^2\theta = 1, \quad \sin^2\theta = \frac{9}{25}", r"\cos^2\theta = 1 - \frac{9}{25} = \frac{16}{25}", r"\cos\theta = \pm\frac45",
                      r"\text{quadrant II: } \cos\theta < 0, \text{ so } \cos\theta = -\frac45", r"\tan\theta = \frac{3/5}{-4/5} = -\frac34"], at=[1, 2, 3, 3, 4])
        self.finish()
