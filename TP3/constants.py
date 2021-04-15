import enum

FILES = "files"


# Configurable options
class ActivationOptions(enum.Enum):
   SIMPLE = "simple"
   LINEAR = "linear"
   NON_LINEAR = "nonlinear"

   def __str__(self):
      return str(self.value)

# Configurable options
class ConfigOptions(enum.Enum):
   INPUT_DATA = "input"
   DESIRED_DATA = "desired"
   ITERATIONS = "iterations"
   ACTIVATION = "activation"
   LEARNING_RATE = "learningRate"
   MULTILAYER = "multilayer"
   ERROR_LIMIT = "error"

   def __str__(self):
      return str(self.value)