import discord
import random
from discord.ext import commands

from ram_bot.constants import ROLEPLAY_GIFS
from ram_bot.embeds import build_action_embed


class RoleplayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_gif(self, action_name: str) -> str:
        return random.choice(ROLEPLAY_GIFS[action_name])

    async def send_target_action(self, ctx, member: discord.Member | None, action_name: str, description: str):
        target = member or ctx.author
        embed = build_action_embed(
            ctx,
            title=f"{ctx.author.display_name} used {action_name}",
            description=description.format(
                author=ctx.author.mention,
                author_name=ctx.author.display_name,
                target=target.mention,
                target_name=target.display_name,
            ),
            gif_url=self.get_gif(action_name),
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def hug(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "hug",
            "{target} you were hugged by {author_name}!",
        )

    @commands.command()
    async def kiss(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "kiss",
            "{target} you were kissed by {author_name}!",
        )

    @commands.command()
    async def laugh(self, ctx):
        embed = build_action_embed(
            ctx,
            title=f"{ctx.author.display_name} is laughing",
            description=f"{ctx.author.mention} is having a great time.",
            gif_url=self.get_gif("laugh"),
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def pat(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "pat",
            "{target} got a head pat from {author_name}.",
        )

    @commands.command()
    async def glare(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "glare",
            "{author_name} is glaring at {target_name}.",
        )

    @commands.command()
    async def cry(self, ctx):
        embed = build_action_embed(
            ctx,
            title=f"{ctx.author.display_name} is crying",
            description=f"{ctx.author.mention} needs a little comfort right now.",
            gif_url=self.get_gif("cry"),
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(RoleplayCog(bot))
