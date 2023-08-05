import numpy as np
keys = [['B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'R'], ['B', 'B', 'B', 'R', 'R'], [
    'B', 'B', 'R', 'R', 'G'], ['B', 'R', 'R', 'G', 'G'], ['B', 'R', 'R', 'G', 'Y'], ['B', 'R', 'G', 'Y', 'P']]
values = [21156876,
          9410300,
          7623222,
          6659862,
          6659862,
          6910906,
          7566038]
groups = {tuple(key): value for key, value in zip(keys, values)}

# # If you want to print the groups:
# for key, value in groups.items():
#     print(f"Key: {key}, Value: {value}")

# Assuming 'groups' is the dictionary containing counts for each key

# Normalize the counts to get probabilities

# Normalize the counts to get probabilities
total_count = sum(groups.values())
probabilities = {key: count / total_count for key, count in groups.items()}


# Compute the entropy for each key
entropies = {key: -p * np.log2(p) if p >
             0 else 0 for key, p in probabilities.items()}

# Print the entropies
for key, entropy in entropies.items():
    print(f"Key: {key}, Entropy: {entropy}")
