import numpy as np
import matplotlib.pyplot as plt

FLOOR_VAL = 0
WAAL_VAL = 1
BOX_VAL = 2
WORKER_VAL = 3
DESTINATION_VAL = 4

def get_xy_positions(val, width, height):
    start_pos_y = val // width
    start_pos_x = val - start_pos_y * width
    return start_pos_x, start_pos_y

def generate_map(width, height):
    if np.round(width) != width or np.round(height) != height:
        raise ValueError("height and width must be integers")
    if width > 100 or height > 100 or width < 1 or height < 1:
        raise ValueError("height and width must be between 1 and 100")
        
    map_size = width * height
    if map_size < 3:
        raise ValueError("no legal map can be generated with mapsize smaller than 3")    
        
    game_map = np.full((height, width), FLOOR_VAL, dtype=np.uint8)
    start_pos = np.random.randint(0, map_size)
    box_pos = np.random.randint(0, map_size)
    end_pos = np.random.randint(0, map_size)
    while box_pos == start_pos:
        box_pos = np.random.randint(0, map_size)
    while end_pos == start_pos or end_pos == box_pos:
        end_pos = np.random.randint(0, map_size)
    
    start_pos_x, start_pos_y = get_xy_positions(start_pos, width, height)
    box_pos_x, box_pos_y = get_xy_positions(box_pos, width, height)
    end_pos_x, end_pos_y = get_xy_positions(end_pos, width, height)
    
    game_map[start_pos_y, start_pos_x] = WORKER_VAL
    game_map[box_pos_y, box_pos_x] = BOX_VAL
    game_map[end_pos_y, end_pos_x] = DESTINATION_VAL

    return game_map
    
for i in range(10000):
    width = np.random.randint(2, 101)
    height = np.random.randint(2, 101)
    m = generate_map(width, height)
    assert((m == 0).sum() == width * height - 3)
    
plt.imshow(m)
plt.show()