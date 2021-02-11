import asyncio
import ctypes
import os
from datetime import datetime

import config
import psutil
from utils import default, lists

import discord
from discord.ext import commands
from discord.ext.commands import errors


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, errors.MissingRequiredArgument) or isinstance(err, errors.BadArgument):
            helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(
                ctx.command)
            await ctx.send_help(helper)

        elif isinstance(err, errors.CommandInvokeError):
            error = default.traceback_maker(err.original)

            if "2000 or fewer" in str(err) and len(ctx.message.clean_content) > 1900:
                return await ctx.send(
                    "You attempted to make the command display more than 2,000 characters...\n"
                    "Both error and command will be ignored."
                )

            await ctx.send(f"There was an error processing the command ☹\n{error}")

        elif isinstance(err, errors.CheckFailure):
            pass

        elif isinstance(err, errors.MaxConcurrencyReached):
            await ctx.send("You've reached max capacity of command usage at once, please finish the previous one...")

        elif isinstance(err, errors.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown... try again in {err.retry_after:.2f} seconds.")

        elif isinstance(err, errors.CommandNotFound):
            pass

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if not config.JOIN_MESSAGE:
            return

        try:
            to_send = sorted([chan for chan in guild.channels if chan.permissions_for(
                guild.me).send_messages and isinstance(chan, discord.TextChannel)], key=lambda x: x.position)[0]
        except IndexError:
            pass
        else:
            await to_send.send(config.JOIN_MESSAGE)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role, mods = None, None
        mods = config.MODS
        for mod, id in mods.items():
            if member.guild.id == int(mod):
                role = member.guild.get_role(id)
            # if member.guild.id == mod

        if role:
            await member.add_roles(role)
        else:
            print("no member role")

        channel = member.guild.system_channel
        if channel is not None:
            message = lists.welcome(member.display_name)
            await channel.send(message)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        try:
            print(f"{ctx.guild.name} > {ctx.author} > {ctx.message.clean_content}")
        except AttributeError:
            print(
                f"Private message > {ctx.author} > {ctx.message.clean_content}")

    @commands.Cog.listener()
    async def on_ready(self):
        """ The function that activates when boot was completed """
        if not hasattr(self.bot, 'uptime'):
            self.bot.uptime = datetime.utcnow()

        # Check if user desires to have something other than online
        status = config.STATUS_TYPE.lower()
        status_type = {"idle": discord.Status.idle, "dnd": discord.Status.dnd}

        # Check if user desires to have a different type of activity
        activity = config.ACTIVITY_TYPE.lower()
        activity_type = {"listening": 2, "watching": 3, "competing": 5}

        await self.bot.change_presence(
            activity=discord.Game(
                type=activity_type.get(activity, 0), name=config.ACTIVITY
            ),
            status=status_type.get(status, discord.Status.online)
        )

        # Indicate that the bot has successfully booted up
        print(f'Ready: {self.bot.user} | Servers: {len(self.bot.guilds)}')


def setup(bot):
    bot.add_cog(Events(bot))
