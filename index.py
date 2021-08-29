import os

import discord
from utils.data import Bot, HelpFormat

config_json = False
try:
    import config
except ImportError:
    if os.environ.get('config'):
        raise ImportError("Can not load config")
    import json
    config = json.dumps(os.environ.get('config'))
    config_json = True

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
        bot.load_extension(f"cogs.{file[:-3]}")

try:
    bot.run(config['token'] if config_json else config.TOKEN)
except Exception as e:
    print(f'Error when logging in:\n{e}')
