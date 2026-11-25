"""Model in Motion · The Logistic Fixed-Effect Model · Episode 8: The Arrow Matrix (how thousands of sliders step at once).

ANIMATIC PASS. Every narration clip has its board. The compositions are meant to stay; most of the motion is still to come.

Render one scene:   manim -ql --media_dir build/media episode/episode08.py S05_Fold      (run from the episode folder)
Every scene reads audio/manifest.json; each `with self.nar("sX_Y") as seg:` block starts that voiceover clip and
holds the scene until the clip (plus a short gap) has finished.
The table, the fold, the joint path and the test fit come from e08_numbers.json, written by e08_numbers.py. The map
of the cold open is Episode 7's. The machine's readings are computed live by mim.meters.FitMachine.
All content stays above y = -3.0, clear of the captions.
"""
from __future__ import annotations

import sys
from pathlib import Path

import os  # noqa: E402

os.environ["MIM_EPISODE"] = str(Path(__file__).resolve().parents[1])   # this episode's folder
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))           # the repository root, for the shared mim package
from mim.common import *  # noqa: E402,F403
from mim.kit import *  # noqa: E402,F403
from mim.lines import *  # noqa: E402,F403
from mim.boards import *  # noqa: E402,F403
from mim.meters import *  # noqa: E402,F403

N = json.loads((ROOT / "e08_numbers.json").read_text())
E7 = json.loads((ROOT.parent / "e07_climbing_the_hill" / "e07_numbers.json").read_text())
TB, SC, FO, FIRST, JOINT, TURNS, COST = N["table"], N["scale"], N["fold"], N["first"], N["joint"], N["turns"], N["cost"]
BETA, G, G0V = N["fit"]["beta"], N["fit"]["gamma"], N["start_gamma"]
MAP = E7["map"]
COL = {n: CLINICS[n]["color"] for n in ORDER}
CAP = [-2.4, -2.72, 0]
RX = 4.6


def minus(v, places=2):
    return f"{v:.{places}f}".replace("-", "\u2212")


def box_around(m, color=PAPER):
    return SurroundingRectangle(m, color=color, buff=0.08, stroke_width=2.5, corner_radius=0.06).set_z_index(7)


def the_map(x0=-5.6, x1=1.2, y0=-2.1, y1=2.4):
    """Episode 7's map: the dial against Birch's slider, the other clinics levelled. Returns (MX, MY, group)."""
    (b0, b1), (g0, g1) = MAP["beta_range"], MAP["gamma_range"]
    MX = lambda bv: x0 + (x1 - x0) * (bv - b0) / (b1 - b0)
    MY = lambda gv: y0 + (y1 - y0) * (gv - g0) / (g1 - g0)
    axes = VGroup(Line([x0, y0, 0], [x1, y0, 0], stroke_width=3, color=MUTED), Line([x0, y0, 0], [x0, y1, 0], stroke_width=3, color=MUTED))
    xl = side("the dial", size=18).move_to([(x0 + x1) / 2, y0 - 0.35, 0])
    yl = side("Birch's slider", size=18).move_to([x0 + 0.55, y1 + 0.28, 0])
    rings = VGroup()
    for k, c in enumerate(sorted(MAP["contours"], key=lambda c: -c["below_top"])):
        line = VMobject(color=MUTED, stroke_width=1.6 + 0.25 * k).set_points_as_corners([np.array([MX(a), MY(b), 0.0]) for a, b in c["points"]])
        rings.add(line.set_stroke(opacity=0.45 + 0.08 * k))
    top = Dot([MX(BETA), MY(G["Birch"]), 0], radius=0.1, color=ACCENT).set_z_index(5)
    return MX, MY, VGroup(axes, xl, yl, rings, top)


