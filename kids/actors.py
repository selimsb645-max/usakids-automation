"""USA Kids Channel - cute Nunu-style characters & props, drawn with PIL.

Everything draws on a 2560x1440 supersampled canvas (downscaled 2x by the
renderer for smooth anti-aliased edges). Coordinates are absolute pixels
on that big canvas; helpers below take a center + scale.

Design language: big round heads, huge dark eyes with white highlights,
blush cheeks, soft candy colors, rounded everything.
"""
import math

W, H = 2560, 1440          # supersample canvas (downscaled to 1280x720)


# ---------------------------------------------------------------- eyes/face
def face(d, cx, cy, r, mood="happy", skin=None, blink=None, look=(0, 0)):
    """Cute face (eyes + blush + mouth) centered at (cx, cy) with radius r.
    mood: happy | sad | cry | sing | sleep | surprised | shh
    blink: 0..1 (1 = fully closed)
    look: eye offset direction (-1..1, -1..1)
    """
    er = r * 0.16                      # eye radius
    ex, ey = cx + look[0] * r * 0.18, cy - r * 0.18
    lx, rx = ex - r * 0.42, ex + r * 0.42
    dark = (40, 34, 44)
    if mood == "sleep":
        for x in (lx, rx):
            d.arc([x - er, ey - er * 0.6, x + er, ey + er * 0.9], 20, 160, fill=dark, width=max(3, int(r*0.045)))
    elif blink and blink > 0.75:
        for x in (lx, rx):
            d.line([x - er, ey, x + er, ey], fill=dark, width=max(3, int(r*0.05)))
    else:
        if mood in ("cry", "sad"):
            # tilted oval eyes
            for i, x in enumerate((lx, rx)):
                tilt = -14 if i == 0 else 14
                d.ellipse([x - er, ey - er * 1.15, x + er, ey + er * 0.6], fill=dark)
            # tears
            ty = ey + er * 1.6
            for i, x in enumerate((lx, rx)):
                ph = (math.sin((blink or 0) * 6 + i) + 1) / 2
                d.ellipse([x - er * 0.35, ty + ph * r * 0.55,
                           x + er * 0.35, ty + ph * r * 0.55 + er * 0.8],
                          fill=(140, 200, 255))
        else:
            for x in (lx, rx):
                d.ellipse([x - er, ey - er * 1.25, x + er, ey + er * 1.25], fill=dark)
                # white highlight
                d.ellipse([x - er * 0.15, ey - er * 0.85, x + er * 0.55, ey - er * 0.15],
                          fill=(255, 255, 255))
    # blush
    br = r * 0.14
    for x in (cx - r * 0.62, cx + r * 0.62):
        d.ellipse([x - br, cy + r * 0.08, x + br, cy + r * 0.08 + br * 1.2],
                  fill=(255, 170, 170))
    # mouth
    my = cy + r * 0.38
    mw = max(3, int(r * 0.05))
    if mood == "cry":
        d.arc([cx - r * 0.3, my - r * 0.22, cx + r * 0.3, my + r * 0.3], 20, 160,
              fill=(120, 60, 60), width=mw)
    elif mood == "sad":
        d.arc([cx - r * 0.26, my - r * 0.2, cx + r * 0.26, my + r * 0.16], 20, 160,
              fill=(150, 80, 80), width=mw)
    elif mood in ("sing", "surprised"):
        d.ellipse([cx - r * 0.22, my - r * 0.18, cx + r * 0.22, my + r * 0.3],
                  fill=(200, 90, 90))
        d.ellipse([cx - r * 0.1, my + r * 0.1, cx + r * 0.1, my + r * 0.22],
                  fill=(255, 160, 170))
    elif mood == "shh":
        # small o mouth
        d.ellipse([cx - r * 0.12, my - r * 0.1, cx + r * 0.12, my + r * 0.14],
                  fill=(200, 100, 100))
    elif mood == "sleep":
        d.arc([cx - r * 0.18, my - r * 0.12, cx + r * 0.18, my + r * 0.2], 10, 170,
              fill=(190, 110, 110), width=mw)
    else:
        d.arc([cx - r * 0.3, my - r * 0.3, cx + r * 0.3, my + r * 0.3], 20, 160,
              fill=(190, 90, 90), width=mw)


