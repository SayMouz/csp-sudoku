class Sudoku :

    MAXIMUM_DOMAIN = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G"]

    def __init__(self, n_lines = 3, n_columns = 3) :
        self.n_lines = n_lines
        self.n_columns = n_columns
        self.board = [
            [0, 0, 0, 0, 4, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 9, 4, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 6, 7],
            [5, 0, 0, 9, 7, 0, 0, 0, 3],
            [9, 4, 0, 0, 8, 0, 0, 2, 5],
            [8, 0, 0, 0, 2, 1, 0, 0, 4],
            [2, 6, 0, 0, 9, 0, 0, 0, 0],
            [0, 0, 1, 2, 0, 7, 0, 0, 0],
            [7, 0, 0, 0, 1, 0, 0, 0, 0],
        ]
    
    def print_board(self) :
        board_size = self.n_lines * self.n_columns
        for l in range(board_size) :
            for i in range(board_size*4 + self.n_lines + 2) :
                if l % self.n_lines == 0 :
                    print("=", end = "")
                else :
                    print("-", end = "")
            print()
            for c in range(board_size) :
                if c % self.n_columns == 0 :
                    print("|", end = "")
                if self.board[l][c] == "0" :
                    print("|   ", end = "")
                else :
                    print(f"| {self.board[l][c]} ", end = "")
            print("||")
        for i in range(board_size*4 + self.n_lines + 2) :
            print("=", end = "")
        print()
    
    def read_sudoku_file(self, filename) :
        file = open(filename)
        lines = file.readlines()

        sudoku_format = lines.pop(0).strip().split("x")
        self.n_lines = int(sudoku_format[0])
        self.n_columns = int(sudoku_format[1])

        self.board = []
        for line in lines :
            self.board.append(line.strip().split(" "))

                

