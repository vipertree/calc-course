"""Quick checks for solids.py (not a lesson). Render stills:

    cd anim && ./render.sh _solids_test.py Sheet -ql -s        # every builder on one frame
    cd anim && ./render.sh _solids_test.py Motion -ql          # tilt, spin, sweep, slice count (timing)
"""
import time

import numpy as np
from manim import *

from solids import *
from style import *


def _sq(s):
    return np.sqrt(max(s, 0))


class Sheet(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BG
        cells = []
        # 1. squares on sqrt x, separate slabs
        v = View(scale=0.55)
        cells.append(Stage(lambda st, v: [*floor_axes(st, v, (-0.3, 4.6), (-0.3, 2.4), ticks={"x": [4]}), floor_region(v, _sq, lambda s: 0, 0, 4),
                                          floor_curve(v, _sq, 0, 4.3), slabs("square", _sq, lambda s: 0, 0, 4, 6, gap=0.25)], v))
        # 2. smooth semicircle solid on 4 - x^2
        par = lambda s: 4 - s * s
        v = View(scale=0.38)
        cells.append(Stage(lambda st, v: [*floor_axes(st, v, (-2.6, 2.8), (-0.3, 4.6)), floor_region(v, par, lambda s: 0, -2, 2),
                                          section_solid("semicircle", par, lambda s: 0, -2, 2, color=DERIV)], v))
        # 3. triangles (equilateral, leg, hyp) slabs
        v = View(scale=0.55)
        cells.append(Stage(lambda st, v: [*floor_axes(st, v, (-0.3, 4.6), (-0.3, 2.4)), floor_region(v, _sq, lambda s: 0, 0, 4),
                                          *slabs("equilateral", _sq, lambda s: 0, 0, 1.3, 3, gap=0.3, color=SECANT), *slabs("leg", _sq, lambda s: 0, 1.4, 2.7, 3, gap=0.3),
                                          *slabs("hyp", _sq, lambda s: 0, 2.8, 4, 3, gap=0.3, color=TANGENT)], v))
        # 4. y-axis squares between x = y^2 and x = 4
        v = View(scale=0.36, yaw=-35)
        cells.append(Stage(lambda st, v: [*floor_axes(st, v, (-0.3, 4.8), (-2.5, 2.6)), floor_region(v, lambda y: 4, lambda y: y * y, -2, 2, var="y"),
                                          *slabs("square", lambda y: 4, lambda y: y * y, -2, 2, 8, gap=0.2, axis="y")], v))
        # 5. full solid of revolution about the x-axis + axis line
        v = View(scale=0.6, yaw=-25, pitch=18)
        cells.append(Stage(lambda st, v: [*upright_axes(st, v, (-0.3, 4.6), (-0.3, 2.6)), merge(revolve(region_outline(_sq, lambda s: 0, 0, 4), "x", 0, grid=True), axis_line("x", 0, -0.3, 4.6))], v))
        # 6. partial sweep of a washer region (between x and x^2) to see inside
        v = View(scale=1.5, yaw=-30, pitch=22)
        cells.append(Stage(lambda st, v: [*upright_axes(st, v, (-0.2, 1.3), (-0.2, 1.3)), revolve(region_outline(lambda s: s, lambda s: s * s, 0, 1), "x", 0, 0, 1.5 * PI)], v))
        # 7. a disc and a washer, angled
        v = View(scale=0.7, yaw=-50, pitch=20)
        cells.append(Stage(lambda st, v: [disc(1.4, 0, 0.5), washer(1.4, 0.8, 2.6, 0.5, color=SECANT)], v))
        # 8. about a vertical axis, cut away
        v = View(scale=0.7, yaw=-20, pitch=25)
        cells.append(Stage(lambda st, v: [*upright_axes(st, v, (-0.3, 2.4), (-0.3, 4.4)), revolve(outline_y(lambda y: np.sqrt(y), lambda y: 0, 0, 4), "y", 0, 0, 1.6 * PI)], v))
        g = Group(*cells).arrange_in_grid(2, 4, buff=0.6).set_max_width(13.5)
        self.add(g)


class Motion(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BG
        t0 = time.time()
        st = Stage(lambda st, v, n: [*floor_axes(st, v, (-0.3, 4.6), (-0.3, 2.4), ticks={"x": [1, 2, 3, 4], "y": [1, 2]}), floor_region(v, _sq, lambda s: 0, 0, 4),
                                     floor_curve(v, _sq, 0, 4.3), slabs("square", _sq, lambda s: 0, 0, 4, int(n), gap=0.15 if n < 40 else 0)],
                   View(origin=LEFT * 3 + DOWN * 1.5, scale=1.3, yaw=0, pitch=90), n=6)
        self.add(st)
        self.play(st.tilt(24), st.spin(-28), run_time=2)
        for n in (12, 24, 48):
            self.play(st.to("n", n), run_time=0.1)
            self.wait(0.4)
        self.play(st.spin(40), run_time=2)
        print("cross sections", time.time() - t0)
        self.clear()
        t0 = time.time()
        sw = Stage(lambda st, v, t: [*upright_axes(st, v, (-0.3, 4.6), (-0.3, 2.6)), upright_region(v, _sq, lambda s: 0, 0, 4),
                                     revolve(region_outline(_sq, lambda s: 0, 0, 4), "x", 0, 0, max(t, 1e-3)) if t > 1e-3 else None],
                   View(origin=LEFT * 3, scale=1.2, yaw=0, pitch=0), t=0)
        self.add(sw)
        self.play(sw.spin(-30), sw.tilt(20), run_time=1.5)
        self.play(sw.to("t", TAU), run_time=3)
        self.play(sw.spin(60), run_time=2)
        print("sweep", time.time() - t0)


class Bread(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BG

        def draw(st, v, gap, pull, turn):
            sl = bread_slices(-2.2, 2.2, 11, gap=gap, w=1.9, h=1.1, dome=0.6)
            k = 7
            if pull > 0:
                w = v.toward()
                phi = np.arctan2(w[1], w[0])
                c = sl[k].center
                sl[k] = sl[k].moved(R=rot("z", np.degrees(phi) * turn), t=(min(pull, 1) * 0.0 + max(pull - 1, 0) * 2.2, -1.6 * min(pull, 1) - max(pull - 1, 0) * 0.8, 0.9 * min(pull, 1)))
            return [cutting_board(-2.6, 2.6, -1.4, 1.4), *sl]
        st = Stage(draw, View(scale=1.0, yaw=-38, pitch=22), gap=0, pull=0, turn=0)
        self.add(st)
        self.play(st.to("gap", 0.12), run_time=1)
        self.play(st.to("pull", 1), run_time=1)
        self.play(st.to("pull", 2), st.to("turn", 1), run_time=1.5)
        self.wait(0.5)
