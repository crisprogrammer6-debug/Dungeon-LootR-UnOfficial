from pathlib import Path
from PIL import Image

ROOT = Path(r"C:\Users\koke_\LootR web Unnoficial")
OUT = ROOT / "assets" / "img" / "materials"
W, H = 118, 112

skip = {p.name for p in OUT.glob("_*.png")}
changed = []
for path in sorted(OUT.glob("*.png")):
    if path.name in skip:
        continue
    im = Image.open(path).convert("RGBA")
    if im.size == (W, H):
        continue
    im.resize((W, H), Image.Resampling.LANCZOS).save(path)
    changed.append(f"{path.name} {im.size} -> ({W}, {H})")

print("resized", len(changed))
for line in changed:
    print(line)
