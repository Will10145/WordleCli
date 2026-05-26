import time
import random
from loadingspinny import loading_spinner # very professional names
from otherfunctions import *
import os, subprocess


word = False


print('='*20)
print("Welcome to Cli Wordle!\nWell done for making it this far!\nPress enter ↵ to start!")
input()


with loading_spinner("Generating random word"):
    with open('5letterwords.txt') as f:
        words = f.readlines()
    word = words[random.randint(2,len(words))]

# Ask if we can put them on leaderboard
consentForLeaderboard = confirmleaderboard()

print(os.environ.get('SSH_AUTH_INFO_0', None))
print(os.environ.get('SSH_CLIENT'))

print('\033[2J\033[H', end='')
print('='*20)
print('Lets Begin!')

# print(word)