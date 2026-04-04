import discord

from ram_bot.catalog import CategoryInfo, CommandInfo, get_categories
from ram_bot.constants import EMBED_COLOR, HELP_GIF_URL

SPACER = "\u200b"


def brand_color() -> discord.Color:
    return discord.Color.from_rgb(*EMBED_COLOR)


def build_help_embed(prefix: str, include_management: bool) -> discord.Embed:
    categories = list(get_categories(include_management))

    embed = discord.Embed(
        title="Help Menu - Ram's Guide For Beginners",
        description=(
            "Here are all my commands.\n"
            f"Use `{prefix}help <command>` for more detail."
        ),
        color=brand_color(),
    )
    embed.add_field(name="Prefix", value=f"`{prefix}`", inline=False)

    for index, category in enumerate(categories, start=1):
        command_list = ", ".join(f"`{command.name}`" for command in category.commands)
        embed.add_field(
            name=category.label,
            value=f"{category.summary}\n{command_list}",
            inline=True,
        )
        if index % 2 == 0:
            embed.add_field(name=SPACER, value=SPACER, inline=False)

    if len(categories) % 2 != 0:
        embed.add_field(
            name=SPACER,
            value=SPACER,
            inline=False,
        )

    embed.add_field(
        name="Examples",
        value=(
            f"`{prefix}help roleplay`\n"
            f"`{prefix}help hug`\n"
            f"`{prefix}hug @user`"
        ),
        inline=False,
    )
    embed.set_image(url=HELP_GIF_URL)
    embed.set_footer(text="Created by Nicholas Tjepkema")
    return embed


def build_help_pages(prefix: str, include_management: bool) -> list[discord.Embed]:
    categories = list(get_categories(include_management))
    pages: list[discord.Embed] = []

    overview = discord.Embed(
        title="Help Menu - Ram's Guide For Beginners",
        description=(
            "Browse the pages below for commands and setup options.\n"
            f"Use `{prefix}help <command>` for direct help."
        ),
        color=brand_color(),
    )
    overview.add_field(name="Prefix", value=f"`{prefix}`", inline=False)
    for index, category in enumerate(categories, start=1):
        command_list = ", ".join(f"`{command.name}`" for command in category.commands[:4])
        if len(category.commands) > 4:
            command_list += ", ..."
        overview.add_field(
            name=category.label,
            value=f"{category.summary}\n{command_list}",
            inline=True,
        )
        if index % 2 == 0:
            overview.add_field(name=SPACER, value=SPACER, inline=False)
    overview.set_image(url=HELP_GIF_URL)
    overview.set_footer(text="Page 1")
    pages.append(overview)

    for page_number, category in enumerate(categories, start=2):
        page = build_category_help_embed(prefix, category)
        page.set_footer(text=f"Page {page_number}")
        pages.append(page)

    return pages


def build_command_help_embed(prefix: str, command: CommandInfo) -> discord.Embed:
    embed = discord.Embed(
        title=f"Command Help - {command.name}",
        description=command.description,
        color=brand_color(),
    )
    embed.add_field(name="Usage", value=f"`{prefix}{command.usage}`", inline=False)
    embed.add_field(name="Category Tip", value=f"Use `{prefix}help` to open the full menu.", inline=False)
    return embed


def build_category_help_embed(prefix: str, category: CategoryInfo) -> discord.Embed:
    embed = discord.Embed(
        title=f"{category.label} Commands",
        description=category.summary,
        color=brand_color(),
    )
    for command in category.commands:
        embed.add_field(
            name=f"{prefix}{command.name}",
            value=f"{command.description}\nUsage: `{prefix}{command.usage}`",
            inline=False,
        )
    embed.set_footer(text=f"Use {prefix}help <command> for individual command help.")
    return embed


def build_action_embed(ctx, title: str, description: str, gif_url: str) -> discord.Embed:
    embed = discord.Embed(
        title=title,
        description=description,
        color=brand_color(),
        timestamp=ctx.message.created_at,
    )
    embed.set_image(url=gif_url)
    return embed
