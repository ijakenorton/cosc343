import numpy as np
cimport numpy as cnp

def evaluate_guess(cnp.ndarray guess, cnp.ndarray target):
    cdef int in_place = 0, in_colour = 0
    cdef cnp.ndarray mismatch_indices
    cdef cnp.ndarray state

    guess = np.reshape(guess, (-1))
    target = np.reshape(target, (-1))
    mismatch_indices = np.where(guess != target)[0]
    in_place = len(guess) - len(mismatch_indices)
    state = np.zeros_like(target, dtype=bool)

    for i in mismatch_indices:
        a = target[i]
        for j in mismatch_indices:
            if state[j]:
                continue
            b = guess[j]
            if a == b:
                in_colour += 1
                state[j] = True
                break

    return in_place, in_colour
