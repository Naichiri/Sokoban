import sokoban
import sys

class Program:
    def __init__(self, mode, input_file = None):
        self.mode = mode
        self.input_file = input_file
    
    def run(self):
        if mode == 1:
            if input_file == None:
                "ERROR: Mode requires standard input"
            else:
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
    if len(sys.argv == 3):
        program = Program(int(sys.argv[1]), sys.argv[2])
    else:
        program = Program(int(sys.argv[1]))
    program.run()
