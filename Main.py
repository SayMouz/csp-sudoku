import sys
import random
from CSP import CSP
from Sudoku import Sudoku

def print_help_message() :
    print("Please enter correct arguments.\n")
    print("To solve a random 9x9 sudoku :")
    print("  python3 Main.py random *difficulty*")
    print("  (With *difficulty* a number from 1 to 9)\n")
    print("To solve read a sudoku from a file :")
    print("  python3 Main.py read *filename*")

def generate_random_sudoku(difficulty: int = 1):
    """
    Génère une grille du Sudoku aléatoire, 9x9
    """
    if difficulty < 1 or difficulty > 9:
        print("Difficulty must be a number from 1 to 9")
        exit()

    genesis_grid = [[0 for i in range(9)] for j in range(9)]
    random_line = random.randint(0, 8)
    random_col = random.randint(0, 8)
    random_val = random.randint(1, 9)
    genesis_grid[random_line][random_col] = random_val

    sudoku = Sudoku()
    sudoku.board = genesis_grid
    sudoku.n_lines = 3
    sudoku.n_columns = 3
    csp = CSP(sudoku)
    csp.solve_sudoku()

    random_grid = csp.get_board_from_graph()

    for j in range(9):
        for i in range(9):
            prob = random.randint(1, difficulty + 1)
            if prob > 1:
                random_grid[j][i] = 0
    
    sudoku.board = random_grid
    return sudoku


sudoku = Sudoku()
if len(sys.argv) > 2 :

    if sys.argv[1] == "random" :
        difficulty = int(sys.argv[2])
        sudoku = generate_random_sudoku(difficulty)
            
    elif sys.argv[1] == "read" :
        filename = sys.argv[2]
        sudoku.read_sudoku_file(filename)

    else :
        print_help_message()
    
    csp = CSP(sudoku)
    sudoku.print_board()
    if csp.solve_sudoku() :
        print("Sudoku solved !")
    else :
        print("No solution found...")
    sudoku.board = csp.get_board_from_graph()
    sudoku.print_board()
else :
    print_help_message()

    
