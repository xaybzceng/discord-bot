import discord
from discord.ext import commands

TOKEN = "MTQ4MTI3NTQ1NTYyMDI1NTc5NQ.GGWC1l._4hzJq-S3-w6EBZ22_1MYISEVD-B9vYEwGkh-4"

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot Online: {bot.user}")


bot.run(TOKEN)
