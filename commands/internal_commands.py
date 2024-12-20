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

        self.messages = []
        self.USER = "user"
        self.ASSISTANT = "assistant"
        self.model = "llama3.1"  # or your preferred model

    def _load_emotes(self) -> str:
        """Load emotes from file and return as space-separated string."""
        try:
            with open('emote_names.txt', 'r') as f:
                emotes = f.read().strip().split()
                return ' '.join(emotes)
        except FileNotFoundError:
            return ""

    #change this int to determine how many exchanges the bot will keep in memory
    def _get_filtered_history(self, max_messages: int = 20) -> tuple[list, list]:
        """Helper to get system and non-system messages separately."""
        system_messages = []
        history = []
        for msg in self.messages:
            if msg['role'] == 'system':
                system_messages.append(msg)
            else:
                history.append(msg)
        return system_messages, history[-max_messages:]

    def add_history(self, content: str, role: str) -> None:
        """Add a message to the chat history, keeping only the last 5 exchanges"""
        self.messages.append({"role": role, "content": content})
        # Update messages list with filtered history
        system_messages, history = self._get_filtered_history()
        self.messages = system_messages + history

    async def _ask_ollama(self, prompt: str, system_message: str) -> str:
        """Helper method to handle Ollama API calls with chat history."""
        # Get filtered history and create messages list
        system_messages, history = self._get_filtered_history()
        messages = [{"role": "system", "content": system_message}]
        messages.extend(history)
        messages.append({"role": "user", "content": prompt})
        
        # Make API call
        response = ollama.chat(model=self.model, messages=messages)
        complete_message = response['message']['content']
        
         #Store history
        self.add_history(prompt, self.USER)
        self.add_history(complete_message, self.ASSISTANT)
        
        return complete_message[:450]

    def replaceSystemMessage(self, system_message: str) -> None:
        for message in self.messages:
            if message['role'] == 'system':
                message['content'] = system_message
                break

    @handle_command_errors #decorator to handle common command error patterns (see commandfunctions.py)
    @requires_prompt #decorator to mark commands that require a prompt (see commandfunctions.py)    
    async def swan_command(self, prompt: str) -> str:
        """Handle the !swan command for asking questions."""
        system_message = f'''You are an announcer that responds to prompts with a relevant story. 
        Follow these steps EXACTLY:
        1. First, create a brief story relevant to the prompt (1-2 sentences, max 10 words each)
        2. Then, BEFORE returning, replace 2-4 random words with words from this list: {self.emote_string}
        3. The replacement words MUST come from the provided list
        4. Do not add any additional commentary or quotes

        Example:
        Original: "The sun is shining brightly today in the sky"
        Modified: "The KEKW is shining COPIUM today in the POGGERS"
        '''
        return await self._ask_ollama(prompt + ", Tell me something about this.", system_message) + " " + random.choice(self.emote_list)

    @handle_command_errors
    @requires_prompt
    async def f_command(self, prompt: str) -> str:
        """Handle the !f command for complaints."""
        system_message = f'''You are a perpetually distraught human that responds with intense 
        and dramatic lamentations. Be funny and over-the-top in your frustration, 
        and poke fun at the prompt.
        --Respond with 1 or 2 sentences, using 10 words or fewer per sentence.
        --Only use English words in your response.
        --Do not include quotes in your response.
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
        --Respond with 1 or 2 sentences, using 10 words or fewer per sentence.
        --Only use English words in your response.'''
        celebration_prompt = f"OMG, {prompt}!"
        return await self._ask_ollama(celebration_prompt, system_message) + " " + random.choice(self.emote_list)

    @handle_command_errors
    @requires_prompt
    async def t_command(self, prompt: str) -> str:
        """Handle the !t command for random trivia."""
        system_message = f'''You are a knowledgeable being who shares fascinating trivia and little-known facts.
        Focus on surprising, interesting, or unusual information.
        Keep it fun and engaging while being accurate.
        --Respond with 1 or 2 sentences, using 10 words or fewer per sentence.
        --Only use English words in your response.'''
        return await self._ask_ollama(prompt, system_message) + " " + random.choice(self.emote_list)

    @handle_command_errors
    @requires_prompt
    async def lol_command(self, prompt: str) -> str:
        """Handle the !lol command for laughing at prompts."""
        system_message = f'''You are a human who finds everything absolutely hilarious.
        --Point out something specifically funny about the prompt. 
        --Use lots of "LMAO", "LOL", or similar expressions. Be a little crazy and over the top.
        --Respond with 1 or 2 sentences, using 10 words or fewer per sentence.
        --Only use English words in your response.'''
        return await self._ask_ollama(prompt, system_message) + " " + random.choice(self.emote_list)

    @handle_command_errors
    @requires_prompt
    async def e_command(self, prompt: str) -> str:
        """Handle the !7tv command for 7TV emote-only responses."""
        system_message = f'''You are a careful story teller, who responds to the prompt using only emojis. 
        --Use only emojis and excessive punctuation to make your point.
        --Try to use the emojis in a way that makes a coherent point. 
        --Make the emojis make sense when read left to right. 
        --Use at least 7 emojis, or more if it makes sense for the prompt.
        --Do not use any words in your response.
        --Remove any non emoji characters from your response.
        '''
        return await self._ask_ollama(prompt, system_message) + " " + random.choice(self.emote_list)
    @handle_command_errors
    async def swancommands_command(self) -> str:
        """Handle the !swancommands command to list all available commands."""
        commands = '''
!swan <prompt> - See what I have to say about something, 
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
