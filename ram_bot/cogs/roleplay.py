import discord
from io import BytesIO
from datetime import datetime, timezone
from discord.ext import commands

from ram_bot.constants import GELBOORU_NSFW_PRESETS, GELBOORU_STARTER_TAGS
from ram_bot.dialogue import build_nsfw_command_reply, record_interaction
from ram_bot.embeds import build_action_embed
from ram_bot.gelbooru import download_gelbooru_image, get_gelbooru_post
from ram_bot.reactions import get_reaction_gif


class RoleplayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_profile(self, guild_id: int, user_id: int) -> dict:
        return self.bot.user_profiles.get_profile(f"guild:{guild_id}", user_id)

    def get_context_profile(self, ctx) -> tuple[str, dict]:
        scope = f"guild:{ctx.guild.id}" if ctx.guild is not None else f"dm:{ctx.author.id}"
        return scope, self.bot.user_profiles.get_profile(scope, ctx.author.id)

    async def ensure_nsfw(self, ctx) -> bool:
        if ctx.guild is None:
            return True
        if not hasattr(ctx.channel, "is_nsfw") or not ctx.channel.is_nsfw():
            await ctx.send("That command is only available in DMs or an NSFW server channel.")
            return False
        return True

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def nsfwcategories(self, ctx):
        if not await self.ensure_nsfw(ctx):
            return
        starters = ", ".join(f"`{tag}`" for tag in GELBOORU_STARTER_TAGS)
        await ctx.send(
            "Starter Gelbooru tags:\n"
            f"{starters}\n\n"
            "Ram will always add your global include tags and append your global exclude tags automatically."
        )

    async def send_gelbooru_embed(self, ctx, title: str, query: str):
        try:
            post, tags = await get_gelbooru_post(
                self.bot.config.gelbooru_auth,
                self.bot.config.gelbooru_global_include,
                self.bot.config.gelbooru_global_exclude,
                query,
            )
        except RuntimeError:
            await ctx.send("Gelbooru could not return an image for those tags right now. Try another tag set or use `!nsfwcategories`.")
            return

        scope, profile = self.get_context_profile(ctx)
        profile["affinity"] += 2
        self.bot.user_profiles.save_profile(scope, ctx.author.id, profile)
        reply_text, relationship = build_nsfw_command_reply(self.bot, ctx, title.split(" - ", 1)[-1].lower())
        record_interaction(self.bot, ctx, title.split(" - ", 1)[-1].lower())

        embed = discord.Embed(
            title=title,
            description=(
                f"{ctx.author.mention} requested a Gelbooru image.\n"
                f"{reply_text}\n"
                f"Tags: `{tags[:900]}`"
            ),
            color=discord.Color.from_rgb(248, 186, 203),
            timestamp=ctx.message.created_at,
        )
        image_file = None
        attachment_url = None
        downloaded = await download_gelbooru_image(post["image_url"])
        if downloaded is not None:
            content, filename = downloaded
            image_file = discord.File(BytesIO(content), filename=filename)
            attachment_url = f"attachment://{filename}"
            embed.set_image(url=attachment_url)
        else:
            embed.set_image(url=post["image_url"])
        if post.get("fallback_url"):
            embed.add_field(name="Image Link", value=post["fallback_url"], inline=False)
        embed.set_footer(text=f"Relationship: {relationship}")
        if image_file is not None:
            await ctx.send(embed=embed, file=image_file)
        else:
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def nsfw(self, ctx, *, category: str):
        if not await self.ensure_nsfw(ctx):
            return
        await self.send_gelbooru_embed(ctx, f"NSFW - {category.lower()}", category)

    async def send_nsfw_preset(self, ctx, preset_name: str):
        if not await self.ensure_nsfw(ctx):
            return
        await self.send_gelbooru_embed(ctx, f"NSFW - {preset_name}", GELBOORU_NSFW_PRESETS[preset_name])

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def pussy(self, ctx):
        await self.send_nsfw_preset(ctx, "pussy")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def tits(self, ctx):
        await self.send_nsfw_preset(ctx, "tits")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def ass(self, ctx):
        await self.send_nsfw_preset(ctx, "ass")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def maid(self, ctx):
        await self.send_nsfw_preset(ctx, "maid")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def rammaid(self, ctx):
        await self.send_nsfw_preset(ctx, "rammaid")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def remmaid(self, ctx):
        await self.send_nsfw_preset(ctx, "remmaid")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def anal(self, ctx):
        await self.send_nsfw_preset(ctx, "anal")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def thighs(self, ctx):
        await self.send_nsfw_preset(ctx, "thighs")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def blowjob(self, ctx):
        await self.send_nsfw_preset(ctx, "blowjob")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def paizuri(self, ctx):
        await self.send_nsfw_preset(ctx, "paizuri")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def handjob(self, ctx):
        await self.send_nsfw_preset(ctx, "handjob")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def footjob(self, ctx):
        await self.send_nsfw_preset(ctx, "footjob")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def creampie(self, ctx):
        await self.send_nsfw_preset(ctx, "creampie")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def ahegao(self, ctx):
        await self.send_nsfw_preset(ctx, "ahegao")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def stockings(self, ctx):
        await self.send_nsfw_preset(ctx, "stockings")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def bikini(self, ctx):
        await self.send_nsfw_preset(ctx, "bikini")

    @commands.command(name="naked_apron")
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def naked_apron_command(self, ctx):
        await self.send_nsfw_preset(ctx, "naked_apron")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def bondage(self, ctx):
        await self.send_nsfw_preset(ctx, "bondage")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def tentacles(self, ctx):
        await self.send_nsfw_preset(ctx, "tentacles")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def doggystyle(self, ctx):
        await self.send_nsfw_preset(ctx, "doggystyle")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def facial(self, ctx):
        await self.send_nsfw_preset(ctx, "facial")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def thighjob(self, ctx):
        await self.send_nsfw_preset(ctx, "thighjob")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def armpit(self, ctx):
        await self.send_nsfw_preset(ctx, "armpit")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def lingerie(self, ctx):
        await self.send_nsfw_preset(ctx, "lingerie")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def cum(self, ctx):
        await self.send_nsfw_preset(ctx, "cum")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def yuri(self, ctx):
        await self.send_nsfw_preset(ctx, "yuri")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def uniform(self, ctx):
        await self.send_nsfw_preset(ctx, "uniform")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def public(self, ctx):
        await self.send_nsfw_preset(ctx, "public")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def nude(self, ctx):
        await self.send_nsfw_preset(ctx, "nude")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def spread(self, ctx):
        await self.send_nsfw_preset(ctx, "spread")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def missionary(self, ctx):
        await self.send_nsfw_preset(ctx, "missionary")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def cowgirl(self, ctx):
        await self.send_nsfw_preset(ctx, "cowgirl")

    @commands.command(name="69")
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def sixty_nine(self, ctx):
        await self.send_nsfw_preset(ctx, "69")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def nipples(self, ctx):
        await self.send_nsfw_preset(ctx, "nipples")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def panties(self, ctx):
        await self.send_nsfw_preset(ctx, "panties")

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def garter(self, ctx):
        await self.send_nsfw_preset(ctx, "garter")

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
        record_interaction(self.bot, ctx, action_name)
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
        if not await self.ensure_nsfw(ctx):
            return
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
    async def love(self, ctx, member: discord.Member | None = None):
        if not await self.ensure_nsfw(ctx):
            return
        await self.send_target_action(
            ctx,
            member,
            "love",
            "{author_name} pulled {target_name} closer",
            "{source_name} pulled {target_name} closer",
            "{target} got a heated look from {author_name}.",
            "{target} got a heated look from {source_name}.",
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

    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def bite(self, ctx, member: discord.Member | None = None):
        if not await self.ensure_nsfw(ctx):
            return
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
