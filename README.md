# Twitch Chatbot 

A Twitch chatbot that uses the Ollama LLM to read and respond to chat messages. 
This bot includes functionality to control a user's web browser, and their OBS recording software
in order to seamlessly share media on stream with a single mod-only command in Twitch chat.

## Instructions and Ollama Setup

1. Install Python 3.7+ if you haven't already (https://python.org)
2. Clone this repository
3. Install ollama (https://ollama.ai/docs/install)
4. Pull llama3.1-8b model (ollama pull llama3.1-8b)
5. Create a file called emote_names.txt in the commands folder where each line the word of an emote your bot can use through 7tv or bttv.
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

OBS/Browser Interaction:
1. Selenium requires a driver to interface with the chosen browser. Make sure the driver is in your PATH, e. g., place it in /usr/bin or /usr/local/bin.
If you're using Chrome, you'll need to download the ChromeDriver executable and ensure it's in your PATH.
2. Have a source in OBS called "ChatLink", and enable this source to have the transitions you'd like 
(such as fade in 1000ms). Right click the source, and select "Show Transitions" and "Hide Transitions" to pick
each type of transition. When this program enables this sources' visibility, it will use the transitions you've set up.
3. Launch Chrome with the following command in your terminal or command prompt in order to use browser extensions
chrome --remote-debugging-port=9222 --user-data-dir="path/to/your/chrome/profile"
4. When launching the bot, with the browser the bot launches,enable any plugins your browser may need, and adjust the youtube and Twitch volume bars to your liking.

## Features
- Reads chat messages
- Responds to "!hello" command with "Hello!"
- Ignores its own messages to prevent loops
- Uses modern async/await syntax with TwitchIO
- Environment variable configuration for secure token management
- Uses ollama (llama3.1) for AI responses