# ---------------------------------------------------------------- characters
SKINS = [(255, 226, 198), (255, 205, 165), (245, 180, 140), (215, 150, 110)]


def baby(d, cx, cy, s, t=0.0, mood="happy", onesie=(255, 120, 160), skin=0,
         hair=(90, 60, 40), hat=None):
    """Adorable toddler mascot. s = body radius; bounces with phase t."""
    bob = abs(math.sin(t * 3.2)) * s * 0.12
    cy = cy - bob
    skin_c = SKINS[skin % len(SKINS)]
    # legs (before body)
    for dx in (-0.34, 0.34):
        d.ellipse([cx + s * dx - s * 0.16, cy + s * 0.78, cx + s * dx + s * 0.16,
                   cy + s * 1.15], fill=(255, 224, 196))
        d.ellipse([cx + s * dx - s * 0.24, cy + s * 1.02, cx + s * dx + s * 0.24,
                   cy + s * 1.3], fill=hat or onesie)
    # arms (waving with bounce)
    aw = math.sin(t * 3.2 + 1.2) * 0.35
    for i, sx in enumerate((-1, 1)):
        ax = cx + sx * (s * 0.75)
        ay = cy + s * 0.05 + (-0.15 if i else 0) * s - aw * s * (0.6 if sx > 0 else 1.0)
        d.line([cx + sx * s * 0.55, cy + s * 0.28, ax + sx * s * 0.3, ay],
               fill=skin_c, width=max(4, int(s * 0.22)))
        d.ellipse([ax + sx * s * 0.3 - s * 0.13, ay - s * 0.13,
                   ax + sx * s * 0.3 + s * 0.13, ay + s * 0.13], fill=skin_c)
    # body: rounded onesie
    d.rounded_rectangle([cx - s * 0.72, cy - s * 0.35, cx + s * 0.72, cy + s * 0.95],
                        radius=int(s * 0.5), fill=onesie)
    # onesie belly button stripe
    d.line([cx, cy + s * 0.42, cx, cy + s * 0.85], fill=_shade(onesie, 0.85), width=max(2, int(s*0.06)))
    # head
    hr = s * 0.78
    d.ellipse([cx - hr, cy - hr * 1.12 - s * 0.3, cx + hr, cy + hr * 0.85 - s * 0.3],
              fill=skin_c)
    # hair tuft
    d.arc([cx - hr * 0.5, cy - hr * 1.45 - s * 0.3, cx + hr * 0.5, cy - hr * 0.7 - s * 0.3],
          180, 340, fill=hair, width=max(4, int(s * 0.09)))
    d.arc([cx - hr * 0.3, cy - hr * 1.35 - s * 0.3, cx + hr * 0.2, cy - hr * 0.75 - s * 0.3],
          180, 330, fill=hair, width=max(3, int(s * 0.08)))
    face(d, cx, cy - s * 0.3, hr, mood=mood, blink=math.sin(t * 1.3))
    return cx, cy


