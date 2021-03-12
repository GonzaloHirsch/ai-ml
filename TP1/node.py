import numpy as np

class Node:
    def __init__(self, parent, playerPos, boxesPos):

        if parent is None:
            self.level = 0
        else:
            self.level = parent.getLevel() + 1

        self.parent = parent
        self.playerPos = playerPos
        # self.boxesPos = np.sort(boxesPos, axis=0)
        self.boxesPos = boxesPos
        self.computedHash = hash(self.__computeHashString())

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

    def __computeHashString(self):
        data = []
        for box in self.boxesPos:
            data.append((box[0], box[1]))
        return hash(str(hash((self.playerPos[0], self.playerPos[1]))) + str(hash(frozenset(data))))

    def __hash__(self):
        return self.computedHash

    def __eq__(self, other):
        return self.computedHash == other.__hash__()