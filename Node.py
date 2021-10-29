
class Node :
    """
    La classe Node représente un noeud du graphe de contraintes.
    Ce noeud correspond à une case du Sudoku est possède les informations suivantes :
    - Une valeur assignée, 0 si la case est vide.
    - La liste des voisins du noeud.
    - Le domaine du noeud, c'est-à-dire les valeurs possibles pour le noeud.
    """

    def __init__(self, value) :
        self.value = value
        self.neighbours = []
        self.domain = []
    
    def add_neighbour(self, neighbour) :
        """
        Ajoute un voisin à liste de voisins.
        """
        self.neighbours.append(neighbour)
    
    def isAssigned(self) :
        """
        Indique si le noeud est assigné ou non.
        """
        return self.value != "0"
    
    def assign(self, value) :
        """
        Assigne une valeur au noeud. 
        """
        self.value = value
        self.domain = [value]

    

