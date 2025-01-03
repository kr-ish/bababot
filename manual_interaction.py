"""
CLI to manually trigger messages responses / reactions from the bot
"""

import os
import asyncio
import typer

import discord
from dotenv import load_dotenv

# Load env vars
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Init Discord client
client = discord.Client()

# Init CLI app
app = typer.Typer()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord')
    # app()
    # await reply([channel_id], [msg_id], "[text]")
    # await react([channel_id], [msg_id], "[emoji]")


@client.event
async def on_error(event, *args, **kwargs):
    print("Ruh roh! unhandled exception:")
    raise


@app.command()
async def react(channel_id: int, message_id: int, reaction: str):
    typer.echo(f"Reacting to {channel_id}, {message_id}")
    channel = client.get_channel(channel_id)
    msg = await channel.fetch_message(message_id)
    await msg.add_reaction(reaction)


@app.command()
async def reply(channel_id: int, message_id: int, text: str):
     typer.echo(f"Replying to {channel_id}, {message_id}")
     channel = client.get_channel(channel_id)
     msg = await channel.fetch_message(message_id)
     await channel.send(text, reference=msg)


if __name__ == '__main__':
    client.run(TOKEN)
