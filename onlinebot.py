import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import os

TOKEN = os.getenv("TOKEN")  # ใส่ TOKEN ใน Render

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# -------- Flask ทำให้บอทไม่หลับ --------
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# -------- บอทออนไลน์ --------
@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

# -------- ระบบต้อนรับ --------
@bot.event
async def on_member_join(member):

    channel = bot.get_channel(1481594709720698962)  # ใส่ ID ช่อง

    embed = discord.Embed(
        title="🎉 ยินดีต้อนรับ!",
        description=f"สวัสดี {member.mention} 👋\nยินดีต้อนรับสู่เซิร์ฟเวอร์!",
        color=0x00ffcc
    )

    embed.add_field(
        name="👥 สมาชิกคนที่",
        value=member.guild.member_count
    )

    embed.set_thumbnail(url=member.avatar.url)

    await channel.send(embed=embed)

# -------- รันบอท --------
keep_alive()
bot.run(TOKEN)
