# Lib imports
from math import ceil, floor
# Local imports
from constants import ItemTypes, Implementacion
from config import Config

class Implementacion:
    def __init__(self, impl):
        self.impl = impl
        self.implementacion = self.implementaciones[impl]       

    # -----------------------------------------------------------------
    # IMPLEMENTACION FUNCTIONS
    # -----------------------------------------------------------------

    def __fillAll(population, children, selection1, selection2, b, gen):
        n = len(population)
        # Population is previous population + the K children that were created
        characters = population + children
        # A percentage of the new population will be chosen with one method and the rest with another
        n1 = ceil(n * b)
        n2 = floor(n * (1 - b))
        list1 = selection1.apply(characters, n1, gen)
        list2 = selection2.apply(characters, n2, gen)
        # Resulting new generation is the sum of both populations retrieved
        return list1 + list2

    def __fillParent(population, children, selection1, selection2, b, gen):
        return True

    # -----------------------------------------------------------------
    # EXPOSED FUNCTIONS
    # -----------------------------------------------------------------

    # Exposed method to calculate
    # Input: entire population, children, selection method 1, selection method 2, b percentage
    # n --> len(population)
    # k --> len(children)
    # Output: next gen
    def apply(self, population, children, selection1, selection2, b, gen):
        return self.implementacion(population, children, selection1, selection2, b, gen)

    # Map with pointers to the functions
    implementaciones = {
        Implementacion.ALL.value: __fillAll,
        Implementacion.PARENT.value: __fillParent
    }

