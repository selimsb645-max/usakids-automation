"""USA Kids Channel - Nunu-style scene painters, one per rhyme line.

draw_scene(rhyme_id, scene_key, t_local, seg) paints the full 2560x1440 frame.
Backgrounds are soft candy-color gradients with rounded hills/clouds.
"""
import math
from PIL import Image, ImageDraw
from . import actors
from .actors import W, H, baby, mom, doctor, animal, bus, bed, star_prop, \
    cloud, rainbow, tree, house, confetti, face, _shade

SKY = {
    "day":     ((180, 230, 255), (255, 250, 220)),
    "night":   ((40, 45, 95), (90, 75, 140)),
    "sunset":  ((255, 200, 140), (255, 160, 180)),
    "pinkroom":((255, 225, 240), (255, 245, 210)),
    "green":   ((200, 240, 200), (255, 252, 215)),
    "rainy":   ((170, 190, 220), (215, 225, 240)),
}


def _bg(d, sky, ground=(140, 210, 120), hills=True):
    c1, c2 = SKY[sky]
    for y in range(0, H, 24):
        f = y / H
        col = tuple(int(c1[i] * (1 - f) + c2[i] * f) for i in range(3))
        d.rectangle([0, y, W, y + 24], fill=col)
    if ground is not None:
        d.rounded_rectangle([0, H * 0.72, W, H], radius=180, fill=ground)
        d.rounded_rectangle([0, H * 0.72, W, H * 0.78], radius=180, fill=_shade(ground, 1.12))
    if hills:
        for cx, r, c in ((W * 0.15, H * 0.16, _shade(ground, 0.94)),
                          (W * 0.8, H * 0.2, _shade(ground, 0.9)),
                          (W * 0.55, H * 0.12, _shade(ground, 1.05))):
            d.ellipse([cx - r * 1.8, H * 0.72 - r, cx + r * 1.8, H * 0.72 + r * 1.5], fill=c)


def _sky_stars(d, t, n=26, color=(255, 245, 200)):
    import random
    rnd = random.Random(7)
    for k in range(n):
        x = rnd.randint(30, W - 30)
        y = rnd.randint(30, int(H * 0.6))
        ph = (math.sin(t * 2.2 + k * 1.7) + 1) / 2
        r = 3 + ph * 6
        d.line([x - r, y, x + r, y], fill=color, width=3)
        d.line([x, y - r, x, y + r], fill=color, width=3)


def _clouds(d, t, n=3):
    for k in range(n):
        x = ((k * 833 + int(t * -30)) % (W + 700)) - 350
        y = 130 + k * 120
        actors.cloud(d, x, y, 90 + k * 22, color=(255, 255, 255))


# ============================================================ wheels on the bus
def _wheels_frame(d, t, seg, scene):
    _bg(d, "day", ground=(150, 215, 120))
    _clouds(d, t)
    tree(d, W * 0.08, H * 0.66, 60, t)
    tree(d, W * 0.9, H * 0.64, 70, t + 2)
    if scene == "babies":
        bus(d, W * 0.42, H * 0.52, 150, t, passengers=())
        # three crying babies beside the bus window row
        for i, bx in enumerate((W * 0.28, W * 0.42, W * 0.56)):
            baby(d, bx, H * 0.6 + (i % 2) * 40, 62, t + i * 0.7, mood="cry", skin=i)
    elif scene == "mommies":
        bus(d, W * 0.5, H * 0.5, 150, t, passengers=())
        mom(d, W * 0.24, H * 0.62, 105, t, shush=True)
        mom(d, W * 0.66, H * 0.62, 105, t + 0.5, shush=True)
    elif scene == "animals":
        bus(d, W * 0.5, H * 0.52, 150, t, passengers=("pig", "dog", "duck"))
        animal(d, "pig", W * 0.08, H * 0.66, 70, t)
        animal(d, "dog", W * 0.9, H * 0.66, 70, t + 1)
    elif scene == "finale":
        bus(d, W * 0.5, H * 0.52, 150, t, passengers=("dog", "cat", "duck"))
        confetti(d, t)
        baby(d, W * 0.85, H * 0.63, 58, t, mood="happy", onesie=(120, 200, 250))
        star_prop(d, W * 0.12, H * 0.25, 60, t)
    elif scene == "wipers":
        bus(d, W * 0.5, H * 0.52, 150, t, passengers=("dog", "cat", "duck"), wipers=True)
    elif scene == "horn":
        bus(d, W * 0.5, H * 0.52, 150, t, passengers=("dog", "cat", "duck"), horn=True)
    else:   # wheels / wheels_echo
        bus(d, W * 0.5, H * 0.52, 150, t, passengers=("dog", "cat", "duck"),
            scroll=t * 260)
        if scene == "wheels_echo":
            # spinning wheel close-up vibes: extra ring highlights
            star_prop(d, W * 0.1, H * 0.22, 52, t, color=(255, 240, 130))


