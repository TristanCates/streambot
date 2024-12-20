import os
import asyncio
import simpleobsws
from dotenv import load_dotenv, find_dotenv
from twitchio.ext import pubsub
from urllib.parse import urlparse
from simpleobsws import Request

class obsCommands():
    def __init__(self, bot):
        load_dotenv(find_dotenv())
        parameters = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks=False)
        
        print(f"Initializing OBS WebSocket connection...")
        ws_password = os.environ.get('OBS_WEB_SOCKET_PASSWORD', 'Not found!')
        print(f"WebSocket password from env: {ws_password}")
        
        self.ws = simpleobsws.WebSocketClient(
            url="ws://localhost:4455",
            password=ws_password,
            identification_parameters=parameters
        )
        
        print("WebSocket client initialized")
        self.clip_url = None
        self.bot = bot

    async def shutdown(self):
        print("Shutting down and closing WebSocket connection...")
        await self.ws.disconnect()
        print("WebSocket connection closed.")

    async def event_ready(self):
        print("Bot ready to display clips")
        await self.ws.connect()
        await self.ws.wait_until_identified()

  