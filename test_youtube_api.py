import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = "UCraDr3i5A3k0j7typ6tOOsQ"

print(f"YouTube API Key: {YOUTUBE_API_KEY}")
print(f"Channel ID: {CHANNEL_ID}")
print("\n--- Testing YouTube API ---\n")

# Test 1: Check API key format
if not YOUTUBE_API_KEY or not YOUTUBE_API_KEY.startswith("AIza"):
    print("[ERROR] Invalid YouTube API key format")
    print("   API keys should start with 'AIza'")
else:
    print("[OK] API key format looks correct")

# Test 2: Try to fetch from YouTube API
base_url = "https://www.googleapis.com/youtube/v3/search"
params = {
    "part": "snippet",
    "channelId": CHANNEL_ID,
    "maxResults": 5,
    "order": "date",
    "type": "video",
    "key": YOUTUBE_API_KEY,
}

print(f"\nMaking request to: {base_url}")
print(f"Channel ID: {CHANNEL_ID}")

try:
    response = requests.get(base_url, params=params)
    print(f"\nResponse Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("[OK] Request successful!")
        print(f"  Items returned: {len(data.get('items', []))}")
        if data.get('items'):
            print(f"\n  First video title: {data['items'][0]['snippet']['title']}")
    else:
        print("[ERROR] Request failed!")
        print(f"  Response: {response.text}")
        
        # Check for common errors
        if response.status_code == 400:
            print("\n  [INFO] Error 400: Bad Request")
            print("     - Check if API key is correct")
            print("     - Check if channel ID is correct")
        elif response.status_code == 403:
            error_data = response.json()
            print("\n  [INFO] Error 403: Forbidden")
            print(f"     - Reason: {error_data.get('error', {}).get('message', 'Unknown')}")
            print("     - API key may be invalid or expired")
            print("     - API may not be enabled in Google Cloud Console")
            print("     - Quota may be exceeded")
        elif response.status_code == 429:
            print("\n  [INFO] Error 429: Too Many Requests")
            print("     - API quota exceeded, try again later")
            
except Exception as e:
    print(f"[ERROR] Exception occurred: {e}")

print("\n--- Test Complete ---")
