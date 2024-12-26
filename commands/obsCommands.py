import os
import asyncio
import simpleobsws
from dotenv import load_dotenv, find_dotenv
from twitchio.ext import pubsub
from urllib.parse import urlparse
import time
import requests

class obsCommands():
    def __init__(self, bot):
        load_dotenv(find_dotenv())
        
        print(f"Initializing OBS WebSocket connection...")
        ws_password = os.environ.get('OBS_WEB_SOCKET_PASSWORD', 'Not found!')
        
        self.ws = simpleobsws.WebSocketClient(
            url="ws://localhost:4455",
            password=ws_password,
            identification_parameters=simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks=False)
        )

    async def connect(self):
        """Async initialization method"""
        await self.ws.connect()
        await self.ws.wait_until_identified()  # Make sure we're fully connected and identified
        print("WebSocket client initialized and identified")

    async def shutdown(self):
        print("Shutting down and closing WebSocket connection...")
        await self.ws.disconnect()
        print("WebSocket connection closed.")  

    async def get_scene_item_id(self, source_name):
        try:
            # First, get the current scene
            current_scene_request = simpleobsws.Request('GetCurrentProgramScene')
            current_scene_response = await self.ws.call(current_scene_request)
            current_scene = current_scene_response.responseData['currentProgramSceneName']
            
            # Then get the scene items
            request = simpleobsws.Request('GetSceneItemList', {
                'sceneName': current_scene
            })
            response = await self.ws.call(request)
            
            # Find the item ID for our source
            for item in response.responseData['sceneItems']:
                if item['sourceName'] == source_name:
                    return item['sceneItemId']
            return None
        except Exception as e:
            print(f"Error getting scene item ID: {e}")
            return None

    async def fade_out_link(self, source_name):
        try:
            # Get current scene and item ID
            item_id = await self.get_scene_item_id(source_name)
            if item_id is None:
                print(f"Could not find source {source_name}")
                return
                
            current_scene_request = simpleobsws.Request('GetCurrentProgramScene')
            current_scene_response = await self.ws.call(current_scene_request)
            current_scene = current_scene_response.responseData['currentProgramSceneName']
            
            # Set visibility
            request = simpleobsws.Request('SetSceneItemEnabled', {
                'sceneName': current_scene,
                'sceneItemId': item_id,
                'sceneItemEnabled': False
            })
            await self.ws.call(request)
            
        except Exception as e:
            print(f"Error hiding source: {e}")

    async def fade_in_link(self, source_name):
        try:
            # Get current scene and item ID
            item_id = await self.get_scene_item_id(source_name)
            if item_id is None:
                print(f"Could not find source {source_name}")
                return
                
            current_scene_request = simpleobsws.Request('GetCurrentProgramScene')
            current_scene_response = await self.ws.call(current_scene_request)
            current_scene = current_scene_response.responseData['currentProgramSceneName']
            
            # Set visibility
            request = simpleobsws.Request('SetSceneItemEnabled', {
                'sceneName': current_scene,
                'sceneItemId': item_id,
                'sceneItemEnabled': True
            })
            await self.ws.call(request)
            
        except Exception as e:
            print(f"Error showing source: {e}")

async def main():
    # Create an instance of obsCommands
    obs = obsCommands(None)  # Pass None since we're not using a bot context
    await obs.connect()
    
    try: 
        await obs.fade_in_link("ChatLink")
        await asyncio.sleep(5)
        await obs.fade_out_link("ChatLink")
 
    except Exception as e:
        print(f"Test failed with error: {e}")
        
    finally:
        # Clean up
        await obs.shutdown()
        print("Test complete.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"Program terminated due to error: {e}")
