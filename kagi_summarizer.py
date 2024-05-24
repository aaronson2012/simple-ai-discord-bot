"""
This is all of the code for a discord bot that will summarize the given url
content

invoke with `/summarize`
"""

import os

import discord

import requests

from dotenv import load_dotenv

load_dotenv()

KAGI_TOKEN = os.environ.get("KAGI_TOKEN")

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)


@tree.command(name="summarize", description="Summarizes the given url content")
@discord.app_commands.describe(url="The url to summarize")
async def summarize(ctx, url: str):
    """
    The main bot entrypoint
    """

    channel = ctx.channel

    if url is None:
        await channel.send("Please provide a url to summarize")

    await ctx.response.defer()
    summary = await get_summary(url)

    await ctx.followup.send(summary)


async def get_summary(url):
    """
    Get the summary from Kagi
    """

    base_url = "https://kagi.com/api/v0/summarize"
    params = {"url": {url}, "summary_type": "summary", "engine": "agnes"}
    headers = {"Authorization": f"Bot {KAGI_TOKEN}"}

    try:
        json_response = requests.get(
            base_url, headers=headers, params=params, timeout=60
        ).json()
    
        formatted_response = f"""
[Click here for full article]({url})
{json_response['data']['output'] or json_response['error']['msg']}
        """
    
        return formatted_response
    except requests.exceptions.Timeout:
        return "Kagi response took too long..."


# Sync slash command to Discord.
@bot.event
async def on_ready():
    """
    on_ready() syncs and updates the slash commands on the Discord server.
    """
    await tree.sync()


bot.run(os.environ.get("DISCORD_TOKEN"))
