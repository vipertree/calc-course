"""Real-world props for the lesson videos: painted sprites (assets/*.png, see assets/CREDITS.md) and a few drawn
objects whose state animates (a water tank whose level moves, a cone that fills).

Adder (2026-10-03): the graphs and geometric pictures are fine as line drawings, but anything that is supposed to be
a real thing should look like one. Sprites are flat illustrations with transparent backgrounds so they sit on both
the parchment and the navy paper; anything that moves or changes level is drawn in manim, in the course palette.
"""
import os
import tempfile

import numpy as np
from manim import *
from PIL import Image, ImageFilter

from style import BG, DIM, FUNC, INK, PANEL, TANGENT, THEME

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


def mix(a, b, t):
    """interpolate_color for the palette's hex strings."""
    return interpolate_color(ManimColor(a), ManimColor(b), t)


def _is_dark():
    c = color_to_rgb(BG)
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2] < 0.5


DARK = _is_dark()


def _rimmed(name, px=4, opacity=0.55):
    """A copy of assets/<name> with a soft light rim behind it, so a dark sprite (the black lamppost) reads on navy."""
    out = os.path.join(tempfile.gettempdir(), f"calcprop_{THEME}_{px}_{name}")
    src = os.path.join(ASSETS, name)
    if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(src):
        return out
    im = Image.open(src).convert("RGBA")
    pad = px * 3
    big = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    big.alpha_composite(im, (pad, pad))
    a = big.getchannel("A").filter(ImageFilter.MaxFilter(2 * px + 1)).filter(ImageFilter.GaussianBlur(px / 2))
    r, g, b = (int(255 * v) for v in color_to_rgb(INK))
    rim = Image.new("RGBA", big.size, (r, g, b, 0))
    rim.putalpha(a.point(lambda v: int(v * opacity)))
    rim.alpha_composite(big)
    rim.save(out)
    return out


def sprite(name, height=None, width=None, rim=False):
    """An ImageMobject from assets/<name>.png, sized by height or width. rim=True gives a dark sprite a light halo on the
    dark themes (no change on paper)."""
    fn = name if name.endswith(".png") else name + ".png"
    path = _rimmed(fn) if (rim and DARK) else os.path.join(ASSETS, fn)
    im = ImageMobject(path)
    if height:
        im.set_height(height)
    elif width:
        im.set_width(width)
    return im


def petri_dish(height=1.3):
    return sprite("petri_dish", height)


def cash_register(height=1.2):
    return sprite("cash_register", height)


def thermometer(height=1.5):
    return sprite("thermometer", height)


def coffee_mug(height=1.4):
    return sprite("coffee_mug", height)


def lamppost(height=4.0):
    return sprite("lamppost", height, rim=True)


def person_walking(height=1.4):
    """Ana, walking to the right."""
    return sprite("person_walking", height)


def car_sprite(width=1.4):
    """A side-view hatchback facing right (the same sprite as 2.1's car). Track its heading with face()."""
    c = sprite("car", width=width)
    c.facing = 1
    return c


def face(car, way):
    """Point a car_sprite right (way = 1) or left (way = -1), mirroring it in place when the heading changes."""
    if way and way != car.facing:
        car.stretch(-1, 0)
        car.facing = way
    return car


def ladder(foot, top, width=0.42):
    """The wooden ladder sprite spanning foot -> top: its length is the distance between them, its feet on `foot`."""
    foot, top = np.array(foot, dtype=float), np.array(top, dtype=float)
    d = top - foot
    L = np.linalg.norm(d)
    im = sprite("ladder", height=L)
    im.stretch_to_fit_width(width)
    im.rotate(np.arctan2(d[1], d[0]) - PI / 2)
    im.move_to((foot + top) / 2)
    return im


def brick_wall(height=6.0, width=0.7, brick_h=0.3):
    """A wall seen from the side, in courses of brick: drawn, so it takes the theme's colors."""
    wall = Rectangle(width=width, height=height, stroke_width=0, fill_color=TANGENT, fill_opacity=0.28)
    lines = VGroup()
    n = int(height / brick_h)
    x0, y0 = -width / 2, -height / 2
    for k in range(1, n + 1):
        y = y0 + k * brick_h
        if y < height / 2 - 1e-6:
            lines.add(Line([x0, y, 0], [x0 + width, y, 0]))
        xs = [0.15, 0.55] if k % 2 else [0.35]
        for fx in xs:
            yy = y0 + (k - 1) * brick_h
            lines.add(Line([x0 + fx * width, yy, 0], [x0 + fx * width, min(yy + brick_h, height / 2), 0]))
    lines.set_stroke(DIM, 1.5, opacity=0.8)
    face_ = Line([width / 2, -height / 2, 0], [width / 2, height / 2, 0], color=DIM, stroke_width=4)
    return VGroup(wall, lines, face_)


