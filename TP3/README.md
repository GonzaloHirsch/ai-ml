# TP 3 - Perceptron simple y multicapa

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
        "input": "datasets/TP3-ej3-Conjuntoentrenamiento.txt",
        "desired": "datasets/TP3-ej3-Salida-deseada.txt",
        "flatten": 7,
        "normalizeDesired": false
    },
    "iterations": 100,
    "activation": "simple",
    "learningRate": 0.02,
    "beta": 1,
    "deltaDesired": 0,
    "error": 0.005,
    "momentum": true,
    "alpha": 0.8,
    "multilayer": false,
    "blockAmount": 5,
    "testBlock": 1,
    "layers": [
        {
            "activation": "simple",
            "perceptrons": 10
        },
        {
            "activation": "simple",
            "perceptrons": 10
        }
    ]
}
```

Los posibles valores de cada campo son:
* `activation` --> Función de activación para el perceptrón simple
    * `simple` --> Función Step
    * `linear` --> Función Lineal
    * `nonlinear` --> Función Sigmoidea (tanh)
* `iterations` --> Número entero mayor a 0, cantidad de iteraciones que se hacen
* `learningRate` --> Número decimal menor a 1, learning rate del programa (buen valor = `0.02`)
* `error` --> Número decimal menor a 1, cota de error (buen valor = `0.05`)
* `multilayer` --> Indica si el problema se resuelve con un perceptron simple o uno multicapa. Puede ser `true` o `false` (`true` para el EJ3 y `false` para el resto)
* `layers` --> Array de objetos JSON, configuración de las capas en caso de ser `multilayer: true`
* `beta` --> Beta a ser usado en la función `tanh` siendo `tanh(beta * x)`
* `deltaDesired` --> Delta para tener en cuenta cuando se hacen pruebas con la red, post entrenamiento
* `momentum` --> Activa el momentum, `true` o `false`
* `alpha` --> Alpha para el momentum, número entre 0 y 1
* `blockAmount` --> Me indica en cuantos bloques quiero dividir el input
* `testBlock` --> Indica que bloque quiero usar del dataset para el testeo luego del entrenamiento.

Dentro del objeto `files` debe ir:
* `input` --> Path desde el root del proyecto al archivo con los datos de prueba
* `desired` --> Path desde el root del proyecto al archivo con los datos de los resultados esperados
* `flatten` --> Cada cuantas filas de input de entrenamiento se agrupa (para el EJ3 debería ser `7`, para el resto `1`)
* `normalizeDesired` --> Flag para definir si se tienen que normalizar los datos de salida (para el EJ2 con el dataset en 3 dimensiones debería ser `true`, para el resto `false`)

Dentro de cada objeto de `layers` (el orden de las capas es según se define en este arreglo):
* `activation` --> Función de activación para esa capa
    * `simple` --> Función Step
    * `linear` --> Función Lineal
    * `nonlinear` --> Función Sigmoidea (tanh)
* `perceptrons` --> Cantidad de perceptrones en esa capa

## Datasets

En la carpeta `datasets` se pueden encontrar archivos con datasets (todos tienen el formato de los datasets datos por la cátedra):
* Archivos para EJ1 - Item 1:
    * `TP3-ej1-Conjuntoentrenamiento-and.txt`
    * `TP3-ej1-Salida-deseada-and.txt`
* Archivos para EJ1 - Item 2:
    * `TP3-ej1-Conjuntoentrenamiento-xor.txt`
    * `TP3-ej1-Salida-deseada-xor.txt`
* Archivos para EJ2:
    * `TP3-ej2-Conjuntoentrenamiento.txt`
    * `TP3-ej2-Salida-deseada.txt`
* Archivos para EJ3:
    * `TP3-ej3-Conjuntoentrenamiento.txt`
    * `TP3-ej3-Salida-deseada.txt`

## Graficar
Para poder ver una animacion de los hiperplanos creados, ya sea de 2D o 3D, debe correr el siguiente comando:
```
python graphing.py -i <input> -w <archivo_de_weights> -e <archivo_de_errores>
```
* `input` --> Indica que datos de entrada debe tomar. Puede ser las siguientes opciones:
    * `xor1` --> Dataset del ej1 XOR
    * `and1` --> Dataset del ej1 AND
    * `ej2` --> Dataset para el ej2
    * `ej3` --> Dataset para el ej3. Esto cortara el programa porque no se puede graficar.
* `archivo_de_weights` --> Nombre del archivo donde se imprimieron los pesos (dentro de la carpeta `output`)
* `archivo_de_errores` --> Nombre del archivo donde se imprimieron los errores (dentro de la carpeta `output`)

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
