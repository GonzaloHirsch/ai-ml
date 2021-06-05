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
        "input": "datasets/TP3-ej2-Conjuntoentrenamiento.txt"
    },
    "iterations": 2000,
    "learningRate": 0.01,
    "beta": 1,
    "error": 0.001,
    "momentum": true,
    "calculateMetrics": false,
    "alpha": 0.8,
    "layers": [
        {
            "activation": "nonlinear",
            "perceptrons": 35
        },
        {
            "activation": "nonlinear",
            "perceptrons": 17
        },
        {
            "activation": "nonlinear",
            "perceptrons": 2
        },
        {
            "activation": "nonlinear",
            "perceptrons": 17
        },
        {
            "activation": "nonlinear",
            "perceptrons": 36
        }
    ]
}
```

Los posibles valores de cada campo son:
* `iterations` --> Número entero mayor a 0, cantidad de iteraciones que se hacen
* `learningRate` --> Número decimal menor a 1, learning rate del programa (buen valor = `0.001`)
* `error` --> Número decimal menor a 1, cota de error (buen valor = `0.05`)
* `layers` --> Array de objetos JSON, configuración de las capas en caso de ser `multilayer: true`
* `beta` --> Beta a ser usado en la función `tanh` siendo `tanh(beta * x)`
* `momentum` --> Activa el momentum, `true` o `false`
* `alpha` --> Alpha para el momentum, número entre 0 y 1

Dentro del objeto `files` debe ir:
* `input` --> Path desde el root del proyecto al archivo con los datos de training

Dentro de cada objeto de `layers` (el orden de las capas es según se define en este arreglo):
* `activation` --> Función de activación para esa capa
    * `simple` --> Función Step
    * `linear` --> Función Lineal
    * `nonlinear` --> Función Sigmoidea (tanh)
* `perceptrons` --> Cantidad de perceptrones en esa capa

**NOTA**: Se agregaron ejemplos de configuraciones en la carpeta `input`

## Datasets

Se recomienda agregar una carpeta `datasets` que ya está ignorada en el `.gitignore`. Ahí dentro se pueden poner los datos de entrada. En [este link](https://drive.google.com/drive/folders/1N8HqoasPf_8VuInag2kxV2yUFMki2RB-?usp=sharing) pueden encontrar datasets para cada problema.

Es recomendable que los datos del ejercicio 1 se formateen de manera idéntica al resto de los datasets.

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
