"""Trig Review lesson 0.1 (T1): Right-triangle trigonometry. Narration comes from transcripts/0_1.md."""
import numpy as np
from manim import *

from kit import *
from style import *
from props import brick_wall, ground, ladder, person_walking

WOOD, WOOD_DARK = "#C08A4E", "#8A5A2B"


def tree(height=3.2):
    """A leafy tree (vector art); the base of the trunk is at the group's bottom center."""
    trunk = Polygon([-0.14, 0, 0], [0.14, 0, 0], [0.09, height * 0.55, 0], [-0.09, height * 0.55, 0], stroke_width=0, fill_color="#8B5A2B", fill_opacity=1)
    greens = ["#3E7C3A", "#4E9A45", "#5DAF52"]
    crown = VGroup(*[Circle(radius=r, stroke_width=0, fill_color=greens[k % 3], fill_opacity=1).move_to([dx, height * 0.55 + dy, 0])
                     for k, (r, dx, dy) in enumerate(((0.75, 0, 0.55), (0.6, -0.55, 0.3), (0.6, 0.55, 0.3), (0.55, 0, 0.95), (0.45, -0.35, 0.85), (0.45, 0.35, 0.85)))])
    return VGroup(trunk, crown)


def surveyor_scene(d=6.0, ang=35):
    """Ground, a tree, a sighting tube d units away, the right triangle with the 35 degree angle."""
    g = -2.6
    T0 = np.array([3.0, g, 0])
    tr = tree((d * np.tan(np.radians(ang)) - 1.5) / 0.55).move_to(T0, aligned_edge=DOWN)
    top = np.array([T0[0], g + d * np.tan(np.radians(ang)), 0])
    S = T0 + LEFT * d
    grd = Line(LEFT * 6.3 + UP * g, RIGHT * 5.5 + UP * g, color=SAND, stroke_width=6)
    tube = VGroup(Line(S, S + 0.55 * np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang)), 0]), color=INK, stroke_width=9),
                  Line(S, S + DOWN * 0.001, color=INK))
    tri = Polygon(S, T0, top, stroke_color=SECANT, stroke_width=3)
    sight = DashedLine(S, top, color=SECANT)
    arc = Arc(radius=0.8, angle=np.radians(ang), arc_center=S, color=SECANT, stroke_width=4)
    labs = VGroup(M(r"20 \text{ m}", 40).next_to(Line(S, T0), DOWN, buff=0.2), M(f"{ang}^\\circ", 38, SECANT).move_to(S + 1.2 * np.array([np.cos(np.radians(ang / 2)), np.sin(np.radians(ang / 2)), 0])),
                  M("h", 46, FUNC).next_to(Line(T0, top), RIGHT, buff=1.0))
    return VGroup(grd, tr, tube, tri, sight, arc, labs)


def ladder_scene():
    """Marisol's ladder: the wooden ladder sprite at 70 degrees against a brick wall."""
    L, a = 4.4, np.radians(70)
    W = np.array([1.2, -2.2, 0])
    foot = W + LEFT * L * np.cos(a)
    topp = W + UP * L * np.sin(a)
    wall = brick_wall(height=4.8, width=0.6).move_to(W + RIGHT * 0.3 + UP * 2.4)
    grd = ground(5.2).move_to(W + LEFT * 1.2, aligned_edge=UP)
    lad = ladder(foot, topp, width=0.45)
    labs = VGroup(M(r"6 \text{ m}", 40).move_to((foot + topp) / 2 + LEFT * 0.65), Arc(radius=0.6, angle=a, arc_center=foot, color=SECANT, stroke_width=4),
                  M(r"70^\circ", 40, SECANT).move_to(foot + RIGHT * 0.95 + UP * 0.4),
                  DashedLine(W + LEFT * 0.06, topp + LEFT * 0.06, color=FUNC), M("h", 40, FUNC).move_to(W + UP * L * np.sin(a) / 2 + LEFT * 0.3))
    return Group(grd, wall, lad, labs)


