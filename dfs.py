from node import Node

def solveDFS(board):
    # Stack to store nodes to visit
    stack = []

    # Create the root
    root = Node(None, [], [])

    while not stack.empty():
        # Poping the first element
        curr = stack.pop()

        # Check if goal, if goal exit loop
        if board.isComplete(curr):
            break
        elif:
            # try to move the player to all 4 positions
            # if possible, create the node and push it to stack
            # each node will have a reference to the parent

            # Create new node with parent reference and new positions
            newNode = Node(curr, [], [])

            # Add the node to the stack
            stack.append(newNode)

    # Iterate from the goal up to the root in order to get the complete list of actions


