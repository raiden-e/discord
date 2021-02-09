import json
import os

import config

import discord
from utils.data import Bot, HelpFormat

print("Logging in...")

bot = Bot(
    command_prefix=config.PREFIX, prefix=config.PREFIX,
    owner_ids=config.OWNERS, command_attrs=dict(hidden=True), help_command=HelpFormat(),
    intents=discord.Intents(
        # kwargs found at https://discordpy.readthedocs.io/en/latest/api.html?highlight=intents#discord.Intents
        guilds=True, members=True, messages=True, reactions=True, presences=True
    )
)

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

try:
    if not config.TOKEN == None:
        bot.run(config.TOKEN)
    else:
        import json
        with os.environ.get('config') as cfg:
            config = json.dumps(cfg)
            bot.run(config['token'])
except Exception as e:
    print(f'Error when logging in: {e}')
