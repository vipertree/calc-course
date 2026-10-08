"""Topic 2.5: The power rule, from a square and a cube nudged by dx. Narration comes from transcripts/2_5.md."""
import numpy as np
from manim import *

from kit import *
from style import *

# oblique projection for the cube: x to the right, y toward the viewer (down-left), z up
EX, EY, EZ = np.array([1, 0, 0]), np.array([-0.5, -0.32, 0]), np.array([0, 1, 0])


def P(x, y, z):
    return x * EX + y * EY + z * EZ


def box(x0, x1, y0, y1, z0, z1, color, origin):
    """Three visible faces of an axis-aligned box: front (y = y1, nearest), right (x = x1) and top (z = z1)."""
    o = origin
    front = Polygon(o + P(x0, y1, z0), o + P(x1, y1, z0), o + P(x1, y1, z1), o + P(x0, y1, z1))
    right = Polygon(o + P(x1, y1, z0), o + P(x1, y0, z0), o + P(x1, y0, z1), o + P(x1, y1, z1))
    top = Polygon(o + P(x0, y1, z1), o + P(x1, y1, z1), o + P(x1, y0, z1), o + P(x0, y0, z1))
    g = VGroup(front, right, top)
    for face, op in zip(g, (0.85, 0.6, 0.4)):
        face.set_fill(color, op).set_stroke(BG, 1.5)
    return g


def cube_pieces(x, d, origin, levels=(0, 1, 2, 3)):
    """The cube [0,x]^3 grown by d toward the viewer, right and up. Grouped by how many sides are nudged."""
    xs, ys, zs = [(0, x), (x, x + d)], [(0, x), (x, x + d)], [(0, x), (x, x + d)]
    cols = {0: FUNC, 1: SECANT, 2: TANGENT, 3: DERIV}
    out = VGroup(*[VGroup() for _ in range(4)])
    for i in (0, 1):
        for j in (0, 1):
            for k in (0, 1):
                n = i + j + k
                if n in levels and (d > 1e-3 or n == 0):
                    out[n].add(box(*xs[i], *ys[j], *zs[k], cols[n], origin))
    return out


