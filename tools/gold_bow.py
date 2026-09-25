from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

SRC = Path(r"C:\Users\koke_\LootR web Unnoficial\tools\debug\matte-56.png")
TEMPEST = Path(r"C:\Users\koke_\LootR web Unnoficial\assets\img\tempest.png")
OUT = Path(r"C:\Users\koke_\LootR web Unnoficial\assets\img")
SIZE = 512
SS = 560


def tempest_ramp(bins=256):
    arr = np.asarray(Image.open(TEMPEST).convert("RGBA"))
    m = arr[:, :, 3] > 200
    rgb = arr[m, :3].astype(np.float32)
    luma = rgb @ np.array([0.3, 0.55, 0.15], dtype=np.float32)
    # Skip near-black recesses so the bow reads as the same bright gold as the crest.
    keep = luma > 70
    rgb = rgb[keep][np.argsort(luma[keep])]
    idx = np.linspace(0, len(rgb) - 1, bins).astype(np.int32)
    return rgb[idx]


src = Image.open(SRC).convert("RGBA")
bbox = src.getbbox()
src = src.crop(bbox)
fit = (SS * 0.72) / max(src.size)
hi = src.resize((max(1, int(src.width * fit)), max(1, int(src.height * fit))), Image.Resampling.LANCZOS)
arr = np.asarray(hi).astype(np.float32)
alpha = arr[:, :, 3] / 255.0
luma = (arr[:, :, 0] * 0.3 + arr[:, :, 1] * 0.5 + arr[:, :, 2] * 0.2) / 255.0
luma = np.where(alpha > 0.04, np.clip(luma / np.maximum(alpha, 0.08), 0, 1), 0)
# Stretch original shading so it uses the full Tempest gold range.
if luma[alpha > 0.2].size:
    lo, hi_v = np.percentile(luma[alpha > 0.2], [8, 96])
    luma = np.clip((luma - lo) / max(hi_v - lo, 1e-3), 0, 1)

ramp = tempest_ramp()
idx = np.clip((luma * (len(ramp) - 1)).astype(np.int32), 0, len(ramp) - 1)
rgb = ramp[idx]

height = (
    np.asarray(Image.fromarray((alpha * 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(1.4))).astype(
        np.float32
    )
    / 255.0
)
gy, gx = np.gradient(height)
norm = np.sqrt(gx * gx + gy * gy + 0.16) + 1e-6
ndotl = np.clip((-gx / norm) * -0.2 + (-gy / norm) * -0.92 + (0.16 / norm) * 0.8, 0, 1)
detail = luma - (
    np.asarray(Image.fromarray((luma * 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(3.2))).astype(
        np.float32
    )
    / 255.0
)
rgb = np.clip(
    rgb * (0.74 + ndotl * 0.5)[..., None]
    + (ndotl ** 16)[..., None] * 110.0
    + detail[..., None] * 90.0,
    0,
    255,
)

# Harder matte: same silhouette, no muddy halo.
alpha = np.clip((alpha - 0.1) / 0.78, 0, 1)
alpha = alpha * alpha * (3 - 2 * alpha)

out = np.zeros(arr.shape, dtype=np.uint8)
out[..., :3] = rgb.astype(np.uint8)
out[..., 3] = np.clip(alpha * 255, 0, 255).astype(np.uint8)
emblem = Image.fromarray(out, "RGBA")
emblem = ImageEnhance.Contrast(emblem).enhance(1.18)
emblem = ImageEnhance.Color(emblem).enhance(1.1)
emblem = ImageEnhance.Sharpness(emblem).enhance(1.55)

if max(emblem.size) > SIZE - 48:
    ratio = (SIZE - 48) / max(emblem.size)
    emblem = emblem.resize(
        (max(1, int(emblem.width * ratio)), max(1, int(emblem.height * ratio))),
        Image.Resampling.LANCZOS,
    )
canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
canvas.paste(emblem, ((SIZE - emblem.width) // 2, (SIZE - emblem.height) // 2), emblem)
canvas.save(OUT / "ruin.png")
canvas.save(OUT / "umbral.png")
print("saved", src.size, "->", emblem.size)