def mom(d, cx, cy, s, t=0.0, mood="happy", dress=(150, 120, 220), skin=1,
        hair=(70, 45, 30), shush=False):
    bob = abs(math.sin(t * 2.4)) * s * 0.06
    cy = cy - bob
    skin_c = SKINS[skin % len(SKINS)]
    # dress
    d.polygon([(cx - s * 0.5, cy - s * 0.2), (cx + s * 0.5, cy - s * 0.2),
               (cx + s * 0.85, cy + s * 1.15), (cx - s * 0.85, cy + s * 1.15)],
              fill=dress)
    # arms
    for sx in (-1, 1):
        if shush and sx > 0:
            d.line([cx + s * 0.4, cy + s * 0.05, cx + s * 0.55, cy - s * 0.75],
                   fill=skin_c, width=max(4, int(s * 0.16)))
            d.ellipse([cx + s * 0.44, cy - s * 1.02, cx + s * 0.66, cy - s * 0.78],
                      fill=skin_c)   # finger to lips
        else:
            d.line([cx + sx * s * 0.42, cy + s * 0.0, cx + sx * s * 0.8, cy + s * 0.42],
                   fill=skin_c, width=max(4, int(s * 0.16)))
    # head
    hr = s * 0.55
    hy = cy - s * 0.62
    d.ellipse([cx - hr, hy - hr, cx + hr, hy + hr], fill=skin_c)
    # mom hair: bun
    d.ellipse([cx - hr * 1.06, hy - hr * 1.05, cx + hr * 1.06, hy + hr * 0.45], fill=hair)
    d.ellipse([cx - hr * 1.02, hy - hr * 0.5, cx + hr * 1.02, hy + hr * 1.02], fill=skin_c)
    d.ellipse([cx - hr * 0.2, hy - hr * 1.5, cx + hr * 0.42, hy - hr * 0.85], fill=hair)
    face(d, cx, hy, hr, mood="shh" if shush else mood, blink=math.sin(t * 1.1))
    return cx, cy


def doctor(d, cx, cy, s, t=0.0, wag=True):
    """Friendly doctor waving a finger."""
    bob = abs(math.sin(t * 2.6)) * s * 0.05
    cy -= bob
    skin_c = SKINS[1]
    # white coat
    d.rounded_rectangle([cx - s * 0.55, cy - s * 0.35, cx + s * 0.55, cy + s * 1.05],
                        radius=int(s * 0.3), fill=(250, 250, 255))
    d.line([cx, cy - s * 0.35, cx, cy + s * 1.05], fill=(210, 220, 235), width=max(3, int(s*0.05)))
    # stethoscope
    d.arc([cx - s * 0.3, cy + s * 0.1, cx + s * 0.3, cy + s * 0.7], 0, 180,
          fill=(90, 90, 110), width=max(3, int(s * 0.06)))
    d.ellipse([cx - s * 0.09, cy + s * 0.68, cx + s * 0.09, cy + s * 0.86], fill=(60, 150, 200))
    # legs
    d.rectangle([cx - s * 0.35, cy + s * 1.05, cx - s * 0.1, cy + s * 1.3], fill=(90, 100, 130))
    d.rectangle([cx + s * 0.1, cy + s * 1.05, cx + s * 0.35, cy + s * 1.3], fill=(90, 100, 130))
    # arm + wagging finger
    wag_ph = math.sin(t * 5.0) if wag else 0
    d.line([cx - s * 0.45, cy + s * 0.1, cx - s * 0.95, cy - s * 0.35 + wag_ph * s * 0.18],
           fill=skin_c, width=max(4, int(s * 0.14)))
    d.ellipse([cx - s * 1.15, cy - s * 0.7 + wag_ph * s * 0.18,
               cx - s * 0.85, cy - s * 0.4 + wag_ph * s * 0.18], fill=skin_c)
    # head
    hr = s * 0.5
    hy = cy - s * 0.55
    d.ellipse([cx - hr, hy - hr, cx + hr, hy + hr], fill=skin_c)
    # head mirror band
    d.arc([cx - hr, hy - hr * 1.15, cx + hr, hy - hr * 0.35], 200, 340,
          fill=(90, 90, 110), width=max(4, int(s * 0.07)))
    d.ellipse([cx - hr * 0.2, hy - hr * 1.3, cx + hr * 0.5, hy - hr * 0.75],
              fill=(200, 200, 220))
    face(d, cx, hy, hr, mood="happy", blink=math.sin(t * 1.4))
    return cx, cy


