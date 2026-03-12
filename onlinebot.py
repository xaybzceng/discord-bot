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
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# -------- WEB SERVER (กันบอทหลับ) --------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run():
    app.run(host="0.0.0.0", port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# -------- เก็บห้องต้อนรับ --------
welcome_channels = {}

# -------- กันส่งซ้ำ --------
welcomed_users = set()

# -------- BOT READY --------
@bot.event
async def on_ready():
    print(f"🤖 Bot online: {bot.user}")

# -------- ตั้งค่าห้องต้อนรับ --------
@bot.command()
async def setwelcome(ctx):

    if ctx.author.id != ctx.guild.owner_id:
        await ctx.send("❌ คำสั่งนี้ใช้ได้เฉพาะเจ้าของเซิร์ฟเวอร์เท่านั้น")
        return

    welcome_channels[ctx.guild.id] = ctx.channel.id

    await ctx.send("✅ ตั้งค่าห้องต้อนรับเรียบร้อยแล้ว")

# -------- WELCOME --------
@bot.event
async def on_member_join(member):

    if member.id in welcomed_users:
        return

    welcomed_users.add(member.id)

    channel_id = welcome_channels.get(member.guild.id)

    if channel_id is None:
        return

    channel = bot.get_channel(channel_id)

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
