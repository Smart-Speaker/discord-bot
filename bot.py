import os

import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("BOT_PREFIX", "!")
OWNER_ID_RAW = os.getenv("OWNER_ID")
HUG_GIF_URL = "https://media.tenor.com/3ZZQ0H6V1n8AAAAC/anime-hug.gif"

if not TOKEN:
    raise ValueError("DISCORD_TOKEN is not set")

if not OWNER_ID_RAW:
    raise ValueError("OWNER_ID is not set")

try:
    OWNER_ID = int(OWNER_ID_RAW)
except ValueError:
    raise ValueError("OWNER_ID must be a valid Discord user ID number")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)


def is_owner(user_id):
    return user_id == OWNER_ID


def build_help_embed(ctx):
    embed = discord.Embed(
        title="Ram Bot Commands",
        description=f"My prefix is `{PREFIX}`",
        color=discord.Color.blurple(),
    )
    embed.add_field(
        name="Public Commands",
        value=(
            f"`{PREFIX}help` - Show this help menu\n"
            f"`{PREFIX}ping` - Check if the bot is online\n"
            f"`{PREFIX}hello` - Get a friendly greeting\n"
            f"`{PREFIX}hug @user` - Send a hug embed to someone"
        ),
        inline=False,
    )

    if is_owner(ctx.author.id):
        embed.add_field(
            name="Owner Commands",
            value=(
                f"`{PREFIX}status` - Show bot and container status\n"
                f"`{PREFIX}whoami` - Show your Discord user ID\n"
                f"`{PREFIX}restartbot` - Exit the bot so Docker can restart it\n"
                f"`{PREFIX}shutdownbot` - Stop the bot process"
            ),
            inline=False,
        )
        embed.set_footer(text="Owner commands are only shown to the configured OWNER_ID.")
    else:
        embed.set_footer(text="Some extra owner-only commands are hidden.")

    return embed


def owner_only():
    async def predicate(ctx):
        if ctx.author.id != OWNER_ID:
            await ctx.send("You are not allowed to use this command.")
            return False
        return True
    return commands.check(predicate)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} with prefix {PREFIX}")


@bot.command(name="help")
async def help_command(ctx):
    await ctx.send(embed=build_help_embed(ctx))


@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! `{round(bot.latency * 1000)}ms`")


@bot.command()
async def hello(ctx):
    await ctx.reply(f"Hi there! {ctx.author.display_name} :)", mention_author=False)


@bot.command()
async def hug(ctx, member: discord.Member = None):
    target = member or ctx.author
    embed = discord.Embed(
        title=f"{ctx.author.display_name} hugged {target.display_name}",
        description=f"{target.mention} you were hugged!",
        color=discord.Color.from_rgb(255, 182, 193),
        timestamp=ctx.message.created_at,
    )
    embed.set_image(url=HUG_GIF_URL)
    await ctx.send(embed=embed)


@bot.command()
@owner_only()
async def status(ctx):
    embed = discord.Embed(
        title="Owner Status Panel",
        color=discord.Color.green(),
    )
    embed.add_field(name="Prefix", value=f"`{PREFIX}`")
    embed.add_field(name="Latency", value=f"`{round(bot.latency * 1000)}ms`")
    embed.add_field(name="Guilds", value=str(len(bot.guilds)))
    embed.add_field(name="Owner ID", value=f"`{OWNER_ID}`", inline=False)
    embed.add_field(
        name="Bot Controls",
        value=(
            f"`{PREFIX}restartbot` will exit the process so Docker can restart it.\n"
            f"`{PREFIX}shutdownbot` will stop the bot process."
        ),
        inline=False,
    )
    await ctx.send(embed=embed)


@bot.command()
@owner_only()
async def whoami(ctx):
    await ctx.send(f"Your user ID is: {ctx.author.id}")


@bot.command()
@owner_only()
async def restartbot(ctx):
    await ctx.send("Restarting the bot process. Your Docker container needs a restart policy enabled for it to come back automatically.")
    raise SystemExit(0)


@bot.command()
@owner_only()
async def shutdownbot(ctx):
    await ctx.send("Shutting down the bot process now.")
    await bot.close()


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        return
    if isinstance(error, commands.CommandNotFound):
        return
    await ctx.send(f"Error: {error}")


bot.run(TOKEN)
