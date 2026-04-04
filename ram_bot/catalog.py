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
    summary="Cute reaction commands with anime GIFs and little Ram-style interactions.",
    commands=(
        CommandInfo("hug", "hug [@user]", "Have Ram send a soft anime hug to someone, or to you by default."),
        CommandInfo("airkiss", "airkiss [@user]", "Blow a cute kiss toward someone."),
        CommandInfo("kiss", "kiss [@user]", "Send a sweet anime kiss reaction."),
        CommandInfo("laugh", "laugh [@user]", "Laugh on your own, or laugh with someone."),
        CommandInfo("pat", "pat [@user]", "Give someone a cute head pat."),
        CommandInfo("cuddle", "cuddle [@user]", "Wrap someone up in a cozy cuddle."),
        CommandInfo("cheers", "cheers [@user]", "Share a playful toast with someone."),
        CommandInfo("clap", "clap [@user]", "Applaud someone dramatically."),
        CommandInfo("wave", "wave [@user]", "Send a friendly anime wave."),
        CommandInfo("blush", "blush [@user]", "Blush on your own, or blush at someone."),
        CommandInfo("handhold", "handhold [@user]", "Reach out and hold someone's hand."),
        CommandInfo("poke", "poke [@user]", "Poke someone for attention."),
        CommandInfo("nuzzle", "nuzzle [@user]", "Nuzzle up to someone in a cute way."),
        CommandInfo("tickle", "tickle [@user]", "Tickle someone into laughing."),
        CommandInfo("smile", "smile [@user]", "Smile softly, or smile at someone."),
        CommandInfo("shy", "shy [@user]", "Act unexpectedly shy around someone."),
        CommandInfo("glare", "glare [@user]", "Give someone a dramatic anime stare."),
        CommandInfo("lick", "lick [@user]", "Send a mischievous licking reaction."),
        CommandInfo("cry", "cry [@user]", "Cry on your own, or cry with someone."),
    ),
)

MODERATION_CATEGORY = CategoryInfo(
    name="Moderation",
    label="Moderation",
    summary="Server moderation, warnings, timeouts, and automod tools.",
    commands=(
        CommandInfo("kick", "kick @user [reason]", "Kick a member from the server."),
        CommandInfo("ban", "ban @user [reason]", "Ban a member from the server."),
        CommandInfo("unban", "unban name#1234", "Unban a previously banned user."),
        CommandInfo("purge", "purge <amount>", "Delete a number of recent messages."),
        CommandInfo("warn", "warn @user [reason]", "Warn a member and track it in Ram's records."),
        CommandInfo("warnings", "warnings @user", "Show a member's stored warnings."),
        CommandInfo("timeout", "timeout @user <time> [reason]", "Apply a Discord timeout to a member."),
    ),
)

SERVER_CATEGORY = CategoryInfo(
    name="Server",
    label="Server",
    summary="Welcome, goodbye, autorole, logs, and automod setup.",
    commands=(
        CommandInfo("setwelcome", "setwelcome #channel <message>", "Set the channel and message used when someone joins. Supports {user}, {username}, {server}, and {count}."),
        CommandInfo("clearwelcome", "clearwelcome", "Turn off welcome messages for the server."),
        CommandInfo("setgoodbye", "setgoodbye #channel <message>", "Set the channel and message used when someone leaves. Supports {user}, {username}, {server}, and {count}."),
        CommandInfo("cleargoodbye", "cleargoodbye", "Turn off goodbye messages for the server."),
        CommandInfo("setautorole", "setautorole @role", "Automatically give new members a role when they join."),
        CommandInfo("clearautorole", "clearautorole", "Disable automatic role assignment."),
        CommandInfo("setlogchannel", "setlogchannel #channel", "Send edited and deleted message logs to a specific channel."),
        CommandInfo("clearlogchannel", "clearlogchannel", "Turn off edited/deleted message logging."),
        CommandInfo("whitelistdomain", "whitelistdomain <domain>", "Allow a domain through the automod link filter."),
        CommandInfo("unwhitelistdomain", "unwhitelistdomain <domain>", "Remove a domain from the automod whitelist."),
        CommandInfo("whitelistdomains", "whitelistdomains", "Show the current domain whitelist."),
        CommandInfo("setwarningthreshold", "setwarningthreshold <count>", "Set how many warnings trigger an automatic timeout."),
        CommandInfo("setautotimeout", "setautotimeout <minutes>", "Set the timeout length used after too many warnings."),
        CommandInfo("serversettings", "serversettings", "Show the current welcome, goodbye, autorole, and log settings."),
    ),
)