def kite(size=1.0):
    """A diamond kite with cross spars and a tail of bows."""
    top, right, bot, left = UP * 0.55, RIGHT * 0.4, DOWN * 0.95, LEFT * 0.4
    sail = VGroup(Polygon(top, right, ORIGIN, stroke_width=0, fill_color="#D7263D", fill_opacity=1),
                  Polygon(right, bot, ORIGIN, stroke_width=0, fill_color="#F6C945", fill_opacity=1),
                  Polygon(bot, left, ORIGIN, stroke_width=0, fill_color="#D7263D", fill_opacity=1),
                  Polygon(left, top, ORIGIN, stroke_width=0, fill_color="#F6C945", fill_opacity=1),
                  Polygon(top, right, bot, left, stroke_color=INK, stroke_width=2))
    spars = VGroup(Line(top, bot, color=WOOD_DARK, stroke_width=3), Line(left, right, color=WOOD_DARK, stroke_width=3))
    pts = [bot + np.array([0.25 * np.sin(2.2 * s), -0.45 * s, 0]) for s in np.linspace(0, 3, 30)]
    tail = VMobject(color=INK, stroke_width=2).set_points_smoothly(pts)
    bows = VGroup(*[VGroup(Polygon(UP * 0.0, LEFT * 0.13 + UP * 0.08, LEFT * 0.13 + DOWN * 0.08, stroke_width=0, fill_color=c, fill_opacity=1),
                           Polygon(UP * 0.0, RIGHT * 0.13 + UP * 0.08, RIGHT * 0.13 + DOWN * 0.08, stroke_width=0, fill_color=c, fill_opacity=1)).move_to(pts[k])
                    for k, c in ((9, "#5B9BD5"), (19, "#59A96A"), (28, "#5B9BD5"))])
    return VGroup(tail, bows, sail, spars).scale(size)


def kite_scene():
    """Jordan's kite: 30 m up, the string at 40 degrees from a hand at ground level."""
    u, a = 0.12, np.radians(40)
    H = 30 * u
    S = np.array([-3.2, -2.3, 0])
    K = S + np.array([H / np.tan(a), H, 0])
    foot = np.array([K[0], S[1], 0])
    grd = ground(7.0).move_to(S + RIGHT * 2.4, aligned_edge=UP)
    spool = VGroup(Circle(radius=0.16, stroke_color=INK, stroke_width=2, fill_color=WOOD, fill_opacity=1), Dot(radius=0.04, color=INK)).move_to(S)
    string = Line(S, K, color=INK, stroke_width=3)
    kt = kite(0.75).move_to(K + DOWN * 0.15 + RIGHT * 0.02)
    labs = VGroup(DashedLine(foot, K, color=FUNC), M(r"30 \text{ m}", 40, FUNC).next_to(Line(foot, K), RIGHT, buff=0.3),
                  Arc(radius=0.8, angle=a, arc_center=S, color=SECANT, stroke_width=4), M(r"40^\circ", 40, SECANT).move_to(S + 1.2 * np.array([np.cos(a / 2), np.sin(a / 2), 0])),
                  M("L", 40).move_to((S + K) / 2 + 0.4 * np.array([-np.sin(a), np.cos(a), 0])))
    return VGroup(grd, labs, string, spool, kt)


def building(width=1.6, height=3.6):
    """An apartment block with rows of windows; its bottom center is the group's bottom center."""
    body = Rectangle(width=width, height=height, stroke_color=INK, stroke_width=2, fill_color="#B9A38A", fill_opacity=1)
    cols, rows = 3, int(height / 0.6)
    wins = VGroup(*[Rectangle(width=width / (cols * 1.9), height=0.3, stroke_width=0, fill_color="#5B9BD5", fill_opacity=0.85)
                    .move_to(body.get_corner(UL) + RIGHT * width * (c + 0.5) / cols + DOWN * (0.45 + 0.6 * r)) for c in range(cols) for r in range(rows - 1)])
    door = Rectangle(width=0.32, height=0.5, stroke_width=0, fill_color=WOOD_DARK, fill_opacity=1).move_to(body.get_bottom(), aligned_edge=DOWN)
    roof = Rectangle(width=width + 0.16, height=0.12, stroke_width=0, fill_color=INK, fill_opacity=1).move_to(body.get_top())
    return VGroup(body, wins, door, roof)


