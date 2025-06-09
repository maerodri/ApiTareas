# Prueba Tecnica Crehana

Este proyecto es una API REST construida con **FastAPI**, que permite gestionar usuarios, listas de tareas y tareas individuales, incluyendo autenticación con **JWT**, encriptación de contraseñas y simulación de notificaciones por correo, el proyecto se entrega a traves de un repositorio publico denominado APITAREAS, este contiene los archivos necesarios para ejecutar la api y/o proyecto en una maquina con docker previamente instalado.

# Contenerizacion

El objetivo del docker es crear 2 contenedores dentro de la carpeta base, 1 encargado de la base de datos en este caso MySql y el otro la api desarrollada en fastApi, adjuntaremos evidencias de su ejecucion.

# Secuencia de la Api

La tarea inicial de la api apenas inicia su ejecucion, es crear las tablas de la base de datos, el usuario para la gestion de las mismas es configurado desde el dockerFile. Una vez ejecutada la aplicacion se podran acceder a los endPoints descritos en el Apartado de [Endpoint Principales.](#endpoints-principales)

---

##  Tecnologías utilizadas

- **FastAPI** 🐍
- **SQLAlchemy** (async)
- **MySQL**
- **Pydantic**
- **Uvicorn**
- **Python-Jose** (JWT)
- **Passlib + Bcrypt**
- **Docker + Docker Compose** (opcional)
- **Alembic** (opcional)

---

##  Estructura del proyecto

```
.
├── domain/                 # Esquemas Pydantic (DTOs)
│   └── schemas.py
├── application/            # Endpoints organizados
│     ├── lists.py
│     ├── tasks.py
│     └── users.py
├── infrastructure/
│   ├── models.py           # Modelos SQLAlchemy
│   ├── database.py         # Conexión a MySQL
│   ├── repositories.py     # Lógica de acceso a datos
│   ├── auth.py             # Generación y verificación de JWT
│   └── notifications.py    # Simulación de notificaciones
├── main.py                 # Punto de entrada FastAPI
└── requirements.txt
```

---

##  Autenticación

- Login con `POST /users/login`
- Genera un **token JWT** con expiración de 1 hora
- Contraseñas encriptadas con **bcrypt**

---

##  Endpoints principales

### ✅ Usuarios
- `GET /users/` — Listar usuarios
- `POST /users/` — Crear usuario
- `PUT /users/{id}` — Actualizar usuario
- `DELETE /users/{id}` — Eliminar usuario
- `POST /users/login` — Iniciar sesión (retorna JWT)

### ✅ Listas de tareas
- `GET /lists/`
- `POST /lists/`
- `PUT /lists/{id}`
- `DELETE /lists/{id}`

### ✅ Tareas
- `GET /tasks/` — Con filtros por estado y prioridad
- `POST /tasks/` — Simula notificación si se asigna a un usuario
- `PUT /tasks/{id}` / `PATCH /tasks/{id}/status`
- `DELETE /tasks/{id}`
- `GET /tasks/list/{list_id}` — Tareas de una lista + % completado

---

## 🔧 Variables de entorno (.env)

```
DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/todo_db 
SECRET_KEY = "secret-****"
```

---

## ▶️ Ejecutar el proyecto

### Local:

```bash
uvicorn main:app --reload
```
### Evidencia:
![Local](./img/local.png)

### Docker:

```bash
docker compose up --build
```

### Evidencia:
![Docker](./img/docker.png)

## ▶️ Ejecutar las pruebas

```bash
pytest
```

---

## 📚 Notas

- Las contraseñas están encriptadas antes de guardarse
- El proyecto está organizado por capas: **Domain / Infrastructure / Application**
- Puedes extender este sistema con permisos, testing, etc.
- Adjunto la collection de postam organizada y utilizada para la ejecucion de pruebas unitarias [Postman](./utilidades/CREHANA.postman_collection.json)

---

## 📬 Notificaciones simuladas

Cuando se crea una tarea con `assigned_user_id`, se imprime un mensaje simulado de notificación por consola.

---

## 📄 Licencia

Este proyecto es parte de una prueba técnica. Libre para uso académico y profesional.