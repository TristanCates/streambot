import time
from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
from selenium.webdriver.common.action_chains import ActionChains
import asyncio

class BrowserCommands:
    def __init__(self, bot):
        self.bot = bot
        self.driver = None
    
        self.chrome_options = Options()
        self.chrome_options.remote_debugging_port = 9222
        self.setup_driver()

    def setup_driver(self):
        print("Starting Chrome driver setup...")
               
        try:
            service = ChromeService(os.getenv("CHROME_DRIVER_PATH"))
            self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
            print("Successfully connected to existing Chrome instance")
        except Exception as e:
            print(f"Chrome driver setup failed: {e}")
            print("Make sure Chrome is running with remote debugging enabled:")
            print("chrome.exe --remote-debugging-port=9222")
            raise

    async def shutdown(self):
        print("Shutting down Chrome driver...")
        if self.driver:
            self.driver.quit()
        print("Chrome driver shutdown complete.")

    async def navigate_to(self, url):
        """Changes the current URL in the Chrome window if it's from Twitch or YouTube"""
        if not self.driver:
            print("Driver not initialized")
            return False
        
        # Check if URL is from allowed domains
        allowed_domains = ["twitch.tv", "youtube.com", "youtu.be"]
        if not any(domain in url.lower() for domain in allowed_domains):
            print(f"URL not allowed. Only Twitch and YouTube links are accepted.")
            return ""
     
        try:
            print(f"Navigating to: {url}")
            self.driver.get(url)

            # For YouTube videos, try to click the video player
            if "youtube.com" in url.lower() or "youtu.be" in url.lower():
                #try:
                    #video_player = self.driver.find_element(By.ID, "movie_player")
                    #video_player.click()
                    #print("Clicked the video player")
                #except Exception as e:
                    #print(f"Could not find video player: {e}")
                return "youtube"
            
            return "twitch"
            
        except Exception as e:
            print(f"Navigation failed: {e}")
            return False
        
async def mute_audio(self, urlType):
    self.chrome_options.add_argument("--mute-audio")

    #also pause the video if it's a youtube video
    if urlType == "youtube":   
        try:
            video_player = self.driver.find_element(By.ID, "movie_player")
            video_player.click()
            print("Clicked the video player")
        except Exception as e:
            print(f"Could not find video player: {e}")

async def unmute_audio(self):
    self.chrome_options.remove_argument("--mute-audio")

async def get_url_input():
    """Asynchronously get URL input from the terminal"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, "Enter URL (or 'exit' to quit): ")

async def main():
    # Initialize the browser commands
    browser = BrowserCommands(None)  # Pass None since we're not using the bot context
    
    try:
        # Main input loop
        while True:
            url = await get_url_input()
            
            if url.lower() == 'exit':
                print("Exiting...")
                break
                
            if url:
                await browser.navigate_to(url)
    
    except KeyboardInterrupt:
        print("\nReceived exit signal, shutting down...")
    except asyncio.CancelledError:
        print("Task was cancelled, shutting down...")
    finally:
        # Clean up
        await browser.shutdown()  # Shutdown the browser
        print("Shutdown complete.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"Program terminated due to error: {e}")