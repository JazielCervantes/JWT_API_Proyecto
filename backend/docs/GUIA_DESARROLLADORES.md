# 📘 Guía de Uso para Desarrolladores

## 🎯 Conceptos Importantes

### 1. ¿Qué es una API REST?

REST (Representational State Transfer) es un estilo arquitectónico para crear APIs. Una API REST:
- Usa métodos HTTP (GET, POST, PUT, DELETE)
- Es stateless (sin estado entre peticiones)
- Retorna datos en formato JSON
- Usa URLs para identificar recursos

### 2. ¿Qué es JWT?

JWT (JSON Web Token) es un estándar para crear tokens de acceso. Un JWT contiene:

**Estructura:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6ImFkbWluIn0.signature
│            Header            │          Payload           │ Signature │
```

**¿Por qué usamos JWT?**
- No requiere guardar sesiones en el servidor
- El token contiene toda la información necesaria
- Es seguro (firmado criptográficamente)
- Puede expirar automáticamente

### 3. Access Token vs Refresh Token

**Access Token:**
- Vida corta (15-30 minutos)
- Se usa en cada petición
- Si se roba, expira pronto

**Refresh Token:**
- Vida larga (7-30 días)
- Solo se usa para obtener nuevos access tokens
- Se guarda en la base de datos (puede invalidarse)

**Flujo:**
```
1. Login → Access + Refresh token
2. Petición con Access token → OK
3. Access token expira
4. Uso Refresh token → Nuevo Access token
5. Continúo con nuevo Access token
```

### 4. Hash de Contraseñas

**¿Por qué hashear?**
- Nunca guardamos contraseñas en texto plano
- Si hackean la BD, no pueden ver las contraseñas
- El hash es irreversible

**Cómo funciona:**
```python
# Registro
password = "miContraseña123"
hashed = hash(password)  # → "$2b$12$..."
# Se guarda en BD: hashed

# Login
password_ingresada = "miContraseña123"
hashed_guardado = "$2b$12$..."
if verify(password_ingresada, hashed_guardado):
    print("Contraseña correcta")
```

Usamos **bcrypt** que:
- Genera un salt único por cada hash
- Es lento (dificulta ataques de fuerza bruta)
- Es un estándar de la industria

---

## 🔐 Flujo de Autenticación Completo

### Paso 1: Registro

```bash
POST http://localhost:8000/api/auth/register
Content-Type: application/json

{
  "email": "juan@ejemplo.com",
  "username": "juan",
  "password": "contraseña123",
  "full_name": "Juan Pérez"
}
```

**¿Qué pasa internamente?**
1. Se validan los datos con Pydantic
2. Se verifica que email y username no existan
3. Se hashea la contraseña con bcrypt
4. Se crea el usuario en la BD con rol "user"

### Paso 2: Login

```bash
POST http://localhost:8000/api/auth/login
Content-Type: application/json

{
  "username": "juan",
  "password": "contraseña123"
}
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

**¿Qué pasa internamente?**
1. Se busca el usuario por username o email
2. Se verifica el hash de la contraseña
3. Se generan ambos tokens (access y refresh)
4. Se guarda el refresh token en la BD
5. Se retornan ambos tokens

### Paso 3: Usar el Access Token

```bash
GET http://localhost:8000/api/users/me
Authorization: Bearer eyJhbGc...
```

**¿Qué pasa internamente?**
1. FastAPI extrae el token del header
2. Se decodifica y valida el JWT
3. Se verifica que no haya expirado
4. Se extrae el user_id del token
5. Se busca el usuario en la BD
6. Se ejecuta el endpoint con el usuario autenticado

### Paso 4: Refrescar Token (cuando expira)

```bash
POST http://localhost:8000/api/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGc..."
}
```

**¿Qué pasa internamente?**
1. Se decodifica el refresh token
2. Se verifica que coincida con el guardado en BD
3. Se generan nuevos tokens
4. Se actualiza el refresh token en BD

---

## 🛡️ Sistema de Roles

### Roles Disponibles

**USER (usuario normal):**
- Ver su propio perfil
- Actualizar su propio perfil
- Cambiar su contraseña
- Ver productos (sin crear/editar)

**ADMIN (administrador):**
- Todo lo que puede hacer un USER
- Ver todos los usuarios
- Crear/editar/eliminar usuarios
- Cambiar roles de usuarios
- Crear/editar/eliminar productos

### Proteger Endpoints

**Ejemplo 1: Solo usuarios autenticados**
```python
@app.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    # Solo usuarios con token válido pueden acceder
    return {"message": f"Hola {current_user.username}"}
```

**Ejemplo 2: Solo administradores**
```python
@app.delete("/users/{id}")
def delete_user(user_id: int, admin: User = Depends(require_admin)):
    # Solo usuarios con rol admin pueden acceder
    pass
```

**Ejemplo 3: Endpoint público**
```python
@app.get("/products")
def list_products(db: Session = Depends(get_db)):
    # No requiere autenticación
    return db.query(Product).all()
```

---

## 📊 Paginación y Filtros

### ¿Por qué paginar?

Si tienes 10,000 productos, no quieres retornar todos. La paginación:
- Mejora el rendimiento
- Reduce el uso de memoria
- Mejora la experiencia del usuario

### Parámetros de Paginación

```bash
GET /api/products?skip=0&limit=10
```

- **skip**: Cuántos registros saltar (offset)
- **limit**: Cuántos registros retornar (máximo)

