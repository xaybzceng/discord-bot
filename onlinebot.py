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

bot = commands.Bot(command_prefix="!", intents=intents)

# -------- WEB SERVER --------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run():
    app.run(host="0.0.0.0", port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# -------- กันส่งซ้ำ --------
welcomed_users = set()

# -------- BOT READY --------
@bot.event
async def on_ready():
    print(f"🤖 Bot online: {bot.user}")

# -------- WELCOME --------
@bot.event
async def on_member_join(member):

    # กันส่งซ้ำ
    if member.id in welcomed_users:
        return

    welcomed_users.add(member.id)

    channel = bot.get_channel(1481213640354037772)

    embed = discord.Embed(
        title="🎉 ยินดีต้อนรับเข้าสู่เซิร์ฟเวอร์!",
        description=f"ฮัลโหล {member.mention} 👋\nยินดีต้อนรับเข้าสู่ **{member.guild.name}**",
        color=discord.Color.green()
    )

    embed.add_field(
        name="👥 สมาชิกคนที่",
        value=member.guild.member_count,
        inline=False
    )

    embed.set_thumbnail(url=member.display_avatar.url)

    embed.set_image(
        url="https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif"
    )

    embed.set_footer(text=f"User ID: {member.id}")

    await channel.send(embed=embed)

# -------- RUN --------
keep_alive()
bot.run(TOKEN)
