import discord
from discord.ext import commands

from ram_bot.constants import DEFAULT_AUTO_TIMEOUT_MINUTES, DEFAULT_DOMAIN_WHITELIST, DEFAULT_WARNING_THRESHOLD, GUILD_JOIN_GIF_URL
from ram_bot.embeds import brand_color

DEFAULT_WELCOME_TEMPLATE = "Welcome {user} to {server}!"
DEFAULT_GOODBYE_TEMPLATE = "Goodbye {username}."


class ServerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def find_join_channel(self, guild: discord.Guild) -> discord.abc.Messageable | None:
        if guild.system_channel and guild.system_channel.permissions_for(guild.me).send_messages:
            return guild.system_channel

        for channel in guild.text_channels:
            permissions = channel.permissions_for(guild.me)
            if permissions.send_messages and permissions.embed_links:
                return channel

        return None

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
    @commands.has_permissions(administrator=True)
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
    @commands.has_permissions(administrator=True)
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
    @commands.has_permissions(administrator=True)
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
    @commands.has_permissions(administrator=True)
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
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def setautorole(self, ctx, role: discord.Role):
        self.bot.settings.update_guild(ctx.guild.id, autorole_id=role.id)
        await ctx.send(f"Auto role set to {role.mention}.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def clearautorole(self, ctx):
        self.bot.settings.update_guild(ctx.guild.id, autorole_id=None)
        await ctx.send("Auto role has been disabled.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def setlogchannel(self, ctx, channel: discord.TextChannel):
        self.bot.settings.update_guild(ctx.guild.id, log_channel_id=channel.id)
        await ctx.send(f"Audit logs will be sent in {channel.mention}.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def clearlogchannel(self, ctx):
        self.bot.settings.update_guild(ctx.guild.id, log_channel_id=None)
        await ctx.send("Audit log channel cleared.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def serversettings(self, ctx):
        settings = self.get_settings(ctx.guild.id)
        embed = discord.Embed(
            title=f"{ctx.guild.name} Settings",
            color=brand_color(),
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
        embed.add_field(
            name="Warning Threshold",
            value=str(settings.get("warning_threshold", DEFAULT_WARNING_THRESHOLD)),
            inline=True,
        )
        embed.add_field(
            name="Auto Timeout",
            value=f"{settings.get('auto_timeout_minutes', DEFAULT_AUTO_TIMEOUT_MINUTES)} minutes",
            inline=True,
        )
        domains = settings.get("domain_whitelist", list(DEFAULT_DOMAIN_WHITELIST))
        embed.add_field(
            name="Whitelisted Domains",
            value=", ".join(f"`{domain}`" for domain in domains[:8]) + (" ..." if len(domains) > 8 else ""),
            inline=False,
        )
        level_roles = settings.get("level_roles", {})
        embed.add_field(
            name="Level Roles",
            value=(
                "\n".join(f"Level {level}: <@&{role_id}>" for level, role_id in sorted(level_roles.items(), key=lambda item: int(item[0])))
                if level_roles
                else "None configured"
            ),
            inline=False,
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

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        channel = self.find_join_channel(guild)
        updates: dict[str, int | str] = {}

        if channel is not None and isinstance(channel, discord.TextChannel):
            settings = self.get_settings(guild.id)
            if not settings.get("welcome_channel_id"):
                updates["welcome_channel_id"] = channel.id
            if not settings.get("welcome_message"):
                updates["welcome_message"] = DEFAULT_WELCOME_TEMPLATE
            if not settings.get("goodbye_channel_id"):
                updates["goodbye_channel_id"] = channel.id
            if not settings.get("goodbye_message"):
                updates["goodbye_message"] = DEFAULT_GOODBYE_TEMPLATE

        if updates:
            self.bot.settings.update_guild(guild.id, **updates)

        if channel is None:
            return

        embed = discord.Embed(
            title="Ram has arrived",
            description=(
                "Hmph. Ram is here now.\n"
                "Use `!help` if you need the command list. Try not to waste Ram's time."
            ),
            color=brand_color(),
        )
        embed.set_image(url=GUILD_JOIN_GIF_URL)
        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ServerCog(bot))
