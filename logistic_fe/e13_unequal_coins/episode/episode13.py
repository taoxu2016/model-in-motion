"""Model in Motion · The Logistic Fixed-Effect Model · Episode 13: Unequal Coins (is this count surprising for a reference clinic?).

ANIMATIC PASS. Every narration clip has its board. The compositions are meant to stay; most of the motion is still to come.

Render one scene:   manim -ql --media_dir build/media episode/episode13.py S04_Exact      (run from the episode folder)
Every scene reads audio/manifest.json; each `with self.nar("sX_Y") as seg:` block starts that voiceover clip and
holds the scene until the clip (plus a short gap) has finished.
Every number comes from e13_numbers.json, written by e13_numbers.py; none is typed here. In S08 the pile and its
p-value are rebuilt live at each gamma, with the same two functions the numbers file uses (mim.castfit).
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
from mim.castfit import CAST, coin_pmf, mid_p  # noqa: E402
from mim.piles import Hist, tail_colors  # noqa: E402

N = json.loads((ROOT / "e13_numbers.json").read_text())
REFD, CASTD, SIM, PMF, PARTIAL, EQUAL, DN, AL, PV, IV, RIV, CAL = (N[k] for k in ("reference", "cast", "sim", "pmf", "partial", "equal", "dune", "alder", "p_value", "interval", "ratio_interval", "calibration"))
REF, BETA, G = REFD["gamma"], N["fit"]["beta"], N["fit"]["gamma"]
P_LO, P_HI = REFD["p_low"], REFD["p_high"]
COL = {n: CLINICS[n]["color"] for n in ORDER}
SX = 4.55                                           # centre of the side column beside a histogram


def pct(p, places=0):
    return f"{100 * p:.{places}f}%"


def minus(v, places=2):
    return f"{v:.{places}f}".replace("-", "\u2212")


def prob(g):
    return 1.0 / (1.0 + float(np.exp(-g)))


def coins(name, g=REF):
    """One chance per patient: what each of a clinic's patients would face at level g."""
    return np.array([prob(g)] * CASTD[name]["low"] + [prob(g + BETA)] * CASTD[name]["high"])


def coin_row(ps, color, r, x0, dx, y):
    return VGroup(*[risk_chip(float(p), r=r, color=color).move_to([x0 + dx * k, y, 0]) for k, p in enumerate(ps)])


# =================================================================================== S01
class S01_ColdOpen(EpisodeScene):
    def construct(self):
        a = CASTD["Alder"]
        count = VGroup(VGroup(side("Alder observed", size=22, color=PAPER), big(str(a["observed"]), size=72, color=ALDER)).arrange(DOWN, buff=0.15), side("against", size=22),
                       VGroup(side("expected at the reference", size=22, color=PAPER), big(f"{a['expected']:.2f}", size=72, color=CEDAR)).arrange(DOWN, buff=0.15)).arrange(RIGHT, buff=0.7).move_to([0, 0.7, 0])
        luck = big("a real difference, or luck?", size=32, color=ACCENT).move_to([0, -1.5, 0])
        with self.nar("s1_1") as seg:
            self.play(FadeIn(count, scale=0.95), run_time=1.1)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(luck, shift=UP * 0.1), run_time=0.8)

        d = CASTD["Dune"]
        n0, e0, n1, e1 = CAST["Dune"]
        lo = VGroup(*[chip(DUNE, k < e0, 0.17) for k in range(n0)]).arrange(RIGHT, buff=0.14)
        hi = VGroup(*[chip(DUNE, k < e1, 0.17) for k in range(n1)]).arrange(RIGHT, buff=0.14)
        tray = VGroup(VGroup(lo, side("six lower-risk patients", size=16)).arrange(DOWN, buff=0.2), VGroup(hi, side("six higher-risk patients", size=16)).arrange(DOWN, buff=0.2)).arrange(RIGHT, buff=0.9).move_to([0, 0.5, 0])
        name = txt("Dune", 30, DUNE, weight=SEMIBOLD).next_to(tray, UP, buff=0.5)
        ask = side("what does luck look like?", size=22, color=ACCENT).move_to([0, 2.75, 0])
        with self.nar("s1_2") as seg:
            self.play(FadeOut(VGroup(count, luck)), FadeIn(ask), run_time=0.8)
            seg.wait_until(seg.word(1, "We'll start with Dune"))
            self.play(FadeIn(name), FadeIn(tray), run_time=1.0)

        figs = VGroup(*[VGroup(big(v, size=40, color=c), side(l, size=18, color=PAPER)).arrange(DOWN, buff=0.1) for v, l, c in
                        ((str(d["observed"]), "observed", DUNE), (f"{d['expected']:.1f}", "expected at the reference", CEDAR), (pct(d["raw"]), "readmitted: the highest raw rate", PAPER))]).arrange(RIGHT, buff=1.0).move_to([0, -1.35, 0])
        guess = big("is Dune unusual?", size=28, color=ACCENT).move_to([0, -2.6, 0])
        with self.nar("s1_3", gap=0.8) as seg:
            self.play(FadeIn(figs[0]), run_time=0.6)
            seg.wait_until(seg.word(0, "against 4.8 expected"))
            self.play(FadeIn(figs[1]), run_time=0.6)
            seg.wait_until(seg.word(0, "the highest raw rate"))
            self.play(FadeIn(figs[2]), run_time=0.6)
            seg.wait_until(seg.word(0, "So make a guess"))
            self.play(FadeIn(guess, shift=UP * 0.1), run_time=0.7)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S02