# ============================================================ twinkle twinkle
def _twinkle_frame(d, t, seg, scene):
    _bg(d, "night", ground=(70, 90, 80))
    _sky_stars(d, t)
    if scene == "high":
        star_prop(d, W * 0.5, H * 0.28, 120, t)
        for k in range(5):
            cloud(d, W * (0.15 + k * 0.18), H * 0.58 + (k % 2) * 40, 70,
                  color=(140, 140, 190))
    elif scene == "diamond":
        for k in range(6):
            a = t * 1.2 + k * math.pi / 3
            cx, cy = W * 0.5, H * 0.3
            r = 150 + math.sin(t * 2 + k) * 14
            d.line([cx + math.cos(a) * 90, cy + math.sin(a) * 90,
                    cx + math.cos(a) * r, cy + math.sin(a) * r],
                   fill=(255, 235, 140), width=8)
        star_prop(d, W * 0.5, H * 0.3, 110, t)
    elif scene == "wonder":
        star_prop(d, W * 0.66, H * 0.24, 95, t)
        baby(d, W * 0.35, H * 0.68, 88, t, onesie=(150, 200, 255))
        # pointing arm up
        d.line([W * 0.35 + 66, H * 0.68 - 20, W * 0.35 + 190, H * 0.68 - 150],
               fill=SKINS_ONE, width=26)
    else:  # star
        star_prop(d, W * 0.5, H * 0.32, 130, t)
    # baby on the hill watching
    if scene in ("star", "wonder"):
        baby(d, W * 0.78, H * 0.7, 76, t + 1, onesie=(255, 150, 180))


SKINS_ONE = (255, 226, 198)


# ============================================================ abc song
ABC_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ABC_COLORS = [(255, 100, 100), (255, 170, 60), (255, 220, 70), (120, 210, 110),
              (90, 180, 240), (150, 130, 240), (240, 130, 200)]
_ABC_GROUPS = [("ABCDEFG", "letters1"), ("HIJKLMNOP", "letters2"),
                ("QRS", "letters3"), ("TUV", "letters3b"), ("WXYZ", "letters4")]


def _abc_frame(d, t, seg, scene):
    _bg(d, "green", ground=(255, 235, 170))
    _clouds(d, t, 2)
    baby(d, W * 0.12, H * 0.66, 74, t, onesie=(120, 200, 250))
    # letter blocks pop in one at a time
    if scene == "letters1":
        group, pop = "ABCDEFG", min(7, int(t * 1.6) + 1)
    elif scene == "letters2":
        group, pop = "HIJKLMNOP", min(8, int(t * 1.6) + 1)
    elif scene == "letters3":
        group, pop = "QRSTU", min(5, int(t * 1.6) + 1)
    elif scene == "letters3b":
        group, pop = "TUV", 3
    elif scene == "letters4":
        group, pop = "WXYZ", min(4, int(t * 1.6) + 1)
    elif scene in ("nowknow", "nexttime"):
        group, pop = ABC_LETTERS, 26
        if scene == "nexttime":
            confetti(d, t)
    else:
        group, pop = ABC_LETTERS[:10], 10
    n = len(group)
    shown = group[:pop]
    cols = 7
    r = 108
    from PIL import ImageFont
    try:
        fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(r * 1.15))
    except Exception:
        fnt = ImageFont.load_default()
    for i, ch in enumerate(shown):
        # pop animation
        ph = min(1.0, (t * 1.6 - i) + 0.25)
        if ph <= 0:
            continue
        scale = 0.6 + 0.4 * min(1, ph * 3) + math.sin(t * 4 + i) * 0.05
        rr = int(r * scale)
        row, col = divmod(i, cols)
        cx = W * 0.5 + (col - min(cols, n) / 2 + 0.5) * r * 2.3 if n > cols else \
             W * 0.5 + (i - (n - 1) / 2) * r * 2.3
        cy = H * 0.4 + row * r * 2.5
        col_c = ABC_COLORS[i % len(ABC_COLORS)]
        d.rounded_rectangle([cx - rr, cy - rr, cx + rr, cy + rr], radius=int(rr * 0.3),
                            fill=col_c, outline=_shade(col_c, 0.7), width=6)
        tw = d.textlength(ch, font=fnt)
        d.text((cx - tw / 2, cy - r * 0.62), ch, font=fnt, fill=(255, 255, 255))


