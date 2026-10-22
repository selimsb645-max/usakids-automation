"""USA Kids Channel - nursery-rhyme compilation renderer (Nunu TV style).

Timeline: intro card -> [song card + lyric lines] per rhyme -> outro card.
Voice: Kokoro af_heart per lyric line. Music: the rhyme's own marimba melody.
Lyrics appear in a soft karaoke pill so families can sing along.
"""
import math
import os
import shutil
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from . import actors, rhyme_scenes, audio
from .actors import W, H, baby, animal, star_prop, cloud, confetti, _shade

FPS = 15
SMALL_W, SMALL_H = 1280, 720
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

FONT_CACHE = {}
def _font(sz):
    if sz not in FONT_CACHE:
        FONT_CACHE[sz] = ImageFont.truetype(FONT_BOLD, sz)
    return FONT_CACHE[sz]


def _card_base(sky_key, tint=(255, 250, 230)):
    big = Image.new("RGB", (W, H), tint)
    d = ImageDraw.Draw(big)
    from .rhyme_scenes import _bg, SKY
    _bg(d, sky_key, ground=(250, 235, 190))
    return big, d


def _big_center_text(d, text, y, size=190, fill=(255, 255, 255), stroke=(70, 60, 120)):
    f = _font(size)
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        t2 = (cur + " " + w_).strip()
        if d.textlength(t2, font=f) > W * 0.84 and cur:
            lines.append(cur)
            cur = w_
        else:
            cur = t2
    lines.append(cur)
    yy = y - len(lines) * size * 0.62
    for ln in lines:
        tw = d.textlength(ln, font=f)
        d.text(((W - tw) / 2, yy), ln, font=f, fill=fill,
               stroke_width=max(10, size // 14), stroke_fill=stroke)
        yy += size * 1.18
    return yy


def intro_card(t, brand="USA KIDS"):
    big, d = _card_base("day")
    cloud(d, W * 0.18, H * 0.2, 90)
    cloud(d, W * 0.8, H * 0.16, 80)
    confetti(d, t)
    bounce = abs(math.sin(t * 3)) * 30
    baby(d, W * 0.5, H * 0.56 - bounce, 110, t, onesie=(255, 120, 160))
    star_prop(d, W * 0.16, H * 0.3, 70, t)
    star_prop(d, W * 0.84, H * 0.34, 62, t + 1)
    # brand pill
    f = _font(150)
    tw = d.textlength(brand, font=f)
    d.rounded_rectangle([(W - tw) / 2 - 90, H * 0.08, (W + tw) / 2 + 90, H * 0.08 + 240],
                        radius=70, fill=(255, 210, 80))
    d.text(((W - tw) / 2, H * 0.08 + 34), brand, font=f, fill=(255, 255, 255),
           stroke_width=16, stroke_fill=(200, 90, 40))
    f2 = _font(84)
    sub = "Sing-Along Nursery Rhymes!"
    tw2 = d.textlength(sub, font=f2)
    d.text(((W - tw2) / 2, H * 0.86), sub, font=f2, fill=(120, 80, 160),
           stroke_width=10, stroke_fill=(255, 255, 255))
    return big.resize((SMALL_W, SMALL_H), Image.LANCZOS)


def song_card(rhyme, t):
    big, d = _card_base("sunset")
    confetti(d, t, seed=5)
    bounce = abs(math.sin(t * 3.4)) * 26
    animal(d, "chick", W * 0.2, H * 0.72 - bounce, 74, t)
    baby(d, W * 0.78, H * 0.74 - abs(math.sin(t * 3.4 + 1)) * 26, 70, t + 0.6,
         onesie=(120, 200, 250))
    star_prop(d, W * 0.1, H * 0.2, 55, t)
    star_prop(d, W * 0.88, H * 0.24, 48, t + 0.7)
    _big_center_text(d, rhyme["title"], H * 0.28, size=170,
                     stroke=(200, 70, 60))
    return big.resize((SMALL_W, SMALL_H), Image.LANCZOS)


def outro_card(t):
    big, d = _card_base("night")
    from .rhyme_scenes import _sky_stars
    _sky_stars(d, t, n=34)
    star_prop(d, W * 0.5, H * 0.3, 130, t)
    baby(d, W * 0.5, H * 0.68, 96, t, onesie=(255, 160, 190))
    _big_center_text(d, "Subscribe for More Fun Songs!", H * 0.72, size=110,
                     stroke=(60, 60, 110))
    return big.resize((SMALL_W, SMALL_H), Image.LANCZOS)


def caption_pill(img, text, t, seg):
    """Soft rounded lyric pill at the bottom, gently bobbing."""
    d = ImageDraw.Draw(img)
    f = _font(56)
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        t2 = (cur + " " + w_).strip()
        if d.textlength(t2, font=f) > SMALL_W * 0.8 and cur:
            lines.append(cur)
            cur = w_
        else:
            cur = t2
    lines.append(cur)
    lh = 70
    box_h = len(lines) * lh + 44
    y0 = SMALL_H - box_h - 26 + math.sin(t * 2.6) * 4
    d.rounded_rectangle([SMALL_W * 0.06, y0, SMALL_W * 0.94, y0 + box_h],
                        radius=40, fill=(255, 255, 255))
    d.rounded_rectangle([SMALL_W * 0.06, y0, SMALL_W * 0.94, y0 + box_h],
                        radius=40, outline=(255, 170, 60), width=8)
    yy = y0 + 20
    for ln in lines:
        tw = d.textlength(ln, font=f)
        d.text(((SMALL_W - tw) / 2, yy), ln, font=f, fill=(90, 60, 130),
               stroke_width=4, stroke_fill=(255, 255, 255))
        yy += lh
    return img


def render(comp, workdir, seed=7):
    """comp: list of 3 rhyme dicts. Renders final.mp4 (1280x720, 15fps)."""
    os.makedirs(workdir, exist_ok=True)
    voice_dir = os.path.join(workdir, "voice")
    shutil.rmtree(voice_dir, ignore_errors=True)

    # ---- collect lyric lines across rhymes
    lines = []            # (rhyme, scene_key, text)
    for r in comp:
        for scene_key, text in r["lines"]:
            lines.append((r, scene_key, text))
    texts = [l[2] for l in lines]
    durs = audio.tts_lines(texts, voice_dir)

    # ---- timing: cards fixed, lines min 3.0s snapped to 0.5s
    CARD_S = 3.0
    OUTRO_S = 5.0
    starts, t = [], 0.0
    plan = []             # ("card", which, dur) / ("line", idx, dur)
    plan.append(("card", "intro", CARD_S)); t += CARD_S
    cur_rhyme = None
    line_starts = {}
    for i, (r, scene_key, text) in enumerate(lines):
        if r is not cur_rhyme:
            plan.append(("card", ("song", r), CARD_S)); t += CARD_S
            cur_rhyme = r
        seg = max(3.0, math.ceil((durs[i] + 0.55) * 2) / 2.0)
        line_starts[i] = t
        plan.append(("line", i, seg))
        t += seg
    plan.append(("card", "outro", OUTRO_S)); t += OUTRO_S
    total = t

    # section start times (parallel to plan)
    sec_starts = []
    acc = 0.0
    for k, w, s in plan:
        sec_starts.append(acc)
        acc += s

    # ---- audio: melody switches to each rhyme's own tune
    sr = audio.SR
    track = np.zeros(int((total + 1) * sr), dtype=np.float32)
    def add_track(mt, at_s):
        s = int(at_s * sr)
        e = min(len(track), s + len(mt))
        if e > s:
            track[s:e] += mt[:e - s]
    for idx, (kind, which, seg) in enumerate(plan):
        if kind == "card" and which == "intro":
            add_track(audio.melody_track(
                [("C5", 1), ("G4", 1), ("E4", 1), ("C4", 1), ("D4", 1), ("E4", 1), ("G4", 2)],
                seg, bpm=132), sec_starts[idx])
        elif kind == "card" and which == "outro":
            add_track(audio.melody_track([("C4", 1), ("E4", 1), ("G4", 1), ("C5", 1),
                                          ("G4", 1), ("C5", 3)], seg, bpm=132),
                      sec_starts[idx])
        elif kind == "card":
            add_track(audio.melody_track(which[1]["tune"], seg, bpm=116), sec_starts[idx])
        else:
            r = lines[which][0]
            add_track(audio.melody_track(r["tune"], seg, bpm=116), sec_starts[idx])
    track = track[:int(total * sr)]
    track *= 0.9 / max(1e-6, np.abs(track).max())

    # ---- video frames
    frames = os.path.join(workdir, "frames")
    shutil.rmtree(frames, ignore_errors=True)
    os.makedirs(frames, exist_ok=True)
    n_frames = int(total * FPS)
    fi = 0
    t_now = 0.0
    for k, which, seg in plan:
        n_f = int(round(seg * FPS))
        for j in range(n_f):
            lt = j / FPS
            if k == "card" and which == "intro":
                img = intro_card(lt)
            elif k == "card" and which == "outro":
                img = outro_card(lt)
            elif k == "card":
                img = song_card(which[1], lt)
            else:
                r, scene_key, text = lines[which]
                img = rhyme_scenes.draw_scene(r["id"], scene_key, lt, seg)
                img = caption_pill(img, text, lt, seg)
            img.save(os.path.join(frames, f"{fi:05d}.png"))
            fi += 1
        t_now += seg
        if fi % 150 == 0 and fi > 0:
            print(f"frame {fi}/{n_frames}", flush=True)
    print(f"frames done: {fi} (~{fi/FPS:.0f}s)", flush=True)

    # ---- mix voice into track
    mix = track.copy()
    for i, (r, scene_key, text) in enumerate(lines):
        v, _sr = audio._read_wav(os.path.join(voice_dir, f"line_{i:02d}.wav"))
        s = int(line_starts[i] * sr)
        e = min(len(mix), s + len(v))
        mix[s:e] += v[:e - s] * 0.95
    peak = np.abs(mix).max()
    if peak > 0.95:
        mix *= 0.95 / peak
    mix = np.tanh(mix * 1.02)
    pk = np.abs(mix).max()
    if 0 < pk < 0.85:
        mix *= 0.85 / pk
    mix_path = os.path.join(workdir, "mix.wav")
    audio._write_wav(mix_path, mix)
    print(f"audio: mixed {len(lines)} lines + melody -> {mix_path} "
          f"({total:.1f}s, peak {np.abs(mix).max():.2f})", flush=True)

    mp4 = os.path.join(workdir, "final.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
                    "-framerate", str(FPS), "-i", os.path.join(frames, "%05d.png"),
                    "-i", mix_path,
                    "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", mp4], check=True)
    shutil.rmtree(frames, ignore_errors=True)
    size = os.path.getsize(mp4)
    print(f"render: {mp4} ({size/1e6:.1f} MB, {total:.1f}s)", flush=True)
    return mp4, total


def starts_of(plan, rhyme):
    """Start time of this rhyme's song card + lines (for melody)."""
    # computed during render; simple helper returning [0] placeholder
    return [0.0]


def make_thumb(comp, workdir):
    """Cocomelon-style thumbnail: cute character reaching up to big letter
    balloons over a sunny sky, huge hook word + brand tag. High-saturation,
    phone-readable, no watermark issues (all self-drawn)."""
    import math as _m
    r = comp[0]
    img = Image.new("RGB", (SMALL_W, SMALL_H))
    d = ImageDraw.Draw(img)
    # sky gradient (bright day)
    for y in range(SMALL_H):
        t = y / SMALL_H
        d.line([(0, y), (SMALL_W, y)],
               fill=(int(120 + 100 * t), int(200 - 40 * t), 255))
    # sun with rays, top-right
    sx, sy, sr = SMALL_W * 0.86, SMALL_H * 0.14, 58
    for a in range(12):
        ang = a * _m.pi / 6
        d.line([sx + _m.cos(ang) * sr, sy + _m.sin(ang) * sr,
                sx + _m.cos(ang) * (sr + 26), sy + _m.sin(ang) * (sr + 26)],
               fill=(255, 230, 90), width=10)
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 220, 60))
    # grass ground
    gh = 200
    d.rounded_rectangle([-40, SMALL_H - gh + 20, SMALL_W + 40, SMALL_H + 60],
                        radius=140, fill=(120, 205, 90))
    d.ellipse([-160, SMALL_H - gh - 40, 520, SMALL_H - gh + 120], fill=(150, 220, 105))
    cloud(d, SMALL_W * 0.24, SMALL_H * 0.16, 70)
    cloud(d, SMALL_W * 0.66, SMALL_H * 0.24, 55)
    # --- letter balloons (the Cocomelon signature) ---
    letters = list(r.get("thumb_letters", ["A", "B", "C"]))
    bal_c = [(250, 80, 90), (255, 205, 60), (95, 160, 255), (250, 130, 190)]
    bx = [SMALL_W * 0.30, SMALL_W * 0.48, SMALL_W * 0.66, SMALL_W * 0.80]
    by = [SMALL_H * 0.30, SMALL_H * 0.44, SMALL_H * 0.32, SMALL_H * 0.47]
    bs = 86
    for i, ch in enumerate(letters[:4]):
        x, y, c = bx[i], by[i], bal_c[i]
        # string from balloon to the baby's raised hand
        hx, hy = SMALL_W * 0.30, SMALL_H * 0.80
        d.line([x, y + bs * 1.02, (x + hx) / 2, (y + hy) / 2 - 30, hx, hy],
               fill=(250, 250, 250), width=5, joint="curve")
        d.ellipse([x - bs, y - bs * 1.08, x + bs, y + bs * 1.02], fill=c,
                  outline=_shade(c, 0.6), width=6)
        d.ellipse([x - bs * 0.45, y - bs * 0.62, x - bs * 0.12, y - bs * 0.30],
                  fill=_shade(c, 1.25))          # shine
        f = _font(96)
        d.text((x - d.textlength(ch, font=f) / 2, y - 62), ch, font=f,
               fill=(255, 255, 255), stroke_width=8, stroke_fill=(60, 50, 100))
    # --- cute baby reaching up (arms raised at t=0.1) ---
    baby(d, SMALL_W * 0.30, SMALL_H * 0.78, 118, t=0.1, onesie=(90, 170, 255))
    # --- big hook word pill, top-left ---
    words = r.get("thumb_words", ["USA", "KIDS"])
    f1 = _font(132)
    tw = d.textlength(words[0], font=f1)
    d.rounded_rectangle([26, 22, 26 + tw + 64, 200], radius=34, fill=(255, 210, 60),
                        outline=(200, 140, 30), width=8)
    d.text((58, 44), words[0], font=f1, fill=(255, 255, 255),
           stroke_width=12, stroke_fill=(200, 70, 40))
    # second word bottom banner
    f2 = _font(104)
    w2 = words[1] if len(words) > 1 else "KIDS!"
    tw2 = d.textlength(w2, font=f2)
    d.rounded_rectangle([SMALL_W - tw2 - 140, SMALL_H - 156, SMALL_W - 26, SMALL_H - 40],
                        radius=28, fill=(255, 120, 140), outline=(170, 40, 60), width=8)
    d.text((SMALL_W - tw2 - 106, SMALL_H - 140), w2, font=f2, fill=(255, 255, 255),
           stroke_width=10, stroke_fill=(140, 30, 40))
    # brand tag bottom-left (like the logo corner on big kids channels)
    fb = _font(46)
    bt = "USA KIDS"
    bw = d.textlength(bt, font=fb)
    d.rounded_rectangle([26, SMALL_H - 88, 26 + bw + 40, SMALL_H - 26], radius=22,
                        fill=(255, 255, 255), outline=(60, 60, 120), width=5)
    d.text((46, SMALL_H - 78), bt, font=fb, fill=(90, 70, 160))
    thumb = os.path.join(workdir, "thumb.jpg")
    img.save(thumb, quality=92)
    print(f"thumb: {thumb}", flush=True)
    return thumb
