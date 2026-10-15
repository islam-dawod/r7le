# -*- coding: utf-8 -*-
"""Build a wide 2:1 hero banner that always shows the FULL composite photo
(top labels + bottom passports), with a softly blurred fill on the sides so
nothing is cropped at common widths."""
from PIL import Image, ImageFilter, ImageEnhance
import os

OUT = "assets/img/photos"
src = Image.open("3cbg.jpeg").convert("RGB")
sw, sh = src.size

CW, CH = 2000, 1000  # 2:1 canvas


def cover(img, w, h):
    iw, ih = img.size
    s = max(w / iw, h / ih)
    img = img.resize((round(iw * s), round(ih * s)), Image.LANCZOS)
    iw, ih = img.size
    l = (iw - w) // 2
    t = (ih - h) // 2
    return img.crop((l, t, l + w, t + h))


# blurred, slightly darkened background that fills the whole canvas
bg = cover(src, CW, CH).filter(ImageFilter.GaussianBlur(28))
bg = ImageEnhance.Brightness(bg).enhance(0.82)

# sharp full photo scaled to full canvas height, centered
fw = round(sw * CH / sh)
fg = src.resize((fw, CH), Image.LANCZOS)
x = (CW - fw) // 2
# soft feather seam: paste with a subtle shadow line
canvas = bg.copy()
canvas.paste(fg, (x, 0))

p = os.path.join(OUT, "hero.jpg")
canvas.save(p, "JPEG", quality=86, optimize=True, progressive=True)
print("hero.jpg", canvas.size, "sharp width", fw, os.path.getsize(p) // 1024, "KB")
