import numpy as np
import math  

from constants import CharacterGenes


class Character:
    def __init__(self, height, arma, botas, casco, guantes, pechera):

        self.gene = [height, arma, botas, casco, guantes, pechera]
        
        self.qualities = {
            Qualities.FUERZA.value: 0, 
            Qualities.AGILIDAD.value: 0,
            Qualities.PERICIA.value: 0,
            Qualities.RESISTENCIA.value: 0,
            Qualities.VIDA.value: 0,
        }


    # -----------------------------------------------------------------
    # QUALITIES FUNCTIONS
    # -----------------------------------------------------------------

    def calculateQualities(self):
        for quality in Qualities:
            self.qualities[quality.value] = self._calculateQuality[quality.value]()


    def _getQualityMultiplier(self, quality):
        if Quality.FUERZA == quality:
            return 100
        elif Quality.AGILIDAD == quality:
            return 1
        elif Quality.PERICIA == quality:
            return 0.6
        elif Quality.RESISTENCIA == quality:
            return 1
        elif Quality.VIDA == quality:
            return 100


    def _calculateQuality(self, quality):
        itemsValue = 0
        multiplier = self._getQualityMultiplier(quality)

        for idx in range(1, len(self.gene)):
            itemsValue += self.gene[idx][quality]

        return multiplier * math.tanh(0.01 * itemsValue)

    