class ArrowTable:
    """The table of who disturbs whom. Rows are the six meters, columns the six controls: five clinics, then the dial."""

    def __init__(self, cx=-2.4, cy=-0.45, cell=0.74):
        self.cell, n = cell, 6
        x0, y0 = cx - cell * (n - 1) / 2, cy + cell * (n - 1) / 2
        self.pos = lambda i, k: np.array([x0 + k * cell, y0 - i * cell, 0.0])
        self.grid = VGroup(*[Square(side_length=cell * 0.94, stroke_color=FAINT, stroke_width=1.5).move_to(self.pos(i, k)) for i in range(n) for k in range(n)])
        cols, rows = VGroup(), VGroup()
        for k, nm in enumerate(ORDER + ["dial"]):
            top = tex(r"\beta", 28, ACCENT) if nm == "dial" else txt(nm[0], 20, COL[nm], weight=SEMIBOLD)
            cols.add(top.move_to(self.pos(0, k) + UP * cell * 0.82))
            left = tex(r"\beta", 28, ACCENT) if nm == "dial" else txt(nm, 18, COL[nm], weight=SEMIBOLD)
            rows.add(left.next_to(self.pos(k, 0) + LEFT * cell * 0.5, LEFT, buff=0.18))
        self.heads = VGroup(cols, rows, side("the six controls", size=15).move_to([cx, y0 + cell * 1.42, 0]),
                            side("the six meters", size=15).rotate(PI / 2).move_to([x0 - cell * 0.5 - 1.35, cy, 0]))
        d, b, c = TB["diag"], TB["border"], TB["corner"]
        self.cells = {}
        for i, nm in enumerate(ORDER):
            self.cells[(i, i)] = self._cell(i, i, d[i], COL[nm])
            self.cells[(i, 5)] = self._cell(i, 5, b[i], ACCENT)
            self.cells[(5, i)] = self._cell(5, i, b[i], ACCENT)
        self.cells[(5, 5)] = self._cell(5, 5, c, ACCENT)
        self.zeros = VGroup(*[Dot(self.pos(i, k), radius=0.03, color=MUTED) for i in range(5) for k in range(5) if i != k])
        shape = [(i, i) for i in range(6)] + [(i, 5) for i in range(5)] + [(5, i) for i in range(5)]
        self.outline = VGroup(*[Square(side_length=cell * 0.94, stroke_color=ACCENT, stroke_width=3).move_to(self.pos(i, k)) for i, k in shape]).set_z_index(6)

    def _cell(self, i, k, v, color):
        sq = Square(side_length=self.cell * 0.94, stroke_width=0, fill_color=color, fill_opacity=0.12 + 0.03 * v).move_to(self.pos(i, k))
        return VGroup(sq, txt(f"{v:.2f}", 16, PAPER, weight=MEDIUM).move_to(self.pos(i, k)))

    def diagonal(self):
        return [self.cells[(i, i)] for i in range(5)]

    def edges(self, i):
        return VGroup(self.cells[(i, 5)], self.cells[(5, i)])

    def everything(self):
        return VGroup(self.grid, self.heads, *self.cells.values(), self.zeros)


def arrow_sketch(size, cx, cy):
    """A large table drawn as its shape only: a diagonal, two thin edges and a corner."""
    sq = Square(side_length=size, stroke_color=MUTED, stroke_width=2).move_to([cx, cy, 0])
    return VGroup(sq, Line(sq.get_corner(UL), sq.get_corner(DR), stroke_width=3, color=PAPER),
                  Line(sq.get_corner(UR) + LEFT * 0.05, sq.get_corner(DR) + LEFT * 0.05, stroke_width=5, color=ACCENT),
                  Line(sq.get_corner(DL) + UP * 0.05, sq.get_corner(DR) + UP * 0.05, stroke_width=5, color=ACCENT))


