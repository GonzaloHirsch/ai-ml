import enum

FILES = "files"
LAYERS = "layers"

# Configurable options
class ActivationOptions(enum.Enum):
   SIMPLE = "simple"
   LINEAR = "linear"
   NON_LINEAR = "nonlinear"
   RELU = "relu"

   def __str__(self):
      return str(self.value)

# Configurable options
class ModeOptions(enum.Enum):
   NORMAL = "normal"
   DENOISER = "denoiser"
   VARIACIONAL = "variacional"
   OPTIMIZER = "optimizer"

   def __str__(self):
      return str(self.value)

# Configurable options
class ConfigOptions(enum.Enum):
   INPUT_DATA = "input"
   ITERATIONS = "iterations"
   LEARNING_RATE = "learningRate"
   ERROR_LIMIT = "error"
   BETA = "beta"
   MOMENTUM = "momentum"
   ALPHA = "alpha"
   CALCULATE_METRICS = "calculateMetrics"
   ACTIVATION = "activation"
   PERCEPTRONS = "perceptrons"
   PLOT_LATENT = "plotLatent"
   MODE = "mode"
   GENERATOR_POINTS = "generatorPoints"
   OPTIMIZER = "optimizer"

   def __str__(self):
      return str(self.value)