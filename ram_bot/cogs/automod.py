import re
from collections import deque
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

import discord
from discord.ext import commands

from ram_bot.constants import (
    BAD_WORDS,
    DEFAULT_AUTO_TIMEOUT_MINUTES,
    DEFAULT_DOMAIN_WHITELIST,
    DEFAULT_WARNING_THRESHOLD,
    REPEAT_MESSAGE_LIMIT,
    SPAM_MESSAGE_LIMIT,
    SPAM_WINDOW_SECONDS,
)
from ram_bot.timeparse import parse_duration


URL_PATTERN = re.compile(r"https?://[^\s]+", re.IGNORECASE)


class AutomodCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def settings(self, guild_id: int) -> dict:
        return self.bot.settings.get_guild(guild_id)

    def profile(self, guild_id: int, user_id: int) -> dict:
        return self.bot.user_profiles.get_profile(f"guild:{guild_id}", user_id)

    def whitelist(self, guild_id: int) -> set[str]:
        settings = self.settings(guild_id)
        domains = settings.get("domain_whitelist", list(DEFAULT_DOMAIN_WHITELIST))
        return {domain.lower() for domain in domains}

    async def add_warning(self, guild: discord.Guild, member: discord.Member, reason: str):
        profile = self.profile(guild.id, member.id)
        warnings = profile.setdefault("warnings", [])
        warnings.append(
            {
                "reason": reason,
                "at": datetime.now(timezone.utc).isoformat(),
            }
        )
        self.bot.user_profiles.save_profile(f"guild:{guild.id}", member.id, profile)

        threshold = self.settings(guild.id).get("warning_threshold", DEFAULT_WARNING_THRESHOLD)
        timeout_minutes = self.settings(guild.id).get("auto_timeout_minutes", DEFAULT_AUTO_TIMEOUT_MINUTES)
        if len(warnings) >= threshold:
            until = discord.utils.utcnow() + timedelta(minutes=timeout_minutes)
            try:
                await member.timeout(until, reason=f"Automatic timeout after {len(warnings)} warnings")
            except discord.Forbidden:
                return f"{member.mention} was warned. Ram could not apply the automatic timeout."
            return f"{member.mention} was warned and timed out for `{timeout_minutes}` minutes after reaching `{len(warnings)}` warnings."
        return f"{member.mention} was warned. Total warnings: `{len(warnings)}`."

    def message_cache(self, guild_id: int, user_id: int) -> dict:
        guild_cache = self.bot.automod_cache.setdefault(guild_id, {})
        return guild_cache.setdefault(
            user_id,
            {
                "times": deque(maxlen=10),
                "texts": deque(maxlen=REPEAT_MESSAGE_LIMIT),
            },
        )

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(moderate_members=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def warn(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        result = await self.add_warning(ctx.guild, member, reason)
        await ctx.send(result)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(moderate_members=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def warnings(self, ctx, member: discord.Member):
        profile = self.profile(ctx.guild.id, member.id)
        warnings = profile.get("warnings", [])
        if not warnings:
            await ctx.send(f"{member.mention} has no warnings.")
            return
        lines = [
            f"`#{index}` {entry['reason']} ({discord.utils.format_dt(datetime.fromisoformat(entry['at']), style='R')})"
            for index, entry in enumerate(warnings[-10:], start=max(1, len(warnings) - 9))
        ]
        embed = discord.Embed(title=f"Warnings - {member.display_name}", description="\n".join(lines), color=discord.Color.orange())
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(moderate_members=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def timeout(self, ctx, member: discord.Member, duration: str, *, reason: str = "No reason provided"):
        delta = parse_duration(duration)
        if delta is None:
            await ctx.send("Use a duration like `10m`, `1h`, or `1d`.")
            return
        until = discord.utils.utcnow() + delta
        await member.timeout(until, reason=reason)
        await ctx.send(f"{member.mention} was timed out until {discord.utils.format_dt(until, style='R')}.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def whitelistdomain(self, ctx, domain: str):
        domain = domain.lower().strip()
        settings = self.settings(ctx.guild.id)
        domains = set(settings.get("domain_whitelist", list(DEFAULT_DOMAIN_WHITELIST)))
        domains.add(domain)
        self.bot.settings.update_guild(ctx.guild.id, domain_whitelist=sorted(domains))
        await ctx.send(f"Added `{domain}` to the whitelist.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def unwhitelistdomain(self, ctx, domain: str):
        domain = domain.lower().strip()
        settings = self.settings(ctx.guild.id)
        domains = set(settings.get("domain_whitelist", list(DEFAULT_DOMAIN_WHITELIST)))
        domains.discard(domain)
        self.bot.settings.update_guild(ctx.guild.id, domain_whitelist=sorted(domains))
        await ctx.send(f"Removed `{domain}` from the whitelist.")

    @commands.command()
    @commands.guild_only()
    async def whitelistdomains(self, ctx):
        domains = sorted(self.whitelist(ctx.guild.id))
        await ctx.send("\n".join(f"`{domain}`" for domain in domains[:50]))

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def setwarningthreshold(self, ctx, count: int):
        self.bot.settings.update_guild(ctx.guild.id, warning_threshold=max(1, count))
        await ctx.send(f"Automatic punishment will trigger after `{max(1, count)}` warnings.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def setautotimeout(self, ctx, minutes: int):
        self.bot.settings.update_guild(ctx.guild.id, auto_timeout_minutes=max(1, minutes))
        await ctx.send(f"Automatic timeouts will last `{max(1, minutes)}` minutes.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is None or message.author.bot or not isinstance(message.author, discord.Member):
            return
        if message.author.guild_permissions.manage_messages:
            return

        cache = self.message_cache(message.guild.id, message.author.id)
        now = datetime.now(timezone.utc)
        cache["times"].append(now)
        cache["texts"].append(message.content.strip().lower())

        reason = None
        recent = [stamp for stamp in cache["times"] if (now - stamp).total_seconds() <= SPAM_WINDOW_SECONDS]
        if len(recent) >= SPAM_MESSAGE_LIMIT:
            reason = "Spam detected: too many rapid messages."
        elif len(cache["texts"]) >= REPEAT_MESSAGE_LIMIT and len(set(cache["texts"])) == 1 and cache["texts"][0]:
            reason = "Spam detected: repeated text."
        else:
            words = set(re.findall(r"\b[\w']+\b", message.content.lower()))
            if any(word in words for word in BAD_WORDS["severe"]):
                reason = "Bad word filter triggered: severe language."
            elif any(word in words for word in BAD_WORDS["mild"]):
                reason = "Bad word filter triggered: mild language."
            else:
                domains = []
                for found in URL_PATTERN.findall(message.content):
                    parsed = urlparse(found)
                    if parsed.hostname:
                        domains.append(parsed.hostname.lower().removeprefix("www."))
                whitelist = self.whitelist(message.guild.id)
                for domain in domains:
                    if not any(domain == allowed or domain.endswith(f".{allowed}") for allowed in whitelist):
                        reason = f"Link filter blocked domain `{domain}`."
                        break

        if reason is None:
            return

        try:
            await message.delete()
        except discord.Forbidden:
            pass

        result = await self.add_warning(message.guild, message.author, reason)
        await message.channel.send(result)


async def setup(bot):
    await bot.add_cog(AutomodCog(bot))
