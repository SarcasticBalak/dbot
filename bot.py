import pyfiglet
import requests
import time
import random
import datetime

TOKEN = "YOUR_DISCORD_BOT_TOKEN"  
CHANNEL_IDS = [1123324986866806865]  

MESSAGES = [
    "Hey, are we early? 👀",
    "How do I get a role here?",
    "Where’s the roadmap? Need to see what’s cooking. 🔥",
    "Is there a guide on how to start?",
    "What’s the requirement to be eligible?",
    "Did I miss it, or is it still open?",
    "When’s the next update?",
    "What’s next after this?",
    "Who’s been here the longest?",
    "How do I check my status?",
    "Is there a way to track progress?",
    "Can someone drop a step-by-step guide?",
    "What’s the best way to stay updated?",
    "Any perks for early members?",
    "How do I invite friends to join?",
    "What’s the official announcement channel?",
    "Who do I contact if I have issues?",
    "Is there a way to verify my account?",
    "How do I know if I’m in?",
    "What’s the timeline for this?",
    "Where can I find the full details?",
    "What’s the easiest way to get started?",
    "Is there a checklist of things to do?",
    "What’s the next step after signing up?",
    "Are there different levels or tiers?",
    "How do I know if I completed all the steps?",
    "Is there a leaderboard or ranking?",
    "What’s the most important thing to do right now?",
    "Can someone confirm if everything is working fine?",
    "What’s the most common mistake people make here?"
    }

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
