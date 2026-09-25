from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
files = [
    "guide.html",
    "extras.html",
    "gamemodes.html",
    "roster.html",
    "classes.html",
    "tierlist.html",
    "npcs.html",
    "events.html",
    "challenges.html",
    "raids-info.html",
    "index.html",
]
search_tag = (
    '    <script src="data/search-index.js?v=1"></script>\n'
    '    <script src="js/search.js?v=1"></script>'
)
for name in files:
    p = root / name
    t = p.read_text(encoding="utf-8")
    t = re.sub(r"css/app\.css\?v=\d+", "css/app.css?v=84", t)
    t = re.sub(r"data/site\.js\?v=\d+", "data/site.js?v=28", t)
    t = re.sub(r"js/site\.js\?v=\d+", "js/site.js?v=28", t)
    if "search-index.js" not in t:
        t = t.replace(
            '    <script src="js/site.js?v=28"></script>',
            '    <script src="js/site.js?v=28"></script>\n' + search_tag,
        )
    p.write_text(t, encoding="utf-8")
    print("updated", name)
