import numpy as np
import enum


# class CharacterGenes(enum.Enum):
#     HEIGHT = 0
#     ARMA = 1
#     BOTAS = 2
#     CASCO = 3
#     GUANTES = 4
#     PECHERA = 5

#     def __eq__(self, value):
#         return self.value == value


class Qualities(enum.Enum):
    FUERZA = 1
    AGILIDAD = 2
    PERICIA = 3
    RESISTENCIA = 4
    VIDA = 5

    def __eq__(self, value):
        return self.value == value
