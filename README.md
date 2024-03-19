# Discord Shell Bot

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
    OWNER_ID=<your Discord ID>
    CHANNEL_ID=<your channel ID>
    LOG_FILE_LOCATION=<path to the log file>
    ```
    - Replace `<your bot token>` with the token of your Discord bot.
    - Replace `<your Discord ID>` with your own Discord ID (to make sure only you can execute console commands).
    - Replace `<your channel ID>` with the ID of the Discord channel where you want the bot to operate.
    - Replace `<path to the log file>` with the desired location for the log file. For example: `/home/logs.txt`.

### Step 6: Customize the starting directory (optional)
- If you want to change the starting directory for the bot's file system navigation, modify the `current_directory` variable in the code to the desired directory path.

### Step 7: Add an optional thumbnail image (optional)
- You have the option to add a thumbnail image to the embedded system information message. To do this, follow the steps below:
    1. Prepare an image file (e.g., `arch.png`) that you want to use as the thumbnail.
    2. Copy the image file to the `termtodiscord` directory.
    3. Open `bot.py` in a text editor.
    4. Find the line `arch_logo = File("ADD-IMAGE-PATH-HERE")`.
    5. Replace `"ADD-IMAGE-PATH-HERE"` with the actual path to the image file. For example: `arch_logo = File("arch.png")`.

### Step 8: Setting up the bot
1. Visit the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click on the "New Application" button.
3. Enter a name for your application (this will be the name of your bot).
4. Click the "Create" button.
5. In the application dashboard, navigate to the "Bot" tab on the left sidebar.
6. Click on the "Add Bot" button.
7. A confirmation prompt will appear. Click "Yes, do it!" to proceed.
8. Customize your bot's display name and profile picture by adjusting the "Username" and "Avatar" settings under the "Bot" tab.
9. Toggle the "Public Bot" switch if you want your bot to be available publicly.
10. Enable the necessary bot permissions under the "Bot Permissions" section. These permissions define what your bot can do on Discord servers.
11. Scroll down and click the "Save Changes" button.
12. Under the "Token" section, click the "Copy" button to copy the bot token. This token is a secret key that identifies your bot to Discord.
13. **Important:** Treat the bot token as sensitive information and keep it private. Do not share it publicly or include it in your code repository.
14. Navigate to the "OAuth2" tab on the left sidebar.
15. In the "Scopes" section, select the necessary bot permissions based on your bot's functionality.
16. Copy the generated OAuth2 URL.
17. Open a new browser tab and paste the URL.
18. Choose the server where you want to invite the bot and follow the prompts to complete the invitation process.

### Step 9: Run the bot
1. Start the bot by running the following command:

    ```
    python bot.py
    ```

### Step 10: Interact with the bot
1. In the designated text channel (specified by `CHANNEL_ID` in the `.env` file), type commands to interact with the bot.
2. Use the `ping` command to check if the bot is responding. Example: `!ping`
3. Use the `hello` command to receive a greeting from the bot. Example: `!hello`
4. Execute shell commands directly by typing them in the channel. Only the bot owner, specified by `OWNER_ID` in the `.env` file, can execute console commands.
5. The bot will execute the command, capture the output, and display it in a formatted message.
6. Use the `cd` command followed by a directory path to navigate the file system. Example: `cd /home/user/Downloads`

### Additional Information
- To ensure security and prevent exposing sensitive information, make sure to keep the `.env` file private and exclude it from version control (if any).
- Feel free to modify and customize the code according
