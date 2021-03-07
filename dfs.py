from node import Node
from board import Board
import numpy as np
import constants
from collections import deque
from helpers import printBoardsToSolution

def solveDFS(board):
    # Create the root
    root = Node(None, board.getPlayerPosition(), board.getBoxesPositions())

    # Map of visited nodes
    visited = {}

    # Stack to store nodes to visit
    stack = deque()
    stack.append(root)

    foundSolution = False
    expandedNodes = 0

    # Iterates while not empty
    while stack:
        # Poping the first element
        curr = stack.pop()

        # Check if goal, if goal exit loop
        if board.isComplete(curr):
            foundSolution = True
            break
        else:
            expandedNodes += 1
            # Try to move the player to all 4 positions
            # if possible, create the node and push it to stack
            for direction in constants.ALL_DIRECTIONS:
                # Test the movement direction
                newPlayerPosition, newBoxesPosition, isPossible = board.testMovement(
                    np.copy(curr.playerPos), np.copy(curr.boxesPos), direction
                )

                # Create a new node and push it if possible
                if isPossible:
                    newNode = Node(curr, newPlayerPosition, newBoxesPosition)
                    if not newNode in visited:
                        stack.append(newNode)
                        visited[newNode] = True

    if foundSolution:
        print("SOLUTION FOUND")
    else:
        print("SOLUTION NOT FOUND")

    print("STATS:")
    print("Expanded Nodes:", expandedNodes)
    print("Frontier Nodes:", len(stack))

    if foundSolution:
        printBoardsToSolution(board, curr)
        
exampleOG = np.array([
    ['X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['X', '.', '.', '.', 'G', 'G', 'X'],
    ['X', '.', 'B', 'B', 'X', '.', 'X'],
    ['X', 'O', '.', '.', '.', '.', 'X'],
    ['X', 'X', 'X', 'X', 'X', 'X', 'X']
])

example = np.array([
    ['X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['X', '.', '.', '.', 'G', 'G', 'X'],
    ['X', '.', '.', '.', 'X', '.', 'X'],
    ['X', '.', '.', '.', '.', '.', 'X'],
    ['X', 'X', 'X', 'X', 'X', 'X', 'X']
])

# board = Board(exampleOG, [np.array([2, 2]),np.array([2, 3])], [np.array([1, 4]), np.array([1, 5])], np.array([3, 1]))

# print(exampleOG)

# solveDFS(board)
