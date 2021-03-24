
# How to access items data:
# Each dataset is translated into a Pandas DataFrame
# Having the DataFrame as df
# Rows can be selected using df.loc[ROW_NUMBER]
# Inside each row, id can be obtained by using df.loc[ROW_NUMBER].name
# Inside each row, values can be obtained by using df.loc[ROW_NUMBER][VALUE_INDEX]
# Values will be indexed like Fu(0) Ag(1) Ex(2) Re(3) Vi(4)
# Constants are in place to simplify and make indexing more readable
class Items:
    def __init__(self, data):
        # Store all dataframes in a single arrray
        self.data = data
        # Precompute the amount of items in each class
        self.limits = []
        for d in data:
            self.limits.append(len(d))

    # Todo: Generar random
    def getRandomItem(enumVal):
        return self.data[enumVal.value][0]