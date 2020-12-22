import asyncio
import ctypes
import os
from datetime import datetime

import psutil
from utils import default

import discord
from discord.ext import commands
from discord.ext.commands import errors


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()
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
        if not self.config["join_message"]:
            return

        try:
            to_send = sorted([chan for chan in guild.channels if chan.permissions_for(
                guild.me).send_messages and isinstance(chan, discord.TextChannel)], key=lambda x: x.position)[0]
        except IndexError:
            pass
        else:
            await to_send.send(self.config["join_message"])

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
        status = self.config["status_type"].lower()
        status_type = {"idle": discord.Status.idle, "dnd": discord.Status.dnd}

        # Check if user desires to have a different type of activity
        activity = self.config["activity_type"].lower()
        activity_type = {"listening": 2, "watching": 3, "competing": 5}

        await self.bot.change_presence(
            activity=discord.Game(
                type=activity_type.get(activity, 0), name=self.config["activity"]
            ),
            status=status_type.get(status, discord.Status.online)
        )

        # Indicate that the bot has successfully booted up
        print(f'Ready: {self.bot.user} | Servers: {len(self.bot.guilds)}')

    @commands.Cog.listener()
    async def on_voice_state_update(ctx, member, before, after):
        audio_source = os.path.join(os.getcwd(), "audio", f"{member}.mp3")
        if member != ctx.user and os.path.exists(audio_source) and after.channel != None and before.channel != after.channel:
            print(f"ctx:   {ctx}")
            print(f"User  {member}\nfrom  {before}\nto    {after}")

            vc = await after.channel.connect()
            print(f"Connected to: {ctx.voice_clients}")

            try:
                if os.system() == 'win32':
                    executable = os.path.join(os.getcwd(), "bin", "ffmpeg.exe")
                    source = await discord.PCMVolumeTransformer(
                        discord.FFmpegPCMAudio(audio_source, executable=executable))
                else:
                    if not discord.opus.is_loaded():
                        discord.opus.load_opus(
                            ctypes.util.find_library('opus'))
                    source = await discord.FFmpegOpusAudio.from_probe(audio_source)
            except Exception as e:
                print(e)
                await vc.disconnect()
                return
            print(source)

            try:
                await asyncio.sleep(2)
                print(vc.play(
                    source,
                    after=lambda e: print(f'Player error: {e}') if e else None)
                )
            except Exception as e:
                print(str(e))

            await asyncio.sleep(1)
            await vc.disconnect()


def setup(bot):
    bot.add_cog(Events(bot))
