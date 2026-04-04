import discord
from discord.ext import commands

from ram_bot.checks import owner_only


class ManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @owner_only()
    async def status(self, ctx):
        embed = discord.Embed(
            title="Owner Status Panel",
            color=discord.Color.green(),
        )
        embed.add_field(name="Prefix", value=f"`{self.bot.command_prefix}`")
        embed.add_field(name="Latency", value=f"`{round(self.bot.latency * 1000)}ms`")
        embed.add_field(name="Guilds", value=str(len(self.bot.guilds)))
        owner_value = (
            f"`{self.bot.config.owner_id}`"
            if self.bot.config.owner_id is not None
            else "`Not configured`"
        )
        embed.add_field(name="Owner ID", value=owner_value, inline=False)
        embed.add_field(
            name="Bot Controls",
            value=(
                f"`{self.bot.command_prefix}restartbot` will exit the process so Docker can restart it.\n"
                f"`{self.bot.command_prefix}shutdownbot` will stop the bot process."
            ),
            inline=False,
        )
        await ctx.send(embed=embed)

    @commands.command()
    @owner_only()
    async def whoami(self, ctx):
        await ctx.send(f"Your user ID is: {ctx.author.id}")

    @commands.command()
    @owner_only()
    async def restartbot(self, ctx):
        await ctx.send("Restarting the bot process. Your Docker container needs a restart policy enabled for it to come back automatically.")
        raise SystemExit(0)

    @commands.command()
    @owner_only()
    async def shutdownbot(self, ctx):
        await ctx.send("Shutting down the bot process now.")
        await self.bot.close()


async def setup(bot):
    await bot.add_cog(ManagementCog(bot))
