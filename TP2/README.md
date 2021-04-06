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
```json
{
    "clase": "defensor",
    "data": "./datasets/allitems-big",
    "gen": {
        "cruce": "2 puntos",
        "mutacion": "completa",
        "seleccion": [
            {
                "name": "torneo prob",
                "params": {
                    "threshold": 0.75
                }
            },
            {
                "name": "boltzmann",
                "params": {
                    "t0": 100,
                    "tbase": 10,
                    "kdecay": 0.5
                }
            }
        ],
        "reemplazo": [
            {
                "name": "torneo det",
                "params": {
                    "M": 2
                }
            },
            {
                "name": "ranking",
                "params": {}
            }
        ],
        "implementacion": "all",
        "corte": "estructura"
    },
    "nums": {
        "A": 0.9,
        "B": 0.1,
        "N": 5000,
        "K": 3500,
        "Pm": 0.05,
        "Pcruce": 0.5,
        "criterio1": 0.9,
        "criterio2": 20
    },
    "plot": {
        "show": false,
        "sampling": 0.01
    }
}
```

Los posibles valores de cada campo son:
* `clase` --> 1 valor de [`guerrero`, `arquero`, `defensor`, `infiltrado`]
* `data` --> Path a la carpeta con el dataset (desde la carpeta `TP2`)

Dentro del objeto `gen` debe ir:
* `cruce` --> 1 valor de [`1 punto`, `2 puntos`, `anular`, `uniforme`]
* `mutacion` --> 1 valor de [`gen`, `limitada`, `uniforme`, `completa`]
* `seleccion` --> 2 objetos JSON del estilo mostrado:
    * `name` --> 1 valor de [`elite`, `ruleta`, `universal`, `boltzmann`, `torneo det`, `torneo prob`, `ranking`]
    * `params` --> Parámetros en formato JSON específicos a cada algoritmo (si no tiene parámetros dejar la propiedad `params` pero vacía(`{}`))
        * Para `boltzmann`:
            * `t0` --> Temperatura inicial
            * `tbase` --> Temperatura base 
            * `kdecay` --> Factor de decaiminiento
        * Para `torneo prob`:
            * `threshold` --> Threshold del algoritmo
        * Para `torneo det`:
            * `M` --> Numero entero mayor a 0, cantidad de individuos por ronda
    ```json
    {
        "name": ...,
        "params": {
            ...
        }
    }
    ```
* `reemplazo` --> Misma descripción que `seleccion`
* `implementacion` --> 1 valor de [`all`,`parent`]
* `corte` --> 1 valor de [`tiempo`, `cantidad`, `aceptable`, `estructura`, `contenido`]

Dentro del objeto `nums` debe ir:
* `A` --> Número decimal entre 0 y 1
* `B` --> Número decimal entre 0 y 1
* `N` --> Número entero mayor a 0, cantidad de personajes en población
* `K` --> Número entero mayor a 0, cantidad de padres a seleccionar
* `Pm` --> Número decimal entre 0 y 1, probabilidad de mutacion
* `Pcruce` --> Número decimal entre 0 y 1, probabilidad en cruce uniforme
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

Dentro del objeto `plot` debe ir:
* `show` --> Determina si se muestra el gráfico en tiempo real, `true` o `false`
* `sampling` --> Intervalo (en segundos) de tiempo en el que el gráfico toma datos, es decir, cada X segundos actualiza --> Recomendable `0.05` o `0.01`

## Dataset

Los datos a utilizar deben estar todos en una misma carpeta, dentro de la carpeta `TP2`. Esta carpeta va a ser referenciada en el archivo de configuración. 

Los nombres de los archivos con los datos deben ser:
* `armas.tsv` --> Archivo de Armas
* `botas.tsv` --> Archivo de Botas
* `cascos.tsv` --> Archivo de Cascos
* `guantes.tsv` --> Archivo de Guantes
* `pecheras.tsv` --> Archivo de Pecheras

## Gráficos

El programa grafica en tiempo real, pero también genera archivos CSV en una carpeta `output`, en donde genera los archivos con un timestamp.

**NOTA**: En algunas distribuciones de linux no funciona el gráfico por la falta de un packete de linux, se puede instalar con [esta guía](https://riptutorial.com/tkinter/example/3206/installation-or-setup) y debería funcionar

## Ejecución

Para ejecutar el programa hay que correr:
```
python main.py
```

El programa, si configurado para que muestre el gráfico, va a generar una ventana con el gráfico. Para **velocidad**, es recomendable correr sin el gráfico en tiempo real. Para los **datos**, es recomendable correr con el gráfico en tiempo real.

Para cortar la ejecución se puede hacer `ctrl + c` en cualquier momento desde la terminal.

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