# ============================================================ five little monkeys
def _monkeys_frame(d, t, seg, scene):
    _bg(d, "pinkroom", ground=(250, 235, 210), hills=False)
    house_wall = (255, 242, 225)
    d.rectangle([0, H * 0.12, W, H * 0.72], fill=house_wall)
    # window
    d.rounded_rectangle([W * 0.05, H * 0.16, W * 0.3, H * 0.48], radius=60,
                        fill=(190, 235, 255), outline=(190, 150, 110), width=14)
    d.line([W * 0.175, H * 0.16, W * 0.175, H * 0.48], fill=(190, 150, 110), width=10)
    # picture frame
    d.rounded_rectangle([W * 0.78, H * 0.16, W * 0.95, H * 0.4], radius=40,
                        fill=(255, 250, 240), outline=(210, 160, 110), width=14)
    star_prop(d, W * 0.865, H * 0.28, 40, t, face_on=False)
    if scene in ("jump5", "jump4"):
        n = 5 if scene == "jump5" else 4
        bed(d, W * 0.5, H * 0.66, 120, t, headboard=(190, 130, 170), blanket=(130, 200, 250))
        for i in range(n):
            bx = W * (0.3 + i * 0.1)
            by = H * 0.6 - abs(math.sin(t * 5.5 + i * 0.9)) * 90
            animal(d, "monkey", bx, by, 56, t + i * 0.6)
    elif scene == "fell":
        bed(d, W * 0.62, H * 0.66, 120, t, headboard=(190, 130, 170), blanket=(130, 200, 250))
        animal(d, "monkey", W * 0.62, H * 0.68, 56, t, mood="sad")
        # tumbling monkey on floor + bump stars
        fp = min(1.0, t / 0.9)
        mx = W * 0.2 + fp * W * 0.06
        my = H * 0.78 - math.sin(fp * math.pi) * 60
        animal(d, "monkey", mx, my - 30, 50, t, mood="sad")
        for k in range(3):
            a = t * 3 + k * 2
            star_prop(d, mx + math.cos(a) * 80, my - 130 + math.sin(a) * 30, 26, t, face_on=False)
    elif scene in ("mama", "doctor"):
        bed(d, W * 0.66, H * 0.66, 120, t, headboard=(190, 130, 170), blanket=(130, 200, 250))
        mom(d, W * 0.24, H * 0.6, 100, t, dress=(200, 120, 160))
        if scene == "mama":
            # phone
            d.rounded_rectangle([W * 0.24 + 92, H * 0.6 - 70, W * 0.24 + 142, H * 0.6 - 10],
                                radius=14, fill=(60, 60, 80))
        else:
            doctor(d, W * 0.5, H * 0.62, 105, t, wag=True)
            for i in range(3):
                animal(d, "monkey", W * (0.14 + i * 0.06), H * 0.82, 44, t + i, mood="sad")


# ============================================================ five little ducks
def _ducks_frame(d, t, seg, scene):
    # pond scene
    _bg(d, "day", ground=(140, 210, 120))
    _clouds(d, t)
    tree(d, W * 0.06, H * 0.6, 70, t)
    tree(d, W * 0.92, H * 0.58, 80, t + 1)
    d.rounded_rectangle([W * 0.12, H * 0.74, W * 0.88, H], radius=140, fill=(110, 195, 235))
    for k in range(4):
        x = ((k * 550 + int(t * 60)) % int(W * 0.7)) + W * 0.14
        d.arc([x, H * 0.82, x + 130, H * 0.94], 200, 340, fill=(200, 235, 255), width=6)
    if scene == "over":
        # ducklings waddling over the hill away
        animal(d, "duck", W * 0.12, H * 0.66, 66, t)
        for i in range(4):
            animal(d, "duck", W * (0.3 + i * 0.13), H * (0.66 - i * 0.02) + math.sin(t*4+i)*14, 44, t + i)
        d.ellipse([W * 0.68, H * 0.5, W * 1.0, H * 0.78], fill=(120, 190, 110))  # hill
    elif scene == "quack":
        animal(d, "duck", W * 0.5, H * 0.6, 110, t)
        for k in range(3):
            ph = (t * 1.4 + k * 0.33) % 1
            r = ph * 240
            d.arc([W * 0.5 - r, H * 0.55 - r * 0.5, W * 0.5 + r, H * 0.55 + r * 0.5],
                  180, 360, fill=(90, 160, 220), width=8)
        for i in range(3):
            animal(d, "duck", W * (0.14 + i * 0.1), H * 0.86, 40, t + i)
    elif scene == "cameback":
        animal(d, "duck", W * 0.5, H * 0.6, 100, t)
        for i in range(5):
            animal(d, "duck", W * (0.16 + i * 0.14), H * 0.84 + (i % 2) * 20, 46, t + i * 0.4)
        confetti(d, t)
    else:  # ducks
        animal(d, "duck", W * 0.5, H * 0.58, 110, t)
        for i in range(5):
            animal(d, "duck", W * (0.16 + i * 0.14), H * 0.84 + (i % 2) * 20, 46, t + i * 0.4)


