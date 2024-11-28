import random
from typing import List
from cheater import WordleCheater
from collections import Counter


def load_words_from_csv(file_path: str) -> List[str]:
    with open(file_path, mode='r', encoding='utf-8') as file:
        words = [line.strip().lower() for line in file]
    return words


def provide_feedback(guess: str, answer: str) -> List[str]:
    feedback = ["gray"] * len(guess)
    answer_char_count = Counter(answer)

    for i, char in enumerate(guess):
        if char == answer[i]:
            feedback[i] = "green"
            answer_char_count[char] -= 1

    for i, char in enumerate(guess):
        if feedback[i] == "gray" and char in answer_char_count and answer_char_count[char] > 0:
            feedback[i] = "yellow"
            answer_char_count[char] -= 1

    return feedback


def wordle_game(file_path: str):
    words = load_words_from_csv(file_path)
    answer = random.choice(words)
    cheater = WordleCheater(words)
    print("Welcome to Wordle!")
    print("Choose a mode:\n1. Debug Mode (Cheater solves the game automatically)\n2. Manual Mode (You play the game)")
    mode = input("Enter 1 or 2: ").strip()

    if mode == "1":
        # Debug Mode: Cheater solves the game
        print(f"Answer (hidden): {answer}")
        for attempt in range(1, 7):
            guess = cheater.suggest_word()
            print(f"Attempt {attempt}: Cheater guessed -> {guess}")

            feedback = provide_feedback(guess, answer)
            cheater.history.append((guess, feedback))
            cheater.filter_words()

            print(f"Feedback: {feedback}")
            print(f"Remaining words: {len(cheater.remaining_words)}")

            if guess == answer:
                print("Cheater guessed the word correctly!")
                return
        print(f"Cheater failed to guess the word. The answer was {answer}.")

    elif mode == "2":
        print("Manual Mode: You have 6 attempts to guess the word.")
        for attempt in range(1, 7):
            help_choice = input("Do you want a suggestion from the cheater? (yes/no): ").strip().lower()
            if help_choice == "yes":
                suggestion = cheater.suggest_word()
                print(f"Suggested word: {suggestion}")
            guess = input(f"Attempt {attempt}: Enter your guess: ").strip().lower()

            if guess not in words:
                print("Invalid word! Please enter a word from the word list.")
                continue
            if len(guess) != len(answer):
                print(f"Please enter a {len(answer)}-letter word.")
                continue

            feedback = provide_feedback(guess, answer)
            print(f"Feedback: {feedback}")

            if guess == answer:
                print("Congratulations! You've guessed the word correctly!")
                return

            cheater.history.append((guess, feedback))
            cheater.filter_words()

        print(f"Game over! The correct word was: {answer}.")

    else:
        print("Invalid mode selected. Please restart the game.")


if __name__ == "__main__":
    wordle_game("full_data.csv")
