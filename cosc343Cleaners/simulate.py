import numpy as np
from settings import game_settings

# Constants
LEFT = -1
RIGHT = 1
GRID_SIZE = (10, 10)
ROWS, COLS = GRID_SIZE
ORIGIN = [int(ROWS / 2), int(COLS / 2)]
NUM_MOVES = 10
NORTH, EAST, SOUTH, WEST = [-1, 0], [0, 1], [1, 0], [0, -1]
DIRECTIONS = [NORTH, EAST, SOUTH, WEST]

np.random.seed(0)
np.set_printoptions(threshold=np.inf)

class Cleaner:

    def __init__(self):
        self.previous_action = 0
        self.direction = 0
        self.coordinates = ORIGIN.copy()
        self.map = np.zeros(GRID_SIZE)
        self.map[tuple(self.coordinates)] += 1

    def _wrap_coordinate(self, coord, max_value):
        return (coord % max_value + max_value) % max_value

    def move(self, move):
        
        if move == 0:
            # print("yo", move, DIRECTIONS[self.direction], self.coordinates)
            self.coordinates = list(np.array(self.coordinates) + np.array(DIRECTIONS[self.direction]))
            # print("coordinates", self.coordinates)
            self.coordinates = [self._wrap_coordinate(self.coordinates[0], ROWS),
                                self._wrap_coordinate(self.coordinates[1], COLS)]
        if move == 3:
            # print("yo", move, DIRECTIONS[self.direction], self.coordinates)
            self.coordinates = list(np.array(self.coordinates) - np.array(DIRECTIONS[self.direction]))
            # print("coordinates", self.coordinates)
            self.coordinates = [self._wrap_coordinate(self.coordinates[0], ROWS),
                                self._wrap_coordinate(self.coordinates[1], COLS)]
        self.map[tuple(self.coordinates)] += 1

    def compute_direction(self, move):
        if move == 1:
            self.direction += RIGHT
            self.direction = (self._wrap_coordinate(self.direction, len(DIRECTIONS)))
        if move == 2:
            self.direction += LEFT
            self.direction = (self._wrap_coordinate(self.direction, len(DIRECTIONS)))

def main():
    moves = np.random.randint(0, 4, NUM_MOVES)
    print(moves)
    bot = Cleaner()
    print(bot.map)
    
    for move in moves:
        bot.compute_direction(move)
        bot.move(move)
        print(move)
        print(bot.map)
        print()
        
        
        # print(bot.coordinates)
        # print(bot.direction)
        
    print(bot.map)
        

if __name__ == "__main__":
    main()
