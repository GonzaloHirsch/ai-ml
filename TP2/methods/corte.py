# Lib imports
from random import uniform
import time
import heapq
from itertools import count
import numpy as np
# Local imports
from constants import Corte
from config import Config

class Corte:
    # Corte timepo variables
    startTime = None
    # Corte cantidad variables
    generations = None
    # Corte estructura variables
    generationsOverLimit = None

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
        config = Config.getInstance()

        # get the best fitness
        cnt = count(start=0, step=1)
        heap = [(ch.fitness * -1, next(cnt), ch) for ch in chs]
        heapq.heapify(heap)       

        bestFitness = heapq.heappop(heap)[0] * -1
        
        # return true if bestFitness reaches criteria.
        return bestFitness >= config.crit1

    def __corteEstructura(chs):
        # First time called, init variables
        if Corte.generationsOverLimit == None:
            Corte.generationsOverLimit = 0
            return False
        # Getting variables
        config = Config.getInstance()
        n = len(chs)
        # Compute hashes for each
        hashes = np.array([hash(ch) for ch in chs])
        # Count instances of each one
        unique, counts = np.unique(hashes, return_counts=True)
        # Calculate frequency
        counts = counts/n
        # Get maximum
        max = np.max(counts)
        # Check if the current percentage is bigger that the limit
        if max >= config.crit1:
            Corte.generationsOverLimit += 1
        else:
            Corte.generationsOverLimit = 0
        return Corte.generationsOverLimit >= config.crit2

    def __corteContenido(chs):
        config = Config.getInstance()

        delta = config.crit1
        generationCount = config.crit2

        # Sorting by best fitness
        cnt = count(start=0, step=1)
        heap = [(ch.fitness * -1, next(cnt), ch) for ch in chs]
        heapq.heapify(heap)       

        bestFitness = heapq.heappop(heap)[0] * -1

        if Corte.currentStat == None:
            Corte.currentStat = bestFitness
            Corte.generations = 0
        
        if (Corte.currentStat - bestFitness) <= delta and (Corte.currentStat - bestFitness) >= (-1*delta):
            Corte.generations += 1
        else:
            Corte.currentStat = bestFitness
            Corte.generations = 0

        return True if Corte.generations >= generationCount else False

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

