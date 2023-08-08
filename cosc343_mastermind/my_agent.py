

__author__ = "Jake Norton"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "norja159@student.otago.ac.nz"

import numpy as np
import itertools
import random
from mastermind import evaluate_guess
import multiprocessing as mp
from multiprocessing import Pool
from math import log2
from concurrent.futures import ProcessPoolExecutor


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

        self.sample = 0.6
        self.lower_bound = 900
        self.code_length = code_length
        self.first_codes = (self.get_first_codes(self.code_length))
        self.num_guesses = num_guesses
        self.all_codes = np.array(list(
            itertools.product(colours, repeat=code_length)))
        possible_outputs = (list(filter(lambda x: sum(
            x) <= code_length, itertools.product(range(code_length+1), repeat=2))))

        self.possible_outputs = []
        for output in possible_outputs:
            self.possible_outputs.append(tuple(output))

        self.possible_codes = self.all_codes
        self.first_guess = self.first_codes[2]
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
            self.reset_game()

            return self.first_guess
        self.generate_possible_codes()
        choice = (self.calculate_entropies())

        return choice

    def reset_game(self):
        """
        Resets the game state to its initial conditions.

        :attribute last_guess: Resets to the value of the first guess.
        :attribute guess_count: Resets the number of guesses made to 0.
        :attribute in_colour: Resets the number of pins that have the correct color but are out of place.
        :attribute in_place: Resets the number of pins that are both the correct color and in the correct position.
        :attribute possible_codes: Resets to the list of all possible codes.
        """

        self.last_guess = self.first_guess
        self.guess_count = 0
        self.in_colour = 0
        self.in_place = 0
        self.possible_codes = self.all_codes

    def generate_possible_codes(self):
        """
        Generate a list of possible codes based on the score of the last guess.

        This function evaluates each code from the existing set of possible codes 
        against the last guess. If the score from this evaluation matches the 
        score of the last guess, then that code is still a possible solution and 
        is retained in the possible codes list.

        Attributes:
            possible_codes (numpy array): An array to store possible codes.
            last_score (tuple): The score of the last guess.
            last_guess (numpy array): The last guess made.
        """

        # Initialize an array of maximum size (equal to the number of possible codes).
        # We will truncate this array at the end.
        possible_codes = np.empty(
            (len(self.possible_codes), len(self.last_guess)), dtype='<U1')
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

    def calculate_entropies(self):
        """
        Calculate entropies for possible codes. If the number of possible codes exceeds a threshold (self.lower_bound),
        a random sample is taken and entropy is calculated for this sample.

        Attributes:
            self.possible_codes (np.array): An array of potential codes.
            self.lower_bound (int): The threshold for determining when to sample.
            self.sample (float): Proportion of possible codes to be used in the sampling.

        Returns:
            np.array: Code with the maximum entropy.
        """
        if len(self.possible_codes) > self.lower_bound:
            sample_size = int(self.sample * len(self.possible_codes))

            indices = np.random.choice(
                self.possible_codes.shape[0], sample_size, replace=False)
            sampled = self.possible_codes[indices]
            entropies = self.get_entropies(sampled)
            max_entropy = np.argmax(entropies)
            return sampled[max_entropy]
        else:
            entropies = self.get_entropies(self.possible_codes)
            max_entropy = np.argmax(entropies)
            return self.possible_codes[max_entropy]

    def get_entropies(self, codes):
        """
        Calculate the entropies for the given codes using parallel processing.

        Args:
            codes (np.array): An array of codes for which entropies are to be calculated.

        Returns:
            list: List of entropies for the given codes.
        """
        with ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
            entropies = list(executor.map(self.partition, codes))

        return entropies

    def partition(self, trial):
        """
        Partition a given trial code based on how many of the possible codes would produce each possible output.

        Args:
            trial (np.array): The code to be evaluated.

        Attributes:
            self.possible_outputs (list): List of possible outputs that can be generated.

        Returns:
            float: Entropy of the partitioned trial.
        """
        counts = {output: 0 for output in self.possible_outputs}
        for code in (self.possible_codes):
            output = evaluate_guess(code, trial)
            counts[output] += 1
        return self.entropy(counts.values())

    def entropy(self, counts):
        """
        Calculate the Shannon entropy for the given counts.

        Args:
            counts (list): List of counts for different partitions.

        Attributes:
            self.possible_codes (np.array): An array of potential codes.

        Returns:
            float: Calculated entropy.
        """
        probabilities = [count / len(self.possible_codes) for count in counts]
        entropy = -sum(p * log2(p) for p in probabilities if p > 0)
        return entropy

    def get_first_codes(self, code_length):
        """
        Generate first set of codes based on the code length.

        Args:
            code_length (int): Length of the code to be generated.

        Returns:
            list: List of initial codes based on the code length.
        """
        groupings = []
        for partition in unique_partitions(code_length):
            groupings.append(partition)
        return self.groupings_to_codes(groupings)

    def groupings_to_codes(self, groupings):
        """
        Convert groupings into actual codes using the color set.

        Args:
            groupings (list): List of groupings to be converted.

        Attributes:
            self.colours (list): List of available colors.

        Returns:
            list: List of codes generated from the groupings.
        """
        codes = []
        for grouping in groupings:
            color_index = 0  # Start from the first color
            code = []
            for group_size in grouping:
                code.extend([self.colours[color_index]] * group_size)
                color_index += 1  # Move to the next color for the next group
            codes.append(code)
        return codes

    def calc_first_guess_entropy(self):
        """
        Calculate the Shannon entropy for the first set of guesses.

        Attributes:
            self.colours (list): List of available colors.

        Returns:
            list: List of entropy values for the first set of guesses.
        """
        all_entropies = []
        for i in range(3, 4):
            first_codes = self.get_first_codes(i)
            all_codes = np.array(list(
                itertools.product(self.colours, repeat=i)))
        #    create a list of tuples containing the key and other necessary parameters
            keys_with_params = [(tuple(sublist), all_codes)
                                for sublist in first_codes]

            # Start multiprocessing pool and map function
            with Pool(mp.cpu_count()) as p:
                result = list(
                    p.map(evaluate_key, keys_with_params))

            # Combine the results
            groups = {k: v for res in result for k, v in res.items()}

            entropy = calc_entropy(groups)
            for key in entropy:
                print(key, entropy[key])
            print('***********************************************')
            all_entropies.append(entropy)
        return all_entropies


