"""Topic 8.1: Average value of a function. Narration comes from transcripts/8_1.md.

Adder's notes (2026-10-14): the unit opens on the 2x2 grid (derivative: rate / slope at a point; integral: accumulation /
area under the curve) plus the bonus that they are inverses. Average value is the total accumulation (a sum of infinitely
thin slivers) divided by the width, compared with a finite average that has real numbers (five readings, 61 degrees)
before the title. The water picture starts as plain area, turns blue, then settles like water (no morph). The MVT for
integrals is the MVT applied to the accumulation function F, whose derivative is the curve.
"""
import numpy as np
from manim import *

from kit import *
from style import *
from props import thermometer


class Lesson(TranscriptScene):
    NUM = "8.1"

    def construct(self):
        f = lambda s: 1.2 + 0.5 * np.sin(1.3 * s) + 0.25 * s
        temp = lambda s: 5 * s**4 / 1536 - 73 * s**3 / 384 + 355 * s**2 / 96 - 2567 * s / 96 + 3717 / 32
        reads = [(6, 52), (10, 61), (14, 70), (18, 66), (22, 56)]

        def temp_graph(w=6.4, h=3.4):
            ax, al = plot_axes([6, 22, 4], [40, 80, 10], w=w, h=h, xlabel="t", ylabel="T")
            return ax, al, ax.plot(temp, x_range=[6, 22], color=FUNC, stroke_width=4)

        with self.beat("Averaging infinitely many numbers") as b:
            ax, al, curve = temp_graph()
            VGroup(ax, al).to_edge(RIGHT, buff=0.8).shift(UP * 1.2)
            curve = ax.plot(temp, x_range=[6, 22], color=FUNC, stroke_width=4)
            therm = thermometer(3.4).to_edge(LEFT, buff=1.0).shift(UP * 0.9)
            self.play(FadeIn(therm), FadeIn(ax), FadeIn(al), Create(curve), run_time=1.4)
            b.line(1)
            dots = VGroup(*[Dot(ax.c2p(t, v), color=SECANT, radius=0.08) for t, v in reads])
            vals = VGroup(*[M(rf"{v}^\circ", 28, SECANT).next_to(ax.c2p(t, v), UP if t in (10, 14) else DOWN, buff=0.15) for t, v in reads])
            self.play(LaggedStart(*[AnimationGroup(FadeIn(d, scale=1.6), FadeIn(l)) for d, l in zip(dots, vals)], lag_ratio=0.35), run_time=2.4)
            b.line(2)
            s1 = M(r"52 + 61 + 70 + 66 + 56 = 305", 40).next_to(ax, DOWN, buff=0.55).shift(LEFT * 1.6)
            s2 = M(r"\text{average} = \frac{305}{5} = 61^\circ", 40, SECANT).next_to(s1, DOWN, buff=0.3, aligned_edge=LEFT)
            self.play(Write(s1), run_time=1.2)
            self.play(Write(s2), run_time=1)
            avg5 = DashedLine(ax.c2p(6, 61), ax.c2p(22, 61), color=SECANT, stroke_width=3)
            self.play(Create(avg5), run_time=0.8)
            b.line(3)
            q = T("What about every instant of the day?", 38, INK).next_to(s2, DOWN, buff=0.4, aligned_edge=LEFT)
            self.play(FadeIn(q), FadeOut(dots), FadeOut(vals), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("Four meanings, plus one") as b:
            grid = FourPanel(width=11.6, height=4.4).shift(UP * 0.85)
            for c in grid.cells.values():
                c[1].set_opacity(0)
            self.play(FadeIn(grid.col_heads), FadeIn(grid.row_heads), *[FadeIn(c[0]) for c in grid.cells.values()], run_time=1)
            b.line(1)
            self.play(grid.cells[("d", "a")][1].animate.set_opacity(1), run_time=0.8)
            self.play(grid.cells[("d", "g")][1].animate.set_opacity(1), run_time=0.8)
            b.line(2)
            self.play(grid.cells[("i", "a")][1].animate.set_opacity(1), run_time=0.8)
            self.play(grid.cells[("i", "g")][1].animate.set_opacity(1), run_time=0.8)
            b.line(3)
            bonus = formula_box(VGroup(T("Bonus: derivatives and integrals are inverses", 32, ACCUM),
                                       M(r"\frac{d}{dx}\int_a^x f(t)\,dt = f(x)", 36)).arrange(RIGHT, buff=0.5), ACCUM)
            bonus.set_max_width(12).to_edge(DOWN, buff=0.35)
            self.play(FadeIn(bonus, shift=UP * 0.2), run_time=1)
        self.clear()

        with self.beat("Summing infinitely thin slivers") as b:
            ax, al, curve = temp_graph(w=5.6, h=3.2)
            VGroup(ax, al).to_edge(LEFT, buff=0.6).shift(UP * 1.3)
            curve = ax.plot(temp, x_range=[6, 22], color=FUNC, stroke_width=4)
            self.play(FadeIn(ax), FadeIn(al), Create(curve), run_time=1)
            col = 0.6
            r1 = T(r"list: average $= \dfrac{\text{sum of the values}}{\text{how many}}$", 32).move_to([col, 2.6, 0], aligned_edge=LEFT)
            self.play(FadeIn(r1), run_time=0.8)
            b.line(1)
            ts = np.linspace(6.1, 21.9, 70)
            slivers = VGroup(*[Line(ax.c2p(t, 40), ax.c2p(t, temp(t)), color=AREA, stroke_width=2.5) for t in ts])
            self.play(LaggedStart(*[Create(l) for l in slivers], lag_ratio=0.04), run_time=3)
            fill = region(ax, temp, lambda s: 40, 6, 22, opacity=0.45)
            self.play(FadeIn(fill), slivers.animate.set_stroke(opacity=0.35), run_time=1)
            b.line(2)
            r2 = T(r"continuous: average $= \dfrac{\text{total accumulation}}{\text{width of the interval}}$", 32).next_to(r1, DOWN, buff=0.45, aligned_edge=LEFT)
            r2.set_max_width(6.4)
            self.play(FadeIn(r2), run_time=0.8)
            b.line(3)
            r3 = M(r"f_{\text{avg}} = \frac{1}{b - a}\int_a^b f(x)\,dx", 44, ACCUM).next_to(r2, DOWN, buff=0.5, aligned_edge=LEFT)
            self.play(Write(r3), run_time=1.2)
            b.line(4)
            box = formula_box(T("total accumulated, divided by the width of the interval", 28), ACCUM).next_to(r3, DOWN, buff=0.4, aligned_edge=LEFT)
            self.play(FadeIn(box), run_time=0.8)
            b.line(5)
            res = VGroup(M(r"\frac{1}{22 - 6}\int_6^{22} T(t)\,dt \approx 62.9^\circ", 38, ACCUM),
                         M(r"\text{five readings: } 61^\circ", 34, SECANT)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(ax, DOWN, buff=0.7).align_to(ax, LEFT)
            lv = DashedLine(ax.c2p(6, 62.9), ax.c2p(22, 62.9), color=ACCUM, stroke_width=3)
            l5 = DashedLine(ax.c2p(6, 61), ax.c2p(22, 61), color=SECANT, stroke_width=2)
            self.play(Write(res[0]), Create(lv), run_time=1.2)
            self.play(FadeIn(res[1]), Create(l5), run_time=0.8)
        self.clear()

        a_, b_ = 0.5, 4.5
        avg = float(np.mean([f(s) for s in np.linspace(a_, b_, 4001)]))
        with self.beat("Leveling the area") as b:
            ax, al = plot_axes([0, 5, 1], [0, 3, 1], w=7, h=4, coords=False)
            VGroup(ax, al).shift(UP * 0.4)
            curve = ax.plot(f, x_range=[0.2, 4.8], color=FUNC, stroke_width=4)
            labs = VGroup(M("a", 30, DIM).next_to(ax.c2p(a_, 0), DOWN, buff=0.15), M("b", 30, DIM).next_to(ax.c2p(b_, 0), DOWN, buff=0.15))
            shade = region(ax, f, lambda s: 0, a_, b_)
            itag = M(r"\int_a^b f(x)\,dx", 36).move_to(ax.c2p((a_ + b_) / 2, 0.75))
            self.play(FadeIn(ax), FadeIn(al), FadeIn(labs), Create(curve), run_time=1.2)
            self.play(FadeIn(shade), Write(itag), run_time=1)
            b.line(1)
            top = max(f(s) for s in np.linspace(a_, b_, 200)) + 0.35
            walls = VGroup(*[Line(ax.c2p(x0, 0), ax.c2p(x0, top), color=INK, stroke_width=5) for x0 in (a_, b_)])
            self.play(Create(walls), FadeOut(itag), run_time=0.8)
            self.play(shade.animate.set_fill(WATER, opacity=0.75), run_time=1.2)
            b.line(2)
            # the water settles: the surface relaxes toward its level with a little slosh; every frame holds the same
            # amount of water (the slosh term integrates to zero over [a, b]). No morph between shapes (Adder).
            k = ValueTracker(0)

            def surface(s, al_):
                u = (s - a_) / (b_ - a_)
                return avg + (f(s) - avg) * (1 - al_)**2 + 0.22 * np.sin(np.pi * al_) * (1 - al_) * np.cos(7 * al_) * np.sin(2 * np.pi * u)

            water = always_redraw(lambda: region(ax, lambda s: surface(s, k.get_value()), lambda s: 0, a_, b_, color=WATER, opacity=0.75, n=120))
            shine = always_redraw(lambda: ax.plot(lambda s: surface(s, k.get_value()), x_range=[a_, b_], color=WATER_HI, stroke_width=3))
            self.remove(shade)
            self.add(water, shine, curve, walls)
            self.play(k.animate.set_value(1), run_time=4.5, rate_func=linear)
            water.clear_updaters()
            shine.clear_updaters()
            b.line(3)
            line = DashedLine(ax.c2p(0, avg), ax.c2p(5, avg), color=SECANT, stroke_width=3)
            tags = VGroup(M(r"\text{height } f_{\text{avg}}", 30, SECANT).next_to(ax.c2p(5, avg), RIGHT, buff=0.1),
                          M(r"\text{width } b - a", 30, DIM).next_to(labs, DOWN, buff=0.1),
                          T("same area", 30, INK).move_to(ax.c2p((a_ + b_) / 2, avg / 2)))
            self.play(Create(line), FadeIn(tags), run_time=1)
        self.clear()

        with self.beat("The Mean Value Theorem for integrals") as b:
            ax, al = plot_axes([0, 5, 1], [0, 3, 1], w=5.2, h=3.2, coords=False)
            VGroup(ax, al).to_edge(LEFT, buff=0.5).shift(UP * 0.9)
            curve = ax.plot(f, x_range=[0.2, 4.8], color=FUNC, stroke_width=4)
            water = region(ax, lambda s: avg, lambda s: 0, a_, b_, color=WATER, opacity=0.55)
            line = DashedLine(ax.c2p(0, avg), ax.c2p(5, avg), color=SECANT, stroke_width=3)
            labs = VGroup(M("a", 28, DIM).next_to(ax.c2p(a_, 0), DOWN, buff=0.12), M("b", 28, DIM).next_to(ax.c2p(b_, 0), DOWN, buff=0.12),
                          M(r"f_{\text{avg}}", 28, SECANT).next_to(ax.c2p(0, avg), LEFT, buff=0.1))
            self.play(FadeIn(ax), FadeIn(al), FadeIn(water), Create(curve), Create(line), FadeIn(labs), run_time=1.2)
            xs = np.linspace(a_, b_, 4001)
            c = float(xs[np.argmin([abs(f(s) - avg) for s in xs])])
            dot = Dot(ax.c2p(a_, f(a_)), color=TANGENT, radius=0.1)
            self.play(FadeIn(dot), run_time=0.4)
            self.play(MoveAlongPath(dot, ax.plot(f, x_range=[a_, c], color=FUNC)), run_time=1.4)
            fc = M(r"f(c) = f_{\text{avg}}", 30, TANGENT).next_to(dot, DR, buff=0.12)
            self.play(FadeIn(fc), Create(DashedLine(ax.c2p(c, 0), ax.c2p(c, avg), color=TANGENT, stroke_width=2)), run_time=0.6)
            b.line(1)
            col = 1.0
            rows = [M(r"F(x) = \int_a^x f(t)\,dt,\ \text{so } F'(x) = f(x)", 36, ACCUM),
                    M(r"\text{MVT for } F:\ F'(c) = \frac{F(b) - F(a)}{b - a}", 36),
                    M(r"F(b) - F(a) = \int_a^b f(t)\,dt", 36),
                    M(r"\text{so } f(c) = \frac{1}{b - a}\int_a^b f(t)\,dt", 36, TANGENT)]
            rows[0].move_to([col, 2.7, 0], aligned_edge=LEFT)
            for r0, r1 in zip(rows, rows[1:]):
                r1.next_to(r0, DOWN, buff=0.45, aligned_edge=LEFT)
            for r in rows:
                r.set_max_width(6.0)
            self.play(Write(rows[0]), run_time=1.2)
            b.line(2)
            self.play(Write(rows[1]), run_time=1.2)
            b.line(3)
            self.play(Write(rows[2]), run_time=1)
            b.line(4)
            self.play(Write(rows[3]), run_time=1.2)
            thm = formula_box(T(r"If $f$ is continuous on $[a, b]$, then $f(c) = f_{\text{avg}}$ for some $c$ in $[a, b]$.", 32), TANGENT).to_edge(DOWN, buff=0.4)
            self.play(FadeIn(thm), run_time=0.8)
        self.clear()

        g = lambda s: s**2
        ax, _ = plot_axes([0, 4.5, 1], [0, 17, 4], w=4.4, h=3.8)
        fig = VGroup(ax, ax.plot(g, x_range=[0, 4.1], color=FUNC, stroke_width=4), region(ax, g, lambda s: 0, 1, 4, opacity=0.3),
                     DashedLine(ax.c2p(0, 7), ax.c2p(4.4, 7), color=SECANT, stroke_width=3), Dot(ax.c2p(np.sqrt(7), 7), color=TANGENT, radius=0.09),
                     M(r"(\sqrt7,\ 7)", 26, TANGENT).next_to(ax.c2p(np.sqrt(7), 7), UL, buff=0.08))
        self.example("Average value of x squared", r"Find the average value of $f(x) = x^2$ on $[1, 4]$. Then find where $f$ equals its average value.",
                     [r"f_{\text{avg}} = \frac{1}{4 - 1}\int_1^4 x^2\,dx", r"= \frac13\left[\frac{x^3}{3}\right]_1^4", r"= \frac13\left(\frac{64}{3} - \frac13\right)", r"= \frac13 \cdot 21",
                      r"= 7", r"x^2 = 7", r"x = \pm\sqrt7", r"TEXT:$\sqrt7 \approx 2.65$ is in $[1, 4]$; $-\sqrt7$ is not."],
                     at=[1, 2, 2, 2, 3, 4, 4, 5], figure=fig, figure_at=4,
                     notes_graph=dict(fns=[("x^2", 0, 4.1)], xr=(0, 4.5), yr=(0, 17), ystep=4), follow=True)

        with self.beat("Average value is not average rate of change") as b:
            def panel(kind):
                ax, _ = plot_axes([0, 4.5, 1], [0, 17, 4], w=4.6, h=3.4)
                grp = VGroup(ax, ax.plot(g, x_range=[0, 4.1], color=FUNC, stroke_width=4))
                if kind == "rate":
                    grp.add(Line(ax.c2p(1, 1), ax.c2p(4, 16), color=SECANT, stroke_width=4), Dot(ax.c2p(1, 1), color=SECANT), Dot(ax.c2p(4, 16), color=SECANT))
                    cap = VGroup(T("average rate of change", 32, SECANT), M(r"\text{a slope: } \frac{16 - 1}{4 - 1} = 5", 34))
                else:
                    grp.add(region(ax, g, lambda s: 0, 1, 4, opacity=0.3), DashedLine(ax.c2p(1, 7), ax.c2p(4, 7), color=ACCUM, stroke_width=4))
                    cap = VGroup(T("average value", 32, ACCUM), M(r"\text{a height: } \frac13\int_1^4 x^2\,dx = 7", 34))
                return VGroup(grp, cap.arrange(DOWN, buff=0.15).next_to(grp, DOWN, buff=0.3))
            left, right = panel("rate"), panel("value")
            VGroup(left, right).arrange(RIGHT, buff=0.9).move_to(UP * 0.2)
            self.play(FadeIn(left), run_time=1)
            b.line(1)
            self.play(FadeIn(right), run_time=1)
            b.line(2)
            note = M(r"\frac{1}{b - a}\int_a^b f'(x)\,dx = \frac{f(b) - f(a)}{b - a}", 36, DERIV).to_edge(DOWN, buff=0.3)
            self.play(FadeOut(VGroup(left[1], right[1])), Write(note), run_time=1)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(formula_box(M(r"f_{\text{avg}} = \frac{1}{b - a}\int_a^b f(x)\,dx", 48, ACCUM), ACCUM),
                          T("the height of the rectangle with the same area", 36),
                          T("continuous $f$ reaches its average at some $c$", 36, TANGENT)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        ax, _ = plot_axes([0, 6.5, 1], [0, 3, 1], w=5, h=2.8)
        fig1 = VGroup(ax, Line(ax.c2p(0, 2), ax.c2p(2, 2), color=FUNC, stroke_width=4),
                      ax.plot(lambda s: np.sqrt(max(4 - (s - 4)**2, 0)), x_range=[2, 6, 0.01], color=FUNC, stroke_width=4))
        self.example("Example 1: From a graph", r"The graph of $f$ on $[0, 6]$ is a segment at height $2$, then a semicircle of radius $2$. Find the average value of $f$ on $[0, 6]$.",
                     [r"\int_0^6 f(x)\,dx = 2 \cdot 2 + \tfrac12\pi(2)^2", r"= 4 + 2\pi", r"f_{\text{avg}} = \frac{4 + 2\pi}{6}", r"= \frac{2 + \pi}{3} \approx 1.71"],
                     at=[1, 1, 2, 3], figure=fig1,
                     notes_graph=dict(fns=[("2+0*x", 0, 2), ("sqrt(abs(4-(x-4)^2))", 2, 6)], xr=(0, 6.5), yr=(0, 3)))
        ax, _ = plot_axes([0, 3.5, 1], [0, 1.2, 0.5], w=4.6, h=2.6, coords=False)
        fig2 = VGroup(ax, ax.plot(np.sin, x_range=[0, np.pi], color=FUNC, stroke_width=4), region(ax, np.sin, lambda s: 0, 0, np.pi, opacity=0.25),
                      DashedLine(ax.c2p(0, 2 / np.pi), ax.c2p(np.pi, 2 / np.pi), color=SECANT, stroke_width=3), M(r"\tfrac{2}{\pi}", 28, SECANT).next_to(ax.c2p(0, 2 / np.pi), LEFT, buff=0.1))
        self.example("Example 2: Average of sine", r"Find the average value of $\sin x$ on $[0, \pi]$.",
                     [r"f_{\text{avg}} = \frac1\pi\int_0^\pi \sin x\,dx", r"= \frac1\pi\left[-\cos x\right]_0^\pi", r"= \frac1\pi(1 + 1)", r"= \frac2\pi \approx 0.637"],
                     at=[1, 2, 2, 3], figure=fig2, figure_at=3)
        tab = table(["t", "0", "2", "4", "6", "8"], [["T(t)", "60", "64", "70", "68", "62"]], size=34)
        self.example("Example 3: Average temperature from a table", VGroup(T(r"Use a trapezoidal sum with four subintervals to approximate the average temperature over $0 \le t \le 8$.", 38), tab).arrange(DOWN, buff=0.3),
                     [r"\int_0^8 T\,dt \approx \tfrac22\left[T(0) + 2T(2) + 2T(4) + 2T(6) + T(8)\right]", r"= 1\left[60 + 2(64) + 2(70) + 2(68) + 62\right]",
                      r"= 60 + 128 + 140 + 136 + 62", r"= 526", r"\text{average} \approx \frac{526}{8} = 65.75\ ^\circ\text{F}"], at=[1, 2, 3, 3, 4],
                     text=r"A table gives $T(t)$ in $^\circ$F at $t = 0, 2, 4, 6, 8$ hours: $60, 64, 70, 68, 62$. Use a trapezoidal sum with four subintervals to approximate the average temperature over $0 \le t \le 8$.")
        self.finish()
