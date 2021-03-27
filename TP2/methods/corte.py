# Lib imports
from random import uniform
import time
# Local imports
from constants import ItemTypes, Corte
from config import Config

class Corte:
    # Corte timepo variables
    startTime = None
    # Corte cantidad variables
    generations = None
    # Corte estructura variables
    generationsOverLimit = None
    currentStat = None
    charactersDistribution = None

    def __init__(self, cte):
        self.cte = cte
        self.corte = self.cortes[cte]

    # -----------------------------------------------------------------
    # CORTE FUNCTIONS
    # -----------------------------------------------------------------

    def __corteTiempo(chs):
        # The first time it is called
        if Corte.startTime == None:
            # Store start time
            Corte.startTime = time.time()
            return False
        # Calculate elapsed time
        elapsed = time.time() - Corte.startTime
        return elapsed > Config.getInstance().crit1

    def __corteCantidad(chs):
        # The first time it is called
        if Corte.generations == None:
            # Store initial generations data
            Corte.generations = 0
            return False
        # Add 1 to the generation counter
        Corte.generations += 1
        return Corte.generations >= Config.getInstance().crit1

    def __corteAceptable(chs):
        return True

    def __corteEstructura(chs):
        # First time called, init variables
        if Corte.charactersDistribution == None:
            Corte.charactersDistribution = {}
            Corte.generationsOverLimit = 0
            Corte.currentStat = 0
            return False
        # Getting variables
        config = Config.getInstance()
        n = len(chs)
        # Store counts of characters per hash
        for ch in chs:
            # Check if the character is there or not, store count of characters
            if ch in Corte.charactersDistribution:
                Corte.charactersDistribution[ch] += 1
            else:
                Corte.charactersDistribution[ch] = 1
        # Compute distributions
        max = 0
        for dist in Corte.charactersDistribution.values():
            val = dist / n
            if val > max:
                max = val
        # Check if the current percentage is bigger that the limit
        if max >= config.crit1:
            Corte.generationsOverLimit += 1
        else:
            Corte.generationsOverLimit = 0
        Corte.currentStat = max
        return Corte.generationsOverLimit >= config.crit2

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

