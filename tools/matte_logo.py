from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter, ImageEnhance

SRC = Path(
    r"C:\Users\koke_\.cursor\projects\c-Users-koke-LootR-web-Unnoficial\assets\c__Users_koke__AppData_Roaming_Cursor_User_workspaceStorage_d804e58a312bcbacf7007f490e68ec7b_images_image-69c9df42-6124-4dc5-b933-211c28147de8.png"
)
OUT_DIR = Path(r"C:\Users\koke_\LootR web Unnoficial\assets\img")
AI_DIR = Path(r"C:\Users\koke_\.cursor\projects\c-Users-koke-LootR-web-Unnoficial\assets")


def flood(crop, can_enter):
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
        if not can_enter(px[x, y]):
            continue
        marked[y][x] = True
        q.extend((
            (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
            (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1),
        ))
    return marked


def apply_mask(im, mask, pad=8):
    r, g, b, _ = im.split()
    out = Image.merge("RGBA", (r, g, b, mask))
    bbox = out.getbbox()
    if bbox:
        out = out.crop(bbox)
    canvas = Image.new("RGBA", (out.width + pad * 2, out.height + pad * 2), (0, 0, 0, 0))
    canvas.paste(out, (pad, pad), out)
    return canvas


def is_logo_plate(pixel):
    r, g, b, _ = pixel
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    sat = max(r, g, b) - min(r, g, b)
    if r >= 68 and r >= b + 8 and r >= g - 12:
        return False
    if b >= 68 and b >= r + 8:
        return False
    if r >= 90 and g >= 70:
        return False
    navy = abs(r - 25) + abs(g - 12) + abs(b - 37)
    if navy < 48 and lum < 52:
        return True
    if lum < 36 and sat < 44:
        return True
    if lum < 28:
        return True
    return False


im = Image.open(SRC).convert("RGBA")
bg = flood(im, is_logo_plate)
w, h = im.size
mask = Image.new("L", (w, h), 0)
mp = mask.load()
px = im.load()
for y in range(h):
    for x in range(w):
        if bg[y][x]:
            mp[x, y] = 0
            continue
        r, g, b, _ = px[x, y]
        lum = 0.299 * r + 0.587 * g + 0.114 * b
        sat = max(r, g, b) - min(r, g, b)
        score = max(lum, sat * 0.95)
        if score >= 70:
            mp[x, y] = 255
        elif score <= 30:
            mp[x, y] = 90
        else:
            mp[x, y] = 90 + int(165 * (score - 30) / 40)

mask = mask.filter(ImageFilter.GaussianBlur(0.85))
logo = apply_mask(im, mask, pad=10)
logo.save(OUT_DIR / "logo.png")
print("logo", logo.size)


def matte_black_icon(src: Path, dest: Path):
    im = Image.open(src).convert("RGBA")
    # shrink a bit from edges in case of jpeg ringing
    w, h = im.size
    px = im.load()

    def is_black(pixel):
        r, g, b, _ = pixel
        return max(r, g, b) < 28

    bg = flood(im, is_black)
    mask = Image.new("L", (w, h), 0)
    mp = mask.load()
    for y in range(h):
        for x in range(w):
            if bg[y][x]:
                mp[x, y] = 0
            else:
                r, g, b, _ = px[x, y]
                mx = max(r, g, b)
                if mx < 36:
                    mp[x, y] = 0
                elif mx < 70:
                    mp[x, y] = int(255 * (mx - 36) / 34)
                else:
                    mp[x, y] = 255
    mask = mask.filter(ImageFilter.GaussianBlur(0.8))
    out = apply_mask(im, mask, pad=24)
    # fit into a square canvas for consistent UI sizing
    side = max(out.width, out.height)
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.paste(out, ((side - out.width) // 2, (side - out.height) // 2), out)
    sq = sq.resize((256, 256), Image.Resampling.LANCZOS)
    sq.save(dest)
    print(dest.name, sq.size)


for name in ("tempest", "aegis", "ruin", "umbral", "alacrity", "fulmin"):
    matte_black_icon(AI_DIR / f"{name}-hq.png", OUT_DIR / f"{name}.png")
