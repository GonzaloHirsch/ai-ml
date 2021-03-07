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

`/input/configuration.json` contiene la configuración para el programa en sí, es decir, el algoritmo a utilizar. Tiene las opciones de `algorithm` y `maxDepth` en el caso de IDDFS. Las opciones de algoritmo son "BFS", "DFS", "IDDFS", "GREEDY".

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

Dentro de la carpeta `/examples` hay ejemplos de tableros

## Dependencias

Cada vez que se instala una librería nueva hacer:
```
pip freeze > requirements.txt
```

Para poder actualizar las dependencias.

