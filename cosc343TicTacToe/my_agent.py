__author__ = "Lech Szymanski"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "lech.szymanski@otago.ac.nz"

# Import the random number generation library
import random
import numpy as np
from cosc343TicTacToe import maxs_possible_moves, mins_possible_moves, terminal, evaluate, state_change_to_action, remove_symmetries

class TicTacToeAgent():
    """
           A class that encapsulates the code dictating the
           behaviour of the TicTacToe playing agent

           Methods
           -------
           AgentFunction(percepts)
               Returns the move made by the agent given state of the game in percepts
           """

    def __init__(self, h):
        """Initialises the agent

        :param h: Handle to the figures showing state of the board -- only used
                  for human_agent.py to enable selecting next move by clicking
                  on the matplotlib figure.
        """
        pass



    def AgentFunction(self, percepts):
        """The agent function of the TicTacToe agent -- returns action
         relating the row and column of where to make the next move

        :param percepts: the state of the board a list of rows, each
        containing a value of three columns, where 0 identifies the empty
        suare, 1 is a square with this agent's mark and -1 is a square with
        opponent's mark
        :return: tuple (r,c) where r is the row and c is the column index
                 where this agent wants to place its mark
        """
        best_move = None
        best_evaluation = float('-inf')
        for move in remove_symmetries(maxs_possible_moves(percepts)):
            evaluation = self.solve(move, 3, False)
            if evaluation > best_evaluation:
                best_evaluation = evaluation
                best_move = move
        
        r,c = state_change_to_action(percepts,best_move)
        return (r,c)
            
    def solve(self , state, depth, max_player):
        global saved_moves
        if depth == 0 or terminal(state) == True:
            return evaluate(state)
        
        if max_player:
            max_evaluation = float('-inf')
            beta = float('-inf')
            count = 0
            moves = remove_symmetries(maxs_possible_moves(state))
            for move in moves :
                count += 1
                evaluation = self.solve(move, depth-1, False) 
                if evaluation < beta:
                    break
                max_evaluation = max(max_evaluation, evaluation) 
                beta = max_evaluation
            return max_evaluation
        if not max_player:
            min_evaluation = float('inf')
            alpha = float('inf')
            count = 0
            moves = remove_symmetries(mins_possible_moves(state))
            for move in moves :
                count += 1
                evaluation = self.solve(move, depth-1, True)
                if evaluation > alpha:
                    break 
                min_evaluation = min(min_evaluation, evaluation)    
                alpha = min_evaluation     
            
            return min_evaluation
        
        


