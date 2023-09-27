# tarea1-sd
Tarea 1 de Sistemas Distribuidos EIT UDP CIT-2011


## Obtención
Para poder tener los contenedores hechos para esta actividad se tiene que hacer el siguiente comando:
```
git clone https://github.com/AkumuKernel/tarea1-sd.git
```

## Acceso a los contenedores
Para poder ejecutar los contenedores que fueron descargados gracias al paso anterior, se debe hacer lo siguiente en la carpeta raíz del proyecto:

```
cd cache_server
```
```
cd local
```
```
cd memcache
```

Cada cd es correspondiente a la carpeta que queramos movernos para iniciar el docker correspondiente, se puede hacer en 3 terminales diferentes y se puede ejecutar sin problemas.

## Ejecución de las instancias

Luego de acceder a la carpeta deseada se ejecuta el siguiente comando:

```
docker compose up -d
```

Para así poder iniciar los contenedores deseados, se pueden ejecutar los 3 compose al mismo tiempo.

## Acceso al contenedor 

Para acceder al contenedor para la búsqueda de los datos:

### Con cache_server
```
docker exec -it search bash
```

### Con local
```
docker exec -it search_json bash
```

### Con memcache
```
docker exec -it search_mem bash
```

## Ejecución del programa

Para poder hacer las búsquedas y hacer las comparaciones, se procede a ejecutar el siguiente comando, este sirve para cualquiera de las 3 instancias:

```
python search.pý
```

## Información adicional
Al momento de hacer las búsquedas aparecerá una interfaz que se muestra a continuación:

> Choose an operation:
> 1. Get
> 2. Simulate Searches
> 3. Generate Graph
> 4. Exit

En esta interfaz cuando se selecciona 1, se deberá insertar la llave a buscar, esta llave es un valor entero.

Cuando se selecciona 2, se deberá insertar un número entero mayor que cero, para así simular las búsquedas, lo recomendable es que sean más de 100.

Cuando se selecciona 3, existen 2 opciones, en el caso que no se haya simulado la búsqueda, te pedirá que la simules, con por lo menos 10 datos, caso contrario, te pasará una imagen con el gráfico comparando JSON y cache y la tabla respectiva.

Cuando se selecciona 4, termina el programa.

Cualquier otra selección imprimirá un error y te devolverá al menú.
