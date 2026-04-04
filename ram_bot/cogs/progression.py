import random
from datetime import datetime, timezone

import discord
from discord.ext import commands

from ram_bot.constants import (
    AFFINITY_REPLIES,
    CHECKIN_AFFINITY_REWARD,
    DAILY_AFFINITY_REWARD,
    DAILY_HUG_AFFINITY_REWARD,
    DAILY_XP_REWARD,
    XP_PER_MESSAGE_RANGE,
)


def scope_id(guild_id: int) -> str:
    return f"guild:{guild_id}"


def level_from_xp(xp: int) -> int:
    return xp // 100


def affinity_tier(affinity: int) -> str:
    if affinity >= 150:
        return "close"
    if affinity >= 75:
        return "warm"
    if affinity >= 25:
        return "neutral"
    return "cold"


class ProgressionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_profile(self, guild_id: int, user_id: int) -> dict:
        return self.bot.user_profiles.get_profile(scope_id(guild_id), user_id)

    async def maybe_apply_level_roles(self, member: discord.Member, level: int):
        settings = self.bot.settings.get_guild(member.guild.id)
        role_map = settings.get("level_roles", {})
        role_id = role_map.get(str(level))
        if not role_id:
            return
        role = member.guild.get_role(role_id)
        if role is None:
            return
        try:
            await member.add_roles(role, reason=f"Reached level {level}")
        except discord.Forbidden:
            return

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def rank(self, ctx, member: discord.Member | None = None):
        target = member or ctx.author
        profile = self.get_profile(ctx.guild.id, target.id)
        embed = discord.Embed(title=f"{target.display_name}'s Rank", color=discord.Color.blurple())
        embed.add_field(name="Level", value=str(profile["level"]), inline=True)
        embed.add_field(name="XP", value=str(profile["xp"]), inline=True)
        embed.add_field(name="Affinity", value=str(profile["affinity"]), inline=True)
        embed.add_field(name="Ram's View", value=random.choice(AFFINITY_REPLIES[affinity_tier(profile["affinity"])]), inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 6, commands.BucketType.guild)
    async def leaderboard(self, ctx):
        profiles = self.bot.user_profiles.all_profiles(scope_id(ctx.guild.id))
        ranked = sorted(profiles.items(), key=lambda item: item[1].get("xp", 0), reverse=True)[:10]
        if not ranked:
            await ctx.send("No one has earned any XP yet.")
            return
        lines = []
        for index, (user_id, profile) in enumerate(ranked, start=1):
            member = ctx.guild.get_member(int(user_id))
            name = member.display_name if member else f"User {user_id}"
            lines.append(f"`#{index}` {name} - Level {profile['level']} ({profile['xp']} XP)")
        embed = discord.Embed(title="Leaderboard", description="\n".join(lines), color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def daily(self, ctx):
        profile = self.get_profile(ctx.guild.id, ctx.author.id)
        today = datetime.now(timezone.utc).date().isoformat()
        if profile.get("last_daily") == today:
            await ctx.send("Ram already gave you your daily reward today.")
            return
        profile["last_daily"] = today
        profile["xp"] += DAILY_XP_REWARD
        profile["affinity"] += DAILY_AFFINITY_REWARD
        new_level = level_from_xp(profile["xp"])
        leveled = new_level > profile["level"]
        profile["level"] = new_level
        self.bot.user_profiles.save_profile(scope_id(ctx.guild.id), ctx.author.id, profile)
        if leveled:
            await self.maybe_apply_level_roles(ctx.author, new_level)
        await ctx.send(f"Daily claimed. `+{DAILY_XP_REWARD} XP` and `+{DAILY_AFFINITY_REWARD} affinity`.")

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def checkin(self, ctx):
        profile = self.get_profile(ctx.guild.id, ctx.author.id)
        profile["affinity"] += CHECKIN_AFFINITY_REWARD
        self.bot.user_profiles.save_profile(scope_id(ctx.guild.id), ctx.author.id, profile)
        await ctx.send(random.choice(AFFINITY_REPLIES[affinity_tier(profile["affinity"])]))

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def dailyhug(self, ctx):
        profile = self.get_profile(ctx.guild.id, ctx.author.id)
        profile["affinity"] += DAILY_HUG_AFFINITY_REWARD
        self.bot.user_profiles.save_profile(scope_id(ctx.guild.id), ctx.author.id, profile)
        await ctx.send(f"{ctx.author.mention} got a daily hug from Ram. Don't get used to it.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def setlevelrole(self, ctx, level: int, role: discord.Role):
        settings = self.bot.settings.get_guild(ctx.guild.id)
        role_map = settings.get("level_roles", {})
        role_map[str(level)] = role.id
        self.bot.settings.update_guild(ctx.guild.id, level_roles=role_map)
        await ctx.send(f"Members will receive {role.mention} at level `{level}`.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def clearlevelrole(self, ctx, level: int):
        settings = self.bot.settings.get_guild(ctx.guild.id)
        role_map = settings.get("level_roles", {})
        role_map.pop(str(level), None)
        self.bot.settings.update_guild(ctx.guild.id, level_roles=role_map)
        await ctx.send(f"Removed the role reward for level `{level}`.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is None or message.author.bot:
            return
        profile = self.get_profile(message.guild.id, message.author.id)
        now = datetime.now(timezone.utc)
        last_xp_at = profile.get("last_xp_at")
        if last_xp_at:
            previous = datetime.fromisoformat(last_xp_at)
            if (now - previous).total_seconds() < 60:
                return

        profile["last_xp_at"] = now.isoformat()
        profile["xp"] += random.randint(*XP_PER_MESSAGE_RANGE)
        new_level = level_from_xp(profile["xp"])
        leveled = new_level > profile["level"]
        profile["level"] = new_level
        self.bot.user_profiles.save_profile(scope_id(message.guild.id), message.author.id, profile)

        if leveled and isinstance(message.author, discord.Member):
            await self.maybe_apply_level_roles(message.author, new_level)
            await message.channel.send(f"{message.author.mention} reached level `{new_level}`.")


async def setup(bot):
    await bot.add_cog(ProgressionCog(bot))
