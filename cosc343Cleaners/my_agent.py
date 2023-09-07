__author__ = "<Jake Norton>"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "<norja159@student.otago.ac.nz>"

import random
import numpy as np
from settings import game_settings
agentName = "<my_agent>"
# Initialization of your variables
NUM_ROUNDS = 50
out_file = 'testing.txt'
trainingSchedule = [("random_agent.py", NUM_ROUNDS)]
SUBSET_SIZE = 0.3
grid_size = game_settings['gridSize']
rows, cols = grid_size
origin = [int(rows/2), int(cols/2)]
MUTATION = 0.01
avg_fitnesses = []
left = -1
right = 1
current_best_population = None
current_best_fitness = 1
ELITE_PERCENTAGE = 0.3
current_round = 1
fitness_function = ["cleaned"]

# Write these initial values to 'averages.txt'
with open(out_file, 'a') as file:
    file.write("------\n")  # A separator for better readability for each run
    file.write(f"Training Schedule: {trainingSchedule}\n")
    file.write(f"SUBSET_SIZE: {SUBSET_SIZE}\n")
    file.write(f"MUTATION: {MUTATION}\n")
    file.write(f"Average Fitnesses: {avg_fitnesses}\n")
    file.write(f"Current Best Population: {current_best_population}\n")
    file.write(f"Current Best Fitness: {current_best_fitness}\n")
    file.write(f"Elite percentage: {ELITE_PERCENTAGE}\n")
    file.write(f"NUM_ROUNDS: {NUM_ROUNDS}\n")
    file.write(f"Current Round: {current_round}\n")
    file.write(f"Fitness Function: {fitness_function}\n")
    file.write("------\n")  # A separator for better readability for each run

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
        self.chromosome = np.stack([np.append(np.random.uniform(0, 100, 63), np.random.uniform(0, 50)) for _ in range(4)])


    def compute_direction(self, turn):
        if turn == left and self.direction == 0:
            self.direction = 3
        elif turn == right and self.direction == 3:
            self.direction = 0
        else:
            self.direction += turn
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
        vertical_bots = visual[:,:,2] # 3x5 map of bots that can in this turn move up or down (from this bot's point of
                                      # view), -1 if the bot is an enemy, 1 if it is friendly
        horizontal_bots = visual[:,:,3] # 3x5 map of bots that can in this turn move up or down (from this bot's point
                                        # of view), -1 if the bot is an enemy, 1 if it is friendly

        #You may combine floor_state and energy_locations if you'd like: floor_state + energy_locations would give you
        # a mape where -1 indicates dirty square, 0 a clean one, and 1 an energy station.

        # You should implement a model here that translates from 'percepts' to 'actions'
        # through 'self.chromosome'.
        #
        flattened_visual = visual.reshape(-1)
        status = np.array([energy, bin, fails])
        tensor = np.concatenate((flattened_visual, status))
        # The 'actions' variable must be returned, and it must be a 4-item list or a 4-dim numpy vector

        # The index of the largest value in the 'actions' vector/list is the action to be taken,
        # with the following interpretation:
        # largest value at index 0 - move forward;
        # largest value at index 1 - turn right;
        # largest value at index 2 - turn left;
        # largest value at index 3 - move backwards;
        #
        # Different 'percepts' values should lead to different 'actions'.  This way the agent
        # reacts differently to different situations.
        #
        # Different 'self.chromosome' should lead to different 'actions'.  This way different
        # agents can exhibit different behaviour.

        # .
        # .
        # .

        # Right now this agent ignores percepts and chooses a random action.  Your agents should not
        # perform random actions - your agents' actions should be deterministic from
        # computation based on self.chromosome and percepts
        action_vector = self.compute_action(tensor)
        if fails ==0:
            self.previous_action = np.argmax(action_vector)
        else:
            self.previous_action = -1
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
        current_fitness = 0
        for metric in fitness_function:
            current_fitness += cleaner.game_stats[metric]
        fitness[n] = current_fitness

    return fitness


def newGeneration(old_population):
    global current_round, current_best_fitness, current_best_population
    # This function should return a tuple consisting of:
    # - a list of the new_population of cleaners that is of the same length as the old_population,
    # - the average fitness of the old population

    N = len(old_population)

    # Fetch the game parameters stored in each agent (we will need them to
    # create a new child agent)
    gridSize = old_population[0].gridSize
    nPercepts = old_population[0].nPercepts
    nActions = old_population[0].nActions
    maxTurns = old_population[0].maxTurns


    fitness = list(evalFitness(old_population))

    num_elites = int(ELITE_PERCENTAGE * N)
    elites  = top_n_indices(fitness, num_elites)

    # Create new population list...
    new_population = list()
    for elite in elites:
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
                    new_cleaner.chromosome[i][j] = (random.randint(0,100))
                elif rand > 0.49:
                    new_cleaner.chromosome[i][j] = (subset_parents[parent1].chromosome[i][j])
                else:
                    new_cleaner.chromosome[i][j] = (subset_parents[parent2].chromosome[i][j])

        new_population.append(new_cleaner)

    # At the end you need to compute the average fitness and return it along with your new population
    avg_fitness = np.mean(fitness)
    if current_round == 1:
        current_best_fitness = avg_fitness
        current_best_population = new_population
        
    current_round += 1
    if avg_fitness > current_best_fitness:
        current_best_fitness = avg_fitness
        current_best_population = new_population
    if current_round == NUM_ROUNDS:
        with open(out_file, 'a') as file:
            file.write("\nBest average fitness:\n " + str(current_best_fitness) + "\n")
            file.write("\nPrevious moves:\n" + str(current_best_population[0].nActions) + "\n")
            file.write("\nMap:\n" + str(current_best_population[0].map) + "\n")
            
        return (current_best_population, current_best_fitness)

    with open(out_file, 'a') as file:
        file.write(str(avg_fitness) + " ")

    
    return (new_population, avg_fitness)

def top_n_indices(lst, n):
    if not lst:
        return []

    n = min(n, len(lst))

    top_indices = sorted(range(len(lst)), key=lambda i: lst[i], reverse=True)[:n]

    return top_indices

