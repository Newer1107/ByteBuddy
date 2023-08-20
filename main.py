import discord
import os
import subprocess
import datetime
import psutil
import random
from discord.ext import commands, tasks
from dotenv import load_dotenv
import sys
from discord import File
import asyncio
import time
import mcstatus
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID'))
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
LOG_FILE = os.getenv('LOG_FILE_LOCATION')

current_directory = '/home/'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
start_time = datetime.datetime.now()

@bot.event
async def on_ready():
    print(f'Successfully Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
    update_uptime.start()

@bot.command()
async def ping(ctx):
    api_ping = round(bot.latency * 1000)
    await ctx.send(f'Bot Response Time: {api_ping}ms')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.name}!')

@bot.command()
async def uptime(ctx):
    system_uptime = get_system_uptime()
    bot_uptime = get_bot_uptime()
    await ctx.send(f'Hello {ctx.author.name}, your server uptime is `{system_uptime}`!\nBot uptime: `{bot_uptime}`')

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
        if message.author.id == OWNER_ID:
            command = message.content.strip()
            output = await execute_command_async(command)
            output_message = f'Command: `{command}`\nOutput:\n```\n{output}\n```'
            if len(output_message) > 2000:
                output_message = f'Command: `{command}`\nOutput is too long to display.'
            await message.channel.send(output_message)

            log_entry = f'{datetime.datetime.now()}\n\nCommand:\n{command}\nOutput:\n{output}\n\n'
            log_to_file(log_entry)
        else:
            await message.channel.send("You are not authorized to execute console commands, if you are the owner, please add your `OWNER_ID` in `.env` file.")

async def execute_command_async(command):
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
            process = await asyncio.create_subprocess_shell(f'cd {current_directory}; {command}', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await process.communicate()
            return stdout.decode()
    except Exception as e:
        return f'Command failed with error: {str(e)}'

def log_to_file(log_entry):
    with open(LOG_FILE, 'a') as file:
        file.write(log_entry)

@bot.command()
async def restart(ctx):
    await ctx.send("Restarting bot...")
    script_name = "restart_bot.py"
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), script_name))
    python = sys.executable
    os.execv(python, [python, script_path])

@bot.command()
async def sysinfo(ctx):
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    system_uptime = get_system_uptime()
    bot_uptime = get_bot_uptime()
    ram_usage = f"{memory.used / (1024**3):.2f} GB out of {memory.total / (1024**3):.2f} GB"
    disk_usage = psutil.disk_usage('/')
    disk_usage_str = f"{disk_usage.used / (1024**3):.2f} GB out of {disk_usage.total / (1024**3):.2f} GB"
    network = psutil.net_io_counters()
    network_sent = network.bytes_sent / (1024**3)
    network_received = network.bytes_recv / (1024**3)

    embed = discord.Embed(title="System Information", color=discord.Color.blue())
    arch_logo = File("/home/raunak/thebot/arch.png")
    embed.set_thumbnail(url="attachment://arch.png")

    embed.add_field(name="CPU Usage", value=f"**{cpu_percent}%**", inline=False)
    embed.add_field(name="RAM Usage", value=f"**{ram_usage}** | *{memory.percent}%*", inline=False)
    embed.add_field(name="Disk Usage", value=f"**{disk_usage_str}** | *{disk_usage.percent}%*", inline=False)
    embed.add_field(name="Network Usage", value=f"Received: **{network_received:.2f} GB** | Sent: **{network_sent:.2f} GB**", inline=False)
    embed.add_field(name="Uptime", value=f"System: **{system_uptime}** | Bot: **{bot_uptime}**", inline=False)
    embed.set_footer(text="Arch Linux")
    await ctx.send(file=arch_logo, embed=embed)

@bot.command()
async def top(ctx):
    command = "ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%mem | head -n 6"
    output = subprocess.check_output(command, shell=True, universal_newlines=True)
    await ctx.send(f"Top 5 Processes: ```{output}```")

@bot.command()
async def shutdown(ctx):
    if ctx.message.author.id == OWNER_ID:
        await bot.change_presence(status=discord.Status.dnd)
        await ctx.send("Shutting Down the bot...")
        await asyncio.sleep(2)
        await ctx.send("Done")
        await bot.close()

@tasks.loop(seconds=12)
async def update_uptime():
    global last_activity
    last_activity = None

    system_uptime = get_system_uptime()
    bot_uptime = get_bot_uptime()

    activities = [
        discord.Activity(type=discord.ActivityType.watching, name=f"Server Uptime: {system_uptime}"),
        discord.Activity(type=discord.ActivityType.watching, name=f"Bot Uptime: {bot_uptime}")
    ]

    activity = random.choice(activities)

    while activity == last_activity:
        activity = random.choice(activities)

    last_activity = activity

    await bot.change_presence(activity=activity)