PROGRESSION_CATEGORY = CategoryInfo(
    name="Progression",
    label="Progression",
    summary="XP, affinity, streaks, daily routines, and Ram's opinion of you.",
    commands=(
        CommandInfo("rank", "rank [@user]", "Show a user's XP, level, and affinity with Ram."),
        CommandInfo("affinity", "affinity [@user]", "See how warm or cold Ram currently feels toward someone."),
        CommandInfo("leaderboard", "leaderboard", "Show the top users by XP in this server."),
        CommandInfo("streak", "streak [@user]", "Show a user's current daily reward streak and next bonus milestone."),
        CommandInfo("daily", "daily", "Claim your main daily reward, build your streak, and earn milestone bonuses."),
        CommandInfo("checkin", "checkin", "Report in to Ram for a smaller repeatable XP and affinity boost."),
        CommandInfo("dailyhug", "dailyhug", "Receive one daily hug from Ram for a softer affection-focused bonus."),
        CommandInfo("setlevelrole", "setlevelrole <level> @role", "Give a role automatically at a specific level."),
        CommandInfo("clearlevelrole", "clearlevelrole <level>", "Remove a configured level reward role."),
    ),
)

UTILITY_CATEGORY = CategoryInfo(
    name="Utility",
    label="Utility",
    summary="Everyday information, reminders, and polls.",
    commands=(
        CommandInfo("avatar", "avatar [@user]", "Show someone's avatar."),
        CommandInfo("userinfo", "userinfo [@user]", "Show details about a user."),
        CommandInfo("serverinfo", "serverinfo", "Show details about the server."),
        CommandInfo("uptime", "uptime", "Show how long the bot has been running."),
        CommandInfo("remind", "remind <time> <message>", "Set a reminder in the current channel."),
        CommandInfo("poll", "poll <question | option 1 | option 2 ...>", "Create a quick reaction poll."),
    ),
)

MANAGEMENT_CATEGORY = CategoryInfo(
    name="Management",
    label="Management",
    summary="Owner-only bot controls and diagnostics.",
    commands=(
        CommandInfo("status", "status", "Show bot and hosting status."),
        CommandInfo("whoami", "whoami", "Show your Discord user ID."),
        CommandInfo("ollamatest", "ollamatest", "Test whether the bot container can reach the Ollama backend."),
        CommandInfo("restartbot", "restartbot", "Exit the bot so Docker can restart it."),
        CommandInfo("shutdownbot", "shutdownbot", "Stop the bot process."),
    ),
)


def get_categories(include_management: bool, include_admin_tools: bool = False) -> tuple[CategoryInfo, ...]:
    categories = [
        GENERAL_CATEGORY,
        ROLEPLAY_CATEGORY,
        PROGRESSION_CATEGORY,
        UTILITY_CATEGORY,
    ]
    if include_admin_tools:
        categories.extend([MODERATION_CATEGORY, SERVER_CATEGORY])
    if include_management:
        categories.append(MANAGEMENT_CATEGORY)
    return tuple(categories)


def find_command(query: str, include_management: bool, include_admin_tools: bool = False) -> CommandInfo | None:
    lowered = query.lower()
    for category in get_categories(include_management, include_admin_tools):
        for command in category.commands:
            if command.name == lowered:
                return command
    return None


def find_category(query: str, include_management: bool, include_admin_tools: bool = False) -> CategoryInfo | None:
    lowered = query.lower()
    for category in get_categories(include_management, include_admin_tools):
        if category.name.lower() == lowered:
            return category
    return None
