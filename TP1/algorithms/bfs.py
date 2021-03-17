from node import Node
from board import Board
import numpy as np
import constants
from collections import deque
import helpers

def solve(board):
    # Create the root
    root = Node(None, board.getPlayerPosition(), board.getBoxesPositions())

    # Map of visited nodes
    visited = {}
    visited[root] = True

    # Queue to store nodes to visit
    queue = deque()
    queue.append(root)

    foundSolution = False
    expandedNodes = 0

    # Iterates while not empty
    while queue:
        # Get the fist element in queue
        curr = queue.popleft()

        # Check if goal, if goal exit loop
        if board.isComplete(curr):
            foundSolution = True
            break
        else:
            expandedNodes += 1
            # Try to move the player to all 4 positions
            # if possible, create the node and append it to queue
            for direction in constants.ALL_DIRECTIONS:
                # Test the movement direction
                newPlayerPosition, newBoxesPosition, isPossible = board.testMovement(
                    np.copy(curr.playerPos), np.copy(curr.boxesPos), direction
                )

                # Create a new node and push it if possible
                if isPossible:
                    newNode = Node(curr, newPlayerPosition, newBoxesPosition)
                    if not newNode in visited:
                        print(newNode)
                        queue.append(newNode)
                        visited[newNode] = True

    if foundSolution:
        helpers.printBoardsToSolution(board, curr)

    if foundSolution:
        print("SOLUTION FOUND\n")
    else:
        print("SOLUTION NOT FOUND\n")

    helpers.printStats(expandedNodes, len(queue), curr)

    