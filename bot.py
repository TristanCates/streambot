import os
import ollama
import asyncio
import signal
from dotenv import load_dotenv, find_dotenv
from twitchio.ext import commands
from commands.internal_commands import InternalCommands
from commands.obsCommands import obsCommands

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
        self.obs = obsCommands(self)
        self.messages = []
        self.USER = "user"
        self.ASSISTANT = "assistant"

    async def shutdown(self):
        print("Shutting down bot...")
        await self.obs.shutdown()
        print("Bot shutdown complete.")

    async def event_ready(self):
        """Called once when the bot goes online. Initialized OBS connection"""
        print("Bot is ready!")
        await self.obs.event_ready()

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

    @commands.command()
    async def e(self, ctx):
        prompt = ctx.message.content[3:].encode('ascii', 'ignore').decode().strip()
        response = await self.internal.e_command(prompt=prompt)
        await ctx.send(response)

    @commands.command()
    async def swan(self, ctx):
        prompt = ctx.message.content[6:].encode('ascii', 'ignore').decode().strip()
        response = await self.internal.swan_command(prompt=prompt)
        await ctx.send(response)

    @commands.command()
    async def f(self, ctx):
        prompt = ctx.message.content[3:].encode('ascii', 'ignore').decode().strip()
        response = await self.internal.f_command(prompt=prompt)
        await ctx.send(response)

    @commands.command()
    async def w(self, ctx):
        prompt = ctx.message.content[3:].encode('ascii', 'ignore').decode().strip()
        response = await self.internal.w_command(prompt=prompt)
        await ctx.send(response)

    @commands.command()
    async def t(self, ctx):
        prompt = ctx.message.content[3:].encode('ascii', 'ignore').decode().strip()
        response = await self.internal.t_command(prompt=prompt)
        await ctx.send(response)

    @commands.command()
    async def lol(self, ctx):
        prompt = ctx.message.content[5:].encode('ascii', 'ignore').decode().strip()
        response = await self.internal.lol_command(prompt=prompt)
        await ctx.send(response)

    @commands.command()
    async def swancommands(self, ctx):
        response = await self.internal.swancommands_command()
        await ctx.send(response)

async def main():
    bot = Bot()
    try:
        await bot.start()
    except KeyboardInterrupt:
        print("Received exit signal, shutting down...")
    except asyncio.CancelledError:
        print("Task was cancelled, shutting down...")
    finally:
        await bot.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program terminated by user.") 