from Node import Node

class CSP :

    def __init__(self, sudoku) :
        self.sudoku = sudoku
        self.graph = []
        self.count = 0

    def init_graph(self) :
        sudoku_size = len(self.sudoku.board)

        # Créer les noeuds
        for l in range(sudoku_size) :
            self.graph.append([])
            for c in range(sudoku_size) :
                node = Node(self.sudoku.board[l][c])
                if node.isAssigned() :
                    node.domain = [node.value]
                else :
                    node.domain = self.sudoku.MAXIMUM_DOMAIN[0:sudoku_size]
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
                for line in range(block_pos_l * self.sudoku.n_lines, (block_pos_l + 1) * self.sudoku.n_lines) :
                    for column in range(block_pos_c * self.sudoku.n_columns, (block_pos_c + 1) * self.sudoku.n_columns) :
                        if line != l and c != column : 
                            self.graph[l][c].add_neighbour(self.graph[line][column])
    
    def solve_sudoku(self) :
        self.init_graph()
        self.AC_3()
        solved = self.backtracking_search()
        if solved :
            print("Sudoku solved !")
        else :
            print("No solution found...")
        self.sudoku.board = self.get_board_from_graph()
        self.sudoku.print_board()
    
    def backtracking_search(self) :
        return self.recursive_backtracking()

    def recursive_backtracking(self) :

        if self.all_assigned() : 
            return True
        
        node = self.select_unassigned_node()
        self.order_domain_values(node)
        n_values = len(node.domain)
        
        for i in range(n_values) :
            value = node.domain[i]
            values_before_assignment, domains_before_assignment = self.get_values_domains_copy()
            node.assign(value)
            self.AC_3()

            if not self.is_there_an_empty_domain() :
                if self.recursive_backtracking() :
                    return True

            for l in range(len(self.graph)) :
                for c in range(len(self.graph)) :
                    self.graph[l][c].domain = domains_before_assignment[l][c]
                    self.graph[l][c].value = values_before_assignment[l][c]
                
        return False

    def AC_3(self) :
        # Initialiser la queue avec tous les arcs de l'arbre
        queue = []
        for l in range(len(self.graph)) :
            for c in range(len(self.graph)) :
                for neighbour in self.graph[l][c].neighbours :
                    queue.append([self.graph[l][c], neighbour])

        while queue :
            arc = queue.pop(0)
            if self.remove_inconsistent_values(arc[0], arc[1]) :
                for neighbour in arc[0].neighbours :
                    if [neighbour, arc[0]] not in queue :
                        queue.append([neighbour, arc[0]])

    def remove_inconsistent_values(self, node_to_update, neighbour_node) :  
        removed = False
        # S'il le noeud voisin a au moins 2 valeurs légales, il y'a forcément une valeur de permis pour 
        # chaque valeur du domaine à mettre à jour.
        if len(neighbour_node.domain) < 2 :
            for value in node_to_update.domain :
                if value in neighbour_node.domain :
                    node_to_update.domain.remove(value)
                    removed = True
        
        if len(node_to_update.domain) == 1 :
            node_to_update.assign(node_to_update.domain[0])
        
              
        return removed

    def select_unassigned_node(self) :
        
        u_nodes = []
        for l in range(len(self.graph)) :
            for c in range(len(self.graph)) :
                if not self.graph[l][c].isAssigned() :
                    u_nodes.append(self.graph[l][c])
        
        # Utilise un tri par insertion, les noeuds sont comparés
        # avec MRV et Degree heuristic
        for n in range(1, len(u_nodes)) :
            key = u_nodes[n]
            j = n - 1
            while j>=0 and self.MRV_degree_heuristic_comparison(key, u_nodes[j], u_nodes) :
                u_nodes[j+1] = u_nodes[j]
                j = j-1
            u_nodes[j+1] = key

        return u_nodes[0]

    def MRV_degree_heuristic_comparison(self, n1, n2, unassigned_nodes) :
        # MRV
        if len(n1.domain) < len(n2.domain) :
            return True
        # Si égalité : degree heuristic
        elif len(n1.domain) == len(n2.domain) :
            n1_unassigned_neighbours = 0
            n2_unassigned_neighbours = 0
            for u_node in unassigned_nodes :
                if u_node in n1.neighbours :
                    n1_unassigned_neighbours = n1_unassigned_neighbours + 1
                if u_node in n2.neighbours :
                    n2_unassigned_neighbours = n2_unassigned_neighbours + 1
            if n1_unassigned_neighbours > n2_unassigned_neighbours :
                return True
        
        return False

    def order_domain_values(self, node) :
        # Utilise un tri par insertion
        for n in range(1, len(node.domain)) :
            key = node.domain[n]
            j = n - 1
            while j>=0 and self.lcv_comparison(node, key, node.domain[j]) :
                node.domain[j+1] = node.domain[j]
                j = j-1
            node.domain[j+1] = key


    def lcv_comparison(self, node, value1, value2) :
        count1 = 0
        count2 = 0
        for ngb in node.neighbours :
            if value1 in ngb.domain and not ngb.isAssigned() :
                count1 = count1 + 1
            if value2 in ngb.domain and not ngb.isAssigned() :
                count2 = count2 + 1
        return count1 < count2

    def get_values_domains_copy(self) :
        domains_copy = []
        values_copy = []
        for l in range(len(self.graph)) :
            domains_copy.append([])
            values_copy.append([])
            for c in range(len(self.graph)) :
                domains_copy[l].append(self.graph[l][c].domain.copy())
                values_copy[l].append(self.graph[l][c].value)
        return values_copy, domains_copy

    def all_assigned(self) : 
        for l in range(len(self.graph)) :
            for c in range(len(self.graph)) :
                if not self.graph[l][c].isAssigned() :
                    return False
        return True
        
    def is_there_an_empty_domain(self) :
        for l in range(len(self.graph)) :
            for c in range(len(self.graph)) :
                if len(self.graph[l][c].domain) < 1 :
                    return True
        return False

    def get_board_from_graph(self) : 
        board = []
        for l in range(len(self.graph)) :
            board.append([])
            for c in range(len(self.graph)) :
                board[l].append(self.graph[l][c].value)
        return board
        
        
    
    

        
        


    