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


class UnitCircle(VGroup):
    """A unit circle with axes. pt(theta) is the point at that angle; arc(a, b) a highlighted piece of it."""

    def __init__(self, r=2.5, center=LEFT * 3.5 + DOWN * 0.4, **kw):
        super().__init__(**kw)
        self.r, self.c = r, np.array(center, dtype=float)
        self.add(Line(self.c + LEFT * (r + 0.4), self.c + RIGHT * (r + 0.4), color=DIM, stroke_width=2),
                 Line(self.c + DOWN * (r + 0.4), self.c + UP * (r + 0.4), color=DIM, stroke_width=2),
                 Circle(radius=r, color=INK, stroke_width=3).move_to(self.c))

    def pt(self, th):
        return self.c + self.r * np.array([np.cos(th), np.sin(th), 0.0])

    def dot(self, th, color=FUNC):
        return Dot(self.pt(th), radius=0.11, color=color)

    def hole(self, th, color=DERIV):
        return Circle(radius=0.1, color=color, stroke_width=4, fill_color=BG, fill_opacity=1).move_to(self.pt(th))

    def arc(self, a, b, color=DERIV):
        return Arc(radius=self.r, start_angle=a, angle=b - a, arc_center=self.c, color=color, stroke_width=11)

    def label(self, th, tex, color=INK, size=34, out=0.5):
        return M(tex, size, color).move_to(self.c + (self.r + out) * np.array([np.cos(th), np.sin(th), 0.0]))


