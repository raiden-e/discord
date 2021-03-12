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


def welcome(name):
    import random
    welcome = [
        f'Good to see you, **{name}**.', f'A wild **{name}** appeared.', f'Welcome **{name}**. Say hi!',
        f'Everyone welcome **{name}**!', f'Glad you\'re here **{name}**', f'**{name}** just landed.',
        f'Yay you made it, **{name}**', f'**{name}** just slid into the server.',
        f"Hey **{name}**! It looks like you need help!"
    ]
    return random.choice(welcome)