class S02_Title(EpisodeScene):
    def construct(self):
        title_card(self, "s2_1", 13, "Unequal Coins", "is this count surprising for a reference clinic?")


# =================================================================================== S03
class S03_Coins(EpisodeScene):
    def construct(self):
        tag = chapter_tag(1, "Twelve coins")
        xs = [-4.4 + 0.8 * k for k in range(12)]
        row = coin_row(coins("Dune"), DUNE, 0.3, xs[0], 0.8, 2.15)
        groups = VGroup(side(f"six lower-risk patients: {pct(P_LO)} each", size=17, color=PAPER).move_to([(xs[0] + xs[5]) / 2, 1.55, 0]),
                        side(f"six higher-risk patients: {pct(P_HI)} each", size=17, color=PAPER).move_to([(xs[6] + xs[11]) / 2, 1.55, 0]))
        with self.nar("s3_1") as seg:
            self.play(FadeIn(tag), run_time=0.7)
            seg.wait_until(seg.word(0, "Then each patient"))
            self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in row], lag_ratio=0.06), run_time=1.3)
            seg.wait_until(seg.word(1, "For the six lower-risk"))
            self.play(FadeIn(groups[0]), run_time=0.6)
            seg.wait_until(seg.word(1, "For the six higher-risk"))
            self.play(FadeIn(groups[1]), run_time=0.6)

        rounds = VGroup()
        for r, (flips, total) in enumerate(zip(SIM["first"], SIM["first_counts"])):
            y = 0.95 - 0.38 * r
            marks = VGroup(*[(Dot([xs[k], y, 0], radius=0.1, color=DUNE) if heads else Circle(radius=0.1, stroke_color=MUTED, stroke_width=2).move_to([xs[k], y, 0])) for k, heads in enumerate(flips)])
            rounds.add(VGroup(side(f"round {r + 1}", size=15).move_to([-5.75, y, 0]), marks, big(str(total), size=26, color=DUNE).move_to([5.45, y, 0])))
        with self.nar("s3_2") as seg:
            for r, cue in enumerate(((0, "Three readmissions"), (1, "Flip again"), (1, "And again"))):
                seg.wait_until(seg.word(*cue) - (0.9 if r == 0 else 0.0))
                self.play(FadeIn(rounds[r][0]), LaggedStart(*[FadeIn(m, scale=0.6) for m in rounds[r][1]], lag_ratio=0.04), run_time=0.8)
                self.play(FadeIn(rounds[r][2], scale=0.8), run_time=0.3)

        H = Hist(-4.6, 4.6, -2.4, -0.45, 12, 0.3)
        axis = H.axis()
        freq = {n: np.array(SIM["stages"][str(n)]) / n for n in (20, 200, SIM["rounds"])}
        bars = H.bars(freq[20], color=DUNE)
        counter = side("20 rounds", size=18, color=PAPER).move_to([4.6, -0.75, 0], aligned_edge=RIGHT)
        mean_x = H.x0 + H.step * (CASTD["Dune"]["expected"] + 0.5)
        mean = VGroup(DashedLine([mean_x, H.y0, 0], [mean_x, H.y1 + 0.05, 0], dash_length=0.08, stroke_width=2.5, color=ACCENT), txt(f"{CASTD['Dune']['expected']:.1f}", 17, ACCENT, weight=SEMIBOLD).move_to([mean_x, H.y1 + 0.25, 0])).set_z_index(5)
        luck = side("what luck looks like", size=18, color=ACCENT).move_to([-3.4, -0.75, 0])
        with self.nar("s3_3", gap=0.8) as seg:
            self.play(FadeIn(axis), FadeIn(bars), FadeIn(counter), run_time=0.9)
            for n, lab in ((200, "200 rounds"), (SIM["rounds"], f"{SIM['rounds']:,} rounds")):
                new = side(lab, size=18, color=PAPER).move_to([4.6, -0.75, 0], aligned_edge=RIGHT)
                self.play(Transform(bars, H.bars(freq[n], color=DUNE)), Transform(counter, new), run_time=1.0)
            self.play(FadeIn(mean), run_time=0.6)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(luck), run_time=0.7)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S04
