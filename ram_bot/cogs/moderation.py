import discord
from discord.ext import commands


class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        if member == ctx.author:
            await ctx.send("You cannot kick yourself.")
            return
        if member == ctx.guild.me:
            await ctx.send("I cannot kick myself.")
            return

        await member.kick(reason=f"{ctx.author} | {reason}")
        await ctx.send(f"Kicked {member.mention}. Reason: {reason}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        if member == ctx.author:
            await ctx.send("You cannot ban yourself.")
            return
        if member == ctx.guild.me:
            await ctx.send("I cannot ban myself.")
            return

        await member.ban(reason=f"{ctx.author} | {reason}")
        await ctx.send(f"Banned {member.mention}. Reason: {reason}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, user: str = ""):
        if "#" not in user:
            await ctx.send("Use the format `name#1234` for the user you want to unban.")
            return

        name, discriminator = user.rsplit("#", 1)
        banned_users = [entry async for entry in ctx.guild.bans()]

        for entry in banned_users:
            banned_user = entry.user
            if banned_user.name == name and banned_user.discriminator == discriminator:
                await ctx.guild.unban(banned_user, reason=f"{ctx.author} | manual unban")
                await ctx.send(f"Unbanned `{banned_user}`.")
                return

        await ctx.send("I could not find that user in the ban list.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        if amount < 1:
            await ctx.send("Please choose a number greater than 0.")
            return

        deleted = await ctx.channel.purge(limit=amount + 1)
        confirmation = await ctx.send(f"Deleted {len(deleted) - 1} messages.")
        await confirmation.delete(delay=5)


async def setup(bot):
    await bot.add_cog(ModerationCog(bot))
