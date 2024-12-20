import os
import ollama
from dotenv import load_dotenv, find_dotenv
from twitchio.ext import commands
from commands.internal_commands import InternalCommands

# Load environment variables
load_dotenv(find_dotenv())

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=os.environ['BOT_OAUTH_TOKEN'],
            prefix='!',
            initial_channels=[os.environ['CHANNEL_NAME']],
            case_sensitive=False
        )
        self.internal = InternalCommands()
        # Add message history storage
        self.messages = []
        self.USER = "user"
        self.ASSISTANT = "assistant"

    async def event_ready(self):
        """Called once when the bot goes online."""
        print(f"Bot is ready! | {self.nick}")

    async def event_message(self, message):
        """Called every time a message is sent in chat."""
        if message.echo:
            return
        
        # Handle commands
        message.content = message.content.lower()
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx):
        response = await self.internal.hello_command()
        await ctx.send(response)

    @commands.command(name='e')
    async def e_command(self, ctx):
        prompt = ctx.message.content[3:].encode('ascii', 'ignore').decode().strip()
        response = await self.internal.e_command(prompt=prompt)
        await ctx.send(response)

    @commands.command()
    async def swan(self, ctx):
        prompt = ctx.message.content[6:].encode('ascii', 'ignore').decode().strip()
        response = await self.internal.swan_command(prompt=prompt)
        await ctx.send(response)

    @commands.command(name='f')
    async def f_command(self, ctx):
        prompt = ctx.message.content[3:].encode('ascii', 'ignore').decode().strip()
        response = await self.internal.f_command(prompt=prompt)
        await ctx.send(response)

    @commands.command(name='w')
    async def w_command(self, ctx):
        prompt = ctx.message.content[3:].encode('ascii', 'ignore').decode().strip()
        response = await self.internal.w_command(prompt=prompt)
        await ctx.send(response)

    @commands.command(name='t')
    async def t_command(self, ctx):
        prompt = ctx.message.content[3:].encode('ascii', 'ignore').decode().strip()
        response = await self.internal.t_command(prompt=prompt)
        await ctx.send(response)

    @commands.command(name='lol')
    async def lol_command(self, ctx):
        prompt = ctx.message.content[5:].encode('ascii', 'ignore').decode().strip()
        response = await self.internal.lol_command(prompt=prompt)
        await ctx.send(response)

    @commands.command(name='swancommands')
    async def swancommands(self, ctx):
        response = await self.internal.swancommands_command()
        await ctx.send(response)

if __name__ == "__main__":
    bot = Bot()
    bot.run() 