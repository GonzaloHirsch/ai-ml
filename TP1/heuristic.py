import heapq

class Heuristic:
    def __init__(self, h_id):
        self.h_id = h_id
        self.heuristic = self.heuristics[h_id]

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

    def __manhattan(c1, c2):
        return sum(abs(c1 - c2))

    # -----------------------------------------------------------------
    # HEURISTIC FUNCTIONS
    # -----------------------------------------------------------------

    def __h1(self, node, board):
        s = 0
        for target in board.targetsPos:
            min = 10000000
            for box in node.boxesPos:
                val = Heuristic.__manhattan(target, box)
                if val < min:
                    min = val
            s += min
        return s

    def __h2(self, node, board):
        min = 10000000
        for box in node.boxesPos:
            val = Heuristic.__manhattan(node.playerPos, box)
            if val < min and val > 0:
                min = val
        return min

    def __h3(self, node, board):

        # Variable declaration
        targets = board.getTargetPosition()
        boxes = node.getBoxesPositions()
        distanceHeap = []
        claimedTargets = {}
        claimedBoxes = {}
        distanceSum = 0

        # Storing the distance between each target and box into a priority queue
        for tIdx in range(len(targets)):
            for bIdx in range(len(boxes)):
                distance = Heuristic.__manhattan(targets[tIdx], boxes[bIdx])
                distanceHeap.append((distance, tIdx, bIdx))
        
        heapq.heapify(distanceHeap)

        # Will keep 1 distance between each box and target
        while distanceHeap:
            curr = heapq.heappop(distanceHeap)
            if curr[1] not in claimedTargets and curr[2] not in claimedBoxes:
                claimedTargets[curr[1]] = True
                claimedBoxes[curr[2]] = True
                distanceSum += curr[0]

        # Will return the sum of the distances and the min distance from player to box
        return distanceSum + self.__h2(node, board)

    # Exposed method to calculate the heuristic value
    def calculate(self, node, board):
        return self.heuristic(self, node, board)

    # Map with pointers to the functions
    heuristics = {1: __h1, 2: __h2, 3: __h3}

    