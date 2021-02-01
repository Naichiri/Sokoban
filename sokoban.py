'''
Author: Christian Konopczyński
Problem: Sokoban
'''

import numpy as np
import search
import map_generation as mg

def solve(field):
    return search.search(search.Problem(field))

if __name__ == "__main__":
    m = np.array([[1, 0, 3, 1,],
                  [0, 2, 1, 1,],
                  [0, 0, 0, 4,],
                  [1, 1, 1, 1,]])
    print(m)
    print(solve(m))
    m = np.array([[0, 0, 0, 0,],
                  [2, 0, 0, 0,],
                  [0, 0, 0, 4,],
                  [0, 0, 0, 3,]])
    print(m)
    print(solve(m))
    m = np.array([[0, 0, 0, 0,],
                  [0, 0, 1, 2,],
                  [0, 0, 0, 4,],
                  [0, 0, 0, 3,]])
    print(m)
    print(solve(m))
    m = np.array([[0, 1, 0, 0,],
                  [2, 0, 0, 0,],
                  [0, 1, 0, 4,],
                  [0, 1, 0, 3,]])
    print(m)
    print(solve(m))
    m = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
                  [0, 0, 1, 2, 1, 0, 0, 0, 0, 0,],
                  [0, 0, 0, 0, 1, 1, 1, 0, 0, 0,],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
                  [0, 0, 0, 1, 0, 0, 0, 0, 0, 0,],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
                  [0, 0, 0, 0, 0, 0, 1, 0, 1, 0,],
                  [0, 0, 0, 0, 0, 0, 0, 3, 4, 0,]])
    print(m)
    print(solve(m))
