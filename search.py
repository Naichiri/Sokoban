'''
Authors: Christian Konopczyński, Wojciech Maciejewski
Problem: Sokoban
'''

import utils
from enum import Enum
from heapq import heappush, heappop
from timeit import default_timer as timer

class Action(Enum):
    up = 0
    down = 1
    left = 2
    right = 3

class State:
    def __init__(self, box_pos, worker_pos):
        self.box_pos = box_pos
        self.worker_pos = worker_pos

class Problem:

    def __init__(self, field):
        self.field_shape = field.shape
        self.initial_state = State(utils.get_box_pos(field), utils.get_worker_pos(field))
        self.walls = set(utils.get_walls(field))
        self.destination = utils.get_destination(field)

    def test_completion(self, state):
        return state.box_pos == self.destination

    def test_deadlock(self, state):
        box_pos_x, box_pos_y = state.box_pos
        # test for map corners
        if (box_pos_x == 0 and box_pos_y == 0):
            return True # top left
        if (box_pos_x == 0 and box_pos_y == self.field_shape[1] - 1):
            return True # top right
        if (box_pos_x == self.field_shape[0] - 1 and box_pos_y == 0):
            return True # bottom left
        if (box_pos_x == self.field_shape[0] - 1 and box_pos_y == self.field_shape[1] - 1):
            return True # bottom right

        # test for map sides + walls
        if box_pos_x == 0 or box_pos_x == self.field_shape[0] - 1:
            # top side or bottom side
            if (box_pos_x, box_pos_y - 1) in self.walls or (box_pos_x, box_pos_y + 1) in self.walls:
                return True
        if box_pos_y == 0 or box_pos_y == self.field_shape[1] - 1:
            # left side or right side
            if (box_pos_x - 1, box_pos_y) in self.walls or (box_pos_x + 1, box_pos_y) in self.walls:
                return True

        # test for walls
        if (box_pos_x - 1, box_pos_y) in self.walls and (box_pos_x, box_pos_y - 1) in self.walls:
            return True # up and left
        if (box_pos_x - 1, box_pos_y) in self.walls and (box_pos_x, box_pos_y + 1) in self.walls:
            return True # up and right
        if (box_pos_x + 1, box_pos_y) in self.walls and (box_pos_x, box_pos_y - 1) in self.walls:
            return True # down and left
        if (box_pos_x + 1, box_pos_y) in self.walls and (box_pos_x, box_pos_y + 1) in self.walls:
            return True # down and right

		# one step before deadlock could be checked as well, e.g.: 3 walls - up, top right, top left and 2 walls - 2 steps left, 2 steps right
	    
        return False

    def get_possible_actions(self, state):
        actions = []
        box_pos_x, box_pos_y = state.box_pos
        worker_pos_x, worker_pos_y = state.worker_pos

        # check for up movement
        new_worker_pos = (worker_pos_x - 1, worker_pos_y)
        new_box_pos = (worker_pos_x - 2, worker_pos_y)
        if new_worker_pos[0] >= 0 and\
            new_worker_pos not in self.walls and\
            (new_worker_pos != state.box_pos or\
             (not any(coord < 0 for coord in new_box_pos) and new_box_pos not in self.walls)):
            actions.append(Action.up)
                
        # check for down movement
        new_worker_pos = (worker_pos_x + 1, worker_pos_y)
        new_box_pos = (worker_pos_x + 2, worker_pos_y)
        if new_worker_pos[0] < self.field_shape[0] and\
            new_worker_pos not in self.walls and\
            (new_worker_pos != state.box_pos or\
             (not any(coord < 0 for coord in new_box_pos) and new_box_pos not in self.walls)):
            actions.append(Action.down)
            
        # check for left movement
        new_worker_pos = (worker_pos_x, worker_pos_y - 1)
        new_box_pos = (worker_pos_x, worker_pos_y - 2)
        if new_worker_pos[1] >= 0 and\
            new_worker_pos not in self.walls and\
            (new_worker_pos != state.box_pos or\
             (not any(coord < 0 for coord in new_box_pos) and new_box_pos not in self.walls)):
            actions.append(Action.left)
            
        # check for right movement
        new_worker_pos = (worker_pos_x, worker_pos_y + 1)
        new_box_pos = (worker_pos_x, worker_pos_y + 2)                
        if new_worker_pos[1] < self.field_shape[1] and\
            new_worker_pos not in self.walls and\
            (new_worker_pos != state.box_pos or\
             (not any(coord < 0 for coord in new_box_pos) and new_box_pos not in self.walls)):
            actions.append(Action.right)
        return actions
    
    def heuristic_cost_estimate(self, state):
        return abs(state.worker_pos[0] - state.box_pos[0]) + abs(state.worker_pos[1] - state.box_pos[1]) +\
            abs(state.box_pos[0] - self.destination[0]) + abs(state.box_pos[1] - self.destination[1]) - 1

