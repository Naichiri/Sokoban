'''
Author: Wojciech Maciejewski
Problem: Sokoban
'''

import numpy as np
import sokoban
import map_generation
import matplotlib.pyplot as plt
import json

def get_maps_for_statistics(output_file, n_maps=1000):
    d = {}
    for i in range(n_maps):
        width = 0
        height = 0
        good_direction_prob = np.random.random()
        floor_noise_prob = np.random.random()
        while width * height < 3 or (width == 2 and height == 2):
            width = np.random.randint(1, 31)
            height = np.random.randint(1, 31)
        m = map_generation.generate_map(width, height, good_direction_prob=good_direction_prob, floor_noise_prob=floor_noise_prob)
        d[str(i)] = m
        
    np.savez(output_file, **d)
    return

if __name__ == '__main__':
    path = 'maps_for_statistics.npz'

    #get_maps_for_statistics(path)

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
    print('time taken for all maps:', np.sum(times))
    branchning_factors = np.array(gen_nodes_numbers) / np.array(explored_states_number)
    print('average branching factor:', branchning_factors.mean())
    print('max branching factor:', branchning_factors.max())
    print('min branching factor:', branchning_factors.min())
    idx = np.argmax(branchning_factors)
    print(f'max for: n_nodes={gen_nodes_numbers[idx]}, n_explored={explored_states_number[idx]}' )
    
    plt.scatter(gen_nodes_numbers, times)
    plt.scatter(sizes, times)
    plt.scatter(sizes, gen_nodes_numbers)
    plt.scatter(branchning_factors, times)
    path_lenghts = [len(output) for output in outputs]
    plt.scatter(path_lenghts, times)
    temp = []
    for path_len, b_factor in zip (path_lenghts, branchning_factors):
        temp.append(np.power(b_factor, path_len))
    plt.scatter(temp, times)
