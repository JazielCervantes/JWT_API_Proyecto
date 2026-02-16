# 🚀 API REST Profesional con JWT + Roles

## 📋 Descripción
API REST completa con autenticación JWT, sistema de roles, y todas las características de una aplicación profesional.

## ✨ Características

- ✅ **Autenticación JWT** con access y refresh tokens
- ✅ **Sistema de Roles** (Admin/User)
- ✅ **Hash de contraseñas** con bcrypt
- ✅ **Protección de endpoints** por roles
- ✅ **Paginación** de resultados
- ✅ **Filtros** avanzados
- ✅ **Manejo de errores** profesional
- ✅ **Documentación automática** con Swagger/OpenAPI
- ✅ **Base de datos MySQL**
- ✅ **Validación de datos** con Pydantic

## 🛠️ Tecnologías

### Backend
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para base de datos
- **Pydantic** - Validación de datos
- **PyJWT** - Manejo de tokens JWT
- **Passlib** - Hash de contraseñas
- **MySQL** - Base de datos relacional

### Frontend (Opcional)
- **Astro** - Framework web estático
- **Vue.js 3** - Framework progresivo

## 📁 Estructura del Proyecto

```
jwt-api-project/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # Punto de entrada de la aplicación
│   │   ├── config.py               # Configuración y variables de entorno
│   │   ├── database.py             # Configuración de la base de datos
│   │   │
│   │   ├── models/                 # Modelos de SQLAlchemy
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   └── product.py
│   │   │
│   │   ├── schemas/                # Schemas de Pydantic
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── auth.py
│   │   │   └── product.py
│   │   │
│   │   ├── routes/                 # Endpoints de la API
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   └── products.py
│   │   │
│   │   ├── services/               # Lógica de negocio
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   └── user_service.py
│   │   │
│   │   ├── utils/                  # Utilidades
│   │   │   ├── __init__.py
│   │   │   ├── security.py         # Hash, JWT, etc.
│   │   │   └── dependencies.py     # Dependencias de FastAPI
│   │   │
│   │   └── middleware/             # Middlewares personalizados
│   │       ├── __init__.py
│   │       └── error_handler.py
│   │
│   ├── requirements.txt            # Dependencias de Python
│   └── .env.example               # Variables de entorno de ejemplo
│
├── frontend/                       # (Opcional) Frontend con Astro + Vue
├── docs/                          # Documentación adicional
└── README.md                      # Este archivo
```

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd jwt-api-project
```

### 2. Configurar Backend

#### Crear entorno virtual
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### Instalar dependencias
```bash
pip install -r requirements.txt
```

#### Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

### 3. Configurar MySQL

#### Crear base de datos
```sql
CREATE DATABASE jwt_api_db;
```

#### Actualizar .env con credenciales
```
DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost:3306/jwt_api_db
```

### 4. Ejecutar migraciones (crear tablas)
```bash
python -m app.database
```

### 5. Iniciar el servidor
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en: `http://localhost:8000`

## 📚 Documentación de la API

Una vez el servidor esté corriendo, accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Autenticación

### Registro de usuario
```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "usuario@ejemplo.com",
  "username": "usuario",
  "password": "contraseña123",
  "full_name": "Nombre Completo"
}
```

### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "username": "usuario",
  "password": "contraseña123"
}

# Respuesta:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Usar el token
```bash
GET /api/users/me
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Refrescar token
```bash
POST /api/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## 👥 Roles

- **user**: Usuario normal (puede ver y editar su perfil)
- **admin**: Administrador (acceso total, puede gestionar usuarios)

## 📊 Endpoints Principales

### Autenticación
- `POST /api/auth/register` - Registrar nuevo usuario
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/refresh` - Refrescar token
- `POST /api/auth/logout` - Cerrar sesión

### Usuarios
- `GET /api/users/me` - Obtener perfil actual
- `PUT /api/users/me` - Actualizar perfil
- `GET /api/users` - Listar usuarios (Admin)
- `GET /api/users/{id}` - Obtener usuario por ID (Admin)
- `PUT /api/users/{id}` - Actualizar usuario (Admin)
- `DELETE /api/users/{id}` - Eliminar usuario (Admin)

### Productos (Ejemplo de CRUD)
- `GET /api/products` - Listar productos (con paginación y filtros)
- `POST /api/products` - Crear producto (Admin)
- `GET /api/products/{id}` - Obtener producto
- `PUT /api/products/{id}` - Actualizar producto (Admin)
- `DELETE /api/products/{id}` - Eliminar producto (Admin)

## 🔍 Paginación y Filtros

### Paginación
```bash
GET /api/products?skip=0&limit=10
```

### Filtros
```bash
GET /api/products?search=laptop&min_price=100&max_price=1000
```

### Ordenamiento
```bash
GET /api/products?sort_by=price&order=desc
```

## 🐛 Manejo de Errores

La API retorna respuestas consistentes:

```json
{
  "detail": "Descripción del error"
}
```

Códigos de estado HTTP:
- `200` - OK
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

## 🧪 Testing

```bash
pytest
```

## 📝 Notas para Desarrolladores Junior

### ¿Qué es JWT?
JWT (JSON Web Token) es un estándar para transmitir información de forma segura. Contiene:
- **Header**: Tipo de token y algoritmo
- **Payload**: Datos del usuario (id, rol, etc.)
- **Signature**: Firma para verificar autenticidad

### ¿Por qué dos tokens?
- **Access Token**: Vida corta (15-30 min), se usa en cada petición
- **Refresh Token**: Vida larga (7-30 días), se usa para obtener nuevos access tokens

### ¿Cómo funciona el hash de contraseñas?
Las contraseñas NUNCA se guardan en texto plano. Se usa bcrypt para crear un hash irreversible.

### Flujo de Autenticación
1. Usuario se registra → Contraseña hasheada → Guardado en BD
2. Usuario hace login → Se verifica hash → Se generan tokens
3. Usuario hace petición → Se verifica access token → Se permite acceso
4. Access token expira → Se usa refresh token → Se genera nuevo access token

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👨‍💻 Autor

Desarrollado para aprendizaje y uso profesional.

## 🔗 Enlaces Útiles

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [JWT.io](https://jwt.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
