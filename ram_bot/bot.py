import discord
from discord.ext import commands, tasks
from itertools import cycle
from datetime import datetime, timezone

from ram_bot.config import BotConfig
from ram_bot.constants import STATUS_MESSAGES
from ram_bot.storage import GuildSettingsStore, ReminderStore, UserProfileStore


class RamBot(commands.Bot):
    def __init__(self, config: BotConfig):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix=config.prefix,
            intents=intents,
            help_command=None,
        )
        self.config = config
        self.settings = GuildSettingsStore(config.data_dir)
        self.user_profiles = UserProfileStore(config.data_dir)
        self.reminders = ReminderStore(config.data_dir)
        self.started_at = datetime.now(timezone.utc)
        self.automod_cache = {}
        self.status_messages = cycle(STATUS_MESSAGES)
        self.initial_extensions = (
            "ram_bot.cogs.general",
            "ram_bot.cogs.roleplay",
            "ram_bot.cogs.moderation",
            "ram_bot.cogs.management",
            "ram_bot.cogs.server",
            "ram_bot.cogs.audit",
            "ram_bot.cogs.automod",
            "ram_bot.cogs.progression",
            "ram_bot.cogs.utility",
        )

    def is_owner(self, user_id: int) -> bool:
        return self.config.owner_id is not None and user_id == self.config.owner_id

    async def setup_hook(self):
        for extension in self.initial_extensions:
            await self.load_extension(extension)
        self.rotate_status.start()

    async def on_ready(self):
        print(f"Logged in as {self.user} with prefix {self.command_prefix}")

    @tasks.loop(minutes=15)
    async def rotate_status(self):
        await self.change_presence(
            activity=discord.CustomActivity(name=next(self.status_messages))
        )

    @rotate_status.before_loop
    async def before_rotate_status(self):
        await self.wait_until_ready()

    @staticmethod
    def format_cooldown(seconds: float) -> str:
        remaining = max(1, int(round(seconds)))
        days, remainder = divmod(remaining, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        parts: list[str] = []
        if days:
            parts.append(f"{days} day{'s' if days != 1 else ''}")
        if hours:
            parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
        if minutes:
            parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
        if seconds and not days:
            parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

        if len(parts) == 1:
            return parts[0]
        if len(parts) == 2:
            return f"{parts[0]} and {parts[1]}"
        return f"{', '.join(parts[:-1])}, and {parts[-1]}"

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            return
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.MissingPermissions):
            perms = ", ".join(error.missing_permissions).replace("_", " ")
            await ctx.send(f"You do not have permission to use that command. Missing: `{perms}`")
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing argument: `{error.param.name}`. Try `{self.command_prefix}help {ctx.command}` for usage.")
            return
        if isinstance(error, commands.BadArgument):
            await ctx.send("I could not understand that argument. Check the command and try again.")
            return
        if isinstance(error, commands.CommandOnCooldown):
            retry_after = self.format_cooldown(error.retry_after)
            await ctx.send(f"Hmph. You're being impatient again. Try `{ctx.command}` in `{retry_after}`.")
            return
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("That command can only be used in a server.")
            return
        if isinstance(error, discord.Forbidden):
            await ctx.send("I do not have enough Discord permissions to do that.")
            return
        await ctx.send(f"Error: {error}")
