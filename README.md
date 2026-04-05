# Ram Discord Bot

Ram is a themed Discord bot inspired by **Ram from Re:Zero**. It combines moderation, server setup, progression, reminders, roleplay reactions, contextual dialogue, and optional local AI replies.

The bot is built with `discord.py`, runs cleanly in Docker, and is structured as a small package with cogs for each feature area.

## Features

- Custom help system with category and command detail pages
- Ram-style dialogue for `!hello`, bot mentions, and fallback chat
- Optional Ollama integration for local AI replies
- Roleplay commands with anime GIFs
- Waifu.im powered image commands with SFW/NSFW behavior based on context
- Moderation commands, warnings, timeouts, and automod
- Welcome, goodbye, autorole, and message logging
- XP, affinity, streaks, relationship tracking, and daily rewards
- Utility commands like avatars, uptime, reminders, and polls
- DM-only Ram mood and relationship controls
- Rotating Ram-themed status messages and short event-based presence changes

## Project Layout

```text
bot.py                  Entrypoint used by Docker
ram_bot/app.py          Bot factory and startup
ram_bot/bot.py          Core bot class and global error handling
ram_bot/config.py       Environment variable loading
ram_bot/catalog.py      Help menu/category metadata
ram_bot/dialogue.py     Ram dialogue logic, moods, affinity, DM state
ram_bot/storage.py      JSON-backed storage for guilds, users, reminders
ram_bot/waifu_api.py    Waifu.im image fetch helper
ram_bot/cogs/           Feature cogs
```

## Requirements

- Python `3.12`
- A Discord bot token
- Discord Developer Portal intents:
  - `Message Content Intent`
  - `Server Members Intent`

Optional:

- Ollama for local AI replies

## Environment Variables

These are the current supported environment variables.

### Required

- `DISCORD_TOKEN`
- `BOT_PREFIX`

### Optional

- `OWNER_ID`
- `AI_ENABLED`
- `OLLAMA_URL`
- `OLLAMA_MODEL`
- `BOT_DATA_DIR`
- `TZ`

### Example

```env
DISCORD_TOKEN=your_discord_bot_token
BOT_PREFIX=!
OWNER_ID=123456789012345678
AI_ENABLED=false
OLLAMA_URL=http://192.168.0.240:11434/api/generate
OLLAMA_MODEL=ram
BOT_DATA_DIR=/appdata
TZ=Europe/London
```

### Variable Notes

- `OWNER_ID` is optional. If left blank, owner-only commands are disabled.
- `AI_ENABLED=false` keeps Ram on the built-in dialogue system.
- `AI_ENABLED=true` enables Ollama-backed mention/chat replies.
- `BOT_DATA_DIR` stores reminders, guild settings, progression, and user profiles.

## Docker

The included `Dockerfile` bakes the bot code into the image and runs:

```dockerfile
CMD ["python", "/app/bot.py"]
```

Build locally:

```bash
docker build -t ram-bot .
```

Run locally:

```bash
docker run -d \
  --name ram-bot \
  -e DISCORD_TOKEN=your_token \
  -e BOT_PREFIX=! \
  -e TZ=Europe/London \
  -v /path/to/appdata:/appdata \
  ram-bot
```

## Unraid Notes

Recommended variables on Unraid:

- `DISCORD_TOKEN`
- `BOT_PREFIX`
- `OWNER_ID`
- `AI_ENABLED`
- `OLLAMA_URL`
- `OLLAMA_MODEL`
- `BOT_DATA_DIR`
- `TZ`

Example values:

- `BOT_PREFIX=!`
- `AI_ENABLED=false`
- `BOT_DATA_DIR=/appdata`
- `TZ=Europe/London`

## Bot Permissions

Recommended permissions:

- `View Channels`
- `Send Messages`
- `Embed Links`
- `Read Message History`
- `Add Reactions`
- `Manage Messages`
- `Manage Roles`
- `Kick Members`
- `Ban Members`
- `Moderate Members`