def unique_partitions(n):
    """
    Generate all unique partitions of an integer.

    A partition of a positive integer `n` is a way of writing `n` as a sum of positive integers.
    This function yields all unique partitions in ascending lexicographic order.

    Args:
        n (int): The integer to be partitioned.

    Yields:
        list: A unique partition of the integer n.

    Examples:
        >>> list(unique_partitions(4))
        [[1, 1, 1, 1], [2, 1, 1], [2, 2], [3, 1], [4]]

        >>> list(unique_partitions(3))
        [[1, 1, 1], [2, 1], [3]]
    """
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
    """
    Calculate the Shannon entropy for the given groups.

    Args:
        groups (dict): Dictionary with keys as codes and values as their corresponding frequencies.

    Returns:
        dict: Dictionary with keys as codes and their corresponding entropy values.
    """
    total_count = sum(groups.values())
    probabilities = {key: count / total_count for key, count in groups.items()}
    # Compute the entropy for each key
    entropies = {key: -p * np.log2(p) if p >
                 0 else 0 for key, p in probabilities.items()}
    # Print the entropies

    return entropies


def evaluate_key(args):
    """
    Evaluate the given key (or code) to produce some score or output.

    Args:
        keys_with_params (tuple): Contains the key and other parameters for evaluation.

    Returns:
        dict: Dictionary with the key and its corresponding evaluation output.
    """
    key, all_codes = args
    groups = {key: 0}
    code = np.array(key)
    for target in (all_codes):
        last_score = evaluate_guess(code, target)
        for c in all_codes:
            guess = evaluate_guess(code, c)
            if guess == last_score:
                groups[key] += 1
    return groups
