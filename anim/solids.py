"""3D-looking solids for the volume lessons (8.7-8.12), drawn in a fixed projection on the ordinary 2D lesson scene.

Why not ThreeDScene: the lessons are LessonScene (voiceover + a caption-safe MovingCameraScene) and the course rule is
calculator-style zooms only, no camera moves. So the camera never moves; the OBJECT is projected onto the screen with
an orthographic View, its faces are shaded by their normals and drawn far-to-near (painter's algorithm), and turning
it is just re-projecting with a new yaw every frame. Text stays ordinary crisp 2D MathTex placed at projected points.

World coordinates (x, y, z), z is up:
  * cross sections (8.7, 8.8): the base region lies on the floor z = 0 (x right, y back), sections stand up in z.
    pitch=90 looks straight down, so the floor is exactly the student's 2D graph; tilt to pitch ~25 for the angled view.
  * revolution (8.9-8.12): the graph stands upright in the plane y = 0 (graph x -> world x, graph y -> world z) and is
    swept around an axis line in that plane. yaw=0, pitch=0 is exactly the flat 2D graph; turn it to see the solid.

    graph_point(gx, gy) = (gx, 0, gy)  is what `revolve` and `upright_*` use.

Pieces
------
View(origin, scale, yaw, pitch)          the projection. P(x, y, z) -> screen point; depth(); toward() (unit vector
                                         to the viewer); shade(color, normal). turned(yaw=, pitch=) is a copy.
Face(pts, color, normal, edge, ...)      one flat polygon (or a 2-point line piece with line=True).
Body(faces, convex, closed)              faces drawn together. Convex bodies are back-face culled (exact). Others are
                                         culled if closed, then sorted face by face. Bodies are ordered among
                                         themselves by bounding-box separation (exact for slabs side by side), else
                                         by center depth. body.moved(R=, t=, about=) rotates/translates a copy.
merge(*bodies)                           one non-convex Body: all faces sorted together (a surface plus its axis).
render(view, items)                      -> VGroup. items: Mobjects (drawn as given, e.g. floor art first) and Bodies.

Stage(draw, view, box=, **params)    a live picture: draw(stage, view, **values) -> list of items, redrawn each
                                         frame when a param or the view changes. Params are ValueTrackers:
                                         stage.to("n", 16) / stage.spin(90) / stage.tilt(25) return animations.
                                         The stage can be moved and scaled like any mobject (an invisible pin inside it
                                         records where it is), so example()'s figure placement works.
                                         stage.label(key, tex, size, color) is a cached MathTex that keeps its size
                                         relative to the stage; stage.still() is a frozen copy.

Floor (cross sections), all lists of 2D mobjects:
floor_axes(st, v, xr, yr, ticks=)        x and y axes lying on the floor, ticks and labels.
floor_region(v, top, bot, a, b, var=)    the shaded base region; floor_curve(v, f, a, b, var=) a boundary curve.
floor_segment(v, top, bot, at, var=)     the segment across the base at one x (or y): the side s of the section.

Cross sections:
profile(kind, lo, hi, height=None)       (u, z) outline standing on [lo, hi]: "square", "rect" (height= number or
                                         function of s), "equilateral", "leg" (isosceles right, a leg on the base),
                                         "hyp" (hypotenuse on the base), "semicircle" (diameter on the base).
prism(prof, w0, w1, axis="x")            the profile extruded from w0 to w1 along x (or y): a convex slab Body.
slab(kind, top, bot, at, d, ...)         one cross-section slab of thickness d centered at `at`.
slabs(kind, top, bot, a, b, n, gap=)     n slabs filling [a, b] (midpoint heights), gap = fraction left between them.
section_solid(kind, top, bot, a, b)      the smooth solid (the limit of slabs): a swept mesh.
grow_slices(scene, make, ns, ...)        the "more and more slices" animation: crossfades make(n) for n in ns.

Revolution (graph coordinates; axis "x" = the horizontal line y = at, "y" = the vertical line x = at):
region_outline(top, bot, a, b)           CCW outline of the region between two graphs of x (outline_y for x = f(y)).
revolve(outline, axis, at, t0, t1)       the surface swept by the outline from angle t0 to t1, plus end caps (the
                                         region itself) when it is not a full turn. A full turn is closed and culled;
                                         a partial one is two-sided, so you can see inside it.
disc(R, x, d, ...) / washer(R, r, x, d)  one slice (a revolved rectangle): washers show the hole with its inner wall.
upright_axes(st, v, xr, yr)              the graph's axes standing in the plane y = 0 (sorted with the solid if you
                                         merge axis_line(...) pieces into it).
axis_line(axis, at, lo, hi)              the axis of revolution as sortable line pieces.

Props: bread_slices(...) a sliced sandwich loaf (crust, crumb faces with holes, end heels), cutting_board(...).

Tested by anim/_solids_test.py (renders a contact sheet of every builder).
"""
import functools

import numpy as np
from manim import (DEGREES, PI, TAU, Mobject, ValueTracker, VGroup, VMobject, Arrow, Line, DashedLine, Polygon,
                   ManimColor, interpolate_color, WHITE, BLACK, FadeIn, FadeOut, ORIGIN, RIGHT, UP, DOWN, LEFT)

from style import BG, INK, DIM, FUNC, AREA, ACCUM, SECANT, M

# ---------------------------------------------------------------------------------------------------------- view


def _rot_z(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])


def _rot_x(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[1.0, 0.0, 0.0], [0.0, c, -s], [0.0, s, c]])


def _rot_y(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]])