class S04_Exact(EpisodeScene):
    def construct(self):
        tag = chapter_tag(2, "No need to flip")
        H = Hist(-5.6, 1.6, -2.2, 2.0, 12, 1.0)
        axis = H.axis()
        bars = H.bars(PARTIAL[0])
        ps = coins("Dune")
        none = VGroup(side("before any coin:", size=18, color=PAPER), side("the count is certainly zero", size=18, color=PAPER)).arrange(DOWN, buff=0.08).move_to([SX, 1.4, 0])
        with self.nar("s4_1") as seg:
            self.play(FadeIn(tag), FadeIn(axis), FadeIn(bars), FadeIn(none), run_time=1.3)

        coin = risk_chip(float(ps[0]), r=0.42, color=DUNE).move_to([SX - 0.9, 1.35, 0])
        num = Integer(1, font_size=40, color=PAPER)
        coin_l = VGroup(side("coin", size=20, color=PAPER), num, side(f"of {len(ps)}", size=20, color=PAPER)).arrange(RIGHT, buff=0.18).move_to([SX + 0.75, 1.35, 0])
        piece = Rectangle(width=H.step * 0.8, height=H.H(ps[0]), stroke_width=0, fill_color=ACCENT, fill_opacity=1).move_to([H.X(0), H.y1 - H.H(ps[0]) / 2, 0]).set_z_index(4)
        stays = side(f"stays: {pct(1 - ps[0])}", size=17, color=PAPER).move_to([SX, 0.15, 0])
        moves = side(f"moves one step right: {pct(ps[0])}", size=17, color=ACCENT).move_to([SX, -0.3, 0])
        with self.nar("s4_2") as seg:
            self.play(FadeOut(none), FadeIn(coin), FadeIn(coin_l), FadeIn(piece), run_time=0.8)
            seg.wait_until(seg.word(0, "One part stays"))
            self.play(FadeIn(stays), run_time=0.5)
            seg.wait_until(seg.word(0, "The other moves"))
            self.play(piece.animate.move_to([H.X(1), H.y0 + H.H(ps[0]) / 2, 0]), Transform(bars[0], H.bar(0, 1 - ps[0])), FadeIn(moves), run_time=1.1)
            self.remove(piece)
            bars.become(H.bars(PARTIAL[1]))
            self.play(FadeOut(stays), FadeOut(moves), run_time=0.3)
            for k in range(2, len(ps) + 1):
                num.set_value(k)
                coin_l.arrange(RIGHT, buff=0.18).move_to([SX + 0.75, 1.35, 0])
                self.play(Transform(bars, H.bars(PARTIAL[k])), Transform(coin, risk_chip(float(ps[k - 1]), r=0.42, color=DUNE).move_to([SX - 0.9, 1.35, 0])), run_time=0.3)

        Z = Hist(-5.6, 1.6, -2.2, 2.0, 12, 0.3)
        dune = PMF["Dune"]
        labels = VGroup(*[big(pct(dune[k]), size=22, color=PAPER).move_to([Z.X(k), Z.y0 + Z.H(dune[k]) + 0.25, 0]) for k in (5, 6, 7)])
        more = VGroup(Line([Z.X(8) - Z.step * 0.4, Z.y0 + 0.75, 0], [Z.X(12) + Z.step * 0.4, Z.y0 + 0.75, 0], stroke_width=2.5, color=ACCENT),
                      big(f"8 or more: {pct(sum(dune[8:]))}", size=20, color=ACCENT).move_to([Z.X(10), Z.y0 + 1.05, 0]))
        done = VGroup(side("after twelve coins:", size=18, color=PAPER), side("the exact pile, enlarged", size=18, color=PAPER)).arrange(DOWN, buff=0.08).move_to([SX, 0.3, 0])
        with self.nar("s4_3", gap=0.8) as seg:
            self.play(FadeOut(VGroup(coin, coin_l)), Transform(bars, Z.bars(dune)), FadeIn(done), run_time=1.2)
            for k, cue in enumerate(("the chance of exactly 5", "Of 6,", "Of 7,")):
                seg.wait_until(seg.word(0, cue))
                self.play(FadeIn(labels[k]), run_time=0.45)
            seg.wait_until(seg.word(0, "And of 8"))
            self.play(Create(more[0]), FadeIn(more[1]), run_time=0.6)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S05
