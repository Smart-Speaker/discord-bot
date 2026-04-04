import discord
import random
from discord.ext import commands

from ram_bot.catalog import find_category, find_command
from ram_bot.constants import RAM_AI_UNAVAILABLE_REPLIES, RAM_FALLBACK_REPLIES
from ram_bot.embeds import (
    build_category_help_pages,
    build_command_help_embed,
    build_help_pages,
)
from ram_bot.ollama import build_ram_prompt, generate_ram_reply


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

    async def send_ram_reply(self, message: discord.Message, content: str):
        if self.bot.config.ai_enabled:
            try:
                prompt = build_ram_prompt(message, content)

                async with message.channel.typing():
                    reply = await generate_ram_reply(
                        self.bot.config.ollama_url,
                        self.bot.config.ollama_model,
                        prompt,
                    )
            except RuntimeError:
                reply = random.choice(RAM_AI_UNAVAILABLE_REPLIES)
        else:
            reply = random.choice(RAM_FALLBACK_REPLIES)

        await message.reply(reply[:2000], mention_author=True)

    @commands.command(name="help")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def help_command(self, ctx, *, query: str | None = None):
        include_management = self.bot.is_owner(ctx.author.id) and ctx.guild is None
        include_admin_tools = bool(ctx.guild and ctx.author.guild_permissions.administrator)

        if not query:
            pages = build_help_pages(
                prefix=self.bot.command_prefix,
                include_management=include_management,
                include_admin_tools=include_admin_tools,
            )
            if len(pages) == 1:
                await ctx.send(embed=pages[0])
            else:
                await ctx.send(embed=pages[0], view=HelpPaginator(ctx.author.id, pages))
            return

        command = find_command(query, include_management, include_admin_tools)
        if command is not None:
            await ctx.send(
                embed=build_command_help_embed(
                    prefix=self.bot.command_prefix,
                    command=command,
                )
            )
            return

        category = find_category(query, include_management, include_admin_tools)
        if category is not None:
            pages = build_category_help_pages(
                prefix=self.bot.command_prefix,
                category=category,
            )
            if len(pages) == 1:
                await ctx.send(embed=pages[0])
            else:
                await ctx.send(embed=pages[0], view=HelpPaginator(ctx.author.id, pages))
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

    @commands.command()
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def ram(self, ctx, *, message: str):
        await self.send_ram_reply(ctx.message, message)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or self.bot.user is None:
            return

        prefix = self.bot.command_prefix
        if isinstance(prefix, str) and message.content.startswith(prefix):
            return

        mention_forms = (
            f"<@{self.bot.user.id}>",
            f"<@!{self.bot.user.id}>",
        )

        content = message.content.strip()
        matched_mention = next((mention for mention in mention_forms if content.startswith(mention)), None)
        if matched_mention is None:
            return

        payload = content[len(matched_mention):].strip()
        if not payload:
            await message.reply("Hmph. If you're going to summon Ram, at least say something useful.", mention_author=True)
            return

        ctx = await self.bot.get_context(message)
        if ctx.valid:
            return

        await self.send_ram_reply(message, payload)


async def setup(bot):
    await bot.add_cog(GeneralCog(bot))
