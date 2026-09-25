from pathlib import Path
from PIL import Image

SRC = Path(
    r"C:\Users\koke_\.cursor\projects\c-Users-koke-LootR-web-Unnoficial\assets"
    r"\c__Users_koke__AppData_Roaming_Cursor_User_workspaceStorage_"
    r"d804e58a312bcbacf7007f490e68ec7b_images_image-80ea0de6-b5bf-489b-b57b-2b4569a16b81.png"
)
OUT = Path(r"C:\Users\koke_\LootR web Unnoficial\assets\img\materials")
W, H = 118, 112

# Twin Jackals: keep left gold (x=105, same as katana). Bottom at own rim.
# Demon Twin Guns: crop to its gold frame (no extra side gutter) so it fills 118x112.
FIX = {
    "twin-jackals": (105, 230, 198, 328),
    "demon-twin-guns": (307, 230, 402, 328),
}

im = Image.open(SRC).convert("RGBA")
for slug, box in FIX.items():
    tile = im.crop(box).resize((W, H), Image.Resampling.LANCZOS)
    tile.save(OUT / f"{slug}.png")
    print(slug, box, "->", tile.size)
