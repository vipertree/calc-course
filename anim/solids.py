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
SortLine(p0, p1, mob=, dashed=, tip=)    an axis in world coordinates. With no solid of revolution in the picture it is
SortMark(mob, pt)                        just `mob` (the flat sketch is unchanged); otherwise render() cuts it into short
                                         pieces after the last body and keeps the pieces no opaque solid of revolution
                                         hides from the viewer (a see-through ghost dims them), so an axis pokes out of
                                         a disc's face, an end cap or a washer's hole and vanishes inside a solid.
                                         revolve() records each solid's shape on its Body (body.rev; a shifted copy
                                         keeps it) for this test. upright_axes and rev_stage's axis of revolution use it.
SortPath(pts, mob=, color=, width=)      a curve lying ON a solid (rev_stage's generating curves and straight boundaries):
                                         the same piecewise test, each piece judged from a point nudged toward the viewer
                                         (bias), so it is hidden only by what is strictly in front of it, never by the
                                         surface, cap or disc rim it lies on, and dimmed through a see-through ghost.

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
                                         inner_color= colors the inner wall (faces looking toward the axis);
                                         grid="inner" adds meridians and rings on it only, so a hollow reads as one.
disc(R, x, d, ...) / washer(R, r, x, d)  one slice (a revolved rectangle): washers show the hole with its inner wall.
upright_axes(st, v, xr, yr)              the graph's axes standing in the plane y = 0 (sorted with the solid if you
                                         merge axis_line(...) pieces into it).
axis_line(axis, at, lo, hi)              the axis of revolution as sortable line pieces.