def animal(d, kind, cx, cy, s, t=0.0, mood="happy"):
    """Cute animal head+body: dog|cat|duck|cow|sheep|monkey|frog|pig|elephant"""
    bob = abs(math.sin(t * 3.0)) * s * 0.08
    cy = cy - bob
    if kind == "duck":
        col = (255, 220, 90)
        d.ellipse([cx - s * 0.8, cy + s * 0.0, cx + s * 0.8, cy + s * 1.1], fill=col)     # body
        d.ellipse([cx - s * 0.5, cy - s * 0.8, cx + s * 0.5, cy + s * 0.1], fill=col)    # head
        d.polygon([(cx + s * 0.35, cy - s * 0.45), (cx + s * 0.95, cy - s * 0.25),
                   (cx + s * 0.35, cy - s * 0.05)], fill=(255, 150, 40))                  # beak
        # wing
        ph = math.sin(t * 6.0)
        d.ellipse([cx - s * 0.55, cy + s * 0.3 - ph * s * 0.15, cx + s * 0.1, cy + s * 0.85],
                  fill=_shade(col, 0.9))
        face(d, cx, cy - s * 0.35, s * 0.5, mood=mood, blink=math.sin(t * 1.2 + 1))
        return cx, cy
    if kind == "elephant":
        col = (170, 180, 230)
        d.ellipse([cx - s * 0.9, cy + s * 0.0, cx + s * 0.9, cy + s * 1.1], fill=col)
        d.ellipse([cx - s * 0.52, cy - s * 0.9, cx + s * 0.52, cy + s * 0.05], fill=col)
        # trunk
        d.arc([cx - s * 0.1, cy - s * 0.5, cx + s * 0.7, cy + s * 0.6], 270, 60,
              fill=col, width=max(5, int(s * 0.24)))
        # big ears
        for sx in (-1, 1):
            d.ellipse([cx + sx * s * 0.5 - s * 0.32, cy - s * 0.85,
                       cx + sx * s * 0.5 + s * 0.32, cy - s * 0.05], fill=_shade(col, 0.92))
        face(d, cx, cy - s * 0.4, s * 0.55, mood=mood, blink=math.sin(t * 1.1))
        return cx, cy
    # generic round animals
    palette = {
        "dog": (230, 180, 120), "cat": (250, 205, 150), "cow": (245, 245, 240),
        "sheep": (250, 248, 242), "monkey": (225, 170, 120), "frog": (140, 210, 120),
        "pig": (255, 190, 200), "chick": (255, 225, 90), "panda": (250, 250, 252),
    }
    col = palette.get(kind, (230, 200, 150))
    # body
    d.ellipse([cx - s * 0.85, cy + s * 0.05, cx + s * 0.85, cy + s * 1.15], fill=col)
    # legs
    for dx in (-0.45, 0.45):
        d.ellipse([cx + s * dx - s * 0.14, cy + s * 0.95, cx + s * dx + s * 0.14, cy + s * 1.3],
                  fill=_shade(col, 0.85))
    # tail
    if kind in ("dog", "cat", "monkey", "pig"):
        tw = math.sin(t * 7.0) * s * 0.2
        d.arc([cx + s * 0.7, cy + s * 0.25, cx + s * 1.25, cy + s * 0.75], 250, 400,
              fill=col, width=max(4, int(s * 0.1)))
        d.ellipse([cx + s * 1.1, cy + s * 0.5 + tw * 0.4, cx + s * 1.3, cy + s * 0.7 + tw * 0.4],
                  fill=col)
    # head
    hr = s * 0.6
    d.ellipse([cx - hr, cy - hr * 1.15, cx + hr, cy + hr * 0.5], fill=col)
    if kind == "dog":
        for sx in (-1, 1):
            d.ellipse([cx + sx * hr * 0.55 - hr * 0.4, cy - hr * 1.35,
                       cx + sx * hr * 0.55 + hr * 0.4, cy - hr * 0.3], fill=_shade(col, 0.82))
        d.ellipse([cx - hr * 0.3, cy + hr * 0.05, cx + hr * 0.3, cy + hr * 0.4],
                  fill=(60, 40, 40))   # snout
        d.ellipse([cx - hr * 0.07, cy + hr * 0.1, cx + hr * 0.07, cy + hr * 0.22], fill=(20, 20, 20))
    elif kind == "cat":
        for sx in (-1, 1):
            d.polygon([(cx + sx * hr * 0.45, cy - hr * 0.95), (cx + sx * hr * 0.85, cy - hr * 1.5),
                       (cx + sx * hr * 0.95, cy - hr * 0.6)], fill=col)
        d.polygon([(cx - hr * 0.14, cy + hr * 0.3), (cx, cy + hr * 0.5), (cx + hr * 0.14, cy + hr * 0.3)], fill=(255, 120, 120))
    elif kind == "cow":
        for sx in (-1, 1):
            d.ellipse([cx + sx * hr * 0.75 - hr * 0.16, cy - hr * 1.15,
                       cx + sx * hr * 0.75 + hr * 0.16, cy - hr * 0.8], fill=(240, 225, 190))
        for px, py, pr in ((-0.45, 0.0, 0.22), (0.5, 0.35, 0.18), (-0.1, 0.8, 0.15)):
            d.ellipse([cx + px * hr - pr * hr, cy + hr * 0.4 + py * hr - pr * hr,
                       cx + px * hr + pr * hr, cy + hr * 0.4 + py * hr + pr * hr],
                      fill=(70, 60, 60))
        d.ellipse([cx - hr * 0.32, cy + hr * 0.08, cx + hr * 0.32, cy + hr * 0.42],
                  fill=(250, 225, 210))  # snout
        d.ellipse([cx - hr * 0.18, cy + hr * 0.18, cx - hr * 0.06, cy + hr * 0.3], fill=(150, 90, 90))
        d.ellipse([cx + hr * 0.06, cy + hr * 0.18, cx + hr * 0.18, cy + hr * 0.3], fill=(150, 90, 90))
    elif kind == "sheep":
        for k in range(9):
            ang = k * 2.51
            d.ellipse([cx + math.cos(ang) * hr * 0.85 - hr * 0.35, cy - hr * 0.4 + math.sin(ang) * hr * 0.8 - hr * 0.35,
                       cx + math.cos(ang) * hr * 0.85 + hr * 0.35, cy - hr * 0.4 + math.sin(ang) * hr * 0.8 + hr * 0.35],
                      fill=(252, 250, 246))
        d.ellipse([cx - hr * 0.62, cy - hr * 0.62, cx + hr * 0.62, cy + hr * 0.5], fill=(60, 50, 55))
        face(d, cx, cy - hr * 0.08, hr * 0.6, mood=mood, blink=math.sin(t * 1.3))
        return cx, cy
    elif kind == "monkey":
        for sx in (-1, 1):
            d.ellipse([cx + sx * hr * 0.8 - hr * 0.28, cy - hr * 1.0,
                       cx + sx * hr * 0.8 + hr * 0.28, cy - hr * 0.3], fill=_shade(col, 0.8))
            d.ellipse([cx + sx * hr * 0.8 - hr * 0.18, cy - hr * 0.9,
                       cx + sx * hr * 0.8 + hr * 0.18, cy - hr * 0.4], fill=(255, 220, 190))
        d.ellipse([cx - hr * 0.6, cy + hr * 0.0, cx + hr * 0.6, cy + hr * 0.5],
                  fill=(255, 225, 195))  # muzzle
        # curling tail
        d.arc([cx + s * 0.75, cy + s * 0.35, cx + s * 1.2, cy + s * 0.85], 90, 380,
              fill=col, width=max(4, int(s * 0.12)))
    elif kind == "frog":
        d.ellipse([cx - hr * 0.55, cy - hr * 1.2, cx + hr * 0.55, cy - hr * 0.4],
                  fill=_shade(col, 0.95))
        d.ellipse([cx - hr * 0.55, cy - hr * 1.25, cx - hr * 0.15, cy - hr * 0.55], fill=col)
        d.ellipse([cx + hr * 0.15, cy - hr * 1.25, cx + hr * 0.55, cy - hr * 0.55], fill=col)
        face(d, cx, cy - hr * 0.45, hr * 0.7, mood=mood, blink=math.sin(t * 1.0))
        return cx, cy
    elif kind == "pig":
        d.ellipse([cx - hr * 0.34, cy + hr * 0.05, cx + hr * 0.34, cy + hr * 0.4],
                  fill=(255, 160, 175))   # snout
        d.ellipse([cx - hr * 0.2, cy + hr * 0.12, cx - hr * 0.06, cy + hr * 0.26], fill=(220, 110, 130))
        d.ellipse([cx + hr * 0.06, cy + hr * 0.12, cx + hr * 0.2, cy + hr * 0.26], fill=(220, 110, 130))
    elif kind == "chick":
        for sx in (-1, 1):
            d.polygon([(cx + sx * hr * 0.3, cy - hr * 0.9), (cx + sx * hr * 0.45, cy - hr * 1.35),
                       (cx + sx * hr * 0.7, cy - hr * 0.75)], fill=(250, 180, 60))
        d.polygon([(cx - hr * 0.1, cy + hr * 0.35), (cx, cy + hr * 0.55), (cx + hr * 0.1, cy + hr * 0.35)], fill=(255, 140, 60))
    face(d, cx, cy - hr * 0.35, hr * 0.75, mood=mood, blink=math.sin(t * 1.25 + 0.5))
    return cx, cy


