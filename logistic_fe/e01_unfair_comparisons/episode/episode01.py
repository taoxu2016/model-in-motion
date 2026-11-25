"""Model in Motion · The Logistic Fixed-Effect Model · Episode 1: Unfair Comparisons (case mix and raw rates).

Render one scene:   manim -qh --media_dir build/media episode/episode01.py S04_LikeWithLike
Every scene reads audio/manifest.json; each `with self.nar("sX_Y") as seg:` block starts that
voiceover clip and holds the scene until the clip (plus a short gap) has finished.
All content stays above y = -3.0 so that burned-in captions never cover it.
"""
import sys
from pathlib import Path

import os  # noqa: E402

os.environ["MIM_EPISODE"] = str(Path(__file__).resolve().parents[1])   # this episode's folder
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))           # the repository root, for the shared mim package
from mim.common import *  # noqa: E402,F403


def pulse(mobs, k=1.3):
    return [m.animate(rate_func=there_and_back).scale(k) for m in mobs]


# =================================================================================== S01
class S01_ColdOpen(EpisodeScene):
    def construct(self):
        trays = {n: Tray(n, XS[k]) for k, n in enumerate(ORDER)}
        chips = [c for n in ORDER for c in trays[n].chips]
        hits = [c for n in ORDER for c, p in zip(trays[n].chips, trays[n].pat) if p["event"]]
        for c in hits:
            c.set_fill(opacity=0)
        question = txt("Which clinic is doing the best job?", 40, PAPER, weight=SEMIBOLD, font=DISPLAY).move_to(UP * 3.3)

        with self.nar("s1_1") as seg:
            self.play(LaggedStart(*[FadeIn(VGroup(trays[n].card, trays[n].label), shift=UP * 0.15) for n in ORDER],
                                  lag_ratio=0.18), run_time=1.8)
            seg.wait_until(seg.s(1))
            self.play(LaggedStart(*[GrowFromCenter(c) for c in chips], lag_ratio=0.012), run_time=2.4)
            seg.wait_until(seg.word(1, "Some of those"))
            self.play(LaggedStart(*[c.animate.set_fill(opacity=1) for c in hits], lag_ratio=0.03), run_time=2.0)
            seg.wait_until(seg.word(1, "Which clinic"))
            self.play(FadeIn(question, shift=UP * 0.15), run_time=1.0)

        leg = VGroup(VGroup(chip(PAPER, True, 0.1), txt("readmitted within 30 days", 20, MUTED)).arrange(RIGHT, buff=0.16),
                     VGroup(chip(PAPER, False, 0.1), txt("not readmitted", 20, MUTED)).arrange(RIGHT, buff=0.16)
                     ).arrange(RIGHT, buff=0.8).move_to([0, -2.5, 0])
        with self.nar("s1_2") as seg:
            self.play(FadeIn(leg, shift=UP * 0.1), run_time=0.8)
            seg.wait_until(seg.word(0, "A filled chip"))
            self.play(*pulse(hits, 1.35), run_time=1.0)

        def show(name, rt=0.9):
            t = trays[name]
            anims = [FadeIn(t.track), FadeIn(t.pct, shift=UP * 0.1), FadeIn(t.count)]
            if t.fill is not None:
                anims.append(GrowFromEdge(t.fill, LEFT))
            self.play(*anims, run_time=rt)

        with self.nar("s1_3") as seg:
            seg.wait_until(seg.word(0, "At Alder"))
            show("Alder", 1.2)
            for cue, name in (("Birch", "Birch"), ("Cedar", "Cedar"), ("Dune", "Dune"), ("And at Elm", "Elm")):
                seg.wait_until(seg.word(1, cue) - 0.1)
                show(name, 0.8)

        ranks = VGroup(*[txt(str(k + 1), 30, MUTED, weight=SEMIBOLD, font=DISPLAY).move_to([XS[k], -2.0, 0]) for k in range(5)])
        with self.nar("s1_4") as seg:
            self.play(*[trays[n].g.animate(path_arc=0.7).shift(RIGHT * (XS[LEAGUE.index(n)] - trays[n].x)) for n in ORDER],
                      FadeOut(question), FadeOut(leg), run_time=2.4)
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ranks], lag_ratio=0.15), run_time=1.0)
            seg.wait_until(seg.word(1, "Elm in first"))
            self.play(Indicate(trays["Elm"].pct, color=ACCENT, scale_factor=1.25), Indicate(ranks[0], color=ACCENT), run_time=0.8)
            seg.wait_until(seg.word(1, "Dune in last"))
            self.play(Indicate(trays["Dune"].pct, color=ACCENT, scale_factor=1.25), Indicate(ranks[4], color=ACCENT), run_time=0.8)
            seg.wait_until(seg.word(1, "Alder just ahead"))
            self.play(Indicate(trays["Alder"].pct, color=ACCENT, scale_factor=1.25),
                      Indicate(trays["Birch"].pct, color=ACCENT, scale_factor=1.25), run_time=1.0)

        veil = VGroup(*[column_veil(XS[k]) for k in (0, 1, 4)])
        swap = CurvedDoubleArrow([XS[2] + 0.45, -2.0, 0], [XS[3] - 0.45, -2.0, 0], angle=TAU / 5, color=ACCENT,
                                 stroke_width=4, tip_length=0.18)
        qm = txt("?", 34, ACCENT, weight=SEMIBOLD, font=DISPLAY).move_to([(XS[2] + XS[3]) / 2, -1.92, 0])
        with self.nar("s1_5", gap=0.7) as seg:
            seg.wait_until(seg.word(0, "But for those two"))
            self.play(FadeIn(veil), FadeOut(ranks), run_time=1.0)
            self.play(Create(swap), FadeIn(qm), run_time=1.1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)


