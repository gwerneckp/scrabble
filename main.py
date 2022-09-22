import time
from random import randrange, getrandbits


class DictionaryGame:
    def __init__(self, difficulty: str):
        self.FR_DICT: set = set(line.strip() for line in open('dict.txt'))
        self.LETTERS: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.TIME_TO_ANSWER: int = 60
        self.difficulty: str = difficulty

    def get_random_letters(self):
        dict_difficulty = {
            'easy': 9,
            'medium': 8,
            'hard': 7
        }
        number_of_letters = dict_difficulty[self.difficulty] + getrandbits(1)
        random_letters = []
        for _ in range(number_of_letters):
            random_letters.append(self.LETTERS[randrange(0, len(self.LETTERS))])
        if not self.are_letters_suitable(random_letters):
            return self.get_random_letters()
        return random_letters

    @staticmethod
    def verify_response_in_letters(letters: list, word: str):
        letters_copy = letters.copy()
        for letter_in_word in word:
            is_in_list = False
            for letter_in_list in letters_copy:
                if letter_in_word == letter_in_list:
                    is_in_list = True
                    letters_copy.remove(letter_in_word)
                    break
                else:
                    continue
            if not is_in_list:
                return False
        return True

    def verify_response_in_dictionary(self, word: str):
        if word in self.FR_DICT:
            return True
        else:
            return False

    # def get_best_solution(self, letters: list):
    #     len_looking: int = 0
    #     current_best_solution: str = ''
    #     for word in self.FR_DICT:
    #         if len_looking < len(word) < len(letters):
    #             if self.verify_response_in_letters(letters, word):
    #                 current_best_solution = word
    #     return current_best_solution

    # this method will return False if there are not at least 5 word possibilities in the letter selection
    def are_letters_suitable(self, letters: list):
        valid_word_count = 0
        for word in self.FR_DICT:
            if self.verify_response_in_letters(letters, word):
                valid_word_count += 1
                if valid_word_count >= 5:
                    return True
        return False

    def turn(self):
        letters = self.get_random_letters()
        finish_time = time.monotonic() + 10  # self.TIME_TO_ANSWER
        print(f'Écrit des mots avec les lettres {letters}:')
        while time.monotonic() <= finish_time:
            submitted_word = input('$ ')
            if (self.verify_response_in_letters(letters, submitted_word) and self.verify_response_in_dictionary(
                    submitted_word)):
                print(f'{len(submitted_word)} points!')
            else:
                print(f'Invalid word.')
        # print(f'The best solution is {self.get_best_solution(letters)}')


if __name__ == '__main__':
    game = DictionaryGame('medium')
    print(game.get_best_solution(['A', 'U', 'R', 'A', 'S']))
    # game.turn()