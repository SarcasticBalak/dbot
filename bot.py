import time
import json
import requests
from colorama import Fore, Style, init
from datetime import datetime
import random
import threading

# Initialize colorama
init(autoreset=True)

COLORS = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]

def get_timestamp():
    """Return the current timestamp in green color."""
    return f"{Fore.YELLOW}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}"

def colorful_text(text):
    """Return the text with each letter in a different random color."""
    return ''.join(random.choice(COLORS) + char for char in text)

def load_config(file_path):
    """Load configuration from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"{get_timestamp()} | {Fore.RED}Error loading {file_path}: {e}")
        exit(1)

def send_message(token, channel_id, message):
    """Send a single message to the specified Discord channel."""
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {"content": message}
    base_url = f"https://discord.com/api/v9/channels/{channel_id}/messages"

    response = requests.post(base_url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"{get_timestamp()} | {Fore.GREEN}Successfully sent: {message}")
    else:
        print(f"{get_timestamp()} | {Fore.RED}Failed to send: {message}. Error: {response.status_code}")

def send_messages(account, messages):
    """Send messages for a specific account."""
    token = account.get("token")
    servers = account.get("servers", [])

    if not token or not servers:
        print(f"{get_timestamp()} | {Fore.RED}Missing token or servers for account!")
        return

    for server in servers:
        server_name = server.get("name")
        channel_id = server.get("channel_id")
        server_messages = messages.get(server_name, [])

        if not channel_id or not server_messages:
            print(f"{get_timestamp()} | {Fore.RED}Missing channel_id or messages for server: {server_name}!")
            continue

        print(f"{get_timestamp()} | {Fore.CYAN}Sending messages to server: {server_name}")
        for message in server_messages:
            send_message(token, channel_id, message)
            time.sleep(60)  # Wait 10 seconds between messages

def run_all_accounts(accounts, messages):
    """Run all accounts simultaneously."""
    threads = []
    for account in accounts:
        thread = threading.Thread(target=send_messages, args=(account, messages))
        threads.append(thread)
        thread.start()
        print(f"{get_timestamp()} | {Fore.CYAN}Started sending messages for account: {account.get('name')}")

    for thread in threads:
        thread.join()
    print(f"{get_timestamp()} | {Fore.BLUE}All accounts have finished sending messages!")

def main():
    # Load configuration and messages
    config = load_config('config.json')
    messages = load_config('messages.json')

    accounts = config.get("accounts", [])

    if not accounts or not messages:
        print(f"{get_timestamp()} | {Fore.RED}Missing required data in configuration files!")
        exit(1)

    # Display colorful ASCII banner
    ascii_art = r'''
 ____  _                       _   _____           _ 
|  _ \(_)___  ___ ___  _ __ __| | |_   _|__   ___ | |
| | | | / __|/ __/ _ \| '__/ _` |   | |/ _ \ / _ \| |
| |_| | \__ \ (_| (_) | | | (_| |   | | (_) | (_) | |
|____/|_|___/\___\___/|_|  \__,_|   |_|\___/ \___/|_|

    '''
    print(f"{Fore.GREEN}{ascii_art}")
    banner_text = "This script will send messages to Discord for selected accounts and servers."
    print(f"{get_timestamp()} | {colorful_text(banner_text)}")

    # Account selection menu
    print(f"{get_timestamp()} | {Fore.MAGENTA}Available options:")
    print(f"{Fore.CYAN}[1] Select a single account")
    print(f"{Fore.CYAN}[2] Run all accounts at once")

    try:
        choice = int(input(f"{get_timestamp()} | {Fore.MAGENTA}Select an option (1-2): "))
        if choice not in [1, 2]:
            raise ValueError("Invalid choice")
    except Exception:
        print(f"{get_timestamp()} | {Fore.RED}Invalid selection. Exiting.")
        exit(1)

    if choice == 1:
        print(f"{get_timestamp()} | {Fore.MAGENTA}Available accounts:")
        for index, account in enumerate(accounts, start=1):
            print(f"{Fore.CYAN}[{index}] {account.get('name')}")

        try:
            account_choice = int(input(f"{get_timestamp()} | {Fore.MAGENTA}Select an account (1-{len(accounts)}): ")) - 1
            if account_choice < 0 or account_choice >= len(accounts):
                raise ValueError("Invalid choice")
        except Exception:
            print(f"{get_timestamp()} | {Fore.RED}Invalid selection. Exiting.")
            exit(1)

        selected_account = accounts[account_choice]
        send_messages(selected_account, messages)

    elif choice == 2:
        print(f"{get_timestamp()} | {Fore.BLUE}Running all accounts...")
        run_all_accounts(accounts, messages)

    print(f"{get_timestamp()} | {Fore.BLUE}All tasks completed successfully!")

if __name__ == "__main__":
    main()
