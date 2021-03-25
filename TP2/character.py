import numpy as np
import math  

from constants import CharacterGenes


class Character:
    def __init__(self, height, arma, botas, casco, guantes, pechera):

        self.gene = [height, arma, botas, casco, guantes, pechera]
        
        self.qualities = {
            Qualities.FU.value: 0, 
            Qualities.AG.value: 0,
            Qualities.EX.value: 0,
            Qualities.RE.value: 0,
            Qualities.VI.value: 0,
        }

        self.calculateQualities()


    # -----------------------------------------------------------------
    # QUALITIES FUNCTIONS
    # -----------------------------------------------------------------

    def calculateQualities(self):
        for quality in Qualities:
            self.qualities[quality.value] = self._calculateQuality[quality.value]()


    def _getQualityMultiplier(self, quality):
        if Quality.FU == quality:
            return 100
        elif Quality.AG == quality:
            return 1
        elif Quality.EX == quality:
            return 0.6
        elif Quality.RE == quality:
            return 1
        elif Quality.VI == quality:
            return 100


    def _calculateQuality(self, quality):
        itemsValue = 0
        multiplier = self._getQualityMultiplier(quality)

        for idx in range(1, len(self.gene)):
            itemsValue += self.gene[idx][quality]

        return multiplier * math.tanh(0.01 * itemsValue)

    # -----------------------------------------------------------------
    # GENE FUNCTIONS
    # -----------------------------------------------------------------

    def setGene(geneItem, item):
        self.gene[geneItem.value] = item

    