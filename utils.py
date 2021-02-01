'''
Author: Christian Konopczyński
Problem: Sokoban
'''

import numpy as np

FLOOR_VAL = 0
WALL_VAL = 1
BOX_VAL = 2
WORKER_VAL = 3
DESTINATION_VAL = 4
MAX_WIDTH = 100
MAX_HEIGHT = 100

def get_coordinates(field, value):
    w = np.where(field == value)
    coordinates = []
    for i in range(w[0].size):
        coordinates.append((w[0][i], w[1][i]))
    return coordinates

def get_walls(field):
    return get_coordinates(field, WALL_VAL)

def get_box_pos(field):
    return get_coordinates(field, BOX_VAL)[0]

def get_worker_pos(field):
    return get_coordinates(field, WORKER_VAL)[0]

def get_destination(field):
    return get_coordinates(field, DESTINATION_VAL)[0]
