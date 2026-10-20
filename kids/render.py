"""USA Kids Channel - video assembly: beats -> frames -> ffmpeg render + thumbnail."""
import math
import os
import shutil
import subprocess

from . import scenes, audio
from PIL import Image, ImageDraw, ImageFont


def build_beats(lesson, intro, outro):
    """Full beat list with intro/outro visuals; texts for TTS."""
    beats = intro + lesson["beats"] + outro
    texts = [b[0] for b in beats]
    return beats, texts


def plan_timing(durs):
    """Beat start times: TTS duration + pad, snapped to 0.5s, min 2.5s."""
    starts, t = [], 0.0
    for d in durs:
        seg = max(2.5, math.ceil((d + 0.75) * 2) / 2.0)   # snap up to half seconds
        starts.append(t)
        t += seg
    return starts, t


def render(lesson, workdir, seed=7):
    from .lessons import INTRO_BEATS, OUTRO_BEATS
    beats, texts = build_beats(lesson, INTRO_BEATS, OUTRO_BEATS)
    voice_dir = os.path.join(workdir, "voice")
    durs = audio.tts_lines(texts, voice_dir)
    starts, total = plan_timing(durs)
    # beat boundaries (start + duration per beat)
    segs = [starts[i + 1] - starts[i] if i + 1 < len(starts) else total - starts[i]
            for i in range(len(starts))]
    wav = audio.assemble([os.path.join(voice_dir, f"line_{i:02d}.wav")
                          for i in range(len(texts))], starts, total,
                         os.path.join(workdir, "mix.wav"))

    frames = os.path.join(workdir, "frames")
    shutil.rmtree(frames, ignore_errors=True)
    os.makedirs(frames, exist_ok=True)
    n_frames = int(total * scenes.FPS)
    for fi in range(n_frames):
        t = fi / scenes.FPS
        bi = max(i for i, s in enumerate(starts) if s <= t)
        draw_vis = beats[bi][1]
        local_t = t - starts[bi]
        scenes.draw_frame(draw_vis, local_t, segs[bi], bi,
                          os.path.join(frames, f"{fi:05d}.png"))
        if fi % 150 == 0:
            print(f"frame {fi}/{n_frames}", flush=True)

    mp4 = os.path.join(workdir, "final.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
                    "-framerate", str(scenes.FPS), "-i", os.path.join(frames, "%05d.png"),
                    "-i", wav,
                    "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", mp4], check=True)
    shutil.rmtree(frames, ignore_errors=True)
    size = os.path.getsize(mp4)
    print(f"render: {mp4} ({size/1e6:.1f} MB, {total:.1f}s)", flush=True)
    return mp4, total


def make_thumb(lesson, workdir):
    """Bright 16:9 PIL thumbnail: colored blocks + 3-4 bold words (owner rule)."""
    W, H = 1280, 720
    cols = [(255, 214, 90), (255, 120, 120), (110, 200, 250), (130, 230, 140)]
    img = Image.new("RGB", (W, H), (255, 245, 225))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 26], fill=(255, 120, 120))
    d.rectangle([0, H - 26, W, H], fill=(110, 200, 250))
    words = lesson.get("thumb_words") or ["USA Kids", "Learning!", "Fun"]
    f_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 210)
    f_mid = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 88)
    # word 0 huge center
    w0 = words[0]
    tw = d.textlength(w0, font=f_big)
    d.rounded_rectangle([(W - tw) / 2 - 60, 90 - 16, (W + tw) / 2 + 60, 340], 36,
                        fill=cols[2])
    d.text(((W - tw) / 2, 100), w0, font=f_big, fill=(255, 255, 255),
           stroke_width=14, stroke_fill=(40, 60, 120))
    # word 1 lower banner
    w1 = words[1] if len(words) > 1 else "Learning!"
    f = f_mid
    tw = d.textlength(w1, font=f)
    d.rounded_rectangle([(W - tw) / 2 - 46, 400 - 10, (W + tw) / 2 + 46, 530], 30,
                        fill=cols[0])
    d.text(((W - tw) / 2, 408), w1, font=f, fill=(120, 60, 20),
           stroke_width=8, stroke_fill=(255, 255, 255))
    # word 2 corner chip
    if len(words) > 2:
        f_s = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 66)
        w2 = words[2]
        tw = d.textlength(w2, font=f_s)
        d.rounded_rectangle([W - tw - 150, 590 - 10, W - 40, 700], 26, fill=cols[1])
        d.text((W - tw - 108, 590), w2, font=f_s, fill=(255, 255, 255),
               stroke_width=8, stroke_fill=(150, 40, 40))
    # playful stars
    from .scenes import _star_points
    for cx, cy, r, c in [(150, 590, 46, (255, 200, 60)), (250, 640, 30, (255, 130, 160)),
                         (95, 480, 26, (120, 220, 130))]:
        d.polygon(_star_points(cx, cy, r), fill=c)
    thumb = os.path.join(workdir, "thumb.jpg")
    img.save(thumb, quality=92)
    print(f"thumb: {thumb}", flush=True)
    return thumb
