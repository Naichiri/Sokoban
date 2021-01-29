import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
import utils

def get_xy_positions(val, width, height):
    '''
    Translate 1d postionon from flattened map to 2 coordinates of 2d map
    '''
    start_pos_y = val // width
    start_pos_x = val - start_pos_y * width
    return start_pos_x, start_pos_y

def check_if_path_exists(width, height, box_pos, end_pos):
    '''
    Check if path exists assuming there are no walls on the map
    '''
    if box_pos == end_pos:
        return True
    
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
    '''
    Check if map with given start_pos, box_pos and end_pos can be legal if there were no 
    additional walls in it
    '''
    
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

def find_path(game_map, width, height, current_pos, finish_pos, is_worker_path=False,
              clear_start_area=False, good_direction_prob=0.8):
    '''
    Make a path from current_pos to finish_pos and update game_map with it.
    '''
    current_pos_x, current_pos_y = get_xy_positions(current_pos, width, height)
    finish_pos_x, finish_pos_y = get_xy_positions(finish_pos, width, height)    
    new_pos_x, new_pos_y = current_pos_x, current_pos_y
    
    # from the perspective of the box there has to be some additional space for
    # the worker to walk around it.
    if clear_start_area:
        g = game_map[max(current_pos_y - 1, 0): min(current_pos_y + 2, height),
                     max(current_pos_x - 1, 0): min(current_pos_x + 2, width)]
        g[:, :][g == utils.WALL_VAL] = utils.FLOOR_VAL
    
    bad_direction_prob = 1.0 - good_direction_prob
    x_diff = finish_pos_x - current_pos_x
    y_diff = finish_pos_y - current_pos_y
    move_vertical = np.random.choice([True, False])

    while (x_diff != 0 or y_diff != 0):
        change_direction = np.random.choice([True, False], p=[0.1, 0.9])
        if change_direction:
            move_vertical = not move_vertical
            
        # If move_to destination is True - the worker goes towards destination.
        # If move_to_destination is False - the workek goes in random direction.
        # It means that the path is biased towards the destination, in the worst case
        # scenario when the if good_direction_prob=0 it will work like random search
        move_to_destination = np.random.choice([True, False], p=[good_direction_prob, bad_direction_prob])
        if move_vertical:
            if move_to_destination and y_diff:
                new_pos_y += math.copysign(1, y_diff)
            else:
                new_pos_y += np.random.choice([-1, 1])
        else:
            if move_to_destination and x_diff:
                new_pos_x += math.copysign(1, x_diff)
            else:
                new_pos_x += np.random.choice([-1, 1])
        
        new_pos = width * new_pos_y + new_pos_x

        # if the new position is legal - update for next iteration
        if new_pos_x < width and new_pos_x >= 0 and\
            new_pos_y < height and new_pos_y >= 0 and\
            (is_worker_path or check_if_path_exists(width, height, new_pos, finish_pos)):
                
            if change_direction:
                g = game_map[max(current_pos_y - 1, 0): min(current_pos_y + 2, height),
                             max(current_pos_x - 1, 0): min(current_pos_x + 2, width)]
                g[:, :][g == utils.WALL_VAL] = utils.FLOOR_VAL
                
            current_pos_y = int(new_pos_y)
            current_pos_x = int(new_pos_x)
            x_diff = finish_pos_x - current_pos_x
            y_diff = finish_pos_y - current_pos_y
            if game_map[current_pos_y, current_pos_x] == utils.WALL_VAL:
                game_map[current_pos_y, current_pos_x] = utils.FLOOR_VAL
                
        else:
            new_pos_x = current_pos_x
            new_pos_y = current_pos_y
    return game_map     

def generate_map(width, height, good_direction_prob=0.5, floor_noise_prob=0.7):
    '''
    Generate random map for our algorithm.
    '''
    
    if np.round(width) != width or np.round(height) != height:
        raise ValueError("height and width must be integers")
    if width > 100 or height > 100 or width < 1 or height < 1:
        raise ValueError("height and width must be between 1 and 100")
        
    map_size = width * height
    if map_size < 3:
        raise ValueError("no legal map can be generated with mapsize smaller than 3")    
    if width == 2 and height == 2:
        raise ValueError("map with height=2 and width=2 cannot be solved")
        
    game_map = np.full((height, width), utils.WALL_VAL, dtype=np.uint8)
    
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
    
    game_map[start_pos_y, start_pos_x] = utils.WORKER_VAL
    game_map[box_pos_y, box_pos_x] = utils.BOX_VAL
    game_map[end_pos_y, end_pos_x] = utils.DESTINATION_VAL
    
    game_map = find_path(game_map, width, height, start_pos, box_pos,
                         is_worker_path=True, good_direction_prob=good_direction_prob)
    game_map = find_path(game_map, width, height, box_pos, end_pos,
                         clear_start_area=True, good_direction_prob=good_direction_prob)
    
    mask = game_map == utils.WALL_VAL
    random_mask = np.random.choice([True, False], size=mask.size, replace=True, p=[floor_noise_prob, 1.0 - floor_noise_prob])
    random_mask = random_mask.reshape(mask.shape)
    mask = mask * random_mask
    game_map[mask] = utils.FLOOR_VAL
    
    return game_map

def visualize_field(field):
    '''
    Visualize the map.
    '''
    values = [utils.FLOOR_VAL, utils.WALL_VAL, utils.WORKER_VAL, utils.BOX_VAL, utils.DESTINATION_VAL]
    labels = ['floor', 'wall', 'worker_start_pos', 'box_start_pos', 'destination']
    im = plt.imshow(field, interpolation='none')
    colors = [ im.cmap(im.norm(value)) for value in values]
    patches = [ mpatches.Patch(color=colors[i], label=labels[i] ) for i in range(len(values)) ]
    # put those patched as legend-handles into the legend
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()
    
if __name__ == "__main__":
    for i in range(1000):
        width = 0
        height = 0
        while width * height < 3 or (width == 2 and height == 2):
            width = np.random.randint(1, 101)
            height = np.random.randint(1, 101)
        m = generate_map(width, height, good_direction_prob=0.8, floor_noise_prob=0.7)
        try:
            assert((m == utils.BOX_VAL).sum() == 1)
            assert((m == utils.WORKER_VAL).sum() == 1)
            assert((m == utils.DESTINATION_VAL).sum() == 1)
        except AssertionError:
            visualize_field(m)
            raise
    visualize_field(m)
