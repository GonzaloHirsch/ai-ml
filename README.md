# TP 1 - Sokoban

Implementacion del juego Sokoban con distintos metodos de busquedas informados y desinformados.

## Requerimientos

Para poder correr el programa es necesario **Python 3**

## Instalación

Pararse dentro del root del proyecto.

Para instalar, correr:
```
pip install -r requirements.txt
```

## Configuración

La configuración del programa se encuentra en 2 archivos, `/input/configuration.txt` y `/input/board.txt`.

`/input/configuration.txt` contiene la configuración para el programa en sí, es decir, el algoritmo a utilizar. El formato es el siguiente:
```
ALGORITMO(["BFS", "DFS", "IDDFS", "GREEDY"])
```

Por ejemplo, para configurar que use DFS el archivo se vería así:
```
DFS
```

`/input/board.txt` contiene el tablero que se va a resolver. Hay que copiar y pegar el tablero aquí. Todos los tableros deberían ser rectangulares (cuadrados o no). Los posibles símbolos son:
    + Espacio --> '.'
    + Pared --> 'X'
    + Caja --> 'B'
    + Jugador --> 'O'
    + Objetivo --> 'G'

## Ejecución

Para ejecutar el programa hay que correr:
```
python main.py
```

## Ejemplos

Dentro de la carpeta `/examples` hay ejemplos de tableros:

* `/examples/board_solvable_2.txt` --> https://sitati.dev/sokoban-builder/?g=%5B%5B%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%23%22%2C%22%23%22%2C%22%23%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%5D%2C%5B%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%23%22%2C%22a%22%2C%22%23%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%5D%2C%5B%22%20%22%2C%22%20%22%2C%22%23%22%2C%22%23%22%2C%22%23%22%2C%22%23%22%2C%22%23%22%2C%22a%22%2C%22%23%22%2C%22%23%22%2C%22%23%22%2C%22%23%22%2C%22%23%22%2C%22%20%22%2C%22%20%22%5D%2C%5B%22%20%22%2C%22%23%22%2C%22%23%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%23%22%2C%22%23%22%2C%22%20%22%5D%2C%5B%22%23%22%2C%22%23%22%2C%22%20%22%2C%22%20%22%2C%22%23%22%2C%22%20%22%2C%22%23%22%2C%22%20%22%2C%22%23%22%2C%22%20%22%2C%22%23%22%2C%22%20%22%2C%22%20%22%2C%22%23%22%2C%22%23%22%5D%2C%5B%22%23%22%2C%22%20%22%2C%22%20%22%2C%22%23%22%2C%22%23%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%23%22%2C%22%23%22%2C%22%20%22%2C%22%20%22%2C%22%23%22%5D%2C%5B%22%23%22%2C%22%20%22%2C%22%23%22%2C%22%23%22%2C%22%20%22%2C%22%20%22%2C%22%23%22%2C%22%20%22%2C%22%23%22%2C%22%20%22%2C%22%20%22%2C%22%23%22%2C%22%23%22%2C%22%20%22%2C%22%23%22%5D%2C%5B%22%23%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%221%22%2C%22%24%22%2C%221%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%23%22%5D%2C%5B%22%23%22%2C%22%23%22%2C%22%23%22%2C%22%23%22%2C%22%20%22%2C%22%20%22%2C%22%23%22%2C%22%23%22%2C%22%23%22%2C%22%20%22%2C%22%20%22%2C%22%23%22%2C%22%23%22%2C%22%23%22%2C%22%23%22%5D%2C%5B%22%20%22%2C%22%20%22%2C%22%20%22%2C%22%23%22%2C%22%23%22%2C%22%23%22%2C%22%23%22%2C%22%20%22%2C%22%23%22%2C%22%23%22%2C%22%23%22%2C%22%23%22%2C%22%20%22%2C%22%20%22%2C%22%20%22%5D%5D

## Dependencias

Cada vez que se instala una librería nueva hacer:
```
pip freeze > requirements.txt
```

Para poder actualizar las dependencias.

