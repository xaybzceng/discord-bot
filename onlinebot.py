import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# -------- Flask --------
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# -------- Bot Ready --------
@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

# -------- Welcome System --------
@bot.event
async def on_member_join(member):

    channel = bot.get_channel(1481213640354037772)

    embed = discord.Embed(
        title="🎉 ยินดีต้อนรับ!",
        description=f"สวัสดี {member.mention} 👋\nยินดีต้อนรับเข้าสู่เซิร์ฟเวอร์",
        color=0x00ffcc
    )

    embed.add_field(
        name="👥 สมาชิกคนที่",
        value=member.guild.member_count
    )

    embed.set_thumbnail(url=member.avatar.url)

    await channel.send(embed=embed)

keep_alive()
bot.run(TOKEN)
