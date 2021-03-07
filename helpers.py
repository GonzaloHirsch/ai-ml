from node import Node
from board import Board
import numpy as np
from collections import deque

def printBoardsToSolution(board, solution):
    # Invert the list into a stack
    solutionStack = deque()     
    node = solution               
    
    while node.getParent() != None:
        solutionStack.append(node)
        node = node.getParent()
    
    solutionStack.append(node)

    print("Solution Cost/Depth: ", len(solutionStack) - 1)
    print("\n")
    print("Solution Steps: ")

    # Print the solution based on the stack
    while solutionStack:
        node = solutionStack.pop()
        if solutionStack:
            print(board.getPlayerMovement(node.getPlayerPosition(), solutionStack[-1].getPlayerPosition()))
