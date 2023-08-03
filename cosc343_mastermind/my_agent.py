__author__ = "Jake Norton"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "norja159@student.otago.ac.nz"

import numpy as np
import itertools
from mastermind import evaluate_guess

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

        self.code_length = code_length
        self.colours = colours
        self.num_guesses = num_guesses
        self.all_codes = list(
            itertools.product(colours, repeat=code_length))
        self.possible_codes = self.all_codes
        # self.initial_colours = 2
        self.first_guess = self.generate_first_guess()
        self.last_guess = self.first_guess
        self.guess_count = 0
        self.in_colour = 0
        self.in_place = 0
        self.possible_colours = colours

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
            return self.first_guess

        if self.guess_counter == 1:
            self.print_state(percepts)
            self.generate_possible_codes()
            print(len(self.possible_codes))
            exit(0)
        return self.first_guess

    def generate_first_guess(self):
        guess = []
        for i in range(0, self.code_length):
            if i < self.code_length//2:
                guess.append(self.colours[0])
            else:
                guess.append(self.colours[1])
        return guess

    def generate_possible_codes(self):
        # if self.in_colour == 0 and self.in_place == 0:
        #     unique_colours = set(self.last_guess)
        #     for code in self.possible_codes:
                
        #     for colour in unique_colours:
        #         if colour in self.possible_colours:
        #             self.possible_colours = self.possible_colours.remove(colour)
        possible_codes = []
        for code in self.possible_codes:
            guess = evaluate_guess(self.last_guess, code)
            # print(guess, self.last_guess)
            if guess == (self.in_place, self.in_colour):
                 possible_codes.append(code)
        self.possible_codes = possible_codes
        
    def generate_non_symmetrical_first_guess(self):
        pass
    
    def get_unique_colours(self):
        unique_colours = set(self.last_guess)
        return len(unique_colours)

    def print_state(self, percepts):
        guess_counter, last_guess, in_place, in_colour = percepts
        print('count: ', guess_counter)
        print('in_place: ', in_place)
        print('in_colour: ', in_colour)
        print('last_guess: ', last_guess)
        print('self.unique_colours: ', self.get_unique_colours())
