# Tools (not published)

Python helpers for crops, search index, and the Suggestions Discord bot. GitHub Pages does **not** deploy this folder.

## Suggestions bot (local)

1. Copy `suggestions-bot.env.example` to `suggestions-bot.env` and fill tokens.
2. From the repo root: `python -u tools/suggestions-bot.py`
3. The site on `127.0.0.1` posts to `http://127.0.0.1:5182/suggest`.

## Public site

The form always POSTs `{type,body,discord,sentAt}` to `window.SUGGESTIONS.endpoint` (`http://127.0.0.1:5182/suggest`). The bot still filters with OpenAI and posts to Discord. Never put Discord or OpenAI keys in HTML or JS.
