import enum

FILES = "files"
METHOD = "method"

# Configurable options
class NetworkOptions(enum.Enum):
   OJA = "oja"
   KOHONEN = "kohonen"
   HOPFIELD = "hopfield"

   def __str__(self):
      return str(self.value)

# Configurable options
class ConfigOptions(enum.Enum):
   INPUT_DATA = "input"
   TEST_DATA = "test"
   FLATTEN_DATA = "flatten"
   COLORMAP = "colormap"
   ITERATIONS = "iterations"
   LEARNING_RATE = "learningRate"
   NETWORK_METHOD = "network"
   K_SIZE_METHOD = "k"

   def __str__(self):
      return str(self.value)