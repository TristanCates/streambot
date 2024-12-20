import os
from dotenv import load_dotenv, find_dotenv
import requests

# Load environment variables first
load_dotenv(find_dotenv())

# Get token from environment
oauth_token = os.environ['BOT_OAUTH_TOKEN']

headers = {
    "Authorization": f"OAuth {oauth_token}"
}

# Send a GET request to the /validate endpoint
response = requests.get("https://id.twitch.tv/oauth2/validate", headers=headers)

# Check the response
if response.status_code == 200:
    data = response.json()
    print("Token is valid!")
    print("User ID:", data["user_id"])
    print("Username:", data["login"])
    print("Scopes:", data["scopes"])
else:
    print("Invalid token. Error:", response.json())
