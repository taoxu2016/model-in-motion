"""Model in Motion: the fitting machine (from Episode 6 on).

A gamma slider and an observed-minus-expected meter for every clinic, the beta dial with its own meter, and a
height bar for the log-likelihood. Everything is driven by ValueTrackers: move a slider or the dial and whatever
depends on it follows, computed with the same formulas the number files use.
"""
from mim.common import *  # noqa: F401,F403
from mim.kit import expit, logit, signed  # noqa: F401
from mim.lines import Dial, Slider


class Meter(VGroup):
    """A balance for observed minus expected. Observed sits on the left and goes down when it is the larger."""

    def __init__(self, color, width=1.05):
        super().__init__()
        self.w = width
        self.pivot = Triangle(fill_color=MUTED, fill_opacity=1, stroke_width=0).scale(0.1)
        self.beam = Line(LEFT * width / 2, RIGHT * width / 2, stroke_width=5, color=color)
        self.pan_o = Dot(radius=0.1, color=color)
        self.pan_e = Circle(radius=0.1, stroke_color=color, stroke_width=2.5).set_fill(INK, opacity=1)
        self.add(self.pivot, self.beam, self.pan_o, self.pan_e)
        self.tilt_to(0.0)

    def tilt_to(self, d):
        a = 0.5 * float(np.tanh(d / 3.0))                 # the angle saturates; the number printed below carries the value
        c = self.pivot.get_top() + UP * 0.04
        u = np.array([np.cos(a), np.sin(a), 0.0])
        left, right = c - u * self.w / 2, c + u * self.w / 2
        self.beam.put_start_and_end_on(left, right)
        self.pan_o.move_to(left)
        self.pan_e.move_to(right)
        return self


class HeightBar(VGroup):
    """A vertical bar whose level reads a height (the log-likelihood)."""

    def __init__(self, lo, hi, length=4.4, width=0.34):
        super().__init__()
        self.lo, self.hi, self.span = lo, hi, length
        self.track = Rectangle(width=width, height=length, stroke_color=FAINT, stroke_width=2, fill_color=INK_2, fill_opacity=1)
        self.fill = Rectangle(width=width - 0.08, height=0.02, stroke_width=0, fill_color=PAPER, fill_opacity=0.9)
        self.add(self.track, self.fill)
        self.level_to(lo)

    def Y(self, v):
        v = min(max(v, self.lo), self.hi)
        return float(self.track.get_bottom()[1] + self.span * (v - self.lo) / (self.hi - self.lo))

    def level_to(self, v):
        b = self.track.get_bottom()
        h = max(0.02, self.Y(v) - b[1])
        self.fill.stretch_to_fit_height(h)
        self.fill.move_to(b + UP * h / 2)
        return self


