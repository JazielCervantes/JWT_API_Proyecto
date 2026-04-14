# 💻 Ejemplos de Uso - Ready-to-Copy Code

---

## 🎯 Antes de Comenzar

Asume que:
- ✅ Backend corriendo en http://localhost:8000
- ✅ Admin user: `admin` / `admin123`

---

## 1. Swagger UI (Recomendado)

**La forma FÁCIL de probar la API.**

### Pasos

1. Abre: http://localhost:8000/docs
2. Ve a `/api/v1/auth/login`
3. Click en **"Try it out"**
4. Ingresa: `{"username":"admin","password":"admin123"}`
5. Click **"Execute"**
6. Copia el `access_token`
7. Click en **"Authorize"** 🔒 (arriba a la derecha)
8. Pega: `Bearer {tu_access_token}`
9. ¡Listo! Ahora puedes probar endpoints protegidos

---

## 2. cURL (Terminal)

Ideal para scripts y automatización.

### Registro de Usuario

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@ejemplo.com",
    "username": "testuser",
    "password": "TestPass123!",
    "full_name": "Usuario de Prueba"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1Ni...",
  "refresh_token": "eyJhbGciOiJIUzI1Ni...",
  "token_type": "bearer"
}
```

**Guardar el token:**
```bash
# En Linux/macOS:
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

echo $TOKEN
```

### Obtener Mi Perfil

```bash
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1Ni..."
```

### Listar Productos

```bash
# Sin filtros
curl -X GET http://localhost:8000/api/v1/products

# Con paginación
curl -X GET "http://localhost:8000/api/v1/products?skip=0&limit=10"

# Con filtros
curl -X GET "http://localhost:8000/api/v1/products?search=laptop&min_price=500&max_price=2000"
```

### Crear Producto (ADMIN)

```bash
curl -X POST http://localhost:8000/api/v1/products \
  -H "Authorization: Bearer {token_admin}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop HP Pavilion",
    "description": "Laptop de 15 pulgadas",
    "price": 799.99,
    "stock": 15,
    "category": "Electrónica",
    "brand": "HP",
    "sku": "HP-PAV-001"
  }'
```

### Refrescar Token

```bash
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"eyJhbGciOiJIUzI1Ni..."}'
```

### Logout

```bash
curl -X POST http://localhost:8000/api/v1/auth/logout \
  -H "Authorization: Bearer {token}"
```

---

## 3. Python + Requests

Perfecto para integración con scripts o Django.

### Instalación

```bash
pip install requests
```

### Script Completo

```python
import requests
import json

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.access_token = None
        self.refresh_token = None
    
    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}" if self.access_token else ""
        }
    
    def register(self, email, username, password, full_name):
        """Registrar nuevo usuario"""
        url = f"{self.base_url}/api/v1/auth/register"
        data = {
            "email": email,
            "username": username,
            "password": password,
            "full_name": full_name
        }
        response = requests.post(url, json=data)
        return response.json()
    
    def login(self, username, password):
        """Iniciar sesión"""
        url = f"{self.base_url}/api/v1/auth/login"
        data = {"username": username, "password": password}
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data["access_token"]
            self.refresh_token = data["refresh_token"]
            return data
        raise Exception(f"Login failed: {response.json()}")
    
    def get_my_profile(self):
        """Obtener mi perfil"""
        url = f"{self.base_url}/api/v1/users/me"
        response = requests.get(url, headers=self.get_headers())
        return response.json()
    
    def list_products(self, skip=0, limit=10, search=None):
        """Listar productos"""
        url = f"{self.base_url}/api/v1/products"
        params = {"skip": skip, "limit": limit}
        if search:
            params["search"] = search
        response = requests.get(url, params=params)
        return response.json()
    
    def create_product(self, product_data):
        """Crear producto (admin)"""
        url = f"{self.base_url}/api/v1/products"
        response = requests.post(url, json=product_data, headers=self.get_headers())
        return response.json()
    
    def refresh_access_token(self):
        """Refrescar token"""
        url = f"{self.base_url}/api/v1/auth/refresh"
        data = {"refresh_token": self.refresh_token}
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data["access_token"]
            return data
        raise Exception("Token refresh failed")
    
    def logout(self):
        """Cerrar sesión"""
        url = f"{self.base_url}/api/v1/auth/logout"
        response = requests.post(url, headers=self.get_headers())
        return response.status_code == 200


# ========== USO ==========

if __name__ == "__main__":
    client = APIClient("http://localhost:8000")
    
    # 1. Registrarse
    print("1. Registrando usuario...")
    user = client.register(
        email="juan@ejemplo.com",
        username="juan",
        password="JuanPass123!",
        full_name="Juan García"
    )
    print(f"✅ {user['username']} registrado")
    
    # 2. Login
    print("\n2. Iniciando sesión...")
    tokens = client.login("juan", "JuanPass123!")
    print(f"✅ Token: {tokens['access_token'][:50]}...")
    
    # 3. Obtener perfil
    print("\n3. Obteniendo perfil...")
    profile = client.get_my_profile()
    print(f"✅ Usuario: {profile['username']} ({profile['role']})")
    
    # 4. Listar productos
    print("\n4. Listando productos...")
    products = client.list_products(limit=5)
    print(f"✅ Total: {products['total']} productos")
    
    # 5. Logout
    print("\n5. Cerrando sesión...")
    if client.logout():
        print("✅ Logout exitoso")
```

### Uso Rápido

```python
# imports
from requests import post, get

