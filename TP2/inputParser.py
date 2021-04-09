# Lib imports

# Local imports


# Function to parse all the items in the files
def parseInput(filepath):
    with open(filepath) as f:
        # Read all lines
        lines = f.readlines()
        data = []

        for line in lines:
            line = line.strip().split()
            print(line)

parseInput()