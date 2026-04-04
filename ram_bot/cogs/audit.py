import discord
from discord.ext import commands

from ram_bot.embeds import brand_color


class AuditCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_log_channel(self, guild: discord.Guild):
        settings = self.bot.settings.get_guild(guild.id)
        channel_id = settings.get("log_channel_id")
        if channel_id is None:
            return None
        return guild.get_channel(channel_id)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.guild is None or message.author.bot:
            return

        channel = self.get_log_channel(message.guild)
        if channel is None:
            return

        embed = discord.Embed(
            title="Message Deleted",
            color=brand_color(),
            timestamp=discord.utils.utcnow(),
        )
        embed.add_field(name="Author", value=message.author.mention, inline=True)
        embed.add_field(name="Channel", value=message.channel.mention, inline=True)
        embed.add_field(name="Content", value=message.content or "*No text content*", inline=False)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.guild is None or before.author.bot or before.content == after.content:
            return

        channel = self.get_log_channel(before.guild)
        if channel is None:
            return

        embed = discord.Embed(
            title="Message Edited",
            color=brand_color(),
            timestamp=discord.utils.utcnow(),
        )
        embed.add_field(name="Author", value=before.author.mention, inline=True)
        embed.add_field(name="Channel", value=before.channel.mention, inline=True)
        embed.add_field(name="Before", value=before.content or "*No text content*", inline=False)
        embed.add_field(name="After", value=after.content or "*No text content*", inline=False)
        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(AuditCog(bot))
