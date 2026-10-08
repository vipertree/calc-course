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

        with self.beat("N and D") as b:
            frac = M(r"\frac{dy}{dx}", r"=", r"\frac{N}{D}", 64).shift(UP * 2.3)
            self.play(Write(frac), run_time=1)
            b.line(1)
            nb = SurroundingRectangle(frac[2][0], color=TANGENT, buff=0.08)
            db = SurroundingRectangle(frac[2][2], color=DERIV, buff=0.08)
            names = VGroup(T("N: numerator", 32, TANGENT), T("D: denominator", 32, DERIV)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(frac, RIGHT, buff=0.8)
            self.play(Create(nb), Create(db), FadeIn(names), run_time=1)
            b.line(2)
            c1 = VGroup(M(r"N = 0,\ D \ne 0", 40, TANGENT), Line(LEFT, RIGHT, color=TANGENT, stroke_width=6), T("slope 0: horizontal tangent", 30)).arrange(DOWN, buff=0.4)
            c2 = VGroup(M(r"D = 0,\ N \ne 0", 40, DERIV), Line(DOWN * 0.8, UP * 0.8, color=DERIV, stroke_width=6), T(r"slope $\to \infty$: vertical tangent", 30)).arrange(DOWN, buff=0.3)
            VGroup(c1, c2).arrange(RIGHT, buff=2.2).shift(DOWN * 0.6)
            self.play(FadeIn(c1), run_time=0.8)
            b.line(3)
            q = T("What makes the slope go off to infinity?", 36, SECANT).move_to(c2)
            self.play(FadeIn(q), run_time=0.6)
            b.line(4)
            self.play(FadeOut(q), run_time=0.3)
            tilt = ValueTracker(20)
            spin = always_redraw(lambda: Line(DOWN * 0.8, UP * 0.8, color=DERIV, stroke_width=6).rotate(-np.radians(90 - tilt.get_value())).move_to(c2[1]))
            self.add(spin)
            self.play(FadeIn(c2[0]), run_time=0.5)
            self.play(tilt.animate.set_value(90), run_time=1.6)
            self.remove(spin)
            self.add(c2[1])
            self.play(FadeIn(c2[2]), run_time=0.5)
            b.line(5)
            both = T(r"$N = 0$ and $D = 0$: look more closely", 30, DIM).to_edge(DOWN, buff=0.5)
            self.play(FadeIn(both), run_time=0.6)
        self.clear()

        ax, al = plot_axes([-6, 6, 2], [-6, 6, 2], w=5.6, h=5.6, coords=False)
        VGroup(ax, al).to_edge(LEFT, buff=1).shift(DOWN * 0.1)
        with self.beat("Back to the curve") as b:
            circ = Circle(radius=ax.c2p(5, 0)[0] - ax.c2p(0, 0)[0], color=FUNC, stroke_width=5).move_to(ax.c2p(0, 0))
            self.play(FadeIn(ax), FadeIn(al), Create(circ), run_time=1)
            note = VGroup(M(r"\frac{dy}{dx} = -\frac{x}{y}", 44), M(r"N = 0:\ x = 0", 40, SECANT)).arrange(DOWN, buff=0.4).to_edge(RIGHT, buff=1).shift(UP * 1)
            line = DashedLine(ax.c2p(0, -6), ax.c2p(0, 6), color=SECANT)
            self.play(FadeIn(note), Create(line), run_time=1)
            b.line(1)
            pts = VGroup(Dot(ax.c2p(0, 5), color=TANGENT, radius=0.1), Dot(ax.c2p(0, -5), color=TANGENT, radius=0.1))
            lab = M(r"(0, 5),\ (0, -5)", 40, TANGENT).next_to(note, DOWN, buff=0.6)
            self.play(FadeIn(pts), FadeIn(lab), run_time=0.8)
        self.clear()

        hx, hl = plot_axes([-4, 4, 1], [-4, 4, 1], w=5.6, h=5.6, coords=False)
        VGroup(hx, hl).to_edge(LEFT, buff=1).shift(DOWN * 0.1)
        with self.beat("Not on the curve") as b:
            hyp = VGroup(hx.plot(lambda s: 1 / s, x_range=[0.25, 4], color=FUNC, stroke_width=5), hx.plot(lambda s: 1 / s, x_range=[-4, -0.25], color=FUNC, stroke_width=5))
            eqs = VGroup(M(r"xy = 1", 44), M(r"\frac{dy}{dx} = -\frac{y}{x}", 44), M(r"D = x", 40, DERIV)).arrange(DOWN, buff=0.4).to_edge(RIGHT, buff=1.2).shift(UP * 1.2)
            self.play(FadeIn(hx), FadeIn(hl), Create(hyp), FadeIn(eqs[0]), run_time=1.2)
            self.play(FadeIn(eqs[1]), run_time=0.6)
            b.line(1)
            dl = DashedLine(hx.c2p(0, -4), hx.c2p(0, 4), color=DERIV)
            self.play(FadeIn(eqs[2]), Create(dl), FadeIn(T("$D = 0$ here", 28, DERIV).next_to(hx.c2p(0, 3.6), RIGHT, buff=0.15)), run_time=0.8)
            b.line(2)
            chk = M(r"x = 0:\ \ xy = 0 \ne 1", 40, TANGENT).next_to(eqs, DOWN, buff=0.6)
            self.play(FadeIn(chk), run_time=0.8)
            b.line(3)
            no = VGroup(T("no point of the curve has $x = 0$:", 30, TANGENT), T("no tangent line at all", 30, TANGENT)).arrange(DOWN, buff=0.12).next_to(chk, DOWN, buff=0.5)
            self.play(FadeIn(no), run_time=0.8)
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
            card = VGroup(M(r"\text{Horizontal: } N = 0", 46, TANGENT), M(r"\text{Vertical: } D = 0", 46, DERIV), T("Then solve with the curve's equation,", 40, SECANT),
                          T("and check the point is on the curve.", 40, SECANT)).arrange(DOWN, buff=0.45)
            self.play(FadeIn(card), run_time=1)
        self.clear()

        self.examples_card()
        self.example("Example 1: A shifted circle",
                     r"Find the points on $x^2 + y^2 - 4x + 6y = 12$ where the tangent is horizontal, and where it is vertical.",
                     [r"2x + 2yy' - 4 + 6y' = 0", r"y'(2y + 6) = 4 - 2x, \ \ y' = \frac{2 - x}{y + 3}", r"N = 2 - x, \ \ D = y + 3",
                      r"N = 0: \ x = 2, \ \ 4 + y^2 - 8 + 6y = 12", r"y^2 + 6y - 16 = 0, \ \ (y + 8)(y - 2) = 0", r"\text{horizontal at } (2, 2),\ (2, -8) \ \ (D \ne 0)",
                      r"D = 0: \ y = -3, \ \ x^2 + 9 - 4x - 18 = 12", r"x^2 - 4x - 21 = 0, \ \ (x - 7)(x + 3) = 0", r"\text{vertical at } (7, -3),\ (-3, -3) \ \ (N \ne 0)"],
                     at=[1, 2, 2, 3, 3, 4, 5, 5, 6])
        self.example("Example 2: A cubic curve", r"Find the points on $y^2 = x^3 - 3x + 3$ where the tangent is horizontal.",
                     [r"2yy' = 3x^2 - 3, \ \ y' = \frac{3x^2 - 3}{2y}", r"N = 0: \ 3x^2 = 3, \ \ x^2 = 1, \ \ x = \pm 1", r"x = 1:\ y^2 = 1 - 3 + 3 = 1:\ (1, 1),\ (1, -1)",
                      r"x = -1:\ y^2 = -1 + 3 + 3 = 5:\ \left(-1, \sqrt5\right),\ \left(-1, -\sqrt5\right)", r"D = 2y \ne 0 \text{ at all four}"], at=[1, 2, 3, 4, 4])
        self.example("Example 3: Which way it bends",
                     r"On $y^2 = x^3 - 3x + 3$, find $\dfrac{d^2y}{dx^2}$ at $(1, 1)$. What does the curve have there?",
                     [r"2y' \cdot y' + 2y \cdot y'' = 6x", r"(1, 1):\ y' = 0, \ \ 0 + 2y'' = 6, \ \ y'' = 3 > 0", r"\text{horizontal tangent, concave up: relative minimum}"], at=[1, 2, 3])
        ex, el = plot_axes([-4, 4, 1], [-4, 4, 1], w=4.6, h=4.6)
        up = lambda s: (-s + np.sqrt(max(28 - 3 * s * s, 0))) / 2
        dn = lambda s: (-s - np.sqrt(max(28 - 3 * s * s, 0))) / 2
        xm = np.sqrt(28 / 3)
        efig = VGroup(ex, el, ex.plot(up, x_range=[-xm, xm, 0.005], color=FUNC, stroke_width=4), ex.plot(dn, x_range=[-xm, xm, 0.005], color=FUNC, stroke_width=4),
                      DashedLine(ex.c2p(1, -4), ex.c2p(1, 4), color=DIM))
        t1 = ex.plot(lambda s: 2 - 0.8 * (s - 1), x_range=[-1.2, 3.2], color=TANGENT, stroke_width=3)
        t2 = ex.plot(lambda s: -3 - 0.2 * (s - 1), x_range=[-2.5, 4], color=TANGENT, stroke_width=3)
        self.example("Example 4: Two tangent lines at one x", r"Find the equations of all lines tangent to $x^2 + xy + y^2 = 7$ at $x = 1$.",
                     [r"1 + y + y^2 = 7", r"y^2 + y - 6 = 0, \ \ (y + 3)(y - 2) = 0: \ \ (1, 2),\ (1, -3)", r"2x + y + xy' + 2yy' = 0",
                      r"y'(x + 2y) = -(2x + y), \ \ y' = -\frac{2x + y}{x + 2y}", r"(1, 2): \ y' = -\frac{2 + 2}{1 + 4} = -\frac45",
                      r"(1, -3): \ y' = -\frac{2 - 3}{1 - 6} = -\frac15", r"y - 2 = -\tfrac45(x - 1), \ \ y + 3 = -\tfrac15(x - 1)"],
                     at=[1, 2, 3, 4, 5, 6, 7], figure=efig,
                     cues={1: lambda sc: sc.play(FadeIn(Dot(ex.c2p(1, 2), color=SECANT)), FadeIn(Dot(ex.c2p(1, -3), color=SECANT)), run_time=0.6),
                           4: lambda sc: sc.play(Create(t1), run_time=0.8), 5: lambda sc: sc.play(Create(t2), run_time=0.8)},
                     notes_graph=dict(fns=[("(-x+sqrt(abs(28-3*x^2)))/2", -3.05, 3.05), ("(-x-sqrt(abs(28-3*x^2)))/2", -3.05, 3.05)], xr=(-4, 4), yr=(-4, 4),
                                      closed=[(1, 2), (1, -3)], vlines=[1]))
        self.finish()
