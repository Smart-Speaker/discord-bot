import random
from datetime import datetime, timedelta, timezone

import discord
from discord.ext import commands

from ram_bot.constants import (
    AFFINITY_REPLIES,
    CHECKIN_LINES,
    CHECKIN_XP_REWARD,
    CHECKIN_AFFINITY_REWARD,
    DAILY_HUG_LINES,
    DAILY_HUG_XP_REWARD,
    DAILY_AFFINITY_REWARD,
    DAILY_REWARD_LINES,
    DAILY_HUG_AFFINITY_REWARD,
    DAILY_XP_REWARD,
    FLAT_LEVEL_START,
    FLAT_LEVEL_XP,
    LEVEL_MILESTONES,
    STREAK_BONUS_XP,
    STREAK_MILESTONE,
    XP_PER_MESSAGE_RANGE,
)
from ram_bot.dialogue import relationship_label
from ram_bot.embeds import brand_color
from ram_bot.reactions import get_reaction_gif


def scope_id(guild_id: int) -> str:
    return f"guild:{guild_id}"


def xp_for_level(level: int) -> int:
    if level <= 0:
        return 0
    if level <= FLAT_LEVEL_START:
        return 100 * level + 25 * level * (level - 1)
    base_xp = 100 * FLAT_LEVEL_START + 25 * FLAT_LEVEL_START * (FLAT_LEVEL_START - 1)
    return base_xp + (level - FLAT_LEVEL_START) * FLAT_LEVEL_XP


def level_from_xp(xp: int) -> int:
    level = 0
    while xp >= xp_for_level(level + 1):
        level += 1
    return level


def affinity_tier(affinity: int) -> str:
    if affinity >= 300:
        return "very_close"
    if affinity >= 150:
        return "close"
    if affinity >= 75:
        return "warm"
    if affinity >= 25:
        return "neutral"
    return "cold"


def parse_iso_date(value: str | None):
    if not value:
        return None
    return datetime.fromisoformat(value).date()


def next_level_milestone(level: int) -> int | None:
    for milestone in LEVEL_MILESTONES:
        if milestone > level:
            return milestone
    return None


class ProgressionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_profile(self, guild_id: int, user_id: int) -> dict:
        return self.bot.user_profiles.get_profile(scope_id(guild_id), user_id)

    async def send_progress_embed(
        self,
        ctx,
        *,
        title: str,
        description: str | None = None,
        reaction: str | None = None,
    ):
        embed = discord.Embed(
            title=title,
            description=description,
            color=brand_color(),
        )
        if reaction:
            embed.set_image(url=await get_reaction_gif(reaction))
        await ctx.send(embed=embed)

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
        tier = affinity_tier(profile["affinity"])
        current_level = profile["level"]
        current_level_xp = xp_for_level(current_level)
        next_level_xp = xp_for_level(current_level + 1)
        progress_xp = profile["xp"] - current_level_xp
        needed_xp = next_level_xp - current_level_xp
        embed = discord.Embed(title=f"{target.display_name}'s Rank", color=brand_color())
        embed.add_field(name="Level", value=str(current_level), inline=True)
        embed.add_field(name="XP", value=str(profile["xp"]), inline=True)
        embed.add_field(name="Affinity", value=f"{profile['affinity']} ({tier.title()})", inline=True)
        embed.add_field(name="Relationship", value=relationship_label(profile["affinity"]), inline=True)
        embed.add_field(
            name="Progress",
            value=f"`{progress_xp}/{needed_xp} XP` to level `{current_level + 1}`",
            inline=True,
        )
        milestone = next_level_milestone(current_level)
        embed.add_field(
            name="Next Milestone",
            value=(f"Level `{milestone}`" if milestone is not None else "Highest milestone reached"),
            inline=False,
        )
        embed.add_field(name="Ram's View", value=random.choice(AFFINITY_REPLIES[affinity_tier(profile["affinity"])]), inline=False)
        embed.set_image(url=await get_reaction_gif("smile"))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def affinity(self, ctx, member: discord.Member | None = None):
        target = member or ctx.author
        profile = self.get_profile(ctx.guild.id, target.id)
        tier = affinity_tier(profile["affinity"])
        embed = discord.Embed(
            title=f"Ram's Affinity - {target.display_name}",
            description=random.choice(AFFINITY_REPLIES[tier]),
            color=brand_color(),
        )
        embed.add_field(name="Affinity", value=str(profile["affinity"]), inline=True)
        embed.add_field(name="Tier", value=tier.title(), inline=True)
        embed.add_field(name="Relationship", value=relationship_label(profile["affinity"]), inline=True)
        embed.set_image(url=await get_reaction_gif("blush" if tier in {"warm", "close"} else "smile"))
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
        embed = discord.Embed(title="Leaderboard", description="\n".join(lines), color=brand_color())
        embed.set_image(url=await get_reaction_gif("celebrate"))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def streak(self, ctx, member: discord.Member | None = None):
        target = member or ctx.author
        profile = self.get_profile(ctx.guild.id, target.id)
        streak = profile.get("daily_streak", 0)
        next_bonus = max(1, STREAK_MILESTONE - (streak % STREAK_MILESTONE or STREAK_MILESTONE))
        embed = discord.Embed(
            title=f"Daily Streak - {target.display_name}",
            description=(
                f"Current streak: `{streak}` day{'s' if streak != 1 else ''}.\n"
                f"Next Ram bonus in `{next_bonus}` day{'s' if next_bonus != 1 else ''}."
            ),
            color=brand_color(),
        )
        embed.set_image(url=await get_reaction_gif("thumbsup"))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def daily(self, ctx):
        profile = self.get_profile(ctx.guild.id, ctx.author.id)
        today = datetime.now(timezone.utc).date()
        if profile.get("last_daily") == today.isoformat():
            await ctx.send("Ram already gave you your daily reward today.")
            return

        previous_daily = parse_iso_date(profile.get("last_daily"))
        if previous_daily and previous_daily == today - timedelta(days=1):
            profile["daily_streak"] = profile.get("daily_streak", 0) + 1
        else:
            profile["daily_streak"] = 1

        profile["last_daily"] = today.isoformat()
        bonus_xp = STREAK_BONUS_XP if profile["daily_streak"] % STREAK_MILESTONE == 0 else 0
        profile["xp"] += DAILY_XP_REWARD + bonus_xp
        profile["affinity"] += DAILY_AFFINITY_REWARD
        new_level = level_from_xp(profile["xp"])
        leveled = new_level > profile["level"]
        profile["level"] = new_level
        self.bot.user_profiles.save_profile(scope_id(ctx.guild.id), ctx.author.id, profile)
        if leveled:
            await self.maybe_apply_level_roles(ctx.author, new_level)
        description = (
            f"{random.choice(DAILY_REWARD_LINES)}\n"
            f"{ctx.author.mention} received `+{DAILY_XP_REWARD + bonus_xp} XP` and `+{DAILY_AFFINITY_REWARD} affinity`.\n"
            f"Current streak: `{profile['daily_streak']}` day{'s' if profile['daily_streak'] != 1 else ''}."
        )
        if bonus_xp:
            description += f"\nStreak bonus: `+{bonus_xp} XP`."
        if leveled:
            description += f"\nYou also reached level `{new_level}`."
        await self.send_progress_embed(
            ctx,
            title="Daily Reward Claimed",
            description=description,
            reaction="yay",
        )
        await self.bot.set_temporary_presence("Distributing rewards with reluctance", seconds=14)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def checkin(self, ctx):
        profile = self.get_profile(ctx.guild.id, ctx.author.id)
        profile["last_checkin"] = datetime.now(timezone.utc).isoformat()
        profile["xp"] += CHECKIN_XP_REWARD
        profile["affinity"] += CHECKIN_AFFINITY_REWARD
        new_level = level_from_xp(profile["xp"])
        leveled = new_level > profile["level"]
        profile["level"] = new_level
        self.bot.user_profiles.save_profile(scope_id(ctx.guild.id), ctx.author.id, profile)
        if leveled:
            await self.maybe_apply_level_roles(ctx.author, new_level)
        await self.send_progress_embed(
            ctx,
            title="Check-in Complete",
            description=(
                f"{random.choice(CHECKIN_LINES)}\n"
                f"`+{CHECKIN_XP_REWARD} XP` and `+{CHECKIN_AFFINITY_REWARD} affinity`."
            ),
            reaction="thumbsup",
        )
        await self.bot.set_temporary_presence("Keeping track of who checked in", seconds=12)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def dailyhug(self, ctx):
        profile = self.get_profile(ctx.guild.id, ctx.author.id)
        profile["last_dailyhug"] = datetime.now(timezone.utc).isoformat()
        profile["xp"] += DAILY_HUG_XP_REWARD
        profile["affinity"] += DAILY_HUG_AFFINITY_REWARD
        new_level = level_from_xp(profile["xp"])
        leveled = new_level > profile["level"]
        profile["level"] = new_level
        self.bot.user_profiles.save_profile(scope_id(ctx.guild.id), ctx.author.id, profile)
        if leveled:
            await self.maybe_apply_level_roles(ctx.author, new_level)
        await self.send_progress_embed(
            ctx,
            title="Daily Hug",
            description=(
                f"{random.choice(DAILY_HUG_LINES)}\n"
                f"{ctx.author.mention} received `+{DAILY_HUG_XP_REWARD} XP` and `+{DAILY_HUG_AFFINITY_REWARD} affinity`."
            ),
            reaction="cuddle" if affinity_tier(profile["affinity"]) in {"warm", "close", "very_close"} else "hug",
        )
        await self.bot.set_temporary_presence("Giving out one daily hug", seconds=12)

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
            embed = discord.Embed(
                title="Level Up",
                description=f"{message.author.mention} reached level `{new_level}`.",
                color=brand_color(),
            )
            embed.set_image(url=await get_reaction_gif("celebrate"))
            await message.channel.send(embed=embed)
            await self.bot.set_temporary_presence(f"Watching someone reach level {new_level}", seconds=16)


async def setup(bot):
    await bot.add_cog(ProgressionCog(bot))
