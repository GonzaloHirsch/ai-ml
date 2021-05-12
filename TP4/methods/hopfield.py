# Lib imports
from numpy import array_equal, zeros, dot, array, sign, transpose
# Local imports

def printMatrix(input, flattenSize):
    cols = int(input.shape[0] / flattenSize)
    for i in range(flattenSize):
        for j in range(cols):
            print(input[cols*i + j], end="  " if input[cols*i + j] < 0 else "   ")
        print("")

def determineMatching(inputs, testInput):
    for index, input in enumerate(inputs):
        if array_equal(input, testInput):
            print("STABLE, PATTERN FOUND, MATCHES INPUT", index, end="\n\n")
            return
    print("STABLE, NO PATTERN FOUND, SPUREOUS\n\n")

def buildWeights (inputs):
    # Store number of inputs 
    n = inputs.shape[1]
    # Multiplier to avoid doing this multiple times
    mult = 1/n
    # Init matrix in 0s
    weights = zeros((n,n))
    # Iterating the matrix
    for row in range(n):
        for col in range(n):
            # If the row == col, leave it as 0
            # If row != col, multiply phi_row * phi_col of each pattern and sum those numbers
            # Equivalent to sum of mu from 1 to P (number of input patterns)
            # of phi_subrow_supramu * phi_subcol_supramu
            # See page 19 of PPT for better reference
            weights[row, col] = (dot(inputs[:,row],inputs[:,col])*mult) if not row == col else 0
    return weights

def apply(config, inputs, testInputs):
    
    # Build weights matrix
    weights = buildWeights(inputs)
    try:
        # Iterate and test each of the test inputs
        for testInput in testInputs:
            # Store number of steps used
            steps = 0
            print("NEW TEST CASE")
            # Keep the previous S and current S
            # Init prev S as empty to be able to enter the while loop
            prevS = array([])
            # Init current S as the test input given
            currS = testInput
            # Operate until it converges and is stable
            # Stability is defined by comparing the 2 arrays
            while not array_equal(prevS, currS):
                # Keep the current S as the previous one to be able to compute the new one
                prevS = currS
                # Printing
                print("Step", steps)
                printMatrix(prevS, config.flatten)
                # Calculate sign(weights * prevS) and cast it as int to avoid float and int comparisons
                # More info on page 21 of PPT
                currS = sign(dot(weights, transpose(prevS))).astype(int)
                # np.sign returns 0 when given a 0, but in this case we keep the old value if 0 is the sum
                # (currS == 0) returns a vector of True/False given the condition
                # ((currS == 0)*prevS) makes it so if the current value is 0, it is replaced by the old value
                currS = currS + ((currS == 0)*prevS)
                steps += 1
            # Determine which was the matching pattern
            determineMatching(inputs, currS)

    except KeyboardInterrupt:
        print("Finishing up...")