# =================================================================================== S01
class S01_ColdOpen(EpisodeScene):
    def construct(self):
        MX, MY, board = the_map()
        stair = VMobject(color=PAPER, stroke_width=3.5).set_points_as_corners([np.array([MX(a), MY(b), 0.0]) for a, b in MAP["stair"]]).set_z_index(4)
        straight = VMobject(color=ACCENT, stroke_width=4.5).set_points_as_corners([np.array([MX(a), MY(b), 0.0]) for a, b in E7["joint"]["path"]]).set_z_index(5)
        t1 = VGroup(side("taking turns", color=PAPER), big(f"{TURNS['plain']} rounds", size=30)).arrange(DOWN, buff=0.1).move_to([RX, 1.2, 0])
        t2 = VGroup(side("stepping together", color=PAPER), big(f"{JOINT['steps']} steps", size=30, color=ACCENT)).arrange(DOWN, buff=0.1).move_to([RX, -0.4, 0])
        with self.nar("s1_1") as seg:
            self.play(FadeIn(board), run_time=1.0)
            self.play(Create(stair), FadeIn(t1), run_time=1.8, rate_func=linear)
            seg.wait_until(seg.s(1))
            self.play(Create(straight), FadeIn(t2), run_time=1.4)

        M = FitMachine({n: G0V for n in ORDER}, 0.0)
        with self.nar("s1_2") as seg:
            self.play(FadeOut(VGroup(board, stair, straight, t1, t2)), run_time=0.6)
            self.play(FadeIn(M.all), run_time=0.9)
            seg.wait_until(seg.s(1))
            bx = box_around(VGroup(M.bmeter, M.bdiff))
            self.play(M.g["Dune"].animate.set_value(float(logit(events("Dune") / size("Dune")))), Create(bx), run_time=2.2)   # Dune alone levels at its own rate

        small = VGroup(*[Square(side_length=0.26, stroke_color=MUTED, stroke_width=1.5) for _ in range(36)]).arrange_in_grid(rows=6, cols=6, buff=0.04).move_to([-4.3, 0.3, 0])
        small_l = VGroup(big("5 clinics", size=26), side(f"{SC['cast'][0]} cells", color=PAPER)).arrange(DOWN, buff=0.1).next_to(small, DOWN, buff=0.35)
        huge = Square(side_length=4.2, stroke_color=MUTED, stroke_width=2, fill_color=INK_2, fill_opacity=1).move_to([1.6, 0.25, 0])
        huge_l = VGroup(big("7,000 providers", size=26), side(f"{SC['national'][0]:,} cells", color=PAPER)).arrange(DOWN, buff=0.1).move_to(huge)
        ask = big("How can this be fast?", size=30, color=ACCENT).move_to([RX + 0.4, -2.3, 0])
        with self.nar("s1_3", gap=0.8) as seg:
            M.clear()
            self.play(*clear(self), run_time=0.6)
            self.play(FadeIn(small), FadeIn(small_l), run_time=0.8)
            seg.wait_until(seg.word(0, "For seven thousand"))
            self.play(GrowFromCenter(huge), FadeIn(huge_l), run_time=1.2)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(ask), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S02
class S02_Title(EpisodeScene):
    def construct(self):
        title_card(self, "s2_1", 8, "The Arrow Matrix", "how thousands of sliders step at once")


# =================================================================================== S03
class S03_Table(EpisodeScene):
    def construct(self):
        tag = chapter_tag(1, "Who disturbs whom")
        T = ArrowTable()
        what = VGroup(side("each cell:", size=18), side("how much that meter moves", size=18, color=PAPER), side("when that control does", size=18, color=PAPER)).arrange(DOWN, buff=0.1).move_to([RX, 1.6, 0])
        info = side("statisticians call this table the information matrix", size=14).move_to([-2.4, -2.85, 0])
        with self.nar("s3_1") as seg:
            self.play(FadeIn(tag), FadeIn(T.grid), FadeIn(T.heads), FadeIn(info), run_time=1.2)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(what), run_time=0.8)

        d_l = VGroup(side("the diagonal:", size=18), side("each clinic's own wobble", size=18, color=PAPER)).arrange(DOWN, buff=0.1).move_to([RX, 0.45, 0])
        c_l = VGroup(side("the corner:", size=18), side("the dial's own", size=18, color=PAPER)).arrange(DOWN, buff=0.1).move_to([RX, -0.5, 0])
        with self.nar("s3_2") as seg:
            self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in T.diagonal()], lag_ratio=0.25), FadeIn(d_l), run_time=2.0)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(T.cells[(5, 5)], scale=0.8), FadeIn(c_l), run_time=0.9)

        e_l = VGroup(side("the two edges:", size=18), side("each clinic's tie to the dial", size=18, color=PAPER)).arrange(DOWN, buff=0.1).move_to([RX, -1.45, 0])
        elm_n = side(f"Elm's {TB['diag'][4]:.2f} is where its slider stopped, at {minus(TB['elm_gamma'])}", size=14).move_to([RX, -2.4, 0])
        with self.nar("s3_3") as seg:
            self.play(LaggedStart(*[FadeIn(T.edges(i), scale=0.8) for i in range(5)], lag_ratio=0.2), FadeIn(e_l), run_time=1.8)
            seg.wait_until(seg.word(1, "Birch"))
            bx = VGroup(*[box_around(c) for c in T.edges(1)])
            self.play(Create(bx), run_time=0.6)
            seg.wait_until(seg.word(1, "Elm"))
            bx2 = VGroup(*[box_around(c, ELM) for c in T.edges(4)])
            self.play(FadeOut(bx), Create(bx2), FadeIn(elm_n), run_time=0.6)

        pick = box_around(Square(side_length=T.cell * 0.94).move_to(T.pos(1, 0)))
        why = VGroup(side("Alder's slider, Birch's meter:", size=17, color=PAPER), side("no patient belongs to both", size=17, color=PAPER)).arrange(DOWN, buff=0.08).move_to([RX, 0.45, 0])
        exact = big("not an approximation", size=24, color=ACCENT).move_to([RX, -0.55, 0])
        with self.nar("s3_4", gap=0.8) as seg:
            self.play(FadeOut(VGroup(bx2, what, d_l, c_l, e_l)), FadeIn(T.zeros), run_time=0.8)
            seg.wait_until(seg.word(0, "Alder's slider"))
            self.play(Create(pick), FadeIn(why), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(exact, shift=UP * 0.1), run_time=0.7)
            seg.wait_until(seg.s(2))
            self.play(FadeOut(pick), LaggedStart(*[Create(m) for m in T.outline], lag_ratio=0.06), run_time=1.6)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S04
