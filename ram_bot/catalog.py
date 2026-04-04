from dataclasses import dataclass


@dataclass(frozen=True)
class CommandInfo:
    name: str
    usage: str
    description: str


@dataclass(frozen=True)
class CategoryInfo:
    name: str
    label: str
    summary: str
    commands: tuple[CommandInfo, ...]


GENERAL_CATEGORY = CategoryInfo(
    name="General",
    label="Tools",
    summary="Core bot commands and help tools.",
    commands=(
        CommandInfo("help", "help [command/category]", "Show the help menu or details for a command."),
        CommandInfo("ping", "ping", "Check whether the bot is online."),
        CommandInfo("hello", "hello", "Get a friendly greeting from Ram."),
    ),
)

ROLEPLAY_CATEGORY = CategoryInfo(
    name="Roleplay",
    label="Roleplay",
    summary="Cute reaction commands with anime GIFs.",
    commands=(
        CommandInfo("hug", "hug [@user]", "Send a soft anime hug."),
        CommandInfo("kiss", "kiss [@user]", "Send a sweet anime kiss."),
        CommandInfo("laugh", "laugh", "Show a cheerful laughing reaction."),
        CommandInfo("pat", "pat [@user]", "Give someone a cute head pat."),
        CommandInfo("cuddle", "cuddle [@user]", "Wrap someone up in a cozy cuddle."),
        CommandInfo("wave", "wave [@user]", "Send a friendly anime wave."),
        CommandInfo("blush", "blush", "Show a shy blushing reaction."),
        CommandInfo("glare", "glare [@user]", "Give someone a dramatic anime stare."),
        CommandInfo("cry", "cry", "Show a sad crying reaction."),
    ),
)

MODERATION_CATEGORY = CategoryInfo(
    name="Moderation",
    label="Moderation",
    summary="Server moderation and cleanup tools.",
    commands=(
        CommandInfo("kick", "kick @user [reason]", "Kick a member from the server."),
        CommandInfo("ban", "ban @user [reason]", "Ban a member from the server."),
        CommandInfo("unban", "unban name#1234", "Unban a previously banned user."),
        CommandInfo("purge", "purge <amount>", "Delete a number of recent messages."),
    ),
)

SERVER_CATEGORY = CategoryInfo(
    name="Server",
    label="Server",
    summary="Welcome, goodbye, autorole, and message log setup.",
    commands=(
        CommandInfo("setwelcome", "setwelcome #channel <message>", "Configure a custom welcome message."),
        CommandInfo("clearwelcome", "clearwelcome", "Disable welcome messages."),
        CommandInfo("setgoodbye", "setgoodbye #channel <message>", "Configure a custom goodbye message."),
        CommandInfo("cleargoodbye", "cleargoodbye", "Disable goodbye messages."),
        CommandInfo("setautorole", "setautorole @role", "Automatically grant a role to new members."),
        CommandInfo("clearautorole", "clearautorole", "Disable the auto role feature."),
        CommandInfo("setlogchannel", "setlogchannel #channel", "Log edited and deleted messages."),
        CommandInfo("clearlogchannel", "clearlogchannel", "Disable edit/delete logging."),
        CommandInfo("serversettings", "serversettings", "Show the current server settings."),
    ),
)

MANAGEMENT_CATEGORY = CategoryInfo(
    name="Management",
    label="Management",
    summary="Owner-only bot controls and diagnostics.",
    commands=(
        CommandInfo("status", "status", "Show bot and hosting status."),
        CommandInfo("whoami", "whoami", "Show your Discord user ID."),
        CommandInfo("restartbot", "restartbot", "Exit the bot so Docker can restart it."),
        CommandInfo("shutdownbot", "shutdownbot", "Stop the bot process."),
    ),
)


def get_categories(include_management: bool) -> tuple[CategoryInfo, ...]:
    categories = [GENERAL_CATEGORY, ROLEPLAY_CATEGORY, MODERATION_CATEGORY, SERVER_CATEGORY]
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