class S05_Tail(EpisodeScene):
    def construct(self):
        tag = chapter_tag(3, "How surprising is seven?")
        H = Hist(-5.6, 1.6, -2.2, 2.0, 12, 0.3)
        dune, o = PMF["Dune"], CASTD["Dune"]["observed"]
        axis, bars = H.axis(), H.bars(dune)
        mark = H.marker(o, "Dune's 7", DUNE, H.y0 + H.H(dune[o]))
        tail = VGroup(side("7 or more", size=20, color=PAPER), big(pct(DN["tail"]), size=44, color=DUNE)).arrange(DOWN, buff=0.1).move_to([SX, 1.5, 0])
        self.play(FadeIn(tag), FadeIn(axis), FadeIn(bars), run_time=1.0)
        with self.nar("s5_1") as seg:
            self.play(FadeIn(mark), run_time=0.7)
            seg.wait_until(seg.word(0, "the chance of 7 or more"))
            self.play(Transform(bars, H.bars(dune, colors=tail_colors(o, 12, DUNE))), FadeIn(tail), run_time=0.9)

        h7 = H.H(dune[o])
        cut = Rectangle(width=H.step * 0.8, height=h7 / 2, stroke_color=DUNE, stroke_width=2, fill_color=INK, fill_opacity=1).move_to([H.X(o), H.y0 + 0.75 * h7, 0]).set_z_index(4)
        sums = VGroup(VGroup(side("half the bar at 7", size=17, color=PAPER), big(f"{DN['half']:.3f}", size=24)).arrange(RIGHT, buff=0.3),
                      VGroup(side("everything beyond", size=17, color=PAPER), big(f"{DN['beyond']:.3f}", size=24)).arrange(RIGHT, buff=0.3),
                      VGroup(side("together", size=17, color=PAPER), big(f"{DN['one_sided']:.3f}", size=28, color=DUNE)).arrange(RIGHT, buff=0.3)).arrange(DOWN, buff=0.18, aligned_edge=RIGHT).move_to([SX, 1.2, 0])
        twice = VGroup(tex(r"\times\, 2", 40, PAPER), tex("=", 40, PAPER), big(f"{DN['p']:.3f}", size=40, color=ACCENT)).arrange(RIGHT, buff=0.3).move_to([SX, -0.35, 0])
        midp = side("the mid-p, two-sided", size=15).next_to(twice, DOWN, buff=0.15)
        with self.nar("s5_2") as seg:
            self.play(FadeOut(tail), run_time=0.4)
            seg.wait_until(seg.word(0, "so we take only half"))
            self.play(FadeIn(cut), FadeIn(sums[0]), FadeIn(sums[1]), run_time=0.9)
            seg.wait_until(seg.word(0, "That brings it to"))
            self.play(FadeIn(sums[2]), run_time=0.6)
            seg.wait_until(seg.word(1, "so we double it"))
            self.play(FadeIn(twice), FadeIn(midp), run_time=0.8)

        verdict = VGroup(side("about 1 time in 6, by luck alone", size=18, color=PAPER), pill("Dune is not flagged", 22)).arrange(DOWN, buff=0.22).move_to([SX, -1.75, 0])
        with self.nar("s5_3", gap=0.8) as seg:
            self.play(Indicate(twice[2], color=ACCENT, scale_factor=1.15), run_time=0.8)
            seg.wait_until(seg.word(0, "About one time in six"))
            self.play(FadeIn(verdict[0]), run_time=0.6)
            seg.wait_until(seg.word(0, "Dune is not flagged"))
            self.play(FadeIn(verdict[1], scale=0.9), run_time=0.6)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S06
