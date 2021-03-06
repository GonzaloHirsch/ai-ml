from node import Node
from board import Board
import numpy as np
import constants
from collections import deque

def solveBFS(board):
    # Create the root
    root = Node(None, board.getPlayerPosition(), board.getBoxesPositions())

    # Map of visited nodes
    visited = {}

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
                        queue.append(newNode)
                        visited[newNode] = True

    if foundSolution:
        print("SOLUTION FOUND \n")
    else:
        print("SOLUTION NOT FOUND \n")

    print("STATS:")
    print("Expanded Nodes: ", expandedNodes)
    print("Frontier Nodes: ", len(queue))
    print("\n")

    if foundSolution:
        # Invert the list into a stack
        solutionStack = deque()                    
        while curr.getParent() != None:
            solutionStack.append(curr)
            curr = curr.getParent()
        solutionStack.append(curr)
        print("Solution Cost/Depth: ", len(solutionStack) - 1)
        print("\n")
        print("Solution Steps: ")
        # Print the solution based on the stack
        while solutionStack:
            curr = solutionStack.pop()
            if solutionStack:
                print(board.getPlayerMovement(curr.getPlayerPosition(), solutionStack[-1].getPlayerPosition()))