# ============================================================ finger family
_FINGER_MEM = {"daddy": (120, 160, 240), "mommy": (240, 120, 160), "babyf": (255, 200, 80)}
_FINGER_TITLE = {"daddy": "DADDY", "mommy": "MOMMY", "babyf": "BABY"}


def _finger_frame(d, t, seg, scene):
    _bg(d, "sunset", ground=(255, 220, 160), hills=False)
    _clouds(d, t, 2)
    base = scene.split("_")[0]
    col = _FINGER_MEM.get(base, (200, 200, 220))
    if scene.endswith("_here"):
        # giant singing finger character center
        d.ellipse([W * 0.5 - 300, H * 0.3 - 300, W * 0.5 + 300, H * 0.3 + 300], fill=col)
        face(d, W * 0.5, H * 0.3, 240, mood="sing", blink=math.sin(t * 1.2))
        confetti(d, t, seed=3)
    else:
        # big hand, one finger up & waving
        hx, hy = W * 0.5, H * 0.62
        d.rounded_rectangle([hx - 380, hy - 60, hx + 380, hy + 260], radius=120,
                            fill=(255, 224, 196))
        # fingers
        for i, fx in enumerate((-300, -150, 0, 150)):
            top = hy - 260 - (0 if i == 0 else (60 + abs(i - 1.5) * 20))
            if base == "babyf" and i in (0, 3):
                continue
            w = 120 if i == 0 else 100
            c = col if i == 0 else (255, 224, 196)
            wag = math.sin(t * 4.0) * 30 if i == 0 else 0
            d.rounded_rectangle([hx + fx - w / 2, top + wag, hx + fx + w / 2, hy],
                                radius=int(w / 2), fill=c)
            if i == 0:
                face(d, hx + fx, top + wag + 90, 48, mood="happy")
        d.rounded_rectangle([hx + 200, hy - 160, hx + 320, hy + 40], radius=60,
                            fill=(255, 224, 196))   # thumb
    # word chip
    try:
        from PIL import ImageFont
        fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
        word = _FINGER_TITLE.get(base, "FAMILY")
        tw = d.textlength(word, font=fnt)
        d.rounded_rectangle([W - tw - 220, 120, W - 60, 300], radius=60, fill=(255, 255, 255))
        d.text((W - tw - 140, 140), word, font=fnt, fill=(90, 60, 140))
    except Exception:
        pass


