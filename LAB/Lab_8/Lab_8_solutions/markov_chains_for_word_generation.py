# Prompts the user to input two positive integers n and N,
# and outputs N words generated by a Markov chain where
# a dictionary file determines the probability that an n-gram
# be followed by this or that character (including the "end-of-word" character).
#
# Written by Eric Martin for COMP9021


from collections import defaultdict, Counter
from random import random
import sys


dictionary_file = 'dictionary.txt'


def compute_markov_chain(words, n):
    counts = Counter((word[i: i + n], word[i + n]) for word in words for i in range(len(word) - n))
    # Include m-grams for m < n (with the particular case of m = 0, to determine the probablity
    # that this or that letter starts a word).
    counts.update((word[: i], word[i]) for word in words for i in range(min(n, len(word))))
    grams = {gram_next_c[0] for gram_next_c in counts}
    totals_for_grams = defaultdict(int)
    for gram_next_c in counts:
        totals_for_grams[gram_next_c[0]] += counts[gram_next_c]
    markov_chain = {}
    for (gram, c) in counts:
        if gram in markov_chain:
            markov_chain[gram].append((c, counts[gram, c] + markov_chain[gram][-1][1]))
        else:
            markov_chain[gram] = [(c, counts[gram, c])]
    return {gram: [(c, count / totals_for_grams[gram]) for (c, count) in markov_chain[gram]]
                                                                                for gram in markov_chain}
    

def generate_word(words, markov_chain, n):
    word = ''
    while True:
        word_end = word[-n: ]
        p = random()
        # Last cumulative proba should be 1, it is ignored for the case
        # it is wrongly computed as smaller to 1.
        for (c, cumulative_proba) in markov_chain[word_end][: -1]:
            if p < cumulative_proba:
                word += c
                break
        else:
            word += markov_chain[word_end][-1][0]
        if word[-1] == '\n':
            return word
        
          
try:
    with open(dictionary_file) as dictionary:
        # We keep the ending new line character to play the role of "end-of-word" character.
        words = set(dictionary)
        while True:
            try:
                n = int(input('What n to use to let an n-gram determine the next character? '))
                if n <= 0:
                    raise ValueError
                break
            except ValueError:
                print('Incorrect input, try again.')               
        cumulative_probabilities = compute_markov_chain(words, n)
        while True:
            try:
                nb_of_words = int(input('How many words do you want to generate? '))
                if n < 0:
                    raise ValueError
                break
            except ValueError:
                print('Incorrect input, try again.')
        for _ in range(nb_of_words):
            word = generate_word(words, cumulative_probabilities, n)
            if word in words:
                print('Rediscovered', word[: -1])
            else:
                print('Invented', word[: -1])
except FileNotFoundError:
    print('Could not open {}. Giving up...'.format(dictionary_file))
    sys.exit()
