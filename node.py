
class Node:
    def __init__(self, parent, playerPos, boxesPos):
        self.parent = parent
        self.playerPos = playerPos
        self.boxesPos = boxesPos
        self.computedHash = hash(self.__computeHashString())

    def getBoxesPositions(self):
        return self.boxesPos

    def getParent(self):
        return self.parent

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