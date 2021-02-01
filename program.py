'''
Authors: Christian Konopczyński, Wojciech Maciejewski
Problem: Sokoban
'''

import sokoban
import numpy as np
import pandas as pd
import sys
import map_generation
import search
import utils

pd.set_option("display.max_rows", None, "display.max_columns", None)

class Program:
    def __init__(self, argv):
        self.mode = argv[1]
        self.argv = argv[2:]

    def run(self):
        length = len(self.argv)
        if self.mode == '1':
            if length == 0:
                print("ERROR: Mode requires input file specified in parameter")
            else:
                data = np.load(self.argv[0])
                for key in data:
                    print_output(sokoban.solve(data[key]))
        elif self.mode == '2' or self.mode == '3':
            d = {}
            default_sizes = False
            if length > 0:
                n_maps = int(self.argv[0])
            else:
                n_maps = 1
            if length > 2:
                if self.argv[1] == 'random' or self.argv[1] == 'r':
                    width = np.random.randint(3, 101)
                else:
                    width = int(self.argv[1])
                if self.argv[2] == 'random' or self.argv[2] == 'r':
                    height = np.random.randint(3, 101)
                else:
                    height = int(self.argv[2])
            else:
                default_sizes = True
                width = 10
                height = 10
            if length > 3: 
                d['good_direction_prob'] = float(self.argv[3])
            if length > 4:
                d['floor_noise_prob'] = float(self.argv[4])
            if self.mode == '2':
                for i in range(n_maps):
                    field = map_generation.generate_map(width, height, **d)
                    map_generation.visualize_field(field)
                    print_output(sokoban.solve(field))
            else:
                if default_sizes:
                    min_size = 3
                    max_size = utils.MAX_WIDTH
                else:
                    min_size = width
                    max_size = height
                    
                size_step = (max_size - min_size) / n_maps
                sizes = []
                times = []
                gen_nodes_numbers = []
                for i in range(n_maps):
                    field = map_generation.generate_map(int(width), int(height), **d)
                    output = sokoban.solve(field)
                    sizes.append(field.size)
                    times.append(output[5])
                    gen_nodes_numbers.append(output[1])
                    
                    width += size_step
                    height += size_step
                
                times = np.array(times) * 1000.0 # seconds to milliseconds
                time_per_node = (np.array(times) / np.array(gen_nodes_numbers)).mean()
                sizes = np.array(sizes)
                estimated_complexity = sizes ** 2
                estimated_complexity = estimated_complexity * np.log(estimated_complexity)
                estimated_time_complexity = estimated_complexity * time_per_node
                
                n_median_index = int((len(sizes) - 1) / 2)
                estimated_TC_median = estimated_time_complexity[n_median_index]
                real_TC_median = times[n_median_index]
                q_n = times * estimated_TC_median / (estimated_time_complexity * real_TC_median)
                
                df = pd.DataFrame({'n': sizes, 't(n)[ms]': times, 'q(n)': q_n})
                print(df)
                
        elif self.mode == "-help":
            print("Available execution parameters:\n", \
                    "-help - displays this text\n", \
                    "1 file.npyz - solves for numpy arrays compressed in the specified .npyz file\n", \
                    "2 [n] [width length] [gdp] [fnp] - solves for n width x length maps which are generated randomly.\n", \
                    "\tBy default solves one 10x10 map. Additional parameters tweak map generation, details in readme\n")
        else:
            print("ERROR: Unknown parameter, try running as:", sys.argv[0], "-help")
        return

def print_output(solve_output):
    if solve_output[0] != None:
        print("Number of steps:", len(solve_output[0]))
        print("Path:")
        for step in solve_output[0]:
            print(step, end=' — ')
        print()
    else:
        print("Solution not found.")
    print("\nNumber of generated nodes:", solve_output[1])
    print("Number of revisited states:", solve_output[2])
    print("Number of items remaining in the open set:", solve_output[3])
    print("Number of explored states:", solve_output[4])
    print("Total time [seconds]:", solve_output[5])
    print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERROR: Not enough arguments, expected amount: 1 or 2, try running as:", sys.argv[0], "-help")
        sys.exit()

    program = Program(sys.argv)
    program.run()
