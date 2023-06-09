# Sistema de autenticación de usuarios

Este es un sistema REST API que permitirá todo lo relacionado a la autenticación de usuarios (inicio de sesión, cierre de sesión, registro). Y a su vez manejara lo que es la autorización de usuarios mediante el uso de Json Web Tokens (JWT). Este proyecto fue realizado de tal forma que pueda ser escalable para agregar más funcionalidades.

Esta hecho con Python y FastAPI, a su vez tiene un sistema de migraciones hecho con Alembic

## Tecnologías utilizadas

- FastAPI
- Python 3.8
- Alembic (para las migraciones)
- MySQL

## Requisitos previos

Antes de comenzar, asegúrate de tener lo siguiente instalado en tu sistema:

- Python 3.8 o superior 
- Virtualenv o Pipenv (Para ejecutarlo en entonrnos virtuales)

Para instalar los demas paquetes utilizados en este proyecto usa este comando en la carpeta raíz:
```
pip install -r requeriments.txt
```


## Importante

Asegurate crear un archivo .env en la carpeta raiz del proyecto con la siguiente información:

```
DB_HOST='localhost' # host de la base de datos
DB_USER= # usuario de la BD
DB_PASS= # password del usuario
DB_DATABASE_NAME= # nombre de la base de datos
DB_DRIVER='mysql+pymysql' # nombre del driver
DB_PORT= # puerto de la base de datos
```
El nombre del driver (Si quieres puedes usar otro asegurate de colocar el nombre del driver correctamente tal y como lo menciona [SQLAlchemy](https://docs.sqlalchemy.org/en/20/core/engines.html))
