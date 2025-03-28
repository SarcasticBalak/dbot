import pyfiglet
import requests
import time
import random
import datetime

TOKEN = "YOUR_DISCORD_BOT_TOKEN"  
CHANNEL_IDS = [1123324986866806865]  

MESSAGES = [
    "Crypto never sleeps! What’s the latest alpha?",
    "DeFi is evolving fast. Any interesting protocols to check out?",
    "Bull or bear? What’s your take on the market today?",
    "Any upcoming airdrops that are worth farming?",
    "Anyone still holding their bags from 2021? 😅",
    "Layer 2 scaling solutions are getting wild! Optimistic rollups or ZK rollups?",
    "Ethereum gas fees are brutal today! Who else is waiting for L2 transactions?",
    "Crypto is down bad today, time to buy or time to wait?",
    "Imagine explaining DeFi to your grandparents. How would you do it?",
    "What’s the best wallet for security and ease of use?"
]

HEADERS = {
    "Authorization": f"Bot {TOKEN}",  
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def display_startup():
    ascii_art = pyfiglet.figlet_format("ARISTO")
    print(ascii_art)
    print("Bot Started - ARISTO")

def send_message(channel_id):
    message_to_send = random.choice(MESSAGES)
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    payload = {"content": message_to_send}

    typing_time = random.randint(3, 7)
    print(f"Typing for {typing_time} seconds before sending...")
    time.sleep(typing_time)

    response = requests.post(url, json=payload, headers=HEADERS)

    if response.status_code == 200:
        msg_id = response.json()["id"]
        print(f"✅ Sent: '{message_to_send}' in {channel_id}")

        delete_delay = random.randint(2,3)  
        time.sleep(delete_delay)

        delete_url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{msg_id}"
        delete_response = requests.delete(delete_url, headers=HEADERS)

        if delete_response.status_code == 204:
            print("🗑 Message deleted successfully!")
        else:
            print(f"⚠️ Failed to delete message: {delete_response.status_code} - {delete_response.text}")

    elif response.status_code == 429:
        retry_after = response.json().get("retry_after", 5)
        print(f"⏳ Rate limited! Waiting {retry_after} seconds before retrying...")
        time.sleep(retry_after)
    
    else:
        print(f"❌ Failed to send message: {response.status_code} - {response.text}")

# Start bot
display_startup()

while True:
    for channel_id in CHANNEL_IDS:
        try:
            send_message(channel_id)
            
            delay = random.randint(300, 600) 
            print(f"⏳ Waiting {delay} seconds before next message...")
            time.sleep(delay)
            
            if random.randint(1, 10) > 8:  
                break_time = random.randint(600, 1200)  # 10-20 min break
                print(f"😴 Taking a short break for {break_time // 60} minutes...")
                time.sleep(break_time)
            
            if datetime.datetime.now().hour in [3, 4, 5]:  # Late-night long break
                print("🌙 Late night detected, taking a long break...")
                time.sleep(3600)  # 1-hour break
        except Exception as e:
            print(f"🚨 Error: {e}. Retrying in 5 minutes...")
            time.sleep(300)