class View:
    """Orthographic view of world (x, y, z), z up. yaw (degrees) turns the object about the vertical axis; pitch
    (degrees) is how far above the floor the eye is (0: level, 90: straight down). origin is where world (0, 0, 0)
    lands on screen; scale is screen units per world unit.

    Default yaw -28, pitch 24: x runs right and a little down, y runs back and to the right, z straight up."""

    def __init__(self, origin=ORIGIN, scale=1.0, yaw=-28.0, pitch=24.0, light=(-0.45, 0.6, 0.66)):
        self.origin = np.array(origin, dtype=float)
        self.scale = float(scale)
        self.yaw, self.pitch = float(yaw), float(pitch)
        l = np.array(light, dtype=float)
        self.light = l / np.linalg.norm(l)                 # in screen terms: right, up, toward the viewer
        a, e = self.yaw * DEGREES, self.pitch * DEGREES
        R = _rot_z(a)
        ca, se = np.cos(e), np.sin(e)
        # rows: screen right, screen up, away from the viewer (depth), as linear maps of world points
        self._u = R[0]
        self._v = R[2] * ca + R[1] * se
        self._d = R[1] * ca - R[2] * se
        self._M = np.vstack([self._u, self._v]) * self.scale

    def turned(self, **kw):
        d = dict(origin=self.origin, scale=self.scale, yaw=self.yaw, pitch=self.pitch, light=self.light)
        d.update(kw)
        return View(**d)

    def P(self, x, y=None, z=None):
        """Screen point of world (x, y, z) (or of one array of shape (3,) or (n, 3))."""
        if y is None:
            p = np.asarray(x, dtype=float)
        else:
            p = np.array([x, y, z], dtype=float)
        if p.ndim == 1:
            uv = self._M @ p
            return self.origin + np.array([uv[0], uv[1], 0.0])
        uv = p @ self._M.T
        return self.origin + np.column_stack([uv, np.zeros(len(p))])

    def depth(self, p):
        """Larger is farther from the viewer."""
        return np.asarray(p, dtype=float) @ self._d

    def toward(self):
        """Unit world vector pointing at the viewer."""
        return -self._d

    def screen_normal(self, n):
        return np.array([n @ self._u, n @ self._v, -(n @ self._d)])

    def shade(self, color, n, ambient=0.38, flip=False):
        """The face color lit by a lamp over the viewer's left shoulder."""
        sn = self.screen_normal(np.asarray(n, dtype=float))
        if flip:
            sn = -sn
        k = ambient + (1 - ambient) * max(0.0, float(sn @ self.light))
        c = ManimColor(color)
        if k < 0.75:
            return interpolate_color(interpolate_color(c, BLACK, 0.5), c, k / 0.75)
        return interpolate_color(c, interpolate_color(c, WHITE, 0.35), (k - 0.75) / 0.25)


# ---------------------------------------------------------------------------------------------------------- faces


def _unit(v):
    L = np.linalg.norm(v)
    return v / L if L > 1e-12 else v


def _newell(pts):
    n = np.zeros(3)
    for i in range(len(pts)):
        p, q = pts[i], pts[(i + 1) % len(pts)]
        n += np.array([(p[1] - q[1]) * (p[2] + q[2]), (p[2] - q[2]) * (p[0] + q[0]), (p[0] - q[0]) * (p[1] + q[1])])
    L = np.linalg.norm(n)
    return n / L if L > 1e-12 else n


class Face:
    """A flat polygon in world coordinates. normal: outward unit normal (from Newell's method if None). edge: draw its
    outline (a crisp slab edge) in a darker shade, or a color; False hides seams between mesh faces. line=True makes a
    2-point line piece (width = stroke width). decor: extra small polygons (world points) drawn on this face when it
    shows, in decor_color (the crumb holes in a slice of bread)."""
    __slots__ = ("pts", "color", "normal", "edge", "opacity", "line", "width", "decor", "decor_color", "shade", "edge_width")

    def __init__(self, pts, color, normal=None, edge=True, opacity=1.0, line=False, width=3.0, decor=None, decor_color=None,
                 shade=True, edge_width=1.6):
        self.pts = np.asarray(pts, dtype=float)
        self.color = color
        self.normal = _newell(self.pts) if normal is None and not line else (np.asarray(normal, dtype=float) if normal is not None else None)
        self.edge, self.opacity, self.line, self.width = edge, opacity, line, width
        self.decor, self.decor_color, self.shade, self.edge_width = decor, decor_color, shade, edge_width


class Body:
    """Faces drawn as one object. convex: back-face cull, no sorting needed (exact). closed: cull, then sort faces by
    depth (a closed non-convex surface). Neither: two-sided (an open surface you can see inside), sorted by depth."""

    def __init__(self, faces, convex=False, closed=False, name=None):
        self.faces = [f for f in faces if f is not None]
        self.convex, self.closed, self.name = convex, closed, name
        pts = np.vstack([f.pts for f in self.faces]) if self.faces else np.zeros((1, 3))
        self.lo, self.hi = pts.min(axis=0), pts.max(axis=0)
        self.center = (self.lo + self.hi) / 2

    def moved(self, R=None, t=(0, 0, 0), about=None):
        """A copy rotated by the 3x3 matrix R about the point `about` (default: its center), then shifted by t."""
        R = np.eye(3) if R is None else np.asarray(R, dtype=float)
        c = self.center if about is None else np.asarray(about, dtype=float)
        t = np.asarray(t, dtype=float)
        out = []
        for f in self.faces:
            g = Face((f.pts - c) @ R.T + c + t, f.color, None if f.normal is None else _unit(R @ f.normal), f.edge, f.opacity, f.line, f.width,
                     None if f.decor is None else [(d - c) @ R.T + c + t for d in f.decor], f.decor_color, f.shade, f.edge_width)
            out.append(g)
        return Body(out, self.convex, self.closed, self.name)

    def recolor(self, color, opacity=None):
        for f in self.faces:
            f.color = color
            if opacity is not None:
                f.opacity = opacity
        return self


def merge(*bodies, closed=False):
    """One body whose faces are all sorted together (e.g. a solid and the axis line running through it)."""
    faces = [f for b in bodies for f in b.faces]
    return Body(faces, convex=False, closed=closed)


def rot(axis, degrees):
    """3x3 rotation matrix about a world axis "x", "y" or "z"."""
    return {"x": _rot_x, "y": _rot_y, "z": _rot_z}[axis](degrees * DEGREES)


# ---------------------------------------------------------------------------------------------------------- drawing


def _poly(pts2, fill, opacity, stroke, sw):
    m = VMobject()
    m.set_points_as_corners(list(pts2) + [pts2[0]])
    m.set_fill(fill, opacity)
    m.set_stroke(stroke, sw, opacity=1.0 if opacity > 0.99 else opacity)
    return m


