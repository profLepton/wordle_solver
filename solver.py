import random
import math
from tqdm import tqdm
file_path = "word_list.txt"

words_list = []

def load_words():
    with open(file_path, "r") as file:
        for line in file:
            words_list.append(line.strip().lower())



load_words()

def rank_words(words):

    frequency_of_letters = {}
    for word in words:
        for i, letter in enumerate(word):
            frequency_of_letters[(i, letter)] = frequency_of_letters.get((i, letter), 0) + 1
            

    probability_of_letters = {}

    l = len(words)

    for letter_pair, frequency in frequency_of_letters.items():
        probability_of_letters[letter_pair] = frequency / l

    word_scores = {}

    for word in words:
        prob = 0
        for i, letter in enumerate(word):
            prob += probability_of_letters[(i, letter)] * -math.log(probability_of_letters[(i, letter)])
        word_scores[word] = prob * len(set(word))
    

    sorted_words = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)

    return sorted_words



def trim_list(correct_placed, wrong_placed_letters, wrong_letters, word_list):

    # correct placed
    for i, letter in correct_placed:
        word_list = [word for word in word_list if word[i] == letter]

    # wrong placed
    for i, letter in wrong_placed_letters:
        word_list = [word for word in word_list if  letter in word and word[i] != letter]

    # wrong letters
    for i, letter in wrong_letters:
        word_list = [word for word in word_list if letter not in word]

    return word_list

def check_word(guess, target):

    correct_placed = []
    wrong_placed_letters = []

    for i in range(len(target)):
        if guess[i] == target[i]:
            correct_placed.append((i, guess[i]))
        elif guess[i] in target:
            wrong_placed_letters.append((i, guess[i]))

    wrong_letters = [(i, guess[i]) for i in range(len(target)) if (i, guess[i]) not in correct_placed and (i, guess[i]) not in wrong_placed_letters]

    return correct_placed, wrong_placed_letters, wrong_letters

def silenced_game(target_word, rank_words):
    
    solved = False
    words = words_list.copy()
    num_tries = 6
    while num_tries > 0 and not solved:

        # print("Number of tries left: ", num_tries)
        # Guess a word
        ranked_list = rank_words(words)

        guess = ranked_list[0]

        # print("Suggestions: ")
        # for i in range(0, min(4, len(ranked_list))):
            # print(f"{i+1}) {ranked_list[i]}")

        # Check if guess is correct

        TakeInput = True

        while TakeInput:
            try:
                # print("Enter a word >", end="")
                # guess = input().strip().lower()
                guess = ranked_list[0][0]

                
                

                if len(guess) != len(target_word):
                    raise ValueError("Word length does not match")
                
                if guess not in words:
                    raise ValueError("Word not in dictionary")
                
                TakeInput = False

            except EOFError:
                exit(0)

            except:
                print("Invalid word. Try again")
                
                continue


        

        if guess == target_word:
            # print("You have guessed the word!")

            return 6 - num_tries
            solved = True


        else:
            correct_placed, wrong_placed_letters, wrong_letters = check_word(guess, target_word)
            # print("--> ", end="")
            # for i, letter in enumerate(guess):
            #     if (i, letter) in correct_placed:
            #         print(f"[{letter}]", end="")
            #     elif (i, letter) in wrong_placed_letters:
            #         print(f"({letter})", end="")
            #     else:
            #         print(letter, end="")

            # print(f"\n {len(correct_placed)} correct placed, {len(wrong_placed_letters)} wrong placed")
            
            old_len = len(words)
            words = trim_list(correct_placed, wrong_placed_letters, wrong_letters, words)
            
            # print(len(words) - old_len, f" words removed from list, {len(words)} words left")


        num_tries -= 1

    if not solved:
        # print("You have run out of tries. The word was ", target_word)
        return -1
    
