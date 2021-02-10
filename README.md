# ![discord_bot.py](https://cdn.discordapp.com/avatars/735515807915704361/824383ea8800e4126a94a4e0c19cc363.png?size=40) Clippy

## Clippy uses the following libs

- Rapptz's [discord.py](https://github.com/Rapptz/discord.py)
- Alex Flipnote's [discord.py template](https://github.com/AlexFlipnote/discord_bot.py) 🍺

## Requirements

- Python 3.6 and up - <https://www.python.org/downloads/>
- git - <https://git-scm.com/download/>

## Useful to always have

Keep [discord.py's docs](https://discordpy.readthedocs.io/en/latest/) saved somewhere.

## How to setup

> You should be able to run either the `setup.sh` or the `setup.ps1` after configuring the bot on Discord

> You can run this on heroku. Make sure to make a `config.py`

1. Make a bot [here](https://discordapp.com/developers/applications/me) and grab the token![Image_Example1](https://i.alexflipnote.dev/f9668b.png)

2. Rename the file **config.py.example* to **config.py**, then fill in the required spots, such as token, prefix and game

3. To install what you need, do 
    ```ps
    # Windows
    pip install -r requirements.txt
    ```
    ```bash
    # bash
    python -m pip install -r requirements.txt
    ```
    `[!NOTE]: Use pip install with Administrator/sudo`


4. Start the bot by having the cmd/terminal inside the bot folder and type 

    `python index.py`

5. You're done, enjoy your bot!

## FAQ

Q: I don't see my bot on my server!

A: Invite it by using this URL: <https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID&scope=bot>

Remember to replace **CLIENT_ID** with your bot client ID
## Optional tools

### Flake8

Flake8 is a tool that helps you keep your code clean. Most coding softwares will have a plugin that supports this Python module so it can be integrated with your IDE. To install it, simply do `pip install flake8`. If you're using python 3.7, install by doing `pip install -e git+https://gitlab.com/pycqa/flake8#egg=flake8`