# =================================================================================== S02
class S02_Title(EpisodeScene):
    def construct(self):
        mark = logo_mark(1.25)
        word = wordmark(64)
        head = VGroup(mark, word).arrange(RIGHT, buff=0.55).move_to(UP * 1.15)
        arc = txt("THE LOGISTIC FIXED-EFFECT MODEL  \u00b7  EPISODE 1", 22, MUTED, weight=MEDIUM).next_to(head, DOWN, buff=0.75)
        title = txt("Unfair Comparisons", 70, PAPER, weight=SEMIBOLD, font=DISPLAY).next_to(arc, DOWN, buff=0.32)
        sub = txt("case mix and raw rates", 32, MUTED, font=SERIF, slant=ITALIC).next_to(title, DOWN, buff=0.26)
        a, dot, b, ring, scan = mark
        with self.nar("s2_1", gap=0.6) as seg:
            self.play(Create(a), Create(b), run_time=1.0, rate_func=smooth)
            self.play(GrowFromCenter(dot), GrowFromCenter(ring), run_time=0.5)
            self.play(FadeIn(scan, shift=RIGHT * 0.6), Write(word, run_time=1.6), run_time=1.6)
            seg.wait_until(seg.s(1))
            self.play(LaggedStart(FadeIn(arc, shift=UP * 0.15), FadeIn(title, shift=UP * 0.2),
                                  FadeIn(sub, shift=UP * 0.15), lag_ratio=0.25), run_time=1.8)
        self.wait(0.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)


# =================================================================================== S03
class S03_CaseMix(EpisodeScene):
    def construct(self):
        tag = chapter_tag(1, "Who walked in the door")
        A, B = BigTray("Alder", -3.45), BigTray("Birch", 3.45)
        units = [u for T in (A, B) for u in T.units]
        highs = [u for u in units if u.high]
        key = VGroup(Unit(PAPER, False, True, r=0.11), txt("a ring marks a higher-risk patient", 21, MUTED)).arrange(RIGHT, buff=0.22)
        key.move_to([0, -1.05, 0])

        with self.nar("s3_1") as seg:
            self.play(FadeIn(tag), FadeIn(A.card), FadeIn(B.card), FadeIn(A.head, shift=UP * 0.1), FadeIn(B.head, shift=UP * 0.1),
                      run_time=1.2)
            self.play(LaggedStart(*[GrowFromCenter(u) for u in units], lag_ratio=0.02), run_time=1.8)

        with self.nar("s3_2") as seg:
            self.play(LaggedStart(*pulse(highs, 1.3), lag_ratio=0.05), run_time=3.0)
            seg.wait_until(seg.s(1) - 0.1)
            self.play(LaggedStart(*[u.ring.animate.set_stroke(opacity=1.0) for u in highs], lag_ratio=0.03),
                      FadeIn(key, shift=UP * 0.1), run_time=1.8)

        with self.nar("s3_3") as seg:
            self.play(LaggedStart(*[u.animate.move_to(T.sorted_pos(k)) for T in (A, B) for k, u in enumerate(T.units)],
                                  lag_ratio=0.008), run_time=2.6)
            self.play(*[FadeIn(lb, shift=UP * 0.08) for T in (A, B) for lb in T.group_labels], run_time=0.8)

        hlA = SurroundingRectangle(VGroup(*A.block(False)), color=ALDER, buff=0.14, corner_radius=0.12, stroke_width=3)
        hlB = SurroundingRectangle(VGroup(*B.block(True)), color=BIRCH, buff=0.14, corner_radius=0.12, stroke_width=3)
        with self.nar("s3_4") as seg:
            seg.wait_until(seg.word(0, "At Alder"))
            self.play(FadeIn(A.counts[0], shift=UP * 0.1), FadeIn(A.counts[1], shift=UP * 0.1), Create(hlA), run_time=1.2)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(B.counts[0], shift=UP * 0.1), FadeIn(B.counts[1], shift=UP * 0.1), Create(hlB), run_time=1.2)

        term = txt("case mix", 40, PAPER, weight=SEMIBOLD, font=DISPLAY).move_to([0, -1.5, 0])
        gloss = txt("the kind of patients a provider serves", 24, MUTED, font=SERIF, slant=ITALIC).next_to(term, DOWN, buff=0.22)
        with self.nar("s3_5", gap=0.6) as seg:
            seg.wait_until(seg.word(0, "case mix") - 0.2)
            self.play(FadeOut(key), FadeIn(term, shift=UP * 0.15), run_time=0.9)
            self.play(FadeIn(gloss), run_time=0.7)
        self.play(FadeOut(VGroup(term, gloss, hlA, hlB, tag)), run_time=0.7)


# =================================================================================== S04
ROWS = [-1.02, -1.58, -2.14]


def score_cell(e, n, x, y):
    f = txt(f"{e} of {n}", 22, MUTED)
    p = txt(pct(e / n), 36, PAPER, weight=SEMIBOLD, font=DISPLAY)
    g = VGroup(f, p).arrange(RIGHT, buff=0.3).move_to([x, y, 0])
    g.p = p
    return g


