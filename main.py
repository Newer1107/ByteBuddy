import discord
import os
import subprocess
from discord.ext import commands
current_directory = '/home/'
# Define your desired intents
intents = discord.Intents.all()
CHANNEL_ID = ADD-CHANNEL-ID-HERE
# Create a new bot instance with the intents argument
bot = commands.Bot(command_prefix='!', intents=intents)
# Event: When the bot is ready and connected to Discord
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

# Command: Ping-Pong
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

# Command: Say Hello
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.name}!')
@bot.event
async def on_message(message):
    global current_directory  # Access the global current_directory variable

    if message.channel.id == CHANNEL_ID and not message.author.bot:
        command = message.content.strip()

        if command == 'clear':
            await clear_channel_messages(message.channel)
        else:
            output = execute_command(command)
            await message.channel.send(f'Command: `{command}`\nOutput:\n```\n{output}\n```')

async def clear_channel_messages(channel):
    await channel.purge(limit=None)

def execute_command(command):
    global current_directory  # Access the global current_directory variable

    try:
        if command.startswith('cd'):
            directory = command.split(maxsplit=1)[1]
            new_directory = os.path.abspath(os.path.join(current_directory, directory))
            if os.path.exists(new_directory) and os.path.isdir(new_directory):
                current_directory = new_directory
                return f'Changed directory to: {current_directory}'
            else:
                return f'Directory not found: {new_directory}'
        else:
            result = subprocess.run(['fish', '-c', f'cd {current_directory}; {command}'], capture_output=True, text=True, check=True)
            return result.stdout
    except subprocess.CalledProcessError as e:
        return f'Command failed with exit code {e.returncode}.\nError: {e.stderr}'


# Run the bot using your bot token
bot.run('BOT-TOKEN')

