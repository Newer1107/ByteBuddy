import discord
import os
import sys
from dotenv import load_dotenv
from discord.ext import commands, tasks
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
LOG_FILE = os.getenv('LOG_FILE_LOCATION')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Bot has been restarted.")
    script_name = "main.py"
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), script_name))
    python = sys.executable
    os.execv(python, [python, script_path])
    await bot.close()
bot.run(BOT_TOKEN)
