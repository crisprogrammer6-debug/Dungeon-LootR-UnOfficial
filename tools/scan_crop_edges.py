from pathlib import Path
import numpy as np
from PIL import Image

SRC = Path(
    r"C:\Users\koke_\.cursor\projects\c-Users-koke-LootR-web-Unnoficial\assets"
    r"\c__Users_koke__AppData_Roaming_Cursor_User_workspaceStorage_"
    r"d804e58a312bcbacf7007f490e68ec7b_images_image-80ea0de6-b5bf-489b-b57b-2b4569a16b81.png"
)
a = np.array(Image.open(SRC).convert("RGB")).astype(int)

def dump(label, xs, y0, y1):
    print(label)
    for x in xs:
        sl = a[y0:y1, x]
        print(f"  x={x:3d} lum={sl.mean():.1f} rgb={tuple(int(v) for v in sl.mean(0))}")

def dumpy(label, ys, x0, x1):
    print(label)
    for y in ys:
        sl = a[y, x0:x1]
        print(f"  y={y:3d} lum={sl.mean():.1f}")

dump("jackals left", range(100, 120), 230, 328)
dump("jackals right", range(185, 210), 230, 328)
dumpy("jackals y", range(226, 340), 110, 192)
print("--- katana ref ---")
dump("katana left", range(100, 120), 120, 217)
dump("katana right", range(185, 210), 120, 217)
dumpy("katana y", range(116, 222), 110, 192)