class Lesson(TranscriptScene):
    NUM = "2.5"

    def square(self, x, d, corner):
        o = corner
        main = Square(x, color=FUNC, fill_color=FUNC, fill_opacity=0.35).move_to(o + (RIGHT + UP) * x / 2)
        right = Rectangle(width=d, height=x, color=SECANT, fill_color=SECANT, fill_opacity=0.7, stroke_width=1).move_to(o + RIGHT * (x + d / 2) + UP * x / 2)
        top = Rectangle(width=x, height=d, color=SECANT, fill_color=SECANT, fill_opacity=0.7, stroke_width=1).move_to(o + RIGHT * x / 2 + UP * (x + d / 2))
        tiny = Square(max(d, 1e-3), color=TANGENT, fill_color=TANGENT, fill_opacity=0.9, stroke_width=1).move_to(o + (RIGHT + UP) * (x + d / 2))
        return VGroup(main, right, top, tiny)

    def construct(self):
        X, corner = 3.2, LEFT * 5.2 + DOWN * 2.4
        DX = 0.4                                 # the nudge: thin, so the strips read as slivers
        d = ValueTracker(0.0)
        sq = always_redraw(lambda: self.square(X, d.get_value(), corner))
        with self.beat("A growing square") as b:
            base = self.square(X, 0, corner)[0]
            lab = M("x^2", 56).move_to(base)
            xl = VGroup(M("x", 40, DIM).next_to(base, DOWN, buff=0.15), M("x", 40, DIM).next_to(base, LEFT, buff=0.15))
            self.play(DrawBorderThenFill(base), FadeIn(lab), FadeIn(xl), run_time=1.2)
            b.line(1)
            self.remove(base)
            self.add(sq, lab)
            self.play(d.animate.set_value(DX), run_time=1.6)
            nudge = T(r"$dx$: a tiny nudge", 34, SECANT).next_to(corner + RIGHT * (X + DX) + UP * X, UR, buff=0.3)
            self.play(FadeIn(nudge), run_time=0.6)
            b.line(2)
            # the nudge is a small double arrow across each sliver, with the strips' long sides labeled x
            arr_r = DoubleArrow(corner + RIGHT * X + UP * (X * 0.25), corner + RIGHT * (X + DX) + UP * (X * 0.25), buff=0, color=INK,
                                stroke_width=3, tip_length=0.1, max_tip_length_to_length_ratio=0.45)
            arr_t = DoubleArrow(corner + RIGHT * (X * 0.25) + UP * X, corner + RIGHT * (X * 0.25) + UP * (X + DX), buff=0, color=INK,
                                stroke_width=3, tip_length=0.1, max_tip_length_to_length_ratio=0.45)
            dxl = VGroup(M("dx", 30).next_to(arr_r, RIGHT, buff=0.1), M("dx", 30).next_to(arr_t, LEFT, buff=0.1))
            self.play(FadeOut(nudge), GrowFromCenter(arr_r), GrowFromCenter(arr_t), FadeIn(dxl), run_time=0.8)
            tags = VGroup(M(r"x", 34, SECANT).next_to(corner + RIGHT * (X + DX) + UP * X * 0.6, RIGHT, buff=0.15),
                          M(r"x", 34, SECANT).next_to(corner + RIGHT * X * 0.6 + UP * (X + DX), UP, buff=0.15),
                          M(r"(dx)^2", 34, TANGENT).next_to(corner + (RIGHT + UP) * (X + DX), UR, buff=0.1))
            areas = VGroup(M(r"x\,dx", 34, SECANT), M(r"x\,dx", 34, SECANT)).arrange(DOWN, buff=0.3).next_to(corner + RIGHT * (X + DX) + UP * X, RIGHT, buff=1.6)
            self.play(LaggedStart(*[FadeIn(t) for t in tags], lag_ratio=0.4), run_time=1.6)
            self.play(FadeIn(T("each strip:", 30, DIM).next_to(areas, UP, buff=0.2)), FadeIn(areas[0]), run_time=0.8)
        self.clear()
        self.remove(sq)
        self.title()

        d.set_value(DX)
        self.add(sq)
        lab = M("x^2", 56).move_to(corner + (RIGHT + UP) * X / 2)
        xs_ = VGroup(M("x", 40, DIM).next_to(corner + RIGHT * X / 2, DOWN, buff=0.15), M("x", 40, DIM).next_to(corner + UP * X / 2, LEFT, buff=0.15))
        # the nudges keep their arrows while dx shrinks, until they are too small to draw
        dxa = always_redraw(lambda: VGroup() if d.get_value() < 0.06 else VGroup(
            nudge_arrow(corner + RIGHT * X, corner + RIGHT * (X + d.get_value()), "dx", DOWN),
            nudge_arrow(corner + UP * X, corner + UP * (X + d.get_value()), "dx", LEFT)))
        self.play(FadeIn(lab), FadeIn(xs_), FadeIn(dxa), run_time=0.4)
        with self.beat("From a nudge to a limit") as b:
            e1 = M(r"dA = 2x\,dx + (dx)^2", 48).to_edge(RIGHT, buff=0.6).shift(UP * 2.2)
            self.play(Write(e1), run_time=1.4)
            b.line(1)
            e2 = M(r"\frac{dA}{dx} = 2x + dx", 48).next_to(e1, DOWN, buff=0.5).align_to(e1, LEFT)
            self.play(Write(e2), run_time=1.2)
            b.line(2)
            read = always_redraw(lambda: M(rf"dx = {d.get_value():.2f}, \quad (dx)^2 = {d.get_value() ** 2:.4f}", 36, DIM)
                                 .next_to(e2, DOWN, buff=0.5).align_to(e1, LEFT))
            self.add(read)
            self.play(d.animate.set_value(0.1), run_time=3)
            b.line(3)
            self.play(d.animate.set_value(0.01), run_time=2)
            b.line(4)
            self.remove(read)
            e3 = M(r"dx \to 0:\quad \frac{dA}{dx} = 2x", 50, DERIV).next_to(e2, DOWN, buff=0.6).align_to(e1, LEFT)
            self.play(Write(e3), run_time=1.6)
        self.clear()
        self.remove(sq)

        with self.beat("What d x means") as b:
            eq = M(r"\frac{dA}{dx} = 2x + dx", 64).shift(UP * 1.6)
            self.play(FadeIn(eq), run_time=0.8)
            arrow = VGroup(Arrow(UP * 0.4, DOWN * 0.4, color=DIM), M(r"dx \to 0", 36, DIM)).arrange(RIGHT, buff=0.2).next_to(eq, DOWN, buff=0.3)
            self.play(FadeIn(arrow), run_time=0.6)
            res = M(r"\frac{dA}{dx} = 2x", 64, DERIV).next_to(arrow, DOWN, buff=0.3)
            self.play(TransformFromCopy(eq, res), run_time=1.2)
            b.line(1)
            cap = T(r"divide by $dx$, then let the nudge shrink to $0$: \\ the limit definition, in short form", 36, DIM).next_to(res, DOWN, buff=0.6)
            cap2 = T(r"think: infinitely small changes \\ officially: a limit", 36, SECANT).next_to(cap, DOWN, buff=0.4)
            self.play(FadeIn(cap), run_time=1)
            b.line(2)
            self.play(FadeIn(cap2), run_time=0.8)
        self.clear()

        X3, origin = 2.6, LEFT * 3.2 + DOWN * 1.6
        with self.beat("A growing cube") as b:
            base = cube_pieces(X3, 0, origin, levels=(0,))
            self.play(FadeIn(base), FadeIn(M("x^3", 50).next_to(base, UP, buff=0.3)), run_time=1)
            b.line(1)
            dd = 0.35
            grown = cube_pieces(X3, dd, origin)
            self.play(FadeIn(grown[0]), run_time=0.01)
            self.remove(base)
            self.play(LaggedStart(*[FadeIn(p, shift=0.3 * UP) for p in grown[1]], lag_ratio=0.4), run_time=1.6)
            o3 = origin
            dims = VGroup(M("x", 36, DIM).next_to(o3 + P(X3 / 2, X3 + dd, 0), DOWN, buff=0.15),
                          nudge_arrow(o3 + P(X3, X3 + dd, 0), o3 + P(X3 + dd, X3 + dd, 0), "dx", DOWN),
                          nudge_arrow(o3 + P(0, X3 + dd, X3), o3 + P(0, X3 + dd, X3 + dd), "dx", LEFT),
                          nudge_arrow(o3 + P(0, X3, 0), o3 + P(0, X3 + dd, 0), "dx", LEFT + DOWN * 0.3))
            self.play(FadeIn(dims), run_time=0.8)
            t1 = M(r"dV = 3x^2\,dx", 46, SECANT).to_edge(RIGHT, buff=0.8).shift(UP * 2)
            self.play(Write(t1), run_time=0.8)
            b.line(2)
            self.play(FadeIn(grown[2]), run_time=0.8)
            t2 = M(r"+\ 3x\,(dx)^2", 46, TANGENT).next_to(t1, DOWN, buff=0.3).align_to(t1, LEFT)
            self.play(Write(t2), run_time=0.8)
            self.play(FadeIn(grown[3]), run_time=0.6)
            t3 = M(r"+\ (dx)^3", 46, DERIV).next_to(t2, DOWN, buff=0.3).align_to(t1, LEFT)
            self.play(Write(t3), run_time=0.8)
            b.line(3)
            r1 = M(r"\frac{dV}{dx} = 3x^2 + 3x\,dx + (dx)^2", 42).next_to(t3, DOWN, buff=0.6).align_to(t1, LEFT)
            self.play(Write(r1), run_time=1.2)
            b.line(4)
            dv = ValueTracker(dd)
            live = always_redraw(lambda: cube_pieces(X3, dv.get_value(), origin))
            self.remove(grown)
            self.add(live)
            self.play(dv.animate.set_value(0.02), run_time=2.5)
            r2 = M(r"dx \to 0:\quad \frac{dV}{dx} = 3x^2", 46, DERIV).next_to(r1, DOWN, buff=0.4).align_to(t1, LEFT)
            self.play(Write(r2), run_time=1)
            b.line(5)
            self.play(Indicate(t1, color=SECANT), run_time=1)
        self.clear()

        with self.beat("The pattern") as b:
            rows = VGroup(*[M(rf"x^{{{n}}} \ \longrightarrow\ {n}x^{{{n - 1}}}" if n > 2 else r"x^2 \ \longrightarrow\ 2x", 56) for n in (2, 3, 4)])
            rows.arrange(DOWN, buff=0.6, aligned_edge=LEFT)
            for r in rows:
                self.play(Write(r), run_time=0.9)
            gen = M(r"x^n \ \longrightarrow\ n x^{n - 1}", 60, DERIV).next_to(rows, DOWN, buff=0.7)
            self.play(Write(gen), run_time=1)
        self.clear()

        with self.beat("The power rule") as b:
            card = formula_box(M(r"\frac{d}{dx}\, x^n = n x^{n - 1}", 72), DERIV)
            self.play(FadeIn(card), run_time=1)
            b.line(1)
            self.play(FadeIn(T(r"for any real number $n$", 40, DIM).next_to(card, DOWN, buff=0.5)), run_time=0.8)
        self.clear()

        with self.beat("Two steps") as b:
            steps = VGroup(T("1. Multiply by the exponent: bring it down in front.", 40), T("2. Subtract one from the exponent.", 40)).arrange(DOWN, buff=0.4, aligned_edge=LEFT).to_edge(UP, buff=0.6)
            b.line(1)
            self.play(FadeIn(steps), run_time=1)
            b.line(2)
            board = Board().next_to(steps, DOWN, buff=0.9)
            board.write(self, "POWER:x|5|4", size=64)
        self.clear()

        with self.beat("Rewrite first") as b:
            board = Board()
            board.anchor = UP * 2.6
            b.line(1)
            board.write(self, r"\frac{1}{x^2} = x^{-2}")
            board.write(self, "POWER:x|-2|-3")
            b.line(2)
            board.write(self, r"\sqrt{x} = x^{1/2}")
            board.write(self, r"POWER:x|\tfrac12|-\tfrac12")
        self.clear()

        ax, al = plot_axes([0, 3, 1], [0, 27, 9], w=6.4, h=5)
        VGroup(ax, al).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        with self.beat("In context") as b:
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(lambda x: x ** 3, x_range=[0, 3], color=FUNC, stroke_width=5)), run_time=1.2)
            self.play(Create(tangent_line(ax, lambda x: x ** 3, 2, 12, [1.4, 2.6])), FadeIn(closed_dot(ax, 2, 8, INK)),
                      FadeIn(M(r"\text{slope } 12", 40, TANGENT).next_to(ax.c2p(2, 8), RIGHT, buff=0.5)), run_time=1)
            b.line(1)
            note = T(r"side $= 2$: volume grows \\ $12$ cubic units per unit of side", 36).to_edge(RIGHT, buff=0.6).shift(UP * 1.6)
            self.play(FadeIn(note), run_time=1)
        self.clear()

        self.example("Slope and rate", r"(a) Find the slope of the tangent line to $y = x^4$ at $x = -1$. (b) If $A = s^2$ is the area of a square with side $s$ cm, how fast is the area changing with respect to $s$ when $s = 5$?",
                     [r"PART:(a) the slope at x = -1", r"y' = 4x^3,\quad y'(-1) = 4(-1)^3 = -4", r"PART:(b) the rate when s = 5", r"\frac{dA}{ds} = 2s = 2(5) = 10 \ \text{cm}^2\text{ per cm}"],
                     at=[0, 1, 2, 3])
        self.example("Tangent line", r"Find the equation for the line tangent to $y = \sqrt{x}$ at $x = 4$.",
                     [r"y = x^{1/2}", r"POWER:x|\tfrac12|-\tfrac12", r"y' = \frac{1}{2\sqrt x},\quad y'(4) = \frac14", r"(4, 2):\quad y - 2 = \frac14(x - 4)"], at=[1, 1, 2, 3])

        with self.beat("Close") as b:
            # the takeaway is the rule itself, not the pictures (Adder)
            card = formula_box(M(r"\frac{d}{dx}\, x^n = n x^{n - 1}", 64), DERIV).shift(UP * 0.4)
            how = T("bring the exponent down, subtract one from the exponent", 34, DIM).next_to(card, DOWN, buff=0.5)
            self.play(FadeIn(card), run_time=1)
            self.play(FadeIn(how), run_time=0.8)
        self.clear()

        self.examples_card()
        self.example("Example 1: Straight from the rule", r"Find $\dfrac{d}{dx}\,x^7$ and $\dfrac{d}{dx}\,x^{-3}$.",
                     [r"POWER:x|7|6", r"POWER:x|-3|-4", r"= -\frac{3}{x^4}"], at=[1, 2, 3])
        self.example("Example 2: Rewrite, then differentiate", r"Find $\dfrac{dy}{dx}$ at $x = 4$ for $y = \dfrac{1}{\sqrt{x^3}}$.",
                     [r"y = \frac{1}{x^{3/2}} = x^{-3/2}", r"POWER:x|-\tfrac32|-\tfrac52", r"4^{5/2} = 32,\ \text{so}\ \frac{dy}{dx}\Big|_{x=4} = -\frac{3}{2}\cdot\frac{1}{32} = -\frac{3}{64}"],
                     at=[1, 2, 3])
        a3, _ = plot_axes([0, 12, 4], [0, 3, 1], w=5.4, h=3.6)
        fig = VGroup(a3, a3.plot(np.cbrt, x_range=[0, 12, 0.01], color=FUNC, stroke_width=4), a3.plot(lambda x: 2 + (x - 8) / 12, x_range=[2, 12], color=TANGENT, stroke_width=4),
                     closed_dot(a3, 8, 2, INK))
        self.example("Example 3: A tangent line to a cube root", r"Find the equation for the line tangent to $y = \sqrt[3]{x}$ at $x = 8$.",
                     [r"\sqrt[3]{8} = 2,\ \text{so}\ (8, 2)", r"POWER:x|\tfrac13|-\tfrac23", r"8^{2/3} = 4,\ \text{so}\ \text{slope } \frac13 \cdot \frac14 = \frac{1}{12}",
                      r"y - 2 = \frac{1}{12}(x - 8)"], figure=fig, at=[1, 2, 3, 4])
        self.finish()
