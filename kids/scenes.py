"""USA Kids Channel - colorful PIL scene renderer (15fps frames)."""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
FPS = 15
FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
_font_cache = {}


def _font(size):
    if size not in _font_cache:
        path = next((p for p in FONT_PATHS if os.path.exists(p)), None)
        _font_cache[size] = ImageFont.truetype(path, size) if path else ImageFont.load_default()
    return _font_cache[size]


def _pastel(i, accent):
    """Soft bright background that harmonizes with the beat accent color."""
    base = [(255, 248, 220), (255, 240, 245), (235, 250, 255), (250, 255, 240),
            (255, 245, 235), (245, 240, 255), (240, 255, 250), (255, 236, 230)]
    r, g, b = base[i % len(base)]
    a = accent
    return (int(r * 0.85 + a[0] * 0.15), int(g * 0.85 + a[1] * 0.15), int(b * 0.85 + a[2] * 0.15))


def _sparkles(d, t, seed, color=(255, 220, 90)):
    """Little twinkle stars that phase in/out."""
    for k in range(14):
        ang = seed * 1.7 + k * 2.39
        x = 80 + (k * 89 + seed * 37) % (W - 160)
        y = 60 + (k * 137 + seed * 53) % (H - 120)
        ph = (math.sin(t * 3.0 + ang) + 1) / 2
        if ph > 0.55:
            r = int(4 + 5 * ph)
            d.line([x - r, y, x + r, y], fill=color, width=3)
            d.line([x, y - r, x, y + r], fill=color, width=3)


def _star_points(cx, cy, r):
    pts = []
    for i in range(10):
        rad = r if i % 2 == 0 else r * 0.45
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return pts


