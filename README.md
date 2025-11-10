# ComunityTech - Red Social tipo Vlog

Backend desarrollado con Django REST Framework y PostgreSQL para una red social tipo vlog.

## Características

- ✅ Registro y autenticación de usuarios
- ✅ Solicitudes de amistad
- ✅ Seguir a otros usuarios
- ✅ Publicar posts (solo texto por ahora)
- ✅ Comentar publicaciones
- ✅ Dar like a posts y comentarios
- ✅ Compartir publicaciones
- ✅ Enviar mensajes privados
- ✅ Sistema de recomendaciones de posts

## Estructura del Proyecto

El proyecto está dividido en múltiples apps, cada una con una responsabilidad específica:

- **accounts**: Gestión de usuarios y autenticación
- **friends**: Solicitudes de amistad y relaciones de amistad
- **follows**: Sistema de seguir/seguidores
- **posts**: Publicaciones de usuarios
- **comments**: Comentarios en posts
- **likes**: Likes en posts y comentarios
- **shares**: Compartir publicaciones
- **messages**: Mensajería privada
- **recommendations**: Sistema de recomendaciones

## Requisitos

- Python 3.8+
- PostgreSQL 12+
- pip

## Instalación

1. Clonar el repositorio:
```bash
cd comunitytech
```

2. Crear un entorno virtual:
```bash
python -m venv venv
```

3. Activar el entorno virtual:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

5. Configurar variables de entorno:
Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=comunitytech_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

6. Crear la base de datos PostgreSQL:
```sql
CREATE DATABASE comunitytech_db;
```

7. Ejecutar migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

8. Crear un superusuario (opcional):
```bash
python manage.py createsuperuser
```

9. Ejecutar el servidor:
```bash
python manage.py runserver
```

## Endpoints de la API

### Autenticación (`/api/auth/`)
- `POST /api/auth/register/` - Registro de usuario
- `POST /api/auth/login/` - Iniciar sesión
- `GET /api/auth/profile/` - Ver perfil propio
- `PUT /api/auth/profile/` - Actualizar perfil
- `GET /api/auth/user/<id>/` - Ver perfil de otro usuario

### Amigos (`/api/friends/`)
- `GET /api/friends/requests/` - Listar solicitudes de amistad
- `POST /api/friends/requests/` - Enviar solicitud de amistad
- `POST /api/friends/requests/<id>/accept/` - Aceptar solicitud
- `POST /api/friends/requests/<id>/reject/` - Rechazar solicitud
- `POST /api/friends/requests/<id>/cancel/` - Cancelar solicitud
- `GET /api/friends/list/` - Listar amigos

### Seguir (`/api/follows/`)
- `GET /api/follows/` - Listar follows (usar `?type=followers` para seguidores)
- `POST /api/follows/` - Seguir a un usuario
- `POST /api/follows/unfollow/<user_id>/` - Dejar de seguir

### Posts (`/api/posts/`)
- `GET /api/posts/` - Listar posts (de usuarios seguidos/amigos)
- `POST /api/posts/` - Crear post
- `GET /api/posts/<id>/` - Ver post
- `PUT /api/posts/<id>/` - Actualizar post
- `DELETE /api/posts/<id>/` - Eliminar post
- `GET /api/posts/user/<user_id>/` - Posts de un usuario

### Comentarios (`/api/comments/`)
- `GET /api/comments/?post_id=<id>` - Listar comentarios de un post
- `POST /api/comments/` - Crear comentario
- `GET /api/comments/<id>/` - Ver comentario
- `PUT /api/comments/<id>/` - Actualizar comentario
- `DELETE /api/comments/<id>/` - Eliminar comentario
- `GET /api/comments/<id>/replies/` - Ver respuestas de un comentario

### Likes (`/api/likes/`)
- `POST /api/likes/post/<post_id>/` - Dar like a un post
- `DELETE /api/likes/post/<post_id>/` - Quitar like de un post
- `POST /api/likes/comment/<comment_id>/` - Dar like a un comentario
- `DELETE /api/likes/comment/<comment_id>/` - Quitar like de un comentario

### Compartir (`/api/shares/`)
- `GET /api/shares/` - Listar shares (usar `?post_id=<id>` para shares de un post)
- `POST /api/shares/` - Compartir un post
- `DELETE /api/shares/<id>/` - Eliminar share

### Mensajes (`/api/messages/`)
- `GET /api/messages/conversations/` - Listar conversaciones
- `POST /api/messages/conversations/` - Crear conversación
- `GET /api/messages/conversations/<id>/` - Ver conversación
- `GET /api/messages/conversations/<id>/messages/` - Listar mensajes
- `POST /api/messages/conversations/<id>/messages/` - Enviar mensaje
- `POST /api/messages/conversations/<id>/read/` - Marcar mensajes como leídos

### Recomendaciones (`/api/recommendations/`)
- `GET /api/recommendations/posts/` - Obtener posts recomendados

## Autenticación

La API utiliza autenticación por token. Después de registrarte o iniciar sesión, recibirás un token que debes incluir en el header de las peticiones:

```
Authorization: Token <tu-token>
```

## Notas

- Todos los endpoints requieren autenticación excepto `/api/auth/register/` y `/api/auth/login/`
- Los posts eliminados se marcan como `is_deleted=True` (soft delete)
- Los likes se pueden activar/desactivar sin eliminar el registro
- El sistema de recomendaciones se basa en popularidad de posts (likes y comentarios)

