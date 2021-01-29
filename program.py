import sokoban
import sys
import map_generation

class Program:
    def __init__(self, *argv):
        self.mode = argv[1]
        self.argv = argv[2:]
    
    def run(self):
        if mode == 1:
            if len(argv) < 3:

    def run(self):
        length = len(self.argv)
        if self.mode == 1:
            if length == 0:
                "ERROR: Mode requires standard input"
            else:
                pass
        if self.mode == 2:
            
            if length > 0:
                n_maps = argv[0]
            if length > 2:
                width = argv[1]
                height = argv[2]
            if length > 3: 
                good_direction_prob = argv[3]
            if length > 4:
                floor_noise_prob = argv[4]
                
            for i in range(n_maps):
                pass
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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERROR: Not enough arguments, expected amount: 1 or 2")
        sys.exit()

    program = Program(sys.argv)