def _draw_emoji_object(d, vis, cx, cy, r):
    """Draw a simple cheerful object matching the letter lesson word."""
    word = vis.get("word", "").lower()
    acc = vis.get("accent", (255, 120, 60))
    if "apple" in word:
        d.ellipse([cx - r, cy - r * 0.85, cx + r, cy + r * 0.9], fill=(230, 50, 50))
        d.ellipse([cx - r * 0.55, cy - r * 0.5, cx, cy + r * 0.55], fill=(255, 130, 120))
        d.rectangle([cx - 5, cy - r * 1.15, cx + 5, cy - r * 0.6], fill=(120, 70, 40))
        d.ellipse([cx + 4, cy - r * 1.2, cx + r * 0.7, cy - r * 0.8], fill=(90, 200, 90))
    elif "ball" in word or "sun" in word:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 180, 40))
        d.arc([cx - r * 0.7, cy - r * 0.7, cx + r * 0.7, cy + r * 0.7], 20, 160,
              fill=(255, 240, 200), width=8)
    elif "cat" in word or "dog" in word or "lion" in word or "bear" in word or "goat" in word:
        body = (240, 200, 80) if "cat" in word else ((190, 140, 90) if "dog" in word else (230, 170, 90))
        d.ellipse([cx - r, cy - r * 0.7, cx + r, cy + r * 0.8], fill=body)
        d.ellipse([cx - r * 0.7, cy - r * 1.3, cx - r * 0.1, cy - r * 0.6], fill=body)
        d.ellipse([cx + r * 0.1, cy - r * 1.3, cx + r * 0.7, cy - r * 0.6], fill=body)
        d.ellipse([cx - r * 0.5, cy - r * 0.15, cx - r * 0.25, cy + r * 0.1], fill=(40, 40, 40))
        d.ellipse([cx + r * 0.25, cy - r * 0.15, cx + r * 0.5, cy + r * 0.1], fill=(40, 40, 40))
        d.ellipse([cx - r * 0.08, cy + r * 0.25, cx + r * 0.08, cy + r * 0.42], fill=(255, 120, 120))
    elif "fish" in word:
        d.ellipse([cx - r, cy - r * 0.5, cx + r * 0.7, cy + r * 0.5], fill=(60, 170, 220))
        d.polygon([(cx + r * 0.6, cy), (cx + r * 1.1, cy - r * 0.45),
                   (cx + r * 1.1, cy + r * 0.45)], fill=(60, 170, 220))
        d.ellipse([cx - r * 0.55, cy - r * 0.15, cx - r * 0.4, cy], fill=(20, 20, 20))
    elif "egg" in word or "juice" in word or "orange" in word:
        col = (255, 250, 240) if "egg" in word else ((255, 150, 40) if "orange" in word else (250, 180, 60))
        d.ellipse([cx - r * 0.7, cy - r, cx + r * 0.7, cy + r], fill=col)
    elif "hat" in word:
        d.ellipse([cx - r, cy + r * 0.2, cx + r, cy + r * 0.75], fill=(120, 70, 200))
        d.rectangle([cx - r * 0.5, cy - r * 0.8, cx + r * 0.5, cy + r * 0.25], fill=(150, 90, 230))
    elif "ice" in word:
        d.polygon([(cx, cy - r), (cx + r * 0.8, cy), (cx - r * 0.8, cy)], fill=(255, 160, 190))
        d.rectangle([cx - r * 0.12, cy, cx + r * 0.12, cy + r * 1.2], fill=(200, 150, 90))
    elif "kite" in word or "moon" in word:
        if "moon" in word:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 230, 140))
            d.ellipse([cx - r * 0.35, cy - r * 0.85, cx + r * 0.55, cy - r * 0.05],
                      fill=(255, 250, 220))
        else:
            d.polygon([(cx, cy - r), (cx + r * 0.7, cy + r * 0.3), (cx, cy + r),
                       (cx - r * 0.7, cy + r * 0.3)], fill=(240, 90, 120))
            d.line([cx, cy - r, cx, cy - r * 1.4], fill=(80, 80, 80), width=4)
    elif "nest" in word:
        d.arc([cx - r * 0.9, cy - r * 0.4, cx + r * 0.9, cy + r], 0, 180, fill=(150, 100, 50), width=18)
        d.ellipse([cx - r * 0.3, cy - r * 0.7, cx + r * 0.3, cy - r * 0.25], fill=(140, 220, 120))
    elif "parrot" in word:
        d.ellipse([cx - r * 0.5, cy - r, cx + r * 0.5, cy + r * 0.3], fill=(230, 60, 90))
        d.polygon([(cx - r * 0.2, cy + r * 0.1), (cx - r * 0.2, cy + r * 0.9),
                   (cx + r * 0.35, cy + r * 0.3)], fill=(80, 160, 90))
        d.ellipse([cx - r * 0.15, cy - r * 0.85, cx - r * 0.02, cy - r * 0.72], fill=(20, 20, 20))
    elif "queen" in word:
        d.polygon([(cx - r * 0.8, cy + r * 0.6), (cx - r * 0.8, cy - r * 0.3),
                   (cx - r * 0.35, cy), (cx, cy - r * 0.7),
                   (cx + r * 0.35, cy), (cx + r * 0.8, cy - r * 0.3),
                   (cx + r * 0.8, cy + r * 0.6)], fill=(220, 170, 60))
        d.ellipse([cx - r * 0.18, cy + r * 0.1, cx + r * 0.18, cy + r * 0.4], fill=(255, 120, 120))
    elif "rain" in word:
        for k in range(5):
            rx = cx - r * 0.7 + k * r * 0.35
            d.arc([rx - r * 0.15, cy - r * 0.4, rx + r * 0.15, cy + r * 0.5], 200, 340,
                  fill=(80, 160, 240), width=6)
        d.ellipse([cx - r * 0.9, cy - r, cx + r * 0.2, cy - r * 0.35], fill=(200, 210, 230))
    elif "tree" in word:
        d.rectangle([cx - r * 0.15, cy, cx + r * 0.15, cy + r], fill=(130, 85, 50))
        d.ellipse([cx - r * 0.95, cy - r * 1.1, cx + r * 0.95, cy + r * 0.2], fill=(70, 180, 90))
    elif "umbrella" in word:
        d.pieslice([cx - r, cy - r, cx + r, cy + r * 0.8], 180, 360, fill=(240, 70, 90))
        d.line([cx, cy + r * 0.0, cx, cy + r * 0.9], fill=(60, 60, 60), width=6)
        d.arc([cx + r * 0.1, cy + r * 0.4, cx + r * 0.5, cy + r * 0.8], 20, 160,
              fill=(60, 60, 60), width=6)
    elif "van" in word:
        d.rounded_rectangle([cx - r, cy - r * 0.5, cx + r, cy + r * 0.5], 18, fill=(90, 140, 250))
        d.rounded_rectangle([cx + r * 0.2, cy - r * 0.95, cx + r * 0.85, cy - r * 0.45], 10,
                            fill=(200, 235, 255))
        d.ellipse([cx - r * 0.55, cy + r * 0.35, cx - r * 0.2, cy + r * 0.7], fill=(40, 40, 40))
        d.ellipse([cx + r * 0.25, cy + r * 0.35, cx + r * 0.6, cy + r * 0.7], fill=(40, 40, 40))
    elif "watch" in word:
        d.ellipse([cx - r * 0.75, cy - r * 0.75, cx + r * 0.75, cy + r * 0.75], fill=(90, 90, 110))
        d.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55], fill=(255, 255, 250))
        d.line([cx, cy, cx, cy - r * 0.35], fill=(40, 40, 40), width=6)
        d.line([cx, cy, cx + r * 0.28, cy + r * 0.1], fill=(200, 60, 60), width=6)
    elif "xylophone" in word:
        for k in range(5):
            wd = r * (1.0 - k * 0.15)
            col = [(230, 70, 70), (240, 160, 50), (240, 230, 70), (90, 190, 90), (80, 150, 240)][k]
            d.rectangle([cx - wd, cy - r * 0.9 + k * r * 0.36, cx + wd, cy - r * 0.6 + k * r * 0.36],
                        fill=col)
    else:
        d.ellipse([cx - r * 0.7, cy - r * 0.7, cx + r * 0.7, cy + r * 0.7], fill=acc)


