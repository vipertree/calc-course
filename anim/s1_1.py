"""Topic 1.1: Can change occur at an instant? Zeno's arrow, s(t) = 60t - 12t^2. Narration comes from transcripts/1_1.md."""
from manim import *

from kit import *
from style import *


def s(t):
    return 60 * t - 12 * t ** 2


def avg(a, b):
    return (s(b) - s(a)) / (b - a)


QUOTE = (r"``If everything when it occupies an equal space \\ is at rest, and if that which is in locomotion \\ "
         r"is always occupying such a space at any \\ moment, the flying arrow is therefore motionless.''")


class Lesson(TranscriptScene):
    NUM = "1.1"

    def construct(self):
        # ---------------------------------------------------------------- Zeno
        with self.beat("Zeno's arrow") as b:
            bust = zeno_bust(6.0).to_edge(LEFT, buff=0.5).shift(UP * 0.4)
            name = T(r"Zeno of Elea \\ {\footnotesize bust etched by Jan de Bisschop, c.\ 1670}", 30, DIM).next_to(bust, DOWN, buff=0.15)
            self.play(FadeIn(bust, shift=RIGHT * 0.3), FadeIn(name), run_time=1.6)
            b.line(2)
            q = T(QUOTE, 38).set_max_width(8.2).to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
            who = T(r"Aristotle, \emph{Physics} VI.9, \\ describing Zeno's argument", 28, DIM).next_to(q, DOWN, buff=0.4).align_to(q, RIGHT)
            self.play(FadeIn(q), run_time=2.5)
            self.play(FadeIn(who), run_time=1)
        self.clear()

        spots = [(-4.2, 0.2), (-1.9, 1.0), (0.4, 1.3), (2.6, 1.0)]          # where the arrow is at four instants
        arrow = arrow_prop(3.0).move_to(RIGHT * spots[0][0] + UP * spots[0][1])
        outline = always_redraw(lambda: DashedVMobject(SurroundingRectangle(arrow, buff=0.08, color=DIM), num_dashes=30))
        hand = Line(ORIGIN, UP * 0.65, color=INK, stroke_width=4)
        clock = VGroup(Circle(radius=0.8, color=DIM, stroke_width=4), hand, Dot(radius=0.05, color=INK)).move_to(RIGHT * 5.4 + DOWN * 1.6)
        with self.beat("Unpacking the paradox") as b:
            arrow.shift(LEFT * 8)
            self.add(arrow)
            self.play(arrow.animate.shift(RIGHT * 8), FadeIn(clock), run_time=1.6, rate_func=rate_functions.ease_out_cubic)
            self.play(Create(outline), run_time=1.2)
            b.line(2)
            # every instant is a frozen snapshot: the arrow vanishes from one spot and appears, still, in the next
            for x, y in spots[1:]:
                self.play(FadeOut(arrow, run_time=0.25), Rotate(hand, -PI / 3, about_point=clock[0].get_center(), run_time=0.35))
                arrow.move_to(RIGHT * x + UP * y)
                self.play(FadeIn(arrow), run_time=0.25)
                self.wait(0.6)
        self.clear()
        self.title()

        # ---------------------------------------------------------------- one frame, two frames
        with self.beat("What a single frame can't show") as b:
            frame = RoundedRectangle(width=7.0, height=2.6, corner_radius=0.1, color=DIM)
            snap = arrow_prop(2.2).move_to(frame.get_center() + LEFT * 1.6)
            cap = M(r"t = 1\text{ s}", 32, DIM).next_to(frame, DOWN, buff=0.2)
            self.play(Create(frame), FadeIn(snap), FadeIn(cap), run_time=1)
            b.line(1)
            ghost = snap.copy().set_opacity(0.25)
            self.add(ghost)
            self.play(snap.animate.shift(RIGHT * 3.2), Transform(cap, M(r"t = 2\text{ s}", 32, DIM).move_to(cap)), run_time=1.2)
        self.clear()

        # ---------------------------------------------------------------- the graph
        ax, labs = plot_axes([0, 2.5, 0.5], [0, 80, 20], w=7.4, h=5.4, xlabel="t", ylabel="s(t)")
        VGroup(ax, labs).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        curve = ax.plot(s, x_range=[0, 2.5], color=FUNC, stroke_width=5)
        rule = M("s(t) = 60t - 12t^2", 44, FUNC).to_corner(UR, buff=0.6)
        P, Q = closed_dot(ax, 1, 48), closed_dot(ax, 2, 72)
        with self.beat("Distance and time") as b:
            self.play(Create(ax), FadeIn(labs), Write(rule), run_time=1.6)
            self.play(Create(curve), run_time=2)
            b.line(1)
            # the graph is not the flight path: an inset of the real arc, and what the vertical axis records
            ground = Line(LEFT * 2.4, RIGHT * 2.4, color=DIM, stroke_width=3)
            arc = ArcBetweenPoints(ground.get_start(), ground.get_end(), angle=-PI / 2.2, color=DIM, stroke_width=2)
            dashed = DashedVMobject(arc, num_dashes=24)
            fly = arrow_prop(1.5).rotate(-0.5).move_to(arc.point_from_proportion(0.62))
            dist = BraceBetweenPoints(ground.get_start(), np.array([fly.get_center()[0], ground.get_start()[1], 0]), DOWN, color=SECANT)
            inset = Group(ground, dashed, fly, dist, M(r"s(t)", 30, SECANT).next_to(dist, DOWN, buff=0.08),
                          T("the real flight", 30, DIM).next_to(arc, UP, buff=0.35))
            inset.scale(1.15).next_to(rule, DOWN, buff=0.8)
            self.play(FadeIn(inset), run_time=1)
            axis_words = VGroup(T("time", 28, DIM).next_to(ax.x_axis, DOWN, buff=0.45).align_to(ax.x_axis, RIGHT),
                                T(r"= distance from the bow", 26, SECANT).next_to(labs[1], RIGHT, buff=0.15))
            self.play(FadeIn(axis_words), Indicate(labs[1], color=SECANT), run_time=1.2)
            b.line(2)
            self.play(FadeOut(inset), run_time=0.6)
            self.play(FadeIn(P, scale=0.5), FadeIn(M("(1, 48)", 26).next_to(P, UL, buff=0.08)), run_time=0.6)
            self.play(FadeIn(Q, scale=0.5), FadeIn(M("(2, 72)", 26).next_to(Q, DR, buff=0.08)), run_time=0.6)

        with self.beat("Average velocity") as b:
            run = DashedLine(ax.c2p(1, 48), ax.c2p(2, 48), color=DIM)
            rise = DashedLine(ax.c2p(2, 48), ax.c2p(2, 72), color=DIM)
            sec = secant_line(ax, s, 1, 2, [0.4, 2.5])
            q = M(r"\frac{72 - 48}{2 - 1} = 24\ \text{m/s}", 38, SECANT).next_to(rule, DOWN, buff=0.6)
            self.play(Create(run), Create(rise), run_time=1)
            self.play(Write(q), run_time=1.4)
            b.line(1)
            box = callout(r"average rate of change $= \dfrac{\text{change in output}}{\text{change in input}}$", INK, 26).next_to(q, DOWN, buff=0.4)
            self.play(FadeIn(box), run_time=0.8)
            b.line(2)
            self.play(Create(sec), run_time=1.2)
            b.line(3)
            circ = Circle(radius=0.9, color=DIM, stroke_width=3)
            pts = [circ.point_at_angle(a) for a in (2.4, -0.3)]
            geo = VGroup(circ, Line(pts[0] + (pts[0] - pts[1]) * 0.35, pts[1] + (pts[1] - pts[0]) * 0.35, color=SECANT, stroke_width=4),
                         *[Dot(p_, color=INK, radius=0.06) for p_ in pts])
            geo.add(T("a secant of a circle", 24, DIM).next_to(circ, DOWN, buff=0.15))
            geo.next_to(box, DOWN, buff=0.4)
            self.play(FadeIn(geo), run_time=0.8)
        self.play(FadeOut(box), FadeOut(run), FadeOut(rise), FadeOut(geo), run_time=0.5)

        with self.beat("An average isn't an instant") as b:
            speed = M(r"\text{speed} \approx 36", 32, TANGENT).next_to(q, DOWN, buff=0.6)
            tr = ValueTracker(1)
            ghost = always_redraw(lambda: Dot(ax.c2p(tr.get_value(), s(tr.get_value())), color=TANGENT, radius=0.1))
            self.add(ghost)
            self.play(FadeIn(speed), run_time=0.5)
            self.play(tr.animate.set_value(2), Transform(speed, M(r"\text{speed} \approx 12", 32, TANGENT).move_to(speed)), run_time=3, rate_func=linear)
            b.line(2)
            self.play(Indicate(P, scale_factor=1.8, color=TANGENT), run_time=1.2)
        self.play(FadeOut(ghost), FadeOut(speed), run_time=0.4)

        # ---------------------------------------------------------------- shrinking
        h = ValueTracker(1)
        Qm = always_redraw(lambda: closed_dot(ax, 1 + h.get_value(), s(1 + h.get_value()), SECANT))
        secm = always_redraw(lambda: secant_line(ax, s, 1, 1 + h.get_value(), [0.3, 2.5]))
        self.remove(sec, Q)
        self.add(secm, Qm)
        rows = [("1", "24"), ("0.5", "30"), ("0.1", "34.8"), ("0.01", "35.88"), ("0.001", "35.988")]
        tb = table([r"\Delta t", r"\text{average (m/s)}"], [[a, v] for a, v in rows], size=32)
        tb.scale(0.95).next_to(rule, DOWN, buff=0.5)
        self.play(FadeOut(q), run_time=0.4)
        with self.beat("Shrinking the interval") as b:
            self.play(FadeIn(tb[1]), FadeIn(tb[0][0]), run_time=0.6)
            self.play(FadeIn(tb[0][1]), run_time=0.5)
            for i, dt in zip(range(1, 5), [0.5, 0.1, 0.01, 0.001]):
                b.line(i if i < 4 else 3)
                self.play(h.animate.set_value(dt), FadeIn(tb[0][i + 1]), run_time=1.0)
            b.line(4)
            target = M(r"\to 36\,?", 34, TANGENT).next_to(tb, RIGHT, buff=0.3)
            self.play(FadeIn(target), run_time=0.6)

        with self.beat("From the other side") as b:
            extra = table([r"\Delta t", r"\text{average}"], [["-0.1", "37.2"], ["-0.01", "36.12"]], size=30)
            extra[0][0].set_opacity(0)
            extra[1].set_opacity(0)
            extra.scale(0.95).next_to(tb, DOWN, buff=0.05).align_to(tb, LEFT)
            self.play(h.animate.set_value(-0.1), FadeIn(extra[0][1]), run_time=1)
            self.play(h.animate.set_value(-0.01), FadeIn(extra[0][2]), run_time=1)
            b.line(1)
            self.play(Indicate(target, color=TANGENT), run_time=1)

        with self.beat("Why not zero?") as b:
            self.play(h.animate.set_value(0.0001), run_time=1.2)
            zz = M(r"\frac{48 - 48}{1 - 1} = \frac{0}{0}\ ?", 40, TANGENT).next_to(ax, RIGHT, buff=0.3).shift(DOWN * 1.5)
            b.line(1)
            self.play(FadeOut(tb), FadeOut(extra), FadeOut(target), Write(zz), run_time=1.4)
            b.line(2)
            self.play(Indicate(zz, color=TANGENT), run_time=1)
        self.clear()
        self.example("Two average velocities", r"The arrow's position is $s(t) = 60t - 12t^2$ meters. Find its average velocity (a) from $t = 0$ to $t = 2$ and (b) from $t = 1$ to $t = 2$.",
                     [r"s(0) = 0, \quad s(1) = 48, \quad s(2) = 72", r"\text{(a) } \frac{s(2) - s(0)}{2 - 0} = \frac{72 - 0}{2} = 36 \text{ m/s}", r"\text{(b) } \frac{s(2) - s(1)}{2 - 1} = \frac{72 - 48}{1} = 24 \text{ m/s}", r"TEXT:The arrow is slowing down, so its later average is smaller."], at=[1, 2, 3, 4])
        sprint = table(["t", "0", "1", "2", "3", "4"], [["D(t)", "0", "3", "9", "17", "26"]], size=38)
        self.example("A sprinter", r"A sprinter's distance $D(t)$, in meters, $t$ seconds after the start is in the table. Estimate the sprinter's speed at $t = 2$ seconds.",
                     [r"\text{shortest interval with } t = 2 \text{ in the middle: } [1, 3]", r"\frac{D(3) - D(1)}{3 - 1} = \frac{17 - 3}{2} = 7 \text{ m/s}"], at=[1, 2], figure=sprint, text=r"A sprinter's distance $D(t)$ in meters, $t$ seconds after the start: \par\smallskip\centerline{\begin{tabular}{c|ccccc} $t$ (s) & 0 & 1 & 2 & 3 & 4 \\ \hline $D(t)$ (m) & 0 & 3 & 9 & 17 & 26 \end{tabular}} \par Estimate the sprinter's speed at $t = 2$ seconds.")

        # ---------------------------------------------------------------- closer, but still an interval
        col = VGroup(*[M(v, 48) for v in ["24", "30", "34.8", "35.88", "35.988"]]).arrange(DOWN, buff=0.25).shift(LEFT * 3)
        tgt = M("36", 80, TANGENT).shift(RIGHT * 1.2)
        with self.beat("Closer and closer") as b:
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.3) for m in col], lag_ratio=0.2), FadeIn(tgt), run_time=2)
            b.line(1)
            ring = Circle(radius=0.55, color=SECANT).move_to(col[-1])
            self.play(Create(ring), run_time=0.8)
            b.line(2)
            mag = Group(Circle(radius=1.6, color=SECANT, stroke_width=4), arrow_prop(1.4)).move_to(RIGHT * 4.3 + DOWN * 0.6)
            lab = M(r"[1,\ 1.001]", 28, DIM).next_to(mag, DOWN, buff=0.2)
            self.play(FadeIn(mag), FadeIn(lab), run_time=0.8)
            self.play(mag[1].animate.shift(RIGHT * 0.35), run_time=2, rate_func=linear)
        self.clear()

        with self.beat("The question stays open") as b:
            a2 = arrow_prop(5.0).shift(LEFT * 1.8)
            ol = DashedVMobject(SurroundingRectangle(a2, buff=0.08, color=DIM), num_dashes=40)
            self.play(FadeIn(a2), Create(ol), run_time=1)
            b.line(1)
            qq = M(r"36\ ?", 80, TANGENT).shift(RIGHT * 3)
            self.play(Write(qq), run_time=1)
            b.line(3)
            lim = T(r"the tool: a \emph{limit}", 48, SECANT).shift(DOWN * 2.2)
            self.play(FadeIn(lim), run_time=0.8)
        self.clear()

        # ---------------------------------------------------------------- worked examples
        self.examples_card()
        ax1, _ = plot_axes([0, 5, 1], [-3, 5, 1], w=4.6, h=3.8)
        f = lambda x: x * x - 3 * x
        fig1 = VGroup(ax1, ax1.plot(f, x_range=[0, 4.6], color=FUNC, stroke_width=4), secant_line(ax1, f, 1, 4, [0.4, 4.6]),
                      closed_dot(ax1, 1, -2), closed_dot(ax1, 4, 4))
        self.example("Example 1: An average rate from a formula",
                     r"Find the average rate of change of $f(x) = x^2 - 3x$ on $[1, 4]$.",
                     [r"f(4) = 16 - 12 = 4", r"f(1) = 1 - 3 = -2", r"\frac{4 - (-2)}{4 - 1}", r"= \frac{6}{3} = 2"], figure=fig1, at=[1, 1, 2, 3])

        kettle = table(["t", "0", "2", "5", "6", "9"], [["H(t)", "20", "34", "52", "57", "70"]], size=32)
        self.example("Example 2: A rate from a table",
                     VGroup(T(r"Kettle temperature $H(t)$, $^\circ$C, after $t$ minutes. Estimate the rate at $t = 4$.", 32), kettle).arrange(DOWN, buff=0.35),
                     [r"\text{closest times on each side: } t = 2 \text{ and } t = 5", r"\frac{H(5) - H(2)}{5 - 2} = \frac{52 - 34}{3}",
                      r"= 6\ ^\circ\text{C per minute}"], at=[3, 3, 4],
                     text=r"A kettle's temperature $H(t)$, in $^\circ$C, after $t$ minutes: \[ \begin{array}{c|ccccc} t & 0 & 2 & 5 & 6 & 9 \\ \hline H(t) & 20 & 34 & 52 & 57 & 70 \end{array} \] Estimate how fast the temperature is rising at $t = 4$.")

        self.example("Example 3: Shrinking an interval",
                     r"Estimate the rate of change of $g(x) = x^3$ at $x = 2$.",
                     [r"[2,\ 2.1]: \frac{9.261 - 8}{0.1} = 12.61", r"[2,\ 2.01]: 12.0601", r"[1.99,\ 2]: 11.9401",
                      r"\text{closing in on } 12"], at=[1, 2, 3, 4])
        self.finish()
