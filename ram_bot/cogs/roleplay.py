import discord
from datetime import datetime, timezone
from discord.ext import commands

from ram_bot.embeds import build_action_embed
from ram_bot.reactions import get_reaction_gif


class RoleplayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_profile(self, guild_id: int, user_id: int) -> dict:
        return self.bot.user_profiles.get_profile(f"guild:{guild_id}", user_id)

    async def post_roleplay_bonus(self, ctx, action_name: str):
        if ctx.guild is None:
            return
        profile = self.get_profile(ctx.guild.id, ctx.author.id)
        now = datetime.now(timezone.utc)
        previous_at_raw = profile.get("last_roleplay_at")
        if previous_at_raw:
            previous_at = datetime.fromisoformat(previous_at_raw)
            if (now - previous_at).total_seconds() > 600:
                profile["last_roleplay_action"] = None

        profile["affinity"] += 1
        profile["last_roleplay_action"] = action_name
        profile["last_roleplay_at"] = now.isoformat()
        self.bot.user_profiles.save_profile(f"guild:{ctx.guild.id}", ctx.author.id, profile)
        event_statuses = {
            "hug": "Delivering hugs with reluctance",
            "kiss": "Pretending not to notice the flirting",
            "cuddle": "Allowing brief affection",
            "glare": "Watching someone with disappointment",
            "cry": "Enduring an inconvenient emotional moment",
        }
        status = event_statuses.get(action_name)
        if status:
            await self.bot.set_temporary_presence(status, seconds=12)

    async def send_self_action(self, ctx, action_name: str, title: str, description: str):
        gif_url = await get_reaction_gif(action_name)
        embed = build_action_embed(
            ctx,
            title=title.format(author_name=ctx.author.display_name),
            description=description.format(author=ctx.author.mention, author_name=ctx.author.display_name),
            gif_url=gif_url,
        )
        await ctx.send(embed=embed)
        await self.post_roleplay_bonus(ctx, action_name)

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
        await self.post_roleplay_bonus(ctx, action_name)

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
    async def airkiss(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "airkiss",
            "{author_name} blew a kiss to {target_name}",
            "{source_name} blew a kiss to {target_name}",
            "{target} got an air kiss from {author_name}.",
            "{target} got an air kiss from {source_name}.",
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
    async def cheers(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "cheers",
            "{author_name} clinked glasses with {target_name}",
            "{source_name} clinked glasses with {target_name}",
            "{target} shared a cheerful toast with {author_name}.",
            "{target} shared a cheerful toast with {source_name}.",
        )

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def clap(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "clap",
            "{author_name} applauded {target_name}",
            "{source_name} applauded {target_name}",
            "{target} is being applauded by {author_name}.",
            "{target} is being applauded by {source_name}.",
        )

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def handhold(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "handhold",
            "{author_name} held {target_name}'s hand",
            "{source_name} held {target_name}'s hand",
            "{target} is holding hands with {author_name}.",
            "{target} is holding hands with {source_name}.",
        )

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def poke(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "poke",
            "{author_name} poked {target_name}",
            "{source_name} poked {target_name}",
            "{target} got poked by {author_name}.",
            "{target} got poked by {source_name}.",
        )

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def nuzzle(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "nuzzle",
            "{author_name} nuzzled {target_name}",
            "{source_name} nuzzled {target_name}",
            "{target} got a soft nuzzle from {author_name}.",
            "{target} got a soft nuzzle from {source_name}.",
        )

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def tickle(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "tickle",
            "{author_name} tickled {target_name}",
            "{source_name} tickled {target_name}",
            "{target} is being tickled by {author_name}.",
            "{target} is being tickled by {source_name}.",
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
    async def smile(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "smile",
            "{author_name} smiled at {target_name}",
            "{source_name} smiled at {target_name}",
            "{author} smiled at {target}.",
            "{target} got a soft smile from {source_name}.",
        )

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def shy(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "shy",
            "{author_name} looked shy around {target_name}",
            "{source_name} looked shy around {target_name}",
            "{author} is acting shy around {target}.",
            "{target} made {source_name} act unexpectedly shy.",
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
    async def lick(self, ctx, member: discord.Member | None = None):
        await self.send_target_action(
            ctx,
            member,
            "lick",
            "{author_name} licked {target_name}",
            "{source_name} licked {target_name}",
            "{target} got licked by {author_name}.",
            "{target} got licked by {source_name}.",
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
