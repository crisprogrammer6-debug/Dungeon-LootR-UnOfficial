from pathlib import Path
import numpy as np
from PIL import Image

SRC = Path(
    r"C:\Users\koke_\.cursor\projects\c-Users-koke-LootR-web-Unnoficial\assets"
    r"\c__Users_koke__AppData_Roaming_Cursor_User_workspaceStorage_"
    r"d804e58a312bcbacf7007f490e68ec7b_images_image-80ea0de6-b5bf-489b-b57b-2b4569a16b81.png"
)
a = np.array(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
# bronze rim: around 70,68,60, not background 18,33,41
rim = (np.abs(r - 72) < 18) & (np.abs(g - 70) < 18) & (np.abs(b - 62) < 18) & (r > 50) & (g > 50)
# stronger: r~g, slightly brown
# project
xs = rim.mean(axis=0)
ys = rim.mean(axis=1)
print("x peaks over 0.15")
for i, v in enumerate(xs):
    if v > 0.15:
        print(i, round(float(v), 3))
print("y peaks over 0.08")
for i, v in enumerate(ys):
    if v > 0.08:
        print(i, round(float(v), 3))
Image.fromarray((rim * 255).astype(np.uint8)).save(
    r"C:\Users\koke_\LootR web Unnoficial\assets\img\materials\_inv_goldmask.png"
)
