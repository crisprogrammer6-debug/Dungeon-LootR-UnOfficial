from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

SRC = Path(r"C:\Users\koke_\LootR web Unnoficial\tools\debug\sinister.png")
OUT = Path(r"C:\Users\koke_\LootR web Unnoficial\assets\img")
DBG = Path(r"C:\Users\koke_\LootR web Unnoficial\tools\debug")
SIZE = 512


def gold_score(pixel):
    r, g, b, a = pixel
    if a < 8:
        return 0
    mx = max(r, g, b)
    if mx < 52:
        return 0
    if b > g + 22 and r < 100:
        return 0
    if b > r + 24 and b >= g:
        return 0
    if abs(r - g) < 32 and r >= 68 and g >= 58 and b <= r + 20:
        return mx
    mid = (r + g) / 2.0
    if abs(r - g) > 58:
        return 0
    if b > mid * 0.96 + 14:
        return 0
    if r < 46 or g < 34:
        return 0
    return mx


def flood_bg(crop, is_bg):
    w, h = crop.size
    px = crop.load()
    marked = [[False] * w for _ in range(h)]
    q = deque()
    for x in range(w):
        q.append((x, 0))
        q.append((x, h - 1))
    for y in range(h):
        q.append((0, y))
        q.append((w - 1, y))
    while q:
        x, y = q.popleft()
        if x < 0 or y < 0 or x >= w or y >= h or marked[y][x]:
            continue
        if not is_bg(px[x, y]):
            continue
        marked[y][x] = True
        q.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    return marked


crop = Image.open(SRC).convert("RGBA").crop((0, 5, 33, 34))
bg = flood_bg(crop, lambda p: gold_score(p) < 56)
w, h = crop.size
mask_np = np.zeros((h, w), dtype=np.uint8)
for y in range(h):
    for x in range(w):
        if not bg[y][x]:
            mask_np[y, x] = 255

rgba = np.asarray(crop).copy()
rgba[mask_np == 0] = (0, 0, 0, 0)
src = Image.fromarray(rgba, "RGBA")
mask = Image.fromarray(mask_np, "L")
bbox = src.getbbox()
src = src.crop(bbox)
mask = mask.crop(bbox)
src.save(DBG / "bow-clean-src.png")

scale = max(1, (SIZE * 74 // 100) // max(src.width, src.height))
tw, th = src.width * scale, src.height * scale
hi_rgb = src.convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
hi_a = mask.resize((tw, th), Image.Resampling.NEAREST).filter(ImageFilter.GaussianBlur(0.7))
hi = Image.merge("RGBA", (*hi_rgb.split(), hi_a))
hi = ImageEnhance.Contrast(hi).enhance(1.1)
hi = ImageEnhance.Sharpness(hi).enhance(1.55)

canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
canvas.paste(hi, ((SIZE - hi.width) // 2, (SIZE - hi.height) // 2), hi)
canvas.save(OUT / "ruin.png")
canvas.save(OUT / "umbral.png")
print("saved", src.size, "x", scale, "->", hi.size)