Useful optional permissions:

- `Attach Files`
- `Use External Emojis`
- `Create Polls`

Avoid giving the bot `Administrator` unless you intentionally want that.

## Main Systems

### 1. Dialogue

Ram has a contextual dialogue system used for:

- `!hello`
- mention replies like `@Ram hello`
- non-AI fallback chat

It can react based on:

- affinity
- relationship
- mood
- time of day
- recent actions
- return after absence
- spammy behavior

### 2. DM State

In DMs, Ram has manual state controls for the user:

- relationship
- mood

Default DM state:

- Relationship: `Freinds`
- Mood: `Neutral`

These DM-only commands let the user change that behavior:

- `!setrelationship <not_friends|freinds|partners|waifu|soulmate>`
- `!setmood <neutral|sleepy|annoyed|happy|flirty|protective>`
- `!dmstate`

### 3. AI Chat

If `AI_ENABLED=true`, Ram can send prompts to a local Ollama model.

Current behavior:

- mentioning the bot triggers Ram chat
- context includes user, channel, and NSFW status
- if Ollama is unavailable, Ram falls back to built-in replies

### 4. Roleplay

Roleplay commands send themed embeds with anime GIFs.

Examples:

- `!hug @user`
- `!kiss @user`
- `!cuddle @user`
- `!pat @user`
- `!wave`
- `!cry @user`

### 5. Image Commands

