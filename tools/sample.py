from pathlib import Path
from PIL import Image

SRC = Path(
    r"C:\Users\koke_\.cursor\projects\c-Users-koke-LootR-web-Unnoficial\assets\c__Users_koke__AppData_Roaming_Cursor_User_workspaceStorage_d804e58a312bcbacf7007f490e68ec7b_images_image-69c9df42-6124-4dc5-b933-211c28147de8.png"
)
im = Image.open(SRC).convert("RGBA")
px = im.load()
w, h = im.size
print("size", w, h)
pts = []
for y in (0, 1, 5, h//2, h-6, h-1):
    for x in (0, 1, 10, w//4, w//2, 3*w//4, w-11, w-1):
        r,g,b,a = px[x,y]
        lum = 0.299*r+0.587*g+0.114*b
        sat = max(r,g,b)-min(r,g,b)
        pts.append((x,y,(r,g,b),round(lum,1),sat))
for p in pts:
    print(p)
