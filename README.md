# Discord Shell Bot (ONLY For Linux)

## Overview
This project implements a Discord bot using Python and the `discord.py` library. The bot acts as a command execution and shell interaction tool within a designated Discord text channel. Users can execute commands, navigate the file system, and receive command output directly in the Discord channel.

## Installation and Usage (For Linux)
Follow the steps below to install and run the Discord Shell Bot on Linux:

### Prerequisites
- Python and pip should be installed on your Linux system.
- Git should be installed to clone the repository.

### Step 1: Clone the repository
1. Open your terminal and navigate to the directory where you want to clone the repository.
2. Run the following command to clone the repository:
   
    ```
    git clone https://github.com/Newer1107/termtodiscord
    ```

### Step 2: Set up the environment
1. Navigate to the cloned repository:
   
    ```
    cd termtodiscord
    ```
2. Create a new virtual environment using the following command:
   
    ```
    python -m venv .
    ```

### Step 3: Activate the virtual environment
- Activate the virtual environment by running the following command:
  
    ```
    source bin/activate
    ```

### Step 4: Install dependencies
1. Install the required dependencies by running the following command:
   
    ```
    pip install -r requirements.txt
    ```

### Step 5: Configure the bot
1. Rename the `.env.example` file to `.env`:
   
    ```
    mv .env.example .env
    ```
3. Open the `.env` file and update the following lines:
   
    ```
    BOT_TOKEN=<your bot token>
    CHANNEL_ID=<your channel ID>
    LOG_FILE_LOCATION=<path to the log file>
    ```
    - Replace `<your bot token>` with the token of your Discord bot.
    - Replace `<your channel ID>` with the ID of the Discord channel where you want the bot to operate.
    - Replace `<path to the log file>` with the desired location for the log file. For example: `/home/logs.txt`.

### Step 6: Customize the starting directory (optional)
- If you want to change the starting directory for the bot's file system navigation, modify the `current_directory` variable in the code to the desired directory path.

### Step 7: Run the bot
1. Start the bot by running the following command:
   
    ```
    python bot.py
    ```

### Step 8: Invite the bot to your Discord server
1. Create a new Discord bot and obtain its token. You can do this through the [Discord Developer Portal](https://discord.com/developers/applications).
2. Invite the bot to your server using the generated OAuth2 URL. Make sure to grant the necessary permissions for the bot to read and send messages in the designated channel.

### Step 9: Interact with the bot
1. In the designated text channel (specified by `CHANNEL_ID` in the `.env` file), type commands to interact with the bot.
2. Use the `ping` command to check if the bot is responding. Example: `!ping`
3. Use the `hello` command to receive a greeting from the bot. Example: `!hello`
4. Execute shell commands directly by typing them in the channel. Example: `cowsay hello`
5. The bot will execute the command, capture the output, and display it in a formatted message.
6. Use the `cd` command followed by a directory path to navigate the file system. Example: `cd /home/Downloads`

### Additional Information
- To ensure security and prevent exposing sensitive information, make sure to keep the `.env` file private and exclude it from version control (if any).
- Feel free to modify and customize the code according to your specific requirements.

## Dependencies
- Linux
- Python
- Libraries in `requirements.txt`

Please note that this documentation is specifically for Linux users and assumes familiarity with Linux environments, Python, Discord bots, and command-line interfaces.
