import discord
from discord.ext import commands

from ram_bot.config import BotConfig


class RamBot(commands.Bot):
    def __init__(self, config: BotConfig):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(
            command_prefix=config.prefix,
            intents=intents,
            help_command=None,
        )
        self.config = config
        self.initial_extensions = (
            "ram_bot.cogs.general",
            "ram_bot.cogs.roleplay",
            "ram_bot.cogs.moderation",
            "ram_bot.cogs.management",
        )

    def is_owner(self, user_id: int) -> bool:
        return user_id == self.config.owner_id

    async def setup_hook(self):
        for extension in self.initial_extensions:
            await self.load_extension(extension)

    async def on_ready(self):
        print(f"Logged in as {self.user} with prefix {self.command_prefix}")

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            return
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use that command.")
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing argument. Try `{self.command_prefix}help` to see the command list.")
            return
        if isinstance(error, commands.BadArgument):
            await ctx.send("I could not understand that argument. Check the command and try again.")
            return
        if isinstance(error, discord.Forbidden):
            await ctx.send("I do not have enough Discord permissions to do that.")
            return
        await ctx.send(f"Error: {error}")
