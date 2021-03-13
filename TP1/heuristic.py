class Heuristic:
    def __init__(self, h_id):
        self.h_id = h_id
        self.heuristic = self.heuristics[h_id]
        self.tree = None

    # -----------------------------------------------------------------
    # HELPER FUNCTIONS
    # -----------------------------------------------------------------

    def __min_element(arr):
        # Arbitrary minimum
        min = 100000
        for elem in arr:
            if elem > 0 and elem < min:
                min = elem
        return min

    # -----------------------------------------------------------------
    # HEURISTIC FUNCTIONS
    # -----------------------------------------------------------------

    def __h1(self, node, board):
        min = 100000
        for target in board.targetsPos:
            for box in node.boxesPos:
                val = sum(abs(target - box))
                if val < min and val > 0:
                    min = val
        return val

    def __h2(self, node, board):
        print(2)

    def __h3(self, node, board):
        print(3)

    # Exposed method to calculate the heuristic value
    def calculate(self, node, board):
        return self.heuristic(self, node, board)

    # Map with pointers to the functions
    heuristics = {1: __h1, 2: __h2, 3: __h3}

    