def game(target_word, rank_words):
    
    solved = False
    words = words_list.copy()
    num_tries = 6
    while num_tries > 0 and not solved:

        print("Number of tries left: ", num_tries)
        # Guess a word
        ranked_list = rank_words(words)

        guess = ranked_list[0]

        print("Suggestions: ")
        for i in range(0, min(5, len(ranked_list))):
            print(f"{i+1}) {ranked_list[i]}")

        # Check if guess is correct

        TakeInput = True

        while TakeInput:
            try:
                print("Enter a word >", end="")
                guess = input().strip().lower()
                

                
                

                if len(guess) != len(target_word):
                    raise ValueError("Word length does not match")
                
                if guess not in words:
                    raise ValueError("Word not in dictionary")
                
                TakeInput = False

            except EOFError:
                exit(0)

            except:
                print("Invalid word. Try again")
                
                continue


        

        if guess == target_word:
            print("You have guessed the word!")

            return 6 - num_tries
            solved = True


        else:
            correct_placed, wrong_placed_letters, wrong_letters = check_word(guess, target_word)
            print("--> ", end="")
            for i, letter in enumerate(guess):
                if (i, letter) in correct_placed:
                    print(f"[{letter}]", end="")
                elif (i, letter) in wrong_placed_letters:
                    print(f"({letter})", end="")
                else:
                    print(letter, end="")

            print(f"\n {len(correct_placed)} correct placed, {len(wrong_placed_letters)} wrong placed")
            
            old_len = len(words)
            words = trim_list(correct_placed, wrong_placed_letters, wrong_letters, words)
            
            print(len(words) - old_len, f" words removed from list, {len(words)} words left")


        num_tries -= 1

    if not solved:
        print("You have run out of tries. The word was ", target_word)
        return -1

def get_strategy_score(strategy):
    score = 0
    num_solved = 0
    unsolved = 0
    


    for word in tqdm(words_list):
        score = silenced_game(word, strategy)
        if score == -1:
            unsolved += 1
        else:
            score += score
            num_solved += 1

    print(f"Strategy score: {score/num_solved} \n Solve rate: {num_solved/len(words_list)} \n Unsolved: {unsolved}")



def get_word_placements_from_user(guess):
    correct_placed = []
    wrong_placed_letters = []
    wrong_letters = []

    for i, letter in enumerate(guess):
        print(f"Letter {i+1}/{len(guess)}: {letter}")
        print("1) Correct placement")
        print("2) Wrong placement")
        print("3) Wrong letter")
        print("4) Skip")
        print("5) Exit")

        choice = input(">")
        if choice == "1":
            correct_placed.append((i, letter))
        elif choice == "2":
            wrong_placed_letters.append((i, letter))
        elif choice == "3":
            wrong_letters.append((i, letter))
        elif choice == "4":
            continue
        elif choice == "5":
            exit(0)
        else:
            print("Invalid choice. Try again")
            i -= 1

    return correct_placed, wrong_placed_letters, wrong_letters

def human_game( rank_words):
    
    solved = False
    words = words_list.copy()
    num_tries = 6
    while num_tries > 0 and not solved:

        print("Number of tries left: ", num_tries)
        # Guess a word
        ranked_list = rank_words(words)

        guess = ranked_list[0]

        print("Suggestions: ")
        for i in range(0, min(5, len(ranked_list))):
            print(f"{i+1}) {ranked_list[i]}")

        # Check if guess is correct

        TakeInput = True

        while TakeInput:
            try:
                print("Enter a word >", end="")
                guess = input().strip().lower()
                
                
                if guess not in words:
                    raise ValueError("Word not in dictionary")
                
                TakeInput = False

            except EOFError:
                exit(0)



        else:
            correct_placed, wrong_placed_letters, wrong_letters = get_word_placements_from_user(guess)
            print("--> ", end="")
            for i, letter in enumerate(guess):
                if (i, letter) in correct_placed:
                    print(f"[{letter}]", end="")
                elif (i, letter) in wrong_placed_letters:
                    print(f"({letter})", end="")
                else:
                    print(letter, end="")

            print(f"\n {len(correct_placed)} correct placed, {len(wrong_placed_letters)} wrong placed")
            
            old_len = len(words)
            words = trim_list(correct_placed, wrong_placed_letters, wrong_letters, words)
            
            print(len(words) - old_len, f" words removed from list, {len(words)} words left")


        num_tries -= 1

    if not solved:
        print("You have run out of tries. The word was ", target_word)
        return -1

def get_strategy_score(strategy):
    score = 0
    num_solved = 0
    unsolved = 0
    


    for word in tqdm(words_list):
        score = silenced_game(word, strategy)
        if score == -1:
            unsolved += 1
        else:
            score += score
            num_solved += 1

    print(f"Strategy score: {score/num_solved} \n Solve rate: {num_solved/len(words_list)} \n Unsolved: {unsolved}")


def play_game(strategy):
    target_word = random.choice(words_list)
    game(target_word, strategy)

if __name__ == "__main__":
    # play_game(rank_words)
    # get_strategy_score(rank_words)
    human_game(rank_words)
    