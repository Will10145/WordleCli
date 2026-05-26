# These are small useful functions that I won't ever need to edit / therefore i dont want them getting into the way of things
import os
from dotenv import load_dotenv
import json, requests

load_dotenv()

def url_click(url, text):
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"

def confirmleaderboard():
    while True:
        print('='*20)
        print('Would you like to enter the leaderboard?')
        print('Your Public key will be registered so we can remember your chosen username? This will not be shared.')
        print(url_click('https://willcodes.tech', "Privacy Policy"))
        print("Confirm: Y/n")
        print('='*20)
        d = input('')
        if d.lower() == 'n':
            return False
        elif d.lower() == 'y':
            return True
        

def get_player_info():
    conn = os.environ.get("SSH_CONNECTION", "").split()
    client_ip = conn[0] if conn else "unknown"
 
    auth_info = os.environ.get("SSH_AUTH_INFO_0", "")
    # Public key is the third token: "publickey ssh-ed25519 AAAA..."
    parts = auth_info.split()
    pubkey = parts[2] if len(parts) >= 3 else None
 
    return client_ip, pubkey

def moderate_text(txt):
    url = "https://ai.hackclub.com/proxy/v1/moderations"
    headers = {
        "Authorization": f"Bearer {os.getenv('HACKCLUB_AI_API_KEY')}",
        "Content-Type": "application/json",
    }

    data = {"input": txt}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    mod_data = response.json()
    categories = mod_data["results"][0]["categories"]
    is_flagged = mod_data["results"][0]["flagged"]

    flagged_for = []
    for category, status in categories.items():
        if status == True:
            flagged_for.append(category)
    print(f"DEBUG status: {response.status_code}")
    print(f"DEBUG body: {response.text}")
    return is_flagged, flagged_for


def define_word(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}" 
    response = requests.get(url).json()
    entry = response[0]
    meaning = entry['meanings'][0]['definitions'][0]['definition']
    phonetics_list = [p['text'] for p in entry['phonetics'] if 'text' in p]
    primary_phonetic = phonetics_list[0] if phonetics_list else "No phonetic spelling found"
    return primary_phonetic, meaning

if __name__ == "__main__":
    print('Do NOT run this script directly!')