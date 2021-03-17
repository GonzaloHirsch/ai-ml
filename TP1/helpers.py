from node import Node
import numpy as np
from collections import deque

def printMovesToSolution(board, solution):
    # Invert the list into a stack
    solutionStack = deque()     
    node = solution               
    
    while node.getParent() != None:
        solutionStack.append(node)
        node = node.getParent()
    
    solutionStack.append(node)

    print("Solution Cost/Depth: ", len(solutionStack) - 1)
    # print("\n")
    # print("Solution Steps: ")

    # # Print the solution based on the stack
    # while solutionStack:
    #     node = solutionStack.pop()
    #     if solutionStack:
    #         print(board.getPlayerMovement(node.getPlayerPosition(), solutionStack[-1].getPlayerPosition()))


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
        print("\n------------- MOVE " + str(node.getLevel()) + " ------------------\n")
        board.printCustomBoard(node.getBoxesPositions(), node.getPlayerPosition())        


def printStats(expandedNodes, frontier, lastNode):
    print("STATS:")
    print("Expanded Nodes:", expandedNodes)
    print("Frontier Nodes:", frontier)
    print("Solution Cost/Depth: ", lastNode.getLevel())

def sortPoints(arr):
    # Inspired by https://stackoverflow.com/questions/2828059/sorting-arrays-in-numpy-by-column
    # First sort doesn't need to be stable.
    arr = arr[arr[:,1].argsort()]
    arr = arr[arr[:,0].argsort(kind='mergesort')]
    return arr