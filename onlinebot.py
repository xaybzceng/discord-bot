import discord
from discord.ext import commands

TOKEN = "MTQ4MTI3NTQ1NTYyMDI1NTc5NQ.GkUlKS.d_SmnEGdoy1AcB_mAG9GTrUr9_N2KmNED80sb8"

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot Online: {bot.user}")

bot.run(TOKEN)