class S06_Alder(EpisodeScene):
    def construct(self):
        tag = chapter_tag(4, "Alder's thirty coins")
        ps, o = coins("Alder"), CASTD["Alder"]["observed"]
        row = coin_row(ps, ALDER, 0.125, -5.45, 0.3, 2.55)
        n0, n1 = CASTD["Alder"]["low"], CASTD["Alder"]["high"]
        groups = VGroup(side(f"{n0} at {pct(P_LO)}", size=16, color=PAPER).move_to([-5.45 + 0.3 * (n0 - 1) / 2, 2.2, 0]), side(f"{n1} at {pct(P_HI)}", size=16, color=PAPER).move_to([-5.45 + 0.3 * (n0 + (n1 - 1) / 2), 2.2, 0]))
        H = Hist(-5.6, 1.6, -2.2, 1.35, 18, 0.2)
        alder = PMF["Alder"]
        axis, bars = H.axis(every=2), H.bars(alder)
        mark = H.marker(o, "Alder's 13", ALDER, H.y0 + H.H(alder[o]))
        tail = VGroup(side("13 or more", size=19, color=PAPER), big(pct(AL["tail"], 1), size=36, color=ALDER)).arrange(DOWN, buff=0.08).move_to([SX, 1.75, 0])
        pval = VGroup(side("the p-value", size=19, color=PAPER), big(f"{AL['p']:.3f}", size=44, color=ACCENT)).arrange(DOWN, buff=0.08).move_to([SX, 0.45, 0])
        with self.nar("s6_1") as seg:
            self.play(FadeIn(tag), LaggedStart(*[FadeIn(c) for c in row], lag_ratio=0.02), FadeIn(groups), run_time=1.5)
            seg.wait_until(seg.word(0, "The pile centres"))
            self.play(FadeIn(axis), FadeIn(bars), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(mark), run_time=0.6)
            seg.wait_until(seg.word(1, "The chance of 13 or more"))
            self.play(Transform(bars, H.bars(alder, colors=tail_colors(o, 18, ALDER))), FadeIn(tail), run_time=0.8)
            seg.wait_until(seg.word(1, "and the p-value is"))
            self.play(FadeIn(pval), run_time=0.7)

        line = VGroup(side("the usual line: 0.05", size=17), pill("Alder is flagged", 22)).arrange(DOWN, buff=0.2).move_to([SX, -0.85, 0])
        line[1][0].set_stroke(ALERT, width=2.5)
        with self.nar("s6_2") as seg:
            self.play(FadeIn(line[0]), run_time=0.6)
            seg.wait_until(seg.word(0, "Alder is flagged"))
            self.play(FadeIn(line[1], scale=0.9), run_time=0.7)

        def summary(n):
            c = CASTD[n]
            flagged = n in N["flagged"]
            return VGroup(txt(n, 22, COL[n], weight=SEMIBOLD), side(f"{c['size']} patients, {pct(c['raw'])} readmitted", size=16, color=PAPER),
                          VGroup(big(f"p = {pct(PV[n], 1 if flagged else 0)}", size=24, color=PAPER), side("flagged" if flagged else "not flagged", size=17, color=ALERT if flagged else MUTED)).arrange(RIGHT, buff=0.25)).arrange(DOWN, buff=0.08)

        pair = VGroup(summary("Dune"), summary("Alder")).arrange(DOWN, buff=0.45).move_to([SX, 0.6, 0])
        room = side("twelve patients leave room for luck; thirty leave less", size=16, color=ACCENT)
        room = fit_width(room, 4.5).move_to([SX, -1.5, 0])
        with self.nar("s6_3") as seg:
            self.play(FadeOut(VGroup(tail, pval, line)), run_time=0.5)
            self.play(FadeIn(pair), run_time=0.9)
            seg.wait_until(seg.word(0, "Twelve patients leave"))
            self.play(FadeIn(room), run_time=0.7)

        rows = VGroup()
        for n in ORDER:
            flagged = n in N["flagged"]
            rows.add(VGroup(txt(n, 20, COL[n], weight=SEMIBOLD), big(f"{PV[n]:.3f}" if PV[n] < 0.1 else f"{PV[n]:.2f}", size=24, color=PAPER), side("flagged" if flagged else "", size=16, color=ALERT)).arrange(RIGHT, buff=0.35))
        table = VGroup(side("p-values", size=17), *rows).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([SX, 0.25, 0])
        zero = side("Elm's is its whole bar at zero", size=15)
        zero = fit_width(zero, 4.4).next_to(table, DOWN, buff=0.3)
        with self.nar("s6_4", gap=0.8) as seg:
            self.play(FadeOut(VGroup(pair, room)), FadeIn(table[0]), FadeIn(rows[0]), FadeIn(rows[3]), run_time=0.8)
            for k, cue in ((1, "Birch,"), (2, "Cedar,"), (4, "And Elm")):
                seg.wait_until(seg.word(0, cue))
                self.play(FadeIn(rows[k]), run_time=0.45)
            self.play(FadeIn(zero), run_time=0.5)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S07