def range_card(name, ins, outs):
    """What an inverse trig function takes and gives back."""
    rows = VGroup(M(name, 52, DERIV), M(r"\text{inputs: }" + ins, 44), M(r"\text{outputs: }" + outs, 44)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    return formula_box(rows, DERIV, buff=0.3).move_to(RIGHT * 3.4 + DOWN * 1.8)


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

        # ---------------- a reminder of the inverse trig functions themselves (Adder, 3.4 review)
        with self.beat("Undoing sine") as b:
            uc = UnitCircle()
            self.play(Create(uc), run_time=1)
            p1 = uc.dot(PI / 6)
            h1 = Line([uc.pt(PI / 6)[0], uc.c[1], 0], uc.pt(PI / 6), color=FUNC, stroke_width=6)
            lab1 = M(r"\tfrac{\pi}{6}", 42).next_to(p1, RIGHT, buff=0.15)
            half = M(r"\tfrac12", 40, FUNC).next_to(h1, LEFT, buff=0.12)
            self.play(Create(h1), FadeIn(p1), FadeIn(lab1), FadeIn(half), run_time=1)
            b.line(1)
            p2 = uc.dot(5 * PI / 6)
            h2 = Line([uc.pt(5 * PI / 6)[0], uc.c[1], 0], uc.pt(5 * PI / 6), color=FUNC, stroke_width=6)
            lab2 = M(r"\tfrac{5\pi}{6}", 42).next_to(p2, LEFT, buff=0.15)
            level = DashedLine(uc.pt(5 * PI / 6) + LEFT * 0.5, uc.pt(PI / 6) + RIGHT * 0.3, color=DIM, stroke_width=2)
            eq = M(r"\sin\tfrac{\pi}{6} = \sin\tfrac{5\pi}{6} = \tfrac12", 52).move_to(RIGHT * 3.4 + UP * 2.6)
            self.play(Create(h2), FadeIn(p2), FadeIn(lab2), Create(level), FadeIn(eq), run_time=1)
            not11 = T("Sine is not one-to-one.", 44, TANGENT).next_to(eq, DOWN, buff=0.45)
            self.play(FadeIn(not11), run_time=0.6)
            b.line(2)
            keep = uc.arc(-PI / 2, PI / 2)
            top = M(r"\tfrac{\pi}{2}", 42, DERIV).next_to(uc.pt(PI / 2), UR, buff=0.1)
            bot = M(r"-\tfrac{\pi}{2}", 42, DERIV).next_to(uc.pt(-PI / 2), DR, buff=0.1)
            self.play(Create(keep), FadeIn(top), FadeIn(bot), VGroup(p2, h2, lab2, level).animate.set_opacity(0.2), run_time=1.4)
            b.line(3)
            self.play(FadeIn(range_card(r"\arcsin x", r"-1 \le x \le 1", r"-\tfrac{\pi}{2} \le \arcsin x \le \tfrac{\pi}{2}")), run_time=0.8)
        self.clear()

        with self.beat("Undoing cosine") as b:
            uc = UnitCircle()
            self.play(Create(uc), run_time=0.8)
            b.line(1)
            parts = VGroup()
            for th, side in ((PI / 3, UR), (-PI / 3, DR)):
                d = uc.dot(th)
                seg = Line([uc.c[0], uc.pt(th)[1], 0], uc.pt(th), color=FUNC, stroke_width=6)
                h = M(r"\tfrac12", 40, FUNC).next_to(seg, UP if th > 0 else DOWN, buff=0.1)
                lab = M(r"\tfrac{\pi}{3}" if th > 0 else r"-\tfrac{\pi}{3}", 42).next_to(d, side, buff=0.1)
                parts.add(VGroup(seg, d, h, lab))
            level = DashedLine(uc.pt(-PI / 3) + DOWN * 0.4, uc.pt(PI / 3) + UP * 0.4, color=DIM, stroke_width=2)
            eq = M(r"\cos\tfrac{\pi}{3} = \cos\left(-\tfrac{\pi}{3}\right) = \tfrac12", 52).move_to(RIGHT * 3.4 + UP * 2.6)
            self.play(Create(parts[0][0]), Create(parts[1][0]), *[FadeIn(VGroup(*p[1:])) for p in parts], Create(level), FadeIn(eq), run_time=1.2)
            b.line(2)
            keep = uc.arc(0, PI)
            zero = M("0", 42, DERIV).next_to(uc.pt(0), UR, buff=0.1)
            pi_ = M(r"\pi", 42, DERIV).next_to(uc.pt(PI), UL, buff=0.1)
            self.play(Create(keep), FadeIn(zero), FadeIn(pi_), VGroup(parts[1], level).animate.set_opacity(0.2), run_time=1.4)
            b.line(3)
            self.play(FadeIn(range_card(r"\arccos x", r"-1 \le x \le 1", r"0 \le \arccos x \le \pi")), run_time=0.8)
        self.clear()

        with self.beat("Undoing tangent") as b:
            uc = UnitCircle()
            self.play(Create(uc), run_time=0.8)
            u = np.array([np.cos(PI / 4), np.sin(PI / 4), 0.0])
            ray = Line(uc.c - u * (uc.r + 0.6), uc.c + u * (uc.r + 0.6), color=SECANT, stroke_width=5)
            slope = M(r"\text{slope } 1", 38, SECANT).next_to(ray.get_end(), RIGHT, buff=0.12)
            self.play(Create(ray), FadeIn(slope), run_time=1)
            b.line(1)
            d1, d2 = uc.dot(PI / 4), uc.dot(5 * PI / 4)
            l1 = M(r"\tfrac{\pi}{4}", 42).next_to(d1, UL, buff=0.08)
            l2 = M(r"\tfrac{5\pi}{4}", 42).next_to(d2, UL, buff=0.1)
            eq = M(r"\tan\tfrac{\pi}{4} = \tan\tfrac{5\pi}{4} = 1", 52).move_to(RIGHT * 3.4 + UP * 2.6)
            self.play(FadeIn(d1), FadeIn(d2), FadeIn(l1), FadeIn(l2), FadeIn(eq), run_time=1)
            b.line(2)
            keep = uc.arc(-PI / 2, PI / 2)
            holes = VGroup(uc.hole(PI / 2), uc.hole(-PI / 2))
            top = M(r"\tfrac{\pi}{2}", 42, DERIV).next_to(uc.pt(PI / 2), UR, buff=0.12)
            bot = M(r"-\tfrac{\pi}{2}", 42, DERIV).next_to(uc.pt(-PI / 2), DR, buff=0.12)
            note = T("No slope straight up or down.", 42, DIM).next_to(eq, DOWN, buff=0.45)
            self.play(Create(keep), FadeIn(holes), FadeIn(top), FadeIn(bot), FadeIn(note), VGroup(d2, l2).animate.set_opacity(0.2), run_time=1.4)
            b.line(3)
            self.play(FadeIn(range_card(r"\arctan x", r"\text{every real } x", r"-\tfrac{\pi}{2} < \arctan x < \tfrac{\pi}{2}")), run_time=0.8)
        self.clear()

        with self.beat("Arcsecant, briefly") as b:
            eq = M(r"\sec x = \frac{1}{\cos x}, \text{ so } \operatorname{arcsec} x = \arccos\frac{1}{x}", 50).set_max_width(7.2).move_to(RIGHT * 3.3 + UP * 2.4)
            self.play(FadeIn(eq), run_time=0.8)
            b.line(1)
            uc = UnitCircle()
            keep = uc.arc(0, PI)
            zero = M("0", 42, DERIV).next_to(uc.pt(0), UR, buff=0.1)
            pi_ = M(r"\pi", 42, DERIV).next_to(uc.pt(PI), UL, buff=0.1)
            gap = M(r"\tfrac{\pi}{2}", 42, DIM).next_to(uc.pt(PI / 2), UR, buff=0.12)
            self.play(Create(uc), Create(keep), FadeIn(zero), FadeIn(pi_), run_time=1.2)
            self.play(FadeIn(uc.hole(PI / 2)), FadeIn(gap), run_time=0.6)
            b.line(2)
            self.play(FadeIn(range_card(r"\operatorname{arcsec} x", r"x \le -1 \text{ or } x \ge 1", r"0 \text{ to } \pi, \text{ but not } \tfrac{\pi}{2}")), run_time=0.8)
        self.clear()

        with self.beat("Domains and ranges") as b:
            head = T("Domains and ranges", 52).to_edge(UP, buff=0.5)
            tab = table([r"\text{function}", r"\text{inputs (domain)}", r"\text{outputs (range)}", r"\text{piece of the circle}"],
                        [[r"\arcsin x", r"-1 \le x \le 1", r"\left[-\tfrac{\pi}{2}, \tfrac{\pi}{2}\right]", r"\text{right half}"],
                         [r"\arccos x", r"-1 \le x \le 1", r"[0, \pi]", r"\text{top half}"],
                         [r"\arctan x", r"\text{every real } x", r"\left(-\tfrac{\pi}{2}, \tfrac{\pi}{2}\right)", r"\text{right half, no ends}"],
                         [r"\operatorname{arcsec} x", r"|x| \ge 1", r"[0, \pi], \text{ not } \tfrac{\pi}{2}", r"\text{top half, no top}"]], size=44)
            tab.set_max_width(13.4).next_to(head, DOWN, buff=0.7)
            self.play(FadeIn(head), FadeIn(tab), run_time=1.2)
            b.line(1)
            box = SurroundingRectangle(VGroup(*[tab.cells[r][2] for r in range(5)]), color=DERIV, buff=0.15, corner_radius=0.1)
            self.play(Create(box), *[tab.cells[r][2].animate.set_color(DERIV) for r in range(1, 5)], run_time=1)
        self.clear()

        with self.beat("Try a few") as b:
            uc = UnitCircle()
            self.play(Create(uc), run_time=0.8)
            qs = [(r"\arcsin\tfrac12 =", r"\tfrac{\pi}{6}", (-PI / 2, PI / 2), PI / 6, UR),
                  (r"\arccos\left(-\tfrac{\sqrt2}{2}\right) =", r"\tfrac{3\pi}{4}", (0, PI), 3 * PI / 4, UL),
                  (r"\arctan(-1) =", r"-\tfrac{\pi}{4}", (-PI / 2, PI / 2), -PI / 4, RIGHT),
                  (r"\arcsin(-1) =", r"-\tfrac{\pi}{2}", (-PI / 2, PI / 2), -PI / 2, DR)]
            shown = VGroup()
            for k, (q, a, (lo, hi), th, side) in enumerate(qs):
                b.line(1 + 2 * k)
                qm = M(q, 52).move_to(RIGHT * 0.6 + UP * (2.6 - 1.6 * k), aligned_edge=LEFT)
                old = [FadeOut(shown)] if len(shown) else []
                keep = uc.arc(lo, hi)
                shown = VGroup(keep)
                if th == -PI / 4:                           # arctangent: the ends of the half are not included
                    shown.add(uc.hole(PI / 2), uc.hole(-PI / 2))
                self.play(FadeIn(qm), *[Create(m) if m is keep else FadeIn(m) for m in shown], *old, run_time=0.9)
                b.line(2 + 2 * k)
                d = uc.dot(th, TANGENT)
                lab = M(a, 42, TANGENT).next_to(d, side, buff=0.1)
                cross = None
                if th == -PI / 4:
                    u = np.array([np.cos(th), np.sin(th), 0.0])
                    ray = Line(uc.c - u * (uc.r + 0.5), uc.c + u * (uc.r + 0.5), color=SECANT, stroke_width=4)
                    ghost = uc.dot(3 * PI / 4, DIM)
                    glab = M(r"\tfrac{3\pi}{4}", 42, DIM).next_to(ghost, UL, buff=0.1)
                    cross = Cross(VGroup(ghost, glab), stroke_color=TANGENT, stroke_width=4, scale_factor=0.9)
                    shown.add(ray, ghost, glab, cross)
                    self.play(Create(ray), run_time=0.6)
                ans = M(a, 52, DERIV).next_to(qm, RIGHT, buff=0.2)
                shown.add(d, lab)
                self.play(FadeIn(d), FadeIn(lab), Write(ans), run_time=0.9)
                if cross is not None:
                    self.play(FadeIn(ghost), FadeIn(glab), run_time=0.5)
                    self.play(Create(cross), run_time=0.6)
        self.clear()

        with self.beat("Differentiate implicitly") as b:
            board = Board()
            board.anchor = UP * 3.0
            board.write(self, r"y = \arcsin x, \ \text{so} \ \sin y = x")
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
            board.write(self, r"y = \arctan x, \ \text{so} \ \tan y = x")
            b.line(1)
            board.write(self, r"\sec^2 y\,\frac{dy}{dx} = 1")
            b.line(2)
            board.write(self, r"\sec^2 y = 1 + \tan^2 y = 1 + x^2")
            b.line(3)
            board.write(self, r"\frac{d}{dx}\arctan x = \frac{1}{1 + x^2}", color=DERIV)
        self.clear()

        # the chart, in Adder's order: arcsin, arcsec, arctan down the left; their co-functions, the negatives, down the right
        D = r"\frac{d}{dx}\,"
        left = [M(D + r"\mathrm{arc}", r"\mathrm{s}", r"\mathrm{in}\, x =", r"\frac{1}{\sqrt{1", "-", r"x^2}}", 50),
                M(D + r"\mathrm{arc}", r"\mathrm{s}", r"\mathrm{ec}\, x =", r"\frac{1}{|x|\sqrt{x^2", "-", r"1}}", 50),
                M(D + r"\mathrm{arctan}\, x =", r"\frac{1}{1", "+", r"x^2}", 50)]
        right = [M(D + r"\mathrm{arccos}\, x =", "-", r"\frac{1}{\sqrt{1 - x^2}}", 50),
                 M(D + r"\mathrm{arccsc}\, x =", "-", r"\frac{1}{|x|\sqrt{x^2 - 1}}", 50),
                 M(D + r"\mathrm{arccot}\, x =", "-", r"\frac{1}{1 + x^2}", 50)]
        for m in left[:2]:
            VGroup(*m[3:]).set_color(DERIV)
        VGroup(*left[2][1:]).set_color(DERIV)
        for m in right:
            VGroup(*m[1:]).set_color(DERIV)
        grid = VGroup(*[c for pair in zip(left, right) for c in pair]).arrange_in_grid(3, 2, buff=(1.2, 0.55), col_alignments="ll")
        grid.move_to(UP * 0.55)
        with self.beat("All six derivatives") as b:
            for m in left:
                self.play(FadeIn(m), run_time=0.6)
            b.line(1)
            self.play(Indicate(left[1], color=DERIV, scale_factor=1.06), run_time=1)
            b.line(2)
            for m in right:
                self.play(FadeIn(m), run_time=0.6)
            b.line(3)
            memo = T("Memorize these.", 50, SECANT).next_to(grid, UP, buff=0.4)
            self.play(FadeIn(memo, shift=DOWN * 0.2), run_time=0.8)

        with self.beat("Remembering them") as b:
            signs = [m[1] for m in right]
            self.play(*[m.animate.set_color(TANGENT) for m in signs], run_time=0.4)
            self.play(*[Indicate(m, color=TANGENT, scale_factor=1.8) for m in signs], run_time=1.2)
            b.line(1)
            subs = [left[0][1], left[0][4], left[1][1], left[1][4]]
            self.play(*[m.animate.set_color(SECANT) for m in subs], run_time=0.4)
            self.play(*[Indicate(m, color=SECANT, scale_factor=1.8) for m in subs], run_time=1.2)
            tip = T(r"\textbf{S} for subtraction: arc\textbf{s}in, arc\textbf{s}ec", 44, SECANT).next_to(grid, DOWN, buff=0.55).align_to(grid, LEFT)
            self.play(FadeIn(tip), run_time=0.6)
            b.line(2)
            self.play(left[2][2].animate.set_color(FUNC), run_time=0.4)
            self.play(Indicate(left[2][2], color=FUNC, scale_factor=1.8), run_time=1.2)
            b.line(3)
            ch = M(r"\frac{d}{dx}\arctan\big(u(x)\big) = \frac{u'(x)}{1 + u(x)^2}", 46, SECANT).next_to(grid, DOWN, buff=0.45).align_to(grid, RIGHT)
            self.play(Write(ch), run_time=1.2)
        self.clear()
        self.example("Arcsine with the chain rule", r"Find $\dfrac{d}{dx}\arctan(3x)$ and $\dfrac{d}{dx}\arcsin\left(x^2\right)$.",
                     [r"u = 3x,\ u' = 3: \quad \frac{1}{1 + u^2}\cdot u' = \frac{3}{1 + 9x^2}", r"u = x^2,\ u' = 2x: \quad \frac{1}{\sqrt{1 - u^2}}\cdot u' = \frac{2x}{\sqrt{1 - x^4}}"], at=[1, 2])

        # the absolute value in arcsecant: even powers drop it, odd powers keep it (Adder, 3.4 review)
        sec_rule = r"\frac{d}{dx}\operatorname{arcsec} u = \frac{u'}{|u|\sqrt{u^2 - 1}}"
        self.example("Arcsecant of x squared", r"Find $\dfrac{d}{dx}\operatorname{arcsec}\left(x^2\right)$.",
                     [r"u = x^2,\ u' = 2x: \quad \frac{2x}{\left|x^2\right|\sqrt{x^4 - 1}}",
                      r"TEXT:$x^2$ is never negative, so $\left|x^2\right| = x^2$.",
                      r"\frac{2x}{x^2\sqrt{x^4 - 1}} = \frac{2}{x\sqrt{x^4 - 1}}"], at=[1, 2, 3], follow=True, ref=sec_rule)
        self.example("Arcsecant of x cubed", r"Find $\dfrac{d}{dx}\operatorname{arcsec}\left(x^3\right)$.",
                     [r"u = x^3,\ u' = 3x^2: \quad \frac{3x^2}{\left|x^3\right|\sqrt{x^6 - 1}}",
                      r"TEXT:$x^3$ has the same sign as $x$, so $\left|x^3\right| = x^2|x|$.",
                      r"\frac{3x^2}{x^2|x|\sqrt{x^6 - 1}} = \frac{3}{|x|\sqrt{x^6 - 1}}",
                      r"TEXT:Even powers: $\left|x^2\right| = x^2$. Odd powers keep the sign of $x$, so the absolute value stays."],
                     at=[1, 2, 3, 4], ref=sec_rule)

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
                     [r"\arctan 1 = \frac{\pi}{4}, \ \text{so the point is} \ \left(1, \frac{\pi}{4}\right)", r"\frac{1}{1 + 1^2} = \frac12", r"y - \frac{\pi}{4} = \frac12(x - 1)"],
                     figure=fig, at=[1, 2, 3])
        self.finish()