# ============================================================ london bridge
def _london_frame(d, t, seg, scene):
    _bg(d, "day", ground=(130, 200, 240), hills=False)   # river
    d.rectangle([0, H * 0.68, W, H], fill=(90, 170, 220))   # water
    for k in range(6):
        x = ((k * 420 + int(t * 90)) % W)
        d.arc([x, H * 0.78, x + 220, H * 0.95], 200, 340, fill=(180, 225, 250), width=8)
    if scene == "falling":
        # bridge deck blocks tumbling
        for i in range(7):
            fp = min(1.0, max(0.0, t * 0.8 - i * 0.1))
            drop = fp * fp * 300
            rot = fp * 0.8
            bx = W * 0.12 + i * W * 0.13
            by = H * 0.6 + drop
            d.rounded_rectangle([bx - 70, by - 40, bx + 70, by + 40], radius=16,
                                fill=(200, 160, 120))
        # towers standing
        for tx in (W * 0.2, W * 0.75):
            d.rounded_rectangle([tx - 60, H * 0.2, tx + 60, H * 0.68], radius=30,
                                fill=(220, 170, 130), outline=(160, 110, 70), width=10)
    elif scene == "lady":
        for tx in (W * 0.2, W * 0.75):
            d.rounded_rectangle([tx - 60, H * 0.2, tx + 60, H * 0.68], radius=30,
                                fill=(220, 170, 130), outline=(160, 110, 70), width=10)
        d.rectangle([W * 0.42, H * 0.62, W * 0.62, H * 0.7], fill=(200, 160, 120))
        mom(d, W * 0.5, H * 0.48, 95, t, dress=(240, 190, 90))
        # crown
        d.polygon([(W * 0.5 - 50, H * 0.48 - 195), (W * 0.5 - 50, H * 0.48 - 245),
                   (W * 0.5, H * 0.48 - 210), (W * 0.5 + 50, H * 0.48 - 245),
                   (W * 0.5 + 50, H * 0.48 - 195)], fill=(255, 210, 80))
        confetti(d, t, seed=5)
    else:   # bridge standing
        d.rectangle([W * 0.12, H * 0.6, W * 0.88, H * 0.68], fill=(210, 165, 125))
        for tx in (W * 0.2, W * 0.75):
            d.rounded_rectangle([tx - 60, H * 0.2, tx + 60, H * 0.68], radius=30,
                                fill=(220, 170, 130), outline=(160, 110, 70), width=10)
            for k in range(2):
                d.rectangle([tx - 44 + k * 22, H * 0.28, tx - 30 + k * 22, H * 0.42],
                            fill=(150, 200, 235))
        # little boat
        bx = ((t * 90) % W)
        d.polygon([(bx - 90, H * 0.72), (bx + 90, H * 0.72), (bx, H * 0.82)], fill=(150, 90, 60))
        d.rectangle([bx - 4, H * 0.58, bx + 4, H * 0.72], fill=(120, 80, 50))
        d.polygon([(bx + 4, H * 0.6), (bx + 70, H * 0.66), (bx + 4, H * 0.72)], fill=(255, 250, 240))


# ============================================================ rain rain go away
def _rain_frame(d, t, seg, scene):
    if scene in ("rain",):
        _bg(d, "rainy", ground=(140, 190, 150), hills=False)
        cloud(d, W * 0.28, H * 0.22, 130, color=(170, 180, 205))
        cloud(d, W * 0.7, H * 0.18, 110, color=(160, 175, 200))
        house(d, W * 0.72, H * 0.62, 130)
        # window with baby watching
        d.rounded_rectangle([W * 0.72 - 66, H * 0.62 + 30, W * 0.72 + 66, H * 0.62 + 170],
                            radius=20, fill=(190, 230, 255), outline=(150, 100, 70), width=12)
        baby(d, W * 0.36, H * 0.78, 62, t, mood="sad", onesie=(200, 130, 170))
        for k in range(16):
            rx = (k * 173 + int(t * 700)) % W
            ry = (k * 97 + int(t * 1100)) % H
            d.line([rx, ry, rx - 16, ry + 46], fill=(160, 200, 250), width=6)
    elif scene == "another":
        _bg(d, "rainy", ground=(140, 190, 150), hills=False)
        cloud(d, W * 0.3, H * 0.2, 120, color=(170, 180, 205))
        # sun peeking from corner
        sx, sy = W * 0.86, H * 0.2
        ph = (math.sin(t * 1.5) + 1) / 2
        d.ellipse([sx - 90, sy - 90, sx + 90, sy + 90], fill=(255, 220, 90))
        for k in range(8):
            a = k * math.pi / 4 + t * 0.4
            d.line([sx + math.cos(a) * 110, sy + math.sin(a) * 110,
                    sx + math.cos(a) * (150 + ph * 30), sy + math.sin(a) * (150 + ph * 30)],
                   fill=(255, 230, 120), width=12)
        rainbow(d, W * 0.4, H * 0.72, 320)
        baby(d, W * 0.4, H * 0.8, 60, t, onesie=(255, 150, 120))
    elif scene == "play":
        _bg(d, "day", ground=(150, 215, 120))
        _clouds(d, t, 2)
        # baby with ball + umbrella
        baby(d, W * 0.5, H * 0.7, 70, t, onesie=(130, 210, 250))
        d.arc([W * 0.5 + 40, H * 0.7 - 160, W * 0.5 + 420, H * 0.7 + 120], 180, 320,
              fill=(230, 90, 120), width=16)
        d.line([W * 0.5 + 62, H * 0.7 - 40, W * 0.5 + 62, H * 0.7 + 130], fill=(120, 80, 60), width=10)
        d.ellipse([W * 0.72, H * 0.78, W * 0.72 + 120, H * 0.78 + 120], fill=(255, 120, 150))
        d.arc([W * 0.72, H * 0.78, W * 0.72 + 120, H * 0.78 + 120], 90, 270,
              fill=(255, 200, 210), width=10)
        star_prop(d, W * 0.12, H * 0.25, 55, t)
    else:  # sun
        _bg(d, "day", ground=(150, 215, 120))
        sx, sy = W * 0.5, H * 0.3
        d.ellipse([sx - 130, sy - 130, sx + 130, sy + 130], fill=(255, 220, 90))
        face(d, sx, sy, 110, mood="happy", blink=math.sin(t))
        for k in range(10):
            a = k * math.pi / 5 + t * 0.5
            d.line([sx + math.cos(a) * 150, sy + math.sin(a) * 150,
                    sx + math.cos(a) * 210, sy + math.sin(a) * 210],
                   fill=(255, 230, 120), width=14)
        baby(d, W * 0.22, H * 0.75, 66, t, onesie=(255, 160, 190))
        animal(d, "chick", W * 0.75, H * 0.78, 52, t)