def ground(width=7.0, depth=0.35):
    """A strip of ground with grass tufts along the top, for people, posts and ladders to stand on."""
    line = Line(LEFT * width / 2, RIGHT * width / 2, color=DIM, stroke_width=4)
    hatch = VGroup(*[Line([x, 0, 0], [x - depth * 0.6, -depth, 0], color=DIM, stroke_width=1.5, stroke_opacity=0.6)
                     for x in np.arange(-width / 2 + 0.3, width / 2, 0.3)])
    return VGroup(hatch, line)


# ---------------------------------------------------------------- the water tank

class Tank(VGroup):
    """A glass water tank on a stand, drawn as a short cylinder seen a little from above, with a gauge on its side and a
    drain pipe and valve at the bottom right. The water level is live: tank.level is a ValueTracker (0 = empty, 1 =
    full) and the water, its rippling surface and the gauge follow it, wherever the tank is moved or scaled.

        tk = Tank(0.7).shift(LEFT * 3)
        tk.drain_on()                       # drops start falling from the pipe
        self.play(tk.level.animate.set_value(0.4), run_time=3)

    inlet=True adds a faucet over the top left; tank.pour_on() runs a stream from it down to the water."""

    def __init__(self, level=0.6, width=2.4, height=3.0, gauge=("0", "20", "40", "60", "80"), unit="L", drain=True,
                 inlet=False, color=FUNC):
        super().__init__()
        self.level = ValueTracker(level)
        self.wave = ValueTracker(0)
        self.color = color
        w, h = width, height
        e = 0.13 * w                                     # half-height of the rim ellipse
        self.e_ratio = e / w
        frame = Rectangle(width=w, height=h, stroke_opacity=0, fill_opacity=0)
        self.frame = frame
        # stand: a low round plinth the tank sits on
        plinth = self._cylinder(-h / 2 - 0.2, -h / 2 + 0.02, w * 1.14, e * 1.14).set_fill(DIM, 0.5).set_stroke(DIM, 2)
        plinth_top = Ellipse(width=w * 1.14, height=2 * e * 1.14).move_to(UP * (-h / 2 + 0.02)).set_fill(DIM, 0.3).set_stroke(DIM, 1.5)
        # glass: a faint tint, the back of the rim, the side walls and the front of the base
        tint = self._cylinder(-h / 2, h / 2, w, e).set_fill(PANEL, 0.35).set_stroke(width=0)
        back_rim = Arc(radius=1, start_angle=0, angle=PI).stretch(w / 2, 0).stretch(e, 1).shift(UP * h / 2)
        back_rim.set_stroke(DIM, 2, opacity=0.7)
        walls = VGroup(Line([-w / 2, -h / 2, 0], [-w / 2, h / 2, 0]), Line([w / 2, -h / 2, 0], [w / 2, h / 2, 0]))
        walls.set_stroke(INK, 3.5)
        base_front = Arc(radius=1, start_angle=PI, angle=PI).stretch(w / 2, 0).stretch(e, 1).shift(DOWN * h / 2)
        base_front.set_stroke(INK, 3.5)
        front_rim = Arc(radius=1, start_angle=PI, angle=PI).stretch(w / 2, 0).stretch(e, 1).shift(UP * h / 2)
        front_rim.set_stroke(INK, 3.5)
        # metal bands at the top and bottom
        bands = VGroup(front_rim.copy().set_stroke(DIM, 9, opacity=0.55), base_front.copy().set_stroke(DIM, 9, opacity=0.55))
        # highlights on the glass: two soft vertical streaks on the left
        shine = VGroup(Line([-0.36 * w, -0.4 * h, 0], [-0.36 * w, 0.4 * h, 0]).set_stroke(WHITE, 7, opacity=0.28),
                       Line([-0.27 * w, -0.3 * h, 0], [-0.27 * w, 0.33 * h, 0]).set_stroke(WHITE, 3, opacity=0.22))
        # gauge: ticks up the right side, labels just outside
        g = VGroup()
        n = len(gauge) - 1
        for k, lab in enumerate(gauge):
            y = -h / 2 + h * k / n
            major = Line([w / 2 - 0.22, y, 0], [w / 2, y, 0]).set_stroke(INK, 2.5)
            g.add(major)
            if k < n:
                g.add(Line([w / 2 - 0.12, y + h / (2 * n), 0], [w / 2, y + h / (2 * n), 0]).set_stroke(INK, 1.5, opacity=0.7))
            if lab:
                g.add(MathTex(lab, font_size=22, color=DIM).next_to([w / 2, y, 0], RIGHT, buff=0.12))
        if unit:
            g.add(MathTex(r"\text{" + unit + "}", font_size=22, color=DIM).next_to([w / 2, h / 2, 0], RIGHT, buff=0.12).shift(UP * 0.32))
        parts = [frame, plinth, plinth_top, tint, back_rim]
        self.add(*parts)
        # the water lives between the back rim and the front glass, redrawn from the frame each frame
        self.water = always_redraw(self._draw_water)
        self.add(self.water)
        self.add(shine, walls, base_front, bands, front_rim, g)
        self.mouth = None
        if drain:
            y = -h / 2 + 0.22
            pipe = VGroup(Line([w / 2, y, 0], [w / 2 + 0.55, y, 0]), Line([w / 2 + 0.55, y, 0], [w / 2 + 0.55, y - 0.38, 0]))
            pipe.set_stroke(DIM, 11)
            pipe_in = pipe.copy().set_stroke(PANEL, 5)
            wheel = VGroup(Circle(radius=0.13).set_stroke(TANGENT, 3.5), Line(LEFT * 0.13, RIGHT * 0.13).set_stroke(TANGENT, 2.5),
                           Line(DOWN * 0.13, UP * 0.13).set_stroke(TANGENT, 2.5)).move_to([w / 2 + 0.3, y + 0.2, 0])
            stem = Line([w / 2 + 0.3, y, 0], [w / 2 + 0.3, y + 0.08, 0]).set_stroke(DIM, 3)
            self.mouth = Dot([w / 2 + 0.55, y - 0.4, 0], radius=0.001).set_opacity(0)
            self.add(pipe, pipe_in, stem, wheel, self.mouth)
        self.faucet = None
        if inlet:
            x0 = -0.25 * w
            top = h / 2 + 0.75
            spout = VGroup(Line([-w / 2 - 0.7, top, 0], [x0, top, 0]), Line([x0, top, 0], [x0, top - 0.3, 0])).set_stroke(DIM, 11)
            spout_in = spout.copy().set_stroke(PANEL, 5)
            self.faucet = Dot([x0, top - 0.32, 0], radius=0.001).set_opacity(0)
            self.add(spout, spout_in, self.faucet)
        self._t = 0.0
        self.drops = VGroup()
        self.stream = VGroup()
        self.add(self.drops, self.stream)

    # geometry, from the (possibly moved and scaled) frame
    def _geom(self):
        f = self.frame
        w = f.width
        h = f.height
        c = f.get_center()
        return c, w, h, self.e_ratio * w

    @staticmethod
    def _cylinder(y0, y1, w, e, c=ORIGIN):
        """Side view of a cylinder section from height y0 (its lower rim's front edge bulging down) to y1."""
        front = Arc(radius=1, start_angle=PI, angle=PI).stretch(w / 2, 0).stretch(e, 1).shift(UP * y0)
        p = VMobject()
        pts = [*front.get_anchors()]
        p.set_points_as_corners([*pts, [w / 2, y1, 0], [-w / 2, y1, 0], pts[0]])
        return p.shift(c)

    def _draw_water(self):
        c, w, h, e = self._geom()
        lv = float(np.clip(self.level.get_value(), 0, 1))
        y0 = c[1] - h / 2
        y1 = y0 + max(lv, 0.002) * h
        xs = np.linspace(-1, 1, 41)
        # the body: down the front of the base ellipse, up the walls to the level
        base = [[c[0] + x * w / 2, y0 - e * np.sqrt(max(1 - x * x, 0)), 0] for x in xs]
        body = VMobject().set_points_as_corners([*base, [c[0] + w / 2, y1, 0], [c[0] - w / 2, y1, 0], base[0]])
        body.set_fill([self.color, mix(self.color, BG, 0.35)], 0.55).set_stroke(width=0)
        body.set_sheen_direction(UP)
        # the surface: an ellipse at the level whose front edge ripples with the wave tracker
        ph = self.wave.get_value()
        amp = 0.014 * w
        front = [[c[0] + x * w / 2, y1 - e * np.sqrt(max(1 - x * x, 0)) + amp * np.sin(6 * x + ph) * (1 - x * x), 0] for x in xs]
        back = [[c[0] + x * w / 2, y1 + e * np.sqrt(max(1 - x * x, 0)), 0] for x in xs[::-1]]
        surf = VMobject().set_points_smoothly([*front, *back, front[0]])
        surf.set_fill(mix(self.color, WHITE if DARK else BG, 0.3), 0.75).set_stroke(self.color, 2)
        return VGroup(body, surf)

    def surface_point(self):
        c, w, h, e = self._geom()
        return np.array([c[0] - 0.25 * w, c[1] - h / 2 + float(np.clip(self.level.get_value(), 0, 1)) * h, 0])

    def _drip(self, m, dt):
        """Drops fall from the drain mouth, and the surface keeps a gentle ripple."""
        self._t += dt
        self.wave.increment_value(dt * 2.4)
        fall = 1.1 * (self.frame.width / 2.4)
        drops = []
        if self.mouth is not None and self._draining:
            p = self.mouth.get_center()
            n = int(round(3 + 2 * self._outflow))
            for k in range(n):
                q = (self._t * (1.0 + 0.6 * self._outflow) + k / n) % 1
                drops.append(Ellipse(width=0.07, height=0.12).set_fill(self.color, 0.9 * (1 - q) + 0.1).set_stroke(width=0)
                             .move_to(p + DOWN * fall * q * q))
        self.drops.become(VGroup(*drops) if drops else VGroup())
        if self.faucet is not None and self._pouring:
            a, b = self.faucet.get_center(), self.surface_point()
            b = np.array([a[0], b[1], 0])
            self.stream.become(VGroup(Line(a, b).set_stroke(self.color, 2 + 7 * self._inflow, opacity=0.8),
                                      Line(a, b).set_stroke(WHITE, 1.5, opacity=0.35))) if a[1] > b[1] else self.stream.become(VGroup())
        else:
            self.stream.become(VGroup())

    _draining = False
    _pouring = False
    _inflow = 1.0
    _outflow = 1.0

    def _ensure(self):
        if not getattr(self, "_updating", False):
            self.drops.add_updater(lambda m, dt: self._drip(m, dt))
            self._updating = True

    def drain_on(self, strength=1.0):
        """Drops fall from the drain; strength (about 0.3 to 2) sets how many and how fast."""
        self._draining = True
        self._outflow = strength
        self._ensure()
        return self

    def pour_on(self, strength=1.0):
        """A stream runs from the faucet to the water; strength (about 0.3 to 1.5) sets its thickness."""
        self._pouring = True
        self._inflow = strength
        self._ensure()
        return self

    def still(self):
        self._draining = self._pouring = False
        return self


