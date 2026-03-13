import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

TOKEN = os.getenv("TOKEN")

VOICE_CHANNEL_ID = 123456789012345678  # ใส่ ID ห้องเสียง

app = Flask('')

@app.route('/')
def home():
    return "Bot is running"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} ออนไลน์แล้ว")

    channel = bot.get_channel(VOICE_CHANNEL_ID)

    if channel:
        await channel.connect()
        print("เข้าห้องเสียงแล้ว")

keep_alive()
bot.run(TOKEN)