Lesson helpers (8.7, 8.8):
base_stage(curves, region, kind, ...)    a cross-section example as one Stage that starts as the flat 2D sketch (pitch
                                         90): params c0.. (draw each boundary), shade, seg (the slice), one (stand the
                                         highlighted section), many (the solid around it), fit (zoom the angled pose
                                         into the sketch's box). d=None (default): one thin slice, 1.2% of the range,
                                         with the smooth solid as a see-through ghost around it and the side's label
                                         by its base edge; d="slab": the older look, the section one of n slabs. base_cues(st) gives example() cue functions: draw(i, ...),
                                         shade(), seg(), stand(), fill() (with a slow turn), flat(), both(*cues).
Stage.reserve(*poses)                    fix a stage's footprint to the union of its pictures in those poses.
draw() may return (items, view)          to render with a changed view (zoom/pan driven by a param).
face_labels(v, cap, other, area, thick) a label pointing at a slab's face and a double arrow for its thickness.
Lesson helpers (8.9 on, revolution):
rev_stage(curves, outline, axis, k, edge, xr, yr, at, shade=, lines=, axis_tex=, axis_lab=, hole=, d=, ...)
                                         a revolution example as one Stage that starts as the flat upright sketch
                                         (FLAT_UP: yaw 0, pitch 0): params c0.. (draw each curve/line), shade, axis (the
                                         dashed axis of revolution y = k / x = k with its label), rad (the radius at `at`
                                         from the axis to edge(at), labeled R), sweep (0 -> 1: the region turns about the
                                         axis and the part swept so far stays), solid (opacity; slice() fades it to the
                                         ghost), one (the single thin disc at `at`; a washer when hole= is given, for
                                         8.11+), fit. extra(st, v, p) / extra_params add items and params of your own.
                                         d defaults to 1.2% of the range: one slice, thickness negligible.
                                         Washers (hole=): rin, the inner radius r beside R; the hollow's inner wall
                                         and the washer's hole wall in a toned color, with rings on the hollow's wall.
                                         Openings: wedge (cutaway quarter), cut_line, split/cut/pieces (pull the
                                         solid apart around one slice), many/n/smooth (rebuild it from slices).
rev_cues(st)                             draw(i..), shade(), axis(), rad(), rin(), spin() (tilt, sweep, slow turn), slice()
                                         (ghost + one disc with R on its face), flat() (back to the sketch, region and R),
                                         both(*cues). Pass cues to example(cues={step: ...}).
upright_axes(..., ticks=)                tick numbers on the upright axes.
Stage(..., fresh_labels=True)            labels sort with the picture during a play (rev_stage sets it; see label()).

Speed: faces are built by copying a template VMobject's state (_fast_vm) and collected into the picture in one go;
a full solid redraws in well under 0.1 s. Pictures are pixel-identical to the first version.

Props: bread_slices(...) a sliced sandwich loaf (crust, crumb faces with holes, end heels), cutting_board(...).

Gotcha (why redraw empties old children in place): during an animation the Cairo renderer draws the family members
it listed when the animation began, so replaced children would linger as ghosts.

Tested by anim/_solids_test.py: Sheet (every builder on one frame), Motion (tilt, spin, slice count, sweep; timing),
Bread (the loaf prop).
"""
import functools

import numpy as np
from manim import (DEGREES, PI, TAU, Mobject, ValueTracker, VGroup, VMobject, Arrow, Line, DashedLine, Polygon, SurroundingRectangle,
                   ManimColor, interpolate_color, WHITE, BLACK, FadeIn, FadeOut, ORIGIN, RIGHT, UP, DOWN, LEFT, smooth)

from style import BG, INK, DIM, FUNC, AREA, ACCUM, SECANT, TANGENT, DERIV, M

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

    def __init__(self, faces, convex=False, closed=False, name=None, rev=None):
        self.faces = [f for f in faces if f is not None]
        self.convex, self.closed, self.name = convex, closed, name
        self.rev = rev          # a solid of revolution's shape (see revolve), so axis lines can tell where it hides them
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
        rev = None
        if self.rev is not None and np.allclose(R, np.eye(3)):
            rev = dict(self.rev, shift=self.rev["shift"] + t)        # a shifted solid of revolution still hides lines
        return Body(out, self.convex, self.closed, self.name, rev=rev)

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


_PROTO = []


_RGB = {}


def _rgb(c):
    if isinstance(c, np.ndarray):
        return c
    key = c if isinstance(c, str) else None
    if key is not None and key in _RGB:
        return _RGB[key]
    out = np.asarray(ManimColor(c).to_rgb(), dtype=float)
    if key is not None:
        _RGB[key] = out
    return out


def _fast_vm(points, fill_rgba, stroke_rgba, sw):
    """A VMobject made by copying a template's state instead of running VMobject.__init__ (which was most of the time
    of a redraw: a solid is a thousand or more faces, rebuilt every frame)."""
    if not _PROTO:
        _PROTO.append(VMobject())
    m = VMobject.__new__(VMobject)
    d = dict(_PROTO[0].__dict__)
    d.update(submobjects=[], updaters=[], points=points, fill_rgbas=fill_rgba.reshape(1, 4), stroke_rgbas=stroke_rgba.reshape(1, 4),
             background_stroke_rgbas=_PROTO[0].background_stroke_rgbas.copy(), sheen_direction=_PROTO[0].sheen_direction.copy(),
             fill_opacity=float(fill_rgba[3]), stroke_opacity=float(stroke_rgba[3]), stroke_width=sw)
    m.__dict__ = d
    return m


def _corners(P):
    """Bezier points of the straight path through the points P (n, 3), as set_points_as_corners makes them."""
    a, b = P[:-1], P[1:]
    return np.stack([a, a + (b - a) / 3, a + 2 * (b - a) / 3, b], axis=1).reshape(-1, 3)


def _poly(pts2, fill, opacity, stroke, sw):
    P = np.asarray(pts2, dtype=float)
    P = np.vstack([P, P[:1]])
    return _fast_vm(_corners(P), np.append(_rgb(fill), opacity), np.append(_rgb(stroke), 1.0 if opacity > 0.99 else opacity), sw)


def _seg(p0, p1, color, sw):
    P = np.array([p0, p1], dtype=float)
    return _fast_vm(_corners(P), np.append(_rgb(color), 0.0), np.append(_rgb(color), 1.0), sw)


def _mix(a, b, t):
    return a + (b - a) * t


_BLACK, _WHITE = np.zeros(3), np.ones(3)


def _shade_rgb(view, color, n, flip=False, ambient=0.38):
    """View.shade as an rgb array (the same arithmetic, without making ManimColors)."""
    sn = view.screen_normal(np.asarray(n, dtype=float))
    if flip:
        sn = -sn
    k = ambient + (1 - ambient) * max(0.0, float(sn @ view.light))
    c = _rgb(color)
    if k < 0.75:
        return _mix(_mix(c, _BLACK, 0.5), c, k / 0.75)
    return _mix(c, _mix(c, _WHITE, 0.35), (k - 0.75) / 0.25)


def _face_mobs(view, f, flip, sw_scale):
    if f.line:
        p = view.P(f.pts)
        return [_seg(p[0], p[1], f.color, f.width * sw_scale)]
    col = _shade_rgb(view, f.color, f.normal, flip=flip) if f.shade else _rgb(f.color)
    if flip:
        col = _mix(col, _BLACK, 0.12)                           # insides read a touch darker
    p2 = view.P(f.pts)
    if f.edge is True:
        stroke, sw = _mix(_rgb(f.color), _BLACK, 0.45), f.edge_width
    elif f.edge:
        stroke, sw = _rgb(f.edge), f.edge_width
    elif f.opacity > 0.99:
        stroke, sw = col, 1.0                                   # same color: hides the seams between mesh faces
    else:
        stroke, sw = col, 0.0                                   # see-through: a seam stroke would double up into a grid
    out = [_poly(p2, col, f.opacity, stroke, sw * sw_scale)]
    if f.decor:
        dc = _rgb(f.decor_color) if f.decor_color else _mix(_rgb(f.color), _BLACK, 0.25)
        for d in f.decor:
            out.append(_poly(view.P(d), dc, f.opacity, dc, 0.5))
    return out


def _visible(view, f, cull):
    if f.normal is None:
        return True, False
    if f.line:                                  # a line piece on a surface (a ring) hides with the face it lies on
        return (not cull) or float(f.normal @ view.toward()) > 1e-6, False
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


class SortLine:
    """A straight line in world coordinates (an axis) that solids of revolution can hide. render() draws `mob` in place
    when no solid of revolution is in the picture (the flat sketch, unchanged); otherwise it cuts the line into short
    pieces after the last body and draws each piece that no opaque solid hides (dimmed by a see-through one), so an
    axis pokes out of a disc's face, an end cap or a washer's hole, and vanishes inside the solid. dashed: draw every
    other piece (dash length in screen units). tip: a mobject (an arrowhead) drawn when the end p1 shows."""

    def __init__(self, p0, p1, mob=None, color=INK, width=2.5, dashed=None, tip=None, frac=1.0):
        self.p0, self.p1 = np.asarray(p0, dtype=float), np.asarray(p1, dtype=float)
        self.mob, self.color, self.width, self.dashed, self.tip, self.frac = mob, color, width, dashed, tip, frac


class SortPath:
    """A curve lying ON a solid of revolution (the generating curve, a straight boundary): a polyline of world points.
    Like SortLine, it is `mob` on the flat sketch; with solids of revolution in the picture render() cuts it into short
    pieces, each tested from a point nudged a little toward the viewer, so it is hidden only by what is strictly in front
    of it, never by the surface, cap or disc rim it lies on, and dimmed through a see-through ghost."""

    def __init__(self, pts, mob=None, color=INK, width=4.0, bias=0.012):
        self.pts, self.mob, self.color, self.width, self.bias = np.asarray(pts, dtype=float), mob, color, width, bias


class SortMark:
    """A small mobject (a tick mark) pinned to one world point: drawn in place, or with the axis pieces when that point
    shows (see SortLine)."""

    def __init__(self, mob, pt):
        self.mob, self.pt = mob, np.asarray(pt, dtype=float)


def _in_poly(px, py, poly):
    """Even-odd point-in-polygon for arrays of points against one polygon (k, 2)."""
    x0, y0 = poly[:, 0], poly[:, 1]
    x1, y1 = np.roll(x0, -1), np.roll(y0, -1)
    PX, PY = px[..., None], py[..., None]
    with np.errstate(divide="ignore", invalid="ignore"):
        cross = ((y0 > PY) != (y1 > PY)) & (PX < (x1 - x0) * (PY - y0) / (y1 - y0) + x0)
    return np.count_nonzero(cross, axis=-1) % 2 == 1


def _rev_inside(rev, P):
    """Which world points (n, 3) lie inside a solid of revolution (revolve()'s rev record)."""
    q = P - rev["shift"]
    at, poly = rev["at"], rev["poly"]
    if rev["axis"] == "x":
        s, a, b = q[:, 0], -q[:, 1], q[:, 2] - at          # a = r sin(th), b = r cos(th) for the graph offset r
    else:
        s, a, b = q[:, 2], -q[:, 1], q[:, 0] - at
    rho = np.hypot(a, b)
    th = np.arctan2(a, b)
    hit = np.zeros(len(q), dtype=bool)
    for sgn, dth in ((1.0, 0.0), (-1.0, PI)):
        c = at + sgn * rho
        inside = _in_poly(s, c, poly) if rev["axis"] == "x" else _in_poly(c, s, poly)
        if not rev["full"]:
            span = rev["t1"] - rev["t0"]
            inside &= np.mod(th + dth - rev["t0"], TAU) <= span + 1e-9
        hit |= inside
    return hit


def _hidden_by(view, rev, lo, hi, P, n=40):
    """For world points P (m, 3): True where the sight line toward the viewer passes through the solid (box lo..hi)."""
    w = view.toward()
    m = len(P)
    # where each ray is inside the solid's box (slab method), from just off the point
    with np.errstate(divide="ignore", invalid="ignore"):
        ta, tb = (lo - P) / w, (hi - P) / w
    t_in = np.where(np.abs(w) < 1e-12, np.where((P >= lo) & (P <= hi), -np.inf, np.inf), np.minimum(ta, tb)).max(axis=1)
    t_out = np.where(np.abs(w) < 1e-12, np.where((P >= lo) & (P <= hi), np.inf, -np.inf), np.maximum(ta, tb)).min(axis=1)
    eps = 1e-4 * max(float(np.max(hi - lo)), 1e-6)
    t_in = np.maximum(t_in, eps)
    ok = t_out > t_in
    if not ok.any():
        return np.zeros(m, dtype=bool)
    u = np.linspace(0.0, 1.0, n)
    T = t_in[:, None] + (t_out - t_in)[:, None] * u[None, :]
    # thin pieces of the shape along the axis (a disc's thickness): also sample where the ray crosses their middles
    k = 0 if rev["axis"] == "x" else 1
    ss = np.unique(np.round(rev["poly"][:, k], 9))
    gaps = np.diff(ss)
    thin = (ss[:-1] + gaps / 2)[gaps < (ss[-1] - ss[0]) / n * 2] if len(ss) > 1 else np.zeros(0)
    ax = np.array([1.0, 0, 0]) if rev["axis"] == "x" else np.array([0, 0, 1.0])
    ws = w @ ax
    if len(thin) and abs(ws) > 1e-9:
        s0 = (P - rev["shift"]) @ ax
        Tm = (thin[None, :] - s0[:, None]) / ws
        Tm = np.where((Tm > t_in[:, None]) & (Tm < t_out[:, None]), Tm, t_in[:, None])
        T = np.hstack([T, Tm])
    pts = P[:, None, :] + T[..., None] * w[None, None, :]
    inside = _rev_inside(rev, pts.reshape(-1, 3)).reshape(T.shape)
    return ok & inside.any(axis=1)


def _late_lines(view, lines, occ, sw_scale):
    """Mobjects for the SortLines and SortMarks, each piece kept (and dimmed) by what hides it."""
    def keep(P):
        f = np.ones(len(P))
        for b in occ:
            op = b.faces[0].opacity if b.faces else 1.0
            if op < 0.02:
                continue
            f = np.where(_hidden_by(view, b.rev, b.lo, b.hi, P), f * (1 - min(op, 1.0)), f)
        return f
    out = []
    for it in lines:
        if isinstance(it, SortPath):
            out += _path_pieces(view, it, keep, occ)
            continue
        if isinstance(it, SortMark):
            f = keep(it.pt[None, :])[0]
            if f > 0.02:
                out.append(it.mob.copy().set_stroke(opacity=f) if f < 0.98 else it.mob)
            continue
        p1 = it.p0 + (it.p1 - it.p0) * it.frac
        L = float(np.linalg.norm(view.P(p1) - view.P(it.p0)))
        if L < 1e-4:
            continue
        step = it.dashed if it.dashed else 0.05
        n = max(2, int(np.ceil(L / step)))
        s = np.linspace(0.0, 1.0, n + 1)
        A = it.p0[None, :] + (p1 - it.p0)[None, :] * s[:-1, None]
        B = it.p0[None, :] + (p1 - it.p0)[None, :] * s[1:, None]
        f = keep((A + B) / 2)
        sa, sb = view.P(A), view.P(B)
        i = 0
        while i < n:                                   # join runs of pieces with the same look into one line
            if (it.dashed and i % 2) or f[i] < 0.02:
                i += 1
                continue
            j = i
            while j + 1 < n and not it.dashed and abs(f[j + 1] - f[i]) < 1e-6:
                j += 1
            out.append(Line(sa[i], sb[j], color=it.color, stroke_width=it.width, stroke_opacity=float(f[i])))
            i = j + 1
        if it.tip is not None and it.frac > 0.999:
            ft = keep(it.p1[None, :])[0]
            if ft > 0.02:
                out.append(it.tip if ft > 0.98 else it.tip.copy().set_opacity(ft))
    return out


def _path_pieces(view, it, keep, occ):
    """A SortPath as runs of visible pieces (see SortPath)."""
    P = it.pts
    if len(P) < 2:
        return []
    S = view.P(P)
    seg = np.linalg.norm(np.diff(S, axis=0), axis=1)
    # resample so no piece is longer than about 0.04 screen units
    reps = np.maximum(1, np.ceil(seg / 0.04).astype(int))
    Q = [P[0]]
    for i, k_ in enumerate(reps):
        for j in range(1, k_ + 1):
            Q.append(P[i] + (P[i + 1] - P[i]) * j / k_)
    Q = np.array(Q)
    ext = max((float(np.max(b.hi - b.lo)) for b in occ), default=1.0)
    mid = (Q[:-1] + Q[1:]) / 2 + view.toward()[None, :] * it.bias * ext
    f = keep(mid)
    SQ = view.P(Q)
    out, i, n = [], 0, len(f)
    while i < n:
        if f[i] < 0.02:
            i += 1
            continue
        j = i
        while j + 1 < n and abs(f[j + 1] - f[i]) < 1e-6:
            j += 1
        out.append(VMobject().set_points_as_corners(SQ[i:j + 2]).set_stroke(it.color, it.width, opacity=float(f[i])).set_fill(opacity=0))
        i = j + 1
    return out


def render(view, items, sw_scale=1.0):
    """Draw a list of items: Mobjects as they are (in order), runs of Bodies sorted far to near. SortLines and
    SortMarks (axes) are drawn in place, or, when solids of revolution are in the picture, after the last body, with
    the parts those solids hide left out."""
    flat = []
    for it in items:
        if isinstance(it, (list, tuple)):
            flat.extend(it)
        elif it is not None:
            flat.append(it)
    items = flat
    occ = [it for it in items if isinstance(it, Body) and it.rev is not None]
    last = max((i for i, it in enumerate(items) if isinstance(it, Body)), default=-1)
    late = []
    out = VGroup()
    mobs, seen = [], set()          # collected here and set once: VGroup.add per face was quadratic in the face count

    def put(m):
        if id(m) in seen:           # as VGroup.add: a mobject listed twice is drawn once, at its last place
            mobs.remove(m)
        seen.add(id(m))
        mobs.append(m)

    def flush(run):
        if not run:
            return
        # sort a copy and clear the caller's list (rebinding `run` here once left the bodies in it, drawn twice: again
        # at the end, over whatever was meant to sit on top of them)
        for b in sorted(run, key=functools.cmp_to_key(_body_cmp(view))):
            if b.convex:
                for f in b.faces:
                    vis, flip = _visible(view, f, True)
                    if vis:
                        mobs.extend(_face_mobs(view, f, flip, sw_scale))
            else:
                faces = []
                bias = 0.03 * float(np.max(b.hi - b.lo))     # a ring drawn on a surface sorts just in front of it
                for f in b.faces:
                    vis, flip = _visible(view, f, b.closed)
                    if vis:
                        d = float(view.depth(f.pts.mean(axis=0)))
                        faces.append((d - bias if (f.line and f.normal is not None) else d, f, flip))
                faces.sort(key=lambda t: -t[0])
                for _, f, flip in faces:
                    mobs.extend(_face_mobs(view, f, flip, sw_scale))
        run.clear()

    run = []
    for i, it in enumerate(items):
        if isinstance(it, (SortLine, SortMark, SortPath)):
            if occ and i < last:
                late.append(it)                 # drawn after the last body, below whatever follows it (labels)
            elif occ:
                flush(run)
                mobs.extend(_late_lines(view, [it], occ, sw_scale))
            elif isinstance(it, (SortMark, SortPath)) or it.mob is not None:
                flush(run)
                put(it.mob)
            else:
                flush(run)
                mobs.extend(_late_lines(view, [it], [], sw_scale))
        elif isinstance(it, Body):
            run.append(it)
        else:
            flush(run)
            put(it)
        if i == last:
            flush(run)
            if late:
                mobs.extend(_late_lines(view, late, occ, sw_scale))
    flush(run)
    out.submobjects = mobs
    return out


class Stage(VGroup):
    """A live 3D picture. draw(stage, view, **values) returns the items to render (see render()), or (items, view) to
    render with a changed view (an object zoomed or panned by a parameter). Every keyword
    parameter becomes a ValueTracker; yaw and pitch always exist. The picture is rebuilt on a frame when a value, or
    the stage's place on screen, has changed.

        st = Stage(draw, View(origin=..., scale=1.2, pitch=90), t=0)
        self.add(st)
        self.play(st.tilt(25), run_time=2)       # from the flat 2D graph to the angled view
        self.play(st.to("t", 1), run_time=3)     # whatever t means to draw()
        self.play(st.spin(60), run_time=3)       # turn the object

    Don't animate a Stage with .animate (its children are rebuilt); move it with shift/scale/next_to, or FadeIn/Out."""

    fresh_labels = False

    def __init__(self, draw, view=None, sw_scale=1.0, box=None, fresh_labels=False, **params):
        """box: (x0, y0, x1, y1) screen rectangle (where the stage is created) that the stage always occupies, drawn
        invisibly: the room the picture needs in every pose, so a layout made around it holds while it tilts.
        fresh_labels: label() hands out a copy each frame, so labels sort with the picture during a play (otherwise a
        label is drawn over the solids while animating; 8.7 and 8.8 were rendered without it)."""
        super().__init__()
        self.fresh_labels = fresh_labels
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
        if self.fresh_labels:
            # a copy each frame: during a play the renderer's list still names the cached label on its own, and that
            # later entry wins, so a cached label is drawn over everything (tick numbers showing through a solid)
            c = m.copy()
            c.clear_updaters()
            return c
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
        if isinstance(items, tuple) and len(items) == 2 and isinstance(items[1], View):
            items, v = items                     # draw() changed the view (zoomed or panned the object)
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


def revolve(outline, axis="x", at=0.0, t0=0.0, t1=TAU, nt=48, color=ACCUM, cap_color=AREA, opacity=1.0, caps=True, grid=False,
            inner_color=None):
    """The solid swept by a region (CCW outline in graph coordinates) turning about the axis line from angle t0 to t1.
    A full turn is closed (culled). A partial turn is open: two-sided, so its inside shows, and gets caps (the region
    itself in cap_color) at both ends. grid=True draws faint lines along the surface (helps it read as round);
    grid="inner" draws them only on the inner wall. inner_color: the color of the inner wall (the faces that look
    toward the axis: a washer's hole, a hollow solid's bowl), so you can see into the hollow; None keeps `color`."""
    full = abs((t1 - t0) - TAU) < 1e-6
    n_t = max(2, int(np.ceil(nt * abs(t1 - t0) / TAU)))
    ths = np.linspace(t0, t1, n_t + 1)
    pts2 = [tuple(map(float, p)) for p in outline]
    k = len(pts2)
    faces = []
    n_in = 0                                    # inner-wall edges so far (grid="inner" rings every few of them)
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
        # an inner wall looks toward the axis: its normal points back across the radius
        radial = ny * np.sign((y0 + y1) / 2 - at) if axis == "x" else nx * np.sign((x0 + x1) / 2 - at)
        inner = radial < -1e-9
        col = inner_color if (inner and inner_color is not None) else color
        g_on = grid is True or (grid == "inner" and inner)
        for i in range(n_t):
            a_, b_ = ths[i], ths[i + 1]
            q = np.array([_rev(axis, at, x0, y0, a_), _rev(axis, at, x1, y1, a_), _rev(axis, at, x1, y1, b_), _rev(axis, at, x0, y0, b_)])
            nrm = _rev_dir(axis, nx, ny, (a_ + b_) / 2)
            wall = abs(x1 - x0) < 1e-9 if axis == "x" else abs(y1 - y0) < 1e-9       # an end wall: no grid spokes on it
            if grid == "inner":
                edge = False
                if inner and i % 4 == 0:            # a meridian on the inner wall, as one clean line
                    faces.append(Face([q[0], q[1]], interpolate_color(ManimColor(col), BLACK, 0.3), line=True, width=1.2, opacity=opacity,
                                      normal=_rev_dir(axis, nx, ny, a_)))
            else:
                edge = (ManimColor(interpolate_color(ManimColor(col), BLACK, 0.2)) if g_on and i % 4 == 0 and not wall else False)
            faces.append(Face(q, col, normal=nrm, edge=edge, opacity=opacity, edge_width=0.8))
        if grid == "inner" and inner:
            if n_in % 6 == 3:                   # a ring around the hollow: shows how deep it goes
                ring = interpolate_color(ManimColor(col), BLACK, 0.3)
                for i in range(n_t):
                    faces.append(Face([_rev(axis, at, x0, y0, ths[i]), _rev(axis, at, x0, y0, ths[i + 1])], ring, line=True, width=1.2,
                                      opacity=opacity, normal=_rev_dir(axis, nx, ny, (ths[i] + ths[i + 1]) / 2)))
            n_in += 1
    if caps and not full:
        # each cap is the region itself, cut into thin strips across the axis so it depth-sorts against the small
        # surface faces (one big polygon sorted by its center showed through the solid's narrow end); its outline is
        # drawn as sortable line pieces
        strips = _cap_strips(pts2, axis)
        rim = interpolate_color(ManimColor(cap_color), BLACK, 0.45)
        for th, sgn in ((t0, -1), (t1, 1)):
            tang = _rev_dir(axis, 0, 1, th + PI / 2) if axis == "x" else _rev_dir(axis, 1, 0, th + PI / 2)
            for quad in strips:
                q = np.array([_rev(axis, at, x, y, th) for x, y in quad])
                faces.append(Face(q, cap_color, normal=sgn * tang, edge=False, opacity=opacity))
            for j in range(k):
                (x0, y0), (x1, y1) = pts2[j], pts2[(j + 1) % k]
                if abs(x1 - x0) + abs(y1 - y0) > 1e-9:
                    faces.append(Face([_rev(axis, at, x0, y0, th), _rev(axis, at, x1, y1, th)], rim, line=True, width=1.6))
    return Body(faces, closed=full, rev=dict(poly=np.array(pts2, dtype=float), axis=axis, at=float(at), t0=float(t0), t1=float(t1),
                                             full=full, shift=np.zeros(3)))


def _cap_strips(pts2, axis, n=40):
    """A polygon (graph coordinates) cut into quads between n + 1 lines across the axis (x = const for a horizontal
    axis, y = const for a vertical one). Each line meets the outline in pairs of crossings (the region's intervals);
    a strip joins matching intervals on neighboring lines."""
    i_s, i_c = (0, 1) if axis == "x" else (1, 0)
    S = np.array([p[i_s] for p in pts2])
    C = np.array([p[i_c] for p in pts2])
    k = len(pts2)

    def cuts(s):
        xs = []
        for j in range(k):
            s0, s1 = S[j], S[(j + 1) % k]
            if (s0 <= s < s1) or (s1 <= s < s0):
                xs.append(C[j] + (s - s0) / (s1 - s0) * (C[(j + 1) % k] - C[j]))
        xs.sort()
        return list(zip(xs[0::2], xs[1::2]))
    lo, hi = S.min(), S.max()
    eps = 1e-7 * max(hi - lo, 1e-9)
    grid = np.linspace(lo + eps, hi - eps, n + 1)
    rows = [cuts(s) for s in grid]
    out = []
    for i in range(n):
        A, B = rows[i], rows[i + 1]
        if len(A) != len(B):
            continue
        for (a0, a1), (b0, b1) in zip(A, B):
            quad = [(grid[i], a0), (grid[i + 1], b0), (grid[i + 1], b1), (grid[i], a1)]
            out.append([(q[0], q[1]) if axis == "x" else (q[1], q[0]) for q in quad])
    return out


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


def upright_axes(st, v, xr, yr, color=None, size=28, ticks=None, tick_size=26, labels=True):
    """The graph's x and y axes in the upright plane (world x and z), with labels. ticks: {"x": [...], "y": [...]}
    adds tick marks with numbers (below the x-axis, left of the y-axis, as on paper; beside them when turned)."""
    color = color or DIM
    xa = Arrow(v.P(xr[0], 0, 0), v.P(xr[1], 0, 0), buff=0, color=color, stroke_width=2.5, tip_length=0.18, max_tip_length_to_length_ratio=0.08)
    ya = Arrow(v.P(0, 0, yr[0]), v.P(0, 0, yr[1]), buff=0, color=color, stroke_width=2.5, tip_length=0.18, max_tip_length_to_length_ratio=0.08)
    # the axes go to render() as SortLines: drawn as these arrows on the flat sketch, cut where a solid hides them
    out = [SortLine((xr[0], 0, 0), (xr[1], 0, 0), mob=xa, color=color, width=2.5, tip=xa.get_tip()),
           SortLine((0, 0, yr[0]), (0, 0, yr[1]), mob=ya, color=color, width=2.5, tip=ya.get_tip())]
    if labels:
        lx, ly = st.label("ux", "x", size, color), st.label("uy", "y", size, color)
        out += [lx.next_to(xa.get_end(), RIGHT, buff=0.08), ly.next_to(ya.get_end(), UP, buff=0.08)]
    ux, uz = v.P(1, 0, 0) - v.P(0, 0, 0), v.P(0, 0, 1) - v.P(0, 0, 0)
    for t in (ticks or {}).get("x", []):
        c = v.P(t, 0, 0)
        d = uz / max(np.linalg.norm(uz), 1e-6) * 0.07
        out.append(SortMark(Line(c - d, c + d, color=color, stroke_width=2), (t, 0, 0)))
        lab = st.label(("utx", t), _num(t), tick_size, color)
        out.append(lab.move_to(c + _away(-uz, lab)))
    for t in (ticks or {}).get("y", []):
        c = v.P(0, 0, t)
        d = ux / max(np.linalg.norm(ux), 1e-6) * 0.07
        out.append(SortMark(Line(c - d, c + d, color=color, stroke_width=2), (0, 0, t)))
        lab = st.label(("uty", t), _num(t), tick_size, color)
        out.append(lab.move_to(c + _away(-ux, lab)))
    return out


# ---------------------------------------------------------------------------------------------------------- labels


def face_labels(v, cap, other, area, thick):
    """(kit-dependent) A label pointing at a lifted slab's face (beside it, not on it) and a double arrow for its thickness across the top."""
    from kit import nudge_arrow
    c = v.P(cap.pts.mean(axis=0))
    top = max(range(len(cap.pts)), key=lambda i: v.P(cap.pts[i])[1])
    lab = M(area, 36, INK).move_to(c + LEFT * 1.9 + UP * 0.2)
    ptr = Arrow(lab.get_right() + RIGHT * 0.05, c, buff=0.08, color=INK, stroke_width=3, max_tip_length_to_length_ratio=0.15)
    p0, p1 = v.P(cap.pts[top]), v.P(other.pts[top])
    arr = nudge_arrow(p0 + UP * 0.25, p1 + UP * 0.25, label=thick, side=UP)
    return VGroup(lab, ptr), arr


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
               seg_label="s", gap=0.25, lines=(), d=None, ghost=0.3):
    """The picture for a cross-section worked example, as a Stage that starts as the student's flat 2D sketch.

    curves: [(f, lo, hi, color, tex, (lx, ly), var), ...] boundary curves on the floor (f of x for var "x", of y for
    "y"), each with its label's world position. region: (top, bot, a, b) in the slicing variable `var`.
    lines: [(x0, y0, x1, y1, color, tex, (lx, ly))] straight boundaries (x = 4, say), drawn with the curves.
    Params (all start at 0): c0, c1, ... draw each curve (and line) 0 -> 1; shade the base; seg the slice segment at
    `at` with its label; one stands the cross section on it (0 -> 1); many stands n slabs on the base; yaw/pitch.
    d: the highlighted slice's thickness. None (the default, for worked examples) is one thin slice, 1.2% of the
    slicing range, thickness negligible; then `many` raises the smooth solid as a see-through ghost (opacity `ghost`)
    around that one slice, and the side's label stays on the slice's base edge. d="slab" is the older look: the
    highlighted section is one of the n slabs (a visible wedge, thickness (b - a)/n). A number is that thickness.
    Cues: base_cues(st, pose) gives the usual moves as scene functions."""
    k_lines = len(curves)
    params = {f"c{i}": 0.0 for i in range(len(curves) + len(lines))}
    params.update(shade=0.0, seg=0.0, one=0.0, many=0.0, n=float(n), fit=0.0)
    top, bot, a, b = region
    thin = d != "slab"
    span = (xr[1] - xr[0]) if var == "x" else (yr[1] - yr[0])
    dd = (0.012 * span if d is None else float(d)) if thin else None     # one thin slice: its thickness is negligible
    fit_to = [1.0, np.zeros(3)]                 # zoom and shift (creation units) that fit the angled pose in the flat box

    def draw(st, v, **p):
        if p["fit"] > 0:
            z = 1 + (fit_to[0] - 1) * p["fit"]
            kk = v.scale / st.view0.scale
            v = v.turned(origin=v.origin + fit_to[1] * kk * p["fit"], scale=v.scale * z)
        out = list(floor_axes(st, v, xr, yr, ticks=ticks))
        if p["shade"] > 0:
            out.append(floor_region(v, top, bot, a, b, var=var, opacity=0.35 * p["shade"]))
        for i, (f, lo, hi, col, tex, lab, cvar) in enumerate(curves):
            t = p[f"c{i}"]
            if t > 0.01:
                out.append(floor_curve(v, f, lo, lo + (hi - lo) * t, var=cvar, color=col))
            if t > 0.98 and tex and p["fit"] < 0.5:          # sketch labels: off while the solid stands (they'd sit on it)
                out.append(st.label(("curve", i), tex, 28, col).move_to(v.P(lab[0], lab[1], 0)))
        for j, (x0, y0, x1, y1, col, tex, lab) in enumerate(lines):
            t = p[f"c{k_lines + j}"]
            if t > 0.01:
                out.append(Line(v.P(x0, y0, 0), v.P(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, 0), color=col, stroke_width=4))
            if t > 0.98 and tex and p["fit"] < 0.5:
                out.append(st.label(("line", j), tex, 28, col).move_to(v.P(lab[0], lab[1], 0)))
        if p["seg"] > 0.01:
            sg = floor_segment(v, top, bot, at, var=var)
            sg.set_stroke(opacity=p["seg"])
            out.append(sg)
        bodies = []
        nn = max(int(round(p["n"])), 1)
        w = (b - a) / nn
        k_at = min(nn - 1, max(0, int((at - a) / w)))          # the slab the highlighted one stands in for
        if thin:
            if p["many"] > 0.01:
                # the smooth solid as a see-through ghost, drawn first; the one thin slice goes over it
                out.append(section_solid(kind, top, bot, a, b, axis=var, color=color, height=height, rise=p["many"],
                                         opacity=ghost * min(1.0, p["many"] / 0.3)))
                out.append(VMobject())
            if p["one"] > 0.01:
                bodies.append(slab(kind, top, bot, at, dd, axis=var, color=SECANT, height=height, rise=p["one"], cap_edge_width=2.6))
        else:
            if p["many"] > 0.01:
                many = slabs(kind, top, bot, a, b, nn, gap=gap, axis=var, color=color, height=height, rise=p["many"])
                bodies += [bb for i, bb in enumerate(many) if not (p["one"] > 0.01 and i == k_at)]
            if p["one"] > 0.01:
                c = a + (k_at + 0.5) * w if p["many"] > 0.01 else at
                bodies.append(slab(kind, top, bot, c, w * (1 - gap), axis=var, color=SECANT, height=height, rise=p["one"]))
        out += [bb for bb in bodies if bb is not None]
        if p["seg"] > 0.98 and seg_label and (p["one"] < 0.01 or (thin and p["fit"] > 0.5)):
            # the segment's label sits off its middle, on the side away from the solid's front (on a backing once the
            # thin slice stands, so it reads over the ghost)
            m = (bot(at) + top(at)) / 2
            pt = v.P(at, m, 0) if var == "x" else v.P(m, at, 0)
            lab = st.label("seg", seg_label, 30, SECANT)
            u = (v.P(1, 0, 0) - v.P(0, 0, 0)) if var == "x" else (v.P(0, 1, 0) - v.P(0, 0, 0))
            u = -u / max(np.linalg.norm(u), 1e-6)
            if thin and p["one"] > 0.01:
                # beside the slice's base edge, on the screen-down side (the slice rises above it)
                q0, q1 = (v.P(at, bot(at), 0), v.P(at, top(at), 0)) if var == "x" else (v.P(bot(at), at, 0), v.P(top(at), at, 0))
                e = q1 - q0
                u = np.array([e[1], -e[0], 0.0]) / max(np.linalg.norm(e), 1e-6)
                u = u if u[1] < 0 else -u
            lab.move_to(pt + _away(u, lab, 0.14))
            if p["one"] > 0.01:
                out.append(SurroundingRectangle(lab, buff=0.05, corner_radius=0.06, stroke_width=0).set_fill(BG, 0.85))
            out.append(lab)
        return out, v

    st = Stage(draw, View(scale=scale, yaw=FLAT["yaw"], pitch=FLAT["pitch"]), **params)
    full = {f"c{i}": 1.0 for i in range(len(curves) + len(lines))}
    flat_pose = dict(FLAT, **full, shade=1, seg=1)
    angled = dict(yaw=pose[0], pitch=pose[1], **full, shade=1, seg=1, many=1, one=1)

    def box(pose_):
        for k_, v_ in pose_.items():
            st.trackers[k_].set_value(v_)
        st.redraw(force=True)
        g = VGroup(*[m for m in st.submobjects[1:] if len(m.get_family()) > 1 or len(m.points)])
        return np.array([g.get_left()[0], g.get_bottom()[1], g.get_right()[0], g.get_top()[1]])
    F, B = box(flat_pose), box(angled)
    o = st.view0.origin
    z = 0.97 * min((F[2] - F[0]) / (B[2] - B[0]), (F[3] - F[1]) / (B[3] - B[1]))
    Fc, Bc = np.array([(F[0] + F[2]) / 2, (F[1] + F[3]) / 2, 0]), np.array([(B[0] + B[2]) / 2, (B[1] + B[3]) / 2, 0])
    fit_to[0], fit_to[1] = z, Fc - o - z * (Bc - o)
    for k_ in st.trackers:
        st.trackers[k_].set_value(params.get(k_, FLAT.get(k_, 0.0)))
    st.reserve(flat_pose)
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
            sc.play(st.to("yaw", st.pose[0]), st.to("pitch", st.pose[1]), st.to("fit", 1), run_time=rt)
            sc.play(st.to("one", 1), run_time=1.2)
        return cue

    def fill(rt=1.6, turn=16.0, hold=3.0):
        def cue(sc):
            sc.play(st.to("many", 1), run_time=rt)
            if turn:
                sc.play(st.spin(turn), run_time=hold)       # a slow turn while it is up, so there is time to look
        return cue

    def flat(rt=1.8):
        def cue(sc):
            sc.play(st.to("many", 0), st.to("one", 0), run_time=0.8)
            sc.play(st.to("yaw", FLAT["yaw"]), st.to("pitch", FLAT["pitch"]), st.to("fit", 0), run_time=rt)
        return cue

    def both(*fns):
        def cue(sc):
            for f in fns:
                f(sc)
        return cue
    return dict(draw=draw, shade=shade, seg=seg, stand=stand, fill=fill, flat=flat, both=both)


