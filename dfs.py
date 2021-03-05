from node import Node
from board import Board
import numpy as np
import constants
from collections import deque

def solveDFS(board):
    # Create the root
    root = Node(None, board.getPlayerPosition(), board.getBoxesPositions())

    # Map of visited nodes
    visited = {}

    # Stack to store nodes to visit
    stack = deque()
    stack.append(root)

    foundSolution = False

    # Iterates while not empty
    while stack:
        # Poping the first element
        curr = stack.pop()

        # Check if goal, if goal exit loop
        if board.isComplete(curr):
            foundSolution = True
            break
        else:
            # Try to move the player to all 4 positions
            # if possible, create the node and push it to stack
            for direction in constants.ALL_DIRECTIONS:
                # Test the movement direction
                newPlayerPosition, newBoxesPosition, isPossible = board.testMovement(
                    np.copy(curr.playerPos), np.copy(curr.boxesPos), direction)

                # Create a new node and push it if possible
                if isPossible:
                    newNode = Node(curr, newPlayerPosition, newBoxesPosition)
                    if not newNode in visited:
                        stack.append(newNode)
                        visited[newNode] = True

    if foundSolution:
        print("SOLUTION FOUND")
        # Invert the list into a stack
        solutionStack = deque()                    
        while curr.getParent() != None:
            solutionStack.append(curr)
            curr = curr.getParent()
        solutionStack.append(curr)

        # Print the solution based on the stack
        while solutionStack:
            curr = solutionStack.pop()
            if solutionStack:
                print(board.getPlayerMovement(curr.getPlayerPosition(), solutionStack[-1].getPlayerPosition()))
    else:
        print("SOLUTION NOT FOUND")

    # Iterate from the goal up to the root in order to get the complete list of actions

exampleOG = np.array([
    ['X', 'X', 'X', 'X', 'X', 'X'],
    ['X', '.', '.', '.', 'G', 'X'],
    ['X', '.', 'B', 'X', '.', 'X'],
    ['X', 'O', '.', '.', '.', 'X'],
    ['X', 'X', 'X', 'X', 'X', 'X']
])

example = np.array([
    ['X', 'X', 'X', 'X', 'X', 'X'],
    ['X', '.', '.', '.', 'G', 'X'],
    ['X', '.', '.', 'X', '.', 'X'],
    ['X', '.', '.', '.', '.', 'X'],
    ['X', 'X', 'X', 'X', 'X', 'X']
])

board = Board(example, np.array([3, 1]), [np.array([1, 4])], [np.array([2, 2])])

print(exampleOG)

solveDFS(board)