class S04_LikeWithLike(EpisodeScene):
    def construct(self):
        A, B = BigTray("Alder", -3.45, sorted_=True), BigTray("Birch", 3.45, sorted_=True)
        self.add(A.frame(), B.frame(), *A.units, *B.units)
        tag = chapter_tag(2, "Like with like")
        veil_hi, veil_lo = VGroup(A.veil(True), B.veil(True)), VGroup(A.veil(False), B.veil(False))
        lab = [txt(s, 23, MUTED, font=SERIF, slant=ITALIC).move_to([0, y, 0])
               for s, y in zip(("lower-risk patients", "higher-risk patients", "everyone"), ROWS)]
        a1, b1 = score_cell(8, 24, -3.45, ROWS[0]), score_cell(1, 6, 3.45, ROWS[0])
        a2, b2 = score_cell(5, 6, -3.45, ROWS[1]), score_cell(13, 24, 3.45, ROWS[1])
        a3, b3 = score_cell(13, 30, -3.45, ROWS[2]), score_cell(14, 30, 3.45, ROWS[2])

        def win(cell):
            self.play(cell.p.animate.set_color(GOOD), Flash(cell.p.get_center(), color=GOOD, flash_radius=0.55, line_length=0.12),
                      run_time=0.9)

        with self.nar("s4_1") as seg:
            self.play(FadeIn(tag), run_time=0.8)
            seg.wait_until(seg.word(0, "starting with"))
            self.play(FadeIn(veil_hi), FadeIn(lab[0], shift=UP * 0.1), run_time=1.0)

        with self.nar("s4_2") as seg:
            self.play(*pulse(A.hits(False)), run_time=0.9)
            self.play(FadeIn(a1, shift=UP * 0.1), run_time=0.7)
            seg.wait_until(seg.word(0, "At Birch"))
            self.play(*pulse(B.hits(False)), run_time=0.9)
            self.play(FadeIn(b1, shift=UP * 0.1), run_time=0.7)
            seg.wait_until(seg.s(1))
            win(b1)

        with self.nar("s4_3") as seg:
            self.play(FadeOut(veil_hi), FadeIn(veil_lo), FadeIn(lab[1], shift=UP * 0.1), run_time=1.0)
            seg.wait_until(seg.word(0, "Alder:"))
            self.play(*pulse(A.hits(True)), run_time=0.8)
            self.play(FadeIn(a2, shift=UP * 0.1), run_time=0.6)
            seg.wait_until(seg.word(0, "Birch:"))
            self.play(*pulse(B.hits(True)), run_time=0.8)
            self.play(FadeIn(b2, shift=UP * 0.1), run_time=0.6)
            seg.wait_until(seg.s(1))
            win(b2)

        box = SurroundingRectangle(VGroup(a3, lab[2], b3), color=ALERT, buff=0.13, corner_radius=0.12, stroke_width=3)
        with self.nar("s4_4") as seg:
            self.play(FadeOut(veil_lo), run_time=0.7)
            self.play(Indicate(b1.p, color=GOOD, scale_factor=1.3), run_time=0.9)
            seg.wait_until(seg.word(0, "Higher-risk patients do better"))
            self.play(Indicate(b2.p, color=GOOD, scale_factor=1.3), run_time=0.9)
            seg.wait_until(seg.s(1) + 0.3)
            self.play(FadeIn(lab[2], shift=UP * 0.1), FadeIn(a3, shift=UP * 0.1), FadeIn(b3, shift=UP * 0.1), run_time=1.0)
            seg.wait_until(seg.word(1, "it's Alder"))
            self.play(a3.p.animate.set_color(GOOD), Create(box), run_time=1.0)

        name = txt("Simpson's paradox", 30, PAPER, weight=SEMIBOLD, font=DISPLAY).move_to([0, -2.72, 0])
        with self.nar("s4_5", gap=0.6) as seg:
            seg.wait_until(seg.word(0, "This is Simpson"))
            self.play(FadeIn(name, shift=UP * 0.12), run_time=0.9)
        self.play(FadeOut(VGroup(name, box, a1, b1, a2, b2, a3, b3, *lab, tag)), run_time=0.8)


# =================================================================================== S05
class S05_Balance(EpisodeScene):
    def construct(self):
        A, B = BigTray("Alder", -3.45, sorted_=True), BigTray("Birch", 3.45, sorted_=True)
        frames = VGroup(A.frame(), B.frame())
        self.add(frames, *A.units, *B.units)
        tag = chapter_tag(3, "A balancing act")
        bA, bB = Beam("Alder", YA), Beam("Birch", YB)

        with self.nar("s5_1") as seg:
            self.play(FadeIn(tag), run_time=0.8)
            seg.wait_until(seg.word(0, "Give each clinic"))
            self.play(FadeOut(frames), run_time=0.8)
            self.play(Create(bA.line), Create(bB.line), FadeIn(bA.ticks), FadeIn(bB.ticks), FadeIn(bA.ends), FadeIn(bB.ends),
                      FadeIn(bA.label), FadeIn(bB.label), run_time=1.4)
            seg.wait_until(seg.s(1))
            moves = [Transform(u, bm.unit_for(T.color, T.pat[k], T.gidx[k]))
                     for T, bm in ((A, bA), (B, bB)) for k, u in enumerate(T.units)]
            self.play(LaggedStart(*moves, lag_ratio=0.01), run_time=2.6)
            self.play(*[FadeIn(lb, shift=UP * 0.08) for bm in (bA, bB) for lb in bm.rate_labels], run_time=0.8)

        fA, gA = ValueTracker(bA.mid()), ValueTracker(0.0)
        triA = bA.pivot(bA.mid(), ALDER)
        rigA = VGroup(bA.line, bA.ticks, *bA.rate_labels, *A.units)
        with self.nar("s5_2") as seg:
            seg.wait_until(seg.word(0, "the point where"))
            self.play(FadeIn(triA, shift=UP * 0.25), run_time=0.8)
            bA.follow(triA, fA)
            seg.wait_until(seg.word(0, "And that depends"))
            self.add(rigA)
            bA.tilt_on(rigA, fA, gA, bA.balance)
            self.play(gA.animate.set_value(1.0), run_time=1.0)

        labA = bA.balance_label(bA.balance, ALDER)
        with self.nar("s5_3") as seg:
            seg.wait_until(seg.word(0, "so its balance point"))
            self.play(fA.animate.set_value(bA.balance), run_time=2.2)
            rigA.clear_updaters()
            triA.clear_updaters()
            self.play(FadeIn(labA, shift=UP * 0.1), run_time=0.7)

        def shift_mark(high, y):
            x1, x2 = bA.X(bA.rate[high]), bB.X(bB.rate[high])
            top2 = bB.pile_pos(high, bB.weight[high] - 1)[1] + 0.22
            return VGroup(DashedLine([x1, YA - 0.62, 0], [x1, y, 0], dash_length=0.06, stroke_width=2, color=GOOD),
                          Arrow([x1, y, 0], [x2, y, 0], buff=0, stroke_width=3, color=GOOD, max_tip_length_to_length_ratio=0.09),
                          DashedLine([x2, y, 0], [x2, top2, 0], dash_length=0.06, stroke_width=2, color=GOOD))

        m_lo, m_hi = shift_mark(False, 0.5), shift_mark(True, 0.05)
        lower = txt("lower rates", 20, GOOD, font=SERIF, slant=ITALIC).move_to([-0.07, 0.28, 0])
        fB, gB = ValueTracker(bB.mid()), ValueTracker(0.0)
        triB = bB.pivot(bB.mid(), BIRCH)
        rigB = VGroup(bB.line, bB.ticks, *bB.rate_labels, *B.units)
        labB = bB.balance_label(bB.balance, BIRCH)
        with self.nar("s5_4") as seg:
            self.play(LaggedStart(Create(m_lo), Create(m_hi), lag_ratio=0.35), FadeIn(lower), run_time=2.2)
            seg.wait_until(seg.s(1))
            self.play(FadeOut(VGroup(m_lo, m_hi, lower)), FadeIn(triB, shift=UP * 0.25), run_time=0.8)
            bB.follow(triB, fB)
            self.add(rigB)
            bB.tilt_on(rigB, fB, gB, bB.balance)
            self.play(gB.animate.set_value(1.0), run_time=0.9)
            seg.wait_until(seg.word(1, "and that drags"))
            self.play(fB.animate.set_value(bB.balance), run_time=2.2)
            rigB.clear_updaters()
            triB.clear_updaters()
            self.play(FadeIn(labB, shift=UP * 0.1), run_time=0.7)

        t1 = VGroup(txt("where the piles sit:", 21, MUTED, font=SERIF, slant=ITALIC),
                    txt("performance", 22, PAPER, weight=SEMIBOLD)).arrange(RIGHT, buff=0.18)
        t2 = VGroup(txt("how heavy they are:", 21, MUTED, font=SERIF, slant=ITALIC),
                    txt("case mix", 22, PAPER, weight=SEMIBOLD)).arrange(RIGHT, buff=0.18)
        tags = VGroup(t1, t2).arrange(DOWN, buff=0.14, aligned_edge=RIGHT).to_corner(UR, buff=0.42)
        with self.nar("s5_5", gap=0.6) as seg:
            seg.wait_until(seg.word(0, "how well a clinic"))
            self.play(FadeIn(t1, shift=LEFT * 0.15), run_time=0.8)
            seg.wait_until(seg.word(0, "and who walked"))
            self.play(FadeIn(t2, shift=LEFT * 0.15), run_time=0.8)
        self.play(FadeOut(tags), FadeOut(tag), run_time=0.7)


