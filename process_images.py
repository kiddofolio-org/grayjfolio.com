#!/usr/bin/env python3
"""Process Gray's first art batch into web images.
Pipeline (matches Willa's): Pillow .thumbnail((1600,1600)) -> -full.jpg,
.thumbnail((800,800)) -> -thumb.jpg. Source files are already JPEGs.
"""
import os
from PIL import Image, ImageOps

SRC = "/home/user/workspace/uploaded_attachments/e88ea644157b4703ab72810e5d753c16"
OUT = "/home/user/workspace/grayjfolio.com/assets"
os.makedirs(OUT, exist_ok=True)

# Archive order, NEWEST FIRST within the 2024–25 group.
# slug -> source filename
MAP = [
    ("gray-01", "unknown-date-1.jpg"),
    ("gray-02", "unknown-date-2.jpg"),
    ("gray-03", "unknown-date-3.jpg"),
    ("gray-04", "unknown-date-4.jpg"),
    ("gray-05", "unknown-date-5.jpg"),
    ("gray-06", "unknown-date-6-jacques.jpg"),
    ("gray-07", "8-24-2024.jpg"),
    ("gray-08", "8-24-2024ii.jpg"),
    ("gray-09", "7-29-2024.jpg"),
    ("gray-10", "2-22-24.jpg"),
]

def save_variant(img, path, max_side):
    im = img.copy()
    im.thumbnail((max_side, max_side), Image.LANCZOS)
    if im.mode != "RGB":
        im = im.convert("RGB")
    im.save(path, "JPEG", quality=88, optimize=True)
    return im.size

for slug, fname in MAP:
    src_path = os.path.join(SRC, fname)
    with Image.open(src_path) as img:
        img = ImageOps.exif_transpose(img)  # honor camera orientation
        full = os.path.join(OUT, f"{slug}-full.jpg")
        thumb = os.path.join(OUT, f"{slug}-thumb.jpg")
        fs = save_variant(img, full, 1600)
        ts = save_variant(img, thumb, 800)
        print(f"{slug}: {fname}  full={fs}  thumb={ts}")

print(f"\nProcessed {len(MAP)} images.")
