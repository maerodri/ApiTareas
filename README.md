# Prueba Tecnica Crehana

Este proyecto es una API REST construida con **FastAPI**, que permite gestionar usuarios, listas de tareas y tareas individuales, incluyendo autenticación con **JWT**, encriptación de contraseñas y simulación de notificaciones por correo.

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
├── infrastructure/
│   ├── models.py           # Modelos SQLAlchemy
│   ├── database.py         # Conexión a MySQL
│   ├── repositories.py     # Lógica de acceso a datos
│   ├── routers/            # Endpoints organizados
│   │   ├── lists.py
│   │   ├── tasks.py
│   │   └── users.py
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
```

---

## ▶️ Ejecutar el proyecto

### Local:

```bash
uvicorn main:app --reload
```

### Docker:

```bash
docker compose up --build
```

---

## 📚 Notas

- Las contraseñas están encriptadas antes de guardarse
- El proyecto está organizado por capas: **Domain / Infrastructure**
- Puedes extender este sistema con permisos, testing, etc.

---

## 📬 Notificaciones simuladas

Cuando se crea una tarea con `assigned_user_id`, se imprime un mensaje simulado de notificación por consola.

---

## 📄 Licencia

Este proyecto es parte de una prueba técnica. Libre para uso académico y profesional.