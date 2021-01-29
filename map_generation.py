import numpy as np
import matplotlib.pyplot as plt
import math

FLOOR_VAL = 0
WAAL_VAL = 1
BOX_VAL = 2
WORKER_VAL = 3
DESTINATION_VAL = 4

def get_xy_positions(val, width, height):
    start_pos_y = val // width
    start_pos_x = val - start_pos_y * width
    return start_pos_x, start_pos_y

def check_if_path_exists(width, height, box_pos, end_pos):
    # initialize useful variables
    map_size = width * height
    upper_left_pos = 0
    upper_right_pos = width - 1
    bottom_left_pos = map_size - width
    bottom_right_pos = map_size - 1
    
    # check if box stuck in the corner
    if (width > 1 and height > 1) and (box_pos == upper_left_pos or\
       box_pos == upper_right_pos or\
       box_pos == bottom_left_pos or\
       box_pos == bottom_right_pos):
        return False
    
    # get x, y coords from positions
    box_pos_x, box_pos_y = get_xy_positions(box_pos, width, height)
    end_pos_x, end_pos_y = get_xy_positions(end_pos, width, height)
    
    # check if box stuck adjecent to map border
    if (end_pos_x != box_pos_x and (box_pos_x == 0 or box_pos_x == width - 1)) or\
       (end_pos_y != box_pos_y and (box_pos_y == 0 or box_pos_y == height - 1)):
           return False
       
    return True

def is_legal(width, height, start_pos, box_pos, end_pos):
    
    # check if positions overlap
    if start_pos == box_pos or start_pos == end_pos or box_pos == end_pos:
        return False
    
    # if one of dimensions is 1 - check if the positions are in legal order
    # legal order: start_pos > box_pos > end_pos or start_pos < box_pos < end_pos
    if (width == 1 or height == 1) and\
        not ((start_pos > box_pos and box_pos > end_pos) or\
             (start_pos < box_pos and box_pos < end_pos)):
            return False
             
    return check_if_path_exists(width, height, box_pos, end_pos)

def find_path(game_map, width, height, current_pos, finish_pos):
    current_pos_x, current_pos_y = get_xy_positions(current_pos, width, height)
    finish_pos_x, finish_pos_y = get_xy_positions(finish_pos, width, height)    
    new_pos_x, new_pos_y = current_pos_x, current_pos_y
    
    x_diff = finish_pos_x - current_pos_x
    y_diff = finish_pos_y - current_pos_y
    move_vertical = np.random.choice([True, False])
    while (x_diff > 0 and y_diff > 0) or\
          not check_if_path_exists(width, height, current_pos, finish_pos):
        
        if not game_map[current_pos_y, current_pos_x]:
            game_map[current_pos_y, current_pos_x] = -1
              
        change_direction = np.random.choice([True, False], p=[0.2, 0.8])
        if change_direction:
            move_vertical = not move_vertical
        
        move_to_destination = np.random.choice([True, False], p=[0.7, 0.3])
        if move_vertical:
            if move_to_destination and y_diff:
                new_pos_y += math.copysign(1, y_diff)
            else:
                new_pos_y += np.random.choice([-1, 1])
        else:
            if move_to_destination and x_diff:
                new_pos_x += math.copysign(1, y_diff)
            else:
                new_pos_x += np.random.choice([-1, 1])

def generate_map(width, height):
    if np.round(width) != width or np.round(height) != height:
        raise ValueError("height and width must be integers")
    if width > 100 or height > 100 or width < 1 or height < 1:
        raise ValueError("height and width must be between 1 and 100")
        
    map_size = width * height
    if map_size < 3:
        raise ValueError("no legal map can be generated with mapsize smaller than 3")    
    if width == 2 and height == 2:
        raise ValueError("map with height=2 and width=2 cannot be solved")
        
    game_map = np.full((height, width), FLOOR_VAL, dtype=np.uint8)
    
    start_pos = np.random.randint(0, map_size)
    box_pos = np.random.randint(0, map_size)
    end_pos = np.random.randint(0, map_size)
    while not is_legal(width, height, start_pos, box_pos, end_pos):
        start_pos = np.random.randint(0, map_size)
        box_pos = np.random.randint(0, map_size)
        end_pos = np.random.randint(0, map_size)
    
    start_pos_x, start_pos_y = get_xy_positions(start_pos, width, height)
    box_pos_x, box_pos_y = get_xy_positions(box_pos, width, height)
    end_pos_x, end_pos_y = get_xy_positions(end_pos, width, height)
    
    game_map[start_pos_y, start_pos_x] = WORKER_VAL
    game_map[box_pos_y, box_pos_x] = BOX_VAL
    game_map[end_pos_y, end_pos_x] = DESTINATION_VAL

    return game_map
    
if __name__ == "__main__":
    for i in range(10000):
        width = 0
        height = 0
        while width * height < 3 or (width == 2 and height == 2):
            width = np.random.randint(1, 101)
            height = np.random.randint(1, 101)
            
        m = generate_map(width, height)
        assert((m == 0).sum() == width * height - 3)
        
    plt.imshow(m)
    plt.show()