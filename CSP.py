from Node import Node

class CSP :

    def __init__(self, sudoku) :
        self.sudoku = sudoku
        self.graph = []

    def init_graph(self) :
        sudoku_size = len(self.sudoku.board)

        # Créer les noeuds
        for l in range(sudoku_size) :
            self.graph.append([])
            for c in range(sudoku_size) :
                node = Node(l, c, self.sudoku.board[l][c])
                if node.isAssigned() :
                    node.domain = [node.value]
                else :
                    node.domain = list(range(1, sudoku_size + 1))
                self.graph[l].append(node)
        
        # Relier les noeuds en leur ajoutant des voisins
        for l in range(sudoku_size) :
            for c in range(sudoku_size) :
                # Voisins sur la même ligne
                for column in range(sudoku_size) :
                    if column != c :
                        self.graph[l][c].add_neighbour(self.graph[l][column])
                # Voisins sur la même colonne
                for line in range(sudoku_size) :
                    if line != l :
                        self.graph[l][c].add_neighbour(self.graph[line][c])
                # Voisins sur le même bloc
                block_pos_l = l // self.sudoku.n_lines
                block_pos_c = c // self.sudoku.n_columns
                for line in range(block_pos_l * self.sudoku.n_lines, block_pos_l * (self.sudoku.n_lines + 1)) :
                    for column in range(block_pos_c * self.sudoku.n_lines, block_pos_c * (self.sudoku.n_columns+ 1)) :
                        if line != l and c != column : 
                            self.graph[l][c].add_neighbour(self.graph[line][column])
    
    def solve_sudoku(self) :
        self.init_graph()

    def AC_3(self, graph) :
        pass
        


    