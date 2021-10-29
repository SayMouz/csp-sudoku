from Node import Node

class CSP :
    """
    La classe CSP implémente un agent capable de résoudre des sudoku.
    """

    # Le domaine maximum pour une case. On se limite ici à des Sudoku de taille 16x16 maximum.
    MAXIMUM_DOMAIN = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G"]

    def __init__(self, sudoku) :
        """
        Constructeur qui prend en paramètre un sudoku de la classe Sudoku.
        """
        self.sudoku = sudoku
        # Graphe de contraintes du CSP 
        self.graph = [] 

    def init_graph(self) :
        """
        Initialise le graphe de contraintes du CSP avec le Sudoku.
        """
        sudoku_size = len(self.sudoku.board)

        #### Créer les noeuds ####
        for l in range(sudoku_size) :
            self.graph.append([])
            for c in range(sudoku_size) :
                node = Node(str(self.sudoku.board[l][c]))
                if node.isAssigned() :
                    # Si le noeud est assigné, le domaine est réduit à la valeur assignée
                    node.domain = [node.value]
                else :
                    # Sinon le domaine est égale à toutes les valeurs possibles selon la taille du Sudoku
                    node.domain = self.MAXIMUM_DOMAIN[0:sudoku_size]
                self.graph[l].append(node)
        
        #### Relier les noeuds en leur ajoutant des voisins ####
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
                        # On ne rajoute pas les voisins qui sont sur la même ligne ou même colonne
                        if line != l and c != column : 
                            self.graph[l][c].add_neighbour(self.graph[line][column])
    
    def solve_sudoku(self) :
        """
        Résoud le sudoku.
        Renvoie True si une solution a été trouvée.
        """

        # On crée le graphe de contraintes
        self.init_graph()
        # Une première itération de AC3 pour réduire les domaines
        self.AC_3()
        # Appel de la function de backtracking
        return self.backtracking_search()
    
    def backtracking_search(self) :
        """
        Fonction de recherche avec backtracking. 
        Résoud le sudoku représenté par le graphe de contraintes et 
        renvoie True ou False en fonction de si une solution a été trouvée ou non.
        """
        return self.recursive_backtracking()

    def recursive_backtracking(self) :
        """
        Fonction récursive de backtracking. 
        """

        # Si toutes les noeuds/cases sont assignés, 
        if self.all_assigned() : 
            return True
        
        # Selectionne un noeud à assigner avec les algorithmes MRV et Degree heuristic
        node = self.select_unassigned_node()

        # Trie les valeurs du domaine du noeud sélectionné selon l'algorithme LCV
        self.order_domain_values(node)

        # Pour chaque valeur du domaine du noeud
        n_values = len(node.domain)
        for i in range(n_values) :
            value = node.domain[i]

            # On sauvegarde une copie du graphe afin de le réassigner si besoin
            values_before_assignment, domains_before_assignment = self.get_values_domains_copy()
            # On assigne la valeur au noeud 
            node.assign(value)
            # L'algorithme AC3 réduit les domaines après l'assignation
            self.AC_3()

            # Si il y a un domaine vide, inutile de continuer
            if not self.is_there_an_empty_domain() :
                # Sinon, on assigne le prochain noeud en rappelant la fonction recursivement
                if self.recursive_backtracking() :
                    return True

            # Si pas de solution trouvée, on remet le graphe dans son état précédent et on passe à la prochaine valeur
            for l in range(len(self.graph)) :
                for c in range(len(self.graph)) :
                    self.graph[l][c].domain = domains_before_assignment[l][c]
                    self.graph[l][c].value = values_before_assignment[l][c]

        # Arrivé ici, aucune solution n'a été trouvée, on retourne alors en arrière        
        return False

    def AC_3(self) :
        """
        Applique l'algorithme AC3 pour réduire les domaines des noeuds du graphe
        """

        # Initialise la queue avec tous les arcs du graphe
        queue = []
        for l in range(len(self.graph)) :
            for c in range(len(self.graph)) :
                for neighbour in self.graph[l][c].neighbours :
                    queue.append([self.graph[l][c], neighbour])

        # Traite tous les arcs de la queue 
        while queue :
            arc = queue.pop(0)
            # Si le domaine d'un noeud a été réduit.
            if self.remove_inconsistent_values(arc[0], arc[1]) :
                # Il faut traiter tous ses noeuds voisins avec le noeud dont le domaine a été réduit.
                for neighbour in arc[0].neighbours :
                    if [neighbour, arc[0]] not in queue :
                        queue.append([neighbour, arc[0]])

    def remove_inconsistent_values(self, node_to_update, neighbour_node) :
        """
        Cette fonction réduit le domaine du noeud node_to_update en fonction
        du domaine d'un noeud voisin neighbour_node.
        Renvoie True s'il y a eu une modification du domaine de node_to_update,
        False sinon.
        """  

        removed = False

        # S'il le noeud voisin a au moins 2 valeurs légales dans son domaine, 
        # il y'a forcément une valeur possible pour chaque valeur du domaine du noeud à mettre à jour.
        if len(neighbour_node.domain) < 2 :
            # Sinon, il faut retirer la valeur du domaine de neighbour_node au domaine de node_to_update
            for value in node_to_update.domain :
                if value in neighbour_node.domain :
                    node_to_update.domain.remove(value)
                    removed = True
        
        # Si le noeud n'a qu'une seule valeur dans son domaine
        # Alors cette valeur lui est assignée directement pour gagner du temps
        if len(node_to_update.domain) == 1 :
            node_to_update.assign(node_to_update.domain[0])
        
        return removed

    def select_unassigned_node(self) :
        """
        Sélectionne un noeud du graphe non assigné.
        Le choix est fait selon les algorithmes MRV et Degree heuristic.
        """

        # On récupère tous les noeuds non assignés
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

        # On retourne le premier noeud de la liste
        return u_nodes[0]

    def MRV_degree_heuristic_comparison(self, n1, n2, unassigned_nodes) :
        """
        Compare deux noeuds selon les heuristiques MRV et Degree heuristic.
        Renvoie True si le noeud n1 devrait être explorer avant le noeud n2.
        """

        # Première comparaison avec MRV. n1 passe avant n2 si son domaine est plus petit.
        if len(n1.domain) < len(n2.domain) :
            return True

        # Si égalité : degree heuristic
        # n1 passe avant n2 s'il possède le plus grand nombre de voisins non assignés.
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
        """
        Tri les valeurs du domaine du noeud selon l'heuristique LCV (Least Constraining Value)
        """

        # Utilise un tri par insertion
        for n in range(1, len(node.domain)) :
            key = node.domain[n]
            j = n - 1
            while j>=0 and self.lcv_comparison(node, key, node.domain[j]) :
                node.domain[j+1] = node.domain[j]
                j = j-1
            node.domain[j+1] = key


    def lcv_comparison(self, node, value1, value2) :
        """
        Compare deux valeurs pour un noeud selon LCV.
        Renvoie True si value1 doit passer avant value2.
        """

        # value1 passe avant value2 si cette valeur affecte le plus petit
        # nombre de voisins non assignés.
        count1 = 0
        count2 = 0
        for ngb in node.neighbours :
            if value1 in ngb.domain and not ngb.isAssigned() :
                count1 = count1 + 1
            if value2 in ngb.domain and not ngb.isAssigned() :
                count2 = count2 + 1
        return count1 < count2

    def get_values_domains_copy(self) :
        """
        Réalise une copie des valeurs et des domaines
        des noeuds du graphe du contraintes.
        """
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
        """
        Renvoie True si tous les noeuds du graphe sont assignés
        """ 
        for l in range(len(self.graph)) :
            for c in range(len(self.graph)) :
                if not self.graph[l][c].isAssigned() :
                    return False
        return True
        
    def is_there_an_empty_domain(self) :
        """
        Renvoie True s'il y a au moins un noeud du graphe avec un domaine vide.
        """
        for l in range(len(self.graph)) :
            for c in range(len(self.graph)) :
                if len(self.graph[l][c].domain) < 1 :
                    return True
        return False

    def get_board_from_graph(self) : 
        """
        Construit une grille du Sudoku à partir du graphe de contraintes
        """
        board = []
        for l in range(len(self.graph)) :
            board.append([])
            for c in range(len(self.graph)) :
                board[l].append(self.graph[l][c].value)
        return board
        
        
    
    

        
        


    