def _face_mobs(view, f, flip, sw_scale):
    if f.line:
        p = view.P(f.pts)
        return [Line(p[0], p[1], color=f.color, stroke_width=f.width * sw_scale)]
    col = view.shade(f.color, f.normal, flip=flip) if f.shade else ManimColor(f.color)
    if flip:
        col = interpolate_color(col, BLACK, 0.12)             # insides read a touch darker
    p2 = view.P(f.pts)
    if f.edge is True:
        stroke, sw = interpolate_color(ManimColor(f.color), BLACK, 0.45), f.edge_width
    elif f.edge:
        stroke, sw = ManimColor(f.edge), f.edge_width
    else:
        stroke, sw = col, 1.0                                   # same color: hides the seams between mesh faces
    out = [_poly(p2, col, f.opacity, stroke, sw * sw_scale)]
    if f.decor:
        dc = ManimColor(f.decor_color or interpolate_color(ManimColor(f.color), BLACK, 0.25))
        for d in f.decor:
            out.append(_poly(view.P(d), dc, f.opacity, dc, 0.5))
    return out


def _visible(view, f, cull):
    if f.line or f.normal is None:
        return True, False
    facing = float(f.normal @ view.toward())
    if cull:
        return facing > 1e-6, False
    return True, facing < 0


def _body_cmp(view):
    w = view.toward()

    def cmp(A, B):
        # a plane between their boxes along x, y or z decides exactly; the one on the far side goes first
        for k in range(3):
            if A.hi[k] <= B.lo[k] + 1e-9:                 # A below B along axis k
                return -1 if w[k] > 1e-9 else (1 if w[k] < -1e-9 else 0)
            if B.hi[k] <= A.lo[k] + 1e-9:
                return 1 if w[k] > 1e-9 else (-1 if w[k] < -1e-9 else 0)
        da, db = view.depth(A.center), view.depth(B.center)
        return -1 if da > db else (1 if da < db else 0)
    return cmp


def render(view, items, sw_scale=1.0):
    """Draw a list of items: Mobjects as they are (in order), runs of Bodies sorted far to near."""
    out = VGroup()

    def flush(run):
        if not run:
            return
        run = sorted(run, key=functools.cmp_to_key(_body_cmp(view)))
        for b in run:
            if b.convex:
                for f in b.faces:
                    vis, flip = _visible(view, f, True)
                    if vis:
                        out.add(*_face_mobs(view, f, flip, sw_scale))
            else:
                faces = []
                for f in b.faces:
                    vis, flip = _visible(view, f, b.closed)
                    if vis:
                        faces.append((float(view.depth(f.pts.mean(axis=0))), f, flip))
                faces.sort(key=lambda t: -t[0])
                for _, f, flip in faces:
                    out.add(*_face_mobs(view, f, flip, sw_scale))
        run.clear()

    run = []
    for it in items:
        if isinstance(it, Body):
            run.append(it)
        elif isinstance(it, (list, tuple)):
            for x in it:
                (run.append(x) if isinstance(x, Body) else (flush(run), out.add(x)))
        elif it is not None:
            flush(run)
            out.add(it)
    flush(run)
    return out


