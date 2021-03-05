import constants
import numpy as np

class Board:
    def __init__(self, board, playerPos, targetsPos, boxesPos):
        self.board = board
        self.playerPos = playerPos
        self.targetsPos = targetsPos
        self.boxesPos = boxesPos

    def getPlayerPosition(self):
        return self.playerPos

    def getBoxesPositions(self):
        return self.boxesPos

    def isComplete(self, node):
        sortedTargets = np.sort(self.targetsPos)
        sortedBoxes = np.sort(node.getBoxesPositions())
        for i in range(len(sortedBoxes)):
            if not np.array_equal(sortedBoxes[i], sortedTargets[i]):
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

    # Determines if a player position overlaps with any box
    def __playerOverlapsBox(self, playerPosition, boxesPosition):
        for i, box in enumerate(boxesPosition, start=0):
            if np.array_equal(playerPosition, box):
                return True, i
        return False, i

    def testMovement(self, playerPosition, boxesPosition, direction):
        # Calculate new player position
        newPlayerPosition = playerPosition + direction

        # Get the type of block to move to
        targetBlockToMove = self.board[newPlayerPosition[0], newPlayerPosition[1]]

        # In case it hits a wall when moving
        if targetBlockToMove == constants.WALL:
            return playerPosition, boxesPosition, False
        
        # In case the player wants to move to a blank space, return new player pos
        playerOverlaps, index = self.__playerOverlapsBox(newPlayerPosition, boxesPosition)
        if not playerOverlaps:
            return newPlayerPosition, boxesPosition, True

        # In case the player wants to move a box
        # Position of the other element
        nextNewPlayerPosition = newPlayerPosition + direction
        # Block in the other element position
        nextTargetBlockToMove = self.board[nextNewPlayerPosition[0], nextNewPlayerPosition[1]]
        # Position of other block overlaps with box
        blockOverlaps, newIndex = self.__playerOverlapsBox(nextNewPlayerPosition, boxesPosition)

        # If the other block is a wall or a box 
        if nextTargetBlockToMove == constants.WALL or blockOverlaps:
            return playerPosition, boxesPosition, False

        # In case the box is moved successfully, we store the new position of that box
        boxesPosition[index] = nextNewPlayerPosition
        return newPlayerPosition, boxesPosition, True


