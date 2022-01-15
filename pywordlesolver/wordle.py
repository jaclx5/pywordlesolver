#!python

"""
Python only WORDLE solver
"""

import argparse
import copy
import math
import os
import re
import random
import sys

from collections import Counter
from functools import reduce

from pywordlesolver import strategies
from pywordlesolver import utils

WORD_FILE = os.path.join(os.path.dirname(__file__), "../data/words05.txt")


# To speed up the first run we precomputed the first try
MOST_INFORMATIVE_WORD_1 = "SAREE"
MOST_INFORMATIVE_WORD_2 = "TARES"



class WordleSolver:
    """
    Solves WORDLE games.

    To use this class:
        1/ Create a new instance of the class.
        2/ Call `next_try` method w/o parameters to get the first guess word.
        3/ Try the word in some game engine and obtain the response.
        4/ Call `next_try` method with the response obtained in the "gyx" notation (see below).
        5/ Repeat 3/ to 5/ until finishing.

    Attributes
    ----------
    words : list(str)
        list of words to use in the game
    fn_strategy : function
        any function that receives a list of words and returns a guess word.
        see `strategies.py` for some examples.
    first_word="" : str
        word to be played in the first try. Use this to speed up the games when playing many games.
        if empty the solver will chose the first word according to the defined strategy.
        defaults to "".

    Methods
    -------
    next_try(response=None):
        Returns the next word to be played. Keeps track of previous responses until finishing the
        game.
    """

    def __init__(self, words, fn_strategy, first_word=""):
        self._fn_strategy = fn_strategy
        self._original_words = words
        self._first_word = first_word

        self._state_reset()

    def _state_reset(self):
        """
        Resets the game state to start a new game (private method do not use it directly).

        THIS METHOD CHANGES THE STATE VARIABLES OF THE CLASS.
        """

        # this state variables (`_s_*`) will change during the game
        self._s_words = copy.copy(self._original_words)

        self._s_greens = [""] * 5
        self._s_yellows = [set() for _ in range(5)]
        self._s_grays = set()

        self._s_word_played = ""

    def _state_update(self, response):
        """
        Updates the game state based on the response clue and the previously played word (private
        method do not use it directly).

        THIS METHOD CHANGES THE STATE VARIABLES OF THE CLASS.
        """

        # compare each position of the response against the word played, update the state variables
        for i, (c, r) in enumerate(zip(self._s_word_played, response)):
            if r == "g":
                # test if the letter is compatible with previous responses
                assert (self._s_greens[i] in [c, ""]), f"Letter in position {i} must be {self._s_greens[i]}"
                assert (c not in self._s_yellows[i]) and (c not in self._s_grays), f"Letter in position {i} can't be {c}"

                # good letter! good position!
                self._s_greens[i] = c

            elif r == "y":
                # test if the letter is compatible with previous responses
                assert c not in self._s_grays, f"Letter in position {i} can't be {c}"

                # good letter! bad position!
                self._s_yellows[i].add(c)

            else:
                # bad letter!
                self._s_grays.add(c)

    def _remove_words(self):
        """
        Updates the list of words using all the clues received until now.

        THIS METHOD CHANGES THE STATE VARIABLES OF THE CLASS.
        """

        # compute the pattern expression taking into ount the information so far:
        pat = ""
        for (s, c) in zip(self._s_greens, self._s_yellows):
            if s != "":
                pat += s
            else:
                pat += f"[^{''.join(self._s_grays) + ''.join(c)}]"

        # removes the words that do not match the pattern
        self._s_words = list(filter(lambda w: re.match(pat, w), self._s_words))

        # the misplaced letters must exist in the word
        missplaced = reduce(lambda x, y: x | y, self._s_yellows)

        # remove the words that do not contain missplaced letters
        self._s_words = list(filter(lambda w: not (missplaced - set(w)), self._s_words))

    def next_try(self, response=""):
        """
        Returns the next word to try. Takes into account all previous responses.

        Reponses should be provided in the "gyx" notatio. For each position of the guess word, the
        i-th position of the response is a:
            - "g" - if the i-th letter of `guess` occurs in the i-th position `solution`.
            - "y" - if the i-th letter of `guess` occurs in `solution` but not in the i-th position.
            - "x" - if the i-th letter of `guess` does not occur in `solution`

        Parameters
        ----------
        response : str
            response to the previously played word. Leave empty if this is the first try.
            defaults to "".

        Returns
        -------
        string
            the guess word for the next try.
        """

        # THIS METHOD CHANGES THE STATE VARIABLES OF THE CLASS.

        first_try = (not response)

        if response == "ggggg":
            # it's solved!
            return True, ""

        """
        update the game state
        """
        if first_try:
            # in the first try start a complete new game
            self._state_reset()
        else:
            # update the game with the response to the last word played
            self._state_update(response)

            # remove all the words not part of the solution
            self._remove_words()

        """
        choose the next word to be played
        """
        if first_try and self._first_word:
            # if the `first_word` was pre-computed play it
            self._s_word_played = self._first_word
        else:
            # use the strategy to choose the first word to play
            self._s_word_played = self._fn_strategy(self._s_words)

        return False, self._s_word_played


