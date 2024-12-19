# Twitch Chatbot (Python)

A Twitch chatbot using TwitchIO that can read chat messages and respond.

## Setup Instructions

1. Install Python 3.7+ if you haven't already (https://python.org)
2. Clone this repository
3. Install ollama (https://ollama.ai/docs/install)
4. Pull llama3.1-8b model (ollama pull llama3.1-8b)
5. Create a file called emote_names.txt in the commands folder where each line is an emote your bot can use through 7tv or bttv.
The program will use this for it's emote command.
6. Create a .env file with the following variables:
   - BOT_USERNAME: Your bot's username
   - BOT_OAUTH_TOKEN: Your bot's OAuth token (get it from Twitch Developer Dashboard)
   - CHANNEL_NAME: The channel you want the bot to join 
   - OLLAMA_PATH: The path to your ollama installation
7. Run the bot using one of the following methods:
 
   - Local development (using venv)
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   python bot.py

   - Production deployment (using Docker)
   docker build -t twitch-bot .
   docker run --env-file .env twitch-bot


The bot will connect to the specified channel

## Features
- Reads chat messages
- Responds to "!hello" command with "Hello!"
- Ignores its own messages to prevent loops
- Uses modern async/await syntax with TwitchIO
- Environment variable configuration for secure token management
- Uses ollama (llama3.3) for AI responses
