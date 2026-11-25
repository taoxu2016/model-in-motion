"""Model in Motion: shared identity, data and helpers (the logistic fixed-effect arc).

Series identity (unchanged from the Cox arc)
  palette   ink background, warm paper text, Okabe-Ito hues (colour-blind safe)
  type      Inter Display (titles), Inter (labels), Lora Italic (asides), LaTeX (maths)
  motifs    risk chips: one disc per patient, filled = event; a pale ring marks a higher-risk patient
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
from manim import *

# The episode being rendered. Its folder holds narration/, audio/, data/ and build/.
# Every episode file sets MIM_EPISODE to its own folder before importing this module.
if "MIM_EPISODE" not in os.environ:
    raise RuntimeError("MIM_EPISODE is not set: import mim.common from an episode file, or set it to an episode folder.")
ROOT = Path(os.environ["MIM_EPISODE"]).resolve()

# ---------------------------------------------------------------- palette
INK, INK_2 = "#0E1621", "#16212F"          # background, card panels
PAPER, MUTED, FAINT = "#F3EEE4", "#8C9AAB", "#33445A"
ALDER, BIRCH = "#E69F00", "#56B4E9"        # the two clinics that swap places (orange, sky blue)
CEDAR, DUNE, ELM = "#AEB9C6", "#CC79A7", "#3CC59A"
ACCENT = "#F0E442"                         # attention; beta in later episodes
GOOD, ALERT = "#3CC59A", "#E8705A"         # the better number, warnings
SANS, DISPLAY, SERIF = "Inter", "Inter Display", "Lora"

config.background_color = INK


def txt(s, size=24, color=PAPER, weight=NORMAL, font=SANS, slant=NORMAL):
    return Text(s, font=font, font_size=size, color=color, weight=weight, slant=slant)


def tex(s, size=34, color=PAPER):
    return MathTex(s, font_size=size, color=color)


def chapter_tag(number: int, title: str):
    n = txt(f"{number:02d}", 19, ACCENT, weight=SEMIBOLD)
    t = txt(title.upper(), 19, MUTED, weight=MEDIUM)
    return VGroup(n, t).arrange(RIGHT, buff=0.2).to_corner(UL, buff=0.42)


def logo_mark(scale=1.0):
    """The series mark: two lifelines (an event and an unfinished story) crossed by the yellow 'now' line."""
    a = Line([-1.0, 0.2, 0], [0.75, 0.2, 0], stroke_width=7, color=ALDER)
    dot = Dot(a.get_end(), radius=0.1, color=ALDER)
    b = Line([-1.0, -0.2, 0], [0.25, -0.2, 0], stroke_width=7, color=BIRCH)
    ring = Circle(radius=0.09, stroke_width=5, color=BIRCH).set_fill(INK, 1).move_to(b.get_end())
    scan = Line([0.0, -0.5, 0], [0.0, 0.5, 0], stroke_width=5, color=ACCENT)
    return VGroup(a, dot, b, ring, scan).scale(scale)


def wordmark(size=60):
    m1 = txt("Model", size, PAPER, weight=SEMIBOLD, font=DISPLAY)
    m2 = txt("in", size, ACCENT, font=SERIF, slant=ITALIC)
    m3 = txt("Motion", size, PAPER, weight=SEMIBOLD, font=DISPLAY)
    g = VGroup(m1, m2, m3).arrange(RIGHT, buff=0.22)
    m2.align_to(m1, DOWN)
    return g


def card(width, height):
    return RoundedRectangle(corner_radius=0.18, width=width, height=height, stroke_color=FAINT,
                            stroke_width=2, fill_color=INK_2, fill_opacity=1)


def arrow_label(left, right, size=19, color=MUTED):
    a, b = txt(left, size, color, font=SERIF, slant=ITALIC), txt(right, size, color, font=SERIF, slant=ITALIC)
    arr = Arrow(ORIGIN, RIGHT * 0.7, buff=0, stroke_width=2.5, color=color, max_tip_length_to_length_ratio=0.3)
    return VGroup(a, arr, b).arrange(RIGHT, buff=0.18)


# ---------------------------------------------------------------- the cast: five clinics, 103 patients
# (patients, readmitted) in each risk group; the blueprint's running example
CLINICS = {
    "Alder": dict(color=ALDER, low=(24, 8), high=(6, 5)),
    "Birch": dict(color=BIRCH, low=(6, 1), high=(24, 13)),
    "Cedar": dict(color=CEDAR, low=(10, 2), high=(10, 6)),
    "Dune": dict(color=DUNE, low=(6, 2), high=(6, 5)),
    "Elm": dict(color=ELM, low=(11, 0), high=(0, 0)),
}
ORDER = ["Alder", "Birch", "Cedar", "Dune", "Elm"]
LEAGUE = ["Elm", "Cedar", "Alder", "Birch", "Dune"]        # sorted by raw rate: 0, 40, 43, 47, 58 percent
JUMBLE = {"Alder": 3, "Birch": 7, "Cedar": 11, "Dune": 13, "Elm": 17}   # seeds for the unsorted trays
XS = [-5.4, -2.7, 0.0, 2.7, 5.4]                           # the five tray columns


def patients(name):
    """One dict per patient: lower-risk first, and within a risk group the readmitted ones first."""
    c, out = CLINICS[name], []
    for high, (n, e) in ((False, c["low"]), (True, c["high"])):
        out += [dict(high=high, event=k < e) for k in range(n)]
    return out


def size(name):
    return CLINICS[name]["low"][0] + CLINICS[name]["high"][0]


def events(name):
    return CLINICS[name]["low"][1] + CLINICS[name]["high"][1]


def rate(name):
    return events(name) / size(name)


def pct(x):
    return f"{int(round(100 * x))}%"


# ---------------------------------------------------------------- chips
def chip(color, event, r=0.105):
    c = Circle(radius=r, stroke_color=color, stroke_width=28 * r)
    c.set_fill(color, opacity=1.0 if event else 0.0)
    return c


class Unit(VGroup):
    """One patient: a chip (filled = readmitted), with a pale ring if the patient is higher-risk."""

    def __init__(self, color, event, high, r=0.14, show_ring=True):
        super().__init__()
        self.high, self.event = high, event
        self.ring = None
        if high:
            self.ring = Circle(radius=1.4 * r, stroke_color=PAPER, stroke_width=1.8 if r > 0.1 else 1.5)
            self.ring.set_fill(opacity=0)
            if not show_ring:
                self.ring.set_stroke(opacity=0)
            self.add(self.ring)
        self.chip = chip(color, event, r)
        self.add(self.chip)
        self.set_z_index(2)


def column_veil(x, opacity=0.78):
    """Dims one tray column without touching the (hollow) chips' own opacities."""
    return Rectangle(width=2.64, height=5.0, stroke_width=0, fill_color=INK, fill_opacity=opacity).move_to([x, 0.45, 0]).set_z_index(5)


