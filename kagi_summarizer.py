"""
This is all of the code for a discord bot that will summarize the given url
content

invoke with `/summarize`
"""

import os

import discord

from dotenv import load_dotenv
load_dotenv()

from kagiapi import KagiClient

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

@tree.command(name="summarize", description="Summarizes the given url content")
@discord.app_commands.describe(url="The url to summarize")
async def summarize(ctx, url: str):
    """
    The main bot entrypoint
    """
    print('slash command is working')

    channel = ctx.channel

    if url is None:
        await channel.send('Please provide a url to summarize')

    summary = await get_summary(url)

    await channel.send(summary)

async def get_summary(url):
    """
    Get the summary from Kagi
    """
    print('summarizer')

    kagi = KagiClient(os.environ.get('KAGI_TOKEN'))
    result = kagi.summarize(url=url, engine="cecil")
    return result["data"]["output"]

# Sync slash command to Discord.
@bot.event
async def on_ready():
    """
    on_ready() syncs and updates the slash commands on the Discord server.
    """
    print('on ready')
    await tree.sync()

bot.run(os.environ.get('DISCORD_TOKEN'))