# ---------------------------------------------------------------- props
def bus(d, cx, cy, s, t=0.0, passengers=(), road=True, wipers=False, horn=False,
        scroll=0.0, body=(255, 200, 60)):
    """Classic yellow school bus. s = bus height ~ radius. passengers: animal kinds."""
    bob = math.sin(t * 4.0) * s * 0.02
    cy = cy + bob
    # road
    if road:
        d.rounded_rectangle([0, cy + s * 0.95, W, cy + s * 1.5], radius=int(s*0.2), fill=(120, 120, 135))
        for k in range(int(scroll) % 3 + 0, 8):
            x = (k * W / 7 - (scroll % (W / 7)))
            d.rectangle([x, cy + s * 1.2, x + s * 0.5, cy + s * 1.28], fill=(250, 250, 250))
    # body
    d.rounded_rectangle([cx - s * 1.7, cy - s * 0.55, cx + s * 1.7, cy + s * 0.95],
                        radius=int(s * 0.22), fill=body)
    # roof stripe
    d.rounded_rectangle([cx - s * 1.7, cy - s * 0.55, cx + s * 1.7, cy - s * 0.35],
                        radius=int(s * 0.2), fill=_shade(body, 0.88))
    # windows (with passengers)
    kinds = list(passengers) or ["dog", "cat", "duck"]
    for i in range(3):
        wx = cx - s * 1.28 + i * s * 0.95
        d.rounded_rectangle([wx - s * 0.36, cy - s * 0.34, wx + s * 0.36, cy + s * 0.4],
                            radius=int(s * 0.16), fill=(190, 235, 255))
        if i < len(kinds):
            k = kinds[i]
            # little head in window
            hr = s * 0.2
            hy = cy + s * 0.16 - abs(math.sin(t * 4.0 + i)) * s * 0.06
            pal = {"dog": (230, 180, 120), "cat": (250, 205, 150), "duck": (255, 220, 90),
                   "cow": (245, 245, 240), "monkey": (225, 170, 120), "sheep": (250, 250, 246),
                   "pig": (255, 190, 200), "frog": (140, 210, 120), "chick": (255, 225, 90)}
            c = pal.get(k, (230, 200, 150))
            d.ellipse([wx - hr, hy - hr, wx + hr, hy + hr], fill=c)
            if k == "cat":
                for sx in (-1, 1):
                    d.polygon([(wx + sx * hr * 0.5, hy - hr * 0.8), (wx + sx * hr * 0.8, hy - hr * 1.25),
                               (wx + sx * hr * 0.9, hy - hr * 0.5)], fill=c)
            if k == "dog":
                for sx in (-1, 1):
                    d.ellipse([wx + sx * hr * 0.5 - hr * 0.35, hy - hr * 1.1,
                               wx + sx * hr * 0.5 + hr * 0.35, hy - hr * 0.4], fill=_shade(c, 0.82))
            if k == "duck" or k == "chick":
                d.polygon([(wx + hr * 0.6, hy - hr * 0.2), (wx + hr * 1.1, hy), (wx + hr * 0.6, hy + hr * 0.25)],
                          fill=(255, 150, 40))
            if k == "sheep":
                d.ellipse([wx - hr * 0.75, hy - hr * 0.75, wx + hr * 0.75, hy + hr * 0.75], fill=(252, 250, 246))
                d.ellipse([wx - hr * 0.5, hy - hr * 0.5, wx + hr * 0.5, hy + hr * 0.4], fill=(60, 50, 55))
            d.ellipse([wx - hr * 0.45, hy - hr * 0.15, wx - hr * 0.15, hy + hr * 0.15], fill=(40, 34, 44))
            d.ellipse([wx + hr * 0.15, hy - hr * 0.15, wx + hr * 0.45, hy + hr * 0.15], fill=(40, 34, 44))
    # door
    dx = cx + s * 1.45
    d.rounded_rectangle([dx - s * 0.25, cy - s * 0.25, dx + s * 0.25, cy + s * 0.9],
                        radius=int(s * 0.12), fill=_shade(body, 0.8))
    # headlight + bumper
    d.ellipse([cx + s * 1.58, cy + s * 0.5, cx + s * 1.82, cy + s * 0.74], fill=(255, 250, 200))
    d.rounded_rectangle([cx - s * 1.75, cy + s * 0.82, cx + s * 1.75, cy + s * 0.98],
                        radius=int(s * 0.08), fill=(90, 90, 100))
    # wheels (rotating)
    for wx in (cx - s * 0.95, cx + s * 0.85):
        wr = s * 0.3
        wy = cy + s * 0.95
        d.ellipse([wx - wr, wy - wr, wx + wr, wy + wr], fill=(50, 50, 60))
        d.ellipse([wx - wr * 0.55, wy - wr * 0.55, wx + wr * 0.55, wy + wr * 0.55], fill=(230, 230, 235))
        ang = t * 5.0
        for k in range(4):
            a = ang + k * math.pi / 2
            d.line([wx, wy, wx + math.cos(a) * wr * 0.55, wy + math.sin(a) * wr * 0.55],
                   fill=(120, 120, 130), width=max(3, int(s * 0.04)))
    # wipers
    if wipers:
        ph = math.sin(t * 3.4) * 0.5
        for i in range(3):
            wx = cx - s * 1.28 + i * s * 0.95
            d.arc([wx - s * 0.5, cy - s * 0.6, wx + s * 0.5, cy + s * 0.4],
                  200 - ph * 30, 260 - ph * 30, fill=(60, 60, 70), width=max(3, int(s * 0.05)))
        for k in range(10):
            rx = (k * 271 + int(t * 900)) % W
            ry = (k * 173 + int(t * 1400)) % (H * 0.6)
            d.line([rx, ry, rx - 12, ry + 34], fill=(150, 200, 255), width=4)
    # horn rings
    if horn:
        ph = (t * 1.6) % 1
        for k in range(3):
            r = (ph + k * 0.33) * s * 1.4
            d.arc([cx + s * 1.2 - r, cy - s * 0.1 - r, cx + s * 1.2 + r, cy - s * 0.1 + r],
                  -80, 80, fill=(255, 120, 120), width=max(3, int(s * 0.06)))
    return cx, cy


