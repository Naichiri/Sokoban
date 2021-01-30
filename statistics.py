import numpy as np
import sokoban
import map_generation
import matplotlib.pyplot as plt
import json

def get_maps_for_statistics(output_file, n_maps=10000):
    d = {}
    for i in range(n_maps):
        width = 0
        height = 0
        good_direction_prob = np.random.random()
        floor_noise_prob = np.random.random()
        while width * height < 3 or (width == 2 and height == 2):
            width = np.random.randint(1, 11)
            height = np.random.randint(1, 11)
        m = map_generation.generate_map(width, height,
                                        good_direction_prob=good_direction_prob,
                                        floor_noise_prob=0)
        d[str(i)] = m
        
    np.savez(output_file, **d)
    return

if __name__ == '__main__':
    path = 'maps_for_statistics_small.npz'
    get_maps_for_statistics(path)
    
    data = np.load(path)
    sizes = []
    gen_nodes_numbers = []
    revisited_states_numbers = []
    items_remaining_numbers = []
    explored_states_number = []
    times = []
    outputs = []
    for key in data:
        print(key)
        field = data[key]
        output = sokoban.solve(field)
        sizes.append(field.size)
        gen_nodes_numbers.append(output[1])
        revisited_states_numbers.append(output[2])
        items_remaining_numbers.append(output[3])
        explored_states_number.append(output[4])
        times.append(output[5])

        outputs.append(list(output))
    print(np.sum(times))
    '''
    for output in outputs:
        output[0] = [str(action) for action in output[0]]
    with open('test.json', 'w') as f:
        f.write(json.dumps(outputs))
    
    with open('test.json', 'r') as f:
        old_outputs = json.load(f)
    
    outputs = [output[0] for output in outputs]
    new_outputs = []
    for output in outputs:
        new_outputs.append([str(action) for action in output])
    old_outputs = [output[0] for output in old_outputs]
    
    assert(old_outputs == new_outputs)
    '''
    
    plt.scatter(gen_nodes_numbers, times)
    