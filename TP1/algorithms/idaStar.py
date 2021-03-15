from node import Node
from board import Board
import numpy as np
import constants
from collections import deque
import helpers
import heapq

def solve(board, heuristic):
    # Map of visited nodes
    visited = {}
    
    # Create the root
    root = Node(None, board.getPlayerPosition(), board.getBoxesPositions())
    root.setHeuristic(heuristic.calculate(root, board))

    # Priority queue for frontier nodes
    # Elements are (heuristic, hash, Node) to provide uniqueness
    frontierHeap = [(root.getFValue(), root.heuristic, root.id, root)]
    heapq.heapify(frontierHeap)

    foundSolution = False
    expandedNodes = 0

    # Iterates while not empty
    while frontierHeap and not foundSolution:
        # Poping the first element, keeping the 
        node = heapq.heappop(frontierHeap)
        node = node[3]                     

        if not node in visited:
            visited[node] = node.getLevel()

        # Set up the DFS stack
        stack = deque()
        stack.append(node)

        limit = node.getFValue()

        #print("Limit = ", limit)

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

                            # Calculate heuristic and store it
                            newNode.setHeuristic(heuristic.calculate(newNode, board))
                            
                            # Cost + heuristic = f
                            fvalue = newNode.getFValue()

                            # Do not want to continue DFS with this node if it exceeds the limit
                            # Will add it to the frontier heap
                            if fvalue > limit:
                                heapq.heappush(frontierHeap, (fvalue, newNode.heuristic, newNode.id, newNode))
                            else: 
                                stack.append(newNode)
                                visited[newNode] = newNode.getLevel() 
                    
   

    if foundSolution:
        print("SOLUTION FOUND")
    else:
        print("SOLUTION NOT FOUND")

    helpers.printStats(expandedNodes, frontierHeap)

    if foundSolution:
        helpers.printMovesToSolution(board, curr)
        helpers.printBoardsToSolution(board, curr)