**Ejemplos:**
- Página 1: `skip=0&limit=10` → registros 1-10
- Página 2: `skip=10&limit=10` → registros 11-20
- Página 3: `skip=20&limit=10` → registros 21-30

### Filtros Avanzados

```bash
# Búsqueda por texto
GET /api/products?search=laptop

# Múltiples filtros
GET /api/products?category=Electrónica&min_price=500&max_price=2000

# Con paginación
GET /api/products?search=laptop&skip=0&limit=20

# Ordenamiento
GET /api/products?sort_by=price&order=asc
```

**Implementación interna:**
```python
query = db.query(Product)

# Aplicar filtros
if search:
    query = query.filter(Product.name.like(f"%{search}%"))

if min_price:
    query = query.filter(Product.price >= min_price)

# Contar total (antes de paginar)
total = query.count()

# Paginar
products = query.offset(skip).limit(limit).all()
```

---

## ⚠️ Manejo de Errores

### Códigos HTTP Importantes

- **200 OK**: Todo bien
- **201 Created**: Recurso creado exitosamente
- **204 No Content**: Operación exitosa sin contenido
- **400 Bad Request**: Error en los datos enviados
- **401 Unauthorized**: No autenticado (falta token)
- **403 Forbidden**: No autorizado (sin permisos)
- **404 Not Found**: Recurso no encontrado
- **422 Unprocessable Entity**: Error de validación
- **500 Internal Server Error**: Error del servidor

### Lanzar Errores

```python
from fastapi import HTTPException, status

# Usuario no encontrado
if not user:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )

# Sin permisos
if current_user.role != UserRole.ADMIN:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Se requieren permisos de administrador"
    )
```

---

## 🧪 Probar la API

### Opción 1: Swagger UI (Recomendado)

1. Inicia el servidor: `uvicorn app.main:app --reload`
2. Abre: http://localhost:8000/docs
3. Puedes probar todos los endpoints directamente

**Para endpoints protegidos:**
1. Haz login en `/api/auth/login`
2. Copia el `access_token`
3. Click en "Authorize" (candado)
4. Pega: `Bearer <tu_token>`
5. Ahora puedes probar endpoints protegidos

### Opción 2: cURL

```bash
# Registro
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@test.com",
    "username": "test",
    "password": "test123",
    "full_name": "Test User"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test",
    "password": "test123"
  }'

# Usar token
curl -X GET http://localhost:8000/api/users/me \
  -H "Authorization: Bearer <tu_access_token>"
```

### Opción 3: Postman

1. Importa la colección desde Swagger
2. Crea una variable de entorno `{{access_token}}`
3. Configura el header: `Authorization: Bearer {{access_token}}`

---

## 🗄️ Base de Datos

### Estructura de Tablas

**users:**
- id (PK, auto-increment)
- email (unique)
- username (unique)
- hashed_password
- full_name
- role (enum: user/admin)
- is_active (boolean)
- created_at (timestamp)
- updated_at (timestamp)
- refresh_token (para invalidar sesiones)

**products:**
- id (PK, auto-increment)
- name
- description
- price
- stock
- category
- brand
- sku (unique)
- is_active (boolean)
- created_at (timestamp)
- updated_at (timestamp)

### Ver las Queries SQL

En `.env` configura:
```
DEBUG=True
```

Ahora verás en consola todas las queries que se ejecutan. Útil para debugging.

---

## 🚀 Despliegue a Producción

### Checklist de Seguridad

- [ ] Cambiar `SECRET_KEY` por una clave segura
- [ ] Cambiar credenciales de admin
- [ ] Configurar `DEBUG=False`
- [ ] Usar HTTPS
- [ ] Configurar CORS correctamente
- [ ] Usar variables de entorno seguras
- [ ] Configurar rate limiting
- [ ] Monitorear logs

### Variables de Entorno en Producción

```bash
# Generar SECRET_KEY segura
openssl rand -hex 32

# .env de producción
DATABASE_URL=mysql+pymysql://user:pass@host:3306/db
SECRET_KEY=<clave_super_segura>
DEBUG=False
ALLOWED_ORIGINS=https://tu-frontend.com
```

---

## 💡 Buenas Prácticas

1. **Nunca commits el .env**: Agrega `.env` al `.gitignore`
2. **Valida datos**: Usa Pydantic para validar todo
3. **Maneja errores**: Usa try-except y HTTPException
4. **Documenta**: Agrega docstrings a todas las funciones
5. **Separa lógica**: Usa services para lógica de negocio
6. **Testea**: Escribe tests para endpoints críticos
7. **Logs**: Usa logging para debugging en producción

---

## 🆘 Troubleshooting

### Error: "No module named 'app'"

**Solución:** Ejecuta desde el directorio `backend`:
```bash
cd backend
uvicorn app.main:app --reload
```

### Error: "Can't connect to MySQL server"

**Solución:**
1. Verifica que MySQL esté corriendo
2. Verifica credenciales en `.env`
3. Crea la base de datos: `CREATE DATABASE jwt_api_db;`

### Error: "Token expired"

**Solución:** Usa el refresh token para obtener uno nuevo:
```bash
POST /api/auth/refresh
{
  "refresh_token": "..."
}
```

### Error: "403 Forbidden"

**Solución:** Verifica que tu usuario tenga el rol necesario.

---

## 📚 Recursos Adicionales

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [JWT.io - Debugger](https://jwt.io/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/14/tutorial/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [HTTP Status Codes](https://httpstatuses.com/)
