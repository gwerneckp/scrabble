from time import monotonic
from random import getrandbits, choices
from pytimedinput import timedInput

class DictionaryGame:

    def __init__(self, difficulty: str):
        self.FR_DICT: set = set(line.strip() for line in open('dict.txt'))
        self.LETTERS: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.TIME_TO_ANSWER: int = 60
        self.difficulty: str = difficulty

    def get_random_letters(self):
        dict_difficulty = {'easy': 10, 'medium': 9, 'hard': 8}
        number_of_letters = dict_difficulty[self.difficulty] + getrandbits(1)
        # each 'weight' is associated with an index in the self.LETTERS attribute
        # TO-DO: find a more elegant way to associate a letter with a weight
        random_letters = choices(self.LETTERS,
                                 weights=(711, 113, 318, 367, 1210, 111, 123,
                                          111, 659, 34, 28, 496, 262, 639, 501,
                                          249, 65, 607, 651, 592, 449, 111, 17,
                                          38, 46, 15),
                                 k=number_of_letters)
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

    def get_best_solution(self, letters: list):
        len_looking: int = 0
        current_best_solution: str = ''
        for word in self.FR_DICT:
            if len_looking < len(word) <= len(letters):
                if self.verify_response_in_letters(letters, word):
                    current_best_solution = word
                    len_looking = len(current_best_solution)
        return current_best_solution

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
        TIME_TURN = 5
        CORRECTION_TIME = 0.1 #this will be added to avoid calling the timedInput function with low timeout
        points_scored = 0
        letters = self.get_random_letters()
        finish_time = monotonic() + TIME_TURN  # self.TIME_TO_ANSWER
        print(f'Écrit des mots avec les lettres {letters}:')
        while monotonic() <= finish_time:
            submitted_word, _ = timedInput(prompt='$ ', timeout=(finish_time-monotonic()+CORRECTION_TIME), resetOnInput=True, endCharacters="\x1b\n\r")
            if submitted_word:
                submitted_word = submitted_word.upper()
                if self.verify_response_in_letters(letters, submitted_word):
                    if self.verify_response_in_dictionary(submitted_word):
                        print(f'{len(submitted_word)} points!')
                        points_scored += len(submitted_word)
                    else:
                        print(f'Not in the dictionnary')
                else:
                    print(f'Invalid letters.')
        print(f'You scored {points_scored} points!')
        print(f'The best solution is {self.get_best_solution(letters)}')


if __name__ == '__main__':
    game = DictionaryGame('easy')
    game.turn()
