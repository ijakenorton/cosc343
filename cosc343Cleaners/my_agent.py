__author__ = "<Jake Norton>"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "<norja159@student.otago.ac.nz>"

import random
import numpy as np
from settings import game_settings
agentName = "<my_agent>"
# Initialization of your variables
NUM_ROUNDS = 500

out_file = 'fitness.csv'
trainingSchedule = [("random_agent.py", NUM_ROUNDS)]
SUBSET_SIZE = 0.2
GRID_SIZE = game_settings['gridSize']
ROWS, COLS = GRID_SIZE
ORIGIN = [[int(ROWS/2), int(COLS/2)]]
MUTATION = 0.01
avg_fitnesses = []
current_best_population = None
current_best_fitness = 1
ELITE_PERCENTAGE = 0.2
current_round = 1
place_in_cycle = 1
NUM_TURNS_TO_AVERAGE = 6
LEFT = -1
RIGHT = 1
best_cleaners = []
NORTH, EAST, SOUTH, WEST = [-1, 0], [0, 1], [1, 0], [0, -1]
DIRECTIONS = [NORTH, EAST, SOUTH, WEST]
fitness_function = ["emptied", "visits"]
with open(out_file, 'w') as file:
    file.write(" ")
# with open(out_file, 'r') as file:
# Write these initial values to 'averages.txt'
# with open(out_file, 'a') as file:
#     file.write("------\n")  # A separator for better readability for each run
#     file.write(f"Training Schedule: {trainingSchedule}\n")
#     file.write(f"SUBSET_SIZE: {SUBSET_SIZE}\n")
#     file.write(f"MUTATION: {MUTATION}\n")
#     file.write(f"Average Fitnesses: {avg_fitnesses}\n")
#     file.write(f"Current Best Population: {current_best_population}\n")
#     file.write(f"Current Best Fitness: {current_best_fitness}\n")
#     file.write(f"Elite percentage: {ELITE_PERCENTAGE}\n")
#     file.write(f"NUM_ROUNDS: {NUM_ROUNDS}\n")
#     file.write(f"Current Round: {current_round}\n")
#     file.write(f"Fitness Function: {fitness_function}\n")
#     file.write("------\n")  # A separator for better readability for each run