def rooftop_scene(labels=True):
    """Priya 50 m from a 30 m building: the right triangle from her feet to the roof."""
    u = 0.1
    S = np.array([-3.0, -2.3, 0])
    B = S + RIGHT * 50 * u
    blg = building(1.6, 30 * u).move_to(B + RIGHT * 0.8, aligned_edge=DOWN)
    top = B + UP * 30 * u
    grd = ground(7.4).move_to(S + RIGHT * 2.8, aligned_edge=UP)
    priya = person_walking(height=1.1).move_to(S + LEFT * 0.35, aligned_edge=DOWN)
    th = np.arctan2(30, 50)
    g = Group(grd, blg, priya, Polygon(S, B, top, stroke_color=SECANT, stroke_width=3))
    if labels:
        g.add(M(r"50 \text{ m}", 40).next_to(Line(S, B), DOWN, buff=0.35), M(r"30 \text{ m}", 40, FUNC).next_to(blg, RIGHT, buff=0.15),
              Arc(radius=0.8, angle=th, arc_center=S, color=SECANT, stroke_width=4), M(r"\theta", 40, SECANT).move_to(S + 1.15 * np.array([np.cos(th / 2), np.sin(th / 2), 0])))
    return g


def ramp_scene():
    """Deshawn's skateboard ramp: a plywood wedge, surface 4 m, high end 1.2 m, with a board on top."""
    u = 1.2
    th = np.arcsin(0.3)
    A = np.array([-2.4, -1.6, 0])
    run = 4 * u * np.cos(th)
    B, C = A + RIGHT * run, A + RIGHT * run + UP * 1.2 * u
    wedge = Polygon(A, B, C, stroke_color=WOOD_DARK, stroke_width=3, fill_color=WOOD, fill_opacity=1)
    slats = VGroup(*[Line(A + RIGHT * x, A + RIGHT * x + UP * x * np.tan(th), color=WOOD_DARK, stroke_width=2) for x in np.linspace(0.6, run - 0.05, 6)])
    d = (C - A) / np.linalg.norm(C - A)
    n = np.array([-d[1], d[0], 0])
    mid = A + 0.62 * (C - A)
    board = VGroup(RoundedRectangle(width=1.0, height=0.09, corner_radius=0.04, stroke_width=0, fill_color="#3A3A3A", fill_opacity=1),
                   Dot(LEFT * 0.33 + DOWN * 0.1, radius=0.065, color="#E8C547"), Dot(RIGHT * 0.33 + DOWN * 0.1, radius=0.065, color="#E8C547"))
    board.rotate(th).move_to(mid + n * 0.17)
    grd = ground(run + 2.2).move_to((A + B) / 2, aligned_edge=UP)
    labs = VGroup(M(r"4 \text{ m}", 40).move_to((A + C) / 2 + n * 0.75 + LEFT * 0.3), M(r"1.2 \text{ m}", 40, FUNC).next_to(Line(B, C), RIGHT, buff=0.15),
                  Arc(radius=0.9, angle=th, arc_center=A, color=SECANT, stroke_width=4), M(r"\theta", 40, SECANT).move_to(A + 1.25 * np.array([np.cos(th / 2), np.sin(th / 2), 0])))
    return VGroup(grd, wedge, slats, board, labs)


