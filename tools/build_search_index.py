"""Build data/search-index.js from catalog files."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def strip_html(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def rec(title, href, kind, keys=""):
    blob = " ".join(x for x in (title, kind, keys) if x)
    return {"title": title, "href": href, "kind": kind, "keys": blob.lower()}


records = []

# Pages / maps / extras
records += [
    rec("Home", "index.html", "Page", "lobby play now discord clickbytes"),
    rec("Beginner Guide", "guide.html", "Guide", "tutorial new player first hours beginner onboarding"),
    rec("Index", "roster.html", "Page", "catalog items consumables materials equipment"),
    rec("Classes", "classes.html", "Page", "kits roster class list"),
    rec("Tier List", "tierlist.html", "Page", "meta ranking competitive"),
    rec("Gamemodes", "gamemodes.html", "Page", "dungeons modes"),
    rec("Dungeons", "gamemodes.html", "Gamemode", "maps floors extract blessing"),
    rec("Challenges", "challenges.html", "Gamemode", "challenge dungeon floor 55"),
    rec("Boss Rush", "raids-info.html", "Gamemode", "raids raid stacked boss"),
    rec("NPC's", "npcs.html", "Page", "lobby npcs"),
    rec("Events", "events.html", "Page", "limited playlist"),
    rec("Extras", "extras.html", "Page", "systems"),
    rec("Stats", "extras.html", "Extras", "strength dexterity intelligence vitality recommended re-spec respec sp"),
    rec("Quests", "extras.html", "Extras", "daily weekly limited battlepass battle pass"),
    rec("Codes", "extras.html", "Extras", "redeem menu more codes"),
    rec("Suggestions", "suggestions.html", "Page", "suggestion ideas feedback"),
    rec("Bandit's Den", "guide.html", "Map", "bandit first dungeon"),
    rec("Goblin's Stronghold", "guide.html", "Map", "goblin stronghold"),
    rec("Forgotten Ruins", "guide.html", "Map", "knight ruins"),
    rec("The Catacombs", "guide.html", "Map", "catacombs"),
    rec("Frostspire Bastion", "guide.html", "Map", "frostspire awakened devil nightmare"),
    rec("Underworld Gate", "guide.html", "Map", "underworld scarlet knight nightmare"),
    rec("City of Mages", "guide.html", "Map", "mages city"),
]

classes_src = read("data/classes.js")
for m in re.finditer(
    r'\{\s*id:\s*"([^"]+)"\s*,\s*name:\s*"([^"]+)"\s*,\s*rarity:\s*"([^"]+)"\s*,\s*archetype:\s*"([^"]+)"\s*,\s*obtain:\s*"([^"]*)"',
    classes_src,
):
    cid, name, rarity, arch, obtain = m.groups()
    block = classes_src[m.start() : m.start() + 2500]
    skills = re.findall(r'name:\s*"([^"]+)"', block)
    keys = " ".join([rarity, arch, obtain] + skills[1:])
    records.append(rec(name, f"classes.html?id={cid}", "Class", keys))

index_src = read("data/index.js")
kind_label = {
    "items": "Item",
    "consumables": "Consumable",
    "equipments": "Equipment",
    "materials": "Material",
}
for tab, kind in kind_label.items():
    chunk_m = re.search(rf"{tab}:\s*\[(.*?)\]\s*,?\s*(?:equipments|consumables|items|materials|}})", index_src, re.S)
    if not chunk_m:
        continue
    for obj in re.finditer(r"\{[^{}]*\}", chunk_m.group(1)):
        block = obj.group(0)
        im = re.search(r'id:\s*"([^"]+)"', block)
        nm = re.search(r'name:\s*"([^"]+)"', block)
        if not im or not nm:
            continue
        extra = []
        for field in ("group", "rarity", "blurb"):
            fm = re.search(rf'{field}:\s*"([^"]*)"', block)
            if fm:
                extra.append(strip_html(fm.group(1)))
        records.append(rec(nm.group(1), f"roster.html?tab={tab}&id={im.group(1)}", kind, " ".join(extra)))

topics_src = read("data/topics.js")
for section, href_base in (("events", "events.html"), ("npcs", "npcs.html")):
    chunk_m = re.search(rf"\b{section}:\s*\[(.*?)\]\s*,?\s*(?:npcs:|\}})", topics_src, re.S)
    if not chunk_m:
        continue
    for obj in re.finditer(r'id:\s*"([^"]+)"\s*,\s*title:\s*"([^"]+)"', chunk_m.group(1)):
        kind = "Event" if section == "events" else "NPC"
        records.append(rec(obj.group(2), f"{href_base}#{obj.group(1)}", kind, obj.group(1).replace("-", " ")))

synonym_groups = [
    ["forgotten ruins", "knight", "knight ruins", "ruins"],
    ["goblin's stronghold", "goblin stronghold", "goblin", "goblins"],
    ["frostspire bastion", "frostspire", "frost"],
    ["underworld gate", "underworld"],
    ["the catacombs", "catacombs"],
    ["bandit's den", "bandit", "bandits den"],
    ["city of mages", "mages", "mage city"],
    ["rejuvenation tonic", "tonic", "heal", "healing potion", "hp potion"],
    ["luck potion", "luck pot", "loot luck"],
    ["normal spin", "spin", "summon", "summoning", "gacha"],
    ["lucky spin", "lucky"],
    ["awakened devil ex", "awakened devil", "ade"],
    ["scarlet knight", "scarlet"],
    ["devil heart", "devil hearts"],
    ["strength", "str"],
    ["dexterity", "dex"],
    ["intelligence", "int"],
    ["vitality", "vit"],
    ["beginner guide", "beginner", "tutorial", "new player"],
    ["boss rush", "raid", "raids"],
    ["challenges", "challenge dungeon", "challenge"],
    ["suggestions", "suggestion", "idea", "ideas", "feedback"],
    ["protection scroll", "prot scroll"],
    ["reforge stone", "reforge"],
    ["aspect gem", "aspect"],
    ["class xp essence", "class xp", "class exp"],
    ["unrestricted", "unrestricted fighter"],
    ["honored one", "honoured one"],
    ["anti magic", "antimagic"],
    ["cybernetic katana", "cybernatic katana"],
    ["payload", "aether marks"],
    ["magic unleashed", "mage coins"],
    ["mystery merchant", "star shop"],
    ["afk", "afk world", "afk chamber"],
]

# dedupe by href+title
seen = set()
out = []
for r in records:
    k = (r["href"], r["title"])
    if k in seen:
        continue
    seen.add(k)
    out.append(r)

text = (
    "/** Auto-generated search index. Re-run tools/build_search_index.py after catalog edits. */\n"
    "window.SEARCH_INDEX = "
    + json.dumps({"synonymGroups": synonym_groups, "records": out}, ensure_ascii=False, indent=2)
    + ";\n"
)
(ROOT / "data" / "search-index.js").write_text(text, encoding="utf-8")
print(f"wrote {len(out)} records")