def bed(d, cx, cy, s, t=0.0, headboard=(150, 100, 160), blanket=(120, 180, 240)):
    d.rounded_rectangle([cx - s * 1.6, cy - s * 0.6, cx + s * 1.6, cy + s * 0.55],
                        radius=int(s * 0.2), fill=_shade(headboard, 0.9))
    d.rounded_rectangle([cx - s * 1.5, cy - s * 0.5, cx + s * 1.5, cy + s * 0.35],
                        radius=int(s * 0.15), fill=(255, 255, 255))      # mattress
    d.rounded_rectangle([cx - s * 1.55, cy + s * 0.15, cx + s * 1.55, cy + s * 0.55],
                        radius=int(s * 0.18), fill=blanket)             # blanket
    d.ellipse([cx - s * 1.15, cy - s * 0.45, cx - s * 0.65, cy - s * 0.0],
              fill=(255, 245, 230))                                     # pillow
    # headboard posts
    for sx in (-1, 1):
        d.rounded_rectangle([cx + sx * s * 1.6 - s * 0.12, cy - s * 1.15,
                             cx + sx * s * 1.6 + s * 0.12, cy - s * 0.3],
                            radius=int(s * 0.1), fill=headboard)
        d.ellipse([cx + sx * s * 1.6 - s * 0.2, cy - s * 1.35,
                   cx + sx * s * 1.6 + s * 0.2, cy - s * 0.95], fill=(255, 170, 200))
    # legs
    for sx in (-1, 1):
        d.rectangle([cx + sx * s * 1.4 - s * 0.1, cy + s * 0.55,
                     cx + sx * s * 1.4 + s * 0.1, cy + s * 0.95], fill=headboard)
    return cx, cy


