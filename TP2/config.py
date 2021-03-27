class Config:
    __instance = None

    # Asumes the class was instantiated once
    @staticmethod
    def getInstance():
        if Config.__instance == None:
            raise Exception("No config instance available")
        return Config.__instance

    def __init__(self, clase, data, cruce, mutacion, seleccion, reemplazo, implementacion, corte, a, b, n, k, pm):
        if Config.__instance != None:
            raise Exception("Cannot create another instance of config")

        self.clase = clase
        self.data = data    # Path to datasets
        self.cruce = cruce
        self.mutacion = mutacion
        self.seleccion = seleccion
        self.reemplazo = reemplazo
        self.implementacion = implementacion
        self.corte = corte
        self.a = a
        self.b = b
        self.n = n
        self.k = k
        self.pm = pm
        Config.__instance = self
    
    def __str__(self):
        return '%s{%s\n}' % (
            type(self).__name__,
            ', '.join('\n\t%s = %s' % item for item in vars(self).items())
        )
