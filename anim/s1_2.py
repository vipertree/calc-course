"""Topic 1.2: Defining limits and using limit notation. Narration comes from transcripts/1_2.md."""
from manim import *

from kit import *
from style import *


def machine(label):
    box = RoundedRectangle(width=3.4, height=1.8, corner_radius=0.2, color=FUNC, stroke_width=4, fill_color=PANEL, fill_opacity=1)
    funnel = Polygon(LEFT * 0.7 + UP * 1.3, RIGHT * 0.7 + UP * 1.3, RIGHT * 0.25 + UP * 0.9, LEFT * 0.25 + UP * 0.9, color=DIM)
    spout = Rectangle(width=0.5, height=0.4, color=DIM).move_to(DOWN * 1.1)
    return VGroup(box, funnel, spout, M(label, 40, FUNC).move_to(box))


class Lesson(TranscriptScene):
    NUM = "1.2"

    def construct(self):
        # ---------------------------------------------------------------- functions as machines
        mac = machine("f(x) = 2x + 1").scale(1.6)
        with self.beat("Inputs and outputs") as b:
            self.play(FadeIn(mac), run_time=1)
            record = VGroup(M(r"\text{in}", 34, DIM), M(r"\text{out}", 34, DIM)).arrange(RIGHT, buff=0.9).to_edge(RIGHT, buff=1.2).shift(UP * 1.6)
            self.play(mac.animate.shift(LEFT * 1.6), FadeIn(record), run_time=0.8)
            for k, (a, o) in enumerate([("3", "7"), ("0", "1")]):
                b.line(2 + k)
                inp = M(a, 64, SECANT).next_to(mac, UP, buff=0.9)
                self.play(FadeIn(inp, shift=DOWN * 0.3), run_time=0.6)
                self.play(inp.animate.move_to(mac[1].get_center()).set_opacity(0), run_time=1.0)
                self.play(Indicate(mac[0], color=FUNC, scale_factor=1.03), run_time=0.6)
                out = M(o, 64, TANGENT).move_to(mac[2].get_center())
                self.play(out.animate.next_to(mac, DOWN, buff=0.4), run_time=1.0)
                row = VGroup(M(a, 44, SECANT).move_to(record[0]), M(o, 44, TANGENT).move_to(record[1])).shift(DOWN * 0.7 * (k + 1))
                self.play(TransformFromCopy(out, row[1]), FadeIn(row[0]), FadeOut(out), run_time=0.9)
        self.clear()

        top, bot, labs = number_line_pair(0, 9, "x", "f(x)")
        top.set_color(SECANT)
        bot.set_color(TANGENT)
        x = ValueTracker(1.5)
        din = always_redraw(lambda: Dot(top.n2p(x.get_value()), color=SECANT, radius=0.1))
        dout = always_redraw(lambda: Dot(bot.n2p(2 * x.get_value() + 1), color=TANGENT, radius=0.1))
        rin = always_redraw(lambda: DecimalNumber(x.get_value(), num_decimal_places=3, font_size=34, color=SECANT).next_to(din, UP))
        rout = always_redraw(lambda: DecimalNumber(2 * x.get_value() + 1, num_decimal_places=3, font_size=34, color=TANGENT).next_to(dout, DOWN))
        with self.beat("Approaching") as b:
            self.play(Create(top), Create(bot), FadeIn(labs), run_time=1.2)
            self.add(din, dout, rin, rout)
            b.line(1)
            for v in [2.9, 2.99, 2.999]:
                self.play(x.animate.set_value(v), run_time=1)
            b.line(3)
            self.play(Indicate(rout, color=TANGENT), run_time=1)
            b.line(4)
            q = M(r"x = c \text{ not allowed?}", 44, INK).move_to(ORIGIN)
            self.play(FadeIn(q), run_time=0.8)
        self.clear()
        self.title()

        # ---------------------------------------------------------------- the hole
        g = M(r"g(x) = \frac{x^2 - 1}{x - 1}", 56, FUNC).to_edge(UP, buff=0.8)
        with self.beat("A function with a hole") as b:
            self.play(Write(g), run_time=1.5)
            b.line(1)
            sub = M(r"g(1) = \frac{1 - 1}{1 - 1} = \frac{0}{0}", 52, TANGENT).next_to(g, DOWN, buff=0.7)
            self.play(Write(sub), run_time=1.4)
        self.play(FadeOut(sub), g.animate.scale(0.7).to_corner(UR, buff=0.6), run_time=0.8)

        ax, al = plot_axes([-1, 3, 1], [-1, 4, 1], w=7.2, h=5.4)
        VGroup(ax, al).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        line = ax.plot(lambda t: t + 1, x_range=[-1, 3], color=FUNC, stroke_width=5)
        hole = open_dot(ax, 1, 2)
        xv = ValueTracker(0.4)
        mover = always_redraw(lambda: Dot(ax.c2p(xv.get_value(), xv.get_value() + 1), color=SECANT, radius=0.1))
        coord = always_redraw(lambda: M(f"({xv.get_value():.3f},\\ {xv.get_value() + 1:.3f})", 34, SECANT).next_to(g, DOWN, buff=0.8))
        with self.beat("What the graph does near the hole") as b:
            self.play(Create(ax), FadeIn(al), Create(line), run_time=1.6)
            self.play(FadeIn(hole, scale=0.5), run_time=0.5)
            b.line(1)
            self.add(mover, coord)
            for v in [0.9, 0.99, 0.999]:
                self.play(xv.animate.set_value(v), run_time=0.9)
            b.line(2)
            xv.set_value(1.6)
            for v in [1.1, 1.01, 1.001]:
                self.play(xv.animate.set_value(v), run_time=0.9)
            b.line(3)
            self.play(Indicate(hole, color=SECANT, scale_factor=2), run_time=1)
        self.remove(mover, coord)

        # ---------------------------------------------------------------- epsilon game (no Greek letters on screen)
        eps = ValueTracker(0.5)
        band = always_redraw(lambda: Rectangle(width=ax.x_length, height=abs(ax.c2p(0, 2 + eps.get_value())[1] - ax.c2p(0, 2 - eps.get_value())[1]),
                                                fill_color=SECANT, fill_opacity=0.18, stroke_width=0).move_to(ax.c2p(1, 2)))
        win = always_redraw(lambda: Rectangle(height=ax.y_length, width=abs(ax.c2p(1 + eps.get_value(), 0)[0] - ax.c2p(1 - eps.get_value(), 0)[0]),
                                               fill_color=TANGENT, fill_opacity=0.15, stroke_width=0).move_to(ax.c2p(1, 1.5)))
        with self.beat("The closeness game") as b:
            self.add(band)
            self.play(FadeIn(band), run_time=0.6)
            b.line(1)
            self.add(win)
            self.play(FadeIn(win), run_time=0.6)
            b.line(2)
            self.play(eps.animate.set_value(0.1), run_time=1.6)
            self.play(eps.animate.set_value(0.03), run_time=1.4)
            b.line(3)
            lim = M(r"\lim_{x\to1} g(x) = 2", 48, SECANT).next_to(g, DOWN, buff=0.8)
            self.play(Write(lim), run_time=1.2)
            b.line(4)
            note = callout(r"the formal definition: \\ not tested on the AP exam", DIM, 30).next_to(lim, DOWN, buff=0.5)
            self.play(FadeIn(note), run_time=0.8)
        self.clear()

        with self.beat("The definition in words") as b:
            d = VGroup(T(r"The \textbf{limit} of $f(x)$ as $x$ approaches $c$ is $L$", 42),
                       T(r"if $f(x)$ can be made as close to $L$ as we like", 42),
                       T(r"by taking $x$ close enough to $c$,", 42),
                       T(r"but not equal to $c$.", 42, SECANT)).arrange(DOWN, buff=0.35)
            for m in d[:3]:
                self.play(FadeIn(m, shift=UP * 0.2), run_time=0.9)
            b.line(1)
            self.play(FadeIn(d[3], shift=UP * 0.2), run_time=0.8)
            self.play(Circumscribe(d[3], color=SECANT), run_time=1.2)
        self.clear()

        with self.beat("The notation") as b:
            n = MathTex(r"\lim_{x \to 1}", r"g(x)", r"=", r"2", font_size=96)
            n[0].set_color(SECANT)
            n[1].set_color(FUNC)
            n[3].set_color(TANGENT)
            self.play(Write(n), run_time=1.6)
            b.line(1)
            labs2 = VGroup(T("what $x$ is doing", 32, SECANT).next_to(n[0], DOWN, buff=0.6),
                           T("what we watch", 32, FUNC).next_to(n[1], UP, buff=0.6),
                           T("where the outputs head", 32, TANGENT).next_to(n[3], DOWN, buff=0.6))
            for m in labs2:
                self.play(FadeIn(m), run_time=0.7)
        self.clear()
        self.example("Symbols to words", r"$T(t)$ is the temperature in degrees Fahrenheit $t$ hours after noon. Explain the meaning of $\displaystyle\lim_{t\to3} T(t) = 72$.",
                     [r"\text{input: } t \to 3 \ \ (\text{the time approaches 3 PM})", r"\text{output: } T(t) \to 72 \ \ (\text{the temperature approaches } 72^\circ\text{F})", r"TEXT:As the time gets closer and closer to 3 PM, the temperature gets closer and closer to $72^\circ$F."], at=[1, 1, 2])
        self.example("Words to symbols", r"Write in limit notation: ``As $x$ approaches $-2$ from the left, $h(x)$ approaches $7$.''",
                     [r"\text{from the left: } x \to -2^-", r"\lim_{x\to -2^-} h(x) = 7"], at=[1, 2])

        ax2, al2 = plot_axes([-1, 3, 1], [-1, 6, 1], w=7.2, h=5.4)
        VGroup(ax2, al2).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        with self.beat("The point doesn't matter") as b:
            self.play(Create(ax2), FadeIn(al2), Create(ax2.plot(lambda t: t + 1, x_range=[-1, 3], color=FUNC, stroke_width=5)), run_time=1.4)
            self.play(FadeIn(open_dot(ax2, 1, 2)), FadeIn(closed_dot(ax2, 1, 5, SECANT)), run_time=0.8)
            facts = VGroup(M(r"k(1) = 5", 48, SECANT), M(r"\lim_{x\to1} k(x) = 2", 48, FUNC)).arrange(DOWN, buff=0.5, aligned_edge=LEFT).to_edge(RIGHT, buff=0.8)
            self.play(Write(facts[0]), run_time=0.8)
            self.play(Write(facts[1]), run_time=1)
            b.line(1)
            self.play(Circumscribe(facts, color=INK), run_time=1.2)
        self.clear()
        ga, gl = plot_axes([-0.5, 4.5, 1], [-0.5, 6, 1], w=5, h=4.2)
        gfig = VGroup(ga, gl, ga.plot(lambda x: 0.5 * (x - 2) ** 2 + 3, x_range=[-0.5, 4.5], color=FUNC, stroke_width=4), open_dot(ga, 2, 3), closed_dot(ga, 2, 1, FUNC))
        self.example("Reading a graph", r"Use the graph of $f$ to find $f(2)$ and $\displaystyle\lim_{x\to2} f(x)$.",
                     [r"f(2) = 1 \ \ (\text{the filled dot})", r"\lim_{x\to2} f(x) = 3 \ \ (\text{where the graph is heading})"], at=[1, 2], figure=gfig, text=r"Use the graph of $f$ above to find $f(2)$ and \[ \lim_{x\to2} f(x). \]")

        with self.beat("Three ways to see a limit") as b:
            pg = VGroup(*[RoundedRectangle(width=4.2, height=3.4, corner_radius=0.15, color=DIM) for _ in range(3)]).arrange(RIGHT, buff=0.35)
            heads = VGroup(*[T(s_, 34, DIM).next_to(p, UP, buff=0.2) for s_, p in zip(["graph", "table", "formula"], pg)])
            a3, _ = plot_axes([0, 2, 1], [0, 3, 1], w=3.2, h=2.4, coords=False)
            a3.move_to(pg[0])
            gp = VGroup(a3, a3.plot(lambda t: t + 1, x_range=[0, 2], color=FUNC), open_dot(a3, 1, 2))
            tb = table(["x", "g(x)"], [["0.99", "1.99"], ["1.01", "2.01"]], size=30).move_to(pg[1])
            al_ = VGroup(M(r"\frac{(x-1)(x+1)}{x-1}", 36), M(r"\to 2", 36, SECANT)).arrange(DOWN).move_to(pg[2])
            self.play(FadeIn(pg), FadeIn(heads), run_time=0.8)
            self.play(FadeIn(gp), FadeIn(tb), FadeIn(al_), run_time=1.6)
        self.clear()

        with self.beat("Close") as b:
            ax3, al3 = plot_axes([-1, 3, 1], [-1, 4, 1], w=6.4, h=4.6)
            VGroup(ax3, al3).to_edge(LEFT, buff=0.8)
            h3 = open_dot(ax3, 1, 2)
            st = M(r"\lim_{x\to1} g(x) = 2", 52, SECANT).to_edge(RIGHT, buff=0.8)
            self.play(FadeIn(ax3), FadeIn(al3), Create(ax3.plot(lambda t: t + 1, x_range=[-1, 3], color=FUNC, stroke_width=5)), FadeIn(h3), Write(st), run_time=1.6)
            b.line(1)
            self.play(Indicate(h3, scale_factor=2.2, color=SECANT), run_time=1.2)
        self.clear()

        # ---------------------------------------------------------------- worked examples
        self.examples_card()
        tb1 = table(["x", "1.9", "1.99", "2", "2.01", "2.1"], [["f(x)", "4.9", "4.99", r"\tfrac00", "5.01", "5.1"]])
        self.example("Example 1: A limit from a table",
                     r"Estimate $\displaystyle\lim_{x\to2}\frac{x^2 + x - 6}{x - 2}$.",
                     [r"f(2) = \frac{0}{0}\ \text{(undefined)}", tb1, r"\text{left: } 4.9,\ 4.99 \qquad \text{right: } 5.01,\ 5.1",
                      r"\lim_{x\to2}\frac{x^2 + x - 6}{x - 2} = 5"], at=[1, 2, 3, 4],
                     text=r"Estimate $\displaystyle\lim_{x\to2}\frac{x^2 + x - 6}{x - 2}$ using the table. \[ \begin{array}{c|ccccc} x & 1.9 & 1.99 & 2 & 2.01 & 2.1 \\ \hline f(x) & 4.9 & 4.99 & \tfrac00 & 5.01 & 5.1 \end{array} \]")

        a4, _ = plot_axes([0, 4, 1], [0, 5, 1], w=5.6, h=4.4)
        fig = VGroup(a4, a4.plot(lambda t: 3 - 0.6 * (t - 2) ** 2 + 0.3 * (t - 2), x_range=[0.2, 3.8], color=FUNC, stroke_width=4),
                     open_dot(a4, 2, 3), closed_dot(a4, 2, 1, SECANT))
        self.example("Example 2: Value versus limit", r"Find $f(2)$ and $\displaystyle\lim_{x\to2} f(x)$.",
                     [r"f(2) = 1", r"\lim_{x\to2} f(x) = 3"], figure=fig, at=[1, 2],
                     notes_graph=dict(fns=[("3-0.6*(x-2)^2+0.3*(x-2)", 0.2, 3.8)], xr=(0, 4), yr=(0, 5), open=[(2, 3)], closed=[(2, 1)]))

        self.example("Example 3: Words and symbols", r"``As $t$ approaches $4$, $P(t)$ approaches $90$.''",
                     [r"\lim_{t\to4} P(t) = 90", r"\lim_{x\to-1} h(x) = 6", r"\text{``As } x \text{ approaches } -1,\ h(x) \text{ approaches } 6.\text{''}",
                      r"\text{(says nothing about } P(4) \text{ or } h(-1))"], at=[1, 2, 3, 4])
        self.finish()
