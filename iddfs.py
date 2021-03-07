from node import Node
from board import Board
import numpy as np
import constants
from collections import deque
from helpers import printBoardsToSolution

def solveIDDFS(board, maxDepth):
    # Create the root
    root = Node(None, board.getPlayerPosition(), board.getBoxesPositions())

    # Map of visited nodes
    visited = {}

    # Queue of frontier nodes
    # These are the nodes that must be analyzed in the next iteration
    frontier = deque()
    frontier.append(root)

    # Variables
    foundSolution = False
    expandedNodes = 0

    while frontier:

        # Set up the DFS stack
        stack = deque()
        stack.append(frontier.popleft())
        
        currDepth = 0

        # Iterates while not empty
        while stack and currDepth < maxDepth:

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

                            # If the next node is the limit, add to the frontier
                            # Will be analyzed in the next iteration
                            if (currDepth + 1) == maxDepth:
                                frontier.append(newNode)
                            else:
                                stack.append(newNode)
                                visited[newNode] = True

            currDepth += 1

        if foundSolution:
            break

    if foundSolution:
        print("SOLUTION FOUND")
    else:
        print("SOLUTION NOT FOUND")

    print("STATS:")
    print("Expanded Nodes:", expandedNodes)
    print("Frontier Nodes:", len(stack))

    if foundSolution:
        printBoardsToSolution(board, curr)


    # Iterate from the goal up to the root in order to get the complete list of actions
