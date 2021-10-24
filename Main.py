import sys
from CSP import CSP
from Sudoku import Sudoku

sudoku = Sudoku()
if len(sys.argv) > 1 :
    filename = sys.argv[1]
    sudoku.read_sudoku_file(filename)
    csp = CSP(sudoku)
    sudoku.print_board()
    csp.solve_sudoku()
else :
    print("Please choose a sudoku file.")
    print("Example : python3 Main.py mysudoku.txt")
