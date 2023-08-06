__author__ = "Jake Norton"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "norja159@student.otago.ac.nz"

import numpy as np
import itertools
import random
from evaluate import evaluate_guess
# from mastermind import evaluate_guess
from tqdm import tqdm
import multiprocessing as mp
from multiprocessing import Pool
from math import log2


class MastermindAgent():
    """
             A class that encapsulates the code dictating the
             behaviour of the agent playing the game of Mastermind.

             ...

             Attributes
             ----------
             code_length: int
                 the length of the code to guess
             colours : list of char
                 a list of colours represented as characters
             num_guesses : int
                 the max. number of guesses per game

             Methods
             -------
             AgentFunction(percepts)
                 Returns the next guess of the colours on the board


             """

    def __init__(self, code_length,  colours, num_guesses):
        """
        :param code_length: the length of the code to guess
        :param colours: list of letter representing colours used to play
        :param num_guesses: the max. number of guesses per game
        """
        self.colours = colours
        self.non_symmetrical_first_guesses = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 1],
            [0, 0, 1, 1, 2],
            [0, 1, 1, 1, 2],
            [0, 1, 1, 2, 2],
            [0, 1, 1, 2, 3],
            [0, 1, 2, 3, 4]
        ]
        self.code_length = code_length
        self.first_codes = np.array(self.get_first_codes())
        self.num_guesses = num_guesses
        self.all_codes = np.array(list(
            itertools.product(colours, repeat=code_length)))
        possible_outputs = (list(filter(lambda x: sum(
            x) <= code_length, itertools.product(range(code_length+1), repeat=2))))
        
        self.possible_outputs = []
        for output in possible_outputs:
            self.possible_outputs.append(tuple(output))
            
        self.possible_codes = self.all_codes
        self.first_guess = self.first_codes[3]
        self.last_guess = self.first_guess
        self.guess_count = 0
        self.in_colour = 0
        self.in_place = 0

    def AgentFunction(self, percepts):
        """Returns the next board guess given state of the game in percepts

              :param percepts: a tuple of four items: guess_counter, last_guess, in_place, in_colour

                       , where

                       guess_counter - is an integer indicating how many guesses have been made, starting with 0 for
                                       initial guess;

                       last_guess - is a num_rows x num_cols structure with the copy of the previous guess

                       in_place - is the number of character in the last guess of correct colour and position

                       in_colour - is the number of characters in the last guess of correct colour but not in the
                                   correct position

              :return: list of chars - a list of code_length chars constituting the next guess
              """

        # Extract different parts of percepts.
        self.guess_counter, self.last_guess, self.in_place, self.in_colour = percepts

        if self.guess_counter == 0:
            self.last_guess = self.first_guess
            self.guess_count = 0
            self.in_colour = 0
            self.in_place = 0
            self.possible_codes = self.all_codes

            return self.first_guess

        self.generate_possible_codes()
        if len(self.possible_codes) > 500:
            sample_size = int(0.20 * len(self.possible_codes))
            entropies = []
            indices = np.random.choice(self.possible_codes.shape[0], sample_size, replace=False)
            with Pool(mp.cpu_count()) as p:
                entropies = list(p.map(self.partition, self.possible_codes[indices]))
        else:
            entropies = []
            with Pool(mp.cpu_count()) as p:
                entropies = list(p.map(self.partition, self.possible_codes))

        # max_entropy = entropies.index(max(entropies))
        max_entropy = entropies.index(max(entropies))
        choice = self.possible_codes[max_entropy]
        return choice

    def generate_possible_codes(self):
        # Initialize an array of maximum size (equal to the number of possible codes).
        # We will truncate this array at the end.
        possible_codes = np.empty((len(self.possible_codes), len(self.last_guess)), dtype='<U1')
        last_score = (self.in_place, self.in_colour)
        last_guess = np.array(self.last_guess)

        i = 0
        for code in self.possible_codes:
            guess = evaluate_guess(last_guess, code)
            if guess == last_score:
                possible_codes[i] = code
                i += 1

        # Truncate the array to the number of codes that matched the score.
        self.possible_codes = possible_codes[:i]


    def get_first_codes(self):
        groupings = []
        for partition in unique_partitions(self.code_length):
            groupings.append(partition)
        print(groupings)
        return groupings


    def calc_first_guess_entropy(self):
        # create a list of tuples containing the key and other necessary parameters
        keys_with_params = [(tuple(sublist), self.all_codes)
                            for sublist in self.first_codes]

        # Start multiprocessing pool and map function
        with Pool(mp.cpu_count()) as p:
            result = list(
                tqdm(p.imap(evaluate_key, keys_with_params), total=len(keys_with_params)))

        # Combine the results
        groups = {k: v for res in result for k, v in res.items()}

        # Print the results
        for key in groups.keys():
            print(groups[key])
        calc_entropy(groups)


    def create_buckets(self):
        return {output: 0 for output in self.possible_outputs}

    def partition(self, trial):
        counts = self.create_buckets()
        for code in self.possible_codes:
            output = evaluate_guess(code, trial)
            counts[output] += 1
        return self.entropy(counts.values())

    def entropy(self, counts):
        probabilities = [count / len(self.possible_codes) for count in counts]
        entropy = -sum(p * log2(p) for p in probabilities if p > 0)
        return entropy

def unique_partitions(n):
# Base case of recursion: zero is the sum of the empty list
    if n == 0:
        yield []
        return
        
    # Modify partitions of n-1 to form partitions of n
    for p in unique_partitions(n-1):
        yield [1] + p
        if p and (len(p) < 2 or p[1] > p[0]):
            yield [p[0] + 1] + p[1:]


def calc_entropy(groups):
    total_count = sum(groups.values())
    probabilities = {key: count / total_count for key, count in groups.items()}
    # Compute the entropy for each key
    entropies = {key: -p * np.log2(p) if p >
                 0 else 0 for key, p in probabilities.items()}
    # Print the entropies
    for key, entropy in entropies.items():
        print(f"Key: {key}, Entropy: {entropy}")


def evaluate_key(args):
    key, all_codes = args
    groups = {key: 0}
    code = np.array(key)
    for target in tqdm(all_codes):
        last_score = evaluate_guess(code, target)
        for c in all_codes:
            guess = evaluate_guess(code, c)
            if guess == last_score:
                groups[key] += 1
    return groups
