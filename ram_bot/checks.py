from discord.ext import commands


def owner_only():
    async def predicate(ctx):
        if ctx.guild is not None:
            await ctx.send("Management commands can only be used in my DMs.")
            return False
        if ctx.bot.config.owner_id is None:
            await ctx.send("Owner commands are disabled until OWNER_ID is configured.")
            return False
        if ctx.author.id != ctx.bot.config.owner_id:
            await ctx.send("You are not allowed to use this command.")
            return False
        return True

    return commands.check(predicate)
