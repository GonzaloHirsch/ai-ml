
class Board:
    def __init__(self, board, playerPos, targetsPos, boxesPos):
        self.board = board
        self.playerPos = playerPos
        self.targetsPos = targetsPos
        self.boxesPos = boxesPos

    def getPlayerPosition(self):
        return self.playerPos