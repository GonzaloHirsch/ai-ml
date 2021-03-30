# Local Imports
from constants import ConfigOptions

class Config:
    __instance = None

    # Asumes the class was instantiated once
    @staticmethod
    def getInstance():
        if Config.__instance == None:
            raise Exception("No config instance available")
        return Config.__instance

    def __init__(self, clase, data, cruce, mutacion, seleccion, reemplazo, implementacion, corte, a, b, n, k, pm, pcruce, crit1, crit2, show, sampling):
        if Config.__instance != None:
            raise Exception("Cannot create another instance of config")

        self.clase = clase
        self.data = data    # Path to datasets
        self.cruce = cruce
        self.mutacion = mutacion
        self.seleccion = [sel[ConfigOptions.NAME.value] for sel in seleccion]
        self.reemplazo = [remp[ConfigOptions.NAME.value] for remp in reemplazo]
        self.seleccionParams = [sel[ConfigOptions.PARAMS.value] for sel in seleccion]
        self.reemplazoParams = [remp[ConfigOptions.PARAMS.value] for remp in reemplazo]
        self.implementacion = implementacion
        self.corte = corte
        self.a = a
        self.b = b
        self.n = n
        self.k = k
        self.pm = pm
        self.pcruce = pcruce
        self.crit1 = crit1
        self.crit2 = crit2
        self.show = show
        self.sampling = sampling
        Config.__instance = self
    
    def __str__(self):
        return '%s{%s\n}' % (
            type(self).__name__,
            ', '.join('\n\t%s = %s' % item for item in vars(self).items())
        )
