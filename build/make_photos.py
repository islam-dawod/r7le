# -*- coding: utf-8 -*-
"""Process source photos (from .src-photos) into optimized web assets, and
generate a flat brand illustration for Australia. Run from repo root."""
from PIL import Image, ImageDraw, ImageFilter
import os

SRC = ".src-photos"
OUT = "assets/img/photos"
os.makedirs(OUT, exist_ok=True)


def cover(img, w, h):
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    img = img.resize((round(iw * scale), round(ih * scale)), Image.LANCZOS)
    iw, ih = img.size
    left = (iw - w) // 2
    top = (ih - h) // 2
    return img.crop((left, top, left + w, top + h))


def save(img, name, q=82):
    p = os.path.join(OUT, name)
    img.convert("RGB").save(p, "JPEG", quality=q, optimize=True, progressive=True)
    print(name, img.size, os.path.getsize(p) // 1024, "KB")


save(cover(Image.open(os.path.join(SRC, "hero.png")), 1100, 1000), "hero.jpg", 84)
save(cover(Image.open(os.path.join(SRC, "usa.jpg")), 820, 512), "usa.jpg")
save(cover(Image.open(os.path.join(SRC, "canada.jpg")), 820, 512), "canada.jpg")
save(cover(Image.open(os.path.join(SRC, "art_appt.jpg")), 900, 600), "appointment.jpg")

# ---- Australia: clean flat brand illustration (Sydney sails + Harbour Bridge) ----
W, H = 1640, 1024
im = Image.new("RGB", (W, H))
px = im.load()
top = (0x12, 0x6E, 0x7D)
bot = (0x7E, 0xC8, 0xD0)
for y in range(H):
    t = y / H
    r = int(top[0] + (bot[0] - top[0]) * t)
    g = int(top[1] + (bot[1] - top[1]) * t)
    b = int(top[2] + (bot[2] - top[2]) * t)
    row = (r, g, b)
    for x in range(W):
        px[x, y] = row
d = ImageDraw.Draw(im, "RGBA")
d.ellipse([W - 430, 90, W - 170, 350], fill=(0xF2, 0xA5, 0x16, 230))
d.ellipse([W - 470, 50, W - 130, 390], fill=(0xF2, 0xA5, 0x16, 60))
waterY = int(H * 0.70)
navy = (0x07, 0x23, 0x2A, 255)
bx0, bx1 = 150, 760
arc_top = waterY - 300
d.arc([bx0, arc_top, bx1, waterY + 120], 200, 340, fill=navy, width=26)
d.rectangle([bx0 - 10, waterY - 70, bx1 + 10, waterY - 44], fill=navy)
for px0 in (bx0 - 6, bx1 - 14):
    d.rectangle([px0, waterY - 150, px0 + 22, waterY - 44], fill=navy)
# bridge hangers: evenly spaced vertical lines from the arch down to the deck
import math
deckY = waterY - 70
for i in range(1, 16):
    hx = bx0 + i * ((bx1 - bx0) / 16)
    # y on the arc ellipse (lower half) at this x
    a = (bx1 - bx0) / 2.0
    bb = (waterY + 120 - arc_top) / 2.0
    cx0 = (bx0 + bx1) / 2.0
    cy0 = (arc_top + waterY + 120) / 2.0
    val = 1 - ((hx - cx0) / a) ** 2
    if val <= 0:
        continue
    ay = cy0 - bb * math.sqrt(val)
    if ay < deckY - 6:
        d.line([hx, ay, hx, deckY], fill=navy, width=4)

# Opera House: clean leaning white sails (triangles) rising from the waterline
base = waterY + 8
sails = [(905, 70, 150, 16), (975, 82, 205, 10), (1055, 92, 255, 0),
         (1150, 80, 205, -10), (1225, 62, 150, -16)]
for cx, half, h, lean in sails:
    d.polygon([(cx - half, base), (cx + half, base), (cx + lean, base - h)],
              fill=(255, 255, 255, 255))
d.rectangle([0, waterY, W, H], fill=(0x0A, 0x55, 0x60, 255))
for rx in (975, 1150):
    d.line([rx, waterY + 30, rx, waterY + 95], fill=(255, 255, 255, 70), width=7)
im = im.filter(ImageFilter.SMOOTH)
save(cover(im, 820, 512), "australia.jpg", 86)
