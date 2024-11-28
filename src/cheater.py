import random
from collections import Counter
from typing import List


class WordleCheater:
    def __init__(self, word_list: List[str]):
        self.remaining_words = word_list.copy()
        self.history = []

    def filter_words(self):
        for guess, feedback in self.history:
            filtered_words = []
            for word in self.remaining_words:
                valid = True
                char_count = Counter(word)

                for i, (char, fb) in enumerate(zip(guess, feedback)):
                    if fb == "green":
                        if word[i] != char:
                            valid = False
                            break
                    elif fb == "yellow":
                        if char not in word or word[i] == char:
                            valid = False
                            break
                        if char_count[char] <= 0:
                            valid = False
                            break
                        char_count[char] -= 1
                    elif fb == "gray":
                        green_yellow_elsewhere = any(
                            (c == char and fb2 in ["green", "yellow"]) for c, fb2 in zip(guess, feedback)
                        )
                        if char in word and not green_yellow_elsewhere:
                            valid = False
                            break

                        if green_yellow_elsewhere and char_count[char] > 0:
                            # Check for additional occurrences beyond green/yellow allowances
                            positions = [j for j, (c, fb2) in enumerate(zip(guess, feedback))
                                         if c == char and fb2 == "green"]
                            total_allowed = sum(word[j] == char for j in positions)
                            if char_count[char] > total_allowed:
                                valid = False
                                break
                if valid:
                    filtered_words.append(word)
            self.remaining_words = filtered_words

    def suggest_word(self):
        if not self.history:
            return "crane"
        return random.choice(self.remaining_words)
