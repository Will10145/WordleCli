import time
import random
from loadingspinny import loading_spinner # very professional names
from otherfunctions import *
import os, signal, json
from pathlib import Path

"""
This is made to be running in SSH for anybody to play!
"""

MAX_GUESSES      = 6
STATS_FILE       = "/var/lib/wordle/stats.json"
word             = False

# handle the people trying to escape SSH
def graceful_exit(sig, frame):
    print(f"\n\n  Thanks for playing Wordle!\n")
    raise SystemExit(0)

signal.signal(signal.SIGINT, graceful_exit)
signal.signal(signal.SIGTERM, graceful_exit)

# colours
RESET     = "\033[0m"
BOLD      = "\033[1m"
BG_GREEN  = "\033[42m"
BG_YELLOW = "\033[43m"
BG_GREY   = "\033[100m"
FG_WHITE  = "\033[97m"

def green(text):  return f"{BG_GREEN}{FG_WHITE}{BOLD} {text.upper()} {RESET}"
def yellow(text): return f"{BG_YELLOW}{FG_WHITE}{BOLD} {text.upper()} {RESET}"
def grey(text):   return f"{BG_GREY}{FG_WHITE}{BOLD} {text.upper()} {RESET}"
def clear():      print('\033[2J\033[H', end='')

# ── stats helpers ──────────────────────────────────────────────────────────────

def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def get_pubkey():
    parts = os.environ.get("SSH_AUTH_INFO_0", "").split()
    return parts[2] if len(parts) >= 3 else None

def get_returning_player(pubkey):
    if not pubkey:
        return None
    return load_json(STATS_FILE).get(pubkey)

def save_player(pubkey, data):
    stats = load_json(STATS_FILE)
    stats[pubkey] = data
    save_json(STATS_FILE, stats)

def update_stats(pubkey, player, won, guess_count):
    player["games"]  = player.get("games", 0) + 1
    player["wins"]   = player.get("wins", 0) + (1 if won else 0)
    player["streak"] = (player.get("streak", 0) + 1) if won else 0
    if won:
        player["last_guesses"] = guess_count
    save_player(pubkey, player)

def show_leaderboard():
    stats = load_json(STATS_FILE)
    if not stats:
        print("\n  No leaderboard entries yet.\n")
        return

    players = sorted(
        [(v["username"], v.get("wins", 0), v.get("games", 0))
         for v in stats.values() if "username" in v],
        key=lambda x: x[1], reverse=True
    )

    print(f"\n  {'─'*32}")
    print(f"  {'LEADERBOARD':^32}")
    print(f"  {'─'*32}")
    print(f"  {'#':<4} {'Player':<16} {'Wins':<6} Games")
    print(f"  {'─'*32}")
    for i, (name, wins, games) in enumerate(players[:10], 1):
        print(f"  {i:<4} {name:<16} {wins:<6} {games}")
    print(f"  {'─'*32}\n")

# ── game logic ─────────────────────────────────────────────────────────────────

def evaluate_guess(guess, word):
    result         = ['grey'] * 5
    word_remaining = list(word)

    for i in range(5):                          # greens first
        if guess[i] == word[i]:
            result[i]         = 'green'
            word_remaining[i] = None

    for i in range(5):                          # then yellows
        if result[i] == 'green':
            continue
        if guess[i] in word_remaining:
            result[i] = 'yellow'
            word_remaining[word_remaining.index(guess[i])] = None

    return list(zip(guess, result))

def render_row(evaluated):
    row = "  "
    for letter, result in evaluated:
        if   result == 'green':  row += green(letter)
        elif result == 'yellow': row += yellow(letter)
        else:                    row += grey(letter)
    print(row)

def render_board(guesses):
    print()
    for ev in guesses:
        render_row(ev)
    for _ in range(MAX_GUESSES - len(guesses)):
        print("  " + "".join(f"{BG_GREY}   {RESET}" for _ in range(5)))
    print()

def render_keyboard(guesses):
    used     = {}
    priority = {'green': 3, 'yellow': 2, 'grey': 1}
    for ev in guesses:
        for letter, result in ev:
            if letter not in used or priority[result] > priority[used[letter]]:
                used[letter] = result

    print()
    for row in ["qwertyuiop", "asdfghjkl", "zxcvbnm"]:
        line = "  "
        for ch in row:
            if ch in used:
                r = used[ch]
                if   r == 'green':  line += green(ch)
                elif r == 'yellow': line += yellow(ch)
                else:               line += grey(ch)
            else:
                line += f" {ch.upper()} "
        print(line)
    print()

# ── startup ────────────────────────────────────────────────────────────────────

clear()
print('='*20)
print("Welcome to Cli Wordle!\nWell done for making it this far!\nPress enter ↵ to start!")
input()

with loading_spinner("Generating random word"):
    words = load_json('words.json')
    if not isinstance(words, list) or not words:
        raise ValueError("words.json must contain a non-empty list of words.")
    word = random.choice(words)

# check for returning player first
pubkey          = get_pubkey()
player          = get_returning_player(pubkey)
username        = player.get("username") if player else None
consentForLeaderboard = player is not None

# new player — ask about leaderboard + username
if not consentForLeaderboard:
    consentForLeaderboard = confirmleaderboard()

    if consentForLeaderboard:
        username = False
        while True:
            username = input('Username:\n')
            with loading_spinner("Moderating Username"):
                is_flagged, flagged_for = moderate_text(username)
            if not is_flagged:
                break
            print(f"Your username has been flagged for: {', '.join(flagged_for)}")
            print('Please try again.')

        if pubkey:
            save_player(pubkey, {"username": username, "wins": 0, "games": 0, "streak": 0})
            player = load_json(STATS_FILE).get(pubkey)

# let's go
clear()
print('='*20)
if username and player:
    print(f"  Welcome back, {username}!  Wins: {player.get('wins',0)}/{player.get('games',0)}  Streak: {player.get('streak',0)}")
else:
    print(f"  {green('A')} correct   {yellow('B')} wrong place   {grey('C')} not in word")
print("Lets Begin!\n")

guesses = []
won = False

while len(guesses) < MAX_GUESSES:
    render_board(guesses)
    render_keyboard(guesses)

    print(f"  Guess ({MAX_GUESSES - len(guesses)} left): ", end="", flush=True)
    try:
        raw = input().strip().lower()
    except EOFError:
        graceful_exit(None, None)

    if len(raw) != 5:
        print("  5 letters please.")
        continue
    if not raw.isalpha():
        print("  Letters only please.")
        continue

    guesses.append(evaluate_guess(raw, word))

    clear()
    print('='*20)
    if username:
        print(f"  {username}\n")

    if raw == word:
        won = True
        break

# end

render_board(guesses)

# get word definition
meaning, phonetic = False, False
with loading_spinner('Finding definition'):
    phonetic, meaning = define_word(word)
print(f"The word was:\n{word} • {phonetic}\n{meaning}")
if won:
    print(f"  {BOLD}Well done, {username}, you got it in {len(guesses)}! Well done 👏{RESET}")
else:
    print(f"  oh well ):, at least you tried!")

if consentForLeaderboard and pubkey and player:
    update_stats(pubkey, player, won, len(guesses))

print()
if input("  Show leaderboard? (yes/no)\n  > ").strip().lower() in ("yes", "y"):
    show_leaderboard()

print("  Thanks for playing!\n")