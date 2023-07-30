import itertools

def all_combinations(my_list):
    all_combinations = []
    
    for r in range(1, len(my_list) + 1):
        combinations_object = itertools.combinations(my_list, r)
        combinations_list = list(combinations_object)
        all_combinations += combinations_list
    
    return all_combinations

# Your list
my_list = [1, 5, 4, 7, 0, 2, 3, 6, 8, ]

result = all_combinations(my_list)

# print all combinations
for combo in result:
    print(list(combo))
