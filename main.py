from sys import __stdin__, stderr, stdout, platform
from os import environ
from time import monotonic
from random import getrandbits, choices
from re import sub

if __stdin__.isatty():
    from pytimedinput import timedInput
else:
    from threading import Timer

    print('This game was intended to be played in an interactive shell.', file=stderr)

def supports_color():
    # supported_platform = platform != 'Pocket PC' and (platform != 'win32' or 'ANSICON' in environ)
    # is_a_tty = hasattr(stdout, 'isatty') and stdout.isatty()
    # return supported_platform and is_a_tty

    # TODO: detect if terminal supports ANSI escape codes

    return True
class bcolors:
    if supports_color():
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
    else:
        HEADER = ''
        OKBLUE = ''
        OKCYAN = ''
        OKGREEN = ''
        WARNING = ''
        FAIL = ''
        ENDC = ''
        BOLD = ''
        UNDERLINE = ''


class DictionaryGame:

    def __init__(self, difficulty: str):
        self.FR_DICT: set = set(line.strip() for line in open('en_dict.txt'))
        self.LETTERS: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.TIME_TO_ANSWER: int = 15  # DEBUG PURPOSES
        self.difficulty: str = difficulty
        self.score: int = 1
        self.high_score: int = 1

        self.__dict_difficulty_points = {
            'easy': 7,
            'medium': 8,
            'hard': 9
        }
        self.points_to_win: int = self.__dict_difficulty_points[self.difficulty]
        self.__max_points_to_win: int = 15

    def get_random_letters(self):
        dict_difficulty_length = {'easy': 10, 'medium': 9, 'hard': 8}
        number_of_letters = dict_difficulty_length[self.difficulty] + getrandbits(1)
        # each 'weight' is associated with an index in the self.LETTERS attribute
        # TODO: find a more elegant way to associate a letter with a weight
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

    @staticmethod
    def string_sanitize(word: str):
        word = sub(r'[àáâãäå]', 'a', word)
        word = sub(r'[èéêë]', 'e', word)
        word = sub(r'[ìíîï]', 'i', word)
        word = sub(r'[òóôõö]', 'o', word)
        word = sub(r'[ùúûü]', 'u', word)
        word = word.upper()
        word = sub(r'[^A-Z]', '', word)
        return word

    def increment_score(self):
        self.score += 1

    def increment_points_to_win(self):
        if self.points_to_win < self.__max_points_to_win:
            self.points_to_win += 1

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
        CORRECTION_CONST = 10
        sum_valid_words_length = 0
        for word in self.FR_DICT:
            if self.verify_response_in_letters(letters, word):
                sum_valid_words_length += len(word)
                if sum_valid_words_length >= (self.points_to_win + CORRECTION_CONST):
                    return True
        return False

    def turn(self):
        CORRECTION_TIME = 0.1  # this will be added to avoid calling the timedInput function with low timeout
        points_scored = 0
        letters = self.get_random_letters()
        BEST_SOLUTION = self.get_best_solution(letters)
        finish_time = monotonic() + self.TIME_TO_ANSWER  # self.TIME_TO_ANSWER
        print(f'Round: {bcolors.BOLD}{self.score}{bcolors.ENDC}')
        input(f'Press {bcolors.BOLD}ENTER{bcolors.ENDC} to start round {bcolors.BOLD}{self.score}{bcolors.ENDC}...\n')
        print(f'Submit words with the letters: {bcolors.OKBLUE}{", ".join(letters)}{bcolors.ENDC}:')
        print(f'The best solution has {bcolors.OKBLUE}{len(BEST_SOLUTION)}{bcolors.ENDC} letters.')
        if __stdin__.isatty():
            while monotonic() <= finish_time:
                submitted_word, _ = timedInput(prompt='$ ', timeout=(finish_time - monotonic() + CORRECTION_TIME),
                                               resetOnInput=True, endCharacters="\x1b\n\r")
                if submitted_word:
                    submitted_word = self.string_sanitize(submitted_word)
                    if self.verify_response_in_letters(letters, submitted_word):
                        if self.verify_response_in_dictionary(submitted_word):
                            print(f'{len(submitted_word)} points!')
                            points_scored += len(submitted_word)
                        else:
                            print(f'Not in the dictionnary')
                    else:
                        print(f'Invalid letters.')
            print(f"{bcolors.WARNING}* Time's up!{bcolors.ENDC}\n")
        else:
            t = Timer(self.TIME_TO_ANSWER, print, [f"\n{bcolors.WARNING}* Time's up!{bcolors.ENDC}\n"])
            t.start()
            while monotonic() <= finish_time:
                submitted_word = input('$ ')
                if submitted_word:
                    submitted_word = self.string_sanitize(submitted_word)
                    if self.verify_response_in_letters(letters, submitted_word):
                        if self.verify_response_in_dictionary(submitted_word):
                            print(f'{bcolors.OKGREEN}{len(submitted_word)} points!{bcolors.ENDC}')
                            points_scored += len(submitted_word)
                        else:
                            print(f'{bcolors.FAIL}Not in the dictionnary{bcolors.ENDC}')
                    else:
                        print(f'{bcolors.FAIL}Invalid letters.{bcolors.ENDC}')

        if points_scored >= self.points_to_win:
            print(f'You scored {points_scored} points and beat round {self.score}!')
            print(f'The best solution was {BEST_SOLUTION}')
            self.increment_score()
            self.increment_points_to_win()
            print('\n')
            self.turn()
        else:
            print(f'{bcolors.WARNING}Game Over :({bcolors.ENDC}\nYou scored {bcolors.BOLD}{points_scored}/{self.points_to_win} points{bcolors.ENDC}!')
            print(f'The best solution is {bcolors.OKBLUE}{BEST_SOLUTION}{bcolors.ENDC}\n')
            self.game_over()

    def game_over(self):
        if self.score > self.high_score:
            self.high_score = self.score
            print(f'New high score, you went to round {self.high_score}.')
        else:
            print(f'You beat {self.score} round{"" if self.score <= 1 else "s"}\n')
        input(f'Press {bcolors.BOLD}ENTER{bcolors.ENDC} to start a new game...\n')
        self.new_game()

    def new_game(self):
        self.score = 1
        self.points_to_win = self.__dict_difficulty_points[self.difficulty]
        self.turn()


if __name__ == '__main__':
    game = DictionaryGame('easy')
    game.new_game()
