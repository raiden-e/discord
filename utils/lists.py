import discord
ballresponse = [
    'Yes', 'No', 'Take a wild guess...', 'Very doubtful',
    'Sure', 'Without a doubt', 'Most likely', 'Might be possible',
    "You'll be the judge", 'ask someone else', 'maybe',
    'Perhaps'
]

spotify_reg = [
    r'^[a-zA-Z0-9]{22}$', # assume track
    r'^((http|https):\/\/){0,1}open\.spotify\.com\/album\/[a-zA-Z0-9]{22}',
    r'^((http|https):\/\/){0,1}open\.spotify\.com\/track\/[a-zA-Z0-9]{22}',
    r'^spotify:album:([a-zA-Z0-9]{22})$',
    r'^spotify:track:([a-zA-Z0-9]{22})$',
]


def welcome(user: discord.Member):
    import random
    welcome = [
        f'Good to see you, <@!{user.id}>.',
        f'Welcome <@!{user.id}>. Say hi!',
        f'Everyone welcome <@!{user.id}>!',
        f'Glad you\'re here <@!{user.id}>',
        f'Yay you made it, <@!{user.id}>',
        f'<@!{user.id}> just slid into the server.',
        f"Hey <@!{user.id}>! It looks like you need help!",
        f"Welcome to Jurassic Park, <@!{user.id}>!",
        f"<@!{user.id}> just joined the server - glhf!",
        f"<@!{user.id}> just joined. Everyone, look busy!",
        f"<@!{user.id}> just joined. Can I get a heal?",
        f"<@!{user.id}> joined your party.",
        f"<@!{user.id}> joined. You must construct additional pylons.",
        f"Ermagherd. <@!{user.id}> is here.",
        f"Welcome, <@!{user.id}>. Stay awhile and listen.",
        f"Welcome, <@!{user.id}>. We were expecting you ( ͡° ͜ʖ ͡°)",
        f"Welcome, <@!{user.id}>. We hope you brought pizza.",
        f"Welcome <@!{user.id}>. Leave your weapons by the door.",
        f"A wild <@!{user.id}> appeared.",
        f"Swoooosh. <@!{user.id}> just landed.",
        f"Brace yourselves. <@!{user.id}> just joined the server.",
        f"<@!{user.id}> just joined. Hide your bananas.",
        f"<@!{user.id}> just arrived. Seems OP - please nerf.",
        f"A <@!{user.id}> has spawned in the server.",
        f"Big <@!{user.id}> showed up!",
        f"Where’s <@!{user.id}>? In the server!",
        f"<@!{user.id}> hopped into the server. Kangaroo!!",
        f"<@!{user.id}> just showed up. Hold my beer.",
        f"Challenger approaching - <@!{user.id}> has appeared!",
        f"It's a bird! It's a plane! Nevermind, it's just <@!{user.id}>.",
        f"It's <@!{user.id}>! Praise the sun! [T]/",
        f"Never gonna give <@!{user.id}> up. Never gonna let <@!{user.id}> down.",
        f"Ha! <@!{user.id}> has joined! You activated my trap card!",
        f"Cheers, love! <@!{user.id}>'s here!",
        f"Hey! Listen! <@!{user.id}> has joined!",
        f"We've been expecting you <@!{user.id}>",
        f"It's dangerous to go alone, take <@!{user.id}>!",
        f"<@!{user.id}> has joined the server! It's super effective!",
        f"Cheers, love! <@!{user.id}> is here!",
        f"<@!{user.id}> is here, as the prophecy foretold.",
        f"<@!{user.id}> has arrived. Party's over.",
        f"Ready player <@!{user.id}>",
        f"<@!{user.id}> is here to kick butt and chew bubblegum. And <@!{user.id}> is all out of gum.",
        f"Hello. Is it <@!{user.id}> you're looking for?",
        f"<@!{user.id}> has joined. Stay a while and listen!",
        f"Roses are red, violets are blue, <@!{user.id}> joined this server with you",
    ]
    return random.choice(welcome)
