import constants
from constants import BoardElement
import numpy as np
from helpers import sortPoints

class Board:
    def __init__(self, board, boxesPos, targetsPos, playerPos):
        self.board = board
        self.boxesPos = boxesPos
        self.targetsPos = sortPoints(targetsPos)
        self.playerPos = playerPos

    def getPlayerPosition(self):
        return self.playerPos

    def getBoxesPositions(self):
        return self.boxesPos

    def getTargetPosition(self):
        return self.targetsPos

    def isComplete(self, node):
        sortedBoxes = sortPoints(node.getBoxesPositions())
        for i in range(len(sortedBoxes)):
            if not np.array_equal(sortedBoxes[i], self.targetsPos[i]):
                return False
        return True


    def getPlayerMovement(self, oldPosition, newPosition):
        delta = newPosition - oldPosition
        if np.array_equal(delta, constants.UP):
            return "MOVE UP"
        elif np.array_equal(delta, constants.RIGHT):
            return "MOVE RIGHT"
        elif np.array_equal(delta, constants.DOWN):
            return "MOVE DOWN"
        else:
            return "MOVE LEFT"

    # Determines if an object's position overlaps with any box
    def __objectOverlapsBox(self, objectPosition, boxesPosition):
        for i, box in enumerate(boxesPosition, start=0):
            if np.array_equal(objectPosition, box):
                return True, i
        return False, i

    def testMovement(self, playerPosition, boxesPosition, direction):
        # Calculate new player position
        newPlayerPosition = playerPosition + direction

        # Get the type of box to move to
        targetBoxToMove = self.board[newPlayerPosition[0], newPlayerPosition[1]]

        # In case it hits a wall when moving
        if targetBoxToMove == BoardElement.WALL:
            return playerPosition, boxesPosition, False
        
        # In case the player wants to move to a blank space, return new player pos
        playerOverlaps, index = self.__objectOverlapsBox(newPlayerPosition, boxesPosition)
        if not playerOverlaps:
            return newPlayerPosition, boxesPosition, True

        # In case the player wants to move a box
        # Position of the other element
        newBoxPosition = newPlayerPosition + direction

        # Box in the other element position
        nextElementToMove = self.board[newBoxPosition[0], newBoxPosition[1]]
        
        # Position of other box overlaps with box
        boxOverlaps, newIndex = self.__objectOverlapsBox(newBoxPosition, boxesPosition)

        # If the other box is a wall or a box 
        if nextElementToMove == BoardElement.WALL or boxOverlaps:
            return playerPosition, boxesPosition, False

        # In case the box is moved successfully, we store the new position of that box
        boxesPosition[index] = newBoxPosition
        return newPlayerPosition, boxesPosition, True


    def printCustomBoard(self, boxesPos, playerPos):
        self.boxesPos = boxesPos
        self.playerPos = playerPos

        self.printBoard()

    
    def printBoard(self):

        rows = self.board.shape[0]
        cols = self.board.shape[1]

        currBoard = np.copy(self.board)

        for boxIdx in range(0, len(self.boxesPos)):
            i = int(self.boxesPos[boxIdx][0])
            j = int(self.boxesPos[boxIdx][1])
            currBoard[i][j] = BoardElement.BOX.value
            boxIdx += 1

        currBoard[self.playerPos[0]][self.playerPos[1]] = BoardElement.PLAYER.value

        for rowIdx in range(0, rows):            
            for colIdx in range(0, cols):
                print(currBoard[rowIdx][colIdx], end = "")
            
            print("")

                

