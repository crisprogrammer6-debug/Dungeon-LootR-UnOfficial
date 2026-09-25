from pathlib import Path
from PIL import Image

root = Path(r"C:\Users\koke_\LootR web Unnoficial\assets")
out = Path(r"C:\Users\koke_\LootR web Unnoficial\assets\img")
out.mkdir(parents=True, exist_ok=True)
src = Path(
    r"C:\Users\koke_\.cursor\projects\c-Users-koke-LootR-web-Unnoficial\assets\c__Users_koke__AppData_Roaming_Cursor_User_workspaceStorage_d804e58a312bcbacf7007f490e68ec7b_images_image-f4ce226d-299a-497b-9e4c-e189e35fa36b.png"
)
Image.open(src).crop((688, 4, 854, 86)).save(out / "logo.png")

rows = {
    "s1": Image.open(root / "s1.png").convert("RGBA"),
    "s2": Image.open(root / "s2.png").convert("RGBA"),
    "meta": Image.open(root / "meta_row.png").convert("RGBA"),
    "a1": Image.open(root / "a1.png").convert("RGBA"),
    "b1": Image.open(root / "b1.png").convert("RGBA"),
    "d1": Image.open(root / "d1.png").convert("RGBA"),
}

specs = {
    "tempest": ("s2", (174, 18, 208, 58)),
    "aegis": ("meta", (360, 18, 390, 58)),
    "ruin": ("s1", (360, 20, 392, 56)),
    "umbral": ("b1", (360, 20, 392, 56)),
    "alacrity": ("a1", (542, 18, 574, 56)),
    "fulmin": ("d1", (176, 18, 206, 56)),
}


def punch(crop):
    crop = crop.convert("RGBA")
    px = crop.load()
    for y in range(crop.height):
        for x in range(crop.width):
            r, g, b, _ = px[x, y]
            sat = max(r, g, b) - min(r, g, b)
            border = sat > 38 and (b > r + 8 or (r > g + 18 and r > 80))
            if max(r, g, b) < 62 or border:
                px[x, y] = (0, 0, 0, 0)
    bbox = crop.getbbox()
    if bbox:
        crop = crop.crop(bbox)
    w, h = crop.size
    side = max(w, h, 1) + 10
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(crop, ((side - w) // 2, (side - h) // 2), crop)
    return canvas


for name, (row, box) in specs.items():
    img = punch(rows[row].crop(box))
    img.save(out / f"{name}.png")
    img.resize((img.width * 6, img.height * 6), Image.NEAREST).save(root / f"final_{name}.png")
    print(name, img.size)
