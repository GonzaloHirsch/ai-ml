from node import Node
from board import Board
import numpy as np
import constants
from collections import deque
import helpers

def solve(board, maxDepth):
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
    lookaheadLimit = int(0.75 * maxDepth)

    while frontier:

        node = frontier.popleft()

        if not node in visited:
            visited[node] = node.getLevel()

        # Set up the DFS stack
        stack = deque()
        stack.append(node)
        
        currDepth = node.getLevel()
        currMaxDepth = currDepth + maxDepth

        # print(node)

        # Iterates while not empty
        while stack:

            # Poping the first element
            curr = stack.pop()
            currDepth = curr.getLevel()

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
                        
                        # If the node wasnt visited or it has been but took  
                        # at least 10 more cost to get to it, visit it again
                        if not newNode in visited or (lookaheadLimit > 0 and (visited[newNode] - lookaheadLimit) > newNode.getLevel()):
                            visited[newNode] = newNode.getLevel()
                            # If the next node is the limit, add to the frontier
                            # Will be analyzed in the next iteration
                            if newNode.getLevel() >= currMaxDepth:
                                frontier.append(newNode)
                            else:
                                stack.append(newNode)


        if foundSolution:
            break

    if foundSolution:
        # helpers.printMovesToSolution(board, curr)
        helpers.printBoardsToSolution(board, curr)
    
    if foundSolution:
        print("SOLUTION FOUND\n")
    else:
        print("SOLUTION NOT FOUND\n")

    helpers.printStats(expandedNodes, len(frontier) + len(stack), curr)
        


    # Iterate from the goal up to the root in order to get the complete list of actions
