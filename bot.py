import os
from dotenv import load_dotenv, find_dotenv
from twitchio.ext import commands
from commands.basic_commands import BasicCommands

# Load environment variables
load_dotenv(find_dotenv())

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=os.environ['BOT_OAUTH_TOKEN'],
            prefix='!',
            initial_channels=[os.environ['CHANNEL_NAME']]
        )
        # Load commands
        self.add_cog(BasicCommands(self))

    async def event_ready(self):
        """Called once when the bot goes online."""
        print(f"Bot is ready! | {self.nick}")

    async def event_message(self, message):
        """Called every time a message is sent in chat."""
        # Ignore messages from the bot itself
        if message.echo:
            return

        # Handle commands, see commands/basic_commands.py for more examples
        await self.handle_commands(message)

if __name__ == "__main__":
    bot = Bot()
    bot.run() 