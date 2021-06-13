# TP 5 - Deep Learning

## Requerimientos

Para poder correr el programa es necesario **Python 3**

## Instalación

Pararse dentro del root del proyecto.

Para instalar, correr:
```
pip install -r requirements.txt
```

## Configuración

La configuración del programa se realiza desde el archivo `input/configuration.json`, el formato del archivo tiene que ser el siguiente:
```json
{
    "files": {
        "input": "datasets/font.txt"
    },
    "mode": "optimizer",
    "optimizer": "TNC",
    "noise": {
        "count": 5,
        "probability": 0.2
    },
    "iterations": 15000,
    "learningRate": 0.005,
    "beta": 1,
    "error": 0.001,
    "momentum": true,
    "calculateMetrics": false,
    "plotLatent": false,
    "alpha": 0.8,
    "generatorPoints": [[0.5, 0.6], [0.2, 0.75], [0.1, 0.9], [0.9, -0.5]],
    "layers": [
        {
            "activation": "nonlinear",
            "perceptrons": 35
        },
        {
            "activation": "nonlinear",
            "perceptrons": 25
        },
        {
            "activation": "nonlinear",
            "perceptrons": 2
        },
        {
            "activation": "nonlinear",
            "perceptrons": 25
        },
        {
            "activation": "nonlinear",
            "perceptrons": 35
        }
    ]
}
```

Los posibles valores de cada campo son:
* `mode` --> Modo que se usa de Autoencoder, los valores pueden ser:
    * `normal` --> Autoencoder normal
    * `denoiser` --> Autoencoder preparado para entrenar de modo denoiser
    * `generativo` --> Autoencoder preparado para entrenar y generar datos nuevos
    * `optimizer` --> Autoencoder para entrenar con un optimizador
* `optimizer` --> Optimizador usado solo con `mode: optimizer`, posibles valores son [`Nelder-Mead`, `Powell`, `CG`, `BFGS`, `L-BFGS-B`, `TNC`]
* `iterations` --> Número entero mayor a 0, cantidad de iteraciones que se hacen
* `learningRate` --> Número decimal menor a 1, learning rate del programa (buen valor = `0.001`)
* `error` --> Número decimal menor a 1, cota de error (buen valor = `0.05`)
* `layers` --> Array de objetos JSON, configuración de las capas en caso de ser `multilayer: true`
* `beta` --> Beta a ser usado en la función `tanh` siendo `tanh(beta * x)`
* `momentum` --> Activa el momentum, `true` o `false`
* `alpha` --> Alpha para el momentum, número entre 0 y 1
* `plotLatent` --> Booleano que define si se hace un gráfico del espacio latente. NO sirve con el `mode: optimizer`
* `generatorPoints`--> Array de arrays JSON, cada sub array tiene 2 elementos, un X e Y que se usan para generar muestras nuevas desde el espacio latente

Dentro del objeto `files` debe ir:
* `input` --> Path desde el root del proyecto al archivo con los datos de training

Dentro del objeto `noise` debe ir (sólo para `mode: denoiser`):
* `count` --> Cantidad de letras diferentes usadas para entrenar
* `probability` --> Probabilidad de ruido, decimal entre 0 y 1

Dentro de cada objeto de `layers` (el orden de las capas es según se define en este arreglo):
* `activation` --> Función de activación para esa capa
    * `simple` --> Función Step
    * `linear` --> Función Lineal
    * `nonlinear` --> Función Sigmoidea (tanh)
* `perceptrons` --> Cantidad de perceptrones en esa capa

## Datasets

Se recomienda agregar una carpeta `datasets` que ya está ignorada en el `.gitignore`. Ahí dentro se pueden poner los datos de entrada. Se incluye la versión del archivo `font.h` usada por el grupo, el `font.txt` en la carpeta `input`.

## Ejecución

Para ejecutar al programa, una vez lista la configuración, se puede correr así:
```python
python main.py
```

## Dependencias

Cada vez que se instala una librería nueva hacer:
```
pip freeze > requirements.txt
```

Para poder actualizar las dependencias.

## Presentación

La presentación se puede encontrar dentro de la carpeta `presentacion`.

## Autores

* Gonzalo Hirsch --> ghirsch@itba.edu.ar
* Florencia Petrikovich --> fpetrikovich@itba.edu.ar
* Juan Martin Oliva --> juoliva@itba.edu.ar
