# Lib imports
from random import uniform
# Local imports
from constants import ItemTypes, Cruce
from character import Character

class Cruce:
    def __init__(self, cru):
        self.cru = cru
        self.cruce = self.cruces[cru]

    # -----------------------------------------------------------------
    # CRUCE FUNCTIONS
    # -----------------------------------------------------------------

    def __crucePunto1(p1, p2):
        return p1, p2

    def __crucePunto2(p1, p2):
        # Calculate crossing points
        point1 = int(uniform(0, len(p1.gene)))
        point2 = int(uniform(0, len(p1.gene)))
        # Swap them to get always point1 <= point2
        if point1 > point2:
            point1, point2 = point2, point1
        # Generate list of new genes for each one
        new1Gene = []
        new2Gene = []
        # Make the gene crossing
        for i in range(len(p1.gene)):
            if i < point1 or i > point2:
                new1Gene.append(p1.gene[i])
                new2Gene.append(p2.gene[i])
            elif i <= point2:
                new1Gene.append(p2.gene[i])
                new2Gene.append(p1.gene[i])
        # Create new characters
        new1 = Character.fromList(p1.clase, new1Gene)
        new2 = Character.fromList(p2.clase, new2Gene)
        return new1, new2

    def __cruceAnular(p1, p2):
        return p1, p2

    def __cruceUniforme(p1, p2):
        return p1, p2

    # -----------------------------------------------------------------
    # EXPOSED FUNCTIONS
    # -----------------------------------------------------------------

    # Exposed method to calculate
    # Input: parent 1 and parent 2
    def apply(self, p1, p2):
        return self.cruce(p1, p2)

    # Map with pointers to the functions
    cruces = {
        Cruce.PUNTO_1.value: __crucePunto1,
        Cruce.PUNTO_2.value: __crucePunto2,
        Cruce.ANULAR.value: __cruceAnular,
        Cruce.UNIFORME.value: __cruceUniforme
    }
            