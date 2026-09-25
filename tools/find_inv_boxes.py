from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw

SRC = Path(
    r"C:\Users\koke_\.cursor\projects\c-Users-koke-LootR-web-Unnoficial\assets"
    r"\c__Users_koke__AppData_Roaming_Cursor_User_workspaceStorage_"
    r"d804e58a312bcbacf7007f490e68ec7b_images_image-80ea0de6-b5bf-489b-b57b-2b4569a16b81.png"
)
OUT = Path(r"C:\Users\koke_\LootR web Unnoficial\assets\img\materials")
REF = Image.open(OUT / "underworld-glaive.png").convert("RGBA")
W, H = REF.size

im = Image.open(SRC).convert("RGBA")
a = np.array(im.convert("RGB"))
r, g, b = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
gold = ((r > 155) & (g > 118) & (b < 100) & ((r - b) > 60)).astype(np.uint8) * 255
gold = cv2.dilate(gold, np.ones((3, 3), np.uint8), iterations=1)
gold = cv2.morphologyEx(gold, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
cnts, _ = cv2.findContours(gold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
boxes = []
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    if w > 60 and h > 70:
        boxes.append((x, y, w, h))
boxes.sort(key=lambda t: (t[1] // 40, t[0]))
print("boxes", len(boxes))
for t in boxes:
    print(t)

debug = im.copy()
d = ImageDraw.Draw(debug)
for i, (x, y, w, h) in enumerate(boxes):
    d.rectangle((x, y, x + w, y + h), outline=(255, 40, 40, 255), width=2)
    d.text((x + 3, y + 3), str(i), fill=(0, 255, 80, 255))
debug.save(OUT / "_inv_boxes.png")
Image.fromarray(gold).save(OUT / "_inv_goldmask.png")
print("saved")
