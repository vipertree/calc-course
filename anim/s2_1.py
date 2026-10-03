"""Topic 2.1: Average and instantaneous rates of change. Narration comes from transcripts/2_1.md.

Amara's distance from home is s(t) = t^3 - 9t^2 + 24t miles. The average velocity on [1, 4] is 0 (she turned
around); shrinking h settles the secant slopes on s'(1) = 9. Then Zeno's arrow, s(t) = 60t - 12t^2, gets its answer: 36.
"""
import numpy as np
from manim import *

from kit import *
from style import *


def s(t):
    return t ** 3 - 9 * t ** 2 + 24 * t


def avg(h):
    return (s(1 + h) - s(1)) / h


def zeno(t):
    return 60 * t - 12 * t * t


class Lesson(TranscriptScene):
    NUM = "2.1"

    def graph(self):
        ax, al = plot_axes([0, 4.5, 1], [0, 24, 4], w=6.6, h=4.8, xlabel="t", ylabel="s")
        VGroup(ax, al).to_edge(LEFT, buff=0.6).shift(DOWN * 0.4)
        return ax, al

    def secant(self, ax, h, color=SECANT):
        """The line through (1, 16) and (1 + h, s(1 + h)), trimmed to the window."""
        m = avg(h)
        lo, hi = 0.1, min(1 + max(h, 0) + 0.9, 4.5)
        if m > 0:
            lo, hi = max(lo, 1 + (0.5 - 16) / m), min(hi, 1 + (23.5 - 16) / m)
        elif m < 0:
            lo, hi = max(lo, 1 + (23.5 - 16) / m), min(hi, 1 + (0.5 - 16) / m)
        return ax.plot(lambda x: 16 + m * (x - 1), x_range=[lo, hi], color=color, stroke_width=4)

    def construct(self):
        # ---------------------------------------------------------------- Zeno's arrow, again
        arrow = arrow_prop(4.0, angle=FLIGHT_TILT).shift(LEFT * 3 + UP * 0.6)
        outline = DashedVMobject(SurroundingRectangle(arrow, buff=0.08, color=DIM), num_dashes=40)
        rows = [["1", "24"], ["0.5", "30"], ["0.1", "34.8"], ["0.01", "35.88"], ["0.001", "35.988"]]
        tb = table([r"\Delta t", r"\text{average (m/s)}"], rows, size=32).to_edge(RIGHT, buff=0.9).shift(UP * 0.4)
        q = M(r"36\,?", 56, SECANT).next_to(tb, DOWN, buff=0.4)
        with self.beat("Zeno's arrow, again") as b:
            self.play(FadeIn(arrow), Create(outline), run_time=1.2)
            b.line(1)
            self.play(FadeIn(tb, shift=LEFT * 0.3), run_time=1.2)
            self.play(Write(q), run_time=0.8)
            b.line(2)
            self.play(Indicate(q, color=TANGENT), run_time=1)
            b.line(3)
            lim = M(r"\lim", 60, FUNC).next_to(arrow, DOWN, buff=0.8)
            self.play(Write(lim), run_time=0.8)
        self.clear()
        self.title()

        # ---------------------------------------------------------------- Amara's drive
        ax, al = self.graph()
        curve = ax.plot(s, x_range=[0, 4.5], color=FUNC, stroke_width=5)
        road = Line(LEFT * 5.5, RIGHT * 5.5, color=DIM, stroke_width=6).to_edge(UP, buff=0.5)
        house = VGroup(Square(0.4, color=INK, stroke_width=3), Triangle(color=INK, stroke_width=3).scale(0.28).shift(UP * 0.33)).next_to(road.get_left(), UP, buff=0.05)
        tt = ValueTracker(0)
        mile = lambda d: road.point_from_proportion(min(d / 22, 1))
        car = always_redraw(lambda: RoundedRectangle(width=0.55, height=0.28, corner_radius=0.08, color=SECANT, fill_color=SECANT, fill_opacity=1)
                            .move_to(mile(s(tt.get_value())) + UP * 0.2))
        with self.beat("Amara's drive") as b:
            self.play(Create(road), FadeIn(house), FadeIn(car), run_time=1.2)
            b.line(1)
            self.play(FadeIn(ax), FadeIn(al), FadeIn(M(r"s(t) = t^3 - 9t^2 + 24t", 40, FUNC).to_edge(RIGHT, buff=0.6).shift(UP * 1.6)), run_time=1)
            b.line(2)
            self.play(Create(curve), tt.animate.set_value(4.5), run_time=3.5, rate_func=linear)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (ax, al, curve)], run_time=0.5)
        self.remove(car)

        p1 = closed_dot(ax, 1, 16, INK)
        with self.beat("The question") as b:
            self.play(FadeIn(p1, scale=2), FadeIn(M("(1, 16)", 32).next_to(p1, LEFT, buff=0.15)), run_time=0.8)
            b.line(1)
            dial = VGroup(Arc(radius=0.9, start_angle=PI, angle=-PI, color=INK, stroke_width=4), Line(ORIGIN, UP * 0.75 + RIGHT * 0.25, color=TANGENT, stroke_width=5),
                          M("?", 48, TANGENT).shift(DOWN * 0.45)).move_to(RIGHT * 4 + UP * 1)
            self.play(FadeIn(dial), run_time=0.8)
            b.line(2)
            self.play(FadeOut(dial), run_time=0.6)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (ax, al, curve, p1)], run_time=0.4)

        # ---------------------------------------------------------------- the second moment
        h = ValueTracker(3)
        p2 = always_redraw(lambda: closed_dot(ax, 1 + h.get_value(), s(1 + h.get_value()), SECANT))
        brace = always_redraw(lambda: BraceBetweenPoints(ax.c2p(1, 0), ax.c2p(1 + h.get_value(), 0), DOWN, color=SECANT))
        hlab = always_redraw(lambda: M("h", 34, SECANT).next_to(brace, DOWN, buff=0.08))
        with self.beat("Two moments") as b:
            b.line(1)
            self.play(FadeIn(p2, scale=2), run_time=0.6)
            self.play(FadeIn(brace), FadeIn(hlab), run_time=0.8)
        read = always_redraw(lambda: M(rf"h = {h.get_value():.1f} \ \to\ \text{{second time}} = {1 + h.get_value():.1f}", 36).to_edge(RIGHT, buff=0.5).shift(UP * 1.4))
        with self.beat("What one plus h means") as b:
            tick = always_redraw(lambda: M("1 + h", 28, SECANT).next_to(ax.c2p(1 + h.get_value(), 0), UP, buff=0.12))
            self.play(FadeIn(tick), run_time=0.6)
            b.line(2)
            self.play(FadeIn(read), run_time=0.6)
            b.line(3)
            self.play(h.animate.set_value(0.5), run_time=1.6)
            b.line(4)
            self.play(h.animate.set_value(2), run_time=1.2)
            self.play(h.animate.set_value(0.8), run_time=1.2)
            self.play(h.animate.set_value(3), run_time=1.2)
            self.play(FadeOut(tick), FadeOut(read), run_time=0.4)

        with self.beat("Average velocity") as b:
            fr = M(r"\frac{s(1 + h) - s(1)}{h}", 50).to_edge(RIGHT, buff=0.8).shift(UP * 1.6)
            b.line(1)
            self.play(Write(fr), run_time=1.2)
            b.line(2)
            fr2 = M(r"= \frac{s(4) - s(1)}{3}", 46).next_to(fr, DOWN, buff=0.4)
            self.play(Write(fr2), run_time=1)
            b.line(3)
            units = VGroup(T("output units per input unit", 32, SECANT),
                           T(r"miles per hour \quad liters per minute \quad dollars per shirt", 28, DIM)).arrange(DOWN, buff=0.2)
            units.to_edge(DOWN, buff=0.35).to_edge(RIGHT, buff=0.5)
            self.play(FadeIn(units, shift=UP * 0.2), run_time=0.8)
            self.wait(2.5)
            self.play(FadeOut(units), run_time=0.4)
        with self.beat("An average hides things") as b:
            fr3 = M(r"= \frac{16 - 16}{3} = 0", 46, SECANT).next_to(fr2, DOWN, buff=0.4)
            self.play(Write(fr3), run_time=1)
            b.line(2)
            rider = Dot(ax.c2p(1, 16), color=INK, radius=0.11)
            self.play(FadeIn(rider), run_time=0.3)
            self.play(MoveAlongPath(rider, ax.plot(s, x_range=[1, 4])), run_time=3, rate_func=linear)
            self.play(Flash(ax.c2p(2, 20), color=TANGENT), FadeIn(M("20", 30, TANGENT).next_to(ax.c2p(2, 20), UP, buff=0.15)), run_time=0.8)
            self.play(FadeOut(rider), run_time=0.3)
            b.line(3)
            vs = VGroup(T("velocity: includes direction", 36, SECANT),
                        T("speed: ignores direction", 36, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
            vs.next_to(fr3, DOWN, buff=0.5).to_edge(RIGHT, buff=0.4)
            self.play(FadeIn(vs[0]), run_time=0.6)
            self.play(FadeIn(vs[1]), run_time=0.8)
            b.line(4)
            avg = M(r"\text{average velocity} = 0", 38, SECANT).next_to(vs, DOWN, buff=0.4).align_to(vs, LEFT)
            self.play(FadeIn(avg), Indicate(vs[0], color=SECANT), run_time=0.9)
            self.play(FadeOut(vs), FadeOut(avg), run_time=0.4)
        self.play(FadeOut(fr2), FadeOut(fr3), *[FadeOut(m) for m in self.mobjects if isinstance(m, MathTex) and m.tex_string == "20"], run_time=0.5)

        sec = always_redraw(lambda: self.secant(ax, h.get_value()))
        with self.beat("Secant line") as b:
            self.play(Create(sec), run_time=1)
            b.line(1)
            self.play(h.animate.set_value(2), run_time=1)
            tri = VGroup(DashedLine(ax.c2p(1, 16), ax.c2p(3, 16), color=DIM), DashedLine(ax.c2p(3, 16), ax.c2p(3, s(3)), color=DIM))
            self.play(FadeIn(tri), run_time=0.5)
            b.line(2)
            name = T("secant line", 36, SECANT).next_to(fr, DOWN, buff=0.5)
            self.play(FadeIn(name), run_time=0.6)

        # ---------------------------------------------------------------- shrinking h
        all_rows = [["2", "1"], ["1", "4"], ["0.5", "6.25"], ["0.1", "8.41"], ["0.01", "8.9401"]]
        st = table(["h", r"\text{slope}"], all_rows, size=34).to_edge(RIGHT, buff=1.2).shift(UP * 0.4)
        grid = st[0]
        with self.beat("Shrinking h") as b:
            self.play(FadeOut(name), FadeOut(fr), FadeOut(tri), run_time=0.4)
            self.remove(tri)
            self.play(FadeIn(grid[0]), FadeIn(st[1]), run_time=0.6)
            for i, hv in zip((1, 2, 3), (2, 1, 0.5)):
                b.line(i)
                self.play(h.animate.set_value(hv), run_time=1)
                self.play(FadeIn(grid[i], shift=LEFT * 0.2), run_time=0.5)
        with self.beat("Settling on nine") as b:
            self.play(h.animate.set_value(0.1), run_time=1)
            self.play(FadeIn(grid[4], shift=LEFT * 0.2), run_time=0.5)
            b.line(1)
            self.play(h.animate.set_value(0.01), run_time=0.8)
            self.play(FadeIn(grid[5], shift=LEFT * 0.2), run_time=0.5)
            b.line(2)
            nine = M(r"9\,?", 54, TANGENT).next_to(st, DOWN, buff=0.4)
            self.play(Indicate(grid[4][1]), Indicate(grid[5][1]), FadeIn(nine), run_time=1.2)

        with self.beat("Zooming in") as b:
            self.play(h.animate.set_value(0.4), run_time=0.6)
            self.camera.frame.save_state()
            self.play(self.camera.frame.animate.scale(0.12).move_to(ax.c2p(1.15, s(1.15))), run_time=3)
            b.line(1)
            self.play(h.animate.set_value(0.15), run_time=1.5)
            self.play(Restore(self.camera.frame), run_time=2)

        with self.beat("Why h can't be zero") as b:
            self.play(FadeOut(sec), FadeOut(brace), FadeOut(hlab), FadeOut(st), FadeOut(nine), run_time=0.5)
            self.remove(sec, brace, hlab)
            self.play(h.animate.set_value(0.0001), run_time=1.2)
            zz = M(r"\frac{s(1 + 0) - s(1)}{0} = \frac{16 - 16}{0} = \frac{0}{0}", 46).to_edge(RIGHT, buff=0.5).shift(UP * 1.4)
            b.line(1)
            self.play(Write(zz), run_time=1.4)
            self.play(zz.animate.set_color(TANGENT), run_time=0.6)

        with self.beat("The limit") as b:
            self.play(FadeOut(zz), h.animate.set_value(0.5), run_time=0.8)
            b.line(1)
            lim = M(r"\lim_{h\to0}\frac{s(1 + h) - s(1)}{h}", 50).to_edge(RIGHT, buff=0.6).shift(UP * 1.4)
            self.play(Write(lim), run_time=1.4)
            b.line(2)
            dv = M(r"= s'(1)", 50, TANGENT).next_to(lim, DOWN, buff=0.4).align_to(lim, LEFT)
            self.play(Write(dv), run_time=0.8)
            b.line(3)
            nine = M(r"= 9 \text{ mi/hr}", 50, TANGENT).next_to(dv, DOWN, buff=0.3).align_to(lim, LEFT)
            self.play(Write(nine), run_time=0.8)

        with self.beat("The tangent line") as b:
            self.remove(p2)
            for hv in (2, 1, 0.5, 0.1):
                ln = self.secant(ax, hv)
                self.play(FadeIn(ln), run_time=0.35)
                self.play(FadeOut(ln), run_time=0.25)
            tan = tangent_line(ax, s, 1, 9, [0.2, 1.8])
            self.play(Create(tan), run_time=1)
            b.line(1)
            self.play(FadeIn(T("slope 9", 36, TANGENT).next_to(ax.c2p(1.75, 23), RIGHT, buff=0.1)), run_time=0.6)
        self.clear()

        with self.beat("Any function") as b:
            gen = M(r"f'(a) = \lim_{h\to0}\frac{f(a + h) - f(a)}{h}", 64, INK)
            box = formula_box(gen, TANGENT)
            box[0].set_z_index(-1)
            cap = T(r"The derivative of $f$ at $a$", 36, DIM).next_to(box, UP, buff=0.4)
            self.play(FadeIn(cap), Write(gen), run_time=1.6)
            b.line(1)
            self.play(Create(box[0]), run_time=0.8)
        self.clear()

        with self.beat("Two meanings") as b:
            cards = VGroup()
            for key, val in ((("d", "a"), "9 \\text{ mi/hr}"), (("d", "g"), "9")):
                head, sub = MEANINGS[key]
                body = VGroup(T(head, 38, TANGENT), T(sub, 28, DIM), M(val, 54)).arrange(DOWN, buff=0.35)
                rect = RoundedRectangle(width=5.6, height=3.4, corner_radius=0.15, color=DIM, fill_color=PANEL, fill_opacity=1)
                cards.add(VGroup(rect, body))
            cards.arrange(RIGHT, buff=0.6)
            labels = VGroup(T("analytical", 30, DIM).next_to(cards[0], UP), T("graphical", 30, DIM).next_to(cards[1], UP))
            b.line(1)
            self.play(FadeIn(cards[0]), FadeIn(labels[0]), run_time=0.8)
            b.line(2)
            self.play(FadeIn(cards[1]), FadeIn(labels[1]), run_time=0.8)
            b.line(3)
            eq = M("=", 80, SECANT).move_to(cards.get_center())
            self.play(FadeIn(eq, scale=1.5), run_time=0.6)
        self.clear()

        ax, al = self.graph()
        curve = ax.plot(s, x_range=[0, 4.5], color=FUNC, stroke_width=5)
        X = ValueTracker(3)
        with self.beat("The other form") as b:
            self.play(FadeIn(ax), FadeIn(al), Create(curve), run_time=1)
            pa = VGroup(closed_dot(ax, 1, 16, INK), M(r"(a, f(a))", 30).next_to(ax.c2p(1, 16), UL, buff=0.1))
            px = always_redraw(lambda: closed_dot(ax, X.get_value(), s(X.get_value()), SECANT))
            br = always_redraw(lambda: BraceBetweenPoints(ax.c2p(1, 0), ax.c2p(X.get_value(), 0), DOWN, color=SECANT))
            bl = always_redraw(lambda: M(r"h = x - a", 30, SECANT).next_to(br, DOWN, buff=0.08))
            xl = always_redraw(lambda: M("x", 30, SECANT).next_to(ax.c2p(X.get_value(), 0), UP, buff=0.12))
            sec = always_redraw(lambda: self.secant(ax, X.get_value() - 1))
            self.play(FadeIn(pa), FadeIn(px), Create(sec), run_time=0.8)
            b.line(1)
            self.play(FadeIn(br), FadeIn(bl), FadeIn(xl), run_time=0.8)
            b.line(2)
            rd = always_redraw(lambda: VGroup(M(rf"h = {X.get_value() - 1:.2f}", 38, SECANT), M(rf"x = {X.get_value():.2f}", 38, SECANT))
                               .arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=1.2).shift(UP * 1.8))
            self.add(rd)
            self.play(X.animate.set_value(1.05), run_time=3)
            arrows = M(r"h \to 0 \iff x \to a", 42, TANGENT).next_to(rd, DOWN, buff=0.5)
            self.play(FadeIn(arrows), run_time=0.6)
            b.line(3)
            form = M(r"f'(a) = \lim_{x\to a}\frac{f(x) - f(a)}{x - a}", 46, INK).to_edge(RIGHT, buff=0.4).shift(DOWN * 1.2)
            box = SurroundingRectangle(form, color=TANGENT, buff=0.25)
            self.play(Write(form), Create(box), run_time=1.4)
        self.clear()

        self.example("Zeno's arrow, answered",
                     r"The arrow's position is $s(t) = 60t - 12t^2$ meters. Its average velocities near $t = 1$ closed in on $36$ m/s. Use the definition to find $s'(1)$.",
                     [r"s'(1) = \lim_{h\to0}\frac{60(1 + h) - 12(1 + h)^2 - 48}{h}",
                      r"= \lim_{h\to0}\frac{60 + 60h - 12 - 24h - 12h^2 - 48}{h}",
                      r"= \lim_{h\to0}\frac{\cancel{60} + 60h - \cancel{12} - 24h - 12h^2 - \cancel{48}}{h} = \lim_{h\to0}\frac{36h - 12h^2}{h}",
                      r"= \lim_{h\to0}\frac{\cancel{h}(36 - 12h)}{\cancel{h}}", r"= \lim_{h\to0}(36 - 12h) = 36 \text{ m/s}",
                      r"TEXT:The velocity at an instant is the limit of the average velocities around it."], at=[1, 2, 3, 4, 5, 6])
        self.example("The h form", r"Let $f(x) = x^2$. Use the definition to find $f'(3)$.",
                     [r"f'(3) = \lim_{h\to0}\frac{(3 + h)^2 - 9}{h}", r"= \lim_{h\to0}\frac{\cancel{9} + 6h + h^2 - \cancel{9}}{h}",
                      r"= \lim_{h\to0}\frac{\cancel{h}(6 + h)}{\cancel{h}}", r"= \lim_{h\to0}(6 + h) = 6"], at=[1, 2, 3, 4])
        self.example("The x to a form", r"Let $g(x) = \dfrac{1}{x}$. Use the $x \to a$ form of the definition to find $g'(2)$.",
                     [r"g'(2) = \lim_{x\to2}\frac{\frac1x - \frac12}{x - 2} = \lim_{x\to2}\frac{\frac{2 - x}{2x}}{x - 2}", r"= \lim_{x\to2}\frac{2 - x}{2x(x - 2)}",
                      r"= \lim_{x\to2}\frac{-\cancel{(x - 2)}}{2x\cancel{(x - 2)}}", r"= \lim_{x\to2}\left(-\frac{1}{2x}\right) = -\frac14"], at=[1, 2, 3, 4])

        # ---------------------------------------------------------------- worked examples
        self.examples_card()
        a1, _ = plot_axes([0, 10, 2], [0, 4, 1], w=5.6, h=3.6)
        fig1 = VGroup(a1, a1.plot(np.sqrt, x_range=[0, 10], color=FUNC, stroke_width=4),
                      a1.plot(lambda x: 1 + (x - 1) / 4, x_range=[0, 10], color=SECANT, stroke_width=4),
                      closed_dot(a1, 1, 1), closed_dot(a1, 9, 3))
        self.example("Example 1: An average rate of change", r"Find the average rate of change of $f(x) = \sqrt{x}$ on $[1, 9]$.",
                     [r"f(9) = 3, \quad f(1) = 1", r"\frac{f(9) - f(1)}{9 - 1} = \frac{3 - 1}{9 - 1} = \frac{2}{8} = \frac14",
                      r"\text{slope of the secant line}"], figure=fig1, at=[1, 2, 3])
        self.example("Example 2: A derivative from the definition", r"Use the definition to find $f'(2)$ for $f(x) = x^2 + 3x$.",
                     [r"f'(2) = \lim_{h\to0}\frac{(2 + h)^2 + 3(2 + h) - 10}{h}", r"= \lim_{h\to0}\frac{4 + 4h + h^2 + 6 + 3h - 10}{h}",
                      r"= \lim_{h\to0}\frac{\cancel{4} + 4h + h^2 + \cancel{6} + 3h - \cancel{10}}{h} = \lim_{h\to0}\frac{7h + h^2}{h}",
                      r"= \lim_{h\to0}\frac{\cancel{h}(7 + h)}{\cancel{h}}", r"= \lim_{h\to0}(7 + h) = 7"], at=[1, 2, 3, 4, 5])
        self.example("Example 3: Reading a limit as a derivative",
                     r"$\displaystyle\lim_{h\to0}\frac{(3 + h)^3 - 27}{h}$ is $f'(a)$ for some $f$ and $a$. Find $f$, $a$, and the value.",
                     [r"f(x) = x^3, \quad a = 3, \quad f(3) = 27", r"\lim_{h\to0}\frac{\cancel{27} + 27h + 9h^2 + h^3 - \cancel{27}}{h}",
                      r"= \lim_{h\to0}\frac{\cancel{h}(27 + 9h + h^2)}{\cancel{h}}", r"= \lim_{h\to0}(27 + 9h + h^2) = 27"], at=[1, 2, 3, 4])
        self.finish()