class S07_Unequal(EpisodeScene):
    def construct(self):
        tag = chapter_tag(5, "Why unequal matters")
        ps, o = coins("Alder"), CASTD["Alder"]["observed"]
        mixed = coin_row(ps, ALDER, 0.12, -5.45, 0.29, 2.6)
        same = coin_row([AL["equal_chance"]] * len(ps), PAPER, 0.12, -5.45, 0.29, 2.15)
        row_l = VGroup(side("Alder's thirty: mixed", size=16, color=ALDER).move_to([3.5, 2.6, 0], aligned_edge=LEFT), side(f"thirty identical: {pct(AL['equal_chance'])} each", size=16, color=PAPER).move_to([3.5, 2.15, 0], aligned_edge=LEFT))
        H = Hist(-5.6, 1.6, -2.2, 1.35, 18, 0.2)
        axis = H.axis(every=2)
        true = H.bars(PMF["Alder"], color=ALDER, opacity=0.85)
        flat = H.bars(EQUAL["Alder"], color=PAPER, outline=True).set_z_index(4)
        mark = H.marker(o, "13", ALDER, H.y0 + H.H(max(PMF["Alder"][o], EQUAL["Alder"][o])))
        pv = VGroup(VGroup(side("mixed coins", size=18, color=ALDER), big(pct(AL["p"], 1), size=34, color=ALDER)).arrange(RIGHT, buff=0.35),
                    VGroup(side("identical coins", size=18, color=PAPER), big(pct(AL["p_equal"], 1), size=34, color=PAPER)).arrange(RIGHT, buff=0.35)).arrange(DOWN, buff=0.3, aligned_edge=RIGHT).move_to([SX, 0.75, 0])
        slips = side("above 5%: Alder slips under the bar", size=17, color=ACCENT)
        slips = fit_width(slips, 4.4).move_to([SX, -0.3, 0])
        with self.nar("s7_1") as seg:
            self.play(FadeIn(tag), FadeIn(mixed), FadeIn(row_l[0]), FadeIn(axis), FadeIn(true), FadeIn(mark), FadeIn(pv[0]), run_time=1.3)
            seg.wait_until(seg.word(0, "Swap Alder's thirty"))
            self.play(FadeIn(same), FadeIn(row_l[1]), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(LaggedStart(*[Create(b) for b in flat], lag_ratio=0.03), run_time=1.2)
            seg.wait_until(seg.word(1, "The p-value rises"))
            self.play(FadeIn(pv[1]), run_time=0.7)
            seg.wait_until(seg.word(1, "and Alder slips"))
            self.play(FadeIn(slips), run_time=0.6)

        spread = VGroup(side("how much the count varies", size=16), VGroup(big(f"{AL['variance']:.2f}", size=28, color=ALDER), side("against", size=16), big(f"{AL['variance_equal']:.2f}", size=28, color=PAPER)).arrange(RIGHT, buff=0.3)).arrange(DOWN, buff=0.12).move_to([SX, -1.5, 0])
        with self.nar("s7_2", gap=0.8) as seg:
            self.play(FadeIn(spread), run_time=0.9)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S08
class S08_Inside(EpisodeScene):
    def construct(self):
        tag = chapter_tag(6, "Turn the test inside out")
        o = CASTD["Alder"]["observed"]
        lo, hi = IV["Alder"]
        H = Hist(-5.6, 1.6, -1.15, 1.9, 26, 0.2)
        axis = H.axis(every=2)
        axis.remove(axis[2])                               # the gamma ruler sits under this histogram, so its axis label is left off
        g = ValueTracker(REF)
        pile = always_redraw(lambda: H.bars(coin_pmf(coins("Alder", g.get_value())), color=ALDER, opacity=0.85))
        mark = H.marker(o, "Alder's 13", ALDER, H.y0 + H.H(0.19))
        R = Ruler(-2.45, -2.0, 0.6, x0=-5.1, x1=1.2, ticks=[-2, -1.5, -1, -0.5, 0, 0.5], labels={v: minus(v, 1) for v in (-2, -1.5, -1, -0.5, 0, 0.5)}, title="gamma")
        knob = always_redraw(lambda: Triangle(color=ACCENT, fill_opacity=1, stroke_width=0).scale(0.15).rotate(PI).move_to(R.P(g.get_value(), 0.2)).set_z_index(6))
        ref_tick = VGroup(Line(R.P(REF, -0.02), R.P(REF, 0.42), stroke_width=4, color=CEDAR), txt("reference", 14, CEDAR, weight=SEMIBOLD).move_to(R.P(REF, 0.6) + LEFT * 0.45))
        p_live = DecimalNumber(mid_p(coin_pmf(coins("Alder")), o), num_decimal_places=3, font_size=48, color=ACCENT).move_to([SX, 0.75, 0])
        p_live.add_updater(lambda m: m.set_value(mid_p(coin_pmf(coins("Alder", g.get_value())), o)))
        g_live = DecimalNumber(REF, num_decimal_places=2, font_size=34, color=PAPER).move_to([SX + 0.65, 1.9, 0])
        g_live.add_updater(lambda m: m.set_value(g.get_value()))
        heads = VGroup(side("gamma", size=18, color=PAPER).move_to([SX - 0.75, 1.9, 0]), side("p-value for Alder's 13", size=17, color=PAPER).move_to([SX, 1.3, 0]))
        with self.nar("s8_1") as seg:
            self.play(FadeIn(tag), FadeIn(axis), FadeIn(mark), FadeIn(R.g), FadeIn(ref_tick), run_time=1.2)
            self.add(pile, knob)
            self.play(FadeIn(heads), FadeIn(p_live), FadeIn(g_live), run_time=0.8)

        edges = VGroup(*[VGroup(Line(R.P(v, -0.02), R.P(v, 0.3), stroke_width=4, color=ACCENT), big(minus(v) if v < 0 else f"+{v:.2f}", size=20, color=ACCENT).move_to(R.P(v, 0.55) + (RIGHT * 0.35 if v < 0 else ORIGIN))) for v in (lo, hi)])
        span = Line(R.P(lo, 0.0), R.P(hi, 0.0), stroke_width=9, color=ACCENT).set_z_index(4)
        name = VGroup(big("Alder's exact 95% interval", size=22), side("the reference lies just outside it", size=17, color=CEDAR)).arrange(DOWN, buff=0.12)
        name = fit_width(name, 4.5).move_to([SX, -0.55, 0])
        with self.nar("s8_2") as seg:
            seg.wait_until(seg.word(0, "Slide the gamma up"))
            self.play(g.animate.set_value(lo), run_time=0.7)
            self.play(FadeIn(edges[0]), run_time=0.3)
            self.play(g.animate.set_value(hi), run_time=3.0, rate_func=linear)
            self.play(FadeIn(edges[1]), Create(span), run_time=0.5)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(name[0]), run_time=0.6)
            seg.wait_until(seg.word(1, "The reference, at"))
            self.play(Indicate(ref_tick, color=CEDAR, scale_factor=1.25), FadeIn(name[1]), run_time=0.9)
        p_live.clear_updaters(); g_live.clear_updaters(); pile.clear_updaters(); knob.clear_updaters()

        AX = lambda r: -3.3 + 2.9 * r
        y_ax, ys = -1.9, {"Alder": 1.3, "Dune": 0.2, "Elm": -0.9}
        axis2 = VGroup(Line([AX(0), y_ax, 0], [AX(2.4), y_ax, 0], stroke_width=3, color=MUTED),
                       *[VGroup(Line([AX(v), y_ax, 0], [AX(v), y_ax - 0.1, 0], stroke_width=2, color=MUTED), txt(f"{v:g}", 16, MUTED).move_to([AX(v), y_ax - 0.3, 0])) for v in (0, 0.5, 1, 1.5, 2)],
                       side("observed, over expected at the reference", size=16).move_to([AX(1.2), y_ax - 0.64, 0]))
        one = VGroup(DashedLine([AX(1), y_ax, 0], [AX(1), 2.0, 0], dash_length=0.1, stroke_width=2.5, color=CEDAR), txt("the reference", 16, CEDAR, weight=SEMIBOLD).move_to([AX(1), 2.25, 0]))
        rows = {}
        for n in ("Alder", "Dune", "Elm"):
            y, (a, b), r = ys[n], RIV[n], N["ratio"][n]
            bar = VGroup(Line([AX(a), y, 0], [AX(b), y, 0], stroke_width=6, color=COL[n]), *[Line([AX(v), y - 0.13, 0], [AX(v), y + 0.13, 0], stroke_width=4, color=COL[n]) for v in (a, b)],
                         Dot([AX(r), y, 0], radius=0.12, color=PAPER).set_z_index(5))
            rows[n] = VGroup(txt(n, 22, COL[n], weight=SEMIBOLD).move_to([-6.2, y, 0], aligned_edge=LEFT), bar, big(f"{a:.2f} to {b:.2f}" if a > 0 else f"0 to {b:.2f}", size=24, color=COL[n]).move_to([5.3, y, 0]))
        sa, sb = N["shortcut_interval"]
        short = VGroup(Line([AX(sa), ys["Alder"] - 0.38, 0], [AX(sb), ys["Alder"] - 0.38, 0], stroke_width=3, color=MUTED),
                       fit_width(side(f"Episode 11's shortcut: {sa:.2f} to {sb:.2f}", size=14), 3.3).move_to([5.3, ys["Alder"] - 0.4, 0]))
        with self.nar("s8_3", gap=0.8) as seg:
            self.play(*[FadeOut(m) for m in (axis, mark, R.g, ref_tick, pile, knob, heads, p_live, g_live, edges, span, name)], run_time=0.6)
            self.play(FadeIn(axis2), FadeIn(one), FadeIn(rows["Alder"]), FadeIn(short), run_time=1.0)
            seg.wait_until(seg.word(0, "Dune's, between"))
            self.play(FadeIn(rows["Dune"]), run_time=0.6)
            self.play(FadeIn(rows["Elm"]), run_time=0.6)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S09
