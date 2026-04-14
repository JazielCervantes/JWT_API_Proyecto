# 📘 Guía de Desarrollo - Conceptos y Arquitectura

---

## 🎯 Conceptos Fundamentales

### ¿Qué es una API REST?

**REST** (Representational State Transfer) es un estilo arquitectónico para crear APIs. Principios:

| Principio | Explicación |
|-----------|-------------|
| **Recursos** | TODO es un recurso: usuarios, productos, pedidos |
| **URL** | Cada recurso tiene una URL única |
| **Métodos HTTP** | GET (leer), POST (crear), PUT (actualizar), DELETE (eliminar) |
| **Sin estado** | El servidor no guarda estado del cliente entre peticiones |
| **JSON** | Formato de datos estándar para respuestas |

**Ejemplo:**
```bash
GET    /api/v1/users          # Listar usuarios
POST   /api/v1/users          # Crear usuario
GET    /api/v1/users/1        # Obtener usuario con ID 1
PUT    /api/v1/users/1        # Actualizar usuario con ID 1
DELETE /api/v1/users/1        # Eliminar usuario con ID 1
```

### ¿Qué es JWT?

**JWT** (JSON Web Token) es un token autodescriptivo que contiene toda la información del usuario.

**Estructura:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9 . eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIn0 . signature
└─ HEADER (algoritmo) ─┘                 └─ PAYLOAD (datos) ─┘                            └─ SIGNATURE ─┘
```

**¿Por qué JWT?**
- ✅ No necesita guardar sesiones en servidor
- ✅ El token contiene toda la información
- ✅ Es seguro (firma criptográfica verifica autenticidad)
- ✅ Puede expirar automáticamente
- ✅ Escalable para microservicios

### Access Token vs Refresh Token

**Access Token**
- Vida corta: **15 minutos**
- Usado en cada petición: `Authorization: Bearer {token}`
- Si se roba, expira en 15 min
- Se guarda en `sessionStorage` (vulnerable a XSS pero se borra al cerrar)

**Refresh Token**
- Vida larga: **7 días**
- Se usa solo para obtener nuevo access token
- Se guarda en BD (puede invalidarse)
- En **HTTP-Only cookie** (JavaScript NO puede acceder, protegido contra XSS)

**Flujo Completo:**
```
1. Login → Genera access_token (15 min) + refresh_token (7 días)
2. Petición → Envía Bearer {access_token}
3. Token expira (15 min después) → 401 Unauthorized
4. Usar refresh_token → Obtener nuevo access_token
5. Continuar con el nuevo token
7 días después → Redirect a login (refresh_token expiró)
```

### Hash de Contraseñas

**¿Por qué?**
- NUNCA guardar contraseñas en texto plano
- Si hackean la BD, no ven las contraseñas
- El hash es **irreversible**

**Cómo funciona con bcrypt:**

```python
# Registro
password = "MiContraseña123!"
hashed = bcrypt.hash(password)  # → "$2b$12$..." 

# BD guarda: "$2b$12$..." (NO la contraseña original)

# Login - Verificar
password_ingresada = "MiContraseña123!"
if bcrypt.verify(password_ingresada, hashed_guardado):
    print("✅ Contraseña correcta")
else:
    print("❌ Contraseña incorrecta")
