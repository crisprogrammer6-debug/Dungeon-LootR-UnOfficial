from pathlib import Path
from PIL import Image, ImageFilter
from collections import deque

src = Path(r"C:\Users\koke_\.cursor\projects\c-Users-koke-LootR-web-Unnoficial\assets\umbral-hq.png")
dest = Path(r"C:\Users\koke_\LootR web Unnoficial\assets\img\umbral.png")
im = Image.open(src).convert("RGBA")
w, h = im.size
px = im.load()
marked = [[False] * w for _ in range(h)]
q = deque()
for x in range(w):
    q.append((x, 0)); q.append((x, h - 1))
for y in range(h):
    q.append((0, y)); q.append((w - 1, y))
while q:
    x, y = q.popleft()
    if x < 0 or y < 0 or x >= w or y >= h or marked[y][x]:
        continue
    r, g, b, _ = px[x, y]
    if max(r, g, b) >= 28:
        continue
    marked[y][x] = True
    q.extend(((x+1,y),(x-1,y),(x,y+1),(x,y-1),(x+1,y+1),(x-1,y-1),(x+1,y-1),(x-1,y+1)))
mask = Image.new("L", (w, h), 0)
mp = mask.load()
for y in range(h):
    for x in range(w):
        if marked[y][x]:
            mp[x, y] = 0
        else:
            mx = max(px[x, y][:3])
            mp[x, y] = 0 if mx < 36 else (255 if mx >= 70 else int(255 * (mx - 36) / 34))
mask = mask.filter(ImageFilter.GaussianBlur(0.8))
r, g, b, _ = im.split()
out = Image.merge("RGBA", (r, g, b, mask))
bbox = out.getbbox()
if bbox:
    out = out.crop(bbox)
pad = 24
canvas = Image.new("RGBA", (out.width + pad * 2, out.height + pad * 2), (0, 0, 0, 0))
canvas.paste(out, (pad, pad), out)
side = max(canvas.size)
sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
sq.paste(canvas, ((side - canvas.width) // 2, (side - canvas.height) // 2), canvas)
sq.resize((256, 256), Image.Resampling.LANCZOS).save(dest)
print("umbral ok")
