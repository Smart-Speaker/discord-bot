import discord
from discord.ext import commands

from ram_bot.catalog import find_category, find_command
from ram_bot.embeds import (
    build_category_help_embed,
    build_command_help_embed,
    build_help_embed,
)


class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx, *, query: str | None = None):
        include_management = self.bot.is_owner(ctx.author.id)

        if not query:
            await ctx.send(
                embed=build_help_embed(
                    prefix=self.bot.command_prefix,
                    include_management=include_management,
                )
            )
            return

        command = find_command(query, include_management)
        if command is not None:
            await ctx.send(
                embed=build_command_help_embed(
                    prefix=self.bot.command_prefix,
                    command=command,
                )
            )
            return

        category = find_category(query, include_management)
        if category is not None:
            await ctx.send(
                embed=build_category_help_embed(
                    prefix=self.bot.command_prefix,
                    category=category,
                )
            )
            return

        await ctx.send("I could not find that command or category.")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! `{round(self.bot.latency * 1000)}ms`")

    @commands.command()
    async def hello(self, ctx):
        await ctx.reply(f"Hi there! {ctx.author.display_name} :)", mention_author=True)


async def setup(bot):
    await bot.add_cog(GeneralCog(bot))
