# Ejemplos de uso de la API

Documentación práctica con ejemplos para consumir los endpoints directamente.

URL base en producción: `https://jwtapiproyecto-production.up.railway.app`  
URL base en desarrollo: `http://localhost:8000`

---

## Autenticación

Todos los endpoints protegidos requieren el header `Authorization: Bearer <token>`. El token se obtiene haciendo login.

### Registro

```bash
curl -X POST https://jwtapiproyecto-production.up.railway.app/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@ejemplo.com",
    "username": "miusuario",
    "password": "Segura123!",
    "full_name": "Mi Usuario"
  }'
```

Respuesta:
```json
{
  "id": 5,
  "email": "usuario@ejemplo.com",
  "username": "miusuario",
  "full_name": "Mi Usuario",
  "role": "user",
  "is_active": true
}
```

### Login

```bash
curl -X POST https://jwtapiproyecto-production.up.railway.app/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"username":"admin","password":"admin123"}'
```

`-c cookies.txt` guarda el refresh token (cookie `HttpOnly`) para usarlo después.

Respuesta:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGci...",
  "token_type": "bearer",
  "expires_in": 900
}
```

### Renovar el access token

```bash
# Usa la cookie guardada con -c/-b
curl -X POST https://jwtapiproyecto-production.up.railway.app/api/v1/auth/refresh \
  -b cookies.txt \
  -c cookies.txt
```

### Obtener mi perfil

```bash
curl https://jwtapiproyecto-production.up.railway.app/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

### Logout

```bash
curl -X POST https://jwtapiproyecto-production.up.railway.app/api/v1/auth/logout \
  -H "Authorization: Bearer $TOKEN" \
  -b cookies.txt
```

---

## Productos

### Listar productos

No requiere autenticación.

```bash
# Lista paginada básica
curl "https://jwtapiproyecto-production.up.railway.app/api/v1/products?skip=0&limit=10"

# Con filtros
curl "https://jwtapiproyecto-production.up.railway.app/api/v1/products?category=Electrónica&sort_by=price&order=asc"
```

Parámetros disponibles:

| Parámetro | Tipo | Descripción |
|---|---|---|
| `skip` | int | Registros a omitir (default 0) |
| `limit` | int | Máximo de resultados (default 10, max 100) |
| `category` | string | Filtrar por categoría |
| `brand` | string | Filtrar por marca |
| `min_price` | float | Precio mínimo |
| `max_price` | float | Precio máximo |
| `sort_by` | string | Campo para ordenar: `name`, `price`, `stock`, `created_at` |
| `order` | string | `asc` o `desc` |
| `search` | string | Búsqueda por nombre o descripción |

Respuesta:
```json
{
  "products": [
    {
      "id": 1,
      "name": "Laptop Pro",
      "description": "...",
      "price": 1299.99,
      "stock": 15,
      "category": "Electrónica",
      "brand": "Dell",
      "is_active": true,
      "created_at": "2025-01-01T00:00:00"
    }
  ],
  "total": 20,
  "skip": 0,
  "limit": 10
}
```

### Obtener un producto

```bash
curl https://jwtapiproyecto-production.up.railway.app/api/v1/products/1
```

### Crear producto (admin)

```bash
curl -X POST https://jwtapiproyecto-production.up.railway.app/api/v1/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Monitor 4K",
    "description": "Monitor UHD de 27 pulgadas",
    "price": 499.99,
    "stock": 8,
    "category": "Monitores",
    "brand": "LG"
  }'
```

### Actualizar producto (admin)

Solo se envían los campos que cambian:

```bash
curl -X PUT https://jwtapiproyecto-production.up.railway.app/api/v1/products/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"price": 449.99, "stock": 12}'
```

### Eliminar producto (admin)

```bash
curl -X DELETE https://jwtapiproyecto-production.up.railway.app/api/v1/products/1 \
  -H "Authorization: Bearer $TOKEN"
```

---

## Usuarios

### Listar usuarios (admin)

```bash
curl "https://jwtapiproyecto-production.up.railway.app/api/v1/users?skip=0&limit=20" \
  -H "Authorization: Bearer $TOKEN"
```

### Obtener un usuario

```bash
curl https://jwtapiproyecto-production.up.railway.app/api/v1/users/2 \
  -H "Authorization: Bearer $TOKEN"
```

### Actualizar mi perfil

```bash
curl -X PUT https://jwtapiproyecto-production.up.railway.app/api/v1/users/me \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"full_name": "Nombre actualizado"}'
```

### Cambiar contraseña

```bash
curl -X POST https://jwtapiproyecto-production.up.railway.app/api/v1/users/me/change-password \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"current_password": "actual", "new_password": "Nueva123!"}'
```

### Cambiar rol de usuario (admin)

```bash
curl -X PATCH https://jwtapiproyecto-production.up.railway.app/api/v1/users/3/role \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"role": "admin"}'
```

Roles disponibles: `user`, `admin`.

### Activar / desactivar usuario (admin)

```bash
curl -X PATCH https://jwtapiproyecto-production.up.railway.app/api/v1/users/3/status \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"is_active": false}'
```

---

## Python (requests)

```python
import requests

BASE = "https://jwtapiproyecto-production.up.railway.app/api/v1"

# Login (guarda cookies automáticamente con Session)
session = requests.Session()
resp = session.post(f"{BASE}/auth/login", json={
    "username": "admin",
    "password": "admin123"
})
token = resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Listar productos
products = session.get(f"{BASE}/products", params={"limit": 5}).json()
for p in products["products"]:
    print(f"{p['name']}: ${p['price']}")

# Crear un producto
nuevo = session.post(f"{BASE}/products", headers=headers, json={
    "name": "Webcam HD",
    "description": "1080p, autofocus",
    "price": 79.99,
    "stock": 25,
    "category": "Accesorios",
    "brand": "Logitech"
}).json()
print(f"Producto creado: ID {nuevo['id']}")

# Renovar token con la cookie de sesión
nuevo_token = session.post(f"{BASE}/auth/refresh").json()["access_token"]
```

---

## Exploración interactiva

La forma más cómoda de explorar todos los endpoints, parámetros y schemas es la interfaz Swagger:

- Producción: https://jwtapiproyecto-production.up.railway.app/docs
- Local: http://localhost:8000/docs

Y la versión ReDoc (solo lectura, mejor para leer documentación):

- Producción: https://jwtapiproyecto-production.up.railway.app/redoc
- Local: http://localhost:8000/redoc