class Tray:
    """A clinic in the five-across overview: a card of jumbled chips with its raw-rate bar underneath."""
    W, H = 2.4, 2.1

    def __init__(self, name, x, y=1.0, luck=False):
        c = CLINICS[name]
        self.name, self.color, self.x, self.y = name, c["color"], x, y
        self.pat = patients(name)
        n = len(self.pat)
        self.slot = np.random.default_rng(JUMBLE[name]).permutation(n)
        self.card = card(self.W, self.H).move_to([x, y, 0])
        self.label = txt(name, 26, self.color, weight=SEMIBOLD).next_to(self.card, UP, buff=0.16)
        self.chips = VGroup(*[chip(self.color, p["event"]).move_to(self.slot_pos(self.slot[k]))
                              for k, p in enumerate(self.pat)])
        self.ty = y - self.H / 2 - 0.36
        self.track = Rectangle(width=self.W, height=0.13, stroke_width=0, fill_color=FAINT, fill_opacity=1).move_to([x, self.ty, 0])
        e = events(name)
        self.fill = self.make_fill(e / n) if e else None
        dy = 0.28 if luck else 0.0
        self.pct_pos, self.count_pos = [x, self.ty - 0.52 - dy, 0], [x, self.ty - 0.98 - dy, 0]
        self.pct = self.pct_text(e / n)
        self.count = self.count_text(e, n)
        self.g = VGroup(*([self.card, self.label, self.chips, self.track, self.pct, self.count] + ([self.fill] if self.fill else [])))

    def slot_pos(self, s):
        return np.array([self.x + (s % 6 - 2.5) * 0.33, self.y + self.H / 2 - 0.36 - (s // 6) * 0.33, 0.0])

    def rate_x(self, r):
        return self.x - self.W / 2 + self.W * r

    def make_fill(self, r):
        w = max(self.W * r, 0.012)
        return Rectangle(width=w, height=0.13, stroke_width=0, fill_color=self.color, fill_opacity=1).move_to(
            [self.x - self.W / 2 + w / 2, self.ty, 0])

    def pct_text(self, r):
        return txt(pct(r), 34, PAPER, weight=SEMIBOLD, font=DISPLAY).move_to(self.pct_pos)

    def count_text(self, e, n):
        return txt(f"{e} of {n}", 19, MUTED).move_to(self.count_pos)


class BigTray:
    """Alder or Birch up close: 30 units, jumbled (10 x 3) or sorted into a lower-risk and a higher-risk block."""
    W, H = 6.2, 3.0

    def __init__(self, name, cx, cy=1.0, sorted_=False, r=0.14):
        c = CLINICS[name]
        self.name, self.color, self.cx, self.cy = name, c["color"], cx, cy
        self.pat = patients(name)
        self.slot = np.random.default_rng(JUMBLE[name]).permutation(len(self.pat))
        self.gidx, seen = [], {False: 0, True: 0}
        for p in self.pat:
            self.gidx.append(seen[p["high"]])
            seen[p["high"]] += 1
        self.card = card(self.W, self.H).move_to([cx, cy, 0])
        self.head = VGroup(txt(name, 30, self.color, weight=SEMIBOLD),
                           txt(f"{pct(rate(name))} readmitted", 22, MUTED)).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        self.head.next_to(self.card, UP, buff=0.16)
        self.units = [Unit(self.color, p["event"], p["high"], r, show_ring=sorted_) for p in self.pat]
        for k, u in enumerate(self.units):
            u.move_to(self.sorted_pos(k) if sorted_ else self.jumble_pos(k))
        self.group_labels = [txt("lower risk", 21, MUTED, font=SERIF, slant=ITALIC).move_to([cx - 1.55, cy + 1.2, 0]),
                             txt("higher risk", 21, MUTED, font=SERIF, slant=ITALIC).move_to([cx + 1.55, cy + 1.2, 0])]
        self.counts = [self._count(c["low"][0], cx - 1.55), self._count(c["high"][0], cx + 1.55)]

    def _count(self, n, x):
        g = VGroup(txt(str(n), 24, PAPER, weight=SEMIBOLD), txt("patients", 19, MUTED)).arrange(RIGHT, buff=0.14, aligned_edge=DOWN)
        return g.move_to([x, self.cy - 1.12, 0])

    def jumble_pos(self, k):
        s = self.slot[k]
        return np.array([self.cx + (s % 10 - 4.5) * 0.5, self.cy + 0.5 - (s // 10) * 0.5, 0.0])

    def sorted_pos(self, k):
        j, high = self.gidx[k], self.pat[k]["high"]
        gx = self.cx + (1.55 if high else -1.55)
        return np.array([gx + (j % 6 - 2.5) * 0.42, self.cy + 0.72 - (j // 6) * 0.42, 0.0])

    def block(self, high):
        return [u for u in self.units if u.high == high]

    def hits(self, high):
        return [u for u in self.units if u.high == high and u.event]

    def frame(self):
        return VGroup(self.card, self.head, *self.group_labels, *self.counts)

    def everything(self):
        return VGroup(self.card, self.head, *self.group_labels, *self.counts, *self.units)

    def veil(self, high):
        gx = self.cx + (1.55 if high else -1.55)
        return Rectangle(width=2.95, height=2.8, stroke_width=0, fill_color=INK_2, fill_opacity=0.84).move_to(
            [gx, self.cy + 0.02, 0]).set_z_index(5)


YA, YB = 1.75, -1.65            # heights of the two beams


class Beam:
    """A clinic as a balance beam marked 0-100%: each risk group is a pile of chips sitting at its own rate."""
    X0, X1 = -4.1, 5.1

    def __init__(self, name, y):
        c = CLINICS[name]
        self.name, self.y, self.color = name, y, c["color"]
        (nl, el), (nh, eh) = c["low"], c["high"]
        self.rate = {False: 100 * el / nl, True: 100 * eh / nh}
        self.weight = {False: nl, True: nh}
        self.balance = 100 * (el + eh) / (nl + nh)
        self.line = Line([self.X0, y, 0], [self.X1, y, 0], stroke_width=7, color=PAPER)
        self.ticks = VGroup(*[Line([self.X(p), y, 0], [self.X(p), y - (0.16 if p % 50 == 0 else 0.09), 0],
                                   stroke_width=2, color=MUTED) for p in range(0, 101, 10)])
        self.ends = VGroup(txt("0%", 18, MUTED).move_to([self.X0 - 0.4, y, 0]), txt("100%", 18, MUTED).move_to([self.X1 + 0.52, y, 0]))
        self.label = txt(name, 26, self.color, weight=SEMIBOLD).move_to([self.X0 - 1.5, y, 0])
        self.rate_labels = [txt(pct(self.rate[h] / 100), 22, PAPER, weight=MEDIUM).move_to([self.X(self.rate[h]), y - 0.42, 0])
                            for h in (False, True)]

    def X(self, p):
        return self.X0 + (self.X1 - self.X0) * p / 100

    def mid(self):
        return (self.rate[False] + self.rate[True]) / 2

    def mean_with(self, other):
        """Balance point if this clinic kept its two rates but carried the other clinic's patients."""
        w = other.weight
        return (w[False] * self.rate[False] + w[True] * self.rate[True]) / (w[False] + w[True])

    def pile_pos(self, high, j):
        return np.array([self.X(self.rate[high]) + (j % 6 - 2.5) * 0.27, self.y + 0.24 + (j // 6) * 0.27, 0.0])

    def unit_for(self, color, p, j):
        u = Unit(color, p["event"], p["high"], r=0.09, show_ring=True).move_to(self.pile_pos(p["high"], j))
        u.j = j
        return u

    def own_units(self):
        """This clinic's own patients as small units already sitting on the beam."""
        out, seen = [], {False: 0, True: 0}
        for p in patients(self.name):
            out.append(self.unit_for(self.color, p, seen[p["high"]]))
            seen[p["high"]] += 1
        return out

    def static(self):
        return VGroup(self.line, self.ticks, self.ends, self.label, *self.rate_labels)

    def pivot(self, at, color):
        return Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(0.17).next_to([self.X(at), self.y, 0], DOWN, buff=0.07)

    def follow(self, tri, f):
        tri.add_updater(lambda m: m.next_to([self.X(f.get_value()), self.y, 0], DOWN, buff=0.07))

    def balance_label(self, at, color):
        return txt(pct(at / 100), 26, color, weight=SEMIBOLD).move_to([self.X(at), self.y - 0.68, 0])

    def tilt_on(self, rig, f, g, mean):
        """Let `rig` (line, ticks, labels, piles) tip about the pivot at f: level only when f reaches the mean."""
        rest = rig.copy()

        def upd(m):
            fv = f.get_value()
            ang = g.get_value() * float(np.clip(1.1 * (mean - fv) / 100, -0.07, 0.07))
            m.become(rest.copy().rotate(-ang, about_point=[self.X(fv), self.y, 0]))
        rig.add_updater(upd)


# ---------------------------------------------------------------- narration sync
SPEC = json.loads((ROOT / "narration" / "narration.json").read_text())
SAY = {g["id"]: [s.get("say", s["text"]) for s in g["sentences"]] for sc in SPEC["scenes"] for g in sc["segments"]}
MANIFEST = json.loads((ROOT / "audio" / "manifest.json").read_text())


class _Segment:
    def __init__(self, narrator, sid, gap):
        self.n, self.id, self.gap = narrator, sid, gap
        self.info = MANIFEST[sid]
        self.dur = self.info["duration"]

    def __enter__(self):
        self.t0 = self.n.now()
        self.n.scene.add_sound(str(ROOT / self.info["file"]))
        self.n.log.append({"id": self.id, "start": round(self.t0, 4), "duration": self.dur})
        return self

    @property
    def elapsed(self):
        return self.n.now() - self.t0

    def s(self, k):                      # start offset of sentence k
        return self.info["sentences"][k]["start"]

    def e(self, k):                      # end offset of sentence k
        return self.info["sentences"][k]["end"]

    def word(self, k, fragment, nth=1):  # estimated offset of a phrase inside sentence k (by character position)
        sen = self.info["sentences"][k]
        ref = SAY[self.id][k] if fragment in SAY[self.id][k] else sen["text"]
        pos = -1
        for _ in range(nth):
            pos = ref.find(fragment, pos + 1)
            if pos < 0:
                break
        if pos < 0:
            print(f"[cue not found] {self.id}[{k}]: {fragment!r}")
            pos = 0
        return sen["start"] + pos / max(len(ref), 1) * (sen["end"] - sen["start"])

    def until(self, offset):             # seconds left until an offset (never negative)
        return max(0.0, offset - self.elapsed)

    def wait_until(self, offset):
        dt = offset - self.elapsed
        if dt > 1 / 30:
            self.n.scene.wait(dt)

    def __exit__(self, *exc):
        if exc[0] is None:
            self.wait_until(self.dur + self.gap)


class Narrator:
    def __init__(self, scene, gap=0.35):
        self.scene, self.gap, self.log = scene, gap, []

    def __call__(self, sid, gap=None):
        return _Segment(self, sid, self.gap if gap is None else gap)

    def now(self):
        return self.scene.renderer.time

    def save(self):
        out = ROOT / "build" / "timings"
        out.mkdir(parents=True, exist_ok=True)
        name = type(self.scene).__name__
        (out / f"{name}.json").write_text(json.dumps(
            {"scene": name, "duration": round(self.now(), 4), "segments": self.log}, indent=1))


class EpisodeScene(Scene):
    def setup(self):
        self.nar = Narrator(self)

    def tear_down(self):
        self.nar.save()
