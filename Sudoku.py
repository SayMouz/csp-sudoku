class Sudoku :
    """
    La classe Sudoku représente une grille de Sudoku.
    Le nombre de lignes et le nombres représentent la taille 
    d'un sous rectangle du sudoku. 
    Par exemple un sudoku à 3 lignes et 3 colonnes représente une grille de taille 9x9
    """

    def __init__(self, n_lines = 3, n_columns = 3) :
        self.n_lines = n_lines
        self.n_columns = n_columns
        
    def print_board(self) :
        """
        Affiche la grille de Sudoku dans le terminal.
        """

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
                if str(self.board[l][c]) == "0" :
                    print("|   ", end = "")
                else :
                    print(f"| {self.board[l][c]} ", end = "")
            print("||")
        for i in range(board_size*4 + self.n_lines + 2) :
            print("=", end = "")
        print()
 
    def read_sudoku_file(self, filename) :
        """
        Lis un fichier de sudoku est remplie la grille avec.
        Le fichier doit respecter la syntaxe indiquee dans le README.
        """
        file = open(filename)
        lines = file.readlines()

        # Lecture de la taille du sudoku
        sudoku_format = lines.pop(0).strip().split("x")
        self.n_lines = int(sudoku_format[0])
        self.n_columns = int(sudoku_format[1])

        # Lecture du sudoku
        self.board = []
        for line in lines :
            self.board.append(line.strip().split(" "))

    

                

