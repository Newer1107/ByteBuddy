# Discord Shell Bot

## Overview
This project implements a Discord bot using Python and the `discord.py` library. The bot acts as a command execution and shell interaction tool within a designated Discord text channel. Users can execute commands, navigate the file system, and receive command output directly in the Discord channel.

## Features
- Command Execution: Execute various shell commands by typing in the desired channel.
- Output Display: Capture and format the output of executed commands in code blocks for better readability.
- Change Directory: Use the "cd" command followed by a directory path to navigate the file system.
- Clear Channel Messages: Delete all messages in the Discord channel using the "clear" command.
- Ping-Pong and Greetings: Interact with the bot using the "ping" and "hello" commands.

## Usage
1. Make sure you have python and pip installed.
2. In Linux, install tmux and run `tmux new -s bot`.
3. RUN THESE COMMANDS IN TMUX SESSION:
    ```mkdir myenv
    cd myenv
    python -m venv .
    source bin/activate```
4. do `pip install discord.py`.
5. Invite the bot to your Discord server and ensure it has the necessary permissions.
6. [IMPORTANT] Add BOT_TOKEN and CHANNEL_ID in the file.
2. (OPTIONAL) Set the `current_directory` variable in the code to the desired starting directory.
3. Run the script and provide your bot token.
4. In the designated text channel (specified by `CHANNEL_ID`), type commands to interact with the bot.

## Dependencies
- Python
- `discord.py` library


Feel free to modify and customize the code according to your specific requirements.
