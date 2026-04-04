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
    @commands.cooldown(1, 4, commands.BucketType.user)
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
    @commands.cooldown(1, 4, commands.BucketType.user)
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
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def laugh(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "laugh",
            "{author_name} laughed with {target_name}",
            "{source_name} laughed with {target_name}",
            "{target} is laughing with {author_name}.",
            "{target} is laughing with {source_name}.",
        )

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
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
    @commands.cooldown(1, 4, commands.BucketType.user)
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
    @commands.cooldown(1, 4, commands.BucketType.user)
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
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def blush(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "blush",
            "{author_name} blushed at {target_name}",
            "{source_name} blushed at {target_name}",
            "{author} is blushing at {target}.",
            "{target} made {source_name} blush.",
        )

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
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
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def cry(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "cry",
            "{author_name} cried with {target_name}",
            "{source_name} cried with {target_name}",
            "{author} is crying with {target}.",
            "{target} is crying with {source_name}.",
        )

    @commands.command(hidden=True)
    @commands.cooldown(1, 4, commands.BucketType.user)
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
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def smug(self, ctx):
        await self.send_self_action(
            ctx,
            "smug",
            "{author_name} is feeling smug",
            "{author} looks very pleased with themselves.",
        )

    @commands.command(hidden=True)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def pout(self, ctx):
        await self.send_self_action(
            ctx,
            "pout",
            "{author_name} is pouting",
            "{author} is being adorably stubborn right now.",
        )


async def setup(bot):
    await bot.add_cog(RoleplayCog(bot))
