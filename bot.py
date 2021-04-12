"""
Bababooey bot
"""

from io import BytesIO
from itertools import product
import logging
import os
import random
import urllib.request

import discord
from discord.ext import commands
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

# Init bot
bot = commands.Bot(command_prefix='!')


def get_all_bababooeys() -> list:
    """
    Returns all permutations of "bababooey" with acceptable character substitutions.
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
            char_possibilities.append((c))
        else:
            char_possibilities.append((c, sub))

    all_bababooeys = ["".join(subbed) for subbed in product(*char_possibilities)]
    return all_bababooeys


ALL_BABABOOEYS = get_all_bababooeys()


@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord')


@bot.event
async def on_message(message):
    # prevent infinite bababooey :(
    if message.author == bot.user:
        return

    for word in message.content.lower().split(' '):
        if word in ALL_BABABOOEYS:
            await message.add_reaction('🅱️')  # 🅱️

            # respond to bababooey with text to speech bababooey, image babaooey or random text bababooey
            random_float = random.random()
            if random_float < 0.1:
                await message.channel.send('babAbooey', tts=True)
            elif random_float < 0.2:
                # TODO: instead, just post github link?- discord will auto render..
                await message.reply(file=discord.File('doctrine.png'))
            elif random_float < 0.3:
                await message.reply(file=discord.File('babaisbooey.png'))
            elif random_float < 0.32: # this one is extra, extra bad so make it rare
                await message.reply(file=discord.File('noyes.png'))
            else:
                response = random.choice(ALL_BABABOOEYS)
                await message.reply(response)

    # process bot commands
    await bot.process_commands(message)


@bot.command(name='c', help='Posts lastfm chart for the given user for the given duration. Usage: !c [last fm username] [duration - (w/m)]')
async def fm_chart(ctx, fm_username: str, duration: str = 'w'):
    duration_to_tapmusic_type = {
        'w': '7day',
        'm': '1month',
    }
    tapmusic_type = duration_to_tapmusic_type[duration]
    image = BytesIO(urllib.request.urlopen(f'https://tapmusic.net/collage.php?user={fm_username}&type={tapmusic_type}&size=5x5&caption=true').read())
    await ctx.send(file=discord.File(image, filename=f'{fm_username}_{duration}.jpg'))


@bot.event
async def on_error(event, *args, **kwargs):
    logger.exception("Ruh roh! unhandled exception:")

    # DM user that an error occurred if specified
    user = await bot.fetch_user(int(USER_ID_TO_DM_ON_ERROR)) if USER_ID_TO_DM_ON_ERROR else None
    if user:
        await user.send('bababot error! check logs')

bot.run(TOKEN)