# ---------------------------------------------------------------------------------------------------------- revolution lessons

FLAT_UP = {"yaw": 0.0, "pitch": 0.0}             # the upright graph seen straight on: exactly the student's 2D sketch


def _gpt(axis, s, c):
    """Graph point of slice position s (x for a horizontal axis, y for a vertical one) and cross coordinate c."""
    return (s, c) if axis == "x" else (c, s)


def _clip_outline(outline, i_s, c, side):
    """The part of a polygon (graph coordinates) with coordinate i_s <= c (side -1) or >= c (side 1): one
    Sutherland-Hodgman pass, enough for a region between two graphs."""
    pts = [tuple(map(float, q)) for q in outline]
    keep = (lambda q: q[i_s] <= c + 1e-12) if side < 0 else (lambda q: q[i_s] >= c - 1e-12)
    out = []
    for j in range(len(pts)):
        a, b = pts[j - 1], pts[j]
        if keep(b):
            if not keep(a):
                t = (c - a[i_s]) / (b[i_s] - a[i_s])
                out.append(tuple(a[m] + t * (b[m] - a[m]) for m in range(2)))
            out.append(b)
        elif keep(a):
            t = (c - a[i_s]) / (b[i_s] - a[i_s])
            out.append(tuple(a[m] + t * (b[m] - a[m]) for m in range(2)))
    return out


