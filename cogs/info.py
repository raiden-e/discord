import os
import time
from datetime import datetime

import config
import psutil
from utils import default, permissions

import discord
from discord.ext import commands


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())

    @commands.command(aliases=['test'])
    async def ping(self, ctx):
        """ Pong! """
        before = time.monotonic()
        before_ws = int(round(self.bot.latency * 1000, 1))
        message = await ctx.send("🏓 Pong")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms")

    @commands.command(aliases=['joinme', 'join', 'botinvite'])
    async def invite(self, ctx):
        """ Invite me to your server """
        await ctx.send(f"**{ctx.author.name}**, use this URL to invite me\n<{discord.utils.oauth_url(self.bot.user.id)}>")

    @commands.command()
    async def source(self, ctx):
        """ Check out my source code =) """
        # Do not remove this command, this has to stay due to the GitHub LICENSE.
        # TL:DR, you have to disclose source according to MIT.
        # Reference: https://github.com/AlexFlipnote/discord_bot.py/blob/master/LICENSE
        await ctx.send(f"**{ctx.bot.user}**'s repo is https://github.com/raiden-e/discord\n"
                       f"and powered by:\n"
                       f"https://github.com/Rapptz/discord.py\n"
                       f"https://github.com/AlexFlipnote/discord_bot.py")

    @commands.command(aliases=['supportserver', 'feedbackserver'])
    async def botserver(self, ctx):
        """ Get an invite to our support server! """
        async def get_inv():
            guild = self.bot.get_guild(config.INVITE[0])
            channel = guild.get_channel(config.INVITE[1])
            return await channel.create_invite(
                max_age=300, max_uses=1, reason="botserver")
        try:
            if isinstance(ctx.channel, discord.DMChannel):
                await ctx.author.send(f"Here you go, **{ctx.author}**!\n{await get_inv()}")
            else:
                if ctx.guild.id == config.INVITE[0]:
                    await ctx.send(f"**{ctx.author.name}**, this is my home you know")
                else:
                    await ctx.author.send(f"Here you go, **{ctx.author}**!\n{await get_inv()}")
                    if permissions.can_handle(ctx, "add_reactions"):
                        await ctx.message.add_reaction(chr(0x2709))
                    else:
                        await ctx.send("Check ur dm's")
        except AttributeError as e:
            await ctx.send(f"Where did I come from!?!")
            raise e

    @commands.command(aliases=['ver'])
    async def version(self, ctx):
        """ Get an invite to our support server! """
        return await ctx.send(f"Im on another level!\nversion: **{config.VERSION}**")

    @commands.command(aliases=['info', 'stats', 'status'])
    async def about(self, ctx):
        """ About the bot """
        ramUsage = self.process.memory_full_info().rss / 1024**2
        avgmembers = round(len(self.bot.users) / len(self.bot.guilds))

        embedColour = discord.Embed.Empty
        if hasattr(ctx, 'guild') and ctx.guild is not None:
            embedColour = ctx.me.top_role.colour

        embed = discord.Embed(colour=embedColour)
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.add_field(name="Last boot", value=default.timeagoo(
            datetime.now() - self.bot.uptime), inline=True)
        embed.add_field(
            name=f"Developer{'' if len(config.OWNERS) == 1 else 's'}",
            value=', '.join(
                [str(self.bot.get_user(x)) for x in config.OWNERS]
            ),
            inline=True)
        embed.add_field(name="Library", value="discord.py", inline=True)
        embed.add_field(
            name="Servers", value=f"{len(ctx.bot.guilds)} ( avg: {avgmembers} users/server )", inline=True)
        embed.add_field(name="Commands loaded", value=len(
            [x.name for x in self.bot.commands]), inline=True)
        embed.add_field(name="RAM", value=f"{ramUsage:.2f} MB", inline=True)

        await ctx.send(content=f"ℹ About **{ctx.bot.user}** | **{config.VERSION}**", embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