def draw_frame(vis, local_t, dur, beat_idx, out_path):
    """Render one frame for the given visual."""
    acc = vis.get("accent", (255, 120, 60))
    img = Image.new("RGB", (W, H), _pastel(beat_idx, acc))
    d = ImageDraw.Draw(img)
    _sparkles(d, local_t, beat_idx)
    prog = min(1.0, local_t / max(0.001, dur))
    bounce = abs(math.sin(math.pi * (local_t * 2.2)))           # bouncy motion
    pop = 1.0 + 0.06 * bounce                                   # scale pulse
    t = vis.get("type", "banner")

    if t == "banner":
        word = vis.get("word", "")
        f_big = _font(190)
        tw = d.textlength(word, font=f_big)
        d.text(((W - tw) / 2, H / 2 - 160 - 26 * bounce), word, font=f_big,
               fill=(60, 40, 90), stroke_width=10, stroke_fill=(255, 255, 255))
        f_sub = _font(46)
        sub = "USA Kids Channel"
        sw = d.textlength(sub, font=f_sub)
        d.text(((W - sw) / 2, H / 2 + 90), sub, font=f_sub, fill=acc)
    elif t == "letter":
        ch = vis.get("char", "A")
        f_big = _font(300 * pop)
        tw = d.textlength(ch, font=f_big)
        x0 = (W - tw) / 2
        y0 = 80 - 30 * bounce
        d.text((x0, y0), ch, font=f_big, fill=acc, stroke_width=12, stroke_fill=(255, 255, 255))
        _draw_emoji_object(d, vis, W / 2, 560 + 16 * bounce, 78)
        f_w = _font(64)
        word = vis.get("word", "")
        ww = d.textlength(word, font=f_w)
        d.text(((W - ww) / 2, 600), word, font=f_w, fill=(70, 50, 100),
               stroke_width=6, stroke_fill=(255, 255, 255))
    elif t == "count":
        n = min(vis.get("n", 1), 20)
        # numeral
        f_num = _font(int(240 * pop))
        num = vis.get("word", str(n))
        nw = d.textlength(num, font=f_num)
        d.text(((W - nw) / 2, 40 - 24 * bounce), num, font=f_num, fill=acc,
               stroke_width=10, stroke_fill=(255, 255, 255))
        # n stars in a playful arc
        cols = [(255, 90, 90), (255, 160, 70), (250, 210, 60), (110, 200, 100),
                (90, 200, 220), (100, 150, 255), (180, 130, 255), (255, 130, 200)]
        per_row = min(n, 5)
        rows = math.ceil(n / per_row)
        for i in range(n):
            r_i, c_i = divmod(i, per_row)
            cx = W / 2 + (c_i - (min(n - r_i * per_row, per_row) - 1) / 2) * 150
            cy = 330 + r_i * 150 + 18 * math.sin(2 * math.pi * (local_t * 2.0 + i * 0.55))
            d.polygon(_star_points(cx, cy, 44 + 5 * bounce), fill=cols[i % len(cols)])
    elif t == "color":
        fill = vis.get("fill", (200, 60, 60))
        name = vis.get("name", "")
        r = 180 + 22 * bounce
        d.rounded_rectangle([W / 2 - r, 200 - r * 0.3 - 20 * bounce,
                             W / 2 + r, 200 + r * 1.5 + 20 * bounce], 60, fill=fill)
        f_n = _font(90)
        nw = d.textlength(name, font=f_n)
        d.text(((W - nw) / 2, 545), name, font=f_n, fill=(70, 50, 100),
               stroke_width=8, stroke_fill=(255, 255, 255))
    elif t == "shape":
        sh = vis.get("shape", "circle")
        r = 170 * pop
        cx, cy = W / 2, 330 + 18 * bounce
        if sh == "circle":
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=acc)
        elif sh == "square":
            d.rounded_rectangle([cx - r * 0.9, cy - r * 0.9, cx + r * 0.9, cy + r * 0.9], 24, fill=acc)
        elif sh == "triangle":
            d.polygon([(cx, cy - r), (cx + r, cy + r * 0.8), (cx - r, cy + r * 0.8)], fill=acc)
        elif sh == "star":
            d.polygon(_star_points(cx, cy, r), fill=acc)
        elif sh == "heart":
            d.ellipse([cx - r * 0.9, cy - r * 0.7, cx - r * 0.05, cy + r * 0.15], fill=acc)
            d.ellipse([cx + r * 0.05, cy - r * 0.7, cx + r * 0.9, cy + r * 0.15], fill=acc)
            d.polygon([(cx - r * 0.88, cy - r * 0.05), (cx + r * 0.88, cy - r * 0.05),
                       (cx, cy + r * 0.95)], fill=acc)
        elif sh == "oval":
            d.ellipse([cx - r * 1.15, cy - r * 0.7, cx + r * 1.15, cy + r * 0.7], fill=acc)
        elif sh == "rect":
            d.rounded_rectangle([cx - r * 1.2, cy - r * 0.7, cx + r * 1.2, cy + r * 0.7], 22, fill=acc)
        elif sh == "diamond":
            d.polygon([(cx, cy - r), (cx + r * 0.8, cy), (cx, cy + r), (cx - r * 0.8, cy)], fill=acc)
        f_n = _font(84)
        name = vis.get("name", "")
        nw = d.textlength(name, font=f_n)
        d.text(((W - nw) / 2, 555), name, font=f_n, fill=(70, 50, 100),
               stroke_width=8, stroke_fill=(255, 255, 255))
    # corner channel stamp
    f_s = _font(28)
    d.text((24, 18), "USA Kids Channel", font=f_s, fill=(255, 255, 255),
           stroke_width=3, stroke_fill=(150, 120, 60))
    img.save(out_path)
    return out_path
