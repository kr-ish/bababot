"""
Bababooey bot
"""

import logging
import os
import random
from itertools import product

import discord
from dotenv import load_dotenv

# Create a custom logger that logs to file and to stream
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create separate stream and file handlers
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler('error.log')
stream_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.WARNING)

# Create formatters and add to handlers
log_format = logging.Formatter('%(asctime)s %(levelname)s:%(name)s:%(message)s', datefmt='%d-%b-%y %H:%M:%S')
stream_handler.setFormatter(log_format)
file_handler.setFormatter(log_format)

# Add handlers to the logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler)


# Load env vars
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
USER_ID_TO_DM_ON_ERROR = os.getenv('USER_ID_TO_DM_ON_ERROR')

# Init client
client = discord.Client()


def get_all_bababooeys() -> list:
    """
    Returns all permutations of "bababooey" with acceptable character/ capitalization substitutions.
    :return: list of all bababooeys
    """
    substitutions = {
        'b': '🅱️',
        'o': '0',
        'e': '3',
    }

    char_possibilities = []
    for c in 'bababooey':
        sub = substitutions.get(c)
        if sub is None:
            char_possibilities.append((c, c.capitalize()))
        else:
            char_possibilities.append((c, c.capitalize(), sub))

    all_bababooeys = ["".join(subbed) for subbed in product(*char_possibilities)]
    return all_bababooeys


ALL_BABABOOEYS = get_all_bababooeys()


@client.event
async def on_ready():
    logger.info(f'{client.user} has connected to Discord')


@client.event
async def on_message(message):
    # prevent infinite bababooey :(
    if message.author == client.user:
        return

    if message.content in ALL_BABABOOEYS:
        await message.add_reaction('🅱')  # 🅱️

        # respond to bababooey with text to speech bababooey, image babaooey or random text bababooey
        random_float = random.random()
        if random_float < 0.1:
            await message.channel.send('babAbooey', tts=True)
        elif random_float < 0.2:
            # TODO: instead, just post github link?- discord will auto render..
            with open('doctrine.png', 'rb') as fp:
                await message.reply(file=discord.File(fp, 'doctrine.png'))
        else:
            response = random.choice(ALL_BABABOOEYS)
            await message.reply(response)

    logger.info('yoyoy')
    raise discord.DiscordException


@client.event
async def on_error(event, *args, **kwargs):
    logger.exception("Ruh roh! unhandled exception:")

    # DM user that an error occurred if specified
    user = await client.fetch_user(int(USER_ID_TO_DM_ON_ERROR)) if USER_ID_TO_DM_ON_ERROR else None
    if user:
        await user.send('bababot error! check logs')

client.run(TOKEN)
