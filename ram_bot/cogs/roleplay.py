import discord
from discord.ext import commands

from ram_bot.embeds import build_action_embed
from ram_bot.reactions import get_reaction_gif


class RoleplayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_target_action(
        self,
        ctx,
        member: discord.Member | None,
        action_name: str,
        targeted_title: str,
        self_title: str,
        targeted_description: str,
        self_description: str,
    ):
        target = member or ctx.author
        source_name = ctx.author.display_name if member is not None else ctx.me.display_name
        gif_url = await get_reaction_gif(action_name)
        embed = build_action_embed(
            ctx,
            title=(targeted_title if member is not None else self_title).format(
                author_name=ctx.author.display_name,
                source_name=source_name,
                target_name=target.display_name,
            ),
            description=(targeted_description if member is not None else self_description).format(
                author=ctx.author.mention,
                author_name=ctx.author.display_name,
                source_name=source_name,
                target=target.mention,
                target_name=target.display_name,
            ),
            gif_url=gif_url,
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def hug(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "hug",
            "{author_name} hugged {target_name}",
            "{source_name} hugged {target_name}",
            "{target} you were hugged by {author_name}!",
            "{target} you were hugged by {source_name}!",
        )

    @commands.command()
    async def kiss(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "kiss",
            "{author_name} kissed {target_name}",
            "{source_name} kissed {target_name}",
            "{target} you were kissed by {author_name}!",
            "{target} you were kissed by {source_name}!",
        )

    @commands.command()
    async def laugh(self, ctx):
        gif_url = await get_reaction_gif("laugh")
        embed = build_action_embed(
            ctx,
            title=f"{ctx.author.display_name} is laughing",
            description=f"{ctx.author.mention} is having a great time.",
            gif_url=gif_url,
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def pat(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "pat",
            "{author_name} patted {target_name}",
            "{source_name} patted {target_name}",
            "{target} got a head pat from {author_name}.",
            "{target} got a head pat from {source_name}.",
        )

    @commands.command()
    async def glare(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "glare",
            "{author_name} glared at {target_name}",
            "{source_name} glared at {target_name}",
            "{author_name} is glaring at {target}.",
            "{source_name} is glaring at {target}.",
        )

    @commands.command()
    async def cry(self, ctx):
        gif_url = await get_reaction_gif("cry")
        embed = build_action_embed(
            ctx,
            title=f"{ctx.author.display_name} is crying",
            description=f"{ctx.author.mention} needs a little comfort right now.",
            gif_url=gif_url,
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(RoleplayCog(bot))
