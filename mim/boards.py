"""Model in Motion: board helpers shared from Episode 5 on.

Text styles, tick and cross marks, the control strip (beta dial and gamma sliders), dimension brackets,
and the standard title and end cards. Episode 4 still carries its own copies of some of these.
"""
from mim.common import *  # noqa: F401,F403
from mim.kit import *  # noqa: F401,F403
from mim.lines import *  # noqa: F401,F403

SX = 4.6                                    # centre of the right-hand strip (dial, sliders, notes)


def side(s, x=0.0, y=0.0, size=21, color=MUTED):
    """An aside in the serif italic. The serif face has no Greek: spell gamma and beta out here."""
    return txt(s, size, color, font=SERIF, slant=ITALIC).move_to([x, y, 0])


def big(s, x=0.0, y=0.0, size=32, color=PAPER):
    return txt(s, size, color, weight=SEMIBOLD, font=DISPLAY).move_to([x, y, 0])


def fit_width(m, w):
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def tick_mark(color=GOOD, s=1.0):
    return VGroup(Line([-0.14 * s, 0, 0], [-0.04 * s, -0.12 * s, 0], stroke_width=5, color=color),
                  Line([-0.04 * s, -0.12 * s, 0], [0.16 * s, 0.14 * s, 0], stroke_width=5, color=color))


def cross_mark(color=ALERT, s=1.0):
    return VGroup(Line([-0.12 * s, -0.12 * s, 0], [0.12 * s, 0.12 * s, 0], stroke_width=5, color=color),
                  Line([-0.12 * s, 0.12 * s, 0], [0.12 * s, -0.12 * s, 0], stroke_width=5, color=color))


def clear(scene, keep=()):
    """Fade-outs for everything on screen except `keep`."""
    return [FadeOut(m) for m in scene.mobjects if m not in keep]


def ring_at(point, color):
    return Circle(radius=0.09, stroke_color=color, stroke_width=3).set_fill(INK, opacity=1).move_to(point).set_z_index(5)


def dim_bracket(P, t, v0, v1, dx, label):
    """A dimension line beside panel position t, from height v0 to v1, with leaders back to the exact position."""
    x = P.X(t) + dx
    a, b = np.array([x, P.Y(v0), 0.0]), np.array([x, P.Y(v1), 0.0])
    arr = DoubleArrow(a, b, buff=0, stroke_width=3, color=ACCENT, tip_length=0.12)
    lead = VGroup(*[DashedLine(P.P(t, v), np.array([x, P.Y(v), 0.0]), dash_length=0.05, stroke_width=1.5, color=ACCENT) for v in (v0, v1)])
    lab = txt(label, 22, ACCENT, weight=SEMIBOLD).next_to(arr, LEFT if dx < 0 else RIGHT, buff=0.12)
    lab.add_background_rectangle(color=INK, opacity=0.85, buff=0.05)
    return VGroup(lead, arr, lab).set_z_index(6)


def controls(beta, gammas, lo=-3.2, hi=0.4):
    """The machine, in the top band of the right strip: one beta dial and one gamma slider per clinic."""
    dial = Dial(beta).move_to([3.15, 1.75, 0])
    dial.turn_to(beta)
    blab = tex(r"\beta", 36, ACCENT).next_to(dial, UP, buff=0.22)
    sl = {}
    for k, n in enumerate(ORDER):
        sl[n] = Slider(n, gammas[n], lo=lo, hi=hi).move_to([4.1 + 0.65 * k, 1.62, 0])
        sl[n].slide_to(gammas[n])
    glab = tex(r"\gamma", 36, PAPER).move_to([5.4, 3.05, 0])
    return dial, blab, sl, glab


def value_tag(slider, text, color=PAPER):
    return txt(text, 14, color).next_to(slider.track, UP, buff=0.12)


def title_card(scene, clip, episode, title, subtitle, arc="THE LOGISTIC FIXED-EFFECT MODEL"):
    """The series title scene: logo, wordmark, arc and episode number, title and subtitle."""
    mark, word = logo_mark(1.25), wordmark(64)
    head = VGroup(mark, word).arrange(RIGHT, buff=0.55).move_to(UP * 1.15)
    arc_t = txt(f"{arc}  \u00b7  EPISODE {episode}", 22, MUTED, weight=MEDIUM).next_to(head, DOWN, buff=0.75)
    title_t = txt(title, 66, PAPER, weight=SEMIBOLD, font=DISPLAY).next_to(arc_t, DOWN, buff=0.32)
    sub_t = txt(subtitle, 30, MUTED, font=SERIF, slant=ITALIC).next_to(title_t, DOWN, buff=0.26)
    a, dot, b, ring, scan = mark
    with scene.nar(clip, gap=0.6) as seg:
        scene.play(Create(a), Create(b), run_time=0.8)
        scene.play(GrowFromCenter(dot), GrowFromCenter(ring), FadeIn(scan, shift=RIGHT * 0.6), Write(word), run_time=1.3)
        seg.wait_until(seg.s(1) - 0.2)
        scene.play(LaggedStart(FadeIn(arc_t, shift=UP * 0.15), FadeIn(title_t, shift=UP * 0.2), FadeIn(sub_t, shift=UP * 0.15), lag_ratio=0.25), run_time=1.6)
    scene.wait(0.8)
    scene.play(*clear(scene), run_time=0.9)


def series_end_card(scene, clip, line):
    """The end card of an arc's last episode: no next episode, one closing line under the wordmark."""
    mark, word = logo_mark(1.0), wordmark(54)
    head = VGroup(mark, word).arrange(RIGHT, buff=0.5).move_to(UP * 0.7)
    ep = txt(line.upper(), 22, MUTED, weight=MEDIUM).next_to(head, DOWN, buff=0.6)
    thanks = txt("thanks for following the story", 28, PAPER, font=SERIF, slant=ITALIC).next_to(ep, DOWN, buff=0.45)
    with scene.nar(clip, gap=2.4):
        scene.play(*clear(scene), run_time=0.7)
        scene.play(FadeIn(head, shift=UP * 0.15), FadeIn(ep), run_time=1.0)
        scene.play(FadeIn(thanks, shift=UP * 0.1), run_time=0.8)
    scene.play(*clear(scene), run_time=1.4)


def end_card(scene, clip, next_episode, next_title):
    """The series end card, naming the next episode."""
    mark, word = logo_mark(1.0), wordmark(54)
    head = VGroup(mark, word).arrange(RIGHT, buff=0.5).move_to(UP * 0.7)
    ep = txt(f"NEXT  \u00b7  EPISODE {next_episode}  \u00b7  {next_title.upper()}", 22, MUTED, weight=MEDIUM).next_to(head, DOWN, buff=0.6)
    thanks = txt("thanks for following the story", 28, PAPER, font=SERIF, slant=ITALIC).next_to(ep, DOWN, buff=0.45)
    with scene.nar(clip, gap=1.8):
        scene.play(*clear(scene), run_time=0.7)
        scene.play(FadeIn(head, shift=UP * 0.15), FadeIn(ep), run_time=1.0)
        scene.play(FadeIn(thanks, shift=UP * 0.1), run_time=0.8)
    scene.play(*clear(scene), run_time=1.0)
