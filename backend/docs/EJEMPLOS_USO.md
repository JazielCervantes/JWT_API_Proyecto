# 🚀 Ejemplos de Uso de la API

Este documento contiene ejemplos prácticos para usar la API con diferentes herramientas.

---

## 📋 Tabla de Contenidos

1. [Swagger UI](#swagger-ui)
2. [cURL (Terminal)](#curl-terminal)
3. [Python + Requests](#python-requests)
4. [JavaScript + Fetch](#javascript-fetch)
5. [Postman](#postman)

---

## 1. Swagger UI

La forma más fácil de probar la API.

### Pasos:

1. **Inicia el servidor**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. **Abre Swagger UI**
   - URL: http://localhost:8000/docs

3. **Prueba el login**
   - Expande `/api/auth/login`
   - Click en "Try it out"
   - Ingresa:
     ```json
     {
       "username": "admin",
       "password": "admin123"
     }
     ```
   - Click "Execute"
   - Copia el `access_token`

4. **Autoriza tu sesión**
   - Click en el botón "Authorize" 🔒 (arriba a la derecha)
   - Pega: `Bearer <tu_access_token>`
   - Click "Authorize"

5. **Prueba endpoints protegidos**
   - Ahora puedes probar `/api/users/me` y otros endpoints

---

## 2. cURL (Terminal)

Ideal para scripts y testing rápido.

### Registro de Usuario

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@ejemplo.com",
    "username": "testuser",
    "password": "password123",
    "full_name": "Usuario de Prueba"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Obtener Mi Perfil

```bash
curl -X GET http://localhost:8000/api/users/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Listar Productos

```bash
# Sin filtros
curl -X GET http://localhost:8000/api/products

# Con paginación
curl -X GET "http://localhost:8000/api/products?skip=0&limit=10"

# Con filtros
curl -X GET "http://localhost:8000/api/products?search=laptop&min_price=500&max_price=2000"
```

### Crear Producto (Admin)

```bash
curl -X POST http://localhost:8000/api/products \
  -H "Authorization: Bearer <tu_token_admin>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop HP Pavilion",
    "description": "Laptop para uso general",
    "price": 799.99,
    "stock": 15,
    "category": "Electrónica",
    "brand": "HP",
    "sku": "HP-PAV-001"
  }'
```

### Actualizar Producto (Admin)

```bash
curl -X PUT http://localhost:8000/api/products/1 \
  -H "Authorization: Bearer <tu_token_admin>" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 749.99,
    "stock": 20
  }'
```

### Eliminar Producto (Admin)

```bash
curl -X DELETE http://localhost:8000/api/products/1 \
  -H "Authorization: Bearer <tu_token_admin>"
```

### Refrescar Token

```bash
curl -X POST http://localhost:8000/api/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

---

## 3. Python + Requests

Perfecto para integración con scripts Python.

### Instalación

```bash
pip install requests
```

### Código de Ejemplo

```python
import requests
import json

# Configuración
BASE_URL = "http://localhost:8000"
session = requests.Session()

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.access_token = None
        self.refresh_token = None
    
    def register(self, email, username, password, full_name):
        """Registrar nuevo usuario"""
        url = f"{self.base_url}/api/auth/register"
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
        url = f"{self.base_url}/api/auth/login"
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens["access_token"]
            self.refresh_token = tokens["refresh_token"]
            return tokens
        else:
            raise Exception(f"Error en login: {response.json()}")
    
    def get_headers(self):
        """Obtener headers con autenticación"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def get_my_profile(self):
        """Obtener mi perfil"""
        url = f"{self.base_url}/api/users/me"
        response = requests.get(url, headers=self.get_headers())
        return response.json()
    
    def list_products(self, skip=0, limit=10, **filters):
        """Listar productos con filtros"""
        url = f"{self.base_url}/api/products"
        params = {"skip": skip, "limit": limit, **filters}
        response = requests.get(url, params=params)
        return response.json()
    
    def create_product(self, product_data):
        """Crear producto (admin)"""
        url = f"{self.base_url}/api/products"
        response = requests.post(
            url, 
            json=product_data, 
            headers=self.get_headers()
        )
        return response.json()
    
    def update_product(self, product_id, update_data):
        """Actualizar producto (admin)"""
        url = f"{self.base_url}/api/products/{product_id}"
        response = requests.put(
            url,
            json=update_data,
            headers=self.get_headers()
        )
        return response.json()
    
    def delete_product(self, product_id):
        """Eliminar producto (admin)"""
        url = f"{self.base_url}/api/products/{product_id}"
        response = requests.delete(url, headers=self.get_headers())
        return response.status_code == 204
    
    def refresh_access_token(self):
        """Refrescar el access token"""
        url = f"{self.base_url}/api/auth/refresh"
        data = {"refresh_token": self.refresh_token}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens["access_token"]
            self.refresh_token = tokens["refresh_token"]
            return tokens
        else:
            raise Exception(f"Error al refrescar token: {response.json()}")

# ============ EJEMPLO DE USO ============

if __name__ == "__main__":
    # Crear cliente
    client = APIClient(BASE_URL)
    
    # 1. Registrar usuario
    print("1. Registrando usuario...")
    try:
        user = client.register(
            email="test@ejemplo.com",
            username="testuser",
            password="password123",
            full_name="Usuario de Prueba"
        )
        print(f"✅ Usuario registrado: {user['username']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 2. Login
    print("\n2. Iniciando sesión...")
    try:
        tokens = client.login("admin", "admin123")
        print(f"✅ Login exitoso")
        print(f"Access Token: {tokens['access_token'][:50]}...")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 3. Obtener perfil
    print("\n3. Obteniendo perfil...")
    try:
        profile = client.get_my_profile()
        print(f"✅ Usuario: {profile['username']} ({profile['role']})")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 4. Listar productos
    print("\n4. Listando productos...")
    try:
        products = client.list_products(limit=5)
        print(f"✅ Total productos: {products['total']}")
        for product in products['products']:
            print(f"  - {product['name']}: ${product['price']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 5. Crear producto (si es admin)
    print("\n5. Creando producto...")
    try:
        new_product = client.create_product({
            "name": "Producto de Prueba",
            "description": "Creado desde Python",
            "price": 99.99,
            "stock": 10,
            "category": "Test",
            "brand": "Python",
            "sku": "PY-TEST-001"
        })
        print(f"✅ Producto creado: {new_product['name']} (ID: {new_product['id']})")
    except Exception as e:
        print(f"❌ Error: {e}")
```

---

## 4. JavaScript + Fetch

Para usar en frontend o Node.js.

### Código de Ejemplo

```javascript
class APIClient {
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
    this.accessToken = null;
    this.refreshToken = null;
  }

  // Helper para headers
  getHeaders() {
    return {
      'Content-Type': 'application/json',
      ...(this.accessToken && { 
        'Authorization': `Bearer ${this.accessToken}` 
      })
    };
  }

  // Registro
  async register(email, username, password, fullName) {
    const response = await fetch(`${this.baseUrl}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email,
        username,
        password,
        full_name: fullName
      })
    });
    return response.json();
  }

  // Login
  async login(username, password) {
    const response = await fetch(`${this.baseUrl}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    
    if (response.ok) {
      const data = await response.json();
      this.accessToken = data.access_token;
      this.refreshToken = data.refresh_token;
      
      // Guardar en localStorage (opcional)
      localStorage.setItem('access_token', this.accessToken);
      localStorage.setItem('refresh_token', this.refreshToken);
      
      return data;
    }
    throw new Error('Login failed');
  }

  // Obtener perfil
  async getMyProfile() {
    const response = await fetch(`${this.baseUrl}/api/users/me`, {
      headers: this.getHeaders()
    });
    return response.json();
  }

  // Listar productos
  async listProducts(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const response = await fetch(
      `${this.baseUrl}/api/products?${queryString}`
    );
    return response.json();
  }

  // Crear producto
  async createProduct(productData) {
    const response = await fetch(`${this.baseUrl}/api/products`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(productData)
    });
    return response.json();
  }

  // Actualizar producto
  async updateProduct(productId, updateData) {
    const response = await fetch(
      `${this.baseUrl}/api/products/${productId}`,
      {
        method: 'PUT',
        headers: this.getHeaders(),
        body: JSON.stringify(updateData)
      }
    );
    return response.json();
  }

  // Eliminar producto
  async deleteProduct(productId) {
    const response = await fetch(
      `${this.baseUrl}/api/products/${productId}`,
      {
        method: 'DELETE',
        headers: this.getHeaders()
      }
    );
    return response.ok;
  }

  // Refrescar token
  async refreshAccessToken() {
    const response = await fetch(`${this.baseUrl}/api/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        refresh_token: this.refreshToken 
      })
    });
    
    if (response.ok) {
      const data = await response.json();
      this.accessToken = data.access_token;
      this.refreshToken = data.refresh_token;
      
      localStorage.setItem('access_token', this.accessToken);
      localStorage.setItem('refresh_token', this.refreshToken);
      
      return data;
    }
    throw new Error('Token refresh failed');
  }
}

