from methods.mutacion import Mutacion

class GeneticAlgorithm:
    def __init__(self, config):
        self.config = config
        self.mutacion = Mutacion(config.mutacion)

    # -----------------------------------------------------------------
    # EXPOSED FUNCTIONS
    # -----------------------------------------------------------------

    def mutate(self, character):
        return self.mutacion.apply(character)