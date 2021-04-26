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
        "inputTest": "datasets/TP3-ej3-Conjuntoentrenamiento.txt",
        "desiredTest": "datasets/TP3-ej3-Salida-deseada.txt",
        "flatten": 7,
        "normalizeDesired": false
    },
    "kTraining": {
        "useKTraining": true,
        "blockAmount": 10,
        "testBlock": 9,
        "randomizeBlock": false
    },
    "iterations": 100,
    "activation": "simple",
    "learningRate": 0.02,
    "beta": 1,
    "deltaDesired": 0,
    "error": 0.005,
    "momentum": true,
    "alpha": 0.8,
    "calculateMetrics": false,
    "multilayer": false,
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
* `learningRate` --> Número decimal menor a 1, learning rate del programa (buen valor = `0.001`)
* `error` --> Número decimal menor a 1, cota de error (buen valor = `0.05`)
* `multilayer` --> Indica si el problema se resuelve con un perceptron simple o uno multicapa. Puede ser `true` o `false` (`true` para el EJ3 y `false` para el resto)
* `layers` --> Array de objetos JSON, configuración de las capas en caso de ser `multilayer: true`
* `beta` --> Beta a ser usado en la función `tanh` siendo `tanh(beta * x)`
* `deltaDesired` --> Delta para tener en cuenta cuando se hacen pruebas con la red, post entrenamiento
* `momentum` --> Activa el momentum, `true` o `false`
* `alpha` --> Alpha para el momentum, número entre 0 y 1
* `calculateMetrics` --> Booleano, indica si se calculan métricas como Precision, Recall y F1-Score.

Dentro del objeto `files` debe ir:
* `input` --> Path desde el root del proyecto al archivo con los datos de training
* `desired` --> Path desde el root del proyecto al archivo con los datos de los resultados esperados para training
* `inputTest` --> Path desde el root del proyecto al archivo con los datos de testing. Se ignora si `randomizeBlock` es `true`. 
* `desiredTest` --> Path desde el root del proyecto al archivo con los datos de los resultados esperados para testing. Se ignora si `randomizeBlock` es `true`. 
* `flatten` --> Cada cuantas filas de input de entrenamiento se agrupa (para el EJ3 debería ser `7`, para el resto `1`)
* `normalizeDesired` --> Flag para definir si se tienen que normalizar los datos de salida (para el EJ2 con el dataset en 3 dimensiones debería ser `true`, para el resto `false`)

Dentro del objeto `kTraining` debe ir:
* `useKTraining` --> Booleano, indica si se usa validación cruzada (`true` o `false`)
* `blockAmount` --> Número entero, cantidad de bloques que se usan
* `testBlock` --> Número entero entre `0` y `blockAmount - 1`, indica que bloque quiero usar del dataset para el testeo luego del entrenamiento. No tiene efecto si `randomizeBlock` es `true`.
* `randomizeBlock` --> Booleano, indica si se hacen `blockAmount` entrenamientos y pruebas con una randomización del dataset.

Dentro de cada objeto de `layers` (el orden de las capas es según se define en este arreglo):
* `activation` --> Función de activación para esa capa
    * `simple` --> Función Step
    * `linear` --> Función Lineal
    * `nonlinear` --> Función Sigmoidea (tanh)
* `perceptrons` --> Cantidad de perceptrones en esa capa

**NOTA**: Se agregaron ejemplos de configuraciones en la carpeta `input`

## Datasets

Se recomienda agregar una carpeta `datasets` que ya está ignorada en el `.gitignore`. Ahí dentro se pueden poner los datos de entrada. En [este link](https://drive.google.com/drive/folders/1N8HqoasPf_8VuInag2kxV2yUFMki2RB-?usp=sharing) pueden encontrar datasets para cada problema.

Es recomendable que los datos del ejercicio 1 se formatee de manera idéntica al resto de los datasets.

## Graficar
Para poder ver una animacion de los hiperplanos creados, ya sea de 2D o 3D, debe correr el siguiente comando:
```
python graphing.py -i <input> -w <archivo_de_weights> -e <archivo_de_errores>
```
* `input` --> Indica que datos de entrada debe tomar. Puede ser las siguientes opciones:
    * `xor1` --> Dataset del ej1 XOR. Se espera que los datos estén archivos:
        * Entrada --> `datasets/TP3-ej1-Conjuntoentrenamiento-xor.txt`
        * Salida Esperada --> `datasets/TP3-ej1-Salida-deseada-xor.txt`
    * `and1` --> Dataset del ej1 AND
        * Entrada --> `datasets/TP3-ej1-Conjuntoentrenamiento-and.txt`
        * Salida Esperada --> `datasets/TP3-ej1-Salida-deseada-and.txt`
    * `ej2` --> Dataset para el ej2
        * Entrada --> `datasets/TP3-ej2-Conjuntoentrenamiento.txt`
        * Salida Esperada --> `datasets/TP3-ej2-Salida-deseada.txt`
    * `ej3` --> Dataset para el ej3. Esto cortara el programa porque no se puede graficar.
* `archivo_de_weights` --> Nombre del archivo donde se imprimieron los pesos (dentro de la carpeta `output`)
* `archivo_de_errores` --> Nombre del archivo donde se imprimieron los errores (dentro de la carpeta `output`)

Para poder ver una comparación de accuracy en `train` y `test`:
```
python graphing.py -train <archivo_de_train> -test <archivo_de_test>
```
* `archivo_de_train` --> Nombre del archivo donde se imprimieron las accuracy de train (dentro de la carpeta `output`)
* `archivo_de_test` --> Nombre del archivo donde se imprimieron las accuracy de test (dentro de la carpeta `output`)

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
