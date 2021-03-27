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

    def __fillAll(population, children, selection1, selection2, b):
        return True

    def __fillParent(population, children, selection1, selection2, b):
        return True

    # -----------------------------------------------------------------
    # EXPOSED FUNCTIONS
    # -----------------------------------------------------------------

    # Exposed method to calculate
    # Input: entire population, children, selection method 1, selection method 2, b percentage
    # Output: next gen
    def apply(self, population, children, selection1, selection2, b):
        return self.implementacion(population, children, selection1, selection2, b)

    # Map with pointers to the functions
    implementaciones = {
        Implementacion.ALL.value: __fillAll,
        Implementacion.PARENT.value: __fillParent
    }

