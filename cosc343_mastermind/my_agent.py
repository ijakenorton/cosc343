__author__ = "Jake Norton"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "norja159@student.otago.ac.nz"

import numpy as np
import itertools
import random
# from evaluate import evaluate_guess
from mastermind import evaluate_guess
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
        self.first_codes = np.array(self.get_first_codes())
        self.code_length = code_length
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
        print(self.first_guess)
        print(len(self.possible_codes))
        exit(0)
        for code in tqdm(self.possible_codes):
            self.partition(code)
        choice = list(random.choice(self.possible_codes))
        return np.array(choice)

    def generate_possible_codes(self):
        possible_codes = []
        last_score = (self.in_place, self.in_colour)
        last_guess = np.array(self.last_guess)
        for code in self.possible_codes:
            guess = evaluate_guess(last_guess, code)
            if guess == last_score:
                possible_codes.append(code)
        self.possible_codes = possible_codes

    def get_first_codes(self):
        codes = []
        for i in range(0, len(self.non_symmetrical_first_guesses)):
            codes.append([])
            for j in range(0, len(self.non_symmetrical_first_guesses[i])):
                codes[i].append(
                    self.colours[self.non_symmetrical_first_guesses[i][j]])

        return codes

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

    def generate_first_guess(self):
        guess = []
        for i in range(0, self.code_length):
            if i < self.code_length//2:
                guess.append(self.colours[0])
            else:
                guess.append(self.colours[1])
        return guess

    def create_buckets(self):
        counts = {}
        for output in self.possible_outputs:
            counts[output] = 0
        return counts
    
    def partition(self, trial):
        counts = self.create_buckets()
        for code in self.possible_codes:
            output = evaluate_guess(code, trial)
            counts[output] += 1       
        # for key in counts:
        #     print("key: ",key,' length: ',counts[key])
        print(self.entropy(counts.values()))
# Start by picking a possible guess.

# Partition the set of all remaining possible true codes based on the feedback that would be received if the current guess were true. In other words, group together all codes that would give the same feedback. For example, you might have a group of codes that would all give feedback of "2 black pegs, 1 white peg", another group that would all give "1 black peg, 2 white pegs", etc.

# For each partition, calculate the probability of ending up in that partition if the current guess were made. This would just be the size of the partition (the number of codes in it) divided by the total number of remaining possible codes.

# Calculate the entropy of the resulting distribution over partitions. This is done in the same way as before: sum over all partitions (-P(partition) * log2(P(partition))).

# Repeat this process for each possible guess, and choose the guess that results in the highest entropy.

    def entropy(self, counts):
        
        probabilities = [count / len(self.possible_codes) for count in counts]

        entropy = -sum(p * log2(p) for p in probabilities if p > 0)
        return entropy
  # 'lengths' should be replaced with the list of all lengths.

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


#     return in_place, in_colour
    # def calc_first_guess_entropy(self):
    #     default_value = 0
    #     groups = {tuple(sublist): default_value for sublist in self.first_codes}
    #     for key in tqdm(groups):
    #         code = list(key)
    #         for target in tqdm(self.all_codes):
    #             last_score = evaluate_guess(code, target)
    #             for c in self.all_codes:
    #                 guess = evaluate_guess(code, c)
    #                 if guess == last_score:
    #                     groups[key] += 1
    #     for key in groups.keys():
    #         print(groups[key])


    def generate_non_symmetrical_first_guess(self):
        pass

    def print_state(self, percepts):
        guess_counter, last_guess, in_place, in_colour = percepts
        print('count: ', guess_counter)
        print('in_place: ', in_place)
        print('in_colour: ', in_colour)
        print('last_guess: ', last_guess)