def _front_ring(v, axis, k, s, c, frac, color, n=64):
    """The cut line drawn around a solid of revolution at slice position s (graph cross coordinate c of its outer
    edge), frac of the way around: only the half that faces us, drawn over the solid."""
    w = v.toward()
    sg = 1.0 if c >= k else -1.0
    g = _gpt(axis, s, c)
    th = np.linspace(0, TAU * frac, max(2, int(n * frac)) + 1)
    out = []
    for a, b_ in zip(th[:-1], th[1:]):
        nrm = _rev_dir(axis, 0.0, sg, (a + b_) / 2) if axis == "x" else _rev_dir(axis, sg, 0.0, (a + b_) / 2)
        if nrm @ w > 0:
            out.append(Line(v.P(_rev(axis, k, g[0], g[1], a)), v.P(_rev(axis, k, g[0], g[1], b_)), color=color, stroke_width=5))
    return out


def rev_stage(curves, outline, axis, k, edge, xr, yr, at, shade=None, lines=(), ticks=None, color=ACCUM, disc_color=SECANT,
              rad_color=TANGENT, axis_color=None, axis_tex=None, axis_lab=None, scale=1.0, pose=(-30.0, 20.0), turn=24.0, d=None,
              hole=None, rad_label="R", rad_side=-1, ghost=0.35, nt=48, extra=None, extra_params=None, rin_color=None, rin_label="r",
              inner=None, lab_at=0.5):
    """The picture for a solid-of-revolution worked example, as a Stage that starts as the student's flat 2D sketch
    (the upright graph seen straight on, FLAT_UP), the revolution counterpart of base_stage.

    curves: [(f, lo, hi, color, tex, (lx, ly), var), ...] boundary curves (y = f(x) for var "x", x = f(y) for "y"),
    each with its label's graph position. lines: [(x0, y0, x1, y1, color, tex, (lx, ly))] straight boundaries.
    shade: (top, bot, a, b, var) the region, as upright_region takes it. outline: the region's CCW outline (graph
    coordinates: region_outline / outline_y) that revolve() sweeps about the axis ("x": the line y = k, "y": x = k).
    edge(s): the curve's cross coordinate at slice position s, so R(s) = |edge(s) - k|; hole(s): the inner edge for a
    washer (8.11 on). at: the slice we care about. lab_at: where along R (and r) their labels sit (0.5: the middle; move it
    when the middle would put a label on a coordinate axis). axis_tex: draw the axis of revolution as a dashed line with this
    label at graph point axis_lab (for an axis other than a coordinate axis).
    extra(st, v, p) -> items drawn on top, with extra_params {name: start value} as more params.
    Washers (hole= given): rin draws the inner radius r from the axis to hole(at) (rin_color, default DERIV), R and r
    then sit side by side (R on rad_side, r on the other) so neither covers the other; the hollow's inner wall and the
    washer's hole wall get their own tone (inner=, default the color mixed 30% toward the background: darker on a dark
    page, lighter on paper), with faint rings and meridians on the hollow's wall, so you can see into it.

    Params (all start at 0 unless noted): c0, c1, ... draw each curve (and line) 0 -> 1; shade; axis (the dashed axis
    line); rad (the R segment at `at` and its label); sweep (the region turning about the axis, 0 -> 1 = a full turn; the
    part swept so far stays); solid (1: its opacity, faded to `ghost` to see a slice inside); one (the disc at `at`, with
    R drawn on its face); fit (zoom the angled pose into the sketch's box); yaw/pitch. Cues: rev_cues(st).
    For a lesson's opening (8.11 on; all off by default): wedge (0 -> 1 cuts the quarter of the full solid between its
    top and the side facing us away, so the hollow and the wall, the region itself, show); cut_line (a ring drawn
    around the solid at `at`); split (1: the solid is cut at `at`: the two pieces, opacity pieces (1), slide apart by
    cut, leaving the slice of thickness d; a solid below 1 shows as a ghost behind them); many (the solid rebuilt
    from n slices, n starts at 8, then smooth = 1 for the smooth solid). Pass d= for a slice thick enough to see."""
    k_lines = len(curves)
    params = {f"c{i}": 0.0 for i in range(len(curves) + len(lines))}
    params.update(shade=0.0, axis=0.0, rad=0.0, rin=0.0, sweep=0.0, solid=1.0, one=0.0, fit=0.0, wedge=0.0, cut_line=0.0, split=0.0, cut=0.0,
                  pieces=1.0, many=0.0, n=8.0, smooth=0.0)
    params.update(extra_params or {})
    axis_color = axis_color or INK
    rin_color = rin_color or DERIV
    dark = (lambda c: interpolate_color(ManimColor(c), ManimColor(BG), 0.3))     # darker on a dark page, lighter on paper
    in_solid = (inner if inner is not None else dark(color)) if hole else None
    in_disc = (inner if inner is not None else dark(disc_color)) if hole else None
    span = (xr[1] - xr[0]) if axis == "x" else (yr[1] - yr[0])
    dd = d if d is not None else 0.012 * span          # one thin slice: its thickness is negligible
    s_lo, s_hi = (min(q[0 if axis == "x" else 1] for q in outline), max(q[0 if axis == "x" else 1] for q in outline))
    fit_to = [1.0, np.zeros(3)]

    def world(gx, gy, off=0.0):
        """Graph point to world, nudged `off` along the slicing direction (onto a disc's face)."""
        return (gx + off, 0.0, gy) if axis == "x" else (gx, 0.0, gy + off)

    def draw(st, v, **p):
        if p["fit"] > 0:
            z = 1 + (fit_to[0] - 1) * p["fit"]
            kk = v.scale / st.view0.scale
            v = v.turned(origin=v.origin + fit_to[1] * kk * p["fit"], scale=v.scale * z)
        flat = p["fit"] < 0.5
        out = list(upright_axes(st, v, xr, yr, ticks=ticks))
        lit = p["shade"] * max(0.0, 1 - p["sweep"] / 0.04)        # once it turns, the region is the solid's end face
        if shade and lit > 0.01:
            top, bot, a, b, var = shade
            out.append(upright_region(v, top, bot, a, b, var=var, opacity=0.45 * lit))
        for i, (f, lo, hi, col, tex, lab, cvar) in enumerate(curves):
            t = p[f"c{i}"]
            if t > 0.01:
                # the curve lies on the solid's outer surface: sorted in pieces, so a disc's rim never covers it
                ss = np.linspace(lo, lo + (hi - lo) * t, 80)
                wp = [(q, 0.0, f(q)) if cvar == "x" else (f(q), 0.0, q) for q in ss]
                out.append(SortPath(wp, mob=upright_curve(v, f, lo, lo + (hi - lo) * t, var=cvar, color=col), color=col, width=4))
            if t > 0.98 and tex and flat:
                out.append(st.label(("curve", i), tex, 28, col).move_to(v.P(lab[0], 0, lab[1])))
        for j, (x0, y0, x1, y1, col, tex, lab) in enumerate(lines):
            t = p[f"c{k_lines + j}"]
            if t > 0.01:
                e = (x0 + (x1 - x0) * t, 0, y0 + (y1 - y0) * t)
                out.append(SortPath([(x0, 0, y0), e], mob=Line(v.P(x0, 0, y0), v.P(*e), color=col, stroke_width=4), color=col, width=4))
            if t > 0.98 and tex and flat:
                out.append(st.label(("line", j), tex, 28, col).move_to(v.P(lab[0], 0, lab[1])))
        if axis_tex and p["axis"] > 0.01:
            (g0, g1) = ((xr[0], k), (xr[1], k)) if axis == "x" else ((k, yr[0]), (k, yr[1]))
            q0, q1 = v.P(*world(*g0)), v.P(*world(*g1))
            out.append(SortLine(world(*g0), world(*g1), mob=DashedLine(q0, q0 + (q1 - q0) * p["axis"], color=axis_color, stroke_width=4, dash_length=0.14),
                                color=axis_color, width=4, dashed=0.14, frac=p["axis"]))
            if p["axis"] > 0.98 and axis_lab is not None and flat:
                out.append(st.label("axis", axis_tex, 28, axis_color).move_to(v.P(*world(*axis_lab))))
        sw, op, one = p["sweep"], p["solid"], p["one"]
        skw = dict(inner_color=in_solid, grid="inner") if hole else {}
        sgn = 1.0 if edge(at) >= k else -1.0           # which side of the axis the region is on
        if p["many"] > 0.01:
            # the solid rebuilt from n slices (n = 8, 16, 40, ...), then smooth
            if p["smooth"] > 0.5:
                out.append(revolve(outline, axis, k, nt=nt, color=color, **skw))
            else:
                nn = max(1, int(round(p["n"])))
                w = (s_hi - s_lo) / nn
                for i in range(nn):
                    m = s_lo + (i + 0.5) * w
                    R_ = abs(edge(m) - k)
                    ww = w * (0.82 if nn < 30 else 1.0)
                    out.append(washer(R_, abs(hole(m) - k), m, ww, axis, k, color=color, nt=40, inner_color=in_solid) if hole
                               else disc(R_, m, ww, axis, k, color=color, nt=40))
        elif p["split"] > 0.5:
            # cut at `at`: the two pieces slide apart (cut) and fade (pieces), leaving the one slice
            if op < 0.99 and op > 0.01:
                out += [revolve(outline, axis, k, nt=nt, color=color, opacity=op, **skw), VMobject()]
            if p["pieces"] > 0.01:
                g, po = 0.6 * p["cut"] * span / 4, (1.0 if p["pieces"] > 0.99 else p["pieces"])
                tv = (lambda d_: (d_, 0, 0)) if axis == "x" else (lambda d_: (0, 0, d_))
                for side_, mv in ((-1, -g), (1, g)):
                    piece = _clip_outline(outline, 0 if axis == "x" else 1, at + side_ * dd / 2, side_)
                    if len(piece) >= 3:
                        out.append(revolve(piece, axis, k, nt=nt, color=color, opacity=po, **skw).moved(t=tv(mv)))
            out.append(washer(abs(edge(at) - k), abs(hole(at) - k), at, dd, axis, k, color=disc_color, inner_color=in_disc) if hole
                       else disc(abs(edge(at) - k), at, dd, axis, k, color=disc_color))
        elif sw > 1e-3 and op > 0.01:
            t1 = TAU if sw > 0.999 else sw * TAU
            t0 = 0.0
            if p["wedge"] > 0.01 and sw > 0.999:       # a quarter cut away (top to front), to see inside
                if sgn > 0:
                    t0 = p["wedge"] * PI / 2
                else:
                    t1 = TAU - p["wedge"] * PI / 2
            out.append(revolve(outline, axis, k, t0, t1, nt=nt, color=color, opacity=1.0 if op > 0.99 else op, **skw))
            if p["cut_line"] > 0.01:
                out += _front_ring(v, axis, k, at, edge(at), p["cut_line"], disc_color)
        if one > 0.01 and p["split"] < 0.5 and p["many"] < 0.01:
            R = abs(edge(at) - k)
            body = (washer(R, abs(hole(at) - k), at, dd, axis, k, color=disc_color, opacity=min(1.0, one), inner_color=in_disc)
                    if hole else disc(R, at, dd, axis, k, color=disc_color, opacity=min(1.0, one)))
            if op < 0.99:
                out.append(VMobject())          # the ghost is drawn first, the slice over it
            out.append(body)
        # the radius: on the sketch, then on the slice's face that shows (hidden inside a solid being swept)
        vis = 1.0 if (one > 0.5 or op < 0.5) else max(0.0, 1 - sw / 0.04)
        radii = [("rad", edge, rad_color, rad_label, rad_side)]
        if hole:
            radii.append(("rin", hole, rin_color, rin_label, -rad_side))
        for key, fn, col, tex, side in radii:
            show = p[key] * vis
            if show < 0.01:
                continue
            off = 0.0
            if one > 0.5:
                n = np.array([1.0, 0, 0]) if axis == "x" else np.array([0, 0, 1.0])
                off = dd / 2 * (1 if n @ v.toward() >= 0 else -1)
            p0, p1 = v.P(*world(*_gpt(axis, at, k), off)), v.P(*world(*_gpt(axis, at, fn(at)), off))
            u = p1 - p0
            u = u / max(np.linalg.norm(u), 1e-6)
            perp = np.array([-u[1], u[0], 0.0]) * (-side)
            if hole:                            # R and r side by side, each nudged to its own side
                p0, p1 = p0 + perp * 0.05, p1 + perp * 0.05
            p1 = p0 + (p1 - p0) * min(1.0, p[key])
            out.append(Line(p0, p1, color=BG, stroke_width=11, stroke_opacity=min(1.0, show)))
            out.append(Line(p0, p1, color=col, stroke_width=6, stroke_opacity=min(1.0, show)))
            if p[key] > 0.98 and tex:
                lab = st.label(key, tex, 32, col)
                lab.set_opacity(min(1.0, show))
                lab.move_to(p0 + (p1 - p0) * lab_at + _away(perp, lab, 0.1))
                if one > 0.5:                   # on the slice's face: a backing so it reads on any color
                    out.append(SurroundingRectangle(lab, buff=0.05, corner_radius=0.06, stroke_width=0).set_fill(BG, 0.85 * min(1.0, show)))
                out.append(lab)
        if extra:
            out += list(extra(st, v, p))
        return out, v

    st = Stage(draw, View(scale=scale, yaw=FLAT_UP["yaw"], pitch=FLAT_UP["pitch"]), fresh_labels=True, **params)
    full = {f"c{i}": 1.0 for i in range(len(curves) + len(lines))}
    flat_pose = dict(FLAT_UP, **full, shade=1, axis=1, rad=1, rin=1 if hole else 0)
    angled = [dict(yaw=y_, pitch=pose[1], **full, shade=1, axis=1, sweep=1) for y_ in (pose[0], pose[0] + turn)]

    def box(pose_):
        for k_, v_ in pose_.items():
            st.trackers[k_].set_value(v_)
        st.redraw(force=True)
        g = VGroup(*[m for m in st.submobjects[1:] if len(m.get_family()) > 1 or len(m.points)])
        return np.array([g.get_left()[0], g.get_bottom()[1], g.get_right()[0], g.get_top()[1]])
    F = box(flat_pose)
    Bs = [box(a_) for a_ in angled]
    B = np.array([min(b_[0] for b_ in Bs), min(b_[1] for b_ in Bs), max(b_[2] for b_ in Bs), max(b_[3] for b_ in Bs)])
    o = st.view0.origin
    z = 0.97 * min((F[2] - F[0]) / (B[2] - B[0]), (F[3] - F[1]) / (B[3] - B[1]))
    Fc, Bc = np.array([(F[0] + F[2]) / 2, (F[1] + F[3]) / 2, 0]), np.array([(B[0] + B[2]) / 2, (B[1] + B[3]) / 2, 0])
    fit_to[0], fit_to[1] = z, Fc - o - z * (Bc - o)
    for k_ in st.trackers:
        st.trackers[k_].set_value(params.get(k_, FLAT_UP.get(k_, 0.0)))
    st.reserve(flat_pose)
    st.pose, st.turn_by, st.ghost = pose, turn, ghost
    return st


