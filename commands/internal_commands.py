import ollama
import random
from dotenv import load_dotenv
import os
from typing import Optional, Callable, Any
from commands.commandfunctions import handle_command_errors, requires_prompt

class InternalCommands:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        # Add Ollama to PATH
        ollama_path = os.getenv('OLLAMA_PATH')
        if ollama_path and ollama_path not in os.environ['PATH']:
            os.environ['PATH'] = ollama_path + os.pathsep + os.environ['PATH']
        
        # Configure ollama client
        ollama.Client.base_url = "http://localhost:11434"
        
        # Load emotes
        self.emote_string = self._load_emotes()
        self.emote_list = self.emote_string.split()

    def _load_emotes(self) -> str:
        """Load emotes from file and return as space-separated string."""
        try:
            with open('emote_names.txt', 'r') as f:
                emotes = f.read().strip().split()
                return ' '.join(emotes)
        except FileNotFoundError:
            return ""

    async def _ask_ollama(self, prompt: str, system_message: str) -> str:
        """Helper method to handle Ollama API calls."""
        response = ollama.chat(model='llama3.1', messages=[
            {
                'role': 'system',
                'content': system_message
            },
            {
                'role': 'user',
                'content': prompt,
            }
        ])
        return response['message']['content'][:500]

    @handle_command_errors #decorator to handle common command error patterns (see commandfunctions.py)
    @requires_prompt #decorator to mark commands that require a prompt (see commandfunctions.py)    
    async def swan_command(self, prompt: str) -> str:
        """Handle the !swan command for asking questions."""
        system_message = f'''You are a helpful human scholar that provides concise but thorough answers. 
        Focus on the most important information, and respond with 1 or 2 sentences, using 10 words or fewer per sentence. 
        Always replace two to four words in your response
        with random words from the list of words: {self.emote_string}, and do not use punctuation.
        '''
        return await self._ask_ollama(prompt, system_message) + " " + random.choice(self.emote_list)

    @handle_command_errors
    @requires_prompt
    async def f_command(self, prompt: str) -> str:
        """Handle the !f command for complaints."""
        system_message = f'''You are a perpetually distraught human that responds with intense 
        and dramatic lamentations. Be funny and over-the-top in your frustration, 
        and poke fun at the prompt.
        Respond with 1 or 2 sentences, using 10 words or fewer per sentence.
        Do not include quotes in your response.
      '''
        complaint_prompt = f"Ugh, can you believe this? {prompt}"
        return await self._ask_ollama(complaint_prompt, system_message) + " " + random.choice(self.emote_list)

    @handle_command_errors
    async def hello_command(self) -> str:
        """Handle the !hello command."""
        return "Hello! 👋" + random.choice(self.emote_list)

    @handle_command_errors
    @requires_prompt
    async def w_command(self, prompt: str) -> str:
        """Handle the !w command for celebrations."""
        system_message = f'''You are an incredibly enthusiastic hype man that motivates people in a positive way.
        Make everything sound like the most amazing thing ever.
        Keep responses fun and uplifting.
        Match and amplify any excitement in the prompt.
        Respond with 1 or 2 sentences, using 10 words or fewer per sentence.'''
        celebration_prompt = f"OMG, {prompt}!"
        return await self._ask_ollama(celebration_prompt, system_message) + " " + random.choice(self.emote_list)

    @handle_command_errors
    @requires_prompt
    async def t_command(self, prompt: str) -> str:
        """Handle the !t command for random trivia."""
        system_message = f'''You are a knowledgeable human sharing fascinating trivia and little-known facts.
        Focus on surprising, interesting, or unusual information.
        Keep it fun and engaging while being accurate.
        Respond with 1 or 2 sentences, using 10 words or fewer per sentence.'''
        return await self._ask_ollama(prompt, system_message) + " " + random.choice(self.emote_list)

    @handle_command_errors
    @requires_prompt
    async def lol_command(self, prompt: str) -> str:
        """Handle the !lol command for laughing at prompts."""
        system_message = f'''You are a human who finds everything absolutely hilarious.
        Point out something specifically funny about the prompt. 
        Use lots of "LMAO", "LOL", or similar expressions. Be a little crazy and over the top.
        Respond with 1 or 2 sentences, using 10 words or fewer per sentence.'''
        return await self._ask_ollama(prompt, system_message) + " " + random.choice(self.emote_list)

    @handle_command_errors
    @requires_prompt
    async def e_command(self, prompt: str) -> str:
        """Handle the !7tv command for 7TV emote-only responses."""
        system_message = f'''You are an AI that communicates exclusively using a specific list of words.
Never use words, emojis, or any special characters - only these words, unaltered: {self.emote_string} 
Try to make a coherent point with only these words. Use exactly 10 words. Make sure to keep the exact capitalization of the words given.
Try to have the words make logical sense when read left to right. Do not use any punctuation.
'''
        return await self._ask_ollama(prompt, system_message)

    @handle_command_errors
    async def swancommands_command(self) -> str:
        """Handle the !swancommands command to list all available commands."""
        commands = '''
!swan <prompt> - Ask me anything, 
!f <prompt>, 
!w <prompt>, 
!e <prompt>, 
!t <prompt>, 
!lol <prompt>
'''
        return commands

    @handle_command_errors
    async def handle_invalid_command(self, command: str) -> Optional[str]:
        """Handle any invalid/unknown commands by doing nothing."""
        return None