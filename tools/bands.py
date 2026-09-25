from pathlib import Path
from PIL import Image

src = Path(
    r"C:\Users\koke_\.cursor\projects\c-Users-koke-LootR-web-Unnoficial\assets\c__Users_koke__AppData_Roaming_Cursor_User_workspaceStorage_d804e58a312bcbacf7007f490e68ec7b_images_image-f4ce226d-299a-497b-9e4c-e189e35fa36b.png"
)
dbg = Path(r"C:\Users\koke_\LootR web Unnoficial\assets")
im = Image.open(src).convert("RGBA")
# save bands
for i, y0 in enumerate(range(90, 800, 70)):
    im.crop((120, y0, 850, y0 + 70)).save(dbg / f"band_{i}_{y0}.png")
    print("band", i, y0)
