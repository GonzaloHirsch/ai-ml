# TP 2 - Algoritmos Genéticos

Implementacion de algoritmos genéticos para optimizar la configuración de un personaje.

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
```
{
    "clase": "guerrero",
    "data": "./datasets/allitems-small",
    "gen": {
        "cruce": "uniforme",
        "mutacion": "limitada",
        "seleccion": ["elite", "ruleta"],
        "reemplazo": ["universal", "ranking"],
        "implementacion": "parent",
        "corte": "cantidad"
    },
    "nums": {
        "A": 0.4,
        "B": 0.6,
        "N": 3,
        "K": 4
    }
}
```

Los posibles valores de cada campo son:
* `clase` --> 1 valor de [`guerrero`, `arquero`, `defensor`, `infiltrado`]
* `data` --> Path a la carpeta con el dataset (desde la carpeta `TP2`)
* `cruce` --> 1 valor de [`1 punto`, `2 puntos`, `anular`, `uniforme`]
* `mutacion` --> 1 valor de [`gen`, `limitada`, `uniforme`, `completa`]
* `seleccion` --> 2 valores de [`elite`, `ruleta`, `universal`, `boltzmann`, `torneo det`, `torneo prob`, `ranking`] (en formato array)
* `reemplazo` --> 2 valores de [`elite`, `ruleta`, `universal`, `boltzmann`, `torneo det`, `torneo prob`, `ranking`] (en formato array)
* `implementacion` --> 1 valor de [`all`,`parent`]
* `corte` --> 1 valor de [`tiempo`, `cantidad`, `aceptable`, `estructura`, `contenido`]
* `A` --> Número decimal entre 0 y 1
* `B` --> Número decimal entre 0 y 1
* `N` --> Número entero mayor a 0
* `K` --> Número entero mayor a 0

## Dataset

Los datos a utilizar deben estar todos en una misma carpeta, dentro de la carpeta `TP2`. Esta carpeta va a ser referenciada en el archivo de configuración. 

Los nombres de los archivos con los datos deben ser:
* `armas.tsv` --> Archivo de Armas
* `botas.tsv` --> Archivo de Botas
* `cascos.tsv` --> Archivo de Cascos
* `guantes.tsv` --> Archivo de Guantes
* `pecheras.tsv` --> Archivo de Pecheras

## Ejecución

Para ejecutar el programa hay que correr:
```
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
