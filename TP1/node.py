import numpy as np

class Node:
    INSTANCES = 0
    def __init__(self, parent, playerPos, boxesPos):
        self.id = Node.INSTANCES
        if parent is None:
            self.level = 0
        else:
            self.level = parent.getLevel() + 1

        self.parent = parent
        self.playerPos = playerPos
        self.boxesPos = boxesPos
        self.computedHash = hash(self.__computeHashString())
        self.heuristic = 0
        Node.INSTANCES += 1

    def getBoxesPositions(self):
        return self.boxesPos

    def getParent(self):
        return self.parent

    def getLevel(self):
        return self.level

    def getPlayerPosition(self):
        return self.playerPos

    def getHash(self):
        return self.playerPos

    def getFValue(self):
        return self.level + self.heuristic

    def setHeuristic(self, heuristic):
        self.heuristic = heuristic

    def __computeHashString(self):
        data = []
        for box in self.boxesPos:
            data.append((box[0], box[1]))
        return hash(str(hash((self.playerPos[0], self.playerPos[1]))) + str(hash(frozenset(data))))

    def __hash__(self):
        return self.computedHash

    def __eq__(self, other):
        return self.computedHash == other.__hash__()

    def __str__(self):
        return "level: " + str(self.level) + " heur: " + str(self.heuristic) + " player: " + str(self.playerPos) + " boxes: " + str(self.boxesPos)