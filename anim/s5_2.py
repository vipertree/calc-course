"""Topic 5.2: EVT, absolute vs relative extrema, critical points. Narration comes from transcripts/5_2.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "5.2"

    def construct(self):
        trail = lambda s: 1.2 * np.sin(1.3 * s) + 0.5 * np.sin(2.6 * s + 0.8) + 0.12 * s
        ax = Axes(x_range=[0, 6.5], y_range=[-2.5, 2.8], x_length=12, y_length=5, tips=False, axis_config={"stroke_opacity": 0}).shift(DOWN * 0.4)
        with self.beat("A hike") as b:
            path = ax.plot(trail, x_range=[0, 6.2], color=FUNC, stroke_width=6)
            flags = VGroup(T("start", 30, DIM).next_to(ax.c2p(0, trail(0)), DOWN, buff=0.2), T("finish", 30, DIM).next_to(ax.c2p(6.2, trail(6.2)), DOWN, buff=0.2))
            self.play(Create(path), FadeIn(flags), run_time=1.6)
            S = ValueTracker(0)
            hiker = always_redraw(lambda: Dot(ax.c2p(S.get_value(), trail(S.get_value())), color=SECANT, radius=0.13))
            self.add(hiker)
            self.play(S.animate.set_value(6.2), run_time=4, rate_func=linear)
            b.line(1)
            xs = np.linspace(0, 6.2, 2000)
            ys = trail(xs)
            peaks = [i for i in range(1, len(xs) - 1) if ys[i] > ys[i - 1] and ys[i] > ys[i + 1]]
            top = max(peaks, key=lambda i: ys[i])
            other = [i for i in peaks if i != top][0]
            lab1 = T("highest point of the hike", 30, TANGENT).next_to(ax.c2p(xs[top], ys[top]), UP, buff=0.2)
            lab2 = T("top of a hill", 30, DERIV).next_to(ax.c2p(xs[other], ys[other]), UP, buff=0.2)
            self.play(FadeIn(Dot(ax.c2p(xs[top], ys[top]), color=TANGENT)), FadeIn(lab1), run_time=0.8)
            self.play(FadeIn(Dot(ax.c2p(xs[other], ys[other]), color=DERIV)), FadeIn(lab2), run_time=0.8)
        self.clear()
        self.title()

        ax, al = plot_axes([-1, 5, 1], [0, 6, 1], w=7.6, h=5.4, coords=False)
        VGroup(ax, al).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        f = lambda s: 0.3 * s**3 - 1.8 * s**2 + 2.7 * s + 1.6
        with self.beat("Absolute and relative") as b:
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(f, x_range=[-0.2, 4.6], color=FUNC, stroke_width=5)), run_time=1.2)
            spots = [(4.6, "absolute max", TANGENT, UP), (-0.2, "absolute min", TANGENT, DR), (1, "relative max", DERIV, UP), (3, "relative min", DERIV, DOWN)]
            marks = [VGroup(Dot(ax.c2p(s, f(s)), color=c), T(t, 28, c).next_to(ax.c2p(s, f(s)), d, buff=0.25)) for s, t, c, d in spots]
            self.play(FadeIn(marks[0]), FadeIn(marks[1]), run_time=0.8)
            b.line(1)
            self.play(FadeIn(marks[2]), FadeIn(marks[3]), run_time=0.8)
            b.line(2)
            self.play(Indicate(marks[0], color=TANGENT), Indicate(marks[1], color=TANGENT), run_time=1)
        self.clear()

        with self.beat("A little Latin") as b:
            words = table([r"\text{one}", r"\text{two or more}"], [[r"\text{maximum}", r"\text{maxima}"], [r"\text{minimum}", r"\text{minima}"],
                                                                  [r"\text{extremum}", r"\text{extrema}"]], size=46).shift(UP * 0.8 + LEFT * 1.6)
            rows = [VGroup(*words.cells[r]) for r in (1, 2, 3)]
            either = T("a max or a min", 34, SECANT).next_to(rows[2], RIGHT, buff=0.8)
            english = T("In English, also: maximums, minimums, extreme values.", 36, DIM).next_to(words, DOWN, buff=0.9).set_x(0)
            self.play(FadeIn(VGroup(*words.cells[0])), FadeIn(words[1]), run_time=0.6)
            b.line(1)
            self.play(FadeIn(rows[0]), run_time=0.6)
            self.wait(1)
            self.play(FadeIn(rows[1]), run_time=0.6)
            b.line(2)
            self.play(FadeIn(rows[2]), run_time=0.6)
            self.play(FadeIn(either), run_time=0.6)
            b.line(3)
            self.play(FadeIn(english), run_time=0.8)
        self.clear()

        with self.beat("The Extreme Value Theorem") as b:
            thm = VGroup(Tex(r"If $f$ is ", r"continuous", r" on ", r"$[a, b]$", r", then $f$ has", font_size=44, color=INK),
                         T(r"an absolute maximum and an absolute minimum on $[a, b]$.", 44)).arrange(DOWN, buff=0.3)
            box = VGroup(thm, SurroundingRectangle(thm, color=TANGENT, buff=0.35))
            self.play(FadeIn(box), run_time=1)
            b.line(1)
            u1 = Underline(thm[0][3], color=SECANT)        # [a, b]
            u2 = Underline(thm[0][1], color=SECANT)        # continuous
            self.play(Create(u1), run_time=0.6)
            self.wait(0.6)
            self.play(Create(u2), run_time=0.6)
        self.clear()

        with self.beat("No endpoint, no maximum") as b:
            def zoom_panel(W, lo_lab, x_lab):
                """y = x on a window [1 - 2W, 1 + W/2] (both axes); the dot sits at 1 - W/5, so each panel is the last one magnified 10x."""
                lo, hi = 1 - 2 * W, 1 + 0.5 * W
                a = Axes(x_range=[lo, hi, W], y_range=[lo, hi, W], x_length=3.3, y_length=3.3, tips=False, axis_config={"color": DIM, "stroke_width": 2})
                frame = Polygon(a.c2p(lo, lo), a.c2p(hi, lo), a.c2p(hi, hi), a.c2p(lo, hi), color=DIM, stroke_width=2)
                line = a.plot(lambda s: s, x_range=[lo, 1], color=FUNC, stroke_width=5)
                hole = Circle(radius=0.09, color=FUNC, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(a.c2p(1, 1))
                xd = 1 - W / 5
                dot = Dot(a.c2p(xd, xd), color=SECANT, radius=0.09)
                ticks = VGroup(M(lo_lab, 26, DIM).next_to(a.c2p(lo, lo), DOWN, buff=0.15), M("1", 26, DIM).next_to(a.c2p(1, lo), DOWN, buff=0.15))
                read = M(rf"f({x_lab}) = {x_lab}", 32, SECANT).next_to(a, DOWN, buff=0.55)
                box = Polygon(*[a.c2p(1 + dx * W / 10, 1 + dy * W / 10) for dx, dy in ((-2, -2), (0.5, -2), (0.5, 0.5), (-2, 0.5))], color=TANGENT, stroke_width=2)
                return dict(ax=a, frame=frame, line=line, hole=hole, dot=dot, ticks=ticks, read=read, box=box)
            ps = [zoom_panel(0.5, "0", "0.9"), zoom_panel(0.05, "0.9", "0.99"), zoom_panel(0.005, "0.99", "0.999")]
            for p in ps:
                p["all"] = VGroup(p["ax"], p["frame"], p["line"], p["hole"], p["dot"], p["ticks"], p["read"])
            VGroup(*[p["all"] for p in ps]).arrange(RIGHT, buff=1.0, aligned_edge=UP).shift(UP * 0.2)
            for p in ps:     # re-place the boxes now that the panels have moved
                a = p["ax"]
                p["box"].move_to(a.c2p(1 - 0.75 * (a.x_range[2] / 10), 1 - 0.75 * (a.x_range[2] / 10)))
            head = T(r"$y = x$ on the open interval $(0, 1)$", 40).to_edge(UP, buff=0.4)
            p0 = ps[0]
            self.play(FadeIn(head), FadeIn(p0["ax"]), FadeIn(p0["frame"]), FadeIn(p0["ticks"]), Create(p0["line"]), run_time=1.2)
            b.line(1)
            self.play(FadeIn(p0["hole"]), run_time=0.4)
            self.play(Indicate(p0["hole"], color=TANGENT, scale_factor=2), run_time=1)
            b.line(2)
            self.play(FadeIn(p0["dot"]), FadeIn(p0["read"]), run_time=0.8)
            for k in (1, 2):
                b.line(k + 2)
                src, dst = ps[k - 1], ps[k]
                links = VGroup(Line(src["box"].get_corner(UR), dst["frame"].get_corner(UL), color=TANGENT, stroke_width=1.5),
                               Line(src["box"].get_corner(DR), dst["frame"].get_corner(DL), color=TANGENT, stroke_width=1.5))
                self.play(Create(src["box"]), run_time=0.5)
                grow = VGroup(dst["ax"], dst["frame"], dst["line"], dst["hole"], dst["ticks"])
                self.play(Create(links), TransformFromCopy(src["box"], dst["frame"]), FadeIn(grow), run_time=1.2)
                self.play(FadeIn(dst["dot"]), FadeIn(dst["read"]), run_time=0.8)
            b.line(5)
            last = T(r"always a little closer to $1$, never reaching it: no maximum", 36, TANGENT).to_edge(DOWN, buff=0.4)
            self.play(Indicate(ps[2]["hole"], color=TANGENT, scale_factor=2), FadeIn(last), run_time=1.2)
        self.clear()

        with self.beat("Off to infinity") as b:
            ax, al = plot_axes([-1, 1, 1], [-12, 12, 4], w=5.6, h=5.4, coords=False)
            VGroup(ax, al).to_edge(LEFT, buff=1.0).shift(DOWN * 0.3)
            head = T(r"$y = \frac1x$ on $[-1, 1]$", 40).to_edge(UP, buff=0.4)
            right = ax.plot(lambda s: 1 / s, x_range=[1 / 12, 1], color=FUNC, stroke_width=5)
            left = ax.plot(lambda s: 1 / s, x_range=[-1, -1 / 12], color=FUNC, stroke_width=5)
            asym = asymptote(ax, 0, (-12, 12))
            self.play(FadeIn(head), FadeIn(ax), FadeIn(al), Create(left), Create(right), FadeIn(asym), run_time=1.4)
            tab = table([r"x", r"\frac1x"], [["0.1", "10"], ["0.01", "100"], ["0.001", "1000"]], size=40).to_edge(RIGHT, buff=1.4).shift(UP * 0.6)
            rows = [VGroup(*tab.cells[r]) for r in (1, 2, 3)]
            X = ValueTracker(1.0)
            climber = always_redraw(lambda: Dot(ax.c2p(X.get_value(), min(1 / X.get_value(), 12)), color=SECANT, radius=0.1))
            self.add(climber)
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab[1]), run_time=0.6)
            b.line(1)
            self.play(X.animate.set_value(0.1), FadeIn(rows[0]), run_time=1.6, rate_func=rate_functions.ease_in_out_sine)
            b.line(2)
            self.play(X.animate.set_value(1 / 12), FadeIn(rows[1]), run_time=1.2)
            up = Arrow(ax.c2p(1 / 12, 10.5), ax.c2p(1 / 12, 10.5) + UP * 1.2, color=SECANT, buff=0, stroke_width=5)
            self.play(GrowArrow(up), FadeIn(rows[2]), run_time=1.2)
            b.line(3)
            last = T(r"not continuous at $0$: no maximum", 36, TANGENT).next_to(tab, DOWN, buff=0.8)
            self.play(FadeIn(last), run_time=0.8)
            b.line(4)
            both = T(r"EVT needs: closed interval \emph{and} continuous", 36, SECANT).next_to(last, DOWN, buff=0.5)
            self.play(FadeIn(both), run_time=0.8)
        self.clear()

        with self.beat("Critical points") as b:
            def mini(fn, xr, label):
                a, _ = plot_axes([xr[0], xr[1], 1], [-1.5, 1.5, 1], w=3.4, h=2.8, coords=False)
                return VGroup(a, a.plot(fn, x_range=[xr[0], xr[1], 0.01], color=FUNC, stroke_width=5), M(label, 32, TANGENT)), a
            m1, a1 = mini(lambda s: 1 - s * s, (-1.2, 1.2), r"f'(c) = 0")
            m2, a2 = mini(lambda s: 1 - 1.6 * abs(s), (-1.2, 1.2), r"f'(c) \text{ undefined}")
            m3, a3 = mini(lambda s: s**3, (-1.1, 1.1), r"f'(0) = 0,\ \text{no peak}")
            m1.add(Line(a1.c2p(-0.6, 1), a1.c2p(0.6, 1), color=TANGENT, stroke_width=4))
            m3.add(Line(a3.c2p(-0.6, 0), a3.c2p(0.6, 0), color=TANGENT, stroke_width=4))
            for m in (m1, m2, m3):
                m[2].next_to(m[0], DOWN, buff=0.3)
            row = VGroup(m1, m2, m3).arrange(RIGHT, buff=0.8).to_edge(UP, buff=0.5)
            self.play(FadeIn(m1), run_time=0.8)
            b.line(1)
            self.play(FadeIn(m2), run_time=0.8)
            b.line(2)
            defn = formula_box(VGroup(T(r"\textbf{Critical point:} $x = c$ in the domain of $f$ where", 38, SECANT),
                                      M(r"f'(c) = 0 \quad \text{or} \quad f'(c) \text{ is undefined}", 44, SECANT)).arrange(DOWN, buff=0.25), SECANT)
            defn.to_edge(DOWN, buff=0.4)
            self.play(FadeIn(defn), run_time=0.8)
            b.line(3)
            self.play(Indicate(defn[1][1], color=SECANT), run_time=1)
            b.line(4)
            self.play(FadeIn(m3), run_time=0.8)
        self.clear()
        self.example("Find the critical points", r"Find the critical points of $f(x) = x^4 - 8x^2$.",
                     [r"f'(x) = 4x^3 - 16x", r"= 4x(x^2 - 4)", r"= 4x(x - 2)(x + 2)", r"4x = 0 \text{ or } x - 2 = 0 \text{ or } x + 2 = 0",
                      r"x = 0,\ x = 2,\ x = -2", r"f' \text{ is never undefined}"], at=[1, 2, 3, 4, 4, 5])

        with self.beat("Close") as b:
            card = VGroup(M(r"\text{Critical point: } f'(c) = 0 \text{ or } f'(c) \text{ undefined}", 44, SECANT),
                          T("Every relative extremum is at a critical point.", 38), T("Not every critical point is an extremum.", 38, TANGENT)).arrange(DOWN, buff=0.5)
            self.play(FadeIn(card[0]), run_time=0.8)
            self.play(FadeIn(card[1]), run_time=0.6)
            self.play(FadeIn(card[2]), run_time=0.6)
        self.clear()

        self.examples_card()
        self.example("Example 1: A cubic", r"Find the critical points of $f(x) = x^3 - 3x^2$.",
                     [r"f'(x) = 3x^2 - 6x", r"= 3x(x - 2)", r"3x = 0 \text{ or } x - 2 = 0", r"x = 0 \text{ or } x = 2",
                      r"\text{critical points: } x = 0,\ x = 2"], at=[1, 2, 3, 3, 4])
        self.example("Example 2: A cusp", r"Find the critical points of $f(x) = x^{2/3}(x - 5)$, given $f'(x) = \dfrac{5(x - 2)}{3x^{1/3}}$.",
                     [r"f'(x) = 0 \text{ at } x = 2", r"f'(x) \text{ undefined at } x = 0, \text{ and } f(0) = 0 \text{ is defined}", r"\text{critical points: } x = 0,\ x = 2"], at=[1, 2, 3])
        self.example("Example 3: Is a maximum guaranteed?",
                     r"Does the Extreme Value Theorem guarantee an absolute maximum for $f(x) = \dfrac{1}{x^2}$ on $[-1, 1]$? On $[1, 3]$?",
                     [r"TEXT:On $[-1, 1]$: $f$ is not continuous at $0$. No guarantee (and in fact no maximum).",
                      r"TEXT:On $[1, 3]$: $f$ is continuous on a closed interval. Yes."], at=[1, 2])
        self.finish()
