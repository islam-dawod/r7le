# -*- coding: utf-8 -*-
"""Set the three-destinations composite (3cbg.jpeg) as the main hero image."""
from PIL import Image
import os

OUT = "assets/img/photos"
im = Image.open("3cbg.jpeg").convert("RGB")
# keep full composition (labels + passports); cap width at 1600 for the web
w = 1600
if im.size[0] > w:
    im = im.resize((w, round(im.size[1] * w / im.size[0])), Image.LANCZOS)
p = os.path.join(OUT, "hero.jpg")
im.save(p, "JPEG", quality=86, optimize=True, progressive=True)
print("hero.jpg (destinations composite)", im.size, os.path.getsize(p) // 1024, "KB")