def star_prop(d, cx, cy, r, t=0.0, color=(255, 215, 90), face_on=True):
    tw = 1 + math.sin(t * 3.0) * 0.08
    r = r * tw
    pts = []
    for i in range(10):
        rad = r if i % 2 == 0 else r * 0.45
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    d.polygon(pts, fill=color)
    for k in range(4):
        a = t * 0.8 + k * math.pi / 2
        d.line([cx + math.cos(a) * r * 1.15, cy + math.sin(a) * r * 1.15,
                cx + math.cos(a) * r * 1.45, cy + math.sin(a) * r * 1.45],
               fill=(255, 240, 150), width=6)
    if face_on:
        face(d, cx, cy - r * 0.05, r * 0.55, mood="happy", blink=math.sin(t * 1.2))


def cloud(d, cx, cy, s, color=(255, 255, 255)):
    for dx, dy, rr in ((-0.5, 0.1, 0.55), (0, -0.25, 0.75), (0.55, 0.1, 0.6), (0, 0.3, 0.8)):
        d.ellipse([cx + dx * s - rr * s, cy + dy * s - rr * s,
                   cx + dx * s + rr * s, cy + dy * s + rr * s], fill=color)


def rainbow(d, cx, cy, s, alpha_colors=None):
    colors = alpha_colors or [(255, 100, 100), (255, 180, 80), (255, 235, 100),
                              (130, 220, 120), (110, 190, 250), (170, 140, 240)]
    for i, c in enumerate(colors):
        r = s * (1 - i * 0.09)
        d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=c, width=max(8, int(s * 0.09)))


