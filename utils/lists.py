import discord
ballresponse = [
    'Yes', 'No', 'Take a wild guess...', 'Very doubtful',
    'Sure', 'Without a doubt', 'Most likely', 'Might be possible',
    "You'll be the judge", 'ask someone else', 'maybe',
    'Perhaps'
]

spotify_reg = [
    r'^[a-zA-Z0-9]{22}$',
    r'^((http|https):\/\/){0,1}open\.spotify\.com\/track\/[a-zA-Z0-9]{22}',
    r'^spotify:track:([a-zA-Z0-9]{22})$'
]


def welcome(user: discord.Member):
    import random
    welcome = [
        f'Good to see you, <@!{user.id}>.', f'A wild <@!{user.id}> appeared.', f'Welcome <@!{user.id}>. Say hi!',
        f'Everyone welcome <@!{user.id}>!', f'Glad you\'re here <@!{user.id}>', f'<@!{user.id}> just landed.',
        f'Yay you made it, <@!{user.id}>', f'<@!{user.id}> just slid into the server.',
        f"Hey <@!{user.id}>! It looks like you need help!"
    ]
    return random.choice(welcome)
