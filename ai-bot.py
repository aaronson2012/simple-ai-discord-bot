import os
import discord
from dotenv import load_dotenv
import aiohttp

load_dotenv()

OPENAI_API_URL = os.environ.get("OPENAI_API_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
AI_MODEL = os.environ.get("AI_MODEL")

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
    Get the response from OpenAI
    """
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": {AI_MODEL},  # Specify your desired model
        "messages": [{"role": "user", "content": prompt}]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(OPENAI_API_URL, headers=headers, json=data) as response:
            if response.status == 200:
                json_response = await response.json()
                return json_response['choices'][0]['message']['content']
            else:
                return f"Error: {response.status} - {await response.text()}"

# Sync slash command to Discord.
@bot.event
async def on_ready():
    """
    on_ready() syncs and updates the slash commands on the Discord server.
    """
    await tree.sync()

bot.run(os.environ.get("DISCORD_TOKEN"))
