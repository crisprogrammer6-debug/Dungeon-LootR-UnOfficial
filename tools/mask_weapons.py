"""Punch black backgrounds and mask original katanas."""
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(r"C:\Users\koke_\LootR web Unnoficial\assets\img\weapons")
ROOT.mkdir(parents=True, exist_ok=True)
PROJ = Path(r"C:\Users\koke_\.cursor\projects\c-Users-koke-LootR-web-Unnoficial\assets")


def punch_black(src: Path, dest: Path, thresh: int = 22):
    im = Image.open(src).convert("RGBA")
    arr = np.array(im)
    r, g, b, a = arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3]
    dark = (r.astype(int) + g.astype(int) + b.astype(int)) < thresh * 3
    arr[..., 3] = np.where(dark, 0, a)
    out = Image.fromarray(arr)
    bbox = out.getbbox()
    if bbox:
        out = out.crop(bbox)
    out.save(dest)
    print("punched", dest.name, out.size)


def mask_katana(src: Path, dest: Path, crop, blade_dark=True):
    im = Image.open(src).convert("RGBA")
    im = im.crop(crop)
    arr = np.array(im).astype(np.int16)
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    # drop UI reds and green bars
    red_ui = (r > 140) & (g < 80) & (b < 70)
    green_ui = (g > 90) & (g > r + 20) & (g > b)
    # drop skin / yellow-beige character
    skin = (r > 150) & (g > 110) & (b > 70) & (r > b + 20) & (g > b)
    # drop pink awning
    pink = (r > 160) & (b > 140) & (g > 90) & (g < 180)
    # drop warm wall / wood
    wall = (r > 90) & (g > 85) & (b > 60) & (abs(r - g) < 45) & (b < r + 10) & (r + g + b > 280)
    # drop blue window-ish
    sky = (b > r + 25) & (b > 80) & (g > 70)
    keep_metal = (np.maximum(r, np.maximum(g, b)) - np.minimum(r, np.minimum(g, b)) < 28) & (
        (r + g + b) > 90
    )
    keep_gold = (r > 140) & (g > 90) & (b < 90) & (r > b + 40)
    keep_blade = keep_metal | keep_gold
    if blade_dark:
        keep_blade = keep_blade | ((r + g + b < 220) & (np.abs(r - g) < 40) & (np.abs(g - b) < 40) & (r < 90))
    alpha = np.where(keep_blade & ~red_ui & ~green_ui & ~skin & ~pink & ~wall & ~sky, 255, 0).astype(
        np.uint8
    )
    out = arr.astype(np.uint8)
    out[..., 3] = alpha
    img = Image.fromarray(out)
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    img.save(dest)
    print("masked", dest.name, img.size)


# AI punches
ai = {
    "weapon-default.png": "greatsword.png",
    "weapon-bastion-shield.png": "shield.png",
    "weapon-bastion-spear.png": "spear.png",
    "weapon-azure-v2.png": "azure-ai.png",
    "weapon-ronin-v2.png": "ronin-ai.png",
    "weapon-azure.png": "azure-ai-old.png",
    "weapon-ronin.png": "ronin-ai-old.png",
}
for src_name, dest_name in ai.items():
    p = PROJ / src_name
    if p.exists():
        punch_black(p, ROOT / dest_name)

# Original katanas
refs = Path(
    r"C:\Users\koke_\.cursor\projects\c-Users-koke-LootR-web-Unnoficial\assets\c__Users_koke__AppData_Roaming_Cursor_User_workspaceStorage_d804e58a312bcbacf7007f490e68ec7b_images"
)
azure = refs / "image-74839129-15e9-4209-93ac-c91007f4f00a.png"
ronin = refs / "image-35789125-f21f-474d-ad92-0d465184be6e.png"
if azure.exists():
    im = Image.open(azure)
    print("azure src", im.size)
    mask_katana(azure, ROOT / "azure-src.png", (0, 80, im.width, im.height - 40))
if ronin.exists():
    im = Image.open(ronin)
    print("ronin src", im.size)
    mask_katana(ronin, ROOT / "ronin-src.png", (180, 40, im.width, im.height - 80))
