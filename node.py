import numpy as np

class Node:
    def __init__(self, parent, playerPos, boxesPos):

        if parent is None:
            self.level = 0
        else:
            self.level = parent.getLevel() + 1

        self.parent = parent
        self.playerPos = playerPos
        self.boxesPos = np.sort(boxesPos, axis=0)
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
        s = str(self.playerPos[0]) + str(self.playerPos[1])
        for box in self.boxesPos:
            s = s + str(box[0]) + str(box[1])
        return s

    def __hash__(self):
        return self.computedHash

    def __eq__(self, other):
        return self.computedHash == other.__hash__()