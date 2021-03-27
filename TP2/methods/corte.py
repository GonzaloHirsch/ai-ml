# Lib imports
from random import uniform
import time
# Local imports
from constants import ItemTypes, Corte
from config import Config

class Corte:
    variables = []

    def __init__(self, cte):
        self.cte = cte
        self.corte = self.cortes[cte]

    # -----------------------------------------------------------------
    # CORTE FUNCTIONS
    # -----------------------------------------------------------------

    def __corteTiempo(chs):
        # The first time it is called
        if len(Corte.variables) == 0:
            # Store start time
            Corte.variables.append(time.time())
            return False
        # Get time limit
        config = Config.getInstance()
        # Calculate elapsed time
        elapsed = time.time() - Corte.variables[0]
        return True if elapsed > config.crit1 else False

    def __corteCantidad(chs):
        return True

    def __corteAceptable(chs):
        return True

    def __corteEstructura(chs):
        return True

    def __corteContenido(chs):
        return True

    # -----------------------------------------------------------------
    # EXPOSED FUNCTIONS
    # -----------------------------------------------------------------

    # Exposed method to calculate
    # Input: parent 1 and parent 2
    def apply(self, chs):
        return self.corte(chs)

    # Map with pointers to the functions
    cortes = {
        Corte.TIEMPO.value: __corteTiempo,
        Corte.CANTIDAD.value: __corteCantidad,
        Corte.ACEPTABLE.value: __corteAceptable,
        Corte.ESTRUCTURA.value: __corteEstructura,
        Corte.CONTENIDO.value: __corteContenido
    }

