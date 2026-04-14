# Ejemplos de uso de la API

Asume que el backend está corriendo en `http://localhost:8000` y que tienes las credenciales del admin por defecto.

---

## Swagger UI

La forma más directa de probar la API sin escribir código.

1. Abre http://localhost:8000/docs
2. Ve a `POST /api/v1/auth/login` → **Try it out**
3. Ingresa las credenciales:
   ```json
   { "username": "admin", "password": "admin123" }
   ```
4. Ejecuta y copia el `access_token` de la respuesta
5. Click en el botón **Authorize** (arriba a la derecha)
6. Pega `Bearer <tu_token>` en el campo
7. A partir de ahora puedes probar cualquier endpoint protegido

---

## cURL

### Login y guardar el token

```bash
# Linux/macOS: guarda el token en una variable
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

echo $TOKEN
```

```bash
# Windows PowerShell
$response = Invoke-RestMethod -Method POST -Uri "http://localhost:8000/api/v1/auth/login" `
  -ContentType "application/json" `
  -Body '{"username":"admin","password":"admin123"}'
$TOKEN = $response.access_token
```

### Registro de usuario

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nuevo@ejemplo.com",
    "username": "nuevousuario",
    "password": "Password123!",
    "full_name": "Nuevo Usuario"
  }'
```

### Obtener mi perfil

```bash
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

### Listar productos (no requiere auth)

```bash
# Lista básica
curl http://localhost:8000/api/v1/products

# Con paginación y filtros
curl "http://localhost:8000/api/v1/products?skip=0&limit=10&category=Electrónica&sort_by=price&order=asc"
```

### Crear un producto (solo admin)

```bash
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Laptop Pro",
    "description": "Laptop para desarrollo",
    "price": 1299.99,
    "stock": 15,
    "category": "Electrónica",
    "brand": "Dell"
  }'
```

### Actualizar un producto

```bash
curl -X PUT http://localhost:8000/api/v1/products/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"price": 1199.99, "stock": 20}'
```

### Eliminar un producto

```bash
curl -X DELETE http://localhost:8000/api/v1/products/1 \
  -H "Authorization: Bearer $TOKEN"
```

### Listar usuarios (solo admin)

```bash
curl http://localhost:8000/api/v1/users \
  -H "Authorization: Bearer $TOKEN"
```

### Cambiar rol de un usuario

```bash
curl -X PATCH http://localhost:8000/api/v1/users/2/role \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"role": "admin"}'
```

---

## Python (requests)

```python
import requests

BASE = "http://localhost:8000/api/v1"

# Login
resp = requests.post(f"{BASE}/auth/login", json={
    "username": "admin",
    "password": "admin123"
})
token = resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Obtener productos
products = requests.get(f"{BASE}/products", params={"limit": 5}).json()
for p in products["products"]:
    print(f"{p['name']} - ${p['price']}")

# Crear producto
new_product = requests.post(f"{BASE}/products", headers=headers, json={
    "name": "Teclado compacto",
    "description": "Teclado inalámbrico 75%",
    "price": 89.99,
    "stock": 30,
    "category": "Accesorios",
    "brand": "Keychron"
}).json()
print(f"Creado con ID: {new_product['id']}")
```

---

## JavaScript (fetch)

```javascript
const BASE = 'http://localhost:8000/api/v1';

// Login
const loginResp = await fetch(`${BASE}/auth/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  credentials: 'include',  // para que el refresh token llegue en cookie
  body: JSON.stringify({ username: 'admin', password: 'admin123' })
});
const { access_token } = await loginResp.json();

// Cualquier petición autenticada
const meResp = await fetch(`${BASE}/auth/me`, {
  headers: { 'Authorization': `Bearer ${access_token}` },
  credentials: 'include'
});
const me = await meResp.json();
console.log(me.full_name);

// Listar productos (sin auth)
const prodResp = await fetch(`${BASE}/products?limit=5`);
const { products, total } = await prodResp.json();
console.log(`${total} productos en total`);
```

---

## Endpoints disponibles

| Método | Ruta | Descripción | Auth |
|---|---|---|---|
| POST | `/api/v1/auth/register` | Registrar cuenta | No |
| POST | `/api/v1/auth/login` | Iniciar sesión | No |
| POST | `/api/v1/auth/refresh` | Renovar access token | Cookie |
| POST | `/api/v1/auth/logout` | Cerrar sesión | Sí |
| GET | `/api/v1/auth/me` | Datos del usuario actual | Sí |
| GET | `/api/v1/products` | Listar productos | No |
| GET | `/api/v1/products/{id}` | Obtener producto | No |
| POST | `/api/v1/products` | Crear producto | Admin |
| PUT | `/api/v1/products/{id}` | Actualizar producto | Admin |
| DELETE | `/api/v1/products/{id}` | Eliminar producto | Admin |
| GET | `/api/v1/users` | Listar usuarios | Admin |
| GET | `/api/v1/users/{id}` | Obtener usuario | Sí |
| PUT | `/api/v1/users/me` | Actualizar perfil | Sí |
| POST | `/api/v1/users/me/change-password` | Cambiar contraseña | Sí |
| PATCH | `/api/v1/users/{id}/role` | Cambiar rol | Admin |
| DELETE | `/api/v1/users/{id}` | Eliminar usuario | Admin |

Todos los detalles de parámetros y respuestas están documentados interactivamente en `/docs`.
