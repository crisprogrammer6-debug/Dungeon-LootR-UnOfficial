import os

import numpy as np
from PIL import Image

src_dir = r"C:\Users\koke_\.cursor\projects\c-Users-koke-LootR-web-Unnoficial\assets"
out_dir = r"C:\Users\koke_\LootR web Unnoficial\assets\img\weapons"
preview_dir = os.path.join(out_dir, "_preview")
os.makedirs(out_dir, exist_ok=True)
os.makedirs(preview_dir, exist_ok=True)

files = [
    "weapon-01-katana.png",
    "weapon-02-pistols-x.png",
    "weapon-03-energy-katana.png",
    "weapon-04-wood-bow.png",
    "weapon-05-dagger.png",
    "weapon-06-greatsword.png",
    "weapon-07-gold-bow.png",
    "weapon-08-paintbrush.png",
    "weapon-09-silver-katana.png",
    "weapon-10-black-gold-bow.png",
    "weapon-11-gauntlets.png",
    "weapon-12-red-pistols-x.png",
]


def corner_rgb(arr):
    h, w = arr.shape[:2]
    pts = arr[[2, 2, h - 3, h - 3], [2, w - 3, 2, w - 3], :3].astype(np.float32)
    return pts.mean(axis=0)


def detect_mode(rgb):
    r, g, b = rgb
    if g > r + 25 and g > b + 25:
        return "green"
    if b > r + 40 and b > g + 40 and r < 80:
        return "blue"
    if r > 170 and g > 50 and b < 80 and r > b + 70:
        return "orange"
    if r > 120 and b > 70 and g < 100:
        return "magenta"
    return "magenta"


def dilate(mask):
    d = mask.copy()
    d[:-1] |= mask[1:]
    d[1:] |= mask[:-1]
    d[:, :-1] |= mask[:, 1:]
    d[:, 1:] |= mask[:, :-1]
    return d


def process(path, dest, preview):
    im = Image.open(path).convert("RGBA")
    arr = np.array(im).astype(np.float32)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
    mode = detect_mode(corner_rgb(arr))

    if mode == "green":
        spill = np.clip(g - np.maximum(r, b), 0, 255)
        screen = (g > 115) & (g > r + 32) & (g > b + 32)
        g = np.minimum(g, np.maximum(r, b) + 8)
    elif mode == "blue":
        spill = np.clip(b - np.maximum(r, g), 0, 255)
        screen = (b > 120) & (b > r + 40) & (b > g + 25) & (g < 140)
        b = np.minimum(b, np.maximum(r, g) + 12)
    elif mode == "orange":
        spill = np.clip(r - np.maximum(g, b) * 0.7, 0, 255)
        # Orange screen; protect neon green/yellow energy blade
        screen = (r > 175) & (b < 70) & (g < 165) & (g > 35) & (r > g + 35)
        # Pull leftover orange from edges without eating the blade
        orange_spill = screen | ((r > 160) & (b < 80) & (g < 170) & (r > g + 25) & (g < 180))
        r = np.where(~((g > 170) | (g > r + 10)), np.minimum(r, g + 20), r)
    else:
        spill = np.clip(np.minimum(r, b) - g, 0, 255)
        # Global magenta including enclosed holes; keep gold/red gems
        # Gold: high R, mid G, low B. Magenta: high R, low G, high B.
        screen = (
            (r > 125)
            & (g < 115)
            & (b > 55)
            & ((r - g) > 50)
            & ((b - g) > 22)
            & (b > g * 0.85)
            & (spill > 12)
        )
        mag = np.clip(np.minimum(r, b) - g, 0, 255)
        r = r - mag * 0.95
        b = b - mag * 0.95

    alpha = np.where(screen, 0.0, a)
    spill_n = spill / 255.0
    ring = dilate(screen) & (~screen)
    edge_cut = (spill_n > 0.14) & (ring | (spill_n > 0.28))
    alpha = np.where(edge_cut, alpha * np.clip(1.0 - (spill_n - 0.12) * 2.2, 0, 1), alpha)

    # Extra magenta fringe on any mode (pink outline pixels)
    mag_edge = (
        (alpha > 0)
        & (r > 110)
        & (g < 120)
        & (b > 70)
        & ((r - g) > 45)
        & ((b - g) > 20)
        & (b > g * 0.9)
    )
    alpha = np.where(mag_edge, 0.0, alpha)

    trans = alpha < 8
    r = np.where(trans, 0, np.clip(r, 0, 255))
    g = np.where(trans, 0, np.clip(g, 0, 255))
    b = np.where(trans, 0, np.clip(b, 0, 255))
    alpha = np.where(trans, 0, alpha)

    if mode == "green":
        leftover = (g > 135) & (g > r + 40) & (g > b + 40) & (alpha > 0)
    elif mode == "blue":
        leftover = (b > 140) & (b > r + 50) & (b > g + 30) & (g < 130) & (alpha > 0)
    elif mode == "orange":
        leftover = (r > 185) & (b < 65) & (g < 160) & (r > g + 40) & (alpha > 0)
    else:
        leftover = (
            (r > 130)
            & (g < 105)
            & (b > 65)
            & ((r - g) > 60)
            & ((b - g) > 25)
            & (b > g * 0.85)
            & (alpha > 0)
        )
    r = np.where(leftover, 0, r)
    g = np.where(leftover, 0, g)
    b = np.where(leftover, 0, b)
    alpha = np.where(leftover, 0, alpha)

    out = np.dstack(
        [
            np.clip(r, 0, 255).astype(np.uint8),
            np.clip(g, 0, 255).astype(np.uint8),
            np.clip(b, 0, 255).astype(np.uint8),
            np.clip(alpha, 0, 255).astype(np.uint8),
        ]
    )

    ys, xs = np.where(out[:, :, 3] > 12)
    pad = 20
    h, w = out.shape[:2]
    x0, x1 = max(0, int(xs.min()) - pad), min(w - 1, int(xs.max()) + pad)
    y0, y1 = max(0, int(ys.min()) - pad), min(h - 1, int(ys.max()) + pad)
    cropped = out[y0 : y1 + 1, x0 : x1 + 1]
    Image.fromarray(cropped, "RGBA").save(dest)

    ph, pw = cropped.shape[:2]
    chk = np.zeros((ph, pw, 3), dtype=np.uint8)
    tile = 16
    yy, xx = np.indices((ph, pw))
    dark = ((yy // tile) + (xx // tile)) % 2 == 0
    chk[dark] = (40, 40, 40)
    chk[~dark] = (180, 180, 180)
    fa = cropped[:, :, 3:4].astype(np.float32) / 255.0
    rgb = cropped[:, :, :3].astype(np.float32)
    comp = rgb * fa + chk.astype(np.float32) * (1 - fa)
    Image.fromarray(comp.astype(np.uint8), "RGB").save(preview)

    print(
        f"{os.path.basename(dest):28} mode={mode:8} {cropped.shape[1]}x{cropped.shape[0]} leftover_killed={int(leftover.sum())}"
    )


for f in files:
    src = os.path.join(src_dir, f)
    if not os.path.isfile(src):
        print("missing", src)
        continue
    process(
        src,
        os.path.join(out_dir, f),
        os.path.join(preview_dir, f.replace(".png", "-preview.png")),
    )
print("done")
