"""Topic 5.9: Connecting f, f' and f''. Narration comes from transcripts/5_9.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def story_chart():
    """Adder's f / f' / f'' chart: a tinted header and three groups of rows (alternate shading, rules between groups).
    Returns (frame, [group1, group2, group3]); each group is rows of VGroup(shade, cells) plus a closing rule."""
    W, RH, HH, top = [4.3, 3.9, 3.9], 0.5, 0.75, 2.95
    cols = (FUNC, DERIV, TANGENT)
    x0 = -sum(W) / 2
    xs = [x0, x0 + W[0], x0 + W[0] + W[1]]
    rule = lambda y, w=2: Line([x0, y, 0], [-x0, y, 0], color=INK, stroke_width=w)
    band = Rectangle(width=sum(W), height=HH, stroke_width=0, fill_color=SECANT, fill_opacity=0.25).move_to([0, top - HH / 2, 0])
    hdr = VGroup(*[T(h, 30, cols[i]).move_to([xs[i] + W[i] / 2, top - HH / 2, 0])
                   for i, h in enumerate(["Function, $f$", "First derivative, $f'$", "Second derivative, $f''$"])])
    frame = VGroup(band, hdr, rule(top, 3), rule(top - HH))
    groups = [[("positive", "", ""), ("zero", "", ""), ("negative", "", "")],
              [("increasing", "positive", ""), ("decreasing", "negative", ""), ("local max or min", "zero, and changes sign", ""),
               ("horizontal tangent", "zero", "")],
              [("concave up", "increasing", "positive"), ("concave down", "decreasing", "negative"),
               ("inflection point", "local max or min", "zero, and changes sign")]]
    y, k, out = top - HH, 0, []
    for g in groups:
        gv = VGroup()
        for r in g:
            cy = y - RH / 2
            shade = Rectangle(width=sum(W), height=RH, stroke_width=0, fill_color=SECANT, fill_opacity=0.08 if k % 2 else 0).move_to([0, cy, 0])
            cells = VGroup(*[(T(t, 28, cols[i]).move_to([xs[i] + W[i] / 2, cy, 0]) if t else VMobject()) for i, t in enumerate(r)])
            gv.add(VGroup(shade, cells))
            y -= RH
            k += 1
        gv.add(rule(y, 3 if g is groups[-1] else 2))
        out.append(gv)
    return frame, out


class Lesson(TranscriptScene):
    NUM = "5.9"

    def three(self):
        f = lambda s: 0.25 * s**4 - s**3 + 2
        d1 = lambda s: s**3 - 3 * s**2
        d2 = lambda s: 3 * s**2 - 6 * s
        rows = []
        for fn, yr, lab, col in ((f, [-6, 3, 3], "f", FUNC), (d1, [-5, 10, 5], "f'", DERIV), (d2, [-5, 20, 5], "f''", TANGENT)):
            a, l = plot_axes([-1, 4, 1], yr, w=8, h=1.9, coords=False, ylabel=lab, font=22)
            rows.append(VGroup(a, l, a.plot(fn, x_range=[-0.6, 3.5], color=col, stroke_width=4)))
        g = VGroup(*rows).arrange(DOWN, buff=0.25).to_edge(LEFT, buff=0.6)
        return g, (f, d1, d2)

    def construct(self):
        g, fns = self.three()
        with self.beat("Three graphs, one function") as b:
            self.play(LaggedStart(*[FadeIn(r) for r in g], lag_ratio=0.3), run_time=1.6)
            b.line(1)
            S = ValueTracker(-0.55)
            axes = [r[0] for r in g]
            line = always_redraw(lambda: Line(axes[0].c2p(S.get_value(), 3), axes[2].c2p(S.get_value(), -5), color=SECANT, stroke_width=3))
            sg = lambda v: "+" if v > 1e-9 else "-" if v < -1e-9 else "0"
            read = always_redraw(lambda: VGroup(
                M(rf"f' \; {sg(fns[1](S.get_value()))}", 38, DERIV), M(rf"f'' \; {sg(fns[2](S.get_value()))}", 38, TANGENT)).arrange(DOWN, buff=0.4).to_edge(RIGHT, buff=1.2))
            self.add(line, read)
            b.line(2)
            self.play(S.animate.set_value(3.45), run_time=6, rate_func=linear)
        self.clear()
        self.title()

        with self.beat("The chart") as b:
            frame, grp = story_chart()
            self.play(FadeIn(frame), run_time=1)
            b.line(1)
            self.play(LaggedStart(*[FadeIn(r) for r in grp[0]], lag_ratio=0.3), run_time=1.2)
            b.line(2)
            self.play(FadeIn(grp[1][0]), run_time=0.6)
            self.play(FadeIn(grp[1][1]), run_time=0.6)
            b.line(3)
            self.play(FadeIn(grp[1][2]), run_time=0.6)
            self.play(FadeIn(grp[1][3]), FadeIn(grp[1][4]), run_time=0.6)
            b.line(4)
            self.play(FadeIn(grp[2][0]), run_time=0.6)
            self.play(FadeIn(grp[2][1]), run_time=0.6)
            b.line(5)
            self.play(FadeIn(grp[2][2]), FadeIn(grp[2][3]), run_time=0.6)
            b.line(6)
            for r in range(3):      # the diagonal: group 2's f and f' words reappear one column right in group 3
                self.play(Indicate(grp[1][r][1][0], color=SECANT), Indicate(grp[2][r][1][1], color=SECANT), run_time=0.7)
                self.play(Indicate(grp[1][r][1][1], color=SECANT), Indicate(grp[2][r][1][2], color=SECANT), run_time=0.7)
        self.clear()

        with self.beat("Zero is not enough") as b:
            def mini(signs, name, text, color):
                sc = sign_chart(["c"], list(signs), name=name, width=3.4, size=38)
                return VGroup(sc, T(text, 28, color).next_to(sc, DOWN, buff=0.9))
            m1 = mini("+-", "f'", "zero and changes sign: a max", DERIV)
            m2 = mini("++", "f'", "zero, no change: just a flat spot", DIM)
            m3 = mini("-+", "f''", "zero and changes sign: inflection", TANGENT)
            m4 = mini("++", "f''", r"zero, no change: no inflection (like $x^4$)", DIM)
            grid = VGroup(VGroup(m1, m2).arrange(RIGHT, buff=1.4), VGroup(m3, m4).arrange(RIGHT, buff=1.4)).arrange(DOWN, buff=0.9)
            grid.set_max_width(12.5)
            b.line(1)
            self.play(FadeIn(m1), run_time=0.8)
            self.play(FadeIn(m2), run_time=0.8)
            b.line(2)
            self.play(FadeIn(m3), run_time=0.8)
            self.play(FadeIn(m4), run_time=0.8)
        self.clear()

        with self.beat("Justify at the right level") as b:
            good = T(r"$f$ is concave up on $(3, \infty)$ \textbf{because} $f'' > 0$ there.", 42, DERIV).shift(UP * 1)
            bad = T(r"$f$ is concave up because it curves upward.", 42, DIM).shift(DOWN * 0.8)
            self.play(FadeIn(good), run_time=0.8)
            b.line(1)
            self.play(FadeIn(bad), run_time=0.6)
            self.play(Create(Cross(bad, stroke_color=TANGENT, scale_factor=0.9)), run_time=0.5)
        self.clear()

        with self.beat("Close") as b:
            g, _ = self.three()
            self.play(FadeIn(g), run_time=1)
            labs = VGroup(T(r"$f'$: direction and extrema", 32, DERIV).next_to(g[1], RIGHT, buff=0.3), T(r"$f''$: concavity and inflection", 32, TANGENT).next_to(g[2], RIGHT, buff=0.3))
            self.play(FadeIn(labs), run_time=0.8)
        self.clear()

        self.examples_card()
        e1 = staged_chart([1, 4], ["-", "-", "+"], words=["dec", "dec", "inc"], name="f'", width=6)
        e2 = staged_chart([1, 3], ["+", "-", "+"], words=["up", "down", "up"], name="f''", width=6)
        efig = VGroup(e1, e2).arrange(DOWN, buff=0.7)
        self.example("Example 1: All the features", r"$f'(x) = (x - 1)^2(x - 4)$. Find the relative extrema and inflection points of $f$.",
                     [r"x - 1 = 0 \text{ or } x - 4 = 0, \ \text{so}\ x = 1 \text{ or } x = 4",
                      r"f'(0) = -4 < 0, \ f'(2) = -2 < 0, \ f'(5) = 16 > 0",
                      r"x = 1: \text{ no sign change, no extremum}; \ x = 4: - \text{ to } +, \text{ rel. min}",
                      r"f''(x) = 2(x - 1)(x - 4) + (x - 1)^2", r"= (x - 1)(2x - 8 + x - 1) = 3(x - 1)(x - 3)",
                      r"f''(0) = 9 > 0, \ f''(2) = -3 < 0, \ f''(4) = 9 > 0", r"\text{inflection points at } x = 1 \text{ and } x = 3"],
                     at=[1, 2, 3, 4, 5, 6, 7], figure=efig,
                     cues={1: lambda sc: (reveal_sign(e1, 0, 1, 2)(sc), reveal_words(e1)(sc)),
                           2: lambda sc: (mark_point(e1, 0, "neither", DIM)(sc), mark_point(e1, 1, "min")(sc)),
                           5: lambda sc: (reveal_sign(e2, 0, 1, 2)(sc), reveal_words(e2)(sc)),
                           6: lambda sc: (mark_point(e2, 0, "inflection")(sc), mark_point(e2, 1, "inflection")(sc))})
        self.example("Example 2: A sign table",
                     r"On $(-\infty, -1)$: $f' > 0$, $f'' < 0$. At $-1$: $f' = 0$. On $(-1, 2)$: $f' < 0$, $f'' < 0$. At $2$: $f'' = 0$. On $(2, \infty)$: $f' < 0$, $f'' > 0$. "
                     r"Find the relative extrema and inflection points of $f$.",
                     [r"x = -1:\ f' \text{ changes from } + \text{ to } -:\ \text{relative max}", r"x = 2:\ f'' \text{ changes from } - \text{ to } +:\ \text{inflection}",
                      r"\text{no relative min: } f' \text{ never goes from } - \text{ to } +"], at=[1, 2, 3])
        self.example("Example 3: When the second derivative is zero too", r"$f'(2) = 0$ and $f''(x) = (x - 2)e^{x}$. Does $f$ have a relative extremum at $x = 2$?",
                     [r"f''(2) = 0:\ \text{the Second Derivative Test is silent}", r"f'' < 0 \text{ for } x < 2,\ \ f'' > 0 \text{ for } x > 2",
                      r"f' \text{ has its minimum, } 0, \text{ at } x = 2:\ \ f' \ge 0 \text{ near } 2", r"\text{no extremum; an inflection point at } x = 2"], at=[1, 2, 3, 4])
        pa, pl = plot_axes([-3, 4, 1], [-3, 3, 1], w=5.6, h=3.6, ylabel="f'(x)")
        segA, segB, segC = (Line(pa.c2p(*p), pa.c2p(*q), color=FUNC, stroke_width=5) for p, q in (((-3, 0), (-1, 2)), ((-1, 2), (1, -2)), ((1, -2), (4, 1))))
        pfig = VGroup(pa, pl, segA, segB, segC)
        self.example("Example 4: Every column from one graph",
                     r"The graph of $f'$ (three segments) is shown. Where does $f$ have relative extrema? Where is $f$ concave up or down, and where are its "
                     r"inflection points? Find $f''(2)$.",
                     [r"x = 0: \ f' \ + \text{ to } -, \ \text{rel. max}", r"x = 3: \ f' \ - \text{ to } +, \ \text{rel. min}",
                      r"f' \text{ rising on } (-3, -1),\ (1, 4): \ \text{concave up}", r"f' \text{ falling on } (-1, 1): \ \text{concave down}",
                      r"\text{inflection at } x = -1 \text{ and } x = 1", r"f''(2) = \text{slope of } f' = \frac{1 - (-2)}{4 - 1} = 1"],
                     at=[1, 1, 2, 3, 3, 4], figure=pfig,
                     cues={2: lambda sc: sc.play(segA.animate.set_color(DERIV), segC.animate.set_color(DERIV), run_time=0.6),
                           3: lambda sc: sc.play(segB.animate.set_color(TANGENT), run_time=0.6),
                           5: lambda sc: sc.play(Indicate(segC, color=SECANT), run_time=0.8)},
                     text=r"The graph of $f'$ on $[-3, 4]$ consists of three line segments, as shown. Where does $f$ have relative extrema? Where is the graph "
                          r"of $f$ concave up or down, and where are its inflection points? Find $f''(2)$.",
                     notes_graph=dict(fns=[("x+3", -3, -1), ("-2*x", -1, 1), ("x-3", 1, 4)], xr=(-3, 4), yr=(-3, 3), ylabel="f'(x)"))
        self.finish()
