from CSP import CSP
from Sudoku import Sudoku

s = Sudoku()
csp = CSP(s)
s.print_board()
csp.solve_sudoku()