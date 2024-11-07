# Tarea 2 - CC5002 Desarrollo de Aplicaciones Web

- Nombre: Joel Riquelme
- Rut: 20.499.444-7
- Fecha de entgrega: 07 de Octubre de 2024

## Consideraciones generales

A priori se imprementaron todos los requerimientos solicitados en la tarea 3. Se corrigieron algnos errores de la tarea 2.

Para las validaciones se utilizó JavaScript tal como se pidió. Además se utilizó CSS para darle estilo a la página, siendo el archivo `style.css` el base para el diseño de la página, mientras que se utilizaron otros archivos CSS para darle estilo a los elementos y vistas de la página.

Las imagenes utilizadas en la página se guardan en la carpeta `uploads`.

En cuanto al archivo con las regiones y comunas, se utilizó el entregado en material docente.

## Como correr el proyecto

### Base de datos

La base de datos es la misma utilizada para la tarea 2 con todas las credecienciales y configuraciones necesarias.

### Requerimientos

Primero debe instalar los requerimientos del proyecto. Para ello, ejecute el siguiente comando en la terminal una vez este activo el entorno virtual:
``` 
$ python -r requirements.txt 

o 

$ py -r requirements.txt
```

### Iniciar el servidor

Para iniciar el servidor, ejecute el siguiente comando en la terminal:
```
# Pararse en la carpeta del proyecto
$ cd flask_app

# Correr el servidor
$ flask run
```

### Acceder a la página

Para acceder a la página, abra su navegador y vaya a la siguiente dirección:

http://localhost:5000/

si es que no se ha modificado el puerto en el archivo `flask_app/__init__.py`.



