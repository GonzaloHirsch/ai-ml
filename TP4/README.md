# TP 4 - Métodos de Aprendizaje NO Supervisado

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
        "input": "datasets/europe.csv",
        "test": "datasets/letters-test-big.txt",
        "flatten": 1
    },
    "method": {
        "network": "oja",
        "k": 10
    },
    "iterations": 15000,
    "learningRate": 0.005,
    "colormap": false
}
```

Los posibles valores de cada campo son:
* `iterations` --> Número entero mayor a 0, cantidad de iteraciones que se hacen
* `learningRate` --> Número decimal menor a 1, learning rate del programa (buen valor = `0.005`)
* `colormap` --> Determina si se realiza el mapa de colores y la matriz U para redes de Kohonen, `true` o `false`

Dentro del objeto `files` debe ir:
* `input` --> Path desde el root del proyecto al archivo con los datos de training
* `test` --> Path desde el root del proyecto al archivo con los de testing para redes de hopfield, deberían tener el mismo tamaño de flatten. Solo se usa cuando `network=hopfield`
* `flatten` --> Cada cuantas filas de input de entrenamiento se agrupa (para el de Hopfield debería ser `5`, para el resto `1`)

Dentro del objeto `method` debe ir:
* `network` --> Método que se usa, posibles valores son [`oja`, `kohonen`, `hopfield`]
* `k` --> Tamaño de la matriz de Kohonen (k x k). Solo se usa si `network=kohonen`.

**NOTA**: Se agregaron ejemplos de configuraciones en la carpeta `input`

## Datasets

Se recomienda agregar una carpeta `datasets` que ya está ignorada en el `.gitignore`. Ahí dentro se pueden poner los datos de entrada.

El ejercicio de PCA con el dataset de europa espera que el dataset se encuentre en la dirección `datasets/europe.csv`.

## Ejecución

Para ejecutar al programa, una vez lista la configuración, se puede correr así:
```python
python main.py
```

Para ejecutar al programa de PCA con los datos de Europa, una vez lista la configuración, se puede correr así:
```python
python europePca.py
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
