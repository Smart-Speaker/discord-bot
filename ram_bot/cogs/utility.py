from datetime import datetime, timezone
from uuid import uuid4

import discord
from discord.ext import commands, tasks

from ram_bot.embeds import brand_color
from ram_bot.timeparse import parse_duration


POLL_REACTIONS = ("1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟")


class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminder_loop.start()

    def cog_unload(self):
        self.reminder_loop.cancel()

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def avatar(self, ctx, member: discord.Member | discord.User | None = None):
        target = member or ctx.author
        embed = discord.Embed(title=f"{target.display_name}'s Avatar", color=brand_color())
        embed.set_image(url=target.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def userinfo(self, ctx, member: discord.Member | None = None):
        target = member or ctx.author
        embed = discord.Embed(title=f"User Info - {target.display_name}", color=brand_color())
        embed.add_field(name="Mention", value=target.mention, inline=True)
        embed.add_field(name="ID", value=f"`{target.id}`", inline=True)
        embed.add_field(name="Joined", value=discord.utils.format_dt(target.joined_at, style="F") if target.joined_at else "Unknown", inline=False)
        embed.add_field(name="Created", value=discord.utils.format_dt(target.created_at, style="F"), inline=False)
        top_role = target.top_role.mention if target.top_role and target.top_role != ctx.guild.default_role else "None"
        embed.add_field(name="Top Role", value=top_role, inline=True)
        embed.add_field(name="Bot", value="Yes" if target.bot else "No", inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"Server Info - {guild.name}", color=brand_color())
        embed.add_field(name="Members", value=str(guild.member_count), inline=True)
        embed.add_field(name="Channels", value=str(len(guild.channels)), inline=True)
        embed.add_field(name="Roles", value=str(len(guild.roles)), inline=True)
        embed.add_field(name="Created", value=discord.utils.format_dt(guild.created_at, style="F"), inline=False)
        embed.add_field(name="Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=True)
        embed.add_field(name="Boost Tier", value=str(guild.premium_tier), inline=True)
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def uptime(self, ctx):
        delta = datetime.now(timezone.utc) - self.bot.started_at
        total = int(delta.total_seconds())
        days, remainder = divmod(total, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        parts = []
        if days:
            parts.append(f"{days}d")
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        parts.append(f"{seconds}s")
        await ctx.send(f"Ram has been running for `{' '.join(parts)}`.")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def remind(self, ctx, duration: str, *, message: str):
        delta = parse_duration(duration)
        if delta is None:
            await ctx.send("Use a time like `10m`, `2h`, or `1d12h`.")
            return

        due_at = datetime.now(timezone.utc) + delta
        reminder = {
            "id": str(uuid4()),
            "user_id": ctx.author.id,
            "channel_id": ctx.channel.id,
            "guild_id": ctx.guild.id if ctx.guild else None,
            "message": message,
            "due_at": due_at.isoformat(),
        }
        self.bot.reminders.add(reminder)
        await ctx.send(f"Ram will DM that reminder to you {discord.utils.format_dt(due_at, style='R')}.")

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def poll(self, ctx, *, content: str):
        parts = [part.strip() for part in content.split("|") if part.strip()]
        if len(parts) == 1:
            question = parts[0]
            options = ["Yes", "No"]
        elif 3 <= len(parts) <= 11:
            question = parts[0]
            options = parts[1:]
        else:
            await ctx.send("Use `question | option 1 | option 2` with up to 10 options.")
            return

        embed = discord.Embed(title="Poll", description=question, color=brand_color())
        lines = [f"{POLL_REACTIONS[index]} {option}" for index, option in enumerate(options)]
        embed.add_field(name="Options", value="\n".join(lines), inline=False)
        poll_message = await ctx.send(embed=embed)
        for index in range(len(options)):
            await poll_message.add_reaction(POLL_REACTIONS[index])

    @tasks.loop(seconds=30)
    async def reminder_loop(self):
        now = datetime.now(timezone.utc)
        due = []
        for reminder in self.bot.reminders.all():
            due_at = datetime.fromisoformat(reminder["due_at"])
            if due_at <= now:
                due.append(reminder)

        if not due:
            return

        remove_ids = set()
        for reminder in due:
            user = self.bot.get_user(reminder["user_id"])
            if user is None:
                try:
                    user = await self.bot.fetch_user(reminder["user_id"])
                except (discord.NotFound, discord.HTTPException):
                    remove_ids.add(reminder["id"])
                    continue
            embed = discord.Embed(
                title="Reminder",
                description=reminder["message"],
                color=brand_color(),
                timestamp=now,
            )
            if reminder.get("guild_id"):
                embed.add_field(name="From", value="A server reminder you asked Ram to keep.", inline=False)
            try:
                await user.send(embed=embed)
            except discord.Forbidden:
                remove_ids.add(reminder["id"])
                continue
            remove_ids.add(reminder["id"])

        self.bot.reminders.remove_ids(remove_ids)

    @reminder_loop.before_loop
    async def before_reminder_loop(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(UtilityCog(bot))
