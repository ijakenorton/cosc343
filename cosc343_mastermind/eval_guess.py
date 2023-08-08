import numpy as np
from collections import Counter

def evaluate_guess(secret_code, guess):
    score1 = [1 for i in range(len(secret_code)) if guess[i] == secret_code[i]]  ## list for exact matches
    score2 = [0 for i in range(len(secret_code)) if guess[i] in secret_code]   ## list for "color" matches
    score1.extend(score2[:-len(score1)])
    score1.sort(reverse=True)  
    ## in this method, every 1 also shows up as a zero, so when you combine the lists, you just account for that by subtracting a zero for every one that appears
    print(score1)
    exit(0)
    return score1[0], score1[1]

# def evaluate_key(secret_code, key, position):
#     # Will return a None value in case of a "miss", as per your plan.
#     if key == secret_code[position]:
#         return 1
#     elif key in secret_code:
#         return 0

# def evaluate_guess(secret_code, guess, secret_code_length=5):
#     return sorted(
#         filter(None.__ne__, # Filter out None values. See https://docs.python.org/3.5/reference/datamodel.html#object.__ne__
#             [evaluate_key(secret_code, g, p) 
#             for (g, p) in zip(guess, list(range(secret_code_length)))]
#         ),
#         reverse=True
#     )