```

**¿Por qué bcrypt?**
- ✅ Genera salt único por cada password
- ✅ Es lento (dificulta fuerza bruta)
- ✅ Es el estándar de la industria

---

## 🏗️ Arquitectura del Proyecto

### Layered Architecture (5 capas)

```
┌─────────────────────────────────────┐
│   🎨 Presentación (HTTP routes)     │  ← Endpoints /api/v1/*
├─────────────────────────────────────┤
│   🔀 Schemas (Pydantic validation)  │  ← Validación automática
├─────────────────────────────────────┤
│   ⚙️  Services (Business Logic)     │  ← AuthService, UserService
├─────────────────────────────────────┤
│   💾 Repositories (Data Access)     │  ← BaseRepository, UserRepository
├─────────────────────────────────────┤
│   🗄️  Database (SQLAlchemy Models) │  ← User, Product models
└─────────────────────────────────────┘
```

### Flujo de una Petición

```
1. Cliente envía POST /api/v1/auth/login
2. FastAPI valida JSON con Pydantic (LoginSchema)
3. Routing envía a route_auth.login()
4. AuthService.login() ejecuta lógica
5. AuthService usa UserRepository.get_by_username()
6. Repository consulta BD con SQLAlchemy
7. Se verifica hash de contraseña con bcrypt
8. Se generan JWT tokens
9. Se retorna respuesta JSON al cliente
```

### Carpetas y Responsabilidades

| Carpeta | Responsabilidad | Ejemplo |
|---------|-----------------|---------|
| `routes/` | Endpoints HTTP | `/auth/login`, `/users/me` |
| `schemas/` | Validación Pydantic | `LoginRequest`, `UserResponse` |
| `services/` | Lógica de negocio | `AuthService.login()` |
| `repositories/` | Acceso a datos | `UserRepository.get_by_email()` |
| `models/` | Definición de tablas | `User`, `Product` modelos SQLAlchemy |
| `utils/` | Funciones helper | JWT encoding, password hashing |
| `middleware/` | Interceptores HTTP | Logging, error handling, rate limiting |
| `core/` | Configuración global | Logger, exceptions, constants |

---

## 🔐 Flujo de Autenticación Completo

### 1. Registro

```bash
POST /api/v1/auth/register
{
  "email": "juan@ejemplo.com",
  "username": "juan",
  "password": "MiContraseña123!",
  "full_name": "Juan Pérez"
}
```

**¿Qué pasa internamente?**
1. Pydantic valida el request
2. Verificar que email NO exista (UserRepository.email_exists())
3. Verificar que username NO exista (UserRepository.username_exists())
4. **Hash** la contraseña con bcrypt
5. Crear usuario en BD con rol "user"
6. Retornar datos del usuario (SIN la contraseña)

**Respuesta:**
```json
{
  "id": 1,
  "email": "juan@ejemplo.com",
  "username": "juan",
  "full_name": "Juan Pérez",
  "role": "user",
  "created_at": "2026-04-14T10:30:00"
}
```

### 2. Login

```bash
POST /api/v1/auth/login
{
  "username": "juan",
  "password": "MiContraseña123!"
}
```

**¿Qué pasa internamente?**
1. Pydantic valida el request
2. Buscar usuario por username (UserRepository)
3. Si no existe → 404
4. **Verificar** que la contraseña sea correcta (bcrypt.verify)
5. Si es incorrecta → 401 Unauthorized
6. **Generar** access_token (15 min, HS256)
7. **Generar** refresh_token (7 días, HS256)
8. **Guardar** refresh_token en BD (para invalidación)
9. Retornar ambos tokens

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOi...",
  "refresh_token": "eyJhbGciOi...",
  "token_type": "bearer"
}
```

### 3. Usar el Access Token

```bash
GET /api/v1/users/me
Authorization: Bearer eyJhbGciOi...
```

**¿Qué pasa internamente?**
1. FastAPI extrae el token del header
2. **Decodificar** y validar JWT (secret_key)
3. Verificar que NO haya expirado
4. Extraer `user_id` del token
5. Buscar usuario en BD (UserRepository)
6. Inyectar usuario en la función (Depends)
7. Ejecutar endpoint con usuario autenticado

### 4. Refrescar Token

```bash
POST /api/v1/auth/refresh
{
  "refresh_token": "eyJhbGciOi..."
}
```

**¿Qué pasa internamente?**
1. **Decodificar** refresh_token
2. Verificar que coincida con el guardado en BD
3. Si no coincide → 401 (refresh_token fue revocado)
4. Si expiró → 401 (refresh_token tiempo de vida agotado)
5. **Generar** nuevo access_token (15 min)
6. Opcional: generar nuevo refresh_token (7 días)
7. Actualizar refresh_token en BD
8. Retornar token nuevo

### 5. Logout

```bash
POST /api/v1/auth/logout
Authorization: Bearer eyJhbGciOi...
```

**¿Qué pasa internamente?**
1. Verificar que el token sea válido
2. **Eliminar** refresh_token de BD
3. Retornar 200 OK
4. Después: Cliente elimina access_token de sessionStorage

---

## 👥 Sistema de Roles

### Roles Disponibles

**USER (usuario normal)**
- [ ] Ver productos
- [x] Ver su perfil
- [x] Actualizar su perfil
- [x] Cambiar su contraseña
- [ ] Listar usuarios (No)
- [ ] Crear/editar/eliminar productos (No)
- [ ] Cambiar roles (No)

**ADMIN (administrador)**
- [x] Todo lo que puede USER
- [x] Listar todos los usuarios
- [x] Ver detalles de cualquier usuario
- [x] Cambiar roles a otros usuarios
- [x] Crear/editar/eliminar productos
- [x] Cambiar roles

### Proteger Endpoints

**Ejemplo 1: Solo autenticados**
```python
@app.get("/api/v1/users/me")
def get_my_profile(current_user: User = Depends(get_current_user)):
    # Solo usuarios con token válido pueden acceder
    return current_user
```

**Ejemplo 2: Solo admins**
```python
@app.delete("/api/v1/users/{user_id}")
def delete_user(user_id: int, admin: User = Depends(require_admin)):
    # Solo admin puede acceder
    # require_admin verifica que role == "admin"
    pass
```

**Ejemplo 3: Público (sin auth)**
```python
@app.get("/api/v1/products")
def list_products():
    # SIN Depends, acceso público
    return products
```

---

## 🛠️ Patrones Implementados

### 1. Repository Pattern

**¿Qué es?** Abstracción para acceso a datos

**Ventajas:**
- ✅ Queries centralizadas
- ✅ Fácil para cambiar BD (SQLite → PostgreSQL)
- ✅ Testeable (se mockea el repository)

**Ejemplo:**
```python
# routes/users.py - No sabe cómo se obtiene el usuario
@app.get("/api/v1/users/{user_id}")
def get_user(user_id: int, repo: UserRepository = Depends()):
    user = repo.get_by_id(user_id)  # ← Repository abstrae la query
    return user

# services/ - Usa el repository
def find_user(user_id: int, repository: UserRepository):
    return repository.get_by_id(user_id)

# repositories/user_repository.py - Implementación real
class UserRepository(BaseRepository):
    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
```

### 2. Dependency Injection

**¿Qué es?** Inyectar dependencias en lugar de crearlas dentro

**Ventajas:**
- ✅ Loose coupling (acoplamiento bajo)
- ✅ Fácil para testear (inyectar mock)
- ✅ Código más limpio

**Ejemplo:**
```python
# Usar Depends() de FastAPI
@app.get("/api/v1/users/me")
def get_me(current_user: User = Depends(get_current_user)):
    # FastAPI automáticamente llama get_current_user()
    # e inyecta el resultado como current_user
    return current_user

# Definir la función que se inyecta
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Verificar token y retornar usuario
    return user_from_token
```

### 3. Exception Pattern

**¿Qué es?** Jerarquía de excepciones personalizadas

**Ventajas:**
- ✅ Errores específicos y descriptivos
- ✅ Fácil de manejar por tipo
- ✅ Códigos HTTP consistentes

**Ejemplo:**
```python
# core/exceptions.py
class UserNotFound(Exception):
    pass

class UserAlreadyExists(Exception):
    pass

# routes/users.py
def get_user(user_id: int, repo: UserRepository = Depends()):
    user = repo.get_by_id(user_id)
    if not user:
        raise UserNotFound(f"Usuario {user_id} no existe")
    return user

# middleware/error_handler.py
@app.exception_handler(UserNotFound)
def handle_user_not_found(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "USER_NOT_FOUND", "message": str(exc)}
    )
```

### 4. Logging Pattern

**¿Qué es?** Registrar eventos en formato JSON estructurado

**Ventajas:**
- ✅ Logs parseables automáticamente
- ✅ Fácil para análisis y debug
- ✅ Trazabilidad de peticiones

**Ejemplo:**
```python
# core/logger.py - JSON estructurado
logger.info(
    "User logged in",
    extra={
        "user_id": 1,
        "username": "juan",
        "ip_address": "192.168.1.1",
        "duration_ms": 245
    }
)

# Salida:
# {
#   "timestamp": "2026-04-14T10:30:00.123Z",
#   "level": "INFO",
#   "message": "User logged in",
#   "user_id": 1,
#   "username": "juan",
#   "ip_address": "192.168.1.1",
#   "duration_ms": 245
# }
```

---

## 📊 Paginación y Filtros

### ¿Por qué?

Si tienes 100,000 productos, NO quieres retornarlos todos en una petición:
- Lentitud (dura minutos descargarse)
- Alto consumo de memoria
- Mala experiencia del usuario

### Paginación

```bash
GET /api/v1/products?skip=0&limit=10
```

- **skip**: Cuántos registros saltar (offset)
- **limit**: Cuántos registros retornar (máximo: 100)

**Ejemplos:**
- Página 1: `/products?skip=0&limit=10` → registros 1-10
- Página 2: `/products?skip=10&limit=10` → registros 11-20
- Página 3: `/products?skip=20&limit=10` → registros 21-30

**Respuesta:**
```json
{
  "total": 5432,
  "skip": 0,
  "limit": 10,
  "products": [...]
}
```

### Filtros

```bash
GET /api/v1/products?search=laptop&min_price=500&max_price=2000&category=Electrónica
```

**Implementación:**
```python
@app.get("/api/v1/products")
def list_products(
    skip: int = 0,
    limit: int = 10,
    search: str = None,
    min_price: float = None,
    max_price: float = None,
    category: str = None,
    repo: ProductRepository = Depends()
):
    # Repository implementa filtrado
    return repo.list(
        skip=skip, 
        limit=limit, 
        search=search,
        min_price=min_price,
        max_price=max_price,
        category=category
    )
```

---

## 🔒 Seguridad en Profundidad

### Protecciones Implementadas

| Protección | Técnica | Ubicación |
|-----------|---------|-----------|
| **XSS** | sessionStorage + HTTP-Only cookie | frontend/lib/api.js |
| **CSRF** | SameSite=Strict en cookies | config.py |
| **Brute Force** | Rate limiting (slowapi) | middleware/security.py |
| **Weak Passwords** | Validación en Pydantic | schemas/auth.py |
| **SQL Injection** | SQLAlchemy ORM | repositories/ |
| **Weak JWT** | HS256 + SECRET_KEY único | utils/security.py |
| **Token Hijacking** | Refresh token en BD (revocable) | services/auth_service.py |

### Rate Limiting

```python
# middleware/security.py
limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/auth/login")
@limiter.limit("5/minute")  # Max 5 logins por minuto
def login(request: LoginRequest):
    pass
```

---

## 🚀 Despliegue a Producción

### Checklist de Seguridad

Antes de desplegar a producción:

- [ ] Cambiar `SECRET_KEY` por una cadena segura (32 caracteres)
- [ ] Cambiar `ADMIN_PASSWORD`
- [ ] Configurar `DEBUG=False`
- [ ] Usar HTTPS (obligatorio)
- [ ] Configurar `ALLOWED_ORIGINS` para tu dominio real
- [ ] Configurar rate limiting
- [ ] Setupear monitoreo de logs
- [ ] Activar backups automáticos de BD
- [ ] Usar variables de entorno seguras (no en código)

### Variables de Entorno para Producción

```env
DATABASE_URL=mysql+pymysql://user:PASS@host:3306/db_name
SECRET_KEY=GENERAR_CON: python -c "import secrets; print(secrets.token_hex(32))"
DEBUG=False
ALLOWED_ORIGINS=https://tu-frontend.vercel.app,https://tu-dominio.com
ADMIN_PASSWORD=PASSWORD_SUPER_SEGURO
HTTPS=True
```

---

**↓ Ver [docs/DEPLOYMENT.md](DEPLOYMENT.md) para deploy a Railway/Vercel**