def tree(d, cx, cy, s, t=0.0):
    d.rectangle([cx - s * 0.12, cy, cx + s * 0.12, cy + s * 1.1], fill=(140, 95, 55))
    sway = math.sin(t * 1.5) * s * 0.04
    d.ellipse([cx - s * 0.85 + sway, cy - s * 1.15, cx + s * 0.85 + sway, cy + s * 0.15],
              fill=(90, 190, 110))
    d.ellipse([cx - s * 0.5 + sway, cy - s * 1.35, cx + s * 0.4 + sway, cy - s * 0.75],
              fill=(110, 210, 120))


def house(d, cx, cy, s, color=(255, 180, 120)):
    d.rectangle([cx - s, cy, cx + s, cy + s * 0.95], fill=(250, 240, 225))
    d.polygon([(cx - s * 1.15, cy), (cx, cy - s * 0.75), (cx + s * 1.15, cy)], fill=color)
    d.rounded_rectangle([cx - s * 0.22, cy + s * 0.35, cx + s * 0.22, cy + s * 0.95],
                        radius=int(s * 0.1), fill=(150, 100, 70))
    d.rectangle([cx - s * 0.75, cy + s * 0.2, cx - s * 0.35, cy + s * 0.6], fill=(180, 225, 250))
    d.rectangle([cx + s * 0.35, cy + s * 0.2, cx + s * 0.75, cy + s * 0.6], fill=(180, 225, 250))


def confetti(d, t, seed=1):
    import random
    rnd = random.Random(seed)
    cols = [(255, 120, 140), (255, 214, 90), (110, 200, 250), (130, 230, 140),
            (200, 140, 255), (255, 160, 90)]
    for k in range(40):
        ph = (t * 0.35 + rnd.random()) % 1
        x = rnd.randint(40, W - 40)
        y = ph * H
        c = cols[k % len(cols)]
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=c)


def _shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)
