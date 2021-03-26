# Lib imports
import random

# How to access items data:
# Each dataset is translated into a Pandas DataFrame
# Having the DataFrame as df
# Rows can be selected using df.loc[ROW_NUMBER]
# Inside each row, id can be obtained by using df.loc[ROW_NUMBER].name
# Inside each row, values can be obtained by using df.loc[ROW_NUMBER][VALUE_INDEX]
# Values will be indexed like Fu(0) Ag(1) Ex(2) Re(3) Vi(4)
# Constants are in place to simplify and make indexing more readable
class Items:
    __instance = None

    @staticmethod
    def setInstance(data):
        if Items.__instance == None:
            Items(data)
    
    # Asumes the setInstance method was called
    @staticmethod
    def getInstance():
        if Items.__instance == None:
            raise Exception("No items instance available")
        return Items.__instance

    def __init__(self, data):
        if Items.__instance != None:
            raise Exception("Cannot create another instance of items")
        # Store all dataframes in a single arrray
        self.data = data
        # Precompute the amount of items in each class
        self.limits = []
        for d in data:
            self.limits.append(len(d))
        # Store instance
        Items.__instance = self

    # -----------------------------------------------------------------
    # RANDOM ITEM FUNCTIONS
    # -----------------------------------------------------------------

    # Picks a random item with a uniform distribution
    # Input: enum value from ItemTypes
    def getRandomItem(self, enumVal):
        idx = int(random.uniform(0, self.limits[enumVal.value]))
        return self.data[enumVal.value].loc[idx]

    # Picks a random height with a uniform distribution
    def getRandomHeight(self):
        return random.uniform(1.3, 2)
