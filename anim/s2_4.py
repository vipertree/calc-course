"""Topic 2.4: Connecting differentiability and continuity. Narration comes from transcripts/2_4.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def zoom_view(fn, cx, cy, R, w=7.6, h=5, mag=None, smooth=True):
    """The graph of fn in the window [cx - R, cx + R] x [cy - R*h/w, cy + R*h/w], drawn at the same size whatever R is."""
    ry = R * h / w
    ax = Axes(x_range=[cx - R, cx + R, R], y_range=[cy - ry, cy + ry, ry], x_length=w, y_length=h, tips=False,
              axis_config={"color": DIM, "stroke_width": 2, "include_ticks": False}).set_opacity(0.0)
    frame = Rectangle(width=w, height=h, color=DIM, stroke_width=2)
    xs = np.linspace(cx - R, cx + R, 401)
    pts = [ax.c2p(x, fn(x)) for x in xs if abs(fn(x) - cy) <= ry]
    curve = VMobject(color=FUNC, stroke_width=5)
    if smooth:
        curve.set_points_smoothly(pts)
    else:
        curve.set_points_as_corners(pts)
    label = M(rf"\times {mag}" if mag else r"\times 1", 36, DIM).next_to(frame, UP, buff=0.15).align_to(frame, RIGHT)
    return VGroup(frame, curve, Dot(ax.c2p(cx, cy), color=INK, radius=0.07), label)


def tick_view(fn, R, w=7.6, h=5, labels=False, cx=0.0, cy=0.0, smooth=True, step=None):
    """A window [cx - R, cx + R] x [cy - ry, cy + ry] with axes through the origin (when in view), tick marks every `step`
    (default R/4), and, if labels=True, the tick values. The same picture at any R, so a zoom is a sequence of these."""
    ry = R * h / w
    step = step or R / 4
    frame = Rectangle(width=w, height=h, color=DIM, stroke_width=2)
    to = lambda x, y: frame.get_center() + RIGHT * (x - cx) / R * w / 2 + UP * (y - cy) / ry * h / 2
    g = VGroup(frame)
    if abs(cy) <= ry:
        g.add(Line(to(cx - R, 0), to(cx + R, 0), color=DIM, stroke_width=2))
    if abs(cx) <= R:
        g.add(Line(to(0, cy - ry), to(0, cy + ry), color=DIM, stroke_width=2))
    fmt = lambda v: f"{v:.10f}".rstrip("0").rstrip(".") if abs(v) > 1e-12 else "0"
    k0, k1 = int(np.ceil((cx - R) / step)), int(np.floor((cx + R) / step))
    for k in range(k0, k1 + 1):
        x = k * step
        if k == 0 or abs(cy) > ry:
            continue
        g.add(Line(to(x, 0) + DOWN * 0.08, to(x, 0) + UP * 0.08, color=DIM, stroke_width=2))
        if labels and k % 2 == 0:
            g.add(M(fmt(x), 22, DIM).next_to(to(x, 0), DOWN, buff=0.12))
    k0, k1 = int(np.ceil((cy - ry) / step)), int(np.floor((cy + ry) / step))
    for k in range(k0, k1 + 1):
        y = k * step
        if k == 0 or abs(cx) > R:
            continue
        g.add(Line(to(0, y) + LEFT * 0.08, to(0, y) + RIGHT * 0.08, color=DIM, stroke_width=2))
        if labels:
            g.add(M(fmt(y), 22, DIM).next_to(to(0, y), LEFT, buff=0.12))
    xs = np.linspace(cx - R, cx + R, 600)
    pts = [to(x, fn(x)) for x in xs if abs(fn(x) - cy) <= ry]
    curve = VMobject(color=FUNC, stroke_width=5)
    curve.set_points_smoothly(pts) if smooth else curve.set_points_as_corners(pts)
    g.add(curve)
    return g


class Lesson(TranscriptScene):
    NUM = "2.4"

    def construct(self):
        sq = lambda x: x * x
        wave = lambda x: np.sin(2 * x) + 0.001
        v = tick_view(wave, 0.004, step=0.001).shift(DOWN * 0.3)
        with self.beat("Guess the function") as b:
            self.play(FadeIn(v), run_time=1.2)
            b.line(1)
            g1 = M(r"y = 2x + 1\,?", 48, SECANT).next_to(v, UP, buff=0.25)
            self.play(Write(g1), run_time=1)
        with self.beat("Reveal the scale") as b:
            v2 = tick_view(wave, 0.004, step=0.001, labels=True).shift(DOWN * 0.3)
            self.play(Transform(v, v2), run_time=1.2)
            b.line(1)
            g2 = M(r"y = 2x + 0.001\,?", 48, SECANT).move_to(g1)
            self.play(ReplacementTransform(g1, g2), run_time=1)
        with self.beat("Zoom out") as b:
            for R in (0.02, 0.1, 0.4, 1.2, 3.2):
                self.play(Transform(v, tick_view(wave, R, labels=True).shift(DOWN * 0.3)), run_time=1.4)
            b.line(1)
            fn = M(r"y = \sin(2x) + 0.001", 48, FUNC).move_to(g2)
            self.play(ReplacementTransform(g2, fn), run_time=1)
            b.line(2)
            self.play(Indicate(fn, color=FUNC), run_time=0.8)
        self.clear()
        self.title()

        v = tick_view(wave, 0.01, labels=True).shift(DOWN * 0.6)
        with self.beat("Local linearity") as b:
            self.play(FadeIn(v), run_time=0.8)
            ll = T("locally linear at $x = 0$", 44, SECANT).next_to(v, UP, buff=0.3)
            self.play(FadeIn(ll), run_time=0.8)
            b.line(1)
            dd = T("differentiable at $x = 0$", 40, DERIV).next_to(v, DOWN, buff=0.3)
            self.play(FadeIn(dd), run_time=0.8)
        self.clear()

        v = tick_view(abs, 2, labels=True, smooth=False, cy=1).shift(DOWN * 0.3)
        with self.beat("A corner doesn't straighten") as b:
            self.play(FadeIn(v), run_time=1)
            for R in (0.2, 0.02, 0.002):
                self.play(Transform(v, tick_view(abs, R, labels=True, smooth=False, cy=R / 2).shift(DOWN * 0.3)), run_time=1.6)
            b.line(1)
            labs = VGroup(M(r"\text{slope } {-1}", 36, SECANT).move_to(v[0].get_center() + LEFT * 2.2 + UP * 1.4),
                          M(r"\text{slope } 1", 36, TANGENT).move_to(v[0].get_center() + RIGHT * 2.2 + UP * 1.4))
            self.play(FadeIn(labs), run_time=0.8)
            b.line(2)
            lim = M(r"\lim_{h\to0}\frac{|0 + h| - |0|}{h} = \lim_{h\to0}\frac{|h|}{h}:\ \ -1 \text{ from the left},\ 1 \text{ from the right}", 34).next_to(v, DOWN, buff=0.25)
            self.play(Write(lim), run_time=1.4)
        self.clear()

        with self.beat("Other ways to fail") as b:
            cusp = lambda x: np.cbrt(x * x)
            vert = np.cbrt
            panels = VGroup()
            for fn, name in ((cusp, "cusp"), (vert, "vertical tangent")):
                a, _ = plot_axes([-2, 2, 1], [-2, 2, 1], w=3.6, h=3.2, coords=False)
                panels.add(VGroup(a, a.plot(fn, x_range=[-2, 2, 0.002], color=FUNC, stroke_width=4), T(name, 30, DIM).next_to(a, DOWN)))
            a, _ = plot_axes([-2, 2, 1], [-2, 2, 1], w=3.6, h=3.2, coords=False)
            panels.add(VGroup(a, a.plot(lambda x: 0.4 * x - 0.8, x_range=[-2, 0], color=FUNC, stroke_width=4), a.plot(lambda x: 0.4 * x + 0.8, x_range=[0, 2], color=FUNC, stroke_width=4),
                              open_dot(a, 0, -0.8), closed_dot(a, 0, 0.8, FUNC), T("jump", 30, DIM).next_to(a, DOWN)))
            panels.arrange(RIGHT, buff=0.6)
            for i, p in enumerate(panels):
                b.line(i)
                self.play(FadeIn(p), run_time=0.8)
            vt = DashedLine(panels[1][0].c2p(0, -2), panels[1][0].c2p(0, 2), color=TANGENT)
            self.play(Create(vt), run_time=0.6)
        self.clear()

        with self.beat("The one-way street") as b:
            d = callout("differentiable at $c$", DERIV, 40).shift(LEFT * 3.4 + UP * 1)
            c = callout("continuous at $c$", FUNC, 40).shift(RIGHT * 3.4 + UP * 1)
            fwd = Arrow(d.get_right(), c.get_left(), color=INK, buff=0.15, stroke_width=6)
            self.play(FadeIn(d), run_time=0.6)
            self.play(GrowArrow(fwd), FadeIn(c), run_time=1)
            b.line(1)
            back = CurvedArrow(c.get_bottom() + DOWN * 0.1, d.get_bottom() + DOWN * 0.1, color=DIM, angle=-TAU / 6)
            a, _ = plot_axes([-2, 2, 1], [0, 2, 1], w=3.2, h=1.8, coords=False)
            vg = VGroup(a, a.plot(abs, x_range=[-2, 2], color=FUNC, stroke_width=4, use_smoothing=False), M("|x|", 32).next_to(a, RIGHT)).shift(DOWN * 2.3)
            self.play(Create(back), FadeIn(vg), run_time=1)
            b.line(2)
            x = Cross(back, stroke_color=TANGENT, scale_factor=0.25)
            self.play(Create(x), run_time=0.6)
        self.clear()

        a0, _ = plot_axes([-0.5, 2.5, 1], [-1, 4, 1], w=5, h=4.4)
        fig0 = VGroup(a0, a0.plot(lambda x: x * x, x_range=[-0.5, 1], color=FUNC, stroke_width=4), a0.plot(lambda x: 2 * x - 1, x_range=[1, 2.5], color=SECANT, stroke_width=4),
                      closed_dot(a0, 1, 1, INK))
        self.example("Check value and slope", r"Is $f$ differentiable at $x = 1$? \[ f(x) = \begin{cases} x^2, & x \le 1 \\ 2x - 1, & x > 1 \end{cases} \]",
                     [r"\text{values: } 1^2 = 1, \quad \lim_{x\to1^+}(2x - 1) = 1 \ \checkmark", r"\text{slopes: } 2x\big|_{x=1} = 2, \quad \text{line slope } 2 \ \checkmark",
                      r"\text{differentiable at } x = 1,\ \ f'(1) = 2"], figure=fig0, at=[1, 2, 3])

        with self.beat("Close") as b:
            l = tick_view(wave, 0.01, w=5.2, h=3.6, labels=True)
            r = tick_view(abs, 0.002, w=5.2, h=3.6, labels=True, smooth=False, cy=0.001)
            VGroup(l, r).arrange(RIGHT, buff=0.8)
            self.play(FadeIn(l), FadeIn(r), run_time=1.2)
        self.clear()

        self.examples_card()
        a1, _ = plot_axes([0, 3, 1], [0, 9, 3], w=5, h=4.4)
        fig1 = VGroup(a1, a1.plot(lambda x: x * x, x_range=[0, 2], color=FUNC, stroke_width=4), a1.plot(lambda x: 4 * x - 4, x_range=[2, 3], color=SECANT, stroke_width=4),
                      closed_dot(a1, 2, 4, INK))
        self.example("Example 1: A smooth seam", r"Is $f$ differentiable at $x = 2$? \[ f(x) = \begin{cases} x^2, & x < 2 \\ 4x - 4, & x \ge 2 \end{cases} \]",
                     [r"\lim_{x\to2^-}x^2 = 4, \quad 4(2) - 4 = 4 \ \checkmark", r"2x\big|_{x=2} = 4, \quad \text{slope } 4 \ \checkmark", r"\text{differentiable, } f'(2) = 4"],
                     figure=fig1, at=[1, 2, 3])
        a2, _ = plot_axes([0, 2, 1], [0, 5, 1], w=5, h=4.4)
        fig2 = VGroup(a2, a2.plot(lambda x: x * x + 1, x_range=[0, 1], color=FUNC, stroke_width=4), a2.plot(lambda x: 3 * x - 1, x_range=[1, 2], color=SECANT, stroke_width=4),
                      closed_dot(a2, 1, 2, INK))
        self.example("Example 2: A corner at the seam", r"Is $g$ differentiable at $x = 1$? \[ g(x) = \begin{cases} x^2 + 1, & x \le 1 \\ 3x - 1, & x > 1 \end{cases} \]",
                     [r"1^2 + 1 = 2, \quad \lim_{x\to1^+}(3x - 1) = 2 \ \checkmark", r"\text{slopes: } 2 \text{ and } 3 \ \times",
                      r"\text{continuous, not differentiable}"], figure=fig2, at=[1, 2, 3])
        self.example("Example 3: Making it smooth", r"Find $a$ and $b$ so that $h$ is differentiable at $x = 1$. \[ h(x) = \begin{cases} ax^2, & x \le 1 \\ 4x + b, & x > 1 \end{cases} \]",
                     [r"\text{slopes match and values match}", r"2a(1) = 4 \ \Rightarrow\ a = 2", r"a(1)^2 = 4(1) + b \ \Rightarrow\ 2 = 4 + b \ \Rightarrow\ b = -2"],
                     at=[1, 2, 3])
        self.finish()
