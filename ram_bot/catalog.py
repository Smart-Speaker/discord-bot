from dataclasses import dataclass


@dataclass(frozen=True)
class CommandInfo:
    name: str
    usage: str
    description: str


@dataclass(frozen=True)
class CategoryInfo:
    name: str
    commands: tuple[CommandInfo, ...]


GENERAL_CATEGORY = CategoryInfo(
    name="General",
    commands=(
        CommandInfo("help", "help [command/category]", "Show the help menu or details for a command."),
        CommandInfo("ping", "ping", "Check whether the bot is online."),
        CommandInfo("hello", "hello", "Get a friendly greeting from Ram."),
    ),
)

ROLEPLAY_CATEGORY = CategoryInfo(
    name="Roleplay",
    commands=(
        CommandInfo("hug", "hug [@user]", "Send a hug embed."),
        CommandInfo("kiss", "kiss [@user]", "Send a kiss embed."),
        CommandInfo("laugh", "laugh", "Show a laughing reaction."),
        CommandInfo("pat", "pat [@user]", "Give someone a head pat."),
        CommandInfo("glare", "glare [@user]", "Glare at someone dramatically."),
        CommandInfo("cry", "cry", "Show a crying reaction."),
    ),
)

MODERATION_CATEGORY = CategoryInfo(
    name="Moderation",
    commands=(
        CommandInfo("kick", "kick @user [reason]", "Kick a member from the server."),
        CommandInfo("ban", "ban @user [reason]", "Ban a member from the server."),
        CommandInfo("unban", "unban name#1234", "Unban a previously banned user."),
        CommandInfo("purge", "purge <amount>", "Delete a number of recent messages."),
    ),
)

MANAGEMENT_CATEGORY = CategoryInfo(
    name="Management",
    commands=(
        CommandInfo("status", "status", "Show bot and hosting status."),
        CommandInfo("whoami", "whoami", "Show your Discord user ID."),
        CommandInfo("restartbot", "restartbot", "Exit the bot so Docker can restart it."),
        CommandInfo("shutdownbot", "shutdownbot", "Stop the bot process."),
    ),
)


def get_categories(include_management: bool) -> tuple[CategoryInfo, ...]:
    categories = [GENERAL_CATEGORY, ROLEPLAY_CATEGORY, MODERATION_CATEGORY]
    if include_management:
        categories.append(MANAGEMENT_CATEGORY)
    return tuple(categories)


def find_command(query: str, include_management: bool) -> CommandInfo | None:
    lowered = query.lower()
    for category in get_categories(include_management):
        for command in category.commands:
            if command.name == lowered:
                return command
    return None


def find_category(query: str, include_management: bool) -> CategoryInfo | None:
    lowered = query.lower()
    for category in get_categories(include_management):
        if category.name.lower() == lowered:
            return category
    return None
