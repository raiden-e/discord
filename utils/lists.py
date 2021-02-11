ballresponse = [
    'Yes', 'No', 'Take a wild guess...', 'Very doubtful',
    'Sure', 'Without a doubt', 'Most likely', 'Might be possible',
    "You'll be the judge", 'ask someone else', 'maybe',
    'Perhaps'
]


def welcome(name):
    import random
    welcome = [
        f'Good to see you, **{name}**.', f'A wild **{name}** appeared.', f'Welcome **{name}**. Say hi!',
        f'Everyone welcome **{name}**!', f'Glad you\'re here **{name}**', f'**{name}** just landed.',
        f'Yay you made it, **{name}**', f'**{name}** just slid into the server.'
    ]
    return random.choice(welcome)
