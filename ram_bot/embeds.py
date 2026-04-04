import discord

from ram_bot.catalog import CategoryInfo, CommandInfo, get_categories
from ram_bot.constants import EMBED_COLOR, HELP_GIF_URL


def brand_color() -> discord.Color:
    return discord.Color.from_rgb(*EMBED_COLOR)


def build_help_embed(prefix: str, include_management: bool) -> discord.Embed:
    embed = discord.Embed(
        title="Help Menu - Ram's Guide For Beginners",
        description=(
            "Here are all my commands. Pick a category below, or use "
            f"`{prefix}help <command>` for more detail."
        ),
        color=brand_color(),
    )
    embed.add_field(name="Prefix", value=f"`{prefix}`", inline=False)

    for category in get_categories(include_management):
        command_list = ", ".join(f"`{command.name}`" for command in category.commands)
        embed.add_field(
            name=f"{category.emoji} {category.name}",
            value=f"{category.summary}\n{command_list}",
            inline=False,
        )

    if not include_management:
        embed.add_field(
            name="⚙️ Management",
            value="Owner-only commands are hidden until OWNER_ID is configured.",
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
        title=f"{category.emoji} {category.name} Commands",
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
