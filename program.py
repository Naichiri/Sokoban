import sokoban
import numpy as np
import sys
import map_generation
import search
import utils

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
        elif self.mode == '2':
            d = {}
            if length > 0:
                n_maps = int(self.argv[0])
            else:
                n_maps = 1
            if length > 2:
                width = self.argv[1]
                height = self.argv[2]
            else:
                width = 10
                height = 10
            if length > 3: 
                d['good_direction_prob'] = self.argv[3]
            if length > 4:
                d['floor_noise_prob'] = self.argv[4]
                
            for i in range(n_maps):
                field = map_generation.generate_map(width, height, **d)
                map_generation.visualize_field(field)
                print_output(sokoban.solve(field))
        elif self.mode == "-help":
            print("Available execution parameters:\n", \
                    "-help - displays this text\n", \
                    "1 file.npyz - solves for numpy arrays compressed in the specified .npyz file\n", \
                    "2 [n] [width length] [gdp] [fnp] - solves for n width x length maps which are generated randomly.\n", \
                    "\tDefaultly solves one 10x10 map. Additional parameters tweak map generation, details in readme\n")
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
