"""
A strategy is an word chooser algorithm.

Given the list of possible words it chooses the "best" according to some criteria.
"""

import math
import random

from collections import Counter

from pywordlesolver import utils

LETTER_NUM = 5
ALL_LETTERS = list(map(chr, range(65, 91))) # all letters A-Z


def rnd(words):
    """
    Picks a random word from the list.

    Parameters
    ----------
    words : list of str
        list of valid words.

    Returns
    -------
    string
        the guess word.
    """

    return random.sample(words, 1)[0] if words else ""


def mil(words):
    """
    Picks the word that maximizes the sum of information (SI) of each letter. The SI is computed
    independently for each letter.

    Parameters
    ----------
    words : list of str
        list of valid words.

    Returns
    -------
    string
        the guess word.
    """

    # "+1" to avoid log2(0)
    N = len(words) + 1

    # compute the most informative letter for each position
    imap = []

    for i in range(5):
        ichar = {}
        
        for c in ALL_LETTERS:
            # "+1" to avoid log2(0) 
            (g, y, x) = (1, 1, 1)
            
            for w in words:
                if w[i] == c:
                    g += 1
                elif c in w:
                    y += 1
                else:
                    x += 1
            
            pg, py, px = g/N, y/N, x/N
            ichar[c] = -(pg * math.log2(pg) + py * math.log2(py) + px * math.log2(px))
        
        imap.append(ichar)

    # compute the word with the maximum sum of informative letters
    max_i = 0
    max_w = ""

    for w in words:
        inf = sum([imap[i][c] for i, c in enumerate(w)])
        if inf > max_i:
            max_i, max_w = inf, w

    return max_w


def miw(words):
    """
    Picks the most informative word from the list.

    Parameters
    ----------
    words : list of str
        list of valid words.

    Returns
    -------
    string
        the guess word.
    """

    N = len(words)

    max_i = 0
    max_w = ""

    for guess in words:
        resps = []
        
        for solution in words:
            resps.append(utils.compute_response(solution, guess))
        
        inf = 0
        for count in Counter(resps).values():
            inf += -math.log2(count/N) * (count/N)
        
        if inf >= max_i:
            max_i, max_w = inf, guess

    return max_w