class Lesson(TranscriptScene):
    NUM = "0.1"

    def construct(self):
        with self.beat("How tall is the tree") as b:
            sc = surveyor_scene()
            self.play(FadeIn(sc[0]), FadeIn(sc[1]), FadeIn(sc[2]), run_time=1)
            self.play(Create(sc[4]), Create(sc[5]), FadeIn(sc[6][1]), run_time=1)
            self.play(FadeIn(sc[6][0]), run_time=0.5)
            b.line(1)
            self.play(Create(sc[3]), run_time=1)
            b.line(2)
            self.play(FadeIn(sc[6][2]), Indicate(sc[6][2]), run_time=1)
        self.clear()
        self.title()

        with self.beat("Naming the sides") as b:
            A, B, C = np.array([-5.6, -2.2, 0]), np.array([-0.6, -2.2, 0]), np.array([-0.6, 1.2, 0])
            tri = Polygon(A, B, C, color=INK, stroke_width=4)
            sq = Square(0.3, color=DIM, stroke_width=2).move_to(B + LEFT * 0.15 + UP * 0.15)
            self.play(Create(tri), FadeIn(sq), run_time=1)
            hyp = Line(A, C, color=ACCUM, stroke_width=8)
            hyp_lab = T("hypotenuse (longest side)", 32, ACCUM).rotate(np.arctan2(C[1] - A[1], C[0] - A[0])).move_to((A + C) / 2 + 0.45 * np.array([-0.56, 0.83, 0]))
            self.play(Create(hyp), FadeIn(hyp_lab), run_time=1)
            b.line(1)
            arcA = VGroup(Arc(radius=0.7, angle=np.arctan2(C[1] - A[1], C[0] - A[0]), arc_center=A, color=SECANT, stroke_width=4),
                          M(r"\theta", 34, SECANT).move_to(A + RIGHT * 1.05 + UP * 0.32))
            self.play(FadeIn(arcA), run_time=0.6)
            opp = Line(B, C, color=FUNC, stroke_width=8)
            adj = Line(A, B, color=DERIV, stroke_width=8)
            opp_lab = T("opposite", 32, FUNC).next_to(opp, RIGHT, buff=0.2)
            adj_lab = T("adjacent", 32, DERIV).next_to(adj, DOWN, buff=0.2)
            self.play(Create(opp), FadeIn(opp_lab), run_time=0.8)
            self.play(Create(adj), FadeIn(adj_lab), run_time=0.8)
            b.line(2)
            angC = np.arctan2(A[1] - C[1], A[0] - C[0])
            arcC = VGroup(Arc(radius=0.7, start_angle=angC, angle=-PI / 2 - angC, arc_center=C, color=SECANT, stroke_width=4),
                          M(r"\theta", 34, SECANT).move_to(C + DOWN * 1.05 + LEFT * 0.35))
            self.play(ReplacementTransform(arcA, arcC), run_time=1.2)
            opp2, adj2 = Line(A, B, color=FUNC, stroke_width=8), Line(B, C, color=DERIV, stroke_width=8)
            self.play(Transform(opp, opp2), Transform(adj, adj2), Transform(opp_lab, T("opposite", 32, FUNC).next_to(adj, DOWN, buff=0.2)),
                      Transform(adj_lab, T("adjacent", 32, DERIV).next_to(opp, RIGHT, buff=0.2)), run_time=1.2)
            self.play(FadeIn(T("the hypotenuse never changes", 40, ACCUM).to_edge(RIGHT, buff=0.6).shift(UP * 0.4)), run_time=0.6)
        self.clear()

        with self.beat("Same angle, same ratios") as b:
            u, A = 1.15, np.array([-6.0, -2.6, 0])
            tris = VGroup()
            for k, (a, o) in enumerate(((2, 1.4), (3, 2.1), (4, 2.8))):
                col = [FUNC, DERIV, TANGENT][k]
                tris.add(VGroup(Polygon(A, A + RIGHT * a * u, A + RIGHT * a * u + UP * o * u, stroke_color=col, stroke_width=4),
                                M(f"{o}", 26, col).next_to(A + RIGHT * a * u + UP * o * u / 2, RIGHT, buff=0.08)))
            ang = VGroup(Arc(radius=0.7, angle=np.radians(35), arc_center=A, color=SECANT, stroke_width=4), M(r"35^\circ", 26, SECANT).move_to(A + RIGHT * 1.05 + UP * 0.3))
            self.play(FadeIn(ang), LaggedStart(*[Create(t[0]) for t in tris], lag_ratio=0.4), run_time=1.6)
            self.play(FadeIn(VGroup(*[t[1] for t in tris])), FadeIn(VGroup(*[M(str(a), 26, c).next_to(A + RIGHT * a * u, DOWN, buff=0.12)
                                                                                for a, c in ((2, FUNC), (3, DERIV), (4, TANGENT))])), run_time=0.8)
            b.line(1)
            tab = table(["\\text{adjacent}", "\\text{opposite}", "\\frac{\\text{opposite}}{\\text{adjacent}}"],
                        [["2", "1.4", r"\phantom{0.7}"], ["3", "2.1", r"\phantom{0.7}"], ["4", "2.8", r"\phantom{0.7}"]], size=32, gap=0.3).to_edge(RIGHT, buff=0.6).shift(UP * 1.2)
            self.play(FadeIn(tab), run_time=0.8)
            for r in (1, 2, 3):
                # column 2's x from its header, row r's y from its first cell (the placeholder cells are empty)
                spot = np.array([tab.cells[0][2].get_center()[0], tab.cells[r][0].get_center()[1], 0])
                self.play(FadeIn(M(r"\approx 0.7", 32, SECANT).move_to(spot)), run_time=0.5)
            b.line(2)
            self.play(FadeIn(formula_box(T("the ratio depends only on the angle", 34, ACCUM), ACCUM).next_to(tab, DOWN, buff=0.6)), run_time=0.8)
        self.clear()

        with self.beat("SOH CAH TOA") as b:
            tri = right_triangle(4.4, 2.9, opp=r"\text{opposite}", adj=r"\text{adjacent}", hyp=r"\text{hypotenuse}", angle=r"\theta", size=30).move_to(LEFT * 3.6 + DOWN * 0.4)
            self.play(Create(tri[0]), FadeIn(tri[1:]), run_time=1)
            names = VGroup(T("sine", 34, FUNC), T("cosine", 34, DERIV), T("tangent", 34, TANGENT)).arrange(RIGHT, buff=0.6).to_edge(RIGHT, buff=0.8).shift(UP * 2.6)
            self.play(FadeIn(names), run_time=0.6)
            b.line(1)
            rat = VGroup(M(r"\sin\theta = \frac{\text{opposite}}{\text{hypotenuse}}", 38, FUNC), M(r"\cos\theta = \frac{\text{adjacent}}{\text{hypotenuse}}", 38, DERIV),
                         M(r"\tan\theta = \frac{\text{opposite}}{\text{adjacent}}", 38, TANGENT)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).to_edge(RIGHT, buff=0.6).shift(UP * 0.4)
            self.play(FadeOut(names), run_time=0.3)
            for r_ in rat:
                self.play(Write(r_), run_time=0.8)
            b.line(2)
            self.play(FadeIn(formula_box(T("SOH \\ CAH \\ TOA", 48, ACCUM), ACCUM).next_to(rat, DOWN, buff=0.5)), run_time=0.8)
        self.clear()

        # the three ratios stay in the corner for every worked example from here on
        self.example_ref = (r"\begin{aligned}\sin\theta &= \tfrac{\text{opp}}{\text{hyp}}\\ \cos\theta &= \tfrac{\text{adj}}{\text{hyp}}\\"
                            r" \tan\theta &= \tfrac{\text{opp}}{\text{adj}}\end{aligned}")

        tri = right_triangle(3.6, 1.92, opp="8", adj="15", hyp="?", angle=r"\theta", size=32)
        self.example("Ratios from sides", r"A right triangle has legs $8$ and $15$. $\theta$ is the angle opposite the side of length $8$. Find $\sin\theta$, $\cos\theta$, and $\tan\theta$.",
                     [r"\text{hyp}^2 = 8^2 + 15^2 = 64 + 225 = 289", r"\text{hyp} = 17", r"\sin\theta = \frac{\text{opp}}{\text{hyp}} = \frac{8}{17}", r"\cos\theta = \frac{\text{adj}}{\text{hyp}} = \frac{15}{17}",
                      r"\tan\theta = \frac{\text{opp}}{\text{adj}} = \frac{8}{15}"], at=[1, 2, 3, 4, 5], figure=tri, follow=True)

        with self.beat("The reciprocal ratios") as b:
            cols = VGroup(*[VGroup(M(top, 38, c), M(bot, 38, c), T(name, 28, DIM)).arrange(DOWN, buff=0.3) for top, bot, name, c in
                            ((r"\sin\theta = \frac{\text{opp}}{\text{hyp}}", r"\csc\theta = \frac{\text{hyp}}{\text{opp}} = \frac{1}{\sin\theta}", "cosecant", FUNC),
                             (r"\cos\theta = \frac{\text{adj}}{\text{hyp}}", r"\sec\theta = \frac{\text{hyp}}{\text{adj}} = \frac{1}{\cos\theta}", "secant", DERIV),
                             (r"\tan\theta = \frac{\text{opp}}{\text{adj}}", r"\cot\theta = \frac{\text{adj}}{\text{opp}} = \frac{1}{\tan\theta}", "cotangent", TANGENT))]).arrange(RIGHT, buff=0.6)
            cols.set_max_width(12.8).to_edge(UP, buff=0.6)
            self.play(FadeIn(VGroup(*[c[0] for c in cols])), run_time=0.6)
            self.play(Write(cols[0][1]), FadeIn(cols[0][2]), run_time=0.8)
            b.line(1)
            for c in cols[1:]:
                self.play(Write(c[1]), FadeIn(c[2]), run_time=0.8)
            b.line(2)
            tip = formula_box(T(r"one ``co'' per pair: sine with \textbf{co}secant, \textbf{co}sine with secant", 32, ACCUM), ACCUM).next_to(cols, DOWN, buff=0.5)
            self.play(FadeIn(tip), run_time=0.8)
            b.line(3)
            small = right_triangle(2.7, 1.44, opp="8", adj="15", hyp="17", angle=r"\theta", size=28).to_edge(LEFT, buff=1.0).to_edge(DOWN, buff=0.6)
            vals = M(r"\csc\theta = \frac{17}{8}, \quad \sec\theta = \frac{17}{15}, \quad \cot\theta = \frac{15}{8}", 40).next_to(small, RIGHT, buff=1.0)
            self.play(FadeIn(small), run_time=0.6)
            self.play(Write(vals), run_time=1.2)
        self.clear()

        self.example("Finding a side", r"From $20$ m away, the angle up to the top of a tree is $35^\circ$. How tall is the tree?",
                     [r"TEXT:$h$ is opposite $35^\circ$; $20$ m is adjacent.", r"\tan 35^\circ = \frac{h}{20}", r"h = 20\tan 35^\circ", r"\approx 20(0.7002) \quad \text{(degree mode)}",
                      r"\approx 14.0 \text{ m}"], at=[1, 2, 3, 4, 5], figure=surveyor_scene(), follow=True)

        with self.beat("Working back to the angle") as b:
            fwd = M(r"\tan 35^\circ \approx 0.7002", 46, TANGENT).to_edge(UP, buff=0.7).shift(LEFT * 3)
            self.play(Write(fwd), run_time=0.8)
            b.line(1)
            back = M(r"\tan^{-1}(0.7002) \approx 35^\circ", 46, SECANT).next_to(fwd, DOWN, buff=0.7, aligned_edge=LEFT)
            arr = CurvedArrow(fwd.get_right() + RIGHT * 0.2, back.get_right() + RIGHT * 0.2, color=SECANT, angle=-PI / 2)
            self.play(Create(arr), Write(back), run_time=1.2)
            b.line(2)
            keys = VGroup(*[formula_box(M(k, 36), DIM) for k in (r"\sin^{-1}", r"\cos^{-1}", r"\tan^{-1}")]).arrange(RIGHT, buff=0.4)
            keys.add(T("ratio in, angle out", 32, DIM).next_to(keys, DOWN, buff=0.25))
            keys.next_to(back, DOWN, buff=0.7, aligned_edge=LEFT)
            self.play(FadeIn(keys), run_time=0.8)
            b.line(3)
            u = 0.08
            S = np.array([1.6, -2.6, 0])
            blg = building(1.3, 3.2).move_to(S + RIGHT * 3.6, aligned_edge=DOWN)
            top = blg.get_corner(UL) + RIGHT * 0.02
            grd = ground(5.8).move_to(S + RIGHT * 2.4, aligned_edge=UP)
            person = person_walking(height=0.95).move_to(S + LEFT * 0.1, aligned_edge=DOWN)
            eye = S + UP * 0.85
            el = np.arctan2(top[1] - eye[1], top[0] - eye[0])
            elev = VGroup(DashedLine(eye, np.array([top[0], eye[1], 0]), color=DIM), Line(eye, top, color=SECANT, stroke_width=3),
                          Arc(radius=0.8, angle=el, arc_center=eye, color=SECANT, stroke_width=4), T("elevation", 26, SECANT).next_to(eye + RIGHT * 0.9, UP, buff=0.35).shift(RIGHT * 0.5))
            self.play(FadeIn(grd), FadeIn(blg), FadeIn(person), run_time=0.8)
            self.play(Create(elev[:3]), FadeIn(elev[3]), run_time=1)
            dep = VGroup(DashedLine(top, top + LEFT * 2.2, color=DIM), Arc(radius=0.8, start_angle=PI, angle=el, arc_center=top, color=TANGENT, stroke_width=4),
                         T("depression", 26, TANGENT).next_to(top + LEFT * 1.4, UP, buff=0.12))
            self.play(Create(dep[:2]), FadeIn(dep[2]), run_time=1)
        self.clear()

        self.example("Finding an angle", r"Priya stands $50$ m from the base of a building that is $30$ m tall. Find the angle of elevation from where she stands to the top of the building.",
                     [r"TEXT:$30$ m is opposite $\theta$; $50$ m is adjacent.", r"\tan\theta = \frac{30}{50} = 0.6", r"\theta = \tan^{-1}(0.6)", r"\approx 31.0^\circ"],
                     at=[1, 2, 3, 4], figure=rooftop_scene(), follow=True)

        with self.beat("Close") as b:
            card = VGroup(M(r"\sin\theta = \frac{\text{opp}}{\text{hyp}}, \quad \cos\theta = \frac{\text{adj}}{\text{hyp}}, \quad \tan\theta = \frac{\text{opp}}{\text{adj}}", 42, ACCUM),
                          M(r"\csc\theta = \frac{\text{hyp}}{\text{opp}}, \quad \sec\theta = \frac{\text{hyp}}{\text{adj}}, \quad \cot\theta = \frac{\text{adj}}{\text{opp}}", 40),
                          T("Find a side: the ratio that links the side you know to the side you want.", 32),
                          T(r"Find an angle: an inverse key on the ratio ($\sin^{-1}$, $\cos^{-1}$, $\tan^{-1}$).", 32)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: The ladder", r"Marisol leans a $6$ m ladder against a wall. It makes a $70^\circ$ angle with the ground. How high up the wall does it reach?",
                     [r"TEXT:The ladder is the hypotenuse; $h$ is opposite $70^\circ$.", r"\sin 70^\circ = \frac{h}{6}", r"h = 6\sin 70^\circ", r"\approx 6(0.9397)", r"\approx 5.64 \text{ m}"],
                     at=[1, 2, 2, 3, 4], figure=ladder_scene())
        self.example("Example 2: The kite string", r"Jordan's kite is $30$ m above the ground. They hold the string at ground level, and it makes a $40^\circ$ angle with the ground. How long is the string?",
                     [r"\sin 40^\circ = \frac{30}{L}", r"L\sin 40^\circ = 30", r"L = \frac{30}{\sin 40^\circ}", r"\approx \frac{30}{0.6428}", r"\approx 46.7 \text{ m}",
                      r"TEXT:Longer than $30$ m, as a hypotenuse must be."], at=[1, 2, 3, 4, 4, 5], figure=kite_scene(), follow=True)
        self.example("Example 3: A skateboard ramp", r"Deshawn builds a skateboard ramp. Its sloped surface is $4$ m long, and its high end is $1.2$ m off the ground. What angle does the ramp make with the ground?",
                     [r"TEXT:$1.2$ m is opposite $\theta$; $4$ m is the hypotenuse.", r"\sin\theta = \frac{1.2}{4} = 0.3", r"\theta = \sin^{-1}(0.3)", r"\approx 17.5^\circ"],
                     at=[1, 2, 3, 4], figure=ramp_scene())
        tri4 = right_triangle(12 * np.cos(np.radians(25)) * 0.42, 12 * np.sin(np.radians(25)) * 0.42, opp="a", adj="b", hyp="12", angle=r"25^\circ", size=32)
        self.example("Example 4: Solving a whole triangle", r"A right triangle has hypotenuse $12$ and an acute angle of $25^\circ$. Find the other acute angle and the lengths of both legs.",
                     [r"90^\circ - 25^\circ = 65^\circ", r"\sin 25^\circ = \frac{a}{12}, \text{ so } a = 12\sin 25^\circ \approx 5.07", r"\cos 25^\circ = \frac{b}{12}, \text{ so } b = 12\cos 25^\circ \approx 10.88",
                      r"\text{check: } 5.07^2 + 10.88^2 \approx 144 = 12^2"], at=[1, 2, 3, 4], figure=tri4)
        self.finish()
