import discord
from discord.ext import commands

from ram_bot.catalog import find_category, find_command
from ram_bot.embeds import (
    build_category_help_embed,
    build_command_help_embed,
    build_help_pages,
)


class HelpPaginator(discord.ui.View):
    def __init__(self, author_id: int, pages: list[discord.Embed]):
        super().__init__(timeout=120)
        self.author_id = author_id
        self.pages = pages
        self.index = 0
        self.sync_buttons()

    def sync_buttons(self):
        self.previous_page.disabled = self.index == 0
        self.next_page.disabled = self.index >= len(self.pages) - 1

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Only the user who opened this help menu can use these buttons.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.secondary)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index -= 1
        self.sync_buttons()
        await interaction.response.edit_message(embed=self.pages[self.index], view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index += 1
        self.sync_buttons()
        await interaction.response.edit_message(embed=self.pages[self.index], view=self)


class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def help_command(self, ctx, *, query: str | None = None):
        include_management = self.bot.is_owner(ctx.author.id) and ctx.guild is None

        if not query:
            pages = build_help_pages(prefix=self.bot.command_prefix, include_management=include_management)
            await ctx.send(embed=pages[0], view=HelpPaginator(ctx.author.id, pages))
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
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ping(self, ctx):
        await ctx.send(f"Pong! `{round(self.bot.latency * 1000)}ms`")

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def hello(self, ctx):
        await ctx.reply(f"Hi there! {ctx.author.display_name} :grin:", mention_author=True)


async def setup(bot):
    await bot.add_cog(GeneralCog(bot))
