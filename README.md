# Dungeon LootR — companion site

Static HTML/CSS/JS. No build step. The public site is the files at the repo root; `tools/` stays off GitHub Pages.

This is a **fan companion**, not an official ClickBytes product.

## File layout

```
*.html                 Public pages (Home, Guide, Index, Classes, …)
css/app.css            All styles
js/                    Page scripts
data/                  Catalogs and copy (site.js, classes, index, topics, …)
assets/img/            Icons, maps, NPCs, home art
404.html               GitHub Pages fallback → Home
.nojekyll              Keep GitHub from running Jekyll
.github/workflows/     Publish to GitHub Pages
tools/                 Crops, search indexer, Suggestions bot — not published
calc.html              Private local calc — not published
```

Add a new page: HTML at root → link in `data/site.js` `nav` (do not add the calc). Bump `?v=` on CSS/JS you change so browsers pick it up.

## Local preview

```
python -m http.server 5181 --bind 127.0.0.1
```

Open `http://127.0.0.1:5181/`. Suggestions need `python -u tools/suggestions-bot.py` as well.

## Publish with GitHub Pages

1. Create a GitHub repo (public) and push this project to `main`.
2. Repo → **Settings → Pages**:
   - Source: **GitHub Actions** (not “Deploy from a branch”).
3. Push (or run the workflow **Deploy GitHub Pages** by hand).
4. The live URL is `https://<user>.github.io/<repo>/`.

If the repo is named `<user>.github.io`, the site is the user homepage (`https://<user>.github.io/`). Relative links (`classes.html`, `css/app.css`) already work in a project subfolder.

### Custom domain (later)

1. Buy a domain and point a CNAME (or A records) at GitHub Pages.
2. Add a `CNAME` file at the repo root with the hostname (one line).
3. Settings → Pages → Custom domain, then enable HTTPS.

### After it is live

- Suggestions stays as we built it: the form POSTs JSON to the bot (`POST /suggest`). Keep `tools/suggestions-bot.py` running.
- Never commit `tools/suggestions-bot.env` or webhook files.
- Keep `source` in `data/site.js` as the credit line in the footer.

## What the workflow publishes

Included: HTML (except `calc.html`), `css/`, `js/`, `data/*.js`, `assets/`, `.nojekyll`, `404.html`.

Excluded: `tools/`, Python scripts, `calc.html`, this README.
