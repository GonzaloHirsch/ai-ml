class Heuristic:
    def __init__(self, h_id):
        self.h_id = h_id
        self.heuristic = self.heuristics[h_id]

    def __h1(node, board):
        print(1)

    def __h2(node, board):
        print(2)

    def __h3(node, board):
        print(3)

    # Exposed method to calculate the heuristic value
    def calculate(self, node, board):
        self.heuristic(node, board)

    # Map with pointers to the functions
    heuristics = {1: __h1, 2: __h2, 3: __h3}