import discord
from discord.ext import commands
from discord import app_commands
from flask import Flask
from threading import Thread
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------- WEB SERVER ----------------

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run():
    app.run(host="0.0.0.0", port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ---------------- DATA ----------------

welcome_channels = {}

gifs = [
"https://media.giphy.com/media/OkJat1YNdoD3W/giphy.gif",
"https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
"https://media.giphy.com/media/ASd0Ukj0y3qMM/giphy.gif"
]

# ---------------- READY ----------------

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"🤖 Bot Online : {bot.user}")

# ---------------- SET WELCOME ----------------

@bot.tree.command(name="setwelcome", description="ตั้งค่าห้องต้อนรับ")
async def setwelcome(interaction: discord.Interaction):

    if interaction.user.id != interaction.guild.owner_id:
        await interaction.response.send_message(
            "❌ คำสั่งนี้ใช้ได้เฉพาะเจ้าของเซิร์ฟเวอร์",
            ephemeral=True
        )
        return

    welcome_channels[interaction.guild.id] = interaction.channel.id

    await interaction.response.send_message(
        "✅ ตั้งค่าห้องต้อนรับเรียบร้อยแล้ว"
    )

# ---------------- MEMBER JOIN ----------------

@bot.event
async def on_member_join(member):

    guild_id = member.guild.id

    if guild_id not in welcome_channels:
        return

    channel = bot.get_channel(welcome_channels[guild_id])

    embed = discord.Embed(
        title="🎉 ยินดีต้อนรับ!",
        description=f"สวัสดี {member.mention} 👋\nยินดีต้อนรับเข้าสู่ **{member.guild.name}**",
        color=discord.Color.green()
    )

    embed.add_field(
        name="👥 สมาชิกคนที่",
        value=member.guild.member_count
    )

    embed.set_thumbnail(url=member.display_avatar.url)

    import random
    embed.set_image(url=random.choice(gifs))

    await channel.send(embed=embed)

# ---------------- RUN ----------------

keep_alive()
bot.run(TOKEN)