# =================================================================================== S06
class S06_Trade(EpisodeScene):
    def construct(self):
        bA, bB = Beam("Alder", YA), Beam("Birch", YB)
        uA, uB = bA.own_units(), bB.own_units()
        triA, triB = bA.pivot(bA.balance, ALDER), bB.pivot(bB.balance, BIRCH)
        labA, labB = bA.balance_label(bA.balance, ALDER), bB.balance_label(bB.balance, BIRCH)
        self.add(bA.static(), bB.static(), *uA, *uB, triA, triB, labA, labB)
        tag = chapter_tag(4, "Trading patients")
        ghostA = VGroup(triA.copy().set_fill(opacity=0).set_stroke(MUTED, width=2, opacity=1), labA.copy().set_color(MUTED))
        ghostB = VGroup(triB.copy().set_fill(opacity=0).set_stroke(MUTED, width=2, opacity=1), labB.copy().set_color(MUTED))
        mA, mB = bA.mean_with(bB), bB.mean_with(bA)          # 73.3% and 24.2%

        def moved(u, beam):
            t = u.copy()
            t.chip.set_fill(opacity=0.45)                    # outcomes at the other clinic are hypothetical
            return t.move_to(beam.pile_pos(u.high, u.j))

        with self.nar("s6_1") as seg:
            self.play(FadeIn(tag), run_time=0.8)
            seg.wait_until(seg.word(0, "Imagine"))
            self.add(ghostA, ghostB)
            self.play(FadeOut(labA), FadeOut(labB), triA.animate.set_color(BIRCH), triB.animate.set_color(ALDER), run_time=0.7)
            self.play(LaggedStart(*[Transform(u, moved(u, bB), path_arc=-0.5) for u in uA],
                                  *[Transform(u, moved(u, bA), path_arc=-0.5) for u in uB], lag_ratio=0.006), run_time=3.0)

        y1, y2 = 0.52, -0.04

        def rowlabel(color, s, y):
            g = VGroup(chip(color, True, 0.09).set_fill(opacity=0.45), txt(s, 21, MUTED, font=SERIF, slant=ITALIC)).arrange(RIGHT, buff=0.18)
            return g.move_to([-3.3, y, 0])

        def cell(name, color, value, x, y, vcolor=PAPER):
            g = VGroup(txt(name, 21, color, weight=SEMIBOLD),
                       txt(pct(value / 100), 30, vcolor, weight=SEMIBOLD, font=DISPLAY)).arrange(RIGHT, buff=0.22, aligned_edge=DOWN)
            return g.move_to([x, y, 0])

        r1, r2 = rowlabel(BIRCH, "with Birch's patients", y1), rowlabel(ALDER, "with Alder's patients", y2)
        a1, b1 = cell("Alder", ALDER, mA, 1.1, y1), cell("Birch", BIRCH, bB.balance, 4.0, y1, GOOD)
        a2, b2 = cell("Alder", ALDER, bA.balance, 1.1, y2), cell("Birch", BIRCH, mB, 4.0, y2, GOOD)

        rigA = VGroup(bA.line, bA.ticks, *bA.rate_labels, *uB)
        fA, gA = ValueTracker(bA.balance), ValueTracker(0.0)
        newA = bA.balance_label(mA, BIRCH)
        with self.nar("s6_2") as seg:
            self.play(*[Indicate(lb, color=ACCENT, scale_factor=1.3) for lb in bA.rate_labels], run_time=1.0)
            seg.wait_until(seg.word(0, "But now it carries"))
            bA.follow(triA, fA)
            self.add(rigA)
            bA.tilt_on(rigA, fA, gA, mA)
            self.play(gA.animate.set_value(1.0), FadeIn(r1, shift=RIGHT * 0.15), run_time=0.9)
            seg.wait_until(seg.word(0, "and its balance point"))
            self.play(fA.animate.set_value(mA), run_time=2.4)
            rigA.clear_updaters()
            triA.clear_updaters()
            self.play(FadeIn(newA, shift=UP * 0.1), run_time=0.6)
            self.play(TransformFromCopy(newA, a1[1]), FadeIn(a1[0]), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(Indicate(ghostB[1], color=ACCENT, scale_factor=1.3), run_time=0.8)
            self.play(TransformFromCopy(ghostB[1], b1[1]), FadeIn(b1[0]), run_time=0.8)

        rigB = VGroup(bB.line, bB.ticks, *bB.rate_labels, *uA)
        fB, gB = ValueTracker(bB.balance), ValueTracker(0.0)
        newB = bB.balance_label(mB, ALDER)
        with self.nar("s6_3") as seg:
            bB.follow(triB, fB)
            self.add(rigB)
            bB.tilt_on(rigB, fB, gB, mB)
            self.play(gB.animate.set_value(1.0), FadeIn(r2, shift=RIGHT * 0.15), run_time=0.9)
            seg.wait_until(seg.word(0, "Its balance point"))
            self.play(fB.animate.set_value(mB), run_time=2.2)
            rigB.clear_updaters()
            triB.clear_updaters()
            self.play(FadeIn(newB, shift=UP * 0.1), run_time=0.6)
            self.play(TransformFromCopy(newB, b2[1]), FadeIn(b2[0]), run_time=0.8)
            seg.wait_until(seg.word(0, "where Alder had") - 0.2)
            self.play(Indicate(ghostA[1], color=ACCENT, scale_factor=1.3), run_time=0.7)
            self.play(TransformFromCopy(ghostA[1], a2[1]), FadeIn(a2[0]), run_time=0.8)

        colbox = SurroundingRectangle(VGroup(b1, b2), color=GOOD, buff=0.16, corner_radius=0.12, stroke_width=3)
        note = txt("raw league table: Alder ahead of Birch", 20, MUTED, font=SERIF, slant=ITALIC).to_corner(UR, buff=0.42)
        strike = Line(note.get_left() + LEFT * 0.08, note.get_right() + RIGHT * 0.08, color=ALERT, stroke_width=3)
        with self.nar("s6_4", gap=0.7) as seg:
            seg.wait_until(seg.word(0, "Birch comes out"))
            self.play(Create(colbox), run_time=1.0)
            seg.wait_until(seg.word(0, "The league table"))
            self.play(FadeIn(note), run_time=0.7)
            seg.wait_until(seg.word(0, "the wrong way"))
            self.play(Create(strike), run_time=0.7)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)


