"""
Word Game

This is a pass and play word game where players take turns coming up with English 
words that include a random substring.

How it works:   
1. Players enter their names and decide how many lives everyone starts with.
2. Each round, the game picks a random substring from a word.
3. Players take turns entering any English words that contain the substring:
   - If you fail to provide a valid word, 
   or your word doesn’t include the substring, you lose a life.
4. Longest word: Gain a life, Shortest word: Lose a life.
5. Elimination:
   - Players are out of the game when their lives hit zero.
   - The game ends when there’s only one player left or everyone is out.

6. Features:
- Choose your difficulty (Easy, Medium, Hard) to set how long the substrings are.
- Words are validated to ensure they are real and include the substring.
- At the end, all the words used by the players are saved to a file, `words_used.txt`.

"""

import random

# Load a file of English words as a set 
with open("words_alpha.txt") as f:
    valid_words = set(f.read().splitlines())

# Ask user for the number of players playing
def ask_p_num():
    try:
        return int(input("Number of players: "))
    except ValueError:
        # If user puts wrong input
        print("Invalid input! Please enter a valid number.")
        return ask_p_num() 
p_num = ask_p_num()

# Make a list p_num long to store the names of each player 
players = [""]*p_num

for i in range(p_num):
    players[i] = input("Player " + str(i+1) + " name: ")# Ask each player for name

# Ask user for desired starting lives for each player            
def ask_p_lives():
    try:
        return int(input("Starting lives per player: "))
    except ValueError:
        # If user puts wrong input
        print("Invalid input! Please enter a valid number.")
        return ask_p_lives() 
p_lives = ask_p_lives()

# Make a list p_num long to store the lives of each player
p_lives = [p_lives]*p_num 

# Ask player for difficulty
# This will affect the max substring length
def ask_dif():
    try:
        dif = input("Difficulty (easy,med,hard)(assumes easy if anything else): ")
        if dif == "hard":
            return 5
        elif dif == "med":
            return 3
        # Assume easy
        return 2
    except:
        print("Invalid input! Please enter a valid input (how did u even do dis :crying:).")
        return ask_p_lives()

MAX_SUBSTRING_LEN = ask_dif()

# Checks if what the player put is a valid word and not keyboard spam
def is_valid_word(player_input):
    return player_input.lower() in valid_words

# Check if anyone has lives below 1 and updatate corrisponding values
# This will be run at the end of every round
def check_lives():
    to_remove = []
    global p_num
    for i in range(p_num):
        if p_lives[i] < 1:
            to_remove.append(i)
            death_msg(i)
        
    # Remove the dead players from the game
    for i in range(len(to_remove)):
        p_num -= 1
        p_lives.pop(to_remove[i] - i)
        players.pop(to_remove[i] - i)
    
            
def death_msg(p_index):
    # Displays death messages for players
    print(players[p_index] + " ran out of lives and is out of the game.")

# Retrieve a random word from the set of valid words
def pick_word():

    return random.choice(list(valid_words))

# Chooses a random section of a word to use as the substring
def pick_substring():
    rand_word = pick_word()
    start = random.randint(0, len(rand_word) - 1)
    end = start + random.randint(1,MAX_SUBSTRING_LEN)
    return rand_word[start:end]

def check_game_end():
    if len(players) < 2:
        return True
    return False

def reward_players(players_i):
    for p in range(len(players_i)):
        p_lives[players_i[p]] += 1
    rewarded = []
    for p in players_i:
        rewarded.append(players[p])

    print(" and ".join(rewarded) + " gained a life for longest word!")

def punish_players(players_i):
    for p in range(len(players_i)):
        p_lives[players_i[p]] -= 1
    punished = []
    for p in players_i:
        punished.append(players[p])
    print(" and ".join(punished) + " lost a life for shortest word!")


# Used to store the words used by the players
# Output as a file when game ends
words_used = set()

# Main Game Loop
while not check_game_end():
    print("============NEW ROUND============\n")
    print("Players: "+" ".join(players))
    print("Lives:   "+" ".join(map(str, p_lives))+"\n")
    substring_this_round = pick_substring()

    print(f"Substring this round:\n\n{substring_this_round}\n")

    # Used later to find shortest and longest word lengths
    longest_word = -1
    shortest_word = 999

    # Used later to update stats after every round
    players_rewarded = []
    players_punished = []

    for i in range(p_num):
        inputed_string = input(players[i] + "'s turn: \n")

        #Checks if the player put a correct word
        if not is_valid_word(inputed_string) or substring_this_round not in inputed_string:
            p_lives[i] -= 1
            print("nice try not a valid word (-1 life)")
            continue

        # Add to the set of used words 
        words_used.add(inputed_string)

        #get the player(s) that put the shortest and longest words to punish/reward
        word_len = len(inputed_string)
        
        if word_len > longest_word:
            longest_word = word_len
            players_rewarded = [i]
        elif word_len == longest_word:
            players_rewarded.append(i)

        
        if word_len < shortest_word:
            shortest_word = word_len
            players_punished = [i]
        elif word_len == shortest_word:
            players_punished.append(i)

    # If the player is both rewarded and punished, their lives do not change
    canceled_out = set(players_punished) & set(players_rewarded)

    # Exclude players that get canceled out
    players_rewarded = [item for item in players_rewarded if item not in canceled_out]
    players_punished = [item for item in players_punished if item not in canceled_out]

    # Print what happend this round to the players
    print("\nResults:\n")
    
    if len(players_rewarded) > 0:
        reward_players(players_rewarded)
    else:
        print("no one was rewarded for longest word")

    if len(players_punished) > 0:
        punish_players(players_punished)
    else:
        print("no one was punished for shortest word")
    
    # Update players if anyone died
    print("\nDeaths:\n")
    check_lives()
    

# After the game, print results and output file of used words
print("\n============GAME OVER============\n")
try:
    print(players[0] + " has won the game!")
except:
    print("Everyone is out!")

# Output a file of all the words used by the players
with open("words_used.txt", 'w') as file:
        # Write each word on a new line
        for word in words_used:
            file.write(word + "\n")