The bot uses [Waifu.im](https://api.waifu.im) for image commands.

It supports these tag commands:

- `!waifu`
- `!ero`
- `!ecchi`
- `!oppai`
- `!hentai`
- `!milf`
- `!uniform`
- `!ass`
- `!maid`
- `!selfies`
- `!paizuri`
- `!oral`

Also:

- `!nsfw <tag[,tag2,...]>`
- `!nsfwcategories`

Behavior:

- In DMs: requests are treated as NSFW-enabled
- In NSFW guild channels: requests are treated as NSFW-enabled
- In normal guild channels: requests fall back to SFW mode where possible

### 6. Moderation

Admin/guild-owner moderation features include:

- `!kick @user [reason]`
- `!ban @user [reason]`
- `!unban name#1234`
- `!purge <amount>`
- `!warn @user [reason]`
- `!warnings @user`
- `!timeout @user <time> [reason]`

Moderation help is hidden from users who are not:

- server admins
- server owners

### 7. Server Setup

Admin/guild-owner server commands:

- `!setwelcome #channel <message>`
- `!clearwelcome`
- `!setgoodbye #channel <message>`
- `!cleargoodbye`
- `!setautorole @role`
- `!clearautorole`
- `!setlogchannel #channel`
- `!clearlogchannel`
- `!whitelistdomain <domain>`
- `!unwhitelistdomain <domain>`
- `!whitelistdomains`
- `!setwarningthreshold <count>`
- `!setautotimeout <minutes>`
- `!serversettings`

Supported placeholders in welcome/goodbye messages:

- `{user}`
- `{username}`
- `{server}`
- `{count}`

### 8. Progression

Users gain XP from normal guild messages and certain interactions.

Progression includes:

- XP
- levels
- level milestones
- affinity
- relationship labels
- daily streaks
- daily/checkin/dailyhug routines
- level roles

Commands:

- `!rank [@user]`
- `!affinity [@user]`
- `!leaderboard`
- `!streak [@user]`
- `!daily`
- `!checkin`
- `!dailyhug`
- `!setlevelrole <level> @role`
- `!clearlevelrole <level>`

### 9. Utility

Commands:

- `!avatar [@user]`
- `!userinfo [@user]`
- `!serverinfo`
- `!uptime`
- `!remind <time> <message>`
- `!poll <question | option 1 | option 2 ...>`

Reminder behavior:

- reminders are delivered by DM when due

### 10. Management

Owner-only and DM-only:

- `!status`
- `!whoami`
- `!ollamatest`
- `!restartbot`
- `!shutdownbot`

These only work when `OWNER_ID` is configured.

## Help System

The help menu is custom and context-aware.

It hides commands when they should not be visible:

- guild-only commands are hidden in DMs
- moderation/server commands are hidden from non-admins
- management commands are only shown to the configured owner in DMs
- NSFW-only roleplay commands are only shown in DMs or NSFW channels

Examples:

```text
!help
!help roleplay
!help nsfw
!help hug
```

## Data Storage

The bot stores JSON files in `BOT_DATA_DIR`:

- guild settings
- user profiles
- reminders

This includes:

- welcome/goodbye config
- automod settings
- warnings
- XP and affinity
- DM relationship and mood state
- reminder queue

## Current Command Overview

### General

- `!help`
- `!ping`
- `!hello`
- `!ram <message>`
- mention the bot, for example `@Ram hello`
- `!setrelationship` (DM only)
- `!setmood` (DM only)
- `!dmstate` (DM only)

### Roleplay

- `!hug [@user]`
- `!airkiss [@user]`
- `!kiss [@user]`
- `!laugh [@user]`
- `!pat [@user]`
- `!cuddle [@user]`
- `!cheers [@user]`
- `!clap [@user]`
- `!wave [@user]`
- `!blush [@user]`
- `!handhold [@user]`
- `!poke [@user]`
- `!nuzzle [@user]`
- `!tickle [@user]`
- `!smile [@user]`
- `!shy [@user]`
- `!glare [@user]`
- `!cry [@user]`

NSFW roleplay:

- `!lick [@user]`
- `!bite [@user]`
- `!love [@user]`

### Image Tags

- `!waifu`
- `!ero`
- `!ecchi`
- `!oppai`
- `!hentai`
- `!milf`
- `!uniform`
- `!ass`
- `!maid`
- `!selfies`
- `!paizuri`
- `!oral`
- `!nsfw <tag[,tag2,...]>`
- `!nsfwcategories`

### Moderation

- `!kick @user [reason]`
- `!ban @user [reason]`
- `!unban name#1234`
- `!purge <amount>`
- `!warn @user [reason]`
- `!warnings @user`
- `!timeout @user <time> [reason]`

### Server

- `!setwelcome #channel <message>`
- `!clearwelcome`
- `!setgoodbye #channel <message>`
- `!cleargoodbye`
- `!setautorole @role`
- `!clearautorole`
- `!setlogchannel #channel`
- `!clearlogchannel`
- `!whitelistdomain <domain>`
- `!unwhitelistdomain <domain>`
- `!whitelistdomains`
- `!setwarningthreshold <count>`
- `!setautotimeout <minutes>`
- `!serversettings`

### Progression

- `!rank [@user]`
- `!affinity [@user]`
- `!leaderboard`
- `!streak [@user]`
- `!daily`
- `!checkin`
- `!dailyhug`
- `!setlevelrole <level> @role`
- `!clearlevelrole <level>`

### Utility

- `!avatar [@user]`
- `!userinfo [@user]`
- `!serverinfo`
- `!uptime`
- `!remind <time> <message>`
- `!poll <question | option 1 | option 2 ...>`

### Management

- `!status`
- `!whoami`
- `!ollamatest`
- `!restartbot`
- `!shutdownbot`

## Development

Install dependencies:

```bash
pip install -r requirements.txt
```

Run locally:

```bash
python bot.py
```

Syntax check:

```bash
python -m py_compile bot.py
python -m py_compile ram_bot\\*.py
```

## Notes

- The bot is designed for image-based Docker deployment.
- Owner features are optional.
- AI is optional.
- The help menu intentionally hides commands based on context and permissions.
- Ram's tone can change depending on affinity, recent behavior, DM state, and time of day.