def rev_cues(st):
    """Scene functions for a rev_stage: draw(i) a curve, shade(), axis(), rad(); spin() turns the sketch to the angled
    view and sweeps the region around the axis (the swept part stays), then turns the whole solid slowly; slice() fades
    the solid to a ghost and stands the one disc at `at` in it with its R; flat() goes back to the 2D sketch (on paper:
    the region and one R)."""
    def draw(*idx, rt=1.2):
        return lambda sc: sc.play(*[st.to(f"c{i}", 1) for i in idx], run_time=rt)

    def one_param(name, rt):
        return lambda sc: sc.play(st.to(name, 1), run_time=rt)

    def spin(rt=2.0, sweep=4.0, hold=2.5):
        def cue(sc):
            sc.play(st.to("yaw", st.pose[0]), st.to("pitch", st.pose[1]), st.to("fit", 1), run_time=rt)
            sc.play(st.to("sweep", 1), run_time=sweep, rate_func=smooth)
            if hold:
                sc.play(st.spin(st.turn_by), run_time=hold)
        return cue

    def slice_(rt=1.4, hold=0.0):
        def cue(sc):
            sc.play(st.to("solid", st.ghost), st.to("one", 1), run_time=rt)
            if hold:
                sc.play(st.spin(-st.turn_by / 2), run_time=hold)
        return cue

    def flat(rt=1.8):
        def cue(sc):
            sc.play(st.to("one", 0), st.to("solid", 0), run_time=0.8)
            st.set("sweep", 0)
            st.set("solid", 1)
            sc.play(st.to("yaw", FLAT_UP["yaw"]), st.to("pitch", FLAT_UP["pitch"]), st.to("fit", 0), run_time=rt)
        return cue

    def both(*fns):
        def cue(sc):
            for f in fns:
                f(sc)
        return cue
    return dict(draw=draw, shade=lambda rt=0.8: one_param("shade", rt), axis=lambda rt=0.8: one_param("axis", rt),
                rad=lambda rt=0.8: one_param("rad", rt), rin=lambda rt=0.8: one_param("rin", rt), spin=spin, slice=slice_, flat=flat, both=both)
