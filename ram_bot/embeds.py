import discord

from ram_bot.catalog import CategoryInfo, CommandInfo, get_categories
from ram_bot.constants import EMBED_COLOR, HELP_GIF_URL

SPACER = "\u200b"


def brand_color() -> discord.Color:
    return discord.Color.from_rgb(*EMBED_COLOR)


def format_command_rows(commands: tuple[CommandInfo, ...], per_row: int = 3, limit: int | None = None) -> str:
    entries = [f"`{command.name}`" for command in commands[:limit]]
    rows = [
        " | ".join(entries[index:index + per_row])
        for index in range(0, len(entries), per_row)
    ]
    return "\n".join(f"- {row}" for row in rows)


def build_help_embed(prefix: str, include_management: bool, include_admin_tools: bool = False, in_guild: bool = True) -> discord.Embed:
    categories = list(get_categories(include_management, include_admin_tools, in_guild))

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
        command_list = format_command_rows(category.commands, per_row=3)
        embed.add_field(
            name=category.label,
            value=f"{category.summary}\n\n**Commands**\n{command_list}",
            inline=True,
        )
        if index % 2 == 0:
            embed.add_field(name=SPACER, value=SPACER, inline=False)

    if len(categories) % 2 != 0:
        embed.add_field(name=SPACER, value=SPACER, inline=False)

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


def build_help_pages(prefix: str, include_management: bool, include_admin_tools: bool = False, in_guild: bool = True) -> list[discord.Embed]:
    categories = list(get_categories(include_management, include_admin_tools, in_guild))
    overview = discord.Embed(
        title="Help Menu - Ram's Guide For Beginners",
        description=(
            "Browse the categories below.\n"
            f"Use `{prefix}help <command>` for direct help."
        ),
        color=brand_color(),
    )
    overview.add_field(name="Prefix", value=f"`{prefix}`", inline=False)
    for category in categories:
        command_list = format_command_rows(category.commands, per_row=3)
        overview.add_field(
            name=category.label,
            value=f"{category.summary}\n\n**Commands**\n{command_list}",
            inline=False,
        )
    overview.set_image(url=HELP_GIF_URL)
    overview.set_footer(text="Created by Nicholas Tjepkema")
    return [overview]


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
    if category.name == "Server":
        embed.add_field(
            name="Examples",
            value=(
                f"`{prefix}setwelcome #general Welcome {{user}} to {{server}}!`\n"
                f"`{prefix}setgoodbye #general Goodbye {{username}}.`\n"
                f"`{prefix}setautorole @Members`\n"
                f"`{prefix}setlogchannel #logs`"
            ),
            inline=False,
        )
    embed.set_footer(text=f"Use {prefix}help <command> for individual command help.")
    return embed


def build_category_help_pages(prefix: str, category: CategoryInfo, page_size: int = 6) -> list[discord.Embed]:
    chunks = [
        category.commands[index:index + page_size]
        for index in range(0, len(category.commands), page_size)
    ]
    pages: list[discord.Embed] = []
    total_pages = max(1, len(chunks))

    for page_number, chunk in enumerate(chunks, start=1):
        embed = discord.Embed(
            title=f"{category.label} Commands",
            description=category.summary,
            color=brand_color(),
        )
        for command in chunk:
            embed.add_field(
                name=f"{prefix}{command.name}",
                value=f"{command.description}\nUsage: `{prefix}{command.usage}`",
                inline=False,
            )
        if category.name == "Server" and page_number == total_pages:
            embed.add_field(
                name="Examples",
                value=(
                    f"`{prefix}setwelcome #general Welcome {{user}} to {{server}}!`\n"
                    f"`{prefix}setgoodbye #general Goodbye {{username}}.`\n"
                    f"`{prefix}setautorole @Members`\n"
                    f"`{prefix}setlogchannel #logs`"
                ),
                inline=False,
            )
        embed.set_footer(text=f"Page {page_number}/{total_pages} - Use {prefix}help <command> for individual command help.")
        pages.append(embed)

    return pages


def build_action_embed(ctx, title: str, description: str, gif_url: str) -> discord.Embed:
    embed = discord.Embed(
        title=title,
        description=description,
        color=brand_color(),
        timestamp=ctx.message.created_at,
    )
    embed.set_image(url=gif_url)
    return embed
