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

    def box(self, X, center, k=0.22, fold=None):
        """The box in an oblique view: base (12 - 2X) inches square, flaps X inches, folded up by angle fold (a ValueTracker
        in degrees; 90 = finished box). The inside faces are darker than the outside and the rim is outlined, so it reads
        as an open-top box (Adder)."""
        D = np.array([0.45, 0.3, 0])                    # screen offset per unit of depth
        INNER, INNER_DK = "#8F6438", "#7A532E"

        def draw():
            x = X.get_value()
            th = np.radians(fold.get_value() if fold is not None else 90)
            w, t = (12 - 2 * x) * k, x * k
            o = center + LEFT * (w * (1 + D[0])) / 2 + DOWN * (w * D[1]) / 2
            P = lambda u, v, z: o + u * RIGHT + v * D + z * UP
            c, s_ = t * np.cos(th), t * np.sin(th)
            face = lambda pts, col: Polygon(*pts, stroke_color=CARD_DK, stroke_width=2, fill_color=col, fill_opacity=1)
            back = face([P(0, w, 0), P(w, w, 0), P(w, w + c, s_), P(0, w + c, s_)], INNER)
            left = face([P(0, 0, 0), P(0, w, 0), P(-c, w, s_), P(-c, 0, s_)], INNER_DK)
            floor = face([P(0, 0, 0), P(w, 0, 0), P(w, w, 0), P(0, w, 0)], interpolate_color(ManimColor(CARD_LT), ManimColor(INNER_DK), min(th / 1.2, 1)))
            right = face([P(w, 0, 0), P(w, w, 0), P(w + c, w, s_), P(w + c, 0, s_)], CARD_DK)
            front = face([P(0, 0, 0), P(w, 0, 0), P(w, -c, s_), P(0, -c, s_)], CARD)
            out = VGroup(back, left, floor, right, front)
            if th > 1.2:                                # nearly upright: outline the open rim
                out.add(VMobject(stroke_color=INK, stroke_width=3).set_points_as_corners(
                    [P(0, 0, t), P(w, 0, t), P(w, w, t), P(0, w, t), P(0, 0, t)]))
            return out
        return always_redraw(draw)

    def can(self, r=1.0, h=2.2):
        """A closed cylinder as a student would sketch it: top ellipse, sides, bottom ellipse with its back half dashed,
        a radius on the top and the height along the side. Returns (group, top_and_bottom, side)."""
        e = 0.32
        top = Ellipse(width=2 * r, height=2 * r * e, stroke_color=INK, stroke_width=3, fill_color=CARD_LT, fill_opacity=0.9).shift(UP * h / 2)
        bot_front = Arc(radius=r, start_angle=PI, angle=PI, stroke_color=INK, stroke_width=3).stretch(e, 1).shift(DOWN * h / 2)
        bot_back = DashedVMobject(Arc(radius=r, start_angle=0, angle=PI, stroke_color=DIM, stroke_width=2).stretch(e, 1).shift(DOWN * h / 2), num_dashes=12)
        side = Polygon(LEFT * r + UP * h / 2, LEFT * r + DOWN * h / 2, RIGHT * r + DOWN * h / 2, RIGHT * r + UP * h / 2,
                       stroke_width=0, fill_color=CARD, fill_opacity=0.55)
        walls = VGroup(Line(LEFT * r + UP * h / 2, LEFT * r + DOWN * h / 2, color=INK, stroke_width=3),
                       Line(RIGHT * r + UP * h / 2, RIGHT * r + DOWN * h / 2, color=INK, stroke_width=3))
        rad = Line(UP * h / 2, UP * h / 2 + RIGHT * r, color=SECANT, stroke_width=3)
        labs = VGroup(M("r", 32, SECANT).next_to(rad, UP, buff=0.08), M("h", 32, SECANT).next_to(walls[1], RIGHT, buff=0.15))
        g = VGroup(side, bot_back, bot_front, walls, top, rad, Dot(UP * h / 2, radius=0.04, color=INK), labs)
        return g, VGroup(top, bot_front), side

    def construct(self):
        X = ValueTracker(2)
        F = ValueTracker(0)
        sh = self.sheet(X, LEFT * 4)
        bx = self.box(X, RIGHT * 1.2 + DOWN * 0.4, fold=F)
        V = lambda x: x * (12 - 2 * x)**2
        read = always_redraw(lambda: VGroup(M(rf"x = {X.get_value():.1f}\ \text{{in}}", 36, DIM), M(rf"V = {V(X.get_value()):.0f}\ \text{{in}}^3", 40, FUNC))
                             .arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.6).shift(UP * 1.5))
        with self.beat("Folding a box") as b:
            self.add(sh, bx)
            self.wait(1)
            self.play(F.animate.set_value(90), run_time=3, rate_func=rate_functions.ease_in_out_sine)
            self.play(FadeIn(read), run_time=0.6)
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
        la, ll = plot_axes([-1, 4, 1], [-1, 4, 1], w=4.4, h=4.4)
        P0 = ValueTracker(-0.5)
        lfig = VGroup(la, ll, la.plot(lambda s: s + 1, x_range=[-1, 3], color=FUNC, stroke_width=4), Dot(la.c2p(3, 0), color=SECANT),
                      M("(3, 0)", 28, SECANT).next_to(la.c2p(3, 0), UP, buff=0.15))
        seg = always_redraw(lambda: VGroup(DashedLine(la.c2p(3, 0), la.c2p(P0.get_value(), P0.get_value() + 1), color=TANGENT),
                                           Dot(la.c2p(P0.get_value(), P0.get_value() + 1), color=TANGENT)))
        self.example("Closest point", r"Find the point on the line $y = x + 1$ closest to $(3, 0)$.",
                     [r"TEXT:A point on the line: $(x, x + 1)$.", r"D^2 = (x - 3)^2 + (x + 1)^2", r"= x^2 - 6x + 9 + x^2 + 2x + 1 = 2x^2 - 4x + 10", r"\left(D^2\right)' = 4x - 4",
                      r"4x - 4 = 0, \ \ x = 1", r"\text{second derivative } 4 > 0: \ \text{minimum}", r"y = 1 + 1 = 2: \ \text{the point } (1, 2)",
                      r"D = \sqrt{(1 - 3)^2 + 2^2} = \sqrt8 = 2\sqrt2"], at=[1, 2, 3, 4, 4, 5, 6, 6], figure=lfig,
                     cues={0: lambda sc: (sc.add(seg), sc.play(P0.animate.set_value(2.5), run_time=1.2), sc.play(P0.animate.set_value(0), run_time=1)),
                           6: lambda sc: sc.play(P0.animate.set_value(1), run_time=0.8)})

        with self.beat("Close") as b:
            X2 = ValueTracker(2)
            bx2 = self.box(X2, UP * 0.6)
            self.add(bx2)
            self.play(FadeIn(M(r"x = 2\ \text{in},\ \ V = 128\ \text{in}^3", 44, FUNC).shift(DOWN * 2)), run_time=0.8)
        self.clear()

        self.examples_card()
        Xb = ValueTracker(2)
        bfig = self.box(Xb, ORIGIN, k=0.3)
        bfig.clear_updaters()                           # a still sketch: the example helper moves it into place
        blabs = VGroup(M("x", 30, SECANT), M("12 - 2x", 28, SECANT), M("12 - 2x", 28, SECANT))
        bfig = VGroup(bfig, blabs)
        blabs[0].next_to(bfig[0], LEFT, buff=0.1)
        blabs[1].next_to(bfig[0], DOWN, buff=0.1).shift(LEFT * 0.5)
        blabs[2].next_to(bfig[0], RIGHT, buff=0.1).shift(DOWN * 0.4)
        self.example("Example 1: The open box",
                     r"An open box is made from a $12 \times 12$ inch sheet by cutting squares of side $x$ from the corners. What $x$ gives the largest volume, and what is that volume? (Volume $=$ length $\times$ width $\times$ height.)",
                     [r"V(x) = x(12 - 2x)^2", r"\text{domain: } 0 \le x \le 6", r"V'(x) = (12 - 2x)^2 + x \cdot 2(12 - 2x)(-2)",
                      r"= (12 - 2x)\left[(12 - 2x) - 4x\right] = (12 - 2x)(12 - 6x)", r"12 - 2x = 0 \text{ or } 12 - 6x = 0: \ \ x = 6 \text{ or } x = 2",
                      r"V(0) = 0, \ \ V(2) = 2 \cdot 8^2 = 128, \ \ V(6) = 0", r"x = 2 \text{ in},\ \ V = 128\ \text{in}^3"],
                     at=[1, 2, 3, 4, 5, 6, 7], figure=bfig)
        ra2, rl2 = plot_axes([0, 4, 1], [-0.5, 2.5, 1], w=4.6, h=3)
        cx = 2.5
        rfig2 = VGroup(ra2, rl2, ra2.plot(np.sqrt, x_range=[0.001, 4], color=FUNC, stroke_width=4), Dot(ra2.c2p(3, 0), color=SECANT),
                       M("(3, 0)", 26, SECANT).next_to(ra2.c2p(3, 0), DOWN, buff=0.12))
        dseg = VGroup(DashedLine(ra2.c2p(3, 0), ra2.c2p(cx, np.sqrt(cx)), color=TANGENT), Dot(ra2.c2p(cx, np.sqrt(cx)), color=TANGENT),
                      M("D", 28, TANGENT).next_to(ra2.c2p(2.75, np.sqrt(cx) / 2), RIGHT, buff=0.1))
        rfig2.add(dseg)
        self.example("Example 2: The closest point", r"Find the point on $y = \sqrt{x}$ closest to $(3, 0)$.",
                     [r"D^2 = (x - 3)^2 + \left(\sqrt x\right)^2", r"= x^2 - 6x + 9 + x = x^2 - 5x + 9", r"\left(D^2\right)' = 2x - 5",
                      r"2x - 5 = 0, \ \ x = \frac52", r"\text{second derivative } 2 > 0,\ \text{only critical point: minimum}",
                      r"\left(\frac52, \sqrt{\frac52}\right), \ \ D^2 = \frac{25}{4} - \frac{25}{2} + 9 = \frac{11}{4}, \ \ D = \frac{\sqrt{11}}{2}"],
                     at=[1, 2, 3, 3, 4, 5], figure=rfig2,
                     notes_graph=dict(fns=[("sqrt(x)", 0, 4)], xr=(0, 4), yr=(-0.5, 2.5), closed=[(3, 0)]))
        cyl, ends, side = self.can()
        self.example("Example 3: The can", r"A closed cylindrical can holds $16\pi$ in$^3$. What radius and height use the least material? (For a cylinder, $V = \pi r^2 h$ and $S = 2\pi r^2 + 2\pi r h$.)",
                     [r"\pi r^2 h = 16\pi", r"h = \frac{16}{r^2}", r"S = 2\pi r^2 + 2\pi r h = 2\pi r^2 + 2\pi r \cdot \frac{16}{r^2} = 2\pi r^2 + \frac{32\pi}{r}",
                      r"S' = 4\pi r - \frac{32\pi}{r^2}", r"4\pi r = \frac{32\pi}{r^2}, \ \ 4\pi r^3 = 32\pi, \ \ r^3 = 8, \ \ r = 2",
                      r"S'' = 4\pi + \frac{64\pi}{r^3} > 0: \ \text{only critical point, minimum}", r"h = \frac{16}{2^2} = 4: \ \ r = 2 \text{ in}, \ h = 4 \text{ in}"],
                     at=[1, 2, 3, 4, 4, 5, 6], figure=cyl,
                     cues={2: lambda sc: (sc.play(Indicate(ends, color=SECANT), run_time=0.8), sc.play(Indicate(side, color=SECANT), run_time=0.8))})
        self.finish()
