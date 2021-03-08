"""
Bababooey bot
"""

import os
import asyncio

import discord
from dotenv import load_dotenv

# Load env vars
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Init client
client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord')

    message = await get_message_by_id(channel_id=754850483017089128, message_id=804396187561361418)   # general among utc
    # message = await get_message_by_id(channel_id=676550314593222717, message_id=802668709478793216)
    # print(message)
    # await asyncio.sleep(1)
    # await message.add_reaction('🅱️')  # 🅱️
    # await message.add_reaction('🅱️')  # 🅱️
    # await message.add_reaction('🆎')  # 🅱️
    # await message.add_reaction('🅰️')  # 🅱️ :b::ab::a:
    # emoji = client.get_emoji(676838265764052992)  # :patrickbinocs: (use /:patrickbinocs: to get id)
    emoji = client.get_emoji(756637715323158620)  # :yellow: amongus (use /:yellow: to get id or copy link from chat)
    await message.add_reaction(emoji)
    # await message.reply('oh yes')


async def get_message_by_id(channel_id, message_id):
        channel = client.get_channel(channel_id)
        print(channel)
        # try:
        msg = await channel.fetch_message(message_id)
        print(msg)
        return msg
        # except discord.NotFound:
        #     continue
        # print(msg.content)


@client.event
async def on_error(event, *args, **kwargs):
    print("Ruh roh! unhandled exception:")
    raise


client.run(TOKEN)
