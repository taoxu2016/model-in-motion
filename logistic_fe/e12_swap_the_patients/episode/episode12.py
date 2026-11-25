"""Model in Motion · The Logistic Fixed-Effect Model · Episode 12: Swap the Patients (one clinic's curve, everyone's patients).

ANIMATIC PASS. Every narration clip has its board. The compositions are meant to stay; most of the motion is still to come.

Render one scene:   manim -ql --media_dir build/media episode/episode12.py S03_Puzzle      (run from the episode folder)
Every scene reads audio/manifest.json; each `with self.nar("sX_Y") as seg:` block starts that voiceover clip and
holds the scene until the clip (plus a short gap) has finished.
Every number comes from e12_numbers.json, written by e12_numbers.py; none is typed here. Two figures from earlier
episodes (Elm's two direct rates, Alder's expected count at the reference) are read from those episodes' number files.
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

N = json.loads((ROOT / "e12_numbers.json").read_text())
E10 = json.loads((ROOT.parent / "e10_no_events_no_peak" / "e10_numbers.json").read_text())
E11 = json.loads((ROOT.parent / "e11_swap_the_curve" / "e11_numbers.json").read_text())
OWN, REF_P, MULT, CASTD, EVERY, IND, DIR, CROWD = N["own"], N["reference"]["p"], N["multiple"], N["cast"], N["everyone"], N["indirect"], N["direct"], N["crowd"]
REF, BETA, G = N["reference"]["gamma"], N["fit"]["beta"], N["fit"]["gamma"]
COL = {n: CLINICS[n]["color"] for n in ORDER}
SX = 4.3                                            # centre of the side column beside the probability panel


def pct(p, places=0):
    return f"{100 * p:.{places}f}%"


def box_around(m, color=PAPER):
    return SurroundingRectangle(m, color=color, buff=0.1, stroke_width=2.5, corner_radius=0.06).set_z_index(7)


def mini_curve(color, shift=0.0, w=1.7, h=1.0):
    return ParametricFunction(lambda t: np.array([w * t, h * (1.0 / (1.0 + np.exp(-6.0 * (t - shift))) - 0.5), 0.0]), t_range=[-0.5, 0.5, 0.02], color=color, stroke_width=4)


def picture(curve_color, dot_colors, x, y, w=3.5, h=2.0):
    """A small picture of one measure: a curve, and the patients it is applied to."""
    c = card(w, h).move_to([x, y, 0])
    return VGroup(c, mini_curve(curve_color).move_to(c.get_center() + UP * 0.3), VGroup(*[Dot(radius=0.09, color=col) for col in dot_colors]).arrange(RIGHT, buff=0.1).move_to(c.get_center() + DOWN * 0.6))


MIXED = [ALDER, BIRCH, CEDAR, DUNE, ELM, BIRCH, ALDER]


# =================================================================================== S01
class S01_ColdOpen(EpisodeScene):
    def construct(self):
        AX = lambda r: -2.6 + 3.2 * r
        y_ax, ys = -0.9, {"Alder": 0.9, "Dune": 0.0}
        axis = VGroup(Line([AX(0), y_ax, 0], [AX(2.0), y_ax, 0], stroke_width=3, color=MUTED),
                      *[VGroup(Line([AX(v), y_ax, 0], [AX(v), y_ax - 0.1, 0], stroke_width=2, color=MUTED), txt(f"{v:g}", 16, MUTED).move_to([AX(v), y_ax - 0.3, 0])) for v in (0, 0.5, 1, 1.5, 2)],
                      side("last time: observed, over expected at the reference", size=16).move_to([AX(1.0), y_ax - 0.66, 0]))
        one = VGroup(DashedLine([AX(1), y_ax, 0], [AX(1), 1.5, 0], dash_length=0.1, stroke_width=2.5, color=CEDAR), txt("the reference", 16, CEDAR, weight=SEMIBOLD).move_to([AX(1), 1.75, 0]))
        rows = {n: VGroup(txt(n, 24, COL[n], weight=SEMIBOLD).move_to([-5.6, ys[n], 0], aligned_edge=LEFT), Line([AX(1), ys[n], 0], [AX(IND[n]), ys[n], 0], stroke_width=4, color=COL[n]).set_stroke(opacity=0.7),
                          Dot([AX(IND[n]), ys[n], 0], radius=0.15, color=COL[n]).set_z_index(5), big(f"{IND[n]:.2f}", size=30, color=COL[n]).move_to([AX(2.0) + 0.9, ys[n], 0])) for n in ("Alder", "Dune")}
        worse = side("so Alder looks the worse of the two", size=20, color=PAPER).move_to([0.4, -2.35, 0])
        with self.nar("s1_1") as seg:
            self.play(FadeIn(axis), FadeIn(one), FadeIn(rows["Alder"]), run_time=1.2)
            seg.wait_until(seg.word(0, "and Dune's at"))
            self.play(FadeIn(rows["Dune"]), run_time=0.7)
            seg.wait_until(seg.word(0, "So Alder looks"))
            self.play(FadeIn(worse), run_time=0.7)

        C = CurvePanel(BETA)
        curves = {n: C.curve(G[n], COL[n]) for n in ("Alder", "Dune")}
        centre = np.array([-0.15, -0.95, 0.0])                # a lens in the panel's empty corner, magnifying the lower-risk crossing
        up = np.array([0.5, 0.3, 0.0])
        lens = VGroup(Circle(radius=0.72, stroke_color=MUTED, stroke_width=2.5, fill_color=INK_2, fill_opacity=1).move_to(centre),
                      Line(centre - up + UP * 0.16, centre + up + UP * 0.16, stroke_width=5, color=DUNE), Line(centre - up + DOWN * 0.16, centre + up + DOWN * 0.16, stroke_width=5, color=ALDER),
                      txt("Dune", 15, DUNE, weight=SEMIBOLD).move_to(centre + np.array([-0.2, 0.42, 0.0])), txt("Alder", 15, ALDER, weight=SEMIBOLD).move_to(centre + np.array([0.22, -0.42, 0.0])))
        leader = DashedLine(C.P(0.0, OWN["Alder"][0]), centre + np.array([-0.62, 0.36, 0.0]), dash_length=0.07, stroke_width=2, color=MUTED)
        legend = VGroup(leader, lens, side("magnified", size=13).move_to(centre + DOWN * 0.92))
        marks = VGroup(*[Dot(C.P(s, OWN[n][k]), radius=0.07, color=COL[n]).set_stroke(INK, 1.5).set_z_index(5) for n in ("Alder", "Dune") for k, s in ((0, 0.0), (1, BETA))])

        def versus(k, title, y):
            return VGroup(side(title, size=17, color=PAPER), VGroup(big(pct(OWN["Dune"][k]), size=30, color=DUNE), side("against", size=16), big(pct(OWN["Alder"][k]), size=30, color=ALDER)).arrange(RIGHT, buff=0.25)).arrange(DOWN, buff=0.1).move_to([SX, y, 0])

        lo, hi = versus(0, "lower-risk patients", 1.6), versus(1, "higher-risk patients", 0.35)
        with self.nar("s1_2") as seg:
            self.play(FadeOut(VGroup(axis, one, worse, *rows.values())), run_time=0.6)
            self.play(FadeIn(C.g), Create(curves["Alder"]), Create(curves["Dune"]), FadeIn(legend), run_time=1.5)
            seg.wait_until(seg.word(0, "Dune's is the higher one"))
            self.play(FadeIn(marks), FadeIn(lo), FadeIn(hi), run_time=0.9)

        ask = VGroup(big("the higher curve,", size=26), big("but the smaller ratio?", size=26, color=ACCENT), side(f"Dune {IND['Dune']:.2f}, Alder {IND['Alder']:.2f}", size=18, color=PAPER)).arrange(DOWN, buff=0.14).move_to([SX, -1.45, 0])
        with self.nar("s1_3", gap=0.8) as seg:
            self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.9)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S02
class S02_Title(EpisodeScene):
    def construct(self):
        title_card(self, "s2_1", 12, "Swap the Patients", "one clinic's curve, everyone's patients")


# =================================================================================== S03
class S03_Puzzle(EpisodeScene):
    def construct(self):
        tag = chapter_tag(1, "Two clinics, two crowds")
        cx = {0: -2.9, 1: 1.0}
        ry = {"ref": 1.75, "Alder": 0.4, "Dune": -1.05}
        heads = VGroup(side("lower-risk patients", cx[0] + 0.6, 2.55, 17), side("higher-risk patients", cx[1] + 0.6, 2.55, 17))
        names = VGroup(txt("the reference", 20, CEDAR, weight=SEMIBOLD).move_to([-6.3, ry["ref"], 0], aligned_edge=LEFT),
                       *[txt(n, 22, COL[n], weight=SEMIBOLD).move_to([-6.3, ry[n], 0], aligned_edge=LEFT) for n in ("Alder", "Dune")])
        cell, mult, bars = {}, {}, {}
        for k in (0, 1):
            c = risk_chip(REF_P[k], r=0.32, color=CEDAR).move_to([cx[k], ry["ref"], 0])
            cell[("ref", k)] = VGroup(c, big(pct(REF_P[k]), size=28, color=CEDAR).next_to(c, RIGHT, buff=0.2))
            for n in ("Alder", "Dune"):
                c = risk_chip(OWN[n][k], r=0.32, color=COL[n]).move_to([cx[k], ry[n], 0])
                cell[(n, k)] = VGroup(c, big(pct(OWN[n][k]), size=28, color=COL[n]).next_to(c, RIGHT, buff=0.2))
                mult[(n, k)] = big(f"\u00d7 {MULT[n][k]:.1f}", size=24, color=ACCENT).move_to([cx[k] + 2.25, ry[n], 0])
                count = CASTD[n]["high" if k else "low"]
                b = Rectangle(width=0.07 * count, height=0.16, stroke_width=0, fill_color=COL[n], fill_opacity=1).move_to([cx[k] - 0.32 + 0.035 * count, ry[n] - 0.58, 0])
                bars[(n, k)] = VGroup(b, side(f"{count} patients", size=15, color=PAPER).next_to(b, RIGHT, buff=0.12))
        with self.nar("s3_1") as seg:
            self.play(FadeIn(tag), FadeIn(heads[0]), FadeIn(names), run_time=1.0)
            for key, cue in ((("ref", 0), "At the reference"), (("Alder", 0), "At Alder it is"), (("Dune", 0), "and at Dune")):
                seg.wait_until(seg.word(0, cue))
                self.play(FadeIn(cell[key], scale=0.85), run_time=0.55)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(mult[("Alder", 0)]), FadeIn(mult[("Dune", 0)]), run_time=0.7)

        with self.nar("s3_2") as seg:
            self.play(FadeIn(heads[1]), FadeIn(cell[("ref", 1)], scale=0.85), run_time=0.8)
            seg.wait_until(seg.word(0, "80 at Alder"))
            self.play(FadeIn(cell[("Alder", 1)], scale=0.85), run_time=0.5)
            seg.wait_until(seg.word(0, "81 at Dune"))
            self.play(FadeIn(cell[("Dune", 1)], scale=0.85), run_time=0.5)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(mult[("Alder", 1)]), FadeIn(mult[("Dune", 1)]), run_time=0.7)

        ratio_h = side("last time's ratio", 5.75, 2.55, 17)
        ratios = {n: big(f"{IND[n]:.2f}", size=34, color=COL[n]).move_to([5.75, ry[n], 0]) for n in ("Alder", "Dune")}
        with self.nar("s3_3") as seg:
            seg.wait_until(seg.word(0, "Of Alder's 30 patients"))
            self.play(FadeIn(bars[("Alder", 0)]), FadeIn(bars[("Alder", 1)]), run_time=0.7)
            self.play(Create(box_around(VGroup(cell[("Alder", 0)], mult[("Alder", 0)], bars[("Alder", 0)]), ALDER)), run_time=0.6)
            seg.wait_until(seg.word(0, "Dune's 12 are"))
            self.play(FadeIn(bars[("Dune", 0)]), FadeIn(bars[("Dune", 1)]), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(ratio_h), FadeIn(ratios["Alder"]), FadeIn(ratios["Dune"]), run_time=0.8)

        swap = VGroup(side("Dune's curve, with Alder's patients:", size=20, color=PAPER), big(f"{N['swapped']['dune_with_alders']:.2f}", size=34, color=DUNE), side(f"above Alder's {IND['Alder']:.2f}", size=18)).arrange(RIGHT, buff=0.3).move_to([-0.6, -2.25, 0])
        own = side("each ratio judges a clinic on its own patients", size=19, color=ACCENT).move_to([-0.6, -2.8, 0])
        with self.nar("s3_4", gap=0.8) as seg:
            self.play(FadeIn(swap), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(own), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S04
class S04_Swap(EpisodeScene):
    def construct(self):
        tag = chapter_tag(2, "Swap the patients")
        last = picture(CEDAR, [ALDER] * 7, -3.3, 1.45)
        now = picture(ALDER, MIXED, 3.3, 1.45)
        labels = VGroup(VGroup(side("last time", size=17), side("its own patients, the reference curve", size=17, color=PAPER)).arrange(DOWN, buff=0.06).next_to(last, DOWN, buff=0.15),
                        VGroup(side("today", size=17, color=ACCENT), side("everyone's patients, its own curve", size=17, color=PAPER)).arrange(DOWN, buff=0.06).next_to(now, DOWN, buff=0.15))

        def crowd(key, x):
            cols = [COL[n] for n in ORDER for _ in range(CASTD[n][key])]
            return VGroup(*[Dot(radius=0.07, color=c) for c in cols]).arrange_in_grid(cols=12, buff=0.07).move_to([x, -1.55, 0])

        lo, hi = crowd("low", -2.6), crowd("high", 2.6)
        counts = VGroup(big(f"{EVERY['low']} lower-risk", size=24).next_to(lo, DOWN, buff=0.2), big(f"{EVERY['high']} higher-risk", size=24).next_to(hi, DOWN, buff=0.2))
        every = side(f"everyone: all {EVERY['total']} patients", size=18, color=ACCENT).move_to([0, -0.55, 0])
        with self.nar("s4_1") as seg:
            self.play(FadeIn(tag), FadeIn(last), FadeIn(labels[0]), run_time=1.0)
            seg.wait_until(seg.word(0, "Keep each clinic's curve"))
            self.play(FadeIn(now), FadeIn(labels[1]), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(every), FadeIn(lo, lag_ratio=0.01), FadeIn(hi, lag_ratio=0.01), run_time=1.6)
            seg.wait_until(seg.word(1, "57 lower-risk"))
            self.play(FadeIn(counts), run_time=0.7)

        C = CurvePanel(BETA)
        curve = C.curve(G["Alder"], ALDER)
        curve_l = VGroup(Line(ORIGIN, RIGHT * 0.5, stroke_width=4.5, color=ALDER), txt("Alder's curve", 17, ALDER, weight=SEMIBOLD)).arrange(RIGHT, buff=0.15).move_to([-0.3, -1.6, 0])
        chips = {}
        for k, (s, where, n) in enumerate(((0.0, LEFT, EVERY["low"]), (BETA, UL, EVERY["high"]))):
            c = risk_chip(OWN["Alder"][k], r=0.34, color=PAPER).move_to(C.P(s, OWN["Alder"][k])).set_z_index(6)
            lab = VGroup(big(pct(OWN["Alder"][k]), size=24, color=PAPER), side(f"{n} patients", size=16, color=ACCENT)).arrange(DOWN, buff=0.04)
            lab.next_to(c, where, buff=0.12 if k == 0 else 0.03)
            chips[k] = VGroup(c, lab.shift(UP * 0.18) if k == 0 else lab)
        total = MathTex(rf"{EVERY['low']} \times {OWN['Alder'][0]:.3f} + {EVERY['high']} \times {OWN['Alder'][1]:.3f}", "=", f"{DIR['expected']['Alder']:.1f}", font_size=32, color=PAPER)
        total[2].set_color(ALDER)
        total_g = VGroup(side("everyone's chances, under Alder's curve", size=17, color=PAPER), fit_width(total, 4.8)).arrange(DOWN, buff=0.14).move_to([SX, 1.55, 0])
        of = VGroup(VGroup(big(f"{DIR['expected']['Alder']:.1f}", size=34, color=ALDER), side(f"out of {EVERY['total']}", size=20, color=PAPER)).arrange(RIGHT, buff=0.25), big(pct(DIR["rate"]["Alder"] / 100, 1), size=54, color=ACCENT)).arrange(DOWN, buff=0.2).move_to([SX, -0.15, 0])
        with self.nar("s4_2") as seg:
            self.play(FadeOut(VGroup(last, now, labels, lo, hi, counts, every)), run_time=0.6)
            self.play(FadeIn(C.g), Create(curve), FadeIn(curve_l), run_time=1.1)
            seg.wait_until(seg.word(0, "57 patients at"))
            self.play(FadeIn(chips[0], scale=0.85), run_time=0.6)
            seg.wait_until(seg.word(0, "and 46 at"))
            self.play(FadeIn(chips[1], scale=0.85), run_time=0.6)
            seg.wait_until(seg.word(0, "Add up the chances"))
            self.play(FadeIn(total_g), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(of[0]), run_time=0.6)
            seg.wait_until(seg.word(1, "If everyone had gone"))
            self.play(FadeIn(of[1], scale=0.9), run_time=0.8)

        name = VGroup(big("Alder's direct rate", size=26), side("one clinic's curve, everyone's patients", size=18, color=PAPER)).arrange(DOWN, buff=0.12).move_to([SX, -1.9, 0])
        with self.nar("s4_3", gap=0.8) as seg:
            self.play(FadeIn(name, shift=UP * 0.1), run_time=0.9)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S05
class S05_All(EpisodeScene):
    def construct(self):
        tag = chapter_tag(3, "The same patients, at every clinic")
        U, bx = 5.4, -3.7
        rows = {}
        for k, n in enumerate(ORDER):
            y, v = 1.5 - 0.72 * k, DIR["rate"][n] / 100
            frame = Rectangle(width=U, height=0.36, stroke_color=FAINT, stroke_width=1.5).move_to([bx + U / 2, y, 0])
            if n == "Elm":
                bar = VGroup(Rectangle(width=0.2, height=0.36, stroke_color=ELM, stroke_width=2).move_to([bx + 0.1, y, 0]),
                             *[Line([bx + 0.02, y - 0.16 + 0.1 * j, 0], [bx + 0.18, y - 0.04 + 0.1 * j, 0], stroke_width=1.8, color=ELM) for j in range(3)])
            else:
                bar = Rectangle(width=U * v, height=0.36, stroke_width=0, fill_color=COL[n], fill_opacity=1).move_to([bx + U * v / 2, y, 0])
            rows[n] = VGroup(txt(n, 22, COL[n], weight=SEMIBOLD).move_to([-6.3, y, 0], aligned_edge=LEFT), frame, bar, big(pct(v, 1), size=26, color=COL[n]).move_to([bx + U + 0.85, y, 0]),
                             side(f"{IND[n]:.2f}" if IND[n] else "0", size=20, color=PAPER if n in ("Alder", "Dune") else MUTED).move_to([bx + U + 2.75, y, 0]))
        heads = VGroup(side("direct rate", bx + U + 0.85, 2.1, 16), side("last time's ratio", bx + U + 2.75, 2.1, 16))
        ys = {n: 1.5 - 0.72 * k for k, n in enumerate(ORDER)}
        back = side("Dune is back above Alder", size=19, color=ACCENT).move_to([bx + U / 2, -2.2, 0])
        with self.nar("s5_1") as seg:
            self.play(FadeIn(tag), FadeIn(heads[0]), *[FadeIn(VGroup(rows[n][0], rows[n][1])) for n in ORDER], run_time=1.1)
            for n, cue in zip(FOUR, ("Alder,", "Birch,", "Cedar,", "Dune,")):
                seg.wait_until(seg.word(0, cue))
                self.play(GrowFromEdge(rows[n][2], LEFT), FadeIn(rows[n][3]), run_time=0.55)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(heads[1]), *[FadeIn(rows[n][4]) for n in FOUR], FadeIn(back), run_time=0.9)
            self.play(Indicate(rows["Dune"][3], color=PAPER, scale_factor=1.15), Indicate(rows["Alder"][3], color=PAPER, scale_factor=1.15), run_time=0.9)

        dr = E10["breaks"]["direct_rate"]
        elm_note = side(f"Elm: {dr['together']:.2f}% or {dr['turns']:.3f}%, depending on where the fitting stopped", size=17, color=ELM).move_to([bx + U / 2 + 0.6, -2.2, 0])
        with self.nar("s5_2") as seg:
            self.play(FadeOut(back), FadeIn(rows["Elm"][2]), FadeIn(rows["Elm"][3]), FadeIn(rows["Elm"][4]), run_time=0.8)
            self.play(FadeIn(elm_note), run_time=0.7)

        x_all, x_ref = bx + U * EVERY["rate"] / 100, bx + U * DIR["rate"]["Cedar"] / 100
        l_all = VGroup(DashedLine([x_all, 1.9, 0], [x_all, -1.75, 0], dash_length=0.1, stroke_width=2.5, color=MUTED),
                       side(f"the overall rate, {pct(EVERY['rate'] / 100, 1)}: not the yardstick", size=15).move_to([x_all + 1.75, 2.55, 0]))
        l_ref = VGroup(DashedLine([x_ref, 1.9, 0], [x_ref, -1.75, 0], dash_length=0.1, stroke_width=3, color=CEDAR),
                       txt(f"the reference clinic: {pct(DIR['rate']['Cedar'] / 100, 1)}", 16, CEDAR, weight=SEMIBOLD).move_to([x_ref - 1.55, 2.2, 0]))
        same = side(f"everyone at the reference: {DIR['expected']['Cedar']:.1f} readmissions, the total we met last time", size=17, color=PAPER).move_to([bx + U / 2 + 0.6, -2.2, 0])
        with self.nar("s5_3") as seg:
            self.play(FadeOut(elm_note), run_time=0.4)
            seg.wait_until(seg.word(0, "but that is not the yardstick"))
            self.play(Create(l_all[0]), FadeIn(l_all[1]), run_time=0.8)
            seg.wait_until(seg.word(0, "Cedar, the reference clinic"))
            self.play(Create(l_ref[0]), FadeIn(l_ref[1]), run_time=0.8)
            seg.wait_until(seg.word(1, "Everyone at the reference"))
            self.play(FadeIn(same), run_time=0.8)

        div = MathTex(rf"{DIR['rate']['Alder']:.1f} \div {DIR['rate']['Cedar']:.1f}", "=", f"{DIR['against_reference']['Alder']:.2f}", font_size=40, color=PAPER)
        div[2].set_color(ACCENT)
        both = VGroup(VGroup(side("today, on everyone's patients", size=16, color=PAPER), div).arrange(DOWN, buff=0.1),
                      VGroup(side("last time, on its own patients", size=16, color=PAPER), big(f"{IND['Alder']:.2f}", size=34, color=ALDER)).arrange(DOWN, buff=0.1)).arrange(RIGHT, buff=1.1).move_to([bx + U / 2 + 0.6, -2.3, 0])
        with self.nar("s5_4", gap=0.8) as seg:
            self.play(FadeOut(same), FadeIn(both[0]), run_time=0.8)
            seg.wait_until(seg.word(0, "Last time's ratio said"))
            self.play(FadeIn(both[1]), run_time=0.7)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S06
class S06_Which(EpisodeScene):
    def construct(self):
        tag = chapter_tag(4, "Which question?")

        def side_card(x, when, when_color, curve_color, dots, question, use):
            c = card(5.7, 4.3).move_to([x, 0.25, 0])
            pic = VGroup(mini_curve(curve_color), VGroup(*[Dot(radius=0.1, color=col) for col in dots]).arrange(RIGHT, buff=0.11)).arrange(DOWN, buff=0.25).move_to([x, 1.05, 0])
            return VGroup(c, txt(when, 18, when_color, weight=SEMIBOLD).move_to([x, 2.05, 0]), pic, VGroup(*[txt(s, 20, PAPER) for s in question]).arrange(DOWN, buff=0.1).move_to([x, -0.45, 0]), pill(use, 19).move_to([x, -1.4, 0]))

        left = side_card(-3.25, "last time", MUTED, CEDAR, [ALDER] * 7, ["how did this clinic do", "with the patients it treated?"], "holding a clinic to account")
        right = side_card(3.25, "today", ACCENT, ALDER, MIXED, ["how would this clinic do", "with everyone's patients?"], "choosing between clinics")
        with self.nar("s6_1") as seg:
            self.play(FadeIn(tag), FadeIn(VGroup(*left[:4])), run_time=1.2)
            seg.wait_until(seg.word(0, "That is the one to ask"))
            self.play(FadeIn(left[4], scale=0.9), run_time=0.7)

        neither = big("neither is a rate that anyone experienced", size=24, color=ACCENT).move_to([0, -2.6, 0])
        with self.nar("s6_2", gap=0.8) as seg:
            self.play(FadeIn(VGroup(*right[:4])), run_time=1.0)
            seg.wait_until(seg.word(0, "That is closer to"))
            self.play(FadeIn(right[4], scale=0.9), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(neither, shift=UP * 0.1), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S07
class S07_Price(EpisodeScene):
    def construct(self):
        tag = chapter_tag(5, "The price of a common footing")
        U, xs = 0.045, {0: -3.5, 1: -0.3}
        heads = VGroup(side("lower-risk", xs[0] + 0.6, 2.5, 16), side("higher-risk", xs[1] + 0.6, 2.5, 16))

        def block(name, y):
            g = VGroup(txt(name, 24, COL[name], weight=SEMIBOLD).move_to([-6.3, y + 0.25, 0], aligned_edge=LEFT))
            parts = {}
            for row, (lab, vals, dy, op) in enumerate((("treated", N["asked"][name]["treated"], 0.25, 1.0), ("asked about", N["asked"][name]["asked"], -0.35, 0.45))):
                rl = side(lab, size=16, color=PAPER).move_to([-4.75, y + dy, 0], aligned_edge=LEFT)
                cells = VGroup()
                for k in (0, 1):
                    w = max(U * vals[k], 0.02)
                    b = Rectangle(width=w, height=0.3, stroke_width=0, fill_color=COL[name], fill_opacity=op if vals[k] else 0).move_to([xs[k] + w / 2, y + dy, 0])
                    cells.add(VGroup(b, txt(str(vals[k]), 20, PAPER if vals[k] else ALERT, weight=SEMIBOLD).next_to(b, RIGHT, buff=0.12)))
                parts[lab] = VGroup(rl, cells)
            return g, parts

        a_name, a = block("Alder", 1.5)
        e_name, e = block("Elm", -1.0)
        ex, lo_part, hi_part = DIR["expected"]["Alder"], *DIR["parts"]["Alder"]
        BU = 0.052
        stack = VGroup(Rectangle(width=BU * lo_part, height=0.34, stroke_width=0, fill_color=ALDER, fill_opacity=0.45).move_to([3.1 + BU * lo_part / 2, 1.45, 0]),
                       Rectangle(width=BU * hi_part, height=0.34, stroke_width=0, fill_color=ALDER, fill_opacity=1).move_to([3.1 + BU * lo_part + BU * hi_part / 2, 1.45, 0]))
        two_thirds = fit_width(side("two-thirds from higher-risk patients", size=16, color=ACCENT), 3.6).move_to([3.1 + BU * ex / 2 + 0.25, 0.9, 0])
        stack_l = VGroup(side(f"Alder's {ex:.1f}", size=17, color=PAPER).move_to([3.1 + BU * ex / 2, 2.0, 0]), txt(f"{lo_part:.1f}", 16, PAPER).move_to(stack[0]), txt(f"{hi_part:.1f}", 16, INK, weight=SEMIBOLD).move_to(stack[1]), two_thirds)
        with self.nar("s7_1") as seg:
            self.play(FadeIn(tag), FadeIn(heads), FadeIn(a_name), run_time=1.0)
            seg.wait_until(seg.word(0, "Alder treated only"))
            self.play(FadeIn(a["treated"]), run_time=0.7)
            seg.wait_until(seg.word(0, "Its direct rate asks"))
            self.play(FadeIn(a["asked about"]), run_time=0.7)
            self.play(Create(box_around(VGroup(a["treated"][1][1], a["asked about"][1][1]), ACCENT)), run_time=0.6)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(stack), FadeIn(stack_l), run_time=1.0)

        shape = VGroup(side(f"{pct(DIR['from_high']['Elm'])} of Elm's count comes from", size=17, color=PAPER), side("patients of a kind it never treated", size=17, color=PAPER),
                       big("it rests on curves of one shape", size=22, color=ACCENT)).arrange(DOWN, buff=0.1)
        shape = fit_width(shape, 3.9).move_to([4.95, -1.05, 0])
        with self.nar("s7_2", gap=0.8) as seg:
            self.play(FadeIn(e_name), FadeIn(e["treated"]), FadeIn(e["asked about"]), run_time=1.0)
            seg.wait_until(seg.word(0, "Elm treated no"))
            self.play(Create(box_around(VGroup(e["treated"][1][1], e["asked about"][1][1]), ALERT)), run_time=0.7)
            seg.wait_until(seg.word(0, "Its figure rests"))
            self.play(FadeIn(shape), run_time=0.9)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S08
class S08_Crowd(EpisodeScene):
    def construct(self):
        tag = chapter_tag(6, "In the crowd")
        x0, x1, y0, y1 = -5.2, 1.0, -1.9, 2.2
        isr, dsr, move = np.array(CROWD["isr"]), np.array(CROWD["dsr"]), np.array(CROWD["move"])
        a_lo, a_hi, b_lo, b_hi = 0.3, 2.1, float(np.floor(dsr.min() * 10) / 10), float(np.ceil(dsr.max() * 10) / 10)
        X = lambda v: x0 + (x1 - x0) * (v - a_lo) / (a_hi - a_lo)
        Y = lambda v: y0 + (y1 - y0) * (v - b_lo) / (b_hi - b_lo)
        yt = [v for v in (0.6, 0.8, 1.0, 1.2, 1.4, 1.6) if b_lo <= v <= b_hi]
        axes = VGroup(Line([x0, y0, 0], [x1, y0, 0], stroke_width=3, color=MUTED), Line([x0, y0, 0], [x0, y1, 0], stroke_width=3, color=MUTED),
                      *[VGroup(Line([X(v), y0, 0], [X(v), y0 - 0.1, 0], stroke_width=2, color=MUTED), txt(f"{v:g}", 16, MUTED).move_to([X(v), y0 - 0.3, 0])) for v in (0.5, 1, 1.5, 2)],
                      *[VGroup(Line([x0 - 0.1, Y(v), 0], [x0, Y(v), 0], stroke_width=2, color=MUTED), txt(f"{v:g}", 16, MUTED).move_to([x0 - 0.4, Y(v), 0])) for v in yt],
                      side("last time's ratio: its own patients", size=16).move_to([(x0 + x1) / 2, y0 - 0.64, 0]), side("today's ratio: everyone's patients", size=16).move_to([x0 + 1.75, y1 + 0.26, 0]))
        cloud = VGroup(*[Dot([X(a), Y(b), 0], radius=0.045, color=PAPER).set_opacity(0.7) for a, b in zip(isr, dsr)])
        big_movers = [k for k in range(len(move)) if move[k] >= 10]
        rings = VGroup(*[Circle(radius=0.16, stroke_color=ACCENT, stroke_width=3).move_to([X(isr[k]), Y(dsr[k]), 0]) for k in big_movers]).set_z_index(5)
        agree = VGroup(side("the two measures agree closely", size=18, color=PAPER), big(f"correlation {CROWD['corr']:.2f}", size=26)).arrange(DOWN, buff=0.12).move_to([SX + 0.1, 1.3, 0])
        yet = VGroup(big(f"{CROWD['movers']} providers", size=28, color=ACCENT), side("move ten places or more", size=18, color=PAPER), side(f"between the two rankings; the largest move is {CROWD['largest']}", size=15)).arrange(DOWN, buff=0.12)
        yet = fit_width(yet, 4.4).move_to([SX + 0.1, -0.4, 0])
        shift = side("a ranking can shift with the question", size=18, color=ACCENT).move_to([SX + 0.1, -1.9, 0])
        with self.nar("s8_1", gap=0.8) as seg:
            self.play(FadeIn(tag), FadeIn(axes), run_time=1.0)
            self.play(FadeIn(cloud, lag_ratio=0.01), FadeIn(agree), run_time=1.6)
            seg.wait_until(seg.word(0, "Yet between the two rankings"))
            self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.2), FadeIn(yet), run_time=1.2)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(shift), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S09
class S09_Recap(EpisodeScene):
    def construct(self):
        tag = chapter_tag(7, "Recap")
        xs = (-4.45, 0.0, 4.45)
        cards = VGroup(*[card(4.05, 3.7).move_to([x, 0.15, 0]) for x in xs])
        pic = lambda curve_color, dots: VGroup(mini_curve(curve_color, w=1.5, h=0.8), VGroup(*[Dot(radius=0.08, color=c) for c in dots]).arrange(RIGHT, buff=0.09)).arrange(DOWN, buff=0.18)
        warn = VGroup(Triangle(color=ALERT, stroke_width=3).scale(0.2), txt("!", 18, ALERT, weight=SEMIBOLD))
        warn[1].move_to(warn[0].get_center() + DOWN * 0.03)
        icon3 = VGroup(VGroup(tick_mark(s=0.9), txt("like with like", 17, PAPER)).arrange(RIGHT, buff=0.15), VGroup(warn, txt("never treated", 17, PAPER)).arrange(RIGHT, buff=0.15)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        icons = [pic(CEDAR, [ALDER] * 6), pic(ALDER, MIXED[:6]), icon3]
        caps = [["Last time: a clinic's own", "patients, the reference curve"], ["This time: everyone's patients,", "the clinic's own curve"], ["The second compares like with", "like, but extrapolates.", "Say which one you report"]]
        captions = VGroup()
        for k, (ic, cp) in enumerate(zip(icons, caps)):
            ic.move_to([xs[k], 0.9, 0])
            captions.add(fit_width(VGroup(*[txt(s, 19, PAPER) for s in cp]).arrange(DOWN, buff=0.1), 3.6).move_to([xs[k], -0.85, 0]))
        with self.nar("s9_1") as seg:
            self.play(FadeIn(tag), run_time=0.8)
            for k in range(3):
                seg.wait_until(seg.s(k + 1) - 0.1)
                self.play(FadeIn(cards[k], shift=UP * 0.15), FadeIn(captions[k], shift=UP * 0.1), FadeIn(icons[k], shift=UP * 0.1), run_time=1.1)

        obs = CASTD["Alder"]["observed"]
        count = VGroup(VGroup(side("Alder observed", size=22, color=PAPER), big(str(obs), size=72, color=ALDER)).arrange(DOWN, buff=0.15), side("against", size=22),
                       VGroup(side("expected at the reference", size=22, color=PAPER), big(f"{E11['alder']['ref_expected']:.2f}", size=72, color=CEDAR)).arrange(DOWN, buff=0.15)).arrange(RIGHT, buff=0.7).move_to([-2.0, 0.55, 0])
        luck = big("a real difference, or luck?", size=30, color=ACCENT).move_to([-2.0, -1.5, 0])
        nxt = VGroup(txt("Next:", 26, MUTED), big("unequal coins", size=34)).arrange(DOWN, buff=0.2).move_to([4.8, 0.35, 0])
        with self.nar("s9_2") as seg:
            self.play(FadeOut(VGroup(cards, captions, *icons)), run_time=0.7)
            self.play(FadeIn(count, scale=0.95), run_time=1.0)
            seg.wait_until(seg.word(0, "A real difference"))
            self.play(FadeIn(luck, shift=UP * 0.1), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(nxt, shift=UP * 0.15), run_time=0.9)
        end_card(self, "s9_3", 13, "Unequal Coins")
