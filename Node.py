class Node :

    def __init__(self, value) :
        self.value = value
        self.neighbours = []

        self.domain = []
    
    def add_neighbour(self, neighbour) :
        self.neighbours.append(neighbour)
    
    def isAssigned(self) :
        return self.value != "0"
    
    def assign(self, value) :
        self.value = value
        self.domain = [value]

    