# This is the class for your cleaner/agent
class Cleaner:

    def __init__(self, nPercepts, nActions, gridSize, maxTurns):
        # This is where agent initialisation code goes (including setting up a chromosome with random values)

        # Leave these variables as they are, even if you don't use them in your AgentFunction - they are
        # needed for initialisation of children Cleaners.
        self.nPercepts = nPercepts
        self.nActions = nActions
        self.gridSize = gridSize
        self.maxTurns = maxTurns
        self.chromosome = np.stack([np.append(np.random.uniform(-1, 1, 33), np.random.uniform(-1, 1)) for _ in range(3)])
        self.previous_action = 0
        self.direction = 0
        self.coordinates = ORIGIN[0].copy()
        self.map = np.zeros(GRID_SIZE)
        self.charge_stations = ORIGIN.copy()
        self.map[tuple(self.coordinates)] += 1
        self.is_charging = False
        self.fitness = 0

    def __lt__(self, other):
        # This method helps to sort agents based on their fitness
        return self.fitness < other.fitness
    
    def __repr__(self):
        return f"fitness={self.fitness}"
    
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
        if self.is_charging and (self.coordinates) not in self.charge_stations:
            self.charge_stations.append((self.coordinates))

    def compute_direction(self, move):
        if move == 1:
            self.direction += RIGHT
            self.direction = (self._wrap_coordinate(self.direction, len(DIRECTIONS)))
        if move == 2:
            self.direction += LEFT
            self.direction = (self._wrap_coordinate(self.direction, len(DIRECTIONS)))
            
            
    def AgentFunction(self, percepts):

        # The percepts are a tuple consisting of four pieces of information
        #
        # visual - it information of the 3x5 grid of the squares in front and to the side of the cleaner; this variable
        #          is a 3x5x4 tensor, giving four maps with different information
        #          - the dirty,clean squares
        #          - the energy
        #          - the friendly and enemy cleaners that are able to traverse vertically
        #          - the friendly and enemy cleaners that are able to traverse horizontally
        #
        #  energy - int value giving the battery state of the cleaner -- it's effectively the number of actions
        #           the cleaner can still perform before it runs out of charge
        #
        #  bin    - number of free spots in the bin - when 0, there is no more room in the bin - must emtpy
        #
        #  fails - number of consecutive turns that the agent's action failed (rotations always successful, forward or
        #          backward movement might fail if it would result in a collision with another robot); fails=0 means
        #          the last action succeeded.


        visual, energy, bin, fails = percepts

        # You can further break down the visual information

        floor_state = visual[:,:,0]   # 3x5 map where -1 indicates dirty square, 0 clean one
        energy_locations = visual[:,:,1] #3x5 map where 1 indicates the location of energy station, 0 otherwise
        vertical_bots = visual[:,:,2] # 3x5 map of bots that can in this turn move up or down (from this bot's point of view), -1 if the bot is an enemy, 1 if it is friendly
        horizontal_bots = visual[:,:,3] # 3x5 map of bots that can in this turn move up or down (from this bot's point of view), -1 if the bot is an enemy, 1 if it is friendly

        #You may combine floor_state and energy_locations if you'd like: floor_state + energy_locations would give you
        # a map where -1 indicates dirty square, 0 a clean one, and 1 an energy station.

        # You should implement a model here that translates from 'percepts' to 'actions'
        # through 'self.chromosome'.
        #
        flattened_floor = floor_state.reshape(-1)
        flattened_energy = energy_locations.reshape(-1)

        # Concatenate the flattened arrays
        flattened_visual = np.concatenate((flattened_floor, flattened_energy))

        status = np.array([energy, bin, fails])
        tensor = np.concatenate((flattened_visual, status))

        
        # energy_map = self.map.reshape(-1)
        # flattened_visual = visual.reshape(-1)
        # status = np.array([energy, bin, fails])
        # tensor = np.concatenate((flattened_visual, energy_map))
        # tensor = np.concatenate((tensor, status))
        
        action_vector = self.compute_action(tensor)
        action_vector = np.append(action_vector, -1)
        
        if fails ==0:
            self.previous_action = np.argmax(action_vector)
        else:
            self.previous_action = -1
        if energy == 20:
            self.is_charging = True
        else:
            self.is_charging = False
        self.compute_direction(self.previous_action)
        self.move(self.previous_action)
        return action_vector
    
    
    def compute_action(self, tensor):
                # Extract the weights and biases from the chromosome
        weights = self.chromosome[:, :-1]
        biases = self.chromosome[:, -1]

        # Compute v1, v2, v3, v4
        v = np.dot(weights, tensor) + biases

        return v
def evalFitness(population):

    N = len(population)

    # Fitness initialiser for all agents
    fitness = np.zeros((N))

    # This loop iterates over your agents in the old population - the purpose of this boilerplate
    # code is to demonstrate how to fetch information from the old_population in order
    # to score fitness of each agent
    for n, cleaner in enumerate(population):
        # cleaner is an instance of the Cleaner class that you implemented above, therefore you can access any attributes
        # (such as `self.chromosome').  Additionally, each object have 'game_stats' attribute provided by the
        # game engine, which is a dictionary with the following information on the performance of the cleaner in
        # the last game:
        #
        #  cleaner.game_stats['cleaned'] - int, total number of dirt loads picked up
        #  cleaner.game_stats['emptied'] - int, total number of dirt loads emptied at a charge station
        #  cleaner.game_stats['active_turns'] - int, total number of turns the bot was active (non-zero energy)
        #  cleaner.game_stats['successful_actions'] - int, total number of successful actions performed during active
        #                                                  turns
        #  cleaner.game_stats['recharge_count'] - int, number of turns spent at a charging station
        #  cleaner.game_stats['recharge_energy'] - int, total energy gained from the charging station
        #  cleaner.game_stats['visits'] - int, total number of squares visited (visiting the same square twice counts
        #                                      as one visit)

        # This fitness functions considers total number of cleaned squares.  This may NOT be the best fitness function.
        # You SHOULD consider augmenting it with information from other stats as well.  You DON'T HAVE TO make use
        # of every stat.
        current_fitness = 1
        # current_fitness += cleaner.game_stats['visits'] * 0.15
        # current_fitness += cleaner.game_stats['cleaned'] * 0.1
        for metric in fitness_function:
            current_fitness *= cleaner.game_stats[metric]
        
        # current_fitness *= cleaner.game_stats['visits']
        
        for coordinate in cleaner.charge_stations:            
            if cleaner.map[tuple(coordinate)] > 1:
                current_fitness -= cleaner.map[tuple(coordinate)]
        # current_fitness -= cleaner.map[tuple(ORIGIN[0])] 
        cleaner.fitness += current_fitness
        fitness[n] = cleaner.fitness/place_in_cycle

    return fitness


