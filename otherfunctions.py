# These are small useful functions that I won't ever need to edit / therefore i dont want them getting into the way of things

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
        

if __name__ == "__main__":
    print('Do NOT run this script directly!')