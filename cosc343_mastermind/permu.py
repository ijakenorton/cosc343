import itertools

permutations = []

possible_outputs = list(filter(lambda x: sum(x) <= 5, itertools.product(range(6), repeat=2)))
print(len(possible_outputs))