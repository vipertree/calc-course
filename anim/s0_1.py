"""Topic 0.1: Angles and radian measure. Narration comes from transcripts/0_1.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def wheel_at(th, u, x0, ground):
    """A bicycle wheel of radius u (one 'unit') that has rolled through angle th from x = x0."""
    c = np.array([x0 + u * th, ground + u, 0])
    rim = Circle(radius=u, stroke_color=INK, stroke_width=6).move_to(c)
    spokes = VGroup(*[Line(c, c + u * np.array([np.cos(a - th), np.sin(a - th), 0]), color=DIM, stroke_width=2) for a in np.linspace(0, TAU, 12, endpoint=False)])
    dot = Dot(c + u * np.array([np.cos(-PI / 2 - th), np.sin(-PI / 2 - th), 0]), radius=0.1, color=TANGENT)
    return VGroup(spokes, rim, Dot(c, radius=0.07, color=INK), dot)


def pizza(r=1.2, slice_angle=PI / 4):
    """A pizza with one slice pulled out a little (vector art)."""
    crust, cheese = "#D9A35B", "#F6D67A"
    rest = AnnularSector(inner_radius=0, outer_radius=r, angle=TAU - slice_angle, start_angle=slice_angle, fill_color=cheese, fill_opacity=1, stroke_color=crust, stroke_width=8)
    piece = Sector(radius=r, angle=slice_angle, fill_color=cheese, fill_opacity=1, stroke_color=crust, stroke_width=8).shift(0.3 * np.array([np.cos(slice_angle / 2), np.sin(slice_angle / 2), 0]))
    rng = np.random.default_rng(7)
    pep = VGroup(*[Circle(radius=0.11, stroke_width=0, fill_color="#B5332E", fill_opacity=1).move_to(rr * np.array([np.cos(a), np.sin(a), 0]))
                   for rr, a in zip(r * (0.25 + 0.6 * rng.random(9)), slice_angle + (TAU - slice_angle) * rng.random(9))])
    return VGroup(rest, pep, piece)


class Lesson(TranscriptScene):
    NUM = "0.1"

    def construct(self):
        with self.beat("Measuring a turn") as b:
            u, x0, ground = 0.9, -5.4, -2.4
            road = Line(LEFT * 6.4 + UP * ground, RIGHT * 6.4 + UP * ground, color=INK, stroke_width=4)
            th = ValueTracker(0)
            wheel = always_redraw(lambda: wheel_at(th.get_value(), u, x0, ground))
            trail = always_redraw(lambda: Line(np.array([x0, ground, 0]), np.array([x0 + u * th.get_value() + 1e-3, ground, 0]), color=TANGENT, stroke_width=8))
            proto = VGroup(Arc(radius=1.1, angle=PI, color=DIM, stroke_width=3), Line(LEFT * 1.1, RIGHT * 1.1, color=DIM, stroke_width=3),
                           M(r"360^\circ\,?", 40, DIM).shift(UP * 0.5)).move_to(RIGHT * 4 + UP * 2.2)
            self.play(Create(road), FadeIn(wheel), FadeIn(proto), run_time=1)
            b.line(1)
            self.add(trail)
            for k, (stop, lab) in enumerate(((PI / 2, "1.57"), (PI, "3.14"), (2 * PI, "6.28"))):
                self.play(th.animate.set_value(stop), run_time=1.4)
                self.play(FadeIn(M(lab, 30, TANGENT).move_to(np.array([x0 + u * stop, ground - 0.4, 0]))), run_time=0.4)
            b.line(2)
            self.play(FadeOut(proto), FadeIn(T("distance rolled = angle turned, in radians", 36, TANGENT).to_edge(UP, buff=0.8)), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("Angles in standard position") as b:
            ax, _ = plot_axes([-3, 3, 1], [-3, 3, 1], w=5.6, h=5.6, coords=False)
            ax.shift(LEFT * 2.6 + DOWN * 0.2)
            O = ax.c2p(0, 0)
            init = Line(O, ax.c2p(2.6, 0), color=INK, stroke_width=5)
            self.play(FadeIn(ax), Create(init), FadeIn(T("initial side", 28).next_to(ax.c2p(2.0, 0), DOWN, buff=0.15)), run_time=0.9)
            t = ValueTracker(0.001)
            term = always_redraw(lambda: Line(O, O + 2.6 * ax.x_axis.get_unit_size() / 1.0 * np.array([np.cos(t.get_value()), np.sin(t.get_value()), 0]), color=FUNC, stroke_width=5))
            arc = always_redraw(lambda: Arc(radius=0.7, angle=t.get_value(), arc_center=O, color=SECANT, stroke_width=4).add_tip(tip_length=0.15))
            self.add(term, arc)
            self.play(t.animate.set_value(2.2), run_time=1.6)
            self.play(FadeIn(M(r"\theta > 0", 34, SECANT).move_to(O + 1.25 * np.array([np.cos(1.1), np.sin(1.1), 0]))),
                      FadeIn(T("terminal side", 28, FUNC).next_to(O + 2.6 * ax.x_axis.get_unit_size() * np.array([np.cos(2.2), np.sin(2.2), 0]), UP, buff=0.1)), run_time=0.6)
            b.line(1)
            self.play(FadeIn(T("counterclockwise: positive", 34, SECANT).to_edge(RIGHT, buff=0.6).shift(UP * 1)), run_time=0.6)
            neg = Arc(radius=1.0, angle=-1.0, arc_center=O, color=TANGENT, stroke_width=4).add_tip(tip_length=0.15)
            self.play(Create(Line(O, O + 2.6 * ax.x_axis.get_unit_size() * np.array([np.cos(-1.0), np.sin(-1.0), 0]), color=TANGENT, stroke_width=5)), Create(neg), run_time=1)
            self.play(FadeIn(T("clockwise: negative", 34, TANGENT).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.2)), run_time=0.6)
        self.clear()

        with self.beat("What a radian is") as b:
            R, O = 2.0, LEFT * 3 + DOWN * 0.3
            circ = Circle(radius=R, color=INK, stroke_width=3).move_to(O)
            rad = Line(O, O + RIGHT * R, color=FUNC, stroke_width=6)
            self.play(Create(circ), Create(rad), FadeIn(M("r", 34, FUNC).next_to(rad, DOWN, buff=0.1)), run_time=1)
            b.line(1)
            bent = Arc(radius=R, start_angle=0, angle=1, arc_center=O, color=FUNC, stroke_width=8)
            self.play(Transform(rad.copy(), bent), run_time=1.4)
            self.play(FadeIn(Sector(radius=R, angle=1, arc_center=O, fill_color=SECANT, fill_opacity=0.3, stroke_width=0)),
                      Create(Line(O, O + R * np.array([np.cos(1), np.sin(1), 0]), color=INK, stroke_width=3)),
                      FadeIn(M(r"1 \text{ radian} \approx 57.3^\circ", 34, SECANT).to_edge(RIGHT, buff=0.8).shift(UP * 2)), run_time=1)
            b.line(2)
            arcs = VGroup(*[Arc(radius=R + 0.12 * (k % 2), start_angle=k, angle=min(1, TAU - k), arc_center=O, color=[FUNC, DERIV][k % 2], stroke_width=8) for k in range(7)])
            nums = VGroup(*[M(str(k + 1), 28, [FUNC, DERIV][k % 2]).move_to(O + (R + 0.5) * np.array([np.cos(k + 0.5), np.sin(k + 0.5), 0])) for k in range(6)])
            for a, n in zip(arcs[:6], nums):
                self.play(Create(a), FadeIn(n), run_time=0.45)
            self.play(Create(arcs[6]), run_time=0.4)
            self.play(FadeIn(M(r"\text{circumference} = 2\pi r", 38).to_edge(RIGHT, buff=0.8).shift(UP * 0.6)), run_time=0.8)
            b.line(3)
            box = formula_box(VGroup(M(r"\text{full turn} = 2\pi \approx 6.28 \text{ radians}", 40, ACCUM), M(r"\text{half turn} = \pi \text{ radians}", 40, ACCUM)).arrange(DOWN, buff=0.3), ACCUM)
            self.play(FadeIn(box.to_edge(RIGHT, buff=0.6).shift(DOWN * 1.4)), run_time=0.8)
        self.clear()

        with self.beat("Converting") as b:
            fact = formula_box(M(r"180^\circ = \pi \text{ radians}", 56, ACCUM), ACCUM).to_edge(UP, buff=0.8)
            self.play(FadeIn(fact), run_time=0.8)
            b.line(1)
            r1 = M(r"\text{degrees} \to \text{radians:} \quad \times \frac{\pi}{180^\circ}", 46, FUNC)
            r2 = M(r"\text{radians} \to \text{degrees:} \quad \times \frac{180^\circ}{\pi}", 46, DERIV)
            VGroup(r1, r2).arrange(DOWN, buff=0.6).next_to(fact, DOWN, buff=0.8)
            self.play(Write(r1), run_time=1)
            self.play(Write(r2), run_time=1)
            b.line(2)
            self.play(FadeIn(M(r"60^\circ \cdot \frac{\pi}{180^\circ} = \frac{\pi}{3}", 42, DIM).next_to(r2, DOWN, buff=0.7)), run_time=0.8)
        self.clear()

        self.example("Converting 150 degrees", r"Convert $150^\circ$ to radians.",
                     [r"150^\circ \cdot \frac{\pi}{180^\circ}", r"= \frac{150\pi}{180}", r"= \frac{150 \div 30}{180 \div 30}\,\pi = \frac{5\pi}{6}"], at=[1, 2, 3])

        with self.beat("Landmark angles") as b:
            uc = TrigCircle(r=2.7, center=LEFT * 2.2 + DOWN * 0.2, ticks=False)
            self.play(Create(uc), run_time=0.8)
            names = {0: ("0", "0^\\circ"), 1: (r"\tfrac{\pi}{6}", "30^\\circ"), 2: (r"\tfrac{\pi}{4}", "45^\\circ"), 3: (r"\tfrac{\pi}{3}", "60^\\circ")}
            quads = [(PI / 2, r"\tfrac{\pi}{2}", "90^\\circ"), (PI, r"\pi", "180^\\circ"), (3 * PI / 2, r"\tfrac{3\pi}{2}", "270^\\circ")]

            def mark(t, lab, deg, col=FUNC):
                d = np.array([np.cos(t), np.sin(t), 0])
                return VGroup(uc.dot(t, col), M(lab, 30, col).move_to(uc.pt(t) + 0.55 * d), M(deg, 20, DIM).move_to(uc.pt(t) + 0.98 * d))
            self.play(FadeIn(mark(0, "0", "0^\\circ")), *[FadeIn(mark(t, l, d)) for t, l, d in quads], run_time=1)
            b.line(1)
            self.play(*[FadeIn(mark(t, l, d, SECANT)) for t, l, d in ((PI / 6, r"\tfrac{\pi}{6}", "30^\\circ"), (PI / 4, r"\tfrac{\pi}{4}", "45^\\circ"), (PI / 3, r"\tfrac{\pi}{3}", "60^\\circ"))], run_time=1)
            b.line(2)
            rest = [(2 * PI / 3, r"\tfrac{2\pi}{3}"), (3 * PI / 4, r"\tfrac{3\pi}{4}"), (5 * PI / 6, r"\tfrac{5\pi}{6}"), (7 * PI / 6, r"\tfrac{7\pi}{6}"), (5 * PI / 4, r"\tfrac{5\pi}{4}"),
                    (4 * PI / 3, r"\tfrac{4\pi}{3}"), (5 * PI / 3, r"\tfrac{5\pi}{3}"), (7 * PI / 4, r"\tfrac{7\pi}{4}"), (11 * PI / 6, r"\tfrac{11\pi}{6}")]
            for q in range(3):
                grp = [(t, l) for t, l in rest if q * PI / 2 + PI / 2 < t < (q + 2) * PI / 2]
                self.play(*[FadeIn(mark(t, l, f"{round(np.degrees(t))}^\\circ", DERIV)) for t, l in grp], run_time=0.8)
            steps = VGroup(*[Line(uc.c, uc.pt(k * PI / 6), color=DERIV, stroke_width=2) for k in range(1, 6)])
            self.play(Create(steps), FadeIn(M(r"\tfrac{5\pi}{6} = 5 \times 30^\circ", 38, DERIV).to_edge(RIGHT, buff=0.6)), run_time=1)
        self.clear()

        with self.beat("Coterminal angles") as b:
            uc = TrigCircle(r=2.3, center=LEFT * 3 + DOWN * 0.3)
            self.play(Create(uc), Create(uc.ray(PI / 3, FUNC)), FadeIn(uc.angle_arc(PI / 3, FUNC, label=r"\tfrac{\pi}{3}")), run_time=1)
            t = ValueTracker(0.001)
            spin = always_redraw(lambda: VGroup(uc.ray(t.get_value(), SECANT), ParametricFunction(lambda s: uc.c + (0.8 + 0.06 * s) * np.array([np.cos(s), np.sin(s), 0]), t_range=[0, t.get_value(), 0.02], color=SECANT, stroke_width=4)))
            self.add(spin)
            self.play(t.animate.set_value(PI / 3 + 2 * PI), run_time=2.2)
            self.play(FadeIn(M(r"\tfrac{\pi}{3} + 2\pi = \tfrac{7\pi}{3}", 42, SECANT).to_edge(RIGHT, buff=0.7).shift(UP * 1.2)), run_time=0.6)
            b.line(1)
            t2 = ValueTracker(-0.001)
            spin2 = always_redraw(lambda: ParametricFunction(lambda s: uc.c + (1.25 + 0.06 * abs(s)) * np.array([np.cos(s), np.sin(s), 0]), t_range=[t2.get_value(), 0, 0.02], color=TANGENT, stroke_width=4))
            self.add(spin2)
            self.play(t2.animate.set_value(PI / 3 - 2 * PI), run_time=1.6)
            self.play(FadeIn(M(r"\tfrac{\pi}{3} - 2\pi = -\tfrac{5\pi}{3}", 42, TANGENT).to_edge(RIGHT, buff=0.7).shift(DOWN * 0.2)), run_time=0.6)
            self.play(FadeIn(T("same terminal side", 34).to_edge(RIGHT, buff=0.9).shift(DOWN * 1.6)), run_time=0.6)
        self.clear()

        with self.beat("Arc length and sector area") as b:
            R, O, th = 2.2, LEFT * 3.4 + DOWN * 0.8, 1.1
            circ = Circle(radius=R, color=DIM, stroke_width=2).move_to(O)
            sec = Sector(radius=R, angle=th, arc_center=O, fill_color=AREA, fill_opacity=0.4, stroke_width=0)
            arc = Arc(radius=R, angle=th, arc_center=O, color=TANGENT, stroke_width=9)
            edges = VGroup(Line(O, O + RIGHT * R, color=INK), Line(O, O + R * np.array([np.cos(th), np.sin(th), 0]), color=INK))
            self.play(Create(circ), Create(edges), FadeIn(M("r", 30).next_to(edges[0], DOWN, buff=0.1)), FadeIn(M(r"\theta", 30, SECANT).move_to(O + 0.6 * np.array([np.cos(th / 2), np.sin(th / 2), 0]))), run_time=0.8)
            self.play(Create(arc), FadeIn(M("s", 34, TANGENT).move_to(O + (R + 0.35) * np.array([np.cos(th / 2), np.sin(th / 2), 0]))), run_time=0.8)
            f1 = M(r"s = r\theta", 52, TANGENT).to_edge(RIGHT, buff=1.6).shift(UP * 2)
            self.play(Write(f1), run_time=0.8)
            b.line(1)
            self.play(FadeIn(sec), run_time=0.6)
            f2 = M(r"A = \frac{\theta}{2\pi}\cdot \pi r^2 = \tfrac12 r^2\theta", 46, AREA).next_to(f1, DOWN, buff=0.6)
            self.play(Write(f2), run_time=1)
            self.play(FadeIn(pizza(0.9).next_to(f2, DOWN, buff=0.5)), run_time=0.6)
            b.line(2)
            self.play(FadeIn(T(r"$\theta$ in radians", 36, SECANT).next_to(circ, DOWN, buff=0.3)), run_time=0.6)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(M(r"180^\circ = \pi \text{ radians}", 46, ACCUM), M(r"\text{full turn: } 2\pi", 42), M(r"\text{coterminal: add or subtract } 2\pi", 40),
                          M(r"s = r\theta, \quad A = \tfrac12 r^2\theta \quad (\theta \text{ in radians})", 42, TANGENT)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Radians to degrees", r"Convert $\frac{5\pi}{4}$ to degrees.",
                     [r"\frac{5\pi}{4} \cdot \frac{180^\circ}{\pi}", r"= \frac{5 \cdot 180^\circ}{4}", r"= 5 \cdot 45^\circ = 225^\circ"], at=[1, 2, 3])
        self.example("Example 2: Coterminal angles", r"Find the angle between $0$ and $2\pi$ that is coterminal with $\frac{17\pi}{6}$.",
                     [r"2\pi = \frac{12\pi}{6}", r"\frac{17\pi}{6} - \frac{12\pi}{6} = \frac{5\pi}{6}", r"TEXT:$\frac{5\pi}{6}$ is between $0$ and $2\pi$."], at=[1, 2, 3])
        pend = VGroup(Dot(ORIGIN, radius=0.08, color=INK), Line(ORIGIN, 3 * np.array([np.sin(-PI / 12), -np.cos(PI / 12), 0]), color=DIM, stroke_width=3),
                      Line(ORIGIN, 3 * np.array([np.sin(PI / 12), -np.cos(PI / 12), 0]), color=INK, stroke_width=4),
                      Arc(radius=3, start_angle=-PI / 2 - PI / 12, angle=PI / 6, color=TANGENT, stroke_width=8),
                      Circle(radius=0.22, stroke_color=INK, fill_color="#C9A227", fill_opacity=1).move_to(3 * np.array([np.sin(PI / 12), -np.cos(PI / 12), 0])),
                      M(r"80 \text{ cm}", 28).move_to(1.5 * np.array([np.sin(PI / 12), -np.cos(PI / 12), 0]) + RIGHT * 0.6),
                      M(r"30^\circ", 28, SECANT).move_to(DOWN * 1.0))
        self.example("Example 3: Arc length", r"A pendulum $80$ cm long swings through an angle of $30^\circ$. How far does its tip travel?",
                     [r"30^\circ = \frac{\pi}{6}", r"s = r\theta = 80 \cdot \frac{\pi}{6}", r"= \frac{40\pi}{3} \approx 41.9 \text{ cm}"], at=[1, 2, 3], figure=pend)
        self.example("Example 4: Sector area", r"A pizza has radius $8$ inches and is cut into $8$ equal slices. Find the area of one slice.",
                     [r"\theta = \frac{2\pi}{8} = \frac{\pi}{4}", r"A = \tfrac12 r^2\theta = \tfrac12 \cdot 64 \cdot \frac{\pi}{4}", r"= 8\pi \approx 25.1 \text{ in}^2"], at=[1, 2, 3], figure=pizza(1.6))
        self.finish()