class S04_Scale(EpisodeScene):
    def construct(self):
        tag = chapter_tag(2, "Why the shape matters")
        a = arrow_sketch(2.3, -4.3, 0.4)
        a_l = VGroup(side("200 providers, 2 risk factors", size=17, color=PAPER), big(f"{SC['crowd'][0]:,} cells", size=26),
                     big(f"{SC['crowd'][1]:,} not zero", size=22, color=ACCENT)).arrange(DOWN, buff=0.1).next_to(a, DOWN, buff=0.3)
        b = arrow_sketch(3.9, 1.6, 0.55)
        share = 100 * SC["national"][1] / SC["national"][0]
        b_l = VGroup(side("7,000 providers, 50 risk factors", size=17, color=PAPER), big(f"{SC['national'][0]:,} cells", size=26),
                     big(f"{share:.1f}% not zero", size=22, color=ACCENT)).arrange(DOWN, buff=0.1).move_to([5.3, 0.55, 0])
        b_l = fit_width(b_l, 3.2).move_to([5.45, 0.55, 0])
        easy = side("as an ordinary table: stuck.  as an arrow: easy.", size=22, color=PAPER).move_to([0.6, -2.5, 0])
        with self.nar("s4_1") as seg:
            self.play(FadeIn(tag), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(a), FadeIn(a_l[0]), FadeIn(a_l[1]), run_time=1.2)
            seg.wait_until(seg.word(1, "Only"))
            self.play(FadeIn(a_l[2]), run_time=0.7)

        with self.nar("s4_2", gap=0.8) as seg:
            self.play(FadeIn(b), FadeIn(b_l[0]), FadeIn(b_l[1]), run_time=1.3)
            seg.wait_until(seg.word(0, "Nearly all"))
            self.play(FadeIn(b_l[2]), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(easy), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S05
class S05_Fold(EpisodeScene):
    def construct(self):
        tag = chapter_tag(3, "Folding the arrow")
        T = ArrowTable()
        d, b = TB["diag"], TB["border"]
        self.play(FadeIn(tag), FadeIn(T.everything()), run_time=1.0)
        trio = lambda i: VGroup(T.cells[(i, i)], T.cells[(i, 5)], T.cells[(5, i)])
        boxes = [VGroup(*[box_around(c, COL[ORDER[i]]) for c in trio(i)]) for i in range(5)]
        recipe = VGroup(side("for one clinic:", size=18), side("square its tie to the dial,", size=18, color=PAPER), side("divide by its own wobble,", size=18, color=PAPER),
                        side("take that from the corner", size=18, color=PAPER)).arrange(DOWN, buff=0.1).move_to([RX, 1.35, 0])
        worked = MathTex(rf"{b[0]:.2f}^2 \div {d[0]:.2f}", "=", f"{FO['terms'][0]:.2f}", font_size=34, color=PAPER).move_to([RX, 0.0, 0])
        worked[2].set_color(ALDER)
        with self.nar("s5_1") as seg:
            seg.wait_until(seg.s(1))
            self.play(Create(boxes[0]), FadeIn(recipe), run_time=1.0)
            seg.wait_until(seg.word(1, "take that away") - 0.4)
            self.play(Write(worked), run_time=1.0)

        corner_num = T.cells[(5, 5)][1]
        took = VGroup()
        with self.nar("s5_2") as seg:
            for i, cue in enumerate(("Alder takes", "Birch,", "Cedar,", "Dune,", "Elm,")):
                seg.wait_until(seg.word(0, cue))
                row = VGroup(txt(ORDER[i], 18, COL[ORDER[i]], weight=SEMIBOLD), txt(f"\u2212 {FO['terms'][i]:.2f}", 20, PAPER)).arrange(RIGHT, buff=0.3)
                row.move_to([RX - 0.2, -0.75 - 0.36 * i, 0])
                took.add(row)
                new_num = txt(f"{FO['running'][i]:.2f}", 16, PAPER, weight=MEDIUM).move_to(T.pos(5, 5))
                anims = [FadeIn(row, shift=LEFT * 0.1), Transform(corner_num, new_num)]
                if i:
                    anims += [FadeOut(boxes[i - 1]), Create(boxes[i])]
                self.play(*anims, run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(FadeOut(boxes[4]), Indicate(T.cells[(5, 5)], color=ACCENT, scale_factor=1.25), run_time=1.0)

        dimmed = VGroup(*[T.cells[k] for k in T.cells if k != (5, 5)], T.zeros)
        s_big = VGroup(big(f"{FO['S']:.2f}", size=44, color=ACCENT), side("one number, for the dial alone", size=18, color=PAPER)).arrange(DOWN, buff=0.12).move_to([RX, 0.9, 0])
        with self.nar("s5_3") as seg:
            self.play(FadeOut(VGroup(recipe, worked, took)), dimmed.animate.set_opacity(0.18), run_time=0.9)
            self.play(FadeIn(s_big, shift=UP * 0.1), run_time=0.8)

        U, x0 = 1.35, 2.55
        segs, labels, x = VGroup(), VGroup(), x0
        for i, n in enumerate(ORDER):
            v = FO["within"][i]
            if v > 1e-9:
                r = Rectangle(width=U * v, height=0.34, stroke_color=INK, stroke_width=1.5, fill_color=COL[n], fill_opacity=1).move_to([x + U * v / 2, -0.55, 0])
                segs.add(r)
                labels.add(VGroup(txt(n, 14, COL[n], weight=SEMIBOLD), txt(f"{v:.2f}", 15, PAPER)).arrange(DOWN, buff=0.04).next_to(r, DOWN, buff=0.1))
                x += U * v
        elm_piece = VGroup(txt("Elm", 14, ELM, weight=SEMIBOLD), txt("0", 15, PAPER)).arrange(DOWN, buff=0.04).move_to([x + 0.3, -1.03, 0])
        mean = VGroup(side("how much patients differ in risk", size=17, color=PAPER), side("from others in their own clinic", size=17, color=PAPER)).arrange(DOWN, buff=0.08).move_to([RX, -1.85, 0])
        with self.nar("s5_4") as seg:
            self.play(LaggedStart(*[GrowFromEdge(r, LEFT) for r in segs], lag_ratio=0.3), FadeIn(labels), run_time=1.8)
            self.play(FadeIn(mean), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(elm_piece), run_time=0.7)

        BU, bx0 = 0.33, 2.5                                 # bar length per unit; left edge of both bars
        def bar_row(label, value, color, y):
            r = Rectangle(width=BU * value, height=0.3, stroke_width=0, fill_color=color, fill_opacity=1).move_to([bx0 + BU * value / 2, y, 0])
            return VGroup(side(label, size=17, color=PAPER).move_to([bx0, y + 0.38, 0], aligned_edge=LEFT), r, txt(f"{value:.2f}", 20, color, weight=SEMIBOLD).next_to(r, RIGHT, buff=0.15))

        bars = VGroup(bar_row("ignoring the clinics", TB["corner"], MUTED, -0.35), bar_row("after folding", FO["S"], ACCENT, -1.3))
        times = big(f"{FO['overstate']:.1f} times too much", size=26, color=ALERT).move_to([RX, -2.1, 0])
        with self.nar("s5_5", gap=0.8) as seg:
            self.play(FadeOut(VGroup(segs, labels, elm_piece, mean)), run_time=0.6)
            self.play(FadeIn(bars), run_time=0.9)
            seg.wait_until(seg.word(0, "three and a half"))
            self.play(FadeIn(times, shift=UP * 0.1), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S06
class S06_Step(EpisodeScene):
    def construct(self):
        tag = chapter_tag(4, "One step, together")
        M = FitMachine({n: G0V for n in ORDER}, 0.0)
        path = JOINT["path"]
        division = MathTex(rf"{FIRST['corrected_tilt']:.2f} \div {FIRST['S']:.2f}", "=", f"{FIRST['dial_step']:.2f}", font_size=34, color=PAPER)
        division[2].set_color(ACCENT)
        first = VGroup(side("the dial's first step:", color=PAPER), division).arrange(RIGHT, buff=0.35).move_to(CAP)
        rd = Integer(0, font_size=34, color=ACCENT)
        counter = VGroup(side("joint step", color=PAPER), rd).arrange(RIGHT, buff=0.25).move_to(CAP)

        def step(k, rt):
            self.play(M.b.animate.set_value(path[k]["beta"]), *[M.g[n].animate.set_value(path[k]["gamma"][i]) for i, n in enumerate(ORDER)], run_time=rt)
            rd.set_value(k)

        self.play(FadeIn(tag), FadeIn(M.all), run_time=1.0)
        with self.nar("s6_1") as seg:
            seg.wait_until(seg.word(0, "From the plain guess"))
            self.play(FadeIn(first), run_time=0.9)

        with self.nar("s6_2") as seg:
            self.play(FadeOut(first), FadeIn(counter), run_time=0.5)
            seg.wait_until(seg.word(0, "One joint step"))
            step(1, 1.4)
            seg.wait_until(seg.word(0, "A second"))
            step(2, 1.0)
            seg.wait_until(seg.word(0, "A third"))
            step(3, 0.9)
            seg.wait_until(seg.s(1))
            step(4, 0.6)
            step(5, 0.6)
            versus = VGroup(side("taking turns:", color=PAPER), big(f"{TURNS['plain']} rounds", size=26, color=MUTED)).arrange(RIGHT, buff=0.25).next_to(counter, RIGHT, buff=0.9)
            self.play(FadeIn(versus), run_time=0.7)

        same = side("recorded as 0 and 1, as 5 and 6, or as 50 and 51: the same five steps", size=19, color=PAPER).move_to([-1.6, -2.72, 0])
        with self.nar("s6_3", gap=0.8) as seg:
            self.play(FadeOut(VGroup(counter, versus)), run_time=0.5)
            seg.wait_until(seg.word(0, "Record the risk factor"))
            self.play(FadeIn(same), run_time=0.9)
        M.clear()
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S07
class S07_Cost(EpisodeScene):
    def construct(self):
        tag = chapter_tag(5, "What it buys")
        jobs = VGroup(*[pill(s, 20) for s in ("add up over the patients", "fold once for each provider", "solve one small system")]).arrange(RIGHT, buff=0.55).move_to([0, 2.0, 0])
        arrows = VGroup(*[Arrow(jobs[k].get_right(), jobs[k + 1].get_left(), buff=0.1, stroke_width=3, color=MUTED, max_tip_length_to_length_ratio=0.3) for k in range(2)])
        test = VGroup(big(f"{COST['providers']:,} providers", size=28), big(f"{COST['patients']:,} patients", size=28),
                      VGroup(big("well under a second", size=28, color=GOOD), side(f"({COST['seconds']:.2f} s in this run)", size=16)).arrange(RIGHT, buff=0.3)).arrange(DOWN, buff=0.18).move_to([-3.2, 0.1, 0])
        wide = Rectangle(width=5.2, height=1.1, stroke_color=MUTED, stroke_width=2, fill_color=INK_2, fill_opacity=1).move_to([3.4, 0.35, 0])
        wide_l = VGroup(side("the same data as an ordinary table", size=16, color=PAPER), side(f"{COST['patients']:,} rows \u00d7 {COST['providers'] + 2:,} columns", size=16)).arrange(DOWN, buff=0.06).move_to(wide)
        gb = big(f"{COST['dense_gb']:.1f} gigabytes", size=30, color=ALERT).next_to(wide, DOWN, buff=0.25)
        with self.nar("s7_1") as seg:
            self.play(FadeIn(tag), LaggedStart(FadeIn(jobs[0]), GrowArrow(arrows[0]), FadeIn(jobs[1]), GrowArrow(arrows[1]), FadeIn(jobs[2]), lag_ratio=0.5), run_time=3.4)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(test[0]), FadeIn(test[1]), run_time=0.9)
            seg.wait_until(seg.word(1, "The fit took"))
            self.play(FadeIn(test[2], shift=UP * 0.1), run_time=0.8)

        with self.nar("s7_2") as seg:
            self.play(FadeIn(wide), FadeIn(wide_l), run_time=1.0)
            seg.wait_until(seg.word(0, "would fill"))
            self.play(FadeIn(gb, shift=UP * 0.1), run_time=0.8)

        not_p = big("many providers: not a computing problem", size=28, color=PAPER).move_to([0, -1.55, 0])
        one = side("the arrow's one condition: every patient in exactly one provider", size=20, color=ACCENT).move_to([0, -2.35, 0])
        with self.nar("s7_3", gap=0.8) as seg:
            self.play(FadeIn(not_p, shift=UP * 0.1), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(one), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S08
class S08_Recap(EpisodeScene):
    def construct(self):
        tag = chapter_tag(6, "Recap")
        xs = (-4.45, 0.0, 4.45)
        cards = VGroup(*[card(4.05, 3.7).move_to([x, 0.15, 0]) for x in xs])
        icon1 = arrow_sketch(1.2, 0, 0)
        corner = Square(side_length=0.5, stroke_width=0, fill_color=ACCENT, fill_opacity=0.9).move_to([0.45, -0.35, 0])
        icon2 = VGroup(corner, *[Arrow(p, corner.get_center() + (np.array(p) - corner.get_center()) * 0.38, buff=0, stroke_width=3, color=PAPER, max_tip_length_to_length_ratio=0.3)
                                 for p in ([-0.7, 0.5, 0], [-0.75, -0.1, 0], [-0.15, 0.6, 0])])
        icon3 = VGroup(tex("=", 54, PAPER), tick_mark(s=1.3)).arrange(RIGHT, buff=0.35)
        icons = [icon1, icon2, icon3]
        caps = [["Clinics disturb each other", "only through the dial:", "the table is an arrow"], ["Fold each clinic into the corner:", "one small system is left"],
                ["Nothing is approximated:", "last episode's step,", "for everything at once"]]
        captions = VGroup()
        for k, (ic, cp) in enumerate(zip(icons, caps)):
            ic.move_to([xs[k], 0.85, 0])
            captions.add(VGroup(*[txt(s, 19, PAPER) for s in cp]).arrange(DOWN, buff=0.1).move_to([xs[k], -0.85, 0]))
        with self.nar("s8_1") as seg:
            self.play(FadeIn(tag), run_time=0.8)
            for k in range(3):
                seg.wait_until(seg.s(k + 1) - 0.1)
                self.play(FadeIn(cards[k], shift=UP * 0.15), FadeIn(captions[k], shift=UP * 0.1), FadeIn(icons[k], shift=UP * 0.1), run_time=1.1)

        s_big = VGroup(big(f"{FO['S']:.2f}", size=72, color=ACCENT), side("how firmly the data hold the dial in place", size=22, color=PAPER)).arrange(DOWN, buff=0.25).move_to([-1.8, 0.2, 0])
        nxt = VGroup(txt("Next:", 26, MUTED), big("how sure are we?", size=34)).arrange(DOWN, buff=0.2).move_to([RX, 0.2, 0])
        with self.nar("s8_2") as seg:
            self.play(FadeOut(VGroup(cards, captions, *icons)), run_time=0.7)
            self.play(FadeIn(s_big, scale=0.9), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(nxt, shift=UP * 0.15), run_time=0.9)
        end_card(self, "s8_3", 9, "How sure are we?")
