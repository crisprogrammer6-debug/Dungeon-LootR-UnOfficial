from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter

SRC = Path(
    r"C:\Users\koke_\.cursor\projects\c-Users-koke-LootR-web-Unnoficial\assets\c__Users_koke__AppData_Roaming_Cursor_User_workspaceStorage_d804e58a312bcbacf7007f490e68ec7b_images_image-f4ce226d-299a-497b-9e4c-e189e35fa36b.png"
)
OUT = Path(r"C:\Users\koke_\LootR web Unnoficial\assets\img")
OUT.mkdir(parents=True, exist_ok=True)
im = Image.open(SRC).convert("RGBA")


def gold_score(pixel):
    r, g, b, _ = pixel
    mx = max(r, g, b)
    if mx < 44:
        return 0
    if b > g + 8 and r > g + 8:
        return 0
    if b > r + 14 and b >= g:
        return 0
    if abs(r - g) < 22 and r >= 78 and g >= 78 and b <= r + 10:
        return mx
    mid = (r + g) / 2.0
    if abs(r - g) > 48:
        return 0
    if b > mid * 0.92 + 8:
        return 0
    if r < 48 or g < 38:
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
        q.extend((
            (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
            (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1),
        ))
    return marked


def keep_blobs(bg, min_cells=18):
    h, w = len(bg), len(bg[0])
    seen = [[False] * w for _ in range(h)]
    keep = []
    nbr = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1))
    for y in range(h):
        for x in range(w):
            if bg[y][x] or seen[y][x]:
                continue
            cells = []
            q = deque([(x, y)])
            seen[y][x] = True
            while q:
                cx, cy = q.popleft()
                cells.append((cx, cy))
                for dx, dy in nbr:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx] and not bg[ny][nx]:
                        seen[ny][nx] = True
                        q.append((nx, ny))
            if len(cells) >= min_cells:
                keep.extend(cells)
    out = [[True] * w for _ in range(h)]
    for x, y in keep:
        out[y][x] = False
    return out


def dilate_fg(bg, steps=1):
    h, w = len(bg), len(bg[0])
    cur = bg
    for _ in range(steps):
        nxt = [row[:] for row in cur]
        for y in range(h):
            for x in range(w):
                if not cur[y][x]:
                    continue
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < w and 0 <= ny < h and not cur[ny][nx]:
                        nxt[y][x] = False
                        break
        cur = nxt
    return cur


def to_mask(bg, feather):
    h, w = len(bg), len(bg[0])
    mask = Image.new("L", (w, h), 0)
    mp = mask.load()
    for y in range(h):
        for x in range(w):
            if not bg[y][x]:
                mp[x, y] = 255
    if feather:
        mask = mask.filter(ImageFilter.GaussianBlur(feather))
    return mask


def apply(crop, mask, pad=6):
    r, g, b, _ = crop.split()
    out = Image.merge("RGBA", (r, g, b, mask))
    bbox = out.getbbox()
    if bbox:
        out = out.crop(bbox)
    w, h = out.size
    canvas = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    canvas.paste(out, (pad, pad), out)
    return canvas


SPECS = {
    "tempest": (261, 258, 304, 299),
    "aegis": (444, 103, 484, 144),
    "ruin": (438, 186, 496, 240),
    "umbral": (452, 503, 490, 542),
    "alacrity": (626, 412, 667, 456),
    "fulmin": (262, 656, 302, 699),
}

for name, box in SPECS.items():
    crop = im.crop(box)
    bg = flood_bg(crop, lambda p: gold_score(p) < 50)
    bg = keep_blobs(bg)
    bg = dilate_fg(bg, 1)
    icon = apply(crop, to_mask(bg, 0.55), pad=5)
    icon.save(OUT / f"{name}.png")
    print(name, icon.size)


def logo_alpha(pixel):
    r, g, b, _ = pixel
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    sat = max(r, g, b) - min(r, g, b)
    fire = r > 70 and r > b + 8 and r >= g
    ice = b > 70 and b > r + 8
    score = max(lum, sat * 0.85)
    if fire or ice:
        score = max(score, 90)
    if score < 26:
        return 0
    if score > 78:
        return 255
    return int(255 * (score - 26) / (78 - 26))


logo_crop = im.crop((688, 6, 852, 88))
w, h = logo_crop.size
px = logo_crop.load()
mask = Image.new("L", (w, h), 0)
mp = mask.load()
for y in range(h):
    for x in range(w):
        mp[x, y] = logo_alpha(px[x, y])
mask = mask.filter(ImageFilter.GaussianBlur(0.6))
logo = apply(logo_crop, mask, pad=4)
logo.save(OUT / "logo.png")
print("logo", logo.size)