# ============================================================ head shoulders
def _shoulders_frame(d, t, seg, scene):
    _bg(d, "green", ground=(250, 235, 170), hills=False)
    _clouds(d, t, 2)
    if scene == "face":
        # big friendly face closeup, sparkle rings on features
        cx, cy = W * 0.5, H * 0.45
        d.ellipse([cx - 280, cy - 300, cx + 280, cy + 260], fill=(255, 224, 196))
        d.arc([cx - 280, cy - 340, cx - 120, cy - 180], 90, 270, fill=(120, 80, 50), width=24)
        d.arc([cx + 120, cy - 340, cx + 280, cy - 180], 270, 90, fill=(120, 80, 50), width=24)
        face(d, cx, cy, 240, mood="sing", blink=math.sin(t * 1.1))
        # feature highlight rings cycling
        for k, (fx, fy, fr, fc) in enumerate([
                (cx, cy - 95, 60, (255, 100, 100)),       # eyes
                (cx - 150, cy + 10, 70, (120, 190, 240)),  # ears
                (cx + 150, cy + 10, 70, (120, 190, 240)),
                (cx, cy + 80, 55, (255, 170, 80)),         # mouth
                (cx, cy - 200, 65, (130, 220, 130))]):     # nose
            ph = (math.sin(t * 2.0 - k * 1.2) + 1) / 2
            if ph > 0.6:
                d.ellipse([fx - fr, fy - fr, fx + fr, fy + fr], outline=fc,
                          width=max(4, int(fr * 0.14)))
    else:
        # full body touching head/shoulders/knees/toes in cycle
        baby(d, W * 0.42, H * 0.5, 105, t, onesie=(150, 200, 255))
        # hands guide: bouncing pointer stars at body positions
        pts = [(W * 0.42, H * 0.5 - 240, "HEAD"), (W * 0.42 - 150, H * 0.5 - 60, "SHOULDER"),
               (W * 0.42 - 90, H * 0.62, "KNEE"), (W * 0.42 + 60, H * 0.78, "TOE")]
        k = int(t * 2.2) % 4
        px, py, label = pts[k]
        ph = (t * 2.2) % 1
        star_prop(d, px, py - 40 - ph * 30, 44, t, color=(255, 210, 90), face_on=False)
        try:
            from PIL import ImageFont
            fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 74)
            tw = d.textlength(label, font=fnt)
            d.rounded_rectangle([px - tw / 2 - 24, py + 60, px + tw / 2 + 24, py + 160],
                                radius=30, fill=(255, 255, 255))
            d.text((px - tw / 2, py + 70), label, font=fnt, fill=(80, 90, 160))
        except Exception:
            pass


# ============================================================ dispatch
_PAINTERS = {
    "wheels_bus": _wheels_frame,
    "twinkle": _twinkle_frame,
    "abc_song": _abc_frame,
    "five_monkeys": _monkeys_frame,
    "five_ducks": _ducks_frame,
    "finger_family": _finger_frame,
    "london_bridge": _london_frame,
    "rain_rain": _rain_frame,
    "head_shoulders": _shoulders_frame,
}


def draw_scene(rhyme_id, scene_key, t_local, seg):
    """Returns a finished 1280x720 PIL image for this rhyme line."""
    big = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(big)
    painter = _PAINTERS[rhyme_id]
    painter(d, t_local, seg, scene_key)
    return big.resize((1280, 720), Image.LANCZOS)
