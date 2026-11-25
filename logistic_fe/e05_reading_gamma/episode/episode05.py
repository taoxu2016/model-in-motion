"""Model in Motion · The Logistic Fixed-Effect Model · Episode 5: Reading gamma (what a gap between two clinics means for a patient).

ANIMATIC PASS. Every narration clip has its board. The compositions are meant to stay; most of the motion is still to come.

Render one scene:   manim -ql --media_dir build/media episode/episode05.py S04_Slide      (run from the episode folder)
Every scene reads audio/manifest.json; each `with self.nar("sX_Y") as seg:` block starts that voiceover clip and
holds the scene until the clip (plus a short gap) has finished.
Every number comes from e05_numbers.json, written by e05_numbers.py; none is typed here.
All content stays above y = -3.0 so that burned-in captions never cover it.
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

N = json.loads((ROOT / "e05_numbers.json").read_text())
BETA, G, PR = N["fit"]["beta"], N["fit"]["gamma"], N["fit"]["p"]          # PR[clinic] = [lower-risk, higher-risk] probability
GAP, OR = N["gap"]["alder_minus_cedar"], N["gap"]["odds_ratio"]
GA, GC = G["Alder"], G["Cedar"]
R1, R2, R3, SLIDE, ZERO, AVG = N["reading_one"], N["reading_two"], N["reading_three"], N["slide"], N["zero"], N["averages"]
COL = {n: CLINICS[n]["color"] for n in ORDER}
X24 = f"{OR:.1f}"                           # the odds ratio as it is spoken: 2.4


def reading_header(k, text):
    return VGroup(big(str(k), size=40, color=ACCENT), big(text, size=30)).arrange(RIGHT, buff=0.35).move_to([0, 2.35, 0])


def row_arrow(y):
    return Arrow([0.25, y, 0], [1.15, y, 0], buff=0, stroke_width=3, color=MUTED, max_tip_length_to_length_ratio=0.25)


# =================================================================================== S01
class S01_ColdOpen(EpisodeScene):
    def construct(self):
        P = LinePanel()
        la, lc = P.line(GA, BETA, ALDER), P.line(GC, BETA, CEDAR)
        names = VGroup(txt("Alder", 20, ALDER, weight=SEMIBOLD).next_to(P.P(1.0, GA + BETA), UL, buff=0.12),
                       txt("Cedar", 20, CEDAR, weight=SEMIBOLD).next_to(P.P(1.0, GC + BETA), DR, buff=0.12))
        z = ValueTracker(0.5)

        def bracket():
            t = z.get_value()
            arr = DoubleArrow(P.P(t, GC + BETA * t), P.P(t, GA + BETA * t), buff=0, stroke_width=3.5, color=ACCENT, tip_length=0.14)
            lab = txt(f"{GAP:.2f}", 26, ACCENT, weight=SEMIBOLD, font=DISPLAY).next_to(arr, RIGHT, buff=0.18)
            return VGroup(arr, lab).set_z_index(6)

        br = always_redraw(bracket)
        with self.nar("s1_1") as seg:
            self.play(FadeIn(P.g), Create(la), Create(lc), FadeIn(names), run_time=1.4)
            seg.wait_until(seg.s(1))
            self.add(br)
            seg.wait_until(seg.word(1, "At the lower-risk end"))
            self.play(z.animate.set_value(0.0), run_time=1.0)
            seg.wait_until(seg.word(1, "at the higher-risk end"))
            self.play(z.animate.set_value(1.0), run_time=1.2)
            seg.wait_until(seg.word(1, "anywhere you look"))
            self.play(z.animate.set_value(0.5), run_time=1.0)

        step = VGroup(side("a step of", color=PAPER), big(f"{GAP:.2f}", size=34, color=ACCENT)).arrange(RIGHT, buff=0.25).move_to([SX, 1.2, 0])
        arrow = Arrow(UP * 0.3, DOWN * 0.3, buff=0, stroke_width=3, color=MUTED, max_tip_length_to_length_ratio=0.3).move_to([SX, 0.5, 0])
        mult = fit_width(VGroup(side("multiplies the odds by", color=PAPER), big(X24, size=40, color=ACCENT)).arrange(RIGHT, buff=0.25), 4.4).move_to([SX, -0.2, 0])
        what = VGroup(big(f"{X24} times", size=32), big("what?", size=32, color=ACCENT)).arrange(RIGHT, buff=0.2).move_to([SX, -1.5, 0])
        with self.nar("s1_2") as seg:
            self.play(FadeIn(step, shift=UP * 0.1), run_time=0.8)
            seg.wait_until(seg.word(0, "multiplies the odds"))
            self.play(GrowArrow(arrow), FadeIn(mult, shift=UP * 0.1), run_time=0.9)
            seg.wait_until(seg.word(1, "But"))
            self.play(FadeIn(what, shift=UP * 0.1), run_time=0.8)

        xs = (-4.45, 0.0, 4.45)
        cards = VGroup(*[card(4.05, 3.2).move_to([x, -0.1, 0]) for x in xs])
        nums = VGroup(*[big(str(k + 1), xs[k], 0.95, 44, ACCENT) for k in range(3)])
        texts = [["Alder has", f"{X24} times as many", "readmissions"], ["each patient is", f"{X24} times as likely", "to be readmitted"],
                 ["each patient's odds", "of readmission are", f"{X24} times as high"]]
        caps = VGroup(*[VGroup(*[txt(s, 22, PAPER) for s in t]).arrange(DOWN, buff=0.1).move_to([xs[k], -0.5, 0]) for k, t in enumerate(texts)])
        head = big(f"Alder is {X24} times Cedar. {X24} times what?", 0, 2.45, 32)
        pick = side("pick one before we go on", size=24, color=ACCENT).move_to([0, -2.4, 0])
        with self.nar("s1_3", gap=0.8) as seg:
            br.clear_updaters()
            self.play(*clear(self), run_time=0.7)
            self.play(FadeIn(head, shift=UP * 0.1), run_time=0.7)
            for k in range(3):
                seg.wait_until(seg.s(k + 1) - 0.1)
                self.play(FadeIn(cards[k], shift=UP * 0.15), FadeIn(nums[k]), FadeIn(caps[k], shift=UP * 0.1), run_time=0.9)
            seg.wait_until(seg.s(4))
            self.play(FadeIn(pick), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S02
class S02_Title(EpisodeScene):
    def construct(self):
        title_card(self, "s2_1", 5, "Reading \u03b3", "what a gap between two clinics means for a patient")


# =================================================================================== S03
class S03_Three(EpisodeScene):
    def construct(self):
        tag = chapter_tag(1, "Three readings")

        # ---- reading one: as many readmissions?
        h1 = reading_header(1, f"Alder has {X24} times as many readmissions?")
        rows1 = {}
        for n, y in (("Alder", 0.7), ("Cedar", -0.5)):
            e, m, r = R1[n.lower()]
            rows1[n] = VGroup(txt(n, 26, COL[n], weight=SEMIBOLD).move_to([-5.6, y, 0], aligned_edge=LEFT),
                              txt(f"{e} of {m}", 24, PAPER).move_to([-4.0, y, 0], aligned_edge=LEFT),
                              Rectangle(width=6.0, height=0.36, stroke_width=0, fill_color=FAINT, fill_opacity=1).move_to([1.0, y, 0]),
                              Rectangle(width=6.0 * r, height=0.36, stroke_width=0, fill_color=COL[n], fill_opacity=1).move_to([-2.0 + 3.0 * r, y, 0]),
                              big(pct(r), 5.0, y, 30, COL[n]))
        note1 = side("raw counts depend on who each clinic treats", size=22).move_to([0, -1.8, 0])
        x1 = cross_mark(s=1.6).next_to(h1, RIGHT, buff=0.4)
        with self.nar("s3_1") as seg:
            self.play(FadeIn(tag), FadeIn(h1, shift=UP * 0.1), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(rows1["Alder"][:3]), GrowFromEdge(rows1["Alder"][3], LEFT), run_time=1.0)
            seg.wait_until(seg.word(1, "Cedar had"))
            self.play(FadeIn(rows1["Cedar"][:3]), GrowFromEdge(rows1["Cedar"][3], LEFT), run_time=1.0)
            seg.wait_until(seg.word(1, "That is"))
            self.play(FadeIn(rows1["Alder"][4]), FadeIn(rows1["Cedar"][4]), run_time=0.7)
            seg.wait_until(seg.s(2))
            self.play(FadeIn(note1), Create(x1), run_time=0.9)

        # ---- reading two: as likely?
        h2 = reading_header(2, f"each patient is {X24} times as likely?")
        heads = VGroup(side("at Cedar", -1.0, 1.6, 19), side("at Alder", 2.35, 1.6, 19))

        def chip_row(label, pc, pa, mult, y):
            return VGroup(side(label, size=22, color=PAPER).move_to([-5.9, y, 0], aligned_edge=LEFT),
                          risk_chip(pc, r=0.42, color=CEDAR).move_to([-1.5, y, 0]), big(pct(pc), -0.5, y, 28, CEDAR), row_arrow(y),
                          risk_chip(pa, r=0.42, color=ALDER).move_to([1.9, y, 0]), big(pct(pa), 2.9, y, 28, ALDER),
                          big(f"\u00d7 {mult:.1f}", 5.0, y, 32, PAPER))

        rl = chip_row("a lower-risk patient", PR["Cedar"][0], PR["Alder"][0], R2["ratio_low"], 0.6)
        rh = chip_row("a higher-risk patient", PR["Cedar"][1], PR["Alder"][1], R2["ratio_high"], -0.7)
        imp = side(f"{X24} \u00d7 {pct(PR['Cedar'][1])} would be {100 * R2['impossible']:.0f}%", size=22, color=ALERT).move_to([0, -1.9, 0])
        x2 = cross_mark(s=1.6).next_to(h2, RIGHT, buff=0.4)
        with self.nar("s3_2") as seg:
            self.play(*clear(self, keep=(tag,)), run_time=0.6)
            self.play(FadeIn(h2, shift=UP * 0.1), FadeIn(heads), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(rl[:6]), run_time=1.0)
            seg.wait_until(seg.word(1, "That is"))
            self.play(FadeIn(rl[6], shift=LEFT * 0.1), run_time=0.7)
            seg.wait_until(seg.s(2))
            self.play(FadeIn(rh[:6]), run_time=1.0)
            seg.wait_until(seg.word(2, "only"))
            self.play(FadeIn(rh[6], shift=LEFT * 0.1), run_time=0.7)
            seg.wait_until(seg.s(3))
            self.play(FadeIn(imp), Create(x2), run_time=0.9)

        # ---- reading three: odds
        h3 = reading_header(3, f"each patient's odds are {X24} times as high?")

        def odds_row(label, oc, oa, y):
            return VGroup(side(label, size=22, color=PAPER).move_to([-5.9, y, 0], aligned_edge=LEFT),
                          VGroup(side("odds", size=18), big(f"{oc:.2f}", size=30, color=CEDAR)).arrange(RIGHT, buff=0.2).move_to([-1.0, y, 0]), row_arrow(y),
                          VGroup(side("odds", size=18), big(f"{oa:.2f}", size=30, color=ALDER)).arrange(RIGHT, buff=0.2).move_to([2.35, y, 0]),
                          big(f"\u00d7 {X24}", 5.0, y, 32, ACCENT))

        ol = odds_row("a lower-risk patient", R3["cedar_odds"][0], R3["alder_odds"][0], 0.6)
        oh = odds_row("a higher-risk patient", R3["cedar_odds"][1], R3["alder_odds"][1], -0.7)
        formula = MathTex(r"e^{\,\gamma_{\text{Alder}} - \gamma_{\text{Cedar}}}", "=", rf"e^{{\,{GAP:.2f}}}", "=", X24, font_size=40, color=PAPER).move_to([-1.2, -1.85, 0])
        formula[4].set_color(ACCENT)
        orlab = side("the odds ratio", size=24, color=ACCENT).next_to(formula, RIGHT, buff=0.5)
        t3 = tick_mark(s=1.6).next_to(h3, RIGHT, buff=0.4)
        with self.nar("s3_3", gap=0.8) as seg:
            self.play(*clear(self, keep=(tag, heads)), run_time=0.6)
            self.play(FadeIn(h3, shift=UP * 0.1), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(ol[:4]), run_time=0.9)
            self.play(FadeIn(ol[4], shift=LEFT * 0.1), run_time=0.6)
            seg.wait_until(seg.s(2))
            self.play(FadeIn(oh[:4]), run_time=0.9)
            self.play(FadeIn(oh[4], shift=LEFT * 0.1), run_time=0.6)
            seg.wait_until(seg.s(3))
            self.play(Write(formula), Create(t3), run_time=1.4)
            seg.wait_until(seg.word(3, "the odds ratio"))
            self.play(FadeIn(orlab, shift=LEFT * 0.1), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S04
class S04_Slide(EpisodeScene):
    def construct(self):
        tag = chapter_tag(2, "One odds ratio, many effects")
        C = CurvePanel(BETA)
        cc, ca = C.curve(GC, CEDAR), C.curve(GA, ALDER)
        nC = txt("Cedar", 20, CEDAR, weight=SEMIBOLD).next_to(C.P(3.9, expit(GC + 3.9)), DR, buff=0.1)
        nA = txt("Alder", 20, ALDER, weight=SEMIBOLD).next_to(C.P(-0.6, expit(GA - 0.6)), UL, buff=0.1)
        s = ValueTracker(SLIDE[0]["s"] - 1.0)
        dC = always_redraw(lambda: Dot(C.P(s.get_value(), expit(GC + s.get_value())), radius=0.1, color=CEDAR).set_stroke(INK, 1.5).set_z_index(6))
        dA = always_redraw(lambda: Dot(C.P(s.get_value(), expit(GA + s.get_value())), radius=0.1, color=ALDER).set_stroke(INK, 1.5).set_z_index(6))
        link = always_redraw(lambda: Line(C.P(s.get_value(), expit(GC + s.get_value())), C.P(s.get_value(), expit(GA + s.get_value())),
                                          stroke_width=5, color=ACCENT).set_z_index(5))
        cols = (3.0, 4.15, 5.35, 6.5)
        heads = VGroup(side("at Cedar", cols[0], 2.1, 17), side("at Alder", cols[1], 2.1, 17), side("difference", cols[2], 2.1, 17))
        rhead = side("ratio", cols[3], 2.1, 17)
        rows, ratios, ghosts = [], [], []
        for k, r in enumerate(SLIDE):
            y = 1.5 - 0.55 * k
            rows.append(VGroup(big(pct(r["cedar"]), cols[0], y, 24, CEDAR), big(pct(r["alder"]), cols[1], y, 24, ALDER),
                               big(f"+{round(100 * r['alder']) - round(100 * r['cedar'])}", cols[2], y, 24, ACCENT)))
            ratios.append(txt(f"\u00d7 {r['ratio']:.2f}" if r["ratio"] < 1.1 else f"\u00d7 {r['ratio']:.1f}", 20, PAPER).move_to([cols[3], y, 0]))
            ghosts.append(VGroup(Line(C.P(r["s"], r["cedar"]), C.P(r["s"], r["alder"]), stroke_width=3, color=ACCENT),
                                 Dot(C.P(r["s"], r["cedar"]), radius=0.07, color=CEDAR), Dot(C.P(r["s"], r["alder"]), radius=0.07, color=ALDER)).set_z_index(4))
        cost = VGroup(side("what a gap costs depends on", size=18, color=PAPER), side("which patients a clinic sees", size=18, color=PAPER)).arrange(DOWN, buff=0.08)
        cost.move_to([4.75, -1.85, 0])
        with self.nar("s4_1") as seg:
            self.play(FadeIn(tag), FadeIn(C.g), Create(cc), Create(ca), FadeIn(nC), FadeIn(nA), run_time=1.6)
            seg.wait_until(seg.s(1))
            self.add(link, dC, dA)
            self.play(s.animate.set_value(SLIDE[0]["s"] - 0.4), FadeIn(heads), run_time=1.2)

        with self.nar("s4_2") as seg:
            for k, r in enumerate(SLIDE):
                if k:
                    seg.wait_until(seg.s(k) - 0.1)
                self.play(s.animate.set_value(r["s"]), run_time=0.9)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.1), FadeIn(ghosts[k]), run_time=0.6)

        with self.nar("s4_3", gap=0.8) as seg:
            seg.wait_until(seg.word(0, "the difference in probability"))
            self.play(*[Indicate(rw[2], color=PAPER, scale_factor=1.3) for rw in rows], run_time=1.2)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(rhead), LaggedStart(*[FadeIn(x, shift=RIGHT * 0.1) for x in ratios], lag_ratio=0.15), run_time=1.4)
            seg.wait_until(seg.s(2))
            self.play(FadeIn(cost), run_time=0.9)
        for m in (link, dC, dA):
            m.clear_updaters()
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S05
class S05_Zero(EpisodeScene):
    def construct(self):
        tag = chapter_tag(3, "Gammas move. Gaps don't.")
        P = LinePanel()
        lines = VGroup(*[P.line(G[n], BETA, COL[n]) for n in FOUR])
        z = ValueTracker(0.0)
        zero = always_redraw(lambda: VGroup(Line(P.P(z.get_value(), P.lo), P.P(z.get_value(), P.hi), stroke_width=3, color=ACCENT),
                                            txt("zero", 18, ACCENT, weight=SEMIBOLD).next_to(P.P(z.get_value(), P.hi), UP, buff=0.08)).set_z_index(2))
        rings = {n: always_redraw(lambda n=n: ring_at(P.P(z.get_value(), G[n] + BETA * z.get_value()), COL[n])) for n in FOUR}
        dial, blab, sl, glab = controls(BETA, {**G, "Elm": -2.2}, lo=-2.2, hi=1.8)
        bval = big(f"{BETA:.2f}", size=26, color=ACCENT).next_to(dial, DOWN, buff=0.22)
        vals = {}
        for n in FOUR:
            sl[n].add_updater(lambda m, n=n: m.slide_to(G[n] + BETA * z.get_value()))
            vals[n] = DecimalNumber(G[n], num_decimal_places=2, include_sign=True, font_size=18, color=PAPER)
            vals[n].add_updater(lambda m, n=n: m.set_value(G[n] + BETA * z.get_value()).next_to(sl[n].track, UP, buff=0.12))
            vals[n].update()

        def bracket():
            t = z.get_value()
            arr = DoubleArrow(P.P(t, GC + BETA * t) + RIGHT * 0.22, P.P(t, GA + BETA * t) + RIGHT * 0.22, buff=0, stroke_width=3.5, color=ACCENT, tip_length=0.14)
            return VGroup(arr, txt(f"{GAP:.2f}", 22, ACCENT, weight=SEMIBOLD).next_to(arr, RIGHT, buff=0.12)).set_z_index(6)

        br = always_redraw(bracket)
        zl = VGroup(side("so far, zero has meant", size=18, color=PAPER), side("a lower-risk patient", size=18, color=PAPER)).arrange(DOWN, buff=0.08).move_to([SX, -0.9, 0])
        t_hi = VGroup(side("every gamma", color=PAPER), big(f"+ {ZERO['higher']['shift_in_gamma']:.2f}", size=34, color=ACCENT)).arrange(RIGHT, buff=0.3).move_to([SX, -0.9, 0])
        t_mid = VGroup(side("every gamma", color=PAPER), big(f"+ {ZERO['halfway']['shift_in_gamma']:.2f}", size=34, color=ACCENT)).arrange(RIGHT, buff=0.3).move_to([SX, -0.9, 0])
        t_mid_note = side("from where it started", size=17).next_to(t_mid, DOWN, buff=0.12)
        moral = VGroup(side("a gamma depends on where zero is", size=18, color=PAPER), big("a gap doesn't", size=30, color=ACCENT)).arrange(DOWN, buff=0.14).move_to([SX, -1.9, 0])
        self.play(FadeIn(tag), FadeIn(P.g), FadeIn(lines), FadeIn(dial), FadeIn(blab), FadeIn(glab), FadeIn(bval), *[FadeIn(x) for x in sl.values()], run_time=1.0)

        with self.nar("s5_1") as seg:
            seg.wait_until(seg.s(1))
            self.add(zero, *rings.values())
            self.play(*[FadeIn(v) for v in vals.values()], run_time=0.8)
            seg.wait_until(seg.word(1, "So far"))
            self.play(FadeIn(zl), run_time=0.7)

        with self.nar("s5_2") as seg:
            seg.wait_until(seg.word(0, "Call the higher-risk"))
            self.play(z.animate.set_value(1.0), FadeOut(zl), run_time=2.2)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(t_hi, shift=UP * 0.1), run_time=0.8)
            seg.wait_until(seg.s(2))
            self.play(z.animate.set_value(0.5), FadeOut(t_hi), run_time=1.8)
            seg.wait_until(seg.word(2, "Now every gamma"))
            self.play(FadeIn(t_mid, shift=UP * 0.1), FadeIn(t_mid_note), run_time=0.8)

        with self.nar("s5_3", gap=0.8) as seg:
            self.play(Indicate(lines, color=PAPER, scale_factor=1.02), FadeOut(t_mid), FadeOut(t_mid_note), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.add(br)
            self.play(z.animate.set_value(0.0), run_time=1.2)
            self.play(z.animate.set_value(1.0), run_time=1.4)
            seg.wait_until(seg.s(2))
            self.play(z.animate.set_value(0.5), FadeIn(moral, shift=UP * 0.1), run_time=1.2)
        for m in [zero, br, *rings.values(), *sl.values(), *vals.values()]:
            m.clear_updaters()
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S06
class S06_Averages(EpisodeScene):
    def construct(self):
        tag = chapter_tag(4, "A warning about averages")

        def avg_row(n, y):
            lab = txt(f"all {N['patients']} patients at {n}'s level", 24, COL[n], weight=SEMIBOLD).move_to([-6.2, y, 0], aligned_edge=LEFT)
            det = side(f"{AVG['n_low']} lower-risk at {pct(PR[n][0])},  {AVG['n_high']} higher-risk at {pct(PR[n][1])}", size=17).next_to(lab, DOWN, buff=0.1, aligned_edge=LEFT)
            return VGroup(lab, det, big(pct(AVG[f"{n.lower()}_rate"]), 0.6, y - 0.15, 40, COL[n]))

        rC, rA = avg_row("Cedar", 2.2), avg_row("Alder", 1.0)
        lc, la = logit(AVG["cedar_rate"]), logit(AVG["alder_rate"])
        R = Ruler(-1.35, -1.0, 1.0, x0=-5.2, x1=0.8, ticks=[-1.0, -0.5, 0.0, 0.5, 1.0], labels={-1.0: signed(-1, 0), 0.0: "0", 1.0: signed(1, 0)}, title="log-odds")
        dC, dA = Dot(R.P(lc), radius=0.12, color=CEDAR).set_z_index(4), Dot(R.P(la), radius=0.12, color=ALDER).set_z_index(4)
        pcs = VGroup(txt(pct(AVG["cedar_rate"]), 18, CEDAR, weight=SEMIBOLD).next_to(dC, DOWN, buff=0.45), txt(pct(AVG["alder_rate"]), 18, ALDER, weight=SEMIBOLD).next_to(dA, DOWN, buff=0.45))
        brk = DoubleArrow(R.P(lc, 0.4), R.P(la, 0.4), buff=0, stroke_width=3.5, color=PAPER, tip_length=0.14)
        brl = big(f"{AVG['gap']:.2f}", size=28).next_to(brk, UP, buff=0.12)

        U, x0 = 3.6, 2.5

        def bar(value, color, title, caption, y):
            head = VGroup(side(title, size=18, color=PAPER), big(f"{value:.2f}", size=28, color=color)).arrange(RIGHT, buff=0.3).move_to([x0, y + 0.42, 0], aligned_edge=LEFT)
            rect = Rectangle(width=U * value, height=0.26, stroke_width=0, fill_color=color, fill_opacity=1).move_to([x0 + U * value / 2, y, 0])
            cap = fit_width(side(caption, size=16), 4.4).move_to([x0, y - 0.36, 0], aligned_edge=LEFT)
            return VGroup(head, rect), cap

        b87, c87 = bar(GAP, ACCENT, "for each patient", "one kind of patient at a time", 0.05)
        b69, c69 = bar(AVG["gap"], PAPER, "between the two averages", "over patients of very different risk", -1.25)
        moral = fit_width(side("smaller whenever patients differ in risk", size=18, color=ACCENT), 4.4).move_to([x0, -2.25, 0], aligned_edge=LEFT)
        last = side("a model's gap can exceed the gap between two overall rates: no contradiction", size=17, color=PAPER).move_to([-2.4, -2.5, 0])
        with self.nar("s6_1") as seg:
            self.play(FadeIn(tag), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(rC[0]), FadeIn(rC[1]), run_time=0.9)
            seg.wait_until(seg.word(1, "The model says"))
            self.play(FadeIn(rC[2], scale=1.2), run_time=0.7)
            seg.wait_until(seg.word(1, "All of them at Alder"))
            self.play(FadeIn(rA[0]), FadeIn(rA[1]), run_time=0.8)
            self.play(FadeIn(rA[2], scale=1.2), run_time=0.6)

        with self.nar("s6_2") as seg:
            self.play(FadeIn(R.g), GrowFromCenter(dC), GrowFromCenter(dA), FadeIn(pcs), run_time=1.2)
            seg.wait_until(seg.word(0, "They are"))
            self.play(GrowFromCenter(brk), FadeIn(brl), run_time=0.8)
            seg.wait_until(seg.word(0, ", not"))
            self.play(FadeIn(b87), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(c87), run_time=0.6)
            seg.wait_until(seg.word(1, "compares two averages"))
            self.play(FadeIn(b69), FadeIn(c69), run_time=0.8)
            seg.wait_until(seg.s(2))
            self.play(FadeIn(moral), run_time=0.8)

        with self.nar("s6_3", gap=0.8) as seg:
            self.play(FadeIn(last, shift=UP * 0.1), run_time=0.9)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S07
class S07_Recap(EpisodeScene):
    def construct(self):
        tag = chapter_tag(5, "Recap")
        xs = (-4.45, 0.0, 4.45)
        cards = VGroup(*[card(4.05, 3.7).move_to([x, 0.15, 0]) for x in xs])
        icon1 = VGroup(Line([-0.8, -0.35, 0], [0.8, 0.2, 0], stroke_width=4.5, color=CEDAR), Line([-0.8, 0.1, 0], [0.8, 0.65, 0], stroke_width=4.5, color=ALDER),
                       DoubleArrow([0, -0.075, 0], [0, 0.375, 0], buff=0, stroke_width=3, color=ACCENT, tip_length=0.1))

        def f(t, shift):
            return 0.9 * expit(4 * (t - shift)) - 0.45

        def scurve(shift, color):
            return ParametricFunction(lambda t: np.array([t, f(t, shift), 0.0]), t_range=[-1.0, 1.0, 0.02], color=color, stroke_width=4)

        icon2 = VGroup(scurve(0.18, CEDAR), scurve(-0.18, ALDER),
                       Line([0, f(0, 0.18), 0], [0, f(0, -0.18), 0], stroke_width=4, color=ACCENT),
                       Line([-0.7, f(-0.7, 0.18), 0], [-0.7, f(-0.7, -0.18), 0], stroke_width=4, color=ACCENT))
        icon3 = VGroup(Line([-0.9, 0, 0], [0.9, 0, 0], stroke_width=4, color=PAPER), Dot([-0.25, 0, 0], radius=0.1, color=CEDAR), Dot([0.45, 0, 0], radius=0.1, color=ALDER),
                       DoubleArrow([-0.25, 0.3, 0], [0.45, 0.3, 0], buff=0, stroke_width=3, color=ACCENT, tip_length=0.1),
                       Triangle(fill_color=ACCENT, fill_opacity=1, stroke_width=0).scale(0.09).move_to([-0.7, -0.25, 0]))
        icons = [icon1, icon2, icon3]
        caps = [["A gap between gammas", "multiplies each patient's odds"], ["What that does to a probability", "depends on where the patient starts"],
                ["Gammas depend on where zero is.", "Gaps do not."]]
        captions = VGroup()
        for k, (ic, cp) in enumerate(zip(icons, caps)):
            ic.move_to([xs[k], 0.8, 0])
            captions.add(VGroup(*[txt(s, 19, PAPER) for s in cp]).arrange(DOWN, buff=0.1).move_to([xs[k], -0.85, 0]))
        with self.nar("s7_1") as seg:
            self.play(FadeIn(tag), run_time=0.8)
            for k in range(3):
                seg.wait_until(seg.s(k + 1) - 0.1)
                self.play(FadeIn(cards[k], shift=UP * 0.15), FadeIn(captions[k], shift=UP * 0.1), FadeIn(icons[k], shift=UP * 0.1), run_time=1.1)

        rough = side(f"{N['patients']} patients: every gap read today is rough", size=22, color=PAPER).move_to([0, -2.35, 0])
        P = LinePanel()
        b0, g0 = 1.2, {"Alder": -1.5, "Birch": -1.0, "Cedar": -0.7, "Dune": -2.0}        # the unfitted position Episode 4 drifted in from
        b = ValueTracker(BETA)
        g = {n: ValueTracker(G[n]) for n in FOUR}
        lines = {n: always_redraw(lambda n=n: P.line(g[n].get_value(), b.get_value(), COL[n])) for n in FOUR}
        dial, blab, sl, glab = controls(BETA, {**G, "Elm": -3.2})
        dial.add_updater(lambda m: m.turn_to(b.get_value()))
        for n in FOUR:
            sl[n].add_updater(lambda m, n=n: m.slide_to(g[n].get_value()))
        nxt = VGroup(txt("Next:", 26, MUTED), big("fitting by balance", size=34)).arrange(DOWN, buff=0.2).move_to([SX, -1.2, 0])
        with self.nar("s7_2") as seg:
            self.play(FadeIn(rough, shift=UP * 0.1), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeOut(VGroup(cards, captions, rough, *icons)), run_time=0.7)
            self.play(FadeIn(P.g), run_time=0.6)
            self.add(*lines.values())
            seg.wait_until(seg.s(2))
            self.play(FadeIn(dial), FadeIn(blab), FadeIn(glab), *[FadeIn(x) for x in sl.values()], run_time=0.8)
            self.play(b.animate.set_value(b0), *[g[n].animate.set_value(g0[n]) for n in FOUR], run_time=1.3)
            self.play(b.animate.set_value(BETA), *[g[n].animate.set_value(G[n]) for n in FOUR], FadeIn(nxt, shift=UP * 0.15), run_time=2.0)
        for m in [dial, *sl.values(), *lines.values()]:
            m.clear_updaters()
        end_card(self, "s7_3", 6, "Fitting by balance")
