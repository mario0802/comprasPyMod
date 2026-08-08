# Solicitudes de Compras API

API REST para gestión de usuarios y solicitudes de compra, construida bajo un de **Clean Architecture** (separación en capas `domain`, `application`, `infrastructure` e `interfaces` por cada módulo de negocio).

## Stack técnico

| Herramienta | Versión / Detalle | Uso |
|---|---|---|
| **Python** | 3.12.10 | Lenguaje base del proyecto |
| **Flask** | - | Framework web |
| **Flask-Smorest** | - | Blueprints, validación de esquemas y documentación OpenAPI/Swagger automática |
| **SQLAlchemy** | - | ORM para acceso a datos |
| **Alembic** | - | Migraciones de base de datos |
| **PostgreSQL** | 17.10 | Base de datos relacional |
| **PyJWT** | - | Generación y validación de tokens JWT para autenticación |
| **Gunicorn** | - | Servidor WSGI para producción/contenedor |
| **Docker / Docker Compose** | - | Contenerización de la app y sus servicios |
| **pgAdmin** | - | Administración visual de PostgreSQL |
| **Postman** | - | Colección de pruebas de los endpoints |

## Arquitectura

El proyecto sigue un patrón donde cada dominio de negocio (`users`, `solicitudes_compra`, etc.) vive en `src/modules/` como un módulo independiente y autocontenido, dividido en:

- **domain**: entidades de negocio puras, interfaces de repositorios y excepciones propias del dominio.
- **application**: casos de uso (use cases) y DTOs — orquestan la lógica de negocio sin depender de frameworks.
- **infrastructure**: modelos SQLAlchemy, implementación concreta de repositorios y mappers.
- **interfaces**: blueprints de Flask, controladores y schemas de validación (entrada/salida HTTP).

Además existe una capa transversal (`src/shared/`) con logging, manejo de excepciones, autenticación (JWT), middlewares y utilidades de respuesta, reutilizable por todos los módulos.

## Estructura del proyecto

```
proyecto/
├── src/
│   ├── shared/            # Capa transversal (logging, auth, excepciones, middlewares)
│   ├── modules/            # Módulos de negocio (users, solicitudes_compra, ...)
│   ├── config/             # Settings y configuración de BD
│   └── app.py              # Application factory (create_app)
├── tests/                  # Pruebas unitarias e integración
├── migrations/              # Migraciones Alembic
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── requirements.txt
└── run.py                  # Punto de entrada
```

## Cómo levantar el proyecto

### Requisitos previos

- Docker y Docker Compose instalados.
- Puerto `5000` (API), `5432` (Postgres) y `8080` (pgAdmin) disponibles.

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd proyecto
```

### 2. Configurar variables de entorno

Copia el archivo de ejemplo y ajusta los valores si es necesario:

```bash
cp .env.example .env
```

Variables principales:

```dotenv
# App
APP_NAME=compras
ENV=development
DEBUG=true

# Logging
LOG_LEVEL=INFO
LOG_JSON=false

# Seguridad
SECRET_KEY=<tu-secret-key>
JWT_SECRET_KEY=<tu-jwt-secret-key>
JWT_ACCESS_TOKEN_EXPIRES_MIN=60

# Base de datos
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/compra_db

# Migracion
RUN_MIGRATIONS=true
```

> Dentro de Docker Compose, `DATABASE_URL` se sobrescribe automáticamente para apuntar al servicio `postgres` en lugar de `localhost`.

### 3. Construir y levantar los contenedores

```bash
docker compose up -d --build
```

Esto levanta 3 servicios:

| Servicio | Puerto | Descripción |
|---|---|---|
| `app` | 5000 | API Flask (Compras) |
| `postgres` | 5432 | Base de datos PostgreSQL |
| `pgadmin` | 8080 | Interfaz web para administrar Postgres |

### 4. Verificar que la API está corriendo

```bash
curl http://localhost:5000/health
```

### 5. Ver logs de la aplicación

```bash
docker compose logs -f app
```

### 6. Detener los servicios

```bash
docker compose down
```

## Documentación de la API (Swagger)

Gracias a Flask-Smorest, la documentación interactiva OpenAPI está disponible una vez levantado el proyecto en:

```
http://localhost:5000/docs/swagger
```

## Autenticación

La mayoría de los endpoints (excepto creación de usuario y login) requieren autenticación mediante **Bearer Token JWT**, obtenido a través del endpoint de login.

```
Authorization: Bearer <token>
```

## Endpoints (colección Postman)

| Método | Endpoint | Auth | Descripción | Body de ejemplo |
|---|---|---|---|---|
| `POST` | `/api/users` | No | Crear usuario | `{ "nombre", "apellido", "correo", "nick", "password" }` |
| `GET` | `/api/users/{id}` | Bearer | Obtener usuario por ID | - |
| `POST` | `/api/users/login` | No | Login y obtención de token JWT | `{ "correo", "password" }` |
| `POST` | `/api/solicitudes-compra` | Bearer | Crear solicitud de compra | `{ "solicitante_id", "descripcion", "monto" }` |
| `GET` | `/api/solicitudes-compra` | Bearer | Listar solicitudes de compra | - |
| `GET` | `/api/solicitudes-compra/{id}` | Bearer | Obtener solicitud de compra por ID | - |
| `PATCH` | `/api/solicitudes-compra/{id}` | Bearer | Actualizar estado de una solicitud (aprobar/rechazar) | `{ "estado", "aprobado_por" }` |

## Notas adicionales

- Los estados posibles de una solicitud de compra incluyen (entre otros) `PENDIENTE`, `APROBADA`, `RECHAZADA`.
- El campo `aprobado_por` corresponde al ID del usuario que aprueba/rechaza la solicitud.