# Login
response = post("http://localhost:8000/api/v1/auth/login", json={
    "username": "admin",
    "password": "admin123"
})
token = response.json()["access_token"]

# Usar token
headers = {"Authorization": f"Bearer {token}"}
user = get("http://localhost:8000/api/v1/users/me", headers=headers).json()
print(user)
```

---

## 4. JavaScript + Fetch

Para usar en el navegador o Node.js.

### Código Completo

```javascript
class APIClient {
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
    this.accessToken = null;
  }

  getHeaders() {
    return {
      'Content-Type': 'application/json',
      ...(this.accessToken && { 'Authorization': `Bearer ${this.accessToken}` })
    };
  }

  async login(username, password) {
    const response = await fetch(`${this.baseUrl}/api/v1/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    
    if (response.ok) {
      const data = await response.json();
      this.accessToken = data.access_token;
      localStorage.setItem('refresh_token', data.refresh_token);
      return data;
    }
    throw new Error((await response.json()).detail);
  }

  async getMyProfile() {
    const response = await fetch(`${this.baseUrl}/api/v1/users/me`, {
      headers: this.getHeaders()
    });
    return response.json();
  }

  async listProducts(skip = 0, limit = 10) {
    const response = await fetch(
      `${this.baseUrl}/api/v1/products?skip=${skip}&limit=${limit}`
    );
    return response.json();
  }

  async logout() {
    await fetch(`${this.baseUrl}/api/v1/auth/logout`, {
      method: 'POST',
      headers: this.getHeaders()
    });
    this.accessToken = null;
    localStorage.removeItem('refresh_token');
  }
}

// ========== USO ==========

const client = new APIClient('http://localhost:8000');

// Login
await client.login('admin', 'admin123');
console.log('✅ Login exitoso');

// Mi perfil
const profile = await client.getMyProfile();
console.log('✅ Usuario:', profile.username);

// Listar productos
const products = await client.listProducts();
console.log('✅ Productos:', products);
```

### Uso Rápido

```javascript
// Login
const loginRes = await fetch('http://localhost:8000/api/v1/auth/login', {
  method: 'POST',
  body: JSON.stringify({ username: 'admin', password: 'admin123' })
});
const { access_token } = await loginRes.json();

// Usar token
const meRes = await fetch('http://localhost:8000/api/v1/users/me', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
const user = await meRes.json();
console.log(user);
```

---

## 5. Postman Collection

### Crear Colección

1. Abre Postman
2. **Collections** → **+ New**
3. Nombre: "JWT API"
4. **Create**

### Agregar Requests

#### 1. Login
- **Method**: POST
- **URL**: `{{base_url}}/api/v1/auth/login`
- **Body** (JSON):
  ```json
  {
    "username": "admin",
    "password": "admin123"
  }
  ```
- **Tests** (para guardar token):
  ```javascript
  var jsonData = pm.response.json();
  pm.environment.set("access_token", jsonData.access_token);
  pm.environment.set("refresh_token", jsonData.refresh_token);
  ```

#### 2. Get Me
- **Method**: GET
- **URL**: `{{base_url}}/api/v1/users/me`
- **Headers**:
  - Key: `Authorization`
  - Value: `Bearer {{access_token}}`

#### 3. List Products
- **Method**: GET
- **URL**: `{{base_url}}/api/v1/products?skip=0&limit=10`

#### 4. Create Product
- **Method**: POST
- **URL**: `{{base_url}}/api/v1/products`
- **Headers**:
  - Key: `Authorization`
  - Value: `Bearer {{access_token}}`
- **Body** (JSON):
  ```json
  {
    "name": "Laptop",
    "description": "Test",
    "price": 999.99,
    "stock": 10,
    "category": "Tech",
    "brand": "Dell",
    "sku": "DELL-001"
  }
  ```

### Usar Colección

1. Click en **Environment** (arriba)
2. **+ New**
3. Name: "Desarrollo"
4. Variable `base_url` = `http://localhost:8000`
5. **Save**
6. Ahora corre requests que automáticamente usan variables

---

## 🎯 Casos de Uso Comunes

### Flujo: Registro → Login → Ver Perfil → Logout

**cURL:**
```bash
# 1. Registrarse
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"new@ejemplo.com","username":"newuser","password":"Test123!","full_name":"New User"}'

# 2. Login
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","password":"Test123!"}' | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

# 3. Ver perfil
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer $TOKEN"

# 4. Logout
curl -X POST http://localhost:8000/api/v1/auth/logout \
  -H "Authorization: Bearer $TOKEN"
```

**JavaScript:**
```javascript
// 1. Registrarse
await fetch('http://localhost:8000/api/v1/auth/register', {
  method: 'POST',
  body: JSON.stringify({
    email: "new@ejemplo.com",
    username: "newuser",
    password: "Test123!",
    full_name: "New User"
  })
});

// 2. Login
const loginRes = await fetch('http://localhost:8000/api/v1/auth/login', {
  method: 'POST',
  body: JSON.stringify({ username: "newuser", password: "Test123!" })
});
const token = (await loginRes.json()).access_token;

// 3. Ver perfil
const me = await fetch('http://localhost:8000/api/v1/users/me', {
  headers: { 'Authorization': `Bearer ${token}` }
});
console.log(await me.json());

// 4. Logout
await fetch('http://localhost:8000/api/v1/auth/logout', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` }
});
```

---

**Ver [docs/DEVELOPMENT.md](DEVELOPMENT.md) para entender conceptos**
