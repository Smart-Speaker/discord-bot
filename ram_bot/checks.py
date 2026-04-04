from discord.ext import commands


def owner_only():
    async def predicate(ctx):
        if ctx.author.id != ctx.bot.config.owner_id:
            await ctx.send("You are not allowed to use this command.")
            return False
        return True

    return commands.check(predicate)
