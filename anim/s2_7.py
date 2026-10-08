"""Topic 2.7: Derivatives of cos x, sin x, e^x and ln x. Narration comes from transcripts/2_7.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def trig_axes(yl, x0=0.0, u=1.25):
    """Two stacked graphs over [x0, 2 pi], the function above and its slope below. Both axes use the same scale
    (u scene units per 1 on x and on y), so a slope of 1 really looks like 45 degrees."""
    xr, yr = [x0, 2 * PI, PI / 2], [-1.2, 1.2, 1]
    top, tl = plot_axes(xr, yr, w=(2 * PI - x0) * u, h=2.4 * u, coords=False, ylabel=yl[0])
    bot, bl = plot_axes(xr, yr, w=(2 * PI - x0) * u, h=2.4 * u, coords=False, ylabel=yl[1])
    g = VGroup(VGroup(top, tl), VGroup(bot, bl)).arrange(DOWN, buff=0.45).shift(DOWN * 0.2)
    names = {-PI / 2: r"-\tfrac{\pi}{2}", PI / 2: r"\tfrac{\pi}{2}", PI: r"\pi", 3 * PI / 2: r"\tfrac{3\pi}{2}", 2 * PI: r"2\pi"}
    ticks = VGroup(*[M(t, 26, DIM).next_to(ax.c2p(v, 0), DOWN, buff=0.12) for ax in (top, bot) for v, t in names.items() if v >= x0 - 1e-9])
    ticks.add(*[M(t, 24, DIM).next_to(ax.c2p(0, v), LEFT, buff=0.12) for ax in (top, bot) for v, t in ((1, "1"), (-1, "-1"))])
    return top, bot, VGroup(g, ticks)


class Lesson(TranscriptScene):
    NUM = "2.7"

    def slide(self, fn, dfn, yl, color_out, stops, b=None):
        top, bot, g = trig_axes(yl)
        x = ValueTracker(0.001)
        tan = always_redraw(lambda: top.plot(lambda t: fn(x.get_value()) + dfn(x.get_value()) * (t - x.get_value()),
                                             x_range=[max(0, x.get_value() - 0.7), min(2 * PI, x.get_value() + 0.7)], color=TANGENT, stroke_width=4))
        dot = always_redraw(lambda: closed_dot(top, x.get_value(), fn(x.get_value()), INK))
        # the slope graph is redrawn up to the current x each frame (a TracedPath dropped points on long, fast moves)
        trace = always_redraw(lambda: bot.plot(dfn, x_range=[0, max(x.get_value(), 0.002), 0.01], color=color_out, stroke_width=5))
        self.play(FadeIn(g), Create(top.plot(fn, x_range=[0, 2 * PI], color=FUNC, stroke_width=4)), run_time=1)
        self.play(FadeIn(dot), Create(tan), run_time=0.6)
        self.add(trace)
        for i, xv in stops:
            if b is not None and i is not None:
                b.line(i)
            self.play(x.animate.set_value(xv), run_time=1.4 if xv - x.get_value() < 2 else 2.4, rate_func=linear)
            self.add(closed_dot(bot, xv, dfn(xv), color_out))
        return top, bot, g

    def construct(self):
        with self.beat("Sliding along a sine wave") as b:
            top, bot, g = trig_axes(("y", r"\text{slope}"), x0=-PI / 2)
            self.play(FadeIn(g), Create(top.plot(np.sin, x_range=[-PI / 2, 2 * PI], color=FUNC, stroke_width=4)), run_time=1.2)
            self.play(FadeIn(M(r"y = \sin x", 38, FUNC).next_to(top.c2p(2 * PI, 0), RIGHT, buff=0.25).shift(UP * 0.5)), run_time=0.6)

            def estimate(xv, slope, extra=()):
                """The tangent line at xv, a dot on it, then its slope dropped onto the slope graph below."""
                tan = tangent_line(top, np.sin, xv, slope, [xv - 1.1, xv + 1.1])
                d = closed_dot(top, xv, np.sin(xv), INK)
                self.play(FadeIn(d), Create(tan), *extra, run_time=1)
                rec = closed_dot(bot, xv, slope, DERIV)
                drop = DashedLine(top.c2p(xv, np.sin(xv)), bot.c2p(xv, slope), color=DIM, stroke_width=2)
                self.play(Create(drop), run_time=0.6)
                self.play(FadeIn(rec, scale=2), run_time=0.5)
                self.play(FadeOut(drop), tan.animate.set_stroke(opacity=0.35), run_time=0.4)
                return rec

            b.line(1)
            run = DashedLine(top.c2p(0, 0), top.c2p(1, 0), color=SECANT, stroke_width=3)
            rise = DashedLine(top.c2p(1, 0), top.c2p(1, 1), color=SECANT, stroke_width=3)
            rr = VGroup(run, rise, M("1", 28, SECANT).next_to(run, DOWN, buff=0.08), M("1", 28, SECANT).next_to(rise, RIGHT, buff=0.08))
            rec = [estimate(0, 1, [Create(rr)])]
            notes = [M(r"\approx 1", 32, DERIV).next_to(rec[0], RIGHT, buff=0.12)]
            self.play(FadeIn(notes[0]), FadeOut(rr), run_time=0.6)
            b.line(2)
            rec.append(estimate(PI / 2, 0))
            notes.append(M("0", 32, DERIV).next_to(rec[1], UP, buff=0.12))
            self.play(FadeIn(notes[1]), run_time=0.4)
            b.line(3)
            rec.append(estimate(PI, -1))
            notes.append(M(r"\approx -1", 32, DERIV).next_to(rec[2], RIGHT, buff=0.12))
            self.play(FadeIn(notes[2]), run_time=0.4)
            b.line(4)
            self.play(*[FadeOut(n) for n in notes], run_time=0.4)
            more = [closed_dot(bot, v, np.cos(v), DERIV).scale(0.8) for v in np.arange(-PI / 2, 2 * PI + 1e-6, PI / 12)
                    if min(abs(v), abs(v - PI / 2), abs(v - PI)) > 1e-6]
            self.play(LaggedStart(*[FadeIn(m, scale=2) for m in more], lag_ratio=0.12), run_time=3)
            b.line(5)
            cosc = bot.plot(np.cos, x_range=[-PI / 2, 2 * PI], color=DERIV, stroke_width=5)
            self.play(Create(cosc), run_time=2.4)
            b.line(6)
            self.play(FadeIn(M(r"\cos x", 40, DERIV).next_to(bot.c2p(2 * PI, 0), RIGHT, buff=0.25).shift(UP * 0.5)), run_time=0.8)
            self.play(Indicate(cosc, color=DERIV), run_time=1)
        self.clear()
        self.title()

        # ---------------------------------------------------------------- the unit-circle picture
        R, O = 2.7, LEFT * 3.4 + DOWN * 0.6
        th, dth = 0.75, ValueTracker(0.35)
        pt = lambda a: O + R * np.array([np.cos(a), np.sin(a), 0])
        with self.beat("A nudge around the circle") as b:
            circ = Circle(radius=R, color=DIM, stroke_width=3).move_to(O)
            axes = VGroup(Line(O + LEFT * (R + 0.3), O + RIGHT * (R + 0.3), color=DIM, stroke_width=2), Line(O + DOWN * (R + 0.3), O + UP * (R + 0.3), color=DIM, stroke_width=2))
            P = pt(th)
            foot = O + RIGHT * R * np.cos(th)
            big = VGroup(Line(O, P, color=INK, stroke_width=4), Line(foot, P, color=SECANT, stroke_width=5), Line(O, foot, color=FUNC, stroke_width=5))
            self.play(FadeIn(axes), Create(circ), run_time=1)
            self.play(Create(big), FadeIn(Dot(P, color=INK)), FadeIn(M(r"\theta", 34).move_to(O + 0.55 * np.array([np.cos(th / 2), np.sin(th / 2), 0]))),
                      FadeIn(M(r"\sin\theta", 32, SECANT).next_to(big[1], RIGHT, buff=0.1)), FadeIn(M(r"\cos\theta", 32, FUNC).next_to(big[2], DOWN, buff=0.1)), run_time=1.2)
            b.line(1)
            arc = always_redraw(lambda: Arc(radius=R, start_angle=th, angle=dth.get_value(), arc_center=O, color=TANGENT, stroke_width=7))
            Q = always_redraw(lambda: Dot(pt(th + dth.get_value()), color=TANGENT))
            self.play(Create(arc), FadeIn(Q), FadeIn(M(r"d\theta", 32, TANGENT).next_to(pt(th + 0.17), UR, buff=0.1)), run_time=1)
            b.line(2)
            Qp = pt(th + dth.get_value())
            C = np.array([Qp[0], P[1], 0])
            tiny = VGroup(Line(P, C, color=FUNC, stroke_width=4), Line(C, Qp, color=SECANT, stroke_width=4), Line(P, Qp, color=TANGENT, stroke_width=4))
            self.play(Create(tiny), run_time=1)
            b.line(3)
            self.play(Indicate(big[0], color=INK), Indicate(tiny[2], color=TANGENT), run_time=1.2)
            mag = tiny.copy()
            self.play(mag.animate.scale(4.5).move_to(RIGHT * 3.6 + UP * 0.8), run_time=1.2)
            self.play(Rotate(mag, -PI / 2), run_time=1.2)
            legs = VGroup(M(r"d(\sin\theta)", 32, SECANT).next_to(mag[1], DOWN, buff=0.12), M(r"d\theta", 32, TANGENT).next_to(mag[2].get_center(), UL, buff=0.1))
            self.play(FadeIn(legs), run_time=0.8)
            b.line(4)
            self.play(Indicate(big[2], color=FUNC), Indicate(mag[1], color=SECANT), run_time=1.2)
            b.line(5)
            ratio = M(r"\frac{d(\sin\theta)}{d\theta} \approx \frac{\cos\theta}{1}", 46).to_edge(RIGHT, buff=0.6).shift(DOWN * 2.2)
            self.play(Write(ratio), run_time=1.2)
        with self.beat("From the picture to the limit") as b:
            self.play(Indicate(ratio, color=TANGENT), run_time=1)
            b.line(1)
            self.play(FadeOut(tiny), run_time=0.3)
            self.play(dth.animate.set_value(0.04), run_time=2.5)
            b.line(2)
            lim = M(r"d\theta \to 0:\quad \frac{d(\sin\theta)}{d\theta} = \cos\theta", 46, DERIV).move_to(ratio)
            self.play(ReplacementTransform(ratio, lim), run_time=1.2)
            b.line(3)
            self.play(Indicate(mag[0], color=FUNC), run_time=1)
        self.clear()

        with self.beat("Why sine's derivative is cosine") as b:
            board = Board()
            board.anchor = UP * 3.3
            board.write(self, r"\lim_{h\to0}\frac{\sin(x + h) - \sin x}{h} = \lim_{h\to0}\frac{\sin x\cos h + \cos x\sin h - \sin x}{h}", size=44)
            board.write(self, r"= \lim_{h\to0}\left[\sin x\cdot\frac{\cos h - 1}{h} + \cos x\cdot\frac{\sin h}{h}\right]", size=44)
            b.line(1)
            board.write(self, r"\lim_{h\to0}\frac{\sin h}{h} = 1, \qquad \lim_{h\to0}\frac{\cos h - 1}{h} = 0", color=SECANT, size=44)
            b.line(2)
            board.write(self, r"\frac{d}{dx}\sin x = \sin x\cdot 0 + \cos x\cdot 1 = \cos x", color=DERIV, size=44)
        self.clear()

        with self.beat("Cosine") as b:
            top, bot, g = self.slide(np.cos, lambda t: -np.sin(t), ("y", r"\text{slope}"), DERIV, [(None, PI / 2), (None, PI), (None, 2 * PI - 0.001)])
            self.play(FadeIn(M(r"-\sin x", 40, DERIV).next_to(bot, RIGHT, buff=0.2).shift(UP * 0.6)), run_time=0.6)
            b.line(1)
            self.play(FadeIn(callout("radians", SECANT, 34).to_edge(UP, buff=0.3)), run_time=0.6)
            b.line(2)
            # the proofs are for understanding; the rules are what to keep (Adder)
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
            card = VGroup(T("The proofs won't be on the exam.", 40, DIM), T("Memorize the rules:", 44),
                          M(r"\frac{d}{dx}\sin x = \cos x \qquad \frac{d}{dx}\cos x = -\sin x", 52, DERIV)).arrange(DOWN, buff=0.45)
            self.play(FadeIn(card[0]), run_time=0.6)
            self.play(FadeIn(card[1]), Write(card[2]), run_time=1.2)
        self.clear()

        with self.beat("Its own derivative") as b:
            q = T("Can a function be its own derivative?", 48, SECANT).to_edge(UP, buff=0.6)
            self.play(FadeIn(q), run_time=0.8)
            b.line(1)
            need = M(r"\text{slope} = \text{height, everywhere}", 44).next_to(q, DOWN, buff=0.5)
            self.play(Write(need), run_time=1)
            b.line(2)
            qa, _ = plot_axes([-2, 2, 1], [0, 6, 1], w=5.4, h=3.8, coords=False)
            qa.next_to(need, DOWN, buff=0.4)
            curve = qa.plot(np.exp, x_range=[-2, np.log(6)], color=FUNC, stroke_width=4)
            self.play(FadeIn(qa), Create(curve), run_time=1)
            for xv, lab in ((-1.2, "small: nearly flat"), (1.4, "big: steep")):
                self.play(Create(tangent_line(qa, np.exp, xv, np.exp(xv), [xv - 0.5, xv + 0.5])), FadeIn(T(lab, 28, TANGENT).next_to(qa.c2p(xv, np.exp(xv)), RIGHT if xv < 0 else LEFT, buff=0.3)), run_time=0.8)
            b.line(3)
            self.play(Indicate(curve, color=FUNC), run_time=0.8)
        self.clear()

        ax, al = plot_axes([-2, 2, 1], [0, 6, 1], w=6.4, h=5)
        VGroup(ax, al).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        with self.beat("A function that is its own slope") as b:
            info = VGroup()
            for base, col, name, lx in ((2, DIM, "2^x", 2.0), (3, SECANT, "3^x", 1.55), (np.e, FUNC, "e^x", 1.62)):
                top_x = min(lx, np.log(6) / np.log(base))
                self.play(Create(ax.plot(lambda x: base ** x, x_range=[-2, min(2, np.log(6) / np.log(base))], color=col, stroke_width=4)),
                          FadeIn(M(name, 32, col).next_to(ax.c2p(top_x, base ** top_x), LEFT if base > 2 else RIGHT, buff=0.15)), run_time=0.6)
            for base, col, s in ((2, DIM, "0.693"), (3, SECANT, "1.099")):
                self.play(Create(tangent_line(ax, lambda x: base ** x, 0, np.log(base), [-0.9, 0.9], color=col)), run_time=0.5)
                info.add(M(rf"{base}^x:\ \text{{slope at 0}} = {s}", 36, col))
            info.arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT, buff=0.5).shift(UP * 1.8)
            self.play(FadeIn(info), run_time=0.8)
            b.line(1)
            self.play(Create(tangent_line(ax, np.exp, 0, 1, [-0.9, 0.9], color=TANGENT)), run_time=0.6)
            e = M(r"e^x:\ \text{slope at 0} = 1, \quad e \approx 2.718", 36, FUNC).next_to(info, DOWN, buff=0.3, aligned_edge=LEFT)
            self.play(FadeIn(e), run_time=0.6)
            b.line(2)
            about = T(r"$e$: one particular number, irrational like $\pi$", 30, DIM).next_to(e, DOWN, buff=0.25, aligned_edge=LEFT)
            self.play(FadeIn(about), run_time=0.6)
            b.line(3)
            for xv in (-1, 0.5, 1.2):
                self.play(Create(tangent_line(ax, np.exp, xv, np.exp(xv), [xv - 0.4, xv + 0.4], color=TANGENT)), Flash(ax.c2p(xv, np.exp(xv)), color=TANGENT), run_time=0.6)
            sb = callout(r"slope $=$ height", TANGENT, 36).next_to(e, DOWN, buff=0.5)
            self.play(FadeIn(sb), run_time=0.6)
        self.clear()

        ax, al = plot_axes([-1, 5, 1], [-1, 5, 1], w=5.6, h=5.6)
        VGroup(ax, al).to_edge(LEFT, buff=1.2).shift(DOWN * 0.2)
        with self.beat("The natural log") as b:
            ex = ax.plot(np.exp, x_range=[-1, np.log(5)], color=FUNC, stroke_width=4)
            diag = DashedLine(ax.c2p(-1, -1), ax.c2p(5, 5), color=DIM)
            self.play(FadeIn(ax), FadeIn(al), Create(ex), Create(diag), run_time=1)
            ln = ax.plot(np.log, x_range=[np.exp(-1), 5], color=DERIV, stroke_width=4)
            self.play(TransformFromCopy(ex, ln), run_time=1.4)
            names = VGroup(M("y = e^x", 32, FUNC).next_to(ax.c2p(1.3, np.exp(1.3)), LEFT, buff=0.2),
                           M(r"y = \ln x", 32, DERIV).next_to(ax.c2p(4.6, np.log(4.6)), DOWN, buff=0.2),
                           M("y = x", 30, DIM).next_to(ax.c2p(4.4, 4.4), RIGHT, buff=0.1))
            self.play(FadeIn(names), run_time=0.6)
            b.line(1)
            self.play(Create(tangent_line(ax, np.exp, np.log(2), 2, [np.log(2) - 0.5, np.log(2) + 0.5], color=SECANT)),
                      Create(tangent_line(ax, np.log, 2, 0.5, [1, 3], color=SECANT)), run_time=1)
            b.line(2)
            self.play(Create(tangent_line(ax, np.log, 4, 0.25, [3, 5], color=TANGENT)), run_time=0.8)
            labs = VGroup(M(r"x = 2:\ \text{slope } \tfrac12", 38), M(r"x = 4:\ \text{slope } \tfrac14", 38), M(r"\frac{d}{dx}\ln x = \frac1x", 46, DERIV)).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
            labs.to_edge(RIGHT, buff=0.8)
            self.play(FadeIn(labs), run_time=1)
        self.clear()

        with self.beat("The four rules") as b:
            rows = VGroup(M(r"\frac{d}{dx}\sin x = \cos x", 48), M(r"\frac{d}{dx}\cos x = -\sin x", 48), M(r"\frac{d}{dx}e^x = e^x", 48), M(r"\frac{d}{dx}\ln x = \frac1x", 48))
            rows.arrange_in_grid(2, 2, buff=(1.0, 0.6))
            self.play(FadeIn(formula_box(rows, DERIV)), run_time=1.2)
        self.clear()

        fa, fl = plot_axes([0, 2 * PI, PI / 2], [0, 60, 20], w=5.4, h=3.6, coords=False, xlabel="t", ylabel="H")
        H = lambda t: 30 - 25 * np.cos(t)
        fticks = VGroup(*[M(lab, 24, DIM).next_to(fa.c2p(v, 0), DOWN, buff=0.1) for v, lab in ((PI / 2, r"\tfrac{\pi}{2}"), (PI, r"\pi"), (3 * PI / 2, r"\tfrac{3\pi}{2}"), (2 * PI, r"2\pi"))],
                        *[M(str(v), 24, DIM).next_to(fa.c2p(0, v), LEFT, buff=0.1) for v in (20, 40, 60)])
        ferris = VGroup(fa, fl, fticks, fa.plot(H, x_range=[0, 2 * PI], color=FUNC, stroke_width=4),
                        fa.plot(lambda t: 30 + 25 * (t - PI / 2), x_range=[PI / 2 - 0.45, PI / 2 + 0.45], color=TANGENT, stroke_width=4), closed_dot(fa, PI / 2, 30, INK))
        self.example("In context", r"A Ferris wheel seat is $H(t) = 30 - 25\cos t$ feet high after $t$ minutes. Find $H'\!\left(\dfrac\pi2\right)$ and interpret it.",
                     [r"H'(t) = 0 - 25(-\sin t) = 25\sin t", r"H'\!\left(\tfrac\pi2\right) = 25\sin\tfrac\pi2 = 25",
                      r"TEXT:At $t = \frac\pi2$ minutes the seat is rising at $25$ feet per minute, the fastest it ever rises."], figure=ferris, at=[1, 2, 3])
        self.example("Combine with earlier rules", r"Find $f'(x)$ for $f(x) = 3\sin x - 4e^x + 2\ln x - \cos x$.",
                     [r"f'(x) = 3\cos x - 4e^x + 2\cdot\frac1x - (-\sin x)", r"f'(x) = 3\cos x - 4e^x + \frac{2}{x} + \sin x"], at=[1, 2])
        self.example("A tangent line", r"Find the equation for the line tangent to $y = e^x$ at $x = 0$.",
                     [r"\text{point: } e^0 = 1,\ \text{so}\ (0, 1)", r"\text{slope: } y' = e^x,\ \ e^0 = 1", r"y - 1 = 1(x - 0),\ \text{ or } y = x + 1"], at=[1, 2, 3])

        with self.beat("Close") as b:
            top, bot, g = trig_axes(("y", r"y'"))
            g.scale(0.7).to_edge(LEFT, buff=0.5)
            self.play(FadeIn(g), Create(top.plot(np.sin, x_range=[0, 2 * PI], color=FUNC)), Create(bot.plot(np.cos, x_range=[0, 2 * PI], color=DERIV)), run_time=1.2)
            a3, _ = plot_axes([-2, 2, 1], [0, 6, 1], w=3.6, h=3.6, coords=False)
            grp = VGroup(a3, a3.plot(np.exp, x_range=[-2, np.log(6)], color=FUNC), T(r"slope $=$ height", 30, TANGENT).next_to(a3, DOWN)).to_edge(RIGHT, buff=0.8)
            self.play(FadeIn(grp), run_time=0.8)
        self.clear()

        self.examples_card()
        self.example("Example 1: Mixing the new rules with the old", r"Find $f'(x)$ for $f(x) = 4\sin x - 3e^x + 5\ln x - x^2$.",
                     [r"4\sin x \to 4\cos x, \qquad -3e^x \to -3e^x", r"5\ln x \to \frac5x, \qquad -x^2 \to -2x", r"f'(x) = 4\cos x - 3e^x + \frac5x - 2x"], at=[2, 3, 4])
        a2, _ = plot_axes([0, PI, 1], [0, 2.5, 1], w=5.4, h=3.8)
        fig2 = VGroup(a2, a2.plot(lambda x: 2 * np.sin(x), x_range=[0, PI], color=FUNC, stroke_width=4),
                      a2.plot(lambda x: np.sqrt(3) + (x - PI / 3), x_range=[0.2, 1.7], color=TANGENT, stroke_width=4), closed_dot(a2, PI / 3, np.sqrt(3), INK))
        self.example("Example 2: A tangent line to a sine curve", r"Find the equation for the line tangent to $y = 2\sin x$ at $x = \dfrac{\pi}{3}$.",
                     [r"2\sin\frac{\pi}{3} = 2\cdot\frac{\sqrt3}{2} = \sqrt3", r"y' = 2\cos x, \quad 2\cos\frac{\pi}{3} = 1", r"y - \sqrt3 = x - \frac{\pi}{3}"], figure=fig2, at=[1, 2, 3])
        a3, _ = plot_axes([-1, 2, 1], [0, 3, 1], w=5.4, h=3.8)
        fig3 = VGroup(a3, a3.plot(lambda x: np.exp(x) - 2 * x, x_range=[-0.4, 1.6], color=FUNC, stroke_width=4),
                      Line(a3.c2p(np.log(2) - 0.5, 2 - 2 * np.log(2)), a3.c2p(np.log(2) + 0.5, 2 - 2 * np.log(2)), color=TANGENT, stroke_width=4),
                      closed_dot(a3, np.log(2), 2 - 2 * np.log(2), INK))
        self.example("Example 3: Where is the slope a given value?", r"Where does $y = e^x - 2x$ have a horizontal tangent line?",
                     [r"y' = e^x - 2 = 0,\ \text{so}\ e^x = 2", r"x = \ln 2", r"\approx 0.693"], figure=fig3, at=[1, 2, 3])
        self.finish()
