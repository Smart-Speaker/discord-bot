import discord
from discord.ext import commands


class ServerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_settings(self, guild_id: int) -> dict:
        return self.bot.settings.get_guild(guild_id)

    def format_message(self, template: str, member: discord.Member) -> str:
        return template.format(
            user=member.mention,
            username=member.display_name,
            server=member.guild.name,
            count=member.guild.member_count,
        )

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def setwelcome(self, ctx, channel: discord.TextChannel, *, message: str):
        self.bot.settings.update_guild(
            ctx.guild.id,
            welcome_channel_id=channel.id,
            welcome_message=message,
        )
        await ctx.send(f"Welcome messages will be sent in {channel.mention}.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def clearwelcome(self, ctx):
        self.bot.settings.update_guild(
            ctx.guild.id,
            welcome_channel_id=None,
            welcome_message=None,
        )
        await ctx.send("Welcome messages have been disabled.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def setgoodbye(self, ctx, channel: discord.TextChannel, *, message: str):
        self.bot.settings.update_guild(
            ctx.guild.id,
            goodbye_channel_id=channel.id,
            goodbye_message=message,
        )
        await ctx.send(f"Goodbye messages will be sent in {channel.mention}.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def cleargoodbye(self, ctx):
        self.bot.settings.update_guild(
            ctx.guild.id,
            goodbye_channel_id=None,
            goodbye_message=None,
        )
        await ctx.send("Goodbye messages have been disabled.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def setautorole(self, ctx, role: discord.Role):
        self.bot.settings.update_guild(ctx.guild.id, autorole_id=role.id)
        await ctx.send(f"Auto role set to {role.mention}.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def clearautorole(self, ctx):
        self.bot.settings.update_guild(ctx.guild.id, autorole_id=None)
        await ctx.send("Auto role has been disabled.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def setlogchannel(self, ctx, channel: discord.TextChannel):
        self.bot.settings.update_guild(ctx.guild.id, log_channel_id=channel.id)
        await ctx.send(f"Audit logs will be sent in {channel.mention}.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def clearlogchannel(self, ctx):
        self.bot.settings.update_guild(ctx.guild.id, log_channel_id=None)
        await ctx.send("Audit log channel cleared.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def serversettings(self, ctx):
        settings = self.get_settings(ctx.guild.id)
        embed = discord.Embed(
            title=f"{ctx.guild.name} Settings",
            color=discord.Color.blurple(),
        )
        embed.add_field(
            name="Welcome",
            value=(
                f"Channel: <#{settings['welcome_channel_id']}>\nMessage: {settings['welcome_message']}"
                if settings.get("welcome_channel_id") and settings.get("welcome_message")
                else "Disabled"
            ),
            inline=False,
        )
        embed.add_field(
            name="Goodbye",
            value=(
                f"Channel: <#{settings['goodbye_channel_id']}>\nMessage: {settings['goodbye_message']}"
                if settings.get("goodbye_channel_id") and settings.get("goodbye_message")
                else "Disabled"
            ),
            inline=False,
        )
        embed.add_field(
            name="Auto Role",
            value=f"<@&{settings['autorole_id']}>" if settings.get("autorole_id") else "Disabled",
            inline=True,
        )
        embed.add_field(
            name="Log Channel",
            value=f"<#{settings['log_channel_id']}>" if settings.get("log_channel_id") else "Disabled",
            inline=True,
        )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        settings = self.get_settings(member.guild.id)

        autorole_id = settings.get("autorole_id")
        if autorole_id is not None:
            role = member.guild.get_role(autorole_id)
            if role is not None:
                try:
                    await member.add_roles(role, reason="Auto role on join")
                except discord.Forbidden:
                    pass

        channel_id = settings.get("welcome_channel_id")
        template = settings.get("welcome_message")
        if channel_id and template:
            channel = member.guild.get_channel(channel_id)
            if channel is not None:
                await channel.send(self.format_message(template, member))

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        settings = self.get_settings(member.guild.id)
        channel_id = settings.get("goodbye_channel_id")
        template = settings.get("goodbye_message")
        if channel_id and template:
            channel = member.guild.get_channel(channel_id)
            if channel is not None:
                await channel.send(self.format_message(template, member))


async def setup(bot):
    await bot.add_cog(ServerCog(bot))
