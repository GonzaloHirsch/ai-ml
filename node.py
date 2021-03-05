
class Node:
    def __init__(self, parent, playerPos, boxesPos):
        self.parent = parent
        self.playerPos = playerPos
        self.boxesPos = boxesPos

    def getBoxesPositions(self):
        return self.boxesPos