class Stage(VGroup):
    """A live 3D picture. draw(stage, view, **values) returns the items to render (see render()). Every keyword
    parameter becomes a ValueTracker; yaw and pitch always exist. The picture is rebuilt on a frame when a value, or
    the stage's place on screen, has changed.

        st = Stage(draw, View(origin=..., scale=1.2, pitch=90), t=0)
        self.add(st)
        self.play(st.tilt(25), run_time=2)       # from the flat 2D graph to the angled view
        self.play(st.to("t", 1), run_time=3)     # whatever t means to draw()
        self.play(st.spin(60), run_time=3)       # turn the object

    Don't animate a Stage with .animate (its children are rebuilt); move it with shift/scale/next_to, or FadeIn/Out."""

    def __init__(self, draw, view=None, sw_scale=1.0, box=None, **params):
        """box: (x0, y0, x1, y1) screen rectangle (where the stage is created) that the stage always occupies, drawn
        invisibly: the room the picture needs in every pose, so a layout made around it holds while it tilts."""
        super().__init__()
        self._box0 = box
        self.draw_fn = draw
        self.view0 = view or View()
        self.sw_scale = sw_scale
        self.trackers = {"yaw": ValueTracker(self.view0.yaw), "pitch": ValueTracker(self.view0.pitch)}
        for k, v in params.items():
            self.trackers[k] = ValueTracker(float(v))
        self._labels = {}
        self._key = None
        self.pin = VMobject().set_points_as_corners([self.view0.origin, self.view0.origin + RIGHT * 0.01]).set_stroke(opacity=0).set_fill(opacity=0)
        self.redraw(force=True)
        self.add_updater(lambda m: m.redraw())

    # -- values
    def value(self, k):
        return self.trackers[k].get_value()

    def set(self, k, v):
        self.trackers[k].set_value(v)
        self.redraw()
        return self

    def to(self, k, v):
        return self.trackers[k].animate.set_value(v)

    def spin(self, degrees):
        return self.to("yaw", self.value("yaw") + degrees)

    def tilt(self, pitch):
        return self.to("pitch", pitch)

    # -- where it is on screen (the pin moves with every shift/scale applied to this stage or its parents)
    def _place(self):
        p = self.pin.get_points()
        o, e = p[0], p[-1]
        return o, np.linalg.norm(e - o) / 0.01

    def view(self):
        o, k = self._place()
        vals = {n: t.get_value() for n, t in self.trackers.items()}
        return self.view0.turned(origin=o, scale=self.view0.scale * k, yaw=vals["yaw"], pitch=vals["pitch"])

    def label(self, key, tex, size=30, color=INK):
        """A cached MathTex for draw() to place; it keeps its size relative to the stage as the stage is scaled."""
        if key not in self._labels:
            m = M(tex, size, color)
            self._labels[key] = (m, m.height, self._place()[1])
        m, h0, k0 = self._labels[key]
        if getattr(m, "_stage_hidden", False):
            m.set_opacity(1)
            m._stage_hidden = False
        want = h0 * self._place()[1] / k0
        if m.height > 0 and abs(m.height - want) > 1e-4:
            m.scale(want / m.height)
        return m

    def redraw(self, force=False):
        o, k = self._place()
        vals = tuple(round(t.get_value(), 6) for t in self.trackers.values())
        key = (round(o[0], 5), round(o[1], 5), round(k, 6), vals)
        if not force and key == self._key:
            return self
        self._key = key
        v = self.view()
        values = {n: t.get_value() for n, t in self.trackers.items() if n not in ("yaw", "pitch")}
        items = self.draw_fn(self, v, **values)
        pic = render(v, items, self.sw_scale * k)
        new = [self.pin] + list(pic.submobjects)
        if self._box0 is not None:
            o0 = self.view0.origin
            x0, y0, x1, y1 = self._box0
            cs = [o + k * (np.array([x, y, 0.0]) - o0) for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
            new.insert(1, VMobject().set_points_as_corners(cs + [cs[0]]).set_stroke(opacity=0).set_fill(opacity=0))
        # During an animation the Cairo renderer draws the family members it listed when the animation began, so
        # children replaced here would linger as ghosts of the starting picture: empty them in place instead.
        keep = {id(f) for m in new for f in m.get_family()}
        cached = {id(m[0]): m[0] for m in self._labels.values()}
        cached_fam = {id(f) for m in cached.values() for f in m.get_family()}
        for old in self.submobjects:
            if id(old) in cached:
                if id(old) not in keep:
                    old.set_opacity(0)
                    old._stage_hidden = True
                continue
            for f in old.get_family():
                if id(f) not in keep and id(f) not in cached_fam:
                    f.points = np.zeros((0, 3))
        self.submobjects = new
        return self

    def reserve(self, *poses, pad=0.15):
        """Make the stage's footprint the union of its pictures in these poses (dicts of param values, e.g.
        {"pitch": 90, "yaw": 0} and {"pitch": 26, "yaw": -32, "rise": 1}), so layout made around it holds in all of them."""
        now = {k: t.get_value() for k, t in self.trackers.items()}
        boxes = []
        self._box0 = None
        for pose in poses:
            for k, v in pose.items():
                self.trackers[k].set_value(v)
            self.redraw(force=True)
            fam = [m for m in self.submobjects[1:] if len(m.get_family()) > 1 or len(m.points)]
            if fam:
                g = VGroup(*fam)
                boxes.append((g.get_left()[0], g.get_bottom()[1], g.get_right()[0], g.get_top()[1]))
        for k, v in now.items():
            self.trackers[k].set_value(v)
        o, k = self._place()
        # stored in creation coordinates (redraw maps them through the pin)
        o0 = self.view0.origin
        to0 = lambda x, y: o0 + (np.array([x, y, 0.0]) - o) / k
        x0, y0 = to0(min(b[0] for b in boxes) - pad, min(b[1] for b in boxes) - pad)[:2]
        x1, y1 = to0(max(b[2] for b in boxes) + pad, max(b[3] for b in boxes) + pad)[:2]
        self._box0 = (x0, y0, x1, y1)
        self.redraw(force=True)
        return self

    def still(self):
        """A frozen copy (no updater) of the picture as it is now."""
        c = VGroup(*[m.copy() for m in self.submobjects[1:] if len(m.get_family()) > 1 or len(m.points)])
        c.clear_updaters()
        return c


# ---------------------------------------------------------------------------------------------------------- floor


def floor_curve(v, f, a, b, var="x", color=FUNC, width=4, n=80):
    s = np.linspace(a, b, n)
    pts = [(t, f(t), 0) if var == "x" else (f(t), t, 0) for t in s]
    m = VMobject().set_points_smoothly(list(v.P(np.array(pts, dtype=float))))
    return m.set_stroke(color, width).set_fill(opacity=0)


def floor_region(v, top, bot, a, b, var="x", color=AREA, opacity=0.35, n=60):
    s = np.linspace(a, b, n)
    if var == "x":
        pts = [(t, top(t), 0) for t in s] + [(t, bot(t), 0) for t in s[::-1]]
    else:
        pts = [(top(t), t, 0) for t in s] + [(bot(t), t, 0) for t in s[::-1]]
    return Polygon(*v.P(np.array(pts, dtype=float)), stroke_width=0, fill_color=color, fill_opacity=opacity)


def floor_segment(v, top, bot, at, var="x", color=SECANT, width=6):
    p, q = ((at, bot(at), 0), (at, top(at), 0)) if var == "x" else ((bot(at), at, 0), (top(at), at, 0))
    return Line(v.P(*p), v.P(*q), color=color, stroke_width=width)


def floor_axes(st, v, xr, yr, ticks=None, color=None, labels=True, size=28, tick_size=26):
    """x and y axes lying on the floor, with arrow tips, optional ticks {"x": [...], "y": [...]} and labels from the
    stage's label cache (so they stay crisp and sized with the stage)."""
    color = color or DIM
    k = v.scale
    out = []
    xa = Arrow(v.P(xr[0], 0, 0), v.P(xr[1], 0, 0), buff=0, color=color, stroke_width=2.5, tip_length=0.2 * min(1, k), max_tip_length_to_length_ratio=0.08)
    ya = Arrow(v.P(0, yr[0], 0), v.P(0, yr[1], 0), buff=0, color=color, stroke_width=2.5, tip_length=0.2 * min(1, k), max_tip_length_to_length_ratio=0.08)
    out += [xa, ya]
    ux, uy = v.P(1, 0, 0) - v.P(0, 0, 0), v.P(0, 1, 0) - v.P(0, 0, 0)
    for t in (ticks or {}).get("x", []):
        c = v.P(t, 0, 0)
        d = uy / max(np.linalg.norm(uy), 1e-6) * 0.07
        out.append(Line(c - d, c + d, color=color, stroke_width=2))
        lab = st.label(("tx", t), _num(t), tick_size, color)
        # below the axis on screen, or beside it when the y direction is foreshortened away
        out.append(lab.move_to(c + _away(-uy, lab)))
    for t in (ticks or {}).get("y", []):
        c = v.P(0, t, 0)
        d = ux / max(np.linalg.norm(ux), 1e-6) * 0.07
        out.append(Line(c - d, c + d, color=color, stroke_width=2))
        lab = st.label(("ty", t), _num(t), tick_size, color)
        out.append(lab.move_to(c + _away(-ux, lab)))
    if labels:
        lx = st.label("ax_x", "x", size, color)
        ly = st.label("ax_y", "y", size, color)
        out.append(lx.move_to(xa.get_end() + _away(ux, lx, 0.1)))
        out.append(ly.move_to(ya.get_end() + _away(uy, ly, 0.1)))
    return out


def _num(t):
    return str(int(t)) if float(t).is_integer() else f"{t:g}"


def _away(direction, lab, buff=0.12):
    """Offset that puts a label's box just past a point in screen `direction`."""
    d = np.array(direction, dtype=float)
    L = np.linalg.norm(d[:2])
    if L < 1e-6:
        d, L = np.array([0.0, -1.0, 0.0]), 1.0
    d = d / L
    # distance from the label's center to its box edge along d
    r = 0.5 * (abs(d[0]) * lab.width + abs(d[1]) * lab.height)
    return d * (r + buff)


# ---------------------------------------------------------------------------------------------------------- cross sections


def profile(kind, lo, hi, height=None, m=28, rise=1.0):
    """CCW (u, z) outline of a cross section standing on the base segment [lo, hi] (side s = hi - lo).
    rise in (0, 1] squashes the heights (a section standing up as rise goes from 0 to 1)."""
    if rise < 1.0:
        return [(u, z * max(rise, 1e-3)) for u, z in profile(kind, lo, hi, height, m)]
    s = hi - lo
    mid = (lo + hi) / 2
    if kind == "square":
        return [(lo, 0), (hi, 0), (hi, s), (lo, s)]
    if kind == "rect":
        h = height(s) if callable(height) else float(height)
        return [(lo, 0), (hi, 0), (hi, h), (lo, h)]
    if kind == "equilateral":
        return [(lo, 0), (hi, 0), (mid, s * np.sqrt(3) / 2)]
    if kind == "leg":
        return [(lo, 0), (hi, 0), (lo, s)]
    if kind == "hyp":
        return [(lo, 0), (hi, 0), (mid, s / 2)]
    if kind == "semicircle":
        return [(mid + s / 2 * np.cos(t), s / 2 * np.sin(t)) for t in np.linspace(0, PI, m)]
    raise ValueError(kind)


def _embed(axis, w, u, z):
    return (w, u, z) if axis == "x" else (u, w, z)


def prism(prof, w0, w1, axis="x", color=ACCUM, cap_color=None, side_color=None, edge=True, smooth=None, opacity=1.0, cap_decor=None,
          decor_color=None, cap_edge=None, cap_edge_width=1.6):
    """A convex profile (CCW (u, z) points) extruded along `axis` from w0 to w1: a slab with two caps and its sides.
    smooth: draw no edges between side faces (a curved side, such as a semicircle's); default True for long profiles.
    cap_decor: list of (u, z) polygons drawn on both caps (crumb holes)."""
    prof = [tuple(map(float, p)) for p in prof]
    n = len(prof)
    smooth = (n > 6) if smooth is None else smooth
    ax_dir = np.array([1.0, 0, 0]) if axis == "x" else np.array([0, 1.0, 0])
    faces = []
    cc, sc = cap_color or color, side_color or color
    for w, sgn in ((w0, -1), (w1, 1)):
        pts = [_embed(axis, w, u, z) for u, z in prof]
        dec = None
        if cap_decor:
            dec = [np.array([_embed(axis, w + sgn * 1e-3, u, z) for u, z in poly]) for poly in cap_decor]
        faces.append(Face(pts, cc, normal=sgn * ax_dir, edge=edge if cap_edge is None else cap_edge, opacity=opacity, decor=dec,
                          decor_color=decor_color, edge_width=cap_edge_width))
    for i in range(n):
        (u0, z0), (u1, z1) = prof[i], prof[(i + 1) % n]
        if abs(u1 - u0) + abs(z1 - z0) < 1e-9:
            continue
        nu, nz = z1 - z0, -(u1 - u0)                      # right of travel = outward for a CCW profile
        L = np.hypot(nu, nz)
        nrm = np.array(_embed(axis, 0.0, nu / L, nz / L))
        pts = [_embed(axis, w0, u0, z0), _embed(axis, w0, u1, z1), _embed(axis, w1, u1, z1), _embed(axis, w1, u0, z0)]
        is_base = abs(z0) < 1e-9 and abs(z1) < 1e-9
        faces.append(Face(pts, sc, normal=nrm, edge=(edge and not smooth) or (is_base and edge), opacity=opacity))
    return Body(faces, convex=True)


def slab(kind, top, bot, at, d, axis="x", color=ACCUM, height=None, rise=1.0, **kw):
    """One cross-section slab: thickness d centered at `at`, standing on [bot(at), top(at)]."""
    lo, hi = bot(at), top(at)
    if hi - lo < 1e-6:
        return None
    return prism(profile(kind, lo, hi, height, rise=rise), at - d / 2, at + d / 2, axis, color, **kw)


def slabs(kind, top, bot, a, b, n, gap=0.0, axis="x", color=ACCUM, height=None, rise=1.0, **kw):
    """n slabs filling [a, b], each as tall as the cross section at its middle; gap: fraction of each slab's width
    left empty (0.15 makes separate slices, 0 a stepped solid)."""
    w = (b - a) / n
    out = []
    for i in range(n):
        c = a + (i + 0.5) * w
        s = slab(kind, top, bot, c, w * (1 - gap), axis, color, height, rise, **kw)
        if s is not None:
            out.append(s)
    return out


def section_solid(kind, top, bot, a, b, n=60, axis="x", color=ACCUM, height=None, m=28, opacity=1.0, rise=1.0):
    """The smooth solid with these cross sections: each profile edge swept from a to b, plus the two end caps."""
    ws = np.linspace(a, b, n + 1)
    profs = [profile(kind, bot(w), top(w), height, m, rise) for w in ws]
    faces = []
    k = len(profs[0])
    for i in range(n):
        A, B = profs[i], profs[i + 1]
        for j in range(k):
            p = [_embed(axis, ws[i], *A[j]), _embed(axis, ws[i], *A[(j + 1) % k]), _embed(axis, ws[i + 1], *B[(j + 1) % k]), _embed(axis, ws[i + 1], *B[j])]
            p = np.array(p, dtype=float)
            if np.linalg.norm(np.cross(p[2] - p[0], p[3] - p[1])) < 1e-10:
                continue
            nrm = _newell(p)
            # orient outward: compare with the profile's own outward normal there
            (u0, z0), (u1, z1) = A[j], A[(j + 1) % k]
            if abs(u1 - u0) + abs(z1 - z0) < 1e-12:
                (u0, z0), (u1, z1) = B[j], B[(j + 1) % k]
            out2 = np.array(_embed(axis, 0.0, z1 - z0, -(u1 - u0)))
            if nrm @ out2 < 0:
                nrm = -nrm
            faces.append(Face(p, color, normal=nrm, edge=False, opacity=opacity))
    ax_dir = np.array([1.0, 0, 0]) if axis == "x" else np.array([0, 1.0, 0])
    for w, P_, sgn in ((a, profs[0], -1), (b, profs[-1], 1)):
        if abs(P_[1][0] - P_[0][0]) + abs(max(z for _, z in P_)) > 1e-6:
            faces.append(Face([_embed(axis, w, u, z) for u, z in P_], color, normal=sgn * ax_dir, edge=True, opacity=opacity))
    return Body(faces, closed=True)


def grow_slices(scene, make, ns, hold=0.7, fade=0.5, keep=True):
    """The slices get thinner: crossfade make(n) (a mobject, e.g. a Stage or a rendered picture) for each n in ns,
    holding each for `hold` seconds. Returns the last one (left on screen when keep)."""
    cur = None
    for n in ns:
        new = make(n)
        if cur is None:
            scene.play(FadeIn(new), run_time=fade)
        else:
            scene.play(FadeOut(cur), FadeIn(new), run_time=fade)
        cur = new
        scene.wait(hold)
    if not keep:
        scene.play(FadeOut(cur), run_time=fade)
    return cur


# ---------------------------------------------------------------------------------------------------------- revolution


def region_outline(top, bot, a, b, n=48):
    """CCW outline (graph coordinates) of the region between y = bot(x) and y = top(x), a <= x <= b."""
    s = np.linspace(a, b, n)
    return [(t, bot(t)) for t in s] + [(t, top(t)) for t in s[::-1]]


def outline_y(right, left, c, d, n=48):
    """CCW outline of the region between x = left(y) and x = right(y), c <= y <= d."""
    s = np.linspace(c, d, n)
    return [(left(t), t) for t in s[::-1]] + [(right(t), t) for t in s]


def rect_outline(x0, x1, y0, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def _rev(axis, at, gx, gy, th):
    """Graph point (gx, gy) turned by th about the axis line, in world coordinates (graph plane is y = 0)."""
    if axis == "x":
        r = gy - at
        return np.array([gx, -r * np.sin(th), at + r * np.cos(th)])
    r = gx - at
    return np.array([at + r * np.cos(th), -r * np.sin(th), gy])


def _rev_dir(axis, nx, ny, th):
    if axis == "x":
        return np.array([nx, -ny * np.sin(th), ny * np.cos(th)])
    return np.array([nx * np.cos(th), -nx * np.sin(th), ny])


def revolve(outline, axis="x", at=0.0, t0=0.0, t1=TAU, nt=48, color=ACCUM, cap_color=AREA, opacity=1.0, caps=True, grid=False):
    """The solid swept by a region (CCW outline in graph coordinates) turning about the axis line from angle t0 to t1.
    A full turn is closed (culled). A partial turn is open: two-sided, so its inside shows, and gets caps (the region
    itself in cap_color) at both ends. grid=True draws faint lines along the surface (helps it read as round)."""
    full = abs((t1 - t0) - TAU) < 1e-6
    n_t = max(2, int(np.ceil(nt * abs(t1 - t0) / TAU)))
    ths = np.linspace(t0, t1, n_t + 1)
    pts2 = [tuple(map(float, p)) for p in outline]
    k = len(pts2)
    faces = []
    for j in range(k):
        (x0, y0), (x1, y1) = pts2[j], pts2[(j + 1) % k]
        if abs(x1 - x0) + abs(y1 - y0) < 1e-9:
            continue
        nx, ny = y1 - y0, -(x1 - x0)
        L = np.hypot(nx, ny)
        nx, ny = nx / L, ny / L
        # an edge lying on the axis sweeps out nothing
        on_axis = (axis == "x" and abs(y0 - at) < 1e-9 and abs(y1 - at) < 1e-9) or (axis == "y" and abs(x0 - at) < 1e-9 and abs(x1 - at) < 1e-9)
        if on_axis:
            continue
        for i in range(n_t):
            a_, b_ = ths[i], ths[i + 1]
            q = np.array([_rev(axis, at, x0, y0, a_), _rev(axis, at, x1, y1, a_), _rev(axis, at, x1, y1, b_), _rev(axis, at, x0, y0, b_)])
            nrm = _rev_dir(axis, nx, ny, (a_ + b_) / 2)
            edge = (ManimColor(interpolate_color(ManimColor(color), BLACK, 0.2)) if grid and i % 4 == 0 else False)
            faces.append(Face(q, color, normal=nrm, edge=edge, opacity=opacity, edge_width=0.8))
    if caps and not full:
        for th, sgn in ((t0, -1), (t1, 1)):
            q = np.array([_rev(axis, at, x, y, th) for x, y in pts2])
            tang = _rev_dir(axis, 0, 1, th + PI / 2) if axis == "x" else _rev_dir(axis, 1, 0, th + PI / 2)
            faces.append(Face(q, cap_color, normal=sgn * tang, edge=True, opacity=opacity))
    return Body(faces, closed=full)


def disc(R, x, d, axis="x", at=0.0, color=ACCUM, nt=56, **kw):
    """One disc slice: radius R (from the axis), thickness d centered at x (a y value for axis "y")."""
    if axis == "x":
        return revolve(rect_outline(x - d / 2, x + d / 2, at, at + R), "x", at, nt=nt, color=color, **kw)
    return revolve(rect_outline(at, at + R, x - d / 2, x + d / 2), "y", at, nt=nt, color=color, **kw)


def washer(R, r, x, d, axis="x", at=0.0, color=ACCUM, nt=56, **kw):
    """One washer slice: outer radius R, hole radius r, thickness d centered at x. The hole's inner wall is drawn, so
    you can see into it from an angle."""
    if axis == "x":
        return revolve(rect_outline(x - d / 2, x + d / 2, at + r, at + R), "x", at, nt=nt, color=color, **kw)
    return revolve(rect_outline(at + r, at + R, x - d / 2, x + d / 2), "y", at, nt=nt, color=color, **kw)


def axis_line(axis, at, lo, hi, color=None, width=3, n=40, dashed=False):
    """The axis of revolution as short line pieces, to merge() with a solid so the solid hides what is inside it."""
    color = color or INK
    s = np.linspace(lo, hi, n + 1)
    faces = []
    for i in range(n):
        if dashed and i % 2:
            continue
        p = [_rev(axis, at, s[i], at, 0), _rev(axis, at, s[i + 1], at, 0)] if axis == "x" else [_rev(axis, at, at, s[i], 0), _rev(axis, at, at, s[i + 1], 0)]
        faces.append(Face(p, color, line=True, width=width))
    return Body(faces)


def upright_curve(v, f, a, b, var="x", color=FUNC, width=4, n=80):
    """A graph y = f(x) (or x = f(y)) drawn in the upright graph plane y = 0."""
    s = np.linspace(a, b, n)
    pts = [(t, 0, f(t)) if var == "x" else (f(t), 0, t) for t in s]
    return VMobject().set_points_smoothly(list(v.P(np.array(pts, dtype=float)))).set_stroke(color, width).set_fill(opacity=0)


def upright_region(v, top, bot, a, b, color=AREA, opacity=0.45, var="x", n=60):
    s = np.linspace(a, b, n)
    if var == "x":
        pts = [(t, 0, top(t)) for t in s] + [(t, 0, bot(t)) for t in s[::-1]]
    else:
        pts = [(top(t), 0, t) for t in s] + [(bot(t), 0, t) for t in s[::-1]]
    return Polygon(*v.P(np.array(pts, dtype=float)), stroke_width=0, fill_color=color, fill_opacity=opacity)


def upright_axes(st, v, xr, yr, color=None, size=28):
    """The graph's x and y axes in the upright plane (world x and z), with labels."""
    color = color or DIM
    xa = Arrow(v.P(xr[0], 0, 0), v.P(xr[1], 0, 0), buff=0, color=color, stroke_width=2.5, tip_length=0.18, max_tip_length_to_length_ratio=0.08)
    ya = Arrow(v.P(0, 0, yr[0]), v.P(0, 0, yr[1]), buff=0, color=color, stroke_width=2.5, tip_length=0.18, max_tip_length_to_length_ratio=0.08)
    lx, ly = st.label("ux", "x", size, color), st.label("uy", "y", size, color)
    return [xa, ya, lx.next_to(xa.get_end(), RIGHT, buff=0.08), ly.next_to(ya.get_end(), UP, buff=0.08)]


# ---------------------------------------------------------------------------------------------------------- props

CRUST, CRUST_TOP, CRUST_RIM, CRUMB, CRUMB_HOLE = "#B9773A", "#9A5A26", "#8E4F1E", "#F1DCAA", "#D9BC83"
WOOD, WOOD_SIDE = "#C99A64", "#A97A48"


def loaf_profile(w=1.0, h=0.6, dome=0.34, m=22):
    """CCW (u, z) outline of a sandwich loaf: straight pan sides and a domed top, centered on u = 0."""
    r = 0.07 * w
    pts = [(-w / 2 + r, 0.0), (w / 2 - r, 0.0)]
    pts += [(w / 2 - r + r * np.cos(t), r + r * np.sin(t)) for t in np.linspace(-PI / 2, 0, 5)[1:]]
    pts += [(w / 2, h)]
    pts += [(w / 2 * np.cos(t), h + dome * np.sin(t)) for t in np.linspace(0, PI, m)[1:-1]]
    pts += [(-w / 2, h)]
    pts += [(-w / 2 + r + r * np.cos(t), r + r * np.sin(t)) for t in np.linspace(PI, 1.5 * PI, 5)[:-1]]
    return pts


def _crumb_holes(w, h, dome, n=34, seed=7):
    rng = np.random.default_rng(seed)
    out = []
    while len(out) < n:
        u, z = rng.uniform(-0.42 * w, 0.42 * w), rng.uniform(0.07 * w, h + 0.75 * dome)
        if z > h and (u / (0.44 * w))**2 + ((z - h) / (0.8 * dome))**2 > 1:
            continue
        a, b, th = rng.uniform(0.008, 0.022) * w, rng.uniform(0.006, 0.014) * w, rng.uniform(0, PI)
        out.append([(u + a * np.cos(t) * np.cos(th) - b * np.sin(t) * np.sin(th), z + a * np.cos(t) * np.sin(th) + b * np.sin(t) * np.cos(th))
                    for t in np.linspace(0, TAU, 9)[:-1]])
    return out


def bread_slices(x0, x1, n, gap=0.0, w=1.0, h=0.6, dome=0.34, rim=5.0):
    """A sandwich loaf lying along x from x0 to x1, cut into n slices with `gap` (a fraction of a slice) between
    them: crust sides and top, crumb faces with a crust rim and a few holes, crusty heels at both ends. Returns a list
    of Bodies (slice i is element i), ready to move one with Body.moved()."""
    prof = loaf_profile(w, h, dome)
    holes = _crumb_holes(w, h, dome)
    d = (x1 - x0) / n
    out = []
    for i in range(n):
        a, b = x0 + i * d + d * gap / 2, x0 + (i + 1) * d - d * gap / 2
        body = prism(prof, a, b, "x", color=CRUST, cap_color=CRUMB, side_color=CRUST, edge=False, cap_edge=CRUST_RIM,
                     cap_edge_width=rim, cap_decor=holes, decor_color=CRUMB_HOLE)
        for f in body.faces[2:]:
            if f.pts[:, 2].min() > h * 0.98:
                f.color = CRUST_TOP
        if i == 0:
            body.faces[0].color, body.faces[0].decor, body.faces[0].edge = CRUST, None, False
        if i == n - 1:
            body.faces[1].color, body.faces[1].decor, body.faces[1].edge = CRUST, None, False
        out.append(body)
    return out


def cutting_board(x0, x1, y0, y1, t=0.08):
    """A wooden board on the floor, top at z = 0 (so things on it stand on the floor)."""
    return prism([(y0, -t), (y1, -t), (y1, 0), (y0, 0)], x0, x1, "x", color=WOOD_SIDE, cap_color=WOOD_SIDE, side_color=WOOD, edge=True)


# ---------------------------------------------------------------------------------------------------------- lessons


FLAT = {"yaw": 0.0, "pitch": 90.0}


def base_stage(curves, region, kind, xr, yr, at, n=10, var="x", ticks=None, height=None, color=ACCUM, scale=1.0, pose=(-32.0, 26.0),
               seg_label="s", gap=0.25, lines=()):
    """The picture for a cross-section worked example, as a Stage that starts as the student's flat 2D sketch.

    curves: [(f, lo, hi, color, tex, (lx, ly), var), ...] boundary curves on the floor (f of x for var "x", of y for
    "y"), each with its label's world position. region: (top, bot, a, b) in the slicing variable `var`.
    lines: [(x0, y0, x1, y1, color, tex, (lx, ly))] straight boundaries (x = 4, say), drawn with the curves.
    Params (all start at 0): c0, c1, ... draw each curve (and line) 0 -> 1; shade the base; seg the slice segment at
    `at` with its label; one stands the cross section on it (0 -> 1); many stands n slabs on the base; yaw/pitch.
    Cues: base_cues(st, pose) gives the usual moves as scene functions."""
    k_lines = len(curves)
    params = {f"c{i}": 0.0 for i in range(len(curves) + len(lines))}
    params.update(shade=0.0, seg=0.0, one=0.0, many=0.0, n=float(n))
    top, bot, a, b = region

    def draw(st, v, **p):
        out = list(floor_axes(st, v, xr, yr, ticks=ticks))
        if p["shade"] > 0:
            out.append(floor_region(v, top, bot, a, b, var=var, opacity=0.35 * p["shade"]))
        for i, (f, lo, hi, col, tex, lab, cvar) in enumerate(curves):
            t = p[f"c{i}"]
            if t > 0.01:
                out.append(floor_curve(v, f, lo, lo + (hi - lo) * t, var=cvar, color=col))
            if t > 0.98 and tex:
                out.append(st.label(("curve", i), tex, 28, col).move_to(v.P(lab[0], lab[1], 0)))
        for j, (x0, y0, x1, y1, col, tex, lab) in enumerate(lines):
            t = p[f"c{k_lines + j}"]
            if t > 0.01:
                out.append(Line(v.P(x0, y0, 0), v.P(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, 0), color=col, stroke_width=4))
            if t > 0.98 and tex:
                out.append(st.label(("line", j), tex, 28, col).move_to(v.P(lab[0], lab[1], 0)))
        if p["seg"] > 0.01:
            sg = floor_segment(v, top, bot, at, var=var)
            sg.set_stroke(opacity=p["seg"])
            out.append(sg)
        bodies = []
        nn = max(int(round(p["n"])), 1)
        w = (b - a) / nn
        k_at = min(nn - 1, max(0, int((at - a) / w)))          # the slab the highlighted one stands in for
        if p["many"] > 0.01:
            many = slabs(kind, top, bot, a, b, nn, gap=gap, axis=var, color=color, height=height, rise=p["many"])
            bodies += [bb for i, bb in enumerate(many) if not (p["one"] > 0.01 and i == k_at)]
        if p["one"] > 0.01:
            c = a + (k_at + 0.5) * w if p["many"] > 0.01 else at
            bodies.append(slab(kind, top, bot, c, w * (1 - gap), axis=var, color=SECANT, height=height, rise=p["one"]))
        out += [bb for bb in bodies if bb is not None]
        if p["seg"] > 0.98 and seg_label:
            # the segment's label sits off its middle, on the side away from the solid's front
            m = (bot(at) + top(at)) / 2
            pt = v.P(at, m, 0) if var == "x" else v.P(m, at, 0)
            lab = st.label("seg", seg_label, 30, SECANT)
            d = (v.P(1, 0, 0) - v.P(0, 0, 0)) if var == "x" else (v.P(0, 1, 0) - v.P(0, 0, 0))
            d = -d / max(np.linalg.norm(d), 1e-6)
            out.append(lab.move_to(pt + d * (0.12 + lab.width / 2 + 0.05)))
        return out

    st = Stage(draw, View(scale=scale, yaw=FLAT["yaw"], pitch=FLAT["pitch"]), **params)
    full = {f"c{i}": 1.0 for i in range(len(curves) + len(lines))}
    st.reserve(dict(FLAT, **full, shade=1, seg=1), dict(yaw=pose[0], pitch=pose[1], **full, shade=1, seg=1, many=1, one=1))
    st.pose = pose
    return st


def base_cues(st):
    """Scene functions for a base_stage: draw(i) a curve, shade(), seg(), stand() (tilt to the angled view and stand
    the one section up), fill() (stand n slabs), flat() (tilt back to the student's 2D sketch, the slabs gone)."""
    def draw(*idx, rt=1.2):
        return lambda sc: sc.play(*[st.to(f"c{i}", 1) for i in idx], run_time=rt)

    def shade(rt=0.8):
        return lambda sc: sc.play(st.to("shade", 1), run_time=rt)

    def seg(rt=0.8):
        return lambda sc: sc.play(st.to("seg", 1), run_time=rt)

    def stand(rt=2.0):
        def cue(sc):
            sc.play(st.to("yaw", st.pose[0]), st.to("pitch", st.pose[1]), run_time=rt)
            sc.play(st.to("one", 1), run_time=1.2)
        return cue

    def fill(rt=1.6):
        return lambda sc: sc.play(st.to("many", 1), run_time=rt)

    def flat(rt=1.8):
        def cue(sc):
            sc.play(st.to("many", 0), st.to("one", 0), run_time=0.8)
            sc.play(st.to("yaw", FLAT["yaw"]), st.to("pitch", FLAT["pitch"]), run_time=rt)
        return cue

    def both(*fns):
        def cue(sc):
            for f in fns:
                f(sc)
        return cue
    return dict(draw=draw, shade=shade, seg=seg, stand=stand, fill=fill, flat=flat, both=both)
