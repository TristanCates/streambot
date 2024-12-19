from commands.internal_commands import InternalCommands
import asyncio
import signal
import sys

class InternalBot:
    def __init__(self):
        print("Internal Bot initialized")
        self.commands = InternalCommands()
        self.is_running = False

    async def process_command(self, text: str):
        # Convert input to lowercase for case-insensitive matching
        text_lower = text.lower() 

      #refer to commands/internal_commands.py for more information on the commands and their functionality
        if text_lower.startswith('!swan'):
            if text_lower == '!swancommands':
                response = await self.commands.swancommands_command()
            else:
                response = await self.commands.swan_command(prompt=text[5:].strip())
            print(response)
            
        elif text_lower.startswith('!f '):
            response = await self.commands.f_command(prompt=text[3:].strip())
            print(response)
        elif text_lower.startswith('!w '):
            response = await self.commands.w_command(prompt=text[3:].strip())
            print(response)
        elif text_lower.startswith('!e '):
            response = await self.commands.e_command(prompt=text[3:].strip())
            print(response)
        elif text_lower.startswith('!t '):
            response = await self.commands.t_command(prompt=text[3:].strip())
            print(response)
        elif text_lower.startswith('!lol '):
            response = await self.commands.lol_command(prompt=text[5:].strip())
            print(response)
        elif text_lower.startswith('!hello '):
            response = await self.commands.hello_command()
            print(response)
        # Invalid commands are silently ignored

    async def run(self):
        self.is_running = True
        print("Bot is ready! Press Ctrl+C to quit")
        print("Available commands: !swan <question>, !f <complaint>, !w <celebration>, !e <prompt>, !t <prompt>, !lol <prompt>")
        
        try:
            while self.is_running:
                try:
                    user_input = input("\nEnter a command: ")
                    await self.process_command(user_input)
                except EOFError:  # Handles Ctrl+D
                    self.is_running = False
                    print("\nGoodbye!")
        except Exception as e:
            print(f"\nAn error occurred: {e}")

    def stop(self):
        self.is_running = False

if __name__ == "__main__":
    bot = InternalBot()
    
    # Set up signal handler for graceful shutdown
    def signal_handler(sig, frame):
        print("\nShutting down gracefully...")
        bot.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler) #handles ctrl+c
    signal.signal(signal.SIGTERM, signal_handler) #handles ctrl+d
    
    asyncio.run(bot.run()) #runs the bot