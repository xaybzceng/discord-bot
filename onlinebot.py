import os
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

VOICE_CHANNEL_ID = 1481939207478972510

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Bot Online")

    channel = bot.get_channel(VOICE_CHANNEL_ID)

    if channel:
        await channel.connect()

bot.run(TOKEN)
