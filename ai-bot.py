"""
This is all of the code for a discord bot that will interface with the AI chatbot.

invoke with `/ai`
"""

import os

import discord
from dotenv import load_dotenv
from litellm import Chat

load_dotenv()

# Initialize the Litellm Chat instance
chat = Chat()

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

@tree.command(name="ai", description="Get a response from the AI")
@discord.app_commands.describe(prompt="The prompt for the AI")
async def ai(ctx, prompt: str):
    """
    The main bot entrypoint
    """

    channel = ctx.channel

    if not prompt:
        await channel.send("Please provide a prompt.")
        return

    await ctx.response.defer()
    response = await get_response(prompt)

    await ctx.followup.send(response)

async def get_response(prompt):
    """
    Get the response from Litellm
    """
    
    try:
        # Using Litellm to generate the response
        response = await chat.generate(prompt)
        return response
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Sync slash command to Discord.
@bot.event
async def on_ready():
    """
    on_ready() syncs and updates the slash commands on the Discord server.
    """
    await tree.sync()

bot.run(os.environ.get("DISCORD_TOKEN"))
