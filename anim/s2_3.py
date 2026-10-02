"""Topic 2.3: Estimating derivatives of a function at a point. Narration comes from transcripts/2_3.md."""
import numpy as np
from manim import *

from kit import *
from style import *

TS = [0, 2, 5, 7, 10]
TEMP = [48, 55, 63, 66, 64]
_fit = np.polyfit(TS, TEMP, 4)


def temp(t):
    return float(np.polyval(_fit, t))


def temp_table(size=40):
    return table(["t\\text{ (hr)}"] + [str(t) for t in TS], [["T\\ (^\\circ\\text{F})"] + [str(v) for v in TEMP]], size=size)


class Lesson(TranscriptScene):
    NUM = "2.3"

    def construct(self):
        with self.beat("When there's no formula") as b:
            tb = temp_table(44)
            self.play(FadeIn(tb, shift=UP * 0.3), run_time=1.2)
            nof = T(r"no formula", 40, DIM).next_to(tb, DOWN, buff=0.8)
            self.play(FadeIn(nof), run_time=0.6)
            b.line(1)
            self.play(FadeIn(M(r"T'(6) \approx\ ?", 50, TANGENT).next_to(nof, DOWN, buff=0.5)), run_time=0.8)
        self.clear()
        self.title()

        tb = temp_table(40).to_edge(UP, buff=0.6)
        cells = tb.cells
        with self.beat("Using the closest data") as b:
            self.play(FadeIn(tb), run_time=0.6)
            tgt = VGroup(Arrow(UP * 0.5, DOWN * 0.1, color=TANGENT, buff=0), M("t = 6", 32, TANGENT))
            tgt[1].next_to(tgt[0], UP, buff=0.1)
            tgt.next_to(VGroup(cells[0][3], cells[0][4]), UP, buff=0.05)
            self.play(FadeIn(tgt), run_time=0.6)
            boxes = VGroup(*[SurroundingRectangle(VGroup(cells[0][c], cells[1][c]), color=SECANT, buff=0.12) for c in (3, 4)])
            self.play(Create(boxes), run_time=0.8)
            b.line(1)
            q = M(r"\frac{66 - 63}{7 - 5} = \frac{3}{2} = 1.5", 54).shift(DOWN * 0.6)
            self.play(Write(q), run_time=1.4)
            b.line(2)
            est = M(r"T'(6) \approx 1.5\ ^\circ\text{F per hour}", 50, TANGENT).next_to(q, DOWN, buff=0.6)
            self.play(Write(est), run_time=1)
        self.clear()

        ax, al = plot_axes([0, 10, 2], [40, 70, 10], w=7, h=4.4, xlabel="t", ylabel="T")
        VGroup(ax, al).to_edge(LEFT, buff=0.8).shift(DOWN * 0.6)
        with self.beat("Why the closest points") as b:
            pts = VGroup(*[closed_dot(ax, t, v, INK) for t, v in zip(TS, TEMP)])
            self.play(FadeIn(ax), FadeIn(al), FadeIn(pts), Create(ax.plot(temp, x_range=[0, 10], color=FUNC, stroke_width=3).set_opacity(0.5)), run_time=1.2)
            wide = ax.plot(lambda t: 55 + 9 / 8 * (t - 2), x_range=[1, 10], color=DIM, stroke_width=4)
            near = ax.plot(lambda t: 63 + 1.5 * (t - 5), x_range=[3.5, 8.5], color=SECANT, stroke_width=4)
            self.play(Create(wide), FadeIn(M(r"[2, 10]:\ \tfrac{9}{8}", 38, DIM).to_edge(RIGHT, buff=0.8).shift(UP * 1.4)), run_time=1)
            self.play(Create(near), FadeIn(M(r"[5, 7]:\ 1.5", 38, SECANT).to_edge(RIGHT, buff=0.8).shift(UP * 0.5)), run_time=1)
            b.line(1)
            self.play(Create(tangent_line(ax, temp, 6, 1.525, [4.3, 7.7])), run_time=1)
        self.clear()

        g = lambda x: 0.12 * (x - 1) ** 3 - 0.3 * (x - 1) + 2
        dg = lambda x: 0.36 * (x - 1) ** 2 - 0.3
        a2, _ = plot_axes([0, 5, 1], [0, 6, 1], w=7.4, h=5, coords=False)
        a2.shift(DOWN * 0.3)
        with self.beat("Symmetric intervals") as b:
            a, h = 3, 1
            self.play(FadeIn(a2), Create(a2.plot(g, x_range=[0, 5], color=FUNC, stroke_width=5)), FadeIn(closed_dot(a2, a, g(a), INK)), run_time=1.2)
            self.play(Create(tangent_line(a2, g, a, dg(a), [1.5, 4.5])), run_time=0.8)
            one = a2.plot(lambda x: g(a) + (g(a + h) - g(a)) / h * (x - a), x_range=[2, 4.6], color=DIM, stroke_width=4)
            self.play(Create(one), FadeIn(T("one-sided", 30, DIM).next_to(a2.c2p(4.6, 6), DOWN)), run_time=1)
            sym = a2.plot(lambda x: g(a) + (g(a + h) - g(a - h)) / (2 * h) * (x - a), x_range=[1.6, 4.4], color=SECANT, stroke_width=4)
            self.play(Create(sym), FadeIn(closed_dot(a2, a - h, g(a - h), SECANT)), FadeIn(closed_dot(a2, a + h, g(a + h), SECANT)),
                      FadeIn(T("centered", 30, SECANT).to_edge(RIGHT, buff=0.8).shift(DOWN * 0.5)), run_time=1)
        self.clear()

        tab = table(["t", "0", "2", "5", "7", "10"], [["T(t)", "48", "55", "63", "66", "64"]], size=36)
        self.example("Only one side", r"Using the table, estimate $T'(10)$.",
                     [r"\text{no data after } 10:\ \text{use } t = 7 \text{ and } t = 10", r"T'(10) \approx \frac{T(10) - T(7)}{10 - 7} = \frac{64 - 66}{3} = -\frac23 \ ^\circ\text{F/hr}",
                      r"TEXT:The temperature is dropping at about $\frac23$ of a degree per hour."], figure=tab, at=[1, 2, 3],
                     text=r"Using the temperature table above, estimate $T'(10)$.")

        c = lambda x: 2 + (x - 3) + 0.15 * (x - 3) ** 2
        a3, al3 = plot_axes([0, 6, 1], [0, 7, 1], w=7, h=5)
        VGroup(a3, al3).shift(DOWN * 0.3)
        with self.beat("Reading a graph") as b:
            grid = NumberPlane(x_range=[0, 6, 1], y_range=[0, 7, 1], x_length=7, y_length=5,
                               background_line_style={"stroke_color": DIM, "stroke_opacity": 0.25, "stroke_width": 1}, axis_config={"stroke_opacity": 0})
            grid.move_to(a3.c2p(3, 3.5))
            self.play(FadeIn(grid), FadeIn(a3), FadeIn(al3), Create(a3.plot(c, x_range=[0, 6], color=FUNC, stroke_width=5)), run_time=1.2)
            self.play(Create(a3.plot(lambda x: x - 1, x_range=[0.6, 5.8], color=TANGENT, stroke_width=4)), FadeIn(closed_dot(a3, 3, 2, INK)), run_time=1)
            for p in ((1, 0), (5, 4)):
                self.play(FadeIn(closed_dot(a3, *p, SECANT)), FadeIn(M(str(p), 30, SECANT).next_to(a3.c2p(*p), RIGHT, buff=0.15)), run_time=0.5)
            b.line(1)
            run = DashedLine(a3.c2p(1, 0), a3.c2p(5, 0), color=SECANT)
            rise = DashedLine(a3.c2p(5, 0), a3.c2p(5, 4), color=SECANT)
            self.play(Create(run), Create(rise), FadeIn(M(r"\frac{4}{4} = 1", 44, TANGENT).next_to(a3.c2p(5.5, 2), RIGHT)), run_time=1)
        self.clear()

        with self.beat("Calculators") as b:
            panel = RoundedRectangle(width=8, height=3.6, corner_radius=0.2, color=DIM, fill_color=PANEL, fill_opacity=1)
            rows = VGroup(M(r"f(x) = x^3", 46), M(r"\frac{d}{dx} f(x)\Big|_{x = 1.5}", 46), M(r"= 6.75", 46, DERIV)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(panel)
            self.play(FadeIn(panel), run_time=0.5)
            for r in rows:
                self.play(Write(r), run_time=0.8)
        self.clear()

        a4, al4 = plot_axes([-2, 2, 1], [0, 2, 1], w=6, h=3.6)
        VGroup(a4, al4).shift(DOWN * 0.5)
        with self.beat("A calculator trap") as b:
            self.play(FadeIn(a4), FadeIn(al4), Create(a4.plot(abs, x_range=[-2, 2], color=FUNC, stroke_width=5, use_smoothing=False)), run_time=1.2)
            sym = DashedLine(a4.c2p(-1, 1), a4.c2p(1, 1), color=SECANT)
            self.play(Create(sym), FadeIn(closed_dot(a4, -1, 1, SECANT)), FadeIn(closed_dot(a4, 1, 1, SECANT)), run_time=0.8)
            self.play(FadeIn(M(r"\frac{|1| - |-1|}{2} = 0", 42, SECANT).to_edge(UP, buff=0.5)), run_time=0.8)
            b.line(1)
            warn = callout("no tangent line here", TANGENT, 34).next_to(a4.c2p(0, 0), UP, buff=1.8).shift(RIGHT * 3)
            self.play(Flash(a4.c2p(0, 0), color=TANGENT), FadeIn(warn), run_time=1)
        self.clear()

        with self.beat("Close") as b:
            tb = temp_table(40).shift(UP * 1)
            est = M(r"T'(6) \approx 1.5\ ^\circ\text{F per hour}", 50, TANGENT)
            box = formula_box(est, TANGENT).next_to(tb, DOWN, buff=0.8)
            self.play(FadeIn(tb), FadeIn(box), run_time=1.2)
        self.clear()

        self.examples_card()
        bt = table([r"t\text{ (hr)}", "0", "3", "5", "8", "12"], [["B(t)", "200", "260", "310", "400", "520"]], size=36)
        for cc in (2, 3):
            bt.cells[0][cc].set_color(SECANT)
            bt.cells[1][cc].set_color(SECANT)
        self.example("Example 1: A rate from a table, with units",
                     VGroup(T(r"Bacteria are counted every few hours. Estimate $B'(4)$ and explain its meaning.", 38), bt).arrange(DOWN, buff=0.3),
                     [r"\text{closest times: } t = 3 \text{ and } t = 5", r"\frac{B(5) - B(3)}{5 - 3} = \frac{310 - 260}{2} = 25",
                      r"B'(4) \approx 25 \text{ bacteria per hour}", r"TEXT:At 4 hours, the population grows by about 25 bacteria per hour."], at=[1, 2, 3, 4],
                     text=r"Bacteria are counted every few hours. \[ \begin{array}{c|ccccc} t\text{ (hr)} & 0 & 3 & 5 & 8 & 12 \\ \hline B(t) & 200 & 260 & 310 & 400 & 520 \end{array} \] Estimate $B'(4)$ and explain its meaning.")
        a5, _ = plot_axes([-3, 5, 1], [0, 8, 1], w=6, h=5)
        cf = lambda x: 3.5 - 0.5 * (x - 1) + 0.1 * (x - 1) ** 2
        fig = VGroup(a5, a5.plot(cf, x_range=[-3, 5], color=FUNC, stroke_width=4), a5.plot(lambda x: 3.5 - 0.5 * (x - 1), x_range=[-3, 5], color=TANGENT, stroke_width=4),
                     closed_dot(a5, -2, 5, SECANT), closed_dot(a5, 4, 2, SECANT), DashedLine(a5.c2p(-2, 5), a5.c2p(4, 5), color=SECANT),
                     DashedLine(a5.c2p(4, 5), a5.c2p(4, 2), color=SECANT))
        self.example("Example 2: A slope from a tangent line on a graph", r"The tangent line to $f$ at $x = 1$ is drawn. Estimate $f'(1)$.",
                     [r"(-2, 5) \text{ and } (4, 2)", r"\text{rise} = 2 - 5 = -3, \quad \text{run} = 4 - (-2) = 6", r"f'(1) \approx \frac{-3}{6} = -\frac12"],
                     figure=fig, at=[1, 2, 3],
                     notes_graph=dict(fns=[("3.5-0.5*(x-1)+0.1*(x-1)^2", -3, 5), ("3.5-0.5*(x-1)", -3, 5, "dashed")], xr=(-3, 5), yr=(0, 8),
                                      closed=[(-2, 5), (4, 2)]))
        self.example("Example 3: A centered estimate", r"Estimate $f'(4)$ for $f(x) = \sqrt{x}$ using $x = 3.99$ and $x = 4.01$.",
                     [r"\frac{\sqrt{4.01} - \sqrt{3.99}}{4.01 - 3.99}", r"\approx 0.25000", r"\text{exact: } f'(4) = \frac14"], at=[1, 2, 3])
        self.finish()
