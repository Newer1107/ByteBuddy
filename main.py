import discord
import os
import subprocess
import datetime
import psutil
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
LOG_FILE = os.getenv('LOG_FILE_LOCATION')
current_directory = '/home/'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Successfully Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
    update_uptime.start()
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.name}!')

@bot.command()
async def uptime(ctx):
    uptime = get_system_uptime()
    await ctx.send(f'Hello {ctx.author.name}, your server uptime is `{uptime}`!')
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.CommandInvokeError):
        original_error = error.original
        if isinstance(original_error, discord.errors.HTTPException):
            if "Invalid Form Body" in str(original_error):
                await ctx.send("Command output is too long to display.")
                return

        raise error

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
    elif message.channel.id == CHANNEL_ID:
        command = message.content.strip()
        output = execute_command(command)
        output_message = f'Command: `{command}`\nOutput:\n```\n{output}\n```'
        if len(output_message) > 2000:
            output_message = f'{username} Command: `{command}`\nOutput is too long to display.'
        await message.channel.send(output_message)

        # Log the command and output to a file
        log_entry = f'{datetime.datetime.now()}\n\n Command:\n {command}\nOutput:\n {output}\n\n'
        log_to_file(log_entry)

def execute_command(command):
    global current_directory

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

def log_to_file(log_entry):
    with open(LOG_FILE, 'a') as file:
        file.write(log_entry)
@tasks.loop(minutes=5)  # Update every 5 minutes, adjust the interval as needed
async def update_uptime():
    uptime = get_system_uptime()
    activity = discord.Activity(type=discord.ActivityType.watching, name=f"Uptime: {uptime}")
    await bot.change_presence(activity=activity)

def get_system_uptime():
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
    days, hours, minutes, seconds = uptime.days, uptime.seconds // 3600, (uptime.seconds // 60) % 60, uptime.seconds % 60
    return f"{days}d {hours}h {minutes}m {seconds}s"


bot.run(BOT_TOKEN)