class S09_Trust(EpisodeScene):
    def construct(self):
        tag = chapter_tag(7, "What the p-value promises")
        setup = VGroup(big(f"{CAL['crowds']} simulated crowds", size=28), side("every provider truly equals the reference", size=20, color=PAPER), side(f"{CAL['tests']:,} tests", size=20, color=PAPER)).arrange(DOWN, buff=0.14).move_to([0, 1.75, 0])
        U, bx = 0.9, -3.4

        def gauge(label, value, color, y):
            b = Rectangle(width=U * 100 * value, height=0.38, stroke_width=0, fill_color=color, fill_opacity=1).move_to([bx + U * 100 * value / 2, y, 0])
            return VGroup(side(label, size=18, color=PAPER).next_to(b, LEFT, buff=0.25), b, big(pct(value, 1), size=30, color=color).next_to(b, RIGHT, buff=0.25))

        got = gauge("flagged", CAL["rate"], ACCENT, 0.2)
        want = gauge("promised", 0.05, MUTED, -0.5)
        small = side(f"among providers under 50 patients: {pct(CAL['small_rate'], 1)}", size=17).move_to([0, -1.4, 0])
        with self.nar("s9_1") as seg:
            self.play(FadeIn(tag), FadeIn(setup), run_time=1.2)
            seg.wait_until(seg.s(1))
            self.play(GrowFromEdge(got[1], LEFT), FadeIn(got[0]), FadeIn(got[2]), run_time=0.9)
            seg.wait_until(seg.word(1, "against the 5%"))
            self.play(GrowFromEdge(want[1], LEFT), FadeIn(want[0]), FadeIn(want[2]), FadeIn(small), run_time=0.9)

        def caution(lines, x):
            c = card(5.6, 2.3).move_to([x, -0.2, 0])
            return VGroup(c, VGroup(*[txt(s, 20, PAPER) for s in lines]).arrange(DOWN, buff=0.12).move_to(c))

        known = caution(["the dial and the reference", "are treated as known"], -3.2)
        notp = caution(["a p-value is not the chance", "that the clinic is ordinary"], 3.2)
        is_p = side("it is the chance of a count like this, if it were", size=20, color=ACCENT).move_to([0, -2.0, 0])
        with self.nar("s9_2", gap=0.8) as seg:
            self.play(FadeOut(VGroup(setup, got, want, small)), run_time=0.6)
            seg.wait_until(seg.word(0, "The test treats"))
            self.play(FadeIn(known), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(notp), run_time=0.8)
            seg.wait_until(seg.word(1, "It is the chance"))
            self.play(FadeIn(is_p), run_time=0.7)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S10
