from twitchio.ext import commands

# Cog class (TwitchIO's way of organizing commands)
class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
   
    #Command decorator (TwitchIO's way of marking a function as a command)
    @commands.command()
    async def hello(self, ctx):
        """Responds with 'Hello!' when someone uses the !hello command"""
        #await ctx.send('Hello!') 
        print('Hello!')

    @bot.command(name='swan')
    async def swan_command(ctx: commands.Context):
        # Get the prompt by removing "!swan " from the message
        prompt = ctx.message.content[6:].strip()
        
        if not prompt:
            # await ctx.send("Please provide a question after !swan")
            print("Please provide a question after !swan")
            return
        
        try:
            # Call Ollama API with the prompt
            response = ollama.chat(model='llama2', messages=[
                {
                    'role': 'user',
                    'content': prompt,
                }
            ])
            
            # Get the response content and limit to 500 characters
            response_text = response['message']['content'][:500]
            
            # await ctx.send(response_text)
            print(response_text)
            
        except Exception as e:
            # await ctx.send(f"Sorry, there was an error processing your request: {str(e)}")
            print(f"Sorry, there was an error processing your request: {str(e)}")