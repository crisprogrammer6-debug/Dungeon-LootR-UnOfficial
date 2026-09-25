from pathlib import Path
from PIL import Image

SRC = Path(
    r"C:\Users\koke_\.cursor\projects\c-Users-koke-LootR-web-Unnoficial\assets\c__Users_koke__AppData_Roaming_Cursor_User_workspaceStorage_d804e58a312bcbacf7007f490e68ec7b_images_image-ec28a570-ef10-4570-b171-03cab5ccb3cc.png"
)
OUT = Path(r"C:\Users\koke_\LootR web Unnoficial\tools\debug")
OUT.mkdir(parents=True, exist_ok=True)
im = Image.open(SRC).convert("RGBA")
boxes = {
    "sinister": (325, 98, 365, 132),
    "awakened": (139, 228, 176, 269),
    "witch": (325, 470, 365, 515),
    "artemis": (325, 408, 365, 445),
    "archer": (143, 648, 182, 688),
    "unrestricted": (321, 8, 361, 48),
}
for name, box in boxes.items():
    im.crop(box).save(OUT / f"{name}.png")