class S10_Recap(EpisodeScene):
    def construct(self):
        tag = chapter_tag(8, "Recap")
        xs = (-4.45, 0.0, 4.45)
        cards = VGroup(*[card(4.05, 3.7).move_to([x, 0.15, 0]) for x in xs])
        icon1 = VGroup(*[risk_chip(p, r=0.24, color=PAPER) for p in (P_LO, P_HI, P_LO, P_HI)]).arrange(RIGHT, buff=0.14)
        m = Hist(-1.1, 1.1, 0.0, 1.0, 12, 0.3)
        icon2 = m.bars(PMF["Dune"], colors=tail_colors(CASTD["Dune"]["observed"], 12, ACCENT))
        icon3 = VGroup(Line([-1.1, 0, 0], [1.1, 0, 0], stroke_width=3, color=MUTED), Line([-0.35, 0, 0], [0.75, 0, 0], stroke_width=8, color=ACCENT), Line([-0.75, -0.18, 0], [-0.75, 0.18, 0], stroke_width=4, color=CEDAR),
                       *[Line([v, -0.14, 0], [v, 0.14, 0], stroke_width=4, color=ACCENT) for v in (-0.35, 0.75)])
        icons = [icon1, icon2, icon3]
        caps = [["Like the reference: each patient", "is a coin with their own chance"], ["The count's distribution is exact;", "its tail gives the p-value"], ["Turned inside out, the same", "test gives an interval"]]
        captions = VGroup()
        for k, (ic, cp) in enumerate(zip(icons, caps)):
            ic.move_to([xs[k], 0.9, 0])
            captions.add(fit_width(VGroup(*[txt(s, 19, PAPER) for s in cp]).arrange(DOWN, buff=0.1), 3.6).move_to([xs[k], -0.85, 0]))
        with self.nar("s10_1") as seg:
            self.play(FadeIn(tag), run_time=0.8)
            for k in range(3):
                seg.wait_until(seg.s(k + 1) - 0.1)
                self.play(FadeIn(cards[k], shift=UP * 0.15), FadeIn(captions[k], shift=UP * 0.1), FadeIn(icons[k], shift=UP * 0.1), run_time=1.1)

        E = Hist(-5.4, -1.4, -1.0, 1.4, 12, 0.3)
        exact = VGroup(E.bars(PMF["Dune"]), Line([E.x0, E.y0, 0], [E.x1, E.y0, 0], stroke_width=3, color=MUTED), side("exact, coin by coin", size=18, color=PAPER).move_to([-3.4, -1.45, 0]))
        bell = ParametricFunction(lambda t: np.array([t, 0.9 * np.exp(-4.5 * t * t), 0.0]), t_range=[-0.8, 0.8, 0.02], color=PAPER, stroke_width=4)
        ruler = VGroup(Line([-0.8, 0, 0], [0.8, 0, 0], stroke_width=3, color=PAPER), *[Line([v, -0.12, 0], [v, 0.12, 0], stroke_width=3, color=PAPER) for v in (-0.8, -0.4, 0, 0.4, 0.8)])
        dice = VGroup(*[Dot(radius=0.07, color=PAPER) for _ in range(9)]).arrange_in_grid(cols=3, buff=0.16)
        sketches = VGroup(bell, ruler, dice).arrange(RIGHT, buff=0.7).move_to([3.0, 0.9, 0])
        quick = side("three quicker ways?", size=20, color=ACCENT).move_to([3.0, 0.0, 0])
        nxt = VGroup(txt("Next:", 26, MUTED), big("three shortcuts", size=34)).arrange(DOWN, buff=0.2).move_to([3.0, -1.35, 0])
        with self.nar("s10_2") as seg:
            self.play(FadeOut(VGroup(cards, captions, *icons)), run_time=0.7)
            self.play(FadeIn(exact), run_time=0.9)
            seg.wait_until(seg.word(0, "Are there quicker ways"))
            self.play(LaggedStart(*[FadeIn(s_) for s_ in sketches], lag_ratio=0.3), FadeIn(quick), run_time=1.2)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(nxt, shift=UP * 0.15), run_time=0.9)
        end_card(self, "s10_3", 14, "Three Shortcuts")
