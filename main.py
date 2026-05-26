import time
import random
from loadingspinny import loading_spinner # very professional names
from otherfunctions import *
import os, subprocess
import signal


"""
This is made to be running in SSH for anybody to play!

"""
word = False

#handle the people trying to escape SSH
def graceful_exit(sig, frame):
    print(f"\n\n  Thanks for playing Wordle!\n")
    raise SystemExit(0)
 
signal.signal(signal.SIGINT, graceful_exit)
signal.signal(signal.SIGTERM, graceful_exit)


print('\033[2J\033[H', end='')
print('='*20)
print("Welcome to Cli Wordle!\nWell done for making it this far!\nPress enter ↵ to start!")
input()



with loading_spinner("Generating random word"):
    with open('5letterwords.txt') as f:
        words = f.readlines()
    word = words[random.randint(2,len(words))]

# Ask if we can put them on leaderboard
consentForLeaderboard = confirmleaderboard()

if consentForLeaderboard: get_player_info

if consentForLeaderboard:
    username = False
    while True:
        username = input('Username:\n')
        result = False
        with loading_spinner("Moderating Username"):
            is_flagged, flagged_for = moderate_text(username)
        if is_flagged == False:
            break
        else:
            print(f"Your username has been flagged for: {", ".join(flagged_for)}")
            print('Please try again.')
    

print('\033[2J\033[H', end='')
print('='*20)
print('Lets Begin!')

# print(word)



# Colours
RESET     = "\033[0m"
BOLD      = "\033[1m"
BG_GREEN  = "\033[42m"
BG_YELLOW = "\033[43m"
BG_GREY   = "\033[100m"
FG_WHITE  = "\033[97m"
 
def green(text):   return f"{BG_GREEN}{FG_WHITE}{BOLD} {text.upper()} {RESET}"
def yellow(text):  return f"{BG_YELLOW}{FG_WHITE}{BOLD} {text.upper()} {RESET}"
def grey(text):    return f"{BG_GREY}{FG_WHITE}{BOLD} {text.upper()} {RESET}"
def clear():       print('\033[2J\033[H', end='')

