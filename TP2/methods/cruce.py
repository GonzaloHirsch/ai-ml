# Lib imports
from random import uniform
from math import ceil
# Local imports
from constants import ItemTypes, Cruce
from character import Character

class Cruce:
    def __init__(self, cru):
        self.cru = cru
        self.cruce = self.cruces[cru]

    def __crossGeneAtIdx(g1, g2, idx):
        g1[idx], g2[idx] = g2[idx], g1[idx]
        return g1, g2

    # -----------------------------------------------------------------
    # CRUCE FUNCTIONS
    # -----------------------------------------------------------------

    def __crucePunto1(p1, p2):
        # get crossing point
        point = int(uniform(0, len(p1.genes)))

        # Generate list of new genes for each one
        newGene1 = list.copy(p1.genes)
        newGene2 = list.copy(p2.genes)

        # gene crossing
        for i in range(point, p1.genes):
            Cruce.__crossGeneAtIdx(newGene1, newGene2, i)

        # Create new characters
        child1 = Character.fromList(p1.clase, newGene1)
        child2 = Character.fromList(p2.clase, newGene2)
        return child1, child2

    def __crucePunto2(p1, p2):
        # Calculate crossing points
        point1 = int(uniform(0, len(p1.genes)))
        point2 = int(uniform(0, len(p1.genes)))
        # Swap them to get always point1 <= point2
        if point1 > point2:
            point1, point2 = point2, point1

        # Generate list of new genes for each one
        newGene1 = list.copy(p1.genes)
        newGene2 = list.copy(p2.genes)

        # Make the gene crossing
        for i in range(point1, point2+1):
            Cruce.__crossGeneAtIdx(newGene1, newGene2, i)

        # Create new characters
        child1 = Character.fromList(p1.clase, newGene1)
        child2 = Character.fromList(p2.clase, newGene2)
        return child1, child2

    def __cruceAnular(p1, p2):
        # Variables
        P = int(uniform(0, len(p1.genes)))
        L = int(uniform(0, ceil(len(p1.genes)/2))+1)
        idx = P

        # Generate list of new genes for each one
        newGene1 = list.copy(p1.genes)
        newGene2 = list.copy(p2.genes)

        while L > 0:
            # Return to the beginning if the end was reached
            if idx == len(p1.genes):
                idx = 0
            Cruce.__crossGeneAtIdx(newGene1, newGene2, idx)
            L -= 1
            idx += 1
        
        # Create new characters
        child1 = Character.fromList(p1.clase, newGene1)
        child2 = Character.fromList(p2.clase, newGene2)
        return child1, child2

    def __cruceUniforme(p1, p2):
        # Generate list of new genes for each one
        newGene1 = list.copy(p1.genes)
        newGene2 = list.copy(p2.genes)

        # gene crossing
        for i in range(len(p1.genes)):
            r = random.uniform(0, 1)
            if r > 0.5:
                Cruce.__crossGeneAtIdx(newGene1, newGene2, i)
                
        # Create new characters
        child1 = Character.fromList(p1.clase, newGene1)
        child2 = Character.fromList(p2.clase, newGene2)
        return child1, child2

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
        Cruce.UNIFORME.value: __cruceUniforme,
    }
            