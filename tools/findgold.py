from collections import deque
from pathlib import Path
from PIL import Image

SRC = Path(
    r"C:\Users\koke_\.cursor\projects\c-Users-koke-LootR-web-Unnoficial\assets\c__Users_koke__AppData_Roaming_Cursor_User_workspaceStorage_d804e58a312bcbacf7007f490e68ec7b_images_image-ec28a570-ef10-4570-b171-03cab5ccb3cc.png"
)
im = Image.open(SRC).convert("RGBA")
px = im.load()
w, h = im.size


def is_gold(r, g, b):
    if max(r, g, b) < 62:
        return False
    mid = (r + g) / 2.0
    return r >= 62 and g >= 48 and abs(r - g) < 42 and b < 0.88 * mid + 6


seen = [[False] * w for _ in range(h)]
for y in range(h):
    for x in range(w):
        if seen[y][x]:
            continue
        r, g, b, a = px[x, y]
        if not is_gold(r, g, b):
            seen[y][x] = True
            continue
        q = deque([(x, y)])
        seen[y][x] = True
        n = 0
        minx = maxx = x
        miny = maxy = y
        while q:
            cx, cy = q.popleft()
            n += 1
            minx, maxx = min(minx, cx), max(maxx, cx)
            miny, maxy = min(miny, cy), max(maxy, cy)
            for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx]:
                    nr, ng, nb, _ = px[nx, ny]
                    if is_gold(nr, ng, nb):
                        seen[ny][nx] = True
                        q.append((nx, ny))
                    else:
                        seen[ny][nx] = True
        bw, bh = maxx - minx + 1, maxy - miny + 1
        if 40 <= n <= 500 and 10 <= bw <= 50 and 10 <= bh <= 45 and minx > 80:
            print(f"n={n:3d} box=({minx},{miny},{maxx+1},{maxy+1}) {bw}x{bh}")