# =================================================================================== S07
class S07_Crowd(EpisodeScene):
    def construct(self):
        d = json.loads((ROOT / "data" / "crowd.json").read_text())
        rt, rr, rm = [np.array(d[k]) for k in ("rank_true", "rank_raw", "rank_mix")]
        N, L, x0, y0 = 200, 4.7, -5.3, -2.42

        def X(r):
            return x0 + (r + 0.5) / N * L

        def Y(r):
            return y0 + (r + 0.5) / N * L

        cols = color_gradient([GOOD, "#E6DFCF", ALERT], N)
        dots = VGroup(*[Dot([(i % 20 - 9.5) * 0.42, 1.95 - (i // 20) * 0.42, 0], radius=0.055, color=PAPER).set_z_index(3)
                        for i in range(N)])
        by_truth = [int(i) for i in np.argsort(rt)]
        tag = chapter_tag(5, "Two hundred providers")

        with self.nar("s7_1") as seg:
            self.play(FadeIn(tag), run_time=0.8)
            seg.wait_until(seg.word(0, "So let's zoom out"))
            self.play(LaggedStart(*[GrowFromCenter(dt) for dt in dots], lag_ratio=0.01), run_time=2.4)
            seg.wait_until(seg.word(1, "we know how good"))
            self.play(LaggedStart(*[dots[i].animate.set_color(cols[int(rt[i])]) for i in by_truth], lag_ratio=0.006), run_time=2.0)

        xaxis = Line([x0, y0, 0], [x0 + L, y0, 0], stroke_width=2, color=MUTED)
        yaxis = Line([x0, y0, 0], [x0, y0 + L, 0], stroke_width=2, color=MUTED)
        xl = arrow_label("truly better", "truly worse").move_to([x0 + L / 2, y0 - 0.33, 0])
        yl = arrow_label("lower raw rate", "higher").rotate(PI / 2).move_to([x0 - 0.33, y0 + L / 2, 0])
        with self.nar("s7_2") as seg:
            self.play(Create(xaxis), FadeIn(xl), *[dots[i].animate.move_to([X(rt[i]), y0 + 0.14, 0]) for i in range(N)], run_time=2.6)
            seg.wait_until(seg.s(1))
            self.play(Create(yaxis), FadeIn(yl), run_time=0.8)
            self.play(LaggedStart(*[dots[i].animate.move_to([X(rt[i]), Y(rr[i]), 0]) for i in by_truth], lag_ratio=0.004), run_time=2.6)

        diag = DashedLine([x0, y0, 0], [x0 + L, y0 + L, 0], dash_length=0.1, stroke_width=2.5, color=PAPER).set_stroke(opacity=0.75)
        rx = 3.3
        c_lab = txt("rank correlation", 22, MUTED).move_to([rx, 1.35, 0])
        c_val = txt("0.16", 84, PAPER, weight=SEMIBOLD, font=DISPLAY).move_to([rx, 0.4, 0])
        c_sub = txt("raw rate against true performance", 20, MUTED, font=SERIF, slant=ITALIC).move_to([rx, -0.5, 0])
        with self.nar("s7_3") as seg:
            seg.wait_until(seg.word(0, "the dots would hug"))
            self.play(Create(diag), run_time=1.2)
            seg.wait_until(seg.word(0, "a rank correlation"))
            self.play(FadeIn(c_lab), FadeIn(c_val, shift=UP * 0.15), FadeIn(c_sub), run_time=1.0)

        grid = VGroup(*[Line([x0 + k * L / 5, y0, 0], [x0 + k * L / 5, y0 + L, 0], stroke_width=1.5, color=FAINT) for k in range(1, 6)],
                      *[Line([x0, y0 + k * L / 5, 0], [x0 + L, y0 + k * L / 5, 0], stroke_width=1.5, color=FAINT) for k in range(1, 6)])
        blocks = VGroup(*[Square(L / 5, stroke_width=0, fill_color=PAPER, fill_opacity=0.1).move_to(
            [x0 + (k + 0.5) * L / 5, y0 + (k + 0.5) * L / 5, 0]) for k in range(5)])
        wrong = [i for i in range(N) if rt[i] // 40 != rr[i] // 40]
        w_val = txt(str(len(wrong)), 84, ALERT, weight=SEMIBOLD, font=DISPLAY).move_to([rx, 0.4, 0])
        w_lab = txt("of 200 providers", 22, MUTED).move_to([rx, -0.5, 0])
        w_sub = txt("land in the wrong fifth of the table", 20, MUTED, font=SERIF, slant=ITALIC).move_to([rx, -0.95, 0])
        with self.nar("s7_4") as seg:
            self.play(Create(grid), FadeIn(blocks), run_time=1.2)
            seg.wait_until(seg.word(0, "a hundred and forty-two") - 0.2)
            self.play(*[dots[i].animate.set_opacity(0.25) for i in wrong], FadeOut(VGroup(c_lab, c_val, c_sub)), run_time=1.0)
            self.play(FadeIn(w_val, shift=UP * 0.15), FadeIn(w_lab), FadeIn(w_sub), run_time=0.8)

        xl2 = arrow_label("healthier patients", "sicker patients").move_to([x0 + L / 2, y0 - 0.33, 0])
        m_lab = txt("rank correlation", 22, MUTED).move_to([rx, 1.35, 0])
        m_val = txt("0.58", 84, ACCENT, weight=SEMIBOLD, font=DISPLAY).move_to([rx, 0.4, 0])
        m_sub = txt("raw rate against case mix", 20, MUTED, font=SERIF, slant=ITALIC).move_to([rx, -0.5, 0])
        with self.nar("s7_5", gap=0.8) as seg:
            self.play(FadeOut(VGroup(grid, blocks, w_val, w_lab, w_sub)), *[dots[i].animate.set_opacity(1) for i in wrong], run_time=0.9)
            seg.wait_until(seg.word(0, "by how sick"))
            self.play(FadeOut(xl), FadeIn(xl2), *[dots[i].animate.move_to([X(rm[i]), Y(rr[i]), 0]) for i in range(N)], run_time=2.8)
            seg.wait_until(seg.word(1, "a correlation of"))
            self.play(FadeIn(m_lab), FadeIn(m_val, shift=UP * 0.15), FadeIn(m_sub), run_time=1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)


# =================================================================================== S08
class S08_Luck(EpisodeScene):
    def construct(self):
        luck = json.loads((ROOT / "data" / "luck.json").read_text())
        trays = {n: Tray(n, XS[LEAGUE.index(n)], luck=True) for n in ORDER}
        tag = chapter_tag(6, "And then there's luck")
        veil = VGroup(*[column_veil(XS[k]) for k in (1, 2, 3)])

        with self.nar("s8_1") as seg:
            self.play(FadeIn(tag), *[FadeIn(trays[n].g) for n in ORDER], run_time=1.4)
            seg.wait_until(seg.word(0, "Look at the two"))
            self.play(FadeIn(veil), run_time=0.9)

        with self.nar("s8_2") as seg:
            seg.wait_until(seg.word(0, "rests on twelve") - 0.2)
            self.play(Indicate(trays["Dune"].count, color=ACCENT, scale_factor=1.4), run_time=1.0)
            seg.wait_until(seg.word(0, "on eleven") - 0.3)
            self.play(Indicate(trays["Elm"].count, color=ACCENT, scale_factor=1.4), run_time=1.0)

        p0 = luck["p"]
        note = txt("an experiment: every patient, at every clinic, has the same 4-in-10 chance", 21, MUTED,
                   font=SERIF, slant=ITALIC).move_to([0, 2.98, 0])
        marks = VGroup(*[Line([trays[n].rate_x(p0), trays[n].ty + 0.2, 0], [trays[n].rate_x(p0), trays[n].ty - 0.2, 0],
                              stroke_width=2.5, color=ACCENT) for n in ORDER])
        visited = {n: [] for n in ORDER}
        ticks = VGroup()

        def deal(k, rt=0.34):
            anims = []
            for j, n in enumerate(ORDER):
                t, on = trays[n], luck["draws"][k][j]
                for c, flag in zip(t.chips, on):
                    target = 1.0 if flag else 0.0
                    if abs(c.get_fill_opacity() - target) > 0.5:
                        anims.append(c.animate.set_fill(opacity=target))
                e, r = sum(on), sum(on) / len(on)
                visited[n].append(r)
                t.pct.become(t.pct_text(r))
                t.count.become(t.count_text(e, len(on)))
                anims.append(Transform(t.bar, t.make_fill(r)))
                tick = Line([t.rate_x(r), t.ty + 0.13, 0], [t.rate_x(r), t.ty - 0.13, 0], stroke_width=2, color=PAPER)
                tick.set_stroke(opacity=0.65)
                ticks.add(tick)
                anims.append(FadeIn(tick))
            self.play(*anims, run_time=rt)

        with self.nar("s8_3", gap=0.3) as seg:
            self.play(FadeOut(veil), run_time=0.6)
            seg.wait_until(seg.word(0, "Suppose all five"))
            resets = [c.animate.set_fill(opacity=0) for n in ORDER for c in trays[n].chips if c.get_fill_opacity() > 0.5]
            for n in ORDER:
                trays[n].bar = trays[n].make_fill(0.0)
            self.add(*[trays[n].bar for n in ORDER])
            self.play(*resets, *[FadeOut(trays[n].fill) for n in ORDER if trays[n].fill is not None],
                      *[trays[n].pct.animate.set_opacity(0.25) for n in ORDER],
                      *[trays[n].count.animate.set_opacity(0.25) for n in ORDER], FadeIn(note), FadeIn(marks), run_time=1.2)
            seg.wait_until(seg.word(0, "Now deal out"))
            deal(0, 0.5)
            seg.wait_until(seg.word(0, "And again", 1))
            deal(1, 0.45)
            seg.wait_until(seg.word(0, "And again", 2))
            deal(2, 0.45)
            per = max(0.42, seg.until(seg.e(1)) / 9)
            for k in range(3, 12):
                deal(k, 0.26)
                self.wait(per - 0.26)

        def bracket(n):
            t, lo, hi, y = trays[n], min(visited[n]), max(visited[n]), trays[n].ty - 0.32
            return VGroup(Line([t.rate_x(lo), y, 0], [t.rate_x(hi), y, 0], stroke_width=3.5, color=ACCENT),
                          Line([t.rate_x(lo), y - 0.08, 0], [t.rate_x(lo), y + 0.08, 0], stroke_width=3.5, color=ACCENT),
                          Line([t.rate_x(hi), y - 0.08, 0], [t.rate_x(hi), y + 0.08, 0], stroke_width=3.5, color=ACCENT))

        with self.nar("s8_4", gap=0.8) as seg:
            br = {n: bracket(n) for n in ORDER}
            self.play(LaggedStart(*[Create(br[n]) for n in LEAGUE], lag_ratio=0.2), run_time=1.8)
            seg.wait_until(seg.word(0, "chance alone"))
            self.play(Indicate(br["Elm"], color=PAPER, scale_factor=1.08), Indicate(br["Dune"], color=PAPER, scale_factor=1.08), run_time=1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)


# =================================================================================== S09
class S09_Recap(EpisodeScene):
    def construct(self):
        tag = chapter_tag(7, "Recap")
        xs = (-4.45, 0.0, 4.45)
        cards = VGroup(*[card(4.05, 3.7).move_to([x, 0.15, 0]) for x in xs])

        # icon 1: a beam balancing a heavy pile and a light one
        beam = Line([-1.3, 0, 0], [1.3, 0, 0], stroke_width=5, color=PAPER)
        pile1 = VGroup(*[chip(ALDER, k < 3, 0.07).move_to([-0.75 + (k % 4 - 1.5) * 0.19, 0.14 + (k // 4) * 0.19, 0]) for k in range(8)])
        pile2 = VGroup(*[chip(ALDER, k < 1, 0.07).move_to([0.9 + (k - 0.5) * 0.19, 0.14, 0]) for k in range(2)])
        piv = Triangle(fill_color=ALDER, fill_opacity=1, stroke_width=0).scale(0.13).next_to([-0.42, 0, 0], DOWN, buff=0.05)
        icon1 = VGroup(beam, pile1, pile2, piv)
        # icon 2: three pairs of bars; the shorter bar wins twice for blue, then for orange
        icon2 = VGroup()
        for r, (a, b) in enumerate(((0.33, 0.17), (0.83, 0.54), (0.43, 0.47))):
            y = 0.62 - r * 0.62
            icon2.add(Rectangle(width=2.2 * a, height=0.14, stroke_width=0, fill_color=ALDER, fill_opacity=1).move_to([-1.1 + 1.1 * a, y + 0.1, 0]),
                      Rectangle(width=2.2 * b, height=0.14, stroke_width=0, fill_color=BIRCH, fill_opacity=1).move_to([-1.1 + 1.1 * b, y - 0.1, 0]),
                      Dot([-1.1 + 2.2 * min(a, b) + 0.17, y + (0.1 if a < b else -0.1), 0], radius=0.06, color=GOOD))
        icon2.add(DashedLine([-1.2, -0.31, 0], [1.2, -0.31, 0], dash_length=0.06, stroke_width=1.5, color=MUTED))
        # icon 3: a short track with widely scattered ticks
        tr = Line([-1.2, 0, 0], [1.2, 0, 0], stroke_width=5, color=FAINT)
        tk = VGroup(*[Line([x, 0.17, 0], [x, -0.17, 0], stroke_width=2.5, color=PAPER).set_stroke(opacity=0.75)
                      for x in (-0.95, -0.6, -0.42, -0.1, 0.05, 0.3, 0.52, 0.85, 1.05)])
        brk = VGroup(Line([-0.95, -0.38, 0], [1.05, -0.38, 0], stroke_width=3.5, color=ACCENT),
                     Line([-0.95, -0.46, 0], [-0.95, -0.3, 0], stroke_width=3.5, color=ACCENT),
                     Line([1.05, -0.46, 0], [1.05, -0.3, 0], stroke_width=3.5, color=ACCENT))
        few = VGroup(*[chip(DUNE, k in (0, 3), 0.07).move_to([(k - 2.5) * 0.2, 0.5, 0]) for k in range(6)])
        icon3 = VGroup(tr, tk, brk, few)
        icons = [icon1, icon2, icon3]
        caps = [["A raw rate blends", "performance with case mix"],
                ["Compare like with like,", "and a ranking can flip"],
                ["Small providers", "swing with chance"]]
        captions = VGroup()
        for k, (ic, cp) in enumerate(zip(icons, caps)):
            ic.move_to([xs[k], 0.8, 0])
            captions.add(VGroup(*[txt(s, 21, PAPER) for s in cp]).arrange(DOWN, buff=0.1).move_to([xs[k], -0.85, 0]))

        with self.nar("s9_1") as seg:
            self.play(FadeIn(tag), run_time=0.8)
            for k in range(3):
                seg.wait_until(seg.s(k + 1) - 0.1)
                self.play(FadeIn(cards[k], shift=UP * 0.15), FadeIn(captions[k], shift=UP * 0.1), FadeIn(icons[k], shift=UP * 0.1),
                          run_time=1.1)

        pool = [Unit(MUTED, k in (1, 4, 6, 11), k % 2 == 1, r=0.11) for k in range(12)]
        for k, u in enumerate(pool):
            u.move_to([(k % 6 - 2.5) * 0.36, 2.3 - (k // 6) * 0.36, 0])
        cA, cB = card(3.4, 1.7).move_to([-3.3, -0.75, 0]), card(3.4, 1.7).move_to([3.3, -0.75, 0])
        nA = txt("Alder", 26, ALDER, weight=SEMIBOLD).next_to(cA, UP, buff=0.14)
        nB = txt("Birch", 26, BIRCH, weight=SEMIBOLD).next_to(cB, UP, buff=0.14)
        same = txt("the same patients", 22, MUTED, font=SERIF, slant=ITALIC).move_to([0, 1.35, 0])
        with self.nar("s9_2") as seg:
            self.play(FadeOut(VGroup(cards, captions, *icons)), run_time=0.8)
            self.play(LaggedStart(*[GrowFromCenter(u) for u in pool], lag_ratio=0.04), FadeIn(cA), FadeIn(cB), FadeIn(nA), FadeIn(nB),
                      run_time=1.4)
            seg.wait_until(seg.word(0, "as if they had all"))
            copyA, copyB = VGroup(*[u.copy() for u in pool]), VGroup(*[u.copy() for u in pool])
            self.add(copyA, copyB)
            self.play(copyA.animate.move_to(cA.get_center()), copyB.animate.move_to(cB.get_center()), FadeIn(same), run_time=1.6)
            seg.wait_until(seg.s(1))
            lows, highs = [u for u in pool if not u.high], [u for u in pool if u.high]
            self.play(FadeOut(VGroup(cA, cB, nA, nB, copyA, copyB, same)),
                      *[u.animate.move_to([-1.3 + (j % 3 - 1) * 0.36, 1.5 - (j // 3) * 0.36, 0]) for j, u in enumerate(lows)],
                      *[u.animate.move_to([1.3 + (j % 3 - 1) * 0.36, 1.5 - (j // 3) * 0.36, 0]) for j, u in enumerate(highs)],
                      run_time=1.4)
            seg.wait_until(seg.word(1, "But real patients"))
            hero = highs[0]
            big = Unit(PAPER, True, True, r=0.3).move_to([0, 0.75, 0])
            big.chip.set_stroke(width=6)
            big.ring.set_stroke(width=2.5)
            self.play(FadeOut(VGroup(*[u for u in pool if u is not hero])), Transform(hero, big), run_time=1.0)
            spots = [(-3.6, 2.0), (3.6, 2.0), (-4.4, 0.75), (4.4, 0.75), (-3.6, -0.5), (3.6, -0.5)]
            words = ["age 81", "diabetes", "lives alone", "third stay this year", "kidney disease", "twelve medicines"]
            pills, links = VGroup(), VGroup()
            for (x, y), w in zip(spots, words):
                t = txt(w, 21, PAPER)
                box = RoundedRectangle(corner_radius=0.16, width=t.width + 0.5, height=0.52, stroke_color=FAINT, stroke_width=2,
                                       fill_color=INK_2, fill_opacity=1)
                pills.add(VGroup(box, t).move_to([x, y, 0]))
                start = np.array([0, 0.75, 0])
                end = np.array([x - np.sign(x) * (t.width / 2 + 0.3), y, 0])
                links.add(Line(start + 0.5 * (end - start) / np.linalg.norm(end - start), end, stroke_width=1.5, color=FAINT))
            self.play(LaggedStart(*[AnimationGroup(Create(ln), FadeIn(pl, shift=(pl.get_center() - np.array([0, 0.75, 0])) * 0.08))
                                    for ln, pl in zip(links, pills)], lag_ratio=0.22), run_time=2.6)

        ry, rx0, rx1 = -1.75, -4.2, 4.2
        ruler = Line([rx0, ry, 0], [rx1, ry, 0], stroke_width=6, color=PAPER)
        rticks = VGroup(*[Line([rx0 + (rx1 - rx0) * p / 10, ry, 0], [rx0 + (rx1 - rx0) * p / 10, ry - (0.16 if p % 5 == 0 else 0.09), 0],
                               stroke_width=2, color=MUTED) for p in range(11)])
        rl = VGroup(txt("0%", 18, MUTED).move_to([rx0 - 0.4, ry, 0]), txt("100%", 18, MUTED).move_to([rx1 + 0.52, ry, 0]))
        px = rx0 + (rx1 - rx0) * 0.7
        land = Unit(PAPER, True, True, r=0.14).move_to([px, ry + 0.34, 0])
        pv = txt("70%", 30, ACCENT, weight=SEMIBOLD, font=DISPLAY).move_to([px, ry - 0.52, 0])
        nxt = VGroup(txt("Next:", 28, MUTED), txt("odds and the S-curve", 40, PAPER, weight=SEMIBOLD, font=DISPLAY)).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        nxt.move_to([0, 1.2, 0])
        with self.nar("s9_3") as seg:
            seg.wait_until(seg.word(0, "a single ruler"))
            self.play(Create(ruler), FadeIn(rticks), FadeIn(rl), run_time=1.2)
            seg.wait_until(seg.word(0, "a way to turn"))
            self.play(*[pl.animate.move_to([0, 0.75, 0]).scale(0.2).set_opacity(0) for pl in pills], FadeOut(links), run_time=1.2)
            self.remove(pills)
            self.play(Transform(hero, land, path_arc=-0.6), run_time=1.3)
            self.play(FadeIn(pv, shift=UP * 0.1), FadeIn(nxt, shift=UP * 0.15), run_time=0.9)

        mark, word = logo_mark(1.0), wordmark(54)
        head = VGroup(mark, word).arrange(RIGHT, buff=0.5).move_to(UP * 0.7)
        ep2 = txt("NEXT  \u00b7  EPISODE 2  \u00b7  ODDS AND THE S-CURVE", 22, MUTED, weight=MEDIUM).next_to(head, DOWN, buff=0.6)
        thanks = txt("thanks for following the story", 28, PAPER, font=SERIF, slant=ITALIC).next_to(ep2, DOWN, buff=0.45)
        with self.nar("s9_4", gap=1.8) as seg:
            self.play(FadeOut(VGroup(ruler, rticks, rl, hero, pv, nxt, tag)), run_time=0.7)
            self.play(FadeIn(head, shift=UP * 0.15), FadeIn(ep2), run_time=1.0)
            self.play(FadeIn(thanks, shift=UP * 0.1), run_time=0.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
