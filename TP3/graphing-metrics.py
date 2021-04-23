import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse


def getColumnFromCSVFile(inputFile, column):
    df = pd.read_csv(inputFile, usecols=column )
    return df[column].values.tolist()


def graphAccuracies(trainAcc, testAcc):
    fig, ax = plt.subplots()

    x = np.arange(0, len(trainAcc), 1)
    
    ax.set_xlabel('x', color='#1C2833')
    ax.set_ylabel('y', color='#1C2833')
    ax.grid()

    ax.plot(x, trainAcc, '-r')

    plt.show()


def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Generating metrics graphs")

    # add arguments
    parser.add_argument('-train', dest='trainResultsFile', required=True)
    parser.add_argument('-test', dest='testResultsFile', required=True)

    args = parser.parse_args()

    print(args)   

    trainAcc = getColumnFromCSVFile(args.trainResultsFile, ["accuracy"])
    testAcc = getColumnFromCSVFile(args.testResultsFile, ["accuracy"])


    graphAccuracies(trainAcc, testAcc)

# call main
if __name__ == '__main__':
    main()