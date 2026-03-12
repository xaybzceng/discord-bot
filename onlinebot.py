import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import os

TOKEN = os.getenv("TOKEN")

# ---------- INTENTS ----------
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    member_cache_flags=discord.MemberCacheFlags.all()
)

# ---------- WEB SERVER (กันบอทหลับ) ----------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run():
    app.run(host="0.0.0.0", port=10000)

def keep_alive():
    server = Thread(target=run)
    server.start()

# ---------- BOT READY ----------
@bot.event
async def on_ready():
    print(f"🤖 Bot online: {bot.user}")

# ---------- WELCOME SYSTEM ----------
@bot.event
async def on_member_join(member):

    channel = bot.get_channel(1481213640354037772)

    embed = discord.Embed(
        title="🎉 ยินดีต้อนรับสู่เซิร์ฟเวอร์!",
        description=f"สวัสดี {member.mention} 👋\n"
                    f"ยินดีต้อนรับเข้าสู่ **{member.guild.name}**",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="👥 สมาชิกคนที่",
        value=f"{member.guild.member_count}",
        inline=False
    )

    embed.add_field(
        name="📜 กฎเซิร์ฟเวอร์",
        value="กรุณาอ่านกฎก่อนใช้งานนะครับ",
        inline=False
    )

    embed.set_thumbnail(url=member.display_avatar.url)

    embed.set_image(
        url="https://media.giphy.com/media/OkJat1YNdoD3W/giphy.gif"
    )

    embed.set_footer(text=f"User ID: {member.id}")

    await channel.send(embed=embed)

# ---------- RUN ----------
keep_alive()
bot.run(TOKEN)
