import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import os

TOKEN = os.getenv("TOKEN")

# -------- INTENTS --------
intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# -------- WEB SERVER (กันหลับ) --------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run():
    app.run(host="0.0.0.0", port=10000)

def keep_alive():
    server = Thread(target=run)
    server.start()

# -------- BOT ONLINE --------
@bot.event
async def on_ready():
    print(f"🤖 Bot online: {bot.user}")

# -------- WELCOME --------
@bot.event
async def on_member_join(member):

    channel = bot.get_channel(1481213640354037772)

    embed = discord.Embed(
        title="🎉 ยินดีต้อนรับ!",
        description=f"สวัสดี {member.mention} 👋\nยินดีต้อนรับเข้าสู่ **{member.guild.name}**",
        color=discord.Color.green()
    )

    embed.add_field(
        name="👥 สมาชิกคนที่",
        value=f"{member.guild.member_count}",
        inline=False
    )

    embed.set_thumbnail(url=member.display_avatar.url)

    embed.set_footer(text=f"User ID: {member.id}")

    await channel.send(embed=embed)

# -------- RUN --------
keep_alive()
bot.run(TOKEN)
