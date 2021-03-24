# TP 2 - Algoritmos Genéticos

Implementacion del juego Sokoban con distintos metodos de busquedas informados y desinformados.

DataFrame.from_csv('c:/~/trainSetRel3.txt', sep='\t', header=0)

## Requerimientos

Para poder correr el programa es necesario **Python 3**

## Instalación

Pararse dentro del root del proyecto.

Para instalar, correr:
```
pip install -r requirements.txt
```

## Configuración

La configuración del programa se encuentra en 2 archivos, `/input/configuration.json` y `/input/board.txt`.

`/input/configuration.json` contiene la configuración para el programa en sí, es decir, el algoritmo a utilizar. Tiene las opciones de `algorithm`, `maxDepth` (en el caso de IDDFS) y `heuristic` (en el caso de GREEDY, A* e IDA*). 

Las opciones de algoritmo son `BFS`, `DFS`, `IDDFS`, `GREEDY`, `A*` e `IDA*`.

Las opciones de heurística son `1`, `2` y `3`:
* La heurística `1` es la suma de las mínimas distancias entre cajas y objetivos.
* La heurística `2` es la mínima distancia entre el Sokoban y una caja.
* La heurística `3` es la suma de las mínimas distancias asignando una caja a un objetivo + la mínima distancia entre el Sokoban y una caja.

Algunas configuraciones de ejemplo son:
```
{
    "algorithm": "IDDFS",
    "maxDepth": 10
}
{
    "algorithm": "DFS"
}
{
    "algorithm": "BFS"
}
{
    "algorithm": "A*",
    "heuristic": 1
}
```

`/input/board.txt` contiene el tablero que se va a resolver. Hay que copiar y pegar el tablero aquí. Todos los tableros deberían ser rectangulares (cuadrados o no). Los posibles símbolos son:
+ Espacio --> `.`
+ Pared --> `X`
+ Caja --> `B`
+ Jugador --> `O`
+ Objetivo --> `G`
+ Caja sobre Objetivo --> `V`
+ Jugador sobre Objetivo --> `M`

## Ejecución

Para ejecutar el programa hay que correr:
```
python main.py
```

## Ejemplos

Dentro de la carpeta `/examples` hay ejemplos de tableros. Los tableros son:
* Board 1 --> 16 Pasos
* Board 2 --> 78 Pasos --> http://www.game-sokoban.com/index.php?mode=level&lid=200
* Board 3 --> 83 Pasos --> http://www.game-sokoban.com/index.php?mode=level&lid=202
* Board 4 --> 44 Pasos --> http://www.game-sokoban.com/index.php?mode=level&lid=44957
* Board 5 --> 59 Pasos --> http://www.game-sokoban.com/index.php?mode=level&lid=19517
* Board 6 --> 52 Pasos --> http://www.game-sokoban.com/index.php?mode=level&lid=350
* Board Hard --> 102 Pasos --> http://www.game-sokoban.com/index.php?mode=level&lid=349

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