def get_system_uptime():
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
    days, hours, minutes, seconds = uptime.days, uptime.seconds // 3600, (uptime.seconds // 60) % 60, uptime.seconds % 60
    return f"{days}d {hours}h {minutes}m {seconds}s"

def get_bot_uptime():
    bot_uptime = datetime.datetime.now() - start_time
    days, hours, minutes, seconds = bot_uptime.days, bot_uptime.seconds // 3600, (bot_uptime.seconds // 60) % 60, bot_uptime.seconds % 60
    return f"{days}d {hours}h {minutes}m {seconds}s"

system_info_messages = {}

@bot.command()
async def start_sysinfo_monitor(ctx):
    if ctx.channel.id not in system_info_messages:
        await ctx.send("Starting system information monitoring...")
        system_info_messages[ctx.channel.id] = await send_initial_sysinfo(ctx)
        bot.loop.create_task(update_system_info(ctx.channel.id))

@bot.command()
async def stop_sysinfo_monitor(ctx):
    if ctx.channel.id in system_info_messages:
        await ctx.send("Stopping system information monitoring...")
        system_info_messages.pop(ctx.channel.id)
    else:
        await ctx.send("System information monitoring is not active in this channel.")

async def update_system_info(channel_id):
    while channel_id in system_info_messages:
        await asyncio.sleep(10)  # Update every 10 seconds

        channel = bot.get_channel(channel_id)
        if channel:
            message_id = system_info_messages[channel_id]
            old_message = await channel.fetch_message(message_id)
            updated_embed = await generate_sysinfo_embed()

            await old_message.edit(embed=updated_embed)


async def send_initial_sysinfo(ctx):
    embed = await generate_sysinfo_embed()
    initial_message = await ctx.send(embed=embed)
    return initial_message.id

async def generate_sysinfo_embed():
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    system_uptime = get_system_uptime()
    bot_uptime = get_bot_uptime()
    ram_usage = f"{memory.used / (1024**3):.2f} GB out of {memory.total / (1024**3):.2f} GB"
    disk_usage = psutil.disk_usage('/')
    disk_usage_str = f"{disk_usage.used / (1024**3):.2f} GB out of {disk_usage.total / (1024**3):.2f} GB"
    network = psutil.net_io_counters()
    network_sent = network.bytes_sent / (1024**3)
    network_received = network.bytes_recv / (1024**3)

    embed = discord.Embed(title="System Information", color=discord.Color.blue())
    embed.set_thumbnail(url="attachment://arch.png")
    event_time = datetime.datetime.now()  # Replace with your event's datetime
    event_unix_timestamp = int(event_time.timestamp())

    footer_text = f"Event time: <t:{event_unix_timestamp}:R>"
    embed.add_field(name="CPU Usage", value=f"**{cpu_percent}%**", inline=False)
    embed.add_field(name="RAM Usage", value=f"**{ram_usage}** | *{memory.percent}%*", inline=False)
    embed.add_field(name="Disk Usage", value=f"**{disk_usage_str}** | *{disk_usage.percent}%*", inline=False)
    embed.add_field(name="Network Usage", value=f"Received: **{network_received:.2f} GB** | Sent: **{network_sent:.2f} GB**", inline=False)
    embed.add_field(name="Uptime", value=f"System: **{system_uptime}** | Bot: **{bot_uptime}**", inline=False)
    embed.set_footer(text="Arch Linux")
    server_ip = "mc.aboutraunak.tk"
    server_port = 13048

    try:
        server = mcstatus.JavaServer.lookup(f"{server_ip}:{server_port}")
        status = server.status()

        players = status.players.online if status.players.sample is not None else 0
        tps = status.latency
        tps_formatted = f"{int(tps)} ms"
        server_online = True
        embed.add_field(name="Server IP", value=f"**{server_ip}:{server_port}**", inline=False)
        embed.add_field(name="Online Players", value=f"**{players}**", inline=False)
        embed.add_field(name="Response Time", value=f"**{tps_formatted}**", inline=False)
        embed.add_field(name="Status", value="**Online**", inline=False)
        embed.add_field(name="Last Updated", value=f"{footer_text}", inline=False)

    except (ConnectionRefusedError, OSError):
        server_online = False
        embed.add_field(name="Server IP", value=f"**{server_ip}:{server_port}**", inline=False)
        embed.add_field(name="Status", value="**Offline**", inline=False)
        embed.add_field(name="Last Updated", value=f"{footer_text}", inline=False)
    return embed


bot.run(BOT_TOKEN)