def load_words(words_file):
    # get all the words in the Ubuntu american-english dictionary
    return open(words_file).read().strip().split("\n")


def interactive_solver(strategy):
    """
    Starts an interactive game solver.

    Parameters
    ----------
    strategy : str
        Name of the strategy to apply.
    """    
    print(f"""
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    Solving WORDLE with the '{args.strategy}' strategy.
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    Play the word suggested by the game in some game engine and type the response
    back.

    When typing WORDLE response use:
        - g - For right letter in the right place (green letters)
        - y - For right letter in the wrong place (yellow letters)
        - x - Wrong letters (gray letters)

    For example:
        If the solution is:   DRINK
        and we try:           FROND
        The response will be: xgxgy
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n
    """)

    solver = WordleSolver(load_words(WORD_FILE), fn_strategy=getattr(strategies, strategy))

    response = None
    n = 0

    while True:
        n += 1
        
        os.sys.stdout.write("\nWait for it...")
        os.sys.stdout.flush()

        finished, word = solver.next_try(response)

        print("\b" * 20 + " " * 20 + "\b" * 20)

        if finished:
            print(f"Done in {n} tries")
            break

        if not word:
            print(f"Can't solve it, sorry!\n\n")
            break

        print(f"Try #{n}: {word}\n")

        response = input("Response: ")

def interactive_player():
    """
    Starts an interactive game player.
    """    

    print(f"""
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    Play WORDLE
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    Try to find the word I chose.

    After typing your response you will get the following clues:
        - g - For right letter in the right place (green letters)
        - y - For right letter in the wrong place (yellow letters)
        - x - Wrong letters (gray letters)

    For example:
        If the solution is:   DRINK
        and we try:           FROND
        The response will be: xgxgy
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n
    """)

    words = load_words(WORD_FILE)

    # use the random strategy to get a random word
    solution = strategies.rnd(words)

    response = None
    n = 0

    import time

    while True:
        n += 1

        guess = ""
        while guess not in words:        
            print(f"\n== Try #{n:10d} ==")
            guess = input("Type your guess: ").upper()

            if guess not in words:
                print(f"\n{guess} is not a word, sorry")
                print(f"Try again, please")

        response = utils.compute_response(solution, guess)

        print(f"Result:          {response}")

        if response == "ggggg":
            print(f"Done in {n} tries!")
            break


def interactive_benchmark():
    strategies_to_benchmark = {
        'rnd': "Random",
        'mil': "Most Informative Letter",
        'miw': "Most Informative Word",
    }

    words = load_words(WORD_FILE)

    print(f"Benchmarking:")
    print(f"- {len(strategies_to_benchmark)} strategies.")
    print(f"- {len(words)} words.")

    for strategy, name in strategies_to_benchmark.items():
        print("\n\n" + "-" * 60)
        print(f"Testing the '{name}' strategy:")
        print("-" * 60)

        fn_strategy = getattr(strategies, strategy)

        # get the first word to be reused (it saves a lot of time)
        first_word = fn_strategy(words)

        counts = []
        not_solved = 0
        max_tries = 0
        max_word = ""

        for i, solution in enumerate(words):
            sys.stdout.write('\b' * 20 + f"working: {int(i/len(words)*100)}%")
            sys.stdout.flush()

            solver = WordleSolver(words, fn_strategy=fn_strategy, first_word=first_word)
            response = None

            count = 0

            while response != "ggggg":
                finished, word = solver.next_try(response)
                response = utils.compute_response(solution, word)

                count += 1

            if count > 6:
                not_solved += 1

            if count > max_tries:
                max_tries = count
                max_word = solution

            counts.append(count)
        
        print('\b' * 20 + f"Count of words solved in # tries:")
        
        cnt = Counter(counts)
        
        x, c = 0, 0
        for k in sorted(cnt):
            x += k * cnt[k]
            c += cnt[k]

            print(f"{k:2d}: {'=' * (int(cnt[k]/40) + 1)} {cnt[k]}")

        print(f"\nAverage number of tries:       {x/c:6.3f}")
        print(f"Puzzles not solved in 6 tries: {not_solved} ({not_solved / len(words) * 100:5.1f}%)")
        print(f"The most difficult word '{max_word}' required {max_tries} tries.")

#
# Main
#

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solve / Play / Benchmark WORDLE.')
    parser.add_argument('mode', type=str, help='game mode: solve, play, benchmark')
    parser.add_argument('strategy', type=str, nargs='?', default="miw", help='Play strategy: rnd, mil, miw (default)')
    args = parser.parse_args()

    if args.mode == "solve":
        interactive_solver(args.strategy)
    elif args.mode == "play":
        interactive_player()
    elif args.mode == "benchmark":
        interactive_benchmark()
    else:
        print("Unknown mode try: solve / play")
