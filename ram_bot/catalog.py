from dataclasses import dataclass


@dataclass(frozen=True)
class CommandInfo:
    name: str
    usage: str
    description: str
    guild_only: bool = False
    dm_only: bool = False
    nsfw_only: bool = False


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
        CommandInfo("setrelationship", "setrelationship <not_friends|freinds|partners|waifu|soulmate>", "Set Ram's DM-only relationship state for how she should respond to you there.", dm_only=True),
        CommandInfo("setmood", "setmood <neutral|sleepy|annoyed|happy|flirty|protective>", "Set Ram's DM-only mood so her replies stay in that tone.", dm_only=True),
        CommandInfo("dmstate", "dmstate", "Show Ram's current DM-only relationship and mood settings for you.", dm_only=True),
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
        CommandInfo("cry", "cry [@user]", "Cry on your own, or cry with someone."),
    ),
)

NSFW_CATEGORY = CategoryInfo(
    name="NSFW",
    label="NSFW",
    summary="Waifu.im image pulls that switch between SFW and NSFW based on channel context. Each tag below fetches that specific style.",
    commands=(
        CommandInfo("nsfw", "nsfw <tag[,tag2,...]>", "Fetch a Waifu.im image using one or more supported tags from this category.", nsfw_only=False),
        CommandInfo("nsfwcategories", "nsfwcategories", "Show the supported Waifu.im tags Ram can use.", nsfw_only=False),
        CommandInfo("waifu", "waifu", "Female anime or manga character art.", nsfw_only=False),
        CommandInfo("ero", "ero", "Erotic content with a stronger adult tone.", nsfw_only=False),
        CommandInfo("ecchi", "ecchi", "Softer sexual content with nudity but no visible genital detail.", nsfw_only=False),
        CommandInfo("oppai", "oppai", "Large-breasted women.", nsfw_only=False),
        CommandInfo("hentai", "hentai", "Explicit sexual content.", nsfw_only=False),
        CommandInfo("milf", "milf", "Sexually attractive older women.", nsfw_only=False),
        CommandInfo("uniform", "uniform", "Women wearing uniforms, cosplay, or similar outfits.", nsfw_only=False),
        CommandInfo("ass", "ass", "Women with an emphasized butt focus.", nsfw_only=False),
        CommandInfo("maid", "maid", "Cute women in maid outfits.", nsfw_only=False),
        CommandInfo("selfies", "selfies", "Photo-like selfie styled anime images.", nsfw_only=False),
        CommandInfo("paizuri", "paizuri", "Breast-focused explicit content.", nsfw_only=False),
        CommandInfo("oral", "oral", "Oral sex themed content.", nsfw_only=False),
        CommandInfo("lick", "lick [@user]", "Send a mischievous licking reaction.", nsfw_only=True),
        CommandInfo("bite", "bite [@user]", "Bite someone in a more heated playful way.", nsfw_only=True),
        CommandInfo("love", "love [@user]", "Show stronger affectionate interest in an NSFW channel.", nsfw_only=True),
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
        CommandInfo("rank", "rank [@user]", "Show a user's XP, level, and affinity with Ram.", guild_only=True),
        CommandInfo("affinity", "affinity [@user]", "See how warm or cold Ram currently feels toward someone.", guild_only=True),
        CommandInfo("leaderboard", "leaderboard", "Show the top users by XP in this server.", guild_only=True),
        CommandInfo("streak", "streak [@user]", "Show a user's current daily reward streak and next bonus milestone.", guild_only=True),
        CommandInfo("daily", "daily", "Claim your main daily reward, build your streak, and earn milestone bonuses.", guild_only=True),
        CommandInfo("checkin", "checkin", "Report in to Ram for a smaller repeatable XP and affinity boost.", guild_only=True),
        CommandInfo("dailyhug", "dailyhug", "Receive one daily hug from Ram for a softer affection-focused bonus.", guild_only=True),
        CommandInfo("setlevelrole", "setlevelrole <level> @role", "Give a role automatically at a specific level.", guild_only=True),
        CommandInfo("clearlevelrole", "clearlevelrole <level>", "Remove a configured level reward role.", guild_only=True),
    ),
)

UTILITY_CATEGORY = CategoryInfo(
    name="Utility",
    label="Utility",
    summary="Everyday information, reminders, and polls.",
    commands=(
        CommandInfo("avatar", "avatar [@user]", "Show someone's avatar."),
        CommandInfo("userinfo", "userinfo [@user]", "Show details about a user.", guild_only=True),
        CommandInfo("serverinfo", "serverinfo", "Show details about the server.", guild_only=True),
        CommandInfo("uptime", "uptime", "Show how long the bot has been running."),
        CommandInfo("remind", "remind <time> <message>", "Set a reminder that Ram will DM to you at the chosen time."),
        CommandInfo("poll", "poll <question | option 1 | option 2 ...>", "Create a quick reaction poll.", guild_only=True),
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


def visible_commands(commands: tuple[CommandInfo, ...], in_guild: bool, in_nsfw_context: bool) -> tuple[CommandInfo, ...]:
    return tuple(
        command
        for command in commands
        if (in_guild or not command.guild_only)
        and ((not in_guild) or not command.dm_only)
        and (in_nsfw_context or not command.nsfw_only)
    )


def get_categories(
    include_management: bool,
    include_admin_tools: bool = False,
    in_guild: bool = True,
    in_nsfw_context: bool = False,
) -> tuple[CategoryInfo, ...]:
    categories = [
        GENERAL_CATEGORY,
        ROLEPLAY_CATEGORY,
        PROGRESSION_CATEGORY,
        UTILITY_CATEGORY,
    ]
    if in_nsfw_context:
        categories.append(NSFW_CATEGORY)
    if include_admin_tools:
        categories.extend([MODERATION_CATEGORY, SERVER_CATEGORY])
    if include_management:
        categories.append(MANAGEMENT_CATEGORY)
    filtered_categories = []
    for category in categories:
        commands = visible_commands(category.commands, in_guild, in_nsfw_context)
        if commands:
            filtered_categories.append(
                CategoryInfo(
                    name=category.name,
                    label=category.label,
                    summary=category.summary,
                    commands=commands,
                )
            )
    return tuple(filtered_categories)

def find_command(
    query: str,
    include_management: bool,
    include_admin_tools: bool = False,
    in_guild: bool = True,
    in_nsfw_context: bool = False,
) -> CommandInfo | None:
    lowered = query.lower()
    for category in get_categories(include_management, include_admin_tools, in_guild, in_nsfw_context):
        for command in category.commands:
            if command.name == lowered:
                return command
    return None


def find_category(
    query: str,
    include_management: bool,
    include_admin_tools: bool = False,
    in_guild: bool = True,
    in_nsfw_context: bool = False,
) -> CategoryInfo | None:
    lowered = query.lower()
    for category in get_categories(include_management, include_admin_tools, in_guild, in_nsfw_context):
        if category.name.lower() == lowered:
            return category
    return None