class FitMachine:
    """Sliders, meters, dial and height bar for the five-clinic cast, driven by the trackers g[clinic] and b."""
    XS = {"Alder": -5.6, "Birch": -4.0, "Cedar": -2.4, "Dune": -0.8, "Elm": 0.8}
    XB, XH = 3.0, 5.5

    def __init__(self, gammas, beta, height=(-70.5, -55.0), slider=(-3.2, 1.3)):
        self.g = {n: ValueTracker(gammas[n]) for n in ORDER}
        self.b = ValueTracker(beta)
        self.col, self.sl, self.meter, self.diff, self.expd, self.gval = {}, {}, {}, {}, {}, {}
        self._live = []
        for n in ORDER:
            x, c = self.XS[n], CLINICS[n]["color"]
            name = txt(n, 20, c, weight=SEMIBOLD).move_to([x, 2.85, 0])
            s = Slider(n, gammas[n], h=1.5, lo=slider[0], hi=slider[1], tag=False).move_to([x, 1.6, 0])
            s.slide_to(gammas[n])
            s.add_updater(lambda m, n=n: m.slide_to(self.g[n].get_value()))
            gv = DecimalNumber(gammas[n], num_decimal_places=2, include_sign=True, font_size=20, color=PAPER)
            gv.add_updater(lambda m, n=n, s=s: m.set_value(self.g[n].get_value()).next_to(s.track, DOWN, buff=0.16))
            mt = Meter(c).move_to([x, -0.55, 0])
            mt.add_updater(lambda m, n=n: m.tilt_to(self.O(n) - self.E(n)))
            df = DecimalNumber(0.0, num_decimal_places=2, include_sign=True, font_size=24, color=c)
            df.add_updater(lambda m, n=n, x=x: m.set_value(self.O(n) - self.E(n)).move_to([x, -1.3, 0]))
            ob = txt(f"observed {self.O(n)}", 14, MUTED).move_to([x, -1.8, 0])
            ex = VGroup(txt("expected", 14, MUTED), DecimalNumber(0.0, num_decimal_places=1, font_size=18, color=PAPER))
            ex.add_updater(lambda m, n=n, x=x: self._expected(m, self.E(n), x))
            for m in (gv, mt, df, ex):
                m.update()
            self._live += [s, gv, mt, df, ex]
            self.sl[n], self.meter[n], self.diff[n], self.expd[n], self.gval[n] = s, mt, df, ex, gv
            self.col[n] = VGroup(name, s, gv, mt, df, ob, ex)

        xb = self.XB
        self.blab = tex(r"\beta", 34, ACCENT).move_to([xb, 2.85, 0])
        self.dial = Dial(beta, r=0.5).move_to([xb, 1.6, 0])
        self.dial.turn_to(beta)
        self.dial.add_updater(lambda m: m.turn_to(self.b.get_value()))
        self.bval = DecimalNumber(beta, num_decimal_places=2, font_size=22, color=ACCENT)
        self.bval.add_updater(lambda m: m.set_value(self.b.get_value()).move_to([xb, 0.62, 0]))
        self.bnote = txt("higher-risk patients", 14, ACCENT).move_to([xb, 0.12, 0])
        self.bmeter = Meter(ACCENT).move_to([xb, -0.55, 0])
        self.bmeter.add_updater(lambda m: m.tilt_to(self.Ub()))
        self.bdiff = DecimalNumber(0.0, num_decimal_places=2, include_sign=True, font_size=24, color=ACCENT)
        self.bdiff.add_updater(lambda m: m.set_value(self.Ub()).move_to([xb, -1.3, 0]))
        self.bobs = txt(f"observed {self.O_high()}", 14, MUTED).move_to([xb, -1.8, 0])
        self.bexp = VGroup(txt("expected", 14, MUTED), DecimalNumber(0.0, num_decimal_places=1, font_size=18, color=PAPER))
        self.bexp.add_updater(lambda m: self._expected(m, self.E_high(), xb))
        self.dialcol = VGroup(self.blab, self.dial, self.bval, self.bnote, self.bmeter, self.bdiff, self.bobs, self.bexp)

        xh = self.XH
        self.hlab = txt("height", 20, PAPER, weight=SEMIBOLD).move_to([xh, 2.85, 0])
        self.hbar = HeightBar(*height).move_to([xh, 0.1, 0])
        self.hbar.add_updater(lambda m: m.level_to(self.loglik()))
        self.hval = DecimalNumber(0.0, num_decimal_places=2, font_size=22, color=PAPER)
        self.hval.add_updater(lambda m: m.set_value(self.loglik()).move_to([xh + 0.8, self.hbar.Y(self.loglik()), 0]))
        self.hsub = txt("log-likelihood", 13, MUTED).move_to([xh, -2.42, 0])
        self.heightcol = VGroup(self.hlab, self.hbar, self.hval, self.hsub)
        live = [self.dial, self.bval, self.bmeter, self.bdiff, self.bexp, self.hbar, self.hval]
        for m in live:
            m.update()
        self._live += live
        self.all = VGroup(*self.col.values(), self.dialcol, self.heightcol)

    @staticmethod
    def _expected(m, value, x):
        m[1].set_value(value)
        m.arrange(RIGHT, buff=0.1).move_to([x, -2.15, 0])

    # ---- the model, read off the trackers
    def p(self, n, high):
        return float(expit(self.g[n].get_value() + (self.b.get_value() if high else 0.0)))

    def O(self, n):
        return events(n)

    def E(self, n):
        c = CLINICS[n]
        return c["low"][0] * self.p(n, False) + c["high"][0] * self.p(n, True)

    def O_high(self):
        return sum(CLINICS[n]["high"][1] for n in ORDER)

    def E_high(self):
        return sum(CLINICS[n]["high"][0] * self.p(n, True) for n in ORDER)

    def Ub(self):
        """The dial's meter: observed minus expected among higher-risk patients."""
        return self.O_high() - self.E_high()

    def loglik(self):
        t = 0.0
        for n in ORDER:
            for high, key in ((False, "low"), (True, "high")):
                m, e = CLINICS[n][key]
                if m:
                    q = min(max(self.p(n, high), 1e-12), 1 - 1e-12)
                    t += e * np.log(q) + (m - e) * np.log(1 - q)
        return float(t)

    def clear(self):
        for m in self._live:
            m.clear_updaters()
