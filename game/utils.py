import numpy as np
from itertools import combinations
from random import choice, shuffle

def indices_of_ones(binary_array: np.ndarray) -> list:
    """Returns the indices of only the elements equal to 1.
    Assumed that the input is a binary array."""
    return [i for i,v in np.ndenumerate(binary_array) if v == 1]

def sum_indices_of_ones(indxs: list, shape: tuple) -> np.ndarray:
    """Returns the original array from which we got one-indices.
    Is the inverse function of indices_of_ones."""
    binary_array = np.zeros(shape)
    for idx in idxs:
        binary_array[idx[0],idx[1]] = 1
    return binary_array
    

def list_nonzero_combinations(v: np.ndarray, L: int) -> list:
    """Returns a list of every combination of indices of elements equal to 1, where number of indices range from 1 to L."""
    idxs = indices_of_ones(v)
    list_combinations = []
    if len(idxs) > 0:
        for r in range(1, L+1):
            list_combinations += [c for c in combinations(idxs, r)]
    return list_combinations
