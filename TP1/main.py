from constants import SearchMethods
from board import Board
from inputParser import generateConfigDetails, generateMatrixAndPositions
from algorithms import dfs
from algorithms import iddfs
from algorithms import bfs
from algorithms import greedy
from heuristic import Heuristic
import time

BOARD_INPUT = "input/board.txt"
CONFIG_INPUT = "input/configuration.json"

def generateAndRunGame(configFile, matrixFile):
    # Parse config
    config = generateConfigDetails(configFile)

    # Check algorithm
    try:
        config.algorithm = SearchMethods[config.algorithm]
    except:
        print("Invalid algorithm in the configuration file: ", config.algorithm)

    # Generate matrix
    matrix, boxes, targets, player = generateMatrixAndPositions(matrixFile)

    # Generate board and heuristic
    board = Board(matrix, boxes, targets, player)
    heuristic = Heuristic(config.heuristic)
    
    # Start timer
    start = time.time()

    # Show the board
    print("Initial Board")
    board.printBoard()

    # Run the selected algorithm
    if config.algorithm == SearchMethods.BFS:
        print("============================")
        print("\n[Starting BFS Algorithm]\n")
        print("============================\n")
        bfs.solve(board)    
        print("\n============================")
        print("\n[Finished BFS Algorithm]\n")
        print("============================")
    elif config.algorithm == SearchMethods.DFS:
        print("============================")
        print("\n[Starting DFS Algorithm]\n")
        print("============================\n")
        dfs.solve(board)
        print("\n============================")
        print("\n[Finished DFS Algorithm]\n")
        print("============================")
    elif config.algorithm == SearchMethods.IDDFS:
        print("============================")
        print("\n[Starting IDDFS Algorithm]\n")
        print("============================\n")
        iddfs.solve(board, config.maxDepth)
        print("\n============================")
        print("\n[Finished IDDFS Algorithm]\n")
        print("============================")
    elif config.algorithm == SearchMethods.GREEDY:
        print("============================")
        print("\n[Starting GREEDY Algorithm]\n")
        print("============================\n")
        greedy.solve(board, heuristic)
        print("\n============================")
        print("\n[Finished GREEDY Algorithm]\n")
        print("============================")
    elif config.algorithm == SearchMethods.A_STAR:
        print("============================")
        print("\n[Starting GREEDY Algorithm]\n")
        print("============================\n")

        # call
        
        print("\n============================")
        print("\n[Finished GREEDY Algorithm]\n")
        print("============================")
    elif config.algorithm == SearchMethods.IDA_STAR:
        print("============================")
        print("\n[Starting GREEDY Algorithm]\n")
        print("============================\n")

        # call
        
        print("\n============================")
        print("\n[Finished GREEDY Algorithm]\n")
        print("============================")

    end = time.time()
    print("\nResolution time: ", end - start)


generateAndRunGame(CONFIG_INPUT, BOARD_INPUT)