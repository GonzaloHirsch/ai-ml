import enum

# Enum for item filename
class ItemFiles(enum.Enum):
   ARMAS = "armas.tsv"
   BOTAS = "botas.tsv"
   CASCOS = "cascos.tsv"
   GUANTES = "guantes.tsv"
   PECHERAS = "pecheras.tsv"

   def __str__(self):
      return str(self.value)

   def __eq__(self, value):
      return self.value == value

# Enum for item types with indexes
class ItemTypes(enum.Enum):
   ARMAS = 0
   BOTAS = 1
   CASCOS = 2
   GUANTES = 3
   PECHERAS = 4
   ALTURA = 5

   def __str__(self):
      return str(self.value)

   def __eq__(self, value):
      return self.value == value

# Enum for item properties with indexes
class Qualities(enum.Enum):
   FU = 0
   AG = 1
   EX = 2
   RE = 3
   VI = 4

   def __str__(self):
      return str(self.value)

   def __eq__(self, value):
      return self.value == value

# Configurable options
class ConfigOptions(enum.Enum):
   CLASE = "clase"
   DATA = "data"
   GEN = "gen"
   CRUCE = "cruce"
   MUTACION = "mutacion"
   SELECCION = "seleccion"
   REEMPLAZO = "reemplazo"
   IMPLEMENTACION = "implementacion"
   CORTE = "corte"
   NUMS = "nums"
   A = "A"
   B = "B"
   N = "N"
   K = "K"
   PM = "Pm"
   P_CRUCE = "Pcruce"
   CRITERIO_1 = "criterio1"
   CRITERIO_2 = "criterio2"
   PLOT = "plot"
   SHOW = "show"
   SAMPLING = "sampling"
   NAME = "name"
   PARAMS = "params"
   T0 = "t0"
   TBASE = "tbase"
   THRESHOLD = "threshold"
   K_DECAY = "kdecay"
   M_IND = "M"

   def __str__(self):
      return str(self.value)

# Posibles opciones de configuraciones
class Clase(enum.Enum):
   GUERRERO = "guerrero"
   ARQUERO = "arquero"
   DEFENSOR = "defensor"
   INFILTRADO = "infiltrado"

   def __str__(self):
      return str(self.value)

class Cruce(enum.Enum):
   PUNTO_1 = "1 punto"
   PUNTO_2 = "2 puntos"
   ANULAR = "anular"
   UNIFORME = "uniforme"

   def __str__(self):
      return str(self.value)

class Mutacion(enum.Enum):
   GEN = "gen"
   LIMITADA = "limitada"
   UNIFORME = "uniforme"
   COMPLETA = "completa"

   def __str__(self):
      return str(self.value)

class Seleccion(enum.Enum):
   ELITE = "elite"
   RULETA = "ruleta"
   UNIVERSAL = "universal"
   BOLTZMANN = "boltzmann"
   TORNEO_DET = "torneo det"
   TORNEO_PROB = "torneo prob"
   RANKING = "ranking"

   def __str__(self):
      return str(self.value)

class Implementacion(enum.Enum):
   ALL = "all"
   PARENT = "parent"

   def __str__(self):
      return str(self.value)

class Corte(enum.Enum):
   TIEMPO = "tiempo"
   CANTIDAD = "cantidad"
   ACEPTABLE = "aceptable"
   ESTRUCTURA = "estructura"
   CONTENIDO = "contenido"

   def __str__(self):
      return str(self.value)

# Precomputed data to accelerate lookups

MULTIPLIERS = {
   Qualities.FU.value: 100,
   Qualities.AG.value: 1,
   Qualities.EX.value: 0.6,
   Qualities.RE.value: 1,
   Qualities.VI.value: 100
}