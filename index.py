import json
import os

try:
    with open("config.json", "r", encoding='utf-8-sig') as data:
        config = json.loads(data.read())

except FileNotFoundError:
    try:
        config = os.environ.get('config')
    except Exception:
        raise "Could not load 'config' from env"
    if not config or config == "":
        raise "Could not load 'config' from env"
    with open("config.json", mode="w", encoding='utf-8-sig') as data:
        data.write(config)
    try:
        with open("config.json", mode="r", encoding='utf-8-sig') as data:
            config = json.load(data.read())
    except Exception:
        config = os.environ.get('config')

import discord

from utils.data import Bot, HelpFormat

# config = default.config()
print("Logging in...")

bot = Bot(
    command_prefix=config["prefix"], prefix=config["prefix"],
    owner_ids=config["owners"], command_attrs=dict(hidden=True), help_command=HelpFormat(),
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
    if not config["token"] == None:
        bot.run(config["token"])
    else:
        import json
        with os.environ.get('config') as cfg:
            config = json.dumps(cfg)
            bot.run(config['token'])
except Exception as e:
    print(f'Error when logging in: {e}')
