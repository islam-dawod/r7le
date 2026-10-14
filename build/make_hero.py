# -*- coding: utf-8 -*-
"""Set the Sydney photo (firstimg.jpeg) as the hero image, preserving the
previous airplane hero as travel.jpg for use on other pages."""
from PIL import Image
import os
import shutil

OUT = "assets/img/photos"

# 1) preserve current hero (airplane) as travel.jpg
cur = os.path.join(OUT, "hero.jpg")
if os.path.exists(cur):
    shutil.copyfile(cur, os.path.join(OUT, "travel.jpg"))
    print("travel.jpg <- previous hero.jpg")


def cover(img, w, h):
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    img = img.resize((round(iw * scale), round(ih * scale)), Image.LANCZOS)
    iw, ih = img.size
    left = (iw - w) // 2
    top = (ih - h) // 2
    return img.crop((left, top, left + w, top + h))


# 2) new hero.jpg = Sydney, 3:2 landscape
src = Image.open("firstimg.jpeg").convert("RGB")
hero = cover(src, 1500, 1000)
hero.save(os.path.join(OUT, "hero.jpg"), "JPEG", quality=84, optimize=True, progressive=True)
print("hero.jpg (Sydney)", hero.size, os.path.getsize(os.path.join(OUT, "hero.jpg")) // 1024, "KB")
