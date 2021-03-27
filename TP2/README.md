# TP 2 - Algoritmos Genéticos

Implementacion de algoritmos genéticos para optimizar la configuración de un personaje.

## Tareas

Selección de padres y reemplazo de individuos
- [x] ~~Elite - G~~
- [x] ~~Ruleta - F~~
- [x] ~~Universal - F~~
- [ ] Boltzmann - J
- [ ] Torneos (ambas versiones) - J
- [x] ~~Ranking - G~~

Operadores genéticos
- [ ] Cruce de un punto - J
- [x] ~~Cruce de dos puntos - G~~
- [ ] Cruce anular - F
- [ ] Cruce uniforme - J

Mutación
- [x] ~~Gen - G~~
- [x] ~~Multigen Limitada - F~~
- [ ] Multigen Uniforme - J
- [x] ~~Completa - G~~

Implementación
- [ ] Fill-All - F
- [ ] Fill-Parent - J

Criterios de corte
- [x] ~~Tiempo - G~~
- [ ] Cantidad de generaciones - F
- [ ] Solución aceptable - J
- [ ] Estructura - G
- [ ] Contenido - F

General
- [x] ~~parseo + configuracion - G~~
- [x] ~~clase character - F~~

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
        "K": 4,
        "Pm": 0.05,
        "criterio1": 10,
        "criterio2": 10
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
* `Pm` --> Número decimal entre 0 y 1
* `criterio1` --> Número decimal/entero, sirve para los parámetros de corte, dependiendo del valor de `corte` representa
    * `corte = tiempo` --> Tiempo en segundos que se deja corriendo
    * `corte = cantidad` --> Cantidad de generaciones usadas
    * `corte = aceptable` --> Fitness mayor aceptable
    * `corte = estructura` --> Porcentaje (entre 0 y 1) de la población que se mantiene estable
    * `corte = contenido` --> Delta de cambio de fitness
* `criterio2` --> Número decimal/entero, sirve para los parámetros de corte, dependiendo del valor de `corte` representa
    * `corte = tiempo` --> No aplica, ignorar en este caso
    * `corte = cantidad` --> No aplica, ignorar en este caso
    * `corte = aceptable` --> No aplica, ignorar en este caso
    * `corte = estructura` --> Cantidad de generaciones contadas
    * `corte = contenido` --> Cantidad de generaciones contadas

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