// ============ EJEMPLO DE USO ============

(async () => {
  const client = new APIClient('http://localhost:8000');
  
  try {
    // Login
    console.log('Iniciando sesión...');
    await client.login('admin', 'admin123');
    console.log('✅ Login exitoso');
    
    // Obtener perfil
    const profile = await client.getMyProfile();
    console.log(`Usuario: ${profile.username}`);
    
    // Listar productos
    const products = await client.listProducts({ limit: 5 });
    console.log(`Total productos: ${products.total}`);
    
  } catch (error) {
    console.error('Error:', error);
  }
})();
```

### Uso en Vue.js

```vue
<script setup>
import { ref, onMounted } from 'vue';

const products = ref([]);
const loading = ref(false);
const accessToken = ref(localStorage.getItem('access_token'));

async function fetchProducts() {
  loading.value = true;
  try {
    const response = await fetch('http://localhost:8000/api/products');
    const data = await response.json();
    products.value = data.products;
  } catch (error) {
    console.error('Error:', error);
  } finally {
    loading.value = false;
  }
}

async function login(username, password) {
  const response = await fetch('http://localhost:8000/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  
  const data = await response.json();
  accessToken.value = data.access_token;
  localStorage.setItem('access_token', data.access_token);
}

onMounted(() => {
  fetchProducts();
});
</script>

<template>
  <div>
    <h1>Productos</h1>
    <div v-if="loading">Cargando...</div>
    <div v-else>
      <div v-for="product in products" :key="product.id">
        {{ product.name }} - ${{ product.price }}
      </div>
    </div>
  </div>
</template>
```

---

## 5. Postman

### Configuración Inicial

1. **Crear nueva colección**: "JWT API"

2. **Configurar variables de entorno**:
   - `base_url`: `http://localhost:8000`
   - `access_token`: (se llenará automáticamente)
   - `refresh_token`: (se llenará automáticamente)

3. **Configurar autorización**:
   - Type: Bearer Token
   - Token: `{{access_token}}`

### Script para Login (Tests tab)

```javascript
// Guardar tokens automáticamente después del login
if (pm.response.code === 200) {
    const jsonData = pm.response.json();
    pm.environment.set("access_token", jsonData.access_token);
    pm.environment.set("refresh_token", jsonData.refresh_token);
    console.log("✅ Tokens guardados");
}
```

### Colección de Requests

1. **Login**
   - POST `{{base_url}}/api/auth/login`
   - Body: 
     ```json
     {
       "username": "admin",
       "password": "admin123"
     }
     ```

2. **Get My Profile**
   - GET `{{base_url}}/api/users/me`
   - Auth: Bearer {{access_token}}

3. **List Products**
   - GET `{{base_url}}/api/products?limit=10`

4. **Create Product**
   - POST `{{base_url}}/api/products`
   - Auth: Bearer {{access_token}}
   - Body:
     ```json
     {
       "name": "Test Product",
       "price": 99.99,
       "stock": 10
     }
     ```

---

## 📝 Notas Importantes

1. **Tokens expiran**: El access token expira en 30 minutos por defecto
2. **Refrescar tokens**: Usa el endpoint `/api/auth/refresh` cuando el access token expire
3. **Errores 401**: Significa que el token expiró o es inválido
4. **Errores 403**: Significa que no tienes permisos para esa acción
5. **CORS**: Asegúrate de que tu frontend esté en la lista de orígenes permitidos en `.env`

---

## 🎯 Flujo Recomendado

1. **Registro** → Crear cuenta
2. **Login** → Obtener tokens
3. **Usar API** → Hacer peticiones con access token
4. **Token expira** → Usar refresh token
5. **Logout** → Invalidar tokens
