import asyncio
import concurrent.futures
import random
import re
import secrets
import time
import urllib
from io import BytesIO

import aiohttp
import config
import duckduckpy
from utils import argparser, gist, http, lists, permissions

import discord
from discord.ext import commands


class Fun_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.alex_api_token = config.ALEXFLIPNOTE_API

    async def randomimageapi(self, ctx, url: str, endpoint: str, token: str = None):
        try:
            r = await http.get(url, res_method="json", no_cache=True, headers={"Authorization": config.ALEXFLIPNOTE_API})
        except aiohttp.ClientConnectorError:
            return await ctx.send("The API seems to be down...")
        except aiohttp.ContentTypeError:
            return await ctx.send("The API returned an error or didn't return JSON...")

        await ctx.send(r[endpoint])

    async def api_img_creator(self, ctx, url: str, filename: str, content: str = None, token: str = None):
        async with ctx.channel.typing():
            req = await http.get(url, res_method="read", headers={"Authorization": config.ALEXFLIPNOTE_API})

            if not req:
                return await ctx.send("I couldn't create the image 😥")

            bio = BytesIO(req)
            bio.seek(0)
            await ctx.send(content=content, file=discord.File(bio, filename=filename))

    @commands.command(aliases=["dis", "d"])
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def disable(self, ctx, *, track: str):
        track = track.strip()
        if re.match(r'^[a-zA-Z0-9]{22}$', track):
            track = f'spotify:track:{track}'
        elif not re.match(r'^spotify:track:([a-zA-Z0-9]{22})$', track):
            return await ctx.send("Incorrect URI format")

        if ctx.author.id == 664221806642593804:
            the_gist = "disabled.json"
            message = "disabled"
        else:
            await ctx.send("I will consider that.")
            the_gist = "by_others.json"
            message = "considered"

        disabled_tracks = gist.load(the_gist)
        if type(disabled_tracks) is not list:
            raise TypeError("not a list", disabled_tracks)
        if track in disabled_tracks:
            return await ctx.send(f"Already {message}: `{track}`")

        disabled_tracks.append(track)

        gist.update(the_gist, disabled_tracks,
                    f"Added track: `{track}`")
        return await ctx.send(f"Added track: {track}")

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def cat(self, ctx):
        """ Posts a random cat """
        await self.randomimageapi(ctx, 'https://api.alexflipnote.dev/cats', 'file', token=self.alex_api_token)

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def dog(self, ctx):
        """ Posts a random dog """
        await self.randomimageapi(ctx, 'https://api.alexflipnote.dev/dogs', 'file', token=self.alex_api_token)

    @commands.command(aliases=["bird"])
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def birb(self, ctx):
        """ Posts a random birb """
        await self.randomimageapi(ctx, 'https://api.alexflipnote.dev/birb', 'file', token=self.alex_api_token)

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def duck(self, ctx):
        """ Posts a random duck """
        await self.randomimageapi(ctx, 'https://random-d.uk/api/v1/random', 'url')

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def coffee(self, ctx):
        """ Posts a random coffee """
        await self.randomimageapi(ctx, 'https://coffee.alexflipnote.dev/random.json', 'file')

    @commands.command(aliases=['8ball'])
    async def eightball(self, ctx, *, question: commands.clean_content):
        """ Consult 8ball to receive an answer """
        answer = random.choice(lists.ballresponse)
        await ctx.send(f"🎱 **Question:** {question}\n**Answer:** {answer}")

    @commands.command(aliases=['flip', 'coin'])
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ['Heads', 'Tails']
        await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

    @commands.command()
    async def f(self, ctx, *, text: commands.clean_content = None):
        """ Press F to pay respect """
        hearts = ['❤', '💛', '💚', '💙', '💜', '🖤', '🤎', '🤍', '♥']
        reason = f"for **{text}** " if text else ""
        await ctx.send(f"**{ctx.author.name}** has paid their respect {reason}{random.choice(hearts)}")

    @commands.command()
    async def supreme(self, ctx, *, text: commands.clean_content(fix_channel_mentions=True)):
        """ Make a fake Supreme logo

        Arguments:
            --dark | Make the background to dark colour
            --light | Make background to light and text to dark colour
        """
        parser = argparser.Arguments()
        parser.add_argument('input', nargs="+", default=None)
        parser.add_argument('-d', '--dark', action='store_true')
        parser.add_argument('-l', '--light', action='store_true')

        args, valid_check = parser.parse_args(text)
        if not valid_check:
            return await ctx.send(args)

        inputText = urllib.parse.quote(' '.join(args.input))
        if len(inputText) > 500:
            return await ctx.send(f"**{ctx.author.name}**, the Supreme API is limited to 500 characters, sorry.")

        darkorlight = None
        if args.dark:
            darkorlight = "dark=true"
        if args.light:
            darkorlight = "light=true"
        if all(args.dark, args.light):
            return await ctx.send(f"**{ctx.author.name}**, you can't define both --dark and --light, sorry..")

        await self.api_img_creator(ctx, f"https://api.alexflipnote.dev/supreme?text={inputText}&{darkorlight}", "supreme.png", token=self.alex_api_token)

    @commands.command(aliases=['color'])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def colour(self, ctx, colour: str):
        """ View the colour HEX details """
        async with ctx.channel.typing():
            if not permissions.can_handle(ctx, "embed_links"):
                return await ctx.send("I can't embed in this channel ;-;")

            if colour == "random":
                colour = "%06x" % random.randint(0, 0xFFFFFF)

            if colour[:1] == "#":
                colour = colour[1:]

            if not re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', colour):
                return await ctx.send("You're only allowed to enter HEX (0-9 & A-F)")

            try:
                r = await http.get(
                    f"https://api.alexflipnote.dev/colour/{colour}", res_method="json",
                    no_cache=True, headers={"Authorization": self.alex_api_token}
                )
            except aiohttp.ClientConnectorError:
                return await ctx.send("The API seems to be down...")
            except aiohttp.ContentTypeError:
                return await ctx.send("The API returned an error or didn't return JSON...")

            embed = discord.Embed(colour=r["int"])
            embed.set_thumbnail(url=r["image"])
            embed.set_image(url=r["image_gradient"])

            embed.add_field(name="HEX", value=r['hex'], inline=True)
            embed.add_field(name="RGB", value=r['rgb'], inline=True)
            embed.add_field(name="Int", value=r['int'], inline=True)
            embed.add_field(name="Brightness",
                            value=r['brightness'], inline=True)

            await ctx.send(embed=embed, content=f"{ctx.invoked_with.title()} name: **{r['name']}**")

    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def urban(self, ctx, *, search: commands.clean_content):
        """ Find the 'best' definition to your words """
        async with ctx.channel.typing():
            try:
                url = await http.get(f'https://api.urbandictionary.com/v0/define?term={search}', res_method="json")
            except Exception:
                return await ctx.send("Urban API returned invalid data... might be down atm.")

            if not url:
                return await ctx.send("I think the API broke...")

            if not len(url['list']):
                return await ctx.send("Couldn't find your search in the dictionary...")

            result = sorted(url['list'], reverse=True,
                            key=lambda g: int(g["thumbs_up"]))[0]

            definition = result['definition']
            if len(definition) >= 1000:
                definition = definition[:1000]
                definition = definition.rsplit(' ', 1)[0]
                definition += '...'

            await ctx.send(f"📚 Definitions for **{result['word']}**```fix\n{definition}```")

    @commands.command()
    async def reverse(self, ctx, *, text: str):
        """ !poow ,ffuts esreveR
        Everything you type after reverse will of course, be reversed
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev}")

    @commands.command()
    async def password(self, ctx, nbytes: int = 18):
        """ Generates a random password string for you

        This returns a random URL-safe text string, containing nbytes random bytes.
        The text is Base64 encoded, so on average each byte results in approximately 1.3 characters.
        """
        if nbytes not in range(3, 1401):
            return await ctx.send("I only accept any numbers between 3-1400")
        if hasattr(ctx, 'guild') and ctx.guild is not None:
            await ctx.send(f"Sending you a private message with your random generated password **{ctx.author.name}**")
        await ctx.author.send(f"🎁 **Here is your password:**\n{secrets.token_urlsafe(nbytes)}")

    @commands.command()
    async def rate(self, ctx, *, thing: commands.clean_content):
        """ Rates what you desire """
        rate_amount = random.uniform(0.0, 100.0)
        await ctx.send(f"I'd rate `{thing}` a **{round(rate_amount, 4)} / 100**")

    @commands.command()
    async def beer(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
        """ Give someone a beer! 🍻 """
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.name}**: paaaarty!🎉🍺")
        if user.id == self.bot.user.id:
            return await ctx.send("*drinks beer with you* 🍻")
        if user.bot:
            return await ctx.send(f"I would love to give beer to the bot **{ctx.author.name}**, but I don't think it will respond to you :/")

        beer_offer = f"**{user.name}**, you got a 🍺 offer from **{ctx.author.name}**"
        if reason:
            beer_offer = f"{beer_offer}\n\n**Reason:** {reason}"
        msg = await ctx.send(beer_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
                return True
            return False

        try:
            await msg.add_reaction("🍻")
            await self.bot.wait_for('raw_reaction_add', timeout=30.0, check=reaction_check)
            await msg.edit(content=f"**{user.name}** and **{ctx.author.name}** are enjoying a lovely beer together 🍻")
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f"well, doesn't seem like **{user.name}** wanted a beer with you **{ctx.author.name}** ;-;")
        except discord.Forbidden:
            # Yeah so, bot doesn't have reaction permission, drop the "offer" word
            beer_offer = f"**{user.name}**, you got a 🍺 from **{ctx.author.name}**"
            beer_offer = beer_offer + \
                f"\n\n**Reason:** {reason}" if reason else beer_offer
            await msg.edit(content=beer_offer)

    @commands.command(aliases=['slots', 'bet'])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
        else:
            await ctx.send(f"{slotmachine} No match, you lost 😢")

    @commands.command(aliases=['google', 'ws', 'ddg'])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def search(self, ctx, *, query: commands.clean_content):
        """ Search DuckDuckGo """
        response = None

        async with ctx.channel.typing():
            try:
                with concurrent.futures.ThreadPoolExecutor() as _executor:
                    future = _executor.submit(duckduckpy.query, query)
                    response = future.result()
            except Exception:
                return await ctx.send("Something went wrong...")

            if response.answer:
                return await ctx.send(response.answer)

            if response.abstract_source:
                dc_response = f"From `{response.abstract_source}`:\n{response.abstract_url}"

                if response.related_topics:
                    dc_response += "\n\nOther sources:\n"
                    for topic in response.related_topics:
                        if isinstance(type(topic), duckduckpy.api.Result):
                            dc_response += f"{topic.text}\n"
                        if isinstance(type(topic), duckduckpy.api.RelatedTopic):
                            dc_response += f"Related: {topic.name}\n"
                return await ctx.send(dc_response)

            if response.image:
                return await ctx.send(response.image)

            return await ctx.send("No results...")


def setup(bot):
    bot.add_cog(Fun_Commands(bot))
