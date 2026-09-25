"""
Suggestions relay + Discord bot.

Website POSTs JSON to http://127.0.0.1:5182/suggest

If DISCORD_BOT_TOKEN + channel id are set (tools/suggestions-bot.env),
the bot posts the embed, filters insults via OpenAI Moderation, and
handles /suggestions wipe and /suggestions summary.

If only the webhook file is set, posts through the webhook (no commands, no filter).

Run:  python tools/suggestions-bot.py
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from aiohttp import ClientError, ClientSession, ClientTimeout, web

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
ENV_FILE = HERE / "suggestions-bot.env"
WEBHOOK_FILE = HERE / "suggestions-webhook.txt"
INBOX = ROOT / "data" / "suggestions-inbox.jsonl"
HOST = "127.0.0.1"
PORT = 5182
EMBED_TITLE = "Suggestion"
EMBED_COLOR = 13936122
MAX_HISTORY = 500


def load_env() -> None:
    if not ENV_FILE.exists():
        return
    for raw in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


def env(name: str) -> str:
    return (os.environ.get(name) or "").strip()


def webhook_url() -> str:
    if env("DISCORD_WEBHOOK_URL"):
        return env("DISCORD_WEBHOOK_URL")
    if WEBHOOK_FILE.exists():
        return WEBHOOK_FILE.read_text(encoding="utf-8").splitlines()[0].strip()
    return ""


def int_env(name: str) -> int:
    raw = env(name)
    return int(raw) if raw.isdigit() else 0


def append_inbox(payload: dict) -> None:
    INBOX.parent.mkdir(parents=True, exist_ok=True)
    with INBOX.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")


def suggestion_embed(payload: dict) -> dict:
    who = payload.get("discord") or "—"
    text = payload.get("body") or ""
    when = payload.get("sentAt") or datetime.now(timezone.utc).isoformat()
    return {
        "title": EMBED_TITLE,
        "description": text[:4000],
        "color": EMBED_COLOR,
        "fields": [
            {"name": "Discord", "value": str(who)[:256], "inline": True},
            {"name": "Sent", "value": str(when)[:64], "inline": True},
        ],
    }


def is_suggestion_message(message) -> bool:
    if not message.embeds:
        return False
    title = message.embeds[0].title or ""
    return title.strip().lower() == EMBED_TITLE.lower()


OPENAI_MODEL = "gpt-5.4-mini"


def openai_key() -> str:
    return env("OPENAI_API_KEY")


async def openai_chat(session: ClientSession, prompt: str, system: str) -> str:
    key = openai_key()
    if not key:
        raise RuntimeError("OPENAI_API_KEY missing")
    headers = {"Authorization": "Bearer %s" % key, "Content-Type": "application/json"}
    timeout = ClientTimeout(total=60)
    chat_payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "max_completion_tokens": 1024,
    }
    async with session.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=chat_payload,
        timeout=timeout,
    ) as res:
        data = await res.json()
        if res.status < 400:
            return (data["choices"][0]["message"].get("content") or "").strip()
        chat_err = "%s %s" % (res.status, data)
    resp_payload = {
        "model": OPENAI_MODEL,
        "input": system + "\n\n" + prompt,
        "max_output_tokens": 1024,
    }
    async with session.post(
        "https://api.openai.com/v1/responses",
        headers=headers,
        json=resp_payload,
        timeout=timeout,
    ) as res:
        data = await res.json()
        if res.status >= 400:
            raise RuntimeError("OpenAI %s (chat: %s)" % (data, chat_err))
    text = data.get("output_text") or ""
    if not text:
        for item in data.get("output") or []:
            for part in item.get("content") or []:
                if part.get("type") in ("output_text", "text"):
                    text += part.get("text") or ""
    if not text.strip():
        raise RuntimeError("Empty OpenAI response: %s" % data)
    return text.strip()


async def moderate_ok(session: ClientSession, text: str) -> bool:
    if not openai_key():
        return True
    prompt = (
        "Reject insults, hate, slurs, harassment, sexual content involving minors, "
        "and spam that is only abuse. Allow normal game feedback, even if blunt. "
        "Reply with JSON only: {\"ok\": true} or {\"ok\": false}.\n\n"
        "TEXT:\n" + text[:4000]
    )
    try:
        raw = await openai_chat(session, prompt, "You are a chat filter for a game wiki suggestion box.")
    except Exception as err:
        sys.stderr.write("Moderation failed: %s\n" % err)
        return True
    blob = raw.strip()
    if blob.startswith("```"):
        blob = blob.strip("`")
        blob = blob.replace("json", "", 1).strip()
    try:
        parsed = json.loads(blob)
        ok = bool(parsed.get("ok", True))
    except json.JSONDecodeError:
        low = blob.lower()
        ok = "false" not in low[:80]
    if not ok:
        sys.stderr.write("Dropped suggestion (%s filter)\n" % OPENAI_MODEL)
    return ok


async def summarize_texts(session: ClientSession, texts: list[str]) -> str:
    blob = "\n---\n".join(texts)[:12000]
    if not openai_key():
        lines = ["%s. %s" % (i + 1, t[:180].replace("\n", " ")) for i, t in enumerate(texts[:25])]
        extra = "" if len(texts) <= 25 else "\n…and %s more." % (len(texts) - 25)
        return "OpenAI key missing — raw list:\n" + "\n".join(lines) + extra
    prompt = (
        "Summarize these game-archive suggestions for staff. "
        "Group by theme, note duplicates, keep it short. "
        "Reply in the same language as most of the suggestions.\n\n" + blob
    )
    return await openai_chat(session, prompt, "You summarize user suggestions. No fluff.")


async def post_webhook(session: ClientSession, payload: dict) -> None:
    url = webhook_url()
    if not url:
        raise RuntimeError("No Discord bot token/channel and no webhook.")
    body = {"username": "LootR Archive", "embeds": [suggestion_embed(payload)]}
    async with session.post(
        url,
        json=body,
        headers={"User-Agent": "LootRArchive-Relay/1.0"},
        timeout=ClientTimeout(total=12),
    ) as res:
        if res.status >= 400:
            detail = await res.text()
            raise RuntimeError("Discord webhook %s: %s" % (res.status, detail[:200]))


def staff_ok(interaction) -> bool:
    user = interaction.user
    perms = getattr(user, "guild_permissions", None)
    if perms and (perms.manage_messages or perms.administrator):
        return True
    role_id = int_env("DISCORD_STAFF_ROLE_ID")
    roles = getattr(user, "roles", None) or []
    return bool(role_id and any(r.id == role_id for r in roles))


def build_discord():
    import discord
    from discord import app_commands

    intents = discord.Intents.default()
    intents.guilds = True
    intents.messages = True
    intents.message_content = True

    class SuggestBot(discord.Client):
        def __init__(self):
            super().__init__(intents=intents)
            self.tree = app_commands.CommandTree(self)
            self.http_session: ClientSession | None = None
            self.web_runner: web.AppRunner | None = None

        async def setup_hook(self):
            self.http_session = ClientSession()
            app = web.Application()
            app["bot"] = self
            app.router.add_post("/suggest", handle_suggest)
            app.router.add_route("OPTIONS", "/suggest", handle_options)
            self.web_runner = web.AppRunner(app)
            await self.web_runner.setup()
            await web.TCPSite(self.web_runner, HOST, PORT).start()
            print("Suggestion relay on http://%s:%s/suggest" % (HOST, PORT))
            guild_id = int_env("DISCORD_GUILD_ID")
            try:
                if guild_id:
                    guild = discord.Object(id=guild_id)
                    self.tree.copy_global_to(guild=guild)
                    await self.tree.sync(guild=guild)
                    print("Slash commands synced to guild %s" % guild_id)
                else:
                    await self.tree.sync()
                    print("Slash commands synced globally (can take up to 1 hour)")
            except discord.Forbidden:
                print("Could not sync slash commands (Missing Access). Invite the bot to that server with scope applications.commands.")
            except discord.HTTPException as err:
                print("Could not sync slash commands: %s" % err)

        async def on_ready(self):
            guilds = ", ".join("%s (%s)" % (g.name, g.id) for g in self.guilds) or "none"
            print("Logged in as %s — guilds: %s" % (self.user, guilds))

        async def on_guild_join(self, guild):
            want = int_env("DISCORD_GUILD_ID")
            if want and guild.id != want:
                return
            try:
                await self.tree.sync(guild=guild)
                print("Slash commands synced after join: %s" % guild.id)
            except discord.HTTPException as err:
                print("Sync after join failed: %s" % err)

        async def close(self):
            if self.http_session:
                await self.http_session.close()
            if self.web_runner:
                await self.web_runner.cleanup()
            await super().close()

        async def post_suggestion(self, payload: dict) -> None:
            channel_id = int_env("DISCORD_SUGGESTIONS_CHANNEL_ID")
            channel = self.get_channel(channel_id) if channel_id else None
            if channel is None and channel_id:
                channel = await self.fetch_channel(channel_id)
            if channel is None:
                await post_webhook(self.http_session, payload)
                return
            embed = discord.Embed.from_dict(suggestion_embed(payload))
            await channel.send(embed=embed)

    bot = SuggestBot()

    def require_staff():
        async def predicate(interaction: discord.Interaction):
            if staff_ok(interaction):
                return True
            raise app_commands.CheckFailure("Staff only (Manage Messages).")

        return app_commands.check(predicate)

    group = app_commands.Group(name="suggestions", description="Manage the suggestions channel")

    @group.command(name="wipe", description="Delete every suggestion in this channel")
    @require_staff()
    async def wipe_cmd(interaction: discord.Interaction):
        channel_id = int_env("DISCORD_SUGGESTIONS_CHANNEL_ID")
        if channel_id and interaction.channel_id != channel_id:
            await interaction.response.send_message("Run this in the suggestions channel.", ephemeral=True)
            return

        class Confirm(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=30)

            @discord.ui.button(label="Delete all", style=discord.ButtonStyle.danger)
            async def confirm(self, click: discord.Interaction, _button: discord.ui.Button):
                if click.user.id != interaction.user.id:
                    await click.response.send_message("Only the staff who ran the command can confirm.", ephemeral=True)
                    return
                await click.response.defer(ephemeral=True)
                removed = 0
                try:
                    deleted = await click.channel.purge(limit=MAX_HISTORY, check=is_suggestion_message)
                    removed += len(deleted)
                except discord.Forbidden:
                    await click.followup.send("Missing Manage Messages.", ephemeral=True)
                    return
                leftovers = []
                async for msg in click.channel.history(limit=MAX_HISTORY):
                    if is_suggestion_message(msg):
                        leftovers.append(msg)
                for msg in leftovers:
                    try:
                        await msg.delete()
                        removed += 1
                    except discord.HTTPException:
                        pass
                await click.followup.send("Deleted %s suggestion(s)." % removed, ephemeral=True)
                self.stop()

            @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
            async def cancel(self, click: discord.Interaction, _button: discord.ui.Button):
                if click.user.id != interaction.user.id:
                    await click.response.send_message("Only the staff who ran the command can cancel.", ephemeral=True)
                    return
                await click.response.edit_message(content="Cancelled.", view=None)
                self.stop()

        await interaction.response.send_message(
            "This deletes suggestion posts in this channel (last %s messages scanned). Confirm?" % MAX_HISTORY,
            view=Confirm(),
            ephemeral=True,
        )

    @group.command(name="summary", description="Summarize suggestions in this channel")
    @require_staff()
    async def summary_cmd(interaction: discord.Interaction):
        channel_id = int_env("DISCORD_SUGGESTIONS_CHANNEL_ID")
        if channel_id and interaction.channel_id != channel_id:
            await interaction.response.send_message("Run this in the suggestions channel.", ephemeral=True)
            return
        await interaction.response.defer(thinking=True)
        texts = []
        async for msg in interaction.channel.history(limit=MAX_HISTORY):
            if not is_suggestion_message(msg):
                continue
            desc = msg.embeds[0].description or ""
            if desc.strip():
                texts.append(desc.strip())
        if not texts:
            await interaction.followup.send("No suggestions in the recent channel history.")
            return
        session = interaction.client.http_session
        try:
            summary = await summarize_texts(session, texts)
        except Exception as err:
            await interaction.followup.send("Could not summarize: %s" % err)
            return
        header = "**%s suggestion(s)** (last %s messages scanned)\n\n" % (len(texts), MAX_HISTORY)
        body = (header + summary)[:3900]
        await interaction.followup.send(body)

    @bot.tree.error
    async def on_app_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        msg = "Staff only." if isinstance(error, app_commands.CheckFailure) else "Command failed."
        if interaction.response.is_done():
            await interaction.followup.send(msg, ephemeral=True)
        else:
            await interaction.response.send_message(msg, ephemeral=True)

    bot.tree.add_command(group)
    return bot


async def handle_options(_request: web.Request) -> web.Response:
    return web.Response(status=204, headers=_cors())


def _cors() -> dict:
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
    }


async def handle_suggest(request: web.Request) -> web.Response:
    bot = request.app["bot"]
    if int(request.headers.get("Content-Length") or "0") > 8000:
        return web.json_response({"error": "Bad payload size."}, status=400, headers=_cors())
    try:
        payload = await request.json()
    except (json.JSONDecodeError, UnicodeDecodeError):
        return web.json_response({"error": "Expected JSON."}, status=400, headers=_cors())
    if payload.get("type") != "suggestion":
        return web.json_response({"error": "Expected type suggestion."}, status=400, headers=_cors())
    body = str(payload.get("body") or "").strip()
    if len(body) < 4:
        return web.json_response({"error": "Suggestion is too short."}, status=400, headers=_cors())
    clean = {
        "type": "suggestion",
        "body": body[:1000],
        "discord": str(payload.get("discord") or "").strip()[:80],
        "sentAt": str(payload.get("sentAt") or datetime.now(timezone.utc).isoformat())[:64],
    }
    session = bot.http_session
    if not await moderate_ok(session, clean["body"] + "\n" + clean["discord"]):
        return web.json_response({"ok": True}, headers=_cors())
    try:
        if env("DISCORD_BOT_TOKEN") and bot.is_ready():
            await bot.post_suggestion(clean)
        else:
            await post_webhook(session, clean)
        append_inbox(clean)
    except Exception as err:
        sys.stderr.write("Post failed: %s\n" % err)
        return web.json_response({"error": "Could not post."}, status=502, headers=_cors())
    return web.json_response({"ok": True}, headers=_cors())


async def webhook_only() -> None:
    session = ClientSession()
    app = web.Application()

    class Shim:
        http_session = session
        def is_ready(self):
            return False

        async def post_suggestion(self, payload):
            await post_webhook(session, payload)

    app["bot"] = Shim()
    app.router.add_post("/suggest", handle_suggest)
    app.router.add_route("OPTIONS", "/suggest", handle_options)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, HOST, PORT).start()
    print("Suggestion relay on http://%s:%s/suggest" % (HOST, PORT))
    print("Mode: webhook only (no slash commands, no AI until bot token + OpenAI key)")
    print("Webhook:", "set" if webhook_url() else "MISSING")
    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        await session.close()
        await runner.cleanup()


def main() -> None:
    load_env()
    token = env("DISCORD_BOT_TOKEN")
    if token:
        try:
            bot = build_discord()
        except ImportError:
            print("Install discord.py:  pip install discord.py")
            sys.exit(1)
        print("Mode: Discord bot")
        print("Channel:", int_env("DISCORD_SUGGESTIONS_CHANNEL_ID") or "MISSING")
        print("OpenAI:", "set (%s)" % OPENAI_MODEL if openai_key() else "MISSING — no filter / weak summary")
        bot.run(token)
        return
    if not webhook_url():
        print("Need tools/suggestions-bot.env (bot token + channel) or tools/suggestions-webhook.txt")
        sys.exit(1)
    asyncio.run(webhook_only())


if __name__ == "__main__":
    main()
