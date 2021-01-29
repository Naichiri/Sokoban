import sokoban
import sys
import map_generation

class Program:
    def __init__(self, *argv):
        self.mode = argv[1]
    
    def run(self):
        if mode == 1:
            if len(argv) < 3:
                "ERROR: Mode requires standard input"
            else:
                pass
        if mode == 2:
            length = len(argv)
            if length > 2:
                n_maps = argv[1]
            if length > 4:
                width = argv[2]
                height = argv[3]
            if length > 5: 
                good_direction_prob = argv[4]
            if length > 6:
                floor_noise_prob = argv[5]
                
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
    program.run()
