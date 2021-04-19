import enum

FILES = "files"
LAYERS = "layers"

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
   INPUT_TEST_DATA = "inputTest"
   DESIRED_TEST_DATA = "desiredTest"
   FLATTEN_DATA = "flatten"
   NORMALIZE_DESIRED_DATA = "normalizeDesired"
   ITERATIONS = "iterations"
   ACTIVATION = "activation"
   PERCEPTRONS = "perceptrons"
   LEARNING_RATE = "learningRate"
   MULTILAYER = "multilayer"
   ERROR_LIMIT = "error"
   BETA = "beta"
   DELTA_DESIRED = "deltaDesired"
   MOMENTUM = "momentum"
   ALPHA = "alpha"

   def __str__(self):
      return str(self.value)