# -*- coding: utf-8 -*-
"""Replace the Australia illustration with the real Sydney photo
(firstimg.jpeg), matching the other destination photos' size (820x512)."""
from PIL import Image
import os

OUT = "assets/img/photos"


def cover(img, w, h):
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    img = img.resize((round(iw * scale), round(ih * scale)), Image.LANCZOS)
    iw, ih = img.size
    left = (iw - w) // 2
    top = (ih - h) // 2
    return img.crop((left, top, left + w, top + h))


src = Image.open("firstimg.jpeg").convert("RGB")
out = cover(src, 820, 512)
p = os.path.join(OUT, "australia.jpg")
out.save(p, "JPEG", quality=84, optimize=True, progressive=True)
print("australia.jpg (Sydney photo)", out.size, os.path.getsize(p) // 1024, "KB")
