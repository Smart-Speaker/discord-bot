import discord

from ram_bot.catalog import CategoryInfo, CommandInfo, get_categories
from ram_bot.constants import EMBED_COLOR, HELP_GIF_URL


def brand_color() -> discord.Color:
    return discord.Color.from_rgb(*EMBED_COLOR)


def build_help_embed(prefix: str, include_management: bool) -> discord.Embed:
    embed = discord.Embed(
        title="Help Menu - Ram's Guide For Beginners",
        description="Here are all my commands hope this helps!",
        color=brand_color(),
    )
    embed.add_field(name="Prefix", value=f"`{prefix}`", inline=False)

    for category in get_categories(include_management):
        command_list = ", ".join(f"`{prefix}{command.name}`" for command in category.commands)
        embed.add_field(name=category.name, value=command_list, inline=True)

    if not include_management:
        embed.add_field(name="Management", value="Owner-only commands are hidden.", inline=True)

    embed.add_field(
        name="Using Commands",
        value=f"To view further information on how to use any command, use `{prefix}help <command>`.",
        inline=False,
    )
    embed.set_image(url=HELP_GIF_URL)
    embed.set_footer(text="Created by Nicholas Tjepkema")
    return embed


def build_command_help_embed(prefix: str, command: CommandInfo) -> discord.Embed:
    embed = discord.Embed(
        title=f"Command Help - {command.name}",
        color=brand_color(),
    )
    embed.add_field(name="Usage", value=f"`{prefix}{command.usage}`", inline=False)
    embed.add_field(name="Description", value=command.description, inline=False)
    return embed


def build_category_help_embed(prefix: str, category: CategoryInfo) -> discord.Embed:
    embed = discord.Embed(
        title=f"{category.name} Commands",
        color=brand_color(),
    )
    for command in category.commands:
        embed.add_field(
            name=f"{prefix}{command.name}",
            value=f"{command.description}\nUsage: `{prefix}{command.usage}`",
            inline=False,
        )
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