# ---------------------------------------------------------------- the cone

def water_cone(depth=0.6, H=4.2, R=1.4, tip=ORIGIN):
    """A glass cone, point down, holding water to `depth` (fraction of H): elliptical rim and water surface so it reads as
    a solid, not a triangle. Returns (group, h, r) with group = VGroup(water, shell) and shell[0], shell[1] the slant
    edges from the tip (shell[0].get_start() is the tip), shell[2] the rim."""
    tip = np.array(tip, dtype=float)
    e_r = 0.18                                          # ellipse half-height per unit radius
    h, r = H * depth, R * depth
    xs = np.linspace(-1, 1, 41)
    front = [tip + [x * r, h - e_r * r * np.sqrt(1 - x * x), 0] for x in xs]
    body = VMobject().set_points_as_corners([tip, *front, tip])
    body.set_fill([FUNC, mix(FUNC, BG, 0.35)], 0.55).set_stroke(width=0).set_sheen_direction(UP)
    surf = Ellipse(width=2 * r, height=2 * e_r * r).move_to(tip + UP * h)
    surf.set_fill(mix(FUNC, WHITE if DARK else BG, 0.3), 0.75).set_stroke(FUNC, 2)
    water = VGroup(body, surf)
    left = Line(tip, tip + [-R, H, 0]).set_stroke(INK, 3.5)
    right = Line(tip, tip + [R, H, 0]).set_stroke(INK, 3.5)
    rim = Ellipse(width=2 * R, height=2 * e_r * R).move_to(tip + UP * H).set_stroke(INK, 3.5)
    tint = VMobject().set_points_as_corners([tip, tip + [-R, H, 0], tip + [R, H, 0], tip]).set_fill(PANEL, 0.3).set_stroke(width=0)
    shine = Line(tip + [-0.55 * R * 0.6, H * 0.6, 0], tip + [-0.55 * R * 0.95, H * 0.95, 0]).set_stroke(WHITE, 5, opacity=0.25)
    shell = VGroup(left, right, rim, tint, shine)
    return VGroup(water, shell), h, r