def newGeneration(old_population):
    global current_round, current_best_fitness, current_best_population, best_cleaners, place_in_cycle
    # This function should return a tuple consisting of:
    # - a list of the new_population of cleaners that is of the same length as the old_population,
    fitness = list(evalFitness(old_population))
    avg_fitness = np.mean(fitness)
    with open(out_file, 'a') as file:
        file.write(str(avg_fitness) + " ")
    # - the average fitness of the old population
    if place_in_cycle < NUM_TURNS_TO_AVERAGE:
        place_in_cycle += 1
        return  (old_population, avg_fitness)
    else:

        N = len(old_population)

        # Fetch the game parameters stored in each agent (we will need them to
        # create a new child agent)
        gridSize = old_population[0].gridSize
        nPercepts = old_population[0].nPercepts
        nActions = old_population[0].nActions
        maxTurns = old_population[0].maxTurns



        num_elites = int(ELITE_PERCENTAGE * N)
        elites  = top_n_indices(fitness, num_elites)
        
        place_in_cycle = 1
    
    # Create new population list...
        new_population = list()
        for elite in elites:
            old_population[elite].fitness = 0
            new_population.append(old_population[elite])

        for n in range(N-num_elites):

            # Create a new cleaner
            new_cleaner = Cleaner(nPercepts, nActions, gridSize, maxTurns)
            indices = random.sample(range(N), int(N* SUBSET_SIZE))
            subset_scores = [fitness[j] for j in indices]
            subset_parents = [old_population[x] for x in indices]
            parent1, parent2 = top_n_indices(subset_scores,2)
            
            for i in range(0, len(subset_parents[parent1].chromosome)):
                for j in range(len(subset_parents[parent1].chromosome[i])):
                    rand = random.random()
                    if rand < MUTATION:
                        new_cleaner.chromosome[i][j] = (random.randint(-1,1))
                    elif rand > 0.49:
                        new_cleaner.chromosome[i][j] = subset_parents[parent1].chromosome[i][j]
                    else:
                        new_cleaner.chromosome[i][j] = subset_parents[parent2].chromosome[i][j]

            new_population.append(new_cleaner)

        # At the end you need to compute the average fitness and return it along with your new population
        if current_round == 1:
            
            current_best_fitness = avg_fitness
            current_best_population = new_population

        current_round += 1
        # if avg_fitness > current_best_fitness and current_round > int(NUM_ROUNDS* 0.8):
        #     current_best_fitness = avg_fitness
        #     current_best_population = new_population
        # if current_round > int(NUM_ROUNDS*0.8):
            
        #     for agent in old_population:
        #         best_cleaners = add_new_agent(best_cleaners,agent)
        # if current_round == NUM_ROUNDS:
            
        #     with open(out_file, 'a') as file:
        #         file.write("\nlast round:\n " + str(sorted(old_population)) + "\n")
        #         file.write("\nbest_cleaners:\n " + str(best_cleaners) + "\n")
                
        #     return (best_cleaners, current_best_fitness)
        


        
        return (new_population, avg_fitness)

def add_new_agent(top_agents, new_agent):
    """
    Adds a new agent to the top_agents list if it's better than the worst one in the list.
    The list is then sorted and returned.
    """
    if len(top_agents) < game_settings['nCleaners']:
        top_agents.append(new_agent)
    elif new_agent.fitness > top_agents[0].fitness:  # since the list is sorted, the first agent is the worst one
        top_agents[0] = new_agent  # replace the worst agent

    # Return the sorted list of top agents
    return sorted(top_agents)


def top_n_indices(lst, n):
    if not lst:
        return []

    n = min(n, len(lst))

    top_indices = sorted(range(len(lst)), key=lambda i: lst[i], reverse=True)[:n]

    return top_indices