class Node:
    def __init__(self, cost, state, parent, move):
        self.cost = cost
        self.state = state
        self.parent = parent
        self.move = move

    def calculate_cost(self, problem):
        return self.cost + problem.heuristic_cost_estimate(self.state)

    def get_child(self, action):
        worker_pos_x = self.state.worker_pos[0]
        worker_pos_y = self.state.worker_pos[1]
        
        new_box_pos = self.state.box_pos

        if action == Action.up:
            new_worker_pos = (worker_pos_x - 1, worker_pos_y)
            if new_box_pos == new_worker_pos:
                new_box_pos = (worker_pos_x - 2, worker_pos_y)
        elif action == Action.down:
            new_worker_pos = (worker_pos_x + 1, worker_pos_y)
            if new_box_pos == new_worker_pos:
                new_box_pos = (worker_pos_x + 2, worker_pos_y)
        elif action == Action.left:
            new_worker_pos = (worker_pos_x, worker_pos_y - 1)
            if new_box_pos == new_worker_pos:
                new_box_pos = (worker_pos_x, worker_pos_y - 2)
        elif action == Action.right:
            new_worker_pos = (worker_pos_x, worker_pos_y + 1)
            if new_box_pos == new_worker_pos:
                new_box_pos = (worker_pos_x, worker_pos_y + 2)

        return Node(self.cost + 1, State(new_box_pos, new_worker_pos), self, action)

def search(problem):
    timer_start = timer()
    node_total = 1 # counts nodes in the created tree
    revisited = 0
    counter = 0 # additional value put in tuple in case of equal f and h functions

    fringe = [] # open set
    # starting point
    initial = Node(0, problem.initial_state, None, None)
    explored_states = {initial} # visited states
    node_explored = 1
    heappush(fringe, (initial.calculate_cost(problem), problem.heuristic_cost_estimate(initial.state), counter, initial))
    counter += 1
    while len(fringe):
        n = heappop(fringe)[3]
        if problem.test_completion(n.state):
            return get_solution(n, node_total, revisited, len(fringe), node_explored, timer() - timer_start)
        if not problem.test_deadlock(n.state):
            explored_states.add((n.state.box_pos, n.state.worker_pos))
            node_explored += 1
            possible_actions = problem.get_possible_actions(n.state)
            for action in possible_actions:
                child = n.get_child(action)
                node_total += 1
                if (child.state.box_pos, child.state.worker_pos) not in explored_states: 
                    heappush(fringe, (child.calculate_cost(problem), problem.heuristic_cost_estimate(child.state), counter, child))
                    counter += 1
                else:
                    revisited += 1

    return (None, node_total, revisited, len(fringe), node_explored, timer() - timer_start)

def get_solution(current_node, node_total, revisited, fringe_size, explored_size, total_time):
    steps_taken = []
    # path reconstruction
    while current_node != None:
        steps_taken.insert(0, current_node.move)
        current_node = current_node.parent
    return (steps_taken, node_total, revisited, fringe_size, explored_size, total_time)
