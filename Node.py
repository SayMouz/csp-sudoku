class Node :

    def __init__(self, line, column, value) :
        self.line = line
        self.column = column

        self.value = value
        self.neighbours = []

        self.domain = []
    
    def add_neighbour(self, neighbour) :
        self.neighbours.append(neighbour)
    
    def isAssigned(self) :
        return self.value != 0

    

