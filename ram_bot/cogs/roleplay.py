import discord
from discord.ext import commands

from ram_bot.embeds import build_action_embed
from ram_bot.reactions import get_reaction_gif


class RoleplayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_self_action(self, ctx, action_name: str, title: str, description: str):
        gif_url = await get_reaction_gif(action_name)
        embed = build_action_embed(
            ctx,
            title=title.format(author_name=ctx.author.display_name),
            description=description.format(author=ctx.author.mention, author_name=ctx.author.display_name),
            gif_url=gif_url,
        )
        await ctx.send(embed=embed)

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
        await self.send_self_action(
            ctx,
            "laugh",
            "{author_name} is laughing",
            "{author} is having a great time.",
        )

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
    async def cuddle(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "cuddle",
            "{author_name} cuddled {target_name}",
            "{source_name} cuddled {target_name}",
            "{target} got a cozy cuddle from {author_name}.",
            "{target} got a cozy cuddle from {source_name}.",
        )

    @commands.command()
    async def wave(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "wave",
            "{author_name} waved at {target_name}",
            "{source_name} waved at {target_name}",
            "{target} got a cute wave from {author_name}.",
            "{target} got a cute wave from {source_name}.",
        )

    @commands.command()
    async def blush(self, ctx):
        await self.send_self_action(
            ctx,
            "blush",
            "{author_name} is blushing",
            "{author} is feeling a little shy right now.",
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
        await self.send_self_action(
            ctx,
            "cry",
            "{author_name} is crying",
            "{author} needs a little comfort right now.",
        )

    @commands.command(hidden=True)
    async def bite(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "bite",
            "{author_name} bit {target_name}",
            "{source_name} bit {target_name}",
            "{target} got bitten by {author_name}!",
            "{target} got bitten by {source_name}!",
        )

    @commands.command(hidden=True)
    async def smug(self, ctx):
        await self.send_self_action(
            ctx,
            "smug",
            "{author_name} is feeling smug",
            "{author} looks very pleased with themselves.",
        )

    @commands.command(hidden=True)
    async def pout(self, ctx):
        await self.send_self_action(
            ctx,
            "pout",
            "{author_name} is pouting",
            "{author} is being adorably stubborn right now.",
        )


async def setup(bot):
    await bot.add_cog(RoleplayCog(bot))
